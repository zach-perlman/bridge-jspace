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

from scripts import story_style as S

PLANTED = "PLANTED data, not results. "
WRAP = 104  # subtitle characters per line at 11 pt across the 8.8 in column
LINE = 0.19  # inches per subtitle or legend line
TARGETS = tuple((t, m, name) for t, m, name in S.MODELS if m != "122b")  # batch 47 ran on the 9B, the 27B and Muse
NAME = {t: name for t, _, name in S.MODELS}
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse"}
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


def build_47_4(verdict_dir: Path, out_name: str = "fig17_cumulative", title: str | None = None, *,
               group: str = "locker-first", out_dir: Path | None = None, planted: bool = False) -> str:  # fmt: skip
    """47.4 (x47_cumulative's x47_4.json): per design (main test; clean one-pick scenes) and model, the lookup's and the
    recall's items split by what switches them: the bridge-word change at L, then the bridge word at every layer <= L,
    then the pick sentence's other tokens; the rest is carried outside the pick sentence. (b)->(c), the propagation
    check, is drawn in red only where it is not 0; a negative term is drawn at 0 and printed."""
    path = verdict_dir / "x47_4.json"
    blob = json.loads(path.read_text())
    src = rel(path)
    by = {m["target"]: m for m in blob["models"]}
    plt = S.setup()
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 6.0), sharey=True)
    ns = ", ".join(f"{SHORT[t]} {by[t]['cells']['main']['lookup'][group]['n']} / "
                   f"{by[t]['cells']['clean']['lookup'][group]['n']}"
                   for t, _, _ in TARGETS if t in by and by[t]["status"] == "tested")  # fmt: skip
    flag = " BUG FLAG in the verdict: not to be read." if blob.get("flags") else ""
    y = header(fig, title or cumulative_title(blob, group),
               f"Answers (%) in scenes with the {ORDER_TEXT[group]}, by what switches them when more of the changed "
               f"prompt's states are placed; the rest is carried outside the pick sentence. Items (main / clean): "
               f"{ns or 'none'}. Descriptive, no bar; arms fixed in advance.{flag}", planted)  # fmt: skip
    place(fig, y, 2, left=0.17, right=0.98, bottom=0.1, wspace=0.14)
    rows = [(t, w) for t, _, _ in TARGETS for w in ("lookup", "recall")]
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
                    ax.text(2, yy - 0.5, "not run" if not m or m["status"] != "tested" else "no items", va="center",
                            color=S.COL["muted"])  # fmt: skip
                continue
            vals = {"a": c["rate"]["a"], **c["terms"]}
            left = 0.0
            for (k, _), col in zip(SEGMENTS, TINT[w], strict=True):
                v = 100 * vals[k][0]
                S.record(out_name, t, f"47.4 {design}, {group}, {w}: {k}", *vals[k][:3], n=c["n"], source=src)
                if k == "propagation" and abs(v) < 0.5:
                    continue
                hatch = k == "outside"
                ax.barh(yy, max(v, 0.0), left=left, height=0.72, color=col, ec=S.COL["muted"] if hatch else "white",
                        lw=0.8, hatch="///" if hatch else None)  # fmt: skip
                if v >= 9 or v < -0.5:
                    dark = k == "a" or (k == "before_L" and w == "recall")
                    ax.text(left + v / 2 if v >= 9 else left + 1, yy, f"{v:.0f}", ha="center" if v >= 9 else "left",
                            va="center", color="white" if dark else "#222222", fontsize=S.FONT,
                            bbox={"fc": "white", "ec": "none", "pad": 0.5} if hatch else None)  # fmt: skip
                left += max(v, 0.0)
    axes[0].set_yticks(list(ys.values()), [f"{SHORT[t]} {w}" for t, w in ys])
    for lab, (_, w) in zip(axes[0].get_yticklabels(), ys, strict=True):
        lab.set_color(S.COL[w])
    fig.supxlabel("answers (%)", x=0.575, y=0.01, fontsize=S.FONT)
    hs: list[tuple[Rectangle, ...]] = [(Rectangle((0, 0), 1, 1, color=TINT["lookup"][i]), Rectangle((0, 0), 1, 1, color=TINT["recall"][i]))
          for i in (0, 1, 3)]  # fmt: skip
    hs.append((Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["muted"], hatch="///"),))
    legend(fig, hs, [SEGMENTS[i][1] for i in (0, 1, 3, 4)], y, ncol=2,
           handler_map={tuple: HandlerTuple(ndivide=None, pad=0.0)})  # fmt: skip
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


TESTS: dict[str, tuple[str, Any, str]] = {
    "D1": ("scripts/x47_depthmap.py", build_d1, "fig16_depth_map"),
    "47.4": ("scripts/x47_cumulative.py", build_47_4, "fig17_cumulative"),
    "47.6": ("scripts/x47_edges.py", build_47_6, "fig18_formation"),
    "47.7": ("scripts/x47_value.py", build_47_7, "fig19_value"),
    "47.0": ("scripts/x47_verbal.py", build_47_0, "fig20_verbal"),
}
