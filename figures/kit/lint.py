"""The figure grammar's lint (brief, Fri 30 Oct ~00:50): run on a matplotlib figure before it is saved. Fails on marker
shapes other than "o", hatch, banned strings inside axes, text under 11 pt, a legend outside its axes, a model name
outside the fixed set, red or green hex colours, figures taller than wide, and any figure or axes title."""

from __future__ import annotations

import re

from matplotlib.colors import to_hex
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BANNED = ("not run", "not tested", "cannot report", "too few", "gate", "fixed in advance", "after the data",
          "descriptive", "n =")  # fmt: skip
MODELISH = re.compile(r"Qwen|Muse|Lightning|Nemotron|Bolt|OLMo|DeepSeek|Ministral|Gemma")


def _redgreen(c) -> bool:
    try:
        h = to_hex(c)
    except ValueError:
        return False
    r, g, b = (int(h[i : i + 2], 16) for i in (1, 3, 5))
    return (r > 150 and g < 90 and b < 90) or (g > 120 and r < 90 and b < 110 and g - max(r, b) > 50)


def problems(fig, name: str, names: set[str], titles_ok: bool = False) -> list[str]:
    out = []
    w, h = fig.get_size_inches()
    if h > w:
        out.append(f"{name}: taller than wide")
    if not titles_ok and fig._suptitle is not None and fig._suptitle.get_text():
        out.append(f"{name}: suptitle")
    for ax in fig.axes:
        if not titles_ok and any(ax.get_title(loc=loc) for loc in ("left", "center", "right")):
            out.append(f"{name}: axes title")
        leg = ax.get_legend()
        if leg is not None and leg.get_bbox_to_anchor().bounds != ax.bbox.bounds:
            out.append(f"{name}: legend outside its axes")
        for lab in [*ax.get_xticklabels(), *ax.get_yticklabels()]:
            t = lab.get_text()
            if t and MODELISH.search(t) and t not in names:
                out.append(f"{name}: model name {t!r} not in the set")
        for art in ax.get_children():
            if isinstance(art, Line2D) and art.get_marker() not in ("None", None, "", "o", " "):
                out.append(f"{name}: marker {art.get_marker()!r}")
            if isinstance(art, Patch) and art.get_hatch():
                out.append(f"{name}: hatch")
            for getter in ("get_color", "get_facecolor", "get_edgecolor"):
                c = getattr(art, getter, None)
                if c is not None:
                    try:
                        col = c()
                    except Exception:
                        continue
                    flat = isinstance(col, str) or (
                        hasattr(col, "__len__") and len(col) in (3, 4) and not hasattr(col[0], "__len__")
                    )
                    if flat and _redgreen(col):
                        out.append(f"{name}: red/green colour {to_hex(col)}")
        for t in ax.texts:
            if any(b in t.get_text().lower() for b in BANNED):
                out.append(f"{name}: banned text inside axes {t.get_text()[:30]!r}")
    for t in fig.findobj(match=lambda a: hasattr(a, "get_fontsize") and hasattr(a, "get_text")):
        if t.get_text() and t.get_visible() and t.get_fontsize() < 11 - 1e-6:
            out.append(f"{name}: text under 11 pt {t.get_text()[:30]!r}")
    return sorted(set(out))
