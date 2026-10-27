"""finding6_split (T9, 2026-10-22; CPU re-analysis of finished pointer_swap runs): does finding 6 ("the order label
counts order in the list, not place in the text") hold for the asked sentences 3-5 alone, not only pooled?

README slide 4 ("How the label counts") pools every asked sentence; the critic noted that the signal may come mostly
from the 1st and 2nd. This recomputes the counting comparison of the counting and shift runs split by the place k of
the donor's asked statement (k = slots.position + 1 = the donor's query_slot + 1, as in finding5_confirm): 1st-2nd
(k = 1, 2), 3rd-5th (k = 3, 4, 5), each k, and all k pooled (which must reproduce the run's summary.json).

Cells: memory -> prompt (RL), source dissoc, the last two tokens.
Layers: README slide 4's layer per model (figures f15 and f8: Qwen3.6-27B 50, Qwen3.5-9B 18, OLMo-3-7B-Instruct 18,
Gemma 4 31B 40) with every split; next to it, with 1st-2nd / 3rd-5th / all only, the run spec's other decisive layers:
Qwen3.6-27B 48 (pointer_swap's pre-registered primary pair 48 / 50), OLMo 17 and 19 (its spec's 17-19), and on
Qwen3.5-9B and Gemma the spec's value rule (every swept layer whose level's own cell has the donor's digit, value, at a
Wilson upper bound < 0.10; jobs/d3/*_r2.yaml). The value rule is recorded for every run and level.
Comparison per level: order = position (the original's k-th statement) vs place = the outcome that keeps the place:
  pointer_v4x  e5-off, e5more, e5fewer: token (the same token position); e5more / e5fewer also end (k-th from the end)
  pointer_v6   e5-abs: token (the same token position); e5-rel: back (the same distance back from the question)
Rates: share of patched items with that outcome, Wilson 95%. Differences: per item 1[order] - 1[place] (and
1[order] - 1[end]), the mean with an entity-cluster bootstrap 95% interval (the original's queried entity resampled
within its topic; stats.cluster_bootstrap, 4000 draws, seed 0, as finding5_confirm). Baseline: the rand control (a
random direction at the dissoc patch's norm, same cell) for order and place. Collateral damage: the same control's
changed share (any answer but the original's). Per cell, the items whose predictions are not all distinct digits.
No decision rule: a descriptive table; nothing here was fixed in advance.

uv run python scripts/finding6_split.py [--out DIR]
Writes <DIR>/<YYYYmmdd-HHMMSS>/table.md and table.json (DIR: results/finding6_split); prints only the folder, the
layers and the checks, no rates.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import cluster_bootstrap, wilson
from bridge_jspace.utils import git_state

PS_RESULTS = pins.RESULTS_DIR / "pointer_swap"
OUT = pins.RESULTS_DIR / "finding6_split"
FAMILY, GROUP = "RL", "last"
N_BOOT, SEED, VALUE_UB = 4000, 0, 0.10
# run -> (model, README slide 4's layer, the spec's other decisive layers: fixed, or None = by the spec's value rule)
RUNS = {
    "d3v4x_swap_main": ("Qwen3.6-27B", 50, (48,)),
    "qwen35_9b_d3v4x_swap_r2": ("Qwen3.5-9B", 18, None),
    "olmo3_7b_instruct_d3v4x_swap": ("OLMo-3-7B-Instruct", 18, (17, 19)),
    "gemma4it_d3v4x_swap_r2": ("Gemma 4 31B", 40, None),
    "d3v6_swap_27b": ("Qwen3.6-27B", 50, (48,)),
    "qwen35_9b_d3v6_swap_r2": ("Qwen3.5-9B", 18, None),
    "olmo3_7b_instruct_d3v6_swap": ("OLMo-3-7B-Instruct", 18, (17, 19)),
    "gemma4it_d3v6_swap_r2": ("Gemma 4 31B", 40, None),
}
PLACE = {"e5-off": "token", "e5more": "token", "e5fewer": "token", "e5-abs": "token", "e5-rel": "back"}
END_LEVELS = ("e5more", "e5fewer")
SPLITS = [("1st-2nd", (1, 2)), ("3rd-5th", (3, 4, 5)), ("all", (1, 2, 3, 4, 5))]
K_SPLITS = [(f"k={k}", (k,)) for k in range(1, 6)]  # at the README layer only


def diff(rows: list[dict], a: str, b: str) -> list[float] | None:
    """mean(1[role a] - 1[role b]) with its entity-cluster bootstrap interval (within topic); None for no rows."""
    if not rows:
        return None
    vals = [float(r["role"] == a) - float(r["role"] == b) for r in rows]
    out = cluster_bootstrap(vals, [r["_entity"] for r in rows], [r["domain"] for r in rows], n_boot=N_BOOT, seed=SEED)
    return [round(x, 4) for x in out]


def rates(rows: list[dict], roles: tuple[str, ...]) -> dict[str, list[float]]:
    n = len(rows)
    c = collections.Counter(r["role"] for r in rows)
    return {x: [round(v, 4) for v in wilson(c[x], n)] for x in roles} if n else {}


def cell(dissoc: list[dict], rand: list[dict], same: list[dict], lv: str) -> dict:
    place = PLACE[lv]
    shown = ("position", place, *(("end",) if lv in END_LEVELS else ()), "identity", "value", "none")
    same_changed = wilson(sum(r["role"] != "none" for r in same), len(same)) if same else None
    out: dict = {
        "n": len(dissoc),
        "k_entities": len({r["_entity"] for r in dissoc}),
        "not_distinct": sum(not r["_distinct"] for r in dissoc),
        "counts": dict(collections.Counter(r["role"] for r in dissoc)),
        "rates": rates(dissoc, shown),
        "order_minus_place": diff(dissoc, "position", place),
        "rand": {"n": len(rand), **rates(rand, ("position", place))},
        "same": {"n": len(same), "changed": [round(v, 4) for v in same_changed] if same_changed else None},
    }
    if lv in END_LEVELS:
        out["order_minus_end"] = diff(dissoc, "position", "end")
    return out


def check_pooled(c: dict, s_cell: dict | None) -> list[str]:
    """The pooled cell (all k) against the run's summary.json cell (summarise: Wilson rates of every role seen)."""
    if s_cell is None:
        return ["summary.json has no such cell"]
    errs = [] if s_cell["n"] == c["n"] else [f"n {c['n']} != summary {s_cell['n']}"]
    for role, cnt in c["counts"].items():
        if role not in s_cell or round(cnt / c["n"], 4) != s_cell[role][0]:
            errs.append(f"{role} rate differs from summary.json")
    for role in s_cell:
        if role != "n" and role not in c["counts"] and s_cell[role][0] != 0:
            errs.append(f"{role}: summary.json has hits, the recomputation none")
    return errs


