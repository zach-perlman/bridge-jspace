"""Batch 50, Z1 and Z2 (scripts/x50_zach.py): the K / M pairing, the counterfactual prompts on Zach's v2 passages (only
the pointer's name / the description changes, the patch token at one index), the leak filter, the order strata, the
rules on planted numbers, the seal, and the run stage end to end on a tiny fake model (CPU). No real model."""

import json
import math
from types import SimpleNamespace

import pytest

from scripts import x0_necessity as X
from scripts import x50_zach as Z
from tests.test_x47_cue import FakeLens, FakeModel


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


@pytest.fixture(scope="module")
def z1_pairs():
    ps, why = Z.load_pairs(Z.SETS[0], "z1")
    assert not why and len(ps) == 358
    return ps


# ---- pairing and passages -----------------------------------------------------------------------------------------


def item(word: str, scene: str, **kw) -> dict:
    base = {"id": f"{word}-{scene}", "module": "facts", "word": word, "scene": scene, "question": "q", "answer": "a",
            "bridge": "b", "entities": ["b", "c"], "wording": 0, "relation": "countries", "start_desc": "d"}  # fmt: skip
    return {**base, **kw}


def test_pairs_join_the_k_and_m_items_of_one_scene():
    items = [item("PK", "s1"), item("PM", "s1"), item("PK", "s2"), item("PM", "s3"), item("PP", "s1"),
             item("PK", "s4"), item("PM", "s4", answer="z"), item("MK", "s5"), item("MM", "s5")]  # fmt: skip
    ps, why = Z.pairs(items, "z1")
    assert [p[Z.LOOKUP]["id"] for p in ps] == ["PK-s1"] and ps[0][Z.RECALL]["id"] == "PM-s1"
    assert why == {"a reader is missing": 2, "the K and M items differ in question, answer, bridge or entities": 1}
    ps2, _ = Z.pairs(items, "z2")
    assert [(p[Z.LOOKUP]["word"], p[Z.RECALL]["word"]) for p in ps2] == [("MK", "MM")]


def test_k_and_m_passages_share_the_pointer_and_differ_in_the_final_hop(z1_pairs):
    for p in z1_pairs[:40]:
        k, m = p[Z.LOOKUP], p[Z.RECALL]
        sent = Z.pointer(k, k["bridge"])
        assert k["context"].count(sent) == 1 and m["context"].count(sent) == 1
        assert Z.kfact(k["relation"], k["wording"], k["bridge"]) in k["context"]
        assert k["answer"] not in m["context"]  # the M passage does not state the bridge's fact


def test_leak_filter_drops_answers_and_derived_words():
    assert Z.leaks("the country whose people speak French", ["French"]) == ["French"]
    assert Z.leaks("the country around France's border", ["French"]) == ["France"]  # DERIV: French -> France
    assert Z.leaks("the city that hosted the 1992 Olympics", ["Spain"]) == []
    assert Z.leaks("a Frenchman's dish", ["French"]) == []  # whole words only
    assert Z.leaks("the poet of south america", ["South America"]) == ["South America", "America"]  # case-insensitive


def test_z1_counterfactual_changes_only_the_pointers_name(tok, z1_pairs):
    cases, why = Z.z1_cases(tok, z1_pairs[:60])
    assert len(cases) + sum(why.values()) == 60 and len(cases) >= 30
    for c in cases:
        assert c["cf_bridge"] != c["bridge"] and c["cf_answer"] == Z.fact(c["relation"], c["cf_bridge"]) != c["answer"]
        for r, rd in c["readers"].items():
            o, s = rd["context"], rd["cf_context"]
            k = next(p for p in z1_pairs if p[Z.LOOKUP]["scene"] == c["scene"])[r]
            sent = Z.pointer(k, c["bridge"])
            assert s == o.replace(sent, Z.pointer(k, c["cf_bridge"])) and rd["question"] == rd["cf_question"]
            org, alt, pos = rd["ids"]["org"], rd["ids"]["alt"], rd["pos"]
            assert len(org) == len(alt)
            changed = [i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b]
            assert pos in changed and all(rd["span"][0] <= i <= pos for i in changed)
            assert tok.decode(org[rd["span"][0] : pos + 1]).strip().endswith(c["bridge"].split()[-1])
            assert tok.decode(alt[rd["span"][0] : pos + 1]).strip().endswith(c["cf_bridge"].split()[-1])
            assert rd["tok_A"] != rd["tok_b"]
        lu = c["readers"][Z.RECALL]["lure"]
        assert lu is not None and lu != c["cf_answer"]  # the M passage's fictional value for the other entity
        assert c["readers"][Z.LOOKUP]["lure"] is None


