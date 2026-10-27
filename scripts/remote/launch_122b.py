"""A short Qwen3.5-122B-A10B session on a rented 1x H200 / B200 box, torn down by the provider's API (Dan, 23 Oct).

Run on the Mac. It waits for ssh, prepares the box (rsync / tmux / git / curl if missing, uv; checks the GPUs: >= 135 GB
in total, one H200 or 2x H100 80 GB, where every step then splits the model over them with BJ_DEVICE_MAP=auto; compute
capability >= 8.9 on each for FP8, driver CUDA >= 12.8; picks the writable disk with the most free space for the repo,
HF_HOME and the uv cache), uploads the working tree (tracked and untracked-not-ignored files, without results/ and .env:
no token goes to the box, the models are public) and starts a runner in tmux on the box: `uv sync --locked`, the model
(Qwen/Qwen3.5-122B-A10B-FP8 at the revision pinned in pins.TARGETS) and its J++ lens (sha256-checked), then the jobs, one
after another, each timed (seconds, peak GPU memory) so the rest can be priced. The Mac polls every 30 s and stops at:
all jobs done, the first failure (any step, the runner gone, the launcher's own error or Ctrl-C), or the hard wall limit
(default 2 h from launch; the box kills its job 10 min before it, so the copy-back fits). Then it copies the box's
results, logs and status.json to log/remote/qwen35_122b-<stamp>/, copies each new run dir into results/ (never over an
existing one) and runs $TERMINATE_CMD (the provider's API call; never `shutdown`), retried up to 5 times.

    export TERMINATE_CMD='curl -fsS -X DELETE -H "Authorization: Bearer $KEY" https://<provider>/instances/<id>'
    uv run python scripts/remote/launch_122b.py launch --host root@1.2.3.4 --port 22 --dry-run   # print every command
    uv run python scripts/remote/launch_122b.py launch --host root@1.2.3.4 --port 22
    uv run python scripts/remote/launch_122b.py attach --host root@1.2.3.4 --port 22   # the launcher died: re-attach

TERMINATE_CMD runs on the Mac with `sh -c` (curl -f: an HTTP error must exit non-zero, or a failed call passes as a
terminate). Key-based ssh only (BatchMode); a fresh known_hosts file per launch, so a reused IP does not block. Run the
launcher in a Mac tmux session, plugged in (caffeinate keeps the Mac awake while it runs). Ctrl-C (or SIGTERM / SIGHUP)
also copies back and terminates; to leave the box running, kill -9 the launcher and finish later with `attach`. Jobs
(--jobs picks and orders them): lens_gate = jobs/d1/qwen35_122b_lens_gate_v2.yaml's command; port_smoke =
scripts/port_smoke.py --name qwen35_122b_port_smoke. The launcher prints timings and progress bars, never a job's result
lines (the lens gate is unopened until Dan predicts). A run dir already in the Mac's results/ is never overwritten. On
the box: `tmux attach -t bj122` (the runner's lines), `tail -f <work>/logs/<step>.log` (a step's output). The box side
(box-*) is stdlib only (system python3), except box-fetch (uv run).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent  # .parent, not .parents[2]: the home copy on the box sits at ~/
TARGET = "qwen3.5-122b-a10b"
SESSION = WORK_NAME = "bj122"
POINTER = ".bj122.json"  # in the box user's home: {"work": <work dir>}, so `attach` and a re-prep find the work dir
DRY_WORK = "/BOX_DISK/bj122"  # --dry-run: stands for the work dir box-prep picks
LENS_GATE_SPEC = "jobs/d1/qwen35_122b_lens_gate_v2.yaml"
PORT_SMOKE = f"BJ_TARGET={TARGET} uv run python scripts/port_smoke.py --name qwen35_122b_port_smoke"
LIMIT_MIN = 120
RESERVE_S = 600  # the box's job is killed this long before the wall limit: copy-back and terminate fit in it
GRACE_S = 60  # the Mac waits this long past the box's own stop before it gives up on the box
POLL_S, WAIT_SSH_S = 30, 600
MIN_GPU_GIB, MIN_CC, MIN_DRIVER_CUDA, MIN_FREE_GB = 135, 8.9, (12, 8), 180  # FP8 weights ~125 GB on disk and GPU
TERMINAL = ("DONE", "FAIL", "ABORT_TIME", "DIED")
PSEUDO_FS = {"tmpfs", "devtmpfs", "ramfs", "proc", "sysfs", "cgroup", "cgroup2", "devpts", "mqueue", "securityfs",
             "debugfs", "tracefs", "pstore", "bpf", "configfs", "fusectl", "hugetlbfs", "autofs", "binfmt_misc",
             "squashfs", "nsfs", "efivarfs", "rpc_pipefs"}  # fmt: skip


class Failure(Exception):
    pass


def _jobq():
    """scripts.jobq's stdlib helpers (on the box: from the uploaded repo, not the home copy)."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from scripts import jobq

    return jobq


