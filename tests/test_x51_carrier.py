"""Batch 51, 51.7 (scripts/x51_carrier.py): Z1's items rebuilt as stored, the before-L arms' values and edits, the full
swap reproducing S, the rules on planted numbers, the seal, and the run stage end to end on a tiny fake model (CPU).
No real model; no Z1 outcome is printed."""

import json
from types import SimpleNamespace

import pytest

from scripts import x0_necessity as X
from scripts import x50_zach as Z
from scripts import x51_carrier as C
from tests.test_x47_cue import FakeLens, FakeModel


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


@pytest.fixture(scope="module")
def built(tok):
    from bridge_jspace import pins

    if pins.TARGET not in C.RUNS or not (C.z1_dir(pins.TARGET) / "gate.json").exists():
        pytest.skip("Z1's run for this target is not here")
    return C.z1_items(tok, pins.TARGET)


# ---- items ----------------------------------------------------------------------------------------------------------


def test_z1_items_rebuild_z1s_stored_cases_with_their_windows(tok, built):
    items, bad = built
    assert bad == [] and len(items) == 200
    assert {c["stratum"] for c in items} == set(C.STRATA)
    for c in items:
        rd = c["readers"][C.LOOKUP]
        org, alt, pos = rd["ids"]["org"], rd["ids"]["alt"], rd["pos"]
        assert pos in c["window"] and c["window"] == sorted(c["window"])
        assert all(org[q] == alt[q] for q in c["window"] if q != pos)
        for role in ("bridge", "cf_bridge"):
            text = tok.decode([org[q] for q in c["fact_pos"][role]])
            assert c[role].split()[-1] in text and Z.fact(c["relation"], c[role]) in text
        assert all(c["n_changed"][w] >= 1 for w in C.READERS)
        if c["stratum"] == "fact-after":
            assert min(c["fact_pos"]["bridge"]) > pos
        else:
            assert max(c["fact_pos"]["bridge"]) < pos
    keys = C.window_keys(items)
    after = [(c["set"], c["scene"]) for c in items if c["stratum"] == "fact-after"]
    assert len(keys) == C.N_WINDOW and keys == after[: C.N_WINDOW]


def test_mismatch_names_what_differs():
    rd = {"pos": 3, "tok_A": 1, "tok_b": 2, "tok_lure": None, "ids": {"org": [1, 2, 3, 4], "alt": [1, 2, 5, 4]}}
    case = {
        "cf_bridge": "x",
        "stratum": "fact-first",
        "answer": "A",
        "cf_answer": "B",
        "readers": {w: rd for w in C.READERS},
    }
    assert C.mismatch(case, json.loads(json.dumps(case))) == ""
    assert C.mismatch(None, case) == "not rebuilt" and C.mismatch(case, None) == "not stored"
    other = json.loads(json.dumps(case))
    other["readers"]["M"]["ids"]["alt"][2] = 9
    assert C.mismatch(case, other) == "M ids"
    assert C.mismatch(case, {**case, "stratum": "fact-after"}) == "stratum"


# ---- the arms' values and edits ---------------------------------------------------------------------------------------


def parts(n=6, d=32, seed=0):
    import torch

    from scripts import statement_positions as SP

    g = torch.Generator().manual_seed(seed)
    jdic = torch.nn.functional.normalize(torch.randn(64, d, generator=g), dim=-1)
    h_s, h_o = torch.randn(n, d, generator=g), torch.randn(n, d, generator=g)
    basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED))
    return jdic, h_s, h_o, basis


