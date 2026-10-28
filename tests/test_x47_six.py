"""Batch 47, test 47.2 (scripts/x47_six.py): the six-slot scene generator (texts, and the target's tokenizer where it is
cached), the fit, PCA and shift vectors on planted data, the rule on planted outcomes, the seal, and the run stage end
to end on a tiny fake causal model (CPU, with the five-slot fallback). No real model."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_six as Q

LK, RC = X.LOOKUP, X.RECALL
ANIMALS = ["ant", "bee", "cat", "cow", "crow", "duck", "fox", "frog", "goat", "hen", "owl", "pig", "yak", "eel"]
PEOPLE = ["Ann", "Ben", "Cara", "Dan", "Eve", "Finn", "Gus"]
LEGS = {a: 6 if a in ("ant", "bee") else 2 if a in ("crow", "duck", "hen", "owl") else 0 if a == "eel" else 4
        for a in ANIMALS}  # fmt: skip


# ---- the scenes (texts) ---------------------------------------------------------------------------------------------


@pytest.mark.parametrize("n", [6, 5])
def test_move_scenes_every_pair(n):
    for i, j in Q.pairs(n):
        rng = random.Random(f"t|{i}-{j}")
        for _ in range(5):
            t = Q.move_text(rng, ANIMALS, PEOPLE, n, i, j)
            assert Q.text_checks(t) == []
            so, ss = Q.sentences(t["o"]), Q.sentences(t["s"])
            assert len(so) == n + 3 and all(s.startswith("The locker of the ") for s in so[:n])  # locker-first
            assert all(" picked the " in s for s in so[n:])  # three pick sentences
            assert so[:n] == [f"The locker of the {x} is {v}." for x, v in zip(t["items"], t["values"], strict=True)]
            assert ss[j - 1] == f"The locker of the {t['bridge']} is {t['new']}."  # moved to slot j, a new number
            assert ss[i - 1] == f"The locker of the {t['items'][j - 1]} is {t['values'][j - 1]}."  # swapped in
            assert so[n:] == ss[n:] and t["bridge"] == t["cf_bridge"]  # the picks (and the bridge) are O's
            assert len(set(t["values"])) == n and t["new"] not in t["values"] and 1 <= t["new"] <= 9
            assert t["expect"] == {"identity": t["values"][i - 1], "position": t["values"][j - 1], "value": t["new"],
                                   "original": t["values"][i - 1]}  # fmt: skip
            assert f"{t['asked']} picked the {t['bridge']}." in t["o"] and t["move"] == [i, j]


def test_c0_scenes_swap_only_the_asked_pick():
    rng = random.Random(0)
    got = [t for t in (Q.c0_text(rng, ANIMALS, PEOPLE, LEGS, 6) for _ in range(60)) if t is not None]
    assert 10 < len(got) < 60  # some draws dropped: the same number of legs
    for t in got:
        assert Q.text_checks(t) == [] and LEGS[t["bridge"]] != LEGS[t["cf_bridge"]]
        assert t["o"].replace(f"{t['asked']} picked the {t['bridge']}.", f"{t['asked']} picked the {t['cf_bridge']}.") \
            == t["s"]  # fmt: skip
        assert t["expect"]["switch"] == t["values"][t["items"].index(t["cf_bridge"])]
        assert t["move"] == [t["items"].index(t["bridge"]) + 1, t["items"].index(t["cf_bridge"]) + 1]


def test_text_checks_catch_leaks():
    t = Q.move_text(random.Random(3), ANIMALS, PEOPLE, 6, 2, 5)
    assert Q.text_checks(t) == []
    leak = {**t, "o": t["o"].replace(f" is {t['values'][0]}.", f" is {t['new']}.", 1)}
    assert any("new digit" in b for b in Q.text_checks(leak))
    first = Q.sentences(t["o"])
    early = {
        **t,
        "o": " ".join([first[-1], *first[:-1]]),
        "s": " ".join([Q.sentences(t["s"])[-1], *Q.sentences(t["s"])[:-1]]),
    }
    assert any("first mention" in b for b in Q.text_checks(early))  # a pick before its locker sentence
    third = t["s"].replace(Q.sentences(t["s"])[3], "The locker of the yak is 1.")
    assert any("differ" in b for b in Q.text_checks({**t, "s": third}))


def test_first_mentions_and_pick_index():
    ctx = "The locker of the cat is 2. The locker of the cow is 3. Ann picked the cow. Ben picked the cat."
    assert Q.first_mentions_are_lockers(ctx, ["cat", "cow"])
    assert not Q.first_mentions_are_lockers("Ann picked the cow. The locker of the cow is 3.", ["cow"])
    assert Q.pick_index(ctx, "Ben") == 3 and Q.pick_index(ctx, "Ann") == 2


def test_build_cases_on_the_tokenizer():
    """With the target's tokenizer (skipped where it is not cached): every pair filled, the bridge one token at one
    index in O and S, distinct slot digit tokens, the routes' tokens are the slots' digits, the asked pick's layout."""
    from scripts import x45m

    try:
        tok = x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    cases, _ = Q.build_cases(tok, 6, n_cand=2, n_c0=4)
    moves = [c for c in cases if c["condition"] == "M"]
    assert len(moves) == 60 and sum(c["condition"] == "C0" for c in cases) == 4
    assert {tuple(c["move"]) for c in moves} == set(Q.pairs(6))
    for c in cases:
        ids = c["readers"][LK]["ids"]
        assert len(ids["org"]) == len(ids["alt"]) and tok.decode([ids["org"][c["pos"]]]).strip() == c["bridge"]
        assert c["readers"][RC]["ids"]["org"][: c["pos"] + 1] == ids["org"][: c["pos"] + 1]
        assert len(set(c["slot_tokens"])) == 6 and c["layout"].startswith("LLLLLL")
        i, j = c["move"]
        if c["condition"] == "M":
            assert c["new_token"] not in c["slot_tokens"]
            assert c["route_tokens"]["identity"] == c["slot_tokens"][i - 1]
            assert c["route_tokens"]["position"] == c["slot_tokens"][j - 1]
            assert c["route_tokens"]["value"] == c["new_token"] == c["readers"][LK]["tok_b"]
            assert c["readers"][RC]["tok_A"] == c["readers"][RC]["tok_b"]  # the same bridge: the recall cannot switch
            assert ids["org"][c["pos"]] == ids["alt"][c["pos"]]
        else:
            assert c["readers"][LK]["tok_b"] == c["slot_tokens"][j - 1]


