"""Batch 51, test 51.3 (scripts/x51_das.py): DAS at scale. The pooled identity pairs (dedup, the per-reader cap, the
split by entity), the routes C0 pairs, the main-test pool against x48_das.select_pairs on the real stored run (where the
target's tokenizer is cached), the top-up's stop rules and gate, early stopping around x48_das's loop (identical without
dev rows), the OOM fallback, the new rule and Q51.3's readouts on planted numbers, the seal, and the run / verdict /
view stages end to end on x49_das_pos's tiny fake causal model. CPU, no real model."""

from __future__ import annotations

import json
import random
from types import SimpleNamespace

import numpy as np
import pytest
import test_x49_das_pos as T49
import torch

from scripts import suite_v1 as S
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x48_das as D
from scripts import x49_das_pos as Q
from scripts import x51_das as Z

D_MODEL = T49.D_MODEL
LK, RC = X.LOOKUP, X.RECALL


# ---- C0 scenes on the word tokenizer (x6_routes' C0: S = O but Iris picked B) -----------------------------------------


def c0_case(tok, idx: int, rng: random.Random) -> dict:
    A, B, C = rng.sample(T49.ANIMALS, 3)
    a, b, c = rng.sample(range(1, 10), 3)
    order = rng.sample([A, B, C], 3)
    val = {A: a, B: b, C: c}
    picks = rng.sample([("Iris", A), ("Tom", B), ("Ann", C)], 3)
    o = R.context([(x, val[x]) for x in order], picks)
    s = R.context([(x, val[x]) for x in order], [(q, B if q == "Iris" else x) for q, x in picks])
    one = lambda v: S.answer_token(tok, str(v), "digit")  # noqa: E731
    readers, pos = {}, None
    for w, q, ans in ((LK, R.LOOKUP_Q, (a, b)), (RC, R.RECALL_Q, (T49.LEGS[A], T49.LEGS[B]))):
        ids = {}
        for v, ctx, item in (("org", o, A), ("alt", s, B)):
            text = f"{ctx} {q.format(p='Iris')} Answer:"
            enc = tok(text, return_offsets_mapping=True)
            w0 = text.index(f"Iris picked the {item}.") + len("Iris picked the")
            at = [k for k, (st, _) in enumerate(enc.offset_mapping) if st == w0]
            pos = at[0] if pos is None else pos
            assert at[0] == pos
            ids[v] = enc.input_ids
        readers[w] = {"question": q.format(p="Iris"), "answer": str(ans[0]), "cf_answer": str(ans[1]), "ids": ids,
                      "tok_A": one(ans[0]), "tok_b": one(ans[1])}  # fmt: skip
    return {"scene": f"C0-{idx:04d}", "condition": "C0", "rendering": "chat", "domain": "animals", "bridge": A,
            "cf_bridge": B, "context": o, "cf_context": s, "pos": pos, "space": [tok.vocab.setdefault(" ", len(tok.vocab))],
            "expect": {"switch": b, "original": a}, "route_tokens": {"original": one(a)}, "readers": readers}  # fmt: skip


def c0_cases(tok, n: int, seed: int = 1, start: int = 1) -> list[dict]:
    rng = random.Random(seed)
    return [c0_case(tok, start + i, rng) for i in range(n)]


def identity_pool(tok, n: int, seed: int = 1, source: str = "routes", sw=lambda i: {LK: 1, RC: int(i % 3 != 0)}):
    return [Z.identity_pair(tok, c, sw(i), source) for i, c in enumerate(c0_cases(tok, n, seed))]


# ---- the pairs -------------------------------------------------------------------------------------------------------


def test_identity_pair_keeps_both_readers_and_the_stored_switches():
    tok = T49.WordTok()
    c = c0_cases(tok, 1)[0]
    p = Z.identity_pair(tok, c, {LK: 1, RC: 0}, "routes")
    assert p["scene"] == f"routes:{c['scene']}" and p["source_scene"] == c["scene"] and p["entity"] == c["bridge"]
    assert p["stored_whole"] == {LK: 1, RC: 0} and p["pos"] == c["pos"]
    assert p["locker_index"] == [s.split(" is ")[0] for s in c["context"].split(". ")].index(
        f"The locker of the {c['bridge']}"
    )
    for w in X.READERS:
        assert p["readers"][w]["ids"] == c["readers"][w]["ids"] and p["readers"][w]["tok_b"] == c["readers"][w]["tok_b"]
        assert p["readers"][w]["marked"].count("⟦bridge:") == 1
        assert (
            p["readers"][w]["marked"].split("⟦bridge:")[1].startswith(f" {c['bridge']}")
        )  # the word tokenizer: "cat."
    assert Z.routes_locker_first(c)
    late = {**c, "context": c["context"].replace("The locker", "X", 1) + " The locker of the yak is 9."}
    assert not Z.routes_locker_first(late)


