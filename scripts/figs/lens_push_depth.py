"""lens_push_depth: finding 7, "a lens push writes a stated bridge for recall; the lookup does not follow" (Dan's figure
guide, 6g).

The test (early_push_where): the hidden state at the stated bridge's word or sentence is pushed along the lens's
direction toward another animal (v_X - v_I) at a grid of layers and sizes; the rule picks its test point on recalls
alone (the valid cell that switches the most recalls, prompt -> memory) and reads the lookups (prompt -> prompt) there.
One panel per test: the % of answers switched to X's answer by depth (% of the model's layers), recalls (dark grey,
the positive control) and lookups (the accent), each with its Wilson 95% band, at the test point's position and size;
the test point as a thin vertical line.

Numbers: the lookups at the test point are the grid cell's value (common.cell_number); the recalls there and the
random push are the cell's control text (source CONTROL, extra["control"] = readme_build.CONTROLS["f7"]'s name); every
curve point comes from the summary.json the cell names (source = that file), whose test point and rates are checked
against the grid first (a mismatch raises; nothing is patched). The random push of the same size on lookups is drawn
as a light grey line only where it is not 0 at every layer; else the caption says so.

MAIN: per model, the README table's cell (scene set 2's main rule where it has a value, else the main rule, else the
amended rule): only models with a valid test point. FULL: every test point, a cell judged by both rules once.

uv run python scripts/figs/lens_push_depth.py [--grid DIR] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bridge_jspace import pins
from bridge_jspace import plot_style as PS
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import stated_bridge as SB

STEM = "lens_push_depth"
F = "f7"
MAIN_ORDER = ("main rule, draw 2", "main rule", "amended rule")  # the README table's order for finding 7
FULL_SETTINGS = ("main rule", "amended rule", "main rule, draw 2", "amended rule, draw 2")
CONTROL = SB.CONTROL
NUM = SB.NUM
CELL = re.compile(r"cell: (word|sentence), layer (\d+), (\d+(?:\.\d+)?)x")
RECALL = re.compile(rf"recall switched {NUM}% \[{NUM}, {NUM}\]")
RANDOM = re.compile(rf"random push on lookups {NUM}%")
SUBSET = {"word": "w", "sentence": "s"}
MOVED = 5.0  # a lookup point whose Wilson lower bound is above this % is labelled (an exception: the lookup moved)
XLIM, XTICKS, YMAX = (12.0, 82.0), (20, 40, 60), 128.0  # room above 100% for the test point's label

TITLE = "A lens push writes recall, not the lookup"
SUBTITLE = "% of answers switched to the pushed bridge's answer, by depth of the lens push"


@dataclass
class Curve:
    """One test point's curves: family ("lookup" / "recall" / "random") -> one Number per layer."""

    model: str
    settings: list[str]
    word: str
    where: str  # "word" / "sentence"
    layer: int
    scale: float
    n_layers: int
    path: str
    x: list[float] = field(default_factory=list)  # % of depth
    points: dict[str, list[C.Number]] = field(default_factory=dict)
    chosen: dict[str, C.Number] = field(default_factory=dict)  # the grid's numbers at the test point

    @property
    def depth(self) -> float:
        return 100 * self.layer / self.n_layers

    def numbers(self) -> list[C.Number]:
        return [n for ns in self.points.values() for n in ns] + list(self.chosen.values())


def manifest_of(summary: Path) -> dict:
    """The run's manifest: next to summary.json, or one folder up for an analysis-*/summary.json."""
    for d in (summary.parent, summary.parent.parent):
        if (d / "manifest.json").exists():
            return json.loads((d / "manifest.json").read_text())
    raise FileNotFoundError(f"no manifest.json for {summary}")


