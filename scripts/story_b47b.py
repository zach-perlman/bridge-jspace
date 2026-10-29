"""Batch 47's README figures, set B (Dan, 28 Oct): one figure per test, each read from that test's verdict folder, in
story_style's look. Sealed tests (D1 + D2, 47.4, 47.6 (b), 47.7) take their title as a parameter, or build it from the
verdict's own label and numbers so it reads true for any outcome; 47.0 is descriptive and already open. Every plotted
number goes through story_style.record with the verdict file as its source.

    test   script                     verdict file (results/...)               default figure
    D1     scripts/x47_depthmap.py    x47_depthmap/depth-*/depth.json          fig16_depth_map (D2's window row in it)
    47.4   scripts/x47_cumulative.py  x47_cumulative/x47_4-*/x47_4.json        fig17_cumulative
    47.6   scripts/x47_edges.py       x47_edges/x47_6-*/verdict.json           fig18_formation
    47.7   scripts/x47_value.py       x47_value/x47_7{a,c,b}-*/x47_7{a,c,b}.json  fig19_value
    47.0   scripts/x47_verbal.py      x47_verbal/summary-*/verbal.json         fig20_verbal

    from scripts import story_b47b as B
    B.build_d1(Path("results/x47_depthmap/depth-<UTC>"), "fig16_depth_map")   # into figures/story/ (out_dir= to change)
"""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.colors import Colormap, LinearSegmentedColormap
from matplotlib.legend_handler import HandlerTuple
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory

from scripts import story_style as S

PLANTED = "PLANTED data, not results. "
WRAP = 104  # subtitle characters per line at 11 pt across the 8.8 in column
LINE = 0.19  # inches per subtitle or legend line
TARGETS = tuple((t, m, name) for t, m, name in S.MODELS if m != "122b")  # batch 47 ran on the 9B, the 27B and Muse
NAME = {t: name for t, _, name in S.MODELS}
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse", "nemotron-3.5-lightning": "Lightning"}
# batch 52's fourth model (readme_story_figures.LT), drawn hollow: its gate was chosen after its pre-check was seen
LT_ROW = ("nemotron-3.5-lightning", "lightning", "Nemotron 3.5 Lightning")
NAME[LT_ROW[0]] = LT_ROW[2]
LT_NOTE = "Hollow: Lightning's gate chosen after the 60-scene pre-check was seen."
ROUTE_COL = {"position": S.COL["position"], "identity": S.COL["identity"], "value": S.COL["value"],
             "original": S.COL["original"], "other": S.COL["other"]}  # fmt: skip
ROUTE_TEXT = {"position": "position", "identity": "identity", "value": "value", "original": "original answer",
              "other": "other"}  # fmt: skip
BAR = "#111111"  # a rule's bar: thin, dashed, labelled


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO)) if path.is_relative_to(S.REPO) else str(path)


def header(fig, title: str, text: str, planted: bool) -> float:
    """The claim as the title, the subtitle wrapped to the column (PLANTED first on planted data); returns the figure
    fraction just under the subtitle."""
    body = textwrap.fill((PLANTED if planted else "") + text, WRAP)
    S.title(fig, title, body, limit=86)
    return 1 - (0.42 + LINE * (body.count("\n") + 1) + 0.12) / fig.get_figheight()


def place(fig, y: float, legend_rows: int, title_lines: int = 1, **adjust) -> None:
    """The axes under the header, a legend of legend_rows rows and panel titles of title_lines lines."""
    room = 1.35 * LINE * legend_rows + 0.22 + 0.2 * title_lines
    fig.subplots_adjust(top=y - room / fig.get_figheight(), **adjust)


def legend(fig, handles, labels, y: float, ncol: int | None = None, **kw) -> None:
    """One legend under the subtitle (readme_story_figures.legend's placement)."""
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.0, y + 0.01), frameon=False, handletextpad=0.4,
               ncol=ncol or min(len(labels), 3), columnspacing=1.2, handlelength=1.4, borderaxespad=0.2, **kw)  # fmt: skip


def save(fig, name: str, out_dir: Path | None) -> str:
    """story_style.save into out_dir (default figures/story/); returns the name."""
    out = out_dir or S.OUT
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", facecolor="white")
    fig.savefig(out / f"{name}.png", dpi=200, facecolor="white")
    S.plt.close(fig)
    return name


def rule_bar(ax, x: float, label: str, y: float) -> None:
    ax.axvline(x, color=BAR, lw=0.8, ls=(0, (3, 2)), zorder=1)
    ax.text(x, y, f" {label}", fontsize=S.FONT - 1, va="bottom", color=BAR)


def pct(v) -> tuple[float, float, float]:
    return (100 * v[0], 100 * v[1], 100 * v[2])


