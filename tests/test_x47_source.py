"""Batch 47, test 47.15 (scripts/x47_source.py): the attribute sentences (false digits distinct, outside the locker digits
and the true legs), the rendering per condition on a fake tokenizer (the bridge index shared by O, S and the three
conditions; an instruction before the passage is refused), the rule on planted numbers at its bars, the sealed verdict,
and the run stage end to end on a tiny fake causal model (CPU). No real model."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_source as Q

LK = X.LOOKUP
# a C2 routes scene: Iris's pick frog -> bee in S; the bee's and the duck's locker sentences swapped, the bee's digit new.
# The locker digits {4, 6, 2, 9} and the true legs (frog 4, bee 6, duck 2) leave {1, 3, 5, 7, 8} for the false digits.
ORG = ("The locker of the frog is 4. The locker of the bee is 6. The locker of the duck is 2. "
       "Iris picked the frog. Noah picked the bee. Sara picked the duck.")  # fmt: skip
ALT = ("The locker of the frog is 4. The locker of the duck is 2. The locker of the bee is 9. "
       "Iris picked the bee. Noah picked the bee. Sara picked the duck.")  # fmt: skip
EXPECT = {"identity": 6, "position": 2, "value": 9, "original": 4}
ANIMALS = ("frog", "bee", "duck", "spider")  # legs 4, 6, 2, 8: consecutive pairs always differ (the generator's rule)


def renamed(text: str, names: tuple[str, str, str]) -> str:
    """ORG / ALT with frog, bee, duck renamed in one pass (so a name already placed is not renamed again)."""
    table: dict[str, str] = dict(zip(("frog", "bee", "duck"), names, strict=True))
    return re.sub(r"\b(frog|bee|duck)\b", lambda m: table[m.group(1)], text)


def legs_of() -> dict[str, int]:
    from scripts import tasks_v2 as T

    return dict(T.DOMAINS["animals"].values)


class WordTok:
    """Words with their leading whitespace as tokens, ids from a shared vocab (as tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids, skip_special_tokens=False) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


def wrap(context: str, question: str) -> str:
    """X0's chat prompt without the template (the instruction after the question, as tasks_v2.render places it)."""
    return f"<|im_start|>user\n{context}\n{question} Answer with a single digit and nothing else.<|im_end|>\nAnswer:"


def render_after(tok, item, rendering, ctx):
    return wrap(ctx, item["question"])


def bridge_index(tok, text: str, asked: str, item: str) -> int:
    enc = tok(text, return_offsets_mapping=True)
    at = text.index(f"{asked} picked the {item}.") + len(f"{asked} picked the ")
    return next(k for k, (a, b) in enumerate(enc.offset_mapping) if a <= at < b)


def base_case(tok, scene: str = "C2-0001") -> dict:
    return {"scene": scene, "condition": "C2", "context": ORG, "cf_context": ALT, "bridge": "frog", "cf_bridge": "bee",
            "expect": EXPECT, "pos": bridge_index(tok, wrap(ORG, R.LOOKUP_Q.format(p="Iris")), "Iris", "frog"),
            "readers": {LK: {"question": R.LOOKUP_Q.format(p="Iris")}}}  # fmt: skip


# ---- the attribute sentences ----------------------------------------------------------------------------------------


def test_attribute_plan_digits_are_distinct_and_outside_lockers_and_legs():
    legs = {"frog": 4, "bee": 6, "duck": 2}
    plan = Q.attribute_plan(ORG, ALT, legs, random.Random("x"))
    assert plan is not None and set(plan["false"]) == {"frog", "bee", "duck"}
    digits = list(plan["false"].values())
    assert len(set(digits)) == 3 and all(1 <= d <= 9 for d in digits)
    assert not set(digits) & {4, 6, 2, 9}  # O's and S's locker digits, and the true legs
    assert set(digits) <= {1, 3, 5, 7, 8}
    assert sorted(plan["order"]) == ["bee", "duck", "frog"]
    assert plan == Q.attribute_plan(ORG, ALT, legs, random.Random("x"))  # seeded


