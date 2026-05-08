# PODCAST

听觉形态的学习层。脚本写给 AI 语音播放、用户跑步 / 通勤时听。

---

## 这一层是什么

`PODCAST/` 不是 KNOWLEDGE 的复制粘贴，也不是音频文件存放区。它是**给耳朵的版本**：

- KNOWLEDGE 节点：眼睛看的形态——可以有标题、bullet、公式符号、代码块。读者来回看、跳着看。
- PODCAST 脚本：耳朵听的形态——纯流动散文。听众无法翻回去，必须线性结构 + 重复关键点 + 口语化数字。

两层服务同一个学习目标，但形态不同。

---

## 两类用法

### (a) Review 型

已有 KNOWLEDGE 节点的"听版"。日常复习用。

例：用户已经学过 `KNOWLEDGE/ml/gradient-flow-deep-networks/`，想跑步时复习一遍——LLM 把节点改写成 `PODCAST/ml/gradient-flow.md`。

frontmatter：

```yaml
type: review
related_nodes:
  - KNOWLEDGE/ml/gradient-flow-deep-networks/
```

### (b) Pre-learning 型

用户还没系统学的内容，先听一遍。听完可能感兴趣再开对话深入——后续走 triage 长成 KNOWLEDGE 节点。

例：用户提到"还没来得及学 long-context degradation，给我写个播客脚本听"——LLM 写 `PODCAST/llm/long-context-degradation-intro.md`。

frontmatter：

```yaml
type: intro
target_for_future_node: KNOWLEDGE/llm/long-context-degradation/
source_hint: "..."
```

---

## 形态规则速览

详见 `META/policies/podcast_script.md`。要点：

- 完整流动散文，从头到尾朗读不卡
- 数字 / 公式口语化（"零点五的二十次方" 不是 "0.5^20"）
- 没有 markdown 子标题、bullet、公式符号、代码块
- 5-15 分钟（800-2500 字）
- 关键转折前有提示性短句帮听众跟上
- 重要点重复 + 换角度复述
- 收尾留思考钩子，不机械结束

写脚本前先读 `META/llm/few_shots/podcast_script.example.md` 看具体形态。

---

## 文件组织

```
PODCAST/
├── README.md
├── ml/
│   └── gradient-flow.md
├── transformer/
│   └── qkv-three-matrix-design.md
└── llm/
    └── long-context-degradation-intro.md
```

domain 边界和 `KNOWLEDGE/<domain>/` 一致。intro 型 filename 加 `-intro` 后缀辅助识别（建议非强制，type 在 frontmatter）。

---

## Ownership

LLM 写入区，但**不自动触发**。

触发方式：用户明确说

- "把 KNOWLEDGE/ml/gradient-flow-deep-networks 做成播客脚本"
- "我还没学 long-context degradation，给我写个播客脚本听一遍"

LLM 不在 triage 时自动建播客脚本——这是用户主动请求的产物。

---

## 与 KNOWLEDGE 的关系

| | KNOWLEDGE | PODCAST |
|---|---|---|
| 形态 | 视觉布局（标题、bullet、公式、代码块） | 听觉散文（无视觉元素） |
| 公式 | `softmax(QK^T/√d_k)` | "softmax 里 QK 转置除以根号 dk" |
| 节奏 | 读者自己控制（来回看） | 线性叙述（不能跳回） |
| 动作 | 边看边记 | 跑步 / 通勤边听边想 |
| Source of truth | 是 | review 型不是；冲突时以 KNOWLEDGE 为准 |

---

## 使用建议（来自用户）

> "我某天跑步就是听着脚本，可以一边思考一边运动。所以这部分适用于听，knowledge 适用于看。后续我会希望，有一些知识我还没来得及学，把这部分内容写成脚本我自己用 AI 语音播客来给我讲。"

按这个原则使用：review 型用于巩固已学，intro 型用于尚未系统学习的内容预热。
