"""53.4 (Lightning attention blocks 19 / 26): knockout.knock_out on NemotronH's softmax-attention blocks (a tiny random
NemotronH from transformers' own classes, CPU, MLP and attention blocks only): the masked edge carries zero attention
weight and the knocked queries' other weights renormalise over the keys they still read, as in 47.6; sdpa and eager
agree; x47_edges.forward leaves an unknocked row of the batch as the plain forward. The script's pure parts: blocks per
arm, the control's source, the rule."""

import math
import types

import pytest
import torch

transformers = pytest.importorskip("transformers")

from bridge_jspace.knockout import FULL, LINEAR, OTHER, knock_out  # noqa: E402
from scripts import x53_attnblock as AB  # noqa: E402

KINDS = ["mlp", "full_attention", "mlp", "full_attention"]


def tiny(attn: str = "eager"):
    from transformers import NemotronHConfig, NemotronHForCausalLM

    cfg = NemotronHConfig(vocab_size=64, hidden_size=32, num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                          intermediate_size=48, layers_block_type=list(KINDS), num_hidden_layers=len(KINDS),
                          attn_implementation=attn)  # fmt: skip
    torch.manual_seed(0)
    return NemotronHForCausalLM(cfg).eval()


def weights(m, ids, knock=None) -> dict[int, torch.Tensor]:
    """Each attention block's eager softmax weights [b, heads, T, T], with an optional knock_out(layers, src, dst)."""
    seen = {}

    def keep(la):
        return lambda _m, _a, out: seen.__setitem__(la, out[1].detach().clone())

    handles = [m.model.layers[la].mixer.register_forward_hook(keep(la)) for la in (1, 3)]
    try:
        with torch.no_grad():
            if knock is None:
                m(ids)
            else:
                with knock_out(m, *knock):
                    m(ids)
    finally:
        for h in handles:
            h.remove()
    return seen


def test_masked_edge_has_zero_weight_and_the_rest_renormalises():
    m = tiny()
    ids = torch.randint(0, 64, (1, 10), generator=torch.Generator().manual_seed(1))
    src, dst = 4, list(range(5, 10))
    w0 = weights(m, ids)
    w1 = weights(m, ids, ([1, 3], [[src]], [dst]))
    for la in (1, 3):
        assert (w1[la][0, :, dst, src] == 0).all()
        assert torch.allclose(w1[la][0].sum(-1), torch.ones(4, 10), atol=1e-5)
    # block 1 is the first knocked block and block 0 mixes no tokens: its queries' inputs are the unknocked ones, so a
    # knocked query's weights are the unknocked ones over the keys it still reads, renormalised
    a, b = w0[1][0], w1[1][0]
    expect = a[:, dst].clone()
    expect[:, :, src] = 0
    expect = expect / expect.sum(-1, keepdim=True)
    assert torch.allclose(b[:, dst], expect, atol=1e-5)
    assert torch.allclose(b[:, : src + 1], a[:, : src + 1], atol=1e-6)  # queries up to the source: untouched
    assert not torch.allclose(w1[3][0][:, dst], w0[3][0][:, dst], atol=1e-4)  # block 3 is knocked too


def test_sdpa_and_eager_agree_under_the_knock_out():
    ids = torch.randint(0, 64, (2, 9), generator=torch.Generator().manual_seed(2))
    knock = ([[1], [1, 3]], [[3], [6]], [[4, 5, 6, 7, 8], [7, 8]])
    out = {}
    for attn in ("eager", "sdpa"):
        m = tiny(attn)
        with torch.no_grad(), knock_out(m, *knock):
            out[attn] = m(ids).logits.float()
    assert torch.allclose(out["eager"], out["sdpa"], atol=1e-5)


def test_knock_out_refuses_a_block_that_is_not_softmax_attention():
    m = tiny()
    ids = torch.randint(0, 64, (1, 6), generator=torch.Generator().manual_seed(3))
    match = "knock_out supports Gated DeltaNet and softmax attention"
    with pytest.raises(AssertionError, match=match), torch.no_grad(), knock_out(m, [0], [[2]], [[3, 4, 5]]):
        m(ids)


