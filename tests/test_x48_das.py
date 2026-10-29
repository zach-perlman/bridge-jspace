"""Batch 48, test 48.1 and batch 47's D3 (scripts/x48_das.py): the DAS intervention and its orthonormal R, the split by
entity, the read-outs on planted vectors, the rules on planted numbers, the sealed verdicts, and the run / verdict /
depth stages end to end on a tiny fake causal model whose blocks are torch modules (so the training path's hooks are the
real ones). CPU, no real model."""

from __future__ import annotations

import json
import os
import re
from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x48_das as D

D_MODEL, VOCAB, N_LETTERS = 64, 256, 128


class WordTok:
    """Words with their leading whitespace as tokens, ids from a shared vocab (as tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}
        self.pad_token_id, self.eos_token_id = 0, 0
        self.vocab["<pad>"] = 0

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


class Block(torch.nn.Module):
    """Mixes the running mean of the positions so far into every position (causal), scaled by a parameter."""

    def __init__(self) -> None:
        super().__init__()
        self.w = torch.nn.Parameter(torch.tensor(1.0))

    def forward(self, h):
        return h + 0.1 * self.w * torch.cumsum(h, 1) / torch.arange(1, h.shape[1] + 1, device=h.device)[None, :, None]


class FakeHF(torch.nn.Module):
    def __init__(self, n_layers: int, d: int, vocab: int) -> None:
        super().__init__()
        g = torch.Generator().manual_seed(0)
        self.emb = torch.nn.Embedding(vocab, d)
        self.emb.weight.data = torch.randn(vocab, d, generator=g)
        self.unemb = torch.nn.Parameter(torch.randn(vocab, d, generator=g))
        self.blocks = torch.nn.ModuleList([Block() for _ in range(n_layers)])

    def get_input_embeddings(self):
        return self.emb

    def forward(self, input_ids=None, attention_mask=None, use_cache=False, **_):
        h = self.emb(input_ids)
        for b in self.blocks:
            h = b(h)
        return SimpleNamespace(logits=h @ self.unemb.T)


class FakeModel:
    """A stand-in for bridge_jspace.model.Model: hf (a torch module whose blocks are `layers`), run with edits and
    recording, generate_batch (first logits under per-row edit sets)."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = D_MODEL, vocab: int = VOCAB):
        self.hf = FakeHF(n_layers, d, vocab)
        self.tokenizer, self.n_layers = tok, n_layers
        self.device = torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

    @property
    def layers(self):
        return self.hf.blocks

    def forward(self, ids: list[int], edits: dict):
        with torch.no_grad():
            h = self.hf.emb(torch.as_tensor(ids))[None]
            states = {}
            for layer, b in enumerate(self.hf.blocks):
                h = b(h)
                if layer in edits:
                    h = edits[layer](h[0].float())[None]
                states[layer] = h[0].clone()
            return (h[0, -1] @ self.hf.unemb.T), states

    def run(self, ids, edits=None, record=()):
        logits, states = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: states[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return torch.arange(1, N_LETTERS + 1)


class FakeLens:
    def __init__(self, model, name):
        assert name == "jpp"

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), D_MODEL, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


# ---- the intervention, R, the split ---------------------------------------------------------------------------------


def test_intervention_formula_projects_the_change():
    g = torch.Generator().manual_seed(1)
    h_o, h_s = torch.randn(3, 8, generator=g), torch.randn(3, 8, generator=g)
    r = D.random_basis(8, 2, 0)
    out = D.intervene(h_o, h_s - h_o, r)
    assert torch.allclose(out, h_o + ((h_s - h_o) @ r) @ r.T)
    full = D.random_basis(8, 8, 0)  # the whole space: the intervention is S's state
    assert torch.allclose(D.intervene(h_o, h_s - h_o, full), h_s, atol=1e-5)
    assert torch.allclose(D.intervene(h_o, h_s - h_o, torch.zeros(8, 0)), h_o)


