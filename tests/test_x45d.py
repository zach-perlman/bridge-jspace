"""45d (batch 45, a pointer outside templates): the locker-swap pairs in prose / JSON / tables, the split by bridge item,
the held-out filter, the per-format basis, and the rule on planted (synthetic) outcomes. No model, no real results."""

import json
import math
import random
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import suite_v1 as S
from scripts import tasks_v2 as T
from scripts import x0_necessity as X
from scripts import x0b_generalize as B
from scripts import x7_pcf as P


def scene(fmt: str, level: int, domain: str = "animals", seed: int = 0) -> tuple[dict, dict]:
    rng = random.Random(seed)
    its = None
    while its is None:
        its = T.make_scene(rng, "P", ["PP", "PM"], domain, fmt, T.LEVELS[level], list(T.DOMAINS))
    pp, pm = its
    extra = {"scene": f"s{seed}", "level": level}
    return {**pp, "id": f"PP-{seed}", **extra}, {**pm, "id": f"PM-{seed}", **extra}


# ---- the pairs (no tokenizer) ---------------------------------------------------------------------------------------


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
@pytest.mark.parametrize("level", [0, 1, 2])
def test_swap_trades_the_two_locker_statements_and_keeps_their_numbers(fmt, level):
    for seed in range(6):  # both number styles turn up over the seeds
        pp, _ = scene(fmt, level, domain=("animals", "planets", "greek")[seed % 3], seed=seed)
        f = pp["facts"]
        x = f["x"]
        t = next(u for u in f["locker"] if u != x)
        sx, st = P.locker_statement(pp, x), P.locker_statement(pp, t)
        assert pp["context"].count(sx) == 1 and pp["context"].count(st) == 1
        swapped = P.swap_lockers(pp, x, t)
        # every other character stays; the two statements trade places, each with its own number
        assert sorted(swapped) == sorted(pp["context"]) and len(swapped) == len(pp["context"])
        assert swapped.count(sx) == 1 and swapped.count(st) == 1
        first = min(pp["context"].index(sx), pp["context"].index(st))
        assert swapped[first:].startswith(st if pp["context"].index(sx) == first else sx)
        assert swapped.replace(sx, "@X").replace(st, "@T") == pp["context"].replace(sx, "@T").replace(st, "@X")
        # the asked pick and the lookup's answer (the bridge's own locker number) are unchanged
        pick, _ = B.statements(pp, f["person"], x)
        assert swapped.count(pick) == 1 and str(f["locker"][x]) == pp["answer"]


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_before_pick_agrees_with_the_scene_order(fmt):
    seen = set()
    for seed in range(30):
        pp, _ = scene(fmt, 1, seed=seed)
        order = B.order_of(pp)
        seen.add(order)
        assert P.before_pick(pp, pp["facts"]["x"]) == (order == "before")
        if fmt != "prose":  # one block of locker rows: all on the same side of the picks
            assert len({P.before_pick(pp, t) for t in pp["facts"]["locker"]}) == 1
    assert seen == {"before", "after"}


def test_split_is_seeded_disjoint_and_covers_every_item():
    items = [f"e{i}" for i in range(31)] * 3
    a, b = P.split_items(items), P.split_items(list(reversed(items)))
    assert a == b  # the order of the cases does not matter, only the seed
    assert not set(a["fit"]) & set(a["test"]) and set(a["fit"]) | set(a["test"]) == set(items)
    assert len(a["fit"]) == 15 and len(a["test"]) == 16
    assert P.split_items(items, seed=1) != a


def test_held_out_keeps_the_test_half_of_each_format():
    split = {"formats": {"prose": {"fit": ["a"], "test": ["b"]}, "json": {"fit": ["b"], "test": ["a"]}}}
    cases = [{"scene": "1", "format": "prose", "bridge": "a"}, {"scene": "2", "format": "prose", "bridge": "b"},
             {"scene": "3", "format": "json", "bridge": "a"}, {"scene": "4", "format": "table", "bridge": "a"}]  # fmt: skip
    assert [c["scene"] for c in B.held_out(cases, split)] == ["2", "3"]
    with pytest.raises(AssertionError, match="not in the split"):
        B.held_out([{"scene": "5", "format": "prose", "bridge": "z"}], split)


