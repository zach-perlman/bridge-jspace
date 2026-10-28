"""scripts/x51_heads.py (batch 51, test 51.2): each reader's ablation sites (item construction), the ranking from 49.7's
stored moves on the fit half, the head sets and their matched random controls, the mean capture and mean ablation on
tiny Qwen3.5 (hybrid) and Muse Glimmer models, the rules on planted numbers, the logistic fit and AUC, the seal, and a
planted run through the CPU verdict and view."""

from __future__ import annotations

import json
import math
import random
import re
from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x49_attn as A
from scripts import x51_heads as M
from tests.test_x48_heads import forward, ids_for, tiny_muse, tiny_qwen
from tests.test_x49_attn import CONTEXT, QUESTION, planted_run

# ---- item construction --------------------------------------------------------------------------------------------


class FakeTok:
    """Word-level ids and offsets (x49_attn's test tokenizer): a leading space joins the next word."""

    def __init__(self):
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r" ?[A-Za-z]+|'s|[0-9]|[.?:<>]|\n", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans)


def fake_render(_tok, context, question):
    return f"<user>{context}\n{question}\nAnswer:"


def test_reader_sites_are_each_readers_own_positions(monkeypatch):
    """last = the appended read token (len(ids)); question = the question text's tokens; a recall question one token
    longer shifts both (49.7 used the lookup's positions for the recall)."""
    monkeypatch.setattr(A, "rendered", fake_render)
    tok = FakeTok()
    recall_q = "How many legs does Lucy's pick have?"
    ids_l = tok(fake_render(tok, CONTEXT, QUESTION)).input_ids
    ids_r = tok(fake_render(tok, CONTEXT, recall_q)).input_ids
    sl = M.reader_sites(tok, CONTEXT, QUESTION, ids_l, [99])
    sr = M.reader_sites(tok, CONTEXT, recall_q, ids_r, [99])
    text = fake_render(tok, CONTEXT, QUESTION)
    spans = tok(text, return_offsets_mapping=True).offset_mapping
    assert "".join(text[spans[p][0] : spans[p][1]] for p in sl["question"]) == QUESTION
    assert sl["last"] == [len(ids_l)] and sr["last"] == [len(ids_r)] and len(ids_r) == len(ids_l) + 1
    assert len(sr["question"]) == len(sl["question"]) + 1 and sr["question"][0] == sl["question"][0]
    with pytest.raises(AssertionError, match="read suffix"):
        M.reader_sites(tok, CONTEXT, QUESTION, ids_l, [99, 98])
    with pytest.raises(AssertionError, match="ids differ"):
        M.reader_sites(tok, CONTEXT, QUESTION, ids_l[:-1], [99])
    it = {"scene": "s", "context": CONTEXT, "space": [99],
          "layout": {"last": sl["last"][0], "question": sl["question"]},
          "readers": {X.LOOKUP: {"question": QUESTION, "ids": ids_l}, X.RECALL: {"question": recall_q, "ids": ids_r}}}  # fmt: skip
    assert M.with_sites(tok, it)["sites"] == {X.LOOKUP: sl, X.RECALL: sr}
    it["layout"]["last"] += 1
    with pytest.raises(AssertionError, match="lookup sites differ"):
        M.with_sites(tok, it)


# ---- ranking and sets ---------------------------------------------------------------------------------------------


def planted_source(tmp_path, monkeypatch):
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x49")
    planted_run(tmp_path / "x49", "qwen35_9b_x49_7")
    return M.source_run("qwen3.5-9b")