def test_subspace_module_keeps_orthonormal_columns_under_training():
    mod = D.subspace_module(16, 4, seed=3)
    w: Any = mod.weight
    assert w.shape == (16, 4) and torch.allclose(w.T @ w, torch.eye(4), atol=1e-5)
    opt = torch.optim.Adam(mod.parameters(), lr=1e-2)
    for _ in range(5):
        opt.zero_grad()
        w = mod.weight
        (w.sum() ** 2).backward()
        opt.step()
    w = mod.weight
    assert torch.allclose(w.T @ w, torch.eye(4), atol=1e-5)
    a: Any = D.subspace_module(16, 4, seed=3).weight
    b: Any = D.subspace_module(16, 4, seed=3).weight
    assert torch.allclose(a, b)


def test_random_basis_is_orthonormal_and_seeded():
    r = D.random_basis(32, 5, 7)
    assert torch.allclose(r.T @ r, torch.eye(5), atol=1e-5)
    assert torch.allclose(r, D.random_basis(32, 5, 7)) and not torch.allclose(r, D.random_basis(32, 5, 8))


def test_split_by_entity_60_20_20_seeded():
    ents = [f"e{i % 10}" for i in range(40)]
    s = D.split_entities(ents, seed=0)
    assert set(s) == {f"e{i}" for i in range(10)}
    assert sorted(s.values()).count("train") == 6 and sorted(s.values()).count("select") == 2
    assert s == D.split_entities(ents, seed=0) and s != D.split_entities(ents, seed=1)
    small = D.split_entities(["a", "b", "c"], seed=0)
    assert sorted(small.values()) == ["select", "test", "train"]


# ---- read-outs on planted vectors --------------------------------------------------------------------------------


def test_geometry_on_planted_vectors():
    d = 64
    eye = torch.eye(d)
    jdic, wdic = eye, eye  # atoms = the standard basis
    atoms_j = torch.arange(100) % d  # the first 25: e_0..e_24
    atoms_w = torch.arange(25) + 30  # e_30..e_54
    u = eye[:, 60:64]  # U = span(e_60..e_63), rank 4
    u_fit = eye[:, 58:62]
    spans = D.spans_of(jdic, wdic, u, u_fit, atoms_j, atoms_w)
    delta = eye[0] + eye[1] + eye[60] + eye[40]  # inside J++-25, inside U, inside W_E-25; norm^2 = 4
    g = D.geometry_row(delta, eye[:, :2], spans)  # R = span(e_0, e_1)
    assert g["energy"] == pytest.approx(0.5) and g["in_jpp25"] == pytest.approx(1.0) and g["in_U"] == pytest.approx(0.0)
    assert g["in_jpp100"] == pytest.approx(1.0) and g["in_we25"] == pytest.approx(0.0)
    assert g["outside_union"] == pytest.approx(0.0)
    g = D.geometry_row(delta, eye[:, 60:61], spans)  # R = e_60: the address
    assert (
        g["energy"] == pytest.approx(0.25) and g["in_U"] == pytest.approx(1.0) and g["in_jpp25"] == pytest.approx(0.0)
    )
    assert g["in_Ufit"] == pytest.approx(1.0) and g["outside_union"] == pytest.approx(0.0)
    delta2 = delta + eye[57]  # a third code outside every part
    g = D.geometry_row(delta2, eye[:, 57:58], spans)
    assert g["outside_union"] == pytest.approx(1.0) and g["in_Ufit"] == pytest.approx(0.0)
    assert D.geometry_row(torch.zeros(d), eye[:, :2], spans)["energy"] is None
    from scripts.x6_routes import mean_cos2

    assert mean_cos2(eye[:, 60:62], u) == pytest.approx(0.5)  # ||R^T U||_F^2 / rank U
    assert mean_cos2(eye[:, :4], u) == pytest.approx(0.0)


def test_principal_angles():
    eye = torch.eye(8)
    assert D.principal_angles(eye[:, :2], eye[:, :2]) == [0.0, 0.0]
    assert D.principal_angles(eye[:, :2], eye[:, 2:4]) == [90.0, 90.0]
    assert D.principal_angles(eye[:, :2], eye[:, 1:3]) == [0.0, 90.0]


def test_fit_pointer_rank_is_classes_minus_one():
    g = torch.Generator().manual_seed(0)
    h = torch.randn(30, 16, generator=g).numpy()
    u = D.fit_pointer(h, [i % 4 for i in range(30)])
    assert u.shape == (16, 3) and np.allclose(u.T @ u, np.eye(3), atol=1e-8)
    with pytest.raises(AssertionError):
        D.fit_pointer(h, [1] * 30)


