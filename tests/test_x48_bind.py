"""Batch 48, test 48.3 (scripts/x48_bind.py): scene selection (pickers, strata, the write candidate, the halves) on a
fake tokenizer, the probe's split and candidate-restricted prediction on planted states, the run stage end to end on a
tiny fake causal model (the write's positions, vectors and norms), the rule on planted numbers, the sealed verdict and
the verdict stage on the fake run. No real model."""

import json
import re
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x48_bind as W

# O: Iris (asked) picked the frog; its locker sentence comes after her pick (locker-after). Noah picked the tick, whose
# locker sentence comes after both picks (the write candidate); Peter's rabbit has its locker before his pick.
ORG = ("The locker of the rabbit is 1. Peter picked the rabbit. Iris picked the frog. The locker of the frog is 5. "
       "Noah picked the tick. The locker of the tick is 2.")  # fmt: skip
FACTS = {"pick": {"Peter": "rabbit", "Iris": "frog", "Noah": "tick"}, "locker": {"rabbit": 1, "frog": 5, "tick": 2}}


def wrap(context: str, question: str) -> str:
    return f"<|im_start|>user\n{context}\n{question}<|im_end|>\nAnswer:"


class WordTok:
    """Words with their leading whitespace as tokens, punctuation on its own (as the targets' BPE splits 'frog.' into
    ' frog' and '.'); ids from a shared vocab (after tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\w+|\S", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


QUESTIONS = {"PP": "Which locker belongs to Iris's pick?", "PM": "How many legs does Iris's pick have?"}


def fake_case(tok: WordTok, context: str = ORG, scene: str = "s000", bridge: str = "frog", asked: str = "Iris",
              cf_bridge: str = "tick") -> tuple[dict, dict]:  # fmt: skip
    """An X0 chat case (both readers) and its tasks_v2 items by id, on the fake tokenizer."""
    readers, by_id = {}, {}
    pos = None
    for w, q0 in QUESTIONS.items():
        q = q0.replace("Iris", asked)
        text = wrap(context, q)
        enc = tok(text, return_offsets_mapping=True)
        pos = next(
            j for j, (a, b) in enumerate(enc.offset_mapping) if text[a:b] == f" {bridge}" and a > text.index("picked")
        )
        digit = {d: tok(d).input_ids[0] for d in "0123456789"}
        answer = "5" if w == "PP" else "4"
        readers[w] = {"id": f"{w}-{scene}", "question": q, "answer": answer, "tok_A": digit[answer],
                      "ids": {"org": enc.input_ids, "alt": enc.input_ids}}  # fmt: skip
        by_id[f"{w}-{scene}"] = {"id": f"{w}-{scene}", "scene_facts": FACTS, "numbers": "digits", "context": context,
                                 "question": q, "kind": "digit", "format": "prose"}  # fmt: skip
    case = {"scene": scene, "rendering": "chat", "domain": "animals", "bridge": bridge, "cf_bridge": cf_bridge,
            "context": context, "cf_context": context, "pos": pos, "upstream": False,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "readers": readers}  # fmt: skip
    return case, by_id


@pytest.fixture
def render_fake(monkeypatch):
    monkeypatch.setattr(W.X, "render", lambda tok, item, rendering, context: wrap(context, item["question"]))


# ---- scenes -------------------------------------------------------------------------------------------------------


def test_picks_and_lockers_in_context_order():
    assert [(p["person"], p["item"], p["index"]) for p in W.picks_of(ORG)] == [("Peter", "rabbit", 1), ("Iris", "frog", 2),
                                                                                ("Noah", "tick", 4)]  # fmt: skip
    lk = W.lockers_of(ORG)
    assert [(x["k"], x["index"], x["item"], x["number"]) for x in lk] == [(0, 0, "rabbit", "1"), (1, 3, "frog", "5"),
                                                                           (2, 5, "tick", "2")]  # fmt: skip
    assert W.lockers_of("The locker of nitrogen is five.")[0]["item"] == "nitrogen"


def test_scene_item_strata_write_candidate_and_names(render_fake):
    tok = WordTok()
    case, by_id = fake_case(tok)
    it = W.scene_item(tok, case, "main", by_id)
    assert it["asked"] == {"person": "Iris", "pick_index": 2} and it["names"] == ["Peter", "Iris", "Noah"]
    assert it["group"] == "after"
    strata = {s["item"]: s["stratum"] for s in it["sentences"]}
    assert strata == {"rabbit": "before", "frog": "after", "tick": "after"}
    assert [s["asked"] for s in it["sentences"]] == [False, True, False]
    wr = it["write"]
    assert wr["item"] == "tick" and wr["person"] == "Noah" and wr["digit"] == "2" and wr["attribute"] == "8"
    assert wr["same_attribute"] is False  # tick 8 legs, frog 4
    ids = case["readers"]["PP"]["ids"]["org"]
    text = wrap(ORG, QUESTIONS["PP"])
    assert (
        tok.decode([ids[wr["positions"]["item"][0]]]) == " tick"
        and tok.decode([ids[wr["positions"]["number"][0]]]) == " 2"
    )
    assert [text[slice(*s)].strip() for s in it["marks"]["write"]] == ["tick", "2"]
    assert "⟦bridge:frog⟧" in W.item_marked(it, "PP") and "⟦write:tick⟧ is ⟦write:2⟧" in W.item_marked(it, "PP")
    # the write's tokens are after the bridge word
    assert wr["positions"]["item"][0] > it["pos"]


def test_scene_item_group_before_has_no_write(render_fake):
    tok = WordTok()
    ctx = ("The locker of the frog is 5. Peter picked the rabbit. Iris picked the frog. The locker of the rabbit is 1. "
           "Noah picked the tick. The locker of the tick is 2.")  # fmt: skip
    case, by_id = fake_case(tok, ctx)
    it = W.scene_item(tok, case, "main", by_id)
    assert it["group"] == "before" and it["write"] is None and it["write_dropped"] is None
    assert {s["item"]: s["stratum"] for s in it["sentences"]} == {"frog": "before", "rabbit": "after", "tick": "after"}


def test_write_candidate_needs_a_sentence_after_both_picks(render_fake):
    tok = WordTok()
    # the tick's locker sentence comes before Iris's pick: no candidate
    ctx = ("The locker of the rabbit is 1. Peter picked the rabbit. Noah picked the tick. The locker of the tick is 2. "
           "Iris picked the frog. The locker of the frog is 5.")  # fmt: skip
    case, by_id = fake_case(tok, ctx)
    it = W.scene_item(tok, case, "main", by_id)
    assert it["group"] == "after" and it["write"] is None
    assert it["write_dropped"] == "no other person's locker sentence after both picks"


def test_the_generators_picks_must_match_the_sentences(render_fake):
    tok = WordTok()
    case, by_id = fake_case(tok)
    by_id["PP-s000"]["scene_facts"] = {**FACTS, "pick": {"Peter": "rabbit", "Iris": "frog", "Nora": "tick"}}
    with pytest.raises(AssertionError, match="not the generator's picks"):
        W.scene_item(tok, case, "main", by_id)


def test_the_readers_prompts_must_agree_through_the_last_locker_token(monkeypatch):
    # the recall's prompt rendered with a sentence before the context: its locker tokens sit one token later
    monkeypatch.setattr(W.X, "render", lambda tok, item, rendering, context: (
        ("Note. " if item["id"].startswith("PM") else "") + wrap(context, item["question"])))  # fmt: skip
    tok = WordTok()
    case, by_id = fake_case(tok)
    case["readers"]["PM"]["ids"]["org"] = tok("Note. " + wrap(ORG, QUESTIONS["PM"])).input_ids
    with pytest.raises(W.Dropped, match="differ before the last locker token"):
        W.scene_item(tok, case, "main", by_id)


def test_halves_balance_locker_after_scenes_and_are_seeded():
    items = [{"entity": f"e{i % 7}", "group": "after" if i % 3 else "before"} for i in range(42)]
    h = W.halves(items)
    assert set(h) == {f"e{i}" for i in range(7)} and set(h.values()) == {"A", "B"}
    after = {e: sum(it["entity"] == e and it["group"] == "after" for it in items) for e in h}
    size = {s: sum(after[e] for e in h if h[e] == s) for s in ("A", "B")}
    assert abs(size["A"] - size["B"]) <= max(after.values())
    assert W.halves(items) == h and W.halves(items, seed=1) != h


# ---- the probe ----------------------------------------------------------------------------------------------------


def test_seeded_folds_hold_whole_entities_out():
    groups = [f"g{i % 9}" for i in range(50)]
    f = W.seeded_folds(groups)
    assert len(set(f)) == 5
    for g in set(groups):
        assert len({f[i] for i in range(50) if groups[i] == g}) == 1
    assert (W.seeded_folds(groups) == f).all()
    assert np.bincount(f).max() - np.bincount(f).min() <= 6


def test_predict_names_picks_the_best_candidate_only():
    classes = ["Ann", "Bob", "Cy", "Di"]
    scores = np.array([[0.1, 0.9, 0.5, 0.0], [0.9, 0.1, 0.2, 0.3]])
    assert W.predict_names(scores, classes, [["Ann", "Cy", "Di"], ["Bob", "Cy", "Eve"]]) == ["Cy", "Cy"]
    assert W.predict_names(scores[:1], classes, [["Eve", "Fay", "Gus"]]) == [None]


def planted_rows(n_scenes: int, seed: int = 0) -> tuple[list[dict], np.ndarray]:
    """Probe rows of planted scenes (3 pickers of 9 names each, items of 12), states = the picker's name vector plus
    noise in the after stratum, noise alone in the before stratum."""
    rng = np.random.default_rng(seed)
    names = [f"N{i}" for i in range(9)]
    vec = {n: rng.normal(size=16) * 3 for n in names}
    rows, h = [], []
    for s in range(n_scenes):
        people = [names[j] for j in rng.choice(9, 3, replace=False)]
        for k, who in enumerate(people):
            item = f"it{(s * 3 + k) % 12}"
            stratum = "after" if (s + k) % 2 == 0 else "before"
            rows.append({"item": s, "scene": f"s{s}", "source": "main", "entity": item, "domain": "animals",
                         "group": "after" if stratum == "after" else "before", "half": "A", "k": k,
                         "locker_item": item, "picker": who, "stratum": stratum, "asked": k == 0, "names": people})  # fmt: skip
            h.append((vec[who] if stratum == "after" else 0) + rng.normal(size=16))
    return rows, np.stack(h)


def test_probe_reads_planted_names_after_and_sits_at_chance_before():
    rows, h = planted_rows(120)
    out = W.probe_cells(h, rows, n_boot=200)
    assert out["after"]["accuracy"][0] >= 0.9 and out["after_all"]["accuracy"][0] >= 0.9
    assert out["before"]["accuracy"][0] <= 0.5 and out["before_all"]["accuracy"][0] <= 0.5
    assert out["transfer_all"]["accuracy"][0] <= 0.5
    assert out["after"]["n"] + out["before"]["n"] == sum(r["asked"] for r in rows)
    assert all(v[1] <= v[0] + 1e-12 <= v[2] + 2e-12 for v in (out[c]["accuracy"] for c in ("after", "before")))


def test_class_means_use_half_a_after_rows_with_enough_states():
    rows, h = planted_rows(40)
    for r in rows[: len(rows) // 2]:
        r["half"] = "B"
    means, counts = W.class_means(h, rows, min_fit=2)
    for n, mu in means.items():
        sel = [j for j, r in enumerate(rows) if r["picker"] == n and r["stratum"] == "after" and r["half"] == "A"]
        assert counts[n] == len(sel) >= 2 and np.allclose(mu, h[sel].mean(0))
    assert all(c < 2 for n, c in counts.items() if n not in means)


# ---- the rule on planted numbers ----------------------------------------------------------------------------------


def rates(**target: float) -> dict:
    return {"arms": {a: {"target": [target.get(a, 0.0), 0, 1]} for a in W.ARMS}}


def test_write_clause_needs_the_write_and_its_random_at_the_same_s():
    assert W.clause_write(rates(w1=0.3, r1=0.05))["holds"]  # the bars are inclusive
    assert not W.clause_write(rates(w1=0.29, r1=0.0))["holds"]
    assert not W.clause_write(rates(w1=0.5, r1=0.06))["holds"]
    c = W.clause_write(rates(w1=0.1, r1=0.0, w2=0.4, r2=0.02))
    assert c["holds"] and not c["by_s"]["1"]["holds"] and c["by_s"]["2"]["holds"]
    assert not W.clause_write(rates(w1=0.4, r1=0.1, w2=0.2, r2=0.0))["holds"]  # not across s
    assert not W.clause_write({"n": 0})["holds"]


def probe(after: float, before: float) -> dict:
    return {"after": {"accuracy": [after, 0, 1]}, "before": {"accuracy": [before, 0, 1]}}


def test_token_clause_bars():
    assert W.clause_token(probe(0.85, 0.5), 0.10, 0.05)["holds"]
    assert not W.clause_token(probe(0.84, 0.5), 0.10, 0.05)["probe"]
    assert not W.clause_token(probe(0.9, 0.51), 0.10, 0.05)["probe"]
    assert not W.clause_token(probe(0.9, 0.3), 0.11, 0.05)["lens"]
    assert not W.clause_token(probe(0.9, 0.3), None, 0.05)["lens"]


def test_rule_needs_one_token_and_the_lookups_write():
    ok, no = {"holds": True, "why": "ok"}, {"holds": False, "why": "no"}
    lk = {"holds": True, "by_s": {"1": {"why": "w"}}}
    rc = {"holds": False, "by_s": {"1": {"why": "r"}}}
    r = W.rule({"item": no, "number": ok}, lk, rc)
    assert r["holds"] and r["tokens_holding"] == ["number"] and not r["recall_moves"]
    assert not W.rule({"item": no, "number": no}, lk, rc)["holds"]
    assert not W.rule({"item": ok, "number": ok}, {**lk, "holds": False}, rc)["holds"]


def test_batch_verdict_needs_both_models():
    def m(status: str, holds: bool = False, moves: bool = False, target: str = "x") -> dict:
        return {"run": status, "status": status, "holds": holds, "recall_moves": moves, "target": target}

    assert W.batch_verdict([m("tested", True, True, "a"), m("tested", True, False, "b")])["label"] == "holds"
    v = W.batch_verdict([m("tested", True, True, "a"), m("tested", True, False, "b")])
    assert v["Q48.3"] == "yes" and v["recall_moves"]["answer"] == "no"
    assert W.batch_verdict([m("tested", True, True, "a"), m("pending")])["label"] == "pending"
    assert W.batch_verdict([m("tested", True), m("tested", False)])["label"] == "does not hold"
    assert W.batch_verdict([m("tested", False), m("pending")])["label"] == "does not hold"
    assert (
        W.batch_verdict([m("tested", True, True, "a"), m("tested", True, True, "b")])["recall_moves"]["answer"] == "yes"
    )


def test_dan_answer_reads_only_the_q48_3_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = (
        "**Q48.2** (48.2) ...\n\nDan: yes\n\n**Q48.3** (48.3) ...\n\nRule: ...\n\nDan:{}\n\n**Q48.4** x\n\nDan: z\n"
    )
    monkeypatch.setattr(W.subprocess, "run", fake_git(blocks.format("")))
    assert W.dan_answer() == ""
    monkeypatch.setattr(W.subprocess, "run", fake_git(blocks.format(" yes · 60%; recall no · 70%")))
    assert W.dan_answer() == "yes · 60%; recall no · 70%"


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (copied from tests/test_x45p.py, d = 32 so that k = 25
    atoms stay below it): each block mixes the running mean of the positions so far into every position; an edit acts
    on a block's output, as Model's hooks do."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 32, vocab: int = 256):
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


NAMES = ("Iris", "Noah", "Peter", "Zoe", "Will", "Paul")
ITEMS = ("frog", "tick", "rabbit", "bee", "owl", "deer", "cat", "dog")


def fake_scene(i: int) -> tuple[str, dict, str, str, str]:
    """A locker-after scene i: the asked person picks the bridge; another person's item has its locker sentence after
    both picks (the 45m scenes' cf bridge, so x45m's grouping reads locker-after); the names and items rotate so that
    every name has states in both halves."""
    a, j, p = NAMES[i % 6], NAMES[(i + 1) % 6], NAMES[(i + 2) % 6]
    bridge, other, third = ITEMS[i % 8], ITEMS[(i + 3) % 8], ITEMS[(i + 5) % 8]
    ctx = (f"The locker of the {third} is 1. {p} picked the {third}. {a} picked the {bridge}. The locker of the {bridge} "
           f"is 5. {j} picked the {other}. The locker of the {other} is 2.")  # fmt: skip
    facts = {"pick": {p: third, a: bridge, j: other}, "locker": {third: 1, bridge: 5, other: 2}}
    return ctx, facts, bridge, a, other


def fake_items(tok: WordTok, n: int = 24) -> list[dict]:
    from scripts import tasks_v2 as T

    items = []
    for i in range(n):
        ctx, facts, bridge, asked, other = fake_scene(i)
        case, by_id = fake_case(tok, ctx, f"s{i:03d}", bridge, asked, other)
        for w in case["readers"]:
            by_id[f"{w}-s{i:03d}"]["scene_facts"] = facts
            case["readers"][w]["answer"] = "5" if w == "PP" else str(T.DOMAINS["animals"].values[bridge])
        it = W.scene_item(tok, case, "main" if i % 2 else "45m", by_id)
        it["half"] = "A" if i % 4 < 2 else "B"
        items.append(it)
    return items


PLAN = {"scenes": 24, "runs": {}, "dropped": {}, "entities": 8, "halves": {"A": [], "B": []},
        "locker_after": {"scenes": 24, "A": 12, "B": 12}, "write_candidates_B": 12, "write_dropped": {}, "names": 6,
        "strata": {"after": 48, "before": 24}, "numbers": {"digits": 24}, "exact": {}}  # fmt: skip


@pytest.fixture
def fake_run(tmp_path, monkeypatch, render_fake):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = fake_items(tok)
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(W, "select", lambda *_: (items, PLAN))
    monkeypatch.setattr(W, "RESULTS", tmp_path / "x48")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pins, "TARGET", "qwen3.5-9b")
    monkeypatch.setattr(pins, "RUN_PREFIX", "qwen35_9b_")
    monkeypatch.setattr(W, "SPEC", tmp_path / "batch48.yaml")
    W.SPEC.write_text("")
    for runs in W.SOURCES.values():
        src = tmp_path / "x0" / runs["qwen3.5-9b"]
        src.mkdir(parents=True)
        for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
            (src / f).write_text("")
    return SimpleNamespace(tok=tok, items=items, fake=fake, out=W.stage_run("qwen35_9b_fake_run", "test"))


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    import torch

    out, items, fake = fake_run.out, fake_run.items, fake_run.fake
    la = 12
    m = json.loads((out / "manifest.json").read_text())
    assert m["layer"] == la and m["k"] == 25 and "sealed" in m
    assert not any(p.name.startswith(("verdict", "x48_bind-")) for p in out.iterdir())
    rows_p = X.read_jsonl(out / "probe_rows.jsonl")
    z = np.load(out / "states.npz")
    assert z["h_item"].shape == (len(rows_p), 32) == z["h_number"].shape
    assert len(rows_p) == sum(bool(s["picker"]) for it in items for s in it["sentences"])
    # the states are O's clean states at L at each sentence's item / number token
    it = items[0]
    h = fake.run(torch.tensor([it["readers"]["PP"]["ids"]["org"]]), record=(la,))[1][la]
    first = [j for j, r in enumerate(rows_p) if r["item"] == 0]
    for j, s in zip(first, it["sentences"], strict=True):
        assert torch.allclose(torch.tensor(z["h_item"][j]).float(), h[s["positions"]["item"][0]], atol=1e-2)
        assert torch.allclose(torch.tensor(z["h_number"][j]).float(), h[s["positions"]["number"][0]], atol=1e-2)
    contrasts = json.loads((out / "contrasts.json").read_text())
    writes = [i for i, it in enumerate(items) if it["group"] == "after" and it["half"] == "B" and it["write"]]
    assert [w["item"] for w in contrasts["per_write"]] == writes and contrasts["writes"] == len(writes)
    assert len(contrasts["random_dirs_share"]["item"]) == W.N_RANDOM_DIRS
    assert all(0 < s <= 1 for s in contrasts["random_dirs_share"]["item"])
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (items[i]["scene"], w, a) for i in writes for w in X.READERS for a in W.ARMS
    }
    assert {r["class"] for r in rows} <= {"target", "original", "other", "same"}
    # the first read: the lookup's O with the space token appended, every arm in order
    it, (seq, edits) = items[writes[0]], fake.calls[0]
    assert seq == len(it["readers"]["PP"]["ids"]["org"]) + 1 and edits[0] == {} and len(edits) == len(W.ARMS)
    e = {arm: edit[la] for arm, edit in zip(W.ARMS[1:], edits[1:], strict=True)}
    wr = it["write"]
    for arm in e.values():
        assert arm.positions == [wr["positions"]["item"][0], wr["positions"]["number"][0]]
    # the write = s (mu_asked - mu_picker) per token, the means over half A's after rows (MIN_FIT states each)
    for t, row in zip(W.TOKENS, range(2), strict=True):
        hh = z[f"h_{t}"].astype(np.float64)
        mu = {n: hh[[j for j, r in enumerate(rows_p) if r["picker"] == n and r["stratum"] == "after" and r["half"] == "A"]].mean(0)
              for n in (it["asked"]["person"], wr["person"])}  # fmt: skip
        delta = torch.tensor(mu[it["asked"]["person"]] - mu[wr["person"]]).float()
        assert torch.allclose(e["w1"].delta[row], delta, atol=1e-2) and torch.allclose(
            e["w2"].delta[row], 2 * delta, atol=1e-2
        )
        assert torch.allclose(e["r1"].delta[row].norm(), delta.norm(), atol=1e-2)
        assert torch.allclose(e["r2"].delta[row].norm(), 2 * delta.norm(), atol=1e-2)
        assert not torch.allclose(e["r1"].delta[row], delta, atol=1e-2)
        assert abs(contrasts["per_write"][0][f"norm_{t}"] - float(delta.norm())) < 1e-2
    # under w1 only the written tokens' states change at L
    _, st = fake.run(torch.tensor([it["readers"]["PP"]["ids"]["org"]]), edits=edits[1], record=(la,))
    h = fake.run(torch.tensor([it["readers"]["PP"]["ids"]["org"]]), record=(la,))[1][la]
    keep = [p for p in range(len(h)) if p not in e["w1"].positions]
    assert torch.allclose(st[la][keep], h[keep]) and not torch.allclose(st[la][e["w1"].positions], h[e["w1"].positions])
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == min(X.K_EXAMPLES, len(writes)) * 2 * len(W.ARMS)


def test_verdict_is_sealed_until_dans_answer(fake_run, monkeypatch):
    monkeypatch.setattr(W, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        W.stage_verdict([fake_run.out.name], n_boot=50)


def test_verdict_stage_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(W, "dan_answer", lambda: "no · 60%")
    out = W.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x48_bind.json").read_text())
    assert blob["dan"] == "no · 60%" and out.parent == W.RESULTS
    model = blob["models"][0]
    assert model["target"] == "qwen3.5-9b" and model["status"] == "tested"
    assert set(model["probes"]) == {"item", "number"} and set(model["clauses"]) == {"tokens", "lookup", "recall"}
    assert model["rates"]["lookup"]["n"] == 12 and set(model["rates"]["lookup"]["arms"]) == set(W.ARMS)
    assert blob["models"][1]["status"] == "pending" and blob["verdict"]["label"] in ("pending", "does not hold")
    md = (out / "x48_bind.md").read_text()
    assert "UNVERIFIED" in md and "Verdict" in md
    assert (out / "examples.md").read_text().count("```") == 2 * 2 * min(X.K_EXAMPLES, 12)
