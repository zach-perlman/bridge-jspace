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
