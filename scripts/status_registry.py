"""Write data/figures/status.csv: one row per (figure, cell) a v2 figure draws, with its status (fixed_in_advance,
post_hoc, descriptive, not_claimed), its tag ("not claimed: <reason>" where the post does not claim the cell), the
reason and the source of that status (figure grammar v2, docs/shared/figure_style.md B).

The statuses are read from the rules the figures already followed, each cited in `source`:
- figkit/data.hollow: Lightning post hoc everywhere, the 122B post hoc where its gate was lowered;
- the band test's post hoc models, Muse 30B and Qwen 122B (figures/writeup/README.md, Fig. 1 and 5), and the two whose
  split the post does not claim (writeup_figs.NOT_CLAIMED);
- figures/writeup/README.md's "fixed in advance / post hoc" column for the rest.
Where two sources disagree, both rows are kept in DISAGREEMENTS (printed and written to the report), not resolved.

uv run python scripts/status_registry.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from bridge_jspace.figkit import data as D  # noqa: E402
from bridge_jspace.figkit import writeup_figs as WF  # noqa: E402
from bridge_jspace.palette import MODELS  # noqa: E402

OUT = REPO / "data" / "figures" / "status.csv"
README = "figures/writeup/README.md"
SHORT = {"qwen3.5-9b": "q9", "qwen3.6-27b": "q27", "muse-glimmer-30b": "mu", "nemotron-3.5-lightning": "nl",
         "qwen3.5-122b-a10b": "q122"}  # fmt: skip
TWIN = ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")
DISAGREEMENTS: list[str] = []
DAN_7NOV = "Dan, 7 Nov (decision 9)"
ANSWER_SPAN = "answer span kept: a descriptive number under a fixed label (note 41 keep table)"


def row(fig, cell, status, reason, source, tag=""):
    return {"figure": fig, "cell": cell, "status": status, "tag": tag, "reason": reason, "source": source}


def by_hollow(fig, cell, m, lowered=False, what=""):
    ph = D.hollow(m, lowered)
    return row(fig, cell, "post_hoc" if ph else "fixed_in_advance",
               f"{what}: {'post hoc' if ph else 'fixed in advance'} for {m}",
               f"src/bridge_jspace/figkit/data.py hollow(lowered_test={lowered})")  # fmt: skip


def fig01() -> list[dict]:
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        if k in WF.NOT_CLAIMED:
            out.append(row("fig01_main_split", f"band.{k}", "post_hoc", "the band test on this model was run after the "
                           "data (README Fig. 1: hollow)", f"{README} Fig. 1 row; docs/breadth/data.csv",
                           tag=WF.NOT_CLAIMED[k]))  # fmt: skip
        else:
            out.append(row("fig01_main_split", f"band.{k}", "fixed_in_advance", "the band test, fixed in advance on the "
                           "three models", f"{README} Fig. 1 row"))  # fmt: skip
        out.append(by_hollow("fig01_main_split", f"layer.{k}", m, what="one layer, the conflict test"))
    return out


def fig04() -> list[dict]:
    out = []
    for m in TWIN:
        k = SHORT[m]
        for cond in ("paper10", "paper10_rot", "paper10_keepA"):
            for reader in ("recall", "lookup"):
                if cond == "paper10_keepA":
                    out.append(row("fig04_twin_set", f"{reader}.{cond}.{k}", "descriptive", ANSWER_SPAN, DAN_7NOV))
                    continue
                out.append(row("fig04_twin_set", f"{reader}.{cond}.{k}", "fixed_in_advance",
                               "the twin set's readings, fixed in advance (note 41)", f"{README} Fig. 4 row"))  # fmt: skip
        for cond in ("paper10", "paper10_rot"):
            out.append(row("fig04_twin_set", f"gap.{cond}.{k}", "fixed_in_advance",
                           "the twin set's gap, fixed in advance (note 41)", f"{README} Fig. 4 row"))  # fmt: skip
    return out


def fig09() -> list[dict]:
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        for ds in ("locker", "facts"):
            for when in ("first", "after"):
                out.append(by_hollow("fig09_order", f"{ds}.{when}.{k}", m, what="sentence order"))
    return out


def fig12() -> list[dict]:
    return [row("fig12_pointer", f"{cond}.{SHORT[m]}", "fixed_in_advance", "the pointer runs, fixed in advance",
                f"{README} Fig. 12 row (no post hoc mark)")
            for m in TWIN for cond in ("swap", "neutral", "noown", "rot")]  # fmt: skip


def appB_f17() -> list[dict]:
    out = []
    for m in ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"):
        for when in ("old", "new"):
            for q in ("switched", "stayed", "nochange", "random"):
                out.append(row("appB_f17_attention", f"att.{when}.{q}.{SHORT[m]}", "fixed_in_advance",
                               "attention under the address swap; the template drew no mark hollow",
                               "src/bridge_jspace/figkit/curve_figs.py f_attention"))  # fmt: skip
    for m in ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning"):
        for q in ("top10", "random10"):
            out.append(by_hollow("appB_f17b_heads", f"heads.{q}.{SHORT[m]}", m, what="zeroing the top 10 heads"))
    return out


def fixed(fig, cell, what, source):
    return row(fig, cell, "fixed_in_advance", f"{what}: the figkit figure drew no mark hollow", source)


def post_hoc(fig, cell, what, source):
    return row(fig, cell, "post_hoc", f"{what}: the figkit figure drew it hollow (post hoc)", source)


def styles_plot_port() -> list[dict]:
    """The figures moved to styles-plot after the pilot (figkit/writeup_sp_b.py): each status is the one the figkit
    figure drew (its hollow rule, cited), so the port changes the presentation only."""
    src = "src/bridge_jspace/figkit/"
    out = []
    for m, _ in MODELS:  # Fig. 5: the band test's post hoc models hollow in every arm (writeup_figs.fig05_controls)
        k = SHORT[m]
        if k in WF.NOT_CLAIMED:
            out.append(row("fig05_controls", f"band.{k}", "post_hoc", "the band test on this model was run after the "
                           "data (as Fig. 1)", f"{src}writeup_figs.py fig05_controls zach_post_hoc",
                           tag=WF.NOT_CLAIMED[k]))  # fmt: skip
        else:
            out.append(fixed("fig05_controls", f"band.{k}", "the band test", f"{src}writeup_figs.py fig05_controls"))
        out.append(fixed("fig05_controls", f"layer.{k}", "one layer, the earlier same-size runs",
                         f"{src}writeup_figs.py fig05_controls"))  # fmt: skip
        out.append(by_hollow("fig08a_address_read_remove", f"probe.{k}", m, what="the locker probe"))
        out.append(by_hollow("fig08a_address_read_remove", f"remove.{k}", m, lowered=True, what="the address removed"))
        out.append(by_hollow("fig08b_address_swap_lens", f"swap.{k}", m, lowered=True, what="the address swap"))
        out.append(by_hollow("fig08b_address_swap_lens", f"lens.{k}", m, lowered=True, what="the lens rebuild"))
        out.append(by_hollow("fig13_last_token", f"last.{k}", m, what="the last token"))
        out.append(by_hollow("appB_f8_facts", f"facts.{k}", m, what="true and made-up facts"))
        out.append(fixed("appB_f8_directions", f"dirs.{k}", "more lens directions", f"{src}writeup_appendix.py"))
        for when in ("after", "before"):
            if D.hollow(m) or m == "qwen3.6-27b":
                out.append(post_hoc("appB_f12_order", f"{when}.{k}", "question order (the 27B's rule set after its "
                                    "cells; Lightning's gate after its pre-check)", f"{src}writeup_address.py appB_f12_order"))  # fmt: skip
            else:
                out.append(fixed("appB_f12_order", f"{when}.{k}", "question order", f"{src}writeup_address.py"))
        for tag in ("address", "lens"):
            out.append(post_hoc("appB_f14_two_codes", f"{tag}.{k}", "the two removals, every cell post hoc",
                                f"{src}writeup_claims.py appB_f14_two_codes"))  # fmt: skip
        out.append(by_hollow("appB_f19_six_lockers", f"six.{k}", m, what="six lockers"))
        out.append(by_hollow("appB_f5_atoms", f"atoms.{k}", m, what="the lens part's atoms (writeup_appendix.f5_atoms)"))
    for k in ("q9", "q27", "mu", "nl"):  # appB_f9's models
        for band_ in ("mid", "late"):
            for j in range(3):
                out.append(fixed("appB_f9_where", f"{band_}.{j}.{k}", "where in the prompt", f"{src}writeup_appendix.py"))
    for m in TWIN:
        k = SHORT[m]
        out.append(row("fig10_answer_span", f"keep.{k}", "descriptive", ANSWER_SPAN, DAN_7NOV))
        out.append(row("fig10_answer_span", f"keep_ctrl.{k}", "fixed_in_advance", "the answer span's random keep, "
                       "fixed in advance (note 50 P1)", DAN_7NOV))  # fmt: skip
        for panel in ("v4", "codename"):
            out.append(fixed("fig10_answer_span", f"remove.{panel}.{k}", "remove the answer span", f"{src}writeup_figs.py"))
        for key_ in ("city", "answers"):
            out.append(fixed("fig11_orthogonal", f"onehop.{key_}.{k}", "the one-hop question", f"{src}writeup_figs.py"))
        out.append(post_hoc("fig11_orthogonal", f"onehop.city_perp.{k}", "the city directions orthogonal to the "
                            "answers, not a reading fixed in advance on this question", f"{src}writeup_figs.py fig11"))  # fmt: skip
        out.append(fixed("fig11_orthogonal", f"subspace.{k}", "the cleaned city subspace", f"{src}writeup_figs.py"))
        for col in ("copy", "pick", "verify", "produce", "derive"):
            q = WF._quantities().get(f"figA1.{col}.{k}", "")
            if "registered role: descriptive" in q or "role: none" in q:
                out.append(row("figA1_agents", f"{col}.{k}", "descriptive", "no reading fixed in advance for this "
                               "cell (data.csv quantity)", "data/figures/writeup/data.csv"))  # fmt: skip
            else:
                out.append(fixed("figA1_agents", f"{col}.{k}", "agent transcripts", "data/figures/writeup/data.csv"))
    return out


def key() -> list[dict]:
    """The key figure draws Fig. 1's cells (the 27B's band and one-layer rows, Muse 30B's band row): their statuses."""
    f1 = {r["cell"]: r for r in fig01()}
    return [{**f1[c], "figure": "key", "tag": "", "source": f"{f1[c]['source']} (as Fig. 1; the key shows the mark only)"} for c in ("band.q27", "band.mu",
                                                                                          "layer.q27")]  # fmt: skip