def test_z1_order_strata_follow_the_sentence_order(tok, z1_pairs):
    cases, _ = Z.z1_cases(tok, z1_pairs[:60])
    assert {c["stratum"] for c in cases} == {"fact-first", "fact-after"}
    for c in cases:
        k = c["readers"][Z.LOOKUP]
        ctx = k["context"]
        src = next(p for p in z1_pairs if p[Z.LOOKUP]["scene"] == c["scene"])[Z.LOOKUP]
        first = ctx.index(Z.kfact(c["relation"], c["wording"], c["bridge"])) < ctx.index(Z.pointer(src, c["bridge"]))
        assert (c["stratum"] == "fact-first") == first == c["order"]["bridge_fact_first"]


def test_z2_counterfactual_changes_only_the_description(tok):
    ps, _ = Z.load_pairs(Z.SETS[0], "z2")
    opts, _ = Z.z2_options(tok, ps[:80])
    assert opts
    for _, cs in opts:
        for c in cs:
            assert c["cf_desc"] in [d for d, _ in Z.descriptions(c["relation"], c["cf_bridge"])]
            assert not Z.leaks(c["cf_desc"], [c["answer"], c["cf_answer"]])
            for rd in c["readers"].values():
                assert rd["context"] == rd["cf_context"] and rd["cf_question"] != rd["question"]
                org, alt, pos = rd["ids"]["org"], rd["ids"]["alt"], rd["pos"]
                changed = [i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b]
                assert changed and all(rd["span"][0] <= i <= pos for i in changed)
                assert c["desc"].split()[-1].lower().endswith(tok.decode(org[pos : pos + 1]).strip().lower())
                assert c["bridge"] not in rd["question"]  # never named in the question
    # the competence step keeps O's description and picks the first kept S option
    p, cs = opts[0]
    k = p[Z.LOOKUP]
    kept = {f"{k['relation']}|{k['bridge']}|{k['start_desc']}": {"kept": True}}
    assert Z.z2_choose([(p, cs)], kept)[0] == []
    kept[f"{cs[-1]['relation']}|{cs[-1]['cf_bridge']}|{cs[-1]['cf_desc']}"] = {"kept": True}
    chosen = Z.z2_choose([(p, cs)], kept)[0][0]
    assert (chosen["cf_bridge"], chosen["cf_desc"]) == (cs[-1]["cf_bridge"], cs[-1]["cf_desc"])


def test_desc_table_keeps_descriptions_at_the_bar():
    rows = [{"relation": "people", "entity": e, "desc": "d", "right": i < k} for e, k in (("Kant", 9), ("Bach", 8))
            for i in range(10)]  # fmt: skip
    t = Z.desc_table(rows)
    assert t["people|Kant|d"]["kept"] and not t["people|Bach|d"]["kept"] and t["people|Bach|d"]["share"] == 0.8
    assert Z.says("Wolfgang Amadeus Mozart.", Z.alts("people", "Mozart"))
    assert Z.says("Eiffel Tower", ["the Eiffel Tower", "Eiffel Tower"]) and not Z.says("\n", ["Kant"])


# ---- rules on planted numbers -------------------------------------------------------------------------------------


def test_main_rule_bars():
    nan = float("nan")
    assert Z.main_rule("z1", 0.10, 0.30) == "the split holds on his passages"
    assert Z.main_rule("z1", 0.20, 0.50) == "the lookup follows the lens here"
    assert Z.main_rule("z1", 0.15, 0.50) == "in between" and Z.main_rule("z1", 0.05, 0.29) == "in between"
    assert Z.main_rule("z2", 0.0, 0.4).startswith("(a) ") and Z.main_rule("z2", 0.3, 0.0).startswith("(a') ")
    assert Z.main_rule("z2", 0.12, 0.4).startswith("(d) ") and Z.main_rule("z2", nan, 0.4).startswith("can't tell")


def test_order_rule_bars():
    assert Z.order_rule([0.6, 0.5, 0.7], [0.3, 0.2, 0.4])["replicates"]
    r = Z.order_rule([0.59, 0.5, 0.7], [0.3, 0.2, 0.4])
    assert not r["replicates"] and r["separate"]
    assert Z.order_rule([0.2, 0.1, 0.3], [0.0, 0.0, 0.0]) == {"replicates": True, "ratio": math.inf, "separate": True}
    assert not Z.order_rule([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])["replicates"]


