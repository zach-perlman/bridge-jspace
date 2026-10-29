"""Batch 53, test 53.1 (scripts/x53_2x2.py): the Q-after number cell is the main test byte for byte, the Q-before cells
move only the question (the scene text and the bridge token unchanged), the word cells change only the recall's
instruction and read, the relation rule's choice, and the rules across cells on planted labels. No GPU."""

import pytest

from scripts import x0_necessity as X
from scripts import x53_2x2 as T2

LK, RC = X.LOOKUP, X.RECALL
N_PAIRS = 40  # scenes checked against the main test's own builder (the full 600 are checked by `plan`)


def _tok():
    from scripts import statement_positions as SP

    try:
        return SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


@pytest.fixture(scope="module")
def tok():
    return _tok()


@pytest.fixture(scope="module")
def all_pairs():
    return T2.scene_pairs()[:N_PAIRS]


@pytest.fixture(scope="module")
def pairs(tok, all_pairs):
    """The scenes every cell builds on this tokenizer (Lightning's drops a bridge split in two)."""
    return [p for p in all_pairs if all(T2.cell_case(tok, p, c)[0] is not None for c in T2.CELLS)]


def _case(tok, p: dict, cell: str) -> dict:
    c, why = T2.cell_case(tok, p, cell)
    assert c is not None, why
    return c


def _buildable(tok, n: int) -> list[dict]:
    """The first n scenes every cell builds on this tokenizer."""
    out = []
    for p in T2.scene_pairs():
        if all(T2.cell_case(tok, p, c)[0] is not None for c in T2.CELLS):
            out.append(p)
        if len(out) == n:
            return out
    raise AssertionError(f"fewer than {n} scenes build")


# ---- prompts --------------------------------------------------------------------------------------------------------


def test_user_content_moves_only_the_question():
    q, ctx = "Which locker belongs to Ann's pick?", "The locker of the duck is 4. Ann picked the duck."
    after, before = (T2.user_content(q, ctx, "digit", p) for p in ("after", "before"))
    assert after == f"{ctx}\n{q} Answer with a single digit and nothing else."
    assert before == f"Question: {q} Answer with a single digit and nothing else.\n\nScene:\n{ctx}"
    word = T2.user_content(q, ctx, "word", "after")
    assert word == f"{ctx}\n{q} {T2.WORD_INSTRUCTION}"
    with pytest.raises(AssertionError):
        T2.user_content(q, ctx, "digit", "middle")


def test_qa_num_is_the_main_test_byte_for_byte(tok, all_pairs):
    """(Q-after, number) = x0_necessity's chat cases: the same scenes dropped, the same ids for both readers in O and S,
    the same bridge position and read tokens, one Δ from the lookup's prompts."""
    for p in all_pairs:
        ref, _ = X.scene_case(tok, p, "chat")
        mine, _ = T2.cell_case(tok, p, "qa_num")
        assert (ref is None) == (mine is None), p[LK]["scene"]
        if ref is None or mine is None:
            continue
        assert mine["pos"] == ref["pos"]
        for w in X.READERS:
            assert mine["readers"][w]["ids"] == ref["readers"][w]["ids"], (p[LK]["scene"], w)
            assert mine["readers"][w]["set_A"] == [ref["readers"][w]["tok_A"]]
            assert mine["readers"][w]["set_b"] == [ref["readers"][w]["tok_b"]]
            assert mine["readers"][w]["suffix"] == ref["space"]
            assert mine["readers"][w]["src"] == LK
        text = X.render(tok, p[RC], "chat", p[RC]["context"])
        assert text == T2.render(tok, p[RC]["question"], p[RC]["context"], "digit", "after")


