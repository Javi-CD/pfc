from typer.testing import CliRunner

from pfc.presentation.cli import app

runner = CliRunner()

def test_list_formats():
    result = runner.invoke(app, ["list-formats"])
    assert result.exit_code == 0
    assert "Loaded converters:" in result.stdout
    assert "CsvToJsonConverter" in result.stdout
    assert "JsonToCsvConverter" in result.stdout
    assert "CsvToXlsxConverter" in result.stdout
    assert "XlsxToCsvConverter" in result.stdout
    assert "ImageConverter" in result.stdout
    assert "PdfToTxtConverter" in result.stdout
    assert "PdfToDocxConverter" in result.stdout
    assert "DocxToTxtConverter" in result.stdout
    assert "TxtToDocxConverter" in result.stdout
    assert "DocxToPdfConverter" in result.stdout

def test_plugins_command():
    result = runner.invoke(app, ["plugins"])
    assert result.exit_code == 0
    assert "Registered Plugins:" in result.stdout
    assert "csv_to_json" in result.stdout
    assert "image_converter" in result.stdout

def test_info_command(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")
    
    result = runner.invoke(app, ["info", str(test_file)])
    assert result.exit_code == 0
    assert "File Information:" in result.stdout
    assert "Size:" in result.stdout

def test_info_file_not_found(tmp_path):
    test_file = tmp_path / "missing.txt"
    result = runner.invoke(app, ["info", str(test_file)])
    assert result.exit_code == 1
    assert "Error:" in result.stdout
