"""Does the pointer result rest on the first sentence? (Dan 26 Oct ~14:30 / ~16:20; CPU, after the data, descriptive.)

The main test's pointer removal (x0_massmean: the 9B and 27B layout-free runs, the 122B and Muse grid runs, on their
one-change items), the items the whole change switches, split by where the original and the changed bridge's locker
sentences sit: (a) either is the context's first sentence; (b) either is the first locker sentence but not the first
sentence (a pick sentence comes before it); (c) neither. Per group and reader: n, the extra loss without the pointer
directions (switches lost without Alf minus lost without its random part, over the whole change's switches) and the
switch rate with only the pointer part (keep_Alf), with cluster-bootstrap intervals over bridge entities (10,000
resamples, seed 0). UNVERIFIED.

uv run python scripts/x0_first_sentence.py          # results/x0_massmean/first-sentence-<stamp>/
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X

RESULTS = X.RESULTS.parent / "x0_massmean"
RUNS = {"qwen3.5-9b": "qwen35_9b_x0_massmean_lf", "qwen3.6-27b": "x0_massmean_lf_27b",
        "qwen3.5-122b-a10b": "qwen35_122b_x0_massmean_grid", "muse-glimmer-30b": "muse30b_x0_massmean_grid"}  # fmt: skip
GROUPS = ("(a) first sentence", "(b) first locker, not first sentence", "(c) neither")


def group_of(case: dict) -> str:
    """Where the original and the changed bridge's locker sentences sit in the context."""
    sents = re.split(r"(?<=\.)\s+", case["context"])
    lockers = [i for i, s in enumerate(sents) if s.startswith("The locker of")]
    where = [next((i for i in lockers if re.search(rf"\b{re.escape(e)}\b", sents[i])), None)
             for e in (case["bridge"], case["cf_bridge"])]  # fmt: skip
    if 0 in where:
        return GROUPS[0]
    if lockers and lockers[0] in where:
        return GROUPS[1]
    return GROUPS[2]


def cell(rows: dict[str, dict], scenes: list[str], ent: dict[str, str], n_boot: int) -> dict:
    """Over these switched items: extra loss without Alf (vs its random part) and keep_Alf's switch rate."""
    sw = {a: [int(rows[s][a]["switched"]) for s in scenes] for a in ("whole", "no_Alf", "no_Alf_rand", "keep_Alf")}
    r = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
    ex = (np.array(sw["no_Alf_rand"]).mean() - np.array(sw["no_Alf"]).mean()) / np.array(sw["whole"]).mean()
    ex_r = (r["no_Alf_rand"] - r["no_Alf"]) / r["whole"]
    return {"n": len(scenes), "entities": len(set(ent[s] for s in scenes)), "extra_loss": [float(ex), *X.interval(ex_r)],
            "keep_alf": [float(np.mean(sw["keep_Alf"])), *X.interval(r["keep_Alf"])]}  # fmt: skip


def diff(rows: dict[str, dict], g1: list[str], g2: list[str], ent: dict[str, str], n_boot: int) -> dict:
    """Group 1 minus group 2 (extra loss without Alf; keep_Alf's switch rate), paired: one cluster resample of the bridge
    entities for both groups (seed 0)."""
    keys = sorted({ent[s] for s in g1 + g2})
    pick = np.random.default_rng(X.BOOT_SEED).integers(0, len(keys), size=(n_boot, len(keys)))

    def rates(scenes: list[str]) -> dict[str, np.ndarray]:
        e = np.array([keys.index(ent[s]) for s in scenes])
        cnt = np.bincount(e, minlength=len(keys)).astype(float)[pick].sum(1)
        out = {}
        for a in ("whole", "no_Alf", "no_Alf_rand", "keep_Alf"):
            x = np.bincount(e, weights=[float(rows[s][a]["switched"]) for s in scenes], minlength=len(keys))
            out[a] = x[pick].sum(1) / np.where(cnt > 0, cnt, np.nan)
        return out

    r1, r2 = rates(g1), rates(g2)
    ex = lambda r: (r["no_Alf_rand"] - r["no_Alf"]) / r["whole"]  # noqa: E731
    point = {k: cell(rows, g, ent, 1) for k, g in (("g1", g1), ("g2", g2))}
    return {"extra_loss": [point["g1"]["extra_loss"][0] - point["g2"]["extra_loss"][0], *X.interval(ex(r1) - ex(r2))],
            "keep_alf": [point["g1"]["keep_alf"][0] - point["g2"]["keep_alf"][0],
                         *X.interval(r1["keep_Alf"] - r2["keep_Alf"])]}  # fmt: skip


def main(n_boot: int = X.N_BOOT) -> Path:
    out = RESULTS / f"first-sentence-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    blob, lines = {"after_the_data": True, "groups": GROUPS}, [
        "# Does the pointer result rest on the first sentence? (after the data, descriptive)", "",
        "The main test's pointer removal on its one-change items, the items the whole change switches, by where the original "
        "and the changed bridge's locker sentences sit. Extra loss without the pointer directions (vs their random part) "
        "and the switch rate with only the pointer part; cluster bootstrap over bridge entities. UNVERIFIED.", "",
        "| model | reader | group | n | extra loss without the pointer | only the pointer part: switch rate |",
        "|---|---|---|---|---|---|"]  # fmt: skip
    for target, run in RUNS.items():
        m = json.loads((RESULTS / run / "manifest.json").read_text())
        cases = {
            c["scene"]: c for c in X.read_jsonl(X.RESULTS / m["single"] / "cases.jsonl") if c["rendering"] == "chat"
        }
        rows: dict = {}
        ent: dict = {}
        for r in X.read_jsonl(RESULTS / run / "outcomes.jsonl"):
            rows.setdefault(r["reader"], {}).setdefault(r["scene"], {})[r["arm"]] = r
            ent[r["scene"]] = r["entity"]
        blob[target] = {"run": run}
        for w in X.READERS:
            switched = [s for s, a in rows[w].items() if a["whole"]["switched"]]
            for g in GROUPS:
                mine = sorted(s for s in switched if group_of(cases[s]) == g)
                c = cell(rows[w], mine, ent, n_boot) if len({ent[s] for s in mine}) >= 2 else {"n": len(mine)}
                blob[target][f"{w}|{g}"] = c
                name = "lookup" if w == X.LOOKUP else "recall"
                if "extra_loss" in c:
                    lines.append(
                        f"| {target} | {name} | {g} | {c['n']} | {ci(c['extra_loss'])} | {ci(c['keep_alf'])} |"
                    )
                else:
                    lines.append(f"| {target} | {name} | {g} | {c['n']} | – | – |")
            by = {g: sorted(s for s in switched if group_of(cases[s]) == g) for g in GROUPS}
            for label, g2 in (("(a) − (b)", by[GROUPS[1]]), ("(a) − (b, c)", by[GROUPS[1]] + by[GROUPS[2]])):
                d = diff(rows[w], by[GROUPS[0]], g2, ent, n_boot)
                blob[target][f"{w}|{label}"] = d
                lines.append(
                    f"| {target} | {name} | **{label}**, paired | | {ci(d['extra_loss'])} | {ci(d['keep_alf'])} |"
                )
    (out / "first.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "first.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    main()
