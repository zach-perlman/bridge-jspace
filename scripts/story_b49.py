"""README figure for batch 49, test 49.1: the gain map, drawn from the test's verdict folder (the json its `verdict`
stage writes) in story_style's look, every plotted number recorded for data/figures/depth/data.csv.

  49.1  x49_gain.py   x49_1-<UTC>/x49_1.json   Fig. 27: the gain map, two readers, two weights

The title is the claim, built from the verdict's labels so it reads true for any outcome (pass `title` once Dan has
worded it). Tested on planted verdicts (tests/test_story_b49.py).
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_style as S
from scripts import x49_gain as G
from scripts.story_b47a import NOTE, by_target, fig_id, majority

TARGETS = tuple((t, m) for t, m, _ in S.MODELS if m != "122b")  # 9B, 27B, Muse
WRAP = 104  # subtitle characters per line at 11 pt in the 8.8 in column
HEAT_IN, STRIP_IN, LABELS_IN, GAP_IN, LEFT_IN = 2.3, 0.42, 1.08, 0.22, 0.78  # widths (inches)
TITLE_IN, XLABEL_IN, ROW_GAP_IN = 0.32, 0.62, 0.22  # per model row (inches)
WHOLE_EDGE = S.COL["position"]  # the box around the whole change
STRIP = ((G.gname("R", 0, 1), "rand (0, 1)"), (G.gname("R", 1, 0), "rand (1, 0)"), (G.gname("R", 2, 0), "rand (2, 0)"),
         (G.gname("R", 0, 2), "rand (0, 2)"), (G.NOU, "no pointer"), (G.NOU_RAND, "rand pointer"))  # fmt: skip
TITLES = {"a": "The readers weigh the same two parts: weights, not routes",
          "b": "Two routes: the recall needs the J++ part; the rest cannot stand in",
          "a_prime": "The rest moves the recall only through the address",
          "c": "The gain map: neither weights nor routes"}  # fmt: skip
SHORT = {"a": "weights, not routes", "b": "routes", "a_prime": "only through the address", "c": "neither"}
SUB = ("Main test, scenes with the locker before the pick. At the bridge word at L the change is added to the original prompt as α × its "
       "J++ part + β × the rest; answers switched to the changed prompt's (%), per reader. Boxed: the whole change "
       "(1, 1). Strips: a random part of the J++ part's share in its place (rand), and (0, 2) with the pointer taken out "
       "of the rest (no pointer), beside a random part of the pointer's share (rand pointer). Fixed in advance.")  # fmt: skip


def outcome(m: dict) -> str:
    """A tested model's reading as one key: a, b, a_prime, c, or several joined by '+'."""
    return "+".join(m["holds"]) or "c"


def gain_title(v: dict) -> str:
    tested = [m for m in v["models"] if m["status"] == "tested"]
    if not tested:
        return "The gain map: no model tested yet"
    keys = [outcome(m) for m in tested]
    top = max(set(keys), key=keys.count)
    if top in TITLES and keys.count(top) == len(keys):
        return TITLES[top]
    if top in TITLES and keys.count(top) >= majority(len(keys)):
        return f"{TITLES[top]}, on {keys.count(top)} of {len(keys)} models"
    return "The gain map: the reading differs by model"


def cmap(colour: str) -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list("gain", ["#ffffff", colour])


def cell_text(ax, x: float, y: float, v: float) -> None:
    ax.text(x, y, f"{100 * v:.0f}", ha="center", va="center", gid="value", color="white" if v > 0.55 else "#222222")


def heat(ax, rate: dict, colour: str) -> None:
    """The 5x5 map: α across, β up, every cell's switch rate (%) written in it, the whole change boxed."""
    n = len(G.GAINS)
    grid = np.array([[rate[G.gname("J", a, b)][0] for a in G.GAINS] for b in G.GAINS])
    ax.imshow(
        grid, origin="lower", cmap=cmap(colour), vmin=0, vmax=1, aspect="auto", extent=(-0.5, n - 0.5, -0.5, n - 0.5)
    )
    for j, b in enumerate(G.GAINS):
        for i, a in enumerate(G.GAINS):
            cell_text(ax, i, j, rate[G.gname("J", a, b)][0])
    w = G.GAINS.index(1.0)
    ax.add_patch(Rectangle((w - 0.5, w - 0.5), 1, 1, fill=False, lw=2.4, edgecolor=WHOLE_EDGE, zorder=3))


