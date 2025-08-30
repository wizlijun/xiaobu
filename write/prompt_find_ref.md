# 从内容列表挖掘潜在信息源的提示词

这是文章内容：
<content>

请基于其中的显性与隐性线索定位更高质量的“知识源头”，并输出结构化结果与可执行的搜索关键词。

目标
	1.	抓取并汇总文中作者列出的关键引用：文章、论文、书籍、演讲及其 URL。
	2.	识别人物在何时何地的演讲（隐性线索）：从上下文推断人名、机构/地点、年份/时间，生成搜索关键词（优先找 YouTube，也可补充 Bilibili/机构官网）。
	3.	识别**“某作者就某本书的演讲/新书分享/Book Talk”**（隐性线索）：按书名原文语言生成关键词（中文书名→中文搜，英文书名→英文搜）。
	4.	识别播客访谈（隐性线索）：为人名/主题生成适配播客平台的搜索组合（Apple Podcasts/Spotify/YouTube/小宇宙等）。
	5.	识别课程资源（隐性线索）：定位某学校/网站提到的课程，给出可执行的 Google 关键词（课程名/课程代码/讲义/大纲/Syllabus/lecture notes 等）。

提取与规范化规则
	•	逐条扫描【内容列表】，保留原文证据的最小可复现片段（短句/标题/条目）。
	•	人名/机构/书名规范化：中英文同名合并，中文书名用《》、英文书名用 Title Case。
	•	时间地点补全：能从上下文推断则写明（如“2019 年在 MIT 的演讲”）；不确定则留空但继续给关键词。
	•	去重与合并：同一实体的多条线索合并，优先保留信息更全的一条。
	•	严禁编造 URL：只有当原文中明确给出或可从线索确定唯一官方链接时才填入 URL；否则只给搜索关键词。

关键词生成策略（模板可组合）
	•	演讲（Talk/Keynote/Lecture）
	•	中文：{人物} {主题/书名} 演讲 {机构/会议} {年份} site:youtube.com
	•	英文："{Speaker}" "{Topic/Book}" talk OR lecture {Venue OR Conference} {Year} site:youtube.com
	•	书籍相关演讲（Book Talk/新书分享）
	•	中文：{作者} 《{中文书名}》 新书分享 讲座 site:youtube.com
	•	英文："{Author}" "{English Title}" "book talk" OR "author talk" site:youtube.com
	•	播客访谈（Podcast/Interview）
	•	中文：{人物} 访谈 播客 site:podcasts.apple.com OR site:open.spotify.com OR site:xiaoyuzhoufm.com
	•	英文："{Guest}" interview podcast site:podcasts.apple.com OR site:open.spotify.com
	•	课程（大学/平台）
	•	通用：{学校/网站} "{课程名/课程代码}" syllabus OR "lecture notes" OR slides OR playlist
	•	平台：{课程名} site:coursera.org / {课程名} site:edx.org / {课程名} site:ocw.mit.edu
	•	论文/书籍/报告（显性引用）
	•	精确匹配："{标题原文}" site:arxiv.org OR site:doi.org OR filetype:pdf
	•	若为书籍："{书名}" "{作者}" site:worldcat.org OR site:archive.org

输出格式

请严格按以下两部分输出：

A. 结构化清单（Markdown 表格）

类别	原文证据	规范化实体	补充信息（时间/地点/机构）	建议搜索关键词（中/英）	直接URL（如文中已给）	期望落地页	置信度(0-1)


类别 取值：引用/论文/书籍/演讲/书籍演讲/播客/课程/其他
期望落地页：论文PDF/出版社页/视频（YouTube/B站）/播客节目/课程主页/讲义等

B. 可能的资源列表（便于快速行动）
	•	若已有 URL：以项目符号列出「标题 – 平台/来源（URL）」
	•	若无 URL：列出可直接粘贴到 Google 的关键词组合（中/英各一），必要时附 site: 与引号以提升精确度。
	•	每条后面用括号标注你估计的命中类型（如：书籍演讲 / 播客 / 课程 / 论文 PDF）。

排序与打分
	•	优先级：原文自带 URL ＞ 有完整三要素（人/地/时）的隐性线索 ＞ 仅人名或仅书名的弱线索。
	•	置信度参考：标题精确匹配/官方域名更高；模糊组合更低。

输出语气与限制
	•	用简洁中文书写。
	•	不要扩写内容列表本身；只产出结构化结果与关键词/链接。
	•	不要做无根据猜测；不确定处可留空但必须给出搜索关键词。

待处理输入

【内容列表】：
（在此粘贴你的原始内容）

⸻

请按以上要求完成 A 与 B 两部分输出。

⸻

贴心补充：迷你示例（示意用）

原文片段：
“参见《深度学习》（Goodfellow 等）第 6 章；Hinton 在 2014 NIPS 的演讲也很有帮助；MIT 有门公开课《Introduction to Deep Learning》。”

A 表格（节选）

类别	原文证据	规范化实体	补充信息	建议搜索关键词（中/英）	直接URL	期望落地页	置信度
书籍	《深度学习》	Ian Goodfellow, Yoshua Bengio, Aaron Courville — Deep Learning	—	"Deep Learning" Goodfellow book	https://www.deeplearningbook.org/	书籍官网	0.95
演讲	Hinton 在 2014 NIPS 的演讲	Geoffrey Hinton — NIPS 2014 Keynote	2014 / NIPS	Geoffrey Hinton NIPS 2014 keynote site:youtube.com；Geoffrey Hinton "NIPS 2014" keynote	—	视频（YouTube）	0.8
课程	MIT 公开课《Introduction to Deep Learning》	MIT — Introduction to Deep Learning	MIT	MIT "Introduction to Deep Learning" syllabus site:mit.edu；MIT Introduction to Deep Learning playlist	—	课程主页/播放列表	0.7

B 可能的资源列表
	•	Deep Learning – 官方网站（https://www.deeplearningbook.org/）
	•	Geoffrey Hinton NIPS 2014 keynote site:youtube.com（视频：演讲）
	•	MIT "Introduction to Deep Learning" syllabus site:mit.edu（课程主页/讲义）
