#!/usr/bin/env python3
import os
import re
import yaml
from collections import defaultdict

# 定义分组关键词
TAG_GROUPS = {
    'bushcraft': ['bushcraft', 'outdoor', 'camping', '露营', '野外', '生存', '技艺', 'survival', 'nature', 'skills', 'crafts', 'blacksmith', 'birchbark', 'cooking', 'talkbc', 'fullbc', 'outdoors'],
    'ai': ['ai', 'llm', 'gpt', 'claude', 'gemini', 'model', '人工智能', '大模型', 'openai', 'altman', 'microsoft', 'meta', 'atlassian'],
    'mind': ['mind', 'psychology', 'cognitive', 'mental', 'brain', '思维', '心理', '认知', '大脑', 'philosophy', 'stoic', 'stoicism', 'learning', 'education', 'taxonomy', 'youth', 'society', 'community', 'belonging', 'life', 'anthropology', 'evolution'],
    'se': ['software', 'programming', 'code', 'development', 'engineering', '软件', '编程', '代码', '开发', 'tools', 'pkm', 'roam', 'notes', 'productivity', 'research', 'business', 'management', 'coordination', 'leadership'],
    'others': []  # 默认分组
}

# 直接映射某些特定标签到指定分组
DIRECT_TAG_MAPPING = {
    'survival': 'bushcraft',
    'nature': 'bushcraft',
    'skills': 'bushcraft',
    'crafts': 'bushcraft',
    'cooking': 'bushcraft',
    'notes': 'se',
    'tools': 'se',
    'pkm': 'se',
    'roam': 'se',
    'productivity': 'se',
    'management': 'se',
    'coordination': 'se',
    'business': 'se',
    'leadership': 'se',
    'research': 'se',
    'society': 'mind',
    'community': 'mind',
    'belonging': 'mind',
    'philosophy': 'mind',
    'stoicism': 'mind',
    'learning': 'mind',
    'education': 'mind',
    'anthropology': 'mind',
    'youth': 'mind',
    'life': 'mind',
    'evolution': 'mind',
    'taxonomy': 'mind',
    'atlassian': 'se',
    'meta': 'ai',
    'microsoft': 'ai',
    'altman': 'ai',
}

# 无意义的标签列表
MEANINGLESS_TAGS = ['tag1', 'tag2', 'tag3', 'sample', 'test', 'example']

def parse_yaml_header(html_content):
    """从HTML内容中解析YAML头部"""
    # 匹配HTML注释中的YAML头部
    yaml_pattern = re.compile(r'<!--\s*---\s*(.*?)\s*---\s*-->', re.DOTALL)
    match = yaml_pattern.search(html_content)
    
    if match:
        yaml_str = match.group(1)
        try:
            # 解析YAML
            data = yaml.safe_load(yaml_str)
            return data
        except yaml.YAMLError as e:
            print(f"解析YAML时出错: {e}")
    
    return None

def get_tag_group(tag):
    """确定标签属于哪个分组"""
    tag_lower = tag.lower()
    
    # 检查标签是否无意义
    if tag_lower in MEANINGLESS_TAGS:
        return None
    
    # 首先检查直接映射
    if tag_lower in DIRECT_TAG_MAPPING:
        return DIRECT_TAG_MAPPING[tag_lower]
    
    # 然后检查关键词匹配
    for group, keywords in TAG_GROUPS.items():
        for keyword in keywords:
            if keyword in tag_lower:
                return group
    
    # 默认归类为others
    return 'others'

