"""Batch 47, test 47.7 (scripts/x47_value.py): question-first rendering keeps the bridge token (a fake tokenizer, and the
target's tokenizer when cached), slot / digit independence, the colour tokens, the moved-item counterfactual in the three
formats, the rules on planted numbers, and the sealed verdict. No GPU."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x47_value as V

LK, RC = X.LOOKUP, X.RECALL


class WordTok:
    """Words with their leading whitespace as tokens (byte-level BPE attaches the space), a fake chat template."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {"<bos>": 0}
        self.bos_token_id = 0  # a BOS target (Muse) gets it prepended by raw_encoding, the same in every rendering

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids, skip_special_tokens=False) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False):
        return f"<|im_start|>user\n{msgs[0]['content']}<|im_end|>\n<|im_start|>assistant\n"

    def __len__(self) -> int:
        return len(self.vocab)


def _real_tokenizer():
    from scripts import statement_positions as SP

    try:
        return SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


# ---- rendering and the bridge token --------------------------------------------------------------------------------


def test_question_first_puts_the_question_block_before_the_context():
    q, ctx = "Which locker belongs to Ann's pick?", "The locker of the duck is 4. Ann picked the duck."
    ql, qf = (V.user_content(q, ctx, "digit", r) for r in ("ql", "qf"))
    assert ql == f"{ctx}\n{q} Answer with a single digit and nothing else."
    assert qf == f"Question: {q} Answer with a single digit and nothing else.\n\n{ctx}"
    assert V.user_content(q, ctx, "colour", "ql").endswith("Answer with a single word and nothing else.")


def test_question_last_is_the_routes_prompt_on_the_targets_tokenizer():
    tok = _real_tokenizer()
    q, ctx = "Which locker belongs to Ann's pick?", "The locker of the duck is 4. Ann picked the duck."
    item = {"format": "prose", "kind": "digit", "context": ctx, "question": q}
    assert V.render(tok, q, ctx, "digit", "ql") == X.render(tok, item, "chat", ctx)


def test_encode_reader_keeps_the_bridge_token_across_renderings():
    tok = WordTok()
    o = "The locker of the duck is 4. The locker of the frog is 3. Ann picked the duck. Tom picked the frog."
    s = "The locker of the frog is 7. The locker of the duck is 4. Ann picked the frog. Tom picked the frog."
    q = "Which locker belongs to Ann's pick?"
    enc = V.encode_reader(tok, q, "digit", o, s, (o.index("Ann picked the duck") + 15, s.index("Ann picked the frog") + 15),
                          ("duck", "frog"), V.RENDERINGS)  # fmt: skip
    assert isinstance(enc, dict)
    for r in V.RENDERINGS:
        ids = enc["ids"][r]
        # the fake tokenizer glues the period to the word (" duck."); the bridge token is the word in O and S
        assert tok.decode([ids["org"][enc["pos"][r]]]).strip(" .") == "duck"
        assert tok.decode([ids["alt"][enc["pos"][r]]]).strip(" .") == "frog"
        assert len(ids["org"]) == len(ids["alt"])
    # the shift is the question block's token count (Question: + 6 words + 8 instruction words = 15 tokens here)
    assert enc["shift"] == enc["pos"]["qf"] - enc["pos"]["ql"] == 15
    cq, cl = enc["ctx0"]["qf"], enc["ctx0"]["ql"]
    assert (
        enc["ids"]["qf"]["org"][cq + 1 : enc["pos"]["qf"] + 1] == enc["ids"]["ql"]["org"][cl + 1 : enc["pos"]["ql"] + 1]
    )
    assert (
        tok.decode([enc["ids"]["qf"]["org"][cq]]).strip() == tok.decode([enc["ids"]["ql"]["org"][cl]]).strip() == "The"
    )


def test_encode_reader_rejects_a_moved_bridge():
    tok = WordTok()
    o = "The locker of the duck is 4. Ann picked the duck."
    s = "The locker of the duck is 4. Also: Ann picked the frog."  # one more token before the bridge in S
    out = V.encode_reader(tok, "q?", "digit", o, s, (o.index("duck."), s.index("frog.")), ("duck", "frog"), ("ql",))
    assert isinstance(out, str) and "same index" in out


