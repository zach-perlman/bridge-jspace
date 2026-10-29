"""Batch 51, test 51.12 (scripts/x51_answer.py, r2 after Dan's amendment 20:20): the answer directions (number words
on e1 / cue, first tokens on z2, letter tokens only, span), the parts (the J++ part with A projected out, A alone, the
frequency-matched F), the frequency match on planted ids and norms, the OMP support against signed_omp, the arms
against the stored runs' removal path, the rules on planted numbers (bars inclusive; z2's two controls), the readout
classes and the readout check's shares and case, the arm-1 agreement, the run end to end (e1 and z2), the verdict on a
planted run, and the seal. No real model."""

import json
import math
from collections.abc import Sequence
from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x51_answer as A
from scripts.exp04_brew_parts import signed_omp

LK, RC = X.LOOKUP, X.RECALL


class FakeTok:
    """Word-level: a leading space before a digit is its own token (as on Qwen), before a word it is part of it; words
    in `split` are two tokens (first two characters, then the rest); an id not in the vocabulary decodes as 'w<id>'."""

    def __init__(self, split: tuple[str, ...] = ()):
        self.vocab: dict[str, int] = {}
        self.split = split

    def _id(self, s: str) -> int:
        return self.vocab.setdefault(s, len(self.vocab))

    def __call__(self, text: str, add_special_tokens: bool = False):
        if text.startswith(" ") and text[1:2].isdigit():
            return SimpleNamespace(input_ids=[self._id(" "), self._id(text[1:])])
        if text.strip() in self.split:
            k = 3 if text.startswith(" ") else 1
            return SimpleNamespace(input_ids=[self._id(text[:k]), self._id(text[k:])])
        return SimpleNamespace(input_ids=[self._id(text)])

    def decode(self, ids, **_):
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"w{int(i)}") for i in ids)


def words_of(tok, ids):
    return sorted(tok.decode([i]) for i in ids)


def test_variants_drop_whitespace_first_tokens_and_keep_caps():
    tok = FakeTok()
    ids = A.variant_ids(tok, ["5", "europe"])
    assert words_of(tok, ids) == [" Europe", " europe", "5", "Europe", "europe"]  # " 5" -> " " dropped


def test_number_words_and_their_one_token_letter_variants():
    assert A.number_word("6") == "six" and A.number_word(" 0") == "zero"
    with pytest.raises(AssertionError, match="single digit"):
        A.number_word("10")
    tok = FakeTok(split=("Seven",))
    # whole: a variant counts only if it is one token; "Seven" / " Seven" split here, so only "seven" / " seven"
    assert words_of(tok, A.word_ids(tok, ["six", "seven"], whole=True)) == [
        " Six",
        " seven",
        " six",
        "Six",
        "seven",
        "six",
    ]
    assert A.word_ids(tok, ["5", "7"], whole=True) == [] and A.word_ids(tok, ["5"], whole=False) == []  # digits never


def test_z2_keeps_the_first_token_of_a_split_answer_word():
    tok = FakeTok(split=("Greece",))
    ids = A.word_ids(tok, ["Greece", "Spain"], whole=False)
    assert words_of(tok, ids) == [" Gr", " Spain", "G", "Spain"]  # "Greece" -> "G" + "reece"; " Greece" -> " Gr" + ...


def e1_item(answers: dict[str, tuple[str, str]], extra: dict | None = None, set_name: str = "e1") -> dict:
    c = {"scene": "s0", "pos": 1, "space": [0],
         "readers": {w: {"answer": a, "cf_answer": b, "ids": {"org": [1, 2], "alt": [1, 3]}, "tok_A": 5, "tok_b": 6}
                     for w, (a, b) in answers.items()}}  # fmt: skip
    if set_name == "cue":
        c |= {"route_tokens": {}, "expect": {}}
    return A.unit(set_name, c, "s0", "frog", "bee", extra or {})


def test_item_tokens_e1_number_words_of_both_readers_on_o_and_s():
    tok = FakeTok()
    tk = A.item_tokens(tok, e1_item({LK: ("2", "6"), RC: ("9", "4")}))
    assert tk["A_words"] == ["two", "six", "nine", "four"]
    assert len(tk["A"]) == 16 and all(any(c.isalpha() for c in tok.decode([t])) for t in tk["A"])  # no digit in A
    assert words_of(tok, tk["own_word"]["org"][RC]) == [" Nine", " nine", "Nine", "nine"]
    assert words_of(tok, tk["own_word"]["alt"][LK]) == [" Six", " six", "Six", "six"]
    assert "6" in words_of(tok, tk["own"]["alt"][LK])  # the top-1 class counts the answer as stated too


def test_item_tokens_cue_all_four_lockers_and_the_legs():
    tok = FakeTok()
    it = e1_item({LK: ("9", "7"), RC: ("2", "4")}, {LK: ["2", "5"]}, set_name="cue")  # a = 9, e = 7, b = 2, c = 5
    tk = A.item_tokens(tok, it)
    assert sorted(tk["A_words"]) == ["five", "four", "nine", "seven", "two"] and len(tk["A"]) == 20