# ---- the rules on planted numbers --------------------------------------------------------------------------------


def test_chosen_k_smallest_k_at_or_above_0_7_else_best():
    assert D.chosen_k({1: 0.2, 4: 0.7, 16: 0.9, 64: 0.95}) == 4
    assert D.chosen_k({1: 0.75, 4: 0.7, 16: 0.9, 64: 0.95}) == 1
    assert D.chosen_k({1: 0.2, 4: 0.3, 16: 0.6, 64: 0.95}) == 64  # none at 0.7 below 16: the best
    assert D.chosen_k({1: 0.2, 4: 0.65, 16: 0.65, 64: 0.5}) == 4  # a tie: the smaller k
    assert D.chosen_k({1: 0.2, 4: 0.3, 16: 0.3, 64: 0.8}) == 64  # k = 64 is never "some k <= 16"


def planted(lookup: dict, recall: dict, geometry: dict, routes_identity: float = 0.5, k64: float = 0.9) -> dict:
    """A model's numbers as model_numbers writes them, from the quantities the rules read."""

    def reader(spec: dict, k: int) -> dict:
        return {"k": k, "select": {}, "test": {"own_at_k": [spec["own"], spec["own"] - 0.1, spec["own"] + 0.1],
                                             "cross_iia": [spec["cross"], 0, 0],
                                             "own_minus_cross": [spec["own"] - spec["cross"], spec.get("lo", 0.1), 1],
                                             "own_at_k64": [k64, 0, 1]}}  # fmt: skip

    geo = {}
    for key, g in geometry.items():
        geo[key] = {"in_jpp25": [g.get("jpp", 0.0), 0, 1], "outside_union": [g.get("out", 0.0), 0, 1],
                    "cos2_U": g.get("cos2", 0.0), "energy": [g.get("energy", 0.3), 0, 1]}  # fmt: skip
    k_l, k_r = lookup.get("k", 4), recall.get("k", 4)
    return {"readers": {X.LOOKUP: reader(lookup, k_l), X.RECALL: reader(recall, k_r)}, "geometry": geo,
            "routes": {f"R_{X.LOOKUP}_k{k_l}": {"identity": [routes_identity, 0, 1]}}}  # fmt: skip


GEO = {"R_PP_k4": {"jpp": 0.1, "out": 0.6, "cos2": 0.6}, "R_PM_k4": {"jpp": 0.7, "out": 0.1, "cos2": 0.01},
       "rand_k4": {"jpp": 0.05, "out": 0.9, "cos2": 0.001}}  # fmt: skip


def test_rules_all_four_hold_on_planted_numbers():
    v = D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, GEO))
    assert v["a"] and v["b"] and v["c"] and v["d"] and not v["fallback_no_low_dimensional_mediator"]
    assert v["not_selective"] == {}


def test_rule_a_needs_both_readers_low_cross_and_a_paired_ci_above_zero():
    assert not D.rules(planted({"own": 0.8, "cross": 0.3}, {"own": 0.75, "cross": 0.2}, GEO))["a"]
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.6, "cross": 0.2}, GEO))["a"]
    assert not D.rules(planted({"own": 0.8, "cross": 0.1, "lo": -0.05}, {"own": 0.75, "cross": 0.2}, GEO))["a"]
    big = {**GEO, "R_PP_k64": GEO["R_PP_k4"], "rand_k64": GEO["rand_k4"]}
    v = D.rules(planted({"own": 0.8, "cross": 0.1, "k": 64}, {"own": 0.75, "cross": 0.2}, big))
    assert not v["a"] and v["detail"]["own_ok"]["lookup"] is False  # k = 64 is not "some k <= 16"
    v = D.rules(planted({"own": 0.7, "cross": 0.25}, {"own": 0.7, "cross": 0.25}, GEO))
    assert v["a"]  # the bars are inclusive


