"""slot_outcomes (Dan's B3, 23 Oct): where the answer goes, sentence by sentence, when the last two tokens are copied.

Reads results/slot_outcomes/<stamp>/table.csv (scripts/slot_outcomes.py; default: the newest stamp). One stacked bar per
place k of the sentence the copied prompt asks about: every patched answer in one of the outcomes, 100% per bar. Order
(same place in the list; LOOKUP purple, the accent) is stacked from the bottom and identity (same entity; dark grey)
ends at the top, so both read against a fixed edge; between them, bottom to top: another listed digit (teal), the copied
digit (the donor's own, patch_by_depth's brown), answers off the list (palest grey) and unchanged (light grey). Shares are
recomputed from the counts, so a bar sums to exactly 100%.

MAIN: questions whose bridge is recalled (memory -> prompt, RL), the 5-sentence lists pooled over the three prompt sets,
four models (MAIN_MODELS: two hybrids, two attention-only); thin lines beside a bar are the Wilson 95% intervals (order's
left of it, identity's right); the shares that carry the story are written in the bars (order at k = 1-2, identity from
k = 3). FULL: every model (rows) x recalled and named bridges (memory -> prompt RL, named -> prompt DL) x lists of 5, 8
and 12 sentences (columns); no intervals (table.csv has them). Every drawn share is a Number with table.csv as source.

uv run python scripts/figs/slot_outcomes.py [--table results/slot_outcomes/<stamp>] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from matplotlib.lines import Line2D
from matplotlib.transforms import offset_copy

from bridge_jspace import pins
from scripts import readme_build as RB
from scripts import slot_outcomes as SO
from scripts.figs import common as C
from scripts.figs import order_identity as OI
from scripts.figs import patch_by_depth as PBD

STEM = "slot_outcomes"
MAIN_MODELS = ("27b", "9b", "32b", "gemma")  # two hybrids, two attention-only (as patch_by_depth); the rest in FULL
ANOTHER = "#018571"  # another listed digit: a teal apart from LOOKUP's purple and the digit's brown (4.6:1 on white)
OFF = "#ededed"  # answers off the list: the palest grey, below unchanged's light grey


@dataclass(frozen=True)
class Seg:
    key: str  # the table's column prefix
    label: str  # the direct label
    color: str


SEGS = (  # bottom to top
    Seg("order", "same place (order)", C.LOOKUP),
    Seg("another", "another listed digit", ANOTHER),
    Seg("donor", "the copied digit", PBD.DIGIT),
    Seg("off_list", "off the list", OFF),
    Seg("unchanged", "unchanged", C.CONTROL),
    Seg("identity", "same entity", C.RECALL),
)
LISTS = ((SO.POOLED, 5), ("8 sentences", 8), ("12 sentences", 12))
FAMILY = {"RL": "Bridge recalled from memory", "DL": "Bridge named in the question"}
TITLE = "Sentences 1–2 go by order, later ones by entity"
SUBTITLE = "Last two tokens copied from a prompt asking about its k-th sentence: where answers go"
HOW = "one bar per k, all answers; purple = same place in the list, dark grey = same entity."
HOW_FULL = "one bar per k, all answers; per side, lists of 5, 8 and 12 sentences; colors on the right."
XLABEL = "k: the sentence the copied prompt asks about"
VALUE_MIN = 15.0  # % : a share is written in its bar only when the bar's segment is at least this tall
Rows = dict[tuple[str, str, str], list[dict[str, str]]]


def newest_table() -> Path:
    found = sorted(SO.OUT.glob("*/table.csv"))
    if not found:
        raise FileNotFoundError(f"no {SO.OUT}/<stamp>/table.csv: run scripts/slot_outcomes.py first")
    return found[-1].parent


def read_table(folder: Path) -> Rows:
    """{(model, family, setting): rows by k} of the pooled 5-sentence lists and the 8- and 12-sentence lists."""
    out: Rows = collections.defaultdict(list)
    with (folder / "table.csv").open() as fh:
        for r in csv.DictReader(fh):
            if r["setting"] in dict(LISTS):
                out[(r["model"], r["family"], r["setting"])].append(r)
    for rs in out.values():
        rs.sort(key=lambda r: int(r["k"]))
    return dict(out)


def shares(r: dict[str, str]) -> dict[str, float]:
    """% of the bar's answers per segment, from the counts (they sum to n, so the bar ends at 100)."""
    n = int(r["n"])
    return {s.key: 100 * int(r[f"{s.key}_n"]) / n for s in SEGS}


