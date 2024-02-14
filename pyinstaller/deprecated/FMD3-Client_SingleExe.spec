from pyinstaller.common import binaries,datas,hiddenimports, raw_version, system, a, pyz, exe, coll

output_name = f'FMD3-AllInOneFMD3_{raw_version}_{system()}'

a.scripts = ['../src/FMD3_Tkinter/__main__.py']

exe.name = output_name
coll.name = output_name