def finite(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


# ---- D1 + D2: the token x layer map ----------------------------------------------------------------------------------

D1_ROWS = {"bridge": "bridge word", "pick_rest": "rest of the pick sentence", "person": "asked person",
           "lk_org_item": "old item's locker: item", "lk_org_num": "old item's locker: number",
           "lk_cf_item": "new item's locker: item", "lk_cf_num": "new item's locker: number",
           "lk_other1_item": "other locker: item", "lk_other1_num": "other locker: number",
           "lk_other2_item": "third locker: item", "lk_other2_num": "third locker: number",
           "question": "question", "last": "last token"}  # fmt: skip
D1_MARGINS = (("b", "bridge word, every layer ≤ l"), ("w", "bridge word, every layer ≥ l"))
DESIGN_TEXT = {"clean": "clean one-pick scenes", "main": "main test (two people swap picks)"}
ORDER_TEXT = {"locker-first": "locker before the pick", "locker-after": "locker after the pick", "all": "all scenes"}
HOT, W_FLOOR = 0.3, 0.1  # x47_depthmap.HOT, W_FLOOR (the rules' bars)


def reader_cmap(reader: str) -> Colormap:
    return LinearSegmentedColormap.from_list(reader, ["#ffffff", S.COL[reader]]).with_extremes(bad="#f4f4f4")


def d1_title(m: dict, design: str, group: str) -> str:
    """The claim from the verdict's rule on the drawn order group (locker before the pick: D1 (b), the last layer at
    which each reader's bridge-word cell switches >= 30%; locker after: D1 (a))."""
    r = m["rules"][design]
    if group == "locker-after":
        a = r["a"]
        if a.get("holds"):
            return "Locker after the pick: the lookup reads the lockers, not the bridge word"
        return (
            f"Locker after the pick: the bridge word switches up to {100 * (a.get('bridge_max') or 0):.0f}% of lookups"
        )
    b = r["b"]
    at = lambda x: f"layer {x}" if x is not None else "no layer"  # noqa: E731
    return f"The lookup reads the bridge word to {at(b.get('lookup_last'))}, the recall to {at(b.get('recall_last'))}"


def d1_map(ax, cells: dict, layers: list[int], groups: list[str], reader: str, layer: int) -> list[tuple]:
    """One reader's map (rows: token groups, then the two margins; columns: the input token, then the layers; L's
    column ticked 'L'); returns the (arm, value) of every drawn cell."""
    cols = ["emb", *layers]
    rows = [*groups, *(k for k, _ in D1_MARGINS)]
    grid = np.full((len(rows), len(cols)), np.nan)
    drawn = []
    for i, g in enumerate(rows):
        for j, la in enumerate(cols):
            arm = f"g{g}@{la}" if i < len(groups) else (f"{g}{la}" if la != "emb" else None)
            if arm and arm in cells:
                grid[i, j] = cells[arm][0]
                drawn.append((arm, cells[arm]))
    ax.imshow(np.ma.masked_invalid(grid), cmap=reader_cmap(reader), vmin=0, vmax=1, aspect="auto",
              interpolation="nearest")  # fmt: skip
    ax.axhline(len(groups) - 0.5, color="white", lw=4)
    ax.axvline(0.5, color="white", lw=3)
    step = 8 if max(layers) < 40 else 12
    jl = cols.index(layer) if layer in layers else None
    ticks = [(0, "in")] + [(j, str(la)) for j, la in enumerate(cols) if j and la % step == 0  # type: ignore[operator]
                           and (jl is None or abs(j - jl) > 1)]  # fmt: skip
    if jl is not None:
        ticks.append((jl, "L"))
    ax.set_xticks([j for j, _ in ticks], [t for _, t in ticks])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    return drawn


def outline(ax, row: int, col: int) -> None:
    ax.add_patch(Rectangle((col - 0.5, row - 0.5), 1, 1, fill=False, ec="#111111", lw=1.8, zorder=4))


def colour_scale(fig, x: float, reader: str) -> None:
    """A small 0-100% scale for one reader's map, at the bottom left of its panel."""
    cax = fig.add_axes((x, 0.022, 0.13, 0.018))
    cax.imshow(np.linspace(0, 1, 50)[None, :], cmap=reader_cmap(reader), aspect="auto")
    cax.set_axis_off()
    cax.text(-2, 0, "0", ha="right", va="center", fontsize=S.FONT - 1)
    cax.text(51, 0, f"100% {reader}s switched", ha="left", va="center", fontsize=S.FONT - 1)


def build_d1(verdict_dir: Path, out_name: str = "fig16_depth_map", title: str | None = None, *,
             target: str = "qwen3.5-9b", design: str = "clean", group: str = "locker-first",
             out_dir: Path | None = None, planted: bool = False) -> str:  # fmt: skip
    """D1 + D2 (x47_depthmap's depth.json) on one model, design and order group: the lookup's map and the recall's,
    side by side, token group x layer (the cell: answers switched when that group alone takes the changed prompt's
    state at that layer), D1's margins below (the bridge word at every layer <= l; D2's window, at every layer >= l).
    Outlined: per reader the last layer whose bridge-word cell switches >= 30% (D1 (b)) and D2's l_R (the first layer
    from which the window switches <= 10%)."""
    path = verdict_dir / "depth.json"
    blob = json.loads(path.read_text())
    m = next(x for x in blob["models"] if x["target"] == target)
    src = rel(path)
    plt = S.setup()
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 7.4), sharey=True)
    if m["status"] != "tested":
        y = header(fig, title or f"{NAME[target]}: not run", "D1 has no run on this model.", planted)
        place(fig, y, 0, left=0.27, right=0.99, bottom=0.14, wspace=0.06)
        for ax in axes:
            S.empty(ax, "not run")
        return save(fig, out_name, out_dir)
    per = m["cells"][design][group]
    layers = m["layers"]
    readers = [w for w in ("lookup", "recall") if w in per]
    have = set().union(*(per[w]["cells"] for w in readers))
    groups = [g for g in D1_ROWS if any(a.startswith(f"g{g}@") for a in have)]
    n = " / ".join(str(per[w]["n"]) if w in per else "0" for w in ("lookup", "recall"))
    whole = " / ".join(f"{100 * per[w]['cells']['d'][0]:.0f}%" if "d" in per.get(w, {}).get("cells", {}) else "–"
                       for w in ("lookup", "recall"))  # fmt: skip
    y = header(fig, title or d1_title(m, design, group),
               f"{NAME[target]}, {DESIGN_TEXT[design]}, {ORDER_TEXT[group]}; n = {n} (lookup / recall). A cell: "
               "answers switched when one token group takes the changed prompt's state at one layer ('in': the input "
               f"token only). Outlined: the bridge word's last layer at ≥ {100 * HOT:.0f}%, and the first layer from "
               f"which it is no longer read (every layer ≥ l switches ≤ {100 * W_FLOOR:.0f}%). The whole pick sentence "
               f"at every layer switches {whole}. Fixed in advance.", planted)  # fmt: skip
    place(fig, y, 0, left=0.27, right=0.99, bottom=0.14, wspace=0.06)
    cols = ["emb", *layers]
    for ax, w in zip(axes, ("lookup", "recall"), strict=True):
        ax.set_title(w, fontsize=S.FONT + 1, color=S.COL[w], weight="bold")
        if w not in per:
            S.empty(ax, "no items")
            continue
        c = per[w]["cells"]
        for arm, v in d1_map(ax, c, layers, groups, w, m["layer"]):
            S.record(out_name, target, f"D1 {design}, {group}, {w}: {arm} switched", *v[:3], n=per[w]["n"], source=src)
        hot = [la for la in layers if f"gbridge@{la}" in c and c[f"gbridge@{la}"][0] >= HOT - 1e-9]
        if hot and "bridge" in groups:
            outline(ax, groups.index("bridge"), cols.index(max(hot)))
        if per[w].get("l_R") is not None:
            outline(ax, len(groups) + 1, cols.index(per[w]["l_R"]))
        S.record(out_name, target, f"D1 {design}, {group}, {w}: last layer with the bridge word >= 0.3",
                 max(hot) if hot else None, source=src)  # fmt: skip
        S.record(out_name, target, f"D2 {design}, {group}, {w}: l_R", per[w].get("l_R"), source=src)
        if "d" in c:
            S.record(out_name, target, f"D1 {design}, {group}, {w}: d switched", *c["d"][:3], n=per[w]["n"], source=src)
    axes[0].set_yticks(range(len(groups) + 2), [D1_ROWS[g] for g in groups] + [t for _, t in D1_MARGINS])
    fig.supxlabel("layer at which the changed prompt's state is placed", x=0.63, y=0.055, fontsize=S.FONT)
    for ax, w in zip(axes, ("lookup", "recall"), strict=True):
        colour_scale(fig, ax.get_position().x0 + 0.01, w)
    return save(fig, out_name, out_dir)


E11_GROUPS = (("locker-first", "Locker before the pick"), ("locker-after", "Locker after the pick"))
E11_PITCH = 2.35  # rows per token group: the lookup's row, the recall's, a gap
# v6 iteration 2 (Dan, 28 Oct ~15:40): the rows in words; the eight locker-sentence rows under one bracket, "each
# locker sentence: item / number", each with its sentence and token
E11_ROWS = {"bridge": "the bridge word", "pick_rest": "the rest of the pick sentence", "person": "the asked person",
            "lk_org_item": "old item's · item", "lk_org_num": "old item's · number",
            "lk_cf_item": "new item's · item", "lk_cf_num": "new item's · number",
            "lk_other1_item": "other · item", "lk_other1_num": "other · number",
            "lk_other2_item": "third · item", "lk_other2_num": "third · number",
            "question": "the question", "last": "the last token"}  # fmt: skip
# Dan's round 3 (28 Oct 21:10): the two margin rows in plain words
E11_MARGINS = {"b": "bridge word replaced at\nevery layer up to l\n(the whole word changed)",
               "w": "replaced from l on\n(what later layers\nstill take from it)"}  # fmt: skip
E11_MARGIN_GAP = (1.4, 3.8)  # extra room above the first margin row and between the two (three-line labels)


def e11_scale(fig, x: float, y: float, reader: str, text: str) -> None:
    """A 0-100% colour scale drawn as figure patches (no extra axes: a v6 figure has at most two panels)."""
    cmap, w, hh, k = reader_cmap(reader), 0.13, 0.016, 40
    for i in range(k):
        fig.add_artist(Rectangle((x + w * i / k, y), w / k + 0.0005, hh, transform=fig.transFigure, lw=0,
                                 color=cmap((i + 0.5) / k)))  # fmt: skip
    fig.text(x - 0.006, y + hh / 2, "0", ha="right", va="center", fontsize=S.FONT - 1)
    fig.text(x + w + 0.006, y + hh / 2, f"1  {text}", ha="left", va="center", fontsize=S.FONT - 1)