def test_rules_b_c_d_and_the_fallback():
    g = {**GEO, "R_PM_k4": {"jpp": 0.4, "out": 0.1}}
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))["b"]
    g = {**GEO, "rand_k4": {"jpp": 0.2}}
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))["b"]
    g = {**GEO, "R_PP_k4": {"jpp": 0.3, "out": 0.6, "cos2": 0.6}}
    v = D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))
    assert not v["b"] and v["c"] and v["d"]
    g = {**GEO, "R_PP_k4": {"jpp": 0.1, "out": 0.6, "cos2": 0.4}}
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))["c"]
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, GEO, routes_identity=0.2))["d"]
    g = {**GEO, "R_PP_k4": {"jpp": 0.1, "out": 0.4, "cos2": 0.6}}
    assert not D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))["d"]
    assert not D.rules(planted({"own": 0.6, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, GEO))["d"]
    v = D.rules(planted({"own": 0.3, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, GEO, k64=0.45))
    assert v["fallback_no_low_dimensional_mediator"] and not v["a"]
    g = {**GEO, "R_PP_k4": {**GEO["R_PP_k4"], "energy": 0.85}}
    assert D.rules(planted({"own": 0.8, "cross": 0.1}, {"own": 0.75, "cross": 0.2}, g))["not_selective"] == {
        "R_PP_k4": True
    }


def planted_layer(lookup: tuple[float, float], recall: tuple[float, float]) -> dict:
    """(energy inside J++-25, own-IIA) per reader at one layer, as layer_numbers writes them (k = 4)."""
    return {"readers": {w: {"k": 4, "test": {"own_at_k": [iia, 0, 1]}} for w, (_, iia) in
                        ((X.LOOKUP, lookup), (X.RECALL, recall))},
            "geometry": {f"R_{w}_k4": {"in_jpp25": [e, 0, 1]} for w, (e, _) in ((X.LOOKUP, lookup), (X.RECALL, recall))}}  # fmt: skip


def test_rules_d3_on_planted_numbers():
    by = {
        6: planted_layer((0.5, 0.7), (0.6, 0.8)),
        12: planted_layer((0.15, 0.7), (0.5, 0.8)),
        24: planted_layer((0.1, 0.3), (0.3, 0.4)),
    }
    v = D.rules_d3(by, 12)
    assert v["leaves_the_lens"] and v["recall_stays"] and v["recall_tested_layers"] == [6, 12]
    by[12] = planted_layer((0.25, 0.7), (0.5, 0.8))
    assert not D.rules_d3(by, 12)["leaves_the_lens"]
    by[12] = planted_layer((0.15, 0.5), (0.5, 0.8))  # IIA below 0.6 at L: not "while own-IIA stays >= 0.6"
    assert not D.rules_d3(by, 12)["leaves_the_lens"]
    by[12] = planted_layer((0.15, 0.7), (0.3, 0.8))  # the recall's share drops where its IIA is high
    assert not D.rules_d3(by, 12)["recall_stays"]
    v = D.rules_d3({12: planted_layer((0.15, 0.7), (0.5, 0.8))}, 12)
    assert not v["leaves_tested"] and not v["leaves_the_lens"]
    v = D.rules_d3({6: planted_layer((0.5, 0.7), (0.6, 0.5)), 12: planted_layer((0.15, 0.7), (0.5, 0.5))}, 12)
    assert not v["recall_stays"] and v["recall_tested_layers"] == []


def test_dan_answer_reads_the_blocks(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.8** x\n\nDan: a\n\n**Q-depth** (amendment 3)\n- D3 ...\n\nDan:{}\n\n**Q48.1** (48.1)\n\nRule: ...\n\nDan:{}\n"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("", "")))
    assert D.dan_answer() == "" and D.dan_answer(D.QUESTION_DEPTH) == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" yes · 60%", " (a) yes 70%")))
    assert D.dan_answer() == "(a) yes 70%" and D.dan_answer(D.QUESTION_DEPTH) == "yes · 60%"


# ---- the training forward on the fake model ----------------------------------------------------------------------


def test_batch_logits_matches_the_single_prompt_edit_and_carries_gradient():
    from scripts.exp04_brew_parts import AddRows

    tok = WordTok()
    fake = FakeModel(tok, n_layers=6)
    rows = [tok("a b c d e").input_ids, tok("f g h").input_ids]  # two lengths: the second is padded
    adds = torch.randn(2, D_MODEL, requires_grad=True)
    logits = D.batch_logits(fake, 2, rows, [1, 0], adds)
    for i, (ids, pos) in enumerate(zip(rows, [1, 0], strict=True)):
        ref, _ = fake.run(torch.tensor([ids]), edits={2: AddRows(adds[i : i + 1].detach(), [pos])})
        assert torch.allclose(logits[i], ref, atol=1e-4), f"row {i}"
    logits.sum().backward()
    assert adds.grad is not None and adds.grad.abs().sum() > 0