def box_steps(jobs: list[dict[str, str]]) -> list[dict[str, str]]:
    """What the box runner runs, in order, from the repo dir; the first failure stops it."""
    return [{"name": "uv_sync", "command": "uv sync --locked"},
            {"name": "fetch", "command": "uv run python scripts/remote/launch_122b.py box-fetch"}, *jobs]  # fmt: skip


def box_env(work: str, n_gpus: int = 1) -> dict[str, str]:
    """Added to the runner's environment for every step (PATH gets ~/.local/bin, where uv installs, in front). On
    several GPUs the model is split over them (BJ_DEVICE_MAP=auto): the memory check counts their total."""
    env = {"HF_HOME": f"{work}/hf", "UV_CACHE_DIR": f"{work}/uv-cache", "HF_XET_HIGH_PERFORMANCE": "1",
           "PYTHONUNBUFFERED": "1"}  # fmt: skip
    return {**env, "BJ_DEVICE_MAP": "auto"} if n_gpus > 1 else env


def gpu_problems(mem_gib: list[float], compute_caps: list[float]) -> list[str]:
    """The GPU checks of box-prep, per GPU's memory (GiB) and compute capability: the FP8 weights (~125 GB) and the
    lens need MIN_GPU_GIB in total over the GPUs (the model is split over several: box_env), and every GPU needs native
    FP8 (compute capability >= MIN_CC)."""
    if not mem_gib:
        return ["no GPU"]
    out = []
    if (total := round(sum(mem_gib), 1)) < MIN_GPU_GIB:
        out.append(f"the GPUs have {total} GiB in total ({len(mem_gib)} x {mem_gib[0]}) < {MIN_GPU_GIB}")
    if (cc := min(compute_caps)) < MIN_CC:
        out.append(f"compute capability {cc} < {MIN_CC}: no native FP8")
    return out


# ---------------------------------------------------------------- Mac side


class Log:
    def __init__(self, path: Path | None):
        self.path = path

    def say(self, msg: str) -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        with contextlib.suppress(OSError):  # a closed terminal must not stop the copy-back and the terminate
            print(line, flush=True)
        if self.path:
            with open(self.path, "a") as f:
                f.write(line + "\n")


class Remote:
    """ssh / scp / rsync to the box; with dry=True every command is printed and none is run (`fake` is returned)."""

    def __init__(self, host: str, port: int | None, known_hosts: Path, dry: bool, log: Log):
        self.host, self.dry, self.log = host, dry, log
        self.opts = ["-o", "BatchMode=yes", "-o", "ConnectTimeout=20", "-o", "ServerAliveInterval=15",
                     "-o", "ServerAliveCountMax=4", "-o", "StrictHostKeyChecking=accept-new",
                     "-o", f"UserKnownHostsFile={known_hosts}"]  # fmt: skip
        self.port = ["-p", str(port)] if port else []
        self.scp_port = ["-P", str(port)] if port else []

    def run(self, argv: list[str], timeout: float, fake: str = "", quiet: bool = False) -> str:
        if not quiet:
            self.log.say("$ " + shlex.join(argv))
        if self.dry:
            return fake
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            raise Failure(f"timed out after {timeout:.0f} s: {shlex.join(argv)[:300]}") from None
        if r.returncode:
            raise Failure(f"exit {r.returncode}: {shlex.join(argv)[:300]}\n{(r.stdout + r.stderr)[-1500:]}")
        return r.stdout

    def ssh(self, cmd: str, timeout: float, fake: str = "", quiet: bool = False) -> str:
        return self.run(["ssh", *self.opts, *self.port, self.host, cmd], timeout, fake, quiet)

    def scp(self, src: Path, dst: str, timeout: float = 120) -> None:
        self.run(["scp", "-q", *self.opts, *self.scp_port, str(src), f"{self.host}:{dst}"], timeout)

    def rsync(self, args: list[str], timeout: float) -> None:
        self.run(["rsync", "-a", "--timeout=60", "-e", shlex.join(["ssh", *self.opts, *self.port]), *args], timeout)


