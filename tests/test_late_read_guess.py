"""scripts/late_read_guess.py on synthetic rows: answer classes, arm choice, the rates and chances, the grid gate."""

import pytest

from scripts import late_read_guess as G

DECODE = {100 + d: str(d) for d in range(10)} | {1: " none", 2: "\n", 3: "10", 4: " 7"}
NAMES = ("camel", "mouse", "worm", "eagle", "rabbit")


def tok(d: str) -> int:
    return 100 + int(d)


def case(i: int, digits: list[str], q: int, family: str = "RL") -> dict:
    """Five sentences, one token each (its offsets span the whole sentence); sentence q is asked."""
    sents = [f"The {NAMES[k]}'s locker is {d}." for k, d in enumerate(digits)]
    prompt, offsets = "", []
    for s in sents:
        offsets.append([len(prompt), len(prompt) + len(s)])
        prompt += s + " "
    return {"id": f"c{i}", "family": family, "answer": digits[q], "query_slot": q, "prompt": prompt,
            "conf_answers": sorted(d for k, d in enumerate(digits) if k != q), "offsets": offsets,
            "statements": [[k] for k in range(len(digits))]}  # fmt: skip


def row(c: dict, top: int, source: str = "none", dest: str = "-", layers: str = "-", mode: str = "-") -> dict:
    return {"family": c["family"], "id": c["id"], "source": source, "dest": dest, "layers": layers, "mode": mode,
            "top": top, "correct": top == tok(c["answer"])}  # fmt: skip


def test_classify():
    vis = {"1", "3", "5", "8"}
    assert G.classify("9", "9", vis) == "hidden"
    assert G.classify(" 9 ", "9", vis) == "hidden"  # whitespace stripped
    assert G.classify("3", "9", vis) == "visible"
    assert G.classify("0", "9", vis) == "outside"
    assert G.classify("6", "9", vis) == "outside"
    assert G.classify("10", "9", vis) == "non-digit"
    assert G.classify(" none", "9", vis) == "non-digit"
    assert G.classify("\n", "9", vis) == "non-digit"


def test_slot_digits_and_validation():
    c = case(0, ["5", "3", "1", "9", "8"], 3)
    assert G.slot_digits(c) == ["5", "3", "1", "9", "8"]
    bad = c | {"answer": "4"}
    assert G.slot_digits(bad) is None
    two = c | {"prompt": c["prompt"].replace("camel's", "camel7's")}  # same length: the offsets still hold
    assert G.slot_digits(two) is None  # a sentence with two digits


def test_arms_hybrid_and_full_attention():
    c = case(0, ["5", "3", "1", "9", "8"], 3)
    full = [row(c, 109), row(c, 109, "lookup", "final", "all", "value"), row(c, 109, "lookup", "after", "all", "value")]
    assert [(a, lab) for a, lab, _ in G.arms(full)] == [
        ("unedited", ("none", "-", "-")), ("last tokens", ("lookup", "final", "all")), ("after", ("lookup", "after", "all"))]  # fmt: skip
    hybrid = [*full, row(c, 109, "lookup", "final", "attn", "value")]
    got = {a: lab for a, lab, _ in G.arms(hybrid)}
    assert got["last tokens"] == ("lookup", "final", "attn")
    assert got["last tokens, all layers"] == ("lookup", "final", "all")
    assert got["after"] == ("lookup", "after", "all")


def scene() -> tuple[list[dict], list[dict]]:
    """Ten items, digits 1-9, four visible each; item 9 wrong unedited (out of the blocked arms)."""
    cases = [case(i, ["5", "3", "1", "9", "8"], i % 5) for i in range(10)]
    rows = [row(c, tok(c["answer"]) if i < 9 else tok(c["conf_answers"][0])) for i, c in enumerate(cases)]
    # last tokens: 6 visible, 1 right, 1 outside (0), 1 non-digit; the wrong-unedited item answers right (dropped)
    last = ["v", "v", "v", "v", "v", "v", "h", "0", "nd", "h"]
    # after: 1 visible, 2 right, 6 outside (one of them 0), the dropped item
    after = ["v", "h", "h", "o", "o", "o", "o", "o", "0", "h"]
    for i, c in enumerate(cases):
        free = sorted(set("0123456789") - set(c["conf_answers"]) - {c["answer"], "0"})
        pick = {"v": tok(c["conf_answers"][0]), "h": tok(c["answer"]), "0": 100, "nd": 1, "o": tok(free[0])}
        rows.append(row(c, pick[last[i]], "lookup", "final", "all", "value"))
        rows.append(row(c, pick[after[i]], "lookup", "after", "all", "value"))
        rows.append(row(c, tok(c["answer"]), "lookup", "after", "all", "absent"))  # mode absent: never counted
    rows.append(row(case(0, ["5", "3", "1", "9", "8"], 0, family="DL"), 100, "lookup", "final", "all", "value"))
    return rows, cases


