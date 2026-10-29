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


def test_ans13_mode_is_the_lookup_alone_at_answer_minus_1_and_3(tmp_path, monkeypatch):
    from bridge_jspace import pins

    monkeypatch.setattr(JR, "RESULTS", tmp_path / "x51_jread")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    plant_51_10(JR.RESULTS, LC.SOURCE_RUNS[pins.TARGET], {"lookup": 24, "recall": 27}, {"lookup": 29, "recall": 29})
    lay = LC.layers_of(pins.TARGET, "ans13")
    assert list(lay["readers"]) == ["lookup"] and lay["readers"]["lookup"]["layers"] == [28, 26]


def test_word_layers_and_the_rule_across_readers():
    assert LC.word_layers(20, 12, list(range(31))) == ([19, 18, 17, 12], [])
    assert LC.word_layers(31, 24, list(range(31))) == ([30, 29, 28, 24], [])
    assert LC.word_layers(32, 24, list(range(31))) == ([30, 29, 24], [31])
    assert LC.word_layers(None, 24, list(range(31))) == ([24], [])

    def model(target: str, lk: str, rc: str, valid: bool = True) -> dict:
        cells = [{"reader": w, "layer": 20 - o, "label": lab, "x0_valid": valid}
                 for w, lab in (("lookup", lk), ("recall", rc)) for o in (1, 2, 3)]  # fmt: skip
        return {
            "target": target,
            "cells": cells,
            "layers": {"readers": {"lookup": {"answer": 20}, "recall": {"answer": 20}}},
        }

    copy = [model(f"m{i}", "outside", "through") for i in range(3)]
    assert LC.across_readers(copy)["label"] == "copy bypasses the lens"
    assert LC.across_readers(copy[:2])["label"] == "pending (2 of 4 models)"
    digits = [model(f"m{i}", "through", "through") for i in range(4)]
    assert LC.across_readers(digits)["label"] == "digits only"
    mixed = [*copy[:2], *(model(f"d{i}", "through", "through") for i in range(2))]
    assert LC.across_readers(mixed)["label"] == "in between"
    invalid = [model(f"m{i}", "outside", "through", valid=False) for i in range(4)]
    assert LC.across_readers(invalid)["label"] == "in between" and not LC.across_readers(invalid)["copy_models"]


def plant_z1p(root, run: str, n: int, data_dir) -> list[dict]:
    """A planted Z1-P run: n passages (the order alternates the two sets; only jsuite_v2_test_chat's are read) and the
    v2.1 item ids."""
    items, ids = [], []
    for i in range(n):
        st = "jsuite_v2_test_chat" if i % 3 else "jsuite_v2nb_test_chat"
        readers = {}
        for s, q in (("K", "Which word?"), ("M", "Which word, recalled?")):
            org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6, 7, 8 + (s == "M")]
            alt = [*org[:4], 40 + i % 5, *org[5:]]
            rid = f"j2:chat:facts:P{'P' if s == 'K' else 'M'}-L0-{i:05d}"
            ids.append(rid)
            readers[s] = {"id": rid, "question": q, "answer": "x", "cf_answer": "y", "context": "a passage",
                          "ids": {"org": org, "alt": alt}, "tok_A": 5, "tok_b": 3, "pos": 4}  # fmt: skip
        items.append({"set": st, "scene": f"P-L0-{i}", "bridge": f"e{i % 5}", "cf_bridge": f"f{i % 5}",
                      "relation": "animals", "readers": readers})  # fmt: skip
    (root / run).mkdir(parents=True)
    X.write_jsonl(root / run / "cases.jsonl", items)
    gate = {"org_read_accuracy": {"K": 0.9, "M": 0.9}, "pass": True, "eligible": n, "chosen": n,
            "order": [[c["set"], c["scene"]] for c in items]}  # fmt: skip
    (root / run / "gate.json").write_text(json.dumps(gate))
    (data_dir / "tasks_v2" / "jsuite_v2_1_test_chat").mkdir(parents=True)
    X.write_jsonl(data_dir / "tasks_v2" / "jsuite_v2_1_test_chat" / "items.jsonl", [{"id": r} for r in ids])
    return [c for c in items if c["set"] == "jsuite_v2_test_chat"]


def test_words_run_and_verdict_end_to_end_on_the_fake_model(tmp_path, monkeypatch):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x50_zach as Z

    fake = JFake()
    setattr(fake, "decoded", [f"t{i}" for i in range(fake.unemb.shape[0])])  # noqa: B010
    setattr(fake, "special_ids", frozenset())  # noqa: B010
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", JLensFake)
    monkeypatch.setattr(JR, "RESULTS", tmp_path / "x51_jread")
    monkeypatch.setattr(LC, "RESULTS", tmp_path / "x53_lastconflict")
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x50_zach")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pins, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(LC, "SPEC", tmp_path / "batch53.yaml")
    LC.SPEC.write_text("")
    monkeypatch.setattr(JR, "settle_layer", lambda tops, tok: 12)  # every passage settles at L12: answer layer 12
    monkeypatch.setitem(LC.WORD_SOURCE, pins.TARGET, "fake_z1p")
    plant_51_10(JR.RESULTS, LC.SOURCE_RUNS[pins.TARGET], {"lookup": 8, "recall": 10}, {"lookup": 30, "recall": 30})
    used = plant_z1p(Z.RESULTS, "fake_z1p", 15, pins.DATA_DIR)
    out = LC.stage_run_words(LC.WORD_RUNS[pins.TARGET], "test")
    m = json.loads((out / "manifest.json").read_text())
    assert m["layers"]["readers"]["lookup"]["layers"] == [11, 10, 9, 8] and m["layers"]["readers"]["recall"][
        "layers"
    ] == [11, 10, 9]
    assert m["arm_names"] == list(LC.ARMS_WORDS) and m["below_gate"] is None
    rows = X.read_jsonl(out / "outcomes.jsonl")
    keys = {(r["scene"], r["reader"], r["layer"], r["arm"]) for r in rows}
    want = {(f"{c['set']}:{c['scene']}", LK, la, a) for c in used for la in (11, 10, 9, 8) for a in LC.ARMS_WORDS[1:]}
    want |= {(f"{c['set']}:{c['scene']}", RC, la, a) for c in used for la in (11, 10, 9) for a in LC.ARMS_WORDS[1:]}
    want |= {(f"{c['set']}:{c['scene']}", w, None, "none") for c in used for w in (LK, RC)}
    assert keys == want
    v = LC.stage_verdict_words([out.name], [], n_boot=50)
    assert v.name.startswith("x53_lastconflict_words-") and v.parent == LC.RESULTS
    blob = json.loads((v / "verdict.json").read_text())
    assert blob["across"]["label"].startswith(("pending", "in between", "copy", "digits"))
    assert {(c["reader"], c["layer"]) for c in blob["models"][0]["cells"]} == {
        ("lookup", la) for la in (11, 10, 9, 8)
    } | {("recall", la) for la in (11, 10, 9)}
    md = (v / "verdict.md").read_text()
    assert "53.3b" in md and "UNVERIFIED" in md and (v / "x53_lastconflict_words.png").exists()
    assert (v / "examples.md").read_text().count("### jsuite_v2_test_chat:") == len(used)


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
