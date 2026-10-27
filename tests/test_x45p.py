"""Batch 45, test 45p (scripts/x45p.py): the new item's and the control item's token positions (a fake tokenizer, and the
target's tokenizer and 45m run when cached), the rule on planted outcomes, the batch rule, the sealed verdict, and the run
stage end to end on a tiny fake causal model (CPU). No real model."""

import json
import re
from types import SimpleNamespace

import pytest

from scripts import x0_necessity as X
from scripts import x45p as P

# a 45m scene: the bee's locker sentence is the inserted one; Iris's pick changes from the frog (O) to the bee (S)
ORG = ("Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the bee is 3. "
       "The locker of the frog is 5. Noah picked the tick. Iris picked the frog.")  # fmt: skip
ALT = ORG.replace("Iris picked the frog.", "Iris picked the bee.")


def wrap(context: str, question: str = "Which locker belongs to Iris's pick?") -> str:
    return f"<|im_start|>user\n{context}\n{question}<|im_end|>\nAnswer:"


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


# ---- positions ----------------------------------------------------------------------------------------------------


def test_locker_items_in_context_order():
    assert P.locker_items(ORG) == [("The locker of the tick is 2.", "tick"), ("The locker of the rabbit is 1.", "rabbit"),
                                   ("The locker of the bee is 3.", "bee"), ("The locker of the frog is 5.", "frog")]  # fmt: skip
    assert P.locker_items("The locker of nitrogen is five.") == [("The locker of nitrogen is five.", "nitrogen")]


def test_item_spans_new_item_and_first_other_locker_item():
    text = wrap(ORG)
    s = P.item_spans(text, ORG, "frog", "bee")
    assert text[slice(*s["new"]["span"])] == "bee" and s["new"]["index"] == 2
    assert s["new"]["sentence"] == "The locker of the bee is 3."
    assert text[slice(*s["control"]["span"])] == "tick" and s["control"]["index"] == 0  # first in context order


def test_control_skips_the_bridge_and_the_new_item():
    ctx = ("The locker of the frog is 5. The locker of the bee is 3. Iris picked the frog. The locker of the tick is 2. "
           "Noah picked the tick.")  # fmt: skip
    s = P.item_spans(wrap(ctx), ctx, "frog", "bee")
    assert s["control"]["item"] == "tick" and s["control"]["index"] == 2
    only = "The locker of the frog is 5. The locker of the bee is 3. Iris picked the frog."
    with pytest.raises(P.NoControl):
        P.item_spans(wrap(only), only, "frog", "bee")


def test_item_spans_never_match_the_name_in_a_pick_sentence():
    # "tick" is also in "Noah picked the tick." and the bridge "frog" in the asked pick: only locker sentences count
    text = wrap(ORG)
    s = P.item_spans(text, ORG, "frog", "bee")
    a, _ = s["control"]["span"]
    assert text[:a].endswith("The locker of the ") and a < text.index("Noah picked")


def test_token_positions_are_the_names_tokens_on_the_fake_tokenizer():
    tok = WordTok()
    text = wrap(ORG)
    enc = tok(text, return_offsets_mapping=True)
    s = P.item_spans(text, ORG, "frog", "bee")
    for part, name in (("new", "bee"), ("control", "tick")):
        pos = P.token_positions(enc.offset_mapping, s[part]["span"])
        assert len(pos) == 1 and tok.decode([enc.input_ids[p] for p in pos]) == f" {name}"
        assert P.exact(tok, enc.input_ids, pos, name)
    assert not P.exact(tok, enc.input_ids, [pos[0], pos[0] + 1], "tick")  # one token too many


def test_marked_labels_spans_and_keeps_text():
    text = "Iris picked the frog. The locker of the bee is 3."
    out = P.marked(text, [(15, 20, "bridge"), (39, 43, "new")])
    assert out == "Iris picked the ⟦bridge:frog⟧. The locker of the ⟦new:bee⟧ is 3."
    assert re.sub(r"⟦\w+:|⟧", "", out) == text
    with pytest.raises(AssertionError):
        P.marked(text, [(0, 10, "a"), (5, 12, "b")])


