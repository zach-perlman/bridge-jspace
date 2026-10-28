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

Several GPUs per job (23 Oct, the 122B on 2x H100 80 GB): a worker owns one GPU (--gpu N) or several (--gpus 0,1;
tmux jobq-gpu0-1). A job with `gpus: k` runs on the first k GPUs of a worker that owns at least k (CUDA_VISIBLE_DEVICES
lists them; its command splits the model over them, BJ_DEVICE_MAP=auto, which the spec check requires); a worker with
fewer GPUs passes it over. `mem_gb` is the free memory the job needs in total over its k GPUs, and the peak recorded is
the total too (per GPU in peak_mem_gb_per_gpu). A worker's GPUs are its own: no other worker may own one of them.

Box layout (~/jobq): repo.git, pending/ running/ done/ failed/ cancelled/ (one JSON per job), runs/<id>/log.txt
(and runs/<id>/code/, the checkout, removed after the run), results/ (every job's new results dirs), ledger.jsonl,
drafts/<id>.md, worker-gpu<N>.log, archive/<state>/ (finished records moved out of the listing by `archive`). Jobs
read earlier jobs' results: results/ is copied into each checkout first.

    uv run python -m scripts.jobq validate jobs/d2/d2_ko_v1.yaml     # spec check, no box needed
    uv run python -m scripts.jobq enqueue jobs/d2/d2_ko_v1.yaml      # committed tree only; new ids and run names
    uv run python -m scripts.jobq status | pull | cancel ID | archive | start-worker [--gpu N | --gpus 0,1]
    python3 ~/jobq/jobq.py worker --gpu 0                             # on the box (stdlib only: system python3)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
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
    "mem_gb": (int, float),  # free GPU memory the job needs before it starts, in total over its gpus (DEFAULT_MEM_GB)
    "notes": (str,),
    "title": (str,),  # the run's plain name, shown instead of its id (jobs/titles.yaml for older runs)
}
DEFAULT_MEM_GB = 70  # Qwen3.6-27B: ~54 GB bf16 weights + lens maps + activations
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_]*$")
NAME_RE = re.compile(r"--name[ =]['\"]?([\w.-]+)")  # a script's run name: it writes results/<script>/<name>/
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
    gpus = spec.get("gpus")
    if isinstance(gpus, int) and not isinstance(gpus, bool):
        if gpus < 1:
            errors.append("'gpus' must be >= 1")
        elif gpus > 1 and "BJ_DEVICE_MAP=" not in str(spec.get("command", "")):
            # without it the model loads onto the first GPU alone and the others sit idle (bridge_jspace.model)
            errors.append(f"gpus: {gpus} needs a command that splits the model over them (BJ_DEVICE_MAP=auto)")
    text = " ".join(spec[k] for k in COMMAND_KEYS if isinstance(spec.get(k), str))
    errors += [f"placeholder {p} in the command: replace it with the value before enqueue"
               for p in dict.fromkeys(PLACEHOLDER_RE.findall(text))]  # fmt: skip
    return errors + renamed_targets(spec, path)


# A value a draft spec waits for, written as <WHAT>_FROM_<WHO> (45s: BJ_MAMBA_SSM_REVISION=REVISION_FROM_ZACH): validate,
# and so enqueue, refuses the spec until it is replaced.
PLACEHOLDER_RE = re.compile(r"\b[A-Z][A-Z0-9_]*_FROM_[A-Z]+\b")


