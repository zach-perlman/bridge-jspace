from scripts import x52_write2x as W


def row(role: str, top: int, key: str = "k", reader: str = "PM", arm: str = "ans2") -> dict:
    return {"role": role, "top": top, "key": key, "reader": reader, "arm": arm}


def test_classify_puts_each_top_token_in_one_class():
    written, digits = {50, 51}, {1, 2, 3}
    assert W.classify(row("b", 2), written, digits) == "target"
    assert W.classify(row("A", 3), written, digits) == "original"
    assert W.classify(row("other", 51), written, digits) == "written"
    assert W.classify(row("other", 1), written, digits) == "digit"
    assert W.classify(row("other", 99), written, digits) == "other"


def test_summarise_shares_sum_to_one_and_use_each_items_own_written_tokens():
    rows = [row("b", 2, "a"), row("other", 50, "a"), row("other", 50, "b"), row("other", 7, "b")]
    norms = {("a", "PM"): [50], ("b", "PM"): [60]}  # token 50 is written for item a only
    s = W.summarise(rows, norms, {1, 2, 3}, str)["PM|ans2"]
    assert s["n"] == 4
    assert s["share"] == {"target": 0.25, "original": 0.0, "written": 0.25, "digit": 0.0, "other": 0.5}
    assert sum(s["share"].values()) == 1.0
    assert dict(s["top"]["other"]) == {"50": 1, "7": 1}
