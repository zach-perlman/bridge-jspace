"""exp09_bind_recall: the counterfactual prompts change one word, the right one (no model)."""

from bridge_jspace import pins
from scripts.exp09_bind_recall import changed_token, role_of, variants
from scripts.exp09_make_items import CAPITALS


def words_changed(a: str, b: str) -> list[tuple[str, str]]:
    return [(x, y) for x, y in zip(a.split(), b.split(), strict=True) if x != y]


def test_variants_change_one_word_each():
    items = pins.bind_recall_items()
    for index, item in enumerate(items[:: len(items) // 40]):
        v = variants(item, index)
        cf, off = words_changed(item["prompt"], v["cf"]), words_changed(item["prompt"], v["off"])
        assert len(cf) == 1 and len(off) == 1, item["name"]
        if item["family"] == "R":
            assert cf[0][0] == item["cue"]  # the city
        else:
            assert cf[0] == (f"{item['bridge']}.", f"{item['target']}.")  # the queried person's country
        new_off = off[0][1].rstrip(".")
        assert new_off in CAPITALS and new_off not in (item["bridge"], item["target"], *item["context_countries"])


def test_changed_token_and_roles():
    assert changed_token([1, 2, 3], [1, 9, 3]) == 1
    assert changed_token([1, 2, 3], [1, 9, 8]) is None
    assert changed_token([1, 2], [1, 2, 3]) is None
    item = {"bridge": "France", "target": "Peru"}
    assert role_of("lima", item) == "b" and role_of("paris", item) == "A" and role_of(None, item) == "none"
