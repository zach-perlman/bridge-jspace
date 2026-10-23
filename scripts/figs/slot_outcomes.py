"""slot_outcomes (Dan's B3, 23 Oct): where the answer goes, sentence by sentence, when the last two tokens are copied.

Reads results/slot_outcomes/<stamp>/table.csv (scripts/slot_outcomes.py; default: the newest stamp). One stacked bar per
place k of the sentence the copied prompt asks about: every patched answer in one of the outcomes, 100% per bar. Order
(same place in the list; LOOKUP purple, the accent) is stacked from the bottom and identity (same entity; dark grey)
ends at the top, so both read against a fixed edge; between them, bottom to top: another listed digit (teal), the copied
digit (the donor's own, patch_by_depth's brown), answers off the list (palest grey) and unchanged (light grey). Shares are
recomputed from the counts, so a bar sums to exactly 100%.

MAIN: questions whose bridge is recalled (memory -> prompt, RL), the 5-sentence lists pooled over the three prompt sets,
three models (MAIN_MODELS: the 27B, the 32B, Gemma) and a fourth panel, the 27B with the copied prompt's entity absent
from the original (results/absent_entity/<run>/verdict.json, the decisive items by k: originals not asking their 1st
sentence; k = 1 not tested, order and the 1st sentence's digit are one digit there). That panel splits off the original's
1st-sentence digit (fallback, magenta) and has no same-entity answer (the entity is not in the original). Thin vertical
lines on the bar's centre are the Wilson 95% intervals at the order segment's top and the identity segment's bottom
(the absent panel: order's only); the shares that carry the story are written in the bars (order at k = 1-2, identity
from k = 3; the absent panel: order at every k). FULL: every model (rows) x recalled and named bridges (memory -> prompt
RL, named -> prompt DL) x lists of 5, 8 and 12 sentences (columns); no intervals (table.csv has them). Every drawn share
is a Number with table.csv (or the absent run's verdict.json) as source.

uv run python scripts/figs/slot_outcomes.py [--table results/slot_outcomes/<stamp>] [--absent results/absent_entity/<run>]
    [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from matplotlib import patheffects
from matplotlib.lines import Line2D
from matplotlib.transforms import offset_copy

from bridge_jspace import pins
from bridge_jspace import plot_style as PS
from scripts import readme_build as RB
from scripts import slot_outcomes as SO
from scripts.figs import common as C
from scripts.figs import order_identity as OI
from scripts.figs import patch_by_depth as PBD

STEM = "slot_outcomes"
# the 27B, the 32B, Gemma; the fourth MAIN panel is the 27B with the entity absent (the 9B and the rest in FULL)
MAIN_MODELS = ("27b", "32b", "gemma")
ABSENT_ROOT = pins.REPO_ROOT / "results" / "absent_entity"
ABSENT_GLOB = "d3_absent_entity_27b_r2_*/verdict.json"
ABSENT_KEY = ("27b", "RL", "5 sentences, entity absent")  # the absent panel's Number key (model, family, setting)
ANOTHER = "#018571"  # another listed digit: a teal apart from LOOKUP's purple and the digit's brown (4.6:1 on white)
OFF = "#ededed"  # answers off the list: the palest grey, below unchanged's light grey
FALLBACK = "#D01C8B"  # the original's 1st-sentence digit (absent panel): a magenta apart from the other outcomes


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
# the absent panel, bottom to top: no same-entity answer (the entity is not in the original), the 1st sentence apart
ABSENT_SEGS = (
    SEGS[0],
    Seg("fallback", "1st sentence's digit", FALLBACK),
    *SEGS[1:5],
)
KEY_SEGS = (SEGS[0], ABSENT_SEGS[1], *SEGS[1:])  # MAIN's key: every outcome drawn, bottom to top
ABSENT_SHARES = {"order": "order", "fallback": "fallback", "another": "other_digit", "unchanged": "unchanged"}
LISTS = ((SO.POOLED, 5), ("8 sentences", 8), ("12 sentences", 12))
FAMILY = {"RL": "Bridge recalled from memory", "DL": "Bridge named in the question"}
TITLE = "Sentences 1–2 go by order; after that no single signal wins"
SUBTITLE = "Last two tokens copied from a prompt asking about its k-th sentence: where answers go"
HOW = "one bar per k, all answers; purple = same place in the list, dark grey = same entity."
ABSENT_TITLE = "Qwen3.6-27B, entity absent"  # the caption says from what
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


def newest_absent(root: Path = ABSENT_ROOT) -> Path | None:
    found = sorted(root.glob(ABSENT_GLOB))
    return found[-1] if found else None


def read_absent(path: Path, family: str = "RL") -> list[dict[str, str]]:
    """The absent run's decisive items by k (2-5) as table-like rows: counts per ABSENT_SEGS key (the shares times n,
    rounded: verdict.json keeps 4 decimals) and each share's Wilson interval in %; k = 1 has no decisive item."""
    by_k = json.loads(path.read_text())["families"][family]["by_k"]
    out = []
    for k in sorted(by_k, key=int):
        d = by_k[k]["decisive"]
        n = int(d["n"])
        if n == 0:
            continue
        r = {"k": k, "n": str(n), "runs": path.parent.name}
        for s in ABSENT_SEGS:
            got = d.get(ABSENT_SHARES.get(s.key, ""), [0.0, 0.0, 0.0])
            r[f"{s.key}_n"] = str(round(got[0] * n))
            r[f"{s.key}_lo"], r[f"{s.key}_hi"] = str(100 * got[1]), str(100 * got[2])
        if sum(int(r[f"{s.key}_n"]) for s in ABSENT_SEGS) != n:
            raise ValueError(f"{path}: k = {k}: the shares do not sum to n = {n}")
        out.append(r)
    return out


