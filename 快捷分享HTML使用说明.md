# 快捷分享HTML应用 - 使用说明

## 📱 应用介绍

快捷分享HTML是一个macOS应用，帮助你快速将HTML文件分享到网站。应用会自动创建规范的文件夹结构，生成元数据，并执行推送脚本。

## 🚀 安装方法

### 方法一：使用安装脚本（推荐）
```bash
./install.sh
```

### 方法二：手动安装
1. 复制 `dist/快捷分享HTML.app` 到 `/Applications/` 文件夹
2. 双击启动应用

## 💡 功能特性

- ✅ 图形化界面，操作简单
- ✅ 自动创建文件夹结构（`name_files/capsule.html`）
- ✅ 自动生成meta.yaml元数据文件
- ✅ 支持HTML文件的右键打开
- ✅ 一键复制分享链接
- ✅ 自动调用处理脚本
- ✅ 详细的操作日志

## 🛠️ 使用方法

### 1. 基本设置
- **待分享文件**：选择要分享的HTML文件
- **本地Git仓库路径**：设置目标仓库路径（默认：`~/git/xiaobu/ai`）
- **分享后文件名**：设置分享后的文件名（会自动填入）
- **原始URL**：可选，填写原始文件的URL
- **分享脚本路径**：设置推送脚本路径（默认：`~/git/xiaobu/push.sh`）
- **网站地址**：设置分享网站地址（默认：`https://www.xiaobu.net/ai/`）

### 2. 分享流程
1. 选择HTML文件后，应用会自动填入文件名
2. 可以编辑文件名（只编辑文件名部分，不包括扩展名）
3. 填写原始URL（可选）
4. 点击"分享"按钮

### 3. 自动处理过程
应用会依次执行：
1. 创建 `name_files` 文件夹
2. 将HTML文件复制为 `name_files/capsule.html`
3. 提取HTML的title标签内容
4. 创建 `name_files/meta.yaml` 文件，包含：
   - `title`: HTML文件的标题
   - `datetime`: 当前时间（ISO格式）
   - `source`: 原始URL（格式：`()[url]`）
5. 调用 `gencapsule.py` 脚本进行进一步处理
6. 执行Git推送脚本
7. 自动复制分享链接到剪贴板

## 📋 生成的文件结构

假设输入文件名为 `report.html`，会生成：
```
ai/
└── report_files/
    ├── capsule.html      # 原HTML文件的副本
    └── meta.yaml         # 元数据文件
```

最终分享链接：`https://www.xiaobu.net/ai/report_files/capsule.html`

## 📝 meta.yaml 示例

```yaml
title: 我的报告标题
datetime: '2024-01-15T14:30:45.123456'
source: ()[https://example.com/original.html]
```

## 🔧 高级功能

### 右键打开HTML文件
应用已配置为HTML文件的可选打开方式：
1. 右键点击HTML文件
2. 选择"打开方式" > "快捷分享HTML"
3. 应用会自动启动并加载该文件

### 设置保存
应用会自动保存以下设置：
- Git仓库路径
- 原始URL
- 分享脚本路径
- 网站地址

## ❗ 注意事项

1. 确保 `gencapsule.py` 文件与应用在同一目录
2. 确保推送脚本有执行权限
3. 首次使用时需要配置Git仓库路径和脚本路径
4. 应用需要网络连接来执行Git推送

## 🐛 故障排除

### 应用无法启动
- 检查macOS安全设置，允许未知开发者的应用
- 在终端运行：`sudo xattr -r -d com.apple.quarantine /Applications/快捷分享HTML.app`

### 分享失败
- 检查Git仓库路径是否正确
- 确保推送脚本存在且有执行权限
- 查看应用日志区域的错误信息

### PyYAML相关错误
应用已内置PyYAML，如果出现相关错误，可能是打包问题，请重新打包。

## 📞 支持

如有问题，请查看应用内的日志输出或联系开发者。 