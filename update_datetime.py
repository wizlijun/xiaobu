#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime, timezone

# 获取文件的git创建时间
def get_git_creation_time(file_path):
    try:
        # 运行git命令获取文件的首次提交时间（ISO 8601格式）
        cmd = ["git", "log", "--follow", "--format=%aI", "--reverse", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dates = result.stdout.strip().split('\n')
        if dates:
            # 返回第一次提交的时间（标准ISO 8601格式）
            # 确保时区偏移格式正确（+08:00而不是+0800）
            iso_date = dates[0]
            if '+' in iso_date or '-' in iso_date:
                offset_char = '+' if '+' in iso_date else '-'
                parts = iso_date.split(offset_char)
                offset = parts[1]
                if ':' not in offset and len(offset) == 4:  # 处理无冒号格式
                    iso_date = f"{parts[0]}{offset_char}{offset[:2]}:{offset[2:]}"
            return iso_date
        return None
    except Exception as e:
        print(f"获取 {file_path} 的git创建时间时出错: {e}")
        # 如果无法获取git时间，使用当前时间的ISO 8601格式
        now = datetime.now(timezone.utc).astimezone()
        return now.strftime('%Y-%m-%dT%H:%M:%S%z').replace('+0800', '+08:00')

# 更新HTML文件中的datetime
def update_datetime(file_path, new_datetime):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 在正则表达式之前先进行简单的文本替换处理已知的错误格式
        # 例如替换前面有P的日期
        content = re.sub(r'\nP(\d{2,4}-\d{2}-\d{2}T[^\n]*?)\n', f'\ndatetime: {new_datetime}\n', content)
        
        # 检查是否有datetime行
        datetime_pattern = r'(datetime: ).*?(\n)'
        
        if re.search(datetime_pattern, content):
            # 使用正则表达式替换datetime行
            updated_content = re.sub(datetime_pattern, f'\\1{new_datetime}\\2', content)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"已更新 {file_path} 的datetime为 {new_datetime}")
            return True
        else:
            # 如果没有匹配到标准的datetime行，尝试更强的匹配
            print(f"尝试修复 {file_path} 中的datetime行")
            # 查找前置元数据部分
            frontmatter_pattern = r'<!--\s*---.*?---\s*-->'
            frontmatter_match = re.search(frontmatter_pattern, content, re.DOTALL)
            
            if frontmatter_match:
                frontmatter = frontmatter_match.group(0)
                # 尝试多种匹配模式
                patterns = [
                    # 任何形式的日期/时间行
                    r'(\n)([^\n]*?(?:date|time)[^\n]*?)(\n)',
                    # 格式错误的datetime
                    r'(\n)(P?\d{2,4}-\d{2}-\d{2}T.*?)(\n)',
                    # 任何看起来像日期的行
                    r'(\n)(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}.*?)(\n)'
                ]
                
                replaced = False
                for pattern in patterns:
                    if re.search(pattern, frontmatter):
                        # 替换匹配的行
                        fixed_frontmatter = re.sub(pattern, f'\\1datetime: {new_datetime}\\3', frontmatter)
                        updated_content = content.replace(frontmatter, fixed_frontmatter)
                        
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(updated_content)
                        
                        print(f"已修复并更新 {file_path} 的datetime为 {new_datetime}")
                        replaced = True
                        break
                
                if replaced:
                    return True
                else:
                    # 在元数据中添加datetime行（如果没有找到任何日期相关行）
                    title_pattern = r'(title: .*?\n)'
                    if re.search(title_pattern, frontmatter):
                        fixed_frontmatter = re.sub(title_pattern, f'\\1datetime: {new_datetime}\\n', frontmatter)
                        updated_content = content.replace(frontmatter, fixed_frontmatter)
                        
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(updated_content)
                        
                        print(f"已在 {file_path} 中添加新的datetime: {new_datetime}")
                        return True
            
            print(f"无法在 {file_path} 中找到或修复datetime行")
            return False
    except Exception as e:
        print(f"更新 {file_path} 的datetime时出错: {e}")
        return False

# 主函数
def main():
    # ai目录的路径
    ai_dir = "ai"
    
    # 获取所有html和htm文件（除了index.html）
    html_files = []
    for file in os.listdir(ai_dir):
        if (file.endswith(".html") or file.endswith(".htm")) and file != "index.html":
            html_files.append(os.path.join(ai_dir, file))
    
    # 对每个文件更新datetime
    for file_path in html_files:
        git_time = get_git_creation_time(file_path)
        if git_time:
            update_datetime(file_path, git_time)
        else:
            print(f"无法获取 {file_path} 的git创建时间")

if __name__ == "__main__":
    main() 