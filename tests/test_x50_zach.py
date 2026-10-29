"""Batch 50, Z1, Z2 and Z3 (scripts/x50_zach.py): the K / M pairing, the counterfactual prompts on Zach's v2 passages
(only the pointer's name / the description changes, the patch token at one index; Z3: B's and C's fact sentences swap
slots, B's with an unstated value), the leak filter, the order strata, the route classification, the rules on planted
numbers, the seal, and the run stage end to end on a tiny fake model (CPU). No real model."""

import functools
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


def test_z1p_reads_the_made_up_facts_of_the_p_passage(tok):
    """Z1-P (Dan's morning brief, 29 Oct): Z1 on the P items: the lookup reads the PP passage (made-up values stated for
    every entity), the recall PM; O's and S's lookup answers are the made-up values its passage states, the recall's the
    true facts; the order strata follow the P passage's own fact sentences; Z1's rule verbatim; the committed L only."""
    ps, why = Z.load_pairs(Z.SETS[0], "z1p")
    assert not why and len(ps) == 358 and all(p[Z.LOOKUP]["word"] == "PP" and p[Z.RECALL]["word"] == "PM" for p in ps)
    cases, drops = Z.z1_cases(tok, ps[:60], "z1p")
    assert len(cases) + sum(drops.values()) == 60 and len(cases) >= 30
    for c in cases:
        k, m = c["readers"][Z.LOOKUP], c["readers"][Z.RECALL]
        src = next(p for p in ps if p[Z.LOOKUP]["scene"] == c["scene"])
        rel, w = c["relation"], c["wording"]
        assert k["answer"] == src[Z.LOOKUP]["answer"] == Z.lure(rel, w, c["bridge"], k["context"])
        assert k["cf_answer"] == Z.lure(rel, w, c["cf_bridge"], k["context"]) != k["answer"]
        assert m["answer"] == Z.fact(rel, c["bridge"]) and m["cf_answer"] == Z.fact(rel, c["cf_bridge"])
        assert k["tok_A"] != k["tok_b"] and m["tok_A"] != m["tok_b"] and k["lure"] is None
        ptr = k["context"].index(Z.pointer(src[Z.LOOKUP], c["bridge"]))
        first = k["context"].index(Z.pfact(rel, w, c["bridge"], k["answer"])) < ptr
        assert (c["stratum"] == "fact-first") == first
    assert Z.RULE["z1p"] == Z.RULE["z1"] and "z1p" not in Z.RUNS
    assert set(Z.COVERAGE_RUNS["z1p"]) == {
        "qwen3.5-9b",
        "qwen3.6-27b",
        "nemotron-3.5-lightning",
        "muse-glimmer-30b",
        "qwen3.5-122b-a10b",
    }


