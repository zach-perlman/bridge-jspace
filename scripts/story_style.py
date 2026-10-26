"""The README v2 figures' shared style (Dan, 25 Oct): sized for GitHub's ~880 px column (8.8 in wide, text >= 13 px at
that width), the claim as the only title, fixed colours, extra loss as a dot with a 95% CI whisker on a shared
[-0.2, 1.0] axis, models in the order 9B, 27B, 122B; filled = fixed in advance, hollow = after the data, hollow with a
dashed whisker = a rerun with a lowered gate; every plotted number recorded for figures/story/data.csv."""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "figures" / "story"
NUMBERS = REPO / "docs" / "x0_numbers.json"
WIDTH = 8.8  # inches: 880 px at 100 px per inch, GitHub's README column
COL = {"lookup": "#6a4bd6", "recall": "#3a3a3a", "identity": "#2b7bba", "position": "#e08a1e", "original": "#c8c8c8",
       "value": "#2e9e5b", "other": "#ececec", "control": "#bdbdbd", "band": "#f0f0f0", "muted": "#777777"}  # fmt: skip
MODELS = (("qwen3.5-9b", "9b", "Qwen3.5-9B"), ("qwen3.6-27b", "27b", "Qwen3.6-27B"),
          ("qwen3.5-122b-a10b", "122b", "Qwen3.5-122B"), ("muse-glimmer-30b", "muse", "Muse Glimmer 30B"))  # fmt: skip
XLIM = (-0.2, 1.0)
NOT_NEEDED = 0.10  # the rule's "not needed" band (X0: extra loss <= 0.10)
ROWS: list[dict] = []


def setup():
    plt.rcParams.update({"font.size": 10.5, "axes.titlesize": 11, "axes.labelsize": 10.5, "xtick.labelsize": 10,
                         "ytick.labelsize": 10.5, "axes.spines.top": False, "axes.spines.right": False,
                         "font.family": "DejaVu Sans", "svg.fonttype": "none", "axes.edgecolor": "#555555"})  # fmt: skip
    return plt


def title(fig, text: str, limit: int = 70) -> None:
    assert len(text) <= limit, f"title over {limit} characters: {text!r}"
    # a title past 70 characters shrinks to fit the 880 px column (86 characters: 10.6 pt, about 15 px)
    fig.suptitle(text, x=0.01, ha="left", fontsize=13 * min(1.0, 70 / len(text)), weight="bold")


def numbers() -> dict[str, str]:
    return {k: v["text"] for k, v in json.loads(NUMBERS.read_text()).items()}


def parse(text: str | None) -> tuple[float, float, float] | None:
    """'0.53 [0.42, 0.61]' (with typographic minus signs) -> (0.53, 0.42, 0.61); None if absent."""
    if not text:
        return None
    v = [float(x.replace("−", "-")) for x in re.findall(r"[−-]?\d+\.\d+", text)]
    return (v[0], v[1], v[2]) if len(v) >= 3 else None


def record(fig: str, model: str, quantity: str, v, lo=None, hi=None, n=None, source: str = "") -> None:
    ROWS.append({"figure": fig, "model": model, "quantity": quantity, "value": v, "lo": lo, "hi": hi, "n": n,
                 "source": source})  # fmt: skip


def dot(ax, x: float, y: float, v: tuple[float, float, float], color: str, kind: str = "fixed", size: float = 7.5):
    """An extra-loss dot with its 95% CI whisker; kind: fixed (filled), after (hollow), rerun (hollow, dashed)."""
    ls = "--" if kind == "rerun" else "-"
    ax.plot([v[1], v[2]], [y, y], color=color, lw=1.6, ls=ls, zorder=2, solid_capstyle="butt")
    face = color if kind == "fixed" else "white"
    ax.plot([v[0]], [y], "o", ms=size, mfc=face, mec=color, mew=1.6, zorder=3)


def extra_axis(ax, label: bool = True) -> None:
    ax.set_xlim(*XLIM)
    ax.axvspan(XLIM[0], NOT_NEEDED, color=COL["band"], lw=0, zorder=0)
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    if label:
        ax.set_xlabel("extra loss")


def empty(ax, text: str) -> None:
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha="center", va="center", fontsize=10, color=COL["muted"])


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=200, facecolor="white")
    plt.close(fig)


def write_data() -> None:
    """figures/story/data.csv: every plotted number, then every number docs/x0_numbers.json holds (the README's)."""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["figure", "model", "quantity", "value", "lo", "hi", "n", "source"])
    w.writeheader()
    w.writerows(ROWS)
    for key, num in json.loads(NUMBERS.read_text()).items():
        w.writerow({"figure": "numbers", "quantity": key, "value": num["text"], "source": num["source"]})
    (OUT / "data.csv").write_text(buf.getvalue())