def build_e11(verdict_dir: Path, out_name: str = "fig03d_depth_map", title: str | None = None, *,
              target: str = "qwen3.5-9b", design: str = "clean", out_dir: Path | None = None,
              coverage: dict | None = None, one_model: bool = False) -> str:  # fmt: skip
    """E11 (v6): D1 + D2 (x47_depthmap's depth.json) on one model and design, one panel per sentence order (locker
    before the pick; after it). Rows: each token group as a pair, the lookup's row (purple) over the recall's (grey);
    then D1's margins (the bridge word at every layer <= l; D2's window, every layer >= l), labelled in plain words
    (Dan's round 3, 28 Oct 21:10). A cell: answers switched when that group alone takes the changed prompt's state at
    that layer. Outlined per reader: the last layer whose bridge-word cell switches >= 30% (D1 (b)) and D2's l_R (the
    first layer from which the window switches <= 10%). Locker before the pick: a dashed line after the lookup's last
    such layer (L16 on the 9B), 'the lookup reads the bridge word up to' it. The subtitle says what the map shows (Dan's
    line); the model, the scenes and the cell go to the caption. By default the four-model version (e11_four; Dan's
    figures brief, 29 Oct 10:00): the 9B and Muse from verdict_dir, the others from coverage ({target: (depth.json,
    design)}, default E11_COVERAGE); one_model: the single-model map above."""
    if not one_model:
        return e11_four(verdict_dir, out_name, title, E11_COVERAGE if coverage is None else coverage, out_dir)
    path = verdict_dir / "depth.json"
    blob = json.loads(path.read_text())
    m = next(x for x in blob["models"] if x["target"] == target and x["status"] == "tested")
    src = rel(path)
    layers = m["layers"]
    cols = ["emb", *layers]
    xs = [0.0] + [j + 0.35 for j in range(1, len(cols))]  # a gap after the input token's column
    plt = S.setup()
    top_in, body_in, bottom_in = 1.45, 6.25, 1.55
    h = top_in + body_in + bottom_in
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.32, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.05)
    # Dan (21:55): which model and scenes in the subtitle, the outline in the one caption line
    S.title(fig, title or "Locker after the pick: the lookup leaves the bridge word early",
            f"{NAME[target]}, {DESIGN_TEXT[design]}: the whole changed state placed in one token group at one layer")  # fmt: skip
    per_all = m["cells"][design]
    have = set().union(*(per_all[g][w]["cells"] for g, _ in E11_GROUPS for w in ("lookup", "recall")))
    groups = [g for g in D1_ROWS if any(a.startswith(f"g{g}@") for a in have)]
    rows = [*groups, *(k for k, _ in D1_MARGINS)]
    y_of = {g: -i * E11_PITCH for i, g in enumerate(groups)}
    y_of["b"] = y_of[groups[-1]] - E11_PITCH - E11_MARGIN_GAP[0]
    y_of["w"] = y_of["b"] - E11_PITCH - E11_MARGIN_GAP[1]
    for ax, (group, label) in zip(axes, E11_GROUPS, strict=True):
        per = per_all[group]
        for dy, w in ((0.0, "lookup"), (-1.0, "recall")):
            c = per[w]["cells"]
            cmap = reader_cmap(w)
            for g in rows:
                arms = [f"g{g}@{la}" if g in groups else (f"{g}{la}" if la != "emb" else None) for la in cols]
                y0 = y_of[g] + dy
                for x, arm in zip(xs, arms, strict=True):
                    v = c.get(arm) if arm else None
                    if v is not None:  # a cell not measured stays blank
                        ax.add_patch(Rectangle((x - 0.5, y0 - 0.5), 1, 1, lw=0, color=cmap(v[0])))
                        S.record(out_name, target, f"D1 {design}, {group}, {w}: {arm} switched", *v[:3], n=per[w]["n"],
                                 source=src)  # fmt: skip
            hot = [la for la in layers if f"gbridge@{la}" in c and c[f"gbridge@{la}"][0] >= HOT - 1e-9]
            if hot and "bridge" in groups:
                x = xs[cols.index(max(hot))]
                ax.add_patch(Rectangle((x - 0.5, y_of["bridge"] + dy - 0.5), 1, 1, fill=False, ec="#111111", lw=1.6,
                                       zorder=4))  # fmt: skip
                if w == "lookup" and group == "locker-first":  # Dan's round 3: the layer marked, in words
                    ax.axvline(x + 0.5, color="#111111", lw=1.1, ls=(0, (4, 3)), zorder=5)
                    ax.text(x + 1.0, y_of[groups[1]] + 0.4, f"the lookup reads\nthe bridge word\nup to L{max(hot)}",
                            ha="left", va="top", fontsize=S.FONT - 1, color="#111111", zorder=6, linespacing=1.15)  # fmt: skip
            if per[w].get("l_R") is not None:
                x = xs[cols.index(per[w]["l_R"])]
                ax.add_patch(Rectangle((x - 0.5, y_of["w"] + dy - 0.5), 1, 1, fill=False, ec="#111111", lw=1.6,
                                       zorder=4))  # fmt: skip
            S.record(out_name, target, f"D1 {design}, {group}, {w}: last layer with the bridge word >= 0.3",
                     max(hot) if hot else None, source=src)  # fmt: skip
            S.record(out_name, target, f"D2 {design}, {group}, {w}: l_R", per[w].get("l_R"), source=src)
            if "d" in c:
                S.record(out_name, target, f"D1 {design}, {group}, {w}: d switched", *c["d"][:3], n=per[w]["n"],
                         source=src)  # fmt: skip
        ax.set_title(label, fontsize=12, weight="bold", loc="left", pad=24)
        S.panel_tag(ax, f"{per['lookup']['n']}, {per['recall']['n']}", "fixed")
        jl = cols.index(m["layer"]) if m["layer"] in layers else None
        step = 8 if max(layers) < 40 else 12
        ticks = [(0, "in")] + [(j, str(la)) for j, la in enumerate(cols) if j and la % step == 0  # type: ignore[operator]
                               and (jl is None or abs(j - jl) > 1)]  # fmt: skip
        if jl is not None:
            ticks.append((jl, "L"))
        ax.set_xticks([xs[j] for j, _ in ticks], [t for _, t in ticks])
        ax.set_xlim(-0.6, xs[-1] + 0.6)
        ax.set_ylim(y_of[rows[-1]] - 1.7, 0.7)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].set_yticks(
        [y_of[g] - 0.5 for g in rows], [E11_ROWS[g] for g in groups] + [E11_MARGINS[k] for k, _ in D1_MARGINS]
    )
    lockers = [g for g in groups if g.startswith("lk_")]
    if lockers:  # the locker-sentence rows under one bracket, its label left of their tick labels
        tr = blended_transform_factory(fig.transFigure, axes[0].transData)
        top, bot = y_of[lockers[0]] + 0.3, y_of[lockers[-1]] - 1.3
        x = 0.13
        axes[0].plot([x + 0.006, x, x, x + 0.006], [top, top, bot, bot], transform=tr, color="#888888", lw=1,
                     clip_on=False)  # fmt: skip
        axes[0].text(x - 0.008, (top + bot) / 2, "each locker sentence: item / number", transform=tr, ha="right",
                     va="center", fontsize=S.FONT, rotation=90)  # fmt: skip
    fig.supxlabel("layer at which the changed prompt's state is placed", x=0.64, y=0.98 / h, fontsize=S.FONT)
    e11_scale(fig, 0.06, 0.6 / h, "lookup", "lookups switched (upper row)")
    e11_scale(fig, 0.55, 0.6 / h, "recall", "recalls switched (lower row)")
    fig.text(0.01, 0.1 / h, f"Outlined, per reader: the bridge word's last layer at ≥ {HOT:.1f}; the first layer from "
             f"which it switches ≤ {W_FLOOR:.1f}.", fontsize=S.FONT - 1, color=S.COL["muted"])  # fmt: skip
    return save(fig, out_name, out_dir)


# Dan's figures brief (29 Oct 10:00): every per-model figure has four slots (9B, 27B, Muse, Lightning). E11's map on all
# four, each in a compact block: the 27B's and Lightning's depth maps are batch 52 coverage folders, read by explicit
# path (the newest depth-* folder holds the 9B and Muse only); Lightning has the main test only (no clean one-pick run
# passed its gate), hollow
E11_COVERAGE = {
    "qwen3.6-27b": (S.REPO / "results" / "x47_depthmap" / "x52_depthmap-20261029T010426Z" / "depth.json", "clean"),
    "nemotron-3.5-lightning": (S.REPO / "results" / "x47_depthmap" / "x52_depthmap-20261029T011452Z" / "depth.json",
                               "main"),
}  # fmt: skip
E11_FOUR_ROWS = (("bridge", "the bridge word"), ("locker", "a locker sentence (its best cell)"),
                 ("question", "the question"), ("last", "the last token"),
                 ("b", "bridge word, every layer up to l"), ("w", "bridge word, from l on"))  # fmt: skip
E11_FOUR_PITCH, E11_BLOCK_GAP = 2.15, 3.7  # rows per group (lookup, recall, gap); room between two models' blocks
E11_COLS = 16.0  # each model's columns (input token, then its sampled layers) spread over the same width


