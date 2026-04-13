# Paper Ingestion Prompt Template

用于把一篇新论文，或一个只包含原文链接的 source，按 Algo Engineer OS 的分层规则接入仓库。

这个模板默认面向“能读仓库、能直接编辑文件”的 LLM。
如果当前 LLM 不能直接改文件，可以要求它输出按文件路径分组的拟议改动。

---

## 什么时候用

在这些场景下使用：

- 你手里只有论文链接
- 你已经有 `RAW_SOURCES/` 下的论文入口页
- 你希望 LLM 不只是总结论文，而是把论文接入整个仓库
- 你希望 LLM 遵守 `source -> structure -> synthesis` 的顺序

---

## 先填这几个变量

- `{{SOURCE_INPUT}}`
  可以是：
  - `RAW_SOURCES/.../README.md` 路径
  - arXiv HTML 链接
  - arXiv PDF 链接
  - 其他论文原文链接

- `{{SOURCE_TYPE}}`
  可选值例如：
  - `raw_source_page`
  - `arxiv_html`
  - `arxiv_pdf`
  - `paper_link`
  - `mixed`

- `{{SCOPE}}`
  推荐可选值：
  - `source-only`
  - `source->refs`
  - `source->nodes`
  - `source->nodes->problems`
  - `source->nodes->problems->projects->repro`
  - `full-ingestion-except-wiki`
  - `full-ingestion-including-wiki`

- `{{KNOWN_RELATED_OBJECTS}}`
  选填。
  可以写你已经知道相关的 nodes / problems / projects。

- `{{NEW_NODE_POLICY}}`
  推荐可选值：
  - `reuse-first`
  - `allow-new-nodes-if-justified`
  - `do-not-create-new-nodes-without-review`

- `{{META_CHANGE_POLICY}}`
  推荐可选值：
  - `minimal`
  - `allow-if-justified`
  - `review-first`

- `{{WIKI_POLICY}}`
  推荐可选值：
  - `do-not-touch-wiki`
  - `update-existing-wiki-only`
  - `allow-new-wiki-if-justified`

- `{{OUTPUT_MODE}}`
  推荐可选值：
  - `edit-files-directly`
  - `propose-file-changes-only`

---

## 标准模板

