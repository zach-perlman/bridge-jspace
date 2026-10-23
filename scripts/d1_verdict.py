"""d1_verdict: the D1-topics replication rule (jobs/d1/*d1_topics_*.yaml, amended 2026-10-22 17:36 +0200 before any
result was opened) applied to a map run and its parts run.

  cell     the decisive lookup cell, from the lens-free map alone: among the lookup family's statement cells
           (bind_bridge, bridge_word, context) in transit at the coarse layers in [32, onset), the one where C's whole
           copy flips the most lookups (point estimate; ties: the earlier layer, then bind_bridge, bridge_word, context)
  verdict  replicates iff at that cell, pooled over topics, the lens-readable part alone (jspace) switches <= 0.10 of
           lookups and everything else (not_jspace) >= 0.50, while the recall family's lens-readable part switches
           >= 0.30 there (the positive control); no recall row at the cell, or a failing positive control: not
           interpretable. Otherwise: does not replicate.
  reported per topic and by number style (digits / words; tasks_v2 sets), and the nulls (the lens-readable part's
           random-direction null, the OMP over a random dictionary), not decisive.
"switches" = the read's top token is the C bridge's answer (role b); items: every parts row of the cell (the parts
stage ran only on items the model answers right).

--cell SET:LAYER (d1_topics_v2 runs, fixed 2026-10-22 evening before they ran): the decisive cell is given in advance
(context:32, the cell d1_topics_map_27b chose) instead of chosen from the map. With a tasks set, each topic also gets
the same verdict on its own rows (topic_verdicts); a topic counts only if its own positive control passes.

--keep-min K (Gemma 4, Muse Glimmer; Dan, 22 Oct 23:45, before those runs): under the lens-part patch the lookups
must keep their original answer on >= K of items (role A at the decisive cell), else the verdict is "not
interpretable" (a model that breaks under almost any intervention makes a null meaningless).

--rule late-binding (Dan, 23 Oct ~12:00 +0200, written before qwen35_122b_d1_late_parts and
qwen35_122b_d1_formats_late_parts ran; the rules above untouched): on Qwen3.5-122B the lens-readable part of a stated
bridge switched 29% [23, 36] of lookups at the map's cell (context, layer 24). Does the lookup bind later?
  cells    --cells SET:LAYER ... (the bridge's sentence and the context at 30, 33, 36: every 3rd layer is the 122B's
           coarse grid); a cell is decisive iff the lens-free map has it in transit for lookups; the others and
           --reference cells (context:24) are reported only
  late binding holds iff at some decisive cell (a) the lens part's lookup switching has Wilson upper bound <= 0.05,
           (b) the rest switches >= 0.30 of lookups (point estimate), (c) recall control: the lens part switches >= 0.30
           of recalls there (point; the same patch: the lens part is not too small to act), and (d) random-subspace
           control: on recalls the lens part beats rand_sub (a random subspace keeping the lens part's share of the
           change, per row) with Wilson intervals apart (lens lower bound > rand_sub upper bound)
  finding 2 fails on this model iff at every decisive cell the lens part's lookup switching has Wilson lower bound
           >= 0.20 and lies above rand_sub's on lookups (lens lower bound > rand_sub upper bound: not a size effect)
  otherwise inconclusive (the reason named). Reported per cell, lookups and recalls: full, jspace, not_jspace,
           rand_sub, jspace_matched, rand_omp, the lens part's random-direction null, the parts' median shares;
           per topic and per format (not decisive).
  --figures: the figure of the newest late-binding verdict of --parts, in a new analysis-*-figures/ folder of it.

uv run python scripts/d1_verdict.py --map M --parts P [--lookup PP --recall PM] [--tasks-set S] [--onset 44]
                                    [--cell SET:LAYER]
uv run python scripts/d1_verdict.py --rule late-binding --map M --parts P --cells SET:LAYER ... [--reference ...]
uv run python scripts/d1_verdict.py --rule late-binding --parts P --figures
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import wilson

SP = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "d1_verdict"
SETS = ("bind_bridge", "bridge_word", "context")
JSPACE_MAX, REST_MIN, POSITIVE_MIN = 0.10, 0.50, 0.30
# --rule late-binding (see the docstring)
LATE_JSPACE_HI, LATE_REST_MIN, LATE_RECALL_MIN, FAIL_JSPACE_LO = 0.05, 0.30, 0.30, 0.20
LATE_PARTS = ("full", "jspace", "not_jspace", "rand_sub", "jspace_matched", "rand_omp")


def decisive_cell(rates: list[dict], lookup: str, lo: int, onset: int) -> dict | None:
    # The map's coarse grid (suite_split's MAP_LAYERS): every N/16-th layer, or the lens's own layers where it has only
    # some. Was "every 4th layer" (right for the 64-layer Qwens only): on Muse (52 layers, every 3rd) it never met the
    # parts' cells, on Gemma (60) only at 36; on 32-layer models it skipped half the grid (fixed 23 Oct ~01:00, before
    # any Muse / Gemma / OLMo-J++ D1 verdict ran; the 64-layer models' cells are unchanged).
    step = max(1, pins.N_LAYERS // 16)
    grid = (lambda la: la in pins.LENS_LAYERS) if pins.LENS_LAYERS else (lambda la: la % step == 0)
    cands = [r for r in rates if r["family"] == lookup and r["set"] in SETS and r["transit"] and lo <= r["layer"] < onset
             and grid(r["layer"])]  # fmt: skip
    if not cands:
        return None
    best = min(cands, key=lambda r: (-r["cf"]["flips"][0], r["layer"], SETS.index(r["set"])))
    return {"set": best["set"], "layer": best["layer"], "map_flips": best["cf"]["flips"]}


def fixed_cell(rates: list[dict], spec: str, lookup: str) -> dict:
    """--cell SET:LAYER, with the map's flips there when the map has that row."""
    s, layer = spec.split(":")
    assert s in SETS, f"--cell: {s} not one of {SETS}"
    row = next((r for r in rates if r["family"] == lookup and r["set"] == s and r["layer"] == int(layer)), None)
    return {"set": s, "layer": int(layer), "map_flips": row["cf"]["flips"] if row else None, "fixed": True,
            "transit": row["transit"] if row else None}  # fmt: skip