def test_finish_identity_dedups_caps_per_reader_in_pool_order_and_splits_by_entity(monkeypatch):
    tok = T49.WordTok()
    pool = identity_pool(tok, 40)
    pool += [dict(pool[0], scene="dup")]  # the same O and S prompts again
    monkeypatch.setattr(Z, "ID_MAX", 20)
    out, info = Z.finish_identity([dict(p) for p in pool])
    assert info["duplicates_dropped"] == 1 and "dup" not in {p["scene"] for p in out}
    assert info["per_reader_before_cap"] == {"lookup": 40, "recall": sum(i % 3 != 0 for i in range(40))}
    assert info["per_reader"] == {"lookup": 20, "recall": 20}
    lk = [p["scene"] for p in out if p["in_pairs"][LK]]
    assert lk == [p["scene"] for p in pool[:20]]  # the first 20 in pool order
    rc = [p["scene"] for p in out if p["in_pairs"][RC]]
    assert rc == [p["scene"] for i, p in enumerate(pool[:40]) if i % 3 != 0][:20]
    assert all(any(p["in_pairs"].values()) for p in out)  # no scene in neither reader's pairs
    by_entity = {}
    for p in out:
        assert by_entity.setdefault(p["entity"], p["split"]) == p["split"]  # entities held out
    assert set(by_entity.values()) == {"train", "select", "test"}
    assert by_entity == D.split_entities(list(by_entity))


def test_need_identity():
    tok = T49.WordTok()
    pool = identity_pool(tok, 10)
    need = Z.need_identity(pool)
    assert need == {LK: Z.ID_MIN - 10, RC: Z.ID_MIN - sum(i % 3 != 0 for i in range(10))}


def test_topup_candidates_follow_the_stored_run_in_generator_order():
    gen = [{"scene": f"{c}-{i:04d}", "condition": c} for i in (5, 1, 9, 3, 12) for c in ("C0", "C1")]
    got = Z.topup_candidates(gen, "C0", 4)
    assert [c["scene"] for c in got] == ["C0-0005", "C0-0009", "C0-0012"]
    assert Z.scene_index("C2-0123") == 123


def test_x0_pool_on_the_main_run_matches_x48_das_select_pairs():
    """The target's stored main test with the real tokenizer (skipped where it or the run is missing): x0_pool with
    alt cf keeps exactly 48.1's pairs (scenes, stored switches)."""
    from bridge_jspace import pins
    from scripts import x45m

    if pins.TARGET not in D.MAIN_RUN or not (X.RESULTS / D.MAIN_RUN[pins.TARGET] / "outcomes.jsonl").exists():
        pytest.skip("no stored main run of the target")
    try:
        tok = x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    layer = X.PREDICTED[pins.TARGET]
    mine, info = Z.x0_pool(tok, D.MAIN_RUN[pins.TARGET], layer, "cf", "main")
    ref, _ = D.select_pairs(tok, D.MAIN_RUN[pins.TARGET], layer)
    assert [p["source_scene"] for p in mine] == [p["scene"] for p in ref]
    assert [p["stored_whole"] for p in mine] == [p["stored_whole"] for p in ref]
    assert info["per_reader"] == {
        "lookup": sum(p["stored_whole"][LK] for p in ref),
        "recall": sum(p["stored_whole"][RC] for p in ref),
    }


# ---- the top-up (fake model, competence planted) -----------------------------------------------------------------


def all_right(model, cases, digits, ws):
    return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "right": True, "read_right": True}
            for c in cases for w in X.READERS for v in ("org", "alt")]  # fmt: skip


def test_topup_stops_at_the_scene_that_meets_the_rule(monkeypatch):
    tok = T49.WordTok()
    fake = T49.FakeModel(tok)
    monkeypatch.setattr(X, "competence", all_right)
    cases = c0_cases(tok, 40)
    ws, digits = X.whitespace_mask(fake), torch.tensor(X.digit_ids(tok))
    recs, gate = Z.topup(fake, cases, 3, ws, digits, lambda r: len(r) >= 7, chunk=5)
    assert [r["scene"] for r in recs] == [c["scene"] for c in cases[:7]]  # not the rest of its chunk
    assert gate["reached"] and gate["pass"] and gate["eligible"] == 7
    # the whole change read: h_S - h_O at the bridge added on O, the read's top token
    c = cases[0]
    ids = c["readers"][LK]["ids"]
    h = {v: fake.run(torch.tensor([ids[v]]), record=(3,))[1][3][c["pos"]] for v in ("org", "alt")}
    from scripts.exp04_brew_parts import AddRows

    lg = fake.generate_batch(torch.tensor([ids["org"] + c["space"]]), 1, [{3: AddRows((h["alt"] - h["org"])[None], [c["pos"]])}],
                             first_logits=True)[1][0]  # fmt: skip
    assert recs[0][LK]["top"] == int(lg.argmax()) and recs[0][LK]["switched"] == int(
        int(lg.argmax()) == c["readers"][LK]["tok_b"]
    )


