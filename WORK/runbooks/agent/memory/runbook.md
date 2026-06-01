# Agent Runbook · Memory

> 索引和使用方式在 [README.md](../README.md)。模板在 [`META/templates/runbook_entry.template.md`](../../../../META/templates/runbook_entry.template.md)。

---

## P-040：过时记忆被当作当前事实权威引用

`type: remedy-menu`   `severity: reversible-cheap`

**症状**
- Agent 引用了"某函数在文件 A 的第 23 行"，但那个函数早已重构到别处
- 记忆里存的是两个月前的项目结构，agent 还在按它做决策
- 用户发现 agent 给出的信息听起来很权威但实际上过时了，而且用户一开始根本没有怀疑
- 越具体的记忆（含文件路径、行号、数值）被错误引用时造成的误导性越强

**根因**

记忆是时间点快照，不是实时状态。但被注入上下文时如果没有时效标注，模型会把它当作当前事实——因为它出现在上下文里就意味着"相关且可信"。记忆的"权威感"来自具体性，而不来自时效性。

**当前方案**

*方案 1：所有注入记忆必须附带时效标注（默认先上）*

注入记忆时附加：
- 今天或昨天写的 → 不加警告
- 超过 N 天的 → 附加声明："这条记忆是 N 天前写的，里面关于代码行为或文件位置的描述可能已过时，在基于它做决策之前请先验证当前状态"

关键：**打破虚假的权威感**——告诉模型"这只是过去某个时间点的观察，不是当前事实"。

*方案 2：按记忆类型设不同时效阈值*

- 代码相关记忆（文件路径 / 函数名 / 行号）→ 衰减快，48h 就应该警告
- 项目进展 / 决策记忆 → 中等，1-2 周警告
- 用户偏好 / 习惯记忆 → 衰减慢，30 天警告

*方案 3：记忆访问后加验证步骤*

在 agent 访问记忆后、采取行动前，加一个工具调用验证步骤——用 `read_file` / `search` 等工具验证记忆里的具体 claim 是否仍然成立，确认后再行动。

**适用与失效**
- 适用：任何使用跨会话记忆的 agent 系统
- 失效：记忆内容本就是"历史记录"语义的（用户的过去偏好、项目历史决策）——这类记忆本来就是历史，过期警告可能反而造成混乱；需要按记忆类型区分处理

**源**

`[[agent-memory-system]]`（Cloud Code 真实事故：旧记忆里的函数位置，模型权威引用，用户一开始没有怀疑；过期警告机制的设计动机和实现）。验证状态：部分验证（事故和机制来自 Cloud Code 源码注释）。

**See also**
- `[[memory-temporal-annotation]]`（DC pattern）
- `[[agent-memory-system]]`

---

## P-041：Skills/SOP 未维护导致过时流程被执行

`type: remedy-menu`   `severity: reversible-cheap`

**症状**
- Agent 找到了一个已保存的 Skill/SOP，按照它执行，但步骤已过时（API 接口变了、部署流程改了、环境变量名不同了）
- 系统里积累了大量"一次写好但从未更新"的 Skill，agent 每次执行都踩同样的坑
- "过时的 Skill 让 agent 更自信地走错路"——比没有 Skill 还糟糕

**根因**

Skill/SOP 在首次创建后如果不随使用中的发现即时更新，会迅速变成负资产——它以明确的权威形式存储了错误信息，agent 执行时不会质疑。**过时的 Skill 比没有 Skill 更危险**，因为它让 agent 以"已知正确流程"的信念去执行错误步骤。

**当前方案**

*方案 1：在 agent 的 system prompt 里写入即时更新指令（默认先上）*

明确写入："当使用 Skill 发现它过时 / 不完整 / 错误时，立即用 patch 操作更新它——不要等到被要求。Skills that aren't maintained become liabilities."

*方案 2：Skill 执行失败时触发审查*

执行 Skill 某步骤失败时，先不直接报错，而是触发一次 Skill 审查：
- 当前步骤是否应该更新？
- Skill 整体是否仍然可用？
- 如果过时：更新后重试；如果不可用：标记为 deprecated 并走完整执行路径

*方案 3：Skill 文件加时效字段*

给 Skill 文件加 `last_validated_at` 字段，超过阈值后在 Skill 索引里附上"此 Skill 可能已过时，请验证后使用"警告（类似 P-040 的过期标注机制）。

*方案 4：单调增规模防腐规则*

只增不减的 Skill 系统最终会变成"大泥球"。定期（如每季度）审查所有 Skill：删除从未被调用的 / 标记执行成功率低于阈值的为 deprecated。

**适用与失效**
- 适用：任何使用持久化 Skill/SOP/Procedure 系统的 agent
- 失效：一次性任务 agent（不积累 Skill）；任务域变化频率极低的系统（Skill 几乎不会过时）

**源**

`[[agent-skills-closed-loop]]`（Hermes Skills 设计："Skills that aren't maintained become liabilities"；Skill 的持续修订机制和 `skill_manage(action='patch')` 即时更新约束）。验证状态：未验证（外部 claim）。

**See also**
- P-040 过时记忆被当作当前事实（同类"时效性失效"问题，记忆层的版本）
- `[[memory-temporal-annotation]]`（DC pattern，时效标注机制）
- `[[agent-skills-closed-loop]]`