def e11_four(verdict_dir: Path, out_name: str, title: str | None, coverage: dict, out_dir: Path | None) -> str:
    """E11 on four models (Dan's figures brief, 29 Oct 10:00): one panel per sentence order, one block per model (9B,
    27B, Muse: clean one-pick scenes; Lightning: the main test, hollow). Per block: the bridge word, a locker sentence
    (at each layer the best of its eight token groups: whether one locker cell carries the lookup), the question, the
    last token, and D1's two margins; each a pair of rows, lookup over recall. Columns: the input token, then the
    model's sampled layers, spread over one width; L ticked per block. Outlined per reader: the bridge word's last layer
    at >= 30% (D1 (b)) and D2's l_R. Every cell of the drawn design is recorded, the locker rows' maxima beside them."""
    base = verdict_dir / "depth.json"
    blob = json.loads(base.read_text())
    slots = []
    for t, m, name in (*TARGETS, LT_ROW):
        path, design = coverage.get(t, (base, "clean"))
        mod = next((x for x in json.loads(path.read_text())["models"] if x["target"] == t), None)
        if mod is None and path == base:
            mod = next((x for x in blob["models"] if x["target"] == t), None)
        ok = mod is not None and mod["status"] == "tested" and bool(mod["cells"].get(design, {}).get("locker-first"))
        slots.append((t, m, name, mod if ok else None, design, rel(path)))
    plt = S.setup()
    n_rows = len(E11_FOUR_ROWS)
    block = n_rows * E11_FOUR_PITCH
    top_in, body_in, bottom_in = 1.2, 0.125 * (len(slots) * (block + E11_BLOCK_GAP)), 1.75
    h = top_in + body_in + bottom_in
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.3, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.05)
    S.title(fig, title or "Locker after the pick: the lookup leaves the bridge word early",
            "The whole changed state placed in one token group at one layer, on each model")  # fmt: skip
    ticks, labels, status = [], [], []
    for k, (t, _m, name, mod, design, src) in enumerate(slots):
        y0 = -k * (block + E11_BLOCK_GAP)
        y_of = {g: y0 - i * E11_FOUR_PITCH for i, (g, _) in enumerate(E11_FOUR_ROWS)}
        hollow = t == LT_ROW[0]
        ticks += [y_of[g] - 0.5 for g, _ in E11_FOUR_ROWS]
        labels += [lab for _, lab in E11_FOUR_ROWS]
        what = f"{SHORT[t]}, {DESIGN_TEXT[design]}" if mod else SHORT[t]
        mark = f"  {S.STATUS_GLYPH['after']}" if hollow else ""
        short = {"clean": "clean one-pick scenes", "main": "main test"}[design]
        axes[0].text(-0.9, y0 + 1.15, (f"{SHORT[t]} · {short}" if mod else name) + mark, ha="left",
                     va="bottom", fontsize=S.FONT, weight="bold", clip_on=False, zorder=6)  # fmt: skip
        if mod is None:
            why = "not tested: gate" if hollow else "not run"
            for ax in axes:
                ax.text(E11_COLS / 2, y0 - block / 2 + 1, why, ha="center", va="center", color=S.COL["muted"])
            status.append(f"{SHORT[t]}: {why}")
            continue
        status.append(f"{what}" + (", hollow" if hollow else ""))
        layers = mod["layers"]
        cols = ["emb", *layers]
        xs = [0.0] + [0.6 + (E11_COLS - 0.6) * (j - 1) / max(1, len(cols) - 2) for j in range(1, len(cols))]
        wcell = (E11_COLS - 0.6) / max(1, len(cols) - 2)
        for ax, (group, _) in zip(axes, E11_GROUPS, strict=True):
            per = mod["cells"][design][group]
            for dy, w in ((0.0, "lookup"), (-1.0, "recall")):
                if w not in per:
                    continue
                c, n = per[w]["cells"], per[w]["n"]
                cmap = reader_cmap(w)
                for arm, v in c.items():  # every cell of this design, as the one-model figure recorded them
                    S.record(out_name, t, f"D1 {design}, {group}, {w}: {arm} switched", *v[:3], n=n, source=src)
                lk = [g for g in D1_ROWS if g.startswith("lk_") and any(a.startswith(f"g{g}@") for a in c)]
                for g, _ in E11_FOUR_ROWS:
                    for x, la in zip(xs, cols, strict=True):
                        if g == "locker":
                            vals = [c[f"g{x_}@{la}"] for x_ in lk if f"g{x_}@{la}" in c]
                            v = max(vals, key=lambda u: u[0]) if vals else None
                            if v is not None:
                                S.record(out_name, t, f"D1 {design}, {group}, {w}: the best locker-sentence cell at "
                                         f"layer {la} (max over the locker groups)", *v[:3], n=n, source=src)  # fmt: skip
                        else:
                            arm = f"g{g}@{la}" if g in ("bridge", "question", "last") else (
                                f"{g}{la}" if la != "emb" else None)  # fmt: skip
                            v = c.get(arm) if arm else None
                        if v is None:
                            continue
                        yy = y_of[g] + dy
                        ax.add_patch(Rectangle((x - wcell / 2, yy - 0.5), wcell, 1, lw=0, color=cmap(v[0])))
                hot = [la for la in layers if f"gbridge@{la}" in c and c[f"gbridge@{la}"][0] >= HOT - 1e-9]
                if hot:
                    x = xs[cols.index(max(hot))]
                    ax.add_patch(Rectangle((x - wcell / 2, y_of["bridge"] + dy - 0.5), wcell, 1, fill=False,
                                           ec="#111111", lw=1.4, zorder=4, ls="--" if hollow else "-"))  # fmt: skip
                if per[w].get("l_R") is not None and per[w]["l_R"] in cols:
                    x = xs[cols.index(per[w]["l_R"])]
                    ax.add_patch(Rectangle((x - wcell / 2, y_of["w"] + dy - 0.5), wcell, 1, fill=False, ec="#111111",
                                           lw=1.4, zorder=4, ls="--" if hollow else "-"))  # fmt: skip
                S.record(out_name, t, f"D1 {design}, {group}, {w}: last layer with the bridge word >= 0.3",
                         max(hot) if hot else None, source=src)  # fmt: skip
                S.record(out_name, t, f"D2 {design}, {group}, {w}: l_R", per[w].get("l_R"), source=src)
            # L, per block: a tick under the block; its layers and n on the block's title line, right
            if mod["layer"] in layers:
                xl = xs[cols.index(mod["layer"])]
                yb = y_of["w"] - 1.75
                ax.plot([xl], [yb], "^", ms=5, color="#111111", mfc="white" if hollow else "#111111", zorder=5)
                ax.text(xl + 0.3, yb, "L", va="center", fontsize=S.FONT - 1)
            ax.text(E11_COLS + 0.6, y_of["w"] - 3.0, f"layers {layers[0]}–{layers[-1]}, n = {per['lookup']['n']}",
                    ha="right", va="center", fontsize=S.FONT - 2, color=S.COL["muted"])  # fmt: skip
    for ax, (_, label) in zip(axes, E11_GROUPS, strict=True):
        ax.set_title(label, fontsize=12, weight="bold", loc="left", pad=8)
        ax.set_xlim(-0.9, E11_COLS + 0.6)
        ax.set_ylim(-len(slots) * (block + E11_BLOCK_GAP) + E11_BLOCK_GAP - 2.4, 2.4)
        ax.set_xticks([0.0, E11_COLS], ["in", "last"])
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].set_yticks(ticks, labels, fontsize=S.FONT - 1)
    fig.supxlabel("the input token, then the model's sampled layers, first to last", x=0.64, y=1.3 / h,
                  fontsize=S.FONT - 1)  # fmt: skip
    e11_scale(fig, 0.06, 0.98 / h, "lookup", "lookups switched (upper row)")
    e11_scale(fig, 0.55, 0.98 / h, "recall", "recalls switched (lower row)")
    line = (f"Outlined: the bridge word's last layer at ≥ {HOT:.1f}; the first layer from which it switches ≤ "
            f"{W_FLOOR:.1f}. " + "; ".join(status) + ". " + LT_NOTE)  # fmt: skip
    fig.text(0.01, 0.78 / h, textwrap.fill(line, WRAP + 8), fontsize=S.FONT - 1, color=S.COL["muted"], va="top")
    return save(fig, out_name, out_dir)


# ---- 47.4: where the missing switches sit ----------------------------------------------------------------------------

TERM_TEXT = {"before_L": "at the bridge word before L", "pick_other": "at the pick sentence's other tokens",
             "outside": "outside the pick sentence"}  # fmt: skip
SEGMENTS = (("a", "switched by the bridge-word change at L"), ("before_L", "+ the bridge word at every layer ≤ L"),
            ("propagation", "+ every layer after L (should be 0)"), ("pick_other", "+ the pick sentence's other tokens"),
            ("outside", "outside the pick sentence"))  # fmt: skip
TINT = {"lookup": ("#6a4bd6", "#b6a6ec", "#d62728", "#e4ddf8", "#ffffff"),
        "recall": ("#3a3a3a", "#9a9a9a", "#d62728", "#dcdcdc", "#ffffff")}  # fmt: skip


def cumulative_title(blob: dict, group: str = "locker-first") -> str:
    """The largest of Q47.4's three terms for the lookup in the main test (the verdict's 'largest'), over the tested
    models: the most common one and on how many."""
    tested = [m for m in blob["models"] if m["status"] == "tested"]
    largest = [x for x in (m["cells"]["main"]["lookup"][group].get("largest") for m in tested) if x]
    if not largest:
        return "Why not every lookup switches: no tested model"
    top = max(TERM_TEXT, key=largest.count)
    return f"Lookups the change misses sit mostly {TERM_TEXT[top]} ({largest.count(top)} of {len(tested)} models)"


LT_47_4 = S.REPO / "results" / "x47_cumulative" / "x52_cumulative-20261029T044453Z" / "x47_4.json"  # 27B + Lightning