def test_topup_gate_and_ineligible_scenes(monkeypatch):
    tok = T49.WordTok()
    fake = T49.FakeModel(tok)
    cases = c0_cases(tok, 10)

    def half_wrong(model, cs, digits, ws):
        rows = all_right(model, cs, digits, ws)
        for r in rows:
            if r["reader"] == RC and r["variant"] == "org" and int(r["scene"][-1]) % 2:
                r["read_right"] = False
        return rows

    monkeypatch.setattr(X, "competence", half_wrong)
    recs, gate = Z.topup(fake, cases, 3, X.whitespace_mask(fake), torch.tensor(X.digit_ids(tok)), lambda r: False)
    assert len(recs) == 10 and not gate["reached"]
    assert [r["eligible"] for r in recs] == [int(not int(c["scene"][-1]) % 2) for c in cases]
    assert all(RC not in r for r in recs if not r["eligible"])  # no read for an ineligible scene
    assert gate["org_read_accuracy"]["recall"] == 0.5 and not gate["pass"]


def test_identity_topup_reads_until_every_reader_has_its_minimum_and_drops_on_a_failed_gate(monkeypatch):
    tok = T49.WordTok()
    pool = identity_pool(tok, 6, seed=1, sw=lambda i: {LK: 1, RC: 0})
    cands = c0_cases(tok, 20, seed=2, start=100)
    monkeypatch.setattr(Z, "ID_MIN", 8)
    recs = [{"scene": c["scene"], "condition": "C0", "eligible": 1, LK: {"switched": 1, "top": 0, "route": None},
             RC: {"switched": int(i % 2 == 0), "top": 0, "route": None}} for i, c in enumerate(cands)]  # fmt: skip
    seen = {}

    def fake_topup(model, cs, layer, ws, digits, done, chunk=16):
        for n in range(1, len(recs) + 1):
            if done(recs[:n]):
                seen["n"] = n
                return recs[:n], {"pass": True, "reached": True}
        return recs, {"pass": True, "reached": False}

    monkeypatch.setattr(Z, "topup", fake_topup)
    out, info = Z.identity_topup(None, tok, pool, cands, 3, None, None)
    assert seen["n"] == 15  # the recall needs 8 switches: every second scene, the 8th at the 15th
    assert len(out) == 15 and all(p["source"] == "routes_topup" for p in out)
    assert info["added"] == {"lookup": 15, "recall": 8} and info["short"] == {"lookup": 2, "recall": 8}
    monkeypatch.setattr(Z, "topup", lambda *a, **k: (recs[:15], {"pass": False, "reached": True}))
    out, info = Z.identity_topup(None, tok, pool, cands, 3, None, None)
    assert out == [] and "dropped" in info
    full = identity_pool(tok, 8, seed=4, sw=lambda i: {LK: 1, RC: 1})
    assert Z.identity_topup(None, tok, full, cands, 3, None, None) == ([], {"needed": False})


def test_address_topup_keeps_the_position_route(monkeypatch):
    tok = T49.WordTok()
    cases = T49.c1_cases(tok, 12)
    pool = [Q.position_pair(tok, c) for c in cases[:3]]
    monkeypatch.setattr(Z, "POS_MIN", 6)
    routes = ["position", "identity", "position", "position", "other", "position", "position"]
    recs = [{"scene": c["scene"], "condition": "C1", "eligible": 1, LK: {"switched": 0, "top": 0, "route": rt},
             RC: {"switched": 0, "top": c["readers"][RC]["tok_A"], "route": None}}
            for c, rt in zip(cases[3:], routes, strict=False)]  # fmt: skip

    def fake_topup(model, cs, layer, ws, digits, done, chunk=16):
        n = next(n for n in range(1, len(recs) + 1) if done(recs[:n]))
        return recs[:n], {"pass": True, "reached": True}

    monkeypatch.setattr(Z, "topup", fake_topup)
    out, info = Z.address_topup(None, tok, pool, cases[3:], 3, None, None)
    assert len(out) == 3 and info["added"] == 3 and info["routes"] == {"position": 3, "identity": 1}
    assert [p["scene"] for p in out] == [cases[3]["scene"], cases[5]["scene"], cases[6]["scene"]]
    assert all(p["stored_recall_kept"] == 1 and p["topup"] == 1 for p in out)


