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
   视频/资料消化后写下来的内容 → INBOX/<topic>/internalized/
   其它东西丢到 INBOX 任意位置都行（参考材料 ppts/notes/ 不入 KNOWLEDGE）

2. 一段学习告一段落，开新 Claude session，说"整理 INBOX"
   LLM 读 META/llm/triage.md + REGISTRY 启动；按需加载其它 stage 规则；处理 INBOX

3. LLM 完成后输出 Triage Report
   ✅ 我建/改了哪些文件
   🔔 4 类待你执行的建议（勾 TRACKS / 改 skill-gap / 实习挖掘 nudge / 横向对比触发）
   ⚠️ 冲突 / 待确认
   📊 本次统计

4. 你审 Report
   重点检查：
   - 节点形态对（因果叙述 + 反事实，不是 bullet 摘要）
   - 节点稀疏（没"为完整性"补内容）
   - _self_check deck 题目质量（浅→深排序、链接对、没拍脑袋出题）
   - artifact 没引用 INBOX 路径
   你执行 Report 中的建议（勾 TRACKS、改 skill-gap、决定要不要建议建的页）

5. INBOX 中处理过的内容已被标记。你随时可以删 INBOX。下次回 1
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
| `CAREER/applications/` 的真实状态字段 | 投递状态、联系人、结果等事实以你确认为准 |
| `META/` | 所有规则、模板、policies（LLM 只读）|

### 🤖 LLM 写入区（从对话 log / 你 drop 的内容触发）

| 路径 | 触发条件 |
|---|---|
| `KNOWLEDGE/<domain>/<node>/` | 从 `INBOX/<topic>/dialogue_logs/` 或 `internalized/` 自动长出 |
| `KNOWLEDGE/_self_check/<domain>.md` | 节点新建/形态大改后同步更新（自检题独立于节点） |
| `PROBLEMS/*` | 当对话 log 出现"横向对比 N 方案" |
| `PROJECTS/*` | 当对话是项目复盘 / 实习挖掘 / 论文复现 |
| `RAW_SOURCES/*` | 当 INBOX 出现论文 / 完整文档 |
| `REPRO_INDEX/*` | 当 INBOX 出现外部 repo |
| `CAREER/interview-bank/*` | 你丢面经到 INBOX，LLM triage |
| `CAREER/applications/*` | 你明确请求整理投递工作时，LLM 可辅助创建 / 更新投递记录 |
| `WORK/playbooks/*` | 当对话明确说"这流程要沉淀成 SOP" |
| `PODCAST/*` | 你明确请求 "做成播客脚本" 或 "intro 一下未学的 X"（**不自动触发**）|
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
├── INBOX/              你随手丢学习痕迹（唯一入口，临时层 — 可删）
│   └── <topic>/
│       ├── dialogue_logs/    ← 入库源（你和 LLM 对话）
│       ├── internalized/     ← 入库源（你看视频/读资料后主动消化的内容）
│       ├── notes/, ppts/...  ← 参考材料，不入库
├── RAW_SOURCES/        原始资料（论文、文档）
├── KNOWLEDGE/          可复用知识节点（backbone，自含 artifact，不引用 INBOX）
│   ├── <domain>/<node>/      节点本体
│   └── _self_check/<domain>.md  自检题 deck（浅 → 深，跨节点链接）
├── PODCAST/            听觉形态层（review / intro 型脚本，跑步通勤听）
├── PROBLEMS/           问题对比框架页（横向方案对比触发）
├── PROJECTS/           有边界的执行单元
│   ├── research/       论文复现 / 技术探索
│   ├── work/           实习 / 全职项目
│   └── side-projects/  自发项目
├── WORK/               未来层：从 PROJECTS 提炼的 playbook / SOP
├── CAREER/             活跃工作区
│   ├── cv.md
│   ├── applications/          ← 真实投递流水（pipeline + 单岗位记录）
│   ├── target-roles/
│   ├── skill-gap.md
│   └── interview-bank/{technical,behavioral}/
├── REPRO_INDEX/        外部代码 / 实验 repo 索引
├── TRACKS/             多目标进度面板
│   ├── active/         有截止日期的临时任务
│   └── roadmap/        长期能力地图
└── META/               规则 / 模板 / 索引 / LLM 上下文
    ├── llm/triage.md         Stage-0 入口
    ├── llm/CONTEXT.md        Stage-1 ownership
    ├── llm/few_shots/        形态范例（node_form / podcast_script）
    └── policies/             node_form / self_check / podcast_script / ...
