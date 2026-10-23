"""The redesigned figures of findings 2 and 7 (scripts/figs/stated_bridge.py, scripts/figs/lens_push_depth.py).

Synthetic inputs (a grid.csv, the verdict.json / summary.json files its cells name, in tmp_path): each figure saves its
MAIN and FULL version without an overlap error, every grid cell value drawn matches grid.csv (common.check_numbers)
and every control number matches the cell's control text (readme_build.Book.control); files that disagree with the
grid raise instead of being drawn. On the real newest grid, when it and its result files are here, the same checks.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from bridge_jspace.stats import wilson
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import lens_push_depth as LP
from scripts.figs import stated_bridge as SB

LENS = "J++, synthetic, 00000000"


def check_controls(path: Path, b: RB.Book) -> list[str]:
    """Mismatches between a data file's control numbers and the cells' control text (Book.control)."""
    bad = []
    for d in json.loads(path.read_text()):
        if d["source"] != SB.CONTROL:
            continue
        cs = [c for c in b.of(d["finding"], d["model"]) if c.setting == d["setting"] and c.part == d["part"]]
        xs = b.control(d["finding"], d["extra"]["control"], cs) if cs else []
        if len(xs) != 1 or abs(xs[0] - d["value"]) > 1e-9:
            bad.append(f"{path.name}: {d['finding']} {d['model']} {d['setting']} {d['extra']['control']}")
    return bad


def grid_csv(rows: list[tuple]) -> str:
    """rows: (model, finding, setting, n, value, (lo, hi), control, verdict, path)."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for m, f, s, n, v, ci, ctl, verdict, path in rows:
        w.writerow([G.MODEL[m].label, G.FINDING[f].name, s, LENS, "" if n is None else n,
                    "" if v is None else f"{v} %", "" if ci is None else f"[{ci[0]}, {ci[1]}]", ctl, verdict, "", "-",
                    path])  # fmt: skip
    return out.getvalue()


def tri(k: int, n: int) -> list:
    return [*wilson(k, n), n]


def f2_control(recall: int, rest: int, rnd: tuple[int, int], n: int) -> str:
    rl, rr = (tri(x, n) for x in rnd)
    return (f"recall, lens-readable part (the control, needs >= 30%): {recall}% "
            f"{G.ci_txt(*wilson(recall * n // 100, n)[1:])}; lookup, the rest (needs >= 50%): {rest}%; cell context at "
            f"layer 32; same-share random part (jspace_matched): lookups {G.pct(rl[0])} {G.ci_txt(rl[1], rl[2])} n={n}, "
            f"recalls {G.pct(rr[0])} {G.ci_txt(rr[1], rr[2])} n={n}")  # fmt: skip


def f2_files(tmp: Path) -> list[tuple]:
    """Four f2 cells (27B scene set 2 and table hold, 122B fails, 32B not interpretable) and their verdict files."""
    rows = []
    for m, s, look, rest, recall, recall_rest, verdict in (
        ("27b", "draw 2", 1, 146, 69, 49, "holds"),  # of 180: 1%, 81%, 38%, 27%
        ("122b", "draw 2", 53, 135, 68, 103, "fails"),
        ("32b", "draw 1", 6, 106, 11, 95, "not interpretable (the positive control fails)"),
        ("27b", "table", 2, 80, 35, 23, "holds"),
    ):
        n = 120 if s == "draw 1" else 180 if s == "draw 2" else 83
        lk, lr, rc, rr = (tri(k, n) for k in (look, rest, recall, recall_rest))
        if s == "table":
            v = {"by_format": {"table": {"PP_jspace": lk, "PP_not_jspace": lr, "PM_jspace": rc, "PM_not_jspace": rr}}}
        else:
            v = {"lookup": {"jspace": lk, "not_jspace": lr}, "recall": {"jspace": rc, "not_jspace": rr}}
        p = tmp / f"verdict_{m}_{s.replace(' ', '')}.json"
        p.write_text(json.dumps(v))
        ctl = f2_control(G.r100(rc[0]), G.r100(lr[0]), (0, 1), n)
        rows.append((m, "f2", s, n, round(100 * lk[0], 1), (round(100 * lk[1], 1), round(100 * lk[2], 1)), ctl,
                     verdict, str(p)))  # fmt: skip
    rows.append(("olmo_hybrid", "f2", "draw 2", None, None, None, "", "not testable (no lens)", ""))
    return rows


LAYERS = (12, 16, 20, 24, 28, 32, 36, 40, 44)


