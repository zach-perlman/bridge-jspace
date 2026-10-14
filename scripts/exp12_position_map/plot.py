"""Figures for an exp12 run, recomputed from its saved grids (eligible items only). Writes into a new folder.

by_offset.png          one panel per reader: share of band layers with the bridge (blue) / answer (orange) top-1
                       in its pool, per prompt position, with 95% CIs; distractors grey; optimal positions marked.
position_layer.png     heatmaps, readers x {bridge, answer}: share of items with the word top-1 at each
                       (position, layer); the optimal position outlined.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
READER_TITLE = {"logit": "logit lens (baseline)", "jlens": "J-lens", "jpp": "J++"}
# Sequential, one hue each, from the surface to a dark step of the series colour.
CMAP = {
    "bridge": LinearSegmentedColormap.from_list("bridge", [SURFACE, "#86b6ef", BRIDGE, "#104281"]),
    "answer": LinearSegmentedColormap.from_list("answer", [SURFACE, "#f5b08f", ANSWER, "#8a3112"]),
}


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _offset_labels(summary: dict[str, Any]) -> list[str]:
    tokens = summary["tokens_per_offset"]
    return [f"{o}  {tokens[str(o)][0][0].strip() or '␣'!s}" for o in summary["offsets"]]


def plot_run(run_dir: str | Path, out_dir: str | Path, summary: dict[str, Any], chance: dict[str, float]) -> Path:
    from .experiment import load_grids

    run_dir, out = Path(run_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = json.loads(json.dumps(summary, default=str))  # int offsets -> str keys, as on disk
    readers = list(summary["readers"])
    offsets = summary["offsets"]
    lo, hi = summary["band"]
    labels = _offset_labels(summary)

    # 1. Band share per offset ("which position to read").
    fig, axes = plt.subplots(1, len(readers), figsize=(5.2 * len(readers), 4.2), facecolor=SURFACE, sharey=True)
    x = np.arange(len(offsets))
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        res = summary["readers"][reader]
        for role, color, lw in (
            ("distractor", CONTROL, 1),
            ("swap_answer", CONTROL, 1),
            ("bridge", BRIDGE, 2.5),
            ("answer", ANSWER, 2.5),
        ):
            bo = res["by_offset"].get(role, {})
            m = np.array([bo.get(str(o), {}).get("mean", np.nan) for o in offsets])
            ls = "--" if role in ("answer", "swap_answer") else "-"
            ax.plot(x, m, color=color, lw=lw, ls=ls, marker="o" if lw > 1 else None, ms=4)
            if lw > 1:
                lo_ = np.array([bo.get(str(o), {}).get("lo", np.nan) for o in offsets])
                hi_ = np.array([bo.get(str(o), {}).get("hi", np.nan) for o in offsets])
                ax.fill_between(x, lo_, hi_, color=color, alpha=0.15, lw=0)
                opt = res["optimal"].get(role)
                if opt:
                    i = offsets.index(int(opt["offset"]))
                    ax.annotate(f"best {role}", (x[i], m[i]), xytext=(0, 8), textcoords="offset points",
                                ha="center", fontsize=8, color=color, fontweight="bold")  # fmt: skip
        ax.axhline(chance["entities"], color=MUTED, lw=1, ls=":")
        ax.set_xticks(x, labels, rotation=60, ha="right", fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("prompt position (offset from the last word, its usual token)", color=MUTED)
        style_axes(ax)
    np.atleast_1d(axes)[0].set_ylabel(f"share of layers {lo}-{hi} with the word top-1", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, marker="o", ms=4, label="bridge among entities"),
        Line2D([], [], color=ANSWER, lw=2.5, ls="--", marker="o", ms=4, label="answer among answers"),
        Line2D([], [], color=CONTROL, lw=1, label="controls: distractors"),
        Line2D([], [], color=MUTED, lw=1, ls=":", label="chance"),
    ]
    n = summary["n_per_offset"]
    _finish(
        fig,
        handles,
        f"Where in the prompt is each word readable? (eligible items; n per position {min(n.values())}-{max(n.values())}, 95% CI)",
        out / "by_offset.png",
    )

    # 2. Heatmaps position x layer.
    meta = {m["name"]: m for m in _load(run_dir / "items.jsonl") if m["status"] == "eligible"}
    layers = json.loads((run_dir / "layers.json").read_text())
    fig, axes = plt.subplots(len(readers), 2, figsize=(13, 3.2 * len(readers)), facecolor=SURFACE, squeeze=False)
    for r_i, reader in enumerate(readers):
        grids = load_grids(run_dir / f"grids_{reader}.npz")
        for c_i, role in enumerate(("bridge", "answer")):
            ax = axes[r_i][c_i]
            share = np.full((len(offsets), len(layers[reader])), np.nan)
            for o_i, off in enumerate(offsets):
                cols = [
                    grids[nm][f"{role}_pool"][:, m["offsets"].index(off)] == 1
                    for nm, m in meta.items()
                    if off in m["offsets"] and f"{role}_pool" in grids.get(nm, {})
                ]
                if cols:
                    share[o_i] = np.mean(cols, axis=0)
            im = ax.imshow(share, aspect="auto", cmap=CMAP[role], vmin=0, vmax=1, origin="lower",
                           extent=(layers[reader][0] - 0.5, layers[reader][-1] + 0.5, -0.5, len(offsets) - 0.5))  # fmt: skip
            ax.axvline(lo - 0.5, color=MUTED, lw=0.8, ls=":")
            ax.axvline(hi + 0.5, color=MUTED, lw=0.8, ls=":")
            opt = summary["readers"][reader]["optimal"].get(role)
            if opt:
                i = offsets.index(int(opt["offset"]))
                ax.add_patch(
                    plt.Rectangle((lo - 0.5, i - 0.5), hi - lo + 1, 1, fill=False, ec=INK, lw=1.2)  # type: ignore[attr-defined]
                )
            ax.set_yticks(range(len(offsets)), labels, fontsize=7)
            ax.set_title(f"{READER_TITLE.get(reader, reader)}: {role}", color=INK, fontsize=10, loc="left")
            ax.set_xlabel("layer", color=MUTED)
            ax.tick_params(colors=MUTED, labelsize=8)
            fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01).ax.tick_params(labelsize=7, colors=MUTED)
    fig.suptitle(
        "Share of items with the word top-1 in its pool, by prompt position and layer "
        f"(box: best position, layers {lo}-{hi})",
        color=INK,
        fontsize=11,
        x=0.01,
        ha="left",
    )
    fig.tight_layout()
    fig.savefig(out / "position_layer.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return out


def _finish(fig, handles, title: str, path: Path) -> None:
    fig.suptitle(title, color=INK, fontsize=11, x=0.01, ha="left")
    fig.legend(handles=handles, loc="lower center", ncols=len(handles), frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
