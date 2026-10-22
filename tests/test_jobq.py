"""The job queue (scripts/jobq.py): spec checks, the worker end to end on a throwaway repo (no GPU, no ssh), and the
job pages (bridge_jspace.job_pages)."""

import json
import subprocess
from pathlib import Path

import pytest

from bridge_jspace import job_pages
from scripts import jobq


def spec(**over):
    s = {
        "id": "t_ok_v1",
        "thread": "D2",
        "command": "python3 write.py",
        "gpus": 1,
        "est_gpu_hours": 0.1,
        "question": "Does the toy job write its result?",
        "why_it_matters": "It tests the queue.",
        "hypotheses": {"H-works": "summary.json exists", "H-broken": "no file"},
        "decision_rule": "works if summary.json exists",
        "controls": ["none: a test"],
        "n": 1,
        "seeds": [0],
        "mem_gb": 0,
    }
    s.update(over)
    return s


def test_validate_accepts_a_full_spec_and_names_each_problem():
    assert jobq.validate(spec(), Path("jobs/d2/t_ok_v1.yaml")) == []
    errors = jobq.validate(spec(id="Bad-Id", hypotheses={}, gpus=2, typo=1), Path("jobs/d2/x.yaml"))
    joined = " | ".join(errors)
    for needle in ("id 'Bad-Id'", "'hypotheses' is empty", "single-GPU", "unknown key 'typo'", "<id>.yaml"):
        assert needle in joined
    no_rule = spec()
    del no_rule["decision_rule"]
    assert jobq.validate(no_rule) == ["missing 'decision_rule'"]
    assert jobq.validate(spec(gpus=True)) == ["'gpus' must be int"]


def test_draft_row_leaves_result_and_verdict_to_a_human():
    rec = {**spec(), "commit": "abcdef1234", "ended_at": "2026-10-21T03:00:00+00:00", "run_s": 5400, "wall_s": 5600}
    row = jobq.draft_row({**rec, "new_results": ["attn_knockout/t_ok_v1"], "wandb": [], "exit_code": 0})
    cols = row.split(" | ")
    assert cols[0] == "2026-10-21" and len(cols) == 6
    assert "abcdef1" in cols[1] and "run 1h30m" in cols[1] and "results/attn_knockout/t_ok_v1" in cols[1]
    assert cols[2] == rec["question"] and cols[-1].startswith("UNVERIFIED")


