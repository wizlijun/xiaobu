请使用中文，生成html5，以html5动态交互的方式，生成视频的摘要，要求提炼全部核心要点，高亮事实和观点，做成有趣的闪卡形式


请使用中文，生成html5，以html5动态交互的方式，生成本书的摘要，要求提炼全部核心要点，高亮事实和观点，以书籍层次目录的形式



请在ai目录下每个 html、htm 文件顶部增加 yaml header，参考 template.html 顶部yaml header的样子。title=文档标题，datetime=文件的创建日期，tags为文章最核心的标记，不要超过3个，description是全文的摘要，限于20字以内


解析ai目录下每个 HTML 文件的 YAML header
读取 tag 字段，构建 tag 索引
自动生成 ai/tags.yaml（用于管理 tags 分组）
按5个关键词将tag分组： bushcraft（野外生活技艺）, ai, mind,se(软件工程),others
忽略掉没有意义的标签，例如 tag1 tag2 sample 等
自动生成 ai/tags.html 交互 文件