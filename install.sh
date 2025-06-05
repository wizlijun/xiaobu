#!/bin/bash

# 快捷分享HTML应用安装脚本
echo "正在安装快捷分享HTML应用..."

# 检查应用是否存在
if [ ! -d "dist/快捷分享HTML.app" ]; then
    echo "错误：未找到应用文件。请先运行打包命令。"
    exit 1
fi

# 复制应用到Applications文件夹
echo "正在复制应用到/Applications..."
sudo cp -R "dist/快捷分享HTML.app" "/Applications/"

# 验证安装
if [ -d "/Applications/快捷分享HTML.app" ]; then
    echo "✅ 应用安装成功！"
    echo "📱 你现在可以在启动台或Applications文件夹中找到"快捷分享HTML"应用。"
    echo "🔗 应用支持HTML文件的右键菜单"打开方式"。"
    
    # 询问是否立即启动
    read -p "是否立即启动应用？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "/Applications/快捷分享HTML.app"
    fi
else
    echo "❌ 安装失败。请检查权限并重试。"
    exit 1
fi 