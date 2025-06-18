#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cpsourcehtml.py - 批处理复制HTML文件到_files目录

用于处理ai目录下的HTML文件：
1. 为每个HTML文件创建对应的_files目录（如果不存在）
2. 将原HTML文件复制为_files/capsule.html（如果不存在）

使用方法: python cpsourcehtml.py
"""

import os
import shutil
from pathlib import Path


def copy_html_to_capsule(html_path):
    """将HTML文件复制到对应的_files/capsule.html"""
    print(f"处理文件: {html_path}")
    
    # 确定文件名（不含扩展名）
    file_stem = html_path.stem
    
    # 创建_files目录路径
    files_dir = html_path.parent / f"{file_stem}_files"
    capsule_path = files_dir / "capsule.html"
    
    # 检查并创建_files目录
    if not files_dir.exists():
        try:
            files_dir.mkdir(parents=True, exist_ok=True)
            print(f"  创建目录: {files_dir}")
        except Exception as e:
            print(f"  创建目录失败: {e}")
            return False
    else:
        print(f"  目录已存在: {files_dir}")
    
    # 检查并复制capsule.html
    if not capsule_path.exists():
        try:
            shutil.copy2(html_path, capsule_path)
            print(f"  复制文件: {html_path} -> {capsule_path}")
            return True
        except Exception as e:
            print(f"  复制文件失败: {e}")
            return False
    else:
        print(f"  文件已存在: {capsule_path}")
        return False


def main():
    """主函数"""
    ai_dir = Path('ai')
    
    # 检查ai目录是否存在
    if not ai_dir.exists():
        print(f"错误: ai目录不存在: {ai_dir}")
        return
    
    print(f"开始处理ai目录: {ai_dir}")
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
    created_dirs = 0
    
    # 处理每个HTML文件
    for html_file in html_files:
        # 记录目录创建前的状态
        file_stem = html_file.stem
        files_dir = html_file.parent / f"{file_stem}_files"
        dir_existed = files_dir.exists()
        
        # 处理文件
        if copy_html_to_capsule(html_file):
            processed_count += 1
        else:
            skipped_count += 1
        
        # 统计新创建的目录
        if not dir_existed and files_dir.exists():
            created_dirs += 1
        
        print()
    
    # 输出统计结果
    print("=" * 50)
    print("处理完成!")
    print(f"已复制: {processed_count} 个文件")
    print(f"已跳过: {skipped_count} 个文件")
    print(f"创建目录: {created_dirs} 个")
    print(f"总计: {len(html_files)} 个文件")


if __name__ == "__main__":
    main() 