def build_47_4(verdict_dir: Path, out_name: str = "fig17_cumulative", title: str | None = None, *,
               group: str = "locker-first", out_dir: Path | None = None, planted: bool = False,
               coverage: Path | None = LT_47_4) -> str:  # fmt: skip
    """47.4 (x47_cumulative's x47_4.json): per design (main test; clean one-pick scenes) and model, the lookup's and the
    recall's items split by what switches them: the bridge-word change at L, then the bridge word at every layer <= L,
    then the pick sentence's other tokens; the rest is carried outside the pick sentence. (b)->(c), the propagation
    check, is drawn in red only where it is not 0; a negative term is drawn at 0 and printed. coverage (batch 52, by
    explicit path): fills a model the first verdict did not test (the 27B) and adds Lightning, hollow; a design with no
    items on Lightning (the clean one: no run passed its gate) keeps its row, labelled."""
    path = verdict_dir / "x47_4.json"
    blob = json.loads(path.read_text())
    by = {m["target"]: m for m in blob["models"]}
    srcs = dict.fromkeys(by, rel(path))
    targets = TARGETS
    if coverage is not None:
        for m in json.loads(coverage.read_text())["models"]:
            if m["status"] == "tested" and by.get(m["target"], {}).get("status") != "tested":
                by[m["target"]], srcs[m["target"]] = m, rel(coverage)
        targets = (*TARGETS, LT_ROW)
    plt = S.setup()
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 6.0 + 1.9 * (coverage is not None)), sharey=True)
    ns = ", ".join(f"{SHORT[t]} {by[t]['cells']['main']['lookup'][group]['n']} / "
                   f"{by[t]['cells']['clean']['lookup'][group]['n']}"
                   for t, _, _ in targets if t in by and by[t]["status"] == "tested")  # fmt: skip
    flag = " BUG FLAG in the verdict: not to be read." if blob.get("flags") else ""
    y = header(fig, title or cumulative_title({"models": [by[t] for t, _, _ in targets if t in by]}, group),
               f"Answers (%) in scenes with the {ORDER_TEXT[group]}, by what switches them when more of the changed "
               f"prompt's states are placed; the rest is carried outside the pick sentence. Items (main / clean): "
               f"{ns or 'none'}. Descriptive, no bar; arms fixed in advance.{flag}", planted)  # fmt: skip
    place(fig, y, 2, left=0.21, right=0.98, bottom=0.1 + 0.05 * (coverage is not None), wspace=0.14)
    rows = [(t, w) for t, _, _ in targets for w in ("lookup", "recall")]
    ys = {r: -i - (i // 2) * 0.6 for i, r in enumerate(rows)}  # a gap between models
    for ax, design in zip(axes, ("main", "clean"), strict=True):
        ax.set_title(DESIGN_TEXT[design], fontsize=S.FONT, weight="bold")
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 50, 100])
        ax.set_ylim(min(ys.values()) - 0.6, 0.6)
        ax.tick_params(axis="y", length=0)
        for (t, w), yy in ys.items():
            m = by.get(t)
            c: dict[str, Any] = (
                m["cells"][design][w].get(group, {"n": 0}) if m and m["status"] == "tested" else {"n": 0}
            )
            if not c["n"]:
                if w == "lookup":
                    why = "not run" if not m or m["status"] != "tested" else "no items"
                    why = "not tested: gate" if t == LT_ROW[0] and why == "no items" else why
                    ax.text(2, yy - 0.5, why, va="center", color=S.COL["muted"])
                continue
            hollow = t == LT_ROW[0]
            vals = {"a": c["rate"]["a"], **c["terms"]}
            left = 0.0
            for (k, _), col in zip(SEGMENTS, TINT[w], strict=True):
                v = 100 * vals[k][0]
                S.record(out_name, t, f"47.4 {design}, {group}, {w}: {k}", *vals[k][:3], n=c["n"], source=srcs[t])
                if k == "propagation" and abs(v) < 0.5:
                    continue
                hatch = k == "outside"
                if hollow and not hatch:  # Lightning: the segment's colour as its edge, white inside
                    ax.barh(yy, max(v, 0.0), left=left, height=0.72, fc="white", ec=col, lw=1.4)
                else:
                    ax.barh(yy, max(v, 0.0), left=left, height=0.72, color=col, lw=0.8, hatch="///" if hatch else None,
                            ec=S.COL["muted"] if hatch else "white")  # fmt: skip
                if v >= 9 or v < -0.5:
                    dark = not hollow and (k == "a" or (k == "before_L" and w == "recall"))
                    ax.text(left + v / 2 if v >= 9 else left + 1, yy, f"{v:.0f}", ha="center" if v >= 9 else "left",
                            va="center", color="white" if dark else "#222222", fontsize=S.FONT,
                            bbox={"fc": "white", "ec": "none", "pad": 0.5} if hatch else None)  # fmt: skip
                left += max(v, 0.0)
    axes[0].set_yticks(list(ys.values()), [f"{SHORT[t]} {w}" for t, w in ys])
    for lab, (_, w) in zip(axes[0].get_yticklabels(), ys, strict=True):
        lab.set_color(S.COL[w])
    fig.supxlabel("answers (%)", x=0.575, y=0.01 + 0.06 * (coverage is not None), fontsize=S.FONT)
    hs: list[tuple[Rectangle, ...]] = [(Rectangle((0, 0), 1, 1, color=TINT["lookup"][i]), Rectangle((0, 0), 1, 1, color=TINT["recall"][i]))
          for i in (0, 1, 3)]  # fmt: skip
    hs.append((Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["muted"], hatch="///"),))
    legend(fig, hs, [SEGMENTS[i][1] for i in (0, 1, 3, 4)], y, ncol=2,
           handler_map={tuple: HandlerTuple(ndivide=None, pad=0.0)})  # fmt: skip
    if coverage is not None:  # Dan's figures brief (29 Oct 10:00): each model's status in one line
        status = "; ".join(
            f"{SHORT[t]}: " + ("not run" if t not in by or by[t]["status"] != "tested" else
                               "main test only (clean: not tested, gate), hollow" if t == LT_ROW[0] else
                               "both designs")
            for t, _, _ in targets)  # fmt: skip
        fig.text(0.01, 0.045, textwrap.fill(f"{status}. {LT_NOTE}", WRAP + 6), fontsize=S.FONT - 1,
                 color=S.COL["muted"], va="top")  # fmt: skip
    return save(fig, out_name, out_dir)


# ---- 47.6 (b): is the pointer formed by the pick sentence reading the lockers? -----------------------------------------

DECISIVE_B, CONTROL_B = "block/sentence/all", "control/sentence/all"  # x47_edges' decisive arms
F_ROWS = (("none", "whole change"), (DECISIVE_B, "pick sentence cannot\nread the lockers"),
          (CONTROL_B, "same number of edges\nfrom a neutral sentence"))  # fmt: skip
F_MODELS = tuple(x for x in TARGETS if x[0] != "qwen3.6-27b")  # 47.6 runs on the 9B and Muse


def formation_title(v: dict, res: dict) -> str:
    if v["formation"]["holds"]:
        return "The pointer is formed by the pick sentence reading the lockers"
    tested = [r for r in res.values() if r.get("status") == "tested"]
    if tested and all(r["formation"]["clauses"]["position_fell"] for r in tested):
        return "Blocking the lockers removes position answers, but not selectively"
    return "Position answers survive when the pick sentence cannot read the lockers"


