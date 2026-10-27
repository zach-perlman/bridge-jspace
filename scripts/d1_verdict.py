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

--rule late-switch (Dan, 23 Oct ~12:00 +0200, written before qwen35_122b_d1_late_parts and
qwen35_122b_d1_formats_late_parts ran; the rules above untouched; named "late binding" until Dan renamed it, 23 Oct
afternoon, before any run, logic unchanged: the map shows the bridge still at its position at layers 33-38, so what
would change is the form the lookup reads, not the place): on Qwen3.5-122B the lens-readable part of a stated bridge
switched 29% [23, 36] of lookups at the map's cell (context, layer 24). Does the lookup stop reading it later?
  cells    --cells SET:LAYER ... (the bridge's sentence and the context at 30, 33, 36: every 3rd layer is the 122B's
           coarse grid); a cell is decisive iff the lens-free map has it in transit for lookups; the others and
           --reference cells (context:24) are reported only
  late switch holds iff at some decisive cell (a) the lens part's lookup switching has Wilson upper bound <= 0.05,
           (b) the rest switches >= 0.30 of lookups (point estimate), (c) recall control: the lens part switches >= 0.30
           of recalls there (point; the same patch: the lens part is not too small to act), and (d) random-subspace
           control: on recalls the lens part beats rand_sub (a random subspace keeping the lens part's share of the
           change, per row) with Wilson intervals apart (lens lower bound > rand_sub upper bound), and (e) it stays quiet
           (amended by Dan 23 Oct 12:30, before any run): at every later decisive cell of the same position set
           (sentence / context) the lens part's lookup switching has Wilson upper bound <= 0.10
  finding 2 fails on this model iff at every decisive cell the lens part's lookup switching has Wilson lower bound
           >= 0.20 and lies above rand_sub's on lookups (lens lower bound > rand_sub upper bound: not a size effect)
  otherwise inconclusive (the reason named). Reported per cell, lookups and recalls: full, jspace, not_jspace,
           not_jspace_matched, rand_sub, jspace_matched, rand_omp, the lens part's random-direction null, the parts'
           median shares; per topic and per format (not decisive).

--rule rest-size (A2, Dan 23 Oct afternoon, written before any run; the rules above untouched): where the lens part of
a stated bridge's change is quiet on lookups, is that its form (what it carries) or its size (a small piece of the
change)? not_jspace_matched = the rest of the change, each row shrunk to the lens part's norm.
  cells    --cells SET:LAYER ... each get the verdict below (reported); --decisive SET:LAYER decides for the model:
           finding 2's own decisive cell there (Qwen3.6-27B context:32, Qwen3.5-9B context:16). It must be in transit
           for lookups on the lens-free map, else not interpretable.
  H-form   the rest at the lens part's size switches lookups with Wilson lower bound >= 0.20 while the lens part's
           Wilson upper bound is <= 0.05
  H-size   the rest at the lens part's size switches lookups with Wilson upper bound <= 0.10: the lens part's quiet on
           lookups says nothing about its form (the lookup half of claim 6 carries no information)
  otherwise inconclusive. Reported per cell: lookups and recalls for every part above (recalls for both the lens part
           and the rest at its size); per topic at the decisive cell.

