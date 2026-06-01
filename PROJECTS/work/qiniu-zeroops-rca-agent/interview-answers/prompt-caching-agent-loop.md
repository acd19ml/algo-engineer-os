# Q: 你知道 Prompt Caching 吗？有没有看过 Claude Code 源码？它是怎么做的？

## 来源

- 出处：技术面深问（考察 LLM infra 认知深度 + 工具素养 + 能否连回自身项目）
- 频率：中（Agent 工程方向面试偶发，但能答出三层的人少）

## 涉及节点

- `KNOWLEDGE/agent/cache-aware-agent-loop/` — DeepSeek Reasonix 产品分析（三区域设计 + 44x 成本差）
- `KNOWLEDGE/agent/small-model-harness-engineering/` — Forge 五层防护（第五层压缩破坏缓存）
- 关联：`qiniu-react-context-management.md`（同目录）（自身项目上下文管理）

---

## 第一层：机制（KV activations，不只是"文字缓存"）

LLM 每次处理文本，都在 Transformer 的每个 attention 层计算 Query / Key / Value 矩阵。**Prompt Caching 缓存的是这些 KV activations**，不是原始文字。

```
普通请求：
  System Prompt (3000 tokens) + 对话 (500 tokens)
  → 每次全部重算 3500 tokens 的 KV
  → 慢 + 贵

Prompt Caching 命中：
  System Prompt 部分直接复用 KV activations，跳过前向计算
  → 只计算新增的 500 tokens
  → 快 + 便宜（Anthropic: cached token 约为普通 input 的 1/10）
```

**Cache TTL = 5 分钟**（Anthropic），每次命中刷新计时。超时失效，下次重新付全价。

### Anthropic API 用法（显式标记断点）

```python
client.messages.create(
    model="claude-opus-4-7",
    system=[{
        "type": "text",
        "text": "长 system prompt（工具定义 + 角色设定 + SOP...）",
        "cache_control": {"type": "ephemeral"}   # ← 断点
    }],
    messages=[{"role": "user", "content": "当前输入"}]
)
```

断点之前的内容必须在多次请求中**字节完全一致**，差一个字符，缓存失效。最多可设 4 个断点。

---

## 第二层：数量级感知（为什么值得认真对待）

来自 DeepSeek ReasonX Coding Agent 的真实数据（2026-05-01）：

> 同一个用户，同一天，同一批工作量（4.35 亿 input token）：
>
> - 缓存命中率高：**1.38**
> - 无缓存优化：**≈ 61**
> - **成本差：44 倍**

原因：DeepSeek 的 cache hit token 收费是 cache miss 的 **1/50**。

**关键结论**：缓存由 provider 端自动维护，**命中率完全由客户端决定**。大多数 Agent 框架命中率只有 2–30%——不是 provider 不给，是客户端在无意识地破坏缓存。

---

## 第三层：三种最常见的无意识破坏行为


| 破坏方式         | 触发场景                    | 根本原因                       |
| ------------ | ----------------------- | -------------------------- |
| **工具定义重序列化** | 每次请求前 JSON 序列化工具 schema | 字段顺序/空格可能变 → 前缀字节不同 → miss |
| **CoT 进入历史** | 推理模型的思维链被记录到对话历史        | 下一轮前缀包含上一轮特有思维链内容 → 前缀永远不同 |
| **压缩改写历史**   | 删除旧消息 / 用摘要替换旧消息        | 从被改那条开始，之后所有字节失效           |


第三条最重要，也是下面 Forge 张力的核心。

---

## 第四层：Reasonix 的解法 — 三区域设计（Append-only 纪律）

DeepSeek ReasonX Coding Agent 把整个上下文切成三个区域：

```
[区域一] Immutable Prefix（不可变前缀）
         系统提示词 + 工具定义列表 + few-shot 示例
         对话开始后字节级不变，有指纹追踪
         约束：工具定义顺序不能变、system prompt 不能动态注入变量

[区域二] Append-only Log（只追加日志）
         对话历史：只追加，绝不修改/删除/重排
         每次新请求的前缀 = 上次完整内容 + 新消息
         → 前缀永远是上次的超集 → 永远命中缓存

[区域三] Volatile Scratch（临时暂存区）
         思维链、中间状态
         不发送给 API，每轮开始时清空
         有用信息提取后以结构化形式追加进 Log
```

**压缩时的做法 — Cache Line Fold**：当上下文使用率超过 70%，把旧消息总结成摘要然后**追加**到前缀后面（不是替换）——前缀本身不动，缓存继续命中。

---

## 第五层：Forge 的做法 — Tiered Compact（主动删除历史）

Forge（本地 8B 模型 Agent 框架）的第五层防护是上下文压缩，三阶段依次执行：

1. 删除所有纠正消息；旧工具返回截断到前 200 字符
2. 删除旧工具返回结果（**保留推理过程**——推理是模型对数据的解读，比原始数据更关键）
3. 删除推理和失败回复，只保留工具调用骨架

按 ReasonX 标准，**这三步都是在破坏缓存**——历史消息被修改，之后前缀失效。

**但 Forge 的约束根本不是 API 成本，而是 VRAM**：

```
< 24GB GPU   → 上下文上限 4000 token
24–48GB GPU → 上下文上限 32000 token
> 48GB GPU  → 上下文上限 26 万 token
```

llama.cpp 在显存不足时会**静默回退到 CPU**，速度降 10–100 倍，用户毫无感知。本地推理根本没有 API prefix cache 的概念——模型没有离开本地机器。

---

## 客观判断：两套策略解决两个不同的问题


