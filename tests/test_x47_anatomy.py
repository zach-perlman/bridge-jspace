"""Batch 47, test 47.8 (scripts/x47_anatomy.py, scripts/x47_anatomy_fig.py): the split by entity, the per-layer fit on
planted states, the parts and their random pairing, the arms, l_J / l_P / l_probe and rules (a)-(e) on planted curves,
the run stage end to end on a tiny fake causal model (CPU, no real model), the sealed verdict and the figure."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_anatomy as A
from scripts import x47_anatomy_fig as F

LOOKUP_Q, RECALL_Q = "Which locker belongs to Iris's pick?", "How many legs does Iris's pick have?"


def wrap(context: str, question: str) -> str:
    return f"<|im_start|>user\n{context}\n{question}<|im_end|>\nAnswer:"


class WordTok:
    """Words with their leading whitespace as tokens (copied from tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


# ---- fake routes scenes (x6_routes.encode's shape, on the fake tokenizer) -------------------------------------------


def fake_scenes(tok, n: int, seed: int = 1, animals: list[str] | None = None) -> tuple[list[dict], dict]:
    """n base scenes, each as C0 and C2, as x6_routes.scenes builds them (lockers first, three picks)."""
    legs = A.legs_of()
    pool = animals or sorted(a for a in legs if 0 <= legs[a] <= 9)[:10]
    rng = random.Random(seed)
    out = []
    for i in range(1, n + 1):
        while True:
            a_, b_, c_ = rng.sample(pool, 3)
            if legs[a_] != legs[b_]:
                break
        a, b, c, _d, e = rng.sample(range(1, 10), 5)  # d: C1's new digit, unused here
        order = rng.sample([a_, b_, c_], 3)
        val = {a_: a, b_: b, c_: c}
        others = rng.sample(["Noah", "Peter", "Mia"], 2)
        picks = rng.sample([("Iris", a_), (others[0], b_), (others[1], c_)], 3)
        o = R.context([(x, val[x]) for x in order], picks)
        for cond in ("C0", "C2"):
            if cond == "C0":
                s = R.context([(x, val[x]) for x in order], [(q, b_ if q == "Iris" else x) for q, x in picks])
                expect = {"switch": b, "original": a}
            else:
                sw = {b_: c_, c_: b_}
                s_lock = [(sw.get(x, x), e if sw.get(x, x) == b_ else val[sw.get(x, x)]) for x in order]
                s = R.context(s_lock, [(q, b_ if q == "Iris" else x) for q, x in picks])
                expect = {"identity": b, "position": c, "value": e, "original": a}
            s_answer = expect["switch"] if "switch" in expect else expect["value"]
            readers, pos = {}, None
            for w, q, ans in ((X.LOOKUP, LOOKUP_Q, (a, s_answer)), (X.RECALL, RECALL_Q, (legs[a_], legs[b_]))):
                ids = {v: tok(wrap(ctx, q)).input_ids for v, ctx in (("org", o), ("alt", s))}
                text = wrap(o, q)
                enc = tok(text, return_offsets_mapping=True)
                sent = f"Iris picked the {a_}."
                w0 = text.index(sent) + sent.index(a_)
                at = [j for j, (x, y) in enumerate(enc.offset_mapping) if x < w0 + len(a_) and y > w0]
                assert len(at) == 1 and (pos is None or at[0] == pos)
                pos = at[0]
                readers[w] = {"question": q, "answer": str(ans[0]), "cf_answer": str(ans[1]), "ids": ids,
                              "tok_A": tok(str(ans[0])).input_ids[0], "tok_b": tok(str(ans[1])).input_ids[0]}  # fmt: skip
            routes = {k: tok(str(v)).input_ids[0] for k, v in expect.items() if k != "switch"}
            out.append({"scene": f"{cond}-{i:04d}", "condition": cond, "rendering": "chat", "domain": "animals",
                        "bridge": a_, "cf_bridge": b_, "context": o, "cf_context": s, "pos": pos,
                        "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "expect": {k: int(v) for k, v in expect.items()},
                        "route_tokens": routes, "readers": readers})  # fmt: skip
    return out, {}


def fake_competence(model, cases, digits, ws) -> list[dict]:
    return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "greedy": "5", "said": "5",
             "right": True, "read_right": True, "ws_skipped": 0, "cand_right": True}
            for c in cases for w in X.READERS for v in ("org", "alt")]  # fmt: skip


