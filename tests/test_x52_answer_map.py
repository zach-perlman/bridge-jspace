"""Batch 52 B (scripts/x52_answer_map.py): where the lens reads the answer and whether writing it works. The token
groups' positions (the earlier mention, the question's '?'), the token sets, the best-of-set rank against brute force,
the answer layer, Dan's rules on planted numbers (readable, usable, the four combinations; bars inclusive), the write's
cell, sizes and vectors, the cluster bootstrap against X0's, the run names, and the read -> write -> verdict path end to
end on a tiny fake causal model (CPU). No real model."""

import json
import math
from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest
import torch

from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x52_answer_map as M
from tests.test_x51_answer import FakeTok

LK, RC = X.LOOKUP, X.RECALL


def word_offsets(text: str) -> list[tuple[int, int]]:
    """Offsets of a whitespace-attached word tokenization: ' word' and punctuation as separate tokens."""
    import re

    return [(m.start(), m.end()) for m in re.finditer(r" ?\w+|[^\w\s]| ", text)]


# ---- positions and tokens ---------------------------------------------------------------------------------------------


def test_earlier_mention_is_the_last_whole_word_mention_before_the_bridge_word():
    text = "The locker of iota is two. Amy picked iotas. The locker of Iota is six. Leo picked iota."
    offs = word_offsets(text)
    bridge = text.rindex(" iota")
    e = M.earlier_mention(text, offs, "iota", offs[[s for s, _ in offs].index(bridge)][0])
    assert e is not None
    assert text[offs[e][0] : offs[e][1]] == " Iota"  # the last one before the bridge word; "iotas" is not a mention
    assert M.earlier_mention(text, offs, "iota", text.index(" is two")) == 3  # only the first one before
    assert M.earlier_mention(text, offs, "delta", len(text)) is None


def test_earlier_mention_takes_the_names_last_token():
    text = "Simon moved there. Mumbai is in India. In which country is the city?"
    offs = [(0, 5), (5, 11), (11, 17), (17, 18), (18, 23), (23, 25), (25, 28), (28, 31), (31, 37), (37, 38)]
    assert M.earlier_mention(text, offs, "Mumbai", text.index("In which")) == 5  # "Mumb" + "ai": the "ai" token


def test_question_mark_is_the_questions_closing_mark():
    q = "In which country is the city that is home to the Kremlin and Red Square?"
    text = f"Context? {q} Answer with just the answer."
    offs = word_offsets(text)
    i = M.question_mark(text, offs, q)
    assert i is not None
    assert text[offs[i][0] : offs[i][1]] == "?" and offs[i][0] == text.rindex("?")
    assert M.question_mark(text, offs, "no mark") is None


def test_reader_tokens_follow_51_12_and_keep_the_whole_words_beside():
    tok = FakeTok(split=("Iota",))
    rd = {"answer": "6", "cf_answer": "3", "tok_A": 99}
    t = M.reader_tokens(tok, "main", rd, "iota", "delta")
    dec = lambda ids: sorted(tok.decode([i]) for i in ids)  # noqa: E731
    assert dec(t["ans"]) == [" Six", " six", "Six", "six"] and dec(t["ans_S"]) == [" Three", " three", "Three", "three"]
    assert dec(t["bridge"]) == [" Io", " iota", "I", "iota"]  # 51.12's first tokens, fragments included
    assert dec(t["bridge_whole"]) == [" iota", "iota"] and t["tokA"] == [99]
    z = M.reader_tokens(
        FakeTok(split=("Greece",)), "z2", {"answer": "Greece", "cf_answer": "Spain", "tok_A": 1}, "x", "y"
    )
    assert len(z["ans"]) == 2 and z["ans_whole"] == []  # "Greece" -> "G" only as a first token


def test_run_names_spec_ids_and_layers():
    from bridge_jspace import pins

    assert M.run_name("read", "main", "qwen3.5-9b") == "qwen35_9b_x52_read_main"
    assert M.run_name("write", "z2", "qwen3.6-27b") == "x52_write_z2_27b"
    assert M.run_name("read", "z2", "muse-glimmer-30b") == "muse30_x52_read_z2"
    for t in M.MODELS:
        for st in M.STAGES:
            for s in M.SETS:
                name = M.run_name(st, s, t)
                assert name.startswith(pins.TARGETS[t]["run_prefix"]) and "_raw" not in name
                assert M.spec_id(st, s, t) == f"x52_{st}_{s}_{M.TAGS[t]}"
    assert M.layers_for(32) == tuple(range(0, 31, 2)) and len(M.layers_for(64)) == 32 and M.layers_for(52)[-1] == 50
    assert (M.TOP_K, M.READ_SHARE, M.USE_SWITCH, M.USE_RAND) == (5, 0.5, 0.3, 0.10)
    assert M.NO_PREDICTION == "rule fixed in advance in jobs/c3/batch52.yaml (B); no prediction"


