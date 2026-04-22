# LLM Rules

这个目录是 LLM 维护知识库的完整上下文包。

## 使用方式

把 `META/llm/` 目录 + `META/REGISTRY.md` + `INBOX/` 交给 LLM，LLM 即可自动整理知识库。

## 文件说明

| 文件 | 作用 |
|---|---|
| [CONTEXT.md](./CONTEXT.md) | 自包含的 LLM 指令：系统结构、规则、模板、编辑规范、审查清单 |
| [triage.md](./triage.md) | INBOX 分流规则：如何判断内容归属、执行整理、更新索引 |

## LLM 阅读顺序

1. 读 `CONTEXT.md` — 理解系统全貌和规则
2. 读 `META/REGISTRY.md` — 了解当前已有什么
3. 读 `triage.md` — 了解如何处理 INBOX
4. 读 `INBOX/` — 开始工作
