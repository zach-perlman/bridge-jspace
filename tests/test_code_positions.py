"""code_positions (D1 in code): the programs, the position sets, statement_positions configured for the two code
families, and the H-D1-code reading."""

import pytest

from scripts import code_positions as CP
from scripts import statement_positions as SP


def test_items_pair_the_two_readers_on_one_program():
    items = CP.generate()
    assert len(items) == 2 * CP.N_SCENES
    by_scene: dict[str, dict[str, dict]] = {}
    for it in items:
        by_scene.setdefault(it["scene"], {})[it["family"]] = it
    for sc, fams in by_scene.items():
        kl, kr = fams["KL"], fams["KR"]
        assert kl["context"] == kr["context"] and kl["cf_context"] == kr["cf_context"], sc  # one patch, two questions
        assert CP.GROUP_OF[kl["bridge"]] == CP.GROUP_OF[kl["cf_bridge"]]  # token-aligned C
        assert CP.GROUP_OF[kl["spare"]] == CP.GROUP_OF[kl["spare_o"]]  # token-aligned O
        assert kl["answer"] != kl["cf_answer"] and kr["answer"] != kr["cf_answer"]
        assert kr["answer"] == CP.CAPITAL[kr["bridge"]]
        assert kl["cf_context"].replace(f'key = "{kl["cf_bridge"]}"', f'key = "{kl["bridge"]}"') == kl["context"]
        assert kl["off_context"].replace(f'spare = "{kl["spare_o"]}"', f'spare = "{kl["spare"]}"') == kl["context"]
    assert items == CP.generate()  # seeded


def test_judge(monkeypatch):
    monkeypatch.setattr(CP.S, "said", CP.said)  # what competence does: the digit branch must not call itself
    assert CP.said(" 7\n", "digit") == "7"
    assert CP.said(" Tokyo.", "word") == "Tokyo"
    assert CP.said(" The value is Japan", "country") == "Japan"
    assert CP.capital_judge(" Lima") == "Lima"


@pytest.fixture(scope="module")
def tok():
    from scripts import pointer_v1 as PV

    try:
        return PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")


def test_position_sets_and_alignment(tok, monkeypatch):
    if not CP.ITEMS.exists():
        pytest.skip("no data/code_positions_v1/items.json")
    monkeypatch.setattr(CP, "COMPETENCE", "none")
    cases, counts = CP.build_cases(tok, 6, list(CP.FAMILIES))
    assert counts["code"]["unaligned_skipped"] == 0 and len(cases) == 12
    for c in cases:
        ids = c["ids"]["clean"]
        assert tok.decode([ids[i] for i in c["sets"]["bind_bridge"]]).strip() == f'key = "{c["bridge"]}"'
        assert c["bridge"] in tok.decode([ids[i] for i in c["sets"]["bridge_word"]])
        assert set(c["changed"]["cf"]) <= set(c["sets"]["bridge_word"])
        assert max(c["sets"]["lookup_bridge"]) < min(c["changed"]["cf"])  # a paste there is an exact no-op
    kl = [c for c in cases if c["family"] == "KL"]
    kr = [c for c in cases if c["family"] == "KR"]
    for a, b in zip(kl, kr, strict=True):  # same program, same statement positions: one patch for both readers
        assert a["sets"]["bind_bridge"] == b["sets"]["bind_bridge"] and a["sets"]["context"] == b["sets"]["context"]


def test_configure_points_statement_positions_at_the_code_families(monkeypatch):
    for name in ("EXP", "RESULTS", "FAMILIES", "SUITE", "COUNTRIES", "C", "CUE_ONLY", "BOUND", "LOOKUP_USED_BOUND",
                 "POSITIVE", "PAIRS", "build_cases", "manifest_common"):  # fmt: skip
        monkeypatch.setattr(SP, name, getattr(SP, name))  # restored after the test
    CP.configure()
    assert SP.LOOKUP_USED_BOUND == ("KL",) and SP.POSITIVE == ("KR",) and SP.PAIRS == (("KL", "KR"),)
    assert SP.build_cases is CP.build_cases and SP.RESULTS == CP.RESULTS
    assert SP.C.judge(" Paris") == "Paris"


