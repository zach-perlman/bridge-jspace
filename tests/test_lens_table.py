"""scripts/lens_table.py: its pass@k is the J++ recipe's (checked against the recipe's own output on a committed run),
and the row lookup keeps a lens's numbers to its own files."""

import csv

import pytest

from scripts import lens_table as lt

EXP19 = lt.REPO / "results/exp19_fit_data/fit_v3/eval_wiki64"


def rank(ev, item, inter, layer, r, lens="L"):
    return (ev, lens, item, inter, layer, r)


def test_pass_at_k_takes_the_best_layer_and_weights_items_not_intermediates():
    ranks = [
        rank("multihop", "a", "x", 0, 50),
        rank("multihop", "a", "x", 1, 3),  # best over layers: 3 -> hit
        rank("multihop", "a", "y", 0, 99),  # item a: 1 of 2 intermediates -> 0.5
        rank("multihop", "b", "z", 0, 11),  # item b: miss -> 0.0
    ]
    assert lt.pass_at_k(ranks, [0, 1])["multihop"] == pytest.approx(0.25)
    assert lt.pass_at_k(ranks, [0])["multihop"] == 0.0  # layer 1 not scored
    assert lt.pass_at_k(ranks, [0], k=11)["multihop"] == pytest.approx(0.5)
    assert "macro" not in lt.pass_at_k(ranks, [0, 1])  # four evals missing: no macro (the recipe gives NaN)


def test_macro_is_the_unweighted_mean_of_the_five_evals():
    ranks: list[lt.Rank] = [rank(ev, f"{ev}-1", "w", 0, 1 if ev == "typo" else 500) for ev in lt.EVALS]
    ranks.append(rank("order-ops", "o", "w", 0, 1))  # not a macro eval
    res = lt.pass_at_k(ranks, [0])
    assert res["macro"] == pytest.approx(0.2) and res["order-ops"] == 1.0


@pytest.mark.skipif(not (EXP19 / "eval_ranks.csv").exists(), reason="exp19 rank file not in this checkout")
@pytest.mark.parametrize("k", [1, 10])
def test_matches_the_recipes_own_pass_at_k_on_a_committed_run(k):
    ranks = lt.read_ranks((EXP19 / "eval_ranks.csv").read_text())
    with open(EXP19 / "eval_ranks_pass_at_k.csv") as f:
        want = [d for d in csv.DictReader(f) if d["weighting"] == "item" and int(d["k"]) == k]
    lenses = {d["lens"] for d in want}
    assert lenses == {"jpp_wiki64", "pooled_wiki64"}
    for lens in lenses:
        mine = [x for x in ranks if x[1] == lens]
        got = lt.pass_at_k(mine, {x[4] for x in mine}, k=k)
        for d in want:
            if d["lens"] == lens:
                assert got[d["eval"]] == pytest.approx(float(d["pass_at_k"]), abs=1e-12), (lens, d["eval"])


def test_layers_text():
    assert lt.layers_text(range(63)) == "0-62"
    assert lt.layers_text(range(0, 31, 3)) == "0-30 every 3rd"
    assert lt.layers_text([1, 2, 5]) == "1,2,5"
    assert lt.layers_text([]) == "-"


def test_dedupe_keeps_one_rank_per_layer():
    a = rank("typo", "t", "w", 3, 7, lens="logit")
    assert lt.dedupe([a, a, rank("typo", "t", "w", 4, 7, lens="logit")]) == [a, rank("typo", "t", "w", 4, 7, "logit")]


def test_a_row_takes_its_lens_from_the_first_file_that_has_it(tmp_path, monkeypatch):
    monkeypatch.setattr(lt, "REPO", tmp_path)
    monkeypatch.setattr(lt, "_CACHE", {})
    head = "eval,lens,item,intermediate,layer,rank,n_candidates\n"
    (tmp_path / "a").mkdir()
    (tmp_path / "a/eval_ranks_g0.csv").write_text(head + "typo,other,t,w,0,1,3\n")
    (tmp_path / "a/eval_ranks_g0_pass_at_k.csv").write_text("not ranks")  # skipped
    (tmp_path / "b").mkdir()
    (tmp_path / "b/eval_ranks.csv").write_text(head + "typo,mine,t,w,0,2,3\ntypo,pooled_lens,t,w,0,40,3\n")
    row = lt.Row("qwen3-32b", "mine", "x", "J++", "s", "r", ("a/eval_ranks*.csv", "b/eval_ranks*.csv"), "pooled_lens")
    files, ranks, pooled = lt.find(row)
    assert files == ["b/eval_ranks.csv"] and ranks == [("typo", "mine", "t", "w", 0, 2)]
    assert pooled == [("typo", "pooled_lens", "t", "w", 0, 40)]
    assert lt.find(lt.Row("qwen3-32b", "absent", "x", "J++", "s", "r", ("a/*.csv",))) == ([], [], [])
