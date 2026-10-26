"""Batch 45, test 45b (scripts/x45b_binding.py): the locker-sentence positions and their O/S alignment (a fake tokenizer,
and the target's tokenizer when cached), the rule on planted outcomes, the verdict / examples stages on planted run
folders, and the run stage end to end on a tiny fake causal model (CPU). No real model."""

import json
import re
from types import SimpleNamespace

import pytest

from scripts import x0_necessity as X
from scripts import x45b_binding as B

ORG = ("The locker of nitrogen is 5. Julia picked hydrogen. The locker of hydrogen is 6. The locker of carbon is 4. "
       "Eva picked nitrogen. Mark picked carbon.")  # fmt: skip
ALT = ("The locker of nitrogen is 5. Julia picked carbon. The locker of hydrogen is 6. The locker of carbon is 4. "
       "Eva picked nitrogen. Mark picked hydrogen.")  # fmt: skip
LOCKERS = ["The locker of nitrogen is 5.", "The locker of hydrogen is 6.", "The locker of carbon is 4."]


def wrap(context: str) -> str:
    return f"<|im_start|>user\n{context}\nWhich locker belongs to Julia's pick?<|im_end|>\nAnswer: "


class WordTok:
    """Words with their leading whitespace as tokens (as byte-level BPE attaches a space), ids from a shared vocab."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


def positions(tok, context: str) -> tuple[list[int], list[list[int]], list[tuple[int, int]]]:
    text = wrap(context)
    enc = tok(text, return_offsets_mapping=True)
    return enc.input_ids, B.locker_positions(enc.offset_mapping, B.locker_spans(text, context)), enc.offset_mapping


# ---- positions and alignment --------------------------------------------------------------------------------------


def test_arm_layers_use_integer_division():
    assert B.arm_layers(12) == {"a": 12, "b_half": 6, "b_quarter": 3, "c": 12, "d": 6}
    assert B.arm_layers(32) == {"a": 32, "b_half": 16, "b_quarter": 8, "c": 32, "d": 16}


def test_locker_sentences_in_context_order():
    assert B.locker_sentences(ORG) == LOCKERS
    assert B.locker_sentences("Ann picked the cat. Bo picked the dog.") == []


def test_locker_positions_cover_each_sentence_exactly():
    tok = WordTok()
    text = wrap(ORG)
    _, pos, offsets = positions(tok, ORG)
    for sent, ps in zip(LOCKERS, pos, strict=True):
        assert ps == list(range(ps[0], ps[-1] + 1))  # contiguous
        assert text[offsets[ps[0]][0] : offsets[ps[-1]][1]].strip() == sent
        assert offsets[ps[-1] + 1][0] >= text.index(sent) + len(sent)  # nothing after the sentence's end


def test_two_picks_swapped_align_token_for_token():
    tok = WordTok()
    ids_o, pos_o, _ = positions(tok, ORG)
    ids_s, pos_s, _ = positions(tok, ALT)
    patched, source, how = B.align(pos_o, pos_s, ids_o, ids_s)
    assert how == "token" and patched == source == [p for s in pos_o for p in s]


def test_shifted_sentences_align_by_sentence():
    tok = WordTok()
    ids_o, pos_o, _ = positions(tok, ORG)
    longer = ALT.replace("Julia picked carbon.", "Julia picked the carbon.")  # one more token before two lockers
    ids_s, pos_s, _ = positions(tok, longer)
    patched, source, how = B.align(pos_o, pos_s, ids_o, ids_s)
    assert how == "sentence"
    assert patched == [p for s in pos_o for p in s]
    assert source[:6] == patched[:6] and source[6:] == [p + 1 for p in patched[6:]]  # 6 word tokens per sentence


def test_misaligned_sentences_are_dropped():
    tok = WordTok()
    ids_o, pos_o, _ = positions(tok, ORG)
    ids_s, pos_s, _ = positions(tok, ALT.replace("hydrogen is 6", "hydrogen is number 6"))
    with pytest.raises(B.Misaligned, match="locker sentence 1: 6 tokens in O, 7 in S"):
        B.align(pos_o, pos_s, ids_o, ids_s)
    fewer = "Julia picked carbon. The locker of hydrogen is 6. Eva picked nitrogen. Mark picked hydrogen."
    ids_f, pos_f, _ = positions(tok, fewer)
    with pytest.raises(B.Misaligned, match="3 locker sentences in O, 1 in S"):
        B.align(pos_o, pos_f, ids_o, ids_f)


def test_same_positions_other_ids_fall_back_to_sentence():
    tok = WordTok()
    ids_o, pos_o, _ = positions(tok, ORG)
    ids_s, pos_s, _ = positions(tok, ALT.replace("carbon is 4", "carbon is 7"))
    assert pos_o == pos_s
    assert B.align(pos_o, pos_s, ids_o, ids_s)[2] == "sentence"


def test_positions_on_the_targets_tokenizer():
    from scripts import statement_positions as SP

    try:
        tok = SP.load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    from bridge_jspace.tokens import raw_encoding

    enc = {}
    pos = {}
    for v, ctx in (("org", ORG), ("alt", ALT)):
        text = wrap(ctx)
        enc[v] = raw_encoding(tok, text, offsets=True)
        pos[v] = B.locker_positions(enc[v]["offset_mapping"], B.locker_spans(text, ctx))
        decoded = [tok.decode([enc[v]["input_ids"][p] for p in ps]).strip() for ps in pos[v]]
        assert decoded == LOCKERS
    patched, _, how = B.align(pos["org"], pos["alt"], enc["org"]["input_ids"], enc["alt"]["input_ids"])
    assert how == "token" and len(patched) == sum(map(len, pos["org"]))


def test_marked_brackets_spans_and_keeps_text():
    text = "a picked the frog. The locker of frog is 5."
    spans = [(12, 17), (19, 43)]  # ' frog' (its leading space) and the locker sentence
    out = B.marked(text, spans)
    assert out == "a picked the ⟦frog⟧. ⟦The locker of frog is 5.⟧"
    assert out.replace("⟦", "").replace("⟧", "") == text
    with pytest.raises(AssertionError):
        B.marked(text, [(0, 10), (5, 12)])


# ---- the rule on planted outcomes ---------------------------------------------------------------------------------


def planted(n: int, s: range | set, **arms: range | set) -> dict[str, list[int]]:
    """Per-item 0/1 switches: S switches the items in s, each named arm the items given, every other arm none."""
    out = {a: [0] * n for a in B.ARMS}
    out[B.S_ARM] = [int(i in s) for i in range(n)]
    for arm, idx in arms.items():
        out[arm] = [int(i in idx) for i in range(n)]
    return out


def ents(n: int, k: int = 10) -> list[str]:
    return [f"e{i % k}" for i in range(n)]


def verdict_of(sw: dict[str, list[int]]) -> dict:
    return B.rule(B.numbers(sw, ents(len(sw["S"])), n_boot=300))


def test_holds_when_the_locker_patch_switches_and_the_bridge_word_does_not():
    r = verdict_of(planted(40, range(40), c=range(25), d=range(5), a=range(8)))
    assert r["verdict"] == "holds" and r["c_at_least_half_of_S"] and not r["d_at_least_half_of_S"]


def test_thresholds_are_inclusive_and_d_alone_suffices():
    r = verdict_of(planted(40, range(40), c=range(10), d=range(20), a=range(10)))  # d exactly half, a exactly 0.25
    assert r["verdict"] == "holds" and r["d_at_least_half_of_S"] and r["a_at_most_0.25"]


def test_bridge_word_above_a_quarter_breaks_it():
    r = verdict_of(planted(40, range(40), c=range(30), d=range(30), a=range(11)))  # a = 0.275
    assert r["verdict"] == "does not hold" and not r["a_at_most_0.25"]


def test_locker_patch_below_half_breaks_it():
    r = verdict_of(planted(40, range(40), c=range(19), d=range(19)))
    assert r["verdict"] == "does not hold" and not (r["c_at_least_half_of_S"] or r["d_at_least_half_of_S"])


def test_half_is_of_the_lookups_s_switches_not_of_all_items():
    # S switches 20 of 40; c switches 20 items too, but only 8 of S's: 0.4 of S's switches (a ratio of rates would
    # say 1.0)
    sw = planted(40, range(20), c=range(12, 32))
    nums = B.numbers(sw, ents(40), n_boot=300)
    assert nums["hits_of_S"]["c"] == 8 and nums["of_S"]["c"][0] == pytest.approx(0.4)
    assert nums["rate"]["c"][0] == nums["rate"]["S"][0] == 0.5
    assert B.rule(nums)["verdict"] == "does not hold"


def test_cant_tell_when_s_switches_nothing():
    r = verdict_of(planted(40, set(), c=range(30)))
    assert r["verdict"].startswith("can't tell") and not r["holds"]


def test_intervals_bracket_the_point_and_are_clustered():
    sw = planted(60, range(60), c=range(0, 60, 2), a=range(6))
    nums = B.numbers(sw, ents(60, 12), n_boot=2000)
    for arm in B.ARMS:
        p, lo, hi = nums["rate"][arm]
        assert lo <= p <= hi
    assert nums["rate"]["S"] == [1.0, 1.0, 1.0]
    assert nums["of_S"]["c"][1] < 0.5 < nums["of_S"]["c"][2]
    assert nums["n"] == 60 and nums["entities"] == 12


# ---- stages on planted run folders --------------------------------------------------------------------------------


def item_record(
    i: int,
    tok: WordTok,
    org: str = ORG,
    alt: str = ALT,
    lockers: list[str] = LOCKERS,
    cf: tuple[str, str] = ("carbon", "4"),
) -> dict:
    """One 45b item as select() writes it, built with the fake tokenizer (O = ORG, S = ALT: two picks swapped; cf: S's
    bridge and answer)."""
    text_o, text_s = wrap(org), wrap(alt)
    enc = tok(text_o, return_offsets_mapping=True)
    enc_s = tok(text_s, return_offsets_mapping=True)
    pos_o = B.locker_positions(enc.offset_mapping, B.locker_spans(text_o, org))
    pos_s = B.locker_positions(enc_s.offset_mapping, B.locker_spans(text_s, alt))
    patched, source, how = B.align(pos_o, pos_s, enc.input_ids, enc_s.input_ids)
    bridge = next(j for j, (a, b) in enumerate(enc.offset_mapping) if text_o[a:b].strip() == "hydrogen.")
    marks = {"bridge": [list(enc.offset_mapping[bridge])],
             "lockers": [[enc.offset_mapping[s[0]][0], enc.offset_mapping[s[-1]][1]] for s in pos_o]}  # fmt: skip
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    readers = {w: {"id": f"{w}-{i}", "question": "Which locker belongs to Julia's pick?", "answer": "6",
                   "cf_answer": cf[1], "tok_A": digit["6"], "tok_b": digit[cf[1]],
                   "ids": {"org": enc.input_ids, "alt": enc_s.input_ids}, "text": {"org": text_o, "alt": text_s}}
               for w in X.READERS}  # fmt: skip
    return {"scene": f"s{i:03d}", "entity": f"e{i % 10}", "cf_bridge": cf[0], "domain": "elements", "pos": bridge,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ",
            "lockers": {"sentences": lockers, "org": pos_o, "alt": pos_s, "align": how},
            "patched": patched, "source": source, "marks": marks, "readers": readers,
            "stored": {"whole": {"12": {"PP": 0, "PM": 1}}, "S_read": {"PP": 1, "PM": 1}}}  # fmt: skip


def write_run(tmp_path, monkeypatch, sw: dict[str, list[int]]):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    n = len(sw["S"])
    tok = WordTok()
    items = [item_record(i, tok) for i in range(n)]
    layers = B.arm_layers(12)
    rows = []
    for i, it in enumerate(items):
        for w in X.READERS:
            for arm in B.ARMS:
                hit = sw[arm][i] if w == X.LOOKUP else 1
                rows.append({"scene": it["scene"], "entity": it["entity"], "reader": w, "arm": arm,
                             "layer": layers.get(arm), "switched": hit, "role": "b" if hit else "A",
                             "top": 4 if hit else 6, "top_text": "4" if hit else "6"})  # fmt: skip
    norms = [{"scene": it["scene"], "arm": arm, "delta_norm": 1.0} for it in items for arm in layers]
    manifest = {"model": {"target": "qwen3.5-9b"}, "main_run": "main", "layer": 12, "arm_layers": layers}
    (src / "manifest.json").write_text(json.dumps(manifest))
    plan = {"locker_after": n, "dropped": {}, "align": {"token": n}}
    (src / "plan.json").write_text(json.dumps(plan))
    for fname, data in (("outcomes.jsonl", rows), ("cases.jsonl", items), ("norms.jsonl", norms)):
        X.write_jsonl(src / fname, data)
    X.write_jsonl(src / "examples_greedy.jsonl", [])
    return src


@pytest.mark.parametrize(
    ("arms", "expected"),
    [({"c": range(15), "a": range(5)}, "holds"), ({"c": range(10), "d": range(14), "a": range(3)}, "does not hold")],
)
def test_verdict_stage_on_planted_runs(tmp_path, monkeypatch, arms, expected):
    src = write_run(tmp_path, monkeypatch, planted(30, range(30), **arms))
    out = B.stage_verdict("fake", n_boot=300)
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["rule"]["verdict"] == expected
    assert blob["readers"][X.LOOKUP]["n"] == 30 and blob["readers"][X.RECALL]["rate"]["c"][0] == 1.0
    # the rerun arm a against the stored whole arm (all 0 for the lookup) at L12; S against the stored S read (all 1)
    assert blob["checks"]["PP a vs stored whole at L12"] == {"n": 30, "agree": 25 if expected == "holds" else 27,
                                                            "rerun": 30 - (25 if expected == "holds" else 27), "stored": 0}  # fmt: skip
    assert blob["checks"]["PP S vs stored S read"]["agree"] == 30
    assert expected.upper() in (out / "verdict.md").read_text()
    assert src == out.parent


def test_examples_stage_marks_prompts_and_writes_once(tmp_path, monkeypatch):
    src = write_run(tmp_path, monkeypatch, planted(12, range(12), c=range(6)))
    path = B.stage_examples("fake", k=4, seed=0)
    blob = json.loads(path.read_text())
    assert len(blob["examples"]) == 4 * len(X.READERS)
    ex = blob["examples"][0]
    assert ex["prompt"] == wrap(ORG) + " "
    assert ex["prompt_marked"].count("⟦") == 1 + len(LOCKERS)
    assert "Julia picked ⟦hydrogen.⟧" in ex["prompt_marked"]  # the fake tokenizer's bridge token carries the period
    assert {s["role"] for s in ex["spans"]} == {"bridge_word", "patched_locker"}
    assert all(f"{a} " in " ".join(ex["numbers"]) for a in B.ARMS)
    assert (src / "examples.md").read_text().count("```") == 2 * 4 * len(X.READERS)
    with pytest.raises(AssertionError, match="written once"):
        B.stage_examples("fake", k=4, seed=0)


def test_stored_reads_list_scenes_seen_first_at_another_layer(tmp_path, monkeypatch):
    monkeypatch.setattr(X, "RESULTS", tmp_path)
    src = tmp_path / "main"
    src.mkdir()
    rows = [{"scene": s, "rendering": "chat", "arm": "whole", "layer": la, "reader": w, "switched": int(la == 12)}
            for la in (6, 12) for s in ("s2", "s1") for w in X.READERS]  # fmt: skip
    rows.append({"scene": "s1", "rendering": "chat", "arm": "none", "layer": 12, "reader": "PP", "switched": 0})
    X.write_jsonl(src / "outcomes.jsonl", rows)
    comp = [{"scene": s, "rendering": "chat", "reader": w, "variant": v, "read_right": True}
            for s in ("s1", "s2", "s3") for w in X.READERS for v in ("org", "alt")]  # fmt: skip
    X.write_jsonl(src / "competence.jsonl", comp)
    scenes, stored = B.stored_reads("main", 12)
    assert scenes == ["s2", "s1"] and set(stored) == {"s1", "s2"}
    assert stored["s1"] == {"whole": {"6": {"PP": 0, "PM": 0}, "12": {"PP": 1, "PM": 1}}, "S_read": {"PP": 1, "PM": 1}}


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model: each block mixes the running mean of the positions so far
    into every position; an edit acts on a block's output, as Model's hooks do."""

    def __init__(self, tok: WordTok, n_layers: int = 33, d: int = 8, vocab: int = 128):
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
            # linear, so a change keeps its size over 33 blocks (a squashing nonlinearity converges to a fixed point)
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


