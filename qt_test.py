#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QLibraryInfo, QCoreApplication

def main():
    # 设置Qt插件路径
    plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
    if os.path.exists(plugin_path):
        print(f"添加插件路径: {plugin_path}")
        QCoreApplication.addLibraryPath(plugin_path)
    
    # 打印Qt的库路径
    print("Qt库路径:")
    for path in QCoreApplication.libraryPaths():
        print(f"  - {path}")
    
    print(f"Qt插件路径: {QLibraryInfo.location(QLibraryInfo.PluginsPath)}")
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Qt测试")
    window.resize(300, 200)
    
    label = QLabel("Qt测试成功!", window)
    label.move(100, 80)
    
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main()) 