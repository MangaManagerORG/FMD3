# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\src\\FMD3_Api\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('..\\src/FMD3','FMD3'),
    ('..\\src/FMD3_API','FMD3_API')
    ],
    hiddenimports=["FMD3"],
    hookspath=["pyinstaller/extra_hooks"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FMD3-API',
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
    name='FMD3-API',
)
