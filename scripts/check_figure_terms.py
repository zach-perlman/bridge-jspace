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
    "fig01_split",
    "fig01c_zeroing",
    "fig05b_identity_outside",
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
    "fig15_mechanisms",
)
# E6's probe, remove / add, swap; E8's read-through, share rebuilt, report (Dan's v6 iteration 2: at most three)
V6_PANELS = {"fig07_writes": 3, "fig07b_verbal": 3,
             # kept on the page as they were, smaller (Dan's v6 iteration 2): their panels stay
             "fig05c_described_bridge": 3, "fig09_transfer": 8}  # fmt: skip
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
              "C0 / C2": r"\bC[02]\b"}  # fmt: skip
V6_SUBTITLE_RETIRED = {"rule:": r"(?i)\brule:"}  # the subtitle says the mechanics; the rule belongs to the caption


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
            layout[stem] = {"title": fig.get_suptitle(), "subtitle": sub, "panels": len(panels)}

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
    v6_hits = v6_style(layout, drawn)
    for where, text, term in hits + joint_hits + v6_hits:
        print(f"{where}: {term!r} in {text!r}")
    from scripts import readme_story_figures as F

    pending = sorted(
        n for n in F.README_NAMES if n not in V6_FIGS and re.search(r"\d", layout.get(n, {}).get("title", ""))
    )
    if pending:  # reported, not failed: these titles wait for their v6 restyle
        print(f"check_figure_terms: README titles with a digit, not yet in V6_FIGS: {', '.join(pending)}")
    print(f"check_figure_terms: {len(hits)} retired term(s); {len(joint_hits)} joint-story term(s) "
          f"(root README and figures/shared/); {len(v6_hits)} v6 style break(s) ({', '.join(V6_FIGS)})")  # fmt: skip
    return 1 if hits or joint_hits or v6_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
