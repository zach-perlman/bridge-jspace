"""split_depth (F1, the hero figure for claim C3; Dan, 23 Oct): lookups let go of the J-space form before recall does.

J-dependence of a family at a cell = (F(whole) - F(without J)) / F(whole), F = the share switched to the new bridge's
answer (role b) when the stated bridge's change (or a part of it) is pasted back: part "full", "not_jspace". The same
edit for both questions: lookups (family PP) and recalls (PM) at the same cell. The control, where a run has it: the
change without a random part of J's share ("not_rand_sub"), (F(whole) - F(without rand)) / F(whole), drawn for lookups
(recalls lose <= the caption's figure to it). Rows: statement_positions parts runs, source "cf", not the null. Interval:
95% percentile bootstrap over items (paired: the same items under whole and without; 2000 draws, seed 0).

x = depth (% of the model's layers, pins n_layers). Filled: the stated bridge's word (bridge_word; the 122B's layers 33
and 36 at its sentence, bind_bridge: its late run has no word cells); hollow: the change pasted over the whole context
("context"), a different position set.

The split (read after seeing the data, 23 Oct; confirmation pending): the first tested layer at which, on any position
set, the lookups' J-dependence is at the random level (its 95% interval reaches the random-part removal's interval;
where no random part was removed, reaches 0) and the recalls' lower bound is above the lookups' upper bound.

Rates are checked against the run's d1_verdict verdict.json wherever one judges the cell (a mismatch raises).

MAIN: 9B, 27B, 122B. FULL: also OLMo-3, the 27B's context cells at layers 36-40 and the 9B's at 16-18 (rest_size run).

uv run python scripts/figs/split_depth.py [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import functools
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np

from bridge_jspace import pins
from scripts.figs import common as C
from scripts.figs import stated_bridge as SB

STEM = "split_depth"
SP = C.REPO / "results" / "statement_positions"
VERDICTS = C.REPO / "results" / "d1_verdict"
FAMILY = {"lookups": "PP", "recalls": "PM"}
TARGET = {"9b": "qwen3.5-9b", "27b": "qwen3.6-27b", "122b": "qwen3.5-122b-a10b", "olmo": "olmo-3-7b-instruct-jpp"}
N_BOOT, SEED = 2000, 0
# (model, run, position set, layers, hollow, FULL only)
CELLS: tuple[tuple[str, str, str, tuple[int, ...], bool, bool], ...] = (
    ("9b", "qwen35_9b_d1_necessity_parts_r2", "bridge_word", (6, 8, 10, 12, 14), False, False),
    ("9b", "qwen35_9b_d1_rest_size_parts_r2", "context", (16, 18), True, True),
    ("27b", "d1_necessity_parts_27b_r2", "bridge_word", (16, 20, 24, 28), False, False),
    ("27b", "d1_topics2_parts_27b", "context", (32,), True, False),
    ("27b", "d1_topics2_parts_27b", "context", (36, 40), True, True),
    ("122b", "qwen35_122b_d1_topics2_parts", "bridge_word", (24, 27, 30), False, False),
    ("122b", "qwen35_122b_d1_late_parts", "bind_bridge", (33, 36), False, False),
    ("122b", "qwen35_122b_d1_topics2_parts", "context", (24, 27, 30), True, False),
    ("122b", "qwen35_122b_d1_late_parts", "context", (33, 36), True, False),
    ("olmo", "olmo3_7b_instruct_jpp_d1_necessity_parts_r2", "bridge_word", (6, 8, 10, 12, 14), False, True),
)
PANELS = {"main": ("9b", "27b", "122b"), "full": ("9b", "27b", "122b", "olmo")}

TITLE = "Lookups let go of the J-space form before recall does"
SUBTITLE = "Share of the switch lost when the change's lens-readable part (J) is removed"
HOW = "1 = the switch needs J, 0 = not at all. Grey: a random part of J's size removed."
CAPTION1 = (
    "Same edit for both questions; split depth read after seeing the data; confirmation pending (rule fixed 23 Oct)."
)
WHY_SPLIT = ("first layer where lookups' 95% CI reaches the random-part removal's (none run: 0) and recalls' lower "
             "bound is above lookups' upper")  # fmt: skip


@dataclass
class Dep:
    """J-dependence at one cell and family: point and 95% interval (0-1), the rates it comes from, n."""

    value: float
    lo: float
    hi: float
    f_whole: float
    f_without: float
    n: int


@dataclass
class Cell:
    model: str
    run: str
    where: str
    layer: int
    hollow: bool
    full_only: bool
    dep: dict[str, Dep]  # lookups / recalls
    rand: dict[str, Dep]  # the random-part removal, where the run has it

    @property
    def depth(self) -> float:
        return 100 * self.layer / n_layers(self.model)


def n_layers(model: str) -> int:
    return int(pins.TARGETS[TARGET[model]]["n_layers"])


@functools.cache
def items_of(path: Path) -> dict[tuple[str, int, str], dict[str, dict]]:
    """(set, layer, family) -> item name -> {part: switched (role b)}: the cf rows, not the null."""
    out: dict[tuple[str, int, str], dict[str, dict]] = defaultdict(dict)
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r["source"] != "cf" or r["null"]:
            continue
        d = out[(r["set"], int(r["layer"]), r["family"])].setdefault(r["name"], {})
        if r["part"] in d:
            raise ValueError(f"{path}: two rows for {r['name']} {r['set']} {r['layer']} {r['part']}")
        d[r["part"]] = r["role"] == "b"
    return dict(out)


def dependence(items: dict[str, dict], minus: str, n_boot: int = N_BOOT, seed: int = SEED) -> Dep | None:
    """(F(whole) - F(minus)) / F(whole) over the items that have both parts, with a paired item bootstrap."""
    names = sorted(k for k, v in items.items() if "full" in v and minus in v)
    if not names:
        return None
    w = np.array([items[k]["full"] for k in names], dtype=float)
    m = np.array([items[k][minus] for k in names], dtype=float)
    if w.sum() == 0:
        return None
    pick = np.random.default_rng(seed).integers(0, len(names), size=(n_boot, len(names)))
    ws, ms = w[pick].sum(1), m[pick].sum(1)
    ok = ws > 0
    boots = (ws[ok] - ms[ok]) / ws[ok]
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return Dep(float((w.sum() - m.sum()) / w.sum()), float(lo), float(hi), float(w.mean()), float(m.mean()),
               len(names))  # fmt: skip


@functools.cache
def verdict_cells(run: str, root: Path = VERDICTS) -> dict[str, dict]:
    """The cells of every d1_verdict verdict.json judging `run` (set:layer -> cell), {} when none does."""
    out: dict[str, dict] = {}
    for p in sorted(root.glob("*/verdict.json")):
        v = json.loads(p.read_text())
        if v.get("parts") == run:
            out.update(v.get("cells") or {})
    return out


def check_verdict(cell: Cell, root: Path = VERDICTS) -> int:
    """Raise when a rate this figure uses differs from the verdict file's; returns how many rates were compared."""
    vc = verdict_cells(cell.run, root).get(f"{cell.where}:{cell.layer}")
    if not vc:
        return 0
    k = 0
    for fam, key in (("lookups", "lookup"), ("recalls", "recall")):
        d = cell.dep.get(fam)
        if d is None or key not in vc:
            continue
        pairs = [("full", d.f_whole), ("not_jspace", d.f_without)]
        if fam in cell.rand:
            pairs.append(("not_rand_sub", cell.rand[fam].f_without))
        for part, mine in pairs:
            if part in vc[key] and abs(vc[key][part][0] - mine) > 1e-9:
                raise ValueError(f"{cell.run} {cell.where}:{cell.layer} {fam} {part}: {mine} here, "
                                 f"{vc[key][part][0]} in the verdict file")  # fmt: skip
            k += part in vc[key]
    return k