--rule necessity (B1, Dan 23 Oct 15:30, written before any run; the rules above untouched): in the band at the
bridge's word (bridge_word, bind_bridge; early layers), does the lookup need the lens-readable part (J) of the
stated bridge's change while the recall does? F(x) = share of items switched by pasting x; full = the change
(delta), not_jspace = delta - J, not_rand_sub = delta - rand_sub (rand_sub: a random subspace of J's share).
  lookup   J not needed iff F(full) - F(not_jspace) <= 0.10 (point), at a cell where the whole change switches >= 0.50
           of lookups (the agent's proposed gate; below it: not interpretable)
  recall   J needed iff F(full) - F(not_jspace) >= 0.20 (point) AND that drop exceeds F(full) - F(not_rand_sub) with
           the 95% lower bound of the difference of the two drops > 0 (paired bootstrap over scenes, 2000 resamples,
           seed 0)
  cell     the claim holds iff both; model: per set, it holds iff it holds at a majority of the set's listed cells
           (not interpretable cells count as not holding); the model holds iff every set holds (the agent's proposal)
  reported the parts' median shares of the change's squared norm (J, the random part; the rests are 1 - those)

--figures (late-switch, rest-size, necessity): the figure of the newest verdict of --parts under that rule, in a new
analysis-*-figures/ folder of the verdict.

uv run python scripts/d1_verdict.py --map M --parts P [--lookup PP --recall PM] [--tasks-set S] [--onset 44]
                                    [--cell SET:LAYER]
uv run python scripts/d1_verdict.py --rule late-switch --map M --parts P --cells SET:LAYER ... [--reference ...]
uv run python scripts/d1_verdict.py --rule rest-size --map M --parts P --cells SET:LAYER ... --decisive SET:LAYER
uv run python scripts/d1_verdict.py --rule late-switch|rest-size --parts P --figures
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import paired_bootstrap_diff, wilson

SP = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "d1_verdict"
SETS = ("bind_bridge", "bridge_word", "context")
JSPACE_MAX, REST_MIN, POSITIVE_MIN = 0.10, 0.50, 0.30
# --rule late-switch and --rule rest-size (see the docstring)
LATE_JSPACE_HI, LATE_REST_MIN, LATE_RECALL_MIN, FAIL_JSPACE_LO = 0.05, 0.30, 0.30, 0.20
LATE_STAYS_HI = 0.10  # (e), Dan 23 Oct 12:30: once quiet, the lens part stays quiet at the set's later decisive cells
FORM_REST_LO, SIZE_REST_HI = 0.20, 0.10  # rest-size: the rest at the lens part's size, Wilson lower / upper bound
REPORT_PARTS = ("full", "jspace", "not_jspace", "not_jspace_matched", "rand_sub", "not_rand_sub", "jspace_matched",
                "rand_omp")  # fmt: skip
# --rule necessity (B1, Dan 23 Oct 15:30): drops in points; LOOKUP_FULL_MIN is the agent's proposed gate
NOT_NEEDED_MAX, NEEDED_MIN, LOOKUP_FULL_MIN, NEED_BOOT, NEED_SEED = 0.10, 0.20, 0.50, 2000, 0


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


def late_switch_verdict(cells: dict[str, dict]) -> dict:
    """--rule late-switch on the decisive cells: cell -> {"lookup": {part: [rate, lo, hi, n]}, "recall": {...}} with
    at least jspace, not_jspace and rand_sub. Returns the verdict, the cells where the late switch holds and every
    check."""
    if not cells:
        return {"verdict": "not interpretable: no later cell is in transit for lookups on the map", "checks": {}}
    need = [(f, p) for f in ("lookup", "recall") for p in ("jspace", "not_jspace", "rand_sub")]
    if missing := [c for c, v in cells.items() if not all(v[f][p][3] for f, p in need)]:
        return {"verdict": f"not interpretable: no parts rows (or no rand_sub rows) at {missing}", "checks": {}}
    checks = {}
    for c, v in cells.items():
        lk, rc = v["lookup"], v["recall"]
        s, la = c.split(":")
        after = [x for x in cells if x.split(":")[0] == s and int(x.split(":")[1]) > int(la)]  # same set, later layers
        checks[c] = {
            "split": lk["jspace"][2] <= LATE_JSPACE_HI and lk["not_jspace"][0] >= LATE_REST_MIN,
            "recall_control": rc["jspace"][0] >= LATE_RECALL_MIN,
            "subspace_control_recall": rc["jspace"][1] > rc["rand_sub"][2],
            "stays_quiet": all(cells[x]["lookup"]["jspace"][2] <= LATE_STAYS_HI for x in after),
            "moves": lk["jspace"][1] >= FAIL_JSPACE_LO,
            "subspace_control_lookup": lk["jspace"][1] > lk["rand_sub"][2],
        }
    holds = ("recall_control", "subspace_control_recall", "stays_quiet")  # (c), (d), (e) on top of the split
    late = [c for c, k in checks.items() if k["split"] and all(k[h] for h in holds)]
    split_only = {c: [h for h in holds if not k[h]] for c, k in checks.items() if k["split"] and c not in late}
    size = [c for c, k in checks.items() if k["moves"] and not k["subspace_control_lookup"]]
    if late:
        verdict = f"late switch holds at {', '.join(late)}"
    elif all(k["moves"] and k["subspace_control_lookup"] for k in checks.values()):
        verdict = "finding 2 fails on this model: the lens part moves >= 20% of lookups at every later cell"
    elif split_only:
        verdict = (f"inconclusive: the split holds at {', '.join(split_only)} but fails there: "
                   + "; ".join(f"{c} {', '.join(f)}" for c, f in split_only.items()))  # fmt: skip
    elif all(k["moves"] for k in checks.values()):
        verdict = ("inconclusive: the lens part moves >= 20% of lookups at every later cell, but not more than a random "
                   f"subspace of its size at {', '.join(size)}")  # fmt: skip
    else:
        verdict = "inconclusive"
    return {"verdict": verdict, "late_cells": late, "checks": checks}


def rest_size_verdict(cell: dict) -> str:
    """--rule rest-size at one cell: {"lookup": {part: [rate, lo, hi, n]}, ...} with jspace and not_jspace_matched."""
    lk = cell["lookup"]
    if not (lk["jspace"][3] and lk["not_jspace_matched"][3]):
        return "not interpretable: no rows of the lens part or of the rest at its size"
    if lk["not_jspace_matched"][1] >= FORM_REST_LO and lk["jspace"][2] <= LATE_JSPACE_HI:
        return "H-form: the rest at the lens part's size switches lookups, the lens part does not"
    if lk["not_jspace_matched"][2] <= SIZE_REST_HI:
        return "H-size: the rest at the lens part's size does not switch lookups either"
    return "inconclusive"


def block(rows: list[dict], fam: str, cell: str) -> dict:
    """part -> [rate, lo, hi, n] of one family at one cell (jspace_null: the lens part's random-direction null)."""
    s, la = cell.split(":")
    at = [r for r in rows if r["family"] == fam and r["set"] == s and r["layer"] == int(la) and r["source"] == "cf"]
    out = {}
    for p, null in [*((p, False) for p in REPORT_PARTS), ("jspace", True)]:
        got = [r for r in at if r["part"] == p and r["null"] == null]
        out[f"{p}_null" if null else p] = [*rate(got), len(got)]
    return out


def switched(rows: list[dict], fam: str, cell: str, part: str) -> dict[str, int]:
    """item -> 1 if pasting `part` at the cell switched it to the other bridge's answer, else 0."""
    s, la = cell.split(":")
    return {r["name"]: int(r["role"] == "b") for r in rows if r["family"] == fam and r["set"] == s
            and r["layer"] == int(la) and r["source"] == "cf" and r["part"] == part and not r["null"]}  # fmt: skip


def necessity_cell(lk: dict[str, dict[str, int]], rc: dict[str, dict[str, int]]) -> dict:
    """--rule necessity at one cell. lk / rc: part -> item -> switched (0/1), parts full, not_jspace, not_rand_sub.
    F(x) = share switched by pasting x; drop_J = F(full) - F(not_jspace), drop_rand = F(full) - F(not_rand_sub)."""

    def f(d: dict[str, dict[str, int]], p: str) -> float:
        return sum(d[p].values()) / len(d[p]) if d.get(p) else float("nan")

    if not all(d.get(p) for d in (lk, rc) for p in ("full", "not_jspace", "not_rand_sub")):
        return {"verdict": "not interpretable: missing parts rows", "holds": False}
    lk_drop, rc_drop = f(lk, "full") - f(lk, "not_jspace"), f(rc, "full") - f(rc, "not_jspace")
    rc_drop_rand = f(rc, "full") - f(rc, "not_rand_sub")
    items = sorted(set(rc["not_rand_sub"]) & set(rc["not_jspace"]))  # drop_J - drop_rand = F(not_rand) - F(not_J)
    diff = paired_bootstrap_diff([rc["not_rand_sub"][i] for i in items], [rc["not_jspace"][i] for i in items],
                                 NEED_BOOT, NEED_SEED)  # fmt: skip
    lookup_gate = f(lk, "full") >= LOOKUP_FULL_MIN
    not_needed = lookup_gate and lk_drop <= NOT_NEEDED_MAX
    needed = rc_drop >= NEEDED_MIN and rc_drop > rc_drop_rand and diff[1] > 0
    if not lookup_gate:
        verdict = f"not interpretable: the whole change switches < {LOOKUP_FULL_MIN:.0%} of lookups here"
    else:
        verdict = "holds" if not_needed and needed else "does not hold"
    return {"verdict": verdict, "holds": not_needed and needed, "lookup_F_full": f(lk, "full"),
            "lookup_drop_J": lk_drop, "lookup_J_not_needed": not_needed, "recall_drop_J": rc_drop,
            "recall_drop_rand": rc_drop_rand, "recall_dropJ_minus_droprand": list(diff), "recall_J_needed": needed,
            "n_lookup": len(lk["full"]), "n_recall": len(items)}  # fmt: skip


def necessity_model(cells: dict[str, dict]) -> dict:
    """Per set (bridge_word, bind_bridge): holds iff the cell verdict holds at a majority of its listed cells (cells
    not interpretable count as not holding); the model holds iff it holds in every set (the agent's proposal)."""
    by_set: dict[str, list[bool]] = {}
    for k, c in cells.items():
        by_set.setdefault(k.split(":")[0], []).append(c["necessity"]["holds"])
    sets = {s: {"holds_at": sum(v), "cells": len(v), "holds": sum(v) > len(v) / 2} for s, v in by_set.items()}
    ok = bool(sets) and all(v["holds"] for v in sets.values())
    detail = "; ".join(f"{s} {v['holds_at']}/{v['cells']}" for s, v in sets.items())
    return {"verdict": f"{'holds' if ok else 'does not hold'} (cells where it holds: {detail})", "sets": sets}


def by_cell(a: argparse.Namespace) -> int:
    """--rule late-switch / rest-size / necessity: the rule's verdict, every listed cell reported for lookups and
    recalls."""
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    rows = [json.loads(x) for x in (SP / a.parts / "outcomes.jsonl").read_text().splitlines()]
    fve = [json.loads(x) for x in (SP / a.parts / "fve.jsonl").read_text().splitlines()]
    meta = load_meta(a.tasks_set)
    listed, reference = (
        [fixed_cell(rates, c, a.lookup) for c in a.cells],
        [fixed_cell(rates, c, a.lookup) for c in a.reference],
    )
    transit = [f"{c['set']}:{c['layer']}" for c in listed if c["transit"]]
    if a.rule == "late-switch":
        decisive = transit
    elif a.rule == "necessity":  # every listed band cell gets a verdict; the sets combine by majority
        decisive = [f"{c['set']}:{c['layer']}" for c in listed]
    else:
        assert a.decisive in a.cells, "rest-size: --decisive must be one of --cells"
        decisive = [a.decisive] if a.decisive in transit else []

    def share(s: str, la: int, what: str) -> float | None:
        v = sorted(f["share"] for f in fve if f.get("family") == a.lookup and f.get("set") == s and f["layer"] == la
                   and f["what"] == what)  # fmt: skip
        return v[len(v) // 2] if v else None

    def role(key: str, c: dict) -> str:
        if key in decisive:
            return "decisive"
        if c in reference:
            return "reference"
        return "reported" if a.rule == "rest-size" and c["transit"] else "not in transit"

    cells = {}
    for c in listed + reference:
        key = f"{c['set']}:{c['layer']}"
        cells[key] = {"role": role(key, c), "map_lookup_flips": c["map_flips"], "map_transit": c["transit"],
                      "lookup": block(rows, a.lookup, key), "recall": block(rows, a.recall, key),
                      "median_share": {w: share(c["set"], c["layer"], w) for w in ("jspace", "rand_sub", "rand_omp")}}  # fmt: skip
        if a.rule == "rest-size":
            cells[key]["verdict"] = rest_size_verdict(cells[key])
        if a.rule == "necessity":
            parts = ("full", "not_jspace", "not_rand_sub")
            cells[key]["necessity"] = necessity_cell({p: switched(rows, a.lookup, key, p) for p in parts},
                                                     {p: switched(rows, a.recall, key, p) for p in parts})  # fmt: skip
            cells[key]["median_share"]["not_jspace"] = 1 - (cells[key]["median_share"]["jspace"] or 0.0)
            cells[key]["median_share"]["not_rand_sub"] = 1 - (cells[key]["median_share"]["rand_sub"] or 0.0)

    def verdict_of_cells(sub: dict[str, dict]) -> dict:
        if a.rule == "late-switch":
            return late_switch_verdict(sub)
        if a.rule == "necessity":
            return necessity_model(sub)
        if not sub:
            return {
                "verdict": f"not interpretable: the decisive cell {a.decisive} is not in transit for lookups on the map"
            }
        return {"verdict": rest_size_verdict(sub[decisive[0]])}

    out = {"rule": a.rule, "map": a.map, "parts": a.parts, "decisive_cells": decisive,
           **verdict_of_cells({k: cells[k] for k in decisive}), "cells": cells}  # fmt: skip
    for key in ("format", "topic") if meta and a.rule != "necessity" else ():  # one format's / topic's rows: reported
        out[f"{key}_verdicts"] = {}
        for v in sorted({m[key] for m in meta.values()}):
            sel = [r for r in rows if meta.get(r["name"], {}).get(key) == v]
            sub = {k: {"lookup": block(sel, a.lookup, k), "recall": block(sel, a.recall, k)} for k in decisive}
            out[f"{key}_verdicts"][v] = {"verdict": verdict_of_cells(sub)["verdict"], "cells": sub}
    d = Path(a.out) / f"{a.parts}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    pct = lambda v: f"{100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}]" if v[3] else "-"  # noqa: E731
    what = "in transit for lookups on the map" if a.rule == "late-switch" else f"--decisive {a.decisive}, if in transit"
    lines = [f"# d1_verdict ({a.rule}) / {a.parts}", "", f"Map {a.map}; decisive cells ({what}): "
             f"{', '.join(decisive) or 'none'}", "", f"**Verdict:** {out['verdict']}", ""]  # fmt: skip
    if a.rule == "rest-size":
        lines += ["Per cell: " + "; ".join(f"{k}: {c['verdict']}" for k, c in cells.items()), ""]
    if a.rule == "necessity":
        lines += ["| cell | verdict | lookups: F(full), drop without J | recalls: drop without J, without the random "
                  "part, difference [95% paired bootstrap] | shares of the change: J, random part |", "|---|---|---|---|---|"]  # fmt: skip
        for k, c in cells.items():
            n, sh = c["necessity"], c["median_share"]
            if "recall_drop_J" not in n:
                lines.append(f"| {k} | {n['verdict']} | - | - | - |")
                continue
            dd = n["recall_dropJ_minus_droprand"]
            lines.append(f"| {k} | {n['verdict']} | {100 * n['lookup_F_full']:.0f}%, {100 * n['lookup_drop_J']:+.0f} pts | "
                         f"{100 * n['recall_drop_J']:+.0f}, {100 * n['recall_drop_rand']:+.0f}, {100 * dd[0]:+.0f} "
                         f"[{100 * dd[1]:+.0f}, {100 * dd[2]:+.0f}] pts | {sh['jspace']}, {sh['rand_sub']} |")  # fmt: skip
        lines.append("")
    for key in ("format", "topic"):
        if f"{key}_verdicts" in out:
            lines += [f"Per {key} (reported): " + "; ".join(f"{t}: {v['verdict']}" for t, v in out[f"{key}_verdicts"].items()), ""]  # fmt: skip
    lines += ["| cell | role | map: whole copy flips lookups | family | " + " | ".join(REPORT_PARTS) + " | jspace null | n |",
              "|---|---|---|---|" + "---|" * (len(REPORT_PARTS) + 2)]  # fmt: skip
    for k, c in cells.items():
        flips = "-" if c["map_lookup_flips"] is None else f"{100 * c['map_lookup_flips'][0]:.0f}%"
        for fam, name in (("lookup", a.lookup), ("recall", a.recall)):
            b = c[fam]
            lines.append(f"| {k} | {c['role']} | {flips} | {name} | " + " | ".join(pct(b[p]) for p in REPORT_PARTS)
                         + f" | {pct(b['jspace_null'])} | {b['jspace'][3]} |")  # fmt: skip
    lines += ["", "Median share of the change's squared norm (lookup rows): " + "; ".join(
        f"{k}: " + ", ".join(f"{w} {v:.3f}" if v is not None else f"{w} -" for w, v in c["median_share"].items())
        for k, c in cells.items())]  # fmt: skip
    (d / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:6]))
    print("wrote", d)
    return 0


BLUE, ORANGE, AQUA, CONTROL = "#2a78d6", "#eb6834", "#1baf7a", "#898781"  # statement_positions' validated slots
LENS, REST = ("jspace", BLUE, "o", False, "lens-readable part"), ("not_jspace", ORANGE, "s", False, "the rest")
REST_SMALL = ("not_jspace_matched", ORANGE, "s", True, "the rest at the lens part's size")
RANDOM = ("rand_sub", CONTROL, "D", False, "control: random subspace, the lens part's size")
FIGURE = {  # per rule: series (part, colour, marker, hollow, label), bars per panel, file, title, how to read
    "late-switch": {
        "series": (("full", AQUA, "o", False, "whole patch"), LENS, REST, REST_SMALL, RANDOM),
        "bars": {"lookup": (LATE_JSPACE_HI, FAIL_JSPACE_LO, LATE_REST_MIN), "recall": (LATE_RECALL_MIN,)},
        "bars_label": "bars: lookups 5% / 20% (lens part), 30% (the rest); recalls 30% (lens part)",
        "file": "late_switch.png",
        "title": "Does the lookup stop using the lens-readable part of a stated bridge at later layers?",
        "how": "Late switch: at some dark-labelled cell the lens part (blue) stays under 5% on lookups while the rest "
        "(orange) switches >= 30%, stays under 10% at the later cells of its row (sentence / context), and still "
        "switches >= 30% of recalls, above the grey control.",
    },
    "necessity": {
        "series": (
            ("full", AQUA, "o", False, "whole change"),
            ("not_jspace", ORANGE, "s", False, "without the lens part"),
            ("not_rand_sub", CONTROL, "D", False, "without a random part, the lens part's size"),
            LENS,
        ),
        "bars": {"lookup": (LOOKUP_FULL_MIN,), "recall": ()},
        "bars_label": "bar: 50%, the whole change must switch this many lookups for the cell to count",
        "file": "necessity.png",
        "title": "In the band at the bridge's word, does the lookup need the lens-readable part? Does the recall?",
        "how": "Per cell: lookups lose <= 10 points without the lens part (orange vs green); recalls lose >= 20 points "
        "without it, more than without a random part of the same size (grey), paired bootstrap lower bound > 0.",
    },
    "rest-size": {
        "series": (LENS, REST, REST_SMALL, RANDOM),
        "bars": {"lookup": (LATE_JSPACE_HI, SIZE_REST_HI, FORM_REST_LO), "recall": ()},
        "bars_label": "bars on lookups: 5% (lens part), 10% and 20% (the rest at the lens part's size)",
        "file": "rest_size.png",
        "title": "Shrunk to the lens-readable part's size, does the rest of a stated bridge's change still switch "
        "lookups?",
        "how": "Form: at the dark-labelled cell the rest at the lens part's size (hollow orange) switches lookups "
        "(lower bound >= 20%) while the lens part (blue) stays under 5%. Size: the shrunk rest stays under 10% too.",
    },
}


def rule_figures(a: argparse.Namespace) -> int:
    """--figures: the newest verdict of --parts under --rule as one figure (lookups | recalls, every cell)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, MUTED, SURFACE, finish, percent_axis, style_axes

    found = [p for p in sorted(Path(a.out).glob(f"{a.parts}_*/verdict.json"))
             if json.loads(p.read_text()).get("rule") == a.rule]  # fmt: skip
    assert found, f"no {a.rule} verdict of {a.parts} under {a.out}"
    v, spec = json.loads(found[-1].read_text()), FIGURE[a.rule]
    folder = found[-1].parent / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    folder.mkdir()
    series = spec["series"]
    keys = sorted(v["cells"], key=lambda k: (SETS.index(k.split(":")[0]), int(k.split(":")[1])))
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.8), sharey=True)
    for ax, fam, name in ((axes[0], "lookup", "lookups (the answer is read from the prompt)"),
                          (axes[1], "recall", "recalls (the answer comes from memory)")):  # fmt: skip
        style_axes(ax)
        for j, (p, color, marker, hollow, _) in enumerate(series):
            dx = (j - (len(series) - 1) / 2) * 0.15
            for i, k in enumerate(keys):
                r = v["cells"][k][fam][p]
                if not r[3]:
                    continue
                ax.plot([i + dx, i + dx], [r[1], r[2]], color=color, lw=2, solid_capstyle="round")
                ax.scatter([i + dx], [r[0]], c=SURFACE if hollow else color, marker=marker, s=44,
                           edgecolors=color if hollow else "white", linewidths=1.5 if hollow else 1, zorder=3)  # fmt: skip
        for y in spec["bars"][fam]:
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
        ax.set_yticks(sorted({0, *spec["bars"]["lookup"], *spec["bars"]["recall"], 0.4, 0.6, 0.8, 1.0}))
        percent_axis(ax)
    axes[0].set_ylabel("items whose answer switches to the other bridge's answer", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, lw=2, label=lab, markerfacecolor=SURFACE if hollow else c)
               for _, c, mk, hollow, lab in series]  # fmt: skip
    handles.append(Line2D([], [], color=MUTED, lw=0.8, ls=(0, (2, 2)), label=spec["bars_label"]))
    n = max(c["lookup"]["jspace"][3] for c in v["cells"].values())
    finish(fig, folder / spec["file"], spec["title"],
           f"Map {v['map']}, parts {v['parts']}; up to {n} items per family and cell, the same scenes for both families; "
           "bars: Wilson 95%.",
           handles=handles, ncols=3, handlelength=2.5,
           explain=[("What we did", "Changed the stated bridge, then pasted one part of the change (e.g. the "
                     "lens-readable part, the rest, the rest shrunk to the lens part's size) into the original run at "
                     "one place and layer."),
                    ("How to read", spec["how"]),
                    ("Control", "A random subspace that keeps the same share of the change as the lens part (grey); "
                     "grey labels: cells that do not decide."),
                    ("Verdict", v["verdict"])])  # fmt: skip
    print("wrote", folder / spec["file"])
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
    ap.add_argument("--rule", choices=("replication", "late-switch", "rest-size", "necessity"), default="replication")
    ap.add_argument("--cells", nargs="+", default=[], help="late-switch / rest-size: the cells, SET:LAYER")
    ap.add_argument("--reference", nargs="*", default=[], help="late-switch: cells reported only, SET:LAYER")
    ap.add_argument("--decisive", default=None, help="rest-size: the cell that decides, SET:LAYER (one of --cells)")
    ap.add_argument("--figures", action="store_true", help="late-switch / rest-size: figure of the newest verdict")
    a = ap.parse_args()
    if a.rule in ("late-switch", "rest-size", "necessity"):
        if a.figures:
            return rule_figures(a)
        assert a.map, f"{a.rule} needs --map"
        assert a.cells, f"{a.rule} needs --cells"
        assert a.rule != "rest-size" or a.decisive, "rest-size needs --decisive"
        return by_cell(a)
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
