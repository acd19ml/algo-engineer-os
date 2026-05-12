# Q: 你做的多智能体根因分析处理日志 / 指标 / 调用链三种数据，为什么选 Result Fusion 而不是 Model Fusion 或 Feature Fusion？

## 来源

- 出处：基于 AgentOps 报告 §3（Result/Model/Feature Fusion 三范式对比）的项目深挖
- 频率：中（需要面试官在多模态方向有储备才会问，但问出来你能扎实回答会显得**学术坐标感非常强**）

## 涉及节点

- 主：`PROJECTS/work/qiniu-zeroops-rca-agent/`
- 相关 KNOWLEDGE 节点：`KNOWLEDGE/agent/multi-agent-rca-paradigm/`（"三件套之二：Result Fusion 多模态融合范式" 段）
- 学术参考：Result Fusion vs Model Fusion vs Feature Fusion 三范式对比已沉淀到上述节点
- 相关问题页：`PROBLEMS/multimodal-fusion-paradigms/`（建议建）

## 我的答案

### 三种范式的本质区别

| 范式 | 流程 | 上限 | 工业落地友好度 |
|---|---|---|---|
| **Result Fusion** | 每模态先单独分析转告警事件 → LLM 综合 | 中（受限于单模态分析工具） | 高 |
| **Model Fusion** | 多模态各自 embedding → 统一模型推理 | 高（端到端表征学习） | 低（需训练融合模型） |
| **Feature Fusion** | 多模态特征对齐到统一空间 → 推理 | 中-高 | 中（需精心设计特征对齐） |

### 我为什么选 Result Fusion（三个原因 + 学术背书）

1. **日志 / 指标 / 调用链各自有成熟工具**——SLS 查询日志、Prometheus 查指标、ARMS 看调用链——没必要重新做 embedding 把已有能力抛掉
2. **转结构化告警事件后 LLM 可直接读**——LLM 本身就擅长处理文本化的多源事件，让它做综合判断比让它处理原始多模态数据更高效
3. **Agent 天然适合多工具输出综合判断**——Multi-agent 范式 + Result Fusion 是天然契合的（一个 agent 一种数据源）

**学术背书（关键金句）**：

> 学术界 2025 年的报告里明确**主流方向偏向 Result Fusion**，理由跟我项目逻辑一致。**我做的多智能体设计不是 naive choice，而是当时学术界主流方向的工业实现**。（详细范式对比见 `KNOWLEDGE/agent/multi-agent-rca-paradigm/`）

### 不选 Model Fusion 的诚实理由

- Model Fusion 上限更高但需要**训练融合模型** + 收集大量标注数据 → MVP 阶段做不起
- AIOps 场景下日志 / 指标 / Trace 的数据规模、采样频率、稳定性都不一样，统一 embedding 很难做好
- **如果有人力 + 数据 + 上线指标真的卡在融合层，Model Fusion 是值得探索的方向**——但 MVP 不是

## 关键金句

> "**Result Fusion 是当时学术界主流方向（参考 AgentOps 报告 §3），同时工业落地最友好——每模态单独分析转告警事件，让 multi-agent 综合判断。我做的不是 naive choice，是当时合理方向的工业实现**。"

## 我答不出的部分（深问准备）

- **"Result Fusion 的上限是什么、什么场景下不够"** → 答：当**跨模态的细粒度时序对齐**对根因定位至关重要时（比如毫秒级日志 + 指标 + Trace 的精确同步），Result Fusion 会丢失这种细粒度信息。这种场景下 Model Fusion / Feature Fusion 上限更高
- **"你怎么知道你的 Result Fusion 在你的场景下够用"** → 答：根因定位成功率迭代中从 20% 到约 70%——但这是 Mock 系统数据，未上线生产验证（**面试时必须坦诚这点**）
- **"这个'学术主流偏向 Result Fusion'你是项目做的时候就知道还是事后知道"** → 答：**事后知道**。项目时段做选型主要基于工程友好性，**后来读到 2025 CCF ChinaSoft 那份 AgentOps 报告才意识到我的选型有学术坐标对应**。这是诚实回答，比假装"我项目时段就读过这个报告"强
