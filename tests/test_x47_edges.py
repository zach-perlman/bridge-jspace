"""x47_edges (batch 47, test 47.6): the edge sets (sources, destinations, layers, matched counts), the positions on the
target's tokenizer, the batched forward (adds, knock-outs, record) on test_knockout's tiny Qwen3.5 hybrid, Muse
Glimmer's attention capture against eager attention weights, the formation rule on planted rows, and the seal. Part
(c) is dropped (Dan, amendment 1): its edge sets and --with-c path are tested so the kept code stays alive; no rule."""

from __future__ import annotations

import json
import math
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from bridge_jspace.knockout import FULL, LINEAR, decoder_layers, knock_out
from scripts import x0_necessity as X
from scripts import x47_edges as E
from tests.test_knockout import ABS, DEVICE, ids_for, tiny_model

LK, RC = X.LOOKUP, X.RECALL
QWEN9B = [LINEAR, LINEAR, LINEAR, FULL] * 8  # Qwen3.5-9B's 32 blocks


def positions(n_filler: int = 27) -> dict:
    """A filler scene's positions as the 9B's tokenizer gives them: filler 2..28, three 9-token locker sentences,
    two other pick sentences, the asked pick sentence 70..74 (bridge 73), questions from 76."""
    return {"lockers": [list(range(29, 38)), list(range(38, 47)), list(range(47, 56))],
            "filler": list(range(2, 2 + n_filler)), "pick": list(range(70, 75)), "bridge": [73],
            "question": {LK: list(range(76, 105)), RC: list(range(76, 106))}}  # fmt: skip


# ---- edge sets ------------------------------------------------------------------------------------------------------


def test_layer_sets_hybrid_and_softmax_only():
    sets = E.layer_sets(QWEN9B, 12)
    assert sets["all"] == {"pre": list(range(13)), "post": list(range(12, 32))}
    assert sets["attn"] == {"pre": [3, 7, 11], "post": [15, 19, 23, 27, 31]}
    muse = E.layer_sets([FULL] * 52, 26)
    assert set(muse) == {"all"}
    assert muse["all"]["pre"] == list(range(27))
    assert muse["all"]["post"] == list(range(26, 52))


def test_formation_arms_sources_dests_layers_and_matched_counts():
    p = positions()
    sets = E.layer_sets(QWEN9B, 12)
    arms = E.formation_arms(p, sets, QWEN9B)
    lockers = list(range(29, 56))
    assert set(arms) == {
        f"{k}/{d}/{s}" for k in ("block", "control") for d in ("sentence", "bridge") for s in ("all", "attn")
    }
    for name, a in arms.items():
        kind, dests, layers = name.split("/")
        assert a["src"] == (lockers if kind == "block" else p["filler"])
        assert a["dst"] == (p["pick"] if dests == "sentence" else [73])
        assert a["layers"] == sets[layers]["pre"]
        assert a["edges"] == 27 * len(a["dst"]) * len(a["layers"])
        assert a["edges"] == arms[f"{'control' if kind == 'block' else 'block'}/{dests}/{layers}"]["edges"]
        assert a["edges_full_attention"] + a["edges_deltanet"] == a["edges"]
    assert arms["block/sentence/all"]["edges"] == 1755  # the plan's count on the 9B
    assert arms["block/sentence/attn"]["edges"] == 405
    assert arms["block/sentence/attn"]["edges_deltanet"] == 0
    assert arms["block/bridge/all"]["edges_full_attention"] == 27 * 3


def test_dereference_arms_per_reader():
    p = positions()
    sets = E.layer_sets(QWEN9B, 12)
    for w, n_q in ((LK, 29), (RC, 30)):
        arms = E.dereference_arms(p, sets, QWEN9B, w)
        assert set(arms) == {"block/all", "control/all", "block/attn", "control/attn"}
        assert arms["block/all"]["dst"] == p["question"][w]
        assert arms["block/all"]["layers"] == list(range(12, 32))
        assert arms["control/attn"]["layers"] == [15, 19, 23, 27, 31]
        assert arms["block/all"]["edges"] == arms["control/all"]["edges"] == 27 * n_q * 20
        assert arms["block/attn"]["edges"] == arms["control/attn"]["edges"] == 27 * n_q * 5


