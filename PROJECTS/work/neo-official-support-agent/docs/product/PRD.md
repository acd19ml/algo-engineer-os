# Neo 官网智能客服 PRD

> 版本：v0.3
> 日期：2026-05-31
> 范围：Neo official website support bot
> 产品定位：Neo 官网入口的安全问答 + 官方资源导航 + Neo N3 / Neo X 只读链上诊断
> Agent 形态：Policy-constrained support orchestrator with verifiable evidence

## 0. 文档职责边界

本文是**产品 source of truth**，只维护产品层决策：

- 用户是谁，问题是什么。
- 产品做什么、不做什么。
- 成功指标是什么。
- 高风险边界和上线阶段是什么。
- 哪些问题仍待业务 / 安全 / DevRel / 工程确认。

本文不维护 API、schema、工具契约、模块图和实现细节；这些内容由配套文档负责：

| 文档 | 负责什么 |
|---|---|
| [`../decision/TECH_PROPOSAL.md`](../decision/TECH_PROPOSAL.md) | 为什么该做、为什么不是泛 RAG / 开放 ReAct / 纯人工。 |
| [`../architecture/ARCHITECTURE.md`](../architecture/ARCHITECTURE.md) | 系统组件、模块边界、数据流、部署形态。 |
| [`../implementation/IMPLEMENTATION_DESIGN.md`](../implementation/IMPLEMENTATION_DESIGN.md) | intent、policy matrix、registry schema、tool contract、evidence、eval、MVP backlog。 |

职责边界原则：

- PRD 可以定义"必须有官方事实源"，但不定义 registry 字段。
- PRD 可以定义"只读链上诊断"，但不定义 adapter 函数。
- PRD 可以定义"投资建议拒答"，但不维护拒答模板细节。
- PRD 可以定义"转人工是产品能力"，但不定义 handoff schema。

## 1. 背景与问题

Neo 官网用户会把多类问题混在一个入口里问：

- "Neo / Neo N3 / Neo X 是什么？"
- "NEO 和 GAS 有什么区别？"
- "这笔交易成功了吗？"
- "为什么我的交易失败？"
- "交易所提现不到账怎么办？"
- "这个链接 / 合约 / 钱包是不是官方的？"
- "我该不该买 NEO / GAS？"
- "我把资产转错了能不能追回？"

这些问题表面像官网客服，实际混合了文档解释、官方导航、链上状态查询、安全风险、第三方边界和投资合规。

传统 RAG bot 的主要风险是答得不准；Neo 官网客服的主要风险是**把不确定事实说成确定事实**，导致用户资金损失或错误信任。

因此，本产品不定义为开放 ReAct agent，也不定义为泛 Web3 RAG bot，而定义为：

> Neo 官网入口的安全问答 + Neo N3 / Neo X 只读链上诊断 + 官方资源导航。

LLM 只负责自然语言理解、受限路由、证据解释和表达；高风险事实必须来自结构化 source of truth。

## 2. 产品目标

### 2.1 用户目标

- 用户能快速理解 Neo、Neo N3、Neo X、NEO、GAS、NeoFS、Oracle、Governance 等官方概念。
- 用户能找到正确的官方文档、开发者资源、钱包资源、explorer、Neo X 入口、bridge 入口。
- 用户贴出 Neo N3 / Neo X 交易哈希后，能获得可验证的交易状态解释。
- 用户遇到失败交易时，能知道失败原因的大类和安全的下一步。
- 用户在输入私钥、WIF、助记词、可疑链接时，被及时拦截和警告。
- 用户遇到交易所、第三方钱包、第三方 dApp 问题时，能被清楚告知 Neo 官网客服能做什么、不能做什么。

### 2.2 业务目标

- 降低官网、社区、开发者入口的重复客服问题。
- 降低用户被钓鱼、误入非官方入口、误信错误合约地址的风险。
- 为人工客服 / 社区管理员生成结构化诊断摘要，减少重复排查时间。
- 将 Neo N3 与 Neo X 的常见链上支持流程产品化。

### 2.3 非目标

- 不做交易所充值提现客服。
- 不替第三方钱包恢复账户或解释本地钱包内部状态。
- 不承诺找回被盗、被骗、转错资产。
- 不提供投资建议、价格预测、买卖建议、收益建议。
- 不提供写链、签名、转账、授权、bridge 代操作能力。
- 不让用户连接钱包到客服 bot。

## 3. 用户与场景

### 3.1 普通持币用户

常见问题：

- "NEO 和 GAS 有什么区别？"
- "我的 GAS 到账了吗？"
- "这个交易哈希怎么看？"
- "钱包显示没到账，但是 explorer 上有记录，哪个准？"

产品能力：

- 解释官方概念。
- 根据 tx hash / address 查公开链上状态。
- 引导用户对比链上状态与钱包展示状态。
- 对第三方钱包问题明确边界。

### 3.2 Neo X 用户

常见问题：

