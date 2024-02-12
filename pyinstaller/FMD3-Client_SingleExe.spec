# -*- mode: python ; coding: utf-8 -*-

from platform import system
ver_path = "../src/FMD3_Tkinter/__version__.py"
with open(ver_path, 'r') as version_file:
    version_globals = {}
    exec(version_file.read(), version_globals)
    raw_version = version_globals.get('__version__')

output_name = f'FMD3-AllInOneFMD3_{raw_version}_{system()}'


a = Analysis(
    ['../src/FMD3_Tkinter/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src/FMD3','FMD3'),
        ('../src/FMD3_Tkinter','FMD3_Tkinter')
    ],
    hiddenimports=["FMD3"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=output_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    hide_console='hide-early',
)
