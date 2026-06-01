# META

规则层。定义知识库如何运作、如何维护。

## 目录结构

> 完整、最新的文件清单见 `META/REGISTRY.md` 的「META（规则层）」段（LLM 每次 triage 同步）。此处只给定位，不手抄文件列表——旧版就因手抄而漏列了 node_form / self_check / podcast_script policies 和全部 design_commitment 模板。

- `REGISTRY.md` — 全局索引（节点 / 问题 / 项目 / pattern 清单）
- `llm/triage.md` — Stage-0 启动必读（两条入口纪律 + INBOX 流程 + 分阶段加载表 + Report 模板）
- `llm/CONTEXT.md` — Stage-1（ownership matrix、引用方向、节点自含）
- `llm/few_shots/` — 形态范例（node_form / podcast_script）
- `policies/` — 稳定规则（node_form / self_check / podcast_script / source_of_truth / naming_convention / node_granularity）
- `templates/` — 页面与 design commitment 模板（node / problem / project / runbook_entry / self_check / podcast_script / design_commitment / design_commitment_pattern）

## 使用

### 让 LLM 整理 INBOX
把 `META/llm/` + `META/REGISTRY.md` + `INBOX/` 交给 LLM。LLM 读 CONTEXT.md → REGISTRY.md → triage.md → INBOX，按规则处理并输出 Triage Report。

### 你手动维护
- 你可以改 META/ 下任何文件（policies、templates、CONTEXT、triage、README）
- LLM 不会写 META/

### 解决信息冲突
按 `policies/source_of_truth.md` 的优先级判断。