def collect(b: RB.Book, m: str, setting: str, root: Path = C.REPO) -> Curve | None:
    """The cell's curves at its test point's position and size, or None when the cell has no value."""
    c = SB.cell_of(b, m, setting, f=F)
    look = C.cell_number(b, F, m, setting, "lookups switched at the test point")
    if c is None or look is None:
        return None
    mt, rc, rn = CELL.search(c.control), RECALL.search(c.control), RANDOM.search(c.control)
    if mt is None or rc is None or rn is None:
        raise ValueError(f"{F} {m} {setting}: no test point, recall or random push in the grid's control text")
    where, layer, scale = mt.group(1), int(mt.group(2)), float(mt.group(3))
    path = root / c.path
    s = json.loads(path.read_text())
    p = s["decision"]["primary"]
    if p is None or (p["subset"], int(p["layer"]), float(p["scale"])) != (SUBSET[where], layer, scale):
        raise ValueError(f"{F} {m} {setting}: {c.path}'s test point is not the grid's ({mt.group(0)})")
    n_layers = int(pins.TARGETS[manifest_of(path)["model"]["target"]]["n_layers"])
    cells = {(d["family"], d["subset"], d["layer"], float(d["scale"]), d["dir"]): d for d in s["cells"]}
    sub = SUBSET[where]
    layers = sorted(la for (f, su, la, sc, d) in cells if (f, su, sc, d) == ("BL", sub, scale, "lens"))
    cv = Curve(m, [setting], c.word, where, layer, scale, n_layers, c.path)
    for fam, (family, direction) in (("lookup", ("BL", "lens")), ("recall", ("BR", "lens")),
                                     ("random", ("BL", "random"))):  # fmt: skip
        pts = []
        for la in layers:
            d = cells.get((family, sub, la, scale, direction))
            if d is None:
                continue
            t = d["to_x"]
            pts.append(C.Number(100 * t[0], f"{fam}s switched, {direction} push", F, m, setting, "",
                                (100 * t[1], 100 * t[2]), int(d["n"]), source=c.path,
                                extra={"family": family, "dir": direction, "where": where, "layer": la,
                                       "scale": scale, "depth": 100 * la / n_layers}))  # fmt: skip
        cv.points[fam] = pts
    cv.x = [n.extra["depth"] for n in cv.points["lookup"]]
    at = {fam: next((n for n in pts if n.extra["layer"] == layer), None) for fam, pts in cv.points.items()}
    if at["lookup"] is None or at["recall"] is None or abs(at["lookup"].value - look.value) > 0.05 + 1e-9:
        raise ValueError(f"{F} {m} {setting}: {c.path} disagrees with the grid at the test point")
    if G.r100(at["recall"].value / 100) != float(rc.group(1)) or (
        at["random"] is not None and G.r100(at["random"].value / 100) != float(rn.group(1))
    ):
        raise ValueError(f"{F} {m} {setting}: {c.path} disagrees with the grid's controls at the test point")
    cv.chosen = {
        "lookup": look,
        "recall": SB.control(m, setting, "recall", "recalls switched at the test point", float(rc.group(1)),
                             (float(rc.group(2)), float(rc.group(3))), at["recall"].n, f=F),
        "random": SB.control(m, setting, "random", "lookups switched by a random push at the test point",
                             float(rn.group(1)), f=F),
    }  # fmt: skip
    return cv


def random_is_zero(curves: list[Curve]) -> bool:
    return all(n.value == 0 for cv in curves for n in cv.points.get("random", []))


# ---------------------------------------------------------------- drawing


def crosses(ax, bb) -> bool:
    """A curve of the panel (Line2D gid "curve") passes through the box (each segment sampled in display space)."""
    for ln in ax.get_lines():
        if ln.get_gid() != "curve":
            continue
        xy = ln.get_transform().transform(ln.get_xydata())
        for (x0, y0), (x1, y1) in itertools.pairwise(xy):
            if any(bb.contains(x0 + (x1 - x0) * k / 40, y0 + (y1 - y0) * k / 40) for k in range(41)):
                return True
    return False


def free(ax, t, avoid: list) -> bool:
    """`t` inside its panel, touching no marker or interval of the figure, no curve of its panel, no other text."""
    fig = ax.figure
    r = PS.renderer(fig)
    bb = t.get_window_extent(r).padded(2)
    if not ax.get_window_extent(r).contains(bb.x0, bb.y0) or not ax.get_window_extent(r).contains(bb.x1, bb.y1):
        return False
    if any(bb.overlaps(g) for _, g in PS.graphic_boxes(fig, r)) or crosses(ax, bb):
        return False
    return not any(bb.overlaps(o.get_window_extent(r)) for o in avoid if o is not t)


