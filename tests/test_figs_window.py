"""scripts/figs/window: the band rule, the validity rule on pooled counts, the title by what holds, the grid cell
booking, the batch-A hook; MAIN and FULL from SYNTHETIC panels save without an overlap error and book no grid number
that disagrees with grid.csv; on the real runs (skipped when not pulled): two drawn points equal the files' values and
every grid number matches the grid."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from bridge_jspace.stats import wilson
from scripts import cross_model_figures as CMF
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import window as W

MAIN_LENS = "J++, synthetic, 00000000"


def book(tmp_path: Path, part_value: float = 29.4) -> RB.Book:
    """A grid.csv with the 122B's finding-2 'draw 2' cell (the lens part on lookups, layer 24)."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    w.writerow([G.MODEL["122b"].label, G.FINDING["f2"].name, "draw 2", MAIN_LENS, 180, f"{part_value} %",
                "[23.3, 36.5]", "", "fails", "", "-", "results/fake/verdict.json"])  # fmt: skip
    d = tmp_path / "grid"
    d.mkdir(exist_ok=True)
    (d / "grid.csv").write_text(out.getvalue())
    return RB.Book(d)


def t(k: int, n: int = 100) -> tuple[float, float, float]:
    return CMF.tri(wilson(k, n))


def series(key: str, layers: list[int], ks: list[int | None], n: int = 100, invalid: list[int | None] | None = None,
           ) -> W.Series:  # fmt: skip
    s = W.Series(key, layers, [None if k is None else t(k, n) for k in ks], [n] * len(layers), "results/fake/x.json")
    if invalid is not None:
        s.invalid = [None if k is None else t(k, n) for k in invalid]
    return s