def verdict_of(lk: dict, rc: dict) -> str:
    """lk / rc: part -> [rate, lo, hi, n] of the lookup and recall families at the decisive cell."""
    if not rc["jspace"][3]:
        return "not interpretable: no recall row at the decisive cell"
    if rc["jspace"][0] < POSITIVE_MIN:
        return "not interpretable: the positive control fails"
    if lk["jspace"][0] <= JSPACE_MAX and lk["not_jspace"][0] >= REST_MIN:
        return "replicates"
    return "does not replicate"


def rate(rows: list[dict]) -> list[float]:
    return list(wilson(sum(r["role"] == "b" for r in rows), len(rows)))


def load_meta(tasks_set: str | None) -> dict[str, dict]:
    """Item id -> topic, number style and format, from a tasks_v2 set ({} without one)."""
    meta: dict[str, dict] = {}
    if tasks_set:
        for line in (pins.DATA_DIR / "tasks_v2" / tasks_set / "items.jsonl").read_text().splitlines():
            it = json.loads(line)
            meta[it["id"]] = {"topic": it["domain"], "numbers": it["numbers"], "format": it.get("format", "prose")}
    return meta


def late_binding_verdict(cells: dict[str, dict]) -> dict:
    """--rule late-binding on the decisive cells: cell -> {"lookup": {part: [rate, lo, hi, n]}, "recall": {...}} with
    at least jspace, not_jspace and rand_sub. Returns the verdict, the cells where late binding holds and every check."""
    if not cells:
        return {"verdict": "not interpretable: no later cell is in transit for lookups on the map", "checks": {}}
    need = [(f, p) for f in ("lookup", "recall") for p in ("jspace", "not_jspace", "rand_sub")]
    if missing := [c for c, v in cells.items() if not all(v[f][p][3] for f, p in need)]:
        return {"verdict": f"not interpretable: no parts rows (or no rand_sub rows) at {missing}", "checks": {}}
    checks = {}
    for c, v in cells.items():
        lk, rc = v["lookup"], v["recall"]
        checks[c] = {
            "split": lk["jspace"][2] <= LATE_JSPACE_HI and lk["not_jspace"][0] >= LATE_REST_MIN,
            "recall_control": rc["jspace"][0] >= LATE_RECALL_MIN,
            "subspace_control_recall": rc["jspace"][1] > rc["rand_sub"][2],
            "moves": lk["jspace"][1] >= FAIL_JSPACE_LO,
            "subspace_control_lookup": lk["jspace"][1] > lk["rand_sub"][2],
        }
    late = [c for c, k in checks.items() if k["split"] and k["recall_control"] and k["subspace_control_recall"]]
    split_only = [c for c, k in checks.items() if k["split"] and c not in late]
    size = [c for c, k in checks.items() if k["moves"] and not k["subspace_control_lookup"]]
    if late:
        verdict = f"late binding holds at {', '.join(late)}"
    elif all(k["moves"] and k["subspace_control_lookup"] for k in checks.values()):
        verdict = "finding 2 fails on this model: the lens part moves >= 20% of lookups at every later cell"
    elif split_only:
        verdict = f"inconclusive: the split holds at {', '.join(split_only)} but its controls fail there"
    elif all(k["moves"] for k in checks.values()):
        verdict = ("inconclusive: the lens part moves >= 20% of lookups at every later cell, but not more than a random "
                   f"subspace of its size at {', '.join(size)}")  # fmt: skip
    else:
        verdict = "inconclusive"
    return {"verdict": verdict, "late_cells": late, "checks": checks}


