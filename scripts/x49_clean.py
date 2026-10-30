"""x49_clean (batch 49, test 49.5; jobs/c3/batch49.yaml, no prediction): the 9B's headline cells rerun from a clean
checkout (job x49_5_9b: the queue runs every job in a fresh checkout of its commit), compared row for row with the
runs of record, as amendment 57's clean57 (results/checks/clean57_1027.json).

Five pairs (record -> clean, same command, only the run name changed; 47.8 with --layers 10 12):
  main test     x0_necessity  qwen35_9b_x0_necessity           -> qwen35_9b_clean49_x0_necessity
  routes        x6_routes     qwen35_9b_x6_routes              -> qwen35_9b_clean49_x6_routes
  only-U        x6_routes     qwen35_9b_x6_routes_keeponly     -> qwen35_9b_clean49_x6_routes_keeponly
  47.5 zeroing  x47_zero      qwen35_9b_x47_5                  -> qwen35_9b_clean49_x47_5
  47.8 anatomy  x47_anatomy   qwen35_9b_x47_anatomy            -> qwen35_9b_clean49_x47_anatomy (record rows at L10, L12
                                                                  and the unedited row only)
Per pair, on outcomes.jsonl: rows keyed per experiment (PAIRS[].key); the exact fields the headline cells are computed
from (switched / kept, top token, route, role, ...) counted where they differ; p_org, p_alt and ld (the logit
difference) as max |diff|; rows only in one run listed. Per headline cell the value from each run's rows.

Writes results/checks/clean49_9b.json (once; refuses to overwrite) and docs/depth/notes/handcheck_clean49.md (one line per
headline cell, then one line per pair). --pending writes the doc alone, with the clean column pending (before the job).

uv run python scripts/x49_clean.py              # CPU, after `jobq pull` brings the clean runs back
uv run python scripts/x49_clean.py --pending    # the doc before the run (record values only)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins

RESULTS = pins.RESULTS_DIR
OUT = pins.RESULTS_DIR / "checks" / "clean49_9b.json"
DOC = pins.REPO_ROOT / "docs" / "depth" / "notes" / "handcheck_clean49.md"
JOB = "x49_5_9b"
LOOKUP, RECALL = "PP", "PM"  # x0_necessity.READERS (not imported: this script needs no model code)
LAYER = 12  # X0's predicted layer for the 9B
NUMERIC = ("p_org", "p_alt", "ld")
N_EXAMPLES = 10


@dataclass(frozen=True)
class Pair:
    label: str
    exp: str
    record: str
    clean: str
    key: tuple[str, ...]
    fields: tuple[str, ...]
    scope: Callable[[dict], bool] | None = None  # record rows in the clean run's scope (None: every row)


def _anatomy_scope(r: dict) -> bool:
    return r["layer"] in (None, 10, 12)


PAIRS = (
    Pair("main test", "x0_necessity", "qwen35_9b_x0_necessity", "qwen35_9b_clean49_x0_necessity",
         ("scene", "rendering", "layer", "reader", "upstream", "dict", "k", "omp", "arm"),
         ("switched", "cand_switched", "cand_org_first", "role", "ws_skipped")),
    Pair("routes", "x6_routes", "qwen35_9b_x6_routes", "qwen35_9b_clean49_x6_routes",
         ("scene", "condition", "reader", "arm"), ("top", "route", "switched", "cand_switched", "cand_org_first", "role")),
    Pair("only-U", "x6_routes", "qwen35_9b_x6_routes_keeponly", "qwen35_9b_clean49_x6_routes_keeponly",
         ("scene", "condition", "reader", "arm"), ("top", "route", "switched", "cand_switched", "cand_org_first", "role")),
    Pair("47.5 zeroing", "x47_zero", "qwen35_9b_x47_5", "qwen35_9b_clean49_x47_5",
         ("scene", "reader", "arm"), ("kept", "to_org", "cand_kept", "top", "role")),
    Pair("47.8 anatomy", "x47_anatomy", "qwen35_9b_x47_anatomy", "qwen35_9b_clean49_x47_anatomy",
         ("scene", "condition", "reader", "layer", "arm"),
         ("route", "switched", "top", "top_text", "cand_switched", "cand_org_first", "role"), _anatomy_scope),
)  # fmt: skip


# ---- rows -----------------------------------------------------------------------------------------------------------


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def keyed(rows: list[dict], key: tuple[str, ...]) -> tuple[dict[tuple, dict], int]:
    """Rows by key, and the number of rows whose key was already taken (the first is kept)."""
    out: dict[tuple, dict] = {}
    dup = 0
    for r in rows:
        k = tuple(r.get(f) for f in key)
        if k in out:
            dup += 1
            continue
        out[k] = r
    return out, dup


def compare(record: list[dict], clean: list[dict], key: tuple[str, ...], fields: tuple[str, ...]) -> dict[str, Any]:
    """Row-for-row comparison: counts, rows only in one run, per field the shared rows where it differs, per numeric
    field the max |diff| over shared rows, and the first N_EXAMPLES differing rows (key and the differing fields)."""
    a, dup_a = keyed(record, key)
    b, dup_b = keyed(clean, key)
    shared = [k for k in a if k in b]
    differing = {f: 0 for f in fields}
    max_diff = {f: 0.0 for f in NUMERIC}
    missing = {f: 0 for f in (*fields, *NUMERIC)}  # shared rows where a field is absent from one side
    examples = []
    for k in shared:
        ra, rb = a[k], b[k]
        diff = {}
        for f in fields:
            if (f in ra) != (f in rb):
                missing[f] += 1
            if ra.get(f) != rb.get(f):
                differing[f] += 1
                diff[f] = [ra.get(f), rb.get(f)]
        for f in NUMERIC:
            if f in ra and f in rb and ra[f] is not None and rb[f] is not None:
                max_diff[f] = max(max_diff[f], abs(float(ra[f]) - float(rb[f])))
            elif (f in ra) != (f in rb):
                missing[f] += 1
        if diff and len(examples) < N_EXAMPLES:
            examples.append({"key": dict(zip(key, k, strict=True)), "differs": diff})
    only_a = [dict(zip(key, k, strict=True)) for k in a if k not in b]
    only_b = [dict(zip(key, k, strict=True)) for k in b if k not in a]
    identical = (not only_a and not only_b and not dup_a and not dup_b and not any(differing.values())
                 and not any(max_diff.values()) and not any(missing.values()))  # fmt: skip
    return {"key": list(key), "fields": list(fields), "rows_record": len(record), "rows_clean": len(clean),
            "shared": len(shared), "only_record": len(only_a), "only_clean": len(only_b),
            "only_record_first": only_a[:N_EXAMPLES], "only_clean_first": only_b[:N_EXAMPLES],
            "duplicate_keys": {"record": dup_a, "clean": dup_b}, "differing": differing,
            "fields_missing": {f: n for f, n in missing.items() if n}, "max_abs_diff": max_diff,
            "examples": examples, "identical": identical}  # fmt: skip


# ---- headline cells -------------------------------------------------------------------------------------------------


def main_gap(rows: list[dict]) -> tuple[float, int]:
    """The main test's gap at L12, chat, J++ k = 25 signed: recall extra loss minus lookup extra loss, each
    (S_no_rand - S_no_part) / S_whole (= Jdep - Rdep, x0_necessity.cell's excess); n = the recall's items."""
    ex, n = {}, 0
    for w in (LOOKUP, RECALL):
        mine = [r for r in rows if r["rendering"] == "chat" and r["layer"] == LAYER and r["reader"] == w]
        hits = {arm: sum(r["switched"] for r in mine if r["arm"] == arm and (arm == "whole" or (r["dict"], r["k"], r["omp"]) == ("jpp", 25, "signed")))
                for arm in ("whole", "no_part", "no_rand")}  # fmt: skip
        n = len({r["scene"] for r in mine if r["arm"] == "whole"})
        ex[w] = (hits["no_rand"] - hits["no_part"]) / hits["whole"] if hits["whole"] else float("nan")
    return ex[RECALL] - ex[LOOKUP], n


def share(rows: list[dict], *, arm: str, route: str, condition: str = "C2", layer: Any = ...) -> tuple[float, int]:
    """The lookup's share of rows with this route (condition, arm; layer when given), and n."""
    mine = [r for r in rows if r["reader"] == LOOKUP and r["condition"] == condition and r["arm"] == arm
            and (layer is ... or r["layer"] == layer)]  # fmt: skip
    return (sum(r["route"] == route for r in mine) / len(mine) if mine else float("nan")), len(mine)


def kept(rows: list[dict], *, arm: str, reader: str = RECALL) -> tuple[float, int]:
    mine = [r for r in rows if r["reader"] == reader and r["arm"] == arm]
    return (sum(r["kept"] for r in mine) / len(mine) if mine else float("nan")), len(mine)


CELLS: tuple[tuple[str, str, Callable[[list[dict]], tuple[float, int]]], ...] = (
    ("Main test gap (recall extra loss minus lookup extra loss), L12, chat", "main test", main_gap),
    ("Routes, another item moved, whole change: identity share", "routes", lambda r: share(r, arm="whole", route="identity")),
    ("Routes, another item moved, whole change: position share", "routes", lambda r: share(r, arm="whole", route="position")),
    ("Routes, another item moved, whole change: value share", "routes", lambda r: share(r, arm="whole", route="value")),
    ("Pointer directions removed: position share", "routes", lambda r: share(r, arm="no_alf", route="position")),
    ("A random part of their size removed: position share", "routes", lambda r: share(r, arm="no_alf_rand", route="position")),
    ("Only the pointer directions added (only-U): position share", "only-U", lambda r: share(r, arm="keep_alf", route="position")),
    ("Only a random part of their size added: position share", "only-U", lambda r: share(r, arm="keep_alf_rand", route="position")),
    ("47.5: recall answers kept, J++ atoms zeroed at L12", "47.5 zeroing", lambda r: kept(r, arm="zero_L")),
    ("47.5: recall answers kept, random subspace zeroed at L12", "47.5 zeroing", lambda r: kept(r, arm="rand_L")),
    ("47.8: position share under the whole change at L10", "47.8 anatomy", lambda r: share(r, arm="whole", route="position", layer=10)),
    ("47.8: position share under the whole change at L12", "47.8 anatomy", lambda r: share(r, arm="whole", route="position", layer=12)),
)  # fmt: skip


# ---- report ---------------------------------------------------------------------------------------------------------


def run_dir(exp: str, name: str) -> Path:
    return RESULTS / exp / name


def code_of(exp: str, name: str) -> dict | None:
    p = run_dir(exp, name) / "manifest.json"
    return json.loads(p.read_text()).get("code") if p.exists() else None


def head() -> str:
    out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=pins.REPO_ROOT, capture_output=True, text=True)
    return out.stdout.strip() or "unknown"


