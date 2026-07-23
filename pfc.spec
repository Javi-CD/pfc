# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

datas = []
datas += copy_metadata('pfc')


a = Analysis(
    ['src\\pfc\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pfc.infrastructure.converters.csv_converter', 'pfc.infrastructure.converters.json_converter', 'pfc.infrastructure.converters.xlsx_converter', 'pfc.infrastructure.converters.image_converter', 'pfc.infrastructure.converters.pdf_converter', 'pfc.infrastructure.converters.docx_converter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pfc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
