"""scripts/x49_attn.py (batch 49, test 49.7): the attention recording on tiny Qwen3.5 (hybrid) and Muse Glimmer models
(full-attention layers recorded, Gated DeltaNet layers skipped, several query positions against eager weights), the head
ablation and W_Q / W_K rows, token groups, the move arithmetic, head selection on the fit half, the rules on planted
numbers, the weights-level score, a planted run through the CPU verdict, and the seal (no download)."""

from __future__ import annotations

import json
import math
from typing import Any

import numpy as np
import pytest
import torch

from bridge_jspace.knockout import FULL, LINEAR, layer_kinds
from scripts import x0_necessity as X
from scripts import x49_attn as A
from tests.test_x48_heads import TYPES, eager_weights, forward, ids_for, tiny_muse, tiny_qwen

# ---- attention recording ------------------------------------------------------------------------------------------


def test_recorded_layers_skip_deltanet():
    """Layers > L: the softmax-attention ones recorded, the Gated DeltaNet ones skipped (and returned for the log)."""
    assert A.recorded_layers(TYPES, 1) == ([3, 7], [2, 4, 5, 6])
    assert A.recorded_layers(TYPES, 3) == ([7], [4, 5, 6])
    assert A.recorded_layers([FULL] * 5, 2) == ([3, 4], [])
    assert layer_kinds(tiny_qwen()) == TYPES


def test_capture_returns_full_layers_only_and_refuses_deltanet():
    """On the hybrid fake model, recording every layer > 1 returns weights for the full-attention layers 3 and 7 only
    (the recorded list), and a Gated DeltaNet layer is refused outright."""
    model = tiny_qwen("eager")
    full, skipped = A.recorded_layers(layer_kinds(model), 1)
    out: dict = {}
    with A.capture_queries(model, full, [10, 25], out):
        forward(model, ids_for(3, 26))
    assert sorted(out) == [3, 7] and skipped == [2, 4, 5, 6]
    assert all(layer_kinds(model)[la] == LINEAR for la in skipped)
    with pytest.raises(AssertionError, match="not a softmax-attention layer"), A.capture_queries(model, [2], [5], {}):
        pass


@pytest.mark.parametrize("which", ["qwen", "muse"])
def test_capture_matches_eager_at_several_queries(which):
    """Probabilities from several query positions equal eager attention's own weights on both architectures (Muse: a
    sliding RoPE layer with window 16 < T and a full NoPE layer); scores are -inf exactly where blocked; the inputs
    captured are the attention's input (post input-norm)."""
    model = tiny_qwen("eager") if which == "qwen" else tiny_muse("eager")
    layers = [3, 7] if which == "qwen" else [5, 7]
    ids = ids_for(11, 26)
    qs = [4, 17, 25]
    out: dict = {}
    ins: dict = {}
    with A.capture_queries(model, layers, qs, out, inputs=ins):
        forward(model, ids)
    for la in layers:
        probs, scores = out[la]
        assert probs.shape == scores.shape == (4, 3, 26)
        for qi, q in enumerate(qs):
            ref = eager_weights(model, ids, la, q)
            assert (probs[:, qi] - ref).abs().max() < 1e-5
        assert torch.isinf(scores[:, 0, 5:]).all() and torch.isfinite(scores[:, 0, :5]).all()  # causal
        assert ins[la].shape == (26, model.config.hidden_size)
    if which == "muse":
        assert float(out[5][0][:, 2, : 26 - 16].abs().max()) == 0.0  # the window blocks old keys for q = 25


def test_zero_head_removes_only_that_slice_at_those_positions():
    """zero_head zeroes head h's slice of o_proj's input at the listed positions only (both architectures); the block
    output before the position is untouched (causal) and differs at it."""
    for model in (tiny_qwen(), tiny_muse()):
        attn: Any = A.decoder_layers(model)[3].self_attn
        hd = attn.head_dim
        seen: list = []
        handle = attn.o_proj.register_forward_hook(lambda _m, args, _o, seen=seen: seen.append(args[0].clone()))
        ids = ids_for(5, 20)
        try:
            forward(model, ids)
            with A.zero_head(model, 3, 2, [12]):
                forward(model, ids)
        finally:
            handle.remove()
        clean, zeroed = seen
        assert float(zeroed[0, 12, 2 * hd : 3 * hd].abs().max()) == 0.0
        assert float(clean[0, 12, 2 * hd : 3 * hd].abs().max()) > 0.0
        mask = torch.ones_like(clean, dtype=torch.bool)
        mask[0, 12, 2 * hd : 3 * hd] = False
        assert torch.equal(clean[mask], zeroed[mask])


