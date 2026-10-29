"""Batch 52 C coverage matrix (scripts/x52_coverage.py): row 4's doses are read from the verdicts (the 9B / Muse values
were once typed swapped), and a coverage cell resolves from what has landed: a verdict naming the run, the run alone, a
failed job in the ledger, or the spec only."""

import json

import pytest

from scripts import x52_coverage as M


def test_row4_doses_read_from_the_verdicts():
    assert (
        M.dose_note("results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md") == "0.02 / 0.46 / 0.73"
    )
    assert M.dose_note("results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md") == "0.05 / 0.52 / 0.52"
    assert M.dose_note("results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md") == "0.01 / 0.24 / 0.50"


@pytest.fixture
def tree(tmp_path, monkeypatch):
    res, jobs = tmp_path / "results", tmp_path / "jobs"
    (res / "jobq").mkdir(parents=True)
    jobs.mkdir()
    (jobs / "spec_a.yaml").write_text("id: spec_a\n")
    monkeypatch.setattr(M, "RES", res)
    monkeypatch.setattr(M, "JOBS", jobs)
    monkeypatch.setattr(M, "rel", lambda p: str(p))
    monkeypatch.setattr(M, "LEDGER", {})
    return res


def test_track_queued_partial_done(tree):
    cell = M.track("spec_a", "exp/run_a", "exp/x52_v-*")
    assert cell["status"] == "queued" and cell["sources"][0].endswith("spec_a.yaml")
    (tree / "exp" / "run_a").mkdir(parents=True)
    (tree / "exp" / "run_a" / "outcomes.jsonl").write_text("")  # landed (a killed job's folder is not)
    assert M.track("spec_a", "exp/run_a", "exp/x52_v-*")["status"] == "partial"
    other = tree / "exp" / "x52_v-20261029T000000Z"
    other.mkdir()
    (other / "v.json").write_text(json.dumps({"runs": ["run_b"]}))
    assert M.track("spec_a", "exp/run_a", "exp/x52_v-*")["status"] == "partial"  # a verdict over another run only
    mine = tree / "exp" / "x52_v-20261029T010000Z"
    mine.mkdir()
    (mine / "v.md").write_text("| nemotron | run_a | tested |")
    cell = M.track("spec_a", "exp/run_a", "exp/x52_v-*", done_as="partial")
    assert cell["status"] == "partial" and cell["sources"][0] == str(mine)
    assert M.track("spec_a", "exp/run_a", "exp/x52_v-*")["status"] == "done"


def test_track_failed_job_and_gate(tree, monkeypatch):
    monkeypatch.setattr(M, "LEDGER", {"spec_a": {"status": "failed", "exit_code": 1, "ledger": "ledger_x.jsonl"}})
    cell = M.track("spec_a", "exp/run_a", "exp/x52_v-*")
    assert cell["status"] == "missing" and "failed (exit 1" in cell["note"]
    run = tree / "exp" / "run_g"
    run.mkdir(parents=True)
    (run / "gate.json").write_text(json.dumps({"pass": False, "eligible": 3}))
    assert M.track("spec_a", "exp/run_g", "exp/{run}/verdict-*", gate_fail=True)["status"] == "not tested"


def test_every_cell_resolves_in_this_checkout():
    rows = M.build()
    assert not M.check_sources()
    assert all(set(cells) == set(M.MODELS) for _, _, cells in rows)
    assert all(cell["status"] in M.STATUS for _, _, cells in rows for cell in cells.values())


def test_audit_downgrades_a_done_cell_whose_verdict_lists_the_model_pending(tree):
    """A fixed 'done' cell is checked against its source: the verdict's row for the column's model pending (its run
    never produced outcomes, as x47_16_muse) -> missing; not tested -> not tested; a run folder with setup files only
    -> missing; tested -> unchanged."""
    v = tree / "exp" / "x47_16-1"
    v.mkdir(parents=True)
    rows = [
        {"target": "qwen3.5-9b", "status": "tested"},
        {"target": "muse-glimmer-30b", "status": "pending", "why": "no run given"},
        {"target": "qwen3.6-27b", "status": "not tested"},
    ]
    (v / "x.json").write_text(json.dumps({"models": rows}))
    cell = M.c("done", "", str(v))
    assert M.audit(cell, "qwen3.5-9b") is cell
    out = M.audit(cell, "muse-glimmer-30b")
    assert out["status"] == "missing" and "pending" in out["note"] and "no run given" in out["note"]
    assert M.audit(cell, "qwen3.6-27b")["status"] == "not tested"
    run = tree / "exp" / "killed"
    run.mkdir()
    for f in ("manifest.json", "cases.jsonl", "competence.jsonl", "gate.json"):
        (run / f).write_text("{}")
    assert not M.landed(run) and M.audit(M.c("done", "", str(run)), "qwen3.5-9b")["status"] == "missing"
    (run / "outcomes.jsonl").write_text("")
    assert M.landed(run)


def test_track_a_killed_run_is_not_landed(tree, monkeypatch):
    """A run folder with setup files only reads 'running' (no outcomes yet), or 'missing' when its job failed."""
    run = tree / "exp" / "run_k"
    run.mkdir(parents=True)
    (run / "manifest.json").write_text("{}")
    assert M.track("spec_a", "exp/run_k", "exp/x52_v-*")["status"] == "running"
    monkeypatch.setattr(M, "LEDGER", {"spec_a": {"status": "failed", "exit_code": 143, "ledger": "l.jsonl"}})
    cell = M.track("spec_a", "exp/run_k", "exp/x52_v-*")
    assert cell["status"] == "missing" and "no outcomes" in cell["note"] and "exit 143" in cell["note"]