def test_scenes_reproduce_x6_routes_draws_on_the_targets_tokenizer():
    from scripts import x6_routes as R

    tok = _real_tokenizer()
    ours, _ = V.scenes(tok, 8)
    theirs = {c["scene"]: c for c in R.scenes(tok, 8)[0]}
    assert len(ours) == 16 and all(c["scene"] in theirs for c in ours)
    for c in ours:
        t = theirs[c["scene"]]
        assert (c["context"], c["cf_context"], c["bridge"], c["cf_bridge"]) == (
            t["context"],
            t["cf_context"],
            t["bridge"],
            t["cf_bridge"],
        )
        assert {k: int(v) for k, v in c["expect"].items()} == {k: v for k, v in t["expect"].items() if k != "switch"}
        for w in X.READERS:
            assert c["readers"][w]["ids"]["ql"] == t["readers"][w]["ids"] and c["readers"][w]["pos"]["ql"] == t["pos"]
            assert c["readers"][w]["shift"] > 0
            ids = c["readers"][w]["ids"]["qf"]["org"]
            assert tok.decode([ids[c["readers"][w]["pos"]["qf"]]]).strip() == c["bridge"]
            assert "Question:" in tok.decode(ids[: c["readers"][w]["pos"]["qf"]])


# ---- dumbest way 2: independence ---------------------------------------------------------------------------------


def test_independence_accepts_independent_and_rejects_planted_dependence():
    rng = random.Random(0)
    free = [(rng.randrange(3), rng.randrange(1, 10)) for _ in range(600)]
    assert V.independence(free, n_perm=300)["independent"]
    tied = [(s, (s * 3 + k % 3) + 1) for s in range(3) for k in range(200)]  # the digit set by the slot
    r = V.independence(tied, n_perm=300)
    assert not r["independent"] and r["p"] < 0.01 and r["cramers_v"] > 0.9
    assert np.array(r["table"]).sum() == 600


def test_scenes_draw_digits_independently_of_slots():
    tok = WordTok()
    cases, _ = V.scenes(tok, 150, renderings=("ql",))
    base = {c["context"]: c for c in cases}
    r = V.independence([(c["slot"], c["readers"][LK]["answer"]) for c in base.values()], n_perm=500)
    assert r["independent"] and r["n"] == len(base) and r["df"] == 16


# ---- colours ------------------------------------------------------------------------------------------------------


def test_colour_pool_keeps_single_token_colours():
    tok = WordTok()
    ok, bad = V.colour_pool(tok)
    assert ok == list(V.COLOURS) and not bad


def test_colours_are_single_tokens_on_the_targets_tokenizer():
    ok, bad = V.colour_pool(_real_tokenizer())
    assert len(ok) >= 5, bad


def test_colour_scenes_read_words_and_digits():
    tok = WordTok()
    cases, _ = V.scenes(tok, 6, kind="colour", renderings=("ql", "qf"))
    c = next(c for c in cases if c["condition"] == "C2")
    assert set(c["expect"].values()) <= set(V.COLOURS) and len(set(c["expect"].values())) == 4
    assert c["readers"][LK]["space"] == [] and c["readers"][RC]["space"] == tok(" ").input_ids
    assert tok.decode([c["readers"][LK]["tok_A"]]) == " " + c["readers"][LK]["answer"]
    assert c["readers"][RC]["answer"].isdigit()
    assert V.said_of("Red\n", "colour") == "red" and V.said_of("  gold or teal", "colour") == "gold"
    assert V.said_of("none", "colour") is None and V.said_of("7", "digit") == "7"


# ---- (c): the moved-item counterfactual ----------------------------------------------------------------------------


