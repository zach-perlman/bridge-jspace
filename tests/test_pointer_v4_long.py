"""pointer_v4's long set: neutral filler (no entity, cue word or digit), seeded per scene, appended after the list in
the item and in every source prompt (no tokenizer)."""

import pytest

from scripts import pointer_v4 as P


def test_filler_is_neutral_and_seeded():
    P.check_filler_words()
    a, b = P.long_filler(846, "animals-e5f0-0001"), P.long_filler(846, "animals-e5f0-0002")
    assert a == P.long_filler(846, "animals-e5f0-0001") and a != b
    assert a.startswith(" ") and a.count(".") == P.LONG_FILLER


def test_long_items_append_the_same_filler_everywhere():
    if not (P.DATA / "seed2").exists():
        pytest.skip("pointer_v4 seed2 data not present")
    for _label, (_path, items, _note) in P.make_long("long").items():
        assert len(items) == P.SETS["long"]["n"]
        for it in items[:5]:
            assert it["context"] == " ".join(it["statements"]) + it["after"]
            assert it["n_filler"] == P.LONG_FILLER
            for s in it["sources"].values():
                assert s["context"].endswith(it["after"]) and s["context"].count(it["after"]) == 1
