"""early_push_where: push positions on real suite scenes (the target's tokenizer; skipped without it), the off-scene
animal, the answer roles and the pre-registered decision on synthetic cells (no model)."""

import json
import math

import pytest
import torch

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


def _gap_cells(lens: dict, patch: dict, rnd: float = 0.0) -> dict:
    rates = {}
    for la in lens:
        rates[("BL", "w", la, 4.0, "lens")] = lens[la]
        rates[("BL", "w", la, 8.0, "lens")] = lens[la]
        rates[("BL", "w", la, 0.0, "patch")] = patch[la]
        rates[("BL", "w", la, 8.0, "random")] = rnd
    return _cells(rates, n=100)[0]


GRID = [12, 14, 16, 18, 20, 22, 24, 26, 28, 30]


@pytest.mark.parametrize(("lens_until", "patch_until", "rnd", "starts"), [
    (18, 28, 0.0, "H-gap"),  # lens stops at 20, patch at 30: a gap of 10 layers
    (18, 20, 0.0, "H-no-gap"),  # both stop at 20-22
    (18, 22, 0.0, "inconclusive"),  # a gap of 4 layers
    (18, 28, 0.2, "not valid"),  # the random push moves lookups too
])  # fmt: skip
def test_layer_gap(lens_until, patch_until, rnd, starts):
    lens = {la: 0.3 if la <= lens_until else 0.0 for la in GRID}
    patch = {la: 0.6 if la <= patch_until else 0.0 for la in GRID}
    g = W.layer_gap(_gap_cells(lens, patch, rnd), GRID)
    assert g["verdict"].startswith(starts), g
    assert g["lens_stop"] == lens_until + 2


def test_stop_layer_needs_every_later_layer_low():
    assert W.stop_layer({12: 0.0, 14: 0.3, 16: 0.0}) == 16
    assert W.stop_layer({12: 0.3, 14: 0.3}) is None


def _embed_cells(lens: float, embed: float, at20: float = 0.0) -> dict:
    rates = {}
    for la in (16, 18, 20):
        for sc in (4.0, 8.0):
            rates[("BL", "w", la, sc, "lens")] = lens if la < 20 else at20
            rates[("BL", "w", la, sc, "embed")] = embed if la < 20 else at20
    return _cells(rates, n=100)[0]


@pytest.mark.parametrize(("lens", "embed", "at20", "starts"), [
    (0.4, 0.05, 0.0, "H_lens"),
    (0.3, 0.3, 0.0, "H_input"),
    (0.3, 0.3, 0.2, "inconclusive"),  # the embedding push still moves lookups at 20
    (0.0, 0.0, 0.0, "no lead"),
])  # fmt: skip
def test_embed_test(lens, embed, at20, starts):
    bridge_of = {f"BL-{i}": f"e{i % 10}" for i in range(100)}
    out = W.embed_test(_embed_cells(lens, embed, at20), bridge_of, [4.0, 8.0])
    assert out["verdict"].startswith(starts), out
    assert len(out["valid_cells"]) == 4


def _gap_v2_cells(lens_until: int, patch_until: int, embed_until: int, rnd: float = 0.0) -> dict:
    rates = {}
    for la in GRID:
        for sc in (4.0, 8.0):
            rates[("BL", "w", la, sc, "lens")] = 0.3 if la <= lens_until else 0.0
            rates[("BL", "w", la, sc, "embed")] = 0.3 if la <= embed_until else 0.0
        rates[("BL", "w", la, 0.0, "patch")] = 0.6 if la <= patch_until else 0.0
        rates[("BL", "w", la, 8.0, "random")] = rnd
        rates[("BL", "w", la, 4.0, "random")] = rnd
    return _cells(rates, n=100)[0]


@pytest.mark.parametrize(("lens_until", "patch_until", "starts"), [
    (18, 28, "H-gap"), (18, 20, "H-no-gap"), (18, 22, "inconclusive")])  # fmt: skip
