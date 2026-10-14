"""The data report on the repo's real (pinned) files: the counts data/README.md quotes."""

from scripts.data_report import build_report, format_report


def test_report_counts_match_readme():
    r = build_report()
    ps, le, ep = r["probe_swap"], r["lens_eval_multihop"], r["entity_prompts"]
    assert (ps["n"], ps["n_categories"], ps["categories_with_one_item"]) == (90, 36, 23)
    assert ps["status"] == {"eligible": 67, "clean_wrong": 16, "multi_token_answer": 7}
    assert ps["eligible"]["labels"] == {"neither": 40, "J-mediated": 25, "both": 1, "non-J": 1}
    assert (le["n"], le["same_prompt_as_probe_swap"]) == (93, 30)
    assert ep["entities"] == 97
    assert "probe-swap two-hop items" in format_report(r)
