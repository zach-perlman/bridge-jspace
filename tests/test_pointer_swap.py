"""pointer_swap's analysis: the pre-registered rule's n threshold, the verdict logic, Newcombe intervals, display names."""

import pytest

from scripts import pointer_swap as PS


def cell(n: int, **k: int) -> dict:
    """A rates cell as roles_of builds it, from role counts."""
    rows = [{"role": r} for r, c in k.items() for _ in range(c)]
    rows += [{"role": "none"}] * (n - len(rows))
    return PS.roles_of(rows)


def test_same_control_bound_needs_35_items():
    moved = {"position": 0}
    for n, expect in ((34, "damage"), (35, "position")):
        d = cell(n, position=n - 2)
        same = cell(n, **moved)
        assert PS.verdict("RL", d, same, {}, 5) == expect, n


def test_one_same_change_is_damage_at_50_not_at_100():
    d50, d100 = cell(50, position=40), cell(100, position=80)
    assert PS.verdict("RL", d50, cell(50, position=1), {}, 5) == "damage"
    assert PS.verdict("RL", d100, cell(100, position=1), {}, 5) == "position"


def test_verdict_none_mixed_and_chance_bar():
    same = cell(100)
    assert PS.verdict("RL", cell(100, position=10), same, {}, 5) == "none"  # changed lower bound < 0.20
    assert PS.verdict("RL", cell(100, position=30, identity=28), same, {}, 5) == "mixed"
    assert PS.verdict("RL", cell(100, position=30, identity=5), same, {}, 5) == "position"
    assert PS.verdict("RL", cell(100, position=30, identity=5), same, {"position": 0.5}, 5) == "mixed"


def test_rr_ignores_value():
    same = cell(100)
    assert PS.verdict("RR", cell(100, identity=60), same, {}, 5) == "identity"


def test_newcombe():
    d, lo, hi = PS.newcombe(30, 100, 30, 100)
    assert d == 0
    assert lo < 0 < hi
    assert lo == pytest.approx(-hi, abs=1e-9)
    d, lo, hi = PS.newcombe(60, 100, 20, 100)
    assert d == pytest.approx(0.4)
    assert 0.2 < lo < d < hi < 0.6


def test_plain_names():
    assert PS.plain("RL and RR, `family == 'RL'`") == "memory → prompt and memory → memory, `family == 'RL'`"
    assert PS.plain("item animals-RL-e5f0-0001") == "item animals-RL-e5f0-0001"  # ids keep their codes
    assert "W" in PS.rule_plain("verdict X in {identity}") and "bridge alt's statement" in PS.rule_plain("identity")
    assert PS.plain("RK and DK") == "memory → prompt and named → prompt"  # code_pointer_v1's families
    fenced = "```\nRL `family == 'RL'`\n```\nRL"  # a ``` fence is not a code span
    assert PS.plain(fenced) == "```\nmemory → prompt `family == 'RL'`\n```\nmemory → prompt"


def test_token_candidate():
    same = cell(100)
    cands = ("identity", "position", "token", "value")
    assert PS.verdict("RL", cell(100, token=40, position=5), same, {}, 5, cands, 1) == "token"
    assert PS.verdict("RL", cell(100, token=30, position=28), same, {}, 5, cands, 1) == "mixed"


def test_eligibility_keyed_by_set(tmp_path):
    import json

    rows = [
        {"label": "main/animals_RL_e5f0", "id": "x-0", "correct": True},
        {"label": "dev/animals_RL_e5f0", "id": "x-0", "correct": False},  # the same id in another set
        {"label": "main/animals_RL_e5f0", "id": "x-1", "correct": False},
    ]
    f = tmp_path / "items.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    assert PS.eligible_ids(f) == {("main", "x-0")}


def test_ref_contrast_pairs_by_scene():
    rows = []
    for i in range(60):
        for lv, val in (("e5-ref", i < 40), ("e5-pln", i < 10)):
            rows.append({"source": "dissoc", "group": "last", "family": "RL", "level": lv, "layer": 56,
                         "name": f"animals-RL-{lv}-{i:04d}", "role": "value" if val else "none"})  # fmt: skip
    m = {"levels": ["e5-ref", "e5-pln"]}
    out = PS.ref_contrasts(m, rows, {"RL|all|e5-pln|last|56": {"verdict": "value"}})
    c = out["RL|e5-ref|last|56"]
    assert c["n_pairs"] == 60
    assert c["ref_value"] == pytest.approx(40 / 60, abs=1e-3)
    assert c["pln_value"] == pytest.approx(10 / 60, abs=1e-3)
    assert c["label"] == "reflexive"
    assert c["interpretable"]


def test_base_level():
    assert PS.base_level("e5-off") == "e5"
    assert PS.base_level("e5f0-xlang") == "e5f0"
    assert PS.base_level("e5f0") == "e5f0"
