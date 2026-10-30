"""The table-style figures (the dot table, Dan's references r1-r5, the deck's f2-f12, the depth README's own) for a
target.

uv run python -m bridge_jspace.figkit.tables                   # the root README's, figures/readme/ (160 dpi)
uv run python -m bridge_jspace.figkit.tables --target slide    # the same, figures/slides/ (200 dpi)
uv run python -m bridge_jspace.figkit.tables --target depth    # docs/depth/README.md's, figures/depth/ (160 dpi)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import depth_figs as DF
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit import lint
from bridge_jspace.figkit.build import page_sheet
from bridge_jspace.figkit.data import REPO

OUT = {"readme": REPO / "figures" / "readme", "slide": REPO / "figures" / "slides", "depth": REPO / "figures" / "depth"}
DPI = {"readme": 160, "slide": 200, "depth": 160}
FIGS = {"r1_c1_split": X.r1_split, "r3_last_token": X.r3_last_token,
        "r4_pointer": X.r4_pointer, "r5_routes": X.r5_routes, "f2_controls": F.f_controls, "f2_main": F.f_main, "f3_nine_models": F.f_nine,
        "f5_atoms": F.f_atoms, "f6_address": F.f_address, "f8_directions": F.f_directions, "f8_facts": F.f_facts,
        "f9_where": F.f_where, "f11_monitor": F.f_monitor, "f12_order": F.f_order, "r1_dan_split": X.r1_dan_split,
        "t12_two_by_two": DF.two_by_two, "p0a_datasets": DF.datasets, "p0b_tools": DF.tools}  # fmt: skip
DEPTH = ("r1_dan_split", "f5_atoms", "f12_order", "f6_address", "f11_monitor", "r3_last_token", "t12_two_by_two")
TARGET = {"readme": [i for i in FIGS if i not in ("r1_dan_split", "t12_two_by_two", "f2_main")], "depth": list(DEPTH)}
# p0a_datasets: the root README's datasets figure (Dan 30 Oct: the table style, no title inside)
TARGET["slide"] = [*TARGET["readme"], "f2_main"]  # f2_main: the deck's one-panel f2 (Dan 30 Oct), slides only; f2_controls is its appendix

CLAIMS = {  # the alt text in the root README (scripts/readme_root.py)
    "r1_c1_split": "Taking the lens part out breaks recalled answers, not lookup ones",
    "r3_last_token": "At the last token the lens reads the entity, and the answer does not go through it",
    "r4_pointer": "Another entity's lens part moves the recall from any context, a probe's subspace that reads the fact does not",
    "r5_routes": "The patch moves the lookup by identity or by position, never by the value",
    "f2_controls": "Random, rotated, logit-lens and PCA directions cost far less than the lens part",
    "f3_nine_models": "Across nine models the lens part is carried, needed, or both: graded",
    "f5_atoms": "The lens part's 25 directions are the two bridge words, almost never the answer word",
    "f6_address": "A probe reads the address, removing the lens part leaves it, a swap moves the lookup, the lens misses it",
    "f8_directions": "With more lens directions removed, the 27B's lookup has more switches blocked",
    "f8_facts": "On passages whose fact the model knows, the lookup follows the lens part; with made-up facts, less so",
    "f9_where": "Middle layers need the bridge's mention; deeper layers, the question",
    "f11_monitor": "At the last token the lens part reads the address worse than a random part of the same energy",
    "f12_order": "With the question before the scene, the 27B's lookup leans a little more on the lens part; the other models missed the gate",
    "p0a_datasets": "One question, two kinds of answer, two datasets.",
    "p0b_tools": "Three tools, one target: the lens part at the bridge.",
}
assert set(CLAIMS) == set(TARGET["readme"])

PROBLEMS: list[str] = []


def _check(fig, path) -> None:
    PROBLEMS.extend(lint.table_problems(fig, Path(path).stem, need_xlabel=True, need_cue=True))


def build(target: str, ids: list[str] | None = None) -> list[str]:
    T.BEFORE_SAVE = _check
    out = OUT[target]
    out.mkdir(parents=True, exist_ok=True)
    X.OUT, F.DPI = str(out), DPI[target]
    done = []
    for i in TARGET[target]:
        if ids and not any(i.startswith(x) for x in ids):
            continue
        FIGS[i]()
        done.append(i)
    return done


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--target", choices=sorted(OUT), default="readme")
    a = ap.parse_args()
    for i in build(a.target, a.ids):
        print("wrote", OUT[a.target] / f"{i}.png")
    print("\n".join(PROBLEMS) or "lint: clean")
    if not a.ids:
        page_sheet([OUT[a.target] / f"{i}.png" for i in TARGET[a.target]], OUT[a.target] / "contact_sheet_tables.png")