def test_run_stage_end_to_end_on_a_fake_model(tmp_path, monkeypatch):
    import torch

    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = [item_record(i, tok) for i in range(12)]
    fake = FakeModel(tok)
    counts = {"locker_after": 12, "dropped": {}, "align": {"token": 12}, "items": 12}
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(B, "select", lambda *_: (items, counts))
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x45b")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)  # the manifest records its inputs relative to the repo
    monkeypatch.setattr(B, "SPEC", tmp_path / "batch45.yaml")
    B.SPEC.write_text("")
    main = tmp_path / "x0" / B.MAIN_RUN[pins.TARGET]
    main.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "competence.jsonl"):
        (main / f).write_text("")
    out = B.stage_run("fake_run", "test")
    layer = X.PREDICTED[pins.TARGET]
    layers = B.arm_layers(layer)
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 12 * len(X.READERS) * len(B.ARMS)
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in items for w in X.READERS for a in B.ARMS
    }
    # the first read: O with the space token appended, under the six O arms, each edit at its layer and positions
    it, (seq, edits) = items[0], fake.calls[0]
    ids = it["readers"][X.LOOKUP]["ids"]
    assert seq == len(ids["org"]) + 1 and edits[0] == {}
    for e, arm in zip(edits[1:], B.O_ARMS[1:], strict=True):
        ((la, add),) = e.items()
        assert la == layers[arm]
        assert add.positions == ([it["pos"]] if arm in B.BRIDGE_ARMS else it["patched"])
    # the patch is h_S - h_O: O's state at every locker token becomes S's at that layer
    h = {v: fake.run(torch.tensor([ids[v]]), record=(layer,))[1][layer] for v in ("org", "alt")}
    c_edit = edits[B.O_ARMS.index("c")][layer]
    assert torch.allclose(h["org"][it["patched"]] + c_edit.delta, h["alt"][it["source"]])
    # the first locker sentence precedes the first change: its 6 tokens get a zero change (a no-op)
    c_norm = next(n for n in X.read_jsonl(out / "norms.jsonl") if n["scene"] == it["scene"] and n["arm"] == "c")
    assert c_norm["positions"] == 18 and c_norm["changed_positions"] == 12
    # S read on S: its own prompt, unedited
    assert fake.calls[1] == (len(ids["alt"]) + 1, [{}])
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == X.K_EXAMPLES * len(X.READERS) * len(B.ARMS)
    assert json.loads((out / "manifest.json").read_text())["arm_layers"] == layers
    # the CPU stages run on its output
    assert B.stage_examples("fake_run").exists()
    assert (B.stage_verdict("fake_run", n_boot=200) / "verdict.json").exists()


