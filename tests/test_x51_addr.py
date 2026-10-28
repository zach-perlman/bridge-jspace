"""Batch 51, test 51.11 (scripts/x51_addr.py): what is the address? The position counterfactual scenes at S slots
(digits kept, the answer fixed across the pair, every locker sentence one token length), the alignment check, d* and
the part 1 / 2 / 3 rules and the part 4 wording on planted numbers, part 2's and part 3's vectors, the seal, and the
run (parts 1, 2, 3; part 2 built without part 1) / verdict / view stages end to end on x49_das_pos's tiny fake causal
model. CPU, no real model."""

from __future__ import annotations

import hashlib
import json
import math
import random
from types import SimpleNamespace

import numpy as np
import pytest
import test_x49_das_pos as T49
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_six as SIX
from scripts import x48_das as D
from scripts import x51_addr as A

LK, RC = X.LOOKUP, X.RECALL
PEOPLE = ["Iris", "Tom", "Ann", "Max", "Eve"]


@pytest.fixture
def words(monkeypatch):
    """The word tokenizer, x49_das_pos's 12 animals, five people, and X0's render as plain text (no chat template)."""
    tok = T49.WordTok()
    monkeypatch.setattr(R, "pools", lambda _tok: (T49.LEGS, sorted(T49.ANIMALS), PEOPLE))
    monkeypatch.setattr(X, "render", lambda _tok, item, _rendering, ctx: f"{ctx} {item['question']} Answer:")
    return tok


# ---- scenes ------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("n", [3, 4, 6, 8])
def test_position_text_swaps_two_locker_sentences_and_keeps_every_digit(n):
    rng = random.Random(n)
    for i, j in SIX.pairs(n):
        t = A.position_text(rng, sorted(T49.ANIMALS), PEOPLE, n, i, j)
        so, ss = SIX.sentences(t["o"]), SIX.sentences(t["s"])
        assert [k for k in range(len(so)) if so[k] != ss[k]] == sorted([i - 1, j - 1])
        assert ss[j - 1] == so[i - 1] == f"The locker of the {t['bridge']} is {t['values'][i - 1]}."  # digit kept
        assert ss[i - 1] == so[j - 1]
        assert t["expect"] == {"identity": t["values"][i - 1], "position": t["values"][j - 1],
                               "value": t["values"][i - 1], "original": t["values"][i - 1]}  # fmt: skip
        assert not SIX.text_checks({**t, "o": t["o"], "s": t["s"]})


def test_candidates_are_aligned_and_every_pair_holds_the_answer(words):
    cases, dropped, lay = A.candidates(words, 4, cap=3)
    assert not dropped and lay["sentence_tokens"] == 7 and lay["layouts_seen"] == 1  # "The locker of the frog is 5."
    assert len(lay["slot_starts"]) == 4 and np.all(np.diff(lay["slot_starts"]) == 7)
    assert sorted({tuple(c["move"]) for c in cases}) == SIX.pairs(4)
    assert all(sum(c["move"] == list(p) for c in cases) == 3 for p in SIX.pairs(4))
    assert A.candidates(words, 4, cap=3)[0] == cases  # seeded per ordered pair
    for c in cases:
        p = A.position_pair(c)
        i, j = c["move"]
        lk = p["readers"][LK]
        assert lk["tok_A"] == lk["tok_s"] and lk["answer"] == lk["s_answer"]  # the answer digit fixed across the pair
        assert lk["cf_answer"] == str(c["values"][j - 1]) and lk["tok_b"] == c["slot_tokens"][j - 1] != lk["tok_A"]
        assert p["readers"][RC]["tok_A"] == p["readers"][RC]["tok_b"]
        assert (p["slot_o"], p["slot_s"], p["move"], p["entity"]) == (i, j, f"{i}->{j}", c["bridge"])
    bad = json.loads(json.dumps(cases[0]))
    bad["readers"][LK]["cf_answer"] = "0"
    with pytest.raises(AssertionError, match="answer digit"):
        A.position_pair(bad)