- "Neo X 是什么？"
- "Neo X 和 Neo N3 是什么关系？"
- "我的 Neo X 交易失败了，为什么？"
- "gas 不够 / nonce 错 / approve 失败怎么办？"

产品能力：

- 基于官方 Neo X 文档解释。
- 查询 Neo X 公开链上交易状态。
- 对失败交易给出 EVM 风格的大类解释和安全下一步。

### 3.3 开发者

常见问题：

- "Neo N3 RPC 怎么查 NEP-17 balance？"
- "application log 里 VM state 是 FAULT 是什么意思？"
- "Neo X 能不能用 Solidity / MetaMask / EVM tooling？"

产品能力：

- 检索官方 developer docs。
- 引用 RPC 方法、SDK 文档、示例。
- 对复杂 bug 转向 GitHub / developer community，并附带已收集上下文。

### 3.4 高风险用户

常见问题：

- "我被骗了，能追回吗？"
- "我把 NEO 转错地址了怎么办？"
- "这是我的助记词，你帮我看看。"
- "这个 token 现在能不能买？"

产品能力：

- 私钥 / 助记词硬中断。
- 投资建议拒答。
- 对不可逆损失保持诚实，不给虚假希望。
- 提供安全下一步和人工升级入口。

## 4. 范围

### 4.1 MVP 范围

MVP 只做五件事：

1. Neo / Neo N3 / Neo X / NEO / GAS 官方解释。
2. 官方链接导航与安全链接校验。
3. Neo N3 tx / address 只读查询。
4. Neo X tx / address 只读查询与 EVM 失败交易解释。
5. 安全拦截、投资建议拒答、人工升级摘要。

### 4.2 延后范围

- 登录态账户数据。
- 用户 ownership sign-message。
- 多语言完整评测集。
- 非 EVM / 非 Neo N3 的第三方链深度诊断。
- 复杂 bridge 全链路 indexer。
- 自动工单创建与 CRM 集成。

### 4.3 明确拒绝范围

- 要求用户输入 seed phrase / private key / WIF。
- 要求用户连接钱包给 bot。
- bot 发起交易、签名、授权、approve、bridge。
- 判断 token 是否值得投资。
- 承诺追回资金。
- 输出未经官方 source 验证的合约地址或下载链接。

## 5. 成功指标

> 下表是产品目标 / 上线验收指标，不是已达成业务结果。当前没有官网客服上线后的客服时间下降、CSAT 或转人工率等真实业务数据。

| 指标 | 目标 | 说明 |
|---|---:|---|
| 高风险事实可追溯率 | >= 99.5% | 地址、链接、支持链、token、fee、bridge、migration、交易状态必须能回指 source。 |
| 高风险错误回答率 | 趋近 0 | 资金相关宁可拒答 / 转人工。 |
| Neo N3 / Neo X tx 查询成功率 | >= 95% | 已知合法 tx hash 能被识别并查到状态或明确返回 not found。 |
| 失败交易解释可用率 | MVP >= 60% | 至少能给出失败大类和下一步；Neo X 优先高于 Neo N3。 |
| 用户重述率 | 持续下降 | 用户换句话重复问同一问题视为回答无效信号。 |
| 人工客服诊断时间 | 降低 >= 30% | 通过 handoff summary 缩短排查。 |
| secret 泄露拦截率 | >= 99% | WIF、private key、seed phrase、mnemonic 在落盘前拦截和 scrub。 |
| 投资建议越权率 | 0 | 不回答买卖建议。 |

## 6. 产品级事实源要求

本产品不能把"收集资料做 RAG"当成事实来源。高风险事实必须确定性化。

| 事实类型 | 产品要求 | 细节归属 |
|---|---|---|
| 支持网络、RPC、explorer | 必须来自官方确认的 network source。 | `IMPLEMENTATION_DESIGN.md` |
| NEO / GAS / token role | 必须来自官方 token source 或 docs source。 | `IMPLEMENTATION_DESIGN.md` |
| 官方链接、钱包下载入口 | 只推荐 allowlist 中的链接。 | `IMPLEMENTATION_DESIGN.md` |
| 合约、bridge、system address | 只做 official / deprecated / risky / unknown 判断，不用模型猜。 | `IMPLEMENTATION_DESIGN.md` |
| 交易状态、余额、transfer history | 必须来自只读链上工具或 approved explorer / indexer。 | `ARCHITECTURE.md` / `IMPLEMENTATION_DESIGN.md` |
| 第三方边界 | 交易所、第三方钱包、第三方 dApp 必须有明确支持边界。 | `IMPLEMENTATION_DESIGN.md` |

缺 source 时的产品原则：

- 不猜官方地址。
- 不背书 unknown link / address。
- 不承诺交易所或第三方钱包账户状态。
- 不承诺追回资金。
- 转追问、转人工或拒答。

## 7. 产品级安全边界

### 7.1 必须硬中断