def test_ranking_from_the_fit_halfs_switched_pairs(tmp_path, monkeypatch):
    """On 49.7's planted run L5:h0 moves 1.0 on switched pairs, every other head 0: it ranks first; the rows are the
    fit half's switched pairs; ties go to the lower layer, then head."""
    S = planted_source(tmp_path, monkeypatch)
    mv, basis = M.fit_moves(S["a"], S["items"], S["rows"])
    n_fit_sw = sum(it["half"] == "fit" for it in S["items"])  # one switched pair per item (k = j + 1)
    assert mv.shape == (n_fit_sw, 2, 2) and "switched" in basis
    rk = M.rank_heads(mv, [5, 9])
    assert (rk[0]["layer"], rk[0]["head"]) == (5, 0) and rk[0]["move"] == pytest.approx(1.0, abs=1e-3)
    assert [(r["layer"], r["head"]) for r in rk[1:]] == [(5, 1), (9, 0), (9, 1)]  # all 0: lower layer, then head
    rows = [r | {"class": "original"} if r["arm"] == "swap" else r for r in S["rows"]]
    mv2, basis2 = M.fit_moves(S["a"], S["items"], rows)
    assert "no fit pair switched" in basis2 and len(mv2) == 2 * n_fit_sw


def test_head_sets_and_matched_random_controls():
    layers, n_heads = [15, 19, 23, 27], 16
    rng = np.random.default_rng(3)
    mv = rng.normal(size=(5, len(layers), n_heads))
    mv[:, 3, 1] += 5  # L27:h1 first
    rk = M.rank_heads(mv, layers)
    sets = M.head_sets(rk, layers, n_heads, n_draws=3)
    assert sets["top1"]["heads"] == [(27, 1)] and [len(sets[f"top{k}"]["heads"]) for k in M.KS] == list(M.KS)
    assert sets["top10"]["heads"] == [(r["layer"], r["head"]) for r in rk[:10]]
    assert sets["best_layer"]["heads"] == [(27, h) for h in range(16)] and sets["best_layer"]["layer"] == 27
    assert len(sets) == (len(M.KS) + 1) * 4
    for k in M.KS:
        top = sets[f"top{k}"]["heads"]
        for d in range(3):
            r = sets[f"top{k}_r{d}"]
            assert r["of"] == f"top{k}" and not set(r["heads"]) & set(top)
            assert {la: len(h) for la, h in M.by_layer(r["heads"]).items()} == {
                la: len(h) for la, h in M.by_layer(top).items()
            }
    for d in range(3):
        r = sets[f"best_layer_r{d}"]["heads"]
        assert len(r) == 16 and all(la != 27 for la, _ in r) and len(set(r)) == 16
    assert M.head_sets(rk, layers, n_heads, n_draws=3) == sets  # seeded
    assert M.head_sets(rk, layers, n_heads, n_draws=3, seed=1)["top5_r0"] != sets["top5_r0"]
    with pytest.raises(AssertionError, match="leave"):
        M.random_matched([(5, 0), (5, 1)], 3, random.Random(0))


# ---- mean capture and ablation on tiny models ---------------------------------------------------------------------


@pytest.mark.parametrize("which", ["qwen", "muse"])
def test_capture_and_mean_ablation_touch_only_the_listed_slices(which):
    """capture_o_inputs returns o_proj's input at the positions; mean_heads replaces exactly the listed heads' slices
    there by the given means (every batch row), nothing else; layers without listed heads are untouched."""
    model = tiny_qwen() if which == "qwen" else tiny_muse()
    blocks: Any = A.decoder_layers(model)
    attn = blocks[3].self_attn
    hd = attn.head_dim
    width = model.config.num_attention_heads * hd
    ids = ids_for(5, 20)
    got: dict = {}
    with M.capture_o_inputs(model, [3, 7], [4, 12], got):
        forward(model, ids)
    seen: list = []
    handle = attn.o_proj.register_forward_hook(lambda _m, args, _o: seen.append(args[0].clone()))
    try:
        forward(model, ids)
        assert torch.allclose(got[3], seen[0][0, [4, 12]].float())
        means = {3: torch.arange(2 * width, dtype=torch.float32).view(2, width) / width}
        with M.mean_heads(model, {3: [0, 2]}, [4, 12], means):
            forward(model, torch.cat([ids, ids]))
    finally:
        handle.remove()
    clean, ablated = seen[0], seen[1]
    for b in range(2):
        for pi, p in enumerate([4, 12]):
            for h in (0, 2):
                assert torch.allclose(
                    ablated[b, p, h * hd : (h + 1) * hd].float(), means[3][pi, h * hd : (h + 1) * hd], atol=1e-3
                )
    mask = torch.ones_like(ablated[0], dtype=torch.bool)
    for p in (4, 12):
        for h in (0, 2):
            mask[p, h * hd : (h + 1) * hd] = False
    assert torch.allclose(clean[0][mask], ablated[0][mask], atol=1e-5)  # other heads and positions untouched