# ---- the fit ------------------------------------------------------------------------------------------------------


def planted_states(n=6, d=40, per=30, seed=0, noise=0.05):
    """States = slot mean + layout-group offset + noise; every slot in every group; one singleton group."""
    g = np.random.default_rng(seed)
    means = g.normal(size=(n, d))
    offs = {grp: g.normal(size=d) * 5 for grp in ("L", "L.", "L..")}
    h, slots, groups = [], [], []
    for k in range(1, n + 1):
        for r in range(per):
            grp = ("L", "L.", "L..")[r % 3]
            h.append(means[k - 1] + offs[grp] + noise * g.normal(size=d))
            slots.append(k)
            groups.append(grp)
    h.append(g.normal(size=d) * 100)  # a group of one: dropped
    slots.append(1)
    groups.append("lonely")
    return np.array(h), slots, groups, means


def test_fit_recovers_planted_slot_means_and_drops_singletons():
    h, slots, groups, means = planted_states()
    fit = Q.fit_slots(h, slots, groups, 6)
    assert fit["dropped_singletons"] == 1 and fit["states"] == len(h) - 1 and fit["per_slot"]["1"] == 30
    for i, t in Q.pairs(6):
        got, want = fit["mu"][t - 1] - fit["mu"][i - 1], means[t - 1] - means[i - 1]
        assert np.linalg.norm(got - want) < 0.05 * np.linalg.norm(want)
        w = fit["W"]
        assert np.linalg.norm(got - w @ (w.T @ got)) < 1e-8 * np.linalg.norm(got)  # mu_t - mu_i lies in W
    assert fit["W"].shape == (40, 5) and np.allclose(fit["W"].T @ fit["W"], np.eye(5), atol=1e-8)


