# TRACKS / active

有截止日期的临时任务。完成即删整个文件。

## 用法

每个文件 = 一个有 deadline 的任务集合。

## 当前

- `final-exam-prep.md` — 4.27 / 4.29 / 5.2 三门 final（考完即删）

## 这一层和 LLM 的关系

- **LLM 只读，不写**。结构、增删、勾选都你来。
- LLM 在 Triage Report 里会建议"本次入库覆盖了 active/X 的以下任务，建议你勾掉"。
- LLM 引用方向：tracks 页可以引用 KNOWLEDGE 节点；KNOWLEDGE 节点**不**反向引用 tracks（保证 knowledge 不依赖 tracks）。

## 删除规则

任务全部完成 → 删整个 .md 文件。临时性是这一层的语义。