def fake_locker_positions(tok, c: dict) -> list[list[int]]:
    ids = c["readers"][X.LOOKUP]["ids"]["org"]
    words = [tok.decode([t]) for t in ids]
    out = []
    for m in re.finditer(r"The locker of the (\w+) is (\d)\.", c["context"]):
        item = words.index(f" {m.group(1)}")
        digit = next(j for j in range(item, len(words)) if words[j] == f" {m.group(2)}.")
        out.append([item, digit])
    return out


class FakeModel:
    """A tiny causal stand-in (tests/test_x45p.py's): each block mixes the running mean of the positions so far into
    every position; an edit acts on a block's output."""

    def __init__(self, tok: WordTok, n_layers: int = 12, d: int = 32, vocab: int = 160):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers = tok, n_layers
        self.device = torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()
        self.reads = 0

    def forward(self, ids: list[int], edits: dict):
        h = self.emb[torch.as_tensor(ids)]
        states = {}
        for layer in range(self.n_layers):
            h = h + 0.1 * torch.cumsum(h, 0) / torch.arange(1, h.shape[0] + 1)[:, None]
            if layer in edits:
                h = edits[layer](h)
            states[layer] = h.clone()
        return self.unemb @ h[-1], states

    def run(self, ids, edits=None, record=()):
        logits, states = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: states[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        self.reads += len(edits)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return list(range(64))


class FakeLens:
    def __init__(self, model, name):
        assert name == "jpp"
        self.model = model

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)

    def readout(self, h, layer):
        w = torch.randn(32, 160, generator=torch.Generator().manual_seed(100 + layer))
        return h.float() @ w


def unit_rows(n: int, d: int, seed: int):
    v = torch.randn(n, d, generator=torch.Generator().manual_seed(seed))
    return v / v.norm(dim=1, keepdim=True)


# ---- scenes and the split ----------------------------------------------------------------------------------------


def test_enrich_adds_slot_pick_and_recall_tokens():
    tok = WordTok()
    raw, _ = fake_scenes(tok, 6)
    cases = A.enrich(tok, raw)
    assert len(cases) == 12
    for c in cases:
        items = re.findall(r"The locker of the (\w+)", c["context"])
        assert c["slot"] == items.index(c["bridge"]) and c["pick_index"] in (3, 4, 5) and c["sentences"] == 6
        assert c["layout"] == "LLL" + "." * (c["pick_index"] - 3)
        assert c["slot_item"] not in (c["bridge"], c["cf_bridge"]) and c["base"] == c["scene"][3:]
        rt = c["recall_tokens"]
        assert rt["changed"] == c["readers"][X.RECALL]["tok_b"] and rt["original"] == c["readers"][X.RECALL]["tok_A"]
    c2 = next(c for c in cases if c["condition"] == "C2")
    assert A.recall_classify(c2["recall_tokens"]["changed"], c2) == "changed"
    assert A.recall_classify(c2["recall_tokens"]["slot"], c2) in ("slot", "changed", "original")
    assert A.recall_classify(-1, c2) == "other"
    assert R.classify(c2["route_tokens"]["position"], c2) == "position"


def test_recall_classify_priority_when_items_share_legs():
    c = {"recall_tokens": {"changed": 7, "original": 7, "slot": 7}}
    assert A.recall_classify(7, c) == "changed"
    c = {"recall_tokens": {"changed": 1, "original": 7, "slot": 7}}
    assert A.recall_classify(7, c) == "original"


def test_split_by_entity_is_disjoint_and_sized():
    cases = [{"scene": f"C2-{i:04d}", "bridge": f"e{i % 9}"} for i in range(90)]
    test, fit, info = A.split_by_entity(cases, 30, seed=0, n_fit_min=20, n_fit_max=35)
    assert len(test) == 30 and len(fit) == 35 and info["eligible"] == 90
    assert not ({c["bridge"] for c in test} & {c["bridge"] for c in fit})
    assert set(info["test_entities"]) | set(info["fit_entities"]) == {f"e{i}" for i in range(9)}
    assert [c["scene"] for c in test] == sorted(c["scene"] for c in test)  # scene order kept
    again, _, _ = A.split_by_entity(cases, 30, seed=0, n_fit_min=20, n_fit_max=35)
    assert [c["scene"] for c in again] == [c["scene"] for c in test]  # seeded
    with pytest.raises(SystemExit, match="split by entity"):
        A.split_by_entity(cases, 80, seed=0, n_fit_min=20)


def test_locker_layers_every_eighth_model_layer():
    assert A.locker_layers(A.LAYERS["qwen3.5-9b"]) == (2, 10, 18, 26)
    assert A.locker_layers(A.LAYERS["muse-glimmer-30b"]) == (2, 10, 18, 26, 34, 42, 50)
    assert A.locker_layers(A.LAYERS["qwen3.6-27b"]) == (4, 12, 20, 28, 36, 44, 52, 60)
    assert A.locker_layers((5,)) == (5,)


