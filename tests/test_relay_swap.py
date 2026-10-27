"""relay_swap: the substitution checks on synthetic items (the target's tokenizer, skipped when not cached), the rows
per item, and the verdict on synthetic rows (no model)."""

from pathlib import Path

import pytest

from bridge_jspace import pins, tokens
from scripts import attn_knockout as A
from scripts import relay_swap as R

ENTS = ["camel", "mouse", "worm", "eagle", "rabbit"]
QUESTION = "Which locker belongs to the animal known for its talons?"


@pytest.fixture(scope="module")
def tok():
    try:
        return tokens.load_tokenizer()
    except Exception:
        try:
            from huggingface_hub import try_to_load_from_cache
            from transformers import AutoTokenizer

            path = try_to_load_from_cache(pins.MODEL_REPO, "tokenizer.json", revision=pins.MODEL_REVISION)
            assert isinstance(path, str)
            return AutoTokenizer.from_pretrained(str(Path(path).parent))
        except Exception:
            pytest.skip("target tokenizer not cached")


def _item(digits=(5, 3, 1, 9, 8), q=3, red=(5, 3, 1, 6, 8), question=QUESTION) -> dict:
    """A pointer_v4-style memory -> prompt item whose 'redigit' prompt has the digits `red`."""

    def st(ds):
        return [f"The {e}'s locker is {d}." for e, d in zip(ENTS, ds, strict=True)]

    return {"id": "t-RL-0", "family": "RL", "domain": "animals", "level": "e5f0", "scene": "t-0", "n_entities": 5,
            "entities": ENTS, "digits": list(digits), "query": ENTS[q], "cue": "the animal known for its talons",
            "slots": {"query": q, "identity": 4, "position": 2}, "context": " ".join(st(digits)),
            "statements": st(digits), "question": question, "answer": str(digits[q]), "answer_kind": "digit",
            "templates": {"statement": 0, "question": 0},
            "sources": {"redigit": {"context": " ".join(st(red)), "statements": st(red), "question": question,
                                    "answer": str(red[q]), "entities": ENTS, "digits": list(red), "query": ENTS[q],
                                    "query_slot": q}}}  # fmt: skip


def test_substitute_changes_the_answer_digit_token_only(tok):
    item = _item()
    case = A.pointer_case(item, tok, "pointer_v4")
    c = R.substitute(case, item, tok)
    assert c["new"] == "6"
    assert len(c["sub_ids"]) == len(case["ids"])
    assert [i for i, (a, b) in enumerate(zip(case["ids"], c["sub_ids"], strict=True)) if a != b] == [c["sub_pos"]]
    assert c["sub_pos"] in case["sources"]["lookup"]
    assert tok.decode([c["sub_ids"][c["sub_pos"]]]).strip() == "6"
    assert c["tok_new"] == R.S.answer_token(tok, "6", "digit") != case["tok_A"]
    assert "The eagle's locker is 6." in c["sub_prompt"] and "The eagle's locker is 9." in case["prompt"]


@pytest.mark.parametrize(
    ("red", "question", "why"),
    [
        ((5, 3, 1, 8, 8), QUESTION, "in the list"),  # the new digit is another statement's
        ((5, 3, 2, 6, 8), QUESTION, "differs too"),  # another statement's digit changes too
        ((5, 3, 1, 6, 8), "Which of the 6 lockers belongs to the animal known for its talons?", "original prompt"),
    ],
)
def test_substitute_refuses_a_bad_substitution(tok, red, question, why):
    item = _item(red=red, question=question)
    case = A.pointer_case(item, tok, "pointer_v4")
    with pytest.raises(AssertionError, match=why):
        R.substitute(case, item, tok)


def test_conditions_put_dans_rows_first_and_add_the_every_layer_block_on_hybrids_only():
    dense = R.conditions([A.FULL] * 8)
    hybrid = R.conditions([A.LINEAR, A.LINEAR, A.LINEAR, A.FULL] * 2)
    keys = [(c["arm"], c["source"], c["dest"], c["layers"]) for c in hybrid]
    assert keys[:6] == [("orig", "none", "-", "-"), ("sub", "none", "-", "-"),
                        ("orig", "lookup", "final", "attn"), ("sub", "lookup", "final", "attn"),
                        ("orig", "lookup_off", "final", "attn"), ("sub", "lookup_off", "final", "attn")]  # fmt: skip
    assert keys[6:] == [("orig", "lookup", "after", "all"), ("sub", "lookup", "after", "all"),
                        ("orig", "lookup", "final", "all"), ("sub", "lookup", "final", "all")]  # fmt: skip
    assert len(dense) == 8 and {c["layers"] for c in dense} == {"-", "all"}


