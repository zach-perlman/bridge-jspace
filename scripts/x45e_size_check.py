"""45e size check (Dan, 27 Oct ~01:00; descriptive, after the data; CPU only).

45e's wrong-pair control is built to hold the same share of each scene's change as identity outside J++ (idout), but in
some scenes it holds less (x6_routes.wrong_share_report). This recomputes 45e's conditions (i) and (ii)
(x6_routes.identity_control_flags, unchanged) on the scenes where the control reached at least 0.9 of idout's share
(share_wrong / share_idout >= 0.9 in the run's norms.jsonl; scenes with idout's share 0 are left out), per model, with n
beside each number. The score of Q45.7 stays as computed; this is reported beside it.

It also says why the control took zero directions in some scenes: wrong_pair_basis keeps the number of directions whose
share is closest to the target, so it takes none exactly when a single wrong-pair direction already holds at least twice
idout's share (or the pool has fewer than two entities). The report gives the pool sizes and idout's share in those
scenes against all scenes.

The 122B's 45e job (x45e_122b_q4) runs the identity arms only (--identity, no --identity-controls): no wrong-pair
control there, so nothing to check.

uv run python scripts/x45e_size_check.py     # results/x6_routes/x45e-size-<stamp>/{size.json, size.md}
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X
from scripts import x6_routes as R

RUNS = {"qwen3.5-9b": "qwen35_9b_x6_routes_x45e_dom", "qwen3.6-27b": "x6_routes_x45e_27b_dom",
        "muse-glimmer-30b": "muse30b_x6_routes_x45e_dom"}  # fmt: skip
AT = 0.9  # Dan: the control reached at least 0.9 of identity outside J++'s share


def matched(norms: list[dict], at: float = AT) -> set[str]:
    """Scenes whose wrong-pair control holds at least `at` of idout's share (idout's share > 0)."""
    return {r["scene"] for r in norms if r["share_idout"] > 0 and r["share_wrong"] / r["share_idout"] >= at - R.EPS}


def zero_directions(norms: list[dict], cases: dict[str, dict]) -> dict:
    """Per condition: the scenes where the wrong-pair control took no direction, their pool sizes and domains, and
    idout's share there against all scenes (median)."""
    out = {}
    for cond in sorted({r["condition"] for r in norms}):
        mine = [r for r in norms if r["condition"] == cond]
        k0 = [r for r in mine if r["k_wrong"] == 0]
        out[cond] = {"n": len(mine), "k0": len(k0),
                     "k0_pools": sorted({r["n_wrong_pool"] for r in k0}),
                     "k0_domains": sorted({cases[r["scene"]]["domain"] for r in k0}),
                     "k0_idout_median": float(np.median([r["share_idout"] for r in k0])) if k0 else None,
                     "all_idout_median": float(np.median([r["share_idout"] for r in mine])),
                     "all_pools": sorted({r["n_wrong_pool"] for r in mine})}  # fmt: skip
    return out


def check(name: str, n_boot: int = X.N_BOOT, at: float = AT) -> dict:
    src = R.RESULTS / name
    norms, rows = X.read_jsonl(src / "norms.jsonl"), X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    keep = matched(norms, at)
    sub = [r for r in rows if r["scene"] in keep]
    entities = {cond: len({cases[s]["bridge"] for s in keep if cases[s]["condition"] == cond}) for cond in ("C0", "C2")}
    return {"run": name, "all": R.identity_control_flags(rows, n_boot), "matched": R.identity_control_flags(sub, n_boot),
            "kept": {cond: sum(cases[s]["condition"] == cond for s in keep) for cond in ("C0", "C2")},
            "kept_entities": entities, "zero_directions": zero_directions(norms, cases)}  # fmt: skip


def fmt(v: list[float]) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def report(res: dict[str, dict]) -> list[str]:
    lines = ["# 45e size check (Dan 27 Oct ~01:00; descriptive, after the data)", "",
             f"Conditions (i) and (ii) of 45e (x6_routes.identity_control_flags, unchanged) on all scenes and on the scenes "
             f"where the wrong-pair control holds at least {AT} of identity outside J++'s share. Lookup; cluster bootstrap "
             f"over bridge entities, {X.N_BOOT} resamples, seed 0. n = scenes (bridge entities).", "",
             "| model | scenes | (i) C0: left without idout + J++ + pointer vs wrong pair + J++ + pointer (n) | (i) holds "
             "| (ii) C2: idout's cut minus the wrong pair's (n) | (ii) holds | both |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for model, r in res.items():
        for key, label in (("all", "all"), ("matched", f"control >= {AT}")):
            f = r[key]
            c0, c2 = f["c0"], f["c2"]
            n0 = f"{c0['n']}" + (f" ({r['kept_entities']['C0']})" if key == "matched" else "") if c0 else "0"
            n2 = f"{c2['n']}" + (f" ({r['kept_entities']['C2']})" if key == "matched" else "") if c2 else "0"
            i_ = f"{fmt(c0['left']['no_jppalfidout'])} vs {fmt(c0['left']['no_jppalfwrong'])} (n {n0})" if c0 else "–"
            ii_ = f"{fmt(c2['idout_vs_wrong'])} (n {n2})" if c2 else "–"
            lines.append(f"| {model} | {label} | {i_} | {'yes' if f['holds_i'] else 'no'} | {ii_} | "
                         f"{'yes' if f['holds_ii'] else 'no'} | {'yes' if f['both'] else 'no'} |")  # fmt: skip
    lines += ["", "Rule (fixed in advance): (i) the first number at most half the second; (ii) at least 0.15; both on at "
              "least 2 of 3 models. Q45.7's score stays as computed on all scenes.", "",
              "## Why the control took zero directions", "",
              "wrong_pair_basis keeps the number of directions whose share is closest to idout's share, so it takes none "
              "exactly when one wrong-pair direction already holds at least twice that share (or the pool has fewer than "
              "two entities).", "", "| model | condition | scenes | zero directions | pool sizes (all scenes) | domains "
              "(zero-direction scenes) | idout's share, median: zero-direction scenes vs all |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for model, r in res.items():
        for cond, z in r["zero_directions"].items():
            med = f"{z['k0_idout_median']:.4f} vs {z['all_idout_median']:.4f}" if z["k0"] else "–"
            lines.append(f"| {model} | {cond} | {z['n']} | {z['k0']} | {', '.join(map(str, z['all_pools']))} | "
                         f"{', '.join(z['k0_domains']) or '–'} | {med} |")  # fmt: skip
    return lines


def main() -> Path:
    res = {model: check(name) for model, name in RUNS.items()}
    out = R.RESULTS / f"x45e-size-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "size.json").write_text(json.dumps({"at": AT, "runs": RUNS, "models": res}, indent=1) + "\n")
    lines = report(res)
    (out / "size.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("wrote", out)
    return out


if __name__ == "__main__":
    main()
