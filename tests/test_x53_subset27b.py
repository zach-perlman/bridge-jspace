import numpy as np
import pytest

from scripts import x53_subset27b as M


def rows_for(scene: str, cond: str, entity: str, routes: dict[str, str], reader: str = "PP") -> list[dict]:
    return [{"scene": scene, "condition": cond, "entity": entity, "reader": reader, "arm": a, "route": r}
            for a, r in routes.items()]  # fmt: skip


def scene(scene: str, cond: str, entity: str, whole: str, **arms: str) -> list[dict]:
    base = {"whole": whole, "no_alf": "identity", "no_alf_rand": "identity", "keep_alf": "original",
            "keep_alf_rand": "original"}  # fmt: skip
    return rows_for(scene, cond, entity, base | arms)


def test_subset_keeps_only_position_under_the_whole_change_in_c1_c2_lookup_rows():
    rows = (scene("C1-0001", "C1", "frog", "position") + scene("C2-0002", "C2", "goose", "identity")
            + scene("C2-0003", "C2", "goose", "position") + scene("C0-0004", "C0", "cat", "position")
            + rows_for("C2-0005", "C2", "cat", {"whole": "position"}, reader="PM"))  # fmt: skip
    by = M.lookup_rows(rows)
    assert set(by) == {("C1", "C1-0001"), ("C2", "C2-0002"), ("C2", "C2-0003")}  # C0 and recall rows left out
    assert M.position_subset(by) == [("C1", "C1-0001"), ("C2", "C2-0003")]


def test_duplicate_rows_for_one_scene_and_arm_are_refused():
    rows = scene("C1-0001", "C1", "frog", "position") + scene("C1-0001", "C1", "frog", "position")
    with pytest.raises(AssertionError):
        M.lookup_rows(rows)


def test_subset_cell_shares_back_left_and_differences():
    rows = []
    for i in range(10):  # 10 position scenes over 5 items: keep_alf brings 3 back, no_alf leaves 1, no_alf_rand 6
        arms = {"keep_alf": "position" if i < 3 else "original", "no_alf": "position" if i < 1 else "identity",
                "no_alf_rand": "position" if i < 6 else "identity"}  # fmt: skip
        rows += scene(f"C2-{i:04d}", "C2", f"e{i % 5}", "position", **arms)
    rows += scene("C2-0100", "C2", "e0", "identity", keep_alf="position")  # outside the subset: must not count
    by = M.lookup_rows(rows)
    c = M.subset_cell(by, M.position_subset(by), n_boot=200)
    assert c["n"] == 10 and c["entities"] == 5
    assert c["share"]["whole"][0] == 1.0
    assert c["back"][0] == pytest.approx(0.3) and c["left"][0] == pytest.approx(0.1)
    assert c["removal_beyond_random"][0] == pytest.approx(0.5)
    assert c["alone_beyond_random"][0] == pytest.approx(0.3)
    lo, hi = c["back"][1:]
    assert lo <= 0.3 <= hi
    assert M.subset_cell(by, [], n_boot=10) is None


def test_rule_bars_are_inclusive_and_both_clauses_are_needed():
    assert M.pattern(0.25, 0.10)  # exactly at both bars counts
    assert M.pattern(0.9, 0.0)
    assert not M.pattern(0.2499, 0.05)  # too little brought back
    assert not M.pattern(0.5, 0.1001)  # too much left without the address
    assert M.LABEL[True] == "same mechanism, used less" and M.LABEL[False] == "the 27B differs"


def test_swap_cell_counts_targets_on_the_subset_scenes_only():
    def w(sc, kind, s, cls, j=0):
        return {"scene": sc, "entity": sc[-1], "reader": "PP", "kind": kind, "s": s, "j": j, "class": cls}

    rows = [w("C2-a", "none", 0, "slot0"), w("C2-a", "write", 2, "target"), w("C2-a", "write", 2, "original"),
            w("C2-b", "none", 0, "slot1", j=1), w("C2-b", "write", 2, "target"), w("C2-b", "write", 2, "third"),
            w("C2-a", "random", 4, "original"), w("C2-b", "random", 4, "target"),
            w("C2-c", "write", 2, "target"), w("C2-c", "write", 2, "target")]  # fmt: skip
    out = M.swap_cell(rows, {"C2-a", "C2-b"}, n_boot=100)
    assert out["swap"]["n_writes"] == 4 and out["swap"]["target"][0] == 0.5
    assert out["swap"]["third"][0] == 0.25 and out["swap_rand"]["target"][0] == 0.5
    assert out["j"] == {0: 1, 1: 1}
    assert np.isfinite(out["swap"]["target"][1])
