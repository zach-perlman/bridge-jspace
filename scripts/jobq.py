"""jobq: a file-based experiment queue on the GPU box (Dan, 2026-10-20).

A job is a YAML spec, jobs/<thread>/<id>.yaml, written and committed BEFORE the run: the command, what it needs, and
its pre-registration (question, why it matters, hypotheses with predictions, decision rule, controls, n, seeds; see
SPEC). `enqueue` ships the commit to a bare repo on the box (a push to the box, never to GitHub) and drops the spec, as
JSON, into the box's queue. One worker per GPU (a tmux session on the box) takes jobs first in, first out once their
dependencies are done and the GPU has the memory they ask for (it waits; it never kills anything), runs each in a
fresh checkout of the job's commit, and appends to a ledger when it started and ended, how long setup, run and
examples took, the exit code and the GPU's peak memory. On success it runs the job's examples command and drafts an
EXPERIMENTS.md row (verdict left to a human). `pull` brings results, logs, the ledger and the drafts back; the job
pages in examples/ (`make examples-render`) show each job's pre-registration, timing and worked examples.

Box layout (~/jobq): repo.git, pending/ running/ done/ failed/ cancelled/ (one JSON per job), runs/<id>/log.txt
(and runs/<id>/code/, the checkout, removed after the run), results/ (every job's new results dirs), ledger.jsonl,
drafts/<id>.md, worker-gpu<N>.log, archive/<state>/ (finished records moved out of the listing by `archive`). Jobs
read earlier jobs' results: results/ is copied into each checkout first.

    uv run python -m scripts.jobq validate jobs/d2/d2_ko_v1.yaml     # spec check, no box needed
    uv run python -m scripts.jobq enqueue jobs/d2/d2_ko_v1.yaml      # committed tree only
    uv run python -m scripts.jobq status | pull | cancel ID | archive | start-worker [--gpu N]
    python3 ~/jobq/jobq.py worker --gpu 0                             # on the box (stdlib only: system python3)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any

HOST = os.environ.get("JOBQ_HOST", "sesterce-a100x4")  # 4x A100 80GB since 2026-10-21
BOX_ROOT = "jobq"  # relative to the box user's home
REPO = Path(__file__).resolve().parents[1]
STATES = ("pending", "running", "done", "failed", "cancelled")
SPEC: dict[str, tuple[type, ...]] = {  # key -> accepted types; every key required
    "id": (str,),
    "thread": (str,),
    "command": (str,),
    "gpus": (int,),
    "est_gpu_hours": (int, float),
    "question": (str,),
    "why_it_matters": (str,),
    "hypotheses": (dict,),
    "decision_rule": (str,),
    "controls": (list,),
    "n": (int, str),
    "seeds": (list,),
}
OPTIONAL: dict[str, tuple[type, ...]] = {
    "depends_on": (list,),  # job ids that must be done first (their results are copied in)
    "examples_command": (str,),  # run after a successful command; writes the run's examples.json
    "figures_command": (str,),  # run after examples; writes the run's figures into a new analysis-*/ folder
    "mem_gb": (int, float),  # free GPU memory the job needs before it starts (default DEFAULT_MEM_GB)
    "notes": (str,),
    "title": (str,),  # the run's plain name, shown instead of its id (jobs/titles.yaml for older runs)
}
DEFAULT_MEM_GB = 70  # Qwen3.6-27B: ~54 GB bf16 weights + lens maps + activations
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_]*$")
URL_RE = re.compile(r"https?://\S*wandb\S*")
PROGRESS_RE = re.compile(r"\d+%\|")


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def fmt_duration(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    m = round(seconds / 60)
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


# ---------------------------------------------------------------- specs


def validate(spec: Any, path: Path | None = None) -> list[str]:
    """Problems with a job spec ([] if none). The pre-registration fields must be non-empty."""
    if not isinstance(spec, dict):
        return ["the spec is not a mapping"]
    errors = []
    for key, types in SPEC.items():
        if key not in spec:
            errors.append(f"missing {key!r}")
        elif not isinstance(spec[key], types) or isinstance(spec[key], bool):
            errors.append(f"{key!r} must be {' or '.join(t.__name__ for t in types)}")
        elif spec[key] in ("", [], {}):
            errors.append(f"{key!r} is empty")
    for key, types in OPTIONAL.items():
        if key in spec and not isinstance(spec[key], types):
            errors.append(f"{key!r} must be {' or '.join(t.__name__ for t in types)}")
    errors += [f"unknown key {k!r}" for k in spec if k not in SPEC and k not in OPTIONAL]
    if isinstance(spec.get("id"), str) and not ID_RE.match(spec["id"]):
        errors.append(f"id {spec['id']!r} must match {ID_RE.pattern}")
    if path is not None and isinstance(spec.get("id"), str) and path.stem != spec["id"]:
        errors.append(f"file name {path.name!r} must be <id>.yaml ({spec['id']}.yaml)")
    if spec.get("gpus") not in (None, 1) and isinstance(spec.get("gpus"), int):
        errors.append("gpus: only single-GPU jobs are supported so far")
    return errors


def load_spec(path: Path) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text())


# ---------------------------------------------------------------- Mac side


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()


def _ssh(cmd: str, stdin: str | None = None) -> str:
    out = subprocess.run(["ssh", HOST, cmd], input=stdin, check=True, capture_output=True, text=True)
    return out.stdout


def _install_box_script() -> None:
    _ssh(f"mkdir -p ~/{BOX_ROOT}")
    subprocess.run(["scp", "-q", str(Path(__file__).resolve()), f"{HOST}:{BOX_ROOT}/jobq.py"], check=True)


def cmd_validate(paths: list[Path]) -> int:
    bad = 0
    for p in paths:
        errors = validate(load_spec(p), p)
        print(f"{p}: {'ok' if not errors else '; '.join(errors)}")
        bad += bool(errors)
    return 1 if bad else 0


def cmd_enqueue(paths: list[Path], allow_dirty: bool = False) -> int:
    """`allow_dirty`: queue although tracked files have uncommitted changes (e.g. another script being edited). The
    job still runs the committed tree only; the uncommitted paths are recorded in its record as `dirty_paths`."""
    specs = []
    for p in paths:
        spec = load_spec(p)
        if errors := validate(spec, p):
            raise SystemExit(f"{p}: {'; '.join(errors)}")
        specs.append((p.resolve(), spec))
    # Prediction forms (jobs/predictions/) are human notes no job reads: being filled in must not block a queue.
    status = _git("status", "--porcelain", "--untracked-files=no").splitlines()
    changed = [(line, line.split(maxsplit=1)[-1]) for line in status]  # _git strips the first line's leading space
    dirty_paths = [path for _, path in changed if not path.startswith("jobs/predictions/")]
    if dirty_paths and not allow_dirty:
        raise SystemExit(
            "commit first: a job runs the committed tree only (or pass --allow-dirty)\n" + "\n".join(dirty_paths)
        )
    for p, _ in specs:
        try:
            _git("ls-files", "--error-unmatch", str(p))
        except subprocess.CalledProcessError:
            raise SystemExit(f"{p}: not committed (git add + commit the spec first)") from None
    commit = _git("rev-parse", "HEAD")
    _install_box_script()
    taken = set(json.loads(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-ids")))
    ids = [s["id"] for _, s in specs]
    if clash := sorted(taken & set(ids)) or sorted({i for i in ids if ids.count(i) > 1}):
        raise SystemExit(f"job ids are write-once and already used: {clash}")
    refspecs = [f"{commit}:refs/jobq/{s['id']}" for _, s in specs]
    subprocess.run(["git", "push", "-q", f"{HOST}:{BOX_ROOT}/repo.git", *refspecs], cwd=REPO, check=True)
    who = _git("config", "user.name") or "?"
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for i, (p, spec) in enumerate(specs):
        record = {
            **spec,
            "commit": commit,
            "spec_path": str(p.relative_to(REPO)),
            "enqueued_at": now(),
            "enqueued_by": who,
            **({"dirty_paths": dirty_paths} if dirty_paths else {}),
        }
        name = f"{stamp}-{i:02d}_{spec['id']}.json"
        _ssh(
            f"cd ~/{BOX_ROOT}/pending && cat > .{name}.tmp && mv .{name}.tmp {name}", stdin=json.dumps(record, indent=1)
        )
        print(f"queued {spec['id']} @ {commit[:7]} (est {spec['est_gpu_hours']} GPU-h)")
    print(f"status: make queue-status   (workers: tmux ls on {HOST}; make queue-worker starts one)")
    return 0


def cmd_status(as_json: bool = False) -> int:
    _install_box_script()
    print(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-status{' --json' if as_json else ''}"), end="")
    return 0


def cmd_pull() -> int:
    """Results (never overwriting a local file), the ledger, drafts and logs; the queue's state for the job pages."""
    box = f"{HOST}:{BOX_ROOT}"
    jq = REPO / "results" / "jobq"
    (jq / "drafts").mkdir(parents=True, exist_ok=True)
    (REPO / "log" / "jobq").mkdir(parents=True, exist_ok=True)
    rsync = ["rsync", "-a"]
    # whole run dirs (results/<exp>/<run>) not here yet: a run already pulled keeps its local state, so a figures
    # folder redrawn here is not joined again by the box's original one
    runs = _ssh(f"cd ~/{BOX_ROOT}/results && find . -mindepth 2 -maxdepth 2 -type d").split()
    new = [r.removeprefix("./") for r in runs if not (REPO / "results" / r.removeprefix("./")).exists()]
    if new:
        listing = REPO / "cache" / "jobq" / "pull_runs.txt"
        listing.parent.mkdir(parents=True, exist_ok=True)
        listing.write_text("\n".join(new) + "\n")
        subprocess.run(
            [*rsync, "-r", f"--files-from={listing}", f"{box}/results/", str(REPO / "results") + "/"], check=True
        )
    subprocess.run([*rsync, f"{box}/ledger.jsonl", str(jq / "ledger.jsonl")], check=False)  # box: append-only
    subprocess.run([*rsync, f"{box}/drafts/", str(jq / "drafts") + "/"], check=False)
    subprocess.run(
        [*rsync, "--include=*/", "--include=log.txt", "--exclude=*", f"{box}/runs/", str(REPO / "log" / "jobq") + "/"],
        check=False,
    )
    _install_box_script()
    state = REPO / "cache" / "jobq" / "queue_state.json"
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-status --json"))
    print(f"pulled into results/ (new dirs only), {jq.relative_to(REPO)}/, log/jobq/; render: make examples-render")
    return 0


