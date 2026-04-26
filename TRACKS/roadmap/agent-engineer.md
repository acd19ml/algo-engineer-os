# Agent 算法工程师成长路线

> ⚠️ **本文件待重写**：当前内容是基于"虚构新手"的层级模板，与你 CV（七牛云 supervisor agent + Neo deepresearch / 区块链 agent）的实际起点不匹配。
>
> 重写触发条件：你提供 `CAREER/target-roles/summer-intern-agent-engineer.md` 和 `newgrad-agent-engineer.md` 的目标方向后。新版本应包含：当前 focus（≤3 项）/ 暑期目标态 / 秋招目标态 / gap → 对应 KNOWLEDGE 节点 / 已掌握（链 cv.md bullet）。
>
> 在重写前，下方内容仅供参考，不要按它推进学习。

## 当前阶段 Focus

（根据实际进展更新这里，指向当前最该优先补的 2-3 项）

- [ ] TBD — 等 final 结束后、target-roles 填完后启动重写

---

## 第 0 层：底层肌肉

> 没有这层，后面所有东西都是空中楼阁。

### Transformer 内部机制

- [ ] 手推 QKV 计算过程
- [ ] 讲清 KV cache 为什么存在
- [ ] prefill vs decode 的差异
- [ ] 长 context 为什么贵
- [ ] MoE 路由机制
- [ ] 读 nanoGPT 源��
- [ ] 读 Flash Attention 论文
- [ ] 自己实现玩具版 KV cache

### 训练三阶段

- [ ] pretrain：解决什么问题、数据长什么样、失败模式
- [ ] SFT：解决什么问题、数据长什么样、失败模式
- [ ] Preference optimization（RLHF/DPO/GRPO）：同上
- [ ] RLVR：同上
- [ ] 能画出完整的四阶段流程图并讲清每步的 why

### 推理时动力学

- [ ] temperature / top-p / logit bias 的实际效果
- [ ] speculative decoding 原理
- [ ] beam search 为什么 agent 用得少
- [ ] constrained decoding 的代价
- [ ] ���些参数如何影响 agent 的 latency 和 cost

---

## 第 1 层：Agent 理论地基

### 经典范式源流

> 重点：每一代在解决上一代的什么失败

- [ ] ReAct
- [ ] Reflexion
- [ ] Toolformer
- [ ] Voyager
- [ ] AWM
- [ ] SWE-agent
- [ ] OpenAI o1 / DeepSeek R1 的 agent 视角

### Planning 流派

- [ ] Decomposition（HTN 式）
- [ ] ReAct 式交替
- [ ] Tree search（ToT / LATS）
- [ ] MCTS in agent（r-Star, rStar-Math）
- [ ] World model 式规划
- [ ] 知道什么任务用什么 planning

### Memory 架构

- [ ] Working memory（context window 内）
- [ ] Episodic（trace 级）
- [ ] Semantic（抽象知识）
- [ ] Procedural（skill/workflow，AWM 属这类）
- [ ] 能画出完整 agent 的 memory 数据流

### Tool Use 工程

- [ ] Function calling 协议
- [ ] MCP
- [ ] Tool 选择（retrieval over tools）
- [ ] Tool error handling
- [ ] Tool output 的 truncation 策略

---

## 第 2 层：GUI Agent 专项

> North star 方向。

### 感知侧

- [ ] Screen parsing（OCR + icon detection + layout 理解）
- [ ] SoM（Set of Mark）标注
- [ ] 坐标回归 vs region 选择的权衡
- [ ] 高分辨率视觉编码（AnyRes、cropping 策略）
- [ ] Visual grounding 的 failure modes

### 动作空间设计

- [ ] Pixel-level vs element-level vs API-level 的 trade-off
- [ ] Mobile-Agent 系列为什么在收敛到某种设计

### Benchmark 与数据

- [ ] AndroidWorld
- [ ] OSWorld
- [ ] WebArena / VisualWebArena
- [ ] Mind2Web
- [ ] AITW
- [ ] 能评判一个新 benchmark 好不好