def build_47_6(verdict_dir: Path, out_name: str = "fig18_formation", title: str | None = None, *,
               out_dir: Path | None = None, planted: bool = False) -> str:  # fmt: skip
    """47.6 (b) (x47_edges' verdict.json): per model (9B, Muse), the lookup's answers under the whole change, with the
    pick sentence blocked from reading the locker sentences at layers 0..L (both forwards that form the change), and
    with the same number of edges blocked from a neutral sentence (the control); position first, so its bar reads
    against the rule's 10%; under each bar the recall's switch with its 95% interval."""
    path = verdict_dir / "verdict.json"
    blob = json.loads(path.read_text())
    src = rel(path)
    res = blob["b"]
    plt = S.setup()
    fig, axes = plt.subplots(1, len(F_MODELS), figsize=(S.WIDTH, 5.6), sharey=True)
    held = ", ".join(f"{SHORT[t]} {'yes' if res[t]['formation']['holds'] else 'no'}"
                     for t, _, _ in F_MODELS if res.get(t, {}).get("status") == "tested")  # fmt: skip
    ns = ", ".join(f"{SHORT[t]} {res[t]['n']}" for t, _, _ in F_MODELS if res.get(t, {}).get("status") == "tested")
    y = header(fig, title or formation_title(blob["verdict"], res),
               f"Lookup answers (%), routes test (another item moved), blocks at layers 0 to L; under each bar the "
               f"recalls switched (%) with 95% interval. Items: {ns or 'none'}. Rule, fixed in advance: position ≤ 10% "
               "with the block; identity and recall within 10 points of the whole change; the neutral sentence within "
               f"10 points on all three. Holds on: {held or 'none'}.", planted)  # fmt: skip
    place(fig, y, 1, left=0.25, right=0.98, bottom=0.12, wspace=0.16)
    for ax, (t, _, name) in zip(axes, F_MODELS, strict=True):
        r = res.get(t, {"status": "pending"})
        ax.set_title(name, fontsize=S.FONT, weight="bold")
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 50, 100])
        ax.set_ylim(-len(F_ROWS) + 0.3, 0.75)
        ax.tick_params(axis="y", length=0)
        if r["status"] != "tested":
            S.empty(ax, "not tested (gate)" if r["status"] == "not tested" else "not run")
            continue
        lk, rc = r["b"]["lookup"]["rate"], r["b"]["recall"]["rate"]
        for i, (arm, _) in enumerate(F_ROWS):
            left = 0.0
            for route in ROUTE_COL:
                v = lk.get(f"{arm}|{route}")
                if v is None:
                    continue
                ax.barh(-i, 100 * v[0], left=left, height=0.5, color=ROUTE_COL[route], ec="white", lw=0.8)
                if route in ("position", "identity") and v[0] >= 0.1:
                    ax.text(left + 50 * v[0], -i, f"{100 * v[0]:.0f}", ha="center", va="center", fontsize=S.FONT,
                            color="white" if route == "identity" else "#222222")  # fmt: skip
                S.record(out_name, t, f"47.6 (b) {arm}: lookup {route} share", *v[:3], n=r["n"], source=src)
                left += 100 * v[0]
            sw = rc.get(f"{arm}|switched")
            if sw is not None:
                v = pct(sw)
                S.dot(ax, 0, -i - 0.4, v, S.COL["recall"], size=6.5)
                right = v[1] < 25
                ax.text(v[2] + 1.5 if right else v[1] - 1.5, -i - 0.4, f"recall {v[0]:.0f}", va="center",
                        ha="left" if right else "right", fontsize=S.FONT - 1, color=S.COL["recall"])  # fmt: skip
                S.record(out_name, t, f"47.6 (b) {arm}: recall switched", *sw[:3], n=r["n"], source=src)
        rule_bar(ax, 10, "rule: position ≤ 10", 0.3)
        S.record(out_name, t, "47.6 (b): the formation rule holds", int(bool(r["formation"]["holds"])), source=src)
    axes[0].set_yticks([-i for i in range(len(F_ROWS))], [x[1] for x in F_ROWS])
    fig.supxlabel("lookup answers (%)", x=0.615, y=0.01, fontsize=S.FONT)
    hs = [Rectangle((0, 0), 1, 1, color=c) for c in ROUTE_COL.values()]
    legend(fig, hs, list(ROUTE_TEXT.values()), y, ncol=5)
    return save(fig, out_name, out_dir)


# ---- 47.7: the value, question first, other formats, colour values -----------------------------------------------------

A_TITLE = {"address regardless": "Even with the question first, the lookup keeps the address",
           "prefetch on demand, not shown in the J-space": "With the question first, the lookup fetches the value",
           "prefetch on demand, the prefetched value is in the J-space":
               "With the question first, the value is fetched into the J++ part",
           "neither label on 2 of 3 models": "Question first: neither prefetch nor address on 2 of 3 models"}  # fmt: skip
FORMAT_TEXT = (("prose", "prose", "o"), ("json", "JSON", "s"), ("table", "table", "^"))
QL_COL = S.COL["control"]


def newest(folder: Path, pattern: str) -> Path | None:
    found = sorted(folder.glob(pattern)) if folder.exists() else []
    return found[-1] if found else None


def value_parts(verdict_dir: Path, c_dir: Path | None, b_dir: Path | None) -> dict[str, tuple[dict, str] | None]:
    """The three parts' verdicts: (a) from verdict_dir, (c) and (b) from the given folders or the newest siblings."""
    out: dict[str, tuple[dict, str] | None] = {}
    for part, d in (("a", verdict_dir), ("c", c_dir), ("b", b_dir)):
        d = d or newest(verdict_dir.parent, f"x47_7{part}-*")
        f = d / f"x47_7{part}.json" if d else None
        out[part] = (json.loads(f.read_text()), rel(f)) if f and f.exists() else None
    return out


def value_title(parts: dict) -> str:
    if parts["a"]:
        label = str(parts["a"][0]["verdict"]["label"])
        return A_TITLE.get(label, label)
    if parts["c"]:
        return f"Other formats: {parts['c'][0]['verdict']['label']}"
    return "The value: no part scored"


def value_verdicts(parts: dict) -> str:
    out = []
    if parts["a"]:
        out.append(f"(a) {parts['a'][0]['verdict']['label']}")
    if parts["c"]:
        out.append(f"(c) {parts['c'][0]['verdict']['label']}")
    if parts["b"]:
        v = parts["b"][0]["verdict"]
        out.append("(b) never the value for a word value too: " + ("yes" if v.get("never_the_value_word") else "no"))
    return "; ".join(out) or "no part scored"


def value_his(m: dict) -> list[float]:
    """Every value share's upper bound a model's verdict holds (the shared x range)."""
    cells = list(m.get("shares", {}).values()) + [c for c in m.get("cells", {}).values() if c]
    return [c["arms"]["whole"]["value"][2] for c in cells if finite(c["arms"]["whole"]["value"][2])]


def build_47_7(verdict_dir: Path, out_name: str = "fig19_value", title: str | None = None, *,
               c_dir: Path | None = None, b_dir: Path | None = None, out_dir: Path | None = None,
               planted: bool = False) -> str:  # fmt: skip
    """47.7 (x47_value's x47_7a / x47_7c / x47_7b.json; verdict_dir is (a)'s folder, (c) and (b) default to the newest
    sibling folders): the lookup's value answers (%) under the whole change, routes test (another item moved). (a) per
    model question last (grey) and question first (green), the value probe under them; (c) per model prose / JSON /
    table, question last; (b) colour values, question last and first. The rule's bars thin and labelled."""
    parts = value_parts(verdict_dir, c_dir, b_dir)
    by = {p: ({m["target"]: m for m in v[0]["models"]} if v else {}) for p, v in parts.items()}
    plt = S.setup()
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 5.4), sharey=True, sharex=True)
    y = header(fig, title or value_title(parts),
               "Lookup answers that name the new value (%) under the whole change, routes test (another item moved), "
               f"95% intervals; (a) also the value probe at the bridge word. Fixed in advance. {value_verdicts(parts)}.",
               planted)  # fmt: skip
    place(fig, y, 1, left=0.19, right=0.985, bottom=0.12, wspace=0.1)
    ys = {t: -i for i, (t, _, _) in enumerate(TARGETS)}
    hi = [100 * x for v in parts.values() if v for m in v[0]["models"] for x in value_his(m)]
    xmax = max(30.0, 10 * math.ceil((max(hi) if hi else 0) / 10))
    heads = (("a", "(a) question first", ((5, "≤ 5"), (15, "≥ 15"))), ("c", "(c) prose / JSON / table", ((5, "≤ 5"),)),
             ("b", "(b) colour values", ((5, "≤ 5"), (15, "≥ 15"))))  # fmt: skip
    for ax, (part, head, bars) in zip(axes, heads, strict=True):
        ax.set_title(head, fontsize=S.FONT, weight="bold")
        ax.set_xlim(-0.04 * xmax, xmax)  # a dot at 0 stays whole
        ax.set_xticks(range(0, int(xmax), 10))
        ax.set_ylim(-len(TARGETS) + 0.35, 0.6)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
        for x, lab in bars:
            rule_bar(ax, x, lab, 0.32)
        found = parts[part]
        if not found:
            S.empty(ax, "not run")
            continue
        src = found[1]
        for t, yy in ys.items():
            m = by[part].get(t)
            if m is None or m["status"] == "pending":
                ax.text(1, yy, "not run", va="center", color=S.COL["muted"])
            elif part == "c":
                value_formats(ax, m, yy, src, out_name)
            else:
                value_renderings(ax, m, yy, part, src, out_name)
    axes[0].set_yticks(list(ys.values()), [NAME[t] for t in ys])
    fig.supxlabel("value answers (%)", x=0.59, y=0.01, fontsize=S.FONT)
    g = S.COL["value"]
    hs = [Line2D([], [], marker="o", ls="", color=QL_COL, ms=7), Line2D([], [], marker="o", ls="", color=g, ms=7),
          *(Line2D([], [], marker=mk, ls="", color=g, ms=6.5) for _, _, mk in FORMAT_TEXT)]  # fmt: skip
    legend(fig, hs, ["question last", "question first", *(lab for _, lab, _ in FORMAT_TEXT)], y, ncol=5)
    return save(fig, out_name, out_dir)


