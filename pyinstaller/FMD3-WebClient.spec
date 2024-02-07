# -*- mode: python ; coding: utf-8 -*-

for root, dirs, files in os.walk("../"):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

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
    [],
    exclude_binaries=True,
    name='FMD3-WebClient',
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
    name='FMD3-WebClient',
)
