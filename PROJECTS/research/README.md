# PROJECTS / research

论文复现 / 自主技术探索类项目。区别于 `work/`：没有公司 / 团队边界，由我个人发起；交付物以"评测方法学 + 受控实验 + 边界结论"为主。

## 已完成

- ✅ `awm-mechanism-audit/` — AWM (Agent Workflow Memory) on Mind2Web 复现 + 机制审计 + 失败模式诊断。**为 Final Presentation 交付**，结论：AWM 是 partial, condition-dependent procedural memory；缺 failure-driven revision loop
- ✅ `selective-transfer-memory/` — 记忆跨任务复用诊断 pilot（HotpotQA → 2WikiMultiHopQA 近迁移）。**为团队课程项目交付**，结论：固定经验预算下，匹配粒度 + 算子可执行抽象共同决定 episodic / consolidation 记忆是否真起作用

## 这两个项目和 CV 的关系

CV 的"Agent Memory 自主研究项目"栏（`CAREER/cv.md`）两条 bullet 即来自这两份研究：

| CV bullet | 项目页 |
|---|---|
| AWM @ Mind2Web step-level 配对 / 6-18% 影响窗口 / paired-case 评测方法学 | `awm-mechanism-audit/` |
| HotpotQA → 2WikiMultiHopQA / matched-mismatched 配对 / 两次受控修复 | `selective-transfer-memory/` |

当面试官追问"你这条 bullet 是什么意思"，打开对应项目页即可。

## 触发条件

- 论文复现型探索完成（"我读了这篇论文 + 跑了实验 + 有发现"）
- 自主设计的小规模 pilot 完成（"我设计了一个 controlled comparison 测试某个假设"）
- 横向对比研究形成完整产出（不只 PROBLEMS 单页对比，而是产出了 paired evaluation）

## 项目页结构

参考 `META/templates/project_README.template.md`。`type: research`。

如果是论文复现，README 至少包含：
- 复现的什么（paper claim）
- 在什么 setting 下复现（model / dataset / decoding）
- 哪些 claim hold up，哪些不 hold
- 自己加了什么诊断（mechanism audit）
- 我从中得到的研究判断
