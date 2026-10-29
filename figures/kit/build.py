"""Build figures from their specs for a target.

uv run python -m figures.kit.build                    # every figure, for the slides -> presentation/
uv run python -m figures.kit.build --target readme    # every figure, for the READMEs -> figures/readme/ (bold claim on top)
uv run python -m figures.kit.build p1_c1_split p5a     # some figures (id or id prefix)

Writes <out>/CAPTIONS.md (claim + caption per figure: the speaker notes) and <out>/contact_sheet.png.
"""

from __future__ import annotations

import argparse
import sys

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from figures.kit.data import REPO
from figures.kit.render import render
from figures.kit.specs import SPECS
from figures.kit.theme import THEMES

OUT = {"slide": REPO / "presentation", "readme": REPO / "figures" / "readme"}


def contact_sheet(out, ids) -> None:
    pngs = [out / f"{i}.png" for i in ids if (out / f"{i}.png").exists()]
    rows = (len(pngs) + 1) // 2
    fig, axs = plt.subplots(rows, 2, figsize=(16, 3.6 * rows), squeeze=False)
    for ax in axs.flat:
        ax.set_axis_off()
    for ax, p in zip(axs.flat, pngs, strict=False):
        ax.imshow(mpimg.imread(p))
        ax.text(0, -0.02, p.name, transform=ax.transAxes, fontsize=12, va="top")
    fig.savefig(out / "contact_sheet.png", dpi=80, facecolor="white")
    plt.close(fig)


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
    (out / "CAPTIONS.md").write_text("# Captions (the speaker notes)\n\nBuilt by `uv run python -m figures.kit.build "
                                     f"--target {a.target}` from figures/kit/specs.py.\n"
                                     + "".join(f"\n## {s.id}\n\n**{s.claim}** {s.caption}\n" for s in specs))  # fmt: skip
    contact_sheet(out, list(SPECS))
    if bad:
        print("\n".join(bad), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
