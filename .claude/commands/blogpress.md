# 自动博客翻译和HTML生成 Prompt

请按照以下步骤自动处理markdown博客文件, 输入markdown文件名  {mdfile}

## 任务目标
将英文markdown博客文件翻译为中文，并生成规范化的HTML文件结构。

## 执行步骤

### 1. 读取源文件

确认{mdfile}存在
提取文件名：例如 /write/blog_github_spec_driven_dev.md 中，文件名为 blog_github_spec_driven_dev.
文件名为 {mdfilename}
```
读取 {mdfile} 文件内容
读取 /template/meta.yaml 模板文件
```

### 2. 创建目录结构
在 `/ai/blog/` 目录下创建对应的文件结构：
- `{mdfilename}_files/` 目录
- `capsule.html` 文件
- `meta.yaml` 文件

### 3. 生成中文HTML文件
创建 `/ai/blog/{mdfilename}_files/capsule.html`，要求：

**HTML结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{翻译后的标题}</title>
    <style>
        /* 现代化CSS样式 */
        body {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        .author-info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
        .process-phase {
            background-color: #f1f8ff;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #0366d6;
        }
        .scenario {
            background-color: #f6f8fa;
            padding: 12px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 3px solid #6f42c1;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        pre {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <!-- 翻译后的完整内容 -->
</body>
</html>
```

**翻译要求**：
- 如果不是中文，则完整的翻译为流畅的中文
- 保持技术术语的准确性
- 保留原文的结构和格式
- 使用适当的HTML标签和CSS类名来突出重要内容

### 4. 获取当前时间 {now}
获取当前系统时间{now}
时间戳字符串为标准的 yaml 时间字符串
样例：'2025-08-04T10:17:19+08:00'


### 5. 生成meta.yaml文件
创建 `/ai/blog/{mdfilename}_files/meta.yaml`：

```yaml
title: {翻译后的标题}
datetime: {now}
tags:
- {相关标签1，全小写英文}
- {相关标签2，全小写英文}  
- {相关标签3，全小写英文}
description: {100字以内的中文描述}
source: ({原文链接描述})[{原文URL}]
attachments:
links:
- ({相关链接描述})[{相关链接URL}]
```

**标签要求**：
- 3个以内
- 全小写英文单词
- 与内容主题相关

### 5. 执行gencapsule.py
运行命令：
```bash
python3 gencapsule.py blog/{mdfilename}
```

## 质量要求
1. **翻译质量**：流畅自然的中文，保持技术准确性
2. **HTML结构**：语义化标签，响应式设计
3. **样式设计**：现代化UI，良好的可读性
4. **元数据**：准确的标签和描述

## 验证步骤
1. 检查所有文件是否创建成功
2. 验证HTML文件在浏览器中的显示效果
3. 确认gencapsule.py执行无错误
4. 检查最终生成的HTML文件内容完整性

请按照以上步骤完整执行，确保每个环节都成功完成后再进行下一步。

