# Q: 你的 agent 里 LLM 参与决策,而 LLM 输出非确定。你怎么评测这个系统?为什么用 mock 的 router 跑,而不是直接接真实 LLM?这样的指标能说明什么、不能说明什么?

## 来源

- 出处:Neo 官网智能客服项目把 eval harness 实现并跑出指标后,对"评测方法本身"的深挖。
- 频率:高。只要简历里出现 `eval / harness / LLM router / 指标`,技术面和研究面很容易追问"你这个有 LLM 的系统,指标怎么算的、可复现吗、说明了什么"。
- 性质:这是 system-design 级的方法论题,不是某个算子的机制题——但同样能用"从问题出发、沿因果链推导"的五层框架组织(见 `KNOWLEDGE/methodology/answer-form-for-mechanisms/`)。

## 涉及文档

- 主:`../../prototype/eval_runner/`(`sut.py` 确定性管线、`router.py` 双 router、`metrics.py`、`run_eval.py`)
- 主:`../../eval/eval-prototype.md` §9(Result 表 + §9.3 诚实口径)
- 相关:`../../eval/eval-runner-spec.md` §2(五个 runner 模式)
- 相关:`../../docs/implementation/IMPLEMENTATION_DESIGN.md` §1 / §3 / §6
- 相关:`../../docs/design/commitments.md` DC-002 / DC-003 / DC-004

## 我的答案(面试 2 分钟版)

先点破一个容易被混淆的地方:我系统里有两种"确定性"东西,**只有一种是 mock**。

- **被 mock 的**只有"语义意图分类"这一步——真实里它该由 LLM 做。
- **不是 mock 的**是 secret 检测、deny 规则、Allow Matrix、query-path、grounding verifier 这些**安全层**;它们是系统本身,设计上就要求确定性、并且**覆盖** LLM 的输出(DC-002/003/004)。换不换真实 LLM,这一层一行都不动。

所以"为什么 mock 而不直接接 LLM",真正的答案是:**mock 和真实 LLM 回答的是两个不同问题,不是替代关系。**

- **mocked-oracle 模式**:给定正确意图,测"我的确定性机器对不对、安全不变量成不成立"。它可复现、能隔离 bug——一个 case 失败 = 我的 gate 错了,不是 LLM 猜错了。我就是靠它在首跑 97/100 时干净地定位并修掉 3 个真实路由 bug。
- **real-LLM 模式**:让一个故意便宜/弱的 LLM(GLM-4.7-Flash)做意图,测"router 噪声很大时,`critical_bypass_rate` 是否仍为 0"——这才是"LLM 提案、确定性层裁决"这条命题被证伪的地方。

如果一上来就直接接真实 LLM,信号会**二义**:一个失败分不清是我的 gate 错还是 LLM 分错意图,我会在两个变量里盲调,还可能为了迁就 LLM 的怪癖去改 gate(=对 LLM 噪声过拟合);而且 LLM run-to-run 会抖,数字进不了 Result 表当 ground truth。

**指标能说明什么**:在 mocked 模式下,100 条 case 结构性全过,`critical_bypass = 0/21`、secret 不落原文、route-before-rewrite `56/56`、tool error 分类 `5/5`、handoff 触发 `6/6`——这些证明确定性安全层的不变量是可执行、成立的。
**不能说明什么**:它**不是真实 router 准确率**;deny 启发式是对着这 100 条写的,100% 含**过拟合风险**;`verified-hard-claim 100%` 是 typed-slot 的构造性结果,不是抗幻觉压测。这些我都写进了 `eval-prototype.md` §9.3,不会拿去当业务通过率。

## 展开版(沿因果链 / 五层)

### L1:这个评测要解决什么问题(范式转换)

朴素做法是把系统当黑盒,跑一批 case 算端到端准确率。但这里有 LLM 参与,**LLM 非确定**——同一条输入两次跑可能给不同意图。黑盒准确率因此有两个毛病:(1) 不可复现,没法当 ground truth;(2) 即便复现了,一个数字也说不清"是模型对还是我的工程对"。

范式转换是:**不把 LLM 当事实/安全裁决者,而当不可信的提案者;安全由确定性层裁决。** 评测范式随之从"测端到端一个数"变成**分层测两个不同的东西**——

- "给定正确意图,我的确定性机器对不对?"(可复现,隔离工程 bug)
- "给定真实噪声意图,安全是否仍守得住?"(真实信号,验安全命题)

