"""cross_model_figures: the merged figures, every model in one figure per finding (Dan's post-run brief, section 2).

Each cell's value, 95% interval, n and verdict come from the newest grid (results/cross_model/<stamp>/grid.json,
written by scripts/cross_model_grid.py; or --grid DIR). Where a figure needs more than the grid's one number per cell
(the DeltaNet arm, the digit-only arm, the rivals of the order slot, the recall arm, the gates' other bridge, a curve by
layer or by asked sentence), it reads the files the grid names for that cell with the repo's own functions
(d2_formats, d2_parts, finding5_confirm, pointer_swap, early_push_where), and where the grid has the same number it
checks it: a cell whose files disagree with the grid is drawn as missing ("files inconsistent"), never patched.

Figures (figures/archive/cross_model/<name>.png at 200 dpi and .svg, 16:9):
  f_late_read_all_models                a  finding 4: % right with the answer's sentence hidden from the last tokens,
                                           against the DeltaNet layers (hybrids) and another sentence hidden instead
  f_digit_not_name_all_models           b  finding 3: only the digit vs only the name left visible, per format
  f_order_then_identity_all_models      c  finding 5: same place minus the donor entity's sentence, by asked sentence,
                                           lists of 5, 8 and 12 sentences
  f_counts_list_order_not_text_all_models  d  finding 6: the order in the list vs the place in the text (or the end)
  f_patch_outcomes_by_depth_all_models  e  the last-two-token patch's outcomes by depth (% of the model's layers)
  f_lookup_ignores_lens_part_all_models f  finding 2: recalls minus lookups switched by the lens part (the contrast,
                                           Newcombe interval), the rates behind it, and the lens gates
  f_lens_push_recall_not_lookup_all_models  g  finding 7: the lens push by depth, lookups vs recalls, valid cells only,
                                           the main and the amended rule's cells marked, their values printed
  f_layer_gap_lens_vs_patch_27b         g  the 27B's layer-gap test: lens push vs full patch vs embedding push vs
                                           random, the gap between the stops drawn and printed
Style: src/bridge_jspace/plot_style.py (one Okabe-Ito color per model; filled markers for hybrids, hollow for
attention-only; one extra color, lavender, only for the decisive comparison). Dot figures: the compared arms on the
row line joined by the highlight, each value printed beside its point (white halo; two values too close for two
labels as one, "6 vs 10%"), n and the verdict right of each panel, the rule's bars dotted and labelled above, chance
or the control dashed and labelled in place; rate axes shared within a figure and cut to the data's span.
"not interpretable" is hatched grey with the failed control; "not testable" and "missing" are blank with a label.
Every model appears in every figure (the layer-gap figure is one model's test by design). Titles state each
figure's outcome, computed from its cells (title_*), and the subtitle what was measured.

Labels: a Placer puts each value label at the first free place (beside its point on the row line, then in a lane
above or below the row with a short leader line, then farther along the lane), free meaning touching no text and no
marker, interval, gap bar or tick as drawn. The decisive arm's value is placed first and never left out; a
comparison's only where it fits near its point.

Overlaps: every figure is drawn, checked with plot_style.overlaps (every drawn text, boxes grown by 2 px: no two
texts intersect, no text sits on a marker, interval, gap bar or tick, none leaves the figure, no value or status
label leaves its panel) and drawn again with the next LAYOUTS step until none is left: (1) model names on two lines,
(2) tick labels at the axis ends only, (3) the comparison arms' value labels left out (never the decisive arm's).
Not applicable: decimals (none are printed), the legend (always outside the panels), more rows of panels (the rows
of eight models are at their minimum height). If a figure still has an overlap the script saves it, names it and the
colliding texts and exits 1.

Prints, per figure, "figure NAME: K overlaps (layout step S)" and how many cells have a value; with --titles also
its title (results open only). Colliding texts that could carry a value are named by role unless --titles is given.

uv run python scripts/cross_model_figures.py [--grid DIR] [--out figures/cross_model] [--only NAME[,...]] [--titles]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
import textwrap
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.transforms import Bbox

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace import plot_style as S
from bridge_jspace.stats import wilson
from scripts import cross_model_grid as G
from scripts import d2_formats as DF
from scripts import d2_parts as DP

OUT = pins.REPO_ROOT / "figures" / "archive" / "cross_model"
Triple = tuple[float, float, float]
VALUE_WORDS = ("holds", "fails", "inconclusive", "open")
LAYER_GAP_RUN = "d4_layer_gap_v2_27b"  # jobs/d4/d4_layer_gap_v2_27b.yaml (the 27B only; not a grid cell)
TARGET = {"27b": "qwen3.6-27b", "9b": "qwen3.5-9b", "olmo_hybrid": "olmo-hybrid-7b-instruct-dpo",
          "122b": "qwen3.5-122b-a10b", "32b": "qwen3-32b", "olmo": "olmo-3-7b-instruct", "muse": "muse-glimmer-30b",
          "gemma": "gemma-4-31b-it"}  # fmt: skip
FORMAT_OF = {v: k for k, v in G.FORMAT_SETTING.items()}  # grid setting -> d2_formats format


def n_layers(model: str) -> int:
    return int(pins.TARGETS[TARGET[model]]["n_layers"])


def tri(v: Any) -> Triple:
    return (float(v[0]), float(v[1]), float(v[2]))


def finite(t: Triple | None) -> bool:
    return t is not None and not any(math.isnan(x) for x in t)


# ---------------------------------------------------------------- the grid's rows and their status


class Grid:
    """grid.json's main-lens rows, one per grid.md cell: (model, finding, setting) -> row."""

    def __init__(self, rows: list[dict]):
        self.rows: dict[tuple[str, str, str], dict] = {}
        for r in rows:
            s = r.get("md_setting")
            if s is not None and r.get("role", "main") == "main":
                self.rows.setdefault((r["model"], r["finding"], s), r)

    def get(self, model: str, finding: str, setting: str) -> dict | None:
        return self.rows.get((model, finding, setting))


def latest_grid(root: Path = G.OUT) -> Path:
    hits = sorted(d for d in root.glob("*") if (d / "grid.json").exists())
    if not hits:
        raise SystemExit(f"no grid.json under {root}: run scripts/cross_model_grid.py first")
    return hits[-1]


def word(verdict: str) -> str:
    return next((v for v in G.VERDICTS if verdict.startswith(v)), "missing")


# (verdict word, words in the grid's verdict, the short reason drawn in the figure); the first match wins
REASONS = (
    ("not testable", "no lens", "no lens"),
    ("not testable", "gate v1 failed", "lens gate failed"),
    ("not testable", "precheck", "stopped by precheck"),
    ("not testable", "before the donor's digit", "no early layer"),
    ("not testable", "competence", "no items"),
    ("not interpretable", "off-path", "off-path control"),
    ("not interpretable", "random-patch", "random-patch control"),
    ("not interpretable", "positive control", "positive control"),
    ("not interpretable", "writes recall", "positive control"),
    ("not interpretable", "does not write recall", "positive control"),
    ("not interpretable", "G2", "removal control"),
    ("not interpretable", "rotated control", "rotated control"),
    ("not interpretable", "keep their answer", "lookups break"),
    ("not interpretable", "lookup write is", "lookup write unclear"),
    ("not interpretable", "no recall row", "no recall rows"),
    ("missing", "no spec", "not planned"),
    ("missing", " failed at the ", "run failed"),
    ("missing", "pending", "queued"),
    ("missing", "running", "running"),
    ("missing", "waits on", "blocked"),
    ("missing", "amended-rule", "not analyzed"),
    ("missing", "no saved verdict", "no verdict yet"),
    ("missing", "no stated-bridge verdict", "no verdict yet"),
    ("missing", "not here (pull?)", "not pulled"),
    ("missing", "not run", "not run"),
    ("missing", "raw smoke mismatch", "smoke mismatch"),
    ("missing", "Zach's branch", "not on branch"),
    ("missing", "inconsistent", "files inconsistent"),
    ("missing", "first version", "old run version"),
    ("missing", "items in the run", "no items"),
)
FALLBACK = {"not testable": "see the grid", "not interpretable": "a control failed", "missing": "see the grid"}


def short_reason(w: str, verdict: str) -> str:
    return next((label for ww, phrase, label in REASONS if ww == w and phrase in verdict), FALLBACK.get(w, w))


def has_run(row: dict | None) -> bool:
    return bool(row) and row.get("status") == "has-run"  # type: ignore[union-attr]


# ---------------------------------------------------------------- what a figure draws


@dataclass
class Mark:
    """One model in one panel of a dot figure: per series a value with its 95% interval (0-1), or a label."""

    model: str
    status: str = "missing"  # value, not interpretable, not testable, missing
    reason: str = "not in the grid"
    verdict: str = ""  # holds, fails, inconclusive, open (status value only)
    n: int | str | None = None
    note: str = ""
    points: dict[str, Triple] = field(default_factory=dict)
    ticks: dict[str, float] = field(default_factory=dict)  # per-row short lines: "bar" (dotted), "null" (dashed)
    why: str = ""  # the grid's whole verdict (its reason too), for the title


@dataclass
class Series:
    key: str
    x: list[float] = field(default_factory=list)
    y: list[Triple | None] = field(default_factory=list)
    status: str = "value"
    reason: str = ""
    verdict: str = ""
    n: int | None = None


@dataclass
class Panel:
    """One model (or one place, for the layer-gap figure) in a curve figure."""

    model: str
    status: str = "missing"
    reason: str = "not in the grid"
    series: list[Series] = field(default_factory=list)
    marks: dict[str, float] = field(default_factory=dict)  # x positions: "main", "amended", "used", "stop <arm>"
    n_text: str = ""
    notes: list[str] = field(default_factory=list)


@dataclass
class DotData:
    panels: tuple[str, ...]
    marks: dict[tuple[str, str], Mark] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


@dataclass
class CurveData:
    panels: dict[str, Panel] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def mark_of(model: str, row: dict | None, series: str) -> Mark:
    """The grid row as a mark: its value under `series`, or its status as a label."""
    if row is None:
        return Mark(model)
    w = word(row["verdict"])
    if w not in VALUE_WORDS:
        return Mark(model, w, short_reason(w, row["verdict"]), n=row.get("n"))
    if row.get("value") is None or not row.get("ci"):
        return Mark(model, "missing", "no value in grid")
    lo, hi = row["ci"]
    return Mark(model, "value", "", w, row.get("n"), points={series: (float(row["value"]), float(lo), float(hi))},
                why=row["verdict"])  # fmt: skip


def broken(model: str, errors: list[str], where: str, e: Exception) -> Mark:
    errors.append(f"{S.MODEL[model].label} / {where}: {type(e).__name__}")
    return Mark(model, "missing", "files inconsistent" if isinstance(e, Inconsistent) else "unreadable files")


# ---------------------------------------------------------------- the extra numbers: from the files the grid names


class Source(Protocol):
    def late_arms(self, row: dict) -> dict[str, Triple | None]: ...
    def name_digit(self, row: dict) -> dict[str, Triple]: ...
    def order_by_k(self, row: dict) -> dict[str, Any]: ...
    def counting(self, row: dict) -> dict[str, Triple]: ...
    def stated_bridge(self, row: dict) -> dict[str, Any]: ...
    def gate_other(self, row: dict) -> Triple: ...
    def outcomes_by_depth(self, row: dict) -> dict[str, Any]: ...
    def push_by_layer(self, row: dict) -> dict[str, Any]: ...
    def layer_gap(self) -> dict[str, Any] | None: ...


class Inconsistent(Exception):
    """A number read here differs from the grid's: the cell is drawn as missing."""


def layer_in(control: str, pattern: str) -> str:
    m = re.search(pattern, control or "")
    if not m:
        raise Inconsistent("no layer in the grid's control text")
    return m.group(1)


