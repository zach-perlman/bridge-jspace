"""Batch 49, test 49.8 (scripts/x49_das_pos.py): the routes position pairs (same item, its locker sentence moved to
another slot, the counterfactual answer = O's locker at that slot; the real generator where the target's tokenizer is
cached), the pair selection from a stored routes run, the energy reads on planted bases, the rules on planted numbers,
the seal, and the run / verdict stages end to end on a tiny fake causal model (x48_das's fixtures). CPU, no real model."""

from __future__ import annotations

import collections
import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import suite_v1 as S
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x48_das as D
from scripts import x49_das_pos as Q

D_MODEL, VOCAB, N_LETTERS = 64, 512, 128
ANIMALS = ["frog", "bee", "cat", "cow", "duck", "fox", "goat", "hen", "owl", "pig", "yak", "ant"]
LEGS = {a: 6 if a in ("bee", "ant") else 2 if a in ("duck", "hen", "owl") else 4 for a in ANIMALS}


# ---- fixtures (copied from tests/test_x48_das.py) -------------------------------------------------------------------


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


# ---- C1 scenes on the word tokenizer (x6_routes' C1 text, encoded as x6_routes.encode lays it out) ------------------


def c1_case(tok: WordTok, idx: int, rng: random.Random) -> dict:
    """One x6_routes C1 scene: A's and C's locker sentences swapped in S, A's number a new digit d; Iris picks A."""
    A, B, C = rng.sample(ANIMALS, 3)
    a, b, c, d = rng.sample(range(1, 10), 4)
    order = rng.sample([A, B, C], 3)
    val = {A: a, B: b, C: c}
    picks = rng.sample([("Iris", A), ("Tom", B), ("Ann", C)], 3)
    o = R.context([(x, val[x]) for x in order], picks)
    sw = {A: C, C: A}
    s = R.context([(sw.get(x, x), d if sw.get(x, x) == A else val[sw.get(x, x)]) for x in order], picks)
    expect = {"identity": a, "position": c, "value": d, "original": a}
    one = lambda v: S.answer_token(tok, str(v), "digit")  # noqa: E731
    readers, pos = {}, None
    for w, q, ans in ((X.LOOKUP, R.LOOKUP_Q, (a, d)), (X.RECALL, R.RECALL_Q, (LEGS[A], LEGS[A]))):
        ids = {}
        for v, ctx in (("org", o), ("alt", s)):
            text = f"{ctx} {q.format(p='Iris')} Answer:"
            enc = tok(text, return_offsets_mapping=True)
            w0 = text.index(f"Iris picked the {A}.") + len("Iris picked the")
            at = [k for k, (st, _) in enumerate(enc.offset_mapping) if st == w0]
            assert len(at) == 1
            pos = at[0] if pos is None else pos
            assert at[0] == pos
            ids[v] = enc.input_ids
        readers[w] = {"question": q.format(p="Iris"), "answer": str(ans[0]), "cf_answer": str(ans[1]), "ids": ids,
                      "tok_A": one(ans[0]), "tok_b": one(ans[1])}  # fmt: skip
    assert pos is not None
    return {"scene": f"C1-{idx:04d}", "condition": "C1", "rendering": "chat", "domain": "animals", "bridge": A,
            "cf_bridge": A, "context": o, "cf_context": s, "pos": pos, "space": [tok.vocab.setdefault(" ", len(tok.vocab))],
            "expect": expect, "route_tokens": {k: one(v) for k, v in expect.items()}, "readers": readers}  # fmt: skip


