# gencapsule.py 使用说明

## 功能描述

`gencapsule.py` 是一个自动化脚本，用于将大模型摘要后的交互式阅读页面生成完整的 HTML 文件。脚本会自动注入样式、交互功能和元数据信息，生成便于用户浏览的完整页面。

## 安装依赖

在使用之前，请确保安装了所需的 Python 包：

```bash
pip install PyYAML
```

或者使用项目的 requirements.txt：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python gencapsule.py <name>
```

其中 `<name>` 是要处理的项目基名（例如：book、article 等）。

### 示例

```bash
python gencapsule.py book
```

这将处理 `/ai/book_files/` 目录下的文件，并生成 `/ai/book.html`。

## 目录结构要求

脚本需要以下目录结构：

```
项目根目录/
├── ai/
│   └── <name>_files/
│       ├── capsule.html      # 原始HTML文件
│       ├── meta.yaml         # 元数据文件
│       └── [附件文件...]     # 可选的附件文件
├── template/
│   ├── capsule.css.html      # CSS样式模板
│   └── capsule.floatbox.html # 浮动框模板
└── gencapsule.py             # 脚本文件
```

## 输入文件格式

### capsule.html

原始的HTML文件，必须包含：
- `</style>` 标签（用于插入CSS样式）
- `</body>` 标签（用于插入浮动框内容）

### meta.yaml

YAML格式的元数据文件，支持以下字段：

```yaml
title: "页面标题"
datetime: "2025-01-01T10:00:00+08:00"
tags: ["标签1", "标签2"]
description: "页面描述"
source: "(原文标题)[原文链接]"
attachments:
  - "(附件1标题)[文件名1.pdf]"
  - "(附件2标题)[文件名2.doc]"
links:
  - "(相关链接1标题)[https://link1.com]"
  - "(相关链接2标题)[https://link2.com]"
```

**链接格式说明**：所有链接都使用 `(标题)[链接地址]` 的格式。

### 模板文件

- `capsule.css.html`：CSS样式代码，将被插入到 `</style>` 标签前
- `capsule.floatbox.html`：浮动框模板（当前版本中会被脚本生成的内容替换）

## 输出

脚本会在 `/ai/` 目录下生成 `<name>.html` 文件，包含：

1. 原始HTML内容
2. 注入的CSS样式
3. 根据元数据生成的浮动框，包含：
   - 原文链接
   - 相关链接列表
   - 附件下载列表

## 功能特性

- **自动路径处理**：根据项目名自动构建正确的文件路径
- **错误处理**：提供清晰的错误信息和异常处理
- **格式解析**：自动解析 `(标题)[链接]` 格式的文本
- **响应式设计**：生成的浮动框支持响应式布局
- **文件安全**：在处理文件时进行安全检查

## 错误处理

脚本会处理以下错误情况：

- 输入目录或文件不存在
- YAML文件格式错误
- HTML文件缺少必要的标签
- 文件编码问题
- 权限问题

所有错误都会输出清晰的错误信息并安全退出。

## 示例运行输出

```
开始处理: book
输入目录: ai/book_files
输出文件: ai/book.html
读取输入文件...
处理元数据...
注入样式和交互内容...
写入输出文件...
成功生成: ai/book.html

统计信息:
- 原文链接: 有
- 相关链接: 2 个
- 附件数量: 3 个
```

## 测试

项目包含测试脚本 `test_gencapsule.py`，可以运行以验证功能：

```bash
python test_gencapsule.py
```

## 注意事项

1. 确保所有输入文件使用 UTF-8 编码
2. meta.yaml 中的附件文件路径相对于 `<name>_files/` 目录
3. 如果某些元数据字段为空，相应的HTML区块会被省略
4. 生成的HTML文件会覆盖同名的现有文件
5. 附件文件本身不会被复制，只生成链接引用 