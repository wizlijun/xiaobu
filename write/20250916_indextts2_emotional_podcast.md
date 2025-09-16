# IndexTTS2 大版本升级，10分钟实现情绪饱满的播客

一直关注 B 站开源的 IndexTTS2，上周他们偷偷发布了大版本升级。那么，在 Claude Code 的帮助下，我们快速生成一个播客吧。

这篇文章将带你体验如何利用 IndexTTS2 和 AI 工具，在 10 分钟内搭建一套完整的情绪播客生成流程。

## 获取代码和模型

首先拉取开源代码：

```bash
git clone https://github.com/index-tts/index-tts
```

模型需要通过 ModelScope 下载：

```bash
modelscope download --model IndexTeam/IndexTTS-2
```

## 调试项目环境

进入 `index-tts` 目录，运行 Claude Code。输入以下 prompt：

> 请调试通过这个项目。如果需要模型下载，请调用 modelscope download --model IndexTeam/IndexTTS-2

Claude Code 会自动调通开源工程，并下载好模型。

## 生成 TTS 命令行脚本

让 AI 生成一个 TTS 命令行工具，把多行文本转成 wav 语音，使用自己的声纹文件 `ning.wav`：

> 请生成一段脚本 gentts.py -v ning.wav -t "你好(happy)我很开心" -o output.wav 调用 indextts2 来生成语音。

这样就可以使用小宁子的声音生成语音了。

## 设计情绪格式和解析

由于 IndexTTS2 不支持 SSML (Speech Synthesis Markup Language)，需要自己设计一种格式。我设定为在每一行句子前面加上 `(情绪,强度)`。

使用以下 prompt 让 AI 设计格式：

> 请设计一个多行的格式字符串格式，(emotion(happy, angry, sad, afraid, disgusted, melancholic, surprised, calm),强度(0.0-1.0))完整句子，来生成带情感的语音。解析更新到 gentts.py 中

## 生成情绪丰富的脚本

使用摘要工具（Claude Code、GPT5 或 Gemini）生成带饱满情绪的脚本。我直接在 Gemini 2.5 Pro 生成的，它理解大量文本时很方便。

### 生成脚本的 Prompt

> 请根据以下群聊内容，请提取事实信息，生成一段情感丰富的口播脚本，用作 TTS 生成，其中带标准协议的情绪。主题是今日的主要新闻。

> 我的 tts 不支持 ssml，请更换为多行句子的描述，并根据内容增加情绪，放在句子最前面，以 (情绪,强度) 句子的形式。情绪为单词 (happy, angry, sad, afraid, disgusted, melancholic, surprised, calm)，如果不标注则为 calm 情绪。强度为 0.0-1.0 的小数，表示情绪的强度。请生成分析结果的多行句子。

### 生成的脚本示例

输入一天的群聊，即可生成今天的群聊脚本：

```markdown
(calm,0.0)让我们看看今天AI编程群里聊了什么。
(happy,0.8)今天群里最热烈的话题，无疑是AI编程工具的"神仙打架"！
(surprised,0.7)随着OpenAI正式发布GPT5 Codex，它与Claude Code的竞争进入了白热化阶段。
(melancholic,0.5)群友们热议，Anthropic公司此前激进的封号策略，可能无形中为新发布的Codex送上了一波"神助攻"。
(angry,0.8)大家还深入讨论了Anthropic公司CEO Dario Amodei公开推动技术封锁的立场，言语间充满了愤慨。
(calm,0.0)在实际使用上，开发者们也分享了各自的工作流，比如结合使用Claude Code进行规划和Codex进行具体编码，以发挥各自的优势。
(melancholic,0.6)另一个核心讨论，是关于AI软件工程的未来，一种"明日不可知"的迷茫感在群里蔓延。
(melancholic,0.5)大家普遍认为，由于技术迭代速度"一日千里"，任何试图定义未来的理论都可能瞬间过时。
(happy,0.6)这种快速进化也体现在提示词工程上，过去需要绞尽脑汁的复杂指令，现在正被更简洁的自然语言所取代！
(surprised,0.6)群里还提出了一个有趣的观点：有时候感觉AI把代码搞乱了，其实是AI的快速响应打乱了开发者的思路，导致开发者自己迷失了方向。
(calm,0.0)在具体应用上，大家也聊到了利用AI进行老旧项目代码迁移，以及让不同大模型匿名互评解决方案的有趣实验。
(happy,0.7)从工具大战到未来迷思，今天的讨论再次展现了AI编程领域的飞速发展和深度思考。
```

## 生成播客语音

运行以下命令，等待逐行运行，即可生成播客语音：

```bash
uv run gentts.py -v ning.wav -f ai.txt -o aitalk.wav
```

可以再快速增加 wav2mp3、调语速等功能。如果不希望情绪这么夸张，可以修改 prompt。

## 功能扩展

我把一整本书丢给 Gemini，在 prompt 中强调想听的内容。它可以很快的生成带情绪的故事脚本，实现本地自动化生成播客。

这套流程不仅适用于日常群聊内容，还能处理各种长文本内容，让你的播客更加生动有趣。

赞 B 站开源、赞 LLM、Claude Code 的强大，让我们 10 分钟就能得到想要的播客生成工具。