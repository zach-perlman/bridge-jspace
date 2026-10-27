"""pointer_order's pure helpers (no model): what each reading predicts, the read test's classes, splits, fit prompts."""

import pytest

import scripts.pointer_order as PO


def layout(f: int, n: int = PO.N_SLOTS) -> list[int | None]:
    """The 6 cells of a scene whose filler sits in cell f: statement indices in order, None for the filler."""
    cells: list[int | None] = list(range(n))
    cells.insert(f, None)
    return cells


def test_target_case_matches_a_brute_force_layout():
    for f in range(PO.N_SLOTS + 1):
        cells = layout(f)
        for a in range(PO.N_SLOTS):
            for j in range(PO.N_SLOTS):
                if j == a:
                    continue
                case, order_stmt, token_stmt = PO.target_case(a, f, j)
                assert order_stmt == j  # the order reading: the j-th statement, wherever it sits
                assert token_stmt == cells[j]  # the token reading: whatever sits in cell j (fitted class j = cell j)
                assert cells.index(j) == j + (j >= f)  # statement j's own cell
                expected = ("agree" if j < f else "filler" if j == f else
                            "separate_on_current" if cells[j] == a else "separate")  # fmt: skip
                assert case == expected
                if case == "separate":
                    assert token_stmt not in (None, j, a)  # three distinct digits: order, token, answer org


def test_separate_targets_never_point_back_at_the_current_statement_when_it_precedes_the_filler():
    for f in range(1, PO.N_SLOTS + 1):
        for a in range(f):  # asked statement before the filler: the primary cut
            for j in range(f + 1, PO.N_SLOTS):
                assert PO.target_case(a, f, j)[0] == "separate"


def test_read_case():
    assert PO.read_case(1, 3) == ("pre", 1)  # before the filler: order and cell agree
    assert PO.read_case(2, 1) == ("post", 3)  # after it: the token reading is one cell later
    assert PO.read_case(4, 2) == ("post_unreadable", None)  # cell 5 has no fitted class


def test_scene_split_is_seeded_disjoint_and_complete():
    names = [f"s{i}" for i in range(11)]
    fit, steer = PO.scene_split(names)
    assert sorted(fit + steer) == sorted(names) and not set(fit) & set(steer)
    assert (fit, steer) == PO.scene_split(list(reversed(names)))
    assert len(fit) == 5


def test_fit_prompts_keep_only_prompts_whose_asked_statement_precedes_the_filler():
    def item(f, a, df, da):
        return {"filler_cell": f, "slots": {"query": a},
                "sources": {"dissoc": {"filler_cell": df, "query_slot": da}, "same": {"filler_cell": f, "query_slot": a}}}  # fmt: skip

    types = {"off": item(4, 1, 2, 3), "pln": item(4, 1, 5, 0), "ref": item(4, 1, 0, 2)}
    got = PO.fit_prompts(types)
    assert ("pln", "base", 4, 1) in got and ("pln", "same", 4, 1) in got
    assert ("pln", "dissoc", 5, 0) in got
    assert ("off", "dissoc", 2, 3) not in got and ("ref", "dissoc", 0, 2) not in got
    assert all(f > a for _, _, f, a in got)


def test_cluster_boot():
    pt, lo, hi = PO.cluster_boot([1, 1, 0, 1], [0, 0, 0, 0], ["a", "a", "b", "c"], n_boot=300)
    assert pt == pytest.approx(0.75) and lo <= pt <= hi
    assert PO.cluster_boot([], [], [])[0] != PO.cluster_boot([], [], [])[0]  # nan when empty