def test_layer_values_are_h_s_minus_each_part_and_z1s_one_layer_vectors():
    import torch

    from scripts import x6_routes as R

    jdic, h_s, h_o, basis = parts()
    sets, one, share = C.layer_values(jdic, h_s, h_o, basis)
    x = h_s - h_o
    fit = X.fit(jdic, x, X.K_MAIN, "signed")
    z1, sh = R.removal_arms(x, {"jpp": fit}, basis)  # Z1's arms, as x50_zach computes them
    assert torch.equal(sets["whole_bL"], h_s) and torch.allclose(sets["no_jpp_bL"], h_s - fit)
    assert torch.allclose(one["whole_1L"], x) and torch.equal(one["no_jpp_1L"], z1["no_jpp"])
    assert torch.equal(one["rand_1L"], z1["no_jpp_rand"]) and torch.equal(share, sh["jpp"])
    # at L the before-L states are Z1's one-layer states (h_O + its vector)
    for b, o in (("whole_bL", "whole_1L"), ("no_jpp_bL", "no_jpp_1L"), ("rand_bL", "rand_1L")):
        assert torch.allclose(sets[b], h_o + one[o], atol=1e-5)
    # the random part removed has the J++ part's share of ||Delta||^2 (to within one basis direction)
    rand_share = (h_s - sets["rand_bL"]).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2
    assert torch.all((rand_share - share).abs() < 0.08)


def test_edit_sets_place_each_arm_at_its_blocks():
    import torch

    from scripts.exp04_brew_parts import AddRows, SetRows

    L, pos, d = 4, 2, 8
    sets_i = {a: {la: torch.full((d,), float(10 * i + la)) for la in range(L + 1)} for i, a in enumerate(C.BEFORE)}
    one_i = {a: torch.full((d,), float(-i - 1)) for i, a in enumerate(C.ONE)}
    es = C.edit_sets(sets_i, one_i, pos, L)
    assert tuple(es) == C.LOSS_ARMS and es["none"] == {} and es[C.EMB] is es["whole_bL"]
    for a in C.ONE:
        assert list(es[a]) == [L] and isinstance(es[a][L], AddRows) and es[a][L].positions == [pos]
    for i, a in enumerate(C.BEFORE):
        assert sorted(es[a]) == list(range(L + 1))
        for la, e in es[a].items():
            assert isinstance(e, SetRows) and e.positions == [pos] and float(e.values[0, 0]) == 10 * i + la
    h = torch.zeros(5, d)
    assert torch.all(es["no_jpp_bL"][3](h)[pos] == 13) and torch.all(es["no_jpp_bL"][3](h)[pos + 1] == 0)
    with pytest.raises(AssertionError):
        C.edit_sets({a: {0: v[0]} for a, v in sets_i.items()}, one_i, pos, L)


def test_the_full_swap_before_l_is_s_and_the_block_outputs_alone_are_not(tok):
    """On a causal fake model: S's states at the patch token at blocks 0..L plus S's token id reproduce S exactly when
    only that token differs; without the id (the three arms' operation) block 0's later tokens still read O's token."""
    import torch

    fake = FakeModel(tok, n_layers=12)
    L, pos = 6, 3
    ids_o, ids_s = [5, 6, 7, 8, 9, 10, 11], [5, 6, 7, 20, 9, 10, 11]
    h_s = fake.run(torch.tensor([ids_s]), record=tuple(range(fake.n_layers)))[1]
    sets_i = {a: {la: h_s[la][pos] for la in range(L + 1)} for a in C.BEFORE}
    es = C.edit_sets(sets_i, {a: torch.zeros(32) for a in C.ONE}, pos, L)
    rd = {"ids": {"org": ids_o, "alt": ids_s}, "pos": pos}
    lg_s = fake.run(torch.tensor([ids_s]))[0]
    lg_emb = fake.run(torch.tensor([C.swapped(rd)]), edits=es[C.EMB])[0]
    lg_bl, st = fake.run(torch.tensor([ids_o]), edits=es["whole_bL"], record=(L, L + 1))
    assert torch.allclose(lg_emb, lg_s, atol=1e-5)
    assert torch.allclose(st[L][pos], h_s[L][pos]) and not torch.allclose(lg_bl, lg_s, atol=1e-5)


# ---- rules on planted numbers -------------------------------------------------------------------------------------------


