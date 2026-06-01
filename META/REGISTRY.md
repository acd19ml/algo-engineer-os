# Registry

知识库全局索引。LLM 在处理 INBOX 前必须先读，避免重复创建。

> 此文件由 LLM 在每次整理后自动同步。人工也可改。

---

## KNOWLEDGE nodes

| id | 路径 | type |
|---|---|---|
| representation-learning-xor | `KNOWLEDGE/ml/representation-learning-xor/` | concept |
| gradient-flow-deep-networks | `KNOWLEDGE/ml/gradient-flow-deep-networks/` | mechanism |
| initialization-and-normalization | `KNOWLEDGE/ml/initialization-and-normalization/` | method |
| residual-connections | `KNOWLEDGE/ml/residual-connections/` | mechanism |
| depthwise-separable-convolution | `KNOWLEDGE/vision/depthwise-separable-convolution/` | method |
| l-smooth-gradient-descent | `KNOWLEDGE/optimization/l-smooth-gradient-descent/` | concept |
| nonconvex-gd-convergence | `KNOWLEDGE/optimization/nonconvex-gd-convergence/` | concept |
| nlp-pipeline-tokenization | `KNOWLEDGE/nlp/nlp-pipeline-tokenization/` | concept |
| bpe-tokenization | `KNOWLEDGE/nlp/bpe-tokenization/` | method |
| classification-training-loop | `KNOWLEDGE/pytorch/classification-training-loop/` | workflow |
| cross-entropy-loss | `KNOWLEDGE/pytorch/cross-entropy-loss/` | concept |
| neural-language-model | `KNOWLEDGE/nlp/neural-language-model/` | method |
| padding-and-attention-mask | `KNOWLEDGE/nlp/padding-and-attention-mask/` | mechanism |
| task-oriented-dialogue-system | `KNOWLEDGE/nlp/task-oriented-dialogue-system/` | system |
| ner-sequence-modeling | `KNOWLEDGE/nlp/ner-sequence-modeling/` | method |
| answer-form-for-mechanisms | `KNOWLEDGE/methodology/answer-form-for-mechanisms/` | capability |
| qkv-three-matrix-design | `KNOWLEDGE/transformer/qkv-three-matrix-design/` | mechanism |
| multi-head-attention | `KNOWLEDGE/transformer/multi-head-attention/` | mechanism |
| kv-cache | `KNOWLEDGE/transformer/kv-cache/` | mechanism |
| agent-engineer-ability | `KNOWLEDGE/agent/agent-engineer-ability/` | capability |
| context-engineering | `KNOWLEDGE/agent/context-engineering/` | capability |
| harness | `KNOWLEDGE/agent/harness/` | capability |
| harness-practice | `KNOWLEDGE/agent/harness-practice/` | system |
| multi-agent | `KNOWLEDGE/agent/multi-agent/` | capability |
| structured-output | `KNOWLEDGE/agent/structured-output/` | capability |
| posttrain-practice-roadmap | `KNOWLEDGE/training/posttrain-practice-roadmap/` | workflow |
| continue-pretrain-vs-finetune | `KNOWLEDGE/training/continue-pretrain-vs-finetune/` | methodology |
| sft-rl-relationship | `KNOWLEDGE/training/sft-rl-relationship/` | concept |
| lora | `KNOWLEDGE/training/lora/` | method |
| long-context-rl | `KNOWLEDGE/training/long-context-rl/` | method |
| sft-data-size | `KNOWLEDGE/training/sft-data-size/` | methodology |
| rlhf-dpo-grpo | `KNOWLEDGE/training/rlhf-dpo-grpo/` | concept |
| agent-context-compaction | `KNOWLEDGE/agent/agent-context-compaction/` | system |
| agent-permission-system | `KNOWLEDGE/agent/agent-permission-system/` | system |
| agent-role-isolation | `KNOWLEDGE/agent/agent-role-isolation/` | system |
| agent-tool-design | `KNOWLEDGE/agent/agent-tool-design/` | capability |
| agent-memory-system | `KNOWLEDGE/agent/agent-memory-system/` | system |
| agent-system-prompt | `KNOWLEDGE/agent/agent-system-prompt/` | capability |
| agentops-vs-opsagent | `KNOWLEDGE/agent/agentops-vs-opsagent/` | concept |
| multi-agent-rca-paradigm | `KNOWLEDGE/agent/multi-agent-rca-paradigm/` | system |
| agent-failure-attribution | `KNOWLEDGE/agent/agent-failure-attribution/` | research-direction |
| agent-anomaly-taxonomy | `KNOWLEDGE/agent/agent-anomaly-taxonomy/` | framework |
| agent-failure-trajectory-dataset | `KNOWLEDGE/agent/agent-failure-trajectory-dataset/` | infrastructure |
| heuristic-learning | `KNOWLEDGE/agent/heuristic-learning/` | concept |
| memory-architecture-thesis | `KNOWLEDGE/agent/memory-architecture-thesis/` | concept |
| agent-skills-closed-loop | `KNOWLEDGE/agent/agent-skills-closed-loop/` | system |
| agent-memory-cascading-update | `KNOWLEDGE/agent/agent-memory-cascading-update/` | research-direction |
| claude-md-rule-design | `KNOWLEDGE/agent/claude-md-rule-design/` | method |
| model-boundary-probing | `KNOWLEDGE/agent/model-boundary-probing/` | capability |
| agent-evaluation-harness | `KNOWLEDGE/agent/agent-evaluation-harness/` | system |
| tool-call-repair-harness | `KNOWLEDGE/agent/tool-call-repair-harness/` | system |
| agentic-rag-vs-long-context | `KNOWLEDGE/agent/agentic-rag-vs-long-context/` | system |
| rag-failure-diagnosis | `KNOWLEDGE/agent/rag-failure-diagnosis/` | workflow |
| rag-query-rewriting | `KNOWLEDGE/agent/rag-query-rewriting/` | method |
| agentic-rag-planning-cache | `KNOWLEDGE/agent/agentic-rag-planning-cache/` | method |
| architecture-design-six-steps | `KNOWLEDGE/methodology/architecture-design-six-steps/` | methodology |
| three-tier-decision-docs | `KNOWLEDGE/methodology/three-tier-decision-docs/` | methodology |
| ai-product-decision-four-questions | `KNOWLEDGE/methodology/ai-product-decision-four-questions/` | methodology |
| sft-loss-signal-allocation | `KNOWLEDGE/training/sft-loss-signal-allocation/` | methodology |
| sft-training-strategy | `KNOWLEDGE/training/sft-training-strategy/` | methodology |
| sft-data-sourcing | `KNOWLEDGE/training/sft-data-sourcing/` | methodology |
| sft-data-quality | `KNOWLEDGE/training/sft-data-quality/` | methodology |
| small-model-harness-engineering | `KNOWLEDGE/agent/small-model-harness-engineering/` | system |
| cache-aware-agent-loop | `KNOWLEDGE/agent/cache-aware-agent-loop/` | system |
| hierarchical-agent-memory | `KNOWLEDGE/agent/hierarchical-agent-memory/` | system |

