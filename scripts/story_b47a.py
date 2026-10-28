"""README figures for batch 47 (part a): one figure per test, each drawn from that test's verdict folder (the json its
`verdict` stage writes) in story_style's look, every plotted number recorded for figures/story/data.csv.

  47.1  x47_atoms.py   x47_1-<UTC>/x47_1.json         Fig. 11: without the J++ lens's directions 26-100; README
                                                      Figs. 5b (the main test's parts) and 5d (the routes test's slices)
  47.5  x47_zero.py    x47_5-<UTC>/x47_5.json         Fig. 12: the J++ part zeroed at one layer
  47.3  x47_cue.py     x47_3-<UTC>/x47_3.json         Fig. 13: a described bridge
  47.2  x47_six.py     x47_2-<UTC>/x47_2.json         Fig. 14: six lockers, one shift vector
  47.13 x47_errors.py  x47_13-<UTC>/x47_errors.json   Fig. 15: the address probe on the lookup's errors

The title is the claim, built from the verdict's labels so it reads true for any outcome (pass `title` once Dan has
worded it); the rule's bars are thin labelled lines; every cell is fixed in advance (filled marks). Tested on planted
verdicts (tests/test_story_b47a.py); readme_story_figures draws them once their verdict folders are named there.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import blended_transform_factory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_style as S
from scripts import x0_necessity as X

TARGETS = tuple((t, m) for t, m, _ in S.MODELS if m != "122b")  # 9B, 27B, Muse
BAR = "#555555"  # the rule's bars
NOTE = ""  # put before every subtitle (the planted previews set "PLANTED data, not a result. ")
WRAP = 104  # subtitle characters per line at 11 pt in the 8.8 in column
ROW_IN, BOTTOM_IN = 0.78, 0.80  # inches per model row; under the panels (two-line axis labels)


def fig_id(out_name: str) -> str:
    return out_name.split("_")[0]


def by_target(models: list[dict]) -> dict[str, dict]:
    return {m["target"]: m for m in models if m.get("target")}


def iv(v, scale: float = 1.0) -> tuple[float, float, float] | None:
    """[point, lo, hi] scaled; None for a missing or nan point."""
    if not v or v[0] is None or v[0] != v[0]:
        return None
    return (scale * v[0], scale * v[1], scale * v[2])


def majority(n_tested: int) -> int:
    """Models a batch-wide title needs: 2 of 3, or every tested model when fewer are in."""
    return min(2, max(1, n_tested))


def frame(title: str, sub: str, ratios: tuple[float, ...], body_in: float, legend=None, left: float = 0.19,
          bottom_in: float = BOTTOM_IN, sharey: bool = True, wrap: bool = True):  # fmt: skip
    """The figure: the claim, the subtitle (NOTE first; wrapped, or with wrap False one line that story_style.title
    shrinks to fit, v6), an optional legend (handles, labels[, ncol]) under it, and panels side by side with body_in
    inches of plot; the height follows from them."""
    # "J++ part" and "J++ lens" stay on one line (the glossary's names), hyphenated words whole
    keep = (NOTE + sub).replace("J++ ", "J++\u00a0")
    lines = [x.replace("\u00a0", " ") for x in textwrap.wrap(keep, WRAP if wrap else 10**4, break_on_hyphens=False)]
    top_in = 0.42 + 0.20 * len(lines) + 0.14
    legend_y = top_in
    if legend:
        top_in += 0.34
    top_in += 0.40  # the panel titles
    h = top_in + body_in + bottom_in
    plt = S.setup()
    fig, axes = plt.subplots(1, len(ratios), figsize=(S.WIDTH, h), sharey=sharey, squeeze=False,
                             gridspec_kw={"width_ratios": ratios})  # fmt: skip
    fig.subplots_adjust(left=left, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.10)
    S.title(fig, title, "\n".join(lines), limit=92)
    if legend:
        F.legend(fig, legend[0], legend[1], 1 - legend_y / h, ncol=legend[2] if len(legend) > 2 else None)
    return fig, list(axes[0])


def row_panels(axes, n_rows: int) -> None:
    """One row per model; the band above row 0 holds the bars' labels."""
    for ax in axes:
        ax.set_ylim(-n_rows + 0.45, 1.0)
        ax.tick_params(axis="y", length=0)


def panel_title(ax, text: str) -> None:
    ax.set_title(text, fontsize=S.FONT, weight="bold", loc="left")


def bar(ax, x: float, text: str, side: str = "right") -> None:
    """The rule's bar: a thin dashed line, its label in the panel's top band beside the line."""
    ax.axvline(x, color=BAR, lw=1.1, ls=(0, (4, 3)), zorder=1.8)
    tr = blended_transform_factory(ax.transData, ax.transAxes)
    dx = 0.015 * (ax.get_xlim()[1] - ax.get_xlim()[0]) * (1 if side == "right" else -1)
    ax.text(x + dx, 0.985, text, transform=tr, ha="left" if side == "right" else "right", va="top", color=BAR)


def pct_axis(ax, label: str, lim: tuple[float, float] = (-20, 100), ticks=(0, 50, 100)) -> None:
    """A share axis in % (docs/glossary.md); data.csv keeps the fractions."""
    ax.set_xlim(*lim)
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.set_xticks(list(ticks), [str(t) for t in ticks])
    ax.grid(axis="x", color="#eeeeee")
    ax.set_axisbelow(True)
    ax.set_xlabel(label)


def share_axis(ax, label: str, ticks=(0, 0.5, 1)) -> None:
    """v6: a share axis on [0, 1] (a little air at both ends)."""
    ax.set_xlim(-0.04, 1.06)
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.set_xticks(list(ticks), [f"{t:g}" for t in ticks])
    ax.grid(axis="x", color="#eeeeee")
    ax.set_axisbelow(True)
    ax.set_xlabel(label)


def text_column(ax, title: str) -> None:
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    panel_title(ax, title)


