from pathlib import Path

import PyInstaller.__main__


def build():
    entry_point = str(Path("src/pfc/__main__.py"))

    PyInstaller.__main__.run(
        [
            entry_point,
            "--name=pfc",
            "--onefile",
            "--console",
            "--clean",
            "--hidden-import=pfc.infrastructure.converters.csv_converter",
            "--hidden-import=pfc.infrastructure.converters.json_converter",
            "--hidden-import=pfc.infrastructure.converters.xlsx_converter",
            "--hidden-import=pfc.infrastructure.converters.image_converter",
            "--hidden-import=pfc.infrastructure.converters.pdf_converter",
            "--hidden-import=pfc.infrastructure.converters.docx_converter",
            "--copy-metadata=pfc",
        ]
    )


if __name__ == "__main__":
    build()