def test_train_subspace_lowers_the_loss_and_keeps_r_orthonormal():
    tok = WordTok()
    fake = FakeModel(tok, n_layers=6)
    g = torch.Generator().manual_seed(0)
    rows = [{"ids": tok(f"w{i} x y z").input_ids, "pos": 0, "delta": torch.randn(D_MODEL, generator=g) * 5, "target": 7}
            for i in range(6)]  # fmt: skip
    log: list[dict] = []
    r = D.train_subspace(fake, 2, rows, k=3, seed=0, steps=12, batch=4, micro=2, log=log)
    assert r.shape == (D_MODEL, 3) and torch.allclose(r.T @ r, torch.eye(3), atol=1e-4)
    assert log[0]["step"] == 0 and log[-1]["step"] == 11 and log[-1]["loss"] < log[0]["loss"]


# ---- the run, verdict and depth stages on the fake model ---------------------------------------------------------


def make_pairs(tok: WordTok, n: int = 30) -> tuple[list[dict], dict]:
    """n planted pairs: distinct O / S prompts (the bridge at index 3), both readers reading a different question after
    the bridge, 10 entities; every pair in the lookup's set, every third one not in the recall's."""
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    pairs = []
    for i in range(n):
        ctx_o, ctx_s = (
            f"The locker of w{i} is {i % 9 + 1}. Iris picked w{i}.",
            f"The locker of w{i} is {i % 9 + 1}. Iris picked v{i}.",
        )
        readers = {}
        for w, q in ((X.LOOKUP, "Which locker?"), (X.RECALL, "How many legs?")):
            o, s = tok(f"{ctx_o} {q} Answer:", return_offsets_mapping=True), tok(f"{ctx_s} {q} Answer:")
            readers[w] = {"id": f"{w}-{i}", "question": q, "answer": "5", "cf_answer": str((i % 8) + 1),
                          "tok_A": digit["5"], "tok_b": digit[str((i % 8) + 1)], "ids": {"org": o.input_ids, "alt": s.input_ids},
                          "text": {"org": f"{ctx_o} {q} Answer:"}}  # fmt: skip
        pos = 8  # "The locker of w{i} is n. Iris picked w{i}.": the bridge token is the 9th word
        mark = list(tok(f"{ctx_o} Which locker? Answer:", return_offsets_mapping=True).offset_mapping[pos])
        pairs.append({"scene": f"s{i:03d}", "entity": f"e{i % 10}", "cf_bridge": f"v{i}", "domain": "animals", "upstream": False,
                      "pos": pos, "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ", "context": ctx_o,
                      "cf_context": ctx_s, "stored_whole": {X.LOOKUP: 1, X.RECALL: int(i % 3 != 0)}, "bridge_mark": mark,
                      "locker_index": i % 3, "read_index": {w: len(readers[w]["ids"]["org"]) for w in X.READERS},
                      "readers": readers})  # fmt: skip
    split = D.split_entities([p["entity"] for p in pairs])
    for p in pairs:
        p["split"] = split[p["entity"]]
    per = {D.READER_NAME[w]: {s: sum(p["split"] == s and p["stored_whole"][w] for p in pairs) for s in ("train", "select", "test")}
           for w in X.READERS}  # fmt: skip
    info = {"main_run": "fake", "layer": 32, "scenes_at_L": n, "dropped": {}, "pairs": n, "entities": 10,
            "entities_per_split": {}, "pairs_per_reader_and_split": per, "split_seed": 0,
            "scene_ids": {s: [p["scene"] for p in pairs if p["split"] == s] for s in ("train", "select", "test")}}  # fmt: skip
    return pairs, info