def label(ax, x: float, y: float, text: str, placed: list, color: str = C.INK, bold: bool = True) -> None:
    """A value label beside its point: the first free place of up-right, down-right, up-left, down-left, left,
    right, then farther above (free: see `free`; none free: the last candidate, and the save's check reports it)."""
    t = None
    for dx, dy, ha, va in ((7, 5, "left", "bottom"), (7, -5, "left", "top"), (-7, 5, "right", "bottom"),
                           (-7, -5, "right", "top"), (-8, 0, "right", "center"), (8, 0, "left", "center"),
                           (-4, 12, "right", "bottom"), (0, 14, "center", "bottom"), (-4, 24, "right", "bottom")):  # fmt: skip
        if t is not None:
            t.remove()
        t = ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=C.NOTE,
                        color=color, fontweight="bold" if bold else "normal", gid="value", zorder=6,
                        path_effects=PS.HALO)  # fmt: skip
        ax.figure.canvas.draw()
        if free(ax, t, placed):
            break
    if t is not None:
        placed.append(t)


def draw_panel(ax, cv: Curve, *, random_line: bool, placed: list) -> None:
    for fam, color in (("recall", C.RECALL), ("lookup", C.LOOKUP)):
        pts = cv.points[fam]
        x = [n.extra["depth"] for n in pts]
        ci = [n.ci or (n.value, n.value) for n in pts]  # every curve point has its Wilson interval (collect)
        ax.fill_between(x, [c[0] for c in ci], [c[1] for c in ci], color=color, alpha=0.13, linewidth=0, zorder=1)
        ax.plot(x, [n.value for n in pts], color=color, linewidth=2.4, zorder=3, gid="curve")
        ax.plot(x, [n.value for n in pts], linestyle="none", marker="o", markersize=5.5, color=color, gid="mark",
                zorder=4)  # fmt: skip
    if random_line and cv.points.get("random"):
        pts = cv.points["random"]
        ax.plot([n.extra["depth"] for n in pts], [n.value for n in pts], color=C.CONTROL, linewidth=1.6, zorder=2)
    ax.axvline(cv.depth, color=C.INK2, linewidth=1.1, zorder=0)
    ax.set_xlim(*XLIM)
    ax.set_xticks(XTICKS, [f"{t}%" for t in XTICKS])
    ax.set_ylim(0, YMAX)
    ax.set_yticks([0, 50, 100], ["0", "50", "100"])
    rec, look = cv.chosen["recall"], cv.chosen["lookup"]  # the values first: they carry the story
    label(ax, cv.depth, rec.value, f"{RD.r0(rec.value)}%", placed, C.RECALL)
    label(ax, cv.depth, look.value, f"{RD.r0(look.value)}%", placed, C.LOOKUP)
    for n in cv.points["lookup"]:  # the exceptions: where the lookup moved
        if n.extra["layer"] != cv.layer and n.ci is not None and n.ci[0] > MOVED:
            label(ax, n.extra["depth"], n.value, f"{RD.r0(n.value)}%", placed, C.LOOKUP)
    t = None  # the line's one label: at its top, on two lines where they fit, else one; else lower down
    for y, sep, dx, ha in ((1, "\n", 6, "left"), (1, "\n", -6, "right"), (1, ": ", 6, "left"), (1, ": ", -6, "right"),
                           (0.6, "\n", 6, "left"), (0.6, "\n", -6, "right")):  # fmt: skip
        tp = f"test point{sep}{cv.where}, {cv.scale:g}x"
        if t is not None:
            t.remove()
        t = ax.annotate(tp, (cv.depth, y), xycoords=("data", "axes fraction"), xytext=(dx, -2),
                        textcoords="offset points", ha=ha, va="top", fontsize=C.NOTE, color=C.INK2, gid="testpoint",
                        linespacing=1.15, multialignment=ha)  # fmt: skip
        ax.figure.canvas.draw()
        if free(ax, t, placed):
            break
    placed.append(t)


