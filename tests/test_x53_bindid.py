"""Batch 53, test 53.8 (scripts/x53_bindid.py): the vector construction (mean over scenes of the mention's state minus its
token embedding, per slot), the doses matched to the real identity change's norm, the controls at equal norms, the
pairing of X / Y / random reads, the rule at its bars, a failed gate giving "not tested", the mention positions and the
held-out pools on the target's tokenizer (9B, Muse: where cached), and the run and verdict end to end on x49_das_pos's
tiny fake causal model with x51_das's word-tokenizer C0 scenes (CPU). No real model."""

from __future__ import annotations

import json
import re

import numpy as np
import pytest
import test_x49_das_pos as T49
import torch
import yaml
from test_x51_das import all_right, c0_cases

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x8_write as W
from scripts import x53_bindid as B

LK, RC = X.LOOKUP, X.RECALL


def test_rule_is_dans_text_verbatim():
    spec = yaml.safe_load(B.SPEC.read_text())
    norm = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
    assert norm(B.RULE_VERBATIM) in norm(spec["critic_1125"])


# ---- the vectors and the doses -------------------------------------------------------------------------------------


def test_mention_codes_are_the_mean_of_state_minus_embedding_per_slot():
    g = torch.Generator().manual_seed(0)
    n, d = 400, 16
    slot_code = torch.randn(3, d, generator=g) * 3
    e = torch.randn(n, 3, d, generator=g)  # each scene's item embeddings (items vary by scene)
    h = e + slot_code[None] + 0.1 * torch.randn(n, 3, d, generator=g)  # the state: token + the slot's code + noise
    codes = B.mention_codes(h, e)
    assert codes.shape == (3, d)
    assert torch.allclose(codes, (h - e).mean(0))
    assert torch.allclose(codes, slot_code, atol=0.05)  # the planted per-slot code comes back
    with pytest.raises(AssertionError):
        B.mention_codes(h, e[:, :2])


@pytest.mark.parametrize("slot_a", [0, 1, 2])
def test_doses_match_the_real_change_and_controls_have_equal_norms(slot_a):
    g = torch.Generator().manual_seed(slot_a)
    codes = torch.randn(3, 32, generator=g) * torch.tensor([[50.0], [3.0], [0.2]])  # very different raw norms
    rand = torch.randn(32, generator=g) * 7
    delta = torch.randn(32, generator=g)
    size = float(delta.norm())
    v = B.arm_vectors(codes, rand, slot_a, size, delta)
    assert list(v) == B.arm_names(slot_a)[1:] and B.arm_names(slot_a)[0] == "none"
    assert torch.equal(v["whole"], delta)
    others = [k for k in B.SLOTS if k != slot_a]
    assert f"code{slot_a}_x1" not in v and f"code{slot_a}_x2" not in v  # never A's own slot
    for d in B.DOSES:
        arms = [f"code{k}_x{d}" for k in others] + [f"rand_x{d}"]
        assert len(arms) == 3  # X's vector, Y's version (the other code arm), random
        for a in arms:
            assert float(v[a].norm()) == pytest.approx(d * size, rel=1e-5)
        for k in others:  # the direction is the slot's code
            assert torch.allclose(v[f"code{k}_x{d}"] / v[f"code{k}_x{d}"].norm(), codes[k] / codes[k].norm(), atol=1e-6)
        assert torch.allclose(v[f"rand_x{d}"] / v[f"rand_x{d}"].norm(), rand / rand.norm(), atol=1e-6)
    assert torch.allclose(v[f"code{others[0]}_x2"], 2 * v[f"code{others[0]}_x1"], atol=1e-5)


# ---- reads, pairs, the rule ----------------------------------------------------------------------------------------


