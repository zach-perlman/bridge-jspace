"""exp04_brew_patch: counterfactual tables, their answers and the patch positions, on the pinned brew items (no model)."""

import pytest
import torch

from bridge_jspace.pins import brew_fresh_items, brew_items
from scripts.exp03_brew_swaps import swap_target
from scripts.exp04_brew_patch import PatchFrom, counterfactuals, group_positions, rewrite_rules, rule_table


def test_rule_table_reads_the_items_table():
    for item in (*brew_items(), *brew_fresh_items()):
        assert rule_table(item["prompt"]) == {c: row["stir"] for c, row in item["table"].items()}


def test_rewrite_rules_changes_only_the_named_lines():
    prompt = "rules:\nA blue potion turns green when stirred.\nAn orange potion turns red when stirred.\nYou stir"
    assert rewrite_rules(prompt, {"orange": "blue"}) == prompt.replace(
        "orange potion turns red", "orange potion turns blue"
    )
    with pytest.raises(AssertionError):
        rewrite_rules(prompt, {"purple": "red"})


def test_counterfactual_answers_follow_their_tables():
    for items in (brew_items(), brew_fresh_items()):
        for index, item in enumerate(items):
            cfs = counterfactuals(item, index)
            if cfs is None:
                continue
            r = cfs["roles"]
            assert r["X"] == swap_target(item, index)
            assert r["X"] not in (r["S"], r["I"], r["A"])
            assert r["b"] not in (r["S"], r["I"], r["A"], r["X"])
            assert r["c"] not in (r["S"], r["I"], r["A"], r["X"], r["b"])
            base = rule_table(item["prompt"])
            cf = rule_table(rewrite_rules(item["prompt"], cfs["cf"]["outputs"]))
            off = rule_table(rewrite_rules(item["prompt"], cfs["off"]["outputs"]))
            assert base[base[r["S"]]] == r["A"]
            assert cf[cf[r["S"]]] == r["c"] == cfs["cf"]["answer"]
            assert base[r["X"]] == r["b"]  # X carried in as the step, then B's table: b
            assert off[off[r["S"]]] == r["A"] == cfs["off"]["answer"]
            assert {c for c in base if cf[c] != base[c]} == {r["S"], r["X"]}
            assert {c for c in base if off[c] != base[c]} == set(cfs["off"]["lines"])
            assert not set(cfs["off"]["lines"]) & {r["S"], r["I"], r["X"]}
            assert cfs["cf"]["lines"][0] == r["S"]  # rule_path patches the path rule


def test_groups_pick_their_lines_and_regions():
    offsets = [(0, 0), (0, 4), (4, 9), (9, 14), (14, 20), (20, 25)]
    regions = {"rules": (0, 14), "stir_line": (14, 15), "start_line": (14, 20), "after_start": (20, 25)}
    lines = [(4, 9), (9, 14)]
    assert group_positions("rule_path", offsets, regions, lines) == [2]
    assert group_positions("rules", offsets, regions, lines) == [2, 3]
    assert group_positions("start_line", offsets, regions, lines) == [4]
    assert group_positions("after_start", offsets, regions, lines) == [5]
    assert group_positions("last", offsets, regions, lines) == [5]


def test_patch_from_replaces_only_its_positions():
    h, source = torch.randn(5, 8), torch.randn(5, 8)
    patch = PatchFrom(source, [1, 3])
    out = patch(h)
    assert torch.equal(out[[1, 3]], source[[1, 3]])
    assert torch.equal(out[[0, 2, 4]], h[[0, 2, 4]])
    assert patch.patch_ratio > 0
