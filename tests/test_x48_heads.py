"""scripts/x48_heads.py (batch 48, test 48.4): W_OV assembly with GQA, attention capture on tiny Qwen3.5 and Muse
Glimmer models against eager weights, head selection, r on planted vectors, the rule on planted numbers, item
selection, and the sealed verdict (no download)."""

from __future__ import annotations

import json
import math
import types
from typing import Any

import pytest
import torch

from bridge_jspace.knockout import FULL, LINEAR
from scripts import x0_necessity as X
from scripts import x48_heads as H

TYPES = [LINEAR, LINEAR, LINEAR, FULL] * 2


def tiny_qwen(impl: str = "sdpa", seed: int = 0):
    from transformers import Qwen3_5TextConfig
    from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM

    cfg = Qwen3_5TextConfig(vocab_size=61, hidden_size=32, intermediate_size=48, num_hidden_layers=len(TYPES),
                            layer_types=TYPES, num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                            linear_num_key_heads=2, linear_num_value_heads=4, linear_key_head_dim=8,
                            linear_value_head_dim=6, linear_conv_kernel_dim=4, max_position_embeddings=128)  # fmt: skip
    cfg._attn_implementation = impl
    torch.manual_seed(seed)
    model = Qwen3_5ForCausalLM(cfg).eval()
    scale_weights(model, seed, "linear_attn.norm.weight")
    return model


def tiny_muse(impl: str = "sdpa", seed: int = 0, window: int = 16):
    """A tiny Muse Glimmer text decoder (its layer pattern: sliding, sliding, sliding, full/NoPE) wrapped so that
    knockout.decoder_layers finds its blocks (as a bridge_jspace Model's .hf would)."""
    from transformers.models.muse_glimmer.configuration_muse_glimmer import MuseGlimmerTextConfig
    from transformers.models.muse_glimmer.modeling_muse_glimmer import MuseGlimmerTextModel

    cfg = MuseGlimmerTextConfig(vocab_size=61, hidden_size=32, intermediate_size=48, num_hidden_layers=8,
                                num_attention_heads=4, num_key_value_heads=2, head_dim=8, sliding_window=window,
                                max_position_embeddings=128)  # fmt: skip
    cfg._attn_implementation = impl
    torch.manual_seed(seed)
    text = MuseGlimmerTextModel(cfg).eval()
    scale_weights(text, seed, None)
    return types.SimpleNamespace(model=text, get_input_embeddings=text.get_input_embeddings, config=cfg)


def scale_weights(model, seed: int, unit_norm: str | None) -> None:
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        for name, p in model.named_parameters():
            if name.endswith(("A_log", "dt_bias")):
                continue
            noise = torch.randn(p.shape, generator=g)
            if p.ndim >= 2:
                p.copy_(noise / math.sqrt(p.shape[-1]))
            else:
                p.copy_((1.0 if unit_norm and name.endswith(unit_norm) else 0.0) + 0.3 * noise)


def ids_for(seed: int, length: int) -> torch.Tensor:
    return torch.randint(0, 61, (1, length), generator=torch.Generator().manual_seed(seed))


# ---- W_OV ---------------------------------------------------------------------------------------------------------


