<!-- PROCESSED: 2026-05-13 → PROJECTS/research/awm-mechanism-audit/ -->

# AWM Final Presentation Speaker Notes

Aligned with:

- [slide-deck-plan.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/report/tmp/pre/slide-deck-plan.md)

Use this as a spoken guide rather than a script that must be read word-for-word. The English is the main presentation text. The Chinese lines are cues for fast review and rehearsal.

## Slide 1. AWM as a Partial Solution to Procedural Memory for GUI Agents

### English

Good afternoon. Today I will present the final outcome of my guided study on memory for GUI agents, with a focus on reproducing and analyzing AWM, or Agent Workflow Memory.

The shortest version of my conclusion is this: AWM is a meaningful step toward procedural memory, but it is not yet a complete memory mechanism.

### 中文提示

先把整场的主结论立住：`AWM 是程序性记忆的重要一步，但还不是完整解。`

---

## Slide 2. From a Broad Memory Survey to a Narrow Procedural-Memory Question

### English

Let me start from the transition between the interim report and the final report.

In the interim report, I began with a broad question about memory for GUI and web agents. But by the end of that review, the problem had become much narrower for me. The real issue was procedural memory: not just storing past information, but storing reusable task workflows.

Once I looked at it that way, a second issue became unavoidable, which is failure-driven write-back. If a stored procedure turns out to be weak or misleading, how does the agent revise it instead of repeating the same mistake?

So the final report asks a more focused question: how far does AWM actually go in addressing the procedural-memory gap, and where does it break down?

### 中文提示

这一页只做一件事：说明 Final 不是换题，而是把 Interim 的 gap 收窄成了一个更尖锐的问题。

---

## Slide 3. Why AWM Is the Right Focal Case

### English

I chose AWM very deliberately.

Among the systems I reviewed, AWM is one of the clearest attempts to extract workflows after task completion and reuse them across later tasks. That makes it a strong focal case for the procedural-memory question raised in the interim report.

So I am not presenting AWM just because it is a well-known paper, or because it was convenient to reproduce. I am using it as a representative test case for one specific research gap.

### 中文提示

这里要让老师听明白：`我不是随便挑了一篇论文复现，而是在拿一个代表性方法测试我在 Interim 里发现的 gap。`

---

## Slide 4. This Final Report Is Reproduction Plus Mechanism Audit

### English

That leads to what I actually did in the final study.

I approached the work in three steps.

First, I did a faithful reproduction of the main Mind2Web claims. At the basic level, I wanted to see which parts of the paper’s story still held in my setting.

Second, I moved beyond aggregate scores and performed a mechanism audit. I wanted to know where workflow memory actually changes behavior, and what kind of help it provides when it does help.

Third, I looked at failure modes and boundary conditions. The point was not only to ask whether AWM works, but to ask when it helps, when it hurts, and what those patterns mean for memory design more broadly.

So this final report is not just a rerun of the original pipeline. It is reproduction plus interpretation.

### 中文提示

三层工作：

- reproduction
- mechanism audit
- failure and boundary analysis

最后落一句：`不是简单重跑，而是复现加解释。`

---

## Slide 5. What Holds Up, and What Does Not

### English

Before going into the detailed findings, let me give the high-level verdict.

What held up best in my reproduction were the mechanistic and structural claims. In particular, LM-induced workflows were indeed more abstract than rule-induced ones, and the workflow libraries were compact.

What became much less stable were the broadest performance narratives. Offline gains were mixed rather than uniform, and the claim that online AWM becomes stronger under larger distribution shift did not reproduce in my setting.

So even at the summary level, the picture is already asymmetric: the core idea survives better than the strongest universality claims around it.

### 中文提示

这一页的关键词是：`mechanism stronger than performance narrative`。

不要读表，要讲判断：

- 支撑得最好的，是结构和机制层面的 claim
- 最不稳定的，是最强的 performance narrative

---

## Slide 6. Finding 1: AWM Is Not Uniformly Effective

### English

The first major finding is that AWM is not uniformly effective.

What I found is not that workflow memory always helps, but that it helps under some conditions and harms under others.

This is visible in the paired-case analysis. On positive-outcome sites such as kayak and newegg, workflow produced zero negative interventions. On negative-outcome sites, the pattern reversed: on budget, negative interventions outnumbered positive ones by 12 to 6, and on sixflags, by 6 to 3.

