# Background Agent Excluded from Recovery Triggers

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你设计的 agent 系统中存在"后台自动触发的子任务"（如记忆提取、上下文压缩、skill 更新等），且这些子任务本身是为了应对某类系统问题而 fork 出来的，先打开这条。

不适用：所有 agent 任务同级运行，没有"后台维护类子任务"的区分；子任务已经明确隔离在独立沙箱中。

## 结构性不变量

后台维护类子 agent（为了处理某类系统问题而创建的 fork，如压缩子 agent、记忆提取子 agent）发出的请求，不得触发与其自身创建目的相同的自动恢复机制；违则形成递归死锁。

## 它预防的症状簇

- P-026：上下文压缩连续失败，系统不停重试浪费 API 调用 → 压缩子 agent 不能再触发压缩，否则会无限嵌套；通过来源标记（QuerySource）排除子 agent 的请求不进入自动触发逻辑，递归死锁从架构层不可能发生。

## 留在 runbook 的部分

- P-026 方案 1 连续失败熔断器（连续 N 次失败就停止重试）：这是针对"普通请求重复失败"的运行时限制，是通用的 [[retry-budget-hard-cap]] 机制；本 pattern 专门针对"子 agent 本身触发同类问题"的递归场景，两者互补不重叠。
- P-026 方案 3 压缩请求本身超长时的处理：这是压缩输入管理的运行时过程，不是排除递归的结构性不变量。

## 代价 / 范围

- 代价：需要给每个 agent 请求附加来源标记（QuerySource 或等价元数据），并在触发逻辑里检查来源；增加轻微工程复杂度。
- 适用：任何存在"为处理 X 而 fork 出子 agent"的系统，且 X 本身可能递归触发同一 fork 的场景。
- 失效：系统中所有 agent 任务同级、不存在"维护类子任务"的区分时，不需要这层。

## 实例化成项目 DC 时要补的校验

- 架构：所有 agent 请求携带来源标记（`query_source: "main" | "compaction_agent" | "memory_agent" | ...`）；自动触发逻辑（压缩触发、记忆提取触发等）在执行前检查来源，来源为维护类子 agent 时跳过触发。
- 静态检查：扫描代码中所有"fork 子 agent"的调用点，确认 fork 出的子 agent 的请求不会进入与其目的相同的触发路径（如压缩 agent 的请求不进入"触发压缩"逻辑）。
- eval：构造"压缩子 agent 上下文过长"场景，验证系统不会再 fork 一个压缩子 agent（不触发递归），而是直接失败或报告给主 agent。
- 人工 review TODO：新增维护类子任务时，代码评审必须检查该子任务的请求是否已被正确排除在相关自动触发逻辑之外。

## 前沿问题

- 来源标记的传播链：如果子 agent 又 fork 了孙 agent，孙 agent 是否自动继承"维护类"来源标记？还是需要显式传播？
- 是否存在"合法的二级维护"场景（如记忆提取 agent 需要对自己的操作做小规模压缩）？怎么设计才不破坏这个不变量？

## 源

`[[agent-context-compaction]]` + P-026（Cloud Code 真实事故：子 agent 排除逻辑，Session Memory 和 Compact 的 QuerySource 不会触发自动压缩）。

验证状态：部分验证（Cloud Code 源码注释中有具体实现描述）。

## 演进日志

- `2026-05`：从 P-026 子 agent 排除逻辑抽出不变量。P-026 的熔断器（retry-budget-hard-cap）作为互补机制留在 runbook。
