"""pointer_v6: one scene under four layouts (nothing moves / absolute shift / relative shift / long statements);
pointer_swap's patching of sources aligned from the end and its pre-registered pointer_v6 tests."""

import pytest

from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import pointer_v4 as P4
from scripts import pointer_v6 as V


@pytest.fixture(scope="module")
def items():
    split = P4.load_split()
    if split is None:
        pytest.skip("no data/pointer_v4/split.json")
    old = V.SETS
    V.SETS = {"main": {"seed": 861, "n": 30}}
    try:
        return split, V.generate("main", split)
    finally:
        V.SETS = old


def by_scene(out) -> dict:
    scenes: dict = {}
    for _, its, _ in out.values():
        for it in its:
            scenes.setdefault((it["family"], it["scene"]), {})[it["level"]] = it
    return scenes


def test_every_level_shares_the_scene(items):
    split, out = items
    assert set(out) == {f"{d}_{f}_{lv}" for d in split["used"] for f in V.FAMILIES for lv in V.LEVELS}
    for levels in by_scene(out).values():
        assert set(levels) == set(V.LEVELS)
        its = list(levels.values())
        for key in ("entities", "digits", "question", "answer", "query"):
            assert len({str(it[key]) for it in its}) == 1, key
        assert len({str(it["sources"]["dissoc"]["entities"]) for it in its}) == 1


def test_layouts_and_predictions(items):
    _, out = items
    for levels in by_scene(out).values():
        for lv, it in levels.items():
            sl, dg, alt = it["slots"], it["digits"], it["sources"]["dissoc"]
            pd, k = alt["predictions"], sl["position"]
            assert len(set(pd.values())) == len(pd) and int(pd["value"]) not in dg
            assert pd["position"] == str(dg[k]) and pd["none"] == it["answer"] == str(dg[sl["query"]])
            sides = (it["filler_side"], alt["filler_side"])
            if lv in ("e5-still", "e5-long"):
                assert sides[0] == sides[1] in ("before", "after") and "align" not in it
                assert not {"token", "back"} & set(sl)
            else:
                moved = "token" if lv == "e5-abs" else "back"
                m = sl[moved]
                assert it["align"] == "end" and abs(m - k) == 1 and pd[moved] == str(dg[m])
                where = "before" if lv == "e5-abs" else "after"
                # m = k + 1: the alt prompt has the sentence before its list (abs), the org before its question (rel)
                want = {("e5-abs", 1): (None, where), ("e5-abs", -1): (where, None),
                        ("e5-rel", 1): (where, None), ("e5-rel", -1): (None, where)}[(lv, m - k)]  # fmt: skip
                assert sides == want, (lv, m - k, sides)
            for src in ("same", "redigit"):  # controls keep the org layout
                assert it["sources"][src]["filler_side"] == it["filler_side"]
        long, still = levels["e5-long"], levels["e5-still"]
        assert all(len(a) > len(b) for a, b in zip(long["statements"], still["statements"], strict=True))


def test_deterministic(items):
    split, out = items
    old = V.SETS
    V.SETS = {"main": {"seed": 861, "n": 30}}
    try:
        again = V.generate("main", split)
    finally:
        V.SETS = old
    assert {k: v[1] for k, v in again.items()} == {k: v[1] for k, v in out.items()}


def test_clauses_are_clean():
    V.check_clauses()


def test_items_check_with_the_real_tokenizer(items):
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    _, out = items
    for label, (_, its, _) in out.items():
        for it in its[:4]:
            res = V.check_item(tok, it)
            assert all(res.values()), (label, it["id"], res)


def test_end_aligned_patch_positions(items):
    """The base's last tokens map to the source's last tokens; template tokens after the question match."""
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    _, out = items
    it = next(i for _, its, _ in out.values() for i in its if i["level"] == "e5-rel")
    prep = PS.prepare(it, tok)
    sh = prep["shift"]["dissoc"]
    assert sh != 0 and prep["shift"]["same"] == 0
    base, src = prep["read_ids"]["base"], prep["read_ids"]["dissoc"]
    assert len(src) == len(base) + sh
    for i in prep["groups"]["final"] + prep["groups"]["last"]:
        assert src[i + sh] == base[i]
    broken = {**it, "align": None}  # the same item without the end-alignment flag is rejected
    with pytest.raises(AssertionError):
        PS.prepare(broken, tok)


def rate(p: float, half: float = 0.04) -> list[float]:
    return [p, max(0.0, p - half), min(1.0, p + half)]


def fake(moved_abs: float, moved_rel: float, slot: float = 0.4, slot_long: float = 0.4, n: int = 400, la: str = "50"):
    out = {}
    for lv, moved, role in (("e5-abs", moved_abs, "token"), ("e5-rel", moved_rel, "back"), ("e5-still", 0, "token"),
                            ("e5-long", 0, "token")):  # fmt: skip
        s = slot_long if lv == "e5-long" else slot
        out[f"RL|all|{lv}|last|{la}|dissoc"] = {"n": n, "k": {role: round(moved * n), "position": round(s * n)},
                                                "position": rate(s), role: rate(moved)}  # fmt: skip
    return out


def test_v6_hypotheses():
    m = {"family_roles": ["RL", "DL", "RR"]}
    x = PS.v6_tests(m, fake(0.05, 0.25))
    assert x["H-rel"] and not x["H-abs"] and x["H-ordinal"] and not x["H-long"]
    x = PS.v6_tests(m, fake(0.25, 0.05))
    assert x["H-abs"] and not x["H-rel"]
    x = PS.v6_tests(m, fake(0.1, 0.1, slot_long=0.2))
    assert not x["H-rel"] and not x["H-abs"] and x["H-long"]
    x = PS.v6_tests(m, fake(0.45, 0.1))  # the moved statement as frequent as the slot: not ordinal
    assert not x["H-ordinal"]
    assert not PS.v6_tests(m, fake(0.05, 0.25, n=20))["H-rel"]  # below the n the rule needs
    # another target's primary layers come from the manifest
    assert PS.v6_tests(m | {"primary_layers": [18]}, fake(0.05, 0.25, la="18"))["H-rel"]
    assert not PS.v6_tests(m, fake(0.05, 0.25, la="18"))["H-rel"]