def late_binding(a: argparse.Namespace) -> int:
    """--rule late-binding: the verdict over the later cells, reported per cell for lookups and recalls."""
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    rows = [json.loads(x) for x in (SP / a.parts / "outcomes.jsonl").read_text().splitlines()]
    fve = [json.loads(x) for x in (SP / a.parts / "fve.jsonl").read_text().splitlines()]
    meta = load_meta(a.tasks_set)
    later, reference = (
        [fixed_cell(rates, c, a.lookup) for c in a.cells],
        [fixed_cell(rates, c, a.lookup) for c in a.reference],
    )
    decisive = [f"{c['set']}:{c['layer']}" for c in later if c["transit"]]

    def block(fam: str, cell: str, sel: list[dict]) -> dict:
        """part -> [rate, lo, hi, n] of one family at one cell (jspace_null: the lens part's random-direction null)."""
        s, la = cell.split(":")
        at = [r for r in sel if r["family"] == fam and r["set"] == s and r["layer"] == int(la) and r["source"] == "cf"]
        out = {}
        for p, null in [*((p, False) for p in LATE_PARTS), ("jspace", True)]:
            got = [r for r in at if r["part"] == p and r["null"] == null]
            out[f"{p}_null" if null else p] = [*rate(got), len(got)]
        return out

    def share(fam: str, s: str, la: int, what: str) -> float | None:
        v = sorted(f["share"] for f in fve if f.get("family") == fam and f.get("set") == s and f["layer"] == la
                   and f["what"] == what)  # fmt: skip
        return v[len(v) // 2] if v else None

    cells = {}
    for c in later + reference:
        key = f"{c['set']}:{c['layer']}"
        cells[key] = {"role": "decisive" if key in decisive else "reference" if c in reference else "not in transit",
                      "map_lookup_flips": c["map_flips"], "map_transit": c["transit"],
                      "lookup": block(a.lookup, key, rows), "recall": block(a.recall, key, rows),
                      "median_share": {w: share(a.lookup, c["set"], c["layer"], w) for w in ("jspace", "rand_sub", "rand_omp")}}  # fmt: skip
    out = {"rule": "late-binding", "map": a.map, "parts": a.parts, "decisive_cells": decisive,
           **late_binding_verdict({k: cells[k] for k in decisive}), "cells": cells}  # fmt: skip
    for key in ("format", "topic") if meta else ():  # the same rule on one format's / topic's rows: reported only
        out[f"{key}_verdicts"] = {}
        for v in sorted({m[key] for m in meta.values()}):
            sel = [r for r in rows if meta.get(r["name"], {}).get(key) == v]
            sub = {k: {"lookup": block(a.lookup, k, sel), "recall": block(a.recall, k, sel)} for k in decisive}
            out[f"{key}_verdicts"][v] = {"verdict": late_binding_verdict(sub)["verdict"], "cells": sub}
    d = Path(a.out) / f"{a.parts}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    pct = lambda v: f"{100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}]" if v[3] else "-"  # noqa: E731
    lines = [f"# d1_verdict (late binding) / {a.parts}", "", f"Map {a.map}; decisive cells (in transit for lookups on "
             f"the map): {', '.join(decisive) or 'none'}", "", f"**Verdict:** {out['verdict']}", ""]  # fmt: skip
    for key in ("format", "topic"):
        if f"{key}_verdicts" in out:
            lines += [f"Per {key} (reported): " + "; ".join(f"{t}: {v['verdict']}" for t, v in out[f"{key}_verdicts"].items()), ""]  # fmt: skip
    lines += ["| cell | role | map: whole copy flips lookups | family | " + " | ".join(LATE_PARTS) + " | jspace null | n |",
              "|---|---|---|---|" + "---|" * (len(LATE_PARTS) + 2)]  # fmt: skip
    for k, c in cells.items():
        flips = "-" if c["map_lookup_flips"] is None else f"{100 * c['map_lookup_flips'][0]:.0f}%"
        for fam, name in (("lookup", a.lookup), ("recall", a.recall)):
            b = c[fam]
            lines.append(f"| {k} | {c['role']} | {flips} | {name} | " + " | ".join(pct(b[p]) for p in LATE_PARTS)
                         + f" | {pct(b['jspace_null'])} | {b['jspace'][3]} |")  # fmt: skip
    lines += ["", "Median share of the change's squared norm (lookup rows): " + "; ".join(
        f"{k}: " + ", ".join(f"{w} {v:.3f}" if v is not None else f"{w} -" for w, v in c["median_share"].items())
        for k, c in cells.items())]  # fmt: skip
    (d / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:6]))
    print("wrote", d)
    return 0


