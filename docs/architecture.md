# PFC Architecture Guide

Welcome to the **Python File Converter (PFC)** architecture guide. If you are reading this, you probably want to understand how the tool works under the hood. You are in the right place.

## The Core Concept: Clean Architecture

In PFC we avoid cross-dependencies and messy code (spaghetti code). For this reason, we decided to adopt **Clean Architecture**. This means the project is divided into strict layers, where the inner layers (the domain) know absolutely nothing about the outer layers (infrastructure, terminal, or third-party libraries).

### The Layers

1. **Domain (`src/pfc/domain`)**:
   This is the heart of our application. Here we define *what* our system needs (models, errors, and protocols/interfaces), but we do not define *how* it is done. The `Converter` protocol lives here, establishing the rules: "If you want to be a converter, you must follow these rules".

   ```python
   # src/pfc/domain/protocols.py
   from typing import Protocol
   from pathlib import Path
   from .models import ConversionResult

   class Converter(Protocol):
       def supports(self, source_format: str, target_format: str) -> bool:
           ...
           
       def convert(self, source: Path, destination: Path) -> ConversionResult:
           ...
   ```

2. **Application (`src/pfc/application`)**:
   Here lies the business logic. We have our `ConversionRegistry` (a registry where we store available converters) and our `ConversionService` (the orchestrator in charge of coordinating the flow, checking security, and calling the appropriate converter).

   ```python
   # src/pfc/application/converter_service.py
   class ConversionService:
       def __init__(self, registry: ConversionRegistry, security_config: SecurityConfig | None = None):
           self._registry = registry
           self._security = security_config or SecurityConfig()
           
       def execute(self, source: Path, target_format: str, destination: Path) -> ConversionResult:
           # 1. Security Checks
           validate_safe_path(source, self._security)
           # 2. Find Converter
           converter = self._registry.get_converter(source.suffix[1:], target_format)
           # 3. Execute
           return converter.convert(source, destination)
   ```

3. **Infrastructure (`src/pfc/infrastructure`)**:
   This is where the dirty work happens. All the code that interacts with the operating system, or that depends on external libraries (like `openpyxl`, `Pillow`, or `pdf2docx`), lives in this layer. **If we decide to change the PDF library for a faster one tomorrow, we only modify this layer and the rest of the system remains untouched.**

4. **Presentation (`src/pfc/presentation`)**:
   The visible face of the project. Here we use `Typer` and `Rich` to display a beautiful and user-friendly Command Line Interface (CLI).

---

## Registry Pattern and Dependency Injection

One of the crown jewels in PFC is how we handle different formats.

Normally, converters are full of `if` and `elif` blocks (e.g., `if it's a pdf do this, if it's a docx do that...`). We avoid this by using the **Registry Pattern**.
Instead of having a hardcoded list, the `ConversionService` asks the `ConversionRegistry`: "Hey, I have a `.csv` file and I want it in `.json`. Do you have any converter that supports this?" and the registry returns the correct object.

### How are converters loaded?

We use the power of `importlib.metadata.entry_points`. This allows the registry to search the environment (or Python's configuration itself) for existing converters and instantiate them automatically upon startup. It is the magic behind our plugin architecture.

## Security by Default

In PFC, security is not an afterthought:

- **Zero Path Traversal:** We validate every path to ensure a malicious actor cannot attempt to overwrite system files using paths like `../../../../../Windows/System32/config`.
- **MIME Signature Validation:** We inspect the pure magic bytes of the file using `filetype`. This prevents someone from sneaking an `.exe` disguised with a `.jpg` extension.
- **Size Limits:** By default, we abort the conversion if a file exceeds 100 MB to prevent RAM exhaustion.

Thank you for reading. If you like this approach and want to contribute code, take a look at our [Plugins Guide](plugins.md).