### 节点形态状态

| 形态 | 节点数 | 说明 |
|---|---|---|
| ✅ 新形态（因果叙述 + 反事实） | 65（全部） | 所有节点都已按 `META/policies/node_form.md` 重写 |
| ⚠️ 旧形态 | 0 | 已全部清零 |

---

## Self-check decks

| domain | 路径 | 状态 |
|---|---|---|
| ml | `KNOWLEDGE/_self_check/ml.md` | 完整（4 节点 + 跨节点） |
| nlp | `KNOWLEDGE/_self_check/nlp.md` | 完整（6 节点 + 跨节点） |
| optimization | `KNOWLEDGE/_self_check/optimization.md` | 完整（2 节点 + 跨节点） |
| pytorch | `KNOWLEDGE/_self_check/pytorch.md` | 完整（2 节点 + 跨节点） |
| vision | `KNOWLEDGE/_self_check/vision.md` | 完整（1 节点） |
| methodology | `KNOWLEDGE/_self_check/methodology.md` | 完整（4 节点 + 跨节点） |
| transformer | `KNOWLEDGE/_self_check/transformer.md` | 完整（3 节点 + 跨节点） |
| agent | `KNOWLEDGE/_self_check/agent.md` | 完整（32 节点 + 跨节点：含 memory-architecture-thesis / heuristic-learning / agent-skills-closed-loop / agent-memory-cascading-update / claude-md-rule-design / 模型边界探测 / Agent 评估 Harness / 工具调用修复 Harness / RAG 与 Agentic RAG + 小模型 Harness / 缓存感知 Agent 循环 / 层级 Agent 记忆 + procedural memory object shape 跨节点深题） |
| training | `KNOWLEDGE/_self_check/training.md` | 完整（11 节点 + 跨节点：新增 SFT 数据来源 / 数据质量 / 训练策略 / loss 信号分配） |

