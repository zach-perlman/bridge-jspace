"""patch_by_depth (Dan's figure guide 6e): where the last-two-token patch sends the answer, by depth, on every model.

The donor prompt's last two tokens are copied into the original prompt at one layer (pointer_swap; memory → prompt:
family RL, source dissoc, group last). Per swept layer, the share of patched answers that go to the original's sentence
in the same place in the list ("same place": order), to its sentence about the donor's entity ("same entity": the
bridge's identity), and to the donor's own digit ("the copied digit"), with Wilson 95% intervals. The figure's words are
plain (5-second test, 23 Oct): no "memory → prompt" or "identity" on it; this docstring keeps the project's terms. Selection and run as the old f_patch_outcomes_by_depth_all_models
(cross_model_figures.collect_depth / roles_by_layer): each model's finding-5 "draw 1" row in grid.json names the run;
its outcomes.jsonl is counted here (by_layer; tests/test_figs_depth.py checks it equals roles_by_layer).

The band: the label → digit window, readme_figures.stages' patch window: the swept layers where answers move (at most
90% unchanged) while the donor's digit is not there yet (Wilson upper bound < 10%, finding5_confirm's layer bar). Each
swept layer stands for the stretch half-way to its neighbours, so a one-layer window is still visible.

MAIN: four models (MAIN_MODELS: two hybrids, two attention-only), the rest named in the caption; FULL: all models,
hybrids in the top row, attention-only below. Every drawn point is a Number with the run file as its source.

uv run python scripts/figs/patch_by_depth.py [--grid DIR] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from matplotlib.transforms import offset_copy

from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import cross_model_figures as CMF
from scripts import cross_model_grid as G
from scripts import finding5_confirm as FC
from scripts import readme_build as RB
from scripts.figs import common as C

STEM = "patch_by_depth"
MAIN_MODELS = ("27b", "9b", "32b", "gemma")  # two hybrids, two attention-only; the rest in FULL
DIGIT = "#A6611A"  # the donor's digit: a brown apart from LOOKUP's purple and RECALL's grey (4.8:1 on white)
BAND = "#EBE1F5"  # the label → digit window: a pale tint of the order line's purple
# (outcome, direct label, color, marker, line width, marker size); order first = drawn on top. The identity line is
# the heaviest so it shows where it runs under the order line (5-second test, 23 Oct).
OUTCOMES = (
    ("position", "same place\nin the list", C.LOOKUP, "o", 2.4, 6.5),
    ("identity", "same\nentity", C.RECALL, "s", 3.2, 8.0),
    ("value", "the copied\ndigit", DIGIT, "^", 2.2, 6.5),
)
MIN_BAND = 5.0  # % of depth: a narrower window is widened to this, never past the swept layers beside it
BAND_EDGE = "#C9B3E6"  # a thin darker outline, so a one-layer window stays visible under the markers
KEPT_MAX = 0.90  # answers move: at most this share unchanged (readme_figures.stages)
DIGIT_UB = FC.VALUE_UB  # the digit is not there yet: its Wilson upper bound below this
Triple = tuple[float, float, float]


@dataclass
class Depth:
    """One model's patch outcomes by swept layer (shares 0-1 with Wilson 95% intervals)."""

    model: str
    source: str  # the run file, relative to the repo
    n_layers: int
    layers: list[int]
    totals: list[int]
    shares: dict[str, list[Triple]]  # position, identity, value, none
    used: int | None = None  # the layer finding 5's cell uses (the grid's control text)
    faded: str = ""  # a reason when the grid calls the cell not interpretable (drawn pale, FULL only)
    window: list[int] = field(init=False)

    def __post_init__(self) -> None:
        self.window = [la for la, kept, val in zip(self.layers, self.shares["none"], self.shares["value"], strict=True)
                       if kept[0] <= KEPT_MAX and val[2] < DIGIT_UB]  # fmt: skip

    def depth(self, layer: float) -> float:
        return 100 * layer / self.n_layers

    def spans(self) -> list[tuple[float, float]]:
        """The window as depth intervals (%): each run of consecutive swept layers in it, from half-way to the swept
        layer before to half-way to the one after (half a step past an end of the sweep); one narrower than MIN_BAND
        is widened about its middle to MIN_BAND, stopping short of the swept layers beside it."""
        out, ls = [], self.layers
        i = 0
        while i < len(ls):
            if ls[i] not in self.window:
                i += 1
                continue
            j = i
            while j + 1 < len(ls) and ls[j + 1] in self.window:
                j += 1
            step = (ls[1] - ls[0]) if len(ls) > 1 else 1
            lo = self.depth((ls[i - 1] + ls[i]) / 2 if i > 0 else ls[i] - step / 2)
            hi = self.depth(
                (ls[j] + ls[j + 1]) / 2 if j + 1 < len(ls) else ls[j] + (ls[j] - ls[j - 1] if j > 0 else step) / 2
            )
            if hi - lo < MIN_BAND:
                mid = (lo + hi) / 2
                floor = self.depth(ls[i - 1]) + 0.5 if i > 0 else -math.inf
                ceil = self.depth(ls[j + 1]) - 0.5 if j + 1 < len(ls) else math.inf
                lo, hi = min(lo, max(mid - MIN_BAND / 2, floor)), max(hi, min(mid + MIN_BAND / 2, ceil))
            out.append((lo, hi))
            i = j + 1
        return out


