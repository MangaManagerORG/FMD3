from pyinstaller.common import binaries,datas,hiddenimports, raw_version, system
output_name = f'FMD3-Client_{raw_version}_{system()}'

a = Analysis(
    ['../src/FMD3_Tkinter/run_web_client.py'],
    pathex=[],
    binaries=binaries,
    datas=[
        ('../src/FMD3','FMD3'),
        ('../src/FMD3_Tkinter','FMD3_Tkinter')
    ] + datas,
    hiddenimports=hiddenimports,
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
