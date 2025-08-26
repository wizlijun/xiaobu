# 小布工具集 🚀

一个功能丰富的文件分享与管理工具集，包含HTML快捷分享应用和高性能文件服务器。

## 📋 项目概述

本项目提供两个核心工具：
- **快捷分享HTML应用**: macOS原生桌面应用，用于快速分享HTML文件到Git仓库
- **文件服务器**: 高性能Python文件服务器，支持大文件传输和断点续传

---

# 🌐 快捷分享HTML应用

一个专为macOS设计的桌面应用程序，能够将HTML文件快速复制到Git仓库并推送到服务器，然后生成可分享的链接。

## ✨ 主要特性

- 🖱️ **Finder集成**: 支持右键"打开方式"直接分享HTML文件
- ⚙️ **灵活配置**: 自定义本地Git仓库路径、分享脚本路径和网站地址
- 📋 **自动复制**: 分享链接自动复制到剪贴板
- 📊 **日志查看**: 完整的操作日志，便于问题排查
- 🎨 **现代界面**: 基于PyQt5的原生macOS界面

## 📦 系统要求

- **操作系统**: macOS 10.12+
- **Python版本**: Python 3.6+
- **依赖库**: PyQt5

## 🛠️ 安装指南

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 验证安装

```bash
python3 sharehtml.py --help
```

## 🚀 使用方法

### 直接运行

```bash
# 启动应用程序
python3 sharehtml.py

# 指定HTML文件
python3 sharehtml.py /path/to/your/file.html
```

### 打包为macOS应用

#### 方法一：使用PyInstaller（推荐）

1. **安装打包工具**
   ```bash
   pip3 install pyinstaller pillow
   ```

2. **创建应用图标**（可选）
   ```bash
   python3 -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (512, 512), color='blue'); draw = ImageDraw.Draw(img); draw.rectangle([100, 100, 412, 412], fill='white'); img.save('icon.png')"
   python3 -c "from PIL import Image; img = Image.open('icon.png'); img.save('appicon.icns')"
   ```

3. **构建应用**
   ```bash
   pyinstaller "快捷分享HTML.spec"
   ```

4. **安装到应用程序文件夹**
   ```bash
   cp -r "dist/快捷分享HTML.app" ~/Applications/
   ```

#### 方法二：使用py2app

1. **安装py2app**
   ```bash
   pip3 install py2app
   ```

2. **构建应用**
   ```bash
   python3 setup.py py2app
   ```

## ⚙️ 文件关联设置

1. 在Finder中右键点击HTML文件
2. 选择"打开方式" → "其他..."
3. 选择"快捷分享HTML"应用
4. 勾选"始终使用此应用打开"
5. 点击"打开"

## 🔧 常见问题解决

### Carbon框架错误

**问题**: 
```
OSError: dlopen(/System/Library/Carbon.framework/Carbon, 0x0006): tried: '/System/Library/Carbon.framework/Carbon' (no such file)
```

**解决方案**: 在setup.py中设置：
```python
OPTIONS = {
    'argv_emulation': False,  # 避免Carbon.framework依赖问题
    # 其他配置...
}
```

### Qt插件错误

**问题**: 
```
qt.qpa.plugin: Could not load the Qt platform plugin "cocoa"
```

**解决方案**: 使用PyInstaller打包时插件会自动包含。如果仍有问题，检查Qt插件路径配置。

---

# 📁 高性能文件服务器

一个基于Python的现代化文件服务器，专门为大文件传输和多设备文件共享场景优化设计。

## ⚡ 核心特性

### 📂 文件管理
- **目录浏览**: 美观的Web界面，响应式设计
- **文件上传**: 支持大文件上传，1MB缓冲区优化
- **文件下载**: 点击即下载，自动触发大文件下载
- **文件信息**: 显示文件大小、修改时间等详细信息

### 🚀 性能优化
- **大文件传输**: 64KB分块传输，避免内存溢出
- **断点续传**: 完整支持HTTP Range请求
- **高效缓冲**: 1MB读写缓冲区，提升I/O性能
- **连接优化**: 智能超时和错误恢复机制
- **内存友好**: 流式传输，不会将大文件加载到内存

### 🔒 安全保护
- **路径安全**: 防止目录遍历攻击
- **访问控制**: 限制在指定目录范围内
- **错误处理**: 完善的异常处理和日志记录

### 🎨 用户体验
- **现代界面**: 清爽的Web界面设计
- **移动优化**: 支持手机和平板设备访问
- **视觉标识**: 大文件特殊标记（>50MB红色显示）
- **便捷导航**: 面包屑导航和返回上级目录

## 📊 性能指标

