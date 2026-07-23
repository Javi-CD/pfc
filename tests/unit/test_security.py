import os
from pathlib import Path
import pytest
from PIL import Image

from pfc.domain.exceptions import FileTooLargeError, SecurityViolationError
from pfc.domain.security import (
    SecurityConfig,
    validate_file_size,
    validate_mime_type,
    validate_safe_path,
)


def test_validate_file_size_success(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("A" * 10)
    config = SecurityConfig(max_file_size_bytes=20)

    # Should not raise
    validate_file_size(test_file, config)


def test_validate_file_size_exceeded(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("A" * 30)
    config = SecurityConfig(max_file_size_bytes=20)

    with pytest.raises(FileTooLargeError):
        validate_file_size(test_file, config)


def test_validate_safe_path_success(tmp_path: Path):
    config = SecurityConfig(prevent_path_traversal=True)
    out_file = tmp_path / "out.txt"
    # Should not raise
    validate_safe_path(out_file, config)


def test_validate_safe_path_traversal():
    config = SecurityConfig(prevent_path_traversal=True)

    if os.name == "nt":
        win_dir = os.environ.get("WINDIR", "C:\\Windows")
        bad_path = Path(win_dir) / "System32" / "hack.txt"
    else:
        bad_path = Path("/etc/passwd")

    with pytest.raises(
        SecurityViolationError, match="Path traversal protection triggered"
    ):
        validate_safe_path(bad_path, config)


def test_validate_mime_type_success(tmp_path: Path):
    config = SecurityConfig(validate_mime_type=True)
    img_file = tmp_path / "real_image.jpg"
    img = Image.new("RGB", (10, 10))
    img.save(img_file)

    # Should not raise
    validate_mime_type(img_file, "jpg", config)


def test_validate_mime_type_mismatch(tmp_path: Path):
    config = SecurityConfig(validate_mime_type=True)
    png_file = tmp_path / "fake_jpg.jpg"
    img = Image.new("RGB", (10, 10))
    img.save(png_file, format="PNG")

    with pytest.raises(SecurityViolationError, match="MIME type validation failed"):
        validate_mime_type(png_file, "jpg", config)


def test_validate_mime_type_unknown(tmp_path: Path):
    # Tests that unknown types fallback to passing (leniency)
    config = SecurityConfig(validate_mime_type=True)
    fake_img = tmp_path / "fake_image.jpg"
    fake_img.write_text("This is not a real image, it's just text.")

    # Should not raise since filetype returns None
    validate_mime_type(fake_img, "jpg", config)
