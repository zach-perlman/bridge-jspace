"""Batch 47 amendment 3, D4 (scripts/x47_depth_cpu.py): principal angles and the persistence rule on planted bases, the
embedding overlap rule on planted norms, the person probe on planted locker states, the alignment table with pending
cells, the stages on the fake 47.8 run (tests/test_x47_anatomy.py's fixture) and the seal. CPU, no real model."""

import json
import random

import numpy as np
import pytest
from test_x47_anatomy import fake_run  # noqa: F401  (the fake 47.8 run: its cache and fit record)

from scripts import x47_anatomy as A
from scripts import x47_depth_cpu as D


def basis(d: int, r: int, seed: int) -> np.ndarray:
    q, _ = np.linalg.qr(np.random.default_rng(seed).standard_normal((d, r)))
    return q


def rotate(b: np.ndarray, angle: float, seed: int) -> np.ndarray:
    """b's columns each tilted by `angle` toward a fresh direction orthogonal to b."""
    d, r = b.shape
    g = np.random.default_rng(seed).standard_normal((d, r))
    g -= b @ (b.T @ g)
    g, _ = np.linalg.qr(g)
    return np.cos(angle) * b + np.sin(angle) * g


def fit_with_probe(layers, slot: dict, ident: dict | None = None) -> dict:
    return {"per_layer": {str(la): {"probes": {"locker sentence": {"probe": [slot.get(la, 0.0), 0, 1]},
                                               "bridge identity": {"probe": [(ident or slot).get(la, 0.0), 0, 1]}}}
                          for la in layers}}  # fmt: skip


# ---- (1) persistence ------------------------------------------------------------------------------------------------


def test_mean_cos2_of_principal_angles():
    b = basis(40, 3, 0)
    assert D.mean_cos2(b, b) == pytest.approx(1.0)
    assert D.mean_cos2(b, rotate(b, np.pi / 2, 1)) == pytest.approx(0.0, abs=1e-9)
    assert D.mean_cos2(b, rotate(b, np.pi / 4, 2)) == pytest.approx(0.5)
    assert D.mean_cos2(b, b[:, :1]) == pytest.approx(1.0)  # a sub-basis: the min rank normalises
    assert D.mean_cos2(b, b[:, :0]) == 0.0


def test_persistence_rule_on_planted_bases():
    layers = [2, 4, 6, 8, 10]
    b = basis(40, 2, 3)
    same = {f"U_L{la}": b for la in layers}
    same.update({f"Id_L{la}": basis(40, 5, 4) for la in layers})
    fit = fit_with_probe(layers, {4: 0.9, 6: 0.9, 8: 0.9, 10: 0.9})
    p = D.persistence_of(same, fit, layers)
    assert (
        p["U"]["label"] == "persistent"
        and p["U"]["window"] == [4, 6, 8, 10]
        and p["U"]["mean_cos2"] == pytest.approx(1.0)
    )
    assert p["Id"]["label"] == "persistent" and p["U"]["matrix"][0][4] == pytest.approx(1.0)
    # re-encoded: every sampled layer carries a fresh, orthogonal code
    fresh = {f"U_L{la}": basis(40, 2, 10 + la) for la in layers}
    fresh.update({f"Id_L{la}": basis(40, 5, 20 + la) for la in layers})
    p = D.persistence_of(fresh, fit, layers)
    assert p["U"]["label"] == "re-encoded" and p["U"]["drops"] and p["U"]["mean_cos2"] < 0.2
    # a slow drift: adjacent layers close (cos^2 ~ 0.75), far layers apart; the mean over all pairs decides
    drift, cur = {}, b
    for la in layers:
        drift[f"U_L{la}"] = cur
        drift[f"Id_L{la}"] = cur
        cur = rotate(cur, np.pi / 6, 100 + la)
    p = D.persistence_of(drift, fit, layers)
    assert p["U"]["label"] in ("persistent", "mixed") and not p["U"]["drops"]
    # a window of one layer is not tested
    p = D.persistence_of(same, fit_with_probe(layers, {10: 0.9}), layers)
    assert p["U"]["label"] == "not tested"


