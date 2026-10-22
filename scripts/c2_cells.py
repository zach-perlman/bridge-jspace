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
          bridge alt's statement) of the patch, the lens push at 1x and 2x, and the random push. C2-lens holds in a cell
          iff the patch >= 0.20 and the lens push, at the size that wrote recall there, is <= random + 0.05 and <= its
          own recall rate / 3. Also pooled over the selected cells. Step b (a supervised identity direction, fitted and
          tested on different entities, which must also write recall; >= 0.15 on the lookups needed) needs >= 12
          distinct asked entities pooled over the selected cells; the count is reported.

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
C2_PATCH_MIN, C2_MARGIN, C2_RATIO = 0.20, 0.05, 3.0
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


def reveal_cell(cell: dict, cases: dict[str, dict], rows: list[dict]) -> dict:
    """The reveal stage on one selected cell: memory -> prompt items whose alt prompt asks statement 3-5."""
    conds = cells_of(rows, "RL").get((cell["domain"], cell["layer"]), {})

    def late(rs: list[dict]) -> list[dict]:
        return [r for r in rs if cases[r["name"]]["target_slot"] >= 2]

    size = cell["lens_size"]
    patch = rate(late(conds.get(("patch", None), [])))
    lens = {str(s): rate(late(conds.get(("lens", s), []))) for s in (1.0, 2.0)}
    rand = {str(s): rate(late(conds.get(("random", s), []))) for s in (1.0, 2.0)}
    lk, rk = lens[str(size)], rand[str(size)]
    holds = (patch["rate"] >= C2_PATCH_MIN and lk["rate"] <= rk["rate"] + C2_MARGIN
             and lk["rate"] <= cell["rr_lens"][str(size)]["rate"] / C2_RATIO)  # fmt: skip
    ents = sorted({cases[r["name"]]["query"] for rs in conds.values() for r in late(rs)})
    out = {**cell, "rl_patch": patch, "rl_lens": lens, "rl_random": rand, "rl_entities": ents, "c2_lens": holds}
    if conds.get(("ident", size)):  # step b: the identity direction at the size the lens wrote recall with
        rr = cells_of(rows, "RR").get((cell["domain"], cell["layer"]), {})
        rl_id, rr_id = rate(late(conds[("ident", size)])), rate(rr.get(("ident", size), []))
        out |= {"rl_ident": rl_id, "rr_ident": rr_id,
                "two_codes": holds and rl_id["rate"] >= IDENT_LOOKUP_MIN and rr_id["rate"] >= IDENT_RECALL_MIN}  # fmt: skip
    return out


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
    revealed = [reveal_cell(c, *data[c["run"]]) for c in sel["cells"] if c["selected"]]
    ents = sorted({e for c in revealed for e in c["rl_entities"]})
    out = {"cells_sha256": digest, "cells": revealed, "pooled_entities": len(ents),
           "step_b_ready": len(ents) >= STEP_B_ENTITIES}  # fmt: skip
    (a.out / "reveal.json").write_text(json.dumps(out, indent=1))
    for c in revealed:
        s = str(c["lens_size"])
        print(f"{c['run']:28s} {c['domain']:9s} L{c['layer']:<3d} lookups 3-5: patch {100 * c['rl_patch']['rate']:.0f}% "
              f"lens {100 * c['rl_lens'][s]['rate']:.0f}% random {100 * c['rl_random'][s]['rate']:.0f}% "
              f"(n {c['rl_patch']['n']}) | recall lens {100 * c['rr_lens'][s]['rate']:.0f}% | C2-lens {c['c2_lens']}"
              + (f" | identity: lookups {100 * c['rl_ident']['rate']:.0f}% (n {c['rl_ident']['n']}), recall "
                 f"{100 * c['rr_ident']['rate']:.0f}% | two codes {c['two_codes']}" if "rl_ident" in c else ""))  # fmt: skip
    print(f"pooled entities {len(ents)}; step b ready: {out['step_b_ready']}; wrote {a.out / 'reveal.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
