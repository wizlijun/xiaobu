#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gencapsule.py - 自动生成胶囊化阅读页面

用于将大模型摘要后的交互式阅读页面自动生成为完整的HTML文件，
包含样式、交互功能和元数据信息。

使用方法: python gencapsule.py <name>
"""

import sys
import os
import yaml
import re
from pathlib import Path


def error_exit(message):
    """输出错误信息并退出程序"""
    print(f"错误: {message}", file=sys.stderr)
    sys.exit(1)


def parse_link_format(text):
    """解析 (标题)[链接] 格式的文本"""
    if not text:
        return None, None
    
    # 匹配 (标题)[链接] 格式
    match = re.match(r'\(([^)]+)\)\[([^\]]+)\]', text.strip())
    if match:
        return match.group(1), match.group(2)
    return text, text


def generate_source_html(source):
    """生成原文链接的HTML"""
    if not source:
        return ""
    
    title, url = parse_link_format(source)
    if title and url:
        return f'<h3>原文</h3>\n    <a href="{url}" target="_blank">{title}</a>'
    return ""


def generate_links_html(links):
    """生成相关链接的HTML"""
    if not links:
        return ""
    
    html = ['<h3>相关链接</h3>']
    
    if isinstance(links, str):
        links = [links]
    
    for link in links:
        title, url = parse_link_format(link)
        if title and url:
            html.append(f'    <a href="{url}" target="_blank">{title}</a><br>')
    
    return '\n    '.join(html)


def format_file_size(size_bytes):
    """格式化文件大小为G、M、K形式"""
    if size_bytes == 0:
        return "0B"
    
    # 定义单位
    units = ['B', 'K', 'M', 'G', 'T']
    unit_index = 0
    size = float(size_bytes)
    
    # 转换到合适的单位
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    # 格式化输出
    if unit_index == 0:  # 字节
        return f"{int(size)}B"
    else:
        return f"{size:.1f}{units[unit_index]}"


def get_file_size_info(file_path):
    """获取文件大小信息"""
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return format_file_size(size_bytes)
        else:
            return "文件不存在"
    except Exception:
        return "未知大小"


def generate_attachments_html(attachments, name):
    """生成附件列表的HTML"""
    if not attachments:
        return ""
    
    html = ['<h3>附件</h3>']
    
    if isinstance(attachments, str):
        attachments = [attachments]
    
    for attachment in attachments:
        title, filename = parse_link_format(attachment)
        if title and filename:
            # 附件文件路径相对于_files目录
            file_path = f"{name}_files/{filename}"
            # 获取实际文件路径用于大小检测
            actual_file_path = Path('ai') / file_path
            file_size = get_file_size_info(actual_file_path)
            
            html.append(f'    <div class="attachment-item">')
            html.append(f'        <h4>{title} <span class="file-size">({file_size})</span></h4>')
            html.append(f'        <a href="{file_path}" class="download-btn" download>下载</a>')
            html.append(f'    </div>')
    
    return '\n    '.join(html)


def read_file_safe(file_path, description):
    """安全读取文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        error_exit(f"{description} 不存在: {file_path}")
    except UnicodeDecodeError:
        error_exit(f"{description} 编码错误: {file_path}")
    except Exception as e:
        error_exit(f"读取 {description} 时发生错误: {e}")


