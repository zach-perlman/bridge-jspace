"""Batch 52's README figure (Dan's README brief, 29 Oct 08:55, decision 7: "What do the lens part's 25 directions stand
for?", batch 52 A, descriptive).

  fig18_atoms  one row per model (9B, 27B, Muse, Lightning): the lens part's rebuilt energy split by the kind of lens
               word each of its 25 directions is (x52_atoms' automatic classes, the e1 set = the main test, the recall's
               view): the original bridge word, the new bridge word, either reader's answer word, another word of the
               scene or of the same class, and no scene word. Lightning (its own report folder) hollow: its gate was
               chosen after its 60-scene pre-check was seen.

Every plotted number is recorded for figures/story/data.csv with its source file.
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts import story_style as S
from scripts.story_b50 import caption

TITLE = "The lens part's directions: the bridge words, almost never the answer"
SUB = "Share of the lens part's rebuilt energy by the kind of word each direction is; main test at L"
ROWS = (
    ("qwen3.5-9b", "9B"),
    ("qwen3.6-27b", "27B"),
    ("muse-glimmer-30b", "Muse"),
    ("nemotron-3.5-lightning", "Lightning"),
)
# the classes drawn, left to right, and the x52_atoms classes each one sums
KINDS = (
    ("the old bridge word", ("bridge",), "#5b5b5b"),
    ("the new bridge word", ("new_bridge",), S.MARK_COL["jpp"]),
    ("an answer word", ("answer_own", "answer_other"), "#b8433a"),
    ("another scene word or its class", ("scene_item", "person", "same_class", "function"), S.COL["control"]),
    ("no scene word", ("other",), S.COL["other"]),
)
HOLLOW = {"nemotron-3.5-lightning"}


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO))


def build_atoms(reports: tuple[Path, ...], out_name: str = "fig18_atoms") -> str:
    """fig18_atoms from x52_atoms report folders (tables.json; each holds some of the models)."""
    data: dict[str, tuple[dict, Path]] = {}
    for d in reports:
        p = d / "tables.json"
        for target, sets in json.loads(p.read_text())["summary"].items():
            data[target] = (sets["e1"]["PM"], p)
    rows = [(t, name) for t, name in ROWS if t in data]
    plt = S.setup()
    top_in, row_in, bottom_in = 0.85, 0.5, 1.75
    h = top_in + row_in * len(rows) + bottom_in
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.13, right=0.88, top=1 - top_in / h, bottom=bottom_in / h)
    S.title(fig, TITLE, SUB)
    for i, (t, _) in enumerate(rows):
        s, p = data[t]
        y, x = -i, 0.0
        hollow = t in HOLLOW
        for what, classes, col in KINDS:
            v = sum(s["energy"][c][0] for c in classes)
            kw = {"facecolor": "white", "edgecolor": col, "hatch": "////", "lw": 1.2} if hollow else {"color": col}
            ax.barh(y, v, left=x, height=0.62, zorder=2, **kw)
            if v >= 0.06:
                box = {"facecolor": "white", "edgecolor": "none", "pad": 1.0} if hollow else None
                ax.text(x + v / 2, y, f"{v:.2f}", ha="center", va="center", fontsize=S.LABEL_PT, bbox=box,
                        color="white" if col in ("#5b5b5b", S.MARK_COL["jpp"]) and not hollow else "#222222")  # fmt: skip
            S.record(out_name, t, f"52 A: share of the rebuilt energy, {what}", round(v, 4), n=s["n"], source=rel(p))
            x += v
        ax.text(1.02, y, f"n = {s['n']}" + (f"  {S.STATUS_GLYPH['after']}" if hollow else ""), va="center",
                fontsize=S.FONT - 1, color=S.COL["muted"])  # fmt: skip
    ax.set_yticks([-i for i in range(len(rows))], [name for _, name in rows], fontsize=S.FONT, weight="bold")
    ax.set_ylim(-len(rows) + 0.45, 0.55)
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.set_xlabel("share of the rebuilt energy")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=col) for _, _, col in KINDS]
    fig.legend(handles, [w for w, _, _ in KINDS], loc="lower left", bbox_to_anchor=(0.01, 0.6 / h),
               ncol=3, frameon=False, fontsize=S.FONT - 1, handlelength=1.2, columnspacing=1.2)  # fmt: skip
    caption(fig, ["Descriptive (no rule): each direction's class is automatic, hand-checked on five items per model "
                  "(9B, 27B, Muse). Some 'no scene word' directions are spellings of the bridge the classifier missed. "
                  "Lightning hatched: its gate was chosen after its 60-scene pre-check was seen."], 0.5)  # fmt: skip
    S.save(fig, out_name)
    return out_name
