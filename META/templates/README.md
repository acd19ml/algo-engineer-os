# Templates

知识库的最小模板。创建新内容时参考这些结构。

## 可用模板

| 模板 | 用途 |
|---|---|
| [node_README.template.md](./node_README.template.md) | KNOWLEDGE 节点（实际形态规则在 `META/policies/node_form.md`） |
| [self_check.template.md](./self_check.template.md) | KNOWLEDGE/_self_check/`<domain>`.md 自检题 deck |
| [podcast_script.template.md](./podcast_script.template.md) | PODCAST/ 播客脚本 |
| [problem_README.template.md](./problem_README.template.md) | PROBLEMS 问题页 |
| [project_README.template.md](./project_README.template.md) | PROJECTS 项目页 |
| [runbook_entry.template.md](./runbook_entry.template.md) | WORK/runbooks/`<domain>`/runbook.md 单条症状导向条目 |
| [design_commitment_pattern.template.md](./design_commitment_pattern.template.md) | WORK/design-commitment-patterns/`<domain>`/`<slug>`.md 设计前候选不变量 |
| [design_commitment.template.md](./design_commitment.template.md) | PROJECTS/`<project>`/design/commitments.md 项目内设计承诺 |

## 使用原则

- 模板是最小结构，不是最大结构。只填有内容的部分。
- 不要创建空 section。没有内容就删掉那个 section。
- KNOWLEDGE 节点的实际形态规则**不在模板里**——模板只是占位。形态规则在 `META/policies/node_form.md` + `META/llm/few_shots/node_form.example.md`。

## 写之前的必读

| 写什么 | 必读规则 |
|---|---|
| KNOWLEDGE 节点 | `META/policies/node_form.md` + few-shot |
| _self_check deck | `META/policies/self_check.md` |
| PODCAST 脚本 | `META/policies/podcast_script.md` + few-shot |
| runbook 条目 | `WORK/runbooks/<domain>/README.md` + `META/templates/runbook_entry.template.md` |
| design commitment pattern | `WORK/design-commitment-patterns/README.md` + `META/templates/design_commitment_pattern.template.md` |
| 项目 design commitment | 项目 README / design 文档 + `META/templates/design_commitment.template.md` |
