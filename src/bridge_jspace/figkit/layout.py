"""The figure sets and their folders. figures/ is by track (Dan, 8 Nov): figures/breadth/{readme,examples},
figures/depth/{readme,ledger,examples}, figures/common/{readme,writeup,examples}; a set's name is its folder under
figures/ ("depth/ledger"). Every set is flat and numbered (Dan, 7 Nov). A figure's file is named by its place in its
document: the write-up and the breadth README number their figures (Fig. 5a → 05a_…, the write-up's appendix in order
→ a01_…, the key → 00_key); the other sets are numbered in reading order (01_…; the depth README's supplementary
figures sNN_…). Beside the PNGs: README.md (the index), _meta/ (the styles-plot sidecars, the caption stores,
order.txt, problems.json) and _sheets/ (the contact sheets). The figure ids (the registry's) do not change.
common/examples holds cards that span both tracks; it is empty for now (Dan: keep it).

ORDER is the one list per set; the builders save through `path`, the index and the sheets read `order`.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
FIGURES = REPO / "figures"
META, SHEETS = "_meta", "_sheets"

# reading order; a ("supp", id) entry is a depth supplementary figure, ("appendix", id) the write-up's appendix
ORDER: dict[str, list[tuple[str, str]]] = {
    "common/writeup": [("key", "key"),
                # the setup section's examples (figkit/writeup_sp_d.py), in the post's order, before the results
                *(("setup", i) for i in ("setup_twins", "setup_locker", "setup_patch", "setup_knockout", "setup_datasets")),
                ("main", "fig00_schematic"),
                # Result 1's first section ends on one figure of its claims (figkit/writeup_sp_c.py), before Figure 3
                ("result", "patch_split"), ("result", "patch_layers"),
                *(("main", i) for i in (
                    "fig01_main_split", "fig02_datasets", "fig03_tools", "fig04_twin_set",
                    "fig05a_controls_band", "fig05b_controls_layer", "fig06_nine_models", "fig07_routes",
                    "fig08a_address_read_remove", "fig08b_address_swap_lens", "fig09_order", "fig10_answer_span",
                    "fig11_orthogonal", "fig12_pointer", "fig13_last_token")),
                *(("appendix", i) for i in (
                    "figA1_agents", "appB_f5_atoms", "appB_f14a_position_route", "appB_f14b_identity_route",
                    "appB_f9_where", "appB_f12_order", "appB_f8_facts", "appB_f8_directions", "appB_f15_link_crossover",
                    "appB_f17_attention", "appB_f17b_heads", "appB_f18_code_tool", "appB_f19_six_lockers"))],
    "common/readme": [("main", i) for i in (
        "p0b_tools", "r1_c1_split", "r1_c1_gaps", "f2_controls", "f2_controls_layer", "f2_controls_more", "r4_pointer", "f5_atoms", "f6a_address_read_remove",
        "f6b_address_swap_lens", "r5_routes", "f10_sentence_order", "f14_two_codes", "f11_monitor", "r3_last_token",
        "f3_nine_models", "f8_directions", "f8_facts", "f12_order", "f9_where")],
    "depth/readme": [*(("main", i) for i in (
        "fig00_setup", "r1_dan_split", "fig09b_six_lockers", "fig21_code_tool", "fig03_order", "fig03c_link_layers",
        "fig06_depth", "fig06d_depth_more", "t12_two_by_two", "fig15_mechanisms", "fig01b_settings",
        "fig02_specificity", "fig02b_k_curve", "fig02c_k_routes", "fig01c_zeroing", "fig16a_dose_lens",
        "fig16b_dose_rest", "fig05b_identity_outside", "fig05c_described_bridge", "fig03b_layers",
        "fig06c_address_depth", "fig07c_probe_errors", "fig08_first_locker", "fig09c_formation", "fig09d_chain",
        "fig10_what_is_left", "fig10b_enrichment", "fig10c_binding", "fig10c2_binding_added", "fig10d_heads",
        "fig10e_second_route", "fig13_attention", "fig14_learned", "fig09_transfer", "fig24_two_codes",
        # docs pass P2-4 (7 Nov): the figures of claims 3 and 7, appended so no later file is renumbered
        "fig03d_earlier_mention", "fig05e_address_added_alone")),
              *(("supp", i) for i in (
                  "s01_split_all_scene_sets", "s02_parts_all", "s03_order_split", "s03d_link_copy_variants", "s03f_link_copy_27b", "s03g_link_copy_muse",
                  "s03e_cumulative", "s07_recall_follows_swap", "s07b_lens_readout",
                  "s08b_pointer_moves_and_neutral_sentence", "s04_routes_design", "s05a_routes_taken_out",
                  "s05b_routes_kept", "s12_das_muse"))],
    # the ledger cards' figures (figkit/depth_sp_f.py), in docs/depth/EXPERIMENTS.md's order
    "depth/ledger": [("main", i) for i in (
        "fig40_item_not_answer", "fig41_lightning_layers", "fig42_ladder", "fig43_follows_both",
        "fig44_number_answer", "fig45_answer_map", "fig46_value_formats", "fig47_identity_code", "fig48_subset27b",
        "fig49_report_first_position", "fig50_last_token_swap", "fig51_last_conflict", "fig52_last_conflict_words",
        "fig53_attention_blocks", "fig54_fact_answer_control", "fig55_every_layer", "fig56_fact_routes",
        "fig57_read_window", "fig58_person_probe", "fig59_any_item", "fig60_described_gap")],
    "breadth/readme": [("main", i) for i in (
        "fig01_needed", "fig02_datasets", "fig02b_datasets", "fig03a_robust", "fig03b_robust",
        "fig04_where", "fig05_carries", "fig07_lookup", "fig08_readable", "fig09_dose",
        "fig10a1_beyond", "fig10a2_beyond", "fig10b_beyond", "fig10c_beyond")],
    # real items as images (scripts/examples.py), by track, in the root README's reading order
    "depth/examples": [("main", i) for i in ("e1_locker_scene", "e4_routes", "e5_address")],
    "breadth/examples": [("main", i) for i in ("e2_fact_passage", "e3_chains")],
    "common/examples": [],
}  # fmt: skip
NUMBERED = {"common/writeup", "breadth/readme"}  # sets whose document numbers its figures (figNN[a] → NN[a]_)
_PREFIX = re.compile(r"^(?:fig(?P<n>\d+)(?P<x>[a-z]\d?)?|figA\d+|appB_f\d+[a-z]?|s\d+[a-z]?|f\d+[a-z]?|r\d+|t\d+|p\d+[a-z]?|e\d+)_")


# a figure that belongs to the one before it (a fold under it): the previous number with "b", "c", ..., so later
# numbers stay
SUB = {"r1_c1_gaps", "f2_controls_layer", "f2_controls_more"}
# short names the id would give badly (a person's name, an old claim code)
STEM = {"fig04_twin_set": "made_up_fact_set", "r1_c1_split": "main_split", "r1_c1_gaps": "main_split_gaps", "r1_dan_split": "one_layer_split"}


def short(fid: str) -> str:
    """The id without its old numbering prefix: fig05a_controls_band → controls_band."""
    return STEM.get(fid, _PREFIX.sub("", fid))


def names(group: str) -> dict[str, str]:
    """Figure id → file stem for a set, in reading order."""
    out, counts = {}, {"main": 0, "appendix": 0, "supp": 0, "setup": 0, "result": 0}
    prev, sub = "", 0
    for kind, fid in ORDER[group]:
        if kind == "key":
            out[fid] = "00_key"
            continue
        if fid in SUB:
            sub += 1
            out[fid] = f"{prev}{chr(ord('a') + sub)}_{short(fid)}"
            continue
        sub = 0
        counts[kind] += 1
        m = _PREFIX.match(fid)
        if kind == "main" and group in NUMBERED and m and m.group("n") is not None:
            num = f"{int(m.group('n')):02d}{m.group('x') or ''}"
        else:
            num = {"main": "", "appendix": "a", "supp": "s", "setup": "e", "result": "r"}[kind] + f"{counts[kind]:02d}"
        out[fid] = f"{num}_{short(fid)}"
        prev = num
    if len(set(out.values())) != len(out):
        raise ValueError(f"{group}: two figures share a file name")
    return out


def folder(group: str) -> Path:
    return FIGURES / group


def path(group: str, fid: str) -> Path:
    return folder(group) / f"{names(group)[fid]}.png"


def order(group: str) -> list[str]:
    """The figure ids of a set in reading order."""
    return [fid for _kind, fid in ORDER[group]]


def write_order(group: str) -> Path:
    """_meta/order.txt: one file name a line, in reading order (for `styles-plot sheet --order`)."""
    p = folder(group) / META / "order.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(f"{names(group)[fid]}.png\n" for fid in order(group)))
    return p


TITLES = {"common/writeup": "the LessWrong write-up", "common/readme": "the root README",
          "depth/readme": "the depth README", "depth/ledger": "the depth ledger (docs/depth/EXPERIMENTS.md)",
          "depth/examples": "the depth track's real examples", "breadth/examples": "the breadth track's real examples",
          "common/examples": "real examples that span both tracks",
          "breadth/readme": "the breadth README"}  # fmt: skip


def status(group: str, stem: str) -> str:
    """One line from the figure's sidecar: post hoc / descriptive / not claimed cells, and UNVERIFIED (no figure is
    hand-checked against its run files yet)."""
    import json

    side = folder(group) / META / f"{stem}.styles.json"
    cells = json.loads(side.read_text()).get("cells", {}) if side.exists() else {}
    timing = [c["timing"] for c in cells.values()]
    claims = [c["claim"] for c in cells.values()]
    parts = []
    if timing and all(t == "post_hoc" for t in timing):
        parts.append("all post hoc")
    elif "post_hoc" in timing:
        parts.append(f"{timing.count('post_hoc')} of {len(timing)} cells post hoc")
    for word in ("descriptive", "not_claimed"):
        if word in claims:
            parts.append(f"{claims.count(word)} {word.replace('_', ' ')}")
    return " · ".join([*parts, "UNVERIFIED"])


def write_index(group: str, shows: dict[str, str] | None = None) -> Path:
    """figures/<set>/README.md: every figure in reading order with a thumbnail, what it shows and its status. What it
    shows: `shows[fid]` if given, else the first sentence of the figure's caption in _meta/captions.toml (a figure
    without one raises KeyError: every figure has a caption, tests/test_figure_layout.py)."""
    from bridge_jspace.figkit import captions  # captions imports this module

    up = "../" * (len(Path(group).parts) + 1)  # from figures/<track>/<set>/ back to the repo root
    lines = [f"# Figures for {TITLES[group]}", "",
             f"Built by `make {'figures-writeup' if group == 'common/writeup' else 'readme'}` with "
             f"[styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml]({up}plotstyle.toml); "
             f"statuses: [data/figures/status.csv]({up}data/figures/status.csv)). File names follow the document's "
             "order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.", "",
             "| № | figure | what it shows | status |", "|---|---|---|---|"]  # fmt: skip
    if not names(group):  # common/examples, kept empty (Dan, 8 Nov): the root README's "Examples" link lands here
        lines = [f"# Figures for {TITLES[group]}", "",
                 "Example cards that span both tracks go here; none does yet. The real examples are by track: "
                 "[depth](../../depth/examples/README.md) (a locker scene, a routes scene) and "
                 "[breadth](../../breadth/examples/README.md) (a fact passage, three-hop chains)."]
    for fid, stem in names(group).items():
        num = stem.split("_", 1)[0]
        what = (shows or {}).get(fid) or captions.first_sentence(captions.caption(group, stem))
        what = what.replace("|", "\\|")  # a bare pipe would split the table cell
        lines.append(f'| {num} | <a href="{stem}.png"><img src="{stem}.png" width="260" alt="{stem}"></a> | '
                     f"{what} | {status(group, stem)} |")  # fmt: skip
    p = folder(group) / "README.md"
    p.write_text("\n".join(lines) + "\n")
    return p


def build(group: str, figs: dict, target: str, ids=None, shows: dict[str, str] | None = None) -> list[str]:
    """Save each figure of a set strict into its numbered file (sidecar under _meta/), then its order and index;
    returns the failures (a failed figure writes nothing)."""
    import styles_plot as sp

    failed = []
    for fid in order(group):
        if ids and not any(fid.startswith(i) for i in ids):
            continue
        try:
            sp.save(figs[fid](), path(group, fid), target=target, root=folder(group))
            print(f"ok    {group}/{names(group)[fid]}  ({fid})")
        except (sp.StyleError, sp.BuildError, ValueError) as e:
            failed.append(fid)
            print(f"FAIL  {group}/{fid}\n{e}")
    write_order(group)
    write_index(group, shows)
    return failed
