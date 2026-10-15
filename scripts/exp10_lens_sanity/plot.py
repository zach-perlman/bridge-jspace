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
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from bridge_jspace.pins import FIGURES_DIR, RESULTS_DIR
from bridge_jspace.plotting import (
    GRID,
    INK,
    MUTED,
    SURFACE,
    bootstrap_note,
    finish,
    percent_axis,
    shade_band,
    style_axes,
)
from bridge_jspace.stats import wilson

# Fixed per reader (entity, not rank). Baseline is recessive gray + dashed.
STYLE = {
    "jlens": {"color": "#2a78d6", "ls": "-", "label": "J-lens"},
    "jpp": {"color": "#eb6834", "ls": "-", "label": "J++"},
    "logit": {"color": "#898781", "ls": "--", "label": "logit lens"},
}
HIT_K = 10

RUNS_DIR = RESULTS_DIR / "exp10_lens_sanity"
# Summary inputs (label, run id): the trailing-space-stripped runs, the setup every experiment uses. The runs on the
# prompts as published (205029, 205736) are a sensitivity check reported in the README's details only.
SUMMARY_RUNS = [
    ("Qwen3.5-4B", "20261013-205057"),
    ("Qwen3.6-27B", "20261013-205936"),
]
SUMMARY_LAYER_RUN = "20261013-205936"  # 27B, stripped
READERS = ["logit", "jlens", "jpp"]
SUBSET = "all_single_token"


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _style(reader: str) -> dict:
    return STYLE.get(reader, {"color": INK, "ls": "-", "label": reader})


def _item_hits(rows: list[dict]) -> np.ndarray:
    """[items, layers] bool: any of the item's bridge forms ranked below HIT_K at that layer (rows of one reader)."""
    by_item: dict[str, list[np.ndarray]] = {}
    for r in rows:
        by_item.setdefault(r["name"], []).append(np.array(r["ranks"]) < HIT_K)
    return np.array([np.any(v, axis=0) for v in by_item.values()])


def _summary(run_dir: Path) -> dict:
    """The run's current aggregation: its newest `analysis-*/summary.json` (re-aggregated with the current rules by
    `experiment analyze`), else the run's own `summary.json`."""
    analyses = sorted(run_dir.glob("analysis-*/summary.json"))
    return json.loads((analyses[-1] if analyses else run_dir / "summary.json").read_text())


# ---- one run ---------------------------------------------------------------------------------


def plot_run(run_dir: str | Path) -> Path:
    """pass@k curves and the per-layer hit rate of one run, into `<run_dir>/figures-<timestamp>/`."""
    run_dir = Path(run_dir)
    rows = _load(run_dir / "multihop_ranks.jsonl")
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    out = run_dir / f"figures-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()

    fig, (ax_k, ax_l) = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURFACE)
    ks = np.unique(np.logspace(0, 3, 60).astype(int))
    for reader in readers:
        st = _style(reader)
        rr = [r for r in rows if r["reader"] == reader]
        # pass@k: per item, found if any of its intermediates (forms of one bridge) has min rank < k.
        by_item: dict[str, list[int]] = {}
        for r in rr:
            by_item.setdefault(r["name"], []).append(r["min_rank"])
        mins = list(by_item.values())
        pass_k = [np.mean([min(m) < k for m in mins]) for k in ks]
        # Legends, not end labels: curves converge at both ends (pass@1000 ~ 1, late-layer hits ~ 0)
        # and the labels collide.
        ax_k.plot(ks, pass_k, color=st["color"], ls=st["ls"], lw=2, label=st["label"])

        # Per-layer hit rate: share of items with any form of the bridge at rank < HIT_K at that layer.
        layers = rr[0]["layers"]
        hits = _item_hits(rr).mean(0)
        ax_l.plot(layers, hits, color=st["color"], ls=st["ls"], lw=2, label=st["label"])

    n_items = len({r["name"] for r in rows})
    ax_k.set_xscale("log")
    ax_k.set_xlabel("k (how deep in the reader's ranking we look)", color=MUTED)
    ax_k.set_ylabel("bridge in the top k at its best layer\n(% of questions)", color=MUTED)
    ax_k.set_title("How deep in the ranking is the bridge?", color=INK, fontsize=11, loc="left")
    ax_l.set_xlabel("model layer (0 = first)", color=MUTED)
    ax_l.set_ylabel(f"bridge in the top {HIT_K}\n(% of questions)", color=MUTED)
    ax_l.set_title(f"At which layers is it in the top {HIT_K}?", color=INK, fontsize=11, loc="left")
    for ax in (ax_k, ax_l):
        ax.set_ylim(0, 1)
        style_axes(ax)
        percent_axis(ax)
        ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)
    path = out / "multihop_pass_at_k.png"
    model = json.loads((run_dir / "manifest.json").read_text())["config"]["model"]["name"].split("/")[-1]
    finish(
        fig,
        path,
        f"{model}: does each reader find the two-hop bridge at the last prompt token?",
        f"Lens-eval multihop set (released with the J-lens), all {n_items} questions (answered correctly or not), read at the last prompt token. "
        "A bridge listed in several forms ('5', 'five') counts as found if any form is. Diagnostic for one run; the "
        "summary figures use the single-token bridges only.",
    )
    return path