def test_a_filler_of_another_length_is_refused():
    with pytest.raises(AssertionError, match="filler 26 tokens"):
        E.formation_arms(positions(26), E.layer_sets(QWEN9B, 12), QWEN9B)
    with pytest.raises(AssertionError, match="filler 26 tokens"):
        E.dereference_arms(positions(26), E.layer_sets(QWEN9B, 12), QWEN9B, LK)


def test_edge_count_drops_pairs_that_read_ahead():
    kinds = [FULL, LINEAR, FULL]
    c = E.edge_count([5, 9], [7, 8], [0, 1, 2], kinds)
    assert c == {"pairs": 2, "n_layers": 3, "edges": 6, "edges_full_attention": 4, "edges_deltanet": 2}


def test_edge_table_keeps_counts_only():
    t = E.edge_table(E.formation_arms(positions(), E.layer_sets(QWEN9B, 12), QWEN9B))
    assert set(t["block/sentence/all"]) == {"pairs", "n_layers", "edges", "edges_full_attention", "edges_deltanet"}


# ---- marks ----------------------------------------------------------------------------------------------------------


def test_marked_nests_and_closes_spans():
    decode = lambda ids: "".join(chr(97 + i) for i in ids)  # noqa: E731
    text = E.marked(decode, list(range(8)), {"pick": [2, 3, 4], "patch": [3], "q": [6, 7]})
    assert text == "ab⟦pick: c⟦patch: d⟧e⟧f⟦q: gh⟧"
    with pytest.raises(AssertionError):
        E.marked(decode, list(range(8)), {"x": [1, 2, 3], "y": [3, 4]})
    with pytest.raises(AssertionError, match="contiguous"):
        E.marked(decode, list(range(8)), {"x": [1, 3]})


# ---- positions on the target's tokenizer (skipped where it is not cached) --------------------------------------------


@pytest.fixture(scope="module")
def tok():
    try:
        return E.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


def test_filler_cases_and_spans_on_the_tokenizer(tok):
    base = E.plain_cases(tok, 8)
    cases, dropped = E.filler_cases(tok, base)
    assert len(cases) == len(base)
    assert not dropped
    for b, c in zip(base, cases, strict=True):
        assert c["context"] == f"{E.FILLER} {b['context']}"
        assert c["cf_context"] == f"{E.FILLER} {b['cf_context']}"
        assert c["expect"] == b["expect"]
        p = E.spans(tok, c)
        flat = [t for s in p["lockers"] for t in s]
        assert len(p["filler"]) == len(flat) == 27  # the filler's design: the three locker sentences' total
        lk = c["readers"][LK]["ids"]
        assert tok.decode([lk["org"][t] for t in p["filler"]]).strip() == E.FILLER
        assert tok.decode([lk["org"][t] for t in p["pick"]]).strip() == f"{E.R.asked_of(c)} picked the {c['bridge']}."
        assert (
            tok.decode([lk["alt"][t] for t in p["pick"]]).strip() == f"{E.R.asked_of(c)} picked the {c['cf_bridge']}."
        )
        for w in X.READERS:
            q = p["question"][w]
            n = len(c["readers"][w]["ids"]["org"]) + len(c["space"])
            assert q[-1] == n - 1
            assert tok.decode([c["readers"][w]["ids"]["org"][q[0]]]).strip().split()[0] in ("Which", "How")
        decode = lambda ids: tok.decode(ids, skip_special_tokens=False)  # noqa: E731
        ids = lk["org"] + c["space"]
        text = E.marked(decode, ids, E.marks_of(p, LK))
        for mark in ("⟦filler: ", "⟦src-locker1: ", "⟦dst-b: ", "⟦patch: ", "⟦dst-c: "):
            assert text.count(mark) == 1
        assert re.sub(r"⟦[a-z0-9-]+: ", "", text).replace("⟧", "") == decode(ids)  # the marks only add brackets


def test_plain_scenes_have_no_filler(tok):
    c = E.plain_cases(tok, 4)[0]
    p = E.spans(tok, c)
    assert p["filler"] == []
    assert [len(s) for s in p["lockers"]] == [9, 9, 9]


