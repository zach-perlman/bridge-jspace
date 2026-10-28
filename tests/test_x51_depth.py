"""Batch 51, test 51.5 (scripts/x51_depth.py): Z1's items in run order (fact-first first) and their re-alignment, the
window ends and the rule on planted numbers (ours and his by the same code), the reference against the stored 47.8 runs,
the seal, and the run stage end to end on a tiny fake model (CPU): the arms, the stratum written before the next one,
the optional split. No real model."""

import json
from types import SimpleNamespace

import pytest

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x50_zach as Z
from scripts import x51_depth as D
from tests.test_x47_cue import FakeLens, FakeModel


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


# ---- items --------------------------------------------------------------------------------------------------------


def test_run_order_puts_fact_first_first_and_keeps_z1s_order():
    cs = [{"scene": s, "stratum": st} for s, st in (("a", "fact-after"), ("b", "fact-first"), ("c", "fact-after"),
                                                     ("d", "fact-first"))]  # fmt: skip
    assert [c["scene"] for c in D.run_order(cs)] == ["b", "d", "a", "c"]


def plant_z1(root, target: str, cases: list[dict], order: list[int], gate_pass: bool = True):
    src = root / Z.RUNS["z1"][target]
    src.mkdir(parents=True)
    X.write_jsonl(src / "cases.jsonl", cases)
    gate = {"pass": gate_pass, "org_read_accuracy": {"K": 0.9, "M": 0.85}, "cases": len(cases) + 5,
            "eligible": len(cases), "order": [[cases[i]["set"], cases[i]["scene"]] for i in order],
            "counts": {"planted": len(cases)}}  # fmt: skip
    (src / "gate.json").write_text(json.dumps(gate))
    return src


def test_z1_items_join_the_gate_order_to_the_cases(tmp_path, monkeypatch):
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    cases = [{"set": "s", "scene": f"p{i}", "stratum": D.STRATA[i % 2]} for i in range(6)]
    plant_z1(tmp_path, "qwen3.5-9b", cases, [5, 0, 3, 2], gate_pass=False)  # p1, p4 not chosen
    items, info = D.z1_items("qwen3.5-9b")
    assert [c["scene"] for c in items] == ["p0", "p2", "p5", "p3"]
    assert info["chosen"] == 4 and info["strata"] == {"fact-first": 2, "fact-after": 2} and info["pass"] is False


@pytest.fixture(scope="module")
def z1_built(tok):
    ps, _ = Z.load_pairs(Z.SETS[0], "z1")
    cases, _ = Z.z1_cases(tok, ps[:40])
    ff = [c for c in cases if c["stratum"] == "fact-first"][:2]
    fa = [c for c in cases if c["stratum"] == "fact-after"][:2]
    assert len(ff) == len(fa) == 2
    return [fa[0], ff[0], fa[1], ff[1]]  # Z1's order mixes the strata


def test_alignment_check_catches_a_changed_item(tok, z1_built):
    good = D.check_alignment(tok, z1_built)
    assert good == {"items": 4, "same": 4, "differ": []}
    bad = json.loads(json.dumps(z1_built))
    bad[2]["readers"]["M"]["pos"] += 1
    bad[3]["cf_bridge"] = "nobody"
    out = D.check_alignment(tok, bad)
    assert out["same"] == 2 and sorted(out["differ"]) == sorted([[c["set"], c["scene"]] for c in bad[2:]])


def test_the_stored_z1_items_realign_on_this_tokenizer(tok):
    if pins.TARGET not in D.TARGETS or not (D.z1_run(pins.TARGET) / "gate.json").exists():
        pytest.skip("no stored Z1 run for this target here")
    items, info = D.z1_items(pins.TARGET)
    assert info["chosen"] == len(items) == 200 and [c["stratum"] for c in items] == sorted(
        (c["stratum"] for c in items), key=D.STRATA.index
    )
    assert D.check_alignment(tok, items[:30] + items[-30:])["same"] == 60


# ---- the window and the rule --------------------------------------------------------------------------------------


