import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from pfc.application.conversion_registry import ConversionRegistry
from pfc.application.converter_service import ConversionService
from pfc.domain.exceptions import ConversionError, ConverterNotFoundError
import importlib.metadata

app = typer.Typer(
    name="pfc",
    help="PFC (Python File Converter) - File conversion tool",
    add_completion=False,
)
console = Console()


def get_registry() -> ConversionRegistry:
    registry = ConversionRegistry()
    try:
        eps = importlib.metadata.entry_points(group="pfc.converters")
    except TypeError:
        # Fallback for older python, though we require >= 3.13
        eps_dict = importlib.metadata.entry_points()
        eps = getattr(eps_dict, "get", lambda k, d: [])("pfc.converters", [])  # type: ignore

    for ep in eps:
        try:
            converter_class = ep.load()
            registry.register(converter_class())
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to load plugin {ep.name}: {e}[/yellow]")

    return registry

def get_service() -> ConversionService:
    return ConversionService(get_registry())


def process_single_file(
    source: Path, destination: Path, source_format: str, target_format: str, overwrite: bool
) -> str:
    """Worker function for batch processing."""
    service = get_service()
    try:
        service.convert(source, destination, source_format, target_format, overwrite)
        return str(source)
    except ConverterNotFoundError:
        return f"SKIP:{source}:Unsupported format"
    except Exception as e:
        return f"ERROR:{source}:{e}"


@app.command()
def convert(
    source: Path = typer.Argument(..., help="Path to the input file"),
    to: str = typer.Option(..., "--to", help="Target format extension (e.g. json, csv)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-o", help="Overwrite the output file if it exists"
    ),
):
    """Convert a file to a specified format."""
    source_format = source.suffix.lstrip(".").lower()
    target_format = to.lower()

    if not source_format:
        console.print("[bold red]Error:[/] Input file must have an extension.")
        sys.exit(1)

    destination = source.with_suffix(f".{target_format}")

    service = get_service()
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f"[bold green]Converting {source.name} to {target_format}...", total=None
            )
            result = service.convert(
                source=source,
                destination=destination,
                source_format=source_format,
                target_format=target_format,
                overwrite=overwrite,
            )

        console.print("[bold green]✓ Conversion completed[/]")
        console.print(f"Input:  {result.source}")
        console.print(f"Output: {result.destination}")
        console.print(f"Size:   {result.size_before} bytes -> {result.size_after} bytes")
    except ConversionError as e:
        console.print(f"[bold red]Error:[/] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {e}")
        sys.exit(1)


@app.command()
def batch(
    directory: Path = typer.Argument(..., help="Path to the input directory"),
    to: str = typer.Option(..., "--to", help="Target format extension (e.g. json, csv)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-o", help="Overwrite the output files if they exist"
    ),
):
    """Convert all supported files in a directory to a specified format."""
    target_format = to.lower()

    if not directory.exists() or not directory.is_dir():
        console.print(f"[bold red]Error:[/] Directory does not exist or is not a directory: {directory}")
        sys.exit(1)

    files_to_convert = [
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lstrip(".").lower() != target_format
    ]

    if not files_to_convert:
        console.print("[yellow]No files found to process.[/]")
        return

    successful = 0
    failed = 0
    skipped = 0
    errors = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("[bold cyan]Processing batch...", total=len(files_to_convert))

        with ProcessPoolExecutor() as executor:
            futures = []
            for source in files_to_convert:
                source_format = source.suffix.lstrip(".").lower()
                destination = source.with_suffix(f".{target_format}")
                future = executor.submit(
                    process_single_file, source, destination, source_format, target_format, overwrite
                )
                futures.append(future)

            for future in as_completed(futures):
                result = future.result()
                if result.startswith("ERROR:"):
                    failed += 1
                    errors.append(result[6:])
                elif result.startswith("SKIP:"):
                    skipped += 1
                else:
                    successful += 1
                progress.advance(task)

    console.print("[bold green]Batch processing completed![/]")
    console.print(f"Successful: {successful}")
    if skipped > 0:
        console.print(f"Skipped (unsupported): {skipped}")
    if failed > 0:
        console.print(f"[bold red]Failed: {failed}[/]")
        for err in errors:
            console.print(f"[red]  - {err}[/]")


@app.command()
def list_formats():
    """List all loaded converters."""
    registry = get_registry()
    converters = registry.get_all()

    console.print("[bold]Loaded converters:[/]")
    console.print()

    if not converters:
        console.print("No converters registered.")
        return

    for converter in converters:
        console.print(f"  - {converter.__class__.__name__}")


@app.command()
def plugins():
    """List all registered plugins."""
    try:
        eps = importlib.metadata.entry_points(group="pfc.converters")
    except TypeError:
        eps_dict = importlib.metadata.entry_points()
        eps = getattr(eps_dict, "get", lambda k, d: [])("pfc.converters", [])  # type: ignore

    console.print("[bold]Registered Plugins:[/bold]")
    console.print()

    if not eps:
        console.print("No plugins found.")
        return

    for ep in eps:
        try:
            ep.load()
            console.print(f"  [green]✓[/green] [cyan]{ep.name}[/cyan] ({ep.value})")
        except Exception as e:
            console.print(f"  [red]✗[/red] [red]{ep.name}[/red] ({ep.value}) - Error: {e}")


@app.command()
def info(source: Path = typer.Argument(..., help="Path to the file")):
    """Get information about a file."""
    if not source.exists() or not source.is_file():
        console.print(f"[bold red]Error:[/] File does not exist: {source}")
        sys.exit(1)

    console.print("[bold]File Information:[/]")
    console.print(f"Name: {source.name}")
    console.print(f"Size: {source.stat().st_size} bytes")
    console.print(f"Format: {source.suffix.lstrip('.').lower()}")


if __name__ == "__main__":
    app()
