# Neo 官网智能客服 · 工业级交付路线图

> 一个资深 agent 架构师从拿到「Neo 官网需要智能客服」到交付完整方案的全过程。
> 8 个 Milestone，每个含目标、前置输入、关键决策、交付物、自检清单。

---

## 总览

```mermaid
flowchart LR
    subgraph DESIGN["设计阶段"]
        M0["M0<br/>需求分析与<br/>产品边界"] --> M1["M1<br/>技术方向<br/>决策"]
        M1 --> M2["M2<br/>安全架构<br/>设计"]
        M2 --> M3["M3<br/>系统架构与<br/>组件边界"]
        M3 --> M4["M4<br/>实现契约"]
        M4 --> M5["M5<br/>工程落地<br/>计划"]
    end

    subgraph VALIDATE["验证阶段"]
        M5 --> M6["M6<br/>Eval 体系<br/>设计"]
        M6 --> M7["M7<br/>运行与<br/>验证"]
    end

    subgraph EXTRACT["收敛阶段"]
        M7 --> M8["M8<br/>方法论<br/>提取"]
    end

    subgraph PRODUCTION["生产阶段"]
        M8 --> M9["M9<br/>生产部署"]
        M9 --> M10["M10<br/>Runtime<br/>可观测性"]
        M10 --> M11["M11<br/>事故响应<br/>与恢复"]
        M11 --> M12["M12<br/>持续 Eval"]
        M12 --> M13["M13<br/>持续改进<br/>闭环"]
    end

    M13 -.->|"反馈"| M5
    M13 -.->|"反馈"| M2

    style M0 fill:#e1f5fe,stroke:#0288d1
    style M1 fill:#e1f5fe,stroke:#0288d1
    style M2 fill:#fce4ec,stroke:#c62828
    style M3 fill:#e8f5e9,stroke:#2e7d32
    style M4 fill:#fff3e0,stroke:#e65100
    style M5 fill:#fff3e0,stroke:#e65100
    style M6 fill:#f3e5f5,stroke:#7b1fa2
    style M7 fill:#f3e5f5,stroke:#7b1fa2
    style M8 fill:#e0e0e0,stroke:#616161
    style M9 fill:#fff3e0,stroke:#e65100
    style M10 fill:#e1f5fe,stroke:#0288d1
    style M11 fill:#fce4ec,stroke:#c62828
    style M12 fill:#f3e5f5,stroke:#7b1fa2
    style M13 fill:#e8f5e9,stroke:#2e7d32
```

| 阶段 | 颜色 | 性质 |
|---|---|---|
| M0-M1（蓝） | 产品与方向 | 决定「做什么、不做什么、为什么这样做」 |
| M2（红） | 安全 | 决定「什么绝对不能错」——安全架构是整个系统的脊梁 |
| M3（绿） | 架构 | 决定「系统由哪些部分组成、怎么组织」 |
| M4-M5（橙） | 落地 | 把架构转成可开发、可评审的契约 |
| M6-M7（紫） | 验证 | 用可量化方式证明设计正确、假设成立 |
| M8（灰） | 收敛 | 把项目经验编译成可复用方法论 |
| M9（橙） | 部署 | 从 prototype 到生产服务 |
| M10（蓝） | 可观测性 | AgentOps 内置——不等部署后外挂补丁 |
| M11（红） | 事故响应 | 安全降级、回滚、复盘 |
| M12（紫） | 持续 Eval | 生产数据回流到 eval 体系 |
| M13（绿） | 持续改进 | 模型升级、规则更新、知识沉淀——闭环 |

---

## M0 · 需求分析与产品边界

> **目标**：定义「这个产品为谁解决什么问题」和「明确不解决什么」。
> 在 Web3 客服场景下，画错边界 = 用户资金风险。

```mermaid
flowchart TD
    A["用户输入混杂:<br/>官方概念 + 链上状态<br/>+ 可疑链接 + 投资建议<br/>+ 交易所/钱包边界"] --> B{"核心矛盾是什么?"}
    B --> C["RAG bot 的主要风险是答不准"]
    B --> D["Neo 客服的主要风险是<br/>把不确定事实说成确定事实<br/>→ 用户资金损失或错误信任"]
    D --> E["结论: 不能用泛 RAG 或开放 ReAct"]

    E --> F["产品定位"]
    F --> F1["Neo 官网入口的安全问答"]
    F --> F2["官方资源导航"]
    F --> F3["Neo N3 / Neo X 只读链上诊断"]

    E --> G["明确拒绝"]
    G --> G1["不做交易所客服"]
    G --> G2["不做投资建议"]
    G --> G3["不做写链/签名/转账"]
    G --> G4["不让用户连接钱包"]
    G --> G5["不承诺追回资金"]

    style D fill:#fce4ec,stroke:#c62828
    style E fill:#e8f5e9,stroke:#2e7d32
```

### 关键决策

| 决策 | 选择 | 拒绝 | 架构师判断 |
|---|---|---|---|
| 产品边界 | Neo 官网入口的安全问答 + 导航 + 只读诊断 | 泛 Web3 bot、多链通用 | 错误类型不是「答得不好」而是「把假的说成真的导致资金损失」——边界必须画在资金安全线上 |
| LLM 角色 | 只做理解、路由、表达 | LLM 作为事实源 | 高风险事实必须来自结构化 source of truth，不能靠模型生成 |
| 动作空间 | 全部只读 | 写链、签名、转账、钱包连接 | 让危险操作从能力层面就不存在——结构安全 > 规则拦截 |
| 上线路径 | 4 阶段渐进（内部 copilot → Beta → 诊断 → 事故联动） | 一步到位 | 渐进式暴露风险，每阶段有独立的安全门槛 |

### 交付物

- `docs/product/PRD.md`：用户、场景、产品范围、非目标、成功指标、安全边界、上线阶段

### 自检

- [ ] 每个非目标都对应一个「如果做了，最坏后果是什么」的反事实
- [ ] 安全边界三档（硬中断 > 拒答 > 降级/转人工）有明确触发条件
- [ ] 回答口径模板已定义（判断 + 证据 + 解释 + 安全下一步 + 边界）

---

## M1 · 技术方向决策

> **目标**：在多种候选方案中选出正确的 agent 架构形态，并给出「为什么不是其他方案」的论证。

```mermaid
flowchart TD
    START["M0 产出: 产品边界已定<br/>需要回答: 用什么技术形态?"] --> CANDIDATES

    subgraph CANDIDATES["候选方案评估"]
        direction TB
        C1["Discord-only<br/>维持社区支持"]
        C2["FAQ 页面"]
        C3["文档 RAG bot"]
        C4["开放 ReAct agent"]
        C5["纯人工客服"]
    end

    CANDIDATES --> EVAL

    subgraph EVAL["逐一排除"]
        E1["Discord-only → 无法产品化重复问题<br/>无法对官方入口做安全背书"]
        E2["FAQ → 用户问题混合文档+链上+安全<br/>关键词搜索无法匹配"]
        E3["RAG → 「最相似文档段落」≠「正确官方地址」<br/>没有 exact match 机制"]
        E4["ReAct → 动作空间过大<br/>容易越权到写链/签名/投资建议"]
        E5["纯人工 → 重复问题无法自动化<br/>每次都要人类重新排查 tx hash/network"]
    end

    EVAL --> FINAL["选择: Policy-constrained<br/>support orchestrator<br/><br/>LLM = 理解+路由+表达<br/>事实源 = registry + chain + docs<br/>安全 = 确定性 gate <br/>动作 = 全部只读"]

    style FINAL fill:#e8f5e9,stroke:#2e7d32
```

