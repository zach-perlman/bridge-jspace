"""Retired terms on the README figures and in their captions (Dan, 27 Oct ~01:05: run it before every commit).

Fails (exit 1, one line per hit) when a retired term appears in a text the README figures draw or in a figure caption:
"first-mentioned", "part removed", "ablation", "Q45" (question numbers belong to predictions/, not figures) and run
ids (a snake_case name such as qwen35_9b_x6_routes, or a UTC stamp such as 20261026T224602Z). The figures are
scripts/readme_story_figures.py's README and supplementary figures, rendered from the run files with savefig caught (no
file is written); the captions are the figure alt texts and "*Fig. N.*" lines of README.md and docs/README.template.md
and the canonical lines of docs/drafts/readme_v5_captions.md. docs/glossary.md's word list is checked by
tests/test_readme_build.py; this script checks the retired terms only.

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
CAPTION_FILES = (REPO / "README.md", REPO / "docs" / "README.template.md")
CAPTIONS_DRAFT = REPO / "docs" / "drafts" / "readme_v5_captions.md"


def retired(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, term) for each text holding a retired term."""
    return [(where, text, term) for where, text in texts for term, rx in RETIRED.items() if re.search(rx, text)]


def caption_texts() -> list[tuple[str, str]]:
    """The figure alt texts and '*Fig. N.*' lines of the README and its template (HTML comments left out), and the
    canonical lines of the captions draft."""
    out = []
    for path in CAPTION_FILES:
        if not path.exists():
            continue
        text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
        out += [(f"{path.name}: alt text", a) for a in re.findall(r"!\[([^\]]*)\]\(figures/", text)]
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
    hits = retired(caption_texts() + figure_texts())
    for where, text, term in hits:
        print(f"{where}: {term!r} in {text!r}")
    print(f"check_figure_terms: {len(hits)} retired term(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