def test_rule_text_is_dans_verbatim():
    brief = (M.SPEC).read_text()
    for v in M.RULE.values():
        assert v.replace("“", "“").replace("”", "”") in brief


# ---- ranks, the answer layer, the rules ------------------------------------------------------------------------------


def test_best_rank_is_the_best_members_rank_with_strict_ties():
    g = torch.Generator().manual_seed(0)
    logits = torch.randn(6, 50, generator=g)
    logits[0, 7] = logits[0, 3] = 10.0  # a tie at the top: both rank 1
    sets = [[7], [3, 9, 11], [], [49, 0], [5], [1, 2, 3, 4]]
    got = M.best_rank(logits, M.pad(sets)).tolist()
    for i, s in enumerate(sets):
        want = min((int((logits[i] > logits[i, t]).sum()) + 1 for t in s), default=-1)
        assert got[i] == want
    assert got[0] == 1 and got[2] == -1


def test_answer_layer_is_the_lower_median_of_first_tops():
    tops = np.array([[0, 5, 5, 1, 5], [0, 0, 0, 5, 5], [0, 0, 0, 0, 0], [5, 0, 0, 0, 5]])
    a = M.answer_layer(tops, [5, 5, 5, 5])
    assert a["per_item"] == [1, 3, None, 0] and a["layer"] == 1 and a["never"] == 1  # lower median of 0, 1, 3
    assert a["settle_layer"] == 4  # 51.10's: on top from there through the last layer (items 0, 1, 3: 4, 3, 4)


def test_readable_needs_half_the_items_in_the_top5_before_the_answer_layer():
    t5 = {("B", 10): 0.49, ("T", 20): 0.5, ("Q", 22): 0.9, ("E", 12): None}
    r = M.readable(t5, 22)
    assert r["holds"] is True and r["cells"] == [["T", 20]] and r["first"] == ["T", 20]  # 0.5 counts; L22 is not before
    assert M.readable(t5, 20)["holds"] is False  # L20 is the answer layer itself: not before
    assert M.readable(t5, 20)["best_before"] == {"group": "B", "layer": 10, "top5": 0.49}
    assert M.readable(t5, None)["holds"] is None


def test_the_write_cell_is_the_most_readable_before_the_answer_layer():
    t5 = {("B", 10): 0.4, ("Q", 10): 0.4, ("T", 8): 0.4, ("T", 30): 1.0, ("E", 4): None}
    med = {("B", 10): 9.0, ("Q", 10): 7.0, ("T", 8): 7.0, ("T", 30): 1.0}
    assert M.select_cell(t5, med, 30) == ("T", 8)  # tie on the share and the median: the earlier layer
    assert M.select_cell(t5, {**med, ("T", 8): 8.0}, 30) == ("Q", 10)  # then the lower median rank decides
    assert M.select_cell(t5, med, None) == ("T", 30)  # no answer layer: every layer
    assert M.select_cell({("B", 4): None}, {}, 10) is None


@pytest.mark.parametrize(
    ("sw", "holds"),
    [({"ans1": 0.3, "rand1": 0.10, "ans2": 0.0, "rand2": 0.0}, True),  # both bars inclusive
     ({"ans1": 0.29, "rand1": 0.0, "ans2": 0.31, "rand2": 0.11}, False),  # gain 2's own random control fails
     ({"ans1": 0.1, "rand1": 0.0, "ans2": 0.6, "rand2": 0.05}, True)],  # gain 2 alone
)  # fmt: skip
def test_usable_rule_on_planted_numbers(sw, holds):
    assert M.usable(sw)["holds"] is holds


def test_the_four_combinations():
    assert M.combination(True, True) == "readable and usable"
    assert M.combination(True, False) == "readable, not usable"
    assert M.combination(False, True) == "usable, not readable"
    assert M.combination(False, False) == "neither" and M.combination(None, True) is None


