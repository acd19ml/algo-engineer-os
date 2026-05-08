# INBOX

学习时随手丢东西的地方。零结构要求。**临时层——你随时可以删**。

---

## 文件夹约定（重要）

`INBOX/` 下面**两个有特殊语义的子文件夹**是 `dialogue_logs/` 和 `internalized/`：

```
INBOX/<topic>/
├── dialogue_logs/      ← KNOWLEDGE 入库源（你和 LLM 学习对话的 log）
├── internalized/       ← KNOWLEDGE 入库源（你看视频/听播客/读资料后主动消化过的内容）
├── notes/              ← 你看的笔记，参考材料
├── notes_zh/           ← 同上
├── ppts/               ← 课件，参考材料
├── tutorials/          ← 教程，参考材料
└── *.pdf / *.md        ← 任意杂物
```

### 入库源（这两个能产出 KNOWLEDGE）

- **`dialogue_logs/*.md`** = 你和 LLM 学习时的对话记录。证明你参与了思考。
- **`internalized/*.md`** = 你看视频 / 听播客 / 读资料后主动**写下来或转述**的内容。区别于 `notes/` 的关键：你在主动消化、不是简单摘抄。

### 参考材料（不入库）

- `notes/`、`notes_zh/`、`ppts/`、`tutorials/` = 学习辅助材料。LLM 可以读它们做事实核对，**但不从这里提取知识入库**。
- 原因：你看了 / 抄了 ≠ 你学会了。只有对话或主动消化才能证明你真的参与了思考。
- 例外：论文 / 完整文档可能 triage 到 `RAW_SOURCES/`。

---

## 重要：INBOX 是临时层

KNOWLEDGE 节点是**自含 artifact**——节点 / `meta.yaml` 不会引用 INBOX 路径。所以 LLM 处理完 INBOX 后，你随时可以删 INBOX 内容，不会影响 KNOWLEDGE 层。

---

## 规则

- 任何格式都行：对话 log、链接、截图、代码、问题、粗读笔记、消化后的转述
- 文件名随意
- 子目录随意（按课程 / 按 topic / 按日期都行）

---

## 处理方式

你不需要手动整理。

开新 Claude session，喊 "整理 INBOX"。LLM 会按 `META/llm/triage.md` 处理。

整理后 LLM 输出一份 **Triage Report**，告诉你：

- 建/改了哪些文件
- 4 类待你执行的建议（勾 TRACKS / 改 skill-gap / 实习挖掘 nudge / 横向对比触发）

被处理过的 INBOX 文件会在顶部加 `<!-- PROCESSED: YYYY-MM-DD -->` 标记，默认不删——但你随时可以手动删整个 INBOX 子目录，不会影响 KNOWLEDGE。
