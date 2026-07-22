from typing import List

from pfc.domain.exceptions import ConverterNotFoundError
from pfc.domain.protocols import Converter


class ConversionRegistry:
    def __init__(self) -> None:
        self._converters: List[Converter] = []

    def register(self, converter: Converter) -> None:
        """Register a new converter in the registry."""
        self._converters.append(converter)

    def get(self, source_format: str, target_format: str) -> Converter:
        """Get the first converter that supports the requested conversion."""
        for converter in self._converters:
            if converter.supports(source_format, target_format):
                return converter
        raise ConverterNotFoundError(f"No converter found for {source_format} -> {target_format}")

    def get_all(self) -> List[Converter]:
        """Return all registered converters."""
        return list(self._converters)
