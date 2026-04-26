# INBOX

学习时随手丢东西的地方。零结构要求。

## 文件夹约定（重要）

`INBOX/` 下面**唯一一个有特殊语义的子文件夹**是 `dialogue_logs/`：

```
INBOX/<topic>/
├── dialogue_logs/      ← LLM 入库源（每个 log 都会被提炼成 KNOWLEDGE 节点 + 自检题）
├── notes/              ← 你看的笔记，参考材料
├── notes_zh/           ← 同上
├── ppts/               ← 课件，参考材料
├── tutorials/          ← 教程，参考材料
└── *.pdf / *.md        ← 任意杂物
```

- **`dialogue_logs/*.md`** = 你和 LLM 学习时的对话记录。**这是入库主源**。LLM triage 时只从这里提炼知识进入 `KNOWLEDGE/`。
- **其它子文件夹**（`notes/`、`ppts/`、`tutorials/`、cheat sheet 等）= 学习过程辅助材料。LLM 可以读它们做事实核对，**但不从这里提取知识入库**。原因：你看了/抄了 ≠ 你学会了。只有对话过程才能证明你真的参与了思考。
- 例外：如果是论文 / 完整文档，LLM 可能 triage 到 `RAW_SOURCES/`。

## 规则

- 任何格式都行：对话 log、链接、截图、代码、问题、粗读笔记
- 文件名随意
- 子目录随意（按课程 / 按 topic / 按日期都行）

## 处理方式

你不需要手动整理。

把 `META/llm/` 目录 + `META/REGISTRY.md` + `INBOX/` 交给 LLM，LLM 按 `META/llm/triage.md` 自动分流。

整理后 LLM 会输出一份 **Triage Report**，告诉你：
- 建/改了哪些文件
- 4 类待你执行的建议（勾 TRACKS / 改 skill-gap / 实习挖掘 nudge / 横向对比触发）

被处理过的对话 log 会在文件顶部加 `<!-- PROCESSED: YYYY-MM-DD -->` 标记，默认不删除。