---

## PODCAST

| domain | 路径 | 状态 |
|---|---|---|
| —— | `PODCAST/README.md` | 框架说明 |

（暂无具体脚本。用户请求 "做成播客脚本" 或 "intro 一下未学的 X" 时由 LLM 写。）

---

## PROBLEMS

| id | 路径 | status |
|---|---|---|
| agent-memory-architecture | `PROBLEMS/agent-memory-architecture/` | active |
| agent-harness-boundary-map | `PROBLEMS/agent-harness-boundary-map/` | active |

> `agent-memory-architecture/`：Claude Code（6 层 + LLM 路由）vs OpenClaw（2 层 + SQLite 混合搜索）vs 学术轴（Ledger+Views+Policy 三件套 / AWM 程序性记忆）vs **OpenViking（虚拟 FS + 三层加载 + 层级检索，2026-05-27 新增）** 四路横向对比。保留两套系统的完整 mermaid + 代码 + 限制表 + Hybrid Fusion 公式，供面试 / CV 引用。
>
> `agent-harness-boundary-map/`：Context / Evaluation / Tool Call Repair / Memory-Skill / Boundary Probing 五类 Harness 的失败信号、干预点、确定性边界、观测指标与删除条件横向对比，供 Agent 面试与系统设计回答复用。

---

## PROJECTS

| id | 路径 | type | status |
|---|---|---|---|
| qiniu-zeroops-rca-agent | `PROJECTS/work/qiniu-zeroops-rca-agent/` | work | done |
| neo-official-support-agent | `PROJECTS/work/neo-official-support-agent/` | work | **in-progress** |
| awm-mechanism-audit | `PROJECTS/research/awm-mechanism-audit/` | research | done |
| selective-transfer-memory | `PROJECTS/research/selective-transfer-memory/` | research | done |

> `qiniu-zeroops-rca-agent/` 含 4 份文档：`README.md`（决策复盘）+ `system-anatomy.md`（系统解剖）+ `agent-subsystem.md`（Agent 子系统解剖）+ `interview-defense-matrix.md`（挑战防御矩阵 · living）
>
> `neo-official-support-agent/` 已完成全周期设计（M0-M13）：设计阶段（PRD→技术方向→安全架构→系统架构→实现契约→工程计划）、验证阶段（Eval 体系→运行验证）、收敛阶段（方法论提取→playbook）。prototype eval：mocked oracle 100/100、LLM router 四档横扫 critical_bypass=0 跨全档、14B+ 98/100（main）+ 7/7（T1 heldout）。项目事实：2025.02-2025.07，一人负责产品方案；Neo 官网原无独立客服；当前不能声称已上线或有业务降本数据。生产阶段（M9-M13）已设计未执行。
>
> `awm-mechanism-audit/`（research）：AWM @ Mind2Web 复现+机制审计，4 个 finding（6-18% 影响窗口 / abstraction ≠ better execution / action-mode redirection / workflow-family mismatch）+ partial condition-dependent 结论。**支撑 CV "Agent Memory 自主研究项目" 第 1 条 bullet**。
>
> `selective-transfer-memory/`（research）：HotpotQA → 2WikiMultiHopQA pilot，matched/mismatched 配对设计 + 两次受控修复（Source Rerouting + Operator Repair）。**支撑 CV "Agent Memory 自主研究项目" 第 2 条 bullet**。

---

## RAW_SOURCES

