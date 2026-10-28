"""Batch 47, test 47.13 (scripts/x47_errors.py), on planted rows (CPU, no model): the wrong answer's slot per format,
the probe on the wrong items with the entity held out (a planted signal is found, a too-small group gets no probe), the
rates and the rule (bars inclusive, not tested below N_MIN, pending without the lens), the verdict on planted folders,
and the seal until Dan's Q47.13 answer."""

import json
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x47_errors as E

PROSE = {"id": "PP-L0-0001", "scene": "P2-L0-0001", "format": "prose", "domain": "greek", "bridge": "eta",
         "context": "Victor picked beta. The locker of gamma is six. The locker of eta is three. The locker of beta is "
                    "five. Eva picked gamma. Henry picked eta.",
         "facts": {"person": "Henry", "x": "eta", "pick": {"Eva": "gamma", "Henry": "eta", "Victor": "beta"},
                   "locker": {"gamma": 6, "eta": 3, "beta": 5}, "lookalike_picks": []}}  # fmt: skip
TABLE = {"id": "PP-L0-0002", "scene": "P2-L0-0002", "format": "table", "domain": "greek", "bridge": "theta",
         "context": "Table lockers:\n| item | locker |\n|---|---|\n| gamma | eight |\n| theta | two |\n| beta | seven |"
                    "\n\nTable picks:\n| name | pick |\n|---|---|\n| Sean | gamma |\n| Finn | theta |\n| Mia | beta |",
         "facts": {"person": "Finn", "x": "theta", "pick": {"Sean": "gamma", "Finn": "theta", "Mia": "beta"},
                   "locker": {"gamma": 8, "theta": 2, "beta": 7}, "lookalike_picks": []}}  # fmt: skip


def test_slot_of_the_answered_digit_per_format():
    assert E.locker_ordinals(PROSE) == {"gamma": 0, "eta": 1, "beta": 2}
    assert E.locker_ordinals(TABLE) == {"gamma": 0, "theta": 1, "beta": 2}
    assert (E.slot_of(PROSE, "6"), E.slot_of(PROSE, "3"), E.slot_of(PROSE, "5")) == (0, 1, 2)
    assert (E.slot_of(TABLE, "8"), E.slot_of(TABLE, "7")) == (0, 2)
    assert E.slot_of(PROSE, "7") is None and E.slot_of(PROSE, None) is None and E.slot_of(PROSE, "x") is None
    twice = {**PROSE, "facts": {**PROSE["facts"], "locker": {"gamma": 5, "eta": 3, "beta": 5}}}
    assert E.slot_of(twice, "5") is None  # two statements state it


def test_item_rows_drop_said_right_read_wrong_and_keep_the_wrong_slot():
    case = {**PROSE, "rendering": "chat", "order": "before", "level": 0, "numbers": "words",
            "readers": {X.LOOKUP: {"answer": "3"}}}  # fmt: skip
    reads = {"P2-L0-0001": {"said": "6", "right": False, "read_right": False}}
    (row,) = E.item_rows([case], reads)
    assert row["locker_index"] == 1 and row["wrong_slot"] == 0 and not row["right"] and row["n_lockers"] == 3
    reads = {"P2-L0-0001": {"said": "3", "right": True, "read_right": False}}
    assert E.item_rows([case], reads) == []


def planted(n_ent=20, per=8, d=24, n_wrong=12, seed=0):
    """Right scenes whose state carries their gold slot (0-2) as a planted direction; wrong scenes whose state carries
    the wrong answer's slot instead; one tiny json group with no probe."""
    rng = np.random.default_rng(seed)
    items, rows = [], []
    for e in range(n_ent):
        for j in range(per):
            slot = int(rng.integers(0, 3))
            wrong = len([i for i in items if not i["right"]]) < n_wrong and j == 0
            wrong_slot = (slot + 1) % 3 if wrong else None
            items.append({"scene": f"s{e}-{j}", "entity": f"e{e}", "format": "prose", "order": "before", "right": not wrong,
                          "locker_index": slot, "pick_index": 3, "layout": "3/3", "wrong_slot": wrong_slot,
                          "n_lockers": 3})  # fmt: skip
            x = rng.normal(size=d)
            x[wrong_slot if wrong else slot] += 4.0
            rows.append(x)
    for k in range(3):  # a json group too small for a probe: 2 right scenes, 1 wrong
        items.append({"scene": f"j{k}", "entity": f"e{k}", "format": "json", "order": "before", "right": k < 2,
                      "locker_index": k % 3, "pick_index": 3, "layout": "3/3", "wrong_slot": None if k < 2 else 1,
                      "n_lockers": 3})  # fmt: skip
        rows.append(rng.normal(size=d))
    return np.array(rows), items


def test_probe_finds_the_planted_wrong_slot_with_the_entity_held_out():
    h, items = planted()
    preds, groups = E.predict_wrong(h, items)
    by = {p["scene"]: p for p in preds}
    wrong = [it for it in items if not it["right"] and it["format"] == "prose"]
    hits = [by[it["scene"]]["probe_slot"] == it["wrong_slot"] for it in wrong]
    assert len(wrong) == 12 and np.mean(hits) >= 0.9
    assert all(by[it["scene"]]["majority_slot"] in (0, 1, 2) for it in wrong)
    g = {(x["format"], x["order"]): x for x in groups}
    assert g[("prose", "before")]["probe"] and g[("prose", "before")]["cv_accuracy_right"] > 0.9
    assert not g[("json", "before")]["probe"] and by["j2"]["probe_slot"] is None and by["j2"]["majority_slot"] == 0