def load(sp: Path = SP, cells=CELLS, verdicts: Path = VERDICTS) -> list[Cell]:
    out = []
    for m, run, where, layers, hollow, full_only in cells:
        rows = items_of(sp / run / "outcomes.jsonl")
        for la in layers:
            dep, rand = {}, {}
            for fam, family in FAMILY.items():
                it = rows.get((where, la, family))
                if not it:
                    continue
                if (d := dependence(it, "not_jspace")) is not None:
                    dep[fam] = d
                if (r := dependence(it, "not_rand_sub")) is not None:
                    rand[fam] = r
            if "lookups" not in dep:
                raise ValueError(f"split_depth: no lookups at {run} {where} layer {la}")
            c = Cell(m, run, where, la, hollow, full_only, dep, rand)
            check_verdict(c, verdicts)
            out.append(c)
    return out


def split_of(cells: list[Cell]) -> int | None:
    """The first tested layer where, on any position set, lookups are at the random level and recalls well above."""
    for la in sorted({c.layer for c in cells}):
        for c in (c for c in cells if c.layer == la):
            look, rec = c.dep.get("lookups"), c.dep.get("recalls")
            if look is None or rec is None:
                continue
            ref = c.rand.get("lookups")
            at_random = look.lo <= (ref.hi if ref is not None else 0.0)
            if at_random and rec.lo > look.hi:
                return la
    return None