def _context_pos(tok, ids: list[int], context: str) -> list[int]:
    """The positions of the context's tokens in a prompt (by character offsets of the decoded prompt)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    text = tok.decode(ids)
    enc = raw_encoding(tok, text, offsets=True)
    assert list(enc["input_ids"]) == ids
    a = text.index(context)
    return SP.tokens_in(enc["offset_mapping"], a, a + len(context))


def _context_ids(tok, ids: list[int], context: str) -> list[int]:
    return [ids[i] for i in _context_pos(tok, ids, context)]


def test_q_before_keeps_the_scene_and_the_bridge_token(tok, pairs):
    """Q-before vs Q-after per reader and prompt: the scene text once and unchanged, its tokens the same, the bridge the
    same token at the same offset from the scene's start; only the question block moved (and the 'Scene:' label)."""
    for cell_b, cell_a in (("qb_num", "qa_num"), ("qb_word", "qa_word")):
        for p in pairs[:10]:
            a, b = _case(tok, p, cell_a), _case(tok, p, cell_b)
            for w in X.READERS:
                ra, rb = a["readers"][w], b["readers"][w]
                assert rb["src"] == w  # per-reader Δ: the readers' prompts differ before the bridge
                for v, ctx in (("org", p[w]["context"]), ("alt", p[w]["cf_context"])):
                    ta, tb = tok.decode(ra["ids"][v]), tok.decode(rb["ids"][v])
                    assert ta.count(ctx) == 1 and tb.count(ctx) == 1
                    ca, cb = _context_ids(tok, ra["ids"][v], ctx), _context_ids(tok, rb["ids"][v], ctx)
                    # the scene's tokens the same; only its last one may merge with what follows it (Lightning's
                    # tokenizer joins the final '.' with Q-after's newline), never a token up to the bridge
                    assert ca[:-1] == cb[:-1] and len(ca) == len(cb)
                    fa, fb = _context_pos(tok, ra["ids"][v], ctx)[0], _context_pos(tok, rb["ids"][v], ctx)[0]
                    assert ra["ids"][v][fa : ra["pos"] + 1] == rb["ids"][v][fb : rb["pos"] + 1]
                    q_block = tb[: tb.index("Scene:\n")]
                    assert p[w]["question"] in q_block and ctx not in q_block
                    assert ta.replace(f"{ctx}\n{p[w]['question']} ", "").count(p[w]["question"]) == 0
                    ua = T2.user_content(p[w]["question"], ctx, ra["kind"], "after")
                    ub = T2.user_content(p[w]["question"], ctx, rb["kind"], "before")
                    q_and_instr = ua[len(ctx) + 1 :]
                    assert ub == f"Question: {q_and_instr}\n\nScene:\n{ctx}"
                    # the bridge at the same offset from the scene's first token
                    first_a, first_b = _context_pos(tok, ra["ids"][v], ctx)[0], _context_pos(tok, rb["ids"][v], ctx)[0]
                    assert ra["pos"] - first_a == rb["pos"] - first_b
                    assert first_b > first_a  # the question block precedes the scene
                assert ra["set_A"] == rb["set_A"] and ra["set_b"] == rb["set_b"]


def test_word_cells_change_only_the_recalls_answer(tok, pairs):
    for p in pairs[:10]:
        num, word = _case(tok, p, "qa_num"), _case(tok, p, "qa_word")
        assert word["readers"][LK]["ids"] == num["readers"][LK]["ids"]  # the lookup unchanged
        rw = word["readers"][RC]
        assert rw["kind"] == "word" and rw["suffix"] == []
        assert rw["said_A"] == T2.number_word(p[RC]["answer"]) and rw["said_b"] == T2.number_word(p[RC]["cf_answer"])
        assert rw["set_A"][0] == T2.ids(tok, " " + rw["said_A"])[0]
        assert not set(rw["set_A"]) & set(rw["set_b"])
        assert rw["words_A"] == [p[RC]["answer"], p[RC]["cf_answer"]]  # 51.12's A: the number words of the answers
        assert rw["ids"]["org"][: word["pos"] + 1] == word["readers"][LK]["ids"]["org"][: word["pos"] + 1]
        assert T2.WORD_INSTRUCTION in tok.decode(rw["ids"]["org"])


# ---- the relation ---------------------------------------------------------------------------------------------------


def test_relation_rule_picks_the_number_word():
    """The rule on the 9B's tokenizer (the brief: chosen on the 9B), whatever BJ_TARGET is."""
    from scripts import x52_atoms as A52

    try:
        tok9 = A52.tokenizer_of(T2.NINE_B)
    except Exception as e:
        pytest.skip(f"the 9B's tokenizer is not cached: {e}")
    cov = T2.coverage(tok9, T2.scene_pairs())
    assert cov["all lexical pooled"]["scenes"] < X.N_MIN
    assert all(not v["admissible"] for k, v in cov.items() if k not in (T2.NUMBER_WORD, "all lexical pooled"))
    assert cov[T2.NUMBER_WORD]["scenes"] >= X.N_MIN
    assert T2.choose(cov) == T2.RELATION == T2.NUMBER_WORD