def cmd_cancel(job_id: str) -> int:
    _install_box_script()
    print(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-cancel {job_id}"), end="")
    return 0


def cmd_archive() -> int:
    _install_box_script()
    print(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-archive"), end="")
    return 0


def cmd_start_worker(gpu: int) -> int:
    _install_box_script()
    s = f"jobq-gpu{gpu}"
    run = f"python3 ~/{BOX_ROOT}/jobq.py worker --gpu {gpu} 2>&1 | tee -a ~/{BOX_ROOT}/worker-gpu{gpu}.log"
    _ssh(f"tmux has-session -t {s} 2>/dev/null || tmux new-session -d -s {s} bash -c '{run}; exec bash'")
    print(f"worker {s} on {HOST}: ssh {HOST} -t tmux attach -t {s}")
    return 0


# ---------------------------------------------------------------- box side (stdlib only)


def box_root() -> Path:
    return Path(os.environ.get("JOBQ_ROOT", f"~/{BOX_ROOT}")).expanduser()


def main_repo() -> Path:
    """The box's working copy: its .env (HF token, W&B) and cache/ are shared with the jobs."""
    return Path(os.environ.get("JOBQ_MAIN", "~/bridge-jspace")).expanduser()


def ensure_layout(root: Path) -> None:
    for d in (*STATES, "runs", "results", "drafts"):
        (root / d).mkdir(parents=True, exist_ok=True)
    if not (root / "repo.git").exists():
        subprocess.run(["git", "init", "--bare", "-q", str(root / "repo.git")], check=True)


def read_ledger(root: Path) -> list[dict[str, Any]]:
    path = root / "ledger.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def append_ledger(root: Path, record: dict[str, Any]) -> None:
    with open(root / "ledger.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")


def jobs_in(root: Path, state: str) -> list[Path]:
    return sorted((root / state).glob("*.json"))


def write_json_atomic(path: Path, record: dict[str, Any]) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(record, indent=1))
    os.replace(tmp, path)


def gpu_query(gpu: int, field: str) -> str | None:
    try:
        out = subprocess.run(
            ["nvidia-smi", f"--query-gpu={field}", "--format=csv,noheader,nounits", "-i", str(gpu)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def gpu_free_gb(gpu: int) -> float | None:
    v = gpu_query(gpu, "memory.free")
    return float(v) / 1024 if v else None


def pick(root: Path, gpu: int, check_mem: bool = True) -> tuple[Path | None, str]:
    """The first pending job whose dependencies are done, if the GPU has its memory; else (None, why waiting).
    First in, first out among ready jobs: a big job is never skipped for a smaller one behind it."""
    status = {r["id"]: r["status"] for r in read_ledger(root)}
    waiting = []
    for path in jobs_in(root, "pending"):
        spec = json.loads(path.read_text())
        deps = spec.get("depends_on", [])
        if failed := [d for d in deps if status.get(d) == "failed"]:
            waiting.append(f"{spec['id']}: blocked, dependency failed {failed}")
            continue
        if missing := [d for d in deps if status.get(d) != "done"]:
            waiting.append(f"{spec['id']}: waiting for {missing}")
            continue
        need = float(spec.get("mem_gb", DEFAULT_MEM_GB))
        free = gpu_free_gb(gpu) if check_mem else None
        if free is not None and free < need:
            return None, f"{spec['id']}: needs {need:.0f} GB free on GPU {gpu}, {free:.0f} GB free"
        return path, ""
    return None, "; ".join(waiting) or "queue empty"


def claim(path: Path, root: Path) -> Path | None:
    """Atomic: of several workers, exactly one rename succeeds."""
    target = root / "running" / path.name
    try:
        os.rename(path, target)
    except FileNotFoundError:
        return None
    return target


def _run_logged(cmd: list[str], cwd: Path, log: Path, env: dict[str, str] | None = None) -> int:
    with open(log, "a") as f:
        f.write(f"\n[jobq {now()}] $ {' '.join(cmd)}\n")
        f.flush()
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env=env).returncode


class MemSampler(threading.Thread):
    """Peak memory.used on the job's GPU (the whole device: other processes count too; the baseline is recorded)."""

    def __init__(self, gpu: int, every: float = 10.0):
        super().__init__(daemon=True)
        self.gpu, self.every, self.peak_mb = gpu, every, None
        self._stop_event = threading.Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            v = gpu_query(self.gpu, "memory.used")
            if v:
                self.peak_mb = max(self.peak_mb or 0.0, float(v))
            self._stop_event.wait(self.every)

    def stop(self) -> float | None:
        self._stop_event.set()
        return None if self.peak_mb is None else round(self.peak_mb / 1024, 1)


def results_dirs(results: Path) -> set[str]:
    """Run dirs, results/<exp>/<run>."""
    return {f"{d.parent.name}/{d.name}" for d in results.glob("*/*") if d.is_dir()} if results.exists() else set()


def draft_row(rec: dict[str, Any]) -> str:
    """A draft EXPERIMENTS.md line: date | job | question | result (n, seeds) | W&B | verdict. The result and the
    verdict are a human's to write."""
    date = (rec.get("ended_at") or now())[:10]
    where = ", ".join(f"results/{d}" for d in rec.get("new_results", [])) or "no results dir"
    job = (
        f"jobq {rec['id']} (code {rec['commit'][:7]}, {rec.get('gpu_name') or 'GPU ?'}, run "
        f"{fmt_duration(rec.get('run_s'))}, total {fmt_duration(rec.get('wall_s'))}; spec {rec.get('spec_path')}; "
        f"{where})"
    )
    result = f"(fill in from {where}) n={rec['n']}, seeds={rec['seeds']}; exit {rec.get('exit_code')}"
    wandb = ", ".join(rec.get("wandb", [])) or "none"
    return f"{date} | {job} | {rec['question']} | {result} | {wandb} | UNVERIFIED; verdict: (human)"


def run_job(path: Path, root: Path, gpu: int) -> dict[str, Any]:
    rec = json.loads(path.read_text())
    run_dir = root / "runs" / rec["id"]
    code, log = run_dir / "code", run_dir / "log.txt"
    run_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    rec.update(
        started_at=now(),
        host=socket.gethostname(),
        gpu=gpu,
        gpu_name=gpu_query(gpu, "name"),
        worker_pid=os.getpid(),
        baseline_mem_gb=None if (u := gpu_query(gpu, "memory.used")) is None else round(float(u) / 1024, 1),
    )
    write_json_atomic(path, rec)
    sampler = MemSampler(gpu)
    exit_code, examples_exit, setup_s, run_s, examples_s, error = None, None, None, None, None, None
    figures_exit, figures_s = None, None
    try:
        repo = root / "repo.git"
        if code.exists():
            subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(code)], check=False)
            shutil.rmtree(code, ignore_errors=True)
        subprocess.run(["git", "-C", str(repo), "worktree", "prune"], check=False)
        subprocess.run(
            ["git", "-C", str(repo), "worktree", "add", "--detach", "-q", str(code), rec["commit"]], check=True
        )
        main = main_repo()
        if (main / ".env").exists():
            shutil.copy(main / ".env", code / ".env")
        (main / "cache").mkdir(parents=True, exist_ok=True)
        if not (code / "cache").exists():
            (code / "cache").symlink_to(main / "cache")
        (code / "results").mkdir(exist_ok=True)
        subprocess.run(["rsync", "-a", "--ignore-existing", f"{root / 'results'}/", f"{code / 'results'}/"], check=True)
        before = results_dirs(code / "results")
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu)}
        env["PATH"] = f"{Path('~/.local/bin').expanduser()}:{env.get('PATH', '')}"
        if (code / "pyproject.toml").exists() and _run_logged(["uv", "sync", "--frozen", "-q"], code, log, env) != 0:
            raise RuntimeError("uv sync failed (see log)")
        setup_s = round(time.time() - t0, 1)
        dotenv = "set -a; [ -f .env ] && . ./.env; set +a; "
        sampler.start()
        t1 = time.time()
        exit_code = _run_logged(["bash", "-c", dotenv + rec["command"]], code, log, env)
        run_s = round(time.time() - t1, 1)
        if exit_code == 0 and rec.get("examples_command"):
            t2 = time.time()
            examples_exit = _run_logged(["bash", "-c", dotenv + rec["examples_command"]], code, log, env)
            examples_s = round(time.time() - t2, 1)
        if exit_code == 0 and rec.get("figures_command"):
            t3 = time.time()
            figures_exit = _run_logged(["bash", "-c", dotenv + rec["figures_command"]], code, log, env)
            figures_s = round(time.time() - t3, 1)
        new = sorted(results_dirs(code / "results") - before)
        for d in new:
            (root / "results" / d).parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["rsync", "-a", f"{code / 'results' / d}/", f"{root / 'results' / d}/"], check=True)
        rec["new_results"] = new
    except Exception:
        error = traceback.format_exc()
        with open(log, "a") as f:
            f.write(f"\n[jobq {now()}] worker error:\n{error}")
    peak = sampler.stop() if sampler.is_alive() else None
    ok = error is None and exit_code == 0 and examples_exit in (None, 0) and figures_exit in (None, 0)
    log_text = log.read_text(errors="replace") if log.exists() else ""
    rec.update(
        status="done" if ok else "failed",
        ended_at=now(),
        wall_s=round(time.time() - t0, 1),
        setup_s=setup_s,
        run_s=run_s,
        examples_s=examples_s,
        exit_code=exit_code,
        examples_exit=examples_exit,
        figures_s=figures_s,
        figures_exit=figures_exit,
        peak_mem_gb=peak,
        error=error,
        log=f"runs/{rec['id']}/log.txt",
        wandb=sorted(set(URL_RE.findall(log_text))),
    )
    rec.setdefault("new_results", [])
    append_ledger(root, rec)
    (root / "drafts" / f"{rec['id']}.md").write_text(draft_row(rec) + "\n")
    write_json_atomic(path, rec)
    os.replace(path, root / rec["status"] / path.name)
    if code.exists():
        subprocess.run(["git", "-C", str(root / "repo.git"), "worktree", "remove", "--force", str(code)], check=False)
    return rec


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def recover_orphans(root: Path, gpu: int) -> None:
    """Jobs left in running/ by a dead worker on this GPU and host are failed (re-enqueue under a new id)."""
    for path in jobs_in(root, "running"):
        rec = json.loads(path.read_text())
        if rec.get("gpu") != gpu or rec.get("host") != socket.gethostname() or _alive(rec.get("worker_pid", -1)):
            continue
        rec.update(status="failed", ended_at=now(), error="worker died during the run (found on worker restart)")
        rec.setdefault("new_results", [])
        append_ledger(root, rec)
        write_json_atomic(path, rec)
        os.replace(path, root / "failed" / path.name)
        print(f"[jobq {now()}] {rec['id']}: orphaned by a dead worker, marked failed", flush=True)