def readme_set(writeup: list[dict]) -> list[dict]:
    """The root README's figures (figkit/readme_sp.py). A README figure that draws a write-up figure (readme_sp.ALIAS)
    takes its rows under the README's id, without the "not claimed" tags: the README's figkit figures never printed
    them (presentation unchanged; listed as a disagreement). The others keep the hollow rule their figkit builder drew,
    cited."""
    from bridge_jspace.figkit.readme_sp import ALIAS

    src = "src/bridge_jspace/figkit/"
    out = []
    for fid, wid in ALIAS.items():
        rs = [r for r in writeup if r["figure"] == wid]
        if any(r["tag"] for r in rs):
            DISAGREEMENTS.append(f"{fid} (README copy of {wid}): the write-up tags {', '.join(r['cell'] for r in rs if r['tag'])} "
                                 "'not claimed'; the README's figkit figure printed no tag. The README copy keeps no tag.")  # fmt: skip
        out += [{**r, "figure": fid, "tag": "", "source": f"{r['source']} (as {wid}, drawn for README.md)"} for r in rs]
    # f6_address: the write-up's Fig. 8a and 8b side by side (their cells and statuses)
    out += [{**r, "figure": "f6_address", "source": f"{r['source']} (as {r['figure']}, drawn for README.md)"}
            for r in writeup if r["figure"] in ("fig08a_address_read_remove", "fig08b_address_swap_lens")]  # fmt: skip
    for m, _ in MODELS:
        k = SHORT[m]
        out.append(by_hollow("r1_dan_split", f"layer.{k}", m, what="one layer, the conflict test"))
        out.append(by_hollow("f5_atoms", f"atoms.{k}", m, what="the lens part's atoms (deck_figs.f_atoms)"))
        out.append(by_hollow("f11_monitor", f"monitor.{k}", m, what="the address at the last token (deck_figs.f_monitor)"))
        out.append(by_hollow("f10_sentence_order", f"order.{k}", m, what="sentence order (claim_figs.f_sentence_order)"))
        for orig in ("before", "after"):
            out.append(post_hoc("f10_sentence_order", f"both.{orig}.{k}", "the two-by-two of both orders",
                                f"{src}claim_figs.py f_sentence_order (hollow=True)"))  # fmt: skip
        for j in range(4):
            out.append(by_hollow("t12_two_by_two", f"t12.{j}.{k}", m, what="both operations on both datasets"))
    for m in TWIN:
        k = SHORT[m]
        for cond in ("swap", "neutral", "noown", "rot", "probe"):
            out.append(fixed("r4_pointer", f"{cond}.{k}", "the pointer runs and the probe's subspace",
                             f"{src}exemplars.py r4_pointer"))  # fmt: skip
    return out


