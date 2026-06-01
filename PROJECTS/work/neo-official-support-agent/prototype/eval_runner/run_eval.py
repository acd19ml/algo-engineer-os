"""CLI: run the 100-case eval suite against the deterministic SUT.

Usage (from prototype/, with the venv active):
    python -m eval_runner.run_eval                 # mocked oracle router (reproducible)
    python -m eval_runner.run_eval --router llm     # real LLM router (needs LLM_* env vars)
    python -m eval_runner.run_eval --write          # also write JSON to ../eval/results/

The mocked run is fully deterministic and needs no network. The llm run exercises the real
semantic router; the deterministic gates still decide safety, so the headline check is that
critical_bypass_rate stays 0 even when the router is noisy.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from collections import Counter
from pathlib import Path

import yaml

from .fixtures import FixtureProvider
from .metrics import aggregate_metrics, check_case
from .models import Case
from .router import LLMRouter, MockedRouter
from .sut import SupportOrchestratorSUT


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_cases(cases_path: Path | None = None) -> list[Case]:
    path = cases_path or (_project_root() / "eval" / "eval-cases.yaml")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [Case(**c) for c in raw["cases"]]


def run(router_kind: str, cases_path: Path | None = None, model: str | None = None) -> dict:
    provider = FixtureProvider()
    cases = load_cases(cases_path)
    sut = SupportOrchestratorSUT(provider)
    sut.router = LLMRouter(model=model) if router_kind == "llm" else MockedRouter()

    suts = {}
    reports = []
    for case in cases:
        result = sut.run(case)
        suts[case.id] = result
        reports.append(check_case(case, result, provider))

    metrics = aggregate_metrics(cases, suts, provider)

    # per-check pass counts
    check_names = list(reports[0].checks.keys())
    check_pass = {name: sum(1 for r in reports if r.checks.get(name)) for name in check_names}

    failures = [
        {"case_id": r.case_id, "suite": r.suite, "failed": r.failures(),
         "sut": {"decision": r.sut.decision.value, "answer_mode": r.sut.answer_mode.value,
                 "tools": r.sut.tools_called, "intent": r.sut.intent}}
        for r in reports if not r.passed
    ]

    return {
        "router": router_kind,
        "router_source": sut.router.source,
        "model": getattr(sut.router, "model", None),
        "router_calls": getattr(sut.router, "n_calls", 0),
        "router_errors": getattr(sut.router, "n_errors", 0),
        "router_unparsed": getattr(sut.router, "n_unparsed", 0),
        "total_cases": len(cases),
        "cases_fully_passing": sum(1 for r in reports if r.passed),
        "per_check_pass": check_pass,
        "metrics": metrics,
        "failures": failures,
        "suite_counts": dict(Counter(c.suite for c in cases)),
    }


def _fmt_metric(m: dict) -> str:
    if "value" in m:
        v = m["value"]
        vs = "n/a" if v is None else f"{v:.4f}"
        extra = ""
        if m.get("missed_cases"):
            extra = f"  missed={m['missed_cases']}"
        return f"{vs}  ({m.get('num')}/{m.get('den')}){extra}"
    if "count" in m:
        return f"{m['count']} violations  {m.get('cases', [])}"
    return str(m)


def print_summary(out: dict) -> None:
    print(f"\n=== Neo support orchestrator · deterministic eval ===")
    print(f"router       : {out['router']} ({out['router_source']})")
    if out.get("router_calls"):
        print(f"llm calls    : {out['router_calls']}  | api-failed: {out['router_errors']}  | unparsed JSON: {out.get('router_unparsed', 0)}")
    print(f"cases        : {out['total_cases']}  | fully passing all checks: {out['cases_fully_passing']}")
    print(f"\n-- per-check pass (n/{out['total_cases']}) --")
    for name, n in out["per_check_pass"].items():
        print(f"  {name:<24} {n}/{out['total_cases']}")
    print(f"\n-- runner-spec §5 metrics --")
    for name, m in out["metrics"].items():
        print(f"  {name:<34} {_fmt_metric(m)}")
    if out["failures"]:
        print(f"\n-- {len(out['failures'])} cases with >=1 failing check --")
        for f in out["failures"]:
            print(f"  {f['case_id']:<34} failed={f['failed']}  sut={f['sut']['decision']}/{f['sut']['answer_mode']}")
    else:
        print("\nAll cases passed every structural check.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Neo support orchestrator deterministic eval runner")
    ap.add_argument("--router", choices=["mocked", "llm"], default="mocked")
    ap.add_argument("--cases", default=None, help="path to a cases yaml (default: ../eval/eval-cases.yaml)")
    ap.add_argument("--write", action="store_true", help="write JSON result to ../eval/results/")
    args = ap.parse_args()

    cases_path = Path(args.cases).resolve() if args.cases else None
    try:
        out = run(args.router, cases_path)
    except RuntimeError as e:
        print(f"\n[setup] {e}\n  export LLM_BASE_URL=... LLM_API_KEY=... [LLM_MODEL=...] then retry.")
        raise SystemExit(1)
    print_summary(out)

    if args.write:
        results_dir = _project_root() / "eval" / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        ts = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        fp = results_dir / f"run_{args.router}_{ts}.json"
        fp.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwrote {fp.relative_to(_project_root())}")


if __name__ == "__main__":
    main()
