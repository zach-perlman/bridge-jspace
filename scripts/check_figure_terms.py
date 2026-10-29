"""Retired terms on the README figures and in their captions (Dan, 27 Oct ~01:05: run it before every commit).

Fails (exit 1, one line per hit) when a retired term appears in a text the README figures draw or in a figure caption:
"first-mentioned", "part removed", "ablation", "Q45" (question numbers belong to predictions/, not figures) and run
ids (a snake_case name such as qwen35_9b_x6_routes, or a UTC stamp such as 20261026T224602Z). The figures are
scripts/readme_story_figures.py's README and supplementary figures, rendered from the run files with savefig caught (no
file is written); the captions are the figure alt texts and "*Fig. N.*" lines of docs/depth/README.md and the template
and the canonical lines of docs/drafts/readme_v5_captions.md. docs/glossary.md's word list is checked by
tests/test_readme_build.py; this script checks the retired terms only.

The joint story (Dan, 27 Oct ~15:50) adds JOINT_RETIRED, the words the root README and its figures leave to the two
reports: M, K, PK, TK, P->P->M, RM - MM, in-context read, final, J-part, J++ part, entity code, pointer, test ids
(45r, Q46.1), GAP, °, X0, paper10, s = 2; since Dan ~19:15 also "stated" (now "lookup answer"), "remove from the
change" (now "remove from the patch") and "x 100" (every joint figure counts in pp; "lookup" is allowed again).
Checked on the root README.md (its prose, alt texts and captions; HTML
comments, code spans and link targets left out) and on the joint figures (figures/shared/: scripts/joint_figures.py's
five and scripts/shared_grid.py's two grids), whose drawn texts also get RETIRED.

Dan's restructure brief (28 Oct 22:20) adds README_IDS: internal ids (47.x, Z1, C0, P2-L0, x0_necessity, rung 6, batch,
amendment) anywhere in docs/depth/README.md's visible text, except the Appendix's "where things live" line.

uv run python scripts/check_figure_terms.py
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[1]
RETIRED = {
    "first-mentioned": r"(?i)\bfirst[- ]mentioned\b",
    # Dan's v6 iteration 2 (28 Oct ~15:40) labels Fig. 5's grey bars "position, a random part removed": that one stays
    "part removed": r"(?i)(?<!random )\bparts? removed\b",
    "ablation": r"(?i)\bablat(?:e|ed|es|ing|ion|ions)\b",
    "Q45": r"\bQ45(?:\.\d+)?\b",
    "run id": r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b",
    "run stamp": r"\b\d{8}T\d{6}Z\b",
}
CAPTION_FILES = (REPO / "docs" / "depth" / "README.md", REPO / "docs" / "README.template.md")
CAPTIONS_DRAFT = REPO / "docs" / "drafts" / "readme_v5_captions.md"
ROOT_README = REPO / "README.md"
JOINT_RETIRED = {
    # a lone capital M or K (the two reports' final codes), also inside "M − K" / "M-K"
    "M / K": r"(?<![\w'’.])[MK](?![\w'’])",
    "PK / TK": r"\b[PT]K\b",
    "chain code": r"\b[PMTKAN]\s*(?:->|→)\s*[PMTKAN]\b",
    "RM / MM": r"\b(?:RM|MM)\b",
    # Dan ~19:15: "lookup answer" replaces "stated answer"; "remove from the patch" replaces "remove from the change";
    # every joint figure counts in pp, never "x 100"
    "stated": r"(?i)\bstated\b",
    "from the change": r"(?i)\bfrom the change\b",
    "x 100": r"(?<![\w.])[x×]\s?100\b",
    "in-context read": r"(?i)\bin-context read",
    "final": r"(?i)\bfinals?\b",
    "J-part": r"(?i)\bJ-parts?\b",
    "J++ part": r"J\+\+ parts?\b",
    "entity code": r"(?i)\bentity codes?\b",
    "pointer": r"(?i)\bpointers?\b",
    "test id": r"\bx?\d{2}[a-z]\b|\bQ\d+(?:\.\d+)?\b",
    "GAP": r"\bGAP\b",
    "degree sign": r"°",
    "X0": r"(?i)\bx0\b",
    "paper10": r"(?i)\bpaper10",
    "s = n": r"(?<![\w'’])s\s*=\s*\d",
}


# Dan's README v6 brief, §5 (docs/figure_plan.md "v6 style rules"), the testable part, on the README's main figures
# (readme_story_figures.README_NAMES, since v6 iteration 2) and fig15: the title is the conclusion on one line with no
# digit (no numbers, no model sizes; number words are fine); the subtitle one line, without the rule; at most two
# panels; "swap" not "write", "address" not "pointer", and none of iteration 2's retired strings
V6_FIGS = (
    "fig00_setup",
    "fig00b_marks",
    "fig01_split",
    "fig01c_zeroing",
    "fig01d_ladder",
    "fig12_two_by_two",
    "fig05b_identity_outside",
    "fig05d_routes_lens",
    "fig05_routes",
    "fig07_writes",
    "fig09b_six_lockers",
    "fig07b_verbal",
    "fig03_order",
    "fig03d_depth_map",
    "fig06b_anatomy",
    "fig11_scorecard",
    "fig05c_described_bridge",
    "fig09_transfer",
    "fig09a_transfer",
    "fig09b_refit",
    "fig13_attention",
    "fig14_learned",
    "fig15_mechanisms",
)
# E6's probe, remove / add, swap (Dan's v6 iteration 2: at most three)
V6_PANELS = {"fig07_writes": 3,
             # kept on the page as they were, smaller (Dan's v6 iteration 2): their panels stay
             "fig05c_described_bridge": 3, "fig09_transfer": 8,
             # Dan's figures brief (28 Oct ~18:30): one panel per model (9B, 27B, Muse); the 2 x 2; Fig. 3's panel on
             # Zach's passages
             "fig01d_ladder": 3, "fig06b_anatomy": 3, "fig12_two_by_two": 4, "fig03_order": 3,
             "fig09a_transfer": 3, "fig09b_refit": 3, "fig13_attention": 3,
             # Dan's Fig. 5b / 5d brief (28 Oct ~20:30): one panel per lens slice (1-25, 26-100, 1-100)
             "fig05d_routes_lens": 3}  # fmt: skip
# Dan's figures brief (28 Oct ~18:30) §1 and §5.1: a cell that was not run, failed its gate or had too few switches is
# left out and listed in one caption line under the plot; these words never stand inside a frame (a text drawn in an
# axes) of a main-page figure
FRAME_RETIRED = {"cannot report": r"(?i)\bcannot report\b"}
# Dan's figures brief (29 Oct 10:00): every per-model figure keeps four model slots; a model without a result keeps
# its slot with a short grey label ("not tested: gate 0.751", "not run", ...), so "not run" / "not tested" may now
# stand inside a frame
# §1, colour = who or what: the figures drawn in the mark system use story_style.MARK_COL's hues and greys only
MARK_FIGS = ("fig00b_marks", "fig01d_ladder", "fig12_two_by_two", "fig03_order", "fig07b_verbal", "fig09a_transfer",
             "fig09b_refit", "fig13_attention", "fig14_learned", "fig05d_routes_lens")  # fmt: skip
V6_RETIRED = {"pointer": r"(?i)\bpointers?\b", "write": r"(?i)\bwrit(?:e|es|ten|ing)\b|\bwrote\b",
              # Dan's v6 iteration 2 (28 Oct ~15:40): words no README figure draws (title, subtitle, legend, ticks,
              # annotations); the part is named, never "it"; test numbers and run names belong to predictions/
              "pronoun for the part": r"(?i)\b(?:without|only|with) it\b",
              "beside": r"(?i)\bbeside\b",
              "reading": r"(?i)\breadings?\b",
              "(band: 95%)": r"(?i)\(band: 95\s?%\)",
              "random or layout control": r"(?i)\brandom or layout control\b",
              "below random": r"(?i)\bbelow random\b",
              "lookups sent to the target locker": r"(?i)\blookups sent to the target locker\b",
              "test number": r"\b4[5-9]\.\d+\b",
              "run name": r"(?<![A-Za-z0-9])x(?:[068]_|4[578])",  # also inside qwen35_9b_x6_routes
              "C0 / C2": r"\bC[02]\b",
              # Dan's Fig. 5b / 5d brief (28 Oct ~20:30): "identity" only as "identity route", "identity answers" or
              # "identity change" (E8's positive control), never bare
              "bare identity": r"(?i)\bidentity\b(?![\s-]+(?:routes?|answers?|changes?)\b)"}  # fmt: skip
V6_SUBTITLE_RETIRED = {"rule:": r"(?i)\brule:"}  # the subtitle says the mechanics; the rule belongs to the caption
# Dan's figures rethink (28 Oct ~21:45): the dose curves, two columns (the J++ part, the rest) by one row per model
V6_FIGS += ("fig16_dose",)
V6_PANELS["fig16_dose"] = 6
MARK_FIGS += ("fig16_dose",)
# Dan's 51.10 brief (28 Oct ~22:35): the last token's read and swap bars (main page, held to the v6 rules); the per-model
# grids are supplementary (their swap grid keeps Dan's heading "Does writing through the lens change the answer?", so
# they stay off V6_FIGS) and are held to the mark system's hues
V6_FIGS += ("fig17_jspace_last_token",)
MARK_FIGS += ("fig17_jspace_last_token", "s17_jspace_grid_9b", "s17_jspace_grid_27b", "s17_jspace_grid_muse")
# Dan's restructure brief (28 Oct 22:20): the earlier mention's card shows Fig. 3c, one panel per model (9B, 27B, Muse)
V6_FIGS += ("fig03c_earlier_mention",)
V6_PANELS["fig03c_earlier_mention"] = 3
# Dan's README brief (29 Oct 08:55, decision 7): the new Part I card "What do the lens part's 25 directions stand for?"
V6_FIGS += ("fig18_atoms",)
# Dan's README brief (29 Oct 08:55, decision 1) and figures brief (10:00): Lightning is the fourth model slot, so the
# figures with one panel per model gain a panel (Fig. 16: two columns by four rows)
V6_PANELS |= {"fig01d_ladder": 4, "fig06b_anatomy": 4, "fig09a_transfer": 4, "fig09b_refit": 4, "fig16_dose": 8,
              "fig03c_earlier_mention": 5, "fig09b_six_lockers": 3}  # fmt: skip
# The same brief, §6: no internal ids in the README body (prose, headings, captions): batch test ids (47.x, 49.x,
# 51.x), Zach's test names (Z1-Z3), scene-set codes (C0-C2, P2-L0), run names (x0_necessity), the ladder's "rung 6",
# "batch", "amendment". Ids live only in the Appendix's "where things live" line and in source comments.
README_IDS = {
    "test id": r"\b(?:4\d|5[0-9])\.\d+[a-z]?\b(?![\d%])",
    "Zach's test name": r"\bZ\d\b",
    "scene-set code": r"\bC[0-9]\b|\bP\d-L\d\b",
    "run name": r"\bx\d+(?:[a-z]+\b|[a-z]?_\w+)",
    "rung number": r"(?i)\brungs? \d",
    "batch": r"(?i)\bbatch(?:es)?\b",
    "amendment": r"(?i)\bamendments?\b",
}
README_PAGE = REPO / "docs" / "depth" / "README.md"


def readme_body_lines(text: str) -> list[tuple[str, str]]:
    """(where, line) for the README's visible lines: source comments and link targets left out, and the Appendix's
    "where things live" line (the one place for paths and ids) skipped."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"(\]\()[^)]*\)", r"\1)", text)
    return [(f"{README_PAGE.name} l.{i}", line) for i, line in enumerate(text.splitlines(), 1)
            if line.strip() and "where things live" not in line]  # fmt: skip


