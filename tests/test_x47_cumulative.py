"""Batch 47, test 47.4 (scripts/x47_cumulative.py): the arms' layers, positions and prompts; the O/S alignment checks (a
fake tokenizer, and the target's tokenizer and X0 runs when cached); the patches' propagation on a tiny fake causal model
(the bridge swapped up to L is S's after L; the clean design's swapped arms are S's own run); the run stage end to end;
the decomposition table, the bug flags and the seal on planted runs (CPU). No real model."""

import json
import re
from types import SimpleNamespace

import pytest
import torch

from scripts import x0_necessity as X
from scripts import x47_cumulative as C
from scripts.exp04_brew_parts import AddRows, SetRows

QUESTION = "Which locker belongs to Iris's pick?"
LOCKERS = "The locker of the frog is 5. The locker of the bee is 3. The locker of the tick is 2."
# clean (45m): only Iris's pick changes, to the bee nobody picks in O
CLEAN = (f"{LOCKERS} Noah picked the tick. Iris picked the frog. Peter picked the rabbit.",
         f"{LOCKERS} Noah picked the tick. Iris picked the bee. Peter picked the rabbit.")  # fmt: skip
# main test (cf): Iris and Noah swap their picks; Noah's pick after Iris's, or before it
AFTER = (
    f"{LOCKERS} Iris picked the frog. Noah picked the bee.",
    f"{LOCKERS} Iris picked the bee. Noah picked the frog.",
)
FIRST = (
    f"{LOCKERS} Noah picked the bee. Iris picked the frog.",
    f"{LOCKERS} Noah picked the frog. Iris picked the bee.",
)


def wrap(context: str, question: str = QUESTION) -> str:
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


def encoded(tok: WordTok, contexts: tuple[str, str], question: str = QUESTION) -> dict:
    """O's and S's prompts on the fake tokenizer: texts, offsets, ids, the bridge position (Iris's pick)."""
    texts = {v: wrap(ctx, question) for v, ctx in zip(("org", "alt"), contexts, strict=True)}
    enc = {v: tok(t, return_offsets_mapping=True) for v, t in texts.items()}
    pos = next(i for i, (a, b) in enumerate(enc["org"].offset_mapping) if texts["org"][a:b] == " frog."
               and texts["org"][:a].endswith("Iris picked the"))  # fmt: skip
    return {"texts": texts, "offsets": {v: e.offset_mapping for v, e in enc.items()},
            "ids": {v: e.input_ids for v, e in enc.items()}, "pos": pos,
            "contexts": dict(zip(("org", "alt"), contexts, strict=True))}  # fmt: skip


SENTENCES = {"org": "Iris picked the frog.", "alt": "Iris picked the bee."}


# ---- alignment ----------------------------------------------------------------------------------------------------


def test_changed_positions_and_the_designs_expected_changes():
    tok = WordTok()
    for contexts, design, other in ((CLEAN, "clean", False), (AFTER, "main", True), (FIRST, "main", True)):
        e = encoded(tok, contexts)
        diff = C.changed_positions(e["ids"]["org"], e["ids"]["alt"])
        got = C.expected_changes(design, diff, e["pos"])
        assert (got is not None) == other and e["pos"] in diff
        if got is not None:
            assert e["texts"]["org"][slice(*e["offsets"]["org"][got])].strip() in ("bee.", "frog.")
            assert (got < e["pos"]) == (contexts is FIRST)
    e = encoded(tok, AFTER)
    with pytest.raises(C.Misaligned, match="beyond the bridge"):  # the main test's second change is not a clean one
        C.expected_changes("clean", C.changed_positions(e["ids"]["org"], e["ids"]["alt"]), e["pos"])
    with pytest.raises(C.Misaligned, match="exactly the bridge token and one other"):
        C.expected_changes("main", [e["pos"]], e["pos"])
    with pytest.raises(C.Misaligned, match="exactly the bridge token and one other"):
        C.expected_changes("main", [1, 2, e["pos"]], e["pos"])
    with pytest.raises(C.Misaligned, match="length"):
        C.changed_positions([1, 2, 3], [1, 2])