def shares(r: dict[str, str], segs: tuple[Seg, ...] = SEGS) -> dict[str, float]:
    """% of the bar's answers per segment, from the counts (they sum to n, so the bar ends at 100)."""
    n = int(r["n"])
    return {s.key: 100 * int(r[f"{s.key}_n"]) / n for s in segs}


def source_of(folder: Path) -> str:
    p = folder / "table.csv"
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


HALO = [patheffects.withStroke(linewidth=3.6, foreground="white")]  # an interval stays visible on any segment


def ci_line(ax, x: float, lo: float, hi: float) -> None:
    """A Wilson interval as a thin dark line on the bar's right edge (clear of the value written in the bar), across
    the segment edge it belongs to."""
    ax.plot([x, x], [lo, hi], color=C.INK, lw=C.ERRORBAR["elinewidth"], solid_capstyle="butt", gid="ci", zorder=3,
            path_effects=HALO)  # fmt: skip


def panel(ax, rows: list[dict[str, str]], key: tuple[str, str, str], source: str, sentences: int, *, main: bool,
          width: float = 0.62, segs: tuple[Seg, ...] = SEGS) -> list[C.Number]:  # fmt: skip
    """One model's stacked bars over k, the intervals and value labels on MAIN; returns the drawn Numbers. With
    ABSENT_SEGS (no same-entity outcome) the intervals and labels are order's at every k."""
    nums: list[C.Number] = []
    has_identity = any(s.key == "identity" for s in segs)
    for r in rows:
        k, sh = int(r["k"]), shares(r, segs)
        y = 0.0
        for s in segs:
            if sh[s.key] > 0:
                ax.bar(k, sh[s.key], width, bottom=y, color=s.color, lw=0, zorder=2)
            ci = None if s.key == "off_list" else (float(r[f"{s.key}_lo"]), float(r[f"{s.key}_hi"]))
            nums.append(C.Number(sh[s.key], f"% of answers: {s.key}", model=key[0], setting=key[2], ci=ci,
                                 n=int(r["n"]), source=source, extra={"family": key[1], "k": k, "outcome": s.key}))  # fmt: skip
            y += sh[s.key]
        if not main:
            continue
        ci_line(ax, k + width / 2, float(r["order_lo"]), float(r["order_hi"]))
        if has_identity:
            ci_line(ax, k + width / 2, 100 - float(r["identity_hi"]), 100 - float(r["identity_lo"]))
        if k <= 2 or not has_identity:
            val, at = sh["order"], sh["order"] / 2
        else:
            val, at = sh["identity"], 100 - sh["identity"] / 2
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


def column_key(fr: C.Frame, top_ax, low_ax, segs: tuple[Seg, ...] = SEGS) -> None:
    """The outcomes' names in stacking order (bottom to top), right of the panels, from the bottom of `low_ax` to the
    top of `top_ax` (one panel is too short for six names)."""
    a, b = top_ax.get_position(), low_ax.get_position()
    for i, s in enumerate(segs):
        y = b.y0 + i * (a.y1 - b.y0) / (len(segs) - 1)
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


def fit_title(fr: C.Frame) -> None:
    """Dan's title (23 Oct) is wider than the figure at common.TITLE: the largest whole point size that fits."""
    t = next(t for t in fr.fig.texts if t.get_gid() == "title")
    room = (0.985 - 0.03) * fr.fig.get_figwidth()
    size = C.TITLE
    while size > C.SUBTITLE and PS.text_width(fr.fig, t.get_text(), size, "bold") > room:
        size -= 1
    t.set_fontsize(size)


