"""Batch 47, test 47.5 (scripts/x47_zero.py): the projection edit, the per-layer parts on synthetic tensors, the arms
end to end on a tiny fake causal model (CPU), the sealed verdict, the rule at its bars and the README verb over the
models, and the verify-pack view on planted runs. No real model."""

import json
import re
import sys
from types import SimpleNamespace

import pytest
import torch

from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_atoms as A
from scripts import x47_zero as Z

LK, RC = X.LOOKUP, X.RECALL
L = X.PREDICTED["qwen3.6-27b"]  # the default target's layer (32): the fake model has blocks past L + 3


def _proj(q: torch.Tensor) -> torch.Tensor:
    return q.double() @ q.double().T


# ---- the edit and the parts ----------------------------------------------------------------------------------------


def test_project_out_removes_the_span_at_its_positions_only():
    g = torch.Generator().manual_seed(0)
    h = torch.randn(5, 16, generator=g)
    q, _ = torch.linalg.qr(torch.randn(16, 3, generator=g))
    e = Z.ProjectOut(q, [1, 3])
    out = e(h)
    assert torch.allclose(out[[0, 2, 4]], h[[0, 2, 4]])
    assert torch.allclose(out[[1, 3]] @ q, torch.zeros(2, 3), atol=1e-5)  # nothing left in the span
    assert torch.allclose(out[[1, 3]], h[[1, 3]] - (h[[1, 3]] @ q) @ q.T)
    assert torch.allclose(e(out), out, atol=1e-6)  # a projection: twice is once
    assert torch.equal(Z.ProjectOut(q[:, :0], [1])(h), h)  # k = 0 random columns: no edit


def test_layer_parts_atoms_and_random_share():
    g = torch.Generator().manual_seed(1)
    d, n = 48, 6
    jdic = torch.nn.functional.normalize(torch.randn(120, d, generator=g), dim=-1)
    h_o, h_s = torch.randn(n, d, generator=g), torch.randn(n, d, generator=g)
    basis = SP.random_basis(d, torch.Generator().manual_seed(7))
    q, ks, recs = Z.layer_parts(jdic, h_s, h_o, basis)
    fit = X.fit(jdic, h_s - h_o, 25, "signed")  # X0's J++ part of Δ: in the atoms' span
    for i in range(n):
        assert q[i].shape == (d, 25) and torch.allclose(q[i].T @ q[i], torch.eye(25), atol=1e-5)
        assert torch.allclose((_proj(q[i]) @ fit[i].double()).float(), fit[i], atol=1e-4)
        hs = h_s[i].double()
        assert recs[i]["share_hS_atoms"] == pytest.approx(
            float((_proj(q[i]) @ hs).norm() ** 2 / hs.norm() ** 2), abs=1e-5
        )
        assert recs[i]["share_delta_atoms"] == pytest.approx(
            float(fit[i].norm() ** 2 / (h_s[i] - h_o[i]).norm() ** 2), abs=1e-4
        )
        assert recs[i]["k_rand"] == ks[i] and recs[i]["atoms_rank"] == 25
        one = float(((hs.float() @ basis) ** 2).max() / hs.norm() ** 2)  # the random share is matched to one direction
        assert abs(recs[i]["share_hS_rand"] - recs[i]["share_hS_atoms"]) <= one + 1e-6
        want = SP.random_subspace_part(h_s[i : i + 1], torch.tensor([recs[i]["share_hS_atoms"]]), basis)[0]
        assert torch.allclose(_proj(basis[:, : ks[i]]).float() @ h_s[i], want, atol=1e-4)  # X0's rand_sub rule


def test_edit_sets_place_each_arm():
    q = {la: torch.eye(8)[:, [la % 8]] for la in range(L, L + 4)}
    bases = {la: torch.eye(8) for la in range(L, L + 4)}
    ks = {la: 2 + la - L for la in range(L, L + 4)}
    e = Z.edit_sets(tuple(range(L, L + 4)), 5, q, bases, ks)
    assert tuple(e) == Z.ARMS and e["none"] == {}
    assert set(e["zero_L"]) == set(e["rand_L"]) == {L} and set(e["zero_L3"]) == set(e["rand_L3"]) == set(
        range(L, L + 4)
    )
    assert e["zero_L"][L].positions == [5] and torch.equal(e["zero_L3"][L + 2].basis, q[L + 2])
    assert e["rand_L3"][L + 3].basis.shape == (8, 5) and e["rand_L"][L].basis.shape == (8, 2)


