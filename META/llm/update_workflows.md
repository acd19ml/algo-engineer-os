# LLM Update Workflows

这个文档定义 LLM 辅助维护时常见的更新工作流。

目标是让那些反复出现的仓库更新更一致、更安全，也更容易 review。

这些 workflow 应与以下文件一起使用：

- `system_prompt.md`
- `editing_rules.md`
- `META/policies/` 下的仓库规则

---

## Workflow A: 新建 knowledge node

### Trigger

当识别出一个值得长期复用的新主题，需要为它建立 node。

### Inputs

- topic name
- broad domain 或目标目录位置
- 已知 prerequisites、related problems、related projects
- 任何可用 raw sources

### Steps

1. 先检查是否已经存在等价 node。
2. 确认这个对象确实是 node，而不是：
   - problem page
   - wiki synthesis
   - project page
   - work playbook
3. 创建标准 node 结构：
   - `README.md`
   - `meta.yaml`
   - `math/README.md`
   - `code/README.md`
   - `refs/README.md`
   - `thoughts/README.md`
4. 使用 node template 起草页面。
5. 补上初始链接到：
   - prerequisites
   - related problems
   - related nodes
   - known external repos
6. 对尚未完成的部分明确标注，不要假装完整。

### Output

一个结构正确、后续容易继续完善的 first-pass node。

---

## Workflow B: 新增 raw source

### Trigger

当新的 paper、document、note 或 source 被加入 `RAW_SOURCES/`。

重复执行这个流程时，可直接使用：

- `META/templates/paper_ingestion_prompt.template.md`

### Inputs

- source content
- source location
- 可能相关的 nodes 或 problems

### Steps

1. 把 source 放到 `RAW_SOURCES/` 下合适的子目录。
2. 识别它相关的：
   - knowledge nodes
   - problem pages
   - project pages
   - wiki pages
3. 更新相关 node 的 `refs/README.md`。
4. 如果它改变了某个 problem space 的理解，更新对应 problem page。
5. 如果它明显影响某个 synthesis page，更新或标记相关 wiki page。
6. 如果它带来 ambiguity 或 contradiction，不要静默处理，应该增加 caveat。

### Output

新的 source 被接入系统，而不是孤立地躺在原始资料层。

---

## Workflow C: 用新理解更新 knowledge node

### Trigger

当一个现有 node 因为学习、阅读、编码或比较，需要被改进。

### Inputs

- the node
- updated understanding
- supporting sources 或 repos

### Steps

1. 先判断应该改哪个文件：
   - conceptual explanation -> `README.md`
   - structure or dependency -> `meta.yaml`
   - formulas -> `math/README.md`
   - implementation -> `code/README.md`
   - references -> `refs/README.md`
   - personal judgment -> `thoughts/README.md`
2. 尽量做局部增量更新。
3. 除非确实必要，不要整页重写。
4. 保持以下区分：
   - fact
   - summary
   - personal interpretation
5. 只有在 synthesis 确实受到实质影响时，才更新相关 wiki page。

### Output

一个更准确的 node，同时避免不必要的 churn。

---

## Workflow D: 新建或更新 problem page

### Trigger

当一个反复出现的 challenge、bottleneck 或 comparison space 需要被正式表述。

### Inputs

- problem statement
- known candidate solutions
- related nodes、projects、work situations

### Steps

1. 先检查 `PROBLEMS/` 下是否已存在该问题。
2. 确认这个对象本质上是 problem，而不是 topic node。
3. 使用 problem template 起草页面。
4. 至少写清：
   - problem definition
   - why it matters
   - failure modes
   - candidate solutions
   - comparison dimensions
   - related nodes
   - open questions
5. 链接相关 nodes 和 projects。
6. 如果比较还不完整，要保留 uncertainty。

### Output

一个以问题为中心的可复用页面，用来把方法组织回 challenge space。

---

## Workflow E: 新建或更新 wiki page

### Trigger

当为了 readability、overview 或 comparison，需要做 cross-node synthesis。

### Inputs

- lower-level pages
- related nodes、problems、projects 或 career materials

### Steps

1. 确认目标页面确实属于 `WIKI/`，而不是 `KNOWLEDGE/` 或 `PROBLEMS/`。
2. 检查是否已有 wiki page 覆盖相同 scope。
3. 使用 wiki page template。
4. 补齐 frontmatter：
   - `title`
   - `page_type`
   - `compiled_from`
   - `last_compiled_at`
   - `confidence`
5. 基于 lower-level materials 做 synthesis。
6. 通过链接回 nodes 和 problems 来保留 traceability。
7. 当 confidence 是 mixed 或 evidence 不完整时，明确写 caveats。

### Output

一个更易读的 compiled page，用于改善导航和理解，但不替代 source truth。

---

## Workflow F: 注册新的 external repo

### Trigger

当新的 external repo 被创建或被纳入系统。

### Inputs

- repo URL
- linked node(s)
- linked project(s)
- repo purpose
- repo type
- environment notes
- status

### Steps

1. 把 repo 加入 `REPRO_INDEX/external-repos.md`。
2. 从相关 node 的 `code/README.md` 链接它。
3. 如果相关，也从 project page 链接它。
4. 如果维护了 `reproduction-status.md`，同步更新。
5. 如果该 repo 明显改变了实现层 confidence，也在相关 node 中注明。

### Output

external repo 成为系统的一部分，而不是孤立资产。

---

## Workflow G: 把项目转成 career assets

### Trigger

当一个项目已经有足够内容，可以转成 career story、resume bullet 或 interview asset。

### Inputs

- project page
- key decisions
- results
- your specific contributions

### Steps

1. 识别项目中最强的 signals：
   - technical depth
   - decision-making
   - execution
   - debugging
   - ownership
   - communication
2. 在 `CAREER/stories/` 中创建或更新对应 story page。
3. 把相关内容转成：
   - resume bullets
   - interview versions
   - target-role fit
4. 回链到：
   - project page
   - knowledge nodes
   - work assets（如果相关）

### Output

技术工作被转成了职业 leverage。

---

## Workflow H: 把 reflection 升级成更正式的页面

### Trigger

当 `THINKING/` 中的一页已经足够成熟，值得升级成更正式的对象。

### Inputs

- reflection page
- supporting sources 或 repeated evidence

### Steps

1. 判断这页 reflection 更适合变成：
   - knowledge node
   - problem page
   - project
   - work playbook
   - wiki page
2. 创建新的正式页面。
3. 只迁移属于新层的内容。
4. 如果原 reflection 仍有价值，就继续保留它作为 cognitive history。
5. 显式地把两者链接起来。

### Output

系统以更 disciplined 的方式增长，同时保留推理历史。

---

## Workflow I: 处理或暴露冲突

### Trigger

当两层或两个页面之间出现明显冲突。

### Inputs

- conflicting pages or claims

### Steps

1. 先检查 source-of-truth priority。
2. 判断冲突属于：
   - structural
   - factual
   - interpretive
   - due to staleness
3. 如果能用 lower-layer truth 解决，就更新 higher layer。
4. 如果不能干净解决，就显式加入 caveat。
5. 需要时，标记 human review。

### Output

冲突被暴露和管理，而不是被隐藏。

---

## 总结

这些 workflows 的存在，是为了让维护过程更：

- consistent
- layered
- reviewable
- reusable

这个仓库不应只靠 ad hoc edits 演化。  
它应通过可重复、可理解的维护模式逐步变好。