def test_switch_rates_and_window_ends():
    rows = [{"reader": "K", "arm": a, "layer": la, "route": "switch" if s else "original"}
            for la, ss in ((2, [1, 1]), (4, [1, 0]), (6, [0, 0]), (8, [1, 0])) for s in ss for a in ("whole", "no_jpp")]  # fmt: skip
    rows += [{"reader": "K", "arm": "none", "layer": None, "route": "switch"}]
    r = D.switch_rates(rows, "K", D.HIS_MOVED)
    assert r == {2: 1.0, 4: 0.5, 6: 0.0, 8: 0.5}
    assert D.window_end(r) == 8 and D.window_start(r) == 2  # the last layer >= 0.3, even past a gap
    assert D.window_end({2: 0.2999, 4: 0.30}) == 4 and D.window_end({2: 0.29}) is None


def test_same_window_bars():
    ours = {"lookup": 16, "recall": 14}
    assert D.same_window(ours, {"lookup": 20, "recall": 10})["holds"]  # exactly 4 either way
    r = D.same_window(ours, {"lookup": 22, "recall": 14})
    assert not r["holds"] and r["per_reader"]["lookup"] == {"ours": 16, "his": 22, "diff": 6, "within": False}
    assert r["label"] == "not the same read window as ours" and r["per_reader"]["recall"]["within"]
    assert not D.same_window(ours, {"lookup": 16, "recall": None})["holds"]  # no window on his passages
    assert D.same_window(ours, {"lookup": 12, "recall": 18})["label"] == "the same read window as ours"


def test_zach_beside():
    assert D.zach_beside({2: 0.1, 4: 0.6, 20: 0.4, 24: 0.31, 26: 0.29, 30: 0.0}) == {
        "first": 4, "last": 24, "his_window": [4, 20], "gone_by_25": True}  # fmt: skip
    assert not D.zach_beside({4: 0.6, 28: 0.3})["gone_by_25"]
    assert D.zach_beside({4: 0.1})["last"] is None


def test_ours_counts_47_8s_switch_routes(tmp_path, monkeypatch):
    from scripts import x47_anatomy as A

    monkeypatch.setattr(A, "RESULTS", tmp_path)
    src = tmp_path / D.OURS["qwen3.5-9b"]
    src.mkdir()
    rows = []
    for la, lk, rc in ((2, ["identity", "position"], ["changed", "changed"]), (4, ["position", "original"],
                       ["slot", "original"]), (6, ["value", "other"], ["original", "other"])):  # fmt: skip
        for i in range(2):
            rows.append({"condition": "C2", "reader": X.LOOKUP, "layer": la, "arm": "whole", "route": lk[i]})
            rows.append({"condition": "C2", "reader": X.RECALL, "layer": la, "arm": "whole", "route": rc[i]})
            rows.append({"condition": "C0", "reader": X.LOOKUP, "layer": la, "arm": "whole", "route": None})
    X.write_jsonl(src / "outcomes.jsonl", rows)
    ref = D.reference("qwen3.5-9b")
    assert ref["rates"]["lookup"] == {"2": 1.0, "4": 0.5, "6": 0.5} and ref["rates"]["recall"] == {
        "2": 1.0,
        "4": 0.0,
        "6": 0.0,
    }
    assert ref["lookup"] == 6 and ref["recall"] == 2 and ref["verdict"] is None and ref["matches_verdict"] is None


def test_the_spec_reference_is_the_stored_runs():
    from scripts import x47_anatomy as A

    for t in D.TARGETS:
        if not (A.RESULTS / D.OURS[t] / "outcomes.jsonl").exists():
            pytest.skip("the stored 47.8 runs are not here")
        ref = D.reference(t)
        assert {w: ref[w] for w in ("lookup", "recall")} == D.REFERENCE[t]
        assert ref["matches_verdict"] is not False


# ---- planted runs: the result, the seal, the verdict and the view -------------------------------------------------


