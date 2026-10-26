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


def item_record(i: int, tok: WordTok) -> dict:
    """One 45b item as select() writes it, built with the fake tokenizer (O = ORG, S = ALT: two picks swapped)."""
    text_o, text_s = wrap(ORG), wrap(ALT)
    enc = tok(text_o, return_offsets_mapping=True)
    enc_s = tok(text_s, return_offsets_mapping=True)
    pos_o = B.locker_positions(enc.offset_mapping, B.locker_spans(text_o, ORG))
    pos_s = B.locker_positions(enc_s.offset_mapping, B.locker_spans(text_s, ALT))
    patched, source, how = B.align(pos_o, pos_s, enc.input_ids, enc_s.input_ids)
    bridge = next(j for j, (a, b) in enumerate(enc.offset_mapping) if text_o[a:b].strip() == "hydrogen.")
    marks = {"bridge": [list(enc.offset_mapping[bridge])],
             "lockers": [[enc.offset_mapping[s[0]][0], enc.offset_mapping[s[-1]][1]] for s in pos_o]}  # fmt: skip
    digit = {d: tok(d).input_ids[0] for d in "0123456789"}
    readers = {w: {"id": f"{w}-{i}", "question": "Which locker belongs to Julia's pick?", "answer": "6",
                   "cf_answer": "4", "tok_A": digit["6"], "tok_b": digit["4"],
                   "ids": {"org": enc.input_ids, "alt": enc_s.input_ids}, "text": {"org": text_o, "alt": text_s}}
               for w in X.READERS}  # fmt: skip
    return {"scene": f"s{i:03d}", "entity": f"e{i % 10}", "cf_bridge": "carbon", "domain": "elements", "pos": bridge,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))], "read_suffix": " ",
            "lockers": {"sentences": LOCKERS, "org": pos_o, "alt": pos_s, "align": how},
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
