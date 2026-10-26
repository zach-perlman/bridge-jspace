"""Duplicate check (Dan, 26 Oct ~21:45; descriptive, after the data; CPU only).

In the one-pick runs only the asked person's pick changes, to an item another person also picks, so the changed prompt
holds a duplicate. Each run's items are split by where that other person's pick sentence sits: BEFORE the asked pick
sentence, or AFTER it (then the bridge word cannot see the duplicate). Per group:
  - n;
  - the lookup's and the recall's J++ extra loss, and the gap (the x0 single runs: J++, k = 25, signed, at the layer
    fixed in advance);
  - the pointer's lookup extra loss (the 45g one-pick runs, all items; the first-sentence regroup's x0_massmean runs,
    the items both of whose locker sentences come before the asked pick).
Extra loss = (switches without the part's random part - switches without the part) / switches of the whole change.
Before minus after, with a cluster-bootstrap CI over bridge entities: the same draws for both groups (paired); 10,000
resamples, seed 0.

Reading (Dan): |before - after| < 0.1 with its CI covering 0: the duplicate does not matter. Otherwise every one-pick
number carries a caveat, and the clean design runs on Wednesday.

uv run python scripts/x45_duplicate.py      # results/x0_necessity/duplicate-<stamp>/{duplicate.json, duplicate.md}
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
from scripts import x0_strata as ST

MM = X.RESULTS.parent / "x0_massmean"
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "qwen3.5-122b-a10b", "muse-glimmer-30b")
SINGLE = {"qwen3.5-9b": "qwen35_9b_x0_single_r2", "qwen3.6-27b": "x0_single_27b_r2",
          "qwen3.5-122b-a10b": "qwen35_122b_x0_single", "muse-glimmer-30b": "muse30b_x0_single"}  # fmt: skip
G45_ONE = {"qwen3.5-9b": "qwen35_9b_x45g_one_r2", "qwen3.6-27b": "x45g_one_27b_r2",
           "qwen3.5-122b-a10b": "qwen35_122b_x45g_one", "muse-glimmer-30b": "muse30b_x45g_one"}  # fmt: skip
FIRST = {"qwen3.5-9b": "qwen35_9b_x0_massmean_lf", "qwen3.6-27b": "x0_massmean_lf_27b",
         "qwen3.5-122b-a10b": "qwen35_122b_x0_massmean_grid", "muse-glimmer-30b": "muse30b_x0_massmean_grid"}  # fmt: skip
GROUPS = ("before", "after")
PICK = re.compile(r"^([A-Z][a-z]+) picked (?:the )?(.+?)\.?$")
ASKED = re.compile(r"([A-Z][a-z]+)'s pick")
SMALL = 0.1  # Dan's "no difference": |diff| < 0.1 and the CI covering 0


def duplicate_side(case: dict) -> str:
    """Where the other person's pick of the changed item sits relative to the asked pick sentence: before / after;
    'none' if nobody else picks it (no duplicate)."""
    asked = ASKED.search(case["readers"][X.LOOKUP]["question"]).group(1)  # type: ignore[union-attr]
    picks = [(i, m.group(1), m.group(2)) for i, s in enumerate(re.split(r"(?<=\.) ", case["context"]))
             if (m := PICK.match(s.strip()))]  # fmt: skip
    me = next(i for i, who, _ in picks if who == asked)
    other = [i for i, who, item in picks if who != asked and item == case["cf_bridge"]]
    if not other:
        return "none"
    return "before" if other[0] < me else "after"


def boot_weights(entities: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> np.ndarray:
    """[n_boot, n_items]: each item's weight in each cluster-bootstrap draw (whole entities drawn with replacement,
    as X.resampled_rates draws them)."""
    keys = sorted(set(entities))
    ent = np.array([keys.index(e) for e in entities])
    pick = np.random.default_rng(seed).integers(0, len(keys), size=(n_boot, len(keys)))
    counts = np.zeros((n_boot, len(keys)))
    np.add.at(counts, (np.arange(n_boot)[:, None], pick), 1)
    return counts[:, ent]


def extra_loss(sw: dict[str, np.ndarray], w: np.ndarray, part: str, rand: str) -> np.ndarray:
    """(S_rand - S_part) / S_whole per weight row (w [..., n] over the items in sw's columns)."""
    whole = w @ sw["whole"]
    with np.errstate(divide="ignore", invalid="ignore"):
        return (w @ sw[rand] - w @ sw[part]) / np.where(whole > 0, whole, np.nan)


def interval(v: np.ndarray) -> list[float]:
    return [float(x) for x in np.nanpercentile(v, [2.5, 97.5])]


def measures(
    items: list[str],
    side: dict[str, str],
    sw: dict[str, dict[str, np.ndarray]],
    entities: list[str],
    parts: dict[str, tuple[str, str, str]],
    n_boot: int,
) -> dict:
    """Per group and measure (name -> (reader, part arm, random arm)) the extra loss with its CI, before minus after
    on the same draws, and n; 'gap' = recall minus lookup J++ when both are measured."""
    w = boot_weights(entities, n_boot)
    point = np.ones((1, len(items)))
    out: dict = {"n": {g: sum(side[s] == g for s in items) for g in (*GROUPS, "none")}, "cells": {}}
    vals: dict[str, dict[str, tuple[float, np.ndarray]]] = {}
    for name, (reader, part, rand) in parts.items():
        vals[name] = {}
        for g in GROUPS:
            mask = np.array([side[s] == g for s in items], dtype=float)
            vals[name][g] = (float(extra_loss(sw[reader], point * mask, part, rand)[0]),
                             extra_loss(sw[reader], w * mask, part, rand))  # fmt: skip
    if {"jpp_lookup", "jpp_recall"} <= set(vals):
        vals["gap"] = {g: (vals["jpp_recall"][g][0] - vals["jpp_lookup"][g][0],
                           vals["jpp_recall"][g][1] - vals["jpp_lookup"][g][1]) for g in GROUPS}  # fmt: skip
    for name, by in vals.items():
        diff = (by["before"][0] - by["after"][0], by["before"][1] - by["after"][1])
        lo, hi = interval(diff[1])
        out["cells"][name] = {**{g: [by[g][0], *interval(by[g][1])] for g in GROUPS}, "diff": [diff[0], lo, hi],
                              "no_difference": bool(abs(diff[0]) < SMALL and lo <= 0 <= hi)}  # fmt: skip
    return out


def table(rows: list[dict], items: list[str], arms: dict[str, list[str]]) -> dict[str, dict[str, np.ndarray]]:
    """reader -> arm -> 0/1 switched per item (in `items` order); every item must have every arm."""
    got = {(r["reader"], r["arm"], r["scene"]): int(r["switched"]) for r in rows}
    return {w: {a: np.array([got[(w, a, s)] for s in items], dtype=float) for a in arms[w]} for w in arms}


def single_run(run: str, n_boot: int) -> dict:
    """The x0 single run: J++ (k = 25, signed) at the layer fixed in advance, both readers."""
    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == m["predicted"]
            and (r["arm"] == "whole" or (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed"))]  # fmt: skip
    items = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    ent = {r["scene"]: r["entity"] for r in rows}
    side = {s: duplicate_side(cases[s]) for s in items}
    sw = table(rows, items, {w: ["whole", "no_part", "no_rand"] for w in X.READERS})
    parts = {"jpp_lookup": (X.LOOKUP, "no_part", "no_rand"), "jpp_recall": (X.RECALL, "no_part", "no_rand")}
    # beside Dan's split (agent, after the data): a duplicate before the asked pick also names the changed item before
    # the bridge word, so the same split within each place of the changed item's locker sentence
    alt_locker = {s: ST.features(cases[s])["alt locker vs asked pick"] for s in items}
    strata = {}
    for place in ("before", "after"):
        sub = [i for i, s in enumerate(items) if alt_locker[s] == place]
        sub_sw = {w: {a: v[sub] for a, v in arms.items()} for w, arms in sw.items()}
        strata[place] = measures([items[i] for i in sub], side, sub_sw, [ent[items[i]] for i in sub], parts, n_boot)
    return {"run": f"x0_necessity/{run}", "layer": m["predicted"],
            **measures(items, side, sw, [ent[s] for s in items], parts, n_boot), "by_alt_locker": strata}  # fmt: skip


def pointer_run(run: str, n_boot: int) -> dict | None:
    """An x0_massmean run on a single run's items: the pointer (Alf) removed against its random part, the lookup."""
    src = MM / run
    if not (src / "outcomes.jsonl").exists():
        return None
    m = json.loads((src / "manifest.json").read_text())
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / m["single"] / "cases.jsonl") if c["rendering"] == "chat"}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    ent = {r["scene"]: r["entity"] for r in rows}
    side = {s: duplicate_side(cases[s]) for s in items}
    sw = table(rows, items, {X.LOOKUP: ["whole", "no_Alf", "no_Alf_rand"]})
    return {"run": f"x0_massmean/{run}", "items_rule": m.get("items_rule"),
            **measures(items, side, sw, [ent[s] for s in items], {"pointer_lookup": (X.LOOKUP, "no_Alf", "no_Alf_rand")},
                       n_boot)}  # fmt: skip


def fmt(v: list[float]) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def main(n_boot: int = X.N_BOOT) -> Path:
    out = X.RESULTS / f"duplicate-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob: dict = {}
    lines = ["# Duplicate check: the other person's pick of the changed item before or after the asked pick", "",
             "Dan 26 Oct ~21:45; descriptive, after the data. One-pick runs only. Extra loss = (switches without the "
             "random part - switches without the part) / whole-change switches, per group; before - after on the same "
             f"cluster-bootstrap draws over bridge entities ({n_boot}, seed {X.BOOT_SEED}). 'no difference' = |diff| < "
             f"{SMALL} and the CI covering 0. UNVERIFIED.", "",
             "| model | run | measure | n before / after (none) | before | after | before - after | no difference |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for target in MODELS:
        got = [
            single_run(SINGLE[target], n_boot),
            pointer_run(G45_ONE[target], n_boot),
            pointer_run(FIRST[target], n_boot),
        ]
        blob[target] = [g for g in got if g is not None]
        for g in blob[target]:
            n = g["n"]
            for name, c in g["cells"].items():
                lines.append(f"| {target} | {g['run']} | {name} | {n['before']} / {n['after']} ({n['none']}) | "
                             f"{fmt(c['before'])} | {fmt(c['after'])} | {fmt(c['diff'])} | "
                             f"{'yes' if c['no_difference'] else '**no**'} |")  # fmt: skip
        if G45_ONE[target] not in {Path(g["run"]).name for g in blob[target]}:
            lines.append(f"| {target} | x0_massmean/{G45_ONE[target]} | pointer_lookup | not run yet | | | | |")
    lines += ["", "## Beside the split (agent, after the data): within each place of the changed item's locker sentence", "",
              "A duplicate before the asked pick also names the changed item before the bridge word. Within 'its locker "
              "sentence before the pick' the item is named earlier in both groups; within 'after', only the duplicate "
              "names it earlier. x0 single runs, J++ k = 25.", "",
              "| model | changed item's locker sentence | measure | n before / after | before | after | before - after |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for target in MODELS:
        for place, g in blob[target][0]["by_alt_locker"].items():
            for name, c in g["cells"].items():
                lines.append(f"| {target} | {place} the pick | {name} | {g['n']['before']} / {g['n']['after']} | "
                             f"{fmt(c['before'])} | {fmt(c['after'])} | {fmt(c['diff'])} |")  # fmt: skip
    (out / "duplicate.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "duplicate.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    main()
