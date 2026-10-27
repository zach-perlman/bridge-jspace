"""pointer_v4: the entity probe's rule, the held-out split, the cap, the items' predictions; pointer_swap and
pointer_fit's entity-cluster intervals."""

import collections

import pytest

from scripts import pointer_fit as PF
from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import pointer_v4 as P4


class WordTok:
    """A tokenizer stand-in: one id per word (cue lengths = word counts)."""

    class _Enc:
        def __init__(self, n: int):
            self.input_ids = list(range(n))

    def __call__(self, text: str, add_special_tokens: bool = False):
        return self._Enc(len(text.split()))


@pytest.fixture(scope="module")
def split():
    return P4.make_split(None, WordTok())


@pytest.fixture(scope="module")
def sets(split):
    return {w: P4.generate(w, split) for w in P4.SETS}


def probe_rows(passing: dict[str, int]) -> list[dict]:
    """Every candidate's three steps; the first `passing[d]` entities of a domain right, the rest wrong at 'chain'."""
    rows = []
    for d, spec in P4.SPEC.items():
        for i, e in enumerate(spec["candidates"]):
            for step in ("cue", "fact", "chain"):
                rows.append({"domain": d, "entity": e, "step": step,
                             "correct": i < passing.get(d, 0) or step != "chain"})  # fmt: skip
    return rows


def test_probe_rule_keeps_entities_right_on_every_step_and_the_first_three_usable_domains():
    r = P4.probe_result(probe_rows({"countries": 30, "sports": 15, "animals": 16, "body": 20}))
    assert r["domains"]["sports"]["usable"] is False  # 15 < 16
    assert r["domains"]["animals"]["n_pass"] == 16
    assert r["used"] == ["countries", "animals", "body"]  # sports fails, the backup steps in
    fail = r["domains"]["countries"]["fail"]
    assert all(steps == ["chain"] for steps in fail.values())
    assert len(fail) == len(P4.COUNTRIES) - 30


def test_judge_reads_entities_and_digits_without_recursion():
    assert P4.said(" Peru\n", "countries") == "Peru"
    assert P4.said(" Ice hockey.", "sports") == "hockey"
    assert P4.said(" the owl", "animals") == "owl"
    old = PV.said
    try:
        PV.said = P4.said  # what competence does: the v4 judge must still reach pointer_v1's digit judge
        assert P4.said(" 7 legs", "digit") == "7"
        assert P4.said(" four", "digit") == "4"
    finally:
        PV.said = old


def test_split_holds_out_a_third_and_template_two(split):
    for d in split["used"]:
        info = split["domains"][d]
        held, fit = set(info["held_out_entities"]), set(info["fit_entities"])
        assert not held & fit
        assert held | fit == set(info["pool"])
        assert abs(len(held) - len(info["pool"]) / 3) <= 1
        assert info["held_out_template"] == 2


def test_cap_no_entity_asked_in_more_than_a_twelfth(sets):
    for which, out in sets.items():
        for label, (_, items, _) in out.items():
            asked = collections.Counter(it["query"] for it in items)
            assert max(asked.values()) / len(items) <= 1 / P4.CAP + 1e-9, (which, label)
            assert len({it["context"] + it["question"] for it in items}) == len(items), (which, label)


def test_fit_never_sees_a_held_out_entity_or_wording(split, sets):
    for label, (_, items, _) in sets["fit"].items():
        held = set(split["domains"][items[0]["domain"]]["held_out_entities"])
        for it in items:
            assert it["family"] == "RL"
            assert not set(it["entities"]) & held, label
            assert not set(it["sources"]["dissoc"]["entities"]) & held, label
            assert P4.HELD_OUT_TEMPLATE not in it["templates"].values(), label
            assert it["cut"] == "neither"


def test_main_items_record_their_cut_and_cover_every_wording(split, sets):
    for label, (_, items, _) in sets["main"].items():
        held = set(split["domains"][items[0]["domain"]]["held_out_entities"])
        for it in items:
            ent, tpl = it["query"] in held, 2 in it["templates"].values()
            assert (it["held_out_entity"], it["held_out_template"]) == (ent, tpl)
            assert it["cut"] == {(True, True): "both", (True, False): "entity", (False, True): "template",
                                 (False, False): "neither"}[(ent, tpl)]  # fmt: skip
        assert {(it["templates"]["statement"], it["templates"]["question"]) for it in items} == {
            (s, q) for s in range(3) for q in range(3)
        }, label


