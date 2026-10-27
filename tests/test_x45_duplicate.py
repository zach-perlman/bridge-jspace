"""Duplicate check (scripts/x45_duplicate.py): where the duplicate pick sits, and the paired group extra loss."""

import numpy as np

from scripts import x0_necessity as X
from scripts import x45_duplicate as D


def _case(context: str, asked: str, org: str, alt: str) -> dict:
    q = f"Which locker belongs to {asked}'s pick? Answer with a single digit and nothing else."
    return {"context": context, "bridge": org, "cf_bridge": alt, "readers": {X.LOOKUP: {"question": q}}}


def test_duplicate_side_reads_the_pick_sentences():
    ctx = ("Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog "
           "is 5. Noah picked the tick. Iris picked the frog.")  # fmt: skip
    assert D.duplicate_side(_case(ctx, "Iris", "frog", "tick")) == "before"  # Noah's tick comes first
    assert D.duplicate_side(_case(ctx, "Noah", "tick", "frog")) == "after"  # Iris's frog comes later
    assert D.duplicate_side(_case(ctx, "Iris", "frog", "owl")) == "none"
    greek = "Ann picked iota. The locker of iota is 3. The locker of delta is 4. Leo picked delta."
    assert D.duplicate_side(_case(greek, "Leo", "delta", "iota")) == "before"


def test_measures_split_the_groups_on_the_same_draws():
    # 40 items, 10 entities; group before: the part costs 0.5 of the switches, after: 0; the random part costs nothing
    items = [f"s{i}" for i in range(40)]
    side = {s: "before" if i % 2 == 0 else "after" for i, s in enumerate(items)}
    ents = [f"e{i % 10}" for i in range(40)]
    part = np.array([0.0 if (i % 2 == 0 and i % 4 == 0) else 1.0 for i in range(40)])
    sw = {X.LOOKUP: {"whole": np.ones(40), "no_part": part, "no_rand": np.ones(40)}}
    got = D.measures(items, side, sw, ents, {"x": (X.LOOKUP, "no_part", "no_rand")}, n_boot=300)
    c = got["cells"]["x"]
    assert got["n"] == {"before": 20, "after": 20, "none": 0}
    assert abs(c["before"][0] - 0.5) < 1e-9 and abs(c["after"][0]) < 1e-9 and abs(c["diff"][0] - 0.5) < 1e-9
    assert c["diff"][1] > 0 and not c["no_difference"]


def test_gap_is_recall_minus_lookup():
    items = [f"s{i}" for i in range(20)]
    side = {s: "before" if i < 10 else "after" for i, s in enumerate(items)}
    ones, half = np.ones(20), np.array([i % 2 for i in range(20)], dtype=float)
    sw = {X.LOOKUP: {"whole": ones, "no_part": ones, "no_rand": ones},
          X.RECALL: {"whole": ones, "no_part": half, "no_rand": ones}}  # fmt: skip
    parts = {"jpp_lookup": (X.LOOKUP, "no_part", "no_rand"), "jpp_recall": (X.RECALL, "no_part", "no_rand")}
    got = D.measures(items, side, sw, [f"e{i % 5}" for i in range(20)], parts, n_boot=200)
    assert abs(got["cells"]["gap"]["before"][0] - 0.5) < 1e-9 and got["cells"]["gap"]["no_difference"]
