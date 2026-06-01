"""Model sweep: run the LLM-router eval across several models with ONE key set once.

No per-model `export LLM_MODEL` needed — the model is passed per run. This is the
router-capability ablation harness (vary the router, hold the deterministic harness fixed).

Usage (from prototype/, venv active):
    export LLM_BASE_URL="https://<your-endpoint>/v1"
    export LLM_API_KEY="<your-key>"
    python -m eval_runner.sweep                      # 4 Qwen2.5 sizes on the 100-set
    python -m eval_runner.sweep --suite both          # also run the T1 held-out set
    python -m eval_runner.sweep --models "Qwen2.5-7B-Instruct,Qwen2.5-72B-Instruct"

Writes eval/results/sweep_<ts>.json (raw) + sweep_<ts>.md (paste-ready comparison table).
The headline column to watch is critical_bypass — it must stay 0 across every model.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path

from .run_eval import _project_root, run

# the four sizes you swept; override with --models
DEFAULT_MODELS = [
    "Qwen2.5-7B-Instruct",
    "Qwen2.5-14B-Instruct",
    "Qwen2.5-32B-Instruct",
    "Qwen2.5-72B-Instruct",
]


def _heldout_path() -> Path:
    return _project_root() / "eval" / "eval-cases-heldout-t1.yaml"


def _row(model: str, suite: str, out: dict) -> dict:
    m = out["metrics"]
    return {
        "model": model,
        "suite": suite,
        "full_pass": out["cases_fully_passing"],
        "total": out["total_cases"],
        "policy_resolution": m["policy_resolution_accuracy"]["value"],
        "critical_bypass": m["critical_bypass_rate"]["value"],
        "missing_evidence_block": m["missing_evidence_block_rate"]["value"],
        "handoff": m["handoff_trigger_accuracy"]["value"],
        "tool_error": m["tool_error_classification_accuracy"]["value"],
        "llm_calls": out.get("router_calls"),
        "api_failed": out.get("router_errors"),
        "unparsed": out.get("router_unparsed"),
        "failures": out.get("failures", []),
    }


def _md_table(rows: list[dict], errors: list[dict]) -> str:
    hdr = (
        "| model | suite | pass | policy_res | **critical_bypass** | miss_ev_block | handoff | tool_err | unparsed | api_fail |\n"
        "|---|---|---:|---:|:---:|---:|---:|---:|---:|---:|"
    )
    lines = [hdr]
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['suite']} | {r['full_pass']}/{r['total']} | {r['policy_resolution']} | "
            f"{r['critical_bypass']} | {r['missing_evidence_block']} | {r['handoff']} | {r['tool_error']} | "
            f"{r['unparsed']} | {r['api_failed']} |"
        )
    out = "\n".join(lines)
    if errors:
        out += "\n\n跳过(运行出错):\n" + "\n".join(f"- {e['model']}/{e['suite']}: {e['error']}" for e in errors)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="LLM-router model sweep (router-capability ablation)")
    ap.add_argument("--models", default=None, help="comma-separated; default = 4 Qwen2.5 sizes")
    ap.add_argument("--suite", choices=["main", "heldout", "both"], default="main")
    args = ap.parse_args()

    if not os.environ.get("LLM_BASE_URL") or not os.environ.get("LLM_API_KEY"):
        print("[setup] set LLM_BASE_URL and LLM_API_KEY once, then re-run.\n"
              "  export LLM_BASE_URL=...  LLM_API_KEY=...")
        raise SystemExit(1)

    models = [s.strip() for s in args.models.split(",")] if args.models else DEFAULT_MODELS
    suites: list[tuple[str, Path | None]] = []
    if args.suite in ("main", "both"):
        suites.append(("main", None))
    if args.suite in ("heldout", "both"):
        suites.append(("heldout_t1", _heldout_path()))

    rows: list[dict] = []
    errors: list[dict] = []
    for model in models:
        for sname, cp in suites:
            print(f"… {model} on {sname} (LLM calls, ~1-3 min) …", flush=True)
            try:
                out = run("llm", cp, model=model)
            except Exception as e:  # one bad model shouldn't kill the whole sweep
                print(f"  [skip] {model}/{sname}: {e}")
                errors.append({"model": model, "suite": sname, "error": str(e)})
                continue
            r = _row(model, sname, out)
            rows.append(r)
            print(f"  pass {r['full_pass']}/{r['total']} | policy {r['policy_resolution']} | "
                  f"critical_bypass {r['critical_bypass']} | unparsed {r['unparsed']} | api_fail {r['api_failed']}")

    md = _md_table(rows, errors)
    print("\n" + md)

    results = _project_root() / "eval" / "results"
    results.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    (results / f"sweep_{ts}.json").write_text(
        json.dumps({"rows": rows, "errors": errors}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (results / f"sweep_{ts}.md").write_text(md + "\n", encoding="utf-8")
    print(f"\nwrote eval/results/sweep_{ts}.json + sweep_{ts}.md")


if __name__ == "__main__":
    main()
