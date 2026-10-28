"""The figures drawn after the overnight queue (Dan 27 Oct ~01:05; readme_story_figures.f03b_q, f03c_p, s01c_nochat),
tested on fake data in the exact on-disk format: 45q's and 45p's verdict folders are made by their own verdict stages
from planted runs, 45i''s runs are planted x0_necessity runs without the chat template. Nothing is written to figures/;
each saved figure is checked with plot_style.overlaps(), the glossary's banned variants and the retired terms."""

from __future__ import annotations

import json

import pytest
import test_readme_build as RB
from matplotlib.text import Text

from bridge_jspace import pins
from bridge_jspace import plot_style as PS
from scripts import check_figure_terms as C
from scripts import readme_story_figures as F
from scripts import story_style as S
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x45p as P

N_BOOT = 100


@pytest.fixture
def saved(tmp_path, monkeypatch):
    """S.OUT / S.SUPP in tmp_path; per saved figure its overlaps(), drawn texts and folder; data.csv rows in S.ROWS."""
    monkeypatch.setattr(S, "OUT", tmp_path / "story")
    monkeypatch.setattr(S, "SUPP", tmp_path / "supp")
    monkeypatch.setattr(S, "ROWS", [])
    got: dict[str, dict] = {}
    orig = S.save

    def save(fig, name, supp=False):
        got[name] = {"overlaps": PS.overlaps(fig), "supp": supp,
                     "texts": [t.get_text() for t in fig.findobj(Text) if t.get_text().strip()],
                     "title": fig._suptitle.get_text() if fig._suptitle else ""}  # fmt: skip
        orig(fig, name, supp)

    monkeypatch.setattr(S, "save", save)
    S.setup()
    return got


def check(fig: dict) -> None:
    flat = [("fig", t) for t in fig["texts"]]
    assert fig["overlaps"] == [], fig["overlaps"]
    assert not RB.banned(flat), RB.banned(flat)
    assert not C.retired(flat), C.retired(flat)


# ---- 45q ------------------------------------------------------------------------------------------------------------


def q_rate(arm: str, family: str, layer: int | None, top: int, holds: bool) -> float:
    """A planted switch rate per arm: S 0.9; 45b's copy c at L 0.7 (holds) or 0.2, a 0.1 or 0.5; the sweep's bridge
    word falling with depth and the locker-sentence copies rising, the number and the period 0."""
    if arm == B.S_ARM:
        return 0.9
    if family == "45b":
        return {"a": 0.1 if holds else 0.5, "c": 0.7 if holds else 0.2, "d": 0.3}.get(arm, 0.6)
    if family == "45n":
        return {"c_nojpp": 0.6, "c_norand": 0.65}[arm]
    if family == "sweep":
        kind, frac = arm.rstrip("0123456789"), (layer or 0) / top
        return {"bw": 1 - frac, "ls": frac, "li": 0.7 * frac, "lr": 0.3 * frac}.get(kind, 0.0)
    return 0.0


def write_q(root, name: str, target: str, holds: bool | None, n: int = 24) -> None:
    """A planted 45q run (q-run's files): n items passing the sanity check, every arm of q_arms read by both readers;
    holds None: no outcomes yet (pending)."""
    layer = X.PREDICTED[target]
    sweep = B.q_sweep_layers(2 * layer + 2)
    arms = B.q_arms(layer, sweep)
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"test": "45q", "model": {"target": target}, "main_run": "m45",
                                                   "layer": layer, "arm_layers": B.arm_layers(layer)}))  # fmt: skip
    (src / "plan.json").write_text(json.dumps({"locker_after": n + 3, "dropped": {"misaligned": 3}, "items": n,
                                               "align": {"token": n}}))  # fmt: skip
    cases = [{"scene": f"s{i}", "pos": 1, "readers": {w: {"ids": {"org": [1, 2, 3], "alt": [1, 9, 3]}} for w in X.READERS},
              "stored": {"whole": {}, "S_read": {}}} for i in range(n)]  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", cases)
    if holds is None:
        return
    rows = []
    for arm, (family, la) in [*arms.items(), (B.S_ARM, ("-", None))]:
        k = round(q_rate(arm, family, la, sweep[-1], holds) * n)
        rows += [{"scene": f"s{i}", "entity": f"e{i % 6}", "reader": w, "arm": arm, "family": family, "layer": la,
                  "switched": int(i < k)} for i in range(n) for w in X.READERS]  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "norms.jsonl", [{"scene": f"s{i}", "arm": "c_link", "layer": layer, "positions": 12,
                                         "changed_positions": 12, "median_jpp_share": 0.2} for i in range(n)])  # fmt: skip


