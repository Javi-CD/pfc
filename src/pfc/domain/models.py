from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionFormat:
    source: str
    target: str


@dataclass(frozen=True)
class ConversionRequest:
    source: Path
    destination: Path
    source_format: str
    target_format: str


@dataclass(frozen=True)
class ConversionResult:
    source: Path
    destination: Path
    source_format: str
    target_format: str
    size_before: int
    size_after: int
