"""docs/writeup/figure_map.md: the post's figures in order, for swapping them in the Google Doc by hand: number, section,
file, caption (read from the caption stores, figures/<set>/_meta/captions.toml, its numbers rendered as on the READMEs, src comments dropped) and what changed
against the deck figure the Doc shows now (the figkit versions as of 25d7b48e).

uv run python scripts/writeup_figure_map.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from bridge_jspace.figkit import captions  # noqa: E402
from scripts import readme_root as RR  # noqa: E402  the captions' markers rendered as on the READMEs

OUT = REPO / "docs/writeup/figure_map.md"
F1, F2, F3, F4 = ("Finding 1: recall needs the lens part", "Finding 2: lookup runs on codes outside the lens",
                  "Finding 3: recall needs its answer's own directions",
                  "Finding 4: a lens reading reports associations, not use")  # fmt: skip

# (number, section, [(set, file stem)], what changed against the deck figure)
ROWS = [
    ("top", "TL;DR, under the title", [("common/writeup", "00_schematic")],
     "Same scene and three parts, now coloured words with dots instead of squares; each arrow carries its label"),
    ("key", "How to read the numbers", [("common/writeup", "00_key")],
     "Roles in two columns with no \"mention\" or \"question\" colours (neutral is now a quantity of no role, such "
     "as a difference); every control named; one example row (Qwen 27B's band test) read aloud, \"removing the lens "
     "part everywhere\""),
    ("result", "Result 1, end of its first section, after \"For the lookup, the same four-layer removal costs nothing.\"",
     [("common/writeup", "r01_patch_split"), ("common/writeup", "r02_patch_layers")],
     "New: the section's claims in two figures, panels (A) the patch at one layer and (B) the answer word in r01, (C) one layer against four on the ladder's one-pick scenes in r02; (A) draws the same keys as Figure 3's right panel"),
    ("1", F1, [("common/writeup", "01_main_split")],
     "Whiskers span the full interval (the deck's were one-sided); the gap is slate, not black; the one-layer header "
     "reads \"switches blocked beyond random\"; the largest control is a grey tick, not a number in brackets (the old "
     "caption's \"in brackets\" no longer applies); not-claimed tags under the band panels"),
    ("setup", "Setup: fact passages, after the bullets", [("common/writeup", "e01_setup_twins")],
     "New: a pair of twins (the Rovio pair the post quotes), every sentence verbatim from items.jsonl"),
    ("setup", "Setup: locker scenes, after the bullets", [("common/writeup", "e02_setup_locker")],
     "New: the carbon scene and its two questions (illustrative)"),
    ("setup", "Setup: the Patch subsection, after its first paragraph",
     [("common/writeup", "e03_setup_patch")],
     "The depth report's patch picture moved to the post: +Δ on the bridge word, − and + into Δ, the changed words marked"),
    ("2", "Setup: the two datasets",
     [("common/writeup", "02_datasets"), ("depth/examples", "01_locker_scene"), ("breadth/examples", "01_fact_passage")],
     "The prompt table is unchanged in content; the example cards E1 and E2 are new: real items picked by a stated "
     "rule, each reader's answer under each operation"),
    ("3", "Setup: the three tools", [("common/writeup", "03_tools")],
     "Grids over a real scene's last words (bridge word in bold) instead of blank cells; one teal box per test; the "
     "swap is teal (a lens part), not blue; panel titles Knock-out, Patch and Swap, as in the post's table"),
    ("setup", "Setup: the Knock-out subsection, after the controls", [("common/writeup", "e04_setup_knockout")],
     "New: the knock-out and its rotated control on the Rovio pair (Qwen 27B), with the known-fact set's rates; the pair is the one the post quotes, the second item of its section (the first names Russian figures), not picked by outcome"),
    ("setup", "Setup: known-fact set and made-up-fact set, after the table and the note under it", [("common/writeup", "e05_setup_datasets")],
     "New: both sets as illustrations in each set's format (the made-up-fact example is the documented one)"),
    ("4", F1, [("common/writeup", "04_made_up_fact_set")],
     "Three labelled lanes per model (knock-out, rotated, answer span kept) instead of colour words; the answer-span "
     "lanes are tagged descriptive; the gap is slate with full whiskers"),
    ("5", F1, [("common/writeup", "05a_controls_band"), ("common/writeup", "05b_controls_layer")],
     "Split into two figures (band of layers, one layer); one column per control on the same scale; the post embeds "
     "both where it embedded fig05_controls"),
    ("6", F1, [("common/writeup", "06_nine_models")],
     "Rows in three bands by the bar fixed before the main runs; the gap against the bar of 30, "
     "and each same-size control in its own panel against the limit of 10; the probability gap, the swap and the "
     "100-direction runs move to the Appendix E3 table (data/figures/writeup/appendix_e3.csv)"),
    ("7", F2, [("depth/examples", "02_routes"), ("common/writeup", "07_routes")],
     "The stack has no whiskers and no numbers in the bars; the position share's interval and the number's share sit "
     "in columns beside it; the E4 card shows the lockers each route predicts on a real scene"),
    ("8", F2, [("common/writeup", "08a_address_read_remove"), ("common/writeup", "08b_address_swap_lens")],
     "The layout-only probe is a grey dot (was a tick); the removal is a dumbbell to its random control; \"item "
     "change\" reads \"a change of item\"; no left-pointing cue"),
    ("9", F2, [("common/writeup", "09_order")],
     "Two labelled lanes per model (sentence before, after the pick); full whiskers; no zero line"),
    ("10", F3, [("common/writeup", "10_answer_span")],
     "The random keep is a grey dot with its value; descriptive tags on the keep cells; the matched-share notes "
     "under their cells"),
    ("11", F3, [("common/writeup", "11_orthogonal")],
     "Panels swapped (the data-built subspace first, with its bar fixed in advance); the orthogonal arm is a hollow "
     "slate dot (post hoc); colour words instead of legend lines"),
    ("12", F4, [("common/writeup", "12_pointer")],
     "Two tables in one figure (was two pasted images); full whiskers; the difference is signed, its interval not"),
    ("13", F4, [("common/writeup", "13_last_token")],
     "A column with the lens part's value; the whole state swapped in is a named grey control"),
    ("A1", "Appendix A: agents", [("common/writeup", "a01_agents")],
     "Dots in the recall's colour throughout; descriptive cells tagged in grey words (no longer grey dots)"),
    ("B1", "Appendix B", [("common/writeup", "a02_atoms")],
     "One dot column per word type (old bridge word, new bridge word, another scene word, no scene word) and the "
     "answer word's share"),
    ("B2", "Appendix B", [("common/writeup", "a03_position_route")],
     "The top half of appB_f14_two_codes as its own figure; all estimates post hoc, said once in the key"),
    ("B3", "Appendix B", [("common/writeup", "a04_identity_route")],
     "The bottom half of appB_f14_two_codes as its own figure; all estimates post hoc"),
    ("B4", "Appendix B", [("common/writeup", "a05_where")], "Values print in the points unit's decimals; a grey rotated dot per cell"),
    ("B5", "Appendix B", [("common/writeup", "a06_order")],
     "Two labelled lanes per model (question after, before the scene) instead of shades; gate words in the cells"),
    ("B6", "Appendix B", [("common/writeup", "a07_facts")], "Two labelled lanes (true facts, made-up facts); made-up values printed"),
    ("B7", "Appendix B", [("common/writeup", "a08_directions")], "One column per number of directions on the grey band"),
    ("B8", "Appendix B", [("common/writeup", "a09_link_crossover")],
     "Two lookup lines named at their ends; the cells fixed in advance as points with whiskers; a grey post-hoc tag "
     "per panel; no numbers-only table"),
    ("B9", "Appendix B", [("common/writeup", "a10_attention")],
     "Four labelled lanes per model; both controls grey and named; the colour word reads \"address swap\""),
    ("B10", "Appendix B", [("common/writeup", "a11_heads")],
     "The bar fixed in advance as a labelled dashed rule; the values in two columns"),
    ("B11", "Appendix B", [("common/writeup", "a12_code_tool")],
     "Redrawn from the depth figure: each arm in its own column against a random part; \"below gate\" where the "
     "9B's code probe was not run"),
    ("B12", "Appendix B", [("common/writeup", "a13_six_lockers")],
     "Pairs as dots and a count column instead of bars; the shift vector's whisker is the range over start lockers"),
]  # fmt: skip

HEAD = """<!-- Generated by scripts/writeup_figure_map.py from the caption stores; edit the script or the stores. -->
# Write-up figure map: what goes where in the Google Doc

