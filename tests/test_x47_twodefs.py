"""Batch 47, test 47.12 (scripts/x47_twodefs.py): the two parts (ours vs Zach's top-10 on the same vector; the
protection; the projection), the run stage end to end on a tiny fake model with fake dictionaries (sealed), the gap
and the rule on planted rows, the seal. No real model."""

import json
import re
from types import SimpleNamespace

import pytest
import torch

from bridge_jspace.ablate import MatrixDictionary, top_span_removal
from scripts import x0_necessity as X
from scripts import x47_atoms as A
from scripts import x47_cumulative as C
from scripts import x47_twodefs as D


def _dic(n: int = 64, d: int = 32, seed: int = 0) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    return torch.nn.functional.normalize(torch.randn(n, d, generator=g), dim=-1)


# ---- the parts ------------------------------------------------------------------------------------------------------


def test_top_parts_are_his_top_span_removal_on_delta_and_the_state_variant_a_projection():
    dic = MatrixDictionary(_dic())
    g = torch.Generator().manual_seed(1)
    x, h_s = torch.randn(1, 32, generator=g), torch.randn(1, 32, generator=g)
    tp = D.top_parts(dic, x, h_s, None)
    assert torch.allclose(tp["top10"], top_span_removal(dic, x, 10), atol=1e-5)
    assert tp["atoms_top10"] == dic.logits(x).topk(10).indices[0].tolist() == tp["atoms_unprotected"]
    assert tp["atoms_top10_state"] == dic.logits(h_s).topk(10).indices[0].tolist()
    # (ii') projects Δ onto the state's atoms: Δ's remainder is orthogonal to every one of them
    rest = x - tp["top10_state"]
    assert torch.allclose(rest @ dic.atoms(torch.tensor(tp["atoms_top10_state"])).T, torch.zeros(1, 10), atol=1e-4)
    assert float((x - tp["top10"]).norm()) <= float(x.norm()) and float(tp["top10"].norm()) > 0


def test_protection_displaces_the_protected_atom():
    dic = MatrixDictionary(_dic())
    x = torch.randn(1, 32, generator=torch.Generator().manual_seed(2))
    top = dic.logits(x).topk(10).indices[0]
    tp = D.top_parts(dic, x, x, torch.tensor([int(top[0])]))
    assert int(top[0]) not in tp["atoms_top10"] and int(top[0]) in tp["atoms_unprotected"]
    assert len(set(tp["atoms_unprotected"]) - set(tp["atoms_top10"])) == 1


def test_protected_rows_keep_only_dictionary_tokens():
    row_of = torch.full((50,), -1, dtype=torch.long)
    row_of[:20] = torch.arange(20)  # tokens 0-19 are dictionary rows; 20-49 (digits etc.) are not
    logits = torch.zeros(50)
    logits[[3, 45, 7, 48, 10, 11, 12, 13, 14, 15, 16]] = torch.arange(11, 0, -1).float()
    assert D.protected_rows(logits, row_of).tolist() == [3, 7, 10, 11, 12, 13, 14, 15]  # the top-10: 3 45 7 48 10..15


# ---- the run stage on a fake model ----------------------------------------------------------------------------------


class WordTok:
    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


class FakeModel:
    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 32, vocab: int = 200):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers = tok, n_layers
        self.device = torch.device("cpu")
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

    def letter_token_ids(self):
        return torch.arange(64)


