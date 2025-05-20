# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['sharehtml.py'],
    pathex=[],
    binaries=[],
    datas=[('plugins', 'plugins')],
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
    [],
    exclude_binaries=True,
    name='快捷分享HTML',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['appicon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='快捷分享HTML',
)
app = BUNDLE(
    coll,
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
        'LSEnvironment': {
            'QT_QPA_PLATFORM_PLUGIN_PATH': '@executable_path/../Resources/plugins/platforms',
            'QT_PLUGIN_PATH': '@executable_path/../Resources/plugins',
        },
    },
)