def test_pca_reads_a_line_as_monotone_and_first_vs_rest_as_not():
    g = np.random.default_rng(1)
    a, b = g.normal(size=30), g.normal(size=30)
    line = np.stack([b + k * a for k in range(1, 7)])
    p = Q.pca_reading(line)
    assert p["cumulative"][0] > 0.999 and abs(p["spearman_pc1_slot"]) > 0.999 and p["monotone"]
    first = np.stack([a] + [np.zeros(30)] * 5)  # one bit: slots 2-6 tie on PC1
    p = Q.pca_reading(first)
    assert p["cumulative"][0] > 0.99 and abs(p["spearman_pc1_slot"]) < 0.9 and not p["monotone"]
    bent = np.stack([b + k * a + (k == 4) * 10 * g.normal(size=30) for k in range(1, 7)])
    assert Q.pca_reading(bent)["cumulative"][0] < 0.99 and len(Q.pca_reading(bent)["cumulative"]) == 3


def test_shift_vectors_telescope():
    mu = np.random.default_rng(2).normal(size=(6, 8))
    sv = Q.shift_vectors(mu)
    assert np.allclose(sv["v"], (mu[5] - mu[0]) / 5) and np.allclose(sv["v12"], mu[1] - mu[0])
    assert np.allclose(sv["vno12"], (mu[5] - mu[1]) / 4)
    geo = Q.geometry(mu)
    assert len(geo["step_norms"]) == 5 and -1 <= geo["cos_v_v12"] <= 1


def test_arms_and_their_vectors():
    n = 6
    assert len(Q.arm_list(3, n)) == 6 + 2 * (5 + 1 + 3 + 1)
    first, last = Q.arm_list(1, n), Q.arm_list(n, n)
    assert not any(a["arm"] == "vrev" for a in first) and not any(a["arm"] in ("v", "v12", "vno12") for a in last)
    assert {a["target"] for a in Q.arm_list(4, n) if a["arm"] == "write" and a["s"] == 2} == {1, 2, 3, 5, 6}
    assert all(a["target"] == 5 for a in Q.arm_list(4, n) if a["arm"] in ("v", "v12", "vno12"))
    g = torch.Generator().manual_seed(0)
    mu, x = torch.randn(n, 16, generator=g), torch.randn(16, generator=g)
    sv = {k: torch.tensor(v / np.linalg.norm(v), dtype=torch.float32) for k, v in Q.shift_vectors(mu.numpy()).items()}
    r = Q.rand_dir("M6-12-001", 16)
    assert torch.equal(r, Q.rand_dir("M6-12-001", 16)) and not torch.equal(r, Q.rand_dir("M6-12-002", 16))
    parts = {a: 0.5 * x for a in ("no_slot", "no_slot_rand", "no_U", "no_U_rand")}
    for a in Q.arm_list(4, n):
        vec = Q.arm_vector(a, 4, x, parts, 3.0, mu, sv, r)
        if a["arm"] == "none":
            assert vec is None
        elif a["arm"] in ("write", "random", *Q.SHIFTS):
            assert vec is not None and abs(float(vec.norm()) - 3.0 * a["s"]) < 1e-4
    w = Q.arm_vector({"arm": "write", "s": 1, "target": 2}, 4, x, parts, 3.0, mu, sv, r)
    d = mu[1] - mu[3]
    assert w is not None and torch.allclose(w, 3.0 * d / d.norm(), atol=1e-6)
    back = Q.arm_vector({"arm": "vrev", "s": 2}, 4, x, parts, 3.0, mu, sv, r)
    on = Q.arm_vector({"arm": "v", "s": 2}, 4, x, parts, 3.0, mu, sv, r)
    assert back is not None and on is not None and torch.allclose(back, -on)


# ---- the rule on planted outcomes -------------------------------------------------------------------------------------


