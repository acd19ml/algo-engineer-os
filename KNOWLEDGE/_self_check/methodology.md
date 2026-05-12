# Self-Check: Methodology

> 日常自检：从上往下看题，能答出来跳下一题；卡住就点链接跳到知识节点重新学。
> 答案不在这里——答案在链接的节点里。

---

## 答题方法（机制类问题）

- [浅] 面试被问 "讲一下 X 机制"，从论文目录顺序复述（input → operation → output）有什么根本问题？ → `KNOWLEDGE/methodology/answer-form-for-mechanisms/`
- [浅] 五层框架 L1 到 L5 各自该讲什么？ → `KNOWLEDGE/methodology/answer-form-for-mechanisms/`
- [中] L2 "设计动机" 该怎么展开才有区分度？为什么 "如果不这样会怎样" 比 "这样做是为了 X" 强一个数量级？ → `KNOWLEDGE/methodology/answer-form-for-mechanisms/`
- [中] 用 attention 当例子：L1 / L2 / L3 / L4 / L5 各举一个具体小问题。 → `KNOWLEDGE/methodology/answer-form-for-mechanisms/` + `KNOWLEDGE/transformer/qkv-three-matrix-design/`
- [中] 四条回答策略——节奏 / 反事实 / 具体数字 / 承认边界。每条背后的判别本质是什么？为什么"不全部一口气倒出来"反而显得从容？ → `KNOWLEDGE/methodology/answer-form-for-mechanisms/`
- [深] 这套五层框架在 system design 类问题上能直接套用吗？哪几层适用、哪几层需要改？ → `KNOWLEDGE/methodology/answer-form-for-mechanisms/#open-questions` (open)

## 架构设计 6 步法

- [浅] 6 步法的顺序是什么？产品定位 / 原型图 / API / 数据表 / 模块拆分 / 详细设计——这个顺序为什么不能反过来？ → `KNOWLEDGE/methodology/architecture-design-six-steps/`
- [浅] 跳过"产品定位 + 原型图"直接画架构图会发生什么连锁返工？ → `KNOWLEDGE/methodology/architecture-design-six-steps/`
- [中] "表的边界决定模块边界"这条原则背后的逻辑是什么？模块拆分跳过数据表设计会出什么问题？ → `KNOWLEDGE/methodology/architecture-design-six-steps/`
- [中] "团队全员参与架构设计"这条建议的前提是什么？让算法同学参与后端架构设计的问题在哪里？ → `KNOWLEDGE/methodology/architecture-design-six-steps/`（"团队共识"段）
- [中] 重大变更 / 普通功能 / 小变更 / bugfix 各自适用 6 步法的哪些步骤？怎么判断变化的规模？ → `KNOWLEDGE/methodology/architecture-design-six-steps/`
- [深] 6 步法理论上每一步约束下一步、方向一变就全套返工——但实战中能不能用"接口稳定 + 实现替换"的方式让上层不重做？ → `KNOWLEDGE/methodology/architecture-design-six-steps/#open-questions` (open)

## 三类决策层级文档

- [浅] 技术提案 / 架构设计 / 实现设计三类文档的核心问题各自是什么？为什么"决策层级 ≠ 详略差异"？ → `KNOWLEDGE/methodology/three-tier-decision-docs/`
- [浅] 用 Kubernetes 做例子——KEPs / Cluster Architecture / API Conventions 各自对应哪一类？ → `KNOWLEDGE/methodology/three-tier-decision-docs/`
- [中] 团队在技术提案阶段争论字段名 / 在实现设计阶段还在争"该不该做"——这两种现象各暴露什么问题？ → `KNOWLEDGE/methodology/three-tier-decision-docs/`
- [中] 用关键词判断文档归属：motivation / proposal / alternatives → 哪类？architecture / component / control plane → 哪类？API / schema / field → 哪类？ → `KNOWLEDGE/methodology/three-tier-decision-docs/`
- [中] 三类文档跟"架构设计 6 步法"的关系是什么？为什么"6 步法走得稳，底层方向没共识"仍然失败？ → `KNOWLEDGE/methodology/three-tier-decision-docs/`（"与 6 步法的联系"段）+ `KNOWLEDGE/methodology/architecture-design-six-steps/`
- [深] AI 生成"混合层级文档"——如何自动检测当前 AI 生成的设计文档属于哪一类、缺哪一类？ → `KNOWLEDGE/methodology/three-tier-decision-docs/#open-questions` (open)

## AI 产品决策四问（面试自检框架）

- [浅] AI 产品决策四问是哪四问（场景判断 / 风险意识 / 标准感 / 边界感）？每一问检验什么能力？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/`
- [浅] 为什么"AI 不是万能的"加上"靠提示词压一压就算了"会立刻暴露候选人没经历过 AI 上线？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/`（第二问）
- [中] "事前定指标 vs 事后补指标"的本质区别是什么？为什么事后补的几乎等于没指标？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/`（第三问）
- [中] 边界感问到"AI 处理不了的怎么 fallback"——如果你回答"边界没画 / 没调过"，面试官会立即得出什么判断？为什么"边界是 AI 系统的一等公民"？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/`（第四问）
- [中] 用四问框架反向重塑旧项目叙事——具体怎么操作？为什么"挑参与最深的小项目"比"铺很广讲大项目"强？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/`
- [深] 四问之外是否还有第五问值得加（如"演进 / 退役 / 重构"）？AI 工程师 vs AI 产品经理 vs AI 训练师的四问侧重是否应该不同？ → `KNOWLEDGE/methodology/ai-product-decision-four-questions/#open-questions` (open)

---

## 跨节点综合

- [深] **三个 methodology 节点串成一条决策叙事链**：6 步法（架构设计层内部顺序）/ 三类决策层级文档（架构设计在整个流程中的位置）/ 四问框架（讲清决策过程的话术）——把一个完整的项目讲给面试官时，**怎么用这三层框架同时讲清"做了什么 + 怎么决策 + 决策过程能讲扎实"**？ → `KNOWLEDGE/methodology/architecture-design-six-steps/` + `KNOWLEDGE/methodology/three-tier-decision-docs/` + `KNOWLEDGE/methodology/ai-product-decision-four-questions/`
- [深] **七牛云 ZeroOps 失败教训用三个 methodology 节点反向解读**：项目走了 6 步法但仍然三次返工——失败原因不在 6 步法层，而在缺"技术提案"层；CEO 后期拍板本质上是替团队补"技术提案 + 共识"环节。**用 AI 产品决策四问的"场景判断"和"标准感"反观 ZeroOps 团队当时缺什么？** → 全部三个节点 + `PROJECTS/work/qiniu-zeroops-rca-agent/`