def test_alignment_rejects_uneven_straddling_or_shifted_sentences():
    ok = {"org": [[3, 4], [5, 6], [7, 8]], "alt": [[3, 4], [5, 6], [7, 8]]}
    assert A.alignment(ok) == ("", (2, (3, 5, 7)))
    assert A.alignment({**ok, "alt": [[3, 4], [5, 6, 7], [8, 9]]})[0] == "the locker sentences differ in token length"
    assert (
        A.alignment({"org": [[3, 4], [4, 5]], "alt": [[3, 4], [4, 5]]})[0] == "a token straddles two locker sentences"
    )
    assert A.alignment({"org": [[3, 4], [5, 6]], "alt": [[3, 4], [6, 7]]})[0] == "O and S lay the slots out differently"


def test_one_entity_split_over_the_pool(words):
    split = A.entity_split(words)
    assert set(split) == set(T49.ANIMALS) and split == D.split_entities(sorted(T49.ANIMALS))
    assert {s: list(split.values()).count(s) for s in ("train", "select", "test")} == {
        "train": 7,
        "select": 2,
        "test": 3,
    }


# ---- rules on planted numbers -------------------------------------------------------------------------------------------


def test_d_star_needs_the_bar_and_the_random_bar_of_the_same_k():
    own = {1: 0.5, 2: 0.85, 3: 0.9, 4: 0.95, 5: 0.95, 7: 0.95}
    rand = {1: 0.0, 2: 0.30, 3: 0.15, 4: 0.0, 5: 0.0, 7: 0.0}
    v = A.d_star(own, rand)
    assert v == {"d_star": 3, "own_only": 2, "random_blocked": [2], "max_k": 7}  # 0.15 is at the bar: it counts
    assert A.d_star({k: 0.79 for k in A.KS}, {k: 0.0 for k in A.KS})["d_star"] is None
    assert A.d_star({k: 0.8 for k in A.KS}, {k: 0.0 for k in A.KS})["d_star"] == 1


@pytest.mark.parametrize(
    ("ds", "label", "holding"),
    [
        ({3: 1, 4: 2, 6: 2, 8: 2}, "ordinal", ["ordinal"]),
        ({3: 1, 4: 2, 6: 4, 8: None}, "one_per_slot", ["one_per_slot"]),  # d*(8) > 7 read as infinity
        ({3: 1, 4: 2, 6: 4, 8: 7}, "one_per_slot", ["one_per_slot"]),
        ({3: 1, 4: 2, 6: 4, 8: 5}, "growing", ["growing"]),  # d*(8) = 5 < S - 2 = 6
        ({3: 2, 4: 3, 6: 3, 8: 4}, "growing", ["growing"]),
        ({3: 1, 4: 5, 6: 2, 8: 3}, "in_between", []),  # not monotone
        ({3: 1, 4: 2, 6: 3, 8: 6}, "in_between", []),  # d*(6) < 4 and d*(8) > 5
    ],
)
def test_part1_rule(ds, label, holding):
    v = A.part1_rule(ds)
    assert v["label"] == label and v["holding"] == holding and v["text"] == A.P1_LABELS[label]


def test_part1_rule_needs_every_s():
    v = A.part1_rule({3: 1, 6: 2})
    assert v["label"] is None and "[4, 8] not tested" in v["text"]


@pytest.mark.parametrize(
    ("reach", "cut", "label"),
    [
        ((1.0, 0.8, 0.7), 0.6, "one_code"),
        ((1.0, 0.6, 0.6), 0.29, "partly"),
        ((1.0, 0.25, 0.9), 0.1, "different"),
        ((1.0, 0.9, 0.29), 0.9, "different"),
        ((1.0, 0.7, 0.7), 0.45, "in_between"),
        ((1.0, 0.5, 0.7), 0.9, "in_between"),
        ((1.0, math.nan, 0.7), 0.9, "in_between"),
    ],
)
def test_part2_rule(reach, cut, label):
    cuts = {f"{x}->{b}": cut for x in A.BASES for b in A.BASES if x != b}
    v = A.part2_rule(dict(zip(A.BASES, reach, strict=True)), cuts)
    assert v["label"] == label