def value_renderings(ax, m: dict, y: float, part: str, src: str, fig_id: str) -> None:
    """(a) and (b): question last (grey) above question first (green); (a): the value probe as text under them."""
    if m["status"] != "tested":  # the gate, or the sanity swap's check (x47_value labels it "C0 failed")
        why = "not tested (sanity swap)" if m.get("why", "").startswith("C0") else "not tested (gate)"
        ax.text(1, y, why, va="center", color=S.COL["muted"])
        return
    for dy, r, col in ((0.17, "ql", QL_COL), (-0.17, "qf", S.COL["value"])):
        s = m.get("shares", {}).get(r)
        if not s:
            continue
        v = s["arms"]["whole"]["value"]
        S.dot(ax, 0, y + dy, pct(v), col, size=7)
        S.record(fig_id, m["target"], f"47.7({part}) {r}: value share (whole change)", *v[:3], n=s["n"], source=src)
    p = m.get("probe", {})
    if part == "a" and "ql" in p and "qf" in p and finite(p["qf"]["probe"][0]):
        ax.text(0.5, y - 0.45, f"value probe {100 * p['ql']['probe'][0]:.0f} → {100 * p['qf']['probe'][0]:.0f}%",
                va="center", fontsize=S.FONT - 1, color=S.COL["muted"], zorder=4,
                bbox={"fc": "white", "ec": "none", "pad": 0.5})  # fmt: skip
        for r in ("ql", "qf"):
            S.record(fig_id, m["target"], f"47.7(a) {r}: value probe", *p[r]["probe"][:3], n=p[r].get("n"), source=src)


def value_formats(ax, m: dict, y: float, src: str, fig_id: str) -> None:
    """(c): prose / JSON / table, question last, one marker shape each."""
    for k, (f, lab, mk) in enumerate(FORMAT_TEXT):
        yy = y + 0.25 - 0.25 * k
        c = m["cells"].get(f)
        if c is None:
            ax.text(1, yy, f"{lab}: not tested (gate)", va="center", fontsize=S.FONT - 1, color=S.COL["muted"])
            continue
        v = pct(c["arms"]["whole"]["value"])
        ax.plot([v[1], v[2]], [yy, yy], color=S.COL["value"], lw=1.6, solid_capstyle="butt", zorder=2)
        ax.plot([v[0]], [yy], mk, ms=6.5, color=S.COL["value"], zorder=3)
        S.record(fig_id, m["target"], f"47.7(c) {f}: value share (whole change)", *c["arms"]["whole"]["value"][:3],
                 n=c["n"], source=src)  # fmt: skip


# ---- 47.0: the lens monitor does not see the pointer -----------------------------------------------------------------

POINTER_COL = S.COL["position"]  # the pointer carries the position route


def verbal_title(blob: dict) -> str:
    o = blob["overall"]
    if o == "not verbalizable":
        return "Read through the J++ lens, the pointer looks like a random direction"
    if o.startswith("partly"):
        return "Read through the J++ lens, the pointer is partly visible"
    return f"Read through the J++ lens, the pointer is {o}"


def null_band(ax, y: float, lo: float, hi: float) -> None:
    """The random draws from their median (or mean) to the cutoff, a grey bar behind the row's dot."""
    ax.plot([min(lo, hi), max(lo, hi)], [y, y], color=S.COL["control"], lw=11, solid_capstyle="butt", zorder=1)


def build_47_0(verdict_dir: Path, out_name: str = "fig20_verbal", title: str | None = None, *,
               out_dir: Path | None = None, planted: bool = False) -> str:  # fmt: skip
    """47.0 (x47_verbal's verbal.json; descriptive): per model, the pointer write (h + 2 (mu_k - mu_j)) against 200
    random draws of the same norm and the identity change (positive comparison): (1) the rank in the lens readout of
    the best ordinal word (pointer) and of the new item's name (identity); (2) the share of the direction 25 lens
    directions rebuild; (3) how far the readout moves (KL). Grey: the random draws, from their median (mean for the
    share) to the cutoff (ranks: the best 5%; share and KL: the top 5%)."""
    path = verdict_dir / "verbal.json"
    blob = json.loads(path.read_text())
    src = rel(path)
    models = blob["models"]
    plt = S.setup()
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 4.8), sharey=True)
    ns = sorted({models[t]["n_cases"] for t in models})
    n = f"{ns[0]} cases per model" if len(ns) == 1 else " / ".join(str(models[t]["n_cases"]) for t, _, _ in TARGETS
                                                                   if t in models) + " cases"  # fmt: skip
    y = header(fig, title or verbal_title(blob),
               f"Descriptive. The J++ lens at L on the bridge word, {n}: a pointer write (dose 2×), an identity "
               "change and 200 random draws of the same size (grey: their median to their most extreme 5%).",
               planted)  # fmt: skip
    place(fig, y, 1, title_lines=2, left=0.19, right=0.985, bottom=0.08, wspace=0.12)
    ys = {t: -i for i, (t, _, _) in enumerate(TARGETS) if t in models}
    k = 25
    for t, yy in ys.items():
        r = models[t]
        a_o, a_i = r["a"]["write|best_ordinal"], r["a"].get("identity|alt_name")
        null_band(axes[0], yy + 0.15, a_o["null_median_of_medians"], a_o["null_cut"])
        axes[0].plot([a_o["median"]], [yy + 0.15], "o", ms=7.5, color=POINTER_COL, zorder=3)
        S.record(out_name, t, "47.0 (a) best ordinal word's rank, h + pointer write (median; null cut, null median)",
                 a_o["median"], a_o["null_cut"], a_o["null_median_of_medians"], n=r["n_cases"], source=src)  # fmt: skip
        if a_i:
            null_band(axes[0], yy - 0.15, a_i["null_median_of_medians"], a_i["null_cut"])
            axes[0].plot([a_i["median"]], [yy - 0.15], "o", ms=7.5, color=S.COL["identity"], zorder=3)
            S.record(out_name, t, "47.0 (a) new item's name rank, h + identity change (median; null cut, null median)",
                     a_i["median"], a_i["null_cut"], a_i["null_median_of_medians"], n=r["n_identity_cases"],
                     source=src)  # fmt: skip
        b = r["b"][f"all|{k}"]
        S.record(out_name, t, f"47.0 (b) share rebuilt by {k} lens directions: random draws (mean; mean, 95th pct)",
                 b["random_mean"], b["random_mean"], b["random_p95"], source=src)  # fmt: skip
        for dy, key, col in ((0.15, "pointer", POINTER_COL), (-0.15, "identity_mean", S.COL["identity"])):
            null_band(axes[1], yy + dy, 100 * b["random_mean"], 100 * b["random_p95"])
            axes[1].plot([100 * b[key]], [yy + dy], "o", ms=7.5, color=col, zorder=3)
            S.record(out_name, t, f"47.0 (b) share rebuilt by {k} lens directions: {key}", b[key], source=src)
        axes[1].text(100 * max(b["pointer"], b["random_p95"]) + 1, yy + 0.15, f"{b['ratio']:.1f}× random",
                     va="center", fontsize=S.FONT - 1, color=POINTER_COL)  # fmt: skip
        for dy, key, col in ((0.15, "write", POINTER_COL), (-0.15, "identity", S.COL["identity"])):
            c = r["c"].get(key)
            if not c:
                continue
            null_band(axes[2], yy + dy, c["null_median_of_medians"], c["null_cut"])
            axes[2].plot([c["median"]], [yy + dy], "o", ms=7.5, color=col, zorder=3)
            S.record(out_name, t, f"47.0 (c) KL of the readout, h + {key} (median; null median, null cut)", c["median"],
                     c["null_median_of_medians"], c["null_cut"], n=r["n_cases"], source=src)  # fmt: skip
    axes[0].set_xscale("log")
    axes[0].set_xlim(1, 1e5)
    axes[0].set_xticks([1, 100, 10000], ["1", "100", "10k"])
    axes[0].set_title("rank of the word\n(1 = the lens says it)", fontsize=S.FONT, weight="bold")
    axes[1].set_xlim(0, 27)
    axes[1].set_xticks([0, 10, 20])
    axes[1].set_title(f"share rebuilt by\n{k} lens directions (%)", fontsize=S.FONT, weight="bold")
    axes[2].set_xscale("log")
    axes[2].set_xlim(0.02, 10)
    axes[2].set_xticks([0.1, 1, 10], ["0.1", "1", "10"])
    axes[2].set_title("readout moves\n(KL, nats)", fontsize=S.FONT, weight="bold")
    for ax in axes:
        ax.set_ylim(-len(ys) + 0.5, 0.5)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
    axes[0].set_yticks(list(ys.values()), [NAME[t] for t in ys])
    hs = [Line2D([], [], marker="o", ls="", color=POINTER_COL, ms=7.5),
          Line2D([], [], marker="o", ls="", color=S.COL["identity"], ms=7.5),
          Rectangle((0, 0), 1, 0.6, color=S.COL["control"])]  # fmt: skip
    legend(fig, hs, ["pointer write", "identity change", "random draws (same size)"], y, ncol=3)
    return save(fig, out_name, out_dir)


