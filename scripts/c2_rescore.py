"""c2_rescore: a CPU-only re-score of the write_max (C2) steering outcomes (review agent, 2026-10-24).

Reads results/write_max/<RUN>/outcomes.jsonl (and the old verdicts in results/write_max/c2_graded and c2_narrow) from
/workspace/bridge-jspace, read-only. Writes /workspace/scratch/c2_rescore/{rescore.json, rescore.md}. No model, no GPU.

RULE (fixed in this docstring before any re-scored number was computed or looked at):

Cells. The own lens direction writes (lens_add, lens_swap) at positions "question" / "final", any single layer or the
  joint band, any strength: the cell family of C2-graded and C2'.
Gate A (unchanged from c2_graded). The cell's matched-norm random control keeps the clean answer on >= 95% of the
  word's cases.
Gate B (new). The write's own breakage, the share of the word's cases whose top token is neither the clean answer nor
  C's ("other"), is <= 10%.
  A cell is eligible for a pair of words only if A and B pass on both words, each on all of that word's cases. Neither
  gate looks at flips to C's answer.
Pairs. (M->P, M->M) for C2-graded / C2-relative; (P->P, P->M) and (C->P, C->M) for C2'. Suite run: RL/RR and BL/BR.
Fixed-cell cross-validated estimate (one cell for both words of a pair):
  - split the pair's bridge entities at random into two halves;
  - on one half, pick the eligible cell that maximises the mean of the two words' flip rates (raw rates, not
    paste-normalised: several ceilings are near 0); ties go to the first cell in sorted order;
  - score both words at that cell on the other half, then swap the halves, so every case is scored once by a cell
    chosen without its bridge;
  - pool over 100 random splits.
  D = (recall word) - (lookup word) at the same cell, so the two words are paired.
Interval. 500 bootstrap resamples of bridge entities (multiplicity weights; the halves split unique bridges, so a
  resampled bridge never sits in both halves), 20 splits each; percentile 95% intervals for each word, D and the
  ratios.
Ceiling. Paste (copy) cells at question / final that really paste C's state:
  - single-layer copies always;
  - the joint copy only in runs at or after commit 1330338 (SetRows); earlier runs stacked it, so their joint copy is
    left out, unless a copy-only ceiling run on the same cases exists (27B wm2_full2_v2 -> wm2_full2_v2_ceiling);
  - chosen per word by the same half-split CV (best copy cell on one half, scored on the other), gate B applied.
Raw relative = the fixed cell's CV write / the CV ceiling, not capped at 1; a value > 1 (the write beats the "ceiling")
  is flagged.
Verdicts (re-scored, the original thresholds):
  - C2-graded*: MM >= 3 x MP and MM >= MP + 0.30 (CV, fixed cell), and D's 95% interval above 0.
  - C2-relative*: valid only if both CV ceilings are >= 0.5; holds if relative MM >= 0.5 and >= 3 x relative MP.
  - C2'*: for X in {P, C}, XM >= XP + 0.10, XM >= 3 x XP and D's interval above 0. HOLDS if both pass, PARTIAL if one,
    FAILS if neither; UNDERPOWERED if any of PP PM CP CM has < 30 cases.
  - If no cell passes both gates on a pair: NO CELL (the write cannot be measured without breaking > 10%).
Stacking. A joint lens_add cell adds alpha x |h_l| along unit(v_X - v_I)_l at every one of the band's n_L layers, and
  the residual carries each addition forward. The total added at the band's last layer, relative to |h| there:
  - is at most alpha x n_L (directions aligned, |h| non-decreasing over the band);
  - is about alpha x sqrt(n_L) if the per-layer directions were orthogonal.
  The logs hold neither the per-layer norms nor the cross-layer cosines, so only these two bounds are reported, next to
  the natural size of the top-1 J-lens component from results/removal_size, where that model has one. lens_swap's
  size depends on the data and is not logged: n/a.

python3 /workspace/scratch/c2_rescore.py [--splits 100] [--boot 500] [--boot-splits 20] [RUN ...]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import subprocess
import time
from pathlib import Path

import numpy as np

REPO = Path("/workspace/bridge-jspace")
WM = REPO / "results" / "write_max"
OUT = Path("/workspace/scratch/c2_rescore")
KEEP_GATE, BREAK_GATE = 0.95, 0.10
OWN, SITES = ("lens_add", "lens_swap"), ("question", "final")
RUNS = {  # model label -> runs (every two-step / suite steering run with outcomes; smoke, late-only and posctrl excluded)
    "Qwen3.6-27B": ["wm2_suite_v1", "wm2_ctrl_v1", "wm2_full2_v1", "wm2_full2_v2", "wm2_full2_aligned_v1"],
    "Qwen3-32B": ["qwen3_32b_wm2_full2_v1", "qwen3_32b_wm2_full2_aligned_v1"],
    "Muse Glimmer 30B": ["muse30_wm2_full2_v1", "muse30_wm2_full2_aligned_v1", "muse30_wm2_fresh2_v1"],
    "Qwen3.5-9B": ["qwen35_9b_wm2_full2_v1", "qwen35_9b_wm2_full2_aligned_v1", "qwen35_9b_wm2_fresh2_v1"],
    "Qwen3.5-122B-A10B": ["qwen35_122b_wm2_full2_v1", "qwen35_122b_wm2_full2_aligned_v1"],
    "Olmo-3-7B": ["olmo3d7_wm2_full2_v1", "olmo3d7_wm2_full2_aligned_v1"],
    "Olmo-Hybrid-7B": ["olmoh7_wm2_full2_v1", "olmoh7_wm2_full2_aligned_v1"],
    "gpt-oss-20b (our J++)": ["gptoss20_wm2_full2_v1", "gptoss20_wm2_full2_aligned_v1"],
    "gpt-oss-20b (J-lens)": ["gptoss20j_wm2_full2_v1", "gptoss20j_wm2_full2_aligned_v1"],
}
CEILING_FROM = {"wm2_full2_v2": "wm2_full2_v2_ceiling"}
REMOVAL_SIZE = {"qwen3.6-27b": "removal_size_v1", "qwen3-32b": "qwen3_32b_removal_size_v1",
                "muse-glimmer-30b": "muse30_removal_size_v1", "qwen3.5-9b": "qwen35_9b_removal_size_v1",
                "olmo-hybrid-7b": "olmoh7_removal_size_v1", "gpt-oss-20b": "gptoss20_removal_size_v1",
                "gpt-oss-20b-jlens": "gptoss20_removal_size_v1"}  # fmt: skip


def layer_key(la) -> int:
    return 10_000 if str(la) == "joint" else int(la)


def cell_sort(c: tuple) -> tuple:
    w, pos, la, s = c
    return (w, pos, layer_key(la), float(s))


def load(run: str) -> list[dict]:
    keep = ("family", "name", "bridge", "write", "pos", "layer", "strength", "control", "role")
    rows = []
    with open(WM / run / "outcomes.jsonl") as f:
        for line in f:
            r = json.loads(line)
            rows.append({k: r.get(k) for k in keep})
    return rows


def paste_fixed(run: str) -> bool:
    c = json.loads((WM / run / "manifest.json").read_text()).get("git_commit", "")
    rc = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", "1330338", c], capture_output=True).returncode
    return rc == 0


class Word:
    """Per word: cases, bridges, per-cell per-bridge counts of flips (b), others and cases; random-control keep rates."""

    def __init__(self, rows: list[dict]):
        self.cases = {}
        self.cells: dict = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))  # b, other, n
        self.ctrl: dict = collections.defaultdict(lambda: [0, 0])  # keepA, n
        for r in rows:
            self.cases[r["name"]] = r["bridge"]
            cell = (r["write"], r["pos"], str(r["layer"]), r["strength"])
            if r["control"]:
                k = self.ctrl[cell]
                k[0] += r["role"] == "A"
                k[1] += 1
            else:
                k = self.cells[cell][r["bridge"]]
                k[0] += r["role"] == "b"
                k[1] += r["role"] == "other"
                k[2] += 1
        self.n = len(self.cases)
        self.bridges = sorted(set(self.cases.values()))

    def rate(self, cell, idx: int) -> float:
        t = [sum(v[i] for v in self.cells[cell].values()) for i in (idx, 2)]
        return t[0] / t[1] if t[1] else float("nan")

    def gate_a(self, cell) -> bool:
        k = self.ctrl.get(cell)
        return bool(k and k[1] and k[0] / k[1] >= KEEP_GATE)

    def gate_b(self, cell) -> bool:
        return self.rate(cell, 1) <= BREAK_GATE  # module global; --break-gate 1.0 = sensitivity run without gate B

    def own_cells(self) -> list:
        return sorted((c for c in self.cells if c[0] in OWN and c[1] in SITES), key=cell_sort)

    def arrays(self, cells: list, bridges: list) -> tuple[np.ndarray, np.ndarray]:
        F = np.zeros((len(bridges), len(cells)))
        N = np.zeros((len(bridges), len(cells)))
        for j, c in enumerate(cells):
            for i, b in enumerate(bridges):
                v = self.cells[c].get(b)
                if v:
                    F[i, j], N[i, j] = v[0], v[2]
        return F, N


def rates(w: np.ndarray, F: np.ndarray, N: np.ndarray) -> np.ndarray:
    n = w @ N
    return np.where(n > 0, (w @ F) / np.maximum(n, 1e-12), 0.0)


def cv_pair(FX, NX, FY, NY, w, rng, splits):
    """Fixed-cell CV for a pair: (rate X, rate Y, pick counts)."""
    ub = np.nonzero(w > 0)[0]
    acc = np.zeros(4)
    picks: collections.Counter = collections.Counter()
    if len(ub) < 2:
        return float("nan"), float("nan"), picks
    for _ in range(splits):
        perm = rng.permutation(ub)
        h = len(perm) // 2
        for sel, ev in ((perm[:h], perm[h:]), (perm[h:], perm[:h])):
            ws = np.zeros_like(w)
            ws[sel] = w[sel]
            c = int(np.argmax((rates(ws, FX, NX) + rates(ws, FY, NY)) / 2))
            picks[c] += 1
            we = np.zeros_like(w)
            we[ev] = w[ev]
            acc += [we @ FX[:, c], we @ NX[:, c], we @ FY[:, c], we @ NY[:, c]]
    return acc[0] / max(acc[1], 1e-12), acc[2] / max(acc[3], 1e-12), picks


def cv_single(F, N, w, rng, splits):
    ub = np.nonzero((w > 0) & (N.sum(1) > 0))[0]
    if len(ub) < 2 or F.shape[1] == 0:
        return float("nan")
    acc = np.zeros(2)
    for _ in range(splits):
        perm = rng.permutation(ub)
        h = len(perm) // 2
        for sel, ev in ((perm[:h], perm[h:]), (perm[h:], perm[:h])):
            ws = np.zeros_like(w)
            ws[sel] = w[sel]
            c = int(np.argmax(rates(ws, F, N)))
            we = np.zeros_like(w)
            we[ev] = w[ev]
            acc += [we @ F[:, c], we @ N[:, c]]
    return acc[0] / max(acc[1], 1e-12)


def ci(xs: list[float]) -> list[float] | None:
    a = np.array([x for x in xs if x is not None and not math.isnan(x)])
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else None


def score_pair(words: dict, lo: str, hi: str, ceil_words: dict, joint_paste: bool, args, seed: int) -> dict:
    X, Y = words[lo], words[hi]
    cX, cY = X.own_cells(), Y.own_cells()
    common = [c for c in cX if c in set(cY)]
    survive = {w: {"own_cells": len(cs), "gate_A": sum(W.gate_a(c) for c in cs),
                   "gate_A_and_B": sum(W.gate_a(c) and W.gate_b(c) for c in cs)}
               for w, W, cs in ((lo, X, cX), (hi, Y, cY))}  # fmt: skip
    elig = [c for c in common if X.gate_a(c) and Y.gate_a(c) and X.gate_b(c) and Y.gate_b(c)]
    out = {"pair": [lo, hi], "n": {lo: X.n, hi: Y.n}, "bridges": len(set(X.bridges) | set(Y.bridges)),
           "cells_survive": survive, "eligible_pair_cells": len(elig)}  # fmt: skip
    # ceilings (per word, CV over its own copy cells)
    def copy_cells(W: Word) -> list:
        cs = [c for c in W.cells if c[0] == "copy" and c[1] in SITES and (c[2] != "joint" or joint_paste)]
        return sorted((c for c in cs if W.gate_b(c)), key=cell_sort)

    U = sorted(set(X.bridges) | set(Y.bridges))
    CW = {k: ceil_words[k] for k in (lo, hi)}
    cc = {k: copy_cells(W) for k, W in CW.items()}
    CA = {k: CW[k].arrays(cc[k], U) for k in (lo, hi)}
    out["ceiling_cells"] = {k: len(v) for k, v in cc.items()}
    out["ceiling_insample_max"] = {k: max((CW[k].rate(c, 0) for c in cc[k]), default=None) for k in (lo, hi)}
    if not elig:
        out["verdict_note"] = "NO CELL"
        rng = np.random.default_rng(seed)
        w1 = np.ones(len(U))
        out["ceiling_cv"] = {k: cv_single(*CA[k], w1, rng, args.splits) for k in (lo, hi)}
        return out
    FX, NX = X.arrays(elig, U)
    FY, NY = Y.arrays(elig, U)
    rng = np.random.default_rng(seed)
    w1 = np.ones(len(U))
    rX, rY, picks = cv_pair(FX, NX, FY, NY, w1, rng, args.splits)
    ceil = {k: cv_single(*CA[k], w1, rng, args.splits) for k in (lo, hi)}
    rel = {lo: rX / ceil[lo] if ceil[lo] else None, hi: rY / ceil[hi] if ceil[hi] else None}
    # in-sample cell (descriptive): chosen on all bridges
    j_in = int(np.argmax((rates(w1, FX, NX) + rates(w1, FY, NY)) / 2))
    mode, mode_n = picks.most_common(1)[0]
    boot = collections.defaultdict(list)
    rb = np.random.default_rng(seed + 1)
    for _ in range(args.boot):
        wb = rb.multinomial(len(U), np.ones(len(U)) / len(U)).astype(float)
        bx, by, _ = cv_pair(FX, NX, FY, NY, wb, rb, args.boot_splits)
        cb = {k: cv_single(*CA[k], wb, rb, args.boot_splits) for k in (lo, hi)}
        boot[lo].append(bx)
        boot[hi].append(by)
        boot["D"].append(by - bx)
        for k, v in ((lo, bx), (hi, by)):
            boot[f"rel_{k}"].append(v / cb[k] if cb[k] else None)
    cell_desc = lambda c: {"write": c[0], "pos": c[1], "layer": c[2], "strength": c[3]}  # noqa: E731
    out |= {
        "cv": {lo: rX, hi: rY, "D": rY - rX},
        "ci": {lo: ci(boot[lo]), hi: ci(boot[hi]), "D": ci(boot["D"]),
               f"rel_{lo}": ci(boot[f"rel_{lo}"]), f"rel_{hi}": ci(boot[f"rel_{hi}"])},  # fmt: skip
        "ceiling_cv": ceil,
        "relative_raw": rel,
        "relative_gt_1": [k for k, v in rel.items() if v is not None and v > 1],
        "cv_modal_cell": cell_desc(elig[mode]) | {"share_of_picks": mode_n / sum(picks.values())},
        "insample_cell": cell_desc(elig[j_in]) | {
            "rates": {lo: X.rate(elig[j_in], 0), hi: Y.rate(elig[j_in], 0)},
            "other": {lo: X.rate(elig[j_in], 1), hi: Y.rate(elig[j_in], 1)}},  # fmt: skip
        "eligible_joint_share": sum(c[2] == "joint" for c in elig) / len(elig),
    }
    return out


def old_verdicts(run: str) -> dict:
    g = WM / "c2_graded" / f"{run}.json"
    p = WM / "c2_graded" / f"{run}_paste.json"
    n = WM / "c2_narrow" / f"{run}.json"
    out: dict = {}
    if g.exists():
        d = json.loads(g.read_text())
        r = d.get("rule") or {}
        out["graded"] = None if not r else ("HOLDS" if r["C2_graded_holds"] else "FAILS")
        out["graded_nums"] = None if not r else {"mp_best": r["mp_best"], "mm_best": r["mm_best"]}
        rr = json.loads(p.read_text())["rule_relative"] if p.exists() else d.get("rule_relative")
        out["relative"] = rr and rr["verdict"]
        out["relative_nums"] = rr and {"ceiling": rr["ceiling"], "relative_capped": rr["relative"]}
        out["relative_source"] = "paste ceiling run" if p.exists() else "own run"
        out["own_best"] = {f: (v.get("own_direction") or {}).get("flips") for f, v in d["families"].items()}
    out["narrow"] = json.loads(n.read_text())["verdict"] if n.exists() else "not scored"
    return out


def stacking(run: str, target: str, cells: list[dict]) -> dict:
    m = json.loads((WM / run / "manifest.json").read_text())
    nl = len(m.get("band", []))
    nat = None
    rs = REMOVAL_SIZE.get(target)
    if rs and (REPO / "results" / "removal_size" / rs / "summary.json").exists():
        ms = json.loads((REPO / "results" / "removal_size" / rs / "summary.json").read_text())["median_share"]
        mid = m["band"][len(m["band"]) // 2] if m.get("band") else None
        if mid is not None:
            la = min(ms, key=lambda k: abs(int(k) - mid))
            nat = {"layer": int(la), "jlens_top1_median_share": ms[la].get("jlens_top1"), "source": rs}
    out = {"n_band_layers": nl, "natural_top1_share": nat, "cells": []}
    for c in cells:
        if c and c["layer"] == "joint" and c["write"] == "lens_add":
            a = float(c["strength"])
            out["cells"].append({**c, "alpha_per_layer": a, "stacked_upper": a * nl, "stacked_orthogonal": a * math.sqrt(nl)})
        elif c:
            note = ("lens_swap: size not logged (n/a)" if c["write"] == "lens_swap"
                    else "single layer: alpha x |h| added once")  # fmt: skip
            out["cells"].append({**c, "note": note})
    return out


def main(args) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    results = {"rule": (__doc__ or "").split("\n\n", 2)[2].split("\npython3")[0], "runs": {}}
    want = set(args.runs) if args.runs else None
    for model, runs in RUNS.items():
        for run in runs:
            if want and run not in want:
                continue
            rows = load(run)
            fams = sorted({r["family"] for r in rows})
            words = {f: Word([r for r in rows if r["family"] == f]) for f in fams}
            joint_paste = paste_fixed(run)
            ceil_words = words
            ceil_src = "own run" + ("" if joint_paste else " (single-layer pastes only: joint copy stacked)")
            if run in CEILING_FROM:
                crows = load(CEILING_FROM[run])
                ceil_words = {f: Word([r for r in crows if r["family"] == f]) for f in fams if any(r["family"] == f for r in crows)}
                for f in ceil_words:
                    assert set(ceil_words[f].cases) == set(words[f].cases), f"{CEILING_FROM[run]}: other {f} cases"
                joint_paste = paste_fixed(CEILING_FROM[run])
                ceil_src = CEILING_FROM[run]
            suite = "RR" in fams
            pairs = {"M": ("RL", "RR"), "P": ("BL", "BR")} if suite else {"M": ("MP", "MM"), "P": ("PP", "PM"), "C": ("CP", "CM")}
            target = json.loads((WM / run / "manifest.json").read_text())["model"]["target"]
            res = {"model": model, "target": target, "ceiling_source": ceil_src, "pairs": {}}
            # reproduce the old per-word best gated own-direction cell (gate A only), as a reading check
            res["old_best_reproduced"] = {}
            for f, W in words.items():
                cs = [c for c in W.own_cells() if W.gate_a(c)]
                res["old_best_reproduced"][f] = max((W.rate(c, 0) for c in cs), default=None)
            for i, (k, (lo, hi)) in enumerate(pairs.items()):
                if lo in words and hi in words:
                    res["pairs"][k] = score_pair(words, lo, hi, ceil_words, joint_paste, args, seed=1000 + i)
            res["old"] = old_verdicts(run)
            res["new"] = verdicts(res, suite)
            res["stacking"] = stacking(run, target, [p.get("cv_modal_cell") for p in res["pairs"].values()])
            results["runs"][run] = res
            print(f"{run}: done ({time.time() - t0:.0f}s) -> {res['new']}", flush=True)
    results["break_gate"] = BREAK_GATE
    tag = f"_{args.tag}" if args.tag else ""
    (OUT / f"rescore{tag}.json").write_text(json.dumps(clean(results), indent=2) + "\n")
    (OUT / f"rescore{tag}.md").write_text(markdown(results))
    print((OUT / f"rescore{tag}.md").read_text())


def clean(x):
    """NaN -> None, recursively (strict JSON)."""
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, float) and math.isnan(x):
        return None
    return x


def verdicts(res: dict, suite: bool) -> dict:
    P = res["pairs"]
    out: dict = {}
    m = P.get("M")
    if m is None:
        out["graded"] = out["relative"] = "n/a"
    elif "cv" not in m:
        out["graded"] = out["relative"] = "NO CELL"
    else:
        lo, hi = m["pair"]
        a, b = m["cv"][lo], m["cv"][hi]
        dci = m["ci"]["D"]
        out["graded"] = "HOLDS" if (b >= 3 * a and b >= a + 0.30 and dci and dci[0] > 0) else "FAILS"
        c = m["ceiling_cv"]
        valid = all(v is not None and not math.isnan(v) and v >= 0.5 for v in c.values())
        rl, rh = m["relative_raw"][lo], m["relative_raw"][hi]
        if not valid:
            out["relative"] = "inconclusive (ceiling < 0.5)"
        else:
            out["relative"] = "HOLDS" if (rh >= 0.5 and rh >= 3 * rl) else "FAILS"
    if suite:
        out["narrow"] = "n/a (no C words)"
        return out
    per = {}
    under = False
    for x in ("P", "C"):
        p = P.get(x)
        if p is None:
            per[x] = None
            continue
        under |= min(p["n"].values()) < 30
        if "cv" not in p:
            per[x] = "NO CELL"
            continue
        lo, hi = p["pair"]
        a, b = p["cv"][lo], p["cv"][hi]
        dci = p["ci"]["D"]
        per[x] = bool(b >= a + 0.10 and b >= 3 * a and dci and dci[0] > 0)
    if any(v is None for v in per.values()):
        out["narrow"] = "n/a"
    elif under:
        out["narrow"] = "UNDERPOWERED"
    else:
        k = sum(v is True for v in per.values())
        out["narrow"] = "HOLDS" if k == 2 else "PARTIAL" if k == 1 else "FAILS"
        if all(v == "NO CELL" for v in per.values()):
            out["narrow"] = "NO CELL"
    out["narrow_per_source"] = per
    return out


def markdown(results: dict) -> str:
    pct = lambda v: "-" if v is None or (isinstance(v, float) and math.isnan(v)) else f"{100 * v:.0f}"  # noqa: E731
    civ = lambda c: "" if not c else f" [{100 * c[0]:.0f}, {100 * c[1]:.0f}]"  # noqa: E731
    L = ["# C2 re-score (scripts: /workspace/scratch/c2_rescore.py; rule in its docstring)", "",
         "Fixed-cell cross-validated flips to C's answer (%), one cell per pair, chosen on half the bridges and scored "
         "on the other half, cells gated on random-control keep >= 95% AND own breakage <= 10%. "
         "[95% bootstrap over bridges]. D = recall word - lookup word at the same cell.", "",
         "| model | run | n MP/MM, PP/PM, CP/CM | eligible cells M/P/C | M->P vs M->M (D) | ceilings MP/MM; raw relative | "
         "P: PP vs PM (D) | C: CP vs CM (D) | C2-graded old -> new | C2-relative old -> new | C2' old -> new |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for run, r in results["runs"].items():
        P = r["pairs"]

        def ns(k):
            p = P.get(k)
            return "-" if not p else "/".join(str(v) for v in p["n"].values())

        def pr(k):
            p = P.get(k)
            if not p:
                return "-"
            if "cv" not in p:
                return "NO CELL"
            lo, hi = p["pair"]
            return f"{pct(p['cv'][lo])} vs {pct(p['cv'][hi])} (D {pct(p['cv']['D'])}{civ(p['ci']['D'])})"

        m = P.get("M") or {}
        if "cv" in m:
            lo, hi = m["pair"]
            rel = m["relative_raw"]
            flag = " **>1**" if m["relative_gt_1"] else ""
            f2 = lambda v: "-" if v is None or math.isnan(v) else f"{v:.2f}"  # noqa: E731
            cs = f"{pct(m['ceiling_cv'][lo])}/{pct(m['ceiling_cv'][hi])}; {f2(rel[lo])}/{f2(rel[hi])}{flag}"
        else:
            cs = "-"
        el = "/".join(str(P[k]["eligible_pair_cells"]) if k in P else "-" for k in ("M", "P", "C"))
        o, n = r["old"], r["new"]
        gn = o.get("graded_nums") or {}
        og = f"{o.get('graded')} ({pct(gn.get('mp_best'))}/{pct(gn.get('mm_best'))})"
        L.append(f"| {r['model']} | {run} | {ns('M')}, {ns('P')}, {ns('C')} | {el} | {pr('M')} | {cs} | {pr('P')} | "
                 f"{pr('C')} | {og} -> {n['graded']} | {o.get('relative')} -> {n['relative']} | "
                 f"{o.get('narrow')} -> {n['narrow']} |")  # fmt: skip
    L += ["", "## Cells surviving the gates (own lens direction cells at question/final, per word: total / gate A / A and B)", ""]
    for run, r in results["runs"].items():
        s = []
        for p in r["pairs"].values():
            for w, v in p["cells_survive"].items():
                s.append(f"{w} {v['own_cells']}/{v['gate_A']}/{v['gate_A_and_B']}")
        L.append(f"- {run}: " + ", ".join(s))
    L += ["", "## Stacked joint writes (modal CV cell per pair; bounds on the added norm / |h| at the band's last layer)", ""]
    for run, r in results["runs"].items():
        st = r["stacking"]
        nat = st["natural_top1_share"]
        parts = []
        for c in st["cells"]:
            if "stacked_upper" in c:
                parts.append(f"{c['write']} {c['pos']} joint a={c['alpha_per_layer']:g}: <= {c['stacked_upper']:.2f} (orthogonal {c['stacked_orthogonal']:.2f})")
            else:
                parts.append(f"{c['write']} {c['pos']} L{c['layer']} a={c['strength']:g}: {c['note']}")
        natv = f"; natural top-1 J share L{nat['layer']} {nat['jlens_top1_median_share']:.3f}" if nat else ""
        L.append(f"- {run} (n_L={st['n_band_layers']}{natv}): " + "; ".join(parts))
    L += ["", "## Reading check: old per-word best gated own-direction flips (c2_graded) vs recomputed here", ""]
    for run, r in results["runs"].items():
        ob = r["old"].get("own_best", {})
        mism = [f"{f} {pct(ob.get(f))} vs {pct(v)}" for f, v in r["old_best_reproduced"].items()
                if ob.get(f) is not None and v is not None and abs(ob[f] - v) > 1e-9]
        L.append(f"- {run}: " + ("all match" if not mism else "MISMATCH " + ", ".join(mism)))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="*")
    ap.add_argument("--splits", type=int, default=100)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--boot-splits", type=int, default=20)
    ap.add_argument("--break-gate", type=float, default=BREAK_GATE, help="sensitivity only (the rule is 0.10)")
    ap.add_argument("--tag", default="", help="output suffix for sensitivity runs")
    a = ap.parse_args()
    BREAK_GATE = a.break_gate
    main(a)
