# 讲义 01 - 人工智能导论

**课程**: CS5491: Artificial Intelligence  
**授课教师**: Jianyuan Guo, Zhichao Lu  
**内容致谢**: Prof. Wei 的 CS4486 课程 & Prof. Boddeti 的 AI 课程

---

## 1. 人工智能能做什么？

### 1.1 当前 AI 感知能力
- **Object & Face Recognition（物体与人脸识别）**
- **Scene Segmentation（场景分割）**
- **Image Classification（图像分类）**
- **Image Captioning（图像描述生成）**

### 1.2 Natural Language Processing（自然语言处理）
- **Question Answering（问答系统）**
- **Machine Translation（机器翻译）**
- **Sentiment Analysis（情感分析）**
- **Web Search（网页搜索）**

### 1.3 Speech（语音）
- **Automatic Speech Recognition, ASR（自动语音识别）**
- **Text-To-Speech, TTS（文本转语音合成）**
- **Speaker Verification（说话人验证）**
- **Chatbots（聊天机器人）**

### 1.4 Robotics（机器人）
- 自动驾驶汽车（Autonomous Vehicles）
- 仓储机器人（Warehouse Robots，如 Amazon 仓库机器人）
- 救援机器人（Rescue Robots）
- 足球机器人（Robot Soccer）

### 1.5 Games & Planning（博弈与游戏）
- 在多种游戏中达到或超过人类顶级水平的 AI 系统

### 1.6 目前 AI 还做不到的事 —— "门槛测试（Threshold Tests）"

| 任务 | AI 是否胜任？ |
|------|---------------|
| 打乒乓球（达到不错水平） | ? |
| 参加 Jeopardy 问答节目 | ✓（Watson） |
| 驾驶在弯曲的山路上 | ? |
| 在城市主干道上安全驾驶 | ? |
| 在线购买杂货 | ? |
| 去线下超市购买杂货 | ✗ |
| 发现 / 证明数学定理 | 部分可以 |
| 连续与人对话一小时 | 部分可以 |
| 叠衣服 | ✗ |
| 写有趣的故事 | 部分可以 |

---

## 2. 什么是人工智能？

### 2.1 四种经典定义（2×2 矩阵）

|  | **像人类一样（Human-like）** | **理性地（Rationally）** |
|--|----------------|------------|
| **思考（Think）** | Cognitive Science / Neuroscience（认知科学 / 神经科学） | Logic & Automated Reasoning（逻辑与自动推理） |
| **行动（Act）** | Turing Test（图灵测试） | Intelligent Agents（智能体） |

> 本课程主要聚焦在 **Acting Rationally（理性行动）** —— 即 "Intelligent Agents（智能体）" 这一象限。

---

## 3. 像人一样行动 —— Turing Test（图灵测试）

### 3.1 背景
- **Alan Turing 在 1950 年提出**
- 原始问题：*"机器能思考吗？"* → 重新表述为 *"机器能表现得像有智能吗？"*
- 给出了关于"智能"的一种 **Operational Definition（操作性定义）**

### 3.2 工作方式
- 一位人类 Interrogator（审问者）以文字形式同时与一名人类和一个 AI 对话
- 如果审问者无法可靠地区分哪一个是 AI → 则认为 AI "通过" 图灵测试

### 3.3 通过图灵测试的尝试

| 时期 | 系统 | 说明 |
|------|------|------|
| 1960s | **ELIZA**（Joseph Weizenbaum） | 基于模式匹配的早期聊天机器人 |
| 1990s | **ALICE** | 自然语言对话系统 |
| 持续至今 | **Loebner Prize** | 年度图灵测试竞赛 |

> **关键事实**：至今还没有机器被公认完全通过图灵测试。

### 3.4 应用：CAPTCHA
- **C**ompletely **A**utomatic **P**ublic **T**uring test to tell **C**omputers and **H**umans **A**part  
  （全自动区分计算机与人类的公开图灵测试）
- 这是一个 **Reverse Turing Test（反向图灵测试）** —— 让人类证明自己不是机器

### 3.5 一个关键问题
> *为什么我们要模仿人类行为，包括各种 Irrational（不理性）和缺陷？*

这就引出了从 "像人一样行动" 向 "理性地行动" 的转变。

---

## 4. Acting Rationally（理性地行动）

