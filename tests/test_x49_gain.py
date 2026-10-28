"""Batch 49, test 49.1 (scripts/x49_gain.py): the arm algebra (the 5x5 grid, the random corners, the no-U arm and its
twin, the K = 100 corners), the parts on synthetic tensors, every arm end to end on a tiny fake causal model (CPU), the
sealed run stage, the rules (a), (b), (a'), (c) on planted numbers and on planted runs, the loss flag, and the seal. No
real model."""

import json
from types import SimpleNamespace

import pytest
import torch

from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x49_gain as G

LK, RC = X.LOOKUP, X.RECALL
L = X.PREDICTED["qwen3.6-27b"]  # the default target's layer (32)
D = 48


def _orth(d: int, r: int, seed: int) -> torch.Tensor:
    q, _ = torch.linalg.qr(torch.randn(d, r, generator=torch.Generator().manual_seed(seed)))
    return q


# ---- the arms ------------------------------------------------------------------------------------------------------


def test_arm_names_cover_the_design():
    narrow, wide = G.arm_names(False), G.arm_names(True)
    assert len(narrow) == 25 + 4 + 2 == len(set(narrow)) and len(wide) == len(narrow) + 8 == len(set(wide))
    assert narrow[0] == G.NONE == "J(0,0)" and G.WHOLE == "J(1,1)" in narrow
    assert {"R(0,1)", "R(1,0)", "R(2,0)", "R(0,2)", "J(0,2)-U", "J(0,2)-RU"} <= set(narrow)
    assert wide[: len(narrow)] == narrow and {"J100(2,0)", "R100(0,2)"} <= set(wide)
    assert G.WIDE_TARGETS == ("qwen3.5-9b",)


def test_arm_algebra():
    g = torch.Generator().manual_seed(0)
    n = 5
    delta, pj, rj, up, ru = (torch.randn(n, D, generator=g) for _ in range(5))
    p100, r100 = torch.randn(n, D, generator=g), torch.randn(n, D, generator=g)
    arms = G.arm_deltas(delta, pj, rj, up, ru, (p100, r100))
    assert list(arms) == G.arm_names(True)
    for a in G.GAINS:
        for b in G.GAINS:
            assert torch.allclose(arms[G.gname("J", a, b)], a * pj + b * (delta - pj))
    assert torch.allclose(arms["J(1,1)"], delta) and not arms["J(0,0)"].any()
    assert torch.allclose(arms["J(1,0)"], pj) and torch.allclose(arms["J(0,1)"], delta - pj)
    assert torch.allclose(arms["J(2,0)"], 2 * pj) and torch.allclose(arms["J(0,2)"], 2 * (delta - pj))
    # the random corners: the random part of the J++ part's share in its place
    assert torch.allclose(arms["R(1,0)"], rj) and torch.allclose(arms["R(2,0)"], 2 * rj)
    assert torch.allclose(arms["R(0,1)"], delta - rj) and torch.allclose(arms["R(0,2)"], 2 * (delta - rj))
    # amendment 2, as written: 2 (Δ - P_J Δ - U U^T Δ), and the twin with the random part of U's share
    assert torch.allclose(arms["J(0,2)-U"], 2 * (delta - pj - up))
    assert torch.allclose(arms["J(0,2)-RU"], 2 * (delta - pj - ru))
    assert torch.allclose(arms["J100(2,0)"], 2 * p100) and torch.allclose(arms["R100(0,2)"], 2 * (delta - r100))
    assert list(G.arm_deltas(delta, pj, rj, up, ru)) == G.arm_names(False)


