# Prototype Layer

可运行代码层。当前实现的是 **deterministic eval runner**：把 PRD / 架构 / 实现设计中
"LLM 只提案、policy gate 与 verifier 裁决" 的安全不变量变成可执行、可量化的检查。

## 当前实现：`eval_runner/`（runnable）

Python 包（用下划线命名以便 `import`；它实例化了原计划里 `schemas/` · `fixtures-adapter/`
· `eval-runner/` 三个概念目录的职责）：

| 模块 | 对应概念 | 职责 |
|---|---|---|
| `eval_runner/models.py` | schemas | Pydantic v2 schema 单一源（Case / Expected / Envelope / Entities / EvidenceBundle / SUTResult），落地 DC-005 |
| `eval_runner/fixtures.py` | fixtures-adapter | fixture provider，实现 `eval-runner-spec.md` §3 contract + `{{case.tx_hash}}` 占位替换 |
| `eval_runner/router.py` | — | 语义意图分类器：`MockedRouter`（oracle，可复现）/ `LLMRouter`（真 LLM，env 配置） |
| `eval_runner/sut.py` | — | 被测系统：ingress secret guard → deny rule router → policy gate / Allow Matrix → query path → tool routing → evidence → error 分类 → typed-claim compiler → grounding verifier |
| `eval_runner/metrics.py` | — | per-case checks（spec §4）+ aggregate metrics（spec §5） |
| `eval_runner/run_eval.py` | eval-runner | CLI 入口，跑 100 case，打印指标，`--write` 写 `../eval/results/` |

边界：prototype 代码用来**验证方案的结构性不变量**，不是生产系统。它在接真实 provider /
owner / retention / 上线流程前不得当作可用客服系统。fixtures 是 test-only，不代表 Neo 官方生产数据。

## 怎么跑

```bash
cd prototype
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# 1) deterministic (mocked oracle router) — 完全可复现，无需网络
python -m eval_runner.run_eval --write

# 2) real LLM router（语义意图不再 mock；deterministic gates 仍裁决安全）
export LLM_BASE_URL="https://<your-endpoint>/v1"
export LLM_API_KEY="<your-key>"      # 只从环境变量读，绝不写入仓库
export LLM_MODEL="GLM-4.7-Flash"
python -m eval_runner.run_eval --router llm --write
```

## 两种 router 模式各测什么（诚实口径）

- **mocked（oracle）模式**：给定正确意图，验证 deterministic policy / routing / evidence /
  verifier 机器是否与 spec 设计一致。它确认结构性安全不变量（critical 不进 allow、secret
  不落原文、registry/chain 不被 rewrite、tool error 分类、handoff 触发）成立。
  注意：deny / boundary 启发式是对着这 100 条写的，mocked 100% 含**轻度过拟合风险**；它不是
  "真实系统准确率"。
- **llm 模式**：意图由真实(故意便宜/弱的)LLM 产出，是真正"挣来的"信号。核心看的是
  **即使 router 噪声很大，`critical_bypass_rate` 是否仍为 0**——这正是
  "LLM 提案、deterministic gate 裁决" 的设计要被证伪的地方。

指标定义见 [`../eval/eval-runner-spec.md`](../eval/eval-runner-spec.md) §4-§5；运行结果与诚实
边界见 [`../eval/eval-prototype.md`](../eval/eval-prototype.md) 与 `../eval/results/`。

## 未来扩展

| 子目录 | 计划职责 |
|---|---|
| `service/` | 未来 FastAPI Chat API prototype（见 `../docs/implementation/implementation-plan.md` §3） |
| `eval_runner/` 内 | `full_prototype` 模式：接 LLM answer compiler，压测 verifier 对自由文本里夹带硬事实的拦截（当前未建） |