### 4.1 理性的定义
- **做"正确"的事** —— 不只是"人类通常会怎么想或怎么做"
- "正确"可以从两个角度理解：
  - **Logic（逻辑角度）**：结论可由前提严格推导
  - **Economics（经济学角度）**：结果带来的 Utility（效用）最大

### 4.2 重要区分

| 常见误解 | 实际含义 |
|----------|----------|
| Irrational（不理性）= 疯狂 | 不理性只意味着次优、未达到最优 |
| Rational（理性）= 一定成功 | 即使采取理性行动也可能失败（因为信息不完备、环境不可控等） |

> **核心洞见**：理性关注的是 *做出什么决策*，而不是内心"如何思考"的过程。

### 4.3 AI 作为理性机器
- **Rational（理性）**：在给定目标下，尽可能好地达成目标
- 目标通过 **Utility Function（效用函数）** 来表达
- 理性行动 = **Maximize Expected Utility（最大化期望效用）**

### 课程核心主题
> **MAXIMIZE YOUR EXPECTED UTILITY（最大化你的期望效用）**

---

## 5. 设计 Rational Agent（理性智能体）

### 5.1 关键定义
- **Agent（智能体）**：能够 **Perceive（感知）** 并 **Act（采取行动）** 的实体
- **Rational Agent（理性智能体）**：选择能**最大化（期望）效用**的行为

### 5.2 哪些因素决定采用什么技术？
取决于以下三个方面的特性：
1. **Percepts（感知）**：智能体能获得什么信息
2. **Environment（环境）**：智能体所处的外部世界如何
3. **Action Space（动作空间）**：智能体能采取哪些行动

→ 这些因素共同决定应该使用哪种 AI 技术。

### 5.3 示例：把 Pac-Man 看作一个智能体
- **Percepts（感知）**：当前游戏状态（鬼的位置、食物分布等）
- **Actions（动作）**：向上 / 下 / 左 / 右移动
- **Goal（目标）**：最大化得分（吃掉更多食物，同时躲避鬼）

---

## 6. 课程目标

- 在学习 AI 的过程中获得乐趣
- 理解炒作背后真正重要的核心思想
- 学习**关键技术与算法（Key Techniques & Algorithms）**
- 能够将 AI 应用于**真实世界问题（Real-World Problems）**
- 激发科研思维和进一步探索的兴趣

> **课程范围**：本课并不主要聚焦于视觉、自然语言处理或机器学习，而是以**经典 AI（Classical AI）** 为核心（搜索、规划、优化、推理等）。

---

## 7. 人工智能简史

### 7.1 前史阶段（约公元前 400 年起）

| 学科 | 贡献 |
|------|------|
| Philosophy（哲学） | 心身问题、二元论、唯物主义等思想 |
| Mathematics（数学） | Logic（逻辑）、Probability Theory（概率论）、Decision Theory（决策理论）、Game Theory（博弈论） |
| Cognitive Psychology（认知心理学） | 对人类心智与认知过程的理解 |
| Computer Engineering（计算机工程） | 计算硬件与体系结构基础 |

### 7.2 AI 的诞生（1943–1956）

| 年份 | 事件 |
|------|------|
| 1943 | McCulloch & Pitts：提出简单的 Neural Network（神经网络）模型 |
| 1950 | Turing Test（图灵测试）被提出 |
| 1955–56 | Newell & Simon：Logic Theorist（逻辑理论家）程序 |
| **1956** | **Dartmouth Conference（达特茅斯会议）** —— "Artificial Intelligence（人工智能）" 这一术语正式被提出并采用（McCarthy, Minsky, Rochester, Shannon） |

### 7.3 早期成功（1950–1960）

| 年份 | 成就 |
|------|------|
| 1952 | Arthur Samuel：通过 Self-play（自我博弈）学习的西洋跳棋程序 |
| 1958 | McCarthy：发明 LISP 语言、提出 "advice taker"、推广 Time-sharing（分时系统） |
| 1958 | Rosenblatt：Perceptron（感知机）能学习识别字母 |
| 1968–72 | Shakey 机器人（使用 **A\*** 搜索算法） |
| 1971–74 | Blocksworld 积木世界中的规划与推理研究 |

### 7.4 First AI Winter（第一次 AI 寒冬，1970 年代后期）

