"""exp11's pure aggregation helpers (no model)."""

from scripts.exp11_bridge_vs_answer_by_layer.experiment import aggregate, emergence_layer, subsets


def test_emergence_needs_a_run_of_top1_layers():
    layers = [10, 11, 12, 13, 14, 15]
    assert emergence_layer([1, 3, 1, 1, 1, 2], layers, run=3) == 12  # the lone top-1 at 10 does not count
    assert emergence_layer([1, 3, 1, 1, 1, 2], layers, run=1) == 10
    assert emergence_layer([2, 1, 1, 2, 1, 1], layers, run=3) is None


def _row(name, bridge_word, distr_word, bridge_pool, answer_pool):
    n = len(bridge_word)
    return {
        "name": name,
        "reader": "jlens",
        "layers": list(range(n)),
        "bridge_word": bridge_word,
        "distractor_word": distr_word,
        "answer_word": [999] * n,
        "swap_answer_word": [999] * n,
        "bridge_pool": bridge_pool,
        "distractor_pool": [2] * n,
        "answer_pool": answer_pool,
        "swap_answer_pool": None if answer_pool is None else [2] * n,
    }


def test_aggregate_band_shares_and_order():
    meta = [
        {"name": "a", "status": "eligible", "label": "J-mediated", "ends_with_space": True},
        {"name": "b", "status": "eligible", "label": "neither", "ends_with_space": False},
        {"name": "c", "status": "eligible", "label": "neither", "ends_with_space": False},
        {"name": "d", "status": "clean_wrong", "label": "", "ends_with_space": False},
    ]
    rows = [
        # a: bridge top-1 from layer 1 on, answer from layer 2 on -> bridge first, lag +1
        _row("a", [9, 1, 3, 7, 7], [8, 8, 8, 8, 8], [3, 1, 1, 1, 1], [5, 5, 1, 1, 1]),
        # b: answer top-1 from 0 (runs 0-2), bridge from 2 (runs 2-4) -> answer first, lag -2
        _row("b", [9, 9, 9, 2, 2], [1, 1, 1, 1, 1], [2, 2, 1, 1, 1], [1, 1, 1, 1, 1]),
        # c: bridge emerges at 0, answer never -> bridge_only; no answer pool would skip it entirely
        _row("c", [1, 1, 1, 1, 1], [9, 9, 9, 9, 9], [1, 1, 1, 2, 2], [2, 2, 2, 2, 2]),
        _row("d", [1, 1, 1, 1, 1], [9, 9, 9, 9, 9], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),
    ]
    out = aggregate(rows, meta, ["jlens"], {"b": [1, 2], "off": [90, 99]}, emerge_run=3, n_boot=200, seed=0)
    el = out["eligible"]["jlens"]
    assert out["eligible"]["n"] == 3
    assert set(el["bands"]) == {"b"}  # a band outside the model's layers is skipped
    assert el["bands"]["b"]["bridge_pool_top1"]["mean"] == round((1 + 0.5 + 1) / 3, 4)  # a 2/2, b 1/2, c 2/2
    assert el["bands"]["b"]["bridge_above_distractor"]["mean"] == round((1 + 0 + 1) / 3, 4)  # a yes, b no, c yes
    assert el["bands"]["b"]["answer_pool_top1"]["mean"] == round((0.5 + 1 + 0) / 3, 4)
    o = el["order"]
    assert (o["both"], o["bridge_only"], o["answer_only"], o["neither"]) == (2, 1, 0, 0)
    assert o["bridge_first"]["mean"] == 0.5 and o["same_layer"] == 0.0 and o["median_lag_layers"] == -0.5  # +1, -2
    assert out["eligible_j_mediated"]["n"] == 1 and out["all"]["n"] == 4


def test_subsets_only_eligible_in_splits():
    meta = [{"name": "x", "status": "clean_wrong", "label": "J-mediated", "ends_with_space": True}]
    s = subsets(meta)
    assert s["eligible_j_mediated"] == [] and s["all"] == ["x"]
