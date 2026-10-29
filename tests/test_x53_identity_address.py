"""Batch 53, test 53.6 (scripts/x53_identity_address.py): the scene roles (A, B, C, their slots and answer tokens; the
ambiguous-legs drop), the classes, the arms' vectors, the rule's labels at the bars, and the run and verdict stages end
to end on x49_das_pos's tiny fake causal model with x51_das's word-tokenizer C0 scenes (CPU). No real model."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
import pytest
import test_x49_das_pos as T49
import torch
from test_x51_das import all_right, c0_cases

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W
from scripts import x53_identity_address as IA

LK, RC = X.LOOKUP, X.RECALL


def test_roles_are_a_b_c_with_their_slots_and_tokens_and_ambiguous_legs_drop():
    tok = T49.WordTok()
    cases = c0_cases(tok, 40, seed=3)
    kept, n_amb = 0, 0
    for c in cases:
        legs = dict(T49.LEGS)
        r = IA.roles(tok, c, legs)
        items = [x for x, _ in W.slots_of(c["context"])]
        third = next(x for x in items if x not in (c["bridge"], c["cf_bridge"]))
        if legs[third] in (legs[c["bridge"]], legs[c["cf_bridge"]]):
            assert r is None
            n_amb += 1
            continue
        kept += 1
        assert r is not None
        assert (r["original"]["item"], r["B"]["item"], r["C"]["item"]) == (c["bridge"], c["cf_bridge"], third)
        assert [r[k]["slot"] for k in ("original", "B", "C")] == [
            items.index(r[k]["item"]) for k in ("original", "B", "C")
        ]
        assert (
            r["original"]["tok_legs"] == c["readers"][RC]["tok_A"] and r["B"]["tok_legs"] == c["readers"][RC]["tok_b"]
        )
        assert (
            r["original"]["tok_digit"] == c["readers"][LK]["tok_A"] and r["B"]["tok_digit"] == c["readers"][LK]["tok_b"]
        )
        assert IA.classify(r["C"]["tok_legs"], r, "tok_legs") == "C" and IA.classify(-1, r, "tok_legs") == "other"
    assert kept and n_amb  # both kinds occur in 40 planted scenes


def test_arm_vectors():
    g = torch.Generator().manual_seed(0)
    lens, addr, r = (torch.randn(8, generator=g) for _ in range(3))
    r = r / r.norm()
    v = IA.arm_vectors(lens, addr, r)
    assert torch.allclose(v["both"], lens + addr) and torch.allclose((v["both_rand"] - lens).norm(), addr.norm())
    assert set(v) == set(IA.ARMS) - {"none"}


@pytest.mark.parametrize(
    ("b", "c", "want"),
    [(0.4, 0.2, "identity"), (0.4, 0.2001, "both"), (0.2, 0.4, "address"), (0.2001, 0.4, "both"), (0.3, 0.0, "identity"),
     (0.0, 0.1, "address"), (0.0, 0.0, "neither"), (0.3, 0.3, "both")],
)  # fmt: skip
def test_rule_labels_at_the_bars(b, c, want):
    assert IA.label(b, c) == want


def test_run_and_verdict_end_to_end_on_the_fake_model(tmp_path, monkeypatch):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    tok = T49.WordTok()
    cases = c0_cases(tok, 60, seed=5)
    fake = T49.FakeModel(tok)
    g = torch.Generator().manual_seed(7)
    mu = {k: torch.randn(T49.D_MODEL, generator=g).numpy() for k in range(3)}
    run = f"{pins.RUN_PREFIX}fake_53_6"
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", T49.FakeLens)
    monkeypatch.setattr(IA, "c0_cases", lambda tok_, n_gen=None: (cases, {"planted": 0}))
    monkeypatch.setattr(R, "pools", lambda tok_: (dict(T49.LEGS), list(T49.ANIMALS), ["Iris", "Tom", "Ann"]))
    monkeypatch.setattr(X, "competence", all_right)
    monkeypatch.setattr(MM, "pointer_means", lambda run_: mu)
    monkeypatch.setattr(IA, "RUNS", {pins.TARGET: run})
    monkeypatch.setattr(IA, "RESULTS", tmp_path / "x53_identity_address")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(IA, "SPEC", tmp_path / "batch53.yaml")
    IA.SPEC.write_text("")
    out = IA.stage_run(run, "test", n_items=20)
    used = X.read_jsonl(out / "cases.jsonl")
    assert len(used) == 20 and all(c["roles"]["C"]["legs"] not in (c["roles"]["original"]["legs"], c["roles"]["B"]["legs"])
                                   for c in used)  # fmt: skip
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {(c["scene"], w, a) for c in used for w in (LK, RC)
                                                                   for a in IA.ARMS}  # fmt: skip
    # the address arm's vector: 2 (mu_C - mu_A) at the bridge word, recomputed through the fake's own read
    from scripts.exp04_brew_parts import AddRows

    c0 = used[0]
    addr = 2 * (torch.tensor(mu[c0["roles"]["C"]["slot"]]) - torch.tensor(mu[c0["roles"]["original"]["slot"]]))
    lg: Any = fake.generate_batch(torch.tensor([c0["readers"][RC]["ids"]["org"] + c0["space"]]), 1,
                             [{X.PREDICTED[pins.TARGET]: AddRows(addr[None].float(), [c0["pos"]])}], first_logits=True)[1]  # fmt: skip
    rec = next(r for r in rows if r["scene"] == c0["scene"] and r["reader"] == RC and r["arm"] == "addr")
    assert rec["top"] == int(lg[0].argmax())
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 20 and all(r["norm_addr"] > 0 and 0 <= r["share_lens"] <= 1 + 1e-6 for r in norms)
    gate = json.loads((out / "gate.json").read_text())
    assert gate["pass"] and gate["used"] == 20 and gate["roles"]["kept"] == gate["cases"]
    v = IA.stage_verdict([run], n_boot=50)
    assert v.name.startswith("x53_identity_address-") and v.parent == IA.RESULTS
    blob = json.loads((v / "verdict.json").read_text())
    mdl = blob["models"][0]
    both = [r for r in rows if r["reader"] == RC and r["arm"] == "both"]
    b, c = (np.mean([r["class"] == k for r in both]) for k in ("B", "C"))
    assert mdl["cells"][RC]["both"]["B"][0] == pytest.approx(b) and mdl["label"] == IA.label(float(b), float(c))
    md = (v / "verdict.md").read_text()
    assert "UNVERIFIED" in md and "no prediction" in md and (v / "x53_identity_address.png").exists()
    assert (v / "examples.md").read_text().count("### C0-") == 10