def unchanged_range(rows: Rows, model: str, family: str = "RL") -> str:
    """'56–69%': the model's unchanged shares over its pooled 5-sentence bars."""
    us = [shares(r)["unchanged"] for r in rows.get((model, family, SO.POOLED), [])]
    lo, hi = round(min(us)), round(max(us))
    return f"{lo}%" if lo == hi else f"{lo}–{hi}%"


def absent_panel(ax, path: Path) -> list[C.Number]:
    """The 27B with the copied prompt's entity absent from the original: the decisive items by k (2-5); k = 1 is
    marked not tested (order and the 1st sentence's digit are one digit there)."""
    nums = panel(ax, read_absent(path), ABSENT_KEY, source_of_file(path), 5, main=True, segs=ABSENT_SEGS)
    ax.text(1, 50, "not\ntested", ha="center", va="center", fontsize=C.NOTE, color=C.CAPTION_INK, style="italic",
            linespacing=1.1, gid="status")  # fmt: skip
    return nums


def source_of_file(p: Path) -> str:
    return str(p.relative_to(pins.REPO_ROOT)) if p.is_relative_to(pins.REPO_ROOT) else str(p)


def draw_main(folder: Path, out: Path = C.OUT, absent: Path | None = None) -> list[Path]:
    """MAIN: MAIN_MODELS' pooled 5-sentence bars, and (`absent`: the absent run's verdict.json) the 27B with the
    entity absent from the original as the second panel."""
    rows = read_table(folder)
    keys = [(m, "RL", SO.POOLED) for m in MAIN_MODELS if (m, "RL", SO.POOLED) in rows]
    if not keys:
        raise ValueError("no MAIN model has pooled 5-sentence rows")
    off = max(shares(r)["off_list"] for k in keys for r in rows[k])
    sets = {k[0]: len(rows[k][0]["runs"].split()) for k in keys}
    absent_rows = read_absent(absent) if absent else []
    gemma = f"Gemma's patch leaves {unchanged_range(rows, 'gemma')} unchanged." if ("gemma", "RL", SO.POOLED) in rows else ""  # fmt: skip
    caption = OI.pack([
        f"Recalled bridges, {'3 prompt sets' if set(sets.values()) == {3} else 'prompt sets'} pooled, "
        f"n = {n_range(rows, keys)}; lines: 95% CI.",
        gemma,
        (f"Entity absent: the copied prompt's entity is not in the original (n = "
         f"{min(int(r['n']) for r in absent_rows)}–{max(int(r['n']) for r in absent_rows)}).") if absent_rows else "",
        f"Off the list: {'none' if off == 0 else f'≤ {off:.1f}%'}." if not absent_rows else "",
        "Other models: full version.",
    ])  # fmt: skip
    fr = C.frame("main", TITLE, SUBTITLE, how=HOW, caption=caption, nrows=2, ncols=2, left=0.075, right=0.78,
                 wspace=0.12, hspace=0.62, panel_titles=True)  # fmt: skip
    fit_title(fr)
    nums: list[C.Number] = []
    source = source_of(folder)
    slots = list(fr.axes)
    panels: list[tuple[str, tuple[str, str, str] | None]] = [(C.MODEL[k[0]].name, k) for k in keys]
    if absent:
        panels.insert(1, (ABSENT_TITLE, None))
    for i, (ax, (title, key)) in enumerate(zip(slots, panels, strict=False)):
        if key is None:
            assert absent is not None
            nums += absent_panel(ax, absent)
        else:
            nums += panel(ax, rows[key], key, source, 5, main=True)
        y_axis(ax, i % 2 == 0)
        ax.set_title(title, fontsize=C.LABEL, fontweight="bold", pad=8, loc="left")
    for ax in slots[len(panels) :]:
        fr.fig.delaxes(ax)
    drawn = slots[: len(panels)]
    segs = KEY_SEGS if absent else SEGS
    segs = tuple(s for s in segs if s.key != "off_list" or off >= 1.0)
    right = drawn[1] if len(drawn) > 1 else drawn[0]
    low = drawn[3] if len(drawn) > 3 else right
    column_key(fr, right, low, segs)
    x_label(fr, drawn[-2:] if len(drawn) > 2 else drawn)
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
    fit_title(fr)
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
    ap.add_argument("--absent", type=Path, default=None,
                    help="a results/absent_entity/<run> folder (default: the newest; 'none': no absent panel)")  # fmt: skip
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    folder = a.table or newest_table()
    absent = None if str(a.absent) == "none" else (a.absent / "verdict.json" if a.absent else newest_absent())
    for kind in ("main", "full"):
        if a.only in (None, kind):
            paths = draw_main(folder, a.out, absent) if kind == "main" else draw_full(folder, a.out)
            for p in paths:
                print(p.relative_to(pins.REPO_ROOT) if p.is_relative_to(pins.REPO_ROOT) else p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
