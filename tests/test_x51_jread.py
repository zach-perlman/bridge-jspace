"""Batch 51, test 51.10 (scripts/x51_jread.py): the positions (P2 the question's pick token, P2 / P3 placed in S from
the end), the write parts (his swap by his code path, the J++ part, the matched random parts), his knock-out at one
position, the probes (scene-level folds, planted signal vs noise), the answer layer and the read peak, the rules'
labels on planted numbers (the ratio read at the peak, not the max), the run / read / verdict / view stages end to end
on a tiny fake model (CPU), and the seal. No real model."""

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from bridge_jspace.ablate import MatrixDictionary, top_span_removal
from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x49_gain as G
from scripts import x51_jread as J
from tests.test_x49_gain import D as DIM
from tests.test_x49_gain import FakeLens, FakeModel

LK, RC = X.LOOKUP, X.RECALL


# ---- positions ------------------------------------------------------------------------------------------------------


def _offsets(pieces: list[str]) -> tuple[str, list[tuple[int, int]]]:
    text, offs = "", []
    for p in pieces:
        offs.append((len(text), len(text) + len(p)))
        text += p
    return text, offs


def test_pick_position_is_the_questions_pick_token_not_the_contexts_picked():
    pieces = [
        "Leo",
        " picked",
        " iota",
        ".",
        "\n",
        "Which",
        " locker",
        " belongs",
        " to",
        " Leo",
        "'s",
        " pick",
        "?",
        " A",
    ]
    text, offs = _offsets(pieces)
    assert J.pick_position(text, "Which locker belongs to Leo's pick?", offs) == 11
    pieces2 = [
        "Leo",
        " picked",
        " iota",
        ".\n",
        "How",
        " many",
        " legs",
        " does",
        " Leo",
        "'s",
        " pi",
        "ck",
        " have",
        "?",
    ]
    text2, offs2 = _offsets(pieces2)
    assert J.pick_position(text2, "How many legs does Leo's pick have?", offs2) == 11  # the last token over "pick"
    with pytest.raises(J.Dropped):
        J.pick_position(text, "Which locker is it?", offs)


def test_positions_in_s_are_counted_from_the_end():
    org = [1, 2, 3, 50, 7, 8, 9]
    alt = [1, 2, 3, 3, 60, 7, 8, 9]  # one more token before the question
    pos = J.positions_of({"org": org, "alt": alt}, 3, 5, 1)
    assert pos["P1"] == {"org": 3, "alt": 3} and pos["P2"] == {"org": 5, "alt": 6}
    assert pos["P3"] == {"org": 7, "alt": 8}  # the read's appended space token
    with pytest.raises(J.Dropped, match="differ after"):
        J.positions_of({"org": org, "alt": [1, 2, 3, 60, 7, 0, 9]}, 3, 5, 1)
    with pytest.raises(J.Dropped, match="not after"):
        J.positions_of({"org": org, "alt": org}, 5, 5, 1)


def test_layers_fixed_in_advance():
    assert J.LAYERS["qwen3.5-9b"] == tuple(range(2, 31, 2)) and max(J.LAYERS["qwen3.5-9b"]) < J.N_LAYERS["qwen3.5-9b"]
    assert J.LAYERS["qwen3.6-27b"] == (4, 8, 12, 16, 20, 24, 28, 30, 32, 34, 36, 40, 44, 48, 52, 56, 60)
    assert J.LAYERS["muse-glimmer-30b"] == (4, 8, 12, 16, 20, 24, 26, 28, 32, 36, 40, 44, 48)
    for t, la in J.LAYERS.items():
        assert X.PREDICTED[t] in la and J.N_LAYERS[t] == J.pins.TARGETS[t]["n_layers"]
    assert len(J.write_names((2, 4))) == 3 * 2 * 8 and len(J.loss_names((2, 4))) == 2 * 2 * 8


# ---- the parts and edits ---------------------------------------------------------------------------------------------


def _dict(n: int = 80, seed: int = 0) -> torch.Tensor:
    return torch.nn.functional.normalize(torch.randn(n, DIM, generator=torch.Generator().manual_seed(seed)), dim=-1)


