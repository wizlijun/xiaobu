import os
import sys
import datetime
import re
import yaml
from collections import defaultdict
from pathlib import Path

def load_tags_yaml(tags_yaml_path):
    """加载tags.yaml文件并返回标签组信息"""
    try:
        with open(tags_yaml_path, 'r', encoding='utf-8') as f:
            tags_data = yaml.safe_load(f)
            
        # 创建从标签到组的映射
        tag_to_group = {}
        for group_name, tags in tags_data.get('tag_groups', {}).items():
            for tag in tags:
                tag_to_group[tag] = group_name
                
        # 获取文件标题映射
        file_titles = tags_data.get('file_titles', {})
        
        # 获取标签组显示名称
        group_display_names = tags_data.get('group_display_names', {})
                
        return tag_to_group, file_titles, group_display_names
    except Exception as e:
        print(f"读取tags.yaml文件出错: {e}")
        return {}, {}, {}

def extract_yaml_tags(yaml_content):
    """从YAML内容中提取tags字段"""
    if not yaml_content:
        return []
    
    # 尝试多种tags字段格式
    tags_patterns = [
        r'tags\s*:\s*\[(.*?)\]',              # 数组格式: tags: [tag1, tag2]
        r'tags\s*:\s*\n\s*-\s*(.*?)(?:\n|$)', # YAML列表格式: tags:\n  - tag1\n  - tag2
        r'tags\s*:\s*([\w\s,]+)',              # 简单格式: tags: tag1, tag2
    ]
    
    for pattern in tags_patterns:
        tags_match = re.search(pattern, yaml_content, re.IGNORECASE | re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1).strip()
            # 处理不同格式的标签
            if ',' in tags_str:  # 逗号分隔的格式
                return [tag.strip() for tag in tags_str.split(',')]
            elif '\n' in tags_str:  # 多行YAML列表
                return [line.strip().lstrip('- ') for line in tags_str.split('\n') if line.strip()]
            else:  # 单个标签或空格分隔
                return [tag.strip() for tag in tags_str.split() if tag.strip()]
    
    return []

def extract_yaml_datetime(file_path):
    """从HTML文件的YAML header中提取datetime字段"""
    try:
        print(f"尝试从 {file_path} 提取YAML日期")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 检查文件内容前30行，查看实际格式
            first_lines = '\n'.join(content.split('\n')[:30])
            print(f"文件前几行内容样本:\n{first_lines[:300]}...")
            
            # 尝试多种YAML header格式
            yaml_patterns = [
                # 标准的YAML格式，以三个短横线开始和结束
                r'^---\s*\n(.*?)\n---',
                # 也可能是HTML注释中的YAML
                r'<!--\s*---\s*\n(.*?)\n---\s*-->',
                # Jekyll风格的YAML front matter
                r'^---\s*\n(.*?)\n---\s*\n',
                # 简单的键值对格式（非严格YAML）
                r'<!--\s*((?:[\w-]+\s*:\s*.*\n)+)\s*-->'
            ]
            
            yaml_content = None
            for pattern in yaml_patterns:
                yaml_match = re.search(pattern, content, re.DOTALL)
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    print(f"使用模式 '{pattern}' 找到YAML header: {yaml_content[:100]}...")
                    break
            
            if yaml_content:
                # 提取tags信息
                tags = extract_yaml_tags(yaml_content)
                
                # 尝试多种datetime字段格式
                datetime_patterns = [
                    r'datetime\s*:\s*([\d\-: \.TZ+]+)',  # 标准格式: datetime: 2023-01-01 12:00
                    r'date\s*:\s*([\d\-: \.TZ+]+)',      # 或者使用date字段
                    r'time\s*:\s*([\d\-: \.TZ+]+)',      # 或者使用time字段
                    r'published\s*:\s*([\d\-: \.TZ+]+)', # 或者使用published字段
                    r'created\s*:\s*([\d\-: \.TZ+]+)'    # 或者使用created字段
                ]
                
                for pattern in datetime_patterns:
                    datetime_match = re.search(pattern, yaml_content, re.IGNORECASE)
                    if datetime_match:
                        yaml_datetime = datetime_match.group(1).strip()
                        print(f"找到日期字段: {yaml_datetime} (使用模式: {pattern})")
                        return yaml_datetime, tags, yaml_content
                
                print(f"YAML中没有找到任何日期相关字段")
                return None, tags, yaml_content
            else:
                print(f"文件中没有找到YAML header")
        return None, [], None
    except Exception as e:
        print(f"提取YAML日期时出错: {e}")
        return None, [], None