def test_sweeps_hold_the_fixed_layer_and_the_arms_are_fourteen():
    from scripts import x51_lightning as L6

    for t, layers in A.LAYERS.items():  # Lightning's fixed layer: the committed one (batch 52, BJ_PREDICTED_LAYER)
        assert (L6.committed_layer() if t == L6.TARGET else X.PREDICTED[t]) in layers
    assert len(A.ARMS) == 14 and A.ARMS[:2] == ("none", "whole")
    assert len(A.read_labels((2, 4), A.ARMS)) == 1 + 2 * 13
    assert A.read_labels((2,), A.C0_ARMS) == [(None, "none"), (2, "whole")]


# ---- the fit on planted states -----------------------------------------------------------------------------------


def planted_states(n: int, d: int, seed: int = 0):
    """States = a layout mean + a slot code + an entity code + noise; the slot code spans two directions."""
    g = torch.Generator().manual_seed(seed)
    rng = random.Random(seed)
    slot_dirs, ent_dirs = torch.randn(3, d, generator=g), torch.randn(8, d, generator=g)
    lay_dirs = torch.randn(3, d, generator=g) * 5
    fit = []
    h, h_s = torch.empty(n, d), torch.empty(n, d)
    for i in range(n):
        slot, ent, lay = rng.randrange(3), rng.randrange(8), rng.randrange(3)
        base = lay_dirs[lay] + 3 * slot_dirs[slot] + 0.3 * torch.randn(d, generator=g)
        h[i] = base + 3 * ent_dirs[ent]
        h_s[i] = base + 3 * ent_dirs[(ent + 1) % 8]  # S's bridge word carries the other entity's code
        fit.append({"slot": slot, "bridge": f"e{ent}", "cf_bridge": f"e{(ent + 1) % 8}", "layout": "LLL" + "." * lay,
                    "pick_index": 3 + lay})  # fmt: skip
    return h, h_s, fit, slot_dirs, ent_dirs


def test_fit_layer_recovers_slot_and_entity_codes():
    h, h_s, fit, slot_dirs, _ = planted_states(120, 24)
    f = A.fit_layer(h, h_s, fit)
    assert f["U"].shape == (24, 2) and f["Id"].shape[1] == 7 and sorted(f["slot_means"]) == [0, 1, 2]
    assert set(f["entity_means"]) == {f"e{i}" for i in range(8)}
    # U_l spans the slot code's differences: a slot difference projects almost fully onto it
    diff = (slot_dirs[1] - slot_dirs[0]).double()
    assert float((f["U"].T @ diff).norm() ** 2 / diff.norm() ** 2) > 0.9
    ho = A.held_out_accuracy(f, h, fit)
    assert ho["slot"] > 0.95 and ho["entity"] > 0.95 and ho["rank_U"] == 2 and ho["entity_n"] == 120


def test_layout_free_takes_each_groups_mean_out():
    h = torch.tensor([[1.0, 0.0], [3.0, 0.0], [0.0, 5.0]])
    res, means = A.layout_free(h, ["a", "a", "b"])
    assert torch.allclose(res[:2], torch.tensor([[-1.0, 0.0], [1.0, 0.0]], dtype=torch.float64))
    assert torch.allclose(means["b"], h.mean(0).double())  # a singleton keeps itself minus the grand mean


def test_probes_on_planted_states_read_slot_and_identity():
    h, _, fit, _, _ = planted_states(100, 24)
    for i, c in enumerate(fit):
        c["readers"] = {X.LOOKUP: {"answer": str(1 + c["slot"] * 2)}}  # the digit tied to the slot: decodable
        c["scene"] = f"s{i}"
    p = A.probes_at(h.numpy(), fit, n_boot=50)
    assert set(p) == set(A.PR.TARGETS)
    assert p["locker sentence"]["probe"][0] > 0.9 and p["bridge identity"]["probe"][0] > 0.9


# ---- the parts and their random pairing ----------------------------------------------------------------------------


def test_random_atoms_basis_is_orthonormal_and_seeded():
    jdic = unit_rows(64, 32, 0)
    q = A.random_atoms_basis(jdic, 777)
    assert q.shape == (32, 32) and torch.allclose(q.T @ q, torch.eye(32), atol=1e-4)
    assert torch.allclose(q, A.random_atoms_basis(jdic, 777))
    assert not torch.allclose(q, A.random_atoms_basis(jdic, 778))