def worker(gpu: int, root: Path | None = None, once: bool = False, poll: float = 20.0, check_mem: bool = True) -> None:
    root = root or box_root()
    ensure_layout(root)
    recover_orphans(root, gpu)
    print(f"[jobq {now()}] worker on GPU {gpu}, root {root}", flush=True)
    last = None
    while True:
        path, why = pick(root, gpu, check_mem)
        if path is None:
            if why != last:
                print(f"[jobq {now()}] idle: {why}", flush=True)
                last = why
            if once:
                return
            time.sleep(poll)
            continue
        last = None
        claimed = claim(path, root)
        if claimed is not None:
            print(f"[jobq {now()}] start {claimed.stem}", flush=True)
            rec = run_job(claimed, root, gpu)
            print(
                f"[jobq {now()}] {rec['status']} {rec['id']}: run {fmt_duration(rec['run_s'])}, total "
                f"{fmt_duration(rec['wall_s'])}, exit {rec['exit_code']}",
                flush=True,
            )
        if once:
            return


def last_progress(log: Path) -> str:
    if not log.exists():
        return ""
    tail = log.read_bytes()[-20000:].decode(errors="replace").replace("\r", "\n").splitlines()
    for line in reversed(tail):
        if PROGRESS_RE.search(line) or "ETA" in line:
            return line.strip()[:160]
    return tail[-1].strip()[:160] if tail else ""


