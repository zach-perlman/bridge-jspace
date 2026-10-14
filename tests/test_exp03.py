"""exp03_brew_swaps: swap targets, the off-path control and answer reading, on the pinned brew items (no model)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.pins import brew_items
from scripts.exp03_brew_swaps import answer_colour, control_pair, regime_positions, swap_target


def test_swap_target_predicts_a_distinct_answer():
    for index, item in enumerate(brew_items()):
        x = swap_target(item, index)
        if x is None:
            continue
        f, inter = item["table"], item["intermediates"][0]
        assert x not in (item["start"], inter, item["answer"])
        assert f[x]["stir"] not in (item["answer"], inter, x, item["start"])
        assert f[inter]["stir"] == item["answer"]  # the bank's own two-step chain
        assert f[item["start"]]["stir"] == inter


def test_control_pair_is_off_trajectory():
    for index, item in enumerate(brew_items()):
        pair = control_pair(item, index)
        if pair is not None:
            a, b = pair
            assert a != b
            assert {a, b} <= set(item["off_trajectory"])


def test_answer_colour_reads_the_first_colour_on_the_first_line():
    palette = ["black", "green", "red"]
    assert answer_colour(" Black.\nQuestion: green", palette) == "black"
    assert answer_colour("\n\nred", palette) == "red"
    assert answer_colour(" none of these", palette) is None


def test_regimes_pick_tokens_inside_their_region():
    offsets = [(0, 0), (0, 5), (5, 10), (10, 15), (15, 20)]
    regions = {"rules": (5, 12), "stir_line": (0, 1), "start_line": (15, 20), "after_start": (20, 20)}
    assert regime_positions("rules", offsets, regions) == [2, 3]
    assert regime_positions("last", offsets, regions) == [4]
    assert regime_positions("all", offsets, regions) == [1, 2, 3, 4]


def test_start_and_answer_targets_predict_new_answers():
    from scripts.exp03_brew_swaps import answer_target, start_target

    for index, item in enumerate(brew_items()):
        f, path = item["table"], {item["start"], item["intermediates"][0], item["answer"]}
        s2 = start_target(item, index)
        if s2 is not None:
            assert s2 not in path
            assert f[f[s2]["stir"]]["stir"] not in path
        a2 = answer_target(item, index)
        if a2 is not None:
            assert a2 in item["off_trajectory"]


def test_add_direction_edits_only_its_positions():
    import torch

    from scripts.exp03_brew_swaps import AddDirection

    h = torch.randn(5, 8)
    d = torch.nn.functional.normalize(torch.randn(8), dim=0)
    out = AddDirection(d, 0.1, [2, 4])(h)
    torch.testing.assert_close(out[[0, 1, 3]], h[[0, 1, 3]])
    torch.testing.assert_close((out[2] - h[2]).norm(), 0.1 * h[2].norm())
