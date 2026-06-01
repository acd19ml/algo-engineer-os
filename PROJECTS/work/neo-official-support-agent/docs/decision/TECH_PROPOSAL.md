# Neo 官网智能客服 · 技术提案

> 决策层级：技术提案。本文只回答"该不该做、为什么这么做而不是别的方案"；组件和 schema 细节分别放在 [`../architecture/ARCHITECTURE.md`](../architecture/ARCHITECTURE.md) 与 [`../implementation/IMPLEMENTATION_DESIGN.md`](../implementation/IMPLEMENTATION_DESIGN.md)。

## 1. 提案结论

建议建设 **Neo 官网入口的 policy-constrained support orchestrator**：

- LLM 负责自然语言理解、受限路由、证据解释和用户可读表达。
- 高风险事实只来自 Neo 官方 registry、Neo N3 / Neo X 只读链上工具、官方文档和公告。
- 系统不做写链、签名、授权、approve、bridge 代操作，不让用户连接钱包。
- 证据不足、边界不清或资金损失类问题进入拒答、追问或人工升级。

一句话：**用 AI 处理表达和路由，用确定性 source of truth 处理事实和边界。**

## 2. 要解决的问题

Neo 官网用户的问题不是单一的"文档问答"：

- 概念解释：Neo / Neo N3 / Neo X / NEO / GAS。
- 官方导航：官网、文档、developer resources、wallet、explorer、bridge。
- 链上诊断：Neo N3 / Neo X 交易是否成功、为什么失败、地址余额或转账记录。
- 安全风险：可疑链接、合约地址、私钥 / WIF / 助记词、钓鱼。
- 第三方边界：交易所提现、第三方钱包、第三方 dApp。
- 合规边界：买卖建议、价格预测、收益建议。

传统 RAG bot 的主要风险是答不准；本项目的主要风险是 **把不确定事实说成确定事实**，进而导致用户资金损失或错误信任。

## 3. 为什么这里该上 AI

### 3.1 AI 适用点

| 需求特征 | 为什么适合 AI |
|---|---|
| 用户表达高度自然语言化 | 同一个问题可能用多语言、黑话、错误术语或混合 intent 表达。 |
| 问题需要路由 | 一个输入可能同时包含 tx hash、交易所边界、安全风险和概念解释。 |
| 证据需要解释 | 链上 receipt、VM state、logs、docs source 需要转成用户能理解的下一步。 |
| 人工需要摘要 | 支持团队需要结构化 handoff summary，而不是完整聊天记录。 |

### 3.2 不适合让 AI 自由处理的点

| 事实类型 | 为什么不能自由生成 |
|---|---|
| 官方地址 / 合约 / bridge | 错一个字符就可能导致资金损失。 |
| RPC / explorer / wallet 下载链接 | 容易被钓鱼域名利用。 |
| 交易状态 / 余额 / transfer history | 必须来自链上只读工具。 |
| token 支持状态 / migration deadline | 快变且高风险，必须绑定 source。 |
| 投资建议 | 合规风险，不回答。 |

结论：本项目不是"让 LLM 当客服"，而是让 LLM 在确定性 guardrail 内做客服编排。

## 4. 替代方案比较

| 方案 | 优点 | 问题 | 结论 |
|---|---|---|---|
| 纯 FAQ / 静态导航 | 成本低、风险可控 | 无法处理混合意图、tx 诊断、失败交易解释和 handoff summary | 作为 docs source 保留，但不足以解决目标问题 |
| 泛 RAG bot | 上线快，能回答文档问题 | 容易把文档片段外推成官方事实，无法保证地址 / link / tx 状态 exact match | 不作为最终形态 |
| 开放 ReAct Web3 agent | 能做多步工具调用 | 动作空间过大，容易越权到写链 / 签名 / 投资建议 / 第三方操作 | 明确拒绝 |
| 纯人工客服 | 风险低，判断灵活 | 重复问题多、响应慢、无法产品化链上查询流程 | 作为升级路径，不作为主入口唯一方案 |
| 本提案：受策略约束的客服编排器 | 兼顾自然语言体验、可验证事实和安全边界 | 需要维护 registry、评估集、policy 和 source owner | 推荐 |

## 5. 产品范围

### 5.1 包含

- Neo / Neo N3 / Neo X / NEO / GAS 官方解释。
- 官方链接导航与安全链接校验。
- Neo N3 tx / address 只读查询。
- Neo X tx / address 只读查询与 EVM 失败交易解释。
- 安全拦截、投资建议拒答、人工升级摘要。

### 5.2 不包含

- 交易所充值提现客服。
- 第三方钱包账户恢复或本地状态解释。
- 第三方 dApp 损失承担或资产追回承诺。
- 任何写链、签名、授权、转账、approve、bridge 代操作。
- 价格预测、买卖建议、收益建议。
- 用户连接钱包到客服 bot。

## 6. 关键决策