### 关键决策

| 决策 | 为什么 |
|---|---|
| 拒绝 Discord-only | 社区能处理复杂问题，但重复问题无法产品化 |
| 拒绝 FAQ | 用户输入不是关键词查询——混合了文档、链上、安全、边界 |
| 拒绝泛 RAG | 官方地址、合约、bridge 不能靠向量相似度判断——需要 exact match |
| 拒绝开放 ReAct | 客服 bot 的动作空间必须被约束——「帮我转账」不能被当真执行 |
| 拒绝纯人工 | AI 可以把重复问题产品化，让人处理复杂/高风险 case |
| **选择 policy-constrained orchestrator** | LLM 提案、确定性层裁决——模型不碰事实判断和动作授权 |

### 额外决策

| 决策 | 选择 | 理由 |
|---|---|---|
| Neo N3 / Neo X 处理 | 双 adapter，不合并 | N3（UTXO + application log）和 Neo X（EVM + receipt）的失败诊断语义完全不同 |
| AI 决策框架 | 四问（场景判断 + 风险意识 + 标准感 + 边界感） | 约束 AI 决策讨论不跑偏到实现细节 |

### 交付物

- `docs/decision/TECH_PROPOSAL.md`：替代方案比较、关键决策、AI 四问

### 自检

- [ ] 每个被拒绝的方案都有「如果选了这个，哪里会出问题」的反事实
- [ ] agent 形态选择说清了「LLM 负责什么、不负责什么」

---

## M2 · 安全架构设计

> **目标**：定义安全不变量——系统从 day-1 起必须满足哪些条件，以及如何抓到违反。
> 安全架构是整个系统的脊梁，必须先于组件设计。

```mermaid
flowchart TD
    subgraph DENY["Deny Layer · 保安 · 先跑"]
        D1["secret 检测<br/>ingress guard<br/>在任何 log/LLM/tool 之前"]
        D2["投资建议检测<br/>rule router<br/>关键词触发即拦"]
        D3["写链/连钱包检测<br/>rule router<br/>动作空间=只读是兜底"]
    end

    subgraph GATE["Policy Gate · 两层裁决"]
        G1["Deny Layer 先跑<br/>命中即短路"]
        G2["Allow Matrix 后查<br/>intent → allowed tools"]
        G3["deny 覆盖 allow<br/>不允许 override"]
    end

    subgraph VERIFY["Grounding Verifier · 独立审查"]
        V1["只读 claims + evidence<br/>不看 compiler 自我解释"]
        V2["硬事实 exact match<br/>软叙述禁语+夹带扫描"]
        V3["异常 fail closed<br/>缺证据 → 拦截/删 claim/handoff"]
    end

    DENY --> GATE --> VERIFY

    subgraph INVARIANTS["不可绕过的底线"]
        I1["secret deny 不可被运营配置关闭"]
        I2["投资 deny 不可被运营配置关闭"]
        I3["写链/连钱包 deny 不可被运营配置关闭"]
        I4["动作空间=只读<br/>（能力不存在 > 规则拦截）"]
    end

    style DENY fill:#fce4ec,stroke:#c62828
    style GATE fill:#fff3e0,stroke:#e65100
    style VERIFY fill:#e8f5e9,stroke:#2e7d32
    style INVARIANTS fill:#fce4ec,stroke:#c62828
```

### 安全层次

| 层 | 做什么 | 失败后果 | 兜底 |
|---|---|---|---|
| 动作空间 = 只读 | 无签名/转账/授权/approve 工具 | 越权写链 = 资金损失 | 结构保证——能力不存在 |
| Ingress guard | secret 检测，在任何下游组件之前 | secret 进 log/LLM | 硬中断，不进任何下游 |
| Deny layer | 投资/写链/连钱包关键词拦截 | 合规 + 品牌风险 | LLM 前短路 |
| Allow matrix | intent → allowed tools 子集 | 工具误用 | deny 覆盖 allow |
| Grounding verifier | claims vs evidence 对照 | 假官方地址 = 资金损失 | fail closed |

### 设计承诺（Design Commitments）

| DC | 不变量 |
|---|---|
| DC-001 | 高风险事实只能来自 evidence，不得由 LLM 生成 |
| DC-002 | secret / 投资 / 写链 / 连钱包是不可绕过底线 |
| DC-003 | Policy Gate 是唯一工具分配裁决点，Deny Layer 在 Router 前拦截安全关键路径，Allow Matrix 做 intent → 工具映射，deny 覆盖 allow。Router 的 intent 正确性由 DC-004 verifier 兜底 |
| DC-004 | 高风险回答必须经过独立 verifier，异常 fail closed |
| DC-005 | LLM 结构化输出必须先 parse → schema_validate → business_validate |
| DC-006 | 诊断和官方性判断必须有前置证据门 |
| DC-007 | 不定长工具输出必须有预算、preview 和指针 |
| DC-008 | 工具错误必须分类计数（resolution_error vs hard_error），重试有硬上限 |
| DC-009 | Docs query rewrite 只在 ambiguous docs 分支触发 |

> **DC 体系 = TLA（Trustworthy Level Agreement）的雏形**。
> 报告 `AgentOS_AgentOps_report.md` 提出：每个 agent 系统需要可观测的可信度围栏，运行时监控各级 TLA 是否 violation。
> 我们的 9 条 DC 恰好是 9 条 TLA——区别在于 DC-001~DC-009 中 DC-007（工具输出预算）尚未自动化检查，其余 8 条已通过 eval harness 逐条验证。

### 交付物

- `docs/design/commitments.md`：9 条 DC，每条含反事实、校验方式、覆盖范围

### 自检

- [ ] 每个 DC 都有「如果被违反，系统会怎样」的反事实
- [ ] 每个 DC 都有可执行的校验方式（代码级或 review 级）
- [ ] 安全 deny 不可被运营配置或事故状态关闭

---

## M3 · 系统架构与组件边界

> **目标**：把安全架构展开为可实现的组件拓扑——谁调谁、数据怎么流、边界在哪。

