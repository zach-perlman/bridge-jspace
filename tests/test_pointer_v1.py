"""pointer_v1's generator: predictions, permutations, collision policy, slot balance, determinism, token alignment."""

import collections

import pytest

from scripts import pointer_v1 as PV

CELLS = [(d, n_ent, n_fill) for d in PV.DOMAINS for n_ent, n_fill in ((3, 0), (5, 0), (5, 4))]


def cell(domain: str, n_ent: int, n_fill: int, n: int = 40) -> dict[str, list[dict]]:
    return PV.generate_cell(123, domain, f"e{n_ent}f{n_fill}", n_ent, n_fill, n)


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_predictions_distinct_and_correct(domain, n_ent, n_fill):
    for fam, items in cell(domain, n_ent, n_fill).items():
        for it in items:
            sl, d = it["slots"], it["sources"]["dissoc"]
            look = dict(zip(it["entities"], it["digits"], strict=True))
            q_s, p = d["query"], it["entities"][sl["position"]]
            assert it["entities"][sl["query"]] == it["query"]
            assert it["entities"][sl["identity"]] == q_s
            assert d["entities"][sl["position"]] == q_s  # the source queries slot k, where the base has p
            assert len({sl["query"], sl["identity"], sl["position"]}) == 3
            pd = d["predictions"]
            if fam == "RR":
                assert pd["none"] != pd["identity"]
                assert pd["value"] == pd["identity"]
                assert pd["position"] == str(PV.rec(domain, p))
            else:
                assert len(set(pd.values())) == 4
                assert pd == {
                    "none": str(look[it["query"]]),
                    "identity": str(look[q_s]),
                    "position": str(look[p]),
                    "value": d["answer"],
                }
                assert int(pd["value"]) not in it["digits"]  # the value is absent from the base context
            assert set(it["sources"]["same"]["predictions"].values()) == {it["answer"]}


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_collision_policy(domain, n_ent, n_fill):
    for items in cell(domain, n_ent, n_fill).values():
        for it in items:
            d = it["sources"]["dissoc"]
            critical = {PV.rec(domain, e) for e in (it["query"], d["query"], it["entities"][it["slots"]["position"]])}
            assert not set(it["digits"]) & critical  # hard: always
            assert not set(d["digits"]) & critical
            if it["digit_policy"] == "soft":  # promised only where the pool allows
                assert not set(it["digits"]) & set(it["recalled"].values())
        if n_ent == 3:
            assert all(it["digit_policy"] == "soft" for it in items)


@pytest.mark.parametrize(("domain", "n_ent"), [(d, n) for d in PV.DOMAINS for n in (3, 5)])
def test_slots_balanced(domain, n_ent):
    n_pairs = n_ent * (n_ent - 1)
    items = cell(domain, n_ent, 0, n=3 * n_pairs)["RL"]
    for key in ("query", "position"):
        counts = collections.Counter(it["slots"][key] for it in items)
        assert set(counts.values()) == {3 * (n_ent - 1)}, (key, counts)


def test_controls_and_contexts():
    for it in cell("animals", 5, 4)["RL"]:
        same, red = it["sources"]["same"], it["sources"]["redigit"]
        a = it["slots"]["query"]
        assert same["entities"][a] == it["query"]
        assert same["digits"][a] == it["digits"][a]
        assert same["context"] != it["context"]
        assert red["entities"] == it["entities"]
        assert sum(x != y for x, y in zip(red["digits"], it["digits"], strict=True)) == 1
        assert red["predictions"]["value"] == it["sources"]["dissoc"]["predictions"]["value"]
        for fill in (s for s in it["context"].split(". ") if "locker" not in s):  # filler sits at the same places
            assert fill in it["sources"]["dissoc"]["context"]


def test_deterministic():
    assert cell("months", 5, 0) == cell("months", 5, 0)
    assert PV.generate_cell(1, "months", "e5f0", 5, 0, 10) != PV.generate_cell(2, "months", "e5f0", 5, 0, 10)


def test_token_alignment():
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")
    PV.check_pools(tok)
    for domain in PV.DOMAINS:
        for items in cell(domain, 5, 4, n=8).values():
            for it in items:
                got = PV.check_item(tok, it)
                for k in ("dissoc_aligned", "same_aligned", "redigit_aligned", "permutation", "value_absent"):
                    assert got[k], (it["id"], k)
