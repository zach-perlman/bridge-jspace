"""x0_paired (Dan's item 1, 24 Oct ~18:45; descriptive, added after data): is the drop in excess from the two-change
X0 edit to the single-change edit the item set or the edit?

At the predicted layer, the word, chat, J++ k = 25 signed: per reader, S_whole, Jdep, Rdep and excess for
  (1) the two-change run on all its items; (2) the two-change run on the items both runs share;
  (3) the single-change run on the shared items; (4) the single-change run on all its items;
and the paired differences on the shared items, (3) - (2) (the edit) and (2) - (1) (the item set, unpaired: a subset),
with 95% CIs from one cluster bootstrap over bridge entities (10,000 resamples, seed 0) for the paired ones.
Writes results/x0_necessity/<single run>/paired-<UTC>/{paired.md, paired.json}.

uv run python scripts/x0_paired.py --cf x0_necessity_27b_chat --single x0_single_27b_r2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X

NOTE = "Descriptive, added after data (Dan, 24 Oct ~18:45, item 1); not part of X0's rule."


def arms_of(rows: list[dict], layer: int, reader: str) -> dict[str, dict[str, int]]:
    """scene -> switched, per arm (whole, no_part, no_rand) at the layer, J++ k = 25 signed."""
    out: dict[str, dict[str, int]] = {"whole": {}, "no_part": {}, "no_rand": {}}
    for r in rows:
        if r["rendering"] != "chat" or r["layer"] != layer or r["reader"] != reader:
            continue
        if r["arm"] == "whole":
            out["whole"][r["scene"]] = r["switched"]
        elif r["arm"] in ("no_part", "no_rand") and (r["dict"], r["k"], r["omp"]) == X.MAIN:
            out[r["arm"]][r["scene"]] = r["switched"]
    return out


def measures(src: dict) -> dict:
    jdep, rdep = X.dependence(src["whole"], src["no_part"]), X.dependence(src["whole"], src["no_rand"])
    return {"S_whole": src["whole"], "Jdep": jdep, "Rdep": rdep, "excess": jdep - rdep}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cf", required=True)
    ap.add_argument("--single", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    runs = {"cf": a.cf, "single": a.single}
    pred = json.loads((X.RESULTS / a.single / "manifest.json").read_text())["predicted"]
    rows = {k: X.read_jsonl(X.RESULTS / r / "outcomes.jsonl") for k, r in runs.items()}
    ent = {r["scene"]: r["entity"] for rs in rows.values() for r in rs}
    blob = {"runs": runs, "layer": pred, "note": NOTE, "readers": {}}
    lines = [f"# Two-change vs single-change edit at layer {pred}: {a.cf} vs {a.single}", "",
             f"{NOTE} J++ k = 25 signed; bootstrap over bridge entities, {a.n_boot} resamples, seed {X.BOOT_SEED}. "
             "UNVERIFIED.", "",
             "| reader | items | n | entities | S_whole | Jdep | Rdep | excess |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    diffs = ["", "Paired differences on the shared items (single - two-change):", "",
             "| reader | n | S_whole | Jdep | Rdep | excess |", "|---|---|---|---|---|---|"]  # fmt: skip
    for w in X.READERS:
        arms = {k: arms_of(rs, pred, w) for k, rs in rows.items()}
        shared = sorted(set(arms["cf"]["whole"]) & set(arms["single"]["whole"]))
        out = {}
        for label, run, scenes in (("two-change, all", "cf", sorted(arms["cf"]["whole"])),
                                   ("two-change, shared", "cf", shared), ("single, shared", "single", shared),
                                   ("single, all", "single", sorted(arms["single"]["whole"]))):  # fmt: skip
            sw = {arm: [arms[run][arm][s] for s in scenes] for arm in ("whole", "no_part", "no_rand")}
            c = X.cell(sw, [ent[s] for s in scenes], a.n_boot)
            out[label] = c
            lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {label} | {c['n']} | {c['entities']} | "
                         f"{X.fmt3(c['S_whole'])} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} |")  # fmt: skip
        sw = {f"{run}/{arm}": [arms[run][arm][s] for s in shared] for run in runs for arm in ("whole", "no_part", "no_rand")}
        r = X.resampled_rates(sw, [ent[s] for s in shared], a.n_boot)
        point = {k: sum(v) / len(v) for k, v in sw.items()}
        m = {run: measures({arm: src[f"{run}/{arm}"] for arm in ("whole", "no_part", "no_rand")})
             for run, src in (("cf", point), ("single", point))}  # fmt: skip
        mr = {run: measures({arm: r[f"{run}/{arm}"] for arm in ("whole", "no_part", "no_rand")}) for run in runs}
        d = {k: [float(m["single"][k] - m["cf"][k]), *X.interval(mr["single"][k] - mr["cf"][k])] for k in mr["cf"]}
        out["paired_difference"] = {"n": len(shared), **d}
        diffs.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {len(shared)} | {X.fmt3(d['S_whole'])} | "
                     f"{X.fmt3(d['Jdep'])} | {X.fmt3(d['Rdep'])} | {X.fmt3(d['excess'])} |")  # fmt: skip
        blob["readers"][w] = out
    out_dir = X.RESULTS / a.single / f"paired-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out_dir.mkdir()
    (out_dir / "paired.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out_dir / "paired.md").write_text("\n".join(lines + diffs) + "\n")
    print("\n".join(lines + diffs))


if __name__ == "__main__":
    main()