def test_pick_positions_cover_the_pick_sentence_and_its_person():
    tok = WordTok()
    for contexts in (CLEAN, AFTER, FIRST):
        e = encoded(tok, contexts)
        pick, person = C.pick_positions(e["texts"], e["offsets"], e["ids"], SENTENCES, e["contexts"], e["pos"])
        text = e["texts"]["org"]
        assert pick == list(range(pick[0], pick[-1] + 1)) and e["pos"] == pick[-1]
        assert text[e["offsets"]["org"][pick[0]][0] : e["offsets"]["org"][pick[-1]][1]].strip() == SENTENCES["org"]
        assert [text[slice(*e["offsets"]["org"][p])].strip() for p in person] == ["Iris"]
        assert all(e["ids"]["org"][p] == e["ids"]["alt"][p] for p in pick if p != e["pos"])


def test_pick_positions_refuse_a_sentence_that_does_not_line_up():
    tok = WordTok()
    two_words = (CLEAN[0], CLEAN[1].replace("Iris picked the bee.", "Iris picked the sea lion."))
    e = encoded(tok, two_words)
    with pytest.raises(C.Misaligned, match="different positions"):
        C.pick_positions(e["texts"], e["offsets"], e["ids"], {"org": SENTENCES["org"], "alt": "Iris picked the sea lion."},
                         e["contexts"], e["pos"])  # fmt: skip


def test_pick_sentence_is_the_asked_persons():
    item = {"id": "x", "question": QUESTION, "bridge": "frog", "cf_bridge": "bee"}
    assert C.pick_sentence(item, AFTER[0], "frog") == "Iris picked the frog."
    assert C.pick_sentence(item, AFTER[1], "bee") == "Iris picked the bee."


def _real_tokenizer():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


@pytest.mark.parametrize("design", C.DESIGNS)
def test_select_on_the_targets_x0_runs(design):
    # the target's own source run (rebuilt on its tokenizer); skipped where the run or the tokenizer is absent
    from bridge_jspace import pins

    run = C.SOURCES[design].get(pins.TARGET)
    if run is None or not (X.RESULTS / run / "cases.jsonl").exists():
        pytest.skip(f"no {design} run of the target here")
    tok = _real_tokenizer()
    items, counts = C.select(tok, design, run, X.PREDICTED[pins.TARGET])
    assert (
        counts["items"] == len(items) > 0 and counts["items"] + sum(counts["dropped"].values()) == counts["items_at_L"]
    )
    for it in items:
        ids = it["readers"][X.LOOKUP]["ids"]
        diff = [i for i, (a, b) in enumerate(zip(ids["org"], ids["alt"], strict=True)) if a != b]
        assert diff == sorted([it["pos"], *([it["other"]] if design == "main" else [])])
        assert tok.decode([ids["org"][p] for p in it["pick"]]).strip() == it["sentences"]["org"]
        assert tok.decode([ids["alt"][p] for p in it["pick"]]).strip() == it["sentences"]["alt"]
        assert tok.decode([ids["org"][p] for p in it["person"]]).strip() == it["sentences"]["org"].split(" picked")[0]
        assert it["upstream"] == (design == "main" and it["other"] < it["pos"])
        C.assert_item(it)


# ---- the arms -----------------------------------------------------------------------------------------------------


def states(n_layers: int, seq: int, d: int, seed: int) -> dict[int, torch.Tensor]:
    g = torch.Generator().manual_seed(seed)
    return {la: torch.randn(seq, d, generator=g) for la in range(n_layers)}