# ---------------------------------------------------------------- loading (the files the grid names)


def by_layer(rows: list[dict], level: str | None = None, family: str = "RL") -> dict[int, collections.Counter]:
    """Every role's count per numeric layer, on cross_model_figures.roles_by_layer's rows (source dissoc, group last,
    the family, the level if given)."""
    by: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    for o in rows:
        if o["source"] != "dissoc" or o["group"] != "last" or o["family"] != family:
            continue
        if (level is not None and o["level"] != level) or not str(o["layer"]).lstrip("-").isdigit():
            continue
        by[int(o["layer"])][o["role"]] += 1
    return dict(sorted(by.items()))


def depth_of(model: str, counts: dict[int, collections.Counter], source: str, used: int | None = None,
             faded: str = "") -> Depth:  # fmt: skip
    layers = list(counts)
    totals = [sum(counts[la].values()) for la in layers]
    shares = {r: [CMF.tri(wilson(counts[la][r], t)) for la, t in zip(layers, totals, strict=True)]
              for r in (*(o[0] for o in OUTCOMES), "none")}  # fmt: skip
    return Depth(model, source, CMF.n_layers(model), layers, totals, shares, used, faded)


def load(grid_dir: Path) -> tuple[dict[str, Depth], dict[str, str]]:
    """Per model, its finding-5 'draw 1' run's outcomes by layer; and the models without one, with the reason."""
    grid = CMF.Grid(json.loads((grid_dir / "grid.json").read_text())["rows"])
    opts = {(c.model, c.run): c.opts for c in G._cells() if c.finding == "f5"}
    data: dict[str, Depth] = {}
    missing: dict[str, str] = {}
    for m in C.MODELS:
        row = grid.get(m.key, "f5", "draw 1")
        if row is None:
            missing[m.key] = "not in the grid"
            continue
        w = CMF.word(row["verdict"])
        if not CMF.has_run(row):
            missing[m.key] = CMF.short_reason(w, row["verdict"])
            continue
        path = G.RESULTS / "pointer_swap" / row["run"] / "outcomes.jsonl"
        if not path.exists():
            missing[m.key] = "not pulled"
            continue
        counts = by_layer(G.jl(path), opts.get((m.key, row["run"]), {}).get("level"))
        if not counts:
            missing[m.key] = "no patched rows"
            continue
        used = re.search(r"layer (\d+) \(", row.get("control") or "")
        faded = CMF.short_reason(w, row["verdict"]) if w == "not interpretable" else ""
        data[m.key] = depth_of(m.key, counts, str(path.relative_to(pins.REPO_ROOT)), int(used.group(1)) if used else None,
                               faded)  # fmt: skip
    return data, missing


