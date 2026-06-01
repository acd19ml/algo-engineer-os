# Fail Loud on Bad JSON

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你设计的系统将 LLM 生成的 JSON 作为工具调用参数或下游流程输入时，先打开这条。无论是截断、语法错误还是 parse 失败，都必须有明确的失败行为设计。

不适用：LLM 输出不经过 JSON parse 直接作为文本使用；工具输入完全不依赖 LLM 生成的结构化数据。

## 结构性不变量

工具层解析 LLM 输出的 JSON 失败时（截断 / 语法错误 / 无法补全），必须向上层返回明确错误信号并终止当前工具调用；不得以空对象 `{}`、null 或任意默认值静默替代不完整的 JSON 继续执行工具。

## 它预防的症状簇

- P-018：模型输出 JSON 被截断，工具层静默用空对象执行 → fail-loud 保证截断产生显式错误（而非无声的错误行为），错误进入模型上下文触发重试或纠正，不产生"工具调用了但结果莫名其妙"的静默语义错误。

## 留在 runbook 的部分

- P-018 的可确定性补全逻辑（不平衡括号检测 → 尝试补 `}` 后 parse）：这是在判定"不可恢复"之前的一次确定性修复尝试，属于运行时恢复过程。判定不可恢复后才触发 fail-loud；补全逻辑本身不是不变量。
- P-009 方案 3 验证 + 重试（语法层 rescue parse）：P-001 / P-009 的救援解析是另一层恢复机制，和 fail-loud 的关系是"能补就补，不能补就 fail loud"，顺序先后留在 runbook 里描述。

## 代价 / 范围

- 代价：系统需要为"工具层收到明确错误"设计上层处理逻辑（重试 / 纠正 / abort）；历史上很多框架默认 fail-silent，改为 fail-loud 需要有意识地去掉 `or {}` 这类兜底。
- 适用：所有用 LLM 输出 JSON 喂工具的场景，无例外。Fail-loud 是防御 silent failure 的最低保证。
- 失效：无（这是通用原则，没有应该 fail-silent 的场景——静默用默认值最多在极少数"有合法业务默认值"的参数上可接受，但必须显式设计而非框架自动补全）。

## 实例化成项目 DC 时要补的校验

- 架构：工具 Dispatcher 的 JSON 解析逻辑中，parse 失败路径不存在 `except: return {}` / `return None` 类似的静默兜底；所有失败路径都会 raise 或 return 带错误信息的结构体。
- 静态检查：grep 代码中 `json.loads` / `JSON.parse` 的 except/catch 块，确认没有静默返回空对象或 None 的分支。
- eval：构造截断的 JSON 样本（缺 `}`）、完全损坏的 JSON 样本，喂入 Dispatcher，期望：（1）返回明确错误而非成功响应；（2）错误信息足够具体（"JSON 截断：缺少闭合括号"，不只是"parse 失败"）。
- 人工 review TODO：代码评审重点检查任何"parse JSON → 如果失败怎么办"的代码路径，确认 fallback 不是空对象。

## 前沿问题

- 当可确定性补全（检测缺 `}` 然后补上）和 fail-loud 之间的界线在实践中如何画？哪些情况"尝试补全是合理的"，哪些情况"应该直接 fail loud"？
- 对于嵌套很深的 JSON，截断检测（括号配对）会不会在某些合法 edge case 上误判为截断？
- 随着模型能力提升，截断是否会变成小概率事件，使得 fail-loud 的"拦截率"接近于零但仍必须保留？

## 源

`[[cache-aware-agent-loop]]` + P-018（工具调用修复管道 / Truncation 段）。

验证状态：未验证（外部 claim，未在本地项目实例化验证）。

## 演进日志

- `2026-05`：从 P-018 "fail loud, not silent"原则抽出不变量。P-018 的可确定性补全逻辑和 P-009 救援解析明确留在 runbook（恢复过程）。