The other important point is that AWM’s influence window is actually narrow. It changes behavior on only a small fraction of steps, roughly 6 to 18 percent. So the aggregate outcome is not driven by broad, uniform guidance across the whole trajectory. It is driven by a small number of decisive interventions.

That was an important shift in how I interpreted AWM. I stopped seeing it as a broadly effective memory method, and started seeing it as a condition-dependent mechanism.

### 中文提示

这里一定要把证据讲出来，不然会太抽象。

最关键三句：

- 正向 site 没有 negative intervention
- 负向 site 是 negative 多于 positive
- 真正改变行为的 step 只有 6% 到 18%

---

## Slide 7. Finding 2: Abstraction Is Real, but It Does Not Guarantee Better Execution

### English

The second major finding is about abstraction.

One thing that did reproduce clearly is that LM-induced workflows are more abstract at the text level. They are shorter, more parameterized, and contain no concrete task-specific values.

I observed this most clearly in the workflow-text comparison. Across the three audited sites, LM workflows were much shorter, around 1.7 to 2.7 steps per workflow, while the rule-induced versions were much longer, around 7.8 to 12.5 steps, and carried many concrete values.

But that does not automatically translate into better execution.

At the performance level, the comparison is mixed rather than one-sided. On united, LM has a clearer advantage. On newegg, rule workflows can be competitive or even stronger because the task patterns are relatively fixed and the concrete values still transfer well.

So the lesson here is not that abstraction is useless. The lesson is narrower: abstraction is real, and it is promising, but by itself it does not guarantee robust execution.

### 中文提示

这一页不要讲成“LM 更好”。正确说法是：

- LM 的抽象化是真的
- 但抽象化不自动等于更好的执行

最好把 `united` 和 `newegg` 作为一句 qualification 带出来。

---

## Slide 8. What Help Looks Like: Action-Mode Redirection

### English

At this point, I want to show one concrete positive case, so that the mechanism does not remain abstract.

This example comes from the United setting. The task required the agent to enter the departure city. The prompt already contained a workflow about entering flight locations.

In the baseline condition, the model clicked the wrong package-type control. In the workflow condition, it typed the correct city into the correct combobox: `TYPE [10892] [las vegas]`.

So the workflow is not merely adding extra text into the prompt. In this case, it redirects the model toward the correct action mode. That is a cleaner and more convincing mechanism than simply saying that the score improved.

### 中文提示

这页的作用是把“workflow 有时怎么帮”讲具体。

关键句：

- baseline 做错的是 action mode
- workflow 条件把它拉回正确的 `TYPE`
- 所以 workflow 的作用不是“多给信息”，而是“把动作类型导正”

---

## Slide 9. What Harm Looks Like: Workflow-Content Mismatch

### English

Now let me contrast that with a negative case.

This example comes from sixflags. The task is to apply for a job. But the injected workflow is about selecting a park.

In the baseline condition, the model takes the correct `Jobs` click. In the workflow condition, it follows the injected park-selection routine and clicks `Browse the Parks Below` instead.

What matters here is that this is not just a random mistake. It is a workflow-family mismatch. The stored workflow belongs to the wrong task family, but it is still strong enough to redirect the first action.

That is exactly where the limitation shows up. AWM can preserve useful procedures, but if the workflow is mismatched, it can also preserve and replay the wrong procedural bias.

### 中文提示

这页要把“harm”讲成机制，不要讲成普通 error。

落点是：

- 这是 task family mismatch
- 错误不是随机的
- 错在错误 workflow 被带进了 prompt，还影响了第一步

---

## Slide 10. Final Interpretation: AWM Is a Partial, Condition-Dependent Memory Mechanism

### English

Putting these pieces together, my final interpretation is that AWM is a partial and condition-dependent memory mechanism.

It does capture one important part of procedural memory, because it externalizes workflows and reuses them across tasks. That is a real contribution.

But it helps mainly when three things line up: the workflow family is reusable, the retrieved procedure matches the current task, and the baseline still has room for improvement.

What is still missing is a strong revision loop. The system does not yet have a robust way to detect harmful workflows, revise them after failure, or suppress them when the task match is weak.

So my conclusion is not simply that AWM works or fails. It is that AWM shows what procedural memory can look like in practice, but it also shows why workflow reuse alone is not enough. Without failure-driven revision, memory remains helpful, but not fully reliable.

