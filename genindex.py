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
        group_articles = {}
        
        # 遍历所有分组（除了ignored_tags）
        for group_name, group_info in tags_data.items():
            if group_name == 'ignored_tags':
                continue
                
            if isinstance(group_info, dict) and 'tags' in group_info:
                # 获取分组的显示名称
                group_display_names[group_name] = group_info.get('name', group_name)
                
                # 获取分组的文章列表
                group_articles[group_name] = group_info.get('articles', [])
                
                # 将该分组下的所有标签映射到分组名
                for tag in group_info['tags']:
                    tag_to_group[tag] = group_name
        
        # 获取忽略的标签列表
        ignored_tags = set(tags_data.get('ignored_tags', []))
                
        return tag_to_group, group_display_names, group_articles, ignored_tags
    except Exception as e:
        print(f"读取tags.yaml文件出错: {e}")
        return {}, {}, {}, set()



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
        title, date_str, filename, file_tags, is_blog_file = info
        
        # 收集文件标签对应的所有标签组
        group_tags = set()
        for tag in file_tags:
            if tag in tag_to_group:
                group_tags.add(tag_to_group[tag])
        
        # 如果是blog文件，自动添加blog标签组
        if is_blog_file:
            group_tags.add("blog")
        
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

def load_meta_yaml(html_file_path, ignored_tags=None):
    """从对应的meta.yaml文件中读取信息"""
    if ignored_tags is None:
        ignored_tags = set()
        
    try:
        # 获取HTML文件的文件名（不含扩展名）
        html_file = Path(html_file_path)
        name_without_ext = html_file.stem
        
        # 构建meta.yaml文件路径：name_files/meta.yaml
        meta_yaml_path = html_file.parent / f"{name_without_ext}_files" / "meta.yaml"
        
        print(f"尝试读取meta.yaml文件: {meta_yaml_path}")
        
        if not meta_yaml_path.exists():
            print(f"meta.yaml文件不存在: {meta_yaml_path}")
            return None, None, None
        
        with open(meta_yaml_path, 'r', encoding='utf-8') as f:
            meta_data = yaml.safe_load(f)
        
        if not meta_data:
            print(f"meta.yaml文件为空或格式错误")
            return None, None, None
        
        # 提取标题
        title = meta_data.get('title') or meta_data.get('name')
        
        # 提取日期时间
        datetime_value = (meta_data.get('datetime') or 
                         meta_data.get('date') or 
                         meta_data.get('time') or 
                         meta_data.get('published') or 
                         meta_data.get('created'))
        
        # 提取标签
        raw_tags = meta_data.get('tags', [])
        if isinstance(raw_tags, str):
            # 如果tags是字符串，按逗号分割
            raw_tags = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]
        elif not isinstance(raw_tags, list):
            raw_tags = []
        
        # 过滤掉被忽略的标签
        tags = [tag for tag in raw_tags if tag and tag not in ignored_tags]
        
        print(f"从meta.yaml读取到 - 标题: {title}, 日期: {datetime_value}, 原始标签: {raw_tags}, 过滤后标签: {tags}")
        
        return title, datetime_value, tags
        
    except Exception as e:
        print(f"读取meta.yaml文件时出错: {e}")
        return None, None, None

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
        group_display_names = {}
        group_articles = {}
        ignored_tags = set()
    else:
        tag_to_group, group_display_names, group_articles, ignored_tags = load_tags_yaml(tags_yaml_path)
        print(f"已加载 {len(tag_to_group)} 个标签映射、{len(group_display_names)} 个标签组显示名称、{len(group_articles)} 个分组文章列表和 {len(ignored_tags)} 个忽略标签")

    # 添加blog标签组到映射
    group_display_names['blog'] = 'Blog'
    
    # 收集HTML文件：主目录和blog目录
    html_files = [
        f for f in path.glob('*.htm*')
        if f.name not in {'index.html', 'template.html', 'tags.html'}
    ]
    
    # 添加blog目录下的HTML文件
    blog_path = path / 'blog'
    if blog_path.is_dir():
        blog_files = [
            f for f in blog_path.glob('*.htm*')
            if f.name not in {'index.html', 'template.html', 'tags.html'}
        ]
        html_files.extend(blog_files)
        print(f"在blog目录中找到 {len(blog_files)} 个HTML文件")
    
    print(f"找到 {len(html_files)} 个HTML文件进行处理")

    file_infos = []
    for file in html_files:
        try:
            print(f"\n处理文件: {file}")
            # 严格只从meta.yaml文件中获取信息
            meta_title, meta_datetime, meta_tags = load_meta_yaml(file, ignored_tags)
            
            # 使用meta.yaml中的标签信息
            tags = meta_tags or []
            
            # 检查文件是否在blog目录中，如果是则自动添加blog标签组
            is_blog_file = 'blog' in file.parts
            if is_blog_file:
                print(f"检测到blog目录文件，自动归入blog标签组")
            
            print(f"提取到的标签: {tags}")
            
            # 时间处理：严格使用meta.yaml中的datetime
            if meta_datetime:
                date_str = str(meta_datetime)
                print(f"使用meta.yaml中的日期: {date_str}")
                
                # 确保日期格式正确
                try:
                    # 如果是字符串，尝试转换为ISO 8601格式
                    if isinstance(meta_datetime, str):
                        # 尝试不同的日期格式
                        date_formats = [
                            '%Y-%m-%dT%H:%M:%S%z',     # 2023-01-01T12:00:00+0800
                            '%Y-%m-%dT%H:%M:%S',       # 2023-01-01T12:00:00
                            '%Y-%m-%d %H:%M:%S',       # 2023-01-01 12:00:00
                            '%Y-%m-%d %H:%M',          # 2023-01-01 12:00
                            '%Y-%m-%d',                # 2023-01-01
                        ]
                        
                        parsed = False
                        for fmt in date_formats:
                            try:
                                parsed_date = datetime.datetime.strptime(date_str, fmt)
                                # 如果没有时区信息，添加本地时区
                                if fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
                                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                                    parsed_date = parsed_date.replace(tzinfo=local_tz)
                                
                                date_str = parsed_date.isoformat()
                                print(f"成功解析meta.yaml日期: {date_str}")
                                parsed = True
                                break
                            except ValueError:
                                continue
                        
                        if not parsed:
                            print(f"无法解析meta.yaml中的日期格式: {date_str}，使用当前时间")
                            raise ValueError("日期格式无法解析")
                    
                except Exception as e:
                    print(f"meta.yaml日期处理异常: {e}，使用当前时间")
                    current_time = datetime.datetime.now().astimezone()
                    date_str = current_time.isoformat()
                    print(f"使用当前时间: {date_str}")
            else:
                # meta.yaml中没有datetime，使用当前时间
                current_time = datetime.datetime.now().astimezone()
                date_str = current_time.isoformat()
                print(f"meta.yaml中没有datetime，使用当前时间: {date_str}")
                
            title = meta_title or extract_title(file)
            print(f"文件标题: {title}")
            
            # 对于blog目录下的文件，生成正确的相对路径
            if is_blog_file:
                relative_path = f"blog/{file.name}"
            else:
                relative_path = file.name
                
            file_infos.append((title, date_str, relative_path, tags, is_blog_file))
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
        _, _, _, file_tags, is_blog_file = info
        for tag in file_tags:
            if tag in tag_to_group:
                tag_groups.add(tag_to_group[tag])
        
        # 如果是blog文件，添加blog标签组
        if is_blog_file:
            tag_groups.add('blog')
        
        # 如果没有任何标签组，添加others
        if not any(tag in tag_to_group for tag in file_tags) and not is_blog_file:
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