def _scene(fmt: str, level: int, seed: int = 0):
    from scripts import tasks_v2 as T

    rng = random.Random(seed)
    its = None
    while its is None:
        its = T.make_scene(rng, "P", ["PP", "PM"], "animals", fmt, T.LEVELS[level], list(T.DOMAINS))
    pp, pm = its
    return {**pp, "id": "PP-x", "scene": "s"}, {**pm, "id": "PM-x", "scene": "s"}


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_moved_context_changes_the_pick_and_two_locker_statements_only(fmt):
    from scripts import x7_pcf as PC

    for seed in range(12):
        pp, _ = _scene(fmt, 1, seed)
        f = pp["facts"]
        x = f["x"]
        things = [t for t in f["locker"] if t != x]
        if len(things) < 2:
            continue
        t, u = things[:2]
        e = next(n for n in range(1, 10) if n not in f["locker"].values())
        s = V.moved_context(pp, t, u, e)
        assert PC.locker_statement(pp, u) in s and PC.locker_statement(pp, x) in s
        new_t = PC.locker_statement({**pp, "facts": {**f, "locker": {**f["locker"], t: e}}}, t)
        assert new_t in s and PC.locker_statement(pp, t) not in s
        # t's new statement sits where u's was, u's where t's was
        o_t, o_u = PC.statement_at(pp, t), PC.statement_at(pp, u)
        assert (s.index(new_t) < s.index(PC.locker_statement(pp, u))) == (o_u < o_t)
        # the pick changed x -> t and nothing else differs
        from scripts import x0b_generalize as B

        pick_o, _ = B.statements(pp, f["person"], x)
        pick_s, _ = B.statements(pp, f["person"], t)
        assert pick_o not in s and s.count(pick_s) == 1
        back = s.replace(pick_s, pick_o).replace(new_t, PC.locker_statement(pp, t))
        assert sorted(back.split()) == sorted(pp["context"].split())
        return
    pytest.skip("no scene with three locker items")


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_moved_case_routes_are_distinct_and_s_equals_o_from_the_bridge_on(fmt):
    tok = _real_tokenizer()
    got = 0
    for seed in range(30):
        pp, pm = _scene(fmt, 1, seed)
        c, _ = V.moved_case(tok, pp, pm, random.Random(seed))
        if c is None:
            continue
        got += 1
        f = pp["facts"]
        assert len(set(c["expect"].values())) == 4 and c["expect"]["original"] == pp["answer"]
        assert c["expect"]["identity"] == str(f["locker"][c["cf_bridge"]]) and c["expect"]["position"] == str(
            f["locker"][c["third"]]
        )
        assert int(c["expect"]["value"]) not in f["locker"].values()
        # S's lookup answer is the moved bridge's new number, as in C2 (the x47_7c runs of 28 Oct had the identity
        # number here and found no eligible case: the lookup says the value on S)
        assert c["readers"][LK]["cf_answer"] == c["expect"]["value"] and c["readers"][LK]["answer"] == pp["answer"]
        for w in X.READERS:
            ids, pos = c["readers"][w]["ids"]["ql"], c["readers"][w]["pos"]["ql"]
            assert ids["org"][pos + 1 :] == ids["alt"][pos + 1 :] and ids["org"][pos] != ids["alt"][pos]
            assert (
                tok.decode([ids["org"][pos]]).strip() == c["bridge"]
                and tok.decode([ids["alt"][pos]]).strip() == c["cf_bridge"]
            )
        assert c["readers"][LK]["ids"]["ql"]["org"][: pos + 1] == c["readers"][RC]["ids"]["ql"]["org"][: pos + 1]
    assert got >= 3, f"only {got} moved cases in 30 {fmt} scenes"


# ---- the rules on planted numbers ----------------------------------------------------------------------------------


def _rows_a(n: int, ents: int, qf: dict, ql: dict, cond: str = "C2") -> list[dict]:
    """Planted lookup rows: per rendering and arm, the share of value / position answers (the rest identity)."""
    rows = []
    for i in range(n):
        for r, spec in (("qf", qf), ("ql", ql)):
            for a, (v, p) in spec.items():
                frac = i / n
                route = "value" if frac < v else "position" if frac < v + p else "identity"
                rows.append({"scene": f"{cond}-{i:04d}", "condition": cond, "entity": f"e{i % ents}", "reader": LK,
                             "rendering": r, "arm": a, "route": route, "switched": 0, "format": "prose"})  # fmt: skip
    return rows


def test_route_shares_and_the_fall_beyond_random():
    rows = _rows_a(200, 20, {"whole": (0.3, 0.5), "no_jpp": (0.05, 0.5), "no_jpp_rand": (0.4, 0.5), "no_alf": (0.3, 0.1),
                             "no_alf_rand": (0.3, 0.5)}, {"whole": (0.0, 0.5)})  # fmt: skip
    s = V.route_shares(rows, lambda r: r["rendering"] == "qf", V.ARMS, n_boot=200)
    assert s is not None
    assert s["n"] == 200 and s["arms"]["whole"]["value"][0] == pytest.approx(0.3)
    assert s["fall_beyond_random"]["jpp"]["value"][0] == pytest.approx(0.35)
    assert s["fall_beyond_random"]["alf"]["position"][0] == pytest.approx(0.4)
    assert s["fall_beyond_random"]["alf"]["value"][0] == pytest.approx(0.0)
    d = V.paired_rendering_diff(rows, "C2", "value", n_boot=200)
    assert d is not None
    assert d[0] == pytest.approx(0.3) and d[1] <= d[0] <= d[2]
    assert V.route_shares(rows, lambda r: r["rendering"] == "xx", V.ARMS, 10) is None