def test_parts_are_x0s_and_the_shares_match():
    g = torch.Generator().manual_seed(1)
    n = 6
    jdic = torch.nn.functional.normalize(torch.randn(120, D, generator=g), dim=-1)
    delta = torch.randn(n, D, generator=g)
    basis = SP.random_basis(D, torch.Generator().manual_seed(X.SUBSPACE_SEED + L))
    u = _orth(D, 4, 2)
    pj, rj = G.lens_parts(jdic, delta, 25, basis)
    assert torch.allclose(pj, X.fit(jdic, delta, 25, "signed"))  # X0's J++ part
    assert torch.allclose(rj, SP.random_subspace_part(delta, G.share(pj, delta), basis))  # X0's random part
    up, ru = G.pointer_parts(delta, u, basis)
    assert torch.allclose(up, delta @ u @ u.T, atol=1e-5)
    one = ((delta @ basis) ** 2).max(dim=-1).values / delta.norm(dim=-1) ** 2  # matched to within one direction
    assert ((G.share(rj, delta) - G.share(pj, delta)).abs() <= one + 1e-6).all()
    assert ((G.share(ru, delta) - G.share(up, delta)).abs() <= one + 1e-6).all()
    recs = G.norm_records(delta, pj, rj, up, ru, u)
    assert len(recs) == n and set(recs[0]) == {"norm_delta", "share_J", "share_J_rand", "share_U", "share_U_rand",
                                               "share_U_in_J"}  # fmt: skip
    # the written no-U arm and "U removed from the rest" differ by exactly 2 U U^T P_J Δ (recorded as share_U_in_J)
    arms = G.arm_deltas(delta, pj, rj, up, ru)
    rest_without_u = 2 * (delta - pj - (delta - pj) @ u @ u.T)
    gap = rest_without_u - arms[G.NOU]
    assert torch.allclose(gap, 2 * (pj @ u @ u.T), atol=1e-5)
    for i in range(n):
        assert recs[i]["share_U_in_J"] == pytest.approx(
            float(G.share((pj @ u @ u.T)[i : i + 1], delta[i : i + 1])), abs=1e-5
        )