def test_arm_edits_layers_positions_and_prompts():
    n, layer, pos, pick = 10, 4, 6, [3, 4, 5, 6, 7]
    h_o, h_s = states(n, 9, 4, 0), states(n, 9, 4, 1)
    arms = C.arm_edits(AddRows, SetRows, h_o, h_s, pos, pick, layer, n)
    assert tuple(arms) == C.ARMS
    assert {a: p for a, (p, _) in arms.items()} == {"none": "org", "a": "org", "b": "swap", "c": "swap", "d": "swap",
                                                   "b_blocks": "org", "S": "alt"}  # fmt: skip
    assert arms["none"][1] == {} and arms["S"][1] == {}
    ((la, e),) = arms["a"][1].items()
    assert la == layer and isinstance(e, AddRows) and e.positions == [pos]
    assert torch.equal(e.delta[0], h_s[layer][pos] - h_o[layer][pos])
    assert sorted(arms["b"][1]) == sorted(arms["b_blocks"][1]) == list(range(layer + 1))
    assert sorted(arms["c"][1]) == sorted(arms["d"][1]) == list(range(n))
    for arm, where in (("b", [pos]), ("c", [pos]), ("d", pick), ("b_blocks", [pos])):
        for la, e in arms[arm][1].items():
            assert isinstance(e, SetRows) and e.positions == where
            assert torch.equal(e.values, h_s[la][where])  # S's own state at that layer, set (not added)


def test_prompts_of_swaps_only_the_bridge_token():
    p = C.prompts_of({"org": [1, 2, 3, 4], "alt": [1, 9, 3, 8]}, 1)
    assert p == {"org": [1, 2, 3, 4], "swap": [1, 9, 3, 4], "alt": [1, 9, 3, 8]}
    with pytest.raises(AssertionError, match="length"):
        C.prompts_of({"org": [1, 2], "alt": [1]}, 0)


