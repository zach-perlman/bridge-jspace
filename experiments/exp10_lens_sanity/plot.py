"""Figures for an exp10 run, recomputed from its multihop_ranks.jsonl.

Each call writes a new folder `<run_dir>/figures-<timestamp>/` (never overwrites).
    uv run python -m experiments.exp10_lens_sanity.plot results/exp10_lens_sanity/<stamp>
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

# Fixed per reader (entity, not rank). Baseline is recessive gray + dashed.
STYLE = {
    "jlens": {"color": "#2a78d6", "ls": "-", "label": "J-lens"},
    "jpp": {"color": "#eb6834", "ls": "-", "label": "J++"},
    "logit": {"color": "#898781", "ls": "--", "label": "logit lens"},
}
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb"
HIT_K = 10


def _load(run_dir: Path) -> list[dict]:
    with (run_dir / "multihop_ranks.jsonl").open() as f:
        return [json.loads(line) for line in f if line.strip()]


def _style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=9)


def _end_label(ax, x, y, reader: str) -> None:
    ax.annotate(
        STYLE.get(reader, {"label": reader})["label"],
        (x, y),
        xytext=(4, 0),
        textcoords="offset points",
        va="center",
        fontsize=9,
        color=INK,
    )


def plot_run(run_dir: str | Path) -> Path:
    run_dir = Path(run_dir)
    rows = _load(run_dir)
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    out = run_dir / f"figures-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()

    fig, (ax_k, ax_l) = plt.subplots(1, 2, figsize=(11, 4), facecolor=SURFACE)
    ks = np.unique(np.logspace(0, 3, 60).astype(int))
    for reader in readers:
        st = STYLE.get(reader, {"color": INK, "ls": "-", "label": reader})
        rr = [r for r in rows if r["reader"] == reader]
        # pass@k: per item, fraction of intermediates with min rank < k; then mean over items.
        by_item: dict[str, list[int]] = {}
        for r in rr:
            by_item.setdefault(r["name"], []).append(r["min_rank"])
        mins = list(by_item.values())
        pass_k = [np.mean([np.mean(np.array(m) < k) for m in mins]) for k in ks]
        ax_k.plot(ks, pass_k, color=st["color"], ls=st["ls"], lw=2)
        _end_label(ax_k, ks[-1], pass_k[-1], reader)

        # Per-layer hit rate: share of (item, intermediate) with rank < HIT_K at that layer.
        layers = rr[0]["layers"]
        hits = np.mean([np.array(r["ranks"]) < HIT_K for r in rr], axis=0)
        # Legend, not end labels: curves often all end near 0 here and the labels would collide.
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
        _style_axes(ax)
    ax_l.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout()
    path = out / "multihop_pass_at_k.png"
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print(plot_run(sys.argv[1]))
