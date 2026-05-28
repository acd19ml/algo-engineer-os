# 面试深挖题：Agent Memory 自主研究

> 对当前 `cv.md` 项目栏 **Agent Memory 自主研究项目** 两条 bullet 的可能追问派生。
>
> 当前 CV 已不再放“Coding Agent + Procedural Memory 全链路主项目”，所以本文件只围绕已完成 / 已写入 CV 的研究经历准备。旧主项目想法只作为“未来延伸 / 如果重做”材料，不主动当成已完成项目讲。

---

## A. 项目总定位

| 追问 | 答题要点 | 链接 / Gap |
|---|---|---|
| 这个 Agent Memory 自主研究项目到底是什么？ | 它不是泛泛读论文，而是两组受控实验：第一组复现并审计 AWM @ Mind2Web，做 step-level paired case 分析；第二组在 HotpotQA → 2WikiMultiHopQA 上做 near-transfer pilot，验证记忆跨任务复用的边界。核心问题都是：memory 什么时候真的改变执行，什么时候只是噪声或误导。 | `PROJECTS/research/awm-mechanism-audit/`；`PROJECTS/research/selective-transfer-memory/` |
| 两条 bullet 之间的关系是什么？ | AWM 审计回答“workflow memory 对 web agent 执行到底影响在哪些 step”；HotpotQA → 2WikiMultiHopQA 回答“跨任务复用时，什么样的 memory 抽象才可执行”。前者定位影响窗口，后者定位迁移边界。 | `KNOWLEDGE/agent/memory-architecture-thesis/` |
| 为什么研究 memory，而不是只做 RAG 或微调？ | RAG 主要给知识片段，memory 更关注跨任务行为状态；微调把能力写进参数，更新慢且难审计。Agent memory 的价值在于把经验作为外部状态热更新，并在合适场景 selective reuse。 | `PROBLEMS/agent-memory-architecture/` |
| 这个项目有什么工程价值？ | 它给后续 Agent 系统设计提供评测方法：不要只看“有 memory vs 无 memory”的 aggregate 分数，而要做 paired-case、matched/mismatched、positive/negative/ineffective/redundant 拆解，定位 memory 何时帮、何时害。 | `PROBLEMS/agent-harness-boundary-map/` |

## B. AWM 复现与审计

| 追问 | 答题要点 | 链接 / Gap |
|---|---|---|
| 475 step-pair 是 475 个独立题目吗？ | 不是。它是 7 个站点、52 个 task 展开后的 step-pair 总数。每个 paired case = 同站点、同 task_id、同 step_idx 下，baseline vs workflow 的对比。独立性不强，是嵌套结构；适合机制分析，不适合外推强统计结论。 | `PROJECTS/research/awm-mechanism-audit/` |
| 6-18% 影响窗口怎么算？ | 把 paired case 分成 positive `(0,1)`、negative `(1,0)`、ineffective `(0,0)`、redundant `(1,1)`。workflow 实际改变 baseline 行为的窗口 = positive + negative 占比；7 个站点分布在 6-18%。 | 同上 |
| 为什么说正 / 负向站点干预模式反向？ | matched 站点上 workflow 更可能 strategy redirection、value format correction、premature termination prevention；mismatched 站点上更可能 domain misdirection、template step-skipping、workflow-first bias。说明 workflow 不是普遍有益，而是强依赖 task-workflow 匹配度。 | `KNOWLEDGE/agent/model-boundary-probing/` |
| 8 类 mechanism 怎么讲？ | 主线用“6 个步骤级机制 + 2 个轨迹现象”：matched 3 个正向机制，mismatched 3 个负向机制，再加 ineffective 和 accumulation 两类轨迹现象。若面试官追问 taxonomy 表，说明那是另一维度：按边界条件 pattern 组织。 | Gap：可整理成单独速记卡 |
| 这个研究能证明 AWM 不行吗？ | 不能这么说。更准确是：在我的 setting 下，AWM 的实际影响窗口比 aggregate score 暗示的小，并且有效性高度依赖 workflow 与任务匹配。它不是否定 AWM，而是补充边界条件。 | 诚实边界 |
| paired-case 方法为什么重要？ | 只看最终成功率会把“帮了 / 害了 / 没影响 / 本来就对”混在一起。paired-case 把同一 step 下有无 workflow 的行为对齐，能定位 memory 具体在哪个步骤改变了执行。 | `KNOWLEDGE/agent/agent-evaluation-harness/` |
| 为什么不能只看 task-level success？ | 因为 memory 可能只影响少数 step，但这些 step 是关键瓶颈；也可能最终成功但路径更差、调用更多工具。step-level 能解释机制，task-level 只能给结果。 | `PROBLEMS/agent-harness-boundary-map/` |

## C. HotpotQA → 2WikiMultiHopQA 近迁移实验