def _model(v_qf, v_ql, p_qf, p_ql, fall, lens_qf, lens_ql=0.1, status="tested") -> dict:
    return {"run": "r", "status": status, "why": "",
            "shares": {"qf": {"arms": {"whole": {"value": [v_qf, 0, 1]}}, "fall_beyond_random": {"jpp": {"value": [fall, 0, 1]}}},
                       "ql": {"arms": {"whole": {"value": [v_ql, 0, 1]}}, "fall_beyond_random": {}}},
            "probe": {"qf": {"probe": [p_qf, 0, 1]}, "ql": {"probe": [p_ql, 0, 1]}},
            "lens": {"qf": {"first": [lens_qf, 0, 1]}, "ql": {"first": [lens_ql, 0, 1]}}}  # fmt: skip


def test_rule_a_labels():
    r = V.rule_a(_model(0.2, 0.0, 0.7, 0.3, 0.35, 0.5))
    assert r["prefetch"] and r["jspace"] and not r["address"] and r["premise_ql"]
    r = V.rule_a(_model(0.15, 0.0, 0.6, 0.3, 0.3, 0.4))  # bars inclusive
    assert r["prefetch"] and r["jspace"]
    r = V.rule_a(_model(0.2, 0.0, 0.7, 0.3, 0.2, 0.5))  # the fall misses 0.3
    assert r["prefetch"] and not r["jspace"]
    r = V.rule_a(_model(0.0, 0.0, 0.35, 0.3, 0.0, 0.1))
    assert r["address"] and not r["prefetch"]
    r = V.rule_a(_model(0.0, 0.0, 0.5, 0.3, 0.0, 0.1))  # the probe moved by 0.2: not address
    assert not r["address"] and not r["prefetch"]
    r = V.rule_a(_model(0.2, 0.1, 0.7, 0.5, 0.35, 0.5))  # the premise fails: reported, labels unchanged
    assert r["prefetch"] and not r["premise_ql"]
    assert not any(
        V.rule_a({**_model(0.2, 0, 0.7, 0.3, 0.35, 0.5), "status": "not tested", "why": "gate"}).get(k)
        for k in ("prefetch", "jspace", "address")
    )


def test_batch_a_counts_two_of_three():
    def m(prefetch, jspace, address, status="tested"):
        return {"run": status, "status": status, "rule": {"prefetch": prefetch, "jspace": jspace, "address": address}}

    assert (
        V.batch_a([m(1, 1, 0), m(1, 1, 0), m(0, 0, 1)])["label"]
        == "prefetch on demand, the prefetched value is in the J-space"
    )
    assert V.batch_a([m(1, 0, 0), m(1, 1, 0), m(0, 0, 1)])["label"] == "prefetch on demand, not shown in the J-space"
    assert V.batch_a([m(0, 0, 1), m(0, 0, 1), m(1, 1, 0)])["label"] == "address regardless"
    assert V.batch_a([m(0, 0, 1), m(1, 1, 0), m(0, 0, 0, "pending")])["label"] == "neither label on 2 of 3 models"
    v = V.batch_a([m(0, 0, 1), m(0, 0, 1), m(0, 0, 0, "not tested")])
    assert v["label"] == "address regardless" and v["not_tested"] == ["not tested"]


def test_rule_c_and_batch_c():
    def cell(v, p, cut=None):
        c = {"n": 50, "arms": {"whole": {"value": [v, 0, 1], "position": [p, 0, 1]}}, "fall_beyond_random": {}}
        if cut is not None:
            c["fall_beyond_random"]["pcf"] = {"position": [cut, 0, 1]}
        return c

    r = V.rule_c(cell(0.05, 0.3, 0.3))
    assert r["tested"] and r["value_ok"] and r["position_route"]
    assert not V.rule_c(cell(0.06, 0.3, 0.3))["value_ok"]
    assert V.rule_c(cell(0.0, 0.3))["position_route"] is None  # no refit arm (the 27B)
    assert not V.rule_c(cell(0.0, 0.19, 0.5))["position_route"]
    good = {"run": "g", "rule": {f: V.rule_c(cell(0.0, 0.1, 0.0)) for f in V.FORMATS}}
    bad = {"run": "b", "rule": {**good["rule"], "json": V.rule_c(cell(0.2, 0.3, 0.4))}}
    missing = {"run": "m", "rule": {**good["rule"], "table": V.rule_c(None)}}
    assert V.batch_c([good, good, good])["label"] == "never the value generalizes"
    v = V.batch_c([good, bad, good])
    assert v["label"] == "does not generalize" and v["value_above"] == ["b/json"] and v["position_route"] == ["b/json"]
    v = V.batch_c([good, missing, good])
    assert v["label"] == "incomplete" and v["untested"] == ["m/table"]


