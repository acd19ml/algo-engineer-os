# META

规则层。定义知识库如何运作、如何维护。

## 目录结构

```
META/
├── REGISTRY.md         全局索引（已有节点、问题、项目清单）
├── llm/                LLM 维护上下文包
│   ├── CONTEXT.md      系统全貌、ownership matrix、规则
│   └── triage.md       INBOX 处理流程 + Triage Report 模板
├── templates/          最小页面模板
│   ├── node_README.template.md
│   ├── problem_README.template.md
│   └── project_README.template.md
└── policies/           稳定规则
    ├── source_of_truth.md
    ├── naming_convention.md
    └── node_granularity.md
```

## 使用

### 让 LLM 整理 INBOX
把 `META/llm/` + `META/REGISTRY.md` + `INBOX/` 交给 LLM。LLM 读 CONTEXT.md → REGISTRY.md → triage.md → INBOX，按规则处理并输出 Triage Report。

### 你手动维护
- 你可以改 META/ 下任何文件（policies、templates、CONTEXT、triage、README）
- LLM 不会写 META/

### 解决信息冲突
按 `policies/source_of_truth.md` 的优先级判断。