@contextlib.contextmanager
def phase(record: dict[str, Any], name: str):
    t = time.time()
    try:
        yield
    finally:
        record["phases"][name] = round(time.time() - t, 1)


def job_list(names: list[str]) -> list[dict[str, str]]:
    import yaml

    known = {"lens_gate": yaml.safe_load((REPO / LENS_GATE_SPEC).read_text())["command"], "port_smoke": PORT_SMOKE}
    if unknown := [n for n in names if n not in known]:
        raise SystemExit(f"unknown jobs {unknown}; known: {sorted(known)}")
    jobs = [{"name": n, "command": known[n]} for n in names]
    for j in jobs:
        assert j["command"].startswith(f"BJ_TARGET={TARGET} "), f"{j['name']}: not a {TARGET} command"
    return jobs


def upload_list() -> list[str]:
    """The working tree as git sees it (tracked + untracked-not-ignored, so .venv, cache/, log/ and .env stay here),
    without results/: the jobs read nothing there (lens_gate: data/tasks_v2; port_smoke: nothing)."""
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout  # fmt: skip
    files = sorted({f for f in out.split("\0") if f and not f.startswith("results/") and (REPO / f).is_file()})
    secret = [f for f in files if re.fullmatch(r"\.env(\..+)?", Path(f).name) and f != ".env.example"]
    assert not secret, f"refusing to upload {secret}"
    return files


def keep_awake(log: Log, dry: bool) -> None:
    if sys.platform != "darwin":
        return
    argv = ["caffeinate", "-is", "-w", str(os.getpid())]
    log.say("$ " + shlex.join(argv) + "   # background, ends with the launcher")
    if not dry:
        subprocess.Popen(argv)


def wait_for_ssh(box: Remote, log: Log) -> None:
    t, first = time.time(), True
    while True:
        try:
            box.ssh("true", 40, quiet=not first)
            return
        except Failure as e:
            if time.time() - t > WAIT_SSH_S:
                raise Failure(f"no ssh to {box.host} after {WAIT_SSH_S // 60} min: {e}") from None
            log.say(f"ssh not up yet ({str(e).splitlines()[-1][:120]}); retrying in 20 s")
            first = False
            time.sleep(20)


def status_cmd(work: str) -> str:
    return f"python3 {shlex.quote(work + '/bridge-jspace/scripts/remote/launch_122b.py')} box-status"


def watch(box: Remote, log: Log, work: str, stop_at: float) -> str:
    """Poll the runner until it ends or `stop_at` (Mac clock); returns the final state."""
    fmt = _jobq().fmt_duration
    t0, first = time.time(), True
    while time.time() < stop_at:
        try:
            out = box.ssh(status_cmd(work), 60, fake=json.dumps({"state": "DONE", "steps": []}), quiet=not first)
            st = json.loads(out)
            first = False
        except (Failure, ValueError) as e:
            log.say(f"poll failed: {str(e)[:200]}")
            time.sleep(POLL_S)
            continue
        state, now_b = st.get("state"), st.get("now", 0.0)
        if state in TERMINAL:
            log.say(f"box: {state} at {st.get('at', '-')}")
            return state
        if state == "STARTING":
            if time.time() - t0 > 180:
                log.say("the runner did not write status.json within 3 min (see logs/runner.log)")
                return "DIED"
        else:
            el, left = now_b - st.get("at_since_epoch", now_b), st.get("deadline_epoch", now_b) - now_b
            log.say(f"{state} {st.get('at', '-')} {fmt(el)} (box budget left {fmt(left)}) | {st.get('progress', '')}")
        time.sleep(POLL_S)
    log.say("wall limit reached on the Mac")
    return "ABORT_TIME"


