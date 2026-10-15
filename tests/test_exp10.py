"""exp10's pure aggregation helpers (no model)."""

from scripts.exp10_lens_sanity.experiment import aggregate, item_scores


def _rows(reader, ranks_by_item):
    return [
        {"name": name, "reader": reader, "intermediate": f"form{i}", "min_rank": r}
        for name, ranks in ranks_by_item.items()
        for i, r in enumerate(ranks)
    ]


def test_item_found_if_any_form_is():
    rows = _rows("jlens", {"rings": [12, 3], "cube": [12, 15], "moon": [0]})  # '5' missed, 'five' found
    assert item_scores(rows, "jlens", 10, "any") == {"rings": 1.0, "cube": 0.0, "moon": 1.0}
    assert item_scores(rows, "jlens", 10, "fraction") == {"rings": 0.5, "cube": 0.0, "moon": 1.0}


def test_aggregate_reports_both_rules():
    meta = [{"name": n, "model_correct": True, "all_single_token": True} for n in ("rings", "cube", "moon")]
    rows = _rows("jlens", {"rings": [12, 3], "cube": [12, 15], "moon": [0]}) + _rows(
        "logit", {"rings": [50, 50], "cube": [50, 50], "moon": [50]}
    )
    out = aggregate(rows, meta, ["logit", "jlens"], [10], n_boot=200, seed=0)
    assert out["pass_at_k"]["all"]["jlens"][10]["mean"] == round(2 / 3, 4)
    assert out["pass_at_k_fraction"]["all"]["jlens"][10]["mean"] == 0.5
    assert out["diff_vs_logit"]["all"]["jlens"][10]["mean"] == round(2 / 3, 4)


def test_bridge_labels():
    from scripts.exp10_lens_sanity.experiment import bridge_in_prompt, bridge_kind

    assert bridge_kind(["6", "six"]) == "number" and bridge_kind(["3", "three", "third"]) == "number"
    assert bridge_kind(["H"]) == "letter" and bridge_kind(["Brazil"]) == "word"
    assert bridge_in_prompt("the time of day when plants photosynthesize", ["day"])
    assert not bridge_in_prompt("The position in the alphabet of the chemical symbol", ["H", "C"])  # inside words