# ---- early stopping around x48_das's loop ----------------------------------------------------------------------------


def das_rows(tok, n: int, seed: int = 0, target: int = 7):
    g = torch.Generator().manual_seed(seed)
    return [{"ids": tok(f"w{i} x y z").input_ids, "pos": 0, "delta": torch.randn(D_MODEL, generator=g) * 5, "target": target}
            for i in range(n)]  # fmt: skip


def test_train_early_without_dev_rows_is_x48_das_train_subspace():
    tok = T49.WordTok()
    fake = T49.FakeModel(tok, n_layers=6)
    rows = das_rows(tok, 6)
    torch.manual_seed(5)  # train_early seeds the global RNG with the R's seed (the parametrisation draws from it)
    ref = D.train_subspace(fake, 2, rows, k=3, seed=5, steps=12, batch=4, micro=2)
    mine, info = Z.train_early(fake, 2, rows, [], k=3, seed=5, steps=12, batch=4, micro=2)
    assert torch.allclose(mine, ref, atol=1e-6) and info["best_step"] is None and info["stopped_at"] == 11
    torch.manual_seed(5)
    ref_s = D.train_subspace(fake, 2, rows, k=3, seed=5, steps=12, batch=4, micro=2, shuffle=9)
    mine_s, _ = Z.train_early(fake, 2, rows, [], k=3, seed=5, steps=12, batch=4, micro=2, shuffle=9)
    assert torch.allclose(mine_s, ref_s, atol=1e-6)
    again, _ = Z.train_early(fake, 2, rows, [], k=3, seed=5, steps=12, batch=4, micro=2, shuffle=9)
    assert torch.equal(again, mine_s)  # reproducible from the seed alone


def test_train_early_keeps_the_best_dev_r_and_stops_after_patience(monkeypatch):
    tok = T49.WordTok()
    fake = T49.FakeModel(tok, n_layers=6)
    rows, dev = das_rows(tok, 6), das_rows(tok, 4, seed=1)
    scores = iter([0.25, 0.75, 0.5, 0.75, 0.5, 0.5, 1.0])
    seen = []

    def planted_dev(model, layer, dv, targets, r, micro):
        seen.append(r.clone())
        return next(scores)

    monkeypatch.setattr(Z, "dev_iia", planted_dev)
    log: list[dict] = []
    r, info = Z.train_early(
        fake, 2, rows, dev, k=3, seed=5, steps=40, batch=4, micro=2, eval_every=5, patience=3, log=log
    )
    # reads at steps 4, 9, 14, 19, 24: 0.25, 0.75 (best), 0.5, 0.75 (a tie is no gain), 0.5 -> stop at step 24
    assert [e["step"] for e in info["evals"]] == [4, 9, 14, 19, 24] and info["stopped_at"] == 24
    assert info["best_step"] == 9 and info["best_dev_iia"] == 0.75 and torch.allclose(r, seen[1])
    assert [x["dev_iia"] for x in log if "dev_iia" in x] == [0.25, 0.75, 0.5, 0.75, 0.5]


def test_dev_iia_reads_the_argmax_under_the_edit():
    tok = T49.WordTok()
    fake = T49.FakeModel(tok, n_layers=6)
    dev = das_rows(tok, 5)
    r = D.random_basis(D_MODEL, 3, 1)
    tops = []
    for d_ in dev:
        lg = D.batch_logits(fake, 2, [d_["ids"]], [d_["pos"]], ((d_["delta"][None] @ r) @ r.T))
        tops.append(int(lg[0].argmax()))
    assert Z.dev_iia(fake, 2, dev, tops, r, micro=2) == 1.0
    assert Z.dev_iia(fake, 2, dev, [t + 1 for t in tops], r, micro=2) == 0.0


