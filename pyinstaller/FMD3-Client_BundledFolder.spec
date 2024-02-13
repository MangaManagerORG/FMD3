# -*- mode: python ; coding: utf-8 -*-
from pyinstaller.common import binaries,datas,hiddenimports

a = Analysis(
    ['../src/FMD3_Tkinter/__main__.py'],
    pathex=[],
    binaries=binaries,
    datas=[
        ('../src/FMD3','FMD3'),
        ('../src/FMD3_Tkinter','FMD3_Tkinter'),
    ]+datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FMD3-Client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FMD3-Client',
)
