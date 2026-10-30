"""check_style: every figure embedded or linked in a README draws its hues from the one palette
(src/bridge_jspace/palette.py; docs/shared/figure_style.md). Dan, 30 Oct: the same colour for the same concept in all
README.md files.

For each PNG a README shows (`![..](x.png)` or `[..](x.png)`), the saturated pixels (chroma above CHROMA) are matched
to the nearest allowed colour; a figure fails when more than TOLERANCE of its saturated pixels are farther than DIST
from every allowed colour (anti-aliased edges between two palette colours stay inside the tolerance).

uv run python scripts/check_style.py            # the three READMEs, one line per figure, exit 1 on a failure
uv run python scripts/check_style.py --report   # the same, never failing (a breadth figure is Zach's until redrawn)
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import palette as P  # noqa: E402

READMES = {"root": REPO / "README.md", "depth": REPO / "docs" / "depth" / "README.md",
           "breadth": REPO / "docs" / "breadth" / "README.md"}  # fmt: skip
CHROMA, DIST, TOLERANCE = 40, 22, 0.05  # 5%: anti-aliasing between two roles is not a hue of its own
PNG = re.compile(r"\]\(([^)#\s]+\.png)\)")


def figures(readme: Path) -> list[Path]:
    out = []
    for target in dict.fromkeys(PNG.findall(readme.read_text())):
        if target.startswith("http"):
            continue
        if "contact_sheet" in target:  # a downscaled sheet of the figures, not a figure
            continue
        out.append((readme.parent / target).resolve())
    return out


def _rgb(hexes) -> np.ndarray:
    return np.array([[int(h[i : i + 2], 16) for i in (1, 3, 5)] for h in hexes], dtype=float)


def off_palette(png: Path) -> tuple[float, str, int]:
    """(share of the saturated pixels that match no allowed colour, the most common such colour, saturated pixels)."""
    im = np.asarray(Image.open(png).convert("RGB"), dtype=float).reshape(-1, 3)
    sat = im[im.max(1) - im.min(1) > CHROMA]
    if len(sat) == 0:
        return 0.0, "", 0
    allowed = _rgb(sorted(P.ALLOWED))
    # a pixel is on the palette when it lies on the line from an allowed colour to white: anti-aliasing and a lighter
    # tint of a role blend with the page, so they stay inside; a hue that no role blends to does not
    white = np.array([255.0, 255.0, 255.0])
    d = np.full(len(sat), np.inf)
    for a_ in allowed:
        v = white - a_
        t = np.clip(((sat - a_) @ v) / (v @ v), 0, 1)
        d = np.minimum(d, np.sqrt(((sat - (a_ + t[:, None] * v)) ** 2).sum(-1)))
    bad = sat[d > DIST]
    top = ""
    if len(bad):
        q = (bad // 16 * 16 + 8).astype(int)
        (r, g, b), _ = Counter(map(tuple, q)).most_common(1)[0]
        top = f"#{r:02x}{g:02x}{b:02x}"
    return len(bad) / len(sat), top, len(sat)


def main(argv: list[str]) -> int:
    report = "--report" in argv
    failed = 0
    for name, readme in READMES.items():
        if not readme.exists():
            continue
        print(f"== {name}: {readme.relative_to(REPO)}")
        for png in figures(readme):
            if not png.exists():
                print(f"   MISSING {png.relative_to(REPO)}")
                failed += 1
                continue
            share, top, n = off_palette(png)
            bad = share > TOLERANCE
            failed += bad
            print(f"   {'OFF ' if bad else 'ok  '} {png.relative_to(REPO)}  saturated {n}, off-palette {share:.1%}"
                  + (f", e.g. {top}" if bad else ""))  # fmt: skip
    print(f"check_style: {failed} figure(s) off the palette")
    return 0 if report or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
