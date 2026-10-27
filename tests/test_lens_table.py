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


HEAD = "eval,lens,item,intermediate,layer,rank,n_candidates\n"


def test_a_glob_over_several_fit_records_reads_the_newest_only(tmp_path, monkeypatch):
    monkeypatch.setattr(lt, "REPO", tmp_path)
    monkeypatch.setattr(lt, "_CACHE", {})
    for stamp, r in (("20261022-000000", 7), ("20261023-000000", 2)):
        (tmp_path / f"fit_{stamp}").mkdir()
        (tmp_path / f"fit_{stamp}/eval_ranks.csv").write_text(HEAD + f"typo,mine,t,w,0,{r},3\n")
    files, ranks, _ = lt.find(lt.Row("qwen3-32b", "mine", "x", "J++", "s", "r", ("fit_*/eval_ranks*.csv",)))
    assert files == ["fit_20261023-000000/eval_ranks.csv"] and ranks == [("typo", "mine", "t", "w", 0, 2)]


def test_a_lens_graded_on_other_items_than_the_logit_run_is_compared_on_the_shared_items(tmp_path, monkeypatch):
    """Our fit's evaluate and the lens_eval run grade the model separately: one item each is theirs alone. The lens's
    own macro keeps its items; the difference to the logit lens is taken on the shared ones, at the layers scored
    (OLMo: every 3rd, here 0) and at every layer both have (0-1)."""
    monkeypatch.setattr(lt, "REPO", tmp_path)
    monkeypatch.setattr(lt, "_CACHE", {})
    jpp, logit = [], []
    for ev in lt.EVALS:  # shared: the lens names it at both layers, the logit lens at layer 1 only
        jpp += [f"{ev},mine,{ev}-1,w,0,1,3", f"{ev},mine,{ev}-1,w,1,1,3"]
        logit += [f"{ev},logit,{ev}-1,w,0,500,3", f"{ev},logit,{ev}-1,w,1,1,3"]
    jpp += ["typo,mine,typo-x,w,0,500,3", "typo,mine,typo-x,w,1,500,3"]  # the fit's run only: a miss
    logit += ["typo,logit,typo-y,w,0,1,3", "typo,logit,typo-y,w,1,1,3"]  # the lens_eval run only: a hit
    logit += [f"{ev},plain,{ev}-1,w,0,1,3" for ev in lt.EVALS] + ["typo,plain,typo-y,w,0,1,3"]  # the logit's items
    (tmp_path / "fit_20261023-000000").mkdir()
    (tmp_path / "fit_20261023-000000/eval_ranks.csv").write_text(HEAD + "\n".join(jpp) + "\n")
    (tmp_path / "ev").mkdir()
    (tmp_path / "ev/eval_ranks_g0.csv").write_text(HEAD + "\n".join(logit) + "\n")
    lrow = lt.Row("olmo-3-7b-instruct", lt.LOGIT, "logit lens", "logit lens", "-", "-", ("ev/eval_ranks*.csv",))
    row = lt.Row("olmo-3-7b-instruct", "mine", "ours", "J++", "s", "r", ("fit_*/eval_ranks*.csv",))
    lrec = lt.score_row(lrow, None)
    rec = lt.score_row(row, lrec)
    assert rec["layers"] == "0" and rec["items"] == 6 and lrec["items"] == 6
    assert rec["macro"] == pytest.approx((4 + 0.5) / 5)  # its own items: typo-x missed
    assert rec["shared_items"] == 5 and "6 here, 6 there, 5 shared" in rec["vs_logit"]
    assert (rec["macro_same"], rec["logit_same"], rec["d_logit"]) == (pytest.approx(1.0), 0.0, pytest.approx(1.0))
    assert rec["common_layers"] == "0-1" and rec["d_logit_common"] == pytest.approx(0.0)
    # a lens of the logit lens's own run: the same items, nothing dropped (logit at layer 0: only typo-y, macro 0.1)
    same = lt.score_row(
        lt.Row("olmo-3-7b-instruct", "plain", "x", "plain J-lens", "s", "r", ("ev/eval_ranks*.csv",)), lrec
    )
    assert "vs_logit" not in same and "shared_items" not in same
    assert same["macro"] == pytest.approx(1.0) and same["d_logit"] == pytest.approx(0.9)