def c1_cases(tok: WordTok, n: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    return [c1_case(tok, i, rng) for i in range(n)]


# ---- the pairs -------------------------------------------------------------------------------------------------------


def check_pair(p: dict, c: dict) -> None:
    """Same item, its locker sentence moved from slot i to slot j != i, the counterfactual answer O's digit at j."""
    lo, ls = Q.lockers(c["context"]), Q.lockers(c["cf_context"])
    i, j = p["slot_o"], p["slot_s"]
    assert p["entity"] == c["bridge"] == c["cf_bridge"] and i != j
    assert lo[i - 1][0] == ls[j - 1][0] == c["bridge"]  # the same item, moved
    assert ls[j - 1][1] not in [v for _, v in lo]  # a new number in S (the value route)
    assert ls[i - 1] == lo[j - 1]  # swapped with the sentence at slot j
    assert [x for k, x in enumerate(lo) if k not in (i - 1, j - 1)] == [
        x for k, x in enumerate(ls) if k not in (i - 1, j - 1)
    ]
    lk = p["readers"][X.LOOKUP]
    assert lk["cf_answer"] == str(lo[j - 1][1]) and lk["tok_b"] == c["route_tokens"]["position"]  # slot j's locker in O
    assert lk["s_answer"] == str(ls[j - 1][1]) and lk["tok_s"] == c["readers"][X.LOOKUP]["tok_b"]  # S's own: the value
    assert lk["answer"] == str(lo[i - 1][1]) and lk["tok_A"] == c["readers"][X.LOOKUP]["tok_A"]
    rc = p["readers"][X.RECALL]
    assert rc["tok_b"] == rc["tok_A"]  # the recall cannot switch: a move is collateral
    for w in X.READERS:
        org, alt = p["readers"][w]["marked"]["org"], p["readers"][w]["marked"]["alt"]
        assert f"⟦own:The locker of the {c['bridge']} is {lo[i - 1][1]}.⟧" in org
        assert f"⟦target:The locker of the {lo[j - 1][0]} is {lo[j - 1][1]}.⟧" in org
        assert f"⟦moved:The locker of the {c['bridge']} is {ls[j - 1][1]}.⟧" in alt
        assert org.count("⟦bridge:") == 1 and org.split("⟦bridge:")[1].startswith(f" {c['bridge']}")


def test_position_pair_same_item_moved_slot_counterfactual_answer():
    tok = WordTok()
    cases = c1_cases(tok, 40)
    moves = collections.Counter()
    for c in cases:
        p = Q.position_pair(tok, c)
        check_pair(p, c)
        moves[p["move"]] += 1
    assert len(moves) >= 4  # the slots vary (x6_routes shuffles the locker order)


def test_position_pair_refuses_other_conditions():
    tok = WordTok()
    c = c1_cases(tok, 1)[0]
    with pytest.raises(AssertionError, match="same-item"):
        Q.position_pair(tok, {**c, "condition": "C2"})
    with pytest.raises(AssertionError, match="same-item"):
        Q.position_pair(tok, {**c, "cf_bridge": "zebra"})
    with pytest.raises(AssertionError):
        Q.position_pair(tok, {**c, "expect": {**c["expect"], "position": c["expect"]["value"]}})


def test_position_pairs_on_the_target_tokenizer():
    """x6_routes' own generator with the target's tokenizer (skipped where it is not cached): every C1 scene a pair."""
    from scripts import x45m

    try:
        tok = x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    cases = [c for c in R.scenes(tok, 30)[0] if c["condition"] == "C1"]
    assert len(cases) == 30
    for c in cases:
        check_pair(Q.position_pair(tok, c), c)


def stored_run(tmp_path, cases: list[dict], routes: dict[str, str], kept: dict[str, int]):
    """A stored x6_routes run: manifest, cases, the whole arm's outcomes per C1 scene (and a no_jpp arm, ignored)."""
    from bridge_jspace import pins

    src = tmp_path / "x6_routes" / "fake_routes"
    src.mkdir(parents=True)
    m = {"model": {"target": pins.TARGET, "prompt_format": "chat"}, "layer": X.PREDICTED[pins.TARGET], "seed": R.SEED}
    (src / "manifest.json").write_text(json.dumps(m))
    X.write_jsonl(src / "cases.jsonl", cases)
    rows = []
    for c in cases:
        for arm in ("whole", "no_jpp"):
            rows.append({"scene": c["scene"], "condition": "C1", "reader": X.LOOKUP, "arm": arm, "route": routes[c["scene"]],
                         "top": 0, "switched": 0})  # fmt: skip
            rc = c["readers"][X.RECALL]
            rows.append({"scene": c["scene"], "condition": "C1", "reader": X.RECALL, "arm": arm, "route": None,
                         "top": rc["tok_A"] if kept[c["scene"]] else -1, "switched": kept[c["scene"]]})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    return src


def test_select_pairs_keeps_the_position_route_and_splits_by_entity(tmp_path, monkeypatch):
    from bridge_jspace import pins

    tok = WordTok()
    cases = c1_cases(tok, 40)
    routes = {c["scene"]: ("position" if i % 3 else "identity") for i, c in enumerate(cases)}
    kept = {c["scene"]: int(i % 5 != 0) for i, c in enumerate(cases)}
    stored_run(tmp_path, cases, routes, kept)
    monkeypatch.setattr(R, "RESULTS", tmp_path / "x6_routes")
    monkeypatch.setattr(
        R, "scenes", lambda tok_, n, rendering="chat": (json.loads(json.dumps(cases)), collections.Counter())
    )
    pairs, info = Q.select_pairs(tok, "fake_routes", X.PREDICTED[pins.TARGET])
    want = [c["scene"] for c in cases if routes[c["scene"]] == "position"]
    assert [p["scene"] for p in pairs] == want and info["pairs"] == len(want)
    assert info["whole_change_routes"] == dict(collections.Counter(routes.values()))
    assert all(p["stored_recall_kept"] == kept[p["scene"]] for p in pairs)
    by_ent = collections.defaultdict(set)
    for p in pairs:
        by_ent[p["entity"]].add(p["split"])
    assert all(len(s) == 1 for s in by_ent.values())  # an entity in one split
    assert set(info["entities_per_split"]) == {"train", "select", "test"}
    assert sum(info["pairs_per_split"].values()) == len(pairs) and sum(info["moves"].values()) == len(pairs)
    # the stored ids must match the rebuilt ones
    bad = json.loads(json.dumps(cases))
    bad[1]["readers"][X.LOOKUP]["ids"]["org"][0] += 1
    monkeypatch.setattr(R, "scenes", lambda tok_, n, rendering="chat": (bad, collections.Counter()))
    with pytest.raises(AssertionError, match="ids changed"):
        Q.select_pairs(tok, "fake_routes", X.PREDICTED[pins.TARGET])


# ---- the energy reads on planted bases ------------------------------------------------------------------------------


def test_subspace_reads_on_planted_bases():
    eye = torch.eye(16, dtype=torch.float64)
    u, w = eye[:, 0:4], eye[:, 2:7]  # U: e0-e3 (rank 4); W: e2-e6 (rank 5)
    r = Q.subspace_reads(eye[:, 0:2], u, w)  # R = e0, e1: half of U, none of W
    assert r["k"] == 2 and r["cos2_U"] == pytest.approx(0.5) and r["cos2_W"] == pytest.approx(0.0)
    assert r["random_expectation"] == pytest.approx(2 / 16) and r["angles_vs_U"] == [0.0, 0.0]
    assert r["angles_vs_W"] == [90.0, 90.0]
    r = Q.subspace_reads(eye[:, 2:6], u, w)  # R = e2-e5: U's e2, e3; W's e2-e5
    assert r["cos2_U"] == pytest.approx(0.5) and r["cos2_W"] == pytest.approx(0.8)
    r = Q.subspace_reads(eye[:, 0:4], u, w)  # R = U: all of U's energy
    assert r["cos2_U"] == pytest.approx(1.0) and r["cos2_W"] == pytest.approx(0.4)
    rot = (eye[:, 0:1] + eye[:, 10:11]) / 2**0.5  # 45 degrees off U
    assert Q.subspace_reads(rot, u, w)["angles_vs_U"] == [pytest.approx(45.0)]


def test_geometry_with_w_on_planted_vectors():
    d = 64
    eye = torch.eye(d)
    spans = {**D.spans_of(eye, eye, eye[:, 60:64], eye[:, 58:60], torch.arange(100) % d, torch.arange(25) + 30),
             "W": eye[:, 50:55].double()}  # fmt: skip
    delta = eye[0] + eye[52] + eye[61]  # J++-25, W (and W_E-25), U
    g = D.geometry_row(delta, eye[:, 52:53], spans)  # R = e52: inside W only (and W_E's span)
    assert g["energy"] == pytest.approx(1 / 3) and g["in_W"] == pytest.approx(1.0) and g["in_U"] == pytest.approx(0.0)
    g = D.geometry_row(delta, eye[:, 61:62], spans)
    assert g["in_W"] == pytest.approx(0.0) and g["in_U"] == pytest.approx(1.0) and g["in_jpp25"] == pytest.approx(0.0)


# ---- the rules on planted numbers ---------------------------------------------------------------------------------


def planted(own: float, u_e: float, cross: float, w_e: float = 0.3, energy: float = 0.3, k: int = 4) -> dict:
    return {"test": {"own_iia": {k: [own, own - 0.1, own + 0.1]}, "recall_cross": {k: [cross, 0, cross + 0.1]}},
            "geometry": {f"R_pos_k{k}": {"cos2_U": u_e, "cos2_W": w_e, "random_expectation": k / 4096,
                                         "energy": [energy, 0, 1]},
                         f"rand_k{k}": {"cos2_U": 0.001, "cos2_W": 0.001, "random_expectation": k / 4096,
                                        "energy": [0.001, 0, 0.01]}}}  # fmt: skip


@pytest.mark.parametrize(
    ("own", "u_e", "cross", "label"),
    [
        (0.8, 0.7, 0.05, "ours"),
        (0.6, 0.6, 0.1, "ours"),  # the bars are inclusive
        (0.8, 0.7, 0.15, "in_between"),  # the recall moves too much
        (0.8, 0.5, 0.05, "in_between"),  # U's energy between 0.2 and 0.6
        (0.8, 0.2, 0.05, "two_codes"),
        (0.8, 0.05, 0.4, "two_codes"),  # two codes does not read the recall
        (0.59, 0.9, 0.0, "no_mediator"),
        (0.2, 0.0, 0.0, "no_mediator"),
    ],
)
def test_rules_on_planted_numbers(own, u_e, cross, label):
    v = Q.rules(planted(own, u_e, cross))
    assert v["label"] == label and v["text"] == Q.LABELS[label]
    assert sum(v[x] for x in ("ours", "two_codes", "no_mediator", "in_between")) == 1  # exactly one label
    assert v["detail"]["own_iia"] == own and v["detail"]["U_energy_in_R"] == u_e


def test_rules_flag_a_not_selective_r():
    v = Q.rules(planted(0.8, 0.7, 0.05, energy=0.85))
    assert v["label"] == "ours" and v["not_selective"] == ["R_pos_k4"]


# ---- the seal -------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_q49_8_only(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = (
        "**Q49.7** x\n\nDan: (a) 70%\n\n**Q49.8** DAS for the address (9B, k = 4).\n- (a) ...\n- (b) ...\n\nDan:{}\n"
    )
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert Q.dan_answer() == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" (b) 60%")))
    assert Q.dan_answer() == "(b) 60%"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("\nDan (9B): (a) 55%\n- why: U is the address")))
    assert "Dan (9B): (a) 55%" in Q.dan_answer() and "U is the address" in Q.dan_answer()
    monkeypatch.setattr(D.subprocess, "run", fake_git("**Q49.7** x\n\nDan: (a)\n"))
    assert Q.dan_answer() == ""