```mermaid
flowchart TD
    U["用户输入"] --> IG["Ingress Guard<br/>secret 检测 + scrub"]
    IG -->|"通过"| EE["Entity Extractor<br/>tx hash / address / URL / network"]
    EE --> RR["Rule Router<br/>投资 / 写链 / 连钱包 关键词"]
    RR -->|"通过"| RI["Router-independent<br/>转人工检测 / 链上歧义检测"]
    RI -->|"通过"| LR["LLM Router<br/>语义意图分类<br/>（mocked 或真实 LLM）"]
    LR --> PG["Policy Gate<br/>Deny Layer → Allow Matrix"]
    PG --> QP["Query Path Classifier<br/>registry_exact / chain / docs_direct / docs_ambiguous"]
    QP --> TOOLS["Tool Execution"]
    TOOLS --> EB["Evidence Bundle Builder"]
    EB --> AC["Answer Compiler<br/>typed claims"]
    AC --> GV["Grounding Verifier<br/>claims vs evidence"]
    GV -->|"通过"| OUT["用户回答 + sources"]
    GV -->|"拦截"| FC["fail closed<br/>删 claim / clarify / handoff"]

    subgraph TOOLS_SUB["只读工具集"]
        T1["Registry Lookup<br/>官方地址/链接/token<br/>exact match only"]
        T2["N3 Adapter<br/>getrawtransaction<br/>getapplicationlog<br/>getnep17balances"]
        T3["EVM Adapter<br/>eth_getTransactionReceipt<br/>eth_call"]
        T4["Docs Retriever<br/>带 source_id 的<br/>官方文档检索"]
        T5["Incident Feed<br/>RPC/explorer/bridge<br/>事故状态"]
    end

    TOOLS -.-> TOOLS_SUB

    style IG fill:#fce4ec,stroke:#c62828
    style RR fill:#fce4ec,stroke:#c62828
    style RI fill:#fff3e0,stroke:#e65100
    style LR fill:#e1f5fe,stroke:#0288d1
    style PG fill:#fff3e0,stroke:#e65100
    style GV fill:#e8f5e9,stroke:#2e7d28
    style FC fill:#fce4ec,stroke:#c62828
```

### Conversation State（多轮支持的跨轮次结构化状态）

当前 pipeline 是无状态的——每条 `user_message` 独立处理。真实客服场景是多轮的（用户追问、纠正、补充信息），需要在 pipeline 前后维护一个跨轮次的结构化状态。

**Schema（与 entity / evidence bundle 同 Pydantic v2 源）**：

| 字段 | 类型 | 说明 | 更新规则 |
|---|---|---|---|
| `entities` | `Entity`（累积 + 可纠正） | 跨轮次合并的 tx_hashes / addresses / urls / networks / token_symbols | 每轮 entity extractor 抽取后 merge；用户纠正时覆盖（"不对，是 Neo N3"→ 覆盖 networks） |
| `resolved_intent` | `Intent` | 当前有效的意图分类 | LLM router 产出后更新；用户纠正时重新分类 |
| `pending` | `list[ClarificationPrompt]` | 待用户补充的信息队列 | policy gate 产出 clarify 时 push；用户回复满足条件时 pop |
| `prior_evidence` | `list[EvidenceRef]` | 前轮已查到的证据引用（turn + type + source_id） | 每轮 evidence bundle 构建后追加 |
| `turn_count` | `int` | 当前对话轮次 | 每轮递增 |
| `handoff_readiness` | `bool` | 是否已触发过早停检测 | 用于 Termination Anomaly 监控 |

**在 pipeline 中的位置**：

```mermaid
flowchart LR
    CS_IN["Conversation<br/>State (read)<br/>注入累积 entities"] --> EE["Entity Extractor<br/>合并当前轮次 + 历史"]
    EE --> RR["Rule Router"]
    RR --> RI["Router-independent"]
    RI --> LR["LLM Router<br/>参考 resolved_intent"]
    LR --> PG["Policy Gate"]
    PG --> QP["Query Path"]
    QP --> TOOLS["Tools"]
    TOOLS --> EB["Evidence Bundle"]
    EB --> CS_OUT["Conversation<br/>State (write)<br/>更新 entities / intent / evidence"]
    CS_OUT --> AC["Answer Compiler"]
    AC --> GV["Grounding Verifier"]
```

**为什么不是把所有历史轮次塞进上下文**：

| 方案 | 问题 | KNOWLEDGE 节点 |
|---|---|---|
| 原始对话全塞 | Memory Anomaly · Long Context——上下文增长，注意力衰减。早期关键信息（tx hash、network）被埋在中间，模型"看得到但注意不到" | `[[agent-anomaly-taxonomy]]` |
| 原始对话全塞 | 上下文利用率超过 ~40% 后性能下降 | `[[agentic-rag-vs-long-context]]` |
| 原始对话全塞 | Context Anxiety——上下文越长，模型越倾向于草草收工（客服场景 = 过早 handoff） | `[[harness-practice]]` |
| **结构化状态** | 状态是压缩的、类型化的、可精确覆盖的。模型只看当前轮次 + 结构化摘要 | — |

**Compaction 策略**（来自 `[[context-engineering]]` 第 2 层）：

当 `turn_count > N` 或 token 估算超阈值时触发：
1. 保留 `conversation_state`（结构化，不可丢）
2. 保留最近 3 轮的原始对话
3. 更早的轮次：只保留模型推理过程（关键决策），丢弃冗余文本和纠正消息

### 数据资产

| 资产 | 内容 | 正确性保证 | freshness |
|---|---|---|---|
| Official Registry | 官方地址、合约、链接、token、钱包入口、bridge、支持边界 | owner 确认 + review | 变更时更新 |
| Docs Index | 官方文档、开发者文档、Neo X 文档 | source URL 可追溯 | 按 indexing cadence |
| Chain Adapters | N3 RPC + Neo X RPC 只读查询 | 官方 endpoint 或 approved provider | 实时 |
| Incident Feed | RPC/explorer/bridge/docs 事故状态 | status page 或内部配置 | 实时 |

### 部署形态

| 阶段 | 形态 | 理由 |
|---|---|---|
| Phase 0（内部 copilot） | 单体 Python service + YAML registry | 先验证逻辑正确，不引入分布式复杂度 |
| Phase 1（Beta） | 同上 + signed registry release | 需要 registry 可信度保证 |
| Phase 2+ | 可拆微服务 | 模块化边界已预留 |

### 交付物

- `docs/architecture/ARCHITECTURE.md`：组件拓扑、数据流、数据资产、部署视图

### 自检

- [ ] 每个组件的输入/输出边界清楚——不会出现 A 组件依赖 B 组件的内部状态
- [ ] 安全组件（红）在语义组件（蓝）之前执行
- [ ] 验证组件（绿）在输出前最后一道
- [ ] Conversation State 的读写位置正确：pipeline 开始时读取（合并历史实体），evidence bundle 之后写入（更新累积状态）

---

## M4 · 实现契约

> **目标**：把架构转成可开发、可测试、可评审的精确契约——字段、schema、pipeline 每一步的输入输出。

```mermaid
flowchart LR
    subgraph INPUT["输入"]
        I1["user_message: str"]
    end

    subgraph ENTITIES["实体抽取"]
        E1["tx_hashes: [64hex | 0x+64hex]"]
        E2["addresses: [N3 addr | 0x+40hex]"]
        E3["urls: [validated URL]"]
        E4["networks: [n3_mainnet | x_mainnet | ...]"]
        E5["token_symbols: [str]"]
        E6["malformed_tx_like: [str]"]
        E7["network_ambiguous: bool"]
    end

    subgraph INTENT["意图 + 风险"]
        N1["intent: 12 类<br/>neo_basic_explain ~ unsupported"]
        N2["risk: low | medium | high | critical"]
    end

    subgraph POLICY["策略裁决"]
        P1["decision: deny | handoff_or_clarify | allow"]
        P2["answer_mode: 8 种<br/>hard_interrupt ~ handoff"]
        P3["tools_called: [str]"]
    end

    subgraph EVIDENCE["证据"]
        V1["evidence_types: [registry | docs | chain | incident]"]
        V2["claim_types: [hard_fact | soft_narrative | ...]"]
        V3["source_ids: [str]"]
    end

    INPUT --> ENTITIES --> INTENT --> POLICY --> EVIDENCE

    style INPUT fill:#e1f5fe,stroke:#0288d1
    style ENTITIES fill:#fff3e0,stroke:#e65100
    style INTENT fill:#e1f5fe,stroke:#0288d1
    style POLICY fill:#fce4ec,stroke:#c62828
    style EVIDENCE fill:#e8f5e9,stroke:#2e7d32
```