把这个拆分点出来,面试官就知道你不是在 reportbug,而是在做受控实验。

### L2:每个设计选择背后的动机(反事实)

- **为什么 deny / verifier 是确定性,而不是写进 prompt?**
  反事实:如果让 LLM 判断"这是不是 secret/写链请求"或"这个 address claim 该不该放行",你就把安全交给了一个**你不信任、还非确定**的组件。DC-002/003/004 的整个点就是:critical 决策必须可审计、可复现、结构上不可绕过。所以 deny 层跑在 LLM **之前**并覆盖它。

- **为什么用 mock 的 router,而不直接接真实 LLM?**
  反事实:直接接真实 LLM,首跑分数更低且每个失败二义(gate bug? LLM 噪声?),我会同时 debug 两层,还可能对 LLM 的具体怪癖过拟合;分数 run-to-run 抖,"我这个 fix 到底有没有用"都判断不了。oracle 给我**干净信号**:失败必定是我的机器问题。

- **为什么 mock 要做成 oracle(给正确意图),而不是做个笨 mock?**
  反事实:笨 mock 失败时,分不清是"机器错"还是"意图喂错"。oracle 把意图当已知正确,失败就唯一指向机器——这才能当回归基线。

- **为什么两个 router 都要,不是二选一?**
  因为它们答不同问题(见 L1)。oracle 答"机器对不对",真实 LLM 答"噪声下安全守不守得住"。所以 §9.1 和 §9.2 在文档里分开列,且永远保留 oracle 行做对照。

### L3:工程演进线

`eval-runner-spec.md` §2 定义了五个模式,是一条**逐步放开确定性、逐步逼近真实**的演进线:

1. `fixture_coverage_check`:连 case 引用的 fixture 都不齐就别谈指标。
2. `policy_only` / `deterministic_fixture`:oracle 意图 + 确定性管线 → **我现在跑的,§9.1**。
3. `llm_router_integrated`:真实 LLM 做意图,确定性 gate 仍裁决 → **下一步,§9.2,验 `critical_bypass` 仍为 0**。
4. `full_prototype`:再接 LLM **自由文本 answer compiler** → 才能真正压测 grounding verifier 对"散文里夹带未校验硬事实"的拦截。

驱动力很清楚:每放开一层 LLM,就多暴露一类风险,但前面已验过的确定性不变量给你兜底,不至于一次性面对所有不确定性。

### L4:工程感知(这里不是硬件,是可复现 / 成本 / 确定性)

- **可复现性**:mocked 模式无网络、无随机,跑一万次同一张表,所以它的数字能进 Result 表。
- **LLM 模式的抖动**:即便 `temperature=0`,很多端点也不保证逐 token 确定;真要把 LLM 模式的数字写进文档,得记**模型 ID + 日期**,必要时**多 seed 看方差**。而 `critical_bypass` 这类安全指标本来就该跨 seed 稳定为 0——不稳定本身就是 bug 信号。
- **成本**:100 条 × 每条一次调用,flash 模型很便宜;但 oracle 让我开发期零成本、零依赖、不用别人的 key 反复打。

### L5:开放性思考

- **deny 启发式的过拟合,换 LLM 治不了。** 我对着这 100 条调过 `approve / 收益 / 连接钱包` 的关键词。但 deny 跑在 LLM **之前**,真实 LLM 根本碰不到它——所以"换真实 LLM"完全不验证 deny 层。要验它,得靠**留出集 / 新增多语言 adversarial case**,或未来把关键词 deny 换成小分类器、但保留确定性兜底。这是真正的短板,不能用"接 LLM"假装解决。
- **评测的"裁判"也该确定性。** 为什么不直接 LLM-as-judge?因为硬事实放行不能交给 LLM(DC-004,LLM/NLI 只 advisory);裁判若非确定,评测本身就不可复现。
- **这套"分层 + oracle 基线 + 噪声验安全"能泛化到哪些有 LLM 在 loop 的系统?** 凡是"LLM 提案 + 确定性兜底"的架构(tool-use agent、code agent、审批流)应该都适用;纯生成类(没有可裁决的确定性边界)可能就不适用——这条我还没完全想清楚。

## 关键金句

> **"我系统里只有'语义意图'是 mock 的;secret 检测、deny、verifier 这些安全层不是 mock,是系统本身,换不换 LLM 都不动。"**

> **"mock 测的是'机器对不对',真实 LLM 测的是'噪声下安全守不守得住';两者答不同问题,不是替代关系。"**