def source_of(folder: Path) -> str:
    p = folder / "table.csv"
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


def panel(ax, rows: list[dict[str, str]], key: tuple[str, str, str], source: str, sentences: int, *, main: bool,
          width: float = 0.62) -> list[C.Number]:  # fmt: skip
    """One model's stacked bars over k, the intervals and value labels on MAIN; returns the drawn Numbers."""
    nums: list[C.Number] = []
    for r in rows:
        k, sh = int(r["k"]), shares(r)
        y = 0.0
        for s in SEGS:
            if sh[s.key] > 0:
                ax.bar(k, sh[s.key], width, bottom=y, color=s.color, lw=0, zorder=2)
            ci = None if s.key == "off_list" else (float(r[f"{s.key}_lo"]), float(r[f"{s.key}_hi"]))
            nums.append(C.Number(sh[s.key], f"% of answers: {s.key}", model=key[0], setting=key[2], ci=ci,
                                 n=int(r["n"]), source=source, extra={"family": key[1], "k": k, "outcome": s.key}))  # fmt: skip
            y += sh[s.key]
        if not main:
            continue
        lo, hi = float(r["order_lo"]), float(r["order_hi"])
        side = width / 2 + 0.07
        ax.plot([k - side] * 2, [lo, hi], color=C.INK2, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
                solid_capstyle="butt", gid="ci", zorder=3)  # fmt: skip
        lo, hi = float(r["identity_lo"]), float(r["identity_hi"])
        ax.plot([k + side] * 2, [100 - hi, 100 - lo], color=C.INK2, lw=C.ERRORBAR["elinewidth"],
                alpha=C.ERRORBAR["alpha"], solid_capstyle="butt", gid="ci", zorder=3)  # fmt: skip
        val, at = (sh["order"], sh["order"] / 2) if k <= 2 else (sh["identity"], 100 - sh["identity"] / 2)
        if val >= VALUE_MIN:
            ax.text(k, at, f"{val:.0f}", ha="center", va="center", fontsize=C.NOTE, color="white", fontweight="bold",
                    gid="value", zorder=4)  # fmt: skip
    ax.set_xlim(0.4, sentences + 0.6)
    ax.set_ylim(0, 100)
    ticks = list(range(1, sentences + 1)) if sentences <= 8 else [1, 2, 3, 6, 9, 12]
    ax.set_xticks(ticks, [str(t) for t in ticks])
    ax.tick_params(axis="x", length=0)
    ax.spines["bottom"].set_visible(False)
    return nums


def y_axis(ax, first: bool, label: str | None = "% of answers") -> None:
    ax.set_yticks([0, 50, 100], ["0", "50", "100"] if first else [])
    ax.tick_params(axis="y", length=3.5 if first else 0)
    ax.spines["left"].set_visible(first)
    if first and label:
        ax.set_ylabel(label)


def side_labels(ax, r: dict[str, str], keys: tuple[str, ...]) -> None:
    """The outcomes' names right of the panel, at their segment's middle in its last bar, pushed apart; each with a
    swatch of its color (text in ink: the light greys are too pale to read as text)."""
    sh = shares(r)
    mids, y = {}, 0.0
    for s in SEGS:
        mids[s.key] = y + sh[s.key] / 2
        y += sh[s.key]
    segs = [s for s in SEGS if s.key in keys]
    height_in = ax.get_position().height * ax.figure.get_figheight()
    gap = (C.NOTE * 1.25 + 4) / 72 / height_in * 100
    ys = PBD.spread([mids[s.key] for s in segs], gap, gap / 2, 100 - gap / 2)
    tr = offset_copy(ax.get_yaxis_transform(), fig=ax.figure, x=10, units="points")
    sw = offset_copy(ax.get_yaxis_transform(), fig=ax.figure, x=18, units="points")
    for s, yy in zip(segs, ys, strict=True):
        ax.plot([1.0], [yy], transform=tr, marker="s", markersize=11, color=s.color, markeredgecolor=C.INK2,
                markeredgewidth=0.6, clip_on=False, linestyle="none")  # fmt: skip
        ax.text(1.0, yy, s.label, transform=sw, ha="left", va="center", fontsize=C.NOTE, color=C.INK, gid="label")