def fake_items(tok: WordTok, n: int = 12) -> list[dict]:
    """n main-test items as x47_cumulative.select writes them (the keys 47.12 and its view read)."""
    out = []
    digit = {str(d): tok(str(d)).input_ids[0] for d in range(10)}
    for i in range(n):
        o = f"Noah picked the bee. Iris picked the frog. The locker of the frog is 5. The locker of the bee is 3. Q{i}?"
        s = f"Noah picked the frog. Iris picked the bee. The locker of the frog is 5. The locker of the bee is 3. Q{i}?"
        texts = {v: f"<user> {ctx} Answer:" for v, ctx in (("org", o), ("alt", s))}
        enc = {v: tok(t, return_offsets_mapping=True) for v, t in texts.items()}
        ids = {v: e.input_ids for v, e in enc.items()}
        diff = [j for j, (a, b) in enumerate(zip(ids["org"], ids["alt"], strict=True)) if a != b]
        pos, other = diff[1], diff[0]
        off = enc["org"].offset_mapping
        readers = {w: {"id": f"{w}-{i}", "question": "q", "answer": "5", "cf_answer": "3", "tok_A": digit["5"], "tok_b": digit["3"],
                       "ids": ids, "text": {"org": texts["org"]}} for w in X.READERS}  # fmt: skip
        out.append({"scene": f"P{i:03d}", "design": "main", "entity": f"e{i % 5}", "cf_bridge": "bee", "domain": "animals",
                    "upstream": True, "prefix_same": False, "group": "locker-after", "pos": pos, "other": other,
                    "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ", "readers": readers,
                    "marks": {"bridge": [list(off[pos])], "pick": [], "other": [list(off[other])]},
                    "stored": {"whole": {"PP": 1, "PM": 0}}})  # fmt: skip
    return out


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = fake_items(tok)
    fake = FakeModel(tok)
    dic = _dic(64, 32)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", lambda model, name: SimpleNamespace(name=name))
    monkeypatch.setattr(D, "omp_dictionary", lambda model, lens, layer, letters: dic)
    monkeypatch.setattr(D, "zach_dictionary", lambda model, lens, layer, letters: MatrixDictionary(dic))
    monkeypatch.setattr(D, "RUNS", {**D.RUNS, pins.TARGET: f"{pins.RUN_PREFIX}fake_x47_12"})
    monkeypatch.setattr(D, "SOURCES", {**D.SOURCES, pins.TARGET: "fake_main"})
    counts = {
        "design": "main",
        "source": "fake_main",
        "items_at_L": len(items),
        "items": len(items),
        "dropped": {},
        "entities": 5,
    }
    monkeypatch.setattr(C, "select", lambda tok, design, run, layer: (items, counts))
    monkeypatch.setattr(X, "lens_record", lambda: {"name": "jpp", "source": ["fake"], "sha256": "0"})
    monkeypatch.setattr(X, "digit_ids", lambda tok: [tok(str(d)).input_ids[0] for d in range(10)])
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x47")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(D, "SPEC", tmp_path / "batch47.yaml")
    D.SPEC.write_text("")
    src = tmp_path / "x0" / "fake_main"
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    out = D.stage_run(f"{pins.RUN_PREFIX}fake_x47_12", "test")
    return SimpleNamespace(tok=tok, items=items, out=out, dic=dic)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    out, items = fake_run.out, fake_run.items
    assert {p.name for p in out.iterdir()} == {
        "manifest.json",
        "plan.json",
        "cases.jsonl",
        "outcomes.jsonl",
        "shares.jsonl",
    }
    rows = X.read_jsonl(out / "outcomes.jsonl")
    want = {(it["scene"], w, a) for it in items for w in X.READERS for a in D.ARMS}
    got = {(r["scene"], r["reader"], f"{r['definition']}:{r['arm']}" if r["definition"] else r["arm"]) for r in rows}
    assert got == want and len(rows) == len(want)
    keys = {(r["dict"], r["k"], r["omp"]) for r in rows if r["definition"]}
    assert keys == set(map(tuple, D.DEFS.values()))
    assert all(r["rendering"] == "chat" and r["layer"] == X.PREDICTED[C.pins.TARGET] for r in rows)
    shares = X.read_jsonl(out / "shares.jsonl")
    assert len(shares) == 2 * len(items)
    for s in shares:
        assert len(s["atoms_omp25"]) == 25 and len(s["atoms_top10"]) == 10 and len(s["atoms_top10_state"]) == 10
        assert 0 <= s["share_omp25"] <= 1 and 0 <= s["share_top10"] <= 1 and 0 <= s["share_top10_state"] <= 1
        assert 0 <= s["overlap_top10_in_omp25"] <= 10 and s["top10_displaced_by_protection"] >= 0
    m = json.loads((out / "manifest.json").read_text())
    assert "sealed" in m and m["keys"]["top10"] == ["paper10", 10, "top"] and "switches" in m


def test_verdict_and_view_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(A, "dan_answer", lambda question="", rev="HEAD": "yes · 70%")
    out = D.stage_verdict([fake_run.out.name], n_boot=100)
    blob = json.loads((out / "x47_12.json").read_text())
    m = blob["models"][0]
    assert (
        m["status"] == "tested" and m["answer"] in ("yes", "no", "can't tell") and set(m["definitions"]) == set(D.DEFS)
    )
    assert m["whole_vs_stored"]["lookup"]["n"] == 12 and {x["status"] for x in blob["models"][1:]} == {"pending"}
    assert "Q47.12" in (out / "x47_12.md").read_text()
    view = D.stage_view([fake_run.out.name])
    text = (view / "view.md").read_text()
    # 10 items x 2 readers marked, plus the header's legend; every arm row names its definition
    assert text.count("⟦bridge:") == 2 * 10 + 1 and text.count("| omp25:no_part |") == 0
    assert text.count("| no_part | omp25 |") == 20 and text.count("| no_rand | top10 |") == 20


