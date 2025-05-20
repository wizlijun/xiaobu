#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import sys
from PyQt5 import QtCore
import glob

# 获取Qt库路径
qt_path = os.path.dirname(os.path.dirname(QtCore.__file__))
qt_plugins_path = os.path.join(qt_path, "Qt5", "plugins")
qt_platforms_path = os.path.join(qt_plugins_path, "platforms")
qt_lib_path = qt_path

# 查找所有Qt库文件
qt_libs = glob.glob(os.path.join(qt_path, "**", "*.so"), recursive=True)
qt_libs += glob.glob(os.path.join(qt_path, "**", "*.dylib"), recursive=True)

APP = ['sharehtml.py']
OPTIONS = {
    'argv_emulation': False,  # 设置为False以避免Carbon.framework依赖问题
    'packages': ['PyQt5'],
    'includes': ['sip'],
    'excludes': ['tkinter', 'matplotlib'],
    # 确保包含所有Qt平台插件
    'qt_plugins': ['platforms', 'styles', 'imageformats', 'printsupport'],
    'include_plugins': [qt_plugins_path],
    # 使用绝对路径引用系统Python
    'matplotlib_backends': [],
    # 包含Python框架
    'frameworks': ['/opt/homebrew/opt/python@3.13/Frameworks/Python.framework'],
    # 确保包含所有Qt库
    'dylib_excludes': ['libqcocoa.dylib'],  # 排除，因为我们会单独处理
    'resources': [],
    'iconfile': 'appicon.icns' if os.path.exists('appicon.icns') else None,
    'plist': {
        'CFBundleName': '快捷分享HTML',
        'CFBundleDisplayName': '快捷分享HTML',
        'CFBundleGetInfoString': "快速分享HTML文件到服务器",
        'CFBundleIdentifier': "net.xiaobu.sharehtml",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2023, 小布, All Rights Reserved",
        'LSEnvironment': {
            'QT_PLUGIN_PATH': '@executable_path/../PlugIns',
            'QT_QPA_PLATFORM_PLUGIN_PATH': '@executable_path/../PlugIns/platforms'
        },
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'HTML Document',
                'CFBundleTypeExtensions': ['html', 'htm'],
                'CFBundleTypeRole': 'Viewer',
            },
        ],
    }
}

setup(
    app=APP,
    name='快捷分享HTML',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 