def test_layer_gap_v2(lens_until, patch_until, starts):
    g = W.layer_gap_v2(_gap_v2_cells(lens_until, patch_until, 16), GRID)
    assert g["verdict"].startswith(starts), g
    assert g["lens"]["stop"] == lens_until + 2 and g["embed"]["stop"] == 18


def test_layer_gap_v2_needs_valid_cells():
    g = W.layer_gap_v2(_gap_v2_cells(18, 28, 16, rnd=0.2), GRID)  # the random push moves lookups: no valid cell
    assert g["verdict"].startswith("inconclusive") and g["lens"]["stop"] is None


# ---- the dose control and the layer-16 split (23 Oct) ----------------------------------------------------------------


def test_at_norm_keeps_the_patch_direction_at_the_lens_push_norm():
    g = torch.Generator().manual_seed(0)
    delta = torch.randn(4, 16, generator=g)
    delta[:2] = 0  # the sentence's tokens before the bridge's word: the patch is zero there (causality)
    norms = torch.full((4,), 8 * 2.5)  # the lens push: 8x a reference norm at every pushed position
    push = W.at_norm(delta, norms)
    assert math.isclose(float(push.norm()), float(norms.norm()), rel_tol=1e-5)  # the lens push's total norm
    assert math.isclose(float(torch.nn.functional.cosine_similarity(push.flatten(), delta.flatten(), dim=0)), 1.0, rel_tol=1e-5)  # fmt: skip
    assert not push[:2].any()  # no change where the patch has none
    word = torch.randn(1, 16, generator=g)  # one token (the word): exactly the lens push's norm there
    assert math.isclose(float(W.at_norm(word, torch.tensor([20.0])).norm()), 20.0, rel_tol=1e-5)
    with pytest.raises(AssertionError):
        W.at_norm(torch.zeros(1, 16), torch.tensor([20.0]))


def _split_inputs(d: int = 256):
    g = torch.Generator().manual_seed(1)
    dictionary = torch.nn.functional.normalize(torch.randn(512, d, generator=g), dim=-1)
    sparse = 3.0 * dictionary[5] - 2.0 * dictionary[9]  # inside the dictionary's span with 2 atoms
    delta = torch.stack([sparse, torch.randn(d, generator=g), torch.zeros(d)])
    return dictionary, delta, sparse


def test_split_patch_parts_add_up_and_find_a_sparse_patch():
    dictionary, delta, sparse = _split_inputs()
    pair = dictionary[:2]
    basis = W.SP.random_basis(delta.shape[1], torch.Generator().manual_seed(W.SP.SUBSPACE_SEED + 16))
    parts = W.split_patch(delta, dictionary, pair, basis, k=4)
    assert set(parts) == set(W.SPLIT_PARTS)
    for a, b in (("jspace", "not_jspace"), ("lens2", "not_lens2")):
        assert torch.allclose(parts[a] + parts[b], delta, atol=1e-5)
    assert torch.allclose(parts["jspace"][0], sparse, atol=1e-4)  # OMP recovers a 2-atom row with 4 atoms
    assert torch.allclose(parts["not_lens2"] @ pair.T, torch.zeros(3, 2), atol=1e-4)  # orthogonal to the pair
    for p in ("jspace", "lens2", "rand_sub"):
        assert not parts[p][2].any()  # a zero row stays zero