def test_answer_basis_rank_and_parts():
    g = torch.Generator().manual_seed(0)
    d = 16
    v = torch.randn(3, d, generator=g)
    q = A.answer_basis(torch.cat([v, v[:1] * 2.0]))  # a duplicate direction adds no rank
    assert q.shape == (d, 3) and torch.allclose(q.T @ q, torch.eye(3), atol=1e-5)
    delta, pj = torch.randn(2, d, generator=g), torch.randn(2, d, generator=g)
    empty = A.answer_basis(torch.zeros(0, d))
    pja, pa = A.answer_parts(delta, pj, [q, empty])
    assert torch.allclose(q.T @ pja[0], torch.zeros(3), atol=1e-5)  # nothing of span(A) left in arm 2's removed part
    assert torch.allclose(pa[0], q @ (q.T @ delta[0]), atol=1e-5) and torch.allclose(
        pja[0] + q @ (q.T @ pj[0]), pj[0], atol=1e-5
    )
    assert torch.equal(pja[1], pj[1]) and not pa[1].any()  # no answer atoms: arm 2 = arm 1, arm 3 removes nothing


def test_omp_support_matches_signed_omp_and_finds_planted_atoms():
    g = torch.Generator().manual_seed(1)
    dic = torch.nn.functional.normalize(torch.randn(40, 32, generator=g), dim=-1)
    x = torch.stack([2.0 * dic[3] - 1.5 * dic[17] + 0.5 * dic[30], torch.randn(32, generator=g)])
    chosen, approx = A.omp_support(dic, x, 5)
    assert torch.allclose(approx, signed_omp(dic, x, 5))
    assert {3, 17, 30} <= set(chosen[0].tolist()) and chosen.shape == (2, 5)


def test_all_arms_follow_the_stored_removal_path_and_add_f():
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    g = torch.Generator().manual_seed(2)
    d = 24
    delta, pj = torch.randn(3, d, generator=g), torch.randn(3, d, generator=g)
    q = A.answer_basis(torch.randn(2, d, generator=g))
    basis = SP.random_basis(d, torch.Generator().manual_seed(888))
    arms, sh = A.all_arms(delta, pj, [q, q, q], basis)
    assert tuple(arms) == A.ARMS == A.arms_of("e1")
    old, _ = R.removal_arms(delta, {"jpp": pj}, basis)  # x50_zach / x47_cue's arms (X0's: x - part, x - rand)
    assert torch.equal(arms["no_jpp"], old["no_jpp"]) and torch.equal(arms["no_jpp_rand"], old["no_jpp_rand"])
    assert torch.allclose(arms["no_A"], delta - (delta @ q) @ q.T, atol=1e-5)
    assert torch.allclose(sh["A_in_jpp"] + sh["jpp_A"], sh["jpp"], atol=1e-4)  # orthogonal split of the J++ part
    qf = A.answer_basis(torch.randn(2, d, generator=g))
    arms_f, sh_f = A.all_arms(delta, pj, [q, q, q], basis, [qf, qf, qf])
    assert tuple(arms_f) == A.arms_of("z2") and torch.equal(arms_f["no_A"], arms["no_A"])
    assert torch.allclose(arms_f[A.F_ARM], delta - (delta @ qf) @ qf.T, atol=1e-5)
    assert torch.allclose(sh_f["F"], ((delta @ qf) ** 2).sum(-1) / (delta**2).sum(-1), atol=1e-5)


# ---- the frequency-matched control on planted ids and norms ---------------------------------------------------------


def planted_letters():
    ids = np.arange(10, 3000)
    norm = np.full(len(ids), 5.0)
    at = lambda t: int(t) - 10  # noqa: E731
    norm[at(100)], norm[at(150)], norm[at(60)] = 3.0, 3.0, 3.01  # 150: an exact norm match within the band
    norm[at(500)], norm[at(2000)], norm[at(800)] = 7.0, 7.0, 7.2  # 2000: exact but outside the factor-2 band
    return ids, np.log(norm), at


def test_freq_match_band_then_closest_norm():
    ids, log_norm, at = planted_letters()
    banned = np.zeros(len(ids), dtype=bool)
    m = A.freq_match([100, 500], ids, log_norm, banned)
    assert [x["f"] for x in m] == [150, 800] and all(x["band"] == 2.0 for x in m)
    assert m[0]["norm_ratio"] == pytest.approx(1.0) and m[1]["norm_ratio"] == pytest.approx(7.2 / 7.0, abs=1e-4)
    assert all(0.5 <= x["id_ratio"] <= 2.0 for x in m)
    banned[at(150)] = True  # related to the set: never a control
    assert A.freq_match([100], ids, log_norm, banned)[0]["f"] == 60


def test_freq_match_never_twice_never_in_a_and_widens():
    ids = np.array([10, 11, 12, 40, 41])
    log_norm = np.log(np.array([1.0, 1.0, 1.0, 1.0, 9.0]))
    m = A.freq_match([10, 11], ids, log_norm, np.zeros(5, dtype=bool))
    assert [x["f"] for x in m] == [12, 40] and m[1]["band"] == 4.0  # 12 taken by 10, not 10 / 11 (in A); widened once
    with pytest.raises(AssertionError, match="not a letter token"):
        A.freq_match([13], ids, log_norm, np.zeros(5, dtype=bool))