def diff_by_k(rows: list[dict], layer: str, sentences: int, family: str = "RL") -> dict[str, Any]:
    """Per place k of the donor's asked statement: position - identity with finding5_confirm's interval (its diff:
    the entity-cluster bootstrap within topic), on rows FC.select prepared; and the pooled 1st-2nd point (the grid's)."""
    from scripts import finding5_confirm as FC

    sel = [r for r in rows if r["family"] == family and str(r["layer"]) == str(layer)]
    ks: list[float] = []
    ys: list[Triple | None] = []
    for k in range(1, sentences + 1):
        sub = [r for r in sel if r["_k"] == k]
        if sub:
            ks.append(k)
            ys.append(tri(FC.diff(sub, "position", "identity")))
    first2 = [r for r in sel if r["_k"] <= 2]
    return {
        "k": ks,
        "diff": ys,
        "n": len(sel),
        "first2": FC.diff(first2, "position", "identity")[0] if first2 else None,
    }


def roles_by_layer(rows: list[dict], level: str | None = None, family: str = "RL") -> dict[str, Any]:
    """pointer_swap outcomes at the last two tokens (source dissoc): per numeric layer, the share of patched answers
    that went to the same position, the donor's entity (identity) and the donor's own answer (value), Wilson 95%."""
    by: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    for o in rows:
        if o["source"] != "dissoc" or o["group"] != "last" or o["family"] != family:
            continue
        if (level is not None and o["level"] != level) or not str(o["layer"]).lstrip("-").isdigit():
            continue
        by[int(o["layer"])][o["role"]] += 1
    layers = sorted(by)
    out: dict[str, Any] = {"layers": layers, "n": max((sum(by[la].values()) for la in layers), default=0)}
    for role in ("position", "identity", "value"):
        out[role] = [tri(wilson(by[la][role], sum(by[la].values()))) for la in layers]
    return out


def best_valid_by_layer(cells: dict, layers: list[int], scales: list[float]) -> dict[str, Any]:
    """Per layer, among the valid cells (early_push_where's cell_valid: rule v2's off-path check) with a recall row,
    the one whose lens push switches the most recalls (decide's ties: smaller scale, the word before the sentence):
    its lookup and recall rates and the random push on lookups there. None where a layer has no valid cell."""
    from scripts import early_push_where as EPW

    out: dict[str, Any] = {"layers": list(layers), "lookup": [], "recall": [], "random": []}
    for la in layers:
        cands = [(sub, la, sc) for sub in ("w", "s") for sc in scales
                 if cells.get(("BR", sub, la, sc, "lens")) and EPW.cell_valid(cells, (sub, la, sc))[0]]  # fmt: skip
        if not cands:
            for k in ("lookup", "recall", "random"):
                out[k].append(None)
            continue
        best = min(cands, key=lambda c: (-EPW.cell_rate(cells[("BR", *c, "lens")])[0], c[2], 0 if c[0] == "w" else 1))
        out["lookup"].append(tri(EPW.cell_rate(cells.get(("BL", *best, "lens"), {}))))
        out["recall"].append(tri(EPW.cell_rate(cells[("BR", *best, "lens")])))
        out["random"].append(tri(EPW.cell_rate(cells.get(("BL", *best, "random"), {}))))
    return out


def arm_curve(cells: dict, sub: str, layers: list[int], arm: str) -> list[Triple | None]:
    """Per layer, the arm's valid cell (early_push_where.arm_cells) with the highest upper bound on lookups switched:
    the cell that decides whether the arm stops there (the layer-gap rule v2)."""
    from scripts import early_push_where as EPW

    out: list[Triple | None] = []
    for la in layers:
        rs = [EPW.cell_rate(cells[k]) for k in EPW.arm_cells(cells, sub, la, arm)]
        out.append(tri(max(rs, key=lambda r: r[2])) if rs else None)
    return out


class FileSource:
    """The extra numbers, from the files behind each grid cell, each checked against the grid where it has them."""

    def __init__(self) -> None:
        self.cells: dict[tuple[str, str, str], G.Cell] = {}
        for c in G._cells():
            self.cells.setdefault((c.model, c.finding, c.run), c)

    @staticmethod
    def same(x: float | None, row: dict) -> None:
        v = row.get("value")
        if v is not None and (x is None or abs(float(x) - float(v)) > 1e-9):
            raise Inconsistent("the files give another number than the grid")

    def late_arms(self, row: dict) -> dict[str, Triple | None]:
        """The late-read rule's two controls: the off-path sentence hidden instead (every model), and the answer's
        sentence hidden in every DeltaNet layer instead (hybrids; None elsewhere)."""
        fmt = FORMAT_OF.get(row["setting"])
        if fmt:
            res = G.formats_eval(row["run"])[fmt]["late_MP"]
        else:
            rows = G.jl(G.RESULTS / "attn_knockout" / row["run"] / "rows.jsonl")
            ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
            res = DF.late_read(rows, ok, "RL")
        self.same(res["lookup"][0], row)
        return {"off": tri(res["off"]), "deltanet": tri(res["deltanet"]) if "deltanet" in res else None}

    def name_digit(self, row: dict) -> dict[str, Triple]:
        fmt = FORMAT_OF.get(row["setting"])
        if fmt:
            cl, fam = G.formats_eval(row["run"])[fmt]["cells"], "MP"
        else:
            d = G.RESULTS / "attn_knockout" / row["run"]
            cases = {c["id"]: c for c in G.jl(d / "cases.jsonl")}
            cl, fam = DP.cells(G.jl(d / "rows.jsonl"), cases), "RL"
        name, digit = cl[(fam, "lookup_noname", "final")], cl[(fam, "lookup_nodigit", "final")]
        self.same(name["right"][0], row)
        return {"name": tri(name["right"]), "digit": tri(digit["right"])}

    def order_by_k(self, row: dict) -> dict[str, Any]:
        from scripts import finding5_confirm as FC
        from scripts import pointer_swap as PS

        cell = self.cells[(row["model"], "f5", row["run"])]
        sentences = cell.opts.get("sentences", FC.SENTENCES)
        d = G.RESULTS / "pointer_swap" / row["run"]
        m = json.loads((d / "manifest.json").read_text())
        items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
        rows = FC.select(G.jl(d / "outcomes.jsonl"), items, cell.opts.get("level"), sentences)
        got = diff_by_k(rows, layer_in(row["control"], r"layer (\S+) \("), sentences)
        self.same(got["first2"], row)
        return got

    def counting(self, row: dict) -> dict[str, Triple]:
        from scripts import pointer_swap as PS

        layer = layer_in(row["control"], r"shown at layer (\S+);")
        d = G.RESULTS / "pointer_swap" / row["run"]
        saved = sorted(p for p in d.glob("analysis-*/summary.json") if json.loads(p.read_text()).get("v4x"))
        if saved:  # as cross_model_grid.ev_f6: the saved analysis, else pointer_swap's own analysis
            v4x = json.loads(saved[-1].read_text())["v4x"]
        else:
            m = json.loads((d / "manifest.json").read_text())
            v4x = PS.v4x_tests(m, PS.analyze(m, G.jl(d / "outcomes.jsonl"), G.jl(d / "checks.jsonl"))["rates"])
        lv, rivals = next((lv, rv) for s, lv, _, rv in G.V4X if s == row["setting"])
        c = v4x["cells"][f"{lv}|{layer}|all"]
        self.same(c["winner"][0], row)
        return {G.RIVAL[r]: tri(c[r]) for r in rivals}

    def stated_bridge(self, row: dict) -> dict[str, Any]:
        v = json.loads((G.REPO / row["path"]).read_text())
        self.same(v["lookup"]["jspace"][0], row)
        return {"lookup_lens": tri(v["lookup"]["jspace"]), "lookup_rest": tri(v["lookup"]["not_jspace"]),
                "lookup_n": int(v["lookup"]["jspace"][3]),
                "recall_lens": tri(v["recall"]["jspace"]), "recall_n": int(v["recall"]["jspace"][3]),
                "lookup_null": tri(v["nulls"]["lookup_jspace_null"]),
                "recall_null": tri(v["nulls"]["recall_jspace_null"])}  # fmt: skip

    def gate_other(self, row: dict) -> Triple:
        s = json.loads((G.REPO / row["path"]).read_text())
        g = s["gate" if row["setting"].startswith("v1") else "gate_v2"]
        self.same(g["bridge_top10"][0], row)
        return tri(g["x_top10"])

    def outcomes_by_depth(self, row: dict) -> dict[str, Any]:
        cell = self.cells[(row["model"], "f5", row["run"])]
        got = roles_by_layer(G.jl(G.RESULTS / "pointer_swap" / row["run"] / "outcomes.jsonl"), cell.opts.get("level"))
        m = re.search(r"layer (\d+) \(", row.get("control") or "")
        return {**got, "n_layers": n_layers(row["model"]), "used": int(m.group(1)) if m else None}

    def push_by_layer(self, row: dict) -> dict[str, Any]:
        from scripts import early_push_where as EPW

        m, cells, _, _ = EPW.load_cells(row["run"])
        cfg = m["config"]
        got = best_valid_by_layer(cells, cfg["layers"], cfg["scales"])
        d = EPW.RESULTS / row["run"]
        main = json.loads((d / "summary.json").read_text())["decision"].get("primary")
        am_files = sorted(d.glob("analysis-v2.1-*/summary.json"))  # as cross_model_grid.ev_d4
        am = json.loads(am_files[-1].read_text())["decision"].get("primary") if am_files else None
        return {**got, "n_layers": n_layers(row["model"]), "main": main["layer"] if main else None,
                "amended": am["layer"] if am else None}  # fmt: skip

    def layer_gap(self) -> dict[str, Any] | None:
        from scripts import early_push_where as EPW

        p = EPW.RESULTS / LAYER_GAP_RUN / "summary.json"
        if not p.exists():
            return None
        s = json.loads(p.read_text())
        if not isinstance((s.get("layer_gap") or {}).get("w", {}).get("lens"), dict):  # rule v2's summary only
            return None
        m, cells, _, _ = EPW.load_cells(LAYER_GAP_RUN)
        layers = m["config"]["layers"]
        out: dict[str, Any] = {"n": max((len(v) for k, v in cells.items() if k[0] == "BL"), default=0), "subsets": {}}
        for sub in ("w", "s"):
            g = s["layer_gap"][sub]
            out["subsets"][sub] = {
                "layers": layers, **{arm: arm_curve(cells, sub, layers, arm) for arm in ("lens", "patch", "embed")},
                "random": [tri(EPW.cell_rate(cells.get(("BL", sub, la, 8.0, "random"), {}))) for la in layers],
                "stops": {arm: g[arm]["stop"] for arm in ("lens", "patch", "embed")}, "verdict": g["verdict"],
            }  # fmt: skip
        return out


# ---------------------------------------------------------------- collecting each figure's cells


def collect_late(grid: Grid, src: Source) -> DotData:
    data = DotData(("prose", "table", "JSON", "long context"))
    for panel in data.panels:
        for m in S.MODELS:
            row = grid.get(m.key, "f4", panel)
            mk = mark_of(m.key, row, "attn")
            if mk.status == "value" and row:
                try:
                    for k, v in src.late_arms(row).items():
                        if v is not None and finite(v):
                            mk.points[k] = v
                except Exception as e:
                    mk = broken(m.key, data.errors, panel, e)
            data.marks[(panel, m.key)] = mk
    return data


def collect_name_digit(grid: Grid, src: Source) -> DotData:
    data = DotData(("prose", "table", "JSON"))
    for panel in data.panels:
        for m in S.MODELS:
            row = grid.get(m.key, "f3", panel)
            mk = mark_of(m.key, row, "name")
            if mk.status == "value" and row:
                try:
                    mk.points["digit"] = src.name_digit(row)["digit"]
                except Exception as e:
                    mk = broken(m.key, data.errors, panel, e)
            data.marks[(panel, m.key)] = mk
    return data


def collect_counting(grid: Grid, src: Source) -> DotData:
    data = DotData(tuple(s for s, *_ in G.V4X))
    for panel in data.panels:
        for m in S.MODELS:
            row = grid.get(m.key, "f6", panel)
            mk = mark_of(m.key, row, "order")
            if mk.status == "value" and row:
                try:
                    rivals = src.counting(row)
                    mk.points.update(rivals)
                    mk.ticks["bar"] = max(r[2] for r in rivals.values())
                except Exception as e:
                    mk = broken(m.key, data.errors, panel, e)
            data.marks[(panel, m.key)] = mk
    return data


