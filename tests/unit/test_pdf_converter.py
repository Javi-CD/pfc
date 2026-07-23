from pfc.infrastructure.converters.pdf_converter import (
    PdfToDocxConverter,
    PdfToTxtConverter,
)


def test_pdf_to_txt_supports():
    converter = PdfToTxtConverter()
    assert converter.supports("pdf", "txt")
    assert not converter.supports("txt", "pdf")

def test_pdf_to_docx_supports():
    converter = PdfToDocxConverter()
    assert converter.supports("pdf", "docx")
    assert not converter.supports("docx", "pdf")