def copy_back(box: Remote, log: Log, dest: Path, work: str, dry: bool) -> None:
    """Results first (they matter most), then logs and status; each rsync bounded, a failure logged, never raised."""
    pairs = ((f"{work}/bridge-jspace/results/", dest / "results"), (f"{work}/logs/", dest / "logs"),
             (f"{work}/status.json", dest / "status.json"))  # fmt: skip
    for src, dst in pairs:
        if not dry and src.endswith("/"):
            dst.mkdir(parents=True, exist_ok=True)
        try:
            box.rsync([f"{box.host}:{src}", f"{dst}/" if src.endswith("/") else str(dst)], timeout=150)
        except Failure as e:
            log.say(f"copy-back of {src} failed: {str(e)[:300]}")
    if dry:
        log.say(f"then: each run dir {dest.relative_to(REPO)}/results/<exp>/<run> not yet in results/ is copied there")
        return
    for run in sorted((dest / "results").glob("*/*")):
        if not run.is_dir():
            continue
        target = REPO / "results" / run.parent.name / run.name
        if target.exists():
            log.say(f"kept the local {target.relative_to(REPO)}; the box's run is in {run.relative_to(REPO)}")
        else:
            shutil.copytree(run, target)
            log.say(f"new run: {target.relative_to(REPO)}")


def terminate(log: Log, term: str, dry: bool) -> bool:
    shown = '$ sh -c "$TERMINATE_CMD"'  # never its value: it may hold the provider's key
    if dry:
        log.say(f"{shown}   # TERMINATE_CMD {'set' if term else 'UNSET: a real launch refuses to start'}")
        return True
    for i in range(1, 6):
        log.say(f"{shown}   # attempt {i}/5")
        try:
            r = subprocess.run(["sh", "-c", term], capture_output=True, text=True, timeout=120, check=False)
        except subprocess.TimeoutExpired:
            log.say("TERMINATE_CMD timed out")
        else:
            tail = (r.stdout + r.stderr).strip()[-300:]
            if r.returncode == 0:
                log.say(f"terminated (TERMINATE_CMD exit 0) {tail}")
                return True
            log.say(f"TERMINATE_CMD exit {r.returncode}: {tail}")
        time.sleep(20)
    log.say("!! TERMINATE FAILED 5 times: terminate the instance by hand NOW")
    return False


def summary(log: Log, record: dict[str, Any], status: Path) -> None:
    st = json.loads(status.read_text()) if status.exists() else {}
    log.say(f"timing (for pricing; GPU {st.get('gpu') or record.get('box', {}).get('gpu', {}).get('name', '?')}):")
    for name, s in record["phases"].items():
        log.say(f"  mac  {name:<12} {s:>7.0f} s")
    for s in st.get("steps", []):
        log.say(f"  box  {s['step']:<12} {s['seconds']:>7.0f} s  exit {s['exit']}  peak GPU {s['peak_mem_gb']} GB")
    log.say(f"  launch to terminate: {record['total_s']:.0f} s; outcome {record['outcome']}")


def _interrupt(signum, frame):
    raise KeyboardInterrupt


