# 为 AI 编写文档：最佳实践

检索增强生成 (RAG) 系统如 Kapa 依赖您的文档来提供准确、有用的信息。当文档既能很好地服务于人类又能服务于机器时，它会创建一个内容质量的自我强化循环：清晰的文档改善 AI 答案，而这些答案有助于发现进一步改善文档的差距。

本指南提供了创建既能有效服务于人类读者又能有效用于 RAG 系统中 AI/LLM 消费的文档的最佳实践。许多最佳实践同时惠及两者，通常以互补的方式。

## 为什么文档质量很重要

文档质量一直对帮助用户理解和有效使用您的产品很重要。当 AI 系统使用相同的内容来回答用户问题时，它变得更加重要。糟糕的文档不仅让人类读者感到沮丧，还直接降低 AI 响应的质量，创造出复合问题，即糟糕的内容导致糟糕的答案。

了解 AI 系统如何处理和使用您的文档揭示了为什么内容质量对良好的 AI 性能是不可协商的。

## AI 系统如何处理您的文档

Kapa 通过找到您内容的相关片段并使用它们构建答案来工作。该过程涉及三个主要组件：

- **检索器**：搜索您的知识源以找到与用户问题匹配的内容
- **向量数据库**：以可搜索的格式存储您的内容，实现快速准确的检索
- **生成器**：使用检索到的内容创建有用回应的大型语言模型 (LLM)

一旦您将知识源连接到 Kapa，信息就会通过特定流程流动：

1. **摄取**：内容被分成块（更小、更聚焦的部分）并存储在向量数据库中
2. **查询处理**：当用户提问时，系统将他们的问题转换为可搜索的格式
3. **检索**：系统从您的文档中找到最相关的块
4. **答案生成**：LLM 使用这些块作为上下文生成回应

在 AI 消费您的内容的步骤中，有一些值得强调的写作和结构模式，它们可能会负面影响您的内容被理解的程度：

- **AI 系统使用块工作**：它们将文档作为离散的独立片段处理，而不是作为连续的叙述阅读
- **它们依赖内容匹配**：它们通过比较用户问题与您的内容来找到信息，而不是通过遵循逻辑文档结构
- **它们失去隐含连接**：除非明确说明，否则章节之间的关系可能不会被保留
- **它们无法推断未陈述的信息**：与可以做出合理假设的人类不同，AI 系统只能使用明确记录的信息

为 AI 系统优化的文档理想情况下应该是明确的、自包含的和上下文完整的。一个块能够独立存在，同时与相关内容保持清晰关系的程度越高，AI 理解它的程度就越好。信息越明确、越不模糊，检索准确性就越好，AI 就越有能力自信地回答问题。

虽然 AI 在处理非结构化内容方面表现出色，但以检索为目的编写和构建的信息也确实可以大大提高您知识源的"询问 AI"界面的质量。

## 为什么分块是必要的

理想情况下，分块是不必要的，AI 可以持续地将您的整个知识库保持在上下文中，始终如此。不幸的是，这是不切实际的。这不仅是由于令牌限制，还因为 LLM 在提供优化的、聚焦的上下文时表现明显更好。大型或过于宽泛的上下文增加了模型忽略或误解关键信息的可能性，导致准确性降低和输出不够连贯。

将文档分割为更小的、语义连贯的块使检索系统能够向 LLM 呈现最相关的内容。这种有针对性的方法显著提高了模型理解、检索精度和整体响应质量。

## 优化内容的快速技巧

为 AI 优化内容在原理上类似于为可访问性和屏幕阅读器优化内容：您的内容越清晰、越结构化、越机器可读，它的表现就越好。正如清晰的语义结构帮助可访问性工具有效解析内容一样，清晰的结构显著提高了 AI 的准确性。本节概述了一些您今天就可以应用的可操作的实用改进，以使您的文档更加机器可读。

优先考虑这些调整为解决更细致的内容挑战奠定了坚实的基础，如 **AI 内容设计挑战** 部分所讨论的。

### 1. 使用标准化的语义 HTML

对于网站源，确保正确和语义化地使用 HTML 元素，如标题（`<h1>`、`<h2>`）、列表（`<ul>`、`<ol>`）和表格（`<table>`）。语义 HTML 确保清晰的文档结构，提高内容分块和检索的准确性。

**示例：**
```html
<h2>如何启用 webhook</h2>
<ol>
  <li>登录您的 CloudSync 控制台。</li>
  <li>导航到设置 &gt; Webhook。</li>
  <li>将 webhook 切换为"已启用"。</li>
</ol>
```

