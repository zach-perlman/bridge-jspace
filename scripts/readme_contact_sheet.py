"""docs/review/readme_v2_contact_sheet.png: every figure the root README shows, in its order, at the 720 px reading width,
with the caption the README prints under it (src comments dropped), for checking captions against figures by eye.

uv run python scripts/readme_contact_sheet.py [--docs README.md docs/depth/README.md --out docs/review/docs_pass_contact_sheet.png]
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
OUT = REPO / "docs/review/readme_v2_contact_sheet.png"
WIDTH, PAD, LINE = 720, 12, 17
IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+\.png)\)")


def figures(doc: Path = README) -> list[tuple[str, str, str]]:
    """(repo path, alt text, caption) for each image in a markdown file; the caption is the next italic line, if any."""
    lines = doc.read_text().splitlines()
    out = []
    for i, line in enumerate(lines):
        m = IMG.search(line)
        if not m:
            continue
        cap = next((ln for ln in lines[i + 1 : i + 4] if ln.startswith("*") and not ln.startswith("**")), "")
        cap = re.sub(r"<!--.*?-->", "", cap).strip("* ")
        path = (doc.parent / m.group(2)).resolve().relative_to(REPO)
        out.append((str(path), m.group(1), cap))
    return out


def main(argv: list[str] | None = None) -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docs", nargs="+", default=["README.md"], help="markdown files, in order (default README.md)")
    ap.add_argument("--out", default=str(OUT.relative_to(REPO)), help="the sheet, relative to the repo root")
    a = ap.parse_args(argv)
    out = REPO / a.out
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    tiles = []
    for doc in a.docs:
        for path, alt, cap in figures(REPO / doc):
            im = Image.open(REPO / path).convert("RGB")
            im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
            text = [f"{doc}: {path}", *textwrap.wrap(f"alt: {alt}", 110), *textwrap.wrap(cap or "(no caption)", 110)]
            tiles.append((im, text))
    height = sum(im.height + LINE * len(t) + 3 * PAD for im, t in tiles)
    sheet = Image.new("RGB", (WIDTH, height), "white")
    draw = ImageDraw.Draw(sheet)
    y = 0
    for im, text in tiles:
        sheet.paste(im, (0, y))
        y += im.height + PAD
        for j, s in enumerate(text):
            draw.text((PAD, y + j * LINE), s, fill="#1a1a1a" if j == 0 else "#555555", font=font)
        y += LINE * len(text) + 2 * PAD
        draw.line([(0, y - PAD), (WIDTH, y - PAD)], fill="#dddddd")
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"wrote {out.relative_to(REPO)}: {len(tiles)} figures")


if __name__ == "__main__":
    main()
