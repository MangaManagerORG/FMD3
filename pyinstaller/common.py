# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.api import EXE as EXE_, COLLECT as COLLECT_, PYZ
from PyInstaller.building.build_main import Analysis as Analysis_


ver_path = "src/FMD3_API/__version__.py"
with open(ver_path, 'r') as version_file:
    version_globals = {}
    exec(version_file.read(), version_globals)
    raw_version = version_globals.get('__version__', "")

datas = []
binaries = []
hiddenimports = ["FMD3", "PIL.ImageFont", "PIL.ImageDraw"]
collects = [collect_all('tkinterweb'), collect_all('pygubu'), collect_all("sv_ttk")]
for ret in collects:
    datas += ret[0]
    binaries += ret[1]
    hiddenimports += ret[2]


class Analysis(Analysis_):
    def __init__(self, scripts):
        super().__init__(scripts,
                         pathex=[],
                         binaries=binaries,
                         datas=[
                                   ('../src/FMD3', 'FMD3'),
                                   ('../src/FMD3_Tkinter', 'FMD3_Tkinter'),
                               ] + datas,
                         hiddenimports=hiddenimports,
                         hookspath=["pyinstaller/extra_hooks"],
                         hooksconfig={},
                         runtime_hooks=[],
                         excludes=[],
                         noarchive=False
                         )


class EXE(EXE_):
    def __init__(self, a, pyz, name):
        super().__init__(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name=name,
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None, )


class COLLECT(COLLECT_):
    def __init__(self, a, exe, name):
        super().__init__(exe,
                         a.binaries,
                         a.datas,
                         strip=False,
                         upx=True,
                         upx_exclude=[],
                         name=name, )