def test_fit_basis_recovers_a_planted_subspace():
    rng = np.random.default_rng(0)
    q, _ = np.linalg.qr(rng.normal(size=(64, 4)))
    x = rng.normal(size=(300, 4)) * [5, 4, 3, 2] @ q.T + 0.05 * rng.normal(size=(300, 64)) + 3.0  # an offset too
    p, mean, var = P.fit_basis(x)
    assert p.shape == (64, 4) and np.allclose(p.T @ p, np.eye(4), atol=1e-8)
    assert min(P.principal_cos2(p, q)) > 0.99 and sum(var[:4]) > 0.99 and np.allclose(mean, x.mean(0))
    with pytest.raises(AssertionError):
        P.fit_basis(x[:4])


def test_the_pcf_dictionary_is_the_formats_basis(monkeypatch):
    torch = pytest.importorskip("torch")
    basis = torch.linalg.qr(torch.randn(16, 4))[0]
    monkeypatch.setattr(X, "PCF", basis)
    assert torch.equal(X.dictionary("pcf", 0, None, None, None), basis.T)
    monkeypatch.setattr(X, "PCF", None)
    with pytest.raises(AssertionError):
        X.dictionary("pcf", 0, None, None, None)


# ---- the pairs on the tokenizer ---------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def tok():
    from bridge_jspace.tokens import load_tokenizer

    try:
        return load_tokenizer()
    except Exception:
        try:
            from scripts import statement_positions as SP

            return SP.load_tokenizer()
        except Exception:
            pytest.skip("target tokenizer not cached")


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_pairs_change_only_tokens_before_the_bridge(tok, fmt):
    made = 0
    for seed in range(40):
        pp, pm = scene(fmt, 1, domain=("animals", "greek")[seed % 2], seed=seed)
        case, _ = B.scene_case(tok, {X.LOOKUP: pp, X.RECALL: pm})
        if case is None:
            continue
        pairs, why = P.varied_pairs(tok, [case], {case["scene"]: pp})
        assert why["scenes"] == 1
        for p in pairs:
            made += 1
            o, s = p["ids"]["org"], p["ids"]["alt"]
            diff = S.changed(o, s)
            assert diff and max(diff) < p["pos"], "only tokens before the bridge change"
            assert o[p["pos"] :] == s[p["pos"] :]
            assert tok.decode(o[p["pos"] : p["pos"] + 1]).strip() == p["bridge"]
            assert p["cf_context"] == P.swap_lockers(pp, p["bridge"], p["partner"]) and p["cf_context"] in tok.decode(s)
            assert P.before_pick(pp, p["partner"]) and P.before_pick(pp, p["bridge"])
        if B.order_of(pp) == "after":
            assert not pairs and why["the bridge's locker statement comes after the pick"] == 1
    assert made >= 5, f"{fmt}: too few pairs to test"


# ---- the rule (planted outcomes) ----------------------------------------------------------------------------------


def test_rule_outcomes_on_planted_numbers():
    nan = float("nan")
    rule = lambda prose, js, table: B.pcf_rule({"prose": prose, "json": js, "table": table})  # noqa: E731
    assert rule([0.30, 0.15, 0.4], [0.25, 0.12, 0.4], [0.0, -0.1, 0.1])["outcome"] == "pointer elsewhere"
    assert rule([0.30, 0.15, 0.4], [0.25, 0.12, 0.4], [0.5, 0.3, 0.7])["passed"] == ["prose", "json", "table"]
    assert rule([0.05, -0.1, 0.2], [0.09, 0.0, 0.2], [-0.02, -0.1, 0.1])["outcome"] == "no linear pointer found"
    # one format passes, one is in between: neither
    assert rule([0.30, 0.15, 0.4], [0.15, 0.05, 0.3], [0.0, -0.1, 0.1])["outcome"] == "neither"
    # the lower CI must be above 0.1 (strict): 0.1 itself does not pass
    assert rule([0.30, 0.10, 0.4], [0.25, 0.10, 0.4], [0.0, -0.1, 0.1])["outcome"] == "neither"
    # a point estimate just under 0.2 does not pass; 0.2 computed in floats (1 - 0.8) does
    assert rule([0.199, 0.15, 0.3], [0.25, 0.12, 0.4], [0.0, -0.1, 0.1])["outcome"] == "neither"
    assert rule([1 - 0.8, 0.15, 0.3], [0.25, 0.12, 0.4], [0.0, -0.1, 0.1])["outcome"] == "pointer elsewhere"
    # "below 0.1" is strict on the point estimate
    assert rule([0.1, 0.0, 0.2], [0.0, -0.1, 0.1], [0.0, -0.1, 0.1])["outcome"] == "neither"
    # a format without a cell: never passes; "incomplete" unless two others already make "pointer elsewhere"
    v = rule([0.05, -0.1, 0.2], None, [0.0, -0.1, 0.1])
    assert v["outcome"] == "incomplete" and v["not_tested"] == ["json"]
    assert rule([nan, nan, nan], [0.25, 0.12, 0.4], [0.3, 0.2, 0.4])["outcome"] == "pointer elsewhere"
    # a lower CI that is not a number is never "above 0.1"
    assert rule([0.3, nan, 0.4], [0.25, 0.12, 0.4], [0.0, -0.1, 0.1])["passed"] == ["json"]