def test_write_parts_are_his_swap_x0s_jpp_part_and_matched_random_parts():
    g = torch.Generator().manual_seed(1)
    jd = _dict()
    dic = MatrixDictionary(jd)
    ho, hs = torch.randn(6, DIM, generator=g), torch.randn(6, DIM, generator=g)
    basis = SP.random_basis(DIM, torch.Generator().manual_seed(X.SUBSPACE_SEED + 4))
    prot = [(torch.tensor([0, 1, 2]), torch.tensor([5, 7]))]
    pt = J.write_parts(jd, dic, ho, hs, prot, basis)
    delta = hs - ho
    assert torch.allclose(pt["delta"], delta)
    assert torch.allclose(pt["pj"], X.fit(jd, delta, J.K, "signed"), atol=1e-5)  # 49.1's P_J Δ
    # his swap, jswap's expression: h_X - J10(h_X) + J10(h_D), both with O's protected rows
    rx, rd = top_span_removal(dic, ho, 10, protected=prot), top_span_removal(dic, hs, 10, protected=prot)
    for i in range(6):
        assert torch.allclose(ho[i] + J.arm_vector(pt, "swap", i), (ho - rx + rd)[i], atol=1e-5)
    # a protected row is never in the top-10 of the rows it protects; the other rows choose as unprotected
    free = top_span_removal(dic, ho, 10, return_chosen=True)[1]
    chosen = top_span_removal(dic, ho, 10, protected=prot, return_chosen=True)[1]
    assert not (set(chosen[0].tolist()) & {5, 7}) and torch.equal(free[3:], chosen[3:])
    one = ((delta @ basis) ** 2).max(dim=-1).values / delta.norm(dim=-1) ** 2
    assert ((G.share(pt["rj"], delta) - G.share(pt["pj"], delta)).abs() <= one + 1e-6).all()
    capped = pt["share_c"].clamp(max=1.0)
    assert ((G.share(pt["rc"], delta) - capped).abs() <= one + 1e-6).all()
    # his rotated control: the swap's change at its own size, turned by jswap's rotation (ablate.rotation, seed 888 + l)
    from bridge_jspace.ablate import rotation

    rot = rotation(DIM, X.SUBSPACE_SEED + 4, device="cpu")
    assert torch.allclose(J.arm_vector(pt, "swap_rot", 3), (rd - rx)[3] @ rot.T, atol=1e-4)
    assert torch.allclose(J.arm_vector(pt, "swap_rot", 3).norm(), (rd - rx)[3].norm(), atol=1e-4)
    assert torch.allclose(J.arm_vector(pt, "jpp2", 2), 2 * pt["pj"][2]) and torch.allclose(
        J.arm_vector(pt, "whole", 1), delta[1]
    )
    assert torch.allclose(J.arm_vector(pt, "rand2", 0), 2 * pt["rj"][0]) and set(J.TWIN.values()) < set(J.WRITE_ARMS)
    rec = J.norm_record(pt, 0)
    assert rec["swap_share_capped"] == bool(pt["share_c"][0] > 1) and rec["share_J"] == pytest.approx(
        float(G.share(pt["pj"][:1], delta[:1])[0]), abs=1e-5
    )


def test_his_knockout_at_one_position_and_its_random_twin():
    g = torch.Generator().manual_seed(2)
    dic = MatrixDictionary(_dict(seed=3))
    h = torch.randn(7, DIM, generator=g)
    prot = torch.tensor([1, 2])
    ko = J.TopAt(dic, prot, 6)
    out = ko(h)
    assert torch.equal(out[:6], h[:6])
    r = top_span_removal(dic, h[6:7], 10, protected=[(torch.tensor([0]), prot)])
    assert torch.allclose(out[6], h[6] - r[0], atol=1e-5)
    basis = SP.random_basis(DIM, torch.Generator().manual_seed(9))
    kr = J.TopAt(dic, prot, 6, basis)
    out2 = kr(h)
    assert torch.equal(out2[:6], h[:6])
    one = float(((h[6] @ basis) ** 2).max() / h[6].norm() ** 2)
    assert abs(kr.log[0] - ko.log[0]) <= one + 1e-6  # the same share of ||h||^2, within one random direction