更重要的是，避免错误使用元素。例如，错误放置的 `<h2>` 元素可能对机器解析您的内容产生严重后果。

### 2. 避免 PDF，首选 HTML 或 Markdown

PDF 文档通常具有复杂的视觉布局，使机器解析变得困难。将内容从 PDF 迁移到 HTML 或 Markdown 会大大提高文本提取和检索质量。

### 3. 创建爬虫友好的内容

通过减少或消除自定义 UI 元素、JavaScript 驱动的动态内容和复杂动画来简化页面结构。清晰、可预测的 HTML 结构有助于更容易的索引和解析。

用纯文本替代方案或简单的交互元素替换复杂的 JavaScript 小部件。

### 4. 确保语义清晰度

使用描述性标题和反映内容层次结构的有意义的 URL。语义清晰度帮助 AI 正确推断内容关系，大大提高检索准确性。

**有意义 URL 的示例：**
- ✅ 好：`/docs/cloudsync/setup-webhooks`
- ❌ 差：`/docs/page12345`

### 5. 为视觉内容提供文本等效物

始终为关键视觉信息（如图表、图形和截图）包含清晰的文本描述。这确保关键细节对机器和屏幕阅读器都保持可访问。

**示例：**
```markdown
![系统架构图](architecture.png)

**图 1：** 说明 CloudSync 集成工作流程的图表，
详细说明身份验证、数据上传和确认步骤。
```

### 6. 保持布局简单

避免意义严重依赖视觉定位或格式的布局。布局在转换过程中会丢失，其设计传达的任何意义也会随之丢失。使用清晰标题、列表和段落的简单结构内容可以有效地转换为纯文本。

## AI 内容设计挑战

本节深入研究了可能为 AI 系统创建挑战的常见内容设计反模式。这些挑战通常源于信息的组织、上下文化或假设方式，而非格式化方式。每个示例都突出了特定的问题模式、为什么它会给 AI 造成问题，以及如何重写或重构您的内容来避免它。

### 上下文依赖

**问题：** 将关键细节和定义分散在多个章节或段落中的文档在内容被分成块时会产生问题。当关键信息与其上下文分离时，单个块可能变得模糊或不完整。

了解分块在实践中的工作原理揭示了邻近性为什么重要。Kapa 尝试通过尽可能保持章节完整来保持文档结构，但实际约束经常强制分割：

- 太长的章节在段落或句子边界处被分割
- 太短的章节与相邻内容合并
- 块大小必须平衡以获得最佳检索性能

由于无法完美预测块边界，相关信息在源内容中出现得越近，分块后保持在一起的可能性就越大。这个邻近性原则对于保持意义变得至关重要。

考虑这个（简化的）问题示例：

> 身份验证令牌默认在 24 小时后过期。
> 
> 系统为不同环境提供了几个配置选项。
> 
> 在实现登录流程时，确保您适当地处理这个问题。

当这个内容被分块时，关于配置选项的中间句子可能导致分块算法将令牌过期细节与实现指导分离。包含"在实现登录流程时，确保您适当地处理这个问题"的结果块失去了关于"这个"指什么和特定 24 小时时间框架的关键上下文。

**解决方案：** 在紧密邻近的范围内保持相关信息在一起。当引入具有重要约束或上下文的概念时，在同一段落或紧邻段落中包含这些细节。

> 身份验证令牌默认在 24 小时后过期。在实现登录流程时，确保您通过在 24 小时限制之前刷新令牌或为过期令牌响应实现适当的错误处理来处理令牌过期。
> 
> 系统为不同环境提供了几个配置选项，包括自定义令牌过期时间。

通过保持约束（24 小时过期）接近其实现指导，无论边界落在何处，它们更有可能保持在同一块中。

寻找孤立阅读时变得不清楚的章节，特别是标题通用和引用早期段落上下文的多步骤过程。

### 语义可发现性差距

**问题：** Kapa 基于查询和内容之间的语义相似性找到信息。如果重要术语或概念不在块中出现，该块不会被相关查询检索，即使它包含所需的确切信息。

```markdown
## 配置超时

配置自定义超时设置和重试逻辑以提高生产环境的可靠性。
通过管理面板访问这些选项。
```

如果用户询问"如何配置 CloudSync 超时？"，这个块可能不会被检索，因为文本中没有出现"CloudSync"。

