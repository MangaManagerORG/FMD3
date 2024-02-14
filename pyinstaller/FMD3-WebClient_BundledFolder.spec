# -*- mode: python ; coding: utf-8 -*-
from platform import system
from pyinstaller.common import Analysis, COLLECT, EXE, raw_version
from PyInstaller.building.api import PYZ

output_name = f'FMD3-WebClient_{raw_version}_{system()}'
scripts = ['../src/FMD3_Tkinter/run_web_client.py']

a = Analysis(scripts=scripts)

pyz = PYZ(a.pure)

exe = EXE(a, pyz, output_name)

coll = COLLECT(a, exe, output_name)