def test_related_mask_equal_or_containing():
    keys = ["africa", "african", "afr", "g", "ga", "europe", "bund", "w12"]
    mask = A.related_mask(keys, {"africa", "g"})
    assert mask.tolist() == [True, True, True, True, False, False, False, False]


def test_related_keys_cover_answers_bridges_and_the_edited_token():
    tok = FakeTok(split=("Greece",))
    c = {"scene": "s", "set": "j", "desc": "d", "cf_desc": "cd",
         "readers": {w: {"answer": "Greece", "cf_answer": "Spain", "ids": {"org": [90, 91], "alt": [90, 92]}, "pos": 1,
                         "tok_A": 0, "tok_b": 1, "tok_lure": None} for w in ("K", "M")}}  # fmt: skip
    it = A.unit("z2", c, "j|s", "Athens", "Madrid", {})
    keys = A.related_keys(tok, [it], [A.item_tokens(tok, it)])
    assert {"greece", "spain", "g", "gr", "athens", "madrid", "w91", "w92"} <= keys


# ---- rules, reads, checks -------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("e", "key"),
    [((0.5, 0.35, 0.10), "entity"),  # bars inclusive: 0.7 of arm 1, 0.10
     ((0.5, 0.15, 0.25), "answer"),  # 0.3 and 0.5 of arm 1
     ((0.5, 0.35, 0.11), "mixed"), ((0.5, 0.2, 0.2), "mixed"), ((0.0, 0.3, 0.3), "na"), ((float("nan"), 0, 0), "na"),
     ((-0.1, 0.0, 0.0), "na"),
     ((0.5, 0.35, 0.05, 0.10), "entity"), ((0.5, 0.35, 0.05, 0.12), "mixed"),  # z2: entity against both controls
     ((0.5, 0.15, 0.30, 0.25), "answer"), ((0.5, 0.15, 0.30, 0.10), "mixed"),  # z2: answer against both controls
     ((0.5, 0.15, 0.30, float("nan")), "mixed")],
)  # fmt: skip
def test_rule_on_planted_numbers(e, key):
    r = A.rule(*e)
    assert r["key"] == key and r["label"] == A.LABELS[key]


def rows_for(sw: dict[str, list[int]], reader: str = RC) -> list[dict]:
    n = len(sw["whole"])
    return [{"key": f"s{i}", "scene": f"s{i}", "entity": f"e{i % 5}", "reader": reader, "arm": a, "sw": sw[a][i],
             "switched": sw[a][i], "top": 1, "route": None} for a in sw for i in range(n)]  # fmt: skip


def planted_sw(n: int = 20) -> dict[str, list[int]]:
    """whole 10 of 20; arm 1: 2 vs random 8 (e1 = 0.6); arm 2: 3 vs 8 (e2 = 0.5); arm 3: 10 vs 10 (e3 = 0)."""
    on = lambda k: [1] * k + [0] * (n - k)  # noqa: E731
    return {"none": on(0), "whole": on(10), "no_jpp": on(2), "no_jpp_rand": on(8), "no_jpp_A": on(3),
            "no_jpp_A_rand": on(8), "no_A": on(10), "no_A_rand": on(10)}  # fmt: skip


def test_reader_numbers_extra_losses_and_label():
    r = A.reader_numbers(rows_for(planted_sw()), RC, n_boot=200)
    assert r["n"] == 20 and r["entities"] == 5 and "3f" not in r["extra"] and r["share3f"] is None
    assert r["extra"]["1"][0] == pytest.approx(0.6) and r["extra"]["2"][0] == pytest.approx(0.5)
    assert r["extra"]["3"][0] == pytest.approx(0.0) and r["share2"][0] == pytest.approx(5 / 6)
    assert r["key"] == "entity" and r["valid"] is False  # 10 switches < X0's 30 (beside, not in the rule)


def test_reader_numbers_z2_reads_arm_3_against_the_frequency_control():
    on = lambda k: [1] * k + [0] * (20 - k)  # noqa: E731
    sw = {**planted_sw(), "no_jpp_A": on(7), "no_A": on(4), "no_A_rand": on(8), A.F_ARM: on(5)}
    r = A.reader_numbers(rows_for(sw), RC, n_boot=200)
    # e1 0.6; e2 0.1 (share 1/6); e3 vs random 0.4 (2/3 of e1), vs frequency-matched 0.1 (1/6): answer needs both
    assert r["extra"]["3"][0] == pytest.approx(0.4) and r["extra"]["3f"][0] == pytest.approx(0.1)
    assert r["share3f"][0] == pytest.approx(1 / 6) and r["key"] == "mixed"
    sw[A.F_ARM] = on(8)
    assert A.reader_numbers(rows_for(sw), RC, n_boot=50)["key"] == "answer"


