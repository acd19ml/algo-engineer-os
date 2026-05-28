# Registry

知识库全局索引。LLM 在处理 INBOX 前必须先读，避免重复创建。

> 此文件由 LLM 在每次整理后自动同步。人工也可改。

---

## KNOWLEDGE nodes

| id | 路径 | type | status |
|---|---|---|---|
| representation-learning-xor | `KNOWLEDGE/ml/representation-learning-xor/` | concept | learning |
| gradient-flow-deep-networks | `KNOWLEDGE/ml/gradient-flow-deep-networks/` | mechanism | learning |
| initialization-and-normalization | `KNOWLEDGE/ml/initialization-and-normalization/` | method | learning |
| residual-connections | `KNOWLEDGE/ml/residual-connections/` | mechanism | learning |
| depthwise-separable-convolution | `KNOWLEDGE/vision/depthwise-separable-convolution/` | method | learning |
| l-smooth-gradient-descent | `KNOWLEDGE/optimization/l-smooth-gradient-descent/` | concept | learning |
| nonconvex-gd-convergence | `KNOWLEDGE/optimization/nonconvex-gd-convergence/` | concept | learning |
| nlp-pipeline-tokenization | `KNOWLEDGE/nlp/nlp-pipeline-tokenization/` | concept | learning |
| bpe-tokenization | `KNOWLEDGE/nlp/bpe-tokenization/` | method | learning |
| classification-training-loop | `KNOWLEDGE/pytorch/classification-training-loop/` | workflow | learning |
| cross-entropy-loss | `KNOWLEDGE/pytorch/cross-entropy-loss/` | concept | learning |
| neural-language-model | `KNOWLEDGE/nlp/neural-language-model/` | method | learning |
| padding-and-attention-mask | `KNOWLEDGE/nlp/padding-and-attention-mask/` | mechanism | learning |
| task-oriented-dialogue-system | `KNOWLEDGE/nlp/task-oriented-dialogue-system/` | system | learning |
| ner-sequence-modeling | `KNOWLEDGE/nlp/ner-sequence-modeling/` | method | learning |
| answer-form-for-mechanisms | `KNOWLEDGE/methodology/answer-form-for-mechanisms/` | capability | stable |
| qkv-three-matrix-design | `KNOWLEDGE/transformer/qkv-three-matrix-design/` | mechanism | stable |
| multi-head-attention | `KNOWLEDGE/transformer/multi-head-attention/` | mechanism | stable |
| kv-cache | `KNOWLEDGE/transformer/kv-cache/` | mechanism | stable |
| agent-engineer-ability | `KNOWLEDGE/agent/agent-engineer-ability/` | capability | stable |
| context-engineering | `KNOWLEDGE/agent/context-engineering/` | capability | stable |
| harness | `KNOWLEDGE/agent/harness/` | capability | stable |
| harness-practice | `KNOWLEDGE/agent/harness-practice/` | system | stable |
| multi-agent | `KNOWLEDGE/agent/multi-agent/` | capability | stable |
| structured-output | `KNOWLEDGE/agent/structured-output/` | capability | stable |
| posttrain-practice-roadmap | `KNOWLEDGE/training/posttrain-practice-roadmap/` | workflow | stable |
| continue-pretrain-vs-finetune | `KNOWLEDGE/training/continue-pretrain-vs-finetune/` | methodology | stable |
| sft-rl-relationship | `KNOWLEDGE/training/sft-rl-relationship/` | concept | stable |
| lora | `KNOWLEDGE/training/lora/` | method | stable |
| long-context-rl | `KNOWLEDGE/training/long-context-rl/` | method | stable |
| sft-data-size | `KNOWLEDGE/training/sft-data-size/` | methodology | stable |
| rlhf-dpo-grpo | `KNOWLEDGE/training/rlhf-dpo-grpo/` | concept | stable |
| agent-context-compaction | `KNOWLEDGE/agent/agent-context-compaction/` | system | stable |
| agent-permission-system | `KNOWLEDGE/agent/agent-permission-system/` | system | stable |
| agent-role-isolation | `KNOWLEDGE/agent/agent-role-isolation/` | system | stable |
| agent-tool-design | `KNOWLEDGE/agent/agent-tool-design/` | capability | stable |
| agent-memory-system | `KNOWLEDGE/agent/agent-memory-system/` | system | stable |
| agent-system-prompt | `KNOWLEDGE/agent/agent-system-prompt/` | capability | stable |
| agentops-vs-opsagent | `KNOWLEDGE/agent/agentops-vs-opsagent/` | concept | stable |
| multi-agent-rca-paradigm | `KNOWLEDGE/agent/multi-agent-rca-paradigm/` | system | stable |
| agent-failure-attribution | `KNOWLEDGE/agent/agent-failure-attribution/` | research-direction | stable |
| agent-anomaly-taxonomy | `KNOWLEDGE/agent/agent-anomaly-taxonomy/` | framework | stable |
| agent-failure-trajectory-dataset | `KNOWLEDGE/agent/agent-failure-trajectory-dataset/` | infrastructure | stable |
| heuristic-learning | `KNOWLEDGE/agent/heuristic-learning/` | concept | learning |
| memory-architecture-thesis | `KNOWLEDGE/agent/memory-architecture-thesis/` | concept | learning |
| agent-skills-closed-loop | `KNOWLEDGE/agent/agent-skills-closed-loop/` | system | learning |
| agent-memory-cascading-update | `KNOWLEDGE/agent/agent-memory-cascading-update/` | research-direction | learning |
| claude-md-rule-design | `KNOWLEDGE/agent/claude-md-rule-design/` | method | learning |
| model-boundary-probing | `KNOWLEDGE/agent/model-boundary-probing/` | capability | learning |
| agent-evaluation-harness | `KNOWLEDGE/agent/agent-evaluation-harness/` | system | learning |
| tool-call-repair-harness | `KNOWLEDGE/agent/tool-call-repair-harness/` | system | learning |
| agentic-rag-vs-long-context | `KNOWLEDGE/agent/agentic-rag-vs-long-context/` | system | learning |
| rag-failure-diagnosis | `KNOWLEDGE/agent/rag-failure-diagnosis/` | workflow | learning |
| rag-query-rewriting | `KNOWLEDGE/agent/rag-query-rewriting/` | method | learning |
| agentic-rag-planning-cache | `KNOWLEDGE/agent/agentic-rag-planning-cache/` | method | learning |
| architecture-design-six-steps | `KNOWLEDGE/methodology/architecture-design-six-steps/` | methodology | stable |
| three-tier-decision-docs | `KNOWLEDGE/methodology/three-tier-decision-docs/` | methodology | stable |
| ai-product-decision-four-questions | `KNOWLEDGE/methodology/ai-product-decision-four-questions/` | methodology | stable |
| sft-loss-signal-allocation | `KNOWLEDGE/training/sft-loss-signal-allocation/` | methodology | learning |
| sft-training-strategy | `KNOWLEDGE/training/sft-training-strategy/` | methodology | learning |
| sft-data-sourcing | `KNOWLEDGE/training/sft-data-sourcing/` | methodology | learning |
| sft-data-quality | `KNOWLEDGE/training/sft-data-quality/` | methodology | learning |
| small-model-harness-engineering | `KNOWLEDGE/agent/small-model-harness-engineering/` | system | learning |
| cache-aware-agent-loop | `KNOWLEDGE/agent/cache-aware-agent-loop/` | system | learning |
| hierarchical-agent-memory | `KNOWLEDGE/agent/hierarchical-agent-memory/` | system | learning |

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
| neo-deepresearch-and-react-agent | `PROJECTS/work/neo-deepresearch-and-react-agent/` | work | **in-progress** |
| awm-mechanism-audit | `PROJECTS/research/awm-mechanism-audit/` | research | done |
| selective-transfer-memory | `PROJECTS/research/selective-transfer-memory/` | research | done |