def test_clashes_catch_spelling_initial_and_symbol(tok):
    assert T2.clashes(tok, "chick", "chicken", "animals")  # a prefix of the item
    assert T2.clashes(tok, "duckling", "duck", "animals")  # the item's word
    assert not T2.clashes(tok, "six", "carbon", "elements")
    assert not T2.clashes(tok, "kitten", "cat", "animals")


# ---- CPU rules ------------------------------------------------------------------------------------------------------


def test_said_word():
    assert T2.said_word(" Six.\nMore") == "six"
    assert T2.said_word("6") is None
    assert T2.said_word("\n\n eight") == "eight"


def test_read_row_accepts_both_cases_of_the_word():
    import torch

    rd = {"set_A": [3, 4], "set_b": [7, 8], "kind": "word", "tok_A": 3, "tok_b": 7}
    lg = torch.zeros(10)
    lg[8] = 5.0
    r = T2.read_row(lg, rd, torch.arange(10))
    assert r["switched"] == 1 and r["role"] == "b" and "cand_switched" not in r
    lg = torch.zeros(10)
    lg[4] = 5.0
    r = T2.read_row(lg, rd, torch.arange(10))
    assert r["switched"] == 0 and r["role"] == "A" and r["ld"] < 0
    rd = {"set_A": [3], "set_b": [7], "kind": "digit", "tok_A": 3, "tok_b": 7}
    lg = torch.zeros(10)
    lg[7] = 1.0
    assert T2.read_row(lg, rd, torch.arange(10))["cand_switched"] == 1


def _comp(scenes, right_rate, n_bad=0):
    rows = []
    for i, s in enumerate(scenes):
        for w in X.READERS:
            for v in ("org", "alt"):
                ok = i >= n_bad and (i / len(scenes) < right_rate)
                rows.append({"scene": s, "reader": w, "variant": v, "right": ok, "read_right": ok})
    return rows


def test_gate_of_is_x0s_gate():
    scenes = [f"s{i:03d}" for i in range(300)]
    cases = [{"scene": s} for s in scenes]
    g, chosen = T2.gate_of(cases, _comp(scenes, 0.9))
    assert g["pass"] and g["tested"] and g["eligible"] == 270 and len(chosen) == X.N_ITEMS
    assert g["order"] == scenes[: X.N_ITEMS]
    g, chosen = T2.gate_of(cases, _comp(scenes, 0.79))
    assert not g["pass"] and not g["tested"] and chosen == []
    assert T2.gate_status(g) == "not tested (gate 0.79 < 0.80)"
    g, chosen = T2.gate_of(cases[:160], _comp(scenes[:160], 0.85))
    assert g["pass"] and not g["enough"] and T2.gate_status(g).startswith("not tested (136 eligible")
    dev = set(scenes[:60])  # Lightning: the dev scenes leave the selection after the gate, as in X0
    g, chosen = T2.gate_of(cases, _comp(scenes, 0.9), dev)
    assert g["org_read_accuracy"] == {LK: 0.9, RC: 0.9} and g["eligible"] == 270 and g["excluded"] == 60
    assert g["tested"] and [c["scene"] for c in chosen] == scenes[60 : 60 + X.N_ITEMS]


def test_dev_scenes():
    assert T2.dev_scenes("qwen3.5-9b") == set()
    assert len(T2.dev_scenes("nemotron-3.5-lightning")) == 60


@pytest.mark.parametrize(
    ("labels", "want"),
    [
        (("entity", "mixed", "entity", "answer"), "position"),
        (("entity", "answer", "entity", "entity"), "position"),
        (("entity", "entity", "mixed", "mixed"), "readability"),
        (("entity", "mixed", "mixed", "answer"), "both"),
        (("entity", "entity", "entity", "entity"), "neither"),
        (("entity", "entity", "entity", "mixed"), "none of the four patterns"),
        (("entity", "not_read", "entity", "entity"), "none of the four patterns"),
        (("entity", "na", "mixed", "answer"), "none of the four patterns"),
        (("entity", None, "entity", "entity"), "can't tell: (Q-before, number) without a label"),
    ],
)
def test_across_cells(labels, want):
    assert T2.across(dict(zip(T2.CELLS, labels, strict=True))) == want