def test_switch_of_47_3_lookup_follows_the_change():
    assert A.switch_of("cue", LK, {"route": "identity", "switched": 0}) == 1
    assert A.switch_of("cue", LK, {"route": "original", "switched": 0}) == 0
    assert A.switch_of("cue", RC, {"route": None, "switched": 1}) == 1
    assert A.switch_of("e1", LK, {"route": None, "switched": 1}) == 1


def test_readout_row_classes_and_word_ranks():
    it = {"key": "k", "entity": "frog", "readers": {LK: {"tok_A": 5, "tok_b": 6}, RC: {"tok_A": 7, "tok_b": 8}}}
    toks = {"own": {"org": {LK: [5, 25], RC: [7]}, "alt": {LK: [6], RC: [8]}}, "bridge": {"org": [20], "alt": [21]},
            "own_word": {"org": {LK: [25, 26], RC: []}, "alt": {LK: [27], RC: [28]}}}  # fmt: skip
    digit_ids = [5, 6, 7, 8]
    lg = torch.zeros(30)
    lg[5], lg[7], lg[26] = 3.0, 2.0, 2.5  # the lookup's digit on top at O; its word " six" (26) 2nd
    r = A.readout_row(it, toks, LK, "org", lg, digit_ids)
    assert r["class"] == "answer" and r["own_answer_of"] == [LK] and r["answer_rank"] == {LK: 1, RC: 3}
    assert r["answer_digit_rank"] == {LK: 1, RC: 2} and r["top_digit"] == 5
    assert r["answer_word_rank"] == {LK: 2, RC: None}  # best variant; no letter token -> None
    lg = torch.zeros(30)
    lg[20] = 1.0
    r = A.readout_row(it, toks, LK, "org", lg, digit_ids)
    assert r["class"] == "bridge" and r["bridge_rank"] == 1
    lg = torch.zeros(30)
    lg[6] = 1.0  # S's answer read at O: neither, flagged as the other prompt's answer
    r = A.readout_row(it, toks, LK, "org", lg, digit_ids)
    assert r["class"] == "neither" and r["other_answer"]


def check_rows(
    ranks: Sequence[tuple[int | None, int]], reader: str = RC, source: str = LK, bridge: int = 10
) -> list[dict]:
    return [{"key": f"s{i}", "entity": f"e{i % 5}", "source": source, "variant": v,
             "answer_word_rank": {reader: ro if v == "org" else rs}, "bridge_rank": bridge}
            for i, (ro, rs) in enumerate(ranks) for v in ("org", "alt")]  # fmt: skip


def test_readout_check_shares_and_case():
    ranks = [(100, 200)] * 9 + [(5, 300)]
    c = A.readout_check(check_rows(ranks), RC, n_boot=100)
    assert c["n"] == 10 and c["source"] == LK  # e1 / cue: the recall is read on the lookup's (shared) state
    assert (
        c["top10_O"][0] == pytest.approx(0.1) and c["top50_S"][0] == 0.0 and c["top50_either"][0] == pytest.approx(0.1)
    )
    assert c["not_read"][0] == pytest.approx(0.9) and c["case"] == "not_read"  # 90 % inclusive
    assert (
        c["median_rank_O"] == 100 and c["median_bridge_rank_S"] == 10 and c["above_bridge_O"][0] == pytest.approx(0.1)
    )
    c = A.readout_check(check_rows([(100, 200)] * 8 + [(5, 300), (60, 40)]), RC, n_boot=100)
    assert c["not_read"][0] == pytest.approx(0.8) and c["case"] == "arms"
    c = A.readout_check(check_rows([(1, 1)] * 3 + [(None, 2)], reader="M", source="M"), "M", n_boot=50)
    assert c["source"] == "M" and c["n"] == 3 and c["missing"] == 1 and c["case"] == "arms"  # z2: its own state


def test_agreement_item_by_item():
    sw = planted_sw()
    rows = rows_for(sw)
    stored = {(r["key"], r["reader"], r["arm"]): {"sw": r["sw"], "top": 1, "switched": r["sw"]} for r in rows
              if r["arm"] in ("none", "whole", "no_jpp", "no_jpp_rand")}  # fmt: skip
    stored[("s0", RC, "no_jpp")] = {"sw": 0, "top": 2, "switched": 0}
    agree = A.agreement("e1", rows, stored)["recall"]
    assert agree["whole"] == {"n": 20, "matched": 20, "agree_switch": 20, "agree_top": 20, "top_stored": 20,
                              "rerun": 10, "stored": 10}  # fmt: skip
    stored = {k: {**v, "top": None} for k, v in stored.items()}  # the 9B's X0 run stores no top token
    assert A.agreement("e1", rows, stored)["recall"]["whole"]["top_stored"] == 0
    assert agree["no_jpp"]["agree_switch"] == 19 and agree["no_jpp"]["agree_top"] == 19
    assert agree["extra_loss_arm1"]["rerun"] == pytest.approx(0.6) and agree["extra_loss_arm1"][
        "stored"
    ] == pytest.approx(0.7)


# ---- the run stage end to end on 49.1's tiny fake causal model (CPU) ------------------------------------------------


