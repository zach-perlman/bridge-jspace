"""scripts/figs/patch_by_depth (guide 6e) and scripts/figs/layer_gap (guide 6h).

Synthetic inputs (no result file read): each figure, MAIN and FULL, saves without an overlap error, draws no empty
panel, and its data file has no grid number that disagrees with grid.csv; the window band and the stops follow their
rules; a stop that disagrees with the summary raises; the dose hook draws a third line. Real runs (skipped when not
pulled): the drawn points equal the run files' values (two spot checks per figure), the depth counts equal
cross_model_figures.roles_by_layer's, and the layer-gap curves equal the old loader's (from outcomes.jsonl).
"""

from __future__ import annotations

import collections
import csv
import io
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from scripts import cross_model_figures as CMF
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import layer_gap as LG
from scripts.figs import patch_by_depth as PD

MAIN_LENS = "J++, synthetic, 00000000"


def synth_book(tmp_path: Path) -> RB.Book:
    """A grid.csv with one finding-5 'draw 1' cell per model (holds)."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for m in C.MODELS:
        w.writerow([G.MODEL[m.key].label, G.FINDING["f5"].name, "draw 1", MAIN_LENS, 300, "50.0 pts", "[40.0, 60.0]",
                    "layer 10 (synthetic)", "holds", "", "-", f"results/fake/{m.key}/outcomes.jsonl"])  # fmt: skip
    d = tmp_path / "grid"
    d.mkdir()
    (d / "grid.csv").write_text(out.getvalue())
    return RB.Book(d)


# ---------------------------------------------------------------- patch_by_depth, synthetic


def synth_counts(n_layers: int) -> dict[int, collections.Counter]:
    """Eight swept layers from 40% to 96% of the depth: nothing moves, then two window layers (order and identity),
    then the digit."""
    layers = sorted({round(n_layers * f) for f in (0.40, 0.48, 0.56, 0.64, 0.72, 0.80, 0.88, 0.96)})
    out = {}
    for i, la in enumerate(layers):
        if i < 3:
            out[la] = collections.Counter(none=300)
        elif i < 5:
            out[la] = collections.Counter(position=120, identity=75, context=15, none=90)
        else:
            out[la] = collections.Counter(value=270, position=6, none=24)
    return out


def synth_depth(faded: dict[str, str] | None = None) -> dict[str, PD.Depth]:
    faded = faded or {}
    return {m.key: PD.depth_of(m.key, synth_counts(CMF.n_layers(m.key)), f"results/fake/{m.key}/outcomes.jsonl",
                               faded=faded.get(m.key, "")) for m in C.MODELS}  # fmt: skip


def test_window_and_spans():
    d = PD.depth_of("27b", synth_counts(64), "x")
    assert d.window == d.layers[3:5]  # moved, digit absent; not the quiet layers, not the digit's
    ((lo, hi),) = d.spans()
    assert lo == pytest.approx(100 * (d.layers[2] + d.layers[3]) / 2 / 64)
    assert hi == pytest.approx(100 * (d.layers[4] + d.layers[5]) / 2 / 64)
    one = PD.depth_of("27b", {10: collections.Counter(position=50, none=50), 12: collections.Counter(value=99, none=1)},
                      "x")  # fmt: skip
    assert one.window == [10] and one.spans() == [(pytest.approx(100 * 9 / 64), pytest.approx(100 * 11 / 64))]
    # the digit's upper bound at the bar: not in the window, even though answers move
    near = PD.depth_of("27b", {10: collections.Counter(value=8, position=50, none=42)}, "x")
    assert near.window == []


def test_title_counts_models_without_a_window():
    data = synth_depth()
    assert PD.title(data) == "Order or identity first, the donor's digit later"
    data["muse"] = PD.depth_of("muse", {20: collections.Counter(none=300), 30: collections.Counter(value=300)}, "x")
    assert PD.title(data) == "On 7 of 8 models: order or identity first, digit later"


@pytest.mark.parametrize("kind", ["main", "full"])
def test_depth_synthetic_saves(tmp_path: Path, kind: str):
    b = synth_book(tmp_path)
    paths = PD.build(kind, synth_depth(), {}, b, tmp_path)  # raises on any overlapping or clipped text
    assert all(p.exists() for p in paths)
    data_file = tmp_path / "data" / f"patch_by_depth_{kind}.json"
    recs = json.loads(data_file.read_text())
    assert C.check_numbers(data_file, b) == []
    models = {r["model"] for r in recs}
    assert models == (set(PD.MAIN_MODELS) if kind == "main" else {m.key for m in C.MODELS})
    assert all(r["source"].endswith("outcomes.jsonl") and r["finding"] is None for r in recs)


def test_depth_full_no_empty_panel_and_faded(tmp_path: Path):
    b = synth_book(tmp_path)
    data = synth_depth({"olmo": "off-path control"})
    del data["muse"]
    fr, nums = PD.draw("full", data, {"muse": "run failed"}, b)
    assert len(fr.fig.axes) == 7  # the missing model is named in the caption, not drawn as an empty panel
    cap = next(t.get_text() for t in fr.fig.texts if t.get_gid() == "caption")
    assert "Muse (run failed)" in cap
    status = [t.get_text() for ax in fr.fig.axes for t in ax.texts if t.get_gid() == "status"]
    assert status == ["not interpretable\n(off-path control)"]  # drawn pale with a short grey label (FULL only)
    C.save(fr, PD.STEM, nums, tmp_path)
    fr, _ = PD.draw("main", data, {"muse": "run failed"}, b)
    assert len(fr.fig.axes) == 4
    plt.close(fr.fig)


# ---------------------------------------------------------------- layer_gap, synthetic

LAYERS = list(range(12, 36, 2))


def cell(fam: str, sub: str, la: int, sc: float, d: str, k: int, n: int = 100) -> dict:
    from bridge_jspace.stats import wilson

    t = list(wilson(k, n))
    return {
        "family": fam,
        "subset": sub,
        "layer": la,
        "scale": sc,
        "dir": d,
        "n": n,
        "to_x": t,
        "changed": t,
        "to_y": t,
    }


def synth_summary(dose: bool = False) -> dict:
    """Lens push moves lookups to layer 18 (8x invalid at 20-26: off-path 20%), the full patch to 26; recalls move
    under both; the dose arm (patch_dir) to 22."""
    cells = []
    for sub in ("w", "s"):
        for la in LAYERS:
            for sc in (4.0, 8.0):
                cells.append(cell("BL", sub, la, sc, "lens", 15 if la <= 18 else 0))
                cells.append(cell("BR", sub, la, sc, "lens", 70))
                for f in ("RL", "RR"):
                    cells.append(cell(f, sub, la, sc, "lens", 20 if sc == 8.0 and 20 <= la <= 26 else 0))
                for d in ("random", "embed"):
                    cells.append(cell("BL", sub, la, sc, d, 0))
                if dose:
                    cells.append(cell("BL", sub, la, sc, "patch_dir", 50 if la <= 22 else 0))
                    cells.append(cell("BR", sub, la, sc, "patch_dir", 90))
            cells.append(cell("BL", sub, la, 0.0, "patch", 80 if la <= 26 else 0))
            cells.append(cell("BR", sub, la, 0.0, "patch", 100))
            for f in ("RL", "RR"):
                cells.append(cell(f, sub, la, 0.0, "patch", 0))
    s: dict = {"cells": cells, "layer_gap": {sub: {"lens": {"stop": 20}, "patch": {"stop": 28}, "verdict": "H-gap"}
                                             for sub in ("w", "s")}}  # fmt: skip
    if dose:
        s["dose_test"] = {sub: {"patch_dir": {"stop": 24}} for sub in ("w", "s")}
    return s


def test_gap_arms_follow_the_rule(tmp_path: Path):
    p = tmp_path / "summary.json"
    p.write_text(json.dumps(synth_summary()))
    data = LG.load(p)
    lens, patch = data["w"]["lens"], data["w"]["patch"]
    assert (lens.stop, patch.stop, LG.gap_of(data["w"])) == (20, 28, 8)
    assert lens.invalid_top == [20, 22, 24, 26]  # only the 4x push is valid there
    assert [s for la, s in zip(lens.layers, lens.scale, strict=True) if la in (16, 22)] == [4.0, 4.0]  # ties: 4x
    assert LG.title(data["w"]) == "The full patch outlasts the lens push by 8 layers"
    assert LG.verdicts(p) == {"w": "holds", "s": "holds"}
    bad = synth_summary()
    bad["layer_gap"]["w"]["lens"]["stop"] = 22
    p.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="stops at 20 here, 22 in the summary"):
        LG.load(p)


@pytest.mark.parametrize("kind", ["main", "full"])
@pytest.mark.parametrize("with_dose", [False, True])
def test_gap_synthetic_saves(tmp_path: Path, kind: str, with_dose: bool):
    p = tmp_path / "summary.json"
    p.write_text(json.dumps(synth_summary(dose=with_dose)))
    data = LG.load(p)
    dose = {sub: a["patch_dir"] for sub, a in LG.load(p, arms=("patch_dir",)).items()} if with_dose else None
    if dose:
        assert dose["w"].stop == 24
    paths = LG.build(kind, data, LG.controls(p), dose, tmp_path, LG.verdicts(p))
    assert all(q.exists() for q in paths)
    data_file = tmp_path / "data" / f"layer_gap_{kind}.json"
    recs = json.loads(data_file.read_text())
    assert C.check_numbers(data_file, synth_book(tmp_path)) == []
    pushes = {r["extra"].get("push") for r in recs if "push" in r["extra"]}
    assert pushes == ({"lens", "patch", "patch_dir"} if with_dose else {"lens", "patch"})
    assert [r["value"] for r in recs if r["what"].startswith("layers between")] == [8.0] * (1 if kind == "main" else 2)


# ---------------------------------------------------------------- real runs (skipped when not pulled)


def outcome_rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines()]


@pytest.fixture(scope="module")
def real_depth():
    try:
        grid_dir = CMF.latest_grid()
    except SystemExit:
        pytest.skip("no grid")
    data, missing = PD.load(grid_dir)
    if not {"27b", "gemma"} <= set(data):
        pytest.skip("pointer_swap runs not pulled")
    return grid_dir, data, missing


def test_depth_real_matches_the_runs(real_depth, tmp_path: Path):
    grid_dir, data, missing = real_depth
    b = RB.Book(grid_dir)
    PD.build("main", data, missing, b, tmp_path)
    data_file = tmp_path / "data" / "patch_by_depth_main.json"
    assert C.check_numbers(data_file, b) == []
    recs = json.loads(data_file.read_text())
    for model, role in (("27b", "position"), ("gemma", "value")):
        d = data[model]
        rows = outcome_rows(C.REPO / d.source)
        old = CMF.roles_by_layer(rows)  # the old figure's loading
        assert old["layers"] == d.layers
        for r in ("position", "identity", "value"):
            assert all(math.isclose(a, b_) for t, u in zip(old[r], d.shares[r], strict=True)
                       for a, b_ in zip(t, u, strict=True))  # fmt: skip
        # spot check: the drawn point at the window's last layer, counted straight from the file
        la = d.window[-1]
        sel = [o for o in rows if o["source"] == "dissoc" and o["group"] == "last" and o["family"] == "RL"
               and str(o["layer"]) == str(la)]  # fmt: skip
        want = 100 * sum(o["role"] == role for o in sel) / len(sel)
        got = [
            r
            for r in recs
            if r["model"] == model and r["extra"].get("layer") == la and r["extra"].get("outcome") == role
        ]
        assert len(got) == 1 and got[0]["value"] == pytest.approx(want) and got[0]["n"] == len(sel)


def test_gap_real_matches_the_run(tmp_path: Path):
    if not LG.SUMMARY.exists():
        pytest.skip("layer-gap run not pulled")
    data = LG.load()
    assert (data["w"]["lens"].stop, data["w"]["patch"].stop) == (20, 28)
    assert LG.verdicts() == {"w": "holds", "s": "holds"}  # the summary's H-gap
    LG.build("main", data, LG.controls(), None, tmp_path)
    recs = json.loads((tmp_path / "data" / "layer_gap_main.json").read_text())
    cells = {(c["family"], c["subset"], c["layer"], c["scale"], c["dir"]): c
             for c in json.loads(LG.SUMMARY.read_text())["cells"]}  # fmt: skip
    for fam, la, push in (("BL", 16, "lens"), ("BL", 24, "patch"), ("BR", 24, "lens")):
        got = [r for r in recs if r["extra"].get("family") == fam and r["extra"].get("layer") == la
               and r["extra"].get("push") == push and r["extra"].get("subset") == "w"]  # fmt: skip
        assert len(got) == 1
        c = cells[(fam, "w", la, got[0]["extra"]["scale"], push)]
        assert got[0]["value"] == pytest.approx(100 * c["to_x"][0]) and got[0]["n"] == c["n"]
    assert [r["value"] for r in recs if r["what"].startswith("layers between")] == [8.0]
    # the summary-based curves equal the old figure's loader (cells from outcomes.jsonl, cross_model_figures)
    if not (LG.EPW.RESULTS / LG.RUN / "outcomes.jsonl").exists():
        return
    old = CMF.FileSource().layer_gap()
    assert old is not None
    for sub in ("w", "s"):
        for arm in ("lens", "patch"):
            for t, u in zip(old["subsets"][sub][arm], data[sub][arm].lookup, strict=True):
                assert (t is None) == (u is None)
                if t is not None and u is not None:
                    assert all(math.isclose(a, b) for a, b in zip(t, u, strict=True))
            assert old["subsets"][sub]["stops"][arm] == data[sub][arm].stop