def test_attribute_plan_is_none_when_fewer_than_three_digits_remain():
    o = "The locker of the frog is 1. The locker of the bee is 2. The locker of the duck is 3. Iris picked the frog."
    s = "The locker of the frog is 1. The locker of the duck is 3. The locker of the bee is 4. Iris picked the bee."
    assert Q.attribute_plan(o, s, {"frog": 5, "bee": 6, "duck": 7}, random.Random(0)) is None  # only 8 and 9 remain
    assert Q.attribute_plan(o, s, {"frog": 5, "bee": 6, "duck": 6}, random.Random(0)) is not None  # 7, 8, 9


def test_with_attributes_places_the_sentences():
    attrs = ["The bee has 1 leg.", "The frog has 8 legs.", "The duck has 3 legs."]
    after, before = Q.with_attributes(ORG, attrs, "after"), Q.with_attributes(ORG, attrs, "before")
    lockers, picks = Q.sentences(ORG)[:3], Q.sentences(ORG)[3:]
    assert Q.sentences(after) == lockers + picks + attrs
    assert Q.sentences(before) == lockers + attrs + picks
    assert (
        Q.attribute_sentence("bee", 1) == "The bee has 1 leg."
        and Q.attribute_sentence("frog", 8) == "The frog has 8 legs."
    )
    assert Q.locker_slots(ALT) == [("frog", 4), ("duck", 2), ("bee", 9)]


# ---- the rendering per condition -------------------------------------------------------------------------------------


@pytest.fixture
def fake_tok(monkeypatch):
    monkeypatch.setattr(X, "render", render_after)
    tok = WordTok()
    for d in range(10):
        tok(str(d))
    return tok


def test_encode_keeps_the_bridge_index_across_conditions(fake_tok):
    tok = fake_tok
    attrs = ["The bee has 1 leg.", "The frog has 8 legs.", "The duck has 3 legs."]
    answers = {"text": (8, 1), "memory": (4, 6)}
    for placement in Q.PLACEMENTS:
        o, s = Q.with_attributes(ORG, attrs, placement), Q.with_attributes(ALT, attrs, placement)
        c, why = Q.encode(tok, o, s, "Iris", "frog", "bee", answers, "C2-0001", placement)
        assert c is not None, why
        c.update({"legs": {"frog": 4, "bee": 6, "duck": 2}, "false": {"frog": 8, "bee": 1, "duck": 3},
                  "base_pos": bridge_index(tok, wrap(ORG, R.LOOKUP_Q.format(p="Iris")), "Iris", "frog")})  # fmt: skip
        Q.check_case(c)
        rd = c["readers"]
        assert set(rd) == set(Q.CONDS) and c["pos"] == bridge_index(
            tok, wrap(o, rd["none"]["question"]), "Iris", "frog"
        )
        assert (
            tok.decode([rd["none"]["ids"]["org"][c["pos"]]]) == " frog."
            and tok.decode([rd["none"]["ids"]["alt"][c["pos"]]]) == " bee."
        )
        # the no-instruction prompt is the routes recall prompt on the extended passage; the instructed ones add the
        # instruction after the question: longer prompts, the same bridge index, a later read index
        assert tok.decode(rd["none"]["ids"]["org"]) == wrap(o, R.RECALL_Q.format(p="Iris"))
        assert rd["text"]["question"] == "How many legs does Iris's pick have? Answer using only the passage."
        assert (
            rd["memory"]["question"]
            == "How many legs does Iris's pick have? Ignore the passage; answer from what you know."
        )
        assert (
            rd["text"]["read_index"] > rd["none"]["read_index"]
            and rd["memory"]["read_index"] > rd["none"]["read_index"]
        )
        for cond in Q.CONDS:
            assert rd[cond]["read_index"] == len(rd[cond]["ids"]["org"]) == len(rd[cond]["ids"]["alt"])
        assert (rd["text"]["answer"], rd["text"]["cf_answer"]) == ("8", "1")
        assert (rd["memory"]["answer"], rd["memory"]["cf_answer"]) == ("4", "6")
        assert rd["text"]["tokens"]["memory"]["alt"] == rd["memory"]["tok_b"] == tok("6").input_ids[0]
        if placement == "after":
            assert c["pos"] == c["base_pos"]  # the attribute sentences come after the bridge
        else:
            assert c["pos"] == c["base_pos"] + 15  # three sentences of five words before the picks