# ---------------------------------------------------------------- targets whose meaning changed at the merge
# The merge of danorel into main (27 Oct 2026, merge commit fbedabbb; our side 66d4b724) kept main's pins keys. Two of
# our specs' names now mean something else: BJ_TARGET=qwen3-32b is Zach's J++ (sha256 6fbc0386), our plain J-lens
# being qwen3-32b-jlens (prefix qwen3_32bj_); and our run prefixes muse30b_ and qwen36_27b_jlens_ are main's muse30_ and
# q27jlens_ (pins.check_run_name refuses them). Specs are never edited: validate, and so enqueue, refuses those specs.
COMMAND_KEYS = ("command", "examples_command", "figures_command")
QWEN3_32B_RE = re.compile(r"""\bBJ_TARGET=["']?qwen3-32b(?![\w.-])""")  # not qwen3-32b-jlens / -jpp / -jpp32
# The specs "older than the merge" that set it: those in our tree at 66d4b724 (frozen list; tests/test_jobq.py checks
# it against that tree). Read only when a spec sets BJ_TARGET=qwen3-32b (validate runs on the Mac, never on the box).
PRE_MERGE_QWEN3_32B = Path(__file__).with_name("jobq_pre_merge_qwen3_32b.txt")
RENAMED_PREFIXES = {  # our old run prefix -> (the key that has those runs' target now, its prefix)
    "muse30b_": ("muse-glimmer-30b", "muse30_"),
    "qwen36_27b_jlens_": ("qwen3.6-27b-jlens", "q27jlens_"),
}


def pre_merge_qwen3_32b_specs() -> frozenset[str]:
    lines = PRE_MERGE_QWEN3_32B.read_text().splitlines()
    return frozenset(line.strip() for line in lines if line.strip() and not line.startswith("#"))


def spec_key(path: Path | None) -> str | None:
    """A spec's path from the repo root (jobs/<thread>/<id>.yaml), as the frozen list names it."""
    if path is None:
        return None
    p = Path(path)
    try:
        return (p if p.is_absolute() else Path.cwd() / p).resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


def renamed_targets(spec: dict[str, Any], path: Path | None = None) -> list[str]:
    """Refusals for a spec that names a target whose meaning changed at the merge into main (Dan, 27 Oct ~14:40): a
    pre-merge spec with BJ_TARGET=qwen3-32b; a run name written with one of our old prefixes (a --name value, or on
    that prefix's own target any name in the command: some scripts take it positionally). A spec on another target
    that only reads an old run (the 27B's x45m reads muse30b_x45m_fresh) passes. [] if none."""
    commands = [spec[k] for k in COMMAND_KEYS if isinstance(spec.get(k), str)]
    text = " ".join(commands)
    errors = []
    key = spec_key(path)
    if key and QWEN3_32B_RE.search(text) and key in pre_merge_qwen3_32b_specs():
        errors.append(
            f"{key} is older than the merge into main (27 Oct), when BJ_TARGET=qwen3-32b was our plain J-lens: it is "
            "now Zach's J++ (sha256 6fbc0386). Our J-lens is BJ_TARGET=qwen3-32b-jlens (run prefix qwen3_32bj_): "
            "write a new spec with it; this one is not enqueued"
        )
    for old, (target, new) in RENAMED_PREFIXES.items():
        written = [n for n in run_names(text) if n.startswith(old)]
        if re.search(rf"\bBJ_TARGET=[\"']?{re.escape(target)}(?![\w.-])", text):
            written += re.findall(rf"(?<![\w-]){re.escape(old)}[\w.-]*", text)
        for name in dict.fromkeys(written):
            errors.append(
                f"run name {name!r}: the prefix {old} belongs to no target since the merge into main (27 Oct); its "
                f"target is BJ_TARGET={target}, run prefix {new} (pins.check_run_name). Write a new spec (e.g. "
                f"{new}{name[len(old) :]}); this one is not enqueued"
            )
    return errors


def load_spec(path: Path) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text())


def run_names(command: str) -> list[str]:
    """The run names a command writes (each `--name X`, once, in order; `manifest --name X && run --name X` is one)."""
    return list(dict.fromkeys(NAME_RE.findall(command)))