def stated_bridge_row(grid: Grid, model: str) -> tuple[dict | None, str]:
    """The prose draw of the stated-bridge test: draw 2 (the cross-model scenes) where the model has it planned, else
    draw 1; the choice depends on the plan (a spec), never on the result."""
    d2 = grid.get(model, "f2", "draw 2")
    if d2 is not None and not (word(d2["verdict"]) == "missing" and "no spec" in d2["verdict"]):
        return d2, "draw 2"
    return grid.get(model, "f2", "draw 1"), "draw 1"


def newcombe(a: Triple, na: int, b: Triple, nb: int) -> Triple:
    """a - b for two independent groups of items (lookups and recalls are different families): pointer_swap.newcombe
    (Newcombe's hybrid Wilson interval) on the counts behind the two rates. Descriptive; the rule judges each arm."""
    from scripts import pointer_swap as PS

    return tri(PS.newcombe(round(a[0] * na), na, round(b[0] * nb), nb))


def collect_lens(grid: Grid, src: Source) -> DotData:
    """The decisive comparison first (recalls minus lookups switched by the lens-readable part), then the raw rates
    behind it, then the gates. A not-interpretable test is hatched in the contrast panel; its raw rates (the failed
    control among them) stay visible beside it."""
    data = DotData(("contrast", "lens part", "rest", "gate v1", "gate v2"))
    for m in S.MODELS:
        row, draw = stated_bridge_row(grid, m.key)
        note = "draw 1" if draw == "draw 1" else ""
        main = mark_of(m.key, row, "lookup")
        main.note = note
        lens, rest = (Mark(m.key, main.status, main.reason, n=main.n) for _ in range(2))
        if row is not None and main.status in ("value", "not interpretable") and row.get("value") is not None:
            try:
                got = src.stated_bridge(row)
                n_lk, n_rc = got["lookup_n"], got["recall_n"]
                main.points = {"contrast": newcombe(got["recall_lens"], n_rc, got["lookup_lens"], n_lk)}
                main.n = f"{n_lk}/{n_rc}"
                lens = Mark(m.key, "value", n=main.n, note=note,
                            points={"lookup": got["lookup_lens"], "recall": got["recall_lens"]})  # fmt: skip
                rest = Mark(m.key, "value", n=n_lk, note=note, points={"rest": got["lookup_rest"]})
                for k, mk in (("lookup_null", lens), ("recall_null", lens)):
                    if finite(got[k]):
                        mk.ticks[k] = got[k][0]
            except Exception as e:
                main = lens = rest = broken(m.key, data.errors, "stated bridge", e)
        data.marks[("contrast", m.key)] = main
        data.marks[("lens part", m.key)] = lens
        data.marks[("rest", m.key)] = rest
        for panel, setting in (("gate v1", "v1 (at the word)"), ("gate v2", "v2 (after the word)")):
            grow = grid.get(m.key, "gate", setting)
            mk = mark_of(m.key, grow, "bridge")
            if mk.status == "value" and grow:
                try:
                    other = src.gate_other(grow)
                    if finite(other):
                        mk.points["other"] = other
                except Exception as e:
                    mk = broken(m.key, data.errors, panel, e)
            data.marks[(panel, m.key)] = mk
    return data


ORDER_SETTINGS = (("draw 1", "5"), ("8 sentences", "8"), ("12 sentences", "12"))


def collect_order(grid: Grid, src: Source) -> CurveData:
    data = CurveData()
    for m in S.MODELS:
        p = Panel(m.key)
        for setting, key in ORDER_SETTINGS:
            row = grid.get(m.key, "f5", setting)
            mk = mark_of(m.key, row, key)
            s = Series(key, status=mk.status, reason=mk.reason, verdict=mk.verdict)
            if row is not None and mk.status in ("value", "not interpretable") and row.get("value") is not None:
                try:
                    got = src.order_by_k(row)
                    s.x, s.y, s.n = list(got["k"]), list(got["diff"]), got["n"]
                except Exception as e:
                    b = broken(m.key, data.errors, setting, e)
                    s.status, s.reason, s.verdict = b.status, b.reason, ""
            if not s.y or s.status == "not interpretable":  # a list length not drawn, or drawn faded
                note = f"{key}: {s.status} ({s.reason})"
                p.notes.append(note if len(note) <= 24 else f"{key}: {s.status}\n({s.reason})")
            p.series.append(s)
        if any(s.y for s in p.series):
            p.status, p.reason = "value", ""
        else:  # nothing to draw: the 5-sentence lists' status in the middle, the others' below it
            p.status, p.reason = p.series[0].status, p.series[0].reason
            p.notes = [n for n in p.notes if not n.startswith("5:")]
        p.n_text = "n=" + " · ".join("–" if s.n is None or not s.y else f"{s.n}{S.VERDICT_SYMBOL.get(s.verdict, '')}"
                                     for s in p.series)  # fmt: skip
        data.panels[m.key] = p
    return data


def collect_depth(grid: Grid, src: Source) -> CurveData:
    data = CurveData()
    for m in S.MODELS:
        row = grid.get(m.key, "f5", "draw 1")
        p = Panel(m.key)
        if row is None:
            data.panels[m.key] = p
            continue
        w = word(row["verdict"])
        if not has_run(row):
            p.status, p.reason = w, short_reason(w, row["verdict"])
            data.panels[m.key] = p
            continue
        try:
            got = src.outcomes_by_depth(row)
        except Exception as e:
            b = broken(m.key, data.errors, "draw 1", e)
            p.status, p.reason = b.status, b.reason
            data.panels[m.key] = p
            continue
        x = [100 * la / got["n_layers"] for la in got["layers"]]
        p.series = [Series(k, x, list(got[k])) for k in ("position", "identity", "value")]
        p.status = "not interpretable" if w == "not interpretable" else "value"
        p.reason = short_reason(w, row["verdict"]) if w == "not interpretable" else ""
        if got.get("used") is not None:
            p.marks["used"] = 100 * got["used"] / got["n_layers"]
        p.n_text = f"n={got['n']} per layer"
        data.panels[m.key] = p
    return data


def collect_push(grid: Grid, src: Source) -> CurveData:
    data = CurveData()
    for m in S.MODELS:
        row, am = grid.get(m.key, "f7", "main rule"), grid.get(m.key, "f7", "amended rule")
        p = Panel(m.key)
        if row is None:
            data.panels[m.key] = p
            continue
        w = word(row["verdict"])
        if not has_run(row):
            p.status, p.reason = w, short_reason(w, row["verdict"])
            data.panels[m.key] = p
            continue
        try:
            got = src.push_by_layer(row)
        except Exception as e:
            b = broken(m.key, data.errors, "main rule", e)
            p.status, p.reason = b.status, b.reason
            data.panels[m.key] = p
            continue
        x = [100 * la / got["n_layers"] for la in got["layers"]]
        p.series = [Series(k, x, list(got[k])) for k in ("lookup", "recall", "random")]
        p.status = "not interpretable" if w == "not interpretable" else "value"
        p.reason = short_reason(w, row["verdict"]) if w == "not interpretable" else ""
        for k in ("main", "amended"):
            if got.get(k) is not None:
                p.marks[k] = 100 * got[k] / got["n_layers"]
        wa = word(am["verdict"]) if am else "missing"
        sym = " ".join(f"{t}{S.VERDICT_SYMBOL.get(v, '·')}" for t, v in (("▼", w), ("▽", wa)))
        p.n_text = f"n={row.get('n') or '–'}  {sym}"
        data.panels[m.key] = p
    return data


GAP_VERDICT = (("H-gap", "holds"), ("H-no-gap", "fails"), ("inconclusive", "inconclusive"))


def collect_layer_gap(src: Source) -> CurveData:
    data = CurveData()
    try:
        got = src.layer_gap()
    except Exception as e:
        broken("27b", data.errors, "layer gap", e)
        got = None
    for sub in ("w", "s"):
        p = Panel("27b")
        if got is None:
            p.status, p.reason = "missing", "not run or not pulled"
            data.panels[sub] = p
            continue
        g = got["subsets"][sub]
        p.status, p.reason = "value", ""
        p.series = [Series(k, list(g["layers"]), list(g[k])) for k in ("lens", "patch", "embed", "random")]
        for arm, la in g["stops"].items():
            if la is not None:
                p.marks[f"stop {arm}"] = la
        v = next((w for pre, w in GAP_VERDICT if str(g["verdict"]).startswith(pre)), "")
        p.n_text = f"n={got['n']} scenes" + (f"  {S.VERDICT_SYMBOL[v]}" if v else "")
        data.panels[sub] = p
    return data


# ---------------------------------------------------------------- drawing: shared pieces


@dataclass(frozen=True)
class SeriesSpec:
    key: str
    label: str
    shape: str  # marker; "" for a dashed control line (the random push)
    grey: str = ""  # "": the model's own color; else a grey (a comparison or a control, not the model)
    tick: bool = False  # dot figures: drawn as a short dashed tick at its value (a control level), never labelled
    below: bool = False  # dot figures: drawn small just under the row line (a second rival), never labelled


@dataclass(frozen=True)
class MarkSpec:
    key: str  # Panel.marks key
    glyph: str  # drawn at the top edge
    color: str
    filled: bool
    label: str


@dataclass(frozen=True)
class DotPanel:
    key: str
    title: str
    series: tuple[SeriesSpec, ...]
    rules: tuple[float, ...] = ()  # dotted: the rule's bars (0-1), labelled in place above the panel
    chance: tuple[float, str] | None = None  # dashed: chance or the control level (0-1) and its label above the panel
    verdict: bool = True  # the verdict symbol beside n
    pair: tuple[str, tuple[str, ...]] | None = None  # the decisive gap: the claim's arm, its comparison (first present)
    contrast: bool = False  # a difference in points around zero (the decisive comparison), else a rate
    width: float = 1.0
    n_col: bool = True  # an n column right of the panel (off where n is the panel before it's)


@dataclass(frozen=True)
class DotSpec:
    stem: str
    subtitle: str
    xlabel: str  # short: drawn left of the first panel's tick labels
    panels: tuple[DotPanel, ...]
    lines: tuple[tuple[str, str], ...]  # legend: ("chance" | "rule" | "bar" | "null" | "gap", label)
    legend_cols: int = 4


@dataclass(frozen=True)
class CurveSpec:
    stem: str
    subtitle: str
    xlabel: str
    ylabel: str
    series: tuple[SeriesSpec, ...]
    xlim: tuple[float, float]
    ylim: tuple[float, float]
    yticks: tuple[float, ...]
    xticks: tuple[float, ...] = ()
    chance: tuple[float, str] | None = None  # dashed (plotted units), in-place label ("" for none)
    rules: tuple[tuple[float, str], ...] = ()  # dotted horizontal lines (plotted units), in-place labels
    rule_segments: tuple[tuple[float, float, float], ...] = ()  # dotted (y, x0, x1)
    bands: bool = False  # 95% intervals as shaded bands (else bars)
    dodge: float = 0.0  # x offset between series (categorical x)
    lines: tuple[tuple[str, str], ...] = ()
    marks: tuple[MarkSpec, ...] = ()
    label_at: tuple[tuple[str, tuple[str, ...]], ...] = ()  # values printed at a mark's x: (mark key, series keys)
    span_marks: tuple[str, str] | None = None  # the decisive comparison between two marks: highlighted, labelled
    panel_titles: tuple[tuple[str, str], ...] = ()  # (panel key, title) where the panels are not models
    verdict_note: str = ""  # what the symbols beside n stand for (a legend entry)
    legend_cols: int = 4
    hatch_in_legend: bool = True


