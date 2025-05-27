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
        group_display_names = {}
        
        # 遍历所有分组（除了ignored_tags）
        for group_name, group_info in tags_data.items():
            if group_name == 'ignored_tags':
                continue
                
            if isinstance(group_info, dict) and 'tags' in group_info:
                # 获取分组的显示名称
                group_display_names[group_name] = group_info.get('name', group_name)
                
                # 将该分组下的所有标签映射到分组名
                for tag in group_info['tags']:
                    tag_to_group[tag] = group_name
        
        # 获取忽略的标签列表
        ignored_tags = set(tags_data.get('ignored_tags', []))
                
        return tag_to_group, {}, group_display_names, ignored_tags
    except Exception as e:
        print(f"读取tags.yaml文件出错: {e}")
        return {}, {}, {}, set()

def extract_yaml_tags(yaml_content, ignored_tags=None):
    """从YAML内容中提取tags字段，并过滤掉被忽略的标签"""
    if not yaml_content:
        return []
    
    if ignored_tags is None:
        ignored_tags = set()
    
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
                raw_tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]
            elif '\n' in tags_str:  # 多行YAML列表
                raw_tags = [line.strip().lstrip('- ').strip('"\'') for line in tags_str.split('\n') if line.strip()]
            else:  # 单个标签或空格分隔
                raw_tags = [tag.strip().strip('"\'') for tag in tags_str.split() if tag.strip()]
            
            # 过滤掉被忽略的标签
            filtered_tags = [tag for tag in raw_tags if tag and tag not in ignored_tags]
            return filtered_tags
    
    return []

def extract_yaml_datetime(file_path, ignored_tags=None):
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
                # 提取tags信息，传递ignored_tags参数
                tags = extract_yaml_tags(yaml_content, ignored_tags)
                
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