def box_status(root: Path, as_json: bool = False) -> str:
    ensure_layout(root)
    state: dict[str, list[dict[str, Any]]] = {s: [] for s in STATES}
    for s in STATES:
        for path in jobs_in(root, s):
            rec = json.loads(path.read_text())
            if s == "running":
                started = dt.datetime.fromisoformat(rec["started_at"]) if rec.get("started_at") else None
                rec["elapsed_s"] = (dt.datetime.now().astimezone() - started).total_seconds() if started else None
                rec["progress"] = last_progress(root / "runs" / rec["id"] / "log.txt")
            state[s].append(rec)
    if as_json:
        return json.dumps(state, indent=1)
    lines = []
    for rec in state["running"]:
        lines.append(
            f"RUNNING  {rec['id']:<32} GPU {rec.get('gpu')}  {fmt_duration(rec.get('elapsed_s'))} "
            f"of est {rec['est_gpu_hours']}h  | {rec.get('progress', '')}"
        )
    gpu0 = 0
    for rec in state["pending"]:
        lines.append(f"PENDING  {rec['id']:<32} est {rec['est_gpu_hours']}h  deps {rec.get('depends_on', [])}")
    if state["pending"]:
        lines.append(f"         next: {pick(root, gpu0)[1] or 'ready'}")
    for s in ("done", "failed"):
        for rec in sorted(state[s], key=lambda r: r.get("ended_at", ""))[-10:]:
            lines.append(
                f"{s.upper():<8} {rec['id']:<32} run {fmt_duration(rec.get('run_s'))} (est {rec['est_gpu_hours']}h), "
                f"total {fmt_duration(rec.get('wall_s'))}, exit {rec.get('exit_code')}, ended {rec.get('ended_at')}"
            )
    return "\n".join(lines or ["queue empty"]) + "\n"