def test_sweep_layers_run_from_half_to_l_every_two():
    assert B.sweep_layers(12) == [6, 8, 10, 12]
    assert B.sweep_layers(32) == list(range(16, 33, 2))
    assert B.sweep_layers(13) == [6, 8, 10, 12, 13]  # L always included


def test_role_positions_split_each_locker_sentence():
    tok = WordTok()
    it = item_record(0, tok)
    roles = B.role_positions(tok, it)
    ids = it["readers"][X.LOOKUP]["ids"]["org"]
    # the fake tokenizer keeps the final '.' on the value's word: value and final are the same token there
    assert [tok.decode([ids[p]]).strip() for p in roles["item"][0]] == ["nitrogen", "hydrogen", "carbon"]
    assert [tok.decode([ids[p]]).strip() for p in roles["value"][0]] == ["5.", "6.", "4."]
    assert roles["final"][0] == roles["value"][0]
    assert all(p in it["patched"] for o, _ in roles.values() for p in o)
    assert roles["item"][1] == [it["source"][it["patched"].index(p)] for p in roles["item"][0]]


def test_role_positions_on_the_9b_items():
    # the real tokenizer on the 45b run's stored items (skipped where the tokenizer or the run is absent)
    from bridge_jspace import pins

    path = pins.RESULTS_DIR / "x45b_binding" / "qwen35_9b_x45b_binding" / "cases.jsonl"
    if not path.exists():
        pytest.skip("no 45b 9B run here")
    try:
        from scripts import statement_positions as SP

        tok = SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"no tokenizer: {e}")
    for it in X.read_jsonl(path)[:20]:
        roles = B.role_positions(tok, it)
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        n = len(it["lockers"]["sentences"])
        assert len(roles["final"][0]) == n and all(tok.decode([ids[p]]) == "." for p in roles["final"][0])
        items = [B.LOCKER_RE.match(s).group(1) for s in it["lockers"]["sentences"]]  # type: ignore[union-attr]
        assert "".join(tok.decode([ids[p]]) for p in roles["item"][0]).split() == " ".join(items).split()