# ---- the batched forward on the tiny hybrid ---------------------------------------------------------------------------


def wrap(hf):
    return SimpleNamespace(hf=hf, layers=decoder_layers(hf))


def test_forward_plain_rows_equal_the_hf_forward():
    hf = tiny_model()
    ids = ids_for(3, 14, 2).tolist()
    lg, h = E.forward(wrap(hf), ids)
    with torch.no_grad():
        ref = hf(input_ids=torch.tensor(ids, device=DEVICE), use_cache=False, logits_to_keep=1).logits[:, -1].float()
    assert h is None
    assert lg is not None
    assert torch.allclose(lg, ref, atol=ABS)


def test_forward_record_stops_at_the_block_and_matches_hidden_states():
    hf = tiny_model()
    ids = ids_for(4, 12, 2).tolist()
    lg, h = E.forward(wrap(hf), ids, record=(4, 6))
    with torch.no_grad():
        hs = hf(input_ids=torch.tensor(ids, device=DEVICE), use_cache=False, output_hidden_states=True).hidden_states
    assert lg is None
    assert h is not None
    assert torch.allclose(h, hs[5][:, 6].float(), atol=ABS)  # hidden_states[i + 1]: block i's output


def test_forward_adds_per_row_at_one_position():
    hf = tiny_model()
    m = wrap(hf)
    ids = ids_for(5, 12, 1).tolist() * 3
    vec = torch.randn(32, generator=torch.Generator().manual_seed(0))
    _, h0 = E.forward(m, ids, record=(3, 5))
    adds = [None, [(3, 5, vec)], [(3, 5, torch.zeros(32))]]
    _, h = E.forward(m, ids, adds=adds, record=(3, 5))
    assert h is not None
    assert h0 is not None
    assert torch.allclose((h[1] - h0[1]).cpu(), vec, atol=1e-5)  # the record at the add's own block sees the sum
    assert torch.equal(h[0], h0[0])
    assert torch.equal(h[2], h0[2])
    lg, _ = E.forward(m, ids, adds=adds)
    lg0, _ = E.forward(m, ids)
    assert lg is not None
    assert lg0 is not None
    assert torch.equal(lg[0], lg0[0])
    assert (lg[1] - lg0[1]).abs().max() > 1e-3  # the add reaches the last position


def test_forward_knocks_only_its_rows_as_knock_out_does():
    hf = tiny_model()
    m = wrap(hf)
    ids = ids_for(6, 16, 1).tolist() * 3
    src, dst, layers = [2, 3, 4], [9, 10, 11], list(range(6))
    lg, _ = E.forward(m, ids, knock=[None, (layers, src, dst), None])
    plain, _ = E.forward(m, ids[:1])
    with knock_out(hf, layers, [src], [dst]), torch.no_grad():
        ref = hf(input_ids=torch.tensor(ids[:1], device=DEVICE), use_cache=False).logits[:, -1].float()
    assert lg is not None
    assert plain is not None
    assert torch.allclose(lg[1], ref[0], atol=ABS)
    assert torch.allclose(lg[0], plain[0], atol=ABS)
    assert torch.allclose(lg[2], plain[0], atol=ABS)
    assert (lg[1] - plain[0]).abs().max() > 0.1  # the knock-out moves the last position's logits


def test_forward_records_the_change_formed_under_a_block():
    """(b)'s formation forward: O and S rows, the block at layers 0..L only on the knocked pair; the destinations'
    record at L moves, a row whose destinations precede the sources' end does not (nothing reads ahead)."""
    hf = tiny_model()
    m = wrap(hf)
    o, s = ids_for(7, 12, 1).tolist()[0], ids_for(7, 12, 1).tolist()[0]
    s[8] = (s[8] + 1) % 61  # S differs at the "bridge" (position 8)
    rows = [o, s, o, s]
    k = (list(range(5)), [2, 3, 4], [6, 7, 8])
    _, h = E.forward(m, rows, knock=[None, None, k, k], record=(4, 8))
    assert h is not None
    d0, d1 = h[1] - h[0], h[3] - h[2]
    assert (d0 - d1).norm() / d0.norm() > 1e-3
    _, h2 = E.forward(m, rows, knock=[None, None, (list(range(5)), [9, 10], [6, 7, 8]), None], record=(4, 8))
    assert h2 is not None
    assert torch.allclose(h2[2], h2[0], atol=ABS)  # sources after the destinations: no edge, no change