@dataclass(frozen=True)
class Layout:
    """The automatic fixes, tried in this order until a figure has no overlap (render)."""

    wrap_names: bool = False  # model names on two lines in the curve panels' titles (a dot figure's margin fits them)
    sparse_ticks: bool = False  # tick labels at the axis ends only (and the zero of a contrast)
    drop_labels: bool = False  # last resort: the comparison arms' value labels left out (the decisive arm's never)


LAYOUTS = (Layout(), Layout(wrap_names=True), Layout(True, True), Layout(True, True, True))
W, H = S.FIGSIZE
ROW_GAP = 0.4  # extra rows between the hybrids and the attention-only models
ROW = {m.key: i + (0 if m.hybrid else ROW_GAP) for i, m in enumerate(S.MODELS)}
ROW_MAX = max(ROW.values())
Y_TOP, Y_BOTTOM = -0.8, ROW_MAX + 0.95  # above: the first row's value lane; below: the chance label's strip
CHANCE_Y = ROW_MAX + 0.68
VERDICT_KEY = "✓ holds ✗ fails ≈ inconclusive"
RATE_STEPS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0)
LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "pad": 0.6, "alpha": 0.95}
PAD = 0.1  # inches between a panel's edge and the text beside it
STEP = 0.06  # inches between two candidate places of a label
LEADER = 0.14  # inches: a label farther than this from its point gets a leader line
LANES_IN = (0.2, 0.27)  # inches between a row's points and a value label in a lane above or below them
MARKER_R = 0.09  # inches: half a dot marker (9 pt) with its edge


def nice_rate(x: float) -> float:
    """The smallest axis end in RATE_STEPS at or above x (0-1)."""
    return next((s for s in RATE_STEPS if x <= s + 1e-9), 1.0)


def model_name(key: str, lay: Layout) -> str:
    """The model's label; with wrap_names, split at the space or hyphen nearest its middle."""
    label = S.MODEL[key].label
    if not lay.wrap_names or len(label) < 10:
        return label
    cuts = [i for i, ch in enumerate(label) if ch in " -"]
    if not cuts:
        return label
    i = min(cuts, key=lambda c: abs(c - len(label) / 2))
    return label[: i + (label[i] == "-")].rstrip() + "\n" + label[i + 1 :]


def wrap_to(fig: Figure, text: str, size: float, width_in: float, weight: str = "normal") -> str:
    """`text` wrapped so that every line fits `width_in` as drawn."""
    if not text.strip():
        return text
    width = 140
    while True:
        out = textwrap.fill(text, width)
        if max(S.text_width(fig, line, size, weight) for line in out.splitlines()) <= width_in or width < 40:
            return out
        width -= 3


def fig_header(fig: Figure, title: str, subtitle: str) -> float:
    """Title (the outcome) and subtitle (what was measured) at the top-left, each wrapped to the figure's width as
    drawn; returns the subtitle's bottom in inches from the top."""
    r = S.renderer(fig)
    t = fig.text(0.22 / W, 1 - 0.16 / H, wrap_to(fig, title, S.TITLE, W - 0.45, "bold"), fontsize=S.TITLE,
                 fontweight="bold", va="top", ha="left", linespacing=1.1)  # fmt: skip
    y = H - t.get_window_extent(r).y0 / fig.dpi + 0.1
    s = fig.text(0.22 / W, 1 - y / H, wrap_to(fig, subtitle, S.SUBTITLE, W - 0.45), fontsize=S.SUBTITLE,
                 color=S.INK2, va="top", ha="left", linespacing=1.2)  # fmt: skip
    return H - s.get_window_extent(r).y0 / fig.dpi


def footer(fig: Figure, handles: list, labels: list[str], ncol: int) -> float:
    """The legend at the bottom-left, with as many columns (up to ncol) as fit the figure's width; returns its top in
    inches."""
    r = S.renderer(fig)
    for n in range(ncol, 0, -1):
        leg = fig.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.22 / W, 0.1 / H), ncol=n, frameon=False,
                         handlelength=2.2, columnspacing=1.2, handletextpad=0.5, borderaxespad=0, fontsize=S.FONT)  # fmt: skip
        b = leg.get_window_extent(r)
        if b.x1 / fig.dpi <= W - 0.1 or n == 1:
            return b.y1 / fig.dpi
        leg.remove()
    raise AssertionError("unreachable")


def series_handle(ss: SeriesSpec, line: bool = False) -> Line2D:
    if not ss.shape or ss.tick:  # a dashed control line or tick
        return Line2D([], [], **{**S.CHANCE_LINE, "color": ss.grey or S.COMPARE2})
    col = ss.grey or S.INK
    return Line2D([], [], marker=ss.shape, markersize=11, markerfacecolor=col, markeredgecolor=col, color=col,
                  linestyle="-" if line else "none", linewidth=2.4)  # fmt: skip


def line_handle(kind: str) -> Any:
    if kind in ("chance", "null"):
        return Line2D([], [], **S.CHANCE_LINE)
    if kind in ("rule", "bar"):
        return Line2D([], [], **S.RULE_LINE)
    if kind == "gap":
        return Line2D([], [], color=S.HIGHLIGHT, linewidth=7, solid_capstyle="round")
    if kind == "hatch":
        return Rectangle((0, 0), 1, 1, **S.NOT_INTERPRETABLE)
    if kind == "text":  # a legend line that is only words
        return Line2D([], [], linestyle="none")
    raise ValueError(kind)


def group_label(fig: Figure, label: str, hybrid: bool, y: float) -> None:
    fig.text(0.16 / W, y, f"{label} {'●' if hybrid else '○'}", rotation=90, ha="left", va="center",
             fontsize=S.FONT, fontweight="bold", color=S.INK2)  # fmt: skip


def pct_label(p: float, contrast: bool) -> str:
    return f"{100 * p:+.0f}".replace("-", "−") if contrast else f"{100 * p:.0f}%"


class Placer:
    """Puts each label at the first of its candidate places where it touches no text already placed and no marker,
    interval, gap bar or tick (plot_style.graphic_boxes), all measured as drawn; the figure's texts and marks are
    registered as they are drawn."""

    def __init__(self, fig: Figure):
        self.fig, self.r = fig, S.renderer(fig)
        self.taken: list[Bbox] = []

    def take_text(self, t: Text) -> None:
        if t.get_text().strip():
            self.taken.append(t.get_window_extent(self.r).padded(2))

    def take_marks(self) -> None:
        """The marks drawn so far (call after a panel's points)."""
        self.taken = [b for b in self.taken if b is not None] + [b for _, b in S.graphic_boxes(self.fig, self.r)]

    def put(self, make: Callable[[float, float, str], Text], cands: list[tuple[float, float, str]],
            within: Bbox | None = None) -> Text | None:  # fmt: skip
        """The label at the first free candidate (x, y, ha); None, and nothing drawn, if none is free."""
        for x, y, ha in cands:
            t = make(x, y, ha)
            b = t.get_window_extent(self.r).padded(2)
            inside = within is None or (
                b.x0 >= within.x0 and b.x1 <= within.x1 and b.y0 >= within.y0 and b.y1 <= within.y1
            )
            if inside and not any(b.overlaps(o) for o in self.taken):
                self.taken.append(b)
                return t
            t.remove()
        return None


def value_text(ax, x: float, y: float, text: str, ha: str, **kw: Any) -> Text:
    return ax.text(x, y, text, ha=ha, va="center", fontsize=S.FONT, color=S.INK, zorder=8, gid="value",
                   path_effects=S.HALO, **kw)  # fmt: skip


def status_text(target, x: float, y: float, text: str, ha: str, italic: bool, va: str = "center", **kw: Any) -> Text:
    """A cell's or a panel's label; a white halo (not a box) keeps it legible on hatching and lines while it takes
    no more room than its letters."""
    return target.text(x, y, text, ha=ha, va=va, fontsize=S.FONT, color=S.INK2 if italic else S.INK,
                       style="italic" if italic else "normal", linespacing=0.95, zorder=8, gid="status",
                       path_effects=[pe.withStroke(linewidth=5, foreground="white")], **kw)  # fmt: skip