def make_routes(tok: WordTok, n: int = 4) -> list[dict]:
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    out = []
    for i in range(n):
        o, s = (
            f"The locker of the frog is 1. Iris picked the frog{i}.",
            f"The locker of the frog is 1. Iris picked the bee{i}.",
        )
        readers = {w: {"question": q, "answer": "1", "cf_answer": "2", "tok_A": digit["1"], "tok_b": digit["2"],
                       "ids": {"org": tok(f"{o} {q} Answer:").input_ids, "alt": tok(f"{s} {q} Answer:").input_ids}}
                   for w, q in ((X.LOOKUP, "Which locker?"), (X.RECALL, "How many legs?"))}  # fmt: skip
        out.append({"scene": f"C2-{i}", "condition": "C2", "rendering": "chat", "domain": "animals", "bridge": "frog",
                    "cf_bridge": "bee", "context": o, "cf_context": s, "pos": 10, "space": [tok.vocab[" "]],
                    "expect": {"identity": 2, "position": 3, "value": 4, "original": 1},
                    "route_tokens": {"identity": digit["2"], "position": digit["3"], "value": digit["4"], "original": digit["1"]},
                    "readers": readers})  # fmt: skip
    return out


@pytest.fixture
def fake_env(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    pairs, info = make_pairs(tok)
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(D, "select_pairs", lambda *_: (pairs, info))
    u = D.random_basis(D_MODEL, 4, 11).numpy()
    monkeypatch.setattr(D, "pointer_basis", lambda _t: (u, {"states_run": "fake", "rank": 4}))
    monkeypatch.setattr(D, "routes_scenes", lambda *_a, **_k: (make_routes(tok), {"used": 4}))
    monkeypatch.setattr(D, "K_JPP", (25, 30))
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x48_das")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(D, "SPEC", tmp_path / "batch48.yaml")
    monkeypatch.setattr(D, "SPEC_47", tmp_path / "batch47.yaml")
    D.SPEC.write_text("")
    D.SPEC_47.write_text("")
    src = tmp_path / "x0" / D.MAIN_RUN[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "gate.json"):
        (src / f).write_text("")
    return SimpleNamespace(tok=tok, pairs=pairs, fake=fake, u=u, prefix=pins.RUN_PREFIX)


def test_run_stage_end_to_end_on_the_fake_model(fake_env):
    from bridge_jspace import pins

    pairs = fake_env.pairs
    out = D.stage_run(f"{fake_env.prefix}fake_48", "test", steps=2, ks=(1, 2))
    la = X.PREDICTED[pins.TARGET]
    assert not any(p.name.startswith(("verdict", "depth")) for p in out.iterdir())  # sealed
    m = json.loads((out / "manifest.json").read_text())
    assert m["layers"] == [la] and m["ks"] == [1, 2] and "sealed" in m and m["routes"]["used"] == 4
    held = [p for p in pairs if p["split"] != "train"]
    rows = X.read_jsonl(out / "outcomes.jsonl")
    arms = D.arm_names((1, 2))
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (p["scene"], w, a) for p in held for w in X.READERS for a in arms
    }
    assert all(r["layer"] == la for r in rows)
    # R: one per reader, k and baseline; orthonormal columns; the geometry per pair and R
    blob = torch.load(out / "R.pt")
    mats = blob["R"][f"L{la}"]
    assert set(mats) == set(arms) - {"none", "whole"}
    for key, r in mats.items():
        k = int(key.rsplit("k", 1)[1])
        assert r.shape == (D_MODEL, k) and torch.allclose(r.T @ r, torch.eye(k), atol=1e-4)
    assert np.allclose(blob["U"].numpy(), fake_env.u)
    geo = X.read_jsonl(out / "geometry.jsonl")
    assert len(geo) == len(pairs) * len(mats)
    for g in geo:
        assert 0 <= g["energy"] <= 1 + 1e-6 and 0 <= g["in_jpp25"] <= 1 + 1e-6 and 0 <= g["outside_union"] <= 1 + 1e-6
        assert g["in_jpp25"] <= g["in_jpp100"] + 1e-6
    # the random R's energy is small (k / d of the change), a trained R's share inside U lies in [0, 1]
    st = torch.load(out / f"states_L{la}.pt")
    assert st["delta"].shape == (len(pairs), D_MODEL) and st["scenes"] == [p["scene"] for p in pairs]
    ro = json.loads((out / "readouts.json").read_text())[f"L{la}"]
    assert ro["rank_U"] == 4 and ro["rank_Ufit"] == 2 and set(ro["principal_angles_deg"]) == {"k1", "k2"}
    assert len(ro["principal_angles_deg"]["k2"]) == 2 and 0 <= ro["R_PP_k1"]["cos2_U"] <= 1
    # the states: delta = h_S - h_O at the bridge token of the lookup's prompts
    p0 = pairs[0]
    ids = p0["readers"][X.LOOKUP]["ids"]
    h = {v: fake_env.fake.run(torch.tensor([ids[v]]), record=(la,))[1][la][p0["pos"]] for v in ("org", "alt")}
    assert torch.allclose(st["delta"][0], h["alt"] - h["org"], atol=1e-5)
    # the read under R: the AddRows edit is R R^T delta at the bridge position (checked through the fake's own forward)
    r = mats["R_PP_k2"]
    part = (st["delta"][0:1] @ r) @ r.T
    from scripts.exp04_brew_parts import AddRows

    lg = fake_env.fake.generate_batch(
        torch.tensor([ids["org"] + p0["space"]]), 1, [{la: AddRows(part, [p0["pos"]])}], first_logits=True
    )[1]
    rec = next(r_ for r_ in rows if r_["scene"] == p0["scene"] and r_["reader"] == X.LOOKUP and r_["arm"] == "R_PP_k2")
    assert rec["top"] == int(lg[0].argmax()) if p0["split"] != "train" else True
    train = X.read_jsonl(out / "train.jsonl")
    assert {t["R"] for t in train} == {k for k in mats if not k.startswith("rand")}
    assert len(X.read_jsonl(out / "routes.jsonl")) == 4 * 2 * (2 + 2 + 2)