# ---------------------------------------------------------------- text


def title(data: dict[str, Depth]) -> str:
    """The claim, from every model with data: a window before the digit, and the digit taking over after it."""
    ok = [d for d in data.values() if not d.faded]
    shown = [d for d in ok if arrives_after(d)]
    if ok and len(shown) == len(ok):
        return "Same place or entity first, the copied digit later"
    return f"On {len(shown)} of {len(ok)} models: place or entity first, digit later"


def arrives_after(d: Depth) -> bool:
    """A window, and the digit arrived (point share >= the bar) at a swept layer after it."""
    return bool(d.window) and any(la > d.window[-1] and v[0] >= DIGIT_UB
                                  for la, v in zip(d.layers, d.shares["value"], strict=True))  # fmt: skip


def caption(data: dict[str, Depth], keys: list[str], missing: dict[str, str], b: RB.Book) -> str:
    """Line 1: the shading's rule and where the other models are; line 2: n, the bands, the markers, what is missing."""
    drawn = [data[k] for k in keys]
    ns = [t for d in drawn for t in d.totals]
    line1 = (f"Shaded: ≥ {100 - 100 * KEPT_MAX:.0f}% of answers changed, digit's 95% upper bound "
             f"< {100 * DIGIT_UB:.0f}%.")  # fmt: skip
    others = [C.MODEL[k].short for k in data if k not in keys]
    if others:
        line1 += " FULL: " + ", ".join(others) + "."
    n = f"{min(ns)}" if min(ns) == max(ns) else f"{min(ns)}–{max(ns)}"
    line2 = f"n = {n} per layer; pale bands: 95% CI; filled markers: hybrid, hollow: attention-only."
    if missing:
        line2 += " " + (C.not_tested(b, "f5", list(missing))
                        or "Not drawn: " + ", ".join(f"{C.MODEL[k].short} ({why})" for k, why in missing.items()) + ".")  # fmt: skip
    return line1 + "\n" + line2


SUBTITLE = "Last two tokens copied from a prompt with the list reordered: where does the answer go?"
HOW = "One panel per model. Shaded: the answer already moves, the digit has not arrived."


# ---------------------------------------------------------------- drawing


def panel(ax, d: Depth) -> list[C.Number]:
    """One model's three outcome lines with pale 95% bands over the window band; returns the drawn points."""
    hybrid = C.MODEL[d.model].hybrid
    x = [d.depth(la) for la in d.layers]
    nums: list[C.Number] = []
    for lo, hi in d.spans():
        ax.axvspan(lo, hi, facecolor=BAND, edgecolor=BAND_EDGE, lw=1.0, zorder=0)
        nums += [C.Number(lo, "window start, % of depth", model=d.model, setting="draw 1", source=d.source,
                          extra={"window layers": d.window}),
                 C.Number(hi, "window end, % of depth", model=d.model, setting="draw 1", source=d.source,
                          extra={"window layers": d.window})]  # fmt: skip
    for z, (role, _, color, shape, width, size) in zip((5, 4, 3), OUTCOMES, strict=True):
        col = C.CONTROL if d.faded else color
        ts = d.shares[role]
        ax.fill_between(x, [100 * t[1] for t in ts], [100 * t[2] for t in ts], color=col, alpha=0.16, lw=0, zorder=1)
        ax.plot(x, [100 * t[0] for t in ts], color=col, lw=width, marker=shape, markersize=size,
                markerfacecolor=col if hybrid else "white", markeredgecolor=col, markeredgewidth=1.8, zorder=z,
                gid="mark")  # fmt: skip
        for la, xx, t, n in zip(d.layers, x, ts, d.totals, strict=True):
            nums.append(C.Number(100 * t[0], f"% of patched answers: {role}", model=d.model, setting="draw 1",
                                 ci=(100 * t[1], 100 * t[2]), n=n, source=d.source,
                                 extra={"layer": la, "depth": xx, "outcome": role}))  # fmt: skip
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 104)
    ax.set_xticks([0, 50, 100])
    ax.set_yticks([0, 50, 100])
    ax.tick_params(length=4)
    ax.set_title(C.MODEL[d.model].name, loc="left", fontsize=C.LABEL, fontweight="bold", pad=10)
    if d.faded:
        ax.text(0.03, 0.97, f"not interpretable\n({d.faded})", transform=ax.transAxes, fontsize=C.NOTE,
                color=C.CAPTION_INK, va="top", gid="status")  # fmt: skip
    return nums