def fig05_split(writeup: list[dict]) -> list[dict]:
    """Fig. 5 drawn as two figures (Dan, 7 Nov): fig05a the band test's cells, fig05b the one-layer test's."""
    return [{**r, "figure": "fig05a_controls_band" if r["cell"].startswith("band.") else "fig05b_controls_layer"}
            for r in writeup if r["figure"] == "fig05_controls"]  # fmt: skip


def f14_split(writeup: list[dict]) -> list[dict]:
    """appB_f14 drawn as two figures (Dan, 7 Nov): the position route's cells and the identity route's."""
    return [{**r, "figure": "appB_f14a_position_route" if r["cell"].startswith("address.") else "appB_f14b_identity_route"}
            for r in writeup if r["figure"] == "appB_f14_two_codes"]  # fmt: skip


# Lightning's status per test (Dan, 7 Nov, decision 8): the breadth tests are fixed in advance where the
# preregistration registered Lightning's runs; the depth tests are post hoc (figkit/data.py hollow() is depth-only)
PREREG = "docs/breadth/prereg_replication_1022.md"
CHAIN = f"{PREREG} Amendment 45 note 2 (Lightning's chain: gate, profile, knock-out, swap, set before the fit)"
TWIN_NOTES = f"{PREREG} Amendment 58 notes 15 and 17, Lightning addendum"
BREADTH = {  # (figure, cell prefix) -> the registration it cites
    ("fig01_main_split", "band."): CHAIN, ("r1_c1_split", "band."): CHAIN, ("key", "band."): CHAIN,
    ("fig05_controls", "band."): CHAIN, ("fig05a_controls_band", "band."): CHAIN, ("f2_controls", "band."): CHAIN,
    ("fig12_pointer", ""): CHAIN, ("r4_pointer", ""): CHAIN,
    ("t12_two_by_two", "t12.2."): CHAIN, ("t12_two_by_two", "t12.3."): CHAIN,
    ("fig04_twin_set", ""): TWIN_NOTES, ("fig10_answer_span", ""): TWIN_NOTES, ("fig11_orthogonal", ""): TWIN_NOTES,
}  # fmt: skip
DEPTH_FIGS = {"fig08a_address_read_remove", "fig08b_address_swap_lens", "f6_address", "fig13_last_token",
              "r3_last_token", "r1_dan_split", "fig05b_controls_layer", "fig01b_settings", "fig01c_zeroing",
              "fig02_specificity", "fig05b_identity_outside", "fig05c_described_bridge", "fig07c_probe_errors",
              "fig09d_chain", "fig21_code_tool", "fig14_learned", "fig08_first_locker", "fig09_transfer",
              "fig10_what_is_left", "fig15_mechanisms", "s01_split_all_scene_sets", "s02_parts_all",
              "s03_order_split", "s08b_pointer_moves_and_neutral_sentence"}  # fmt: skip
