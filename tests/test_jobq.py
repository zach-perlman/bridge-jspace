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
    for needle in ("id 'Bad-Id'", "'hypotheses' is empty", "BJ_DEVICE_MAP", "unknown key 'typo'", "<id>.yaml"):
        assert needle in joined
    no_rule = spec()
    del no_rule["decision_rule"]
    assert jobq.validate(no_rule) == ["missing 'decision_rule'"]
    assert jobq.validate(spec(gpus=True)) == ["'gpus' must be int"]


def test_validate_multi_gpu_jobs_must_split_the_model():
    split = "BJ_TARGET=qwen3.5-122b-a10b BJ_DEVICE_MAP=auto uv run python x.py"
    assert jobq.validate(spec(gpus=2, command=split)) == []
    assert jobq.validate(spec(gpus=2, command="uv run python x.py")) == [
        "gpus: 2 needs a command that splits the model over them (BJ_DEVICE_MAP=auto)"
    ]
    assert jobq.validate(spec(gpus=0)) == ["'gpus' must be >= 1"]


def test_gpu_list_and_tag():
    assert jobq.gpu_list(0) == [0] and jobq.gpu_list("0,1") == [0, 1] and jobq.gpu_list([2, 3]) == [2, 3]
    assert jobq.gpu_tag([0, 1]) == "0-1" and jobq.gpu_tag([3]) == "3"
    with pytest.raises(ValueError, match="once each"):
        jobq.gpu_list("0,0")


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


def fake_gpus(monkeypatch, free_mib: dict[int, float], used_mib: float = 1024.0, name: str = "NVIDIA H100 PCIe"):
    """nvidia-smi faked per GPU: memory.free, memory.used and the name."""

    def query(gpu, field):
        return {"memory.free": str(free_mib[gpu]), "memory.used": str(used_mib), "name": name}[field]

    monkeypatch.setattr(jobq, "gpu_query", query)


def test_a_two_gpu_job_waits_for_a_worker_with_two_gpus_and_their_total_memory(box, monkeypatch):
    """The 122B in FP8 (~125 GB) on 2x H100 80 GB: mem_gb is the total over the job's GPUs, so 135 fits two idle cards
    (2 x ~79.6 GB free) and never one; a one-GPU worker passes the job over and takes the one-GPU job behind it."""
    root, enqueue = box
    fake_gpus(monkeypatch, {0: 81000.0, 1: 81000.0})
    enqueue(1, id="t_two_v1", gpus=2, mem_gb=135, command="BJ_DEVICE_MAP=auto python3 write.py t_two_v1")
    enqueue(2, id="t_one_v1", gpus=1, mem_gb=70)
    path, _ = jobq.pick(root, [0, 1])
    assert path is not None and path.name.endswith("t_two_v1.json")
    path, why = jobq.pick(root, 0)  # one GPU: the two-GPU job is left to a worker that has two
    assert path is not None and path.name.endswith("t_one_v1.json")
    path, why = jobq.pick(root, [1])
    assert path is not None and path.name.endswith("t_one_v1.json")
    fake_gpus(monkeypatch, {0: 81000.0, 1: 40000.0})  # 118 GB free in total: the head job waits, FIFO holds
    path, why = jobq.pick(root, [0, 1])
    assert path is None and why == "t_two_v1: needs 135 GB free on GPU 0-1, 118 GB free"
    for p in jobq.jobs_in(root, "pending"):
        if p.name.endswith("t_one_v1.json"):
            p.unlink()
    path, why = jobq.pick(root, 0)
    assert path is None and why == "t_two_v1: needs 2 GPUs, a worker on GPU 0 has 1"