# ---- the arms end to end on a fake model ---------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (after tests/test_x45p.py): each block mixes the running mean
    of the positions so far into every position; an edit acts on a block's output, as Model's hooks do."""

    def __init__(self, n_layers: int = L + 6, d: int = 48, vocab: int = 128):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.n_layers, self.device = n_layers, torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()
        self.tokenizer = SimpleNamespace(name="fake")
        self.calls: list[tuple[int, list[dict]]] = []

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
        self.calls.append((ids.shape[1], edits))
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [f" t{int(lg.argmax())}" for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return torch.arange(100)


class FakeLens:
    source_layers = tuple(range(L + 6))

    def __init__(self, model=None, name="jpp"):
        assert name == "jpp"

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), 48, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def _item(i: int) -> dict:
    """An X0-like case: both readers' prompts agree through the bridge word (position 4), S changes only it."""
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    rd = {"id": f"PP-{i}", "question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
          "ids": {"org": [*org, 7], "alt": [*alt, 7]}, "tok_A": 5, "tok_b": 3}  # fmt: skip
    rc = {**rd, "id": f"PM-{i}", "question": "How many legs?", "ids": {"org": [*org, 8, 9], "alt": [*alt, 8, 9]}}
    return {"scene": f"P2-{i:04d}", "bridge": f"e{i % 4}", "cf_bridge": "bee", "domain": "animals", "pos": 4,
            "rendering": "chat", "space": [11], "readers": {LK: rd, RC: rc}}  # fmt: skip


@pytest.fixture
def fake_items():
    model = FakeModel()
    items = [_item(i) for i in range(12)]
    layers = tuple(range(L, L + Z.SPAN))
    ws = X.whitespace_mask(model)
    rows, norms, greedy = Z.run_items(model, FakeLens(), items, layers, ws, torch.arange(10))
    return SimpleNamespace(model=model, items=items, layers=layers, rows=rows, norms=norms, greedy=greedy)


def test_run_items_reads_every_arm_on_s(fake_items):
    f = fake_items
    assert {(r["scene"], r["reader"], r["arm"]) for r in f.rows} == {
        (c["scene"], w, a) for c in f.items for w in X.READERS for a in Z.ARMS
    }
    assert len(f.rows) == len(f.items) * 2 * len(Z.ARMS)
    assert all(r["kept"] == int(r["top"] == 3) and r["to_org"] == int(r["top"] == 5) for r in f.rows)
    assert len(f.greedy) == X.K_EXAMPLES * 2 * len(Z.ARMS)
    assert [len(n["layers"]) for n in f.norms] == [Z.SPAN] * len(f.items)
    # the first read is the lookup's S prompt with the digit's space token appended, under the five arms
    seq, edits = f.model.calls[0]
    assert seq == len(f.items[0]["readers"][LK]["ids"]["alt"]) + 1 and len(edits) == len(Z.ARMS) and edits[0] == {}


def test_the_zeroing_takes_the_atoms_span_out_of_s_at_each_layer(fake_items):
    f = fake_items
    c = f.items[0]
    ids = torch.tensor([c["readers"][LK]["ids"]["alt"]])
    edits = dict(zip(Z.ARMS, f.model.calls[0][1], strict=True))
    clean = f.model.run(ids, record=f.layers)[1]
    o = f.model.run(torch.tensor([c["readers"][LK]["ids"]["org"]]), record=f.layers)[1]
    lens = FakeLens()
    for la in f.layers:  # each layer's basis: Δ_l's 25 OMP atoms over that layer's lens
        q, _ = Z.atom_bases(lens.vectors(la, torch.arange(100)), (clean[la][4] - o[la][4])[None])
        assert torch.allclose(_proj(edits["zero_L3"][la].basis), _proj(q[0]), atol=1e-5)
    # zero_L: at L, S's state minus its projection; every other position as clean
    q_l = edits["zero_L"][L].basis
    st = f.model.run(ids, edits=edits["zero_L"], record=(L,))[1][L]
    assert torch.allclose(st[4], clean[L][4] - (clean[L][4] @ q_l) @ q_l.T, atol=1e-5)
    keep = [p for p in range(ids.shape[1]) if p != 4]
    assert torch.allclose(st[keep], clean[L][keep])
    # zero_L3: at every layer the state as it arrives has nothing left in that layer's span
    st3 = f.model.run(ids, edits=edits["zero_L3"], record=f.layers)[1]
    for la in f.layers:
        assert float((st3[la][4] @ edits["zero_L3"][la].basis).norm()) < 1e-4
    # the random arm at L: the first k columns of X0's random basis (seed 888 + L), at the atoms' share of ||h_S||^2
    basis = SP.random_basis(48, torch.Generator().manual_seed(X.SUBSPACE_SEED + L))
    k = f.norms[0]["layers"][0]["k_rand"]
    assert torch.allclose(_proj(edits["rand_L"][L].basis), _proj(basis[:, :k]), atol=1e-5)


