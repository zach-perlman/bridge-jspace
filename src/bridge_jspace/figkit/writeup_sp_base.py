"""What every styles-plot write-up module shares: the vocabulary (plotstyle.toml), the model ids, and the way a data
cell (value, lo, hi) becomes an estimate."""

from __future__ import annotations

from functools import cache
from pathlib import Path

import styles_plot as sp

from bridge_jspace import figdata as W

REPO = Path(__file__).resolve().parents[3]
ZK = W.ZK  # model key -> short id (the registry's cell suffix)
MODEL = {k: m for m, k in ZK.items()}


@cache
def vocab() -> sp.Vocab:
    return sp.load(REPO / "plotstyle.toml")


def need(c, what: str):
    """A value every figure must have: a missing one stops the build (it is never drawn as a guess)."""
    if c is None:
        raise ValueError(f"no data for {what}")
    return c


def est(c, cell, key=None, label=False, interval=True, note=None) -> sp.Est:
    """A data cell (value, lo, hi) as an estimate; interval=False draws the dot alone."""
    lo, hi = (c[1], c[2]) if interval and len(c) > 2 and c[1] is not None else (None, None)
    return sp.Est(c[0], lo, hi, cell=cell, key=key, label=label, note=note)