def readme_ids(lines: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, line, kind) for each internal id on a README body line."""
    return [(where, line, kind) for where, line in lines for kind, rx in README_IDS.items() if re.search(rx, line)]


def v6_style(layout: dict[str, dict], texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(figure, text, rule) for each v6 rule a V6_FIGS figure breaks. layout: figure -> {"title", "subtitle", "panels"}
    (figure_texts fills it); texts: (figure, drawn text)."""
    out = []
    for name in V6_FIGS:
        lay = layout.get(name)
        if lay is None:
            out.append((name, "", "not drawn"))
            continue
        title, sub = lay["title"], lay["subtitle"]
        if not title.strip():
            out.append((name, title, "no title"))
        if re.search(r"\d", title):
            out.append((name, title, "digit in the title"))
        if "\n" in title:
            out.append((name, title, "title over one line"))
        if "\n" in sub:
            out.append((name, sub, "subtitle over one line"))
        out += [(name, sub, term) for term, rx in V6_SUBTITLE_RETIRED.items() if re.search(rx, sub)]
        if lay["panels"] > V6_PANELS.get(name, 2):
            out.append((name, str(lay["panels"]), "more than two panels" if name not in V6_PANELS else
                        f"more than {V6_PANELS[name]} panels"))  # fmt: skip
    out += [(where, text, term) for where, text in texts if where in V6_FIGS
            for term, rx in V6_RETIRED.items() if re.search(rx, text)]  # fmt: skip
    return out