def _stage_patches(monkeypatch, tmp_path, items):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M

    fake = FakeModel()
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", FakeLens)
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x47_zero")
    monkeypatch.setattr(X, "build_cases", lambda tok, s: (items, {"scenes": len(items)}))
    monkeypatch.setattr(X, "competence", lambda *a: [])
    gate = {"chat": {"pass": bool(items), "eligible": len(items)}}
    monkeypatch.setattr(X, "gate_and_eligible", lambda cases, comp: (gate, {"chat": items}))
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    return fake


def test_stage_run_end_to_end_sealed(tmp_path, monkeypatch):
    items = [_item(i) for i in range(12)]
    _stage_patches(monkeypatch, tmp_path, items)
    renderings = X.RENDERINGS
    out = Z.stage_run("x47_test_zero", "test")
    assert renderings == X.RENDERINGS  # X0's settings restored
    m = json.loads((out / "manifest.json").read_text())
    assert m["layers"] == list(range(L, L + 4)) and m["k"] == 25 and "sealed" in m and m["test"] == "47.5"
    assert len(X.read_jsonl(out / "outcomes.jsonl")) == 12 * 2 * len(Z.ARMS)
    assert json.loads((out / "gate.json").read_text())["order"] == [c["scene"] for c in items]
    assert sorted(p.name for p in out.iterdir()) == ["cases.jsonl", "competence.jsonl", "examples_greedy.jsonl",
                                                     "gate.json", "manifest.json", "norms.jsonl", "outcomes.jsonl"]  # fmt: skip


def test_stage_run_without_eligible_items_writes_no_outcomes(tmp_path, monkeypatch):
    _stage_patches(monkeypatch, tmp_path, [])
    out = Z.stage_run("x47_test_gate", "test")
    assert not (out / "outcomes.jsonl").exists() and (out / "gate.json").exists()


def test_stage_run_needs_the_lens_at_l_to_l_plus_3(tmp_path, monkeypatch):
    _stage_patches(monkeypatch, tmp_path, [_item(0)])
    monkeypatch.setattr(FakeLens, "source_layers", tuple(range(L + 2)))
    with pytest.raises(AssertionError, match="no map at layers"):
        Z.stage_run("x47_test_lens", "test")


# ---- the rule ------------------------------------------------------------------------------------------------------

N = 100


def _rows(kept: dict[str, dict[str, int]], n: int = N) -> list[dict]:
    """Planted rows: under each arm the reader keeps S's answer on its first kept[reader][arm] items (none: all)."""
    rows = []
    for i in range(n):
        for w in X.READERS:
            for a in Z.ARMS:
                k = kept.get(w, {}).get(a, n)
                rows.append({"scene": f"P2-{i:04d}", "entity": f"e{i % 20}", "reader": w, "arm": a, "kept": int(i < k),
                             "top": 3 if i < k else 5})  # fmt: skip
    return rows


def _lab(zero: int, rand: int, pair: str = "L", reader: str = RC) -> str:
    arms = {"L": ("zero_L", "rand_L"), "L..L+3": ("zero_L3", "rand_L3")}[pair]
    rows = _rows({reader: dict(zip(arms, (zero, rand), strict=True))})
    return Z.label(Z.numbers(rows, reader, 200), pair)


@pytest.mark.parametrize(
    ("zero", "rand", "want"),
    [
        (80, 90, Z.FOLLOWED),  # both bars exactly met
        (95, 100, Z.FOLLOWED),
        (80, 91, Z.NEITHER),  # 0.11 below random
        (79, 85, Z.NEITHER),  # keeps less than 0.80
        (65, 95, Z.NEEDS),  # 0.30 beyond random, exactly
        (10, 90, Z.NEEDS),
        (66, 95, Z.NEITHER),
        (95, 80, Z.NEITHER),  # keeps 0.15 more than random: not "within 0.10"
    ],
)
def test_label_at_the_bars(zero, rand, want):
    assert _lab(zero, rand) == want


