#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QFont, QIcon

class ShareHtmlApp(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.settings = QSettings("XiaoBu", "ShareHTML")
        self.initUI()
        if file_path and os.path.exists(file_path):
            self.file_path_input.setText(file_path)
            self.update_share_filename()

    def initUI(self):
        self.setWindowTitle("快捷分享HTML")
        self.setGeometry(300, 300, 700, 500)
        
        # 主窗口布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 1. 待分享文件输入框
        file_layout = QHBoxLayout()
        file_label = QLabel("待分享文件：")
        self.file_path_input = QLineEdit()
        self.file_path_input.textChanged.connect(self.update_share_filename)
        select_file_btn = QPushButton("选择文件")
        select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(select_file_btn)
        main_layout.addLayout(file_layout)
        
        # 2. 本地Git仓库路径
        git_layout = QHBoxLayout()
        git_label = QLabel("本地Git仓库路径：")
        self.git_path_input = QLineEdit()
        self.git_path_input.setText(self.settings.value("git_path", os.path.expanduser("~/git/xiaobu/ai")))
        self.git_path_input.textChanged.connect(lambda: self.settings.setValue("git_path", self.git_path_input.text()))
        select_git_btn = QPushButton("选择目录")
        select_git_btn.clicked.connect(self.select_git_path)
        git_layout.addWidget(git_label)
        git_layout.addWidget(self.git_path_input)
        git_layout.addWidget(select_git_btn)
        main_layout.addLayout(git_layout)
        
        # 3. 分享后文件名
        filename_layout = QHBoxLayout()
        filename_label = QLabel("分享后文件名：")
        self.share_filename_input = QLineEdit()
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.share_filename_input)
        main_layout.addLayout(filename_layout)
        
        # 4. 分享脚本路径
        script_layout = QHBoxLayout()
        script_label = QLabel("分享脚本路径：")
        self.script_path_input = QLineEdit()
        self.script_path_input.setText(self.settings.value("script_path", os.path.expanduser("~/git/xiaobu/push.sh")))
        self.script_path_input.textChanged.connect(lambda: self.settings.setValue("script_path", self.script_path_input.text()))
        select_script_btn = QPushButton("选择脚本")
        select_script_btn.clicked.connect(self.select_script_path)
        script_layout.addWidget(script_label)
        script_layout.addWidget(self.script_path_input)
        script_layout.addWidget(select_script_btn)
        main_layout.addLayout(script_layout)
        
        # 5. 网站地址
        website_layout = QHBoxLayout()
        website_label = QLabel("网站地址：")
        self.website_input = QLineEdit()
        self.website_input.setText(self.settings.value("website", "https://www.xiaobu.net/ai/"))
        self.website_input.textChanged.connect(lambda: self.settings.setValue("website", self.website_input.text()))
        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_input)
        main_layout.addLayout(website_layout)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        self.copy_link_btn = QPushButton("复制分享链接")
        self.copy_link_btn.clicked.connect(self.copy_share_link)
        self.share_btn = QPushButton("分享")
        self.share_btn.clicked.connect(self.share_file)
        btn_layout.addWidget(self.copy_link_btn)
        btn_layout.addWidget(self.share_btn)
        main_layout.addLayout(btn_layout)
        
        # 日志区域
        log_label = QLabel("执行日志：")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_text)
        
        # 状态栏
        self.statusBar().showMessage("就绪")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择HTML文件", "", "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.file_path_input.setText(file_path)
            self.update_share_filename()
    
    def select_git_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择本地Git仓库目录")
        if dir_path:
            self.git_path_input.setText(dir_path)
            self.settings.setValue("git_path", dir_path)
    
    def select_script_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择分享脚本", "", "Shell Scripts (*.sh);;All Files (*)"
        )
        if file_path:
            self.script_path_input.setText(file_path)
            self.settings.setValue("script_path", file_path)
    
    def update_share_filename(self):
        file_path = self.file_path_input.text()
        if file_path:
            filename = os.path.basename(file_path)
            self.share_filename_input.setText(filename)
            # 选中文件名部分，不包括扩展名
            basename, ext = os.path.splitext(filename)
            self.share_filename_input.setFocus()
            self.share_filename_input.setSelection(0, len(basename))
    
    def copy_share_link(self):
        filename = self.share_filename_input.text()
        if not filename:
            QMessageBox.warning(self, "警告", "请先指定分享后的文件名！")
            return
        
        website = self.website_input.text()
        if not website.endswith("/"):
            website += "/"
        
        full_url = website + filename
        clipboard = QApplication.clipboard()
        clipboard.setText(full_url)
        self.statusBar().showMessage(f"已复制链接: {full_url}", 3000)
        self.log_text.append(f"已复制链接: {full_url}")
    
    def share_file(self):
        # 检查输入
        source_file = self.file_path_input.text()
        git_path = self.git_path_input.text()
        share_filename = self.share_filename_input.text()
        script_path = self.script_path_input.text()
        
        if not os.path.exists(source_file):
            QMessageBox.critical(self, "错误", "待分享文件不存在！")
            return
        
        if not os.path.exists(git_path):
            QMessageBox.critical(self, "错误", "本地Git仓库路径不存在！")
            return
        
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "错误", "分享脚本不存在！")
            return
        
        if not share_filename:
            QMessageBox.critical(self, "错误", "请指定分享后的文件名！")
            return
        
        # 执行分享流程
        self.log_text.clear()
        self.log_text.append("开始分享文件...")
        
        try:
            # 1. 复制文件到Git仓库
            target_path = os.path.join(git_path, share_filename)
            self.log_text.append(f"正在复制文件到 {target_path}")
            shutil.copy2(source_file, target_path)
            
            # 2. 执行分享脚本
            self.log_text.append(f"正在执行分享脚本 {script_path}")
            process = subprocess.Popen(
                [script_path], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(script_path)
            )
            stdout, stderr = process.communicate()
            
            if stdout:
                self.log_text.append("脚本输出：")
                self.log_text.append(stdout)
            
            if stderr:
                self.log_text.append("错误输出：")
                self.log_text.append(stderr)
            
            if process.returncode == 0:
                self.log_text.append("分享成功！")
                self.statusBar().showMessage("分享成功！", 3000)
                # 自动复制分享链接
                self.copy_share_link()
            else:
                self.log_text.append(f"分享脚本执行失败，返回码: {process.returncode}")
                self.statusBar().showMessage("分享失败！", 3000)
        
        except Exception as e:
            self.log_text.append(f"发生错误: {str(e)}")
            self.statusBar().showMessage("分享失败！", 3000)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion风格，在macOS上看起来更原生
    
    # 检查命令行参数，如果有传入文件路径则使用
    file_path = None
    if len(sys.argv) > 1:
        potential_path = sys.argv[1]
        if os.path.exists(potential_path) and potential_path.lower().endswith(('.html', '.htm')):
            file_path = potential_path
    
    window = ShareHtmlApp(file_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 