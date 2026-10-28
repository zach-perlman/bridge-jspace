"""Batch 51, test 51.1 (scripts/x51_dose.py): the arms (the doses, their random twins, the rest without the address),
49.1's floats for the cells both tests share, every arm end to end on 49.1's tiny fake causal model (CPU), the sealed run
stage, rules (i), (ii), (iii) on planted numbers (the loss bar, the bars inclusive), the logistic fit on planted
coefficients, the verdict and the view on planted runs, and the seal. No real model."""

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x49_gain as G
from scripts import x51_dose as D
from tests.test_x49_gain import D as DIM
from tests.test_x49_gain import FakeLens, FakeModel, L, _item, _orth

LK, RC = X.LOOKUP, X.RECALL


# ---- the arms ------------------------------------------------------------------------------------------------------


def test_arm_names_cover_the_design():
    names = D.arm_names()
    assert len(names) == 2 + 2 * 5 + 2 * 5 + 2 * 5 == len(set(names)) == 32
    assert names[:2] == ["J(0,0)", "J(1,1)"]
    assert {f"J({a:g},0)" for a in D.ALPHAS} | {f"R({a:g},0)" for a in D.ALPHAS} <= set(names)
    assert {"J(3,0)", "R(3,0)", "J(0,0.25)", "R(0,0.25)", "J(0,1.5)-U", "J(0,0.75)-RU"} <= set(names)
    assert D.ALPHAS == (0.5, 1.0, 1.5, 2.0, 3.0) and D.BETAS == (0.25, 0.5, 0.75, 1.0, 1.5)


def test_arm_algebra_and_49_1s_floats():
    g = torch.Generator().manual_seed(0)
    delta, pj, rj, up, ru = (torch.randn(5, DIM, generator=g) for _ in range(5))
    arms = D.arm_deltas(delta, pj, rj, up, ru)
    assert list(arms) == D.arm_names()
    assert not arms["J(0,0)"].any() and torch.allclose(arms["J(1,1)"], delta)
    for a in D.ALPHAS:
        assert torch.allclose(arms[f"J({a:g},0)"], a * pj) and torch.allclose(arms[f"R({a:g},0)"], a * rj)
    for b in D.BETAS:
        assert torch.allclose(arms[f"J(0,{b:g})"], b * (delta - pj))
        assert torch.allclose(arms[f"R(0,{b:g})"], b * (delta - rj))
        assert torch.allclose(arms[D.nou(b)], b * (delta - pj - up))
        assert torch.allclose(arms[D.nou_rand(b)], b * (delta - pj - ru))
    old = G.arm_deltas(delta, pj, rj, up, ru)
    shared = set(old) & set(arms)
    assert {"J(1,1)", "J(0.5,0)", "J(2,0)", "J(0,1.5)", "R(1,0)", "R(0,1)"} <= shared
    assert all(torch.equal(old[a], arms[a]) for a in shared)  # the same floats as 49.1's


def test_dose_cells_are_the_j_arms_with_the_address():
    cells = D.dose_cells(D.arm_names())
    assert (0.0, 0.0, "J(0,0)") in cells and (3.0, 0.0, "J(3,0)") in cells and (0.0, 0.25, "J(0,0.25)") in cells
    assert len(cells) == 2 + 5 + 5 and not any("U" in n or n.startswith("R") for *_, n in cells)


# ---- end to end on the fake model ----------------------------------------------------------------------------------


@pytest.fixture
def fake_items():
    model = FakeModel()
    items = [_item(i) for i in range(12)]
    u = _orth(DIM, 4, 3)
    rows, norms, losses, greedy = D.run_items(model, FakeLens(), items, L, torch.arange(10), u)
    return SimpleNamespace(model=model, items=items, u=u, rows=rows, norms=norms, losses=losses, greedy=greedy)


def test_run_items_reads_every_arm_on_o(fake_items):
    f, names = fake_items, D.arm_names()
    assert {(r["scene"], r["reader"], r["arm"]) for r in f.rows} == {
        (c["scene"], w, a) for c in f.items for w in X.READERS for a in names
    }
    assert len(f.rows) == 12 * 2 * len(names) and len(f.losses) == 12 * len(names)
    assert len(f.greedy) == X.K_EXAMPLES * 2 * len(names) and len(f.norms) == 12
    prompt, edits = f.model.calls[0]
    it = f.items[0]
    assert prompt == it["readers"][LK]["ids"]["org"] + it["space"] and len(edits) == len(names)
    assert all(list(e) == [L] and e[L].positions == [it["pos"]] for e in edits)