| 决策 | 候选 | 选择 | 理由 |
|---|---|---|---|
| 产品形态 | FAQ / RAG bot / open agent / support orchestrator | support orchestrator | 官网客服既需要自然语言体验，也需要强事实约束和高风险降级。 |
| Agent 动作空间 | 只读 + 模板 / 可写链 / 可连接钱包 | 只读 | 资金场景下不可逆操作不应进入客服 bot。 |
| 高风险事实来源 | LLM / docs RAG / registry + tool | registry + chain tool + official source | 地址、链接、token、tx status 必须 exact match 和可追溯。 |
| Neo N3 / Neo X 处理 | 统一链工具 / 双 adapter | 双 adapter | Neo N3 与 EVM 风格 Neo X 的失败诊断、地址和 receipt 语义不同。 |
| 风险处理 | prompt 提醒 / policy gate + verifier | policy gate + verifier | 高风险边界不能只靠提示词。 |
| 人工升级 | 异常失败路径 / 产品能力 | 产品能力 | 转人工是安全策略，不是系统失败。 |

## 7. 成功标准

| 指标 | 目标 | 决策含义 |
|---|---:|---|
| 高风险事实可追溯率 | >= 99.5% | 地址、链接、token、fee、bridge、migration、tx status 必须有 source。 |
| 高风险错误回答率 | 趋近 0 | 宁可拒答 / 转人工，不为了覆盖率牺牲安全。 |
| Neo N3 / Neo X tx 查询成功率 | >= 95% | 合法 tx hash 能查到状态或明确 not found。 |
| 失败交易解释可用率 | MVP >= 60% | 先给大类和下一步，Neo X 优先。 |
| secret 泄露拦截率 | >= 99% | WIF、private key、seed phrase 在落盘前拦截和 scrub。 |
| 投资建议越权率 | 0 | 任何买卖建议都拒答。 |

## 8. AI 产品决策四问

### 8.1 场景判断

该场景适合 AI 的原因不是"客服都可以用 AI"，而是：

- 用户输入天然模糊、多语言、混合意图。
- 系统需要根据风险切换 docs、registry、链上工具、incident、handoff。
- 链上 evidence 需要解释成普通用户可执行的下一步。

反面边界同样明确：官方地址、合约、bridge、钱包下载链接、交易状态不能让 LLM 猜；写链和投资建议不进入系统能力。

### 8.2 风险意识

主要风险和产品级兜底：

| 风险 | 兜底 |
|---|---|
| 幻觉官方地址 / 链接 | registry only，unknown 不背书。 |
| 交易状态解释错误 | chain adapter exact result + grounding verifier。 |
| secret 泄露 | ingress guard pre-log scrub，命中后不进 LLM / RAG / trace。 |
| prompt injection | 外部内容全视为 data，不得改变 policy。 |
| 投资建议诱导 | rule guard 覆写 LLM，固定拒答模板。 |
| 第三方边界混淆 | support boundary registry + handoff / redirect。 |

### 8.3 标准感

上线前必须有 golden set、adversarial eval、tool eval 和 faithfulness eval。指标不是上线后补，而是直接决定是否能从内部 copilot 进入官网 beta。

### 8.4 边界感

触发降级 / 人工的条件：

- 高风险问题证据不足。
- registry 缺失官方事实。
- 链上工具返回不一致。
- 用户资金损失、被盗、被骗。
- 用户请求写链、签名、授权、恢复账户或投资建议。
- 多次重述仍无法解决。

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| Registry owner 不清 | source 过期导致错误背书 | 每类 registry 指定 owner、last_verified_at、review SLA。 |
| Neo X bridge / explorer source 不稳定 | 关键导航不可信 | 缺 source 时拒绝输出地址，只给官方入口或转人工。 |
| 链上节点 / explorer incident | 大量误诊断 | Status / Incident Tool 优先于逐 tx 诊断。 |
| 多语言 secret 检测不足 | 泄露进入日志 | secret pattern + multilingual adversarial eval + redacted event only。 |
| 用户把 unknown URL 理解为安全 | 钓鱼风险 | unknown 只表达"无法确认官方"，不表达"安全"。 |
| 失败交易解释过度确定 | 误导用户行动 | 输出原因大类、证据和不确定性，不承诺追回或确定业务原因。 |

## 10. 决策门槛

进入 Phase 1 官网只读 Beta 前，至少满足：

- Network / Token / Official Link / Address / Wallet / Support Boundary registry 有 owner 和初始数据。
- Secret guard 在日志、trace、LLM 调用前生效。
- Investment advice、seed phrase、fake official link、fake bridge address adversarial case 全部通过。
- Neo N3 / Neo X tx 查询路径接入真实或 approved source。
- Grounding verifier 能阻断无 evidence 的高风险 claim。

## 11. 未决问题

1. Neo 官网当前权威 source of truth 是哪些系统。
2. Neo N3 / Neo X 是否有官方推荐 RPC endpoint 或 partner provider。
3. Neo X bridge 的官方 contract / explorer / status 源由谁维护。
4. 钱包列表是官方背书还是生态资源导航。
5. 客服 handoff summary 写入哪个系统。
6. 是否允许存储用户地址 / tx hash，以及 retention 多久。