def frame_style(layout: dict[str, dict], names) -> list[tuple[str, str, str]]:
    """(figure, text, rule) for each FRAME_RETIRED word drawn inside a frame of a main-page figure (names), and for
    each hue a MARK_FIGS figure draws outside story_style.MARK_COL. layout: figure_texts' (its "in_frame" and "hues")."""
    from scripts import story_style as S

    palette = {colour_key(c) for c in S.MARK_COL.values()}
    out = [(name, text, f"{term} inside a frame") for name in names
           for text in layout.get(name, {}).get("in_frame", []) for term, rx in FRAME_RETIRED.items()
           if re.search(rx, text)]  # fmt: skip
    out += [(name, hue, "hue outside the mark system") for name in MARK_FIGS
            for hue in sorted(layout.get(name, {}).get("hues", set()) - palette)]  # fmt: skip
    return out


def colour_key(c) -> str:
    """A colour as '#rrggbb' (alpha dropped), or '' for a grey (r = g = b within 6 of 255), white and black included."""
    from matplotlib.colors import to_hex, to_rgb

    r, g, b = (round(255 * x) for x in to_rgb(c))
    return "" if max(r, g, b) - min(r, g, b) <= 6 else to_hex((r / 255, g / 255, b / 255))


def figure_hues(fig) -> set[str]:
    """The non-grey colours a figure draws: lines and their marks, patches, collections and texts (fully transparent
    ones and 'none' left out)."""
    import numpy as np
    from matplotlib.collections import Collection
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from matplotlib.text import Text

    found = []
    for a in fig.findobj():
        if not a.get_visible():
            continue
        if isinstance(a, Line2D):
            found += [a.get_color(), a.get_markerfacecolor(), a.get_markeredgecolor()]
        elif isinstance(a, Patch):
            found += [a.get_facecolor(), a.get_edgecolor()]
        elif isinstance(a, Collection):
            found += [tuple(c) for c in np.atleast_2d(a.get_facecolors())] + [
                tuple(c) for c in np.atleast_2d(a.get_edgecolors())]  # fmt: skip
        elif isinstance(a, Text) and a.get_text().strip():
            found.append(a.get_color())
    keep = set()
    for c in found:
        if c is None or (isinstance(c, str) and c.lower() == "none"):
            continue
        if not isinstance(c, str) and len(c) == 4 and c[3] == 0:
            continue
        keep.add(colour_key(c))
    return keep - {""}