N_ENT, PER_ENT = 12, 5  # per format: 12 bridge items x 5 scenes


def _run(root, name: str, plan: dict[str, tuple[str, float] | None]) -> None:
    """A synthetic 45d run: per format a planted lookup loss without the refit basis, ("even", q): q of every item's
    scenes; ("clustered", q): every scene of the first q x 12 items. The random parts never cost a switch; U and the
    recall lose a lot everywhere (the rule must ignore them). None: the format has no rows."""
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(
        json.dumps({"predicted": 12, "pcf_from": "x7_pcf/fit", "model": {"target": "toy"}})
    )
    cases, rows, shares = [], [], []
    for f, how in plan.items():
        for i in range(N_ENT * PER_ENT):
            s, e, j = f"{f}{i}", f"{f}-e{i % N_ENT}", i // N_ENT  # j: the scene's index within its item
            cases.append({"scene": s, "format": f})
            if how is None:
                continue
            kind, q = how
            lost = j < round(q * PER_ENT) if kind == "even" else i % N_ENT < round(q * N_ENT)
            for w in X.READERS:
                base = {"scene": s, "entity": e, "rendering": "chat", "layer": 12, "reader": w, "top": 7, "role": "b"}
                rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
                for d in ("pcf", "alf"):
                    gone = (lost and w == X.LOOKUP) if d == "pcf" else True
                    rows.append(
                        {**base, "dict": d, "k": 4, "omp": "signed", "arm": "no_part", "switched": int(not gone)}
                    )
                    rows.append({**base, "dict": d, "k": 4, "omp": "signed", "arm": "no_rand", "switched": 1})
            for d in ("pcf", "alf"):
                shares.append({"scene": s, "layer": 12, "dict": d, "k": 4, "omp": "signed", "share": 0.03})
    for fname, data in (("cases.jsonl", cases), ("outcomes.jsonl", rows), ("shares.jsonl", shares)):
        (src / fname).write_text("".join(json.dumps(r) + "\n" for r in data))


@pytest.mark.parametrize(
    ("plan", "outcome"),
    [
        ({"prose": ("even", 0.4), "json": ("even", 0.2), "table": ("even", 0.0)}, "pointer elsewhere"),
        ({"prose": ("even", 0.0), "json": ("even", 0.0), "table": ("even", 0.0)}, "no linear pointer found"),
        # json at 0.25 but carried by 3 of 12 items: its lower CI falls below 0.1
        ({"prose": ("even", 0.4), "json": ("clustered", 0.25), "table": ("even", 0.0)}, "neither"),
        ({"prose": ("even", 0.4), "json": None, "table": ("even", 0.0)}, "incomplete"),
    ],
)
def test_verdict_on_synthetic_runs(tmp_path, monkeypatch, plan, outcome):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    _run(tmp_path, "toy_x45d", plan)
    out = B.write_pcf_verdict("toy_x45d", n_boot=500)
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["verdict"]["outcome"] == outcome
    for f, how in plan.items():
        got = blob["lookup_refit"][f]
        if how is None:
            assert got is None
        else:
            assert math.isclose(got[0], how[1], abs_tol=1e-9)
            if how[0] == "even":  # every item loses the same share: the CI is the point
                assert math.isclose(got[1], how[1], abs_tol=1e-9) and math.isclose(got[2], how[1], abs_tol=1e-9)
            else:
                assert got[1] < 0.1
    alf = [c for c in blob["cells"] if c["part"] == "alf" and c["reader"] == X.LOOKUP]
    assert alf and all(math.isclose(c["excess"][0], 1.0) for c in alf)  # U loses everything: not in the rule
    assert "Outcome: " + outcome in (out / "verdict.md").read_text()
    png = B.pcf_figure(out)
    assert png.exists() and png.parent.name.startswith("analysis-") and png.parent.parent == out.parent