def test_z2p_reads_mp_with_the_made_up_facts_and_mm_beside(tok):
    """53.1b (batch 53): Z2's design on his M-start passages with the P final: the lookup reads MP (the question
    describes the bridge; O's and S's answers are the made-up values its passage states), the recall MM (true facts);
    S's question is each reader's own template (q2P / q2M) with S's description; the leak filter checks every answer of
    both readers; the committed L only; no rule of its own (x51_answer reads it)."""
    ps, why = Z.load_pairs(Z.SETS[0], "z2p")
    assert not why and len(ps) == 358 and all(p[Z.LOOKUP]["word"] == "MP" and p[Z.RECALL]["word"] == "MM" for p in ps)
    for p in ps:
        for r in Z.READERS:
            assert Z.question(p[r], p[r]["start_desc"]) == p[r]["question"]
    opts, _ = Z.z2_options(tok, ps[:80], "z2p")
    assert len(opts) >= 10
    for p, cs in opts:
        for c in cs:
            k, m = c["readers"][Z.LOOKUP], c["readers"][Z.RECALL]
            rel, w = c["relation"], c["wording"]
            assert k["answer"] == p[Z.LOOKUP]["answer"] == Z.lure(rel, w, c["bridge"], k["context"])
            assert k["cf_answer"] == Z.lure(rel, w, c["cf_bridge"], k["context"]) != k["answer"]
            assert m["answer"] == Z.fact(rel, c["bridge"]) and m["cf_answer"] == Z.fact(rel, c["cf_bridge"])
            assert k["cf_question"] == Z.question(p[Z.LOOKUP], c["cf_desc"]) != k["question"]
            assert m["cf_question"] == Z.question(p[Z.RECALL], c["cf_desc"]) != m["question"]
            assert not Z.leaks(c["cf_desc"], [k["answer"], k["cf_answer"], m["answer"], m["cf_answer"]])
            for rd in (k, m):
                org, alt, pos = rd["ids"]["org"], rd["ids"]["alt"], rd["pos"]
                changed = [i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b]
                assert changed and all(rd["span"][0] <= i <= pos for i in changed) and rd["tok_A"] != rd["tok_b"]
            assert k["lure"] is None and m["lure"] is not None
    assert "z2p" not in Z.RUNS and set(Z.COVERAGE_RUNS["z2p"]) == {"qwen3.5-9b", "qwen3.6-27b"}
    assert "z2p" not in Z.PARTS and "z2p" in Z.RUN_PARTS  # the default plan's parts unchanged
    with pytest.raises(AssertionError, match="no rule of its own"):
        Z.require_answer("z2p")


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

    blocks = (
        "**Q50.1** (Z1) ...\n\nDan:{}\n\n**Q50.2** (Z2) ...\n\nDan:{}\n\n**Q50.3** z\n- Position >= 0.2\n\nDan: w\n"
    )
    monkeypatch.setattr(Z.subprocess, "run", fake_git(blocks.format("", "")))
    assert Z.dan_answer("Q50.1") == "" and Z.dan_answer("Q50.2") == "" and Z.dan_answer("Q50.3") == "w"
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


@pytest.mark.parametrize("part", ["z1", "z2", "z2p"])
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
    planted = sum(i % 4 != 3 for i in range(gate["cases"])) / gate["cases"]  # 3 of 4 read right (z2p: few cases)
    assert gate["chosen"] == 3 and gate["sets_used"] == [Z.SETS[0]] and gate["pass"] == (planted >= Z.GATE)
    assert part == "z2p" or not gate["pass"]
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
    if part in Z.Z2_LIKE:
        assert (out / "desc_competence.jsonl").exists()


# ---- Z3: routes on scattered facts ----------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def z3_built(tok):
    ps, _ = Z.load_pairs(Z.SETS[0], "z3")
    cases, why = Z.z3_cases(tok, ps)
    assert len(cases) + sum(why.values()) == len(ps) == 358
    return ps, cases, why


def test_swap_slots_puts_c_in_bs_slot_and_b_with_its_new_value_in_cs():
    ctx = "Intro. B is b. Filler. C is c. Iris picked A."
    assert Z.swap_slots(ctx, "B is b.", "C is c.", "B is e.") == "Intro. C is c. Filler. B is e. Iris picked A."
    assert Z.swap_slots("C is c. B is b.", "B is b.", "C is c.", "B is e.") == "B is e. C is c."
    with pytest.raises(AssertionError):
        Z.swap_slots("B is b. B is b. C is c.", "B is b.", "C is c.", "B is e.")


def masked(text: str, sents: list[str], ptr: str) -> str:
    """The text with each fact sentence replaced by '#' and the pointer sentence by 'P'."""
    return functools.reduce(lambda u, x: u.replace(x, "#"), sents, text).replace(ptr, "P")