def test_boot_shares_are_x0s_draws_and_skip_missing_items():
    ents = [f"e{i % 7}" for i in range(40)]
    x = (np.arange(40) % 3 == 0).astype(float)
    ours = M.boot_shares(x[None], ents, 200)[0]
    assert np.allclose(ours, X.resampled_rates({"a": x.tolist()}, ents, 200)["a"])
    gap = x.copy()
    gap[::2] = np.nan  # an item without the position counts in neither the numerator nor the denominator
    both = M.boot_shares(np.stack([x, gap]), ents, 200)
    assert np.allclose(both[0], ours) and np.nanmax(both[1]) <= 1.0
    ci = M.share_ci(np.stack([x, gap, np.full(40, np.nan)]), ents, 200)
    assert ci[0][0] == pytest.approx(x.mean()) and ci[1][0] == pytest.approx(np.nanmean(gap)) and math.isnan(ci[2][0])


def test_write_size_and_vectors():
    d = 16
    g = torch.Generator().manual_seed(3)
    ho, hs, bo, bs = (torch.randn(d, generator=g) for _ in range(4))
    s, flagged = M.write_size(ho, hs, bo, bs)
    assert s == pytest.approx(float((hs - ho).norm())) and not flagged
    s, flagged = M.write_size(ho, ho.clone(), bo, bs)  # the position precedes the change: the bridge word's size
    assert s == pytest.approx(float((bs - bo).norm())) and flagged
    assert M.write_size(ho, None, bo, bs)[1]
    u = M.unit_sum(torch.nn.functional.normalize(torch.randn(3, d, generator=g), dim=-1))
    uf = M.unit_sum(torch.randn(2, d, generator=g))
    basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + 4))
    v = M.write_vectors(u, uf, basis, 2.5, hs - ho)
    assert tuple(v) == M.ARMS and torch.allclose(v["whole"], hs - ho)
    for gain in M.GAINS:
        for a in ("ans", "rand", "freq"):
            assert float(v[f"{a}{gain}"].norm()) == pytest.approx(2.5 * gain, rel=1e-5)
    assert torch.allclose(v["rand1"], 2.5 * (u @ basis.T)) and torch.allclose(v["ans2"], 2 * v["ans1"])
    assert abs(float(v["rand1"] @ v["ans1"])) < 0.9 * 2.5**2  # turned away from the answer direction


# ---- end to end on a tiny fake causal model --------------------------------------------------------------------------


def fake_item(i: int, set_name: str = "main") -> dict:
    """Prompts agree through the bridge word (position 4) except there; E (position 1) precedes the change, Q at 6."""
    org = [50 + i % 3, 30 + i % 4, 21, 22, 60 + i % 5, 24, 25, 26]
    alt = [*org[:4], 70 + i % 5, *org[5:]]
    suffix = [11] if set_name == "main" else []
    readers = {}
    for k, w in enumerate((LK, RC) if set_name == "main" else ("K", "M")):
        ids = {"org": [*org, 40 + k], "alt": [*alt, 40 + k]}
        t = len(ids["org"]) + len(suffix) - 1
        pos = {"B": 4, "E": 1 if i % 3 else None, "Q": 6, "T": t}
        readers[w] = {"ids": ids, "suffix": suffix, "pos": {"org": pos, "alt": dict(pos)}, "question": "q",
                      "answer": "5" if set_name == "main" else "Spain", "cf_answer": "3" if set_name == "main" else "Italy",
                      "tok_A": 5, "tok_b": 3, "tok_lure": None,
                      "toks": {"ans": [80 + i % 4], "ans_S": [90 + i % 4], "bridge": [50 + i % 3], "bridge_S": [70],
                               "tokA": [5], "bridge_whole": [50 + i % 3], "ans_whole": [80 + i % 4]}}  # fmt: skip
    return {"set": set_name, "key": f"s{i}", "scene": f"s{i}", "entity": f"e{i % 4}", "cf_entity": "bee", "lf": True,
            "readers": readers}  # fmt: skip


