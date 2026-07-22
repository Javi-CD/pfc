from pathlib import Path

from PIL import Image

from pfc.domain.exceptions import ConversionError
from pfc.domain.models import ConversionResult


class ImageConverter:
    SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "webp"}

    def supports(self, source_format: str, target_format: str) -> bool:
        src = source_format.lower()
        tgt = target_format.lower()
        if tgt == "jpg":
            tgt = "jpeg"
        if src == "jpg":
            src = "jpeg"
        return (
            src in self.SUPPORTED_FORMATS
            and tgt in self.SUPPORTED_FORMATS
            and src != tgt
        )

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        size_before = source.stat().st_size
        try:
            with Image.open(source) as img:
                target_format = destination.suffix.lstrip(".").lower()
                # If target is JPEG and image has alpha channel, convert to RGB
                if target_format in ("jpg", "jpeg") and img.mode in ("RGBA", "LA", "P"):
                    rgb_img = img.convert("RGB")
                    rgb_img.save(destination)
                else:
                    img.save(destination)
        except Exception as e:
            raise ConversionError(f"Failed to convert image: {e}")

        size_after = destination.stat().st_size
        return ConversionResult(
            source=source,
            destination=destination,
            source_format=source.suffix.lstrip(".").lower(),
            target_format=target_format,
            size_before=size_before,
            size_after=size_after,
        )