def extract_datetime_from_filename(filename):
    """尝试从文件名中提取日期时间信息"""
    # 常见的日期格式模式
    patterns = [
        r'(\d{4})[_\-]?(\d{2})[_\-]?(\d{2})[_\-]?(\d{2})[_\-]?(\d{2})',  # 20230101_1200 或 2023-01-01-12-00
        r'(\d{4})[_\-]?(\d{2})[_\-]?(\d{2})',                            # 20230101 或 2023-01-01
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            groups = match.groups()
            if len(groups) == 5:  # 带时间
                year, month, day, hour, minute = groups
                try:
                    dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
                    # 添加本地时区
                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                    dt = dt.replace(tzinfo=local_tz)
                    return dt.isoformat()
                except ValueError:
                    pass
            elif len(groups) == 3:  # 只有日期
                year, month, day = groups
                try:
                    dt = datetime.datetime(int(year), int(month), int(day))
                    # 添加本地时区
                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                    dt = dt.replace(tzinfo=local_tz)
                    return dt.isoformat()
                except ValueError:
                    pass
    return None

def generate_grouped_entries(file_infos, preurl, tag_to_group):
    """按年周分组生成 HTML 列表，包含标签信息"""
    groups = defaultdict(list)
    
    for info in file_infos:
        title, date_str, filename, file_tags = info
        
        # 收集文件标签对应的所有标签组
        group_tags = set()
        for tag in file_tags:
            if tag in tag_to_group:
                group_tags.add(tag_to_group[tag])
        
        # 如果没有找到任何标签组，使用默认分组
        if not group_tags:
            group_tags.add("others")
        
        # 按字母顺序排序标签组
        sorted_group_tags = sorted(group_tags)
        
        # 生成标签组标记，如 [ai][se]
        group_tags_str = "".join(f"[{tag}]" for tag in sorted_group_tags)
        
        # 用于筛选的data-tags属性值
        data_tags_attr = " ".join(sorted_group_tags)
        
        # 解析不同格式的日期字符串
        try:
            # 统一将所有日期转换为datetime对象，不论格式如何
            if 'T' in date_str:
                # ISO 8601格式
                if '+' in date_str or '-' in date_str.split('T')[1] or 'Z' in date_str:
                    # 带时区信息的ISO格式
                    if 'Z' in date_str:
                        date_str = date_str.replace('Z', '+00:00')
                    # 处理时区格式没有冒号的情况（例如+0800）
                    if '+' in date_str or '-' in date_str.split('T')[1]:
                        for char in ['+', '-']:
                            if char in date_str.split('T')[1]:
                                parts = date_str.split(char)
                                if len(parts) > 1:
                                    offset = parts[1]
                                    if len(offset) == 4 and ':' not in offset:  # 如+0800
                                        date_str = f"{parts[0]}{char}{offset[:2]}:{offset[2:]}"
                    date_obj = datetime.datetime.fromisoformat(date_str)
                else:
                    # 不带时区的ISO格式，假定为本地时区
                    date_obj = datetime.datetime.fromisoformat(date_str)
                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                    date_obj = date_obj.replace(tzinfo=local_tz)
            else:
                # 旧格式 YYYY-MM-DD HH:MM
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                # 添加本地时区
                local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                date_obj = date_obj.replace(tzinfo=local_tz)
            
            # 统一显示格式
            display_date = date_obj.strftime('%Y-%m-%d %H:%M')
        except Exception as e:
            # 任何解析错误，使用当前时间
            print(f"日期解析错误 '{date_str}': {e}，使用当前时间")
            date_obj = datetime.datetime.now().astimezone()  # 带时区的当前时间
            display_date = date_obj.strftime('%Y-%m-%d %H:%M')
        
        # 获取年份和周数
        year, week, _ = date_obj.isocalendar()
        year_week = f'{year}.W{week:02d}'  # 修改为 YYYY.WXX 格式，周数补零为两位
        
        # 构建相对路径链接（不使用斜杠开头的绝对路径）
        href = f"{filename}" if not preurl else f"{preurl.lstrip('/')}{filename}"
        
        # 使用格式化后的日期显示和标签
        link = f'<li data-tags="{data_tags_attr}"><a href="{href}">{group_tags_str}{title}</a>（{display_date}）</li>'
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
        ignored_tags = set()
    else:
        tag_to_group, file_titles, group_display_names, ignored_tags = load_tags_yaml(tags_yaml_path)
        print(f"已加载 {len(tag_to_group)} 个标签映射、{len(group_display_names)} 个标签组显示名称和 {len(ignored_tags)} 个忽略标签")

    html_files = [
        f for f in path.glob('*.htm*')
        if f.name not in {'index.html', 'template.html', 'tags.html'}
    ]
    
    print(f"找到 {len(html_files)} 个HTML文件进行处理")

    file_infos = []
    for file in html_files:
        try:
            print(f"\n处理文件: {file.name}")
            # 优先从YAML header中获取日期和标签
            yaml_datetime, tags, yaml_content = extract_yaml_datetime(file, ignored_tags)
            
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
                # 如果YAML中没有日期，尝试从文件名提取
                filename_date = extract_datetime_from_filename(file.name)
                if filename_date:
                    date_str = filename_date
                    print(f"从文件名提取到日期: {date_str}")
                else:
                    # 如果文件名中没有日期，使用文件修改时间
                    stat = file.stat()
                    modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                    
                    # 添加系统时区信息
                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                    modified_with_tz = modified.replace(tzinfo=local_tz)
                    date_str = modified_with_tz.isoformat()
                    
                    print(f"使用文件修改时间: {date_str}")
                
            title = extract_title(file)
            print(f"文件标题: {title}")
            file_infos.append((title, date_str, file.name, tags))
        except Exception as e:
            print(f"跳过文件 {file}: {e}")

    # 按创建时间降序排列，如果时间相同则按文件名排序（确保排序稳定性）
    file_infos.sort(key=lambda x: (x[1], x[2]), reverse=True)

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

    # 确保others标签组显示在最后
    sorted_groups = sorted([g for g in tag_groups if g != 'others'])
    if 'others' in tag_groups:
        sorted_groups.append('others')

    for group in sorted_groups:
        # 使用配置的显示名称
        display_name = group_display_names.get(group, group)
        tag_groups_html += f'<span class="tag" data-tag="{group}">{display_name}</span>\n'
    tag_groups_html += '</div>'
    
    # 替换标签组部分
    new_index = re.sub(
        r'<div class="tags">.*?</div>',
        tag_groups_html,
        new_index,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 修复JavaScript标签筛选功能
    js_fix = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const tags = document.querySelectorAll('.tag');
        const listItems = document.querySelectorAll('li[data-tags]');
        
        // 当前选中的标签
        let activeTag = 'all';
        
        // 解析URL参数
        function getUrlParameter(name) {
            const url = window.location.search.substring(1);
            const urlParams = url.split('&');
            for (let i = 0; i < urlParams.length; i++) {
                const paramName = urlParams[i].split('=');
                if (paramName[0] === name) {
                    return paramName[1] === undefined ? true : decodeURIComponent(paramName[1]);
                }
            }
            // 特殊处理: 如果URL是index.html?tagname的形式
            if (url && !url.includes('=')) {
                return url;
            }
            return null;
        }
        
        // 更新可见性
        function updateVisibility() {
            if (activeTag === 'all') {
                // 显示所有项目
                listItems.forEach(item => {
                    item.style.display = '';
                });
            } else {
                // 根据标签筛选
                listItems.forEach(item => {
                    const itemTags = item.getAttribute('data-tags').split(' ');
                    if (itemTags.includes(activeTag)) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
            
            // 更新年周标题可见性
            document.querySelectorAll('h2').forEach(heading => {
                const nextElement = heading.nextElementSibling;
                if (nextElement && nextElement.tagName === 'UL') {
                    const visibleItems = Array.from(nextElement.querySelectorAll('li')).filter(li => 
                        li.style.display !== 'none'
                    );
                    heading.style.display = visibleItems.length > 0 ? '' : 'none';
                    nextElement.style.display = visibleItems.length > 0 ? '' : 'none';
                }
            });
        }
        
        // 激活特定标签
        function activateTag(tagName) {
            const tagElement = document.querySelector(`.tag[data-tag="${tagName}"]`);
            if (tagElement) {
                // 移除所有标签激活状态
                tags.forEach(t => t.classList.remove('active'));
                
                // 设置指定标签为激活状态
                tagElement.classList.add('active');
                
                // 更新当前活跃标签
                activeTag = tagName;
                
                // 更新URL
                if (tagName === 'all') {
                    // 如果选择"全部"标签，则移除URL参数部分
                    const urlWithoutParams = window.location.pathname;
                    history.pushState(null, document.title, urlWithoutParams);
                } else {
                    // 如果选择特定标签，则更新URL参数
                    // 确保无论是否有斜杠或index.html都能正确生成URL
                    let basePath = window.location.pathname;
                    
                    // 处理URL末尾可能没有index.html的情况
                    if (basePath.endsWith('/')) {
                        basePath += 'index.html';
                    } else if (!basePath.includes('.html')) {
                        // 如果路径既不以/结尾，也不包含.html，添加/index.html
                        basePath += '/index.html';
                    }
                    
                    const urlWithParams = basePath + '?' + tagName;
                    history.pushState(null, document.title, urlWithParams);
                }
                
                // 更新可见性
                updateVisibility();
                
                return true;
            }
            return false;
        }
        
        // 标签点击事件
        tags.forEach(tag => {
            tag.addEventListener('click', function() {
                const tagName = this.getAttribute('data-tag');
                activateTag(tagName);
            });
        });
        
        // 检查URL参数
        const tagParam = getUrlParameter('taggroup') || getUrlParameter('tag');
        if (tagParam) {
            // 尝试激活URL中指定的标签
            if (!activateTag(tagParam)) {
                // 如果没有找到匹配的标签，则使用默认的"all"标签
                activateTag('all');
            }
        } else {
            // 初始化显示
            updateVisibility();
        }
    });
    </script>
    """

    # 替换JavaScript部分
    new_index = re.sub(
        r'<script>.*?</script>',
        js_fix,
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