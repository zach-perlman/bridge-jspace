"""The helpers the table figures share (ctrl, conflict). The old spec figures (p0b was the last) are retired: every
figure is built by figkit/tables.py (depth_figs.py: p0a datasets, p0b tools)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D


def largest(m: str) -> tuple[str, float] | None:
    """Zach's largest same-size control in M - K, as (key, value): the max of rotated (rot), logit lens (u) and PCA (pc,
    or the size-matched ratio x mk)."""
    pc, pcr, mk = D.b(f"ko.{m}.pc"), D.b(f"ko.{m}.pcr"), D.b(f"ko.{m}.mk")
    vals = {k: v[0] for k, v in (("rot", D.b(f"ko.{m}.rot")), ("u", D.b(f"ko.{m}.u"))) if v}
    if pc:
        vals["pc"] = pc[0]
    elif pcr and mk:
        vals["pc"] = pcr[0] * mk[0]
    return max(vals.items(), key=lambda kv: kv[1]) if vals else None


def ctrl(m: str) -> float | None:
    """The value of the largest same-size control in M - K (see largest)."""
    top = largest(m)
    return top[1] if top else None


def conflict(m: str, reader: str):
    key = {"recall": "rc", "lookup": "lk"}[reader]
    return D.x(f"{key}_excess_{D.SHORT.get(m, '-')}") or D.s(
        m, f"conflict: {reader}, switches lost beyond a random part"
    )


SPECS: dict = {}  # every figure is a table figure now (figkit/tables.py); the old spec figures are retired
