"""x0_necessity's cells, labels and rule (jobs/c3/X0.md) on synthetic outcomes (no model)."""

import numpy as np

from scripts import x0_necessity as X


def outcomes(n: int, whole: int, no_part: int, no_rand: int) -> dict[str, list[int]]:
    """Per-item 0/1 switches with the given counts; items switched by a removal arm are a subset of the whole's."""
    return {"whole": [int(i < whole) for i in range(n)], "no_part": [int(i < no_part) for i in range(n)],
            "no_rand": [int(i < no_rand) for i in range(n)]}  # fmt: skip


def ents(n: int, k: int = 20) -> list[str]:
    return [f"e{i % k}" for i in range(n)]


def test_lookup_around_and_recall_through():
    lk = X.cell(outcomes(200, 160, 156, 156), ents(200), n_boot=2000)
    rc = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=2000)
    assert lk["label"] == "around" and abs(lk["excess"][0]) < 1e-9
    assert rc["label"] == "through" and rc["Jdep"][0] > 0.7 and rc["excess"][1] >= 0.10
    assert X.split(lk, rc) and X.verdict(lk, rc) == "confirmed"


def test_invalid_cells_cannot_tell():
    weak = X.cell(outcomes(200, 50, 50, 50), ents(200), n_boot=500)  # S_whole 0.25 < 0.30
    few = X.cell(outcomes(80, 28, 28, 28), ents(80), n_boot=500)  # 35% but 28 < 30 items switched
    ok = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=500)
    assert weak["label"] == few["label"] == "can't tell"
    assert X.verdict(weak, ok) == X.verdict(ok, few) == "can't tell"


def test_kill_and_the_zone_between():
    rc = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=500)
    lk_needs = X.cell(outcomes(200, 160, 100, 156), ents(200), n_boot=500)  # excess 0.35
    assert X.verdict(lk_needs, rc) == "killed"
    lk_between = X.cell(outcomes(200, 160, 136, 160), ents(200), n_boot=500)  # excess 0.15
    assert X.verdict(lk_between, rc) == "not confirmed"
    lk = X.cell(outcomes(200, 160, 160, 160), ents(200), n_boot=500)
    rc_flat = X.cell(outcomes(200, 180, 150, 175), ents(200), n_boot=500)  # recall Jdep 0.17 < 0.20
    assert X.verdict(lk, rc_flat) == "killed"


def test_dependence_is_relative_to_the_whole_edit():
    c = X.cell(outcomes(100, 50, 25, 50), ents(100), n_boot=500)
    assert c["Jdep"][0] == 0.5 and c["Rdep"][0] == 0.0 and c["excess"][0] == 0.5


def test_resamples_are_paired_across_arms():
    # no_part identical to whole: every resample's Jdep is exactly 0, so its interval is a point
    sw = outcomes(120, 70, 70, 50)
    c = X.cell(sw, ents(120, 12), n_boot=1000)
    assert c["Jdep"] == [0.0, 0.0, 0.0]


def test_correlated_entities_widen_the_interval():
    n = 200
    rng = np.random.default_rng(0)
    whole = [1] * n
    per_entity = rng.integers(0, 2, 10)  # each entity's items all lose or all keep the switch without J
    no_part = [int(per_entity[i // 20]) for i in range(n)]
    sw = {"whole": whole, "no_part": no_part, "no_rand": whole}
    clustered = X.cell(sw, [f"e{i // 20}" for i in range(n)], n_boot=4000)
    independent = X.cell(sw, [f"e{i}" for i in range(n)], n_boot=4000)
    width = lambda c: c["Jdep"][2] - c["Jdep"][1]  # noqa: E731
    assert width(clustered) > 2 * width(independent)


def test_h_token_branches():
    around = X.cell(outcomes(200, 160, 156, 156), ents(200), n_boot=500)
    needs = X.cell(outcomes(200, 160, 100, 156), ents(200), n_boot=500)
    assert X.h_token(around, needs).startswith("token identity")
    assert X.h_token(around, around).startswith("neither")
    assert X.h_token(needs, needs).startswith("not applicable")
