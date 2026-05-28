# CAREER

把技术工作转成职业资产的层。**这是你日常的活跃工作区**，不是"等学完再填"的占位。

## 目录结构

```
CAREER/
├── cv.md                       简历（你拥有，LLM 只读）
├── target-roles/               目标岗位画像（每个岗位一个 .md）
├── applications/               真实投递流水（按明确请求由 LLM 辅助维护）
├── skill-gap.md                CV 现状 ↔ 目标岗位的缺口表（roadmap 的输入）
└── interview-bank/             面笔试题库
    ├── technical/              技术题（每题链 KNOWLEDGE 节点）
    └── behavioral/             行为题 + STAR 故事（链 PROJECTS）
```

## 各文件作用

### `cv.md`
你的简历单一来源。**只有你写**，LLM 不写不改。

### `target-roles/`
每个目标岗位一个 .md。包含：JD 关键词 / 典型面笔试题 / 技术栈 / 参考公司。
- 你可以亲自填，也可以和 LLM 对话讨论后让 log 走 triage 流程长出来。
- 至少要有：`summer-intern-agent-engineer.md` 和 `newgrad-agent-engineer.md`（暑期 + 秋招目标态）。

### `applications/`
真实投递流水。记录每一个具体岗位的状态、渠道、材料版本、沟通记录、面试准备和复盘。
- `RAW_SOURCES/jd-and-interviews/` 保存 JD / 面经原始素材。
- `target-roles/` 总结岗位类型画像。
- `applications/` 只记录你真实准备投 / 已投 / 面试中的岗位。
- 这个目录可由 LLM 在你明确请求时辅助创建和更新，但投递状态、联系人和结果以你确认的信息为准。

### `skill-gap.md`
CV 现状 vs 目标岗位的差异表。
- LLM 在 triage 末尾会**建议 diff**（如"今天入库了 mem0，建议把'长期记忆系统'从 gap 移到已有"）。
- 但**实际编辑你来做**。这是你的判断面板。

### `interview-bank/`
- **来源**：你自己丢面经/题到 INBOX，LLM triage 到这里。LLM **不**自己生成题。
- `technical/`：每题链回 `KNOWLEDGE/x/`。学懂的判定标准 = 这题能答出。
- `behavioral/`：每题链回 `PROJECTS/work/x/` 的 STAR 故事。

## 这层和其它层的关系

| 来源 | 流向 CAREER 哪里 |
|---|---|
| `KNOWLEDGE/` 节点完成 | 可能填补 `skill-gap.md` 中的 gap |
| `PROJECTS/work/<实习>/` 复盘 | 产出 `interview-bank/behavioral/` 的 STAR 故事 |
| `RAW_SOURCES/jd-and-interviews/` 的具体 JD | 进入 `applications/active/` 成为单次投递记录 |
| 实习中可复用 SOP | `WORK/playbooks/`（不在 CAREER） |

## 工作流

1. **现在就该做**：填 `target-roles/summer-intern-agent-engineer.md` 和 `newgrad-agent-engineer.md`（半个月后开始找暑期，9 月秋招）
2. 填 `skill-gap.md` 第一版（用现有 cv.md vs target-roles 做差异）
3. 平时学习时，LLM 会建议 skill-gap 更新
4. 找面经丢 INBOX，长出 interview-bank
5. 简历该更新时手动更新 cv.md
