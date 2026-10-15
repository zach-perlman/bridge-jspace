"""Figures for exp09_bind_recall (part B), from its map, parts and swaps runs.

exp09_figures.py OUT_NAME [--map M --parts P --swaps S]  -> figures/exp09_bind_recall/OUT_NAME/ (write-once)
    bind_recall.png  left: the lens-free map, how often copying the counterfactual's activation at the question's
                     tokens (solid) or the last token (dashed) gives X's capital, by layer, recalled (R) and bound (B);
                     middle: at the window, how often each part of the copy does (exp04's split, J++), with the
                     random-direction nulls; right: exp02's probe swaps at the cue phrase, layers 24-40
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

EXP = "exp09_bind_recall"
FAMILY = {"R": ("#3b6fb6", "recalled (R)"), "B": ("#c07a2c", "bound in context (B)")}
CONTROL = "#b4b2a9"
PARTS = [
    ("full", "the whole copy"),
    ("jspace", "J-space part"),
    ("not_jspace", "all but that"),
    ("lens2", "I/X lens coords"),
    ("not_lens2", "all but those"),
]
SWAPS = [("jpart", "J-part"), ("full_probe", "full probe"), ("remainder", "remainder"), ("jpart_matched", "matched")]


def read_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def step(rows: list[dict]) -> float:
    per: dict[str, list[bool]] = {}
    for o in rows:
        per.setdefault(o["name"], []).append(o["role"] == "b")
    return 100 * statistics.mean(statistics.mean(v) for v in per.values()) if per else float("nan")


def figure(root: Path, map_run: str, parts_run: str, swaps_run: str, out: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.6), facecolor=SURFACE, width_ratios=(1.2, 1.2, 1))
    ax = axes[0]
    style_axes(ax)
    m = read_jsonl(root / map_run / "outcomes.jsonl")
    layers = sorted({o["layer"] for o in m})
    for fam, (colour, label) in FAMILY.items():
        for group, ls in (("question", "-"), ("last", "--")):
            ys = []
            for layer in layers:
                cell = [o for o in m if (o["family"], o["group"], o["layer"], o["source"]) == (fam, group, layer, "cf")]
                ys.append(100 * sum(o["role"] == "b" for o in cell) / len(cell))
            ax.plot(
                layers, ys, color=colour, ls=ls, lw=1.8, label=f"{label}, {'question' if ls == '-' else 'last token'}"
            )
        off = [
            100
            * statistics.mean(
                o["role"] != "A" for o in m if (o["family"], o["layer"], o["source"]) == (fam, layer, "off")
            )
            for layer in layers
        ]
        ax.plot(layers, off, color=CONTROL, lw=1, ls=":")
    ax.set_ylim(-3, 103)
    ax.set_xlabel("layer copied", color=MUTED, fontsize=9)
    ax.set_ylabel("% of items answering X's capital", color=MUTED, fontsize=9)
    ax.set_title(
        "Map, lens-free (dotted: off-path copy)",
        loc="left",
        fontsize=10,
        color=INK,
    )
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    style_axes(ax)
    p = read_jsonl(root / parts_run / "outcomes.jsonl")
    width = 0.38
    for k, (fam, (colour, label)) in enumerate(FAMILY.items()):
        rows = [o for o in p if o["family"] == fam and o["source"] == "cf"]
        if not rows:
            continue
        window = sorted({o["layer"] for o in rows})
        for x, (part, _) in enumerate(PARTS):
            real = step([o for o in rows if o["part"] == part and not o["null"]])
            null = step([o for o in rows if o["part"] == part and o["null"]])
            ax.bar(
                x + (k - 0.5) * width,
                real,
                width=width * 0.9,
                color=colour,
                label=f"{label}, layers {window}" if x == 0 else None,
            )
            if part != "full":
                ax.plot(
                    [x + (k - 0.5) * width - width * 0.4, x + (k - 0.5) * width + width * 0.4],
                    [null, null],
                    color=INK,
                    lw=1,
                )
    ax.set_xticks(range(len(PARTS)))
    ax.set_xticklabels([label for _, label in PARTS], rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("step score (% of window layers)", color=MUTED, fontsize=9)
    ax.set_title("Split at the window (J++; black ticks: random nulls)", loc="left", fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[2]
    style_axes(ax)
    s = read_jsonl(root / swaps_run / "outcomes.jsonl")
    for k, (fam, (colour, label)) in enumerate(FAMILY.items()):
        for x, (cond, _) in enumerate(SWAPS):
            rows = [o for o in s if o["family"] == fam and o["condition"] == cond and not o["null"]]
            m_, lo, hi = wilson(sum(o["role"] == "b" for o in rows), len(rows))
            xs = x + (k - 0.5) * width
            ax.bar(xs, 100 * m_, width=width * 0.9, color=colour, label=label if x == 0 else None)
            ax.errorbar(
                xs, 100 * m_, yerr=[[100 * max(m_ - lo, 0)], [100 * max(hi - m_, 0)]], color=INK, lw=1, capsize=2
            )
    ax.set_xticks(range(len(SWAPS)))
    ax.set_xticklabels([label for _, label in SWAPS], fontsize=8.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of items answering X's capital", color=MUTED, fontsize=9)
    ax.set_title("exp02's probe swaps, cue phrase, layers 24-40", loc="left", fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Recalled vs bound-in-context bridge: same question, countries and second hop",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out / "bind_recall.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, map_run: str, parts_run: str, swaps_run: str, out_root: Path, results_root: Path) -> None:
    out = out_root / out_name
    assert not out.exists(), f"{out} exists; figure folders are write-once"
    out.mkdir(parents=True)
    figure(results_root / EXP, map_run, parts_run, swaps_run, out)
    (out / "sources.json").write_text(json.dumps({"runs": [map_run, parts_run, swaps_run]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/exp09_bind_recall/ (write-once)")
    parser.add_argument("--map", default="map_v1")
    parser.add_argument("--parts", default="parts_v1")
    parser.add_argument("--swaps", default="swaps_v1")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    parser.add_argument("--results-root", type=Path, default=pins.RESULTS_DIR, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.map, args.parts, args.swaps, args.out_root, args.results_root)
