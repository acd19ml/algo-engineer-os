# Agent Runbook

症状导向的 agent 故障排查手册。读者带着"我看到了什么问题"来查，每条给出可立即操作的下一步。结构接近 SRE runbook，不是教科书也不是设计文档。

三个工作时刻：

- debug 时（反应）：ctrl-F 症状 → 按条目动作走。
- 面试 / 自测（反应，无安全网）：合上答案，照症状产出动作。
- 设计时（预防）：runbook 只提供压缩信号；真正使用的是 design commitment patterns / project commitments 的决策索引。

和 KNOWLEDGE 节点的区别：节点是"概念为什么这样"（自含因果叙述，密度在这里）；runbook 条目是"看到 X 下一步做什么"（薄：动作 + 回链）。因果的"为什么"只在节点里一份，runbook 不复述。

层边界：KNOWLEDGE 节点之间的关系（节点交叉、横向对比、按主题归类）是 KB 层的事，不在这里。本 README 只管两件事：条目怎么从节点 / debug 经验长出来；一簇条目什么时候沉淀成 design commitment pattern。

---

## 怎么用

1. ctrl-F 症状关键词（或下面索引）。
2. 命中后先看 `type`：
   - `remedy-menu` → 方案按期望解决成本排序，可跳着试，最先该试的在前。
   - `diagnostic-procedure` → 按顺序走，不许跳步；跳步会把上游故障伪装成下游故障。
3. 再看 `severity`：`irreversible` 的条目，第一步永远是先止血（断权限 / 回滚 / 硬中断）再诊断。
4. 看"适用与失效"判断是否真适用你的场景。
5. 试完后，如果验证状态还是"未验证"，回来更新。

---

## 文件组织

超过 30 条后已按 agent 生命周期拆子目录：

```text
WORK/runbooks/agent/
├── README.md               本文件
├── perception/runbook.md   感知 / 信息获取层（P-019, P-039）
├── planning/runbook.md     规划 / 任务分解层（P-013, P-029, P-035, P-042）
├── tool-use/runbook.md     工具调用层（P-001~P-005, P-008~P-012, P-017~P-018, P-020~P-021, P-037~P-038）
├── context/runbook.md      上下文管理层（P-006, P-014~P-015, P-026）
├── execution/runbook.md    执行控制层（P-007, P-016, P-027~P-028, P-030~P-034）
├── memory/runbook.md       记忆层（P-040~P-041）
└── reliability/runbook.md  可靠性 / 安全层（P-022~P-025, P-036）
```

**P-XXX 编号全局单调递增，不按子目录重置**。子目录拆分时只改 README 里的链接路径，DC pattern 里的 P-XXX 引用不需要改。

---

## 索引（按 P-编号排序）

