from pathlib import Path

import pytest

from pfc.application.conversion_registry import ConversionRegistry
from pfc.domain.exceptions import ConverterNotFoundError
from pfc.domain.models import ConversionResult


class MockConverter:
    def __init__(self, source_format: str, target_format: str):
        self._source = source_format
        self._target = target_format

    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format == self._source and target_format == self._target

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        return ConversionResult(source, destination, self._source, self._target, 10, 20)


def test_registry_register_and_get():
    registry = ConversionRegistry()
    converter = MockConverter("csv", "json")
    registry.register(converter)
    
    retrieved = registry.get("csv", "json")
    assert retrieved is converter


def test_registry_get_not_found():
    registry = ConversionRegistry()
    
    with pytest.raises(ConverterNotFoundError):
        registry.get("csv", "json")
