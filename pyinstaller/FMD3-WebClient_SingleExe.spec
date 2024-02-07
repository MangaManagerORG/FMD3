# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../src/FMD3_Tkinter/run_web_client.py'],
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
    name='FMD3-WebClient',
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