# ---------------------------------------------------------------- drawing


def number(c: Cell, fam: str, d: Dep, what: str) -> C.Number:
    path = SP / c.run / "outcomes.jsonl"
    return C.Number(d.value, what, model=c.model, setting=f"{c.where}, layer {c.layer}", ci=(d.lo, d.hi), n=d.n,
                    source=str(path.relative_to(C.REPO)),
                    extra={"family": FAMILY[fam], "set": c.where, "layer": c.layer, "depth": c.depth,
                           "F_whole": d.f_whole, "F_without": d.f_without, "hollow": c.hollow})  # fmt: skip


def series(ax, cs: list[Cell], fam: str, color: str, hollow: bool) -> None:
    cs = sorted((c for c in cs if fam in c.dep), key=lambda c: c.layer)
    if not cs:
        return
    xs, ds = [c.depth for c in cs], [c.dep[fam] for c in cs]
    for x, d in zip(xs, ds, strict=True):
        ax.plot([x, x], [d.lo, d.hi], color=color, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"], zorder=3,
                gid="ci")  # fmt: skip
    ax.plot(xs, [d.value for d in ds], color=color, lw=1.4 if hollow else 2.6, linestyle=(0, (2, 2)) if hollow else "-",
            marker="o", markersize=8, markerfacecolor="white" if hollow else color, markeredgecolor=color,
            markeredgewidth=2.0, zorder=4, gid="mark")  # fmt: skip


def draw_panel(ax, cs: list[Cell], split: int | None, model: str) -> list[C.Number]:
    nums: list[C.Number] = []
    filled = [c for c in cs if not c.hollow]
    rnd = sorted((c for c in filled if "lookups" in c.rand), key=lambda c: c.layer)
    if rnd:
        xs = [c.depth for c in rnd]
        ax.fill_between(xs, [c.rand["lookups"].lo for c in rnd], [c.rand["lookups"].hi for c in rnd], color=C.CHANCE,
                        lw=0, zorder=1)  # fmt: skip
        ax.plot(xs, [c.rand["lookups"].value for c in rnd], color=C.CONTROL, lw=2.0, zorder=2, gid="mark")
    for c in cs:
        for fam, d in c.rand.items():
            nums.append(number(c, fam, d, f"{fam}: share lost without a random part of J's share"))
    for hollow in (False, True):
        part = [c for c in cs if c.hollow == hollow]
        series(ax, part, "recalls", C.RECALL, hollow)
        series(ax, part, "lookups", C.LOOKUP, hollow)
        for c in part:
            for fam, d in c.dep.items():
                nums.append(number(c, fam, d, f"{fam}: J-dependence (share lost without J)"))
    if split is not None:
        x = 100 * split / n_layers(model)
        ax.axvline(x, color=C.INK2, lw=1.0, zorder=0)
        nums.append(C.Number(float(split), "split layer (read after seeing the data)", model=model,
                             source="read after seeing the data (rule fixed 23 Oct); confirmation pending",
                             extra={"depth": x, "n_layers": n_layers(model), "rule": WHY_SPLIT}))  # fmt: skip
    ax.axhline(0, color=C.CONTROL, lw=0.8, zorder=0)
    ax.set_xlim(15, 80)
    ax.set_xticks([20, 40, 60, 80])
    ax.set_ylim(-0.1, 1.05)
    ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    return nums


