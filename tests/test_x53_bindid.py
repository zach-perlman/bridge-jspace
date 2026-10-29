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


def test_rule_and_the_centered_arm_are_dans_text_verbatim():
    spec = yaml.safe_load(B.SPEC.read_text())
    norm = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
    assert norm(B.RULE_VERBATIM) in norm(spec["critic_1125"])
    assert norm(B.CENTERED_VERBATIM) in norm(spec["decisions_1210b"])
    assert B.HEADLINE == "uncentered" and B.VARIANTS == {"uncentered": "code", "centered": "ccode"}


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


def planted_codes(d: int = 32, common: float = 150.0, seed: int = 0):
    """Slot vectors = one large component shared by every slot + a small slot-specific part (the parts sum to zero)."""
    g = torch.Generator().manual_seed(seed)
    shared = torch.randn(d, generator=g)
    shared = common * shared / shared.norm()
    parts = torch.randn(3, d, generator=g) * torch.tensor([[1.0], [2.0], [3.0]])
    parts = parts - parts.mean(0)
    return shared[None] + parts, parts


def test_centered_codes_are_the_slot_specific_parts_on_planted_data():
    codes, parts = planted_codes()
    cc = B.centered(codes)
    assert torch.allclose(cc, parts, atol=1e-5) and torch.allclose(cc.sum(0), torch.zeros(32), atol=1e-4)
    assert torch.allclose(B.centered(cc), cc, atol=1e-5)  # centering twice changes nothing
    assert np.allclose(B.centered(codes.numpy()), parts.numpy(), atol=1e-5)  # numpy too (the verdict's geometry)
    g = B.geometry(codes.numpy(), None)
    norm, spec = [float(c.norm()) for c in codes], [float(p.norm()) for p in parts]
    assert g["norm"] == pytest.approx(norm, abs=1e-3) and g["slot_specific_norm"] == pytest.approx(spec, abs=1e-3)
    assert g["slot_specific_share"] == pytest.approx([s / n for s, n in zip(spec, norm, strict=True)], abs=1e-4)
    assert min(g["cos"].values()) > 0.9  # the shared component dominates the raw slot vectors
    cos = lambda a, b: float(a @ b / (a.norm() * b.norm()))  # noqa: E731
    assert g["cos_centered"]["0-1"] == pytest.approx(cos(parts[0], parts[1]), abs=1e-4)
    assert min(g["cos_centered"].values()) < 0  # parts summing to zero: their pairwise dot products sum below zero
    mu = {k: np.random.default_rng(k).normal(size=32) for k in range(5)}
    gm = B.geometry(codes.numpy(), mu)
    want = cos((codes[2] - codes[0]).double(), torch.tensor(mu[2] - mu[0], dtype=torch.float64))
    assert gm["cos_diff_vs_pointer_means"]["0-2"] == pytest.approx(want, abs=1e-4)


@pytest.mark.parametrize("slot_a", [0, 1, 2])
def test_doses_match_the_real_change_and_controls_have_equal_norms(slot_a):
    g = torch.Generator().manual_seed(slot_a)
    codes = torch.randn(3, 32, generator=g) * torch.tensor([[50.0], [3.0], [0.2]])  # very different raw norms
    rand = torch.randn(32, generator=g) * 7
    delta = torch.randn(32, generator=g)
    size = float(delta.norm())
    v = B.arm_vectors(codes, rand, slot_a, size, delta)
    assert list(v) == B.arm_names(slot_a)[1:] and B.arm_names(slot_a)[0] == "none"
    assert len(v) == 1 + len(B.DOSES) * 5  # whole; per dose 2 codes, random, 2 centered codes
    assert torch.equal(v["whole"], delta)
    others = [k for k in B.SLOTS if k != slot_a]
    assert not {f"{p}{slot_a}_x{d}" for p in ("code", "ccode") for d in B.DOSES} & set(v)  # never A's own slot
    cc = B.centered(codes)
    for d in B.DOSES:
        for prefix in ("code", "ccode"):  # X's vector, Y's version (the other slot's) and random: one norm, d ||Δ||
            arms = [f"{prefix}{k}_x{d}" for k in others] + [f"rand_x{d}"]
            for a in arms:
                assert float(v[a].norm()) == pytest.approx(d * size, rel=1e-5)
        for k in others:  # the directions: the slot's vector, raw and centered
            assert torch.allclose(v[f"code{k}_x{d}"] / v[f"code{k}_x{d}"].norm(), codes[k] / codes[k].norm(), atol=1e-6)
            assert torch.allclose(v[f"ccode{k}_x{d}"] / v[f"ccode{k}_x{d}"].norm(), cc[k] / cc[k].norm(), atol=1e-6)
        assert torch.allclose(v[f"rand_x{d}"] / v[f"rand_x{d}"].norm(), rand / rand.norm(), atol=1e-6)
    assert torch.allclose(v[f"code{others[0]}_x2"], 2 * v[f"code{others[0]}_x1"], atol=1e-5)
    assert torch.allclose(v[f"ccode{others[0]}_x2"], 2 * v[f"ccode{others[0]}_x1"], atol=1e-5)