def test_part2_rule_reads_every_cut():
    cuts = {f"{x}->{b}": 0.9 for x in A.BASES for b in A.BASES if x != b}
    cuts["P->R"] = 0.5
    assert A.part2_rule({"U": 1.0, "P": 0.9, "R": 0.9}, cuts)["label"] == "in_between"
    cuts["P->R"] = 0.1
    assert A.part2_rule({"U": 1.0, "P": 0.9, "R": 0.9}, cuts)["label"] == "in_between"


@pytest.mark.parametrize(
    ("mid1", "mid6", "full", "label"),
    [
        (0.3, 0.35, 0.9, "metric"),
        (0.05, 0.09, 0.4, "categories"),
        (0.05, 0.09, 0.39, "none"),
        (0.6, 0.2, 0.9, "first_rest"),
        (0.2, 0.6, 0.9, "none"),
    ],
)
def test_part3_rule(mid1, mid6, full, label):
    assert A.part3_rule({1: mid1, 6: mid6}, full, 6)["label"] == label


def test_mid_class_and_the_ends():
    assert A.ends(6) == {1: (3, 5), 6: (4, 2)}
    assert [A.mid_class(s, 1, 5) for s in (1, 2, 3, 4, 5, 6, None)] == [
        "original", "near", "midpoint", "another slot", "far", "another slot", "not a slot"]  # fmt: skip
    assert [A.mid_class(s, 1, 3) for s in (1, 2, 3)] == ["original", "midpoint", "far"]  # near = midpoint: midpoint
    assert [A.mid_class(s, 6, 2) for s in (6, 5, 4, 2)] == ["original", "near", "midpoint", "far"]


@pytest.mark.parametrize(
    ("labels", "row"),
    [
        (("ordinal", "one_code", "metric"), 1),
        (("one_per_slot", "one_code", "categories"), 2),
        (("growing", "partly", "metric"), 3),
        (("growing", "partly", None), 3),
        ((None, "different", None), 4),  # the 27B: part 2 only
        (("ordinal", "different", "categories"), 4),
        (("ordinal", "one_code", "categories"), None),
        ((None, "one_code", None), None),
    ],
)
def test_wording_row(labels, row):
    w = A.wording(*labels)
    assert w["row"] == row and "four directions" in w["note"]
    if row:
        assert w["text"] == A.WORDING[row - 1][3]


# ---- part 2 and part 3 vectors -------------------------------------------------------------------------------------------


def test_part2_arms_project_remove_and_match_norms():
    torch.manual_seed(0)
    d, n = 16, 4
    mu = torch.randn(n, d)
    u = R.orthonormal((mu - mu.mean(0)).T).float()  # the means span U (rank n - 1)
    assert u.shape == (d, n - 1)
    p = D.random_basis(d, 2, 1)
    r = D.random_basis(d, 2, 2)
    bases = {"U": u, "P": p, "R": r}
    h, hbar = torch.randn(d), torch.randn(d)
    c = {"scene": "P4-12-0001", "move": [2, 4]}
    arms = A.part2_arms(c, n, mu, bases, h, hbar)
    by = {(m["arm"], m["removed"], m["basis"], m["target"]): v for m, v in arms}
    assert by[("none", None, None, None)] is None
    assert len(arms) == 1 + 3 + (n - 1) * 4 * (2 + 3)
    for t in (1, 3, 4):
        step = mu[t - 1] - mu[1]
        assert torch.allclose(by[("swap", None, "whole", t)], 2 * step, atol=1e-5)
        assert torch.allclose(by[("swap", None, "U", t)], 2 * step, atol=1e-4)  # U's projection is the swap itself
        assert torch.allclose(by[("swap", None, "P", t)], 2 * p @ (p.T @ step), atol=1e-5)
        for b in ("whole", *A.BASES):
            v = by[("swap", None, b, t)]
            assert torch.isclose(by[("random", None, b, t)].norm(), v.norm(), atol=1e-4)
            for x in A.BASES:
                after = h + by[("swap", x, b, t)]  # the swapped state with x's coordinates reset to hbar's
                q = bases[x]
                assert torch.allclose(q.T @ after, q.T @ hbar, atol=1e-4)
                assert torch.allclose(after - q @ (q.T @ after), (h + v) - q @ (q.T @ (h + v)), atol=1e-4)
    for x in A.BASES:
        q = bases[x]
        assert torch.allclose(q.T @ (h + by[("remove", x, None, None)]), q.T @ hbar, atol=1e-4)