def test_train_fit_halves_the_micro_batch_on_cuda_oom(monkeypatch):
    calls = []

    def oom_at_8(model, layer, rows, dev, k, seed, steps, micro, shuffle, log, desc):
        calls.append(micro)
        log.append({"micro": micro})
        if micro > 4:
            raise torch.cuda.OutOfMemoryError("planted")
        return torch.eye(4)[:, :2], {"micro": micro}

    monkeypatch.setattr(Z, "train_early", lambda m, la, rows, dev, k, seed, steps, micro, shuffle, log, desc:
                        oom_at_8(m, la, rows, dev, k, seed, steps, micro, shuffle, log, desc))  # fmt: skip
    log: list[dict] = [{"earlier": 1}]
    _, info = Z.train_fit(None, 2, [], [], 2, 0, 3, 8, None, log, "x")
    assert calls == [8, 4] and info["oom_micro_tried"] == [8] and info["micro"] == 4
    assert log == [{"earlier": 1}, {"micro": 4}]  # the failed try's records dropped


# ---- the rules on planted numbers ------------------------------------------------------------------------------------


def planted_ident(own_rc: dict[int, float], n_rc: int = 350, k_lk: int = 4, shares=(0.1, 0.05, 0.05, 0.85)) -> dict:
    ci = lambda v: [v, v - 0.1, v + 0.1]  # noqa: E731
    return {"readers": {RC: {"n_pairs": n_rc, "test": {"own_iia": {k: ci(v) for k, v in own_rc.items()}}},
                        LK: {"k": k_lk}},
            "geometry": {f"R_{LK}_k{k_lk}": {"in_U": ci(shares[0]), "in_jpp25": ci(shares[1]), "in_we25": ci(shares[2]),
                                             "outside_union": ci(shares[3]), "cos2_U": 0.01}}}  # fmt: skip


def planted_addr(u_e: float) -> dict:
    return {"geometry": {"R_pos_k4": {"cos2_U": u_e, "cos2_W": 0.2}}}


@pytest.mark.parametrize(
    ("own", "n", "no_sub", "tested", "found"),
    [
        ({4: 0.1, 16: 0.2, 64: 0.3, 128: 0.4}, 350, True, True, False),
        ({4: 0.1, 16: 0.2, 64: 0.3, 128: 0.5}, 350, False, True, True),  # the bar is inclusive
        ({4: 0.1, 16: 0.6, 64: 0.3, 128: 0.4}, 350, True, True, True),  # the rule reads k = 128; found reads any k
        ({4: 0.1, 16: 0.2, 64: 0.3, 128: 0.4}, 299, False, False, False),  # fewer than 300 pairs: not tested
        ({4: 0.1, 16: 0.2, 64: 0.3, 128: 0.4}, 300, True, True, False),
    ],
)
def test_the_new_recall_rule(own, n, no_sub, tested, found):
    v = Z.rules_51(planted_ident(own, n_rc=n), planted_addr(0.7))
    assert (
        v["no_recall_subspace"] == no_sub and v["recall_rule_tested"] == tested and v["recall_found_q51_3_i"] == found
    )
    assert v["recall_own_iia_k128"] == own[128] and v["recall_pairs"] == n


def test_q51_3_lookup_shares_and_the_address_overlap():
    own = {4: 0.9, 16: 0.9, 64: 0.9, 128: 0.9}
    v = Z.rules_51(planted_ident(own, shares=(0.6, 0.1, 0.05, 0.3)), planted_addr(0.6))
    assert v["lookup_mostly"] == ["U"] and v["address_overlaps_U"] and v["lookup_shares"]["U"] == 0.6
    v = Z.rules_51(planted_ident(own, shares=(0.1, 0.1, 0.05, 0.8)), planted_addr(0.59))
    assert v["lookup_mostly"] == ["outside"] and not v["address_overlaps_U"]
    v = Z.rules_51(planted_ident(own, shares=(0.3, 0.3, 0.3, 0.4)), planted_addr(0.0))
    assert v["lookup_mostly"] == []


# ---- the seal ---------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_q51_3_only(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q51.2** x\n\nDan: small 70%\n\n**Q51.3** (51.3) DAS at scale\n- (i) ...\n- (ii) ...\n\nDan:{}\n\n**Q51.4** y\n\nDan: (a)\n"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    assert Z.dan_answer() == ""
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format(" (i) 9B 60%")))
    assert Z.dan_answer() == "(i) 9B 60%"
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("\nDan (27B): (i) 40%\n- (ii) outside")))
    assert "Dan (27B): (i) 40%" in Z.dan_answer() and "(ii) outside" in Z.dan_answer()
    monkeypatch.setattr(D.subprocess, "run", fake_git(blocks.format("")))
    with pytest.raises(AssertionError, match="sealed"):
        Z.unsealed()


# ---- the run, verdict and view stages on the fake model -------------------------------------------------------------


