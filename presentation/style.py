"""The deck's figure style (presentation brief, 30 Oct ~00:40, Section 1): canvas, colours, model order and names,
font sizes, hollow marks, and the readers of the CSV / JSON sources. Every figure in presentation/ uses this module."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "presentation"
FULL, HALF, THIRD = (12.3, 5.3), (6.0, 5.3), (4.0, 5.3)
DPI = 200
AXIS, TICK, SERIES, VALUE, SMALL = 14, 12, 13, 12, 11  # pt; nothing under SMALL
COL = {"recall": "#2B2B2B", "lookup": "#6B5BD2", "lens": "#1A9E8A", "address": "#E08A1E", "identity": "#3A7DC9",
       "random": "#9E9E9E", "light": "#D9D9D9", "band": "#9E9E9E"}  # fmt: skip
BAND_ALPHA = 0.5 * 0.5  # the brief's 50% alpha, on a light grey fill
# Dan's five, in order: (data key, the deck's name)
DAN = (("qwen3.5-9b", "Qwen 9B"), ("qwen3.6-27b", "Qwen 27B"), ("muse-glimmer-30b", "Muse 30B"),
       ("nemotron-3.5-lightning", "Lightning ○"), ("qwen3.5-122b-a10b", "Qwen 122B"))  # fmt: skip
# Zach's nine, in order: (breadth key, the deck's name)
ZACH = (("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning"), ("ds", "DeepSeek"), ("mi", "Ministral"),
        ("nb", "Bolt"), ("ol", "OLMo"), ("mu", "Muse 30B"), ("q122", "Qwen 122B"))  # fmt: skip
NAMES = {n for _, n in DAN} | {n for _, n in ZACH} | {"Muse 30B ○", "Qwen 122B ○"}
LOWERED = {"qwen3.5-122b-a10b"}  # the 122B's routes / address / swap gates lowered after the data


def hollow(model: str, lowered_test: bool = False) -> bool:
    """Hollow mark: Lightning everywhere; the 122B on the routes / address / swap cells."""
    return model == "nemotron-3.5-lightning" or (lowered_test and model in LOWERED)


def setup() -> None:
    plt.rcParams.update({"font.size": TICK, "axes.labelsize": AXIS, "xtick.labelsize": TICK, "ytick.labelsize": TICK,
                         "legend.fontsize": SERIES, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none"})  # fmt: skip


def figure(size=FULL, ncols: int = 1, **kw):
    return plt.subplots(1, ncols, figsize=size, dpi=DPI, constrained_layout=True, **kw)


# ---- sources -----------------------------------------------------------------------------------------------------
Cell = tuple[float, float | None, float | None, str]


def _f(x: str | None) -> float | None:
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def story() -> dict[tuple[str, str, str], Cell]:
    out = {}
    with (REPO / "figures/story/data.csv").open() as f:
        for r in csv.DictReader(f):
            v = _f(r["value"])
            if v is not None:
                out[(r["figure"], r["model"], r["quantity"])] = (v, _f(r["lo"]), _f(r["hi"]), r["n"])
    return out


def breadth() -> dict[str, Cell]:
    out = {}
    with (REPO / "docs/breadth/data.csv").open() as f:
        for r in csv.DictReader(f):
            v = _f(r["value"])
            if v is not None:
                out[r["key"]] = (v, _f(r["lo"]), _f(r["hi"]), r["n"])
    return out


def x0() -> dict[str, Cell]:
    """docs/x0_numbers.json: 'v [lo, hi]' texts parsed."""
    out = {}
    for k, d in json.loads((REPO / "docs/x0_numbers.json").read_text()).items():
        nums = re.findall(r"[−-]?\d+\.\d+", str(d.get("text", "")) if isinstance(d, dict) else str(d))
        vals = [float(x.replace("−", "-")) for x in nums]
        if vals:
            out[k] = (vals[0], vals[1] if len(vals) > 2 else None, vals[2] if len(vals) > 2 else None, "")
    return out


def find(S: dict, model: str, quantity: str, figure: str | None = None) -> Cell | None:
    """A story row by model and quantity (any figure unless given)."""
    if figure:
        return S.get((figure, model, quantity))
    return next((v for k, v in S.items() if k[1] == model and k[2] == quantity), None)
