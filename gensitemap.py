#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成 sitemap.xml 工具
根据 ai/index.html 中的所有链接生成网站地图
"""

import os
import re
import argparse
from urllib.parse import urlparse, urljoin
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    """自定义HTML解析器，提取链接"""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_tag = None
        self.current_attrs = None
        self.current_text = ""
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        self.current_text = ""
        
    def handle_endtag(self, tag):
        if tag == 'a' and self.current_attrs and 'href' in self.current_attrs:
            href = self.current_attrs['href']
            text = self.current_text.strip()
            if href.startswith('http'):
                self.links.append({
                    'url': href,
                    'text': text,
                    'tag': None  # 保持兼容性
                })
        self.current_tag = None
        self.current_attrs = None
        self.current_text = ""
        
    def handle_data(self, data):
        if self.current_tag == 'a':
            self.current_text += data


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
    """从文本中提取日期信息"""
    # 匹配格式：（2025-07-21 14:33）
    date_pattern = r'（(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}）'
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)
    return None


def get_priority_by_tag(url, text):
    """根据标签和内容确定优先级"""
    # 默认优先级
    priority = 0.5
    
    # 博客文章优先级更高
    if '[blog]' in text:
        priority = 0.9
    elif '[ai]' in text:
        priority = 0.8
    elif '[bushcraft]' in text or '[mind]' in text:
        priority = 0.7
    elif '[se]' in text:
        priority = 0.6
    
    return priority


def get_change_frequency(url, text):
    """根据内容类型确定更新频率"""
    if '[blog]' in text:
        return 'weekly'
    elif 'index.html' in url or 'tags.html' in url:
        return 'daily'
    else:
        return 'monthly'


def generate_sitemap(links, base_url="https://www.xiaobu.net"):
    """生成 sitemap.xml"""
    print("正在生成 sitemap.xml...")
    
    # 创建根元素
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # 添加首页
    url_elem = SubElement(urlset, 'url')
    SubElement(url_elem, 'loc').text = base_url
    SubElement(url_elem, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    SubElement(url_elem, 'changefreq').text = 'daily'
    SubElement(url_elem, 'priority').text = '1.0'
    
    # 添加 ai/index.html
    url_elem = SubElement(urlset, 'url')
    SubElement(url_elem, 'loc').text = f"{base_url}/ai/index.html"
    SubElement(url_elem, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    SubElement(url_elem, 'changefreq').text = 'daily'
    SubElement(url_elem, 'priority').text = '0.9'
    
    # 处理所有链接
    processed_urls = set()  # 去重
    
    for link in links:
        url = link['url']
        text = link['text']
        
        # 去重处理
        if url in processed_urls:
            continue
        processed_urls.add(url)
        
        # 创建 URL 元素
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = url
        
        # 尝试从文本中提取日期
        date_str = extract_date_from_text(text)
        if date_str:
            SubElement(url_elem, 'lastmod').text = date_str
        else:
            # 使用当前日期
            SubElement(url_elem, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
        
        # 设置更新频率
        changefreq = get_change_frequency(url, text)
        SubElement(url_elem, 'changefreq').text = changefreq
        
        # 设置优先级
        priority = get_priority_by_tag(url, text)
        SubElement(url_elem, 'priority').text = str(priority)
    
    return urlset


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
    
    return "https://www.xiaobu.net"  # 默认域名


def replace_domain_in_links(links, new_base_url):
    """将链接中的域名替换为新的基础URL域名"""
    new_parsed = urlparse(new_base_url)
    new_netloc = new_parsed.netloc
    new_scheme = new_parsed.scheme
    
    replaced_links = []
    for link in links:
        old_url = link['url']
        old_parsed = urlparse(old_url)
        
        # 构建新的URL（保持路径和查询参数）
        new_url = f"{new_scheme}://{new_netloc}{old_parsed.path}"
        if old_parsed.query:
            new_url += f"?{old_parsed.query}"
        if old_parsed.fragment:
            new_url += f"#{old_parsed.fragment}"
        
        # 创建新的链接对象
        new_link = link.copy()
        new_link['url'] = new_url
        replaced_links.append(new_link)
    
    return replaced_links


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成网站地图 sitemap.xml')
    parser.add_argument('-u', '--url', '--base-url', 
                      help='指定基础URL (例如: https://www.xiaobu.net)')
    parser.add_argument('-i', '--input', default='ai/index.html',
                      help='输入HTML文件路径 (默认: ai/index.html)')
    parser.add_argument('-o', '--output', default='sitemap.xml',
                      help='输出XML文件路径 (默认: sitemap.xml)')
    parser.add_argument('--auto-detect', action='store_true',
                      help='自动检测基础URL（从HTML文件中的链接）')
    parser.add_argument('--replace-domain', action='store_true',
                      help='替换链接中的域名为指定的基础URL域名（而不是过滤链接）')
    
    args = parser.parse_args()
    
    print("=== 网站地图生成器 ===")
    
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
        
        # 确定基础URL和处理链接
        if args.url:
            base_url = args.url.rstrip('/')  # 移除末尾的斜杠
            print(f"🌐 使用指定的基础URL: {base_url}")
            
            if args.replace_domain:
                # 替换所有链接的域名
                links = replace_domain_in_links(all_links, base_url)
                print(f"🔄 已将 {len(links)} 个链接的域名替换为: {urlparse(base_url).netloc}")
            else:
                # 过滤出匹配指定域名的链接
                parsed_base = urlparse(base_url)
                domain_to_filter = parsed_base.netloc
                links = [link for link in all_links if domain_to_filter in link['url']]
                print(f"🔍 过滤后找到 {len(links)} 个匹配域名的链接")
                
                # 检查过滤后是否还有链接
                if not links:
                    print(f"⚠️  警告: 没有找到匹配域名 '{parsed_base.netloc}' 的链接")
                    print(f"📋 所有找到的域名:")
                    domains = set()
                    for link in all_links:
                        parsed = urlparse(link['url'])
                        domains.add(parsed.netloc)
                    for domain in sorted(domains):
                        print(f"  - {domain}")
                    print(f"💡 提示: 使用 --replace-domain 参数可以替换域名而不是过滤")
                    return
        else:
            # 自动检测域名
            base_url = auto_detect_base_url(all_links)
            print(f"🔍 自动检测到基础URL: {base_url}")
            print("💡 提示: 可以使用 -u 参数指定自定义域名")
            # 使用检测到的域名，不进行过滤
            links = all_links
        
        # 生成 sitemap
        sitemap = generate_sitemap(links, base_url)
        
        # 格式化并保存 XML
        xml_content = format_xml(sitemap)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 成功生成 {args.output}")
        print(f"📊 包含 {len(links) + 2} 个 URL（包括首页和索引页）")
        
        # 显示一些统计信息
        print(f"🏠 基础域名: {base_url}")
        print("\n📈 链接统计:")
        tag_counts = {}
        for link in links:
            text = link['text']
            # 提取标签
            tags = re.findall(r'\[([^\]]+)\]', text)
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  [{tag}]: {count} 篇")
            
        # 显示使用示例
        print(f"\n💡 多域名使用示例:")
        print(f"  # 过滤现有域名的链接：")
        print(f"  python3 gensitemap.py -u https://www.laobu.net")
        print(f"  # 替换为新域名：")
        print(f"  python3 gensitemap.py -u https://blog.laobu.net --replace-domain -o sitemap-blog.xml")
        print(f"  python3 gensitemap.py -u https://docs.laobu.net --replace-domain -o sitemap-docs.xml")  
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main() 