# ---- Muse Glimmer's attention capture (a tiny random text model, no download) ----------------------------------------


def tiny_muse(impl: str, window: int = 5):
    from transformers.models.muse_glimmer.configuration_muse_glimmer import MuseGlimmerTextConfig
    from transformers.models.muse_glimmer.modeling_muse_glimmer import MuseGlimmerTextModel

    cfg = MuseGlimmerTextConfig(vocab_size=61, hidden_size=32, intermediate_size=48, num_hidden_layers=4,
                                num_attention_heads=4, num_key_value_heads=2, head_dim=8, sliding_window=window,
                                max_position_embeddings=64, rope_parameters={"rope_theta": 10000.0, "rope_type": "default"})  # fmt: skip
    cfg._attn_implementation = impl
    torch.manual_seed(0)
    model = MuseGlimmerTextModel(cfg).eval()
    g = torch.Generator().manual_seed(0)
    with torch.no_grad():
        for _, p in model.named_parameters():
            if p.ndim >= 2:
                p.copy_(torch.randn(p.shape, generator=g) / math.sqrt(p.shape[-1]))
    return model


@pytest.mark.parametrize("impl", ["eager", "sdpa"])
def test_muse_capture_matches_eager_attention_weights(impl):
    model = tiny_muse(impl)
    types, theta = model.config.layer_types, model.config.layer_rope_theta
    assert types is not None
    assert theta is not None
    assert types[3] == "full_attention"
    assert theta[3] == 0  # the global layer is NoPE
    ids = ids_for(8, 11, 2).cpu()
    q = [10, 7]
    got: dict = {}
    with torch.no_grad(), E.muse_capture(model.layers, [0, 1, 2, 3], q, got):
        model(input_ids=ids, use_cache=False)
    eager = tiny_muse("eager")
    with torch.no_grad():
        ref = eager(input_ids=ids, use_cache=False, output_attentions=True).attentions
    for la in range(4):
        assert got[la].shape == (2, 4, 2, 11)
        assert torch.allclose(got[la], ref[la][:, :, q].float(), atol=1e-5), la
    assert float(got[0][0, 0, 0, :6].sum()) < 1e-6  # the sliding window (5) hides keys 0..5 from query 10
    assert float(got[3][0, 0, 0, :6].sum()) > 1e-3  # the global layer sees them


# ---- the run stage end to end on a tiny model (the target's tokenizer; skipped where it is not cached) ----------------


def tiny_target(tok):
    """A tiny random Qwen3.5 hybrid with the 9B's 32-block pattern and the tokenizer's vocabulary, as a Model."""
    from transformers import Qwen3_5TextConfig
    from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM

    from bridge_jspace.model import Model

    cfg = Qwen3_5TextConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=48, num_hidden_layers=32,
                            layer_types=QWEN9B, num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                            linear_num_key_heads=2, linear_num_value_heads=4, linear_key_head_dim=8,
                            linear_value_head_dim=6, linear_conv_kernel_dim=4, max_position_embeddings=256)  # fmt: skip
    cfg._attn_implementation = "sdpa"
    torch.manual_seed(0)
    hf = Qwen3_5ForCausalLM(cfg).eval()
    return Model(hf, tok, [], frozenset(), torch.zeros(1, dtype=torch.bool))