def test_verdict_is_sealed_until_dans_answer(fake_env, monkeypatch):
    out = D.stage_run(f"{fake_env.prefix}fake_48s", "test", steps=1, ks=(1, 2))
    monkeypatch.setattr(D, "dan_answer", lambda *_: "")
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_verdict([out.name], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_depth([out.name], n_boot=50)


def test_verdict_and_depth_stages_on_the_fake_runs(fake_env, monkeypatch):
    from bridge_jspace import pins

    la = X.PREDICTED[pins.TARGET]
    main = D.stage_run(f"{fake_env.prefix}fake_48v", "test", steps=1, ks=(1, 2))
    monkeypatch.setattr(D, "KS", (1, 2))
    monkeypatch.setattr(D, "dan_answer", lambda *_: "(a) yes 60%")
    out = D.stage_verdict([main.name], n_boot=50)
    blob = json.loads((out / "verdict.json").read_text())
    mdl = blob["models"][0]
    assert blob["dan"] == "(a) yes 60%" and mdl["layer"] == la and set(mdl["rules"]) >= {"a", "b", "c", "d"}
    for w in X.READERS:
        t = mdl["readers"][w]["test"]
        assert t["n"] == sum(p["split"] == "test" and p["stored_whole"][w] for p in fake_env.pairs)
        assert mdl["readers"][w]["k"] in (1, 2) and len(t["own_minus_cross"]) == 3
    assert "R_PP_k1" in mdl["geometry"] and mdl["routes"]["R_PP_k1"]["n"] == 4
    md = (out / "verdict.md").read_text()
    assert "As computed" in md and "(a)" in md and (out / "examples.md").read_text().count("⟦bridge:") > 0
    # D3: a depth run at two other layers (no shuffled baselines, no routes), then the depth verdict over both runs
    depth = D.stage_run(f"{fake_env.prefix}fake_d3", "test", layers=(la // 2, la - 4), depth=True, steps=1, ks=(1, 2))
    m = json.loads((depth / "manifest.json").read_text())
    assert m["depth"] and m["layers"] == [la // 2, la - 4] and not (depth / "routes.jsonl").exists()
    assert D.arm_names((1, 2), shuffled=False) == m["arms"] and "shuf_PP_k1" not in m["arms"]
    ro = json.loads((depth / "readouts.json").read_text())
    assert set(ro) == {f"L{la // 2}", f"L{la - 4}"} and ro[f"L{la // 2}"]["R_PP_k1"]["cos2_U"] is None
    dv = D.stage_depth([main.name, depth.name], n_boot=50)
    dblob = json.loads((dv / "depth.json").read_text())
    assert set(dblob["layers"]) == {str(la // 2), str(la - 4), str(la)} and set(dblob["rule"]) >= {
        "leaves_the_lens",
        "recall_stays",
    }
    assert "leaves the lens" in (dv / "depth.md").read_text()
    with pytest.raises(AssertionError, match="two runs"):
        D.stage_depth([main.name, main.name], n_boot=50)


def _tiny_gdn():
    from transformers.models.qwen3_5 import configuration_qwen3_5 as cq
    from transformers.models.qwen3_5 import modeling_qwen3_5 as mq

    cfg = cq.Qwen3_5TextConfig(hidden_size=32, linear_num_key_heads=2, linear_num_value_heads=2, linear_key_head_dim=8,
                               linear_value_head_dim=8, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=1,
                               head_dim=16, intermediate_size=64, vocab_size=64)  # fmt: skip
    return mq, torch.nn.Sequential(mq.Qwen3_5GatedDeltaNet(cfg, 0))


def test_torch_gdn_switch_off_leaves_the_kernel(monkeypatch):
    mq, hf = _tiny_gdn()
    monkeypatch.delenv(D.GDN_ENV, raising=False)
    rule = mq.torch_chunk_gated_delta_rule
    assert D.torch_gdn(hf) is None and mq.torch_chunk_gated_delta_rule is rule
    assert D.torch_gdn(torch.nn.Sequential(torch.nn.Linear(2, 2))) is None


def test_torch_gdn_switch_puts_the_torch_reference_in_and_keeps_the_output(monkeypatch):
    # x48_1_9b (28 Oct): fla's gated backward refuses on Hopper with Triton 3.6; the switch routes the GDN layers to
    # transformers' own differentiable torch reference, which must compute the same rule and carry gradients
    mq, hf = _tiny_gdn()
    monkeypatch.setattr(mq, "torch_chunk_gated_delta_rule", mq.torch_chunk_gated_delta_rule)  # restored after the test
    x = torch.randn(1, 5, 32, requires_grad=True)
    before = hf[0](x).detach()
    monkeypatch.setenv(D.GDN_ENV, "torch")
    assert D.torch_gdn(hf) == mq.__name__
    assert mq.torch_chunk_gated_delta_rule.__name__ == "torch_chunk_gated_delta_rule"
    after = hf[0](x)
    torch.testing.assert_close(after.detach(), before, rtol=1e-4, atol=1e-5)
    after.sum().backward()
    assert x.grad is not None and torch.isfinite(x.grad).all()


def test_gradcheck_stage_on_the_fake_model(fake_env, monkeypatch):
    """Batch 52 (Lightning ports): the gradcheck stage end to end on the fake model (no hub kernels there, so both paths
    are one and every bar holds); the CUDA timers stubbed. It refuses without the switch, writes its files, passes."""
    monkeypatch.setattr(torch.cuda, "synchronize", lambda: None)
    monkeypatch.setattr(torch.cuda, "reset_peak_memory_stats", lambda: None)
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda: 0)
    monkeypatch.setattr(D, "torch_mamba", lambda _hf: "stub")
    from bridge_jspace import pins

    monkeypatch.setitem(X.PREDICTED, pins.TARGET, 2)  # an early layer: deep in the fake the read saturates (gradient 0)
    monkeypatch.delenv(D.MAMBA_ENV, raising=False)
    with pytest.raises(AssertionError, match="BJ_DAS_MAMBA=torch"):
        D.stage_gradcheck(f"{fake_env.prefix}fake_gc0", "test")
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    out = D.stage_gradcheck(f"{fake_env.prefix}fake_gc", "test")
    res = json.loads((out / "gradcheck.json").read_text())
    assert res["pass"] and res["rows"] == 16 and res["reads"] == 32 and all(res["checks"].values())
    assert res["kernel_grad"]["cos_with_torch"] > 0.999 and res["torch_grad"]["grad_norm"] > 0
    assert len(res["train_subspace"]["log"]) == 2 and os.environ[D.MAMBA_ENV] == "torch"
    assert "PASS" in (out / "gradcheck.md").read_text()
    m = json.loads((out / "manifest.json").read_text())
    assert m["mamba_kernel"] == "stub" and m["stage"] == "gradcheck"