# ---- probes and the read statistics -----------------------------------------------------------------------------------


def _items(n: int, lf_every: int = 2) -> list[dict]:
    ents = ["ant", "bee", "cat", "dog", "eel", "fox"]
    return [{"scene": f"S{i:03d}", "entity": ents[i % 6], "cf_bridge": ents[(i + 1) % 6], "domain": "animals",
             "lf": i % lf_every == 0} for i in range(n)]  # fmt: skip


def test_probe_rows_keep_a_scenes_o_and_s_together():
    items = _items(30)
    rows = J.probe_rows(items)
    assert rows["labels"][:4] == ["ant", "bee", "bee", "cat"] and list(rows["variant"][:2]) == ["org", "alt"]
    assert (rows["folds"][0::2] == rows["folds"][1::2]).all() and len(set(rows["folds"].tolist())) == J.K_OUTER
    assert rows["chance"][0] == pytest.approx(1 / 6) and rows["lf"][0] and not rows["lf"][2]


def test_probe_reads_a_planted_entity_and_not_noise():
    items = _items(60)
    rows = J.probe_rows(items)
    rng = np.random.default_rng(0)
    means = {e: rng.normal(size=32) * 3 for e in set(rows["labels"])}
    signal = np.stack([means[y] for y in rows["labels"]]) + rng.normal(size=(120, 32))
    noise = rng.normal(size=(120, 32))
    good, bad = J.probe_cell(signal.astype(np.float32), rows, 200), J.probe_cell(noise.astype(np.float32), rows, 200)
    assert good["lf"][0] >= 0.9 and good["all"][0] >= 0.9 and good["lf"][1] <= good["lf"][0] <= good["lf"][2]
    assert bad["lf"][0] <= 0.45 and good["chance_lf"] == pytest.approx(1 / 6) and good["lf_class_unseen"] == 0
    assert good["lf_O"] is not None and good["lf_S"] is not None and good["n_lf"] == 60


def test_settle_layer_answer_layer_and_read_peak():
    assert J.settle_layer([0, 5, 0, 5, 5], 5) == 3 and J.settle_layer([5, 5, 5], 5) == 0
    assert J.settle_layer([5, 5, 0], 5) is None
    cases = {"a": {"lf": True}, "b": {"lf": True}, "c": {"lf": False}, "d": {"lf": True}}
    ll = [{"scene": s, "reader": w, "variant": v, "tok": 5, "top": t}
          for s, t in (("a", [0, 0, 5, 5]), ("b", [0, 5, 5, 5]), ("c", [5, 5, 5, 5]), ("d", [0, 0, 0, 5]))
          for w in X.READERS for v in J.VARIANTS]  # fmt: skip
    ans = J.answer_layers(ll, cases)
    assert ans["lookup"]["layer"] == 2 and ans["recall"]["per_item"] == [2, 1, 3] and ans["lookup"]["never"] == 0
    thru = {2: 0.5, 4: 0.9, 6: 0.9, 8: 1.0}
    assert J.read_peak(thru, (2, 4, 6, 8), 8) == 4  # before the answer layer; ties to the earliest
    assert J.read_peak(thru, (2, 4, 6, 8), 2) is None


# ---- the rules on planted numbers -------------------------------------------------------------------------------------


LAYERS = [4, 8, 12, 16]


def _sw(spec: dict[int, dict[str, float]]) -> dict[int, dict[str, float]]:
    return {la: {a: spec.get(la, {}).get(a, 0.0) for a in J.WRITE_ARMS} for la in LAYERS}


def _cells(thru, full, top5) -> dict[int, dict]:
    return {la: {"thru": t, "full": f, "top5": k} for la, t, f, k in zip(LAYERS, thru, full, top5, strict=True)}


