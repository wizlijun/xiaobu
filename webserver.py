#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的文件服务器
基于 Python 内置的 http.server 模块，支持文件上传和下载
优化大文件传输性能
"""

import os
import sys
import argparse
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import html
import shutil
import mimetypes
import time

class FileServerHandler(SimpleHTTPRequestHandler):
    # 设置更大的缓冲区大小，提高大文件传输性能
    wbufsize = 1024 * 1024  # 1MB 缓冲区
    
    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        """重写 GET 方法，优化文件下载"""
        path = self.translate_path(self.path)
        
        if os.path.isdir(path):
            # 如果是目录，使用自定义的目录列表
            return super().do_GET()
        elif os.path.isfile(path):
            # 如果是文件，使用优化的文件传输
            return self.send_file_optimized(path)
        else:
            self.send_error(404, "File not found")

    def send_file_optimized(self, path):
        """优化的文件发送方法，支持大文件和断点续传"""
        try:
            # 获取文件信息
            stat = os.stat(path)
            file_size = stat.st_size
            last_modified = time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                                        time.gmtime(stat.st_mtime))
            
            # 获取 MIME 类型
            mime_type, encoding = mimetypes.guess_type(path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            # 处理 Range 请求（断点续传）
            range_header = self.headers.get('Range')
            if range_header:
                return self.handle_range_request(path, file_size, mime_type, range_header)
            
            # 发送完整文件
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(file_size))
            self.send_header('Last-Modified', last_modified)
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Cache-Control', 'public, max-age=3600')
            
            # 对于大文件，建议浏览器下载而不是在线查看
            if file_size > 10 * 1024 * 1024:  # 10MB
                filename = os.path.basename(path)
                self.send_header('Content-Disposition', 
                               f'attachment; filename="{filename}"')
            
            self.end_headers()
            
            # 分块发送文件内容
            self.send_file_content(path, 0, file_size)
            
        except (OSError, IOError) as e:
            print(f"Error sending file {path}: {e}")
            self.send_error(500, "Internal server error")

    def handle_range_request(self, path, file_size, mime_type, range_header):
        """处理 Range 请求，支持断点续传"""
        try:
            # 解析 Range 头
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1
            
            # 验证范围
            if start >= file_size or end >= file_size or start > end:
                self.send_error(416, "Requested Range Not Satisfiable")
                return
            
            content_length = end - start + 1
            
            # 发送 206 Partial Content 响应
            self.send_response(206)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(content_length))
            self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()
            
            # 发送指定范围的文件内容
            self.send_file_content(path, start, content_length)
            
        except (ValueError, OSError, IOError) as e:
            print(f"Error handling range request: {e}")
            self.send_error(400, "Bad Request")

    def send_file_content(self, path, start, length):
        """分块发送文件内容"""
        chunk_size = 64 * 1024  # 64KB 块大小
        
        try:
            with open(path, 'rb') as f:
                f.seek(start)
                remaining = length
                
                while remaining > 0:
                    chunk_size_to_read = min(chunk_size, remaining)
                    chunk = f.read(chunk_size_to_read)
                    
                    if not chunk:
                        break
                    
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()  # 确保数据立即发送
                    except (ConnectionResetError, BrokenPipeError):
                        # 客户端断开连接
                        print("Client disconnected during file transfer")
                        break
                    
                    remaining -= len(chunk)
                    
        except (OSError, IOError) as e:
            print(f"Error reading file {path}: {e}")

    def do_POST(self):
        """处理文件上传"""
        try:
            # 获取当前目录路径
            path = urllib.parse.unquote(self.path)
            if path.startswith('/'):
                path = path[1:]
            
            upload_dir = os.path.join(self.directory, path)
            upload_dir = os.path.abspath(upload_dir)
            
            # 安全检查
            if not upload_dir.startswith(os.path.abspath(self.directory)):
                self.send_error(403, "Access Denied")
                return
            
            if not os.path.isdir(upload_dir):
                self.send_error(404, "Directory Not Found")
                return
            
            # 解析上传的文件
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Invalid Content Type")
                return
            
            # 解析表单数据
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            if 'file' not in form:
                self.send_error(400, "No File Uploaded")
                return
            
            file_item = form['file']
            if not file_item.filename:
                self.send_error(400, "No File Selected")
                return
            
            # 保存文件
            filename = os.path.basename(file_item.filename)
            if not filename:
                self.send_error(400, "Invalid Filename")
                return
            
            file_path = os.path.join(upload_dir, filename)
            
            # 使用更大的缓冲区上传大文件
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file_item.file, f, length=1024*1024)  # 1MB 缓冲区
            
            # 返回成功页面
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            success_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>上传成功</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; }}
                    .success {{ color: green; font-size: 24px; }}
                    .back-link {{ margin-top: 20px; }}
                    a {{ color: #007bff; text-decoration: none; }}
                </style>
            </head>
            <body>
                <div class="success">✅ 文件上传成功！</div>
                <p>文件 "{html.escape(filename)}" 已成功上传</p>
                <div class="back-link">
                    <a href="/{path}">← 返回目录</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode('utf-8'))
            
        except Exception as e:
            print(f"Upload error: {str(e)}")
            self.send_error(500, "Upload Failed")

    def list_directory(self, path):
        """重写目录列表方法，添加上传功能"""
        try:
            list_items = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        list_items.sort(key=lambda a: a.lower())
        
        # 获取相对路径用于显示
        rel_path = os.path.relpath(path, self.directory)
        if rel_path == '.':
            rel_path = ''
        
        display_path = '/' + rel_path if rel_path else '/'
        
        # 生成 HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>文件服务器 - {html.escape(display_path)}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 15px;
                    margin-bottom: 30px;
                }}
                .upload-section {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                .upload-section h3 {{
                    margin-top: 0;
                    color: white;
                }}
                .file-input {{
                    background: white;
                    border: 2px dashed #ccc;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 15px 0;
                }}
                .file-input input[type="file"] {{
                    margin: 10px 0;
                    padding: 8px;
                }}
                .upload-btn {{
                    background: #28a745;
                    color: white;
                    padding: 12px 25px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background 0.3s;
                }}
                .upload-btn:hover {{
                    background: #218838;
                }}
                .file-list {{
                    background: white;
                }}
                .file-list table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                .file-list th, .file-list td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                }}
                .file-list th {{
                    background: #f8f9fa;
                    font-weight: bold;
                    color: #495057;
                }}
                .file-list tr:hover {{
                    background: #f8f9fa;
                }}
                .file-list a {{
                    color: #007bff;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                }}
                .file-list a:hover {{
                    text-decoration: underline;
                }}
                .icon {{
                    margin-right: 8px;
                    font-size: 18px;
                }}
                .parent-link {{
                    margin-bottom: 20px;
                }}
                .parent-link a {{
                    color: #6c757d;
                    text-decoration: none;
                    font-size: 16px;
                }}
                .large-file {{
                    color: #dc3545;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📁 文件服务器 - {html.escape(display_path)}</h1>
        """
        
        # 添加返回上级目录链接
        if rel_path:
            parent_path = os.path.dirname(rel_path)
            parent_url = '/' + parent_path if parent_path else '/'
            html_content += f"""
                <div class="parent-link">
                    <a href="{parent_url}">⬆️ 返回上级目录</a>
                </div>
            """
        
        # 添加上传区域
        current_url = '/' + rel_path if rel_path else '/'
        html_content += f"""
                <div class="upload-section">
                    <h3>📤 上传文件</h3>
                    <form method="post" enctype="multipart/form-data" action="{current_url}">
                        <div class="file-input">
                            <input type="file" name="file" required>
                        </div>
                        <button type="submit" class="upload-btn">上传文件</button>
                    </form>
                </div>
                
                <div class="file-list">
                    <table>
                        <thead>
                            <tr>
                                <th>名称</th>
                                <th>类型</th>
                                <th>大小</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        # 添加文件列表
        for name in list_items:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            
            # 处理特殊字符
            if os.path.islink(fullname):
                displayname = name + "@"
            elif os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                icon = "📁"
                file_type = "目录"
                size = "-"
                size_class = ""
            else:
                icon = "📄"
                file_type = "文件"
                try:
                    file_size = os.path.getsize(fullname)
                    size = self.format_size(file_size)
                    # 标记大文件
                    size_class = "large-file" if file_size > 50 * 1024 * 1024 else ""
                except OSError:
                    size = "未知"
                    size_class = ""
            
            # URL 编码
            linkname = urllib.parse.quote(linkname, errors='surrogatepass')
            
            html_content += f"""
                            <tr>
                                <td>
                                    <a href="{linkname}">
                                        <span class="icon">{icon}</span>
                                        {html.escape(displayname, quote=False)}
                                    </a>
                                </td>
                                <td>{file_type}</td>
                                <td class="{size_class}">{size}</td>
                            </tr>
            """
        
        html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 创建一个类似文件的对象
        import io
        encoded = html_content.encode('utf-8', 'surrogateescape')
        f = io.BytesIO(encoded)
        
        # 发送响应头
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        
        return f

    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def log_message(self, format, *args):
        """自定义日志格式，添加时间戳"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def create_handler(directory):
    """创建处理器工厂函数"""
    def handler(*args, **kwargs):
        return FileServerHandler(*args, directory=directory, **kwargs)
    return handler

def main():
    parser = argparse.ArgumentParser(description='简单的文件服务器，支持上传和下载，优化大文件传输')
    parser.add_argument('directory', help='要共享的目录路径')
    parser.add_argument('-p', '--port', type=int, default=8888, help='服务器端口 (默认: 8888)')
    parser.add_argument('-H', '--host', default='0.0.0.0', help='服务器地址 (默认: 0.0.0.0)')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.exists(args.directory):
        print(f"❌ 错误: 目录 '{args.directory}' 不存在")
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"❌ 错误: '{args.directory}' 不是一个目录")
        sys.exit(1)
    
    # 获取绝对路径
    directory = os.path.abspath(args.directory)
    
    # 创建服务器
    handler = create_handler(directory)
    server = HTTPServer((args.host, args.port), handler)
    
    # 设置服务器超时
    server.timeout = 300  # 5分钟超时
    
    print("🚀 文件服务器启动成功!")
    print(f"📂 共享目录: {directory}")
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"💡 功能: 文件上传、下载、目录浏览")
    print(f"⚡ 优化: 支持大文件传输和断点续传")
    print(f"⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        server.shutdown()

if __name__ == '__main__':
    main() 