def test_sweep_stage_end_to_end_on_a_fake_model(tmp_path, monkeypatch):
    import torch

    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    items = [item_record(i, tok) for i in range(12)]
    fake = FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(B, "select", lambda *_: (items, {"items": 12}))
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x45b")
    monkeypatch.setattr(B, "same_after_bridge", lambda it: True)  # the fake items swap a later pick too
    out = B.stage_sweep("fake_sweep", "test")
    layer = X.PREDICTED[pins.TARGET]
    layers = B.sweep_layers(layer)
    arms = ["none", *(f"{s}{la}" for la in layers for s in B.SWEEP_ARMS), "S"]
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in items for w in X.READERS for a in arms
    }
    assert {r["layer"] for r in rows if r["arm"].startswith("ls")} == set(layers)
    # each sweep edit sits at its layer and positions; ls<l> makes O's locker tokens S's at l
    it, (_, edits) = items[0], fake.calls[0]
    ids = it["readers"][X.LOOKUP]["ids"]
    where = {"bw": [it["pos"]], "ls": it["patched"],
             **{arm: it["roles"][role]["org"] for role, arm in B.ROLE_ARM.items()}}  # fmt: skip
    for e, arm in zip(edits[1:], arms[1:-1], strict=True):
        ((la, add),) = e.items()
        assert la == int(arm[2:]) and add.positions == where[arm[:2]]
    la = layers[0]
    h = {v: fake.run(torch.tensor([ids[v]]), record=(la,))[1][la] for v in ("org", "alt")}
    assert torch.allclose(h["org"][it["patched"]] + edits[arms.index(f"ls{la}")][la].delta, h["alt"][it["source"]])
    cells = json.loads((B.stage_sweep_table("fake_sweep", n_boot=200) / "sweep.json").read_text())["cells"]
    assert [c["layer"] for c in cells[X.LOOKUP]] == layers and all(c["n"] == 12 for c in cells[X.RECALL])


# ---- Dan's sanity check and 45n -------------------------------------------------------------------------------------


def _ids_item(scene: str, org: list[int], alt: list[int], pos: int) -> dict:
    return {"scene": scene, "pos": pos, "readers": {w: {"ids": {"org": org, "alt": alt}} for w in X.READERS}}