### 核心契约

| 契约 | 内容 |
|---|---|
| Schema 源 | Pydantic v2 model——喂 LLM 的 JSON Schema 由 `.model_json_schema()` 生成，运行时校验即同一 model |
| 结构化输出校验 | parse → schema_validate → business_validate 三级。parse 失败 fail loud，不返回空对象（DC-005） |
| Policy gate 两层 | Deny Layer（保安，先跑，命中短路）+ Allow Matrix（菜单，后查）。deny 覆盖 allow（DC-003） |
| Query path 分类 | registry_exact / chain / docs_direct / docs_ambiguous。rewrite 只在 ambiguous docs 分支（DC-009） |
| Verifier 输入 | 只读 claims + evidence_bundle，不读 compiler 自我解释（DC-004） |
| 外部内容 | 全部进入 evidence_bundle.data，不进 system instruction |
| 硬事实裁决 | exact match（确定性代码）——不交给 LLM 放行 |
| 软叙述裁决 | 禁语 + 夹带扫描 + LLM 蕴含 advisory |
| 工具错误 | 区分 resolution_error（不计入失败计数）vs hard_error（计入，超限终止）（DC-008） |

### 交付物

- `docs/implementation/IMPLEMENTATION_DESIGN.md`：runtime pipeline、core types、policy matrix、tool contracts、evidence spec、answer compiler spec、MVP backlog

### 自检

- [ ] 每个 schema 字段都有格式约束（pattern / enum / url），没有裸 string
- [ ] pipeline 每一步的输入类型和输出类型明确
- [ ] Deny Layer 表里没有 "allow" 列——critical intent 永不为 allow

---

## M5 · 工程落地计划

> **目标**：把实现契约转成可执行的工程计划——用什么技术栈、API 长什么样、registry 怎么运维。

### 技术栈

| 层 | 选择 | 原因 |
|---|---|---|
| 语言 | Python | |
| API | FastAPI | Chat API、Admin API、Eval Job 都是 HTTP/job 型接口 |
| Schema | Pydantic v2 | 已在 DC-005 锁定为结构化输出单一源 |
| Eval | pytest + deterministic fixture providers | 先验证逻辑，不依赖真实 provider |
| Registry (Phase 0) | YAML + PR review | 先验证 registry schema 正确，不引入 DB 复杂度 |
| Registry (Phase 1) | Git-backed + signed release artifact | 需要可信度保证 |
| Registry (Phase 2+) | DB + admin workflow | 需要操作成熟度 |

### API 设计

```mermaid
flowchart LR
    subgraph CHAT["Chat API"]
        C1["POST /api/chat<br/>user_message → answer"]
    end

    subgraph ADMIN["Admin API (Phase 0: PR-based)"]
        A1["propose registry change"]
        A2["approve / reject change"]
        A3["双人 review for critical changes"]
    end

    subgraph EVAL_API["Eval API"]
        E1["POST /api/eval/run<br/>suite → metrics"]
        E2["GET /api/eval/results"]
    end

    CHAT --> ADMIN
    CHAT --> EVAL_API

    style CHAT fill:#e1f5fe,stroke:#0288d1
    style ADMIN fill:#fff3e0,stroke:#e65100
    style EVAL_API fill:#f3e5f5,stroke:#7b1fa2
```

#### Runtime 可观测性（内置，非外挂）

AgentOps 报告的核心判断：可观测性应原生内置到 Agent runtime，不应等部署后外挂补丁。
因此 Chat API 的 response 不仅返回用户可见的 answer，也记录内部执行轨迹（仅内部使用）：

| 记录项 | 内容 | 用途 |
|---|---|---|
| model_calls | 每次 LLM 调用的 model、prompt、output、token、latency | 路由准确率追踪、成本归因 |
| tool_calls | 每次工具调用的名称、参数、返回结果、error 类型 | DC-008 校验、工具可靠性 |
| pipeline_trace | ingress → deny → router → policy → path → tools → evidence → compiler → verifier 每步的输入/输出摘要 | Failure Attribution——定位 error decisive state |
| tla_violations | 运行时 DC 违反记录（如 verifier 拦截、policy gate deny） | TLA 监控 |

这些记录在 Phase 0 即可落地（内部 copilot），不需要额外的基础设施——和 eval harness 共享同一套 SUT 输出结构。

### Registry 运维

| Registry | Owner | Reviewer | SLA |
|---|---|---|---|
| Official Link | web/product owner | product owner | 30 days or URL change |
| Token Registry | product/docs owner | product owner | 30 days or token change |
| Address/Contract | security/dev owner | security owner | 7 days for critical |
| Wallet Registry | product/devrel | security owner | 30 days |
| Support Boundary | support/legal | product owner | 90 days or policy change |

Provider 分级：`candidate` → `verified` → `source-owner confirmed`。candidate 不可作为生产背书。

### 交付物

- `docs/implementation/implementation-plan.md`：Chat API v0、Admin API v0、Eval Job v0、技术栈
- `docs/operations/registry-ops-plan.md`：owner matrix、review rules、storage plan、provider policy、bridge boundary

### 自检

- [ ] MVP 先做什么、后做什么的优先级清楚（P0 > P1 > P2 > P3）
- [ ] 每个 registry 有 proposed owner 和 SLA
- [ ] 所有 candidate source 明确标注「未经 owner 确认，不用于生产背书」

---

## M6 · Eval 体系设计

> **目标**：在设计阶段就定义「怎么证明系统是对的」——不等上线后才发现问题。

```mermaid
flowchart TD
    subgraph CASES["100 Cases · 12 Suites"]
        C1["Neo basic explain (8)"]
        C2["NEO/GAS role (8)"]
        C3["Official navigation (10)"]
        C4["Address/contract check (12)"]
        C5["N3 tx status (10)"]
        C6["Neo X tx status (10)"]
        C7["Tx failure diagnosis (10)"]
        C8["Exchange/wallet boundary (8)"]
        C9["Secret hard interrupt (8)"]
        C10["Investment refusal (8)"]
        C11["Write-chain/wallet-connect (4)"]
        C12["Prompt injection (4)"]
    end

    subgraph METRICS["8 个指标 · 全部任务语义"]
        M1["policy_resolution_accuracy ≥ 98%"]
        M2["critical_bypass_rate = 0"]
        M3["missing_evidence_block_rate = 100%"]
        M4["verified_hard_claim_precision = 100%"]
        M5["route_before_rewrite_compliance = 100%"]
        M6["secret_raw_persistence_violations = 0"]
        M7["tool_error_classification_accuracy ≥ 95%"]
        M8["handoff_trigger_accuracy ≥ 95%"]
    end

    subgraph HARNESS["Runner 设计"]
        H1["Deterministic SUT<br/>SupportOrchestratorSUT.run(case)"]
        H2["FixtureProvider<br/>YAML → registry/tool/docs mocks"]
        H3["Mocked chain adapters<br/>N3 + EVM fixture responses"]
        H4["Per-case check<br/>decision / answer_mode / tools / <br/>evidence / claims / verifier / handoff"]
    end

    CASES --> METRICS --> HARNESS

    style CASES fill:#e1f5fe,stroke:#0288d1
    style METRICS fill:#f3e5f5,stroke:#7b1fa2
    style HARNESS fill:#fff3e0,stroke:#e65100
```

