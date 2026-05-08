# Self-Check: Vision

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## Depthwise Separable Convolution

- [浅] 标准卷积同时做了哪两件事？这两件事为什么贵？ → `KNOWLEDGE/vision/depthwise-separable-convolution/`
- [浅] depthwise + pointwise 的拆分让每一步只负责什么？ → `KNOWLEDGE/vision/depthwise-separable-convolution/`
- [中] `Cin=3, Cout=8, K=3` 时，标准卷积和 depthwise+pointwise 的参数量分别是多少？比例多少？ → `KNOWLEDGE/vision/depthwise-separable-convolution/`
- [中] 1x1 卷积为什么能混通道但不能看空间邻域？ → `KNOWLEDGE/vision/depthwise-separable-convolution/`
- [深] 深度可分离卷积"不完全等价于"标准卷积。具体损失了什么表达自由度？为什么 MobileNet 仍然愿意付这个代价？ → `KNOWLEDGE/vision/depthwise-separable-convolution/`
