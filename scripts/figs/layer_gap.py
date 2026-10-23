"""layer_gap (Dan's figure guide 6h): the 27B's layer-gap test, lookups only: the layer where a lens push stops moving
lookups against the layer where the full patch does.

Data: SUMMARY, results/early_push_where/d4_layer_gap_v2_27b/analysis-v2-20261023T090847Z/summary.json (rule v2): its
cells (Wilson rates per family, subset, layer, scale and push) and layer_gap.<subset>.<arm>.stop. Per layer and arm
the drawn point is the arm's valid cell with the highest upper bound on lookups switched, as the old
f_layer_gap_lens_vs_patch_27b (cross_model_figures.arm_curve over early_push_where.arm_cells: memory → prompt and
memory → memory changed <= OFF_PATH_MAX, the random push switching <= RAND_MAX of lookups at the same layer and scale,
8x for the patch), here on the summary's rates. The stops are recomputed from the drawn points (early_push_where.
arm_course: from the first layer on which every later tested layer has its upper bound < RAND_MAX) and must equal the
summary's. The band: from the lens push's stop to the full patch's, labelled with its size in layers. Beside the
lookups: recalls (BR) switched at the same cells, each run of the lens push's drawn size labelled (4x / 8x).

Lookups: the lens push in the accent purple, the full patch in a dark teal (dark grey is the recalls'); each line is
labelled directly with a plain definition. The caption says when the lens push's stop rests on a smaller size only
(the larger one fails the off-path check) and how few recalls that size moves: the stop may then be dose.

The dose-matched patch (the guide's third line) is not drawn: its run's predictions are not opened. Hook, for after
Dan says "open": --dose-summary PATH (draw(..., dose=Arm)) draws that summary's patch_dir arm as a third line.

MAIN: at the stated bridge's word (subset w). FULL: the word and the sentence (w, s), the layer-gap rule's verdict per
panel as a small grey word (H-gap: holds), the stop rule and the controls (embedding and random pushes) in the caption.

uv run python scripts/figs/layer_gap.py [--grid DIR] [--only main|full] [--out DIR] [--summary PATH]
                                        [--dose-summary PATH]
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from matplotlib.transforms import Bbox

from bridge_jspace import pins
from bridge_jspace import plot_style as PS
from scripts import cross_model_figures as CMF
from scripts import early_push_where as EPW
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import patch_by_depth as PD

STEM = "layer_gap"
RUN = "d4_layer_gap_v2_27b"
SUMMARY = EPW.RESULTS / RUN / "analysis-v2-20261023T090847Z" / "summary.json"
MODEL = "27b"
BAND = PD.BAND  # the gap: the pale lookup-purple band of the redesigned depth figures
PATCH = "#1B7F79"  # dark teal: the full patch's lookups (4.8:1 on white), apart from the lens push's purple
PLACE = {"w": "word", "s": "sentence"}
# per arm: name, its plain definition (the direct label's second line), line style, marker, color on lookups
# (recalls are all RECALL grey, told apart by style)
STYLE: dict[str, tuple[str, str, Any, str, str]] = {
    "lens": ("lens push", "lens direction only", "-", "o", C.LOOKUP),
    "patch": ("full patch", "the whole change", (0, (5, 2.5)), "s", PATCH),
    "patch_dir": ("dose-matched patch", "lens-push size", (0, (1.2, 2.2)), "^", PATCH),
}
# direct-label candidates per arm, in order: (point of the line, side of its 95% band)
PLACES: dict[str, tuple[tuple[str, str], ...]] = {
    "lens": (("peak", "above"), ("first", "above"), ("last moving", "above")),
    "patch": (("first", "above"), ("first", "below"), ("last moving", "above"), ("last moving", "below")),
    "patch_dir": (("first", "above"), ("first", "below"), ("last moving", "above"), ("last moving", "below"),
                  ("peak", "above")),
}  # fmt: skip
Triple = tuple[float, float, float]
Key = tuple[str, str, int, float, str]  # family, subset, layer, scale, push


@dataclass
class Arm:
    """One push over the layers at one subset: the drawn cell per layer (None: no valid cell) and its stop."""

    key: str  # lens, patch, patch_dir
    subset: str
    layers: list[int]
    scale: list[float | None]
    lookup: list[Triple | None]
    recall: list[Triple | None]
    n: list[int | None]  # lookups (BL) in the drawn cell
    n_recall: list[int | None]  # recalls (BR) in the same cell
    stop: int | None
    source: str  # the summary file, relative to the repo
    invalid_top: list[int]  # layers whose largest-scale cell failed the checks while a smaller one passed


def index(summary: dict) -> dict[Key, dict]:
    return {(c["family"], c["subset"], int(c["layer"]), float(c["scale"]), c["dir"]): c for c in summary["cells"]}


def rate(cell: dict | None, what: str = "to_x") -> float:
    return float("nan") if cell is None else float(cell[what][0])


def valid(idx: dict[Key, dict], sub: str, la: int, sc: float, arm: str) -> bool:
    """early_push_where.arm_cells' check on the summary's rates."""
    off = [rate(idx[(f, sub, la, sc, arm)], "changed") for f in ("RL", "RR") if (f, sub, la, sc, arm) in idx]
    rnd = rate(idx.get(("BL", sub, la, 8.0 if arm == "patch" else sc, "random")))
    return all(v <= EPW.OFF_PATH_MAX for v in off) and (math.isnan(rnd) or rnd <= EPW.RAND_MAX)


def stop_of(layers: list[int], lookup: list[Triple | None]) -> int | None:
    """early_push_where.arm_course's stop: the first tested layer from which every tested layer has its upper bound
    < RAND_MAX (a layer is tested when it has a valid cell; at the drawn cell, the arm's highest upper bound)."""
    stopped = {la: t[2] < EPW.RAND_MAX for la, t in zip(layers, lookup, strict=True) if t is not None}
    tested = list(stopped)
    return next((la for i, la in enumerate(tested) if all(stopped[g] for g in tested[i:])), None)


_UNSET = object()


def summary_stop(summary: dict, sub: str, arm: str) -> Any:
    for block in ("layer_gap", "dose_test"):
        g = (summary.get(block) or {}).get(sub) or {}
        if isinstance(g.get(arm), dict) and "stop" in g[arm]:
            return g[arm]["stop"]
    return _UNSET


def load_arm(summary: dict, sub: str, arm: str, source: str) -> Arm:
    idx = index(summary)
    layers = sorted({k[2] for k in idx if k[0] == "BL" and k[1] == sub and k[4] == arm})
    out = Arm(arm, sub, layers, [], [], [], [], [], None, source, [])
    for la in layers:
        scales = sorted(k[3] for k in idx if k[:3] == ("BL", sub, la) and k[4] == arm)
        ok = [sc for sc in scales if valid(idx, sub, la, sc, arm)]
        if ok and ok[-1] != scales[-1]:
            out.invalid_top.append(la)
        if not ok:
            for lst in (out.scale, out.lookup, out.recall, out.n, out.n_recall):
                lst.append(None)
            continue
        best = max(ok, key=lambda sc: idx[("BL", sub, la, sc, arm)]["to_x"][2])  # ties: the smaller scale (EPW order)
        bl, br = idx[("BL", sub, la, best, arm)], idx.get(("BR", sub, la, best, arm))
        out.scale.append(best)
        out.lookup.append(CMF.tri(bl["to_x"]))
        out.recall.append(CMF.tri(br["to_x"]) if br else None)
        out.n.append(int(bl["n"]))
        out.n_recall.append(int(br["n"]) if br else None)
    out.stop = stop_of(layers, out.lookup)
    want = summary_stop(summary, sub, arm)
    if want is not _UNSET and want != out.stop:
        raise ValueError(f"{source}: {arm} at {sub} stops at {out.stop} here, {want} in the summary")
    return out


def rel(p: Path) -> str:
    p = p.resolve()
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


def load(path: Path = SUMMARY, subsets: tuple[str, ...] = ("w", "s"), arms: tuple[str, ...] = ("lens", "patch"),
         ) -> dict[str, dict[str, Arm]]:  # fmt: skip
    """{subset: {arm: Arm}} from one summary.json."""
    s = json.loads(path.read_text())
    return {sub: {a: load_arm(s, sub, a, rel(path)) for a in arms} for sub in subsets}


def controls(path: Path = SUMMARY, subsets: tuple[str, ...] = ("w", "s")) -> dict[str, float]:
    """The highest share of lookups the embedding push and the random push switch at any layer and scale (0-1)."""
    idx = index(json.loads(path.read_text()))
    return {d: max((rate(c) for k, c in idx.items() if k[0] == "BL" and k[1] in subsets and k[4] == d), default=math.nan)
            for d in ("embed", "random")}  # fmt: skip


# ---------------------------------------------------------------- text


def gap_of(arms: dict[str, Arm]) -> int | None:
    a, b = arms["lens"].stop, arms["patch"].stop
    return None if a is None or b is None else b - a


def title(arms: dict[str, Arm]) -> str:
    d = gap_of(arms)
    if d is None:
        return "The layer-gap test: an arm never stops for good"
    if abs(d) <= EPW.NO_GAP:
        return "The full patch stops moving lookups with the lens push"
    if d < 0:
        return f"The lens push outlasts the full patch by {-d} layers"
    return f"The full patch outlasts the lens push by {d} layers"


VERDICT = {"H-gap": "holds", "H-no-gap": "fails"}  # the summary's layer-gap verdict, as the guide's verdict words


def verdicts(path: Path = SUMMARY) -> dict[str, str]:
    """{subset: 'holds' / 'fails' / 'inconclusive'}: the layer-gap rule's verdict in the summary (H-gap: holds)."""
    s = json.loads(path.read_text())
    return {sub: VERDICT.get(str(g.get("verdict")), "inconclusive") for sub, g in (s.get("layer_gap") or {}).items()}


def span(layers: list[int], sweep: list[int]) -> str:
    """'20–28' for layers that are consecutive in the sweep, else '20, 24'."""
    if len(layers) == 1:
        return str(layers[0])
    i = sweep.index(layers[0])
    if sweep[i : i + len(layers)] == layers:
        return f"{layers[0]}–{layers[-1]}"
    return ", ".join(map(str, layers))


WEAK = 0.20  # a lens push that switches fewer recalls than this (point) barely writes recall: its stop may be dose


def dose_caveat(lens: Arm) -> str:
    """'' when the lens push's stop rests on every size; else which size alone is valid from the stop on (the larger
    fails the off-path check) and, at the first of those layers where it switches < WEAK of recalls, how many."""
    if lens.stop is None:
        return ""
    at = {la: i for i, la in enumerate(lens.layers)}
    small = [la for la in lens.invalid_top if la >= lens.stop and lens.lookup[at[la]] is not None]
    if not small:
        return ""
    sizes = "/".join(f"{s:g}x" for s in sorted({lens.scale[at[la]] or 0.0 for la in small}))
    out = f"Only the {sizes} lens push is valid at {span(small, lens.layers)}"
    weak: list[tuple[int, float]] = []
    for la in small:
        t = lens.recall[at[la]]
        if t is None or t[0] >= WEAK:
            break
        weak.append((la, 100 * t[0]))
    if weak:
        lo, hi = min(v for _, v in weak), max(v for _, v in weak)
        pct = f"{lo:.0f}%" if round(lo) == round(hi) else f"{lo:.0f}–{hi:.0f}%"
        out += f", moving {pct} of recalls at {span([la for la, _ in weak], lens.layers)}"
    return out + ": its stop may be dose"


def caption(kind: str, data: dict[str, dict[str, Arm]], ctl: dict[str, float], dose: Arm | None) -> str:
    """MAIN: n and how a point is chosen, the controls; then the dose caveat (dose_caveat). FULL: the stop rule too;
    the caveat for the word."""
    subs = ["w"] if kind == "main" else list(data)
    ns = sorted({n for sub in subs for a in data[sub].values() for n in a.n if n is not None})
    n = f"n = {ns[0]}" if len(ns) == 1 else f"n = {ns[0]}–{ns[-1]}"
    if kind == "main":
        line1 = f"{n} scenes; point: the layer's valid cell moving the most lookups (95% CI)."
    else:
        line1 = (
            f"{n} scenes; point: best valid cell per layer; stop: all later upper bounds < {100 * EPW.RAND_MAX:.0f}%."
        )
    if all(not math.isnan(v) for v in ctl.values()):
        top = max(ctl.values())
        line1 += " Embedding, random pushes: " + ("0%." if top == 0 else f"≤ {100 * top:.0f}%.")
    caveat = dose_caveat(data["w"]["lens"])
    if caveat and kind == "full":
        caveat = "At the word o" + caveat[1:]
    pending = "dose test pending" if dose is None else "see the dose-matched patch"
    if not caveat:
        return line1 + "\n" + ("Dose-matched patch: not shown yet." if dose is None else "")
    return line1 + "\n" + caveat + (f" ({pending})." if kind == "main" else ".")


SUBTITLE = {
    "main": "One model (Qwen3.6-27B): % of lookups switched to the other bridge, by layer, at its word",
    "full": "One model (Qwen3.6-27B): % of lookups switched to the other bridge, by layer",
}
HOW = "Shaded: layers where the lens push moves no lookups but the full patch still does."
HOW_FULL = "Shaded: the lens push moves no lookups, the full patch still does. Pale bands: 95% CI."


# ---------------------------------------------------------------- drawing


def nan_triples(ts: list[Triple | None]) -> list[Triple]:
    return [t if t is not None else (math.nan, math.nan, math.nan) for t in ts]


def lines(ax, arm: Arm, what: str, size: float, width: float) -> list[C.Number]:
    """One arm's line (lookups: in the arm's color; recalls: RECALL grey) with a pale 95% band; returns the points."""
    _, _, ls, shape, own = STYLE[arm.key]
    color = own if what == "lookup" else C.RECALL
    ts = nan_triples(arm.lookup if what == "lookup" else arm.recall)
    ns = arm.n if what == "lookup" else arm.n_recall
    ax.fill_between(arm.layers, [100 * t[1] for t in ts], [100 * t[2] for t in ts], color=color, alpha=0.14, lw=0,
                    zorder=1)  # fmt: skip
    ax.plot(arm.layers, [100 * t[0] for t in ts], color=color, lw=width, linestyle=ls, marker=shape, markersize=size,
            markerfacecolor=color, markeredgecolor=color, zorder=4 if arm.key == "lens" else 3, gid="mark")  # fmt: skip
    fam = "BL" if what == "lookup" else "BR"
    return [C.Number(100 * t[0], f"% of {what}s switched, {STYLE[arm.key][0]}", model=MODEL,
                     setting=f"layer gap, at the bridge's {PLACE.get(arm.subset, arm.subset)}",
                     ci=(100 * t[1], 100 * t[2]), n=n, source=arm.source,
                     extra={"family": fam, "subset": arm.subset, "layer": la, "scale": sc, "push": arm.key})
            for la, t, sc, n in zip(arm.layers, ts, arm.scale, ns, strict=True)
            if not math.isnan(t[0])]  # fmt: skip


def band(ax, arms: dict[str, Arm], label: bool) -> list[C.Number]:
    a, b = arms["lens"].stop, arms["patch"].stop
    if a is None or b is None or b <= a:
        return []
    d = b - a
    ax.axvspan(a, b, color=BAND, lw=0, zorder=0)
    if label:
        ax.text((a + b) / 2, 101, f"{d} layers", ha="center", va="top", fontsize=C.NOTE, fontweight="bold",
                color=C.INK, gid="gap label")  # fmt: skip
    src = arms["lens"].source
    return [C.Number(float(d), "layers between the stops (full patch - lens push)", model=MODEL,
                     setting=f"layer gap, at the bridge's {PLACE.get(arms['lens'].subset)}", source=src,
                     extra={"lens stop": a, "patch stop": b})]  # fmt: skip


Spot = tuple[float, float, str, str]  # x, y (data), ha, va


class Placer:
    """Puts each label at the first of its candidate spots that stays inside the panel and off every drawn line, the
    labels already placed and the panel's insets; when none is free, at the free spot of a grid over the panel nearest
    the first candidate (a crowded panel, e.g. with the dose-matched line in); the first candidate when none is."""

    def __init__(self, ax) -> None:
        self.ax, self.r = ax, ax.figure.canvas.get_renderer()
        self.taken = [a.get_tightbbox(self.r) for a in ax.child_axes] + [t.get_window_extent(self.r) for t in ax.texts]
        self.taken += [b for _, b in PS.graphic_boxes(ax.figure, self.r)]  # the markers, as the overlap check sees them
        self.paths: list[tuple[float, float]] = []
        for ln in ax.get_lines():
            xy = ln.get_transform().transform(ln.get_xydata())
            for (x0, y0), (x1, y1) in itertools.pairwise(xy):
                if not any(map(math.isnan, (x0, y0, x1, y1))):
                    self.paths += [(x0 + (x1 - x0) * f / 24, y0 + (y1 - y0) * f / 24) for f in range(25)]
        self.inner = ax.get_window_extent(self.r)

    def free_box(self, box: Any) -> bool:
        b, inner = box.padded(4), self.inner
        return (inner.x0 <= b.x0 and b.x1 <= inner.x1 and inner.y0 <= b.y0 and b.y1 <= inner.y1
                and not any(b.overlaps(o) for o in self.taken)
                and not any(b.contains(x, y) for x, y in self.paths))  # fmt: skip

    def free(self, t: Any) -> bool:
        return self.free_box(t.get_window_extent(self.r))

    def put(self, text: str, spots: list[Spot], **kw: Any) -> None:
        made = []
        for x, y, ha, va in spots:
            made.append(self.ax.text(x, y, text, ha=ha, va=va, fontsize=C.NOTE, gid="label", **kw))
            if self.free(made[-1]):
                break
        keep = next((t for t in made if self.free(t)), made[0])
        for t in made:
            if t is not keep:
                t.remove()
        if not self.free(keep):  # the grid: same size, lower-left corners every 1/40 x 1/30 of the free room
            first = keep.get_window_extent(self.r)
            w, h, cx, cy = first.width, first.height, (first.x0 + first.x1) / 2, (first.y0 + first.y1) / 2
            grid = [Bbox.from_bounds(self.inner.x0 + 4 + (self.inner.width - w - 8) * i / 39,
                                     self.inner.y0 + 4 + (self.inner.height - h - 8) * j / 29, w, h)
                    for i in range(40) for j in range(30)]  # fmt: skip
            ok = [b for b in grid if self.free_box(b)]
            if ok:
                b = min(ok, key=lambda b: math.hypot(b.x0 + w / 2 - cx, b.y0 + h / 2 - cy))
                keep.set_position(self.ax.transData.inverted().transform((b.x0, b.y0)))
                keep.set_horizontalalignment("left")
                keep.set_verticalalignment("bottom")
        self.taken.append(keep.get_window_extent(self.r))


def spots(pts: list[tuple[int, Triple]], prefer: tuple[tuple[str, str], ...]) -> list[Spot]:
    """Candidate spots by a line's points: the preferred (point of the line, side of its band) first, then above and
    below every point."""
    moving = [(la, t) for la, t in pts if t[1] > EPW.RAND_MAX]
    at = {"peak": max(pts, key=lambda p: p[1][0]), "first": pts[0], "last moving": (moving or pts)[-1]}
    out: list[Spot] = []
    for (la, t), where, side in [(at[w], w, s) for w, s in prefer] + [(p, "point", s) for s in ("above", "below")
                                                                      for p in pts]:  # fmt: skip
        up = side == "above"
        x, ha = (la + 0.5, "left") if where == "last moving" else (la, "center" if where == "peak" else "left")
        out.append((x, 100 * (t[2] if up else t[1]) + (3 if up else -3), ha, "bottom" if up else "top"))
    return out


def label_lines(ax, arms: dict[str, Arm], dose: Arm | None) -> None:
    """Each lookup line's name and plain definition, in its color, by its line (PLACES)."""
    p = Placer(ax)
    for arm in [arms["lens"], arms["patch"], *([dose] if dose else [])]:
        pts = [(la, t) for la, t in zip(arm.layers, arm.lookup, strict=True) if t is not None]
        if pts:
            name, what, *_, color = STYLE[arm.key]
            p.put(f"{name}\n({what})", spots(pts, PLACES[arm.key]), color=color, fontweight="bold", linespacing=1.1)


def label_recalls(ax, arms: dict[str, Arm], dose: Arm | None, names: bool) -> None:
    """The recall panel: each run of layers where the lens push's drawn size is the same labelled with that size
    ('4x' / '8x'), and (names) each line's name."""
    p = Placer(ax)
    lens = arms["lens"]
    if names:  # first: the names need the larger free spots
        for arm in [arms["patch"], lens, *([dose] if dose else [])]:
            ps = [(la, t) for la, t in zip(arm.layers, arm.recall, strict=True) if t is not None]
            if ps:
                p.put(STYLE[arm.key][0], spots(ps, (("first", "below"), ("first", "above"), ("peak", "above"))),
                      color=C.RECALL, fontweight="bold")  # fmt: skip
    pts = [(la, t, sc) for la, t, sc in zip(lens.layers, lens.recall, lens.scale, strict=True) if t is not None]
    runs: list[list[tuple[int, Triple, float | None]]] = []
    for q in pts:
        if runs and runs[-1][-1][2] == q[2] and lens.layers.index(q[0]) == lens.layers.index(runs[-1][-1][0]) + 1:
            runs[-1].append(q)
        else:
            runs.append([q])
    for run in runs:
        mid = run[len(run) // 2][0] if len(run) % 2 else (run[0][0] + run[-1][0]) / 2
        top, low = max(t[2] for _, t, _ in run), min(t[1] for _, t, _ in run)
        cands: list[Spot] = [(mid, 100 * top + 3, "center", "bottom"), (mid, 100 * low - 3, "center", "top")]
        cands += [(la + dx, 100 * t[0] + dy, "left", "bottom") for la, t, _ in run
                  for dx, dy in ((0.6, 4), (1.0, 3), (1.6, 3))]  # right of a point, then farther  # fmt: skip
        cands += spots([(la, t) for la, t, _ in run], ())
        p.put(f"{run[0][2] or 0:g}x", cands, color=C.CAPTION_INK)


def axes_style(ax, xlabel: bool, ylabel: str | None, ticks: list[int]) -> None:
    ax.set_xlim(10.8, 35.2)
    ax.set_ylim(0, 105)
    ax.set_xticks(ticks)
    ax.set_yticks([0, 50, 100])
    if xlabel:
        ax.set_xlabel("layer (of 64)")
    if ylabel:
        ax.set_ylabel(ylabel)


def recall_axes(ax, arms: dict[str, Arm], dose: Arm | None, xlabel: bool, names: bool) -> list[C.Number]:
    """Recalls switched at the same cells, the gap shaded as on the lookups (its number booked there), the lens push's
    drawn size marked per run of layers, the lines named when `names`."""
    if (gap_of(arms) or 0) > 0:
        ax.axvspan(arms["lens"].stop, arms["patch"].stop, color=BAND, lw=0, zorder=0)
    nums: list[C.Number] = []
    for arm in [*arms.values(), *([dose] if dose else [])]:
        nums += lines(ax, arm, "recall", 5, 2.0)
    ax.set_xlim(10.8, 35.2)
    ax.set_ylim(0, 105)
    ax.set_xticks([12, 20, 28])
    ax.set_yticks([0, 50, 100])
    ax.set_ylabel("% of recalls switched")
    if xlabel:
        ax.set_xlabel("layer")
    ax.set_title("Recalls, same pushes", loc="left", fontsize=C.NOTE, color=C.RECALL, pad=8)
    label_recalls(ax, arms, dose, names)
    return nums


def draw(kind: str, data: dict[str, dict[str, Arm]], ctl: dict[str, float], dose: dict[str, Arm] | None = None,
         rule: dict[str, str] | None = None) -> tuple[C.Frame, list[C.Number]]:  # fmt: skip
    """Per subset (MAIN: the word; FULL: the word and the sentence) the lookups panel and the recalls beside it; FULL
    also names the subset and the layer-gap rule's verdict (`rule`, from verdicts()) as a small grey word. `dose`:
    {subset: the dose-matched patch's Arm}, drawn as a third line (None until its predictions are opened)."""
    subs = ["w"] if kind == "main" else [s for s in ("w", "s") if s in data]
    cap = caption(kind, data, ctl, (dose or {}).get("w"))
    sub_title = SUBTITLE["main" if kind == "main" else "full"]
    fr = C.frame(kind, title(data["w"]), sub_title, how=HOW if kind == "main" else HOW_FULL, caption=cap,
                 nrows=len(subs), ncols=2, width_ratios=[2.5, 1], left=0.085, right=0.975, wspace=0.3,
                 hspace=0.6)  # fmt: skip
    PD.head_room(fr, C.LABEL * 1.2 + 8)  # the panel titles above the panels
    nums: list[C.Number] = []
    for i, sub in enumerate(subs):
        ax, side = fr.axes[2 * i], fr.axes[2 * i + 1]
        arms = data[sub]
        d = (dose or {}).get(sub)
        nums += band(ax, arms, label=True)
        for arm in [*arms.values(), *([d] if d else [])]:
            nums += lines(ax, arm, "lookup", 7, 2.6)
        last = i == len(subs) - 1
        axes_style(ax, last, "% of lookups switched", [12, 16, 20, 24, 28, 32])
        if kind == "full":
            ax.set_title(f"At the bridge's {PLACE[sub]}", loc="left", fontsize=C.LABEL, fontweight="bold", pad=8)
            if rule and sub in rule:
                ax.set_title(f"layer-gap rule: {rule[sub]}", loc="right", fontsize=C.NOTE, color=C.CAPTION_INK, pad=8)
        nums += recall_axes(side, arms, d, last, names=i == 0)
        if i == 0:
            label_lines(ax, arms, d)
    return fr, nums


def build(kind: str, data: dict[str, dict[str, Arm]], ctl: dict[str, float], dose: dict[str, Arm] | None = None,
          out: Path = C.OUT, rule: dict[str, str] | None = None) -> list[Path]:  # fmt: skip
    fr, nums = draw(kind, data, ctl, dose, rule)
    return C.save(fr, STEM, nums, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", type=Path, default=None, help="grid folder (unused by the numbers: not a grid cell)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    ap.add_argument("--summary", type=Path, default=SUMMARY, help="the layer-gap run's summary.json")
    ap.add_argument(
        "--dose-summary",
        type=Path,
        default=None,
        help="the dose-matched run's summary.json: draws its patch_dir arm (only after Dan says 'open')",
    )
    a = ap.parse_args(argv)
    if a.grid is not None:
        RB.Book(a.grid)  # the grid must parse; the layer-gap run is its own run, not a grid cell
    data = load(a.summary)
    dose = load(a.dose_summary, arms=("patch_dir",)) if a.dose_summary else None
    dose_arms = {sub: arms["patch_dir"] for sub, arms in dose.items()} if dose else None
    ctl, rule = controls(a.summary), verdicts(a.summary)
    for kind in [a.only] if a.only else ["main", "full"]:
        for p in build(kind, data, ctl, dose_arms, a.out, rule):
            print(rel(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
