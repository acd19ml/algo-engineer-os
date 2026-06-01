# Semantic Typed Schema Fields

`status: candidate`   `instantiates-to: project-design-commitment`

## 何时打开

当你设计工具的参数 schema，且参数中包含路径 / URL / 命令字符串等语义敏感字段（这些字段在不同上下文中有特定格式约束，不允许富文本装饰），先打开这条。

不适用：所有参数都是无语义约束的通用字符串（如 summary、description 等自由文本字段）。

## 结构性不变量

工具参数 schema 中语义敏感字段（文件路径 / URL / 命令字符串 / 标识符等）不得使用通用 `string` 类型加 description 描述来隐式约束格式，而必须使用语义化类型标注（如 `path-string`、`url`、`command`）或在 schema 层显式声明格式不变量；语义化类型声明覆盖所有同类字段，一次改动全面生效。

## 它预防的症状簇

- P-038：LLM 输出 Markdown 格式路径 / URL，污染工具的文件系统操作 → 在 schema 层声明字段为 `path-string` 类型，并在 description 里明确"不要添加 Markdown 格式化"，模型的聊天分布在工具调用边界被结构性约束；比正则修复更根本（修复是事后，类型约束是事前）。

## 留在 runbook 的部分

- P-038 方案 1 局部正则处理（识别 `[text](url)` 提取路径）：这是在类型约束未建立之前的运行时兜底，或在修复层对漏网之鱼的补救，属于运行时恢复，留在 runbook。

## 代价 / 范围

- 代价：需要为每类语义敏感字段定义对应的语义化类型；如果工具框架不支持自定义类型，需要在 description 中做等价声明（效果略弱）；维护类型定义本身需要持续投入。
- 适用：任何工具参数包含文件路径 / URL / 命令字符串 / 数据库表名等语义敏感字段的场景。
- 失效：参数字段本来就是自由文本（summary / description / content 等生成型字段），语义化类型约束不适用且可能限制输出质量（见 [[reasoning-output-decoupling]]）。

## 实例化成项目 DC 时要补的校验

- 架构：工具 schema 中存在语义化类型定义库（如 `PathString = string with pattern '^[^[]]*$'`）；所有工具注册时对路径 / URL / 命令类字段使用对应语义类型而非通用 `string`。
- 静态检查：扫描所有工具 schema，找出参数名包含 `path` / `url` / `file` / `dir` / `command` / `cmd` 等关键词但类型为通用 `string` 的字段，标记为待改写。
- eval：构造"模型用 Markdown 链接格式填写路径参数"的测试用例，验证工具校验层检测到格式违规（而非静默接受非法路径）。
- 人工 review TODO：新增工具时，代码评审检查所有参数字段，语义敏感字段必须使用对应语义类型或有明确格式约束声明。

## 前沿问题

- 语义化类型的粒度如何确定？`path-string` 是一个类型，还是 `absolute-path` / `relative-path` / `glob-pattern` 各是一个类型？过细可能维护成本过高。
- 随着模型能力提升，训练分布泄露（Markdown 在工具场景中漏出）会减少吗？这个 pattern 会在什么时候退役？
- 工具框架层（如 OpenAI Function Calling / Anthropic Tool Use）对自定义语义类型的支持度如何？在框架限制下，description 声明能达到语义类型的等价效果吗？

## 源

`[[tool-call-repair-harness]]` + P-038（schema 语义化类型作为训练分布泄露的结构层修复；`path-string` vs 通用 `string` 的对比）。

验证状态：未验证（外部 claim）。

## 演进日志

- `2026-05`：从 P-038 schema 结构层修复方案抽出不变量，提炼为通用的"语义敏感字段必须语义化类型约束"原则。P-038 局部正则修复明确留在 runbook。
