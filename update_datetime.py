#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime, timezone

# 获取文件的git创建时间
def get_git_creation_time(file_path):
    try:
        # 运行git命令获取文件的首次提交时间（ISO 8601格式）
        cmd = ["git", "log", "--follow", "--format=%aI", "--reverse", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dates = result.stdout.strip().split('\n')
        if dates and dates[0]:
            # 返回第一次提交的时间（标准ISO 8601格式）
            # 确保时区偏移格式正确（+08:00而不是+0800）
            iso_date = dates[0].strip()
            if '+' in iso_date or '-' in iso_date:
                # 处理时区偏移格式
                if iso_date.endswith('Z'):
                    # UTC时间，转换为本地时区
                    dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
                    local_dt = dt.astimezone()
                    iso_date = local_dt.strftime('%Y-%m-%dT%H:%M:%S%z')
                
                # 确保时区偏移有冒号
                offset_char = '+' if '+' in iso_date else '-'
                if offset_char in iso_date:
                    parts = iso_date.split(offset_char)
                    if len(parts) > 1:
                        offset = parts[1]
                        if ':' not in offset and len(offset) == 4:  # 处理无冒号格式
                            iso_date = f"{parts[0]}{offset_char}{offset[:2]}:{offset[2:]}"
            return iso_date
        return None
    except subprocess.CalledProcessError as e:
        print(f"Git命令执行失败 {file_path}: {e}")
        return None
    except Exception as e:
        print(f"获取 {file_path} 的git创建时间时出错: {e}")
        return None

# 更新HTML文件中的datetime
def update_datetime(file_path, new_datetime):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找YAML front matter（支持HTML注释包围的格式）
        yaml_patterns = [
            r'(<!--\s*---\s*\n)(.*?)(\n---\s*-->)',  # HTML注释包围的YAML
            r'(<!--\s*\n---\s*\n)(.*?)(\n---\s*\n-->)',  # 另一种HTML注释格式
            r'(<!--\s*\n---\s*\n)(.*?)(\n-->)',      # 简化的HTML注释格式（没有结束的---）
            r'(---\s*\n)(.*?)(\n---)',               # 标准YAML front matter
        ]
        
        updated = False
        for pattern in yaml_patterns:
            yaml_match = re.search(pattern, content, re.DOTALL)
            if yaml_match:
                yaml_start = yaml_match.group(1)
                yaml_content = yaml_match.group(2)
                yaml_end = yaml_match.group(3)
                
                # 检查是否已有datetime字段
                datetime_patterns = [
                    r'datetime:\s*.*',
                    r'date:\s*.*',
                    r'P?\d{4}-\d{2}-\d{2}T.*',  # 处理格式错误的日期行
                ]
                
                datetime_found = False
                for dt_pattern in datetime_patterns:
                    if re.search(dt_pattern, yaml_content):
                        # 替换现有的datetime行
                        yaml_content = re.sub(dt_pattern, f'datetime: {new_datetime}', yaml_content)
                        datetime_found = True
                        break
                
                if not datetime_found:
                    # 如果没有找到datetime字段，在title后面添加
                    title_pattern = r'(title:\s*.*?\n)'
                    if re.search(title_pattern, yaml_content):
                        yaml_content = re.sub(title_pattern, f'\\1datetime: {new_datetime}\n', yaml_content)
                    else:
                        # 如果没有title，在开头添加
                        yaml_content = f'datetime: {new_datetime}\n{yaml_content}'
                
                # 重新组装YAML front matter
                new_yaml = yaml_start + yaml_content + yaml_end
                updated_content = content.replace(yaml_match.group(0), new_yaml)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                
                print(f"已更新 {file_path} 的datetime为 {new_datetime}")
                updated = True
                break
        
        if not updated:
            print(f"在 {file_path} 中未找到YAML front matter")
            return False
        
        return True
    except Exception as e:
        print(f"更新 {file_path} 的datetime时出错: {e}")
        return False

# 主函数
def main():
    # ai目录的路径
    ai_dir = "ai"
    
    if not os.path.exists(ai_dir):
        print(f"错误：目录 {ai_dir} 不存在")
        return
    
    # 获取所有html和htm文件（除了index.html和template.html）
    html_files = []
    excluded_files = {"index.html", "template.html", "tags.html"}
    
    for file in os.listdir(ai_dir):
        if (file.endswith(".html") or file.endswith(".htm")) and file not in excluded_files:
            html_files.append(os.path.join(ai_dir, file))
    
    if not html_files:
        print(f"在 {ai_dir} 目录中没有找到需要处理的HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件需要处理")
    print("=" * 50)
    
    success_count = 0
    fail_count = 0
    
    # 对每个文件更新datetime
    for file_path in sorted(html_files):
        print(f"\n处理文件: {os.path.basename(file_path)}")
        git_time = get_git_creation_time(file_path)
        if git_time:
            print(f"Git创建时间: {git_time}")
            if update_datetime(file_path, git_time):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"无法获取 {file_path} 的git创建时间")
            fail_count += 1
    
    print("\n" + "=" * 50)
    print(f"处理完成！成功: {success_count}, 失败: {fail_count}")

if __name__ == "__main__":
    main() 