def extract_title(file_path):
    """从 HTML 文件中提取 <title> 内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else '无标题'
    except Exception as e:
        return '读取失败'

def generate_grouped_entries(file_infos, preurl, tag_to_group):
    """按年周分组生成 HTML 列表，包含标签信息"""
    groups = defaultdict(list)
    
    for info in file_infos:
        title, date_str, filename, file_tags = info
        
        # 确定group_tag
        group_tag = "others"  # 默认分组
        for tag in file_tags:
            if tag in tag_to_group:
                group_tag = tag_to_group[tag]
                break
        
        # 解析不同格式的日期字符串
        try:
            # 尝试解析ISO 8601格式
            if 'T' in date_str:
                # 处理带时区的ISO格式
                if '+' in date_str or 'Z' in date_str:
                    if 'Z' in date_str:  # UTC时间
                        date_str = date_str.replace('Z', '+00:00')
                    # 统一处理带时区的格式
                    date_obj = datetime.datetime.fromisoformat(date_str)
                else:
                    # 处理不带时区的ISO格式
                    date_obj = datetime.datetime.fromisoformat(date_str)
                
                # 保持兼容的日期显示格式
                display_date = date_obj.strftime('%Y-%m-%d %H:%M')
            else:
                # 处理旧的 %Y-%m-%d %H:%M 格式
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                display_date = date_str
        except ValueError:
            # 如果无法解析，尝试最后一种通用方法
            try:
                date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                display_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except:
                print(f"警告: 无法解析日期 '{date_str}'，使用当前时间")
                date_obj = datetime.datetime.now()
                display_date = date_obj.strftime('%Y-%m-%d %H:%M')
        
        # 获取年份和周数
        year, week, _ = date_obj.isocalendar()
        year_week = f'{year}.W{week:02d}'  # 修改为 YYYY.WXX 格式，周数补零为两位
        
        # 使用格式化后的日期显示和标签
        link = f'<li data-tags="{group_tag}"><a href="{preurl}{filename}">[{group_tag}]{title}</a>（{display_date}）</li>'
        groups[year_week].append((date_str, link))  # 保存原始日期用于排序

    # 排序输出（按年周倒序）
    output = []
    
    # 对年周键进行排序
    for year_week in sorted(groups.keys(), reverse=True):
        output.append(f'<h2>{year_week}</h2>\n<ul>')
        # 对每个周内的条目按日期时间倒序排序
        sorted_entries = sorted(groups[year_week], key=lambda x: x[0], reverse=True)
        # 只输出链接部分
        output.extend(entry[1] for entry in sorted_entries)
        output.append('</ul>')
    return '\n'.join(output)

def main(path_str, preurl):
    path = Path(path_str)
    if not path.is_dir():
        print(f"错误：路径不存在或不是目录：{path}")
        sys.exit(1)

    # 加载tags.yaml文件
    tags_yaml_path = Path('ai/tags.yaml')
    if not tags_yaml_path.exists():
        print(f"警告：找不到tags.yaml文件：{tags_yaml_path}")
        tag_to_group = {}
        file_titles = {}
        group_display_names = {}
    else:
        tag_to_group, file_titles, group_display_names = load_tags_yaml(tags_yaml_path)
        print(f"已加载 {len(tag_to_group)} 个标签映射和 {len(group_display_names)} 个标签组显示名称")

    html_files = [
        f for f in path.glob('*.htm*')
        if f.name not in {'index.html', 'template.html'}
    ]
    
    print(f"找到 {len(html_files)} 个HTML文件进行处理")

    file_infos = []
    for file in html_files:
        try:
            print(f"\n处理文件: {file.name}")
            # 优先从YAML header中获取日期和标签
            yaml_datetime, tags, yaml_content = extract_yaml_datetime(file)
            
            print(f"提取到的标签: {tags}")
            
            if yaml_datetime:
                # 如果能从YAML中获取到日期，使用它
                date_str = yaml_datetime
                print(f"使用YAML日期: {date_str}")
                # 确保日期格式统一，如果YAML中的日期格式不是'%Y-%m-%d %H:%M'，可能需要转换
                try:
                    # 使用标准ISO 8601格式解析
                    date_formats = [
                        '%Y-%m-%dT%H:%M:%S%z',  # 2023-01-01T12:00:00+0800
                        '%Y-%m-%dT%H:%M:%SZ',   # 2023-01-01T12:00:00Z (UTC)
                        '%Y-%m-%dT%H:%M:%S'     # 2023-01-01T12:00:00 (无时区信息)
                    ]
                    
                    parsed = False
                    for fmt in date_formats:
                        try:
                            parsed_date = datetime.datetime.strptime(date_str, fmt)
                            # 统一转换为带时区的ISO 8601格式
                            if fmt == '%Y-%m-%dT%H:%M:%S':
                                # 如果原始格式没有时区信息，假定为本地时区
                                local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                                parsed_date = parsed_date.replace(tzinfo=local_tz)
                            
                            date_str = parsed_date.strftime('%Y-%m-%dT%H:%M:%S%z')
                            # 将+0800格式转换为+08:00格式
                            if '+' in date_str or '-' in date_str:
                                offset_char = '+' if '+' in date_str else '-'
                                parts = date_str.split(offset_char)
                                offset = parts[1]
                                if len(offset) == 4:  # 无冒号格式
                                    date_str = f"{parts[0]}{offset_char}{offset[:2]}:{offset[2:]}"
                            
                            print(f"ISO 8601日期解析成功: {date_str}")
                            parsed = True
                            break
                        except ValueError:
                            continue
                    
                    if not parsed:
                        print(f"无法解析为ISO 8601格式: {date_str}，使用当前时间")
                        date_str = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
                        # 添加冒号到时区偏移
                        if '+' in date_str or '-' in date_str:
                            offset_char = '+' if '+' in date_str else '-'
                            parts = date_str.split(offset_char)
                            offset = parts[1]
                            if len(offset) == 4:  # 无冒号格式
                                date_str = f"{parts[0]}{offset_char}{offset[:2]}:{offset[2:]}"
                except Exception as e:
                    print(f"日期解析发生异常: {e}，使用当前时间")
                    date_str = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
                    # 添加冒号到时区偏移
                    if '+' in date_str or '-' in date_str:
                        offset_char = '+' if '+' in date_str else '-'
                        parts = date_str.split(offset_char)
                        offset = parts[1]
                        if len(offset) == 4:  # 无冒号格式
                            date_str = f"{parts[0]}{offset_char}{offset[:2]}:{offset[2:]}"
            else:
                # 如果YAML中没有日期，使用文件创建日期
                stat = file.stat()
                created = datetime.datetime.fromtimestamp(stat.st_ctime)
                date_str = created.strftime('%Y-%m-%d %H:%M')
                print(f"未找到YAML日期，使用文件创建日期: {date_str}")
                
            title = extract_title(file)
            print(f"文件标题: {title}")
            file_infos.append((title, date_str, file.name, tags))
        except Exception as e:
            print(f"跳过文件 {file}: {e}")

    # 按创建时间降序排列
    file_infos.sort(key=lambda x: x[1], reverse=True)

    # 读取模板
    template_path = path / 'template.html'
    if not template_path.exists():
        print("错误：找不到 template.html 模板文件")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    content_html = generate_grouped_entries(file_infos, preurl, tag_to_group)

    # 替换 <content> 标签内容
    new_index = re.sub(
        r'<content>(.*?)</content>',
        f'<content>\n{content_html}\n</content>',
        template,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # 更新标签组部分
    # 获取所有可用的tag groups
    tag_groups = set()
    for info in file_infos:
        _, _, _, file_tags = info
        for tag in file_tags:
            if tag in tag_to_group:
                tag_groups.add(tag_to_group[tag])
            else:
                tag_groups.add('others')
    
    # 生成标签组HTML
    tag_groups_html = '<div class="tags">\n'
    tag_groups_html += '<span class="tag active" data-tag="all">全部</span>\n'
    for group in sorted(tag_groups):
        # 使用配置的显示名称
        display_name = group_display_names.get(group, group)
        tag_groups_html += f'<span class="tag active" data-tag="{group}">{display_name}</span>\n'
    tag_groups_html += '</div>'
    
    # 替换标签组部分
    new_index = re.sub(
        r'<div class="tags">.*?</div>',
        tag_groups_html,
        new_index,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 写入 index.html
    index_path = path / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_index)

    print(f"index.html 已生成于：{index_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python genindex.py <path> <preurl>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])