def analyse_run(run: str, readme_layer: int, fixed: tuple[int, ...] | None) -> dict:
    from scripts import pointer_swap as PS

    d = PS_RESULTS / run
    m = json.loads((d / "manifest.json").read_text())
    for pin in m["items"].values():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{run}: {pin['file']} changed"
    items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
    rows = []
    for line in (d / "outcomes.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["family"] == FAMILY and r["group"] == GROUP and r["source"] in ("dissoc", "rand", "same"):
            rows.append(r)
    for r in rows:
        it = items[r["name"]]
        k = it["slots"]["position"] + 1  # 1-based place of the donor's asked statement
        assert k == it["sources"]["dissoc"]["query_slot"] + 1, r["name"]
        assert 1 <= k <= 5, r["name"]
        r["_k"], r["_entity"], r["_distinct"] = k, f"{r['domain']}:{r['entity']}", bool(it.get("distinct", True))
    summary = json.loads((d / "summary.json").read_text())["rates"]
    by: dict[tuple, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by[(r["source"], r["level"], str(r["layer"]))].append(r)
    levels = [x for x in m["levels"] if x in PLACE]
    value_ub: dict[str, dict[str, float]] = {}
    for lv in levels:
        value_ub[lv] = {}
        for la in m["layers"]:
            sel = by[("dissoc", lv, str(la))]
            value_ub[lv][str(la)] = round(wilson(sum(r["role"] == "value" for r in sel), len(sel))[2], 4)
    rule = {lv: [la for la in m["layers"] if value_ub[lv][str(la)] < VALUE_UB] for lv in levels}
    layers = {lv: [readme_layer, *(fixed if fixed is not None else [x for x in rule[lv] if x != readme_layer])]
              for lv in levels}  # fmt: skip
    cells, errors = {}, []
    for lv in levels:
        for la in layers[lv]:
            src = {s: by[(s, lv, str(la))] for s in ("dissoc", "rand", "same")}
            assert src["dissoc"], f"{run}: no rows for {lv} at layer {la}"
            for name, ks in SPLITS + (K_SPLITS if la == readme_layer else []):
                part = {s: [r for r in v if r["_k"] in ks] for s, v in src.items()}
                cells[f"{lv}|{la}|{name}"] = cell(part["dissoc"], part["rand"], part["same"], lv)
            pooled = cells[f"{lv}|{la}|all"]
            s_cell = summary.get(f"{FAMILY}|all|{lv}|{GROUP}|{la}|dissoc")
            errors += [f"{lv}|{la}: {e}" for e in check_pooled(pooled, s_cell)]
            parts = cells[f"{lv}|{la}|1st-2nd"]["n"] + cells[f"{lv}|{la}|3rd-5th"]["n"]
            if parts != pooled["n"]:
                errors.append(f"{lv}|{la}: splits {parts} != pooled {pooled['n']}")
    return {
        "data": m["data"],
        "manifest_model": m["model"],
        "outcomes_sha256": hashlib.sha256((d / "outcomes.jsonl").read_bytes()).hexdigest(),
        "readme_layer": readme_layer,
        "other_layers_from": "fixed in the spec" if fixed is not None else "by the spec's value rule",
        "layers": layers,
        "value_rule_layers": rule,
        "value_ub_by_level_layer": value_ub,
        "checks": {"pooled_reproduces_summary_and_splits_partition": not errors, "errors": errors},
        "cells": cells,
    }


def pct(x: list[float] | None) -> str:
    return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}]" if x else "-"