def test_z3_items_follow_the_design(tok, z3_built):
    ps, cases, why = z3_built
    assert len(cases) >= 15 and why["not three entities (level 1)"] == 179
    assert why["a fact sentence comes after the pointer sentence"] > 0
    by = {p[Z.LOOKUP]["scene"]: p for p in ps}
    for c in cases:
        k = by[c["scene"]][Z.LOOKUP]
        rel, w, A, B, C, v = c["relation"], c["wording"], c["bridge"], c["cf_bridge"], c["slot_of"], c["values"]
        assert k["level"] == 0 and sorted(k["entities"]) == sorted([A, B, C]) and Z.facts_first(k)
        assert (v["original"], v["identity"], v["position"]) == tuple(Z.fact(rel, e) for e in (A, B, C))
        assert len(set(v.values())) == 4 and v["value"] in Z.tables().vocab(rel)
        assert not Z.leaks(k["context"] + "\n" + k["question"], [v["value"]])  # the new value is unstated in O
        assert list(c["readers"]) == [Z.LOOKUP]
        rd = c["readers"][Z.LOOKUP]
        o, s, s0 = rd["context"], rd["cf_context"], rd["c0_context"]
        assert o == k["context"] and rd["question"] == rd["cf_question"] == k["question"]
        p_o, p_s = Z.pointer(k, A), Z.pointer(k, B)
        fa, fb, fc = (Z.kfact(rel, w, e) for e in (A, B, C))
        fb_new = Z.kfact(rel, w, B, v["value"])
        assert v["value"] in fb_new and s0 == o.replace(p_o, p_s)
        # S: the pointer names B; C's sentence takes B's slot, B's (stating e) takes C's; nothing else moves
        slots_o = sorted([fa, fb, fc], key=o.index)
        slots_s = sorted([fa, fc, fb_new], key=s.index)
        assert slots_s == [{fa: fa, fb: fc, fc: fb_new}[x] for x in slots_o]
        assert all(s.index(x) < s.index(p_s) for x in slots_s)  # still every fact before the pointer
        assert masked(o, [fa, fb, fc], p_o) == masked(s, [fa, fc, fb_new], p_s)
        assert c["slots"] == {"A": slots_o.index(fa), "B": slots_o.index(fb), "C": slots_o.index(fc)}
        # tokens: one length, the patch token = the pointer name's last token, nothing after it changes
        org, pos = rd["ids"]["org"], rd["pos"]
        for var, name in (("alt", B), ("alt0", B)):
            alt = rd["ids"][var]
            assert len(alt) == len(org)
            changed = [i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b]
            assert changed and max(changed) <= pos
            if var == "alt0":
                assert min(changed) >= rd["span"][0]  # S0: only the name
            assert tok.decode(alt[rd["span"][0] : pos + 1]).strip().endswith(name.split()[-1])
        assert tok.decode(org[rd["span"][0] : pos + 1]).strip().endswith(A.split()[-1])
        assert rd["route_tokens"] == {r: Z.answer_tok(tok, v[r]) for r in ("original", "identity", "position", "value")}
        assert (rd["tok_A"], rd["tok_b"], rd["tok_b0"]) == (rd["route_tokens"]["original"], rd["route_tokens"]["value"],
                                                            rd["route_tokens"]["identity"])  # fmt: skip
        assert [g[0] for g in Z.golds(rd)] == ["org", "alt", "alt0"]
        assert [g[1] for g in Z.golds(rd)] == [v["original"], v["value"], v["identity"]]


def test_z3_route_classification_is_x6_routes(z3_built):
    from scripts import x6_routes as R

    assert R.ROUTES == Z.ROUTES
    rd = z3_built[1][0]["readers"][Z.LOOKUP]
    for r, t in rd["route_tokens"].items():
        assert R.classify(t, rd) == r
    assert R.classify(max(rd["route_tokens"].values()) + 1, rd) == "other"


def test_z3_rule_bars():
    nan = float("nan")
    r = Z.z3_rule(0.20, 0.05)
    assert r["clause"] == "the address exists in scattered-fact passages" and r["value_ok"] and r["position_ge_0_2"]
    assert r["follow_up_45d"]
    r = Z.z3_rule(0.05, 0.06)
    assert r["clause"].startswith("no position route in his layout") and not r["value_ok"] and not r["position_ge_0_2"]
    assert Z.z3_rule(0.19, 0.0)["clause"].startswith("in between") and not Z.z3_rule(0.19, 0.0)["follow_up_45d"]
    assert Z.z3_rule(nan, 0.0)["clause"].startswith("can't tell")