def _real_tokenizer():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


def test_positions_on_the_targets_tokenizer():
    from bridge_jspace.tokens import raw_encoding

    tok = _real_tokenizer()
    for ctx, bridge, new, ctl in ((ORG, "frog", "bee", "tick"),
                                  ("The locker of beta is eight. Ivan picked iota. The locker of alpha is nine. The locker "
                                   "of iota is five. Oscar picked beta.", "beta", "alpha", "iota")):  # fmt: skip
        text = wrap(ctx, "Which locker belongs to Oscar's pick?")
        enc = raw_encoding(tok, text, offsets=True)
        s = P.item_spans(text, ctx, bridge, new)
        assert s["control"]["item"] == ctl
        for part in ("new", "control"):
            pos = P.token_positions(enc["offset_mapping"], s[part]["span"])
            assert pos == list(range(pos[0], pos[-1] + 1))  # contiguous
            assert P.exact(tok, enc["input_ids"], pos, s[part]["item"])


def test_select_on_the_targets_45m_run():
    # the target's own 45m run (rebuilt on its tokenizer); skipped where the run or the tokenizer is absent
    from bridge_jspace import pins

    run = P.RUN_45M.get(pins.TARGET)
    if run is None or not (X.RESULTS / run / "cases.jsonl").exists():
        pytest.skip("no 45m run of the target here")
    tok = _real_tokenizer()
    items, counts = P.select(tok, run, X.PREDICTED[pins.TARGET])
    assert counts["items"] == len(items) > 0
    assert counts["items"] + sum(counts["dropped"].values()) == counts["alt locker vs asked pick"]["before"]
    for it in items:
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        assert it["features"]["alt locker vs asked pick"] == "before"
        assert max(it["new"]["positions"]) < it["pos"]
        assert it["new"]["item"] == it["fresh"]["item"] == it["cf_bridge"]
        assert it["control"]["item"] not in (it["entity"], it["cf_bridge"])
        for part in ("new", "control"):
            assert tok.decode([ids[p] for p in it[part]["positions"]]).strip() == it[part]["item"]
        # O and S differ at the bridge word only, and the readers share every patched position
        assert [
            i for i, (a, b) in enumerate(zip(ids, it["readers"][X.LOOKUP]["ids"]["alt"], strict=True)) if a != b
        ] == [it["pos"]]
        last = max(it["pos"], *it["control"]["positions"])
        assert it["readers"][X.RECALL]["ids"]["org"][: last + 1] == ids[: last + 1]


# ---- the rule on planted outcomes ---------------------------------------------------------------------------------


def planted(n: int, **arms: int) -> dict[str, list[int]]:
    """Per-item 0/1 switches: each named arm switches its first k items, every other arm none."""
    return {a: [int(i < arms.get(a, 0)) for i in range(n)] for a in P.ARMS}


def ents(n: int, k: int = 10) -> list[str]:
    return [f"e{i % k}" for i in range(n)]


def rule_of(n: int, **arms: int) -> tuple[dict, dict]:
    nums = P.numbers(planted(n, **arms), ents(n), n_boot=300)
    return nums, P.rule(nums)


def test_holds_when_the_item_edit_costs_more_than_both_controls():
    nums, r = rule_of(100, a1=50, a2=10, a3=40, a4=35)  # losses 0.8, 0.2, 0.3
    assert nums["loss"]["a2"][0] == pytest.approx(0.8) and nums["loss"]["a3"][0] == pytest.approx(0.2)
    assert nums["diff"]["2-3"][0] == pytest.approx(0.6) and nums["diff"]["2-4"][0] == pytest.approx(0.5)
    assert r["status"] == "tested" and r["holds"] and r["over_random"] and r["over_control"]


def test_bars_are_inclusive():
    _, r = rule_of(100, a1=40, a2=10, a3=18, a4=16)  # 0.2 and 0.15 exactly
    assert r["holds"]


def test_random_bar_breaks_it():
    _, r = rule_of(100, a1=40, a2=10, a3=17, a4=30)  # loss_2 - loss_3 = 0.175
    assert not r["holds"] and not r["over_random"] and r["over_control"]