def test_persistence_label_mixed_when_both_clauses_hold():
    window = [2, 4, 6]
    cos2 = {(2, 4): 0.1, (4, 6): 0.9, (2, 6): 0.9}
    cos2.update({(b, a): v for (a, b), v in list(cos2.items())})
    r = D.persistence_label(cos2, window)
    assert r["label"] == "mixed" and r["drops"] == ["2-4"] and r["mean_cos2"] == pytest.approx(0.6333, abs=1e-3)


# ---- (2) the embedding overlap ---------------------------------------------------------------------------------------


def test_embedding_layer_below_and_l_j():
    layers = [2, 4, 6, 8]
    norms = []
    for la, (we, jw) in zip(layers, ((0.9, 0.8), (0.5, 0.3), (0.15, 0.25), (0.1, 0.1)), strict=True):
        for i in range(5):
            norms.append(
                {"layer": la, "WE_inside_J": we + 0.01 * i, "J_inside_WE": jw, "share_WE": 0.3, "share_J": 0.2}
            )
    e = D.embedding_of(norms, layers, l_j=4)
    assert e["layer_below"] == 8 and e["vs_l_J"] == 4 and e["per_layer"]["6"]["overlap"] == pytest.approx(0.25)
    assert "L8" in e["reading"] and "+4" in e["reading"]
    e = D.embedding_of(norms[:10], [2, 4], None)
    assert e["layer_below"] is None and e["vs_l_J"] is None


# ---- (3) the person probe ----------------------------------------------------------------------------------------


def test_person_probe_reads_a_planted_binding():
    rng = np.random.default_rng(0)
    people = ["Iris", "Noah", "Mia"]
    codes = rng.standard_normal((3, 24))
    items, x = [], []
    for i in range(90):
        p = i % 3
        items.append({"scene": f"s{i}", "entity": f"item{i % 15}", "person": people[p]})
        x.append(3 * codes[p] + rng.standard_normal(24) * 0.5)
    r = D.person_probe(np.stack(x), items, n_boot=50)
    assert r["probe"][0] > 0.9 and r["chance"] == pytest.approx(1 / 3, abs=1e-3) and r["classes"] == 3
    # no binding in the states: at chance
    r = D.person_probe(rng.standard_normal((90, 24)), items, n_boot=50)
    assert r["probe"][0] < 0.6


def test_person_labels_follow_the_picks():
    c = {"context": "The locker of the frog is 5. The locker of the bee is 3. The locker of the tick is 2. Noah picked the tick. "
                    "Iris picked the frog. Peter picked the bee."}  # fmt: skip
    assert D.person_labels([c]) == [["Iris", "Peter", "Noah"]]
    assert D.slot_item(c, 2) == "tick"


# ---- (4) the table --------------------------------------------------------------------------------------------------


def test_table_rows_with_pending_cells():
    verdict = {"models": [{"target": "qwen3.5-9b", "status": "tested", "rules": {"l_probe": 6, "l_P": 10, "l_J": 8}},
                          {"target": "qwen3.6-27b", "status": "pending"}]}  # fmt: skip
    d4 = {
        "qwen3.5-9b": {
            "persistence": {"U": {"label": "persistent"}, "Id": {"label": "mixed"}},
            "embedding": {"layer_below": 6},
        }
    }
    rows = D.table_rows(verdict, {"qwen3.5-9b": {"lookup": 20, "recall": 24}}, d4)
    by = {r["model"]: r for r in rows}
    assert set(by) == set(A.RUNS)
    r = by["qwen3.5-9b"]
    assert (r["l_probe"], r["l_P"], r["l_J"], r["l_R_lookup"], r["l_R_recall"]) == (6, 10, 8, 20, 24)
    assert (
        r["mid_band"] == "L12-16"
        and r["late_band"] == "L26-29"
        and r["address"] == "persistent"
        and r["embedding_below"] == 6
    )
    assert by["qwen3.6-27b"]["l_J"] == "pending" and by["muse-glimmer-30b"]["address"] == "pending"
    lines = D.table_lines(rows)
    assert len(lines) == 2 + len(A.RUNS) and "L52-60" in lines[3]


