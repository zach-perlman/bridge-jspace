"""early_push's pure helpers and prompt construction (tokenizer only, no model)."""

import json
import math
from pathlib import Path

import numpy as np
import pytest
import torch

import scripts.early_push as EP
from bridge_jspace import pins, tokens
from scripts import read_write as RW

TEMPLATE_TAIL = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nAnswer:"


@pytest.fixture(scope="module")
def tok():
    try:
        return tokens.load_tokenizer()
    except Exception:
        try:
            from huggingface_hub import try_to_load_from_cache
            from transformers import AutoTokenizer

            path = try_to_load_from_cache(pins.MODEL_REPO, "tokenizer.json", revision=pins.MODEL_REVISION)
            assert isinstance(path, str)
            return AutoTokenizer.from_pretrained(str(Path(path).parent))
        except Exception:
            pytest.skip("Qwen3.6-27B tokenizer not cached")


@pytest.fixture(scope="module")
def cases(tok):
    if not (RW.P.RESULTS / "map_A8_v1" / "cases.jsonl").exists():
        pytest.skip("map_A8_v1 cases not present")
    cfg = {**EP.DEFAULTS, "n": 2}
    return {c["id"]: c for c in EP.build_cases(tok, cfg)}


def by_family(cases, fam):
    return next(c for c in cases.values() if c["family"] == fam)


def test_position_subsets_partition_the_question_region(cases, tok):
    for c in cases.values():
        s, ids = c["subsets"], c["read"]["clean"]
        assert set(s["a"]) == set(s["b"]) | set(s["nb"]) and not set(s["b"]) & set(s["nb"])
        assert set(s["d"]) <= set(s["nb"]) and set(s["r"]) <= set(s["a"])
        assert tok.decode([ids[i] for i in s["d"]]) == TEMPLATE_TAIL
        assert tok.decode([ids[i] for i in s["b"]]).strip() == c["subject"]
        if c["family"] in ("BL", "BR", "B"):  # C changes the context: read_write's group is the whole question
            assert s["r"] == s["a"]
        else:  # C changes the cue (or the city, inside the subject phrase): read_write's group starts after it
            assert min(s["b"]) < min(s["r"])


def test_edits_change_only_the_intended_text(cases, tok):
    rl, bl = by_family(cases, "RL"), by_family(cases, "BL")
    x = rl["cf_bridge"]
    for c in cases.values():
        p = c["prompts"]
        for e in ("E-name", "E-insert", "E-head", "E-unrelated", "E-cue", "off"):
            if e in p:
                assert p[e].startswith("<|im_start|>user\n") and p[e].endswith(TEMPLATE_TAIL), (c["id"], e)
        clean = p["clean"]
        s0, s1 = c["subject_span"]
        x_name = c["cf_bridge"] if c["family"] in ("R", "B") else f"the {c['cf_bridge']}"
        assert p["E-name"] == clean[:s0] + x_name + clean[s1:]
        assert p["E-insert"].startswith(clean[:s1] + ", " + x_name) and p["E-insert"].endswith(clean[s1 + 1 :])
        # token level: everything before the subject and from the question mark / ' have' on is unchanged
        k = EP.common_suffix(c["read"]["clean"], c["read"]["E-name"])
        assert k >= len(c["read"]["clean"]) - max(c["subsets"]["b"]) - 1
        # E-unrelated: the whole question region and template line up from the end
        ku = EP.common_suffix(c["read"]["clean"], c["read"]["E-unrelated"])
        assert ku >= len(c["read"]["clean"]) - min(c["subsets"]["a"])
        assert len(c["read"]["E-cue"]) == len(c["read"]["clean"])  # C is token-aligned (the activation patch needs it)
    assert "Which locker belongs to the " + x + "?" in rl["prompts"]["E-name"]
    assert bl["prompts"]["E-name"] == rl["prompts"]["E-name"]  # same scene, same context: the same direct question
    assert f"{bl['cue']}'s {bl['cf_bridge']}?" in bl["prompts"]["E-head"]
    assert f"the {x} known for {rl['cue']}?" in rl["prompts"]["E-head"]
    assert f"known for {rl['cue']}, the {x}?" in rl["prompts"]["E-insert"]
    rr = by_family(cases, "RR")
    assert f"known for {rr['cue']}, the {rr['cf_bridge']}, have?" in rr["prompts"]["E-insert"]
    r = by_family(cases, "R")
    assert "E-head" not in r["prompts"] and f"What is the capital of {r['cf_bridge']}?" in r["prompts"]["E-name"]