def test_numbers_read_planted_shares_and_pairs():
    nums = Z.numbers(_rows({RC: {"zero_L": 70, "rand_L": 95, "zero_L3": 40, "rand_L3": 90}}), RC, 300)
    assert nums["n"] == N and nums["entities"] == 20 and nums["kept"]["none"][0] == 1.0
    assert nums["beyond_random"]["L"][0] == pytest.approx(0.25) and nums["beyond_random"]["L..L+3"][0] == pytest.approx(
        0.5
    )
    lo, hi = nums["beyond_random"]["L"][1:]
    assert lo <= 0.25 <= hi
    with pytest.raises(AssertionError, match="reads missing"):
        Z.numbers([r for r in _rows({}) if r["arm"] != "rand_L3"], RC, 10)


def test_the_readme_verb_needs_needed_on_all_three():
    def m(label, status="tested"):
        return {"target": f"{label}-{status}", "label": label, "status": status}

    assert Z.batch_verb([m(Z.NEEDS), m(Z.NEEDS), m(Z.NEEDS)])["verb"] == "needs"
    assert Z.batch_verb([m(Z.NEEDS), m(Z.FOLLOWED), m(Z.NEEDS)])["verb"] == "follows / reads"
    assert Z.batch_verb([m(Z.NEEDS), m(Z.NEITHER), m(Z.NEEDS)])["verb"] == "follows / reads"
    assert Z.batch_verb([m(Z.NEEDS), m("pending", "pending"), m(Z.NEEDS)])["verb"] == "pending"
    assert Z.batch_verb([m(Z.FOLLOWED), m("pending", "pending"), m(Z.NEEDS)])["verb"] == "follows / reads"
    assert Z.batch_verb([m(Z.NEEDS), m("not tested", "not tested"), m(Z.NEEDS)])["verb"] == "follows / reads"


# ---- the verdict on planted runs -----------------------------------------------------------------------------------


def _write(path, manifest, **files):
    path.mkdir(parents=True)
    (path / "manifest.json").write_text(json.dumps(manifest))
    for fname, data in files.items():
        (path / fname).write_text(
            json.dumps(data) if isinstance(data, dict) else "".join(json.dumps(r) + "\n" for r in data)
        )


def _planted(tmp_path, monkeypatch, kept: dict[str, dict], skip=()):
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x47_zero")
    layers = {"qwen3.5-9b": 12, "qwen3.6-27b": 32, "muse-glimmer-30b": 26}
    for t in Z.MODELS:
        if t in skip:
            continue
        la = layers[t]
        norms = [{"scene": f"P2-{i:04d}", "entity": f"e{i % 20}",
                  "layers": [{"layer": la + j, "norm_hS": 50.0, "norm_delta": 9.0, "share_hS_atoms": 0.02,
                              "share_delta_atoms": 0.12, "share_hS_rand": 0.021, "k_rand": 90, "atoms_rank": 25}
                             for j in range(4)]} for i in range(N)]  # fmt: skip
        _write(tmp_path / "x47_zero" / Z.RUNS[t], {"model": {"target": t}, "layer": la, "layers": [la + j for j in range(4)]},
               **{"outcomes.jsonl": _rows({RC: kept[t]}), "norms.jsonl": norms,
                  "cases.jsonl": [{**_item(i), "scene": f"P2-{i:04d}"} for i in range(N)],
                  "examples_greedy.jsonl": [{"scene": "P2-0006", "reader": RC, "arm": "zero_L", "greedy": " 5 legs"}],
                  "gate.json": {"gate": {"chat": {"pass": True}}}})  # fmt: skip


def test_verdict_is_sealed_until_dans_answer(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, {t: {} for t in Z.MODELS})
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "")
    with pytest.raises(SystemExit, match="sealed"):
        Z.stage_verdict(n_boot=100, decode_for=lambda t: str)
    assert sorted(p.name for p in (tmp_path / "x47_zero").iterdir()) == sorted(Z.RUNS.values())


