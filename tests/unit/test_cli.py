from typer.testing import CliRunner

from pfc.presentation.cli import app

runner = CliRunner()

def test_list_formats():
    result = runner.invoke(app, ["list-formats"])
    assert result.exit_code == 0
    assert "Supported conversions:" in result.stdout
    assert "CSV  -> JSON" in result.stdout
    assert "JSON -> CSV" in result.stdout
    assert "CSV  -> XLSX" in result.stdout
    assert "XLSX -> CSV" in result.stdout

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
