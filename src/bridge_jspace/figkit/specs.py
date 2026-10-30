"""The setup figure p0b (the root README's three tools) as a spec, and the helpers the table figures share (ctrl,
conflict); p0a is a table figure (figkit/depth_figs.py datasets). The deck's claim figures p1-p9 were retired on 30 Oct (Dan: labels collided): the table style replaces
them (figkit/tables.py: r1-r5, f2-f12, for the README and the slides). SPECS maps id -> function."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit.spec import Figure, Image


def ctrl(m: str) -> float | None:
    """Zach's largest same-size control in M - K: max of rotated, logit lens, PCA (or the size-matched ratio x mk)."""
    pc, pcr, mk = D.b(f"ko.{m}.pc"), D.b(f"ko.{m}.pcr"), D.b(f"ko.{m}.mk")
    vals = [v[0] for v in (D.b(f"ko.{m}.rot"), D.b(f"ko.{m}.u")) if v]
    vals.append(pc[0] if pc else (pcr[0] * mk[0] if pcr and mk else None))
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def conflict(m: str, reader: str):
    key = {"recall": "rc", "lookup": "lk"}[reader]
    return D.x(f"{key}_excess_{D.SHORT.get(m, '-')}") or D.s(
        m, f"conflict: {reader}, switches lost beyond a random part"
    )


# ---- slides 2, 3 ----------------------------------------------------------------------------------------------------
def setup_tools() -> Figure:
    return Figure("p0b_tools", "Three tools, one target: the lens part at the bridge.",
                  "figures/shared/j0_setup.png, its bottom half (a diagram, not re-drawn).",
                  [Image("figures/shared/j0_setup.png", (0.5, 1))])  # fmt: skip


SPECS = {f().id: f for f in (setup_tools,)}