| ID | 症状关键词 | type | severity | 子目录 |
|---|---|---|---|---|
| [P-001](./tool-use/runbook.md#p-001模型该调工具时输出了自由文本) | 该调工具时输出自由文本（格式错，意图对） | remedy-menu | reversible-cheap | tool-use |
| [P-002](./tool-use/runbook.md#p-002模型调用了不存在的工具) | 调用了不存在的工具（工具名幻觉） | remedy-menu | reversible-cheap | tool-use |
| [P-003](./tool-use/runbook.md#p-003模型跳过必要的中间步骤) | 跳过必要的中间步骤直接调终端工具 | remedy-menu | reversible-cheap | tool-use |
| [P-004](./tool-use/runbook.md#p-004工具错误计数混淆系统过早放弃) | 工具错误计数混淆，系统过早放弃 | remedy-menu | reversible-cheap | tool-use |
| [P-005](./tool-use/runbook.md#p-005怀疑本地模型工具调用能力差下结论之前) | 怀疑本地模型工具调用能力差（先排后端） | diagnostic-procedure | reversible-cheap | tool-use |
| [P-006](./context/runbook.md#p-006多步工作流上下文膨胀速度骤降或-oom) | 多步工作流上下文膨胀，速度骤降 / OOM | remedy-menu | reversible-cheap | context |
| [P-007](./execution/runbook.md#p-007纠正循环无限重试) | 纠正循环无限重试 | remedy-menu | reversible-cheap | execution |
| [P-008](./tool-use/runbook.md#p-008模型在调工具和输出文本之间频繁选错) | 模型在"调工具"和"输出文本"之间频繁选错 | remedy-menu | reversible-cheap | tool-use |
| [P-009](./tool-use/runbook.md#p-009json-输出格式不稳多逗号--加前缀--类型错) | JSON 输出格式不稳（语法层，parse 失败） | remedy-menu | reversible-cheap | tool-use |
| [P-010](./tool-use/runbook.md#p-010开启-strict--约束解码后输出语义质量下降) | 开启 strict 后输出语义质量下降 | remedy-menu | reversible-cheap | tool-use |
| [P-011](./tool-use/runbook.md#p-011json-语法对但值不合理语义错误) | JSON 语法对但值不合理（语义层） | remedy-menu | reversible-cheap | tool-use |
| [P-012](./tool-use/runbook.md#p-012工具集合大模型频繁选错想动态增删但会废-kv-cache) | 工具多模型选错；想动态增删但会废 KV cache | remedy-menu | reversible-cheap | tool-use |
| [P-013](./planning/runbook.md#p-013agent-跑几十步后开始机械重复之前的动作) | Agent 长任务后机械重复动作（模式锁定） | remedy-menu | reversible-cheap | planning |
| [P-014](./context/runbook.md#p-014使用前缀缓存-api-但命中率低月账单暴涨) | 前缀缓存 API 命中率低，API 成本暴涨 | remedy-menu | reversible-cheap | context |
| [P-015](./context/runbook.md#p-015做了上下文压缩反而让缓存命中率下降) | 做了上下文压缩反而让缓存命中率下降 | remedy-menu | reversible-cheap | context |
| [P-016](./execution/runbook.md#p-016agent-反复调用相同工具同参数行为卡住) | Agent 反复调用同工具+同参数，行为卡住 | remedy-menu | reversible-cheap | execution |
| [P-017](./tool-use/runbook.md#p-017工具参数-schema-嵌套深--叶子多模型频繁丢参数) | 工具参数 schema 嵌套深 / 字段多，模型丢参数 | remedy-menu | reversible-cheap | tool-use |
| [P-018](./tool-use/runbook.md#p-018模型输出-json-被截断工具层静默用空对象执行) | 模型输出 JSON 被截断，工具静默用空对象 | remedy-menu | reversible-cheap | tool-use |
| [P-019](./perception/runbook.md#p-019rag-回答不准不知道是哪一环坏了) | RAG 回答不准，不知道是哪一环坏了 | diagnostic-procedure | reversible-cheap | perception |
| [P-020](./tool-use/runbook.md#p-020给了-agent-万能工具后专用工具被弃用) | 给了万能工具后专用工具被弃用 | remedy-menu | reversible-cheap | tool-use |
| [P-021](./tool-use/runbook.md#p-021单次工具调用输出一次撑爆上下文窗口) | 单次工具调用输出一次撑爆上下文窗口 | remedy-menu | reversible-cheap | tool-use |
| [P-022](./reliability/runbook.md#p-022agent-做了超出指令范围的事--确认框疲劳无脑点击) | Agent 做超出范围的事 / 确认框疲劳 | remedy-menu | irreversible | reliability |
| [P-023](./reliability/runbook.md#p-023agent-自己审查自己被自我辩护绕过) | Agent 自己审查自己，被自我辩护绕过 | remedy-menu | irreversible | reliability |
| [P-024](./reliability/runbook.md#p-024安全规则写在-prompt-里模型版本一变就失效) | 安全规则写在 prompt 里，换模型就失效 | remedy-menu | irreversible | reliability |
| [P-025](./reliability/runbook.md#p-025最高信任模式下安全底线如-zshrc被破) | 高信任模式下安全底线（如 .zshrc）被破 | remedy-menu | irreversible | reliability |
| [P-026](./context/runbook.md#p-026上下文压缩连续失败系统不停重试浪费-api-调用) | 上下文压缩连续失败，系统不停重试浪费 API 调用 | remedy-menu | reversible-cheap | context |
| [P-027](./execution/runbook.md#p-027agent-在长任务执行中途提前放弃--草草收工) | Agent 在长任务执行中途提前放弃 / 草草收工 | remedy-menu | reversible-cheap | execution |
| [P-028](./execution/runbook.md#p-028评审者宽容--llm-评估偏向表扬生成结果) | 评审者宽容 / LLM 评估偏向表扬生成结果 | remedy-menu | reversible-cheap | execution |
| [P-029](./planning/runbook.md#p-029agent-做任务时顺手做了范围外的事角色越界) | Agent 做任务时"顺手"做了范围外的事（角色越界） | remedy-menu | reversible-cheap | planning |
| [P-030](./execution/runbook.md#p-030system-prompt-里的规则太模糊agent-执行时不遵守) | System prompt 里的规则太模糊，agent 执行时不遵守 | remedy-menu | reversible-cheap | execution |
| [P-031](./execution/runbook.md#p-031agent-报告结果时夸大成功或掩盖失败) | Agent 报告结果时夸大成功或掩盖失败 | remedy-menu | reversible-cheap | execution |
| [P-032](./execution/runbook.md#p-032agent-对同一文件反复编辑但问题没有解决) | Agent 对同一文件反复编辑但问题没有解决 | remedy-menu | reversible-cheap | execution |
| [P-033](./execution/runbook.md#p-033agent-在任务完成前跳过验证直接输出) | Agent 在任务完成前跳过验证直接输出 | remedy-menu | reversible-cheap | execution |
| [P-034](./execution/runbook.md#p-034claudemd--agentsmd-过长agent-合规率急剧下降) | CLAUDE.md / AGENTS.md 过长，agent 合规率急剧下降 | remedy-menu | reversible-cheap | execution |
| [P-035](./planning/runbook.md#p-035给子-agent-下达模糊任务指令多个子-agent-做了相同的事) | 给子 agent 下达模糊任务指令，多个子 agent 做了相同的事 | remedy-menu | reversible-cheap | planning |
| [P-036](./reliability/runbook.md#p-036多个-agent-并行写入共享状态导致工具冲突和状态损坏) | 多个 agent 并行写入共享状态，导致工具冲突和状态损坏 | remedy-menu | irreversible | reliability |
| [P-037](./tool-use/runbook.md#p-037校验前对工具输入预处理静默损坏合法输入) | 校验前对工具输入预处理，静默损坏合法输入 | remedy-menu | reversible-cheap | tool-use |
| [P-038](./tool-use/runbook.md#p-038llm-输出-markdown-格式路径--url污染工具的文件系统操作) | LLM 输出 Markdown 格式路径 / URL，污染工具的文件系统操作 | remedy-menu | reversible-cheap | tool-use |
| [P-039](./perception/runbook.md#p-039query-改写后检索效果反而下降) | Query 改写后检索效果反而下降 | remedy-menu | reversible-cheap | perception |
| [P-040](./memory/runbook.md#p-040过时记忆被当作当前事实权威引用) | 过时记忆被当作当前事实权威引用 | remedy-menu | reversible-cheap | memory |
| [P-041](./memory/runbook.md#p-041skillssop-未维护导致过时流程被执行) | Skills/SOP 未维护导致过时流程被执行 | remedy-menu | reversible-cheap | memory |
| [P-042](./planning/runbook.md#p-042planning-cache-命中了错误模板执行了错误的检索路径) | Planning cache 命中了错误模板，执行了错误的检索路径 | remedy-menu | reversible-cheap | planning |

> 当前 42 条来源：
> - P-001 ~ P-008：`[[small-model-harness-engineering]]`（小模型工具调用故障域）
> - P-009 ~ P-013：`[[structured-output]]`（结构化输出 6 层）
> - P-014 ~ P-018：`[[cache-aware-agent-loop]]`（前缀缓存命中率作为成本杠杆）
> - P-019：`[[rag-failure-diagnosis]]`（RAG 5 步诊断流）
> - P-020 / P-021：`[[agent-tool-design]]`（工具设计三原则）
> - P-022 ~ P-025：`[[agent-permission-system]]`（分层规则 + 两阶段评审）
> - P-026：`[[agent-context-compaction]]`（四层压缩流水线 + 熔断器）
> - P-027 / P-028：`[[harness-practice]]`（GAN 三 agent 系统 + 上下文焦虑 + 自我表扬）
> - P-029：`[[agent-role-isolation]]`（按阶段拆 agent + 三维隔离）
> - P-030 / P-031：`[[agent-system-prompt]]`（模块化 + 具体规则 + 防虚假声明）
> - P-032 / P-033：`[[harness]]`（中间件钩子 + 推理三明治）
> - P-034：`[[claude-md-rule-design]]`（12 条规则 + 200 行天花板）
> - P-035：`[[multi-agent]]`（任务委派四要素 + 缩放规则）
> - P-036：`[[multi-agent]]`（序列化执行 + 独立工作空间）
> - P-037 / P-038：`[[tool-call-repair-harness]]`（先校验再修复 + 语义化类型）
> - P-039：`[[rag-query-rewriting]]`（路由先于改写 + 业务术语注入）
> - P-040：`[[agent-memory-system]]`（过期警告 + 时效标注）
> - P-041：`[[agent-skills-closed-loop]]`（Hermes Skills 即时维护机制）
> - P-042：`[[agentic-rag-planning-cache]]`（模板误命中检测）
>
> 验证状态全部为"未验证"——外部 claim，未在本地复现。回来查到任何一条并实操过，记得更新验证状态。
>
> 方案互冲提示保留：P-006 vs P-014/P-015 在"上下文压缩"上的方案相反。本地推理 / 关心 OOM 走 P-006；云 API / 关心缓存成本走 P-014+P-015，条目内互链。

---

## 条目怎么从节点长出来（node → runbook）

这是一个抽走密度的纵向投影：节点（密集、概念索引）→ 条目（稀疏、症状索引）。只有动作往下走，"为什么"留在节点、条目回链。

方向不是一一对应：

- 一个密集节点可派生多条症状条目（一个机制以几种不同现象暴露）。
- 多个节点可喂同一条症状条目（一个症状的成因 / 修法横跨几个概念）。

出生闸门：从节点得到一条候选洞见时，先查症状索引。

- 已有症状命中 → append：menu 加一个方案后重排当前方案；procedure 加一关后插入正确拓扑位置；演进日志加一行。
- 没命中 → 才新建条目。

去重 key 是症状，不是来源节点。条目会慢慢长出来：新节点触及同一症状、真实 debug 经验验证或替换旧方案，都会让条目更新。

---

## 写新条目

模板：[`META/templates/runbook_entry.template.md`](../../../META/templates/runbook_entry.template.md)。写之前先回答两个先决判断：`type` 和 `severity`。

字段：5 必填（症状 / 根因 / 当前方案 / 适用与失效 / 源）+ 3 可选（前置条件 / 演进日志 / See also）+ 2 条目头声明（type / severity）。

症状字段按"我会用什么关键词搜"反向写。症状写不到位，三个月后翻不出来。

薄判据：删掉条目里所有"为什么"句子后，每一步还能照做吗？能 → 厚度合适；不能 → 你把节点内容塞进 runbook 了。

---

## 维护节奏

跑两周看你是否真回来查。

- 不回来查 → 几乎一定是症状字段没写到位，回来改。
- 真查到并实操过 → 更新验证状态和演进日志。

不强求覆盖率。一条没用过的条目 = 一条会过时的条目。

---

## 出口：沉淀 design commitment pattern

runbook 是反应式、症状索引。设计时没有症状，用不上它；设计时先用 `WORK/design-commitment-patterns/`，项目采纳后再实例化成项目内 design commitments。

先把条目里的修法分两类：

- 运行时恢复 / 一段过程：症状照常发生，事后补救或定位。留在 runbook。
- 结构性不变量：让该类症状，或它的有害后果，从设计上不可能发生。才是候选 design commitment pattern。

同一条目里可能两者并存。只把不变量升级，过程继续留在 runbook。节点的 thesis（"为什么"）不作为承诺，它不可校验，留在 KNOWLEDGE。

升级信号：

1. 同一条结构性不变量同时使多个症状不可能发生 → 创建 / 更新 `WORK/design-commitment-patterns/*`。
2. 一个方案在同一时段成为多条条目的新首选 → 先判定它是恢复过程还是不变量；只有不变量才进入 pattern。
3. 条目里出现"上线后持续监控 X / 设计时应该 Y"这类前瞻预防内容 → 指向 pattern，正文别展开。

当前 pattern：[`WORK/design-commitment-patterns/agent/`](../../design-commitment-patterns/agent/)

---

## 引用方向

- runbook 条目 → KNOWLEDGE 节点：单向，在"根因 / 源 / See also"里。
- KNOWLEDGE 节点不感知 runbook。
- runbook 簇 → design commitment pattern：单向。
- pattern → project design commitment：项目采纳时实例化。
- project design commitment 实例不住在 WORK，住项目 ledger。
- 用户编辑 = ground truth。