```

---

## 几条硬约束（决定这个系统不退化的关键）

1. **入库源限定**：`INBOX/<topic>/dialogue_logs/` 和 `internalized/` 是 KNOWLEDGE 入库的两类源。课件 / 笔记 / cheat sheet / tutorial 是参考材料，不入库
2. **节点是自含 artifact**：KNOWLEDGE 节点不引用 INBOX 路径——INBOX 是临时 scratch，你随时可删，节点必须独立存在
3. **节点形态：因果叙述 + 反事实推导**：不是 bullet 摘要。读者完全忘了能从节点重新学回来。详见 `META/policies/node_form.md`
4. **节点稀疏**：节点只写来源材料实际覆盖的部分。"论文里写但你没参与过" ≠ 你学过
5. **自检题独立于节点**：在 `KNOWLEDGE/_self_check/<domain>.md`，浅 → 深排序、链接到节点。日常自检用
6. **引用单向**：tracks/career → knowledge 单向。knowledge 不感知 tracks（保证稳定层不依赖不稳定层）
7. **用户编辑优先**：你手动改了 LLM 写的文件，LLM 下次读不覆盖

---

## 关键文件

### LLM 入口

| 文件 | 作用 |
|---|---|
| [META/llm/triage.md](./META/llm/triage.md) | Stage-0 入口：INBOX 处理流程 + 决策树 + 分阶段加载表 |
| [META/llm/CONTEXT.md](./META/llm/CONTEXT.md) | Stage-1 必读：ownership matrix、引用方向、节点是自含 artifact |
| [META/REGISTRY.md](./META/REGISTRY.md) | 全局索引 |

### 形态规则（写各类内容前必读）

| 文件 | 作用 |
|---|---|
| [META/policies/node_form.md](./META/policies/node_form.md) | KNOWLEDGE 节点形态（因果叙述 + 反事实） |
| [META/policies/self_check.md](./META/policies/self_check.md) | 自检题 deck 规则 |
| [META/policies/podcast_script.md](./META/policies/podcast_script.md) | 播客脚本规则（听觉形态） |
| [META/llm/few_shots/](./META/llm/few_shots/) | 形态范例（配合上面的抽象规则使用） |

### 其它

| 文件 | 作用 |
|---|---|
| [META/policies/source_of_truth.md](./META/policies/source_of_truth.md) | 真值冲突优先级 |
| [INBOX/README.md](./INBOX/README.md) | INBOX 子目录约定 |
| [CAREER/README.md](./CAREER/README.md) | CAREER 工作区使用方式 |

---

## 当前状态

系统结构已定型，节点形态已升级到因果叙述形态。

**已有**：
- 规则层完整（META/policies + few_shots + ownership matrix + 分阶段加载 triage）
- KNOWLEDGE：38 个节点，**全部已按新形态（因果叙述 + 反事实推导）写完**——9 个域（ml / nlp / optimization / pytorch / vision / methodology / transformer / agent / training），agent 域含 Cloud Code 源码级 6 大子系统拆解
- KNOWLEDGE/_self_check：9 个 domain 的自检题 deck 全部完整
- PODCAST：层框架就绪（spec + template + few-shot），按用户请求触发写脚本
- TRACKS：`active/sprint-2026-summer.md`（求职冲刺双轨道）+ `roadmap/agent-engineer.md`（待重写）
- CAREER：`cv.md` 已更新到投递就绪态（七牛云段已删 RocketMQ + 重写为 Dify L1/L2/L3 + MCP + MVP 措辞）+ target-roles 4 份已填 + skill-gap 第一版已成 + interview-bank（**已派生 3 条 STAR + 4 道技术深问**，全部基于 qiniu-zeroops-rca-agent）
- PROJECTS：`work/qiniu-zeroops-rca-agent/` 完整页（含时代背景锚点 / 主动选型路径 / 真实 SOP / 学术坐标对照 Flow-of-Action / 20%→70% 真实数字 / 7 条复盘）

**接下来该做的**：
1. 重写 `TRACKS/roadmap/agent-engineer.md`（target-roles 已填，可启动）
2. 开对话挖掘 Neo 一段实习，长出 `PROJECTS/work/neo-deepresearch-and-react-agent/` 和对应 STAR
3. 考虑建 `PROBLEMS/multi-agent-decomposition-axis/`（按职责拆 vs 按阶段拆 vs 按角色拆的横向对比）和 `PROBLEMS/multimodal-fusion-paradigms/`
4. 用 PODCAST 层把节点改写成跑步可听的脚本（用户主动请求触发）
