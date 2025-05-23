import os
import sys
import datetime
import re
from collections import defaultdict
from pathlib import Path

def extract_yaml_datetime(file_path):
    """从HTML文件的YAML header中提取datetime字段"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找YAML header（在文件开头由---包围的部分）
            yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if yaml_match:
                yaml_content = yaml_match.group(1)
                # 在YAML内容中查找datetime字段
                datetime_match = re.search(r'datetime\s*:\s*([\d\-: ]+)', yaml_content)
                if datetime_match:
                    return datetime_match.group(1).strip()
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

    file_infos = []
    for file in html_files:
        try:
            # 优先从YAML header中获取日期
            yaml_datetime = extract_yaml_datetime(file)
            
            if yaml_datetime:
                # 如果能从YAML中获取到日期，使用它
                date_str = yaml_datetime
                # 确保日期格式统一，如果YAML中的日期格式不是'%Y-%m-%d %H:%M'，可能需要转换
                try:
                    # 尝试解析并重新格式化为统一格式
                    parsed_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                    date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                except ValueError:
                    # 如果格式不匹配，尝试其他常见格式
                    try:
                        parsed_date = datetime.datetime.fromisoformat(date_str)
                        date_str = parsed_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        # 如果无法解析，回退到使用文件创建日期
                        stat = file.stat()
                        created = datetime.datetime.fromtimestamp(stat.st_ctime)
                        date_str = created.strftime('%Y-%m-%d %H:%M')
            else:
                # 如果YAML中没有日期，使用文件创建日期
                stat = file.stat()
                created = datetime.datetime.fromtimestamp(stat.st_ctime)
                date_str = created.strftime('%Y-%m-%d %H:%M')
                
            title = extract_title(file)
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