def test_rule_a_read_and_write_at_the_peak():
    cells = _cells([0.3, 0.85, 0.7, 0.95], [0.95] * 4, [0.2, 0.6, 0.6, 0.9])
    r = J.position_rule(cells, _sw({8: {"whole": 0.8, "swap": 0.4, "swap_rand": 0.1}}), LAYERS, 16)
    assert r["read"] and r["peak"] == 8 and r["write"] and r["label"] == J.LABELS["a"]
    assert r["first_readable"] == 8 and r["first_readable_before_answer"] == 8  # L16 is not before the answer
    assert r["at_peak"]["arms"]["swap"]["ratio"] == pytest.approx(0.5)  # at the bar counts


def test_rule_b_readable_not_used_and_the_ratio_is_read_at_the_peak_not_the_max():
    cells = _cells([0.3, 0.85, 0.6, 0.4], [0.95] * 4, [0.2, 0.6, 0.6, 0.6])
    sw = _sw({8: {"whole": 0.9, "swap": 0.2, "jpp2": 0.6, "rand2": 0.15}, 12: {"whole": 0.5, "swap": 0.5}})
    r = J.position_rule(cells, sw, LAYERS, 16)
    assert r["peak"] == 8 and not r["write"] and r["label"] == J.LABELS["b"]
    assert r["best_layer"] == 8 and r["at_best"]["arms"]["jpp2"]["ok"] is False  # its random twin is above 0.10
    sw2 = _sw({8: {"whole": 0.9, "swap": 0.2}, 12: {"whole": 0.5, "swap": 0.5}})
    r2 = J.position_rule(cells, sw2, LAYERS, 16)
    assert not r2["write"] and r2["best_layer"] == 12 and r2["at_best"]["holds"]  # the best layer does not decide
    # the swap's decisive twin is swap_rand; his rotated control decides only the beside line
    sw3 = _sw({8: {"whole": 0.8, "swap": 0.6, "swap_rand": 0.5, "swap_rot": 0.05}})
    r3 = J.position_rule(cells, sw3, LAYERS, 16)
    assert not r3["write"] and r3["write_with_his_rotated_control"] and r3["label"] == J.LABELS["b"]


def test_rule_c_routes_around_and_d_not_represented():
    sw = _sw({4: {"whole": 0.9, "swap": 0.05}})
    c = J.position_rule(_cells([0.2, 0.4, 0.45, 0.9], [0.5, 0.92, 0.95, 0.95], [0.0] * 4), sw, LAYERS, 16)
    assert c["routes_clause"] and not c["read"] and c["label"] == J.LABELS["c"]
    d = J.position_rule(_cells([0.1, 0.1, 0.2, 0.9], [0.3, 0.4, 0.45, 0.95], [0.0] * 4), sw, LAYERS, 16)
    assert d["not_represented_clause"] and d["label"] == J.LABELS["d"]
    mid = J.position_rule(_cells([0.6, 0.6, 0.6, 0.6], [0.95] * 4, [0.6] * 4), sw, LAYERS, 16)
    assert mid["label"] == "none of the four"
    wo = J.position_rule(_cells([0.2, 0.3, 0.3, 0.3], [0.95] * 4, [0.0] * 4),
                         _sw({8: {"whole": 0.8, "jpp1": 0.5, "rand1": 0.0}}), LAYERS, 16)  # fmt: skip
    assert (
        wo["peak"] == 8
        and wo["write"]
        and wo["routes_clause"]
        and wo["label"] == "none of the four (writable, not readable)"
    )
    und = J.position_rule(_cells([0.9] * 4, [0.95] * 4, [0.9] * 4), sw, LAYERS, 4)
    assert und["label"] == "undecided" and und["first_readable"] == 4


def test_write_fails_when_the_whole_patch_switches_nothing():
    w = J.write_at({a: 0.0 for a in J.WRITE_ARMS})
    assert not w["holds"] and w["arms"]["swap"]["ratio"] is None


# ---- end to end on a fake model ---------------------------------------------------------------------------------------


class JFake(FakeModel):
    def __init__(self):
        super().__init__(n_layers=J.N_LAYERS[J.pins.TARGET])
        self.hf = SimpleNamespace(lm_head=SimpleNamespace(weight=self.unemb))

    def unembed(self, h):
        return h.float() @ self.unemb.T

    def norm_gain(self):
        return torch.ones(DIM)


