# GitHub Issues 几乎是世界上最好的笔记本

免费且无限制，支持公开和私人笔记。

全面支持 Markdown，包括几乎所有编程语言的语法高亮。还可以直接拖拽图片或视频到笔记中。

内链功能强大。你可以在 Markdown 列表中粘贴其他 issue 的 URL（任何 GitHub 仓库都行）：

- https://github.com/simonw/llm/issues/1078
- https://github.com/simonw/llm/issues/1080

你的 issue 会自动拉取其他 issue 的标题，同时那个 issue 也会获得指向你这里的反向链接——完全遵循可见性规则。

搜索功能卓越，支持仓库内搜索、跨仓库搜索，甚至全 GitHub 搜索，再也不怕忘记把内容放在哪了。

API 功能完善，支持导出笔记和创建编辑新笔记。配合 GitHub Actions 的 issue 事件触发，几乎可以自动化任何操作。

唯一缺失的功能？离线同步支持。我在手机上还是主要用苹果备忘录，就因为它能离线工作，之后再与笔记本同步。

受 Hacker News 讨论启发的补充说明：

隐私问题不用担心。许多公司向 GitHub 付费来保护源代码和相关资源的安全。GitHub 不会为了"训练模型"之类的事情牺牲这种信任。

任何笔记平台都存在可能泄露笔记的 bug 风险。所以我从不在笔记中存放密码！

不付费、不自建是重要特性。我不想因为配置错误或账单问题丢失笔记！

使用 `- [ ] 项目` 语法创建清单功能很实用。甚至可以用 `- [ ] #ref` 引用其他 issue，当那个 issue 关闭时，复选框会自动勾选。

我试过各种本地备份笔记的方法，比如 github-to-sqlite。虽然还没在独立机器上设置定时任务，但真的应该做！

一旦纸质笔记能自动备份到至少两个不同大洲，我就回归纸笔。

GitHub Issues 扩展性强！microsoft/vscode 有 195,376 个 issues，flutter/flutter 有 106,572 个。永远不会用完空间。

将笔记导入 LLM 的格式很有趣。这里有个最近的例子，我用 llm-fragments-github 将一个 50+ 评论、持续 1.5 年的 issue 线程总结成了新评论。

我很好奇自己在 GitHub 上创建了多少 issues 和评论。在 Claude 帮助下，发现可以用 GraphQL 查询：

```
{
  viewer {
    issueComments {
      totalCount
    }
    issues {
      totalCount
    }
  }
}
```

在 GitHub GraphQL Explorer 工具中运行，得到结果：

```
{
  "data": {
    "viewer": {
      "issueComments": {
        "totalCount": 39087
      },
      "issues": {
        "totalCount": 9413
      }
    }
  }
}
```

总共 48,500 个 issues 和评论！