def test_bands_match_the_breadth_readme():
    from bridge_jspace import pins

    text = (pins.REPO_ROOT / "docs" / "breadth" / "README.md").read_text()
    assert "27B (L52-60" in text and "9B (L26-29" in text and "Muse (L36-42)" in text
    assert "Qwen3.6-27B (L32-40)" in text and "Qwen3.5-9B (L12-16)" in text


# ---- the stages on the fake 47.8 run and the seal ---------------------------------------------------------------------


def test_stages_on_the_fake_run(fake_run, monkeypatch, tmp_path):  # noqa: F811
    monkeypatch.setattr(A, "dan_answer", lambda *a, **k: "persistent")
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x47_depth_cpu")
    run = fake_run.out.name
    out = D.stage_persistence([run])
    p = json.loads((out / "persistence.json").read_text())["models"][fake_run.target]
    assert p["layers"] == [2, 6, 10] and p["U"]["label"] in ("persistent", "re-encoded", "mixed", "not tested")
    assert len(p["U"]["matrix"]) == 3 and p["U"]["matrix"][1][1] == pytest.approx(1.0)
    out = D.stage_embedding([run], None)
    e = json.loads((out / "embedding.json").read_text())["models"][fake_run.target]
    assert set(e["per_layer"]) == {"2", "6", "10"} and e["l_J"] is None
    out = D.stage_binding([run], n_boot=20)
    b = json.loads((out / "binding.json").read_text())["models"][fake_run.target]
    assert b["layers"] == [2, 10] and b["n_cases"] == 5 and set(b["2"]) == set(D.TOKEN_KINDS)
    assert b["2"]["item"]["n"] == 15 and b["2"]["item"]["classes"] in (3, 4)  # the fake pool draws 2 of 3 other people
    out = D.stage_table([run], None, None, n_boot=20)
    rows = json.loads((out / "table.json").read_text())["rows"]
    mine = next(r for r in rows if r["model"] == fake_run.target)
    assert mine["l_J"] == "pending" and mine["address"] == p["U"]["label"]


def test_d4_sealed_until_dans_answer(monkeypatch, tmp_path):
    monkeypatch.setattr(A, "dan_answer", lambda *a, **k: "")
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    for stage in (
        lambda: D.stage_persistence([]),
        lambda: D.stage_embedding([], None),
        lambda: D.stage_binding([], 10),
        lambda: D.stage_table([], None, None, 10),
    ):
        with pytest.raises(AssertionError, match="sealed"):
            stage()


def test_dan_answer_for_q_depth_reads_its_own_block(monkeypatch):
    from types import SimpleNamespace

    text = "**Q47.8** ...\n\nDan: a\n\n**Q-depth** (amendment 3)\n- D4: ...\n\nDan:{}\n\n## Batch 48\n\n**Q48.1** ...\n\nDan: b\n"
    monkeypatch.setattr(A.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=text.format("")))
    assert A.dan_answer(question=D.QUESTION) == ""
    monkeypatch.setattr(A.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=text.format(" persistent 60%")))
    assert A.dan_answer(question=D.QUESTION) == "persistent 60%"


def test_random_seed_independence_of_rotate_helper():
    b = basis(10, 2, 0)
    r = rotate(b, 0.3, 5)
    assert np.allclose(r.T @ r, np.eye(2), atol=1e-8)  # the tilted basis stays orthonormal
    assert random.Random(0).random() == random.Random(0).random()