def test_mean_ablation_skips_a_cached_step():
    model = tiny_qwen()
    attn: Any = A.decoder_layers(model)[3].self_attn
    width = model.config.num_attention_heads * attn.head_dim
    seen: list = []
    handle = attn.o_proj.register_forward_hook(lambda _m, args, _o: seen.append(args[0].clone()))
    try:
        forward(model, ids_for(1, 6))
        with M.mean_heads(model, {3: [1]}, [10], {3: torch.ones(1, width)}):
            forward(model, ids_for(1, 6))  # 6 tokens < position 10: nothing to replace
    finally:
        handle.remove()
    assert torch.equal(seen[0], seen[1])


# ---- rules --------------------------------------------------------------------------------------------------------


def cell(s_swap, s_abl, ident=0.0, recall=0.0, n=100):
    sw, ab, rc = round(s_swap * n), round(s_abl * n), round(recall * n)
    ic = round(ident * (n - sw))
    planted = [{"target_swap": int(i < sw), "target_zero": int(i < ab), "identity_swap": i >= sw,
                "lookup_changed": int(sw <= i < sw + ic), "recall_changed": int(i < rc)} for i in range(n)]  # fmt: skip
    rows = M.A.necessity(planted)
    return rows | {"cut": [M.cut_of(rows["switch_swap"], rows["switch_zero"]), 0.0, 1.0]}


def rand(cut):
    return {"cut_mean": cut}


def test_small_set_distributed_neither_on_planted_numbers():
    small = M.rules({1: cell(0.4, 0.4), 3: cell(0.4, 0.2)}, {1: rand(0.0), 3: rand(0.15)}, cell(0.4, 0.1))
    assert small["label"] == "small set" and small["small_ks"] == [3] and not small["distributed"]  # cut exactly 0.5
    assert M.rules({3: cell(0.4, 0.21)}, {3: rand(0.0)}, cell(0.4, 0.1))["label"] == "neither"  # cut 0.475
    assert M.rules({3: cell(0.4, 0.0)}, {3: rand(0.16)}, cell(0.4, 0.1))["label"] == "neither"  # random cuts 0.16
    assert (
        M.rules({3: cell(0.4, 0.0, ident=0.2)}, {3: rand(0.0)}, cell(0.4, 0.1))["label"] == "neither"
    )  # identity moves
    assert (
        M.rules({3: cell(0.4, 0.0, recall=0.11)}, {3: rand(0.0)}, cell(0.4, 0.1))["label"] == "neither"
    )  # recall moves
    d = M.rules({3: cell(0.4, 0.35)}, {3: rand(0.0)}, cell(0.4, 0.29))
    assert d["label"] == "distributed" and d["distributed"] and d["best_layer_cut"] == pytest.approx(0.275)
    assert M.rules({3: cell(0.4, 0.35)}, {3: rand(0.0)}, cell(0.4, 0.28))["label"] == "neither"  # the layer cuts 0.3
    both = M.rules({10: cell(0.4, 0.0)}, {10: rand(0.0)}, cell(0.4, 0.4))
    assert both["label"] == "small set" and both["distributed"]  # both flags shown, small set first
    assert not M.rules({3: cell(0.0, 0.0)}, {3: rand(math.nan)}, cell(0.0, 0.0))["distributed"]  # nothing to cut