def test_centered_arm_on_planted_codes_has_its_own_direction_at_the_same_norm():
    """The planted case the centered arm exists for: raw slot vectors nearly parallel (cos > 0.9), so the raw X and Y
    arms nearly coincide, while the centered arms point along the slot-specific parts alone; the centered X, Y's
    centered version and the random control all at X's dosed norm."""
    codes, parts = planted_codes()
    rand, delta = torch.ones(32), torch.full((32,), 0.5)
    size = float(delta.norm())
    v = B.arm_vectors(codes, rand, 0, size, delta)
    cos = lambda a, b: float(a @ b / (a.norm() * b.norm()))  # noqa: E731
    assert cos(v["code1_x2"], v["code2_x2"]) > 0.9
    for k in (1, 2):
        assert cos(v[f"ccode{k}_x2"], parts[k]) == pytest.approx(1.0, abs=1e-5)
    assert cos(v["ccode1_x2"], v["ccode2_x2"]) == pytest.approx(cos(parts[1], parts[2]), abs=1e-5)
    norms = {a: float(v[a].norm()) for a in ("ccode1_x2", "ccode2_x2", "rand_x2")}
    assert max(norms.values()) - min(norms.values()) < 1e-4 and norms["rand_x2"] == pytest.approx(2 * size, rel=1e-5)


# ---- reads, pairs, the rule ----------------------------------------------------------------------------------------


def planted(n_scenes: int, p_hit: float, seed: int = 0, p_centered: float = 0.0) -> tuple[list[dict], list[dict]]:
    """Cases with slots and lookup rows where, at every dose, each slot's vector sends the lookup to that slot's locker
    with probability p_hit and otherwise leaves it on A's; the random vector always leaves it on A's. So X's share
    under X's vector is about p_hit, under Y's version and random 0, and Y's version sends to Y's locker as often.
    The centered vectors: the same with p_centered, except that they send the lookup to the OTHER non-A slot (so the
    centered arm's X share is 0 while Y's centered version sends to X's locker)."""
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
            for x in others:
                (y,) = [k for k in others if k != x]
                lk[f"ccode{x}_x{d}"] = y if rng.random() < p_centered else a
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
    assert col["ccode_x2"]["n"] == 120 and col["ccode_x2"]["lookup"][0] == 1  # p_centered 0: A's locker kept