# ---- propagation on a fake causal model ----------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (as tests/test_x45p.py's): each block mixes the running mean
    of the positions so far into every position; an edit acts on a block's output, as Model's hooks do."""

    def __init__(self, tok: WordTok, n_layers: int = 36, d: int = 16, vocab: int = 160):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.layers = tok, n_layers, [None] * n_layers
        self.device = torch.device("cpu")
        self.calls: list[tuple[list[list[int]], list[dict]]] = []

    def forward(self, ids: list[int], edits: dict):
        h = self.emb[torch.as_tensor(ids)]
        out = {}
        for layer in range(self.n_layers):
            h = h + 0.1 * torch.cumsum(h, 0) / torch.arange(1, h.shape[0] + 1)[:, None]
            if layer in edits:
                h = edits[layer](h)
            out[layer] = h.clone()
        return self.unemb @ h[-1], out

    def run(self, ids, edits=None, record=()):
        logits, st = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: st[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        self.calls.append(([r.tolist() for r in rows], edits))
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts


def arm_logits(contexts: tuple[str, str], layer: int = 12) -> tuple[dict[str, torch.Tensor], list[float]]:
    """Every arm's final logits for one scene on the fake model, and the state check: under b_blocks, the bridge
    token's relative distance to S's state at each layer after L."""
    tok = WordTok()
    fake = FakeModel(tok)
    e = encoded(tok, contexts)
    pick, _ = C.pick_positions(e["texts"], e["offsets"], e["ids"], SENTENCES, e["contexts"], e["pos"])
    ids = e["ids"]
    h_o = fake.run(torch.tensor([ids["org"]]), record=(layer,))[1]
    h_s = fake.run(torch.tensor([ids["alt"]]), record=tuple(range(fake.n_layers)))[1]
    arms = C.arm_edits(AddRows, SetRows, h_o, h_s, e["pos"], pick, layer, fake.n_layers)
    prompts = C.prompts_of(ids, e["pos"])
    logits = {a: fake.forward(prompts[p], ed)[0] for a, (p, ed) in arms.items()}
    after = list(range(layer + 1, fake.n_layers))
    return logits, C.state_gap(fake, ids["org"], arms["b_blocks"][1], h_s, e["pos"], after)


def test_clean_design_swapped_arms_are_s_own_run():
    lg, gap = arm_logits(CLEAN)
    for arm in ("b", "c", "d"):
        assert torch.equal(lg[arm], lg["S"]), arm
    assert not torch.allclose(lg["a"], lg["S"]) and not torch.allclose(lg["none"], lg["S"])
    # b on O's own tokens: the bridge token's state after L is S's (the patch propagates); the read is not S's
    assert max(gap) == 0.0
    assert not torch.allclose(lg["b_blocks"], lg["S"])  # what later tokens read from the raw token at block 0


def test_main_design_other_change_after_b_equals_c_and_d():
    lg, gap = arm_logits(AFTER)
    assert torch.equal(lg["b"], lg["c"]) and torch.equal(lg["c"], lg["d"])
    assert not torch.allclose(lg["d"], lg["S"])  # Noah's pick is still O's: outside the pick sentence
    assert max(gap) == 0.0


def test_main_design_other_change_first_b_is_not_c():
    lg, gap = arm_logits(FIRST)
    assert not torch.allclose(lg["b"], lg["c"])  # the bridge's later states read Noah's earlier pick in S
    assert min(gap) > 0
    assert not torch.allclose(lg["c"], lg["d"])  # 'Iris picked the' read Noah's pick in S too


# ---- the run stage on the fake model ------------------------------------------------------------------------------


def fake_item(i: int, tok: WordTok, design: str) -> dict:
    """One item as select() writes it, on the fake tokenizer: clean items, or main items with Noah's pick after (even
    i) or before (odd i) Iris's."""
    contexts = CLEAN if design == "clean" else (AFTER if i % 2 == 0 else FIRST)
    e = encoded(tok, contexts)
    pos = e["pos"]
    diff = C.changed_positions(e["ids"]["org"], e["ids"]["alt"])
    other = C.expected_changes(design, diff, pos)
    pick, person = C.pick_positions(e["texts"], e["offsets"], e["ids"], SENTENCES, e["contexts"], pos)
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    readers = {w: {"id": f"{w}-{i}", "question": QUESTION, "answer": "5", "cf_answer": "3", "tok_A": digit["5"],
                   "tok_b": digit["3"], "ids": e["ids"], "text": {"org": e["texts"]["org"]}} for w in X.READERS}  # fmt: skip
    off = e["offsets"]["org"]
    upstream = other is not None and other < pos
    return {"scene": f"{design}{i:03d}", "design": design, "entity": f"e{i % 5}", "cf_bridge": "bee", "domain": "animals",
            "upstream": upstream, "prefix_same": not upstream, "group": ("locker-first", "locker-after")[i % 3 == 0],
            "pos": pos, "pick": pick, "person": person, "other": other, "sentences": SENTENCES,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ", "readers": readers,
            "marks": {"bridge": [list(off[pos])], "pick": [list(off[q]) for q in pick if q != pos],
                      "other": [list(off[other])] if other is not None else []},
            "stored": {"whole": {"PP": 1, "PM": 0}}}  # fmt: skip


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = {d: [fake_item(i, tok, d) for i in range(12)] for d in C.DESIGNS}
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    counts = {d: {"design": d, "source": C.SOURCES[d][pins.TARGET], "items_at_L": 12, "items": 12, "dropped": {},
                  "entities": 5, "groups": {"locker-first": 8, "locker-after": 4},
                  "upstream": {"True": 6, "False": 6} if d == "main" else {"False": 12}} for d in C.DESIGNS}  # fmt: skip
    monkeypatch.setattr(C, "select", lambda tok, design, run, layer: (items[design], counts[design]))
    monkeypatch.setattr(C, "RESULTS", tmp_path / "x47")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pins, "N_LAYERS", fake.n_layers)
    monkeypatch.setattr(C, "SPEC", tmp_path / "batch47.yaml")
    C.SPEC.write_text("")
    for d in C.DESIGNS:
        src = tmp_path / "x0" / C.SOURCES[d][pins.TARGET]
        src.mkdir(parents=True)
        for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
            (src / f).write_text("")
    out = C.stage_run(f"{pins.RUN_PREFIX}fake_x47", "test")
    return SimpleNamespace(tok=tok, items=items, fake=fake, out=out)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    from bridge_jspace import pins

    out, items, fake = fake_run.out, fake_run.items, fake_run.fake
    rows = X.read_jsonl(out / "outcomes.jsonl")
    want = {(d, it["scene"], w, a) for d in C.DESIGNS for it in items[d] for w in X.READERS for a in C.ARMS}
    assert {(r["design"], r["scene"], r["reader"], r["arm"]) for r in rows} == want and len(rows) == len(want)
    assert {p.name for p in out.iterdir()} == {"manifest.json", "plan.json", "cases.jsonl", "outcomes.jsonl",
                                               "checks.jsonl", "examples_greedy.jsonl"}  # sealed: no verdict  # fmt: skip
    m = json.loads((out / "manifest.json").read_text())
    assert m["layer"] == X.PREDICTED[pins.TARGET] and m["n_layers"] == fake.n_layers and "sealed" in m
    assert m["sources"] == {d: C.SOURCES[d][pins.TARGET] for d in C.DESIGNS} and "switches" in m
    # the first read: the first main item's lookup, every arm in order, each prompt with the space token appended
    la = X.PREDICTED[pins.TARGET]
    it = items["main"][0]
    prompts, edits = next(c for c in fake.calls if len(c[1]) == len(C.ARMS))
    ids = it["readers"][X.LOOKUP]["ids"]
    p = C.prompts_of(ids, it["pos"])
    assert prompts == [p[k] + it["space"] for k in ("org", "org", "swap", "swap", "swap", "org", "alt")]
    e = dict(zip(C.ARMS, edits, strict=True))
    assert (
        list(e["a"]) == [la] and sorted(e["b"]) == list(range(la + 1)) and sorted(e["c"]) == list(range(fake.n_layers))
    )
    assert all(x.positions == it["pick"] for x in e["d"].values()) and e["none"] == e["S"] == {}
    # the decisive read is X0's: switched = top token is S's answer; the clean design's swapped arms read as S does
    by = {(r["design"], r["scene"], r["reader"], r["arm"]): r for r in rows}
    for it in items["clean"]:
        for w in X.READERS:
            s = by[("clean", it["scene"], w, "S")]
            assert all(by[("clean", it["scene"], w, a)]["top"] == s["top"] for a in ("b", "c", "d"))
    for it in items["main"]:
        for w in X.READERS:
            if it["prefix_same"]:
                assert by[("main", it["scene"], w, "b")]["top"] == by[("main", it["scene"], w, "c")]["top"]
    checks = X.read_jsonl(out / "checks.jsonl")
    assert len(checks) == 24 and all(c["gap_max"] == 0.0 for c in checks if c["prefix_same"])
    assert all(c["gap_max"] > 0 for c in checks if not c["prefix_same"])
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == 2 * X.K_EXAMPLES * len(X.READERS) * len(C.ARMS)