def retired(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, term) for each text holding a retired term."""
    return [(where, text, term) for where, text in texts for term, rx in RETIRED.items() if re.search(rx, text)]


def joint_retired(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, term) for each text holding a term the joint story retires."""
    return [(where, text, term) for where, text in texts for term, rx in JOINT_RETIRED.items() if re.search(rx, text)]


def root_readme_texts() -> list[tuple[str, str]]:
    """The root README's lines as a reader sees them: HTML comments (the source keys), code spans and link targets
    left out, link texts and alt texts kept."""
    if not ROOT_README.exists():
        return []
    text = re.sub(r"<!--.*?-->", "", ROOT_README.read_text(), flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"(\]\()[^)]*\)", r"\1)", text)  # [text](target) -> [text]()
    return [(f"{ROOT_README.name} l.{i}", line.strip()) for i, line in enumerate(text.splitlines(), 1) if line.strip()]


def joint_figure_texts() -> list[tuple[str, str]]:
    """Every text the joint figures draw, by figure (drawn, not saved): the five README figures and the two grids."""
    import matplotlib
    from matplotlib.text import Text

    from scripts import joint_figures as J
    from scripts import shared_grid as G
    from scripts import story_style as S

    texts: list[tuple[str, str]] = []
    saved = list(J.ROWS)
    with matplotlib.rc_context():
        plt = S.setup()
        try:
            rows = G.build()
            figs = [(name, lambda p, d=draw: d(p)) for name, draw in J.FIGURES]
            figs += [(name, lambda p, n=name: G.draw(p, rows, n)) for name in G.FIGURES]
            for name, draw in figs:
                fig = draw(plt)
                texts += [(name, t.get_text()) for t in fig.findobj(Text) if t.get_text().strip()]
                plt.close(fig)
        finally:
            J.ROWS[:] = saved
    return texts


