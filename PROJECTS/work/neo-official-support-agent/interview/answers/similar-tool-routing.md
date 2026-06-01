# Q: 你是如何保证两个相似的工具能被正确调用的？目前是如何解决这个问题的？

## 来源

- 出处：Neo 官网智能客服项目可能被 agent 开发岗位深挖的工具调用问题。
- 频率：高。只要简历里出现 `tool calling`、`router`、`policy gate`、`registry`、`chain adapter`，面试官很容易追问“相似工具怎么避免误调”。

## 涉及文档

- 主：`PROJECTS/work/neo-official-support-agent/docs/implementation/IMPLEMENTATION_DESIGN.md`
- 相关：`PROJECTS/work/neo-official-support-agent/docs/architecture/ARCHITECTURE.md`
- 相关：`PROJECTS/work/neo-official-support-agent/docs/design/commitments.md`
- 相关：`PROJECTS/work/neo-official-support-agent/eval/eval-cases.yaml`

## 我的答案（面试 2 分钟版）

我不会把“选哪个工具”完全交给 LLM 自由决定。两个工具相似时，核心不是把 tool description 写得更长，而是把工具边界前置成可验证的路由规则、schema 和 policy。

在 Neo 官网客服里，典型的相似工具有两组：

1. **Docs Retriever vs Registry Lookup**
   - `Docs Retriever` 适合解释概念，比如“Neo X 是什么”“NEO 和 GAS 有什么区别”。
   - `Registry Lookup` 才能判断官方链接、钱包入口、合约地址、bridge 地址、token 支持状态。
   - 所以“这个 bridge 地址是不是官方的”不能走 RAG，也不能靠文档相似片段推断，必须走 registry exact lookup。

2. **Neo N3 Adapter vs Neo X EVM Adapter**
   - 两个都像“查交易状态”，但底层语义不同。
   - Neo N3 看 raw transaction、application log、VM state。
   - Neo X 看 EVM transaction、receipt、revert reason。
   - 如果 network 不明确，不能让模型随便猜一个 adapter，而是追问。

目前我的解决方式是四层：

1. **先抽实体，再路由**
   先抽 `tx_hash / address / url / network_hint / intent`，并做 schema 校验。URL、address、tx_hash、network 不是裸字符串，而是有格式、pattern 或 enum 约束。没有合法实体，就不能进入对应工具。

2. **先分类 query path**
   在工具调用前把请求分成 `registry_exact / chain / docs_direct / docs_ambiguous`。只要问题里有 address、URL、tx hash、official bridge、contract 这类高风险实体，就不能进入 docs rewrite，更不能靠 RAG 判断官方性。

3. **Policy Gate 控制工具集合**
   LLM router 只产生候选 intent。最终能不能调用某个工具，由 Policy Gate 的 Deny Layer + Allow Matrix 决定。比如 `address_or_contract_check` 只允许 address registry，不允许 docs retriever 推断 officialness。

4. **不确定就追问，不强行调用**
   如果 tx hash / address 不能决定 Neo N3 还是 Neo X，或者 network hint 不明确，就进入 `clarification`；高风险场景宁可多问一步，也不猜。

一句话总结：

> 我解决相似工具误调用的方法是：不靠 prompt 让模型“自己理解工具区别”，而是把区别编码到 entity schema、query path classification、policy allow matrix 和 eval cases 里。LLM 只做候选路由，真正的工具调用必须过 deterministic policy；如果前置条件不足，就追问或 handoff，而不是猜。

## 展开版（技术面深问）

### 1. 为什么 tool description 不够

如果只是给两个工具写 description，比如：

- `docs_retriever`: search official docs
- `address_registry_lookup`: check official addresses

模型在“Neo X official bridge address”这类问题上仍可能因为语义相近而调用 docs retriever，然后从文档或社区片段里拼出一个地址。Web3 场景里这类错误不是普通问答错误，而是官方背书风险。

所以我的原则是：**相似工具的区别不能只写在自然语言描述里，要落到结构和 policy 里。**

### 2. Docs Retriever vs Registry Lookup

规则：

- 概念解释、开发文档、术语说明：走 `docs_direct` 或 `docs_ambiguous`。
- URL、address、contract、bridge、wallet、token support：走 `registry_exact`。
- `address_or_contract_check` 不能调用 docs retriever 推断官方性。
- 携带高风险实体的 query 不能被 rewrite 成 docs query 后再判断官方性。

例子：

| 用户问题 | 正确路径 | 为什么 |
|---|---|---|
| “Neo X 是什么？” | docs retriever | 概念解释，低风险 |
| “Neo X official bridge address 是多少？” | registry exact lookup | 地址是高风险事实，不能 RAG |
| “这个 0x... 是官方 bridge 吗？” | address registry lookup | officialness 只能 exact match |
| “ne0-docs.example 像官网吗？” | official link registry lookup | lookalike 域名不能让 docs 判断 |

### 3. Neo N3 Adapter vs Neo X EVM Adapter

规则：