@pytest.mark.parametrize(("plants", "label"), [((True, True, False), "holds"), ((False, False, None), "does not hold")])
def test_fig3b_45q_on_planted_runs(tmp_path, monkeypatch, saved, plants, label):
    monkeypatch.setattr(B, "RESULTS", tmp_path / "x45b")
    names = ["q9", "q27", "qmuse"]
    for name, (target, _), holds in zip(names, F.Q_MODELS, plants, strict=True):
        write_q(B.RESULTS, name, target, holds)
    landed = [n for n, h in zip(names, plants, strict=True) if h is not None]
    v_dir = B.stage_q_verdict(names, n_boot=N_BOOT)
    l_dir, s_dir = B.stage_q_link_table(landed, n_boot=N_BOOT), B.stage_q_sweep_table(landed, n_boot=N_BOOT)
    assert json.loads((v_dir / "x45q.json").read_text())["verdict"]["label"] == ("pending" if None in plants else label)
    F.f03b_q(S.setup(), v_dir, l_dir, s_dir)
    fig = saved["fig03b_layers"]
    check(fig)
    assert not fig["supp"] and "locker after the pick" in fig["title"].lower()
    assert ("not run" in fig["texts"]) == (None in plants)
    rows = [r for r in S.ROWS if r["figure"] == "fig03b"]
    assert {r["model"] for r in rows} == {t for (t, _), h in zip(F.Q_MODELS, plants, strict=True) if h is not None}
    supp = saved["s03d_link_copy_variants"]  # the other copies and 45n's parts: the supplementary figure
    check(supp)
    assert supp["supp"]
    rows_supp = [r for r in S.ROWS if r["figure"] == "s03d"]
    assert any("copy at L without the J++ part" in r["quantity"] for r in rows_supp)
    assert any("item's own tokens" in r["quantity"] for r in rows_supp)
    assert not any("item's own tokens" in r["quantity"] for r in rows)


def test_fig3b_dispatch_keeps_the_45b_sweep_until_45q_lands(monkeypatch, saved):
    if not (pins.RESULTS_DIR / "x45b_binding" / F.SWEEP_RUNS["9b"]).exists():
        pytest.skip("the 45b sweep is not in results/")
    monkeypatch.setitem(F.LANDED, "45q", None)
    F.f03b(S.setup())
    assert list(saved) == ["fig03b_layers"] and not saved["fig03b_layers"]["supp"]


# ---- 45p ------------------------------------------------------------------------------------------------------------

PLAN = {"items": 60, "items_at_L": 90, "alt locker vs asked pick": {"before": 60, "after": 30}, "dropped": {},
        "tokens": {"new 1, control 1": 60}, "control": {"before the new item, before the asked pick": 60}}  # fmt: skip