def fake_world(tmp_path, monkeypatch, set_name: str, n: int = 12) -> Any:
    from bridge_jspace import lens as LN
    from bridge_jspace import model as MD
    from tests.test_x49_gain import D, FakeModel

    fake: Any = FakeModel(n_layers=64)
    fake.unembed = lambda h: h.float() @ fake.unemb.T
    fake.letter_token_ids = lambda: torch.arange(0, 100)
    fake.tokenizer = FakeTok()

    class Lens:
        source_layers = tuple(range(63))

        def __init__(self, model=None, name="jpp"):
            assert name == "jpp"
            self.raw = (
                torch.randn(128, D, generator=torch.Generator().manual_seed(7)) * torch.linspace(0.5, 2, 128)[:, None]
            )

        def vectors(self, layer, ids, unit=True):
            v = self.raw[torch.as_tensor(ids, dtype=torch.long).cpu()]
            return v / v.norm(dim=1, keepdim=True) if unit else v

        def readout(self, h, layer):
            return h.float() @ self.raw.T

    items = [fake_item(i, set_name) for i in range(n)]
    monkeypatch.setattr(MD, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", Lens)
    monkeypatch.setattr(M, "RESULTS", tmp_path / "x52")
    monkeypatch.setattr(M.A, "RESULTS", tmp_path / "x51_answer")  # no stored 51.12 readout here
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(X, "whitespace_mask", lambda model: None)
    monkeypatch.setattr(M, "source_files", lambda s, t: [M.SPEC])
    monkeypatch.setattr(M, "BUILD", {**M.BUILD, set_name: lambda tok, t: (items, {"pass": True}, {"items": n})})
    return SimpleNamespace(fake=fake, items=items)


@pytest.mark.parametrize("set_name", ["main", "z2"])
def test_read_write_verdict_end_to_end(tmp_path, monkeypatch, set_name):
    from bridge_jspace import pins

    w = fake_world(tmp_path, monkeypatch, set_name)
    target = pins.TARGET
    read, write = M.run_name("read", set_name, target), M.run_name("write", set_name, target)
    out = M.stage_run(read, set_name)
    m = json.loads((out / "manifest.json").read_text())
    assert m["prediction"] == M.NO_PREDICTION and m["stage"] == "read" and m["items"] == 12
    assert m["layers"] == list(range(0, 63, 2))  # the candidate layers the lens covers
    z = np.load(out / M.RANKS_FILE)
    nl = len(m["layers"])
    assert z["lens_ans"].shape == (12, 2, 4, nl) and z["ll_top"].shape == (12, 2, 64)
    e_missing = [i for i in range(12) if i % 3 == 0]
    assert (z["lens_ans"][e_missing, :, 1] == -1).all() and (z["lens_ans"][:, :, [0, 2, 3]] >= 1).all()
    # the ranks are the lens's: recompute one cell from the cached state
    from bridge_jspace import lens as LN

    st = np.load(out / M.STATES_FILE)
    h = torch.from_numpy(st["h"][2, 1, 0, 3, 5].astype(np.float32))
    lg = LN.JLens(w.fake, "jpp").readout(h[None], m["layers"][5])
    ans = w.items[2]["readers"][M.readers_of(w.items)[1]]["toks"]["ans"]
    assert z["lens_ans"][2, 1, 3, 5] == int(M.best_rank(lg, M.pad([ans]))[0])
    # S is cached too, and differs from O only from the bridge word on
    assert np.array_equal(st["h"][:, :, 0, 1], st["h"][:, :, 1, 1]) and not np.array_equal(
        st["h"][:, :, 0, 3], st["h"][:, :, 1, 3]
    )

    wout = M.stage_write(write, set_name, read)
    rows = X.read_jsonl(wout / "outcomes.jsonl")
    cells = json.loads((wout / "cells.json").read_text())["cells"]
    assert set(cells) == {"lookup", "recall"} and all(c is not None for c in cells.values())
    n_ok = {who: sum(1 for it in w.items if it["readers"][M.readers_of(w.items)[k]]["pos"]["org"][cells[who][0]] is not None)
            for k, who in enumerate(M.WHO)}  # fmt: skip
    assert len(rows) == sum(n_ok.values()) * (1 + len(M.ARMS))
    assert all(r["switched"] == int(r["top"] == 3) and r["changed"] == int(r["top"] != 5) for r in rows)
    norms = [r for r in X.read_jsonl(wout / "norms.jsonl") if "s" in r]
    assert all(r["s"] > 0 and len(r["F"]) == 1 and r["F"][0]["f"] not in r["A_ids"] for r in norms)
    # at E the prompts agree (E precedes the change): the size falls back to the bridge word's
    assert all(r["size_from_bridge_word"] == (r["group"] == "E") for r in norms)

    vout = M.stage_verdict(n_boot=50, decode_for=lambda t: lambda ids: "".join(f"<{i}>" for i in ids))
    blob = json.loads((vout / "verdict.json").read_text())
    key = f"{target}|{set_name}|lookup"
    assert set(blob["combinations"][key]) == {"readable", "usable", "combination"}
    assert blob["combinations"][key]["usable"] is not None and blob["prediction"] == M.NO_PREDICTION
    text = (vout / "verdict.md").read_text()
    assert M.NO_PREDICTION in text and f"| {target} | {set_name} | lookup | 12 |" in text
    assert (vout / f"map_{M.TAGS[target]}.png").exists()
    view = (vout / "view.md").read_text()
    assert view.count("⟦") >= 5 * 2 * 3 and "random rows of" in view