**解决方案：** 为您产品的独特概念建立一致的术语并系统性地使用它们。在记录功能时包含特定的产品或功能名称。

```markdown
## 配置 CloudSync 超时

配置自定义 CloudSync 超时设置和重试逻辑以提高生产环境的可靠性。
通过 CloudSync 管理面板访问这些选项。
```

您产品的独特术语在模型的训练数据中不会得到很好的体现。明确、一致的使用有助于确定哪些内容与哪些产品功能相关。

**平衡说明：** 这并不意味着您应该在每个句子或标题中重复产品名称。Kapa 还使用文档结构、URL 和父标题来推断上下文。重要的是，对于任何给定的块，都有一个清晰一致的信号将其连接到您的产品或功能。请参阅 **分层信息架构** 了解结构元数据如何支持这一点。

### 隐含知识假设

**问题：** Kapa 基于一个简单原则运作：如果信息没有明确记录，它就不存在于系统的知识库中。与可以利用外部知识或做出合理推断的人类读者不同，Kapa 只能使用提供的信息。

当文档假设用户知识时，这些就成为危险的差距。设计良好的 RAG 系统应该选择不确定性而非不准确性，但这只有在文档明确解决用户询问的主题时才有效。

**解决方案：** 在程序性内容中包含先决条件步骤，而不是假设先前的设置。当引用外部工具或概念时，提供简要上下文或详细解释的链接。

**之前：**
```markdown
## 设置 webhook

在控制台中配置您的端点 URL 并测试连接。
```

**之后：**
```markdown
## 设置 CloudSync webhook

在配置 webhook 之前，确保您具备：

- 可公开访问的 HTTPS 端点
- 有效的 SSL 证书
- CloudSync API 凭据

在设置 > 集成下的 CloudSync 控制台中配置您的端点 URL，
然后使用"测试连接"按钮验证设置。
```

寻找假设熟悉工具或界面的说明，或引用没有解释的"标准"配置。

### 视觉信息依赖

**问题：** 嵌入在图像、图表和视频中的关键信息为解析您文档的摄取过程创建问题。当关键信息仅出现在视觉元素中时，用户可能收到不完整的答案。

**示例：** 完全依赖图形元素的信息
```markdown
请参阅下面的图表了解完整的 API 工作流程：
![显示 8 步过程的复杂流程图](workflow.png)

按照以下步骤实现集成。
```

依赖视觉元素的说明对自动化系统变得不可访问，使得说明变得无意义。

**解决方案：** 提供捕获基本信息的基于文本的替代方案。将工作流程图表示为编号步骤列表，同时保留视觉元素作为补充。

```markdown
## CloudSync API 工作流程

CloudSync 集成遵循以下工作流程：

1. **身份验证**：向 `/auth/token` 端点发送 API 凭据
2. **验证**：系统验证凭据并返回访问令牌
3. **数据准备**：根据 CloudSync 模式格式化您的数据
4. **上传请求**：使用访问令牌将数据 POST 到 `/sync/upload`
5. **处理**：CloudSync 验证并处理数据
6. **状态检查**：轮询 `/sync/status/{job_id}` 获取处理更新
7. **完成**：同步完成时接收确认
8. **错误处理**：处理任何验证或处理错误

![API 工作流程图](workflow.png)
_上述工作流程步骤的视觉表示_
```

### 布局依赖信息

**问题：** 依赖视觉布局、定位或表格结构的信息在被机器作为文本处理时经常失去意义。虽然人类可以解释视觉关系和分组内容，但 AI 系统很难维持这些连接。

具有合并标题和视觉分组的复杂或结构不良的比较表在转换为纯文本时变得模糊：

```
定价		
基础计划	标准计划	企业计划
5 个用户	25 个用户	无限用户
1GB 存储	10GB 存储	无限存储
邮件支持	电话支持	7x24 专属支持
API 限制		
100 请求/小时	1,000 请求/小时	无速率限制
仅基础端点	所有端点	所有端点 + webhook
```

**解决方案：** 如果表格表示更合适，确保标题和行在语义上是正确的。但是，表格表示并不总是合适或必要的。您也可以考虑在文本形式中保持关系的替代方案。使用结构化列表或重复上下文来维持连接。例如：

```markdown
## CloudSync 定价计划

### 基础计划

- 5 个用户
- 1GB 存储
- 邮件支持
- API 限制：100 请求/小时，仅基础端点

### 标准计划

- 25 个用户
- 10GB 存储
- 电话支持
- API 限制：1,000 请求/小时，所有端点

### 企业计划

- 无限用户
- 无限存储
- 7x24 专属支持
- API 限制：无速率限制，所有端点加 webhook
```

