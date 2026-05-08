# Self-Check: NLP

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## NLP Pipeline / Tokenization

- [浅] 为什么需要 tokenization？word-level 和 char-level 各自的极端缺陷是什么？ → `KNOWLEDGE/nlp/nlp-pipeline-tokenization/`

## BPE Tokenization

- [浅] BPE 的"加权频率"指什么？ → `KNOWLEDGE/nlp/bpe-tokenization/`
- [中] BPE 手算第一步应该先做什么？最容易出错在哪一步？ → `KNOWLEDGE/nlp/bpe-tokenization/`
- [中] BPE 为什么不能完全消除 OOV？什么情况下 token 会变成 `[UNK]`？ → `KNOWLEDGE/nlp/bpe-tokenization/`

## Padding 和 Attention Mask

- [浅] 为什么需要 padding？它解决了什么、又引入了什么问题？ → `KNOWLEDGE/nlp/padding-and-attention-mask/`
- [浅] attention mask 的 1 和 0 分别表示什么？ → `KNOWLEDGE/nlp/padding-and-attention-mask/`
- [中] BERT 调用时漏传 `attention_mask` 会怎样？self-attention 会被怎么污染？工程上怎么把 padding 位置的 attention 权重压到 0？ → `KNOWLEDGE/nlp/padding-and-attention-mask/`
- [中] mean pooling 时为什么必须用 mask 加权平均？不用会怎么稀释句子表示？ → `KNOWLEDGE/nlp/padding-and-attention-mask/`
- [中] Padding mask 和 causal mask 的区别是什么？形状、目的、何时用？ → `KNOWLEDGE/nlp/padding-and-attention-mask/`

## Neural Language Model

- [中] 什么决定了一个语言模型是 "neural" 的？相对 n-gram 的根本变化在哪？ → `KNOWLEDGE/nlp/neural-language-model/`

## NER / Sequence Modeling

- [浅] NER 是 token-level 任务还是 sentence-level？这决定了模型选择的什么？ → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] 多层 RNN 处理几百词 NER 有哪三个具体问题？ → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] 为什么 NER 经常需要双向上下文？用 `Apple announced...` 例子说明。 → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] BiLSTM-CRF 中 CRF 层在解决什么？什么是非法的 BIO 标签转移？ → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] BERT 做 NER 时，分类头接在哪里？为什么这是 SOTA？ → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] WordPiece 把 `Washington` 切成 `Wash + ##ington`，原本的 `B-LOC` 标签该怎么对齐？两种主流方案是什么？ → `KNOWLEDGE/nlp/ner-sequence-modeling/`
- [中] NER 任务里 padding 位置为什么不应贡献 loss？ → `KNOWLEDGE/nlp/ner-sequence-modeling/` + `KNOWLEDGE/nlp/padding-and-attention-mask/`

## Task-Oriented Dialogue System

- [浅] task-oriented dialogue system 和 open-domain chatbot 的核心目标差别是什么？ → `KNOWLEDGE/nlp/task-oriented-dialogue-system/`

---

## 跨节点综合

- [深] BPE 处理过的 token 进入模型前还要做 padding——这两步一前一后，但都涉及"特殊 token"。`[UNK]` 和 `[PAD]` 的角色差别是什么？模型对它们的处理方式分别是什么？ → `KNOWLEDGE/nlp/bpe-tokenization/` + `KNOWLEDGE/nlp/padding-and-attention-mask/`
