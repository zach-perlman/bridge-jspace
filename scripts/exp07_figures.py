"""Figures for exp07_step_code (part B), from a run's outcomes and reads.

exp07_figures.py OUT_NAME RUN  -> figures/pre-sprint/exp07_step_code/OUT_NAME/ (write-once)
    step_code.png  per item set (fresh, bank). Left: every edit's step score (the share of window layers at which it
                   makes the model answer f(X), averaged over items, 95% bootstrap CI): the lens-free edits, then J++'s
                   and the J-lens's. Right: by layer, how often the main edits give f(X), and how often the code reads
                   the item's own intermediate from its activations (dotted)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes
from scripts.exp04_figures import step_score_ci

EXP = "exp07_step_code"
CONTROL = "#b4b2a9"
LENS_FREE = [  # (direction, dose, colour, label)
    ("copy", "copy", INK, "the copy (exp04)"),
    ("code", "copy", "#3d8c5a", "code"),
    ("random", "copy", CONTROL, "random"),
    ("code", "code", "#9cc9a8", "code, own size"),
    ("random", "code", "#d9d7cf", "random, code's size"),
]
PER_LENS = [  # (direction, colour, label)
    ("lens", "#8a3db8", "lens v_X - v_I"),
    ("sigma_0.5", "#3b6fb6", "Σ_0.5 (v_X - v_I)"),
    ("sigma_0.0", "#7fa3d6", "Σ (v_X - v_I)"),
    ("code_jspace", "#c07a2c", "code's J-space part"),
    ("code_rest", "#e0b47a", "code's rest"),
]
TITLE = {"jpp": "J++", "jlens": "J-lens"}
BY_LAYER = [  # (direction, dose, lens, colour, label)
    ("copy", "copy", None, INK, "the copy (exp04)"),
    ("code", "copy", None, "#3d8c5a", "code"),
    ("code", "code", None, "#9cc9a8", "code, own size"),
    ("lens", "copy", "jpp", "#8a3db8", "J++ lens v_X - v_I"),
    ("sigma_0.0", "copy", "jpp", "#7fa3d6", "J++ Σ (v_X - v_I)"),
    ("random", "copy", None, CONTROL, "random"),
]


def figure(outcomes: list[dict], reads: list[dict], out: Path) -> None:
    sets = [s for s in ("fresh", "bank") if any(o["set"] == s for o in outcomes)]
    layers = sorted({o["layer"] for o in outcomes})
    lenses = [lens for lens in TITLE if any(o["lens"] == lens for o in outcomes)]
    fig, axes = plt.subplots(
        len(sets), 2, figsize=(14.5, 4.6 * len(sets)), facecolor=SURFACE, squeeze=False, width_ratios=(1.6, 1)
    )
    for row, set_name in enumerate(sets):
        rows = [o for o in outcomes if o["set"] == set_name]
        n_items = len({o["name"] for o in rows})
        pick = lambda direction, dose, lens, rows=rows: [  # noqa: E731
            o for o in rows if (o["direction"], o["dose"], o["lens"]) == (direction, dose, lens)
        ]
        bars = [(pick(d, dose, None), colour, label) for d, dose, colour, label in LENS_FREE]
        for lens in lenses:
            bars += [(pick(d, "copy", lens), colour, f"{TITLE[lens]} {label}") for d, colour, label in PER_LENS]
        ax = axes[row, 0]
        style_axes(ax)
        for x, (cells, colour, _) in enumerate(bars):
            m, lo, hi = step_score_ci(cells)
            ax.bar(x, 100 * m, width=0.8, color=colour, edgecolor=SURFACE)
            yerr = [[100 * max(m - lo, 0)], [100 * max(hi - m, 0)]]
            ax.errorbar(x, 100 * m, yerr=yerr, color=INK, lw=1, capsize=2)
        for boundary in range(len(LENS_FREE), len(bars), len(PER_LENS)):
            ax.axvline(boundary - 0.5, color=MUTED, lw=0.6, ls=":")
        ax.set_xticks(range(len(bars)))
        ax.set_xticklabels([label for _, _, label in bars], rotation=40, ha="right", fontsize=8)
        ax.set_ylabel("step score (% of window layers giving f(X))", color=MUTED, fontsize=9)
        ax.set_title(
            f"{set_name} items (n={n_items}): every edit at the copy's size", loc="left", fontsize=10, color=INK
        )
        ax = axes[row, 1]
        style_axes(ax)
        for direction, dose, lens, colour, label in BY_LAYER:
            cells = pick(direction, dose, lens)
            share = [
                100
                * sum(o["role"] == "b" for o in cells if o["layer"] == L)
                / max(1, sum(o["layer"] == L for o in cells))
                for L in layers
            ]
            ax.plot(layers, share, color=colour, lw=1.8, label=f"{label}: f(X)")
        own = [r for r in reads if r["set"] == set_name]
        read = [
            100
            * sum(r["decoded"] == r["I"] for r in own if r["layer"] == L)
            / max(1, sum(r["layer"] == L for r in own))
            for L in layers
        ]
        ax.plot(layers, read, color="#3d8c5a", lw=1.2, ls=":", label="the code reads the item's own I")
        ax.set_ylim(-3, 103)
        ax.set_xlabel("layer edited (after the start line)", color=MUTED, fontsize=9)
        ax.set_ylabel("% of items", color=MUTED, fontsize=9)
        ax.set_title(f"{set_name} items: by layer", loc="left", fontsize=10, color=INK)
    fig.legend(*axes[0, 1].get_legend_handles_labels(), loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    fig.suptitle(
        "Does a code for the intermediate, fit on other items, write the step where the lens does not? (code: E_I[X] - "
        "E_I[I]; every edit as large as exp04's copy unless marked)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(out / "step_code.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def read_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def main(out_name: str, run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    assert not out.exists(), f"{out} exists; figure folders are write-once"
    run_dir = results_root / EXP / run
    outcomes, reads = read_jsonl(run_dir / "outcomes.jsonl"), read_jsonl(run_dir / "reads.jsonl")
    out.mkdir(parents=True)
    figure(outcomes, reads, out)
    (out / "sources.json").write_text(json.dumps({"runs": [run]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/pre-sprint/exp07_step_code/ (write-once)")
    parser.add_argument("run", help="the exp07 run")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    parser.add_argument("--results-root", type=Path, default=pins.RESULTS_DIR, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.run, args.out_root, args.results_root)