def cmd_launch(a: argparse.Namespace) -> int:
    attach = a.cmd == "attach"
    t0 = time.time()
    deadline = t0 + a.limit_min * 60 if not attach else 0.0
    term = os.environ.get("TERMINATE_CMD", "")
    if not term and not a.dry_run:
        raise SystemExit("set TERMINATE_CMD (the provider's terminate API call) first; nothing was started")
    jobs = [] if attach else job_list(a.jobs.split(","))
    dest = REPO / "log" / "remote" / f"qwen35_122b-{time.strftime('%Y%m%d-%H%M%S')}"
    if not a.dry_run:
        dest.mkdir(parents=True)
    log = Log(None if a.dry_run else dest / "launcher.log")
    box = Remote(a.host, a.port, dest / "known_hosts", a.dry_run, log)
    jq = _jobq()
    os.environ["BJ_TARGET"] = TARGET  # before the pins import
    from bridge_jspace import pins

    record: dict[str, Any] = {
        "mode": a.cmd, "launched": jq.now(), "host": a.host, "port": a.port, "commit": jq._git("rev-parse", "HEAD"),
        "dirty": jq._git("status", "--porcelain").splitlines(), "limit_min": None if attach else a.limit_min,
        "pins": {"target": TARGET, "repo": pins.MODEL_REPO, "revision": pins.MODEL_REVISION,
                 "lens": list(pins.LENS_SOURCES[pins.FROZEN_LENS]), "lens_sha256": pins.FROZEN_LENS_SHA256},
        "phases": {}, "jobs": jobs,
    }  # fmt: skip
    if not a.dry_run:
        (dest / "launch.json").write_text(json.dumps(record, indent=1) + "\n")
    log.say(
        f"{a.cmd} {TARGET} ({pins.MODEL_REPO}@{pins.MODEL_REVISION[:8]}) on {a.host}; local dir {dest.relative_to(REPO)}"
    )
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, _interrupt)
    keep_awake(log, a.dry_run)
    work, outcome = None, "LAUNCHER_ERROR"
    try:
        with phase(record, "wait_ssh"):
            wait_for_ssh(box, log)
        if attach:
            work = json.loads(box.ssh(f"cat {POINTER}", 30, fake=json.dumps({"work": DRY_WORK})))["work"]
            st = json.loads(box.ssh(status_cmd(work), 60, fake=json.dumps({"now": 0.0})))
            deadline = time.time() + st.get("deadline_epoch", st["now"]) - st["now"] + RESERVE_S
        else:
            with phase(record, "prep"):
                box.scp(Path(__file__).resolve(), "launch_122b.py")
                disk = f" --disk {shlex.quote(a.disk)}" if a.disk else ""
                fake = {"work": DRY_WORK, "problems": [], "session": False, "gpu": {"name": "(dry run)"}}
                out = box.ssh(f"python3 launch_122b.py box-prep{disk}", 900, fake=json.dumps(fake))
                probe = json.loads(out.strip().splitlines()[-1])
                record["box"] = probe
                log.say(f"box: {json.dumps(probe)}")
                if probe.get("session"):
                    log.say(f"a {SESSION} tmux session already runs on the box: use `attach` (nothing terminated)")
                    return 2
                work = probe["work"]
                if probe["problems"]:
                    raise Failure("box: " + "; ".join(probe["problems"]))
            with phase(record, "upload"):
                files = upload_list()
                listing = dest / "upload.txt"
                if not a.dry_run:
                    listing.write_text("\n".join(files) + "\n")
                    (dest / "jobs.json").write_text(json.dumps(jobs, indent=1) + "\n")
                size = sum((REPO / f).stat().st_size for f in files) / 1e6
                log.say(f"upload: {len(files)} files, {size:.0f} MB (git's view of the tree; no results/, no .env)")
                box.rsync([f"--files-from={listing}", f"{REPO}/", f"{a.host}:{work}/bridge-jspace/"], timeout=1200)
                box.rsync([str(dest / "jobs.json"), f"{a.host}:{work}/jobs.json"], timeout=120)
            budget = int(deadline - RESERVE_S - time.time())
            if budget < 600:
                raise Failure(f"only {budget} s left for the box")
            script = f"{work}/bridge-jspace/scripts/remote/launch_122b.py"
            inner = (f"{shlex.join(['python3', script, 'box-run', '--budget-s', str(budget)])} 2>&1 | "
                     f"tee -a {shlex.quote(work + '/logs/runner.log')}; exec bash")  # fmt: skip
            box.ssh(shlex.join(["tmux", "new-session", "-d", "-s", SESSION, "-c", f"{work}/bridge-jspace", inner]), 60)
            env = " ".join(f"{k}={v}" for k, v in box_env(work, record["box"]["gpu"].get("n", 1)).items())
            log.say(f"box runner (cwd {work}/bridge-jspace; {env}; PATH=~/.local/bin:$PATH), budget {budget} s:")
            for s in box_steps(jobs):
                log.say(f"  {s['name']}: {s['command']}")
            port = f" -p {a.port}" if a.port else ""
            log.say(f"watch: ssh{port} {a.host} -t tmux attach -t {SESSION}   |   tail -f {work}/logs/<step>.log")
        with phase(record, "run"):
            outcome = watch(box, log, work, deadline - RESERVE_S + GRACE_S)
    except Failure as e:
        log.say(f"FAIL: {e}")
        outcome = "FAIL"
    except KeyboardInterrupt:
        log.say("interrupted: copying back and terminating")
        outcome = "INTERRUPTED"
    except Exception:
        log.say(f"launcher error:\n{traceback.format_exc()}")
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):  # the finish is bounded by timeouts: let it complete
        signal.signal(sig, signal.SIG_IGN)
    log.say(f"finishing ({outcome}): copy-back, then TERMINATE_CMD; Ctrl-C is ignored from here")
    if work:
        with phase(record, "copy_back"):
            copy_back(box, log, dest, work, a.dry_run)
    terminated = terminate(log, term, a.dry_run)
    record.update(outcome=outcome, terminated=terminated, ended=jq.now(), total_s=round(time.time() - t0, 1))
    if not a.dry_run:
        (dest / "launch.json").write_text(json.dumps(record, indent=1) + "\n")
    summary(log, record, dest / "status.json")
    log.say(f"everything from the box: {dest.relative_to(REPO)}/")
    return 0 if outcome == "DONE" and terminated else 1