def planted_run(root, target="qwen3.5-9b", ends=(14, 12), strata=D.STRATA, complete=True, gate_pass=True):
    """40 passages, 10 bridge entities, half fact-first: the lookup switches at every layer <= ends[0] (fact-after only
    on even passages), the recall at every layer <= ends[1]; without J++ the recall loses the odd passages."""
    src = root / D.RUNS[target]
    src.mkdir(parents=True)
    layers = list(D.LAYERS[target])
    z1 = {"run": "z1", "pass": gate_pass, "org_read_accuracy": {"K": 0.9, "M": 0.8}, "cases": 50, "eligible": 45,
          "chosen": 40, "sets": {"s": 40}, "strata": {s: 20 for s in D.STRATA}}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layers": layers, "z1": z1,
                                                   "n_layers": 32, "complete": complete}))  # fmt: skip
    rows, cases = [], []
    for i in range(40):
        st = D.STRATA[i // 20]
        if st not in strata:
            continue
        base = {"scene": f"p{i:02d}", "set": "s", "entity": f"e{i % 10}", "cf_entity": "x", "stratum": st}
        cases.append({**base, "bridge": base["entity"], "cf_bridge": "x", "answer": "A", "cf_answer": "B",
                      "readers": {w: {"id": f"{w}{i}", "pos": 1, "ids": {"org": [1, 2, 3], "alt": [1, 5, 3]}} for w in D.READERS}})  # fmt: skip
        for w in D.READERS:
            rows.append(
                {**base, "reader": w, "layer": None, "arm": "none", "route": "original", "top": 7, "switched": 0}
            )
            for la in layers:
                for a in D.ARMS:
                    on = la <= ends[0] and (st == "fact-first" or i % 2 == 0) if w == "K" else la <= ends[1]
                    if w == "M" and a == "no_jpp" and i % 2:
                        on = False
                    rows.append({**base, "reader": w, "layer": la, "arm": a, "route": "switch" if on else "original",
                                 "top": 9 if on else 7, "switched": int(on)})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "cases.jsonl", cases)
    return src.name


@pytest.fixture
def planted(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    ref = {"run": "ours", "verdict": None, "matches_verdict": None, "rates": {}, "lookup": 16, "recall": 14,
           "zach": {"lookup": D.zach_beside({16: 0.5}), "recall": D.zach_beside({14: 0.5})}}  # fmt: skip
    monkeypatch.setattr(D, "reference", lambda t: ref)
    return tmp_path


def test_planted_rule_holds_and_strata_and_losses(planted):
    m = D.model_result(planted_run(planted), n_boot=200)
    assert m["status"] == "tested" and m["n"] == 40 and not m["partial"]
    assert m["ends"]["pooled"] == {"lookup": 14, "recall": 12} and m["rule"]["holds"]
    assert m["rule"]["per_reader"]["lookup"]["diff"] == -2 and m["reference_matches_spec"]
    c = m["cells"]["12"]
    assert c["lookup"]["switch"][0] == 0.75 and c["lookup"]["strata"]["fact-first"]["switch"][0] == 1.0
    assert c["lookup"]["strata"]["fact-after"]["switch"][0] == 0.5 and c["lookup"]["loss"]["excess"][0] == 0.0
    assert c["recall"]["loss"]["excess"][0] == 0.5 and c["recall"]["loss_subspace"]["excess"][0] == 0.5
    assert m["cells"]["16"]["lookup"]["switch"][0] == 0.0 and not m["cells"]["16"]["lookup"]["interpretable"]
    assert m["zach"]["his_passages"]["lookup"] == {"first": 2, "last": 14, "his_window": [4, 20], "gone_by_25": True}


def test_planted_rule_fails_partial_and_gate(planted):
    m = D.model_result(planted_run(planted, ends=(22, 12)), n_boot=50)
    assert not m["rule"]["holds"] and m["rule"]["per_reader"]["lookup"]["diff"] == 6
    (planted / D.RUNS["qwen3.5-9b"]).rename(planted / "old")
    m = D.model_result(planted_run(planted, ends=(14, 12), strata=("fact-first",), complete=False), n_boot=50)
    assert m["partial"] and m["decided_on"].startswith("fact-first only") and m["strata"] == ["fact-first"]
    assert m["rule"]["holds"]
    m = D.model_result(planted_run(planted, target="qwen3.6-27b", gate_pass=False), n_boot=50)
    assert m["status"].startswith("not tested") and not m["reference_matches_spec"]  # planted ref vs the 27B's
    assert D.model_result("x51_5_nothing")["status"] == "pending"


def test_dan_answer_reads_only_the_q51_5_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q51.4** x\n\nDan: travels 60%\n\n**Q51.5** (51.5) The anatomy by depth ... P(yes) per model: 9B / 27B."
              "\n\nDan:{}\n\n**Q51.6** y\n\nDan: yes\n")  # fmt: skip
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert D.dan_answer() == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" 9B 70%")))
    assert D.dan_answer() == "9B 70%"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" 9B 70%\nDan (27B): 55%\n- because ...")))
    assert D.dan_answer() == "9B 70%\nDan (27B): 55%\n- because ..."


