"""Job pages for the examples dashboard: one page per queued job (scripts/jobq.py), with its pre-registration
(question, why it matters, hypotheses, decision rule, controls), its timing (queued, started, ended; setup, run and
examples time against the estimate), where its results are, and its worked examples (the run's examples.json).

Sources: results/jobq/ledger.jsonl (finished jobs, pulled from the box), cache/jobq/queue_state.json (pending and
running jobs at the last `jobq pull`). Each page goes to examples/job_<id>/ with a source.json "entry", so
examples.export_index lists it beside the lens-example pages.

examples.json (written by a script's `examples` stage):
    {"exp", "run", "groups": [{"key", "title", "definition", "n_total"}],
     "examples": [{"group", "family", "item_id", "prompt", "spans": [{"start", "end", "role"}], "condition",
                   "answers": {"clean", "edited", "expected": {hypothesis: answer}}, "numbers": {...}, "why"}]}
"""

from __future__ import annotations

import json
import shutil
from itertools import pairwise
from pathlib import Path
from typing import Any

from bridge_jspace.examples import _CSS, _esc

STATUS_ORDER = ("running", "pending", "failed", "done", "cancelled")
ROLE_COLOURS = ("#2a78d6", "#eb6834", "#2f9e6a", "#9b59b6", "#c9a227", "#d6456b", "#5a6b7d")
_JOB_CSS = """
main.solo{max-width:110ch}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:2px 14px;margin:6px 0}.kv dt{color:var(--faint)}
.kv dd{margin:0;overflow-wrap:anywhere}
.status{font:600 11px var(--sans);padding:1px 8px;border-radius:9px;background:var(--ctrl-bg)}
.status.done{background:rgba(47,158,106,.18)}.status.failed{background:rgba(214,69,107,.2)}
.status.running{background:var(--bridge-bg)}
.unverified{font:600 11px var(--sans);color:var(--answer)}
mark.sp{background:none;border-bottom:3px solid var(--c);padding:0 1px;color:inherit}
.legend span{display:inline-block;margin-right:12px;font-size:12px}
.legend i{display:inline-block;width:18px;height:3px;background:var(--c);vertical-align:middle;margin-right:4px}
td.hit{font-weight:600;color:var(--bridge)}
pre.cmd{font:12px var(--mono);background:var(--panel);padding:6px 8px;border-radius:4px;white-space:pre-wrap;
overflow-wrap:anywhere}
"""