- Neo N3：`n3_get_raw_transaction`、`n3_get_application_log`、`n3_get_nep17_balances`。
- Neo X：`evm_get_transaction_by_hash`、`evm_get_transaction_receipt`、`evm_call_simulate`。
- 如果 network 明确，按 network 走对应 adapter。
- 如果 tx/address 格式能决定，按格式走对应 adapter。
- 如果 network 和格式都不能决定，就追问。

例子：

| 用户问题 | 正确路径 | 为什么 |
|---|---|---|
| “Neo N3 tx 0x... 成功了吗？” | N3 adapter | network 明确 |
| “Neo X tx 0x... reverted 为什么？” | EVM adapter | network 明确 + EVM 失败语义 |
| “这个 0x... 是 N3 还是 Neo X 我不确定” | clarification | 64 hex 本身不能安全决定 network |
| “钱包显示失败但 explorer 成功” | chain adapter + wallet boundary | 链上状态和钱包展示状态是两个事实源 |

### 4. 目前解决到什么程度

诚实说法：

> 目前我是在设计契约和 eval fixture 层解决这个问题：实现设计里已经把 entity schema、query path classification、Policy Gate、Allow Matrix、clarification 规则写清楚；`eval-cases.yaml` 和 `eval-fixtures.yaml` 里也把相似工具误调场景与 mock 返回体列成测试用例。还没有真实 runner 结果，所以我不会说已经在线上验证过，只能说这是我为避免相似工具误调设计的结构性方案。

## 原文依据：四层方法在哪里看

| 四层方法 | 原文位置 | 你看什么 |
|---|---|---|
| 先抽实体，再路由 | `../../docs/implementation/IMPLEMENTATION_DESIGN.md` §1 Runtime Pipeline + §2 Core Types | `entity_extractor.extract(...)`、`validate_structured_output(...)`、`entity` 字段格式约束 |
| 先分类 query path | `../../docs/implementation/IMPLEMENTATION_DESIGN.md` §3.5 Query Path Classification | `registry_exact / chain / docs_direct / docs_ambiguous`，以及携带高风险实体不得进 `docs_ambiguous` |
| Policy Gate 控制工具集合 | `../../docs/implementation/IMPLEMENTATION_DESIGN.md` §3 Policy Resolution + §3.2 Allow Matrix；`../../docs/design/commitments.md` DC-003 | Deny Layer 先跑，Allow Matrix 只描述能干什么；`address_or_contract_check` 只允许 address registry |
| 不确定就追问 | `../../docs/implementation/IMPLEMENTATION_DESIGN.md` §3.2 Allow Matrix rules；`../../eval/eval-cases.yaml` 的 `neo_n3_tx_status_006` / `tx_failure_diagnosis_002` | network ambiguous 时 ask clarification，不猜 adapter |

## 关键金句

> **“相似工具误调不是靠把 tool description 写长解决的，而是靠 route-before-tool-use：先抽实体和风险，再定 query path，再由 policy gate 裁剪工具集合。”**

> **“Docs Retriever 负责解释，Registry 负责背书；这两个职责不能混。RAG 可以告诉用户 Neo X 是什么，但不能告诉用户某个 bridge 地址是不是官方。”**

> **“Neo N3 和 Neo X 看起来都是查交易，但失败语义完全不同：N3 看 application log / VM state，Neo X 看 receipt / revert reason。network 不明确时不能猜，必须追问。”**

> **“LLM router 在我这里只是候选生成器，不是最终授权器。最终能调用什么工具，由 deterministic Policy Gate 决定。”**

## 被继续追问时怎么答

### Q: 如果 LLM router 选错了怎么办？

答：

> LLM router 选错不是灾难，因为它不是最终裁决点。rule router 和 Deny Layer 会先覆盖 critical intent；Policy Gate 会根据 intent、risk、entities 决定 allowed tools。如果 intent 和实体不匹配，比如带 address 却想走 docs ambiguous，query path classification 会挡住。

### Q: 如果两个工具都能回答一点，为什么不都调？

答：

> 高风险事实不能用“多调几个工具然后让模型综合”解决。比如 official address，docs 可能召回到含地址的页面，但 officialness 的裁决仍然必须来自 registry exact match。可以用 docs 做解释，但不能用 docs 放行官方性 claim。

### Q: 为什么不是让模型先 plan，再自己决定工具？

答：

> 因为这个场景的错误代价高。普通信息问答可以让模型自由 plan，但 Web3 support 里工具调用会影响官方背书和资金安全。我的设计是让 LLM 做候选路由，动作授权由 policy gate 控制。

### Q: 你怎么验证这个设计真的防误调？

答：

> 我已经把误调场景写进 `eval-cases.yaml`，比如 official link / address check 禁止 docs retriever，network ambiguous 禁止直接走 N3/EVM adapter，prompt injection 禁止改变 tool policy。下一步需要接 runner，检查 required_tools / forbidden_tools / answer_mode 是否符合 expected。

## 当前短板

- 还没有实际 runner 结果，不能声称误调率已经下降到某个数。
- `eval-fixtures.yaml` 已补，但 runner 还没实现执行。
- 真实 Neo 官方 source owner / provider 未确认，所以 registry 仍是 fixture / candidate source 层，不是生产 source。