# ---------------------------------------------------------------- box side (stdlib only, system python3)


def _biggest_disk() -> tuple[Path, dict[str, float]]:
    """The writable dir with the most free space: home, or a real mount (one candidate per device, home first)."""
    cands = [Path.home()]
    with contextlib.suppress(OSError):
        for line in Path("/proc/mounts").read_text().splitlines():
            parts = line.split()
            # fuse: object-store mounts (s3fs, ...) report huge free space and would make loading 125 GB crawl
            if len(parts) < 3 or parts[2] in PSEUDO_FS or parts[2].startswith("fuse"):
                continue
            mnt = parts[1].replace("\\040", " ")
            if not mnt.startswith(("/proc", "/sys", "/dev", "/run", "/boot", "/snap", "/etc", "/usr")):
                cands.append(Path(mnt))
    seen: dict[int, tuple[float, Path]] = {}
    for c in cands:
        try:
            if c.is_dir() and os.access(c, os.W_OK) and os.stat(c).st_dev not in seen:
                seen[os.stat(c).st_dev] = (shutil.disk_usage(c).free / 1e9, c)
        except OSError:
            continue
    free = {str(c): round(f, 1) for f, c in seen.values()}
    return (max(seen.values())[1] if seen else Path.home()), free


def box_prep(disk: str | None) -> int:
    """Tools, uv, GPU and disk checks, the work dir. Runs from ~/launch_122b.py before the repo is on the box; its
    last stdout line is JSON: work, problems (non-empty = the box is unusable), session (a runner already exists)."""
    err, problems = sys.stderr, []
    missing = [t for t in ("rsync", "tmux", "git", "curl") if not shutil.which(t)]
    if missing:
        if os.geteuid() != 0 and not shutil.which("sudo"):
            problems.append(f"missing {missing}, and no root or sudo to install them")
        else:
            apt = [*([] if os.geteuid() == 0 else ["sudo", "-n"]), "env", "DEBIAN_FRONTEND=noninteractive", "apt-get"]
            subprocess.run([*apt, "update", "-qq"], stdout=err, stderr=err, check=False)
            subprocess.run([*apt, "install", "-y", "-qq", *missing], stdout=err, stderr=err, check=False)
            if still := [t for t in missing if not shutil.which(t)]:
                problems.append(f"missing {still} (apt-get failed)")
    uv = shutil.which("uv") or shutil.which("uv", path=str(Path.home() / ".local" / "bin"))
    if not uv and shutil.which("curl"):
        subprocess.run(
            "curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True, stdout=err, stderr=err, check=False
        )
        uv = shutil.which("uv", path=str(Path.home() / ".local" / "bin"))
    if not uv:
        problems.append("uv not installed")
    gpu: dict[str, Any] = {}
    try:
        q = ["nvidia-smi", "--query-gpu=name,memory.total,compute_cap,driver_version", "--format=csv,noheader,nounits"]
        rows = subprocess.run(q, capture_output=True, text=True, check=True, timeout=60).stdout.strip().splitlines()
        each = [[x.strip() for x in r.split(",")] for r in rows]
        name, driver = each[0][0], each[0][3]
        mem, ccs = [round(float(r[1]) / 1024, 1) for r in each], [float(r[2]) for r in each]
        cuda = re.search(r"CUDA (?:UMD )?Version:\s*(\d+)\.(\d+)", subprocess.run(["nvidia-smi"], capture_output=True,
                         text=True, check=False, timeout=60).stdout)  # fmt: skip
        gpu = {"name": name, "n": len(rows), "mem_gib": round(sum(mem), 1), "mem_gib_each": mem,
               "compute_cap": min(ccs), "driver": driver, "driver_cuda": f"{cuda[1]}.{cuda[2]}" if cuda else None}  # fmt: skip
        problems += gpu_problems(mem, ccs)
        if not cuda or (int(cuda[1]), int(cuda[2])) < MIN_DRIVER_CUDA:
            problems.append(f"driver CUDA {gpu['driver_cuda']} < 12.8 (torch is cu128)")
    except (OSError, subprocess.SubprocessError, ValueError, IndexError) as e:
        problems.append(f"nvidia-smi: {e}")
    pointer = Path.home() / POINTER
    base, free = (Path(disk), {}) if disk else _biggest_disk()
    old = json.loads(pointer.read_text())["work"] if pointer.exists() else None
    work = Path(old) if old and Path(old).is_dir() else base / WORK_NAME
    (work / "logs").mkdir(parents=True, exist_ok=True)
    pointer.write_text(json.dumps({"work": str(work)}) + "\n")
    free_gb = shutil.disk_usage(work).free / 1e9
    if free_gb < MIN_FREE_GB and not (work / "hf").exists():
        problems.append(f"{work}: {free_gb:.0f} GB free < {MIN_FREE_GB} (candidates {free}; pass --disk)")
    session = bool(shutil.which("tmux")) and subprocess.run(["tmux", "has-session", "-t", SESSION],
                                                            capture_output=True, check=False).returncode == 0  # fmt: skip
    print(json.dumps({"work": str(work), "free_gb": round(free_gb), "disks": free, "gpu": gpu, "uv": uv,
                      "session": session, "problems": problems}))  # fmt: skip
    return 0