def test_rule_b_and_batch_b():
    m1 = _model(0.0, 0.2, 0.7, 0.3, 0.35, 0.5)
    m1["shares"]["ql"]["fall_beyond_random"] = {"jpp": {"value": [0.4, 0, 1]}}
    r = V.rule_b(m1)
    assert r["ql"]["appears"] and r["ql"]["jpp_carries"] and not r["ql"]["never"] and not r["qf"]["appears"]
    m2 = _model(0.0, 0.05, 0.7, 0.3, 0.0, 0.1)
    assert V.rule_b(m2)["ql"]["never"] and not V.rule_b(m2)["ql"]["appears"]
    v = V.batch_b([{"run": "a", "rule": r}, {"run": "b", "rule": V.rule_b(m2)}])
    assert v["appears_ql"] == ["a"] and v["jpp_carries_ql"] == ["a"] and not v["never_the_value_word"]
    v = V.batch_b(
        [{"run": "b", "rule": V.rule_b(m2)}, {"run": "p", "rule": {"ql": {"tested": False}, "qf": {"tested": False}}}]
    )
    assert v["never_the_value_word"] and v["tested"] == ["b"]


def test_lens_numbers_dedupe_c0_and_c2_by_base_scene():
    rd = [{"scene": f"{c}-{i:04d}", "rendering": "qf", "entity": f"e{i % 5}", "answer": "3", "rank": 1 if i < 4 else 2,
           "n_candidates": 10} for i in range(10) for c in ("C0", "C2")]  # fmt: skip
    ln = V.lens_numbers(rd, n_boot=100)["qf"]
    assert ln["n"] == 10 and ln["first"][0] == pytest.approx(0.4) and ln["chance"] == 0.1


def test_probe_numbers_on_planted_states(tmp_path):
    rng = np.random.default_rng(0)
    items, h, rends = [], [], []
    for r in ("ql", "qf"):
        for i in range(60):
            ans = str(1 + i % 9)
            items.append({"scene": f"C2-{i:04d}", "condition": "C2", "rendering": r, "entity": f"e{i % 12}", "answer": ans,
                          "slot": i % 3, "context": f"ctx {i}", "format": "prose"})  # fmt: skip
            v = rng.standard_normal(16)
            if r == "qf":
                v[int(ans)] += 6.0  # the digit is linearly decodable question-first only
            h.append(v)
            rends.append(r)
    np.savez_compressed(tmp_path / "states.npz", h=np.stack(h).astype(np.float16), scene=np.array([it["scene"] for it in items]),
                        rendering=np.array(rends))  # fmt: skip
    X.write_jsonl(tmp_path / "items.jsonl", items)
    p = V.probe_numbers(tmp_path, n_boot=100)
    assert p["qf"]["probe"][0] > 0.8 and p["ql"]["probe"][0] < 0.4 and p["qf"]["n"] == 60


def test_dan_answer_reads_only_the_q47_7_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.6** (47.6) ...\n\nDan: yes · 60%\n\n**Q47.7** (47.7) ...\n\nRule: ...\n\nDan:{}\n"
    monkeypatch.setattr(V.subprocess, "run", fake_git(blocks.format("")))
    assert V.dan_answer() == ""
    monkeypatch.setattr(
        V.subprocess, "run", fake_git(blocks.format(" address · 70%") + "\n## Batch 48\n\n**Q48.1** x\n\nDan: z\n")
    )
    assert V.dan_answer() == "address · 70%"


