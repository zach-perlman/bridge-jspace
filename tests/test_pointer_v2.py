"""pointer_v2: the filler grid, the offset-shift / plain / reflexive predictions, slot balance, determinism, alignment."""

import collections
import random

import pytest

from scripts import pointer_v2 as P2


def test_grid_and_order_are_inverse():
    for n in (3, 5):
        for f in range(n + 1):
            cells = [P2.grid(k, f) for k in range(n)]
            assert sorted(cells) == [g for g in range(n + 1) if g != f]
            assert all(P2.order(P2.grid(k, f), f) == k for k in range(n))
            assert P2.order(f, f) is None


@pytest.mark.parametrize("n_ent", [3, 5])
def test_layouts_split_order_and_token(n_ent):
    for a in range(n_ent):
        for f_o, f_a, k, kp, c in P2.layouts(a, n_ent, n_ent >= 5):
            assert f_o != f_a
            assert P2.order(P2.grid(k, f_a), f_o) == kp
            assert len({a, k, kp}) == 3
            if c is not None:
                assert c not in (a, k, kp)


def scenes(which: str, n: int = 30) -> dict[str, list[dict]]:
    spec = dict(P2.SETS[which])
    old = P2.SETS[which]
    P2.SETS[which] = {**spec, "n": n}
    try:
        return {label: items for label, (_p, items, _n) in P2.generate(which).items()}
    finally:
        P2.SETS[which] = old


@pytest.mark.parametrize("which", ["main", "n3"])
def test_predictions(which):
    for label, items in scenes(which).items():
        for it in items:
            d, pd, sl = it["sources"]["dissoc"], it["sources"]["dissoc"]["predictions"], it["slots"]
            ents, dg = it["entities"], it["digits"]
            assert d["entities"][sl["position"]] == d["query"]  # the alt asks about its k-th statement
            assert ents[sl["query"]] == it["query"]
            if it["family"] == "RR":
                continue
            keys = [h for h, x in pd.items() if x != "-"]
            assert len({pd[h] for h in keys}) == len(keys), label  # every recorded prediction distinct
            assert pd["position"] == str(dg[sl["position"]])
            if it["type"] == "off":
                f_o, f_a = it["filler_cell"], d["filler_cell"]
                assert f_o != f_a
                kp = P2.order(P2.grid(sl["position"], f_a), f_o)
                assert kp == sl["token"] != sl["position"]
                assert pd["token"] == str(dg[kp])
            else:
                assert "token" not in pd
                assert d["filler_cell"] == it["filler_cell"]
            if it["type"] == "ref":
                assert pd["value"] == str(dg[sl["value_in_org"]])  # the alt answer is in the org prompt
            else:
                assert int(pd["value"]) not in dg
            if it["n_entities"] >= 5:
                assert pd["identity"] == str(dg[ents.index(d["query"])])
            else:
                assert pd["identity"] == "-"
                assert d["query"] not in ents


def test_types_share_the_org_prompt():
    by_scene = collections.defaultdict(set)
    for items in scenes("main", 12).values():
        for it in items:
            by_scene[(it["scene"], it["family"])].add(it["context"] + it["question"])
    assert all(len(v) == 1 for v in by_scene.values())


@pytest.mark.parametrize(("which", "classes"), [("main", {"first", "middle", "last"}), ("n3", {"first", "last"})])
def test_slot_classes_balanced(which, classes):
    items = scenes(which, 60)[f"animals_RL_{'e5' if which == 'main' else 'e3'}-off"]
    counts = collections.Counter(
        "first" if it["slots"]["query"] == 0 else "last" if it["slots"]["query"] == it["n_entities"] - 1 else "middle"
        for it in items
    )
    assert set(counts) == classes
    assert len(set(counts.values())) == 1


def test_hard_collision_policy():
    for items in scenes("main").values():
        for it in items:
            d, sl = it["sources"]["dissoc"], it["slots"]
            ents = it["entities"]
            crit = {it["recalled"][e] for e in (it["query"], d["query"], ents[sl["position"]])}
            if it["type"] == "off":
                crit.add(it["recalled"][ents[sl["token"]]])
            assert not set(it["digits"]) & crit
            assert not set(d["digits"]) & crit


def test_deterministic():
    assert scenes("main", 6) == scenes("main", 6)
    assert P2.slot_classes(random.Random(1), 9, 5) == P2.slot_classes(random.Random(1), 9, 5)


def test_token_alignment():
    from scripts import pointer_v1 as PV

    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")
    P2.check_filler(tok)
    for items in scenes("main", 4).values():
        for it in items:
            got = P2.check_item(tok, it)
            assert all(
                got[k] for k in ("equal_cells", "dissoc_aligned", "same_aligned", "redigit_aligned", "permutation")
            )
