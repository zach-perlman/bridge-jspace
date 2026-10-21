"""pointer_v4x: v2's filler-moved and v3's one-more / one-fewer layouts on pointer_v4's topics and wordings; and
pointer_swap's pre-registered pointer_v4x tests (H-order-v4, H-start-v4)."""

import collections

import pytest

from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import pointer_v4 as P4
from scripts import pointer_v4x as X


@pytest.fixture(scope="module")
def items():
    split = P4.load_split()
    if split is None:
        pytest.skip("no data/pointer_v4/split.json")
    old = X.SETS
    X.SETS = {"main": {"seed": 851, "n": 45}}
    try:
        return split, X.generate("main", split)
    finally:
        X.SETS = old


def test_every_layout_topic_and_family_is_built(items):
    split, out = items
    assert set(out) == {f"{d}_{f}_{lv}" for d in split["used"] for f in X.FAMILIES for lv in X.LEVELS.values()}
    for label, (_, its, _) in out.items():
        assert len(its) == 45, label


def test_predictions_name_the_designed_statements(items):
    _, out = items
    for label, (_, its, _) in out.items():
        for it in its:
            sl, dg, pd = it["slots"], it["digits"], it["sources"]["dissoc"]["predictions"]
            assert pd["position"] == str(dg[sl["position"]]) and pd["token"] == str(dg[sl["token"]]), label
            assert sl["position"] != sl["token"]
            if it["type"] == "off":
                assert "end" not in pd and it["sources"]["dissoc"]["filler_cells"] != it["filler_cells"]
            else:
                m = len(it["sources"]["dissoc"]["entities"])
                assert m == (6 if it["type"] == "more" else 4)
                assert sl["end"] == X.N_ENT - 1 - (m - 1 - sl["position"]) and pd["end"] == str(dg[sl["end"]])
            assert len(set(pd.values())) == len(pd) and int(pd["value"]) not in dg
            assert it["statements"] == P4.statements(it["domain"], it["templates"]["statement"], it["entities"], dg)


def test_cap_wordings_cut_and_fillers(items):
    split, out = items
    for label, (_, its, _) in out.items():
        assert max(collections.Counter(it["query"] for it in its).values()) <= X.CAP, label
        held = set(split["domains"][its[0]["domain"]]["held_out_entities"])
        for it in its:
            assert it["held_out_entity"] == (it["query"] in held)
            for s in it["context"].split(". "):
                s = s if s.endswith(".") else s + "."
                assert s in it["statements"] or s in X.fillers_for(it["domain"], it["templates"]["statement"])


def test_deterministic(items):
    split, out = items
    old = X.SETS
    X.SETS = {"main": {"seed": 851, "n": 45}}
    try:
        again = X.generate("main", split)
    finally:
        X.SETS = old
    assert {k: v[1] for k, v in again.items()} == {k: v[1] for k, v in out.items()}


def test_token_alignment_with_the_real_tokenizer(items):
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    X.check_lengths(tok)
    _, out = items
    for label, (_, its, _) in out.items():
        for it in its[:6]:
            assert all(X.check_item(tok, it).values()), (label, it["id"], X.check_item(tok, it))


def test_unaligned_scenes_are_dropped_whole(items):
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    _, out = items
    by_label = {k: v[1][:4] for k, v in out.items() if k.startswith("animals_") and k.endswith("e5-off")}
    rl = next(k for k in by_label if "_RL_" in k)
    broken = dict(by_label[rl][0])
    broken["sources"] = {**broken["sources"], "dissoc": {**broken["sources"]["dissoc"],
                         "question": broken["sources"]["dissoc"]["question"] + " Please"}}  # fmt: skip
    by_label[rl] = [broken, *by_label[rl][1:]]
    kept, dropped = PS.drop_unaligned(by_label, tok)
    assert dropped == {"animals": 1}
    assert all(it["scene"] != broken["scene"] for its in kept.values() for it in its)  # both families of the scene
    assert sum(len(v) for v in kept.values()) == sum(len(v) for v in by_label.values()) - 2


def rate(p: float, half: float = 0.05) -> list[float]:
    return [p, max(0.0, p - half), min(1.0, p + half)]


def fake_rates(win: float, rival: float, levels, domains=("a", "b", "c"), topic_win=None, topic_n=120) -> dict:
    out = {}
    for lv in levels:
        for la in PS.V4X_LAYERS:
            for cut in ["all", *(f"domain:{d}" for d in domains)]:
                w = win if cut == "all" or topic_win is None else topic_win.get(cut, win)
                out[f"RL|{cut}|{lv}|last|{la}|dissoc"] = {"n": 360 if cut == "all" else topic_n, "k_entities": 30,
                                                          "position": rate(w), "token": rate(rival),
                                                          "end": rate(rival)}  # fmt: skip
    return out


def test_v4x_hypotheses_need_pooled_and_two_topics():
    m = {"levels": ["e5-off", "e5more", "e5fewer"], "domains": ["a", "b", "c"], "family_roles": ["RL", "DL", "RR"]}
    x = PS.v4x_tests(m, fake_rates(0.4, 0.1, m["levels"]))
    assert x["H-order-v4"]["holds"] and x["H-start-v4"]["holds"]
    # two topics where the winner does not clear the rivals: pooled alone is not enough
    x = PS.v4x_tests(m, fake_rates(0.4, 0.1, m["levels"], topic_win={"domain:a": 0.12, "domain:b": 0.12}))
    assert not x["H-order-v4"]["holds"] and not x["H-start-v4"]["holds"]
    # topics below the n the rule needs (35) do not count
    x = PS.v4x_tests(m, fake_rates(0.4, 0.1, m["levels"], topic_n=20))
    assert not x["H-order-v4"]["holds"] and not x["H-start-v4"]["holds"]
    # only one alt type present: H-start-v4 cannot hold
    m1 = m | {"levels": ["e5-off", "e5more"]}
    x = PS.v4x_tests(m1, fake_rates(0.4, 0.1, m1["levels"]))
    assert x["H-order-v4"]["holds"] and not x["H-start-v4"]["holds"]


def test_v4x_primary_layers_from_the_manifest():
    m = {"levels": ["e5-off", "e5more", "e5fewer"], "domains": ["a", "b", "c"], "family_roles": ["RL", "DL", "RR"]}
    rates = {k.replace("|48|", "|18|"): v for k, v in fake_rates(0.4, 0.1, m["levels"]).items() if "|48|" in k}
    # the 27B's layers by default: OLMo's layer-18 cells are not looked at
    assert not PS.v4x_tests(m, rates)["H-order-v4"]["holds"]
    x = PS.v4x_tests(m | {"primary_layers": [17, 18, 19]}, rates)
    assert x["H-order-v4"]["holds"] and x["H-start-v4"]["holds"]
    assert x["H-order-v4"]["layer 18"] and not x["H-order-v4"]["layer 17"]