def label_lines(ax, cs: list[Cell]) -> None:
    """'lookups', 'recalls', 'random part' by their lines in the first panel (the first free spot)."""
    from scripts.figs import layer_gap as LG

    p = LG.Placer(ax)
    filled = sorted((c for c in cs if not c.hollow), key=lambda c: c.layer)
    for text, color, pts in (
        ("recalls", C.RECALL, [(c.depth, c.dep["recalls"].value, c.dep["recalls"].hi, c.dep["recalls"].lo)
                               for c in filled if "recalls" in c.dep]),
        ("lookups", C.LOOKUP, [(c.depth, c.dep["lookups"].value, c.dep["lookups"].hi, c.dep["lookups"].lo)
                               for c in filled]),
        ("random part", C.CAPTION_INK, [(c.depth, c.rand["lookups"].value, c.rand["lookups"].hi, c.rand["lookups"].lo)
                                        for c in filled if "lookups" in c.rand]),
    ):  # fmt: skip
        below = [(x, lo - 0.03, "left", "top") for x, _, _, lo in pts]
        spots = [(x + 1.2, v + 0.05, "left", "bottom") for x, v, _, _ in pts]
        spots += [(x, hi + 0.04, "center", "bottom") for x, _, hi, _ in pts]
        spots = below + spots if text == "random part" else spots + below
        p.put(text, spots, color=color, fontweight="bold")


def caption(kind: str, cells: list[Cell]) -> str:
    ns = sorted({d.n for c in cells for d in c.dep.values()})
    n = f"n = {ns[0]}" if len(ns) == 1 else f"n = {ns[0]}–{ns[-1]}"
    line2 = f"Hollow: pasted over the whole context. 122B: no random-part run; layers 33–36 at the sentence. {n}."
    return CAPTION1 + "\n" + line2


def figure(kind: str, cells: list[Cell]) -> tuple[C.Frame, list[C.Number]]:
    keys = PANELS[kind]
    cells = [c for c in cells if c.model in keys and (kind == "full" or not c.full_only)]
    size = None if kind == "main" else (12.0, 9.0)
    nrows, ncols = (1, 3) if kind == "main" else (2, 2)
    fr = C.frame(kind, TITLE, SUBTITLE, how=HOW, caption=caption(kind, cells), nrows=nrows, ncols=ncols, size=size,
                 sharey=True, sharex=True, left=0.085, right=0.975, wspace=0.12, hspace=0.45)  # fmt: skip
    SB.shift(fr, top=30)
    for t in fr.fig.texts:  # Dan's title is 0.3% wider than the frame's margin allows: start it nearer the edge
        if t.get_gid() == "title":
            t.set_x(0.012)
    nums: list[C.Number] = []
    for i, (ax, m) in enumerate(zip(fr.axes, keys, strict=True)):
        mine = [c for c in cells if c.model == m]
        split = split_of(mine)
        nums += draw_panel(ax, mine, split, m)
        right = "no split" if split is None else f"split: layer {split}"
        SB.head(ax, C.MODEL[m].name, right, right_size=C.NOTE)
        if i % ncols == 0:
            ax.set_ylabel("J-dependence")
        else:
            ax.tick_params(axis="y", labelleft=False)
        if i // ncols == nrows - 1:
            ax.set_xlabel("depth (% of layers)")
        else:
            ax.tick_params(axis="x", labelbottom=False)
        if i == 0:
            label_lines(ax, mine)
    return fr, nums


def splits(cells: list[Cell]) -> dict[str, int | None]:
    return {m: split_of([c for c in cells if c.model == m]) for m in PANELS["full"]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    cells = load()
    print("splits:", splits(cells))
    for kind in ("main", "full"):
        if a.only in (None, kind):
            fr, nums = figure(kind, cells)
            for p in C.save(fr, STEM, nums, a.out):
                print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
