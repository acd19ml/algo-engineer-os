# LLM Rules

LLM 维护知识库的上下文包。

## 阅读流程（分阶段加载）

LLM 启动后**只读两个文件**：

1. `META/llm/triage.md` —— Stage-0 入口，含 INBOX 处理流程 + 决策树 + Triage Report 模板 + 分阶段加载表
2. `META/REGISTRY.md` —— 当前已有什么

后续按 triage.md 里的 stage 加载表，**触发什么读什么**。不要一次性全读。

## 文件

| 文件 | 作用 |
|---|---|
| [triage.md](./triage.md) | Stage-0 入口：流程、决策树、分阶段加载表 |
| [CONTEXT.md](./CONTEXT.md) | Stage-1 必读：ownership matrix、引用方向、节点是自含 artifact |
| [few_shots/](./few_shots/) | 具体范例（形态参考）。配合 `META/policies/` 的抽象规则使用 |

## 输出契约

每次整理结束**必须**输出 Triage Report，格式见 `triage.md` 末尾模板。Report 包含 4 个固定 section：

1. ✅ 已建 / 已改
2. 🔔 3 类联动建议（TRACKS / 实习挖掘 / 横向对比）
3. ⚠️ 冲突 / 待确认
4. 📊 本次统计