def status_text(ax, y: float, text: str) -> None:
    """A cell with no number (pending, not tested), centred in the panel's row."""
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(0.5, y, text, transform=tr, ha="center", va="center", color=S.COL["muted"], zorder=4,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})  # fmt: skip


def model_labels(ax, rows: list[tuple[str, str]]) -> None:
    """Row labels: the model's name and, below it, its n."""
    ax.set_yticks([-i for i in range(len(rows))], [f"{F.name_of(m)}\n{n}" if n else F.name_of(m) for m, n in rows])


def readers_legend() -> tuple[list, list[str]]:
    return F.reader_handles(S.setup())


# ---- 47.1: directions 26-100 ----------------------------------------------------------------------------------------

ATOMS_LABEL = {"(a) beyond the 25": "beyond the 25", "(b) continuum": "a continuum",
               "(c) outside the lens": "outside the lens", "none of (a)-(c)": "none of the three",
               "can't tell": "can't tell", "not tested": "not tested (gate)", "pending": "pending"}  # fmt: skip


def atoms_title(v: dict) -> str:
    labels = [m["label"] for m in v["models"] if m["status"] == "tested"]
    if v["batch"]["a_holds"] == "holds":
        return "The lookup's identity route sits in lens directions 26–100, not the recall's 25"
    if not labels:
        return "Lens directions 26–100: no model tested yet"
    if labels.count("(c) outside the lens") >= majority(len(labels)):
        return "The lookup's identity route lies outside the lens, not in directions 26–100"
    if labels.count("(b) continuum") >= majority(len(labels)):
        return "Lens directions 26–100 matter to both readers: a continuum, no split"
    return "Lens directions 26–100: no single reading holds across models"


def build_atoms(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.1 (x47_atoms verdict, x47_1.json): one row per model (9B, 27B, Muse). (a) routes test, another item moved:
    the lookup's identity answers lost without directions 26-100 beyond the random part (same size), the rule's bars at
    30 and 10; (b) main test: the recall's and the lookup's extra loss without them (bars 0.10 and 0.20); (c) the
    rule's reading per model."""
    src = verdict_dir / "x47_1.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    fig, (a, b, c) = frame(
        title or atoms_title(v),
        "Taken out of the change at the bridge word: the J++ lens's directions 26–100, the recall's 25 kept, against a "
        "random part (same size). 95% intervals, all fixed in advance. Extra loss (0–1): switches lost without the "
        "directions minus those lost without the random part.",
        (1, 1, 0.55), ROW_IN * len(TARGETS), legend=readers_legend())  # fmt: skip
    row_panels((a, b, c), len(TARGETS))
    pct_axis(a, "identity answers lost\nbeyond random (%)")
    panel_title(a, "(a) routes test: lookup")
    S.extra_axis(b, label=False)
    b.set_xlabel("extra loss")
    panel_title(b, "(b) main test")
    text_column(c, "reading")
    bar(a, 30, "≥ 30")
    bar(a, 10, "< 10", side="left")
    bar(b, 0.10, "≤ 0.10", side="left")
    bar(b, 0.20, "≥ 0.20")
    rows = []
    for i, (target, m) in enumerate(TARGETS):
        y, mod = -i, by.get(target, {"status": "pending", "label": "pending"})
        routes = mod.get("routes") or {}
        rows.append((m, f"n = {routes['n']}" if routes.get("n") else ""))
        reading = str(ATOMS_LABEL.get(mod["label"], mod["label"]))
        c.text(0.04, y, reading, va="center")
        S.record(fid, target, "47.1: the rule's reading", mod["label"], source=source)
        if mod["status"] != "tested":
            for ax in (a, b):
                status_text(ax, y, reading)
            continue
        fall = iv(mod.get("identity_fall"), 100)
        if fall:
            S.dot(a, 0, y, fall, S.COL["identity"], size=8)
            S.record(fid, target, "47.1: identity answers lost without directions 26-100 beyond random (routes test, "
                     "lookup)", *mod["identity_fall"], n=routes.get("n"), source=source)  # fmt: skip
        readers = (mod.get("main") or {}).get("readers", {})
        drawn = False
        for w, dy, col in ((X.RECALL, 0.16, S.COL["recall"]), (X.LOOKUP, -0.16, S.COL["lookup"])):
            cell = readers.get(w, {}).get("26-100")
            ex = iv(cell["excess"]) if cell else None
            if cell is None or ex is None:
                continue
            drawn = True
            S.dot(b, 0, y + dy, ex, col, size=8)
            S.record(fid, target, f"47.1: {'recall' if w == X.RECALL else 'lookup'}'s extra loss without directions "
                     "26-100 (main test)", *cell["excess"], n=cell.get("n"), source=source)  # fmt: skip
        if not drawn:
            status_text(b, y, "no main-test cell")
    model_labels(a, rows)
    S.save(fig, out_name)
    return out_name


# E3 (v6): Fig. 2's parts and 47.1's directions 26-100 on one extra-loss axis; (key, row label, fixed in advance)
E3_PARTS = (("jpp", "J++ part\n(lens\ndirections\n1–25)", False), ("26-100", "lens directions\n26–100", True),
            ("pca_eq", "PCA directions\n(same size)", False), ("wu", "logit-lens\ndirections", True),
            ("rand", "random lens\ndirections", True))  # fmt: skip


