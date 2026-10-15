"""The verbalizers by part B's swap labels: in the questions whose J-space swap changes the answer (J-mediated) and in
those where no swap does (neither), how often the lenses rank the bridge 1st and how often the oracle lens and the NLA
name it, on the same readings (the oracle at layers 32-48, the README's band; the NLA at 42).

    uv run python -m scripts.exp16_nla.by_label results/exp16_nla/<run> results/exp15_oracle_lens/<run> [...]
writes <exp16 run>/analysis-<timestamp>-by-label/ (summary.json, by_swap_label.png).
"""

from __future__ import annotations

import csv
import json
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from bridge_jspace.pins import REPO_ROOT
from bridge_jspace.plotting import INK, MUTED, SURFACE, bootstrap_note, finish, percent_axis, style_axes
from scripts.exp15_oracle_lens.experiment import load_runs, load_scored
from scripts.exp15_oracle_lens.plot import READER_COLOR, _clustered

from .compare import NLA_COLOR

LENS_GREY = "#9aa0a6"
GROUPS = ("J-mediated", "neither")  # part B's labels with enough questions (non-J: 1, both: 2)
LABELS = {"J-lens": "results/exp02_swaps/main_v4_jlens/labels.csv", "J++": "results/exp02_swaps/main_v4_jpp/labels.csv"}


def labels(path: str) -> dict[str, str]:
    rows = csv.DictReader((REPO_ROOT / path).read_text().splitlines())
    return {r["name"]: r["label"] for r in rows if r["status"] == "eligible"}


def gap_difference(a: list[dict], b: list[dict], n_boot: int, seed: int) -> list[float]:
    """(verbalizer - lens) in group a minus the same in group b, per-question means, bootstrap over questions within
    each group: [difference, 2.5th, 97.5th percentile]."""

    def gaps(rows: list[dict]) -> np.ndarray:
        by: dict[str, list[float]] = {}
        for r in rows:
            by.setdefault(r["name"], []).append(float(r["_named"]) - float(r["_lens"]))
        return np.array([np.mean(v) for v in by.values()])

    ga, gb = gaps(a), gaps(b)
    rng = np.random.default_rng(seed)
    boot = [rng.choice(ga, len(ga)).mean() - rng.choice(gb, len(gb)).mean() for _ in range(n_boot)]
    return [float(ga.mean() - gb.mean()), *map(float, np.percentile(boot, [2.5, 97.5]))]


def rows_for(reads: list[dict], layers: Sequence[int], label_of: dict[str, str], group: str) -> list[dict]:
    return [
        {"name": r["name"], "_lens": r["jlens_rank"] == 1 or r["jpp_rank"] == 1, "_named": r["named_bridge"],
         "_distractor": r["named_distractor"]}
        for r in reads
        if r["condition"] == "clean" and r["layer"] in layers and label_of.get(r["name"]) == group
    ]  # fmt: skip


def by_label(nla_run: str | Path, oracle_runs: Sequence[str | Path]) -> Path:
    nla_reads, _, params, _ = load_scored(nla_run)
    oracle_reads = load_runs(oracle_runs)[0] if len(oracle_runs) > 1 else load_scored(oracle_runs[0])[0]
    n_boot, seed = params["n_boot"], params["boot_seed"]
    readers = [("oracle lens, layers 32-48", oracle_reads, range(32, 49), READER_COLOR["oracle"]),
               ("NLA, layer 42", nla_reads, [42], NLA_COLOR)]  # fmt: skip
    summary: dict[str, Any] = {"nla_run": str(nla_run), "oracle_runs": [str(r) for r in oracle_runs]}
    for lab_name, lab_path in LABELS.items():
        label_of = labels(lab_path)
        for name, reads, layers, _ in readers:
            per = {g: rows_for(reads, layers, label_of, g) for g in GROUPS}
            summary[f"{lab_name} labels, {name}"] = {
                **{g: {"questions": len({r["name"] for r in rows}),
                       "lens_1st": _clustered(rows, "_lens", n_boot, seed),
                       "named": _clustered(rows, "_named", n_boot, seed),
                       "distractor_named": _clustered(rows, "_distractor", n_boot, seed)} for g, rows in per.items()},
                "gap J-mediated minus neither": gap_difference(per["J-mediated"], per["neither"], n_boot, seed),
            }  # fmt: skip
    out = Path(nla_run) / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-by-label"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    plot(out / "by_swap_label.png", summary, readers, n_boot)
    return out


def plot(path: Path, summary: dict[str, Any], readers: list, n_boot: int) -> Path:
    """Per group (J-lens labels): the lenses (on the oracle's readings at 32-48 and the NLA's at 42) and each
    verbalizer."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), facecolor=SURFACE, sharey=True)
    for ax, (name, _, _, color) in zip(axes, readers, strict=True):
        block = summary[f"J-lens labels, {name}"]
        for gi, g in enumerate(GROUPS):
            for bi, (key, c) in enumerate((("lens_1st", LENS_GREY), ("named", color))):
                m, lo, hi = block[g][key]
                x = gi + (bi - 0.5) * 0.36
                ax.bar(x, m, 0.32, color=c, zorder=2)
                ax.errorbar(x, m, yerr=[[max(m - lo, 0)], [max(hi - m, 0)]], color=INK, lw=1, capsize=2.5, zorder=3)
                ax.text(x, hi + 0.015, f"{m:.0%}", ha="center", va="bottom", fontsize=10.5, color=INK,
                        fontweight="bold")  # fmt: skip
        d, lo, hi = block["gap J-mediated minus neither"]
        ax.set_xticks(range(len(GROUPS)), [f"{g}\n({block[g]['questions']} questions)" for g in GROUPS], fontsize=10)
        ax.set_title(f"{name}\nits edge over the lenses, J-mediated minus neither: {d:+.0%} [{lo:+.0%}, {hi:+.0%}]",
                     color=INK, fontsize=11, loc="left")  # fmt: skip
        ax.set_ylim(0, 1.05)
        style_axes(ax)
        percent_axis(ax)
        ax.grid(axis="x", visible=False)
        ax.set_xlabel("questions by part B's swap label (J-lens swaps)", color=MUTED, fontsize=10)
    axes[0].set_ylabel("% of readings", color=MUTED, fontsize=10)
    finish(
        fig,
        path,
        "Where swapping the bridge's J-space part does not change the answer, the verbalizers keep naming the bridge",
        "Qwen3.6-27B, the 77 two-hop questions it answers correctly, by part B's swap labels: J-mediated = swapping "
        "the bridge's J-space part changes the answer; neither = no swap does (non-J: 1 question, both: 2, left out). "
        "Same readings for each pair of bars (the last word, -1 and the cue phrase's last token). The lenses see the "
        "bridge less in the neither questions, the verbalizers about as often: the edge is there. A reader of a part "
        "the J-lens cannot see would show this; so would a reader that solves the question whatever the state holds. "
        f"Error bars: {bootstrap_note(n_boot)}; the edge's CI: bootstrap over questions within each group.",
        [
            Patch(color=LENS_GREY, label="the J-lens or J++ ranks the bridge 1st"),
            *(Patch(color=color, label=f"the {name.split(',')[0]} names it") for name, _, _, color in readers),
        ],
    )
    return path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    print(by_label(sys.argv[1], sys.argv[2:]))