def planted(n_scenes: int, p_hit: float, seed: int = 0) -> tuple[list[dict], list[dict]]:
    """Cases with slots and lookup rows where, at every dose, each slot's vector sends the lookup to that slot's locker
    with probability p_hit and otherwise leaves it on A's; the random vector always leaves it on A's. So X's share
    under X's vector is about p_hit, under Y's version and random 0, and Y's version sends to Y's locker as often."""
    rng = np.random.default_rng(seed)
    cases, rows = [], []
    for i in range(n_scenes):
        a = i % 3
        s = f"C0-{i:04d}"
        cases.append({"scene": s, "bridge": f"e{i % 7}", "slots": {"slot_a": a, "slot_b": (a + 1) % 3}})
        others = [k for k in B.SLOTS if k != a]
        lk = {"none": a, "whole": (a + 1) % 3}
        for d in B.DOSES:
            for x in others:
                lk[f"code{x}_x{d}"] = x if rng.random() < p_hit else a
            lk[f"rand_x{d}"] = a
        for arm, slot in lk.items():
            rows.append(
                {"scene": s, "entity": f"e{i % 7}", "reader": LK, "arm": arm, "slot": slot, "kept": int(slot == a)}
            )
            rows.append({"scene": s, "entity": f"e{i % 7}", "reader": RC, "arm": arm, "slot": None, "kept": 1})
    return cases, rows


def test_pair_rows_read_x_under_x_y_and_random():
    cases, rows = planted(60, 0.7)
    pairs = B.pair_rows(rows, cases)
    assert len(pairs) == 2 * len(cases)
    lk = {(r["scene"], r["arm"]): r["slot"] for r in rows if r["reader"] == LK}
    for p in pairs:
        assert {p["x"], p["y"], p["a"]} == {0, 1, 2}
        for d in B.DOSES:
            assert (p[f"X_x{d}"] == "X") == (lk[(p["scene"], f"code{p['x']}_x{d}")] == p["x"])
            # Y's version: the other slot's vector; it sends to its own slot (role Y) or A's (original), never X's here
            assert p[f"Y_x{d}"] in ("Y", "original") and p[f"R_x{d}"] == "original"
    cell = B.dose_cell(pairs, 2, n_boot=200)
    x = np.mean([lk[(p["scene"], f"code{p['x']}_x2")] == p["x"] for p in pairs])
    assert cell["X"][0] == pytest.approx(x) and cell["Y"][0] == 0 and cell["R"][0] == 0
    assert cell["X_minus_R"][0] == pytest.approx(x) and cell["X_minus_R"][1] <= x <= cell["X_minus_R"][2]
    assert cell["roles"]["Y"]["Y"][0] == pytest.approx(x)  # Y's version sends to Y's locker as often as X's to X's
    assert cell["entities"] == 7 and cell["scenes"] == 60
    col = B.collateral(rows, cases, n_boot=50)
    assert col["none"]["lookup"][0] == 1 and col["whole_lookup_to_B"][0] == 1
    assert col["code_x2"]["lookup"][0] == pytest.approx(1 - x) and col["code_x2"]["n"] == 120
    assert col["rand_x1"]["recall"][0] == 1


@pytest.mark.parametrize(
    ("x_rand", "x_y", "want"),
    [(0.25, 0.15, "shared"), (0.40, 0.30, "shared"), (0.2499, 0.15, "between"), (0.25, 0.1499, "between"),
     (0.60, 0.0, "between"), (0.05, 0.40, "no"), (0.0501, 0.0, "between"), (0.0, 0.0, "no"), (-0.10, 0.20, "no"),
     (0.25 - 1e-12, 0.15 - 1e-12, "shared")],
)  # fmt: skip
def test_rule_at_its_bars(x_rand, x_y, want):
    assert B.label(x_rand, x_y) == want


def test_gate_status():
    ok = {"pass": True, "used": 300, "org_read_accuracy": {LK: 1.0, RC: 0.9}, "gate_min": 0.8}
    assert B.gate_status(ok) is None
    bad = {**ok, "pass": False, "org_read_accuracy": {LK: 0.95, RC: 0.7512}}
    assert B.gate_status(bad) == "not tested (gate 0.751 < 0.80)"
    assert B.gate_status({**ok, "used": 0}) == "not tested (no eligible scene)"


# ---- the target's tokenizer (9B, Muse: run with BJ_TARGET; skipped where it is not cached) ------------------------


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