def planted_z3(tmp_path, monkeypatch, *, position=0.30, value=0.0, target="qwen3.5-9b", gate_pass=True):
    """100 passages, 25 bridge entities. C2 whole: the first `position` share answers C's fact, the next `value` share
    the new value, the next 40 B's fact (identity), the rest A's (original); every other arm and C0's arms the original,
    except C0 whole: identity on 60. The first 40 passages keep C's token span."""
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    run = Z.RUNS["z3"][target]
    src = tmp_path / run
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layers": [12]}))
    order = [[Z.Z3_SETS[0], f"s{i:03d}"] for i in range(100)]
    (src / "gate.json").write_text(json.dumps({"pass": gate_pass, "chosen": 100, "eligible": 100, "cases": 120,
                                               "org_read_accuracy": {"K": 0.9}, "order": order}))  # fmt: skip
    n_pos, n_val = round(100 * position), round(100 * value)
    rows, cases = [], []
    for i in range(100):
        s = f"s{i:03d}"
        bounds = (("position", n_pos), ("value", n_pos + n_val), ("identity", n_pos + n_val + 40), ("original", 101))
        whole = next(rt for rt, hi in bounds if i < hi)
        base = {"scene": s, "set": Z.Z3_SETS[0], "entity": f"e{i % 25}", "cf_entity": "x", "layer": 12, "reader": "K",
                "slot_aligned": i < 40}  # fmt: skip
        for cd in Z.Z3_CONDS:
            for a in ("none", *Z.ARMS):
                rt = {("C2", "whole"): whole, ("C0", "whole"): "identity" if i < 60 else "original"}.get(
                    (cd, a), "original"
                )
                rows.append({**base, "condition": cd, "arm": a, "route": rt, "switched": int(rt == "value"), "top": 7})
        cases.append({"set": Z.Z3_SETS[0], "scene": s, "bridge": f"e{i % 25}", "cf_bridge": "B", "slot_of": "C",
                      "answer": "a", "cf_answer": "e", "slot_aligned": i < 40,
                      "values": {"original": "a", "identity": "b", "position": "c", "value": "e"},
                      "readers": {"K": {"id": f"K-{s}", "answer": "a", "cf_answer": "e", "lure": None, "pos": 2,
                                        "ids": {"org": [1, 2, 3, 4], "alt": [1, 5, 6, 4], "alt0": [1, 2, 6, 4]}}}})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "cases.jsonl", cases)
    return run


def test_planted_z3_shares_and_rule(tmp_path, monkeypatch):
    m = Z.model_result("z3", planted_z3(tmp_path, monkeypatch), n_boot=200)
    lr = m["layer_results"][12]
    assert m["status"] == "tested" and lr["n"] == 100 and lr["entities"] == 25 and "beside" not in m
    w = lr["shares"]["C2"]["whole"]
    assert [w[r][0] for r in Z.ROUTES] == [0.40, 0.30, 0.0, 0.30, 0.0]
    assert w["position"][1] <= 0.30 <= w["position"][2]
    assert lr["verdict"]["clause"] == "the address exists in scattered-fact passages" and lr["verdict"]["value_ok"]
    assert lr["shares"]["C0"]["whole"]["identity"][0] == 0.60 and lr["shares"]["C2"]["no_jpp"]["original"][0] == 1.0
    assert lr["slot_aligned"]["n"] == 40 and lr["slot_aligned"]["position"][0] == 0.75  # 30 of the first 40
    (tmp_path / Z.RUNS["z3"]["qwen3.5-9b"]).rename(tmp_path / "old")
    run = planted_z3(tmp_path, monkeypatch, position=0.03, value=0.10)
    lr = Z.model_result("z3", run, n_boot=50)["layer_results"][12]
    assert lr["verdict"]["clause"].startswith("no position route") and not lr["verdict"]["value_ok"]


def test_z3_verdict_is_sealed_then_written(tmp_path, monkeypatch):
    run = planted_z3(tmp_path, monkeypatch)
    monkeypatch.setattr(Z, "dan_answer", lambda q: "")
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_verdict("z3", [run], n_boot=50)
    assert [p.name for p in tmp_path.iterdir()] == [run]
    monkeypatch.setattr(Z, "dan_answer", lambda q: "60%" if q == "Q50.3" else "")
    out = Z.stage_verdict("z3", [run, "muse30_x50_z3"], n_boot=50, decode=lambda ids: "".join(f"<{i}>" for i in ids))
    md = (out / "z3.md").read_text()
    assert "Q50.3 (Dan: 60%)" in md and "| qwen3.5-9b | qwen35_9b_x50_z3 | tested | 12 | 100 (25) |" in md
    assert "| the address exists in scattered-fact passages | True |" in md and "muse30_x50_z3 | pending" in md
    view = (out / "view.md").read_text()
    assert view.count("### s") == Z.N_VIEW and "S0 (C0's source" in view and "| 12 | C2 whole |" in view
    assert (out / "z3_routes.png").exists() and json.loads((out / "z3.json").read_text())["dan"] == "60%"