def name_clashes(specs: list[dict[str, Any]], box_runs: list[str]) -> list[str]:
    """One line per run name a spec's command would write that is taken: a results/<exp>/<name> dir already on the
    box (`box_runs`: '<exp>/<name>'; runs are written once, so the job would die on its write-once check), or a name
    another spec of the same batch writes. [] if none."""
    on_box: dict[str, list[str]] = {}
    for r in box_runs:
        on_box.setdefault(r.split("/", 1)[-1], []).append(f"results/{r}")
    out, first = [], {}
    for s in specs:
        for name in run_names(s["command"]):
            if name in on_box:
                out.append(f"{s['id']}: --name {name} exists on the box: {', '.join(sorted(on_box[name]))}")
            if name in first:
                out.append(f"{s['id']}: --name {name} is also written by {first[name]} in this batch")
            first.setdefault(name, s["id"])
    return out


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


def cmd_enqueue(paths: list[Path], allow_dirty: bool = False, reuse_names: bool = False) -> int:
    """`allow_dirty`: queue although tracked files have uncommitted changes (e.g. another script being edited). The
    job still runs the committed tree only; the uncommitted paths are recorded in its record as `dirty_paths`.
    `reuse_names`: queue although a run name (--name) of a command already exists in the box's results/ (a command
    that only reads that run); refused otherwise, with the existing folders named (one ssh call per batch)."""
    specs = []
    for p in paths:
        spec = load_spec(p)
        if errors := validate(spec, p):
            raise SystemExit(f"{p}: {'; '.join(errors)}")
        specs.append((p.resolve(), spec))
    # Prediction forms (predictions/) are human notes no job reads: being filled in must not block a queue.
    status = _git("status", "--porcelain", "--untracked-files=no").splitlines()
    changed = [(line, line.split(maxsplit=1)[-1]) for line in status]  # _git strips the first line's leading space
    dirty_paths = [path for _, path in changed if not path.startswith("predictions/")]
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
    if other := sorted(ids_on_other_boxes(REPO, HOST) & set(ids)):  # logs / drafts are pulled into one folder per id
        raise SystemExit(f"job ids already used on another queue box (one id, one box): {other}")
    # the box copies its results/ into every checkout: a run name already there dies on the script's write-once check
    box_runs = json.loads(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-runs"))
    if (clash := name_clashes([s for _, s in specs], box_runs)) and not reuse_names:
        raise SystemExit(
            f"run names are written once and already taken on {HOST}:\n" + "\n".join(clash) + "\nrename the runs "
            "(e.g. the _rN suffix of a retry) or, if the command only reads that run, pass --reuse-names"
        )
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


def ids_on_other_boxes(repo: Path, host: str) -> set[str]:
    """Job ids known from the other boxes' pulled ledgers and queue states (results/jobq/ledger_<host>.jsonl,
    cache/jobq/queue_state_<host>.json; the older unsuffixed and archive ledgers count as the A100's)."""
    own = {f"ledger_{host}.jsonl", f"queue_state_{host}.json"}
    if host == "sesterce-a100x4":  # the A100's older ledgers are its own
        own |= {"ledger.jsonl", "queue_state.json", "ledger_a100_until_2026-10-21.jsonl", "ledger_seed_a100x4.jsonl"}
    ids: set[str] = set()
    for p in sorted((repo / "results" / "jobq").glob("ledger*.jsonl")):
        if p.name not in own:
            ids |= {json.loads(x)["id"] for x in p.read_text().splitlines() if x.strip()}
    for p in sorted((repo / "cache" / "jobq").glob("queue_state*.json")):
        if p.name not in own:
            state = json.loads(p.read_text() or "{}")
            ids |= {r["id"] for s in ("pending", "running", "cancelled") for r in state.get(s, [])}
    return ids


def runs_to_pull(runs: list[str], results: Path) -> list[str]:
    """The box's run dirs (exp/run, as `find .` prints them) not here yet: neither under results/ nor under
    results/_failed/, where failed runs' partial dirs are moved (Dan, 27 Oct), so a pull does not bring them back."""
    rel = [r.removeprefix("./") for r in runs]
    return [r for r in rel if not (results / r).exists() and not (results / "_failed" / r).exists()]


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
    new = runs_to_pull(runs, REPO / "results")
    if new:
        listing = REPO / "cache" / "jobq" / "pull_runs.txt"
        listing.parent.mkdir(parents=True, exist_ok=True)
        listing.write_text("\n".join(new) + "\n")
        subprocess.run(
            [*rsync, "-r", f"--files-from={listing}", f"{box}/results/", str(REPO / "results") + "/"], check=True
        )
    # one ledger / queue state per box: a second queue (JOBQ_HOST=sesterce-h200x2) must not overwrite the A100's copies
    sfx = f"_{HOST}"  # every box its own ledger and queue state (Dan, 23 Oct); readers: bridge_jspace.ledgers
    subprocess.run([*rsync, f"{box}/ledger.jsonl", str(jq / f"ledger{sfx}.jsonl")], check=False)  # box: append-only
    subprocess.run([*rsync, f"{box}/drafts/", str(jq / "drafts") + "/"], check=False)
    subprocess.run(
        [*rsync, "--include=*/", "--include=log.txt", "--exclude=*", f"{box}/runs/", str(REPO / "log" / "jobq") + "/"],
        check=False,
    )
    _install_box_script()
    state = REPO / "cache" / "jobq" / f"queue_state{sfx}.json"
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


def gpu_list(gpus: int | str | list[int]) -> list[int]:
    """A worker's GPUs: 0, "0,1" or [0, 1] -> [0, 1] (distinct, in the given order)."""
    if isinstance(gpus, int):
        return [gpus]
    out = [int(g) for g in gpus.split(",")] if isinstance(gpus, str) else list(gpus)
    if not out or len(set(out)) != len(out):
        raise ValueError(f"GPUs must be listed once each: {gpus!r}")
    return out


def gpu_tag(gpus: list[Any]) -> str:
    """The worker's name on the box: jobq-gpu<tag>, worker-gpu<tag>.log ("0", or "0-1" for GPUs 0 and 1)."""
    return "-".join(map(str, gpus))


def cmd_start_worker(gpus: list[int]) -> int:
    _install_box_script()
    tag, arg = gpu_tag(gpus), ",".join(map(str, gpus))
    s = f"jobq-gpu{tag}"
    run = f"python3 ~/{BOX_ROOT}/jobq.py worker --gpus {arg} 2>&1 | tee -a ~/{BOX_ROOT}/worker-gpu{tag}.log"
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


def gpu_free_gb(gpus: int | list[int]) -> float | None:
    """Free memory in total over the GPUs (GB); None if any of them cannot be read."""
    free = [gpu_query(g, "memory.free") for g in gpu_list(gpus)]
    return None if not all(free) else sum(float(v) for v in free if v) / 1024


def box_gpus() -> list[int]:
    """Every GPU on this box ([0] without nvidia-smi)."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=index", "--format=csv,noheader"], capture_output=True,
                             text=True, timeout=30, check=True).stdout.split()  # fmt: skip
    except (OSError, subprocess.SubprocessError):
        return [0]
    return [int(g) for g in out] or [0]


def pick(root: Path, gpus: int | list[int], check_mem: bool = True) -> tuple[Path | None, str]:
    """The first pending job whose dependencies are done and that fits this worker, if its GPUs have the job's memory
    (mem_gb, in total over the job's first `gpus` GPUs of the worker); else (None, why waiting). First in, first out
    among ready jobs: a big job is never skipped for a smaller one behind it; a job needing more GPUs than the worker
    owns is left to a worker that has them."""
    own = gpu_list(gpus)
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
        k = int(spec.get("gpus", 1))
        if k > len(own):
            waiting.append(f"{spec['id']}: needs {k} GPUs, a worker on GPU {gpu_tag(own)} has {len(own)}")
            continue
        need = float(spec.get("mem_gb", DEFAULT_MEM_GB))
        free = gpu_free_gb(own[:k]) if check_mem else None
        if free is not None and free < need:
            return None, f"{spec['id']}: needs {need:.0f} GB free on GPU {gpu_tag(own[:k])}, {free:.0f} GB free"
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
    """Peak memory.used on the job's GPUs (whole devices: other processes count too; the baseline is recorded): the
    peak of the total over its GPUs, and each GPU's own peak."""

    def __init__(self, gpus: int | list[int], every: float = 10.0):
        super().__init__(daemon=True)
        self.gpus, self.every, self.peak_mb = gpu_list(gpus), every, None
        self.peak_mb_per_gpu: list[float | None] = [None] * len(self.gpus)
        self._stop_event = threading.Event()

    def sample(self) -> None:
        used = [gpu_query(g, "memory.used") for g in self.gpus]
        for i, v in enumerate(used):
            if v:
                self.peak_mb_per_gpu[i] = max(self.peak_mb_per_gpu[i] or 0.0, float(v))
        if all(used):
            self.peak_mb = max(self.peak_mb or 0.0, sum(float(v) for v in used if v))

    def run(self) -> None:
        while not self._stop_event.is_set():
            self.sample()
            self._stop_event.wait(self.every)

    def stop(self) -> float | None:
        self._stop_event.set()
        return None if self.peak_mb is None else round(self.peak_mb / 1024, 1)

    def per_gpu(self) -> list[float | None]:
        return [None if v is None else round(v / 1024, 1) for v in self.peak_mb_per_gpu]


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


def run_job(path: Path, root: Path, gpus: int | list[int]) -> dict[str, Any]:
    """Runs the job on the first `gpus` (the spec's count) of the worker's GPUs."""
    rec = json.loads(path.read_text())
    run_dir = root / "runs" / rec["id"]
    code, log = run_dir / "code", run_dir / "log.txt"
    run_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    use = gpu_list(gpus)[: int(rec.get("gpus", 1))]
    name = gpu_query(use[0], "name")
    used = [gpu_query(g, "memory.used") for g in use]
    rec.update(
        started_at=now(),
        host=socket.gethostname(),
        gpu=use[0],  # the first (home) GPU; every GPU in gpu_ids
        gpu_ids=use,
        gpu_name=f"{len(use)}x {name}" if name and len(use) > 1 else name,
        worker_pid=os.getpid(),
        baseline_mem_gb=round(sum(float(u) for u in used if u) / 1024, 1) if all(used) else None,
    )
    write_json_atomic(path, rec)
    sampler = MemSampler(use)
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
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": ",".join(map(str, use))}
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
    per_gpu = sampler.per_gpu()  # all None if it never ran
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
        peak_mem_gb_per_gpu=per_gpu,
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


def recover_orphans(root: Path, gpus: int | list[int]) -> None:
    """Jobs left in running/ by a dead worker on these GPUs and host are failed (re-enqueue under a new id)."""
    own = gpu_list(gpus)
    for path in jobs_in(root, "running"):
        rec = json.loads(path.read_text())
        if rec.get("gpu") not in own or rec.get("host") != socket.gethostname() or _alive(rec.get("worker_pid", -1)):
            continue
        rec.update(status="failed", ended_at=now(), error="worker died during the run (found on worker restart)")
        rec.setdefault("new_results", [])
        append_ledger(root, rec)
        write_json_atomic(path, rec)
        os.replace(path, root / "failed" / path.name)
        print(f"[jobq {now()}] {rec['id']}: orphaned by a dead worker, marked failed", flush=True)


def worker(
    gpus: int | list[int], root: Path | None = None, once: bool = False, poll: float = 20.0, check_mem: bool = True
) -> None:
    """One worker owning `gpus` (one GPU, or several for jobs with gpus > 1), one job at a time."""
    root = root or box_root()
    gpus = gpu_list(gpus)
    ensure_layout(root)
    recover_orphans(root, gpus)
    print(f"[jobq {now()}] worker on GPU {gpu_tag(gpus)}, root {root}", flush=True)
    last = None
    while True:
        path, why = pick(root, gpus, check_mem)
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
            rec = run_job(claimed, root, gpus)
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
            f"RUNNING  {rec['id']:<32} GPU {gpu_tag(rec.get('gpu_ids') or [rec.get('gpu')])}  "
            f"{fmt_duration(rec.get('elapsed_s'))} of est {rec['est_gpu_hours']}h  | {rec.get('progress', '')}"
        )
    for rec in state["pending"]:
        lines.append(f"PENDING  {rec['id']:<32} est {rec['est_gpu_hours']}h  deps {rec.get('depends_on', [])}")
    if state["pending"]:  # as a worker owning every GPU of the box would see it
        lines.append(f"         next: {pick(root, box_gpus())[1] or 'ready'}")
    for s in ("done", "failed"):
        for rec in sorted(state[s], key=lambda r: r.get("ended_at", ""))[-10:]:
            lines.append(
                f"{s.upper():<8} {rec['id']:<32} run {fmt_duration(rec.get('run_s'))} (est {rec['est_gpu_hours']}h), "
                f"total {fmt_duration(rec.get('wall_s'))}, exit {rec.get('exit_code')}, ended {rec.get('ended_at')}"
            )
    return "\n".join(lines or ["queue empty"]) + "\n"


def timeline(
    running_left: list[float], pending: list[dict[str, Any]], done_ids: set[str], n_gpu: int, running_ids=None
) -> tuple[dict[str, tuple[float, float]], float, list[str]]:
    """List scheduling on n_gpu workers, first in first out, a job starting once its dependencies have finished
    (memory not modelled). running_left: hours left of each running job (running_ids: their ids, so pending jobs can
    depend on them). Returns ({id: (start, end) hours from now}, hours until the queue drains, ids that cannot be
    scheduled because a dependency is outside the queue: failed or unknown). Pure."""
    running_ids = list(running_ids or [])
    finish: dict[str, float] = dict(zip(running_ids, running_left, strict=False))
    free = sorted(running_left + [0.0] * max(0, n_gpu - len(running_left)))[:n_gpu] or [0.0]
    spans: dict[str, tuple[float, float]] = {i: (0.0, h) for i, h in finish.items()}
    queue = list(pending)
    while queue:
        free.sort()
        t = free[0]  # the next GPU to free; as the worker does, it takes the first job whose dependencies are done by then
        deps = [r.get("depends_on", []) for r in queue]
        ready = [i for i, ds in enumerate(deps) if all(d in done_ids or finish.get(d, math.inf) <= t + 1e-9 for d in ds)]
        if ready:
            idx, start = ready[0], t
        else:  # nothing ready yet: the GPU idles until the earliest dependency (in the queue or running) finishes
            known = [(max([finish[d] for d in ds if d not in done_ids] or [t]), i)
                     for i, ds in enumerate(deps) if all(d in done_ids or d in finish for d in ds)]  # fmt: skip
            if not known:  # dependencies outside the queue (failed or unknown): the rest stays unscheduled
                return spans, max(free), [r["id"] for r in queue]
            start, idx = min(known)
        rec = queue.pop(idx)
        free[0] = start + float(rec.get("est_gpu_hours", 0.0))
        finish[rec["id"]] = free[0]
        spans[rec["id"]] = (start, free[0])
    return spans, max(free), []


def schedule(running_left: list[float], pending: list[dict[str, Any]], done_ids: set[str], n_gpu: int) -> float:
    """Hours until the queue drains (timeline's second value)."""
    return timeline(running_left, pending, done_ids, n_gpu)[1]


def box_stats(root: Path, hours: float = 24.0, n_gpu: int = 4) -> str:
    """Counts, GPU-hours used in the last `hours`, what is left and when the queue should drain."""
    ensure_layout(root)
    now_ = dt.datetime.now().astimezone()
    since = now_ - dt.timedelta(hours=hours)
    ledger = [r for r in read_ledger(root) if r.get("ended_at") and dt.datetime.fromisoformat(r["ended_at"]) >= since]
    state = {s: [json.loads(p.read_text()) for p in jobs_in(root, s)] for s in ("pending", "running")}
    done = [r for r in ledger if r.get("status") == "done"]
    failed = [r for r in ledger if r.get("status") == "failed"]
    used = sum(r.get("run_s") or 0 for r in ledger) / 3600
    ratios = sorted(
        r["run_s"] / 3600 / float(r["est_gpu_hours"]) for r in done if r.get("run_s") and r.get("est_gpu_hours")
    )
    ratio = ratios[len(ratios) // 2] if ratios else 1.0
    # Two readings of every estimate: "typical" = estimate x the median actual / estimate of this box's done jobs,
    # "estimate" = the spec's own number (the upper end). A running job past its typical time is given 5 min more.
    run_ids, el_h, left_est, left_typ = [], [], [], []
    for rec in state["running"]:
        el = (now_ - dt.datetime.fromisoformat(rec["started_at"])).total_seconds() / 3600 if rec.get("started_at") else 0
        used += el
        est = float(rec["est_gpu_hours"])
        run_ids.append(rec["id"])
        el_h.append(el)
        left_est.append(max(est - el, 1 / 12))
        left_typ.append(max(est * ratio - el, 1 / 12))
    done_ids = {r["id"] for r in read_ledger(root) if r.get("status") == "done"}
    pend = state["pending"]
    span_est, drain_est, stuck = timeline(left_est, pend, done_ids, n_gpu, run_ids)
    span_typ, drain_typ, _ = timeline(
        left_typ, [{**r, "est_gpu_hours": float(r["est_gpu_hours"]) * ratio} for r in pend], done_ids, n_gpu, run_ids
    )
    gpu_h_est = sum(left_est) + sum(float(r["est_gpu_hours"]) for r in pend if r["id"] not in stuck)
    gpu_h_typ = sum(left_typ) + sum(float(r["est_gpu_hours"]) * ratio for r in pend if r["id"] not in stuck)

    def at(h: float) -> str:
        return (now_ + dt.timedelta(hours=h)).astimezone(dt.timezone.utc).strftime("%H:%M")  # noqa: UP017 (the boxes run Python 3.10)

    def hm(h: float) -> str:
        m = round(h * 60)
        return f"{m // 60}h{m % 60:02d}m"

    lines = [f"now {at(0)} UTC · {n_gpu} GPU{'s' if n_gpu != 1 else ''} · {len(state['running'])} running, "
             f"{len(pend)} pending"]  # fmt: skip
    for i, rec in enumerate(state["running"]):
        a, b = span_typ[rec["id"]][1], span_est[rec["id"]][1]
        past = "  (past its typical time)" if el_h[i] > float(rec["est_gpu_hours"]) * ratio else ""
        lines.append(f"  RUN   {rec['id']:<26} {hm(el_h[i])} so far, est {float(rec['est_gpu_hours']):.1f}h"
                     f"   ends {at(min(a, b))}-{at(max(a, b))} UTC{past}")  # fmt: skip
    for rec in pend:
        if rec["id"] in stuck:
            lines.append(f"  WAIT  {rec['id']:<26} blocked: a dependency failed or is not in this queue "
                         f"({', '.join(rec.get('depends_on', []))})")  # fmt: skip
            continue
        (s1, e1), (s2, e2) = span_typ[rec["id"]], span_est[rec["id"]]
        after = f", after {', '.join(rec['depends_on'])}" if rec.get("depends_on") else ""
        lines.append(f"  WAIT  {rec['id']:<26} est {float(rec['est_gpu_hours']):.1f}h{after}"
                     f"   starts {at(min(s1, s2))}-{at(max(s1, s2))}, ends {at(min(e1, e2))}-{at(max(e1, e2))} UTC")  # fmt: skip
    if state["running"] or pend:
        lo, hi = min(drain_typ, drain_est), max(drain_typ, drain_est)
        lines += [
            f"left:   {gpu_h_typ:.1f}-{gpu_h_est:.1f} GPU-h of work · {hm(lo)}-{hm(hi)} wall clock until the queue "
            f"drains · done {at(lo)}-{at(hi)} UTC",
            f"        (low end: estimates x {ratio:.2f}, the median actual / estimate of {len(ratios)} done jobs here; "
            "high end: the specs' estimates; memory not modelled)",
        ]
    else:
        lines.append("left:   nothing queued; this box is idle")
    lines.append(f"last {hours:g} h: {len(done)} done, {len(failed)} failed; {used:.1f} GPU-h used (running included)")
    # only failures still in failed/ (box-archive moves the looked-at ones to archive/; the ledger keeps them all)
    open_ids = {json.loads(p.read_text())["id"] for p in jobs_in(root, "failed")}
    still = [r for r in failed if r["id"] in open_ids]
    if failed:
        lines.append(f"failed, not archived ({len(still)} of {len(failed)} in the last {hours:g} h): "
                     + (", ".join(f"{r['id']} (exit {r.get('exit_code')}, figures {r.get('figures_exit')})" for r in still)
                        or "none"))  # fmt: skip
    return "\n".join(lines) + "\n"


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
    eq.add_argument("--reuse-names", action="store_true", help="queue although a --name exists in the box's results/")
    sub.add_parser("status").add_argument("--json", action="store_true")
    sub.add_parser("pull")
    sub.add_parser("cancel").add_argument("id")
    sub.add_parser("archive", help="move finished jobs' records out of the status listing (ledger unchanged)")
    sw = sub.add_parser("start-worker")
    w = sub.add_parser("worker")
    w.add_argument("--once", action="store_true")
    for p in (sw, w):
        g = p.add_mutually_exclusive_group()
        g.add_argument("--gpu", type=int, default=0, help="the worker's one GPU")
        g.add_argument("--gpus", default=None, help="the worker's GPUs, e.g. 0,1: jobs with gpus: 2 run on both")
    sub.add_parser("box-status").add_argument("--json", action="store_true")
    sub.add_parser("box-ids")
    sub.add_parser("box-runs", help="the run dirs in the box's results/ (<exp>/<run>), as JSON")
    sub.add_parser("box-cancel").add_argument("id")
    sub.add_parser("box-archive")
    for name in ("stats", "box-stats"):
        st = sub.add_parser(name, help="counts, GPU-hours used and left, when the queue drains")
        st.add_argument("--hours", type=float, default=24.0, help="the window for done / failed / used")
        st.add_argument("--gpus", type=int, default=4)
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        return cmd_validate(a.specs)
    if a.cmd == "enqueue":
        return cmd_enqueue(a.specs, a.allow_dirty, a.reuse_names)
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
        return cmd_start_worker(gpu_list(a.gpus if a.gpus is not None else a.gpu))
    if a.cmd == "worker":
        worker(gpu_list(a.gpus if a.gpus is not None else a.gpu), once=a.once)
        return 0
    if a.cmd == "box-status":
        print(box_status(box_root(), a.json), end="")
        return 0
    if a.cmd == "box-ids":
        print(json.dumps(box_ids(box_root())))
        return 0
    if a.cmd == "box-runs":
        print(json.dumps(sorted(results_dirs(box_root() / "results"))))
        return 0
    if a.cmd == "box-cancel":
        print(box_cancel(box_root(), a.id), end="")
        return 0
    if a.cmd == "stats":
        try:
            _install_box_script()
            print(_ssh(f"python3 ~/{BOX_ROOT}/jobq.py box-stats --hours {a.hours} --gpus {a.gpus}"), end="")
        except subprocess.CalledProcessError:  # a deleted box (e.g. the 2x H200 after its queue) is not an error here
            print(f"{HOST}: unreachable (deleted or down); its pulled ledger: results/jobq/ledger_{HOST}.jsonl")
        return 0
    if a.cmd == "box-stats":
        print(box_stats(box_root(), a.hours, a.gpus), end="")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
