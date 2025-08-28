# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('lang', 'lang'),
        ('pics', 'pics'),
        ('icon.ico', '.'),
        ('palia_config.json', '.'),
        ('palia_garden_optimizer.py', '.'),
        ('garden.py', '.'),
        ('crops.py', '.'),
        ('config.py', '.'),
        ('language.py', '.'),
        ('ui_utils.py', '.'),
        ('__init__.py', '.'),
    ],
    hiddenimports=[
        'palia_garden_optimizer',
        'garden',
        'crops',
        'config',
        'language',
        'ui_utils',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'json',
        'os',
        'sys',
        'argparse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PaliaGardenOptimizer',
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
    icon='icon.ico',
    version='version_info.py'
)