def test_x47_edges_forward_keeps_an_unknocked_row_as_the_plain_forward():
    from scripts import x47_edges as E

    m = tiny()
    model = types.SimpleNamespace(hf=m, layers=m.model.layers)
    ids = torch.randint(0, 64, (1, 9), generator=torch.Generator().manual_seed(4)).tolist()[0]
    vec = torch.randn(32, generator=torch.Generator().manual_seed(5))
    with torch.no_grad():
        plain = m(torch.tensor([ids])).logits[0, -1].float()
        logits, _ = E.forward(model, [ids] * 3, [None, None, [(1, 4, vec)]],
                              [None, ([1, 3], [4], list(range(5, 9))), ([3], [4], list(range(5, 9)))])  # fmt: skip
    assert torch.allclose(logits[0], plain, atol=1e-5)
    assert not torch.allclose(logits[1], plain, atol=1e-4)


# ---- the script's pure parts --------------------------------------------------------------------------------------

LIGHTNING_LIKE = [OTHER] * 52
for _la in (5, 12, 19, 26, 33, 42):
    LIGHTNING_LIKE[_la] = FULL
for _la in (0, 2, 4, 7, 9, 11, 14, 16, 18, 21, 23, 25, 28, 30, 32, 35, 37, 39, 41, 44, 46, 48, 50):
    LIGHTNING_LIKE[_la] = LINEAR


def test_arm_layers_on_lightnings_layout():
    sets = AB.arm_layers(LIGHTNING_LIKE, 14)
    assert sets == {"b19": [19], "b26": [26], "both": [19, 26], "after": [19, 26, 33, 42], "control": [19, 26]}
    with pytest.raises(AssertionError, match="not all softmax attention after"):
        AB.arm_layers(LIGHTNING_LIKE, 20)


def test_control_source_is_seeded_per_scene_and_never_the_bridge():
    cands = [10, 11, 13, 14]
    a = AB.control_position("P2-L0-0002", cands)
    assert a == AB.control_position("P2-L0-0002", list(reversed(cands))) and a in cands
    assert len({AB.control_position(f"s{i}", cands) for i in range(40)}) > 1
    with pytest.raises(AssertionError, match="no non-bridge token"):
        AB.control_position("s", [])


def test_knock_of_every_position_after_the_source():
    sets = AB.arm_layers(LIGHTNING_LIKE, 14)
    assert AB.knock_of("none", sets, 12, 10, 30) is None
    assert AB.knock_of("both", sets, 12, 10, 30) == ([19, 26], [12], list(range(13, 30)))
    assert AB.knock_of("control", sets, 12, 10, 30) == ([19, 26], [10], list(range(11, 30)))
    assert AB.knock_of("after", sets, 12, 14, 30)[0] == [19, 26, 33, 42]


def cuts(i, ii, iii, iv, v):
    return {"i": i, "ii": ii, "iii": iii, "iv": iv, "v": v}


def test_rule_labels_in_the_rules_order():
    assert AB.label(cuts(0.2, 0.3, 0.6, 0.8, 0.15))["label"] == "read through two blocks"
    assert AB.label(cuts(0.2, 0.3, 0.6, 0.8, 0.16))["label"] == "in between"  # the control cuts too much
    two_and_one = AB.label(cuts(0.7, 0.1, 0.9, 0.9, 0.0))
    assert two_and_one["label"] == "read through two blocks" and two_and_one["also"] == ["one block"]
    assert AB.label(cuts(0.1, 0.6, 0.5, 0.7, 0.0))["label"] == "one block"
    assert AB.label(cuts(0.0, 0.0, 0.1, 0.29, 0.0))["label"] == "not through attention at the bridge"
    assert AB.label(cuts(0.0, 0.0, 0.1, 0.3, 0.0))["label"] == "in between"  # '< 0.3' is strict
    assert AB.label(cuts(math.nan, 0, 0, 0, 0))["label"].startswith("not tested")


