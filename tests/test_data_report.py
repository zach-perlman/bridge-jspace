"""The data report on the repo's real (pinned) files: the counts data/README.md quotes."""

from scripts.data_report import build_report, format_report


def test_report_counts_match_readme():
    r = build_report()
    ps, le, ep = r["probe_swap"], r["lens_eval_multihop"], r["entity_prompts"]
    assert (ps["n"], ps["n_categories"], ps["categories_with_one_item"]) == (90, 36, 23)
    assert ps["status"] == {"eligible": 77, "clean_wrong": 13}
    assert ps["eligible"]["labels"] == {"neither": 49, "J-mediated": 25, "both": 2, "non-J": 1}
    assert (le["n"], le["same_prompt_as_probe_swap"]) == (93, 30)
    assert ep["entities"] == 97
    assert "probe-swap two-hop items" in format_report(r)