def test_same_after_bridge():
    assert B.same_after_bridge(_ids_item("a", [1, 2, 3, 4], [1, 9, 3, 4], 1))  # only the bridge differs
    assert B.same_after_bridge(_ids_item("b", [5, 2, 3, 4], [6, 9, 3, 4], 1))  # the other pick comes first
    assert not B.same_after_bridge(_ids_item("c", [1, 2, 3, 4], [1, 9, 3, 7], 1))  # a later token differs
    assert not B.same_after_bridge(_ids_item("d", [1, 2, 3, 4], [1, 9, 3], 1))  # lengths differ
    # the fake items swap Julia's pick (the bridge) and Mark's, which comes later: they fail
    assert not B.same_after_bridge(item_record(0, WordTok()))
    keep, counts = B.sane([_ids_item("a", [1, 2], [1, 3], 1), _ids_item("c", [1, 2, 3], [1, 9, 7], 1)])
    assert keep == {"a"} and counts == {"items": 2, "pass": 1, "dropped": 1}


def test_link_parts_share_and_zero_rows():
    import torch

    from scripts import statement_positions as SP

    g = torch.Generator().manual_seed(3)
    d = 24
    jdic = torch.randn(60, d, generator=g)
    jdic = jdic / jdic.norm(dim=1, keepdim=True)
    delta = torch.randn(5, d, generator=g)
    delta[2] = 0
    basis = SP.random_basis(d, torch.Generator().manual_seed(0))
    part, rand, share = B.link_parts(delta, jdic, basis, k=4)
    assert float(part[2].abs().max()) == 0 and float(rand[2].abs().max()) == 0
    live = [0, 1, 3, 4]
    assert ((share[live] > 0) & (share[live] <= 1 + 1e-6)).all()
    # the random part holds the same share to within one basis direction
    rshare = rand.norm(dim=-1) ** 2 / delta.norm(dim=-1).clamp_min(1e-30) ** 2
    one = ((delta @ basis) ** 2 / delta.norm(dim=-1, keepdim=True).clamp_min(1e-30) ** 2).max(dim=-1).values
    assert ((rshare[live] - share[live]).abs() <= one[live] + 1e-5).all()


def test_link_stage_end_to_end_on_a_fake_model(tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M

    class FakeLens:
        def __init__(self, model, name):
            pass

        def vectors(self, layer, ids):
            v = torch.randn(40, 8, generator=torch.Generator().manual_seed(layer))
            return v / v.norm(dim=1, keepdim=True)

    tok = WordTok()
    items = [item_record(i, tok) for i in range(10)]
    fake = FakeModel(tok)
    fake.letter_token_ids = lambda: list(range(40))
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(B, "select", lambda *_: (items, {"items": 10}))
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x45b")
    out = B.stage_link("fake_link", "test")
    rows = X.read_jsonl(out / "outcomes.jsonl")
    arms = ["none", *B.LINK_ARMS, "S"]
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in items for w in X.READERS for a in arms
    }
    # c is 45b's full copy: O's locker tokens become S's; c_nojpp and c_norand subtract parts of it at the same tokens
    it, (_, edits) = items[0], fake.calls[0]
    ids = it["readers"][X.LOOKUP]["ids"]
    la = X.PREDICTED[__import__("bridge_jspace.pins", fromlist=["TARGET"]).TARGET]
    h = {v: fake.run(torch.tensor([ids[v]]), record=(la,))[1][la] for v in ("org", "alt")}
    full = edits[arms.index("c")][la]
    assert full.positions == it["patched"] and torch.allclose(
        h["org"][it["patched"]] + full.delta, h["alt"][it["source"]]
    )
    assert all(edits[arms.index(a)][la].positions == it["patched"] for a in ("c_nojpp", "c_norand"))
    assert len(X.read_jsonl(out / "norms.jsonl")) == 10


def test_link_rule():
    assert B.link_rule({"c": 0.6, "c_nojpp": 0.5, "c_norand": 0.55})  # 0.5 >= 0.48 and >= 0.45
    assert not B.link_rule({"c": 0.6, "c_nojpp": 0.45, "c_norand": 0.5})  # under 0.8 of the full copy
    assert not B.link_rule({"c": 0.5, "c_nojpp": 0.45, "c_norand": 0.6})  # more than 0.1 under the random part's
    assert B.link_rule({"c": 0.5, "c_nojpp": 0.4, "c_norand": 0.5})  # exactly at both bars


def test_link_verdict_on_planted_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    for name, target, nojpp in (("r9", "qwen3.5-9b", 1), ("r27", "qwen3.6-27b", 0)):
        src = tmp_path / name
        src.mkdir()
        (src / "manifest.json").write_text(json.dumps({"model": {"target": target}}))
        cases = [_ids_item(f"s{i}", [1, 2, 3], [1, 9, 3] if i < 18 else [1, 9, 7], 1) for i in range(20)]
        X.write_jsonl(src / "cases.jsonl", cases)
        rows = []
        for i in range(20):
            for w in X.READERS:
                for arm, sw in (("none", 0), ("c", 1), ("c_nojpp", nojpp), ("c_norand", 1), ("S", 1)):
                    rows.append({"scene": f"s{i}", "entity": f"e{i % 5}", "reader": w, "arm": arm, "switched": sw})
        X.write_jsonl(src / "outcomes.jsonl", rows)
    blob = json.loads((B.stage_link_verdict(["r9", "r27"], n_boot=100) / "x45n.json").read_text())
    assert blob["runs"]["r9"]["sanity"] == {"items": 20, "pass": 18, "dropped": 2}
    assert blob["runs"]["r9"]["holds"] and not blob["runs"]["r27"]["holds"]
    assert blob["verdict"] == "not outside the lens"
    other = tmp_path / "only9b"  # a second root: verdict folders are named by the second
    other.mkdir()
    (other / "r9").symlink_to(tmp_path / "r9")
    monkeypatch.setattr(B, "RESULTS", other)
    assert json.loads((B.stage_link_verdict(["r9"], n_boot=100) / "x45n.json").read_text())["verdict"] == "pending"


