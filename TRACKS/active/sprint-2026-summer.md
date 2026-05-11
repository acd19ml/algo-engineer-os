# Sprint 2026 Summer — Agent Engineer 求职冲刺

> 起止：2026-05-09 → 2026-08-初
>
> 目标：拿到 1-2 个暑期实习 offer（agent 算法 / 应用方向）
>
> 双轨道并行：**轨道 A（一周内开始投简历）+ 轨道 B（暑期主项目）**

---

## 总览

```
轨道 A：投递 + 横向对比      Week 1-2 高强度，2-8 持续投递面试
轨道 B：全栈主项目            Week 1 启动数据集调研，Week 3-8 重点
```

---

## 轨道 A — 简历投递 + 横向对比 + 面试准备

### Week 1（2026-05-09 → 2026-05-15）

| Day | 任务 | 产出物 |
|---|---|---|
| Day 1-2 | cv.md 重写 | ✅ 已完成 |
| Day 1-2 | target-roles 4 份 | ✅ 已完成 |
| Day 1-2 | skill-gap.md 第一版 | ✅ 已完成 |
| Day 3-4 | 横向对比四个 repo 第一遍速读（先看架构 + README） | KB `KNOWLEDGE/agent/` 加 4 个对比节点 stub |
| Day 3-4 | 派生 `interview-bank/technical/` 从 shared-interview.md | 8-15 道高频题，每题链 KB |
| Day 5 | 派生 `interview-bank/behavioral/` 的 STAR 故事 3 条（七牛云架构决策 / Neo 语义路由设计 / Neo 海外社区协作） | 3 个 STAR 文件 |
| Day 5-7 | **第一波投递**：A202665 + 业务 Agent 类各 5-8 家 | 投递记录 |

**Week 1 结束验收**：
- [ ] cv.md 投递就绪
- [ ] 4 份 target-roles + skill-gap 完整
- [ ] 横向对比已经看过 4 个 repo 的 README + 顶层架构（不要求看完所有源码）
- [ ] 至少投出 10 家
- [ ] 至少 3 个 STAR 故事写完

### Week 2（2026-05-16 → 2026-05-22）

| 任务 | 产出物 |
|---|---|
| 横向对比四个 repo 深读（重点：记忆机制 + 工具调用） | KB 4 个对比节点写完 + GitHub 公开仓库 markdown 报告 |
| **横向对比报告 push 到 GitHub** | 公开 repo + README |
| cv.md 加 GitHub 链接 + 二次投递 | 投递记录 |
| 模拟面试自检：用 KB self-check decks 过一遍 | 找出还卡壳的题 |
| 卡壳题 → 反向更新 KB 节点 / 派生新 KB 节点 | KB 增量 |

**Week 2 结束验收**：
- [ ] 横向对比报告完整 push 到 GitHub（4 项目 × 5 维度）
- [ ] cv 二次更新（含 GitHub 链接）
- [ ] 累计投递 15-25 家
- [ ] 收到 1-3 个面试邀请

### Week 3-8

- **持续投递 + 面试**——每周至少投 5 家
- **每次面试后做复盘**：放进 `interview-bank/` + 反向更新 KB
- **轨道 B 进度**：每周更新 cv.md 的 "(进行中) coding agent + memory" 段落最新状态

---

## 轨道 B — 全栈主项目（Coding Agent + Procedural Memory）

### 项目定位

```
基于开源 Claude Code 实现（claw-code）扩展 procedural memory 模块
在 SWE-bench-Lite 上设计 matched/mismatched issue 配对评测
全链路：业务定义 → 多 agent 架构 → 数据生产 → SFT → GRPO → 评测 → 部署
```

**方法学来源**：基于 2026 春自主研究的延伸——前期已复现并审计某主流 web agent memory 框架（step-level 分析定位 6-18% 影响窗口 + 归类 8 类失败模式），并在多跳 QA 任务上设计 matched/mismatched 配对实验（验证 memory 抽象的可执行性如何决定迁移边界）。本项目把这些方法学落到 coding agent 全栈工程上。

### 资源约束

