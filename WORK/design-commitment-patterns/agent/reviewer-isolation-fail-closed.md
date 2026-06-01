# Reviewer Isolation + Fail Closed

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你设计 agent 系统中的安全评审机制，且评审者本身也是 LLM 时，先打开这条。包括：multi-agent 系统中的 critic / reviewer 角色、操作前安全审查、权限动态评审等。

不适用：评审者是确定性规则（正则 / 列表匹配），不存在被自然语言操纵的问题；无评审层（单 agent 系统，所有控制靠规则）。

## 结构性不变量

LLM 评审者只能读取被评审 agent 的**动作**（工具调用 + 参数），不得读取被评审 agent 的**文字解释**（自我辩护）；评审机制的任何异常（解析失败 / API 错误 / 超时 / 输入不完整）必须 fail-closed（默认拦截操作），不得 fail-open（默认放行）。

## 它预防的症状簇

- P-023：Agent 自己审查自己，被自我辩护绕过 → 评审者只看"agent 做了什么"（工具调用），不看"agent 说了什么"（解释），切断自我辩护路径；fail-closed 保证评审失效时默认拦截，不被"评审系统出错就放行"漏洞利用。

## 留在 runbook 的部分

- P-023 方案 2 两阶段架构（快速 yes/no 过滤 + 完整推理精排）：这是评审效率优化方案（降低成本翻倍问题），属于实现选型，不是结构性不变量。
- P-023 关于"是否可以让评审者看一部分 agent 解释"的 trade-off：这是设计边界问题，留在 runbook 作为 Open Question，不固化为 pattern。

## 代价 / 范围

- 代价：评审者的输入构造需要过滤 agent 文字输出（只传工具调用记录）；fail-closed 意味着评审基础设施故障时合法操作也会被拦截，需要配套的告警和人工接管机制。
- 适用：使用 LLM 做评审的所有场景，不只权限审查——multi-agent 系统的 critic / reviewer / validator 角色都适用这条不变量。
- 失效：评审者是确定性规则（不存在被自然语言操纵的向量）。
- 注意：完全屏蔽 agent 文字解释有时会丢合法上下文（agent 解释了为什么某操作是必要的）。这个 trade-off 是已知 Open Question，项目采纳时需明确立场（允许部分解释 vs 完全屏蔽）。

## 实例化成项目 DC 时要补的校验

- 架构：评审者的 prompt 构造函数中，输入只包含工具调用结构（工具名 + 参数），不包含 agent 的 assistant 消息文本；异常处理逻辑的所有分支（parse 失败、timeout、API error）都返回"拦截"而非"放行"。
- 静态检查：扫描评审 prompt 构造代码，确认没有将 `assistant_message.content`（文字输出）拼入评审输入。
- eval：构造一组"agent 自我辩护测试用例"（agent 工具调用是危险操作，但 agent 文字输出声称"用户已授权"），验证评审者仍然拦截（不受自我辩护影响）；构造"评审服务 mock 500"场景，验证系统 fail-closed（拦截）而非 fail-open（放行）。
- 人工 review TODO：评审输入构造逻辑必须有独立 review，确认不存在"方便调试"而临时加入的 agent 文字输出路径（调试用 workaround 最容易变成永久漏洞）。

## 前沿问题

- 完全屏蔽 agent 文字解释会不会让评审者在某些合法但不寻常的操作上误判？如果允许"摘要式上下文"（不是 agent 原文），边界在哪里？
- 两阶段评审（快速过滤 + 精排）在 fail-closed 语义下如何优雅降级？第一阶段 fail → 直接拦截，还是升入第二阶段？
- 当评审者本身被 prompt injection（来自工具结果）操控时，"只看动作"是否仍然足够（工具参数里可能包含注入内容）？

## 源

`[[agent-permission-system]]` + P-023（YOLO Classifier 段，生成和评估分离设计）。

验证状态：未验证（Cloud Code 外部设计 claim，未在本地项目实例化验证）。

## 演进日志

- `2026-05`：从 P-023 "只看动作不看解释" + fail-closed 原则抽出不变量。P-023 方案 2 两阶段架构留在 runbook（效率优化，不是不变量）。