def main():
    # 获取ai目录中的所有HTML文件
    ai_dir = 'ai'
    html_files = [f for f in os.listdir(ai_dir) if f.endswith(('.html', '.htm'))]
    
    # 收集所有标签
    all_tags = defaultdict(list)  # 标签 -> 文件列表
    tag_groups = defaultdict(set)  # 分组 -> 标签集合
    file_titles = {}  # 文件名 -> 标题
    
    for html_file in html_files:
        file_path = os.path.join(ai_dir, html_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            yaml_data = parse_yaml_header(content)
            if yaml_data:
                # 存储文件标题
                if 'title' in yaml_data:
                    file_titles[html_file] = yaml_data['title']
                else:
                    # 尝试从HTML的title标签中提取
                    title_match = re.search(r'<title>(.*?)</title>', content)
                    if title_match:
                        file_titles[html_file] = title_match.group(1)
                    else:
                        file_titles[html_file] = html_file  # 默认使用文件名
                
                # 处理标签
                if 'tags' in yaml_data and yaml_data['tags']:
                    for tag in yaml_data['tags']:
                        # 忽略无意义的标签
                        if tag.lower() in MEANINGLESS_TAGS:
                            continue
                        
                        # 添加到标签索引
                        all_tags[tag].append(html_file)
                        
                        # 分组标签
                        group = get_tag_group(tag)
                        if group:
                            tag_groups[group].add(tag)
            else:
                # 对于没有YAML头部的文件，使用文件名作为标题
                file_titles[html_file] = html_file
                
        except Exception as e:
            print(f"处理文件 {html_file} 时出错: {e}")
            file_titles[html_file] = html_file  # 出错时使用文件名作为标题
    
    # 创建tags.yaml文件
    tags_yaml = {
        'tag_groups': {group: sorted(list(tags)) for group, tags in tag_groups.items()},
        'all_tags': {tag: sorted(files) for tag, files in all_tags.items()},
        'file_titles': file_titles
    }
    
    with open(os.path.join(ai_dir, 'tags.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(tags_yaml, f, allow_unicode=True, default_flow_style=False)
    
    # 创建tags.html文件
    tags_html = generate_tags_html(all_tags, tag_groups, file_titles)
    
    with open(os.path.join(ai_dir, 'tags.html'), 'w', encoding='utf-8') as f:
        f.write(tags_html)
    
    print(f"成功解析 {len(html_files)} 个HTML文件")
    print(f"共发现 {len(all_tags)} 个不同的标签")
    print(f"生成了 {os.path.join(ai_dir, 'tags.yaml')} 和 {os.path.join(ai_dir, 'tags.html')}")

def generate_tags_html(all_tags, tag_groups, file_titles):
    """生成标签HTML页面"""
    # 按组排序的标签列表
    grouped_tags_html = ""
    for group, tags in sorted(tag_groups.items()):
        if tags:  # 只显示有标签的分组
            grouped_tags_html += f"""
            <div class="tag-group">
                <h2>{group}</h2>
                <div class="tags">
                    {"".join(f'<span class="tag" data-tag="{tag}">{tag} <small>({len(all_tags[tag])})</small></span>' for tag in sorted(tags))}
                </div>
            </div>
            """
    
    # 所有标签对应的文章列表
    tag_articles_html = ""
    for tag, files in sorted(all_tags.items()):
        tag_group = get_tag_group(tag)
        tag_articles_html += f"""
        <div class="tag-articles" id="tag-{tag.replace(' ', '-')}">
            <h3>{tag} <span class="group-label">{tag_group}</span></h3>
            <ul>
                {"".join(f'<li><a href="{file}">{file_titles.get(file, file)}</a></li>' for file in sorted(files))}
            </ul>
        </div>
        """
    
    # 完整的HTML模板
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标签索引 - 小布的AI知识库</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
        }}
        h1 {{
            font-size: 2rem;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
        }}
        h2 {{
            font-size: 1.4rem;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            padding: 0.5rem 0;
            color: #3498db;
        }}
        h3 {{
            font-size: 1.2rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            color: #2c3e50;
        }}
        .tag-group {{
            margin-bottom: 1.5rem;
        }}
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}
        .tag {{
            display: inline-block;
            padding: 0.3rem 0.6rem;
            background-color: #e1f5fe;
            border-radius: 4px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .tag:hover {{
            background-color: #b3e5fc;
        }}
        .tag.active {{
            background-color: #4fc3f7;
            color: white;
        }}
        small {{
            font-size: 0.8em;
            color: #777;
        }}
        ul {{
            padding-left: 1.5rem;
        }}
        li {{
            margin-bottom: 0.3rem;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .tag-articles {{
            display: none;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background-color: #f0f8ff;
            border-radius: 8px;
        }}
        .group-label {{
            font-size: 0.7rem;
            background-color: #ddd;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            vertical-align: middle;
            color: #666;
        }}
        footer {{
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #eee;
            color: #7f8c8d;
            font-size: 0.9rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>标签索引</h1>
    </header>
    
    <main>
        <p>点击标签查看相关文章。共有 {len(all_tags)} 个标签，分为 {len(tag_groups)} 个分组。</p>
        
        <section id="tag-groups">
            {grouped_tags_html}
        </section>
        
        <section id="articles-by-tag">
            <h2>按标签浏览文章</h2>
            <p id="tag-instruction">请点击上方的标签查看相关文章</p>
            {tag_articles_html}
        </section>
    </main>
    
    <footer>
        <p>© 2025 小布AI. 自动生成于 <script>document.write(new Date().toLocaleDateString())</script></p>
    </footer>
    
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const tags = document.querySelectorAll('.tag');
        const tagArticles = document.querySelectorAll('.tag-articles');
        const tagInstruction = document.getElementById('tag-instruction');
        
        tags.forEach(tag => {{
            tag.addEventListener('click', function() {{
                const tagName = this.getAttribute('data-tag');
                
                // 切换标签活跃状态
                tags.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // 隐藏所有文章列表
                tagArticles.forEach(article => {{
                    article.style.display = 'none';
                }});
                
                // 显示相关文章
                const targetArticle = document.getElementById('tag-' + tagName.replace(' ', '-'));
                if (targetArticle) {{
                    targetArticle.style.display = 'block';
                    tagInstruction.style.display = 'none';
                }}
            }});
        }});
    }});
    </script>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    main() 