### Eval 设计原则

| 原则 | 说明 |
|---|---|
| 看执行轨迹，不看最终答案 | 检查 decision、answer_mode、tools_called、evidence、claims——每个节点都可归因 |
| 先 mocked 后 LLM | 分离「确定性层对不对」和「LLM 意图准不准」两个变量 |
| 指标限 8 个，全部任务语义 | 不加延迟、token 消耗等纯操作性指标 |
| Heldout 集独立于调参 | T1 留出集（7 条）不参与任何规则调整，用于检验泛化 |
| 每个 case 有 expected | decision、answer_mode、required_tools、forbidden_tools、evidence_types、claim_types、source requirement |
| **Eval 与 runtime 同构** | eval harness 的 SUT 和 Chat API 的 pipeline 是同一套代码路径——eval 不是外挂的测试框架，是 runtime 的离线执行模式。这保证了「eval 通过的 = 生产也会通过的」 |

> **当前限制：单轮 eval，未覆盖多轮对话的三类 Memory/Termination Anomaly**。
>
> 来自 `[[agent-anomaly-taxonomy]]`：多轮对话引入的三类异常对应三个不同的失败机制：
>
> | 现象 | 异常类别 | 失败机制 | 客服场景表现 |
> |---|---|---|---|
> | Lost in the Middle | Memory Anomaly · Long Context | 上下文增长，模型注意力衰减——早期关键信息（tx hash、network）被埋在中间，模型"看得到但注意不到" | 用户在第 1 轮提供了 tx hash，第 5 轮追问细节时 bot 忘了查的是哪笔交易 |
> | 模型早停 | Termination Anomaly · Premature Stop | 上下文过长 → 模型产生"上下文焦虑" → 提前终止任务 | 对话长了以后 bot 不再诊断，直接 handoff |
> | 检索污染 | Memory Anomaly · RAG Hallucinations | 多轮检索累积的文档噪声相互叠加 | N 轮 docs_answer 后，后续轮次引用了前轮的无关文档 |
>
> 好消息：检索污染在我们的架构里被部分免疫——T1 事实（地址/合约/tx status）走 registry exact match 和 chain adapter，不经过 RAG。RAG 只在 docs_answer 路径，污染范围限于解释性内容的准确性。
>
> AgentOps 报告警告：71% 的 benchmark 轨迹只有 5-10 步，简单启发式也能拿高分——单轮 eval 有同样的局限。多轮 eval 拆为三个子问题，留在 U-019~U-021。

### 交付物

- `eval/eval-cases.yaml`：100 条 case，每条含 expected 和 fixtures
- `eval/eval-fixtures.yaml`：registry / tool / docs 的 mock 数据
- `eval/eval-runner-spec.md`：runner 契约
- `eval/eval-prototype.md`：eval 方案、指标定义、诚实边界

### 自检

- [ ] 12 个 suite 覆盖安全路径（adversarial）+ 功能路径（golden）+ 边界路径（boundary）
- [ ] 每个指标有明确的评分标准，不是「差不多」
- [ ] 有独立的 heldout 集，不参与规则调参

---

## M7 · 运行与验证

> **目标**：用可复现的方式跑 eval，拿到数字，证明设计正确、假设成立。

```mermaid
flowchart TD
    subgraph RUN1["第一轮: Mocked Oracle"]
        R1["router = mocked<br/>（已知正确意图）"]
        R1 --> R1R["100/100 全部通过<br/>确定性层与 spec 一致"]
    end

    subgraph RUN2["第二轮: LLM Router 四档横扫"]
        R2["router = Qwen2.5<br/>7B / 14B / 32B / 72B"]
        R2 --> R2R["72B: 98/100<br/>critical_bypass = 0 跨全档"]
        R2R --> R2I["发现":<br/>1. 安全不变量与 router 能力无关<br/>2. 14B 以上 policy_resolution 持平<br/>3. 7B 崩在 structured-output conformance<br/>4. 跨模型稳定失败指向 D5 + B 类标注"]
    end

    subgraph FIX["修复"]
        F1["D1-a: URL 正则大小写无关<br/>+ unicode-confusable"]
        F2["D5: router-independent<br/>invariant 提到 router 前"]
        F3["B 类标注: 007 改 expected<br/>004 接受安全兜底"]
    end

    subgraph RUN3["第三轮: Heldout 验证"]
        R3["T1 留出集 7 条<br/>（未参与调参）"]
        R3 --> R3R["14B+: 7/7<br/>修复不是过拟合"]
    end

    RUN1 --> RUN2 --> FIX --> RUN3

    style RUN1 fill:#e8f5e9,stroke:#2e7d32
    style RUN2 fill:#e1f5fe,stroke:#0288d1
    style FIX fill:#fff3e0,stroke:#e65100
    style RUN3 fill:#e8f5e9,stroke:#2e7d32
```

### 关键验证结论

| 假设 | 验证方式 | 结论 |
|---|---|---|
| 「安全不变量与 router 能力无关」 | 四档模型横扫（7B 27% → 72B 98%，critical_bypass 全 0） | ✅ 成立 |
| 「router-independent invariant 不被 router 误判压掉」 | 注入最坏 router（永远返回 basic_explain），四条仍解析正确 | ✅ 成立 |
| 「D1-a 修复不是过拟合」 | T1 留出集 7/7（14B+） | ✅ 成立 |
| 「LLM 不可信」假设被压过 | 四档横扫 critical_bypass=0 | ✅ 未证伪 |
| 「hard-claim precision=100% 是构造性的」 | 硬事实只经 typed verified slot 渲染 | ⚠️ 需 full_prototype 模式证伪 |

### 诚实口径

- mocked 模式 100/100 不代表 real router 准确率——deny/boundary 启发式对着 100 条写，含轻度过拟合风险
- 真正「挣来的」指标：critical_bypass、secret 不落原文、route-before-rewrite、tool error 分类、handoff 触发——这些从 user_message + fixture 推导，不看 expected
- 不把任何数字转成客服时间下降 / CSAT / deflection 等业务声明

### 交付物

- `prototype/eval_runner/`：可运行 runner（`sut.py`、`fixtures.py`、`metrics.py`、`router.py`、`models.py`、`run_eval.py`、`sweep.py`）
- `eval/results/`：mocked + LLM 四档 + sweep 的 JSON/MD 结果
- `eval/harness-kb-alignment.md`：验证结果与 KNOWLEDGE 节点的对应关系
- `eval/eval-prototype.md` §9：结果表 + 诚实口径

#### Failure Attribution 粒度：当前与理想

