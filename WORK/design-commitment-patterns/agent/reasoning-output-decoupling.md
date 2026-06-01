# Reasoning Output Decoupling

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你使用约束解码 / structured outputs / strict mode 来保证 JSON 格式合法性，且模型需要完成带有推理、摘要或解释的生成型任务时，先打开这条。

不适用：纯结构化提取任务（打标签、分类、提取实体），这类任务没有生成型字段，strict 通常安全；模型没有推理阶段（非 CoT 模型）。

## 结构性不变量

推理阶段和结构化输出阶段必须隔离：推理（思考链 / CoT）不施加 schema 约束；schema 约束仅在最终输出阶段施加。生成型字段（summary / explanation / reasoning_text 等）不得开启 strict / constrained decoding。

## 它预防的症状簇

- P-010：开启 strict 后输出语义质量下降 → 推理阶段不受 schema 约束，模型可以自由选 token，关键信息不因 mask 而丢失；最终输出阶段再施加 schema，格式正确不以语义质量为代价。
- P-009（方案 1 滥用）：盲目对整个响应开启 strict，可能同时影响推理字段和结构字段 → 阶段隔离后，只有结构性字段受约束，生成型字段不受影响。

## 留在 runbook 的部分

- P-009 方案 3 验证 + 重试（语法层兜底）：这是 strict 不可用时的运行时恢复流程，不是设计阶段的结构约束。
- P-010 方案 2 按字段分 strict（把 schema 拆成结构字段 strict / 生成字段不 strict）：这是本 pattern 不变量的一种实现方案，但具体字段分法属于实现细节，留在 runbook。
- P-010 方案 3 评估是否真的需要 strict（Bitter Lesson 视角）：这是运行时 A/B 决策，不是设计承诺。

## 代价 / 范围

- 代价：需要把 LLM 调用结构化为两阶段（推理阶段不传 schema，输出阶段传 schema）；或使用支持 thinking 与 output 分阶段的 API（如 Claude API）；整体调用复杂度略增。
- 适用：任何同时包含"推理 / 摘要 / 解释"和"结构化输出"需求的任务；指令微调模型在生成型字段上发现 strict 后质量明显下降时。
- 失效：纯结构化任务（提取、分类、打标签）没有生成型字段，严格开 strict 不会触发此问题，本 pattern 不必要。
- 失效：对话型助手无需保证格式时，整个 schema 约束都可以省略。

## 实例化成项目 DC 时要补的校验

- 架构：LLM 调用流程中，推理调用不包含 response_format / json_schema 参数；仅最终输出调用包含 schema 约束。如果使用原生 thinking API（如 Claude），确认 thinking block 不被纳入 schema 校验。
- 静态检查：扫描所有传递 `strict: true` 或 `response_format: {type: "json_schema"}` 的调用点，确认这些调用点的 schema 中没有字段名包含 summary / explanation / reasoning / description 等生成型字段。
- eval：构造含推理型字段（如 `explanation`）+ 结构型字段（如 `label: enum`）的 schema，分别在 strict / non-strict 两种配置下测 10+ 样本，对比生成型字段内容质量（人工评分或 LLM-as-judge），确认 strict 版本无显著质量下降。
- 人工 review TODO：代码评审时检查混合型 schema（既有枚举又有自由文本字段），确认自由文本字段没有被 strict 约束。

## 前沿问题

- Anthropic extended thinking 和 schema 约束的精确交互规则是什么？thinking block 是否完全绕过 schema 约束？
- 是否存在"推理感知 strict"：仅对结构字段约束，对生成字段只做软格式检查（比如长度、字符集）而非 token mask？
- 随模型能力提升（如 Claude 4.x 以后），在多强的 strict 下推理质量保持不变？threshold 如何量化？

## 源

`[[structured-output]]` + P-009（方案 1 适用范围）、P-010（strict 语义退化根因段）。

验证状态：未验证（来源本身是 qualitative claim，缺少不同模型的退化量化数据）。

## 演进日志

- `2026-05`：从 P-010 的"推理和输出分阶段"方案抽出不变量，吸收 P-009 方案 1 的适用范围说明作为来源。P-009 方案 3 验证重试、P-010 方案 2 按字段分 strict 明确留在 runbook。