- 用户输入 seed phrase / private key / WIF。
- 用户要求 bot 保存、分析或继续处理私钥类信息。
- 用户要求 bot 代签名、代转账、代授权、代 bridge。

### 7.2 必须拒答

- 买卖建议。
- 价格预测。
- 收益判断。
- "这个 token 能不能买"一类投资建议。

### 7.3 必须降级或转人工

- 高风险事实缺 source。
- 链上工具返回不一致。
- 用户资金损失 / 被盗 / 被骗。
- 用户问题依赖账户私有状态。
- 多次重述仍无法解决。
- 系统事故影响 RPC、explorer、bridge、docs 或 indexer。

### 7.4 回答口径

链上查询类回答必须包含：

1. 当前判断。
2. 证据来源。
3. 解释。
4. 安全下一步。
5. 边界 / 是否需要人工。

具体模板和 verifier 规则由 `IMPLEMENTATION_DESIGN.md` 维护。

## 8. 人工升级

转人工不是失败路径，而是安全策略。

必须支持的人工升级价值：

- 把用户问题、抽取实体、已查证据、bot 已回答内容、未解决原因整理成摘要。
- 避免人工重复问 tx hash、network、address、URL 等基础信息。
- 明确推荐处理团队：support、devrel、security、exchange redirect、wallet vendor。

不在 PRD 中维护 handoff schema；schema 由 `IMPLEMENTATION_DESIGN.md` 负责。

## 9. 上线阶段

### Phase 0：内部客服 Copilot

- 只给内部人员用。
- 输出建议回答和 evidence bundle。
- 收集真实问题分布。
- 高风险回答人工审核。

### Phase 1：官网只读 Beta

- Neo 基础解释。
- 官方链接导航。
- N3 / Neo X tx 查询。
- 投资建议拒答。
- secret guard。

### Phase 2：失败交易诊断

- Neo X EVM 失败原因优先。
- Neo N3 application log 解释。
- 建立错误字典。
- 引入 handoff summary。

### Phase 3：状态与事故联动

- status / incident feed。
- explorer / RPC / bridge incident template。
- 事故期间降级回答。

### Phase 4：账户态与 ownership

- 仅在必要时引入 sign-message。
- 固定签名模板。
- 不请求交易签名。
- 不请求 approve。
- 不连接未知域名。

## 10. 上线门槛

进入官网 Beta 前必须满足：

- 高风险事实源 owner 明确。
- 官方链接、合约地址、钱包入口、bridge 入口有可验证 source。
- secret 输入在落盘前拦截。
- 投资建议 100% 拒答。
- Neo N3 / Neo X tx 查询只读路径可用。
- 对 fake official link、fake contract、prompt injection、seed phrase、投资建议诱导有回归测试。
- Grounding verifier 能阻断无证据的高风险 claim。

具体 evaluation suite 和 tool fixture 由 `IMPLEMENTATION_DESIGN.md` 维护。

## 11. Open Questions

> 2026-06-01 已补 [`../operations/registry-ops-plan.md`](../operations/registry-ops-plan.md)：官方 source candidates、provider policy、owner / reviewer / SLA、bridge 边界已有方案级记录。下列问题只有在 Neo 内部 owner 确认后，才能从 open question 升级为 production fact。

1. Neo 官网当前权威 source of truth 是哪几个系统：官网 CMS、docs repo、Neo X docs repo、status page、explorer API、internal config？
2. Neo N3 / Neo X 是否有官方推荐 RPC endpoint，还是必须通过 partner provider？
3. Neo X bridge 的官方 contract / explorer / status 源由谁维护？
4. 钱包列表是否属于 Neo 官方背书，还是只能作为生态资源导航？
5. migration / legacy 信息是否仍然需要客服覆盖？若需要，source of truth 是哪个页面或公告？
6. 是否已有客服工单系统？handoff summary 应写入哪里？
7. 是否需要中文、英文、日文、韩文、俄文等多语言 MVP？
8. 是否允许存储用户地址 / tx hash？retention 多久？
9. 是否已有安全团队维护 phishing URL denylist？
10. Neo X 失败交易是否接第三方 simulation provider，还是先用 RPC + receipt + eth_call？

## 12. 当前决策

| 决策 | 结论 |
|---|---|
| 产品边界 | Neo 官网智能客服，不是泛 Web3 bot。 |
| Agent 形态 | Policy-constrained orchestrator，不做开放 ReAct。 |
| 动作空间 | 全部只读。 |
| 高风险事实来源 | Official source / registry / chain tool。 |
| Neo N3 / Neo X | 双 adapter，不能混成一个链上工具。 |
| 失败交易解释 | Neo X 走 EVM 诊断；Neo N3 走 application log / VM state。 |
| 身份方案 | 公链查询无需鉴权；账户私有状态延后。 |
| 官方地址 | 只查官方 source，不猜。 |
| 投资建议 | 拒答。 |
| secret 输入 | Pre-log scrub + hard interrupt。 |
