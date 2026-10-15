"""Every reader at layer 42: the J-lens and J++ (exact), the NLA (exp16) and the oracle lens at its nearest trained
layers 40 and 44 (exp15), on the same 77 questions and positions.

    uv run python -m scripts.exp16_nla.compare results/exp16_nla/<run> results/exp15_oracle_lens/<run> [...]
writes <exp16 run>/analysis-<timestamp>-compare/ (summary.json, methods_at_42.png).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from bridge_jspace.plotting import INK, MUTED, SURFACE, bootstrap_note, finish, percent_axis, style_axes
from scripts.exp15_oracle_lens.experiment import load_runs, load_scored
from scripts.exp15_oracle_lens.plot import READER_COLOR, _clustered

NLA_COLOR = "#c2410c"


def reader_rows(nla_reads: list[dict], oracle_reads: list[dict]) -> list[tuple[str, str, list[dict]]]:
    """(label, colour, readings with 0/1 fields _word_bridge, _distractor_bridge, _word_answer, _distractor_answer,
    _blind) per reader, clean readings only."""

    def lens(lens_name: str) -> list[dict]:
        return [
            {"name": r["name"], "_blind": r["lens_class"] == "neither",
             "_word_bridge": r[f"{lens_name}_rank"] == 1, "_distractor_bridge": r[f"distractor_{lens_name}_rank"] == 1,
             "_word_answer": None if r["answer_jlens_rank"] is None else r[f"answer_{lens_name}_rank"] == 1,
             "_distractor_answer": None if r["answer_jlens_rank"] is None else r[f"swap_answer_{lens_name}_rank"] == 1}
            for r in nla_reads if r["condition"] == "clean"
        ]  # fmt: skip

    def verbal(reads: list[dict], layer: int | None = None) -> list[dict]:
        return [
            {"name": r["name"], "_blind": r["lens_class"] == "neither",
             "_word_bridge": r["named_bridge"], "_distractor_bridge": r["named_distractor"],
             "_word_answer": None if r["answer_jlens_rank"] is None else r["named_answer"],
             "_distractor_answer": None if r["answer_jlens_rank"] is None else r["named_swap_answer"]}
            for r in reads if r["condition"] == "clean" and (layer is None or r["layer"] == layer)
        ]  # fmt: skip

    return [
        ("J-lens, layer 42", READER_COLOR["jlens"], lens("jlens")),
        ("J++, layer 42", READER_COLOR["jpp"], lens("jpp")),
        ("NLA, layer 42", NLA_COLOR, verbal(nla_reads)),
        ("oracle lens, layer 40", READER_COLOR["oracle"], verbal(oracle_reads, 40)),
        ("oracle lens, layer 44", READER_COLOR["oracle"], verbal(oracle_reads, 44)),
    ]


def rates(readers: list[tuple[str, str, list[dict]]], n_boot: int, seed: int) -> list[dict[str, Any]]:
    """Per reader: the word and its distractor, in all readings and where neither lens has the bridge 1st."""
    out = []
    for label, _, rows in readers:
        row: dict[str, Any] = {"reader": label}
        for word in ("bridge", "answer"):
            sub = [r for r in rows if r[f"_word_{word}"] is not None]
            for kind in ("word", "distractor"):
                row[f"{word} {kind}"] = _clustered(sub, f"_{kind}_{word}", n_boot, seed)
        # where the lenses miss the bridge a lens has it by definition 0% of the time: verbalizers only
        blind = [] if label.startswith(("J-lens", "J++")) else [r for r in rows if r["_blind"]]
        for kind in ("word", "distractor"):
            row[f"bridge {kind}, lenses miss it"] = _clustered(blind, f"_{kind}_bridge", n_boot, seed)
        out.append(row)
    return out


def plot(path: Path, readers: list[tuple[str, str, list[dict]]], table: list[dict], n_boot: int) -> Path:
    panels = [("bridge word", "bridge distractor", "Who has the bridge (e.g. Brazil)?"),
              ("answer word", "answer distractor", "Who has the answer (e.g. Portuguese)?"),
              ("bridge word, lenses miss it", "bridge distractor, lenses miss it",
               "Where neither lens has the bridge 1st:\ndo the verbalizers name it?")]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(19, 5.4), facecolor=SURFACE, sharey=True)
    ys = np.arange(len(readers))
    for ax, (word, distractor, title) in zip(axes, panels, strict=True):
        for y, (_, color, _), row in zip(ys, readers, table, strict=True):
            (m, lo, hi), d = row[word], row[distractor][0]
            if np.isnan(m):
                continue
            ax.plot([d, m], [y, y], color=color, lw=1.5, alpha=0.5, zorder=1)
            ax.plot([lo, hi], [y, y], color=INK, lw=1, zorder=2)
            ax.scatter([m], [y], s=90, color=color, zorder=3)
            ax.scatter([d], [y], s=70, facecolor=SURFACE, edgecolor=color, lw=1.8, zorder=3)
            ax.annotate(f"{m:.0%}", (m, y), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=9.5,
                        color=INK, fontweight="bold")  # fmt: skip
        ax.set_title(title, color=INK, fontsize=11.5, loc="left", pad=12)
        ax.set_xlim(0, 1)
        ax.set_ylim(len(readers) - 0.5, -0.8)  # room above the first row's value label
        style_axes(ax)
        percent_axis(ax, "x")
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("% of readings", color=MUTED, fontsize=10)
    axes[0].set_yticks(ys, [label for label, *_ in readers], fontsize=10)
    handles = [
        Line2D([], [], marker="o", ls="", color=INK, markersize=9, label="the reader has the word"),
        Line2D([], [], marker="o", ls="", markerfacecolor=SURFACE, markeredgecolor=INK, markersize=8,
               label="the reader has its distractor instead (false alarm)"),
    ]  # fmt: skip
    finish(
        fig,
        path,
        "Every reader at layer 42: the lenses, the NLA, and the oracle lens at its nearest layers",
        "Qwen3.6-27B, the 77 two-hop questions it answers correctly (the answer: the 61 with a single-token word "
        "answer); readings at the last word, -1 and the cue phrase's last token. A lens has the word if it ranks it 1st "
        "among its candidates; a verbalizer if the word is in its text. The oracle lens is trained on layers 20-60 in "
        "steps of 4, so it is read at 40 and 44; the NLA only at 42. Right: the readings where neither lens ranks the "
        "bridge 1st at that layer (the lenses themselves have it 0% of the time there, by definition). Black lines: "
        f"{bootstrap_note(n_boot)}.",
        handles,
    )
    return path


def compare(nla_run: str | Path, oracle_runs: Sequence[str | Path]) -> Path:
    nla_reads, _, params, _ = load_scored(nla_run)
    oracle_reads = load_runs(oracle_runs)[0] if len(oracle_runs) > 1 else load_scored(oracle_runs[0])[0]
    readers = reader_rows(nla_reads, oracle_reads)
    table = rates(readers, params["n_boot"], params["boot_seed"])
    out = Path(nla_run) / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-compare"
    out.mkdir()
    sources = {"nla_run": str(nla_run), "oracle_runs": [str(r) for r in oracle_runs]}
    (out / "summary.json").write_text(json.dumps({**sources, "readers": table}, indent=2))
    plot(out / "methods_at_42.png", readers, table, params["n_boot"])
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    print(compare(sys.argv[1], sys.argv[2:]))
