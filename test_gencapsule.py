#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_gencapsule.py - 测试 gencapsule.py 脚本的功能

测试各种边界情况和功能
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import yaml


def create_test_data(temp_dir):
    """创建测试数据"""
    
    # 创建目录结构
    ai_dir = Path(temp_dir) / "ai"
    test_files_dir = ai_dir / "test_files"
    template_dir = Path(temp_dir) / "template"
    
    ai_dir.mkdir()
    test_files_dir.mkdir()
    template_dir.mkdir()
    
    # 创建测试用的 capsule.html
    capsule_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>测试页面</title>
    <style>
        body { margin: 0; }
    </style>
</head>
<body>
    <h1>测试内容</h1>
    <p>这是一个测试页面。</p>
</body>
</html>"""
    
    with open(test_files_dir / "capsule.html", "w", encoding="utf-8") as f:
        f.write(capsule_html)
    
    # 创建测试用的 meta.yaml
    meta_data = {
        "title": "测试标题",
        "datetime": "2025-01-01T10:00:00+08:00",
        "tags": ["test", "example"],
        "description": "这是一个测试描述",
        "source": "(测试原文)[https://example.com]",
        "attachments": [
            "(测试附件1)[test1.pdf]",
            "(测试附件2)[test2.doc]"
        ],
        "links": [
            "(相关链接1)[https://link1.com]",
            "(相关链接2)[https://link2.com]"
        ]
    }
    
    with open(test_files_dir / "meta.yaml", "w", encoding="utf-8") as f:
        yaml.dump(meta_data, f, allow_unicode=True, default_flow_style=False)
    
    # 创建模板文件
    css_template = """
.test-style {
    background: #f0f0f0;
}"""
    
    with open(template_dir / "capsule.css.html", "w", encoding="utf-8") as f:
        f.write(css_template)
    
    floatbox_template = """
<div class="test-floatbox">
    {content}
</div>"""
    
    with open(template_dir / "capsule.floatbox.html", "w", encoding="utf-8") as f:
        f.write(floatbox_template)
    
    # 创建测试附件
    (test_files_dir / "test1.pdf").write_text("测试PDF内容")
    (test_files_dir / "test2.doc").write_text("测试DOC内容")
    
    return temp_dir


def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试数据
        create_test_data(temp_dir)
        
        # 改变工作目录
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # 运行脚本
            sys.path.insert(0, original_cwd)
            from gencapsule import main
            
            # 模拟命令行参数
            sys.argv = ["gencapsule.py", "test"]
            
            # 运行主函数
            main()
            
            # 检查输出文件是否存在
            output_file = Path("ai/test.html")
            if output_file.exists():
                print("✓ 输出文件生成成功")
                
                # 检查文件内容
                content = output_file.read_text(encoding="utf-8")
                
                # 验证样式注入
                if ".test-style" in content:
                    print("✓ CSS样式注入成功")
                else:
                    print("✗ CSS样式注入失败")
                
                # 验证内容注入
                if "测试原文" in content and "example.com" in content:
                    print("✓ 原文链接生成成功")
                else:
                    print("✗ 原文链接生成失败")
                
                if "测试附件1" in content and "test_files/test1.pdf" in content:
                    print("✓ 附件链接生成成功")
                else:
                    print("✗ 附件链接生成失败")
                
                if "相关链接1" in content and "link1.com" in content:
                    print("✓ 相关链接生成成功")
                else:
                    print("✗ 相关链接生成失败")
                
            else:
                print("✗ 输出文件生成失败")
                
        finally:
            os.chdir(original_cwd)


def test_error_handling():
    """测试错误处理"""
    print("\n测试错误处理...")
    
    # 测试文件不存在的情况
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            sys.path.insert(0, original_cwd)
            from gencapsule import main
            
            sys.argv = ["gencapsule.py", "nonexistent"]
            
            try:
                main()
                print("✗ 应该抛出错误但没有")
            except SystemExit:
                print("✓ 正确处理了文件不存在的错误")
                
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    print("开始测试 gencapsule.py...")
    test_basic_functionality()
    test_error_handling()
    print("\n测试完成！") 