"""Batch 47, test 47.0 (scripts/x47_verbal.py): the readings on planted data, the readout statistics against brute
force, and the GPU stage end to end on CPU with a fake model and lens (the real tokenizer, items and pointer means)."""

from __future__ import annotations

import json

import numpy as np
import pytest
import torch

from scripts import x47_verbal as V

# ---- readout statistics ----------------------------------------------------------------------------------------------


def test_ranks_match_brute_force_with_ties():
    g = torch.Generator().manual_seed(0)
    logits = torch.randint(0, 20, (4, 50), generator=g).float()  # many ties
    ids = torch.tensor([0, 7, 49])
    got = V.ranks(logits, ids)
    want = torch.stack([1 + (logits > logits[:, [t]]).sum(-1) for t in ids.tolist()], dim=1)
    assert torch.equal(got, want)


def test_readout_stats_on_planted_logits():
    v = 30
    base = torch.zeros(v)
    base[5] = 3.0
    logp_base = torch.log_softmax(base, -1)
    edit = torch.stack([base.clone(), base.clone()])
    edit[1, 12] = 10.0  # row 1 puts an ordinal token on top
    sets = {"ordinal": torch.tensor([12, 13]), "digits": torch.tensor([20, 21, 22])}
    st = V.readout_stats(edit, logp_base, sets, target_tok=21, alt_tok=5, top=3)
    assert st["kl"][0] == pytest.approx(0.0, abs=1e-6) and st["kl"][1] > 0.5
    assert st["best_ordinal"].tolist()[1] == 1 and int(st["best_ordinal_tok"][1]) == 12
    assert st["best_ordinal"].tolist()[0] == 2  # tied at 0 below token 5: one token strictly higher
    assert st["alt_name"].tolist() == [1, 2]
    assert st["top"][1, 0] == 12
    assert "kl" not in V.readout_stats(edit, None, sets, None, None)


# ---- summary statistics and readings ---------------------------------------------------------------------------------


def planted_null(n_rand=200, n_cases=60, seed=0):
    rng = np.random.default_rng(seed)
    ranks_ = rng.integers(50, 5000, size=(n_rand, n_cases)).astype(float)
    kl = rng.gamma(2.0, 0.01, size=(n_rand, n_cases))
    ents = [f"e{i // 2}" for i in range(n_cases)]
    return ranks_, kl, ents, rng


def test_against_null_detects_a_verbalized_write_and_not_a_random_one():
    ranks_, kl, ents, rng = planted_null()
    named = V.against_null(np.full(ranks_.shape[1], 3.0), ranks_, ents, lower_better=True, n_boot=500)
    assert named["beyond"] and named["median"] == 3.0 and named["case_share_beyond"][0] == 1.0
    like = V.against_null(rng.integers(50, 5000, size=ranks_.shape[1]).astype(float), ranks_, ents, True, n_boot=500)
    assert not like["beyond"] and like["case_share_beyond"][0] < 0.2
    loud = V.against_null(kl[0] * 50, kl, ents, lower_better=False, n_boot=500)
    quiet = V.against_null(kl[1], kl[2:], ents, lower_better=False, n_boot=500)
    assert loud["beyond"] and not quiet["beyond"] and loud["null_pct"] == V.HI_PCT


def test_recon_summary_ratio():
    rows = [
        {"dict": "all", "k": 25, "kind": "write", "share": 0.3},
        {"dict": "all", "k": 25, "kind": "U", "share": 0.1},
        {"dict": "all", "k": 25, "kind": "identity", "share": 0.5},
    ]
    rows += [{"dict": "all", "k": 25, "kind": "random", "share": s} for s in (0.05, 0.1, 0.15)]  # fmt: skip
    r = V.recon_summary(rows)["all|25"]
    assert (
        r["pointer"] == pytest.approx(0.3)
        and r["ratio"] == pytest.approx(3.0)
        and r["identity_ratio"] == pytest.approx(5)
    )


def cell(median, cut, beyond):
    return {"median": median, "null_cut": cut, "beyond": beyond}


def test_model_reading_labels():
    no = cell(4000, 900, False)
    kl_in, kl_out = cell(0.01, 0.05, False), cell(0.2, 0.05, True)
    assert V.model_reading(no, no, 1.5, kl_in)["label"] == "not verbalizable"
    assert V.model_reading(cell(5, 900, True), no, 1.5, kl_in)["label"] == "partly verbalizable"
    assert V.model_reading(no, cell(10, 50, True), 1.0, kl_in)["label"] == "partly verbalizable"  # a digit named
    assert V.model_reading(no, no, 3.0, kl_in)["label"] == "partly verbalizable"  # reconstruction
    assert V.model_reading(no, no, 2.5, kl_in)["label"] == "neither"  # between the bars
    assert V.model_reading(no, no, 1.0, kl_out)["label"] == "neither"  # the lens moves, names nothing
    # beyond the null but not in the top 20: not named
    assert V.model_reading(cell(300, 900, True), no, 1.0, kl_in)["label"] == "not verbalizable"


