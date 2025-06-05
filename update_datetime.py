#!/usr/bin/env python3
import os
import yaml
import subprocess
from pathlib import Path



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
    """处理单个HTML文件的datetime - 用git创建时间更新meta.yaml"""
    html_file = Path(html_file_path)
    name_without_ext = html_file.stem
    
    # 构建meta.yaml路径
    meta_yaml_path = html_file.parent / f"{name_without_ext}_files" / "meta.yaml"
    
    print(f"\n处理文件: {html_file.name}")
    print(f"对应的meta.yaml路径: {meta_yaml_path}")
    
    # 首先获取git创建时间
    git_time = get_git_creation_time(html_file_path)
    if not git_time:
        print("无法获取git创建时间，跳过此文件")
        return False
    
    # 读取meta.yaml
    meta_data = read_meta_yaml(meta_yaml_path)
    
    if meta_data is None:
        # meta.yaml不存在，创建新的
        print("meta.yaml文件不存在，创建新文件")
        meta_data = {}
    
    # 显示当前datetime（如果存在）
    current_datetime = meta_data.get('datetime')
    if current_datetime:
        print(f"当前datetime值: {current_datetime}")
    else:
        print("meta.yaml中没有datetime字段")
    
    # 直接用git时间更新datetime字段
    print(f"更新为git创建时间: {git_time}")
    meta_data['datetime'] = git_time
    
    # 如果没有title字段，从HTML文件提取
    if 'title' not in meta_data:
        title = extract_title_from_html(html_file_path)
        if title:
            meta_data['title'] = title
            print(f"添加标题: {title}")
    
    # 写入meta.yaml
    if write_meta_yaml(meta_yaml_path, meta_data):
        print(f"成功更新meta.yaml，datetime: {git_time}")
        return True
    else:
        print("写入meta.yaml失败")
        return False

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