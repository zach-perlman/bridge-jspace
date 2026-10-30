"""Figures for exp20_competence (task competence, parts A and B), from a run's summary.json.

exp20_figures.py OUT_NAME [--run v1]  -> figures/pre-sprint/exp20_competence/OUT_NAME/competence.png (write-once)
    competence.png   one row per task, three panels sharing the rows. Left: how often the unedited model answers the
                     clean prompt, raw text (as B1 and exp09 ran) vs the chat template vs the chat template with
                     "Answer:" prefilled (as brew ran), Wilson 95% intervals; for exp09's families, hollow: all three of
                     its clean, counterfactual and off-path prompts (exp09's gate). Middle: in the chat template with
                     "Answer:", each step alone vs both in one answer. Right: the median probability of the answer's
                     first token on the clean prompt, per format.
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

from matplotlib.ticker import FuncFormatter

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, percent_axis, style_axes

EXP = "exp20_competence"
TASKS = [  # (task, label): part A and B1's set first, then exp09's families, then brew
    ("probe_swap", "B1 two-hop facts"),
    ("R", "exp09 R: recalled, capital"),
    ("B", "exp09 B: bound, capital"),
    ("L", "exp09 L: bound, colour lookup"),
    ("RL", "exp09 RL: recalled, colour lookup"),
    ("brew_bank", "brew bank (gated)"),
    ("brew_fresh", "brew fresh"),
    ("brew_test", "brew test"),
]
FORMATS = [  # (format, label, colour, marker): colours checked with the dataviz palette validator (light surface)
    ("raw", "raw text", "#c07a2c", "o"),
    ("chat", "chat template", "#3b6fb6", "s"),
    ("chat_prefill", 'chat template + "Answer:"', "#3f9c6b", "^"),
]
STEPS = [  # (kind, label, colour, marker)
    ("hop1", "first step alone", "#b4b2a9", "o"),
    ("hop2", "second step alone", "#898781", "s"),
    ("clean", "both steps in one answer", "#3f9c6b", "^"),
]
AS_RUN_LABEL = {"raw": "ran raw", "chat_prefill": 'ran chat + "Answer:"'}


def err(rate: float, lo: float, hi: float) -> list[list[float]]:
    """errorbar's xerr for a rate and its interval (a Wilson bound can sit a rounding error inside the rate)."""
    return [[max(0.0, rate - lo)], [max(0.0, hi - rate)]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--run", default="v1")
    args = ap.parse_args()
    out = pins.REPO_ROOT / "figures" / EXP / args.out
    assert not out.exists(), f"{out} exists; figure folders are written once"
    summary = json.loads((pins.RESULTS_DIR / EXP / args.run / "summary.json").read_text())
    manifest = json.loads((pins.RESULTS_DIR / EXP / args.run / "manifest.json").read_text())
    cells, joint = summary["cells"], summary["joint"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 6.2), sharey=True, gridspec_kw={"width_ratios": [1.25, 1, 0.9]})
    fig.patch.set_facecolor(SURFACE)
    rows = {task: len(TASKS) - 1 - i for i, (task, _) in enumerate(TASKS)}
    dodge = {0: 0.22, 1: 0.0, 2: -0.22}

    ax = axes[0]
    for j, (fmt, label, colour, marker) in enumerate(FORMATS):
        for task, _ in TASKS:
            c = cells[task].get(fmt, {}).get("clean")
            if not c:
                continue
            y = rows[task] + dodge[j]
            ax.errorbar(c["rate"], y, xerr=err(c["rate"], *c["ci"]), fmt=marker,
                        color=colour, ms=7, lw=1.6, capsize=0, mec=SURFACE, mew=1, label=label if task == "probe_swap" else None)  # fmt: skip
            a3 = joint[task].get(fmt, {}).get("all_three")
            if a3 and fmt == "raw":  # chat: all three at 99-100%, on top of the clean marker
                ax.errorbar(a3["rate"], y, xerr=err(a3["rate"], a3["lo"], a3["hi"]), fmt="D",
                            color=colour, mfc=SURFACE, ms=6, lw=0.9, capsize=0, alpha=0.9,
                            label="the same, all three of exp09's prompts (its gate)" if (task, fmt) == ("R", "raw") else None)  # fmt: skip
    ax.annotate("52%: exp09's R in raw text\npasses its own gate for half", xy=(joint["R"]["raw"]["all_three"]["rate"], rows["R"] + 0.22),
                xytext=(0.43, rows["R"] - 0.75), fontsize=8, color=INK, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})  # fmt: skip
    ax.set_xlim(0.4, 1.02)
    ax.set_title("Does it answer the clean prompt?", fontsize=11, color=INK, loc="left")
    ax.set_xlabel("items answered correctly (greedy)", color=MUTED, fontsize=9)

    ax = axes[1]
    for j, (kind, label, colour, marker) in enumerate(STEPS):
        for task, _ in TASKS:
            c = cells[task].get("chat_prefill", {}).get(kind)
            if not c:
                continue
            y = rows[task] + dodge[j]
            ax.errorbar(c["rate"], y, xerr=err(c["rate"], *c["ci"]), fmt=marker,
                        color=colour, ms=7, lw=1.6, capsize=0, mec=SURFACE, mew=1, label=label if task == "R" else None)  # fmt: skip
    ax.annotate("B1 names its bridge but\nnot its steps: no step prompts", xy=(0.42, rows["probe_swap"]), fontsize=8, color=MUTED, va="center")  # fmt: skip
    ax.set_xlim(0.4, 1.02)
    ax.set_title('Each step alone vs both (chat + "Answer:")', fontsize=11, color=INK, loc="left")
    ax.set_xlabel("items answered correctly (greedy)", color=MUTED, fontsize=9)

    ax = axes[2]
    for j, (fmt, _label, colour, marker) in enumerate(FORMATS):
        for task, _ in TASKS:
            c = cells[task].get(fmt, {}).get("clean")
            if c and c["median_p_answer"] is not None:
                ax.plot(c["median_p_answer"], rows[task] + dodge[j], marker, color=colour, ms=7, mec=SURFACE, mew=1)
    ax.set_xlim(0, 1.02)
    ax.set_title("How sure? (clean prompt)", fontsize=11, color=INK, loc="left")
    ax.set_xlabel("median probability of the answer's first token", color=MUTED, fontsize=9)

    for ax in axes:
        style_axes(ax)
        percent_axis(ax, "x")
        ax.set_ylim(-0.6, len(TASKS) - 0.4)
    axes[2].xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.1f}"))
    axes[0].set_yticks([rows[t] for t, _ in TASKS])
    axes[0].set_yticklabels(
        [f"{label}\n(n={cells[t]['chat_prefill']['clean']['n']}; {AS_RUN_LABEL[summary['as_run'][t]]})" for t, label in TASKS],
        fontsize=9, color=INK,
    )  # fmt: skip

    fig.suptitle("Can Qwen3.6-27B do part B's tasks before any edit, and in which format?", x=0.01, ha="left",
                 fontsize=13, color=INK, y=0.995)  # fmt: skip
    note = (
        f"exp20_competence run {args.run}: every item of each task, unedited, greedy ({manifest['generation'].split(',')[1].strip()}). "
        "Raw text: no chat template, as B1 and exp09 ran. Chat template: thinking off, the statement turned into a question "
        "(B1: fill in the blank). Lines: Wilson 95% intervals. exp09 in the chat formats: all three of its prompts 99-100%."
    )
    fig.text(0.01, 0.945, note, fontsize=8.5, color=MUTED, ha="left", va="top", wrap=True)
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.45, -0.1), ncol=2, frameon=False, fontsize=9)
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=1, frameon=False, fontsize=9)
    axes[2].annotate("formats coloured as\nin the left panel", xy=(0.03, -0.17), xycoords="axes fraction", fontsize=8.5,
                     color=MUTED, va="top")  # fmt: skip
    fig.tight_layout(rect=(0, 0.02, 1, 0.92))
    out.mkdir(parents=True)
    fig.savefig(out / "competence.png", dpi=160, facecolor=SURFACE)
    print("wrote", out / "competence.png")


if __name__ == "__main__":
    main()