def test_the_arms_add_the_parts_at_their_doses(fake_items):
    f, names = fake_items, D.arm_names()
    it = f.items[0]
    ids = it["readers"][LK]["ids"]
    h = {v: f.model.run(torch.tensor([ids[v]]), record=(L,))[1][L][it["pos"]] for v in ("org", "alt")}
    delta = h["alt"] - h["org"]
    edits = dict(zip(names, f.model.calls[0][1], strict=True))
    pj = X.fit(FakeLens().vectors(L, torch.arange(100)), delta[None], 25, "signed")[0]
    up = delta @ f.u.float() @ f.u.float().T
    assert torch.allclose(edits["J(1,1)"][L].delta[0], delta, atol=1e-5)
    assert torch.allclose(edits["J(3,0)"][L].delta[0], 3 * pj, atol=1e-4)
    assert torch.allclose(edits["J(0,0.25)"][L].delta[0], 0.25 * (delta - pj), atol=1e-4)
    assert torch.allclose(edits["J(0,1.5)-U"][L].delta[0], 1.5 * (delta - pj - up), atol=1e-4)
    assert not edits["J(0,0)"][L].delta.any()
    # the loss: O's own next token at the bridge word, the prompt cut after it, every arm
    prompt, ledits = next(c for c in f.model.calls if c[0] == ids["org"][: it["pos"] + 1])
    mine = {r["arm"]: r for r in f.losses if r["scene"] == it["scene"]}
    for a, e in zip(names, ledits, strict=True):
        want = -torch.log_softmax(f.model.forward(prompt, e)[0], -1)[ids["org"][it["pos"] + 1]]
        assert mine[a]["loss"] == pytest.approx(float(want), abs=1e-4)