def test_control_bar_breaks_it():
    _, r = rule_of(100, a1=40, a2=10, a3=30, a4=15)  # loss_2 - loss_4 = 0.125
    assert not r["holds"] and r["over_random"] and not r["over_control"]


def test_fewer_than_30_base_switches_is_not_tested():
    _, r = rule_of(100, a1=29, a2=0, a3=29, a4=29)
    assert r["status"] == "not tested" and not r["holds"]
    _, r = rule_of(100, a1=30, a2=0, a3=29, a4=29)
    assert r["status"] == "tested" and r["holds"]


def test_losses_are_over_all_items_and_nan_without_base_switches():
    # the losses are ratios of rates over all items: an arm switching items arm 1 does not still counts
    nums = P.numbers({**planted(40, a1=20), "a3": [int(i >= 20) for i in range(40)]}, ents(40), n_boot=200)
    assert nums["loss"]["a3"][0] == pytest.approx(0.0)
    nums, r = rule_of(40)
    assert all(v[0] != v[0] for v in nums["loss"].values()) and r["status"] == "not tested"


def test_intervals_bracket_the_points():
    sw = planted(120, a1=80, a2=20, a3=70, a4=60)
    nums = P.numbers(sw, ents(120, 15), n_boot=2000)
    for v in [*nums["rate"].values(), *nums["loss"].values(), *nums["diff"].values()]:
        assert v[1] <= v[0] + 1e-12 and v[0] <= v[2] + 1e-12
    assert nums["entities"] == 15


def test_batch_rule():
    def m(status: str, holds: bool = False) -> dict:
        return {"run": status, "status": status, "holds": holds}

    assert P.batch_verdict([m("tested", True), m("tested", True), m("tested")])["label"] == "holds"
    assert P.batch_verdict([m("tested", True), m("not tested"), m("tested")])["label"] == "does not hold"
    assert P.batch_verdict([m("tested", True), m("pending"), m("tested")])["label"] == "pending"
    assert P.batch_verdict([m("tested", True), m("tested", True), m("pending")])["label"] == "holds"
    assert P.batch_verdict([m("tested"), m("tested"), m("pending")])["label"] == "does not hold"
    assert P.batch_verdict([m("tested", True), m("tested", True), m("tested")])["Q45.13"] == "(a) yes"


def test_dan_answer_reads_only_the_q45_13_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q45.12** (45q) ...\n\nDan: yes · 60%\n\n**Q45.13** (45p) ...\n\nRule: ...\n\nDan:{}\n"
    monkeypatch.setattr(P.subprocess, "run", fake_git(blocks.format("")))
    assert P.dan_answer() == ""
    monkeypatch.setattr(P.subprocess, "run", fake_git(blocks.format(" no · 65%")))
    assert P.dan_answer() == "no · 65%"
    monkeypatch.setattr(P.subprocess, "run", fake_git(blocks.format(" yes · 55%") + "\n**Q45.14** x\n\nDan: z\n"))
    assert P.dan_answer() == "yes · 55%"


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (copied from tests/test_x45b_binding.py, d larger so that
    k = 25 atoms stay below it): each block mixes the running mean of the positions so far into every position; an edit
    acts on a block's output, as Model's hooks do."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 32, vocab: int = 128):
        import torch

        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers = tok, n_layers
        self.device = torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()
        self.calls: list[tuple[int, list[dict]]] = []

    def forward(self, ids: list[int], edits: dict):
        import torch

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
        import torch

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
        import torch

        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def item_record(i: int, tok: WordTok) -> dict:
    """One 45p item as select() writes it, built with the fake tokenizer (O = ORG, S = ALT)."""
    text_o, text_s = wrap(ORG), wrap(ALT)
    enc, enc_s = tok(text_o, return_offsets_mapping=True), tok(text_s, return_offsets_mapping=True)
    pos = next(j for j, (a, b) in enumerate(enc.offset_mapping) if text_o[a:b] == " frog.")
    s = P.item_spans(text_o, ORG, "frog", "bee")
    for part in ("new", "control"):
        s[part]["positions"] = P.token_positions(enc.offset_mapping, s[part]["span"])
    s["control"]["vs_asked_pick"] = "before"
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    readers = {w: {"id": f"{w}-{i}", "question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
                   "tok_A": digit["5"], "tok_b": digit["3"], "ids": {"org": enc.input_ids, "alt": enc_s.input_ids},
                   "text": {"org": text_o}} for w in X.READERS}  # fmt: skip
    marks = {"bridge": [list(enc.offset_mapping[pos])],
             **{p: [list(enc.offset_mapping[q]) for q in s[p]["positions"]] for p in ("new", "control")}}  # fmt: skip
    return {"scene": f"s{i:03d}", "entity": f"e{i % 6}", "cf_bridge": "bee", "domain": "animals", "pos": pos,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ", "new": s["new"],
            "control": s["control"], "marks": marks, "readers": readers,
            "stored": {"whole": {"PP": 1, "PM": 1}, "a1": {"PP": 1, "PM": 0}}}  # fmt: skip