def test_head_qk_weights_are_the_module_projections():
    """W_Q rows (Qwen3.5: the query half of the head's q_proj block, not the gate) and the kv group's W_K rows give the
    module's own per-head query and key before the norms."""
    for model in (tiny_qwen(), tiny_muse()):
        attn: Any = A.decoder_layers(model)[3].self_attn
        cfg = model.config
        n_heads, n_kv, hd = cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim
        x = torch.randn(3, cfg.hidden_size, generator=torch.Generator().manual_seed(4))
        q_all = attn.q_proj(x)
        if q_all.shape[-1] == 2 * n_heads * hd:
            q_all = torch.chunk(q_all.view(3, n_heads, 2 * hd), 2, dim=-1)[0]
        else:
            q_all = q_all.view(3, n_heads, hd)
        k_all = attn.k_proj(x).view(3, n_kv, hd)
        for h in range(n_heads):
            w_q, w_k = A.head_qk_weights(attn, h, n_heads, n_kv, hd)
            assert torch.allclose(x @ w_q.T, q_all[:, h], atol=1e-5)
            assert torch.allclose(x @ w_k.T, k_all[:, A.H.kv_group(h, n_heads, n_kv)], atol=1e-5)


# ---- token groups and reductions ----------------------------------------------------------------------------------

CONTEXT = "The locker of the frog is 5. The locker of the ant is 3. The locker of the crow is 4. Lucy picked the crow."
QUESTION = "Which locker belongs to Lucy's pick?"


def word_offsets(text: str) -> list[tuple[int, int]]:
    """A fake tokenizer's offsets: a leading space joins the next word; '.', '?', "'s" are their own tokens."""
    import re

    return [(m.start(), m.end()) for m in re.finditer(r" ?[A-Za-z]+|'s|[0-9]|[.?]|\n", text)]


def test_locker_groups_and_question_by_character_overlap():
    text = f"<user>{CONTEXT}\n{QUESTION}\nAnswer:"
    off = word_offsets(text)
    groups = A.locker_groups(off, text, CONTEXT)
    piece = lambda ps: "".join(text[off[p][0] : off[p][1]] for p in ps)  # noqa: E731
    assert [piece(g["item"]) for g in groups] == [" frog", " ant", " crow"]
    assert [piece(g["num"]) for g in groups] == [" 5", " 3", " 4"] or [piece(g["num"]) for g in groups] == [
        "5",
        "3",
        "4",
    ]
    assert piece(groups[1]["rest"]) == " The locker of the is."
    q = A.question_positions(off, text, CONTEXT, QUESTION)
    assert piece(q) == QUESTION
    g = A.group_matrix(len(off), groups)
    assert g.sum() == sum(len(x[p]) for x in groups for p in A.PARTS) and g.sum(1).max() == 1
    gm = A.sentence_mean_matrix(len(off), groups)
    assert np.allclose(gm.sum(0), 1.0)


