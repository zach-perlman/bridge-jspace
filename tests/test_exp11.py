"""exp11's pure aggregation helpers (no model)."""

from scripts.exp11_bridge_vs_answer_by_layer.experiment import aggregate, first_layer_within, peak_layer, subsets


def test_peak_layer_earliest_on_ties():
    assert peak_layer([5, 2, 2, 9], [10, 11, 12, 13]) == 11


def test_first_layer_within():
    assert first_layer_within([50, 12, 9, 1], [0, 1, 2, 3], k=10) == 2
    assert first_layer_within([50, 12], [0, 1], k=10) is None


def _row(name, reader, bridge, distr, answer, bridge_pool):
    n = len(bridge)
    return {
        "name": name,
        "reader": reader,
        "layers": list(range(n)),
        "bridge_word": bridge,
        "distractor_word": distr,
        "answer_word": answer,
        "swap_answer_word": [999] * n,
        "bridge_pool": bridge_pool,
        "distractor_pool": [2] * n,
        "answer_pool": None,
        "swap_answer_pool": None,
    }


def test_aggregate_band_shares_and_order():
    meta = [
        {"name": "a", "status": "eligible", "label": "J-mediated", "ends_with_space": True},
        {"name": "b", "status": "eligible", "label": "neither", "ends_with_space": False},
        {"name": "c", "status": "clean_wrong", "label": "", "ends_with_space": False},
    ]
    rows = [
        # a: bridge top-1 in its pool on layers 1-2, peaks at layer 1; answer reaches rank 5 at layer 3 -> lag +2
        _row("a", "jlens", [9, 1, 3, 7], [8, 8, 8, 8], [900, 500, 50, 5], [3, 1, 1, 2]),
        # b: bridge never top-1; peaks at layer 3; answer within top 10 from layer 0 -> lag -3
        _row("b", "jlens", [9, 9, 9, 2], [1, 1, 1, 1], [4, 4, 4, 1], [2, 2, 2, 2]),
        _row("c", "jlens", [1, 1, 1, 1], [9, 9, 9, 9], [1, 1, 1, 1], [1, 1, 1, 1]),
    ]
    out = aggregate(rows, meta, ["jlens"], band=[1, 2], hit_k=10, n_boot=200, seed=0)
    el = out["eligible"]["jlens"]
    assert out["eligible"]["n"] == 2
    assert el["bridge_pool_top1_band"]["mean"] == 0.5  # a: 2/2 band layers, b: 0/2
    assert el["bridge_above_distractor_band"]["mean"] == 0.5  # a: bridge < distractor on 1,2; b: never
    assert el["order"]["n"] == 2
    assert el["order"]["bridge_peaks_first"]["mean"] == 0.5
    assert el["order"]["median_lag_layers"] == -0.5
    assert "answer_pool_top1_band" not in el  # answer pools are None in these rows
    assert out["eligible_j_mediated"]["n"] == 1 and out["all"]["n"] == 3


def test_subsets_only_eligible_in_splits():
    meta = [{"name": "x", "status": "clean_wrong", "label": "J-mediated", "ends_with_space": True}]
    s = subsets(meta)
    assert s["eligible_j_mediated"] == [] and s["all"] == ["x"]
