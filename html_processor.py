#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox

def process_html_file(file_path):
    if not file_path.lower().endswith('.html'):
        messagebox.showerror("错误", "只能处理HTML文件！")
        return
    
    # 创建主窗口但不显示
    root = tk.Tk()
    root.withdraw()
    
    # 获取原始文件名（不含路径和扩展名）
    original_filename = os.path.basename(file_path)
    original_name = os.path.splitext(original_filename)[0]
    
    # 显示输入对话框
    new_name = simpledialog.askstring("文件名", "请输入新的文件名（不含扩展名）:", initialvalue=original_name)
    
    # 如果用户取消，则退出
    if new_name is None:
        root.destroy()
        return
    
    # 如果用户输入为空，显示错误
    if not new_name.strip():
        messagebox.showerror("错误", "文件名不能为空！")
        root.destroy()
        return
    
    try:
        # 构建新的文件名和路径
        new_filename = new_name.strip() + ".html"
        destination_dir = "/Users/bruce/git/xiaobu/ai"
        destination_path = os.path.join(destination_dir, new_filename)
        
        # 确保目标目录存在
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # 复制文件到目标目录
        shutil.copy2(file_path, destination_path)
        
        # 切换到项目目录并运行push.sh
        os.chdir("/Users/bruce/git/xiaobu")
        result = subprocess.run(["./push.sh"], capture_output=True, text=True)
        
        if result.returncode == 0:
            messagebox.showinfo("成功", f"文件已成功复制到 {destination_path} 并执行了提交。")
        else:
            messagebox.showerror("错误", f"执行push.sh时出错：\n{result.stderr}")
    
    except Exception as e:
        messagebox.showerror("错误", f"处理过程中出错：\n{str(e)}")
    
    root.destroy()

if __name__ == "__main__":
    # 判断是否有足够的参数
    if len(sys.argv) < 2:
        print("使用方法: html_processor.py <html文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    process_html_file(file_path)