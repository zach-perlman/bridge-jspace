"""pointer_v5: the same scenes with digit and colour-word answers, 5 and 8 statements; pointer_swap's word reads and
its pre-registered pointer_v5 tests."""

import pytest

from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import pointer_v4 as P4
from scripts import pointer_v5 as V
from scripts import suite_v1 as S


def _first(which: str, n: int = 20) -> dict:
    """The set's generator output with its first n scenes per topic and list length (the same draws as the full set)."""
    split = P4.load_split()
    if split is None:
        pytest.skip("no data/pointer_v4/split.json")
    old = V.SETS
    V.SETS = {**old, which: {**old[which], "n": n}}
    try:
        return V.generate(which, split)
    finally:
        V.SETS = old


@pytest.fixture(scope="module")
def items():
    return _first("main")


@pytest.mark.parametrize("which", list(V.SETS))
def test_sets_reproduce_their_files(which):
    """Each set's first scenes regenerate its committed files' first items (verify does every item)."""
    for label, (path, its, _) in _first(which, 5).items():
        if not path.exists():
            pytest.skip(f"{path} not made")
        assert PV.load_file(path)[: len(its)] == its, label


def test_long_sets():
    l8, l12 = _first("len8"), _first("len12")
    assert {it["level"] for _, its, _ in l8.values() for it in its} == {"e8-digit", "e8-word"}
    assert {it["level"] for _, its, _ in l12.values() for it in its} == {"e12-word"}
    for _, its, _ in l12.values():
        for it in its:
            pd, vals, sl = it["sources"]["dissoc"]["predictions"], it["digits"], it["slots"]
            assert it["n_entities"] == len(vals) == len(set(vals)) == 12 and it["answer_kind"] == "colour16"
            assert set(vals) <= set(V.COLOURS16) and pd["value"] in V.COLOURS16 and pd["value"] not in vals
            assert len(set(pd.values())) == 4 and pd["position"] == vals[sl["position"]]
            assert pd["identity"] == vals[sl["identity"]]
            assert it["family"] == "DL" or it["hop2"]["kind"] == "colour16"  # memory -> prompt's lookup step alone
    main = {it["context"] for _, its, _ in _first("main").values() for it in its}
    assert not main & {it["context"] for _, its, _ in l8.values() for it in its}, "len8 repeats main's scenes"


def test_n_statements():
    assert [PS.n_statements(x) for x in ("e5f0", "e5-off", "e5more", "e8-digit", "e12-word")] == [5, 5, 5, 8, 12]


def test_digit_and_word_share_the_scene(items):
    scenes: dict = {}
    for _, its, _ in items.values():
        for it in its:
            scenes.setdefault((it["family"], it["scene"]), {})[it["type"]] = it
    for pair in scenes.values():
        d, w = pair["digit"], pair["word"]
        assert d["entities"] == w["entities"] and d["slots"] == w["slots"] and d["n_entities"] == w["n_entities"]
        assert all(v in V.DIGITS for v in d["digits"]) and all(v in V.COLOURS for v in w["digits"])
        assert w["answer_kind"] == "colour" and d["answer_kind"] == "digit"


def test_predictions(items):
    for label, (_, its, _) in items.items():
        for it in its:
            pd, vals, sl = it["sources"]["dissoc"]["predictions"], it["digits"], it["slots"]
            assert len(vals) == it["n_entities"] == int(it["level"][1])
            assert len(set(pd.values())) == 4 and pd["value"] not in vals, label
            assert pd["position"] == vals[sl["position"]] and pd["none"] == it["answer"] == vals[sl["query"]]


def test_colour_judge():
    assert V.said("Red.", "colour") == "red"
    assert V.said("The drawer is green.\nmore", "colour") == "green"
    assert V.said("3", "digit") == "3"
    assert V.said("Gold.", "colour16") == "gold" and V.said("Gold, not red.", "colour") == "red"  # main's 11 unchanged


def test_word_items_read_without_the_space(items):
    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")
    w = next(it for _, its, _ in items.values() for it in its if it["type"] == "word")
    d = next(it for _, its, _ in items.values() for it in its if it["type"] == "digit")
    pw, pd = PS.prepare(w, tok), PS.prepare(d, tok)
    space = S.ids(tok, " ")
    assert pd["read_ids"]["base"][-1:] == space and pw["read_ids"]["base"][-1:] != space
    for p in (pw, pd):
        n = len(p["read_ids"]["base"])
        assert p["groups"]["last"] == [n - 2, n - 1]
    for label, (_, its, _) in items.items():
        for it in its[:3]:
            assert all(V.check_item(tok, it).values()), (label, it["id"], V.check_item(tok, it))


def test_v5_hypotheses():
    m = {"family_roles": ["RL", "DL", "RR"], "levels": ["e5-word", "e8-digit"], "domains": ["a", "b", "c"]}

    def v(verdict, n_ok=True):
        return {"verdict": verdict, "rule_reachable": n_ok}

    verdicts = {"RL|all|e5-word|last|50": v("position"), "RL|domain:a|e5-word|last|50": v("position"),
                "RL|domain:b|e5-word|last|50": v("position"), "RL|domain:c|e5-word|last|50": v("mixed"),
                "RL|all|e8-digit|last|48": v("position"), "RL|domain:a|e8-digit|last|48": v("position"),
                "RL|domain:b|e8-digit|last|48": v("position", False)}  # fmt: skip
    x = PS.v5_tests(m, verdicts)
    assert x["e5-word"]["holds"] and not x["e8-digit"]["holds"]
