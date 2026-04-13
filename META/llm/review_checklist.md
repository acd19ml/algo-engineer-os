# LLM Review Checklist

这个文档定义在接受 LLM 辅助更新前的 review checklist。

目标不是否掉每一个不完美草稿。  
目标是确保一条更新能改善系统，而不是破坏 trust、structure 或 long-term maintainability。

---

## 快速检查问题

在接受一条 LLM-generated 或 LLM-edited 更新前，先快速问：

1. 这次更新是否放在了正确的 repository layer？
2. 它是否遵守了 source-of-truth priority？
3. 它是否提升了 clarity 或 usefulness？
4. 它有没有 invent anything？
5. 它有没有抹掉重要 uncertainty？
6. 它有没有保留 links 和 structure？
7. 它以后单独看还成立吗？

如果其中任何一项答案是否定的，先 revise，再接受。

---

## Section A: Layer correctness

### Check A1

这个页面是否真的属于它被创建或编辑的目录？

Examples:

- concept explanation 不应意外变成 wiki synthesis
- project page 不应变成 career story page
- reflection 不应变成 factual reference page

### Check A2

这个页面是否仍然保留了自己这一层的用途？

Examples:

- `KNOWLEDGE/` 应保持 structured and reusable
- `WIKI/` 应保持 compiled and traceable
- `THINKING/` 可以主观，但应清楚地保持主观

---

## Section B: Truthfulness and evidence

### Check B1

这次更新是否引入了 unsupported factual claims？

### Check B2

它是否混淆了这些层次：

- source-backed fact
- synthesis
- personal interpretation
- speculation

### Check B3

如果 confidence 是 low 或 mixed，这一点是否在文字中可见？

### Check B4

如果 lower-level sources 互相冲突，这次编辑是否把冲突显式暴露出来？

---

## Section C: Structural integrity

### Check C1

这次更新是否保留了重要 metadata？

Examples:

- `meta.yaml` fields
- wiki frontmatter
- explicit relationship fields

### Check C2

如果结构关系发生变化，它是否被更新到了正确位置？

Examples:

- dependencies 应反映在 `meta.yaml`
- 而不只是藏在 prose 里

### Check C3

这次更新是否制造了重复，本来一个 link 就够？

### Check C4

它是否保留或改善了内部链接？

---

## Section D: Readability and usefulness

### Check D1

编辑后，这个页面是否更容易使用了？

### Check D2

这次编辑是否至少改善了以下一项：

- clarity
- structure
- traceability
- actionability
- navigation
- reusability

### Check D3

这次更新是不是“更长了，但没更好”？

如果是，就该 trim。

### Check D4

未来的你会不会因为这次编辑，更快看懂这个页面？

---

## Section E: Repository consistency

### Check E1

这个页面是否遵守 naming 和 formatting conventions？

### Check E2

在适用时，它的结构是否大体符合对应 template？

### Check E3

这次更新是否仍然与以下规则一致：

- source-of-truth policy
- naming convention policy
- node granularity policy
- LLM editing rules

---

## Section F: Long-term maintainability

### Check F1

离开当前对话上下文，这页以后还能看懂吗？

### Check F2

这次编辑是否保留了未来的复用价值？

### Check F3

如果以后再次更新，这个页面结构是否容易继续扩展？

### Check F4

这次编辑是否让系统更 coherent，而不只是更 verbose？

---

## Wiki 页专项检查

对于 `WIKI/` 下的编辑，还要额外检查：

- 页面是否清楚说明了 scope
- `compiled_from` 是否存在且有意义
- `confidence` 是否合理
- 页面是否回链到 nodes、problems 或 projects
- 页面是否明确属于 synthesis，而不是伪装成 base truth

---

## Node 页专项检查

对于 `KNOWLEDGE/` 下的编辑，还要额外检查：

- node boundary 是否仍然清楚
- 页面是否仍然 reusable
- 粒度是否依然合适
- facts 与 personal thoughts 是否保持分离
- 页面是否仍像一个 node，而不是 broad survey

---

## Career 资产专项检查

对于 `CAREER/` 下的编辑，还要额外检查：

- 这个 story 是否 grounded in real work or projects
- 是否清楚体现了 role relevance
- 是否避免 exaggeration
- 是否清楚说明了个人贡献
- 是否真正 professional usable

---

## Review outcome options

review 之后，一条更新通常应落到以下之一：

### Accept

页面可以直接保留。

### Accept with minor edits

页面整体可用，但还需要小清理。

### Needs revision

页面有价值，但仍有重要问题待修。

### Reject

页面误导性太强、结构错误，或者不够有用。

---

## 最后原则

一个好的 LLM-generated update，不只是 polished text。

它应该是一个：

- trustworthy
- well-placed
- structurally consistent

的长期知识系统贡献。