def _stage(monkeypatch, tmp_path, items, gate_pass=True):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins

    monkeypatch.setattr(M, "load_model", lambda: FakeModel())
    monkeypatch.setattr(LN, "JLens", FakeLens)
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x51_dose")
    monkeypatch.setattr(G, "RESULTS", tmp_path / "x49_gain")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(D, "SPEC", tmp_path / "batch51.yaml")
    D.SPEC.write_text("")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(
        G, "pointer_basis", lambda t: (_orth(DIM, 4, 3).double().numpy(), {"states_run": "fake", "rank": 4})
    )
    monkeypatch.setattr(G, "select_items", lambda tok, t: (items, {"items_in_group": len(items)}))
    src = X.RESULTS / G.SOURCES[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    (src / "gate.json").write_text(json.dumps({"gate": {"chat": {"pass": gate_pass, "enough": True}}}))


def test_stage_run_end_to_end_sealed(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, [_item(i) for i in range(12)])
    out = D.stage_run(f"{pins.RUN_PREFIX}x51_test", "test")
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "51.1" and m["arms"] == D.arm_names() and "sealed" in m and "switches" in m
    assert m["alphas"] == list(D.ALPHAS) and m["betas"] == list(D.BETAS) and m["x49_run"] == G.RUNS[pins.TARGET]
    assert sorted(p.name for p in out.iterdir()) == ["cases.jsonl", "examples_greedy.jsonl", "gate.json", "losses.jsonl",
                                                     "manifest.json", "norms.jsonl", "outcomes.jsonl", "plan.json"]  # fmt: skip
    assert len(X.read_jsonl(out / "outcomes.jsonl")) == 12 * 2 * 32 and not list(out.glob("verdict*"))


def test_stage_run_without_the_gate_writes_no_outcomes(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, [_item(0)], gate_pass=False)
    out = D.stage_run(f"{pins.RUN_PREFIX}x51_test_gate", "test")
    assert not (out / "outcomes.jsonl").exists() and json.loads((out / "gate.json").read_text())["tested"] is False


# ---- the rules on planted numbers ----------------------------------------------------------------------------------


def _under(over: tuple[str, ...] = ()) -> dict[str, bool]:
    return {a: a not in over for a in D.arm_names()}


def test_rule_i_blind_at_every_alpha_under_the_bar():
    lk = {a: 0.0 for a in D.arm_names()} | {"J(1,0)": 0.15, "R(1,0)": 0.05, "J(3,0)": 0.6, "R(3,0)": 0.0}
    assert D.rule_blind(lk, _under(("J(3,0)",)))["label"] == "yes"  # 0.10 at the bar counts; J(3,0) above the bar
    assert D.rule_blind(lk, _under())["label"] == "no"  # J(3,0) under the bar: 0.6 over its twin
    assert D.rule_blind(lk | {"J(1,0)": 0.16}, _under(("J(3,0)",)))["alphas_failing"] == [1.0]
    none = D.rule_blind(lk, _under(tuple(f"J({a:g},0)" for a in D.ALPHAS)))
    assert none["label"] == "undecided" and none["alphas_under_bar"] == []


def test_rule_ii_at_the_first_alpha_reaching_point_three():
    rc = {a: 0.0 for a in D.arm_names()} | {"J(0.5,0)": 0.2, "J(1,0)": 0.3, "R(1,0)": 0.1, "J(1.5,0)": 0.9}
    r = D.rule_above(rc, _under())
    assert r["label"] == "yes" and r["first_alpha"] == 1.0 and r["first_under_bar"]  # 0.3 - 0.1 = 0.2 at the bar
    assert D.rule_above(rc | {"R(1,0)": 0.11}, _under())["label"] == "no"  # the later, larger gap does not count
    never = D.rule_above({a: 0.29 for a in D.arm_names()}, _under())
    assert never["label"] == "no" and never["first_alpha"] is None


def test_rule_iii_together_only():
    x = {a: 0.0 for a in D.arm_names()} | {"J(2,0)": 0.3, "J(0,1)": 0.25, "J(0,1.5)": 0.9, "J(0,1.5)-U": 0.9}
    over = ("J(0,1.5)",)
    r = D.rule_together(x, _under(over), 0.8)
    assert r["label"] == "yes" and r["best_single"] == ["J(2,0)", 0.3]  # J(0,1.5) above the bar; -U arms not singles
    assert D.rule_together(x, _under(), 0.8)["label"] == "no"
    assert D.rule_together(x, _under(over), 0.79)["label"] == "no"
    assert D.rule_together(x, _under(over), None)["label"] == "undecided"


# ---- the fit -------------------------------------------------------------------------------------------------------


def _sim(coef: list[float], n_ent: int = 40, per: int = 3, seed: int = 0):
    """Planted per-item switches on the 5x5 grid from logit = coef[0] + coef[1] α + coef[2] β (+ coef[3] α β)."""
    rng = np.random.default_rng(seed)
    entities = [f"e{i}" for i in range(n_ent) for _ in range(per)]
    c = [*coef, 0.0][:4]
    cells = {}
    for a in (0.0, 0.5, 1.0, 1.5, 2.0):
        for b in (0.0, 0.5, 1.0, 1.5, 2.0):
            eta = c[0] + c[1] * a + c[2] * b + c[3] * a * b
            cells[(a, b)] = list((rng.random(len(entities)) < 1 / (1 + np.exp(-eta))).astype(int))
    return cells, entities


def test_fit_recovers_planted_coefficients_and_finds_c_only_when_planted():
    add = D.logistic_fit(*_sim([-2.0, 1.0, 2.0], n_ent=200), n_boot=200)
    assert add["additive"]["a"][0] == pytest.approx(1.0, abs=0.25) and add["additive"]["b"][0] == pytest.approx(
        2.0, abs=0.3
    )
    assert add["b_over_a"][0] == pytest.approx(2.0, abs=0.6) and not add["c_needed"]
    inter = D.logistic_fit(*_sim([-2.0, 0.5, 0.5, 1.5], n_ent=200), n_boot=200)
    assert inter["interaction"]["c"][0] == pytest.approx(1.5, abs=0.4) and inter["c_needed"]
    assert inter["lr_naive"]["stat"] > 10 and inter["lr_naive"]["p"] < 0.01


def test_fit_stays_finite_when_a_reader_never_switches_along_an_axis():
    cells, ents = _sim([-2.0, 0.0, 2.0], n_ent=30)
    cells = {k: (v if k[0] == 0 else [0] * len(v)) for k, v in cells.items()}  # α > 0: nothing switches
    f = D.logistic_fit(cells, ents, n_boot=50)
    assert all(np.isfinite(f["interaction"][k][0]) for k in ("a0", "a", "b", "c")) and f["additive"]["a"][0] < 0


def test_irls_weights_are_row_multiplicities():
    design = np.stack([np.ones(4), np.arange(4.0)], 1)
    s, t = np.array([0.0, 1.0, 1.0, 2.0]), np.array([2.0, 2.0, 2.0, 2.0])
    twice = D.irls(design, s, t, np.full((1, 4), 2.0), ridge=0.0)[0]
    doubled = D.irls(design, 2 * s, 2 * t, np.ones((1, 4)), ridge=0.0)[0]
    assert np.allclose(twice, doubled, atol=1e-6)


# ---- planted runs: the verdict, the view, the seal -----------------------------------------------------------------


def planted_rates(kind: str) -> dict[str, dict[str, float]]:
    """Per reader, every arm's planted rate (51.1's arms and 49.1's grid, which share J(1,1) and the doses)."""
    names = set(D.arm_names()) | set(G.arm_names(True))
    lk, rc = {a: 0.0 for a in names}, {a: 0.0 for a in names}
    for a in names:
        if a.startswith(("J(0,", "R(0,")) and not a.endswith(",0)"):
            b = float(a.split(",")[1].split(")")[0])
            lk[a] = min(1.0, 0.6 * b)
            rc[a] = min(1.0, 0.2 * b) if kind == "together" else min(1.0, 0.5 * b)
    rc |= {"J(0.5,0)": 0.1, "J(1,0)": 0.3, "R(1,0)": 0.05, "J(1.5,0)": 0.5, "J(2,0)": 0.7, "J(3,0)": 0.9}
    lk |= {"J(3,0)": 0.5}  # above the loss bar (planted loss 3.0): (i) holds anyway
    if kind == "together":
        rc |= {"J(0.5,0)": 0.1, "J(1,0)": 0.1, "J(1.5,0)": 0.2, "J(2,0)": 0.25, "J(3,0)": 0.25}  # (ii): never 0.3
    lk["J(1,1)"], rc["J(1,1)"] = 0.95, 0.9
    return {LK: lk, RC: rc}


def write_planted(root, run: str, target: str, kind: str, names: list[str], n: int = 60, tested: bool = True):
    src = root / run
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": X.PREDICTED[target],
                                                   "x49_run": G.RUNS[target], "wide": False,
                                                   "pointer": {"rank": 4, "states_run": "fake"}}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"tested": tested, "gate": {"pass": tested}}))
    if not tested:
        return
    pts = planted_rates(kind)
    rows, losses, cases, norms = [], [], [], []
    for i in range(n):
        it = _item(i)
        ent = f"e{i % 10}"
        cases.append({**it, "entity": ent})
        norms.append({"scene": it["scene"], "entity": ent, "norm_delta": 1.0, "share_J": 0.1})
        for w in X.READERS:
            for a in names:
                s = int(i < round(pts[w][a] * n))
                rows.append({"scene": it["scene"], "entity": ent, "domain": "animals", "reader": w, "arm": a,
                             "switched": s, "top": 3 if s else 5, "role": "b" if s else "A"})  # fmt: skip
        losses += [{"scene": it["scene"], "entity": ent, "arm": a, "next": 6, "loss": 3.0 if a == "J(3,0)" else 1.0,
                    "top_is_next": 1} for a in names]  # fmt: skip
    for f, data in (("outcomes", rows), ("losses", losses), ("cases", cases), ("norms", norms),
                    ("examples_greedy", [])):  # fmt: skip
        X.write_jsonl(src / f"{f}.jsonl", data)