| id | 路径 | type |
|---|---|---|
| jd-and-interviews | `RAW_SOURCES/jd-and-interviews/` | external |
| conference-talks | `RAW_SOURCES/conference-talks/` | external |
| articles | `RAW_SOURCES/articles/` | external |
| research-deliverables | `RAW_SOURCES/research-deliverables/` | internal |
| dialogues | `RAW_SOURCES/dialogues/` | internal |
| qiniu-internship-artifacts | `RAW_SOURCES/qiniu-internship-artifacts/` | internal |

> `conference-talks/` 含 `AgentOS_AgentOps_report.md`（2025 CCF ChinaSoft，裴昶华），已拆到 5 个 agent 节点：agentops-vs-opsagent / multi-agent-rca-paradigm / agent-failure-attribution / agent-anomaly-taxonomy / agent-failure-trajectory-dataset
>
> `articles/`（新增）：12 篇公众号 / 博客原文（Claude Code / OpenClaw / Hermes / Harness / Sandbox / Heuristic Learning 主题）。8 篇已完整蒸馏到 KB，3 篇 PENDING 等触发主题节点时回头读，1 篇部分蒸馏（harness-practice 章 2-12 待补）
>
> `research-deliverables/`（新增）：从 INBOX 升上来的 AWM + selective-transfer 研究原件（LaTeX / .bib / speaker notes）。`PROJECTS/research/` 已派生项目页，原件作为不可重新生成的 artifact 长期保留
>
> `dialogues/`（新增）：含 `conversation_01.md`（22 节人类记忆 ↔ AI 记忆深度对话）。核心命题已蒸馏到 `KNOWLEDGE/agent/memory-architecture-thesis/` 等节点；保留原对话作为"用户参与思考"的证据
>
> `qiniu-internship-artifacts/`（新增）：从 INBOX 升上来的 design.md / demo.md / 复盘文档.md。`PROJECTS/work/qiniu-zeroops-rca-agent/` 已派生 4 份文档，原件保留以备面试官追问"最初的 design 长什么样"

---

## CAREER

| 文件 | 作用 | 维护方 |
|---|---|---|
| `CAREER/cv.md` | 简历（从 PROJECTS 派生的 STAR 证据汇）；`interview-bank` / `target-roles` / `applications` / `skill-gap` 已退场，见 `CAREER/README.md` | 你 |

---

## WORK

| 路径 | 状态 |
|---|---|
| `WORK/` | 可复用工程实践层：`runbooks/` 反应式症状排查，`design-commitment-patterns/` 预防式候选不变量，`playbooks/` 可复用执行 SOP |

---

## WORK runbooks

症状导向的 agent 故障排查手册。和 KNOWLEDGE 节点的区别：节点写"概念为什么是这样"，runbook 写"我看到了 X，下一步做什么"。条目编号 P-XXX 全局递增，不按 domain 重置。

| id | 路径 | 条目数 | 状态 |
|---|---|---|---|
| agent-runbook | `WORK/runbooks/agent/` | 42（P-001 ~ P-042） | growing |

> 已按 agent 生命周期拆子目录（42 条 > 30 条阈值触发）：perception（2）/ planning（4）/ tool-use（16）/ context（4）/ execution（9）/ memory（2）/ reliability（5）。P-XXX 全局单调递增，不按子目录重置。
>
> 当前 42 条来源：
> - P-001 ~ P-008：`[[small-model-harness-engineering]]`（小模型工具调用故障域）
> - P-009 ~ P-013：`[[structured-output]]`（结构化输出 6 层）
> - P-014 ~ P-018：`[[cache-aware-agent-loop]]`（前缀缓存命中率作为成本杠杆）
> - P-019：`[[rag-failure-diagnosis]]`（RAG 5 步诊断流）
> - P-020 / P-021：`[[agent-tool-design]]`（工具设计三原则）
> - P-022 ~ P-025：`[[agent-permission-system]]`（分层规则 + 两阶段评审）
> - P-026：`[[agent-context-compaction]]`（四层压缩流水线 + 熔断器）
> - P-027 / P-028：`[[harness-practice]]`（上下文焦虑 + 自我表扬偏差）
> - P-029：`[[agent-role-isolation]]`（按阶段拆 agent + 三维隔离）
> - P-030 / P-031：`[[agent-system-prompt]]`（binary 规则 + 防虚假声明）
> - P-032 / P-033：`[[harness]]`（文件编辑循环 + 退出前验证）
> - P-034：`[[claude-md-rule-design]]`（12 条规则 + 200 行天花板）
> - P-035 / P-036：`[[multi-agent]]`（任务委派四要素 + 序列化执行）
> - P-037 / P-038：`[[tool-call-repair-harness]]`（先校验再修复 + 语义化类型）
> - P-039：`[[rag-query-rewriting]]`（路由先于改写）
> - P-040：`[[agent-memory-system]]`（时效标注 + 过期警告）
> - P-041：`[[agent-skills-closed-loop]]`（Skill 即时维护机制）
> - P-042：`[[agentic-rag-planning-cache]]`（模板误命中检测）
>
> ⚠️ 方案互冲保留：P-006（本地推理 OOM 压缩）vs P-014/P-015（云 API 缓存 append-only）。按是否关心缓存成本选。

