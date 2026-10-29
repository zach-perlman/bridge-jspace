"""The deck figures' lint (presentation brief, Section 1), run on each figure before it is saved: no suptitle, no
axes title, no text under 11 pt, no legend outside its axes, no 'not run / not tested / cannot report' inside the
frame, and every model-like tick label in the fixed name set."""

from __future__ import annotations

import re

from presentation import style as ST

BANNED = ("not run", "not tested", "cannot report")
MODELISH = re.compile(r"Qwen|Muse|Lightning|Nemotron|Bolt|OLMo|DeepSeek|Ministral|Gemma")


def problems(fig, name: str) -> list[str]:
    out = []
    if fig._suptitle is not None and fig._suptitle.get_text():
        out.append(f"{name}: suptitle")
    for ax in fig.axes:
        for loc in ("left", "center", "right"):
            if ax.get_title(loc=loc):
                out.append(f"{name}: axes title {ax.get_title(loc=loc)!r}")
        leg = ax.get_legend()
        if leg is not None and leg.get_bbox_to_anchor().bounds != ax.bbox.bounds:
            out.append(f"{name}: legend outside its axes")
        for lab in [*ax.get_xticklabels(), *ax.get_yticklabels()]:
            t = lab.get_text()
            if t and MODELISH.search(t) and t not in ST.NAMES:
                out.append(f"{name}: model name {t!r} outside the fixed set")
    for t in fig.findobj(match=lambda a: hasattr(a, "get_fontsize") and hasattr(a, "get_text")):
        text = t.get_text()
        if not text or not t.get_visible():
            continue
        if t.get_fontsize() < ST.SMALL - 1e-6:
            out.append(f"{name}: text under {ST.SMALL} pt: {text[:30]!r} ({t.get_fontsize()})")
        if any(b in text.lower() for b in BANNED):
            out.append(f"{name}: banned text {text[:30]!r}")
    return out