If time allows, before questions I would also like to briefly share a few further thoughts that emerged after the report submission. They do not change the report's conclusion, but they sharpen what I think the next research question should be.

### 中文提示

最后一页不要重新总结所有结果，只收成一个研究判断：

- AWM 确实抓住了 procedural memory 的一部分
- 但它缺 failure-driven revision
- 所以它是 partial, condition-dependent solution，不是 complete solution

最后可以加一句过渡：
`在正式 Q&A 之前，我想补充几页 report 之外的 further thoughts，作为 discussion。`

---

## Slide 11. Further Discussion Beyond the Final Report

### English

At this point, I want to shift very briefly from the submitted report to a broader discussion.

After finishing the report, I kept thinking about whether the next question is really just which AWM module should be improved, or whether the deeper issue is the shape of the memory object itself.

Two later influences pushed me in that direction.

First, in a small memory-transfer study, I found that abstraction was not enough by itself. A memory could be topically relevant and still fail, unless it preserved an executable structure.

Second, recent work on experience-object design suggested that runtime shape matters. The issue is not only what experience is stored, but what kind of object returns to the model at test time.

So this section is not meant to replace the report's conclusion. It is meant to open a more upstream discussion.

### 中文提示

这页只做桥接，不要讲细节。

关键是把 discussion 的层级抬起来：

- 不只是问 AWM 下一步做哪个模块
- 而是问 procedural memory object 应该长什么样

---

## Slide 12. Same Experience, Different Object Shapes

### English

Here I am not trying to rank Skill, AWM, and Gene. I am using them as different design points in the space of experience objects.

Skill is already an external procedural object, but it is still more human-readable and prose-heavy.

AWM represents experience as context-conditioned workflow templates with action slots in web environments. So it is already more executable than a plain summary, but its selection, boundary, and revision mechanisms remain weak.

Gene emphasizes a much more compact runtime control object, where trigger, strategy, avoid constraints, and validation are made more explicit.

That is why I kept the raw snippets on the slide. I want the difference in object shape to be visually obvious rather than only verbally summarized.

So the question for me is not which one is simply better. The deeper question is what shape of procedural memory object is most appropriate under different settings.

### 中文提示

这一页不要讲成线性进化：

- Skill、AWM、Gene 不是高低关系
- 它们是不同 object shape

一定点一句：
`我保留 raw snippets，是为了让形态差异一眼可见。`

---

## Slide 13. A Lightweight Testbed for External Procedural Memory

### English

I then tried to ground this question in a more industrial setting.

Imagine an operations diagnosis scenario where the model is already strong and the tools are already solid. In that case, the model may be able to solve a long incident once from scratch. The problem is not that it cannot solve it. The problem is that solving it again from scratch is wasteful.

And the useful diagnosis path is not generic common sense. It depends on current topology, service dependencies, alert patterns, monitoring instrumentation, and the actual deployed system. Those are external structures, not just model-internal knowledge.

So in that setting, procedural memory is not mainly about adding missing knowledge. It is about preserving reusable search paths, verification order, and boundary conditions, so that later incidents can be checked more efficiently.

A full industrial system would be too expensive to build for a study like this. So my current thought is to simulate diagnosis structure rather than operations business itself: a lighter graph-structured environment with hidden topology, tool-based queries, same symptom but different root causes, and slight environment drift.

That would let me test not whether the model can diagnose at all, but whether external procedural memory can reduce repeated search cost and still support selective reuse under changing environments.

So rather than asking only which AWM module to improve next, I would really like to ask three more upstream questions.

What part of procedural memory do you think will be internalized by stronger models, and what part will remain external?

If AWM’s current workflow text is only an intermediate form, what should the next memory object actually look like?

And if I could only do one next experiment, would this kind of lightweight diagnosis environment be a good way to test the independent value of external procedural memory?

### 中文提示

这页把问题落到一个可验证的实验方向。

重点不是：
`模型会不会做诊断`

而是：
`在模型已经能做单次诊断的前提下，external procedural memory 能不能减少重复搜索成本，并在环境变化下支持 selective reuse。`

哪些 procedural memory 会被 stronger models 吸收，哪些会长期外部化？
如果 AWM workflow text 只是中间形态，下一代 memory object 应该怎么定义？
如果只能做一个关键实验，这种轻量诊断环境是不是合理切入？

---

## Optional Closing Line

### English

Thank you. I’m happy to take questions.

### 中文提示

收尾就停，不要再补新信息。