def test_reduce_masses_entropy_logits_and_tv():
    """Planted attention: head 0 puts 0.6 on slot 1's number and 0.4 on slot 2's item from the last query; head 1 is
    uniform over 4 keys. Masses per slot / part, entropy, mean logit per sentence, sites, TV from none."""
    t = 10
    groups = [{"item": [1], "num": [2], "rest": [0]}, {"item": [4], "num": [5], "rest": [3]},
              {"item": [7], "num": [8], "rest": [6]}]  # fmt: skip
    probs = torch.zeros(2, 2, t)
    probs[0, 1, 5], probs[0, 1, 7] = 0.6, 0.4
    probs[0, 0, 0] = 1.0
    probs[1, :, :4] = 0.25
    scores = torch.log(probs.clamp_min(1e-12))
    g, gm = torch.tensor(A.group_matrix(t, groups)), torch.tensor(A.sentence_mean_matrix(t, groups))
    sites = {"question": [0], "last": [1]}
    mass, ent, _logit = A.reduce(probs, scores, g, gm, sites)
    last = A.SITES.index("last")
    m0 = mass[0, last].view(3, 3)
    assert m0[1, 1] == pytest.approx(0.6) and m0[2, 0] == pytest.approx(0.4) and float(m0.sum()) == pytest.approx(1.0)
    m1 = mass[1, last].view(3, 3)  # keys 0..3: slot 0's three tokens and slot 1's rest
    assert float(m1[0].sum()) == pytest.approx(0.75) and float(m1[1, 2]) == pytest.approx(0.25)
    assert torch.allclose(mass[:, A.SITES.index("question")].view(2, 3, 3)[0, 0], torch.tensor([0.0, 0.0, 1.0]))
    assert ent[1, last] == pytest.approx(math.log(4), rel=1e-5)
    assert ent[0, last] == pytest.approx(-(0.6 * math.log(0.6) + 0.4 * math.log(0.4)), rel=1e-5)
    tv = A.tv_sites(probs, probs.flip(0), sites)
    assert tv[0, last] == pytest.approx(1.0)  # disjoint supports (head 0 vs head 1's last-token rows)


def test_move_arithmetic_on_planted_masses():
    """move = (m[k] - m[j]) under the arm minus the same under none, per pair, on any trailing shape."""
    none = np.array([[0.5, 0.1, 0.0], [0.2, 0.2, 0.2]])
    arm = np.array([[0.1, 0.5, 0.0], [0.2, 0.2, 0.6]])
    j, k = np.array([0, 1]), np.array([1, 2])
    assert np.allclose(A.moves(arm, none, j, k), [(0.5 - 0.1) - (0.1 - 0.5), (0.6 - 0.2) - 0.0])
    big = np.broadcast_to(arm[:, None, None, :], (2, 3, 4, 3)).copy()
    bign = np.broadcast_to(none[:, None, None, :], (2, 3, 4, 3)).copy()
    assert np.allclose(A.moves(big, bign, j, k), np.array([0.8, 0.4])[:, None, None])
    assert np.allclose(A.slot_mass(np.ones((2, 3, 3))), 3.0)


def test_split_and_head_selection_on_the_fit_half():
    """The split is seeded and by entity; the five candidates come from the fit items only (read items plant the
    opposite ranking), the best head by the fit half's switched moves."""
    ents = [f"e{i // 2}" for i in range(20)]
    fit, read = A.split_halves(ents)
    assert fit | read == set(ents) and not fit & read and len(fit) == 5
    assert A.split_halves(ents) == (fit, read)
    is_fit = np.array([e in fit for e in ents])
    layers = [3, 7]
    mass = np.zeros((20, 2, 4))
    mass[is_fit, 0, 1], mass[~is_fit, 1, 2] = 0.9, 0.95  # fit favours L3:h1, read favours L7:h2
    mass[:, 1, 0] = 0.3
    cands = A.select_candidates(mass, layers, is_fit, k=2)
    assert [(c["layer"], c["head"]) for c in cands] == [(3, 1), (7, 0)]
    best, why = A.best_head(cands, {(3, 1): np.array([0.1, 0.2]), (7, 0): np.array([0.5])})
    assert (best["layer"], best["head"]) == (7, 0) and "largest" in why
    best, why = A.best_head(cands, {(3, 1): np.array([]), (7, 0): np.array([])})
    assert (best["layer"], best["head"]) == (3, 1) and "no switched" in why


# ---- rules --------------------------------------------------------------------------------------------------------


def stats(m, lo, rand, non, n=40):
    return {"swap_switched": [m, lo, m + 0.1], "random_switched": [rand, rand - 0.01, rand + 0.01],
            "swap_nonswitched": [non, non - 0.01, non + 0.01], "n_switched": n, "n_nonswitched": n}  # fmt: skip


def heads_of(*sts):
    return [{"layer": 15 + 4 * i, "head": i, "stats": s} for i, s in enumerate(sts)]