def build(pending: bool = False) -> dict[str, Any]:
    """Every pair's comparison and every headline cell. pending: clean runs may be missing (their values None)."""
    rows: dict[str, dict[str, list[dict] | None]] = {}
    comparisons = []
    for p in PAIRS:
        rec = read_rows(run_dir(p.exp, p.record) / "outcomes.jsonl")
        rec = [r for r in rec if p.scope(r)] if p.scope else rec
        cpath = run_dir(p.exp, p.clean) / "outcomes.jsonl"
        if not cpath.exists():
            assert pending, f"{cpath} is missing: pull the clean runs first (or --pending for the doc alone)"
            rows[p.label] = {"record": rec, "clean": None}
            comparisons.append({"test": p.label, "exp": p.exp, "record_run": p.record, "clean_run": p.clean,
                                "record_code": code_of(p.exp, p.record), "clean_code": None, "pending": True})  # fmt: skip
            continue
        cl = read_rows(cpath)
        rows[p.label] = {"record": rec, "clean": cl}
        comparisons.append({"test": p.label, "exp": p.exp, "record_run": p.record, "clean_run": p.clean,
                            "record_code": code_of(p.exp, p.record), "clean_code": code_of(p.exp, p.clean),
                            **({"record_scope": "layer in (None, 10, 12)"} if p.scope else {}),
                            **compare(rec, cl, p.key, p.fields)})  # fmt: skip
    cells = []
    for text, label, fn in CELLS:
        r, c = rows[label]["record"], rows[label]["clean"]
        rv, rn = fn(r or [])
        cv, cn = fn(c) if c is not None else (None, None)
        cells.append({"cell": text, "test": label, "record": rv, "n_record": rn, "clean": cv, "n_clean": cn,
                      "same": None if cv is None else (rv == cv and rn == cn)})  # fmt: skip
    done = [c for c in comparisons if not c.get("pending")]
    return {"what": "batch 49, test 49.5: the 9B's headline cells rerun from a clean checkout (job x49_5_9b), compared "
                    "row by row with the runs of record", "test": "49.5", "job": JOB, "written_at": head(),
            "comparisons": comparisons, "cells": cells,
            "all_identical": bool(done) and len(done) == len(comparisons) and all(c["identical"] for c in done)}  # fmt: skip