def test_encode_refuses_an_instruction_before_the_passage(fake_tok, monkeypatch):
    """Dumbest way 1: an instruction placed before the passage moves the bridge between conditions; encode says so."""

    def render_before(tok, item, rendering, ctx):
        q, _, instr = item["question"].partition("? ")
        return (
            wrap(ctx, q + "?")
            if not instr
            else f"<|im_start|>user\n{instr}\n{ctx}\n{q}? Answer with a single digit and nothing else.<|im_end|>\nAnswer:"
        )

    monkeypatch.setattr(X, "render", render_before)
    attrs = ["The bee has 1 leg.", "The frog has 8 legs.", "The duck has 3 legs."]
    c, why = Q.encode(fake_tok, Q.with_attributes(ORG, attrs, "after"), Q.with_attributes(ALT, attrs, "after"), "Iris",
                      "frog", "bee", {"text": (8, 1), "memory": (4, 6)}, "C2-0001", "after")  # fmt: skip
    assert c is None and why == "the conditions' bridge positions differ"


def test_build_pairs_the_placements_and_checks_every_case(fake_tok, monkeypatch):
    tok = fake_tok
    bases = [base_case(tok, "C2-0001"), base_case(tok, "C2-0002"), {**base_case(tok, "C0-0001"), "condition": "C0"}]
    monkeypatch.setattr(R, "scenes", lambda tok_, n, seed=R.SEED, rendering="chat": (bases, {}))
    cases, dropped = Q.build(tok, 3)
    assert not dropped and [c["scene"] for c in cases] == [
        "C2-0001-after",
        "C2-0001-before",
        "C2-0002-after",
        "C2-0002-before",
    ]
    legs = legs_of()
    for c in cases:
        Q.check_case(c)
        assert c["legs"] == {x: legs[x] for x in ("frog", "bee", "duck")} and c["locker_order"] == [
            "frog",
            "bee",
            "duck",
        ]
        assert c["answers"] == {"text": [c["false"]["frog"], c["false"]["bee"]], "memory": [legs["frog"], legs["bee"]]}
        assert all(Q.attribute_sentence(x, c["false"][x]) in c["context"] for x in c["false"])
        assert (
            c["context"].replace("Iris picked the frog.", "Iris picked the bee.") != c["cf_context"]
        )  # C2: lockers differ too
    a, b = cases[0], cases[1]
    assert a["false"] == b["false"] and a["attribute_order"] == b["attribute_order"]  # the same draw per base scene
    assert a["pos"] == a["base_pos"] and b["pos"] == a["pos"] + 15


# ---- the rule --------------------------------------------------------------------------------------------------------


def num(j: float, u: float, valid: bool = True) -> dict:
    return {"valid": valid, "extra": {"jpp": [j, j - 0.1, j + 0.1], "ui": [u, u - 0.1, u + 0.1]}}


def test_label_at_the_bars():
    assert Q.label(num(0.10, 0.30)) == "lookup" and Q.label(num(0.10 + 1e-12, 0.30 - 1e-12)) == "lookup"
    assert Q.label(num(0.30, 0.10)) == "recall" and Q.label(num(0.11, 0.30)) == "neither"
    assert Q.label(num(0.2, 0.2)) == "neither" and Q.label(num(0.0, 0.0)) == "neither"
    assert Q.label(num(0.0, 0.9, valid=False)) == "can't tell"


