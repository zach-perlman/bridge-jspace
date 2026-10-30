"""The figure grammar's lint (brief, Fri 30 Oct ~00:50): run on a matplotlib figure before it is saved. Fails on marker
shapes other than "o", hatch, banned strings inside axes, text under 11 pt, a legend outside its axes, a model name
outside the fixed set, red or green hex colours, figures taller than wide, and any figure or axes title."""

from __future__ import annotations

import re

from matplotlib.colors import to_hex
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

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


def _marks(ax, name: str) -> list[str]:
    """Markers other than "o", hatch, red or green colours among an axes' artists."""
    out = []
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
    return out


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
        out += _marks(ax, name)
        for t in ax.texts:
            if any(b in t.get_text().lower() for b in BANNED):
                out.append(f"{name}: banned text inside axes {t.get_text()[:30]!r}")
    for t in fig.findobj(match=lambda a: hasattr(a, "get_fontsize") and hasattr(a, "get_text")):
        if t.get_text() and t.get_visible() and t.get_fontsize() < 11 - 1e-6:
            out.append(f"{name}: text under 11 pt {t.get_text()[:30]!r}")
    return sorted(set(out))


TABLE_BANNED = ("not run", "not tested", "not designed", "invalid", "under 30", "n =")  # "can't tell" and "below gate" are cell reasons (Dan 30 Oct)
TABLE_NAMES = {"Qwen 9B", "Qwen 27B", "Muse 30B", "Lightning", "Qwen 122B", "DeepSeek", "Ministral", "Bolt", "OLMo"}


def _palette() -> set[str]:
    from bridge_jspace.figkit.dottable import GREYS, INK, MUTED, C

    return {c.lower() for c in (*C.values(), *GREYS, INK, MUTED)} | {"#ffffff", "#000000"}


def _hex(c) -> str | None:
    try:
        return to_hex(c).lower()
    except ValueError:
        return None


def table_problems(fig, name: str, need_xlabel: bool = False) -> list[str]:
    """The table style's lint (morning brief 30 Oct, Section 4; review v3 G1, G2, G4, G6): rotated text, overlapping
    texts, text off the figure, legends, markers other than "o", hatch, red or green, a suptitle, an image taller than
    1.2x its width, banned words, a model name outside the set, a panel with no data; a hollow mark without the key
    item "post hoc" (G1); a mark colour outside the one palette (G2); a data axis without a title when need_xlabel
    (G4); a bar segment that no text names and none carries (G6)."""
    out = []
    w, h = fig.get_size_inches()
    if h > 1.2 * w:
        out.append(f"{name}: taller than 1.2x its width")
    if fig._suptitle is not None and fig._suptitle.get_text():
        out.append(f"{name}: suptitle")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fb = fig.bbox
    texts = [t for t in fig.findobj(match=lambda a: hasattr(a, "get_text") and hasattr(a, "get_rotation"))
             if t.get_text().strip() and t.get_visible()]  # fmt: skip
    boxes = []
    for t in texts:
        s = t.get_text()
        if t.get_rotation() not in (0, 0.0):
            out.append(f"{name}: rotated text {s[:25]!r}")
        if any(b in s.lower() for b in TABLE_BANNED):
            out.append(f"{name}: banned text {s[:25]!r}")
        if MODELISH.search(s) and s.strip() not in TABLE_NAMES and len(s.split()) <= 3:
            out.append(f"{name}: model name {s!r} outside the set")
        bb = t.get_window_extent(r)
        if bb.x0 < fb.x0 - 1 or bb.x1 > fb.x1 + 1 or bb.y0 < fb.y0 - 1 or bb.y1 > fb.y1 + 1:
            out.append(f"{name}: text off the figure {s[:25]!r}")
        boxes.append((s, bb))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if a.x0 < b.x1 - 1 and b.x0 < a.x1 - 1 and a.y0 < b.y1 - 1 and b.y0 < a.y1 - 1:
                out.append(f"{name}: texts overlap {boxes[i][0][:20]!r} / {boxes[j][0][:20]!r}")
    palette = _palette()
    hollow = any(t.get_text().strip() == "○" for t in texts)  # a hollow row label (its key item is the figure's)
    key_words = " ".join(t.get_text() for t in texts)
    text_colours = {_hex(t.get_color()) for t in texts}
    for k, ax in enumerate(fig.axes):
        if ax.get_legend() is not None:
            out.append(f"{name}: legend")
        out += _marks(ax, name)
        for a in ax.get_children():  # G1, G2: hollow marks, mark colours
            if isinstance(a, Line2D) and a.get_marker() == "o":
                mfc, col = _hex(a.get_markerfacecolor()), _hex(a.get_color())
                hollow = hollow or mfc == "#ffffff"
                if col and col not in palette:
                    out.append(f"{name}: mark colour {col} outside the palette")
        for a in ax.patches:  # G2, G6
            if isinstance(a, Rectangle) and a is not ax.patch and a.get_width() > 0:
                fc = _hex(a.get_facecolor())
                if fc and fc not in palette and fc != _hex((0, 0, 0, 0)) and a.get_alpha() in (None, 1.0):
                    out.append(f"{name}: bar colour {fc} outside the palette")
                bb = a.get_window_extent(r)
                carries = any(bb.x0 <= (tb.x0 + tb.x1) / 2 <= bb.x1 and bb.y0 <= (tb.y0 + tb.y1) / 2 <= bb.y1
                              for _s, tb in boxes)  # fmt: skip
                if fc not in ("#ffffff", "#f5f5f5") and fc not in text_colours and not carries and fc != "#e6e6e6":
                    out.append(f"{name}: an unlabelled bar segment {fc}")
        if need_xlabel and not ax.get_xlabel():
            out.append(f"{name}: panel {k + 1} has no x-axis title")
        dots = any(isinstance(a, Line2D) and a.get_marker() == "o" for a in ax.get_children())
        bars = any(isinstance(a, Rectangle) and a is not ax.patch and a.get_width() > 0 for a in ax.patches)
        if not (dots or bars or ax.collections or ax.images):
            out.append(f"{name}: panel {k + 1} has no data")
    if hollow and "post hoc" not in key_words:
        out.append(f"{name}: a hollow mark without the key item 'post hoc'")
    return sorted(set(out))