当前每条 failure 输出 SUT 的最终状态（decision / answer_mode / tools / evidence / claims）。这已经能定位到「哪个组件错了」——

```
neo_n3_tx_status_006:
  failed: [decision, answer_mode]
  sut: {decision: allow, answer_mode: registry_template, intent: address_or_contract_check}
```

→ 直接定位到「router 把链上查询误判为地址查询」→ 修复方向明确（D5）。

**但还可以更细**。AgentOps 报告里 Echo 的分层上下文提示：如果加上 pipeline 中间步骤 trace（entity extractor 抽出了什么 entities → rule router 的判断 → LLM router 的原始输出），debug 可以从「router 判错了」进一步定位到「entity extractor 没抽到 tx hash 所以 router 没看到链上信号」。当前缺少这一层。

### 自检

- [ ] 所有结果可复现（runner 确定性的部分不依赖网络或随机数）
- [ ] 诚实口径和结果数字一起呈现，不分开
- [ ] 跨模型稳定失败有分类（A 类 = router-dependent safeguard，B 类 = 标注/边界模糊）
- [ ] DC-007（工具输出预算）是唯一尚未自动化检查的 DC——当前只在设计契约中存在

---

## M8 · 方法论提取

> **目标**：把项目中的设计选择编译成可复用的原则、playbook 和决策链——不重复踩坑。

```mermaid
flowchart TD
    subgraph EXTRACT["从项目中提取"]
        E1["8 条可迁移原则<br/>每条带 KNOWLEDGE 源 + 项目证据"]
        E2["Detection Hardening Loop playbook<br/>heldout 先行 → 判定 → 条件硬化"]
        E3["完整决策脚印<br/>46 条决策 + 反事实 + 被否方案"]
    end

    subgraph OUTPUT["产出位置"]
        O1["eval/decision-trail-full.md<br/>工业级交付路线图（本文）"]
        O2["WORK/playbooks/<br/>detection-hardening-loop/"]
    end

    EXTRACT --> OUTPUT

    subgraph FEEDBACK["反馈到 KNOWLEDGE"]
        F1["[[three-tier-deny-overrides-allow]]<br/>DC pattern ← 工具级 deny-overrides-allow<br/>（非 intent 验证）"]
        F2["risk-stratification 实践<br/>← T1/T2/T3 分层纠正过程"]
    end

    OUTPUT -.-> FEEDBACK

    style EXTRACT fill:#e8f5e9,stroke:#2e7d32
    style OUTPUT fill:#e1f5fe,stroke:#0288d1
    style FEEDBACK fill:#e0e0e0,stroke:#616161
```

### 8 条可迁移原则

| # | 原则 | KNOWLEDGE 节点 |
|---|---|---|
| P1 | 安全靠结构，不靠文字——让危险操作从能力层面就不存在 | `agent-permission-system` |
| P2 | 生成和评估必须分离——审查者只看事实，不看自我解释 | `harness-practice` |
| P3 | 确定性层裁决安全，LLM 只做语义——安全不变量编码为代码 | `agent-permission-system` + `small-model-harness-engineering` |
| P4 | 约束放在最接近决策点的地方——不在远处的 system prompt 里写 | `agent-tool-design` |
| P5 | 上下文不是数据，是程序本身——外部内容不进 system instruction | `context-engineering` |
| P6 | Eval 看执行轨迹，不看最终答案——决策/工具/证据/claims 可归因 | `agent-evaluation-harness` |
| P7 | Heldout 先行，硬化靠证据驱动——不在主集上 100% 就认为够了 | `harness` |
| P8 | 每个 Harness 组件编码一个假设，跨模型压力测试 | `harness-practice` + `structured-output` |
| P9 | Eval 与 runtime 同构——eval 不是外挂测试框架，是 runtime 的离线执行模式。可观测性原生内置，不等部署后补丁 | AgentOS_AgentOps_report |

### 交付物

- `eval/decision-trail-full.md`：本文——8 个 Milestone 的完整决策链
- `WORK/playbooks/detection-hardening-loop/`：可复用的检测层加固流程（mermaid 流程图 + 5 步工作流 + 3 个反模式）
- `eval/harness-kb-alignment.md`：验证结果与 KNOWLEDGE 节点的精确对应

---

## M9 · 生产部署

> **目标**：将已验证的 prototype 部署为可运行的生产服务，完成所有外部依赖的确认。

```mermaid
flowchart TD
    subgraph BLOCKED["阻塞项解除（依赖 Neo 内部）"]
        B1["确认 official source owner<br/>registry / docs / RPC / explorer"]
        B2["确认 provider policy<br/>candidate → verified → source-owner"]
        B3["确认 handoff 目标系统<br/>工单系统 / 认证方式"]
        B4["确认多语言 MVP 范围<br/>CN / EN / JP / KR / RU ?"]
        B5["确认数据存储合规<br/>地址/tx hash 是否可存 / retention"]
    end

    subgraph DEPLOY["部署"]
        D1["Chat API 上线<br/>FastAPI + pipeline 集成"]
        D2["Registry 从 YAML → signed release<br/>Phase 1 可信度保证"]
        D3["真实链上 adapter 接入<br/>N3 RPC + Neo X RPC<br/>（替换 mocked fixtures）"]
        D4["Handoff summary → 工单系统"]
    end

    BLOCKED --> DEPLOY
    DEPLOY --> GATE{"Phase 1 Beta 门槛<br/>（PRD §10）"}
    GATE -->|"全部满足"| BETA["官网只读 Beta 上线"]
    GATE -->|"未满足"| BACK["阻塞项回环"]

    style BLOCKED fill:#fce4ec,stroke:#c62828
    style DEPLOY fill:#fff3e0,stroke:#e65100
    style BETA fill:#e8f5e9,stroke:#2e7d32
```

### 上线门槛（PRD §10）

| 条件 | 状态 |
|---|---|
| 高风险事实源 owner 明确 | 待 Neo 内部确认 |
| 官方链接、合约地址、钱包入口、bridge 入口有可验证 source | 待 registry production |
| secret 输入在落盘前拦截 | ✅ eval 已验证 |
| 投资建议 100% 拒答 | ✅ eval 已验证 |
| N3 / Neo X tx 查询只读路径可用 | 待真实 adapter 接入 |
| fake official link / fake contract / prompt injection 有回归测试 | ✅ 100 cases 覆盖 |
| Grounding verifier 能阻断无证据的高风险 claim | ✅ eval 已验证 |

### 部署架构

```mermaid
flowchart LR
    subgraph PUBLIC["用户面"]
        U["Neo 官网用户"]
    end

    subgraph SERVICE["Chat Service"]
        API["Chat API<br/>FastAPI"]
        PIPELINE["Pipeline<br/>ingress → deny → router → policy → path → tools → evidence → compiler → verifier"]
        CS["Conversation State<br/>Redis / DB"]
    end

    subgraph PROVIDERS["外部 Provider（只读）"]
        RPC3["Neo N3 RPC"]
        RPCX["Neo X RPC"]
        EXPLORER["Explorer API"]
        DOCS["Docs Index"]
    end

    subgraph REGISTRY["Registry"]
        REG["Signed Release<br/>Git-backed → DB"]
    end

    subgraph HANDOFF["人工升级"]
        TICKET["工单系统<br/>handoff summary → ticket"]
    end

    U --> API --> PIPELINE
    PIPELINE --> CS
    PIPELINE --> PROVIDERS
    PIPELINE --> REGISTRY
    PIPELINE --> HANDOFF

    style PIPELINE fill:#e1f5fe,stroke:#0288d1
```

