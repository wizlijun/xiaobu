#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
processoldhtml.py - 批处理旧HTML文件，提取YAML信息

用于处理ai/blog目录下包含YAML头部信息的HTML文件：
1. 检测HTML文件头部的YAML信息
2. 创建对应的_files目录和meta.yaml文件
3. 从HTML中移除YAML部分并保存

使用方法: python processoldhtml.py
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime


def extract_yaml_from_html(html_content):
    """从HTML内容中提取YAML前置信息"""
    # 匹配HTML注释中的YAML信息（<!-- -->包围的部分）
    yaml_pattern = r'<!--\s*\n(.*?)\n\s*-->'
    match = re.search(yaml_pattern, html_content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        # 移除YAML部分后的HTML内容
        html_without_yaml = html_content[:match.start()] + html_content[match.end():]
        return yaml_content, html_without_yaml
    
    return None, html_content


def clean_yaml_content(yaml_str):
    """清理YAML内容，移除无效行和多余分隔符"""
    lines = yaml_str.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
            
        # 跳过YAML文档分隔符
        if line == '---':
            continue
            
        # 跳过没有冒号的行（没有键值对格式的行）
        if ':' not in line:
            print(f"  跳过无效行: {line}")
            continue
            
        # 检查是否是有效的键值对格式
        if line.count(':') >= 1:
            key_part = line.split(':', 1)[0].strip()
            # 确保键名不为空且不是纯数字或日期格式，且不以P开头
            if (key_part and 
                not re.match(r'^[\d\-T:+]+$', key_part) and 
                not key_part.startswith('P')):
                cleaned_lines.append(line)
            else:
                print(f"  跳过无效键名: {line}")
        else:
            print(f"  跳过格式错误: {line}")
    
    return '\n'.join(cleaned_lines)


def parse_yaml_content(yaml_str):
    """解析YAML字符串"""
    try:
        # 先清理YAML内容
        cleaned_yaml = clean_yaml_content(yaml_str)
        
        if not cleaned_yaml.strip():
            print("  跳过: 清理后无有效YAML内容")
            return None
            
        return yaml.safe_load(cleaned_yaml)
    except yaml.YAMLError as e:
        print(f"YAML解析错误: {e}")
        return None


def create_meta_yaml(yaml_data, output_path):
    """创建meta.yaml文件"""
    # 基础模板结构
    meta_template = {
        'title': '',
        'datetime': '',
        'tags': [],
        'description': '',
        'source': '',
        'attachments': [],
        'links': []
    }
    
    # 从解析的YAML数据中填充
    if yaml_data:
        meta_template['title'] = yaml_data.get('title', '')
        meta_template['datetime'] = yaml_data.get('datetime', datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'))
        meta_template['tags'] = yaml_data.get('tags', [])
        meta_template['description'] = yaml_data.get('description', '')
        meta_template['source'] = yaml_data.get('source', '')
        meta_template['attachments'] = yaml_data.get('attachments', [])
        meta_template['links'] = yaml_data.get('links', [])
    
    # 写入meta.yaml文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(meta_template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"创建meta.yaml失败: {e}")
        return False


def process_html_file(html_path):
    """处理单个HTML文件"""
    print(f"处理文件: {html_path}")
    
    # 读取HTML文件
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"读取HTML文件失败: {e}")
        return False
    
    # 提取YAML信息
    yaml_content, html_without_yaml = extract_yaml_from_html(html_content)
    
    if yaml_content is None:
        print(f"  跳过: 未找到YAML头部信息")
        return False
    
    print(f"  发现YAML头部信息")
    
    # 解析YAML
    yaml_data = parse_yaml_content(yaml_content)
    if yaml_data is None:
        print(f"  跳过: YAML解析失败")
        return False
    
    # 确定文件名（不含扩展名）
    file_stem = html_path.stem
    
    # 创建_files目录
    files_dir = html_path.parent / f"{file_stem}_files"
    try:
        files_dir.mkdir(exist_ok=True)
        print(f"  创建目录: {files_dir}")
    except Exception as e:
        print(f"  创建目录失败: {e}")
        return False
    
    # 创建meta.yaml文件
    meta_yaml_path = files_dir / "meta.yaml"
    if create_meta_yaml(yaml_data, meta_yaml_path):
        print(f"  创建meta.yaml: {meta_yaml_path}")
    else:
        print(f"  创建meta.yaml失败")
        return False
    
    # 保存移除YAML后的HTML文件
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_without_yaml)
        print(f"  更新HTML文件: 已移除YAML头部信息")
    except Exception as e:
        print(f"  更新HTML文件失败: {e}")
        return False
    
    return True


def main():
    """主函数"""
    ai_dir = Path('ai/blog')
    
    # 检查ai/blog目录是否存在
    if not ai_dir.exists():
        print(f"错误: ai/blog目录不存在: {ai_dir}")
        return
    
    print(f"开始处理ai/blog目录: {ai_dir}")
    print("=" * 50)
    
    # 查找所有HTML文件
    html_files = list(ai_dir.glob('*.html'))
    
    if not html_files:
        print("未找到HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件")
    print()
    
    # 统计信息
    processed_count = 0
    skipped_count = 0
    
    # 处理每个HTML文件
    for html_file in html_files:
        if process_html_file(html_file):
            processed_count += 1
        else:
            skipped_count += 1
        print()
    
    # 输出统计结果
    print("=" * 50)
    print("处理完成!")
    print(f"已处理: {processed_count} 个文件")
    print(f"已跳过: {skipped_count} 个文件")
    print(f"总计: {len(html_files)} 个文件")


if __name__ == "__main__":
    main() 