```text
你正在维护 Algo Engineer OS。请把下面这篇新论文按仓库规则接入系统，而不是只写一份普通总结。

[Inputs]
- Source input: {{SOURCE_INPUT}}
- Source type: {{SOURCE_TYPE}}
- Scope: {{SCOPE}}
- Known related objects: {{KNOWN_RELATED_OBJECTS}}
- New node policy: {{NEW_NODE_POLICY}}
- meta.yaml change policy: {{META_CHANGE_POLICY}}
- Wiki policy: {{WIKI_POLICY}}
- Output mode: {{OUTPUT_MODE}}

[Repository rules you must follow]
1. 先遵守 source-of-truth hierarchy：
   RAW_SOURCES/ > KNOWLEDGE/*/meta.yaml > KNOWLEDGE/*/README.md > PROBLEMS/ > WIKI/ > DASHBOARDS/ > OUTPUT/
2. 如果我给你的只有原论文链接，你必须先读取原文，并优先创建或补全 RAW_SOURCES 下对应的论文入口页，再决定更高层更新。
3. 先更新低层，再更新高层。默认顺序是：
   RAW_SOURCES -> KNOWLEDGE refs / meta / README -> PROBLEMS -> PROJECTS -> REPRO_INDEX -> WIKI
4. 复用已有页面优先。只有在新增对象真的能提升结构清晰度时，才创建新页面。
5. 不要把 paper claim、个人判断和猜测写成一种声音。请显式区分：
   - paper claim
   - current repository-maintainer judgment
   - open question / uncertainty
6. 如果 sources 不足，宁可保留空白或 open question，也不要强行补全。
7. 如果要改 meta.yaml 中的关键关系字段，请保持最小改动，并明确说明依据。
8. 不要默认写 Wiki。只有当 Scope 或 Wiki policy 明确允许时，才更新或新建 WIKI 页面。
9. 优先做增量修改，不要大面积重写已有页面，除非页面结构明显错误。
10. 需要创建页面时，使用仓库中已有 templates 和 policies。

[What I want you to do]
1. 先判断这个 source 当前应该落在哪些层。
2. 检查仓库里是否已有相关 raw source page、knowledge nodes、problem pages、project pages、repro entries。
3. 给出一个很短的执行计划。
4. 按 Scope 做实际编辑或提出拟议编辑。
5. 每次新增或修改内容时，保持层次清楚：
   - raw extraction 放 RAW_SOURCES
   - references 放 refs/README.md
   - structural relations 放 meta.yaml
   - concept explanation 放 node README
   - judgments / caveats / open questions 放 thoughts/README.md 或问题页对应部分
6. 如果这篇论文值得拆成多个独立 nodes，请说明 node boundary 为什么这样划分。
7. 如果这篇论文更适合作为已有 node 的 refs 补充，而不是新建 node，也请明确说明。
8. 如果该论文会触发 problem page、project page 或 repro entry，请按最小有用原则补上。

[Preferred output format]
请按下面结构收尾：

1. Source handling
   - 你把 source 接到了哪里
   - 原始证据页新增或补充了什么

2. Structural updates
   - 新增或更新了哪些 nodes / problems / projects / repro entries
   - 每个对象为什么要新增或为什么只更新现有页

3. Uncertainty and review points
   - 哪些地方仍不确定
   - 哪些地方建议我人工 review

4. Files touched
   - 按文件路径列出变更
   - 每个文件一句话说明改动目的

[Important constraints]
- 不要把论文的一轮粗读直接伪装成成熟结论
- 不要把后续常识自动投射回论文原文
- 不要把 Wiki 当作 source of truth
- 不要为了“看起来完整”而制造不存在的 citations、experiments 或 repos
```

---

## 最小版模板

如果你不想每次都填很多变量，可以直接用这一版：

```text
把这篇新论文按 Algo Engineer OS 的规则接入仓库：
{{SOURCE_INPUT}}

要求：
- 先按 source-of-truth 规则处理 source，不要直接写普通总结
- 如果只有原文链接，先创建或补全 RAW_SOURCES 下的论文入口页
- 按 RAW_SOURCES -> KNOWLEDGE -> PROBLEMS -> PROJECTS -> REPRO_INDEX 的顺序增量更新
- 默认先不要写 WIKI
- 复用已有页面优先，不要随意重复建页
- 区分 paper claim、current judgment 和 open questions
- 如果要改 meta.yaml 的关键关系，请显式说明依据
- 最后按 files touched 总结你改了什么、为什么
```

---

## 使用建议

- 第一次接入新论文时，优先用 `full-ingestion-except-wiki`
- 如果你只想先把证据接入系统，用 `source-only` 或 `source->refs`
- 如果你已经知道它只会补充已有主题，把 `NEW_NODE_POLICY` 设成 `reuse-first`
- 如果你担心 LLM 乱改结构，把 `META_CHANGE_POLICY` 设成 `review-first`
- 如果这篇论文只是粗读阶段，不要急着允许它生成 WIKI

---

## 推荐搭配

使用这个模板前后，建议让 LLM 同时遵守这些文件：

- [META/llm/system_prompt.md](../llm/system_prompt.md)
- [META/llm/editing_rules.md](../llm/editing_rules.md)
- [META/llm/update_workflows.md](../llm/update_workflows.md)
- [META/policies/source_of_truth.md](../policies/source_of_truth.md)
- [META/policies/node_granularity.md](../policies/node_granularity.md)

如果只给 LLM 一个论文链接，这个模板的目标不是让它“总结论文”，而是让它“把论文按分层规则接入系统”。