def test_a_two_gpu_worker_runs_the_job_on_both_gpus_and_records_them(box, monkeypatch):
    root, enqueue = box
    fake_gpus(monkeypatch, {0: 81000.0, 1: 81000.0}, used_mib=1024.0)
    cmd = "BJ_DEVICE_MAP=auto python3 write.py t_two_v1 && echo $CUDA_VISIBLE_DEVICES > results/toy/t_two_v1/cvd.txt"
    enqueue(1, id="t_two_v1", gpus=2, mem_gb=135, command=cmd)
    jobq.worker([0, 1], root, once=True)
    [rec] = jobq.read_ledger(root)
    assert rec["status"] == "done", rec.get("error")
    assert (rec["gpu"], rec["gpu_ids"], rec["gpu_name"]) == (0, [0, 1], "2x NVIDIA H100 PCIe")
    assert rec["baseline_mem_gb"] == 2.0  # 1 GB on each of the two
    assert (root / "results/toy/t_two_v1/cvd.txt").read_text().strip() == "0,1"
    enqueue(2, id="t_one_v1", gpus=1, mem_gb=70, command="python3 write.py t_one_v1 && echo $CUDA_VISIBLE_DEVICES > "
            "results/toy/t_one_v1/cvd.txt")  # fmt: skip
    jobq.worker([0, 1], root, once=True)  # a one-GPU job on a two-GPU worker gets its first GPU only
    assert jobq.read_ledger(root)[-1]["gpu_ids"] == [0]
    assert (root / "results/toy/t_one_v1/cvd.txt").read_text().strip() == "0"


def test_mem_sampler_peaks_are_the_total_and_per_gpu(monkeypatch):
    used = {0: "30000", 1: "50000"}
    monkeypatch.setattr(jobq, "gpu_query", lambda gpu, field: used[gpu])
    s = jobq.MemSampler([0, 1])
    s.sample()
    used[0], used[1] = "70000", "10000"
    s.sample()
    assert s.stop() == round(80000 / 1024, 1)  # the peak of the total (both samples total 80000 MiB)
    assert s.per_gpu() == [round(70000 / 1024, 1), round(50000 / 1024, 1)]


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


def test_schedule_respects_dependencies_and_gpus():
    from scripts import jobq as Q

    pend = [{"id": "a", "est_gpu_hours": 2.0}, {"id": "b", "est_gpu_hours": 1.0, "depends_on": ["a"]},
            {"id": "c", "est_gpu_hours": 1.0}]  # fmt: skip
    assert Q.schedule([], pend, set(), 2) == 3.0  # a then b on one GPU, c on the other
    assert Q.schedule([0.5], pend[2:], set(), 1) == 1.5  # c waits for the running job
    assert Q.schedule([], [{"id": "x", "est_gpu_hours": 1.0, "depends_on": ["gone"]}], set(), 2) == 0.0


def test_timeline_lets_pending_jobs_wait_for_a_running_one():
    """28 Oct: a pending job whose dependency was running counted as unschedulable, so the drain time was too short."""
    from scripts import jobq as Q

    pend = [{"id": "p2", "est_gpu_hours": 0.5, "depends_on": ["p1"]}, {"id": "z", "est_gpu_hours": 1.0},
            {"id": "x", "est_gpu_hours": 1.0, "depends_on": ["gone"]}]  # fmt: skip
    spans, drain, stuck = Q.timeline([2.0], pend, set(), 2, ["p1"])
    assert spans["p1"] == (0.0, 2.0) and spans["z"] == (0.0, 1.0)  # z takes the free GPU at once
    assert spans["p2"] == (2.0, 2.5)  # p2 starts when p1 ends
    assert drain == 2.5 and stuck == ["x"]


# ---------------------------------------------------------------- enqueue: run names are written once


@pytest.fixture
def mac(tmp_path, monkeypatch):
    """cmd_enqueue with git, the box (ssh, scp, push) and the other boxes' ids faked: no network. Returns a spec
    writer, the box's results/ listing ('<exp>/<run>') and the calls made."""
    calls: dict = {"ssh": [], "push": 0}
    box_runs: list[str] = []

    def ssh(cmd, stdin=None):
        calls["ssh"].append(cmd)
        return "[]" if "box-ids" in cmd else json.dumps(box_runs) if "box-runs" in cmd else ""

    def run(cmd, **kw):
        assert cmd[:2] == ["git", "push"], cmd
        calls["push"] += 1
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(jobq, "REPO", tmp_path)
    monkeypatch.setattr(jobq, "_git", lambda *a: "")
    monkeypatch.setattr(jobq, "_install_box_script", lambda: None)
    monkeypatch.setattr(jobq, "_ssh", ssh)
    monkeypatch.setattr(jobq, "ids_on_other_boxes", lambda repo, host: set())
    monkeypatch.setattr(jobq.subprocess, "run", run)

    def write(job_id: str, command: str) -> Path:
        p = tmp_path / "jobs" / "d1" / f"{job_id}.yaml"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(spec(id=job_id, command=command)))
        return p

    return write, box_runs, calls


