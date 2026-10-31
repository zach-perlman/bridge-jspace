"""The deck's curve figures (31 Oct), 2400 x 1000 px (12 x 5 in at 200 dpi), no title inside, the key as one line of text (no legend box):
f15_link_crossover (claim 10's panel C: the lookups switched by layer, the change at the bridge word against the same change copied into the locker
sentences) and the depth curves (claim 12: f13b for the three models of the deck, f13c for all five, the appendix). Numbers come from
data/figures/depth/data.csv, the rows scripts/readme_story_figures.py records from the run files."""

from __future__ import annotations

import re

import matplotlib.pyplot as plt

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import lint
from bridge_jspace.figkit.dottable import FAINT, INK, MUTED, C, rich
from bridge_jspace.figkit.exemplars import NAME

OUT, DPI = ".", 200
W, H = 12.0, 5.0
PROBLEMS: list[str] = []
DEPTH = {"qwen3.5-9b": 32, "qwen3.6-27b": 64, "muse-glimmer-30b": 52, "nemotron-3.5-lightning": 52, "qwen3.5-122b-a10b": 48}
GATE = 0.30  # the whole change must switch at least this share of the lookups for a layer to count (scripts/story_style.NI_SWITCH)
FS = 12  # pt: 33 px at 200 dpi


