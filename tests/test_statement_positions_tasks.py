"""statement_positions' tasks_v2 PP / PM adapter (no model): the prose context split into picks and lockers by role."""

import pytest

from scripts import statement_positions as SP


def _item(**kw):
    base = {"id": "PP-L0-0000", "family": "PP", "bridge": "eagle", "cf_bridge": "cat",
            "context": "The locker of the eagle is 3. Ivy picked the cat. Clara picked the eagle. The locker of the cat is 6.",
            "question": "Which locker belongs to Clara's pick?"}  # fmt: skip
    return {**base, **kw}


def test_tasks_statements_roles():
    st = SP.statements(_item())
    assert st["holder"] == "Clara"
    assert st["bind_bridge"] == "Clara picked the eagle."
    assert st["bind_other"] == ["Ivy picked the cat."]
    assert st["lookup_bridge"] == "The locker of the eagle is 3."
    assert st["lookup_x"] == "The locker of the cat is 6."
    assert " ".join(st["all"]) == _item()["context"]


def test_tasks_statements_reject_a_wrong_holder():
    with pytest.raises(AssertionError):
        SP.statements(_item(question="Which locker belongs to Ivy's pick?"))  # Ivy picked the cat, not the eagle
    with pytest.raises(AssertionError):
        SP.statements(_item(context="The weather was fine. Clara picked the eagle. The locker of the eagle is 3."))


@pytest.mark.parametrize("fmt", ["table", "json"])
def test_structured_position_sets_on_generated_items(fmt):
    """Tables and tool-output JSON (d1_formats_v1): the pick row / object, the bridge's cell, the locker rows; the
    usual checks (the counterfactual changes only the picks and changes the bridge's cell) hold."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T

    try:
        tok = SP.load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    items = [it for it in T.load("d1_formats_v1") if it["format"] == fmt and it["word"] == "PP"][:6]
    assert items
    for it in items:
        c = {**it, **T.prepare(it, tok), "family": "PP", "rendered": T.render(tok, it), "context_text": it["context"]}
        enc = raw_encoding(tok, c["rendered"], offsets=True)
        sets, _ = SP.position_sets(c, c["rendered"], enc["offset_mapping"])
        dec = lambda key, sets=sets, c=c: tok.decode([c["ids"]["clean"][i] for i in sets[key]])  # noqa: E731
        assert dec("bridge_word").strip(' "') == c["bridge"]
        holder = it["start_desc"].removesuffix("'s pick")
        assert holder in dec("bind_bridge") and c["bridge"] in dec("bind_bridge")
        assert c["bridge"] in dec("lookup_bridge") and c["cf_bridge"] in dec("lookup_x")
        assert not set(sets["bind_bridge"]) & set(sets["lookup_bridge"])
