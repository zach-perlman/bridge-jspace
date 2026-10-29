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


# ---- the 53.4 follow-up (Dan 11:10): the bridge-to-scene-end span and its control ----------------------------------


def test_span_and_control_on_a_planted_scene():
    """Scene tokens 8..40, the bridge word at 30, the question 42..50: the span is 30..40 (11 tokens); a control of 11
    tokens fits with starts 8..19 (it must end before the bridge word); the control never meets the span or the
    question and has the span's length."""
    sp = AB.span_positions(30, (8, 40), list(range(42, 51)))
    assert sp is not None and sp["span"] == list(range(30, 41)) and sp["starts"] == list(range(8, 20))
    ctrl = AB.control_span("s1", sp["starts"], len(sp["span"]))
    assert len(ctrl) == len(sp["span"]) and ctrl[-1] < 30 and ctrl[0] >= 8
    assert not set(ctrl) & set(sp["span"]) and not set(ctrl) & set(range(42, 51))
    assert ctrl == AB.control_span("s1", sp["starts"], 11)  # seeded per scene
    # the bridge word early: 31 tokens of span, 2 before it in the scene: no control fits
    assert AB.span_positions(10, (8, 40), list(range(42, 51))) is None
    # position 0 is never a source: a scene starting at 0 starts its controls at 1
    sp0 = AB.span_positions(12, (0, 14), [16, 17])
    assert sp0 is not None and min(sp0["starts"]) == 1


def test_control_never_overlaps_and_lengths_match_over_random_scenes():
    import random as rnd

    g = rnd.Random(0)
    fits = 0
    for i in range(500):
        first = g.randint(1, 20)
        last = first + g.randint(5, 60)
        pos = g.randint(first, last)
        question = list(range(last + 2, last + 2 + g.randint(3, 12)))
        sp = AB.span_positions(pos, (first, last), question)
        if sp is None:
            assert last - pos + 1 > pos - first  # no room before the bridge word
            continue
        fits += 1
        ctrl = AB.control_span(f"s{i}", sp["starts"], len(sp["span"]))
        assert len(ctrl) == len(sp["span"]) == last - pos + 1
        assert not set(ctrl) & set(sp["span"]) and not set(ctrl) & set(question)
        assert first <= ctrl[0] and ctrl[-1] < pos and 0 not in ctrl
    assert fits > 100


def test_span_knock_masks():
    sets = AB.arm_layers(LIGHTNING_LIKE, 14)
    it = {"scene": "s", "pos": 30, "control": 28, "scene_end": 40, "span": list(range(30, 41)),
          "span_control": list(range(12, 23))}  # fmt: skip
    n = 52
    k_span, k_ctrl = AB.span_knock("span", sets, it, n), AB.span_knock("span_ctrl", sets, it, n)
    assert k_span is not None and k_ctrl is not None
    blocks, src, dst = k_span
    assert blocks == [19, 26] and src == it["span"] and dst == list(range(41, 52))
    blocks_c, src_c, dst_c = k_ctrl
    assert blocks_c == blocks and src_c == it["span_control"] and dst_c == dst and len(src_c) == len(src)
    assert (
        AB.span_knock("both", sets, it, n) == AB.knock_of("both", sets, 30, 28, n)
        and AB.span_knock("none", sets, it, n) is None
    )


@pytest.mark.parametrize(
    ("span", "ctrl", "want"),
    [(0.6, 0.15, AB.SPAN_LABEL), (0.59, 0.0, AB.LABELS[3]), (0.8, 0.16, AB.LABELS[3]), (0.29, 0.0, AB.LABELS[2]),
     (0.3, 0.3, AB.LABELS[3]), (math.nan, 0.0, "not tested (nothing switched under the whole change)")],
)  # fmt: skip
def test_span_rule_and_else_as_53_4(span, ctrl, want):
    assert AB.label_span(span, ctrl) == want


def test_span_mask_on_nemotronh_zeroes_every_span_edge():
    """knock_out with the span as sources and the positions after the scene as destinations, on the tiny NemotronH: every
    (destination, span) weight is 0 in both attention blocks; attention inside the span is untouched."""
    m = tiny()
    ids = torch.randint(0, 64, (1, 14), generator=torch.Generator().manual_seed(4))
    span, dst = list(range(5, 10)), list(range(10, 14))
    w0 = weights(m, ids)
    w1 = weights(m, ids, ([1, 3], [span], [dst]))
    for la in (1, 3):
        assert (w1[la][0][:, dst][:, :, span] == 0).all()
        assert torch.allclose(
            w1[la][0][:, :10], w0[la][0][:, :10], atol=1e-6
        )  # the queries up to the scene's end as is