def test_split_patch_rand_sub_keeps_the_jspace_share_in_random_directions():
    """rand_sub is statement_positions' random_subspace_part: per row a projection (the rest is orthogonal to it) that
    keeps the J-space part's share of the row's squared norm, to within one basis direction's contribution."""
    dictionary, delta, _ = _split_inputs()
    d = delta.shape[1]
    basis = W.SP.random_basis(d, torch.Generator().manual_seed(W.SP.SUBSPACE_SEED + 16))
    parts = W.split_patch(delta, dictionary, dictionary[:2], basis, k=25)
    rs, rows = parts["rand_sub"], delta[:2]
    rs_share = rs[:2].norm(dim=-1) ** 2 / rows.norm(dim=-1) ** 2
    j_share = parts["jspace"][:2].norm(dim=-1) ** 2 / rows.norm(dim=-1) ** 2
    one_direction = ((rows @ basis) ** 2).max(dim=-1).values / rows.norm(dim=-1) ** 2
    assert torch.all((rs_share - j_share).abs() <= one_direction + 1e-5)
    assert torch.allclose(((rows - rs[:2]) * rs[:2]).sum(dim=-1), torch.zeros(2), atol=1e-3)  # a projection
    assert float(torch.nn.functional.cosine_similarity(rs[1], parts["jspace"][1], dim=0)) < 0.9  # other directions
    again = W.split_patch(delta, dictionary, dictionary[:2], W.SP.random_basis(d, torch.Generator().manual_seed(W.SP.SUBSPACE_SEED + 16)), k=25)  # fmt: skip
    assert torch.equal(again["rand_sub"], rs)  # seeded


def test_above_compares_wilson_intervals():
    assert W.above((0.4, 0.3, 0.5), (0.05, 0.02, 0.1)) == "above"
    assert W.above((0.05, 0.02, 0.1), (0.4, 0.3, 0.5)) == "below"
    assert W.above((0.2, 0.1, 0.3), (0.25, 0.15, 0.35)) == "overlap"
    assert W.above((math.nan, math.nan, math.nan), (0.2, 0.1, 0.3)) == "no data"


def _dose_cells(lens_until: int, dir_until: int, off: float = 0.0) -> dict:
    rates = {}
    for la in GRID:
        for sc in (4.0, 8.0):
            rates[("BL", "w", la, sc, "lens")] = 0.3 if la <= lens_until else 0.0
            rates[("BL", "w", la, sc, "patch_dir")] = 0.4 if la <= dir_until else 0.0
            rates[("BL", "w", la, sc, "random")] = 0.0
            for f in ("RL", "RR"):
                rates[(f, "w", la, sc, "patch_dir")] = off
        rates[("BL", "w", la, 0.0, "patch")] = 0.6 if la <= 26 else 0.0
    return _cells(rates, n=100)[0]


@pytest.mark.parametrize(("lens_until", "dir_until", "off", "starts"), [
    (18, 26, 0.0, "H-direction"),  # lens stops at 20, the cut-down patch at 28
    (18, 30, 0.0, "H-direction"),  # the cut-down patch never stops on the grid: after it
    (18, 20, 0.0, "H-dose"),  # it stops at 22
    (18, 14, 0.0, "H-dose"),  # it stops before the lens push
    (18, 22, 0.0, "inconclusive"),  # 4 layers: partly dose
    (18, 26, 0.3, "inconclusive"),  # it moves memory -> prompt / memory -> memory too: no valid cell
])  # fmt: skip
def test_dose_test(lens_until, dir_until, off, starts):
    d = W.dose_test(_dose_cells(lens_until, dir_until, off), GRID)
    assert d["verdict"].startswith(starts), d
    assert d["lens"]["stop"] == 20 and d["patch"]["stop"] == 28


def _split_cells(j: float, rest: float, full: float = 0.85, null: float = 0.0, off: float = 0.0) -> dict:
    rates = {}
    for la in (14, 16, 18):
        parts = (("full", full), ("jspace", j), ("not_jspace", rest), ("lens2", 0.0), ("not_lens2", full), ("rand_sub", 0.0))  # fmt: skip
        for part, r in parts:
            rates[("BL", "w", la, 0.0, f"split_{part}")] = r
            rates[("BL", "w", la, 0.0, f"split_{part}_null")] = null
            rates[("BR", "w", la, 0.0, f"split_{part}")] = 0.6 if part == "jspace" else 0.5  # recalls
            for f in ("RL", "RR"):
                rates[(f, "w", la, 0.0, f"split_{part}")] = off
    return _cells(rates, n=100)[0]