def f7_run(tmp: Path, name: str, where: str, layer: int, scale: float, lookup: dict[int, int],
           recall: dict[int, int], target: str = "qwen3.6-27b", layers: tuple[int, ...] = LAYERS) -> Path:  # fmt: skip
    """A synthetic early_push_where run of 100 items per cell: summary.json (decision, cells) and manifest.json."""
    d = tmp / name
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({"model": {"target": target}}))
    sub = LP.SUBSET[where]
    cells = []
    for la in layers:
        for fam, direction, k in (("BL", "lens", lookup.get(la, 0)), ("BR", "lens", recall.get(la, 0)),
                                  ("BL", "random", 0)):  # fmt: skip
            cells.append({"family": fam, "subset": sub, "layer": la, "scale": scale, "dir": direction, "n": 100,
                          "to_x": list(wilson(k, 100))})  # fmt: skip
    s = {"decision": {"primary": {"subset": sub, "layer": layer, "scale": scale}}, "cells": cells}
    (d / "summary.json").write_text(json.dumps(s))
    return d / "summary.json"


def f7_rows(tmp: Path) -> list[tuple]:
    recall = {12: 14, 16: 79, 20: 65, 24: 84, 28: 98, 32: 96, 36: 51, 40: 1, 44: 1}
    p2 = f7_run(tmp, "set2", "sentence", 24, 8.0, {16: 19}, recall)
    p1 = f7_run(tmp, "set1", "word", 16, 8.0, {16: 29}, recall)
    big = tuple(range(9, 34, 3))  # the 122B's grid: 48 layers
    p3 = f7_run(tmp, "big", "word", 33, 8.0, {27: 6}, {la: min(100, 3 * la) for la in big}, "qwen3.5-122b-a10b", big)
    small = tuple(range(6, 23, 2))  # 32 layers
    rec_small = {6: 2, 8: 3, 10: 6, 12: 40, 14: 86, 16: 96, 18: 93, 20: 31, 22: 17}
    p4 = f7_run(tmp, "nine", "sentence", 12, 4.0, {}, rec_small, "qwen3.5-9b", small)
    p5 = f7_run(tmp, "olmo", "word", 14, 8.0, {}, rec_small, "olmo-3-7b-instruct-jpp", small)
    ctl = "recall switched {r}% [{lo}, {hi}]; random push on lookups 0%; off-path changed 5% / 3%; cell: {c}"
    r24, r16, r33 = wilson(84, 100), wilson(79, 100), wilson(99, 100)
    r12, r14 = wilson(40, 100), wilson(86, 100)
    running = "missing (the run is running in the queue)"
    return [
        ("122b", "f7", "main rule", 100, 0.0, (0.0, 3.7),
         ctl.format(r=99, lo=G.r100(r33[1]), hi=G.r100(r33[2]), c="word, layer 33, 8x"), "holds", str(p3)),
        ("9b", "f7", "main rule, draw 2", 100, 0.0, (0.0, 3.7),
         ctl.format(r=40, lo=G.r100(r12[1]), hi=G.r100(r12[2]), c="sentence, layer 12, 4x"), "holds", str(p4)),
        ("olmo", "f7", "main rule", 100, 0.0, (0.0, 3.7),
         ctl.format(r=86, lo=G.r100(r14[1]), hi=G.r100(r14[2]), c="word, layer 14, 8x"), "holds", str(p5)),
        *((m, "f7", "main rule", None, None, None, "", running, "") for m in ("32b", "gemma")),
        ("27b", "f7", "main rule, draw 2", 100, 0.0, (0.0, 3.7),
         ctl.format(r=84, lo=G.r100(r24[1]), hi=G.r100(r24[2]), c="sentence, layer 24, 8x"), "holds", str(p2)),
        ("27b", "f7", "main rule", 100, 29.0, (21.0, 38.5),
         ctl.format(r=79, lo=G.r100(r16[1]), hi=G.r100(r16[2]), c="word, layer 16, 8x"),
         "inconclusive (the rule's reading: the lookup moves between 10% and 30%, or the gap is unclear)", str(p1)),
        ("muse", "f7", "main rule", None, None, None, "",
         "not interpretable (no cell where the lens push writes recall: the positive control fails)", ""),
        ("olmo_hybrid", "f7", "main rule", None, None, None, "", "not testable (no lens)", ""),
    ]  # fmt: skip


def synthetic(tmp: Path) -> RB.Book:
    g = tmp / "grid"
    g.mkdir()
    (g / "grid.csv").write_text(grid_csv(f2_files(tmp) + f7_rows(tmp)))
    return RB.Book(g)