PLAN = {"items": 12, "items_at_L": 30, "alt locker vs asked pick": {"before": 12, "after": 18}, "dropped": {},
        "tokens": {"new 1, control 1": 12}, "control": {"before the new item, before the asked pick": 12}}  # fmt: skip


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = [item_record(i, tok) for i in range(12)]
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(P, "select", lambda *_: (items, PLAN))
    monkeypatch.setattr(P, "RESULTS", tmp_path / "x45p")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)  # the manifest records its inputs relative to the repo
    monkeypatch.setattr(P, "SPEC", tmp_path / "batch45.yaml")
    P.SPEC.write_text("")
    src = tmp_path / "x0" / P.RUN_45M[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    return SimpleNamespace(tok=tok, items=items, fake=fake, out=P.stage_run(f"{pins.RUN_PREFIX}fake_run", "test"))


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    import torch

    from bridge_jspace import pins
    from scripts import statement_positions as SP

    out, items, fake = fake_run.out, fake_run.items, fake_run.fake
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in items for w in X.READERS for a in P.ARMS
    }
    assert len(rows) == len(items) * len(X.READERS) * len(P.ARMS)
    assert not any(p.name.startswith(("verdict", "x45p-")) for p in out.iterdir())  # sealed: no verdict in the run
    m = json.loads((out / "manifest.json").read_text())
    assert m["layer"] == X.PREDICTED[pins.TARGET] and m["k"] == 25 and "sealed" in m
    # the first read: the lookup's O with the space token appended, under every arm in order
    la = X.PREDICTED[pins.TARGET]
    it, (seq, edits) = items[0], fake.calls[0]
    ids = it["readers"][X.LOOKUP]["ids"]
    assert seq == len(ids["org"]) + 1 and edits[0] == {} and len(edits) == len(P.ARMS)
    e = {arm: edit[la] for arm, edit in zip(P.ARMS[1:], edits[1:], strict=True)}
    pos, new, ctl = it["pos"], it["new"]["positions"], it["control"]["positions"]
    assert e["whole"].positions == e["a1"].positions == [pos]
    assert e["a2"].positions == e["a3"].positions == [pos, *new] and e["a4"].positions == [pos, *ctl]
    assert e["o2"].positions == new
    # whole = h_S - h_O at the bridge; a1 = whole minus its J++ part; the item rows = -J++(h) / -random part of h
    h = {v: fake.run(torch.tensor([ids[v]]), record=(la,))[1][la] for v in ("org", "alt")}
    jdic = FakeLens(None, "jpp").vectors(la, list(range(64)))
    whole = h["alt"][pos] - h["org"][pos]
    assert torch.allclose(e["whole"].delta[0], whole)
    assert torch.allclose(e["a1"].delta[0], whole - X.fit(jdic, whole[None], 25, "signed")[0], atol=1e-5)
    part = X.fit(jdic, h["org"][new], 25, "signed")
    for arm in ("a2", "a3", "a4"):
        assert torch.allclose(e[arm].delta[0], e["a1"].delta[0])  # every arm on top of the base edit
    assert torch.allclose(e["a2"].delta[1:], -part, atol=1e-5) and torch.allclose(e["o2"].delta, -part, atol=1e-5)
    assert torch.allclose(e["a4"].delta[1:], -X.fit(jdic, h["org"][ctl], 25, "signed"), atol=1e-5)
    # the random part: in X0's random subspace (seed 888 + L), at the J++ part's share to within one basis direction
    basis = SP.random_basis(32, torch.Generator().manual_seed(X.SUBSPACE_SEED + la))
    rand = -e["a3"].delta[1:]
    hn = h["org"][new]
    share = part.norm(dim=-1) ** 2 / hn.norm(dim=-1) ** 2
    rshare = rand.norm(dim=-1) ** 2 / hn.norm(dim=-1) ** 2
    one = ((hn @ basis) ** 2 / hn.norm(dim=-1, keepdim=True) ** 2).max(dim=-1).values
    assert ((rshare - share).abs() <= one + 1e-5).all()
    assert torch.allclose(rand, SP.random_subspace_part(hn, share, basis), atol=1e-5)
    # under a2, the new item's state at L is h minus its J++ part, h being O's clean state at L
    _, st = fake.run(torch.tensor([ids["org"]]), edits=edits[P.ARMS.index("a2")], record=(la,))
    assert torch.allclose(st[la][new], h["org"][new] - part, atol=1e-5)
    keep = [p for p in range(len(ids["org"])) if p not in (pos, *new)]
    assert torch.allclose(st[la][keep], h["org"][keep])
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == len(items) and norms[0]["new_jpp_share"][0] == pytest.approx(float(share[0]), abs=1e-4)
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == X.K_EXAMPLES * len(X.READERS) * len(P.ARMS)


