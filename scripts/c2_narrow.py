"""c2_narrow: the narrow C2 (C2'), pre-registered in docs/prereg_replication_1022.md (Zach, 2026-10-21 ~00:55 UTC
10-22, before any Mistral-Small-24B-2501 or Qwen3-32B run). The 27B's wm2_full2_v2 is the data the rule was read off,
so on the 27B it is reported, not evidence.

Claim (C2'): a bridge stated in the prompt (P) or computed in it (C) is written by its own lens direction only when the
last step recalls from memory (X->M), not when it looks the answer up (X->P).
Rule, per bridge source X in {P, C}, from c2_graded's scoring of the model's two-step steering run (own lens direction,
lens_add / lens_swap, question / final positions, cells gated by the random control): X passes if
  (a) the cross-validated write X->M >= X->P + 10 points, and
  (b) X->M >= 3 x X->P (cross-validated), and
  (c) the lower end of X->M's best-cell 95% interval over bridge entities >= the upper end of X->P's.
C2' HOLDS if P and C both pass, PARTIAL if one does, FAILS if neither; UNDERPOWERED (no verdict) if any of P->P, P->M,
C->P, C->M has fewer than 30 cases. Recalled bridges (M->P, M->M) are reported, not tested.

python scripts/c2_narrow.py RUN [RUN ...]   (reads results/write_max/c2_graded/RUN.json; writes results/write_max/c2_narrow/RUN.md and .json)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

SRC = pins.RESULTS_DIR / "write_max" / "c2_graded"
OUT = pins.RESULTS_DIR / "write_max" / "c2_narrow"
MIN_N, GAP, RATIO = 30, 0.10, 3.0


def verdict(fams: dict) -> dict:
    per = {}
    for x in ("P", "C"):
        lo, hi = fams[f"{x}P"], fams[f"{x}M"]
        wp, wm = lo["cv_own_direction"] or 0.0, hi["cv_own_direction"] or 0.0
        n = min(lo["own_direction"]["n"], hi["own_direction"]["n"])
        ci_ok = hi["own_direction"]["ci"][0] >= lo["own_direction"]["ci"][1]
        per[x] = {"write_XP": wp, "write_XM": wm, "n_min": n, "gap_ok": wm >= wp + GAP, "ratio_ok": wm >= RATIO * wp,
                  "ci_ok": ci_ok, "XM_ci": hi["own_direction"]["ci"], "XP_ci": lo["own_direction"]["ci"]}  # fmt: skip
        per[x]["pass"] = per[x]["gap_ok"] and per[x]["ratio_ok"] and ci_ok
    if any(p["n_min"] < MIN_N for p in per.values()):
        v = "UNDERPOWERED"
    else:
        k = sum(p["pass"] for p in per.values())
        v = "HOLDS" if k == 2 else "PARTIAL" if k == 1 else "FAILS"
    return {"verdict": v, "per_source": per}


def main(runs: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for run in runs:
        fams = json.loads((SRC / f"{run}.json").read_text())["families"]
        out = verdict(fams) | {"run": run, "rule": (__doc__ or "").split("\n\n")[1]}
        recalled = {f: fams[f]["cv_own_direction"] for f in ("MP", "MM") if f in fams}
        out["recalled_reported"] = recalled
        (OUT / f"{run}.json").write_text(json.dumps(out, indent=2) + "\n")
        lines = [f"# C2' (narrow) / {run}: {out['verdict']} (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)", "",
                 "| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |",
                 "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for x, p in out["per_source"].items():
            lines.append(f"| {x} | {100 * p['write_XP']:.0f} [{100 * p['XP_ci'][0]:.0f}-{100 * p['XP_ci'][1]:.0f}] | "
                         f"{100 * p['write_XM']:.0f} [{100 * p['XM_ci'][0]:.0f}-{100 * p['XM_ci'][1]:.0f}] | {p['gap_ok']} | "
                         f"{p['ratio_ok']} | {p['ci_ok']} | {p['n_min']} | {p['pass']} |")  # fmt: skip
        lines += ["", "Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).",
                  "Recalled bridges, reported only (CV write): " + ", ".join(f"{k} {100 * (v or 0):.0f}" for k, v in recalled.items())]
        (OUT / f"{run}.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    main(ap.parse_args().runs)