class JLensFake(FakeLens):
    source_layers = tuple(range(64))

    def __init__(self, model=None, name="jpp"):
        super().__init__(model, name)
        self.model = model

    def J(self, layer, device=None):
        return torch.eye(DIM) + 0.3 * torch.randn(DIM, DIM, generator=torch.Generator().manual_seed(100 + layer))

    def readout(self, h, layer):
        return self.model.unembed(h.float() @ self.J(layer).T)


def _jitem(i: int) -> dict:
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    rd = {"id": f"PP-{i}", "question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
          "ids": {"org": [*org, 7, 12], "alt": [*alt, 7, 12]}, "tok_A": 5, "tok_b": 3}  # fmt: skip
    rc = {**rd, "id": f"PM-{i}", "question": "How many legs does Iris's pick have?",
          "ids": {"org": [*org, 8, 9, 13], "alt": [*alt, 8, 9, 13]}}  # fmt: skip
    it = {"scene": f"P2-{i:04d}", "entity": f"e{20 + i % 5}", "cf_bridge": f"e{40 + i % 5}", "domain": "animals",
          "pos": 4, "group": G.GROUP if i % 2 == 0 else "mixed", "space": [11], "readers": {LK: rd, RC: rc},
          "stored": {"whole": {LK: 1, RC: 0}}}  # fmt: skip
    return {
        **it,
        "lf": i % 2 == 0,
        "jpos": {LK: J.positions_of(rd["ids"], 4, 6, 1), RC: J.positions_of(rc["ids"], 4, 7, 1)},
    }


