# -*- mode: python ; coding: utf-8 -*-
from platform import system
from pyinstaller.common import Analysis, COLLECT, EXE
from PyInstaller.building.api import PYZ

ver_path = "src/FMD3_Tkinter/__version__.py"
with open(ver_path, 'r') as version_file:
    version_globals = {}
    exec(version_file.read(), version_globals)
    raw_version = version_globals.get('__version__', "")

output_name = f'FMD3-Client_{raw_version}_{system()}'
scripts = ['../src/FMD3_Tkinter/run_web_client.py']

a = Analysis(scripts=scripts)

pyz = PYZ(a.pure)

exe = EXE(a, pyz, output_name)

coll = COLLECT(a, exe, output_name)


