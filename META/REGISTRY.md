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

### 节点形态状态

| 形态 | 节点数 | 说明 |
|---|---|---|
| ✅ 新形态（因果叙述 + 反事实） | 32（全部） | 所有节点都已按 `META/policies/node_form.md` 重写 |
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
| methodology | `KNOWLEDGE/_self_check/methodology.md` | 完整（1 节点） |
| transformer | `KNOWLEDGE/_self_check/transformer.md` | 完整（3 节点 + 跨节点） |
| agent | `KNOWLEDGE/_self_check/agent.md` | 完整（6 节点 + 跨节点） |
| training | `KNOWLEDGE/_self_check/training.md` | 完整（7 节点 + 跨节点） |

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

（暂无。等对话 log 出现 "横向对比 N 方案" 时由 LLM 触发建议）

---

## PROJECTS

| id | 路径 | type | status |
|---|---|---|---|

（暂无。`PROJECTS/work/` 下两个待挖掘项目：qiniu-supervisor-agent、neo-deepresearch-and-react-agent）

---

## RAW_SOURCES

| id | 路径 | type |
|---|---|---|

（暂无）

---

## CAREER

| 文件 | 作用 | 维护方 |
|---|---|---|
| `CAREER/cv.md` | 简历（过时，待更新） | 你 |
| `CAREER/skill-gap.md` | CV ↔ 目标岗位缺口表 | 你（LLM 建议 diff） |
| `CAREER/target-roles/` | 目标岗位画像（待填：summer-intern-agent-engineer、newgrad-agent-engineer） | 你（或对话长出但你审）|
| `CAREER/interview-bank/technical/` | 技术题（待填：你丢面经触发）| LLM triage |
| `CAREER/interview-bank/behavioral/` | 行为题 + STAR（待填：从 PROJECTS/work 派生）| LLM triage |

---

## WORK

| 路径 | 状态 |
|---|---|
| `WORK/` | 未来层。等 PROJECTS/work/ 复盘后从中提炼 SOP |

---

## REPRO_INDEX

（暂无条目）

---

## TRACKS

| id | 路径 | 类型 | 状态 |
|---|---|---|---|
| final-exam-prep | TRACKS/active/final-exam-prep.md | 临时 | active |
| agent-engineer | TRACKS/roadmap/agent-engineer.md | 长期 | **待重写**（等 target-roles 填完）|

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
| INBOX、TRACKS、CAREER 下用户私有文件、META | 你 |
| KNOWLEDGE、KNOWLEDGE/_self_check、PROBLEMS、PROJECTS、RAW_SOURCES、REPRO_INDEX、CAREER/interview-bank、WORK/playbooks、PODCAST、REGISTRY | LLM 写入 |
| TRACKS 勾选 / skill-gap 更新 / 实习挖掘 / 横向对比 | LLM 在 Triage Report 建议，你执行 |
| PODCAST 写入 | LLM 写入但**仅在用户明确请求时** |

详见 `README.md` 的 Ownership Matrix 和 `META/llm/CONTEXT.md`。