@pytest.fixture
def fake_env(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = T49.WordTok()
    ident = identity_pool(tok, 30, seed=1, source="main") + identity_pool(
        tok, 24, seed=3, sw=lambda i: {LK: 1, RC: int(i % 2 == 0)}
    )
    addr = []
    for i, c in enumerate(T49.c1_cases(tok, 30)):
        p = Q.position_pair(tok, c)
        p["stored_route"], p["stored_recall_kept"] = "position", int(i % 4 != 0)
        addr.append(p)
    Q.split_info(addr)
    c0_cands = c0_cases(tok, 30, seed=5, start=500)
    c1_cands = T49.c1_cases(tok, 40, seed=6)
    for j, c in enumerate(c1_cands):
        c["scene"] = f"C1-{600 + j:04d}"
    fake = T49.FakeModel(tok)
    u = D.random_basis(D_MODEL, 4, 11).numpy()
    w = D.random_basis(D_MODEL, 5, 12).numpy().astype(np.float64)
    info = {k: {"run": f"fake_{k}", "counts": {"read": 1, "kept": 1}, "per_reader": {"lookup": 1, "recall": 1}}
            for k in ("main", "clean", "routes")}  # fmt: skip

    def fake_pools(tok_, target, layer, n_gen):
        return {"identity": [json.loads(json.dumps(p)) for p in ident], "address": [json.loads(json.dumps(p)) for p in addr],
                "info": {**info, "address": {"pairs": len(addr)}, "address_last_stored_index": 30},
                "candidates": {"C0": c0_cands, "C1": c1_cands}}  # fmt: skip

    routes = [dict(c, scene=f"C2-{c['scene'][3:]}", condition="C2") for c in T49.c1_cases(tok, 4, seed=9)]
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", T49.FakeLens)
    monkeypatch.setattr(Z, "pools", fake_pools)
    monkeypatch.setattr(X, "competence", all_right)
    monkeypatch.setattr(D, "pointer_basis", lambda _t: (u, {"states_run": "fake", "rank": 4}))
    monkeypatch.setattr(Z, "load_w", lambda _t, _l: (w, {"run": "fake_47_2", "rank": 5, "file": "w.npz"}))
    monkeypatch.setattr(D, "routes_scenes", lambda *_a, **_k: (routes, {"used": 4}))
    monkeypatch.setattr(D, "K_JPP", (25, 30))
    monkeypatch.setattr(Z, "KS", {LK: (2, 4), RC: (2, 4, 8)})
    monkeypatch.setattr(Z, "KS_POS", (2, 4))
    monkeypatch.setattr(Z, "K_RECALL_RULE", 8)
    monkeypatch.setattr(Z, "ID_MIN", 30)  # lookup 54, recall 20 + 12 pairs: no identity top-up (unit-tested above)
    monkeypatch.setattr(Z, "POS_MIN", 40)  # 30 stored: the address is topped up with the C1 candidates
    # the fake model's top token is never a locker digit: every second candidate's route planted as the position one
    monkeypatch.setattr(R, "classify", lambda top, c: "position" if Z.scene_index(c["scene"]) % 2 == 0 else "identity")
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x51_das")
    monkeypatch.setattr(Z, "MAIN_RUN", {pins.TARGET: "fake_main"})
    monkeypatch.setattr(Z, "CLEAN_RUN", {pins.TARGET: "fake_clean"})
    monkeypatch.setattr(Z, "ROUTES_RUN", {pins.TARGET: "fake_routes"})
    monkeypatch.setattr(Z, "RUNS", {pins.TARGET: "fake"})
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(R, "RESULTS", tmp_path / "x6_routes")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Z, "SPEC", tmp_path / "batch51.yaml")
    Z.SPEC.write_text("")
    (tmp_path / "w.npz").write_text("")
    for d_, fs in ((tmp_path / "x0" / "fake_main", ("manifest.json", "cases.jsonl", "outcomes.jsonl", "gate.json")),
                   (tmp_path / "x0" / "fake_clean", ("manifest.json", "cases.jsonl", "outcomes.jsonl", "gate.json")),
                   (tmp_path / "x6_routes" / "fake_routes", ("manifest.json", "cases.jsonl", "outcomes.jsonl", "competence.jsonl", "gate.json"))):  # fmt: skip
        d_.mkdir(parents=True)
        for f in fs:
            (d_ / f).write_text("")
    return SimpleNamespace(tok=tok, fake=fake, ident=ident, addr=addr, u=u, w=w, prefix=pins.RUN_PREFIX)