def column_key(fr: C.Frame, top_ax, low_ax) -> None:
    """FULL: the outcomes' names in stacking order (bottom to top), right of the panels, from the bottom of `low_ax`
    to the top of `top_ax` (one panel is too short for six names)."""
    a, b = top_ax.get_position(), low_ax.get_position()
    for i, s in enumerate(SEGS):
        y = b.y0 + i * (a.y1 - b.y0) / (len(SEGS) - 1)
        tr = offset_copy(fr.fig.transFigure, fig=fr.fig, x=12, units="points")
        sw = offset_copy(fr.fig.transFigure, fig=fr.fig, x=20, units="points")
        fr.fig.add_artist(Line2D([a.x1], [y], transform=tr, marker="s", markersize=11, color=s.color,
                                 markeredgecolor=C.INK2, markeredgewidth=0.6, linestyle="none"))  # fmt: skip
        fr.fig.text(a.x1, y, s.label, transform=sw, ha="left", va="center", fontsize=C.NOTE, color=C.INK, gid="label")


def n_range(rows: Rows, keys: list[tuple[str, str, str]]) -> str:
    ns = [int(r["n"]) for k in keys for r in rows[k]]
    return f"{min(ns)}–{max(ns)}" if min(ns) != max(ns) else str(ns[0])


def x_label(fr: C.Frame, axes: list) -> None:
    """One x label, centred under the lowest panels."""
    boxes = [ax.get_position() for ax in axes]
    y0 = min(b.y0 for b in boxes)
    x0, x1 = min(b.x0 for b in boxes), max(b.x1 for b in boxes)
    tr = offset_copy(fr.fig.transFigure, fig=fr.fig, y=-(C.TICK * 1.6 + 8), units="points")
    fr.fig.text((x0 + x1) / 2, y0, XLABEL, transform=tr, ha="center", va="top", fontsize=C.LABEL, color=C.INK)


def draw_main(folder: Path, out: Path = C.OUT) -> list[Path]:
    rows = read_table(folder)
    keys = [(m, "RL", SO.POOLED) for m in MAIN_MODELS if (m, "RL", SO.POOLED) in rows]
    if not keys:
        raise ValueError("no MAIN model has pooled 5-sentence rows")
    off = max(shares(r)["off_list"] for k in keys for r in rows[k])
    sets = {k[0]: len(rows[k][0]["runs"].split()) for k in keys}
    caption = OI.pack([
        f"Questions whose bridge is recalled; {'three prompt sets' if set(sets.values()) == {3} else 'prompt sets'} "
        f"pooled, n = {n_range(rows, keys)} per bar; thin lines: 95% CI.",
        f"Answers off the list: {'none' if off == 0 else f'at most {off:.1f}%'}.",
        "All eight models, named bridges and lists of 8 and 12 sentences: full version.",
    ])  # fmt: skip
    fr = C.frame("main", TITLE, SUBTITLE, how=HOW, caption=caption, nrows=2, ncols=2, left=0.075, right=0.80,
                 wspace=0.12, hspace=0.62, panel_titles=True)  # fmt: skip
    nums: list[C.Number] = []
    source = source_of(folder)
    for i, (ax, key) in enumerate(zip(fr.axes, keys, strict=False)):
        nums += panel(ax, rows[key], key, source, 5, main=True)
        y_axis(ax, i % 2 == 0)
        ax.set_title(C.MODEL[key[0]].name, fontsize=C.LABEL, fontweight="bold", pad=8, loc="left")
    for ax in fr.axes[len(keys) :]:
        fr.fig.delaxes(ax)
    label_ax, label_key = (fr.axes[1], keys[1]) if len(keys) > 1 else (fr.axes[0], keys[0])
    shown = tuple(s.key for s in SEGS if s.key != "off_list" or off >= 1.0)
    side_labels(label_ax, rows[label_key][-1], shown)
    x_label(fr, fr.axes[len(fr.axes) - 2 :] if len(fr.axes) > 2 else fr.axes)
    return C.save(fr, STEM, nums, out)


