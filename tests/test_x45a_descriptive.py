"""45a descriptive table (scripts/x45a_descriptive.py) on planted rows."""

from scripts import x0_necessity as X
from scripts import x45a_descriptive as D


def _rows() -> list[dict]:
    """4 base scenes, two first-locker moves; V0: position everywhere; V1: the first-locker scenes go to identity under
    the whole change and to original pointer-only. Base scene 3 is missing in V1 (dropped from every variant)."""
    rows = []
    for b in range(4):
        move = [0, 1] if b < 2 else [1, 2]
        for v in ("V0", "V1"):
            if v == "V1" and b == 3:
                continue
            for arm in ("whole", "keep_alf", "no_alf"):
                route = "position" if v == "V0" else {"whole": "identity", "keep_alf": "original"}.get(arm, "other")
                rows.append({"reader": X.LOOKUP, "variant": v, "base_scene": f"b{b}", "move": move, "arm": arm,
                             "route": route})  # fmt: skip
                rows.append({"reader": X.RECALL, "variant": v, "base_scene": f"b{b}", "move": move, "arm": arm,
                             "route": None})  # fmt: skip
    return rows


def test_route_table_on_first_locker_moves_of_common_scenes():
    t = D.route_table(_rows())
    assert t["n"] == 2 and t["variants"] == ["V0", "V1"]
    assert t["share"]["whole|V0"]["position"] == 1.0
    assert t["share"]["whole|V1"]["identity"] == 1.0 and t["share"]["keep_alf|V1"]["original"] == 1.0
    assert abs(sum(t["share"]["keep_alf|V1"].values()) - 1.0) < 1e-9


def test_beta_and_accuracy_tables():
    betas = [{"variant": "V1", "beta": b, "entity": f"e{i % 3}"} for i, b in enumerate((0.2, 0.4, 0.6, 0.8))]
    bt = D.beta_table(betas, 200)
    assert (
        bt["V1"]["n"] == 4
        and abs(bt["V1"]["beta"][0] - 0.5) < 1e-9
        and bt["V1"]["beta"][1] <= 0.5 <= bt["V1"]["beta"][2]
    )
    comp = [
        {"scene": s, "reader": X.LOOKUP, "variant": "org", "read_right": ok} for s, ok in (("a", True), ("b", False))
    ]
    acc = D.accuracy_table(comp, {"a": "V0", "b": "V0"})
    assert acc["V0"][f"{X.LOOKUP}|org"] == {"right": 1, "n": 2, "share": 0.5}