def test_run_fails_loudly_when_the_patch_does_not_propagate(tmp_path, monkeypatch, fake_run):
    # a planted bug: (b) sets the bridge one layer too high, so its state after L is not S's
    from bridge_jspace import pins

    real = C.arm_edits

    def shifted(*args, **kwargs):
        arms = real(*args, **kwargs)
        prompt, edits = arms["b_blocks"]
        arms["b_blocks"] = (prompt, {la + 1: e for la, e in edits.items()})
        return arms

    monkeypatch.setattr(C, "arm_edits", shifted)
    with pytest.raises(SystemExit, match="BUG"):
        C.stage_run(f"{pins.RUN_PREFIX}fake_x47_bug", "test")
    assert (C.RESULTS / f"{pins.RUN_PREFIX}fake_x47_bug" / "outcomes.jsonl").exists()  # the files are written first


def test_verdict_on_the_fake_run_flags_nothing(fake_run, monkeypatch):
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "before L · 60%")
    out = C.stage_verdict([fake_run.out.name], n_boot=200)
    blob = json.loads((out / "x47_4.json").read_text())
    assert blob["flags"] == [] and blob["dan"] == "before L · 60%"
    m = blob["models"][0]
    assert m["status"] == "tested" and {x["status"] for x in blob["models"][1:]} == {"pending"}
    clean = m["cells"]["clean"]["lookup"]["all"]
    assert clean["n"] == 12 and clean["terms"]["propagation"][0] == 0.0
    assert clean["terms"]["pick_other"][0] == 0.0 and clean["rate"]["b"][0] == clean["rate"]["S"][0]
    md = (out / "x47_4.md").read_text()
    assert "BUG FLAG" not in md and "Q47.4" in md
    view = C.stage_view([fake_run.out.name])
    text = (view / "view.md").read_text()
    assert text.count("```") == 2 * 2 * X.K_EXAMPLES * len(X.READERS) and "⟦bridge:" in text and "⟦other:" in text
    fig = C.stage_figures(out)
    assert fig.exists()