@pytest.mark.parametrize(("part", "with_c"), [("b", False), ("a", False), ("b", True)])
def test_run_end_to_end_on_a_tiny_model(tok, tmp_path, monkeypatch, part, with_c):
    """stage_run's glue on CPU: the 9B's layer pattern and L12, three items, every arm's rows, the edge counts and the
    attention array in the files the verdict, view and figure read; then those stages read them. (c) only with the
    flag (dropped by Dan; the default run writes no part-c row)."""
    import bridge_jspace.model as BM
    from scripts import x0_massmean as MM
    from scripts import x6_routes as R

    model = tiny_target(tok)
    g = torch.Generator().manual_seed(1)
    alf = torch.linalg.qr(torch.randn(32, 4, generator=g))[0].numpy()
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E.pins, "TARGET", "qwen3.5-9b")
    monkeypatch.setattr(E.pins, "check_run_name", lambda name: None)
    monkeypatch.setattr(E, "config_kinds_of", lambda target: QWEN9B)
    monkeypatch.setattr(BM, "load_model", lambda: model)
    monkeypatch.setattr(R, "N_GEN", 6)
    monkeypatch.setattr(R, "N_ITEMS", 3)
    monkeypatch.setattr(MM, "subspaces", lambda run: ({"Alf": alf}, {}))
    monkeypatch.setattr(MM, "pointer_means", lambda run: {k: torch.randn(32, generator=g).numpy() for k in range(5)})
    digits = torch.tensor(X.digit_ids(tok))
    monkeypatch.setattr(
        E, "eligible", lambda model, cases, out, n: (cases[:n], {"pass": True, "eligible": len(cases)}, digits)
    )
    name = f"qwen35_9b_x47_6_{part}"
    out = E.stage_run(part, name, "test", with_c)
    m = json.loads((out / "manifest.json").read_text())
    assert m["items"] == 3
    assert m["layer"] == 12
    rows = X.read_jsonl(out / "outcomes.jsonl")
    cases = X.read_jsonl(out / "cases.jsonl")
    assert len(cases) == 3
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "x")
    decode = lambda ids: tok.decode(ids, skip_special_tokens=False)  # noqa: E731
    view = (E.stage_view(name, decode=decode) / "view.md").read_text()
    assert "⟦patch: " in view
    if part == "b":
        assert (out / "check.json").exists()
        assert m["with_c"] == with_c
        n_c = 5 if with_c else 0  # (c): none and 4 dereference arms per reader, with the flag only
        assert len(rows) == 3 * 2 * (10 + n_c)  # per reader: unedited, none, 8 formation arms
        assert {r["arm"] for r in rows if r["part"] == "c"} == (
            {"none", "block/all", "control/all", "block/attn", "control/attn"} if with_c else set()
        )
        e = cases[0]["edges"]
        assert e["b"]["block/sentence/all"]["edges"] == e["b"]["control/sentence/all"]["edges"] == 1755
        assert ("c" in e) == with_c
        assert ("c" in m["arms"]) == with_c
        if with_c:
            assert e["c"]["lookup"]["block/all"]["edges"] == 27 * len(cases[0]["spans"]["question"][LK]) * 20
        res = E.b_result(name, 50)
        assert res["status"] == "tested"
        assert "dereference" not in res
        assert (res["c"] is not None) == with_c
        assert set(res["formation"]["clauses"]) == {"position_fell", "identity_within", "recall_within",
                                                     "control_position_within", "control_identity_within",
                                                     "control_recall_within"}  # fmt: skip
        assert res["edges_same_every_item"]
        norms = X.read_jsonl(out / "norms.jsonl")
        assert norms[0]["none"]["cos_none"] == pytest.approx(1.0, abs=1e-4)
        assert "⟦filler: " in view
    else:
        assert len(rows) == 3 * len(E.A_ARMS)
        att = np.load(out / "attention.npz")
        assert att["masses"].shape == (3, len(E.A_ARMS), 8, 4, 3)
        assert list(att["layers"]) == [3, 7, 11, 15, 19, 23, 27, 31]
        assert float(att["masses"].astype(np.float32).sum(-1).max()) <= 1.0 + 1e-2  # masses on three sentences
        a = E.a_result(name, 50)
        assert a["status"] == "tested"
        assert {r["k"] for r in rows if r["arm"] in ("write1", "rand1")} <= {0, 1, 2}
        assert (E.stage_figures(name) / "attention_follow.png").exists()


# ---- the rules on planted rows ---------------------------------------------------------------------------------------