def full_caption(rows: Rows, keys: list[tuple[str, str, str]]) -> str:
    """n range, exceptions (a list where most answers leave it; later sentences where entity does not beat order) and
    what was not run."""
    ties: list[str] = []
    offs: dict[str, list[tuple[float, str]]] = collections.defaultdict(list)  # (family, list) -> (share, model)
    order = {m: i for i, m in enumerate(RB.ORDER)}
    for k in sorted(keys, key=lambda k: (order[k[0]], k[1], k[2])):
        rs = rows[k]
        n = sum(int(r["n"]) for r in rs)
        off = sum(int(r["off_list_n"]) for r in rs) / n
        later = [r for r in rs if int(r["k"]) >= 3]
        diff = sum(int(r["identity_n"]) - int(r["order_n"]) for r in later) / sum(int(r["n"]) for r in later)
        where = f"{'recalled' if k[1] == 'RL' else 'named'}, {k[2].split()[0]}"
        if off >= 0.2:
            offs[where].append((off, C.MODEL[k[0]].short))
        if diff <= 0:
            ties.append(f"{C.MODEL[k[0]].short} ({where}; {100 * diff:+.1f} pts)".replace("-", "−"))
    offs_text = "; ".join(f"{', '.join(f'{m} {100 * s:.0f}%' for s, m in sorted(v, reverse=True))} ({w})"
                          for w, v in offs.items())  # fmt: skip
    gone = []
    for m in sorted({k[0] for k in keys}, key=order.__getitem__):
        lens = [str(n_) for s, n_ in LISTS[1:] if not any(k[0] == m and k[2] == s for k in keys)]
        if lens:
            gone.append(f"{C.MODEL[m].short} {' and '.join(lens)} sentences")
    two = sorted({C.MODEL[k[0]].short for k in keys if k[2] == SO.POOLED and len(rows[k][0]["runs"].split()) < 3})
    return OI.pack([
        f"n = {n_range(rows, keys)} per bar (5 sentences: sets pooled" + (f", {', '.join(two)} two" if two else "")
        + ").",
        ("Not run: " + ", ".join(gone) + ".") if gone else "",
        f"Off the list: {offs_text}." if offs else "",
        ("Entity ≈ order from sentence 3: " + ", ".join(ties) + ".") if ties else "",
    ])  # fmt: skip


def draw_full(folder: Path, out: Path = C.OUT) -> list[Path]:
    rows = read_table(folder)
    models = [m.key for m in C.MODELS if any(k[0] == m.key for k in rows)]
    if not models:
        raise ValueError("no rows to draw")
    cols = [(fam, s, n) for fam in SO.FAMILIES for s, n in LISTS]
    keys = [k for k in rows if k[0] in models]
    ratios = [5, 8, 12, 2.2, 5, 8, 12]
    fr = C.frame("full", TITLE, SUBTITLE, how=HOW_FULL, caption=full_caption(rows, keys), nrows=len(models),
                 ncols=7, size=(12.0, 3.4 + 1.5 * len(models)), width_ratios=ratios, left=0.065, right=0.80,
                 wspace=0.1, hspace=0.62, panel_titles=True)  # fmt: skip
    PBD.head_room(fr, C.LABEL * 1.6)  # the family headings above the first row's model title
    nums: list[C.Number] = []
    source = source_of(folder)
    drawn = []
    grid_axes = list(fr.axes)
    for i, m in enumerate(models):
        row_axes = grid_axes[7 * i : 7 * i + 7]
        fr.fig.delaxes(row_axes[3])  # the gap between the families
        for j, (fam, s, n) in enumerate(cols):
            ax = row_axes[j if j < 3 else j + 1]
            key = (m, fam, s)
            if key not in rows:  # no empty panels: the caption names what was not run
                fr.fig.delaxes(ax)
                continue
            nums += panel(ax, rows[key], key, source, n, main=False, width=0.72)
            y_axis(ax, j in (0, 3), None)
            drawn.append(ax)
        row_axes[0].set_title(C.MODEL[m].name, fontsize=C.LABEL, fontweight="bold", pad=6, loc="left")
    top = grid_axes[0].get_position()
    for fam, j in (("RL", 0), ("DL", 4)):
        a, b = grid_axes[j].get_position(), grid_axes[j + 2].get_position()
        tr = offset_copy(fr.fig.transFigure, fig=fr.fig, y=C.LABEL * 1.6 + 10, units="points")
        fr.fig.text((a.x0 + b.x1) / 2, top.y1, FAMILY[fam], transform=tr, ha="center", va="bottom",
                    fontsize=C.LABEL, fontweight="bold", color=C.INK, gid="family")  # fmt: skip
    column_key(fr, grid_axes[6], grid_axes[13] if len(models) > 1 else grid_axes[6])
    x_label(fr, drawn)
    return C.save(fr, STEM, nums, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", type=Path, default=None, help="a results/slot_outcomes/<stamp> folder (default: newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    folder = a.table or newest_table()
    for kind, draw in (("main", draw_main), ("full", draw_full)):
        if a.only in (None, kind):
            for p in draw(folder, a.out):
                print(p.relative_to(pins.REPO_ROOT) if p.is_relative_to(pins.REPO_ROOT) else p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