def fake_run(tmp_path, monkeypatch, set_name: str, items: list[dict]) -> Any:
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from tests.test_x49_gain import D, FakeModel

    fake: Any = FakeModel()
    fake.letter_token_ids = lambda: torch.arange(0, 100)

    class Lens:
        """J++ atoms from one fixed table (so A's rows are the dictionary's rows), raw norms planted per token."""

        source_layers = tuple(range(60))

        def __init__(self, model=None, name="jpp"):
            assert name == "jpp"
            self.raw = (
                torch.randn(128, D, generator=torch.Generator().manual_seed(7)) * torch.linspace(0.5, 2, 128)[:, None]
            )

        def vectors(self, layer, ids, unit=True):
            v = self.raw[torch.as_tensor(ids, dtype=torch.long).cpu()]
            return v / v.norm(dim=1, keepdim=True) if unit else v

        def readout(self, h, layer):
            return h @ fake.unemb.T

    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", Lens)
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x51_answer")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(X, "whitespace_mask", lambda model: None)
    src = tmp_path / "src"
    src.mkdir(exist_ok=True)
    monkeypatch.setattr(A, "source_of", lambda s, t: src)
    monkeypatch.setattr(A, "layer_of", lambda s, t: X.PREDICTED["qwen3.6-27b"])
    gate = {"pass": True, "chosen": len(items)}
    monkeypatch.setattr(A, "BUILD", {**A.BUILD, set_name: lambda tok, t: (items, gate, {"source": "src"})})
    monkeypatch.setattr(A, "RUNS", {**A.RUNS, set_name: {A.pins.TARGET: "x"}})
    return fake


def test_stage_run_e1_end_to_end_sealed(tmp_path, monkeypatch):
    from bridge_jspace import pins
    from tests.test_x49_gain import _item

    cases = [_item(i) for i in range(12)]
    items = [A.unit("e1", c, c["scene"], c["entity"], c["cf_bridge"], {}) for c in cases]
    fake = fake_run(tmp_path, monkeypatch, "e1", items)
    fake.tokenizer = FakeTok()
    out = A.stage_run(f"{pins.RUN_PREFIX}x51_12_e1_test", "e1")
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "51.12" and m["arms"] == list(A.ARMS) and "sealed" in m and m["items"] == 12
    assert m["frequency_control"] is None and "3f" not in m["pairs"]
    assert sorted(p.name for p in out.iterdir()) == ["agreement.json", "cases.jsonl", "gate.json", "manifest.json",
                                                     "norms.jsonl", "outcomes.jsonl", "plan.json", "readout.jsonl"]  # fmt: skip
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 12 * 2 * (1 + len(A.ARMS))
    norms = X.read_jsonl(out / "norms.jsonl")
    # both readers answer "5" on O and "3" on S: A = five / three, 4 one-token variants each; the digits stay out
    assert len(norms) == 12 and all(n["source"] == LK and n["A_tokens"] == 8 == n["A_rank"] for n in norms)
    assert all(n["A_words"] == ["five", "three"] and 0 <= n["n_answer_atoms_in_25"] <= 8 for n in norms)
    assert all(0 < n["share_A"] < 1 for n in norms)
    readout = X.read_jsonl(out / "readout.jsonl")
    assert len(readout) == 12 * 2 and all(set(r["answer_word_rank"]) == {LK, RC} for r in readout)
    assert all(r["answer_word_rank"][LK] >= 1 for r in readout)
    assert json.loads((out / "agreement.json").read_text())["lookup"]["whole"]["matched"] == 0  # no stored rows here


def z2_case(i: int) -> dict:
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    rd = lambda k: {"answer": "Spain", "cf_answer": "Italy", "ids": {"org": [*org, 7 + k], "alt": [*alt, 7 + k]},  # noqa: E731
                    "pos": 4, "tok_A": 5, "tok_b": 3, "tok_lure": None}  # fmt: skip
    return {"scene": f"z-{i}", "set": "j", "bridge": f"e{i % 4}", "cf_bridge": "bee", "desc": "d", "cf_desc": "cd",
            "readers": {"K": rd(0), "M": rd(1)}}  # fmt: skip


def test_stage_run_z2_end_to_end_with_the_frequency_control(tmp_path, monkeypatch):
    from bridge_jspace import pins

    items = [A.unit("z2", c, f"j|{c['scene']}", c["bridge"], c["cf_bridge"], {}) for c in map(z2_case, range(10))]
    fake = fake_run(tmp_path, monkeypatch, "z2", items)
    tok = fake.tokenizer = FakeTok()
    out = A.stage_run(f"{pins.RUN_PREFIX}x51_12_z2_test", "z2")
    m = json.loads((out / "manifest.json").read_text())
    assert m["arms"] == list(A.arms_of("z2")) and m["pairs"]["3f"] == ["no_A", "no_F"]
    assert m["frequency_control_summary"]["letters"] == 100
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 10 * 2 * (1 + len(A.ARMS) + 1) and sum(r["arm"] == A.F_ARM for r in rows) == 20
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 20 and {n["source"] for n in norms} == {"K", "M"}  # z2: one Δ per reader
    related = {"spain", "italy", "e0", "e1", "e2", "e3", "bee"}
    for n in norms:
        assert n["A_tokens"] == 4 and len(n["F_ids"]) == 4 and not set(n["F_ids"]) & set(n["A_ids"])
        assert not {A.key_of(tok.decode([f])) for f in n["F_ids"]} & related and 0 < n["share_F"] < 1
    cases = X.read_jsonl(out / "cases.jsonl")
    assert all(len(c["F"]) == 4 for c in cases)


