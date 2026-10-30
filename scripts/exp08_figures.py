"""Figures for exp08_brew_read (part B), from a run's reads.

exp08_figures.py OUT_NAME RUN  -> figures/pre-sprint/exp08_brew_read/OUT_NAME/ (write-once; loads the tokenizer for the labels)
    brew_read.png  fresh items, per lens reader (J++, the J-lens, the logit lens). Left: by layer, how often each role's
                   colour (the intermediate I, the distractor X, the start S, the answer A) is the top-1 of the 12
                   palette colours after the start line (over items and the 21 positions), with exp07's code as a
                   lens-free reader of I at the window (dots). Right: where, position by layer, I is the top-1
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
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes

EXP = "exp08_brew_read"
TITLE = {"jpp": "J++", "jlens": "J-lens", "logit": "logit lens"}
ROLE_STYLE = {  # role -> (colour, label)
    "I": ("#3d8c5a", "I, the intermediate"),
    "X": ("#b4b2a9", "X, the distractor"),
    "S": ("#3b6fb6", "S, the start colour"),
    "A": ("#c07a2c", "A, the answer"),
}
WINDOW = (36, 50)


def suffix_labels() -> list[str]:
    """The 21 tokens after the start line (the same in every item; exp07's check)."""
    from bridge_jspace.tokens import load_tokenizer
    from scripts.exp03_brew_swaps import ITEM_SETS
    from scripts.exp07_step_code import tokenized

    tokenizer = load_tokenizer()
    ids, positions = tokenized(tokenizer, ITEM_SETS["fresh"][2]()[0])
    return [repr(tokenizer.decode([ids[p]]))[1:-1] for p in positions]


def top1_share(rows: list[dict], role: str, layer: int, position: int | None = None) -> float:
    cells = [
        rank == 0
        for r in rows
        if r["layer"] == layer
        for p, rank in enumerate(r["colour_rank"][role])
        if position is None or p == position
    ]
    return statistics.mean(cells) if cells else float("nan")


def figure(rows: list[dict], labels: list[str], out: Path) -> None:
    fresh = [r for r in rows if r["set"] == "fresh"]
    readers = [reader for reader in TITLE if any(r["reader"] == reader for r in fresh)]
    n_items = len({r["name"] for r in fresh})
    code = [r for r in fresh if r["reader"] == "code"]
    fig, axes = plt.subplots(
        len(readers), 2, figsize=(14.5, 3.7 * len(readers)), facecolor=SURFACE, squeeze=False, width_ratios=(1, 1.3)
    )
    for row, reader in enumerate(readers):
        mine = [r for r in fresh if r["reader"] == reader]
        layers = sorted({r["layer"] for r in mine})
        ax = axes[row, 0]
        style_axes(ax)
        ax.axvspan(*WINDOW, color="#f1efe8", lw=0, zorder=0)
        for role, (colour, label) in ROLE_STYLE.items():
            ax.plot(
                layers, [100 * top1_share(mine, role, layer) for layer in layers], color=colour, lw=1.8, label=label
            )
        code_layers = sorted({r["layer"] for r in code})
        ax.plot(
            code_layers,
            [100 * top1_share(code, "I", layer) for layer in code_layers],
            color=ROLE_STYLE["I"][0],
            ls="",
            marker="o",
            ms=4,
            label="I, read by exp07's code (no lens)",
        )
        ax.axhline(100 / 12, color=MUTED, lw=0.8, ls=":")
        ax.set_ylim(-3, 103)
        ax.set_xlabel("layer", color=MUTED, fontsize=9)
        ax.set_ylabel("% top-1 of 12 colours", color=MUTED, fontsize=9)
        ax.set_title(f"{TITLE[reader]}: after the start line (shaded: the window)", loc="left", fontsize=10, color=INK)
        ax = axes[row, 1]
        grid = [[100 * top1_share(mine, "I", layer, p) for layer in layers] for p in range(len(labels))]
        image = ax.imshow(grid, aspect="auto", cmap="Greens", vmin=0, vmax=100, origin="upper")
        ax.set_xticks(range(0, len(layers), 2))
        ax.set_xticklabels([layers[i] for i in range(0, len(layers), 2)], fontsize=7.5)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=6.5)
        ax.set_xlabel("layer", color=MUTED, fontsize=9)
        ax.set_title(f"{TITLE[reader]}: I top-1 (%), position x layer", loc="left", fontsize=10, color=INK)
        fig.colorbar(image, ax=ax, fraction=0.03)
    fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="lower center", ncol=5, frameon=False, fontsize=8.5)
    fig.suptitle(
        f"Can the lens read brew's intermediate where the step is carried? (fresh items, n={n_items}; dotted: chance, "
        "1 in 12)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.96))
    fig.savefig(out / "brew_read.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    assert not out.exists(), f"{out} exists; figure folders are write-once"
    with open(results_root / EXP / run / "reads.jsonl") as f:
        rows = [json.loads(line) for line in f]
    labels = suffix_labels()
    out.mkdir(parents=True)
    figure(rows, labels, out)
    (out / "sources.json").write_text(json.dumps({"runs": [run]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/pre-sprint/exp08_brew_read/ (write-once)")
    parser.add_argument("run", help="the exp08 run")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    parser.add_argument("--results-root", type=Path, default=pins.RESULTS_DIR, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.run, args.out_root, args.results_root)