| 特性 | 规格 |
|------|------|
| 单文件最大支持 | 无限制（受存储空间限制） |
| 并发连接 | 取决于系统资源 |
| 传输缓冲区 | 1MB（上传/下载） |
| 分块大小 | 64KB |
| 超时设置 | 5分钟 |
| 大文件阈值 | 50MB（界面标记）/ 10MB（自动下载） |

## 🛠️ 系统要求

- **Python版本**: Python 3.6+
- **依赖库**: 仅使用Python标准库
- **推荐内存**: 1GB+（处理大文件）
- **操作系统**: Windows / macOS / Linux

## 🚀 快速开始

### 基本用法

```bash
# 共享当前目录
python3 webserver.py .

# 共享指定目录
python3 webserver.py /path/to/shared/folder

# Windows示例
python3 webserver.py C:\Users\YourName\Documents
```

### 高级配置

```bash
# 自定义端口
python3 webserver.py ./folder -p 9000

# 指定监听地址
python3 webserver.py ./folder -H 192.168.1.100

# 组合配置
python3 webserver.py /shared -p 8080 -H 0.0.0.0
```

### 参数说明

| 参数 | 描述 | 默认值 | 示例 |
|------|------|--------|------|
| `directory` | 共享目录路径（必需） | - | `./shared` |
| `-p, --port` | 服务器端口 | `8888` | `-p 9000` |
| `-H, --host` | 监听地址 | `0.0.0.0` | `-H 127.0.0.1` |

## 🌐 访问方式

| 访问类型 | URL | 说明 |
|----------|-----|------|
| 本地访问 | `http://localhost:8888` | 仅本机访问 |
| 局域网访问 | `http://你的IP:8888` | 同网段设备访问 |
| 指定接口 | `http://服务器IP:8888` | 指定网络接口 |

## 📱 使用场景

### 💼 办公场景
- **文档共享**: 在团队间快速共享文档和资料
- **演示文件**: 会议中实时分享PPT和演示文件
- **临时文件传输**: 避免邮件附件大小限制

### 🏠 家庭使用
- **设备间传输**: 手机、电脑、平板之间文件共享
- **媒体文件**: 分享照片、视频等大文件
- **备份访问**: 访问NAS或备份文件

### 🎓 教育培训
- **课件分发**: 向学生分发课程资料
- **作业收集**: 学生上传作业到指定目录
- **资源库**: 建立课程资源共享平台

### 🔧 开发测试
- **文件部署**: 快速部署测试文件到服务器
- **日志查看**: 访问远程服务器日志文件
- **资源下载**: 下载构建产物和依赖文件

## 📋 操作指南

### 🔍 浏览文件
1. 在浏览器打开服务器地址
2. 点击文件夹名称进入子目录
3. 使用"返回上级目录"链接导航
4. 大文件会以红色文字显示

### 📤 上传文件
1. 在任意目录页面找到"上传文件"区域
2. 点击"选择文件"按钮
3. 选择要上传的文件
4. 点击"上传"按钮完成

### 📥 下载文件
1. 点击文件名开始下载
2. 大文件（>10MB）会自动触发下载
3. 支持断点续传，可暂停后继续
4. 下载进度显示在浏览器中

### 🔄 断点续传
- 使用支持断点续传的下载工具
- 现代浏览器通常自动支持
- 网络中断后可继续下载
- 服务器支持HTTP Range请求

## 🔧 技术细节

### HTTP特性支持
- ✅ HTTP/1.1协议
- ✅ Range请求（断点续传）
- ✅ MIME类型自动检测
- ✅ Last-Modified头
- ✅ Cache-Control头
- ✅ Accept-Ranges头

### 安全机制
- ✅ 路径遍历防护
- ✅ 文件访问权限检查
- ✅ 异常处理和错误恢复
- ✅ 连接超时控制

### 性能优化技术
- ✅ 分块传输编码
- ✅ 大缓冲区读写
- ✅ 流式文件处理
- ✅ 内存使用优化

## 🛡️ 安全注意事项

### 网络安全
⚠️ **默认配置**: 监听所有网络接口(0.0.0.0)，局域网设备可访问
⚠️ **外网暴露**: 如需外网访问，请配置防火墙规则
⚠️ **敏感文件**: 不要共享包含敏感信息的目录

### 系统安全
⚠️ **文件权限**: 确保Python进程有目录读写权限
⚠️ **磁盘空间**: 监控磁盘使用，避免空间不足
⚠️ **资源限制**: 大量并发可能影响系统性能

### 使用建议
✅ **局域网使用**: 推荐在内网环境中使用
✅ **临时分享**: 适合临时文件分享场景  
✅ **定期检查**: 定期清理共享目录
✅ **备份重要数据**: 上传前备份重要文件

## 🔍 故障排除

### 常见错误

