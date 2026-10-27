"""pointer_v3: start / end / token pointers distinct and correct, predictions, slot balance, determinism, alignment."""

import collections

import pytest

from scripts import pointer_v3 as P3


def scenes(n: int = 24) -> dict[str, list[dict]]:
    old = P3.SETS["main"]
    P3.SETS["main"] = {**old, "n": n}
    try:
        return {label: items for label, (_p, items, _n) in P3.generate("main").items()}
    finally:
        P3.SETS["main"] = old


@pytest.mark.parametrize("typ", P3.TYPES)
def test_layouts_separate_the_three_pointers(typ):
    m = P3.N_ENT + (1 if typ == "more" else -1)
    for a in range(P3.N_ENT):
        for f_org, f_alt, k, (st, en, tk), c in P3.layouts(typ, a):
            assert len({a, c, st, en, tk}) == 5
            assert st == k
            assert en == P3.N_ENT - 1 - (m - 1 - k)  # the same distance from the end of each list
            total = P3.N_ENT + P3.FILLERS[typ][0]
            assert (
                P3.stmt_cells(total, f_org)[tk] == P3.stmt_cells(total, f_alt)[k]
            )  # the same cell, so the same tokens


def test_predictions_and_slots():
    for label, items in scenes().items():
        for it in items:
            d, pd, sl, dg = it["sources"]["dissoc"], it["sources"]["dissoc"]["predictions"], it["slots"], it["digits"]
            assert d["entities"][d["query_slot"]] == d["query"] == it["entities"][sl["identity"]]
            assert len(d["entities"]) == P3.N_ENT + (1 if it["type"] == "more" else -1)
            if it["family"] == "RR":
                assert pd["none"] != pd["identity"]
                continue
            assert len(set(pd.values())) == len(pd), label  # six distinct digits
            for h, key in (("position", "position"), ("end", "end"), ("token", "token"), ("identity", "identity")):
                assert pd[h] == str(dg[sl[key]])
            assert int(pd["value"]) not in dg
            assert set(it["sources"]["same"]["predictions"].values()) == {it["answer"]}


def test_slot_classes_balanced():
    for items in scenes(36).values():
        counts = collections.Counter(
            "first" if it["slots"]["query"] == 0 else "last" if it["slots"]["query"] == P3.N_ENT - 1 else "middle"
            for it in items
        )
        assert counts == {"first": 12, "middle": 12, "last": 12}


def test_same_length_contexts():
    for items in scenes(6).values():
        for it in items:
            n = len(it["context"].split(". "))
            for s in it["sources"].values():
                assert len(s["context"].split(". ")) == n  # the same number of equal-length sentences


def test_deterministic():
    assert scenes(4) == scenes(4)


def test_token_alignment():
    from scripts import pointer_v1 as PV

    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")
    for items in scenes(4).values():
        for it in items:
            got = P3.check_item(tok, it)
            assert all(got.values()), (it["id"], got)