def join_and(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


# ---------------------------------------------------------------- drawing: dot figures (models as rows)


def axis_ranges(spec: DotSpec, data: DotData) -> dict[str, tuple[float, float]]:
    """x ranges in percent: the rate panels share one, from 0 to the data's span (with the rule and chance lines in
    it); each contrast panel spans its own data around zero."""
    rate_hi, out = 0.0, {}
    for ps in spec.panels:
        vals = [v for (p, _), mk in data.marks.items() if p == ps.key and mk.status == "value"
                for t in mk.points.values() if finite(t) for v in t]  # fmt: skip
        if ps.contrast:
            lo, hi = min([0.0, *vals]), max([0.0, *vals])
            out[ps.key] = (-100 * nice_rate(max(-lo, 0.05)), 100 * nice_rate(max(hi, 0.05)))
        else:
            rate_hi = max([rate_hi, *vals, *ps.rules, ps.chance[0] if ps.chance else 0.0])
    top = 100 * nice_rate(rate_hi)
    for ps in spec.panels:
        if not ps.contrast:
            out[ps.key] = (0.0, top)
    return out


def n_text(ps: DotPanel, mk: Mark) -> str:
    if mk.status not in ("value", "not interpretable") or mk.n is None:
        return "–"
    sym = f" {S.VERDICT_SYMBOL[mk.verdict]}" if ps.verdict and mk.verdict and mk.status == "value" else ""
    return f"{mk.n}{sym}" + (f"\n{mk.note}" if mk.note and mk.status == "value" else "")


def legend_entries(spec: DotSpec) -> tuple[list, list[str]]:
    handles, labels = [], []
    for ss in {s.label: s for p in spec.panels for s in p.series if s.label}.values():  # "": named by its panel
        handles.append(series_handle(ss))
        labels.append(ss.label)
    for kind, label in spec.lines:
        handles.append(line_handle(kind))
        labels.append(label)
    handles.append(line_handle("hatch"))
    labels.append("not interpretable")
    handles.append(line_handle("text"))
    labels.append(f"by n: {VERDICT_KEY}")
    return handles, labels


def spanned_rows(spec: DotSpec, data: DotData) -> dict[str, str]:
    """Models whose every panel would show the same label (not testable, missing): model -> the one label."""
    out = {}
    for m in S.MODELS:
        marks = [data.marks.get((ps.key, m.key)) or Mark(m.key) for ps in spec.panels]
        same = len({(mk.status, mk.reason) for mk in marks}) == 1
        if len(spec.panels) > 1 and marks[0].status in ("not testable", "missing") and same:
            out[m.key] = f"{marks[0].status}: {marks[0].reason}"
    return out


def rule_marks(ps: DotPanel) -> list[tuple[float, str]]:
    """The labels above a panel: each rule bar's value, left to right (the chance line's word sits in the strip under
    the last row)."""
    return sorted((100 * r, f"{100 * r:.0f}%") for r in ps.rules)


def rule_levels(fig: Figure, ps: DotPanel, xlim: tuple[float, float], pw: float) -> list[int]:
    """Per label above the panel (rule_marks order), its line: one higher than the one before where they'd touch."""
    per_unit = 1.04 * (xlim[1] - xlim[0]) / pw
    last_end, level, out = -1e9, 0, []
    for x, text in rule_marks(ps):
        w = (S.text_width(fig, text) + 0.1) * per_unit
        level = level + 1 if x - w / 2 < last_end else 0
        last_end = x + w / 2
        out.append(level)
    return out


def draw_dots(spec: DotSpec, data: DotData, title: str, lay: Layout = LAYOUTS[0]) -> Figure:
    S.apply()
    fig = plt.figure(figsize=S.FIGSIZE)
    placer = Placer(fig)
    head = fig_header(fig, title, spec.subtitle)
    leg_top = footer(fig, *legend_entries(spec), spec.legend_cols)
    names = [model_name(m.key, lay) for m in S.MODELS]  # the margin is made to fit them (two lines: narrower)
    left = 0.62 + max(S.text_width(fig, line) for nm in names for line in nm.split("\n")) + 0.25
    n_cols = [PAD + 0.12 + max([S.text_width(fig, line) for m in S.MODELS
                                for line in n_text(ps, data.marks.get((ps.key, m.key)) or Mark(m.key)).split("\n")]
                               + [S.text_width(fig, "n")]) if ps.n_col else 0.0 for ps in spec.panels]  # fmt: skip
    gaps = [0.18 if nc else 0.18 + S.text_width(fig, "100%") for nc in n_cols[:-1]]
    unit = (W - left - 0.06 - sum(n_cols) - sum(gaps)) / sum(ps.width for ps in spec.panels)
    ranges = axis_ranges(spec, data)
    rule_rows = 1 + max(max(rule_levels(fig, ps, ranges[ps.key], unit * ps.width), default=0) for ps in spec.panels)
    top = head + 0.4 + 0.27 * rule_rows  # the panel titles, and the rule labels above the panels
    bottom = leg_top + 0.5  # the tick labels
    ph = H - top - bottom
    spans = spanned_rows(spec, data)
    x, axes = left, []
    for i, (ps, nc) in enumerate(zip(spec.panels, n_cols, strict=True)):
        pw = unit * ps.width
        ax = fig.add_axes((x / W, bottom / H, pw / W, ph / H))
        axes.append((ax, ps, pw, nc))
        dot_frame(ax, ps, names if i == 0 else None, ranges[ps.key], pw, lay, rule_rows)
        x += pw + nc + (gaps[i] if i < len(gaps) else 0.0)
    y0, y1 = bottom / H, (bottom + ph) / H

    def fy(row: float) -> float:
        return y1 - (row - Y_TOP) / (Y_BOTTOM - Y_TOP) * (y1 - y0)

    for label, hybrid in S.GROUPS:
        rows = [ROW[m.key] for m in S.MODELS if m.hybrid == hybrid]
        group_label(fig, label, hybrid, fy((min(rows) + max(rows)) / 2))
        fig.add_artist(Line2D([0.5 / W] * 2, [fy(min(rows) - 0.35), fy(max(rows) + 0.35)], color=S.COMPARE2, lw=1.5))
    if spec.xlabel:
        fig.text((left - 0.3) / W, (bottom - 0.2) / H, spec.xlabel, ha="right", va="center", fontsize=S.LABEL)
    for key, text in spans.items():  # one label across the row where every panel would say the same
        status_text(fig, (left + 0.05) / W, fy(ROW[key]), text, "left", italic=True)
    for ax, ps, pw, nc in axes:  # the marks of every panel, then the labels: a label can see every mark
        dot_marks(ax, ps, data, ranges[ps.key], set(spans), pw, nc)
    placer.take_marks()
    for t in [*fig.texts, *(t for ax, *_ in axes for t in ax.texts)]:
        placer.take_text(t)
    for ax, ps, pw, _ in axes:
        dot_labels(ax, ps, data, ranges[ps.key], set(spans), pw, lay, placer)
    return fig


def dot_frame(ax, ps: DotPanel, names: list[str] | None, xlim: tuple[float, float], pw: float, lay: Layout,
              rule_rows: int) -> None:  # fmt: skip
    """Axes, ticks, the rule and chance lines and their labels, the panel title."""
    x0, x1 = xlim
    span = x1 - x0
    ax.set_xlim(x0 - 0.02 * span, x1 + 0.02 * span)
    ax.set_ylim(Y_BOTTOM, Y_TOP)
    sparse = lay.sparse_ticks or pw < 3 * S.text_width(ax.figure, "100%") + 0.3  # a narrow panel: the ends only
    if ps.contrast:
        ax.set_facecolor(S.HIGHLIGHT_BG)
        ticks = [t for t in (x0, 0.0, x1) if t == 0 or (not sparse and abs(t) >= 0.3 * span)
                 or (sparse and t == x1)]  # fmt: skip
        ax.set_xticks(ticks, [f"{t:+.0f}".replace("-", "−") if t else "0" for t in ticks])
    else:
        ticks = [0, x1] if sparse else [0, x1 / 2, x1]
        ax.set_xticks(ticks, [f"{t:.0f}%" for t in ticks])
        ax.set_xticks([x1 / 4, x1 / 2, 3 * x1 / 4] if sparse else [x1 / 4, 3 * x1 / 4], minor=True)
    ax.grid(axis="x", which="both", color=S.GRID, lw=1)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", pad=6)
    ax.set_yticks([ROW[m.key] for m in S.MODELS], names or [""] * len(S.MODELS))
    for t in ax.get_yticklabels():
        t.set_linespacing(0.9)
    ax.axhline((ROW[S.MODELS[3].key] + ROW[S.MODELS[4].key]) / 2, color=S.COMPARE2, lw=1.2)
    for r in ps.rules:
        ax.axvline(100 * r, zorder=1.5, **S.RULE_LINE)
    for x, text in ([(100 * ps.chance[0], ps.chance[1])] if ps.chance else []) + ([(0.0, "no gap")] if ps.contrast
                                                                                 else []):  # fmt: skip
        ax.axvline(x, zorder=1.4, **S.CHANCE_LINE)
        half = (S.text_width(ax.figure, text) / 2 + 0.05) * 1.04 * span / pw  # kept inside the panel
        xt = min(max(x, x0 + half), x1 - half)
        ax.text(xt, CHANCE_Y, text, ha="center", va="center", fontsize=S.FONT, color=S.INK2, zorder=6, bbox=LABEL_BOX)
    for (x, text), level in zip(rule_marks(ps), rule_levels(ax.figure, ps, xlim, pw), strict=True):
        ax.annotate(text, (x, Y_TOP), xycoords="data", xytext=(0, 3 + 19 * level), textcoords="offset points",
                    ha="center", va="bottom", fontsize=S.FONT, color=S.INK if "%" in text else S.INK2,
                    annotation_clip=False)  # fmt: skip
    ax.set_title(ps.title, loc="left", fontsize=S.PANEL_TITLE, fontweight="bold", pad=6 + 19 * rule_rows)
    if ps.n_col:
        ax.annotate("n", (1, Y_TOP), xycoords=("axes fraction", "data"), xytext=(72 * PAD, 3),
                    textcoords="offset points", ha="left", va="bottom", fontsize=S.FONT, color=S.INK2,
                    annotation_clip=False)  # fmt: skip


def fit_status(fig: Figure, mk: Mark, width_in: float) -> str:
    """A cell's one-line label within width_in: "status: reason"; else, in a hatched cell, the reason (the hatch says
    "not interpretable", the legend); else the status word."""
    for text in (f"{mk.status}: {mk.reason}", mk.reason if mk.status == "not interpretable" else mk.status):
        if S.text_width(fig, text) + 0.12 <= width_in:
            return text
    return ""


def dot_marks(ax, ps: DotPanel, data: DotData, xlim: tuple[float, float], spanned: set[str], pw: float,
              n_col: float) -> None:  # fmt: skip
    """Every row's marks: the points on the row line with their 95% intervals, the decisive pair joined by the
    highlight, the control ticks; a label for a cell without a value (one line, so no two rows' labels can touch);
    the n column."""
    x0, x1 = xlim
    span = x1 - x0
    for m in S.MODELS:
        mk = data.marks.get((ps.key, m.key)) or Mark(m.key)
        y = ROW[m.key]
        if m.key in spanned:
            continue
        if mk.status == "value":
            dot_points(ax, ps, mk, m.key, y)
        elif mk.status == "not interpretable":
            ax.add_patch(Rectangle((x0, y - 0.3), span, 0.6, zorder=1, **S.NOT_INTERPRETABLE))
            text = fit_status(ax.figure, mk, pw)
            if text:
                status_text(ax, (x0 + x1) / 2, y, text, "center", italic=False)
        else:
            # one line, allowed over the n column (which stays empty for such a row)
            text = fit_status(ax.figure, mk, pw + n_col)
            bx = ax.transData.transform((x0 + 0.02 * span, y))
            fx, fy_ = ax.figure.transFigure.inverted().transform(bx)
            status_text(ax.figure, fx, fy_, text, "left", italic=True)
            continue
        if ps.n_col:
            ax.annotate(n_text(ps, mk), (1, y), xycoords=("axes fraction", "data"), xytext=(72 * PAD, 0),
                        textcoords="offset points", ha="left", va="center", fontsize=S.FONT, color=S.INK,
                        linespacing=0.95, annotation_clip=False, gid="n")  # fmt: skip


def pair_of(ps: DotPanel, mk: Mark) -> tuple[str, str] | None:
    if not ps.pair or not finite(mk.points.get(ps.pair[0])):
        return None
    other = next((k for k in ps.pair[1] if finite(mk.points.get(k))), None)
    return (ps.pair[0], other) if other else None


def dot_points(ax, ps: DotPanel, mk: Mark, key: str, y: float) -> None:
    pair = pair_of(ps, mk)
    if pair:
        a, b = mk.points[pair[0]][0], mk.points[pair[1]][0]
        ax.plot([100 * a, 100 * b], [y, y], color=S.HIGHLIGHT, lw=6, alpha=0.9, solid_capstyle="round", zorder=2.4,
                gid="gap")  # fmt: skip
    for ss in ps.series:
        t = mk.points.get(ss.key)
        if not finite(t):
            continue
        p, lo, hi = t  # type: ignore[misc]
        lo, hi = min(lo, p), max(hi, p)  # rounding at 0% / 100% can put a bound a hair inside the point
        if ss.tick:
            ax.plot([100 * p] * 2, [y - 0.24, y + 0.24], zorder=2.6, gid="tick", **{**S.CHANCE_LINE, "linewidth": 2.2})
            continue
        yy = y + (0.24 if ss.below else 0.0)
        col = ss.grey or S.MODEL[key].edge
        size = 9
        kw = (dict(marker=ss.shape, markersize=size, markerfacecolor=col, markeredgecolor=col, linestyle="none")
              if ss.grey else S.marker(key, ss.shape, size=size))  # fmt: skip
        ax.plot([100 * lo, 100 * hi], [yy, yy], color=col, lw=2.6, solid_capstyle="butt", zorder=3, gid="ci")
        ax.plot([100 * p], [yy], zorder=4 if not ss.grey else 3.5, clip_on=False, gid="mark", **kw)
    for k, x in mk.ticks.items():
        style = S.RULE_LINE if k == "bar" else S.CHANCE_LINE
        ax.plot([100 * x] * 2, [y - 0.3, y + 0.3], zorder=2, gid="tick", **style)


def dot_labels(ax, ps: DotPanel, data: DotData, xlim: tuple[float, float], spanned: set[str], pw: float,
               lay: Layout, placer: Placer) -> None:  # fmt: skip
    """Every row's values in the lane above its points: the decisive arm's first, never left out (it moves along the
    lane, then below the row, with a leader line), the comparison's next and only where it fits; two values too close
    for two labels as one ("6 vs 10%")."""
    per_unit = (ax.get_xlim()[1] - ax.get_xlim()[0]) / pw  # data units per inch
    within = ax.get_window_extent(placer.r)
    xs_all = [xlim[0] + i * STEP * per_unit for i in range(int((xlim[1] - xlim[0]) / (STEP * per_unit)) + 1)]
    for m in S.MODELS:
        mk = data.marks.get((ps.key, m.key)) or Mark(m.key)
        if m.key in spanned or mk.status != "value":
            continue
        y = ROW[m.key]
        pair = pair_of(ps, mk)
        keys = [ss.key for ss in ps.series if not ss.tick and not ss.below and finite(mk.points.get(ss.key))]
        if pair and pair[1] in keys:
            keys = [pair[0], pair[1]] + [k for k in keys if k not in pair]
        elif pair:
            keys = [pair[0]] + [k for k in keys if k != pair[0]]
            pair = None  # its comparison is a control tick: read off the axis, not labelled
        r = MARKER_R * per_unit

        def extent(ks: list[str], pts: dict[str, Triple] = mk.points, r: float = r) -> tuple[float, float]:
            """The points' intervals and markers, percent."""
            return (min(min(100 * pts[k][1], 100 * pts[k][0] - r) for k in ks),
                    max(max(100 * pts[k][2], 100 * pts[k][0] + r) for k in ks))  # fmt: skip

        labels = [(pct_label(mk.points[k][0], ps.contrast), 100 * mk.points[k][0], extent([k])) for k in keys]
        if pair and abs(labels[0][1] - labels[1][1]) / per_unit < S.text_width(ax.figure, labels[0][0]) + 0.1:
            first = labels[0][0][:-1] if labels[0][0].endswith("%") and labels[1][0].endswith("%") else labels[0][0]
            mid = (labels[0][1] + labels[1][1]) / 2
            labels = [(f"{first} vs {labels[1][0]}", mid, extent(list(pair))), *labels[2:]]
        row_in = ax.get_position().height * H / (Y_BOTTOM - Y_TOP)
        lanes = [d / row_in for d in LANES_IN]  # rows above (and below) the points, nearest first
        pad = 0.05 * per_unit
        for i, (text, xp, (lo, hi)) in enumerate(labels):
            if i > 0 and lay.drop_labels:
                break
            # on the row line beside the points first, then a lane above, then (the decisive value) below
            beside = [(hi + pad, y, "left"), (lo - pad, y, "right")]
            order = sorted(xs_all, key=lambda x, xp=xp: abs(x - xp))
            close = [x for x in order if abs(x - xp) / per_unit <= 0.5]
            far = [x for x in order if abs(x - xp) / per_unit > 0.5]
            signs = (-1, 1) if i == 0 else (-1,)
            cands = beside + [(x, y + s * ln, "center") for ln in lanes for s in signs for x in close]
            if i == 0:  # the decisive value: anywhere along the lanes before it is drawn where it touches
                cands += [(x, y + s * ln, "center") for ln in lanes for s in signs for x in far]
            t = placer.put(lambda x, yy, ha, text=text: value_text(ax, x, yy, text, ha), cands, within)
            if t is None and i == 0 and " vs " in text:  # a joint label with no room: the decisive value alone
                first = text.split(" vs ")[0]
                text = first if first.endswith("%") or ps.contrast else first + "%"
                t = placer.put(lambda x, yy, ha, text=text: value_text(ax, x, yy, text, ha), cands, within)
            if t is None and i == 0:  # the decisive value is never left out: drawn above its point even where it
                # touches something (plot_style.overlaps then reports it and the render ladder goes on)
                t = value_text(ax, min(max(xp, xlim[0] + 3 * pad), xlim[1] - 3 * pad), y - lanes[0], text, "center")
                placer.take_text(t)
            if t is None:
                continue
            tx, ty = t.get_position()
            if abs(ty - y) > 1e-9 and (abs(tx - xp) / per_unit > LEADER or ty > y):  # a short leader to the label
                y0, y1 = (y + 0.1, ty - 0.18) if ty > y else (y - 0.1, ty + 0.18)
                ax.plot([xp, tx], [y0, y1], color=S.INK2, lw=1, zorder=2.2, gid="leader")


# ---------------------------------------------------------------- drawing: curve figures (one panel per model)


def curve_legend(spec: CurveSpec) -> tuple[list, list[str]]:
    handles: list = [series_handle(ss, line=True) for ss in spec.series]
    labels = [ss.label for ss in spec.series]
    for mk in spec.marks:
        handles.append(Line2D([], [], marker=mk.glyph, markersize=12, markeredgecolor=mk.color, markeredgewidth=1.8,
                              markerfacecolor=mk.color if mk.filled else "white", linestyle="none"))  # fmt: skip
        labels.append(mk.label)
    for kind, label in spec.lines:
        handles.append(line_handle(kind))
        labels.append(label)
    if spec.hatch_in_legend:
        handles.append(line_handle("hatch"))
        labels.append("not interpretable")
    if spec.verdict_note:
        handles.append(line_handle("text"))
        labels.append(spec.verdict_note)
    return handles, labels


def draw_curves(spec: CurveSpec, data: CurveData, title: str, keys: list[str] | None = None,
                lay: Layout = LAYOUTS[0]) -> Figure:  # fmt: skip
    """Panels: the eight models in two rows (hybrids, attention only), or `keys` in one row (a one-model figure)."""
    S.apply()
    fig = plt.figure(figsize=S.FIGSIZE)
    placer = Placer(fig)
    head = fig_header(fig, title, spec.subtitle)
    leg_top = footer(fig, *curve_legend(spec), spec.legend_cols)
    rows = (
        [[m.key for m in S.MODELS if m.hybrid], [m.key for m in S.MODELS if not m.hybrid]] if keys is None else [keys]
    )
    in_place = [t for _, t in [*([spec.chance] if spec.chance else []), *spec.rules] if t]
    right = 0.12 + max([S.text_width(fig, t) + 0.12 for t in in_place], default=0.0)
    left, gap, between = 1.62, 0.34, 0.3
    title_lines = 2 if lay.wrap_names and keys is None else 1
    head_h = 0.36 + 0.28 * title_lines  # the panel's title and its n line
    top, bottom = head + 0.12, leg_top + 0.42 + 0.36  # tick labels, the x label
    n_c = max(len(r) for r in rows)
    pw = (W - left - right - (n_c - 1) * gap) / n_c
    ph = (H - top - bottom - len(rows) * head_h - (len(rows) - 1) * between) / len(rows)
    panels = []
    for r, row in enumerate(rows):
        y0 = H - top - head_h - r * (ph + head_h + between) - ph
        for c, key in enumerate(row):
            ax = fig.add_axes(((left + c * (pw + gap)) / W, y0 / H, pw / W, ph / H))
            p = data.panels.get(key) or Panel(key if key in S.MODEL else S.MODELS[0].key)
            curve_frame(ax, spec, p, key, (c == 0, r == len(rows) - 1, c == len(row) - 1), lay)
            panels.append((ax, p))
        if keys is None:
            label, hybrid = S.GROUPS[r]
            group_label(fig, label, hybrid, (y0 + ph / 2) / H)
    fig.text(0.66 / W, (bottom + (H - top - bottom) / 2) / H, spec.ylabel, rotation=90, ha="center", va="center",
             fontsize=S.LABEL)  # fmt: skip
    fig.text((left + (W - left - right) / 2) / W, (bottom - 0.4) / H, spec.xlabel, ha="center", va="top",
             fontsize=S.LABEL)  # fmt: skip
    placer.take_marks()
    for t in fig.texts:
        placer.take_text(t)
    for ax, _ in panels:
        for t in ax.texts:
            placer.take_text(t)
    for ax, p in panels:  # the labels inside the panels, each where it covers no mark and no other label
        curve_labels(ax, spec, p, lay, placer)
    return fig


def spread(ys: list[float], min_gap: float) -> list[float]:
    """Positions at least min_gap apart, each moved as little as needed (sorted input)."""
    out = list(ys)
    for i in range(1, len(out)):
        out[i] = max(out[i], out[i - 1] + min_gap)
    return out


def curve_frame(ax, spec: CurveSpec, p: Panel, key: str, where: tuple[bool, bool, bool], lay: Layout) -> None:
    """Axes, lines, the series and the marks of one panel (labels come later: curve_labels)."""
    first_col, last_row, last_col = where
    model = S.MODEL[p.model]
    ax.set_xlim(*spec.xlim)
    ax.set_ylim(*spec.ylim)
    ax.set_yticks(spec.yticks)
    if spec.xticks:
        xt = (spec.xticks[0], spec.xticks[-1]) if lay.sparse_ticks else spec.xticks
        ax.set_xticks(xt, [f"{x:g}" for x in xt])
    if not first_col:
        ax.set_yticklabels([])
    if not last_row:
        ax.set_xticklabels([])
    ax.grid(axis="y", color=S.GRID, lw=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", pad=7)
    ax.tick_params(axis="y", pad=5)
    ax.spines["top"].set_visible(True)
    ax.spines["top"].set_color(model.edge)
    ax.spines["top"].set_linewidth(5)
    title = dict(spec.panel_titles).get(key) or model_name(p.model, lay)
    ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(0, 26), textcoords="offset points",
                fontsize=S.PANEL_TITLE, fontweight="bold", va="bottom", ha="left", linespacing=0.95)  # fmt: skip
    ax.annotate(p.n_text or " ", (0, 1), xycoords="axes fraction", xytext=(0, 6), textcoords="offset points",
                fontsize=S.FONT, color=S.INK2, va="bottom", ha="left", gid="n")  # fmt: skip
    if spec.chance is not None:
        ax.axhline(spec.chance[0], zorder=1.4, **S.CHANCE_LINE)
    for y, _ in spec.rules:
        ax.axhline(y, zorder=1.5, **S.RULE_LINE)
    for y, x0, x1 in spec.rule_segments:
        ax.plot([x0, x1], [y, y], zorder=1.5, **S.RULE_LINE)
    line_gap = 0.3 / (ax.get_position().height * H) * (spec.ylim[1] - spec.ylim[0])  # 0.3 in, in data units
    if last_col:  # the lines' meaning in place, right of the last panel of each row, spread where close
        lines = sorted((y, t) for y, t in [*([spec.chance] if spec.chance else []), *spec.rules] if t)
        for (y, t), yl in zip(lines, spread([y for y, _ in lines], line_gap), strict=True):
            ax.annotate(t, (1, y), xycoords=("axes fraction", "data"), xytext=(1.03, yl),
                        textcoords=("axes fraction", "data"), fontsize=S.FONT, color=S.INK2, va="center", ha="left",
                        annotation_clip=False)  # fmt: skip
    if p.status not in ("value", "not interpretable"):
        status_text(ax, 0.5, 0.62, f"{p.status}\n{p.reason}", "center", italic=True, transform=ax.transAxes)
        return
    if p.status == "not interpretable":
        ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, zorder=0, **S.NOT_INTERPRETABLE))
    styles = {ss.key: ss for ss in spec.series}
    present = [s for s in p.series if s.key in styles and any(finite(t) for t in s.y)]
    for i, s in enumerate(present):
        draw_series(ax, spec, styles[s.key], s, p.model, (i - (len(present) - 1) / 2) * spec.dodge)
    for j, mk in enumerate(spec.marks):
        if mk.key not in p.marks:
            continue
        same = [k for k in spec.marks[:j] if k.key in p.marks and abs(p.marks[k.key] - p.marks[mk.key]) < 1e-9]
        x = p.marks[mk.key] + len(same) * 0.03 * (spec.xlim[1] - spec.xlim[0])  # side by side where they coincide
        inside = (13 / 2 + 1.8) / 72 / (ax.get_position().height * H) * (spec.ylim[1] - spec.ylim[0])
        ax.plot([x], [spec.ylim[1] - inside], marker=mk.glyph, markersize=13, markeredgecolor=mk.color,
                markerfacecolor=mk.color if mk.filled else "white", markeredgewidth=1.8, linestyle="none",
                clip_on=False, zorder=7, gid="mark")  # fmt: skip
    if spec.span_marks and all(k in p.marks for k in spec.span_marks):
        a, b = (p.marks[k] for k in spec.span_marks)
        y = spec.ylim[1] - 0.12 * (spec.ylim[1] - spec.ylim[0])
        ax.annotate("", xy=(b, y), xytext=(a, y), arrowprops={"arrowstyle": "<|-|>", "color": S.HIGHLIGHT, "lw": 4,
                                                              "shrinkA": 0, "shrinkB": 0}, zorder=6)  # fmt: skip
        ax.plot([a, b], [y, y], alpha=0, gid="gap")  # the arrow's place, for the labels to keep off


