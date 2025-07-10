# 调用claude翻译一整本电子书

Vibe Coding 使那些过去只服务少数人、甚至只是单个用户的需求也能被高效实现。以往这类需求由于 ROI 很低，即便是企业 CEO 提出的想法，评估后也常因需要大量人力与时间而难以落地，更别说后期的迭代与维护——一旦 CEO 改变主意，前期投入便打了水漂。而现在，借助 AI 编程的能力，这类“高个性化、低经济性”的需求终于具备了可行性。

写代码智能了，这种方式也将极大提升非开发者，如研究人员、产品经理、项目经理、运营等岗位，甚至创客小孩子的数据处理、开源工具使用、问题批量解决等能力。

可以预见，未来大多数 IT 从业者只需清晰描述需求，即可借助 AI Coding 进行实现。只有那些核心产品、具备长期价值的系统，才需要人工持续参与开发与维护，也会更多以 AI 助手或 AI agent 的混合模式出现。

以前我就喜欢写一些自动化脚本，帮助自己批量做一些事情。现在有了 claude code，不仅能力增强很多，还能直接使用大模型能力。阅读、翻译、写作、音视频处理全部得到质的飞跃。一直开着的端侧电脑资源终于得到了利用。

今天我就以一个实际案例来说明——使用 Claude 翻译英文电子书。虽然过程中的 token 消耗相对较多，但对于某些值得精读的小众领域书籍来说，获得高质量中文译本是非常划算的投入。

借由这个例子，我想介绍一下我当前的 Vibe Coding 工作流。

类似这种方式，可以做 PPT翻译、字幕翻译、每日信息的摘要等，都是使用的 Claude 4 模型的质量，效果好过市面上各种收费工具。而且无需额外的 api 消耗。


目前国内使用 Claude code 有难度，但已经有早鸟开始做hacking转售，可以使用，
以下这个 一个月299，通过我的邀请，可以增加10000积分。每天5400积分足够使用，临时不够还可以工单免费重置2次。

https://gaccode.com/signup?ref=R4WOQB8E

## 口述需求如下

尽可能详尽，使用自己看得懂容易改的脚本，如sh python js等

```
技术要求
1. 使用python
2. 每一步骤一个python脚本，以便可以分阶段重做
3. 使用常用的开源组件，如 pandoc等


需求
- 输入 ebook的pdf、docx、epub 格式，例如文件名为 inputbook.pdf
- 输出翻译过的中文 html 文件 
- 语言参数，-l 为输入文本的语言参数，默认为自动识别。 参数--olang,为输出语言，默认为zh
- 实现方式，先创建 inputbook_temp 目录, 所有过程处理的文件放在里面。_- 
	- 将inputbook.pdf 按页码解压到临时目录下，每一页生成一个markdown文件，如page0001.md，和对应的图片资源文件，图片资源文件名为 page0001_img001.jpg等_
- 调用 claude 逐个md翻译，默认prompt为：请翻译page0001.md 文件为 {olang}，输出文件名为 output_page0001.md。 如果output_pagexxx.md 已经存在，则跳过
- 逐个处理完成后，将md合并为 output.md ，每个 page之间使用"\r\n --- \r\n"来分割
- output.md 带图片资源一起转换为 output.html，使用 template.html 作为模板
- 为 output.html 生成toc，放在最前面
```

## 使用LLM 优化和补充需求。使用 Chatgpt 4.1  4o 或 claude 4
prompt：将以下口述需求，整理为可ai coding的需求：{上述文档}
chatgpt4.1：

```
项目需求文档

技术要求
	1.	开发语言：Python
	2.	分阶段脚本：每一步为一个独立的 Python 脚本，方便分阶段执行和重做
	3.	依赖工具：优先选用常用开源组件（如 Pandoc、pdf2image、PyMuPDF、python-docx、ebooklib、requests 等）

⸻

详细需求与流程

输入
	•	支持三种格式：pdf、docx、epub（如：inputbook.pdf）

输出
	•	翻译后的中文 HTML 文件（如：output.html）
	•	支持自定义输入/输出语言参数（如 -l、--olang）

⸻

总体流程分解为以下步骤（每步一个独立脚本）：

⸻

步骤1：环境准备与参数解析
	•	创建临时目录 inputbook_temp/
	•	解析命令行参数（input file、-l、--olang，默认自动识别/zh）

⸻

步骤2：将原始文件按页（或章节）拆分为 markdown
	•	PDF：按页拆分，每页为一个 pageXXXX.md
	•	图片提取为单独文件 pageXXXX_imgYYY.jpg 并保存到 temp
	•	DOCX/EPUB：拆分成每章/每页的 markdown 文件及对应图片
	•	推荐工具：pdf2image、PyMuPDF、python-docx、ebooklib、pandoc

⸻

步骤3：逐页翻译 markdown
	•	针对每个 pageXXXX.md 文件，调用 Claude API 进行翻译
	•	默认 prompt：请翻译 pageXXXX.md 文件为 {olang}，输出文件名为 output_pageXXXX.md
	•	跳过：如 output_pageXXXX.md 已存在，则跳过该页

⸻

步骤4：合并翻译后的 markdown 文件
	•	将所有 output_pageXXXX.md 文件，按顺序合并为 output.md
	•	各页间用 "\r\n --- \r\n" 作为分隔符

⸻

步骤5：markdown + 图片转为 html（基于模板）
	•	使用 Pandoc 或 markdown-it 等，将 output.md 连同图片资源一起转换为 output.html
	•	指定 template.html 作为 HTML 模板（需支持内容插入）

⸻

步骤6：为 HTML 文件生成 TOC（目录）
	•	分析 output.html 中的标题（如 <h1>、<h2>），生成 TOC 并插入到页面最前面

⸻

脚本结构建议
	1.	01_prepare_env.py：解析参数，创建临时目录
	2.	02_split_to_md.py：文件拆分为 markdown + 提取图片
	3.	03_translate_md.py：逐页翻译 markdown
	4.	04_merge_md.py：合并 markdown
	5.	05_md_to_html.py：md+img 转 html
	6.	06_add_toc.py：生成并插入 TOC

⸻

额外说明
	•	所有临时/中间文件统一放到 inputbook_temp/ 下，便于管理和清理
	•	保证脚本可重复运行，已有中间产物时能自动跳过或提示
	•	最终输出为 output.html，且能复用指定模板


```


