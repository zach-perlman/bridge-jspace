"""exp12's position alignment and offset selection (no model)."""

import numpy as np

from scripts.exp12_position_map.experiment import (
    band_score,
    best_offset,
    last_content_index,
    load_grids,
    save_grids,
    scores_by_offset,
)


def test_last_content_index_skips_trailing_space():
    assert last_content_index(["Fact", ":", " is"]) == 2
    assert last_content_index(["Fact", ":", " is", " "]) == 2  # published prompts ending in a lone " "


def test_band_score_reads_the_offset_column():
    # 3 layers x 4 positions; offsets -2..+1 (last content token at column 2, a trailing " " at column 3)
    grid = np.array([[5, 1, 1, 9], [5, 2, 1, 9], [5, 1, 3, 9]])
    offsets = [-2, -1, 0, 1]
    assert band_score(grid, offsets, -1, [0, 1, 2]) == 2 / 3
    assert band_score(grid, offsets, 0, [1, 2]) == 0.5
    assert band_score(grid, offsets, -5, [0]) is None


def test_scores_and_best_offset_skip_rare_offsets():
    meta = [{"name": "a", "offsets": [-2, -1, 0]}, {"name": "b", "offsets": [-1, 0, 1]}]
    grids = {
        "a": {"bridge_pool": np.array([[1, 2, 2], [1, 2, 2]])},  # top-1 only at offset -2
        "b": {"bridge_pool": np.array([[3, 1, 1], [3, 1, 2]])},  # offsets -1, 0, +1 -> columns 0, 1, 2
    }
    sc = scores_by_offset(grids, meta, ["a", "b"], "bridge_pool", [-2, -1, 0, 1], [0, 1])
    assert sc == {-2: [1.0], -1: [0.0, 0.0], 0: [0.0, 1.0], 1: [0.5]}
    assert best_offset(sc, min_items=2) == 0  # -2 scores 1.0 but only one prompt reaches it
    assert best_offset(sc, min_items=1) == -2


def test_grids_round_trip(tmp_path):
    g = {"x": {"bridge_pool": np.array([[1, 2]], np.uint8), "bridge_word": np.array([[7, 65535]], np.uint16)}}
    save_grids(tmp_path / "g.npz", g)
    back = load_grids(tmp_path / "g.npz")
    assert back.keys() == g.keys() and all(np.array_equal(back["x"][k], g["x"][k]) for k in g["x"])
