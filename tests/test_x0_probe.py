"""x0_probe: folds hold whole entities out, the probe finds a planted linear signal and not noise, item parsing."""

import numpy as np

from scripts import x0_probe as P

CASE = {"scene": "P2-L0-0000", "bridge": "frog", "domain": "animals", "upstream": True, "cf_bridge": "tick", "pos": 43,
        "context": "Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of "
                   "the frog is 5. Noah picked the tick. Iris picked the frog.",
        "readers": {"PP": {"question": "Which locker belongs to Iris's pick?", "answer": "5"}}}  # fmt: skip


def test_positions_and_item():
    assert P.positions(CASE) == (5, 3, 6)
    it = P.item_of(CASE, x0=True)
    assert (it["order"], it["answer"], it["locker_index"], it["pick_index"]) == ("before", "5", 3, 5)


def synthetic(n_ent=20, per=10, d=64, signal=True, seed=0):
    rng = np.random.default_rng(seed)
    items, rows = [], []
    for e in range(n_ent):
        for _ in range(per):
            digit = str(rng.integers(1, 10))
            pick = int(rng.integers(3, 6))
            items.append({"entity": f"e{e}", "answer": digit, "locker_index": pick - 1, "pick_index": pick})
            x = rng.normal(size=d)
            if signal:
                x[int(digit)] += 4.0
            rows.append(x)
    return np.array(rows), items


def test_grouped_folds_hold_entities_out():
    groups = [f"e{i % 13}" for i in range(130)]
    f = P.folds(groups, groups, True, 5)
    for g in set(groups):
        assert len({f[i] for i, x in enumerate(groups) if x == g}) == 1
    assert len(set(f.tolist())) == 5


def test_stratified_folds_spread_classes():
    labels = [f"e{i % 7}" for i in range(70)]
    f = P.folds(labels, labels, False, 5)
    for c in set(labels):
        assert len({f[i] for i, x in enumerate(labels) if x == c}) == 5


def test_probe_finds_planted_signal_not_noise():
    x, items = synthetic(signal=True)
    hit = P.score(x, items, "answer digit", n_boot=200)
    assert hit["probe"][0] > 0.9 and hit["probe_minus_best"][1] > 0.5
    x, items = synthetic(signal=False)
    null = P.score(x, items, "answer digit", n_boot=200)
    assert null["probe"][0] < 0.25 and null["probe_minus_best"][1] < 0.05


def test_structure_baseline_reads_the_pick_index():
    x, items = synthetic(signal=False)
    r = P.score(x, items, "locker sentence", n_boot=200)
    assert r["structure"][0] == 1.0 and r["best_baseline"] == "structure"