def test_cross_check():
    good = {c: {"status": "tested", "lookup_extra": [0.05, -0.02, 0.12]} for c in T2.CELLS}
    assert T2.cross_check(good)["holds"] is True
    at_bar = {**good, "qb_word": {"status": "tested", "lookup_extra": [0.10, 0.0, 0.2]}}
    assert T2.cross_check(at_bar)["holds"] is True
    bad = {**good, "qb_num": {"status": "tested", "lookup_extra": [0.25, 0.1, 0.4]}}
    assert T2.cross_check(bad)["holds"] is False
    missing = {**good, "qa_word": {"status": "not tested (gate 0.70 < 0.80)"}}
    assert T2.cross_check(missing)["holds"] is None


# ---- the verdict on a planted run (CPU, end to end) -----------------------------------------------------------------


def _plant(tok, root, target: str, labels: dict[str, str], lookup_loss: float, n: int = 60) -> None:
    """A planted run of one model: per cell gate.json, cases (real items), outcomes giving the recall the wanted 51.12
    label and the lookup the wanted arm-1 extra loss, readout ranks (read), atom lists."""
    import json

    for runs in (T2.RUNS, T2.WORD_RUNS):  # the number cells' run and the word cells' run
        (root / runs[target]).mkdir(parents=True)
        (root / runs[target] / "manifest.json").write_text(json.dumps({"layer": 12, "relation": T2.RELATION}))
    pairs = _buildable(tok, n)
    for cell in T2.CELLS:
        d = root / (T2.RUNS if cell in T2.NUMBER_CELLS else T2.WORD_RUNS)[target] / cell
        d.mkdir()
        items = [_case(tok, p, cell) for p in pairs]
        tested = labels[cell] != "untested"
        g = {"tested": tested, "pass": tested, "eligible": n, "min": 150, "status": None,
             "org_read_accuracy": {LK: 0.95, RC: 0.9 if tested else 0.7}}  # fmt: skip
        (d / "gate.json").write_text(json.dumps(g))
        if not tested:
            continue
        X.write_jsonl(d / "cases.jsonl", items)
        rows, readout, atoms = [], [], []
        entity = labels[cell] == "entity"
        for i, it in enumerate(items):
            half = i % 2 == 0
            lk_lost = i < int(lookup_loss * n)
            sw = {RC: {"none": 0, "whole": 1, "no_jpp": 0 if half else 1, "no_jpp_rand": 1,
                       "no_jpp_A": (0 if half else 1) if entity else 1, "no_jpp_A_rand": 1,
                       "no_A": 1 if entity else (0 if half else 1), "no_A_rand": 1},
                  LK: {"none": 0, "whole": 1, "no_jpp": 0 if lk_lost else 1, "no_jpp_rand": 1, "no_jpp_A": 1,
                       "no_jpp_A_rand": 1, "no_A": 1, "no_A_rand": 1}}  # fmt: skip
            srcs = sorted({rd["src"] for rd in it["readers"].values()})
            for w in X.READERS:
                for a, s in sw[w].items():
                    rows.append({"key": it["key"], "scene": it["scene"], "entity": it["entity"], "reader": w,
                                 "arm": a, "sw": s, "switched": s, "top": 0})  # fmt: skip
            for src in srcs:
                for v in ("org", "alt"):
                    readout.append({"key": it["key"], "entity": it["entity"], "source": src, "variant": v,
                                    "answer_word_rank": {LK: 3, RC: 4}, "bridge_rank": 1})  # fmt: skip
                if i < T2.N_ATOMS:
                    atoms.append({"key": it["key"], "reader": src, "entity": it["entity"], "share_k25": 0.3,
                                  "atoms": [{"rank": 1, "token_id": T2.ids(tok, " " + it["entity"])[0],
                                             "token": " " + it["entity"], "coef": -0.5, "share": 0.2},
                                            {"rank": 2, "token_id": T2.ids(tok, " the")[0], "token": " the",
                                             "coef": 0.1, "share": 0.1}]})  # fmt: skip
        X.write_jsonl(d / "outcomes.jsonl", rows)
        X.write_jsonl(d / "readout.jsonl", readout)
        X.write_jsonl(d / "atoms.jsonl", atoms)