def test_part3_arms_doses_and_the_4x_midpoint():
    torch.manual_seed(1)
    mu = torch.randn(6, 8)
    for start in (1, 6):
        arms = A.part3_arms({"scene": f"P6-s{start}", "move": [start, 2 if start == 1 else 5]}, 6, mu)
        by = {(m["arm"], m["far"], m["dose"]): v for m, v in arms}
        for far in A.ends(6)[start]:
            half = (mu[far - 1] - mu[start - 1]) / 2
            assert torch.allclose(by[("mid", far, 2)], 2 * half) and torch.allclose(by[("mid", far, 4)], 4 * half)
            assert torch.allclose(by[("full", far, 2)], by[("mid", far, 4)])  # 4x of the half = the full swap at 2x
            for kind, dose in (("mid", 2), ("mid", 4), ("full", 2)):
                assert torch.isclose(by[(f"{kind}_random", far, dose)].norm(), by[(kind, far, dose)].norm(), atol=1e-4)
        assert len(arms) == 1 + 2 * 3 * 2


def test_means_geometry_line_and_simplex():
    line = np.outer(np.arange(6), np.ones(4)).astype(float)
    g = A.means_geometry(line)
    assert g["by_lag_over_lag1"][5] == pytest.approx(5.0) and g["corr_distance_lag"] == pytest.approx(1.0)
    simplex = np.eye(6)
    g = A.means_geometry(simplex)
    assert g["spread"] == pytest.approx(0.0, abs=1e-12) and set(np.round(list(g["by_lag"].values()), 6)) == {
        round(math.sqrt(2), 6)
    }


def test_geometry_readouts_against_random():
    u = D.random_basis(32, 3, 1)
    b = {"U": u, "P": u[:, :2], "R": D.random_basis(32, 2, 5)}
    g = A.geometry_readouts(b, 32)
    assert g["U-P"]["mean_cos2"] == pytest.approx(1.0) and g["ranks"] == {"U": 3, "P": 2, "R": 2}
    assert g["U-P"]["random_expectation"] == pytest.approx(3 / 32) and 0 < g["P-R"]["random_mean"] < 1


# ---- the seal ------------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_q51_11_only(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q51.1** x\n\nDan: yes 60%\n\n**Q51.10** y\n\nDan: (a)\n\n**Q51.11** (51.11) What is the address\n"
              "- Part 1 ...\n- Part 2 ...\n\nDan:{}\n")  # fmt: skip
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert A.dan_answer() == ""
    with pytest.raises(AssertionError, match="sealed"):
        A.unsealed()
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" growing 50%")))
    assert A.dan_answer() == "growing 50%"
    monkeypatch.setattr(
        D.subprocess, "run", fake_git(blocks.format(" 9B growing\nDan (Muse): ordinal\n- Part 2 one code"))
    )
    assert "Dan (Muse): ordinal" in A.dan_answer() and "Part 2 one code" in A.dan_answer()


# ---- the run, verdict and view stages on the fake model ----------------------------------------------------------------


def all_right(model, cases, digits, ws):
    return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "right": True, "read_right": True}
            for c in cases for w in X.READERS for v in ("org", "alt")]  # fmt: skip


def planted_route(top, c):
    """The fake model's top token is never a locker digit: half the scenes (by a hash of the id) planted as position."""
    return "position" if int(hashlib.sha256(c["scene"].encode()).hexdigest(), 16) % 2 == 0 else "identity"


