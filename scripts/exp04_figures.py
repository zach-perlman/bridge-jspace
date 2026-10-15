"""Figures for exp04_brew_patch (part B), from a patch_map run's outcomes.

exp04_figures.py OUT_NAME RUN  -> figures/exp04_brew_patch/OUT_NAME/ (write-once)
    patch_map.png   by layer, for each group of prompt positions: how often copying the counterfactual's activation
                    into the original run makes the model answer f(X) (X carried as the step), the counterfactual's
                    answer c, X itself, the original intermediate I (one step instead of two), or keep the original
                    answer; and how often the off-path control's patch changes the answer at all
    patch_logp.png  the same patches, graded: mean log-probability of f(X) and of c at the first answer token,
                    minus that of the original answer
  exp04_figures.py OUT_NAME RUN  (a patch_parts run, exp04_brew_parts.py)
    parts.png       per lens: the step score (the share of window layers at which a copy gives f(X), averaged over
                    items, 95% bootstrap CI) of the full copy and of each part, next to each part's random-direction
                    null; and by layer, how often each part's copy gives f(X) and how often it gives X itself
  exp04_figures.py OUT_NAME RUN  (a patch_positions run, exp04_brew_positions.py)
    positions.png   per item set: the step score of the copy at each group of positions after the start line (and of
                    the off-path control's copy there), and by layer how often each group's copy gives f(X)
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
    ("I", "#c07a2c", "I: the original intermediate"),
    ("A", "#6b6a65", "the original answer"),
]
CONTROL = "#b4b2a9"
SWAP_BAND = (8, 24)  # exp03's lens swaps of the intermediate (after the start line)


def by_cell(outcomes: list[dict]) -> dict[tuple[str, str, int], list[dict]]:
    cells: dict[tuple[str, str, int], list[dict]] = {}
    for o in outcomes:
        cells.setdefault((o["source"], o["group"], o["layer"]), []).append(o)
    return cells


def drawn_groups(cells: dict) -> dict[str, str]:
    """The groups patched at two layers or more (a run can patch the rule lines at layer 0 only)."""
    return {g: t for g, t in GROUPS.items() if len({k[2] for k in cells if k[0] == "cf" and k[1] == g}) >= 2}


def patch_map(cells: dict, layers: list[int], n_items: int, out: Path) -> None:
    groups = drawn_groups(cells)
    wide = len(groups) >= 4  # a narrow figure (a run that patches the rule lines at layer 0 only) wraps its text
    fig, axes = plt.subplots(
        1,
        len(groups),
        figsize=(max(3.3 * len(groups), 9.0), 3.6 if wide else 4.2),
        sharey=True,
        facecolor=SURFACE,
        squeeze=False,
    )
    axes = axes[0]
    for ax, (group, title) in zip(axes, groups.items(), strict=True):
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
    fig.legend(
        *axes[0].get_legend_handles_labels(), loc="lower center", ncol=6 if wide else 3, frameon=False, fontsize=8.5
    )
    fig.suptitle(
        "Copy the counterfactual's activation (S -> X, X -> c) into the original run, one layer at a time"
        f"{' ' if wide else chr(10)}(n={n_items}; shaded: layers {SWAP_BAND[0]}-{SWAP_BAND[1]}, exp03's lens swaps)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94) if wide else (0, 0.13, 1, 0.87))
    fig.savefig(out / "patch_map.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def patch_logp(cells: dict, layers: list[int], n_items: int, out: Path) -> None:
    groups = drawn_groups(cells)
    fig, axes = plt.subplots(
        1, len(groups), figsize=(max(3.3 * len(groups), 9.0), 3.4), sharey=True, facecolor=SURFACE, squeeze=False
    )
    axes = axes[0]
    for ax, (group, title) in zip(axes, groups.items(), strict=True):
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


PART_STYLE = {  # part -> (colour, label)
    "full": (INK, "the whole copy"),
    "lens2": ("#8a3db8", "its I/X lens coordinates"),
    "not_lens2": ("#c9a3e0", "all but those"),
    "jspace": ("#3d8c5a", "its J-space part (25 atoms)"),
    "not_jspace": ("#9cc9a8", "all but that"),
}


def step_score_ci(outcomes: list[dict], n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """Mean over items of each item's share of layers answering f(X), with a percentile bootstrap CI over items."""
    import numpy as np

    by_item: dict[str, list[bool]] = {}
    for o in outcomes:
        by_item.setdefault(o["name"], []).append(o["role"] == "b")
    scores = np.array([np.mean(v) for v in by_item.values()])
    rng = np.random.default_rng(seed)
    boots = scores[rng.integers(0, len(scores), size=(n_boot, len(scores)))].mean(1)
    return float(scores.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def parts_figure(outcomes: list[dict], out: Path) -> None:
    lenses = [lens for lens in ("jpp", "jlens") if any(o["lens"] == lens for o in outcomes)]
    title = {"jpp": "J++", "jlens": "J-lens"}
    layers = sorted({o["layer"] for o in outcomes})
    n_items = len({o["name"] for o in outcomes})
    pick = lambda **w: [o for o in outcomes if all(o[k] == v for k, v in w.items())]  # noqa: E731
    fig, axes = plt.subplots(2, len(lenses), figsize=(6.2 * len(lenses), 7.4), facecolor=SURFACE)
    for col, lens in enumerate(lenses):
        ax = axes[0, col]
        style_axes(ax)
        bars = [("full", pick(part="full", source="cf"), False)]
        for part in ("lens2", "not_lens2", "jspace", "not_jspace"):
            bars += [
                (part, pick(lens=lens, part=part, null=False), False),
                (part, pick(lens=lens, part=part, null=True), True),
            ]
        for x, (part, rows, null) in enumerate(bars):
            m, lo, hi = step_score_ci(rows)
            colour, _ = PART_STYLE[part]
            ax.bar(
                x,
                100 * m,
                color=CONTROL if null else colour,
                width=0.8,
                hatch="//" if null else None,
                edgecolor=SURFACE,
            )
            ax.errorbar(x, 100 * m, yerr=[[100 * (m - lo)], [100 * (hi - m)]], color=INK, lw=1, capsize=2)
        ax.set_xticks(range(len(bars)))
        ax.set_xticklabels(
            [("null" if null else PART_STYLE[part][1]) for part, _, null in bars], rotation=35, ha="right", fontsize=8
        )
        ax.set_ylabel("step score (% of window layers giving f(X))", color=MUTED, fontsize=9)
        ax.set_title(f"{title[lens]}: copy only a part of δ = h_C - h_B", loc="left", fontsize=10, color=INK)
        ax = axes[1, col]
        style_axes(ax)
        for part, (colour, label) in PART_STYLE.items():
            rows = pick(part="full", source="cf") if part == "full" else pick(lens=lens, part=part, null=False)
            b = [
                100
                * sum(o["role"] == "b" for o in rows if o["layer"] == L)
                / max(1, sum(o["layer"] == L for o in rows))
                for L in layers
            ]
            xs = [
                100
                * sum(o["role"] == "X" for o in rows if o["layer"] == L)
                / max(1, sum(o["layer"] == L for o in rows))
                for L in layers
            ]
            ax.plot(layers, b, color=colour, lw=1.8, label=f"{label}: f(X)")
            if part != "full":
                ax.plot(layers, xs, color=colour, lw=1.0, ls=":", label=f"{label}: X itself")
        ax.set_title(f"{title[lens]}: by layer", loc="left", fontsize=10, color=INK)
        ax.set_xlabel("layer copied (after the start line)", color=MUTED, fontsize=9)
        ax.set_ylabel("% of items", color=MUTED, fontsize=9)
        ax.set_ylim(-3, 103)
    fig.legend(*axes[1, 0].get_legend_handles_labels(), loc="lower center", ncol=3, frameon=False, fontsize=8)
    fig.suptitle(
        f"Which part of the window's copy carries the intermediate? (n={n_items}; hatched: the part's matched-norm "
        "random direction)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.09, 1, 0.95))
    fig.savefig(out / "parts.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


POSITION_STYLE = {  # group -> (colour, label)
    "all": (INK, "all 21 positions (exp04's copy)"),
    "reading": ("#3d8c5a", "the 4 where the lens reads I"),
    "all_but_reading": ("#9cc9a8", "the other 17"),
    "assistant_nl": ("#3b6fb6", 'the newline after "assistant"'),
    "think_nl": ("#c07a2c", 'the "\\n\\n" after "</think>"'),
}


def positions_figure(outcomes: list[dict], out: Path) -> None:
    sets = [s for s in ("fresh", "bank") if any(o["set"] == s for o in outcomes)]
    layers = sorted({o["layer"] for o in outcomes})
    fig, axes = plt.subplots(
        len(sets), 2, figsize=(13.5, 4.3 * len(sets)), facecolor=SURFACE, squeeze=False, width_ratios=(1.25, 1)
    )
    for row, set_name in enumerate(sets):
        rows = [o for o in outcomes if o["set"] == set_name]
        pick = lambda g, s, rows=rows: [o for o in rows if (o["group"], o["source"]) == (g, s)]  # noqa: E731
        bars = []
        for group, (colour, label) in POSITION_STYLE.items():
            bars.append((pick(group, "cf"), colour, label, False))
            if pick(group, "off"):
                bars.append((pick(group, "off"), CONTROL, "off-path control", True))
        ax = axes[row, 0]
        style_axes(ax)
        for x, (cells, colour, _, null) in enumerate(bars):
            m, lo, hi = step_score_ci(cells)
            ax.bar(x, 100 * m, width=0.8, color=colour, hatch="//" if null else None, edgecolor=SURFACE)
            ax.errorbar(x, 100 * m, yerr=[[100 * max(m - lo, 0)], [100 * max(hi - m, 0)]], color=INK, lw=1, capsize=2)
        ax.set_xticks(range(len(bars)))
        ax.set_xticklabels([label for _, _, label, _ in bars], rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("step score (% of window layers giving f(X))", color=MUTED, fontsize=9)
        n_items = len({o["name"] for o in rows})
        ax.set_title(
            f"{set_name} items (n={n_items}): copy C at some positions only", loc="left", fontsize=10, color=INK
        )
        ax = axes[row, 1]
        style_axes(ax)
        for group, (colour, label) in POSITION_STYLE.items():
            cells = pick(group, "cf")
            share = [100 * statistics.mean(o["role"] == "b" for o in cells if o["layer"] == L) for L in layers]
            ax.plot(layers, share, color=colour, lw=1.8, label=label)
        ax.set_ylim(-3, 103)
        ax.set_xlabel("layer copied", color=MUTED, fontsize=9)
        ax.set_ylabel("% of items giving f(X)", color=MUTED, fontsize=9)
        ax.set_title(f"{set_name} items: by layer", loc="left", fontsize=10, color=INK)
    fig.legend(*axes[0, 1].get_legend_handles_labels(), loc="lower center", ncol=5, frameon=False, fontsize=8.5)
    fig.suptitle(
        "Which positions after the start line carry the step? (hatched: the off-path counterfactual's copy there)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(out / "positions.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    out.mkdir(parents=True, exist_ok=False)
    with open(results_root / EXP / run / "outcomes.jsonl") as f:
        outcomes = [json.loads(line) for line in f]
    if "set" in outcomes[0]:
        positions_figure(outcomes, out)
    elif "part" in outcomes[0]:
        parts_figure(outcomes, out)
    else:
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