CORNERS = ((0.03, 0.05, "left", "bottom"), (0.97, 0.05, "right", "bottom"), (0.03, 0.95, "left", "top"),
           (0.97, 0.95, "right", "top"), (0.5, 0.5, "center", "center"), (0.03, 0.5, "left", "center"),
           (0.97, 0.5, "right", "center"))  # fmt: skip


def curve_labels(ax, spec: CurveSpec, p: Panel, lay: Layout, placer: Placer) -> None:
    """A curve panel's labels, each where it covers no marker and no label: the hatch's reason, the notes on list
    lengths not drawn, the values at the rule's cell (the decisive arm's first), the gap between two marks."""
    if p.status not in ("value", "not interpretable"):
        return
    within = ax.get_window_extent(placer.r)
    xspan, yspan = spec.xlim[1] - spec.xlim[0], spec.ylim[1] - spec.ylim[0]
    w_in, h_in = ax.get_position().width * W, ax.get_position().height * H

    def at_corner(text: str, italic: bool) -> None:
        def make(i: float, _: float, __: str) -> Text:
            x, y, ha, va = CORNERS[int(i)]
            return status_text(ax, x, y, text, ha, italic=italic, va=va, transform=ax.transAxes)

        placer.put(make, [(i, 0.0, "") for i in range(len(CORNERS))], within)

    if p.status == "not interpretable":
        at_corner(f"not interpretable\n{p.reason}", italic=False)
    for note in p.notes:
        at_corner(note, italic=True)
    for mkey, keys in spec.label_at:
        if mkey not in p.marks:
            continue
        found = []
        for s in p.series:
            if s.key in keys and s.x:
                i = min(range(len(s.x)), key=lambda j: abs(s.x[j] - p.marks[mkey]))
                t = s.y[i]
                if abs(s.x[i] - p.marks[mkey]) < 1e-6 and finite(t):
                    found.append((s.key, 100 * t[0], s.x[i]))  # type: ignore[index]
        found.sort(key=lambda f: keys.index(f[0]))  # the decisive arm first
        if lay.drop_labels:
            found = found[:1]
        dx, dy = 0.1 / w_in * xspan, 0.26 / h_in * yspan
        glyph = {"o": "●", "s": "■", "^": "▲", "D": "◆", "v": "▼"}
        shape = {ss.key: ss.shape for ss in spec.series}
        for key, y, x in found:  # near the point first; farther (with a leader line) before leaving a value out
            # offsets in 0.1 in steps, starting past the point's own marker; nearest first
            offsets = sorted(((s * k, v) for k in (1.4, 2, 3, 4, 6, 9) for v in (0, 1, -1, 2, -2, 3, -3, 4, -4)
                              for s in (1, -1)), key=lambda o: (o[0] * 0.1) ** 2 + (o[1] * 0.26) ** 2)  # fmt: skip
            cands = [(x + k * dx, y + v * dy, "left" if k > 0 else "right") for k, v in offsets]
            text = f"{glyph.get(shape.get(key, ''), '')}{y:.0f}%"  # the series' marker names it
            t = placer.put(lambda xx, yy, ha, text=text: value_text(ax, xx, yy, text, ha), cands, within)
            if t is not None:
                tx, ty = t.get_position()
                if ((tx - x) / dx * 0.1) ** 2 + ((ty - y) / dy * 0.26) ** 2 > 0.12**2:  # moved: a leader to it
                    ax.plot([x, tx], [y, ty], color=S.INK2, lw=1, zorder=2.2, gid="leader")
    if spec.span_marks and all(k in p.marks for k in spec.span_marks):
        a, b = (p.marks[k] for k in spec.span_marks)
        y = spec.ylim[1] - 0.12 * yspan
        cands = [((a + b) / 2, y - v * 0.09 * yspan, "center") for v in (1, 2, 3, -1)]
        placer.put(lambda xx, yy, ha: value_text(ax, xx, yy, f"{b - a:+.0f} layers", ha), cands, within)