def planted(tmp_path, monkeypatch, *, lookup_loss=0.0, gate_pass=True, part="z1", target="qwen3.5-9b"):
    """120 passages, 30 bridge entities. Both readers switch under the whole change; without J++ the K reader loses
    `lookup_loss` of them and the M reader loses the even passages; fact-first passages (i < 60) switch on K, half of the
    fact-after ones do not (the K whole-change shares 1.0 vs 0.5)."""
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    run = Z.RUNS[part][target]
    src = tmp_path / run
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layers": [12]}))
    order = [[Z.SETS[0], f"s{i:03d}"] for i in range(120)]
    (src / "gate.json").write_text(json.dumps({"pass": gate_pass, "chosen": 120, "eligible": 150, "cases": 300,
                                               "org_read_accuracy": {"K": 0.9, "M": 0.85 if gate_pass else 0.7},
                                               "order": order}))  # fmt: skip
    rows, cases = [], []
    n_lose = round(120 * lookup_loss)
    for i in range(120):
        s = f"s{i:03d}"
        base = {"scene": s, "set": Z.SETS[0], "entity": f"e{i % 30}", "cf_entity": "x", "layer": 12,
                "stratum": "fact-first" if i < 60 else "fact-after"}  # fmt: skip
        for a in ("none", *Z.ARMS):
            k_sw = a != "none" and not (a == "no_jpp" and i < n_lose) and not (i >= 60 and i % 2)
            m_sw = a != "none" and not (a == "no_jpp" and i % 2 == 0)
            rows.append({**base, "reader": "K", "arm": a, "switched": int(k_sw), "route": "switch" if k_sw else "original",
                         "top": 1})  # fmt: skip
            rows.append({**base, "reader": "M", "arm": a, "switched": int(m_sw), "route": "switch" if m_sw else "lure",
                         "top": 2})  # fmt: skip
        cases.append({"set": Z.SETS[0], "scene": s, "bridge": f"e{i % 30}", "cf_bridge": "x", "answer": "A",
                      "cf_answer": "B", "stratum": base["stratum"], "desc": "d", "cf_desc": "e",
                      "readers": {w: {"id": f"{w}-{s}", "answer": "A", "cf_answer": "B", "lure": None, "pos": 2,
                                      "ids": {"org": [1, 2, 3, 4], "alt": [1, 2, 5, 4]}} for w in Z.READERS}})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "cases.jsonl", cases)
    return run


def test_planted_split_holds_and_the_order_pattern_replicates(tmp_path, monkeypatch):
    m = Z.model_result("z1", planted(tmp_path, monkeypatch), n_boot=200)
    lr = m["layer_results"][12]
    assert m["status"] == "tested" and lr["n"] == 120 and lr["entities"] == 30
    assert lr["lookup"]["excess"][0] == 0.0 and lr["recall"]["excess"][0] == 0.5 and lr["gap"][0] == 0.5
    assert lr["verdict"] == "the split holds on his passages"
    o = lr["order"]
    assert o["strata"]["fact-first"]["whole_switch"][0] == 1.0 and o["strata"]["fact-after"]["whole_switch"][0] == 0.5
    assert o["replicates"] and o["ratio"] == 2.0 and lr["hard_read"].startswith("no hard-read flag")
    assert m["beside"]["full"]["paper10"]["joined"] == 0  # planted ids are not his


def test_planted_lookup_follows_the_lens_and_a_failed_gate(tmp_path, monkeypatch):
    m = Z.model_result("z2", planted(tmp_path, monkeypatch, lookup_loss=0.25, part="z2"), n_boot=200)
    lr = m["layer_results"][12]
    assert lr["lookup"]["excess"][0] == pytest.approx(0.25 / 0.75) and lr["verdict"].startswith("(a') ")
    assert "order" not in lr and "swap" in m["beside"] and "question" in m["beside"]
    (tmp_path / Z.RUNS["z2"]["qwen3.5-9b"]).rename(tmp_path / "old")
    m = Z.model_result("z2", planted(tmp_path, monkeypatch, gate_pass=False, part="z2"), n_boot=50)
    assert m["status"].startswith("not tested (gate")
    assert Z.model_result("z1", "muse30_x50_z1")["status"] == "pending"


