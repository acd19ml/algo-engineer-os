# Q: 你的智能运维 Agent 上下文是怎么管理的？简历里的三痛点工程优化具体怎么做？

## 来源

- 出处：简历 bullet "针对多智能体 ReAct 模式的延迟高 / token 爆炸 / 循环不终止三个痛点做工程优化"
- 频率：高（Agent 系统工程深挖高频，考察"知道架构"还是"真做过"）

## 涉及节点

- 主：`PROJECTS/work/qiniu-zeroops-rca-agent/agent-subsystem.md` + `mock-system-design.md` §四 步骤7
- 相关 KNOWLEDGE：`KNOWLEDGE/agent/multi-agent-rca-paradigm/` / `KNOWLEDGE/agent/agent-failure-attribution/`

---

## 第一步：先建立层次（开场必说）

```
外层：LangGraph StateGraph（非 ReAct）
       节点 = agent，边 = 条件路由，State 类全局持久化
       ↓ 每个节点内部跑的是 ↓
内层：ReAct（Thought→Action→Observation 循环）
       三个痛点都发生在这一层
```

**开场一句话**：
> "我的系统外层是 LangGraph StateGraph 做编排，内层每个 agent 跑的是 ReAct 循环。延迟高 / token 爆炸 / 循环不终止这三个痛点都是内层 ReAct 的问题，四个工程优化分别对应不同的触发机制。"

---

## 痛点一：Token 爆炸 → 上下文压缩 + 精准引用

### 根源

ReAct 每一轮把完整对话历史放进上下文。第 8 轮时，前 7 轮的 Observation（大段 JSON 指标数据、日志原文）全在里面。Trace Agent 一次调用链查询返回 50+ span 的 JSON，保留原文到第 4 轮就已超 8k token。

### 具体做法

**每轮 Observation 结构化压缩后写回 State**

```python
# 不把原始 tool 输出直接存入 message history
# 而是压缩成结构化 summary 写进 State 的专用字段
state["metric_findings"] = {
    "finding_id": "M01",
    "service": "platform-service",
    "anomaly_type": "cpu_spike",
    "value": "87%",
    "time_window": "14:00-14:05",
    "confidence": "high"
}
```

**后续轮次引用 finding_id，不重复全文**

agent 在第 5 轮写 Thought：
> "根据 M01（平台服务 CPU 异常）+ T02（订单→平台 span 延迟高），可以判断..."

而不是把完整指标数据再贴一遍。

**效果**：token 消耗降低约 38%（10 个 case 总量统计）。

---

## 痛点二：循环不终止 → 智能终止判断（值班长 + 停止条件）

### 根源

单纯给 ReAct 加 `max_iterations=10` 是硬截断，不是智能终止。证据已充分时还在继续查（浪费 token）；证据不足时被截断（结果不完整）。

### 具体做法

引入 **值班长 agent（L3a）** 专门负责终止判断，刻意约束：**不调用任何数据工具，只对已有证据做推理**。

值班长 system prompt 里有明确的停止判据：

```
判断停止条件：
1. 根因服务已定位（精确到服务名）
2. 故障类型已明确（枚举：CPU超限 / 内存泄漏 / DB连接池耗尽 / ...）
3. 三个数据源（Metric / Log / Trace）至少两个已提交 ExplicitSummary

三条同时满足 → 输出停止指令，StateGraph 跳出循环
否则 → 输出"需要补充 [具体缺失信息]" → 路由回对应 data agent
```

这对应 Flow-of-Action 里的 JudgeAgent——把"终止逻辑"从 ReAct 内部剥离，交给专职角色判断。

---

## 痛点三（前半）：显式总结工具 → data agent 何时退出

### 根源

LangGraph StateGraph 怎么知道一个 data agent 的 ReAct 循环"跑完了"？没有显式信号时，agent 可能还在生成 Thought 但实际上已经得到答案——这个状态是未定义的。

### 具体做法

给每个 data agent 的 tool set 加 `ExplicitSummary` 工具：

```python
class ExplicitSummaryInput(BaseModel):
    findings: list[Finding]
    confidence: float      # 0-1
    sufficient: bool       # 证据是否足够支持根因推断

# agent 调用这个工具 = 明确宣告"我这轮任务完成"
# LangGraph 节点收到这个 tool call → 触发节点退出
```

**两个触发路径**：

| 路径 | 触发条件 | 作用 |
|---|---|---|
| 主动 | agent 判断证据充分，主动调用 ExplicitSummary | 正常完成 |
| 强制 | 连续两轮 Thought 语义相似度 > 0.92（在转圈）→ 系统强制注入 | 防止无意义循环 |

**内层 ReAct 的退出**和**外层 StateGraph 的节点跳转**通过工具调用干净解耦。

---

## 痛点三（后半）：减少无效循环

### 三个具体手段

**手段 1：时间中心化（最大单点收益）**

- **问题**：ReAct agent 自己心算时间窗口经常出错（"过去一小时"计算偏 5 分钟），工具返回空数据，agent 重试，再次空，循环。
- **做法**：StateGraph 入口节点统一把 `analysis_start` / `analysis_end` 绝对时间戳写入 State，所有 MCP 工具调用从 State 读取，不让 agent 自己算时间。
- **效果**：消灭"工具必然返回空"类硬错误（C3/C4 两个 case 直接通）。

**手段 2：LRU 缓存**

- 同一个 `(tool_name, params_hash)` 的查询结果缓存。Trace Agent 对同一服务查询两次时直接命中缓存，省掉一个 ReAct 轮次。

**手段 3：SOP 固化在 system prompt**

- 每个 data agent 的 system prompt 里有"严格按 5 步执行，一步不能跳"的固定排查流程（跟运维高工 mentor 共定的"拓扑定位→指标验证→日志取证→根因推断"）。防止 agent 漫无目的探索。

---

## 综合效果（数字必须记住）

| 指标 | 优化前 | 优化后 |
|---|---|---|
| 平均 ReAct 轮次（10 case 均值）| 8.3 轮 | 4.1 轮（−51%）|
| token 消耗 | baseline | 降低约 38% |
| P50 端到端延迟 | ~75s | ~28s |
| 根因定位成功率 | 20% | 70% |

---

## 口述路线图（面试时推荐顺序）

```
1. 先说两层架构（10秒，建立认知框架）
2. 说三个痛点对应的问题现象（"token爆炸具体表现是..."）
3. 逐一说四个优化，每个30-40秒：
   问题 → 具体做了什么 → 效果/数字
4. 最后收尾：
   "这四件事做完后平均 ReAct 轮次从 8.3 降到 4.1，
    token 降了 38%，P50 延迟从 75s 到 28s，
    这是简历里 ReAct 工程优化 bullet 对应的数字。"
```

---

## 常被深追的问题 & 答法

**Q: 语义相似度 0.92 这个阈值怎么定的？**
> 在 10 个 test case 上手动标注了"转圈"样本（连续两轮 Thought 语义相近但没有新 Action），经验阈值，不是严格调参结果。

**Q: 上下文压缩会不会丢失信息？**
> 会损失细节，但 RCA 任务需要的是结构化判据（哪个服务/什么类型），不是原始数据的全文检索。ExplicitSummary 里保存的 findings 字段已经包含足够的判断依据。值班长只看结构化 findings，不看原始 JSON。

**Q: 和 RAG 的上下文管理有什么区别？**
> RAG 是"查询时检索相关文档"；我做的是"每轮执行后结构化压缩并存入 State"。本质不同：RAG 压缩知识，我压缩的是同一个 task 执行过程中的中间状态。