def scene_set(setting: str) -> str:
    return "scene set 2" if "draw 2" in setting else "scene set 1"


def rules(settings: list[str]) -> str:
    kinds = {s.split(" rule")[0] for s in settings}
    return "both rules" if kinds == {"main", "amended"} else f"{kinds.pop()} rule"


def notes(b: RB.Book, shown: dict[str, str]) -> tuple[list[str], list[str]]:
    """(exceptions: a judged setting that did not hold, with its numbers; models / settings without a valid cell)."""
    exc, invalid = [], []
    for mm in C.MODELS:
        cs = {c.setting: c for c in b.of(F, mm.key) if c.part == ""}
        for s in FULL_SETTINGS:
            c = cs.get(s)
            if c is None or c.word not in ("fails", "inconclusive") or c.value is None:
                continue
            mt = CELL.search(c.control)
            where = f" at layer {mt.group(2)}" if mt else ""
            exc.append(f"{mm.short} {scene_set(s).replace('scene ', '')}, {s.split(',')[0]}: {RD.r0(c.value)}% of "
                       f"lookups move{where} ({SB.SHOWN_WORD[c.word]})")  # fmt: skip
        bad = sorted({scene_set(s).replace("scene ", "") for s, c in cs.items()
                      if s in FULL_SETTINGS and c.word == "not interpretable"})  # fmt: skip
        if bad:
            invalid.append(f"{mm.short} {', '.join(bad)}" if mm.key in shown else mm.short)
    return exc, invalid


def caption(b: RB.Book, curves: list[Curve], shown: dict[str, str], rule: bool) -> str:
    exc, invalid = notes(b, shown)
    rnd = "Random push: 0% at every layer." if random_is_zero(curves) else ""
    if rule:  # early_push_where's rule v2 and its amendment v2.1 (v21_min_layer: 31% of the depth on every model)
        first = ("Rule: test point = the valid cell moving most recalls (≥ 30%); holds if lookups ≤ 10%; amended: "
                 "from 31% depth.")  # fmt: skip
        second = ["Random push: 0%." if rnd else ""]
    else:
        first, second = " ".join([f"Exception: {'; '.join(exc)}." if exc else "", rnd]).strip(), []
    if invalid:
        second.append(f"No valid test point: {', '.join(invalid)}.")
    second.append(SB.untested(b, f=F))
    return first + "\n" + " ".join(x for x in second if x)


def how(curves: list[Curve], random_line: bool) -> str:
    ns = sorted({n.n for cv in curves for n in cv.points["lookup"] if n.n is not None})
    n = f"{ns[0]}-{ns[-1]}" if len(ns) > 1 else str(ns[0])
    extra = ", light grey = random push" if random_line else ""
    return f"purple = lookups, grey = recalls (the control){extra}; bands: 95% CI, n = {n}"


def figure_main(b: RB.Book, root: Path = C.REPO) -> tuple[C.Frame, list[C.Number]]:
    curves: list[Curve] = []
    for mm in C.MODELS:
        for s in MAIN_ORDER:
            cv = collect(b, mm.key, s, root)
            if cv is not None:
                curves.append(cv)
                break
    if not curves:
        raise ValueError("finding 7: no valid test point to draw")
    if len(curves) > 4:
        raise ValueError("finding 7: more than 4 models with a test point; MAIN has at most 4 panels")
    random_line = not random_is_zero(curves)
    fr = C.frame("main", TITLE, SUBTITLE, how=how(curves, random_line),
                 caption=caption(b, curves, {cv.model: cv.settings[0] for cv in curves}, rule=False), nrows=1,
                 ncols=len(curves), left=0.075, wspace=0.1, sharex=True, sharey=True)  # fmt: skip
    SB.shift(fr, top=48)
    placed: list = []
    numbers: list[C.Number] = []
    for i, (ax, cv) in enumerate(zip(fr.axes, curves, strict=True)):
        head2(ax, C.MODEL[cv.model].name, f"{scene_set(cv.settings[0])} · {SB.SHOWN_WORD.get(cv.word, cv.word)}")
        draw_panel(ax, cv, random_line=random_line, placed=placed)
        numbers += cv.numbers()
        if i:
            ax.tick_params(axis="y", labelleft=False)
    fr.axes[0].set_ylabel("% switched")
    xlabel(fr, fr.axes)
    return fr, numbers


