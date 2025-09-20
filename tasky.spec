# -*- mode: python ; coding: utf-8 -*-
import os
from sys import platform as sys_platform

a = Analysis(
    ['tasky.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join('files', 'resources', '*'), os.path.join('files', 'resources'))
    ],
    hiddenimports=['PyQt5'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=('tasky' if sys_platform.startswith("linux") else 'Tasky'),
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
    icon=['tlogo.ico'],
)