def fmt(v: float | None) -> str:
    return "pending" if v is None else f"{v:.2f}"


def fmt_diff(c: dict) -> str:
    bad = {f: n for f, n in c["differing"].items() if n}
    return ", ".join(f"{f} {n}" for f, n in bad.items()) or "none"


def render(report: dict[str, Any]) -> str:
    cmp = report["comparisons"]
    clean_code = sorted({f"{c['clean_code']['sha'][:8]}{' (dirty)' if c['clean_code'].get('dirty') else ''}"
                         for c in cmp if c.get("clean_code")})  # fmt: skip
    lines = [
        "# Hand-check pack, 49.5: the 9B's headline cells from a clean checkout",
        "",
        f"Generated by `uv run python scripts/x49_clean.py{' --pending' if any(c.get('pending') for c in cmp) else ''}` "
        f"at commit {report['written_at']}; do not hand-edit (rerun the script). Status: UNVERIFIED until a human adds "
        "it to VERIFIED.md.",
        "",
        "**What this is.** Each headline number below was computed once, by a run of record. Job `x49_5_9b` ran the "
        "same five commands again (only the run name changed: `qwen35_9b_clean49_` in front) in a fresh checkout of "
        "one committed tree, with nothing uncommitted, as the queue runs every job. If the code and data are what the "
        "commits say, every stored answer comes back the same. The 47.8 rerun covers layers 10 and 12 only "
        "(`--layers 10 12`), so its record rows are compared at those layers and the unedited row.",
        "",
        "**How to read it.** The first table gives each headline cell from the run of record and from the clean "
        "rerun, both recomputed here from the stored per-item answers (outcomes.jsonl), no verdict file read. The "
        "second table compares the two runs item by item: rows matched on their key (scene, reader, arm and so on), "
        "the stored answer fields counted where they differ, and the largest difference in the stored probabilities "
        "and logit difference. 'Same' means equal values over the same number of items.",
        "",
        f"Clean runs' commit: {', '.join(clean_code) if clean_code else 'pending'}.",
        "",
        "## Headline cells",
        "",
        "| cell | run of record | clean rerun | n (record / clean) | same |",
        "|---|---|---|---|---|",
    ]
    for c in report["cells"]:
        same = "pending" if c["same"] is None else ("yes" if c["same"] else "**no**")
        n = f"{c['n_record']} / {'pending' if c['n_clean'] is None else c['n_clean']}"
        lines.append(f"| {c['cell']} | {fmt(c['record'])} | {fmt(c['clean'])} | {n} | {same} |")
    lines += [
        "",
        "Formulas: the gap is (S_no_rand − S_no_part) / S_whole on the recall minus the same on the lookup, J++ k = 25, "
        "chat, layer 12 (S = switched items over all items); a share is the lookup's answers with that route over the "
        "items; kept is the recall's answers still S's answer over the items.",
        "",
        "## Row for row",
        "",
        "| test | run of record (commit) | clean run | rows record / clean / shared | only in one | fields that differ "
        "| max \\|diff\\| p_org / p_alt / ld | identical |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in cmp:
        rc = c["record_code"] or {}
        rec = f"`{c['record_run']}` ({str(rc.get('sha', '?'))[:8]}{', dirty' if rc.get('dirty') else ''})"
        if c.get("pending"):
            lines.append(f"| {c['test']} | {rec} | `{c['clean_run']}` | pending | | | | pending |")
            continue
        md = c["max_abs_diff"]
        lines.append(
            f"| {c['test']} | {rec} | `{c['clean_run']}` | {c['rows_record']} / {c['rows_clean']} / {c['shared']} "
            f"| {c['only_record']} / {c['only_clean']} | {fmt_diff(c)} | {md['p_org']:.2g} / {md['p_alt']:.2g} / "
            f"{md['ld']:.2g} | {'yes' if c['identical'] else '**no**'} |"
        )
    lines += ["", f"All identical: {'pending' if not report['all_identical'] and any(c.get('pending') for c in cmp) else ('yes' if report['all_identical'] else '**no**')}.", ""]  # fmt: skip
    diffs = [c for c in cmp if not c.get("pending") and c["examples"]]
    if diffs:
        lines += ["## Differing rows (first 10 per test)", ""]
        for c in diffs:
            for e in c["examples"]:
                lines.append(f"- {c['test']}: {json.dumps(e['key'])}: {json.dumps(e['differs'])}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else None)
    ap.add_argument("--pending", action="store_true", help="the doc alone, clean runs not yet pulled (no json)")
    a = ap.parse_args(argv)
    report = build(pending=a.pending)
    if not a.pending:
        assert not OUT.exists(), f"{OUT} exists: results are written once"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=1) + "\n")
        print("wrote", OUT)
    DOC.write_text(render(report))
    print("wrote", DOC)
    for c in report["cells"]:
        print(f"{c['cell']}: record {fmt(c['record'])} clean {fmt(c['clean'])}")


if __name__ == "__main__":
    main()