def test_rule_bars():
    nan = float("nan")
    assert C.slice_rule(0.30, 0.10) == {"rise_ge_0_3": True, "fact_first_within_0_1": True, "slice_explanation": True}
    assert C.slice_rule(0.29, 0.0)["rise_ge_0_3"] is False and C.slice_rule(0.4, -0.10)["slice_explanation"]
    assert not C.slice_rule(0.4, 0.11)["slice_explanation"] and not C.slice_rule(nan, 0.0)["rise_ge_0_3"]
    assert C.carrier_rule(0.10, 0.30) == "the split holds on the full carrier"
    assert C.carrier_rule(0.20, 0.50) == "the lookup follows the lens on the full carrier"
    assert C.carrier_rule(0.15, 0.5) == "in between" and C.carrier_rule(0.05, 0.29) == "in between"
    assert C.carrier_rule(nan, 0.4).startswith("can't tell")
    assert C.away_rule(0.49) and not C.away_rule(0.50) and not C.away_rule(nan)


def planted(tmp_path, monkeypatch, *, after_bl=2, gate_pass=True, target="qwen3.5-9b"):
    """120 passages, 30 bridge entities; the first 60 fact-first. Z1 at L (stored): K whole switches every fact-first
    passage and 1 in 5 fact-after ones, M every passage; without J++ M loses the even passages, K nothing. Before-L:
    K whole switches every fact-first passage and 1 in `after_bl` fact-after ones, M every passage; without J++ M
    loses the even passages, K none; random = whole. The window switches every window passage."""
    monkeypatch.setattr(C, "RESULTS", tmp_path / "x51")
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x50")
    zrun, run = Z.RUNS["z1"][target], C.RUNS[target]
    zsrc, src = tmp_path / "x50" / zrun, tmp_path / "x51" / run
    zsrc.mkdir(parents=True)
    src.mkdir(parents=True)
    keys = [(Z.SETS[0], f"s{i:03d}") for i in range(120)]
    (zsrc / "gate.json").write_text(json.dumps({"pass": gate_pass, "chosen": 120, "order": [list(k) for k in keys],
                                                "org_read_accuracy": {"K": 0.9, "M": 0.9}}))  # fmt: skip
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "source": zrun}))
    zrows, rows, losses, wrows, cases = [], [], [], [], []
    for i, (s, sc) in enumerate(keys):
        first = i < 60
        base = {"set": s, "scene": sc, "entity": f"e{i % 30}", "stratum": "fact-first" if first else "fact-after"}
        k1 = first or i % 5 == 0
        kb = first or i % after_bl == 0
        for a, ksw, msw in (("none", 0, 0), ("whole", k1, 1), ("no_jpp", k1, i % 2), ("no_jpp_rand", k1, 1)):
            zrows += [{**base, "layer": 12, "reader": "K", "arm": a, "switched": int(ksw), "top": 1},
                      {**base, "layer": 12, "reader": "M", "arm": a, "switched": int(msw), "top": 1},
                      {**base, "layer": 99, "reader": "K", "arm": a, "switched": 0, "top": 1}]  # fmt: skip
        for a, ksw, msw in (("none", 0, 0), ("whole_bL", kb, 1), ("no_jpp_bL", kb, i % 2), ("rand_bL", kb, 1),
                            (C.EMB, kb, 1)):  # fmt: skip
            rows += [{**base, "reader": "K", "arm": a, "switched": int(ksw), "top": 1, "route": "x"},
                     {**base, "reader": "M", "arm": a, "switched": int(msw), "top": 1, "route": "x"}]  # fmt: skip
        for w in C.READERS:
            losses += [
                {**base, "reader": w, "arm": a, "loss": 1.0 + (a in C.BEFORE), "top_is_next": 1} for a in C.LOSS_ARMS
            ]
        cases.append({"set": s, "scene": sc, "bridge": f"e{i % 30}", "cf_bridge": "x", "answer": "A", "cf_answer": "B",
                      "stratum": base["stratum"], "n_changed": {"K": 1 + i % 2, "M": 1}, "window": [2, 3],
                      "fact_pos": {"bridge": [3], "cf_bridge": [3]},
                      "readers": {w: {"id": f"{w}-{sc}", "pos": 2, "tok_A": 1, "tok_b": 2, "lure": None,
                                      "ids": {"org": [1, 2, 3, 4], "alt": [1, 2, 5, 4]}} for w in C.READERS}})  # fmt: skip
    wrows = [{**r, "arm": C.WINDOW, "switched": 1, "window": [2, 3]} for r in rows
             if r["reader"] == "K" and r["arm"] == "none" and r["stratum"] == "fact-after"][: C.N_WINDOW]  # fmt: skip
    X.write_jsonl(zsrc / "outcomes.jsonl", zrows)
    for f, rs in (("outcomes", rows), ("losses", losses), ("window", wrows), ("cases", cases)):
        X.write_jsonl(src / f"{f}.jsonl", rs)
    return run