- **算力预算**：GpuHub $100（首批），可追加
- **模型规模**：Qwen 2.5-3B 快速 iterate → Qwen 2.5-7B 最终版
- **数据集**：SWE-bench-Lite（标准 + 现成）

### 周计划

| Week | 主任务 | 里程碑 |
|---|---|---|
| **Week 1** | 数据集调研（SWE-bench-Lite 格式 + claw-code 仓库结构） | 知道在 claw-code 哪里挂 memory 模块 |
| **Week 2** | 架构设计（Memory Pool + 检索策略 + 更新策略） | 架构文档（学七牛云 6 步法） |
| **Week 3** | 数据生产：从 SWE-bench-Lite 提取 trajectory + 蒸馏 procedural memory | trajectory 数据集 + memory pool v1 |
| **Week 4** | SFT MVP：Qwen 2.5-3B + LoRA → 验证 pipeline | 第一个能跑的版本（即使效果差）|
| **Week 5** | SFT 升级：Qwen 2.5-7B + 调参 + 第一次 selective transfer 评测 | matched 集 vs mismatched 集对比数字 |
| **Week 6** | GRPO 简版：故障域分类策略 / 记忆调用决策策略 | GRPO 训练 pipeline |
| **Week 7** | 评测体系：matched/mismatched + 8 类 boundary pattern 检测 | 完整评测报告 |
| **Week 8** | 部署：vLLM + Docker + Web UI / CLI；文档 + 简历更新 | 可演示版本；cv "进行中" 改为完成 |

### 算力分配（$100 + 预备追加）

| 阶段 | 算力 | 预算 |
|---|---|---|
| Week 4 SFT MVP | ~30h Qwen 2.5-3B → 7B 试 | $30-40 |
| Week 5 SFT 升级 | ~30h | $30-40 |
| Week 6-7 GRPO | ~30-40h | $30-50（可能要追加） |
| **MVP 阶段 ($100)** | Week 4-5 | ~$60-80 |
| **完整阶段（追加 $50-100）** | Week 6-8 | ~$60-100 |

### 关键开放问题（边做边解）

- **claw-code 哪里加 memory 最自然？** — 等 Week 1 横向对比看完源码后定
- **SWE-bench-Lite 的 issue 怎么"配对"成 matched/mismatched？** — Week 2 架构设计时定
- **memory 蒸馏的 oracle 用 GPT-4 还是 Claude？** — Week 3 数据生产时定（看预算）

---

## 跨轨道联动

| 联动点 | 怎么用 |
|---|---|
| 横向对比 → 主项目 | 看完 claw-code 源码后才决定主项目挂载点 |
| 主项目数据 → 简历更新 | 每个里程碑达成更新 cv "进行中" 描述的具体数字 |
| 面试遇到的问题 → KB | 面试卡住的题反向写进 KB，下次不卡 |
| 主项目踩坑 → 简历亮点 | 踩到的坑 + 解决方案就是面试时的 STAR 故事素材 |

---

## 风险预案

| 风险 | 应对 |
|---|---|
| 第一波投递无回响 | Week 2 横向对比报告补到 GitHub，简历加更直接的"研究深度"信号 |
| 主项目某个环节卡住超过 1 周 | 简化目标（Qwen 2.5-7B 改 3B / GRPO 简化为 PPO / 评测集只做 matched 不做 mismatched 的 ablation） |
| GpuHub 预算超支 | 优先 SFT，GRPO 简化为只跑一轮 |
| 拿到 offer 时间窗口紧 | 主项目 Week 7 的状态作为最终展示版本，Week 8 收尾在入职后做 |

---

## 成功标准

**短期（4 周末）**：
- [ ] 拿到至少 3 个面试机会
- [ ] 横向对比报告 GitHub 上线

**中期（6 周末）**：
- [ ] 主项目 SFT MVP 跑通 + 第一次 selective transfer 评测有数字
- [ ] 至少进到 2 家公司的二面 / 三面

**最终（8 周末 / 7 月初）**：
- [ ] 拿到 1-2 个暑期 offer
- [ ] 主项目可演示版本上线
- [ ] cv 全部更新到完成态