DEPTH_PREFIX = (("t12_two_by_two", "t12.0."), ("t12_two_by_two", "t12.1."))


def lightning(rows_: list[dict]) -> list[dict]:
    out = []
    for r in rows_:
        if not r["cell"].endswith(".nl"):
            out.append(r)
            continue
        fig, cell = r["figure"], r["cell"]
        cite = next((c for (f, pre), c in BREADTH.items() if f == fig and cell.startswith(pre)), None)
        if cite is not None:
            if r["status"] == "descriptive":
                out.append(r)
                continue
            r = {**r, "status": "fixed_in_advance", "reason": "Lightning's breadth test, registered before its data",
                 "source": f"{cite}; Dan 7 Nov (decision 8)"}  # fmt: skip
            if cite == TWIN_NOTES:
                UNCLEAR.add(f"{fig}: {TWIN_NOTES} register note 15 (bridge or answer) on Lightning; whether they cover "
                            "this figure's cells is not stated cell by cell")  # fmt: skip
        elif fig in DEPTH_FIGS or cell.startswith("layer.") or any(f == fig and cell.startswith(p) for f, p in DEPTH_PREFIX):
            r = {**r, "status": "post_hoc", "reason": "Lightning's depth test: after the data",
                 "source": "Dan 7 Nov (decision 8): depth tests post hoc; figkit/data.py hollow()"}  # fmt: skip
        elif fig == "figA1_agents":
            UNCLEAR.add(f"figA1_agents ({cell}): no amendment names Lightning's agent transcripts; kept as before")
        out.append(r)
    return out


