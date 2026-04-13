# LLM Editing Rules

这个文档定义 LLM 辅助维护时应遵守的具体编辑规则。

它比 system prompt 更窄，也更偏操作层。

---

## Rule 1: 尊重仓库分层

在编辑之前，先判断目标页面属于哪一层。

不要随意混层。

Examples:

- 不要把 raw source notes 写进 `WIKI/`
- 不要把 personal reflections 当作事实塞进 `KNOWLEDGE/README.md`
- 不要把 `DASHBOARDS/` 当成 canonical truth

---

## Rule 2: 优先更新已有页面，而不是制造重复

在新建页面之前，先检查：

- 这个 topic 是否已经有 node
- 这个 problem 是否已经有页面
- 这段 synthesis 是否本就属于已有 wiki page

只有在新增页面能带来真实结构价值时，才创建新页面。

---

## Rule 3: 不要静默改变结构关系

如果要改一个 node 的 dependency、alternative 或 related-problem mapping，
这类变化主要应落在 `meta.yaml`。

不要只改 prose，让结构与正文失配。

---

## Rule 4: 把事实、综合和判断分开

编辑时要保持：

- fact-like material 要能指向 sources
- synthesis 要明确是 synthesis
- personal judgment 要明确标注

不要把它们压成一种声音。

---

## Rule 5: 保持 uncertainty 可见

如果某件事还没有定论：

- 增加 `Open questions` section
- 或增加 `Caveats` section
- 或使用类似这样的表述：
  - `Current evidence suggests...`
  - `This appears to...`
  - `This has not yet been personally verified.`

不要伪造 closure。

---

## Rule 6: 尽量做 incremental edits

优先：

- adding a section
- refining a section
- improving structure
- clarifying a comparison

除非页面本身已经明显坏掉，否则不要动不动就整页重写。

incremental change 更容易 review，也更安全。

---

## Rule 7: 有意义地交叉链接

编辑页面时，应在确实相关时添加链接到：

- related nodes
- related problems
- related projects
- related work assets
- related career assets
- related wiki pages

但不要为了增加链接密度而乱加。

链接的目标，是降低 navigation cost。

---

## Rule 8: 保持页面身份

一个页面应保持它自己的页面类型。

Examples:

- node page 不应变成 broad survey
- problem page 不应塌成单一方法总结
- wiki page 不应退化成 raw note dump
- career story 不应变成 project README

如果内容本身想变成另一类对象，应创建或更新正确的页面，而不是硬改当前页。

---

## Rule 9: 维护 frontmatter 与 metadata

如果编辑的页面带有 frontmatter，要谨慎保留和更新。

尤其是 wiki pages，要维护这些字段：

- `title`
- `page_type`
- `compiled_from`
- `last_compiled_at`
- `confidence`

不要轻率删除 metadata。

---

## Rule 10: 为未来保留价值

写出的编辑应让未来的仓库主人仍然能受益。

这意味着：

- 不要只为当前对话上下文优化
- 保持页面结构可复用
- 除非明确需要，否则避免临时措辞
- 写完后页面应在以后单独阅读时仍然成立

---

## Rule 11: 暴露歧义，而不是掩埋歧义

如果 sources 互相冲突，或关系并不清楚：

- 直接说明歧义
- 指向冲突材料
- 需要时建议 human review

不要用 polished prose 把 disagreement 藏起来。

---

## Rule 12: 每次编辑都应对系统产生可识别提升

一次好的编辑，至少应改善以下一项：

- clarity
- traceability
- structure
- usefulness
- consistency
- actionability

如果编辑只是把文字变长，大概率还不够好。
