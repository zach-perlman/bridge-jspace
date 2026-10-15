"""Figure for exp18 v2: with C's state patched into B, do the verbalizers name the state's colour (X) or the text's (I)?

  uv run python -m scripts.exp18_brew_verbalizers.plot RUN_DIR OUT_NAME  -> figures/exp18_brew_verbalizers/OUT_NAME/

state_vs_text.png: one panel per reading cell (the NLA at 42 and the oracle lens at 44 after the early patch, the
oracle at 48 after the late one), on the items where that patch took: how often a reading names X (dark) and I
(light) in B as written, B with C's state patched in, B with the off-path state patched in, and C as written; dots:
how often J++ ranks X first of the 12 colours on the same vectors. An item counts if either read position does.

  uv run python -m scripts.exp18_brew_verbalizers.plot RUN_DIR OUT_NAME --v3  -> code_vs_lens.png, for a v3 run:
one panel per reader (the NLA at 42, the oracle lens at 44, J++ at 42), on the items where the code edit took: how
often a reading names X with B as written and under each edit (the code, J++'s direction, a random one), against how
often each edit makes the model itself take X as its step (grey, all eligible items).
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
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes
from bridge_jspace.stats import bootstrap_mean

CELLS = [
    ("nla", "early", 42, "NLA, layer 42 (patch 36-40)"),
    ("oracle", "early", 44, "oracle lens, layer 44 (patch 36-40)"),
    ("oracle", "late", 48, "oracle lens, layer 48 (patch 36-46)"),
]
CONDITIONS = [
    ("clean", "B as written"),
    ("patched", "B + C's state"),
    ("off_patched", "B + off-path state"),
    ("cf", "C as written"),
]
X_COLOUR, I_COLOUR = "#3d8c5a", "#c9a3e0"


def per_item(reads: list[dict], names: set[str], reader: str, regime: str, layer: int, condition: str, field: str):
    hit: dict[str, bool] = {}
    for r in reads:
        same_cell = (r["reader"], r["layer"], r["condition"]) == (reader, layer, condition) and r.get(
            "regime", "-"
        ) in (
            "-",
            regime,
        )
        if same_cell and r["name"] in names:
            hit[r["name"]] = hit.get(r["name"], False) or bool(r[field])
    return [float(v) for v in hit.values()]


def figure(run_dir: Path, out: Path) -> None:
    items = [json.loads(line) for line in (run_dir / "items.jsonl").read_text().splitlines()]
    reads = [json.loads(line) for line in (run_dir / "reads.jsonl").read_text().splitlines()]
    fig, axes = plt.subplots(1, len(CELLS), figsize=(15, 4.4), facecolor=SURFACE, sharey=True)
    for ax, (reader, regime, layer, title) in zip(axes, CELLS, strict=True):
        style_axes(ax)
        took = {r["name"] for r in items if r.get(f"{regime}_took")}
        for x, (condition, _) in enumerate(CONDITIONS):
            for offset, field, colour in ((-0.18, "names_X", X_COLOUR), (0.18, "names_I", I_COLOUR)):
                m, lo, hi = bootstrap_mean(per_item(reads, took, reader, regime, layer, condition, field), 2000, 0)
                ax.bar(x + offset, 100 * m, width=0.34, color=colour)
                ax.errorbar(x + offset, 100 * m, yerr=[[100 * (m - lo)], [100 * (hi - m)]], color=INK, lw=1, capsize=2)
            lens = per_item(reads, took, "jpp", regime, layer, condition, "names_X")
            ax.plot(x - 0.18, 100 * statistics.mean(lens), "o", color=INK, ms=4)
        ax.set_xticks(range(len(CONDITIONS)))
        ax.set_xticklabels([label for _, label in CONDITIONS], rotation=15, ha="right", fontsize=8.5)
        ax.set_ylim(0, 100)
        ax.set_title(f"{title}, n={len(took)}", loc="left", fontsize=10, color=INK)
    axes[0].set_ylabel("% of items whose readings name the colour", color=MUTED, fontsize=9)
    handles = [
        Rectangle((0, 0), 1, 1, color=X_COLOUR),
        Rectangle((0, 0), 1, 1, color=I_COLOUR),
        Line2D([], [], marker="o", color=INK, ls=""),
    ]
    labels = ["names X, the patched state's colour", "names I, the text's colour", "J++ ranks X first (same vectors)"]
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, fontsize=8.5)
    fig.suptitle(
        "Brew: with C's state patched into B, the verbalizers name the state's intermediate, not the text's "
        "(items where the patch changed the model's answer)",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(out / "state_vs_text.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


V3_CELLS = [("nla", 42, "NLA, layer 42"), ("oracle", 44, "oracle lens, layer 44"), ("jpp", 42, "J++, layer 42")]
V3_CONDITIONS = [
    ("clean", "B as written"),
    ("code", "+ exp07's code"),
    ("lens", "+ J++ direction"),
    ("random", "+ random"),
]


def figure_v3(run_dir: Path, out: Path) -> None:
    items = [json.loads(line) for line in (run_dir / "items.jsonl").read_text().splitlines()]
    reads = [json.loads(line) for line in (run_dir / "reads.jsonl").read_text().splitlines()]
    eligible = [r for r in items if r["status"] == "eligible"]
    took = {r["name"] for r in eligible if r["code_took"]}
    fig, axes = plt.subplots(1, len(V3_CELLS), figsize=(15, 4.4), facecolor=SURFACE, sharey=True)
    for ax, (reader, layer, title) in zip(axes, V3_CELLS, strict=True):
        style_axes(ax)
        for x, (condition, _) in enumerate(V3_CONDITIONS):
            values = per_item(reads, took, reader, "-", layer, condition, "names_X")
            m, lo, hi = bootstrap_mean(values, 2000, 0)
            ax.bar(x + 0.18, 100 * m, width=0.34, color=X_COLOUR)
            ax.errorbar(x + 0.18, 100 * m, yerr=[[100 * (m - lo)], [100 * (hi - m)]], color=INK, lw=1, capsize=2)
            model_took = 0.0 if condition == "clean" else statistics.mean(r[f"{condition}_took"] for r in eligible)
            ax.bar(x - 0.18, 100 * model_took, width=0.34, color=MUTED, alpha=0.5)
        ax.set_xticks(range(len(V3_CONDITIONS)))
        ax.set_xticklabels([label for _, label in V3_CONDITIONS], rotation=15, ha="right", fontsize=8.5)
        ax.set_ylim(0, 100)
        ax.set_title(f"{title}, n={len(took)}", loc="left", fontsize=10, color=INK)
    axes[0].set_ylabel("% of items", color=MUTED, fontsize=9)
    handles = [Rectangle((0, 0), 1, 1, color=MUTED, alpha=0.5), Rectangle((0, 0), 1, 1, color=X_COLOUR)]
    labels = ["the model takes X as its step (all eligible items)", "readings name X (items where the code took)"]
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, fontsize=8.5)
    fig.suptitle(
        "Brew: the verbalizers name X most under J++'s direction, which the model ignores, more than under the code it "
        "computes with",
        x=0.01,
        ha="left",
        fontsize=11,
        color=INK,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(out / "code_vs_lens.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(run_dir: Path, out_name: str, v3: bool = False) -> None:
    out = pins.FIGURES_DIR / "exp18_brew_verbalizers" / out_name
    assert not out.exists(), f"{out} exists; figure folders are write-once"
    out.mkdir(parents=True)
    (figure_v3 if v3 else figure)(run_dir, out)
    (out / "sources.json").write_text(json.dumps({"runs": [str(run_dir.relative_to(pins.REPO_ROOT))]}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "run_dir", type=Path, help="an exp18 v2 run, e.g. results/exp18_brew_verbalizers/20261015-205549"
    )
    parser.add_argument("out_name", help="folder under figures/exp18_brew_verbalizers/ (write-once)")
    parser.add_argument("--v3", action="store_true", help="a v3 run (exp07's code against J++'s direction)")
    args = parser.parse_args()
    main(args.run_dir.resolve(), args.out_name, args.v3)