> `qiniu-zeroops-rca-agent/` 含 4 份文档：`README.md`（决策复盘）+ `system-anatomy.md`（系统解剖）+ `agent-subsystem.md`（Agent 子系统解剖）+ `interview-defense-matrix.md`（挑战防御矩阵 · living）
>
> `neo-deepresearch-and-react-agent/` 已有 3 份文档：`README.md`（4 子项目导航 + 挖掘 brief Q1-Q20）+ `interview-defense-matrix.md`（30+ 行 readiness baseline + GAP-N1~N12 清单）+ `subsystem-react-router.md`（D2 ReAct + 语义路由 working draft，待 C2 补齐）。等挖掘 brief 答完后再 evolve 出 `system-anatomy.md`
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
| `CAREER/cv.md` | 简历（过时，待更新） | 你 |
| `CAREER/skill-gap.md` | CV ↔ 目标岗位缺口表 | 你（LLM 建议 diff） |
| `CAREER/target-roles/` | 目标岗位画像（待填：summer-intern-agent-engineer、newgrad-agent-engineer） | 你（或对话长出但你审）|
| `CAREER/applications/` | 真实投递流水：pipeline + 单岗位投递记录 + 沟通话术 | 你确认事实；LLM 可按明确请求辅助维护 |
| `CAREER/interview-bank/technical/` | 技术题（已派生 4 条来自 qiniu-zeroops-rca-agent：agent-loop-vs-workflow / multi-agent-decomposition / multimodal-fusion-paradigm / opsagent-vs-agentops）| LLM triage |
| `CAREER/interview-bank/behavioral/` | 行为题 + STAR（已派生 3 条来自 qiniu-zeroops-rca-agent：ceo-pivot-decision / team-turbulence-handoff / roadshow-emergency-rescue）| LLM triage |