def build_identity(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """Fig. 5b (v6; Fig. 2 and 47.1 merged; the inset left for Fig. 5d, Dan's 5b / 5d brief, 28 Oct ~20:30): the main
    test on one extra-loss axis, one group of rows per part of the change taken out at the bridge word (the J++ part,
    lens directions 26-100, PCA directions of the J++ part's size, logit-lens and random lens directions), one row per
    model (9B, 27B, Muse) with the lookup's and the recall's extra loss and their 95% intervals (open: the parts runs on
    one-pick scenes, after the data; filled: the main test, fixed in advance). The 122B's parts:
    figures/supp/s02_parts_all."""
    src = verdict_dir / "x47_1.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    parts = F.parts_cells()
    h = 6.9
    plt = S.setup()
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, title or "Only the J++ part costs the recall; no single part costs the lookup",
            "The main test; extra loss without each part of the change, beyond a random part of the same size")  # fmt: skip
    ax = fig.add_axes((0.30, 0.6 / h, 0.66, 1 - 1.45 / h - 0.6 / h))
    S.extra_axis(ax, label=False)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
    ax.grid(axis="x", color="#eeeeee")
    ax.set_xlabel("extra loss")
    ticks, labels, ns = [], [], set()
    y = 0.0
    tr = blended_transform_factory(fig.transFigure, ax.transData)
    for key, label, fixed in E3_PARTS:
        top = y
        for target, m in TARGETS:
            got: dict[str, tuple[tuple[float, float, float], int | None]] = {}
            if key == "26-100":
                readers = ((by.get(target) or {}).get("main") or {}).get("readers", {})
                for w in (X.LOOKUP, X.RECALL):
                    cell = readers.get(w, {}).get("26-100")
                    ex = iv(cell["excess"]) if cell else None
                    if cell and ex is not None:
                        got[w] = (ex, cell.get("n"))
                quant = {X.RECALL: "47.1: recall's extra loss without directions 26-100 (main test)",
                         X.LOOKUP: "47.1: lookup's extra loss without directions 26-100 (main test)"}  # fmt: skip
                cell_src = source
            else:
                c = parts[m].get(key) or {}
                for w, r in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
                    if r in c:
                        got[w] = ((c[r][0], c[r][1], c[r][2]), c.get("n"))
                name = next(t for k, t in F.SPEC_PARTS if k == key)
                quant = {X.RECALL: f"{name}: recall extra loss", X.LOOKUP: f"{name}: lookup extra loss"}
                cell_src = c.get("source", "")
            ticks.append(y)
            labels.append(F.name_of(m) if key == E3_PARTS[0][0] else F.SHORT[m])  # full names in the first group
            if not got:
                status_text(ax, y, "not run")
            for w, dy, col in ((X.LOOKUP, 0.15, S.COL["lookup"]), (X.RECALL, -0.15, S.COL["recall"])):
                if w not in got:
                    continue
                val, n = got[w]
                S.dot(ax, 0, y + dy, val, col, "fixed" if fixed else "after", size=7)
                S.record(fid, target, quant[w], *val, n=n, source=cell_src)
                if n:
                    ns.add(int(n))
            y -= 0.62
        ax.text(0.01, (top + y + 0.62) / 2, label, transform=tr, va="center", fontsize=S.FONT, weight="bold",
                linespacing=1.0)  # fmt: skip
        y -= 0.42
        ax.axhline(y + 0.21 + 0.0, color="#dddddd", lw=0.8, zorder=0)
    ax.lines[-1].remove()  # no divider under the last group
    ax.set_yticks(ticks, labels)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(y + 0.42 - 0.4, 0.45)
    ax.text(-0.05, y + 0.42 - 0.33, "not needed", ha="center", va="bottom", color=S.COL["muted"], fontsize=S.FONT - 1)
    n_txt = "–".join(str(n) for n in sorted(ns)) if ns else "–"
    ax.text(1.0, 1.005, f"n = {n_txt} per model  {S.STATUS_GLYPH['fixed']} {S.STATUS_GLYPH['after']}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=S.FONT, color=S.COL["muted"])  # fmt: skip
    hs, ls = F.reader_handles(plt)
    F.legend(fig, hs, ls, 1 - 0.62 / h, ncol=2)
    S.save(fig, out_name)
    return out_name


# ---- Fig. 5d (E3): the routes test's lens slices, both routes -------------------------------------------------------

# Dan's Fig. 5b / 5d brief (28 Oct ~20:30). (47.1's fall label, the part's arm in x47_atoms.PARTS, the panel title)
ROUTE_SLICES = (("1-25", "jpp", "lens directions 1–25"), ("26-100", "jpp26_100", "26–100"),
                ("1-100", "jpp100", "1–100 (both)"))  # fmt: skip
SPLIT_ROUTES = (("identity", "identity route"), ("position", "position route"))
REDUNDANT_MODEL, REDUNDANT_SLICE = "qwen3.6-27b", "1-100"  # the bar Dan's brief labels "redundant copies"
SLICE_XLIM = (-0.42, 0.88)


def route_costs(rows: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """One 47.1 routes run's per-item rows, read as x47_atoms.routes_numbers reads them (the C2 lookup rows, the scenes
    every arm holds, the cluster bootstrap over bridge items on the same draws): per (slice, route) the fall beyond the
    random part (share without the random part minus share without the slice; its point checks the verdict) and what
    the random part itself costs the route (share under the whole change minus share without the random part) with its
    95% interval."""
    from scripts import x47_atoms as A

    lk = [r for r in rows if r["condition"] == "C2" and r["reader"] == X.LOOKUP]
    arms = [a for a in A.ROUTE_ARMS if any(r["arm"] == a for r in lk)]
    by = {a: {r["scene"]: r for r in lk if r["arm"] == a} for a in arms}
    scenes = sorted(set.intersection(*(set(v) for v in by.values())))
    ents = [by["whole"][s]["entity"] for s in scenes]
    sw = {f"{rt}|{a}": [int(by[a][s]["route"] == rt) for s in scenes] for a in arms for rt, _ in SPLIT_ROUTES}
    rr = X.resampled_rates(sw, ents, n_boot)
    pt = {k: float(np.mean(v)) for k, v in sw.items()}
    cells = {}
    for label, p, _ in ROUTE_SLICES:
        for rt, _ in SPLIT_ROUTES:
            whole, part, rand = (f"{rt}|{a}" for a in ("whole", f"no_{p}", f"no_{p}_rand"))
            cells[(label, rt)] = {"fall": pt[rand] - pt[part],
                                  "random": (pt[whole] - pt[rand], *X.interval(rr[whole] - rr[rand]))}  # fmt: skip
    return {"n": len(scenes), "cells": cells}


def value_label(ax, y: float, v: float, col: str) -> None:
    """The point's value in a column at the panel's right edge, clear of the marks and the grey bands."""
    ax.text(SLICE_XLIM[1] - 0.02, y, f"{v:.2f}".replace("-", "−"), ha="right", va="center", fontsize=S.FONT - 1,
            color=col, zorder=5)  # fmt: skip


def build_routes_lens(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """Fig. 5d (E3; Dan's 5b / 5d brief, 28 Oct ~20:30): the routes test (47.1, fixed in advance), one panel per lens
    slice taken out of the change (directions 1-25, 26-100, 1-100), two rows per model (9B, 27B, Muse): the lookup's
    identity-route and position-route answers lost beyond a random part of the same share, with 95% intervals (the
    verdict's routes falls); behind each row, as a grey band, what that random part itself costs the route (whole change
    minus without it, 95% interval; recomputed from the routes run's per-item rows, whose falls are checked against the
    verdict first); the 0.10 band; the 27B's 1-100 identity bar labelled as redundant copies, with its numbers. At the
    top right, Fig. 5's drawing of the routes test, small (readme_story_figures.routes_drawing), for the routes'
    colours."""
    src = verdict_dir / "x47_1.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    models = [(t, m) for t, m in TARGETS if ((by.get(t) or {}).get("routes") or {}).get("falls")]
    omitted = [F.SHORT[m] for t, m in TARGETS if (t, m) not in models]
    gap = 3.4  # rows from one model's identity row to the next's (two rows and room for the 27B's label)
    ys = {t: -k * gap for k, (t, _) in enumerate(models)}
    row_in, top_in, bottom_in = 0.34, 2.0, 0.85 + 0.2 * bool(omitted)
    body = (gap * (len(models) - 1) + 1 + 1.2) * row_in
    h = top_in + body + bottom_in
    plt = S.setup()
    fig, axes = plt.subplots(1, len(ROUTE_SLICES), figsize=(S.WIDTH, h), sharey=True, sharex=True)
    fig.subplots_adjust(left=0.31, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.08)
    S.title(fig, title or "The lookup's identity route runs outside the lens; the position route never touches it",
            "Identity route: the answer names the item's own locker; position route: the locker now at the item's old "
            "place (routes test, E5)", limit=92)  # fmt: skip
    costs, ns = {}, set()
    for t, _ in models:
        run = (by[t].get("runs") or [None])[0]
        path = F.pins.RESULTS_DIR / "x6_routes" / run / "outcomes.jsonl"
        costs[t] = (route_costs(X.read_jsonl(path)), F.rel(path))
        ns.add(by[t]["routes"]["n"])
    for ax, (label, _, name) in zip(axes, ROUTE_SLICES, strict=True):
        ax.set_xlim(*SLICE_XLIM)
        ax.axvspan(SLICE_XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1)
        ax.set_xticks([-0.25, 0, 0.25, 0.5, 0.75], ["", "0", "", "0.5", ""])
        ax.grid(axis="x", color="#eeeeee")
        ax.tick_params(axis="y", length=0)
        ax.set_title(name, fontsize=12, weight="bold", loc="left")
        for t, _ in models:
            r = by[t]["routes"]
            split, cost_src = costs[t]
            for i, (rt, words) in enumerate(SPLIT_ROUTES):
                y, col = ys[t] - i, S.MARK_COL["identity" if rt == "identity" else "address"]
                f = iv(r["falls"][label][rt])
                c = split["cells"][(label, rt)]
                # the per-item rows reproduce the verdict's fall before anything is drawn
                assert np.isclose(c["fall"], f[0]), (t, label, rt, c["fall"], f[0])
                lo, hi = c["random"][1], c["random"][2]
                ax.fill_between([lo, hi], [y - 0.24] * 2, [y + 0.24] * 2, color=S.MARK_COL["null"], alpha=0.6, lw=0,
                                zorder=1)  # fmt: skip
                ax.plot([c["random"][0]] * 2, [y - 0.24, y + 0.24], color="#8a8a8a", lw=1.0, zorder=1.5)
                if t == models[0][0] and i == 0:  # Dan (21:50): every panel names the grey band, on its top row
                    ax.text((lo + hi) / 2, y + 0.3, "random", ha="center", va="bottom", fontsize=S.LABEL_PT,
                            color=S.COL["muted"], zorder=5)  # fmt: skip
                ax.plot([f[1], f[2]], [y, y], color=col, lw=1.6, zorder=3, solid_capstyle="butt")
                ax.plot([f[0]], [y], S.MARK["remove"], ms=7, color=col, zorder=4)
                value_label(ax, y, f[0], col)
                S.record(fid, t, f"47.1: {words}: answers lost beyond random without lens directions {label}", *f,
                         n=r["n"], source=source)  # fmt: skip
                S.record(fid, t, f"47.1: {words}: answers a random part of the same share as lens directions {label} "
                         "costs (whole change minus without it)", *c["random"], n=split["n"],
                         source=cost_src)  # fmt: skip
            if t == REDUNDANT_MODEL and label == REDUNDANT_SLICE:
                # Dan's label, reworded: "alone" is not a figure word (docs/glossary.md), and 1-25 by itself costs
                # the 27B more than "little"; the numbers say what "redundant" rests on (both > the sum of each)
                fall = {k: r["falls"][k]["identity"][0] for k in ("1-25", "26-100", "1-100")}
                ax.text(SLICE_XLIM[0] + 0.03, ys[t] - 1.45, f"redundant copies:\neach slice {fall['1-25']:.2f} / "
                        f"{fall['26-100']:.2f},\nboth together {fall['1-100']:.2f}", ha="left", va="top",
                        fontsize=S.FONT - 1, color=S.MARK_COL["identity"], linespacing=1.1, zorder=5)  # fmt: skip
                ax.annotate("", (fall["1-100"], ys[t] - 0.22), (0.5 * (SLICE_XLIM[0] + fall["1-100"]), ys[t] - 1.4),
                            arrowprops={"arrowstyle": "-", "color": S.MARK_COL["identity"], "lw": 0.8, "shrinkA": 0,
                                        "shrinkB": 4})  # fmt: skip
    # the README's "the position route never loses": its largest fall over every model and slice
    worst = max(((by[t]["routes"]["falls"][k]["position"], t, k) for t, _ in models for k, _, _ in ROUTE_SLICES),
                key=lambda x: x[0][0], default=None)  # fmt: skip
    if worst:
        S.record(fid, "", "47.1: position route: the most answers lost beyond random, over the models and slices",
                 *worst[0], n=by[worst[1]]["routes"]["n"], source=source)  # fmt: skip
    a0 = axes[0]
    ticks = [ys[t] - i for t, _ in models for i in range(len(SPLIT_ROUTES))]
    a0.set_yticks(ticks, [w for _ in models for _, w in SPLIT_ROUTES])
    for lab, i in zip(a0.get_yticklabels(), range(len(ticks)), strict=True):
        lab.set_color(S.MARK_COL["identity" if i % 2 == 0 else "address"])
    a0.set_ylim(ys[models[-1][0]] - 1.6, 0.6)
    tr = blended_transform_factory(fig.transFigure, a0.transData)
    for t, m in models:
        a0.text(0.01, ys[t] - 0.5, F.NAMES[m].replace(" 30B", "\n30B"), transform=tr, ha="left", va="center",
                fontsize=S.FONT, weight="bold", linespacing=1.0)  # fmt: skip
    axes[1].set_xlabel("answers lost without the directions, beyond a random part (same size)")
    n_txt = ", ".join(str(n) for n in sorted(ns))
    axes[-1].text(1.0, 1.10, f"n = {n_txt} per model  {S.STATUS_GLYPH['fixed']}", transform=axes[-1].transAxes,
                  ha="right", va="bottom", fontsize=S.FONT - 1, color=S.COL["muted"])  # fmt: skip
    # the routes' colours from Fig. 5's drawing, small (Dan's Fig. 4 / 5 brief): blue the item's own locker, orange
    # the locker now at its old place; the row labels say the rest
    F.routes_drawing(S.setup(), S.inset(fig, (0.585, 1 - 1.5 / h, 0.39, 0.74 / h)), small=True)
    hs = [Patch(fc=S.MARK_COL["null"], alpha=0.6, ec="none"), Patch(fc=S.COL["band"], ec="none")]
    F.legend(fig, hs, ["what a random part (same size)\nitself costs", "the 0.10 bar"], 1 - 0.74 / h, ncol=1)
    if omitted:
        fig.text(0.01, 0.2 / h, f"Not run: {', '.join(omitted)}.", ha="left", va="bottom", fontsize=S.FONT - 1,
                 color=S.COL["muted"])  # fmt: skip
    S.save(fig, out_name)
    return out_name


# ---- 47.5: one-layer zeroing ----------------------------------------------------------------------------------------

ZERO_LABEL = {"followed, not needed at one layer": "followed", "needed": "needed",
              "neither (between the bars)": "between the bars", "not tested": "not tested (gate)", "pending": "pending"}  # fmt: skip


def zero_title(v: dict) -> str:
    labels = [m["label"] for m in v["models"] if m["status"] == "tested"]
    k = labels.count("needed")
    if v["batch"]["verb"] == "needs":
        return "The recall needs the J++ part at one layer, on all three models"
    if not labels:
        return "The J++ part zeroed at one layer: no model tested yet"
    if k == 0 and all(lab.startswith("followed") for lab in labels):
        return "The J++ part zeroed at one layer: the recall keeps its answers"
    return f"The J++ part zeroed at one layer: the recall needs it on {k} of {len(labels)} models"


def build_zero(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.5 (x47_zero verdict, x47_5.json): one row per model. On the changed prompt, at the bridge word at L, the
    J++ part's 25 directions taken out of the state (the reader's colour) or a random part (same size, grey): the
    changed prompt's answers kept (share, 0-1), (a) recall (the rule's bar at 0.8, "followed if above"; under each row
    the recall's answers lost beyond random, in pp), (b) lookup. n and the status glyph in each panel's corner; the
    rule's reading is recorded for data.csv, not drawn (v6 iteration 2)."""
    src = verdict_dir / "x47_5.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    grey = S.COL["control"]
    legend = ([Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=8),
               Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8),
               Line2D([], [], marker="o", ls="", color=grey, ms=8)],
              ["recall", "lookup", "a random part (same size)"])  # fmt: skip
    fig, (a, b) = frame(
        title or zero_title(v),
        "Main test; the J++ part's 25 directions, or a random part of the same size, taken out at the bridge word at "
        "one layer",
        (1, 1), ROW_IN * len(TARGETS), legend=legend, wrap=False)  # fmt: skip
    row_panels((a, b), len(TARGETS))
    for ax, name in ((a, "(a) recall"), (b, "(b) lookup")):
        share_axis(ax, "answers kept (share)")
        panel_title(ax, name)
        bar(ax, 0.8, "followed if above", side="left")
    rows, ns = [], []
    for i, (target, m) in enumerate(TARGETS):
        y, mod = -i, by.get(target, {"status": "pending", "label": "pending"})
        readers = mod.get("readers", {})
        rows.append((m, ""))
        if "recall" in readers:
            ns.append(str(readers["recall"]["n"]))
        reading = str(ZERO_LABEL.get(mod["label"], mod["label"]))
        S.record(fid, target, "47.5: the rule's reading (recall at L)", mod["label"], source=source)
        if mod["status"] != "tested":
            for ax in (a, b):
                status_text(ax, y, reading)
            continue
        lost = readers["recall"]["beyond_random"]["L"]
        a.text(0.03, y, f"lost beyond random: {100 * lost[0]:.0f} pp", va="center", color=S.COL["muted"])
        S.record(fid, target, "47.5: recall's answers kept, random part minus J++ part taken out (L)", *lost,
                 n=readers["recall"]["n"], source=source)  # fmt: skip
        for ax, w, col in ((a, "recall", S.COL["recall"]), (b, "lookup", S.COL["lookup"])):
            r = readers[w]
            for arm, dy, colour, what in (("zero_L", 0.16, col, "the J++ part's 25 directions taken out"),
                                          ("rand_L", -0.16, grey, "a random part (same size) taken out")):  # fmt: skip
                k = iv(r["kept"][arm])
                if k is None:
                    continue
                S.dot(ax, 0, y + dy, k, colour, size=8)
                S.record(
                    fid, target, f"47.5: {w}'s answers kept at L, {what}", *r["kept"][arm], n=r["n"], source=source
                )
    model_labels(a, rows)
    for ax in (a, b):
        S.panel_tag(ax, ", ".join(ns) if ns else None, "fixed")
    S.save(fig, out_name)
    return out_name


# ---- 47.3: a described bridge ---------------------------------------------------------------------------------------


def cue_title(v: dict) -> str:
    tested = [m for m in v["models"] if m["status"] == "tested"]
    if not tested:
        return "A described bridge: no model tested yet"
    need = majority(len(tested))
    split = ("keeps the split" if sum(m["clauses"]["a"] for m in tested) >= need else
             "is handed through the lens" if sum(m["clauses"]["a_prime"] for m in tested) >= need else
             "gives no clean split")  # fmt: skip
    value = ("the lookup never takes the value" if all(m["clauses"]["b"] for m in tested) else
             "the lookup sometimes takes the value")  # fmt: skip
    return f"A described bridge {split}; {value}"


def build_cue(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.3 (x47_cue verdict, x47_3.json): one row per model (cue step or gate failed: not tested). (a) extra loss
    without the J++ part at the description's word, recall and lookup (bars: the lookup at 0.10 for the split, 0.20
    for "handed through the lens"), the gap beside the model; (b) the lookup's value answers under the whole change
    (bar 5); (c) position answers lost without the label-free pointer beyond random, held-out half (bar 30)."""
    src = verdict_dir / "x47_3.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    fig, (a, b, c) = frame(
        title or cue_title(v),
        "Routes test, the asked pick described (\"Iris picked the one known for honey.\"); the change at the "
        "description's word",
        (1, 0.6, 0.9), ROW_IN * len(TARGETS), legend=readers_legend(), left=0.21, wrap=False)  # fmt: skip
    row_panels((a, b, c), len(TARGETS))
    S.extra_axis(a, label=False)
    a.set_xlabel("extra loss without\nthe J++ part")
    panel_title(a, "(a) the split")
    bar(a, 0.10, "≤ 0.10", side="left")
    bar(a, 0.20, "≥ 0.20")
    share_axis(b, "value answers\n(share)", ticks=(0, 0.1, 0.2, 0.3))
    b.set_xlim(-0.02, 0.3)
    panel_title(b, "(b) the value")
    bar(b, 0.05, "≤ 0.05")
    share_axis(c, "position answers lost\nbeyond random (share)")
    c.set_xlim(-0.2, 1.06)
    panel_title(c, "(c) the address")
    bar(c, 0.3, "≥ 0.3")
    rows, ns = [], []
    for i, (target, m) in enumerate(TARGETS):
        y, mod = -i, by.get(target, {"status": "pending"})
        if mod["status"] != "tested":
            rows.append((m, ""))
            why = mod.get("why", "")
            state = "pending" if mod["status"] == "pending" else (
                "not tested (description)" if "cue" in why else "not tested (gate)")  # fmt: skip
            S.record(fid, target, "47.3: status", state, source=source)
            for ax in (a, b, c):
                status_text(ax, y, state)
            continue
        rows.append((m, ""))
        ns.append(str(mod["n"]))
        S.record(
            fid, target, "47.3: gap (recall's extra loss minus the lookup's)", *mod["gap"], n=mod["n"], source=source
        )
        for w, dy, col in (("recall", 0.16, S.COL["recall"]), ("lookup", -0.16, S.COL["lookup"])):
            ex = iv(mod[w]["excess"])
            if ex is not None:
                S.dot(a, 0, y + dy, ex, col, size=8)
                S.record(fid, target, f"47.3: {w}'s extra loss without the J++ part", *mod[w]["excess"], n=mod["n"],
                         source=source)  # fmt: skip
        val = iv(mod["value"])
        if val is not None:
            S.dot(b, 0, y, val, S.COL["value"], size=8)
            S.record(
                fid, target, "47.3: lookup's value answers, whole change", *mod["value"], n=mod["n"], source=source
            )
        cut = mod["pcf_cut_test"]
        cv = iv(cut["cut"])
        if cv is None:
            status_text(c, y, "no held-out scenes")
        else:
            S.dot(c, 0, y, cv, S.COL["position"], size=8)
            S.record(fid, target, "47.3: position answers lost without the label-free pointer beyond random "
                     "(held-out half)", *cut["cut"], n=cut["n"], source=source)  # fmt: skip
        for clause, ok in mod["clauses"].items():
            S.record(fid, target, f"47.3: clause {clause} holds", int(bool(ok)), source=source)
    model_labels(a, rows)
    # n and the status above the panel titles, at the right (the narrow panels leave no room beside their titles)
    c.text(1.0, 1.13, f"n = {', '.join(ns)}  {S.STATUS_GLYPH['fixed']}" if ns else S.STATUS_GLYPH["fixed"],
           transform=c.transAxes, ha="right", va="bottom", color=S.COL["muted"])  # fmt: skip
    S.save(fig, out_name)
    return out_name


# ---- 47.2: six lockers ----------------------------------------------------------------------------------------------

SIX_LABEL = {"ordinal": "a line (ordinal)", "categorical, first vs rest": "first vs rest",
             "slot-specific": "locker-specific", "none of the three": "none of the three",
             "not interpretable": "not interpretable", "not tested": "not tested (gate)"}  # fmt: skip
SIX_TITLE = {"ordinal": "Six lockers: one shift moves the lookup one locker on, from any start",
             "categorical, first vs rest": "Six lockers: the order code marks the first locker, not a line",
             "slot-specific": "Six lockers: each locker has its own code, no single shift",
             "none of the three": "Six lockers: the order code is not a line, first vs rest or per locker",
             "not interpretable": "Six lockers: the lookup barely follows position, no reading"}  # fmt: skip
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}
SIX_DOSE = "2"  # the rule's decisive dose


def six_title(v: dict) -> str:
    labels = {m["label"] for m in v["models"] if m["status"] == "tested"}
    if not labels:
        return "Six lockers: no model tested yet"
    if len(labels) == 1:
        return SIX_TITLE[labels.pop()]
    return "Six lockers: the order code differs by model"


def build_six(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.2 (x47_six verdict, x47_2.json): one panel per model in the verdict (9B, 27B, Muse order). At the decisive
    dose (2) the shift vector from each start locker k: lookups sent to locker k + 1 (%), filled, and the random
    direction (same size) on the same scenes, grey; the rule's bar at 25; under each panel the reading, the pairwise
    writes reaching 25 and the first PCA axis's Spearman with the locker."""
    src = verdict_dir / "x47_2.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    shown = [(t, m) for t, m in TARGETS if t in by]
    # the shift vector is added at the bridge word: the mark system's diamond (Dan's 18:30 brief), not the removal dot
    legend = ([Line2D([], [], marker=S.MARK["add"], ls="", color=S.COL["lookup"], ms=7),
               Line2D([], [], marker=S.MARK["add"], ls="", color=S.COL["control"], ms=7)],
              ["the shift vector", "a random part (same size)"])  # fmt: skip
    fig, axes = frame(
        title or six_title(v),
        "Routes test with six lockers, held-out half; one shift vector added at the bridge word (twice a real change)",
        tuple(1.0 for _ in shown), 2.3, legend=legend, left=0.12, bottom_in=1.15, wrap=False)  # fmt: skip
    for ax, (target, m) in zip(axes, shown, strict=True):
        mod = by[target]
        ax.set_title(F.name_of(m) if ax is axes[0] else F.SHORT[m], fontsize=S.FONT, weight="bold", loc="left")
        ax.set_ylim(-0.04, 1.04)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="y", color="#eeeeee")
        if mod["status"] == "tested" and mod.get("interpretable"):
            S.panel_tag(ax, str(mod["n"]), "fixed")
        S.record(fid, target, "47.2: the rule's reading (dose 2)", mod.get("label", mod["status"]), source=source)
        if mod["status"] != "tested" or not mod["interpretable"]:
            S.empty(ax, "pending" if mod["status"] == "pending" else SIX_LABEL.get(mod.get("label", ""), "not tested"))
            ax.set_xticks([])
            if mod["status"] == "tested":
                S.record(fid, target, "47.2: position answers under the whole change", *mod["whole_position"],
                         n=mod["n"], source=source)  # fmt: skip
            continue
        n_lockers = int(mod["slots"])
        starts = list(range(1, n_lockers))
        # room right of the last start locker for each series' direct label (Dan's rethink: every panel labelled)
        ax.set_xlim(0.45, n_lockers + 0.55)
        ax.spines["bottom"].set_bounds(starts[0], starts[-1])
        ax.set_xticks(starts, [ORD[k] for k in starts])
        ax.set_xlabel("start locker")
        ax.axhline(0.25, color=BAR, lw=1.0, ls=(0, (4, 3)), zorder=1)
        ax.text(n_lockers + 0.5, 0.27, "≥ 0.25", ha="right", va="bottom", color=BAR)
        ends: list[tuple[float, str, str]] = []
        for k in starts:
            cell = mod["cells"]["shifts"].get(f"{SIX_DOSE}|v|{k}")
            if cell is None:
                continue
            for key, dx, col, what in (("shift", -0.12, S.COL["lookup"], "the shift vector"),
                                       ("random", 0.12, S.COL["control"], "a random direction (same size)")):  # fmt: skip
                r = iv(cell[key])
                if r is None:
                    continue
                ax.plot([k + dx] * 2, [r[1], r[2]], color=col, lw=1.6, zorder=2)
                ax.plot([k + dx], [r[0]], S.MARK["add"], ms=7, color=col, zorder=3)
                S.record(fid, target, f"47.2: lookups sent one locker on from the {ORD[k]} locker, {what}, dose 2",
                         *cell[key], n=cell["n"], source=source)  # fmt: skip
                if k == starts[-1]:
                    ends.append((r[0], "shift" if key == "shift" else "random",
                                 col if key == "shift" else S.COL["muted"]))  # fmt: skip
        S.end_labels(ax, starts[-1] + 0.12, ends, pad=0.18)
        rule, pca = mod["rules"][SIX_DOSE], mod["pca"]
        S.record(fid, target, "47.2: pairwise writes reaching 25% (dose 2)", rule["pairs_reaching"], n=rule["pairs"],
                 source=source)  # fmt: skip
        S.record(fid, target, "47.2: Spearman of the first PCA axis with the locker", pca["spearman_pc1_slot"],
                 source=source)  # fmt: skip
        # Dan (21:55): one line under each panel, the evidence for "its own code" (the reading is the title's)
        ax.text(0.0, -0.36, f"pairs moved ≥ 0.25: {rule['pairs_reaching']} of {rule['pairs']}; PCA axis ρ = "
                f"{pca['spearman_pc1_slot']:.2f}", transform=ax.transAxes, ha="left", va="top",
                fontsize=S.FONT - 1, color=S.COL["muted"])  # fmt: skip
    axes[0].set_ylabel("lookups moved one\nlocker on (share)")
    S.save(fig, out_name)
    return out_name