## 需求直接粘贴给 claude code

生成的代码一次就能运行。

然后根据结果是否满意，再不断对话调整。

claude开始工作，拆分了任务，自己实现，自己调试

Update Todos
  ⎿ ☐ Create 01_prepare_env.py - Parse arguments and create temp directory 
     ☐ Create 02_split_to_md.py - Split files to markdown and extract images
     ☐ Create 03_translate_md.py - Translate markdown files using Claude API
     ☐ Create 04_merge_md.py - Merge translated markdown files
     ☐ Create 05_md_to_html.py - Convert markdown to HTML with template
     ☐ Create 06_add_toc.py - Generate and insert TOC into HTML
     ☐ Create requirements.txt for dependencies
     ☐ Create template.html for HTML output

十几分钟后，任务完成

Features:

  - ✅ Supports PDF, DOCX, EPUB input formats
  - ✅ Multi-language translation (Chinese, English, Japanese, etc.)
  - ✅ Image extraction and preservation
  - ✅ Professional HTML template with dark mode support
  - ✅ Automatic table of contents generation
  - ✅ Responsive design for mobile/desktop
  - ✅ Skip existing files for re-runs
  - ✅ Comprehensive error handling

  The system is now ready for use!


## 优化并调试

prompt：

- template.html 模板太简单了，生成一个适合中文电子书阅读的魔板，使用仿宋体
- 生成一个 translatebook.sh ，将各个步骤串起来，注意参数的传递


掏出买了很久但没有读的电子书 bow.docx

./translatebook.sh bow.docx

坐等翻译结果


报需要claude api 的key。 改用 claude 命令行来处理

prompt：
- 03_translate_md.py实现中，请使用 claude 命令行，带上prompt 实现，用户可增加 -p 'add prompt' 的方式增加prompt


./translatebook.sh bow.docx -p "Bushcraft 专有词汇不做翻译；语言简洁一些；如果有英制，加上公制"  

还是会有些问题，就直接在claude里输入这行命令，让他自己调试通过。

prompt：
- 请调试通过： ./translatebook.sh bow.docx -p "Bushcraft 专有词汇不做翻译；语言简洁一些；如果有英制，加上公制"


它开始自己调试自己修改，当发现我给的 bow.docx 太大时，他会创建一个小的 docx 来调试通过。

代码中没有使用 pandoc 导致效果不满意，知道用哪些强大的开源工具，也是一种能力。可以问一问 chatgpt，哪些开源库好用

> Claude 这类编程工具，解决了开发者 **不知道已有知识和功能存在**的问题。
>     - 很多功能（feature）早就存在，**其实不需要重复造轮子**。例如mmpeg、pandoc、srt等
>     - 对于工具的使用方法和实作技巧（know-how），AI 的掌握 **往往比人类更全面、更广泛**。
>     - 开发者因为 **不知道这些功能或知识的存在**，所以就 **无法使用、甚至无法意识到这些工具的价值**。

prompt
- 请使用 pandoc来实现文档转换拆分合并工作 

....
不少细节的调整，例如：
- 文本段落被分页拆分到不同的 md 里了，需要他写程序优化。
- 图片批量压缩一下
- 折腾python虚拟环境，手动安装一些库，如PyMuPDF之类的


pdf转换为分页md算法时，出现了问题，不同的库效果不一样。
更换不同实现方式时，遗留代码很多。于是删掉大部分代码，重构

prompt：
 - 我已经清理了02_split_to_md.py, 请按我的要求重新实现： docx、epub 先转成pdf，pdf使用pdftohtml 默认参数 转成 html、整理转换的html的图片文件、html根据分页标识 
  拆分成多个 page000x.html ，再使用 pandoc 将html转换为 md


增加断点续传、错误重试等功能，增强可靠性，出错的部分重试就可以补充完成。