def test_run_stage_end_to_end_on_the_fake_model(fake_env):
    from bridge_jspace import pins
    from scripts.exp04_brew_parts import AddRows

    la = X.PREDICTED[pins.TARGET]
    out = Z.stage_run(f"{fake_env.prefix}fake_51", "test", steps=3)
    assert not any(p.name.startswith(("verdict", "view")) for p in out.iterdir())  # sealed
    m = json.loads((out / "manifest.json").read_text())
    assert "sealed" in m and m["switches"]["target"] == pins.TARGET and m["ks"]["recall"] == [2, 4, 8]
    assert set(m["stops"]) == {f"{p}_{w}_k{k}" for p in ("R", "shuf") for w, ks in Z.KS.items() for k in ks} | {
        f"{p}_pos_k{k}" for p in ("R", "shuf") for k in Z.KS_POS
    }
    pairs = json.loads((out / "pairs.json").read_text())
    assert pairs["identity_topup"] == {"needed": False}
    assert pairs["address_topup"]["needed"] and pairs["address"]["pairs"] == 40  # topped up to POS_MIN exactly
    assert (
        sum(r["part"] == "address" for r in X.read_jsonl(out / "topup.jsonl"))
        == pairs["address_topup"]["gate"]["scenes_read"]
    )
    ident = X.read_jsonl(out / "cases.jsonl")
    arms = Z.identity_arms()
    assert arms[:2] == ["none", "whole"] and "R_pos_k4" in arms and "shuf_PM_k8" in arms and "rand_k8" in arms
    rows = X.read_jsonl(out / "outcomes.jsonl")
    held = [p for p in ident if p["split"] != "train"]
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (p["scene"], w, a) for p in held for w in X.READERS for a in arms
    }
    assert all(
        r["in_pairs"] == next(p for p in ident if p["scene"] == r["scene"])["in_pairs"][r["reader"]] for r in rows[:50]
    )
    blob = torch.load(out / "R.pt")
    for key, r in blob["R"].items():
        k = int(key.rsplit("k", 1)[1])
        assert r.shape == (D_MODEL, k) and torch.allclose(r.T @ r, torch.eye(k), atol=1e-4)
    assert torch.equal(blob["R"]["R_pos_k4"], blob["R_address"]["R_pos_k4"])
    # one identity read recomputed: R_recall at k = 4 written at the bridge of the O prompt
    st = torch.load(out / f"states_L{la}.pt")
    p0 = next(p for p in ident if p["split"] == "test")
    i0 = st["scenes"].index(p0["scene"])
    r4 = blob["R"][f"R_{RC}_k4"]
    part = (st["delta"][i0 : i0 + 1] @ r4) @ r4.T
    ids = p0["readers"][RC]["ids"]
    lg = fake_env.fake.generate_batch(torch.tensor([ids["org"] + p0["space"]]), 1, [{la: AddRows(part, [p0["pos"]])}],
                                      first_logits=True)[1]  # fmt: skip
    rec = next(r for r in rows if r["scene"] == p0["scene"] and r["reader"] == RC and r["arm"] == f"R_{RC}_k4")
    assert rec["top"] == int(lg[0].argmax())
    geo = X.read_jsonl(out / "geometry.jsonl")
    assert len(geo) == len(ident) * len(blob["R"]) and all(0 <= g["in_W"] <= 1 + 1e-6 for g in geo)
    a_rows = X.read_jsonl(out / "address" / "outcomes.jsonl")
    assert {r["arm"] for r in a_rows} == set(Q.arm_names(Z.KS_POS))
    assert (out / "routes.jsonl").exists() and json.loads((out / "address" / "manifest.json").read_text())["ks"] == [
        2,
        4,
    ]