def test_identity_parts_are_outside_the_atoms_and_zero_where_missing():
    from scripts.x0_parts import omp_atoms

    jdic = unit_rows(64, 32, 1)
    x = torch.randn(4, 32, generator=torch.Generator().manual_seed(2))
    atoms = omp_atoms(jdic, x, 5)
    means = {"a": torch.randn(32, generator=torch.Generator().manual_seed(3)).double(),
             "b": torch.randn(32, generator=torch.Generator().manual_seed(4)).double()}  # fmt: skip
    part, inside, missing = A.identity_parts(x, atoms, jdic, means, [("a", "b"), ("a", "b"), ("a", "zz"), ("b", "a")])
    assert missing == [False, False, True, False] and inside[2] is None and part[2].abs().sum() == 0
    for i in (0, 1, 3):
        assert 0 <= inside[i] <= 1
        span = jdic[atoms[i]].double()
        assert float((span @ part[i].double()).abs().max()) < 1e-4  # the part is orthogonal to the atoms
        assert part[i].norm() > 0


def test_arms_keep_plus_no_is_the_whole_and_random_shares_match():
    from scripts import statement_positions as SP

    d = 32
    x = torch.randn(6, d, generator=torch.Generator().manual_seed(5))
    jdic = unit_rows(64, d, 6)
    u = torch.linalg.qr(torch.randn(d, 2, generator=torch.Generator().manual_seed(7)))[0]
    parts = {"J": X.fit(jdic, x, 5, "signed"), "U": (x @ u) @ u.T, "I": torch.zeros_like(x)}
    sh = A.shares_of(x, parts)
    basis = SP.random_basis(d, torch.Generator().manual_seed(888))
    rand = {"J": SP.random_subspace_part(x, sh["J"], A.random_atoms_basis(jdic, 777)),
            "U": SP.random_subspace_part(x, sh["U"], basis), "I": SP.random_subspace_part(x, sh["I"], basis)}  # fmt: skip
    arms = A.arms_of(x, parts, rand)
    assert tuple(arms) == A.ARMS[1:]
    for p in A.PARTS:
        assert torch.allclose(arms[f"keep_{p}"] + arms[f"no_{p}"], x, atol=1e-5)
        assert torch.allclose(arms[f"keep_{p}_rand"] + arms[f"no_{p}_rand"], x, atol=1e-5)
    rsh = A.shares_of(x, rand)
    assert float((rsh["J"] - sh["J"]).abs().max()) < 0.12 and float((rsh["U"] - sh["U"]).abs().max()) < 0.12
    assert rsh["I"].abs().max() == 0


def test_overlap_of_a_part_inside_atoms():
    from scripts.x0_parts import omp_atoms

    jdic = unit_rows(64, 32, 8)
    x = torch.randn(3, 32, generator=torch.Generator().manual_seed(9))
    atoms = omp_atoms(jdic, x, 4)
    part = X.fit(jdic, x, 4, "signed")
    ov = A.overlap(part, atoms, jdic)
    assert all(abs(v - 1.0) < 1e-4 for v in ov)  # the J part lies in its own atoms' span
    assert all(0 <= v <= 1 for v in A.overlap(x, atoms, jdic))


# ---- l_J, l_P, l_probe and the rules on planted curves -------------------------------------------------------------


def planted_cells(layers, interp, pos, loss_j, keep_j_id, keep_i_id, value=None, recall_sw=None, recall_loss=None):
    cells = {}
    for la in layers:
        lk = {"interpretable": la in interp, "switch": {"whole": [0.8 if la in interp else 0.1, 0, 1]},
              "share": {a: {rt: [0.0, 0, 0] for rt in A.LOOKUP_ROUTES} for a in A.ARMS}, "loss": {}}  # fmt: skip
        lk["share"]["whole"]["position"] = [pos.get(la, 0.0), 0, 1]
        lk["share"]["whole"]["value"] = [(value or {}).get(la, 0.0), 0, 1]
        lk["share"]["keep_J"]["identity"] = [keep_j_id.get(la, 0.0), 0, 1]
        lk["share"]["keep_I"]["identity"] = [keep_i_id.get(la, 0.0), 0, 1]
        if la in loss_j:
            lk["loss"]["J"] = {"excess": [loss_j[la], loss_j[la] - 0.1, loss_j[la] + 0.1]}
        rc = {"interpretable": True, "switch": {"whole": [(recall_sw or {}).get(la, 0.9), 0, 1]},
              "share": {a: {rt: [0.0, 0, 0] for rt in A.RECALL_ROUTES} for a in A.ARMS},
              "loss": {"J": {"excess": [(recall_loss or {}).get(la, 0.5), 0, 1]}}}  # fmt: skip
        cells[la] = {"layer": la, "lookup": lk, "recall": rc}
    return cells