def test_follows_rule_on_planted_numbers():
    assert A.follows_head(stats(0.30, 0.01, 0.05, 0.10))  # every bar exactly met
    assert not A.follows_head(stats(0.29, 0.01, 0.0, 0.0))  # the move under 0.30
    assert not A.follows_head(stats(0.40, 0.0, 0.0, 0.0))  # CI touches 0
    assert not A.follows_head(stats(0.40, 0.1, 0.06, 0.0))  # the random vector moves it too
    assert not A.follows_head(stats(0.40, 0.1, 0.0, 0.11))  # moves on non-switched items
    assert not A.follows_head(stats(0.40, 0.1, 0.0, 0.0, n=0))
    r = A.rules(
        heads_of(stats(0.4, 0.2, 0.0, 0.0), stats(0.1, 0.0, 0.0, 0.0)),
        0.4,
        0.45,
        {"five": 0.5, "best_layer": 0.4},
        True,
    )
    assert r["label"] == "follows" and r["follows_heads"] == ["L15:h0"] and not r["distributed"] and "caveat" not in r


def test_elsewhere_distributed_neither_and_the_9b_caveat():
    weak = heads_of(*[stats(0.08, 0.01, 0.0, 0.0)] * 5)
    r = A.rules(weak, 0.149, 0.30, {"five": 0.4, "best_layer": 0.1}, True)
    assert r["label"] == "elsewhere" and r["distributed"]  # the five sum to 0.4, none reaches 0.30
    assert r["caveat"] == "the dereference is not in full attention on this model"
    assert "caveat" not in A.rules(weak, 0.149, 0.30, {"five": 0.4, "best_layer": 0.1}, False)  # Muse: no DeltaNet
    assert A.rules(weak, 0.15, 0.30, {"five": 0.1, "best_layer": 0.1}, True)["label"] == "neither"  # a head at 0.15
    assert A.rules(weak, 0.10, 0.29, {"five": 0.1, "best_layer": 0.1}, True)["label"] == "neither"  # too few switches
    r = A.rules(weak, 0.149, 0.5, {"five": 0.1, "best_layer": 0.30}, False)
    assert r["distributed"] and r["label"] == "elsewhere"  # the best layer's sum alone
    strong = heads_of(stats(0.31, 0.0, 0.0, 0.0))  # a head at 0.31 with its CI touching 0: no follows, no distributed
    r = A.rules(strong, 0.31, 0.5, {"five": 0.6, "best_layer": 0.6}, False)
    assert r["label"] == "neither" and not r["distributed"]


def nec_rows(n_target_swap, n_target_zero, n_ident, n_ident_changed, n_recall_changed, n=20):
    rows = []
    for i in range(n):
        rows.append({"target_swap": int(i < n_target_swap), "target_zero": int(i < n_target_zero),
                     "identity_swap": n_target_swap <= i < n_target_swap + n_ident,
                     "lookup_changed": int(n_target_swap <= i < n_target_swap + n_ident_changed),
                     "recall_changed": int(i < n_recall_changed)})  # fmt: skip
    return rows


def test_necessity_rule_on_planted_numbers():
    ok = A.necessity(nec_rows(10, 5, 10, 1, 2))  # falls by exactly half; identity 0.10; recall 0.10
    assert ok["holds"] and ok["fall_share"] == pytest.approx(0.5) and ok["identity_changed"] == pytest.approx(0.1)
    assert not A.necessity(nec_rows(10, 6, 10, 0, 0))["holds"]  # falls by 0.4 of it
    assert not A.necessity(nec_rows(10, 0, 10, 2, 0))["holds"]  # identity answers change 0.2
    assert not A.necessity(nec_rows(10, 0, 10, 0, 3))["holds"]  # the recall changes 0.15
    assert not A.necessity(nec_rows(0, 0, 20, 0, 0))["holds"]  # nothing to fall
    assert A.necessity([])["holds"] is False


def test_score_matrix_and_dominance():
    w = np.eye(3, 4)  # hd = 3, d = 4
    s = A.score_matrix(w, w, 2 * np.eye(3, 4), np.eye(3, 4))
    assert np.allclose(s, 2 * np.eye(3))
    w_k = np.roll(np.eye(3, 4), 1, axis=0)  # keys permuted: the diagonal moves off
    assert np.allclose(A.score_matrix(w, w_k, np.eye(3, 4), np.eye(3, 4)), np.roll(np.eye(3), 1, axis=0))
    assert math.isnan(A.dominance(s))  # off-diagonal spread 0
    planted = np.array([[3.0, 1.0, 0.0], [0.0, 3.0, 1.0], [1.0, 0.0, 3.0]])
    off = np.array([1, 0, 0, 1, 1, 0], dtype=float)
    assert A.dominance(planted) == pytest.approx((3.0 - off.mean()) / off.std())


