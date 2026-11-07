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
            if m == "nemotron-3.5-lightning":
                lightning_note("fig01_main_split (band test)")
        out.append(by_hollow("fig01_main_split", f"layer.{k}", m, what="one layer, the conflict test"))
    return out


def fig04() -> list[dict]:
    lightning_note("fig04_twin_set")
    out = []
    for m in TWIN:
        k = SHORT[m]
        for cond in ("paper10", "paper10_rot", "paper10_keepA"):
            for reader in ("recall", "lookup"):
                out.append(row("fig04_twin_set", f"{reader}.{cond}.{k}", "fixed_in_advance",
                               "the twin set's readings, fixed in advance (note 41)", f"{README} Fig. 4 row"))  # fmt: skip
        for cond in ("paper10", "paper10_rot"):
            out.append(row("fig04_twin_set", f"gap.{cond}.{k}", "fixed_in_advance",
                           "the twin set's gap, fixed in advance (note 41)", f"{README} Fig. 4 row"))  # fmt: skip
        DISAGREEMENTS.append(f"answer span kept ({k}): {README} Fig. 4 says fixed in advance (note 41); its Fig. 10 "
                             "row says the keep is a descriptive number under a fixed label (note 41 keep table)")
    return out


def fig09() -> list[dict]:
    out = []
    for m, _ in MODELS:
        k = SHORT[m]
        for ds in ("locker", "facts"):
            for when in ("first", "after"):
                out.append(by_hollow("fig09_order", f"{ds}.{when}.{k}", m, what="sentence order"))
    return out


def lightning_note(fig: str) -> None:
    DISAGREEMENTS.append(f"Lightning in {fig}: {README} says fixed in advance (no post hoc mark); figkit/data.py hollow() "
                         "says Lightning is post hoc everywhere. The registry keeps the README's status.")


def fig12() -> list[dict]:
    lightning_note("fig12_pointer")
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
        if m == "nemotron-3.5-lightning":
            DISAGREEMENTS.append("Lightning in fig05_controls: the figkit figure drew its cells filled; "
                                 "figkit/data.py hollow() says Lightning is post hoc everywhere. Kept as drawn.")
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
    for k in ("q9", "q27", "mu", "nl"):  # appB_f9's models
        for band_ in ("mid", "late"):
            for j in range(3):
                out.append(fixed("appB_f9_where", f"{band_}.{j}.{k}", "where in the prompt", f"{src}writeup_appendix.py"))
    for m in TWIN:
        k = SHORT[m]
        out.append(fixed("fig10_answer_span", f"keep.{k}", "keep the answer span", f"{src}writeup_figs.py"))
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


def rows() -> list[dict]:
    writeup = [*key(), *fig01(), *fig04(), *fig09(), *fig12(), *appB_f17(), *styles_plot_port()]
    return [*writeup, *readme_set(writeup)]


if __name__ == "__main__":
    rs = rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0]))
        w.writeheader()
        w.writerows(rs)
    print(f"wrote {len(rs)} rows to {OUT.relative_to(REPO)}")
    (OUT.parent / "status_disagreements.txt").write_text("\n".join(sorted(set(DISAGREEMENTS))) + "\n")
    for d in sorted(set(DISAGREEMENTS)):
        print("disagreement:", d)
