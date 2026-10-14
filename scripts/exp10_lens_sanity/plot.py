"""Figures for exp10, recomputed from saved outputs. Each call writes a new folder (never overwrites).

uv run python -m scripts.exp10_lens_sanity.plot results/exp10_lens_sanity/<stamp>   # one run -> <run>/figures-*/
uv run python -m scripts.exp10_lens_sanity.plot --summary                          # README -> figures/exp10_*/
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bridge_jspace.pins import FIGURES_DIR, RESULTS_DIR
from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE, style_axes

# Fixed per reader (entity, not rank). Baseline is recessive gray + dashed.
STYLE = {
    "jlens": {"color": "#2a78d6", "ls": "-", "label": "J-lens"},
    "jpp": {"color": "#eb6834", "ls": "-", "label": "J++"},
    "logit": {"color": "#898781", "ls": "--", "label": "logit lens"},
}
HIT_K = 10

RUNS_DIR = RESULTS_DIR / "exp10_lens_sanity"
# Summary inputs: the four valid runs (label, run id); 204427/204551 predate the token fix and are superseded.
SUMMARY_RUNS = [
    ("Qwen3.5-4B\nprompt as published", "20261013-205029"),
    ("Qwen3.5-4B\nspace stripped", "20261013-205057"),
    ("Qwen3.6-27B\nprompt as published", "20261013-205736"),
    ("Qwen3.6-27B\nspace stripped", "20261013-205936"),
]
SUMMARY_LAYER_RUN = "20261013-205936"  # 27B, stripped
READERS = ["logit", "jlens", "jpp"]
SUBSET = "all_single_token"


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _style(reader: str) -> dict:
    return STYLE.get(reader, {"color": INK, "ls": "-", "label": reader})


# ---- one run ---------------------------------------------------------------------------------


def plot_run(run_dir: str | Path) -> Path:
    """pass@k curves and the per-layer hit rate of one run, into `<run_dir>/figures-<timestamp>/`."""
    run_dir = Path(run_dir)
    rows = _load(run_dir / "multihop_ranks.jsonl")
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    out = run_dir / f"figures-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()

    fig, (ax_k, ax_l) = plt.subplots(1, 2, figsize=(11, 4), facecolor=SURFACE)
    ks = np.unique(np.logspace(0, 3, 60).astype(int))
    for reader in readers:
        st = _style(reader)
        rr = [r for r in rows if r["reader"] == reader]
        # pass@k: per item, fraction of intermediates with min rank < k; then mean over items.
        by_item: dict[str, list[int]] = {}
        for r in rr:
            by_item.setdefault(r["name"], []).append(r["min_rank"])
        mins = list(by_item.values())
        pass_k = [np.mean([np.mean(np.array(m) < k) for m in mins]) for k in ks]
        # Legends, not end labels: curves converge at both ends (pass@1000 ~ 1, late-layer hits ~ 0)
        # and the labels collide.
        ax_k.plot(ks, pass_k, color=st["color"], ls=st["ls"], lw=2, label=st["label"])

        # Per-layer hit rate: share of (item, intermediate) with rank < HIT_K at that layer.
        layers = rr[0]["layers"]
        hits = np.mean([np.array(r["ranks"]) < HIT_K for r in rr], axis=0)
        ax_l.plot(layers, hits, color=st["color"], ls=st["ls"], lw=2, label=st["label"])

    n_items = len({r["name"] for r in rows})
    ax_k.set_xscale("log")
    ax_k.set_xlabel("k", color=MUTED)
    ax_k.set_ylabel("pass@k", color=MUTED)
    ax_k.set_title(f"lens-eval-multihop pass@k (n={n_items} items)", color=INK, fontsize=11, loc="left")
    ax_l.set_xlabel("layer", color=MUTED)
    ax_l.set_ylabel(f"share of intermediates with rank < {HIT_K}", color=MUTED)
    ax_l.set_title("Where the intermediate is read (last prompt token)", color=INK, fontsize=11, loc="left")
    for ax in (ax_k, ax_l):
        ax.set_ylim(0, 1)
        style_axes(ax)
        ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout()
    path = out / "multihop_pass_at_k.png"
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return path


# ---- several runs (README figures) -----------------------------------------------------------


def _summary_bars(ax) -> None:
    width = 0.26
    pk: dict = {}
    for gi, (_, run) in enumerate(SUMMARY_RUNS):
        pk = json.loads((RUNS_DIR / run / "summary.json").read_text())["pass_at_k"][SUBSET]
        for ri, reader in enumerate(READERS):
            if reader not in pk:
                continue  # Qwen3.5-4B has no J++ lens
            v = pk[reader]["10"]
            x = gi + (ri - 1) * width
            st = STYLE[reader]
            ax.bar(x, v["mean"], width * 0.92, color=st["color"], label=st["label"] if gi == 3 else None, zorder=2)
            ax.errorbar(
                x, v["mean"], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], color=INK, lw=1, capsize=3, zorder=3
            )
    ax.set_xticks(range(len(SUMMARY_RUNS)), [label for label, _ in SUMMARY_RUNS], fontsize=9, color=INK)
    ax.set_ylim(0, 1)
    ax.set_ylabel(f"pass@{HIT_K}: bridge in the reader's top {HIT_K}", color=MUTED)
    ax.set_title(
        f"How often each reader sees the bridge at the last prompt token (n={pk['n']}, 95% CI)",
        color=INK,
        fontsize=11,
        loc="left",
    )
    style_axes(ax)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK, ncols=3)


def _summary_layers(ax) -> None:
    rows = _load(RUNS_DIR / SUMMARY_LAYER_RUN / "multihop_ranks.jsonl")
    for reader in READERS:
        rr = [r for r in rows if r["reader"] == reader and r["single_token"]]
        hits = np.mean([np.array(r["ranks"]) < HIT_K for r in rr], axis=0)
        st = STYLE[reader]
        ax.plot(rr[0]["layers"], hits, color=st["color"], ls=st["ls"], lw=2, label=st["label"])
    ax.axvspan(35, 52, color=GRID, alpha=0.6, zorder=0, lw=0)
    ax.annotate("J-lens / J++ read the bridge,\nlogit lens does not", (43.5, 0.42), ha="center", fontsize=9, color=INK)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel("layer", color=MUTED)
    ax.set_ylabel(f"share of bridges in top {HIT_K}", color=MUTED)
    ax.set_title("Qwen3.6-27B, by layer (space stripped)", color=INK, fontsize=11, loc="left")
    style_axes(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)


def plot_summary() -> Path:
    """README figures across SUMMARY_RUNS, into `figures/exp10_lens_sanity/<timestamp>/`."""
    out = FIGURES_DIR / "exp10_lens_sanity" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    for name, draw, size in (
        ("pass_at_10_by_model.png", _summary_bars, (9, 4)),
        ("27b_by_layer.png", _summary_layers, (8, 3.6)),
    ):
        fig, ax = plt.subplots(figsize=size, facecolor=SURFACE)
        draw(ax)
        fig.tight_layout()
        fig.savefig(out / name, dpi=150, facecolor=SURFACE)
        plt.close(fig)
    return out


if __name__ == "__main__":
    print(plot_summary() if sys.argv[1:] == ["--summary"] else plot_run(sys.argv[1]))
