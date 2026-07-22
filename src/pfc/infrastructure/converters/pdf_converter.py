from pathlib import Path

from pdf2docx import Converter  # type: ignore
from pypdf import PdfReader

from pfc.domain.exceptions import ConversionError
from pfc.domain.models import ConversionResult


class PdfToTxtConverter:
    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format.lower() == "pdf" and target_format.lower() == "txt"

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        size_before = source.stat().st_size
        try:
            reader = PdfReader(source)
            text_content = []
            for page in reader.pages:
                text_content.append(page.extract_text() or "")

            with open(destination, "w", encoding="utf-8") as f:
                f.write("\n".join(text_content))
        except Exception as e:
            raise ConversionError(f"Failed to extract text from PDF: {e}")

        size_after = destination.stat().st_size
        return ConversionResult(
            source=source,
            destination=destination,
            source_format="pdf",
            target_format="txt",
            size_before=size_before,
            size_after=size_after,
        )


class PdfToDocxConverter:
    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format.lower() == "pdf" and target_format.lower() == "docx"

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        size_before = source.stat().st_size
        try:
            cv = Converter(str(source))
            cv.convert(str(destination))
            cv.close()
        except Exception as e:
            raise ConversionError(f"Failed to convert PDF to DOCX: {e}")

        size_after = destination.stat().st_size
        return ConversionResult(
            source=source,
            destination=destination,
            source_format="pdf",
            target_format="docx",
            size_before=size_before,
            size_after=size_after,
        )