@pytest.mark.parametrize("placement", ["seeded", "c"])
def test_span_verdict_on_planted_reads(tmp_path, monkeypatch, placement):
    import json

    monkeypatch.setattr(AB, "RESULTS", tmp_path)
    run = tmp_path / AB.RUN_SPAN
    run.mkdir()
    counts = {"items": 30, "entities": 5, "control_before_bridge": 0, "span_items_in_rule": 20,
              "span_dropped_no_control_fits": 10, "span_entities_in_rule": 5, "span_tokens_in_rule": [2, 8, 15],
              "span_tokens_all": [2, 12, 30]}  # fmt: skip
    (run / "manifest.json").write_text(json.dumps({"layer": 14, "arm_layers": AB.arm_layers(LIGHTNING_LIKE, 14),
                                                   "items": counts, "control_placement": placement}))  # fmt: skip
    # the rule's 20 scenes: 10 switch with no block, the span keeps 3 (cut 0.7), the control 9 (cut 0.1)
    keep = {"none": 10, "both": 6, "span": 3, "span_ctrl": 9}
    rows, items = [], []
    for i in range(30):
        s, ok = f"s{i}", i < 20
        items.append(
            {
                "scene": s,
                "in_rule": ok,
                "span": list(range(10 if ok else 20)),
                "span_text": " beta. ...",
                "control_text": "Eve" if ok else None,
                "span_to_question": 1,
                "control_to_question": 12 if ok else None,
            }
        )
        for w in ("PP", "PM"):
            for a in AB.SPAN_ARMS if ok else AB.SPAN_ARMS[:3]:
                for p in AB.PATCHES:
                    sw = int(p == "whole" and (i % 20 < keep[a] if w == "PP" else True))
                    rows.append({"scene": s, "entity": f"e{i % 5}", "reader": w, "arm": a, "patch": p, "switched": sw,
                                 "role": "b" if sw else "A", "top_text": "x", "edges": 3, "in_rule": ok})  # fmt: skip
    AB.X.write_jsonl(run / "outcomes.jsonl", rows)
    AB.X.write_jsonl(run / "items.jsonl", items)
    out = AB.stage_verdict_span(n_boot=200)
    blob = json.loads((out / "verdict.json").read_text())
    stem = "x53_attnspan-" if placement == "seeded" else "x53_attnspan_c-"
    assert out.name.startswith(stem) and blob["label"] == AB.SPAN_LABEL and blob["control_placement"] == placement
    assert blob["to_question_median"] == {"span": 1.0, "control": 12.0}
    assert ("flagged to Dan" in (out / "verdict.md").read_text()) == (placement == "c")
    assert blob["readers"]["lookup"]["n"] == 20 and blob["readers"]["lookup"]["cut"]["span"] == pytest.approx(0.7)
    assert (
        blob["readers"]["lookup"]["cut"]["span_ctrl"] == pytest.approx(0.1) and blob["beside_all"]["lookup"]["n"] == 30
    )
    text = (out / "verdict.md").read_text()
    assert AB.RULE_SPAN in text and "Dan 11:10" in text and "UNVERIFIED" in text and "dropped from the rule" in text
    sel = blob["selection"]
    assert (sel["rule_scenes"], sel["dropped_scenes"]) == (20, 10) and sel["median_span_tokens"] == {
        "rule": 10.0,
        "dropped": 20.0,
        "all": 10.0,
    }
    label_line = next(ln for ln in text.splitlines() if ln.startswith("Label (lookup)"))
    assert "on the 20" in label_line and "on all 30" in label_line and "median span 10.0 tokens" in label_line


def test_placement_c_ends_just_before_the_bridge_sentence():
    """Dan 11:25 (placement c): the control ends at the last token before the bridge's sentence; deterministic; never the
    sentence, the span or the question; the span's length; None when it does not fit inside the scene."""
    # scene 8..40; the bridge's sentence 26..31 with the bridge word at 30; the span 30..40 (11 tokens)
    ctrl = AB.control_before_sentence(26, 8, 11)
    assert ctrl == list(range(15, 26)) and ctrl == AB.control_before_sentence(26, 8, 11)
    assert not set(ctrl) & set(range(26, 41)) and len(ctrl) == 11
    assert AB.control_before_sentence(26, 16, 11) is None  # would start before the scene
    assert AB.control_before_sentence(11, 0, 11) is None  # would reach position 0
    assert AB.control_before_sentence(12, 0, 11) == list(range(1, 12))


def test_placement_c_over_random_scenes():
    import random as rnd

    g = rnd.Random(1)
    fits = 0
    for _ in range(500):
        first = g.randint(1, 20)
        last = first + g.randint(8, 60)
        s0 = g.randint(first, last - 2)
        pos = g.randint(s0, min(s0 + 5, last))
        question = list(range(last + 2, last + 8))
        n = last - pos + 1
        ctrl = AB.control_before_sentence(s0, first, n)
        if ctrl is None:
            assert s0 - n < max(first, 1)
            continue
        fits += 1
        assert len(ctrl) == n and ctrl[-1] == s0 - 1 and ctrl[0] >= first
        assert not set(ctrl) & set(range(s0, last + 1)) and not set(ctrl) & set(question)
    assert fits > 50
