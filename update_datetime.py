#!/usr/bin/env python3
import os
import yaml
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 中国时区（东八区）
CHINA_TZ = timezone(timedelta(hours=8))

def get_git_creation_time(file_path):
    """获取文件的git创建时间（ISO 8601格式）"""
    try:
        # 运行git命令获取文件的首次提交时间
        cmd = ["git", "log", "--follow", "--format=%aI", "--reverse", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dates = result.stdout.strip().split('\n')
        if dates and dates[0]:
            # 返回第一次提交的时间（标准ISO 8601格式）
            iso_date = dates[0].strip()
            print(f"Git创建时间: {iso_date}")
            return iso_date
        return None
    except subprocess.CalledProcessError as e:
        print(f"Git命令执行失败 {file_path}: {e}")
        return None
    except Exception as e:
        print(f"获取 {file_path} 的git创建时间时出错: {e}")
        return None

def is_valid_iso_datetime(datetime_str):
    """检查字符串是否是有效的ISO 8601格式"""
    if not datetime_str:
        return False
    
    # 常见的ISO 8601格式
    iso_formats = [
        '%Y-%m-%dT%H:%M:%S%z',      # 2023-01-01T12:00:00+08:00
        '%Y-%m-%dT%H:%M:%SZ',       # 2023-01-01T12:00:00Z
        '%Y-%m-%dT%H:%M:%S.%fZ',    # 2023-01-01T12:00:00.123456Z
        '%Y-%m-%dT%H:%M:%S.%f%z',   # 2023-01-01T12:00:00.123456+08:00
    ]
    
    try:
        datetime_str = str(datetime_str).strip()
        
        # 处理时区偏移格式（+0800 -> +08:00）
        if '+' in datetime_str or datetime_str.endswith('Z'):
            for fmt in iso_formats:
                try:
                    if 'Z' in datetime_str and fmt.endswith('Z'):
                        datetime.strptime(datetime_str, fmt)
                        return True
                    elif '%z' in fmt:
                        # 处理时区格式
                        test_str = datetime_str
                        if '+' in test_str:
                            parts = test_str.split('+')
                            if len(parts) > 1:
                                offset = parts[1]
                                if ':' not in offset and len(offset) == 4:
                                    test_str = f"{parts[0]}+{offset[:2]}:{offset[2:]}"
                        elif '-' in test_str.split('T')[1] if 'T' in test_str else False:
                            # 处理负时区偏移
                            for i, char in enumerate(test_str):
                                if char == '-' and i > 10:  # 确保不是日期中的-
                                    prefix = test_str[:i]
                                    offset = test_str[i+1:]
                                    if ':' not in offset and len(offset) == 4:
                                        test_str = f"{prefix}-{offset[:2]}:{offset[2:]}"
                                    break
                        
                        datetime.strptime(test_str, fmt)
                        return True
                except ValueError:
                    continue
        return False
    except Exception:
        return False

def get_current_china_time():
    """获取当前中国时间（ISO 8601格式）"""
    china_time = datetime.now(CHINA_TZ)
    return china_time.isoformat()

def read_meta_yaml(meta_yaml_path):
    """读取meta.yaml文件"""
    try:
        if not meta_yaml_path.exists():
            return None
        
        with open(meta_yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"读取meta.yaml文件出错: {e}")
        return None

def write_meta_yaml(meta_yaml_path, data):
    """写入meta.yaml文件"""
    try:
        # 确保目录存在
        meta_yaml_path.parent.mkdir(exist_ok=True)
        
        with open(meta_yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
        return True
    except Exception as e:
        print(f"写入meta.yaml文件出错: {e}")
        return False

def process_html_file(html_file_path):
    """处理单个HTML文件的datetime"""
    html_file = Path(html_file_path)
    name_without_ext = html_file.stem
    
    # 构建meta.yaml路径
    meta_yaml_path = html_file.parent / f"{name_without_ext}_files" / "meta.yaml"
    
    print(f"\n处理文件: {html_file.name}")
    print(f"对应的meta.yaml路径: {meta_yaml_path}")
    
    # 读取meta.yaml
    meta_data = read_meta_yaml(meta_yaml_path)
    
    if meta_data is None:
        # meta.yaml不存在，创建新的
        print("meta.yaml文件不存在，创建新文件")
        meta_data = {}
    
    # 检查datetime字段
    current_datetime = meta_data.get('datetime')
    new_datetime = None
    
    if current_datetime:
        print(f"当前datetime值: {current_datetime}")
        
        if is_valid_iso_datetime(current_datetime):
            print("datetime格式有效，无需修改")
            return True
        else:
            print("datetime格式无效，使用当前中国时间")
            new_datetime = get_current_china_time()
    else:
        print("meta.yaml中没有datetime字段")
        
        # 尝试从git获取创建时间
        git_time = get_git_creation_time(html_file_path)
        if git_time:
            print(f"使用git创建时间: {git_time}")
            new_datetime = git_time
        else:
            print("无法获取git创建时间，使用当前中国时间")
            new_datetime = get_current_china_time()
    
    if new_datetime:
        # 更新datetime字段
        meta_data['datetime'] = new_datetime
        
        # 如果没有title字段，从HTML文件提取
        if 'title' not in meta_data:
            title = extract_title_from_html(html_file_path)
            if title:
                meta_data['title'] = title
        
        # 写入meta.yaml
        if write_meta_yaml(meta_yaml_path, meta_data):
            print(f"成功更新meta.yaml，datetime: {new_datetime}")
            return True
        else:
            print("写入meta.yaml失败")
            return False
    
    return True

def extract_title_from_html(html_file_path):
    """从HTML文件中提取title"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找<title>标签
        import re
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        print(f"从HTML提取标题失败: {e}")
        return None

def main():
    """主函数"""
    # ai目录的路径
    ai_dir = Path("ai")
    
    if not ai_dir.exists():
        print(f"错误：目录 {ai_dir} 不存在")
        return
    
    # 获取所有HTML文件（除了特殊文件）
    excluded_files = {"index.html", "template.html", "tags.html"}
    html_files = []
    
    for file_path in ai_dir.glob("*.html"):
        if file_path.name not in excluded_files:
            html_files.append(file_path)
    
    for file_path in ai_dir.glob("*.htm"):
        if file_path.name not in excluded_files:
            html_files.append(file_path)
    
    if not html_files:
        print(f"在 {ai_dir} 目录中没有找到需要处理的HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件需要处理")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    # 处理每个HTML文件
    for html_file in sorted(html_files):
        try:
            if process_html_file(html_file):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"处理文件 {html_file.name} 时出错: {e}")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"处理完成！成功: {success_count}, 失败: {fail_count}")
    
    if success_count > 0:
        print(f"\n提示：可以运行 genindex.py 来重新生成索引")

if __name__ == "__main__":
    main() 