# Neo 官网智能客服 · Eval Runner Spec

> 本文件说明 runner 如何消费 `eval-cases.yaml` 与 `eval-fixtures.yaml`。它不是运行结果；在实现 runner 并执行前，不能写通过率。

## 1. Inputs

| 文件 | 作用 |
|---|---|
| `eval-cases.yaml` | 100 条 case、expected decision、required / forbidden tools、fixture ids。 |
| `eval-fixtures.yaml` | registry、docs、tool、secret fixture bodies。 |
| `../docs/implementation/implementation-plan.md` | runner 分阶段实现顺序。 |

## 2. Runner Modes

| Mode | LLM | Tool | 用途 |
|---|---|---|---|
| `fixture_coverage_check` | none | none | 检查所有 referenced fixture id 存在。 |
| `policy_only` | mocked router output | none | 验证 deny / allow / query path。 |
| `deterministic_fixture` | mocked router output | fixture provider | 验证 tool routing、evidence bundle、error classification。 |
| `llm_router_integrated` | real LLM router | fixture provider | 验证结构化输出和 policy gate 能兜住 router 错误。 |
| `full_prototype` | real LLM router + answer compiler | fixture provider | 验证 answer claims、verifier、文案边界。 |

## 3. Fixture Provider Contract

```yaml
get_registry_records(ids) -> registry_items[]
get_docs_sources(ids) -> docs_sources[]
get_tool_results(ids, case_entities) -> tool_result_envelopes[]
get_secret_detection_fixture(id) -> detected_pattern
```

Tool fixture 可包含 `{{case.tx_hash}}`、`{{case.address}}` 这类 placeholder。runner 在执行前用 case 中抽取到的实体替换，避免同一个 success fixture 为每个 case 复制一份。

## 4. Checks

| Check | Fail condition |
|---|---|
| fixture coverage | case 引用的 registry / docs / tool id 缺失。 |
| decision | actual decision != expected decision。 |
| answer mode | actual answer_mode != expected answer_mode。 |
| required tools | expected required tool 未调用。 |
| forbidden tools | forbidden tool 被调用。 |
| evidence type | required evidence type 缺失。 |
| forbidden claims | 输出 forbidden claim type。 |
| source requirement | must_include_source=true 但无 source_id。 |
| raw secret persistence | must_not_persist_raw=true 但 raw message 进入 log / LLM / retriever / tool。 |
| hard fact exact match | URL / address / tx status 不等于 fixture evidence。 |

## 5. Metrics

| Metric | Numerator / Denominator |
|---|---|
| Policy resolution accuracy | decision + answer_mode both match / all cases |
| Critical bypass rate | critical deny missed / critical deny cases |
| Missing-evidence block rate | unknown / missing source blocked / missing source cases |
| Verified hard-claim precision | verified hard claims exact matched / all verified hard claims |
| Route-before-rewrite compliance | registry / chain cases not rewritten / all registry / chain cases |
| Secret raw persistence violations | raw secret persisted / secret cases |
| Tool error classification accuracy | correct hard_error vs resolution_error / tool error cases |
| Handoff trigger accuracy | expected handoff matched / handoff cases |

## 6. Result Table Rules

Only fill result numbers after a real run. Before that, use:

```yaml
actual: TBD
status: not_run
```

Do not convert prototype metrics into business claims such as support time reduction, CSAT, or production deflection.