@pytest.mark.parametrize(("j", "rest", "full", "null", "off", "starts"), [
    (0.3, 0.6, 0.85, 0.0, 0.0, "H-lens-part"),
    (0.0, 0.6, 0.85, 0.0, 0.0, "H-rest"),
    (0.03, 0.6, 0.85, 0.0, 0.0, "inconclusive"),  # the J-space part neither moves nor is inert
    (0.0, 0.0, 0.85, 0.0, 0.0, "inconclusive"),  # neither part alone
    (0.3, 0.6, 0.85, 0.2, 0.0, "inconclusive (the J-space part's cell is not valid)"),  # its null moves lookups
    (0.3, 0.6, 0.85, 0.0, 0.3, "inconclusive (the J-space part's cell is not valid)"),  # off the path
    (0.3, 0.6, 0.02, 0.0, 0.0, "not interpretable"),  # the whole patch does not move lookups
])  # fmt: skip
def test_split_test(j, rest, full, null, off, starts):
    t = W.split_test(_split_cells(j, rest, full, null, off), [14, 16, 18])
    assert t["verdict"].startswith(starts), t
    assert set(t["cells"][16]) == set(W.SPLIT_PARTS)
    assert t["cells"][16]["jspace"]["recalls"][0] == 0.6


def test_split_test_reports_rand_sub_without_changing_the_verdict():
    t = W.split_test(_split_cells(0.3, 0.6), [14, 16, 18])  # rand_sub moves no lookup, half the recalls
    assert t["verdict"].startswith("H-lens-part")
    assert t["jspace_vs_rand_sub"] == {"lookups": "above", "recalls": "overlap"}
    cells = _split_cells(0.3, 0.6)
    cells[("BL", "w", 16, 0.0, "split_rand_sub")] = cells[("BL", "w", 16, 0.0, "split_jspace")]  # as the lens part
    t = W.split_test(cells, [14, 16, 18])
    assert t["verdict"].startswith("H-lens-part") and t["jspace_vs_rand_sub"]["lookups"] == "overlap"


def test_agreement_counts_shared_items_per_arm():
    a = {("BL", "w", 16, 8.0, "lens"): {"i1": "b", "i2": "A"}, ("BL", "w", 16, 0.0, "patch"): {"i1": "b"}}
    b = {("BL", "w", 16, 8.0, "lens"): {"i1": "b", "i2": "b", "i3": "A"}, ("BL", "w", 18, 0.0, "patch"): {"i1": "b"}}
    assert W.agreement(a, b) == {"lens": [1, 2]}


# ---- end to end on a synthetic run folder: analyze and figures (no model) ---------------------------------------------