UNCLEAR: set[str] = set()


def depth_set(writeup: list[dict]) -> list[dict]:
    """The depth README's dot tables (figkit/depth_sp.py): a write-up figure under the depth id takes its rows
    (depth_sp.ALIAS); the others are fixed in advance where their test has a rule number set before the data (47.x,
    45m), else after the data, as the story builders' docstrings say (scripts/readme_story_figures.py, story_b47a)."""
    from bridge_jspace.figkit.depth_sp import ALIAS, PARTS02, PARTS05B, SETTINGS

    rs_ = "scripts/readme_story_figures.py"
    out = []
    for fid, wid in ALIAS.items():
        out += [{**r, "figure": fid, "tag": "", "source": f"{r['source']} (as {wid}, drawn for docs/depth)"}
                for r in writeup if r["figure"] == wid]  # fmt: skip
    for m, _ in MODELS:
        k = SHORT[m]
        for key, *_ in SETTINGS:
            out.append(fixed("fig01b_settings", f"{key}.{k}", "the clean one-pick scenes (45m)", f"{rs_} f01b_settings")
                       if key == "clean" else
                       post_hoc("fig01b_settings", f"{key}.{k}", "the split in another setting, after the data",
                                f"{rs_} f01b_settings"))  # fmt: skip
        for key, *_ in PARTS02:
            out.append(post_hoc("fig02_specificity", f"{key}.{k}", "the parts runs, after the data", f"{rs_} f02_specificity"))
        for key, *_ in PARTS05B:
            out.append(fixed("fig05b_identity_outside", f"{key}.{k}", "47.1, directions 26-100", "scripts/story_b47a.py")
                       if key == "d26" else
                       post_hoc("fig05b_identity_outside", f"{key}.{k}", "the parts runs, after the data",
                                "scripts/story_b47a.py build_identity"))  # fmt: skip
        for fid, cid, rule, src in (("fig01c_zeroing", "zero", "47.5", "story_b47a.py build_zero"),
                                    ("fig05c_described_bridge", "described", "47.3", "story_b47a.py build_cue"),
                                    ("fig07c_probe_errors", "errors", "47.13", "story_b47a.py build_errors"),
                                    ("fig09d_chain", "hall", "47.14", "story_b47c.py build_chain"),
                                    ("fig21_code_tool", "code", "53.7", "story_b53b.py build_code_tool"),
                                    ("fig14_learned", "learned", "51.3", "story_b51.py build_learned")):  # fmt: skip
            out.append(fixed(fid, f"{cid}.{k}", f"{rule}, set before its data", f"scripts/{src}"))
    return out


