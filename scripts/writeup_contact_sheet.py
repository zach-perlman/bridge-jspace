"""docs/review/writeup_contact_sheet.png: every write-up figure in the post's order (figures/common/writeup/_meta/order.txt) at
the 720 px reading width, with its caption from the caption store (figures/common/writeup/_meta/captions.toml, src comments
dropped), for checking each caption against its figure by eye before the Google Doc swap (docs/writeup/figure_map.md).

uv run python scripts/writeup_contact_sheet.py
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from bridge_jspace.figkit import captions, layout  # noqa: E402
from scripts.readme_contact_sheet import LINE, PAD, WIDTH  # noqa: E402

OUT = REPO / "docs/review/writeup_contact_sheet.png"


def main() -> None:
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    store = captions.load("common/writeup")
    tiles = []
    for stem in layout.names("common/writeup").values():
        im = Image.open(layout.folder("common/writeup") / f"{stem}.png").convert("RGB")
        im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
        cap = re.sub(r"<!--.*?-->", "", store.get(stem, "")).strip()
        tiles.append((im, [f"figures/common/writeup/{stem}.png", *textwrap.wrap(cap or "(no caption)", 110)]))
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print(f"wrote {OUT.relative_to(REPO)}: {len(tiles)} figures")


if __name__ == "__main__":
    main()