#### 端口占用问题
```
OSError: [Errno 98] Address already in use
```
**解决方案**:
```bash
# 使用其他端口
python3 webserver.py ./folder -p 9000

# 查找占用进程
lsof -i :8888
netstat -tulpn | grep 8888
```

#### 权限不足问题
```
PermissionError: [Errno 13] Permission denied
```
**解决方案**:
```bash
# 检查目录权限
ls -la /path/to/directory

# 修改权限
chmod 755 /path/to/directory

# 或使用管理员权限运行
sudo python3 webserver.py ./folder
```

#### 大文件传输问题
```
连接超时或传输中断
```
**解决方案**:
- 检查网络连接质量
- 使用有线网络代替WiFi
- 关闭防病毒软件实时扫描
- 使用专业下载工具

### 性能调优建议

#### 提升传输速度
1. **网络优化**
   - 使用千兆以太网
   - 避免WiFi信号干扰
   - 减少网络跳数

2. **系统优化**
   - 关闭不必要的后台程序
   - 增加系统内存
   - 使用SSD存储

3. **配置优化**
   - 调整缓冲区大小
   - 优化Python参数
   - 使用多线程版本

#### 处理超大文件（GB级别）
1. **预检查**
   ```bash
   # 检查磁盘空间
   df -h
   
   # 监控内存使用
   top
   htop
   ```

2. **传输建议**
   - 使用稳定的有线连接
   - 避免同时传输多个大文件
   - 考虑文件压缩

3. **监控工具**
   ```bash
   # 监控网络流量
   iftop
   nethogs
   
   # 监控磁盘I/O
   iotop
   ```

### 获取帮助

```bash
# 查看帮助信息
python3 webserver.py -h

# 查看版本信息
python3 webserver.py --version
```

---

# 📊 项目架构

## 目录结构

```
xiaobu/
├── README.md                    # 项目文档
├── requirements.txt             # Python依赖
├── sharehtml.py                # HTML分享主程序
├── webserver.py                # 文件服务器主程序
├── setup.py                    # py2app配置
├── 快捷分享HTML.spec            # PyInstaller配置
├── appicon.icns                # 应用图标
├── plugins/                    # Qt插件目录
├── ai/                         # HTML文件存储
├── write/                      # 写作文档
└── template/                   # 模板文件
```

## 核心文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `sharehtml.py` | HTML分享应用主程序 | macOS桌面应用 |
| `webserver.py` | 文件服务器主程序 | Web文件服务 |
| `setup.py` | py2app打包配置 | macOS应用打包 |
| `快捷分享HTML.spec` | PyInstaller配置 | 应用打包配置 |
| `requirements.txt` | Python依赖列表 | 环境配置 |

---

# 🤝 贡献指南

欢迎为本项目做出贡献！请遵循以下步骤：

## 贡献流程

1. **Fork项目** - 点击GitHub页面右上角的Fork按钮
2. **创建分支** - `git checkout -b feature/your-feature-name`
3. **提交更改** - `git commit -m 'Add some feature'`
4. **推送分支** - `git push origin feature/your-feature-name`
5. **创建Pull Request** - 在GitHub上创建PR

## 代码规范

### Python代码风格
- 使用PEP 8代码风格
- 添加必要的文档字符串
- 包含类型注解（推荐）
- 编写单元测试

### 提交信息格式
```
类型(范围): 简短描述

详细描述（可选）

关闭 #issue编号
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或辅助工具

## 开发环境设置

```bash
# 克隆项目
git clone https://github.com/your-username/xiaobu.git
cd xiaobu

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/
```

## 问题报告

在提交问题时，请包含：
- 操作系统和版本
- Python版本
- 错误信息和堆栈跟踪
- 重现步骤
- 预期行为vs实际行为

---

# 📄 许可证

本项目采用MIT许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## MIT License

```
MIT License

Copyright (c) 2025 Xiaobu Tools

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# 📞 联系方式

- **项目主页**: [GitHub Repository](https://github.com/your-username/xiaobu)
- **问题反馈**: [GitHub Issues](https://github.com/your-username/xiaobu/issues)
- **功能请求**: [GitHub Discussions](https://github.com/your-username/xiaobu/discussions)

---

# 📚 更多资源

## 相关文档
- [Python HTTP服务器文档](https://docs.python.org/3/library/http.server.html)
- [PyQt5官方文档](https://doc.qt.io/qtforpython/)
- [macOS应用打包指南](https://py2app.readthedocs.io/)

## 类似项目
- [SimpleHTTPServer](https://docs.python.org/2/library/simplehttpserver.html) - Python内置简单服务器
- [Caddy](https://caddyserver.com/) - 现代化Web服务器
- [Nginx](https://nginx.org/) - 高性能Web服务器

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个star！⭐**

Made with ❤️ by [Your Name]

</div>