def test_planted_slice_explanation_and_split_on_the_full_carrier(tmp_path, monkeypatch):
    m = C.model_result("qwen3.5-9b", planted(tmp_path, monkeypatch), n_boot=200)
    ff, fa = m["groups"]["fact-first"], m["groups"]["fact-after"]
    assert m["status"] == "tested" and ff["n"] == 60 and fa["n"] == 60 and m["groups"]["all"]["entities"] == 30
    assert fa["shares"]["K"]["whole_1L"][0] == 0.2 and fa["shares"]["K"]["whole_bL"][0] == 0.5
    assert m["rule_i"]["rise"][0] == pytest.approx(0.3) and m["rule_i"]["slice_explanation"]
    assert m["rule_i"]["k_minus_m_fact_first"][0] == 0.0
    assert ff["before"]["lookup"]["excess"][0] == 0.0 and ff["before"]["recall"]["excess"][0] == 0.5
    assert m["rule_ii_decisive"] == "the split holds on the full carrier" == ff["one"]["label"]
    assert not m["rule_iii"]["away"] and m["rule_iii"]["window"] == {"n": C.N_WINDOW, "reported": False}
    assert m["checks"]["none_matches_z1_none"] == [240, 240]
    assert m["loss"]["K"]["whole_bL"]["ratio_to_whole_1L"][0] == 2.0
    assert m["checks"]["only_last_token"]["fact-first, only the last token changed"]["n"] == 30


def test_planted_away_from_the_bridge_token_reports_the_window(tmp_path, monkeypatch):
    m = C.model_result("qwen3.5-9b", planted(tmp_path, monkeypatch, after_bl=4, gate_pass=False), n_boot=200)
    assert m["status"].startswith("not tested (Z1's gate")
    assert m["groups"]["fact-after"]["shares"]["K"]["whole_bL"][0] == 0.25 and not m["rule_i"]["rise_ge_0_3"]
    w = m["rule_iii"]["window"]
    assert m["rule_iii"]["away"] and w["n"] == C.N_WINDOW and w["window"][0] == 1.0
    assert w["whole_bL"][0] == pytest.approx(13 / 50)  # i % 4 == 0 among the first 50 fact-after passages (i = 60..109)
    assert C.model_result("qwen3.6-27b", "x51_7_27b")["status"] == "pending"


# ---- the seal -------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_q51_7(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q51.6** x\n\nDan: yes\n\n**Q51.7** (51.7) Z1 ...\n- (i) ...\n\nDan:{}\n"
    monkeypatch.setattr(Z.subprocess, "run", fake_git(blocks.format("")))
    assert C.dan_answer() == ""
    monkeypatch.setattr(Z.subprocess, "run", fake_git(blocks.format(" (i) 9B 40%\nDan (27B): 30%\n- split holds")))
    assert C.dan_answer() == "(i) 9B 40%\nDan (27B): 30%\n- split holds"


def test_verdict_and_view_are_sealed_then_written(tmp_path, monkeypatch):
    run = planted(tmp_path, monkeypatch)
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_verdict([run], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_view([run], decode=lambda ids: "")
    assert [p.name for p in (tmp_path / "x51").iterdir()] == [run]  # nothing written while sealed
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "9B 40%")
    decode = lambda ids: "".join(f"<{i}>" for i in ids)  # noqa: E731
    out = C.stage_verdict([run], n_boot=50, decode=decode)
    md = (out / "verdict.md").read_text()
    assert "Q51.7 (Dan: 9B 40%)" in md and "| qwen3.5-9b | qwen35_9b_x51_7 | tested |" in md
    assert "the split holds on the full carrier" in md and "not reported" in md
    assert (out / "x51_7_qwen3.5-9b.png").exists() and json.loads((out / "verdict.json").read_text())["dan"] == "9B 40%"
    view = (out / "view.md").read_text()
    assert view.count("### jsuite") == C.N_PROMPTS and "<1><2>⟦<3>⟧<4>" in view
    assert all(f"### arm {a}: {C.N_ROWS} random rows" in view for a in (*C.READ_ARMS, C.WINDOW))
    out2 = C.stage_view([run], decode=decode)
    assert (out2 / "view.md").exists()