# ---- 45q: 45m's clean scenes, the rest role, the run, the rule over three models ------------------------------------

# 45m's design on the fake scene: a locker item nobody picks (oxygen) is added to both prompts; S changes Julia's pick
# to it, so only the bridge token differs
FRESH_ORG = ("The locker of nitrogen is 5. Julia picked hydrogen. The locker of oxygen is 7. The locker of hydrogen is 6. "
             "The locker of carbon is 4. Eva picked nitrogen. Mark picked carbon.")  # fmt: skip
FRESH_ALT = FRESH_ORG.replace("Julia picked hydrogen.", "Julia picked oxygen.")
FRESH_LOCKERS = ["The locker of nitrogen is 5.", "The locker of oxygen is 7.", "The locker of hydrogen is 6.",
                 "The locker of carbon is 4."]  # fmt: skip


def fresh_record(i: int, tok: WordTok) -> dict:
    it = item_record(i, tok, FRESH_ORG, FRESH_ALT, FRESH_LOCKERS, ("oxygen", "7"))
    feats = {"org locker vs asked pick": "after", "alt locker vs asked pick": "after"}
    return {**it, "features": feats, "fresh": {"item": "oxygen", "digit": 7, "sentence": FRESH_LOCKERS[1]}}


def test_role_positions_rest_is_opt_in_and_partitions_the_locker_tokens():
    tok = WordTok()
    it = item_record(0, tok)
    old, new = B.role_positions(tok, it), B.role_positions(tok, it, rest=True)
    assert set(old) == {"item", "value", "final"}  # unchanged unless asked: the 45b sweep's roles
    assert {r: new[r] for r in old} == old and set(new) == {*old, "rest"}
    ids = it["readers"][X.LOOKUP]["ids"]["org"]
    assert [tok.decode([ids[p]]).strip() for p in new["rest"][0]] == ["The", "locker", "of", "is"] * len(LOCKERS)
    # every locker token has a role; rest shares none with the other three
    assert set().union(*(set(o) for o, _ in new.values())) == set(it["patched"])
    assert not set(new["rest"][0]) & set().union(*(set(o) for o, _ in old.values()))
    assert new["rest"][1] == [it["source"][it["patched"].index(p)] for p in new["rest"][0]]


def test_q_sweep_layers_run_to_the_last_lens_layer():
    assert B.q_sweep_layers(32) == [0, 4, 8, 12, 16, 20, 24, 28, 30]  # the 9B: block 31's output is read by nothing
    assert B.q_sweep_layers(64) == [*range(0, 61, 4), 62]
    assert B.q_sweep_layers(52) == [*range(0, 49, 4), 50]
    assert B.q_sweep_layers(34) == list(range(0, 33, 4))  # the last layer once


def test_q_arms_order_and_layers():
    sweep = [0, 4, 6]
    arms = B.q_arms(12, sweep)
    assert list(arms)[: len(B.O_ARMS)] == list(B.O_ARMS)
    assert list(arms)[len(B.O_ARMS) : len(B.O_ARMS) + 2] == ["c_nojpp", "c_norand"]
    assert len(arms) == len(B.O_ARMS) + 2 + len(B.Q_SWEEP_ARMS) * len(sweep)
    assert arms["b_quarter"] == ("45b", 3) and arms["c_norand"] == ("45n", 12) and arms["lr6"] == ("sweep", 6)
    assert arms["none"] == ("-", None)


def test_answered_and_the_seal(tmp_path, monkeypatch):
    path = tmp_path / "pred.md"
    path.write_text("**Q45.11** old\n\nDan: yes · 70%; no · 30%\n\n**Q45.12** (45q) new\n- (a) yes\n\nDan:\n\n"
                    "**Q45.13** (45p)\n\nDan: \n")  # fmt: skip
    assert B.answered("Q45.11", path) and not B.answered("Q45.12", path) and not B.answered("Q45.13", path)
    monkeypatch.setattr(B, "PREDICTIONS", path)
    for argv in (["q-verdict", "--names", "r"], ["q-sweep-table", "--names", "r"], ["q-link-table", "--names", "r"]):
        monkeypatch.setattr("sys.argv", ["x45b_binding.py", *argv])
        with pytest.raises(SystemExit, match="45q is sealed"):
            B.main()
    # 45b's own CPU stages on a 45q run are sealed too
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    (tmp_path / "qrun").mkdir()
    (tmp_path / "qrun" / "manifest.json").write_text(json.dumps({"test": "45q"}))
    for stage in ("verdict", "examples", "sweep-table"):
        monkeypatch.setattr("sys.argv", ["x45b_binding.py", stage, "--name", "qrun"])
        with pytest.raises(SystemExit, match="45q is sealed"):
            B.main()
    path.write_text(path.read_text().replace("Dan:\n\n**Q45.13", "Dan: yes · 60%\n\n**Q45.13"))
    assert B.answered("Q45.12", path)
    B.unsealed()  # no exit once Dan's answer is in


def test_select_checks_the_runs_alt():
    from bridge_jspace import pins

    main, fresh = B.MAIN_RUN[pins.TARGET], B.FRESH_RUN[pins.TARGET]
    if not all((X.RESULTS / r / "manifest.json").exists() for r in (main, fresh)):
        pytest.skip("the target's main or 45m run is not here")
    layer = X.PREDICTED[pins.TARGET]
    with pytest.raises(AssertionError, match="not a 45m run"):
        B.select(None, main, layer, "45m")
    with pytest.raises(AssertionError, match="not the main test's alt"):
        B.select(None, fresh, layer)
    with pytest.raises(AssertionError, match="source"):
        B.select(None, fresh, layer, "fresh")


def real_tokenizer():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


