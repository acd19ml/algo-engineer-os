# Constraint at Decision Point

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你的 agent 同时配置了"万能工具"（如 bash / exec）和"专用工具"（如 file_read / search / grep），并且你希望模型优先使用专用工具时，先打开这条。

更广泛地：任何你希望模型在选择工具时遵循某种约束的场景，都应先检查约束放在哪里。

不适用：agent 只有一类工具（没有专用 vs 万能的分层）；约束本身是高层业务策略（不适合放在工具 docstring 里，需要放在 system prompt）。

## 结构性不变量

工具使用约束（偏好、禁止、条件限制）必须放在工具描述（docstring / description 字段）中，即约束位于模型做工具选择决策的最近处；不得只把约束写在 system prompt 中作为远端软指令。

## 它预防的症状簇

- P-020：给了 agent 万能工具后专用工具被弃用 → 把"不要用 bash 做文件读取，用 file_read"写在 bash 的工具描述里，模型每次考虑是否调用 bash 时都能看到约束；而 system prompt 里的同样内容在长对话中会被新信息冲刷稀释。

## 留在 runbook 的部分

- P-020 方案 2 权限层硬约束（禁止 bash 执行 cat / grep / ls 等命令）：这是 belt-and-suspenders 兜底，属于运行时强制执行机制，和本 pattern 互补（软约束 + 硬约束）。运行时执行层面的策略留在 runbook，不进 pattern。
- P-022 分层权限规则：工具级别的"禁止"档可以和本 pattern 配合，但那是权限控制框架，见 [[three-tier-deny-overrides-allow]]。

## 代价 / 范围

- 代价：需要在每个工具的描述中维护约束信息；当工具间的偏好关系改变时（如新增专用工具），需要更新相关工具的 description；工具描述变长会增加 context 长度（但工具描述是 Immutable Prefix 的一部分，对缓存友好）。
- 适用：任何同时存在"万能工具 + 专用工具"层次的 agent；任何"模型在工具选择时需要遵循约束"的场景。
- 失效：约束是高层业务策略（如"用户 A 级别可以用 web_search，B 级别不行"），这类权限性约束不适合放工具描述，应该通过动态加载工具集来控制（用户 B 压根看不到 web_search）。

## 实例化成项目 DC 时要补的校验

- 架构：每个"万能"或"高风险"工具的 description 字段包含明确的使用前提和让位说明（"除非专用工具无法完成，否则不要使用本工具"）；工具描述中列出对应的专用工具名。
- 静态检查：扫描所有工具定义，确认万能工具（bash / exec / shell / eval 等）的 description 里包含对专用工具的显式引用或让位说明。
- eval：构造混合 benchmark（包含"应该用专用工具"和"确实只有万能工具能做"两类任务），测量专用工具在前一类任务上的调用率（期望 ≥ 80%）。
- 人工 review TODO：每次新增工具时，检查是否需要更新相关万能工具的 description（新增 `code_search` 后是否更新了 bash 的让位说明）。

## 前沿问题

- 工具 description 和 system prompt 两处约束信息是否会在模型注意力分布上产生冲突（两者说法不一致时哪个优先）？
- 工具描述的最大有效长度是多少？约束文字过多会不会反而让模型注意力稀释？
- 对于通过 tool_search 按需加载的延迟工具集，这些工具的 description 在加载前不存在，约束信息应该放在 tool_search 的结果里还是 system prompt 里？

## 源

`[[agent-tool-design]]` + P-020（原则一，工具描述里写让位说明段）。

验证状态：未验证（Cloud Code 外部设计 claim，未在本地项目实例化验证）。

## 演进日志

- `2026-05`：从 P-020 的"关键原则：约束放在最接近决策点的地方"段抽出不变量。P-020 方案 2 权限层硬约束明确留在 runbook，委托给 [[three-tier-deny-overrides-allow]]。
