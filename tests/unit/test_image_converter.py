from pathlib import Path
from PIL import Image
from pfc.infrastructure.converters.image_converter import ImageConverter

def test_image_converter_supports():
    converter = ImageConverter()
    assert converter.supports("png", "jpg")
    assert converter.supports("jpg", "webp")
    assert not converter.supports("png", "png")
    assert not converter.supports("bmp", "jpg")

def test_image_converter_png_to_jpg(tmp_path: Path):
    png_file = tmp_path / "test.png"
    img = Image.new("RGBA", (10, 10), (255, 0, 0, 128))
    img.save(png_file)

    jpg_file = tmp_path / "test.jpg"
    converter = ImageConverter()
    
    result = converter.convert(png_file, jpg_file)

    assert result.source_format == "png"
    assert result.target_format == "jpg"
    assert jpg_file.exists()

    with Image.open(jpg_file) as out:
        assert out.format == "JPEG"
        assert out.mode == "RGB"