def test_verdict_drops_a_format_with_too_few_switches(tmp_path, monkeypatch):
    # every format switches N_ENT * PER_ENT lookups; with the bar one above that, no format counts
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    monkeypatch.setattr(B, "MIN_SWITCHED", N_ENT * PER_ENT + 1)
    _run(tmp_path, "toy_x45d", {"prose": ("even", 0.4), "json": ("even", 0.4), "table": ("even", 0.0)})
    out = B.write_pcf_verdict("toy_x45d", n_boot=200)
    v = json.loads((out / "verdict.json").read_text())["verdict"]
    assert v["outcome"] == "incomplete" and v["too_few_switches"] == list(B.FORMATS)
    assert "does not count" in (out / "verdict.md").read_text()


def test_verdict_refuses_a_run_without_pcf(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    (tmp_path / "r").mkdir()
    (tmp_path / "r" / "manifest.json").write_text(json.dumps({"predicted": 12}))
    with pytest.raises(AssertionError, match="not a 45d run"):
        B.write_pcf_verdict("r", n_boot=10)


# ---- examples -----------------------------------------------------------------------------------------------------


VOCAB = (" ", "<chat>", "The", " frog", " picked", " Answer:", "5", "7")


class ToyTok:
    """Token i decodes to VOCAB[i]; " " encodes to [0]."""

    def decode(self, ids):
        return "".join(VOCAB[i] for i in ids)

    def __call__(self, text, add_special_tokens=False):
        return SimpleNamespace(input_ids=[VOCAB.index(text)])


def test_examples_mark_the_patch_position_and_show_every_arm(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "RESULTS", tmp_path)
    src = tmp_path / "toy_x45d"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"predicted": 12}))
    ids = [1, 2, 4, 3, 5]  # "<chat>The picked frog Answer:", the bridge at 3
    cases, rows = [], []
    for i in range(15):
        rd = {"answer": "5", "cf_answer": "7", "ids": {"org": ids, "alt": ids}}
        cases.append({"scene": f"s{i:02d}", "format": "json", "level": 1, "domain": "animals", "bridge": "frog",
                      "cf_bridge": "cat", "order": "before", "pos": 3, "readers": {"PP": rd, "PM": rd}})  # fmt: skip
        for w in X.READERS:
            for d, arm, _ in B.EXAMPLE_ARMS_45D:
                top = 7 if arm == "whole" or arm == "no_rand" else 6
                rows.append({"scene": f"s{i:02d}", "layer": 12, "reader": w, "dict": d, "arm": arm, "top": top,
                             "role": "b" if top == 7 else "A"})  # fmt: skip
    (src / "cases.jsonl").write_text("".join(json.dumps(c) + "\n" for c in cases))
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    blob, md = B.examples_blob(ToyTok(), "toy_x45d")
    picked = {e["item_id"] for e in blob["examples"]}
    assert len(picked) == 10 and len(blob["examples"]) == 20  # 10 items x both readers
    assert picked == set(sorted(random.Random(0).sample(sorted(c["scene"] for c in cases), 10)))
    ex = blob["examples"][0]
    sp = ex["spans"][0]
    assert ex["prompt"] == "<chat>The picked frog Answer: " and ex["prompt"][sp["start"] : sp["end"]] == " frog"
    assert len(ex["numbers"]) == len(B.EXAMPLE_ARMS_45D)
    assert ex["numbers"]["without the refit basis"] == "'5', original answer"
    assert ex["answers"]["edited"] == "'7', changed answer"
    assert "<chat>The picked⟦ frog⟧ Answer: " in "\n".join(md)