def test_verdict_on_a_planted_run(tok, tmp_path, monkeypatch):
    import json

    monkeypatch.setattr(T2, "RESULTS", tmp_path)
    labels = {"qa_num": "entity", "qb_num": "answer", "qa_word": "entity", "qb_word": "untested"}
    _plant(tok, tmp_path, "qwen3.5-9b", labels, lookup_loss=0.0)
    mv = T2.model_verdict("qwen3.5-9b", 200)
    got = {c: r["label"] for c, r in mv["cells"].items()}
    assert got == {"qa_num": "entity", "qb_num": "answer", "qa_word": "entity", "qb_word": None}
    assert mv["cells"]["qb_word"]["status"] == "not tested (gate 0.70 < 0.80)"
    assert mv["across"] == "can't tell: (Q-before, word) without a label"
    assert mv["cross_check"]["holds"] is None
    assert mv["cells"]["qa_num"]["readers"]["lookup"]["conflict"]["excess"][0] == pytest.approx(0.0)
    assert mv["cells"]["qa_num"]["atoms"]["lookup"]["n"] == T2.N_ATOMS  # Q-after: the lookup's Δ in both views
    assert mv["cells"]["qa_num"]["atoms"]["recall"]["n"] == T2.N_ATOMS
    assert set(mv["cells"]["qb_num"]["atoms"]) == {"lookup", "recall"}  # Q-before: each reader's own Δ
    # the entity's own token is a bridge atom (2/3 of the energy); " the" is too where the bridge is theta (a prefix)
    assert 2 / 3 - 1e-6 <= mv["cells"]["qa_num"]["atoms"]["recall"]["energy"]["bridge"][0] < 0.75
    out = T2.stage_verdict(200)
    assert (out / "x53_2x2.png").stat().st_size > 10_000
    text = (out / "verdict.md").read_text()
    assert "Rule across cells:" in text and '"position": (Q-before, number) is answer or mixed' in text
    blob = json.loads((out / "verdict.json").read_text())
    assert [m["target"] for m in blob] == list(T2.MODEL_ORDER)
    assert blob[1]["status"] == "pending"


class FakeModel:
    """A stand-in for the GPU model on the real tokenizer: the state at a position is a fixed random embedding of the
    prompt's tokens summed up to it (so Δ at the bridge word is the bridge tokens' difference), and the reads answer from
    a table of the cells' prompts: unedited, the prompt's gold answer; edited, S's answer when the edit's norm is above
    half the whole change's (so the removals switch on some items and not on others)."""

    D = 24

    def __init__(self, tok):
        import torch

        from scripts import x52_atoms as A52

        self.tokenizer, self.device, self.answers, self.norms = tok, "cpu", {}, {}
        self.vocab = len(tok)
        letters, self.decoded = A52.letter_ids(tok, self.vocab)
        self._letters = torch.tensor(letters)
        self.special_ids = set(tok.all_special_ids)
        g = torch.Generator().manual_seed(0)
        self.E = torch.randn(self.vocab, self.D, generator=g)
        self.U = torch.nn.functional.normalize(torch.randn(self.vocab, self.D, generator=g), dim=-1)

    def states(self, ids: list[int]):
        import torch

        w = 1.0 + 0.1 * torch.arange(len(ids), dtype=torch.float32)[:, None]  # order matters (the cf swaps two picks)
        return (self.E[ids] * w).cumsum(0) / 4.0

    def learn(self, cases: list[dict]) -> None:
        for c in cases:
            for rd in c["readers"].values():
                for v, said, gold in (("org", rd["said_A"], rd["set_A"][0]), ("alt", rd["said_b"], rd["set_b"][0])):
                    self.answers[tuple(rd["ids"][v])] = (" " + said, gold, rd["set_b"][0])
                p = rd["pos"]
                delta = self.states(rd["ids"]["alt"])[p] - self.states(rd["ids"]["org"])[p]
                self.norms[tuple(rd["ids"]["org"][: p + 1])] = float(delta.norm())

    def letter_token_ids(self):
        return self._letters

    def run(self, ids, edits=None, record=()):
        h = self.states(ids[0].tolist())
        return self.U @ h[-1], {la: h for la in record}

    def _logits(self, ids: list[int], edit):
        import torch

        out = torch.zeros(self.vocab)
        key = tuple(ids)
        _, a, b = self.answers.get(key) or self.answers[key[:-1]]  # digit reads carry the appended space token
        out[a] = 5.0
        if edit:
            (row,) = edit.values()
            whole = self.norms[key[: row.positions[0] + 1]]
            out[b] = 6.0 if float(row.delta.norm()) > 0.5 * whole else 4.0
        return out

    def generate_batch(self, ids, n, edits, first_logits=False, steps=False):
        import torch

        rows = [list(map(int, r)) for r in ids]
        texts = [self.answers.get(tuple(r), ("",))[0] for r in rows]  # reads append a token: their text is unused
        if not first_logits:
            return texts
        return texts, torch.stack([self._logits(r, e) for r, e in zip(rows, edits, strict=True)])