def test_verdict_and_view_are_sealed_until_dans_answer(fake_env, monkeypatch):
    out = Z.stage_run(f"{fake_env.prefix}fake_51s", "test", steps=1)
    monkeypatch.setattr(Z, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_verdict([out.name], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_view([out.name])
    assert not any(p.name.startswith(("verdict", "view")) for p in Z.RESULTS.iterdir())


def test_verdict_and_view_on_the_fake_run(fake_env, monkeypatch):
    out = Z.stage_run(f"{fake_env.prefix}fake_51v", "test", steps=2)
    monkeypatch.setattr(Z, "dan_answer", lambda rev="HEAD": "(i) 9B 60%")
    v_out = Z.stage_verdict([out.name], n_boot=50)
    blob = json.loads((v_out / "verdict.json").read_text())
    mv = blob["models"][0]
    assert blob["dan"] == "(i) 9B 60%" and set(mv["rules_48_1"]) >= {"a", "b", "c", "d"}
    assert mv["rules_49_8"]["label"] in Q.LABELS and not mv["rules_48_1"]["fallback_tested"]  # the lookup has no k = 64
    # recomputed from the raw rows: the recall's own-IIA at k = 8 on its test pairs
    rows = [
        r for r in X.read_jsonl(out / "outcomes.jsonl") if r["split"] == "test" and r["reader"] == RC and r["in_pairs"]
    ]
    own8 = np.mean([r["switched"] for r in rows if r["arm"] == f"R_{RC}_k8"])
    assert mv["rules_51_3"]["recall_own_iia_k128"] == pytest.approx(own8)
    assert mv["rules_51_3"]["no_recall_subspace"] is False  # fewer than 300 recall pairs: not tested
    assert mv["rules_51_3"]["recall_rule_tested"] is False
    md = (v_out / "verdict.md").read_text()
    assert "As computed" in md and "51.3 rule: not tested" in md and (v_out / f"{out.name}.png").exists()
    view = Z.stage_view([out.name])
    text = (view / "view.md").read_text()
    assert text.count("#### ") == 10 and "⟦bridge:" in text and "⟦moved:" in text
    n_arms = len(Z.identity_arms()) + len(Q.arm_names(Z.KS_POS))
    assert text.count("random rows of") == n_arms


def test_coverage_run_without_a_clean_source_and_its_verdict(fake_env, monkeypatch):
    """Batch 52 (Lightning ports, coordinator 10:15 option A): a target without a clean-design run runs on the other
    sources; its manifest carries the 'adapted design' label, and verdict --coverage reads it without the seal ('no
    prediction', x52_das51-<UTC>/, the label in verdict.md); a design run is refused under --coverage."""
    from bridge_jspace import pins

    label = "adapted design: the clean one-pick source left out (test)"
    monkeypatch.setattr(Z, "CLEAN_RUN", {})
    monkeypatch.setattr(Z, "NO_CLEAN", {pins.TARGET: label})
    monkeypatch.setattr(Z, "RUNS", {})
    monkeypatch.setattr(Z, "COVERAGE_RUNS", {pins.TARGET: f"{fake_env.prefix}fake_51c"})
    monkeypatch.setattr(Z, "dan_answer", lambda rev="HEAD": (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = Z.stage_run(f"{fake_env.prefix}fake_51c", "test", steps=1)
    m = json.loads((out / "manifest.json").read_text())
    assert m["adapted"] == label and m["sources"]["clean"] == label
    assert not any("fake_clean" in k for k in m["inputs"])
    v_out = Z.stage_verdict([out.name], n_boot=50, coverage=True)
    assert v_out.name.startswith("x52_das51-")
    blob = json.loads((v_out / "verdict.json").read_text())
    assert blob["dan"].startswith(Z.NO_PREDICTION)
    md = (v_out / "verdict.md").read_text()
    assert f"**{label}**" in md and "batch 52 coverage" in md and "Q51.3, Dan:" not in md
    with pytest.raises(AssertionError, match=r"51\.3 coverage runs are"):
        Z.stage_verdict(["qwen35_9b_x51_3"], n_boot=50, coverage=True)


def test_pools_leave_the_clean_source_out_for_a_target_without_one(monkeypatch):
    """pools() on a target absent from CLEAN_RUN: no clean pairs, the label in its info (the stored runs stubbed)."""
    monkeypatch.setattr(Z, "CLEAN_RUN", {})
    monkeypatch.setattr(Z, "NO_CLEAN", {"t": "adapted design (test)"})
    monkeypatch.setattr(Z, "MAIN_RUN", {"t": "main"})
    monkeypatch.setattr(Z, "ROUTES_RUN", {"t": "routes"})
    monkeypatch.setattr(Z, "generated_scenes", lambda tok, n: [])
    calls: list[str] = []

    def x0_pool(tok, run, layer, alt, src):
        calls.append(run)
        return [{"src": src}], {"run": run}

    monkeypatch.setattr(Z, "x0_pool", x0_pool)
    monkeypatch.setattr(Z, "routes_pool", lambda tok, run, la, gen: ([{"src": "routes"}], {"last_stored_index": 1}))
    monkeypatch.setattr(Q, "select_pairs", lambda tok, run, layer: ([], {"pairs": 0}))
    monkeypatch.setattr(Z, "stored_routes", lambda run, layer, cond: (None, {}, {"C1-0003": {}}))
    pl = Z.pools(None, "t", 14, 10)
    assert calls == ["main"] and [p["src"] for p in pl["identity"]] == ["main", "routes"]
    assert pl["info"]["clean"]["absent"] == "adapted design (test)"
    assert pl["info"]["clean"]["per_reader"] == {"lookup": 0, "recall": 0}