def test_verdict_asks_for_q47_5(monkeypatch):
    asked = []
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: asked.append(q) or "")
    with pytest.raises(SystemExit):
        Z.stage_verdict(n_boot=10)
    assert asked == ["Q47.5"]


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    kept = {"qwen3.5-9b": {"zero_L": 60, "rand_L": 95}, "qwen3.6-27b": {"zero_L": 90, "rand_L": 95},
            "muse-glimmer-30b": {"zero_L": 50, "rand_L": 90}}  # fmt: skip
    _planted(tmp_path, monkeypatch, kept)
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "9B needed 60%")

    def decode_for(target):
        return lambda ids: "".join(f"<{int(t)}>" for t in ids)

    out = Z.stage_verdict(n_boot=200, decode_for=decode_for)
    blob = json.loads((out / "x47_5.json").read_text())
    assert blob["dan"] == "9B needed 60%" and out.parent == Z.RESULTS
    assert blob["batch"]["per_model"] == {"qwen3.5-9b": Z.NEEDS, "qwen3.6-27b": Z.FOLLOWED, "muse-glimmer-30b": Z.NEEDS}
    assert blob["batch"]["verb"] == "follows / reads"
    model = blob["models"][0]
    assert model["labels"]["lookup L"] == Z.FOLLOWED and model["shares_median"]["12"]["k_rand"] == 90
    md = (out / "x47_5.md").read_text()
    assert "**The README's verb: follows / reads**" in md
    ex = (out / "examples.md").read_text()
    assert ex.count("### ") == 3 * X.K_EXAMPLES
    assert re.search(r"<\d><2><3><4>⟦<4\d>⟧<6><7>", ex)  # S's prompt (its bridge token 40-44), the bridge marked
    assert "' 5 legs'" in ex or "P2-0006" not in ex


def test_verdict_with_a_missing_or_untested_model(tmp_path, monkeypatch):
    n = iter(range(1000))
    monkeypatch.setattr(Z.time, "strftime", lambda fmt, t=None: f"t{next(n):03d}")  # two verdicts in one second
    _planted(tmp_path, monkeypatch, {t: {"zero_L": 10, "rand_L": 90} for t in Z.MODELS}, skip=("muse-glimmer-30b",))
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "x")
    blob = json.loads((Z.stage_verdict(n_boot=100, decode_for=lambda t: str) / "x47_5.json").read_text())
    assert [m["status"] for m in blob["models"]] == ["tested", "tested", "pending"] and blob["batch"][
        "verb"
    ] == "pending"
    (tmp_path / "x47_zero" / Z.RUNS["qwen3.6-27b"] / "outcomes.jsonl").write_text("")  # the gate failed: no outcomes
    blob = json.loads((Z.stage_verdict(n_boot=100, decode_for=lambda t: str) / "x47_5.json").read_text())
    assert blob["models"][1]["status"] == "not tested" and blob["batch"]["verb"] == "follows / reads"


def test_atom_bases_match_x0s_picks():
    g = torch.Generator().manual_seed(4)
    jdic = torch.nn.functional.normalize(torch.randn(90, 40, generator=g), dim=-1)
    delta = torch.randn(3, 40, generator=g)
    q, atoms = Z.atom_bases(jdic, delta)
    for i in range(3):
        assert torch.allclose(_proj(q[i]), _proj(R.orthonormal(jdic[atoms[i]].T)), atol=1e-6)
        # X0's no_part arm removes exactly this projection of Δ
        assert torch.allclose((_proj(q[i]) @ delta[i].double()).float(), X.fit(jdic, delta, 25, "signed")[i], atol=1e-4)


@pytest.mark.parametrize(("flags", "want"), [([], None), (["--runs", "a", "b", "c"], ["a", "b", "c"])])
def test_main_passes_the_verdicts_runs(monkeypatch, flags, want):
    seen = {}
    monkeypatch.setattr(Z, "stage_verdict", lambda runs=None, n_boot=0, coverage=False: seen.setdefault("runs", runs))
    monkeypatch.setattr(sys, "argv", ["x47_zero.py", "verdict", *flags])
    Z.main()
    assert seen["runs"] == (None if want is None else dict(zip(Z.MODELS, want, strict=True)))


def test_lightning_coverage_verdict_and_exclude_dev(tmp_path, monkeypatch):
    """Batch 52 C: 47.5 on Lightning reads its coverage run alone with no prediction (x52_zero-<UTC>/), and
    --exclude-dev fills x0_necessity.EXCLUDE with the layer prerequisite's 60 dev scenes."""
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    out = Z.stage_verdict(None, 10, coverage=True)
    text = (out / "x47_5.md").read_text()
    assert out.name.startswith("x52_zero-") and Z.NO_PREDICTION in text and ", Dan:" not in text
    assert "nem35l_x52_zero" in text and "qwen3.5-9b" not in text
    seen = []
    monkeypatch.setattr(X, "EXCLUDE", set())
    monkeypatch.setattr(Z, "stage_verdict", lambda runs, n_boot, coverage=False: seen.append(coverage))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x47_zero.py",
            "verdict",
            "--coverage",
            "--exclude-dev",
            "results/x51_lightning/nem35l_x52_layer_r2/gate.json",
        ],
    )
    Z.main()
    assert seen == [True] and len(X.EXCLUDE) == 60