def test_random_summary_and_cut():
    cells = [{"cut": [0.1, 0, 0], "identity_changed": 0.0, "recall_changed": 0.1},
             {"cut": [0.3, 0, 0], "identity_changed": 0.2, "recall_changed": 0.1}]  # fmt: skip
    s = M.random_summary(cells)
    assert (
        s["cut_mean"] == pytest.approx(0.2)
        and s["cut_sd"] == pytest.approx(0.1)
        and (s["cut_min"], s["cut_max"]) == (0.1, 0.3)
    )
    assert s["identity_changed"] == pytest.approx(0.1) and s["draws"] == 2
    assert M.cut_of(0.4, 0.1) == pytest.approx(0.75) and math.isnan(M.cut_of(0.0, 0.0))


def test_logistic_and_auc():
    rng = np.random.default_rng(0)
    x = np.concatenate([rng.normal(0, 1, 200), rng.normal(2, 1, 200)])
    y = np.r_[np.zeros(200), np.ones(200)]
    ents = [f"e{i % 20}" for i in range(400)]
    lg = M.fit_logistic(x, y)
    assert lg["converged"] and lg["b_per_unit"] == pytest.approx(2.0, rel=0.3)  # the Bayes slope for unit variances
    auc = M.auc_ci(x, y, ents, n_boot=200)
    assert 0.85 < auc[0] < 0.97 and auc[1] < auc[0] < auc[2]
    assert M.auc_ci(np.arange(10.0), np.arange(10) >= 5, [f"e{i}" for i in range(10)], n_boot=50)[0] == 1.0
    assert math.isnan(M.fit_logistic(np.ones(5), np.r_[0, 1, 0, 1, 0])["a"])


# ---- seal and a planted run ---------------------------------------------------------------------------------------


def test_parse_answer_and_the_seal(monkeypatch):
    text = "**Q51.2** (51.2) Joint ...\n- (a) small\n- (b) distributed\n\nDan:\n\n**Q51.3** DAS\n\nDan: (i) 60%\n"
    assert M.parse_answer(text) == ""
    filled = text.replace("Dan:\n\n**Q51.3", "Dan (9B): (a) 60%\nDan (27B): (b) 55%\n- note\n\n**Q51.3")
    assert M.parse_answer(filled) == "(a) 60%\nDan (27B): (b) 55%\n- note"
    monkeypatch.setattr(M, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        M.stage_verdict(["qwen35_9b_x51_2"], n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        M.stage_view(["qwen35_9b_x51_2"])


def planted_x51(root, S: dict) -> None:
    """A 51.2 run on 49.7's planted items: the top 3 / 5 / 10 sets at the last token undo every switch; the top 1 and
    every random set nothing; the best layer cuts a quarter (one of the read half's switched pairs per four); the
    question tokens nothing."""
    src = root / "qwen35_9b_x51_2"
    src.mkdir(parents=True)
    items = [it | {"sites": {X.LOOKUP: {"last": [20], "question": [15, 16]}, X.RECALL: {"last": [21], "question": [15, 16, 17]}}}
             for it in S["items"]]  # fmt: skip
    all4 = [[5, 0], [5, 1], [9, 0], [9, 1]]
    sets: dict[str, dict] = {"top1": {"kind": "top", "k": 1, "heads": [[5, 0]]},
                             "top3": {"kind": "top", "k": 3, "heads": all4[:3]},
                             "top5": {"kind": "top", "k": 5, "heads": all4}, "top10": {"kind": "top", "k": 10, "heads": all4},
                             "best_layer": {"kind": "layer", "k": 2, "layer": 5, "heads": all4[:2]}}  # fmt: skip
    for base in list(sets):
        for d in range(2):
            sets[f"{base}_r{d}"] = {"kind": "random", "of": base, "draw": d, "k": 1, "heads": [[9, 1]]}
    read_sw = [(it["scene"], k) for it in items if it["half"] == "read" for k in it["ks"] if k == (it["j"] + 1) % 3]
    quarter = set(read_sw[::4])
    rows = []
    for it in items:
        if it["half"] != "read":
            continue
        for name, site in [(None, None)] + [(n, s) for n in sets for s in M.SITES]:
            for w in X.READERS:
                rows.append({"scene": it["scene"], "entity": it["entity"], "reader": w, "arm": "none", "k": None, "set": name,
                             "site": site, "top": 1, "class": "original"})  # fmt: skip
                for k in it["ks"]:
                    sw = k == (it["j"] + 1) % 3
                    if site == "last" and name in ("top3", "top5", "top10"):
                        sw = False
                    if site == "last" and name == "best_layer" and (it["scene"], k) in quarter:
                        sw = False
                    rows.append({"scene": it["scene"], "entity": it["entity"], "reader": w, "arm": "swap", "k": k,
                                 "set": name, "site": site, "top": (2 if sw else 1) if w == X.LOOKUP else 7,
                                 "class": "target" if sw else "original"})  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", items)
    X.write_jsonl(src / "ablation.jsonl", rows)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layer": 3, "recorded_layers": [5, 9],
                                                   "skipped_linear_layers": [4, 6], "best_layer": 5, "sets": sets,
                                                   "ranking_top10": [{"layer": 5, "head": 0, "move": 1.0}]}))  # fmt: skip
    (src / "status.json").write_text(json.dumps({"status": "tested"}))


