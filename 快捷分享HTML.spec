# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['sharehtml.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='快捷分享HTML',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='appicon.icns',
)
app = BUNDLE(
    exe,
    name='快捷分享HTML.app',
    icon='appicon.icns',
    bundle_identifier='net.xiaobu.sharehtml',
    info_plist={
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtensions': ['html', 'htm'],
                'CFBundleTypeIconFile': 'appicon.icns',
                'CFBundleTypeName': 'HTML Document',
                'CFBundleTypeRole': 'Editor',
                'LSHandlerRank': 'Alternate',
            }
        ],
        'NSHumanReadableCopyright': 'Copyright © 2023 小布',
    },
)