def planted_fit(layers, slot):
    return {
        "per_layer": {str(la): {"probes": {"locker sentence": {"probe": [slot.get(la, 0.0), 0, 1]}}} for la in layers}
    }


def test_first_layers_and_handoff():
    layers = (2, 4, 6, 8, 10, 12)
    interp = (4, 6, 8, 10, 12)
    cells = planted_cells(layers, interp, pos={8: 0.25, 10: 0.4, 12: 0.5}, loss_j={2: 0.9, 4: 0.5, 6: 0.1, 8: 0.05, 10: 0.0, 12: 0.0},
                          keep_j_id={4: 0.6, 12: 0.05}, keep_i_id={12: 0.4})  # fmt: skip
    fit = planted_fit(layers, {6: 0.85, 8: 0.9, 10: 0.95, 12: 0.95})
    fl = A.first_layers(cells, fit, layers)
    assert (fl["l_J"], fl["l_P"], fl["l_probe"]) == (6, 8, 6)  # l_J at 6: the bar is inclusive (0.1 <= 0.1)
    r = A.rules(cells, fit, layers, 12)
    assert r["a"] == {"holds": True, "gap": 2, "why": "l_P = 8, l_J = 6", "gap_bucket": "<= 2"}
    assert r["b"]["holds"] and not r["b"]["probe_after_use"]
    assert r["c"]["holds"] and r["c"]["earliest"] == 4 and r["c"]["crossing"] == 12
    assert (
        r["d"]["holds"] and r["e"]["window"] == list(layers) and r["e"]["needs_J_throughout"] and r["e"]["onset"] == 2
    )


def test_l_j_needs_the_loss_to_stay_low_and_skips_uninterpretable_layers():
    layers = (2, 4, 6, 8)
    # a late rebound above 0.10 at an interpretable layer: no l_J
    cells = planted_cells(
        layers, (2, 4, 6, 8), pos={}, loss_j={2: 0.05, 4: 0.05, 6: 0.3, 8: 0.05}, keep_j_id={}, keep_i_id={}
    )
    assert A.first_layers(cells, planted_fit(layers, {}), layers)["l_J"] == 8
    cells = planted_cells(
        layers, (2, 4, 6, 8), pos={}, loss_j={2: 0.05, 4: 0.05, 6: 0.05, 8: 0.3}, keep_j_id={}, keep_i_id={}
    )
    assert A.first_layers(cells, planted_fit(layers, {}), layers)["l_J"] is None
    # the rebound at a layer that is not interpretable is not read
    cells = planted_cells(
        layers, (2, 4, 8), pos={}, loss_j={2: 0.05, 4: 0.05, 6: 0.3, 8: 0.05}, keep_j_id={}, keep_i_id={}
    )
    assert A.first_layers(cells, planted_fit(layers, {}), layers)["l_J"] == 2
    r = A.rules(cells, planted_fit(layers, {}), layers, 8)
    assert r["a"]["holds"] is None and r["a"]["gap"] is None and r["b"]["holds"] is None


def test_rules_b_c_d_e_fail_on_the_right_curves():
    layers = (2, 4, 6, 8)
    interp = (4, 6, 8)
    cells = planted_cells(layers, interp, pos={4: 0.3}, loss_j={4: 0.0, 6: 0.0, 8: 0.0}, keep_j_id={4: 0.6, 8: 0.2},
                          keep_i_id={8: 0.4}, value={6: 0.06}, recall_sw={2: 0.9, 4: 0.9, 6: 0.4, 8: 0.3},
                          recall_loss={2: 0.2, 4: 0.5})  # fmt: skip
    fit = planted_fit(layers, {8: 0.9})
    r = A.rules(cells, fit, layers, 8)
    assert r["a"]["holds"] and r["a"]["gap"] == 0
    assert r["b"]["holds"] is False and r["b"]["probe_after_use"]  # the probe reaches 0.8 only after l_P
    assert r["c"]["holds"] is False  # keep_J identity at L is 0.2 > 0.1
    assert r["d"]["holds"] is False and r["d"]["max_value"] == pytest.approx(0.06)
    assert r["e"]["window"] == [2, 4] and r["e"]["needs_J_throughout"] is False and r["e"]["onset"] == 4


