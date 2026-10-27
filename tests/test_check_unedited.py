from scripts.check_unedited import check


def test_all_right() -> None:
    rows = [{"kind": "none", "role": "A"}, {"kind": "none", "role": "A"}, {"kind": "push", "role": "b"}]
    assert check(rows) == (2, 2)


def test_one_wrong_is_counted() -> None:
    rows = [{"kind": "none", "role": "A"}, {"kind": "none", "role": "b"}]
    assert check(rows) == (2, 1)


def test_no_unedited_rows() -> None:
    assert check([{"kind": "push", "role": "A"}]) == (0, 0)
