"""scripts/d5a_head_pointer.py: which statement a row's answer comes from, the read-out scores and the pre-registered
verdicts (no model)."""

from __future__ import annotations

import pytest

from scripts import d5a_head_pointer as D

ITEM = {"id": "x", "family": "RL", "digits": [9, 7, 6, 2, 3], "slots": {"query": 4, "identity": 3, "position": 2},
        "entities": ["Poland", "France", "Norway", "Venezuela", "Japan"]}  # fmt: skip


def test_answer_statement_lookup_and_recall():
    assert D.answer_statement(ITEM, "3", "none") == 4  # kept: the asked statement
    assert D.answer_statement(ITEM, "6", "position") == 2  # the statement holding the new digit
    assert D.answer_statement(ITEM, "2", "identity") == 3
    assert D.answer_statement(ITEM, "7", "context") == 1
    assert D.answer_statement(ITEM, "5", "value") is None  # not in the prompt
    rr = {**ITEM, "family": "RR"}
    assert D.answer_statement(rr, "4", "identity") == 3  # recall: the alt entity's statement (the bridge moved there)
    assert D.answer_statement(rr, "8", "none") == 4
    assert D.outcome_of(ITEM, "position") == "slot" and D.outcome_of(ITEM, "value") == "off the prompt"
    assert D.outcome_of(rr, "identity") == "word" and D.outcome_of(rr, "context") == "off the prompt"


def test_statement_tokens_follow_offsets():
    stmts = ["The Poland file is in drawer 9.", "Drawer 7 holds the France file."]
    text = "<user> " + " ".join(stmts) + " Which drawer?"
    offsets, i = [], 0
    for w in text.split(" "):  # one token per space-separated word
        offsets.append((i, i + len(w)))
        i += len(w) + 1
    toks = D.statement_tokens({"text": text, "offsets": offsets}, {"id": "x", "statements": stmts})
    assert [" ".join(text[offsets[t][0] : offsets[t][1]] for t in ts) for ts in toks][1] == stmts[1]
    assert toks[0][-1] < toks[1][0]


def _row(entity, domain, outcome, new, top, src="dissoc"):
    return {"entity": entity, "domain": domain, "outcome": outcome, "new_statement": new, "org_statement": 4,
            "heads": {"51:22": {"top": top}}, "lens": {"top": 4}, "source": src, "template": "0/0"}  # fmt: skip


def test_reader_scores_and_verdicts():
    rows = []
    for e in range(20):
        rows += [_row(f"e{e}", "animals" if e < 10 else "countries", "slot", 2, 2) for _ in range(3)]  # follows
        rows += [_row(f"e{e}", "animals" if e < 10 else "countries", "kept", 4, 4) for _ in range(3)]  # stays
    sc = D.reader_scores(rows, "51:22")
    assert sc["moved_new"]["share"] == 1.0 and sc["kept_org"]["share"] == 1.0 and sc["moved_org"]["share"] == 0.0
    assert sc["moved_new"]["k"] == 20 and sc["moved_new"]["n"] == 60
    v = D.verdicts(sc)
    assert v["follows"] and not v["static"] and v["verdict"] == "follows the pointer"
    static = [_row(r["entity"], r["domain"], r["outcome"], r["new_statement"], 4) for r in rows]
    vs = D.verdicts(D.reader_scores(static, "51:22"))
    assert vs["static"] and not vs["follows"]
    assert "not judged" in D.verdicts(D.reader_scores(rows[:12], "51:22"))["verdict"]
    pl = D.paired_vs_lens(rows, "51:22")  # the lens stays on statement 4: the head beats it on every moved row
    assert pl["diff"] == pytest.approx(1.0) and pl["head_better"]


def test_patch_layers_keep_depth():
    assert D.patch_layers(64) == [48, 50]
    assert D.patch_layers(24) == [18, 19]
