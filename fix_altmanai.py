#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime, timezone

def fix_altmanai_html():
    file_path = "ai/altmanai.html"
    
    # 获取git创建时间
    try:
        cmd = ["git", "log", "--follow", "--format=%aI", "--reverse", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dates = result.stdout.strip().split('\n')
        if dates:
            git_time = dates[0]
            
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 查找并替换P开头的日期
            updated_content = re.sub(r'P\d{2,4}-\d{2}-\d{2}T[^\n]*', f'datetime: {git_time}', content)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"已修复 {file_path} 中的datetime为 {git_time}")
    except Exception as e:
        print(f"修复 {file_path} 出错: {e}")

if __name__ == "__main__":
    fix_altmanai_html() 