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

3. 也可以将应用打包为macOS应用程序，然后在Finder中右键HTML文件，选择"打开方式"，选择快捷分享HTML.app进行打开。

## 打包为应用程序

有两种方法可以将脚本打包为macOS应用程序：

### 使用PyInstaller方法（推荐）

1. 安装PyInstaller和Pillow：

```bash
pip3 install pyinstaller pillow
```

2. 创建一个简单的图标文件（如果没有）：

```bash
python3 -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (512, 512), color='blue'); draw = ImageDraw.Draw(img); draw.rectangle([100, 100, 412, 412], fill='white'); img.save('icon.png')"
python3 -c "from PIL import Image; img = Image.open('icon.png'); img.save('appicon.icns')"
```

3. 使用提供的spec文件构建应用程序：

```bash
pyinstaller "快捷分享HTML.spec"
```

4. 构建好的应用程序位于`dist/快捷分享HTML.app`目录中。

5. 复制到Applications文件夹：

```bash
cp -r "dist/快捷分享HTML.app" ~/Applications/
```

### 使用py2app方法

1. 安装py2app：

```bash
pip3 install py2app
```

2. 构建应用程序：

```bash
python3 setup.py py2app
```

构建成功后，应用程序位于`dist/快捷分享HTML.app`目录中。

## 文件关联设置

应用程序已经配置为可以打开HTML文件。要关联HTML文件类型，请执行以下步骤：

1. 在Finder中找到一个HTML文件，右键点击
2. 选择"打开方式" > "其他..."
3. 在应用程序列表中找到并选择"快捷分享HTML"
4. 勾选"始终使用此应用打开"选项
5. 点击"打开"

现在，所有的HTML文件都将默认使用"快捷分享HTML"应用程序打开。

## 已知问题及解决方法

### Carbon框架错误

如果在运行打包的应用时遇到以下错误：

```
OSError: dlopen(/System/Library/Carbon.framework/Carbon, 0x0006): tried: '/System/Library/Carbon.framework/Carbon' (no such file)
```

解决方法是将setup.py中的`argv_emulation`设置为False：

```python
OPTIONS = {
    'argv_emulation': False,  # 设置为False以避免Carbon.framework依赖问题
    # 其他配置...
}
```

### Qt插件错误

如果遇到以下错误：

```
qt.qpa.plugin: Could not load the Qt platform plugin "cocoa" in "" even though it was found.
```

解决方法是确保Qt插件被正确打包，使用PyInstaller时插件已经被自动包含。

## 开发指南

项目目录结构：

- `sharehtml.py` - 主程序文件
- `setup.py` - py2app配置文件
- `快捷分享HTML.spec` - PyInstaller配置文件
- `requirements.txt` - 依赖项配置
- `plugins/` - Qt平台插件目录

## 贡献

欢迎提交问题报告和改进建议。 