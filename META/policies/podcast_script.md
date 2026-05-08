# Podcast Script Form

> "听"的脚本规约。所有 `PODCAST/<domain>/<topic>.md` 必须遵守。
>
> 这一层和 KNOWLEDGE 形态有区别——KNOWLEDGE 给眼睛看（视觉布局可以有标题、bullet、公式），PODCAST 给耳朵听（线性流动散文，所有视觉元素都念不出来）。

---

## 这一层是什么

PODCAST 服务"边运动边学"的场景：用户跑步、通勤时听 AI 语音播放脚本。两种用法：

- **(a) Review 型**：已有 KNOWLEDGE 节点的"听版"——同样的内容，重新写成可听的形态。日常复习用。
- **(b) Pre-learning 型**：用户还没系统学的内容，先写成讲解脚本听一遍——后续如果对话深入了，再走 triage 长成 KNOWLEDGE 节点。

---

## 形态规则

### 必含

1. **完整流动散文**。从头到尾一口气念下来不卡。听众无法翻回去看，需要线性结构。
2. **数字 / 公式用口语描述**：
   - ✅ "零点五的二十次方，大概是十的负六次方"
   - ❌ "0.5^20 ≈ 1e-6"
   - ✅ "softmax 里 QK 转置除以根号 dk"
   - ❌ "softmax(QK^T / √d_k)"
3. **关键转折前有提示性短句**——帮听众跟上节奏：
   - "注意"、"听到这里你可能会问"、"OK 我们换个角度"
   - "最后留一个问题给你想"、"反过来想"
4. **冗余冗一点**：重要点重复一遍 + 换角度说一次。听众无法翻回去看，必须靠重复抓住关键。
5. **长度**：5-15 分钟，约 800-2500 字（按朗读语速估）。短于 5 分钟信息量不够，长于 15 分钟听众累。

### 禁止

- markdown 标题（`##`、`###`）出现在脚本正文里——不会被念出来
  - 例外：文件最顶部可以有一个 `#` 标题作为文件名标识，但写作时把它当成"封面"，不在朗读范围
- bullet 列表（`-`、`*`、`1.`）
- 公式符号、代码块、表格
- 一句超过两口气念不完的长复合句

### 建议但非强制

- **开场两句话定锚**："今天聊一个 X" / "你训练 X 时会遇到 Y" / "面试常被问 Z"
- **收尾留思考钩子**："你跑步的时候可以顺便想一下" / "下次开 session 时我们聊聊 X"——不要机械"今天就到这里"
- 自然的口语连接词——"那"、"OK"、"其实"、"换句话说"——比书面语更易听

---

## 文件组织

```
PODCAST/
├── README.md                            # 解释两类用法
└── <domain>/
    └── <topic-slug>.md
```

filename 直接是话题 slug，类型靠 frontmatter 区分。

例：

- `PODCAST/ml/gradient-flow.md`（review 型）
- `PODCAST/transformer/qkv-three-matrix-design.md`（review 型）
- `PODCAST/llm/long-context-degradation-intro.md`（intro 型，filename 加 `-intro` 是建议、非强制）

---

## 元数据（frontmatter）

```yaml
---
type: review | intro
domain: ml | nlp | transformer | ...
estimated_minutes: 5
last_updated_at: YYYY-MM-DD

# review 型：mirror 哪些 KNOWLEDGE 节点
related_nodes:
  - KNOWLEDGE/ml/gradient-flow-deep-networks/

# intro 型：未来可能长成的目标节点 + 来源提示
target_for_future_node: KNOWLEDGE/llm/long-context-degradation/   # 可选
source_hint: "video on transformer attention by 张三"             # 可选，自由文本，不引用 INBOX 路径
---
```

---

## Ownership

PODCAST 是 LLM 写入区，但 **不自动触发**——用户明确说"把 X 做成播客脚本"或"我还没学 Y 给我讲一遍"时由 LLM 写。

- **Review 型**：从对应 KNOWLEDGE 节点改写为听觉形态。内容应保持一致（concept-level），但重新组织叙述使其听得舒服。如果两边出现冲突，KNOWLEDGE 节点是 source of truth。
- **Intro 型**：从用户提供的 paper / 视频 transcript / 话题，写成讲解脚本。后续如果对话深入，可触发建对应 KNOWLEDGE 节点。

---

## 写完前的自检清单

- [ ] 整篇可以从头到尾朗读不卡？
- [ ] 没有不会被念出来的 markdown 元素（标题、bullet、公式符号、代码块）？
- [ ] 数字和公式都翻译成口语了？
- [ ] 长度合适（5-15 分钟，800-2500 字）？
- [ ] 关键转折前有提示性短句？
- [ ] 重要概念有重复 / 换角度复述？
- [ ] 收尾有思考钩子，不是机械结束？
- [ ] frontmatter 完整（type、domain、related_nodes 或 target_for_future_node）？