def test_mention_positions_and_slots_on_the_target_tokenizer(tok):
    from scripts import suite_v1 as S

    cases, _ = B.c0_cases(tok, 12)
    assert len(cases) == 12
    for c in cases:
        pos = B.mention_positions(tok, c)
        assert pos is not None and pos == sorted(pos) and pos[-1] < c["pos"]  # locker sentences before the pick
        ids = c["readers"][LK]["ids"]["org"]
        for p, (x, _) in zip(pos, W.slots_of(c["context"]), strict=True):
            assert ids[p] == S.ids(tok, " " + x)[0] and tok.decode([ids[p]]).strip() == x
        sl = B.slot_info(tok, c)
        assert sl["items"][sl["slot_a"]] == c["bridge"] and sl["items"][sl["slot_b"]] == c["cf_bridge"]
        assert len(set(sl["tokens"])) == 3  # three distinct locker digits: the lookup's slot is unambiguous


def test_pools_are_the_generators_c0_prefix_and_held_out(tok):
    cases, _ = B.c0_cases(tok, 30)
    test, mean = B.split_pools(cases, 20, 10)
    assert [c["scene"] for c in test] == [c["scene"] for c in cases[:20]]
    assert [c["scene"] for c in mean] == [c["scene"] for c in cases[20:30]]
    assert not {c["context"] for c in test} & {c["context"] for c in mean}
    small, _ = B.c0_cases(tok, 20)  # prefix-stable: more scenes per condition keep the first ones
    assert [c["context"] for c in small] == [c["context"] for c in test]


# ---- run and verdict on the fake model -------------------------------------------------------------------------------


@pytest.fixture
def fake_env(tmp_path, monkeypatch):
    from bridge_jspace import model as M

    tok = T49.WordTok()
    cases = c0_cases(tok, 60, seed=5)
    fake = T49.FakeModel(tok)
    run = f"{pins.RUN_PREFIX}fake_53_8"
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(B, "c0_cases", lambda tok_, n_gen=None: (cases, {"planted": 0}))
    monkeypatch.setattr(X, "render", lambda tok_, item, rendering, context: f"{context} {item['question']} Answer:")
    monkeypatch.setitem(pins.TARGETS[pins.TARGET], "bos", False)  # the word tokenizer has no BOS
    monkeypatch.setattr(X, "competence", all_right)
    monkeypatch.setattr(B, "pointer_refs", lambda target: (None, None, "not available (test)"))
    monkeypatch.setattr(B, "RUNS", {pins.TARGET: run})
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x53_bindid")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(B, "SPEC", tmp_path / "batch53.yaml")
    B.SPEC.write_text("")
    return {"tok": tok, "cases": cases, "fake": fake, "run": run}


