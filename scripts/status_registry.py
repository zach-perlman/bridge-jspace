"""Write data/figures/status.csv, the styles-plot status registry (plotstyle.toml [registry]): one row per (figure, cell)
a figure draws, with its timing (fixed_in_advance, post_hoc), its claim (claimed, descriptive, not_claimed with its
reason), the reason and the source of that status. Built as (status, tag) rows and converted on writing (convert).

The statuses are read from the rules the figures already followed, each cited in `source`:
- figkit/data.hollow: Lightning post hoc everywhere, the 122B post hoc where its gate was lowered;
- the band test's post hoc models, Muse 30B and Qwen 122B (figures/common/writeup/README.md, Fig. 1 and 5), and the two whose
  split the post does not claim (writeup_figs.NOT_CLAIMED);
- figures/common/writeup/README.md's "fixed in advance / post hoc" column for the rest.
Where two sources disagree, both rows are kept in DISAGREEMENTS (printed and written to the report), not resolved.

uv run python scripts/status_registry.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from bridge_jspace import figdata as D  # noqa: E402
from bridge_jspace import figdata as WF  # noqa: E402
from bridge_jspace.palette import MODELS  # noqa: E402

OUT = REPO / "data" / "figures" / "status.csv"
README = "figures/common/writeup/README.md"
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
        # descriptive (no rule fixed in advance), said once in the caption instead of a tag on every row (Dan, 10 Nov)
        out.append(row("fig10_answer_span", f"keep.{k}", "fixed_in_advance", f"{ANSWER_SPAN}; descriptive, said in the "
                       "caption, not tagged on the figure", f"{DAN_7NOV}; Dan 10 Nov"))  # fmt: skip
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
    """The root README's figures (figkit/readme_sp.py). A README figure that draws a write-up figure (readme_sp.ALIAS,
    COPIES) takes that figure's rows under the README's id, its "not claimed" tags included (Dan, 8 Nov, Q2a: the tags
    mark the edge of the claim, so the two copies show the same statuses). The others keep the hollow rule their figkit
    builder drew, cited."""
    from bridge_jspace.figkit.readme_sp import ALIAS, COPIES

    src = "src/bridge_jspace/figkit/"
    out = []
    for fid, wid in {**ALIAS, **COPIES}.items():
        rs = [r for r in writeup if r["figure"] == wid]
        out += [{**r, "figure": fid, "source": f"{r['source']} (as {wid}, drawn for README.md)"} for r in rs]
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
BREADTH = {  # (figure, cell prefix) -> the registration it cites
    ("fig01_main_split", "band."): CHAIN, ("r1_c1_split", "band."): CHAIN, ("key", "band."): CHAIN,
    ("fig05_controls", "band."): CHAIN, ("fig05a_controls_band", "band."): CHAIN, ("f2_controls", "band."): CHAIN,
    ("fig12_pointer", ""): CHAIN, ("r4_pointer", ""): CHAIN,
    ("t12_two_by_two", "t12.2."): CHAIN, ("t12_two_by_two", "t12.3."): CHAIN,
    ("fig06_nine_models", ""): CHAIN, ("f3_nine_models", ""): CHAIN,
}  # fmt: skip


def _reg(line: str, committed: str, run: str, started: str) -> str:
    return (f"{PREREG}: \"{line}\" (first committed {committed}); Lightning's run {run} started {started} "
            "(manifest written_utc)")  # fmt: skip


# Dan, 8 Nov (Q2b): a Lightning cell of fig04, fig10, fig11 is fixed in advance only if a registration committed before
# its run started names the test and the model (or states a rule whose words cover the cell); else post hoc. Commit
# times: the oldest commit holding the registration's heading (git log --all -S); run starts: the run's manifest.
_N41 = _reg("Amendment 67 ... Models: 9B, 27B, Lightning ... Note 41: random-span placebo and output-side check for "
            "note 37", "2026-10-30T08:06:54Z", "results/ablate_v2/nem35l_jsuite_v4_test_chat_ko41_cand2_v1",
            "2026-10-30T08:29:29Z")  # fmt: skip
_N50 = _reg("Amendment 72 ... notes 49-55 ... One deterministic run per model: 9B, 27B and Lightning",
            "2026-10-30T09:09:40Z", "results/ablate_v2/nem35l_jsuite_v4_test_chat_ko49_cand2_v1", "2026-10-30T12:13:41Z")
_N57 = _reg("Amendment 79 ... note 57 on Lightning and the 27B", "2026-10-30T12:28:40Z",
            "results/ablate_v2/nem35l_jsuite_v4_test_chat_ko57_cand2_v1", "2026-10-30T13:43:39Z")
_N68 = _reg("Amendment 89, addendum ... note 68 on the 9B and Lightning (confirmatory)", "2026-10-30T23:38:36Z",
            "results/ablate_v2/nem35l_jsuite_v5al_test_chat_ko57_cand2_v1", "2026-10-31T00:00:38Z")
_N62 = _reg("Note 62 ... 9B and Lightning primary", "2026-10-30T18:28:05Z", "results/sd_necessity/nem35l_sd62_ko_test_v1",
            "2026-10-30T18:58:17Z")
_N67 = _reg("Note 67 (as decided) ... 9B primary, Lightning confirmatory", "2026-10-30T19:39:34Z",
            "results/sd_necessity/nem35l_sd67_ko_test_v1", "2026-10-30T21:21:03Z")
_N59 = _reg("Note 59: safety-relevant agent settings ... 9B test and dev primary, Lightning confirmatory",
            "2026-10-30T17:20:51Z", "results/sd_necessity/nem35l_sd59_ko_test_v1", "2026-10-30T17:41:33Z")
_N65 = _reg("Note 65 (as decided): generate vs verify a single claim ... 9B primary, Lightning confirmatory",
            "2026-10-30T19:39:34Z", "results/sd_necessity/nem35l_sd65_ko_test_v1", "2026-10-30T20:53:52Z")
Q2B = {  # (figure, cell prefix) -> the registration it rests on (every one committed before the run started)
    ("fig04_twin_set", "recall.paper10"): _N41, ("fig04_twin_set", "lookup.paper10"): _N41,
    ("fig04_twin_set", "gap."): _N41, ("fig10_answer_span", "keep."): _N41,
    ("fig10_answer_span", "keep_ctrl."): _N50, ("fig10_answer_span", "remove.v4."): _N57,
    ("fig10_answer_span", "remove.codename."): _N68,
    ("fig11_orthogonal", "onehop.city."): _N62, ("fig11_orthogonal", "onehop.answers."): _N62,
    ("fig11_orthogonal", "subspace."): _N67,
    # figA1 (Q2c reversed, Dan 8 Nov): the agent arms follow the same rule; copy / pick / produce read note 59's run,
    # verify note 65's (data/figures/writeup/data.csv sources); copy stays descriptive (its registered role)
    ("figA1_agents", "copy."): _N59, ("figA1_agents", "pick."): _N59, ("figA1_agents", "produce."): _N59,
    ("figA1_agents", "verify."): _N65,
}  # fmt: skip
DEPTH_FIGS = {"fig08a_address_read_remove", "fig08b_address_swap_lens", "f6_address", "fig13_last_token",
              "f6a_address_read_remove", "f6b_address_swap_lens", "fig07_routes", "r5_routes", "appB_f18_code_tool",
              "r3_last_token", "r1_dan_split", "fig05b_controls_layer", "fig01b_settings", "fig01c_zeroing",
              "fig02_specificity", "fig05b_identity_outside", "fig05c_described_bridge", "fig07c_probe_errors",
              "fig09d_chain", "fig21_code_tool", "fig14_learned", "fig08_first_locker", "fig09_transfer",
              "fig10_what_is_left", "fig15_mechanisms", "s01_split_all_scene_sets", "s02_parts_all",
              "s03_order_split", "s08b_pointer_moves_and_neutral_sentence", "fig09c_formation", "fig10e_second_route",
              "s05a_routes_taken_out", "s05b_routes_kept", "s03e_cumulative", "fig16a_dose_lens", "fig16b_dose_rest",
              "s12_das_muse", "fig10c_binding", "fig10c2_binding_added", "fig10d_heads", "s07_recall_follows_swap",
              "s07b_lens_readout", "fig02b_k_curve", "fig02c_k_routes", "fig03b_layers", "s03d_link_copy_variants", "s03f_link_copy_27b", "s03g_link_copy_muse",
              "fig06_depth", "fig06d_depth_more", "fig06c_address_depth", "fig10b_enrichment"}  # fmt: skip
DEPTH_PREFIX = (("t12_two_by_two", "t12.0."), ("t12_two_by_two", "t12.1."))


def lightning(rows_: list[dict]) -> list[dict]:
    out = []
    for r in rows_:
        if not r["cell"].endswith(".nl"):
            out.append(r)
            continue
        fig, cell = r["figure"], r["cell"]
        cite = next((c for (f, pre), c in BREADTH.items() if f == fig and cell.startswith(pre)), None)
        q2b = next((c for (f, pre), c in Q2B.items() if f == fig and cell.startswith(pre)), None)
        if q2b is not None:  # the claim (descriptive) stays; the timing follows the registration
            r = {**r, "status": r["status"] if r["status"] == "descriptive" else "fixed_in_advance",
                 "reason": "Lightning: a registration committed before the run names the test and the model",
                 "source": f"{q2b}; Dan 8 Nov (Q2b)"}  # fmt: skip
        elif cite is not None:
            if r["status"] == "descriptive":
                out.append(r)
                continue
            r = {**r, "status": "fixed_in_advance", "reason": "Lightning's breadth test, registered before its data",
                 "source": f"{cite}; Dan 7 Nov (decision 8)"}  # fmt: skip
        elif fig in DEPTH_FIGS or cell.startswith("layer.") or any(f == fig and cell.startswith(p) for f, p in DEPTH_PREFIX):
            r = {**r, "status": "post_hoc", "reason": "Lightning's depth test: after the data",
                 "source": "Dan 7 Nov (decision 8): depth tests post hoc; figkit/data.py hollow()"}  # fmt: skip
        elif fig == "figA1_agents":  # derive: no Lightning run of this arm, so the figure draws no mark
            r = {**r, "reason": "no Lightning run of this arm; the figure draws no mark"}
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
        out += [{**r, "figure": fid, "source": f"{r['source']} (as {wid}, drawn for docs/depth)"}
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


def depth_set_c() -> list[dict]:
    """The depth README's last figures (figkit/depth_sp_c.py): fixed in advance where the test has a rule number set
    before its data (47.0, 47.4, 47.6, 48.1, 48.3, 48.4, 48.5, 51.1, 45k's routes arm), after the data where the story
    builders say so (scripts/readme_story_figures.py s07_recall_follows_swap, f02b_k (a)); the routes test's arms as
    the routes figures (hollow() with the lowered gate: the 122B's runs after the data)."""
    from bridge_jspace.figkit.depth_sp_c import S03E_SETS, S05_ARMS

    rs_, b48 = "scripts/readme_story_figures.py", "scripts/story_b48.py"
    fixed_cells = (("fig09c_formation", "formation", "47.6 (b)", "scripts/story_b47b.py build_47_6"),
                   ("fig10e_second_route", "route2", "48.5", f"{b48} build_second_route"),
                   ("fig16a_dose_lens", "dose", "51.1 A", f"{rs_} fig16_dose"),
                   ("fig16b_dose_rest", "dose", "51.1 B", f"{rs_} fig16_dose"),
                   ("s12_das_muse", "learned", "48.1", f"{rs_} s12"),
                   ("fig10c_binding", "binding", "48.3", f"{b48} build_binding"),
                   ("fig10c2_binding_added", "binding", "48.3", f"{b48} build_binding"),
                   ("fig10d_heads", "heads", "48.4", f"{b48} build_heads"),
                   ("s07b_lens_readout", "readout", "47.0", f"{rs_} s07b_lens_readout"),
                   ("fig02c_k_routes", "kcurve", "45k's routes test", f"{rs_} f02b_k (b)"))  # fmt: skip
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        for fid, cid, rule, src in fixed_cells:
            out.append(fixed(fid, f"{cid}.{k}", f"{rule}, set before its data", src))
        for s, _label in S03E_SETS:
            out.append(fixed("s03e_cumulative", f"cumulative.{s}.{k}", "47.4, set before its data",
                             "scripts/story_b47b.py SEGMENTS"))  # fmt: skip
        out.append(post_hoc("s07_recall_follows_swap", f"follows.{k}", "supplementary to E6, after the data",
                            f"{rs_} s07_recall_follows_swap"))  # fmt: skip
        out.append(post_hoc("fig02b_k_curve", f"kcurve.{k}", "(a) the main test at 25, 50, 100 directions, after the "
                            "data", f"{rs_} f02b_k (a)"))  # fmt: skip
        for fid, arms in (("s05a_routes_taken_out", S05_ARMS[:5]), ("s05b_routes_kept", S05_ARMS[5:])):
            for arm, _label in arms:
                out.append(by_hollow(fid, f"routes.{arm}.{k}", m, lowered=True, what="the routes test's arms"))
    return out


def depth_set_d() -> list[dict]:
    """The depth README's sweeps (figkit/depth_sp_d.py): 45q's cells fixed in advance and its layer sweeps post hoc
    (as appB_f15: curve_figs.f_link_crossover drew them open); 47.8 fixed in advance, Lightning and the 122B after the
    data (their gates chosen after: hollow() with the lowered gate); 48.2 fixed in advance; D4 under the rule its
    builder states (scripts/story_b47c.py build_depth), not dated there: listed."""
    from bridge_jspace.figkit.depth_sp_d import S03D

    src, cv = "scripts/readme_story_figures.py", "src/bridge_jspace/figkit/curve_figs.py f_link_crossover (open marks)"
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        for arm in ("a", "c", "d"):
            out.append(fixed("fig03b_layers", f"arm.{arm}.{k}", "rule 45q's cells fixed in advance", f"{src} f03b_layers"))
        for tag in ("bridge", "copy"):
            out.append(post_hoc("fig03b_layers", f"sweep.{tag}.{k}", "the layer sweep", cv))
        out.append(fixed("s03d_link_copy_variants", f"arm.c.{k}", "rule 45q's arm c at L", f"{src} s03d_q"))
        for key, *_ in S03D:  # s03d is one figure per model's sweep (depth_sp_d.S03D_FIG)
            sweep_fig = {"q9": "s03d_link_copy_variants", "q27": "s03f_link_copy_27b", "mu": "s03g_link_copy_muse"}
            if k in sweep_fig:
                out.append(post_hoc(sweep_fig[k], f"sweep.{key}.{k}", "the layer sweep", cv))
        for fid in ("fig06_depth", "fig06d_depth_more"):
            out.append(by_hollow(fid, f"depth.{k}", m, lowered=True, what="47.8, by depth"))
        out.append(fixed("fig06c_address_depth", f"overlap.{k}", "D4, under its stated rule",
                         "scripts/story_b47c.py build_depth"))  # fmt: skip
        out.append(fixed("fig10b_enrichment", f"enrich.{k}", "48.2, set before its data", "scripts/story_b48.py "
                         "build_enrichment"))  # fmt: skip
    UNCLEAR.add("fig06c_address_depth: D4's rule is stated in its builder (story_b47c.build_depth), not dated there")
    return out


def depth_set_e() -> list[dict]:
    """The figures of claims 3 and 7 (figkit/depth_sp_e.py, docs pass P2-4): 45p fixed in advance on the 9B, 27B and
    Muse (docs/depth/EXPERIMENTS.md#t45p), Lightning below its gate and the 122B a coverage run with no prediction
    (after the data), its arm 3 (a random part of the same share, the grey dot) timed as the test; the routes test's
    keep-only arms by hollow() with the lowered gate (the 122B's runs at 0.75), as
    the address figure (writeup fig08a) draws them."""
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        for cid in ("item", "other", "random"):
            out.append(fixed("fig03d_earlier_mention", f"{cid}.{k}", "45p, set before its data",
                             "docs/depth/EXPERIMENTS.md#t45p") if k in ("q9", "q27", "mu") else
                       post_hoc("fig03d_earlier_mention", f"{cid}.{k}", "45p, below its gate or a coverage run",
                                "docs/depth/EXPERIMENTS.md#t45p; data/figures/depth/data.csv fig03c"))  # fmt: skip
        out.append(by_hollow("fig05e_address_added_alone", f"keep.{k}", m, lowered=True,
                             what="the routes test, the address added alone"))  # fmt: skip
    return out


LEDGER = "docs/depth/EXPERIMENTS.md"
# models a ledger card ran as a coverage run, with no prediction (the card says so): after the data
COVERAGE = {"t49-3": {"q27"}, "z3": {"q27", "nl"}, "t51-5": {"nl"}, "b52-b": {"nl"}, "t51-4": {"nl"}}


def depth_set_f() -> list[dict]:
    """The ledger cards' figures (figkit/depth_sp_f.py, docs pass P3-3): each card's rule was fixed in advance (its
    Rule line in docs/depth/EXPERIMENTS.md); Lightning and the 122B after the data on depth tests (hollow() with the
    lowered gate); a model the card ran as a coverage run with no prediction, after the data."""
    from bridge_jspace.figkit import depth_sp_f as DF

    out = []
    for card, fid in DF.CARD.items():
        if fid not in DF.FIGS:
            continue
        for m, _ in MODELS:
            k = SHORT[m]
            if k in COVERAGE.get(card, ()):
                out.append(row(fid, f"c.{k}", "post_hoc", f"{card}: a coverage run, no prediction",
                               f"{LEDGER}#{card}"))  # fmt: skip
            else:
                r = by_hollow(fid, f"c.{k}", m, lowered=True, what=f"{card}, its rule fixed in advance")
                r["source"] = f"{LEDGER}#{card}; {r['source']}"
                out.append(r)
    return out


BREADTH_FIGS = {"breadth_fig01_needed": ("mk", "lost"), "breadth_fig03a_robust": ("robust",), "breadth_fig03b_robust": ("robust",), "breadth_fig04_where": ("pos", "prof"),
                "breadth_fig05_carries": ("swap",), "breadth_fig09_dose": ("dose",), "breadth_fig02_datasets": ("data", "var"),
                "breadth_fig07_lookup": ("look",), "breadth_fig08_readable": ("read",)}  # fmt: skip
# per breadth model, the registration of its tests in Zach's preregistration (before that model's data); Muse 30B and
# Qwen 122B per cell (Dan, 7 Nov: fixed in advance where Amendment 1 / 34 registered the run): MU_Q122
BREADTH_CITE = {
    "q27": f"{PREREG} Amendment 33 (jsuite_v2: the 27B and 9B at their pre-registered bands, before any v2 run)",
    "q9": f"{PREREG} Amendment 33 (jsuite_v2: the 27B and 9B at their pre-registered bands, before any v2 run)",
    "ds": f"{PREREG} Amendment 39 (DeepSeek-V4-Flash and Ministral 3 14B on v2, before any non-Qwen run)",
    "mi": f"{PREREG} Amendment 39 (DeepSeek-V4-Flash and Ministral 3 14B on v2, before any non-Qwen run)",
    "nb": f"{PREREG} Amendment 40 note 1 (Nemotron 3.5 Bolt, before any Bolt run)",
    "ol": f"{PREREG} Amendment 31 (OLMo-3 32B base with its published J++)",
}
# Muse 30B and Qwen 122B (Dan, 7 Nov): a cell is fixed in advance where the preregistration registered its run. Their
# breadth cells read the v2 runs (jsuite_v2: knock-out, position, dose), which Amendments 1 (Muse: C1-graded and C2' on
# the toy set) and 34 (the 122B: J-swap and readout on module 1) do not name: those stay post hoc and are listed. The
# 122B's position-restricted v2 knock-out is registered by Amendment 36 ("before the run").
MU_Q122 = {("pos", "q122"): f"{PREREG} Amendment 36 (where the 122B's knock-out acts, position-restricted, v2; before "
                            "the run)"}  # fmt: skip
# fig02 panel B: the other models on the datasets they ran (cell other.<dataset>.<id>)
OTHER = {
    ("toy", "q32"): f"{PREREG} header, C1 (Qwen3-32B, before any of its results)",
    ("toy2", "q32"): f"{PREREG} Amendment 6 A (fresh data seed; Qwen3-32B L44-52)",
    ("toy", "mu"): f"{PREREG} Amendment 1 (Muse: C1-graded at the band chosen on its ctrl_v8 sweep)",
    ("toy", "oh7"): f"{PREREG} Amendments 6 B and 7 (the Olmo pair; a powered Olmo test)",
    ("toy", "o7"): f"{PREREG} Amendments 6 B and 7 (the Olmo pair; a powered Olmo test)",
    ("natural", "oh7"): f"{PREREG} Amendment 12 (the natural pilot on the Olmo pair)",
    ("natural", "o7"): f"{PREREG} Amendment 12 (the natural pilot on the Olmo pair)",
    ("v1", "q122"): f"{PREREG} Amendment 27 B (the 122B on module 1 at its pre-registered band)",
    ("v1", "ol"): BREADTH_CITE["ol"], ("v2", "ol"): BREADTH_CITE["ol"],
}
OTHER_CELLS = {"q32": ("toy", "toy2"), "q122": ("toy", "v1", "v2"), "mu": ("toy", "natplus", "v1", "v2"),
               "oh7": ("toy", "natural"), "o7": ("toy", "natural"), "ol": ("v1", "v2")}  # fmt: skip
# fig10a / fig10b (three hops, numbers) and fig10c (what the model says instead)
A56 = f"{PREREG} Amendment 56 A (v2 modules 2 and 3 on the 27B, 9B and Lightning; before any run)"
A57 = f"{PREREG} Amendment 57 (a powered numbers set and a second three-hop seed; before any run)"
A19 = f"{PREREG} Amendment 19 A (generation spot-check on natplus: the 27B, 9B, Muse)"
A55 = f"{PREREG} Amendment 55 (gen_spot on natplus: what Lightning says under the knock-out)"


def breadth_set(readme: list[dict]) -> list[dict]:
    """The breadth README's figures (figkit/breadth_sp.py): a cell is fixed in advance where Zach's preregistration
    registered that model's tests before its data (BREADTH_CITE; Lightning by lightning(), Amendment 45 note 2; Muse
    30B and Qwen 122B per cell, MU_Q122). Which cells each amendment covers is per model, not checked cell by cell
    (listed). The breadth README shows the root README's r4_pointer (figures/common/readme/04_pointer.png), not a copy."""
    ids = [*SHORT.values(), "ds", "mi", "nb", "ol"]  # the breadth-only models' ids (plotstyle.toml)
    out: list[dict] = []
    for fig, cids in BREADTH_FIGS.items():
        UNCLEAR.add(f"{fig}: the amendments register each model's tests; this figure's cells are not listed one by one")
        for k in ids:
            for cid in cids:
                cell = f"{cid}.{k}"
                if k in ("mu", "q122"):
                    if cite := MU_Q122.get((cid, k)):
                        out.append(row(fig, cell, "fixed_in_advance", "registered before this run", cite))
                    else:
                        out.append(row(fig, cell, "post_hoc", "a v2 run that Amendment 1 (Muse) / 34 (the 122B) does "
                                       "not register (as the write-up's Fig. 1)", f"{PREREG}; Dan 7 Nov"))  # fmt: skip
                        UNCLEAR.add(f"{fig} {cell}: post hoc; Amendments 1 (Muse) and 34 (the 122B) register other "
                                    "runs on this model, not this v2 run")  # fmt: skip
                elif k == "nl":
                    out.append(row(fig, cell, "fixed_in_advance", "Lightning's breadth test", CHAIN))
                else:
                    out.append(row(fig, cell, "fixed_in_advance", "registered before this model's data",
                                   BREADTH_CITE[k]))  # fmt: skip
    return out + breadth_new()


def breadth_new() -> list[dict]:
    """Cells of the breadth figures drawn after e7f9a9d9: fig02 panel B, fig03's never-named table, fig05 panel B,
    fig10a / fig10b / fig10c (the dataset counts, once fig00b, are a table in the breadth README)."""
    out = []
    for k, dss in OTHER_CELLS.items():  # fig02 panel B
        for ds in dss:
            cell = f"other.{ds}.{k}"
            cite = OTHER.get((ds, k)) or MU_Q122.get((ds, k))
            if cite:
                out.append(row("breadth_fig02b_datasets", cell, "fixed_in_advance", "registered before this run", cite))
            else:
                out.append(row("breadth_fig02b_datasets", cell, "post_hoc", "no amendment names this run on this model",
                               f"{PREREG}; Dan 7 Nov"))  # fmt: skip
                UNCLEAR.add(f"breadth_fig02b_datasets {cell}: no amendment names this run on this model; post hoc")
    never = {"q27": f"{PREREG} Amendment 35 note 1 (start R, the 27B; before any R item ran)",
             "q9": f"{PREREG} Amendment 37 (the 9B's R items; before any run)",
             "nl": f"{PREREG} Amendment 54 note 2 (Lightning's never-named bridge; before the run)"}  # fmt: skip
    for k, cite in never.items():  # fig03: the never-named start (R) on the three strong models
        out.append(row("breadth_fig03b_robust", f"never.{k}", "fixed_in_advance", "registered before the run", cite))
    for k in ("q9", "q27"):  # fig05 panel B: the answer direction within the swapped lens part
        out.append(row("breadth_fig05_carries", f"ans.{k}", "fixed_in_advance", "registered before the run",
                       f"{PREREG} Amendment 38 A (what the J-part at the mention carries: swap_ans, swap_noans, "
                       "swap_ans_rot; the 27B and 9B)"))  # fmt: skip
    for ds, cite in (("v2", A56), ("nb", A57)):  # fig10a: three hops; fig10b: numbers
        for k in ("q27", "nl"):
            for fig in ("breadth_fig10a1_beyond", "breadth_fig10a2_beyond"):
                out.append(row(fig, f"three.{ds}.{k}", "fixed_in_advance", "registered before the run", cite))
        for k in ("q9", "q27", "nl"):
            out.append(row("breadth_fig10b_beyond", f"num.{ds}.{k}", "fixed_in_advance", "registered before the run",
                           cite))  # fmt: skip
    for fig in ("breadth_fig10a1_beyond", "breadth_fig10a2_beyond"):
        out.append(row(fig, "three.nat3.nl", "post_hoc", "Lightning's natural three-hop set: no amendment registers it "
                       "on Lightning", f"{PREREG} Amendment 15 (three-step natural chains, the 27B)"))  # fmt: skip
    UNCLEAR.add("breadth_fig10a1/a2_beyond three.nat3.nl: Amendment 15 registers natural three-hop chains before Lightning "
                "was queued (Amendment 40); post hoc")  # fmt: skip
    for k, cite in (("q27", A19), ("q9", A19), ("nl", A55)):  # fig10c
        out.append(row("breadth_fig10c_beyond", f"gen.{k}", "fixed_in_advance", "registered before the run", cite))
    # Amendment 19 calls Muse's part "descriptive, no rule" (Dan, 7 Nov: descriptive)
    out.append(row("breadth_fig10c_beyond", "gen.mu", "descriptive", "Muse's part of the spot-check: descriptive, no "
                   "rule (Amendment 19)", f"{A19}; Dan 7 Nov"))  # fmt: skip
    return out


def unblocked_016(fig01_rows: list[dict], depth: list[dict]) -> list[dict]:
    """The write-up figures styles-plot 0.1.6 draws (figkit/writeup_sp_c.py). fig06: the answers moved per model as
    the breadth figures register them (BREADTH_CITE; Lightning by lightning()), the gap as Fig. 1's band test (its
    rows; the breadth models per BREADTH_CITE), Bolt at 100 directions and the 122B scored by probability after the
    data. fig07: the routes test is a depth test (hollow() with the lowered gate). appB_f15: the cells fixed in advance
    (rule 45q's arms a, c, d) and the layer sweep, post hoc (the figkit figure drew it open). appB_f18: the depth
    README's fig21 (its rows)."""
    src = "src/bridge_jspace/figkit/"
    f1 = {r["cell"]: r for r in fig01_rows}
    out = []
    for k in ("q9", "q27", "mu", "nl", "q122", "ds", "mi", "nb", "ol"):
        if k in BREADTH_CITE:
            out.append(row("fig06_nine_models", f"swap.{k}", "fixed_in_advance", "the swap, registered before this "
                           "model's data", BREADTH_CITE[k]))  # fmt: skip
        elif k == "nl":
            out.append(row("fig06_nine_models", "swap.nl", "fixed_in_advance", "Lightning's swap", CHAIN))
        if f"band.{k}" in f1:
            r = f1[f"band.{k}"]
            # the figure's bands carry the verdict (Dan, 10 Nov), so no "not claimed" tag under the row
            out.append({**r, "figure": "fig06_nine_models", "cell": f"gap.{k}", "tag": "", "source": f"{r['source']} (as Fig. 1)"})
        else:
            out.append(row("fig06_nine_models", f"gap.{k}", "fixed_in_advance", "the band test, registered before "
                           "this model's data", BREADTH_CITE[k]))  # fmt: skip
    for k in ("ds", "mi", "nb", "ol"):
        UNCLEAR.add(f"fig06_nine_models swap.{k} / gap.{k}: the amendment registers the model's tests, not this cell")
    out.append(post_hoc("fig06_nine_models", "swap100.nb", "Bolt at 100 directions, a second run after its data",
                        f"{src}deck_figs.py f_nine (the small dot)"))  # fmt: skip
    out.append(post_hoc("fig06_nine_models", "soft.q122", "the 122B scored by probability, after its data",
                        f"{src}writeup_address.py fig06_nine_models (its grey dot, hollow)"))  # fmt: skip
    for m, _ in MODELS:
        out.append(by_hollow("fig07_routes", f"routes.{SHORT[m]}", m, lowered=True, what="the two routes"))
    for k in ("q9", "q27", "mu"):
        for arm in ("a", "c", "d"):
            out.append(fixed("appB_f15_link_crossover", f"arm.{arm}.{k}", "rule 45q's cells fixed in advance",
                             f"{src}curve_figs.py f_link_crossover"))  # fmt: skip
        for tag in ("bridge", "copy"):
            out.append(post_hoc("appB_f15_link_crossover", f"sweep.{tag}.{k}", "the layer sweep",
                                f"{src}curve_figs.py f_link_crossover (open marks)"))  # fmt: skip
    out += [{**r, "figure": "appB_f18_code_tool", "source": f"{r['source']} (as fig21_code_tool, drawn for the "
             "write-up)"} for r in depth if r["figure"] == "fig21_code_tool"]  # fmt: skip
    return out


# patch_split (Result 1): each panel's cells take the status of the figure that already draws the same numbers
PATCH_FROM = (("patch_split", "layer", "fig01_main_split", "layer"), ("patch_split", "answer", "fig40_item_not_answer", "c"),
              ("patch_split", "energy", "fig40_item_not_answer", "c"), ("patch_layers", "rung1", "fig42_ladder", "c"),
              ("patch_layers", "rung2", "fig42_ladder", "c"), ("patch_layers", "rung5", "fig42_ladder", "c"))  # fmt: skip


def patch_split(rows_: list[dict]) -> list[dict]:
    by = {(r["figure"], r["cell"]): r for r in rows_}
    out = []
    for target, cell, fig, src in PATCH_FROM:
        for k in ("q9", "q27", "mu", "nl", "q122"):
            r = by[(fig, f"{src}.{k}")]
            out.append({**r, "figure": target, "cell": f"{cell}.{k}",
                        "reason": f"{r['reason']} (as {fig}'s {src}.{k}, the same numbers)"})
    return out


# fig06_nine_models, redrawn 10 Nov: the cells the earlier figure did not draw
A48 = ("docs/breadth/prereg_replication_1022.md Amendment 48 A (2026-10-25 20:40 UTC): probability scoring 'post hoc, on "
       "existing rows, already run, all numbers seen'")
SOFT_POST_HOC = {"q9", "q27", "mu", "mi", "ds", "q122", "ol"}  # scored after their runs (OLMo's ran 25 Oct 07:26 UTC)


def nine_models(rows_: list[dict]) -> list[dict]:
    by = {(r["figure"], r["cell"]): r for r in rows_}
    have = {(r["figure"], r["cell"]) for r in rows_}
    out = []
    for k in ("q9", "q27", "mu", "nl", "q122", "ds", "mi", "nb", "ol"):
        g = by[("fig06_nine_models", f"gap.{k}")]
        same = f"{g['reason']} (the same run as the gap)"
        # fig06 draws each control in its own panel; the README's four-test figure the larger one
        out += [{**g, "cell": f"{c}.{k}", "reason": same} for c in ("rot", "logit")]
        out.append({**g, "figure": "f3_nine_models", "cell": f"ctrl.{k}", "reason": same})
        if ("f3_nine_models", f"soft.{k}") not in have:
            out.append(post_hoc("f3_nine_models", f"soft.{k}", "scored by probability after the data", A48)
                       if k in SOFT_POST_HOC else
                       fixed("f3_nine_models", f"soft.{k}", "probability scoring defined before this model's run", A48))
    return out


# the cells fig06_nine_models draws; the probability gap, larger control and swap stay registered under f3_nine_models
NINE_DRAWN = ("gap.", "rot.", "logit.")


def rows() -> list[dict]:
    writeup = [*key(), *fig01(), *fig04(), *fig09(), *fig12(), *appB_f17(), *styles_plot_port()]
    writeup += unblocked_016(fig01(), depth_set(writeup) + depth_set_b())
    writeup += fig05_split(writeup) + f14_split(writeup)
    readme = readme_set(writeup)
    out = lightning([*writeup, *readme, *depth_set(writeup), *depth_set_b(), *depth_set_c(),
                     *depth_set_d(), *depth_set_e(), *depth_set_f(), *breadth_set(readme)])
    out = out + patch_split(out) + nine_models(out)
    out = [r for r in out if r["figure"] != "fig06_nine_models" or r["cell"].startswith(NINE_DRAWN)]
    # fig01 draws the band half only (its one-layer cells are patch_split's; they stay registered for patch_split and
    # the README's copies, which read them above). The post's reader meets fig01 before the nine-model figure, which
    # carries Muse's and the 122B's verdict (Dan, 10 Nov): no "not claimed" notes on fig01; the README's copies keep theirs
    return [{**r, "tag": ""} if r["figure"] == "fig01_main_split" else r for r in out
            if r["figure"] != "fig01_main_split" or r["cell"].startswith("band.")]


COLUMNS = ("figure", "cell", "timing", "claim", "claim_reason", "reason", "source")  # styles-plot's registry schema
NOT_CLAIMED_TAG = "not claimed: "


def convert(row: dict) -> dict:
    """A row as built here (status, tag) in the styles-plot schema: timing = post_hoc where the status is post_hoc, else
    fixed_in_advance; claim = not_claimed (its reason the tag's text) where a tag says so, descriptive where the status
    is descriptive, else claimed."""
    status, tag = row["status"], row["tag"]
    if tag and not tag.startswith(NOT_CLAIMED_TAG):
        raise ValueError(f"{row['figure']} {row['cell']}: unknown tag {tag!r}")
    if status not in ("fixed_in_advance", "post_hoc", "descriptive", "not_claimed"):
        raise ValueError(f"{row['figure']} {row['cell']}: unknown status {status!r}")
    claim = "not_claimed" if tag else "descriptive" if status == "descriptive" else "claimed"
    return {"figure": row["figure"], "cell": row["cell"],
            "timing": "post_hoc" if status == "post_hoc" else "fixed_in_advance", "claim": claim,
            "claim_reason": tag.removeprefix(NOT_CLAIMED_TAG), "reason": row["reason"], "source": row["source"]}  # fmt: skip


if __name__ == "__main__":
    rs = rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(convert(r) for r in rs)
    print(f"wrote {len(rs)} rows to {OUT.relative_to(REPO)}")
    listed = [*sorted(set(DISAGREEMENTS)), *(f"not clearly covered: {u}" for u in sorted(UNCLEAR))]
    (OUT.parent / "status_disagreements.txt").write_text("\n".join(listed) + "\n")
    for d in sorted(set(DISAGREEMENTS)):
        print("disagreement:", d)
    for u in sorted(UNCLEAR):
        print("not clearly covered:", u)
