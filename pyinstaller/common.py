# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

from platform import system

ver_path = "src/FMD3_API/__version__.py"
with open(ver_path, 'r') as version_file:
    version_globals = {}
    exec(version_file.read(), version_globals)
    raw_version = version_globals.get('__version__',"")


datas = []
binaries = []
hiddenimports = ["FMD3", "PIL.ImageFont", "PIL.ImageDraw"]
collects = [collect_all('tkinterweb'), collect_all('pygubu')]
for ret in collects:
    datas += ret[0]
    binaries += ret[1]
    hiddenimports += ret[2]