| 追问 | 答题要点 | 链接 / Gap |
|---|---|---|
| 为什么选 HotpotQA → 2WikiMultiHopQA？ | 两者都是多跳 QA，任务形式相近但实体关系和推理链不完全一致，适合测 near-transfer。比同一数据集 split 更能暴露“经验是否真的跨任务可复用”。 | `PROJECTS/research/selective-transfer-memory/` |
| None / Episodic / Consolidated 三种 memory 是什么？ | None 是无经验；Episodic 是注入具体 source episode 轨迹；Consolidated 是把多个 source episode 压缩成抽象 lesson。核心对比是：细节轨迹 vs 抽象经验，谁更能迁移。 | 同上 |
| matched / mismatched 怎么定义？ | 初始按粗粒度 bridge label 会出问题，后来细化到 attribute_bridge 和 relation_chain_bridge 等 subtype。结论是：relevance 的操作化定义会直接决定迁移是否显现。 | 同上 |
| source rerouting 修复了什么？ | 初始 matched 定义过粗，导致看似匹配的 source episode 其实推理结构不匹配。细化 subtype 后重新路由 source-target pair，matched 条件下的收益恢复。 | 同上 |
| operator-level repair 修复了什么？ | Consolidated lesson 抽象过头，丢掉可执行算子序列，模型知道“方向”但不知道“怎么做”。修复方式是保留 operator sequence + 抽象触发条件。 | `KNOWLEDGE/agent/agentic-rag-planning-cache/` |
| 最终结论是什么？ | selective transfer 不是简单“相似任务就能迁移”。它依赖两件事：第一，relevance 要按可执行推理结构定义；第二，memory 抽象不能丢掉 operator-level 可执行性。 | `KNOWLEDGE/agent/agent-memory-system/` |

## D. 两个研究合起来怎么讲

| 追问 | 答题要点 | 链接 / Gap |
|---|---|---|
| 两个研究共同贡献是什么？ | Agent memory 不是“加 vs 不加”的二元问题，而是 selective reuse 问题：在哪些情境加、加多具体、加错如何诊断。AWM 审计给 step-level 影响窗口，near-transfer pilot 给抽象可执行性边界。 | `PROBLEMS/agent-memory-architecture/` |
| 对真实 Agent 开发有什么启发？ | 设计 memory 系统时要同时设计评测：记录调用轨迹、区分正负影响、测 matched/mismatched，而不是只看平均成功率。否则 memory 可能在 demo 上有效、在错配任务中伤害执行。 | `KNOWLEDGE/agent/agent-evaluation-harness/` |
| 和飞书 / 华为这类企业 Agent 面试有什么关系？ | 企业 Agent 更关心可控性、可评测性和工程边界。这个研究能支撑你讲：企业级 Memory / Skills / Agentic RAG 不能只是“存知识”，还要有 routing、evaluation、failure diagnosis 和权限边界。 | `CAREER/applications/active/` |

## E. 未来延伸：不要主动当成已完成项目讲

| 场景 | 可讲内容 | 边界 |
|---|---|---|
| 如果把 memory 方法迁移到 Coding Agent？ | 可以把 SWE-bench issue 的成功轨迹蒸馏成 procedural memory，再用 matched/mismatched issue pair 测 selective reuse。 | 这是未来设想，不在当前 CV 中 |
| 如果重做七牛云 OpsAgent？ | 可把运维下钻的成功排查路径沉淀成 symptom-anchored procedural playbook，把 service-specific facts 放到 declarative store。 | 这是事后反思，不是当时已实现 |
| 拿到优质数据除了 SFT 还能做什么？ | 除了把行为写进参数，也可以把经验外化成可热更新的 memory / skill，尤其适合环境频繁变化、微调成本高的企业场景。 | 不要声称已训练 memory model |

## F. Active 面试驱动的补洞入口

| 来源 | 暴露空白 | 应补位置 |
|---|---|---|
| 飞书 Agent 面经 | MCP schema、参数校验、鉴权、失败处理需要具体例子 | 先在 `CAREER/applications/active/2026-05-17_bytedance-feishu_agent-backend-intern.md` 写岗位口径；学稳后沉淀到 `KNOWLEDGE/agent/agent-tool-design/` 或新节点 |
| 飞书 Agent 面经 | LangGraph state / checkpoint / key-value 设计 | 先补岗位备面；如果形成稳定理解，再建 `KNOWLEDGE/agent/langgraph-state/` |
| 飞书 Agent 面经 | Agent evaluation：多调用 / 少调用 / 参数错 | `PROBLEMS/agent-harness-boundary-map/` + 可派生 `CAREER/interview-bank/technical/agent-evaluation-metrics.md` |
| 飞书 Agent 面经 | 非 Markdown 文档 chunk / embedding / rerank / RAG 诊断 | 先用 Neo router 页准备；需要学习时建 `KNOWLEDGE/agent/rag-document-processing/` 或 `KNOWLEDGE/agent/rag-retrieval-rerank/` |
| 飞书 Agent 面经 | NumPy 手写 multi-head attention | `CAREER/interview-bank/technical/fundamentals.md` + `KNOWLEDGE/transformer/multi-head-attention/`；若公式不熟，补 `transformer/attention-scaling/` |
