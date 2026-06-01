# Eval Results

保存 runner 真实输出（JSON）：每个 case 的 check 结果、失败列表、§5 指标。

## 已有

| 文件 | router 模式 | 结果 |
|---|---|---|
| `run_mocked_20260601T172114.json` | mocked oracle（可复现） | 100/100 结构 check 通过；critical bypass = 0；详见 [`../eval-prototype.md`](../eval-prototype.md) §9.1 |

## 口径

- 这些是 **prototype 结构性指标**，不是业务 KPI；不得写成客服时间下降 / CSAT / deflection。
- mocked oracle 模式不代表真实 router 准确率（含轻度过拟合风险）。真实意图结果来自
  `--router llm` 模式，跑完后写入新 JSON 并在 `eval-prototype.md` §9.2 追加一行。
- 复现：`cd ../../prototype && . .venv/bin/activate && python -m eval_runner.run_eval --write`。