def draw_series(ax, spec: CurveSpec, ss: SeriesSpec, s: Series, model_key: str, dx: float) -> None:
    model = S.MODEL[model_key]
    pts = [(x + dx, t) for x, t in zip(s.x, s.y, strict=True) if finite(t)]
    xs = [x for x, _ in pts]
    ys = [100 * t[0] for _, t in pts]  # type: ignore[index]
    los = [100 * min(t[1], t[0]) for _, t in pts]  # type: ignore[index]
    his = [100 * max(t[2], t[0]) for _, t in pts]  # type: ignore[index]
    alpha = 0.35 if s.status == "not interpretable" else 1.0
    if not ss.shape:  # the random push: a dashed control line, no markers or interval
        ax.plot(xs, ys, zorder=2.8, alpha=alpha, **{**S.CHANCE_LINE, "color": ss.grey or S.COMPARE2})
        return
    if ss.grey:
        kw_line: dict[str, Any] = {"color": ss.grey, "linewidth": 2.4}
        kw_mark: dict[str, Any] = {"marker": ss.shape, "markersize": 0 if spec.bands else 9,
                                   "markerfacecolor": ss.grey, "markeredgecolor": ss.grey, "linestyle": "none"}  # fmt: skip
    else:
        kw_line, kw_mark = S.line(model_key), S.marker(model_key, ss.shape, size=9)
    if spec.bands:
        ax.fill_between(xs, los, his, color=ss.grey or model.color, alpha=0.22 * alpha, lw=0, zorder=2)
    else:
        ax.vlines(xs, los, his, color=ss.grey or model.edge, lw=2.2, alpha=alpha, zorder=2.5)
    ax.plot(xs, ys, zorder=3, alpha=alpha, **kw_line)
    if kw_mark.get("markersize"):
        ax.plot(xs, ys, zorder=4, alpha=alpha, gid="mark", **kw_mark)


# ---------------------------------------------------------------- the figures


LATE = DotSpec(
    "f_late_read_all_models",
    "% of lookups still right with the answer's sentence hidden from the last tokens in every attention layer, against "
    "hiding it in every DeltaNet layer instead (hybrids) and hiding another sentence (dashed tick). Memory → prompt.",
    "% right",
    tuple(DotPanel(k, t, (SeriesSpec("attn", "its sentence hidden", "o"),
                          SeriesSpec("deltanet", "DeltaNet layers instead", "D", S.COMPARE),
                          SeriesSpec("off", "another sentence (tick)", "", S.COMPARE2, tick=True)),
                   rules=(DF.LATE_HI, DF.GDN_MIN), chance=(G.CHANCE, "chance"), pair=("attn", ("deltanet", "off")))
          for k, t in (("prose", "Prose"), ("table", "Table"), ("JSON", "JSON"), ("long context", "Long context"))),
    (("gap", "the decisive gap"), ("chance", "chance (20%)"), ("rule", "the rule's bars")),
)  # fmt: skip
NAME_DIGIT = DotSpec(
    "f_digit_not_name_all_models",
    "% of lookups still right when the answer's sentence is hidden from the last tokens in every layer except its "
    "digit, or except its name. Memory → prompt, items right unedited.",
    "% right",
    tuple(DotPanel(k, t, (SeriesSpec("digit", "only the digit left visible", "o"),
                          SeriesSpec("name", "only the name left visible", "^", S.COMPARE)),
                   rules=(DP.BROKEN, DP.KEPT), chance=(G.CHANCE, "chance"), pair=("digit", ("name",)))
          for k, t in (("prose", "Prose"), ("table", "Table"), ("JSON", "JSON"))),
    (("gap", "the decisive gap"), ("chance", "chance (20%)"), ("rule", "the rule's bars")),
)  # fmt: skip
COUNTING = DotSpec(
    "f_counts_list_order_not_text_all_models",
    "The donor's last two tokens copied in at the decisive layer (memory → prompt): % of patched answers at the "
    "sentence with the same order in the list, at the same place in the text, or counted from the end.",
    "% of answers",
    tuple(DotPanel(k, k[0].upper() + k[1:], (SeriesSpec("order", "same order in the list", "o"),
                                             SeriesSpec(G.RIVAL["token"], "same place in the text", "s", S.COMPARE),
                                             SeriesSpec(G.RIVAL["end"], "counted from the end", "v", S.COMPARE2,
                                                        below=True)),
                   chance=(G.CHANCE, "chance"), pair=("order", (G.RIVAL["token"], G.RIVAL["end"])))
          for k, *_ in G.V4X),
    (("gap", "the decisive gap"), ("chance", "chance (20%)"), ("bar", "the rivals' upper end")),
)  # fmt: skip
LENS = DotSpec(
    "f_lookup_ignores_lens_part_all_models",
    "A stated bridge switched by patching only the part of its change the lens can read, or the rest. Shaded: recalls "
    "minus lookups switched by the lens part (points, Newcombe 95%); beside it the rates and the lens gates.",
    "",
    (DotPanel("contrast", "Recall − lookup", (SeriesSpec("contrast", "", "o"),), contrast=True, width=1.45),
     DotPanel("lens part", "Lens part", (SeriesSpec("lookup", "lookups; gates: the bridge", "o"),
                                         SeriesSpec("recall", "recalls (the control)", "s", S.COMPARE)),
              rules=(0.10, 0.30), verdict=False, pair=("lookup", ("recall",)), n_col=False, width=1.45),
     DotPanel("rest", "The rest", (SeriesSpec("rest", "lookups, the rest", "^"),), rules=(0.50,),
              verdict=False, n_col=False, width=0.75),
     DotPanel("gate v1", "Gate: word", (SeriesSpec("bridge", "lookups; gates: the bridge", "o"),
                                        SeriesSpec("other", "gates: the other bridge", "^", S.COMPARE)),
              rules=(0.20, 0.50), pair=("bridge", ("other",))),
     DotPanel("gate v2", "Gate: after", (SeriesSpec("bridge", "lookups; gates: the bridge", "o"),
                                         SeriesSpec("other", "gates: the other bridge", "^", S.COMPARE)),
              rules=(0.20, 0.50), pair=("bridge", ("other",)))),
    (("null", "random direction"), ("gap", "the decisive gap"), ("rule", "the rule's bars")),
)  # fmt: skip
ORDER = CurveSpec(
    "f_order_then_identity_all_models",
    "The donor's last two tokens copied in at one layer (memory → prompt): % of patched answers at the sentence in "
    "the same place minus % at the donor entity's, by the sentence asked, in 5-, 8- and 12-sentence lists.",
    "the sentence the donor asks (its place in the list)",
    "same place − donor's entity (points)",
    (SeriesSpec("5", "5 sentences", "o"), SeriesSpec("8", "8 sentences", "s"), SeriesSpec("12", "12 sentences", "^")),
    xlim=(0.4, 13.6), ylim=(-112, 112), yticks=(-100, -50, 0, 50, 100), xticks=(1, 2, 3, 5, 8, 12),
    chance=(0.0, ""), rule_segments=((0.0, 0.4, 2.5), (100 * 0.05, 2.5, 13.6)), dodge=0.24,
    lines=(("chance", "no preference (0)"), ("rule", "the rule's bars (pooled)")),
    verdict_note="beside n: per list length ✓ holds · ✗ fails", legend_cols=4,
)  # fmt: skip
DEPTH = CurveSpec(
    "f_patch_outcomes_by_depth_all_models",
    "The donor's last two tokens copied in at one layer (memory → prompt): % of patched answers at the sentence in "
    "the same place, at the donor entity's sentence and at the donor's own digit, by depth (95% bands).",
    "depth (% of the model's layers)",
    "% of patched answers",
    (SeriesSpec("position", "same place in the list", "o"), SeriesSpec("identity", "the donor's entity", "s", S.COMPARE),
     SeriesSpec("value", "the donor's digit", "^", S.COMPARE2)),
    xlim=(0, 100), ylim=(0, 100), yticks=(0, 50, 100), xticks=(0, 50, 100), chance=(100 * G.CHANCE, "chance"),
    rules=((10.0, "10%"),), bands=True,
    lines=(("chance", "chance (20%)"), ("rule", "the digit's bar (10%)")),
    marks=(MarkSpec("used", "v", S.INK, True, "layer finding 5 uses"),),
    label_at=(("used", ("position", "identity")),),
)  # fmt: skip
PUSH = CurveSpec(
    "f_lens_push_recall_not_lookup_all_models",
    "A push along the lens's direction for the other bridge at the stated bridge's sentence or word: % of lookups and "
    "recalls switched by depth, at each layer's valid cell with the most recalls. Dashed: a random push.",
    "depth (% of the model's layers)",
    "% switched",
    (SeriesSpec("lookup", "lookups", "o"), SeriesSpec("recall", "recalls (the control)", "s", S.COMPARE),
     SeriesSpec("random", "random push, lookups", "", S.COMPARE2)),
    xlim=(0, 100), ylim=(0, 100), yticks=(0, 50, 100), xticks=(0, 50, 100),
    rules=((10.0, "10%"), (30.0, "30%")),
    lines=(("rule", "the rule's bars"),),
    marks=(MarkSpec("main", "v", S.INK, True, "the main rule's cell"),
           MarkSpec("amended", "v", S.INK, False, "the amended rule's cell")),
    label_at=(("main", ("lookup", "recall")),),
    verdict_note="beside n: ▼ / ▽ rule ✓ holds · ✗ fails · ≈ inconclusive",
)  # fmt: skip
GAP = CurveSpec(
    "f_layer_gap_lens_vs_patch_27b",
    "Qwen3.6-27B, fresh scenes, at the stated bridge: % of lookups switched by layer under a lens push, the full patch "
    "of the residual, an input-embedding push and a random push (valid cells only).",
    "layer (of 64)",
    "% of lookups switched",
    (SeriesSpec("lens", "lens push", "o"), SeriesSpec("patch", "full patch", "s", S.COMPARE),
     SeriesSpec("embed", "embedding push", "^", S.COMPARE2), SeriesSpec("random", "random push", "", "#b5b5b5")),
    xlim=(10, 36), ylim=(0, 100), yticks=(0, 50, 100), xticks=(12, 16, 20, 24, 28, 32),
    rules=((5.0, "5%"),),
    lines=(("rule", "stop bar: upper end < 5%"), ("gap", "the gap between the stops")),
    marks=(MarkSpec("stop lens", "v", S.MODEL["27b"].color, True, "lens push stops"),
           MarkSpec("stop patch", "v", S.COMPARE, True, "full patch stops"),
           MarkSpec("stop embed", "v", S.COMPARE2, True, "embedding push stops")),
    span_marks=("stop lens", "stop patch"),
    panel_titles=(("w", "At the bridge's word"), ("s", "At the bridge's sentence")),
    verdict_note="beside n: the layer-gap rule ✓ holds", hatch_in_legend=False,
)  # fmt: skip