# ---- planted run: the verdict, the view, the seal -----------------------------------------------------------------


def planted(tmp_path, monkeypatch, answer: str = "e1: entity 70%") -> None:
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    monkeypatch.setattr(A, "RUNS", {"z2": {}, "e1": {"qwen3.5-9b": "qwen35_9b_x51_12_e1_r2"}, "cue": {}})
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": answer)
    src = tmp_path / "qwen35_9b_x51_12_e1_r2"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "set": "e1", "layer": 12,
                                                   "source": "qwen35_9b_x0_necessity"}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"tested": True, "gate": {"pass": True}}))
    rows = rows_for(planted_sw(), RC) + rows_for({a: [0] * 20 for a in planted_sw()} | {"whole": [1] * 20}, LK)
    X.write_jsonl(src / "outcomes.jsonl", rows)
    items = [{"key": f"s{i}", "entity": f"e{i % 5}", "cf_entity": "x", "tokens": {"A": [1, 2]},
              "readers": {w: {"answer": "1", "cf_answer": "2", "ids": {"org": [1, 2, 3], "alt": [1, 4, 3]}, "pos": 1,
                              "suffix": [5]} for w in (LK, RC)}} for i in range(20)]  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", items)
    # the recall's word is read at the bridge word (rank 3: the arms decide); the lookup's never (rank 400)
    rd = [{"key": f"s{i}", "entity": f"e{i % 5}", "source": LK, "variant": v, "top": 1, "class": "answer",
           "own_answer_of": [LK], "other_answer": False, "other_bridge": False, "answer_rank": {LK: 1, RC: 3},
           "answer_word_rank": {LK: 400, RC: 3}, "bridge_rank": 2, "answer_digit_rank": {LK: 1, RC: 2}}
          for i in range(20) for v in ("org", "alt")]  # fmt: skip
    X.write_jsonl(src / "readout.jsonl", rd)
    nm = [{"key": f"s{i}", "entity": f"e{i % 5}", "source": LK, "A_tokens": 16, "A_rank": 16,
           "n_answer_atoms_in_25": int(i == 0), "share_jpp": 0.2, "share_A": 0.001} for i in range(20)]  # fmt: skip
    X.write_jsonl(src / "norms.jsonl", nm)
    (src / "agreement.json").write_text(json.dumps({"recall": {"whole": {"n": 20, "matched": 20, "agree_switch": 20,
                                                                         "agree_top": 20, "rerun": 10, "stored": 10}}}))  # fmt: skip


def test_verdict_and_view_on_a_planted_run(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch)
    out = A.stage_verdict(n_boot=100)
    text = (out / "verdict.md").read_text()
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["per_cell"]["e1|qwen3.5-9b|recall"] == A.LABELS["entity"]  # read: the arms decide
    assert blob["per_cell"]["e1|qwen3.5-9b|lookup"] == A.LABELS["not_read"]  # not read: said by measurement
    lk = blob["models"][0]["readers"]["lookup"]
    assert lk["arm_label"] == A.LABELS["na"] and lk["check"]["case"] == "not_read"
    assert "void" not in text.replace("never 'void by construction'", "")
    assert "| e1 | qwen3.5-9b | recall | 20 |" in text and "yes |" in text and "Dan: e1: entity 70%" in text
    assert "100% of 20 items; arms beside: can't tell" in text
    view = (A.stage_view(decode_for=lambda t: lambda ids: "".join(f"<{i}>" for i in ids)) / "view.md").read_text()
    assert view.count("⟦") == 1 + 5 * 2 * 2 and "### no_A_rand: 10 random rows of 40 (seed 0)" in view


def test_coverage_verdict_reads_the_coverage_runs_without_the_seal(tmp_path, monkeypatch):
    """Batch 52: the same planted run read as a coverage run: no Q51.12 line needed, 'no prediction' in its place."""
    planted(tmp_path, monkeypatch, answer="")
    monkeypatch.setattr(A, "COVERAGE_RUNS", {"e1": {"qwen3.5-9b": "qwen35_9b_x51_12_e1_r2"}})
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(n_boot=10)
    out = A.stage_verdict(n_boot=100, coverage=True)
    assert out.name.startswith("x52_answer-")
    text = (out / "verdict.md").read_text()
    assert A.NO_PREDICTION in text and "Dan:" not in text and "batch 52 coverage" in text
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["per_cell"]["e1|qwen3.5-9b|recall"] == A.LABELS["entity"] and blob["dan"].startswith(A.NO_PREDICTION)
    assert A.runs_of("e1")["qwen3.5-9b"] == "qwen35_9b_x51_12_e1_r2"


