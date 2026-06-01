# Eval Layer

本目录放评测设计、cases、fixtures、runner spec 和未来执行结果。

| 文件 / 目录 | 职责 |
|---|---|
| `eval-prototype.md` | 指标、suite、未运行 / 已运行口径。 |
| `eval-cases.yaml` | 100 条 prototype cases。 |
| `eval-cases-heldout-t1.yaml` | T1 留出集（未参与调参，验证泛化）。 |
| `eval-fixtures.yaml` | registry / docs / tool / secret fixture bodies。 |
| `eval-runner-spec.md` | runner mode、checks、metrics。 |
| `harness-kb-alignment.md` | eval harness 与 KNOWLEDGE pattern 对齐记录。 |
| `decision-trail-full.md` | M0-M13 全周期设计决策链（工业级交付路线图）。 |
| `decision-trail-d5-hardening.md` | D5 短语检测硬化决策链（sweep → playbook）。 |
| `results/` | 未来保存真实 runner 输出和失败分析。 |

边界：这里的 fixture 不是 production source，不代表真实用户日志。
