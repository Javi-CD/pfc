import json
import pytest

from pfc.infrastructure.converters.csv_converter import CsvToJsonConverter
from pfc.infrastructure.converters.json_converter import JsonToCsvConverter
from pfc.domain.exceptions import ConversionError

def test_csv_to_json_converter(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25", encoding="utf-8")
    json_file = tmp_path / "test.json"
    
    converter = CsvToJsonConverter()
    assert converter.supports("csv", "json")
    assert not converter.supports("json", "csv")
    
    result = converter.convert(csv_file, json_file)
    
    assert result.source_format == "csv"
    assert result.target_format == "json"
    
    data = json.loads(json_file.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == "25"


def test_json_to_csv_converter(tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]', encoding="utf-8")
    csv_file = tmp_path / "test.csv"
    
    converter = JsonToCsvConverter()
    assert converter.supports("json", "csv")
    assert not converter.supports("csv", "json")
    
    result = converter.convert(json_file, csv_file)
    
    assert result.source_format == "json"
    assert result.target_format == "csv"
    
    lines = csv_file.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "name,age"
    assert lines[1] == "Alice,30"


def test_json_to_csv_invalid_format(tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text('{"name": "Alice"}', encoding="utf-8")
    csv_file = tmp_path / "test.csv"
    
    converter = JsonToCsvConverter()
    with pytest.raises(ConversionError):
        converter.convert(json_file, csv_file)
