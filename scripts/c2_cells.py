"""c2_cells (sharp C2, step a; rule fixed 2026-10-22 before the sweep runs): where does the lens push write RECALL, the
positive control a "the lens does not write the lookup" result needs, and in those cells what do the lens push and the
patch do to LOOKUPS of statements 3-5?

Background (UNVERIFIED; README slide 5): at layer 48 on pointer_v4 the lens push writes neither the lookup (0 of 256
lookups of statements 3-5 moved to the bridge's statement) nor recall (memory -> memory: 2 / 150 at 1x, 8 / 150 at 2x,
the patch 50 / 150), so that zero says nothing. The one cell found where the lens does write recall is pointer_v1's
chemical elements at layer 44 (6 entities). The sweep runs (pointer_fit on pointer_v4 and pointer_v1, layers 32-48)
look for more such cells; this script reads them in two stages, in this order:

  select  memory -> memory (RR) rows only, per run x topic x layer: the identity rate (the recalled answer switched to
          bridge alt's) of the lens push at 1x and 2x, the random push at 1x and 2x, and the patch. A cell is SELECTED
          iff the lens push at 1x or at 2x has rate >= 0.20 with a Wilson 95% lower bound >= 0.10, the random push
          stays <= 0.05 at both sizes, and the patch moves >= 0.20. Writes <out>/cells.json. Never reads a memory ->
          prompt row.
  reveal  only once cells.json exists (its sha256 is recorded in the output): in each selected cell, memory -> prompt
          items whose alt prompt asks statement 3-5 (target_slot >= 2): the identity rate (answer = the org digit of
          bridge alt's statement) of the patch, the lens push and the random push at the size that wrote recall there.
          Each cell, and the PRIMARY pool, gets one of four states:
            not testable  the patch moves < 0.20 of these lookups (the lookup does not use what was pushed here)
            refuted       the lens push >= 3x the random push and >= random + 0.15: the lens does write the lookup
            holds         the lens push's upper 95% bound <= half the lower 95% bound of the same push on recall, and
                          the lens push <= random + 0.05
            inconclusive  otherwise
          PRIMARY: one cell per run x topic (the selected layer with the highest lens-on-recall rate, chosen on the
          memory -> memory rows alone; neighbouring layers share their items, so they are not pooled), pooled over
          those cells; the lens push's interval is an entity-cluster bootstrap (asked entity, strata run x topic,
          2000, seed 0) widened to the Wilson interval where that is wider, recall's a Wilson interval. Per-cell states are reported, not decisive.
          Step b (pointer_fit --ident): "two codes" iff the pool holds, and the identity push moves >= 0.15 of the
          lookups and >= 0.20 of the recalls, over >= 12 distinct asked entities.
  Amended 2026-10-22 16:30, after the sweeps ran and before any reveal (no memory -> prompt row of them read): the
  three-state output, the upper-bound rule, the one-layer-per-topic primary pool and the entity bootstrap replace "C2
  holds iff patch >= 0.20, lens <= random + 0.05 and <= recall / 3" on point estimates.

uv run python scripts/c2_cells.py select --runs RUN [RUN ...] --out DIR
uv run python scripts/c2_cells.py reveal --runs RUN [RUN ...] --out DIR
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import wilson

FIT = pins.RESULTS_DIR / "pointer_fit"
LENS_MIN, LENS_LO, RANDOM_MAX, PATCH_MIN = 0.20, 0.10, 0.05, 0.20
C2_PATCH_MIN, C2_MARGIN, HOLD_FRACTION = 0.20, 0.05, 0.5
REFUTE_RATIO, REFUTE_MARGIN = 3.0, 0.15
STEP_B_ENTITIES = 12
IDENT_LOOKUP_MIN, IDENT_RECALL_MIN = 0.15, 0.20  # step b (pointer_fit --ident; its docstring's rule)


def load(run: str) -> tuple[dict[str, dict], list[dict]]:
    d = FIT / run
    cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
    rows = [json.loads(x) for x in (d / "outcomes.jsonl").read_text().splitlines()]
    return cases, rows


def rate(rows: list[dict]) -> dict:
    k, n = sum(r["role"] == "identity" for r in rows), len(rows)
    p, lo, hi = wilson(k, n) if n else (float("nan"),) * 3
    return {"k": k, "n": n, "rate": p, "lo": lo, "hi": hi}


def cells_of(rows: list[dict], family: str) -> dict[tuple, dict[tuple, list[dict]]]:
    """(domain, layer) -> (cond, scale) -> rows, for one family, steer layers only (not the 'window')."""
    out: dict[tuple, dict[tuple, list[dict]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        if (r["family"] == family and r["cond"] in ("lens", "random", "patch", "ident")
                and r["layer"] not in (None, "window")):  # fmt: skip
            out[(r["domain"], int(r["layer"]))][(r["cond"], r["scale"])].append(r)
    return out


def select_cells(run: str, cases: dict[str, dict], rows: list[dict]) -> list[dict]:
    """The select stage on one run: RR rows only."""
    out = []
    for (domain, layer), conds in sorted(cells_of(rows, "RR").items()):
        lens = {s: rate(conds.get(("lens", s), [])) for s in (1.0, 2.0)}
        rand = {s: rate(conds.get(("random", s), [])) for s in (1.0, 2.0)}
        patch = rate(conds.get(("patch", None), []))
        wrote = [s for s in (1.0, 2.0) if lens[s]["n"] and lens[s]["rate"] >= LENS_MIN and lens[s]["lo"] >= LENS_LO]
        best = max(wrote, key=lambda s: lens[s]["rate"]) if wrote else None
        ok = (
            bool(wrote)
            and all(rand[s]["n"] and rand[s]["rate"] <= RANDOM_MAX for s in (1.0, 2.0))
            and (patch["n"] > 0 and patch["rate"] >= PATCH_MIN)
        )
        ents = sorted({cases[r["name"]]["query"] for rs in conds.values() for r in rs if r["name"] in cases})
        out.append({"run": run, "domain": domain, "layer": layer, "selected": ok, "lens_size": best,
                    "rr_lens": {str(s): v for s, v in lens.items()}, "rr_random": {str(s): v for s, v in rand.items()},
                    "rr_patch": patch, "rr_entities": len(ents)})  # fmt: skip
    return out


def c2_state(patch: float, lens: float, lens_hi: float, rand: float, recall_lo: float) -> str:
    """The reveal rule's state from the lookups' patch, lens (and its upper bound) and random rates and the lower bound
    of the same lens push on recall."""
    if patch < C2_PATCH_MIN:
        return "not testable"
    if lens >= REFUTE_RATIO * rand and lens >= rand + REFUTE_MARGIN:
        return "refuted"
    if lens_hi <= HOLD_FRACTION * recall_lo and lens <= rand + C2_MARGIN:
        return "holds"
    return "inconclusive"


def cell_rows(cell: dict, cases: dict[str, dict], rows: list[dict]) -> dict[str, list[dict]]:
    """A selected cell's rows at the size that wrote recall: lookups of statements 3-5 (patch, lens, random, ident) and
    recalls (lens, ident)."""
    size = cell["lens_size"]
    rl = cells_of(rows, "RL").get((cell["domain"], cell["layer"]), {})
    rr = cells_of(rows, "RR").get((cell["domain"], cell["layer"]), {})

    def late(rs: list[dict]) -> list[dict]:
        return [r for r in rs if cases[r["name"]]["target_slot"] >= 2]

    return {"patch": late(rl.get(("patch", None), [])), "lens": late(rl.get(("lens", size), [])),
            "random": late(rl.get(("random", size), [])), "ident": late(rl.get(("ident", size), [])),
            "rr_lens": rr.get(("lens", size), []), "rr_ident": rr.get(("ident", size), [])}  # fmt: skip


def judge(parts: dict[str, list[dict]], cases: dict[str, dict], cluster: bool) -> dict:
    """Rates and the state of one cell (Wilson) or of the primary pool (entity-cluster bootstrap for the lens)."""
    r = {k: rate(v) for k, v in parts.items()}
    if cluster and parts["lens"]:
        from bridge_jspace.stats import cluster_bootstrap

        vals = [float(x["role"] == "identity") for x in parts["lens"]]
        ents = [cases[x["name"]]["query"] for x in parts["lens"]]
        strata = [x["_stratum"] for x in parts["lens"]]
        _, lo, hi = cluster_bootstrap(vals, ents, strata)  # widened to Wilson where wider (zero hits: [0, 0] else)
        r["lens"] |= {"lo": min(lo, r["lens"]["lo"]), "hi": max(hi, r["lens"]["hi"]),
                      "interval": "entity-cluster bootstrap, widened to Wilson"}  # fmt: skip
    state = c2_state(r["patch"]["rate"], r["lens"]["rate"], r["lens"]["hi"], r["random"]["rate"], r["rr_lens"]["lo"])
    out = {"rates": r, "state": state,
           "entities": sorted({cases[x["name"]]["query"] for x in parts["patch"]})}  # fmt: skip
    if parts["ident"]:
        out["two_codes"] = (state == "holds" and r["ident"]["rate"] >= IDENT_LOOKUP_MIN
                            and r["rr_ident"]["rate"] >= IDENT_RECALL_MIN)  # fmt: skip
    return out


def primary_cells(selected: list[dict]) -> list[dict]:
    """One selected cell per run x topic: the layer with the highest lens-on-recall rate (memory -> memory only)."""
    best: dict[tuple, dict] = {}
    for c in selected:
        key = (c["run"], c["domain"])
        score = c["rr_lens"][str(c["lens_size"])]["rate"]
        if key not in best or score > best[key]["rr_lens"][str(best[key]["lens_size"])]["rate"]:
            best[key] = c
    return [best[k] for k in sorted(best)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["select", "reveal"])
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    sel_path = a.out / "cells.json"
    data = {run: load(run) for run in a.runs}
    if a.stage == "select":
        cells = [c for run, (cases, rows) in data.items() for c in select_cells(run, cases, rows)]
        sel_path.write_text(json.dumps({"rule": {"lens_min": LENS_MIN, "lens_lo": LENS_LO, "random_max": RANDOM_MAX,
                                                 "patch_min": PATCH_MIN}, "cells": cells}, indent=1))  # fmt: skip
        for c in cells:
            lens = " ".join(f"{s}x {100 * v['rate']:.0f}% [{100 * v['lo']:.0f}]" for s, v in c["rr_lens"].items())
            print(f"{c['run']:28s} {c['domain']:9s} L{c['layer']:<3d} RR lens {lens} | random "
                  f"{max(v['rate'] for v in c['rr_random'].values()):.2f} | patch {100 * c['rr_patch']['rate']:.0f}% | "
                  f"{c['rr_entities']} ent | {'SELECTED' if c['selected'] else '-'}")  # fmt: skip
        print("wrote", sel_path)
        return 0
    assert sel_path.exists(), "run the select stage first"
    sel = json.loads(sel_path.read_text())
    digest = hashlib.sha256(sel_path.read_bytes()).hexdigest()
    selected = [c for c in sel["cells"] if c["selected"]]
    per_cell = [{**c, **judge(cell_rows(c, *data[c["run"]]), data[c["run"]][0], cluster=False)} for c in selected]
    prim = primary_cells(selected)
    pool: dict[str, list[dict]] = collections.defaultdict(list)
    all_cases: dict[str, dict] = {}
    for c in prim:
        cases, rows = data[c["run"]]
        all_cases |= cases
        for k, v in cell_rows(c, cases, rows).items():
            pool[k] += [{**x, "_stratum": f"{c['run']}|{c['domain']}"} for x in v]
    primary = judge(dict(pool), all_cases, cluster=True) if prim else {"state": "not testable: no cell selected"}
    out = {"cells_sha256": digest, "primary_cells": [(c["run"], c["domain"], c["layer"]) for c in prim],
           "primary": primary, "per_cell": per_cell,
           "step_b_ready": len(primary.get("entities", [])) >= STEP_B_ENTITIES}  # fmt: skip
    (a.out / "reveal.json").write_text(json.dumps(out, indent=1))

    def line(tag: str, j: dict) -> str:
        r = j["rates"]
        ident = (f" | identity: lookups {100 * r['ident']['rate']:.0f}%, recall {100 * r['rr_ident']['rate']:.0f}%, "
                 f"two codes {j['two_codes']}" if "two_codes" in j else "")  # fmt: skip
        return (f"{tag} lookups 3-5 (n {r['patch']['n']}, {len(j['entities'])} ent): patch {100 * r['patch']['rate']:.0f}% "
                f"lens {100 * r['lens']['rate']:.0f}% [{100 * r['lens']['lo']:.0f}, {100 * r['lens']['hi']:.0f}] "
                f"random {100 * r['random']['rate']:.0f}% | lens on recall {100 * r['rr_lens']['rate']:.0f}% "
                f"[lo {100 * r['rr_lens']['lo']:.0f}] | {j['state'].upper()}{ident}")  # fmt: skip

    for c in per_cell:
        print(line(f"{c['run']:28s} {c['domain']:9s} L{c['layer']:<3d}", c))
    print(line("PRIMARY " + ", ".join(f"{d} L{la}" for _, d, la in out["primary_cells"]), primary) if prim
          else "PRIMARY: no cell selected (not testable)")  # fmt: skip
    print(f"step b ready (>= {STEP_B_ENTITIES} entities): {out['step_b_ready']}; wrote {a.out / 'reveal.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