# ---- seal and a planted run through the verdict -------------------------------------------------------------------


def test_parse_answer_reads_per_model_lines_and_bullets(monkeypatch):
    text = "**Q49.7** Does ...\n- (a) x\n- (b) y\n\nIf (a): ...\n\nDan:\n\n**Q49.8** DAS\n\nDan: (a) 60%\n"
    assert A.parse_answer(text) == ""
    filled = text.replace("Dan:\n\n**Q49.8", "Dan (9B): (b) 60%\nDan (Muse): (a) 55%\n- above L+4\n\n**Q49.8")
    got = A.parse_answer(filled)
    assert got == "(b) 60%\nDan (Muse): (a) 55%\n- above L+4"  # x47_chain's regex: the first label is consumed
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(["qwen35_9b_x49_7"], n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_view(["qwen35_9b_x49_7"])


def planted_run(root, run: str) -> None:
    """8 items over 4 entities; layers [5, 9] x 2 heads. L5:h0 moves from slot j to slot k on the switched swap pairs
    (k = j + 1 mod 3), nowhere else; zeroing it at the last token undoes every switch, at the question tokens none."""
    src = root / run
    src.mkdir(parents=True)
    ents = [f"e{i // 2}" for i in range(8)]
    fit, _ = A.split_halves(ents)
    items = [{"scene": f"s{i}", "entity": ents[i], "half": "fit" if ents[i] in fit else "read", "j": i % 3,
              "ks": [k for k in range(3) if k != i % 3], "slots": [["a", 1], ["b", 2], ["c", 3]]} for i in range(8)]  # fmt: skip
    nl, nh, ns = 2, 2, len(A.SITES)
    base = np.zeros((8, nl, nh, ns, 3, 3), np.float32)
    base[..., :, 2] = 0.1  # 0.1 on each sentence's rest
    for i, it in enumerate(items):
        base[i, 0, 0, :, it["j"], 1] = 0.5  # L5:h0 reads slot j's number under none
    p_item = np.repeat(np.arange(8), 2)
    p_k = np.array([k for it in items for k in it["ks"]])
    switched = np.array([k == (items[i]["j"] + 1) % 3 for i, k in zip(p_item, p_k, strict=True)])
    swap = base[p_item].copy()
    for p in np.flatnonzero(switched):
        i = p_item[p]
        swap[p, 0, 0, :, items[i]["j"], 1] = 0.0
        swap[p, 0, 0, :, p_k[p], 1] = 0.5
    rand = base[p_item].copy()
    shp_i, shp_p = (8, nl, nh, ns), (16, nl, nh, ns)
    np.savez_compressed(src / "attention.npz", layers=np.array([5, 9]), sites=np.array(A.SITES), parts=np.array(A.PARTS),
                        pair_item=p_item, pair_k=p_k, mass_none=base.reshape(*shp_i, 9),
                        mass_swap=swap.reshape(*shp_p, 9).astype(np.float16), mass_random=rand.reshape(*shp_p, 9).astype(np.float16),
                        ent_none=np.ones(shp_i, np.float32), ent_swap=np.ones(shp_p, np.float32), ent_random=np.ones(shp_p, np.float32),
                        logit_none=np.zeros((*shp_i, 3), np.float32), logit_swap=np.zeros((*shp_p, 3), np.float32),
                        logit_random=np.zeros((*shp_p, 3), np.float32), tv_swap=np.zeros(shp_p, np.float16),
                        tv_random=np.zeros(shp_p, np.float16))  # fmt: skip
    rows, abl = [], []
    for it in items:
        common = {"scene": it["scene"], "entity": it["entity"], "half": it["half"], "j": it["j"], "zero": None}
        rows.append({**common, "reader": X.LOOKUP, "arm": "none", "k": None, "top": 1, "class": "original"})
        rows.append({**common, "reader": X.RECALL, "arm": "none", "k": None, "top": 7, "changed": 0})
        for k in it["ks"]:
            sw = k == (it["j"] + 1) % 3
            rows.append({**common, "reader": X.LOOKUP, "arm": "swap", "k": k, "top": 2 if sw else 1,
                         "class": "target" if sw else "original"})  # fmt: skip
            rows.append({**common, "reader": X.LOOKUP, "arm": "random", "k": k, "top": 1, "class": "original"})
            for arm in ("swap", "random"):
                rows.append({**common, "reader": X.RECALL, "arm": arm, "k": k, "top": 7, "changed": 0})
        if it["half"] != "read":
            continue
        for zero in (None, "last", "question"):
            b = {"scene": it["scene"], "entity": it["entity"], "j": it["j"], "zero": zero}
            for w in X.READERS:
                abl.append({**b, "reader": w, "arm": "none", "k": None, "top": 1, "class": "original", "changed": 0})
                for k in it["ks"]:
                    sw = k == (it["j"] + 1) % 3 and zero != "last"
                    abl.append({**b, "reader": w, "arm": "swap", "k": k, "top": (2 if sw else 1) if w == X.LOOKUP else 7,
                                "class": "target" if sw else "original", "changed": 0})  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", items)
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "ablation.jsonl", abl)
    is_fit = np.array([it["half"] == "fit" for it in items])
    cands = A.select_candidates(base.reshape(*shp_i, 9)[:, :, :, 0].sum(-1), [5, 9], is_fit)
    (src / "heads.json").write_text(json.dumps({"candidates": cands, "best": cands[0], "why_best": "planted"}))
    d = 4
    rng = np.random.default_rng(0)
    np.savez_compressed(src / "states.npz", j=np.array([it["j"] for it in items]), layers=np.array([5, 9]),
                        last_L5=rng.normal(size=(8, d)), src_L5=rng.normal(size=(8, 3, d)),
                        last_L9=rng.normal(size=(8, d)), src_L9=rng.normal(size=(8, 3, d)))  # fmt: skip
    np.savez_compressed(
        src / "head_weights.npz", w_q=rng.normal(size=(2, d)), w_k=rng.normal(size=(2, d)), layer=5, head=0
    )
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layer": 3, "n_heads": nh,
                                                   "skipped_linear_layers": [4, 6]}))  # fmt: skip
    (src / "status.json").write_text(json.dumps({"status": "tested"}))