def depth_set_b() -> list[dict]:
    """The depth README's second batch (figkit/depth_sp_b.py): statuses as the story builders' docstrings state them
    (scripts/readme_story_figures.py f08_first_locker, f09_transfer, f10_left, s01_split, s02_parts, s03_order_split,
    s08b_pointer_moves; scripts/story_b48.py build_mechanisms), cited per row."""
    from bridge_jspace.figkit.depth_sp_b import REMOVALS, S01, S02, S03

    rs_, b48 = "scripts/readme_story_figures.py", "scripts/story_b48.py build_mechanisms"
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        out.append(post_hoc("fig08_first_locker", f"first.{k}", "45a, after the data", f"{rs_} f08_first_locker"))
        out.append(post_hoc("fig09_transfer", f"format.{k}", "(a) the pointer fit on simple scenes, after the data",
                            f"{rs_} f09_transfer"))  # fmt: skip
        out.append(fixed("fig09_transfer", f"refit.{k}", "(b) 45d, fixed in advance", f"{rs_} f09_transfer"))
        for lane, *_ in REMOVALS:
            out.append(post_hoc("fig10_what_is_left", f"left.{lane}.{k}", "the sanity swap's removals (both-removed "
                                "runs, batch 40; 45e on the matched scenes chosen after the data)", f"{rs_} f10_left"))  # fmt: skip
        for test in ("48.2", "48.3", "48.4", "48.5", "47.6"):
            out.append(fixed("fig15_mechanisms", f"{test}.{k}", f"{test}, every arm fixed in advance", b48))
        for row_, *_ in S01:
            out.append(post_hoc("s01_split_all_scene_sets", f"split.{row_}.{k}", "supplementary to Fig. 1; no rule set "
                                "before these settings' data", f"{rs_} s01_split"))  # fmt: skip
        for row_, *_ in S02:
            if row_ in ("wu", "embed", "rand"):
                out.append(fixed("s02_parts_all", f"part.{row_}.{k}", "the logit-lens, input-embedding and random-atom "
                                 "dictionaries from the main test, fixed in advance", f"{rs_} s02_parts"))  # fmt: skip
            else:
                out.append(post_hoc("s02_parts_all", f"part.{row_}.{k}", "the parts runs on the one-pick scenes, after "
                                    "the data", f"{rs_} s02_parts"))  # fmt: skip
        for lane, *_ in S03:
            if lane.startswith("clean"):
                out.append(fixed("s03_order_split", f"order.{lane}.{k}", "the clean one-pick scenes (45m)",
                                 f"{rs_} s03_order_split"))  # fmt: skip
            else:
                out.append(post_hoc("s03_order_split", f"order.{lane}.{k}", "the main test split by order, after the "
                                    "data", f"{rs_} s03_order_split"))  # fmt: skip
        for cid in ("moves", "shift"):
            out.append(post_hoc("s08b_pointer_moves_and_neutral_sentence", f"{cid}.{k}", "supplementary to Fig. 8, "
                                "after the data", f"{rs_} s08b_pointer_moves"))  # fmt: skip
    return out


BREADTH_FIGS = {"breadth_fig01_needed": ("mk", "lost"), "breadth_fig03_robust": ("robust",), "breadth_fig04_where": ("pos", "prof"),
                "breadth_fig05_carries": ("swap",), "breadth_fig09_dose": ("dose",), "breadth_fig02_datasets": ("data", "var"),
                "breadth_fig07_lookup": ("look",), "breadth_fig08_readable": ("read",)}  # fmt: skip