def write_run(root, name: str, manifest: dict, summary: dict) -> None:
    import json

    (root / name).mkdir(parents=True)
    (root / name / "manifest.json").write_text(json.dumps(manifest))
    (root / name / "summary.json").write_text(json.dumps(summary))


def test_figures_and_report_from_three_runs(tmp_path, monkeypatch):
    for name in ("EXP", "RESULTS", "FAMILIES", "SUITE", "COUNTRIES", "C", "CUE_ONLY", "BOUND", "LOOKUP_USED_BOUND",
                 "POSITIVE", "PAIRS", "build_cases", "manifest_common"):  # fmt: skip
        monkeypatch.setattr(SP, name, getattr(SP, name))
    monkeypatch.setattr(CP, "RESULTS", tmp_path)
    model = {"repo": "Qwen/Qwen3.6-27B"}
    layers = [28, 32, 36]
    rate = {"flips": [0.6, 0.5, 0.7], "changed": [0.6, 0.5, 0.7], "zero": 0, "frac": 0.5}
    ctrl = {"flips": [0.0, 0.0, 0.05], "changed": [0.0, 0.0, 0.05], "zero": 0, "frac": 0.0}
    rates = [{"family": f, "set": s, "layer": la, "n": 80, "cf": rate, "off": ctrl, "rand": ctrl, "transit": True}
             for f in CP.FAMILIES for s in ("bind_bridge", "context", "bridge_word", "q_words", "final") for la in layers]  # fmt: skip
    transit = {f: {"bind_bridge": [32, 36]} for f in CP.FAMILIES}
    write_run(tmp_path, "m", {"kind": "map", "layers": layers, "model": model},
              {"rates": rates, "transit": transit, "sanity": {}, "counts": {"code": {"n": 80}}})  # fmt: skip
    pc = {"KL/bind_bridge/primary": cell("around"), "KR/bind_bridge/primary": cell("inside", (3, 2, 4))}
    write_run(tmp_path, "p", {"kind": "parts", "map": {"run": "m"}, "model": model}, {"cells": pc, "claims": {}})
    by_scale = {f"x{s:g}": {"lens_flips": 0.0, "random_flips": 0.0, "diff": [0, 0, 0.02]} for s in (0.5, 1, 4)}
    rw_cells = {f"{f}/bind_bridge/primary": {"by_scale": by_scale, "write": {"copy": {"flips": 0.6, "frac": 0.5}},
                                             "verdict": "not written"} for f in CP.FAMILIES}  # fmt: skip
    write_run(tmp_path, "r", {"kind": "readwrite", "map": {"run": "m"}, "parts": {"run": "p"}, "model": model},
              {"cells": rw_cells, "claims": {}})  # fmt: skip
    for name, figs in (("m", 1), ("p", 2), ("r", 3)):
        CP.stage_figures(name)
        folder = next((tmp_path / name).glob("analysis-*-figures"))
        assert len(list(folder.glob("*.png"))) == figs, name
        assert (folder / "report.md").exists()
    assert "**holds**" in (next((tmp_path / "r").glob("analysis-*-figures")) / "report.md").read_text()


def cell(verdict: str, conc=(0.2, 0.1, 0.4)) -> dict:
    return {"verdict": verdict, "frac": {"jspace": {"concentration": list(conc)}}}


def test_h_d1_code_needs_transit_around_and_a_passing_positive_control():
    mp = {"transit": {"KL": {"bind_bridge": [32, 36]}}}
    parts = {"cells": {"KL/bind_bridge/primary": cell("around"), "KR/bind_bridge/primary": cell("inside", (3, 2, 4))}}
    assert CP.h_d1_code(parts, None, mp)["H-D1-code"] == "holds"
    parts["cells"]["KR/bind_bridge/primary"] = cell("inconclusive")
    assert "not interpretable" in CP.h_d1_code(parts, None, mp)["H-D1-code"]
    parts["cells"]["KL/bind_bridge/primary"] = cell("inside", (3, 2, 4))
    assert CP.h_d1_code(parts, None, mp)["H-D1-code"] == "does not hold"
    assert "no key-line cell" in CP.h_d1_code({"cells": {}}, None, {"transit": {}})["H-D1-code"]