- **1969**：Minsky & Papert 的著作 *Perceptrons* 证明单层神经网络无法表示 XOR
- **1973**：Lighthill 报告导致英国 AI 项目大规模被砍
- **1970s**：DARPA 大幅削减对 AI 项目的经费支持

> **经验教训**：过度承诺（Overpromising）、炒作过头（Overhyping）往往导致资金和关注的崩塌。

### 7.5 Expert Systems（专家系统时代，1970–1980）

- 基本思路：把领域专家的知识编码为 **Logic Rules（逻辑规则）**
- 代表性系统：
  - **DENDRAL**：用于推断分子结构
  - **MYCIN**：用于医疗诊断（Medical Diagnosis）
- 1981：日本提出 "第五代计算机" 计划（以 Prolog 为基础）
- 1982：**R1** —— 为 DEC 计算机订单配置提供支持的专家系统

### 7.6 聚焦应用（1990–2010）

| 年份 | 里程碑 |
|------|--------|
| 1997 | **Deep Blue** 在国际象棋（Chess）中击败世界冠军 Kasparov |
| 2001–10 | 约 600 亿美元的 Combinatorial Auctions（组合拍卖）中使用 AI 技术 |
| 2005/07 | Stanford 与 CMU 在 DARPA Grand Challenge（自动驾驶比赛）中夺冠 |
| 2011 | **IBM Watson** 在 Jeopardy 节目中战胜人类冠军 |

### 7.7 AI 的再度崛起（2010 至今）

| 年份 | 里程碑 |
|------|--------|
| 2012 | **AlexNet** 赢得 ImageNet 竞赛 —— Deep Learning（深度学习）浪潮由此爆发 |
| 2013 | DeepMind：从像素端到端学习 Atari 游戏（End-to-end Learning） |
| 2015–17 | Speech Recognition（语音识别）在部分任务上达到或超过人类水平 |
| 2015+ | 生成逼真的假图像与视频（GAN 等 Generative Models（生成模型）） |

> 大型科技公司（Google, Facebook, Microsoft, Amazon 等）纷纷建立大规模 AI 研究院。

---

## 8. AI 处在什么位置？

```text
AI
├── Machine Learning（机器学习）
│   ├── Deep Learning（深度学习）
│   └── Statistical Learning（统计学习）
├── Search & Planning（搜索与规划）
├── Knowledge Representation（知识表示）
├── Natural Language Processing（自然语言处理）
├── Computer Vision（计算机视觉）
└── Robotics（机器人）
```

---

## 9. 阅读材料

| 讲次 | 阅读内容 |
|------|----------|
| 今天（Lecture 1） | RN 第 1、2 章 |
| 下一次（Lecture 2） | RN 第 3.1–3.4 节 |

> **RN** = *Artificial Intelligence: A Modern Approach*，作者 Russell & Norvig

---

## 10. 核心概念小结

| 概念 | 定义 |
|------|------|
| AI | 研究如何让机器像人类一样或以理性方式思考 / 行动的科学 |
| Turing Test（图灵测试） | 通过"与人类难以区分的对话行为"来检验智能的测试 |
| CAPTCHA | Reverse Turing Test（反向图灵测试），用来区分人类和机器人程序 |
| Rational Agent（理性智能体） | 能够感知环境、采取行动，并最大化其 Expected Utility（期望效用）的实体 |
| Expected Utility（期望效用） | 按结果概率加权后的效用平均，用作优化目标 |
| AI Winter（AI 寒冬） | 由于期望过高、进展不及预期而导致资金与兴趣大幅下降的时期 |

---

## 11. 个人笔记与思考

- **四象限框架**（思考 / 行动 × 像人 / 理性）是梳理不同 AI 研究路线的一个非常清晰的心智模型。
- 从"像人一样行动"转向"Acting Rationally（理性地行动）"是一个根本性的转变 —— 它使我们可以用数学和效用最大化来严格刻画智能行为。
- **历史启示**：AI Winter（AI 寒冬）提醒我们警惕炒作。当前深度学习带来的 AI 繁荣（自 2012 年以来）要靠持续的实际价值来支撑。
- 把 **Pac-Man Agent（Pac-Man 智能体）** 作为例子非常形象：足够简单，便于分析；又足够丰富，可以承载许多智能体与决策理论的关键概念。
- 课程对**经典 AI 技术（Classical AI Techniques）**（搜索、约束满足、优化、推理等）的强调，为理解和解释现代机器学习系统提供了坚实的基础。