def parse_yaml_safe(file_path):
    """安全解析YAML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        error_exit(f"meta.yaml 文件不存在: {file_path}")
    except yaml.YAMLError as e:
        error_exit(f"YAML 解析错误: {e}")
    except Exception as e:
        error_exit(f"读取 meta.yaml 时发生错误: {e}")


def inject_styles(html_content, css_content):
    """在HTML中注入样式"""
    # 查找 </style> 标签并在其前面插入CSS
    if '</style>' not in html_content:
        error_exit("在HTML文件中找不到 </style> 标签")
    
    return html_content.replace('</style>', css_content + '\n    </style>')


def inject_floatbox(html_content, floatbox_content):
    """在HTML中注入浮动框内容"""
    # 查找 </body> 标签并在其前面插入浮动框
    if '</body>' not in html_content:
        error_exit("在HTML文件中找不到 </body> 标签")
    
    return html_content.replace('</body>', f'\n{floatbox_content}\n</body>')


def main():
    """主函数"""
    if len(sys.argv) != 2:
        error_exit("使用方法: python gencapsule.py <name>")
    
    name = sys.argv[1]
    
    # 定义路径
    base_dir = Path('ai')
    input_dir = base_dir / f"{name}_files"
    output_file = base_dir / f"{name}.html"
    template_dir = Path('template')
    
    capsule_html_path = input_dir / "capsule.html"
    meta_yaml_path = input_dir / "meta.yaml"
    css_template_path = template_dir / "capsule.css.html"
    floatbox_template_path = template_dir / "capsule.floatbox.html"
    
    # 检查输入目录是否存在
    if not input_dir.exists():
        error_exit(f"输入目录不存在: {input_dir}")
    
    # 检查模板目录是否存在
    if not template_dir.exists():
        error_exit(f"模板目录不存在: {template_dir}")
    
    print(f"开始处理: {name}")
    print(f"输入目录: {input_dir}")
    print(f"输出文件: {output_file}")
    
    # 读取输入文件
    print("读取输入文件...")
    capsule_html = read_file_safe(capsule_html_path, "capsule.html")
    meta_data = parse_yaml_safe(meta_yaml_path)
    css_content = read_file_safe(css_template_path, "CSS模板")
    floatbox_template = read_file_safe(floatbox_template_path, "浮动框模板")
    
    # 处理元数据
    print("处理元数据...")
    source_html = generate_source_html(meta_data.get('source'))
    links_html = generate_links_html(meta_data.get('links'))
    attachments_html = generate_attachments_html(meta_data.get('attachments'), name)
    
    # 检查是否有任何内容需要显示在浮动框中
    has_floatbox_content = bool(source_html or links_html or attachments_html)
    
    # 注入样式
    print("注入样式...")
    html_with_styles = inject_styles(capsule_html, css_content)
    
    if has_floatbox_content:
        print("生成浮动框内容...")
        # 构建浮动框内容
        floatbox_content = '<div class="attachments-panel" id="attachments-panel">'
        
        if source_html:
            floatbox_content += f'\n    {source_html}'
        
        if links_html:
            floatbox_content += f'\n    {links_html}'
        
        if attachments_html:
            floatbox_content += f'\n    {attachments_html}'
        
        floatbox_content += '\n</div>'
        
        # 添加切换按钮和JavaScript代码
        toggle_button = '\n<button class="float-toggle" id="float-toggle" title="打开附件面板">⬅</button>'
        
        javascript_code = """
<script>
// 浮动框展开/收起功能
document.addEventListener('DOMContentLoaded', function() {
    const panel = document.getElementById('attachments-panel');
    const toggleBtn = document.getElementById('float-toggle');
    
    if (!panel || !toggleBtn) return;
    
    // 切换面板显示状态
    function togglePanel() {
        panel.classList.toggle('expanded');
        // 更新按钮图标
        const isExpanded = panel.classList.contains('expanded');
        toggleBtn.textContent = isExpanded ? '➡' : '⬅';
        toggleBtn.title = isExpanded ? '关闭附件面板' : '打开附件面板';
        
        // 动态调整按钮位置
        if (isExpanded) {
            // 等待面板展开动画完成后调整按钮位置
            setTimeout(() => {
                const panelWidth = panel.offsetWidth;
                toggleBtn.style.right = (panelWidth + 30) + 'px';
            }, 300);
        } else {
            toggleBtn.style.right = '10px';
        }
    }
    
    // 点击切换按钮
    toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        togglePanel();
    });
    
    // 点击页面其他地方时收起面板
    document.addEventListener('click', function(e) {
        const isClickOnPanel = panel.contains(e.target);
        const isClickOnToggle = toggleBtn.contains(e.target);
        
        if (!isClickOnPanel && !isClickOnToggle) {
            panel.classList.remove('expanded');
            toggleBtn.textContent = '⬅';
            toggleBtn.title = '打开附件面板';
            toggleBtn.style.right = '10px'; // 重置按钮位置
        }
    });
    
    // ESC键关闭面板
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && panel.classList.contains('expanded')) {
            panel.classList.remove('expanded');
            toggleBtn.textContent = '⬅';
            toggleBtn.title = '打开附件面板';
            toggleBtn.style.right = '10px'; // 重置按钮位置
        }
    });
});
</script>"""
        
        floatbox_content += toggle_button
        floatbox_content += javascript_code
        
        # 注入浮动框内容
        print("注入浮动框内容...")
        final_html = inject_floatbox(html_with_styles, floatbox_content)
    else:
        print("无浮动框内容，跳过浮动框生成...")
        final_html = html_with_styles
    
    # 写入输出文件
    print("写入输出文件...")
    try:
        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"成功生成: {output_file}")
        
        # 输出统计信息
        print(f"\n统计信息:")
        print(f"- 原文链接: {'有' if meta_data.get('source') else '无'}")
        print(f"- 相关链接: {len(meta_data.get('links', []))} 个")
        print(f"- 附件数量: {len(meta_data.get('attachments', []))} 个")
        
    except Exception as e:
        error_exit(f"写入输出文件时发生错误: {e}")


if __name__ == "__main__":
    main() 