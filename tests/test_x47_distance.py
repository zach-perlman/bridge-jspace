"""x47_distance (batch 47, test 47.16): the fillers and their checks, the variants at k, the fake end-to-end run with
the stop rule (sealed), the rule on planted cells, and the verify-pack view."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x47_distance as D

LK, RC = X.LOOKUP, X.RECALL
ANIMALS = ["ant", "bee", "cat", "cow", "crow", "duck", "fox", "frog", "goat", "hen", "owl", "pig", "yak", "eel"]
PEOPLE = ["Ann", "Ben", "Cara", "Dan", "Eve", "Finn", "Gus"]
LEGS = {a: 6 if a in ("ant", "bee") else 2 if a in ("crow", "duck", "hen", "owl") else 0 if a == "eel" else 4
        for a in ANIMALS}  # fmt: skip


# ---- fillers and texts ------------------------------------------------------------------------------------------------


def test_filler_pool_is_clean_and_large_enough():
    assert len(D.FILLERS) >= max(D.KS) and D.filler_checks(D.FILLERS, ANIMALS, PEOPLE) == []
    bad = D.filler_checks((*D.FILLERS[:3], "The frog sat by the pond.", "It took 3 hours.", "Ann left early.",
                           "One more thing. Then another."), ANIMALS, PEOPLE)  # fmt: skip
    assert len(bad) == 5 and any("item" in b for b in bad) and any("digit" in b for b in bad)
    assert any("person" in b for b in bad) and any("one sentence" in b for b in bad) and any("number" in b for b in bad)


def test_filler_blocks_nest_and_are_seeded_per_scene():
    blocks = {k: D.filler_block("C2-0001", k) for k in D.KS}
    assert blocks[0] == [] and len(blocks[50]) == 50 and len(set(blocks[50])) == 50
    assert blocks[5] == blocks[20][:5] == blocks[50][:5] and blocks[20] == blocks[50][:20]
    assert D.filler_block("C2-0001", 5) == blocks[5] and D.filler_block("C2-0002", 5) != blocks[5]


def c2_text(rng: random.Random) -> dict:
    """One routes C2 scene's texts (x6_routes' C2: Iris picked A in O, B in S; B's and C's lockers swapped, B -> e)."""
    a_item, b_item, c_item = rng.sample(ANIMALS, 3)
    a, b, c, _, e = rng.sample(range(1, 10), 5)
    asked, p1, p2 = rng.sample(PEOPLE, 3)
    order = rng.sample([a_item, b_item, c_item], 3)
    val = {a_item: a, b_item: b, c_item: c}
    picks = rng.sample([(asked, a_item), (p1, b_item), (p2, c_item)], 3)
    sw = {b_item: c_item, c_item: b_item}
    s_lock = [(sw.get(x, x), e if sw.get(x, x) == b_item else val[sw.get(x, x)]) for x in order]
    s_pick = [(q, b_item if q == asked else x) for q, x in picks]
    return {"o": R.context([(x, val[x]) for x in order], picks), "s": R.context(s_lock, s_pick), "asked": asked,
            "bridge": a_item, "cf_bridge": b_item, "expect": {"identity": b, "position": c, "value": e, "original": a}}  # fmt: skip


def test_with_fillers_sits_between_the_lockers_and_the_picks():
    t = c2_text(random.Random(0))
    block = D.filler_block("x", 5)
    o = D.with_fillers(t["o"], block)
    lockers = [m.end() for m in W.LOCKER.finditer(o)]
    picks = [m.start() for m in R.PICK.finditer(o)]
    first_filler = o.index(block[0])
    assert max(lockers) < first_filler < min(picks) and o.index(block[-1]) < min(picks)
    assert D.with_fillers(t["o"], []) == t["o"] and W.slots_of(o) == W.slots_of(t["o"])


# ---- fakes (as tests/test_x47_six.py) --------------------------------------------------------------------------------


class WordTok:
    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids, skip_special_tokens=False) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


class FakeModel:
    def __init__(self, tok: WordTok, vocab: int, n_layers: int = 33, d: int = 32):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.device = tok, n_layers, torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

    def forward(self, ids, edits):
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
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts


def wrap(tok, item: dict, rendering: str, ctx: str) -> str:
    return f"<|im_start|>user\n{ctx}\n{item['question']} digit<|im_end|>\nAnswer:"


def fake_base(n: int) -> list[dict]:
    rng = random.Random(11)
    out = []
    for i in range(n):
        t = c2_text(rng)
        out.append({"scene": f"C2-{i + 1:04d}", "condition": "C2", "rendering": "chat", "bridge": t["bridge"],
                    "cf_bridge": t["cf_bridge"], "context": t["o"], "cf_context": t["s"], "expect": t["expect"],
                    "readers": {LK: {"question": R.LOOKUP_Q.format(p=t["asked"])}}})  # fmt: skip
    return out


@pytest.fixture
def word_tok(monkeypatch):
    monkeypatch.setattr(X, "render", wrap)
    monkeypatch.setattr(R, "pools", lambda tok: (LEGS, ANIMALS, PEOPLE))
    tok = WordTok()
    for d in range(10):
        tok(str(d))
    return tok


def test_cases_at_reencode_every_k(word_tok):
    base = fake_base(8)
    at = {k: D.cases_at(word_tok, base, k)[0] for k in D.KS}
    for k, cases in at.items():
        assert len(cases) == 8 and all(c["k"] == k and c["scene"].endswith(f"-k{k}") for c in cases)
        for c, b in zip(cases, base, strict=True):
            ids = c["readers"][LK]["ids"]
            assert word_tok.decode([ids["org"][c["pos"]]]).strip().rstrip(".") == b["bridge"]
            assert (
                len(ids["org"]) == len(ids["alt"])
                and c["readers"][RC]["ids"]["org"][: c["pos"] + 1] == ids["org"][: c["pos"] + 1]
            )
            assert len(c["fillers"]) == k and c["j"] == [x for x, _ in W.slots_of(b["context"])].index(b["bridge"])
            assert c["layout"] == "LLL" + "." * (c["pick_index"] - 3) and c["pick_index"] >= 3 + k
            assert len(ids["org"]) == len(at[0][base.index(b)]["readers"][LK]["ids"]["org"]) + sum(
                len(word_tok(" " + f).input_ids) for f in c["fillers"]
            )


@pytest.fixture
def fake_run(tmp_path, monkeypatch, word_tok):
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    base = fake_base(12)
    for k in D.KS:  # the vocab holds every token before the model is built
        D.cases_at(word_tok, base, k)
    fake = FakeModel(word_tok, vocab=len(word_tok.vocab) + 8)

    def competence(model, cs, digits, ws):  # k = 50 misses the gate (the recall reads O wrong on most scenes)
        rows = []
        for i, c in enumerate(cs):
            for w in X.READERS:
                for v in ("org", "alt"):
                    ok = not (
                        (c["k"] == 50 and w == RC and v == "org" and i % 3) or (c["k"] == 5 and i == 1 and v == "alt")
                    )
                    rows.append({"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "greedy": "",
                                 "said": "", "right": ok, "read_right": ok, "ws_skipped": 0, "cand_right": ok})  # fmt: skip
        return rows

    g = torch.Generator().manual_seed(5)
    alf, _ = torch.linalg.qr(torch.randn(32, 2, generator=g))
    mu = {s: (alf @ torch.tensor([float(s), float(s % 2)])).numpy().astype(np.float64) for s in W.SLOTS}
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(X, "competence", competence)
    monkeypatch.setattr(D, "base_cases", lambda tok_, n=D.N_CAND: base)
    monkeypatch.setattr(MM, "pointer_means", lambda run: mu)
    monkeypatch.setattr(MM, "subspaces", lambda run: ({"Alf": alf.numpy().astype(np.float64)}, {}))
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x47_distance")
    name = f"{pins.RUN_PREFIX}fake_x47_16"
    return SimpleNamespace(tok=word_tok, base=base, out=D.stage_run(name, "test"), name=name)


def test_run_stops_at_the_failing_k_and_pairs_the_rest(fake_run):
    out = fake_run.out
    m = json.loads((out / "manifest.json").read_text())
    gate = json.loads((out / "gate.json").read_text())
    assert m["stopped_at"] == 50 and m["skipped"] == [] and m["passed"] == [0, 5, 20] and m["tested"]
    assert gate["gates"]["50"]["pass"] is False and gate["gates"]["5"]["eligible"] == 11
    assert len(gate["chosen"]) == 11 and "C2-0002" not in gate["chosen"]
    assert not list(out.glob("verdict*")) and not list(out.glob("x47_16*"))  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {r["k"] for r in rows} == {0, 5, 20} and {r["base_scene"] for r in rows} == set(gate["chosen"])
    assert len(rows) == 3 * 11 * 2 * (len(D.DELTA_ARMS) + 4)
    lk = [r for r in rows if r["reader"] == LK]
    assert all(r["route"] in D.ROUTES for r in lk)
    assert all(r["swap"] in W.CLASSES for r in lk if r["arm"] in ("write", "random"))
    z = np.load(out / "states.npz")
    assert z["h_0"].shape == z["h_20"].shape == (11, 32) and "h_50" not in z and len(z["j"]) == 11
    betas = X.read_jsonl(out / "beta.jsonl")
    assert {b["k"] for b in betas} == {5, 20} and all(("beta_prev" in b) == (b["j"] >= 1) for b in betas)
    assert all(("beta_next" in b) == (b["j"] <= 1) for b in betas)
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 33 and all(0 <= r["share_alf"] <= 1 + 1e-6 for r in norms)
    assert all(len(r["write_norm"]) == 2 and all(w > 0 for w in r["write_norm"].values()) for r in norms)


def test_verdict_pieces_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "9B robust 60%; Muse breaks at 50")
    res = D.model_result(fake_run.name, n_boot=50)
    assert res["status"] == "tested" and res["label"] == "breaks at k = 50" and sorted(res["cells"]) == [0, 5, 20]
    assert set(res["probes"]) == {0, 5, 20} and set(res["betas"]) == {5, 20} and set(res["beta_within"]) == {5, 20}
    for c in res["cells"].values():
        assert c["swap"]["n"] == 2 * c["n"] and set(c["recall_kept"]) >= set(D.DELTA_ARMS)
    lines = D.report_lines([res, D.model_result("muse30_x47_16")], "9B robust 60%; Muse breaks at 50", 50)
    text = "\n".join(lines)
    assert "breaks at k = 50" in text and "pending" in text and "## Collateral" in text
    ex = D.examples_lines([fake_run.name], decode=fake_run.tok.decode)
    assert sum(line.startswith("### ") for line in ex) == 10 * 3 and any("⟦" in line for line in ex)
    out = D.stage_verdict([fake_run.name], n_boot=50)
    assert (out / "x47_16.md").exists() and (out / "examples.md").exists()


# ---- the rule on planted cells ---------------------------------------------------------------------------------------


def planted(pos, ident, probe, swap, acc50=0.95):
    cells = {k: {"routes": {"whole": {"position": [pos[k], 0, 1], "identity": [ident[k], 0, 1]}},
                 "swap": {"write": [swap[k], 0, 1]}} for k in pos}  # fmt: skip
    probes = {k: {"probe": [probe[k], 0, 1]} for k in pos}
    gates = {str(k): {"org_read_accuracy": {LK: 0.98, RC: acc50 if k == 50 else 0.95}} for k in D.KS}
    return cells, probes, gates


def test_rule_reads_robust_near_far_breaks_and_none():
    flat = {k: 0.5 for k in D.KS}
    betas = {k: {"beta": [0.1, 0, 0.2]} for k in D.KS if k}
    r = D.rule(*planted(flat, flat, {k: 0.9 for k in D.KS}, flat), None, betas)
    assert r["label"] == "distance-robust address" and r["fig8c_holds"]
    pos = {0: 0.5, 5: 0.5, 20: 0.4, 50: 0.25}
    ident = {0: 0.3, 5: 0.3, 20: 0.4, 50: 0.55}
    r = D.rule(*planted(pos, ident, {k: 0.9 for k in D.KS}, flat), None, {5: {"beta": [0.3, 0, 1]}})
    assert r["label"] == "address near, identity far" and not r["fig8c_holds"]
    r = D.rule(*planted(pos, ident, {k: 0.9 for k in D.KS}, flat, acc50=0.7), None, {})
    assert r["label"] == "none of the three" and not r["fig8c_holds"]
    r = D.rule(*planted(flat, flat, {k: 0.9 for k in D.KS}, {0: 0.5, 5: 0.5, 20: 0.34, 50: 0.5}), None, betas)
    assert r["label"] == "none of the three"
    r = D.rule(*planted(flat, flat, {0: 0.9, 5: 0.9, 20: 0.79, 50: 0.9}, flat), None, betas)
    assert r["label"] == "none of the three"
    cells, probes, gates = planted({0: 0.5, 5: 0.5}, {0: 0.3, 5: 0.3}, {0: 0.9, 5: 0.9}, {0: 0.5, 5: 0.5})
    assert D.rule(cells, probes, gates, 20, {5: {"beta": [0.2, 0, 1]}})["label"] == "breaks at k = 20"


def test_beta_cells_average_over_j_at_least_one():
    betas = [{"k": 5, "j": j, "entity": f"e{i}", "beta_prev": 0.1 * j, "norm_d_prev": 1.0, "norm_step_prev": 2.0}
             for i in range(6) for j in (1, 2)] + [{"k": 5, "j": 0, "entity": "e9", "beta_next": 0.5}]  # fmt: skip
    c = D.beta_cells(betas, 5, 50)
    assert c is not None
    assert c["n"] == 12 and abs(c["beta"][0] - 0.15) < 1e-9
    assert abs(c["by_j"]["1"] - 0.1) < 1e-9 and abs(c["by_j"]["2"] - 0.2) < 1e-9
    assert c["norm_ratio_median"] == 0.5 and c["beta_next"] == 0.5 and D.beta_cells(betas, 20, 50) is None


# ---- sealing ------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_q47_16(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = (
        "**Q47.14** x\n\nDan: yes\n\n**Q47.16** (47.16) y\n\nRule: z.\n\nDan:{}\n\n**Q47.7, addition** w\n\nDan: no\n"
    )
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert D.dan_answer() == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" 9B robust 60%; Muse near-far 50%")))
    assert D.dan_answer() == "9B robust 60%; Muse near-far 50%"


def test_verdict_and_examples_refuse_while_sealed(monkeypatch):
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_verdict(["qwen35_9b_x47_16"])
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_examples(["qwen35_9b_x47_16"])