def pts(x: list[float] | None) -> str:
    return f"{100 * x[0]:+.0f} [{100 * x[1]:+.0f}, {100 * x[2]:+.0f}]" if x else "-"


def table_md(out: dict) -> str:
    lines = [
        "# finding6_split: the counting comparison split by the asked sentence",
        "",
        "Question (T9): does finding 6 (\"the order label counts order in the list, not place in the text\") hold for the asked sentences 3-5 alone, not only pooled over all asked sentences as in README slide 4?",
        "",
        f"Cells: memory → prompt, the donor prompt's last two tokens copied into the original prompt at one layer (pointer_swap, source dissoc). Asked = the place k of the donor's asked statement (k = slots.position + 1, as in scripts/finding5_confirm.py). Rows \"all\" pool every k and reproduce the run's summary.json (checked). Commit {out['git']['sha'][:7]}{' (uncommitted changes in the tree)' if out['git']['dirty'] else ''}, script scripts/finding6_split.py.",
        "",
        "Columns: order = the answer went to the original's k-th statement (position); place = the statement at the same place in the text (token; e5-off, e5more, e5fewer, e5-abs) or at the same distance back from the question (back; e5-rel); end = the k-th from the end (e5more, e5fewer only); unchanged = the original's answer. Rates: % of patched items, Wilson 95%. Differences: points, per item 1[order] - 1[place] (or 1[order] - 1[end]), entity-cluster bootstrap 95% (the original's queried entity resampled within its topic, 4000 draws, seed 0). rand = a random direction at the patch's norm (the baseline for order / place); same = the same-control patch (every hypothesis predicts the original answer), its changed share is the collateral damage.",
        "",
        "Layers: \"README\" = the layer README slide 4 reports (every split, and each k). \"spec\" = the run spec's other decisive layers (1st-2nd, 3rd-5th and all only): Qwen3.6-27B 48 (the pre-registered pair 48 / 50), OLMo 17 and 19 (its spec's 17-19), Qwen3.5-9B and Gemma by the spec's value rule (every swept layer whose level's own cell has the donor's digit at a Wilson upper bound < 10%).",
        "",
        "Notes: e5more has no k = 1 and e5fewer no k = 5 (the generators' layouts), so the 1st-2nd rows of e5more are k = 2 only and the 3rd-5th rows of e5fewer k = 3-4. A percentile bootstrap has zero width when every item agrees. No decision rule was fixed for this split: the table is descriptive.",
        "",
    ]  # fmt: skip
    for run, r in out["runs"].items():
        if "error" in r:
            lines += [f"## {r['model']}: {run}", "", f"Not processed: {r['error']}", ""]
            continue
        rl = r["readme_layer"]
        rule_txt = "; ".join(f"{lv}: {', '.join(map(str, v)) or 'none'}" for lv, v in r["value_rule_layers"].items())
        off = [lv for lv, v in r["value_rule_layers"].items() if rl not in v]
        lines += [f"## {r['model']}: {run} ({r['data']})", "",
                  f"README layer {rl}; the other spec layers {r['other_layers_from']}. The value rule's layers per level: {rule_txt}. The README layer {'passes the value rule on every level' if not off else 'fails the value rule on ' + ', '.join(off)}. Checks (the pooled rows reproduce summary.json, the splits partition them): {'ok' if r['checks']['pooled_reproduces_summary_and_splits_partition'] else r['checks']['errors']}.",
                  "",
                  "| level | layer | asked | n / entities | order | place | order − place, pts | end | order − end, pts | identity | unchanged | rand: order / place | same: changed |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for key, c in r["cells"].items():
            lv, la, split = key.split("|")
            place = PLACE[lv]
            fails_rule = "" if int(la) in r["value_rule_layers"][lv] else "; donor's digit ≥ 10%"
            tag = f"{la} ({'README' if int(la) == rl else 'spec'}{fails_rule})"
            if not c["n"]:
                lines.append(f"| {lv} | {tag} | {split} | 0 | - | - | - | - | - | - | - | - | - |")
                continue
            rt, rd = c["rates"], c["rand"]
            nd = f" ({c['not_distinct']} not distinct)" if c["not_distinct"] else ""
            lines.append(
                f"| {lv} | {tag} | {split} | {c['n']} / {c['k_entities']}{nd} | {pct(rt['position'])} | "
                f"{place}: {pct(rt[place])} | {pts(c['order_minus_place'])} | {pct(rt.get('end'))} | "
                f"{pts(c.get('order_minus_end'))} | {pct(rt['identity'])} | {pct(rt['none'])} | "
                f"{pct(rd.get('position'))} / {pct(rd.get(place))} (n {rd['n']}) | "
                f"{pct(c['same']['changed'])} (n {c['same']['n']}) |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new table folder")
    a = ap.parse_args()
    out: dict = {
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "script": "scripts/finding6_split.py",
        "git": git_state(),
        "params": {"family": FAMILY, "group": GROUP, "source": "dissoc", "controls": ["rand", "same"],
                   "splits": dict(SPLITS + K_SPLITS), "k_splits_at": "the README layer only", "place": PLACE,
                   "end_levels": list(END_LEVELS), "rates": "Wilson 95%",
                   "differences": f"entity-cluster bootstrap 95% within topic, {N_BOOT} draws, seed {SEED}",
                   "value_rule": f"swept layers whose level's own cell (RL, last, dissoc) has value's Wilson upper bound < {VALUE_UB}"},
        "runs": {},
    }  # fmt: skip
    for run, (model, readme_layer, fixed) in RUNS.items():
        try:
            out["runs"][run] = {"model": model, **analyse_run(run, readme_layer, fixed)}
        except (FileNotFoundError, AssertionError, KeyError) as e:
            out["runs"][run] = {"model": model, "error": f"{type(e).__name__}: {e}"}
    d = Path(a.out) / time.strftime("%Y%m%d-%H%M%S")
    d.mkdir(parents=True)
    (d / "table.json").write_text(json.dumps(out, indent=1) + "\n")
    (d / "table.md").write_text(table_md(out))
    for run, r in out["runs"].items():  # status only: no rates, the table is read by the humans first
        status = r.get("error") or (
            f"{len(r['cells'])} cells, layers {r['layers']}, checks "
            f"{'ok' if r['checks']['pooled_reproduces_summary_and_splits_partition'] else r['checks']['errors']}"
        )
        print(f"{run}: {status}")
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
