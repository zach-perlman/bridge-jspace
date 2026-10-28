"""Batch 49, test 49.2 (scripts/x49_ladder.py) and its figure (scripts/story_b49b.py): the rungs' token sets, the
per-token projection onto the same 25 atoms at L..L+3, the random subspace per token, rung 6 as Zach's code path, the
arms end to end on a tiny fake causal model (CPU), the rules at their bars on planted numbers, the seal, the verdict
and the figure on planted runs. No real model."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch
from test_readme_phase2_figures import check, saved  # noqa: F401 (saved: a fixture)
from test_x47_zero import FakeLens, FakeModel, _proj

from bridge_jspace.ablate import MatrixDictionary, RowSettings, removal_edit, top_span_removal
from scripts import statement_positions as SP
from scripts import story_b49b as FIG
from scripts import story_style as S
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x47_zero as Z
from scripts import x49_ladder as LD

LK, RC = X.LOOKUP, X.RECALL
L = X.PREDICTED["qwen3.6-27b"]  # the default target's layer (32): the fake model has blocks past L + 4
LAYERS = tuple(range(L, L + LD.SPAN))
BAND = tuple(range(L - 1, L + 4))  # a five-layer band starting below L, as the 9B's L12-16 does not
D = 48


# ---- the rungs' token sets -----------------------------------------------------------------------------------------


def test_rung_positions_are_nested():
    ps = LD.rung_positions(12, 5, [1, 2], [8, 9, 10, 11])
    assert ps[1] == ps[2] == [5]
    assert ps[3] == [1, 2, 5] and ps[4] == [1, 2, 5, 8, 9, 10, 11]
    assert ps[5] == ps[6] == list(range(12))
    for r in (1, 2, 3, 4):
        assert set(ps[r]) <= set(ps[r + 1])
    with pytest.raises(AssertionError, match="outside the prompt"):
        LD.rung_positions(10, 5, [1], [12])


class CharTok:
    """One token per character (id = its code point), with character offsets: enough for the position code."""

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        return SimpleNamespace(
            input_ids=[ord(ch) for ch in text], offset_mapping=[(i, i + 1) for i in range(len(text))]
        )

    def decode(self, ids):
        return "".join(chr(int(i)) for i in ids)


CTX = "The locker of the dog is 6. The locker of the fly is 2. Ruby picked the dog. The locker of the sheep is 3."


@pytest.mark.parametrize("first", [True, False])
def test_reader_record_marks_each_rungs_tokens(monkeypatch, first):
    tok = CharTok()
    # locker after the pick: the dog's locker sentence after Ruby's pick
    ctx = CTX if first else "Ruby picked the dog. The locker of the fly is 2. The locker of the dog is 6."
    question = "\nWhich locker belongs to Ruby's pick? Answer with a digit.<|im_end|>\nAnswer:"
    monkeypatch.setattr(X, "render", lambda tok, item, rendering, context: context + question)
    text = ctx + question
    pick = ctx.index("Ruby picked the dog") + len("Ruby picked the ")
    space = [ord(" ")]
    c = {"pos": pick, "cf_context": ctx, "cf_bridge": "dog", "space": space,
         "readers": {LK: {"id": "PP-1", "question": "q", "answer": "2", "cf_answer": "6", "tok_A": 50, "tok_b": 54,
                          "ids": {"org": [], "alt": [ord(ch) for ch in text]}}}}  # fmt: skip
    rd = LD.reader_record(tok, c, {}, LK)
    mention = ctx.index("of the dog") + len("of the ")
    assert rd["mention"] == [mention, mention + 1, mention + 2]  # the name's characters in its locker sentence
    assert (max(rd["mention"]) < pick) == first
    q0 = len(ctx) + 1  # the question sentence starts after the line break
    assert rd["question_pos"] == list(range(q0, len(text) + 1))  # through the read's appended token
    assert rd["n_read"] == len(text) + 1
    assert "⟦mention:dog⟧" in rd["marked"] and "⟦bridge:d⟧" in rd["marked"]
    assert rd["marked"].count("⟦question:Which locker belongs") == 1 and rd["marked"].endswith("Answer: ⟧")
    c["readers"][LK]["ids"]["alt"] = c["readers"][LK]["ids"]["alt"][:-1]
    with pytest.raises(LD.Dropped, match="ids differ"):
        LD.reader_record(tok, c, {}, LK)


# ---- the edits -----------------------------------------------------------------------------------------------------


def test_random_out_takes_the_first_k_columns_per_token():
    g = torch.Generator().manual_seed(3)
    h = torch.randn(6, 16, generator=g)
    basis = SP.random_basis(16, torch.Generator().manual_seed(5))
    e = LD.RandomOut(basis, [1, 4, 5], [2, 0, 7])
    out = e(h)
    assert torch.allclose(out[[0, 2, 3]], h[[0, 2, 3]])
    for p, k in ((1, 2), (4, 0), (5, 7)):
        assert torch.allclose(out[p], h[p] - _proj(basis[:, :k]).float() @ h[p], atol=1e-5)
    assert torch.allclose(e(h[:5])[4], h[4]) and e(h[:1]).shape == (1, 16)  # a shorter (greedy) prompt: clipped
    assert torch.allclose(LD.AtomsOut(basis[:, :3], [2, 9])(h)[2], h[2] - _proj(basis[:, :3]).float() @ h[2], atol=1e-5)


def _dic(la: int, n: int = 100, d: int = D) -> MatrixDictionary:
    v = torch.randn(n, d, generator=torch.Generator().manual_seed(1000 + la))
    return MatrixDictionary(v / v.norm(dim=1, keepdim=True))


def test_band_dictionaries_are_ablate_v2s_with_one_shared_wg():
    w = torch.randn(128, D, generator=torch.Generator().manual_seed(4))
    model = SimpleNamespace(
        hf=SimpleNamespace(lm_head=SimpleNamespace(weight=w)), norm_gain=lambda: torch.full((D,), 2.0)
    )
    lens = SimpleNamespace(J=lambda la: torch.eye(D) * (la + 1))
    dic = LD.band_dictionaries(model, lens, (3, 4), torch.arange(100))
    assert dic[3].wg is dic[4].wg and torch.allclose(dic[3].wg, 2 * w[:100])
    assert torch.allclose(dic[4].J, 5 * torch.eye(D))
    assert LD.band_dictionaries(model, lens, (), torch.arange(100)) == {}


def test_rung_6_is_zachs_top10_by_his_code_path():
    g = torch.Generator().manual_seed(9)
    h = torch.randn(7, D, generator=g)
    dic, prot = _dic(0), torch.tensor([3, 17])
    top = LD.ZachTop(dic, prot)
    want = removal_edit("top", dic, [RowSettings(protected=prot)], k=10)(h[None])[0]
    assert torch.allclose(top(h), want, atol=1e-5)
    r, chosen = top_span_removal(dic, h, 10, protected=[(torch.arange(7), prot)], return_chosen=True)
    assert torch.allclose(top(h), h - r, atol=1e-5)
    assert not set(chosen.flatten().tolist()) & {3, 17}  # never a protected atom
    share = float((r.norm(dim=-1) ** 2 / h.norm(dim=-1) ** 2).mean())
    assert top.log[-1] == pytest.approx(share, abs=1e-5)
    basis = SP.random_basis(D, torch.Generator().manual_seed(2))
    rnd = LD.ZachRandom(dic, prot, basis)
    out = rnd(h)
    per = r.norm(dim=-1) ** 2 / h.norm(dim=-1) ** 2
    assert torch.allclose(out, h - SP.random_subspace_part(h, per, basis), atol=1e-5)
    one = float(((h @ basis) ** 2 / (h.norm(dim=-1, keepdim=True) ** 2)).max())
    assert abs(rnd.log[-1] - share) <= one + 1e-6  # the same share, to within one random direction


# ---- the arms end to end on a fake model ---------------------------------------------------------------------------


def _item(i: int) -> dict:
    """A clean-design-like item: S changes only the bridge word (position 4); the mention at position 1; the readers
    share the context and differ in the question (positions 6 on)."""
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    base = {"answer": "5", "cf_answer": "3", "tok_A": 5, "tok_b": 3}
    rd = {**base, "id": f"PP-{i}", "question": "q", "ids": {"org": [*org, 7, 9], "alt": [*alt, 7, 9]},
          "question_pos": [6, 7, 8], "n_read": 9, "marked": "<lookup prompt>"}  # fmt: skip
    rc = {**base, "id": f"PM-{i}", "question": "q", "ids": {"org": [*org, 8, 9, 10], "alt": [*alt, 8, 9, 10]},
          "question_pos": [6, 7, 8, 9], "n_read": 10, "marked": "<recall prompt>"}  # fmt: skip
    return {"scene": f"P2-{i:04d}", "entity": f"e{i % 4}", "cf_bridge": "bee", "domain": "animals",
            "order": LD.ORDERS[i % 2], "group45m": "x", "pos": 4, "mention": [1], "space": [11],
            "readers": {LK: rd, RC: rc}}  # fmt: skip


def _zach(model, lens, band, letters):
    return {la: _dic(la) for la in band}


@pytest.fixture
def fake():
    model = FakeModel(n_layers=L + 8)
    items = [_item(i) for i in range(12)]
    ws = X.whitespace_mask(model)
    rows, norms, greedy = LD.run_items(model, FakeLens(), items, LAYERS, BAND, ws, torch.arange(10), _zach)
    return SimpleNamespace(model=model, items=items, rows=rows, norms=norms, greedy=greedy)


def test_run_items_reads_every_rung_on_s(fake):
    arms = LD.arms_of(LD.RUNGS)
    assert len(arms) == 13
    assert {(r["scene"], r["reader"], r["arm"]) for r in fake.rows} == {
        (c["scene"], w, a) for c in fake.items for w in X.READERS for a in arms
    }
    assert all(r["kept"] == int(r["top"] == 3) for r in fake.rows)
    assert len(fake.greedy) == X.K_EXAMPLES * 2 * len(arms)
    seq, edits = fake.model.calls[0]  # the first read: the lookup's S prompt with the space token, 13 arms
    assert seq == len(fake.items[0]["readers"][LK]["ids"]["alt"]) + 1 and len(edits) == 13 and edits[0] == {}
    n = fake.norms[0]
    assert set(n["atoms_share"]) == {str(la) for la in LAYERS} and set(n["zach_share"]["zero6"]) == {
        str(la) for la in BAND
    }
    assert all(0 < v < 1 for kd in ("zero6", "rand6") for v in n["zach_share"][kd].values())


def _arms(fake, call: int = 0) -> dict:
    return dict(zip(LD.arms_of(LD.RUNGS), fake.model.calls[call][1], strict=True))


def test_rungs_take_the_same_atoms_out_at_every_rung_token(fake):
    c = fake.items[0]
    s_ids = c["readers"][LK]["ids"]["alt"] + c["space"]
    edits = _arms(fake)
    clean = fake.model.run(torch.tensor([s_ids]), record=LAYERS)[1]
    o = fake.model.run(torch.tensor([c["readers"][LK]["ids"]["org"]]), record=LAYERS)[1]
    lens = FakeLens()
    for la in LAYERS:  # the same basis at every token: the bridge's Δ_l's 25 OMP atoms over that layer's lens
        q, _ = Z.atom_bases(lens.vectors(la, torch.arange(100)), (clean[la][4] - o[la][4])[None])
        for r in (2, 3, 4, 5):
            assert torch.allclose(_proj(edits[f"zero{r}"][la].basis), _proj(q[0]), atol=1e-5)
    assert set(edits["zero1"]) == {L} and all(set(edits[f"zero{r}"]) == set(LAYERS) for r in (2, 3, 4, 5))
    assert set(edits["zero6"]) == set(edits["rand6"]) == set(BAND)
    want = {1: [4], 2: [4], 3: [1, 4], 4: [1, 4, 6, 7, 8], 5: list(range(len(s_ids)))}
    for r, ps in want.items():
        assert edits[f"zero{r}"][L].positions == ps and edits[f"rand{r}"][L].positions == ps
        st = fake.model.run(torch.tensor([s_ids]), edits=edits[f"zero{r}"], record=LAYERS)[1]
        q_l = edits[f"zero{r}"][L].basis
        assert torch.allclose(st[L][ps], clean[L][ps] - (clean[L][ps] @ q_l) @ q_l.T, atol=1e-5)
        rest = [p for p in range(len(s_ids)) if p not in ps]
        assert torch.allclose(st[L][rest], clean[L][rest])  # untouched at L outside the rung
        for la in edits[f"zero{r}"]:  # nothing left in that layer's span at the rung's tokens, as it arrives
            assert float((st[la][ps] @ edits[f"zero{r}"][la].basis).norm()) < 1e-4


def test_the_random_beside_each_rung_is_per_token(fake):
    c = fake.items[0]
    s_ids = c["readers"][RC]["ids"]["alt"] + c["space"]  # the recall's own prompt: its own clean states
    call = next(e for n, e in fake.model.calls if n == len(s_ids))  # the recall's read (its greedy is one shorter)
    edits = dict(zip(LD.arms_of(LD.RUNGS), call, strict=True))
    clean = fake.model.run(torch.tensor([s_ids]), record=LAYERS)[1]
    for la in LAYERS:
        basis = SP.random_basis(D, torch.Generator().manual_seed(X.SUBSPACE_SEED + la))
        q = edits["zero5"][la].basis
        share = LD.token_shares(clean[la], q)
        ks = R.random_k(clean[la], share, basis).tolist()
        for r in (2, 3, 4, 5):
            e = edits[f"rand{r}"][la]
            assert e.ks == [ks[p] for p in e.positions]
            assert torch.allclose(e.basis, basis.to(e.basis.dtype), atol=1e-6)
        e5 = edits["rand5"][la]
        assert len(set(e5.ks)) > 1  # k differs between tokens
        one = ((clean[la].double() @ basis.double()) ** 2).max(dim=1).values / clean[la].double().norm(dim=1) ** 2
        got = torch.stack(
            [LD.token_shares(clean[la][p : p + 1], basis[:, :k])[0] for p, k in zip(e5.positions, e5.ks, strict=True)]
        )
        assert bool(((got - share).abs() <= one.float() + 1e-5).all())  # the atoms' share per token, to one direction


def test_the_27b_runs_the_bridge_word_rungs_only():
    model = FakeModel(n_layers=L + 8)
    items = [_item(i) for i in range(3)]
    rows, norms, _ = LD.run_items(
        model, FakeLens(), items, LAYERS, (), X.whitespace_mask(model), torch.arange(10), _zach
    )
    assert {r["arm"] for r in rows} == set(LD.arms_of(LD.BRIDGE_RUNGS)) == {"none", "zero1", "rand1", "zero2", "rand2"}
    assert norms[0]["zach_share"] == {}


# ---- the rules on planted numbers ----------------------------------------------------------------------------------

N = 100  # items per order group


def planted_rows(kept: dict, rungs=LD.RUNGS, n: int = N) -> list[dict]:
    """Per order group n items (entities e0-e19); under each arm the reader keeps S's answer on the first
    kept[(order, reader, arm)] items of the group (default: all)."""
    rows = []
    for g, order in enumerate(LD.ORDERS):
        for i in range(n):
            for w in X.READERS:
                for a in LD.arms_of(rungs):
                    k = kept.get((order, LD.READER_NAME[w], a), n)
                    kind, rung = LD.rung_of(a)
                    rows.append({"scene": f"{order}-{i:04d}", "entity": f"e{(i + g * 7) % 20}", "order": order,
                                 "reader": w, "arm": a, "rung": rung, "kind": kind, "kept": int(i < k),
                                 "top": 3 if i < k else 5, "role": "b" if i < k else "A"})  # fmt: skip
    return rows


def ladder(recall: dict[int, int] | None = None, lookup: dict[int, int] | None = None, first2=None, first3=None,
           after2=None) -> dict:  # fmt: skip
    """Planted kept counts: the random arms keep all; zero r keeps recall[r] (both orders) unless the locker-first
    rung 2/3 or locker-after rung 2 count is given."""
    kept = {}
    for order in LD.ORDERS:
        for r, k in (recall or {}).items():
            kept[(order, "recall", f"zero{r}")] = k
        for r, k in (lookup or {}).items():
            kept[(order, "lookup", f"zero{r}")] = k
    for (order, r), k in (((LD.ORDERS[0], 2), first2), ((LD.ORDERS[0], 3), first3), ((LD.ORDERS[1], 2), after2)):
        if k is not None:
            kept[(order, "recall", f"zero{r}")] = k
    return kept


def cells_of(rows, rungs=LD.RUNGS, n_boot: int = 300) -> dict:
    return {LD.READER_NAME[w]: {g: LD.numbers([r for r in rows if g == "all" or r["order"] == g], w, rungs, n_boot)
                                for g in LD.GROUPS} for w in X.READERS}  # fmt: skip


def rule(kept: dict) -> dict:
    return LD.rules(cells_of(planted_rows(kept)))


def test_numbers_read_kept_and_cost_beyond_random():
    kept = ladder({1: 95, 5: 40}, {6: 92})
    kept[(LD.ORDERS[0], "recall", "rand5")] = 90
    c = cells_of(planted_rows(kept))
    rc = c["recall"]
    assert rc["all"]["n"] == 2 * N and rc["locker-first"]["n"] == N and rc["all"]["entities"] == 20
    assert rc["all"]["cost"]["1"][0] == pytest.approx(0.05) and rc["all"]["raw_cost"]["1"][0] == pytest.approx(0.05)
    assert rc["locker-first"]["cost"]["5"][0] == pytest.approx(0.50) and rc["locker-first"]["raw_cost"]["5"][
        0
    ] == pytest.approx(0.60)
    assert rc["all"]["cost"]["5"][0] == pytest.approx(0.55)
    assert c["lookup"]["all"]["cost"]["6"][0] == pytest.approx(0.08)
    lo, hi = rc["all"]["cost"]["5"][1:]
    assert lo <= 0.55 <= hi
    with pytest.raises(AssertionError, match="reads missing"):
        LD.numbers([r for r in planted_rows({}) if r["arm"] != "rand4"], RC, LD.RUNGS, 10)


@pytest.mark.parametrize(
    ("first2", "first3", "after2", "want"),
    [(95, 65, 70, True),  # cost(3) - cost(2) = 0.30 exactly; locker-after rung 2 costs 0.30 exactly
     (95, 66, 70, False),  # 0.29 more
     (95, 65, 71, False),  # locker-after rung 2 costs 0.29
     (100, 20, 10, True)],
)  # fmt: skip
def test_second_copy_at_its_bars(first2, first3, after2, want):
    assert rule(ladder(first2=first2, first3=first3, after2=after2))["second_copy"] is want


@pytest.mark.parametrize(
    ("recall", "want"),
    [({1: 80, 2: 80, 3: 80, 4: 80, 5: 50}, True),  # rungs 1-4 cost 0.20 exactly, rung 5 0.50 exactly
     ({1: 80, 2: 80, 3: 80, 4: 80, 6: 50}, True),  # rung 6 alone reaches 0.50
     ({1: 80, 2: 80, 3: 80, 4: 79, 5: 10}, False),  # rung 4 costs 0.21
     ({1: 100, 5: 51, 6: 51}, False)],  # rungs 5 and 6 cost 0.49
)  # fmt: skip
def test_only_everything_at_its_bars(recall, want):
    assert rule(ladder(recall))["only_everything"] is want


@pytest.mark.parametrize(("lookup", "want"), [({}, True), ({r: 90 for r in LD.RUNGS}, True), ({6: 89}, False)])
def test_the_lookup_never_needs_it_at_its_bar(lookup, want):
    assert rule(ladder(lookup=lookup))["lookup"] is want


def test_the_lookup_rule_is_beyond_random():
    kept = ladder(lookup={5: 40})
    for order in LD.ORDERS:
        kept[(order, "lookup", "rand5")] = 45  # the random breaks it too: 0.05 beyond random
    assert rule(kept)["lookup"] is True


# ---- the seal ------------------------------------------------------------------------------------------------------


def _git_show(text: str):
    def run(cmd, **kw):
        assert cmd[:2] == ["git", "show"] and cmd[2].endswith(LD.PREDICTIONS)
        return SimpleNamespace(stdout=text)

    return run


BLOCK = "**Q49.1** x\n\nDan: 1\n\n**Q49.2** The removal ladder\n- a;\n- b.\n\nDan:{}\n\n**Q49.3** y\n\nDan: 3\n"


@pytest.mark.parametrize(("line", "want"), [("", ""), (" 9B: 60%; Muse 40%", "9B: 60%; Muse 40%")])
def test_dan_answer_reads_q49_2s_own_line(monkeypatch, line, want):
    monkeypatch.setattr(subprocess, "run", _git_show(BLOCK.format(line)))
    assert LD.dan_answer() == want


def test_the_predictions_file_holds_q49_2_and_its_dan_line():
    text = (Path(LD.pins.REPO_ROOT) / LD.PREDICTIONS).read_text()
    assert f"**{LD.QUESTION}**" in text and "Dan:" in text.split(f"**{LD.QUESTION}**", 1)[1].split("\n**Q", 1)[0]


def test_verdict_is_sealed(tmp_path, monkeypatch):
    planted_runs(tmp_path, monkeypatch)
    monkeypatch.setattr(LD, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        LD.stage_verdict(n_boot=50)
    assert sorted(p.name for p in LD.RESULTS.iterdir()) == sorted(LD.RUNS.values())


# ---- the verdict and the figure on planted runs ---------------------------------------------------------------------

PLANTED = {  # the 9B: needed only when everything goes; Muse: the second copy; the 27B: bridge-word rungs
    "qwen3.5-9b": ladder({1: 95, 2: 92, 3: 90, 4: 85, 5: 30, 6: 10}, {6: 85}),
    "muse-glimmer-30b": ladder({1: 98, 4: 50, 5: 30, 6: 20}, first2=95, first3=50, after2=60),
    "qwen3.6-27b": ladder({1: 97, 2: 90}),
}


def planted_runs(root: Path, mp, skip=()) -> None:
    mp.setattr(LD, "RESULTS", root / "x49_ladder")
    layers = {"qwen3.5-9b": 12, "qwen3.6-27b": 32, "muse-glimmer-30b": 26}
    for t in LD.MODELS:
        if t in skip:
            continue
        la, band = layers[t], LD.BAND.get(t, ())
        rungs = LD.RUNGS if band else LD.BRIDGE_RUNGS
        src = root / "x49_ladder" / LD.RUNS[t]
        src.mkdir(parents=True)
        rows = planted_rows(PLANTED[t], rungs)
        scenes = list(dict.fromkeys(r["scene"] for r in rows))
        cases = [{**_item(i), "scene": s, "order": s.split("-0")[0]} for i, s in enumerate(scenes)]
        norms = [{"scene": s, "reader": w, "bridge": None,
                  "atoms_share": {str(la + j): {k: 0.02 for k in ("bridge", "mention", "question", "every")} for j in range(4)},
                  "zach_share": {f"{kd}6": {str(b): 0.3 for b in band} for kd in LD.KINDS} if band else {}}
                 for s in scenes for w in X.READERS]  # fmt: skip
        greedy = [{"scene": scenes[0], "reader": RC, "arm": "zero1", "greedy": " 6 legs"}]
        man = {"model": {"target": t}, "layer": la, "layers": [la + j for j in range(4)], "band": list(band),
               "rungs": {str(r): LD.RUNG_TEXT[r] for r in rungs}, "arms": list(LD.arms_of(rungs))}  # fmt: skip
        (src / "manifest.json").write_text(json.dumps(man))
        for name, data in (("outcomes.jsonl", rows), ("cases.jsonl", cases), ("norms.jsonl", norms),
                           ("examples_greedy.jsonl", greedy)):  # fmt: skip
            X.write_jsonl(src / name, data)


def planted_verdict(root: Path, mp) -> Path:
    planted_runs(root, mp)
    mp.setattr(LD, "dan_answer", lambda rev="HEAD": "planted")
    return LD.stage_verdict(n_boot=200)


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    out = planted_verdict(tmp_path, monkeypatch)
    blob = json.loads((out / "x49_2.json").read_text())
    by = {m["target"]: m for m in blob["models"]}
    assert blob["dan"] == "planted" and out.parent == LD.RESULTS
    assert by["qwen3.5-9b"]["rules"] == {**by["qwen3.5-9b"]["rules"], "second_copy": False, "only_everything": True,
                                         "lookup": False}  # fmt: skip
    assert by["muse-glimmer-30b"]["rules"]["second_copy"] is True
    assert by["muse-glimmer-30b"]["rules"]["only_everything"] is False
    assert by["qwen3.6-27b"]["rules"] is None and by["qwen3.6-27b"]["rungs"] == [1, 2]
    assert by["qwen3.5-9b"]["shares_median"]["zach"]["zero6"]["12"] == 0.3
    md = (out / "x49_2.md").read_text()
    assert "bridge-word rungs only" in md and "two definitions, not one" in md
    ex = (out / "examples.md").read_text()
    assert ex.count("### ") == 3 * X.K_EXAMPLES and "<recall prompt>" in ex


def test_verdict_with_a_pending_model(tmp_path, monkeypatch):
    planted_runs(tmp_path, monkeypatch, skip=("muse-glimmer-30b",))
    monkeypatch.setattr(LD, "dan_answer", lambda rev="HEAD": "x")
    blob = json.loads((LD.stage_verdict(n_boot=50) / "x49_2.json").read_text())
    assert [m["status"] for m in blob["models"]] == ["tested", "tested", "pending"]


def test_the_figure_on_a_planted_verdict(tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = planted_verdict(tmp_path / "results", monkeypatch)
    name = "fig30_removal_ladder"
    assert FIG.build_ladder(verdict, name) == name
    assert (S.OUT / f"{name}.png").exists() and (S.OUT / f"{name}.svg").exists()
    check(saved[name])
    texts = " ".join(saved[name]["texts"])
    assert "Two definitions, not one" in texts and "rung 5" in texts and "rung 6" in texts
    rows = [r for r in S.ROWS if r["figure"] == "fig30"]
    assert rows and all(r["source"].endswith("x49_2.json") for r in rows)
    assert any(isinstance(r["value"], float) and r["lo"] is not None for r in rows)
    kept = [r for r in rows if r["model"] == "qwen3.5-9b" and r["quantity"] == "49.2: recall's answers kept, all"]
    assert not kept  # the figure draws the two orders; "all" stays in the verdict
    q = {(r["model"], r["quantity"]): r["value"] for r in rows}
    assert q[("qwen3.5-9b", "49.2: recall's answers kept, locker-first, rung 5 removed")] == pytest.approx(0.30)
    assert q[("qwen3.6-27b", "49.2: rule 'second_copy' holds")] == "n/a (bridge-word rungs only)"
    assert saved[name]["title"] == "The removal ladder: the recall needs the J++ part only at every token on 1 of 2"


def test_titles_read_the_rules():
    def v(*rules):
        return {"models": [{"status": "tested", "rules": {"second_copy": s, "only_everything": o, "lookup": k}}
                           for s, o, k in rules]}  # fmt: skip

    assert FIG.ladder_title({"models": [{"status": "pending"}]}).endswith("no model has run every rung yet")
    assert FIG.ladder_title(v((False, True, True), (False, True, True))) == (
        "The recall needs the J++ part only when every token loses it; the lookup never"
    )
    assert FIG.ladder_title(v((True, False, False), (True, True, False))).startswith("The recall's second copy")
    for t in (FIG.ladder_title(v((True, True, True), (False, False, True))),):
        assert len(t) <= 86