@pytest.mark.parametrize("mod", [SB, LP])
def test_figures_from_synthetic_inputs(tmp_path, mod):
    b = synthetic(tmp_path)
    out = tmp_path / "out"
    for kind, make in (("main", mod.figure_main), ("full", mod.figure_full)):
        fr, numbers = make(b)
        C.save(fr, mod.STEM, numbers, out)  # raises on overlapping or clipped text
        data = out / "data" / f"{mod.STEM}_{kind}.json"
        assert C.check_numbers(data, b) == []
        assert check_controls(data, b) == []
        records = json.loads(data.read_text())
        assert any(d["source"] == "grid.csv" for d in records)  # the deciding numbers are grid cells
        assert all(d["source"] in ("grid.csv", SB.CONTROL) or Path(d["source"]).exists() for d in records)


def test_stated_bridge_bars_and_choices(tmp_path):
    b = synthetic(tmp_path)
    bars = SB.collect(b, "27b", "draw 2")
    assert bars is not None
    assert {f: set(p) for f, p in bars.parts.items()} == {"lookups": set(SB.PARTS), "recalls": set(SB.PARTS)}
    assert bars.parts["recalls"]["rest"].value == pytest.approx(100 * 49 / 180)  # from the verdict file
    assert SB.collect(b, "olmo_hybrid", "draw 2") is None  # no value: no bars
    assert SB.main_setting(b, "27b") == "draw 2" and SB.main_setting(b, "32b") == "draw 1"
    assert SB.untested(b) == "Not tested: 9B, OLMo-3, Muse, Gemma (no result); Olmo-Hybrid (no lens)."
    fr, _ = SB.figure_main(b)  # MAIN: judged cells only (27B holds, 122B fails), not the 32B
    assert len(fr.axes) == 2


def test_lens_push_curves_and_choices(tmp_path):
    b = synthetic(tmp_path)
    cv = LP.collect(b, "27b", "main rule, draw 2")
    assert cv is not None and (cv.where, cv.layer, cv.scale, cv.n_layers) == ("sentence", 24, 8.0, 64)
    assert [n.extra["layer"] for n in cv.points["lookup"]] == list(LAYERS)
    assert cv.depth == pytest.approx(37.5)
    assert LP.random_is_zero([cv])
    big = LP.collect(b, "122b", "main rule")
    assert big is not None and big.n_layers == 48 and big.depth == pytest.approx(68.75)
    fr, _ = LP.figure_main(b)  # MAIN: the README table's cell per model (scene set 2's main rule first)
    assert len(fr.axes) == 4
    exc, invalid = LP.notes(b, {"27b": "main rule, draw 2"})
    assert exc == ["27B set 1, main rule: 29% of lookups move at layer 16 (can't tell)"] and invalid == ["Muse"]


def test_files_that_disagree_with_the_grid_raise(tmp_path):
    b = synthetic(tmp_path)
    p = tmp_path / "verdict_27b_draw2.json"
    v = json.loads(p.read_text())
    v["recall"]["jspace"] = tri(90, 180)  # the grid says 38%
    p.write_text(json.dumps(v))
    with pytest.raises(ValueError, match="disagrees"):
        SB.collect(b, "27b", "draw 2")
    s = tmp_path / "set2" / "summary.json"
    d = json.loads(s.read_text())
    d["decision"]["primary"]["subset"] = "w"  # the grid's test point is at the sentence
    s.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="test point"):
        LP.collect(b, "27b", "main rule, draw 2")


def newest_real_grid() -> Path | None:
    try:
        g = SB.newest_grid()
    except SystemExit:
        return None
    b = RB.Book(g)
    paths = [c.path for f in ("f2", "f7") for c in b.of(f) if c.value is not None]
    return g if paths and all((C.REPO / p).exists() for p in paths) else None


@pytest.mark.skipif(newest_real_grid() is None, reason="no grid with its finding 2 and 7 result files here")
@pytest.mark.parametrize("mod", [SB, LP])
def test_real_grid_numbers_match(tmp_path, mod):
    g = newest_real_grid()
    assert g is not None
    assert mod.main(["--grid", str(g), "--out", str(tmp_path)]) == 0
    b = RB.Book(g)
    for kind in ("main", "full"):
        data = tmp_path / "data" / f"{mod.STEM}_{kind}.json"
        assert C.check_numbers(data, b) == []
        assert check_controls(data, b) == []