def spread(ys: list[float], gap: float, lo: float, hi: float) -> list[float]:
    """ys moved apart to at least `gap` (order kept), inside [lo, hi]."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = [min(max(ys[i], lo), hi) for i in order]
    for k in range(1, len(out)):
        out[k] = max(out[k], out[k - 1] + gap)
    over = out[-1] - hi
    if over > 0:
        out = [y - over for y in out]
    res = [0.0] * len(ys)
    for k, i in enumerate(order):
        res[i] = out[k]
    return res


def direct_labels(ax, d: Depth) -> None:
    """Each line's name in its color, right-aligned just left of the window band (left of the lines' rise), at the
    height of the line's peak, pushed apart to two text lines."""
    spans = d.spans()
    x = [d.depth(la) for la in d.layers]
    rise = []
    for role, *_ in OUTCOMES:
        ys = [t[0] for t in d.shares[role]]
        rise.append(next(xx for xx, y in zip(x, ys, strict=True) if y >= max(ys) / 2))
    right = min(rise + ([spans[0][0]] if spans else [])) - 4
    peaks = [100 * max(t[0] for t in d.shares[role]) for role, *_ in OUTCOMES]
    lo, hi = ax.get_ylim()
    height_in = ax.get_position().height * ax.figure.get_figheight()
    gap = (C.NOTE * 2.2 + 8) / 72 / height_in * (hi - lo)  # two text lines and a margin, in data units
    for (_, label, color, *_), y in zip(OUTCOMES, spread(peaks, gap, gap / 2, hi - gap / 2), strict=True):
        ax.text(right, y, label, ha="right", va="center", fontsize=C.NOTE, color=color, fontweight="bold",
                linespacing=1.1, gid="label")  # fmt: skip


def group_heads(fr: C.Frame, axes: list, keys: list[str]) -> None:
    """A small grey heading above the first panel of each group (hybrids, attention-only)."""
    prev = None
    for ax, k in zip(axes, keys, strict=True):
        h = C.MODEL[k].hybrid
        if h != prev:
            ax.text(0, 1, "Hybrids" if h else "Attention-only",
                    transform=offset_copy(ax.transAxes, fig=fr.fig, y=C.LABEL * 2.2, units="points"),
                    fontsize=C.NOTE, color=C.CAPTION_INK, va="bottom", ha="left", gid="group")  # fmt: skip
        prev = h


def x_label(fr: C.Frame, axes: list) -> None:
    """One x label, centred under the panels of the last row."""
    boxes = [ax.get_position() for ax in axes]
    y0 = min(b.y0 for b in boxes)
    last = [ax for ax, b in zip(axes, boxes, strict=True) if abs(b.y0 - y0) < 1e-6]
    x0, x1 = min(ax.get_position().x0 for ax in last), max(ax.get_position().x1 for ax in last)
    tr = offset_copy(fr.fig.transFigure, fig=fr.fig, y=-(C.TICK * 1.6 + 8), units="points")
    fr.fig.text((x0 + x1) / 2, y0, "depth (% of the model's layers)", transform=tr, ha="center", va="top",
                fontsize=C.LABEL, color=C.INK)  # fmt: skip


def head_room(fr: C.Frame, points: float) -> None:
    """Lower the panels' top by `points`: the frame's top sits just under the header, and the panel titles (and the
    group headings) go above the panels."""
    gs = fr.axes[0].get_subplotspec().get_gridspec()
    gs.update(top=gs.top - points / 72 / fr.fig.get_figheight())


