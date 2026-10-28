"""Batch 47, test 47.10 (scripts/x47_report.py): the report prompts and answers (a fake tokenizer; the target's tokenizer
when cached: ordinal words one token, the two question orders, the bridge position, X0's lookup and recall prompts
reproduced), the no_jpp dictionary with digit atoms (the letter-only restriction lifted), the lens ranks, the gate per
reader on its own prompt, the cells, the rule on planted numbers and the seal (CPU). No real model."""

import re
from types import SimpleNamespace

import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_report as Q

LOCKERS = "The locker of the frog is 5. The locker of the bee is 3. The locker of the tick is 2."
ORG = f"{LOCKERS} Noah picked the tick. Iris picked the frog. Peter picked the bee."
ALT = ORG.replace("Iris picked the frog.", "Iris picked the bee.")


class WordTok:
    """Words with their leading whitespace as tokens (as byte-level BPE attaches a space), ids from a shared vocab
    (copied from tests/test_x45b_binding.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


def fake_prompt(tok, context, question, kind, order):
    """The prompt shapes without a chat template: question-last as tasks_v2 orders them, question-first reversed."""
    instr = "(digit)" if kind == "digit" else "(word)"
    body = f"{context}\n{question} {instr}" if order == "last" else f"{question} {instr}\n{context}"
    return f"<|im_start|>user\n{body}<|im_end|>\nAnswer:"


def fake_case(tok, org=ORG, alt=ALT, bridge="frog", cf_bridge="bee") -> dict:
    """A routes C0 case whose lookup and recall ids come from fake_prompt (as build_item asserts)."""
    readers = {}
    for key, q, ans in ((X.LOOKUP, R.LOOKUP_Q, ("5", "3")), (X.RECALL, R.RECALL_Q, ("4", "6"))):
        ids = {v: tok(fake_prompt(tok, ctx, q.format(p="Iris"), "digit", "last")).input_ids
               for v, ctx in (("org", org), ("alt", alt))}  # fmt: skip
        readers[key] = {"question": q.format(p="Iris"), "answer": ans[0], "cf_answer": ans[1], "ids": ids}
    return {"scene": "C0-0001", "condition": "C0", "domain": "animals", "bridge": bridge, "cf_bridge": cf_bridge,
            "context": org, "cf_context": alt, "readers": readers}  # fmt: skip


# ---- scenes and prompts -------------------------------------------------------------------------------------------


def test_locker_slots_and_pick_index():
    assert Q.locker_slots(ORG) == {"frog": 0, "bee": 1, "tick": 2}
    assert Q.pick_index(ORG, "Iris") == 4 and Q.pick_index(ORG, "Noah") == 3


def test_build_item_answers_track_the_slot_and_the_orders(monkeypatch):
    monkeypatch.setattr(Q, "prompt", fake_prompt)
    tok = WordTok()
    it, why = Q.build_item(tok, fake_case(tok))
    assert it is not None, why
    assert it["slot"] == {"org": 0, "alt": 1} and it["entity"] == "frog" and it["cf_bridge"] == "bee"
    last = it["orders"]["last"]["readers"]
    assert (last["report"]["answer"], last["report"]["cf_answer"]) == ("first", "second")
    assert (last["report_digit"]["answer"], last["report_digit"]["cf_answer"]) == ("1", "2")
    assert (last["lookup"]["answer"], last["lookup"]["cf_answer"]) == ("5", "3")
    assert (
        last["report"]["tok_A"] == tok(" first").input_ids[0] and last["report_digit"]["tok_A"] == tok("1").input_ids[0]
    )
    # question-last: one bridge position and one prefix for the four prompts; the bridge is the item's token
    pos = last["lookup"]["pos"]
    assert all(rd["pos"] == pos for rd in last.values()) and it["orders"]["last"]["shared_prefix"]
    assert all(rd["ids"]["org"][: pos + 1] == last["lookup"]["ids"]["org"][: pos + 1] for rd in last.values())
    # the fake tokenizer keeps the period in the word's token (" frog."); the real one splits it off
    assert tok.decode([last["report"]["ids"]["org"][pos]]) == " frog."
    assert tok.decode([last["report"]["ids"]["alt"][pos]]) == " bee."
    assert last["report"]["text"]["org"].index(ORG) < last["report"]["text"]["org"].index("Was the locker")
    # question-first: the question before the context, each reader its own position, the bridge still one token
    first = it["orders"]["first"]["readers"]
    assert not it["orders"]["first"]["shared_prefix"]
    assert first["report"]["text"]["org"].index("Was the locker") < first["report"]["text"]["org"].index(ORG)
    assert first["report"]["pos"] != first["lookup"]["pos"] and first["report"]["pos"] > pos
    assert tok.decode([first["report"]["ids"]["org"][first["report"]["pos"]]]) == " frog."
    assert len(first["report"]["ids"]["org"]) == len(first["report"]["ids"]["alt"])


def test_build_item_control_scene_where_the_pick_is_not_the_first_locker(monkeypatch):
    monkeypatch.setattr(Q, "prompt", fake_prompt)
    tok = WordTok()
    org = f"{LOCKERS} Noah picked the frog. Iris picked the tick. Peter picked the bee."
    alt = org.replace("Iris picked the tick.", "Iris picked the frog.")
    it, why = Q.build_item(tok, fake_case(tok, org, alt, "tick", "frog"))
    assert it is not None, why
    assert it["slot"] == {"org": 2, "alt": 0}
    rd = it["orders"]["last"]["readers"]["report"]
    assert (rd["answer"], rd["cf_answer"]) == ("third", "first")


def test_build_item_refuses_a_bridge_that_is_not_one_token(monkeypatch):
    monkeypatch.setattr(Q, "prompt", fake_prompt)
    tok = WordTok()
    c = fake_case(tok)
    c["cf_context"] = c["cf_context"] + " Nobody picked the frog."  # O and S differ in length
    for key in c["readers"]:
        c["readers"][key]["ids"]["alt"] = tok(
            fake_prompt(tok, c["cf_context"], c["readers"][key]["question"], "digit", "last")
        ).input_ids
    it, why = Q.build_item(tok, c)
    assert it is None and "not one token" in why


def test_said_ordinal_and_the_word_reader():
    assert Q.said_ordinal("second") == "second" and Q.said_ordinal(" Third.\nmore") == "third"
    assert Q.said_ordinal("the first one") == "first" and Q.said_ordinal("2") == "second"
    assert Q.said_ordinal("fourth") is None and Q.said_ordinal("") is None
    assert Q.said("first", "word") == "first" and Q.said("two", "digit") == "2"


def _real_tokenizer():
    from scripts import statement_positions as SP

    try:
        return SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


def test_report_prompts_on_the_targets_tokenizer():
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    tok = _real_tokenizer()
    for w, sp in Q.ordinal_tokens(tok).items():
        assert all(v is not None for v in sp.values()), f"{w}: {sp}"  # one token in every spelling
    ords = Q.answer_ids(tok)
    assert [ords[w][0] for w in Q.ORDINALS] == [S.ids(tok, " " + w)[0] for w in Q.ORDINALS]
    assert Q.suffix(tok, "digit") == S.ids(tok, " ") and Q.suffix(tok, "word") == []
    cases, _ = R.scenes(tok, 3)
    items = [Q.build_item(tok, c) for c in cases if c["condition"] == "C0"]
    assert items and all(it is not None for it, _ in items)
    for it, _ in items:
        rd = it["orders"]["last"]["readers"]["report"]
        assert rd["text"]["org"] == T.render(
            tok, {"format": "prose", "kind": "word", "context": it["context"], "question": rd["question"]}
        )
        assert (
            S.INSTRUCTION in rd["text"]["org"]
            and T.DIGIT_INSTRUCTION in it["orders"]["last"]["readers"]["report_digit"]["text"]["org"]
        )
        first = it["orders"]["first"]["readers"]["report"]["text"]["org"]
        assert first.index(rd["question"]) < first.index(it["context"]) and first.endswith("Answer:")
        assert rd["answer"] == Q.ORDINALS[it["slot"]["org"]] and rd["tok_A"] == ords[rd["answer"]][0]
        for order in Q.ORDERS:
            for r in it["orders"][order]["readers"].values():
                assert tok.decode([r["ids"]["org"][r["pos"]]]).strip() == it["entity"]
                assert tok.decode([r["ids"]["alt"][r["pos"]]]).strip() == it["cf_bridge"]


# ---- the dictionary, the lens ranks ---------------------------------------------------------------------------------


def test_dictionary_lifts_the_letter_only_restriction():
    letters, digits = torch.arange(0, 10), torch.arange(20, 30)
    ids = Q.dictionary_ids(letters, digits)
    assert ids.tolist() == [*range(10), *range(20, 30)]  # the digit atoms are in the dictionary
    with pytest.raises(AssertionError):
        Q.dictionary_ids(torch.arange(0, 10), torch.arange(5, 15))


def test_atom_report_names_present_and_absent_ordinal_atoms():
    tok = WordTok()
    ids = {sp: tok(sp).input_ids[0] for w in Q.ORDINALS for sp in Q.spellings(w)}
    digits = [tok(str(d)).input_ids[0] for d in range(10)]
    atoms = [ids[" first"], ids["first"], ids[" second"], ids[" third"], *digits]  # no capitalised spellings
    rep = Q.atom_report(tok, atoms, digits)
    assert rep["atoms"] == len(atoms)
    assert rep["ordinal_atoms_present"] == sorted([" first", "first", " second", " third"])
    assert set(rep["ordinal_spellings_absent"]) == {sp for sp in ids if sp not in rep["ordinal_atoms_present"]}
    assert rep["digit_atoms"] == {str(d): 4 + d for d in range(10)}
    assert rep["ordinal_atoms"]["first"][" first"] == {"id": ids[" first"], "atom": 0}


def test_lens_ranks_on_a_planted_readout():
    lg = torch.zeros(50)
    ords = {"first": [1, 2], "second": [3], "third": [4]}
    slot_digits = {"1": 10, "2": 11, "3": 12}
    lg[3], lg[40], lg[11], lg[13], lg[49] = 5.0, 4.0, 3.0, 2.0, 9.0  # token 49 is special: masked out
    decode = lambda ids: str(ids[0])  # noqa: E731
    r = Q.lens_ranks(lg, {"org": 1, "alt": 0}, ords, slot_digits, 13, [49], decode)
    assert r["rank_ordinal"] == 1 and r["top5_ordinal"] == 1 and r["rank_ordinal_among3"] == 1
    assert r["rank_digit"] == 3 and r["top5_digit"] == 1 and r["rank_digit_among_digits"] == 1
    assert r["rank_value_digit"] == 4 and r["rank_ordinal_alt"] == 5  # four tokens above the tied 'first' spellings
    assert r["top20"][:4] == ["3", "40", "11", "13"] and "49" not in r["top20"]
    r = Q.lens_ranks(lg, {"org": 0, "alt": 1}, ords, slot_digits, 13, [], decode)
    assert r["rank_ordinal"] == 6 and r["top5_ordinal"] == 0 and r["rank_ordinal_among3"] == 2  # ties rank above


# ---- the gate, the cells, the rule ----------------------------------------------------------------------------------


def _items(n: int) -> list[dict]:
    return [{"scene": f"s{i}", "entity": f"e{i % 7}", "slot": {"org": i % 3, "alt": (i + 1) % 3}} for i in range(n)]


def test_gate_per_reader_on_its_own_prompt_and_by_slot():
    items = _items(30)
    comp = []
    for it in items:
        for order in Q.ORDERS:
            for w in Q.READERS:
                for v in ("org", "alt"):
                    # the report misses every third-slot item in the question-first order (reads "first")
                    wrong = order == "first" and w == "report" and it["slot"][v] == 2
                    comp.append({"scene": it["scene"], "order": order, "reader": w, "variant": v, "slot": it["slot"][v],
                                 "right": not wrong, "read_right": not wrong})  # fmt: skip
    gate, chosen = Q.gate_of(items, comp, Q.ORDERS, 0.8, 20)
    assert gate["last"]["pass"] and gate["last"]["failed"] == [] and len(chosen["last"]) == 20
    assert gate["last"]["eligible"] == 30 and gate["last"]["chosen"] == 20
    assert not gate["first"]["pass"] and gate["first"]["failed"] == ["report"] and chosen["first"] == []
    acc = gate["first"]["org_read_accuracy"]
    assert acc["report"] == pytest.approx(20 / 30) and acc["lookup"] == 1.0
    by = gate["first"]["report_read_accuracy_by_true_slot"]["report"]
    assert by["1"] == [1.0, 10] and by["2"] == [1.0, 10] and by["3"] == [0.0, 10]


def _rows(n: int, switched: dict[str, int], reader: str = "report", order: str = "last") -> list[dict]:
    return [{"scene": f"s{i}", "entity": f"e{i % 7}", "order": order, "reader": reader, "arm": a,
             "switched": switched.get(a, 0), "right": int(a == "none")} for i in range(n) for a in Q.ARMS]  # fmt: skip


def test_reader_cells_read_planted_losses():
    rows = _rows(60, {"whole": 1, "no_jpp": 0, "no_jpp_rand": 1, "no_alf": 1, "no_alf_rand": 1, "keep_alf": 1})
    c = Q.reader_cells(rows, "last", "report", n_boot=200)
    assert c["n"] == 60 and c["switches_whole"] == 60 and c["right_unedited"] == 1.0
    assert c["jpp"]["excess"][0] == pytest.approx(1.0) and c["alf"]["excess"][0] == pytest.approx(0.0)
    assert c["jpp"]["Jdep"][0] == pytest.approx(1.0) and c["jpp"]["Rdep"][0] == pytest.approx(0.0)
    assert c["keep_alf_minus_rand"][0] == pytest.approx(1.0) and c["rate"]["none"][0] == 0.0
    with pytest.raises(AssertionError, match="missing"):
        Q.reader_cells(rows[:-1], "last", "report", n_boot=50)


def test_lens_shares_count_top5_and_first_among():
    rows = [{"scene": f"s{i}", "entity": f"e{i % 5}", "order": "first", "reader": "report", "source": "report",
             "top5_ordinal": int(i % 2 == 0), "top5_digit": 0, "rank_ordinal_among3": 1 if i % 4 == 0 else 2,
             "rank_digit_among_digits": 3, "rank_ordinal_alt": 9, "rank_value_digit": 1, "rank_ordinal": 2 + i % 3,
             "rank_digit": 7} for i in range(40)]  # fmt: skip
    s = Q.lens_shares(rows, "first", "report", n_boot=100)
    assert s["n"] == 40 and s["top5_ordinal"][0] == 0.5 and s["first_among_ordinals"][0] == 0.25
    assert s["top5_digit"][0] == 0.0 and s["top5_value_digit"][0] == 1.0 and s["median_rank_ordinal"] == 3


def test_rule_on_planted_numbers():
    ok = {"gate_ok": True, "n_switches": {"report": 80, "lookup": 90}}
    assert Q.rule(0.45, 0.05, 0.35, 0.05, 0.1, **ok)["label"] == "surfaced"
    assert Q.rule(0.4, 0.1, 0.3, 0.1, 0.0, **ok)["label"] == "surfaced"  # at the bars
    assert Q.rule(0.45, 0.15, 0.35, 0.05, 0.1, **ok)["label"] == "neither"  # the lookup prompt reads it too
    assert Q.rule(0.45, 0.05, 0.35, 0.2, 0.1, **ok)["label"] == "neither"  # the lookup loses too
    assert Q.rule(0.05, 0.05, 0.05, 0.05, 0.4, **ok)["label"] == "late"
    assert Q.rule(0.1, 0.1, 0.1, 0.0, 0.3, **ok)["label"] == "late"  # at the bars
    assert Q.rule(0.05, 0.05, 0.2, 0.05, 0.4, **ok)["label"] == "neither"  # J++ loss between the bars
    assert Q.rule(0.05, 0.05, 0.05, 0.05, 0.1, **ok)["label"] == "neither"  # U not needed either
    assert Q.rule(0.45, 0.05, 0.35, 0.05, 0.1, gate_ok=False)["label"] == "not tested"
    r = Q.rule(0.45, 0.05, 0.35, 0.05, 0.1, True, {"report": 12, "lookup": 90})
    assert r["label"] == "not tested" and "12" in r["why"]
    assert set(Q.LABELS) == {"surfaced", "late", "neither", "not tested"}


# ---- the seal -----------------------------------------------------------------------------------------------------


def fake_git(text: str):
    def run(cmd, **_):
        assert cmd[:2] == ["git", "show"]
        return SimpleNamespace(stdout=text)

    return run


def test_dan_answer_reads_only_the_q47_10_block(monkeypatch):
    blocks = "**Q47.8** x\n\nDan: yes\n\n**Q47.10** (47.10) ...\n\nRule: ...\n\nDan:{}\n\n**Q47.11** y\n\nDan: no\n"
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format("")))
    assert Q.dan_answer() == ""
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format(" 27B: reported late · 60%")))
    assert Q.dan_answer() == "27B: reported late · 60%"
    monkeypatch.setattr(Q.subprocess, "run", fake_git("no block"))
    assert Q.dan_answer() == ""


def test_verdict_view_and_figures_are_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_verdict(["x47_report_27b"], n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_view("x47_report_27b")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_figures(tmp_path)


def test_the_committed_predictions_file_has_the_q47_10_block():
    from bridge_jspace import pins

    text = (pins.REPO_ROOT / Q.PREDICTIONS).read_text()
    assert f"**{Q.QUESTION}**" in text and "surfaced on demand" in text and "reported late" in text


def test_verdict_on_a_pending_run_set(monkeypatch, tmp_path):
    monkeypatch.setattr(Q, "dan_answer", lambda: "27B: neither · 50%")
    monkeypatch.setattr(Q, "RESULTS", tmp_path)
    out = Q.stage_verdict([], n_boot=10)
    text = (out / "x47_10.md").read_text()
    assert text.count("pending") == 3 and "Dan: 27B: neither · 50%" in text


# ---- the run stage on a fake model ------------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (as tests/test_x45p.py): each block mixes the running mean
    of the positions so far into every position; an edit acts on a block's output, as Model's hooks do."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 32, vocab: int = 512):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.vocab = tok, n_layers, vocab
        self.device = torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

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
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return torch.tensor([i for s, i in self.tokenizer.vocab.items() if re.search(r"[^\W\d_]", s)])


class FakeLens:
    def __init__(self, model, name):
        assert name == "jpp"
        self.model = model

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)

    def readout(self, h, layer):
        return h.float() @ self.model.unemb.T


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    import numpy as np

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    tok = WordTok()
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Q, "prompt", fake_prompt)
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x47_report")
    monkeypatch.setattr(MM, "subspaces", lambda run: ({"Alf": np.eye(32)[:, :4]}, {}))
    monkeypatch.setattr(R, "c0_reference", lambda target: 0.5)

    def fake_items(tok_, n_gen, orders):
        cases = []
        for i in range(n_gen):
            c = fake_case(tok_)
            c["scene"] = f"C0-{i:04d}"
            cases.append(c)
        items = [Q.build_item(tok_, c, orders)[0] for c in cases]
        for i, it in enumerate(items):
            it["entity"] = f"e{i % 6}"  # six bridge entities for the cluster bootstrap and the probe's folds
        return items, {"generated_C0": n_gen, "items": len(items), "dropped": {}}

    monkeypatch.setattr(Q, "build_items", fake_items)
    # every read right: the fake says the answer token (the gate passes and every item is eligible)
    monkeypatch.setattr(Q, "competence", lambda model, items, orders, ws, cand: [
        {"scene": it["scene"], "order": o, "reader": w, "variant": v, "slot": it["slot"][v], "greedy": "x",
         "said": rd["answer" if v == "org" else "cf_answer"], "right": True, "read_right": True, "cand_right": True}
        for it in items for o in orders for w, rd in it["orders"][o]["readers"].items() for v in ("org", "alt")])  # fmt: skip
    out = Q.stage_run(f"{pins.RUN_PREFIX}fake_run", "test", n_gen=12, n_items=12)
    return SimpleNamespace(tok=tok, fake=fake, out=out, n=12)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    import json

    import numpy as np

    out, n = fake_run.out, fake_run.n
    m = json.loads((out / "manifest.json").read_text())
    assert m["orders_tested"] == list(Q.ORDERS) and m["items"] == {"last": n, "first": n} and "sealed" in m
    assert m["dictionary_atoms"]["ordinal_atoms_present"] and len(m["dictionary_atoms"]["digit_atoms"]) == 10
    assert not any(p.name.startswith(("verdict", "view", "x47_10")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["order"], r["reader"], r["arm"]) for r in rows} == {
        (o, w, a) for o in Q.ORDERS for w in Q.READERS for a in Q.ARMS
    }
    assert len(rows) == n * len(Q.ORDERS) * len(Q.READERS) * len(Q.ARMS)
    assert {r["source"] for r in rows if r["order"] == "last"} == {"lookup"}  # one change serves the four prompts
    assert {r["source"] for r in rows if r["order"] == "first"} == set(Q.READERS)  # each its own
    lens = X.read_jsonl(out / "lens.jsonl")
    assert len(lens) == n * len(Q.ORDERS) * len(Q.READERS) and all(1 <= r["rank_ordinal_among3"] <= 3 for r in lens)
    assert all(len(r["top20"]) == 20 for r in lens)
    # question-last: the four readers read one and the same state (identical lens ranks)
    by = {(r["scene"], r["reader"]): r["rank_ordinal"] for r in lens if r["order"] == "last"}
    assert all(by[(s, w)] == by[(s, "lookup")] for s, w in by)
    z = np.load(out / "states.npz")
    assert set(z) == {f"{o}__{k}" for o in Q.ORDERS for k in (*Q.READERS, "scenes")}
    assert z["last__report"].shape == (n, 32) and np.allclose(z["last__report"], z["last__lookup"])
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == len(lens) and all(0 <= r["share_jpp"] <= 1 and 0 <= r["share_alf"] <= 1 for r in norms)
    greedy = X.read_jsonl(out / "examples_greedy.jsonl")
    assert len(greedy) == min(X.K_EXAMPLES, n) * len(Q.ORDERS) * len(Q.READERS) * len(Q.ARMS)
    c0 = json.loads((out / "c0_check.json").read_text())
    assert c0["reference"] == 0.5 and c0["within"] in (True, False)


def test_verdict_view_and_figures_on_the_fake_run(fake_run, monkeypatch):
    import json

    from bridge_jspace import pins

    monkeypatch.setattr(Q, "dan_answer", lambda: "27B: neither · 50%")
    out = Q.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x47_10.json").read_text())
    mm = blob["models"][0]
    assert mm["target"] == pins.TARGET and set(mm["orders"]) == set(Q.ORDERS)
    for res in mm["orders"].values():
        assert set(res["readers"]) == set(Q.READERS) and res["readers"]["report"]["n"] == fake_run.n
        assert res["rule"]["label"] == "not tested" and "fewer than 30" in res["rule"]["why"]  # 12 items
        assert res["probe"]["report"]["n"] == fake_run.n and 0 <= res["probe"]["report"]["probe"][0] <= 1
    text = (out / "x47_10.md").read_text()
    assert "not tested" in text and text.count("pending") == 2
    view = Q.stage_view(fake_run.out.name, decode=fake_run.tok.decode)
    md = (view / "examples.md").read_text()
    assert md.count("```") == 2 * 2 * min(X.K_EXAMPLES, fake_run.n) * len(Q.ORDERS) * len(Q.READERS)
    assert "⟦ frog.⟧" in md and "⟦ bee.⟧" in md
    figs = Q.stage_figures(out)  # the orders ran (not tested on 12 items: the label is in the title)
    assert len(figs) == 1 and figs[0].exists() and figs[0].name == "x47_10_fake_run.png"