def box_ids(root: Path) -> list[str]:
    ensure_layout(root)
    ids = {r["id"] for r in read_ledger(root)}
    for s in STATES:
        ids |= {json.loads(p.read_text())["id"] for p in jobs_in(root, s)}
    return sorted(ids)


def box_archive(root: Path) -> str:
    """Finished jobs' records (done, failed, cancelled) out of the status listing, into archive/<state>/; nothing is
    deleted. Dependencies and job pages read the ledger, which stays as it is."""
    ensure_layout(root)
    moved = {}
    for s in ("done", "failed", "cancelled"):
        paths = jobs_in(root, s)
        (root / "archive" / s).mkdir(parents=True, exist_ok=True)
        for path in paths:
            os.replace(path, root / "archive" / s / path.name)
        moved[s] = len(paths)
    return "archived " + ", ".join(f"{n} {s}" for s, n in moved.items()) + " (ledger unchanged)\n"


def box_cancel(root: Path, job_id: str) -> str:
    for path in jobs_in(root, "pending"):
        if json.loads(path.read_text())["id"] == job_id:
            os.replace(path, root / "cancelled" / path.name)
            return f"cancelled {job_id}\n"
    return f"{job_id}: not pending (a running job is stopped from its tmux session: Ctrl-C in jobq-gpu<N>)\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").add_argument("specs", nargs="+", type=Path)
    eq = sub.add_parser("enqueue")
    eq.add_argument("specs", nargs="+", type=Path)
    eq.add_argument("--allow-dirty", action="store_true", help="queue despite uncommitted tracked files (recorded)")
    sub.add_parser("status").add_argument("--json", action="store_true")
    sub.add_parser("pull")
    sub.add_parser("cancel").add_argument("id")
    sub.add_parser("archive", help="move finished jobs' records out of the status listing (ledger unchanged)")
    sub.add_parser("start-worker").add_argument("--gpu", type=int, default=0)
    w = sub.add_parser("worker")
    w.add_argument("--gpu", type=int, default=0)
    w.add_argument("--once", action="store_true")
    sub.add_parser("box-status").add_argument("--json", action="store_true")
    sub.add_parser("box-ids")
    sub.add_parser("box-cancel").add_argument("id")
    sub.add_parser("box-archive")
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        return cmd_validate(a.specs)
    if a.cmd == "enqueue":
        return cmd_enqueue(a.specs, a.allow_dirty)
    if a.cmd == "status":
        return cmd_status(a.json)
    if a.cmd == "pull":
        return cmd_pull()
    if a.cmd == "cancel":
        return cmd_cancel(a.id)
    if a.cmd == "archive":
        return cmd_archive()
    if a.cmd == "box-archive":
        print(box_archive(box_root()), end="")
        return 0
    if a.cmd == "start-worker":
        return cmd_start_worker(a.gpu)
    if a.cmd == "worker":
        worker(a.gpu, once=a.once)
        return 0
    if a.cmd == "box-status":
        print(box_status(box_root(), a.json), end="")
        return 0
    if a.cmd == "box-ids":
        print(json.dumps(box_ids(box_root())))
        return 0
    if a.cmd == "box-cancel":
        print(box_cancel(box_root(), a.id), end="")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
