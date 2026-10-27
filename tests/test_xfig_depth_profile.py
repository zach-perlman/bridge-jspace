"""scripts/xfig_depth_profile (X-fig): the paired recall-minus-lookup difference, Zach's per-window gap and its
rows/summary check, the J++-only lens checks, the data file and caption, and the figure saving without an overlap
error, all on synthetic rows; on the real inputs (skipped without Zach's commit) the input check passes."""

from __future__ import annotations

import subprocess

import pytest

from scripts import xfig_depth_profile as X

SD = X.SD


def items(n: int, whole: int, without: int, fam: str) -> tuple[dict[str, dict], dict[str, str]]:
    """n items of one family, one per scene: `whole` switched by the whole change, `without` by the change minus J."""
    it = {f"{fam}-{i}": {"full": i < whole, "not_jspace": i < without} for i in range(n)}
    return it, {f"{fam}-{i}": f"s{i}" for i in range(n)}


def test_paired_diff():
    look, ls = items(20, 20, 18, "PP")  # lookups: J-dependence 0.1
    rec, rs = items(20, 20, 4, "PM")  # recalls: 0.8
    v, lo, hi, n = X.paired_diff(look, rec, ls, rs)
    assert v == pytest.approx(0.7)
    assert lo <= v <= hi
    assert n == 20
    rs["PM-0"] = "elsewhere"
    with pytest.raises(ValueError, match="different scenes"):
        X.paired_diff(look, rec, ls, rs)
    (none, ns), (rec5, rs5) = items(5, 0, 0, "PP"), items(5, 5, 0, "PM")  # no lookup switched by the whole change
    with pytest.raises(ValueError, match="undefined"):
        X.paired_diff(none, rec5, ns, rs5)


def sweep(acc: dict[str, int], n: int = 10) -> tuple[dict, list[dict], list[tuple[str, int, int]]]:
    """One window L4-8, n items per word over 5 bridges, all right unedited; acc: word -> items right knocked out."""
    rows, cells = [], {}
    for w in X.WORDS:
        for i in range(n):
            rows.append(
                {"band": "-", "condition": "none", "family": w, "kind": "clean", "id": f"{w}{i}", "correct": True}
            )
            rows.append({"band": "L4-8", "condition": "paper10", "family": w, "kind": "clean", "id": f"{w}{i}",
                         "correct": i < acc[w], "bridge": f"b{i % 5}", "bridge_protected": False})  # fmt: skip
        cells[f"{w}/clean"] = {"paper10": {"n": n, "accuracy": acc[w] / n}}
    summary = {"unedited_accuracy": {f"{w}/clean": 1 for w in X.WORDS}, "cells": {"L4-8": cells}}
    return summary, rows, [("L4-8", 4, 8)]


def test_zach_gap_and_check():
    summary, rows, windows = sweep({"PP": 10, "MP": 8, "PM": 4, "MM": 2})  # losses 0, 20, 60, 80 points
    (p,) = X.zach_points(summary, rows, windows, n_boot=200)
    assert (p.lookup, p.memory, p.gap) == pytest.approx((10, 70, 60))
    assert p.ci[0] <= p.gap <= p.ci[1]
    assert p.n == {w: 10 for w in X.WORDS}
    summary["cells"]["L4-8"]["PM/clean"]["paper10"]["accuracy"] = 0.5  # a summary that is not its rows
    with pytest.raises(ValueError, match=r"rows and summary\.json differ"):
        X.zach_points(summary, rows, windows, n_boot=10)
    with pytest.raises(ValueError, match="knock-out rows"):
        X.check_sweep("s", {"bands": ["L4-8"]}, *sweep({w: 5 for w in X.WORDS})[:1], rows[1:])


PINS_TEXT = """TARGETS = {
    "toy-7b": {
        "repo": "org/Toy-7B",
        "n_layers": 32,
        "lenses": {"jpp": ("local", "cache/toy/jpp.pt", "ab12")},
    },
}
"""