def test_z3_run_stage_end_to_end_on_a_fake_model(tok, tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    fake = FakeModel(tok, n_layers=40)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(Z, "RESULTS", tmp_path)
    monkeypatch.setattr(Z, "N_ITEMS", 3)
    real_load = Z.load_pairs
    monkeypatch.setattr(Z, "load_pairs", lambda s, p: (real_load(s, p)[0][:120], {}))
    monkeypatch.setattr(Z, "competence", lambda model, cases, ws: [
        {"scene": c["scene"], "set": c["set"], "reader": w, "variant": v, "greedy": "x", "right": True,
         "read_right": i % 4 != 3, "top": 0}
        for i, c in enumerate(cases) for w, rd in c["readers"].items() for v, _, _ in Z.golds(rd)])  # fmt: skip
    out = Z.stage_run(f"{pins.RUN_PREFIX}fake_x50_z3", "z3")
    m = json.loads((out / "manifest.json").read_text())
    gate = json.loads((out / "gate.json").read_text())
    assert m["items"] == 3 and m["readers"] == ["K"] and m["sets"] == list(Z.Z3_SETS) and m["rule"] == Z.RULE["z3"]
    assert m["as_computed"] == Z.AS_COMPUTED_Z3 and "sealed" in m and m["conditions"] == Z.Z3_CONDS
    assert gate["chosen"] == 3 and gate["chosen_s0_right"] == 3 and set(gate["org_read_accuracy"]) == {"K"}
    assert not any(p.name.startswith(("verdict", "z3")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    layers = Z.LAYERS[pins.TARGET]
    assert len(rows) == 3 * 1 * len(Z.Z3_CONDS) * (1 + len(Z.ARMS)) * len(layers)
    assert {r["condition"] for r in rows} == set(Z.Z3_CONDS) and {r["route"] for r in rows} <= set(Z.ROUTES)
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(out / "cases.jsonl")}
    c = cases[tuple(gate["order"][0])]
    rd = c["readers"]["K"]
    for r in rows:
        if (r["set"], r["scene"]) == (c["set"], c["scene"]):
            from scripts import x6_routes as R

            assert r["route"] == R.classify(r["top"], rd) and r["slot_aligned"] == c["slot_aligned"]
            assert r["switched"] == int(r["top"] == (rd["tok_b"] if r["condition"] == "C2" else rd["tok_b0"]))
    # the first two reads: the first chosen passage's C2 then C0, each the whole change h_src - h_O at the patch token
    la = layers[0]
    h = {v: fake.run(torch.tensor([rd["ids"][v]]), record=(la,))[1][la] for v in ("org", "alt", "alt0")}
    reads = [e for s, e in fake.calls if len(e) == 1 + len(Z.ARMS)]
    for edits, v in zip(reads[:2], ("alt", "alt0"), strict=True):
        assert edits[0] == {} and edits[1][la].positions == [rd["pos"]]
        assert torch.allclose(edits[1][la].delta[0], h[v][rd["pos"]] - h["org"][rd["pos"]], atol=1e-5)


def test_lightning_coverage_reads_the_committed_layer_and_his_band(monkeypatch):
    """Batch 52 C: Lightning's Z1 / Z3 at X0's committed L14 and his band's start L27 (Muse's design), his stored
    knock-out rows beside, outside batch 50's RUNS; the coverage verdict needs no Q-line."""
    from scripts import x51_lightning as L6

    lt = "nemotron-3.5-lightning"
    assert Z.LAYERS[lt] == (L6.committed_layer(), 27) and Z.BESIDE_BAND[lt] == "L27-33"
    assert (Z.pins.RESULTS_DIR / "ablate_v2" / Z.BESIDE[lt]["full"]).exists()
    assert all(lt not in Z.RUNS[p] for p in Z.RUNS) and set(Z.COVERAGE_RUNS) == {"z1", "z2", "z3", "z1p", "z2p"}
    monkeypatch.setattr(Z, "COVERAGE", True)
    assert Z.require_answer("z1") == Z.NO_PREDICTION