def late_figures(a: argparse.Namespace) -> int:
    """--figures: the newest late-binding verdict of --parts as one figure (lookups | recalls, every cell)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, MUTED, finish, percent_axis, style_axes

    found = [p for p in sorted(Path(a.out).glob(f"{a.parts}_*/verdict.json"))
             if json.loads(p.read_text()).get("rule") == "late-binding"]  # fmt: skip
    assert found, f"no late-binding verdict of {a.parts} under {a.out}"
    v = json.loads(found[-1].read_text())
    folder = found[-1].parent / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    folder.mkdir()
    blue, orange, aqua, control = "#2a78d6", "#eb6834", "#1baf7a", "#898781"  # statement_positions' validated slots
    series = (("full", aqua, "o", "whole patch"), ("jspace", blue, "o", "lens-readable part"),
              ("not_jspace", orange, "s", "the rest"), ("rand_sub", control, "D", "control: random subspace, same size"))  # fmt: skip
    keys = sorted(v["cells"], key=lambda k: (SETS.index(k.split(":")[0]), int(k.split(":")[1])))
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.8), sharey=True)
    for ax, fam, name in ((axes[0], "lookup", "lookups (the answer is read from the prompt)"),
                          (axes[1], "recall", "recalls (the answer comes from memory)")):  # fmt: skip
        style_axes(ax)
        for j, (p, color, marker, _) in enumerate(series):
            dx = (j - 1.5) * 0.17
            for i, k in enumerate(keys):
                r = v["cells"][k][fam][p]
                if not r[3]:
                    continue
                ax.plot([i + dx, i + dx], [r[1], r[2]], color=color, lw=2, solid_capstyle="round")
                ax.scatter([i + dx], [r[0]], c=color, marker=marker, s=44, edgecolors="white", linewidths=1, zorder=3)
        for y in (LATE_JSPACE_HI, FAIL_JSPACE_LO, LATE_REST_MIN) if fam == "lookup" else (LATE_RECALL_MIN,):
            ax.axhline(y, color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=1)
        labels = []
        for k in keys:
            s, la = k.split(":")
            where = "bridge's sentence" if s == "bind_bridge" else s
            role = {"decisive": "", "reference": "\n(earlier cell)"}.get(v["cells"][k]["role"], "\n(reported only)")
            labels.append(f"{where}\nlayer {la}{role}")
        ax.set_xticks(range(len(keys)), labels, fontsize=8, color=MUTED)
        for t, k in zip(ax.get_xticklabels(), keys, strict=True):
            t.set_color(INK if v["cells"][k]["role"] == "decisive" else MUTED)
        ax.set_title(name, fontsize=9, color=INK, loc="left")
        ax.set_ylim(-0.02, 1.02)
        ax.set_yticks([0, LATE_JSPACE_HI, FAIL_JSPACE_LO, LATE_RECALL_MIN, 0.4, 0.6, 0.8, 1.0])  # the bars' values
        percent_axis(ax)
    axes[0].set_ylabel("items whose answer switches to the other bridge's answer", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, lw=2, label=lab) for _, c, mk, lab in series]
    handles.append(Line2D([], [], color=MUTED, lw=0.8, ls=(0, (2, 2)),
                          label="bars: lookups 5% / 20% (lens part), 30% (the rest); recalls 30% (lens part)"))  # fmt: skip
    n = max(c["lookup"]["jspace"][3] for c in v["cells"].values())
    finish(fig, folder / "late_binding.png",
           "Does the lookup stop using the lens-readable part of a stated bridge at later layers?",
           f"Map {v['map']}, parts {v['parts']}; up to {n} items per family and cell, the same scenes for both families; "
           "bars: Wilson 95%.",
           handles=handles, ncols=5, handlelength=2.5,
           explain=[("What we did", "Changed the stated bridge, then pasted one part of the change (the lens-readable "
                     "part, the rest, the whole) into the original run at one place and layer."),
                    ("How to read", "Late binding: at some dark-labelled cell the lens part (blue) stays under 5% on "
                     "lookups while the rest (orange) switches >= 30%, and the lens part still switches >= 30% of "
                     "recalls, above the grey control."),
                    ("Control", "A random subspace that keeps the same share of the change as the lens part (grey); "
                     "grey labels: cells that do not decide."),
                    ("Verdict", v["verdict"])])  # fmt: skip
    print("wrote", folder / "late_binding.png")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", help="the map run (every mode but --figures)")
    ap.add_argument("--parts", required=True)
    ap.add_argument("--lookup", default="PP")
    ap.add_argument("--recall", default="PM")
    ap.add_argument("--tasks-set", default=None, help="tasks_v2 set: topic and number style per item")
    ap.add_argument("--onset", type=int, default=44)
    ap.add_argument("--lo", type=int, default=32)
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new verdict folder")
    ap.add_argument("--cell", default=None, help="SET:LAYER fixed in advance (else chosen from the map)")
    ap.add_argument("--keep-min", type=float, default=None,
                    help="Gemma-style gate: under the lens-part patch, lookups keep their answer on >= this share")  # fmt: skip
    ap.add_argument("--rule", choices=("replication", "late-binding"), default="replication")
    ap.add_argument("--cells", nargs="+", default=[], help="late-binding: the later cells, SET:LAYER")
    ap.add_argument("--reference", nargs="*", default=[], help="late-binding: cells reported only, SET:LAYER")
    ap.add_argument("--figures", action="store_true", help="late-binding: the figure of the newest verdict of --parts")
    a = ap.parse_args()
    if a.rule == "late-binding":
        if a.figures:
            return late_figures(a)
        assert a.map, "late-binding needs --map"
        assert a.cells, "late-binding needs --cells"
        return late_binding(a)
    assert a.map, "--map is required"
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    cell = fixed_cell(rates, a.cell, a.lookup) if a.cell else decisive_cell(rates, a.lookup, a.lo, a.onset)
    assert cell, "no lookup statement cell in transit in the primary layers"
    rows = [json.loads(x) for x in (SP / a.parts / "outcomes.jsonl").read_text().splitlines()]
    at = [r for r in rows if r["set"] == cell["set"] and r["layer"] == cell["layer"] and r["source"] == "cf"
          and not r["null"]]  # fmt: skip
    nulls = [r for r in rows if r["set"] == cell["set"] and r["layer"] == cell["layer"] and r["source"] == "cf"
             and r["null"]]  # fmt: skip
    meta = load_meta(a.tasks_set)

    def part(fam: str, p: str, pool: list[dict] = at, key: str | None = None, value: str | None = None) -> list[float]:
        sel = [r for r in pool if r["family"] == fam and r["part"] == p
               and (key is None or meta.get(r["name"], {}).get(key) == value)]  # fmt: skip
        return [*rate(sel), len(sel)]

    out = {"map": a.map, "parts": a.parts, "cell": cell,
           "lookup": {p: part(a.lookup, p) for p in ("full", "jspace", "not_jspace", "rand_omp")},
           "recall": {p: part(a.recall, p) for p in ("full", "jspace", "not_jspace", "rand_omp")},
           "nulls": {"lookup_jspace_null": part(a.lookup, "jspace", nulls), "recall_jspace_null": part(a.recall, "jspace", nulls)}}  # fmt: skip
    verdict = verdict_of(out["lookup"], out["recall"])
    if a.keep_min is not None:  # a model that breaks under almost any patch: a null means something only if kept
        lk = [r for r in at if r["family"] == a.lookup and r["part"] == "jspace"]
        out["kept_under_lens_part"] = [*wilson(sum(r["role"] == "A" for r in lk), len(lk)), len(lk)]
        if not lk or out["kept_under_lens_part"][0] < a.keep_min:
            verdict = f"not interpretable: lookups keep their answer under the lens-part patch on < {a.keep_min:.0%}"
    out["verdict"] = verdict
    for key in ("topic", "numbers", "format"):
        values = sorted({m[key] for m in meta.values()})
        out[f"by_{key}"] = {v: {f"{fam}_{p}": part(fam, p, at, key, v) for fam in (a.lookup, a.recall)
                                for p in ("full", "jspace", "not_jspace")} for v in values}  # fmt: skip
    for key in ("topic", "format") if meta else ():  # the same verdict on one topic's / one format's rows
        out[f"{key}_verdicts"] = {
            v: verdict_of({p: c[f"{a.lookup}_{p}"] for p in ("jspace", "not_jspace")},
                          {p: c[f"{a.recall}_{p}"] for p in ("jspace", "not_jspace")})
            for v, c in out[f"by_{key}"].items()
        }  # fmt: skip
    d = Path(a.out) / f"{a.parts}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    flips = "no map row" if cell["map_flips"] is None else f"C's whole copy flips {100 * cell['map_flips'][0]:.0f}% of lookups"  # fmt: skip
    how = "fixed in advance" if cell.get("fixed") else f"chosen from map {a.map}"
    lines = [f"# d1_verdict / {a.parts}", "", f"Decisive cell ({how}): {cell['set']} at layer {cell['layer']} ({flips})",
             "", f"**Verdict:** {verdict}", "", "| family | part | switched [95%] | n |", "|---|---|---|---|"]  # fmt: skip
    for key in ("format", "topic"):
        if f"{key}_verdicts" in out:
            lines[6:6] = [f"Per {key}: " + "; ".join(f"{t}: {v}" for t, v in out[f"{key}_verdicts"].items()), ""]
    for fam, block in ((a.lookup, out["lookup"]), (a.recall, out["recall"])):
        for p, v in block.items():
            lines.append(f"| {fam} | {p} | {100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}] | {v[3]} |")
    for key in ("topic", "numbers", "format"):
        lines += [
            "",
            f"By {key} (reported, not decisive):",
            "",
            "| " + key + " | cell | switched | n |",
            "|---|---|---|---|",
        ]
        for v, cells in out[f"by_{key}"].items():
            for c, r in cells.items():
                if r[3]:
                    lines.append(f"| {v} | {c} | {100 * r[0]:.0f}% [{100 * r[1]:.0f}, {100 * r[2]:.0f}] | {r[3]} |")
    (d / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
