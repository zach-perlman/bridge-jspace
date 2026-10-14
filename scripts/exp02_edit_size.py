"""exp02 edit-size check (part B): does a swap flip more because its edit is bigger?

  exp02_edit_size.py OUT_NAME [--runs JPP_RUN JLENS_RUN]  -> results/exp02_swaps/analysis/OUT_NAME/ (write-once)

From the runs' recorded outcomes only (no model): each swap's edit size is its recorded `edit_ratio`, |edit| / |h| at
the final position averaged over the band's layers (the edit is applied at every position from 1). Reports
  1. flip rate and median edit size per condition and lens (does the bigger edit flip more?);
  2. within each lens, whether the J-part swap's edit size separates the questions that flip from those that do not
     (AUC: the chance a flipped question's edit is bigger than a kept one's; 0.5 = no relation);
  3. J++ against the J-lens at matched edit size: both lenses' J-part swaps pooled, cut into edit-size quartiles,
     flip rate per lens inside each; the paired discordant counts (exact McNemar test); and the questions where
     J++'s edit is no bigger than the J-lens's.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.stats import wilson

EXP_DIR = pins.RESULTS_DIR / "exp02_swaps"
CONDITIONS = ("raw_jlens", "jpart", "full_probe", "remainder", "remainder_clamped")
LENSES = ("jpp", "jlens")


def pct(rate: tuple[float, float, float]) -> str:
    return f"{100 * rate[0]:.0f}% [{100 * rate[1]:.0f}, {100 * rate[2]:.0f}]"


def auc(pos: list[float], neg: list[float]) -> float:
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


def mcnemar_exact(b: int, c: int) -> float:
    n, k = b + c, min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n) if n else 1.0


def main(out_name: str, runs: dict[str, str]) -> None:
    out = EXP_DIR / "analysis" / out_name
    out.mkdir(parents=True, exist_ok=False)
    outcomes = {
        lens: [json.loads(line) for line in (EXP_DIR / run / "outcomes.jsonl").read_text().splitlines()]
        for lens, run in runs.items()
    }
    lines = [f"# exp02 edit size: {out_name}", "", f"Runs: {runs}. Edit size = `edit_ratio`: |edit| / |h| at the final position, mean over the band's "
             "layers.", ""]  # fmt: skip
    summary: dict = {"runs": runs, "conditions": [], "within_lens": {}, "quartiles": [], "paired": {}}

    lines += ["## 1. Flip rate and edit size per condition", ""]
    lines += ["| lens | condition | null | n | flip [95% CI] | edit ratio (median) |", "|---|---|---|---|---|---|"]
    for lens in LENSES:
        for cond in CONDITIONS:
            for null in (False, True):
                group = [o for o in outcomes[lens] if o["condition"] == cond and o["null"] == null]
                rate = wilson(sum(o["flip"] for o in group), len(group))
                edit = statistics.median(o["edit_ratio"] for o in group)
                summary["conditions"].append(
                    {"lens": lens, "condition": cond, "null": null, "n": len(group), "flip": rate, "edit": edit}
                )
                lines.append(f"| {lens} | {cond} | {'yes' if null else ''} | {len(group)} | {pct(rate)} | {edit:.4f} |")

    jpart = {
        lens: {o["name"]: o for o in outcomes[lens] if o["condition"] == "jpart" and not o["null"]} for lens in LENSES
    }
    lines += ["", "## 2. Within each lens: does the J-part edit's size predict a flip?", ""]
    lines += ["| lens | flipped: n, median edit | kept: n, median edit | AUC |", "|---|---|---|---|"]
    for lens in LENSES:
        flipped = [o["edit_ratio"] for o in jpart[lens].values() if o["flip"]]
        kept = [o["edit_ratio"] for o in jpart[lens].values() if not o["flip"]]
        a = auc(flipped, kept)
        summary["within_lens"][lens] = {"n_flipped": len(flipped), "n_kept": len(kept), "auc": a}
        lines.append(
            f"| {lens} | {len(flipped)}, {statistics.median(flipped):.4f} | {len(kept)}, "
            f"{statistics.median(kept):.4f} | {a:.2f} |"
        )

    lines += ["", "## 3. J++ against the J-lens at matched edit size (J-part swap)", ""]
    pool = sorted(((lens, o) for lens in LENSES for o in jpart[lens].values()), key=lambda t: t[1]["edit_ratio"])
    cuts = [round(len(pool) * q / 4) for q in range(5)]
    lines += ["| edit quartile | edit range | J++ flips | J-lens flips |", "|---|---|---|---|"]
    for q in range(4):
        part = pool[cuts[q] : cuts[q + 1]]
        row = {"quartile": q + 1, "edit_lo": part[0][1]["edit_ratio"], "edit_hi": part[-1][1]["edit_ratio"]}
        cells = []
        for lens in LENSES:
            group = [o for name, o in part if name == lens]
            row[lens] = wilson(sum(o["flip"] for o in group), len(group))
            cells.append(f"{sum(o['flip'] for o in group)}/{len(group)} ({pct(row[lens])})")
        summary["quartiles"].append(row)
        lines.append(f"| {q + 1} | {row['edit_lo']:.4f}-{row['edit_hi']:.4f} | {cells[0]} | {cells[1]} |")

    names = sorted(set(jpart["jpp"]) & set(jpart["jlens"]))
    pairs = [(jpart["jpp"][n], jpart["jlens"][n]) for n in names]
    only_jpp = sum(a["flip"] and not b["flip"] for a, b in pairs)
    only_jlens = sum(b["flip"] and not a["flip"] for a, b in pairs)
    ratios = [a["edit_ratio"] / b["edit_ratio"] for a, b in pairs]
    smaller = [(a, b) for a, b in pairs if a["edit_ratio"] <= b["edit_ratio"]]
    summary["paired"] = {
        "n": len(pairs),
        "flip_only_jpp": only_jpp,
        "flip_only_jlens": only_jlens,
        "mcnemar_exact_p": mcnemar_exact(only_jpp, only_jlens),
        "edit_ratio_jpp_over_jlens_median": statistics.median(ratios),
        "edit_ratio_jpp_over_jlens_quartiles": statistics.quantiles(ratios, n=4),
        "n_jpp_edit_not_bigger": len(smaller),
        "flips_there": {"jpp": sum(a["flip"] for a, _ in smaller), "jlens": sum(b["flip"] for _, b in smaller)},
    }
    p = summary["paired"]
    q1, _, q3 = p["edit_ratio_jpp_over_jlens_quartiles"]
    lines += [
        "",
        f"Paired over {p['n']} questions: flipped by J++ only {only_jpp}, by the J-lens only {only_jlens} "
        f"(exact McNemar p = {p['mcnemar_exact_p']:.2g}).",
        f"J++'s J-part edit over the J-lens's, per question: median {p['edit_ratio_jpp_over_jlens_median']:.2f} "
        f"(quartiles {q1:.2f}, {q3:.2f}).",
        f"Questions where J++'s edit is no bigger than the J-lens's: {p['n_jpp_edit_not_bigger']}; flips there: J++ "
        f"{p['flips_there']['jpp']}, J-lens {p['flips_there']['jlens']}.",
        "",
    ]
    (out / "report.md").write_text("\n".join(lines))
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("\n".join(lines))
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under results/exp02_swaps/analysis/ (write-once)")
    parser.add_argument("--runs", nargs=2, default=["main_v4_jpp", "main_v4_jlens"], metavar=("JPP_RUN", "JLENS_RUN"))
    args = parser.parse_args()
    main(args.out_name, dict(zip(LENSES, args.runs, strict=True)))