def planted_rows(n, answer, per=10):
    """Test-half lookup rows: per start slot i, `per` scenes (move i -> the next slot), every arm of arm_list; the
    slot answered by answer(arm, i, j) (None: other)."""
    rows = []
    for i in range(1, n + 1):
        for k in range(per):
            j = i % n + 1
            scene = f"M{n}-{i}{j}-{k:03d}"
            for a in Q.arm_list(i, n):
                slot = answer(a, i, j)
                route = "identity" if slot == i else "position" if slot == j else "other"
                rows.append({"scene": scene, "condition": "M", "slots": n, "i": i, "j": j, "entity": f"e{(i * per + k) % 12}",
                             "reader": LK, "arm": a["arm"], "s": a.get("s"), "target": a.get("target"), "slot": slot,
                             "route": route, "kept": int(slot == i), "switched": 0})  # fmt: skip
    return rows


MONOTONE = {"monotone": True}
FLAT = {"monotone": False}


def ordinal_answer(a, i, j):
    if a["arm"] in ("write", "v", "vrev", "v12", "vno12"):
        return a["target"]
    return j if a["arm"] in ("whole", "no_U_rand", "no_slot_rand") else i


def test_rule_reads_an_ordinal_code():
    n = 6
    cells = Q.model_cells(planted_rows(n, ordinal_answer), n, 200)
    r = Q.rule(cells, MONOTONE, n, 2)
    assert r["complete"] and r["v_works_from"] == 5 and r["random_pooled"] == 0.0
    assert r["holding"] == ["ordinal"] and r["label"] == "ordinal"
    assert cells["removal"]["slot_cut_beyond_random"][0] == 1.0  # W's removal sends every position answer away
    assert Q.rule(cells, FLAT, n, 2)["label"] != "ordinal"  # the PCA clause is needed


def test_rule_reads_first_vs_rest():
    def answer(a, i, j):
        if a["arm"] == "v":
            return a["target"] if i == 1 else i
        if a["arm"] == "write":
            return a["target"] if 1 in (i, a["target"]) else i
        if a["arm"] in ("whole", "no_U", "no_U_rand", "no_slot_rand"):
            return j
        return i

    n = 6
    r = Q.rule(Q.model_cells(planted_rows(n, answer), n, 200), FLAT, n, 2)
    assert r["v_by_start"][1] == 1.0 and r["clauses"]["categorical"] and r["label"] == "categorical, first vs rest"

    # U's removal costs position on moves among 2-6 beyond random: no longer categorical
    def costly(a, i, j):
        return i if a["arm"] == "no_U" and min(i, j) >= 2 else answer(a, i, j)

    assert not Q.rule(Q.model_cells(planted_rows(n, costly), n, 200), FLAT, n, 2)["clauses"]["categorical"]


def test_rule_reads_slot_specific_codes():
    def answer(a, i, j):
        if a["arm"] == "write":
            return a["target"]
        if a["arm"] == "v":
            return a["target"] if i in (1, 2) else i  # the shift works from 2 of 5 start slots only
        return j if a["arm"] == "whole" else i

    n = 6
    r = Q.rule(Q.model_cells(planted_rows(n, answer), n, 200), MONOTONE, n, 2)
    assert r["pairs_reaching"] == 30 and r["v_works_from"] == 2 and r["holding"] == ["slot-specific"]


def test_rule_with_nothing_moving_holds_no_label():
    n = 6
    r = Q.rule(Q.model_cells(planted_rows(n, lambda a, i, j: i), n, 200), MONOTONE, n, 2)
    assert r["holding"] == [] and r["label"] == "none of the three"


def test_rule_at_five_slots_needs_every_start():
    n = 5

    def answer(a, i, j):
        if a["arm"] == "v":
            return a["target"] if i != 3 else i  # 3 of 4 start slots
        return ordinal_answer(a, i, j)

    r = Q.rule(Q.model_cells(planted_rows(n, answer), n, 200), MONOTONE, n, 2)
    assert r["v_needs"] == 4 and r["v_works_from"] == 3 and not r["clauses"]["ordinal"]
    assert Q.rule(Q.model_cells(planted_rows(n, ordinal_answer), n, 200), MONOTONE, n, 2)["clauses"]["ordinal"]


# ---- the seal -----------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_q47_2(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.1** (47.1) x\n\nDan: (a) 70%\n\n**Q47.2** (47.2) y\n- ordinal: z\n\nAnswer per model: 9B; Muse.\n\nDan:{}\n\n**Q47.3** w\n\nDan: (b)\n"
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format("")))
    assert Q.dan_answer() == ""
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format(" 9B ordinal 60%; Muse categorical 70%")))
    assert Q.dan_answer() == "9B ordinal 60%; Muse categorical 70%"