### 关键系统

- [ ] UI-TARS
- [ ] OS-Atlas
- [ ] ShowUI
- [ ] Aguvis
- [ ] GUI-Owl
- [ ] Mobile-Agent v1/v2/v3
- [ ] Claude Computer Use
- [ ] OpenAI Operator
- [ ] 能讲清架构差异

---

## 第 3 层：后训练与数据飞轮

> "无护城河公司"产生价值的核心能力。

### 数据合成

- [ ] Reject sampling
- [ ] Self-instruct / Evol-instruct
- [ ] Distillation from frontier
- [ ] Agent trace → SFT data 的清洗 pipeline

### SFT 实操

- [ ] Format learning vs capability learning
- [ ] Data mixing ratio
- [ ] Catastrophic forgetting 的实战规避
- [ ] LoRA vs full FT 的决策边界

### Preference Learning

- [ ] DPO / IPO / KTO / SimPO 的差异与适用场景
- [ ] 什么时候需要 PPO/GRPO 而不是 DPO

### RLVR 与 Agent RL

- [ ] Reward 设计（process reward vs outcome reward）
- [ ] Credit assignment 在长 trace 里的问题
- [ ] REINFORCE/GRPO 在 agent 上的应用
- [ ] RL 环境的 throughput 工程

### Distillation

- [ ] On-policy vs off-policy distillation
- [ ] Reasoning trace distillation（R1-style）

---

## 第 4 层：Eval

> 最容易低估，但决定所有工作的可信度。

- [ ] 构造 eval 的能力（比跑 eval 重要 10 倍）
- [ ] Task 采样的偏差
- [ ] LLM-as-judge 的陷阱与校准
- [ ] Pairwise vs pointwise
- [ ] Eval 的可复现性工程（seed、温度、版本锁定）
- [ ] Overfitting to eval 的识别
- [ ] Agent 特有：long trace 的部分分
- [ ] Agent 特有：exploration 成功但 execution 失败怎么算
- [ ] Agent 特有：真实环境 eval 的不稳定性
- [ ] Agent 特有：online vs offline eval 的 gap
- [ ] 自己搭一个真能跑的 agent eval harness

---

## 第 5 层：系统与工程

### 推理服务

- [ ] vLLM / SGLang 原理
- [ ] PagedAttention
- [ ] Continuous batching
- [ ] 为什么 agent workload 对 prefix caching 极度敏感

### Orchestration

- [ ] LangGraph / DSPy
- [ ] 自己撸一个 agent framework（至少一次）
- [ ] Go 背景优势：高并发 agent 调度 = 分布式系统问题

### Observability

- [ ] Trace 收集、replay、debug 工具链
- [ ] LangSmith / Arize / 自建

### Cost/Latency Engineering

- [ ] Prompt caching
- [ ] Model cascading（小模型先跑，大模型兜底）
- [ ] Speculative agent execution

---

## 第 6 层：品味与判断

> 最难教，最值钱。靠大量 failed experiments 积累。

- [ ] 对模型能力曲线的预判：哪个 hack 不值得做
- [ ] 哪些任务适合 agent 化，哪些一次性 prompt 就够
- [ ] 学术 demo vs 生产环境的区分
- [ ] 看 trace 能分辨"pretrain 缺失" vs "prompt 没写好" vs "工具设计有问题"

---

## 核心判断框架

> 任一 agent 能力 X，问三件事：

1. X 能否仅靠"更多同类数据 + 更长训练"压进权重？ → 能，就会被替代
2. X 是否依赖上下文外的状态或环境？ → 依赖，就不会被替代
3. 模型能力增强会不会让 X 所在的更高层问题变得可行？ → 会，就是新疆域

---

## 反直觉提醒

- 不要读太多论文，读完要逼自己复现或写 critique
- 早期就开始和真实用户 trace 打交道，纯 benchmark 练出来的直觉是废的
- 最高 ROI 的项目：自己做一次完整的 agent 数据飞轮闭环（frontier 跑 trace → 筛选 → SFT 小模型 → eval → 迭代）