def test_batch_rules_count_c_over_models():
    def m(target, c, status="tested"):
        return {"target": target, "status": status, "rules": {"a": {"holds": True, "gap": 1, "gap_bucket": "<= 2"},
                                                             "b": {"holds": True}, "c": {"holds": c}, "d": {"holds": True}}}  # fmt: skip

    b = A.batch_rules([m("x", True), m("y", True), m("z", False)])
    assert b["c"]["holds"] and b["c"]["held_on"] == ["x", "y"]
    b = A.batch_rules([m("x", True), m("y", False), {"target": "z", "status": "pending"}])
    assert not b["c"]["holds"] and b["c"]["pending"] == ["z"] and set(b["a"]) == {"x", "y"}


def test_layer_cells_on_planted_rows():
    rows, norms = [], []
    scenes = [f"s{i}" for i in range(40)]
    for i, s in enumerate(scenes):
        ent = f"e{i % 8}"
        norms.append({"scene": s, "layer": 4, "I_missing": i >= 36})
        for la in (None, 4):
            for a in A.ARMS:
                if (la is None) != (a == "none"):
                    continue
                # the whole change moves 30 of 40 lookups (position); without J: 15; without the random part: 27
                moved = (
                    i < 30
                    if a in ("whole", "no_U", "no_I", "no_U_rand", "no_I_rand", "keep_J")
                    else i < 15
                    if a == "no_J"
                    else i < 27
                    if a == "no_J_rand"
                    else False
                )
                rows.append({"scene": s, "condition": "C2", "entity": ent, "reader": X.LOOKUP, "layer": la, "arm": a,
                             "route": "position" if moved else "original", "switched": 0})  # fmt: skip
                rows.append({"scene": s, "condition": "C2", "entity": ent, "reader": X.RECALL, "layer": la, "arm": a,
                             "route": "changed" if moved else "other", "switched": int(moved)})  # fmt: skip
    c = A.layer_cells(rows, norms, 4, n_boot=200)
    lk = c["lookup"]
    assert lk["n"] == 40 and lk["interpretable"] and lk["switch"]["whole"][0] == pytest.approx(0.75)
    assert lk["share"]["whole"]["position"][0] == pytest.approx(0.75)
    assert lk["loss"]["J"]["excess"][0] == pytest.approx((1 - 15 / 30) - (1 - 27 / 30))
    assert lk["loss"]["U"]["excess"][0] == pytest.approx(0.0) and lk["loss"]["I"]["n"] == 36  # I missing on 4 scenes
    assert c["recall"]["switch"]["whole"][0] == pytest.approx(0.75) and c["recall"]["loss"]["J"]["excess"][
        0
    ] == pytest.approx(0.4)


# ---- the run stage on the fake model ------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    fake = FakeModel(tok)
    target = pins.TARGET
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(R, "scenes", lambda tok, n, seed=0, rendering="chat": fake_scenes(tok, 40))
    monkeypatch.setattr(R, "c0_reference", lambda t: None)
    monkeypatch.setattr(A, "competence", fake_competence)
    monkeypatch.setattr(A, "locker_token_positions", fake_locker_positions)
    monkeypatch.setattr(A, "we_dictionary", lambda model, lens, layer, letters: unit_rows(64, 32, 500 + layer))
    monkeypatch.setitem(A.LAYERS, target, (2, 6, 10))
    monkeypatch.setitem(A.N_TEST, target, 8)
    monkeypatch.setitem(A.C0_MIN, target, 0.0)
    monkeypatch.setitem(X.PREDICTED, target, 6)
    monkeypatch.setattr(A, "N_FIT_MIN", 10)
    monkeypatch.setattr(A, "N_FIT_MAX", 24)
    monkeypatch.setattr(A, "N_LOCKER", 5)
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x47_anatomy")
    monkeypatch.setattr(A, "SPEC", tmp_path / "batch47.yaml")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    A.SPEC.write_text("spec\n")
    out = A.stage_run(f"{pins.RUN_PREFIX}fake_x47_anatomy", "test", n_boot=50)
    return SimpleNamespace(tok=tok, fake=fake, out=out, target=target)