def planted(root, mp, kinds: dict[str, str | None], answer: str = "planted"):
    mp.setattr(D, "RESULTS", root / "x51_dose")
    mp.setattr(G, "RESULTS", root / "x49_gain")
    mp.setattr(D, "dan_answer", lambda rev="HEAD": answer)
    for target, kind in kinds.items():
        write_planted(D.RESULTS, D.RUNS[target], target, kind or "split", D.arm_names(), tested=kind is not None)
        if kind is not None:
            write_planted(G.RESULTS, G.RUNS[target], target, kind, G.arm_names(False))


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, {"qwen3.5-9b": "split", "qwen3.6-27b": None, "muse-glimmer-30b": "together"})
    out = D.stage_verdict(n_boot=50)
    blob = json.loads((out / "verdict.json").read_text())
    s = blob["summary"]
    assert s["i"] == {"qwen3.5-9b": "yes", "qwen3.6-27b": "not tested", "muse-glimmer-30b": "yes"}
    assert s["ii"]["qwen3.5-9b"] == "yes" and s["ii"]["muse-glimmer-30b"] == "no" and s["iii_muse"] == "yes"
    assert s["i_all_three"] == "undecided"
    m = {x["target"]: x for x in blob["models"]}
    nine = m["qwen3.5-9b"]
    assert nine["rules"]["i"]["alphas_under_bar"] == [0.5, 1.0, 1.5, 2.0] and not nine["loss"]["under_bar"]["J(3,0)"]
    assert nine["rules"]["ii"]["recall"]["first_alpha"] == 1.0
    assert nine["readers"]["recall"]["diff"]["J(1,0) - R(1,0)"][0] == pytest.approx(0.25)
    assert nine["x49"]["recall"]["whole"] == pytest.approx(0.9) and nine["x49"]["recall"]["whole_agree"] == [60, 60]
    assert "16 of 49.1's grid cells" in nine["fit"]["recall"]["source"] and nine["fit"]["recall"]["cells"] == 12 + 16
    assert m["muse-glimmer-30b"]["rules"]["iii"]["recall"]["best_single"][1] <= 0.3
    md = (out / "verdict.md").read_text()
    assert "Dan: planted" in md and "on all three: **undecided**" in md and "| J(3,0) |" in md
    assert (out / "dose_curves.png").stat().st_size > 0