保留每行自包含的简单参考表，但补充或替换单元格之间的关系传达重要意义的复杂表格。

## 内容组织

以下技术有助于创建可以有效检索的内容，而不牺牲可读性。

### 分层信息架构

当您的内容被摄取到 Kapa 中时，预处理步骤提取有助于保持上下文和提高检索准确性的元数据。提取的最有价值的数据之一是每个文档或章节的分层位置。

这个层次结构包括多层上下文：URL 路径、文档标题和标题。这些元素协同工作，为从原始位置分离后的内容块构建上下文理解。

设计您的内容层次结构，使每个章节都承载足够的上下文以便独立理解，同时与父级和同级内容保持清晰的关系。

在规划内容结构时，考虑用户如何在没有搜索的情况下找到任何给定的章节。确保每个章节包含足够的上下文以便独立理解：

- **产品系列**：哪个产品或服务区域
- **产品名称**：特定产品或功能名称
- **版本信息**：适用时
- **组件特异性**：子功能或模块
- **功能上下文**：用户试图完成什么

这种分层清晰度帮助 AI 系统理解概念之间的关系，并在为用户查询检索信息时提供更丰富的上下文。

### 自包含章节

依赖读者遵循线性路径或记住先前章节细节的文档章节在作为独立块处理时会变得有问题。章节基于相关性被检索，文档顺序不被保留，因此章节理想情况下应该在孤立遇到时有意义。

比较同一信息的两种方法：

**上下文依赖：**
```markdown
## 更新 webhook URL

现在将端点更改为您的新 URL 并保存配置。
```

**自包含：**
```markdown
## 更新 webhook URL

要在 CloudSync 中更新 webhook 端点：

1. 在您的 CloudSync 控制台中导航到设置 > Webhook
2. 选择您要修改的 webhook
3. 将端点 URL 更改为您的新地址，然后点击保存
```

自包含版本在作为孤立块检索时有效，因为它包含基本上下文：什么系统（CloudSync）、在哪里找到设置（设置 > Webhook）以及完整步骤。上下文依赖版本假设读者知道"端点"指的是什么以及他们在界面中的位置。

前置基本上下文并在每个章节边界内包含完整信息。这并不意味着在所有地方重复一切，而是确保章节在独立遇到时保持可操作性。

考虑用关于其范围和先决条件的简要上下文开始每个章节，使用指示章节完成什么的描述性标题，并包含基本背景信息而不假设先前阅读。寻找引用"如上所述"、"现在您已经"或"配置好一切"的章节作为需要明确上下文的信号。

### 错误上下文与解决方案

故障排除文档值得特别关注，因为用户经常通过复制他们遇到的确切错误消息来搜索。当您的文档包含特定错误文本以及解决方案时，它在用户查询和有用内容之间创建直接匹配。

在记录故障排除步骤时，引用确切的错误消息并描述可观察的症状以及解决方案。

**通用故障排除：**
```markdown
## 连接问题

如果连接失败，检查您的网络设置和防火墙配置。
```

**具体故障排除：**
```markdown
## CloudSync 连接问题

### 错误："30 秒后连接超时"

当 CloudSync 无法到达...时发生此错误

### 错误："身份验证失败 (401)"

这表示凭据无效或过期...
```

包含确切的错误文本确保用户在使用他们看到的特定消息搜索时可以找到帮助。要确定在文档中优先处理哪些错误消息，请查看 Kapa 平台中的常见问题分析。这向您展示用户最频繁询问的实际错误消息和问题。

## 结论

创建既能有效服务于人类读者又能服务于 AI 的文档集中在一个基本原则上：明确的、自包含的内容，在概念之间保持清晰的关系。消除上下文依赖、确保可发现性、填补知识差距以及为视觉内容提供文本替代有助于缓解机器消费您文档时的固有限制。

为 AI 工作的文档，在其核心，就是出色的文档：清晰、结构化、明确和用户专注。您的文档越好地服务于您的用户，您的 AI 也越好地服务于他们。

审查和分析用户对话，特别是具有不确定或被否决答案的对话。从对常见问题的即时修复开始，然后逐渐将分散的信息重构为连贯、完整的章节。目标是让每个章节都能独立存在，同时与相关概念保持逻辑连接的文档。 