def test_lightning_is_a_coverage_target_of_e1_and_cue():
    assert set(A.COVERAGE_RUNS) == {"e1", "cue", "z2", "z1k", "z1p", "z2p"} and A.COVERAGE_RUNS["e1"] == {
        "nemotron-3.5-lightning": "nem35l_x52_answer"
    }
    assert A.COVERAGE_RUNS["cue"] == {"nemotron-3.5-lightning": "nem35l_x52_cue_answer"} and A.COVERAGE_RUNS["z2"] == {
        "nemotron-3.5-lightning": "nem35l_x52_answer_z2"
    }
    assert "nemotron-3.5-lightning" not in A.RUNS["e1"] and "nemotron-3.5-lightning" in A.runs_of("e1")
    assert A.all_runs(("e1",), coverage=True) == [("e1", "nemotron-3.5-lightning", "nem35l_x52_answer")]


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, answer="")
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_view()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["qwen35_9b_x51_12_e1_r2"]


def test_dan_answer_reads_only_the_q51_12_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q51.11** x\n\nDan: one code\n\n**Q51.12** (51.12) answer directions\n- Z2: 9B; 27B.\n\nDan:{}\n\n"
              "**Q51.13** next\n\nDan: (a)\n")  # fmt: skip
    monkeypatch.setattr(A.subprocess, "run", fake_git(blocks.format("")))
    assert A.dan_answer() == ""
    monkeypatch.setattr(A.subprocess, "run", fake_git(blocks.format(" Z2 entity 60%")))
    assert A.dan_answer() == "Z2 entity 60%"
    monkeypatch.setattr(A.subprocess, "run", fake_git(blocks.format("\nDan (27B): answer 55%\n- E1 entity")))
    assert "Dan (27B): answer 55%" in A.dan_answer() and "- E1 entity" in A.dan_answer()