def head2(ax, name: str, detail: str) -> None:
    """A panel's two-line heading: the model (16 pt) over a small grey line (scene set, rule, verdict)."""
    ax.annotate(name, (0, 1), xycoords="axes fraction", xytext=(0, 28), textcoords="offset points", ha="left",
                va="bottom", fontsize=C.LABEL, color=C.INK)  # fmt: skip
    ax.annotate(detail, (0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points", ha="left",
                va="bottom", fontsize=C.NOTE, color=C.CAPTION_INK)  # fmt: skip


def xlabel(fr: C.Frame, row: list) -> None:
    """One x label under a row of panels (their tick labels drawn), centered on the row."""
    a, z = row[0].get_position(), row[-1].get_position()
    y = a.y0 - (C.TICK * 1.6 + 6) / 72 / fr.fig.get_figheight()
    fr.fig.text((a.x0 + z.x1) / 2, y, "depth of the push (% of the model's layers)", ha="center", va="top",
                fontsize=C.LABEL, color=C.INK, gid="xlabel")  # fmt: skip


def figure_full(b: RB.Book, root: Path = C.REPO) -> tuple[C.Frame, list[C.Number]]:
    curves: list[Curve] = []
    for mm in C.MODELS:
        for s in FULL_SETTINGS:
            cv = collect(b, mm.key, s, root)
            if cv is None:
                continue
            same = next((o for o in curves if o.model == cv.model and RD.run_key(o.path) == RD.run_key(cv.path)
                         and (o.where, o.layer, o.scale) == (cv.where, cv.layer, cv.scale)), None)  # fmt: skip
            if same is not None and same.word == cv.word:  # both rules chose the same test point: one panel
                same.settings.append(s)
                continue
            curves.append(cv)
    if not curves:
        raise ValueError("finding 7: no valid test point to draw")
    random_line = not random_is_zero(curves)
    ncols = 3
    nrows = (len(curves) + ncols - 1) // ncols
    fr = C.frame("full", TITLE, SUBTITLE, how=how(curves, random_line),
                 caption=caption(b, curves, {cv.model: cv.settings[0] for cv in curves}, rule=True), nrows=nrows,
                 ncols=ncols, size=(12.0, 3.4 + 3.6 * nrows), left=0.075, wspace=0.1, hspace=0.75, sharex=True,
                 sharey=True)  # fmt: skip
    SB.shift(fr, top=48)
    placed: list = []
    numbers: list[C.Number] = []
    for i, ax in enumerate(fr.axes):
        if i >= len(curves):
            ax.remove()
            continue
        cv = curves[i]
        head2(ax, C.MODEL[cv.model].name, f"{scene_set(cv.settings[0])}, {rules(cv.settings)} · "
                                          f"{SB.SHOWN_WORD.get(cv.word, cv.word)}")  # fmt: skip
        draw_panel(ax, cv, random_line=random_line, placed=placed)
        numbers += cv.numbers()
        if i % ncols:
            ax.tick_params(axis="y", labelleft=False)
        else:
            ax.set_ylabel("% switched")
        ax.tick_params(axis="x", labelbottom=True)
    for r in range(nrows):  # one x label under each row of panels
        xlabel(fr, [ax for ax in fr.axes[r * ncols : (r + 1) * ncols] if ax in fr.fig.axes])
    return fr, numbers


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--grid", type=Path, default=None, help="results/cross_model/<stamp> (default: the newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    b = C.book(a.grid or SB.newest_grid())
    for kind, make in (("main", figure_main), ("full", figure_full)):
        if a.only in (None, kind):
            fr, numbers = make(b)
            for p in C.save(fr, STEM, numbers, a.out):
                print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