@pytest.fixture
def box(tmp_path, monkeypatch):
    """A bare repo holding one commit whose write.py makes results/toy/<arg>/summary.json, and a queue root."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "write.py").write_text(
        "import json, pathlib, sys\n"
        "name = sys.argv[1] if len(sys.argv) > 1 else 't_ok_v1'\n"
        "d = pathlib.Path('results/toy') / name\n"
        "d.mkdir(parents=True)\n"
        "(d / 'summary.json').write_text(json.dumps({'ok': True}))\n"
        "print('50%|#####     | 1/2 [00:01<00:01, ETA 1s]')\n"
    )
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", str(src)]
    subprocess.run([*git, "init", "-q"], check=True)
    subprocess.run([*git, "add", "."], check=True)
    subprocess.run([*git, "commit", "-qm", "toy"], check=True)
    commit = subprocess.run([*git, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    root = tmp_path / "jobq"
    jobq.ensure_layout(root)
    subprocess.run([*git, "push", "-q", str(root / "repo.git"), f"{commit}:refs/jobq/toy"], check=True)
    main = tmp_path / "main"
    main.mkdir()
    monkeypatch.setenv("JOBQ_MAIN", str(main))
    monkeypatch.setattr(jobq, "gpu_query", lambda gpu, field: None)  # no nvidia-smi here

    def enqueue(order: int, **over):
        rec = {**spec(**over), "commit": commit, "spec_path": "jobs/x.yaml", "enqueued_at": jobq.now()}
        (root / "pending" / f"20261020-0000{order:02d}-00_{rec['id']}.json").write_text(json.dumps(rec))

    return root, enqueue


def test_worker_runs_a_job_records_timing_and_keeps_its_results(box):
    root, enqueue = box
    enqueue(1)
    jobq.worker(0, root, once=True, check_mem=False)
    [rec] = jobq.read_ledger(root)
    assert rec["status"] == "done" and rec["exit_code"] == 0
    assert rec["new_results"] == ["toy/t_ok_v1"]
    assert rec["run_s"] is not None and rec["wall_s"] >= rec["run_s"]
    assert json.loads((root / "results/toy/t_ok_v1/summary.json").read_text()) == {"ok": True}
    assert (root / "drafts/t_ok_v1.md").read_text().startswith(rec["ended_at"][:10])
    assert [p.name.endswith("t_ok_v1.json") for p in jobq.jobs_in(root, "done")] == [True]
    assert not (root / "runs/t_ok_v1/code").exists()  # checkout removed, log kept
    assert "ETA" in jobq.last_progress(root / "runs/t_ok_v1/log.txt")


def test_a_failing_job_is_failed_and_its_dependents_stay_blocked(box):
    root, enqueue = box
    enqueue(1, id="t_fail_v1", command="python3 -c 'raise SystemExit(3)'")
    enqueue(2, id="t_dep_v1", command="python3 write.py t_dep_v1", depends_on=["t_fail_v1"])
    jobq.worker(0, root, once=True, check_mem=False)
    [rec] = jobq.read_ledger(root)
    assert (rec["id"], rec["status"], rec["exit_code"]) == ("t_fail_v1", "failed", 3)
    path, why = jobq.pick(root, 0, check_mem=False)
    assert path is None and "dependency failed" in why


def test_archive_clears_finished_jobs_from_the_listing_and_keeps_dependencies(box):
    root, enqueue = box
    enqueue(1)
    jobq.worker(0, root, once=True, check_mem=False)
    enqueue(2, id="t_dep_v1", command="python3 write.py t_dep_v1", depends_on=["t_ok_v1"])
    assert "DONE" in jobq.box_status(root)
    assert jobq.box_archive(root).startswith("archived 1 done, 0 failed, 0 cancelled")
    listing = jobq.box_status(root)
    assert "DONE" not in listing and "PENDING  t_dep_v1" in listing
    assert len(list((root / "archive" / "done").glob("*t_ok_v1.json"))) == 1
    path, _ = jobq.pick(root, 0, check_mem=False)  # the dependency is read from the ledger, not done/
    assert path is not None and path.name.endswith("t_dep_v1.json")


def test_dependencies_run_in_order_and_see_earlier_results(box):
    root, enqueue = box
    enqueue(1, id="t_dep_v1", command="test -f results/toy/t_ok_v1/summary.json", depends_on=["t_ok_v1"])
    enqueue(2)
    first, _ = jobq.pick(root, 0, check_mem=False)
    assert first is not None and first.name.endswith("t_ok_v1.json")  # the dependent one waits
    jobq.worker(0, root, once=True, check_mem=False)
    jobq.worker(0, root, once=True, check_mem=False)
    assert [(r["id"], r["status"]) for r in jobq.read_ledger(root)] == [("t_ok_v1", "done"), ("t_dep_v1", "done")]


def test_claim_is_exclusive(box):
    root, enqueue = box
    enqueue(1)
    [path] = jobq.jobs_in(root, "pending")
    assert jobq.claim(path, root) is not None
    assert jobq.claim(path, root) is None


def test_job_page_shows_preregistration_timing_and_examples(tmp_path):
    rec = {
        **spec(),
        "status": "done",
        "commit": "abcdef1234",
        "run_s": 120.0,
        "new_results": ["toy/t_ok_v1"],
        "log": "runs/t_ok_v1/log.txt",
    }
    (tmp_path / "results/jobq").mkdir(parents=True)
    (tmp_path / "results/jobq/ledger.jsonl").write_text(json.dumps(rec) + "\n")
    prompt = "Jack's pet is a cow. Which locker belongs to Jack's pet?"
    ex = {
        "exp": "toy",
        "run": "t_ok_v1",
        "groups": [{"key": "flip", "title": "Flipped", "definition": "the answer changed", "n_total": 7}],
        "examples": [
            {
                "group": "flip",
                "family": "BL",
                "item_id": "bl_001",
                "prompt": prompt,
                "spans": [{"start": 0, "end": 20, "role": "source span"}, {"start": 21, "end": 56, "role": "dest"}],
                "condition": "block dest -> source at layers 32-40",
                "answers": {"clean": "5", "edited": "7", "expected": {"H-works": "7", "H-broken": "5"}},
                "numbers": {"dlogp": -3.2},
                "why": "flipped",
            }
        ],
    }
    (tmp_path / "results/toy/t_ok_v1").mkdir(parents=True)
    (tmp_path / "results/toy/t_ok_v1/examples.json").write_text(json.dumps(ex))
    [out] = job_pages.export_jobs(tmp_path / "examples", repo=tmp_path)
    page = (out / "index.html").read_text()
    for needle in (
        "summary.json exists",
        "works if summary.json exists",
        "UNVERIFIED",
        "2m (estimate 0.1 GPU-h)",
        "Flipped",
        "title='source span'",
        "class='hit'>7",
    ):
        assert needle in page
    entry = json.loads((out / "source.json").read_text())["entry"]
    assert entry["n_examples"] == 1 and "done" in entry["meta"]
    assert "No figures yet" in page
    assert "prompt → prompt · bl_001" in page and ">BL ·" not in page  # family shown by its plain name
    assert entry["title"].startswith("t_ok_v1: ")  # no title anywhere: the id and the question

    (tmp_path / "jobs").mkdir()
    (tmp_path / "jobs/titles.yaml").write_text('t_ok_v1: "Toy run: does the queue work?"\n')
    [out] = job_pages.export_jobs(tmp_path / "examples", repo=tmp_path)
    page = (out / "index.html").read_text()
    assert "<h1>Toy run: does the queue work?" in page and "<title>Toy run: does the queue work?</title>" in page
    assert json.loads((out / "source.json").read_text())["entry"]["title"] == "Toy run: does the queue work?"


def test_job_page_shows_the_newest_analysis_figures(tmp_path):
    rec = {**spec(), "status": "done", "commit": "abcdef1234", "new_results": ["toy/t_ok_v1"]}
    (tmp_path / "results/jobq").mkdir(parents=True)
    (tmp_path / "results/jobq/ledger.jsonl").write_text(json.dumps(rec) + "\n")
    run = tmp_path / "results/toy/t_ok_v1"
    for stamp, names in (
        ("analysis-20261021-090000-figures", ["old.png"]),
        ("analysis-20261021-120000-figures", ["b_rates.png", "a_headline.png"]),
    ):
        (run / stamp).mkdir(parents=True)
        for n in names:
            (run / stamp / n).write_bytes(b"\x89PNG\r\n")
    (run / "analysis-20261021-130000").mkdir()  # newer, but no figures: skipped
    [out] = job_pages.export_jobs(tmp_path / "examples", repo=tmp_path)
    page = (out / "index.html").read_text()
    assert "src='figures/00_a_headline.png'" in page and "src='figures/01_b_rates.png'" in page
    assert "old.png" not in page
    assert (out / "figures/00_a_headline.png").read_bytes() == b"\x89PNG\r\n"