# ---- several runs (README figures) -----------------------------------------------------------


def _summary_bars(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8), facecolor=SURFACE)
    width = 0.26
    pk: dict = {}
    n_boot = None
    for gi, (_, run) in enumerate(SUMMARY_RUNS):
        pk = _summary(RUNS_DIR / run)["pass_at_k"][SUBSET]
        n_boot = json.loads((RUNS_DIR / run / "manifest.json").read_text())["config"]["params"]["n_boot"]
        for ri, reader in enumerate(READERS):
            if reader not in pk:
                continue  # Qwen3.5-4B has no J++ lens
            v = pk[reader]["10"]
            x = gi + (ri - 1) * width
            ax.bar(x, v["mean"], width * 0.92, color=STYLE[reader]["color"], zorder=2)
            ax.errorbar(
                x, v["mean"], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], color=INK, lw=1, capsize=3, zorder=3
            )
    ax.set_xticks(range(len(SUMMARY_RUNS)), [label for label, _ in SUMMARY_RUNS], fontsize=9, color=INK)
    ax.set_ylim(0, 1)
    ax.set_ylabel(f"bridge in the reader's top {HIT_K} at\nits best layer (% of questions)", color=MUTED)
    style_axes(ax)
    percent_axis(ax)
    ax.grid(axis="x", visible=False)
    handles = [Patch(color=STYLE[r]["color"], label=STYLE[r]["label"]) for r in READERS]
    finish(
        fig,
        path,
        "How often does each reader find the bridge at the last prompt token?",
        f"The multihop question set released with the J-lens (lens-eval): the {pk['n']} two-hop questions whose bridge is a single token, all of them (answered "
        "correctly or not). Read at the last prompt token at every "
        f"layer; a bridge counts as found if it is in the reader's top {HIT_K} at its best layer (pass@{HIT_K}); a "
        "bridge listed in several forms ('5', 'five') counts as found if any form is. "
        f"Error bars: {bootstrap_note(n_boot or 0)}. Qwen3.5-4B has no J++ lens.",
        handles,
    )


def _summary_layers(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.6), facecolor=SURFACE)
    rows = _load(RUNS_DIR / SUMMARY_LAYER_RUN / "multihop_ranks.jsonl")
    n_items = 0
    for reader in READERS:
        rr = [r for r in rows if r["reader"] == reader and r["single_token"]]
        hits = _item_hits(rr)
        n_items = hits.shape[0]
        ci = np.array([wilson(int(k), n_items) for k in hits.sum(0)])
        st = STYLE[reader]
        ax.fill_between(rr[0]["layers"], ci[:, 1], ci[:, 2], color=st["color"], alpha=0.12, lw=0)
        ax.plot(rr[0]["layers"], hits.mean(0), color=st["color"], ls=st["ls"], lw=2, label=st["label"])
    shade_band(ax, 32, 48)
    ax.set_ylim(0, 0.55)
    ax.set_xlabel("model layer (0 = first)", color=MUTED)
    ax.set_ylabel(f"bridge in the reader's top {HIT_K}\n(% of questions)", color=MUTED)
    style_axes(ax)
    percent_axis(ax)
    handles: list[Artist] = [
        Line2D([], [], color=STYLE[r]["color"], ls=STYLE[r]["ls"], lw=2, label=STYLE[r]["label"]) for r in READERS
    ]
    handles.append(Patch(color=GRID, label="layers 32-48: the band the later analyses average over"))
    finish(
        fig,
        path,
        f"Qwen3.6-27B: at which layers is the bridge in each reader's top {HIT_K}?",
        f"Lens-eval multihop set, the {n_items} questions above, read at the last prompt "
        "token; a bridge listed in several forms ('5', 'five') counts if any form is in the top 10. Shaded: 95% Wilson "
        "CI. The bar chart takes each bridge's "
        "best layer, so the last layers, where the logit lens catches up, hide the middle-layer difference.",
        handles,
    )


def plot_summary() -> Path:
    """README figures across SUMMARY_RUNS, into `figures/exp10_lens_sanity/<timestamp>/`."""
    out = FIGURES_DIR / "exp10_lens_sanity" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    _summary_bars(out / "pass_at_10_by_model.png")
    _summary_layers(out / "27b_by_layer.png")
    return out


if __name__ == "__main__":
    print(plot_summary() if sys.argv[1:] == ["--summary"] else plot_run(sys.argv[1]))