JPP_COL = "#b23b3b"  # the J++ part (story_b48.JPP)


def tag(ax, text: str) -> None:
    """story_style.panel_tag's look for a tag it has no status for (here: descriptive)."""
    ax.text(1.0, 1.015, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=S.FONT, color=S.COL["muted"],
            zorder=8, bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})  # fmt: skip


def build_e8(verbal_dir: Path, report_dir: Path, out_name: str = "fig07b_verbal", *,
             out_dir: Path | None = None) -> str:  # fmt: skip
    """E8 (v6 iteration 2), three panels, one row per model (9B, 27B, Muse). (1) Read-through, 47.0 (a) (descriptive;
    x47_verbal's verbal.json): the median rank of the best ordinal word in the lens readout at L on the bridge word under
    an address swap, against 200 random draws of the same size (grey: their median to their best 5%). (2) Share
    rebuilt, 47.0 (b): the share of the change that 25 lens directions rebuild, for the address swap and an identity
    change, against the random draws (grey: their mean to their 95th percentile). (3) 47.10 on the 27B (fixed in
    advance; x47_report's x47_10.json, question last): the report's switches lost beyond a random part without the
    address (95% interval); the 9B and Muse fail the report gate. The report's loss without the J++ part and the lens
    top-five share are recorded (e8_report), not drawn. 47.0's KL and the identity ranks: supplement s07b_lens_readout."""
    vpath, rpath = verbal_dir / "verbal.json", report_dir / "x47_10.json"
    vblob, rblob = json.loads(vpath.read_text()), json.loads(rpath.read_text())
    vsrc, rsrc = rel(vpath), rel(rpath)
    plt = S.setup()
    h = 4.7
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, h), sharey=True, gridspec_kw={"width_ratios": [1, 1, 1]})
    fig.subplots_adjust(left=0.19, right=0.975, top=1 - 1.55 / h, bottom=0.2, wspace=0.12)
    S.title(fig, "The lens is blind to the address",
            "An address swap read through the lens, against random draws; then the 27B asked to report the position.")  # fmt: skip
    models = vblob["models"]
    ys = {t: -i for i, (t, _, _) in enumerate(TARGETS) if t in models}
    k = 25

    # (1) read-through, 47.0 (a): the right ordinal word's rank under the address swap
    ax = axes[0]
    for t, yy in ys.items():
        a_o = models[t]["a"]["write|best_ordinal"]
        null_band(ax, yy, a_o["null_median_of_medians"], a_o["null_cut"])
        ax.plot([a_o["median"]], [yy], "o", ms=7.5, color=POINTER_COL, zorder=3)
        S.record(out_name, t, "47.0 (a) best ordinal word's rank, h + pointer write (median; null cut, null median)",
                 a_o["median"], a_o["null_cut"], a_o["null_median_of_medians"], n=models[t]["n_cases"], source=vsrc)  # fmt: skip
    ax.set_xscale("log")
    ax.set_xlim(1, 1e5)
    ax.set_xticks([1, 100, 10000], ["1", "100", "10k"])
    ax.set_xlabel("rank of the right\nordinal word")
    ax.set_title("Read through the lens", fontsize=12, weight="bold", loc="left", pad=22)

    # (2) share rebuilt by 25 lens directions, 47.0 (b)
    ax = axes[1]
    for t, yy in ys.items():
        b = models[t]["b"][f"all|{k}"]
        S.record(out_name, t, f"47.0 (b) share rebuilt by {k} lens directions: random draws (mean; mean, 95th pct)",
                 b["random_mean"], b["random_mean"], b["random_p95"], source=vsrc)  # fmt: skip
        # random draws in the middle row: their mean (square) to their 95th percentile (whisker)
        ax.plot([b["random_mean"], b["random_p95"]], [yy, yy], color=S.COL["control"], lw=2.2, zorder=2)
        ax.plot([b["random_mean"]], [yy], "s", ms=7, color=S.COL["control"], zorder=3)
        for dy, key, col in ((0.26, "pointer", POINTER_COL), (-0.26, "identity_mean", S.COL["identity"])):
            ax.plot([b[key]], [yy + dy], "o", ms=7.5, color=col, zorder=3)
            S.record(out_name, t, f"47.0 (b) share rebuilt by {k} lens directions: {key}", b[key], source=vsrc)
        ax.text(max(b["pointer"], b["random_p95"]) + 0.03, yy + 0.26, f"{b['ratio']:.1f}× random", va="center",
                fontsize=S.FONT - 1, color=POINTER_COL)  # fmt: skip
        S.record(out_name, t, f"47.0 (b) share rebuilt by {k} lens directions: pointer / random mean", b["ratio"],
                 source=vsrc)  # fmt: skip
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.set_xlabel("share of the address\nthe lens can rebuild")
    ax.set_title("Share rebuilt", fontsize=12, weight="bold", loc="left", pad=22)
    ns = sorted({models[t]["n_cases"] for t in ys})
    for a in axes[:2]:
        tag(a, f"n = {ns[0] if len(ns) == 1 else ', '.join(map(str, ns))}  descriptive")
        a.grid(axis="x", color="#eeeeee")
    axes[0].set_ylim(-len(ys) + 0.45, 0.6)
    axes[0].set_yticks(list(ys.values()), [NAME[t] for t in ys])
    for a in axes:
        a.tick_params(axis="y", length=0)

    # (3) 47.10 on the 27B, question last
    ax = axes[2]
    m = next(x for x in rblob["models"]
             if x["status"] == "tested" and "report" in x["orders"]["last"].get("readers", {}))  # fmt: skip
    o = m["orders"]["last"]
    rd, lens = o["readers"]["report"], o["lens"]["report"]
    rows = ((rd["alf"]["excess"], "47.10: the report's extra loss without the address", rd["n"]),
            (rd["jpp"]["excess"], "47.10: the report's extra loss without the J++ part", rd["n"]),
            (lens["top5_ordinal"], "47.10: lens top-5 holds the right ordinal (report prompt)", lens["n"]))  # fmt: skip
    for v, quantity, n in rows:
        S.record("e8_report", m["target"], quantity, *v, n=n, source=rsrc)
    v = rd["alf"]["excess"]
    y = ys.get(m["target"], -1)
    ax.barh(y, max(v[0], 0.0), height=0.42, color=POINTER_COL, zorder=2)
    ax.plot([v[1], v[2]], [y, y], color="#1e1e1e", lw=1.2, zorder=3)
    ax.text(max(v[2], v[0], 0.0) + 0.03, y, f"{v[0]:.2f}", va="center", fontsize=S.FONT, color="#1e1e1e")
    for x in rblob["models"]:
        if x is not m and x["target"] in ys:
            ax.text(0.03, ys[x["target"]], "cannot report (gate)", va="center", fontsize=S.FONT - 1,
                    color=S.COL["muted"])  # fmt: skip
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.grid(axis="x", color="#eeeeee")
    ax.set_xlabel("reports lost without\nthe address (share)")
    ax.set_title("The 27B's report", fontsize=12, weight="bold", loc="left", pad=22)
    S.panel_tag(ax, str(rd["n"]), "fixed")
    hs = [Line2D([], [], marker="o", ls="", color=POINTER_COL, ms=7.5),
          Line2D([], [], marker="o", ls="", color=S.COL["identity"], ms=7.5),
          Line2D([], [], marker="s", color=S.COL["control"], ms=7, lw=2.2)]  # fmt: skip
    legend(fig, hs, ["address swap", "identity change", "a random part (same size)"], 1 - 0.62 / h, ncol=3)
    return save(fig, out_name, out_dir)


TESTS: dict[str, tuple[str, Any, str]] = {
    "D1": ("scripts/x47_depthmap.py", build_d1, "fig16_depth_map"),
    "47.4": ("scripts/x47_cumulative.py", build_47_4, "fig17_cumulative"),
    "47.6": ("scripts/x47_edges.py", build_47_6, "fig18_formation"),
    "47.7": ("scripts/x47_value.py", build_47_7, "fig19_value"),
    "47.0": ("scripts/x47_verbal.py", build_47_0, "fig20_verbal"),
}