# ---- the run and verdict stages on the fake model -------------------------------------------------------------------


@pytest.fixture
def fake_env(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    cases = c1_cases(tok, 36)
    pairs = []
    for i, c in enumerate(cases):
        p = Q.position_pair(tok, c)
        p["stored_route"], p["stored_recall_kept"] = "position", int(i % 4 != 0)
        pairs.append(p)
    info = {"routes_run": "fake_routes", **Q.split_info(pairs)}
    fake = FakeModel(tok)
    u = D.random_basis(D_MODEL, 4, 11).numpy()
    w = D.random_basis(D_MODEL, 5, 12).numpy().astype(np.float64)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Q, "select_pairs", lambda *_: (pairs, info))
    monkeypatch.setattr(D, "pointer_basis", lambda _t: (u, {"states_run": "fake", "rank": 4}))
    monkeypatch.setattr(Q, "load_w", lambda _t, _l: (w, {"run": "fake_47_2", "rank": 5}))
    monkeypatch.setattr(D, "K_JPP", (25, 30))
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x49_das_pos")
    monkeypatch.setattr(Q, "ROUTES_RUN", {pins.TARGET: "fake_routes"})
    monkeypatch.setattr(Q, "W_RUN", {pins.TARGET: "fake_47_2"})
    monkeypatch.setattr(R, "RESULTS", tmp_path / "x6_routes")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Q, "SPEC", tmp_path / "batch49.yaml")
    Q.SPEC.write_text("")
    src = tmp_path / "x6_routes" / "fake_routes"
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    return SimpleNamespace(tok=tok, pairs=pairs, fake=fake, u=u, w=w, prefix=pins.RUN_PREFIX)


