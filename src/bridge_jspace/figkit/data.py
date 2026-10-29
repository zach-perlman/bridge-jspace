"""The sources every figure reads, and the model order and names. Nothing on a figure is typed: a spec asks this
module for a cell (value, lo, hi) by its source row."""

from __future__ import annotations

import csv
import json
import re
from functools import cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DAN = [("qwen3.5-9b", "Qwen 9B"), ("qwen3.6-27b", "Qwen 27B"), ("muse-glimmer-30b", "Muse 30B"),
       ("nemotron-3.5-lightning", "Lightning ○"), ("qwen3.5-122b-a10b", "Qwen 122B")]  # fmt: skip
ZACH = [("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning"), ("ds", "DeepSeek"), ("mi", "Ministral"),
        ("nb", "Bolt"), ("ol", "OLMo"), ("mu", "Muse 30B"), ("q122", "Qwen 122B")]  # fmt: skip
NAMES = {n for _, n in DAN} | {n for _, n in ZACH}
SHORT = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}


def hollow(model: str, lowered_test: bool = False) -> bool:
    """After the data: Lightning everywhere; the 122B where its gate was lowered (routes, address, swap)."""
    return model == "nemotron-3.5-lightning" or (lowered_test and model == "qwen3.5-122b-a10b")


def _f(x):
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


@cache
def story() -> dict:
    out = {}
    with (REPO / "figures/story/data.csv").open() as f:
        for r in csv.DictReader(f):
            v = _f(r["value"])
            if v is not None:
                out[(r["figure"], r["model"], r["quantity"])] = (v, _f(r["lo"]), _f(r["hi"]))
    return out


@cache
def breadth() -> dict:
    with (REPO / "docs/breadth/data.csv").open() as f:
        return {
            r["key"]: (_f(r["value"]), _f(r["lo"]), _f(r["hi"]))
            for r in csv.DictReader(f)
            if _f(r["value"]) is not None
        }


@cache
def x0() -> dict:
    out = {}
    for k, d in json.loads((REPO / "docs/x0_numbers.json").read_text()).items():
        nums = [
            float(x.replace("−", "-"))
            for x in re.findall(r"[−-]?\d+\.\d+", str(d.get("text", "") if isinstance(d, dict) else d))
        ]
        if nums:
            out[k] = (nums[0], nums[1] if len(nums) > 2 else None, nums[2] if len(nums) > 2 else None)
    return out


def s(model: str, quantity: str, figure: str | None = None, prefix: bool = False):
    """A figures/story/data.csv cell by model and quantity (exact, or the first quantity starting with it)."""
    for (fig, m, q), v in story().items():
        if m == model and (figure is None or fig == figure) and (q.startswith(quantity) if prefix else q == quantity):
            return v
    return None


def s_match(model: str, pattern: str, figure: str | None = None):
    """(quantity, cell) of the first story row whose quantity matches the regex."""
    for (fig, m, q), v in story().items():
        if m == model and (figure is None or fig == figure) and re.match(pattern, q):
            return q, v
    return None


def b(key: str):
    return breadth().get(key)


def x(key: str):
    return x0().get(key)


def scaled(cell, factor: float):
    """A cell times a stored ratio (no interval)."""
    return (cell[0] * factor, None, None)
