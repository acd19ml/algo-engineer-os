# LLM Rules

LLM 维护知识库的完整上下文包。

## 使用方式

把 `META/llm/` + `META/REGISTRY.md` + `INBOX/` 交给 LLM，LLM 自动整理并输出 Triage Report。

## 文件

| 文件 | 作用 |
|---|---|
| [CONTEXT.md](./CONTEXT.md) | 系统全貌、ownership matrix、入库源唯一规则、引用方向、节点稀疏度、自检题来源限定 |
| [triage.md](./triage.md) | INBOX 处理流程、决策树、Triage Report 模板 |

## 阅读顺序

1. `CONTEXT.md` — 理解系统约束（最重要的是 §1 ownership matrix）
2. `META/REGISTRY.md` — 当前已有什么
3. `triage.md` — 处理流程
4. `INBOX/` — 开始工作

## 输出契约

每次整理结束**必须**输出 Triage Report，格式见 `triage.md` 末尾模板。Report 包含 4 个固定 section：

1. ✅ 已建 / 已改
2. 🔔 4 类联动建议（TRACKS / skill-gap / 实习挖掘 / 横向对比）
3. ⚠️ 冲突 / 待确认
4. 📊 本次统计