def test_verdict_is_sealed_until_dans_answer(fake_run, monkeypatch):
    monkeypatch.setattr(P, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        P.stage_verdict([fake_run.out.name], n_boot=100)


def test_verdict_stage_on_the_fake_run(fake_run, monkeypatch):
    from bridge_jspace import pins

    monkeypatch.setattr(P, "dan_answer", lambda: "no · 60%")
    out = P.stage_verdict([fake_run.out.name], n_boot=100)
    blob = json.loads((out / "x45p.json").read_text())
    assert blob["dan"] == "no · 60%" and out.parent == P.RESULTS
    model = blob["models"][0]
    assert model["target"] == pins.TARGET and model["readers"]["recall"]["n"] == len(fake_run.items)
    assert model["status"] == "not tested"  # 12 items: fewer than 30 recall switches whatever the fake reads
    assert {m["status"] for m in blob["models"][1:]} == {"pending"} and len(blob["models"]) == 3
    assert blob["verdict"]["label"] == "pending"
    assert set(model["checks"]) == {f"{w} {a} vs 45m's stored {s}" for w in ("lookup", "recall")
                                    for a, s in (("whole", "whole"), ("a1", "no_part"))}  # fmt: skip
    assert (out / "examples.md").read_text().count("```") == 2 * X.K_EXAMPLES * len(X.READERS)


def write_planted(root, name: str, target: str, recall: dict[str, int], n: int = 60) -> None:
    """A planted 45p run folder: the recall switches the first recall[arm] items per arm, the lookup every item under
    the edits; O alone with a2's edit read right on all items but the last two (lookup)."""
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "run_45m": "m45"}))
    (src / "plan.json").write_text(json.dumps(PLAN))
    items = [{"scene": f"s{i}", "stored": {"whole": {"PP": 1, "PM": 1}, "a1": {"PP": 1, "PM": int(i < recall["a1"])}}}
             for i in range(n)]  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", items)
    rows = []
    for i in range(n):
        for w in X.READERS:
            for arm in P.ARMS:
                sw = int(i < recall.get(arm, 0)) if w == X.RECALL else int(arm not in ("none", "o2"))
                right = int(arm in ("none", "o2") and not (w == X.LOOKUP and arm == "o2" and i >= n - 2))
                rows.append({"scene": f"s{i}", "entity": f"e{i % 12}", "reader": w, "arm": arm, "switched": sw,
                             "right": right})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "norms.jsonl", [{"whole_jpp_share": 0.3, "new_jpp_share": [0.5], "new_rand_share": [0.49],
                                         "control_jpp_share": [0.4]} for _ in range(n)])  # fmt: skip
    X.write_jsonl(src / "examples_greedy.jsonl", [])