def _save(fig, name: str) -> None:
    PROBLEMS.extend(lint.table_problems(fig, name, need_xlabel=True))
    fig.savefig(f"{OUT}/{name}.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def _layers(model: str, figure: str, pattern: str) -> list[int]:
    return sorted({int(m.group(1)) for (f, mo, q) in D.story() if f == figure and mo == model and (m := re.match(pattern, q))})


def _key(fig, rows: list[list[tuple[str, str, str]]], y0: float) -> None:
    for i, parts in enumerate(rows):
        rich(fig, 0.012, y0 - i * 0.36 / H, parts, size=FS - 0.5)


def _axis_x(ax, depth: int, xmax: float = 1.03) -> None:
    ax.set_xlim(-0.03, xmax)
    ax.set_xticks([0, 0.5, 1.0], [f"{t:g}\nL{round(t * depth)}" for t in (0, 0.5, 1.0)])
    ax.tick_params(labelsize=FS, length=3, color=FAINT)
    ax.set_xlabel("layer, as a share of the depth", fontsize=FS, color=MUTED, labelpad=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(FAINT)
    ax.spines["bottom"].set_color(FAINT)
    ax.grid(axis="y", color="#EEEEEE")
    ax.set_axisbelow(True)


# ---- f15: claim 10, panel C -----------------------------------------------------------------------------------------------
def f_link_crossover() -> None:
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
    fig, axes = plt.subplots(1, 3, figsize=(W, H), sharey=True, gridspec_kw={"width_ratios": [1, 1, 1.75], "wspace": 0.1})
    fig.subplots_adjust(left=0.115, right=0.995, top=1 - 1.6 / H, bottom=1.1 / H)
    light, dark = C["lookup_light"], C["lookup_dark"]
    bw = "45q, layer {}: the bridge-word change (lookups switched)"
    cp = "45q, layer {}: the copy into the locker sentences (lookups switched)"
    arms = (("a", "the bridge-word change at L", "L", light), ("c", "copy at L, every locker-sentence token", "L", dark),
            ("d", "copy at L/2, every locker-sentence token", "L/2", dark))  # (arm, quantity, which layer, colour)
    offs = {"qwen3.5-9b": {"a": (10, -2), "c": (0, 14), "d": (-8, 12)}, "qwen3.6-27b": {"a": (0, 14), "c": (0, 14), "d": (-8, 12)},
            "muse-glimmer-30b": {"a": (0, 14), "c": (0, 14), "d": (10, 6)}}  # value labels in points, clear of the curves
    for k, (ax, m) in enumerate(zip(axes, models, strict=True)):
        depth = DEPTH[m]
        _axis_x(ax, depth, 1.03 + (0.75 if k == 2 else 0))
        ax.set_ylim(-0.04, 1.1)
        ax.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.set_title(NAME[m], fontsize=FS + 2, weight="bold", loc="left", pad=30)
        layers = _layers(m, "fig03", r"45q, layer (\d+): the bridge-word change")
        for name, col, ls in ((bw, light, "--"), (cp, dark, "-")):
            v = [D.s(m, name.format(la), "fig03") for la in layers]
            xs = [la / depth for la in layers]
            ax.fill_between(xs, [t[1] for t in v], [t[2] for t in v], color=col, alpha=0.2, lw=0, zorder=1)
            ax.plot(xs, [t[0] for t in v], color=col, ls=ls, lw=2.4, marker="o", ms=5, mfc="white", mec=col, mew=1.3, zorder=2)  # open marks: the sweep, post hoc
        L, half = (D.s(m, f"45q: {q}", "fig03")[0] for q in ("L, the rule's layer", "L/2, the rule's half layer"))
        for x, txt in ((half / depth, "L/2"), (L / depth, "L")):
            ax.axvline(x, color="#555555", ls=":", lw=1.3, zorder=0)
            ax.text(x, 1.02, txt, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=FS, color="#555555")
        for arm, what, which, col in arms:  # the cells fixed in advance
            off = offs[m][arm]
            r = D.s(m, f"45q, the rule's arm {arm}: {what} (lookups switched)", "fig03")
            x = (L if which == "L" else half) / depth
            ax.plot([x, x], [r[1], r[2]], color=INK, lw=1.6, zorder=5)
            ax.plot([x], [r[0]], "o", ms=12, color=col, mec=INK, mew=1.3, zorder=6)
            ax.annotate(f"{r[0]:.2f}", (x, r[0]), xytext=off, textcoords="offset points", ha="center" if off[0] == 0 else ("right" if off[0] < 0 else "left"), va="center", fontsize=FS,
                        color=INK, zorder=7, bbox={"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"})
        if k == 2:  # each curve named once, at its right end, in the empty margin
            for y, ls, col, txt in ((0.44, "--", light, "the change at\nthe bridge word"), (0.13, "-", dark, "the same change\ncopied into the\nlocker sentences")):
                ax.plot([1.0, 1.1], [y, y], color=col, ls=ls, lw=2.4, clip_on=False)
                ax.text(1.13, y, txt, ha="left", va="center", fontsize=FS, color=col if col == dark else "#7D72D0", linespacing=1.05)
    axes[0].set_ylabel("lookups\nswitched\n(share)", fontsize=FS, rotation=0, ha="right", va="center", labelpad=8)
    _key(fig, [[("●", dark, "normal"), (" the cells fixed in advance (L/2 and L), values printed      ", MUTED, "normal"), ("○", INK, "normal"),
                (" the layer sweep, post hoc      bands and whiskers: 95%", MUTED, "normal")],
               [("Locker sentence after the pick. Lightning (below its gate) and the 122B (no run) are not drawn.", MUTED, "normal")]], 1 - 0.22 / H)
    _save(fig, "f15_link_crossover")


# ---- f13b / f13c: claim 12 -------------------------------------------------------------------------------------------------
SERIES = (  # (quantity, colour, label)
    ("the locker probe's accuracy", C["control"], "locker probe accuracy"),
    ("position answers under the whole change", C["address"], "position answers (whole change)"),
    ("lookup: switches blocked beyond random without the J++ part", C["lookup"], "lookup: switches blocked without the J++ part, beyond random"),
)


def _depth_panel(ax, m: str, first: bool, fs: float) -> None:
    depth, hol = DEPTH[m], D.hollow(m, True)
    layers = _layers(m, "fig06", r"47\.8, layer (\d+): the locker probe's accuracy")
    gated = {la: D.s(m, f"47.8, layer {la}: lookup switches under the whole change", "fig06")[0] >= GATE for la in layers}
    _axis_x(ax, depth, 1.05)
    ax.set_xlim(-0.04, 1.05)
    ax.set_ylim(-0.15, 1.08)
    ax.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    ax.axhline(0, color="#999999", lw=0.8, zorder=1)
    ax.tick_params(labelsize=fs)
    ax.xaxis.label.set_fontsize(fs)
    if fs < FS:
        ax.set_xlabel("share of the depth")
    ax.set_title(NAME[m] + (" (full grid)" if m == "qwen3.6-27b" else "") 
, fontsize=fs + (2 if fs >= FS else 0), weight="bold", loc="left", pad=56)
    for q, col, _ in SERIES:
        pts = [(la, D.s(m, f"47.8, layer {la}: {q}", "fig06")) for la in layers]
        pts = [(la, v) for la, v in pts if v is not None]
        on = [(la / depth, v) for la, v in pts if gated[la]]
        off = on[-1:] + [(la / depth, v) for la, v in pts if not gated[la]]
        if on:
            ax.plot([x for x, _ in on], [v[0] for _, v in on], color=col, lw=2.2, zorder=3)
        if len(off) > 1:
            ax.plot([x for x, _ in off], [v[0] for _, v in off], color=col, lw=1.6, alpha=0.3, zorder=2)
        for x, v in on:
            ax.plot([x, x], [v[1], v[2]], color=col, lw=1.4, alpha=0.8, zorder=3)
            ax.plot([x], [v[0]], "o", color=col, ms=6.5, mfc="white" if hol else col, mew=1.5, zorder=4)
    for key, col, word in (("l_probe", C["control"], "address readable"), ("l_P", C["address"], "position answers begin")):
        layer = D.s(m, f"47.8: {key}", "fig06")[0]
        x = layer / depth
        ax.text(x, 1.0, "▼", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=fs + 2, color=col, clip_on=False)
        ax.text(x, 1.12, f"L{layer:.0f}", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=fs, color=col if col != C["control"] else MUTED, clip_on=False)
    if first:
        ax.set_ylabel("share\n(0-1)", fontsize=fs, rotation=0, ha="right", va="center", labelpad=8)


def _depth_fig(models: tuple[str, ...], name: str, fs: float) -> None:
    fig, axes = plt.subplots(1, len(models), figsize=(W, H), sharey=True)
    fig.subplots_adjust(left=0.1 if len(models) == 3 else 0.09, right=0.995, top=1 - 1.85 / H, bottom=1.1 / H, wspace=0.12 if len(models) == 3 else 0.14)
    for k, (ax, m) in enumerate(zip(axes, models, strict=True)):
        _depth_panel(ax, m, k == 0, fs)
    hollow = any(D.hollow(m, True) for m in models)
    rows = [[("●", C["control"], "normal"), (" locker probe accuracy      ", MUTED, "normal"), ("●", C["address"], "normal"), (" position answers (whole change)      ", MUTED, "normal"),
             ("●", C["lookup"], "normal"), (" lookup: blocked without the J++ part, beyond random", MUTED, "normal")],
            [("▼", C["control"], "normal"), (" address readable (probe ≥ 0.80)      ", MUTED, "normal"), ("▼", C["address"], "normal"),
             (" position answers begin (≥ 0.20)      faded: whole change < 0.30      whiskers: 95%", MUTED, "normal")]]
    if hollow:
        rows[1] += [("      ○", INK, "normal"), (" post hoc", MUTED, "normal")]
    _key(fig, rows, 1 - 0.22 / H)
    _save(fig, name)


def f_depth_curves() -> None:
    _depth_fig(("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"), "f13b_depth_curves", FS)


def f_depth_curves_all() -> None:
    _depth_fig(tuple(DEPTH), "f13c_depth_curves_all", FS - 0.5)
