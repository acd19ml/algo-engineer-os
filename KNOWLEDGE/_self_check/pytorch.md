# Self-Check: PyTorch

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## 分类训练 Loop

- [浅] 一个最小的 PyTorch 分类训练 loop 包含哪些必要步骤？少哪个会出问题？ → `KNOWLEDGE/pytorch/classification-training-loop/`

## Cross Entropy Loss

- [浅] logits 是什么？范围有限制吗？需要求和为 1 吗？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`
- [浅] `CrossEntropyLoss` 应该配什么输入？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`
- [浅] `NLLLoss` 应该配什么输入？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`
- [中] 错误组合"softmax 后再喂 CrossEntropyLoss"会发生什么？数值上会怎么错？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`
- [中] 3 分类中 `q = [0.2, 0.7, 0.1]`，真实标签是类别 0，cross entropy 是多少？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`
- [中] perplexity 和 cross entropy 的关系是什么？perplexity 直觉上代表什么？ → `KNOWLEDGE/pytorch/cross-entropy-loss/`

---

## 训练 Loop 关键概念区分

- [浅] 五步 loop 的顺序 ZFLBS 各对应哪个调用？少 zero_grad、少 backward、少 step 分别会怎样？ → `KNOWLEDGE/pytorch/classification-training-loop/`
- [中] `loss.backward()` 和 `optimizer.step()` 分工不同——前者是反向传播算梯度，后者是参数更新。为什么不能统称"反向传播"？ → `KNOWLEDGE/pytorch/classification-training-loop/`
- [中] PyTorch 为什么把梯度设计成累加而不是覆盖？这个设计支持了什么特殊用法？代价是什么？ → `KNOWLEDGE/pytorch/classification-training-loop/`
- [中] `nn.Embedding` 输入必须是哪种 dtype？为什么是这种？范围有什么硬性约束？ → `KNOWLEDGE/pytorch/classification-training-loop/`

## 跨节点综合

- [深] 训练 loop 里 loss 的 backward 之前是否要 zero_grad？为什么？这背后的 PyTorch autograd 行为是什么？ → `KNOWLEDGE/pytorch/classification-training-loop/`
- [深] 为什么模型应输出 logits 而不是 softmax 后的概率？错误组合（softmax 后再喂 CrossEntropyLoss）会怎么坏？为什么这种 bug **不会报错** 但梯度坏掉？ → `KNOWLEDGE/pytorch/cross-entropy-loss/` + `KNOWLEDGE/pytorch/classification-training-loop/`
