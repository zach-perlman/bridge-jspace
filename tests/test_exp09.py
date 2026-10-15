"""exp09_bind_recall: the counterfactual prompts rewrite one binding and keep every country (no model)."""

from collections import Counter

from bridge_jspace import pins
from scripts.exp09_bind_recall import changed_tokens, role_of, variants


def words_changed(a: str, b: str) -> list[tuple[str, str]]:
    return [(x, y) for x, y in zip(a.split(), b.split(), strict=True) if x != y]


def test_variants_rewrite_one_binding():
    items = pins.bind_recall_items()
    for index, item in enumerate(items):
        if index % 19:
            continue
        v = variants(item, index)
        cf, off = words_changed(item["prompt"], v["cf"]), words_changed(item["prompt"], v["off"])
        assert Counter(item["prompt"].split()) == Counter(v["off"].split())  # O swaps two holders' countries
        assert {w.rstrip(".") for pair in off for w in pair} == {item["target"], item["third"]}
        if item["family"] == "R":
            assert len(cf) == 1 and cf[0][0] == item["cue"]  # only the city changes
        else:
            assert Counter(item["prompt"].split()) == Counter(v["cf"].split())  # the same countries, rebound
            assert {w.rstrip(".") for pair in cf for w in pair} == {item["bridge"], item["target"]}


def test_changed_tokens_and_roles():
    assert changed_tokens([1, 2, 3], [1, 9, 3]) == [1]
    assert changed_tokens([1, 2, 3], [1, 9, 8]) == [1, 2]
    assert changed_tokens([1, 2], [1, 2, 3]) is None
    assert changed_tokens([1, 2], [1, 2]) is None
    item = {"bridge": "France", "target": "Peru"}
    assert role_of("lima", item) == "b" and role_of("paris", item) == "A" and role_of(None, item) == "none"