def write_p(root, name: str, target: str, recall: dict[str, int], n: int = 60) -> None:
    """A planted 45p run (run's files): the recall switches the first recall[arm] items per arm, the lookup half of
    them."""
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "run_45m": "m45"}))
    (src / "plan.json").write_text(json.dumps(PLAN))
    X.write_jsonl(src / "cases.jsonl", [{"scene": f"s{i}", "stored": {"whole": {"PP": 1, "PM": 1}, "a1": {"PP": 1, "PM": 1}}}
                                        for i in range(n)])  # fmt: skip
    rows = [{"scene": f"s{i}", "entity": f"e{i % 12}", "reader": w, "arm": arm,
             "switched": int(i < (recall.get(arm, 0) if w == X.RECALL else recall.get(arm, 0) // 2)),
             "right": int(arm in ("none", "o2"))} for i in range(n) for w in X.READERS for arm in P.ARMS]  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "norms.jsonl", [{"whole_jpp_share": 0.3, "new_jpp_share": [0.5], "new_rand_share": [0.49],
                                         "control_jpp_share": [0.4]} for _ in range(n)])  # fmt: skip
    X.write_jsonl(src / "examples_greedy.jsonl", [])


HOLD = {"whole": 50, "a1": 40, "a2": 10, "a3": 30, "a4": 25}  # loss 0.75 / 0.25 / 0.375: holds
FAIL = {"whole": 50, "a1": 40, "a2": 10, "a3": 15, "a4": 30}  # 0.75 vs 0.625: fails the random bar


@pytest.mark.parametrize(("plants", "story"), [((HOLD, HOLD, FAIL), True), ((FAIL, FAIL, HOLD), False)])
def test_fig3c_45p_on_planted_runs(tmp_path, monkeypatch, saved, plants, story):
    monkeypatch.setattr(P, "RESULTS", tmp_path / "x45p")
    monkeypatch.setattr(P, "dan_answer", lambda: "yes · 65%")
    monkeypatch.setattr(P, "example_lines", lambda run: [])  # the planted cases hold no prompts
    names = ["p9", "p27", "pmuse"]
    for name, (target, _), plant in zip(names, F.Q_MODELS, plants, strict=True):
        write_p(P.RESULTS, name, target, plant)
    out = P.stage_verdict(names, n_boot=N_BOOT)
    name = F.f03c_p(S.setup(), out)
    assert name == ("fig03c_earlier_mention" if story else "s03c_earlier_mention")
    fig = saved[name]
    check(fig)
    assert fig["supp"] is not story
    assert ("rule not met" in fig["title"]) is not story
    assert "not run" in fig["texts"]  # the 122B: no 45p run
    rows = [r for r in S.ROWS if r["figure"] == "fig03c"]
    loss = next(r for r in rows if r["model"] == "qwen3.5-9b" and r["quantity"].startswith("45p, a2: recall"))
    assert loss["value"] == pytest.approx(0.75)


# ---- 45i' -----------------------------------------------------------------------------------------------------------


def nochat_case(i: int, before: bool) -> dict:
    lockers = "The locker of the frog is 5. The locker of the tick is 2."
    picks = "Iris picked the frog. Bob picked the tick."
    ctx = f"{lockers} {picks}" if before else f"{picks} {lockers}"
    return {"scene": f"n{i}", "rendering": "nochat", "context": ctx, "upstream": False, "domain": "animals",
            "bridge": "frog", "cf_bridge": "tick",
            "readers": {X.LOOKUP: {"question": "Which locker belongs to Iris's pick?"},
                        X.RECALL: {"question": "How many legs does Iris's pick have?"}}}  # fmt: skip


def write_nochat(root, name: str, target: str, n: int = 40) -> None:
    """A planted x0_necessity run without the chat template: half the scenes locker-before; the recall needs the J++
    part (switches without it in a quarter), the lookup does not."""
    src = root / name
    src.mkdir(parents=True)
    la = X.PREDICTED[target]
    (src / "manifest.json").write_text(json.dumps({"renderings": ["nochat"], "predicted": la, "gate": 0.75}))
    X.write_jsonl(src / "cases.jsonl", [nochat_case(i, i % 2 == 0) for i in range(n)])
    base = {"rendering": "nochat", "layer": la, "upstream": False}
    rows = []
    for i in range(n):
        for w in X.READERS:
            for arm, d, k, omp in (
                ("whole", "-", 0, "-"),
                ("no_part", "jpp", 25, "signed"),
                ("no_rand", "jpp", 25, "signed"),
            ):
                sw = 1 if arm != "no_part" or w == X.LOOKUP else int(i % 4 == 0)
                rows.append({**base, "scene": f"n{i}", "entity": f"e{i % 8}", "reader": w, "arm": arm, "dict": d,
                             "k": k, "omp": omp, "switched": sw})  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)


def test_supp_45i_on_planted_runs(tmp_path, monkeypatch, saved):
    if not sorted((pins.RESULTS_DIR / "x0_composition").glob("split-by-order-*/split.json")):
        pytest.skip("the split by sentence order is not in results/")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    write_nochat(X.RESULTS, "n9", "qwen3.5-9b")
    write_nochat(X.RESULTS, "n27", "qwen3.6-27b")
    F.s01c_nochat(S.setup(), {"9b": "n9", "27b": "n27"})
    fig = saved["s01c_no_chat_template"]
    check(fig)
    assert fig["supp"]
    rows = [r for r in S.ROWS if r["figure"] == "s01c"]
    gap = next(r for r in rows if r["model"] == "qwen3.5-9b" and r["quantity"].endswith("all scenes, without the chat "
                                                                                          "template: gap"))  # fmt: skip
    assert gap["value"] == pytest.approx(0.75) and gap["n"] == 40  # recall 0.75, lookup 0


def test_nothing_drawn_before_the_tests_land(monkeypatch, saved):
    for key in ("45p", "45i"):
        monkeypatch.setitem(F.LANDED, key, None)
    F.f03c(S.setup())
    F.s01c(S.setup())
    assert saved == {}