def test_planted_run_through_the_verdict(tmp_path, monkeypatch):
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    planted_run(tmp_path, "qwen35_9b_x49_7")
    (tmp_path / "muse30_x49_7").mkdir()
    (tmp_path / "muse30_x49_7" / "status.json").write_text(
        json.dumps({"status": "not tested", "gate": {"pass": False}})
    )
    r = A.analyse("qwen35_9b_x49_7", n_boot=50)
    d = r["sites"][A.DECISIVE]
    top = d["heads"][0]
    assert (top["layer"], top["head"]) == (5, 0)
    assert top["stats"]["swap_switched"][0] == pytest.approx(1.0, abs=1e-3)  # (0.5 - 0) - (0 - 0.5)
    assert top["stats"]["random_switched"][0] == pytest.approx(0.0) and top["stats"]["swap_nonswitched"][
        0
    ] == pytest.approx(0.0)
    assert r["label"] == "follows" and d["rules"]["follows_heads"] == ["L5:h0"]
    assert r["switch_share"][0] == pytest.approx(0.5)
    assert r["necessity"]["last"]["holds"] and not r["necessity"]["question"]["holds"]
    assert r["best_head"]["swap"]["mass_by_role_j_k_third"][1] == pytest.approx(0.6, abs=1e-3)  # num 0.5 + rest 0.1
    assert r["best_head"]["swap"]["slot_k_parts"]["num"] == pytest.approx(0.5, abs=1e-3)
    assert len(r["weights"]["S"]) == 3
    assert A.analyse("muse30_x49_7")["status"] == "not tested"
    assert A.analyse("x49_7_27b")["status"] == "pending"
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": "Dan (9B): (a) 60%")
    out = A.stage_verdict(["qwen35_9b_x49_7", "muse30_x49_7", "x49_7_27b"], n_boot=50)
    md = (out / "verdict.md").read_text()
    assert "**follows** (heads L5:h0)" in md and "not tested" in md and "pending" in md
    assert (out / "best_head_qwen3.5-9b.png").exists() and (out / "examples.md").exists()