# ---- the verdict on planted runs ----------------------------------------------------------------------------------


def test_decomposition_terms_sum_to_the_non_switch():
    n = 100
    sw = {a: [0] * n for a in C.ARMS}
    for arm, k in (("a", 40), ("b", 70), ("c", 70), ("d", 80), ("S", 100), ("b_blocks", 60)):
        sw[arm] = [int(i < k) for i in range(n)]
    d = C.decomposition(sw, [f"e{i % 10}" for i in range(n)], n_boot=500)
    t = d["terms"]
    assert t["before_L"][0] == pytest.approx(0.3) and t["propagation"][0] == pytest.approx(0.0)
    assert t["pick_other"][0] == pytest.approx(0.1) and t["outside"][0] == pytest.approx(0.2)
    assert sum(v[0] for v in t.values()) == pytest.approx(d["non_switch"][0]) == pytest.approx(0.6)
    assert d["largest"] == "before_L" and d["share_of_non_switch"]["before_L"] == pytest.approx(0.5)
    for v in [*t.values(), *d["rate"].values(), d["non_switch"]]:
        assert v[1] <= v[0] + 1e-12 and v[0] <= v[2] + 1e-12


def write_planted(root, name: str, target: str, flip_c: int = 0, clean_b_off: int = 0, n: int = 60) -> None:
    """A planted 47.4 run: per design n items (a third locker-first prefix-identical, a third locker-first with the
    other change first (main) or locker-after, a third mixed); both readers switch a at 20%, S always; in the main test
    b and c at 60%, d at 70%; in the clean design b, c and d always (S's own run); flip_c of the prefix-identical main
    items read (c) other than (b); clean_b_off clean items read (b) other than S (the lookup)."""
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "n_layers": 32,
                                                   "sources": {"main": "m", "clean": "c"}}))  # fmt: skip
    (src / "plan.json").write_text(json.dumps({d: {"items": n, "items_at_L": n, "source": d, "dropped": {}, "groups": {},
                                                   "upstream": {}, "entities": 10} for d in C.DESIGNS}))  # fmt: skip
    cases, rows, checks = [], [], []
    for design in C.DESIGNS:
        for i in range(n):
            third = i * 3 // n
            group = ("locker-first", "locker-first" if design == "main" else "locker-after", "mixed")[third]
            same = design == "clean" or third != 1
            scene = f"{design}{i}"
            cases.append({"scene": scene, "design": design, "stored": {"whole": {"PP": int(i % 5 == 0), "PM": 0}}})
            checks.append({"scene": scene, "design": design, "prefix_same": same, "gap_max": 0.0 if same else 0.3})
            for w in X.READERS:
                k = i % 10
                sw = {"none": 0, "a": int(k < 2), "b": int(k < 6), "c": int(k < 6), "d": int(k < 7), "b_blocks": int(k < 5),
                      "S": 1}  # fmt: skip
                if design == "clean":
                    sw |= {"b": 1, "c": 1, "d": 1}
                if design == "main" and same and group == "locker-first" and i < flip_c and w == X.LOOKUP:
                    sw["c"] = 1 - sw["c"]
                if design == "clean" and i < clean_b_off and w == X.LOOKUP:
                    sw["b"] = 1 - sw["b"]
                for arm, s in sw.items():
                    rows.append({"scene": scene, "entity": f"e{i % 10}", "design": design, "group": group,
                                 "upstream": not same, "prefix_same": same, "reader": w, "arm": arm, "switched": s,
                                 "role": "b" if s else "A"})  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "checks.jsonl", checks)


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "outside · 70%")
    write_planted(tmp_path, "r9", "qwen3.5-9b")
    write_planted(tmp_path, "r27", "qwen3.6-27b")
    out = C.stage_verdict(["r9", "r27"], n_boot=300)
    blob = json.loads((out / "x47_4.json").read_text())
    assert blob["flags"] == []
    m = {x["target"]: x for x in blob["models"]}
    assert m["muse-glimmer-30b"]["status"] == "pending"
    c = m["qwen3.5-9b"]["cells"]["main"]["lookup"]["locker-first"]
    assert c["n"] == 40 and c["rate"]["a"][0] == pytest.approx(0.2)
    assert c["terms"]["before_L"][0] == pytest.approx(0.4) and c["terms"]["outside"][0] == pytest.approx(0.3)
    assert c["largest"] == "before_L"
    first, after = (m["qwen3.5-9b"]["cells"]["main"]["lookup"][g] for g in C.SPLIT)
    assert first["n"] == after["n"] == 20 and C.SPLIT[0] not in m["qwen3.5-9b"]["cells"]["clean"]["lookup"]
    assert m["qwen3.5-9b"]["cells"]["clean"]["lookup"]["locker-after"]["n"] == 20
    assert m["qwen3.5-9b"]["cells"]["clean"]["lookup"]["all"]["n"] == 60
    s = m["qwen3.5-9b"]["checks"]["main lookup"]
    assert s["a_vs_stored_whole"]["n"] == 60 and s["S_reads_S"] == 60 and s["none_reads_O"] == 60
    assert "BUG FLAG" not in (out / "x47_4.md").read_text()


