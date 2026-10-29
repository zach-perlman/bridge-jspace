"""review_states (the J-space inspector's states job, jobs/c3/batch53.yaml inspector_1145 item 1) on the CPU: the token
roles of the planted sample's items, and the GPU stage end to end on a fake model (deterministic states, a random lens),
so a box run cannot die on shapes, indexing or paths. Needs the pinned tokenizer.json in the local HF cache."""

from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from bridge_jspace import pins
from bridge_jspace.review import items as I
from scripts import review_states as RS

MODEL = pins.TARGET  # the tests' process target (BJ_TARGET unset: qwen3.6-27b)


def have_tokenizer(model: str) -> bool:
    try:
        RS.hf_tokenizer(model)
        return True
    except Exception:
        return False


needs_tok = pytest.mark.skipif(not have_tokenizer(MODEL), reason="the pinned tokenizer.json is not in the HF cache")


def dec(tok, ids) -> str:
    return str(tok.decode(list(ids)))


@needs_tok
@pytest.mark.parametrize("view_id", ["main_swap", "routes", "x8_writes"])
def test_roles_mark_the_bridge_the_question_and_the_last_token(view_id):
    tok = RS.hf_tokenizer(MODEL)
    for it in I.items(view_id, MODEL)[:5]:
        lay = RS.layout(tok, it)
        rd = it["case"]["readers"][it["reader"]]
        for v in ("O", "S"):
            ids, roles = lay[f"ids_{v}"], lay[f"roles_{v}"]
            assert "bridge" in roles[str(lay["pos"])]
            assert roles[str(len(ids) - 1)] == ["last"] and ids[-1:] == RS.space_suffix(tok)
            q = [int(p) for p, r in roles.items() if "question" in r]
            assert dec(tok, [ids[p] for p in q]).strip() == rd["question"]
            names = {r.split(": ", 1)[1] for rs in roles.values() for r in rs if r.startswith("mention: ")}
            assert len(names) == 3, names  # the three locker sentences' items
        assert lay["pairs"] == [(i, i) for i in range(len(lay["pos_O"]))]  # same token count: every position pairs
        assert dec(tok, [lay["ids_O"][lay["pos"]]]).strip() == it["case"]["bridge"]
        assert dec(tok, [lay["ids_S"][lay["pos"]]]).strip() == it["case"]["cf_bridge"]


@needs_tok
def test_rank_tokens_are_the_bridge_words_and_the_answers():
    tok = RS.hf_tokenizer(MODEL)
    toks = RS.variant_tokens(tok, "carbon", "elements")
    words = {dec(tok, [t]) for t in toks["word"]}
    assert {" carbon", " Carbon", " C"} <= words and set(toks["word"]) <= set(toks["pieces"])
    assert " He" not in {dec(tok, [t]) for t in RS.variant_tokens(tok, "helium", "elements")["word"]}  # the pronoun
    ans = RS.answer_tokens(tok, "6", None)
    assert "6" in {dec(tok, [t]) for t in ans["digit"]} and " six" in {dec(tok, [t]) for t in ans["word"]}


# ---- the GPU stage on a fake model -----------------------------------------------------------------------------------

D, N_LETTERS = 32, 3000


class FakeNorm(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.zeros(D))
        self.eps = 1e-6


class FakeModel:
    """Block outputs that depend on every earlier token (a cumulative sum of embeddings, scaled per layer)."""

    def __init__(self, vocab: int):
        g = torch.Generator().manual_seed(0)
        self.emb = torch.randn(vocab, D, generator=g)
        self.hf = SimpleNamespace(lm_head=SimpleNamespace(weight=torch.randn(vocab, D, generator=g)),
                                  config=SimpleNamespace(get_text_config=lambda: SimpleNamespace()))  # fmt: skip
        self.final_norm = FakeNorm()
        self.device = torch.device("cpu")
        self.special_ids = frozenset()
        self.decoded = ["x"] * vocab

    def states(self, ids):
        w = 1 + 0.03 * torch.arange(ids.shape[-1], dtype=torch.float32)[:, None]  # order matters (two picks swap)
        return (self.emb[ids] * w).cumsum(0) / w.sqrt()

    def run(self, ids, record=()):
        cum = self.states(ids[0])
        return None, {la: cum * (1 + 0.05 * la) + 0.01 * la for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False):
        """The last state plus whatever each row's edits add (an edit at any layer reaches the read)."""
        rows = []
        for r, row_edits in enumerate(edits):
            h = self.states(ids[r if ids.shape[0] == len(edits) else 0])
            for e in row_edits.values():
                h = e(h)
            rows.append(self.unembed(h[-1:] + h[e.positions[0]][None] if row_edits else h[-1:])[0])
        return ["" for _ in edits], torch.stack(rows)

    def letter_token_ids(self):
        return torch.arange(1000, 1000 + N_LETTERS)

    def unembed(self, h):
        return h.float() @ self.hf.lm_head.weight.T


