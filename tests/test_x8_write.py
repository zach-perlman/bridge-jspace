"""Batch 44 (scripts/x8_write.py): slots, the answer classes, the filler variants, and both verdicts on planted rows."""

import json

from scripts import x8_write as W

ORG = ("The locker of the duck is 4. The locker of the frog is 3. The locker of the goose is 2. "
     "Beth picked the frog. Ann picked the duck. Tom picked the goose.")  # fmt: skip


def _case_45c(i: int, j: int, k: int) -> dict:
    """A routes C2 case whose pointer moves from slot j (the O bridge's) to slot k (the S bridge's)."""
    items = ["duck", "frog", "goose"]
    o = " ".join(f"The locker of the {x} is {d}." for x, d in zip(items, (4, 3, 2), strict=True))
    s_items = list(items)
    s_items[k] = "rabbit"
    s = " ".join(f"The locker of the {x} is {d}." for x, d in zip(s_items, (4, 3, 2), strict=True))
    return {"scene": f"C2-{i}", "context": o, "cf_context": s, "bridge": items[j], "cf_bridge": "rabbit"}


def test_cells_45c_reads_only_the_second_third_moves():
    """45c's rule on planted rows: only the 1 -> 2 / 2 -> 1 moves count; removal leaves 0.25 of 1.0 (halves, CI > 0),
    keep-only gives 0.5 (>= 0.15)."""
    cases, rows = {}, []
    for i in range(80):
        j, k = ((1, 2), (2, 1), (0, 1), (1, 0))[i % 4]
        c = _case_45c(i, j, k)
        cases[c["scene"]] = c
        second_third = (j, k) in W.MOVES_12
        pos = {"whole": 1, "no_alf": int(i % 8 == 0), "no_alf_rand": 1, "keep_alf": int(i % 4 < 2), "keep_alf_rand": 0}
        for arm, p in pos.items():
            rows.append({"scene": c["scene"], "condition": "C2", "reader": "PP", "arm": arm, "entity": f"e{i % 10}",
                         "route": "position" if (p if second_third else 1) else "identity"})  # fmt: skip
    got = W.cells_45c(rows, cases, 300)
    assert got["n"] == 40
    assert got["position"]["whole"] == 1.0 and got["position"]["no_alf"] == 0.25
    assert got["halves"] and got["keep_015"] and got["found"]
    assert got["rand_cut"][0] == 0.0 and not got["rand_halves"]  # the random part keeps every position answer


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


def test_filler_lengths_leave_out_a_bos():
    """A tokenizer that prepends a BOS unless told not to (Muse): the filler's length is its words, not words + 1."""

    def tok(text, add_special_tokens=True):
        return {"input_ids": ([1] if add_special_tokens else []) + [7] * len(text.split())}

    n = W.filler_lengths(tok)
    assert all(n[f] == len(f.split()) for f in W.FILLERS)


def test_real_doses_read_the_latest_recall_stage(tmp_path, monkeypatch):
    """45c: a dose d writes s = d x the pair's s*; s* comes from the newest recall stage of the named x8 run."""
    monkeypatch.setattr(W, "RESULTS", tmp_path)
    for stamp, s12 in (("20261026T100000Z", 9.0), ("20261026T120000Z", 2.43)):
        (tmp_path / "run" / f"recall-{stamp}").mkdir(parents=True)
        (tmp_path / "run" / f"recall-{stamp}" / "recall.json").write_text(
            json.dumps({"s_real": {"0-1": 1.5, "1-2": s12}})
        )
    assert W.real_doses("run") == {"0-1": 1.5, "1-2": 2.43}


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