def caption_texts() -> list[tuple[str, str]]:
    """The figure alt texts and '*Fig. N.*' lines of the README and its template (HTML comments left out), and the
    canonical lines of the captions draft."""
    out = []
    for path in CAPTION_FILES:
        if not path.exists():
            continue
        text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
        out += [(f"{path.name}: alt text", a) for a in re.findall(r"!\[([^\]]*)\]\((?:\.\./)*figures/", text)]
        out += [(f"{path.name}: caption", line) for line in text.splitlines() if re.match(r"\*Fig\. \w+\.\*", line)]
    if CAPTIONS_DRAFT.exists():
        out += [(CAPTIONS_DRAFT.name, line.split(": ", 1)[1]) for line in CAPTIONS_DRAFT.read_text().splitlines()
                if line.startswith("- canonical ") and ": " in line]  # fmt: skip
    return out


def figure_texts(layout: dict[str, dict] | None = None) -> list[tuple[str, str]]:
    """Every text the README and supplementary figures draw, by figure (savefig caught; data.csv and scorecard.csv go
    to a temporary folder). layout, if given, gets each figure's title, subtitle (story_style.title marks it) and number
    of panels (axes)."""
    import matplotlib
    from matplotlib.figure import Figure
    from matplotlib.text import Text

    from scripts import readme_story_figures as F
    from scripts import story_style as S

    texts: list[tuple[str, str]] = []

    def grab(fig, fname, *args, **kwargs) -> None:
        stem = Path(str(fname)).stem
        drawn = [t for t in fig.findobj(Text) if t.get_text().strip()]
        texts.extend((stem, t.get_text()) for t in drawn)
        if layout is not None:
            sub = next((t.get_text() for t in drawn if getattr(t, S.SUBTITLE, False)), "")
            panels = [ax for ax in fig.axes if not getattr(ax, S.INSET, False)]  # a marked inset is not a panel
            in_frame = [t.get_text() for ax in fig.axes for t in ax.texts if t.get_text().strip()]
            layout[stem] = {"title": fig.get_suptitle(), "subtitle": sub, "panels": len(panels), "in_frame": in_frame,
                            "hues": figure_hues(fig) if stem in MARK_FIGS else set()}  # fmt: skip

    saved = (Figure.savefig, S.OUT, S.SUPP, list(S.ROWS))
    with tempfile.TemporaryDirectory() as tmp, matplotlib.rc_context():
        try:
            Figure.savefig = grab  # type: ignore[method-assign]
            S.OUT, S.SUPP = Path(tmp), Path(tmp) / "supp"
            S.ROWS.clear()
            p = S.setup()
            for f in (*F.README_FIGS, *F.SUPP_FIGS):
                f(p)
        finally:
            Figure.savefig, S.OUT, S.SUPP = saved[:3]  # type: ignore[method-assign]
            S.ROWS[:] = saved[3]
    return texts


def main(argv: list[str] | None = None) -> int:
    joint = joint_figure_texts()
    layout: dict[str, dict] = {}
    drawn = figure_texts(layout)
    hits = retired(caption_texts() + drawn + joint)
    joint_hits = joint_retired(joint + root_readme_texts())
    from scripts import readme_story_figures as F

    v6_hits = v6_style(layout, drawn) + frame_style(layout, F.README_NAMES)
    id_hits = readme_ids(readme_body_lines(README_PAGE.read_text())) if README_PAGE.exists() else []
    for where, text, term in hits + joint_hits + v6_hits + id_hits:
        print(f"{where}: {term!r} in {text!r}")

    pending = sorted(
        n for n in F.README_NAMES if n not in V6_FIGS and re.search(r"\d", layout.get(n, {}).get("title", ""))
    )
    if pending:  # reported, not failed: these titles wait for their v6 restyle
        print(f"check_figure_terms: README titles with a digit, not yet in V6_FIGS: {', '.join(pending)}")
    print(f"check_figure_terms: {len(hits)} retired term(s); {len(joint_hits)} joint-story term(s) "
          f"(root README and figures/shared/); {len(v6_hits)} v6 style break(s) ({', '.join(V6_FIGS)}); "
          f"{len(id_hits)} internal id(s) in the depth README's body")  # fmt: skip
    return 1 if hits or joint_hits or v6_hits or id_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