def test_model_and_batch_rule():
    assert Q.model_rule({"text": "lookup", "memory": "recall"})["verdict"] == "follows the source"
    assert Q.model_rule({"text": "recall", "memory": "recall"})["verdict"] == "follows the question"
    assert Q.model_rule({"text": "lookup", "memory": "lookup"})["verdict"] == "follows the question"
    assert Q.model_rule({"text": "neither", "memory": "neither"})["verdict"] == "neither"
    assert Q.model_rule({"text": "recall", "memory": "lookup"})["verdict"] == "neither"
    tested = lambda v: {"status": "tested", "verdict": v}  # noqa: E731
    pend = {"status": "pending"}
    assert (
        Q.batch_rule([tested("follows the source"), tested("follows the source"), tested("neither")])["label"]
        == "follows the source"
    )
    assert (
        Q.batch_rule([tested("follows the question"), tested("follows the question"), pend])["label"]
        == "follows the question"
    )
    assert Q.batch_rule([tested("follows the source"), pend, pend])["label"] == "pending"
    assert (
        Q.batch_rule([tested("follows the source"), tested("neither"), tested("follows the question")])["label"]
        == "neither"
    )
    assert Q.batch_rule([tested("follows the source"), tested("follows the question"), pend])["label"] == "pending"


def test_numbers_read_planted_extra_losses():
    n = 120
    ents = [f"e{i % 30}" for i in range(n)]
    sw = {a: [1] * n for a in Q.ARMS}
    sw["no_jpp"] = [i % 2 for i in range(n)]  # half the switches lost without J++, none without its random part
    sw["no_ui"] = [0] * n  # every switch lost without U + I
    r = Q.numbers(sw, ents, n_boot=500)
    assert r["n"] == n and r["entities"] == 30 and r["valid"]
    assert r["rate"]["whole"][0] == 1.0 and r["extra"]["jpp"][0] == pytest.approx(0.5) and r["extra"]["ui"][0] == 1.0
    assert r["extra"]["jpp"][1] > 0.3 and r["loss"]["jpp"]["no_rand"][0] == 0.0
    assert Q.label(r) == "neither"
    sw["no_jpp"] = [1] * n
    r = Q.numbers(sw, ents, n_boot=200)
    assert Q.label(r) == "lookup"
    sw["whole"] = [int(i < 20) for i in range(n)]  # 20 switches: an invalid cell
    assert not Q.numbers(sw, ents, n_boot=100)["valid"]


def test_item_table_needs_every_arm():
    rows = [{"scene": "s1", "placement": "after", "reader": "text", "arm": a, "entity": "e", "switched_text": 1,
             "switched_memory": 0} for a in Q.ARMS[:-1]]  # fmt: skip
    with pytest.raises(AssertionError, match="missing"):
        Q.item_table(rows, "after", "text", "text")
    rows.append({**rows[0], "arm": "source"})
    scenes, ents, sw = Q.item_table(rows, "after", "text", "memory")
    assert scenes == ["s1"] and ents == ["e"] and all(v == [0] for v in sw.values())


# ---- the run stage on a fake model (CPU) and the sealed verdict -------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (as tests/test_x45p.py): each block mixes the running mean
    of the positions so far into every position; an edit acts on a block's output."""

    def __init__(self, tok: WordTok, vocab: int, n_layers: int = 33, d: int = 32):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.device = tok, n_layers, torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()
        self.calls: list[tuple[int, list[dict]]] = []

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
        self.calls.append((ids.shape[1], edits))
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return list(range(64))


class FakeLens:
    def __init__(self, model, name):
        assert name == "jpp"

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def fake_competence(model, cases, ws, decode):
    """Everything right under both instructions; with no instruction, O and S answer from the text on even base
    scenes and from memory on odd ones (one scene answers 'other' on S)."""
    rows = []
    for c in cases:
        k = int(c["base_scene"].split("-")[1])
        cls = "text" if k % 2 == 0 else "memory"
        for cond in Q.CONDS:
            for v in ("org", "alt"):
                row = {"scene": c["scene"], "base_scene": c["base_scene"], "placement": c["placement"], "reader": cond,
                       "variant": v, "greedy": "7", "said": "7", "no_digit": False, "top": 0, "top_text": "7",
                       "class": cond if cond != "none" else ("other" if k == 3 and v == "alt" else cls), "said_class": cond}  # fmt: skip
                if cond in Q.INSTRUCTED:
                    row.update({"right": True, "read_right": True})
                rows.append(row)
    return rows


