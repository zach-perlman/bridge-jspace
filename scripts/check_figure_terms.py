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
    "part removed": r"(?i)\bparts? removed\b",
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


def figure_texts() -> list[tuple[str, str]]:
    """Every text the README and supplementary figures draw, by figure (savefig caught; data.csv and scorecard.csv go
    to a temporary folder)."""
    import matplotlib
    from matplotlib.figure import Figure
    from matplotlib.text import Text

    from scripts import readme_story_figures as F
    from scripts import story_style as S

    texts: list[tuple[str, str]] = []

    def grab(fig, fname, *args, **kwargs) -> None:
        texts.extend((Path(str(fname)).stem, t.get_text()) for t in fig.findobj(Text) if t.get_text().strip())

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
    hits = retired(caption_texts() + figure_texts() + joint)
    joint_hits = joint_retired(joint + root_readme_texts())
    for where, text, term in hits + joint_hits:
        print(f"{where}: {term!r} in {text!r}")
    print(f"check_figure_terms: {len(hits)} retired term(s); {len(joint_hits)} joint-story term(s) "
          f"(root README and figures/shared/)")  # fmt: skip
    return 1 if hits or joint_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