def _fmt_duration(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    m = round(seconds / 60)
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


def load_jobs(repo: Path) -> list[dict[str, Any]]:
    """Every job known locally: the ledger's last record per id, then pending/running from the queue snapshot."""
    jobs: dict[str, dict[str, Any]] = {}
    ledger = repo / "results" / "jobq" / "ledger.jsonl"
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                jobs[rec["id"]] = rec
    state_file = repo / "cache" / "jobq" / "queue_state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
        for status in ("pending", "running", "cancelled"):
            for rec in state.get(status, []):
                if rec["id"] not in jobs:
                    jobs[rec["id"]] = {**rec, "status": status}
    return sorted(jobs.values(), key=lambda r: (STATUS_ORDER.index(r.get("status", "done")), r["id"]))


def find_examples(repo: Path, rec: dict[str, Any]) -> dict[str, Any] | None:
    for d in rec.get("new_results", []):
        path = repo / "results" / d / "examples.json"
        if path.exists():
            return json.loads(path.read_text())
    return None


def prompt_with_spans(prompt: str, spans: list[dict[str, Any]], colours: dict[str, str]) -> str:
    """The prompt with each span underlined in its role's colour; overlapping spans nest by start."""
    cuts = sorted({0, len(prompt), *(s["start"] for s in spans), *(s["end"] for s in spans)})
    out = []
    for a, b in pairwise(cuts):
        roles = [s["role"] for s in spans if s["start"] <= a and b <= s["end"]]
        text = _esc(prompt[a:b])
        if roles:
            out.append(
                f"<mark class='sp' style='--c:{colours[roles[-1]]}' title='{_esc(', '.join(roles))}'>{text}</mark>"
            )
        else:
            out.append(text)
    return "".join(out)


def _example_html(ex: dict[str, Any], colours: dict[str, str]) -> str:
    answers = ex.get("answers", {})
    edited = answers.get("edited")
    expected = answers.get("expected", {})
    hyp_rows = "".join(
        f"<tr><td>{_esc(h)}</td><td class='{'hit' if str(a) == str(edited) else ''}'>{_esc(str(a))}</td></tr>"
        for h, a in expected.items()
    )
    numbers = "".join(f"<tr><td>{_esc(k)}</td><td>{_esc(str(v))}</td></tr>" for k, v in ex.get("numbers", {}).items())
    return (
        f"<section class='card'><h3>{_esc(str(ex.get('family', '')))} · {_esc(str(ex.get('item_id', '')))}</h3>"
        f"<p class='meta'>{_esc(ex.get('condition', ''))}</p>"
        f"<div class='prompt'>{prompt_with_spans(ex.get('prompt', ''), ex.get('spans', []), colours)}</div>"
        f"<p class='meta'>clean <code>{_esc(str(answers.get('clean')))}</code> → edited "
        f"<code>{_esc(str(edited))}</code> · {_esc(ex.get('why', ''))}</p>"
        + (f"<table><tr><th>hypothesis</th><th>predicts</th></tr>{hyp_rows}</table>" if hyp_rows else "")
        + (f"<table><tr><th>number</th><th>value</th></tr>{numbers}</table>" if numbers else "")
        + "</section>"
    )


def _kv(rows: list[tuple[str, Any]]) -> str:
    cells = "".join(f"<dt>{_esc(k)}</dt><dd>{_esc(str(v))}</dd>" for k, v in rows if v not in (None, ""))
    return f"<dl class='kv'>{cells}</dl>"


def render_job(rec: dict[str, Any], examples: dict[str, Any] | None) -> str:
    status = rec.get("status", "pending")
    est = rec.get("est_gpu_hours")
    timing = [
        ("queued", rec.get("enqueued_at")),
        ("started", rec.get("started_at")),
        ("ended", rec.get("ended_at")),
        ("setup", _fmt_duration(rec.get("setup_s"))),
        ("run", f"{_fmt_duration(rec.get('run_s'))} (estimate {est} GPU-h)"),
        ("examples", _fmt_duration(rec.get("examples_s"))),
        ("total", _fmt_duration(rec.get("wall_s"))),
        (
            "GPU",
            f"{rec.get('gpu_name') or '-'}; peak {rec.get('peak_mem_gb')} GB (device; baseline "
            f"{rec.get('baseline_mem_gb')} GB)",
        ),
        ("exit", f"{rec.get('exit_code')} (examples {rec.get('examples_exit')})"),
    ]
    where = [
        ("code", rec.get("commit", "")[:10]),
        ("spec", rec.get("spec_path")),
        ("results", ", ".join(f"results/{d}" for d in rec.get("new_results", [])) or "-"),
        ("log", f"log/jobq/{rec['id']}/log.txt" if rec.get("log") else "-"),
        ("W&B", ", ".join(rec.get("wandb", [])) or "-"),
    ]
    hyps = "".join(
        f"<tr><td>{_esc(h)}</td><td class='o'>{_esc(str(p))}</td></tr>" for h, p in rec["hypotheses"].items()
    )
    controls = "".join(f"<li>{_esc(str(c))}</li>" for c in rec.get("controls", []))
    body = [
        f"<header><h1>{_esc(rec['id'])} <span class='status {status}'>{status}</span> "
        f"<span class='unverified'>UNVERIFIED</span></h1><div class='lead'><p>{_esc(rec['question'])}</p></div>"
        "</header><main class='solo'>",
        f"<h2>Why it matters</h2><p>{_esc(rec['why_it_matters'])}</p>",
        "<h2>Pre-registration</h2>",
        f"<table><tr><th>hypothesis</th><th>prediction (written before the run)</th></tr>{hyps}</table>",
        f"<p><b>Decision rule.</b> {_esc(rec['decision_rule'])}</p>",
        f"<p><b>Controls.</b></p><ul>{controls}</ul>",
        f"<p class='meta'>thread {_esc(rec['thread'])} · n {_esc(str(rec['n']))} · seeds {_esc(str(rec['seeds']))}"
        f" · depends on {_esc(str(rec.get('depends_on', [])))}</p>",
        f"<h2>Timing</h2>{_kv(timing)}<h2>Where</h2>{_kv(where)}",
        f"<pre class='cmd'>{_esc(rec['command'])}</pre>",
    ]
    if rec.get("error"):
        body.append(f"<h2>Worker error</h2><pre class='cmd'>{_esc(rec['error'])}</pre>")
    if examples:
        roles = sorted({s["role"] for ex in examples["examples"] for s in ex.get("spans", [])})
        colours = {r: ROLE_COLOURS[i % len(ROLE_COLOURS)] for i, r in enumerate(roles)}
        legend = "".join(f"<span style='--c:{c}'><i></i>{_esc(r)}</span>" for r, c in colours.items())
        body.append(f"<h2>Worked examples</h2><p class='legend'>{legend}</p>")
        for g in examples["groups"]:
            exs = [ex for ex in examples["examples"] if ex.get("group") == g["key"]]
            body.append(
                f"<section class='group'><h2>{_esc(g['title'])} <span class='badge'>{g['n_total']}</span></h2>"
                f"<p class='def'>{_esc(g['definition'])}</p>{''.join(_example_html(ex, colours) for ex in exs)}"
                "</section>"
            )
    elif status == "done":
        body.append("<p class='meta'>No examples.json in the job's results (no examples_command?).</p>")
    body.append("</main>")
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        f"<title>{_esc(rec['id'])}</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap">'
        f"<style>{_CSS}{_JOB_CSS}</style></head><body>{''.join(body)}</body></html>"
    )


def export_jobs(root: Path, repo: Path | None = None) -> list[Path]:
    """Render every known job into root/job_<id>/ (replacing the previous view) with an index entry."""
    from bridge_jspace.pins import REPO_ROOT

    repo = repo or REPO_ROOT
    outs = []
    for rec in load_jobs(repo):
        examples = find_examples(repo, rec)
        out = root / f"job_{rec['id']}"
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        (out / "index.html").write_text(render_job(rec, examples))
        meta = (
            f"{rec.get('status', 'pending')} · thread {rec['thread']} · run {_fmt_duration(rec.get('run_s'))} "
            f"(est {rec.get('est_gpu_hours')} GPU-h) · UNVERIFIED"
        )
        entry = {
            "title": f"{rec['id']}: {rec['question']}",
            "groups": (examples or {}).get("groups", []),
            "n_examples": len((examples or {}).get("examples", [])),
            "model": rec.get("gpu_name") or "-",
            "meta": meta,
        }
        (out / "source.json").write_text(json.dumps({"entry": entry, "job": rec["id"]}, indent=2))
        outs.append(out)
    return outs