def wrong_rows(n: int, matched: int, with_slot: int | None = None):
    rows = []
    for i in range(n):
        slot = 0 if (with_slot is None or i < with_slot) else None
        rows.append({"scene": f"s{i}", "entity": f"e{i % 7}", "format": "prose", "order": "before", "n_lockers": 3,
                     "locker_index": 2, "wrong_slot": slot, "probe_slot": 0 if i < matched else 1, "majority_slot": 1,
                     "layout_slot": 1, "structure_slot": 1})  # fmt: skip
    return rows


def lens_for(rows, right: int) -> dict:
    return {r["scene"]: {"top": "x", "top_is_bridge": i < right} for i, r in enumerate(rows)}


def test_rates_and_rule_bars_are_inclusive():
    rows = wrong_rows(30, 15)
    r = E.rates(rows, lens_for(rows, 12), n_boot=50)  # 12 of the 15 matched items: 0.8 exactly
    assert r["n"] == 30 and r["match"]["probe"][0] == pytest.approx(0.5) and r["match"]["majority"][0] == 0.0
    assert r["n_matched"] == 15 and r["lens"]["right_matched"][0] == pytest.approx(0.8)
    assert r["lens"]["right_all"][0] == pytest.approx(12 / 30) and r["probe_gold"][0] == 0.0
    assert E.rule(r) == {"status": "scored", "holds": True, "match_holds": True, "lens_holds": True}
    r = E.rates(rows, lens_for(rows, 11), n_boot=50)
    assert E.rule(r)["holds"] is False and E.rule(r)["lens_holds"] is False
    r = E.rates(wrong_rows(30, 14), lens_for(rows, 30), n_boot=50)
    assert E.rule(r)["holds"] is False and E.rule(r)["match_holds"] is False


def test_no_slot_counts_as_no_match_and_the_with_slot_rate_is_beside():
    rows = wrong_rows(40, 20, with_slot=20)  # the 20 matched ones have a slot; 20 wrong answers no statement states
    r = E.rates(rows, None, n_boot=50)
    assert r["n_slot"] == 20 and r["match"]["probe"][0] == pytest.approx(0.5)
    assert r["match_with_slot"]["probe"][0] == pytest.approx(1.0)
    assert r["lens"] is None and E.rule(r)["status"] == "pending"


def test_fewer_than_n_min_wrong_items_is_not_tested():
    rows = wrong_rows(29, 29)
    assert E.rule(E.rates(rows, lens_for(rows, 29), n_boot=50))["status"] == "not tested"
    assert E.rule(E.rates([], None, n_boot=50))["status"] == "not tested"


def write_planted(root, run: str, target: str, n: int, matched: int, lens_right: int | None):
    count = root / f"{run}-20261028T000000Z"
    count.mkdir(parents=True)
    rows = wrong_rows(n, matched)
    (count / "manifest.json").write_text(json.dumps({"model": {"target": target}, "source": {"run": "x", "layer": 1}}))
    (count / "plan.json").write_text(json.dumps({"wrong": n}))
    (count / "groups.json").write_text(json.dumps([{"format": "prose", "order": "before", "right_scenes": 50,
                                                    "entities": 7, "wrong_items": n, "probe": True, "penalty": 1.0,
                                                    "cv_accuracy_right": 0.9, "majority_share": 0.4}]))  # fmt: skip
    X.write_jsonl(count / "rows.jsonl", rows)
    if lens_right is not None:
        gpu = root / f"{run}-gpu-20261028T000001Z"
        gpu.mkdir()
        X.write_jsonl(
            gpu / "lens.jsonl", [{"source": "x0b", "scene": s, **v} for s, v in lens_for(rows, lens_right).items()]
        )


def test_verdict_on_planted_folders(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "yes · 60%")
    write_planted(tmp_path, "r9", "qwen3.5-9b", 40, 24, 22)
    write_planted(tmp_path, "r27", "qwen3.6-27b", 5, 5, None)
    out = E.stage_verdict(["r9", "r27"], n_boot=50)
    blob = json.loads((out / "x47_errors.json").read_text())
    assert blob["dan"] == "yes · 60%" and out.parent == tmp_path
    m9, m27 = blob["models"]
    assert m9["rule"] == {"status": "scored", "holds": True, "match_holds": True, "lens_holds": True}
    assert m9["rates"]["match"]["probe"][0] == pytest.approx(0.6) and m9["rates"]["lens"]["right_matched"][
        0
    ] == pytest.approx(22 / 24)
    assert m27["rule"]["status"] == "not tested" and m27["gpu"] is None
    md = (out / "x47_errors.md").read_text()
    assert "Dan: yes · 60%" in md and "| qwen3.5-9b | r9 | scored |" in md and "not tested" in md


def test_verdict_is_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "")
    write_planted(tmp_path, "r9", "qwen3.5-9b", 40, 24, 22)
    with pytest.raises(AssertionError, match="sealed"):
        E.stage_verdict(["r9"], n_boot=10)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r9-20261028T000000Z", "r9-gpu-20261028T000001Z"]


def test_dan_answer_reads_only_the_q47_13_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.12** (47.12) ...\n\nDan: yes · 60%\n\n**Q47.13** (47.13, CPU) ...\n\nRule: ...\n\nDan:{}\n\n**Q47.7, addition** x\n\nDan: z\n"
    monkeypatch.setattr(E.subprocess, "run", fake_git(blocks.format("")))
    assert E.dan_answer() == ""
    monkeypatch.setattr(E.subprocess, "run", fake_git(blocks.format(" no · 65%")))
    assert E.dan_answer() == "no · 65%"


def test_the_committed_predictions_file_has_the_q47_13_block():
    text = E.subprocess.run(["git", "show", f"HEAD:{E.PREDICTIONS}"], cwd=E.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{E.QUESTION}**" in text and isinstance(E.dan_answer(), str)
