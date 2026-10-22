"""early_push_where: push positions on real suite scenes (the target's tokenizer; skipped without it), the off-scene
animal, the answer roles and the pre-registered decision on synthetic cells (no model)."""

import pytest

from scripts import early_push as EP
from scripts import early_push_where as W
from scripts import suite_v1 as S

LAYERS, SCALES = [12, 20], [1.0, 8.0]


@pytest.fixture(scope="module")
def cases():
    from bridge_jspace.tokens import load_tokenizer

    try:
        tok = load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    cfg = {**W.DEFAULTS, "n": 6, "countries": False}
    return tok, EP.build_cases(tok, cfg)


def test_positions_decode_to_the_owner_sentence_and_the_bridge(cases):
    tok, cs = cases
    assert {c["family"] for c in cs} == {"BL", "BR", "RL", "RR"}
    for c in cs:
        pos = W.stated_positions(c)
        ids = c["read"]["clean"]
        owner = c["people"][c["pets"].index(c["bridge"])]
        assert tok.decode([ids[i] for i in pos["s"]]).strip() == f"{owner}'s pet is a {c['bridge']}."
        assert tok.decode([ids[i] for i in pos["w"]]).strip() == c["bridge"]
        assert tok.decode([ids[i] for i in pos["c"]]).strip() == c["context"]


def test_scene_families_share_positions(cases):
    """BL, BR, RL, RR on one scene read one context: the same tokens are pushed at s, w and c."""
    _, cs = cases
    by_scene: dict[str, list[dict]] = {}
    for c in cs:
        by_scene.setdefault(c["scene"], []).append(c)
    shared = 0
    for group in by_scene.values():
        ref = W.stated_positions(group[0])
        for c in group[1:]:
            assert W.stated_positions(c) == ref
            shared += 1
    assert shared


def test_offscene_animal_is_outside_the_scene_with_other_legs():
    c = {"pets": ["bee", "cow", "wolf"], "bridge": "cow", "cf_bridge": "bee", "scene": "s1"}
    y = W.offscene_animal(c)
    legs = {a: v[0] for a, v in S.ANIMALS.items()}
    assert y not in c["pets"]
    assert legs[y] not in (legs["cow"], legs["bee"])
    assert W.offscene_animal({**c, "scene": "s1"}) == y


def test_roles():
    cand = {"A": 1, "b": 2, "oc": [3]}
    assert [W.role_of(t, cand, 9) for t in (1, 2, 9, 3, 7)] == ["A", "b", "y", "oc", "other"]
    assert W.role_of(9, cand, None) == "other"


def _cells(rates: dict[tuple, float], n: int = 50) -> tuple[dict, dict]:
    """(family, subset, layer, scale, dir) -> rate of role 'b' (or of 'other' for an off-path change)."""
    cells, scene_of = {}, {}
    for key, rate in rates.items():
        k = round(rate * n)
        role = "other" if key[0].startswith("R") else "b"
        cells[key] = {f"{key[0]}-{i}": (role if i < k else "A") for i in range(n)}
        for i in range(n):
            scene_of[f"{key[0]}-{i}"] = f"scene-{i}"
    return cells, scene_of


def _grid(br: float, bl: float, off: float = 0.0, rnd: float = 0.0) -> dict[tuple, float]:
    rates = {}
    for sub in ("s", "w"):
        for la in LAYERS:
            for sc in SCALES:
                hot = sub == "w" and la == 20 and sc == 8.0
                rates[("BR", sub, la, sc, "lens")] = br if hot else 0.0
                rates[("BL", sub, la, sc, "lens")] = bl if hot else 0.0
                for f in ("RL", "RR"):
                    rates[(f, sub, la, sc, "lens")] = off if hot else 0.0
                for f in ("BR", "BL"):
                    rates[(f, sub, la, sc, "random")] = rnd
    return rates


@pytest.mark.parametrize(("br", "bl", "off", "rnd", "starts"), [
    (0.6, 0.02, 0.0, 0.0, "H-around"),
    (0.6, 0.6, 0.0, 0.0, "H-where"),
    (0.6, 0.2, 0.0, 0.0, "inconclusive"),
    (0.6, 0.02, 0.3, 0.0, "not valid"),
    (0.1, 0.0, 0.0, 0.0, "no cell"),
    (0.6, 0.0, 0.0, 0.2, "no cell"),  # the random push switches BR too: no cell selected
])  # fmt: skip
def test_decide(br, bl, off, rnd, starts):
    cells, scene_of = _cells(_grid(br, bl, off, rnd))
    d = W.decide(cells, scene_of, LAYERS, SCALES)
    assert d["verdict"].startswith(starts), d["verdict"]
    if d["primary"]:
        assert (d["primary"]["subset"], d["primary"]["layer"], d["primary"]["scale"]) == ("w", 20, 8.0)


def test_rule_v2_skips_a_higher_cell_that_moves_answers_off_the_path():
    rates = _grid(0.9, 0.02, off=0.3)  # w 20 8x: BR 90%, but RL and RR changed 30%
    rates |= {("BR", "s", 20, 1.0, "lens"): 0.6, ("BL", "s", 20, 1.0, "lens"): 0.02}  # valid, lower
    cells, scene_of = _cells(rates)
    v1 = W.decide(cells, scene_of, LAYERS, SCALES, "v1")
    assert v1["verdict"].startswith("not valid") and v1["primary"]["subset"] == "w"
    v2 = W.decide(cells, scene_of, LAYERS, SCALES, "v2")
    assert v2["verdict"].startswith("H-around"), v2["verdict"]
    assert (v2["primary"]["subset"], v2["primary"]["layer"], v2["primary"]["scale"]) == ("s", 20, 1.0)
    assert v2["valid"] and len(v2["selected"]) == 1


def test_rule_v21_takes_the_decisive_cell_from_layer_20_on():
    rates = _grid(0.9, 0.2)  # w 20 8x: valid, BL 20%
    rates |= {("BR", "w", 12, 8.0, "lens"): 0.95, ("BL", "w", 12, 8.0, "lens"): 0.25}  # valid, higher, but layer 12
    cells, scene_of = _cells(rates)
    v2 = W.decide(cells, scene_of, LAYERS, SCALES, "v2")
    assert v2["primary"]["layer"] == 12
    v21 = W.decide(cells, scene_of, LAYERS, SCALES, "v2.1")
    assert (v21["primary"]["subset"], v21["primary"]["layer"], v21["primary"]["scale"]) == ("w", 20, 8.0)
    assert v21["below_v21"] == [{"subset": "w", "layer": 12, "scale": 8.0, "br": 0.96, "bl": 0.24}]
    assert v21["verdict"].startswith("inconclusive")


def test_rule_v2_without_a_valid_cell():
    cells, scene_of = _cells(_grid(0.9, 0.02, off=0.3))
    d = W.decide(cells, scene_of, LAYERS, SCALES, "v2")
    assert d["primary"] is None and d["verdict"].startswith("no valid cell")


def test_fresh_scenes_draw():
    eligible = {"BL": {"a", "b", "c", "d", "e"}, "BR": {"a", "b", "c", "d"}, "RL": {"b", "c", "d", "z"}}
    got = W.fresh_scenes(eligible, used={"c"}, n=10)
    assert sorted(got) == ["b", "d"]  # in every family, not used; n capped at the pool
    assert W.fresh_scenes(eligible, set(), 2) == W.fresh_scenes(eligible, set(), 2)  # seeded
    assert len(W.fresh_scenes(eligible, set(), 2)) == 2