# ---- 47.13: the address probe on the lookup's errors ---------------------------------------------------------------


def errors_title(v: dict) -> str:
    scored = [m for m in v["models"] if m["rule"]["status"] == "scored"]
    if not scored:
        return "The address probe on the lookup's errors: too few errors to score"
    k = sum(bool(m["rule"]["holds"]) for m in scored)
    if k == len(scored):
        return "The address probe predicts the lookup's errors; the lens still has the item"
    if k == 0:
        return "The address probe does not predict the lookup's errors"
    return f"The address probe predicts the lookup's errors on {k} of {len(scored)} models"


def build_errors(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.13 (x47_errors verdict, x47_errors.json): one row per model. (a) wrong lookup answers whose locker the
    address probe predicts (%), beside the most-common-locker and layout baselines (grey) and chance (tick), the rule's
    bar at 50; (b) of the matched answers, the lens's top item at the bridge word still the right item (%), bar 80;
    (c) the reading (not tested: fewer than 30 wrong answers; pending: no lens read yet)."""
    src = verdict_dir / "x47_errors.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    grey = S.COL["control"]
    legend = ([Line2D([], [], marker="o", ls="", color=S.COL["position"], ms=8),
               Line2D([], [], marker="s", ls="", color=grey, ms=7),
               Line2D([], [], marker="D", ls="", color=grey, ms=6.5),
               Line2D([], [], marker="|", ls="", color=S.COL["muted"], ms=12, mew=1.6)],
              ["address probe", "most common locker", "… given the layout", "chance"], 4)  # fmt: skip
    fig, (a, b, c) = frame(
        title or errors_title(v),
        "Varied scenes, unedited, where the lookup answers wrong. (a) Wrong answers whose locker the address probe "
        "predicts (%); (b) of those, the lens's top item at the bridge word still the right item (%). 95% intervals, "
        "fixed in advance; a model with fewer than 30 wrong answers is not tested.",
        (1, 1, 0.6), ROW_IN * len(TARGETS), legend=legend)  # fmt: skip
    row_panels((a, b, c), len(TARGETS))
    pct_axis(a, "wrong answers whose\nlocker it predicts (%)", lim=(-4, 106))
    panel_title(a, "(a) the address")
    bar(a, 50, "≥ 50")
    pct_axis(b, "lens's top item\nstill right (%)", lim=(-4, 106))
    panel_title(b, "(b) the item")
    bar(b, 80, "≥ 80", side="left")
    text_column(c, "reading")
    rows = []
    for i, (target, m) in enumerate(TARGETS):
        y, mod = -i, by.get(target)
        if mod is None:
            rows.append((m, ""))
            c.text(0.04, y, "not run", va="center")
            for ax in (a, b):
                status_text(ax, y, "not run")
            continue
        r, rule = mod["rates"], mod["rule"]
        rows.append((m, f"{r['n']} wrong"))
        reading = {"scored": "predicts" if rule["holds"] else "does not\npredict",
                   "pending": "pending", "not tested": "not tested"}[rule["status"]]  # fmt: skip
        c.text(0.04, y, reading, va="center", linespacing=1.0)
        S.record(fid, target, "47.13: the rule's reading", rule["status"] + (": holds" if rule["holds"] else ""),
                 n=r["n"], source=source)  # fmt: skip
        if rule["status"] == "not tested":
            for ax in (a, b):
                status_text(ax, y, "too few wrong answers")
            continue
        for key, dy, col, mk, ms, what in (("probe", 0.2, S.COL["position"], "o", 8, "the address probe"),
                                           ("majority", 0.0, grey, "s", 7, "the most common locker"),
                                           ("layout", -0.2, grey, "D", 6.5, "the most common locker given the layout")):  # fmt: skip
            p = iv(r["match"].get(key), 100)
            if p is None:
                continue
            a.plot([p[1], p[2]], [y + dy] * 2, color=col, lw=1.6, zorder=2)
            a.plot([p[0]], [y + dy], mk, ms=ms, color=col, zorder=3)
            S.record(fid, target, f"47.13: wrong answers whose locker {what} predicts", *r["match"][key], n=r["n"],
                     source=source)  # fmt: skip
        if r.get("chance") is not None:
            a.plot([100 * r["chance"]] * 2, [y - 0.34, y + 0.34], color=S.COL["muted"], lw=1.6, zorder=1)
            S.record(fid, target, "47.13: chance (1 / lockers)", r["chance"], n=r["n"], source=source)
        lens = (r.get("lens") or {}).get("right_matched")
        lv = iv(lens, 100)
        if lens is None or lv is None:
            status_text(b, y, "no lens read yet")
        else:
            S.dot(b, 0, y, lv, S.COL["identity"], size=8)
            S.record(fid, target, "47.13: lens's top item still right, matched wrong answers", *lens,
                     n=r["lens"]["n_matched_with_lens"], source=source)  # fmt: skip
    model_labels(a, rows)
    S.save(fig, out_name)
    return out_name


TESTS = {
    "47.1": ("scripts/x47_atoms.py", build_atoms, "fig11_atoms_26_100"),
    "47.5": ("scripts/x47_zero.py", build_zero, "fig12_zeroing"),
    "47.3": ("scripts/x47_cue.py", build_cue, "fig13_described_bridge"),
    "47.2": ("scripts/x47_six.py", build_six, "fig14_six_lockers"),
    "47.13": ("scripts/x47_errors.py", build_errors, "fig15_probe_errors"),
}