def test_predictions_and_pairs(split, sets):
    for _, (_, items, _) in sets["main"].items():
        for it in items:
            d, pd = it["domain"], it["sources"]["dissoc"]["predictions"]
            q_b, q_s = it["query"], it["sources"]["dissoc"]["query"]
            cue_len = split["domains"][d]["cue_tokens"]
            assert cue_len[q_b] == cue_len[q_s]
            assert P4.rec(d, q_b) != P4.rec(d, q_s)
            assert it["context"] == " ".join(it["statements"])
            t = it["templates"]["statement"]
            for src in P4.SOURCES:  # every prompt of a scene in the scene's wording
                s = it["sources"][src]
                assert s["statements"] == P4.statements(d, t, s["entities"], s["digits"])
            if it["family"] == "RR":
                assert pd["none"] == str(P4.rec(d, q_b)) and pd["identity"] == str(P4.rec(d, q_s))
            else:
                assert len(set(pd.values())) == 4
                assert pd["position"] == str(it["digits"][it["slots"]["position"]])
                assert int(pd["value"]) not in it["digits"]


def test_generator_is_deterministic(split, sets):
    again = P4.generate("main", split)
    assert {k: v[1] for k, v in again.items()} == {k: v[1] for k, v in sets["main"].items()}


def test_items_token_aligned_with_the_real_tokenizer(sets):
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    P4.check_tokens(tok)
    split = P4.make_split(None, tok)  # the real cue lengths
    for _, (_, items, _) in P4.generate("main", split).items():
        for it in items[:12]:
            assert all(P4.check_item(tok, it).values()), it["id"]


def rows_for(clusters: int, per: int, hit_cluster) -> list[dict]:
    return [{"domain": "d", "entity": f"e{c}", "template": f"{c % 3}/0", "role": "position" if hit_cluster(c) else "none"}
            for c in range(clusters) for _ in range(per)]  # fmt: skip


def test_swap_cluster_intervals_widen_and_fall_back_to_wilson():
    rows = rows_for(20, 10, lambda c: c % 2 == 0)  # every entity all-or-nothing: effective n = 20, not 200
    w = PS.roles_of(rows)
    c = PS.roles_of(rows, PS.CLUSTER_CI)
    assert c["position"][0] == w["position"][0]
    assert c["position"][2] - c["position"][1] > 2 * (w["position"][2] - w["position"][1])
    assert c["wilson"]["position"] == w["position"]
    assert c["identity"] == w["identity"]  # 0 events: Wilson stands
    assert (c["n"], c["k_entities"], c["t_wordings"]) == (200, 20, 3)
    assert c["changed"] == c["position"]


def test_verdict_reads_the_cells_own_changed_interval():
    d = {"n": 100, "none": [0.75, 0.66, 0.82], "changed": [0.25, 0.10, 0.40], "identity": [0.0, 0.0, 0.04],
         "position": [0.25, 0.17, 0.35], "value": [0.0, 0.0, 0.04], "context": [0.0, 0.0, 0.04]}  # fmt: skip
    same = {"n": 100, "none": [1.0, 0.96, 1.0], "changed": [0.0, 0.0, 0.04]}
    assert PS.verdict("RL", d, same, {}, 5) == "none"  # the cluster lower bound 0.10 < 0.20, though Wilson's is 0.17
    d["changed"] = [0.25, 0.21, 0.30]
    assert PS.verdict("RL", d, same, {}, 5) == "position"


def test_fit_rate_and_paired_use_clusters_for_v4():
    slot = {f"i{i}": r | {"name": f"i{i}"} for i, r in enumerate(rows_for(20, 10, lambda c: c % 2 == 0))}
    lens = {k: v | {"role": "none"} for k, v in slot.items()}
    w, c = PF.rate(slot), PF.rate(slot, ci=PS.CLUSTER_CI)
    assert w[3] == c[3] == 200
    assert c[2] - c[1] > w[2] - w[1]
    d_item, d_cl = PF.paired(slot, lens), PF.paired(slot, lens, ci=PS.CLUSTER_CI)
    assert d_item[0] == pytest.approx(d_cl[0])
    assert d_cl[2] - d_cl[1] > d_item[2] - d_item[1]
    assert PF.nkt(slot) == [200, 20, 3]
    assert PF.pools(["animals"]) == PF.pools({"domains": ["animals"]})  # older callers pass a list