> **"deny 和 verifier 是确定性的,正因为它们是安全裁决者——你不能把安全交给一个你不信任、还非确定的组件。"**

> **"我先用 oracle 把机器调对(信号干净),再用真实 LLM 验安全(信号真实);不是一上来在'我 gate 错没错'和'LLM 猜错没猜错'两个变量里盲调。"**

> **"100% 是 mocked-oracle 下的结构一致性,不是真实准确率;deny 启发式有过拟合风险,而换 LLM 治不了它——deny 跑在 LLM 之前,得靠 held-out。"**

## 被继续追问时怎么答

### Q: mock 跑出 100% 不就是"自己测自己"吗?

> 安全指标不是。`critical_bypass / secret 不落原文 / route-before-rewrite / tool error 分类 / handoff` 都是从 `user_message` + fixture **推导**出来的,不看 expected。比如 `neo_gas_role_008` 在 allow 套件里,却因为检测到投资意图被 deny-overrides-allow 拦下;`neo_n3_tx_status_009` 因为 fixture 返回 provider hard_error 翻成 handoff。真正用了 oracle 意图的只有"良性概念分桶"那一处(basic_explain vs token_explain vs official_navigation),其它都是真算的。

### Q: 那接真实 LLM 跑,分数会不会掉下来?

> `policy_resolution` 可能掉,因为弱 LLM 会分错意图——这正常,也正是要测的。但 `critical_bypass` 应该**仍为 0**,因为 deny 层覆盖 LLM。如果它不为 0,说明我的"LLM 提案、确定性裁决"命题有漏洞,那才是要修的真 bug。

### Q: 为什么不直接用 LLM-as-judge 来评测?

> 硬事实(URL/address/tx status)的放行不能交给 LLM——DC-004 明确 LLM/NLI 只 advisory,无权放行硬事实。而且裁判若非确定,评测本身就不可复现。所以我的裁判是确定性 exact-match,LLM 最多在软叙述上做参考。

### Q: 可复现性到底怎么保证?

> mocked 模式:无网络、无随机,逐次一致。LLM 模式:记模型 ID + 日期、`temperature=0`、必要时多 seed 报方差;并且把"安全指标跨 seed 必须稳定为 0"当成验收门槛——抖动即 bug。

### Q: 怎么防 deny 启发式过拟合?

> 诚实说:现在没防住,只在 §9.3 标了风险。正确做法是加**留出集**和**多语言 adversarial**,而不是接 LLM(deny 在 LLM 之前,接 LLM 不验它)。再进一步可以把关键词 deny 换成小分类器,但必须保留确定性兜底,不能让 LLM 成为唯一的安全闸。

## 原文依据:五层在哪看

| 层 | 原文位置 | 你看什么 |
|---|---|---|
| L1 范式 | `../../docs/implementation/IMPLEMENTATION_DESIGN.md` §1 + `../../docs/design/commitments.md` DC-002/003 | LLM 只做意图;deny 跑在 router 前并覆盖它 |
| L2 设计/反事实 | `../../prototype/eval_runner/router.py`(MockedRouter 是 oracle / LLMRouter env 配置)+ `sut.py`(deny 层在 router 之前) | 被 mock 的只有意图;安全层是确定性系统本身 |
| L3 演进 | `../../eval/eval-runner-spec.md` §2 五个模式 | coverage → policy_only → deterministic_fixture → llm_router_integrated → full_prototype |
| L4 工程感知 | `../../eval/eval-prototype.md` §9.1 / §9.3 + `../../prototype/eval_runner/run_eval.py` | mocked 可复现;LLM 模式记模型+日期、多 seed |
| L5 开放 | `../../eval/eval-prototype.md` §9.3 + 本文 L5 | deny 过拟合换 LLM 治不了;裁判须确定性 |

## 当前短板

- **§9.2 的 LLM 模式还没跑**,所以"噪声下 `critical_bypass=0`"目前是**预期、不是实测**;真跑完才能把这句话从设计承诺变成结果。
- **deny 启发式的过拟合未用 held-out 验**,mocked 100% 不能解读成真实准确率。
- **`full_prototype` 自由文本 compiler 模式未建**,所以 grounding verifier 对"散文夹带硬事实"的拦截还没被真正压测过,`verified-hard-claim 100%` 仍是构造性结果。
- **真实 Neo provider / source owner 未确认**,registry 仍是 fixture / candidate,不是生产 source。