| 维度                   | ReasonX（DeepSeek API）         | Forge（本地 8B）         |
| -------------------- | ----------------------------- | -------------------- |
| **约束**               | API 成本                        | VRAM / 延迟            |
| **模型位置**             | 远端云 API                       | 本地 GPU               |
| **是否有 prefix cache** | 有（自动，按字节前缀）                   | 无（本地推理）              |
| **压缩策略**             | Append-only + Cache Line Fold | Tiered Compact（主动删除） |
| **缓存是否是目标**          | 是，44x 成本差                     | 无关，不存在这个概念           |


**Forge 不是"破坏了缓存"，而是缓存对它根本不适用。** 两套策略在各自的约束集下都是正确的。

---

## 业务应用框架（什么时候该认真对待 Prompt Caching）

```
用的是云端 API（Anthropic / DeepSeek / 阿里云通义）？
│
├── 是 → system prompt + 工具定义 > 500 token？
│         ├── 是 → 对话是否多轮？
│         │        ├── 是 → ✅ 缓存是成本杠杆，值得架构级设计
│         │        └── 否 → 收益有限（单轮无复用机会）
│         └── 否 → 前缀短，绝对节省额小，优先级低
│
└── 否（本地推理）→ Prompt Caching 无关，换 VRAM 管理策略
```

**跨模型兼容与深度缓存优化是冲突的**：Anthropic 要显式 cache_control；DeepSeek 是自动字节前缀匹配；OpenAI 粒度又不同。要针对一个 provider 做深度缓存优化，就不能用通用框架——这是 ReasonX 只支持 DeepSeek 的原因。

---

## Claude Code 怎么用 Prompt Caching

Claude Code 的完整 prompt 结构大概是：

```
[1] 系统 Prompt（角色定义 + 操作规范）         ← 最稳定，每次完全相同
[2] 工具定义（Read / Write / Edit / Bash /      ← 次稳定，同一 session 不变
    Agent / ... 几十个工具，每个带完整 schema）
[3] CLAUDE.md 内容 + 环境信息                  ← 同一目录内基本不变
[4] Memory 内容（MEMORY.md + 本次召回记忆）     ← 随项目变化
[5] 对话历史（前 N 轮）                        ← 增长
[6] 当前用户输入                               ← 每次不同
```

Cache 断点很可能打在 **[1][2] 之后**——工具定义是几十个带完整 schema 的对象，这块稳定、量大，是最理想的缓存对象。

**最直接的证据**：Claude Code 的 ScheduleWakeup 工具说明里明确写：

> "The Anthropic prompt cache has a 5-minute TTL. Sleeping past 300 seconds means the next wake-up reads your full conversation context uncached — slower and more expensive."

这说明 Claude Code 的工程团队在**产品决策层面**围绕 cache TTL 做了 loop interval 的 trade-off 建议——不是偶然的 API 参数使用，是架构约束。

---

## 连回自己项目（诚实的自我评估）

ZeroOps 系统用阿里云通义 API（qwen-plus-latest / qwen3-coder-plus），通义也有前缀缓存（按字节前缀自动匹配，与 DeepSeek 同范式）。


| 行为                                         | 缓存影响   | 说明                                     |
| ------------------------------------------ | ------ | -------------------------------------- |
| 5 个 agent 各有 1000-2000 token system prompt | 本可稳定命中 | 如果写死不含动态变量                             |
| Observation 压缩成结构化 JSON 写入 State           | 取决于做法  | 若通过改写 message history 实现，则破坏缓存         |
| 时间中心化（绝对时间戳注入 State）                       | ⚠️ 有风险 | 若时间戳注入到 system prompt 里，每次不同 → 必然 miss |
| LRU 缓存（工具结果层）                              | 无关     | 工具层缓存 ≠ prompt prefix 缓存，两个维度          |


**最大的潜在问题**：如果 system prompt 里有动态注入的内容（当前告警时间、版本号），每次请求前缀都不同，缓存永远 miss。这是 Reasonix 指出的"注入时间戳导致前缀失效"这个典型错误的变体。当时没有做缓存感知设计，是技术债。

---

## 口述路线图（面试时推荐顺序）

```
1. 机制层（10秒）："KV activations，不是文字缓存"
2. 数量级（10秒）："ReasonX 真实数据：44倍成本差"
3. 破坏点（20秒）：说出三种无意识破坏，第三条是重点
4. 反例（15秒）："Forge 是反例——本地模型、VRAM约束，
                   缓存对它不适用，两套策略解决两个不同的问题"
5. Claude Code（15秒）：工具定义是缓存主体，TTL影响了loop设计
6. 连回自己（15秒）：system prompt 稳定但未做缓存感知设计，技术债
```

---

## 常被深追的问题

**Q: DeepSeek 的自动前缀缓存 vs Anthropic 的显式 cache_control，哪个更好用？**

> DeepSeek 自动匹配门槛低但控制力弱（你不知道缓存到哪里）；Anthropic 显式控制精确但需要主动标记。高频稳定场景用 DeepSeek 模式更方便；需要精确控制多个断点位置用 Anthropic 模式更合适。

**Q: 你说 Forge 的压缩破坏了缓存——那如果 Forge 改用 Cache Line Fold 能行吗？**

> 不行。Cache Line Fold 是 Append-only 的，上下文会持续增长。Forge 的约束是 VRAM 物理上限，必须真正删减 token 数量，不是追加摘要——追加摘要只是把旧消息换成更短的表达，总 token 数仍在增加。两者目标函数不同：ReasonX 优化成本，Forge 优化内存占用。

**Q: 你自己项目的 system prompt 有没有动态注入变量？**

> 有，体检中心部分会把当前版本号和灰度比例注入 system prompt。这是一个明确的缓存失效来源。如果重做，会把动态元数据移到对话 message 里（让 system prompt 保持静态），只在 user 消息里注入当前上下文。

