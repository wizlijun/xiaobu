#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

APP = ['sharehtml.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],
    'plist': {
        'CFBundleName': '快捷分享HTML',
        'CFBundleDisplayName': '快捷分享HTML',
        'CFBundleGetInfoString': "快速分享HTML文件到服务器",
        'CFBundleIdentifier': "net.xiaobu.sharehtml",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2023, 小布, All Rights Reserved",
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