def _kill_group(p: subprocess.Popen) -> None:
    for sig, wait in ((signal.SIGTERM, 30), (signal.SIGKILL, 10)):
        try:
            os.killpg(p.pid, sig)
        except ProcessLookupError:
            return
        try:
            p.wait(wait)
            return
        except subprocess.TimeoutExpired:
            continue


def box_run(budget_s: float) -> int:
    """The steps in order, each in its own process group with its log in <work>/logs/<step>.log; status.json after
    each change. Stops at the first non-zero exit or at the budget (the job is killed: ABORT_TIME)."""
    jq = _jobq()
    work = REPO.parent
    jobs = json.loads((work / "jobs.json").read_text())
    gpus = jq.box_gpus()
    env = {**os.environ, **box_env(str(work), len(gpus))}
    env["PATH"] = f"{Path.home() / '.local' / 'bin'}:{os.environ.get('PATH', '')}"
    status: dict[str, Any] = {"state": "RUNNING", "pid": os.getpid(), "started": jq.now(), "gpu": jq.gpu_query(0, "name"),
                              "deadline_epoch": time.time() + budget_s, "steps": []}  # fmt: skip

    def save(state: str, **kw: Any) -> None:
        status.update(state=state, **kw)
        jq.write_json_atomic(work / "status.json", status)

    save("RUNNING")
    for step in box_steps(jobs):
        log = work / "logs" / f"{step['name']}.log"
        print(f"[{jq.now()}] start {step['name']}: {step['command']}", flush=True)
        t, peak, killed, started = time.time(), 0.0, False, jq.now()
        with open(log, "a") as f:
            p = subprocess.Popen(["bash", "-c", step["command"]], cwd=REPO, env=env, stdout=f,
                                 stderr=subprocess.STDOUT, start_new_session=True)  # fmt: skip
            save("RUNNING", at=step["name"], at_since_epoch=t)
            while p.poll() is None:
                if time.time() > status["deadline_epoch"]:
                    _kill_group(p)
                    killed = True
                    break
                used = [jq.gpu_query(g, "memory.used") for g in gpus]  # the total over the GPUs
                peak = max(peak, sum(float(u) for u in used if u) / 1024) if all(used) else peak
                time.sleep(10)
        status["steps"].append({"step": step["name"], "command": step["command"], "started": started,
                                "seconds": round(time.time() - t, 1), "exit": p.returncode,
                                "peak_mem_gb": round(peak, 1), "log": f"logs/{log.name}"})  # fmt: skip
        print(f"[{jq.now()}] {step['name']}: exit {p.returncode}, {jq.fmt_duration(time.time() - t)}", flush=True)
        if killed or p.returncode:
            save("ABORT_TIME" if killed else "FAIL")
            return 1
        save("RUNNING")
    save("DONE")
    return 0


