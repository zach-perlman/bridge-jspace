"""Figures for exp04_brew_patch (part B), from a patch_map run's outcomes.

exp04_figures.py OUT_NAME RUN  -> figures/exp04_brew_patch/OUT_NAME/ (write-once)
    patch_map.png   by layer, for each group of prompt positions: how often copying the counterfactual's activation
                    into the original run makes the model answer f(X) (X carried as the step), the counterfactual's
                    answer c, X itself, or keep the original answer; and how often the off-path control's patch
                    changes the answer at all
    patch_logp.png  the same patches, graded: mean log-probability of f(X) and of c at the first answer token,
                    minus that of the original answer
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

EXP = "exp04_brew_patch"
GROUPS = {  # group -> panel title
    "rule_path": "the start colour's rule line",
    "rules": "both changed rule lines",
    "start_line": '"The potion starts out S."',
    "after_start": "after the start line",
    "last": "the last token",
}
ROLES = [  # (role, colour, label)
    ("b", "#3d8c5a", "f(X): X carried as the step"),
    ("c", "#3b6fb6", "c: the counterfactual's answer"),
    ("X", "#8a3db8", "X itself"),
    ("A", "#6b6a65", "the original answer"),
]
CONTROL = "#b4b2a9"
SWAP_BAND = (8, 24)  # exp03's lens swaps of the intermediate (after the start line)


def by_cell(outcomes: list[dict]) -> dict[tuple[str, str, int], list[dict]]:
    cells: dict[tuple[str, str, int], list[dict]] = {}
    for o in outcomes:
        cells.setdefault((o["source"], o["group"], o["layer"]), []).append(o)
    return cells


def patch_map(cells: dict, layers: list[int], n_items: int, out: Path) -> None:
    fig, axes = plt.subplots(1, len(GROUPS), figsize=(3.3 * len(GROUPS), 3.6), sharey=True, facecolor=SURFACE)
    for ax, (group, title) in zip(axes, GROUPS.items(), strict=True):
        style_axes(ax)
        if group in ("start_line", "after_start", "last"):
            ax.axvspan(*SWAP_BAND, color="#f1efe8", lw=0, zorder=0)
        for role, colour, label in ROLES:
            w = [
                wilson(sum(o["role"] == role for o in cells["cf", group, layer]), len(cells["cf", group, layer]))
                for layer in layers
            ]
            ax.plot(layers, [100 * r[0] for r in w], color=colour, lw=1.8, label=label)
            if role in ("b", "c"):
                ax.fill_between(
                    layers, [100 * r[1] for r in w], [100 * r[2] for r in w], color=colour, alpha=0.15, lw=0
                )
        changed = [
            100 * sum(o["role"] != "A" for o in cells["off", group, layer]) / len(cells["off", group, layer])
            for layer in layers
        ]
        ax.plot(layers, changed, color=CONTROL, lw=1.4, ls="--", label="off-path control: answer changed")
        ax.set_title(title, loc="left", fontsize=10, color=INK)
        ax.set_xlabel("layer patched", color=MUTED, fontsize=9)
        ax.set_ylim(-3, 103)
    axes[0].set_ylabel("% of items", color=MUTED, fontsize=9)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", ncol=5, frameon=False, fontsize=8.5)
    fig.suptitle(
        f"Copy the counterfactual's activation (S -> X, X -> c) into the original run, one layer at a time (n={n_items}; "
        f"shaded: layers {SWAP_BAND[0]}-{SWAP_BAND[1]}, exp03's lens swaps)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(out / "patch_map.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def patch_logp(cells: dict, layers: list[int], n_items: int, out: Path) -> None:
    fig, axes = plt.subplots(1, len(GROUPS), figsize=(3.3 * len(GROUPS), 3.4), sharey=True, facecolor=SURFACE)
    for ax, (group, title) in zip(axes, GROUPS.items(), strict=True):
        style_axes(ax)
        for role, colour, label in ROLES[:2]:
            mean = [
                statistics.mean(o["logp"][role] - o["logp"]["A"] for o in cells["cf", group, layer]) for layer in layers
            ]
            ax.plot(layers, mean, color=colour, lw=1.8, label=f"log p({role}) - log p(A): {label}")
        control = [
            statistics.mean(o["logp"]["b"] - o["logp"]["A"] for o in cells["off", group, layer]) for layer in layers
        ]
        ax.plot(layers, control, color=CONTROL, lw=1.4, ls="--", label="off-path control, f(X)")
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_title(title, loc="left", fontsize=10, color=INK)
        ax.set_xlabel("layer patched", color=MUTED, fontsize=9)
    axes[0].set_ylabel("mean log-prob gap (nats)", color=MUTED, fontsize=9)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", ncol=3, frameon=False, fontsize=8.5)
    fig.suptitle(f"The same patches at the first answer token (n={n_items})", x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0.08, 1, 0.92))
    fig.savefig(out / "patch_logp.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    out.mkdir(parents=True, exist_ok=False)
    with open(results_root / EXP / run / "outcomes.jsonl") as f:
        outcomes = [json.loads(line) for line in f]
    cells = by_cell(outcomes)
    layers = sorted({o["layer"] for o in outcomes})
    n_items = len({o["name"] for o in outcomes})
    patch_map(cells, layers, n_items, out)
    patch_logp(cells, layers, n_items, out)
    (out / "sources.json").write_text(json.dumps({"runs": [run]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/exp04_brew_patch/ (write-once)")
    parser.add_argument("run", help="the exp04 patch_map run")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    parser.add_argument("--results-root", type=Path, default=pins.RESULTS_DIR, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.run, args.out_root, args.results_root)
