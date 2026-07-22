import sys
from pathlib import Path

import typer
from rich.console import Console

from pfc.application.conversion_registry import ConversionRegistry
from pfc.application.converter_service import ConversionService
from pfc.domain.exceptions import ConversionError
from pfc.infrastructure.converters.csv_converter import CsvToJsonConverter
from pfc.infrastructure.converters.json_converter import JsonToCsvConverter

app = typer.Typer(
    name="pfc",
    help="PFC (Python File Converter) - File conversion tool",
    add_completion=False,
)
console = Console()


def get_registry() -> ConversionRegistry:
    registry = ConversionRegistry()
    registry.register(CsvToJsonConverter())
    registry.register(JsonToCsvConverter())
    return registry


def get_service() -> ConversionService:
    return ConversionService(get_registry())


@app.command()
def convert(
    source: Path = typer.Argument(
        ..., help="Path to the input file"
    ),
    to: str = typer.Option(
        ..., "--to", help="Target format extension (e.g. json, csv)"
    ),
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
        with console.status(f"[bold green]Converting {source.name} to {target_format}...[/]"):
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
def list_formats():
    """List all supported format conversions."""
    registry = get_registry()
    converters = registry.get_all()

    console.print("[bold]Supported conversions:[/]")
    console.print()

    if not converters:
        console.print("No converters registered.")
        return

    for converter in converters:
        if isinstance(converter, CsvToJsonConverter):
            console.print("  CSV  -> JSON")
        elif isinstance(converter, JsonToCsvConverter):
            console.print("  JSON -> CSV")
        else:
            console.print(f"  {converter.__class__.__name__}")


@app.command()
def info(
    source: Path = typer.Argument(..., help="Path to the file")
):
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