def test_select_main_source_matches_the_stored_45b_run():
    # existing behaviour: select() (source main) gives exactly the items the 45b run stored
    from bridge_jspace import pins

    run = {"qwen3.5-9b": "qwen35_9b_x45b_binding", "qwen3.6-27b": "x45b_binding_27b",
           "muse-glimmer-30b": "muse30b_x45b_binding"}[pins.TARGET]  # fmt: skip
    path = B.RESULTS / run / "cases.jsonl"
    if not path.exists() or not (X.RESULTS / B.MAIN_RUN[pins.TARGET] / "cases.jsonl").exists():
        pytest.skip("the target's 45b run or main run is not here")
    tok = real_tokenizer()
    items, counts = B.select(tok, B.MAIN_RUN[pins.TARGET], X.PREDICTED[pins.TARGET])
    assert json.loads(json.dumps(items)) == X.read_jsonl(path)
    assert "source" not in counts and counts["items"] == len(items)


def test_select_fresh_items_on_the_targets_tokenizer():
    from bridge_jspace import pins

    run = B.FRESH_RUN[pins.TARGET]
    if not (X.RESULTS / run / "cases.jsonl").exists():
        pytest.skip("the target's 45m run is not here")
    tok = real_tokenizer()
    before = (X.ALT, X.RENDERINGS)
    items, counts = B.select(tok, run, X.PREDICTED[pins.TARGET], "45m")
    assert before == (X.ALT, X.RENDERINGS)  # the fresh alt only inside select
    assert items and counts["source"] == "45m" and counts["items"] == len(items)
    assert counts["dropped"] == {} and counts["align"] == {"token": len(items)}  # by construction: one token differs
    assert counts["locker_after"] == len(items) <= counts["main_items"]
    for it in items:
        assert it["features"]["org locker vs asked pick"] == "after"
        assert B.same_after_bridge(it)
        for rd in it["readers"].values():  # only the bridge token differs
            o, s = rd["ids"]["org"], rd["ids"]["alt"]
            assert [k for k in range(len(o)) if o[k] != s[k]] == [it["pos"]]
            assert all(it["fresh"]["sentence"] in rd["text"][v] for v in ("org", "alt"))
        assert it["fresh"]["sentence"] in it["lockers"]["sentences"] and len(it["lockers"]["sentences"]) == 4
    for it in items[:25]:
        roles = B.role_positions(tok, it, rest=True)
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        assert set().union(*(set(o) for o, _ in roles.values())) == set(it["patched"])
        others = set(roles["item"][0]) | set(roles["value"][0]) | set(roles["final"][0])
        assert not set(roles["rest"][0]) & others
        rest = "".join(tok.decode([ids[p]]) for p in roles["rest"][0])
        assert set(rest.split()) <= {"The", "locker", "of", "the", "is"}, rest
        assert all(tok.decode([ids[p]]).strip() == "." for p in roles["final"][0])


class FakeJpp:
    """A stand-in for bridge_jspace.lens.JLens: 40 unit atoms per layer (seeded by the layer)."""

    def __init__(self, model=None, name="jpp"):
        pass

    def vectors(self, layer, ids):
        import torch

        v = torch.randn(40, 8, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def test_q_run_end_to_end_on_a_fake_model(tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import statement_positions as SP

    tok = WordTok()
    items = [fresh_record(i, tok) for i in range(10)]
    assert all(B.same_after_bridge(it) for it in items)
    fake = FakeModel(tok, n_layers=pins.N_LAYERS)
    monkeypatch.setattr(fake, "letter_token_ids", lambda: list(range(40)), raising=False)
    calls = []

    def fake_select(*args):
        calls.append(args[1:])
        return items, {"items": len(items), "locker_after": len(items), "dropped": {}, "align": {"token": 10}}

    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeJpp)
    monkeypatch.setattr(B, "select", fake_select)
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x45b")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(B, "SPEC", tmp_path / "batch45.yaml")
    B.SPEC.write_text("")
    fresh = tmp_path / "x0" / B.FRESH_RUN[pins.TARGET]
    fresh.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "competence.jsonl"):
        (fresh / f).write_text("")
    name = f"{pins.RUN_PREFIX}fake_q"  # the target's run prefix: the test runs under any BJ_TARGET
    out = B.stage_q(name, "test")
    layer = X.PREDICTED[pins.TARGET]
    sweep = B.q_sweep_layers(pins.N_LAYERS)
    arms = B.q_arms(layer, sweep)
    assert calls == [(B.FRESH_RUN[pins.TARGET], layer, "45m")]
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "45q" and m["sweep_layers"] == sweep and m["arm_layers"] == B.arm_layers(layer)
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in items for w in X.READERS for a in (*arms, "S")
    }
    assert len(rows) == len(items) * len(X.READERS) * (len(arms) + 1)
    fam = {r["arm"]: (r["family"], r["layer"]) for r in rows}
    assert fam == {**arms, "S": ("-", None)}
    # the first O read's edits (X.read_logits may split them over several batched calls)
    edits: list[dict] = []
    for _, e in fake.calls:
        edits += e
        if len(edits) >= len(arms):
            break
    assert len(edits) == len(arms) and edits[0] == {}
    it = X.read_jsonl(out / "cases.jsonl")[0]
    where = {"a": [it["pos"]], "b_half": [it["pos"]], "b_quarter": [it["pos"]], "c": it["patched"], "d": it["patched"],
             "c_nojpp": it["patched"], "c_norand": it["patched"], "bw": [it["pos"]], "ls": it["patched"],
             **{k: it["roles"][role]["org"] for role, k in B.Q_ROLE_ARM.items()}}  # fmt: skip
    for arm, e in zip(list(arms)[1:], edits[1:], strict=True):
        ((la, add),) = e.items()
        assert la == arms[arm][1] and add.positions == where.get(arm, where.get(arm[:2])), arm
    ids = it["readers"][X.LOOKUP]["ids"]
    rec = (layer, sweep[1])
    h = {v: fake.run(torch.tensor([ids[v]]), record=rec)[1] for v in ("org", "alt")}
    by = dict(zip(arms, edits, strict=True))
    # c, ls<l> and lr<l> make O's states at their tokens S's; the first locker sentence precedes the change
    assert torch.allclose(h["org"][layer][it["patched"]] + by["c"][layer].delta, h["alt"][layer][it["source"]])
    la = sweep[1]
    rest = it["roles"]["rest"]
    assert torch.allclose(h["org"][la][rest["org"]] + by[f"lr{la}"][la].delta, h["alt"][la][rest["alt"]])
    # c_nojpp / c_norand: the copy at L without each token's J++ part / without the random part of its share
    delta = h["alt"][layer][it["source"]] - h["org"][layer][it["patched"]]
    basis = SP.random_basis(delta.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer))
    part, rand, _ = B.link_parts(delta, FakeJpp().vectors(layer, None), basis)
    assert torch.allclose(by["c_nojpp"][layer].delta, delta - part, atol=1e-5)
    assert torch.allclose(by["c_norand"][layer].delta, delta - rand, atol=1e-5)
    norms = X.read_jsonl(out / "norms.jsonl")
    c_norm = next(n for n in norms if n["scene"] == it["scene"] and n["arm"] == "c")
    assert c_norm["positions"] == 24 and c_norm["changed_positions"] == 18
    assert len(norms) == len(items) * (len(B.BRIDGE_ARMS) + len(B.LOCKER_ARMS) + 1)
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == len(items) * len(X.READERS) * len(B.ARMS)
    # the CPU stages (run by hand after Dan's answer) read it
    v = json.loads((B.stage_q_verdict([name], n_boot=100) / "x45q.json").read_text())
    (model,) = v["models"]
    assert model["sanity"] == {"items": 10, "pass": 10, "dropped": 0} and model["readers"][X.LOOKUP]["n"] == 10
    assert v["verdict"]["label"] == "pending" and pins.TARGET not in v["verdict"]["missing"]
    link = json.loads((B.stage_q_link_table([name], n_boot=100) / "link.json").read_text())
    assert set(link["runs"][name]["readers"][X.LOOKUP]) == {"none", "c", "c_nojpp", "c_norand", "S"}
    cells = json.loads((B.stage_q_sweep_table([name], n_boot=100) / "sweep.json").read_text())["runs"][name]
    assert [c["layer"] for c in cells["cells"][X.LOOKUP]] == sweep
    assert {"bw", "ls", "li", "lr", "lv", "lf", "lr_of_S"} <= set(cells["cells"][X.LOOKUP][0])
    assert B.stage_examples(name).exists()


