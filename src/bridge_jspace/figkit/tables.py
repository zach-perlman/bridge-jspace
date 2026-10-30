"""The table-style figures (the dot table, Dan's references r1-r5 and the deck's f2-f12) for a target.

uv run python -m bridge_jspace.figkit.tables                   # figures/readme/ (160 dpi)
uv run python -m bridge_jspace.figkit.tables --target slide    # figures/slides/ (200 dpi)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit import lint
from bridge_jspace.figkit.build import page_sheet
from bridge_jspace.figkit.data import REPO

OUT = {"readme": REPO / "figures" / "readme", "slide": REPO / "figures" / "slides"}
DPI = {"readme": 160, "slide": 200}
FIGS = {"r1_c1_split": X.r1_split, "r2_address": X.r2_address, "r3_last_token": X.r3_last_token,
        "r4_pointer": X.r4_pointer, "r5_routes": X.r5_routes, "f2_controls": F.f_controls, "f3_nine_models": F.f_nine,
        "f5_atoms": F.f_atoms, "f6_address": F.f_address, "f8_breaks": F.f_breaks, "f9_where": F.f_where,
        "f11_monitor": F.f_monitor, "f12_order": F.f_order}  # fmt: skip


PROBLEMS: list[str] = []


def _check(fig, path) -> None:
    PROBLEMS.extend(lint.table_problems(fig, Path(path).stem))


def build(target: str, ids: list[str] | None = None) -> list[str]:
    T.BEFORE_SAVE = _check
    out = OUT[target]
    out.mkdir(parents=True, exist_ok=True)
    X.OUT, F.DPI = str(out), DPI[target]
    done = []
    for i, f in FIGS.items():
        if ids and not any(i.startswith(x) for x in ids):
            continue
        f()
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
        page_sheet([OUT[a.target] / f"{i}.png" for i in FIGS], OUT[a.target] / "contact_sheet_tables.png")
