"""Batch 47, test 47.11 (scripts/x47_agnostic.py): the matched scenes (shared digits / people / slots across the item
types; names distinct from the pickers; A and B with different facts) on the target's tokenizer when cached; the run
stage end to end on a tiny fake model (per-reader gates, the refit arms on the test half only, sealed); the rule and
the verdict on planted rows; the seal. No real model."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_agnostic as G
from scripts import x47_atoms as A


def _real_tokenizer():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


# ---- scenes -------------------------------------------------------------------------------------------------------


def test_context_names_items_without_the_article():
    assert G.context("names", [("Alice", 5)], [("Iris", "Alice")]) == "The locker of Alice is 5. Iris picked Alice."
    assert (
        G.context("fruits", [("plum", 5)], [("Iris", "plum")]) == "The locker of the plum is 5. Iris picked the plum."
    )


def test_said_of_reads_digits_and_colours():
    assert G.said_of(" 5\n", "digit") == "5" and G.said_of("Yellow.", "word") == "yellow"
    assert G.said_of("I think it is purple", "word") == "purple" and G.said_of("no idea", "word") is None


def test_scenes_are_matched_across_types_on_the_tokenizer():
    tok = _real_tokenizer()
    cases, dropped = G.scenes(tok, 12)
    by = {t: [c for c in cases if c["type"] == t] for t in G.TYPES}
    assert all(len(v) == 12 for v in by.values())
    shared = {
        t: {c["index"]: (c["digits"], c["people"], c["slot_org"], c["slot_alt"]) for c in v} for t, v in by.items()
    }
    common = set.intersection(*(set(v) for v in shared.values()))
    assert len(common) >= 3  # the same scene index gives the same digits, people and slots in every type
    for i in common:
        assert len({json.dumps(shared[t][i]) for t in G.TYPES}) == 1
    for c in cases:
        ids = c["readers"][X.LOOKUP]["ids"]
        assert len(ids["org"]) == len(ids["alt"]) and ids["org"][c["pos"]] != ids["alt"][c["pos"]]
        assert tok.decode([ids["org"][c["pos"]]]).strip() == c["bridge"]
        assert tok.decode([ids["alt"][c["pos"]]]).strip() == c["cf_bridge"]
        assert c["expect"]["identity"] == c["digits"][1] and c["expect"]["position"] == c["digits"][2]
        assert c["expect"]["value"] == c["digits"][4] and c["expect"]["original"] == c["digits"][0]
        if c["type"] == "names":
            assert set(c["items"]).isdisjoint(c["people"]) and X.RECALL not in c["readers"]
        else:
            rd = c["readers"][X.RECALL]
            assert rd["answer"] != rd["cf_answer"] and rd["tok_A"] != rd["tok_b"]
            assert rd["kind"] == ("word" if c["type"] == "fruits" else "digit")
            assert (rd["suffix"] == []) == (c["type"] == "fruits")
            assert rd["ids"]["org"][: c["pos"] + 1] == ids["org"][: c["pos"] + 1]
    assert all(k.split(":")[1].strip() == "A and B share their fact" for k in dropped)


def test_single_token_report_on_cached_tokenizers():
    try:
        rep = G.single_token_report(["qwen3.5-9b"])
    except Exception as e:
        pytest.skip(f"tokenizer.json not cached: {e}")
    assert rep["colours"]["n_kept"] == len(G.COLOURS) and rep["names"]["n_kept"] > 20 and rep["fruits"]["n_kept"] >= 15


def test_refit_basis_and_split():
    g = torch.Generator().manual_seed(0)
    mu = torch.randn(3, 8, generator=g) * 3
    slots = [i % 3 for i in range(60)]
    h = (mu[slots] + 0.1 * torch.randn(60, 8, generator=g)).numpy()
    u = G.refit_basis(h, slots)
    assert u.shape == (8, 2) and np.allclose(u.T @ u, np.eye(2), atol=1e-8)
    fit, test = G.split_halves([f"s{i}" for i in range(11)], "fruits")
    assert sorted(fit + test) == list(range(11)) and len(fit) == 5 and not set(fit) & set(test)
    assert G.split_halves([f"s{i}" for i in range(11)], "fruits") == (fit, test)  # seeded
    with pytest.raises(AssertionError, match="slot"):
        G.refit_basis(h, [0] * 60)


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
    """A tiny causal stand-in (as tests/test_x45p.py's): each block mixes the running mean into every position."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 16, vocab: int = 200):
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


def fake_cases(tok: WordTok, n: int = 10) -> list[dict]:
    """n fake C2 scenes per type as scenes() writes them: a lookup on every type, a recall on animals and fruits."""
    out = []
    digit = {str(d): tok(str(d)).input_ids[0] for d in range(10)}
    for t in G.TYPES:
        for i in range(n):
            # a per-item filler word first, so the fake model's bridge states differ across items (the refit's classes)
            o = f"Note{i}. " + G.context(t, [("x", 1), ("y", 2), ("z", 3)], [("Iris", "x"), ("Bo", "y"), ("Cy", "z")])
            s = f"Note{i}. " + G.context(t, [("x", 1), ("z", 3), ("y", 7)], [("Iris", "y"), ("Bo", "y"), ("Cy", "z")])
            readers = {}
            specs = [(X.LOOKUP, "Which locker belongs to Iris's pick?", "digit", ("1", "7"))]
            if t != "names":
                specs.append(
                    (
                        X.RECALL,
                        "fact?",
                        "digit" if t == "animals" else "word",
                        ("4", "2") if t == "animals" else ("red", "green"),
                    )
                )
            for w, q, kind, ans in specs:
                ids = {v: tok(f"{ctx} {q} Answer:").input_ids for v, ctx in (("org", o), ("alt", s))}
                ta = digit[ans[0]] if kind == "digit" else tok(" " + ans[0]).input_ids[0]
                tb = digit[ans[1]] if kind == "digit" else tok(" " + ans[1]).input_ids[0]
                readers[w] = {"question": q, "kind": kind, "answer": ans[0], "cf_answer": ans[1], "ids": ids, "tok_A": ta,
                              "tok_b": tb, "suffix": [tok.vocab.setdefault(" ", len(tok.vocab))] if kind == "digit" else []}  # fmt: skip
            pos = next(
                j
                for j, (a, b) in enumerate(
                    zip(readers[X.LOOKUP]["ids"]["org"], readers[X.LOOKUP]["ids"]["alt"], strict=True)
                )
                if a != b
            )
            out.append({"scene": f"{t}-{i:04d}", "type": t, "condition": "C2", "rendering": "chat", "domain": t, "bridge": f"x{i % 4}",
                        "cf_bridge": "y", "context": o, "cf_context": s, "pos": pos, "index": i, "slot_org": i % 3, "slot_alt": (i + 1) % 3,
                        "people": ["Iris", "Bo", "Cy"], "digits": [1, 2, 3, 9, 7], "items": ["x", "y", "z"],
                        "expect": {"identity": 2, "position": 3, "value": 7, "original": 1},
                        "route_tokens": {k: digit[str(v)] for k, v in {"identity": 2, "position": 3, "value": 7, "original": 1}.items()},
                        "readers": readers})  # fmt: skip
    return out


def fake_competence(cases, right_recall: set[str]) -> list[dict]:
    rows = []
    for c in cases:
        for w in c["readers"]:
            ok = w == X.LOOKUP or c["scene"] in right_recall
            for v in ("org", "alt"):
                rows.append({"scene": c["scene"], "type": c["type"], "reader": w, "variant": v, "greedy": "", "said": "", "right": ok,
                             "read_right": ok})  # fmt: skip
    return rows


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    cases = fake_cases(tok)
    fake = FakeModel(tok)
    right_recall = {c["scene"] for c in cases if c["type"] == "animals" and int(c["scene"][-1]) < 8} | {
        c["scene"] for c in cases if c["type"] == "fruits" and int(c["scene"][-1]) < 5
    }  # the fruit recall's gate fails (0.5)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(G, "RUNS", {**G.RUNS, pins.TARGET: f"{pins.RUN_PREFIX}fake_x47_11"})
    monkeypatch.setattr(
        G, "item_pools", lambda tok: ({t: [] for t in G.TYPES}, {t: {} for t in G.TYPES}, {t: [] for t in G.TYPES})
    )
    monkeypatch.setattr(G, "scenes", lambda tok, n, types=G.TYPES, **k: ([c for c in cases if c["type"] in types], {}))
    monkeypatch.setattr(G, "competence", lambda model, cases_, ws: fake_competence(cases_, right_recall))
    monkeypatch.setattr(
        G, "pointer_basis", lambda target: np.linalg.qr(np.random.default_rng(0).standard_normal((16, 4)))[0]
    )
    monkeypatch.setattr(X, "whitespace_mask", lambda model: torch.zeros(200, dtype=torch.bool))
    monkeypatch.setattr(X, "digit_ids", lambda tok: [tok(str(d)).input_ids[0] for d in range(10)])
    monkeypatch.setattr(X, "lens_record", lambda: {"name": "jpp", "source": ["fake"], "sha256": "0"})
    monkeypatch.setattr(G, "RESULTS", tmp_path / "x47")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(G, "SPEC", tmp_path / "batch47.yaml")
    G.SPEC.write_text("")
    out = G.stage_run(f"{pins.RUN_PREFIX}fake_x47_11", "test", n=8)
    return SimpleNamespace(tok=tok, cases=cases, fake=fake, out=out, right_recall=right_recall)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    out = fake_run.out
    assert {p.name for p in out.iterdir()} == {"manifest.json", "gate.json", "competence.jsonl", "cases.jsonl", "outcomes.jsonl",
                                               "norms.jsonl", "refit.json"}  # sealed: no verdict  # fmt: skip
    rows = X.read_jsonl(out / "outcomes.jsonl")
    gate = json.loads((out / "gate.json").read_text())["gate"]
    assert all(gate[t]["readers"]["lookup"]["pass"] and gate[t]["chosen"] == 8 for t in G.TYPES)
    assert gate["animals"]["readers"]["recall"]["pass"] and not gate["fruits"]["readers"]["recall"]["pass"]
    assert "recall" not in gate["names"]["readers"]
    lk = [r for r in rows if r["reader"] == X.LOOKUP]
    assert {r["type"] for r in lk} == set(G.TYPES) and all(r["route"] in R.ROUTES for r in lk)
    for t in G.TYPES:
        mine = [r for r in lk if r["type"] == t]
        test = {r["scene"] for r in mine if r["half"] == "test"}
        fit = {r["scene"] for r in mine if r["half"] == "fit"}
        assert len(test) == len(fit) == 4
        assert {r["arm"] for r in mine if r["half"] == "test"} == {"none", *G.ARMS, *G.REFIT_ARMS}
        assert {r["arm"] for r in mine if r["half"] == "fit"} == {"none", *G.ARMS}
    rc = [r for r in rows if r["reader"] == X.RECALL]
    assert {r["type"] for r in rc} == {"animals"}  # the fruit recall's gate failed, names have none
    assert {r["scene"] for r in rc} <= fake_run.right_recall and len({r["scene"] for r in rc}) == 8
    refit = json.loads((out / "refit.json").read_text())
    for t in G.TYPES:
        assert 1 <= refit[t]["rank"] <= 2, refit[t]
        assert refit[t]["n_fit"] == refit[t]["n_test"] == 4, refit[t]
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 24 and all(0 <= n["share_alf"] <= 1 and 0 <= n["share_refit"] <= 1 for n in norms)
    m = json.loads((out / "manifest.json").read_text())
    assert m["items"] == {t: 8 for t in G.TYPES} and "sealed" in m and "switches" in m


def test_verdict_and_view_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(A, "dan_answer", lambda question="", rev="HEAD": "yes · 60%")
    monkeypatch.setattr(G, "stored_animals", lambda target, n_boot=0: None)
    out = G.stage_verdict([fake_run.out.name], n_boot=100)
    blob = json.loads((out / "x47_11.json").read_text())
    m = blob["models"][0]
    assert m["status"] == "tested" and m["answer"] in ("yes", "no") and blob["dan"] == "yes · 60%"
    assert set(m["numbers"]) == set(G.TYPES) and set(m["labels"]) == set(G.NEW_TYPES)
    assert m["numbers"]["animals"]["recall"]["n"] == 8 and m["numbers"]["names"]["recall"] is None
    assert m["numbers"]["fruits"]["refit"]["n"] == 4
    assert {x["status"] for x in blob["models"][1:]} == {"pending"}
    md = (out / "x47_11.md").read_text()
    assert "Q47.11" in md and "slot" in md
    view = G.stage_view([fake_run.out.name], decode_for=lambda target: fake_run.tok.decode)
    text = (view / "view.md").read_text()
    # O and S marked per read reader (lookup on 3 x 8 items, the animal recall on 8), plus the header's legend; the fruit
    # recall (its gate failed) is listed as not read
    assert text.count("⟦") == 2 * (8 * 3 + 8) + 1 and "not read" in text


# ---- the rule on planted numbers --------------------------------------------------------------------------------------


def planted_rows(
    kind: str, pos_no_alf: float, pos_rand: float, pos_keep: float, n: int = 100, refit=None
) -> list[dict]:
    """Lookup rows of one type: whole switches to position on 60%; no_alf / no_alf_rand / keep_alf position shares as
    given (the rest identity or original); refit arms on the test half as `refit` = (fall, keep)."""
    rows = []
    for i in range(n):
        half = "test" if i % 2 else "fit"
        arms = {"none": "original", "whole": "position" if i < round(0.6 * n) else "identity",
                "no_alf": "position" if i < round(pos_no_alf * n) else "original",
                "no_alf_rand": "position" if i < round(pos_rand * n) else "original",
                "keep_alf": "position" if i < round(pos_keep * n) else "original", "keep_alf_rand": "original"}  # fmt: skip
        if refit and half == "test":
            fall, keep = refit
            j = i // 2
            arms.update({"no_refit": "position" if j < round((0.6 - fall) * n / 2) else "original",
                         "no_refit_rand": "position" if j < round(0.6 * n / 2) else "original",
                         "keep_refit": "position" if j < round(keep * n / 2) else "original", "keep_refit_rand": "original"})  # fmt: skip
        for a, rt in arms.items():
            rows.append({"scene": f"{kind}{i}", "type": kind, "entity": f"e{i % 10}", "half": half, "reader": X.LOOKUP, "arm": a,
                         "route": rt, "switched": int(rt != "original"), "top": 0, "top_text": "x"})  # fmt: skip
    return rows


def test_type_numbers_and_label_read_planted_falls():
    animals = G.type_numbers(planted_rows("animals", 0.10, 0.55, 0.30), "animals", n_boot=200)
    fruits = G.type_numbers(planted_rows("fruits", 0.15, 0.55, 0.20, refit=(0.4, 0.3)), "fruits", n_boot=200)
    names = G.type_numbers(planted_rows("names", 0.45, 0.55, 0.05, refit=(0.4, 0.3)), "names", n_boot=200)
    assert animals["fixed"]["position_fall"][0] == pytest.approx(0.45)
    assert fruits["fixed"]["position_fall"][0] == pytest.approx(0.40) and fruits["fixed"]["keep_position"][
        0
    ] == pytest.approx(0.20)
    lab_f = G.type_label(fruits, animals, True)
    assert lab_f["holds"] and lab_f["label"].startswith("an address")
    lab_n = G.type_label(names, animals, True)
    assert not lab_n["holds"] and lab_n["clauses"] == {"fall": False, "near_animals": False, "keep": False}
    assert lab_n["refit"]["passes"] and lab_n["label"].startswith("slot x type")
    assert G.type_label(names, animals, False)["status"] == "not tested"
    assert G.type_label(fruits, None, True)["status"] == "not tested"
    # the animal reference far from the new type: within 0.1 fails even with a large fall
    far = G.type_numbers(planted_rows("animals", 0.0, 0.60, 0.30), "animals", n_boot=200)
    assert not G.type_label(fruits, far, True)["clauses"]["near_animals"]


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(G, "RESULTS", tmp_path)
    monkeypatch.setattr(A, "dan_answer", lambda question="", rev="HEAD": "")
    for stage in (lambda: G.stage_verdict([], n_boot=10), lambda: G.stage_view([])):
        with pytest.raises(AssertionError, match="sealed"):
            stage()
    assert list(tmp_path.iterdir()) == []


def test_the_committed_predictions_file_has_the_q47_11_block():
    text = A.subprocess.run(["git", "show", f"HEAD:{G.PREDICTIONS}"], cwd=A.pins.REPO_ROOT, capture_output=True, text=True,
                            check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{G.QUESTION}**" in text and isinstance(A.dan_answer(G.QUESTION), str)


def test_example_prompts_are_seeded():
    assert sorted(random.Random(X.EXAMPLES_SEED).sample(range(300), 10)) == sorted(
        random.Random(0).sample(range(300), 10)
    )
