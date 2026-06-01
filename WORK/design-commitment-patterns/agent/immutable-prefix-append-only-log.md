# Immutable Prefix + Append-Only Log

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你设计使用前缀缓存 API（DeepSeek / Anthropic / OpenAI）的 agent loop，且对话历史会随 turn 增长时，先打开这条。

不适用：每次请求内容完全不同（如批量翻译不同句子），前缀缓存本来就没价值；本地推理（无前缀缓存 API），上下文管理用 P-006 的 Tiered Compact 更合适。

## 结构性不变量

上下文必须分三个区域，各有严格不变性约束：

- **Immutable Prefix**（system prompt + 工具定义 + few-shot）：会话开始时固定，整个会话不可变；工具定义的顺序、序列化方式、空白字符全部锁定；用内容 hash 追踪漂移，发现变化立即报错。工具定义是 Immutable Prefix 的一部分，不得为可见性控制目的而增删改（→ 用 logit mask 或两级加载控制可见性，不改定义本体）。
- **Append-Only Log**（对话历史）：只能向末尾追加新消息，不得修改、重排或删除已有消息；工具调用失败信息以追加形式进 Log，不得回滚历史再重试。
- **Volatile Scratch**（思维链 / 临时计划）：不发送给 API；每轮结束时清空；需要持久化的有用信息通过工具调用以结构化形式追加进 Append-Only Log。

## 它预防的症状簇

- P-014：前缀缓存命中率低 → 三区域设计保证前 N 个字节在所有请求中完全相同，缓存命中率从 2~30% 提升到可接近 90%（Reasonix case：$1.38 vs 无缓存估算 $61）。
- P-012：动态增删工具定义废 KV cache → 工具定义属于 Immutable Prefix，不动态增删；可见性控制走 logit mask 或两级加载，不触碰定义本体，缓存稳定。

## 留在 runbook 的部分

- P-014 Cache Line Fold（上下文超限时如何压缩而不破坏缓存）：这是 [[immutable-prefix-append-only-log]] 成立后上下文过长时的压缩运行时方案，见 P-015。
- P-016 Storm 滑动窗口行为循环检测：这是 Append-Only Log 上的运行时监控机制，属于检测 + 干预流程，不是结构性不变量。
- P-012 方案 1 Logit Masking / 方案 3 两级加载 + tool_search：这是在工具定义不动的前提下控制工具可见性的具体实现方案，留在 runbook。

## 代价 / 范围

- 代价：禁止"删改历史消息"的操作（包括曾经常用的 rewrite-last-message 策略）；上下文只增不减，需要配套 P-015 Cache Line Fold 来管理长度；工具定义一旦锁定，版本变更需要新建会话。
- 适用：高频调用同一 API 且有大量重复前缀的 agent loop（典型场景：编程助手、客服 agent、多轮检索）。对 DeepSeek 尤其重要（自动字节匹配缓存，规则严格）；Anthropic 还需额外显式标记 cache_control。
- 失效：本地推理（无前缀缓存 API）——这时 Append-Only 约束是不必要的成本，应该用 P-006 Tiered Compact 主动删旧内容。
- 注意：和 P-006 方案 1（删 / 截断旧内容）直接冲突。二选一：关心 API 缓存成本 → 本 pattern；关心 OOM / 本地推理 → P-006。

## 实例化成项目 DC 时要补的校验

- 架构：agent loop 中存在唯一的 `context_builder` 组件，它将上下文分为三段输出；不存在任何修改 Append-Only Log 历史条目的代码路径；工具定义序列化函数是幂等的（同输入永远同输出）。
- 静态检查：扫描代码，确认不存在对 `messages[i].content = ...`（修改历史消息）或 `messages.remove(i)` 类似的操作；确认工具定义在会话生命周期内不重新序列化（或序列化结果通过 hash 验证一致）。
- eval：连续发送 10 个 turn 请求，用 API 的 usage 字段或 SDK 的 cache metrics 确认缓存命中率 ≥ 目标阈值（建议 80%+）。
- 人工 review TODO：代码评审时标记所有"修改 messages 数组"的操作点，逐一确认是否真的必要；如果有，必须另建新会话而不是改写历史。

## 前沿问题

- Anthropic cache_control 的显式标记和 OpenAI / DeepSeek 的自动字节匹配在粒度上有本质差异，三区域设计在跨 provider 场景下需要多少适配？
- Volatile Scratch（思维链）不发 API 时，这部分 token 是否影响 Immutable Prefix 的有效长度（provider 是否把 CoT 计入前缀 hash）？
- 随着模型能力提升，Immutable Prefix 里的 few-shot 示例是否会逐渐变成冗余负担？在什么条件下可以安全压缩 few-shot？

## 源

`[[cache-aware-agent-loop]]` + P-014（三区域设计段）、P-012（工具定义稳定作为子不变量）。

验证状态：未验证（Reasonix case study 是外部 claim，未在本地项目实例化验证）。

## 演进日志

- `2026-05`：从 P-014 三区域设计抽出核心不变量，吸收 P-012 工具定义稳定要求作为 Immutable Prefix 的子约束。P-014 Cache Line Fold、P-016 Storm 检测、P-012 Logit Masking 和两级加载方案明确留在 runbook。
