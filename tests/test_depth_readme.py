"""The depth README after the docs pass (P2, 7 Nov): every claim of the matrix shows its figure inside its card, alt
texts are unique, the same PNG has the same caption on every page, and values listed by model keep the figures'
order (9B, 27B, Muse, Lightning, 122B)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts import readme_build as RB

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "docs" / "depth" / "README.md"
PAGES = [REPO / "README.md", PAGE, REPO / "docs" / "breadth" / "README.md"]
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+\.png)\)")
ORDER = ["9B", "27B", "Muse", "Lightning", "122B"]


def body(path: Path) -> str:
    return re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)


def section(text: str, heading: str) -> str:
    """A heading's section: from the heading to the next heading of the same or a higher level."""
    m = re.search(rf"^(#+) {re.escape(heading)}\s*$", text, flags=re.M)
    assert m, heading
    level = len(m.group(1))
    rest = text[m.end() :]
    nxt = re.search(rf"^#{{1,{level}}} ", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def test_every_claim_has_its_figure_inside_its_card():
    text = body(PAGE)
    for n in RB.CLAIM_CELLS:
        heading = RB.CLAIM_CARD[n]
        assert f"(#{RB.slug(heading)})" in text, n  # the matrix links the card
        assert IMAGE.search(section(text, heading)), (n, heading)


def test_alt_texts_are_unique():
    alts = [a for a, _ in IMAGE.findall(body(PAGE))]
    assert len(alts) == len(set(alts)), sorted({a for a in alts if alts.count(a) > 1})


def test_the_same_png_has_the_same_caption_everywhere():
    seen: dict[str, str] = {}
    compared = 0
    for page in PAGES:
        lines = page.read_text().splitlines()
        for i, line in enumerate(lines):
            for _alt, src in IMAGE.findall(line):
                png = Path(src).name if "figures/" not in src else src.split("figures/", 1)[1]
                # the caption is the next non-blank line (the breadth page leaves a blank line after the image)
                nxt = next((ln.strip() for ln in lines[i + 1 :] if ln.strip()), "")
                cap = nxt if nxt.startswith("*") and nxt.endswith("*") else ""
                if cap and png in seen:
                    assert seen[png] == cap, (page.name, png)
                    compared += 1
                seen.setdefault(png, cap) if cap else None
    assert compared, "no PNG is shown with a caption on two pages: the test compares nothing"


QUOTED = re.compile(r"\"[^\"\n]*\"|“[^”\n]*”")  # verbatim rule quotes keep their own order
RUN = re.compile(r"\b(?:9B|27B|Muse|Lightning|122B)(?: / (?:9B|27B|Muse|Lightning|122B))+")


@pytest.mark.parametrize("page", [REPO / "README.md", PAGE, REPO / "docs" / "depth" / "EXPERIMENTS.md"],
                         ids=lambda p: p.name if p != PAGE else "depth README")  # fmt: skip
def test_values_listed_by_model_keep_the_figures_order(page):
    text = QUOTED.sub("", body(page))
    for line in text.splitlines():
        if line.startswith("|") and sum(f" {m} " in line or f"{m} ○" in line for m in ORDER) >= 3:
            cols = [c.strip().removesuffix(" ○") for c in line.strip("|").split("|")]
            names = [c for c in cols if c in ORDER]
            assert names == sorted(names, key=ORDER.index), line[:120]
        for run in RUN.findall(line):
            names = run.split(" / ")
            assert names == sorted(names, key=ORDER.index), run