def _stage(monkeypatch, tmp_path, items, gate_pass=True):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins

    monkeypatch.setattr(M, "load_model", lambda: JFake())
    monkeypatch.setattr(LN, "JLens", JLensFake)
    monkeypatch.setattr(J, "RESULTS", tmp_path / "x51_jread")
    monkeypatch.setattr(G, "RESULTS", tmp_path / "x49_gain")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(J, "SPEC", tmp_path / "batch51.yaml")
    monkeypatch.setitem(J.LAYERS, pins.TARGET, (4, 8, 12))
    J.SPEC.write_text("")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(J, "select", lambda tok, t: (items, {"items_read": len(items)}))
    src = X.RESULTS / G.SOURCES[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    (src / "gate.json").write_text(json.dumps({"gate": {"chat": {"pass": gate_pass, "enough": True}}}))


def test_stage_run_read_verdict_view_end_to_end(tmp_path, monkeypatch):
    from bridge_jspace import pins

    items = [_jitem(i) for i in range(16)]
    _stage(monkeypatch, tmp_path, items)
    run = J.RUNS[pins.TARGET]
    out = J.stage_run(run, "test")
    files = sorted(p.name for p in out.iterdir())
    assert files == ["cases.jsonl", "clean.jsonl", "gate.json", "logit_lens.jsonl", "losses.jsonl", "manifest.json",
                     "norms.jsonl", "outcomes.jsonl", "peak.json", "plan.json", "removal.jsonl", "removal_norms.jsonl",
                     J.STATES_FILE]  # fmt: skip
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "51.10" and m["layers"] == [4, 8, 12] and "sealed" in m and "switches" in m
    rows = X.read_jsonl(out / "outcomes.jsonl")
    n_lf = 8
    assert len(rows) == n_lf * 2 * (1 + 3 * 3 * 8)
    assert {(r["pos"], r["layer"], r["arm"]) for r in rows} == {(None, None, "none"), *J.write_names((4, 8, 12))}
    assert len(X.read_jsonl(out / "losses.jsonl")) == n_lf * 2 * 2 * (1 + 3 * 8)
    z = np.load(out / J.STATES_FILE)
    assert z["h"].shape == (16, 2, 2, 3, 3, DIM) and z["h"].dtype == np.float16
    # the cached state is the block output at the position: P2 of the recall's S prompt at L8
    it = items[1]
    rec = JFake().run(torch.tensor([it["readers"][RC]["ids"]["alt"] + it["space"]]), record=(8,))[1][8]
    assert np.allclose(z["h"][1, 1, 1, 1, 1], rec[it["jpos"][RC]["P2"]["alt"]].numpy(), atol=1e-2)
    # the lens rank: O's entity token on O's rows
    assert (z["rank_own"] >= 1).all() and (z["rank_own_full"] >= 1).all()
    none = [r for r in rows if r["arm"] == "none"]
    assert len(none) == n_lf * 2
    peaks = json.loads((out / "peak.json").read_text())["peaks"]
    assert set(peaks) == {"lookup", "recall"}
    rem = X.read_jsonl(out / "removal.jsonl")
    assert len(rem) == sum(v is not None for v in peaks.values()) * n_lf * len(J.REMOVE_ARMS)
    assert not list(J.RESULTS.glob("x51_10-*"))  # sealed: no verdict

    rd = J.stage_read(run, n_boot=20)
    stats = json.loads((rd / "read.json").read_text())
    assert stats["peak_matches_run"] is True and stats["n_lf"] == n_lf and stats["n_items"] == 16
    assert set(stats["cells"]) == {f"{w}|{p}|{la}" for w in ("lookup", "recall") for p in J.POS for la in (4, 8, 12)}

    monkeypatch.setattr(J, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        J.stage_verdict(n_boot=20)
    with pytest.raises(AssertionError, match="sealed"):
        J.stage_view(n_boot=20)
    monkeypatch.setattr(J, "dan_answer", lambda rev="HEAD": "planted")
    v = J.stage_verdict(n_boot=20)
    blob = json.loads((v / "verdict.json").read_text())
    assert set(blob["labels"]) == {pins.TARGET} and (v / f"jread_{pins.TARGET}.png").exists()
    assert "| " + pins.TARGET + " | lookup |" in (v / "verdict.md").read_text()
    view = J.stage_view(decode_for=lambda t: lambda ids: " ".join(map(str, ids)), n_boot=20)
    text = (view / "view.md").read_text()
    assert "Dumbest ways to be wrong" in text and "changed to another digit" in text and "not at the max" in text
    assert all(f"### {a}: " in text for a in (*J.WRITE_ARMS, *J.REMOVE_ARMS[1:]))


def test_stage_run_without_the_gate_writes_no_outcomes(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, [_jitem(0)], gate_pass=False)
    out = J.stage_run(f"{pins.RUN_PREFIX}x51_test_gate", "test")
    assert not (out / "outcomes.jsonl").exists() and json.loads((out / "gate.json").read_text())["tested"] is False


# ---- the seal ------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_the_q51_10_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q51.1** x\n\nDan: (i) yes\n\n**Q51.10** (51.10) Does the intermediate ...\n- At the last token: (a) ...\n"
              "- At the pick token: ...\n\nDan:{}\n\n**Q51.11** next\n\nDan: (a)\n")  # fmt: skip
    monkeypatch.setattr(J.subprocess, "run", fake_git(blocks.format("")))
    assert J.dan_answer() == ""
    monkeypatch.setattr(J.subprocess, "run", fake_git(blocks.format(" lookup (c) 70%")))
    assert J.dan_answer() == "lookup (c) 70%"
    monkeypatch.setattr(J.subprocess, "run", fake_git(blocks.format("\nDan (27B): recall (a) 60%\n- P2 (d)")))
    assert "Dan (27B): recall (a) 60%" in J.dan_answer() and "- P2 (d)" in J.dan_answer()


def test_the_committed_predictions_file_has_the_q51_10_block():
    text = J.subprocess.run(["git", "show", f"HEAD:{J.PREDICTIONS}"], cwd=J.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{J.QUESTION}**" in text and isinstance(J.dan_answer(), str)


def test_run_names_pass_the_prefix_check():
    from bridge_jspace import pins

    assert J.RUNS[pins.TARGET].startswith(pins.RUN_PREFIX)
    assert J.RUNS == {
        "qwen3.5-9b": "qwen35_9b_x51_10",
        "qwen3.6-27b": "x51_10_27b",
        "muse-glimmer-30b": "muse30_x51_10",
    }
