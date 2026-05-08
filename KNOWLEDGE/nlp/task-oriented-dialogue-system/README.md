# Task-Oriented Dialogue System

## 它要解决什么问题

要回答 "怎么用对话完成一个具体任务"——比如让用户通过聊天报告 COVID-19 检测结果（CRB: COVID-19 Reporting roBot）。

这类系统和 ChatGPT 那种闲聊机器人**根本不同**——前者必须**填完特定 slot 后真正提交一个事务**，后者可以随便聊；前者有明确任务边界，后者没有。

| Task-oriented | Open-domain |
|---|---|
| 完成具体任务（订餐、报检测结果） | 闲聊、陪伴 |
| 有明确的 slot 要填 | 没有固定结构 |
| CRB / 订机票 bot 属于这种 | ChatGPT 闲聊属于这种 |

要构建 task-oriented dialogue system，**必须形成 closed loop（闭环）**——用户说话 → 系统理解 → 系统决策 → 系统回复 → 用户继续，直到任务完成。

## 朴素直觉为什么不够：只做"理解"是不够的

很多人对对话系统的第一反应是"用大模型理解用户说的话就好"。这只能完成**第一步**。

要完成任务，至少需要四个互相协作的模块：

```
用户输入
   ↓
1. NLU                 ← "用户想要做什么 + 提供了什么信息"
   ↓ (intent + slots)
2. DST                 ← "对话目前到哪一步了 + 还缺什么"
   ↓ (current state)
3. DPL                 ← "下一步系统该做什么"
   ↓ (system action)
4. NLG                 ← "把决策转成自然语言回复"
   ↓
系统回复 → 用户继续输入(回到顶部,形成闭环)
```

少哪个都不行：

- 没有 NLU → 系统看不懂用户说什么
- 没有 DST → 系统不记得已经填了什么、还差什么
- 没有 DPL → 系统不知道下一步该问什么
- 没有 NLG → 系统的决策只是结构化数据，用户看不懂

## NLU 的三个子任务

NLU（Natural Language Understanding）本身就是**三件不同的事**：

### Domain Classification（领域分类）

判断用户说的话**属于哪个业务领域**。

- 输入：`"I want to report my test result"`
- 输出：`domain = COVID-19 reporting`（不是 weather 或 booking）
- 本质：**多分类**，类别是预定义的领域集合

### Intent Detection（意图识别）

确定 domain 后，**判断用户具体想做什么**。

- 输入：`"I tested positive yesterday"`
- 输出：`intent = report_test_result`（不是 cancel_report 或 query_history）
- 本质：**多分类**，类别是预定义的意图集合

### Slot Filling（槽位填充）

从用户的话里**抽取关键信息填进预定义的槽位**。

- 输入：`"I am John Smith, my HKID is A123456, I tested positive on Nov 25 using PCR"`
- 输出：
  - `name = John Smith`
  - `HKID = A123456`
  - `test_result = positive`
  - `test_date = Nov 25`
  - `test_type = PCR`
- 本质：**序列标注**（token-level 标 BIO 标签）或 **span extraction**

> CRB 的合理 slot：`name` / `HKID` / `test_date` / `test_result` / `test_type`——选最核心的 5 个就够。

## 反事实：为什么 NLU 不够，还需要 DST + DPL

NLU 只回答 "**这一句话用户说了什么**"——但对话是**多轮**的。

举个具体场景：

```
Turn 1
用户: "I want to report my test result"
NLU: intent = report_test_result, slots = {}    ← 一个都没填

Turn 2
用户: "I'm John Smith"
NLU: intent = inform, slots = {name: John Smith}    ← 只填了 name
```

仅靠 NLU 系统**不会知道**：

- Turn 2 时已经填过 `intent = report_test_result`（来自 Turn 1）
- 还缺 HKID、test_date、test_result、test_type 四个 slot

要把整个对话状态串起来，需要 **DST（Dialogue State Tracking）**——它**跨多轮**维护：

```
Turn 1 后: {filled: {}, missing: [name, HKID, test_date, test_result, test_type]}
Turn 2 后: {filled: {name: John Smith}, missing: [HKID, test_date, test_result, test_type]}
...
Turn N 后: {filled: {全部}, missing: []}
```

DST 维护了**当前对话状态**——但它不决定"下一步系统该做什么"。这是 **DPL（Dialogue Policy Learning）** 的职责：

```
state = {filled: {name}, missing: [HKID, ...]}
DPL → action = ask(HKID)
```

DPL 根据当前状态选择下一个 system action：问缺失 slot、确认已填信息、还是提交任务。

最后是 **NLG（Natural Language Generation）**——把结构化的 system action 变成人类可读的回复：

```
action = ask(HKID)
NLG → "Thanks, John. Could you please provide your HKID?"
```

## 用 CRB 串完整闭环

```
Turn 1
User: "I want to report my test result"
NLU:  domain=COVID, intent=report_test_result, slots={}
DST:  {filled: {}, missing: [name, HKID, test_date, test_result, test_type]}
DPL:  ask(name)
NLG:  "Sure, may I have your name first?"

Turn 2
User: "I'm John Smith"
NLU:  intent=inform, slots={name: John Smith}
DST:  {filled: {name}, missing: [HKID, test_date, test_result, test_type]}
DPL:  ask(HKID)
NLG:  "Thanks, John. Could you please provide your HKID?"

... (继续直到所有 slot 填满) ...

Turn N
DST:  {filled: 全部, missing: []}
DPL:  confirm_and_submit
NLG:  "I have all your info. Let me confirm: ... Submit?"
User: "Yes"
NLG:  "Your report has been submitted. Reference: ABC123."
```

**这就是 closed loop**——四个模块缺一不可。

## 评价指标：必须分两个层级

容易踩的坑：评价对话系统的指标**不是只有一种**。要分两个层级：

### Component-level（模块级）

评价**单个模块**好不好：

- **Slot Filling F1**：NLU 抽 slot 抽得准不准（precision 和 recall 的调和平均）
- **Intent Classification Accuracy**：意图识别对不对
- **Domain Classification Accuracy**：领域分类对不对

### End-to-end / Task-level（整体任务）

评价**整个对话系统**最终表现：

- **Task Completion Rate**：用户的任务成功完成的比例（100 个用户，90 个成功提交 → 90%）
- **Average Turns to Completion**：平均要几轮才能完成（越少越好）
- **User Satisfaction**：用户主观打分

**只看一个层级会出错**：

- 只看 component-level：每个模块都不错，但拼起来用户卡住了
- 只看 end-to-end：整体差，但不知道是哪个模块的问题

最稳的组合是 **1 个 component-level + 1 个 end-to-end**——比如 Slot Filling F1 + Task Completion Rate。

## Open Questions

- DPL 的训练方法：**rule-based（写规则）vs RL（reinforcement learning）vs supervised（用对话标注训练）**——三种方法各自的适用场景没有展开。RL 在工业界对话系统中的应用情况似乎比想象中少，原因是什么？
- 现在 LLM-based 对话系统（如 ChatGPT 做 task-oriented）逐渐**模糊了 NLU/DST/DPL/NLG 的边界**——所有模块都在一个 prompt 里完成。这种端到端方案 vs 模块化方案在 task completion rate / 错误归因 / 调试性上的 trade-off 是什么？这条线和 agents 主题相关，待单独节点。
- **slot 设计的最小充分性**：5 个 slot 够不够？少一个会怎样、多一个会怎样？这是一个产品 / 系统设计题，需要看具体业务，不是技术题。
