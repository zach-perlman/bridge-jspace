"""Draft report for an exp02_swaps run: a flip-rate chart (each condition next to its matched-norm null) and a
report in the AGENTS format with the mechanical checks filled in.

  report.py RUN   reads results/exp02_swaps/RUN/{manifest,summary}.json; writes
                  figures/exp02_swaps/RUN/flip_rates.png and results/exp02_swaps/analysis/RUN/REPORT_auto.md
                  (both write-once)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins  # noqa: E402

EXP = "exp02_swaps"


def pct(w) -> str:
    return f"{100 * w[0]:.0f}% [{100 * w[1]:.0f}, {100 * w[2]:.0f}]"


def plot(rates: dict, conditions: list[str], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    x = range(len(conditions))
    for ax, metric, title in ((axes[0], "flip", "swap answer at rank 1 (flip)"),
                              (axes[1], "kept_clean", "clean answer kept at rank 1")):
        for offset, null, color, label in ((-0.2, False, "tab:blue", "swap"),
                                           (0.2, True, "lightgray", "matched-norm random direction")):
            w = [rates[(c, null)][metric] for c in conditions]
            ax.bar([i + offset for i in x], [r[0] for r in w], width=0.4, color=color, label=label,
                   yerr=[[r[0] - r[1] for r in w], [r[2] - r[0] for r in w]], capsize=3)
        ax.set_xticks(list(x), conditions, rotation=20)
        ax.set_ylim(0, 1)
        ax.set_title(title)
    axes[0].set_ylabel(f"share of eligible items (n={rates[(conditions[0], False)]['n']}), Wilson 95% CI")
    axes[0].legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main(run: str) -> None:
    run_dir = pins.RESULTS_DIR / EXP / run
    manifest = json.loads((run_dir / "manifest.json").read_text())
    summary = json.loads((run_dir / "summary.json").read_text())
    fig_dir = pins.FIGURES_DIR / EXP / run
    report_dir = pins.RESULTS_DIR / EXP / "analysis" / run
    fig_dir.mkdir(parents=True, exist_ok=False)
    report_dir.mkdir(parents=True, exist_ok=False)

    conditions = manifest["conditions"]
    rates = {(r["condition"], r["null"]): r for r in summary["rates"]}
    plot(rates, conditions, fig_dir / "flip_rates.png")

    commit = subprocess.run(["git", "describe", "--always", "--dirty"], cwd=pins.REPO_ROOT,
                            capture_output=True, text=True).stdout.strip()
    n = rates[(conditions[0], False)]["n"]
    real, null = (lambda c: rates[(c, False)]), (lambda c: rates[(c, True)])
    boots = summary["paired_bootstraps"]
    lines = [
        f"EXP {EXP}/{run} @ {commit} | model {pins.QWEN_REPO}@{pins.QWEN_REVISION[:8]} | n={n} eligible items "
        f"(of 90: {summary['items']}) | band {manifest['bands'][0]} | seeds: null {manifest['null_seed']}, "
        "bootstrap 0",
        "Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the "
        "bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).",
        f"Headline: flip rate J-part = {pct(real('jpart')['flip'])}   remainder = {pct(real('remainder')['flip'])}"
        f"   remainder with J clamped = {pct(real('remainder_clamped')['flip'])}",
        "Paired differences (bootstrap B=2000): " + "; ".join(
            f"{k} = {100 * v[0]:+.0f} pts [{100 * v[1]:+.0f}, {100 * v[2]:+.0f}]" for k, v in boots.items()),
        f"Baseline: full probe = {pct(real('full_probe')['flip'])}   raw J-lens = {pct(real('raw_jlens')['flip'])}",
        "Control (matched-norm random direction): " + "   ".join(f"{c} = {pct(null(c)['flip'])}" for c in conditions),
        "Labels (J-part flip x clamped-remainder flip): " + ", ".join(f"{k} {v}" for k, v in summary["labels"].items()),
        f"Figures: figures/{EXP}/{run}/flip_rates.png",
        "Three dumbest ways this could be wrong:",
        "1) Any edit this large flips the answer. Checked: null flip rates above; null kept-clean rates "
        + ", ".join(f"{c} {pct(null(c)['kept_clean'])}" for c in conditions) + ".",
        "2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final "
        "position " + ", ".join(f"{c} {real(c)['edit_ratio_median']:.3f}" for c in conditions) + ".",
        "3) Flips come from breaking the computation, not from installing the target. Checked: share with neither "
        "answer at rank 1 " + ", ".join(f"{c} {100 * real(c)['neither']:.0f}%" for c in conditions)
        + "; items with skipped (near-parallel) layers "
        + ", ".join(f"{c} {real(c)['items_with_skipped_layers']}" for c in conditions) + ".",
        f"For the human to verify: results/{EXP}/{run}/labels.csv (one row per item; recompute each condition's "
        f"flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).",
        "Status: UNVERIFIED until a human adds it to VERIFIED.md",
    ]
    (report_dir / "REPORT_auto.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run")
    main(parser.parse_args().run)
