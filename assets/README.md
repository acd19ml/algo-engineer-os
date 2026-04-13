# assets

`assets/` 是这个仓库存放共享静态资源的地方。

如果这个仓库同时包含文本、结构、脚本和派生产出，  
那么 `assets/` 保存的就是：**帮助这些内容被解释、被展示、被复用的静态支撑材料**。

这一层是仓库的共享静态资源层（shared static resource layer）。

---

## 这一层是做什么的

`assets/` 用于存放那些会被仓库多个页面或多个目录共同引用的静态文件。

Examples:

- figures
- diagrams
- screenshots
- icons
- small supporting media
- manually maintained images for README pages

这些文件帮助理解和展示，  
但它们本身不是 source knowledge nodes，也不是 generated outputs。

---

## 为什么这一层重要

如果没有共享资源目录，图片和图示很容易散落在各处。  
这通常会带来几个问题：

- path 不一致
- figure 很难复用
- 文件重复
- 更新时维护成本高
- 手工资源和生成产物边界模糊

`assets/` 的作用，就是把这些共享静态材料组织起来，让它们更稳定可复用。

---

## 什么内容主要属于这里

当一个文件主要是在充当 **static support resource** 时，它通常属于 `assets/`。

Examples:

- manually created architecture diagram
- a figure used in multiple README files
- a screenshot of a system view
- an icon set for navigation or presentation
- a reusable visual for a project overview

一个文件通常属于这里，当它满足这些特征：

- static
- manually curated
- 不是主内容对象本身
- 会在多个页面或目录中复用

---

## 什么内容不应首先放在这里

以下内容更适合先放到其它层：

- generated diagrams or auto-built graph outputs -> `OUTPUT/`
- raw source PDFs or paper attachments -> `RAW_SOURCES/`
- code -> external repos 或相关源码目录
- node content -> `KNOWLEDGE/`
- project execution artifacts -> `PROJECTS/`
- automation tools -> `SCRIPTS/`

最关键的区分是：

- `assets/` = shared static supporting materials
- `OUTPUT/` = generated artifacts

---

## 推荐子结构

简单结构通常就够用：

```text
assets/
├── README.md
├── figures/
├── screenshots/
├── diagrams/
└── icons/
```

不需要一开始就全部建全。  
先从 `figures/` 开始也完全可以。

---

## 常见资源类型

### `figures/`

用于可复用视觉解释。

Examples:

- method comparison figures
- architecture illustrations
- process diagrams
- system maps

---

### `screenshots/`

用于保存界面或重要状态的截图。

Examples:

- dashboard screenshots
- tool usage captures
- environment setup screenshots

---

### `diagrams/`

用于保存手工制作的结构图。

Examples:

- repository structure diagram
- knowledge graph sketch
- project architecture flow

---

### `icons/`

用于在展示层面提供少量视觉支撑。

只有在它们确实提高可读性时再使用，避免为了装饰而装饰。

---

## 设计原则

### 1. Keep assets reusable

如果同一张图会在多个地方引用，它大概率就应该放在这里。

### 2. Prefer clear naming

资源文件名应描述“它是什么”，而不是随手命名。

### 3. Separate static assets from generated artifacts

手工绘制图和脚本生成 DAG 不应混在一起。

### 4. Avoid clutter

不要长期保留随机的一次性文件，除非它真的有复用价值。

### 5. Support readability

这一层的核心目的是帮助解释与导航，而不是堆素材。

---

## 命名建议

推荐类似这样的名字：

- `knowledge-graph-overview.png`
- `rope-family-comparison.svg`
- `project-architecture-v1.png`
- `dashboard-current-focus.png`

避免这类模糊命名：

- `img1.png`
- `final2.png`
- `newnew.png`

清晰命名会显著降低后续维护摩擦。

---

## 这一层如何与其它层协作

### With `README.md` files

一些 assets 可以用于解释仓库结构、系统结构或关键概念。

### With `WIKI/`

wiki pages 常常会用到 summary visuals、diagrams 或 comparison figures。

### With `PROJECTS/`

project pages 可以引用 architecture diagrams 或 screenshots。

### With `WORK/`

playbooks 和 design notes 可以引用一些视觉辅助材料。

### With `DASHBOARDS/`

dashboard 文档可以用截图说明视图效果，  
但真正自动生成的 dashboard 文件仍应放在 `OUTPUT/`。

---

## 当前阶段的重点

`assets/` 的第一阶段建议优先：

- a small `figures/` directory
- clean naming
- repository-level shared visuals only
- avoiding duplication between static assets and generated outputs

---

## 相关入口

- [Root README](/Users/mac/studyspace/algo-engineer-os/README.md)
- [WIKI](/Users/mac/studyspace/algo-engineer-os/WIKI/README.md)
- [PROJECTS](/Users/mac/studyspace/algo-engineer-os/PROJECTS/README.md)
- [WORK](/Users/mac/studyspace/algo-engineer-os/WORK/README.md)
- [OUTPUT](/Users/mac/studyspace/algo-engineer-os/OUTPUT/README.md)