class FakeLens:
    def __init__(self, model: FakeModel, name: str):
        g = torch.Generator().manual_seed(1)
        self.model = model
        self.source_layers = list(range(pins.N_LAYERS - 1))
        self.J = {la: torch.eye(D) + 0.1 * torch.randn(D, D, generator=g) for la in self.source_layers}

    def vectors(self, layer, ids, unit=True):
        rows = self.model.hf.lm_head.weight[ids] @ self.J[layer]
        return torch.nn.functional.normalize(rows, dim=-1) if unit else rows

    def readout(self, h, layer):
        return self.model.unembed(h.float() @ self.J[layer].T)


@needs_tok
def test_stage_run_on_a_fake_model_writes_only_its_run_dir_and_cache(tmp_path, monkeypatch):
    import bridge_jspace.lens as lens_mod
    import bridge_jspace.model as model_mod

    tok = RS.hf_tokenizer(MODEL)
    vocab = len(tok)
    monkeypatch.setattr(RS, "RESULTS", tmp_path / "results" / RS.EXP)
    monkeypatch.setattr(RS, "CACHE", tmp_path / "cache" / RS.EXP)
    monkeypatch.setattr(RS, "N", 2)
    monkeypatch.setattr(model_mod, "load_model", lambda: FakeModel(vocab))
    monkeypatch.setattr(lens_mod, "JLens", FakeLens)
    u_real = RS.pointer_basis(I.view("routes")["runs"][MODEL][0])  # the real U loads (d x 4) ...
    assert u_real.shape[0] == RS.model_config(MODEL)["d"] and u_real.shape[1] >= 2
    u_fake = np.linalg.qr(np.random.default_rng(0).standard_normal((D, u_real.shape[1])))[0]  # ... the fake's is D x r
    monkeypatch.setattr(RS, "pointer_basis", lambda run: u_fake)
    out = RS.stage_run("fake_review_states")
    written = {p.relative_to(tmp_path).parts[:2] for p in tmp_path.rglob("*") if p.is_file()}
    assert written <= {("results", RS.EXP), ("cache", RS.EXP)}, written
    plan = json.loads((out / "plan.json").read_text())
    root = tmp_path / "cache" / RS.EXP / MODEL
    assert (root / "head.safetensors").exists() and json.loads((root / "head.json").read_text())["d"] == D
    n_layers = pins.N_LAYERS
    for s in plan["sample"]:
        z = np.load(root / s["file"])
        assert z["h_O"].shape == (len(s["pos_O"]), n_layers, D) and z["h_O"].dtype == np.float16
        assert z["atoms_ids"].shape == (len(s["pairs"]), n_layers, RS.K)
        lens_layers = list(z["lens_layers"])
        assert (z["atoms_ids"][:, lens_layers] >= 1000).all() and (z["atoms_ids"][:, n_layers - 1] == -1).all()
        # at the bridge word: the stored random part has the stored share, about the J++ part's (X0's random part)
        r = next(i for i, (a, _) in enumerate(s["pairs"]) if s["pos_O"][a] == s["pos"])
        a, b = s["pairs"][r]
        dl = z["h_S"][b].astype(np.float32) - z["h_O"][a].astype(np.float32)
        la = plan["layer"]
        sq = float((dl[la] ** 2).sum())
        assert sq > 0
        assert abs(float((z["rand"][r, la].astype(np.float32) ** 2).sum()) / sq - z["rand_share"][r, la]) < 0.05
        assert abs(z["rand_share"][r, la] - z["jpp_share"][r, la]) < 0.2
        meta = json.loads(str(z["meta"]))
        assert meta["item"] == s["item"] and meta["roles_O"] == s["roles_O"]
    rows = [json.loads(line) for line in (out / "rank_check.jsonl").read_text().splitlines()]
    assert len(rows) == sum(len(v) for v in plan["rank"].values())
    assert all(set(r["ranks"]) == {"jpp", "rest", "rand"} and r["ranks"]["jpp"]["S_bridge_word"] >= 1 for r in rows)
    calib = (out / "calib.jsonl").read_text().splitlines()
    assert len(calib) == min(RS.N_CALIB, len(plan["sample"])) * 5 * 2
    arms = [json.loads(line) for line in (out / "arms.jsonl").read_text().splitlines()]
    armed = [s for s in plan["sample"] if s["kind"] in RS.ARM_KINDS]
    n_routes = sum(s["kind"] == "routes" for s in plan["sample"])
    assert len(arms) == 4 * len(armed) + 2 * n_routes and {a["arm"] for a in arms} == {*RS.ARMS, *RS.POINTER_ARMS}
    # an arm the view shows has its stored row beside it; sentence_order shows none / whole only
    assert all(a["stored"] is not None and a["match"] in (True, False) for a in arms if a["label"])
    assert all(a["label"] for a in arms if a["view"] in ("main_swap", "routes"))
    checks = json.loads((out / "checks.json").read_text())
    assert checks["arms"]["rows"] == len(arms)
    assert checks["change_rows"] == sum(len(s["pairs"]) for s in plan["sample"])
