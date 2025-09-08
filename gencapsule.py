#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gencapsule.py - 自动生成胶囊化阅读页面

用于将大模型摘要后的交互式阅读页面自动生成为完整的HTML文件，
包含样式、交互功能和元数据信息。

使用方法: 
    python gencapsule.py <name>              # 处理ai目录下的文件
    python gencapsule.py blog/<name>         # 处理ai/blog目录下的文件
    python gencapsule.py <name> <base_dir>   # 自定义基础目录
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
    # 明确处理None值和空列表
    if not links or links is None:
        return ""
    
    html = ['<h3>相关链接</h3>']
    
    # 确保links是列表格式
    if isinstance(links, str):
        links = [links]
    elif not isinstance(links, list):
        # 如果不是字符串也不是列表，跳过处理
        return ""
    
    for link in links:
        if link:  # 跳过空字符串或None项
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


def generate_attachments_html(attachments, name, base_dir=None):
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
            if base_dir:
                actual_file_path = base_dir / file_path
            else:
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


def fix_image_paths(html_content, name):
    """修正HTML中的图片路径
    
    将相对路径的图片引用修正为正确的路径，确保指向name_files目录
    支持的图片格式：jpg, jpeg, png, gif, svg, webp, bmp
    """
    if not html_content:
        return html_content
    
    print(f"修正图片路径，目标目录: {name}_files/")
    
    # 图片文件扩展名模式
    image_extensions = r'\.(jpg|jpeg|png|gif|svg|webp|bmp)'
    
    # 匹配各种图片引用格式的正则表达式
    patterns = [
        # <img src="..." />
        (r'<img\s+[^>]*src\s*=\s*["\']([^"\']*' + image_extensions + r')["\']', 'img_src'),
        # <image src="..." /> (SVG)
        (r'<image\s+[^>]*src\s*=\s*["\']([^"\']*' + image_extensions + r')["\']', 'image_src'),
        # background-image: url(...)
        (r'background-image\s*:\s*url\s*\(\s*["\']?([^"\']*' + image_extensions + r')["\']?\s*\)', 'css_bg'),
        # CSS中的图片引用
        (r'url\s*\(\s*["\']?([^"\']*' + image_extensions + r')["\']?\s*\)', 'css_url'),
    ]
    
    modified_html = html_content
    fixed_count = 0
    
    for pattern, pattern_type in patterns:
        def replace_path(match):
            nonlocal fixed_count
            original_path = match.group(1)
            
            # 跳过绝对URL（http://、https://、//开头）
            if original_path.startswith(('http://', 'https://', '//', 'data:')):
                return match.group(0)
            
            # 跳过已经正确的路径（已经包含name_files/）
            if f"{name}_files/" in original_path:
                return match.group(0)
            
            # 提取文件名（去除相对路径前缀如 ./ 或 ../ ）
            filename = original_path.split('/')[-1]
            
            # 构建新的路径
            new_path = f"{name}_files/{filename}"
            
            # 根据模式类型替换
            if pattern_type in ['img_src', 'image_src']:
                # 替换img或image标签的src属性
                replacement = match.group(0).replace(original_path, new_path)
            else:
                # 替换CSS中的URL
                replacement = match.group(0).replace(original_path, new_path)
            
            print(f"  修正图片路径: {original_path} -> {new_path}")
            fixed_count += 1
            return replacement
        
        modified_html = re.sub(pattern, replace_path, modified_html, flags=re.IGNORECASE)
    
    if fixed_count > 0:
        print(f"共修正 {fixed_count} 个图片路径")
    else:
        print("未发现需要修正的图片路径")
    
    return modified_html, fixed_count


def main():
    """主函数"""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        error_exit("使用方法: python gencapsule.py <name> [base_dir]\n       或: python gencapsule.py blog/<name>")
    
    name = sys.argv[1]
    
    # 检查是否为 blog/name 格式
    if name.startswith('blog/'):
        # 提取实际的 name 部分
        actual_name = name[5:]  # 去掉 "blog/" 前缀
        base_dir = Path('ai/blog')
        print(f"检测到blog格式参数，处理blog目录下的文件: {actual_name}")
    elif len(sys.argv) == 3:
        # 支持自定义基础目录
        actual_name = name
        base_dir = Path(sys.argv[2])
    else:
        # 默认使用'ai'目录或环境变量指定的目录
        actual_name = name
        base_dir_env = os.environ.get('GENCAPSULE_BASE_DIR', 'ai')
        base_dir = Path(base_dir_env)
    
    # 定义路径
    input_dir = base_dir / f"{actual_name}_files"
    output_file = base_dir / f"{actual_name}.html"
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
    
    print(f"开始处理: {actual_name}")
    print(f"基础目录: {base_dir}")
    print(f"输入目录: {input_dir}")
    print(f"输出文件: {output_file}")
    
    # 读取输入文件
    print("读取输入文件...")
    capsule_html = read_file_safe(capsule_html_path, "capsule.html")
    meta_data = parse_yaml_safe(meta_yaml_path)
    css_content = read_file_safe(css_template_path, "CSS模板")
    floatbox_template = read_file_safe(floatbox_template_path, "浮动框模板")
    
    # 修正图片路径（在所有其他处理之前）
    print("修正图片路径...")
    capsule_html, fixed_images_count = fix_image_paths(capsule_html, actual_name)
    
    # 处理元数据
    print("处理元数据...")
    source_html = generate_source_html(meta_data.get('source'))
    links_html = generate_links_html(meta_data.get('links'))
    attachments_html = generate_attachments_html(meta_data.get('attachments'), actual_name, base_dir)
    
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
        toggle_button = '\n<button class="float-toggle" id="float-toggle" title="打开附件面板">◁</button>'
        
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
        toggleBtn.textContent = isExpanded ? '▷' : '◁';
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
            toggleBtn.textContent = '◁';
            toggleBtn.title = '打开附件面板';
            toggleBtn.style.right = '10px'; // 重置按钮位置
        }
    });
    
    // ESC键关闭面板
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && panel.classList.contains('expanded')) {
            panel.classList.remove('expanded');
            toggleBtn.textContent = '◁';
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
        
        # 安全获取links数量，处理None值
        links = meta_data.get('links') or []
        print(f"- 相关链接: {len(links)} 个")
        
        # 安全获取attachments数量，处理None值
        attachments = meta_data.get('attachments') or []
        print(f"- 附件数量: {len(attachments)} 个")
        
        print(f"- 修正图片路径: {fixed_images_count} 个")
        
    except Exception as e:
        error_exit(f"写入输出文件时发生错误: {e}")


if __name__ == "__main__":
    main() 