def test_candidates_and_off_answer(cases):
    for c in cases.values():
        cand = c["cand"]
        assert cand["A"] != cand["b"] and cand["A"] not in cand["oc"] and cand["b"] not in cand["oc"]
        if c["family"] in ("BL", "RL"):  # O swaps X's and Z's lockers: X's answer in O is Z's clean locker
            assert c["cand_text"]["bO"] == str(c["lockers"][c["third"]]) and cand["bO"] in cand["oc"]


def test_push_norms_and_random_control_match():
    d = torch.randn(16)
    norms = torch.tensor([0.0, 1.0, 2.5, 7.0])
    v = EP.push_rows(d, norms)
    assert torch.allclose(v.norm(dim=-1), norms, atol=1e-5)
    cos = (v[1:] @ torch.nn.functional.normalize(d, dim=0)) / norms[1:]
    assert torch.allclose(cos, torch.ones(3), atol=1e-5)
    r = EP.null_rows(v, torch.Generator().manual_seed(0))
    assert torch.allclose(r.norm(dim=-1), norms, atol=1e-5)
    assert torch.count_nonzero(EP.push_rows(d, torch.zeros(3))) == 0  # zero scale: no edit at all


def test_projection_removes_pushed_directions():
    vecs = torch.randn(3, 2, 8)  # 3 positions, 2 layers' added vectors
    q = EP.basis(vecs)
    x = torch.randn(3, 8)
    y = EP.project_out(x, q)
    assert torch.allclose(torch.einsum("pd,pkd->pk", y, vecs), torch.zeros(3, 2), atol=1e-5)
    edit = {1: EP.AddRows(vecs[:, 0], [2, 3, 4]), 2: EP.AddRows(vecs[:, 1], [2, 3, 4])}
    b = EP.row_basis(edit)
    assert b is not None
    z = EP.perp(torch.randn(6, 8), b, lo=1)  # positions 1..6; the push sits at 2-4
    assert torch.allclose(torch.einsum("pd,pkd->pk", z[1:4], vecs), torch.zeros(3, 2), atol=1e-5)


def test_agreement_statistics():
    a = np.array([1, 1, 0, 0, 1, 0], bool)
    assert EP.kappa(a, a) == pytest.approx(1.0)
    assert EP.kappa(a, ~a) == pytest.approx(-1.0)
    assert math.isnan(EP.kappa(a, np.ones(6, bool)))  # a constant reference has no kappa
    assert EP.jaccard(a, np.array([1, 0, 0, 0, 1, 1], bool)) == pytest.approx(2 / 4)
    pt, lo, hi = EP.boot(EP.kappa, [a, a], n_boot=200)
    assert pt == pytest.approx(1.0) and lo <= pt <= hi


def test_js_divergence():
    p = torch.tensor([0.7, 0.2, 0.1]).log()
    q = torch.tensor([0.1, 0.2, 0.7]).log()
    assert float(EP.js_divergence(p[None], p)[0]) == pytest.approx(0.0, abs=1e-6)
    js = float(EP.js_divergence(p[None], q)[0])
    assert js == pytest.approx(float(EP.js_divergence(q[None], p)[0]))
    assert 0 < js <= math.log(2)


def test_common_suffix_and_char_diff():
    assert EP.common_suffix([1, 2, 3, 4], [9, 3, 4]) == 2
    assert EP.char_diff("Which locker belongs to Jack's pet?", "Which locker belongs to the dog?") == (24, 31)


def test_manifest_doc_has_the_decision_rule():
    doc = EP.__doc__ or ""
    assert "Decision rule" in doc and "K1" in doc and "Predictions" in doc
    json.dumps(EP.DEFAULTS)
