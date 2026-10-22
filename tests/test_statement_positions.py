"""statement_positions (D1): position sets from character offsets on real suite and country items (the cached
Qwen3.6-27B tokenizer; skipped without it), the zero-cell logic and the decision helpers (no model)."""

import collections

import pytest

from scripts import exp09_bind_recall as E
from scripts import statement_positions as D
from scripts import suite_split as P
from scripts import suite_v1 as S

N = 25  # cases per family


@pytest.fixture(scope="module")
def tok():
    try:
        return D.load_tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")


@pytest.fixture(scope="module")
def cases(tok):
    got, counts = D.build_cases(tok, N, list(D.DEFAULT_FAMILIES))  # PP / PM need a tasks_v2 set and competence run
    assert all(v == N for part in counts.values() for v in part["n"].values())
    return got


def text(tok, c, positions):
    return tok.decode([c["ids"]["clean"][i] for i in positions])


def test_sets_decode_to_their_sentences(tok, cases):
    for c in cases:
        st = D.statements(c)
        sets = c["sets"]
        assert text(tok, c, sets["bridge_word"]).strip() == c["bridge"]
        assert text(tok, c, sets["bind_bridge"]).strip() == st["bind_bridge"]
        assert c["bridge"] in st["bind_bridge"]
        if c["family"] in D.BOUND:  # the queried person's statement
            assert st["bind_bridge"].startswith(c["cue"])
        assert text(tok, c, sets["context"]).strip() == c["context_text"]
        if c["family"] in D.SUITE:
            assert text(tok, c, sets["lookup_bridge"]).strip() == st["lookup_bridge"]
            assert text(tok, c, sets["lookup_x"]).strip() == st["lookup_x"]
        final = text(tok, c, sets["final"])
        assert final.startswith("<|im_end|>") and final.endswith("Answer:")
        assert "<|im_end|>" not in text(tok, c, sets["q_words"])


def test_sets_disjoint_and_nested(cases):
    for c in cases:
        s = {k: set(v) for k, v in c["sets"].items()}
        parts = ("bind_bridge", "bind_other", "lookup_bridge", "lookup_x")
        for i, a in enumerate(parts):
            for b in parts[i + 1 :]:
                assert not s[a] & s[b], (c["id"], a, b)
        assert s["bridge_word"] <= s["bind_bridge"]
        assert s["bind_bridge"] | s["bind_other"] | s["lookup_bridge"] | s["lookup_x"] <= s["context"]
        assert not s["context"] & s["question"]
        assert not s["q_words"] & s["final"] and s["q_words"] | s["final"] == s["question"]
        if c["family"] in D.COUNTRIES:
            assert not s["lookup_bridge"] and not s["lookup_x"]


def test_question_set_is_suite_splits(tok, cases):
    """Recomputed independently with suite_split's / exp09's own prepare."""
    items = {f: {it["id"]: it for it in S.load(f)} for f in D.SUITE}
    country_items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(country_items)}
    for c in cases:
        if c["family"] in D.SUITE:
            ref = P.prepare(items[c["family"]][c["id"]], tok)["groups"]["question"]
        else:
            index, item = by_uid[c["id"]]
            ref = E.prepare(item, index, tok, "chat_prefill")["groups"]["question"]
        assert c["sets"]["question"] == ref


def test_cue_only_statements_identical_in_c(cases):
    """RL, RR, countries R: C changes only the cue, after every statement, so copying C there is an exact no-op."""
    seen = collections.Counter()
    for c in cases:
        if c["family"] not in D.CUE_ONLY:
            continue
        seen[c["family"]] += 1
        first = min(c["changed"]["cf"])
        for s in D.STATEMENT_SETS:
            pos = c["sets"][s]
            if pos:
                assert [c["ids"]["clean"][i] for i in pos] == [c["ids"]["cf"][i] for i in pos]
                assert D.zero_by_causality(pos, c["changed"]["cf"]) and max(pos) < first
        assert not D.zero_by_causality(c["sets"]["question"], c["changed"]["cf"])
    assert set(seen) == set(D.CUE_ONLY)


def test_bound_c_rebinds_and_o_is_off_the_bindings(cases):
    for c in cases:
        if c["family"] not in D.BOUND:
            continue
        cf = set(c["changed"]["cf"])
        assert cf <= set(c["sets"]["bind_bridge"]) | set(c["sets"]["bind_other"])
        assert cf & set(c["sets"]["bridge_word"])
        if c["family"] in D.SUITE:  # O changes table rows, all after the binding statements
            for s in ("bind_bridge", "bridge_word", "bind_other"):
                assert D.zero_by_causality(c["sets"][s], c["changed"]["off"])


def test_paired_readers_share_the_statement_patch(cases):
    """BL and BR (BLR and BRL) on one scene: identical clean and C tokens over every binding statement."""
    by = {(c["family"], c["scene"]): c for c in cases}
    pairs = 0
    for a, b in D.PAIRS:
        for (fam, scene), ca in by.items():
            cb = by.get((b, scene))
            if fam != a or cb is None:
                continue
            pairs += 1
            sets = ("bind_bridge", "bind_other") if a == "BLR" else ("context",)
            for s in sets:
                assert ca["sets"][s] == cb["sets"][s]
                for src in ("clean", "cf"):
                    assert [ca["ids"][src][i] for i in ca["sets"][s]] == [cb["ids"][src][i] for i in cb["sets"][s]]
    assert pairs >= N


def test_map_plan_skips_exact_zero_cells(cases):
    for c in cases:
        cells = D.map_plan(c, (0, 32))
        stmt_cf = [x for x in cells if x[0] in D.STATEMENT_SETS and x[2] == "cf"]
        if c["family"] in D.CUE_ONLY:
            assert not stmt_cf
        else:
            assert stmt_cf
        if c["family"] in D.SUITE:
            assert not [x for x in cells if x[0] in ("bind_bridge", "bridge_word", "bind_other") and x[2] == "off"]
        assert ("question", 32, "rand") in cells


def test_find_sentence_respects_boundaries():
    ctx = "Jordan's pet is a cow. Dan's pet is a bee."
    assert D.find_sentence(ctx, "Dan's pet is a bee.") == ctx.index("Dan's")
    with pytest.raises(AssertionError):
        D.find_sentence("Jordan's pet is a cow.", "Dan's pet is a cow.")


def test_decision_helpers():
    assert D.d1_verdict((2.0, 1.5, 2.5), (0.3, 0.2, 0.4), (-0.1, -0.2, 0.0)) == "inside"
    assert D.d1_verdict((2.0, 1.5, 2.5), (1.8, 1.6, 2.0), (-0.1, -0.2, 0.0)) == "inconclusive"  # under the null
    assert D.d1_verdict((0.4, 0.3, 0.5), None, (0.3, 0.2, 0.4)) == "around"
    rows = []
    for i in range(40):
        rows += [{"name": f"c{i}", "part": f"lens_x{sc:g}", "role": "b" if sc >= 2 else "A"} for sc in D.SCALES]
        rows += [{"name": f"c{i}", "part": f"random_x{sc:g}", "role": "A"} for sc in D.SCALES]
    assert D.write_verdict(rows)[0] == "written"
    for r in rows:
        r["role"] = "A"
    assert D.write_verdict(rows)[0] == "not written"
    same = ({"s1": 0.2, "s2": 0.1}, {"s1": 1.0, "s2": 1.0}, {"s1": 0.1, "s2": 0.1})
    assert D.concentration_diff(same, same)[0] == pytest.approx(0.0)