def test_the_centered_arm_is_paired_on_its_own_vectors_with_the_same_random_control():
    cases, rows = planted(60, 0.7, p_centered=0.6)
    lk = {(r["scene"], r["arm"]): r["slot"] for r in rows if r["reader"] == LK}
    raw, cen = B.pair_rows(rows, cases, "code"), B.pair_rows(rows, cases, "ccode")
    assert [(p["scene"], p["x"]) for p in raw] == [(p["scene"], p["x"]) for p in cen]
    for p, q in zip(raw, cen, strict=True):
        for d in B.DOSES:
            assert p[f"R_x{d}"] == q[f"R_x{d}"]  # one random arm, the same norm as both constructions' vectors
            assert (q[f"X_x{d}"] == "X") == (lk[(q["scene"], f"ccode{q['x']}_x{d}")] == q["x"])
            assert (q[f"Y_x{d}"] == "X") == (lk[(q["scene"], f"ccode{q['y']}_x{d}")] == q["x"])
    vr, vc = B.variant_numbers(raw, n_boot=100), B.variant_numbers(cen, n_boot=100)
    y = np.mean([lk[(q["scene"], f"ccode{q['y']}_x2")] == q["x"] for q in cen])
    assert vc["cells"]["2"]["X"][0] == 0 and vc["cells"]["2"]["Y"][0] == pytest.approx(y)
    assert vc["label"] == "no" and vc["label"] == B.label(0.0, -y)
    xr = vr["cells"]["2"]["X"][0]
    assert vr["label"] == B.label(xr, xr) == "shared"  # X 0.7-ish, Y and random 0
    assert set(vr["per_slot"]) == {"0", "1", "2"} and sum(s["n"] for s in vr["per_slot"].values()) == len(raw)


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
    # one code arm and one centered arm recomputed through the fake's own read
    c0 = used[0]
    k = next(k for k in B.SLOTS if k != c0["slots"]["slot_a"])
    ids = c0["readers"][LK]["ids"]
    hd = [fake.run(torch.tensor([ids[v]]), record=(layer,))[1][layer][c0["pos"]] for v in ("org", "alt")]
    size = float((hd[1] - hd[0]).norm())
    space = next(c for c in cases if c["scene"] == c0["scene"])["space"]  # cases.jsonl leaves it out, as X0's does
    cc = torch.tensor(codes["codes"]) - torch.tensor(codes["codes"]).mean(0)
    for arm, raw in ((f"code{k}_x2", torch.tensor(codes["codes"][k])), (f"ccode{k}_x2", cc[k])):
        vec = B.dosed(raw, 2 * size)
        lg = fake.generate_batch(torch.tensor([ids["org"] + space]), 1,
                                 [{layer: AddRows(vec[None].float(), [c0["pos"]])}], first_logits=True)[1]  # fmt: skip
        rec = next(r for r in rows if r["scene"] == c0["scene"] and r["reader"] == LK and r["arm"] == arm)
        assert rec["top"] == int(lg[0].argmax()) and rec["slot"] == B.lookup_slot(rec["top"], c0["slots"]["tokens"])
    # the verdict recomputes from the rows: the headline from the uncentered arm, the centered arm's label beside
    v = B.stage_verdict([run], n_boot=50)
    assert v.name.startswith("x53_bindid-") and v.parent == B.RESULTS
    blob = json.loads((v / "verdict.json").read_text())
    mdl = blob["models"][0]
    assert mdl["status"] == "tested" and mdl["headline"] == "uncentered" and set(mdl["variants"]) == set(B.VARIANTS)
    for var, prefix in B.VARIANTS.items():
        pairs = B.pair_rows(rows, used, prefix)
        x, y, r_ = (np.mean([p[f"{kind}_x2"] == "X" for p in pairs]) for kind in B.KINDS)
        cell = mdl["variants"][var]["cells"]["2"]
        assert (
            cell["X"][0] == pytest.approx(x) and cell["Y"][0] == pytest.approx(y) and cell["R"][0] == pytest.approx(r_)
        )
        assert mdl["variants"][var]["label"] == B.label(float(x - r_), float(x - y))
    assert mdl["label"] == mdl["variants"]["uncentered"]["label"]
    g = mdl["geometry"]
    assert (
        g["slot_specific_norm"] == pytest.approx([float(c.norm()) for c in cc], abs=1e-3)
        and len(g["cos_centered"]) == 3
    )
    md = (v / "verdict.md").read_text()
    assert "UNVERIFIED" in md and "no prediction" in md and B.RULE_VERBATIM in md and B.CENTERED_VERBATIM in md
    assert "label (uncentered)" in md and "label (centered)" in md and "norm of the slot-specific part" in md
    assert md.index("label (uncentered)") < md.index("label (centered)")  # the headline first
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