# ---- the seal -----------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_its_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q50.1** (Z1) ...\n\nDan:{}\n\n**Q50.2** (Z2) ...\n\nDan:{}\n\n**Q50.3** z\n\nDan: w\n"
    monkeypatch.setattr(Z.subprocess, "run", fake_git(blocks.format("", "")))
    assert Z.dan_answer("Q50.1") == "" and Z.dan_answer("Q50.2") == ""
    monkeypatch.setattr(Z.subprocess, "run", fake_git(blocks.format(" split holds 70%", "")))
    assert Z.dan_answer("Q50.1") == "split holds 70%" and Z.dan_answer("Q50.2") == ""


def test_verdict_and_view_are_sealed_then_written(tmp_path, monkeypatch):
    run = planted(tmp_path, monkeypatch)
    monkeypatch.setattr(Z, "dan_answer", lambda q: "")
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_verdict("z1", [run], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_view("z1", [run], decode=lambda ids: "")
    assert [p.name for p in tmp_path.iterdir()] == [run]  # nothing written while sealed
    monkeypatch.setattr(Z, "dan_answer", lambda q: "split holds 60%" if q == "Q50.1" else "")
    out = Z.stage_verdict("z1", [run], n_boot=50, decode=lambda ids: "".join(f"<{i}>" for i in ids))
    md = (out / "z1.md").read_text()
    assert "split holds 60%" in md and "| qwen3.5-9b | qwen35_9b_x50_z1 | tested | 12 | 120 (30) |" in md
    view = (out / "view.md").read_text()
    assert view.count("### s") == Z.N_VIEW and "<1><2>⟦<3>⟧<4>" in view and "⟦<5>⟧" in view
    assert (out / "z1_beside.png").exists() and json.loads((out / "z1.json").read_text())["dan"] == "split holds 60%"
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_verdict("z2", [run], n_boot=50)


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


@pytest.mark.parametrize("part", Z.PARTS)
def test_run_stage_end_to_end_on_a_fake_model(tok, tmp_path, monkeypatch, part):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    fake = FakeModel(tok, n_layers=40)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    monkeypatch.setattr(Z, "N_ITEMS", 3)
    # cut the sets to a few passages (the fake model cannot answer: the competence steps are planted right)
    real_load = Z.load_pairs
    monkeypatch.setattr(Z, "load_pairs", lambda s, p: (real_load(s, p)[0][:25], {}))
    monkeypatch.setattr(Z, "desc_competence", lambda model, prompts: [
        {**{k: q[k] for k in ("relation", "entity", "desc", "template", "instruction")}, "greedy": q["entity"],
         "right": True} for q in prompts])  # fmt: skip
    monkeypatch.setattr(Z, "competence", lambda model, cases, ws: [
        {"scene": c["scene"], "set": c["set"], "reader": w, "variant": v, "greedy": "x", "right": True,
         "read_right": i % 4 != 3, "top": 0} for i, c in enumerate(cases) for w in Z.READERS for v in ("org", "alt")])  # fmt: skip
    out = Z.stage_run(f"{pins.RUN_PREFIX}fake_x50_{part}", part)
    m = json.loads((out / "manifest.json").read_text())
    gate = json.loads((out / "gate.json").read_text())
    assert (
        m["items"] == 3 and m["layers"] == list(Z.LAYERS[pins.TARGET]) and "sealed" in m and m["rule"] == Z.RULE[part]
    )
    assert gate["chosen"] == 3 and gate["sets_used"] == [Z.SETS[0]] and not gate["pass"]  # 3 of 4 read right: < 0.80
    assert not any(p.name.startswith(("verdict", "z1", "z2")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 3 * len(Z.READERS) * (1 + len(Z.ARMS)) * len(Z.LAYERS[pins.TARGET])
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(out / "cases.jsonl")}
    # the whole arm of the first chosen passage's K reader = h_S - h_O at its patch token, added there on O
    la = Z.LAYERS[pins.TARGET][0]
    c = cases[tuple(gate["order"][0])]
    rd = c["readers"]["K"]
    _, edits = next((s, e) for s, e in fake.calls if len(e) == 1 + len(Z.ARMS) and s == len(rd["ids"]["org"]))
    whole = edits[1][la]
    assert whole.positions == [rd["pos"]] and edits[0] == {}
    h = {v: fake.run(torch.tensor([rd["ids"][v]]), record=(la,))[1][la] for v in ("org", "alt")}
    assert torch.allclose(whole.delta[0], h["alt"][rd["pos"]] - h["org"][rd["pos"]], atol=1e-5)
    if part == "z2":
        assert (out / "desc_competence.jsonl").exists()