def test_run_and_verdict_end_to_end_on_the_fake_model(fake_env):
    from scripts.exp04_brew_parts import AddRows

    tok, cases, fake, run = fake_env["tok"], fake_env["cases"], fake_env["fake"], fake_env["run"]
    layer = X.PREDICTED[pins.TARGET]
    out = B.stage_run(run, "test", n_items=20, n_test=40, n_mean=20)
    gate = json.loads((out / "gate.json").read_text())
    assert gate["pass"] and gate["used"] == 20 and gate["test_pool"] == 40 and gate["mean_pool"] == 20
    used = X.read_jsonl(out / "cases.jsonl")
    assert [c["scene"] for c in used] == [c["scene"] for c in cases[:20]]
    # the vectors: recomputed from the fake's own states at L on the held-out scenes 41-60
    hs, es = [], []
    for c in cases[40:60]:
        pos = B.mention_positions(tok, c)
        assert pos is not None
        ids = c["readers"][LK]["ids"]["org"]
        h = fake.run(torch.tensor([ids]), record=(layer,))[1][layer]
        hs.append(h[pos])
        es.append(fake.hf.emb.weight[torch.tensor([ids[p] for p in pos])].detach())
    codes = np.load(out / "codes.npz")
    assert int(codes["n"]) == 20
    assert np.allclose(codes["codes"], (torch.stack(hs) - torch.stack(es)).mean(0).numpy(), atol=1e-5)
    mean_used = X.read_jsonl(out / "mean_cases.jsonl")
    assert {m["scene"] for m in mean_used}.isdisjoint({c["scene"] for c in used})
    # every arm read by both readers; doses matched to the scene's real change
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (c["scene"], w, a) for c in used for w in (LK, RC) for a in B.arm_names(c["slots"]["slot_a"])
    }
    norms = X.read_jsonl(out / "norms.jsonl")
    for r in norms:
        for a, v in r["arm_norms"].items():
            want = r["norm_delta"] if a == "whole" else int(a[-1]) * r["norm_delta"]
            assert v == pytest.approx(want, rel=1e-3, abs=1e-3)
    # one code arm recomputed through the fake's own read
    c0 = used[0]
    k = next(k for k in B.SLOTS if k != c0["slots"]["slot_a"])
    ids = c0["readers"][LK]["ids"]
    hd = [fake.run(torch.tensor([ids[v]]), record=(layer,))[1][layer][c0["pos"]] for v in ("org", "alt")]
    size = float((hd[1] - hd[0]).norm())
    vec = B.dosed(torch.tensor(codes["codes"][k]), 2 * size)
    space = next(c for c in cases if c["scene"] == c0["scene"])["space"]  # cases.jsonl leaves it out, as X0's does
    lg = fake.generate_batch(torch.tensor([ids["org"] + space]), 1, [{layer: AddRows(vec[None].float(), [c0["pos"]])}],
                             first_logits=True)[1]  # fmt: skip
    rec = next(r for r in rows if r["scene"] == c0["scene"] and r["reader"] == LK and r["arm"] == f"code{k}_x2")
    assert rec["top"] == int(lg[0].argmax()) and rec["slot"] == B.lookup_slot(rec["top"], c0["slots"]["tokens"])
    # the verdict recomputes from the rows
    v = B.stage_verdict([run], n_boot=50)
    assert v.name.startswith("x53_bindid-") and v.parent == B.RESULTS
    blob = json.loads((v / "verdict.json").read_text())
    mdl = blob["models"][0]
    pairs = B.pair_rows(rows, used)
    x, y, r_ = (np.mean([p[f"{kind}_x2"] == "X" for p in pairs]) for kind in B.KINDS)
    cell = mdl["cells"]["2"]
    assert cell["X"][0] == pytest.approx(x) and cell["Y"][0] == pytest.approx(y) and cell["R"][0] == pytest.approx(r_)
    assert mdl["status"] == "tested" and mdl["label"] == B.label(float(x - r_), float(x - y))
    md = (v / "verdict.md").read_text()
    assert "UNVERIFIED" in md and "no prediction" in md and B.RULE_VERBATIM in md
    assert B.NOT_DESIGNED in md  # the 27B and Lightning slots
    assert (v / "x53_bindid.png").stat().st_size > 5_000
    assert (v / "examples.md").read_text().count("### C0-") == 10


def test_a_failed_gate_gives_not_tested(fake_env, monkeypatch):
    def recall_misses(model, cases, digits, ws):  # the recall reads O right on 70% of scenes: gate 0.700 < 0.80
        rows = all_right(model, cases, digits, ws)
        for i, r in enumerate(rows):
            if r["reader"] == RC and r["variant"] == "org" and (i // 4) % 10 < 3:
                r["read_right"] = False
        return rows

    monkeypatch.setattr(X, "competence", recall_misses)
    run = fake_env["run"]
    out = B.stage_run(run, "test", n_items=20, n_test=40, n_mean=20)
    gate = json.loads((out / "gate.json").read_text())
    assert not gate["pass"] and gate["org_read_accuracy"][RC] == pytest.approx(0.7)
    assert not (out / "outcomes.jsonl").exists() and not (out / "codes.npz").exists()  # nothing read
    v = B.stage_verdict([run], n_boot=50)
    mdl = json.loads((v / "verdict.json").read_text())["models"][0]
    assert mdl["status"] == "not tested (gate 0.700 < 0.80)" and mdl["label"] is None
    md = (v / "verdict.md").read_text()
    assert "not tested (gate 0.700 < 0.80)" in md and (v / "x53_bindid.png").exists()
