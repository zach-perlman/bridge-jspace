"""Figures for exp06_sigma_writes (part B), from a run's outcomes.

exp06_figures.py OUT_NAME RUN  -> figures/pre-sprint/exp06_sigma_writes/OUT_NAME/ (write-once)
    sigma_writes.png  per lens. Left: exp02's swap of the bridge with its J-part, with the matched-alignment direction
                      (the rest isotropic) and with the same direction's rest drawn from the activation covariance;
                      how often each flips the answer to the swap target (95% Wilson CI), next to its random-direction
                      null, with the median edit size and the share of answers kept. Right: exp03's start-line steering
                      along Σ_λ (v_S' - v_S) by λ (λ = 1 is the lens's own direction), at both sizes: how often the
                      answer becomes f(f(S')) and how often the original answer is kept.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes
from bridge_jspace.stats import wilson

EXP = "exp06_sigma_writes"
TITLE = {"jpp": "J++", "jlens": "J-lens"}
CONDITIONS = {  # condition -> (colour, label)
    "jpart": ("#3d8c5a", "J-part"),
    "jpart_matched": ("#8a3db8", "matched,\nisotropic rest"),
    "jpart_matched_sigma": ("#3b6fb6", "matched,\nΣ-shaped rest"),
}
SCALES = {0.03: ("#c07a2c", "3% of the norm"), 0.05: ("#6b6a65", "5% of the norm")}
CONTROL = "#b4b2a9"


def rate(rows: list[dict], field: str) -> tuple[float, float, float]:
    return wilson(sum(o[field] for o in rows), len(rows))


def figure(outcomes: list[dict], out: Path) -> None:
    lenses = [lens for lens in TITLE if any(o["lens"] == lens for o in outcomes)]
    pick = lambda **w: [o for o in outcomes if all(o.get(k) == v for k, v in w.items())]  # noqa: E731
    fig, axes = plt.subplots(len(lenses), 2, figsize=(12.4, 3.9 * len(lenses)), facecolor=SURFACE, squeeze=False)
    for row, lens in enumerate(lenses):
        ax = axes[row, 0]
        style_axes(ax)
        ticks = []
        for x, (condition, (colour, label)) in enumerate(CONDITIONS.items()):
            for offset, null in ((-0.2, False), (0.2, True)):
                rows = pick(task="matched", lens=lens, condition=condition, null=null)
                m, lo, hi = rate(rows, "flip")
                ax.bar(
                    x + offset,
                    100 * m,
                    width=0.38,
                    color=CONTROL if null else colour,
                    hatch="//" if null else None,
                    edgecolor=SURFACE,
                )
                yerr = [[100 * max(m - lo, 0)], [100 * max(hi - m, 0)]]  # Wilson's bound at 0 can round past m
                ax.errorbar(x + offset, 100 * m, yerr=yerr, color=INK, lw=1, capsize=2)
                if not null:
                    size = statistics.median(o["edit_ratio"] for o in rows)
                    kept = rate(rows, "kept_clean")[0]
                    note = f"edit {100 * size:.1f}%\nkept {100 * kept:.0f}%"
                    ax.text(x + offset, 100 * hi + 2, note, ha="center", va="bottom", fontsize=7.5, color=MUTED)
            ticks.append(label)
        ax.set_xticks(range(len(ticks)))
        ax.set_xticklabels(ticks, fontsize=8.5)
        ax.set_ylim(0, 100)
        ax.set_ylabel("answer flips to the swap target (%)", color=MUTED, fontsize=9)
        ax.set_title(f"{TITLE[lens]}: exp02's swap (n=77; hatched: random null)", loc="left", fontsize=10, color=INK)
        ax = axes[row, 1]
        style_axes(ax)
        lams = sorted({o["lam"] for o in pick(task="steer", lens=lens) if o["lam"] is not None}, reverse=True)
        xs = list(range(len(lams)))
        for scale, (colour, label) in SCALES.items():
            flips = [rate(pick(task="steer", lens=lens, lam=lam, scale=scale), "flip") for lam in lams]
            kept = [rate(pick(task="steer", lens=lens, lam=lam, scale=scale), "kept_clean")[0] for lam in lams]
            ax.plot(xs, [100 * f[0] for f in flips], color=colour, lw=1.8, marker="o", label=f"{label}: f(f(S'))")
            ax.fill_between(
                xs, [100 * f[1] for f in flips], [100 * f[2] for f in flips], color=colour, alpha=0.15, lw=0
            )
            ax.plot(xs, [100 * k for k in kept], color=colour, lw=1.2, ls="--", label=f"{label}: original answer kept")
            null = rate(pick(task="steer", lens=lens, null=True, scale=scale), "flip")[0]
            ax.axhline(100 * null, color=CONTROL, lw=1, ls=":")
        ax.set_xticks(xs)
        ax.set_xticklabels([f"λ = {lam:g}" + (" (lens)" if lam == 1 else "") for lam in lams], fontsize=8.5)
        ax.set_ylim(-3, 103)
        ax.set_ylabel("% of items", color=MUTED, fontsize=9)
        n = len({o["name"] for o in pick(task="steer", lens=lens)})
        ax.set_title(
            f"{TITLE[lens]}: start-line steering along Σ_λ(v_S' - v_S) (n={n}; dotted: random null)",
            loc="left",
            fontsize=10,
            color=INK,
        )
    fig.legend(*axes[0, 1].get_legend_handles_labels(), loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    fig.suptitle(
        "Writing along the activation covariance (Σ) instead of the lens's direction (edit: median share of the "
        "residual norm; kept: original answer kept)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(out / "sigma_writes.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    assert not out.exists(), f"{out} exists; figure folders are write-once"
    with open(results_root / EXP / run / "outcomes.jsonl") as f:
        outcomes = [json.loads(line) for line in f]
    out.mkdir(parents=True)
    figure(outcomes, out)
    (out / "sources.json").write_text(json.dumps({"runs": [run]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/pre-sprint/exp06_sigma_writes/ (write-once)")
    parser.add_argument("run", help="the exp06 run")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    parser.add_argument("--results-root", type=Path, default=pins.RESULTS_DIR, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.run, args.out_root, args.results_root)