def strip(ax, rate: dict, colour: str) -> None:
    """The random corners and the no-U arm with its twin, one cell each, labelled on the right."""
    vals = np.array([[rate[a][0]] for a, _ in STRIP])
    ax.imshow(
        vals,
        origin="upper",
        cmap=cmap(colour),
        vmin=0,
        vmax=1,
        aspect="auto",
        extent=(-0.5, 0.5, -0.5, len(STRIP) - 0.5),
    )
    for k, (a, _) in enumerate(STRIP):
        cell_text(ax, 0, len(STRIP) - 1 - k, rate[a][0])
    ax.set_xticks([])
    ax.yaxis.tick_right()
    ax.set_yticks(range(len(STRIP)), [lab for _, lab in STRIP][::-1])
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)


def axes_at(fig, x_in: float, y_in: float, w_in: float, h_in: float):
    """An axes placed in inches from the figure's bottom-left corner."""
    fw, fh = fig.get_size_inches()
    return fig.add_axes((x_in / fw, y_in / fh, w_in / fw, h_in / fh))


def build_gain(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """49.1 (x49_gain verdict, x49_1.json): one row per model (9B, 27B, Muse); per reader (recall, lookup) the 5x5
    gain map of switch rates with the whole change boxed, and beside it the strip of random corners and the no-U arm
    with its random twin; the reading under the row's title."""
    src = verdict_dir / "x49_1.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    keep = (NOTE + SUB).replace("J++ ", "J++ ")
    lines = [x.replace(" ", " ") for x in textwrap.wrap(keep, WRAP, break_on_hyphens=False)]
    top_in = 0.42 + 0.20 * len(lines) + 0.30
    row_in = TITLE_IN + HEAT_IN + XLABEL_IN + ROW_GAP_IN
    h = top_in + row_in * len(TARGETS)
    plt = S.setup()
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, title or gain_title(v), "\n".join(lines), limit=86)
    for r, (target, m) in enumerate(TARGETS):
        mod = by.get(target, {"status": "pending", "label": "pending"})
        y0 = h - top_in - (r + 1) * row_in + XLABEL_IN + ROW_GAP_IN
        reading = SHORT.get(outcome(mod), mod["label"]) if mod["status"] == "tested" else mod["status"]
        S.record(fid, target, "49.1: the rule's reading", mod["label"], source=source)
        x = LEFT_IN
        for w, colour in (("recall", S.COL["recall"]), ("lookup", S.COL["lookup"])):
            hx = axes_at(fig, x, y0, HEAT_IN, HEAT_IN)
            sx_at = x + HEAT_IN + 0.08
            x += HEAT_IN + 0.08 + STRIP_IN + LABELS_IN + GAP_IN
            n = mod.get("n")
            head = f"{F.name_of(m)}: recall" + (f" (n = {n})" if n else "") if w == "recall" else f"lookup; {reading}"
            hx.set_title(head, fontsize=S.FONT, weight="bold", loc="left")
            if mod["status"] != "tested":
                S.empty(hx, "pending" if mod["status"] == "pending" else "not tested (gate)")
                hx.set_xticks([])
                hx.set_yticks([])
                continue
            rate = mod["readers"][w]["rate"]
            heat(hx, rate, colour)
            strip(axes_at(fig, sx_at, y0, STRIP_IN, HEAT_IN), rate, colour)
            ticks = [f"{g:g}" for g in G.GAINS]
            hx.set_xticks(range(len(G.GAINS)), ticks)
            hx.set_xlabel("α: the J++ part's gain")
            if w == "recall":
                hx.set_yticks(range(len(G.GAINS)), ticks)
                hx.set_ylabel("β: the rest's gain")
            else:
                hx.set_yticks(range(len(G.GAINS)), [""] * len(G.GAINS))
            for a in [G.gname("J", al, be) for al in G.GAINS for be in G.GAINS] + [a for a, _ in STRIP]:
                S.record(fid, target, f"49.1: {w}'s switch rate, {a}", *rate[a], n=n, source=source)
    S.save(fig, out_name)
    return out_name


TESTS = {"49.1": ("scripts/x49_gain.py", build_gain, "fig27_gain_map")}