def test_without_49_1_the_fit_uses_this_run_and_iii_is_undecided(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, {"muse-glimmer-30b": "together"})
    for p in (G.RESULTS / G.RUNS["muse-glimmer-30b"]).iterdir():
        p.unlink()
    m = D.model_result("muse-glimmer-30b", D.RUNS["muse-glimmer-30b"], n_boot=20)
    assert m["rules"]["iii"]["recall"]["label"] == "undecided" and m["fit"]["recall"]["source"] == "this run's J cells"


def test_view_writes_prompts_and_rows_per_arm(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, {"qwen3.5-9b": "split"})
    out = D.stage_view(decode_for=lambda t: lambda ids: "".join(f"<{int(i)}>" for i in ids))
    text = (out / "view.md").read_text()
    assert text.count("#### P2-") == D.N_PROMPTS and text.count("```") == D.N_PROMPTS * 3 * 2
    assert all(f"### {a}: {D.N_ROWS} random rows of 120 (seed 0)" in text for a in D.arm_names())
    assert "qwen3.6-27b: x51_1_27b not here or not tested" in text


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    planted(tmp_path, monkeypatch, {"qwen3.5-9b": "split"}, answer="")
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_verdict(n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_view()
    assert sorted(p.name for p in D.RESULTS.iterdir()) == [D.RUNS["qwen3.5-9b"]]


def test_dan_answer_reads_only_the_q51_1_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q49.1** x\n\nDan: (a) 60%\n\n**Q51.1** (51.1) Dose curves ...\n- (i) The lookup is blind ...\n"
              "- (ii) The recall ...\n\nDan:{}\n\n**Q51.2** (51.2) heads\n\nDan: (a)\n")  # fmt: skip
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert D.dan_answer() == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" (i) 9B 70%")))
    assert D.dan_answer() == "(i) 9B 70%"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("\nDan (27B): (i) 60%\n- (iii) no")))
    assert "Dan (27B): (i) 60%" in D.dan_answer() and "- (iii) no" in D.dan_answer()


def test_the_committed_predictions_file_has_the_q51_1_block():
    text = D.subprocess.run(["git", "show", f"HEAD:{D.PREDICTIONS}"], cwd=D.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{D.QUESTION}**" in text and isinstance(D.dan_answer(), str)


def test_run_names_pass_the_prefix_check():
    from bridge_jspace import pins

    assert D.RUNS[pins.TARGET].startswith(pins.RUN_PREFIX)
