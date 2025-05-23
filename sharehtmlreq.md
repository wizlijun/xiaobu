# 快捷分享 HTML 应用需求说明

一、基本信息
	•	应用名称：sharehtml.app
	•	应用中文名：快捷分享 HTML
	•	开发语言：Python
	•	运行平台：macOS（GUI 应用）
	•	源文件名：sharehtml.py

⸻

二、功能需求

1. 文件关联与启动方式
	•	支持在 Finder 中右键以“打开方式”选择 sharehtml.app 打开 .html 或 .htm 文件；
	•	被打开的文件路径作为参数传入应用主界面，用作默认“待分享文件”。

2. 主界面功能

主界面包含以下输入项和操作按钮：
	1.	待分享文件输入框
	•	默认值：启动时传入的 .html/.htm 文件路径；
	•	提供“选择文件”按钮，可通过文件对话框重新选择。
	2.	本地 Git 仓库路径
	•	默认值：/home/bruce/git/xiaobu/ai；
	•	可编辑，修改后记忆上次设置。
	3.	分享后文件名
	•	默认值：保留原文件名，如 xxx.html；
	•	xxx 部分默认选中，便于修改。
	4.	分享脚本路径
	•	默认值：/home/bruce/git/xiaobu/push.sh；
	•	可编辑，修改后记忆上次设置。
	5.	网站地址
	•	默认值：https://www.xiaobu.net/ai/；
	•	可编辑，修改后记忆上次设置。
	6.	复制分享链接按钮
	•	功能：将“网站地址 + 分享后文件名”拼接为完整 URL，并复制到剪贴板。
	7.	分享按钮
	•	操作流程：
	•	将“待分享文件”复制至本地 Git 路径；
	•	重命名为“分享后文件名”；
	•	执行指定分享脚本；
	•	输出结果显示在日志框；
	•	若执行成功，自动执行“复制分享链接”功能。
	8.	日志框
	•	显示分享脚本执行的过程和结果，便于排查问题。