def box_fetch() -> int:
    """The pinned model snapshot and the target's lens files into HF_HOME (retrying on HF 429s); the frozen lens's
    sha256 is checked here, so a bad file stops the session before any job loads the model."""
    os.environ["BJ_TARGET"] = TARGET  # before the pins import
    _jobq()  # the repo root on sys.path, for scripts.prefetch
    from huggingface_hub import hf_hub_download, snapshot_download

    from bridge_jspace import pins
    from bridge_jspace.lens import check_frozen
    from scripts.prefetch import with_retries

    t = time.time()
    snap = with_retries(lambda: snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION), pins.MODEL_REPO)
    assert snap, pins.MODEL_REPO  # with_retries raises after its last attempt; never None in practice
    size = sum(f.stat().st_size for f in Path(snap).rglob("*") if f.is_file()) / 1e9
    print(f"{pins.MODEL_REPO}@{pins.MODEL_REVISION[:8]}: {size:.1f} GB in {time.time() - t:.0f} s", flush=True)
    for name, (repo, file, rev) in pins.LENS_SOURCES.items():
        if repo == "local":
            continue
        got = with_retries(lambda r=repo, f=file, v=rev: hf_hub_download(r, f, revision=v), name)
        assert got, name
        lens = Path(got)
        if name == pins.FROZEN_LENS:
            check_frozen(lens)
        print(f"lens {name}: {file} ({lens.stat().st_size / 1e9:.1f} GB)", flush=True)
    return 0


def box_status() -> int:
    jq = _jobq()
    work = REPO.parent
    path = work / "status.json"
    st: dict[str, Any] = json.loads(path.read_text()) if path.exists() else {"state": "STARTING"}
    if st["state"] == "RUNNING" and not jq._alive(st["pid"]):
        st["state"] = "DIED"
    if st.get("at"):
        line = jq.last_progress(work / "logs" / f"{st['at']}.log")
        # a job's last line can be its result (lens_gate prints its verdict, unopened until Dan predicts): only a
        # progress bar is shown for jobs; the setup steps may show any last line
        setup = st["at"] in ("uv_sync", "fetch")
        st["progress"] = line if setup or jq.PROGRESS_RE.search(line) or "ETA" in line else "(running)"
    st["now"] = time.time()
    print(json.dumps(st))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("launch", "attach"):
        p = sub.add_parser(name, help="set up, run, copy back, terminate" if name == "launch" else "re-attach")
        p.add_argument("--host", required=True, help="ssh destination: user@ip or an ~/.ssh/config alias")
        p.add_argument("--port", type=int, help="ssh port, if not 22 and not in ~/.ssh/config")
        p.add_argument("--dry-run", action="store_true", help="print every command; run none, write nothing")
        if name == "launch":
            p.add_argument("--jobs", default="lens_gate,port_smoke", help="comma-separated, in order")
            p.add_argument("--limit-min", type=float, default=LIMIT_MIN, help="hard wall limit from launch")
            p.add_argument("--disk", help="the box's large disk (default: the writable one with the most free space)")
    sub.add_parser("box-prep").add_argument("--disk")
    sub.add_parser("box-run").add_argument("--budget-s", type=float, required=True)
    sub.add_parser("box-fetch")
    sub.add_parser("box-status")
    a = ap.parse_args(argv)
    if a.cmd in ("launch", "attach"):
        return cmd_launch(a)
    if a.cmd == "box-prep":
        return box_prep(a.disk)
    if a.cmd == "box-run":
        return box_run(a.budget_s)
    if a.cmd == "box-fetch":
        return box_fetch()
    return box_status()


if __name__ == "__main__":
    sys.exit(main())