def test_run_stage_end_to_end_on_the_fake_model(fake_env):
    from bridge_jspace import pins
    from scripts.exp04_brew_parts import AddRows

    pairs, la = fake_env.pairs, X.PREDICTED[pins.TARGET]
    out = Q.stage_run(f"{fake_env.prefix}fake_49", "test", steps=3, ks=(2, 4))
    assert not any(p.name.startswith("verdict") for p in out.iterdir())  # sealed
    m = json.loads((out / "manifest.json").read_text())
    assert m["ks"] == [2, 4] and m["k_rule"] == 4 and "sealed" in m and m["switches"]["target"] == pins.TARGET
    arms = Q.arm_names((2, 4))
    assert arms == ["none", "whole", "R_pos_k2", "rand_k2", "shuf_pos_k2", "R_pos_k4", "rand_k4", "shuf_pos_k4"]
    rows = X.read_jsonl(out / "outcomes.jsonl")
    held = [p for p in pairs if p["split"] != "train"]
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {(p["scene"], w, a) for p in held for w in X.READERS
                                                                   for a in arms}  # fmt: skip
    by_scene = {p["scene"]: p for p in pairs}
    for r in rows:
        rd = by_scene[r["scene"]]["readers"][r["reader"]]
        assert r["moved"] == int(r["top"] != rd["tok_A"])
        if r["reader"] == X.LOOKUP:  # the switch is the position answer; the route classified
            assert r["switched"] == int(r["top"] == by_scene[r["scene"]]["route_tokens"]["position"])
            assert r["route"] in Q.ROUTES_NAMES_ALL and (r["route"] == "position") == bool(r["switched"])
        else:
            assert r["route"] is None
    blob = torch.load(out / "R.pt")
    assert set(blob["R"]) == set(arms) - {"none", "whole"}
    for key, r in blob["R"].items():
        k = int(key.rsplit("k", 1)[1])
        assert r.shape == (D_MODEL, k) and torch.allclose(r.T @ r, torch.eye(k), atol=1e-4)
    assert np.allclose(blob["U"].numpy(), fake_env.u) and np.allclose(blob["W"].numpy(), fake_env.w)
    assert blob["U_fit"].shape[1] == len({p["slot_o"] for p in pairs if p["split"] == "train"}) - 1
    geo = X.read_jsonl(out / "geometry.jsonl")
    assert len(geo) == len(pairs) * len(blob["R"])
    for g in geo:
        assert 0 <= g["in_W"] <= 1 + 1e-6 and 0 <= g["energy"] <= 1 + 1e-6 and g["in_jpp25"] <= g["in_jpp100"] + 1e-6
    ro = json.loads((out / "readouts.json").read_text())
    assert ro["rank_U"] == 4 and ro["rank_W"] == 5 and len(ro["U_vs_W"]["angles"]) == 4
    assert ro["rand_k4"]["random_expectation"] == pytest.approx(4 / D_MODEL)
    assert ro["R_pos_k4"]["cos2_U"] == pytest.approx(Q.subspace_reads(blob["R"]["R_pos_k4"], torch.tensor(fake_env.u),
                                                                      torch.tensor(fake_env.w))["cos2_U"], abs=1e-5)  # fmt: skip
    train = X.read_jsonl(out / "train.jsonl")
    assert {t["R"] for t in train} == {k for k in blob["R"] if not k.startswith("rand")}
    # the state cache and one read: R R^T Delta added at the bridge position of the O prompt
    st = torch.load(out / f"states_L{la}.pt")
    p0 = next(p for p in pairs if p["split"] == "test")
    i0 = [p["scene"] for p in pairs].index(p0["scene"])
    ids = p0["readers"][X.LOOKUP]["ids"]
    h = {v: fake_env.fake.run(torch.tensor([ids[v]]), record=(la,))[1][la][p0["pos"]] for v in ("org", "alt")}
    assert torch.allclose(st["delta"][i0], h["alt"] - h["org"], atol=1e-5)
    r4 = blob["R"]["R_pos_k4"]
    part = (st["delta"][i0 : i0 + 1] @ r4) @ r4.T
    lg = fake_env.fake.generate_batch(torch.tensor([ids["org"] + p0["space"]]), 1, [{la: AddRows(part, [p0["pos"]])}],
                                      first_logits=True)[1]  # fmt: skip
    rec = next(r for r in rows if r["scene"] == p0["scene"] and r["reader"] == X.LOOKUP and r["arm"] == "R_pos_k4")
    assert rec["top"] == int(lg[0].argmax())


