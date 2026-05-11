# 暑期实习 — Agent 工程师 / 算法工程师（汇总）

> **这是一份汇总指南**——4 个具体岗位画像见同目录其它文件。
>
> **本文件用途**：对所有 agent 方向暑期实习岗位的共同要求 + 投递策略 + 时间线。

## 主投 vs 保留

| 岗位文件 | 优先级 | 类型 |
|---|---|---|
| `a202665-ai-agents-algorithm-intern.md` | ★★★★★ 主投 | Coding Agent 全流程 |
| `business-agent-engineer.md` | ★★★★★ 主投 | 业务 Agent 应用 |
| `data-pretrain-engineer.md` | ★★ 保留 | 数据预训练 |
| `tencent-game-rl.md` | ★★ 保留 | 游戏 NPC RL |

## 共同高频考点（覆盖所有 agent 类岗位面试）

### 八股

- Transformer：QKV 三矩阵设计 / Multi-Head / Position Encoding / KV Cache / MLA
- 训练范式：PPO / DPO / GRPO 区别 / RLHF 整套流程 / KL 散度作用
- Reward Hacking + 奖励坍缩防范

### Agent 系统

- ReAct / Plan-Act / Tree-of-Thought / Function Calling
- Multi-Agent vs 单 Agent 决策（Anthropic 立场：默认单 agent）
- Context Engineering 6 层（Compaction / 外化记忆 / 即时加载 / 隔离 / 工具设计 / 缓存）
- Harness Engineering：Skill / Harness / OpenClaw / Hermes 对比
- 结构化输出 6 层（约束解码 → 验证重试 → 工具调用 → logit mask → 多 agent schema → 模式锁定）

### 工程

- RAG 流程 + 优化角度 + 评测指标
- 缓存策略（cache aside / read/write through / write behind）+ 一致性
- Redis 故障 / 主从切换处理
- AI 编程：LRU / 链表 / 字符串

### 系统设计

- 长对话 RL reward 设计
- 长对话上下文记忆保持
- 多轮对话微调
- agentic RL 设计思路

→ 全部题目派生到 `interview-bank/technical/`（Week 2 完成），每题链 KB 节点。

## 投递时间线

```
Week 1 (现在 - 一周内)
  Day 1-2: cv 重写完成
  Day 3-4: target-roles 4 份完成 + skill-gap 第一版
  Day 5-7: 投出第一波（A202665 + 业务 Agent 类，5-10 个）

Week 2
  - 横向对比报告做完 + 推到 GitHub
  - cv 加上 GitHub 链接二次投递

Week 3-8
  - 边做主项目边面试
  - 主项目里程碑（SFT MVP / GRPO / 评测） 达成时更新 cv 描述

最终目标:
  - 7 月初拿到 1-2 个暑期 offer
  - 8 月开始实习
```

## 简历版本管理

- `cv.md` — 当前主版本
- 不同岗位投递时可微调"项目经历"段落顺序：
  - **Coding Agent 类岗位**：主项目放最前
  - **业务 Agent 类岗位**：主项目 + 七牛云双 highlight，主项目突出全栈，七牛云突出业务理解
  - **数据 / RL 类岗位**：突出主项目的训练 + 评测部分

## 不该做的事（避雷自检）

参考 `INBOX/short-term-plan-for-career/post.md` 的 HR 抱怨清单：

- ❌ 简历写"调用 LangChain 搭 demo"就声称"设计了 Agent 架构"——我的简历不这样写
- ❌ "Fetch 几个 API 加个记忆模块"就声称"实现复杂决策系统"——主项目用具体数字（6-18% 影响窗口、98% 意图匹配、70% 成本降）替代套话
- ❌ "调包当创新"——我的项目是 fork 开源 + 加研究模块，描述里讲清楚了 base 是什么、自己加了什么
- ❌ 缺乏对 agent 痛点的独特思考——主项目的"selective transfer + boundary pattern"就是对"agent memory 不可控"的具体回答
