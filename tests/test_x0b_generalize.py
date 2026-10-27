"""x0b_generalize: the asked pick and the bridge's locker are found in every format, the alt changes only the asked
pick, and the order is read from the context."""

import random

import pytest

from scripts import tasks_v2 as T
from scripts import x0b_generalize as B


def scene(fmt: str, level: int, domain: str = "animals", seed: int = 0) -> tuple[dict, dict]:
    rng = random.Random(seed)
    its = None
    while its is None:
        its = T.make_scene(rng, "P", ["PP", "PM"], domain, fmt, T.LEVELS[level], list(T.DOMAINS))
    pp, pm = its
    return {**pp, "id": "PP-x", "scene": "s"}, {**pm, "id": "PM-x", "scene": "s"}


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
@pytest.mark.parametrize("level", [0, 2])
def test_alt_changes_only_the_asked_pick(fmt, level):
    pp, pm = scene(fmt, level)
    cands = B.alt_candidates(pp, pm)
    assert cands, "the scene has another pick with a different locker and memory number"
    t = cands[0]
    alt = B.alt_context(pp, t)
    person = pp["facts"]["person"]
    pick_org, _ = B.statements(pp, person, pp["facts"]["x"])
    pick_alt, _ = B.statements(pp, person, t)
    assert alt == pp["context"].replace(pick_org, pick_alt)
    assert alt.count(pick_alt) == 1 and pick_org not in alt


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_order_matches_the_statement_offsets(fmt):
    seen = set()
    for seed in range(40):
        pp, _ = scene(fmt, 1, seed=seed)
        seen.add(B.order_of(pp))
    assert seen == {"before", "after"}


@pytest.mark.parametrize("fmt", ["prose", "json", "table"])
def test_ordinals_match_the_rendered_order(fmt):
    pp, _ = scene(fmt, 1, domain="greek", seed=7)
    o = B.ordinals(pp)
    f, ctx = pp["facts"], pp["context"]
    starts = sorted(ctx.index(B.statements(pp, f["person"], t)[1]) for t in f["locker"])
    assert starts[o["locker_index"]] == ctx.index(B.statements(pp, f["person"], f["x"])[1])
    before, total = map(int, o["layout"].split("/"))
    assert total == len(f["locker"]) and (before > o["locker_index"]) == (B.order_of(pp) == "before")


def test_rule_bars():
    cell = lambda ex, hi, valid=True: {"valid": valid, "excess": [ex, ex - 0.05, hi]}  # noqa: E731
    assert B.rule(cell(0.05, 0.12), cell(0.6, 0.7), [0.5, 0.3, 0.7]) == "holds"
    assert B.rule(cell(0.05, 0.25), cell(0.6, 0.7), [0.5, 0.3, 0.7]) == "mixed"
    assert B.rule(cell(0.22, 0.30), cell(0.6, 0.7), [0.5, 0.3, 0.7]) == "fails"
    assert B.rule(cell(0.05, 0.12), cell(0.1, 0.2), [0.05, -0.05, 0.08]) == "fails"
    assert B.rule(cell(0.05, 0.12, valid=False), cell(0.6, 0.7), [0.5, 0.3, 0.7]) == "can't tell"


def test_candidates_differ_in_locker_and_memory_number():
    pp, pm = scene("prose", 2, domain="instruments", seed=3)
    values = T.DOMAINS["instruments"].values
    x = pp["facts"]["x"]
    for t in B.alt_candidates(pp, pm):
        assert pp["facts"]["locker"][t] != pp["facts"]["locker"][x] and values[t] != values[x]
