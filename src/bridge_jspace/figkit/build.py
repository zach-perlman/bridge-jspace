"""Build figures from their specs for a target.

uv run python -m bridge_jspace.figkit.build                    # every figure, for the slides -> figures/slides/
uv run python -m bridge_jspace.figkit.build --target readme    # every figure, for the READMEs -> figures/readme/ (bold claim on top)
uv run python -m bridge_jspace.figkit.build p1_c1_split p5a     # some figures (id or id prefix)

Writes <out>/CAPTIONS.md (claim + caption per figure: the speaker notes) and <out>/contact_sheet.png.
"""

from __future__ import annotations

import argparse
import sys

from bridge_jspace.figkit.data import REPO
from bridge_jspace.figkit.render import render
from bridge_jspace.figkit.specs import SPECS
from bridge_jspace.figkit.theme import THEMES

OUT = {"slide": REPO / "figures" / "slides", "readme": REPO / "figures" / "readme"}
CAPTIONS = {
    "slide": REPO / "docs" / "slides" / "captions_presentation.md",
    "readme": REPO / "docs" / "slides" / "captions_readme.md",
}


def contact_sheet(out, ids) -> None:
    page_sheet([out / f"{i}.png" for i in ids], out / "contact_sheet.png")


def page_sheet(pngs, dest, width: int = 880) -> None:
    """Every PNG scaled to the page width (880 px, GitHub's README column), stacked with its file name above it:
    open at 100% to see the figures as a reader does."""
    from PIL import Image, ImageDraw

    ims = [(p.name, Image.open(p).convert("RGB")) for p in pngs if p.exists()]
    ims = [(n, im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)) for n, im in ims]
    sheet = Image.new("RGB", (width, sum(im.height + 40 for _, im in ims) or 1), "white")
    y, draw = 0, ImageDraw.Draw(sheet)
    for n, im in ims:
        draw.text((4, y + 12), n, fill="#6B6B6B")
        sheet.paste(im, (0, y + 40))
        y += im.height + 40
    sheet.save(dest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--target", choices=sorted(THEMES), default="slide")
    a = ap.parse_args()
    theme, out = THEMES[a.target], OUT[a.target]
    ids = [i for i in SPECS if not a.ids or any(i.startswith(x) for x in a.ids)]
    bad = []
    for i in ids:
        problems = render(SPECS[i](), theme, out)
        bad += problems
        print(("LINT " if problems else "wrote ") + str(out / f"{i}.png"))
    specs = [SPECS[i]() for i in SPECS]
    CAPTIONS[a.target].write_text("# Captions (the speaker notes)\n\nBuilt by `uv run python -m bridge_jspace.figkit.build "
                                     f"--target {a.target}` from src/bridge_jspace/figkit/specs.py.\n"
                                     + "".join(f"\n## {s.id}\n\n**{s.claim}** {s.caption}\n" for s in specs))  # fmt: skip
    contact_sheet(out, list(SPECS))
    if bad:
        print("\n".join(bad), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