def b_rows(n: int, block: dict, control: dict | None = None) -> list[dict]:
    """(b) rows: none half position, half identity, recall switches 0.9; the block / control rows by the given shares
    of position and identity (the rest original) and recall switch."""
    control = control or {"position": 0.5, "identity": 0.5, "recall": 0.9}
    spec = {"unedited": {"position": 0, "identity": 0, "recall": 0}, "none": {"position": 0.5, "identity": 0.5, "recall": 0.9},
            E.DECISIVE_B: block, E.CONTROL_B: control}  # fmt: skip
    rows = []
    for i in range(n):
        for arm, sh in spec.items():
            u = (i + 0.5) / n
            route = (
                "position" if u < sh["position"] else "identity" if u < sh["position"] + sh["identity"] else "original"
            )
            base = {"part": "b", "scene": f"s{i}", "entity": f"e{i % 25}", "arm": arm}
            rows.append({**base, "reader": LK, "route": route, "switched": int(route != "original"), "right": 0})
            rows.append({**base, "reader": RC, "route": None, "switched": int(u < sh["recall"]), "right": 0})
    return rows


def c_rows(n: int, lookup: float, recall: float) -> list[dict]:
    """(c) rows of a --with-c run (dropped from the rule; the verdict shows them descriptively)."""
    rows = []
    block, control = E.C_ARMS
    for i in range(n):
        u = (i + 0.5) / n
        for arm, (a_lk, a_rc) in {"none": (1, 1), block: (lookup, recall), control: (1, 1)}.items():
            base = {"part": "c", "scene": f"s{i}", "entity": f"e{i % 25}", "arm": arm, "switched": 0, "route": None}
            rows.append({**base, "reader": LK, "right": int(u < a_lk)})
            rows.append({**base, "reader": RC, "right": int(u < a_rc)})
    return rows


def rule_b(rows):
    return E.formation(
        E.table(rows, "b", LK, E.ROUTE_KEYS, 200), E.table(rows, "b", RC, {"switched": lambda r: r["switched"]}, 200)
    )


def test_formation_holds_when_position_falls_and_the_rest_stays():
    f = rule_b(b_rows(100, {"position": 0.0, "identity": 0.5, "recall": 0.9}))
    assert f["holds"]
    assert all(f["clauses"].values())


def test_formation_bars_are_inclusive():
    f = rule_b(b_rows(100, {"position": 0.10, "identity": 0.40, "recall": 0.80}))
    assert f["holds"], f["clauses"]  # 0.10 exactly; identity and recall exactly 0.10 away


@pytest.mark.parametrize(
    ("block", "control", "fails"),
    [
        ({"position": 0.12, "identity": 0.5, "recall": 0.9}, None, "position_fell"),
        ({"position": 0.0, "identity": 0.62, "recall": 0.9}, None, "identity_within"),  # a rise counts too
        ({"position": 0.0, "identity": 0.38, "recall": 0.9}, None, "identity_within"),
        ({"position": 0.0, "identity": 0.5, "recall": 0.78}, None, "recall_within"),
        ({"position": 0.0, "identity": 0.5, "recall": 0.9}, {"position": 0.38, "identity": 0.5, "recall": 0.9},
         "control_position_within"),
        ({"position": 0.0, "identity": 0.5, "recall": 0.9}, {"position": 0.5, "identity": 0.5, "recall": 0.7},
         "control_recall_within"),
    ],
)  # fmt: skip
def test_formation_fails_on_each_clause(block, control, fails):
    f = rule_b(b_rows(100, block, control))
    assert not f["holds"]
    assert [k for k, v in f["clauses"].items() if not v] == [fails]


def test_table_refuses_a_missing_arm():
    rows = [
        r
        for r in b_rows(20, {"position": 0, "identity": 0.5, "recall": 0.9})
        if not (r["scene"] == "s3" and r["arm"] == "none")
    ]
    with pytest.raises(AssertionError, match="missing"):
        E.table(rows, "b", LK, E.ROUTE_KEYS, 50)


# ---- the seal and the CPU stages on fake runs -------------------------------------------------------------------------


