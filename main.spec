# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
import os

# Collect everything from the ui/ folder
datas = [
    ('ui/*', 'ui'),
]

# Include any dynamically imported modules in ui/
hiddenimports = collect_submodules('ui')

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],  # Ensure it finds your local modules
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want terminal output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='main.app',
    icon=None,  # or 'resources/icon.icns' if you have one
    bundle_identifier='com.niharika.s3viewer',
    info_plist='Info.plist',
)
