#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成 RSS feed 工具
根据 ai/index.html 中最近30天的链接生成 RSS feed
保存为 feed.xml
"""

import os
import re
import argparse
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    """自定义HTML解析器，提取链接和完整的<li>内容"""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_tag = None
        self.current_attrs = None
        self.current_text = ""
        self.li_content = ""
        self.in_li = False
        self.current_href = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.in_li = True
            self.li_content = ""
            self.current_href = None
        elif tag == 'a' and self.in_li:
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                self.current_href = attrs_dict['href']
        
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        self.current_text = ""
        
    def handle_endtag(self, tag):
        if tag == 'li' and self.in_li:
            if self.current_href and self.current_href.startswith('http'):
                self.links.append({
                    'url': self.current_href,
                    'text': self.li_content.strip(),
                    'tag': None
                })
            self.in_li = False
            self.li_content = ""
            self.current_href = None
        
        self.current_tag = None
        self.current_attrs = None
        self.current_text = ""
        
    def handle_data(self, data):
        if self.in_li:
            self.li_content += data


def parse_html_file(file_path, domain_filter=None):
    """解析 HTML 文件，提取所有链接"""
    print(f"正在解析文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用自定义解析器
    parser = LinkExtractor()
    parser.feed(content)
    
    # 过滤链接
    links = []
    for link in parser.links:
        href = link['url']
        # 如果指定了域名过滤器，只处理匹配的域名
        if domain_filter:
            if domain_filter in href:
                links.append(link)
        else:
            # 不过滤，处理所有HTTP链接
            links.append(link)
    
    print(f"找到 {len(links)} 个有效链接")
    return links


def extract_date_from_text(text):
    """从文本中提取日期信息，返回 datetime 对象"""
    # 匹配格式：（2025-07-21 14:33）使用中文全角括号
    date_pattern = r'（(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})）'
    match = re.search(date_pattern, text)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        try:
            return datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        except ValueError:
            return None
    return None


def filter_recent_links(links, days=30):
    """过滤最近指定天数的链接"""
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_links = []
    
    for link in links:
        date_obj = extract_date_from_text(link['text'])
        if date_obj and date_obj >= cutoff_date:
            link['date'] = date_obj
            recent_links.append(link)
    
    # 按日期排序，最新的在前面
    recent_links.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"找到最近 {days} 天内的 {len(recent_links)} 个链接")
    return recent_links


def filter_links_by_tag(links, tag):
    """按标签过滤链接"""
    if not tag:
        return links
    
    filtered_links = []
    for link in links:
        categories = extract_categories_from_text(link['text'])
        if tag.lower() in [cat.lower() for cat in categories]:
            filtered_links.append(link)
    
    print(f"按标签 '{tag}' 过滤后找到 {len(filtered_links)} 个链接")
    return filtered_links


def extract_title_from_text(text):
    """从文本中提取标题，去掉日期和标签"""
    # 去掉日期部分：（2025-07-21 14:33）
    text = re.sub(r'（\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}）', '', text)
    # 去掉开头的标签：[ai][blog]
    text = re.sub(r'^\[[^\]]+\]', '', text)
    # 去掉多个连续的标签
    text = re.sub(r'^\[[^\]]+\]\[[^\]]+\]', '', text)
    text = re.sub(r'^\[[^\]]+\]\[[^\]]+\]\[[^\]]+\]', '', text)
    return text.strip()


def extract_categories_from_text(text):
    """从文本中提取分类标签"""
    categories = re.findall(r'\[([^\]]+)\]', text)
    return categories


def generate_rss(links, base_url="https://www.laobu.com", site_title="老布的AI知识库", site_description="记录AI相关的学习和思考"):
    """生成 RSS feed XML"""
    print("正在生成 RSS feed...")
    
    # 创建根元素
    rss = Element('rss')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')
    rss.set('version', '2.0')
    
    # 创建 channel 元素
    channel = SubElement(rss, 'channel')
    
    # 基本信息
    SubElement(channel, 'title').text = site_title
    SubElement(channel, 'link').text = base_url + '/ai/index.html'
    SubElement(channel, 'description').text = site_description
    SubElement(channel, 'language').text = 'zh-CN'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    SubElement(channel, 'generator').text = 'genrss.py'
    
    # 添加 atom:link
    atom_link = SubElement(channel, 'atom:link')
    atom_link.set('href', f'{base_url}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # 添加文章项目
    for link in links:
        item = SubElement(channel, 'item')
        
        # 标题
        title = extract_title_from_text(link['text'])
        SubElement(item, 'title').text = title
        
        # 链接
        SubElement(item, 'link').text = link['url']
        SubElement(item, 'guid').text = link['url']
        
        # 描述 - 使用完整文本作为描述
        SubElement(item, 'description').text = link['text']
        
        # 发布日期
        if 'date' in link:
            # RSS 日期格式：Wed, 02 Oct 2002 15:00:00 +0000
            pub_date = link['date'].strftime('%a, %d %b %Y %H:%M:%S +0000')
            SubElement(item, 'pubDate').text = pub_date
        
        # 分类
        categories = extract_categories_from_text(link['text'])
        for category in categories:
            cat_elem = SubElement(item, 'category')
            cat_elem.text = category
    
    return rss


def format_xml(element):
    """格式化 XML 输出"""
    rough_string = tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')


def auto_detect_base_url(links):
    """从链接中自动检测基础域名"""
    domain_counts = {}
    
    for link in links:
        url = link['url']
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    if domain_counts:
        # 返回出现次数最多的域名
        most_common_domain = max(domain_counts.items(), key=lambda x: x[1])[0]
        return most_common_domain
    
    return "https://www.laobu.com"  # 默认域名


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成 RSS feed')
    parser.add_argument('-u', '--url', '--base-url', 
                      help='指定基础URL (例如: https://www.laobu.com)')
    parser.add_argument('-i', '--input', default='ai/index.html',
                      help='输入HTML文件路径 (默认: ai/index.html)')
    parser.add_argument('-o', '--output', default='feed.xml',
                      help='输出RSS文件路径 (默认: feed.xml)')
    parser.add_argument('-d', '--days', type=int, default=30,
                      help='包含最近多少天的文章 (默认: 30)')
    parser.add_argument('-t', '--tag',
                      help='按标签过滤文章，例如 -t ai 或 -t bushcraft')
    parser.add_argument('--title', default='老布的AI知识库',
                      help='RSS feed 标题')
    parser.add_argument('--description', default='记录AI相关的学习和思考',
                      help='RSS feed 描述')
    
    args = parser.parse_args()
    
    # 如果指定了标签但没有指定输出文件，自动设置输出文件名
    if args.tag and args.output == 'feed.xml':
        args.output = f'feed-{args.tag}.xml'
    
    print("=== RSS Feed 生成器 ===")
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 找不到文件 {args.input}")
        return
    
    try:
        # 解析 HTML 文件
        all_links = parse_html_file(args.input)
        
        if not all_links:
            print("警告: 没有找到任何有效链接")
            return
        
        # 确定基础URL
        if args.url:
            base_url = args.url.rstrip('/')
            print(f"🌐 使用指定的基础URL: {base_url}")
        else:
            base_url = auto_detect_base_url(all_links)
            print(f"🔍 自动检测到基础URL: {base_url}")
        
        # 过滤最近的链接
        recent_links = filter_recent_links(all_links, args.days)
        
        if not recent_links:
            print(f"⚠️  警告: 没有找到最近 {args.days} 天内的链接")
            return
        
        # 按标签过滤链接
        if args.tag:
            recent_links = filter_links_by_tag(recent_links, args.tag)
            if not recent_links:
                print(f"⚠️  警告: 没有找到标签为 '{args.tag}' 的链接")
                return
        
        # 生成 RSS feed
        rss = generate_rss(recent_links, base_url, args.title, args.description)
        
        # 格式化并保存 XML
        xml_content = format_xml(rss)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 成功生成 {args.output}")
        print(f"📊 包含最近 {args.days} 天内的 {len(recent_links)} 篇文章")
        
        # 显示一些统计信息
        print(f"🏠 基础域名: {base_url}")
        print(f"📅 时间范围: {recent_links[-1]['date'].strftime('%Y-%m-%d')} 到 {recent_links[0]['date'].strftime('%Y-%m-%d')}")
        
        print("\n📈 分类统计:")
        tag_counts = {}
        for link in recent_links:
            categories = extract_categories_from_text(link['text'])
            for category in categories:
                tag_counts[category] = tag_counts.get(category, 0) + 1
        
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  [{tag}]: {count} 篇")
        
        print(f"\n💡 使用示例:")
        print(f"  # 生成最近7天的RSS:")
        print(f"  python3 genrss.py -d 7 -o feed-weekly.xml")
        print(f"  # 自定义标题和描述:")
        print(f"  python3 genrss.py -t '老布AI博客' --description 'AI学习笔记与思考'")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()