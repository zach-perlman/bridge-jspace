"""window (Dan, 23 Oct, for the TA call): the band of depth where the lookup ignores the lens form but recall follows.

Per model (27B, 9B, OLMo-3, 122B), x = depth (% of the model's layers), y = % switched to the other bridge's answer:
  full patch   the other bridge's whole state copied at the stated bridge's word (statement_positions maps, topics2
               scenes: family PP = lookups, set bridge_word, source cf; summary.json rates). On the 27B also the full
               patch of the layer-gap run (d4_layer_gap_v2_27b), which has the patch and the pushes on the same scenes.
  lens push    the push along the lens direction at the word, 8x (early_push_where runs, animal-suite scenes: BL =
               lookups, BR = recalls, subset w, scale 8, dir lens). Valid cells only: memory -> prompt and memory ->
               memory changed <= OFF_PATH_MAX and the random push switching <= RAND_MAX of lookups at the same cell
               (early_push_where.cell_valid); the invalid layers are left out of MAIN and drawn pale in FULL.
  random push  the random push at 8x on lookups (BL, w, 8, random).
  lens part    122B only: the J-space part of the full copy over the whole context (statement_positions parts run,
               layers 24/27/30; part jspace, null False, source cf) for lookups (PP) and recalls (PM), as points. The
               lookups at layer 24 are a grid cell (finding 2, draw 2) and booked through cell_number.
The 9B's two push runs (the first draw and its fresh seed2 draw) are pooled: counts recovered from each cell's rate and n.

Shaded (the band): the push layers where the lens push on lookups is valid with its Wilson upper bound < LENS_UB, and
the full patch on lookups (the same-scene patch where there is one, else the map at the same layer) is >= PATCH_MIN.
Each band layer stands for the stretch half-way to its neighbours (patch_by_depth.layer_spans).

Hook (batch A, never opened here): extra lines for the size-matched patches, `extra={model: [Series]}` in draw() or
--extra MODEL=SUMMARY (arms patch_dir and patch_dir_perp at 8x, lookups, valid cells), drawn as further lines.

uv run python scripts/figs/window.py [--grid DIR] [--only main|full] [--out DIR] [--extra MODEL=SUMMARY ...]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import cross_model_figures as CMF
from scripts import early_push_where as EPW
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import layer_gap as LG
from scripts.figs import patch_by_depth as PD

STEM = "window"
SP = pins.RESULTS_DIR / "statement_positions"
MODELS = ("27b", "9b", "olmo", "122b")
MAPS = {"27b": "d1_topics2_map_27b", "9b": "qwen35_9b_d1_topics2_map", "olmo": "olmo3_7b_instruct_jpp_d1_topics2_map",
        "122b": "qwen35_122b_d1_topics2_map"}  # fmt: skip
PUSHES = {"27b": ("d4_layer_gap_v2_27b",), "9b": ("qwen35_9b_d4_where", "qwen35_9b_d4_where_fresh_seed2"),
          "olmo": ("olmo3_7b_instruct_jpp_d4_where_raw",), "122b": ("qwen35_122b_d4_where",)}  # fmt: skip
FULL_EXTRA = ("27b first", "27b", ("d4_where_27b",))  # FULL only: the 27B's first push run (other animal-suite scenes)
SAME_SCENES = {"27b": "d4_layer_gap_v2_27b"}  # runs with the full patch on the pushes' own scenes
PARTS = {"122b": ("qwen35_122b_d1_topics2_parts", (24, 27, 30))}
PART_CELL = ("f2", "122b", "draw 2", 24)  # the grid cell the 122B's lookups point at layer 24 is
SCALE = 8.0
PATCH_MIN, LENS_UB = 0.30, EPW.RAND_MAX
PATCH = LG.PATCH
Triple = tuple[float, float, float]
# series key -> (label, color, line style, marker, line width)
STYLE: dict[str, tuple[str, str, Any, str, float]] = {
    "patch": ("full patch → lookups", PATCH, "-", "s", 2.4),
    "patch_same": ("full patch,\nsame scenes", PATCH, (0, (4, 2)), "s", 1.8),
    "lens_lookup": ("lens push → lookups", C.LOOKUP, "-", "o", 2.4),
    "lens_recall": ("lens push → recalls", C.RECALL, "-", "o", 2.4),
    "random": ("random push → lookups", C.CONTROL, "-", "", 1.6),
    "part_lookup": ("diamonds: lens part", C.LOOKUP, "", "D", 0),
    "part_recall": ("diamonds: lens part", C.RECALL, "", "D", 0),
    "patch_dir": ("size-matched patch → lookups", PATCH, (0, (1.2, 2.2)), "^", 1.8),
    "patch_dir_perp": ("size-matched patch, lens part removed", PATCH, (0, (1.2, 2.2)), "v", 1.8),
}


@dataclass
class Series:
    key: str
    layers: list[int]
    rates: list[Triple | None]  # drawn points; None where left out (an invalid cell)
    n: list[int | None]
    source: str  # relative paths, joined by " + " for pooled runs
    invalid: list[Triple | None] = field(default_factory=list)  # the left-out points (FULL: pale)
    number: dict[int, C.Number] = field(default_factory=dict)  # points booked as grid cells, by layer


@dataclass
class Panel:
    key: str  # MODELS or "27b first"
    model: str
    series: dict[str, Series]
    band: list[int]  # push layers in the band

    @property
    def n_layers(self) -> int:
        return CMF.n_layers(self.model)

    def depth(self, layer: float) -> float:
        return 100 * layer / self.n_layers


def rel(p: Path) -> str:
    return str(p.resolve().relative_to(pins.REPO_ROOT)) if p.resolve().is_relative_to(pins.REPO_ROOT) else str(p)


def tri(k: int, n: int) -> Triple:
    return CMF.tri(wilson(k, n))


# ---------------------------------------------------------------- loading


def map_series(run: str, family: str = "PP", where: str = "bridge_word") -> Series:
    """The full patch (C's copy, source cf) at the set: % flipped to X's answer per layer (the map's summary rates)."""
    p = SP / run / "summary.json"
    rows = [r for r in json.loads(p.read_text())["rates"] if r["family"] == family and r["set"] == where]
    rows.sort(key=lambda r: r["layer"])
    return Series("patch", [int(r["layer"]) for r in rows], [CMF.tri(r["cf"]["flips"]) for r in rows],
                  [int(r["n"]) for r in rows], rel(p))  # fmt: skip


Counts = dict[tuple[str, str, int, float, str], dict[str, tuple[int, int]]]  # cell -> {to_x / changed: (k, n)}


def pooled(runs: tuple[str, ...]) -> tuple[Counts, str]:
    """The runs' summary cells as counts (k = rate x n, rounded), summed over runs; and the sources."""
    out: Counts = {}
    paths = []
    for run in runs:
        p = EPW.RESULTS / run / "summary.json"
        paths.append(rel(p))
        for c in json.loads(p.read_text())["cells"]:
            key = (c["family"], c["subset"], int(c["layer"]), float(c["scale"]), c["dir"])
            n = int(c["n"])
            cur = out.setdefault(key, {"to_x": (0, 0), "changed": (0, 0)})
            for what in ("to_x", "changed"):
                k = round(float(c[what][0]) * n)
                cur[what] = (cur[what][0] + k, cur[what][1] + n)
    return out, " + ".join(paths)


def rate_of(cells: Counts, key: tuple[str, str, int, float, str], what: str = "to_x") -> Triple | None:
    c = cells.get(key)
    return None if c is None or c[what][1] == 0 else tri(*c[what])


def valid(cells: Counts, la: int, sc: float, arm: str = "lens", sub: str = "w") -> bool:
    """early_push_where.cell_valid / arm_cells on pooled counts: the arm changes <= OFF_PATH_MAX of memory -> prompt
    and memory -> memory, and the random push (8x for the full patch) switches <= RAND_MAX of lookups."""
    off = [rate_of(cells, (f, sub, la, sc, arm), "changed") for f in ("RL", "RR")]
    rnd = rate_of(cells, ("BL", sub, la, 8.0 if arm == "patch" else sc, "random"))
    return all(o is None or o[0] <= EPW.OFF_PATH_MAX for o in off) and (rnd is None or rnd[0] <= EPW.RAND_MAX)


def arm_series(cells: Counts, source: str, key: str, arm: str, family: str = "BL", sc: float = SCALE,
               check: bool = True) -> Series:  # fmt: skip
    """One push arm by layer at the word: its valid cells drawn, the others kept aside as `invalid`."""
    layers = sorted({k[2] for k in cells if k[0] == family and k[1] == "w" and k[3] == sc and k[4] == arm})
    s = Series(key, layers, [], [], source, [])
    for la in layers:
        r = rate_of(cells, (family, "w", la, sc, arm))
        ok = not check or valid(cells, la, sc, arm)
        s.rates.append(r if ok else None)
        s.invalid.append(None if ok else r)
        s.n.append(cells[(family, "w", la, sc, arm)]["to_x"][1])
    return s


def parts_series(run: str, layers: tuple[int, ...], family: str, key: str) -> Series:
    """The J-space part of the whole-context copy (cf, not the null) at the parts run's layers: % switched to X."""
    p = SP / run / "outcomes.jsonl"
    hits = {la: [0, 0] for la in layers}
    for line in p.read_text().splitlines():
        o = json.loads(line)
        if (o.get("family") == family and o.get("set") == "context" and o.get("part") == "jspace"
                and o.get("source") == "cf" and o.get("null") is False and o.get("layer") in hits):  # fmt: skip
            hits[o["layer"]][0] += o["role"] == "b"
            hits[o["layer"]][1] += 1
    ls = [la for la in layers if hits[la][1]]
    return Series(key, ls, [tri(*hits[la]) for la in ls], [hits[la][1] for la in ls], rel(p))


def band_of(series: dict[str, Series]) -> list[int]:
    """Push layers where the lens push on lookups is valid with upper bound < LENS_UB and the full patch (same scenes
    where there is one) is >= PATCH_MIN at the same layer."""
    lens = series["lens_lookup"]
    patch = series.get("patch_same") or series["patch"]
    at = dict(zip(patch.layers, patch.rates, strict=True))
    return [la for la, r in zip(lens.layers, lens.rates, strict=True)
            if r is not None and r[2] < LENS_UB and (p := at.get(la)) is not None and p[0] >= PATCH_MIN]  # fmt: skip


def panel_of(key: str, model: str, runs: tuple[str, ...], map_run: str | None, extra: list[Series] | None = None,
             b: RB.Book | None = None) -> Panel:  # fmt: skip
    cells, src = pooled(runs)
    series: dict[str, Series] = {}
    if map_run:
        series["patch"] = map_series(map_run)
    if len(runs) == 1 and runs[0] in SAME_SCENES.values():
        series["patch_same"] = arm_series(cells, src, "patch_same", "patch", sc=0.0)
    series["lens_lookup"] = arm_series(cells, src, "lens_lookup", "lens")
    series["lens_recall"] = arm_series(cells, src, "lens_recall", "lens", family="BR")
    series["random"] = arm_series(cells, src, "random", "random", check=False)
    if key in PARTS:
        run, layers = PARTS[key]
        series["part_lookup"] = parts_series(run, layers, "PP", "part_lookup")
        series["part_recall"] = parts_series(run, layers, "PM", "part_recall")
        if b is not None:
            book_part_cell(series["part_lookup"], b)
    for s in extra or []:
        series[s.key] = s
    if "patch" not in series:
        series["patch"] = series.pop("patch_same")
    return Panel(key, model, series, band_of(series))


def book_part_cell(s: Series, b: RB.Book) -> None:
    """The 122B's lookups point at layer 24 is the grid cell PART_CELL: drawn and booked with the cell's value (it must
    match the file's to 0.1 point)."""
    f, m, setting, la = PART_CELL
    if la not in s.layers:
        return
    num = C.cell_number(b, f, m, setting, "% of lookups switched, lens part of the context")
    i = s.layers.index(la)
    r = s.rates[i]
    if num is None or r is None:
        return
    if abs(num.value - 100 * r[0]) > 0.05 + 1e-9:
        raise ValueError(f"{s.source}: layer {la} gives {100 * r[0]:.2f}%, the grid {num.value}%")
    lo, hi = num.ci or (100 * r[1], 100 * r[2])
    s.rates[i] = (num.value / 100, lo / 100, hi / 100)
    num.extra = {"layer": la, "source file": s.source}
    s.number[la] = num


def load(b: RB.Book | None = None, extra: dict[str, list[Series]] | None = None) -> dict[str, Panel]:
    """MAIN's four panels and FULL's extra 27B panel, in that order."""
    out = {m: panel_of(m, m, PUSHES[m], MAPS[m], (extra or {}).get(m), b) for m in MODELS}
    key, model, runs = FULL_EXTRA
    out[key] = panel_of(key, model, runs, MAPS[model], None, b)
    return out


def extra_arms(path: Path) -> list[Series]:
    """The hook: a (batch A) summary's size-matched patch arms at 8x on lookups, valid cells only."""
    cells: Counts = {}
    for c in json.loads(path.read_text())["cells"]:
        n = int(c["n"])
        cells[(c["family"], c["subset"], int(c["layer"]), float(c["scale"]), c["dir"])] = {
            w: (round(float(c[w][0]) * n), n) for w in ("to_x", "changed")}  # fmt: skip
    return [arm_series(cells, rel(path), arm, arm) for arm in ("patch_dir", "patch_dir_perp")
            if any(k[4] == arm for k in cells)]  # fmt: skip


# ---------------------------------------------------------------- text


def recall_follows(p: Panel) -> bool:
    """In the band, the valid lens push switches >= PATCH_MIN of recalls at some band layer."""
    rec = dict(zip(p.series["lens_recall"].layers, p.series["lens_recall"].rates, strict=True))
    return any((r := rec.get(la)) is not None and r[0] >= PATCH_MIN for la in p.band)


def title(panels: dict[str, Panel]) -> str:
    """The claim on MAIN's models (28 pt bold fits ~50 characters): every model has a band with recall following the
    lens push (>= PATCH_MIN of recalls at a band layer), or which do."""
    main = [panels[m] for m in MODELS if m in panels]
    both = [p for p in main if p.band and recall_follows(p)]
    if both and len(both) == len(main):
        return "A band: lookups ignore the lens, recall follows"
    if len(both) == 1:
        return f"In the band, only the {C.MODEL[both[0].model].short}'s recall follows the lens"
    if both:
        return f"In the band, recall follows the lens on {len(both)} of {len(main)} models"
    if any(p.band for p in main):
        return "In the band, recall does not follow the lens"
    return "No band where lookups ignore the lens"


def band_text(p: Panel) -> str:
    if not p.band:
        return "none"
    runs, cur = [], [p.band[0]]
    lens_layers = p.series["lens_lookup"].layers
    for la in p.band[1:]:
        if lens_layers.index(la) == lens_layers.index(cur[-1]) + 1:
            cur.append(la)
        else:
            runs.append(cur)
            cur = [la]
    runs.append(cur)
    return ", ".join(f"L{r[0]}" if len(r) == 1 else f"L{r[0]}–{r[-1]}" for r in runs)


def caption(kind: str, panels: dict[str, Panel], keys: list[str]) -> str:
    """Line 1: the scene sets; line 2: the sizes, the invalid layers, the random push (FULL: and n)."""
    line1 = ("Scenes differ: full patch on topic scenes, pushes on the animal suite (27B dashed: the pushes' "
             "scenes).")  # fmt: skip
    if kind == "main":
        line2 = "Sizes differ: the full patch is not size-matched to the 8x push. Gaps: push not valid there. Grey: random push."
    else:
        ns = sorted({n for k in keys for n in panels[k].series["lens_lookup"].n if n})
        n = f"{ns[0]}" if len(ns) == 1 else f"{ns[0]}–{ns[-1]}"
        line2 = f"Sizes differ (patch vs 8x push). Pale: push not valid. Grey: random push. Push n = {n} (9B: 2 draws pooled)."
    return line1 + "\n" + line2


SUBTITLE = "% switched to the other bridge's answer by depth, edits at the stated bridge's word"
HOW = "Shaded: full patch moves ≥ 30% of lookups, lens push none (upper bound < 5%)."


# ---------------------------------------------------------------- drawing


def draw_series(ax, p: Panel, s: Series, faded: bool) -> list[C.Number]:
    label, color, ls, marker, width = STYLE[s.key]
    x = [p.depth(la) for la in s.layers]
    nums: list[C.Number] = []
    pts = [(xx, r) for xx, r in zip(x, s.rates, strict=True)]
    y = [math.nan if r is None else 100 * r[0] for _, r in pts]
    lo = [math.nan if r is None else 100 * r[1] for _, r in pts]
    hi = [math.nan if r is None else 100 * r[2] for _, r in pts]
    face = color  # filled throughout: the panels are named, so hybrid / attention-only needs no marker code here
    if ls:  # a line with a pale 95% band
        ax.fill_between(x, lo, hi, color=color, alpha=0.13, lw=0, zorder=1)
        ax.plot(x, y, color=color, lw=width, linestyle=ls, marker=marker or None, markersize=5.5,
                markerfacecolor=face, markeredgecolor=color, markeredgewidth=1.5, zorder=3,
                gid="mark" if marker else None)  # fmt: skip
    else:  # points with thin, light error bars (the markers solid on top)
        ax.errorbar(x, y, yerr=[[a - b for a, b in zip(y, lo, strict=True)], [b - a for a, b in zip(y, hi, strict=True)]],
                    fmt="none", ecolor=color, zorder=4, **C.ERRORBAR)  # fmt: skip
        ax.plot(x, y, linestyle="none", marker=marker, markersize=8.5, markerfacecolor=color, markeredgecolor="white",
                markeredgewidth=1.2, zorder=5, gid="mark")  # fmt: skip
    if faded and s.invalid:
        xi = [p.depth(la) for la, r in zip(s.layers, s.invalid, strict=True) if r is not None]
        yi = [100 * r[0] for r in s.invalid if r is not None]
        ax.plot(xi, yi, linestyle="none", marker=marker or "o", markersize=5.5, markerfacecolor="white",
                markeredgecolor=C.CONTROL, markeredgewidth=1.4, zorder=2, gid="mark")  # fmt: skip
    for la, xx, r, n in zip(s.layers, x, s.rates, s.n, strict=True):
        if r is None:
            continue
        if la in s.number:
            nums.append(s.number[la])
            continue
        nums.append(C.Number(100 * r[0], f"% switched, {label}", model=p.model, setting=p.key, ci=(100 * r[1], 100 * r[2]),
                             n=n, source=s.source, extra={"layer": la, "depth": xx, "series": s.key}))  # fmt: skip
    if faded and s.invalid:
        for la, r, n in zip(s.layers, s.invalid, s.n, strict=True):
            if r is not None:
                nums.append(C.Number(100 * r[0], f"% switched, {label} (invalid cell, drawn pale)", model=p.model,
                                     setting=p.key, ci=(100 * r[1], 100 * r[2]), n=n, source=s.source,
                                     extra={"layer": la, "depth": p.depth(la), "series": s.key, "valid": False}))  # fmt: skip
    return nums


ORDER = (
    "random",
    "patch_same",
    "patch",
    "patch_dir",
    "patch_dir_perp",
    "lens_recall",
    "lens_lookup",
    "part_recall",
    "part_lookup",
)  # drawing order: controls first, the lookups on top


def panel(ax, p: Panel, faded: bool) -> list[C.Number]:
    nums: list[C.Number] = []
    for lo, hi in PD.layer_spans(p.series["lens_lookup"].layers, p.band, p.n_layers):
        ax.axvspan(lo, hi, facecolor=PD.BAND, edgecolor=PD.BAND_EDGE, lw=1.0, zorder=0)
    if p.band:
        nums.append(C.Number(float(len(p.band)), "band layers (count)", model=p.model, setting=p.key,
                             source=p.series["lens_lookup"].source,
                             extra={"layers": p.band, "depth": [p.depth(la) for la in p.band]}))  # fmt: skip
    for key in ORDER:
        if key in p.series:
            nums += draw_series(ax, p, p.series[key], faded)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    ax.set_xticks([0, 50, 100])
    ax.set_yticks([0, 50, 100])
    name = C.MODEL[p.model].name + (", first push run" if p.key != p.model else "")
    ax.set_title(name, loc="left", fontsize=C.LABEL, fontweight="bold", pad=8)
    return nums


def direct_labels(ax, p: Panel, keys: tuple[str, ...]) -> None:
    """Each named line's label in its color, by its line (the layer_gap placer: off lines, markers and other labels)."""
    placer = LG.Placer(ax)
    for key in keys:
        s = p.series.get(key)
        if s is None:
            continue
        pts = [(p.depth(la), r) for la, r in zip(s.layers, s.rates, strict=True) if r is not None]
        if not pts:
            continue
        label, color, *_ = STYLE[key]
        if key.startswith("part"):  # both colors of diamonds: a neutral name
            label, color = label.replace(": ", ":\n"), C.INK2
        prefer = (("peak", "above"), ("first", "above"), ("last moving", "above"), ("first", "below"))
        placer.put(label.replace(" → ", "\n→ "), LG.spots(pts, prefer), color=color, fontweight="bold",
                   linespacing=1.05, optional=key.startswith("part"))  # fmt: skip


LABEL_AT = {"122b": ("patch", "lens_recall", "lens_lookup", "part_lookup")}  # which panel names which line; the
# random push and the 27B's dashed same-scene patch are named in the caption


def valid_note(ax, p: Panel) -> None:
    """A small grey note: at how many push layers the 8x lens push is valid (the drawn ones)."""
    s = p.series["lens_lookup"]
    ok = sum(r is not None for r in s.rates)
    if ok == len(s.layers):
        return
    spots: list[LG.Spot] = [(97, y, "right", "top") for y in (100, 85, 70, 55, 40)]
    spots += [(3, y, "left", "bottom") for y in (3, 20, 40)]
    LG.Placer(ax).put(f"8x push valid:\n{ok} of {len(s.layers)} layers", spots, gid="status", optional=True,
                      color=C.CAPTION_INK, linespacing=1.1)  # fmt: skip


def draw(kind: str, panels: dict[str, Panel]) -> tuple[C.Frame, list[C.Number]]:
    keys = [m for m in MODELS if m in panels] + ([FULL_EXTRA[0]] if kind == "full" and FULL_EXTRA[0] in panels else [])
    if kind == "main":  # the 122B, the panel with the most lines and the labels, wider
        fr = C.frame("main", title(panels), SUBTITLE, how=HOW, caption=caption(kind, panels, keys), ncols=len(keys),
                     sharey=True, left=0.075, right=0.97, wspace=0.12,
                     width_ratios=[1.5 if k == "122b" else 1 for k in keys])  # fmt: skip
        axes = fr.axes
    else:
        fr = C.frame("full", title(panels), SUBTITLE, how=HOW, caption=caption(kind, panels, keys), nrows=2, ncols=3,
                     sharey=True, left=0.075, right=0.97, wspace=0.12, hspace=0.5)  # fmt: skip
        order = ["27b", "27b first", "9b", "olmo", "122b"]
        axes = []
        for i, ax in enumerate(fr.axes):
            if i < len(order) and order[i] in panels:
                axes.append(ax)
            else:
                fr.fig.delaxes(ax)
        keys = [k for k in order if k in panels]
    PD.head_room(fr, C.LABEL * 1.2 + 6)
    nums: list[C.Number] = []
    for ax, k in zip(axes, keys, strict=True):
        nums += panel(ax, panels[k], faded=kind == "full")
        if ax.get_subplotspec().colspan.start == 0:
            ax.set_ylabel("% switched")
        else:
            ax.tick_params(labelleft=False)
        ax.tick_params(labelbottom=True)
    for ax, k in zip(axes, keys, strict=True):
        valid_note(ax, panels[k])
        direct_labels(ax, panels[k], LABEL_AT.get(k, ()))
    PD.x_label(fr, axes)
    return fr, nums


def build(kind: str, panels: dict[str, Panel], out: Path = C.OUT) -> list[Path]:
    fr, nums = draw(kind, panels)
    return C.save(fr, STEM, nums, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--grid", type=Path, default=None, help="grid folder (default: the newest under results/cross_model)"
    )
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    ap.add_argument("--extra", action="append", default=[], metavar="MODEL=SUMMARY",
                    help="a size-matched patch run's summary.json (batch A; only after Dan opens it)")  # fmt: skip
    a = ap.parse_args(argv)
    b = RB.Book(a.grid or CMF.latest_grid())
    extra = {}
    for spec in a.extra:
        m, path = spec.split("=", 1)
        extra[m] = extra_arms(Path(path))
    panels = load(b, extra)
    for k in [*MODELS, FULL_EXTRA[0]]:
        p = panels[k]
        print(f"{k}: band {band_text(p)} = " + ", ".join(f"{p.depth(la):.0f}%" for la in p.band))
    for kind in [a.only] if a.only else ["main", "full"]:
        for path in build(kind, panels, a.out):
            print(rel(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