def synth_panel(key: str, model: str) -> W.Panel:
    """A model with a map patch falling from 100 to 0, pushes at 30-70% of depth: the lens push moves no lookups
    (one layer invalid), recalls rise; the 122B with the lens-part points."""
    nl = CMF.n_layers(model)
    push = sorted({round(nl * f) for f in (0.3, 0.4, 0.5, 0.6, 0.7)})
    map_layers = sorted(set(range(0, nl, max(1, nl // 16))) | set(push))
    s = {"patch": series("patch", map_layers, [max(0, 100 - round(160 * la / nl)) for la in map_layers]),
         "lens_lookup": series("lens_lookup", push, [0, 0, None, 0, 0], invalid=[None, None, 0, None, None]),
         "lens_recall": series("lens_recall", push, [10, 40, None, 80, 90], invalid=[None, None, 70, None, None]),
         "random": series("random", push, [0] * len(push))}  # fmt: skip
    if model == "122b":
        s["part_lookup"] = series("part_lookup", [24, 27, 30], [52, 90, 36], 180)  # 28.9%, 50%, 20%
        s["part_recall"] = series("part_recall", [24, 27, 30], [68, 108, 63], 180)
    return W.Panel(key, model, s, W.band_of(s))


def synth_panels() -> dict[str, W.Panel]:
    return {**{m: synth_panel(m, m) for m in W.MODELS}, "27b first": synth_panel("27b first", "27b")}


def test_band_rule():
    p = synth_panel("27b", "27b")  # 64 layers: pushes at 19, 26, 32, 38, 45; patch >= 30% while 160 la / 64 <= 70
    assert p.band == [19, 26]  # 32 is invalid; at 38 and 45 the patch is below 30%
    s = dict(p.series)
    s["patch_same"] = series("patch_same", [19, 26, 32, 38, 45], [80, 20, 90, 90, 90])
    assert W.band_of(s) == [19, 38, 45]  # the same-scene patch decides where there is one; 32 still invalid
    s["lens_lookup"] = series("lens_lookup", [19, 26, 32, 38, 45], [6, 0, None, 0, 9])
    assert W.band_of(s) == [38]  # upper bound of 6/100 and 9/100 >= 5%


def test_validity_on_pooled_counts():
    def cell(fam: str, la: int, sc: float, d: str, rate: float, n: int = 100, changed: float | None = None) -> dict:
        return {"family": fam, "subset": "w", "layer": la, "scale": sc, "dir": d, "n": n,
                "to_x": [rate, 0, 0], "changed": [rate if changed is None else changed, 0, 0]}  # fmt: skip

    counts: W.Counts = {}
    for run in ([cell("BL", 10, 8.0, "lens", 0.0), cell("RL", 10, 8.0, "lens", 0.0, changed=0.12),
                 cell("BL", 10, 8.0, "random", 0.0)],
                [cell("BL", 10, 8.0, "lens", 0.02), cell("RL", 10, 8.0, "lens", 0.0, changed=0.06),
                 cell("BL", 10, 8.0, "random", 0.0)]):  # fmt: skip
        for c in run:
            key = (c["family"], "w", c["layer"], c["scale"], c["dir"])
            cur = counts.setdefault(key, {"to_x": (0, 0), "changed": (0, 0)})
            for what in ("to_x", "changed"):
                cur[what] = (cur[what][0] + round(c[what][0] * c["n"]), cur[what][1] + c["n"])
    assert W.valid(counts, 10, 8.0)  # pooled: 18 / 200 = 9% changed <= 10% (one draw alone: 12%, not valid)
    s = W.arm_series(counts, "x", "lens_lookup", "lens")
    assert s.layers == [10] and s.n == [200] and s.rates[0] == pytest.approx(t(2, 200))


def test_title_by_what_holds():
    panels = synth_panels()
    assert W.title(panels) == "A band: lookups ignore the lens, recall follows"
    for m in ("27b", "9b", "olmo"):  # recall in the band below 30%
        panels[m].series["lens_recall"] = series(
            "lens_recall", panels[m].series["lens_recall"].layers, [10, 20, None, 0, 0]
        )
    assert W.title(panels) == "In the band, only the 122B's recall follows the lens"
    for p in panels.values():
        p.band = []
    assert W.title(panels) == "No band where lookups ignore the lens"


def test_grid_cell_booked_and_checked(tmp_path: Path):
    s = series("part_lookup", [24, 27, 30], [53, 50, 20], 180)  # 53 / 180 = 29.44%: the grid's 29.4
    W.book_part_cell(s, book(tmp_path))
    num = s.number[24]
    assert (num.finding, num.model, num.setting, num.value) == ("f2", "122b", "draw 2", 29.4)
    with pytest.raises(ValueError, match="the grid"):
        W.book_part_cell(series("part_lookup", [24], [60], 180), book(tmp_path))


def test_extra_hook(tmp_path: Path):
    cells = []
    for la in (10, 20, 30):
        for d, rate in (("patch_dir", 0.5), ("patch_dir_perp", 0.1), ("random", 0.0)):
            k = round(rate * 100)
            cells.append({"family": "BL", "subset": "w", "layer": la, "scale": 8.0, "dir": d, "n": 100,
                          "to_x": list(wilson(k, 100)), "changed": list(wilson(k, 100))})  # fmt: skip
    p = tmp_path / "summary.json"
    p.write_text(json.dumps({"cells": cells}))
    extra = W.extra_arms(p)
    assert [s.key for s in extra] == ["patch_dir", "patch_dir_perp"] and extra[0].rates[0] == pytest.approx(t(50))


@pytest.mark.parametrize("kind", ["main", "full"])
def test_synthetic_saves(tmp_path: Path, kind: str):
    panels = synth_panels()
    W.book_part_cell(panels["122b"].series["part_lookup"], book(tmp_path, 28.9))  # 52 / 180
    panels["27b"].series["patch_dir"] = series("patch_dir", [19, 26, 32], [40, 20, 0])  # the hook drawn
    paths = W.build(kind, panels, tmp_path)  # raises on any overlapping or clipped text
    assert all(q.exists() for q in paths)
    data = tmp_path / "data" / f"window_{kind}.json"
    assert C.check_numbers(data, book(tmp_path, 28.9)) == []
    recs = json.loads(data.read_text())
    assert any(r["finding"] == "f2" for r in recs)  # the grid cell is booked as one
    assert {r["model"] for r in recs} == {"27b", "9b", "olmo", "122b"}


def test_real_runs_spot_check(tmp_path: Path):
    try:
        grid = CMF.latest_grid()
        panels = W.load(RB.Book(grid))
    except (SystemExit, FileNotFoundError):
        pytest.skip("runs not pulled")
    W.build("main", panels, tmp_path)
    data = tmp_path / "data" / "window_main.json"
    assert C.check_numbers(data, RB.Book(grid)) == []
    recs = json.loads(data.read_text())
    # the map: the 122B's full patch at layer 24 equals the map summary's cf flips there
    rate = next(r for r in json.loads((W.SP / W.MAPS["122b"] / "summary.json").read_text())["rates"]
                if r["family"] == "PP" and r["set"] == "bridge_word" and r["layer"] == 24)  # fmt: skip
    got = [
        r for r in recs if r["model"] == "122b" and r["extra"].get("series") == "patch" and r["extra"]["layer"] == 24
    ]
    assert len(got) == 1 and got[0]["value"] == pytest.approx(100 * rate["cf"]["flips"][0])
    # a push: the 122B's lens push on recalls at layer 30 equals the run's cell
    cell = next(c for c in json.loads((W.EPW.RESULTS / "qwen35_122b_d4_where" / "summary.json").read_text())["cells"]
                if (c["family"], c["subset"], c["layer"], c["scale"], c["dir"]) == ("BR", "w", 30, 8.0, "lens"))  # fmt: skip
    got = [
        r
        for r in recs
        if r["model"] == "122b" and r["extra"].get("series") == "lens_recall" and r["extra"]["layer"] == 30
    ]
    assert len(got) == 1 and got[0]["value"] == pytest.approx(100 * cell["to_x"][0], abs=1e-6)
    assert panels["122b"].band and all(la in panels["122b"].series["lens_lookup"].layers for la in panels["122b"].band)