def test_the_committed_predictions_file_has_the_q51_12_block():
    text = A.subprocess.run(["git", "show", f"HEAD:{A.PREDICTIONS}"], cwd=A.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{A.QUESTION}**" in text and isinstance(A.dan_answer(), str)


def test_run_names_and_spec_ids():
    from bridge_jspace import pins

    for s in A.SETS:
        for t, name in A.RUNS[s].items():
            assert name.startswith(pins.TARGETS[t]["run_prefix"]) and "_raw" not in name and name.endswith("_r2")
            assert A.SPEC_IDS[s][t] == f"x51_12_{s}_{A.TAGS[t]}_r2"
    assert set(A.RUNS["e1"]) == {"qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"} and set(A.RUNS["z2"]) == set(
        A.RUNS["cue"]
    )
    assert np.isclose(A.ENTITY_KEEP, 0.7) and np.isclose(A.ANSWER_KEEP, 0.3) and np.isclose(A.ANSWER_A_MIN, 0.5)
    assert (
        A.NOT_READ_RANK == 50 and math.isclose(A.NOT_READ_SHARE, 0.9) and set(A.FREQ_SETS) & set(A.SETS) == {"z2"}
    )  # the design: Z2 only (the named sets: batch 52)


def test_zachs_named_passages_k_and_p_are_coverage_sets():
    """Dan's morning brief item 2: 51.12's arms on Zach's named passages, K (Z1's runs) and P (Z1-P's runs), read like
    Z2 (each reader's own Δ at the patch token, word answers, the frequency-matched control), on the 9B, 27B and
    Lightning at the committed L; no prediction (coverage runs)."""
    from scripts import x50_zach as Z

    for s in ("z1k", "z1p"):
        assert s in A.ZACH_SETS and s in A.FREQ_SETS and s not in A.NUMBER_SETS and s not in A.RUNS
        assert set(A.COVERAGE_RUNS[s]) == {"qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning"}
        assert A.DECISIVE[s] == ("lookup", "recall")
        for t in A.COVERAGE_RUNS[s]:
            assert A.layer_of(s, t) == Z.LAYERS[t][0]
    assert A.source_of("z1k", "qwen3.5-9b").name == Z.RUNS["z1"]["qwen3.5-9b"]
    assert A.source_of("z1k", "nemotron-3.5-lightning").name == Z.COVERAGE_RUNS["z1"]["nemotron-3.5-lightning"]
    assert A.source_of("z1p", "qwen3.6-27b").name == Z.COVERAGE_RUNS["z1p"]["qwen3.6-27b"]
    assert A.source_of("z2", "qwen3.5-9b").name == Z.RUNS["z2"]["qwen3.5-9b"]  # unchanged


# ---- batch 53, 53.1b: PP vs MP -------------------------------------------------------------------------------------


def test_z2p_is_53_1b_mp_set_read_like_z2():
    """53.1b: MP / MM (x50_zach part z2p) read like Z2 (each reader's own Δ at the description's last token, word
    answers, the frequency-matched control), 9B and 27B at the committed L; PP / PM are the z1p runs."""
    from scripts import x50_zach as Z

    assert "z2p" in A.ZACH_SETS and "z2p" in A.FREQ_SETS and "z2p" not in A.NUMBER_SETS and "z2p" not in A.RUNS
    assert "z2p" in A.ALL_SETS and "z2p" not in A.SETS and A.DECISIVE["z2p"] == ("lookup", "recall")
    assert set(A.COVERAGE_RUNS["z2p"]) == set(A.JSUITE["targets"]) == {"qwen3.5-9b", "qwen3.6-27b"}
    for t in A.JSUITE["targets"]:
        assert A.layer_of("z2p", t) == Z.LAYERS[t][0] == X.PREDICTED[t]
        assert A.source_of("z2p", t).name == Z.COVERAGE_RUNS["z2p"][t]
        assert A.COVERAGE_RUNS["z1p"][t] in [r for s, tt, r in A.jsuite_runs() if (s, tt) == ("z1p", t)]
    assert [s for s, _, _ in A.jsuite_runs()] == ["z1p", "z1p", "z2p", "z2p"]
    assert A.JSUITE["cells"] == {"z1p": {"K": "PP", "M": "PM"}, "z2p": {"K": "MP", "M": "MM"}}
    assert Z.WORDS["z1p"] == ("PP", "PM") and Z.WORDS["z2p"] == ("MP", "MM")


def test_z2p_items_rebuild_from_a_z2p_source_run(tmp_path, monkeypatch):
    """The z2p items are the source run's chosen passages, rebuilt by x50_zach.encode (part z2p) and checked id by id;
    the lookup's answers are the MP passage's made-up values, the recall's the true facts."""
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x45m
    from scripts import x50_zach as Z
    from tests.test_x47_cue import FakeLens, FakeModel

    try:
        tok = x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    monkeypatch.setattr(M, "load_model", lambda: FakeModel(tok, n_layers=40))
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    monkeypatch.setattr(Z, "N_ITEMS", 3)
    real_load = Z.load_pairs
    monkeypatch.setattr(Z, "load_pairs", lambda s, p: (real_load(s, p)[0][:40], {}))
    monkeypatch.setattr(Z, "desc_competence", lambda model, prompts: [
        {**{k: q[k] for k in ("relation", "entity", "desc", "template", "instruction")}, "greedy": q["entity"],
         "right": True} for q in prompts])  # fmt: skip
    monkeypatch.setattr(Z, "competence", lambda model, cases, ws: [
        {"scene": c["scene"], "set": c["set"], "reader": w, "variant": v, "greedy": "x", "right": True,
         "read_right": True, "top": 0} for c in cases for w in Z.READERS for v in ("org", "alt")])  # fmt: skip
    src = Z.stage_run(f"{pins.RUN_PREFIX}fake_x53_z2p", "z2p")
    assert json.loads((src / "manifest.json").read_text())["question"] == Z.NO_PREDICTION_Z2P
    monkeypatch.setattr(A, "source_of", lambda s, t: src)
    items, gate, counts = A.BUILD["z2p"](tok, pins.TARGET)
    assert gate["pass"] and len(items) == counts["items"] == 3
    stored = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    for it in items:
        old = stored[tuple(it["key"].split("|"))]
        assert it["set"] == "z2p" and (it["desc"], it["cf_desc"]) == (old["desc"], old["cf_desc"])
        k, m = it["readers"]["K"], it["readers"]["M"]
        assert k["src"] == "K" and m["src"] == "M" and k["suffix"] == m["suffix"] == []
        ctx, rel, w = old["readers"]["K"]["context"], old["relation"], old["wording"]
        assert k["answer"] == Z.lure(rel, w, old["bridge"], ctx)
        assert k["cf_answer"] == Z.lure(rel, w, old["cf_bridge"], ctx)
        assert m["answer"] == Z.fact(rel, old["bridge"]) and m["cf_answer"] == Z.fact(rel, old["cf_bridge"])
        assert A.item_tokens(tok, it)["A"]  # word answers: first tokens of each answer word and variant


def test_jsuite_verdict_puts_pp_beside_mp_without_a_q_line(tmp_path, monkeypatch):
    """53.1b's verdict: 51.12's rules on the z1p runs (PP / PM) and the z2p runs (MP / MM), 9B and 27B, into
    x53_jsuite-<UTC>/; no Q-line; a run not here yet is 'pending'."""
    real = A.RESULTS
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    for t in A.JSUITE["targets"]:
        run = A.COVERAGE_RUNS["z1p"][t]
        if not (real / run / "manifest.json").exists():
            pytest.skip(f"{run} is not in this checkout")
        (tmp_path / run).symlink_to(real / run)
    out = A.stage_verdict(n_boot=100, jsuite=True)
    assert out.name.startswith("x53_jsuite-") and out.parent == tmp_path
    blob = json.loads((out / "verdict.json").read_text())
    text = (out / "verdict.md").read_text()
    assert blob["dan"].startswith(A.NO_PREDICTION_JSUITE) and "Dan:" not in text and "batch 53, 53.1b" in text
    for t in A.JSUITE["targets"]:
        cells = blob["jsuite_cells"][t]
        assert cells["MP"] == cells["MM"] == "pending"
        assert cells["PP"] == f"{blob['per_cell'][f'z1p|{t}|lookup']} (n 200)"
    assert "| qwen3.5-9b | " in text and "PP (lookup) | MP (lookup)" in text