# per breadth model, the registration of its tests in Zach's preregistration (before that model's data); Muse 30B and
# Qwen 122B: their band test post hoc, as the write-up's Fig. 1 (listed as a disagreement with Amendments 1 and 34)
BREADTH_CITE = {
    "q27": f"{PREREG} Amendment 33 (jsuite_v2: the 27B and 9B at their pre-registered bands, before any v2 run)",
    "q9": f"{PREREG} Amendment 33 (jsuite_v2: the 27B and 9B at their pre-registered bands, before any v2 run)",
    "ds": f"{PREREG} Amendment 39 (DeepSeek-V4-Flash and Ministral 3 14B on v2, before any non-Qwen run)",
    "mi": f"{PREREG} Amendment 39 (DeepSeek-V4-Flash and Ministral 3 14B on v2, before any non-Qwen run)",
    "nb": f"{PREREG} Amendment 40 note 1 (Nemotron 3.5 Bolt, before any Bolt run)",
    "ol": f"{PREREG} Amendment 31 (OLMo-3 32B base with its published J++)",
}


def breadth_set(readme: list[dict]) -> list[dict]:
    """The breadth README's figures (figkit/breadth_sp.py): a cell is fixed in advance where Zach's preregistration
    registered that model's tests before its data (BREADTH_CITE; Lightning by lightning(), Amendment 45 note 2); Muse
    30B and Qwen 122B post hoc as the write-up's Fig. 1. Which cells each amendment covers is per model, not checked
    cell by cell (listed). fig06_pointer is the README's r4_pointer (its rows copied)."""
    ids = [*SHORT.values(), "ds", "mi", "nb", "ol"]  # the breadth-only models' ids (plotstyle.toml)
    out = [{**r, "figure": "breadth_fig06_pointer", "source": f"{r['source']} (as r4_pointer, drawn for docs/breadth)"}
           for r in readme if r["figure"] == "r4_pointer"]  # fmt: skip
    for fig, cids in BREADTH_FIGS.items():
        UNCLEAR.add(f"{fig}: the amendments register each model's tests; this figure's cells are not listed one by one")
        for k in ids:
            for cid in cids:
                cell = f"{cid}.{k}"
                if k in ("mu", "q122"):
                    out.append(row(fig, cell, "post_hoc", "this model's band test was run after the data (as the "
                                   "write-up's Fig. 1)", "figures/writeup/README.md Fig. 1 row"))  # fmt: skip
                    DISAGREEMENTS.append(f"{fig} {cell}: post hoc as the write-up's Fig. 1; {PREREG} Amendments 1 "
                                         "(Muse) and 34 (the 122B) registered runs on these models")  # fmt: skip
                elif k == "nl":
                    out.append(row(fig, cell, "fixed_in_advance", "Lightning's breadth test", CHAIN))
                else:
                    out.append(row(fig, cell, "fixed_in_advance", "registered before this model's data",
                                   BREADTH_CITE[k]))  # fmt: skip
    return out


def rows() -> list[dict]:
    writeup = [*key(), *fig01(), *fig04(), *fig09(), *fig12(), *appB_f17(), *styles_plot_port()]
    writeup += fig05_split(writeup) + f14_split(writeup)
    readme = readme_set(writeup)
    return lightning([*writeup, *readme, *depth_set(writeup), *depth_set_b(), *breadth_set(readme)])


if __name__ == "__main__":
    rs = rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0]))
        w.writeheader()
        w.writerows(rs)
    print(f"wrote {len(rs)} rows to {OUT.relative_to(REPO)}")
    listed = [*sorted(set(DISAGREEMENTS)), *(f"not clearly covered: {u}" for u in sorted(UNCLEAR))]
    (OUT.parent / "status_disagreements.txt").write_text("\n".join(listed) + "\n")
    for d in sorted(set(DISAGREEMENTS)):
        print("disagreement:", d)
    for u in sorted(UNCLEAR):
        print("not clearly covered:", u)
