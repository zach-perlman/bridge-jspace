"""The table-style figures (the dot table, Dan's references r1-r5, the deck's f2-f12, the depth README's own) for a
target.

uv run python -m bridge_jspace.figkit.tables                   # the root README's, figures/readme/ (160 dpi)
uv run python -m bridge_jspace.figkit.tables --target slide    # the same, figures/slides/ (200 dpi)
uv run python -m bridge_jspace.figkit.tables --target depth    # docs/depth/README.md's, figures/depth/ (160 dpi)
uv run python -m bridge_jspace.figkit.tables --target writeup  # the LessWrong post's, figures/writeup/ (8 in, 200 dpi)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from bridge_jspace.figkit import claim_figs as CF
from bridge_jspace.figkit import curve_figs as CV
from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import depth_figs as DF
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit import grammar as GR
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import writeup_address as WA
from bridge_jspace.figkit import writeup_appendix as WP
from bridge_jspace.figkit import writeup_claims as WC
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit import writeup_intro as WI
from bridge_jspace.figkit import readme_sp as RS
from bridge_jspace.figkit import writeup_sp as SP
from bridge_jspace.figkit import writeup_v2 as W2
from bridge_jspace.figkit.build import page_sheet
from bridge_jspace.figkit.data import REPO
from bridge_jspace.figkit.theme import WRITEUP, WRITEUP_ASPECT, WRITEUP_MIN_ROW

OUT = {"readme": REPO / "figures" / "readme", "slide": REPO / "figures" / "slides", "depth": REPO / "figures" / "depth",
       "writeup": REPO / "figures" / "writeup"}  # fmt: skip
DPI = {"readme": 160, "slide": 200, "depth": 160, "writeup": WRITEUP.dpi}
# the LessWrong post's figures in post order, then the appendix in the brief's order; the file names are fixed (the post
# embeds figures/writeup/<id>.png)
WRITEUP_MODULES = (W, WI, WA, WC, WP, W2)  # W2 last: its grammar v2 figures replace the v1 ones of the same name
_WFIGS = {k: v for m in WRITEUP_MODULES for k, v in m.FIGS.items()}
WRITEUP_ORDER = ("key", "fig00_schematic", "fig01_main_split", "fig02_datasets", "fig03_tools", "fig04_twin_set", "fig05_controls",
                 "fig06_nine_models", "fig07_routes", "fig08a_address_read_remove", "fig08b_address_swap_lens",
                 "fig09_order", "fig10_answer_span", "fig11_orthogonal", "fig12_pointer", "fig13_last_token",
                 "figA1_agents", "appB_f5_atoms", "appB_f14_two_codes", "appB_f9_where", "appB_f12_order",
                 "appB_f8_facts", "appB_f8_directions", "appB_f15_link_crossover", "appB_f17_attention", "appB_f17b_heads",
                 "appB_f18_code_tool", "appB_f19_six_lockers")  # fmt: skip
assert set(WRITEUP_ORDER) == set(_WFIGS), set(WRITEUP_ORDER) ^ set(_WFIGS)
WRITEUP_FIGS = {k: _WFIGS[k] for k in WRITEUP_ORDER}
FIGS = {"r1_c1_split": X.r1_split, "r3_last_token": X.r3_last_token,
        "r4_pointer": X.r4_pointer, "r5_routes": X.r5_routes, "f2_controls": F.f_controls, "f2_main": F.f_main, "f3_nine_models": F.f_nine,
        "f5_atoms": F.f_atoms, "f6_address": F.f_address, "f8_directions": F.f_directions, "f8_facts": F.f_facts,
        "f9_where": F.f_where, "f10_sentence_order": CF.f_sentence_order, "f10a_order_main": CF.f_order_main, "f10b_order_2x2": CF.f_order_2x2, "f15_link_crossover": CV.f_link_crossover, "f13b_depth_curves": CV.f_depth_curves, "f13c_depth_curves_all": CV.f_depth_curves_all, "f16_ladder": CV.f_ladder, "f17_attention": CV.f_attention, "f18_code_tool": CF.f_code_tool, "f19_six_lockers": CF.f_six_lockers, "f6a_address_read_removed": lambda: F.f_address("read_removed"), "f6b_address_swap_lens": lambda: F.f_address("swap_lens"), "f13_depth_anatomy": CF.f_depth, "f14_two_codes": CF.f_two_codes, "f11_monitor": F.f_monitor, "f12_order": F.f_order, "r1_dan_split": X.r1_dan_split,
        "t12_two_by_two": DF.two_by_two, "p0a_datasets": DF.datasets, "p0b_tools": DF.tools,
        **WRITEUP_FIGS}  # fmt: skip
DEPTH = ("r1_dan_split", "f5_atoms", "f12_order", "f6_address", "r5_routes", "f11_monitor", "r3_last_token", "t12_two_by_two")
TARGET = {"readme": [i for i in FIGS if i not in WRITEUP_FIGS and i not in ("r1_dan_split", "t12_two_by_two", "f2_main", "f10a_order_main", "f10b_order_2x2", "f6a_address_read_removed", "f6b_address_swap_lens", "f15_link_crossover", "f13b_depth_curves", "f13c_depth_curves_all", "f16_ladder", "f17_attention", "f18_code_tool", "f19_six_lockers")], "depth": list(DEPTH)}
# p0a_datasets: the root README's datasets figure (Dan 30 Oct: the table style, no title inside)
TARGET["slide"] = [*(i for i in TARGET["readme"] if i != "f10_sentence_order"), "f2_main", "f10a_order_main", "f10b_order_2x2", "f6a_address_read_removed", "f6b_address_swap_lens", "f15_link_crossover", "f13b_depth_curves", "f13c_depth_curves_all", "f16_ladder", "f17_attention", "f18_code_tool", "f19_six_lockers"]  # f2_main: the deck's one-panel f2 (Dan 30 Oct), slides only; f2_controls is its appendix
# the styles-plot figures (figkit/writeup_sp.py) are not built here
TARGET["writeup"] = [i for i in WRITEUP_FIGS if i not in SP.FIGS]

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
    "f10_sentence_order": "The bridge word redirects the lookup when the locker sentence came first; both orders matter (post hoc)",
    "f13_depth_anatomy": "The address is readable before the lookup uses it; the 27B's full grid misses the handoff rule",
    "f14_two_codes": "Without the address the position route goes; without J++ the identity route turns to position (post hoc)",
    "f12_order": "With the question before the scene, the 27B's lookup leans a little more on the lens part; the other models missed the gate",
    "p0a_datasets": "One question, two kinds of answer, two datasets.",
    "p0b_tools": "Three tools, one target: the lens part at the bridge.",
}
assert set(CLAIMS) == set(TARGET["readme"])
# the styles-plot figures (figkit/readme_sp.py) are not built here
# p0a_datasets is a markdown table in the README now (Dan, 7 Nov: text belongs in text)
TARGET["readme"] = [i for i in TARGET["readme"] if i not in RS.FIGS and i != "p0a_datasets"]
TARGET["depth"] = [i for i in TARGET["depth"] if i not in RS.FIGS]

PROBLEMS: list[str] = []


MIN_PT = {"writeup": WRITEUP.label}  # the write-up's floor: nothing under 11 pt


def build(target: str, ids: list[str] | None = None) -> list[str]:
    min_pt = MIN_PT.get(target, 0.0)

    def before_save(fig, path):
        axis = Path(path).stem != "key"  # the key figure's axes are illustrations of marks, not panels
        probs = lint.table_problems(fig, Path(path).stem, need_xlabel=axis, need_cue=axis, min_pt=min_pt)
        if GR.FIGURE["defer_key"]:  # an upper stacked panel: the last panel's key names its marks
            probs = [p for p in probs if not p.endswith(W.HOLLOW_NO_KEY)]
        PROBLEMS.extend(probs)
        if target == "writeup":  # text never crosses a line or a mark (the write-up's rule)
            PROBLEMS.extend(lint.crossings(fig, Path(path).stem))
            if GR.FIGURE["id"] in W2.FIGS:  # grammar v2's meaning checks
                PROBLEMS.extend(GR.check(fig, Path(path).stem))

    T.BEFORE_SAVE = before_save
    out = OUT[target]
    out.mkdir(parents=True, exist_ok=True)
    X.OUT, F.DPI = str(out), DPI[target]
    CF.OUT, CF.DPI = str(out), DPI[target]
    CV.OUT, CV.DPI = str(out), DPI[target]
    for m in WRITEUP_MODULES:
        m.OUT = str(out)
        m.PROBLEMS.clear()
    CV.PROBLEMS.clear()
    fs, min_row, gap, vbox = dict(T.FS), T.MIN_ROW_H, T.VALUE_GAP, T.VALUE_BOX
    if target == "writeup":
        T.FS.update(W.FS)
        T.MIN_ROW_H = WRITEUP_MIN_ROW
        T.VALUE_GAP, T.VALUE_BOX = W.VALUE_GAP, False
    done = []
    try:
        for i in TARGET[target]:
            if ids and not any(i.startswith(x) for x in ids):
                continue
            GR.FIGURE["id"] = ""  # a v1 figure: no grammar v2 check unless it calls grammar.begin
            FIGS[i]()
            done.append(i)
            if target == "writeup":
                PROBLEMS.extend(lint.png_problems(out / f"{i}.png", round(W.WIDTH * DPI[target]), WRITEUP_ASPECT))
    finally:
        T.FS.clear()
        T.FS.update(fs)
        T.MIN_ROW_H, T.VALUE_GAP, T.VALUE_BOX = min_row, gap, vbox
    PROBLEMS.extend(CV.PROBLEMS)
    for m in WRITEUP_MODULES:
        PROBLEMS.extend(m.PROBLEMS)
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
        pngs = [OUT[a.target] / f"{i}.png" for i in TARGET[a.target]]
        if a.target == "writeup":  # the contact sheets come from `styles-plot sheet` (Makefile figures-writeup)
            for fid, fails in sorted(GR.CVD.items()):  # check 8: reported with the numbers, never fixed silently
                for kind, ra, rb, d, floor in fails:
                    print(f"colour vision: {fid}: {ra}-{rb} under {kind}: CIEDE2000 {d} < {floor}")
        else:
            page_sheet(pngs, OUT[a.target] / "contact_sheet_tables.png")
    if a.target == "writeup" and PROBLEMS:
        raise SystemExit(1)
