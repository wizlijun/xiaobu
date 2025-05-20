"""
This is a setup.py script for py2app

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os
import sys

# 为环境变量设置QT插件路径
import PyQt5
os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins", "platforms")
# 添加Mac上下文菜单支持
os.environ['QT_MAC_WANTS_LAYER'] = '1'

APP = ['sharehtml.py']
DATA_FILES = ['icon.png']  # 使用icon.png替代logo.png作为数据文件
OPTIONS = {
    'argv_emulation': False,  # 禁用argv_emulation，避免Carbon框架依赖
    'packages': ['PyQt5'],
    'includes': ['sip', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
    'excludes': ['matplotlib', 'numpy', 'pandas', 'scipy', 'tkinter'],
    'iconfile': 'AppIcon.icns',  # 使用AppIcon.icns作为图标（支持半透明）
    'qt_plugins': ['platforms', 'imageformats', 'styles'],
    'frameworks': [],
    'resources': [],
    'plist': {
        'CFBundleName': 'ShareHTML',
        'CFBundleDisplayName': 'ShareHTML',
        'CFBundleGetInfoString': "分享HTML到网站",
        'CFBundleIdentifier': "net.xiaobu.ShareHTML",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2024, XiaoBu, All Rights Reserved",
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'CFBundleDocumentTypes': [],
        'LSEnvironment': {
            'QT_PLUGIN_PATH': '@executable_path/../Resources/lib/python3.13/PyQt5/Qt5/plugins',
            'QT_QPA_PLATFORM_PLUGIN_PATH': '@executable_path/../Resources/lib/python3.13/PyQt5/Qt5/plugins/platforms',
            'QT_MAC_WANTS_LAYER': '1'
        }
    }
}

setup(
    app=APP,
    name='ShareHTML',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
