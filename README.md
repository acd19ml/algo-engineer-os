# Algo Engineer OS

算法工程师个人知识操作系统。

---

## 核心理念

**学习的痕迹 = 你和 LLM 的对话过程**，不是 LLM 给你写的整理成品。

LLM 替你写完不等于你学了。所以这个系统设计成：你和 LLM 对话学习时把对话 log 丢进 `INBOX/`，LLM 从这些 log 里提炼可复用知识 + 自检题。**自检题来自你卡住、问错、被纠正的位置**——这些才证明你真的参与了思考。

KB 的真实作用：抗遗忘工具。日常做自检（看题想原理），完全忘了能用 KB 重新学一遍。

---

## 你怎么用这个 repo（5 步循环）

```
1. 学习时和 LLM 对话
   把对话 log 保存到 INBOX/<topic>/dialogue_logs/
   （或丢任何东西到 INBOX 任意位置——零结构要求）

2. 一段学习告一段落，开新 Claude session，说"整理 INBOX"
   LLM 自动读 META/llm/ + REGISTRY + INBOX，按 triage.md 处理

3. LLM 完成后输出 Triage Report
   ✅ 我建/改了哪些文件
   🔔 4 类待你执行的建议（勾 TRACKS / 改 skill-gap / 实习挖掘 nudge / 横向对比触发）
   ⚠️ 冲突 / 待确认
   📊 本次统计

4. 你审 Report
   重点检查：节点是否稀疏（没"为完整性"补内容）、自检题是否真触及你卡过的点
   你执行 Report 中的建议（勾 TRACKS、改 skill-gap、决定要不要建议建的页）

5. INBOX 中处理过的对话 log 已被标记。下次回 1
```

---

## Ownership Matrix（权威定义）

谁拥有什么。**不在矩阵里的灰色地带：默认 LLM 不写**。

### 🧑 你的纯私有 surface（LLM 只读，绝不写）

| 路径 | 说明 |
|---|---|
| `INBOX/` 下所有内容 | 你丢，你删 |
| `TRACKS/active/*` | 临时任务（结构 + 勾选都你来） |
| `TRACKS/roadmap/*` | 长期能力地图（结构 + 勾选都你来） |
| `CAREER/cv.md` | 简历 |
| `CAREER/skill-gap.md` | 缺口表（LLM 建议 diff，你执行） |
| `CAREER/target-roles/*.md` | 目标岗位画像（你填或对话长出但你审） |
| `META/` | 所有规则、模板、policies（LLM 只读）|

### 🤖 LLM 写入区（从对话 log / 你 drop 的内容触发）

| 路径 | 触发条件 |
|---|---|
| `KNOWLEDGE/*` | 从 `INBOX/.../dialogue_logs/*.md` 自动长出 |
| `PROBLEMS/*` | 当对话 log 出现"横向对比 N 方案" |
| `PROJECTS/*` | 当对话是项目复盘 / 实习挖掘 / 论文复现 |
| `RAW_SOURCES/*` | 当 INBOX 出现论文 / 完整文档 |
| `REPRO_INDEX/*` | 当 INBOX 出现外部 repo |
| `CAREER/interview-bank/*` | 你丢面经到 INBOX，LLM triage |
| `WORK/playbooks/*` | 当对话明确说"这流程要沉淀成 SOP" |
| `META/REGISTRY.md` | 每次 triage 后同步 |

### 🔔 LLM 只建议、你执行（写进 Triage Report，不直接动文件）

- TRACKS 里"建议勾掉"的 checkbox
- `CAREER/skill-gap.md` 的 diff 建议
- 实习挖掘 nudge（"PROJECTS/work/qiniu-... 还没建，开对话挖一下？"）
- 横向对比触发（"建议建 PROBLEMS/long-context-degradation/"）

### 用户编辑 = ground truth

如果你手动改了 LLM 写的文件，下次 LLM 读时把它当事实，不覆盖。冲突时 LLM 在 Report 里暴露，让你决定。

---

## 仓库结构

```
algo-engineer-os/
├── INBOX/              你随手丢学习痕迹（唯一入口）
│   └── <topic>/
│       ├── dialogue_logs/    ← 入库主源
│       ├── notes/, ppts/...  ← 参考材料，不入库
├── RAW_SOURCES/        原始资料（论文、文档）
├── KNOWLEDGE/          可复用知识节点（backbone）
├── PROBLEMS/           问题对比框架页（横向方案对比触发）
├── PROJECTS/           有边界的执行单元
│   ├── research/       论文复现 / 技术探索
│   ├── work/           实习 / 全职项目
│   └── side-projects/  自发项目
├── WORK/               未来层：从 PROJECTS 提炼的 playbook / SOP
├── CAREER/             活跃工作区
│   ├── cv.md
│   ├── target-roles/
│   ├── skill-gap.md
│   └── interview-bank/{technical,behavioral}/
├── REPRO_INDEX/        外部代码 / 实验 repo 索引
├── TRACKS/             多目标进度面板
│   ├── active/         有截止日期的临时任务
│   └── roadmap/        长期能力地图
└── META/               规则 / 模板 / 索引 / LLM 上下文
```

---

## 几条硬约束（决定这个系统不退化的关键）

1. **入库源唯一**：`INBOX/<topic>/dialogue_logs/*.md` 是唯一的 KNOWLEDGE 入库源。课件 / 笔记 / cheat sheet 是参考材料，不入库
2. **节点稀疏**：节点只写对话 log 实际覆盖的部分。"论文里写但你没在对话里推导过" ≠ 你学过
3. **自检题来源限定**：必须来自对话 log 中你卡住 / 被纠正 / 被要求复述的位置。LLM 不许拍脑袋出题
4. **引用单向**：tracks → knowledge 单向。knowledge 不感知 tracks（保证稳定层不依赖不稳定层）
5. **用户编辑优先**：你手动改了 LLM 写的文件，LLM 下次读不覆盖

---

## 关键文件

| 文件 | 作用 |
|---|---|
| [META/llm/CONTEXT.md](./META/llm/CONTEXT.md) | LLM 的完整操作约束（含 ownership matrix） |
| [META/llm/triage.md](./META/llm/triage.md) | INBOX 处理流程 + Triage Report 模板 |
| [META/REGISTRY.md](./META/REGISTRY.md) | 全局索引 |
| [META/policies/source_of_truth.md](./META/policies/source_of_truth.md) | 真值冲突优先级 |
| [INBOX/README.md](./INBOX/README.md) | INBOX 子目录约定 |
| [CAREER/README.md](./CAREER/README.md) | CAREER 工作区使用方式 |

---

## 当前状态

系统结构已定型，内容待你的真实学习痕迹长出来。

**已有**：
- 规则层完整（META + Ownership Matrix）
- TRACKS：`active/final-exam-prep.md` + `roadmap/agent-engineer.md`（待重写）
- CAREER：`cv.md` 已有（过时，需更新）+ skeleton（target-roles / skill-gap / interview-bank）

**接下来该做的**（不用 LLM 替你做）：
1. 4.27 / 4.29 / 5.2 三场 final 期间，把和 LLM 的对话 log 存进 `INBOX/<课程>/dialogue_logs/`
2. 三场考完，喊 LLM 整理 INBOX
3. 填 `CAREER/target-roles/summer-intern-agent-engineer.md` 和 `newgrad-agent-engineer.md`（半个月内开始投暑期）
4. 给方向后让 LLM 重写 `TRACKS/roadmap/agent-engineer.md`
5. 开对话挖掘七牛云 / Neo 两段实习，长出 `PROJECTS/work/*` 和 `CAREER/interview-bank/behavioral/*`