class FakeLens:
    def __init__(self, model: FakeModel):
        self.model, self.source_layers = model, list(range(64))

    def readout(self, h, layer):
        return h.float() @ self.model.U.T

    def vectors(self, layer, token_ids, unit=True, chunk=0):
        return self.model.U[token_ids.cpu()].float()


def test_run_stage_end_to_end_on_a_fake_model(tok, tmp_path, monkeypatch):
    """stage_run on a fake model: every cell's gate, relation.json, the four cells' files (Δ, readout, arms, atoms), then
    the verdict; the file contract and the shapes, not the numbers."""
    import json

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    if pins.TARGET not in T2.RUNS:
        pytest.skip(f"53.1 does not run on {pins.TARGET}")
    n, chosen = 24, 20
    pairs = _buildable(tok, n)
    fake = FakeModel(tok)
    for cell in T2.CELLS:
        fake.learn([_case(tok, p, cell) for p in pairs])
    monkeypatch.setattr(T2, "RESULTS", tmp_path)
    monkeypatch.setattr(T2, "scene_pairs", lambda set_name=T2.SET: pairs)
    monkeypatch.setattr(X, "N_MIN", 10)
    monkeypatch.setattr(X, "N_ITEMS", chosen)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", lambda model, name: FakeLens(model))
    monkeypatch.setattr(T2, "choose", lambda cov: T2.RELATION)  # 24 scenes cover no candidate's 150
    if pins.TARGET != T2.NINE_B:  # the 9B's relation check, as its word run leaves it
        (tmp_path / T2.WORD_RUNS[T2.NINE_B]).mkdir()
        (tmp_path / T2.WORD_RUNS[T2.NINE_B] / "relation.json").write_text(json.dumps({"passes": True}))
    num = T2.stage_run(T2.RUNS[pins.TARGET], T2.NUMBER_CELLS)
    assert "relation_coverage" not in json.loads((num / "manifest.json").read_text())  # no relation in a number run
    out = T2.stage_run(T2.WORD_RUNS[pins.TARGET], T2.WORD_CELLS)
    with pytest.raises(AssertionError):
        T2.stage_run(T2.RUNS[pins.TARGET] + "_mixed", T2.CELLS)  # the word cells run on their own
    for cell in T2.CELLS:
        out = num if cell in T2.NUMBER_CELLS else T2.RESULTS / T2.WORD_RUNS[pins.TARGET]
        g = json.loads((out / cell / "gate.json").read_text())
        assert g["tested"] and g["chosen"] == chosen and g["org_read_accuracy"] == {LK: 1.0, RC: 1.0}, (cell, g)
        for f in ("competence.jsonl", "cases.jsonl", "readout.jsonl", "norms.jsonl", "atoms.jsonl", "outcomes.jsonl"):
            assert (out / cell / f).stat().st_size > 0, (cell, f)
        rows = X.read_jsonl(out / cell / "outcomes.jsonl")
        assert len(rows) == chosen * 2 * (1 + len(T2._arms()))
        assert all(r["sw"] == 1 for r in rows if r["arm"] == "whole")
        assert all(r["sw"] == 0 for r in rows if r["arm"] == "none")
        atoms = X.read_jsonl(out / cell / "atoms.jsonl")
        assert len(atoms) == chosen * (1 if T2.CELL[cell][0] == "after" else 2)
        assert all(len(a["atoms"]) == X.K_MAIN for a in atoms)
    words = T2.RESULTS / T2.WORD_RUNS[pins.TARGET]
    if pins.TARGET == T2.NINE_B:
        assert json.loads((words / "relation.json").read_text())["passes"] is True
    assert json.loads((num / "manifest.json").read_text())["finished_utc"]
    mv = T2.model_verdict(pins.TARGET, 100)
    assert all(r["status"] == "tested" for r in mv["cells"].values())


def test_verdict_planted_position_and_cross_check(tok, tmp_path, monkeypatch):
    monkeypatch.setattr(T2, "RESULTS", tmp_path)
    labels = {"qa_num": "entity", "qb_num": "answer", "qa_word": "entity", "qb_word": "entity"}
    _plant(tok, tmp_path, "qwen3.5-9b", labels, lookup_loss=0.3)
    mv = T2.model_verdict("qwen3.5-9b", 200)
    assert mv["across"] == "position"
    assert mv["cross_check"]["holds"] is False
    assert mv["cells"]["qa_num"]["lookup_extra"][0] == pytest.approx(0.3)