@pytest.fixture
def fake_run(tmp_path, monkeypatch, fake_tok):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    tok = fake_tok
    bases = []
    for i in range(12):
        names = (ANIMALS[i % 4], ANIMALS[(i + 1) % 4], ANIMALS[(i + 2) % 4])
        o, s = renamed(ORG, names), renamed(ALT, names)
        bases.append({"scene": f"C2-{i:04d}", "condition": "C2", "context": o, "cf_context": s, "bridge": names[0],
                      "cf_bridge": names[1], "expect": EXPECT,
                      "pos": bridge_index(tok, wrap(o, R.LOOKUP_Q.format(p="Iris")), "Iris", names[0]),
                      "readers": {LK: {"question": R.LOOKUP_Q.format(p="Iris")}}})  # fmt: skip
    g = torch.Generator().manual_seed(3)
    alf, _ = torch.linalg.qr(torch.randn(32, 4, generator=g))
    means = {x: torch.randn(32, generator=g).numpy() for x in ANIMALS if x != "spider"}  # the spider: no class mean
    fake = FakeModel(tok, vocab=256)
    monkeypatch.setattr(R, "scenes", lambda tok_, n, seed=R.SEED, rendering="chat": (bases, {}))
    monkeypatch.setattr(R, "pools", lambda tok_: (legs_of(), list(ANIMALS), ["Iris", "Noah", "Sara"]))
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(MM, "entity_means", lambda run: means)
    monkeypatch.setattr(MM, "subspaces", lambda run: ({"Alf": alf.numpy().astype(np.float64)}, {}))
    monkeypatch.setattr(Q, "competence", fake_competence)
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x47_source")
    name = f"{pins.RUN_PREFIX}fake_x47_15"
    monkeypatch.setitem(Q.RUNS, pins.TARGET, name)
    out = Q.stage_run(name, "test", n_gen=12, n_items=5)
    return SimpleNamespace(tok=tok, fake=fake, out=out, name=name, alf=alf, means=means)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    from bridge_jspace import pins
    from scripts import statement_positions as SP

    out, fake = fake_run.out, fake_run.fake
    m = json.loads((out / "manifest.json").read_text())
    g = json.loads((out / "gate.json").read_text())
    la = X.PREDICTED[pins.TARGET]
    assert m["layer"] == la and m["test"] == "47.15" and "sealed" in m and m["items"] == {"after": 5, "before": 5}
    # 12 base scenes x 2 placements; scenes with the spider (no class mean) are dropped before the first 5 are chosen
    assert g["gate"]["after"]["pass"] and g["gate"]["after"]["cases"] == 12 and g["identity_dropped"]["after"] > 0
    assert g["gate"]["after"]["follows"]["text"]["org"]["instructed"] == 1.0
    cases = X.read_jsonl(out / "cases.jsonl")
    chosen = [c for c in cases if c["chosen"]]
    assert len(cases) == 24 and len(chosen) == 10 and all("spider" not in (c["bridge"], c["cf_bridge"]) for c in chosen)
    assert all(c["unedited_class"]["none"]["org"] in ("text", "memory") for c in chosen)
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (c["scene"], w, a) for c in chosen for w in Q.CONDS for a in Q.ARMS
    }
    assert all(r["switched"] is None for r in rows if r["reader"] == "none")
    assert all(r["switched"] == r[f"switched_{r['reader']}"] for r in rows if r["reader"] != "none")
    assert all(r["answer"] in Q.ANSWERS for r in rows)
    assert not any(p.name.startswith("x47_15") for p in out.iterdir())  # sealed: no verdict in the run
    # the first read of the first chosen item: its text reader's O with the arms in order, then S alone
    it = chosen[0]
    seq, edits = fake.calls[0]
    assert seq == len(it["readers"]["text"]["ids"]["org"]) and edits[0] == {} and len(edits) == 1 + len(Q.EDIT_ARMS)
    e = {arm: edit[la] for arm, edit in zip(Q.EDIT_ARMS, edits[1:], strict=True)}
    assert all(v.positions == [it["pos"]] for v in e.values())
    h = {
        v: fake.run(torch.tensor([it["readers"]["none"]["ids"][v]]), record=(la,))[1][la][it["pos"]]
        for v in ("org", "alt")
    }
    whole = h["alt"] - h["org"]
    jdic = FakeLens(None, "jpp").vectors(la, list(range(64)))
    assert torch.allclose(e["whole"].delta[0], whole)
    assert torch.allclose(e["no_jpp"].delta[0], whole - X.fit(jdic, whole[None], 25, "signed")[0], atol=1e-5)
    for part in ("jpp", "ui"):  # the part and the rest add up to the whole; the random twin has the part's share
        assert torch.allclose(e[f"keep_{part}"].delta[0] + e[f"no_{part}"].delta[0], whole, atol=1e-5)
        assert torch.allclose(e[f"keep_{part}_rand"].delta[0] + e[f"no_{part}_rand"].delta[0], whole, atol=1e-5)
    # the U + I part holds the pointer directions' component and more
    ptr = fake_run.alf @ (fake_run.alf.T @ whole)
    keep_ui = e["keep_ui"].delta[0]
    assert keep_ui.norm() >= ptr.norm() - 1e-5 and torch.allclose(
        fake_run.alf.T @ (whole - keep_ui), torch.zeros(4), atol=1e-4
    )
    basis = SP.random_basis(32, torch.Generator().manual_seed(X.SUBSPACE_SEED + la))
    share = (X.fit(jdic, whole[None], 25, "signed")[0].norm() ** 2 / whole.norm() ** 2)[None]
    assert torch.allclose(e["keep_jpp_rand"].delta[0], SP.random_subspace_part(whole[None], share, basis)[0], atol=1e-5)
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 10 and all(0 <= n["share_ui"] <= 1 and n["share_ui"] >= n["share_alf"] - 1e-4 for n in norms)
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == 2 * 5 * len(Q.CONDS) * len(Q.ARMS)  # both placements