# ---- the run stage on a fake model (CPU) ---------------------------------------------------------------------------------


class FakeLensAll(FakeLens):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.source_layers = list(range(40))


def test_run_stage_end_to_end_on_a_fake_model(tok, tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    if pins.TARGET not in C.RUNS:
        pytest.skip("51.7 runs on the 9B and the 27B")
    fake = FakeModel(tok, n_layers=40)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLensAll)
    monkeypatch.setattr(C, "RESULTS", tmp_path / "x51")
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x50")
    monkeypatch.setattr(C, "N_WINDOW", 2)
    real_load = Z.load_pairs
    monkeypatch.setattr(Z, "load_pairs", lambda s, p: (real_load(s, p)[0][:30], {}))
    cases, _ = Z.z1_cases(tok, Z.load_pairs(Z.SETS[0], "z1")[0])
    chosen = [c for c in cases if c["stratum"] == "fact-first"][:2] + [
        c for c in cases if c["stratum"] == "fact-after"
    ][:3]
    zsrc = tmp_path / "x50" / Z.RUNS["z1"][pins.TARGET]
    zsrc.mkdir(parents=True)
    (zsrc / "gate.json").write_text(json.dumps({"pass": True, "order": [[c["set"], c["scene"]] for c in chosen]}))
    X.write_jsonl(zsrc / "cases.jsonl", cases)
    out = C.stage_run(f"{pins.RUN_PREFIX}fake_x51_7")
    m = json.loads((out / "manifest.json").read_text())
    L_ = C.layer_of(pins.TARGET)
    assert m["items"] == 5 and m["layers"] == list(range(L_ + 1)) and m["rule"] == C.RULE and "sealed" in m
    assert not any(p.name.startswith(("verdict", "x51_7")) for p in out.iterdir())  # sealed
    rows, losses = X.read_jsonl(out / "outcomes.jsonl"), X.read_jsonl(out / "losses.jsonl")
    wrows, norms = X.read_jsonl(out / "window.jsonl"), X.read_jsonl(out / "norms.jsonl")
    assert len(rows) == 5 * 2 * len(C.READ_ARMS) and len(losses) == 5 * 2 * len(C.LOSS_ARMS)
    assert len(wrows) == 2 and all(r["reader"] == "K" and r["stratum"] == "fact-after" for r in wrows)
    assert len(norms) == 5 * 2 * (L_ + 1)
    # the first read: the first passage's K reader, none + the three before-L arms on O; whole_bL = S's clean states
    c = chosen[0]
    rd = c["readers"]["K"]
    reads = [e for s, e in fake.calls if len(e) == 1 + len(C.BEFORE) and s == len(rd["ids"]["org"])]
    edits = reads[0]
    assert edits[0] == {} and sorted(edits[1]) == list(range(L_ + 1))
    h_s = fake.run(torch.tensor([rd["ids"]["alt"]]), record=tuple(range(L_ + 1)))[1]
    for la in (0, L_ // 2, L_):
        assert edits[1][la].positions == [rd["pos"]] and torch.allclose(edits[1][la].values[0], h_s[la][rd["pos"]])
    # without J++ before-L at L = Z1's one-layer state at L (h_O + Z1's no_jpp vector)
    loss_calls = [e for s, e in fake.calls if len(e) == len(C.LOSS_ARMS) - 1 and s == rd["pos"] + 1]
    one = loss_calls[0][2][L_]
    h_o = fake.run(torch.tensor([rd["ids"]["org"]]), record=(L_,))[1][L_][rd["pos"]]
    assert torch.allclose(edits[2][L_].values[0], h_o + one.delta[0], atol=1e-5)