PRED = """**Q47.5** (47.5) ...

Dan: followed (80%)

**Q47.6** (47.6 b, c) Is the pointer formed ...

Answer per model: Muse; 9B (formation). Rule: jobs/c3/batch47.yaml, 47.6.

Dan:{answer}
"""


def test_answer_is_read_from_q47_6_only():
    assert E.answer_in(PRED.format(answer="")) == ""
    assert E.answer_in(PRED.format(answer=" Muse: formation yes (60%)")) == "Muse: formation yes (60%)"
    assert E.answer_in("no such block") == ""


def test_dan_answer_at_this_head_is_a_string():
    assert isinstance(E.dan_answer(), str)


@pytest.mark.parametrize("stage", ["verdict", "view", "figures"])
def test_cpu_stages_refuse_until_the_answer(monkeypatch, stage):
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "")
    call = {
        "verdict": lambda: E.stage_verdict(),
        "view": lambda: E.stage_view("x"),
        "figures": lambda: E.stage_figures("x"),
    }
    with pytest.raises(AssertionError, match="sealed"):
        call[stage]()


def write_b(root, run, target, rows, layer):
    """A fake part-b run; (c) edge counts recorded iff the rows hold part-c rows (a --with-c run)."""
    with_c = any(r["part"] == "c" for r in rows)
    d = root / run
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": layer, "part": "b"}))
    X.write_jsonl(d / "outcomes.jsonl", rows)
    arms = ("none", E.DECISIVE_B, E.CONTROL_B)
    X.write_jsonl(d / "norms.jsonl", [{"scene": f"s{i}", **{a: {"norm": 1.0, "share_U": 0.1, "cos_none": 1.0} for a in arms}}
                                      for i in range(5)])  # fmt: skip
    p = positions()
    kinds = [FULL] * 52
    sets = E.layer_sets(kinds, layer)
    edges: dict = {"b": E.edge_table(E.formation_arms(p, sets, kinds))}
    if with_c:
        edges["c"] = {E.READER_NAME[w]: E.edge_table(E.dereference_arms(p, sets, kinds, w)) for w in X.READERS}
    X.write_jsonl(d / "cases.jsonl", [{"scene": f"s{i}", "edges": edges} for i in range(3)])


def test_verdict_on_fake_runs(tmp_path, monkeypatch):
    """Formation is the only rule; a --with-c run's (c) rows show as a descriptive table and decide nothing."""
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "Muse: formation no (60%)")
    good_b = b_rows(60, {"position": 0.0, "identity": 0.5, "recall": 0.9})
    bad_b = b_rows(60, {"position": 0.3, "identity": 0.5, "recall": 0.9})
    write_b(tmp_path, "muse30_x47_6_b", "muse-glimmer-30b", good_b + c_rows(60, 0.3, 0.95), 26)
    write_b(tmp_path, "qwen35_9b_x47_6_b", "qwen3.5-9b", bad_b, 12)
    fake_a_run(tmp_path)  # the 9B's (a) run; Muse's is pending
    out = E.stage_verdict(n_boot=100)
    blob = json.loads((out / "verdict.json").read_text())
    v = blob["verdict"]
    assert list(v) == ["formation"]
    assert not v["formation"]["holds"]
    assert v["formation"]["held_on"] == ["muse-glimmer-30b"]
    assert blob["b"]["muse-glimmer-30b"]["c"] is not None
    assert blob["b"]["qwen3.5-9b"]["c"] is None
    md = (out / "verdict.md").read_text()
    assert "Muse: formation no" in md
    assert "Dereference" not in md
    assert md.count("(c) accuracy per arm") == 1  # Muse's --with-c rows, descriptive
    assert "| block/all | 0.30 [" in md
    assert blob["a"]["qwen3.5-9b"]["status"] == "tested"
    assert blob["a"]["muse-glimmer-30b"]["status"] == "pending"
    assert "| 7 | 0 | " in md  # (a): the planted head leads the table


