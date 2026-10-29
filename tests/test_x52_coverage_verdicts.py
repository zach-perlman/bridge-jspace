"""Batch 52 C: the coverage verdicts of the scripts whose own verdict lists only the design's models. Each takes its
coverage runs (the 27B's or Lightning's) alone, writes "no prediction" in place of Dan's answer (no seal guard), adds
no pending rows for the design's models, and writes to its own x52_<name>-<UTC>/ folder. Runs not landed read as
pending, so the report path runs without model data."""

import importlib

import pytest

LT, Q27 = "nemotron-3.5-lightning", "qwen3.6-27b"

# script, verdict call (module -> path-less call), the folder stem, the coverage targets the call names
CASES = [
    ("x48_heads", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_heads48", {Q27, LT}),
    ("x48_bind", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_bind", {Q27}),
    ("x49_probe", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_probe49", {Q27}),
    ("x47_source", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_source", {LT}),
    ("x47_value", lambda M: M.stage_verdict("a", list(M.COVERAGE_RUNS["a"].values()), 10, coverage=True),
     "x52_valuea", {LT}),
    ("x47_value", lambda M: M.stage_verdict("c", list(M.COVERAGE_RUNS["c"].values()), 10, coverage=True),
     "x52_valuec", {LT}),
    ("x48_enrich", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS_A.values()), list(M.COVERAGE_RUNS_B.values()), 10,
                                             coverage=True), "x52_enrich", {Q27, LT}),
    ("x49_gain", lambda M: M.stage_verdict(None, 10, coverage=True), "x52_gain", {LT}),
    ("x47_edges", lambda M: M.stage_verdict(None, 10, coverage=True), "x52_edges", {Q27}),
    ("x47_cue", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_cue", {LT}),
    ("x47_report", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_report", {LT}),
    ("x47_agnostic", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_agnostic",
     {Q27, LT}),
    ("x47_chain", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_chain", {Q27, LT}),
    ("x47_distance", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_distance",
     {Q27, LT}),
    ("x47_cumulative", lambda M: M.stage_verdict(list(M.COVERAGE_RUNS.values()), 10, coverage=True), "x52_cumulative",
     {Q27, LT}),
]  # fmt: skip
DESIGN_RUNS_REFUSED = ["x48_heads", "x48_bind", "x49_probe", "x47_source", "x47_cue", "x47_report", "x47_agnostic",
                       "x47_chain", "x47_distance"]  # fmt: skip


@pytest.mark.parametrize(("script", "call", "stem", "targets"), CASES, ids=[c[0] for c in CASES])
def test_coverage_verdict_reads_the_coverage_runs_alone(tmp_path, monkeypatch, script, call, stem, targets):
    M = importlib.import_module(f"scripts.{script}")
    monkeypatch.setattr(M, "RESULTS", tmp_path)
    for name in ("dan_answer", "unsealed", "require_answer"):
        if hasattr(M, name):
            monkeypatch.setattr(M, name, lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    call(M)
    (out,) = [p for p in tmp_path.iterdir() if p.is_dir()]
    assert out.name.startswith(f"{stem}-"), out.name
    text = "\n".join(p.read_text() for p in out.glob("*.md"))
    assert M.NO_PREDICTION in text and ", Dan:" not in text
    named = {t for t in (LT, Q27, "qwen3.5-9b", "muse-glimmer-30b") if f"| {t} " in text or f"## {t}" in text
             or f"{t}:" in text}  # fmt: skip
    assert targets <= named and "qwen3.5-9b" not in named and "muse-glimmer-30b" not in named, named


@pytest.mark.parametrize("script", DESIGN_RUNS_REFUSED)
def test_coverage_verdict_refuses_a_design_run(tmp_path, monkeypatch, script):
    """--coverage reads coverage runs only; a design model's run (the 9B's) is refused."""
    M = importlib.import_module(f"scripts.{script}")
    monkeypatch.setattr(M, "RESULTS", tmp_path)
    with pytest.raises(AssertionError, match="runs on"):
        M.stage_verdict([M.RUNS["qwen3.5-9b"]], 10, coverage=True)


@pytest.mark.parametrize("script", ["x47_cue", "x47_report", "x47_agnostic", "x47_chain", "x47_distance",
                                    "x47_cumulative"])  # fmt: skip
def test_cli_coverage_defaults_to_the_coverage_runs(tmp_path, monkeypatch, script):
    """`verdict --coverage` without --runs reads COVERAGE_RUNS; `verdict` alone still reads the design's RUNS."""
    M = importlib.import_module(f"scripts.{script}")
    seen = []
    monkeypatch.setattr(M, "stage_verdict", lambda runs, n_boot, coverage=False: seen.append((runs, coverage)))
    for argv in (["verdict", "--coverage"], ["verdict"]):
        monkeypatch.setattr("sys.argv", [script, *argv])
        M.main()
    assert seen == [(list(M.COVERAGE_RUNS.values()), True), (list(M.RUNS.values()), False)]


def test_natural_verdict_on_a_gate_failed_run_says_not_tested(tmp_path, monkeypatch):
    """x5_natural: a run that stopped at its gate (no outcomes; Lightning's nem35l_x52_natural) exits with 'not tested'
    and writes no verdict folder (it raised a TypeError on the empty bootstrap before)."""
    import json

    from scripts import x5_natural as N

    run = tmp_path / "r"
    run.mkdir()
    (run / "manifest.json").write_text(json.dumps({"model": {"target": LT}, "layer": 14}))
    (run / "gate.json").write_text(json.dumps({"pass": False, "org_read_accuracy": {"PP": 0.77}, "eligible": 36}))
    monkeypatch.setattr(N, "RESULTS", tmp_path)
    with pytest.raises(SystemExit, match="not tested, no outcomes"):
        N.stage_verdict("r", 10)
    assert sorted(p.name for p in run.iterdir()) == ["gate.json", "manifest.json"]


def test_z3_coverage_verdict_on_the_27b(tmp_path, monkeypatch):
    """Z3 on the 27B (batch 52 C, after the matrix): at L32 (X0's layer, the start of Zach's 27B band L32-40), a
    coverage verdict with no prediction, the 27B's run alone, its own folder."""
    from scripts import x50_zach as Z

    monkeypatch.setattr(Z, "RESULTS", tmp_path / "zach")
    monkeypatch.setattr(Z, "COVERAGE", True)
    assert Z.COVERAGE_RUNS["z3"][Q27] == "x50_z3_27b" and Q27 not in Z.RUNS["z3"] and Z.LAYERS[Q27] == (32,)
    assert Z.BESIDE_BAND[Q27] == "L32-40"
    out = Z.stage_verdict("z3", [Z.COVERAGE_RUNS["z3"][Q27]], 10)
    text = (out / "z3.md").read_text()
    assert out.name.startswith("x52_z3-") and Z.NO_PREDICTION in text and "Dan:" not in text and Q27 in text


def test_lightning_z2_cue_and_value_c_lookups(tmp_path, monkeypatch):
    """Lightning's Z2 (x50_zach), 51.12's cue set (x51_answer, on Lightning's 47.3 run) and 47.7 (c) (x47_value, on
    fill5's 45d basis): lookups only, each read by its coverage verdict."""
    from scripts import x47_value as V
    from scripts import x50_zach as Z
    from scripts import x51_answer as AN

    assert Z.COVERAGE_RUNS["z2"] == {LT: "nem35l_x52_z2"} and LT not in Z.RUNS["z2"] and Z.LAYERS[LT] == (14, 27)
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "zach")
    monkeypatch.setattr(Z, "COVERAGE", True)
    out = Z.stage_verdict("z2", [Z.COVERAGE_RUNS["z2"][LT]], 10)
    text = (out / "z2.md").read_text()
    assert out.name.startswith("x52_z2-") and Z.NO_PREDICTION in text and "Dan:" not in text and LT in text
    assert AN.runs_of("cue")[LT] == "nem35l_x52_cue_answer" and AN.source_of("cue", LT).name == "nem35l_x52_cue"
    assert AN.source_of("cue", Q27).name == "x47_cue_27b"  # the design's sources unchanged
    assert V.PCF_FIT[LT] == "x7_pcf/nem35l_x52_x45d_fit" and Q27 not in V.PCF_FIT