def test_analyse_counts_rates_and_chance():
    rows, cases = scene()
    res = G.analyse(rows, cases, DECODE.__getitem__)
    assert (res["items"], res["right_unedited"], res["slots_unparsed"]) == (10, 9, 0)
    un, last, after = res["arms"]["unedited"], res["arms"]["last tokens"], res["arms"]["after"]
    assert un["n"] == 10
    assert un["counts"] == {"hidden": 9, "visible": 1, "outside": 0, "non-digit": 0, "outside_zero": 0}
    assert last["n"] == 9  # items right unedited only
    assert last["counts"] == {"hidden": 1, "visible": 6, "outside": 1, "non-digit": 1, "outside_zero": 1}
    assert last["non_digit_answers"] == {"' none'": 1}
    assert after["counts"] == {"hidden": 2, "visible": 1, "outside": 6, "non-digit": 0, "outside_zero": 1}
    assert after["right"][0] == pytest.approx(2 / 9, abs=1e-4)
    assert after["n_outside"] == 8
    assert after["right_given_outside"][0] == pytest.approx(2 / 8, abs=1e-4)
    assert after["chance_given_outside_0to9"] == pytest.approx(1 / 6)  # 10 - 4 visible
    assert after["n_outside_1to9"] == 7  # the zero left out
    assert after["right_given_outside_1to9"][0] == pytest.approx(2 / 7, abs=1e-4)
    assert after["chance_given_outside_1to9"] == pytest.approx(1 / 5)
    assert after["visible_blind_0to9"] == pytest.approx(0.4)
    assert after["digits_outside_list_per_item"] == {6: 9}
    assert last["hidden_vs_correct_mismatch"] == 0
    lo, hi = last["right_given_outside"][1:]
    assert lo is not None and hi is not None and lo < 0.5 < hi  # 1 of 2, Wilson


def test_visible_by_place():
    cases = [case(0, ["5", "3", "1", "9", "8"], 3), case(1, ["5", "3", "1", "9", "8"], 3)]
    rows = [row(c, tok(c["answer"])) for c in cases]
    rows.append(row(cases[0], tok("8"), "lookup", "final", "all", "value"))  # the next sentence: +1
    rows.append(row(cases[1], tok("5"), "lookup", "final", "all", "value"))  # the first sentence: -3
    res = G.analyse(rows, cases, DECODE.__getitem__)
    assert res["arms"]["last tokens"]["visible_by_place"] == {"-3": 1, "+1": 1}


def test_variant_digit_token_is_flagged():
    c = case(0, ["5", "3", "1", "7", "8"], 3)  # answer 7; token 4 decodes to " 7" but is not the answer's token
    rows = [row(c, tok("7")), row(c, 4, "lookup", "final", "all", "value")]
    res = G.analyse(rows, [c], DECODE.__getitem__)
    assert res["arms"]["last tokens"]["hidden_vs_correct_mismatch"] == 1


def test_grid_numbers_and_check(tmp_path):
    text = ("hidden from the last tokens (every layer): 3% right; from every token after it (all layers): 10% [7, 14] "
            "(the floor, needs <= 10%, upper bound <= 15%); relay -6 points")  # fmt: skip
    p = tmp_path / "grid.csv"
    header = (
        "model,finding,setting,lens,n,value,95% CI,chance or control level,verdict,rule id,spec commit,result path\n"
    )
    p.write_text(header + f'M,f,{G.GRID_SETTING},none,300,1,"[1, 2]","{text}",holds,late-read-v2,abc,'
                 "results/attn_knockout/run_x/rows.jsonl\n"
                 f'M,f,draw 1,none,300,1,"[1, 2]","{text}",holds,late-read,abc,results/attn_knockout/run_y/rows.jsonl\n')  # fmt: skip
    assert G.grid_numbers(p) == {"run_x": (3, 10)}
    res = {"arms": {"last tokens": {"counts": {"hidden": 10}, "n": 300}, "after": {"counts": {"hidden": 30}, "n": 300}}}
    assert G.grid_check(res, (3, 10)) == []
    assert G.grid_check(res, (3, 9)) != []
    assert G.grid_check(res, None) != []