def test_verdict_counts_a_missed_gate_as_not_tested(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "x")
    good = b_rows(40, {"position": 0.0, "identity": 0.5, "recall": 0.9})
    write_b(tmp_path, "muse30_x47_6_b", "muse-glimmer-30b", good, 26)
    d = tmp_path / "qwen35_9b_x47_6_b"
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layer": 12, "not_tested": "gate"}))
    v = json.loads((E.stage_verdict(n_boot=50) / "verdict.json").read_text())["verdict"]
    assert v["formation"]["held_on"] == ["muse-glimmer-30b"]
    assert not v["formation"]["holds"]
    assert v["formation"]["not_tested_or_pending"] == ["qwen3.5-9b"]


def fake_a_run(root, n: int = 30, layers=(3, 7, 11)) -> str:
    """An (a) run where head 0 of the second layer always looks most at the answered locker and every other head at
    slot 0."""
    run = "qwen35_9b_x47_6_a"
    d = root / run
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layer": 12, "part": "a"}))
    rng = np.random.default_rng(0)
    masses = np.zeros((n, len(E.A_ARMS), len(layers), 4, 3), dtype=np.float16)
    rows = []
    for i in range(n):
        for ai, arm in enumerate(E.A_ARMS):
            slot = 0 if arm == "none" else int(rng.integers(0, 3))
            masses[i, ai, :, :, 0] = 0.5
            masses[i, ai, 1, 0] = 0.0
            masses[i, ai, 1, 0, slot] = 0.9
            route = "original" if slot == 0 else "position"
            rows.append({"part": "a", "scene": f"s{i}", "entity": f"e{i % 10}", "reader": LK, "arm": arm, "route": route,
                         "slot": slot, "j": 0, "switched": 0, "right": 0, "top": 5})  # fmt: skip
    X.write_jsonl(d / "outcomes.jsonl", rows)
    np.savez_compressed(d / "attention.npz", masses=masses, scenes=np.array([f"s{i}" for i in range(n)]),
                        arms=np.array(E.A_ARMS), layers=np.array(layers))  # fmt: skip
    return run


def test_a_result_finds_the_following_head_and_the_figure_is_written(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "x")
    run = fake_a_run(tmp_path)
    a = E.a_result(run, 50)
    top = a["top_heads_moved_whole"][0]
    assert (top["layer"], top["head"]) == (7, 0)
    assert top["whole"] == 1.0
    assert a["follow"]["none"][0][1] == 1.0  # under none every answer is slot 0, where every head looks most
    out = E.stage_figures(run)
    assert (out / "attention_follow.png").stat().st_size > 10_000
    blob = json.loads((out / "attention_follow.json").read_text())
    assert blob["best_head_rate"]["whole"][1] == 1.0


def test_view_marks_every_span_and_lists_every_arm(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "RESULTS", tmp_path)
    monkeypatch.setattr(E, "dan_answer", lambda rev="HEAD": "x")
    d = tmp_path / "muse30_x47_6_b"
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({"model": {"target": "muse-glimmer-30b"}, "layer": 26, "part": "b"}))
    p = positions()
    readers = {w: {"question": "q?", "answer": "8", "cf_answer": "7", "ids": {"org": list(range(105 if w == LK else 106)), "alt": []}}
               for w in X.READERS}  # fmt: skip
    case = {"scene": "s0", "bridge": "frog", "cf_bridge": "owl", "expect": {"identity": 7}, "space": [1], "spans": p,
            "readers": readers, "edges": {"b": {"block/sentence/all": {"edges": 3645}}}}  # fmt: skip
    X.write_jsonl(d / "cases.jsonl", [case])
    rows = [{"part": "b", "scene": "s0", "reader": w, "arm": a, "top": 3, "route": "identity" if w == LK else None,
             "slot": 1, "switched": 1, "right": 0} for w in X.READERS for a in ("none", E.DECISIVE_B)]  # fmt: skip
    X.write_jsonl(d / "outcomes.jsonl", rows)
    out = E.stage_view("muse30_x47_6_b", decode=lambda ids: " ".join(str(i) for i in ids))
    text = (out / "view.md").read_text()
    for mark in ("⟦filler: ", "⟦src-locker3: ", "⟦dst-b: ", "⟦patch: ", "⟦dst-c: "):
        assert mark in text
    assert text.count(f"| b | {E.DECISIVE_B} |") == 2
    assert "(b) block/sentence/all 3645" in text