def test_verdict_is_sealed_until_dans_answer(fake_env, monkeypatch):
    out = Q.stage_run(f"{fake_env.prefix}fake_49s", "test", steps=1, ks=(2, 4))
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_verdict([out.name], n_boot=50)
    assert not any(p.name.startswith("verdict") for p in Q.RESULTS.iterdir())


def test_verdict_on_the_fake_run(fake_env, monkeypatch):
    out = Q.stage_run(f"{fake_env.prefix}fake_49v", "test", steps=1, ks=(2, 4))
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "(c) 50%")
    v_out = Q.stage_verdict([out.name], n_boot=50)
    blob = json.loads((v_out / "verdict.json").read_text())
    mdl = blob["models"][0]
    test_pairs = [p for p in fake_env.pairs if p["split"] == "test"]
    assert blob["dan"] == "(c) 50%" and mdl["test"]["n"] == len(test_pairs)
    assert mdl["rules"]["label"] in Q.LABELS and mdl["rules"]["k"] == 4
    rows = [r for r in X.read_jsonl(out / "outcomes.jsonl") if r["split"] == "test"]
    own = np.mean([r["switched"] for r in rows if r["reader"] == X.LOOKUP and r["arm"] == "R_pos_k4"])
    cross = np.mean([r["moved"] for r in rows if r["reader"] == X.RECALL and r["arm"] == "R_pos_k4"])
    assert mdl["rules"]["detail"]["own_iia"] == pytest.approx(own)  # recomputed from the raw rows
    assert mdl["rules"]["detail"]["recall_cross_iia"] == pytest.approx(cross)
    md = (v_out / "verdict.md").read_text()
    assert "As computed" in md and "U vs W" in md and (v_out / f"{out.name}.png").exists()
    ex = (v_out / "examples.md").read_text()
    assert ex.count("### ") == min(10, len(test_pairs)) and "⟦bridge:" in ex and "⟦moved:" in ex