def test_run_stage_end_to_end_on_the_fake_model(fake_run):
    out = fake_run.out
    assert {p.name for p in out.iterdir()} == {"manifest.json", "competence.jsonl", "gate.json", "split.json", "cases.jsonl",
                                               "fit.json", "norms.jsonl", "cache", "outcomes.jsonl", "examples_greedy.jsonl",
                                               "c0_check.json"}  # sealed: no verdict  # fmt: skip
    m = json.loads((out / "manifest.json").read_text())
    assert (
        m["layers"] == [2, 6, 10] and m["fixed_layer"] == 6 and "sealed" in m and m["cache"]["layers_locker"] == [2, 10]
    )
    split = json.loads((out / "split.json").read_text())
    assert split["test"] == 8 and 10 <= split["fit"] <= 24 and split["c0_test"] == 8
    cases = X.read_jsonl(out / "cases.jsonl")
    halves = {h: [c for c in cases if c["half"] == h] for h in ("test", "fit", "c0")}
    assert not ({c["bridge"] for c in halves["test"]} & {c["bridge"] for c in halves["fit"]})
    assert {c["base"] for c in halves["c0"]} == {c["base"] for c in halves["test"]}
    rows = X.read_jsonl(out / "outcomes.jsonl")
    want = {
        (c["scene"], w, la, a) for c in halves["test"] for w in X.READERS for la, a in A.read_labels((2, 6, 10), A.ARMS)
    }
    want |= {
        (c["scene"], w, la, a)
        for c in halves["c0"]
        for w in X.READERS
        for la, a in A.read_labels((2, 6, 10), A.C0_ARMS)
    }
    assert {(r["scene"], r["reader"], r["layer"], r["arm"]) for r in rows} == want and len(rows) == len(want)
    assert all(r["route"] in A.LOOKUP_ROUTES for r in rows if r["reader"] == X.LOOKUP and r["condition"] == "C2")
    assert all(r["route"] in A.RECALL_ROUTES for r in rows if r["reader"] == X.RECALL and r["condition"] == "C2")
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 8 * 3 and all(0 <= n["share_J"] <= 1 and len(n["atoms_J"]) == A.K for n in norms)
    assert all(abs(n["share_U_rand"] - n["share_U"]) < 0.15 for n in norms)
    fit = json.loads((out / "fit.json").read_text())
    for la in ("2", "6", "10"):
        f = fit["per_layer"][la]
        assert set(f["probes"]) == set(A.PR.TARGETS) and f["held_out"]["rank_U"] == 2 and 0 <= f["lens_top10"] <= 1
        assert f["n_fit"] == split["fit"] and f["median_share"]["J"] >= 0
    z = np.load(out / "cache" / "fit_states.npz")
    assert (
        z["O_L2"].shape == (split["fit"], 32)
        and z["O_L2"].dtype == np.float16
        and z["S_L10"].shape == (split["fit"], 32)
    )
    assert z["locker_L2"].shape == (5, 3, 2, 32) and "locker_L6" not in z
    b = np.load(out / "cache" / "bases.npz")
    assert (
        b["U_L6"].shape == (32, 2)
        and b["Id_L6"].shape[0] == 32
        and b["entity_means_L6"].shape[0] == len(fit["per_layer"]["6"]["entities"])
    )
    greedy = X.read_jsonl(out / "examples_greedy.jsonl")
    assert {g["layer"] for g in greedy} == {None, 6} and len(greedy) == 8 * 2 * 14
    assert json.loads((out / "c0_check.json").read_text())["ok"]


def test_verdict_view_and_figure_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(A, "dan_answer", lambda *a, **k: "yes (a) <= 2")
    out = A.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x47_8.json").read_text())
    m = blob["models"][0]
    assert (
        m["status"] == "tested"
        and set(m["cells"]) == {"2", "6", "10"}
        and set(m["rules"]) >= {"a", "b", "c", "d", "e", "l_J", "l_P", "l_probe"}
    )
    assert (out / "x47_8.md").exists() and (out / "x47_anatomy.png").exists()
    assert [x["status"] for x in blob["models"][1:]] == ["pending"] * (len(A.RUNS) - 1)
    text = (out / "x47_8.md").read_text()
    assert "Q47.8" in text and "UNVERIFIED" in text
    view = A.stage_view([fake_run.out.name])
    ex = (view / "examples.md").read_text()
    assert ex.count("### C2-") == 8 and ex.count("whole by layer: L2") == 16  # 8 items, two readers each
    fig = A.stage_figures(out)
    assert fig.exists()


def test_sealed_until_dans_answer(fake_run, monkeypatch):
    monkeypatch.setattr(A, "dan_answer", lambda *a, **k: "")
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict([fake_run.out.name], n_boot=20)
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_view([fake_run.out.name])


def test_dan_answer_reads_only_the_q47_8_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = (
        "**Q47.7** ...\n\nDan: x\n\n**Q47.8** (47.8)\n- (a) ...\n\nRule: ...\n\nDan:{}\n\n**Q-depth** ...\n\nDan: z\n"
    )
    monkeypatch.setattr(A.subprocess, "run", fake_git(blocks.format("")))
    assert A.dan_answer() == ""
    monkeypatch.setattr(A.subprocess, "run", fake_git(blocks.format(" (a) yes 60%")))
    assert A.dan_answer() == "(a) yes 60%"
    assert A.dan_answer(question="Q-depth") == "z"