def test_lens_checks(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(X.ZACH_LENS, "toy_ctrl_sweep_v1", ("local", "cache/toy/jpp.pt", "ab12"))
    assert X.lens_of_sweep("toy_ctrl_sweep_v1", {"lens": ["jpp", "ab12"]}, PINS_TEXT)["kind"] == "ours"
    with pytest.raises(ValueError, match="expected jpp"):
        X.lens_of_sweep("toy_ctrl_sweep_v1", {"lens": ["jlens", "ab12"]}, PINS_TEXT)
    with pytest.raises(ValueError, match=r"not in pins\.py"):
        X.lens_of_sweep("toy_ctrl_sweep_v1", {"lens": ["jpp", "ab12"]}, "")
    with pytest.raises(ValueError, match="plain J-lens"):
        X.lens_of_sweep("qwen3_32bj_ctrl_sweep_v1", {"lens": ["jpp", "ab12"]}, PINS_TEXT)
    targets = {"toy-7b": {"frozen_lens_sha256": "ab12", "lenses": {"jpp": ("local", "cache/toy/jpp.pt", "ab12")}},
               "toy-7b-jlens": {"frozen_lens": "jlens", "frozen_lens_sha256": "cd34",
                                "lenses": {"jlens": ("hub", "toy/jlens.pt", "r")}}}  # fmt: skip
    ok = {"model": {"target": "toy-7b"}, "lens": {"jpp": ["local", "cache/toy/jpp.pt", "ab12"], "sha256": "ab12"}}
    assert X.lens_of_run("toy_parts", ok, targets)["sha256"] == "ab12"
    plain = {"model": {"target": "toy-7b-jlens"}, "lens": {"jlens": ["hub", "toy/jlens.pt", "r"], "sha256": "cd34"}}
    with pytest.raises(ValueError, match="expected jpp"):
        X.lens_of_run("toy_jlens_parts", plain, targets)
    assert X.zach_n_layers(PINS_TEXT, "toy-7b") == 32
    with pytest.raises(ValueError, match="no n_layers"):
        X.zach_n_layers(PINS_TEXT, "other")


def toy_panel(model: str, same: bool, band: tuple[int, int] | None, split: int | None) -> tuple[X.Panel, X.Shown]:
    lens = {"name": "jpp", "source": "local", "file": "cache/toy/jpp.pt", "sha256": "ab12" * 16, "kind": "ours"}
    ck = {"repo": "org/Toy", "revision": "1" * 40}
    dan = X.DanRuns(["toy_parts"], {}, {"toy_parts": lens}, ck, 32, {})
    z = X.Sweep("toy_ctrl_sweep_v1", {"model": ck if same else {**ck, "repo": "org/Toy-DPO"}}, {}, [], [], lens, 32,
                band, "results/ablate_v2/band_choice/toy_ctrl_sweep_v1.json", (10, 14),
                "results/ablate_v2/c1_v2/toy.json", {})  # fmt: skip
    dep = lambda v: SD.Dep(v, v - 0.1, v + 0.1, 0.9, 0.5, 180)  # noqa: E731
    dps = [X.DanPoint(SD.Cell(model, "toy_parts", where, la, hollow, False, {"lookups": dep(0.2), "recalls": dep(0.8)},
                              {}), 0.6, 0.45, 0.75, 180)
           for where, la, hollow in (("bridge_word", 6, False), ("bridge_word", 10, False), ("bridge_word", 14, False),
                                     ("context", 16, True), ("context", 18, True))]  # fmt: skip
    zps = [X.ZachPoint(f"L{s}-{s + 4}", s, s + 4, 50.0, 10.0, 40.0, (25.0, 55.0), {w: 50 for w in X.WORDS})
           for s in range(0, 28, 2)]  # fmt: skip
    kind = "choice" if band else ""
    return X.Panel(model, dan, z), X.Shown(model, SD.C.MODEL[model].name, 32, dps, zps, split, band, kind, same)


def test_data_rows_and_caption():
    p, s = toy_panel("olmo", same=False, band=None, split=None)
    rows = X.data_rows(p, s, "c" * 40)
    drawn = [r for r in rows if r["drawn"]]
    assert {r["quantity"] for r in drawn} == {"recall_minus_lookup_J_dependence",
                                              "memory_final_minus_lookup_final_loss_pts"}  # fmt: skip
    assert all(r["source_file"] and r["row_key"] and r["source_commit"] and r["lens_sha256"] for r in drawn)
    assert {r["source_commit"] for r in drawn if r["side"] == "zach"} == {X.ZACH_COMMIT}
    assert len(drawn) == len(s.dan) + len(s.zach)  # no split, no band: nothing else drawn
    text = X.caption_md({"olmo": p}, [s], ["olmo: no band shaded"])
    for needed in ("held-out data", "lookups excluded", "same J++ dictionary", "post hoc until X0",
                   "bf16 weights, used on the FP8 model", "not one checkpoint", "no band shaded"):  # fmt: skip
        assert needed in text
    p2, s2 = toy_panel("9b", same=True, band=(12, 16), split=12)
    q = [r["quantity"] for r in X.data_rows(p2, s2, "c" * 40) if r["drawn"]]
    assert q.count("split_layer") == 1
    assert {"band_first_layer", "band_last_layer"} <= set(q)
    assert "statement 1 is not checked" not in X.caption_md({"9b": p2}, [s2], [])
    s2.band_kind = "record"  # --band-of-record: C1's band, whose held-out choice is not on file
    assert "statement 1 is not checked" in X.caption_md({"9b": p2}, [s2], [])
    assert {r["source_file"] for r in X.data_rows(p2, s2, "c" * 40) if r["quantity"] == "band_first_layer"} == {
        p2.zach.middle_path
    }


def test_figure_saves_without_overlap(tmp_path):
    shown = [toy_panel("9b", True, (12, 16), 12)[1], toy_panel("27b", True, (16, 20), 16)[1],
             toy_panel("olmo", False, None, None)[1], toy_panel("122b", True, (10, 14), 12)[1]]  # fmt: skip
    shown[3].band_kind = "record"
    fr = X.figure(shown, {"olmo": ("allenai/Olmo-3-7B-Instruct", "allenai/Olmo-3-7B-Instruct-DPO")})
    assert X.C.PS.overlaps(fr.fig) == []
    texts = [t.get_text() for t in fr.fig.texts]
    assert any("*Dan Olmo-3-7B-Instruct, Zach Olmo-3-7B-Instruct-DPO" in t for t in texts)
    fr.fig.savefig(tmp_path / "x.png", dpi=X.C.DPI)
    assert (tmp_path / "x.png").stat().st_size > 0


def test_real_inputs(capsys: pytest.CaptureFixture[str]):
    have = subprocess.run(["git", "-C", str(X.REPO), "cat-file", "-e", f"{X.ZACH_COMMIT}^{{commit}}"],
                          capture_output=True, check=False).returncode == 0  # fmt: skip
    if not have or not all((SD.SP / run / "outcomes.jsonl").exists() for _, run, *_ in SD.CELLS):
        pytest.skip("Zach's commit not fetched or the parts runs not pulled")
    assert X.check_inputs() == 0
    out = capsys.readouterr().out
    assert "DIFFERENT" in out.split("== OLMo-3-7B")[1].split("==")[0]  # Dan's Instruct vs Zach's Instruct-DPO