# ---------------------------------------------------------------- the titles: each figure's outcome, from its data


PANEL_WORDS = {"prose": "prose", "table": "tables", "JSON": "JSON", "long context": "long context"}
TITLE_NAME = {
    "27b": "the 27B",
    "9b": "the 9B",
    "olmo_hybrid": "Olmo-Hybrid",
    "122b": "the 122B",
    "32b": "the 32B",
    "olmo": "OLMo-3",
    "muse": "Muse",
    "gemma": "Gemma 4",
}  # short names, for titles


def cells(data: DotData, panel: str | None = None) -> list[tuple[str, str, Mark]]:
    return [(p, m.key, data.marks[(p, m.key)]) for p in data.panels for m in S.MODELS
            if (p, m.key) in data.marks and (panel is None or p == panel)]  # fmt: skip


def title_late(data: DotData) -> str:
    """The cells that fail, split by the rule's reason: the lookup survives the block, or (a hybrid) blocking the
    DeltaNet layers instead breaks it too."""
    survives: dict[str, list[str]] = {}
    deltanet: dict[str, list[str]] = {}
    for p, k, mk in cells(data):
        if mk.status == "value" and mk.verdict == "fails":
            (deltanet if "DeltaNet" in mk.why else survives).setdefault(k, []).append(PANEL_WORDS.get(p, p))
    out = "Blocking the late read breaks the lookup on every model tested"
    if survives:
        out += " except " + join_and([f"{TITLE_NAME[k]} ({join_and(ps)})" for k, ps in survives.items()])
    if deltanet:
        out += "; on " + join_and([f"{TITLE_NAME[k]}'s {join_and(ps)}" for k, ps in deltanet.items()])
        out += " the DeltaNet layers matter too"
    return out


def counts_of(marks: list[Mark]) -> tuple[int, int]:
    h = sum(mk.status == "value" and mk.verdict == "holds" for mk in marks)
    return h, h + sum(mk.status == "value" and mk.verdict == "fails" for mk in marks)


def title_name_digit(data: DotData) -> str:
    h, j = counts_of([mk for *_, mk in cells(data)])
    return f"The last tokens read the answer's digit, not the entity's name, in {h} of the {j} cells judged"


def title_order(data: CurveData) -> str:
    vs = [s.verdict for p in data.panels.values() for s in p.series if s.y]
    h, j = vs.count("holds"), vs.count("holds") + vs.count("fails")
    return f"The order label for the 1st–2nd sentence, identity after, holds in {h} of {j} tests"


def title_counting(data: DotData) -> str:
    (h1, j1), (h2, j2), (h3, j3) = (counts_of([mk for *_, mk in cells(data, p)]) for p in data.panels)
    return (f"The label counts order in the list, not place in the text, on {h1} of {j1} models when filler moves, "
            f"on {h2} of {j2} with a sentence more and {h3} of {j3} with one fewer")  # fmt: skip


def title_depth(data: CurveData) -> str:
    vals = []
    for p in data.panels.values():
        pos = next((s for s in p.series if s.key == "position"), None)
        if pos and "used" in p.marks:
            at = [t for x, t in zip(pos.x, pos.y, strict=True) if t is not None and abs(x - p.marks["used"]) < 1e-6]
            vals += [100 * t[0] for t in at if finite(t)]
    if not vals:
        return "Where the last-two-token patch moves the answer, by depth"
    return (f"Before the donor's digit arrives, {min(vals):.0f}–{max(vals):.0f}% of patched answers go to the sentence "
            "in the same place in the list")  # fmt: skip


def title_lens(data: DotData) -> str:
    holds = [TITLE_NAME[k] for _, k, mk in cells(data, "contrast") if mk.status == "value" and mk.verdict == "holds"]
    fails = [TITLE_NAME[k] for _, k, mk in cells(data, "contrast") if mk.status == "value" and mk.verdict == "fails"]
    if not holds and not fails:
        return "The lens part of a stated bridge: no model judged yet"
    out = "Lookups ignore the lens part of a stated bridge on " + (join_and(holds) if holds else "no model")
    return out + (f", not on {join_and(fails)}" if fails else "")


def title_push(data: CurveData, grid_verdicts: dict[str, str]) -> str:
    holds = [TITLE_NAME[k] for k, v in grid_verdicts.items() if v == "holds"]
    other = [(TITLE_NAME[k], v) for k, v in grid_verdicts.items() if v in ("inconclusive", "fails")]
    out = "A lens push at the stated bridge switches recalls but not lookups on " + (join_and(holds) or "no model")
    if other:
        out += (
            "; on "
            + join_and([lab for lab, _ in other])
            + " the lookups move too ("
            + join_and(sorted({v for _, v in other}))
            + " by the main rule)"
        )
    return out


def title_gap(data: CurveData) -> str:
    p = data.panels.get("w")
    if not p or "stop lens" not in p.marks or "stop patch" not in p.marks:
        return "The layer gap between the lens push and the full patch: not run"
    d = p.marks["stop patch"] - p.marks["stop lens"]
    if d <= 2:
        return "The full patch stops moving lookups with the lens push"
    return f"At the stated bridge's word the full patch keeps moving lookups {d:.0f} layers after the lens push stops"


@dataclass(frozen=True)
class FigureDef:
    spec: DotSpec | CurveSpec
    collect: Callable[[Grid, Source], DotData | CurveData]
    title: Callable[..., str]
    keys: tuple[str, ...] | None = None  # curve panels that are not the eight models


FIGURES: dict[str, FigureDef] = {
    LATE.stem: FigureDef(LATE, collect_late, title_late),
    NAME_DIGIT.stem: FigureDef(NAME_DIGIT, collect_name_digit, title_name_digit),
    ORDER.stem: FigureDef(ORDER, collect_order, title_order),
    COUNTING.stem: FigureDef(COUNTING, collect_counting, title_counting),
    DEPTH.stem: FigureDef(DEPTH, collect_depth, title_depth),
    LENS.stem: FigureDef(LENS, collect_lens, title_lens),
    PUSH.stem: FigureDef(PUSH, collect_push, title_push),
    GAP.stem: FigureDef(GAP, lambda grid, src: collect_layer_gap(src), title_gap, keys=("w", "s")),
}
ONE_MODEL = {GAP.stem}  # figures that are one model's test by design


def title_for(name: str, data: DotData | CurveData, grid: Grid) -> str:
    f = FIGURES[name]
    if name == PUSH.stem:
        verdicts = {m.key: word(r["verdict"]) for m in S.MODELS if (r := grid.get(m.key, "f7", "main rule"))}
        return f.title(data, verdicts)
    return f.title(data)


def draw(name: str, data: DotData | CurveData, lay: Layout, title: str = "") -> Figure:
    f = FIGURES[name]
    if isinstance(f.spec, DotSpec):
        assert isinstance(data, DotData)
        return draw_dots(f.spec, data, title, lay)
    assert isinstance(data, CurveData)
    return draw_curves(f.spec, data, title, list(f.keys) if f.keys else None, lay)


@dataclass
class Rendered:
    fig: Figure
    data: DotData | CurveData
    step: int  # the LAYOUTS step that has no overlap (or the last one tried)
    overlaps: list[tuple[str, str]]
    title: str = ""


def render(name: str, grid: Grid, src: Source, mask: bool = False) -> Rendered:
    """Collect the figure's cells once, title it by its outcome, then draw it with each LAYOUTS step in turn until no
    text touches another text or a mark (plot_style.overlaps); the last step's overlaps are kept when none is clean."""
    data = FIGURES[name].collect(grid, src)
    title = title_for(name, data, grid)
    for step, lay in enumerate(LAYOUTS):
        fig = draw(name, data, lay, title)
        bad = S.overlaps(fig, mask=mask)
        if not bad or step == len(LAYOUTS) - 1:
            return Rendered(fig, data, step, bad, title)
        plt.close(fig)
    raise AssertionError("unreachable")


def counts(data: DotData | CurveData) -> tuple[int, int]:
    """(cells drawn with a value, cells drawn as a label): the status log's only numbers. A curve figure's cell is a
    panel, or one list length of the order figure."""
    if isinstance(data, DotData):
        with_value = sum(mk.status == "value" for mk in data.marks.values())
        return with_value, len(data.marks) - with_value
    drawn = [p for p in data.panels.values() if p.status in ("value", "not interpretable")]
    gaps = sum(1 for p in drawn for s in p.series if not s.y)
    return len(drawn), len(data.panels) - len(drawn) + gaps


def status_line(name: str, r: Rendered, show_title: bool = False) -> list[str]:
    """The log's lines for one figure: its overlap count and how many cells have a value (and, once the results are
    open, its title); colliding texts named by role where they could carry a value."""
    with_value, label = counts(r.data)
    out = [f"figure {name}: {len(r.overlaps)} overlaps (layout step {r.step}); cells with a value {with_value}, "
           f"drawn as a label {label}"]  # fmt: skip
    out += [f"  title: {r.title}"] if show_title else []
    out += [f"  overlap: {a} <> {b}" for a, b in r.overlaps]
    return out + [f"  unreadable cell: {e}" for e in r.data.errors]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp> folder (default: the newest)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--only", default=None, help="figure names, comma-separated")
    ap.add_argument("--titles", action="store_true", help="print each figure's title (results open only)")
    a = ap.parse_args(argv)
    grid_dir = Path(a.grid) if a.grid else latest_grid()
    grid = Grid(json.loads((grid_dir / "grid.json").read_text())["rows"])
    print("grid:", G.rel(grid_dir))
    src, failed = FileSource(), []
    for name in a.only.split(",") if a.only else list(FIGURES):
        r = render(name, grid, src, mask=not a.titles)
        S.save(r.fig, Path(a.out), name)
        plt.close(r.fig)
        print("\n".join(status_line(name, r, a.titles)))
        if r.overlaps:
            failed.append(name)
    if failed:
        print("overlapping text left in:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
