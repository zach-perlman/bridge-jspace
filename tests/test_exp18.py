"""exp18_brew_verbalizers: scoring and the verdict (no model)."""

import torch

from scripts.exp18_brew_verbalizers.experiment import ROLES, score, summarize

ROW = {"roles": {"A": "blue", "b": "green", "c": "purple", "X": "teal", "I": "brown", "S": "gold"}, "null": "red"}
P = {"n_boot": 200, "boot_seed": 0}


def test_score_names_each_role_colour():
    r = score(("i0", "patched", "last", 42, torch.zeros(2)), "- the potion is teal now, not brown", ROW)
    assert r["reader"] == "nla" and r["names_X"] and r["names_I"] and not r["names_A"] and not r["names_null"]


def reads_for(n: int, patched_text: str) -> tuple[list[dict], list[dict]]:
    texts = {"clean": "brown", "cf": "teal", "patched": patched_text, "off_patched": "brown"}
    reads, rows = [], []
    for i in range(n):
        rows.append({"name": f"i{i}", "took": True})
        for condition, text in texts.items():
            reads.append(score((f"i{i}", condition, "last", 42, torch.zeros(2)), text, ROW))
    return reads, rows


def test_verdicts():
    assert set(ROLES) >= {"I", "X"}
    reads, rows = reads_for(20, "teal")
    assert summarize(reads, rows, P)["readers"]["nla"]["verdict"] == "reads the state"
    reads, rows = reads_for(20, "brown")
    assert summarize(reads, rows, P)["readers"]["nla"]["verdict"] == "solves from the text"
