import os
import sys
import datetime
import re
from collections import defaultdict
from pathlib import Path

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
                        return yaml_datetime
                
                print(f"YAML中没有找到任何日期相关字段")
            else:
                print(f"文件中没有找到YAML header")
        return None
    except Exception as e:
        print(f"提取YAML日期时出错: {e}")
        return None

def extract_title(file_path):
    """从 HTML 文件中提取 <title> 内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else '无标题'
    except Exception as e:
        return '读取失败'

def generate_grouped_entries(file_infos, preurl):
    """按年周分组生成 HTML 列表"""
    groups = defaultdict(list)
    for info in file_infos:
        title, date_str, filename = info
        # 将日期字符串转换为 datetime 对象
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        # 获取年份和周数
        year, week, _ = date_obj.isocalendar()
        year_week = f'{year}.W{week:02d}'  # 修改为 YYYY.WXX 格式，周数补零为两位
        link = f'<li><a href="{preurl}{filename}">{title}</a>（{date_str}）</li>'
        groups[year_week].append((date_str, link))  # 保存日期用于排序

    # 排序输出（按年周倒序）
    output = []
    # 首先对年周键进行排序
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

    html_files = [
        f for f in path.glob('*.htm*')
        if f.name not in {'index.html', 'template.html'}
    ]
    
    print(f"找到 {len(html_files)} 个HTML文件进行处理")

    file_infos = []
    for file in html_files:
        try:
            print(f"\n处理文件: {file.name}")
            # 优先从YAML header中获取日期
            yaml_datetime = extract_yaml_datetime(file)
            
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
            file_infos.append((title, date_str, file.name))
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

    content_html = generate_grouped_entries(file_infos, preurl)

    # 替换 <content> 标签内容
    new_index = re.sub(
        r'<content>(.*?)</content>',
        f'<content>\n{content_html}\n</content>',
        template,
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