### 交付物

- Chat API 可运行服务（替换 prototype eval harness 的 SUT 为生产 pipeline）
- Registry signed release 流程
- 真实 N3 / Neo X adapter（替换 mocked fixtures）
- Handoff → 工单系统集成

---

## M10 · Runtime 可观测性（AgentOps 内置）

> **目标**：将 M5 设计的 runtime observability 落地——不等部署后外挂补丁，AgentOps 原生内置。

来自 `[[agentops-vs-opsagent]]`：AgentOps 的运维对象是 agent 系统本身。监控数据不可靠（同一任务重跑可能走不同路径），需要重建一套容忍随机性的可观测方法。

```mermaid
flowchart TD
    subgraph TRACES["执行轨迹记录（每轮持久化）"]
        T1["model_calls<br/>model / prompt / output / token / latency"]
        T2["tool_calls<br/>tool_name / params / result / error_type"]
        T3["pipeline_trace<br/>每步输入/输出摘要<br/>（entity extractor → verifier 全链路）"]
        T4["tla_violations<br/>DC 违反记录<br/>（verifier 拦截 / policy gate deny）"]
        T5["conversation_state_snapshot<br/>每轮结束时的跨轮次状态"]
    end

    subgraph CACHE["缓存友好设计（来自 [[cache-aware-agent-loop]]）"]
        C1["Append-only Log<br/>只追加，不修改，不删除<br/>保证 KV Cache 命中"]
        C2["不可变前缀<br/>system prompt + tool definitions<br/>一次缓存，全 session 复用"]
        C3["Compaction 策略<br/>Cache Line Fold<br/>不替换旧消息，追加摘要到末尾"]
    end

    subgraph MONITOR["实时监控"]
        M1["TLA dashboard<br/>DC-001~DC-009 运行时违反率"]
        M2["critical_bypass 告警<br/>>0 即 P0"]
        M3["handoff 触发率<br/>按 intent / network 分桶"]
        M4["verifier 拦截率<br/>按 claim_type 分桶"]
    end

    TRACES --> MONITOR
    CACHE --> TRACES

    style TRACES fill:#e1f5fe,stroke:#0288d1
    style CACHE fill:#fff3e0,stroke:#e65100
    style MONITOR fill:#f3e5f5,stroke:#7b1fa2
```

### 与 eval harness 的关系

eval harness 和 runtime observability 共享同一套 SUT 输出结构（`SUTResult`）——eval 是离线回放模式，runtime 是在线记录模式。这保证了「eval 验证过的不变量 = runtime 监控的不变量」。

### 交付物

- Runtime trace 持久化（数据库或日志系统）
- TLA dashboard（DC-001~DC-009 实时违反率）
- critical_bypass P0 告警
- KV Cache 优化的 pipeline（Append-only Log + 不可变前缀）

---

## M11 · 事故响应与恢复

> **目标**：当生产环境出现问题时（RPC 故障、explorer 不可用、模型行为漂移），系统能安全降级而非崩溃。

来自 `[[agentops-vs-opsagent]]`：AgentOps 的 resolution 不是简单下发配置，而是 rollback / rerun / 调 prompt / A/B test，多步多轮。

```mermaid
flowchart TD
    subgraph DETECT["检测"]
        D1["provider health check<br/>N3 RPC / Neo X RPC / Explorer / Docs"]
        D2["model behavior drift<br/>production trajectory vs eval baseline"]
        D3["TLA violation spike<br/>verifier 拦截率突然升高"]
    end

    subgraph RESPOND["响应"]
        R1["Kill Switch<br/>per intent / network / adapter"]
        R2["事故模板<br/>RPC 故障 → 降级回答<br/>Explorer 不可用 → 转人工"]
        R3["rollback to checkpoint<br/>检查点回滚 + 重放"]
        R4["prompt / tool 热更新<br/>不重启服务"]
    end

    subgraph RECOVER["恢复"]
        RC1["post-incident eval<br/>回放事故期间的 production traces"]
        RC2["heldout 集扩充<br/>事故暴露的新 case → heldout"]
        RC3["DC 修订<br/>事故暴露的 TLA 盲区 → 新 DC 或修订现有 DC"]
    end

    DETECT --> RESPOND --> RECOVER
    RECOVER -.->|"反馈"| DETECT

    style DETECT fill:#fce4ec,stroke:#c62828
    style RESPOND fill:#fff3e0,stroke:#e65100
    style RECOVER fill:#e8f5e9,stroke:#2e7d32
```

### 事故分类与响应矩阵

| 事故类型 | 检测方式 | 响应 | 恢复后 |
|---|---|---|---|
| N3 RPC 不可用 | health check 超时 | 降级：N3 查询 → 告知用户暂时不可用 + 建议用 explorer | 回放事故期间的 N3 查询 → 确认无错误回答 |
| Neo X RPC 不可用 | health check 超时 | 同上 | 同上 |
| Explorer 不可用 | health check 超时 | 降级：tx 链接 → 只给 tx hash 文本 | 同上 |
| Docs index 过期 | source indexing cadence 告警 | 降级：docs_answer → 标注「文档可能不是最新」 | 重建索引 + 回放验证 |
| 模型行为漂移 | production trajectory vs eval baseline 偏离 > 阈值 | Kill switch：router → 降级为 rule-only router | A/B test 新模型 → 更新 eval baseline |
| verifier 拦截率 spike | TLA dashboard | 调查 spike 根因 → 如果 verifier 误判 → 热更新 verifier 规则 | heldout 扩充 |

### 交付物

- Provider health check + 告警
- Kill switch（per intent / network / adapter）
- 事故模板（RPC / Explorer / Bridge / Docs 故障）
- Rollback + 回放机制
- Post-incident eval 流程

---

## M12 · 持续 Eval（Production Feedback Loop）

> **目标**：生产环境的数据持续回流到 eval 体系——不是跑完 100 条就完了，而是 eval 集随生产增长。

```mermaid
flowchart TD
    subgraph PROD["生产环境"]
        P1["用户 query"]
        P2["pipeline 执行"]
        P3["用户反馈<br/>（👍/👎 / 转人工 / 追问纠正）"]
    end

    subgraph SHADOW["Shadow Eval"]
        S1["采样 production traces<br/>按 intent / risk / answer_mode 分层"]
        S2["人工标注 expected<br/>（抽样，非全量）"]
        S3["回放验证<br/>同一 trace → 对比当前 vs 历史 pipeline"]
    end

    subgraph UPDATE["Eval 集更新"]
        U1["heldout 扩充<br/>production 暴露的新 pattern → heldout"]
        U2["regression 检测<br/>新模型/新规则 → 已有 heldout 回归测试"]
        U3["drift baseline 更新<br/>模型行为变化 → 更新 eval baseline"]
    end

    PROD --> SHADOW --> UPDATE
    UPDATE -.->|"新 case"| PROD

    style PROD fill:#e1f5fe,stroke:#0288d1
    style SHADOW fill:#f3e5f5,stroke:#7b1fa2
    style UPDATE fill:#e8f5e9,stroke:#2e7d32
```

