#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime, timezone

def fix_html_files():
    # ai目录的路径
    ai_dir = "ai"
    
    # 获取所有html和htm文件（除了index.html）
    html_files = []
    for file in os.listdir(ai_dir):
        if (file.endswith(".html") or file.endswith(".htm")) and file != "index.html":
            html_files.append(os.path.join(ai_dir, file))
    
    # 对每个文件进行修复
    for file_path in html_files:
        try:
            # 获取git创建时间
            cmd = ["git", "log", "--follow", "--format=%aI", "--reverse", file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            dates = result.stdout.strip().split('\n')
            if dates:
                git_time = dates[0]
                
                # 读取文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 检查是否有P开头的日期格式
                has_p_date = re.search(r'P\d{2,4}-\d{2}-\d{2}T[^\n]*', content)
                
                if has_p_date:
                    # 替换P开头的日期
                    updated_content = re.sub(r'P\d{2,4}-\d{2}-\d{2}T[^\n]*', f'datetime: {git_time}', content)
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    
                    print(f"已修复 {file_path} 中的P开头日期为 {git_time}")
                else:
                    print(f"{file_path} 中没有P开头的日期，无需修复")
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")

if __name__ == "__main__":
    fix_html_files() 