"""The helpers the table figures share (ctrl, conflict). The old spec figures (p0b was the last) are retired: every
figure is built by figkit/tables.py (depth_figs.py: p0a datasets, p0b tools)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D


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


SPECS: dict = {}  # every figure is a table figure now (figkit/tables.py); the old spec figures are retired