def test_reader_numbers_cut_and_collateral():
    rows = []
    for i in range(10):
        for a in AB.ARMS:
            sw = {"none": i < 8, "both": i < 2}.get(a, i < 8)
            rows.append({"scene": f"s{i}", "entity": f"e{i % 5}", "reader": "PP", "arm": a, "patch": "whole",
                         "switched": int(sw), "edges": 3})  # fmt: skip
            rows.append({"scene": f"s{i}", "entity": f"e{i % 5}", "reader": "PP", "arm": a, "patch": "clean",
                         "switched": 0, "role": "A" if a != "after" or i < 5 else "other", "edges": 3})  # fmt: skip
    r = AB.reader_numbers(rows, "PP", n_boot=200)
    assert r["S"]["none"] == 0.8 and r["S"]["both"] == 0.2
    assert r["cut"]["both"] == pytest.approx(0.75) and r["cut"]["b19"] == pytest.approx(0.0)
    assert r["clean_kept"]["none"] == 1.0 and r["clean_kept"]["after"] == 0.5
    lo, hi = r["cut_ci"]["both"]
    assert lo <= 0.75 <= hi


def test_rule_is_dans_text_verbatim():
    import re

    import yaml

    spec = yaml.safe_load((AB.SPEC).read_text())["lightning_attn_block"]
    found = re.search(r"Rule: (.*?else in between\.)", " ".join(spec.split()))
    assert found is not None and found.group(1) == AB.RULE


def test_verdict_on_a_planted_run(tmp_path, monkeypatch):
    """The verdict reads the run's rows: the lookup's cuts per rule arm and the label; the recall beside; x53_attnblock-
    <UTC>/ with the rule verbatim and no prediction."""
    import json

    monkeypatch.setattr(AB, "RESULTS", tmp_path)
    run = tmp_path / AB.RUN
    run.mkdir()
    sets = AB.arm_layers(LIGHTNING_LIKE, 14)
    (run / "manifest.json").write_text(json.dumps({"layer": 14, "arm_layers": sets, "items": {
        "items": 20, "entities": 5, "control_before_bridge": 12}}))  # fmt: skip
    # lookup: 10 of 20 switch with no block; both blocks keep 2 (cut 0.8), the control 9 (cut 0.1), one block 6 (0.4)
    keep = {"none": 10, "b19": 6, "b26": 6, "both": 2, "after": 1, "control": 9}
    rows, items = [], []
    for i in range(20):
        s = f"s{i}"
        items.append({"scene": s, "sentence_text": "Eve picked beta.", "bridge_token": " beta", "control_token": "E",
                      "stored_whole": {"PP": int(i < 10), "PM": 1}})  # fmt: skip
        for w in ("PP", "PM"):
            for a in AB.ARMS:
                for p in AB.PATCHES:
                    sw = int(p == "whole" and (i < keep[a] if w == "PP" else True))
                    rows.append({"scene": s, "entity": f"e{i % 5}", "reader": w, "arm": a, "patch": p, "switched": sw,
                                 "role": "b" if sw else "A", "top_text": "x", "edges": 3})  # fmt: skip
    X = AB.X
    X.write_jsonl(run / "outcomes.jsonl", rows)
    X.write_jsonl(run / "items.jsonl", items)
    out = AB.stage_verdict(n_boot=200)
    blob = json.loads((out / "verdict.json").read_text())
    text = (out / "verdict.md").read_text()
    assert out.name.startswith("x53_attnblock-") and blob["label"]["label"] == "read through two blocks"
    assert blob["readers"]["lookup"]["cut"]["both"] == pytest.approx(0.8)
    assert blob["readers"]["recall"]["cut"]["both"] == 0.0 and blob["agreement"]["PP"]["agree"] == 1.0
    assert AB.RULE in text and AB.NO_PREDICTION in text and "UNVERIFIED" in text