# ---- end to end on a fake model ------------------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model (after tests/test_x47_zero.py): each block mixes the running
    mean of the positions so far into every position; an edit acts on a block's output, as Model's hooks do."""

    def __init__(self, n_layers: int = L + 4, vocab: int = 128):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, D, generator=g), torch.randn(vocab, D, generator=g)
        self.n_layers, self.device = n_layers, torch.device("cpu")
        self.tokenizer = SimpleNamespace(name="fake")
        self.calls: list[tuple[list[int], list[dict]]] = []

    def forward(self, ids: list[int], edits: dict):
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
        self.calls.append((rows[0].tolist(), edits))
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [f" t{int(lg.argmax())}" for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return torch.arange(100)


class FakeLens:
    source_layers = tuple(range(L + 4))

    def __init__(self, model=None, name="jpp"):
        assert name == "jpp"

    def vectors(self, layer, ids):
        v = torch.randn(len(ids), D, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def _item(i: int) -> dict:
    """A locker-first item as select_items writes it: both readers' prompts agree through the bridge word (position
    4) and the token after it; S changes only the bridge word here."""
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    rd = {"id": f"PP-{i}", "question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
          "ids": {"org": [*org, 7], "alt": [*alt, 7]}, "tok_A": 5, "tok_b": 3}  # fmt: skip
    rc = {**rd, "id": f"PM-{i}", "question": "How many legs?", "ids": {"org": [*org, 8, 9], "alt": [*alt, 8, 9]}}
    return {"scene": f"P2-{i:04d}", "entity": f"e{i % 4}", "cf_bridge": "bee", "domain": "animals", "pos": 4,
            "group": G.GROUP, "space": [11], "readers": {LK: rd, RC: rc}, "stored": {"whole": {LK: 1, RC: 0}}}  # fmt: skip


@pytest.fixture
def fake_items():
    model = FakeModel()
    items = [_item(i) for i in range(12)]
    u = _orth(D, 4, 3)
    rows, norms, losses, greedy = G.run_items(model, FakeLens(), items, L, torch.arange(10), u, wide=True)
    return SimpleNamespace(model=model, items=items, u=u, rows=rows, norms=norms, losses=losses, greedy=greedy)


def test_run_items_reads_every_arm_on_o(fake_items):
    f = fake_items
    names = G.arm_names(True)
    assert {(r["scene"], r["reader"], r["arm"]) for r in f.rows} == {
        (c["scene"], w, a) for c in f.items for w in X.READERS for a in names
    }
    assert len(f.rows) == len(f.items) * 2 * len(names) and len(f.losses) == len(f.items) * len(names)
    assert len(f.greedy) == X.K_EXAMPLES * 2 * len(names) and len(f.norms) == len(f.items)
    assert all(r["switched"] == int(r["top"] == 3) for r in f.rows)
    # the first read: the lookup's O prompt with the digit's space token appended, every arm in one batch, at L
    prompt, edits = f.model.calls[0]
    it = f.items[0]
    assert prompt == it["readers"][LK]["ids"]["org"] + it["space"] and len(edits) == len(names)
    assert all(list(e) == [L] and e[L].positions == [it["pos"]] for e in edits)


def test_the_arms_add_the_change_split_by_gain(fake_items):
    f = fake_items
    it, names = f.items[0], G.arm_names(True)
    ids = it["readers"][LK]["ids"]
    h = {v: f.model.run(torch.tensor([ids[v]]), record=(L,))[1][L][it["pos"]] for v in ("org", "alt")}
    delta = h["alt"] - h["org"]
    edits = dict(zip(names, f.model.calls[0][1], strict=True))
    assert torch.allclose(edits["J(1,1)"][L].delta[0], delta, atol=1e-5)  # X0's whole arm
    assert not edits["J(0,0)"][L].delta.any()
    jdic = FakeLens().vectors(L, torch.arange(100))
    pj = X.fit(jdic, delta[None], 25, "signed")[0]
    assert torch.allclose(edits["J(2,0.5)"][L].delta[0], 2 * pj + 0.5 * (delta - pj), atol=1e-4)
    up = delta @ f.u @ f.u.T
    assert torch.allclose(edits["J(0,2)-U"][L].delta[0], 2 * (delta - pj - up.float()), atol=1e-4)
    # under the whole change O's bridge state at L is S's
    st = f.model.run(torch.tensor([ids["org"]]), edits=edits["J(1,1)"], record=(L,))[1][L][it["pos"]]
    assert torch.allclose(st, h["alt"], atol=1e-4)
    # J(0,0) reads exactly as O unedited
    lg0 = f.model.forward(ids["org"] + it["space"], {})[0]
    r0 = next(r for r in f.rows if r["scene"] == it["scene"] and r["reader"] == LK and r["arm"] == "J(0,0)")
    assert r0["top"] == int(lg0.argmax())


def test_the_loss_is_os_own_next_token_at_the_bridge_word(fake_items):
    f = fake_items
    it, names = f.items[1], G.arm_names(True)
    ids = it["readers"][LK]["ids"]["org"]
    prompt, edits = next(c for c in f.model.calls if c[0] == ids[: it["pos"] + 1])
    assert len(edits) == len(names)
    mine = {r["arm"]: r for r in f.losses if r["scene"] == it["scene"]}
    for a, e in zip(names, edits, strict=True):
        lg = f.model.forward(prompt, e)[0]
        want = -torch.log_softmax(lg, -1)[ids[it["pos"] + 1]]
        assert mine[a]["loss"] == pytest.approx(float(want), abs=1e-4) and mine[a]["next"] == ids[it["pos"] + 1]


def _stage(monkeypatch, tmp_path, items, gate_pass=True):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins

    fake = FakeModel()
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(LN, "JLens", FakeLens)
    monkeypatch.setattr(G, "RESULTS", tmp_path / "x49_gain")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(G, "SPEC", tmp_path / "batch49.yaml")
    G.SPEC.write_text("")
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(
        G, "pointer_basis", lambda t: (_orth(D, 4, 3).double().numpy(), {"states_run": "fake", "rank": 4})
    )
    monkeypatch.setattr(G, "select_items", lambda tok, t: (items, {"items_in_group": len(items)}))
    src = X.RESULTS / G.SOURCES[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    (src / "gate.json").write_text(json.dumps({"gate": {"chat": {"pass": gate_pass, "enough": True}}}))
    return fake


def test_stage_run_end_to_end_sealed(tmp_path, monkeypatch):
    from bridge_jspace import pins

    items = [_item(i) for i in range(12)]
    _stage(monkeypatch, tmp_path, items)
    out = G.stage_run(f"{pins.RUN_PREFIX}x49_test", "test")
    m = json.loads((out / "manifest.json").read_text())
    assert m["layer"] == L and m["k"] == 25 and m["wide"] is False and "sealed" in m and m["test"] == "49.1"
    assert m["arms"] == G.arm_names(False) and "switches" in m and m["pointer"]["rank"] == 4
    assert sorted(p.name for p in out.iterdir()) == ["cases.jsonl", "examples_greedy.jsonl", "gate.json", "losses.jsonl",
                                                     "manifest.json", "norms.jsonl", "outcomes.jsonl", "plan.json"]  # fmt: skip
    assert len(X.read_jsonl(out / "outcomes.jsonl")) == 12 * 2 * len(G.arm_names(False))
    assert json.loads((out / "gate.json").read_text())["tested"] is True


def test_stage_run_without_the_gate_writes_no_outcomes(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, [_item(0)], gate_pass=False)
    out = G.stage_run(f"{pins.RUN_PREFIX}x49_test_gate", "test")
    assert not (out / "outcomes.jsonl").exists() and json.loads((out / "gate.json").read_text())["tested"] is False


# ---- the rules -----------------------------------------------------------------------------------------------------


def rates(kind: str) -> tuple[dict[str, float], dict[str, float]]:
    """Planted point estimates for each outcome: (recall, lookup) per arm."""
    names = G.arm_names(True)
    rc = {a: 0.3 for a in names}
    lk = {a: 0.3 for a in names}
    if kind in ("a", "a_prime", "a_noisy_rand"):
        for a in G.GAINS:
            for b in G.GAINS:
                rc[G.gname("J", a, b)] = min(1.0, 0.4 * a + 0.3 * b)
                lk[G.gname("J", a, b)] = min(1.0, 0.7 * b)
        rc |= {"R(1,0)": 0.05, "R(2,0)": 0.05, "R(0,1)": 0.3, "R(0,2)": 0.6}
        rc[G.NOU] = 0.6 if kind != "a_prime" else 0.1
        if kind == "a_noisy_rand":
            rc["R(2,0)"] = 0.2
    elif kind == "b":
        for a in G.GAINS:
            for b in G.GAINS:
                rc[G.gname("J", a, b)] = min(1.0, 0.4 * a)
        rc[G.NOU] = 0.0
    return rc, lk


@pytest.mark.parametrize(("kind", "holds", "literal"), [("a", ["a"], False), ("b", ["b"], False),
                                                         ("a_prime", ["a_prime"], False), ("c", [], False),
                                                         ("a_noisy_rand", [], False)])  # fmt: skip
def test_rule_on_planted_numbers(kind, holds, literal):
    r = G.rule(*rates(kind))
    assert r["holds"] == holds and r["a_literal_all_four_corners"] is literal
    assert r["label"] == (" and ".join(G.LABELS[k] for k in holds) or G.LABELS["c"])


def test_rule_bars_are_inclusive_and_the_literal_reading_is_beside():
    rc, lk = rates("a")
    rc |= {"J(2,0)": 0.5, "J(0,2)-U": 0.5, "R(1,0)": 0.15, "R(2,0)": 0.15, "R(0,1)": 0.15, "R(0,2)": 0.15}
    lk |= {"J(2,0)": 0.10, "J(0,1)": 0.6}
    r = G.rule(rc, lk)
    assert r["clauses"]["a"] and r["a_literal_all_four_corners"]
    assert G.rule(rc | {"J(2,0)": 0.5 - 1e-6}, lk)["holds"] == []
    assert not G.rule(rc, lk | {"J(2,0)": 0.11})["clauses"]["a"]
    # (b) and (a') at their bars
    assert G.rule(rc | {"J(0,2)": 0.2, "J(0,2)-U": 0.0}, lk)["clauses"]["b"]
    assert G.rule(rc | {"J(0,2)": 0.5, "J(0,2)-U": 0.2}, lk)["clauses"]["a_prime"]


# ---- planted runs: the verdict, the loss flag, the seal ------------------------------------------------------------


def write_planted(root, run: str, target: str, kind: str, n: int = 60, loss_20: float = 3.0, tested: bool = True):
    """A planted 49.1 run: n items over 10 bridge items, each arm's switch rate from rates(kind) (the first
    round(rate * n) items switch), the loss 1.0 everywhere but J(2,0) (loss_20)."""
    src = root / run
    src.mkdir(parents=True)
    wide = target in G.WIDE_TARGETS
    names = G.arm_names(wide)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": X.PREDICTED[target], "wide": wide,
                                                   "pointer": {"rank": 4, "states_run": "fake"}}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"tested": tested, "gate": {"pass": tested}}))
    if not tested:
        return
    rc, lk = rates(kind)
    rows, losses, cases, norms = [], [], [], []
    for i in range(n):
        it = _item(i)
        scene, ent = it["scene"], f"e{i % 10}"
        cases.append({**it, "entity": ent})
        norms.append({"scene": scene, "entity": ent, "norm_delta": 1.0, "share_J": 0.1, "share_U": 0.02})
        for w, pts in ((RC, rc), (LK, lk)):
            for a in names:
                s = int(i < round(pts[a] * n)) if a != G.NONE else 0
                rows.append({"scene": scene, "entity": ent, "domain": "animals", "reader": w, "arm": a, "switched": s,
                             "top": 3 if s else 5, "role": "b" if s else "A"})  # fmt: skip
        losses += [{"scene": scene, "entity": ent, "arm": a, "next": 6, "loss": loss_20 if a == "J(2,0)" else 1.0,
                    "top_is_next": 1} for a in names]  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "losses.jsonl", losses)
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "norms.jsonl", norms)
    X.write_jsonl(src / "examples_greedy.jsonl", [])


def planted_verdict(root, mp, kinds: dict[str, str | None], n_boot: int = 200):
    """The verdict folder over planted runs (kind None: not tested; a model missing from kinds: pending)."""
    mp.setattr(G, "RESULTS", root)
    mp.setattr(G, "dan_answer", lambda rev="HEAD": "planted")
    for target, kind in kinds.items():
        write_planted(root, G.RUNS[target], target, kind or "c", tested=kind is not None)
    return G.stage_verdict(n_boot=n_boot, decode_for=lambda t: lambda ids: "".join(f"<{int(i)}>" for i in ids))


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    out = planted_verdict(
        tmp_path, monkeypatch, {"qwen3.5-9b": "a", "qwen3.6-27b": "a_prime", "muse-glimmer-30b": None}
    )
    blob = json.loads((out / "x49_1.json").read_text())
    m = {x["target"]: x for x in blob["models"]}
    assert m["qwen3.5-9b"]["holds"] == ["a"] and m["qwen3.6-27b"]["holds"] == ["a_prime"]
    assert m["muse-glimmer-30b"]["status"] == "not tested" and blob["dan"] == "planted"
    nine = m["qwen3.5-9b"]
    assert nine["wide"] and "J100(2,0)" in nine["readers"]["recall"]["rate"] and nine["n"] == 60
    rc = nine["readers"]["recall"]["rate"]
    assert rc["J(2,0)"][0] == pytest.approx(0.8) and rc["J(2,0)"][1] <= 0.8 <= rc["J(2,0)"][2]
    assert nine["loss"]["flag"] == {"J(2,0)": True, "J(0,2)": False, "J(2,2)": False, G.NOU: False}
    assert nine["loss"]["ratio_to_whole"]["J(2,0)"][0] == pytest.approx(3.0)
    assert nine["checks"]["recall"]["none_reads_O"] == 60
    md = (out / "x49_1.md").read_text()
    assert "(a) weights, not routes" in md and "Dan: planted" in md and "| β \\ α |" in md
    assert (out / "examples.md").read_text().count("```") == 2 * 2 * X.K_EXAMPLES * 2  # two tested runs


def test_pending_model(tmp_path, monkeypatch):
    out = planted_verdict(tmp_path, monkeypatch, {"qwen3.6-27b": "b"})
    blob = json.loads((out / "x49_1.json").read_text())
    assert blob["per_model"] == {"qwen3.5-9b": "pending", "qwen3.6-27b": "(b) routes", "muse-glimmer-30b": "pending"}


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(G, "RESULTS", tmp_path)
    monkeypatch.setattr(G, "dan_answer", lambda rev="HEAD": "")
    write_planted(tmp_path, G.RUNS["qwen3.5-9b"], "qwen3.5-9b", "a")
    with pytest.raises(AssertionError, match="sealed"):
        G.stage_verdict(n_boot=10)
    assert sorted(p.name for p in tmp_path.iterdir()) == [G.RUNS["qwen3.5-9b"]]


def test_dan_answer_reads_only_the_q49_1_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q48.6** x\n\nDan: (a) 60%\n\n**Q49.1** The gain map ...\n- (a) Weights\n- (c) Neither.\n\nDan:{}\n\n"
              "**Q49.2** The removal ladder\n\nDan: yes\n")  # fmt: skip
    monkeypatch.setattr(G.subprocess, "run", fake_git(blocks.format("")))
    assert G.dan_answer() == ""
    monkeypatch.setattr(G.subprocess, "run", fake_git(blocks.format(" 9B (a) 60%; 27B (c)")))
    assert G.dan_answer() == "9B (a) 60%; 27B (c)"


def test_the_committed_predictions_file_has_the_q49_1_block():
    text = G.subprocess.run(["git", "show", f"HEAD:{G.PREDICTIONS}"], cwd=G.pins.REPO_ROOT, capture_output=True,
                            text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{G.QUESTION}**" in text and isinstance(G.dan_answer(), str)


def test_matched_share_controls_are_read_within_a_tenth_of_their_cells():
    # Dan (batch 49 amendment 3): R(0,1), R(0,2) are matched-share controls, within 0.10 of J(0,1), J(0,2)
    grid = {G.gname("J", a, b): 0.5 for a in G.GAINS for b in G.GAINS}
    grid.update({G.gname("R", a, b): 0.0 for a, b in G.CORNERS})
    grid[G.NOU] = 0.5
    rc, lk = dict(grid), dict(grid)
    rc[G.gname("R", 0, 1)], rc[G.gname("R", 0, 2)] = 0.55, 0.30
    m = G.rule(rc, lk)["matched_share_controls"]
    assert m["recall R(0,1) within 0.1 of J"] and not m["recall R(0,2) within 0.1 of J"]
