import os
import sys
import datetime
import re
from collections import defaultdict
from pathlib import Path

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
            stat = file.stat()
            created = datetime.datetime.fromtimestamp(stat.st_ctime)
            date_str = created.strftime('%Y-%m-%d %H:%M')  # 修改时间格式精确到分钟
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