def test_verdict_is_sealed_until_dans_answer(monkeypatch):
    monkeypatch.setattr(V, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        V.stage_verdict("a", ["qwen35_9b_x47_7a"], n_boot=10)


def test_gate_cases_uses_the_parts_gate_renderings():
    cases = [{"scene": f"C2-{i:04d}", "condition": "C2", "renderings": ["ql", "qf"],
              "readers": {w: {} for w in X.READERS}} for i in range(20)]  # fmt: skip
    comp = []
    for c in cases:
        for w in X.READERS:
            for r in ("ql", "qf"):
                for v in ("org", "alt"):
                    bad = r == "qf" and w == LK and int(c["scene"][-2:]) < 6  # qf lookup reads 14 of 20 right: 0.70
                    comp.append({"scene": c["scene"], "reader": w, "rendering": r, "variant": v, "right": not bad,
                                 "read_right": not bad})  # fmt: skip
    gate, chosen = V.gate_cases("a", cases, comp)
    assert gate["C2"]["org_read_accuracy"]["qf"][LK] == pytest.approx(0.7) and not gate["C2"]["pass"] and not chosen
    gate, chosen = V.gate_cases("a", cases, comp, gate_min=0.7)
    assert gate["C2"]["pass"] and len(chosen) == 14  # eligible in every rendering


def test_verdict_on_a_planted_run(tmp_path, monkeypatch):
    """A planted 47.7(a) run folder: the value route appears question-first (0.3), falls without J++, the probe reads
    the digit question-first; the verdict labels it prefetch (two of three models pending)."""
    monkeypatch.setattr(V, "RESULTS", tmp_path)
    monkeypatch.setattr(V, "dan_answer", lambda: "prefetch · 60%")
    monkeypatch.setattr(V, "example_lines", lambda run: [f"examples of {run}"])
    src = tmp_path / "qwen35_9b_x47_7a"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layer": 12}))
    (src / "plan.json").write_text("{}")
    (src / "gate.json").write_text(
        json.dumps(
            {"gate": {"C2": {"pass": True, "org_read_accuracy": {}}, "C0": {"pass": True, "org_read_accuracy": {}}}}
        )
    )
    (src / "c0_check.json").write_text(json.dumps({"qf": {"ok": True}, "ql": {"ok": True}}))
    rows = _rows_a(100, 20, {"whole": (0.3, 0.4), "no_jpp": (0.0, 0.4), "no_jpp_rand": (0.35, 0.4), "no_alf": (0.3, 0.0),
                             "no_alf_rand": (0.3, 0.4)}, {"whole": (0.0, 0.5)})  # fmt: skip
    rows += [{**r, "scene": r["scene"].replace("C2", "C0"), "condition": "C0"} for r in rows]
    X.write_jsonl(src / "outcomes.jsonl", rows)
    rng = np.random.default_rng(1)
    items, h, rends, readout = [], [], [], []
    for r in ("ql", "qf"):
        for i in range(100):
            ans = str(1 + i % 9)
            items.append({"scene": f"C2-{i:04d}", "condition": "C2", "rendering": r, "entity": f"e{i % 20}", "answer": ans,
                          "slot": i % 3, "context": f"ctx {i}", "format": "prose"})  # fmt: skip
            v = rng.standard_normal(16)
            if r == "qf":
                v[int(ans)] += 6.0
            h.append(v)
            rends.append(r)
            readout.append({"scene": f"C2-{i:04d}", "condition": "C2", "rendering": r, "entity": f"e{i % 20}", "answer": ans,
                            "rank": 1 if (r == "qf" and i % 2 == 0) else 3, "top": "1", "n_candidates": 10})  # fmt: skip
    np.savez_compressed(src / "states.npz", h=np.stack(h).astype(np.float16), scene=np.array([it["scene"] for it in items]),
                        rendering=np.array(rends))  # fmt: skip
    X.write_jsonl(src / "items.jsonl", items)
    X.write_jsonl(src / "readout.jsonl", readout)
    out = V.stage_verdict("a", ["qwen35_9b_x47_7a"], n_boot=100)
    blob = json.loads((out / "x47_7a.json").read_text())
    m = blob["models"][0]
    assert m["status"] == "tested" and m["rule"]["prefetch"] and m["rule"]["jspace"] and not m["rule"]["address"]
    assert m["shares"]["qf"]["fall_beyond_random"]["jpp"]["value"][0] == pytest.approx(0.35)
    assert m["position_qf_minus_ql"][0] == pytest.approx(-0.1)
    assert m["lens"]["qf"]["first"][0] == pytest.approx(0.5) and m["lens"]["ql"]["first"][0] == 0.0
    assert [x["status"] for x in blob["models"]] == ["tested", "pending", "pending"]
    assert blob["verdict"]["label"] == "neither label on 2 of 3 models"  # one model cannot make 2 of 3
    assert "examples of qwen35_9b_x47_7a" in (out / "examples.md").read_text()
    assert (out / "x47_7a.md").read_text().startswith("# 47.7(a)")
