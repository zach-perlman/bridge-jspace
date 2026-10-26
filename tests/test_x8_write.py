"""Batch 44 (scripts/x8_write.py): slots, the answer classes, the filler variants, and both verdicts on planted rows."""

import json

from scripts import x8_write as W

ORG = ("The locker of the duck is 4. The locker of the frog is 3. The locker of the goose is 2. "
     "Beth picked the frog. Ann picked the duck. Tom picked the goose.")  # fmt: skip


def test_slots_and_classes():
    assert W.slots_of(ORG) == [("duck", 4), ("frog", 3), ("goose", 2)]
    tokens = {0: 40, 1: 30, 2: 20}
    assert W.classify(40, tokens, j=1, k=0) == "target"
    assert W.classify(30, tokens, j=1, k=0) == "original"
    assert W.classify(20, tokens, j=1, k=0) == "third"
    assert W.classify(99, tokens, j=1, k=0) == "other"
    assert W.classify(30, tokens, j=0, k=None) == "slot1"


def test_recall_item_by_legs():
    slots = [("duck", 4), ("rabbit", 3), ("goose", 2)]
    legs = {"duck": 2, "rabbit": 4, "goose": 2}
    assert W.recall_item("4", slots, legs, j=2, k=1) == "target"
    # the third slot's duck matches before the original goose (both 2 legs)
    assert W.recall_item("2", slots, legs, j=2, k=1) == "third"
    assert W.recall_item("6", slots, legs, j=2, k=1) == "other"


def test_filler_variants_move_index_or_distance():
    f = "The weather stayed mild and quiet for most of the afternoon."
    b1, b2 = W.with_filler(ORG, f, "before"), W.with_filler(ORG, f, "between")
    assert b1 == f + " " + ORG
    assert "The locker of the goose is 2. " + f + " Beth picked the frog." in b2
    assert W.slots_of(b1) == W.slots_of(b2) == W.slots_of(ORG)


def _write(tmp_path, monkeypatch, rows, manifest):
    monkeypatch.setattr(W, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps(manifest))
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return src


def test_write_verdict_reads_planted_targets(tmp_path, monkeypatch):
    rows = []
    for i in range(60):
        j = i % 3
        for k in (x for x in W.SLOTS if x != j):
            for kind, cls in (("write", "target"), ("random", "original")):
                base = {"scene": f"s{i}", "entity": f"e{i % 12}", "j": j, "k": k, "s": 1, "kind": kind}
                rows += [{**base, "reader": "PP", "class": cls}, {**base, "reader": "PM", "changed": 0}]
    _write(tmp_path, monkeypatch, rows, {"model": {"target": "fake"}, "layer": 12, "stage": "write", "items": 60})
    blob = json.loads((W.stage_verdict("fake", 200) / "verdict.json").read_text())
    q = blob["questions"]
    assert q["q44_1_pass"] and abs(q["q44_1_target_minus_random"][0] - 1.0) < 1e-9
    assert q["q44_2_moved"] == 120 and q["q44_2_specificity"] == 1.0 and q["q44_2_pass"]
    assert len(q["q44_3_per_pair"]) == 6 and q["q44_3_pass"]


def test_order_verdict_reads_a_distance_code(tmp_path, monkeypatch):
    rows = []
    for i in range(90):
        j = i % 3
        r = {"scene": f"s{i}", "entity": f"e{i % 15}", "j": j, "right": {"B0": 1, "B1": 1, "B2": 1},
             "B1": {"beta": 0.0, "norm_d": 0.1, "norm_step": 1.0}}  # fmt: skip
        if j >= 1:
            r["B2"] = {"beta": 1.0, "norm_d": 1.0, "norm_step": 1.0}
        rows.append(r)
    _write(tmp_path, monkeypatch, rows, {"model": {"target": "fake"}, "layer": 12})
    blob = json.loads((W.stage_order_verdict("fake", 200) / "verdict.json").read_text())
    assert blob["reading"] == "(c) distance"
    assert blob["variants"]["B2"]["n"] == 60 and not blob["variants"]["B1"]["shifted"]
