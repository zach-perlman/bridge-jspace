"""Batch 53, test 53.3 (scripts/x53_lastconflict.py): the layers from 51.10's peak and read files, the arms' vectors, the
rule's labels at the bars on planted numbers, the per-cell numbers recomputed from planted reads, and the run and verdict
stages end to end on 51.10's tiny fake model (CPU). No real model."""

import json

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x49_gain as G
from scripts import x51_jread as JR
from scripts import x53_lastconflict as LC
from tests.test_x51_jread import JFake, JLensFake, _jitem

LK, RC = X.LOOKUP, X.RECALL


def plant_51_10(root, run: str, peaks: dict, answers: dict) -> None:
    (root / run).mkdir(parents=True, exist_ok=True)
    (root / run / "peak.json").write_text(json.dumps({"peaks": peaks}))
    for stamp, shift in (("20261028T000000Z", 5), ("20261028T120000Z", 0)):  # the newest read decides
        d = root / f"read-{run}-{stamp}"
        d.mkdir()
        (d / "read.json").write_text(json.dumps({"answer": {k: {"layer": v + shift} for k, v in answers.items()}}))


def test_layers_are_the_read_peak_and_the_answer_layer_minus_2(tmp_path, monkeypatch):
    from bridge_jspace import pins

    monkeypatch.setattr(JR, "RESULTS", tmp_path / "x51_jread")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    run = LC.SOURCE_RUNS[pins.TARGET]
    plant_51_10(JR.RESULTS, run, {"lookup": 24, "recall": 27}, {"lookup": 29, "recall": 29})
    lay = LC.layers_of(pins.TARGET)
    assert lay["readers"]["lookup"]["layers"] == [24, 27] and lay["readers"]["recall"]["layers"] == [27]  # deduplicated
    assert lay["read_file"].endswith("20261028T120000Z/read.json") and lay["peak_file"].endswith(f"{run}/peak.json")


def test_the_real_51_10_files_give_the_briefs_layers():
    """The committed 51.10 files: the brief's read peaks (9B 24/24, 27B 60/56, Muse 32/40, Lightning 32/36)."""
    want = {
        "qwen3.5-9b": (24, 24),
        "qwen3.6-27b": (60, 56),
        "muse-glimmer-30b": (32, 40),
        "nemotron-3.5-lightning": (32, 36),
    }
    for target, (lk, rc) in want.items():
        if not (JR.RESULTS / LC.SOURCE_RUNS[target] / "peak.json").exists():
            pytest.skip("51.10's results are not in this checkout")
        lay = LC.layers_of(target)["readers"]
        assert (lay["lookup"]["peak"], lay["recall"]["peak"]) == (lk, rc)
        assert all(r["layers"][-1] == r["answer"] - 2 for r in lay.values())


def test_arm_vectors_rest_is_the_change_without_its_lens_part():
    g = torch.Generator().manual_seed(0)
    delta, pj, rj = (torch.randn(3, 8, generator=g) for _ in range(3))
    v = LC.arm_vectors(delta, pj, rj)
    assert set(v) == set(LC.ARMS) - {"none"}
    assert torch.equal(v["rest"], v["no_jpp"]) and torch.allclose(v["no_jpp"] + v["jpp"], v["whole"])
    assert torch.allclose(v["no_rand"], delta - rj)


@pytest.mark.parametrize(
    ("excess", "rest", "want"),
    [(0.10, 0.70, "outside"), (0.10 + 1e-6, 0.9, "between"), (0.05, 0.69, "between"), (0.30, 0.2, "through"),
     (0.29, 0.9, "between"), (-0.2, 1.0, "outside")],
)  # fmt: skip
def test_rule_labels_at_the_bars(excess, rest, want):
    assert LC.label(excess, rest) == want


def planted_rows(rates: dict[str, list[int]], layer: int = 8) -> list[dict]:
    n = len(rates["whole"])
    rows = [{"scene": f"s{i}", "entity": f"e{i % 5}", "reader": LK, "layer": None, "arm": "none", "switched": 0}
            for i in range(n)]  # fmt: skip
    for a, sw in rates.items():
        rows += [{"scene": f"s{i}", "entity": f"e{i % 5}", "reader": LK, "layer": layer, "arm": a, "switched": s}
                 for i, s in enumerate(sw)]  # fmt: skip
    return rows