### 用户反馈信号 → eval case 的映射

| 用户信号 | 含义 | 转化为 |
|---|---|---|
| 👎 + 追问纠正 | bot 第一次回答错误 | 多轮 case：第一次 answer → 用户纠正 → 第二次 answer |
| 转人工（用户主动） | bot 无法解决 | 检查 handoff 触发率是否异常 + 人工标注 expected |
| 转人工（系统触发） | 系统判断无法安全回答 | 抽检 handoff summary 是否正确 |
| 用户重复相同问题 | bot 答案不清晰 | 标注 expected clarification |
| 无反馈 + 对话结束 | 可能满意 | 采样验证 answer 质量 |

### 交付物

- Production trace 采样 + 回放 pipeline
- 人工标注工作流（抽样标注 expected）
- heldout 集自动扩充规则
- Regression 检测（新部署 → 自动跑 heldout）

---

## M13 · 持续改进闭环

> **目标**：生产环境驱动的不只是 bug 修复，而是系统性改进——模型升级、规则更新、DC 修订、知识沉淀。

```mermaid
flowchart TD
    subgraph TRIGGER["触发源"]
        T1["M12 持续 eval<br/>heldout 扩充 + regression"]
        T2["M11 事故复盘<br/>incident → DC 修订"]
        T3["模型升级<br/>新模型 → 重新横扫"]
        T4["Neo 生态变化<br/>新网络 / 新 bridge / 新 token"]
        T5["用户行为变化<br/>新问题类型出现"]
    end

    subgraph IMPROVE["改进动作"]
        I1["pipeline 组件更新<br/>deny 规则 / router prompt / verifier 规则"]
        I2["registry 更新<br/>新地址 / 新 token / 新钱包"]
        I3["DC 修订<br/>新不变量或现有 DC 收窄/放宽"]
        I4["模型升级 + 横扫<br/>新模型 → 四档横扫 → 对比历史 baseline"]
        I5["eval 集更新<br/>新 case → main / heldout"]
    end

    subgraph FEEDBACK["知识沉淀"]
        F1["WORK/playbooks 更新<br/>新发现的可复用流程"]
        F2["WORK/design-commitment-patterns<br/>新的候选不变量"]
        F3["KNOWLEDGE 节点更新<br/>生产验证过的因果机制"]
    end

    TRIGGER --> IMPROVE --> FEEDBACK
    FEEDBACK -.->|"下次触发"| TRIGGER

    style TRIGGER fill:#fce4ec,stroke:#c62828
    style IMPROVE fill:#fff3e0,stroke:#e65100
    style FEEDBACK fill:#e0e0e0,stroke:#616161
```

### 模型升级流程

来自 `[[harness]]` 可拆卸性：「更好的模型会让某些 Harness 组件变成瓶颈」。每次模型升级：

1. 新模型 → 四档横扫（复用 M7 的 sweep harness）
2. 对比历史 baseline（policy_resolution / critical_bypass / handoff / tool_error 各档趋势）
3. 判断：哪些 Harness 组件可以移除/简化？
4. 判断：哪些组件在新模型下反而成为瓶颈？

### 来自 `[[agent-skills-closed-loop]]` 的启发

Hermes 的「Agent 自主将成功做法写成 SOP」在客服场景的映射：

| Hermes 概念 | Neo 客服映射 |
|---|---|
| 5+ tool calls 触发创建 | 多轮诊断成功 → 沉淀为该类问题的 SOP（如「Neo X 失败交易诊断标准流程」） |
| fixing a tricky error | 生产事故修复经验 → registry 更新 / verifier 规则调整 |
| don't wait to be asked | 系统自动检测 pattern（如某类 tx failure 反复出现且回答准确率高）→ 建议固化为 answer template |
| Skills that aren't maintained become liabilities | 过时的 answer template / registry 条目 → 定期审计 + 自动标记「待验证」 |

### 交付物

- 模型升级→横扫→对比的自动化流程
- Registry 定期审计 + 过期标记
- 生产 pattern → playbook / DC pattern 的提取流程
- KNOWLEDGE 节点的生产验证反馈

---

## 尚未尝试解决的问题

### 阻塞项（依赖外部）

| # | 问题 |
|---|---|
| U-001 | Neo 官方 source owner / production provider 确认 |
| U-002 | Registry production storage / retention |
| U-003 | Handoff 目标系统 + 认证 |
| U-004 | 多语言 MVP 语言列表 |
| U-005 | Source indexing cadence |
| U-006 | 用户地址/tx hash 存储合规 |

### 自己可做

| # | 问题 | 对应 Milestone |
|---|---|---|
| U-007 | D5 检测硬化：heldout_investment + heldout_handoff | M7 |
| U-008 | 版本阶梯消融 V1→V5 | M7 |
| U-009 | full_prototype：LLM 自由文本 compiler + verifier 压测 | M7 |
| U-010 | 多语言完整 eval | M6 |
| U-011 | 端到端服务代码（Chat API + 真实链上 adapter） | M5 |
| U-012 | 完整 punycode/IDN 归一化 | M4 |
| U-013 | Secret 检测用 format-valid 合成串 | M2 |

### 设计未决

| # | 问题 |
|---|---|
| U-014 | investment LLM overlay 的模型分离方案 |
| U-015 | 消融基线 V0 的前置——free-text compiler |
| U-016 | handoff/tool_error 指标分母太小（5-6） |

### AgentOps 视角暴露的缺口

| # | 问题 | 对应 AgentOps 概念 |
|---|---|---|
| U-019 | 多轮 Lost in the Middle eval：设计 10-15 条多轮 case，覆盖用户在第 1 轮提供关键信息、第 N 轮追问的场景。验证 conversation_state 的结构化锚定是否有效 | Memory Anomaly · Long Context |
| U-020 | 多轮早停 eval：设计长对话 stress case（8+ 轮），验证模型在上下文增长时是否过早 handoff。测量 handoff 触发轮次的分布 | Termination Anomaly · Premature Stop |
| U-021 | 多轮检索污染 eval：设计纯 docs_answer 的多轮 case，验证第 N 轮的答案是否被前 N-1 轮的无关文档污染 | Memory Anomaly · RAG Hallucinations |
| U-022 | Pipeline 中间步骤 trace：entity extractor / rule router / LLM router 的中间输出进入 failure report | Failure Attribution 粒度 |
| U-023 | DC-007 自动化检查：工具输出预算的 runtime enforcement + eval 指标 | TLA 全量覆盖 |
| U-024 | 生产 runtime observability：model_calls / tool_calls / pipeline_trace 的结构化记录（M5 已设计，待实现） | AgentOps 内置 |
| U-025 | 异常分类学系统化：按 AgentOps taxonomy（推理/规划/行动/记忆/环境）× T1/T2/T3 交叉审计 eval case 覆盖率 | Anomaly Taxonomy |

### 系统级

| # | 问题 |
|---|---|
| U-024 | `TRACKS/roadmap/agent-engineer.md` 重写 |
| U-025 | `PROBLEMS/` 条目：multi-agent-decomposition-axis、multimodal-fusion-paradigms |