---

## WORK

| 路径 | 状态 |
|---|---|
| `WORK/` | 未来层。等 PROJECTS/work/ 复盘后从中提炼 SOP |

---

## WORK runbooks

症状导向的 agent 故障排查手册。和 KNOWLEDGE 节点的区别：节点写"概念为什么是这样"，runbook 写"我看到了 X，下一步做什么"。条目编号 P-XXX 全局递增，不按 domain 重置。

| id | 路径 | 条目数 | 状态 |
|---|---|---|---|
| agent-runbook | `WORK/runbooks/agent/` | 18（P-001 ~ P-018） | seed |

> 当前 18 条来源：
> - P-001 ~ P-008：`KNOWLEDGE/agent/small-model-harness-engineering/`（小模型工具调用故障域）
> - P-009 ~ P-013：`KNOWLEDGE/agent/structured-output/`（结构化输出 6 层）
> - P-014 ~ P-018：`KNOWLEDGE/agent/cache-aware-agent-loop/`（前缀缓存命中率作为成本杠杆）
>
> 验证状态全部为"未验证"——外部 claim，未在本地复现。⚠️ 已记录方案互冲：P-006（本地推理 OOM）vs P-014/P-015（云 API 缓存）在"上下文压缩"上做法相反，条目内互链警告。
>
> seed 阶段：跑两周看是否真的回来查。不回来查 = 症状字段没写到位，回来改。超过 30 条再按 agent 生命周期（perception/planning/tool-use/memory/execution/reliability）拆子目录。

---

## REPRO_INDEX

（暂无条目）

---

## TRACKS

| id | 路径 | 类型 | 状态 |
|---|---|---|---|
| sprint-2026-summer | TRACKS/active/sprint-2026-summer.md | 临时 | active |
| agent-engineer | TRACKS/roadmap/agent-engineer.md | 长期 | **待重写**（target-roles 已填，可重写）|

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
| `META/templates/*` | 各类内容模板 |

---

## Ownership 速查

| 区域 | 维护方 |
|---|---|
| INBOX、TRACKS、CAREER 下用户私有文件（cv / skill-gap / target-roles / applications 事实字段）、META | 你 |
| KNOWLEDGE、KNOWLEDGE/_self_check、PROBLEMS、PROJECTS、RAW_SOURCES、REPRO_INDEX、CAREER/interview-bank、CAREER/applications（明确请求时）、WORK/playbooks、PODCAST、REGISTRY | LLM 写入 |
| TRACKS 勾选 / skill-gap 更新 / 实习挖掘 / 横向对比 | LLM 在 Triage Report 建议，你执行 |
| PODCAST 写入 | LLM 写入但**仅在用户明确请求时** |

详见 `README.md` 的 Ownership Matrix 和 `META/llm/CONTEXT.md`。
