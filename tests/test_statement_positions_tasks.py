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
