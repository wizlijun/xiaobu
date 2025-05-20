# 快捷分享HTML应用

一个用于快速分享HTML文件的macOS桌面应用，能够将HTML文件复制到Git仓库并推送到服务器，然后生成可分享的链接。

## 功能特点

- 支持在Finder中右键选择以"打开方式"打开HTML文件
- 允许用户自定义本地Git仓库路径
- 允许用户自定义分享脚本路径
- 允许用户自定义网站地址
- 提供日志查看功能，方便排查问题
- 自动复制分享链接到剪贴板

## 依赖项

- Python 3.6+
- PyQt5

## 安装依赖

```bash
pip3 install -r requirements.txt
```

## 使用方法

1. 直接运行脚本：

```bash
python3 sharehtml.py
```

2. 或者通过命令行参数指定HTML文件：

```bash
python3 sharehtml.py /path/to/your/file.html
```

3. 也可以将应用打包为macOS应用程序，然后在Finder中右键HTML文件，选择"打开方式"，选择sharehtml.app进行打开。

## 打包为应用程序

可以使用py2app将脚本打包为macOS应用程序：

1. 安装py2app：

```bash
pip3 install py2app
```

2. 创建setup.py文件：

```python
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
```

3. 执行打包命令：

```bash
python3 setup.py py2app
```

打包后的应用程序将位于dist目录中。 