def test_enqueue_refuses_a_run_name_already_in_the_box_results(mac):
    """Gemma's _r2 retries reused the run names whose partial results the first attempt had left on the box."""
    write, box_runs, calls = mac
    box_runs += ["tasks_v2/g_competence", "statement_positions/g_map", "statement_positions/other"]
    retry = ("python3 tasks_v2.py competence --name g_competence && python3 sp.py map --name g_smoke_r2 && "
             "python3 sp.py map --name g_map")  # fmt: skip
    paths = [write("g_map_r2", retry), write("g_parts_r2", "python3 sp.py parts --name g_parts --map g_map")]
    with pytest.raises(SystemExit) as e:
        jobq.cmd_enqueue(paths)
    msg = str(e.value)
    assert "g_map_r2: --name g_competence exists on the box: results/tasks_v2/g_competence" in msg
    assert "g_map_r2: --name g_map exists on the box: results/statement_positions/g_map" in msg
    assert "g_smoke_r2" not in msg and "g_parts_r2" not in msg  # new names, and --map only reads
    assert calls["push"] == 0 and sum("box-runs" in c for c in calls["ssh"]) == 1  # one listing for the batch


def test_enqueue_queues_new_run_names_and_refuses_one_name_twice_in_a_batch(mac):
    write, box_runs, calls = mac
    box_runs.append("statement_positions/g_map")
    assert jobq.cmd_enqueue([write("g_map_r3", "python3 sp.py map --name g_map_r3")]) == 0
    assert calls["push"] == 1 and sum("/pending && cat >" in c for c in calls["ssh"]) == 1
    reads = write("g_fig", "python3 sp.py figures --name g_map")  # only reads the run: queued with the override
    with pytest.raises(SystemExit, match="--reuse-names"):
        jobq.cmd_enqueue([reads])
    assert jobq.cmd_enqueue([reads], reuse_names=True) == 0 and calls["push"] == 2
    with pytest.raises(SystemExit, match="x2: --name same is also written by x1 in this batch"):
        jobq.cmd_enqueue([write("x1", "python3 a.py --name same"), write("x2", "python3 b.py --name=same")])
    assert jobq.run_names("a manifest --name r && a run --name r && b --name 's' --map q") == ["r", "s"]


def test_box_runs_lists_the_box_results_dirs(tmp_path, monkeypatch, capsys):
    (tmp_path / "results" / "tasks_v2" / "g_competence").mkdir(parents=True)
    (tmp_path / "results" / "tasks_v2" / "notes.txt").write_text("not a run dir")
    monkeypatch.setenv("JOBQ_ROOT", str(tmp_path))
    assert jobq.main(["box-runs"]) == 0
    assert json.loads(capsys.readouterr().out) == ["tasks_v2/g_competence"]


def test_runs_to_pull_skips_local_and_failed_runs(tmp_path):
    (tmp_path / "x6_routes" / "done_run").mkdir(parents=True)
    (tmp_path / "_failed" / "x6_routes" / "failed_run").mkdir(parents=True)
    runs = ["./x6_routes/done_run", "./x6_routes/failed_run", "./x6_routes/new_run"]
    assert jobq.runs_to_pull(runs, tmp_path) == ["x6_routes/new_run"]


# ---------------------------------------------------------------- targets whose meaning changed at the merge (27 Oct)

OLD_32B = "jobs/d1/qwen3_32b_lens_gate.yaml"  # in scripts/jobq_pre_merge_qwen3_32b.txt


def at(path: str, command: str, **over) -> tuple[dict, Path]:
    return spec(id=Path(path).stem, command=command, **over), jobq.REPO / path