def _write_run(d, cfg: dict, rates: dict, n: int = 100) -> None:
    d.mkdir(parents=True)
    rows = [{"family": f, "name": f"{f}-{i}", "scene": f"s{i}", "kind": "none", "role": "A"} for f in cfg["families"] for i in range(n)]  # fmt: skip
    for (f, sub, la, sc, dr), rate in rates.items():
        hit, k = ("other" if f.startswith("R") else "b"), round(rate * n)
        rows += [{"family": f, "name": f"{f}-{i}", "scene": f"s{i}", "kind": "push", "subset": sub, "layer": la,
                  "scale": sc, "dir": dr, "role": hit if i < k else "A"} for i in range(n)]  # fmt: skip
    (d / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (d / "manifest.json").write_text(json.dumps({"config": cfg, "model": {"repo": "Qwen/Qwen3.6-27B", "n_layers": 64}}))
    keys = [f"{la}/{s}" for la in cfg["layers"] for s in ("s", "w")]
    cases = [{"family": f, "name": f"{f}-{i}", "positions": {"w": [8], "s": [3, 4, 5, 6, 7, 8, 9]},
              "ref": {str(la): 2.0 for la in cfg["layers"]}, "patch_norm": {k: 40.0 for k in keys},
              **({"split_share": {k: {p: 0.3 for p in W.SPLIT_PARTS} for k in keys}} if cfg.get("split") else {})}
             for f in cfg["families"] for i in range(n)]  # fmt: skip
    (d / "cases.jsonl").write_text("".join(json.dumps(c) + "\n" for c in cases))


def test_dose_and_split_runs_analyze_and_draw(tmp_path, monkeypatch):
    pytest.importorskip("matplotlib")
    monkeypatch.setattr(W, "RESULTS", tmp_path)
    base = {**W.DEFAULTS, "scales": [4.0, 8.0], "rule": "v2", "subsets": ["s", "w"], "scenes": "fresh"}
    layers = [16, 18, 20, 22, 24, 26, 28, 30]
    rates = {}
    for sub in ("w", "s"):
        for la in layers:
            for sc in (4.0, 8.0):
                rates[("BL", sub, la, sc, "lens")] = 0.3 if la <= 18 else 0.0
                rates[("BL", sub, la, sc, "patch_dir")] = 0.4 if la <= 26 else 0.0
                rates[("BL", sub, la, sc, "random")] = 0.0
                for f in ("BR", "RL", "RR"):
                    rates[(f, sub, la, sc, "lens")] = 0.0
            rates[("BL", sub, la, 0.0, "patch")] = 0.6 if la <= 26 else 0.0
    _write_run(tmp_path / "ref", {**base, "layers": layers}, {k: v for k, v in rates.items() if k[4] != "patch_dir"})
    cfg = {**base, "layers": layers, "patch": True, "gap_rule": "v2", "patch_dir": True, "same_scenes": "ref"}
    _write_run(tmp_path / "dose", cfg, rates)
    W.stage_analyze("dose")
    W.stage_figures("dose")
    s = json.loads((tmp_path / "dose" / "summary.json").read_text())
    assert s["dose_test"]["w"]["verdict"].startswith("H-direction"), s["dose_test"]["w"]
    assert s["layer_gap"]["w"]["verdict"] == "H-gap"
    assert s["replication"]["same_role"]["lens"] == [12800, 12800]  # 4 families x 2 subsets x 8 layers x 2 scales x 100
    assert s["scene_patch"]["patch_over_1x_lens"]["16/w"] == 20.0  # 40 / (2 x sqrt(1))
    assert "Dose control (w)" in (tmp_path / "dose" / "summary.md").read_text()
    assert list((tmp_path / "dose").glob("analysis-figures-*/dose.png"))

    split_rates = {}
    for sub in ("w", "s"):
        for la in (14, 16, 18):
            parts = (("full", 0.85), ("jspace", 0.3), ("not_jspace", 0.6), ("lens2", 0.1), ("not_lens2", 0.8), ("rand_sub", 0.0))  # fmt: skip
            for part, r in parts:
                split_rates[("BL", sub, la, 0.0, f"split_{part}")] = r
                split_rates[("BL", sub, la, 0.0, f"split_{part}_null")] = 0.0
                split_rates[("BR", sub, la, 0.0, f"split_{part}")] = 0.0 if part == "rand_sub" else 0.7
            for sc in (4.0, 8.0):
                split_rates[("BL", sub, la, sc, "lens")] = 0.19 if sc == 8.0 else 0.0
                split_rates[("BR", sub, la, sc, "lens")] = 0.83 if sc == 8.0 else 0.4
    _write_run(tmp_path / "split", {**base, "layers": [14, 16, 18], "split": True}, split_rates)
    W.stage_analyze("split")
    W.stage_figures("split")
    s = json.loads((tmp_path / "split" / "summary.json").read_text())
    assert s["split_test"]["w"]["verdict"].startswith("H-lens-part"), s["split_test"]["w"]
    assert s["split_test"]["w"]["jspace_vs_rand_sub"] == {"lookups": "above", "recalls": "above"}
    assert "J-space part against rand_sub at layer 16" in (tmp_path / "split" / "summary.md").read_text()
    assert s["scene_patch"]["split_share"]["16/w"]["jspace"] == 0.3
    assert list((tmp_path / "split").glob("analysis-figures-*/split.png"))