def test_the_committed_predictions_file_has_the_q51_5_block():
    text = D.subprocess.run(["git", "show", f"HEAD:{D.PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{D.QUESTION}**" in text and isinstance(D.dan_answer(), str)


def ours_blob(layers):
    cell = lambda v: [v, max(0.0, v - 0.1), min(1.0, v + 0.1)]  # noqa: E731
    return {"folder": "planted", "layers": layers, "cells": {str(la): {
        "lookup": {"n": 5, "share": {"whole": {"identity": cell(0.6), "position": cell(0.3)}}, "switch": {"whole": cell(0.9)},
                   "loss": {"J": {"excess": cell(0.05)}}},
        "recall": {"switch": {"whole": cell(0.7)}, "loss": {"J": {"excess": cell(0.4)}}}} for la in layers}}  # fmt: skip


def test_verdict_and_view_are_sealed_then_written(planted, monkeypatch):
    run = planted_run(planted)
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_verdict([run], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        D.stage_view([run], decode=lambda ids: "")
    assert [p.name for p in planted.iterdir()] == [run]  # nothing written while sealed
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "9B 70%; 27B 55%")
    monkeypatch.setattr(D, "ours_verdict", lambda t: ours_blob([2, 4, 6]))
    out = D.stage_verdict([run, D.RUNS["qwen3.6-27b"]], n_boot=50)
    md = (out / "verdict.md").read_text()
    assert "Dan: 9B 70%; 27B 55%" in md and "| qwen3.5-9b | qwen35_9b_x51_5 | tested | 40 |" in md
    assert "L14 / L16 (-2) | L12 / L14 (-2) | the same read window as ours |" in md
    assert "| qwen3.6-27b | x51_5_27b | pending" in md and (out / "x51_5_depth.png").exists()
    blob = json.loads((out / "x51_5.json").read_text())
    assert blob["dan"] == "9B 70%; 27B 55%" and blob["models"][0]["rule"]["holds"]
    view = (D.stage_view([run], decode=lambda ids: "".join(f"<{i}>" for i in ids)) / "view.md").read_text()
    assert view.count("### p") == D.N_PROMPTS and "<1>⟦<2>⟧<3>" in view and "<1>⟦<5>⟧<3>" in view
    for a in ("none", *D.ARMS):
        assert f"### arm {a}: {D.N_ROWS} random rows" in view


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


@pytest.fixture
def fake_run(tok, z1_built, tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from scripts import x47_anatomy as A

    if pins.TARGET not in D.TARGETS:
        pytest.skip("51.5 runs on the 9B and the 27B")
    fake = FakeModel(tok, n_layers=40)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "z1")
    monkeypatch.setattr(A, "RESULTS", tmp_path / "ours")
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x51")
    monkeypatch.setattr(D, "LAYERS", {pins.TARGET: (2, 4)})
    plant_z1(tmp_path / "z1", pins.TARGET, z1_built, [0, 1, 2, 3])
    return fake


def test_run_stage_end_to_end_on_a_fake_model(fake_run, z1_built):
    import torch

    from scripts import statement_positions as SP
    from scripts import x47_anatomy as A

    out = D.stage_run(f"{pins.RUN_PREFIX}fake_x51_5", "test")
    m = json.loads((out / "manifest.json").read_text())
    assert m["complete"] and m["strata_done"] == list(D.STRATA) and m["items"] == 4 and not m["split"]
    assert m["reference"] == {"ours": D.OURS[pins.TARGET], **D.REFERENCE[pins.TARGET]} and "sealed" in m
    assert not any(p.name.startswith(("verdict", "x51_5")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    per = 1 + 2 * len(D.ARMS)
    assert len(rows) == 4 * len(D.READERS) * per
    assert [r["stratum"] for r in rows[: 2 * 2 * per]] == ["fact-first"] * (2 * 2 * per)  # fact-first rows first
    assert json.loads((out / "gate.json").read_text())["alignment"]["same"] == 4
    # the first item read (fact-first): its K reader's arms at L2, from h_S - h_O at the patch token
    c = next(c for c in z1_built if c["stratum"] == "fact-first")
    rd = c["readers"]["K"]
    _, edits = next((s, e) for s, e in fake_run.calls if len(e) == per and s == len(rd["ids"]["org"]))
    assert edits[0] == {} and edits[1][2].positions == [rd["pos"]]
    h = {v: fake_run.run(torch.tensor([rd["ids"][v]]), record=(2,))[1][2] for v in ("org", "alt")}
    x = (h["alt"][rd["pos"]] - h["org"][rd["pos"]])[None]
    assert torch.allclose(edits[1][2].delta, x, atol=1e-5)
    jdic = FakeLens(None, "jpp").vectors(2, fake_run.letter_token_ids())
    part = X.fit(jdic, x, X.K_MAIN, "signed")
    assert torch.allclose(edits[2][2].delta, x - part, atol=1e-4)  # no_jpp
    share = part.norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2
    ratoms = SP.random_subspace_part(x, share, A.random_atoms_basis(jdic, D.ATOMS_SEED + 2))
    assert torch.allclose(edits[4][2].delta, x - ratoms, atol=1e-4)  # no_jpp_ratoms: 47.8's random lens atoms
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 4 * 2 * len(D.READERS) and all(abs(n["share_ratoms"] - n["share_jpp"]) < 0.2 for n in norms)


def test_a_failed_fact_after_stratum_keeps_the_fact_first_rows(fake_run, monkeypatch):
    real = D.reads

    def reads(model, cases, arms, layers, ws, desc):
        if cases[0]["stratum"] == "fact-after":
            raise RuntimeError("planted failure")
        return real(model, cases, arms, layers, ws, desc)

    monkeypatch.setattr(D, "reads", reads)
    name = f"{pins.RUN_PREFIX}fake_x51_5"
    with pytest.raises(RuntimeError, match="planted"):
        D.stage_run(name, "test")
    out = D.RESULTS / name
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert rows and {r["stratum"] for r in rows} == {"fact-first"}
    assert not json.loads((out / "manifest.json").read_text()).get("complete")


def test_the_split_flag_reads_z3_items_by_layer(fake_run, monkeypatch):
    monkeypatch.setattr(Z, "N_ITEMS", 2)
    monkeypatch.setattr(Z, "competence", lambda model, cases, ws: [
        {"scene": c["scene"], "set": c["set"], "reader": w, "variant": v, "greedy": "x", "right": True,
         "read_right": True, "top": 0} for c in cases for w in c["readers"] for v in ("org", "alt")])  # fmt: skip
    out = D.stage_run(f"{pins.RUN_PREFIX}fake_x51_5", "test", split=True)
    m = json.loads((out / "manifest.json").read_text())
    assert m["split"] and m["split_gate"]["chosen"] == 2
    rows = X.read_jsonl(out / "split_outcomes.jsonl")
    assert len(rows) == 2 * (1 + 2) and {r["route"] for r in rows} <= set(D.SPLIT_ROUTES)
    assert [r["layer"] for r in rows[:3]] == [None, 2, 4]
