# META

规则层。定义知识库如何运作、如何维护。

---

## 目录结构

```
META/
├── REGISTRY.md      # 全局索引（已有节点、问题、项目清单）
├── llm/             # LLM 维护上下文包
│   ├── CONTEXT.md   # 自包含指令（结构、规则、模板、审查）
│   └── triage.md    # INBOX 分流规则
├── templates/       # 最小页面模板
│   ├── node_README.template.md
│   ├── problem_README.template.md
│   └── project_README.template.md
└── policies/        # 稳定的仓库级规则
    ├── source_of_truth.md
    ├── naming_convention.md
    └── node_granularity.md
```

## 如何使用

### 让 LLM 整理 INBOX

把 `META/llm/` + `META/REGISTRY.md` + `INBOX/` 交给 LLM。LLM 读 CONTEXT.md 获得完整指令，读 REGISTRY.md 了解现状，按 triage.md 执行分流。

### 手动创建内容

参考 `templates/` 下的最小模板。遵守 `policies/` 中的命名和粒度规范。

### 解决信息冲突

按 `policies/source_of_truth.md` 的优先级判断。
