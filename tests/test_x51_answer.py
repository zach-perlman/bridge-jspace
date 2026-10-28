"""Batch 51, test 51.12 (scripts/x51_answer.py): the answer directions (variants, span), the parts (the J++ part with A
projected out, A alone), the OMP support against signed_omp, the arms against the stored runs' removal path, the
rules on planted numbers (bars inclusive), the readout classes, the arm-1 agreement, the verdict on a planted run, and
the seal. No real model."""

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x51_answer as A
from scripts.exp04_brew_parts import signed_omp

LK, RC = X.LOOKUP, X.RECALL


class FakeTok:
    """Word-level: a leading space before a digit is its own token (as on Qwen), before a word it is part of it."""

    def __init__(self):
        self.vocab: dict[str, int] = {}

    def _id(self, s: str) -> int:
        return self.vocab.setdefault(s, len(self.vocab))

    def __call__(self, text: str, add_special_tokens: bool = False):
        split = text.startswith(" ") and text[1:2].isdigit()
        return SimpleNamespace(input_ids=[self._id(" "), self._id(text[1:])] if split else [self._id(text)])

    def decode(self, ids, **_):
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv[int(i)] for i in ids)


def test_variants_drop_whitespace_first_tokens_and_keep_caps():
    tok = FakeTok()
    ids = A.variant_ids(tok, ["5", "europe"])
    words = sorted(tok.decode([i]) for i in ids)
    assert words == [" Europe", " europe", "5", "Europe", "europe"]  # " 5" -> " " dropped; "5" has no capital


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


def test_all_arms_follow_the_stored_removal_path():
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    g = torch.Generator().manual_seed(2)
    d = 24
    delta, pj = torch.randn(3, d, generator=g), torch.randn(3, d, generator=g)
    q = A.answer_basis(torch.randn(2, d, generator=g))
    basis = SP.random_basis(d, torch.Generator().manual_seed(888))
    arms, sh = A.all_arms(delta, pj, [q, q, q], basis)
    assert tuple(arms) == A.ARMS
    old, _ = R.removal_arms(delta, {"jpp": pj}, basis)  # x50_zach / x47_cue's arms (X0's: x - part, x - rand)
    assert torch.equal(arms["no_jpp"], old["no_jpp"]) and torch.equal(arms["no_jpp_rand"], old["no_jpp_rand"])
    assert torch.allclose(arms["no_A"], delta - (delta @ q) @ q.T, atol=1e-5)
    assert torch.allclose(sh["A_in_jpp"] + sh["jpp_A"], sh["jpp"], atol=1e-4)  # orthogonal split of the J++ part