def test_competence_lines_on_the_fake_run(fake_run):
    lines = Q.competence_lines(fake_run.name)
    assert any("| after | 12 | 1.000 | 1.000 | yes | 12 |" in ln for ln in lines)
    assert any("| after | memory | O | 12 | 1.000 | 0.000 | 0.000 | 0.000 |" in ln for ln in lines)


def test_verdict_is_sealed_until_dans_answer(fake_run, monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_verdict([fake_run.name], n_boot=50)


def test_verdict_stage_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "follows the source · 60%")
    out = Q.stage_verdict([fake_run.name], n_boot=100, decode_for=lambda target: fake_run.tok.decode)
    v = json.loads((out / "x47_15.json").read_text())
    assert v["dan"].startswith("follows the source") and len(v["models"]) == 3
    mine = v["models"][0]
    assert mine["status"] == "tested" and mine["verdict"] in ("follows the source", "follows the question", "neither")
    after = mine["placements"]["after"]
    assert set(after["conditions"]) == {"text", "memory"} and after["conditions"]["text"]["n"] == 5
    assert after["none"]["classes"]["org"]["n"] == 5 and after["none"]["classes"]["prefers"] in (
        "text",
        "memory",
        "tie",
    )
    assert after["none"]["text"]["n"] + after["none"]["memory"]["n"] <= 5
    assert [m["status"] for m in v["models"][1:]] == ["pending", "pending"] and v["batch"]["label"] in (
        "pending",
        "neither",
    )
    md = (out / "x47_15.md").read_text()
    assert "Rule (fixed in advance)" in md and "| after | text |" in md and "| before | memory |" in md
    ex = (out / "examples.md").read_text()
    assert ex.count("### C2-") == 5 and "⟦" in ex and "| source |" in ex


def test_dan_answer_reads_the_q47_15_block(monkeypatch):
    from scripts import x47_atoms as A

    text = "**Q47.14** x\n\nDan: yes\n\n**Q47.15** y\n\nRule: r.\n\nDan:\n\n**Q47.16** z\n\nDan: no\n"
    monkeypatch.setattr(A.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=text))
    assert Q.dan_answer() == ""
    monkeypatch.setattr(
        A.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(stdout=text.replace("Dan:\n\n**Q47.16", "Dan: text · 70%\n\n**Q47.16")),
    )
    assert Q.dan_answer() == "text · 70%"
