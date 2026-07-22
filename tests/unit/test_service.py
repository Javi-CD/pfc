import pytest
from pathlib import Path

from pfc.application.conversion_registry import ConversionRegistry
from pfc.application.converter_service import ConversionService
from pfc.domain.exceptions import InvalidInputFileError, OutputFileExistsError
from tests.unit.test_registry import MockConverter


@pytest.fixture
def registry():
    reg = ConversionRegistry()
    reg.register(MockConverter("csv", "json"))
    return reg


@pytest.fixture
def service(registry):
    return ConversionService(registry)


def test_convert_invalid_input(service, tmp_path):
    invalid_source = tmp_path / "does_not_exist.csv"
    dest = tmp_path / "out.json"
    
    with pytest.raises(InvalidInputFileError):
        service.convert(invalid_source, dest, "csv", "json")


def test_convert_output_exists_no_overwrite(service, tmp_path):
    source = tmp_path / "in.csv"
    source.write_text("dummy")
    dest = tmp_path / "out.json"
    dest.write_text("exists")
    
    with pytest.raises(OutputFileExistsError):
        service.convert(source, dest, "csv", "json", overwrite=False)


def test_convert_success(service, tmp_path):
    source = tmp_path / "in.csv"
    source.write_text("dummy")
    dest = tmp_path / "out.json"
    
    result = service.convert(source, dest, "csv", "json")
    
    assert result.source == source
    assert result.destination == dest
    assert result.source_format == "csv"
    assert result.target_format == "json"