def test_a_pre_merge_spec_with_bj_target_qwen3_32b_is_refused_with_the_new_key():
    s, p = at(OLD_32B, "BJ_TARGET=qwen3-32b uv run python scripts/lens_gate.py run --name qwen3_32b_lens_gate")
    errors = " | ".join(jobq.validate(s, p))
    assert "older than the merge" in errors and "qwen3-32b-jlens" in errors and "qwen3_32bj_" in errors
    assert "6fbc0386" in errors  # what qwen3-32b means now
    s, p = at(OLD_32B, "true", figures_command="BJ_TARGET='qwen3-32b' uv run python scripts/lens_gate.py figures")
    assert jobq.renamed_targets(s, p), "figures_command counts too"
    assert jobq.validate(*at(OLD_32B, "BJ_TARGET=qwen3-32b-jlens python3 lens_gate.py --name qwen3_32bj_g")) == []


def test_a_spec_written_after_the_merge_may_use_qwen3_32b():
    """Since the merge qwen3-32b is Zach's J++: a new spec means it."""
    assert (
        jobq.validate(*at("jobs/d1/qwen3_32b_new_v1.yaml", "BJ_TARGET=qwen3-32b python3 x.py --name qwen3_32b_new"))
        == []
    )


@pytest.mark.parametrize(
    ("old", "target", "new"),
    [("muse30b_", "muse-glimmer-30b", "muse30_"), ("qwen36_27b_jlens_", "qwen3.6-27b-jlens", "q27jlens_")],
)
def test_a_run_name_with_an_old_prefix_is_refused_with_the_new_key_and_prefix(old, target, new):
    s, p = at("jobs/c3/x_v1.yaml", f"BJ_TARGET={target} python3 x6_routes.py --name {old}x6_routes")
    errors = jobq.renamed_targets(s, p)
    assert len(errors) == 1 and f"BJ_TARGET={target}" in errors[0] and f"run prefix {new}" in errors[0]
    assert f"{new}x6_routes" in errors[0]
    # a positional name on that prefix's own target (scripts/x0_necessity.py run <name>)
    s, p = at("jobs/c3/x_v1.yaml", f"BJ_TARGET={target} python3 x0_necessity.py run {old}x0_single")
    assert jobq.renamed_targets(s, p)
    # another target reading an old run is fine (the 27B's x45m reads muse30b_x45m_fresh)
    s, p = at(
        "jobs/c3/x_v1.yaml", f"BJ_TARGET=qwen3.6-27b python3 x45m.py --fresh x45m_fresh_27b,{old}x --name x45m_v1"
    )
    assert jobq.validate(s, p) == []


def test_enqueue_refuses_a_renamed_target_before_any_git_or_box_call(mac):
    write, _, calls = mac
    with pytest.raises(SystemExit, match="run prefix muse30_"):
        jobq.cmd_enqueue([write("m_v1", "BJ_TARGET=muse-glimmer-30b python3 x6_routes.py --name muse30b_x6")])
    old = write("qwen3_32b_lens_gate", "BJ_TARGET=qwen3-32b python3 lens_gate.py --name qwen3_32b_lens_gate")
    assert jobq.spec_key(old) == OLD_32B  # REPO is the fixture's folder: the same jobs/<thread>/<id>.yaml
    with pytest.raises(SystemExit, match="qwen3-32b-jlens"):
        jobq.cmd_enqueue([old])
    assert calls == {"ssh": [], "push": 0}


def test_the_pre_merge_list_is_our_tree_at_the_merge():
    """scripts/jobq_pre_merge_qwen3_32b.txt: the specs that set BJ_TARGET=qwen3-32b in a command field in our tree just
    before the merge (66d4b724, the merge's danorel parent)."""
    import yaml

    def git(*a: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *a], cwd=jobq.REPO, capture_output=True, text=True, check=False)

    if git("cat-file", "-e", "66d4b724^{commit}").returncode:
        pytest.skip("commit 66d4b724 not in this clone")
    paths = [
        p for p in git("ls-tree", "-r", "--name-only", "66d4b724", "--", "jobs").stdout.split() if p.endswith(".yaml")
    ]
    want = set()
    for p in paths:
        s = yaml.safe_load(git("show", f"66d4b724:{p}").stdout)
        if any(isinstance(s.get(k), str) and jobq.QWEN3_32B_RE.search(s[k]) for k in jobq.COMMAND_KEYS):
            want.add(p)
    assert jobq.pre_merge_qwen3_32b_specs() == want and OLD_32B in want