def test_overall():
    assert V.overall({"a": "not verbalizable", "b": "not verbalizable"}) == "not verbalizable"
    assert V.overall({"a": "not verbalizable", "b": "partly verbalizable"}) == "partly verbalizable (b)"
    assert V.overall({"a": "not verbalizable", "b": "neither"}).startswith("mixed")
    assert V.overall({}) == "not landed"


def test_sanity_swap_line_source():
    sw = V.sanity_swap()
    for t in ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"):
        assert 0 < sw[t]["part"][0] < sw[t]["random"][0] and sw[t]["source"]


# ---- the GPU stage on CPU (fake model and lens) ----------------------------------------------------------------------


class FakeModel:
    def __init__(self, tok, d: int, vocab: int, n_every: int = 400):
        g = torch.Generator().manual_seed(0)
        self.tokenizer, self.d, self.device = tok, d, torch.device("cpu")
        self.decoded = [f"<{i}>" for i in range(vocab)]
        self.special_ids = frozenset(range(n_every, vocab))  # every non-special token: 0..n_every-1
        self.a = torch.randn(d, 8, generator=g) / d**0.5
        self.b = torch.randn(8, vocab, generator=g)

    def letter_token_ids(self):
        return torch.arange(200)

    def run(self, ids, edits=None, record=()):
        hs = torch.randn(ids.shape[1], self.d, generator=torch.Generator().manual_seed(int(ids.sum())))
        return self.unembed(hs[-1]), {la: hs for la in record}

    def unembed(self, h):
        return (h.float() @ self.a) @ self.b


class FakeLens:
    def __init__(self, model, name):
        self.model = model

    def readout(self, h, layer):
        return self.model.unembed(h)

    def vectors(self, layer, token_ids, unit=True):
        g = torch.Generator().manual_seed(1)
        return torch.nn.functional.normalize(torch.randn(len(token_ids), self.model.d, generator=g), dim=-1)


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


def test_stage_run_end_to_end_on_cpu(tok, tmp_path, monkeypatch):
    import bridge_jspace.lens as L
    import bridge_jspace.model as M
    from bridge_jspace import pins

    target = pins.model_pin()["target"]
    if target not in V.X8_RUN:
        pytest.skip(f"no x8_write run for {target}")
    from scripts import x0_massmean as MM
    from scripts import x6_routes as R

    d = MM.subspaces(R.STATES[target])[0]["Alf"].shape[0]
    vocab = len(tok)
    monkeypatch.setattr(M, "load_model", lambda: FakeModel(tok, d, max(vocab, 1000)))
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(V, "RESULTS", tmp_path)
    monkeypatch.setattr(V, "KS", (3, 5))
    name = pins.RUN_PREFIX + "x47_verbal_smoke"
    out = V.stage_run(name, n_items=3, n_rand=6)
    rows = [json.loads(x) for x in (out / "readouts.jsonl").read_text().splitlines()]
    cases = [r for r in rows if r["arm"] == "write"]
    assert len([r for r in rows if r["arm"] == "base"]) == 3 and len(cases) == 6  # 2 writes per item
    nz = np.load(out / "null.npz")
    assert nz["kl"].shape == (6, 6) and (nz["kl"] >= -1e-5).all()
    omp = [json.loads(x) for x in (out / "omp.jsonl").read_text().splitlines()]
    kinds = {r["kind"] for r in omp}
    assert kinds == {"U", "write", "identity", "random"}
    assert len([r for r in omp if r["kind"] == "write"]) == 6 * 2 * 2  # 6 writes x 2 dictionaries x 2 k
    assert all(0 <= r["share"] <= 1 + 1e-5 for r in omp)
    s = V.run_summary(out, n_boot=200)
    assert s["n_cases"] == 6 and s["reading"]["label"] in ("not verbalizable", "partly verbalizable", "neither")
    blob = {
        "models": {target: s},
        "sanity_swap": V.sanity_swap(),
        "overall": V.overall({target: s["reading"]["label"]}),
    }
    lines = V.summary_lines(blob)
    assert any(line.startswith("| reading |") for line in lines)
    assert (out / "examples.md").exists() and "⟦" in (out / "examples.md").read_text()
