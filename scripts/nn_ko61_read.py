"""nn_ko61_read (Zach, 2026-10-30, prereg amendment 85 note 61): note 58 at windows holding an attention layer (Lightning) and at
the 9B's depth (27B), read (CPU).

Run (scripts/queues/h200_n61_1030.sh), per model prefix P: {P}jsuite_v4_test_chat_ko61_cand2_v1 (note 58's machinery and settings:
v4 draw 4001, note 37's gate, band, batch and cand2 read; paper10 and paper10_rot rerun) with darkperm_W and its calibrated midperm_W
at 3 windows (Lightning L24-27, L31-34, L17-20; 27B L19-22, L24-27, L28-31).
Readings:
  note 58's D1 and DD per window, unchanged (scripts/nn_ko58_read.main on this run, its lines printed as they are);
  per model: "lookup needs the dark space at an attention window" only if D1 holds at >= 1 window with Bonferroni-widened intervals
    (98.3% bootstrap CIs, 3 windows: the 0.83 and 99.17 percentiles of note 58's bridge bootstrap, 2000 draws, random.Random(0))
    for both of D1's inequalities (MP dark - mid >= 15, MP - MM under dark >= 10, each lower end > 0); the 95% reading beside;
  Lightning, given that: the attention window(s) pass while note 58's L27-30 / L28-31 failed (its stored {P}note58.json) = "Lightning's
    null was the window choice" (post hoc framing of a pre-registered test, labelled as such);
  if no window passes on either model (both models' note 61 JSONs present): "the crossover is specific to the 9B at the windows
    tested", and note 58 stays a 9B-only result.
Writes results/ablate_v2/nn_ko_read/{P}note61.json (or --out-dir) and prints the "reading ..." lines.

python scripts/nn_ko61_read.py RUN_DIR PREFIX [--out-dir DIR]   (as scripts/queues/h200_n61_1030.sh calls it; PREFIX "" for the 27B,
  nem35l_ for Lightning; RUN_DIR "-" for the default results/ablate_v2/{P}jsuite_v4_test_chat_ko61_cand2_v1)
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import io
import json
import random
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts import nn_ko58_read as N58  # noqa: E402
from scripts.nn_ko49_read import rows_at  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"
N_WINDOWS = 3
ATTENTION = {"nem35l_": {5, 12, 19, 26, 33, 42}}  # Lightning's attention layers (amendment 85); Qwen: every layer l with l % 4 == 3
MODELS = {"": "27b", "nem35l_": "nem35l", "qwen35_9b_": "9b"}


def boot_level(by: dict, fn, alpha: float, n: int = 2000) -> list | None:
    """nn_ko37_read.boot's bridge bootstrap (2000 draws, random.Random(0)) with a (1 - alpha) interval; alpha = 0.05 reproduces it."""
    keys, rng, out = sorted(by), random.Random(0), []
    for _ in range(n):
        v = fn([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
        if v == v:
            out.append(v)
    out.sort()
    return [round(out[int(alpha / 2 * len(out))], 1), round(out[int((1 - alpha / 2) * len(out)) - 1], 1)] if out else None


def attention_layers(P: str, layers: list[int]) -> list[int]:
    return [la for la in layers if (la in ATTENTION[P] if P in ATTENTION else la % 4 == 3)]


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
    d = run_dir or RES / "ablate_v2" / f"{P}{SET}_ko61_cand2_v1"
    tag = P or "27b_"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 61 {tag}: {d} missing")
        return out
    # note 58's reading on this run, unchanged (its JSON goes to a temporary directory, not over note 58's)
    with tempfile.TemporaryDirectory() as td:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r58 = N58.main(P, d, Path(td))
    print(buf.getvalue(), end="")
    out["note58_style"] = {"C1": r58.get("C1"), "readings": r58.get("readings"), "calibration": r58.get("calibration")}
    acc = rows_at(d)
    base = {f: acc.get((f, "none"), {}) for f in ("MP", "MM")}
    c1 = bool(r58.get("C1", {}).get("met"))
    windows = sorted({mm[1] for (_, c) in acc if (mm := re.fullmatch(r"darkperm_(L\d+-\d+)", c))}, key=lambda w: int(w[1:].split("-")[0]))
    if len(windows) != N_WINDOWS:
        print(f"  note 61 {tag}: {len(windows)} windows in the run (the Bonferroni factor stays {N_WINDOWS}, as registered)")
    alpha = 0.05 / N_WINDOWS
    W: dict = {}
    lines = []
    for w in windows:
        dk, md = f"darkperm_{w}", f"midperm_{w}"
        if ("MP", dk) not in acc or ("MP", md) not in acc:
            continue
        by1, by2 = collections.defaultdict(list), collections.defaultdict(list)
        for i, (ok, _) in base["MP"].items():
            if i in acc[("MP", dk)] and i in acc[("MP", md)]:
                by1[items[i]["bridge"]].append(int(ok) - int(acc[("MP", dk)][i][0]) - (int(ok) - int(acc[("MP", md)][i][0])))
        for f in ("MP", "MM"):
            for i, (ok, _) in base[f].items():
                if i in acc[(f, dk)]:
                    by2[items[i]["bridge"]].append((f, int(ok) - int(acc[(f, dk)][i][0])))
        u1 = [x for v in by1.values() for x in v]
        u2 = [x for v in by2.values() for x in v]
        neg_gap = lambda us: -K.gap_fn(us)  # noqa: E731
        s1, s2 = N58.mean100(u1), neg_gap(u2)
        rec = {"MP_dark_minus_mid": round(s1, 1), "MP_minus_MM_dark": round(s2, 1), "n_MP": len(u1), "n_MP_MM": len(u2)}
        for lvl, a in (("95", 0.05), ("bonf", alpha)):
            ci1, ci2 = boot_level(by1, N58.mean100, a), boot_level(by2, neg_gap, a)
            rec[f"ci1_{lvl}"], rec[f"ci2_{lvl}"] = ci1, ci2
            rec[f"D1_{lvl}"] = bool(s1 >= 15 and ci1 and ci1[0] > 0 and s2 >= 10 and ci2 and ci2[0] > 0)
        layers = list(range(int(w[1:].split("-")[0]), int(w.split("-")[1]) + 1))
        rec["attention_layers"] = attention_layers(P, layers)
        rec["mid_dim"] = r58.get("calibration", {}).get("windows", {}).get(w, {}).get("mid_dim")
        W[w] = rec
        lines.append(f"reading note61 D1 {w} {tag}: Bonferroni (98.3%) {'met' if rec['D1_bonf'] else 'not met'}, 95% {'met' if rec['D1_95'] else 'not met'} | "
                     f"MP dark - mid {rec['MP_dark_minus_mid']} 98.3% {rec['ci1_bonf']} 95% {rec['ci1_95']} (n MP {len(u1)}); "
                     f"MP - MM under dark {rec['MP_minus_MM_dark']} 98.3% {rec['ci2_bonf']} 95% {rec['ci2_95']} (n {len(u2)}); "
                     f"attention layers {rec['attention_layers']}; mid dim {rec['mid_dim']}")  # fmt: skip
    passing = [w for w, r in W.items() if r["D1_bonf"]]
    passing95 = [w for w, r in W.items() if r["D1_95"]]
    lab = ("lookup needs the dark space at an attention window" if passing else "no window passes (Bonferroni)")
    extra = ""
    if passing and P == "nem35l_":
        ref = RES / "ablate_v2" / "nn_ko_read" / f"{P}note58.json"
        r0 = json.loads(ref.read_text()).get("readings", {}) if ref.exists() else {}
        failed = [w for w in ("L27-30", "L28-31") if r0.get(w, {}).get("label") == "no dark-space lookup route on these models"]
        att = [w for w in passing if W[w]["attention_layers"]]
        if att and len(failed) == 2:
            extra = "; Lightning's null was the window choice (post hoc framing of a pre-registered test)"
        out["lightning_note58_windows_failed"] = failed
    out.update({"windows": W, "passing_bonferroni": passing, "passing_95": passing95, "label": lab + extra, "C1_met": c1,
                "double_dissociation_bonferroni": [w for w in passing if c1]})  # fmt: skip
    lines.append(f"reading note61 {MODELS.get(P, tag)}: {lab + extra!r} | passing windows (98.3%): {passing}; 95% beside: {passing95}; "
                 f"C1 {'met' if c1 else 'not met'} (double dissociation at {out['double_dissociation_bonferroni']})")
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note61.json").write_text(json.dumps(out, indent=1) + "\n")
    both = {p: od / f"{p}note61.json" for p in ("", "nem35l_")}
    if all(f.exists() for f in both.values()):
        any_pass = {p: bool(json.loads(f.read_text()).get("passing_bonferroni")) for p, f in both.items()}
        cross = ("the crossover is specific to the 9B at the windows tested (note 58 stays a 9B-only result)" if not any(any_pass.values())
                 else "a window passes on " + ", ".join(MODELS[p] for p, v in any_pass.items() if v))  # fmt: skip
        lines.append(f"reading note61 cross-model: {cross!r} | {any_pass}")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", help='the run directory ("-": the default for PREFIX)')
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, None if a.run_dir == "-" else Path(a.run_dir), a.out_dir)