def gap_groups(fr: C.Frame, keys: list[str], cols: int, extra: float = 0.035) -> None:
    """Whitespace between hybrids and attention-only in a single row: panels after the switch move right."""
    axes = fr.axes
    switch = next((i for i in range(1, len(keys)) if C.MODEL[keys[i]].hybrid != C.MODEL[keys[i - 1]].hybrid), None)
    if switch is None or len(keys) != cols:
        return
    boxes = [ax.get_position() for ax in axes]
    span = boxes[-1].x1 - boxes[0].x0 - extra
    w = (span - (cols - 1) * (boxes[1].x0 - boxes[0].x1)) / cols
    sep = boxes[1].x0 - boxes[0].x1
    x = boxes[0].x0
    for i, (ax, b) in enumerate(zip(axes, boxes, strict=True)):
        if i == switch:
            x += extra
        ax.set_position([x, b.y0, w, b.height])
        x += w + sep


def draw(kind: str, data: dict[str, Depth], missing: dict[str, str], b: RB.Book) -> tuple[C.Frame, list[C.Number]]:
    if kind == "main":
        keys = [k for k in MAIN_MODELS if k in data and not data[k].faded]
    else:
        keys = [m.key for m in C.MODELS if m.key in data]
    hyb = [k for k in keys if C.MODEL[k].hybrid]
    att = [k for k in keys if not C.MODEL[k].hybrid]
    if kind == "main":  # one row, the groups apart
        rows, cols, size = 1, max(len(keys), 1), None
    else:  # hybrids above, attention-only below
        cols = max(len(hyb), len(att), 1)
        rows, size = (2 if hyb and att else 1), (12.0, 9.0)
    fr = C.frame(kind, title(data), SUBTITLE, how=HOW, caption=caption(data, keys, missing, b), nrows=rows,
                 ncols=cols, size=size, sharex=True, sharey=True, left=0.085, right=0.975, wspace=0.18,
                 hspace=0.85)  # fmt: skip
    head_room(fr, C.LABEL * 1.2 + 10 + C.NOTE * 1.3)  # the panel titles and the group headings above them
    if kind == "main":
        placed = list(zip(fr.axes, keys, strict=False))
        gap_groups(fr, keys, cols)
    else:
        grid_keys = (hyb + [""] * (cols - len(hyb)) + att + [""] * (cols - len(att))) if rows == 2 else keys
        placed = [(ax, k) for ax, k in zip(fr.axes, grid_keys, strict=False) if k]
        for ax, k in zip(fr.axes, grid_keys, strict=False):
            if not k:  # no empty panels
                fr.fig.delaxes(ax)
    nums: list[C.Number] = []
    for i, (ax, k) in enumerate(placed):
        nums += panel(ax, data[k])
        first_col = i == 0 or (kind == "full" and k == (att[0] if att else None))
        if first_col:
            ax.set_ylabel("% of patched answers")
        else:
            ax.tick_params(labelleft=False)
    first = placed[0][1]
    direct_labels(placed[0][0], data[first])
    group_heads(fr, [ax for ax, _ in placed], [k for _, k in placed])
    for ax, _ in placed:  # x tick labels on every panel's bottom (sharex hides none here: one row per group)
        ax.tick_params(labelbottom=True)
    x_label(fr, [ax for ax, _ in placed])
    return fr, nums


def build(kind: str, data: dict[str, Depth], missing: dict[str, str], b: RB.Book, out: Path = C.OUT) -> list[Path]:
    fr, nums = draw(kind, data, missing, b)
    return C.save(fr, STEM, nums, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--grid", type=Path, default=None, help="grid folder (default: the newest under results/cross_model)"
    )
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    grid_dir = a.grid or CMF.latest_grid()
    data, missing = load(grid_dir)
    b = RB.Book(grid_dir)
    for kind in [a.only] if a.only else ["main", "full"]:
        for p in build(kind, data, missing, b, a.out):
            print(p.relative_to(pins.REPO_ROOT) if p.is_relative_to(pins.REPO_ROOT) else p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