def test_the_committed_predictions_file_has_the_q47_8_block():
    from bridge_jspace import pins

    text = (pins.REPO_ROOT / A.PREDICTIONS).read_text()
    assert "**Q47.8**" in text and "**Q-depth**" in text


# ---- the figure ---------------------------------------------------------------------------------------------------


def test_figure_builds_with_missing_quantities(tmp_path):
    rows = {"lookup.whole.identity": {4: [0.5, 0.4, 0.6], 8: [0.3, 0.2, 0.4]}, "lookup.whole.position": {4: [0.2, 0.1, 0.3]},
            "loss.lookup.J": {4: [0.5, 0.3, 0.7], 8: [0.0, -0.1, 0.1]}, "probe.slot": {4: [0.9, None, None]},
            "jpp_share.U": {8: [0.1, None, None]}}  # fmt: skip
    models = [{"target": "qwen3.5-9b", "n_layers": 32, "L": 12, "layers": [4, 8], "ni": {"lookup": [4], "recall": []}, "rows": rows},
              {"target": "muse-glimmer-30b", "n_layers": 52, "L": 26, "layers": [26], "ni": {"lookup": [], "recall": []}, "rows": {}}]  # fmt: skip
    path = F.figure(models, tmp_path / "fig.png", preview=True)
    assert path.exists()  # PNG only (Dan, 30 Oct)


def test_preview_models_have_the_contract(monkeypatch):
    from bridge_jspace import pins

    if not (X.RESULTS / "qwen35_9b_x0_necessity" / "outcomes.jsonl").exists():
        pytest.skip("no results here")
    models = F.preview_models()
    assert [m["target"] for m in models] == [t for t, _, _, _ in F.MODELS]
    for m in models:
        assert set(m) >= {"target", "n_layers", "L", "layers", "ni", "rows", "status"}
        for q, pts in m["rows"].items():
            assert all(isinstance(la, int) and len(v) == 3 for la, v in pts.items()), q
    assert pins.RESULTS_DIR.exists()


def test_run_takes_a_reduced_layer_grid(fake_run):
    # 49.4 (batch 49): the 27B's anatomy on a reduced grid passed on the command line; the fixed layer must be in it
    out = A.stage_run(f"{pins_run_prefix()}fake_x47_anatomy_reduced", "test", n_boot=50, layers=(2, 6))
    m = json.loads((out / "manifest.json").read_text())
    assert m["layers"] == [2, 6]
    with pytest.raises(AssertionError, match="fixed layer"):
        A.stage_run(f"{pins_run_prefix()}fake_x47_anatomy_nofixed", "test", n_boot=50, layers=(2, 10))


def pins_run_prefix() -> str:
    from bridge_jspace import pins

    return pins.RUN_PREFIX


def test_lightning_coverage_copies_muses_design():
    """Batch 52: Lightning runs Muse's 52-block design verbatim (every 4th layer L2-L50 holding L14, 200 test scenes,
    C0 >= 0.5) as a coverage run, outside 47.8's own RUNS."""
    lt = "nemotron-3.5-lightning"
    assert A.LAYERS[lt] == A.LAYERS["muse-glimmer-30b"] and 14 in A.LAYERS[lt]
    assert A.N_TEST[lt] == A.N_TEST["muse-glimmer-30b"] and A.C0_MIN[lt] == A.C0_MIN["muse-glimmer-30b"]
    assert lt not in A.RUNS and A.COVERAGE_RUNS[lt].startswith("nem35l_")


def test_coverage_verdict_needs_no_seal(tmp_path, monkeypatch):
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    monkeypatch.setattr(A, "unsealed", lambda: (_ for _ in ()).throw(AssertionError("sealed")))
    monkeypatch.setattr(A, "model_result", lambda r, n_boot: {"run": r, "target": "nemotron-3.5-lightning",
                                                                "status": "pending", "why": "planted"})  # fmt: skip
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(["nem35l_x52_anatomy"], n_boot=10)
    out = A.stage_verdict(["nem35l_x52_anatomy"], n_boot=10, coverage=True)
    assert out.name.startswith("x52_anatomy-")
    blob = json.loads((out / "x47_8.json").read_text())
    assert blob["dan"].startswith(A.NO_PREDICTION) and [m["target"] for m in blob["models"]] == [
        "nemotron-3.5-lightning"
    ]
    assert A.NO_PREDICTION in (out / "x47_8.md").read_text()
