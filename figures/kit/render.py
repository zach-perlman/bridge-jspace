"""Render a Figure spec for a target (slide / readme): lay out its panels in a row, draw each component with the
target's theme, lint, save PNG + SVG, and collect the caption. All drawing lives here; specs and themes never draw."""

from __future__ import annotations

import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from figures.kit import lint
from figures.kit.data import NAMES, REPO
from figures.kit.spec import Bars, Curves, Figure, Image, Multiples, Stacked
from figures.kit.theme import Theme


def _setup(t: Theme) -> None:
    plt.rcParams.update({"font.size": t.tick, "axes.labelsize": t.axis, "xtick.labelsize": t.tick,
                         "ytick.labelsize": t.tick, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none"})  # fmt: skip


def _span(ax) -> float:
    lo, hi = ax.get_ylim()
    return hi - lo


def _rules(ax, rules, t: Theme) -> None:
    for r in rules:
        ax.axhline(r.y, color=t.c("rule"), zorder=1, **t.rule_style)
        ax.text(1.0, r.y, f" {r.word}", transform=ax.get_yaxis_transform(), ha="left", va="center",
                fontsize=t.value, color=t.c("rule"), clip_on=False)  # fmt: skip


def _band(ax, band, t: Theme) -> None:
    if band:
        ax.axhspan(band[0], band[1], color=t.c("control"), alpha=t.band_alpha, lw=0, zorder=0)


def _bar(ax, x, cell, color, width, hollow, t: Theme, fmt, control=False, value=True):
    v, lo, hi = cell[0], cell[1], cell[2]
    w = width * (t.control_scale if control else 1)
    col = t.c("control") if control else t.c(color)
    ax.bar(x, v, w, color="white" if hollow else col, edgecolor=col, lw=1.6, zorder=2)
    if not control and lo is not None and hi is not None:
        ax.vlines(x, lo, hi, zorder=3, **t.whisker)
    if value and not control:
        top = max(v, hi if hi is not None else v, 0)
        ax.text(x, top + 0.012 * _span(ax), fmt.format(v), ha="center", va="bottom", fontsize=t.value, zorder=4)


def bars(ax, p: Bars, t: Theme) -> None:
    ax.set_ylim(*p.ylim)
    keys = [k for k, _ in p.cats]
    n = len(p.series)
    width = t.bar_width / max(n, 1)
    for j, se in enumerate(p.series):
        for i, k in enumerate(keys):
            if k not in se.cells or se.cells[k] is None:
                continue
            xpos = i + (j - (n - 1) / 2) * width
            _bar(ax, xpos, se.cells[k], se.color, width * 0.9, k in se.hollow, t, p.fmt, se.control)
            if se.label and not se.control and k == next(kk for kk in keys if kk in se.cells):
                v = se.cells[k][0]
                inside = v > 0.2 * _span(ax) and k not in se.hollow
                ax.text(xpos, v / 2 if inside else max(v, 0) + 0.1 * _span(ax), se.label, rotation=90, ha="center",
                        va="center", fontsize=t.label, color="white" if inside else t.c(se.color), zorder=5)  # fmt: skip
    for i, k in enumerate(keys):
        if p.ticks and p.ticks.get(k) is not None:
            ax.plot([i - 0.42, i + 0.42], [p.ticks[k]] * 2, color=t.c("rule"), lw=2.2, zorder=4)
        if p.gap and k in p.gap:
            ax.text(i, p.ylim[1], p.fmt.format(p.gap[k]), ha="center", va="top", fontsize=t.value + 1, weight="bold")
        if p.under and k in p.under:
            ax.text(i, -0.16 - 0.04 * (p.rotate > 0), "\n".join(textwrap.wrap(p.under[k], 12)), ha="center", va="top",
                    fontsize=t.value, color=t.c("rule"), transform=ax.get_xaxis_transform())  # fmt: skip
    if p.divider is not None:
        ax.axvline(p.divider, color=t.c("control"), lw=1)
    _band(ax, p.band, t)
    _rules(ax, p.rules, t)
    ax.axhline(0, color="black", lw=0.6, zorder=1)
    ax.set_xticks(range(len(p.cats)), [nm for _, nm in p.cats], rotation=p.rotate, ha="right" if p.rotate else "center")
    ax.set_ylabel(p.ylabel)


def multiples(axes, p: Multiples, t: Theme) -> None:
    for ax, (m, name) in zip(axes, p.models, strict=True):
        ax.set_ylim(*p.ylim)
        for i, c in enumerate(p.conds):
            cell = p.data.get(m, {}).get(c)
            if cell is None:
                continue
            control = p.colors[c] == "control"
            _bar(ax, i, cell, p.colors[c], 0.7, m in p.hollow and not control, t, p.fmt, control)
        ax.axhline(0, color="black", lw=0.6)
        _rules(ax, p.rules if ax is axes[-1] else [], t)
        for r in p.rules if ax is not axes[-1] else []:
            ax.axhline(r.y, color=t.c("rule"), zorder=1, **t.rule_style)
        ax.set_xticks(range(len(p.conds)), p.conds)
        ax.text(0.5, 1.0, name, transform=ax.transAxes, ha="center", va="bottom", fontsize=t.label)
    axes[0].set_ylabel(p.ylabel)
    for ax in axes[1:]:
        ax.tick_params(labelleft=False)


def stacked(ax, p: Stacked, t: Theme) -> None:
    assert len(p.segments) <= 4, "Stacked: at most four segments"
    for i, (k, _) in enumerate(p.cats):
        bottom = 0.0
        for label, color, vals in p.segments:
            v = vals.get(k)
            if v is None:
                continue
            h = k in p.hollow
            ax.bar(i, v, 0.65, bottom=bottom, color="white" if h else t.c(color), edgecolor=t.c(color), lw=1.6)
            if v >= 0.08:
                ax.text(i, bottom + v / 2, f"{v:.2f}", ha="center", va="center", fontsize=t.value,
                        color=t.c(color) if h else "white")  # fmt: skip
            if i == 0 and v >= 0.08:
                ax.text(i - 0.4, bottom + v / 2, label, ha="right", va="center", fontsize=t.label, color=t.c(color))
            bottom += v
    ax.set_xticks(range(len(p.cats)), [nm for _, nm in p.cats], rotation=p.rotate, ha="right" if p.rotate else "center")
    ax.set_xlim(-1.7, len(p.cats) - 0.5)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel(p.ylabel)


def curves(axes, p: Curves, t: Theme) -> None:
    for ax, (name, lines) in zip(axes, p.panels, strict=True):
        ax.set_ylim(*p.ylim)
        if p.xlim:
            ax.set_xlim(*p.xlim)
        if p.xticks:
            ax.set_xticks(p.xticks)
        ends = []
        for ln in lines:
            col = t.c(ln.color)
            ax.plot(ln.xs, ln.ys, color=col, lw=1.5 if ln.thin else 2.3, alpha=0.75 if ln.thin else 1)
            if ln.lo is not None and ln.hi is not None:
                ax.fill_between(ln.xs, ln.lo, ln.hi, color=col, alpha=0.25, lw=0)
            for xv, yv in (ln.mark or {}).items():
                ax.plot(xv, yv, "o", ms=8, color=col)
                ax.text(xv, yv + 0.05 * _span(ax), f"{yv:.2f}", ha="center", fontsize=t.value, color=col)
            if ln.values:
                for xv, yv in zip(ln.xs, ln.ys, strict=True):
                    ax.text(xv, yv + 0.04 * _span(ax), f"{yv:.2f}", ha="center", fontsize=t.value, color=col)
            if ln.label:
                ends.append([ln.xs[-1], ln.ys[-1], ln.label, col])
        ends.sort(key=lambda e: e[1])
        for k in range(1, len(ends)):
            ends[k][1] = max(ends[k][1], ends[k - 1][1] + 0.07 * _span(ax))
        for xv, yv, label, col in ends:
            ax.text(xv, yv, f" {label}", fontsize=t.label, color=col, va="center", ha="left", clip_on=False)
        _band(ax, p.band, t)
        if p.vline:
            ax.axvline(p.vline[0], color=t.c("rule"), lw=1, **{k: v for k, v in t.rule_style.items() if k == "ls"})
        _rules(ax, p.rules if ax is axes[-1] else [], t)
        if name:
            ax.text(0.5, 1.0, name, transform=ax.transAxes, ha="center", va="bottom", fontsize=t.label)
    axes[len(axes) // 2].set_xlabel(p.xlabel)  # one x title per row of panels
    axes[0].set_ylabel(p.ylabel)
    for ax in axes[1:]:
        ax.tick_params(labelleft=False)


def image(ax, p: Image, t: Theme) -> None:
    img = mpimg.imread(REPO / p.path)
    if p.crop:
        h = img.shape[0]
        img = img[int(p.crop[0] * h) : int(p.crop[1] * h)]
    ax.imshow(img)
    ax.set_axis_off()


DRAW = {Bars: bars, Multiples: multiples, Stacked: stacked, Curves: curves, Image: image}


def _n_axes(p) -> int:
    return len(p.models) if isinstance(p, Multiples) else len(p.panels) if isinstance(p, Curves) else 1


def render(spec: Figure, t: Theme, out_dir, lint_on: bool = True) -> list[str]:
    """Draw, lint and save one figure; return the lint problems (saved anyway only when there are none)."""
    _setup(t)
    counts = [_n_axes(p) for p in spec.panels]
    widths = []
    for p, n in zip(spec.panels, counts, strict=True):
        w = (spec.widths or [1] * len(spec.panels))[spec.panels.index(p)]
        widths += [w / n] * n
    fig, axes = plt.subplots(1, sum(counts), figsize=t.sizes[spec.size], dpi=t.dpi, constrained_layout=True,
                             gridspec_kw={"width_ratios": widths}, squeeze=False)  # fmt: skip
    axes = list(axes[0])
    k = 0
    for p, n in zip(spec.panels, counts, strict=True):
        group = axes[k : k + n]
        if n > 1:
            for ax in group[1:]:
                ax.sharey(group[0])
        DRAW[type(p)](group if type(p) in (Multiples, Curves) else group[0], p, t)
        k += n
    if t.title:
        fig.suptitle(spec.claim, x=0.01, ha="left", fontsize=t.title_size, weight="bold")
    problems = (
        lint.problems(fig, spec.id, NAMES, titles_ok=t.title)
        if lint_on and not all(isinstance(p, Image) for p in spec.panels)
        else []
    )
    if not problems:
        out_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_dir / f"{spec.id}.png", dpi=t.dpi, facecolor="white")
        fig.savefig(out_dir / f"{spec.id}.svg", facecolor="white")
    plt.close(fig)
    return problems
