很想写一篇文章讲讲Claude是怎么做到的。但又懒得写，几个要点：
1. 可以不改一行代码，完全让Claude通过对话实现
2. 可以让Claude写个脚本，调用Claude带上prompt处理文本，例如让它把sub.srt翻译为中文。再按要求生成文案，保存为markdown。这个相当于Claude套Claude了，解决了命令行调用LLM的问题。
3. 只需要付费订阅Claude Code，即可使用全部AI能力。不再需要Coze和Cursor了


需要注意几点：
1. 你必须知道自己想要什么
2. 不断观察它选用的开源方案，并引导它使用效果好的方案
3. 它会乱改开源组件的源码，发现了要立即禁止，只允许它写自己能驾驭的脚本代码。
4. 保持耐心。因为它可以让之前不可能的事情变为可能。ROI极高

# 直接看我改了3天的效果：
这是输入YouTube、Instagram短视频，直接翻译，并用自己的声音朗读出来。还会自动生成小红书文案。因为使用了Claude 4模型，所以专业词汇的翻译极其精准。超过了剪映付费版的效果

# 一个sh搞定一切：

## 用法
用法: ./download_and_process.sh [选项] <视频URL>

选项:
  -l, --language LANG    设置原视频语言 (默认: auto)
  -nm, --no-merge       跳过字幕优化，保持原始Whisper输出
  -v, --voice FILE       设置参考语音文件 (默认: bruce.wav)
  -s, --speed RATE       设置语速倍数 (默认: 1.5)
  --fsize SIZE          设置字幕字体大小 (默认: 15)
  -h, --help            显示帮助信息

语言代码:
  auto    自动识别
  ms      马来语
  ru      俄语
  其他    参考whisper支持的语言代码

支持的平台:
- YouTube (youtube.com, youtu.be)
- Instagram (instagram.com)


功能说明:
  1. 使用yt-dlp和Edge浏览器Cookie下载视频
  2. 自动执行视频预处理（音频提取、语音识别、字幕优化）
  3. 使用Claude AI自动翻译字幕为中文
  4. 生成小红书营销文案
  5. 使用IndexTTS生成中文配音视频（含字幕）

# 测试样例
使用雷总的声音，翻译这个不知道哪国小哥的视频

./download_and_process.sh https://www.instagram.com/reel/CkEKn_AAZbE/\?igsh\=MW9xbmo5ZnBjM2Y3bQ\=\= -v lei.wav -s 1.5 -nm

# 生成效果：
文案：
#Word记笔记？你还活在上世纪吗
还在用Word记笔记？那你可能错过了整个数字时代。
**三款神器拯救你的学习效率：**
🔥**Notion**- 学霸专用整理模板不只是笔记，是你的第二个大脑，间隔重复系统，自动提醒复习
📚**RemNote**- 双向链接+卡片记忆边记笔记边制作记忆卡片，算法优化复习时间，科学记忆
🎯**Obsidian**- 颜值与实力并存知识图谱可视化连接，让思维像蜘蛛网一样延展
告别Word的线性思维，拥抱真正的知识管理。
学习不是填鸭，是构建你的知识宇宙。
翻译自: https://www.instagram.com/reel/CkEKn_AAZbE/?igsh=MW9xbmo5ZnBjM2Y3bQ==

# 视频
