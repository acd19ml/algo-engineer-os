# Templates

这个目录存放创建新仓库对象时可直接复用的模板。

如果这个仓库是一个长期系统，那么反复出现的对象就不应该每次都从零写起。

templates 的作用，是让系统保持：

- consistent
- faster to extend
- easier to maintain
- easier for both humans and LLMs to use

---

## 这个目录是做什么的

`META/templates/` 用于标准化常见页面和目录结构。

Examples:

- knowledge node pages
- problem pages
- project pages
- wiki pages
- career story pages
- recurring LLM workflow prompts

它的核心价值是：  
不用每次重新设计结构，而是从稳定起点开始。

---

## 为什么 templates 重要

没有 templates，仓库通常会逐渐漂移成：

- section naming 不一致
- 常见 section 经常缺失
- 大量重复思考结构问题
- 相似页面之间出现难以解释的差异

templates 的存在，就是为了减少这种 drift。

它们尤其重要于这些场景：

- 你会长期创建很多相似页面
- 你希望 LLM 能协助起草
- 你希望未来更新保持可预测

---

## 当前核心模板

### `node_README.template.md`

用于 reusable knowledge node。

### `problem_README.template.md`

用于 problem-centered page。

### `project_README.template.md`

用于 project page。

### `wiki_page.template.md`

用于 compiled wiki page。

### `career_story.template.md`

用于把真实项目 / 工作转成职业表达资产。

### `paper_ingestion_prompt.template.md`

用于把“新论文 / 原文链接 -> 仓库分层对象”的维护请求，变成可重复使用的 LLM 提示词模板。
它不是页面 skeleton，而是 workflow prompt template。

---

## 如何使用 templates

### 对人类维护者

创建新页面时：

1. 先选对对象类型
2. 复制对应 template
3. 填入内容
4. 删除那些确实不需要的 section
5. 除非有充分理由，否则尽量保留整体结构

### 对 LLM 维护

如果没有额外指令：

- 页面模板应被视为默认 page skeleton
- prompt template 应被视为默认 workflow request skeleton

LLM 应：

- 从 template 起草
- 保留必要 sections
- 避免把不同页面类型压成同一种风格

---

## 设计原则

### 1. Template 应该有用，而不是压迫式

template 的目标是引导结构，不是强迫填充无意义的 boilerplate。

### 2. Template 应反映页面用途

不同层需要不同模板，不能一套结构打天下。

### 3. Template 应保持轻量

即使内容还不完整，也应该容易开始。

### 4. Template 应改善一致性

它的核心目标，是减少结构漂移。

### 5. Template 的演化应谨慎

如果很多页面都需要同一种结构调整，优先改 template，  
而不是让以后每页都临时补丁式处理。

---

## 什么时候新增一个 template

在这些情况下，可以新增 template：

- 某种新页面类型开始反复出现
- 这种页面有稳定用途
- 结构已经重要到值得标准化

如果只是一次性页面类型，就先不要急着加 template。

---

## 相关入口

- [Meta](../README.md)
- [Policies](../policies/README.md)
- [LLM Rules](../llm/README.md)