@pytest.fixture
def fake_env(tmp_path, monkeypatch, words):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    fake = T49.FakeModel(words, vocab=1024)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", T49.FakeLens)
    monkeypatch.setattr(X, "competence", all_right)
    monkeypatch.setattr(R, "classify", planted_route)
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x51_addr")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(A, "SPEC", tmp_path / "batch51.yaml")
    A.SPEC.write_text("")
    monkeypatch.setattr(A, "SLOTS", (6, 3))
    monkeypatch.setattr(A, "CAP", {3: 16, 6: 4})
    monkeypatch.setattr(A, "POS_TARGET", 30)
    monkeypatch.setattr(A, "POS_MIN", 20)
    monkeypatch.setattr(A, "GIVE_UP", 4)
    monkeypatch.setattr(A, "KS", (1, 2))
    monkeypatch.setattr(A, "P2_PER_START", {3: 2, 6: 1})
    monkeypatch.setattr(A, "P3_N", 2)
    pre = pins.RUN_PREFIX
    runs = {1: f"{pre}fake_p1", 2: f"{pre}fake_p2", 3: f"{pre}fake_p3"}
    monkeypatch.setattr(A, "RUNS", {pins.TARGET: runs})
    return SimpleNamespace(tok=words, fake=fake, runs=runs, target=pins.TARGET, pre=pre)