---

## WORK design commitment patterns

设计前调用的候选不变量。由 runbook 症状簇压缩而来；项目采纳后再实例化成 `PROJECTS/<project>/design/commitments.md` 或项目仓库内 DC。

| id | 路径 | 来源簇 | 状态 |
|---|---|---|---|
| respond-single-output-channel | `WORK/design-commitment-patterns/agent/respond-single-output-channel.md` | P-008 + P-001 方案 3 + `[[small-model-harness-engineering]]` | candidate |
| prerequisite-gate-before-terminal-tool | `WORK/design-commitment-patterns/agent/prerequisite-gate-before-terminal-tool.md` | P-003 + `[[small-model-harness-engineering]]` | candidate |
| retry-budget-hard-cap | `WORK/design-commitment-patterns/agent/retry-budget-hard-cap.md` | P-007 + P-003 + P-011（重试约束）+ `[[small-model-harness-engineering]]` | candidate |
| tool-error-split-counting | `WORK/design-commitment-patterns/agent/tool-error-split-counting.md` | P-004 + `[[small-model-harness-engineering]]` | candidate |
| reasoning-output-decoupling | `WORK/design-commitment-patterns/agent/reasoning-output-decoupling.md` | P-009 + P-010 + `[[structured-output]]` | candidate |
| business-rule-validation-layer | `WORK/design-commitment-patterns/agent/business-rule-validation-layer.md` | P-011 + `[[structured-output]]` | candidate |
| immutable-prefix-append-only-log | `WORK/design-commitment-patterns/agent/immutable-prefix-append-only-log.md` | P-014 + P-012 + `[[cache-aware-agent-loop]]` | candidate |
| fail-loud-on-bad-json | `WORK/design-commitment-patterns/agent/fail-loud-on-bad-json.md` | P-018 + `[[cache-aware-agent-loop]]` | candidate |
| constraint-at-decision-point | `WORK/design-commitment-patterns/agent/constraint-at-decision-point.md` | P-020 + `[[agent-tool-design]]` | candidate |
| tool-output-budget-with-pointer | `WORK/design-commitment-patterns/agent/tool-output-budget-with-pointer.md` | P-021 + `[[agent-tool-design]]` | candidate |
| three-tier-deny-overrides-allow | `WORK/design-commitment-patterns/agent/three-tier-deny-overrides-allow.md` | P-022 + `[[agent-permission-system]]` | candidate |
| reviewer-isolation-fail-closed | `WORK/design-commitment-patterns/agent/reviewer-isolation-fail-closed.md` | P-023 + `[[agent-permission-system]]` | candidate |
| high-cost-rules-in-code | `WORK/design-commitment-patterns/agent/high-cost-rules-in-code.md` | P-024 + `[[agent-permission-system]]` | candidate |
| non-bypassable-bottom-line | `WORK/design-commitment-patterns/agent/non-bypassable-bottom-line.md` | P-025 + `[[agent-permission-system]]` | candidate |
| background-agent-excluded-from-recovery-triggers | `WORK/design-commitment-patterns/agent/background-agent-excluded-from-recovery-triggers.md` | P-026 + `[[agent-context-compaction]]` | candidate |
| mandatory-verification-before-completion | `WORK/design-commitment-patterns/agent/mandatory-verification-before-completion.md` | P-028 + P-033 + P-031 + `[[harness]]` `[[harness-practice]]` | candidate |
| multi-agent-three-dimension-isolation | `WORK/design-commitment-patterns/agent/multi-agent-three-dimension-isolation.md` | P-029 + `[[agent-role-isolation]]` | candidate |
| agent-config-binary-rules-bounded | `WORK/design-commitment-patterns/agent/agent-config-binary-rules-bounded.md` | P-030 + P-034 + `[[claude-md-rule-design]]` `[[agent-system-prompt]]` | candidate |
| serialize-writes-to-shared-state | `WORK/design-commitment-patterns/agent/serialize-writes-to-shared-state.md` | P-036 + `[[multi-agent]]` | candidate |
| schema-validate-before-repair | `WORK/design-commitment-patterns/agent/schema-validate-before-repair.md` | P-037 + `[[tool-call-repair-harness]]` | candidate |
| semantic-typed-schema-fields | `WORK/design-commitment-patterns/agent/semantic-typed-schema-fields.md` | P-038 + `[[tool-call-repair-harness]]` | candidate |
| route-before-rewrite | `WORK/design-commitment-patterns/agent/route-before-rewrite.md` | P-039 + `[[rag-query-rewriting]]` | candidate |
| memory-temporal-annotation | `WORK/design-commitment-patterns/agent/memory-temporal-annotation.md` | P-040 + P-041 + `[[agent-memory-system]]` `[[agent-skills-closed-loop]]` | candidate |