@pytest.mark.parametrize(
    ("e", "key"),
    [((0.5, 0.35, 0.10), "entity"),  # bars inclusive: 0.7 of arm 1, 0.10
     ((0.5, 0.15, 0.25), "answer"),  # 0.3 and 0.5 of arm 1
     ((0.5, 0.35, 0.11), "mixed"), ((0.5, 0.2, 0.2), "mixed"), ((0.0, 0.3, 0.3), "na"), ((float("nan"), 0, 0), "na"),
     ((-0.1, 0.0, 0.0), "na")],
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
    assert r["n"] == 20 and r["entities"] == 5
    assert r["extra"]["1"][0] == pytest.approx(0.6) and r["extra"]["2"][0] == pytest.approx(0.5)
    assert r["extra"]["3"][0] == pytest.approx(0.0) and r["share2"][0] == pytest.approx(5 / 6)
    assert r["key"] == "entity" and r["valid"] is False  # 10 switches < X0's 30 (beside, not in the rule)


def test_switch_of_47_3_lookup_follows_the_change():
    assert A.switch_of("cue", LK, {"route": "identity", "switched": 0}) == 1
    assert A.switch_of("cue", LK, {"route": "original", "switched": 0}) == 0
    assert A.switch_of("cue", RC, {"route": None, "switched": 1}) == 1
    assert A.switch_of("e1", LK, {"route": None, "switched": 1}) == 1


def test_readout_row_classes():
    it = {"key": "k", "entity": "frog", "readers": {LK: {"tok_A": 5, "tok_b": 6}, RC: {"tok_A": 7, "tok_b": 8}}}
    toks = {"own": {"org": {LK: [5], RC: [7]}, "alt": {LK: [6], RC: [8]}}, "bridge": {"org": [20], "alt": [21]}}
    digit_ids = [5, 6, 7, 8]
    lg = torch.zeros(30)
    lg[5], lg[7] = 3.0, 2.0  # the lookup's digit on top at O
    r = A.readout_row(it, toks, LK, "org", lg, digit_ids)
    assert r["class"] == "answer" and r["own_answer_of"] == [LK] and r["answer_rank"] == {LK: 1, RC: 2}
    assert r["answer_digit_rank"] == {LK: 1, RC: 2} and r["top_digit"] == 5
    lg = torch.zeros(30)
    lg[20] = 1.0
    assert A.readout_row(it, toks, LK, "org", lg, digit_ids)["class"] == "bridge"
    lg = torch.zeros(30)
    lg[6] = 1.0  # S's answer read at O: neither, flagged as the other prompt's answer
    r = A.readout_row(it, toks, LK, "org", lg, digit_ids)
    assert r["class"] == "neither" and r["other_answer"]


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


def test_stage_run_end_to_end_sealed(tmp_path, monkeypatch):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from tests.test_x49_gain import FakeLens, FakeModel, _item

    fake = FakeModel()
    fake.tokenizer = FakeTok()
    fake.letter_token_ids = lambda: torch.arange(20, 100)

    class Lens(FakeLens):
        def readout(self, h, layer):
            return h @ fake.unemb.T

    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", Lens)
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x51_answer")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(X, "whitespace_mask", lambda model: None)
    src = tmp_path / "src"
    src.mkdir()
    monkeypatch.setattr(A, "source_of", lambda s, t: src)
    cases = [_item(i) for i in range(12)]
    items = [A.unit("e1", c, c["scene"], c["entity"], c["cf_bridge"], {}) for c in cases]
    gate = {"pass": True, "chosen": 12}
    monkeypatch.setattr(A, "BUILD", {**A.BUILD, "e1": lambda tok, t: (items, gate, {"source": "src", "items": 12})})
    out = A.stage_run(f"{pins.RUN_PREFIX}x51_12_e1_test", "e1")
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "51.12" and m["arms"] == list(A.ARMS) and "sealed" in m and m["items"] == 12
    assert sorted(p.name for p in out.iterdir()) == ["agreement.json", "cases.jsonl", "gate.json", "manifest.json",
                                                     "norms.jsonl", "outcomes.jsonl", "plan.json", "readout.jsonl"]  # fmt: skip
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 12 * 2 * (1 + len(A.ARMS))
    norms = X.read_jsonl(out / "norms.jsonl")
    # both readers answer "5" on O and "3" on S: A = {"5", "3"} (" 5" / " 3" start with the space token: dropped)
    assert len(norms) == 12 and all(n["source"] == LK and n["A_tokens"] == 2 == n["A_rank"] for n in norms)
    assert all(n["n_answer_atoms_in_25"] == 0 for n in norms)  # digits are not in the letter dictionary
    assert len(X.read_jsonl(out / "readout.jsonl")) == 12 * 2
    assert json.loads((out / "agreement.json").read_text())["lookup"]["whole"]["matched"] == 0  # no stored rows here


# ---- planted run: the verdict, the view, the seal -----------------------------------------------------------------


def planted(tmp_path, monkeypatch, answer: str = "e1: entity 70%") -> None:
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    monkeypatch.setattr(A, "RUNS", {"z2": {}, "e1": {"qwen3.5-9b": "qwen35_9b_x51_12_e1"}, "cue": {}})
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": answer)
    src = tmp_path / "qwen35_9b_x51_12_e1"
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
    rd = [{"key": f"s{i}", "entity": f"e{i % 5}", "source": LK, "variant": v, "top": 1, "class": "answer",
           "own_answer_of": [LK], "other_answer": False, "other_bridge": False, "answer_rank": {LK: 1, RC: 3},
           "answer_digit_rank": {LK: 1, RC: 2}} for i in range(20) for v in ("org", "alt")]  # fmt: skip
    X.write_jsonl(src / "readout.jsonl", rd)
    nm = [{"key": f"s{i}", "entity": f"e{i % 5}", "source": LK, "A_tokens": 4, "A_rank": 4, "A_letter_tokens": 0,
           "n_answer_atoms_in_25": 0, "share_jpp": 0.2, "share_A": 0.001} for i in range(20)]  # fmt: skip
    X.write_jsonl(src / "norms.jsonl", nm)
    (src / "agreement.json").write_text(json.dumps({"recall": {"whole": {"n": 20, "matched": 20, "agree_switch": 20,
                                                                         "agree_top": 20, "rerun": 10, "stored": 10}}}))  # fmt: skip


def test_verdict_and_view_on_a_planted_run(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch)
    out = A.stage_verdict(n_boot=100)
    text = (out / "verdict.md").read_text()
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["per_cell"]["e1|qwen3.5-9b|recall"] == A.LABELS["entity"]
    assert blob["per_cell"]["e1|qwen3.5-9b|lookup"] == A.LABELS["na"]  # e1 = 0 on the lookup: can't tell
    assert "| e1 | qwen3.5-9b | recall | 20 |" in text and "yes |" in text and "Dan: e1: entity 70%" in text
    view = (A.stage_view(decode_for=lambda t: lambda ids: "".join(f"<{i}>" for i in ids)) / "view.md").read_text()
    assert view.count("⟦") == 1 + 5 * 2 * 2 and "### no_A_rand: 10 random rows of 40 (seed 0)" in view


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, answer="")
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_view()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["qwen35_9b_x51_12_e1"]


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
            assert name.startswith(pins.TARGETS[t]["run_prefix"]) and "_raw" not in name
            assert A.SPEC_IDS[s][t] == f"x51_12_{s}_{A.TAGS[t]}"
    assert set(A.RUNS["e1"]) == {"qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"} and set(A.RUNS["z2"]) == set(
        A.RUNS["cue"]
    )
    assert np.isclose(A.ENTITY_KEEP, 0.7) and np.isclose(A.ANSWER_KEEP, 0.3) and np.isclose(A.ANSWER_A_MIN, 0.5)