# ---- the gap and the rule on planted rows --------------------------------------------------------------------------


def planted(
    recall_lost: dict[str, float], lookup_lost: dict[str, float], n: int = 100, s_whole: float = 0.6
) -> list[dict]:
    """Rows of both readers at L12 (chat): the whole change switches s_whole; under each definition's no_part the
    reader keeps (1 - lost) of its switches, under no_rand all of them."""
    rows = []
    for i in range(n):
        for w, lost in ((X.LOOKUP, lookup_lost), (X.RECALL, recall_lost)):
            base = {"scene": f"s{i}", "entity": f"e{i % 10}", "rendering": "chat", "layer": 12, "reader": w}
            sw = int(i < round(s_whole * n))
            rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "definition": None, "switched": sw})
            for d, key in D.DEFS.items():
                kept = int(i < round(s_whole * n * (1 - lost[d])))
                rows.append(
                    {
                        **base,
                        "dict": key[0],
                        "k": key[1],
                        "omp": key[2],
                        "arm": "no_part",
                        "definition": d,
                        "switched": kept,
                    }
                )
                rows.append(
                    {
                        **base,
                        "dict": key[0],
                        "k": key[1],
                        "omp": key[2],
                        "arm": "no_rand",
                        "definition": d,
                        "switched": sw,
                    }
                )
    return rows


def test_gap_and_rule_on_planted_rows():
    agree = planted({"omp25": 0.5, "top10": 0.4, "top10_state": 0.1}, {"omp25": 0.0, "top10": 0.0, "top10_state": 0.0})
    defs = {d: D.gap_of(agree, 12, tuple(k), n_boot=200) for d, k in D.DEFS.items()}
    assert defs["omp25"]["gap"][0] == pytest.approx(0.5) and defs["top10"]["gap"][0] == pytest.approx(0.4)
    assert defs["omp25"]["recall"]["excess"][0] == pytest.approx(0.5) and defs["omp25"]["lookup"]["excess"][0] == 0.0
    r = D.model_rule(defs)
    assert r["answer"] == "yes" and r["difference"] == pytest.approx(-0.1)
    apart = planted({"omp25": 0.5, "top10": 0.2, "top10_state": 0.1}, {"omp25": 0.0, "top10": 0.0, "top10_state": 0.0})
    assert D.model_rule({d: D.gap_of(apart, 12, tuple(k), n_boot=200) for d, k in D.DEFS.items()})["answer"] == "no"
    # the lookup's loss counts too: a lookup loss under (ii) narrows its gap
    lk = planted({"omp25": 0.5, "top10": 0.5, "top10_state": 0.1}, {"omp25": 0.0, "top10": 0.3, "top10_state": 0.0})
    r = D.model_rule({d: D.gap_of(lk, 12, tuple(k), n_boot=200) for d, k in D.DEFS.items()})
    assert r["answer"] == "no" and r["difference"] == pytest.approx(-0.3)
    weak = planted(
        {"omp25": 0.5, "top10": 0.5, "top10_state": 0.1}, {"omp25": 0.0, "top10": 0.0, "top10_state": 0.0}, s_whole=0.2
    )
    assert (
        D.model_rule({d: D.gap_of(weak, 12, tuple(k), n_boot=200) for d, k in D.DEFS.items()})["answer"] == "can't tell"
    )


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    monkeypatch.setattr(A, "dan_answer", lambda question="", rev="HEAD": "")
    for stage in (lambda: D.stage_verdict([], n_boot=10), lambda: D.stage_view([])):
        with pytest.raises(AssertionError, match="sealed"):
            stage()
    assert list(tmp_path.iterdir()) == []


def test_the_committed_predictions_file_has_the_q47_12_block():
    text = A.subprocess.run(["git", "show", f"HEAD:{D.PREDICTIONS}"], cwd=A.pins.REPO_ROOT, capture_output=True, text=True,
                            check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{D.QUESTION}**" in text and isinstance(A.dan_answer(D.QUESTION), str)