def write_q_run(root, name: str, target: str, lookup: dict | None, n: int = 20) -> None:
    """A planted 45q run of n items passing the sanity check; lookup: the items each arm switches (the recall none);
    None: the run has no outcomes yet."""
    src = root / name
    src.mkdir()
    layer = X.PREDICTED[target]
    (src / "manifest.json").write_text(json.dumps({"test": "45q", "model": {"target": target}, "main_run": "m45",
                                                   "layer": layer, "arm_layers": B.arm_layers(layer)}))  # fmt: skip
    (src / "plan.json").write_text(json.dumps({"locker_after": n, "dropped": {}, "items": n, "align": {"token": n}}))
    cases = [{**_ids_item(f"s{i}", [1, 2, 3], [1, 9, 3], 1), "stored": {"whole": {}, "S_read": {}}} for i in range(n)]
    X.write_jsonl(src / "cases.jsonl", cases)
    if lookup is None:
        return
    rows = [{"scene": f"s{i}", "entity": f"e{i % 5}", "reader": w, "arm": a, "family": "-",
             "switched": int(w == X.LOOKUP and i in lookup.get(a, ()))}
            for i in range(n) for w in X.READERS for a in B.ARMS]  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)


HOLDS = {"S": range(20), "c": range(12), "a": range(3)}  # c 0.6 of S's switches, a 0.15
FAILS = {"S": range(20), "c": range(5), "d": range(9), "a": range(10)}  # neither copy reaches half; a 0.5
NO_S = {"c": range(10)}  # S switches no lookup: not tested


@pytest.mark.parametrize(
    ("plants", "label", "not_tested"),
    [
        ((HOLDS, HOLDS, FAILS), "holds", []),
        ((HOLDS, NO_S, FAILS), "does not hold", ["r27"]),
        ((HOLDS, HOLDS, None), "pending", []),
        ((HOLDS, HOLDS, "empty"), "holds", ["rmuse"]),
        ((FAILS, "empty", HOLDS), "does not hold", ["r27"]),
    ],
)
def test_q_verdict_two_of_three(tmp_path, monkeypatch, plants, label, not_tested):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    names = ["r9", "r27", "rmuse"]
    for name, target, plant in zip(names, B.Q_MODELS, plants, strict=True):
        write_q_run(tmp_path, name, target, {} if plant == "empty" else plant, 0 if plant == "empty" else 20)
    v = json.loads((B.stage_q_verdict(names, n_boot=200) / "x45q.json").read_text())
    assert v["verdict"]["label"] == label and v["verdict"]["not_tested"] == not_tested
    assert v["verdict"]["q45_12"] == {"holds": "(a) yes", "does not hold": "(b) no", "pending": "pending"}[label]
    status = {m["run"]: m["status"] for m in v["models"]}
    for name, plant in zip(names, plants, strict=True):
        expect = "pending" if plant is None else "not tested" if plant in ("empty", NO_S) else "tested"
        assert status[name] == expect
    by = {m["run"]: m for m in v["models"]}
    if plants[0] is HOLDS:
        assert by["r9"]["holds"] and by["r9"]["readers"][X.LOOKUP]["of_S"]["c"][0] == pytest.approx(0.6)


def test_q_verdict_refuses_two_runs_of_one_model(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    for name in ("a", "b"):
        write_q_run(tmp_path, name, "qwen3.5-9b", HOLDS)
    with pytest.raises(AssertionError, match="two runs of one model"):
        B.stage_q_verdict(["a", "b"], n_boot=100)