def test_verdict_flags_b_c_disagreement_and_clean_b_off_s(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "x")
    write_planted(tmp_path, "r9", "qwen3.5-9b", flip_c=2)  # 2 of 40 prefix-identical main items: 5% > 2%
    write_planted(tmp_path, "r27", "qwen3.6-27b", clean_b_off=3)  # 3 of 60 clean items: 5%
    out = C.stage_verdict(["r9", "r27"], n_boot=200)
    blob = json.loads((out / "x47_4.json").read_text())
    assert any("qwen3.5-9b: main lookup: (b) and (c) disagree on 2 of 40" in f for f in blob["flags"])
    assert any("qwen3.6-27b: clean lookup: (b) is S's own run" in f for f in blob["flags"])
    assert "<<< BUG FLAG: STOP AND REPORT >>>" in (out / "x47_4.md").read_text()


def test_one_disagreement_in_fifty_is_within_tolerance(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "x")
    write_planted(tmp_path, "r9", "qwen3.5-9b", flip_c=1, n=75)  # 1 of 50 prefix-identical main items: 2%
    blob = json.loads((C.stage_verdict(["r9"], n_boot=100) / "x47_4.json").read_text())
    assert blob["flags"] == []


def test_state_check_flags_only_prefix_identical_items():
    checks = [{"design": "main", "scene": "s1", "prefix_same": True, "gap_max": 0.0},
              {"design": "main", "scene": "s2", "prefix_same": False, "gap_max": 0.9},
              {"design": "clean", "scene": "s3", "prefix_same": True, "gap_max": 0.2}]  # fmt: skip
    assert C.state_flags(checks) == ["clean/s3"]
    assert "BUG FLAG" in C.state_line(checks) and "BUG FLAG" not in C.state_line(checks[:2])


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "")
    write_planted(tmp_path, "r9", "qwen3.5-9b")
    for stage in (lambda: C.stage_verdict(["r9"], n_boot=10), lambda: C.stage_view(["r9"]),
                  lambda: C.stage_figures(tmp_path)):  # fmt: skip
        with pytest.raises(AssertionError, match="sealed"):
            stage()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r9"]


def test_dan_answer_reads_only_the_q47_4_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.3** (47.3) ...\n\nDan: (a) · 60%\n\n**Q47.4** (47.4) ...\n\nRule: ...\n\nDan:{}\n\n**Q47.5** x\n\nDan: y\n"
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format("")))
    assert C.dan_answer() == ""
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format(" before L · 70%")))
    assert C.dan_answer() == "before L · 70%"


def test_the_committed_predictions_file_has_the_q47_4_block():
    # the real file at HEAD: the block exists (its answer may still be empty: the seal)
    text = C.subprocess.run(["git", "show", f"HEAD:{C.PREDICTIONS}"], cwd=C.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{C.QUESTION}**" in text and isinstance(C.dan_answer(), str)