def test_verdict_stage_on_planted_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    monkeypatch.setattr(P, "dan_answer", lambda: "yes · 55%")
    monkeypatch.setattr(P, "example_lines", lambda run: [])  # the planted cases hold no prompts
    write_planted(tmp_path, "r9", "qwen3.5-9b", {"whole": 50, "a1": 40, "a2": 10, "a3": 30, "a4": 25})  # 0.5, 0.375
    write_planted(tmp_path, "r27", "qwen3.6-27b", {"whole": 50, "a1": 40, "a2": 10, "a3": 15, "a4": 30})  # 0.125
    write_planted(tmp_path, "rm", "muse-glimmer-30b", {"whole": 50, "a1": 40, "a2": 20, "a3": 30, "a4": 30})  # 0.25
    blob = json.loads((P.stage_verdict(["r9", "r27", "rm"], n_boot=200) / "x45p.json").read_text())
    by = {m["run"]: m for m in blob["models"]}
    assert by["r9"]["holds"] and not by["r27"]["holds"] and by["rm"]["holds"]
    assert not by["r27"]["over_random"] and by["r27"]["over_control"]
    assert by["r9"]["readers"]["recall"]["diff"]["2-3"][0] == pytest.approx(0.5)
    assert by["rm"]["readers"]["recall"]["diff"]["2-4"][0] == pytest.approx(0.25)
    assert blob["verdict"]["label"] == "holds" and blob["verdict"]["Q45.13"] == "(a) yes"
    o = by["r9"]["o_alone"]
    assert o["o2"]["both_right"] == 58 and o["o2"]["recall_right"] == 60 and o["none"]["both_right"] == 60
    assert by["r9"]["checks"]["recall a1 vs 45m's stored no_part"]["agree"] == 60
    assert by["r9"]["shares_median"]["new_jpp_share"] == 0.5
    # the lookup is reported beside it: every edited arm switches it here
    assert by["r9"]["readers"]["lookup"]["rate"]["a2"][0] == 1.0


def test_verdict_with_a_missing_run(tmp_path, monkeypatch):
    # two models fail and the Muse run is not here: one model cannot make 2 of 3, so the batch does not hold
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    monkeypatch.setattr(P, "dan_answer", lambda: "no · 70%")
    monkeypatch.setattr(P, "example_lines", lambda run: [])
    write_planted(tmp_path, "r9", "qwen3.5-9b", {"a1": 40, "a2": 10, "a3": 12, "a4": 30})
    write_planted(tmp_path, "r27", "qwen3.6-27b", {"a1": 40, "a2": 10, "a3": 15, "a4": 30})
    blob = json.loads(
        (P.stage_verdict(["r9", "r27", P.RUNS["muse-glimmer-30b"]], n_boot=100) / "x45p.json").read_text()
    )
    assert [m["status"] for m in blob["models"]] == ["tested", "tested", "pending"]
    assert blob["verdict"]["label"] == "does not hold" and blob["verdict"]["Q45.13"] == "(b) no"
    # only the 9B given: the other two are pending, and one holding model leaves it open (a second root: verdict
    # folders are named by the second)
    monkeypatch.setattr(P, "RESULTS", tmp_path / "second")
    write_planted(P.RESULTS, "r9b", "qwen3.5-9b", {"a1": 40, "a2": 10, "a3": 30, "a4": 30})
    blob = json.loads((P.stage_verdict(["r9b"], n_boot=100) / "x45p.json").read_text())
    assert len(blob["models"]) == 3 and blob["verdict"]["label"] == "pending"
    with pytest.raises(AssertionError, match="no 45p run 'typo'"):
        P.stage_verdict(["typo"], n_boot=100)
    (P.RESULTS / "r9").symlink_to(tmp_path / "r9")
    with pytest.raises(AssertionError, match="one run per model"):
        P.stage_verdict(["r9", "r9b"], n_boot=100)