def test_standalone_digit():
    assert R.standalone("locker is 6.", "6")
    assert not R.standalone("locker is 16.", "6")
    assert not R.standalone("lockers 61 and 7", "6")


def _rows(n=40, sub_new=0.5, orig_new=0.0, pos=1.0, off=1.0, floor_sub=0.0, right=1.0) -> tuple[list, dict]:
    """Synthetic rows (a model without DeltaNet: LATE = all): item i answers the new digit in a row kind iff i is
    below that kind's share of n; otherwise the old digit (unedited, off-path) or another listed digit (blocked)."""
    share = {("orig", "none"): None, ("sub", "none"): pos, ("orig", "lookup", "final"): orig_new,
             ("sub", "lookup", "final"): sub_new, ("orig", "lookup_off", "final"): 0.0,
             ("sub", "lookup_off", "final"): off, ("orig", "lookup", "after"): 0.0,
             ("sub", "lookup", "after"): floor_sub}  # fmt: skip
    rows, cases = [], {}
    for i in range(n):
        iid = f"it{i}"
        cases[iid] = {"bridge": f"e{i % 10}", "domain": "animals" if i % 2 else "body"}
        for c in R.conditions([A.FULL] * 4):
            k = (c["arm"], c["source"]) if c["source"] == "none" else (c["arm"], c["source"], c["dest"])
            if k == ("orig", "none"):
                new, old = False, i < right * n
            else:
                new = i < share[k] * n
                old = not new and (c["source"] in ("none", "lookup_off") and c["arm"] == "orig")
            rows.append({"family": "RL", "id": iid, **c, "new": new, "old": old, "listed": not (new or old),
                         "top": 1 if new else 2 if old else 3, **cases[iid]})  # fmt: skip
    return rows, cases


M = {"late": "all", "run": "t", "from": "late", "model": {"repo": "org/model"}}


def test_verdict_finds_a_relay():
    rows, cases = _rows(sub_new=0.5)
    v = R.verdict(M, rows, cases)
    assert v["test"]["R"][0] == pytest.approx(0.5) and v["test"]["R"][1] > R.RELAY_LO
    assert v["verdict"] == "relay"
    assert v["every_layer"] is None and set(v["test"]["topics"]) == {"animals", "body"}


def test_verdict_no_relay_when_both_prompts_answer_the_new_digit_alike():
    rows, cases = _rows(sub_new=0.1, orig_new=0.1)
    v = R.verdict(M, rows, cases)
    assert v["test"]["R"][0] == pytest.approx(0.0)
    assert v["verdict"] == "no relay"


@pytest.mark.parametrize(
    ("kw", "why"),
    [({"pos": 0.5}, "positive control"), ({"off": 0.5}, "off-path control"), ({"floor_sub": 0.5}, "the floor")],
)
def test_verdict_not_interpretable_when_a_control_fails(kw, why):
    rows, cases = _rows(**kw)
    v = R.verdict(M, rows, cases)
    assert v["verdict"].startswith("not interpretable") and why in v["verdict"]


def test_verdict_counts_only_items_right_unedited():
    rows, cases = _rows(sub_new=0.5, right=0.5)  # items 0-19 right unedited, and exactly those answer the new digit
    v = R.verdict(M, rows, cases)
    assert v["n_counted"] == 20 and v["n_items"] == 40
    assert v["test"]["R"][0] == pytest.approx(1.0)
    answers = v["answers"]["sub|lookup|final|all"]
    assert answers["new"][0] == pytest.approx(1.0) and answers["listed"][0] == 0.0


def test_figure_and_report_render(tmp_path):
    rows, cases = _rows()
    v = R.verdict(M, rows, cases)
    R.figure(M, v, rows, cases, tmp_path / "f.png")
    assert (tmp_path / "f.png").stat().st_size > 0
    assert "Verdict: relay" in R.report(M, v)