def test_ov_apply_matches_matrix_and_gqa_mapping():
    """ov_apply equals the explicit W_O[:, h] W_V[g] product, with g = h // (n_heads / n_kv) as repeat_kv serves the
    query heads (kv head g's values are seen by heads g*rep .. g*rep+rep-1)."""
    from transformers.models.qwen3_5.modeling_qwen3_5 import repeat_kv

    d, n_heads, n_kv, hd = 12, 6, 2, 4
    g = torch.Generator().manual_seed(1)
    w_o, w_v = torch.randn(d, n_heads * hd, generator=g), torch.randn(n_kv * hd, d, generator=g)
    x = torch.randn(5, d, generator=g)
    for h in range(n_heads):
        m = H.ov_matrix(w_o, w_v, h, n_heads, n_kv, hd)
        assert torch.allclose(H.ov_apply(w_o, w_v, h, n_heads, n_kv, hd, x), x @ m.T, atol=1e-5)
        assert H.kv_group(h, n_heads, n_kv) == h // 3
    # the value each query head reads, by transformers' repeat_kv, is its kv group's
    v = (x @ w_v.T).view(5, n_kv, hd).transpose(0, 1)[None]  # [1, n_kv, T, hd]
    full = repeat_kv(v, n_heads // n_kv)[0]  # [n_heads, T, hd]
    for h in range(n_heads):
        gk = H.kv_group(h, n_heads, n_kv)
        assert torch.equal(full[h], v[0, gk])
        assert torch.allclose(H.ov_apply(w_o, w_v, h, n_heads, n_kv, hd, x), full[h] @ w_o[:, h * hd : (h + 1) * hd].T)


def test_ov_on_tiny_models_is_the_value_path():
    """On both architectures a one-hot attention (one key position) makes the head's contribution to o_proj's input
    its value vector: W_OV x, up to the sigmoid gate the circuit leaves out. Checked through the weights' shapes and
    by assembling W_OV from each module's own o_proj / v_proj."""
    for model in (tiny_qwen(), tiny_muse()):
        block: Any = H.decoder_layers(model)[3]
        attn = block.self_attn
        cfg = model.config
        n_heads, n_kv, hd = cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim
        x = torch.randn(3, cfg.hidden_size, generator=torch.Generator().manual_seed(2))
        for h in range(n_heads):
            y = H.ov_apply(attn.o_proj.weight, attn.v_proj.weight, h, n_heads, n_kv, hd, x)
            v = attn.v_proj(x).view(3, n_kv, hd)[:, H.kv_group(h, n_heads, n_kv)]  # the head's value vector
            expect = torch.zeros(3, n_heads * hd)
            expect[:, h * hd : (h + 1) * hd] = v
            assert torch.allclose(y, attn.o_proj(expect), atol=1e-5)
        gain = H.input_gain(block)
        assert torch.allclose(gain, 1.0 + block.input_layernorm.weight.float())


def test_ratios_on_planted_vectors():
    """r is the transmitted norm ratio: a right-singular vector of W_OV gives its singular value, a null vector 0, a
    zero row nan."""
    d, n_heads, n_kv, hd = 10, 2, 1, 3
    g = torch.Generator().manual_seed(3)
    w_o, w_v = torch.randn(d, n_heads * hd, generator=g), torch.randn(n_kv * hd, d, generator=g)
    m = H.ov_matrix(w_o, w_v, 1, n_heads, n_kv, hd)
    _u, s, vh = torch.linalg.svd(m)
    x = torch.stack([vh[0], vh[-1], torch.zeros(d)])  # rank 3: vh[-1] is in the null space
    r = H.ratios(H.ov_apply(w_o, w_v, 1, n_heads, n_kv, hd, x), x)
    assert r[0] == pytest.approx(float(s[0]), rel=1e-4)
    assert r[1] == pytest.approx(0.0, abs=1e-5)
    assert math.isnan(r[2])


# ---- attention capture --------------------------------------------------------------------------------------------


def forward(model, ids: torch.Tensor, **kw) -> None:
    """One forward of a tiny causal LM, or of the wrapped Muse text decoder."""
    inner: Any = model
    with torch.no_grad():
        (inner if hasattr(inner, "lm_head") else inner.model)(input_ids=ids, use_cache=False, **kw)


def eager_weights(model, ids: torch.Tensor, layer: int, q_pos: int) -> torch.Tensor:
    attn: Any = H.decoder_layers(model)[layer].self_attn
    seen: dict = {}

    def keep(_m, _a, _k, out):
        seen["w"] = out[1]

    handle = attn.register_forward_hook(keep, with_kwargs=True)
    try:
        forward(model, ids, output_attentions=True)
    finally:
        handle.remove()
    return seen["w"][0, :, q_pos].float()


@pytest.mark.parametrize("which", ["qwen", "muse"])
def test_capture_matches_eager_attention(which):
    """The last-token attention recomputed from the layer inputs equals eager attention's own weights on both
    architectures, for a NoPE / full layer and a RoPE / sliding layer of Muse (window 16 < the 26-token prompt, so the
    window matters), and for the 9B-style full-attention layers of the Qwen hybrid."""
    model = tiny_qwen("eager") if which == "qwen" else tiny_muse("eager")
    layers = [3, 7] if which == "qwen" else [5, 7]  # Muse: 5 sliding (RoPE), 7 full (NoPE)
    ids = ids_for(11, 26)
    q_pos = 25
    out: dict = {}
    with H.capture_last_attention(model, layers, q_pos, out):
        forward(model, ids)
    for la in layers:
        ref = eager_weights(model, ids, la, q_pos)
        assert out[la].shape == ref.shape == (4, 26)
        assert (out[la] - ref).abs().max() < 1e-5
        assert torch.allclose(out[la].sum(-1), torch.ones(4), atol=1e-5)
    if which == "muse":
        assert float(out[5][:, : 26 - 16].abs().max()) == 0.0  # the sliding window blocks keys at or before q - 16
        assert float(out[7][:, : 26 - 16].abs().max()) > 0.0  # the full (NoPE) layer reads them


def test_capture_refuses_a_linear_layer():
    model = tiny_qwen()
    with (
        pytest.raises(AssertionError, match="not a softmax-attention layer"),
        H.capture_last_attention(model, [2], 5, {}),
    ):
        pass


def test_candidate_layers_and_architecture():
    assert H.candidate_layers(TYPES, 3) == [7]
    assert H.candidate_layers(TYPES, 2) == [3, 7]
    assert H.candidate_layers([FULL] * 6, 2) == [3, 4, 5]
    a = H.architecture(tiny_muse().config, 3)
    assert a["candidate_layers"] == [4, 5, 6, 7] and a["config_full_attention"] == [7] and a["sliding_window"] == 16
    assert a["n_heads"] == 4 and a["n_kv"] == 2 and a["head_dim"] == 8 and a["candidate_heads"] == 16


# ---- selection and the rule -----------------------------------------------------------------------------------------


def test_select_heads_by_mean_mass_with_ties():
    mass = {(7, 0): [0.1, 0.3], (7, 1): [0.2, 0.2], (3, 2): [0.5, 0.1], (3, 0): [0.9, 0.0], (9, 1): [0.05, 0.05],
            (9, 0): [0.0, 0.3]}  # fmt: skip
    top = H.select_heads(mass, k=4)
    assert [(h["layer"], h["head"]) for h in top] == [
        (3, 0),
        (3, 2),
        (7, 0),
        (7, 1),
    ]  # 0.45, 0.3, 0.2, 0.2 (tie: lower layer, then head)
    assert top[0]["mean_mass"] == pytest.approx(0.45) and top[0]["median_mass"] == pytest.approx(0.45)
    assert [(h["layer"], h["head"]) for h in H.select_heads(mass, k=6)][-2:] == [(9, 0), (9, 1)]  # 0.25 before 0.05


def head(jpp, rest, address, random):
    r = {"jpp": jpp, "rest": rest, "address": address, "random": random}
    return {"r": r, "rule": H.head_rule(r)}


def test_head_rule_on_planted_numbers():
    assert H.head_rule({"jpp": 0.2, "rest": 0.4, "random": 0.3})["reads_rest"]  # exactly 2x, random between
    assert H.head_rule({"jpp": 0.2, "rest": 0.4, "random": 0.1})["reads_rest"]  # random below both
    assert H.head_rule({"jpp": 0.2, "rest": 0.4, "random": 0.4 + 1e-12})["reads_rest"]  # EPS at the bar
    assert not H.head_rule({"jpp": 0.2, "rest": 0.39, "random": 0.1})["reads_rest"]  # under 2x
    assert not H.head_rule({"jpp": 0.2, "rest": 0.4, "random": 0.5})["reads_rest"]  # random above the rest
    assert not H.head_rule({"jpp": math.nan, "rest": 0.4, "random": 0.1})["reads_rest"]


def test_model_and_batch_rules():
    good = [head(0.1, 0.3, 0.3, 0.2)] * 3 + [head(0.3, 0.3, 0.1, 0.2)] * 2
    m = H.model_rule(good)
    assert m["holds"] and m["heads_reading_rest"] == 3 and m["heads_address_at_least_rest"] == 3
    bad = [head(0.1, 0.3, 0.1, 0.2)] * 2 + [head(0.3, 0.3, 0.1, 0.2)] * 3
    assert not H.model_rule(bad)["holds"]
    tested = lambda holds: {"run": "r", "status": "tested", "holds": holds}  # noqa: E731
    pending = {"run": "p", "status": "pending", "holds": False}
    assert H.batch_verdict([tested(True), tested(True)])["label"] == "holds"
    assert H.batch_verdict([tested(True), tested(False)])["label"] == "does not hold"
    assert H.batch_verdict([tested(True), pending])["label"] == "pending"
    assert H.batch_verdict([tested(False), pending])["label"] == "does not hold"


def test_parse_answer_and_sealed_verdict(monkeypatch):
    text = "**Q48.3** (x)\n\nDan: yes\n\n**Q48.4** (y)\n- a / b\n\nRule: r.\n\nDan:\n\n**Q48.5** (z)\n\nDan: no\n"
    assert H.parse_answer(text, "Q48.4") == ""
    assert H.parse_answer(text.replace("Dan:\n\n**Q48.5", "Dan: yes 70%\n\n**Q48.5"), "Q48.4") == "yes 70%"
    assert H.parse_answer(text, "Q48.5") == "no"
    assert H.parse_answer("nothing", "Q48.4") == ""
    monkeypatch.setattr(H, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        H.stage_verdict(["qwen35_9b_x48_heads"], n_boot=10)


# ---- items ---------------------------------------------------------------------------------------------------------


CONTEXT_FIRST = (
    "Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of "
    "the frog is 5. Noah picked the tick. Iris picked the frog."
)  # both lockers before Iris's pick
CONTEXT_AFTER = (
    "Peter picked the rabbit. The locker of the tick is 2. Iris picked the frog. The locker of the frog "
    "is 5. Noah picked the tick. The locker of the rabbit is 1."
)  # the frog's locker after


def case(scene: str, context: str) -> dict:
    readers = {
        w: {
            "id": f"{w}-{scene}",
            "question": "Which locker belongs to Iris's pick?",
            "answer": "5",
            "cf_answer": "2",
            "ids": {"org": list(range(20)), "alt": list(range(20))},
        }
        for w in X.READERS
    }
    return {"scene": scene, "rendering": "chat", "domain": "animals", "bridge": "frog", "cf_bridge": "tick",
            "context": context, "cf_context": context, "pos": 7, "upstream": True, "readers": readers}  # fmt: skip


def fake_main_run(tmp_path, monkeypatch, target: str) -> str:
    from bridge_jspace import pins

    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0_necessity")
    monkeypatch.setattr(pins, "TARGET", target)
    run = "fake_main"
    d = tmp_path / "x0_necessity" / run
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps({"predicted": 12, "model": {"target": target}}))
    cases = [case("S-first", CONTEXT_FIRST), case("S-after", CONTEXT_AFTER), case("S-unread", CONTEXT_FIRST)]
    X.write_jsonl(d / "cases.jsonl", [*cases, {**case("S-raw", CONTEXT_FIRST), "rendering": "raw"}])
    rows = [{"scene": s, "rendering": "chat", "layer": la, "arm": "whole", "reader": X.LOOKUP}
            for s in ("S-after", "S-first") for la in (10, 12)] + [
           {"scene": "S-unread", "rendering": "chat", "layer": 10, "arm": "whole", "reader": X.LOOKUP}]  # fmt: skip
    X.write_jsonl(d / "outcomes.jsonl", rows)
    return run


def test_select_keeps_locker_first_scenes_read_at_L(tmp_path, monkeypatch):
    run = fake_main_run(tmp_path, monkeypatch, "qwen3.5-9b")
    items, counts = H.select(run, 12, [220])
    assert [it["scene"] for it in items] == ["S-first"]  # S-after: the frog's locker after; S-unread: not read at L12
    assert items[0]["space"] == [220] and items[0]["entity"] == "frog" and items[0]["pos"] == 7
    assert counts["items_at_L"] == 2 and counts["items"] == 1 and counts["max_read_len"] == 21
    assert counts["locker vs asked pick"] == {"org before, alt before": 1, "org after, alt before": 1}
    with pytest.raises(AssertionError, match="layer"):
        H.select(run, 10, [220])


# ---- the verdict on a planted run -----------------------------------------------------------------------------------


def planted_run(tmp_path, monkeypatch, run: str, target: str, r_by_head: list[dict], n_items: int = 12) -> None:
    monkeypatch.setattr(H, "RESULTS", tmp_path / "x48_heads")
    d = tmp_path / "x48_heads" / run
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "main_run": "m"}))
    (d / "plan.json").write_text(json.dumps({"items": n_items, "items_at_L": 20, "locker vs asked pick": {},
                                            "candidate_layers": [15], "config_full_attention": [15], "layer_types": {},
                                            "sliding_window": None, "max_read_len": 30, "n_heads": 2, "n_kv": 1,
                                            "head_dim": 4}))  # fmt: skip
    heads = [{"layer": 15, "head": i, "mean_mass": 0.5 - 0.05 * i, "median_mass": 0.4, "n": n_items,
              "recall_mean_mass": 0.1} for i in range(H.N_TOP)]  # fmt: skip
    (d / "heads.json").write_text(json.dumps({"selected_by": "lookup", "heads": heads}))
    items = [{"scene": f"S{i}", "entity": f"e{i % 4}", "domain": "animals", "cf_bridge": "tick", "pos": 3,
              "readers": {w: {"id": f"{w}-{i}", "answer": "5", "marked": "x ⟦bridge:frog⟧ y⟦read: ⟧"} for w in X.READERS}}
             for i in range(n_items)]  # fmt: skip
    X.write_jsonl(d / "cases.jsonl", items)
    rows = [{"scene": it["scene"], "entity": it["entity"], "layer": 15, "head": h, "variant": v, "lookup_mass": 0.4,
             "recall_mass": 0.1, "r": {p: r_by_head[h][p] * (1 + 0.01 * i) for p in H.PARTS}}
            for h in range(H.N_TOP) for v in H.VARIANTS for i, it in enumerate(items)]  # fmt: skip
    X.write_jsonl(d / "r_items.jsonl", rows)


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    """Both models planted: the 9B with 3 of 5 heads reading the rest (holds), Muse with 2 (does not); the batch does
    not hold; the markdown and the verify pack are written; a missing run is pending."""
    monkeypatch.setattr(H, "dan_answer", lambda rev="HEAD": "yes 60%")
    reads = {"jpp": 0.1, "rest": 0.3, "address": 0.35, "random": 0.2}
    flat = {"jpp": 0.3, "rest": 0.3, "address": 0.1, "random": 0.2}
    planted_run(tmp_path, monkeypatch, "qwen35_9b_x48_heads", "qwen3.5-9b", [reads] * 3 + [flat] * 2)
    planted_run(tmp_path, monkeypatch, "muse30_x48_heads", "muse-glimmer-30b", [reads] * 2 + [flat] * 3)
    out = H.stage_verdict(["qwen35_9b_x48_heads", "muse30_x48_heads"], n_boot=50)
    v = json.loads((out / "x48_heads.json").read_text())
    assert v["verdict"]["label"] == "does not hold" and v["verdict"]["Q48.4"] == "no"
    by = {m["target"]: m for m in v["models"]}
    assert by["qwen3.5-9b"]["holds"] and by["qwen3.5-9b"]["heads_reading_rest"] == 3
    assert by["qwen3.5-9b"]["heads_address_at_least_rest"] == 3
    assert not by["muse-glimmer-30b"]["holds"] and by["muse-glimmer-30b"]["heads_reading_rest"] == 2
    h0 = by["qwen3.5-9b"]["selected_heads"][0]
    assert h0["ov"]["rest"][0] == pytest.approx(0.3 * (1 + 0.01 * 5.5), rel=1e-6)  # the median of 12 planted values
    assert h0["ov"]["rest"][1] <= h0["ov"]["rest"][0] <= h0["ov"]["rest"][2]
    md = (out / "x48_heads.md").read_text()
    assert "**Verdict: does not hold**" in md and "| qwen3.5-9b | L15:h00 |" in md
    ex = (out / "examples.md").read_text()
    assert ex.count("### S") == 2 * 10 and "⟦bridge:frog⟧" in ex
    out2 = H.stage_verdict(["qwen35_9b_x48_heads"], n_boot=50)
    v2 = json.loads((out2 / "x48_heads.json").read_text())
    assert v2["verdict"]["label"] == "pending" and v2["verdict"]["pending"] == ["(muse30_x48_heads)"]