### WORK/playbooks

| id | 路径 | 源 | status |
|---|---|---|---|
| detection-hardening-loop | `WORK/playbooks/detection-hardening-loop/` | `[[PROJECTS/work/neo-official-support-agent]]` 复盘 | active |

### WORK/verification-habits

| id | 路径 | 源 | status |
|---|---|---|---|
| verification-habits | `WORK/verification-habits/` | `[[PROJECTS/work/neo-official-support-agent]]` 复盘 + `[[harness-practice]]` + `[[model-boundary-probing]]` | active |

---

## REPRO_INDEX

（暂无条目）

---

## TRACKS

| id | 路径 | 类型 | 状态 |
|---|---|---|---|
| sprint-2026-summer | TRACKS/active/sprint-2026-summer.md | 临时 | active |
| agent-engineer | TRACKS/roadmap/agent-engineer.md | 长期 | **待重写** |

---

## META（规则层）

| 文件 | 作用 |
|---|---|
| `META/llm/triage.md` | Stage-0 入口（LLM 启动必读） |
| `META/llm/CONTEXT.md` | Stage-1 必读（ownership matrix） |
| `META/llm/few_shots/node_form.example.md` | KNOWLEDGE 节点形态范例 |
| `META/llm/few_shots/podcast_script.example.md` | 播客脚本形态范例 |
| `META/policies/node_form.md` | 节点形态规则 |
| `META/policies/self_check.md` | 自检题规则 |
| `META/policies/podcast_script.md` | 播客脚本规则 |
| `META/policies/source_of_truth.md` | 信息冲突优先级 |
| `META/policies/naming_convention.md` | 命名规则 |
| `META/policies/node_granularity.md` | 节点粒度判断 |
| `META/templates/design_commitment_pattern.template.md` | design commitment pattern 形态 |
| `META/templates/design_commitment.template.md` | 项目内 design commitment 形态 + few-shot |
| `META/templates/*` | 各类内容模板 |

---

## Ownership 速查

> **权威定义在 `META/llm/CONTEXT.md` §1**；下表为速查镜像，冲突以 CONTEXT §1 为准。

| 区域 | 维护方 |
|---|---|
| INBOX、TRACKS、CAREER/cv.md、META | 你 |
| KNOWLEDGE、KNOWLEDGE/_self_check、PROBLEMS、PROJECTS、RAW_SOURCES、REPRO_INDEX、WORK/runbooks、WORK/design-commitment-patterns、WORK/playbooks、PODCAST、REGISTRY | LLM 写入 |
| TRACKS 勾选 / 实习挖掘 / 横向对比 / 项目 design commitment 采纳 | LLM 在 Triage Report 建议，你执行 |
| PODCAST 写入 | LLM 写入但**仅在用户明确请求时** |

详见 `README.md` 的 Ownership Matrix 和 `META/llm/CONTEXT.md`。