def test_cell_numbers_recompute_the_excess_and_the_rest_share():
    n = 20
    whole = [1] * 16 + [0] * 4  # 0.80
    no_jpp = [1] * 14 + [0] * 6  # 0.70
    no_rand = [1] * 15 + [0] * 5  # 0.75
    jpp = [1] * 2 + [0] * 18
    c = LC.cell_numbers(planted_rows({"whole": whole, "no_jpp": no_jpp, "no_rand": no_rand, "jpp": jpp, "rest": no_jpp}),
                        LK, 8, n_boot=200)  # fmt: skip
    assert c["n"] == n and c["entities"] == 5
    assert c["excess"][0] == pytest.approx((0.75 - 0.70) / 0.80) and c["rest_share"][0] == pytest.approx(0.70 / 0.80)
    assert c["label"] == "outside" and c["rest_equals_no_jpp"] and not c["x0_valid"]  # 16 switches < 30
    assert c["rates"]["none"][0] == 0 and c["excess"][1] <= c["excess"][0] <= c["excess"][2]
    zero = LC.cell_numbers(planted_rows({a: [0] * n for a in LC.ARMS[1:]}), LK, 8, n_boot=50)
    assert zero["label"] == "untested" and np.isnan(zero["excess"][0])
    with pytest.raises(AssertionError, match="reads missing"):
        LC.cell_numbers(planted_rows({"whole": whole, "no_jpp": no_jpp}), LK, 8, n_boot=50)


def test_run_and_verdict_end_to_end_on_the_fake_model(tmp_path, monkeypatch):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins

    items = [_jitem(i) for i in range(12) if i % 2 == 0]  # the locker-first ones
    fake = JFake()
    setattr(fake, "decoded", [f"t{i}" for i in range(fake.unemb.shape[0])])  # noqa: B010 (Model.decoded: every id's text)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", JLensFake)
    monkeypatch.setattr(JR, "RESULTS", tmp_path / "x51_jread")
    monkeypatch.setattr(LC, "RESULTS", tmp_path / "x53_lastconflict")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(LC, "SPEC", tmp_path / "batch53.yaml")
    LC.SPEC.write_text("")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(LC, "select", lambda tok, t: (items, {"items_used": len(items)}))
    plant_51_10(JR.RESULTS, LC.SOURCE_RUNS[pins.TARGET], {"lookup": 8, "recall": 10}, {"lookup": 12, "recall": 12})
    src = X.RESULTS / G.SOURCES[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    (src / "gate.json").write_text(json.dumps({"gate": {"chat": {"pass": True, "enough": True}}}))
    out = LC.stage_run(LC.RUNS[pins.TARGET], "test")
    rows = X.read_jsonl(out / "outcomes.jsonl")
    want = {(it["scene"], LK, la, a) for it in items for la in (8, 10) for a in LC.ARMS[1:]}
    want |= {(it["scene"], RC, 10, a) for it in items for a in LC.ARMS[1:]}
    want |= {(it["scene"], w, None, "none") for it in items for w in (LK, RC)}
    assert {(r["scene"], r["reader"], r["layer"], r["arm"]) for r in rows} == want
    same = {(r["scene"], r["reader"], r["layer"]): r["top"] for r in rows if r["arm"] == "rest"}
    assert all(same[(r["scene"], r["reader"], r["layer"])] == r["top"] for r in rows if r["arm"] == "no_jpp")
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == len(items) * 3 and all(0 <= r["share_J"] <= 1 + 1e-6 for r in norms)
    m = json.loads((out / "manifest.json").read_text())
    assert m["question"] == LC.NO_PREDICTION and m["layers"]["readers"]["lookup"]["layers"] == [8, 10]
    v = LC.stage_verdict([out.name], n_boot=50)
    assert v.name.startswith("x53_lastconflict-") and v.parent == LC.RESULTS
    blob = json.loads((v / "verdict.json").read_text())
    assert [(c["reader"], c["layer"]) for c in blob["models"][0]["cells"]] == [
        ("lookup", 8),
        ("lookup", 10),
        ("recall", 10),
    ]
    md = (v / "verdict.md").read_text()
    assert "UNVERIFIED" in md and "no prediction" in md and (v / "x53_lastconflict.png").exists()
    assert (v / "examples.md").read_text().count("### ") == len(items)
