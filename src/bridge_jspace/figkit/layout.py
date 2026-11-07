"""The four figure sets and their folders (Dan, 7 Nov): every figures/<set>/ is flat and numbered. A figure's file is
named by its place in its document: the write-up and the breadth README number their figures (Fig. 5a → 05a_…, the
write-up's appendix in order → a01_…, the key → 00_key); the root README and the depth README are numbered in reading
order (01_…; the depth README's supplementary figures sNN_…). Beside the PNGs: README.md (the index), _meta/ (the
styles-plot sidecars, order.txt) and _sheets/ (the contact sheets). The figure ids (the registry's) do not change.

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
    "writeup": [("key", "key"),
                *(("main", i) for i in (
                    "fig00_schematic", "fig01_main_split", "fig02_datasets", "fig03_tools", "fig04_twin_set",
                    "fig05a_controls_band", "fig05b_controls_layer", "fig06_nine_models", "fig07_routes",
                    "fig08a_address_read_remove", "fig08b_address_swap_lens", "fig09_order", "fig10_answer_span",
                    "fig11_orthogonal", "fig12_pointer", "fig13_last_token")),
                *(("appendix", i) for i in (
                    "figA1_agents", "appB_f5_atoms", "appB_f14a_position_route", "appB_f14b_identity_route",
                    "appB_f9_where", "appB_f12_order", "appB_f8_facts", "appB_f8_directions", "appB_f15_link_crossover",
                    "appB_f17_attention", "appB_f17b_heads", "appB_f18_code_tool", "appB_f19_six_lockers"))],
    "readme": [("main", i) for i in (
        "p0b_tools", "r1_c1_split", "r1_c1_gaps", "f2_controls", "f2_controls_layer", "r4_pointer", "f5_atoms", "f6a_address_read_remove",
        "f6b_address_swap_lens", "r5_routes", "f10_sentence_order", "f14_two_codes", "f11_monitor", "r3_last_token",
        "f3_nine_models", "f8_directions", "f8_facts", "f12_order", "f9_where")],
    "depth": [*(("main", i) for i in (
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
    "breadth": [("main", i) for i in (
        "fig01_needed", "fig02_datasets", "fig02b_datasets", "fig03a_robust", "fig03b_robust",
        "fig04_where", "fig05_carries", "fig07_lookup", "fig08_readable", "fig09_dose",
        "fig10a1_beyond", "fig10a2_beyond", "fig10b_beyond", "fig10c_beyond")],
    # real items as images, picked by a stated rule (scripts/examples.py), in the root README's reading order
    "examples": [("main", i) for i in ("e1_locker_scene", "e2_fact_passage", "e4_routes", "e3_chains")],
}  # fmt: skip
NUMBERED = {"writeup", "breadth"}  # sets whose document numbers its figures (figNN[a] → NN[a]_)
_PREFIX = re.compile(r"^(?:fig(?P<n>\d+)(?P<x>[a-z]\d?)?|figA\d+|appB_f\d+[a-z]?|s\d+[a-z]?|f\d+[a-z]?|r\d+|t\d+|p\d+[a-z]?|e\d+)_")


# a figure that belongs to the one before it (a fold under it): the previous number with "b", so later numbers stay
SUB = {"r1_c1_gaps", "f2_controls_layer"}
# short names the id would give badly (a person's name, an old claim code)
STEM = {"r1_c1_split": "main_split", "r1_c1_gaps": "main_split_gaps", "r1_dan_split": "one_layer_split"}


def short(fid: str) -> str:
    """The id without its old numbering prefix: fig05a_controls_band → controls_band."""
    return STEM.get(fid, _PREFIX.sub("", fid))


def names(group: str) -> dict[str, str]:
    """Figure id → file stem for a set, in reading order."""
    out, counts = {}, {"main": 0, "appendix": 0, "supp": 0}
    prev = ""
    for kind, fid in ORDER[group]:
        if kind == "key":
            out[fid] = "00_key"
            continue
        if fid in SUB:
            out[fid] = f"{prev}b_{short(fid)}"
            continue
        counts[kind] += 1
        m = _PREFIX.match(fid)
        if kind == "main" and group in NUMBERED and m and m.group("n") is not None:
            num = f"{int(m.group('n')):02d}{m.group('x') or ''}"
        else:
            num = {"main": "", "appendix": "a", "supp": "s"}[kind] + f"{counts[kind]:02d}"
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


DOCS = {"readme": REPO / "README.md", "depth": REPO / "docs/depth/README.md", "breadth": REPO / "docs/breadth/README.md",
        "examples": REPO / "README.md"}  # fmt: skip
TITLES = {"writeup": "the LessWrong write-up", "readme": "the root README", "depth": "the depth README",
          "examples": "the root README's real examples",
          "breadth": "the breadth README"}  # fmt: skip
_LINK = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+?\.png)\)")


def shown_in_doc(group: str) -> dict[str, str]:
    """File stem → the words its document gives it (an image's alt text, else a link's text), first use."""
    out: dict[str, str] = {}
    doc = DOCS.get(group)
    if doc is None:
        return out
    for text, target in _LINK.findall(doc.read_text()):
        stem = Path(target).stem
        if f"figures/{group}/" in target and text and text not in ("Figure",) and stem not in out:
            out[stem] = text
    return out


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
    """figures/<set>/README.md: every figure in reading order with a thumbnail, what it shows and its status."""
    words = {**shown_in_doc(group), **(shows or {})}
    lines = [f"# Figures for {TITLES[group]}", "",
             f"Built by `make {'figures-writeup' if group == 'writeup' else 'readme'}` with "
             "[styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../plotstyle.toml); "
             "statuses: [data/figures/status.csv](../../data/figures/status.csv)). File names follow the document's "
             "order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.", "",
             "| № | figure | what it shows | status |", "|---|---|---|---|"]  # fmt: skip
    for fid, stem in names(group).items():
        num = stem.split("_", 1)[0]
        what = words.get(stem) or words.get(fid, "")
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
