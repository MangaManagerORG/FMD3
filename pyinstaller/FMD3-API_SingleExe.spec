# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
datas = []
binaries=[]
hiddenimports = ["FMD3","PIL.ImageFont","PIL.ImageDraw"]
collects = [collect_all('tkinterweb'), collect_all('pygubu')]
for ret in collects:
    datas += ret[0]
    binaries += ret[1]
    hiddenimports += ret[2]

from platform import system
ver_path = "src/FMD3_API/__version__.py"
with open(ver_path, 'r') as version_file:
    version_globals = {}
    exec(version_file.read(), version_globals)
    raw_version = version_globals.get('__version__')

output_name = f'FMD3-Server_{raw_version}_{system()}'

a = Analysis(
    ['../src/FMD3_API/__main__.py'],
    pathex=[],
    binaries=binaries,
    datas=[('../src/FMD3','FMD3'),
    ('../src/FMD3_API','FMD3_API')
    ]+datas,
    hiddenimports=hiddenimports,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