def test_verdict_and_examples_refuse_while_sealed(monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_verdict(["qwen35_9b_x47_2"])
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_examples(["qwen35_9b_x47_2"])


# ---- the run stage on a fake model (CPU) ------------------------------------------------------------------------------


class WordTok:
    """Words with their leading whitespace as tokens, ids from a shared vocab (as tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (as tests/test_x45p.py): each block mixes the running mean
    of the positions so far into every position; an edit acts on a block's output."""

    def __init__(self, tok: WordTok, vocab: int, n_layers: int = 33, d: int = 32):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.device = tok, n_layers, torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

    def forward(self, ids, edits):
        h = self.emb[torch.as_tensor(ids)]
        states = {}
        for layer in range(self.n_layers):
            h = h + 0.1 * torch.cumsum(h, 0) / torch.arange(1, h.shape[0] + 1)[:, None]
            if layer in edits:
                h = edits[layer](h)
            states[layer] = h.clone()
        return self.unemb @ h[-1], states

    def run(self, ids, edits=None, record=()):
        logits, states = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: states[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts


def wrap(context: str, question: str) -> str:
    return f"<|im_start|>user\n{context}\n{question}<|im_end|>\nAnswer:"


def fake_case(tok: WordTok, t: dict, scene: str) -> dict:
    """A case as encode_text makes it, on the word tokenizer (the bridge token is ' <item>.')."""
    one = lambda s: tok(s).input_ids[0]  # noqa: E731
    q = {LK: R.LOOKUP_Q.format(p=t["asked"]), RC: R.RECALL_Q.format(p=t["asked"])}
    s_lk = t["expect"]["switch"] if "switch" in t["expect"] else t["expect"]["value"]
    answers = {LK: (t["expect"]["original"], s_lk), RC: (LEGS[t["bridge"]], LEGS[t["cf_bridge"]])}
    readers, pos = {}, None
    for w in X.READERS:
        ids = {}
        for v, ctx, item in (("org", t["o"], t["bridge"]), ("alt", t["s"], t["cf_bridge"])):
            text = wrap(ctx, q[w])
            enc = tok(text, return_offsets_mapping=True)
            at = text.index(f"{t['asked']} picked the {item}.") + len(f"{t['asked']} picked the ")
            p = next(k for k, (a, b) in enumerate(enc.offset_mapping) if a <= at < b)
            assert pos is None or p == pos
            pos, ids[v] = p, enc.input_ids
        a, b = answers[w]
        readers[w] = {"question": q[w], "answer": str(a), "cf_answer": str(b), "ids": ids, "tok_A": one(str(a)),
                      "tok_b": one(str(b))}  # fmt: skip
    routes = {k: one(str(v)) for k, v in t["expect"].items() if k != "switch"}
    pick = Q.pick_index(t["o"], t["asked"])
    return {"scene": scene, "condition": t["condition"], "rendering": "chat", "domain": "animals", "bridge": t["bridge"],
            "cf_bridge": t["cf_bridge"], "context": t["o"], "cf_context": t["s"], "pos": pos, "space": [],
            "expect": t["expect"], "route_tokens": routes, "readers": readers, "slots": t["slots"], "move": t["move"],
            "items": t["items"], "values": t["values"], "new": t["new"],
            "slot_tokens": [one(str(v)) for v in t["values"]], "new_token": None if t["new"] is None else one(str(t["new"])),
            "asked": t["asked"], "pick_index": pick, "layout": Q.P.layout(t["o"], pick), "picks": t["picks"]}  # fmt: skip


def fake_cases(tok: WordTok, n: int, per_pair: int = 4, c0: int = 3) -> list[dict]:
    out = []
    for i, j in Q.pairs(n):
        rng = random.Random(f"f|{n}|{i}-{j}")
        out += [
            fake_case(tok, Q.move_text(rng, ANIMALS, PEOPLE, n, i, j), f"M{n}-{i}{j}-{k:03d}") for k in range(per_pair)
        ]
    rng = random.Random(f"f|{n}|C0")
    while sum(c["condition"] == "C0" for c in out) < c0:
        t = Q.c0_text(rng, ANIMALS, PEOPLE, LEGS, n)
        if t is not None:
            out.append(fake_case(tok, t, f"C0{n}-{len(out):04d}"))
    return out


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    for d in range(10):
        tok(str(d))
    cases = {n: fake_cases(tok, n) for n in Q.SLOTS_TRY}
    fake = FakeModel(tok, vocab=len(tok.vocab) + 8)

    def competence(model, cs, digits, ws):  # six slots miss the gate (the recall reads O wrong half the time)
        rows = []
        for k, c in enumerate(cs):
            for w in X.READERS:
                for v in ("org", "alt"):
                    ok = not (c["slots"] == 6 and w == RC and v == "org" and k % 2)
                    rows.append({"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "greedy": "",
                                 "said": "", "right": ok, "read_right": ok, "ws_skipped": 0, "cand_right": ok})  # fmt: skip
        return rows

    g = torch.Generator().manual_seed(5)
    u_old, _ = torch.linalg.qr(torch.randn(32, 4, generator=g))
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(X, "competence", competence)
    monkeypatch.setattr(Q, "build_cases", lambda tok_, n: (cases[n], {}))
    monkeypatch.setattr(Q, "old_pointer", lambda target: u_old.numpy().astype(np.float64))
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x47_six")
    name = f"{pins.RUN_PREFIX}fake_x47_2"
    return SimpleNamespace(tok=tok, cases=cases, out=Q.stage_run(name, "test"), name=name)


def test_run_falls_back_to_five_and_writes_per_item_outputs(fake_run):
    out = fake_run.out
    m = json.loads((out / "manifest.json").read_text())
    assert m["slots"] == 5 and m["tested"] and m["fallback"]["six_failed_gate"]
    assert m["fallback"]["note"].startswith("six slots failed")
    gate = json.loads((out / "gate.json").read_text())
    assert not gate["gates"]["6"]["M"]["pass"] and gate["gates"]["5"]["M"]["pass"]
    assert not (out / "verdict.md").exists() and not list(out.glob("verdict*"))  # sealed
    split = json.loads((out / "split.json").read_text())
    assert len(split["fit"]) == len(split["test"]) == 20 * 2 and len(split["c0"]) == 3
    assert not set(split["fit"]) & set(split["test"])
    fit = np.load(out / "fit.npz")
    assert fit["mu"].shape == (5, 32) and fit["W"].shape == (32, 4) and fit["h"].shape == (80, 32)
    assert m["unit"]["value"] > 0 and m["fit"]["W_rank"] == 4
    rows = X.read_jsonl(out / "outcomes.jsonl")
    cases = {c["scene"]: c for c in fake_run.cases[5]}
    want = sum(2 * len(Q.arm_list(cases[s]["move"][0], 5)) for s in split["test"]) + 2 * 2 * 3
    assert len(rows) == want
    assert {r["scene"] for r in rows if r["condition"] == "M"} == set(split["test"])
    lk = [r for r in rows if r["reader"] == LK and r["condition"] == "M"]
    assert all(r["route"] in Q.ROUTES for r in lk) and all(r["slot"] in (None, 1, 2, 3, 4, 5) for r in lk)
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 40 and all(0 <= r["share_slot"] <= 1 + 1e-6 for r in norms)


def test_verdict_and_examples_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda rev="HEAD": "9B ordinal 60%")
    res = Q.model_result(fake_run.name, n_boot=50)
    assert res["status"] == "tested" and res["slots"] == 5 and set(res["rules"]) == {"1", "2"}
    assert res["label"] in ("not interpretable", "none of the three", *Q.LABEL_TEXT.values())
    lines = Q.report_lines([res, Q.model_result("muse30_x47_2")], "9B ordinal 60%", 50)
    text = "\n".join(lines)
    assert "Dumbest way 1 first" in text and "pending" in text and text.index("routes split") < text.index("## Verdict")
    ex = Q.examples_lines([fake_run.name], decode=fake_run.tok.decode)
    assert sum(line.startswith("### ") for line in ex) == 10 and any("⟦" in line for line in ex)
