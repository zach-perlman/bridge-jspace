"""paper_swap_read (prereg amendment 65, note 39): the readings A0-A4 of one paper_swap_decomp run, and the descriptive
splits. Pre-registered (note 39), per model, on the primary set (eligible items with a closed answer vocabulary, not in
the side table), primary lens (the frozen J++), primary read (first-token flip); r_X = arm X's flip rate, r_0 = arm 1's
matched-norm null at the same window:
  A0  r_1 - r_0 >= 0.30 at the main band, else the model's A readings are void.
  A1  (primary) at the main band and at the window of arm 1's median onset: K = (r_3 - r_0) / (r_1 - r_0);
      K <= 1/3 "answer-carried", K >= 2/3 "intermediate beyond the answer", else "partly"; valid only if arms 6 and 7
      keep >= 2/3 ((r_6 - r_0) / (r_1 - r_0) and the same for arm 7), otherwise "scrub not specific".
  A2  (r_4 - r_0) / (r_1 - r_0) <= 1/3 confirms A1; >= 1/3 while K <= 1/3: "non-answer content is causal but small".
  A3  "Frenchness is sufficient" if (r_5 - r_5null) / (r_1 - r_0) >= 2/3 at the main band.
  A4  onset = the smallest cumulative-window end at which an arm flips (per item). "The paper's timing replicates":
      median over items of onset(answer) - onset(bridge) >= 2 layers, cluster-bootstrap CI above 0, on items where both
      flip somewhere. "The timing lead is answer-category content": that, plus median onset(arm 5) - onset(arm 1) <= 1
      (items where both flip), plus r_3 <= r_0 + 0.10 in every cumulative window.
Intervals: cluster bootstrap over answer categories (the vocabulary's answer types; B = 2000, seed 0), percentile 95%.
Implementation choices (not in note 39's text, fixed here before any result): the median onset window is the
median_high of arm 1's onsets (an observed window end); arm 3's "null" is arm 1's (arm 3 has none of its own); A3 nets
arm 5 of its own null; A0 is read on the primary set (all eligible items beside it).
Descriptive: word vs number answers; low vs high bridge/answer overlap (exp14's cut: per item the cosine of the two pairs'
difference vectors, mean over main-band layers, split at the median); J++ vs the plain J-lens (27B); the side table and
own-pair-only items; the greedy check (criterion C) at the main band; |edit|/|h| and arm 1's share in span(A); flip_eq
(number twins accepted); the 27B's A0 reproduction against exp02.

python scripts/paper_swap_read.py results/paper_swap_decomp/<run> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.stats import wilson  # noqa: E402

VOCAB = Path(__file__).resolve().parents[1] / "data" / "paper_answer_types.json"
ARM_NO = {"bridge": 1, "answer": 2, "bridge_noA": 3, "bridge_noA_nm": 4, "bridge_onlyA": 5, "bridge_offA": 6,
          "bridge_randA": 7, "bridge_ownA": 8}  # fmt: skip


def load(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []


class Run:
    def __init__(self, run_dir: Path, n_boot: int, seed: int = 0):
        self.dir = run_dir
        self.manifest = json.loads((run_dir / "manifest.json").read_text())
        self.target = self.manifest["target"]
        self.rows = load(run_dir / "rows.jsonl")
        self.greedy = load(run_dir / "greedy.jsonl")
        self.items = load(run_dir / "items.jsonl")
        self.atoms = load(run_dir / "atoms.jsonl")
        vocab = json.loads(VOCAB.read_text())
        self.atype = {n: r["answer_type"] for n, r in vocab["items"].items()}
        self.wn = {n: r["word_or_number"] for n, r in vocab["items"].items()}
        self.flip = {(o["lens"], o["window"], o["arm"], o["null"], o["name"]): bool(o["flip"]) for o in self.rows}
        self.flip_eq = {(o["lens"], o["window"], o["arm"], o["null"], o["name"]): bool(o["flip_eq"]) for o in self.rows}
        self.sets = {o["name"]: o["set"] for o in self.rows}
        self.main = self.manifest["main_band"]
        self.cum = self.manifest["windows"]  # cumulative windows, in order
        self.end = {w: int(w.split("-")[1]) for w in self.cum}
        self.lenses = list(self.manifest["lenses"])
        self.n_boot, self.seed = n_boot, seed

    def names(self, which: str = "primary") -> list[str]:
        return sorted(n for n, s in self.sets.items() if which == "all" or s == which)

    def rate(self, lens, window, arm, null, names, table=None) -> float:
        t = table or self.flip
        v = [t[(lens, window, arm, null, n)] for n in names if (lens, window, arm, null, n) in t]
        return sum(v) / len(v) if v else math.nan

    def cluster_boot(self, names: list[str], stat) -> tuple[float, float, float, int]:
        """(point, lo, hi, n undefined draws): resample answer categories with replacement."""
        clusters: dict[str, list[str]] = {}
        for n in names:
            clusters.setdefault(self.atype[n], []).append(n)
        keys = sorted(clusters)
        point = stat(names)
        rng = np.random.default_rng(self.seed)
        vals, undefined = [], 0
        for _ in range(self.n_boot):
            draw = [n for k in rng.integers(0, len(keys), len(keys)) for n in clusters[keys[k]]]
            v = stat(draw)
            if v is None or (isinstance(v, float) and math.isnan(v)):
                undefined += 1
            else:
                vals.append(v)
        if not vals:
            return (point, math.nan, math.nan, undefined)
        lo, hi = np.percentile(vals, [2.5, 97.5])
        return (point, float(lo), float(hi), undefined)

    # statistics on a (multi)list of names
    def net(self, lens, window, arm, null_arm="bridge"):
        return lambda ns: self.rate(lens, window, arm, False, ns) - self.rate(lens, window, null_arm, True, ns)

    def ratio(self, lens, window, arm, num_null="bridge"):
        def f(ns):
            den = self.rate(lens, window, "bridge", False, ns) - self.rate(lens, window, "bridge", True, ns)
            num = self.rate(lens, window, arm, False, ns) - self.rate(lens, window, num_null, True, ns)
            return num / den if den > 0 else math.nan

        return f

    def onset(self, lens, arm, name) -> int | None:
        for w in self.cum:
            if self.flip.get((lens, w, arm, False, name)):
                return self.end[w]
        return None

    def median_onset_window(self, lens, names) -> str | None:
        ons = [o for n in names if (o := self.onset(lens, "bridge", n)) is not None]
        if not ons:
            return None
        m = statistics.median_high(ons)
        return next(w for w in self.cum if self.end[w] == m)

    def onset_diff(self, lens, arm_a, arm_b):
        """median over items (both flip somewhere) of onset(arm_a) - onset(arm_b)."""

        def f(ns):
            d = [oa - ob for n in ns if (oa := self.onset(lens, arm_a, n)) is not None and (ob := self.onset(lens, arm_b, n)) is not None]
            return float(statistics.median(d)) if d else math.nan

        return f


def label_k(k: float) -> str:
    if math.isnan(k):
        return "undefined (arm 1 not above its null)"
    return "answer-carried" if k <= 1 / 3 else "intermediate beyond the answer" if k >= 2 / 3 else "partly"


def readings(run: Run, lens: str, names: list[str]) -> dict:
    out: dict = {"lens": lens, "n_items": len(names), "n_categories": len({run.atype[n] for n in names})}
    m = run.main
    a0 = run.cluster_boot(names, run.net(lens, m, "bridge"))
    out["A0"] = {"window": m, "r1": run.rate(lens, m, "bridge", False, names), "r0": run.rate(lens, m, "bridge", True, names),
                 "r1_minus_r0": a0, "met": a0[0] >= 0.30,
                 "reading": "A0 met" if a0[0] >= 0.30 else "A0 NOT met: this model's A readings are void"}  # fmt: skip
    wstar = run.median_onset_window(lens, names)
    out["median_onset_window"] = wstar
    out["A1"], out["A2"] = {}, {}
    for tag, w in (("main_band", m), ("median_onset", wstar)):
        if w is None:
            out["A1"][tag] = {"window": None, "reading": "no item flips under arm 1 in any cumulative window"}
            continue
        K = run.cluster_boot(names, run.ratio(lens, w, "bridge_noA"))
        k6 = run.cluster_boot(names, run.ratio(lens, w, "bridge_offA"))
        k7 = run.cluster_boot(names, run.ratio(lens, w, "bridge_randA"))
        k4 = run.cluster_boot(names, run.ratio(lens, w, "bridge_noA_nm"))
        k8 = run.cluster_boot(names, run.ratio(lens, w, "bridge_ownA"))
        valid = not math.isnan(K[0]) and k6[0] >= 2 / 3 and k7[0] >= 2 / 3
        rates = {f"r{ARM_NO[a]}_{a}": run.rate(lens, w, a, False, names) for a in ARM_NO}
        rates.update({f"null_{a}": run.rate(lens, w, a, True, names) for a in ("bridge", "answer", "bridge_onlyA")})
        out["A1"][tag] = {"window": w, "rates": rates, "K": K, "keep_arm6": k6, "keep_arm7": k7, "keep_arm8_own": k8,
                          "valid": valid, "reading": label_k(K[0]) if valid else
                          f"scrub not specific (arm 6 keeps {k6[0]:.2f}, arm 7 keeps {k7[0]:.2f}; K = {K[0]:.2f} would read {label_k(K[0])!r})"}  # fmt: skip
        if math.isnan(k4[0]):
            a2 = "undefined"
        elif k4[0] <= 1 / 3:
            a2 = "arm 4 <= 1/3 of arm 1: confirms A1"
        elif K[0] <= 1 / 3:
            a2 = "non-answer content is causal but small (arm 4 >= 1/3 while arm 3 <= 1/3)"
        else:
            a2 = "arm 4 > 1/3 of arm 1 (and arm 3 > 1/3)"
        out["A2"][tag] = {"window": w, "arm4_over_arm1": k4, "reading": a2}
    a3 = run.cluster_boot(names, run.ratio(lens, m, "bridge_onlyA", num_null="bridge_onlyA"))
    a3raw = run.cluster_boot(names, run.ratio(lens, m, "bridge_onlyA"))
    out["A3"] = {"window": m, "arm5_net_over_arm1": a3, "arm5_over_arm1_with_arm1_null": a3raw,
                 "reading": "Frenchness is sufficient" if a3[0] >= 2 / 3 else "Frenchness not sufficient (arm 5 < 2/3 of arm 1)"}  # fmt: skip
    # A4: timing
    both = [n for n in names if run.onset(lens, "answer", n) is not None and run.onset(lens, "bridge", n) is not None]
    d21 = run.cluster_boot(both, run.onset_diff(lens, "answer", "bridge")) if both else (math.nan,) * 3 + (0,)
    on1 = [o for n in names if (o := run.onset(lens, "bridge", n)) is not None]
    on2 = [o for n in names if (o := run.onset(lens, "answer", n)) is not None]
    replicates = not math.isnan(d21[0]) and d21[0] >= 2 and d21[1] > 0
    both5 = [n for n in names if run.onset(lens, "bridge_onlyA", n) is not None and run.onset(lens, "bridge", n) is not None]
    d51 = run.cluster_boot(both5, run.onset_diff(lens, "bridge_onlyA", "bridge")) if both5 else (math.nan,) * 3 + (0,)
    excess3 = {w: run.rate(lens, w, "bridge_noA", False, names) - run.rate(lens, w, "bridge", True, names) for w in run.cum}
    arm3_quiet = all(v <= 0.10 for v in excess3.values() if not math.isnan(v))
    content = replicates and not math.isnan(d51[0]) and d51[0] <= 1 and arm3_quiet
    out["A4"] = {
        "n_both_flip": len(both), "median_paired_onset_answer_minus_bridge": d21,
        "median_onset_bridge": statistics.median(on1) if on1 else None, "median_onset_answer": statistics.median(on2) if on2 else None,
        "n_flip_somewhere": {"bridge": len(on1), "answer": len(on2)},
        "replicates": replicates, "n_both_flip_arm5_arm1": len(both5), "median_paired_onset_arm5_minus_arm1": d51,
        "arm3_minus_null_by_window": excess3, "arm3_never_above_null_plus_10": arm3_quiet,
        "reading": ("the paper's timing replicates" if replicates else "the paper's timing does not replicate")
        + ("; the timing lead is answer-category content" if content else ""),
    }  # fmt: skip
    return out


def window_table(run: Run, lens: str, names: list[str], table=None) -> list[dict]:
    out = []
    for w in [*run.cum, run.main]:
        row: dict = {"window": w, "main": w == run.main}
        for a in ARM_NO:
            row[f"{ARM_NO[a]}_{a}"] = run.rate(lens, w, a, False, names, table)
        for a in ("bridge", "answer", "bridge_onlyA"):
            row[f"null_{a}"] = run.rate(lens, w, a, True, names, table)
        out.append(row)
    return out


def split_rates(run: Run, lens: str, groups: dict[str, list[str]]) -> dict:
    out = {}
    for g, ns in groups.items():
        out[g] = {"n": len(ns), **{f"{ARM_NO[a]}_{a}": run.rate(lens, run.main, a, False, ns) for a in ARM_NO},
                  "null_bridge": run.rate(lens, run.main, "bridge", True, ns),
                  "K": run.ratio(lens, run.main, "bridge_noA")(ns) if ns else math.nan}  # fmt: skip
    return out


def descriptive(run: Run) -> dict:
    lens = run.lenses[0]
    P = run.names("primary")
    out: dict = {}
    out["by_word_or_number"] = split_rates(run, lens, {g: [n for n in P if run.wn[n] == g] for g in ("word", "number")})
    cos: dict = {}
    lo, hi = (int(x) for x in run.main.split("-"))
    for r in run.atoms:
        if r["lens"] == lens and lo <= r["layer"] <= hi:
            cos.setdefault(r["name"], []).append(r["diff_cosine"])
    mc = {n: statistics.mean(v) for n, v in cos.items() if n in P}
    if mc:
        cut = statistics.median(mc.values())
        out["by_overlap"] = {"cut": cut, **split_rates(run, lens, {"low": [n for n, c in mc.items() if c < cut], "high": [n for n, c in mc.items() if c >= cut]})}
    out["side_table"] = split_rates(run, lens, {"side_table": run.names("side_table")})
    out["own_pair_only"] = {"n": len(run.names("own_pair_only")),
                            **{f"{ARM_NO[a]}_{a}": run.rate(lens, run.main, a, False, run.names("own_pair_only")) for a in ("bridge", "answer", "bridge_ownA")},
                            "null_bridge": run.rate(lens, run.main, "bridge", True, run.names("own_pair_only"))}  # fmt: skip
    g: dict = {}
    for o in run.greedy:
        g.setdefault((o["lens"], o["arm"], o["null"], run.sets.get(o["name"], "?")), []).append(bool(o["flip"]))
    out["greedy_main_band"] = {f"{ln}/{a}{'/null' if nl else ''}/{s}": {"n": len(v), "flip": wilson(sum(v), len(v))}
                               for (ln, a, nl, s), v in sorted(g.items())}  # fmt: skip
    norms = {}
    for a in ARM_NO:
        rs = [o for o in run.rows if o["lens"] == lens and o["window"] == run.main and o["arm"] == a and not o["null"] and o["name"] in set(P)]
        if rs:
            med = lambda k: statistics.median([o[k] for o in rs if o.get(k) is not None and not math.isnan(o[k])] or [math.nan])  # noqa: E731
            norms[f"{ARM_NO[a]}_{a}"] = {"edit_ratio_edited_median": med("edit_ratio_edited"), "edit_ratio_last_median": med("edit_ratio_last"),
                                         "shareA_median": med("shareA"), "items_with_skipped_layers": sum(bool(o["layers_skipped"]) for o in rs),
                                         "dlogp_swap_mean": statistics.mean(o["dlogp_swap"] for o in rs)}  # fmt: skip
    out["edit_size_and_shareA_main_band"] = norms
    bin_ = [r for r in run.atoms if r["lens"] == lens and lo <= r["layer"] <= hi and r["name"] in set(P)]
    if bin_:
        out["bridge_atom_share_in_A_main_band_median"] = statistics.median(statistics.mean(r["bridge_in_A"]) for r in bin_)
        out["answer_atom_share_in_A_main_band_median"] = statistics.median(statistics.mean(r["answer_in_A"]) for r in bin_)
    out["flip_eq_main_band"] = {f"{ARM_NO[a]}_{a}": run.rate(lens, run.main, a, False, P, run.flip_eq) for a in ARM_NO}
    clean = [o for o in run.rows if o["arm"] == "clean" and o["window"] == run.main and o["lens"] == lens]
    out["clean_batched_read"] = {"n": len(clean), "answer_rank1": sum(o["kept"] for o in clean), "swap_rank1": sum(o["flip"] for o in clean)}
    if len(run.lenses) > 1:
        out["other_lenses"] = {ln: readings(run, ln, P) for ln in run.lenses[1:]}
    rp = run.dir / "repro.json"
    if rp.exists():
        out["A0_reproduction_vs_exp02"] = json.loads(rp.read_text())
    return out


def fmt(x) -> str:
    if isinstance(x, tuple | list) and len(x) >= 3 and all(isinstance(v, float | int) for v in x[:3]):
        return f"{x[0]:.2f} [{x[1]:.2f}, {x[2]:.2f}]"
    if isinstance(x, float):
        return f"{x:.2f}"
    return str(x)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    run = Run(Path(a.run_dir), a.boot)
    P = run.names("primary")
    statuses: dict = {}
    for r in run.items:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    res = {"run": str(run.dir), "target": run.target, "statuses": statuses, "primary_n": len(P),
           "readings": readings(run, run.lenses[0], P),
           "readings_all_eligible_A0": readings(run, run.lenses[0], run.names("all"))["A0"],
           "window_table_primary": window_table(run, run.lenses[0], P),
           "window_table_primary_dlogp_note": "flip rates; see rows.jsonl for delta log p",
           "descriptive": descriptive(run)}  # fmt: skip
    (run.dir / "reading.json").write_text(json.dumps(res, indent=2, default=str) + "\n")
    r = res["readings"]
    descriptive_only = run.target == "muse-glimmer-30b"
    print(f"# note 39 reading: {run.dir.name} ({run.target}{', DESCRIPTIVE ONLY' if descriptive_only else ''}); lens {r['lens']}; primary n {r['n_items']} in {r['n_categories']} categories; statuses {statuses}")
    print(f"reading A0: {r['A0']['reading']} (r1 {fmt(r['A0']['r1'])}, null {fmt(r['A0']['r0'])}, r1 - r0 {fmt(r['A0']['r1_minus_r0'])}); all eligible: {fmt(res['readings_all_eligible_A0']['r1_minus_r0'])}")
    for tag, v in r["A1"].items():
        if v.get("window") is None:
            print(f"reading A1 [{tag}]: {v['reading']}")
            continue
        print(f"reading A1 [{tag} {v['window']}]: {v['reading']} (K {fmt(v['K'])}; arm 6 keeps {fmt(v['keep_arm6'])}; arm 7 keeps {fmt(v['keep_arm7'])}; arm 8 keeps {fmt(v['keep_arm8_own'])})")
    for tag, v in r["A2"].items():
        print(f"reading A2 [{tag} {v['window']}]: {v['reading']} (arm 4 / arm 1 {fmt(v['arm4_over_arm1'])})")
    print(f"reading A3: {r['A3']['reading']} (arm 5 net / arm 1 net {fmt(r['A3']['arm5_net_over_arm1'])})")
    a4 = r["A4"]
    print(f"reading A4: {a4['reading']} (n both {a4['n_both_flip']}; median onset answer - bridge {fmt(a4['median_paired_onset_answer_minus_bridge'])}; "
          f"arm 5 - arm 1 {fmt(a4['median_paired_onset_arm5_minus_arm1'])}; arm 3 never above null + 10: {a4['arm3_never_above_null_plus_10']})")
    print("\nflip rates by window (primary set):")
    cols = list(res["window_table_primary"][0])
    print(" | ".join(cols))
    for row in res["window_table_primary"]:
        print(" | ".join(fmt(row[c]) for c in cols))
    d = res["descriptive"]
    if "A0_reproduction_vs_exp02" in d:
        rp = d["A0_reproduction_vs_exp02"]
        print(f"\nA0 reproduction vs exp02 main_v4_jpp (greedy, shared items): {json.dumps(rp['real'])}; reproduced {rp['reproduced']}")
    for ln, rr in d.get("other_lenses", {}).items():
        print(f"\n[{ln}] A0 {rr['A0']['reading']} ({fmt(rr['A0']['r1_minus_r0'])}); A1 main {rr['A1']['main_band'].get('reading')}; A3 {rr['A3']['reading']}; A4 {rr['A4']['reading']}")
    print("\ndescriptive (json): " + json.dumps({k: v for k, v in d.items() if k not in ("other_lenses", "A0_reproduction_vs_exp02")}, default=str)[:4000])


if __name__ == "__main__":
    main()
