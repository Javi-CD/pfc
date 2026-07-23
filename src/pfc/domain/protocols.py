from pathlib import Path
from typing import Protocol

from pfc.domain.models import ConversionResult


class Converter(Protocol):
    def supports(self, source_format: str, target_format: str) -> bool:
        """Check if this converter supports the given format conversion."""
        ...

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        """Perform the file conversion and return the result."""
        ...