def test_parts_end_to_end_on_the_fake_model(fake_env, monkeypatch):
    from bridge_jspace import pins
    from scripts.exp04_brew_parts import AddRows

    la = X.PREDICTED[pins.TARGET]
    p1 = A.stage_run(fake_env.runs[1], 1, "test", steps=2)
    assert not any(p.name.startswith(("verdict", "view")) for p in p1.iterdir())  # sealed
    m = json.loads((p1 / "manifest.json").read_text())
    assert m["part"] == 1 and "sealed" in m and m["failed_slots"] == {} and m["switches"]["target"] == pins.TARGET
    for n in (6, 3):
        d = p1 / f"S{n}"
        assert (d / "done.json").exists()
        info = json.loads((d / "pairs.json").read_text())
        pairs = X.read_jsonl(d / "cases.jsonl")
        reads = {r["scene"]: r for r in X.read_jsonl(d / "reads.jsonl")}
        assert len(pairs) == info["pairs"] >= A.POS_MIN and info["gate"]["pass"]
        assert all(reads[p["scene"]]["route"] == "position" for p in pairs)  # only position-routed pairs
        assert all(p["readers"][LK]["tok_A"] == p["readers"][LK]["tok_s"] for p in pairs)
        split = A.entity_split(fake_env.tok)
        assert all(p["split"] == split[p["entity"]] for p in pairs)
        # U and P on every eligible train-entity scene read (not only the position-routed ones)
        fs = X.read_jsonl(d / "fit_scenes.jsonl")
        assert {f["scene"] for f in fs} == {s for s, r in reads.items() if r["eligible"] and r["split"] == "train"}
        assert any(f["route"] != "position" for f in fs)
        fit = np.load(d / "fit.npz")
        assert fit["U"].shape == (T49.D_MODEL, n - 1) and fit["mu"].shape == (n, T49.D_MODEL)
        assert fit["P"].shape == (T49.D_MODEL, max(A.KS))
        mats = np.load(d / "R.npz")
        assert set(mats.files) == {f"{p}_k{k}" for p in ("R", "shuf", "rand") for k in A.KS}
        rows = X.read_jsonl(d / "outcomes.jsonl")
        held = [p for p in pairs if p["split"] in A.SPLITS_HELD]
        assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
            (p["scene"], w, a) for p in held for w in X.READERS for a in A.arm_names(True)}  # fmt: skip
        # one read recomputed: R at k = 2 added at the bridge of the O prompt
        st = torch.load(d / f"states_L{la}.pt")
        p0 = next(p for p in pairs if p["split"] == "test")
        i0 = st["scenes"].index(p0["scene"])
        r2 = torch.tensor(mats["R_k2"])
        part = ((st["h_S"][i0] - st["h_O"][i0])[None] @ r2) @ r2.T
        ids = p0["readers"][LK]["ids"]["org"] + p0["space"]
        lg = fake_env.fake.generate_batch(
            torch.tensor([ids]), 1, [{la: AddRows(part, [p0["pos"]])}], first_logits=True
        )[1]
        rec = next(r for r in rows if r["scene"] == p0["scene"] and r["reader"] == LK and r["arm"] == "R_k2")
        assert rec["top"] == int(lg[0].argmax())
    # part 2 on part 1's S folders
    p2 = A.stage_run(fake_env.runs[2], 2, "test", part1=fake_env.runs[1], steps=2)
    for n in (6, 3):
        d = p2 / f"S{n}"
        rows = X.read_jsonl(d / "swap_outcomes.jsonl")
        items = X.read_jsonl(d / "swap_items.jsonl")
        assert len(items) == n * A.P2_PER_START[n] and all(it["split"] == "test" for it in items)
        assert {it["move"][0] for it in items} == set(range(1, n + 1))
        per_item = 1 + 3 + (n - 1) * 4 * 5
        assert len(rows) == len(items) * per_item * 2
        ro = json.loads((d / "readouts.json").read_text())
        assert set(ro["geometry"]) >= {"U-P", "U-R", "P-R"} and ro["working"]["k"] in A.KS
    # part 3 on part 1's S = 6
    p3 = A.stage_run(fake_env.runs[3], 3, "test", part1=fake_env.runs[1])
    rows = X.read_jsonl(p3 / "S6" / "p3_outcomes.jsonl")
    items = X.read_jsonl(p3 / "S6" / "p3_items.jsonl")
    assert sorted(it["move"][0] for it in items) == [1, 1, 6, 6] and all(it["split"] in A.SPLITS_HELD for it in items)
    assert all(r["class"] == A.mid_class(r["slot"], r["start"], r["far"]) for r in rows if r["far"] is not None)
    assert len(rows) == len(items) * 13 * 2
    # sealed until Dan's line, then the verdict and the view
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_verdict(n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        A.stage_view(tk=fake_env.tok)
    assert not any(p.name.startswith(("verdict", "view")) for p in A.RESULTS.iterdir())
    monkeypatch.setattr(A, "dan_answer", lambda rev="HEAD": "9B growing")
    v_out = A.stage_verdict(n_boot=50)
    blob = json.loads((v_out / "verdict.json").read_text())
    mv = blob["models"][0]
    assert mv["part1"]["rule"]["label"] is None  # S = 4 and 8 not run here: not decidable
    assert mv["part3"]["rule"]["label"] in A.P3_LABELS and mv["wording"]["row"] is None
    # recomputed from the raw rows: S = 6's own-IIA at k = 2 on the test pairs
    rows6 = [r for r in X.read_jsonl(p1 / "S6" / "outcomes.jsonl") if r["split"] == "test" and r["reader"] == LK]
    own2 = np.mean([r["switched"] for r in rows6 if r["arm"] == "R_k2"])
    assert mv["part1"]["S"]["6"]["curve"]["R"]["2"][0] == pytest.approx(own2)
    md = (v_out / "verdict.md").read_text()
    assert "Part 4" in md and "four directions" in md and (v_out / f"{fake_env.target}_part1.png").exists()
    view = A.stage_view(tk=fake_env.tok)
    text = (view / "view.md").read_text()
    assert "⟦bridge:" in text and "⟦moved:" in text and "random rows of" in text


def test_part2_without_part1_builds_s6_without_shuffled_twins(fake_env):
    p2 = A.stage_run(fake_env.runs[2], 2, "test", steps=2)
    d = p2 / "S6"
    assert (d / "done.json").exists() and not (p2 / "S3").exists()
    assert set(np.load(d / "R.npz").files) == {f"{p}_k{k}" for p in ("R", "rand") for k in A.KS}
    assert (d / "swap_outcomes.jsonl").exists() and (d / "outcomes.jsonl").exists()


def test_a_failing_s_keeps_the_others_and_fails_the_job(fake_env, monkeypatch):
    real = A.build_pairs

    def boom(model, cases, n, *a, **k):
        if n == 3:
            raise torch.cuda.OutOfMemoryError("planted")
        return real(model, cases, n, *a, **k)

    monkeypatch.setattr(A, "build_pairs", boom)
    with pytest.raises(SystemExit, match="S = \\['3'\\] failed"):
        A.stage_run(fake_env.runs[1], 1, "test", steps=1)
    m = json.loads((A.RESULTS / fake_env.runs[1] / "manifest.json").read_text())
    assert set(m["failed_slots"]) == {"3"} and (A.RESULTS / fake_env.runs[1] / "S6" / "done.json").exists()
