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


def test_random_basis_is_orthonormal_and_seeded():
    import torch

    q = D.random_basis(64, torch.Generator().manual_seed(3))
    assert torch.allclose(q.T @ q, torch.eye(64), atol=1e-5)
    assert torch.equal(q, D.random_basis(64, torch.Generator().manual_seed(3)))
    assert not torch.allclose(q, D.random_basis(64, torch.Generator().manual_seed(4)))


def test_rand_sub_is_a_projection_with_the_jspace_parts_share():
    import torch

    from scripts.exp04_brew_parts import signed_omp

    d, g = 256, torch.Generator().manual_seed(5)
    dictionary = torch.nn.functional.normalize(torch.randn(1000, d, generator=g), dim=-1)
    delta = torch.randn(6, d, generator=g) * torch.tensor([[1.0], [3.0], [0.2], [1.0], [1.0], [1.0]])
    delta[3] = 0.0  # a position where C's copy is zero
    jspace = signed_omp(dictionary, delta, 25)  # an OMP fit is a projection: the target size
    share = jspace.norm(dim=-1) ** 2 / (delta.norm(dim=-1) ** 2).clamp_min(1e-30)
    share[4], share[5] = 0.0, 1.0  # the ends
    basis = D.random_basis(d, torch.Generator().manual_seed(6))
    part = D.random_subspace_part(delta, share, basis)
    norm2 = delta.norm(dim=-1) ** 2
    got = part.norm(dim=-1) ** 2 / norm2.clamp_min(1e-30)
    step = ((delta @ basis) ** 2).max(dim=-1).values / norm2.clamp_min(1e-30)  # one basis direction's contribution
    live = [0, 1, 2, 4, 5]
    assert torch.all((got - share)[live].abs() <= step[live] / 2 + 1e-5)  # the same share, row by row
    assert torch.allclose((part * (delta - part)).sum(-1), torch.zeros(6), atol=1e-3)  # a projection of the change
    assert torch.equal(part[3], torch.zeros(d)) and torch.equal(part[4], torch.zeros(d))
    assert torch.allclose(part[5], delta[5], atol=1e-4)
    rows = [0, 1, 2]  # not the J-space part itself: the remainder off delta points elsewhere
    off = lambda x: x - (x * delta).sum(-1, keepdim=True) / norm2[:, None].clamp_min(1e-30) * delta  # noqa: E731
    cos = torch.nn.functional.cosine_similarity(off(part)[rows], off(jspace)[rows], dim=-1)
    assert torch.all(cos.abs() < 0.5)


def test_not_rand_sub_is_the_change_minus_its_random_part():
    """B2 (23 Oct): run_parts sets not_rand_sub = delta - rand_sub; with rand_sub a projection, the two are orthogonal
    and their squared norms add up to the change's."""
    import torch

    d, g = 96, torch.Generator().manual_seed(9)
    delta = torch.randn(4, d, generator=g)
    share = torch.tensor([0.0, 0.2, 0.5, 1.0])
    rand_sub = D.random_subspace_part(delta, share, D.random_basis(d, torch.Generator().manual_seed(10)))
    rest = delta.float() - rand_sub
    assert torch.allclose(rest + rand_sub, delta, atol=1e-5)
    assert torch.allclose((rest * rand_sub).sum(-1), torch.zeros(4), atol=1e-3)
    norms = delta.norm(dim=-1) ** 2
    assert torch.allclose(rest.norm(dim=-1) ** 2 + rand_sub.norm(dim=-1) ** 2, norms, rtol=1e-4)
    assert torch.allclose(rest[0], delta[0]) and torch.allclose(rest[3], torch.zeros(d), atol=1e-4)  # the ends


def test_not_jspace_matched_is_the_rest_at_the_lens_parts_size():
    import torch

    from scripts.exp04_brew_parts import signed_omp

    d, g = 128, torch.Generator().manual_seed(7)
    dictionary = torch.nn.functional.normalize(torch.randn(500, d, generator=g), dim=-1)
    delta = torch.randn(5, d, generator=g) * torch.tensor([[1.0], [4.0], [0.3], [1.0], [1.0]])
    delta[3] = 0.0  # a position where C's copy is zero
    delta[4] = 2.0 * dictionary[11] - dictionary[40]  # all of it in the J-space: the rest is zero
    jspace = signed_omp(dictionary, delta, 25)
    rest = delta - jspace
    got = D.rescale_rows(rest, jspace.norm(dim=-1))
    live = [0, 1, 2]
    assert torch.allclose(got.norm(dim=-1)[live], jspace.norm(dim=-1)[live], rtol=1e-5)  # the lens part's size
    assert torch.allclose(torch.nn.functional.cosine_similarity(got[live], rest[live], dim=-1), torch.ones(3))
    assert torch.allclose((got * jspace).sum(-1)[live], torch.zeros(3), atol=1e-3)  # still off the lens part's atoms
    assert torch.equal(got[3], torch.zeros(d))
    assert torch.allclose(got[4], torch.zeros(d), atol=1e-3)  # rest ~0 (fit to float precision): stays ~0
