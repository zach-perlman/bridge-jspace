"""README figures for batch 47 (part a): one figure per test, each drawn from that test's verdict folder (the json its
`verdict` stage writes) in story_style's look, every plotted number recorded for figures/story/data.csv.

  47.1  x47_atoms.py   x47_1-<UTC>/x47_1.json         Fig. 11: without the J++ lens's directions 26-100
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

from matplotlib.lines import Line2D
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
          bottom_in: float = BOTTOM_IN, sharey: bool = True):  # fmt: skip
    """The figure: the claim, the subtitle (NOTE first, wrapped), an optional legend (handles, labels[, ncol]) under
    it, and panels side by side with body_in inches of plot; the height follows from them."""
    # "J++ part" and "J++ lens" stay on one line (the glossary's names), hyphenated words whole
    keep = (NOTE + sub).replace("J++ ", "J++\u00a0")
    lines = [x.replace("\u00a0", " ") for x in textwrap.wrap(keep, WRAP, break_on_hyphens=False)]
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
    S.title(fig, title, "\n".join(lines), limit=86)
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
E3_PARTS = (("jpp", "J++ part\n(lens directions 1–25)", False), ("26-100", "lens directions\n26–100", True),
            ("pca_eq", "PCA directions\n(same size)", False), ("wu", "logit-lens\ndirections", True),
            ("rand", "random lens\ndirections", True))  # fmt: skip
E3_FALLS = (("1-25", "1–25"), ("26-100", "26–100"), ("1-100", "1–100"))  # the inset's rows (27B)
E3_INSET_MODEL = "qwen3.6-27b"


def build_identity(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """E3 (v6; Fig. 2 and 47.1 merged): one extra-loss axis, one group of rows per part of the change taken out at the
    bridge word (the J++ part, lens directions 26-100, PCA directions of the J++ part's size, logit-lens and random lens
    directions), one row per model (9B, 27B, Muse) with the lookup's and the recall's extra loss and their 95% intervals
    (open: the parts runs on one-pick scenes, after the data; filled: the main test, fixed in advance). Inset: the 27B's
    routes test, the lookup's identity answers lost beyond random without lens directions 1-25, 26-100 and both (47.1,
    fixed in advance). The 122B's parts: figures/supp/s02_parts_all."""
    src = verdict_dir / "x47_1.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    parts = F.parts_cells()
    h = 6.9
    plt = S.setup()
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, title or "Only the J++ part costs the recall; no single part costs the lookup",
            "Extra loss without each part of the change, beyond a random part of the same size; whiskers 95%.")  # fmt: skip
    ax = fig.add_axes((0.30, 0.6 / h, 0.36, 1 - 1.45 / h - 0.6 / h))
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
            labels.append(F.SHORT[m])
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
    ax.text(1.0, 1.005, f"n {n_txt} per model · ● fixed in advance · ○ after the data", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=S.FONT, color=S.COL["muted"])  # fmt: skip
    hs, ls = F.reader_handles(plt)
    F.legend(fig, hs, ls, 1 - 0.62 / h, ncol=2)

    # inset: the 27B's identity answers lost beyond random (routes test), without 1-25, 26-100 and both
    ins = S.inset(fig, (0.79, 0.44, 0.19, 0.22))
    falls = ((by.get(E3_INSET_MODEL) or {}).get("routes") or {}).get("falls", {})
    n_routes = ((by.get(E3_INSET_MODEL) or {}).get("routes") or {}).get("n")
    for i, (k, _) in enumerate(E3_FALLS):
        f = iv((falls.get(k) or {}).get("identity"))
        if f is None:
            status_text(ins, -i, "not run")
            continue
        S.dot(ins, 0, -i, f, S.COL["identity"], size=7)
        ins.text(f[2] + 0.04, -i, f"{f[0]:.2f}", va="center", fontsize=S.FONT - 1, color=S.COL["identity"])
        S.record(fid, E3_INSET_MODEL, f"47.1: identity answers lost beyond random without lens directions {k}", *f,
                 n=n_routes, source=source)  # fmt: skip
    ins.set_xlim(-0.05, 1.0)
    ins.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ins.axvline(0, color="#999999", lw=0.8, zorder=1)
    ins.set_ylim(-len(E3_FALLS) + 0.4, 0.6)
    ins.set_yticks([-i for i in range(len(E3_FALLS))], [name for _, name in E3_FALLS])
    ins.tick_params(axis="y", length=0)
    ins.grid(axis="x", color="#eeeeee")
    ins.set_xlabel("identity answers lost\nbeyond random", fontsize=S.FONT - 1)
    head = blended_transform_factory(fig.transFigure, ins.transAxes)
    ins.text(0.705, 1.42, "The 27B's identity answers\nwithout lens directions", transform=head,
             fontsize=S.FONT, weight="bold", va="bottom", linespacing=1.0)  # fmt: skip
    ins.text(0.705, 1.06, f"routes test · n {n_routes}\n● fixed in advance", transform=head,
             fontsize=S.FONT - 1, color=S.COL["muted"], va="bottom", linespacing=1.1)  # fmt: skip
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
    changed prompt's answers kept (%), (a) recall (the rule's bar at 80), (b) lookup beside; (c) the rule's reading
    and the recall's answers kept below random (the 'needed' bar is 30)."""
    src = verdict_dir / "x47_5.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    grey = S.COL["control"]
    legend = ([Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=8),
               Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8),
               Line2D([], [], marker="o", ls="", color=grey, ms=8)],
              ["recall", "lookup", "random part (same size) taken out"])  # fmt: skip
    fig, (a, b, c) = frame(
        title or zero_title(v),
        "Main test (two people swap picks), on the changed prompt: at the bridge word, at one layer, the J++ part's 25 "
        "directions, or a random part (same size), taken out of its state. Answers kept (%), 95% intervals, fixed in "
        "advance. Rule: followed if ≥ 80 kept, within 10 of random; needed if ≥ 30 below random.",
        (1, 1, 0.62), ROW_IN * len(TARGETS), legend=legend)  # fmt: skip
    row_panels((a, b, c), len(TARGETS))
    for ax, name in ((a, "(a) recall"), (b, "(b) lookup, beside")):
        pct_axis(ax, "changed prompt's\nanswers kept (%)", lim=(-4, 106))
        panel_title(ax, name)
        bar(ax, 80, "≥ 80", side="left")
    text_column(c, "reading (recall)")
    rows = []
    for i, (target, m) in enumerate(TARGETS):
        y, mod = -i, by.get(target, {"status": "pending", "label": "pending"})
        readers = mod.get("readers", {})
        rows.append((m, f"n = {readers['recall']['n']}" if "recall" in readers else ""))
        reading = str(ZERO_LABEL.get(mod["label"], mod["label"]))
        S.record(fid, target, "47.5: the rule's reading (recall at L)", mod["label"], source=source)
        if mod["status"] != "tested":
            c.text(0.04, y, reading, va="center")
            for ax in (a, b):
                status_text(ax, y, reading)
            continue
        lost = readers["recall"]["beyond_random"]["L"]
        c.text(0.04, y + 0.04, reading, va="bottom")
        c.text(0.04, y - 0.04, f"{100 * lost[0]:.0f} below random", va="top", color=S.COL["muted"])
        S.record(fid, target, "47.5: recall's answers kept, random part minus J++ part taken out (L)", *lost,
                 n=readers["recall"]["n"], source=source)  # fmt: skip
        for ax, w, col in ((a, "recall", S.COL["recall"]), (b, "lookup", S.COL["lookup"])):
            r = readers[w]
            for arm, dy, colour, what in (("zero_L", 0.16, col, "the J++ part's 25 directions taken out"),
                                          ("rand_L", -0.16, grey, "a random part (same size) taken out")):  # fmt: skip
                k = iv(r["kept"][arm], 100)
                if k is None:
                    continue
                S.dot(ax, 0, y + dy, k, colour, size=8)
                S.record(
                    fid, target, f"47.5: {w}'s answers kept at L, {what}", *r["kept"][arm], n=r["n"], source=source
                )
    model_labels(a, rows)
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
        "Routes test (another item moved), the asked pick described: \"Iris picked the one known for honey.\" The "
        "change at the description's word. (a) Extra loss (0–1): switches lost without the J++ part minus without a "
        "random part (same size); (b) lookup answers that are the new number; (c) position answers lost without the "
        "label-free pointer beyond random. 95% intervals, fixed in advance.",
        (1, 0.6, 0.9), ROW_IN * len(TARGETS), legend=readers_legend(), left=0.21)  # fmt: skip
    row_panels((a, b, c), len(TARGETS))
    S.extra_axis(a, label=False)
    a.set_xlabel("extra loss")
    panel_title(a, "(a) the split")
    bar(a, 0.10, "≤ 0.10", side="left")
    bar(a, 0.20, "≥ 0.20")
    pct_axis(b, "value\nanswers (%)", lim=(-2, 30), ticks=(0, 10, 20, 30))
    panel_title(b, "(b) the value")
    bar(b, 5, "≤ 5")
    pct_axis(c, "position answers lost\nbeyond random (%)", lim=(-20, 106))
    panel_title(c, "(c) a pointer")
    bar(c, 30, "≥ 30")
    rows = []
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
        gap = iv(mod["gap"])
        rows.append((m, f"n = {mod['n']}, gap {gap[0]:.2f}" if gap else f"n = {mod['n']}"))
        S.record(
            fid, target, "47.3: gap (recall's extra loss minus the lookup's)", *mod["gap"], n=mod["n"], source=source
        )
        for w, dy, col in (("recall", 0.16, S.COL["recall"]), ("lookup", -0.16, S.COL["lookup"])):
            ex = iv(mod[w]["excess"])
            if ex is not None:
                S.dot(a, 0, y + dy, ex, col, size=8)
                S.record(fid, target, f"47.3: {w}'s extra loss without the J++ part", *mod[w]["excess"], n=mod["n"],
                         source=source)  # fmt: skip
        val = iv(mod["value"], 100)
        if val is not None:
            S.dot(b, 0, y, val, S.COL["value"], size=8)
            S.record(
                fid, target, "47.3: lookup's value answers, whole change", *mod["value"], n=mod["n"], source=source
            )
        cut = mod["pcf_cut_test"]
        cv = iv(cut["cut"], 100)
        if cv is None:
            status_text(c, y, "no held-out scenes")
        else:
            S.dot(c, 0, y, cv, S.COL["position"], size=8)
            S.record(fid, target, "47.3: position answers lost without the label-free pointer beyond random "
                     "(held-out half)", *cut["cut"], n=cut["n"], source=source)  # fmt: skip
        for clause, ok in mod["clauses"].items():
            S.record(fid, target, f"47.3: clause {clause} holds", int(bool(ok)), source=source)
    model_labels(a, rows)
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
    legend = ([Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8),
               Line2D([], [], marker="o", ls="", color=S.COL["control"], ms=8)],
              ["the shift vector", "random direction (same size)"])  # fmt: skip
    fig, axes = frame(
        title or six_title(v),
        "Routes test with six lockers (one item's locker sentence moved), held-out half. One shift vector added at "
        "the bridge word (dose 2× a real change) from each start locker: lookups sent one locker on (%), 95% "
        "intervals. Rule for a line: ≥ 25 from 4 of 5 start lockers, the random direction ≤ 5, the first PCA axis "
        "in locker order. Fixed in advance.",
        tuple(1.0 for _ in shown), 2.3, legend=legend, left=0.12, bottom_in=1.45)  # fmt: skip
    for ax, (target, m) in zip(axes, shown, strict=True):
        mod = by[target]
        ax.set_title(F.name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_ylim(-4, 104)
        ax.set_yticks(*F.PCT)
        ax.grid(axis="y", color="#eeeeee")
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
        ax.set_xlim(0.45, n_lockers - 0.45)
        ax.set_xticks(starts, [ORD[k] for k in starts])
        ax.set_xlabel("start locker")
        ax.axhline(25, color=BAR, lw=1.0, ls=(0, (4, 3)), zorder=1)
        ax.text(n_lockers - 0.5, 27, "≥ 25", ha="right", va="bottom", color=BAR)
        for k in starts:
            cell = mod["cells"]["shifts"].get(f"{SIX_DOSE}|v|{k}")
            if cell is None:
                continue
            for key, dx, col, what in (("shift", -0.12, S.COL["lookup"], "the shift vector"),
                                       ("random", 0.12, S.COL["control"], "a random direction (same size)")):  # fmt: skip
                r = iv(cell[key], 100)
                if r is None:
                    continue
                ax.plot([k + dx] * 2, [r[1], r[2]], color=col, lw=1.6, zorder=2)
                ax.plot([k + dx], [r[0]], "o", ms=8, color=col, zorder=3)
                S.record(fid, target, f"47.2: lookups sent one locker on from the {ORD[k]} locker, {what}, dose 2",
                         *cell[key], n=cell["n"], source=source)  # fmt: skip
        rule, pca = mod["rules"][SIX_DOSE], mod["pca"]
        S.record(fid, target, "47.2: pairwise writes reaching 25% (dose 2)", rule["pairs_reaching"], n=rule["pairs"],
                 source=source)  # fmt: skip
        S.record(fid, target, "47.2: Spearman of the first PCA axis with the locker", pca["spearman_pc1_slot"],
                 source=source)  # fmt: skip
        ax.text(0.0, -0.33, SIX_LABEL.get(mod["label"], mod["label"]), transform=ax.transAxes, ha="left", va="top",
                weight="bold")  # fmt: skip
        ax.text(0.0, -0.45, f"pairwise writes ≥ 25: {rule['pairs_reaching']} of {rule['pairs']}\nfirst PCA axis vs "
                f"locker: ρ = {pca['spearman_pc1_slot']:.2f}", transform=ax.transAxes, ha="left", va="top",
                color=S.COL["muted"])  # fmt: skip
    axes[0].set_ylabel("lookups sent\none locker on (%)")
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
