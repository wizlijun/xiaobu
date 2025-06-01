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

# 文件服务器 (webserver.py)

一个简单而功能完整的 Python 文件服务器，支持文件上传、下载和目录浏览，专门优化了大文件传输性能。

## 🚀 功能特性

- 📁 **目录浏览**: 美观的 Web 界面浏览文件夹内容
- 📤 **文件上传**: 通过 Web 界面上传文件到指定目录
- 📥 **文件下载**: 点击文件名即可下载文件
- ⚡ **大文件优化**: 支持大文件快速传输和断点续传
- 🔄 **断点续传**: 支持 HTTP Range 请求，下载中断可继续
- 🔒 **安全防护**: 防止目录遍历攻击，确保只能访问指定目录
- 🎨 **现代界面**: 响应式设计，支持移动设备
- 📊 **文件信息**: 显示文件大小、类型等信息，大文件特别标记

## ⚡ 性能优化

### 大文件传输优化
- **分块传输**: 使用 64KB 块大小进行分块传输
- **大缓冲区**: 1MB 读写缓冲区，提高 I/O 性能
- **断点续传**: 支持 HTTP Range 请求，可从断点继续下载
- **连接管理**: 优化连接超时和错误处理
- **内存优化**: 避免将大文件完全加载到内存

### 适用场景
- ✅ 80MB+ 大文件快速下载
- ✅ 网络不稳定环境下的可靠传输
- ✅ 移动设备和慢速网络
- ✅ 批量文件传输

## 使用方法

### 基本用法

```bash
python webserver.py <目录路径>
```

例如：
```bash
# 共享当前目录
python webserver.py .

# 共享指定目录
python webserver.py /path/to/your/folder

# Windows 示例
python webserver.py C:\Users\YourName\Documents
```

### 高级选项

```bash
# 指定端口 (默认: 8888)
python webserver.py <目录路径> -p 9000

# 指定监听地址 (默认: 0.0.0.0)
python webserver.py <目录路径> -H 127.0.0.1

# 组合使用
python webserver.py /path/to/folder -p 9000 -H 192.168.1.100
```

### 参数说明

- `directory`: 要共享的目录路径（必需）
- `-p, --port`: 服务器端口号（默认: 8888）
- `-H, --host`: 服务器监听地址（默认: 0.0.0.0，表示所有网络接口）

## 访问方式

启动服务器后，可以通过以下方式访问：

- **本地访问**: http://localhost:8888
- **局域网访问**: http://你的IP地址:8888
- **其他设备**: http://服务器IP:8888

## 使用示例

### 1. 启动服务器
```bash
$ python webserver.py ./shared_folder
🚀 文件服务器启动成功!
📂 共享目录: /path/to/shared_folder
🌐 服务地址: http://0.0.0.0:8888
💡 功能: 文件上传、下载、目录浏览
⚡ 优化: 支持大文件传输和断点续传
⏹️  按 Ctrl+C 停止服务器
--------------------------------------------------
```

### 2. 浏览文件
- 在浏览器中打开 http://localhost:8888
- 点击文件夹名称进入子目录
- 点击文件名下载文件（大文件自动触发下载）
- 使用"返回上级目录"链接导航
- 大文件（>50MB）会用红色标记显示

### 3. 上传文件
- 在任意目录页面找到"上传文件"区域
- 点击"选择文件"按钮选择要上传的文件
- 点击"上传文件"按钮完成上传
- 支持大文件上传，使用 1MB 缓冲区优化性能

### 4. 断点续传
- 下载大文件时，如果网络中断，可以使用支持断点续传的下载工具
- 浏览器通常会自动处理断点续传
- 服务器支持 HTTP Range 请求

## 🔧 技术特性

### 性能参数
- **块大小**: 64KB（下载）/ 1MB（上传）
- **缓冲区**: 1MB 读写缓冲区
- **超时设置**: 5分钟连接超时
- **大文件阈值**: 10MB（自动下载）/ 50MB（红色标记）

### HTTP 特性
- 支持 HTTP/1.1 Range 请求
- 正确的 MIME 类型检测
- 缓存控制头（1小时缓存）
- Last-Modified 头支持
- Accept-Ranges 头声明

## 安全注意事项

1. **网络安全**: 默认监听所有网络接口 (0.0.0.0)，局域网内的其他设备都可以访问
2. **目录限制**: 服务器只能访问指定的目录及其子目录，无法访问系统其他位置
3. **文件权限**: 确保 Python 进程有读写指定目录的权限
4. **防火墙**: 如需外网访问，请配置防火墙规则
5. **大文件**: 注意磁盘空间，大文件传输会占用相应的存储空间

## 系统要求

- Python 3.6 或更高版本
- 无需额外依赖，使用 Python 标准库
- 建议：至少 1GB 可用内存（处理大文件时）

## 停止服务器

在终端中按 `Ctrl+C` 即可停止服务器。

## 故障排除

### 常见问题

1. **端口被占用**
   ```
   OSError: [Errno 98] Address already in use
   ```
   解决方案：使用 `-p` 参数指定其他端口

2. **权限不足**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   解决方案：确保对目录有读写权限，或使用管理员权限运行

3. **大文件下载慢**
   - 检查网络连接质量
   - 使用支持断点续传的下载工具
   - 确保服务器有足够的内存和 CPU 资源

4. **上传大文件失败**
   - 检查磁盘空间是否充足
   - 确保网络连接稳定
   - 浏览器可能有上传大小限制

### 性能调优

1. **提高传输速度**
   - 在局域网环境中使用
   - 确保服务器和客户端网络质量良好
   - 关闭不必要的防病毒软件实时扫描

2. **处理超大文件**
   - 确保有足够的磁盘空间
   - 监控服务器内存使用情况
   - 考虑使用专业的文件传输工具

### 获取帮助

```bash
python webserver.py -h
```

## 更新日志

### v2.0 - 大文件优化版本
- ✅ 添加断点续传支持
- ✅ 优化大文件传输性能
- ✅ 增加分块传输机制
- ✅ 改进错误处理和连接管理
- ✅ 添加大文件标记显示
- ✅ 优化内存使用

### v1.0 - 基础版本
- ✅ 基本文件上传下载功能
- ✅ 目录浏览界面
- ✅ 安全防护机制

## 许可证

此项目使用 MIT 许可证。 