For swapping the post's figures by hand (agents do not edit the Doc): in the post's order, each figure's number, the
section it sits in, the file to upload, its caption, and what changed against the deck figure the Doc shows now (the
figkit versions as of `25d7b48e`). Files are in `figures/common/writeup/` unless the path names another folder
under `figures/` (the example cards, `depth/examples/` and `breadth/examples/`).

- **Captions** come from one store per set (`figures/common/writeup/_meta/captions.toml`, `figures/{depth,breadth}/examples/_meta/captions.toml`);
  the same text is in each set's index (`figures/<track>/<set>/README.md`) and under each figure on the contact sheet
  `docs/review/writeup_contact_sheet.png`.
- **Sections** follow the order of results in the finishing-pass brief (Finding 1 recall needs the lens part,
  2 lookup runs on codes outside the lens, 3 recall needs its answer's own directions, 4 a lens reading reports
  associations, not use); check each against the Doc's own headings.
- **Figure 1's old caption** ("in brackets, the largest same-size control's gap") no longer applies: the largest
  same-size control is a grey tick on the gap's axis.
- **Tag (proposed, not created):** `v1.0-writeup` at the commit that closes the finishing pass, once the Doc shows
  these files. The write-up PNGs last changed at `7e0e3c03`; their captions at this map's commit. For Dan:
  `git tag -a v1.0-writeup <commit> -m "Figures and text as in the LessWrong post" && git push origin v1.0-writeup`.

| № | section | file | caption | changed against the deck figure |
|---|---|---|---|---|
"""


def cell(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text).replace("|", "\\|").strip()


def main() -> None:
    lines = []
    for num, section, files, change in ROWS:
        names = "<br>".join(f"`{'' if s == 'common/writeup' else s + '/'}{stem}.png`" for s, stem in files)
        caps = "<br><br>".join(cell(RR.render(captions.caption(s, stem))) for s, stem in files)
        lines.append(f"| {num} | {section} | {names} | {caps} | {cell(change)} |")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HEAD + "\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(REPO)}: {len(ROWS)} rows")


if __name__ == "__main__":
    main()