def test_planted_run_through_the_verdict_and_view(tmp_path, monkeypatch):
    S = planted_source(tmp_path, monkeypatch)
    monkeypatch.setattr(M, "RESULTS", tmp_path / "x51")
    planted_x51(tmp_path / "x51", S)
    (tmp_path / "x51" / "muse30_x51_2").mkdir()
    (tmp_path / "x51" / "muse30_x51_2" / "status.json").write_text(json.dumps({"status": "not tested", "gate": {}}))
    r = M.analyse("qwen35_9b_x51_2", n_boot=50)
    last = r["sites"]["last"]
    assert r["switch_swap"] == pytest.approx(0.5) and last["cells"]["top3"]["cut"][0] == pytest.approx(1.0)
    assert last["cells"]["top1"]["cut"][0] == pytest.approx(0.0) and last["random"]["top3"][
        "cut_mean"
    ] == pytest.approx(0.0)
    assert last["cells"]["best_layer"]["cut"][0] == pytest.approx(0.25)
    assert (
        last["rules"]["label"] == "small set"
        and last["rules"]["small_ks"] == [3, 5, 10]
        and last["rules"]["distributed"]
    )
    assert r["sites"]["question"]["rules"]["label"] == "distributed"  # the best layer cuts 0 there, nothing else does
    assert r["label"] == "small set"
    b = r["beside"]["all_heads"]
    assert b["auc"][0] == pytest.approx(1.0) and b["switched"] == len([1 for it in S["items"] if it["half"] == "read"])
    assert M.analyse("muse30_x51_2")["status"] == "not tested" and M.analyse("x51_2_27b")["status"] == "pending"
    monkeypatch.setattr(M, "dan_answer", lambda rev="HEAD": "Dan (9B): (a) 60%")
    out = M.stage_verdict(["qwen35_9b_x51_2", "muse30_x51_2", "x51_2_27b"], n_boot=50)
    md = (out / "verdict.md").read_text()
    assert "**small set** (last token; small set at k = [3, 5, 10]" in md and "not tested" in md and "pending" in md
    assert (out / "heads_qwen3.5-9b.png").exists()
    ex = (out / "examples.md").read_text()
    assert "### top3 at the last token(s)" in ex and "### best_layer_r0 at the question token(s)" in ex
    view = M.stage_view(["qwen35_9b_x51_2"])
    assert (view / "view.md").exists()
