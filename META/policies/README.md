# Policies

这个目录存放仓库级 policies，用来定义系统应如何长期保持稳定、一致和值得信任。

如果 templates 负责定义“页面长什么样”，  
那么 policies 负责定义“整个仓库应如何被治理”。

---

## 这个目录是做什么的

`META/policies/` 用于保存稳定的、仓库级的规则，例如：

- truth hierarchy
- naming
- node size and boundaries
- consistency expectations
- long-term repository behavior

这些规则的目标，是在仓库不断增长时减少 drift。

---

## 为什么 policies 重要

随着知识系统变大，依赖“口头习惯”会越来越脆弱。

没有明确 policy，通常会出现：

- naming chaos
- page boundary 不一致
- duplication
- accidental truth drift
- review standard 不清楚

policies 的作用，就是让这个系统在时间拉长后仍然 legible。

---

## 当前核心 policies

### `source_of_truth.md`

定义当信息冲突时，哪些层是 authoritative 的。

### `naming_convention.md`

定义 files、directories、nodes、problem pages、projects 和 assets 的命名规则。

### `node_granularity.md`

定义 knowledge node 应该拆多宽、合多窄。

---

## 设计原则

### 1. Policy 应尽量稳定

policy 不应随意频繁改变。

### 2. Policy 应降低歧义

一个好的 policy 应让未来决策更容易，而不是更模糊。

### 3. Policy 应务实

policy 的目标是让仓库更可用，而不是更 ceremonial。

### 4. Policy 应服务长期维护

仓库应随着时间变得更 coherent，而不是更混乱。

### 5. Policy 应支持 LLM-assisted maintenance

只有当仓库行为足够明确时，LLM 才能安全协助。

---

## 如何使用 policies

当你新增或修改内容时，可以用 policies 来回答这些问题：

- 这个对象该放哪里
- 它应该叫什么
- 这是一个 node，还是太小 / 太大
- 当两个页面冲突时，哪一层优先

policies 在这些场景尤其重要：

- splitting or merging nodes
- creating new page types
- renaming objects
- reviewing LLM-generated updates

---

## 相关入口

- [Meta](../README.md)
- [Templates](../templates/README.md)
- [LLM Rules](../llm/README.md)
