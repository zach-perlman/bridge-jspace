"""h200q: Qwen3.5-122B-A10B's job queue on the 2x H200 box after the Qwen3-32B J++ fit, then the box deleted (Dan, 23 Oct
~00:35). Runs on the Mac (the Sesterce key stays here), in tmux session h200q under caffeinate -i:

    caffeinate -i uv run python scripts/remote/h200q_watchdog.py   # log: log/remote/h200q_watchdog.log
    uv run python scripts/remote/h200q_watchdog.py --check         # every condition once; starts and deletes nothing
    uv run python scripts/remote/h200q_watchdog.py --last-batch    # say the last batch of 122B specs is committed

The queue is jobq's (scripts/jobq.py) on the box sesterce-h200x2 (~/jobq; jobs enqueued from the Mac with
JOBQ_HOST=sesterce-h200x2). This script starts its workers, enqueues new 122B specs, pulls, and ends the box:
0. Every 5 min (from the start, workers or not): every committed jobs/*/qwen35_122b_*.yaml not yet in the queue (the
   committed version: a spec with uncommitted edits waits), valid, and not superseded by a committed _rN of it (a
   pending job superseded later is cancelled) is enqueued, lens-free specs first, the lens stages (their command runs
   scripts/d1_precheck.py) after them. All of them queue behind the gate, which runs alone (see 1).
1. Start: wait (every 2 min) until the fit's ~/work/fit32b/status.json is terminal, the Mac's tmux session h200finish has
   ended (it saves the fit's lens to the Mac), the 122B prefetch printed PREFETCH_DONE with its lens sha256 ok, and
   nvidia-smi shows both GPUs free. Then jobq's worker for GPU 0 (tmux jobq-gpu0 on the box); the worker for GPU 1 once
   the lens gate (first in the queue) is done: the gate before any other 122B job. One job per GPU (FP8 122B ~127 GB).
   Workers run with HF_HOME=~/work/hf (the prefetched weights and lens), UV_CACHE_DIR=~/work/uv-cache, and jobq's
   free-memory check off: an idle H200 shows 143771 - 616 MiB = 139.8 GiB free, under the specs' mem_gb 140, so the
   check would hold every job forever; nothing else runs on these GPUs once the fit is over. A restarted watchdog
   takes worker sessions already on the box as started.
2. Every minute the queue's state; every 5 min jobq's pull (new run dirs into results/, this box's ledger and queue
   state as results/jobq/ledger_sesterce-h200x2.jsonl and cache/jobq/queue_state_sesterce-h200x2.json, drafts, logs).
3. Final when the queue is finished (nothing running; every pending job waits on a failed one) after the last batch is
   in (--last-batch wrote cache/jobq/h200q_last_batch, or no new spec was enqueued while the queue sat finished for
   1 h), the lens gate or the port smoke job failed (other failures are logged and the queue goes on), or at 09:50 UTC
   (Dan, 23 Oct ~00:55: the hard limit is 10:00 UTC).
4. The final (Dan's rule: delete ONLY after everything is verified on the Mac, at the hard limit too): pending jobs are
   cancelled (nothing new starts); then up to 3 tries of: jobq's pull; `rsync -a --ignore-existing
   sesterce-h200x2:jobq/results/ results/` (fills files missing here, never overwrites one); ~/work/fit32b's small
   files and ~/work/prefetch_122b.log into log/remote/; and the checks: every file under the box's ~/jobq/results is
   under results/ with its size; the local ledger_sesterce-h200x2.jsonl has as many lines as the box's ledger.jsonl;
   every run's log.txt is under log/jobq/ (same size unless the job still runs); the 32B fit's files are here (its
   status copy in results/lens_fit/, and if DONE the lens with the box's sha256). Only when all pass:
   scripts/lens_fit/h200_finish.py --terminate-only (the checked DELETE). Otherwise NOT deleted: an ACTION line in the
   log for the hourly check, and the final is retried every 10 min until 2 h after the limit, then the box is left up.
   Ctrl-C stops the watchdog only: no pull, no delete.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shlex
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts import jobq as jq

HOST = "sesterce-h200x2"
jq.HOST = HOST  # jobq's Mac-side helpers (and its per-box ledger name) read it at call time
REPO = jq.REPO
GATE, PORT = "qwen35_122b_lens_gate_v2", "qwen35_122b_port_smoke"
LIMIT = dt.datetime(2026, 10, 23, 10, 0, tzinfo=dt.UTC)
FINAL_AT = LIMIT - dt.timedelta(minutes=10)
GIVE_UP = LIMIT + dt.timedelta(hours=2)
WAIT_S, POLL_S, PULL_S, RETRY_S, IDLE_S = 120, 60, 300, 600, 3600
LOG = REPO / "log" / "remote" / "h200q_watchdog.log"
LAST_BATCH = REPO / "cache" / "jobq" / "h200q_last_batch"  # written by --last-batch
LEDGER = REPO / "results" / "jobq" / f"ledger_{HOST}.jsonl"  # jobq pull's name for this box's ledger
FIT_COPY = REPO / "log" / "remote" / "h200_fit32b"
FIT_LENS = REPO / "cache" / "qwen3-32b" / "lenses" / "jpp" / "Qwen3-32B_jpp_lens.pt"
SPEC_RE = re.compile(r"jobs/[^/]+/(qwen35_122b_[a-z0-9_]+)\.yaml")
RANK_RE = re.compile(r"^(.*?)(?:_r(\d+))?$")
WORKER = ("export HF_HOME=$HOME/work/hf UV_CACHE_DIR=$HOME/work/uv-cache; python3 -c {code} 2>&1 | "
          "tee -a ~/jobq/worker-gpu{gpu}.log; exec bash")  # fmt: skip
WORKER_CODE = (
    'import os, sys; sys.path.insert(0, os.path.expanduser("~/jobq")); import jobq; jobq.worker({gpu}, check_mem=False)'
)
WRITE_LOG = True
REJECTED: set[str] = set()  # specs that failed validation (said once)


def now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def say(msg: str) -> None:
    line = f"[{now():%H:%M:%S}Z] {msg}"
    print(line, flush=True)
    if WRITE_LOG:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a") as f:
            f.write(line + "\n")


def run(argv: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False, cwd=REPO)
    except (subprocess.TimeoutExpired, OSError):
        return None


def box(cmd: str, timeout: float = 120) -> str | None:
    """stdout of one command on the box, None if ssh or the command failed."""
    r = run(["ssh", HOST, cmd], timeout)
    return r.stdout if r is not None and r.returncode == 0 else None


def fit_status() -> dict[str, Any] | None:
    out = box("cat ~/work/fit32b/status.json")
    try:
        return json.loads(out) if out else None
    except ValueError:
        return None


def terminal(state: str | None) -> bool:
    return state in ("DONE", "FAIL") or (state or "").startswith("ABORT")


def start_condition() -> tuple[bool, str]:
    s = fit_status()
    fit_over = s is not None and terminal(s.get("state"))
    r = run(["tmux", "has-session", "-t", "h200finish"], 30)
    finish_gone = r is not None and r.returncode != 0
    prefetch = box("cat ~/work/prefetch_122b.log") or ""
    prefetched = "PREFETCH_DONE" in prefetch and "sha256 ok" in prefetch
    used = box("nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits")
    apps = box("nvidia-smi --query-compute-apps=pid --format=csv,noheader")
    try:
        mib = [float(x) for x in (used or "").split()]
    except ValueError:
        mib = []
    free = len(mib) == 2 and max(mib) < 1024 and apps is not None and not apps.strip()
    why = (f"fit {s.get('state') if s else '?'}; h200finish {'ended' if finish_gone else 'running'}; prefetch "
           f"{'done' if prefetched else 'not done'}; GPU MiB used {mib or '?'}, GPU processes "
           f"{len((apps or '').split()) if apps is not None else '?'}")  # fmt: skip
    return fit_over and finish_gone and prefetched and free, why


def worker_running(gpu: int) -> bool:
    return box(f"tmux has-session -t jobq-gpu{gpu}") is not None


def start_worker(gpu: int) -> bool:
    inner = WORKER.format(code=shlex.quote(WORKER_CODE.format(gpu=gpu)), gpu=gpu)
    cmd = shlex.join(["tmux", "new-session", "-d", "-s", f"jobq-gpu{gpu}", "bash", "-c", inner])
    ok = box(f"tmux has-session -t jobq-gpu{gpu} 2>/dev/null || {cmd}") is not None
    say(f"worker GPU {gpu}: {'started' if ok else 'FAILED to start'} (ssh {HOST} -t tmux attach -t jobq-gpu{gpu})")
    return ok


def queue() -> dict[str, Any] | None:
    """Running and pending jobs, each job's last ledger status, and the pending jobs that can still run."""
    st = box("python3 ~/jobq/jobq.py box-status --json")
    led = box("cat ~/jobq/ledger.jsonl 2>/dev/null; true")
    if st is None or led is None:
        return None
    try:
        state = json.loads(st)
        status = {r["id"]: r["status"] for r in (json.loads(x) for x in led.splitlines() if x.strip())}
    except (ValueError, KeyError):
        return None
    running = {r["id"]: r.get("progress", "") for r in state["running"]}
    pending = {r["id"]: r.get("depends_on", []) for r in state["pending"]}
    live = live_pending(status, set(running), pending)
    return {"running": running, "pending": sorted(pending), "live": sorted(live), "status": status}


def live_pending(status: dict[str, str], running: set[str], pending: dict[str, list[str]]) -> set[str]:
    """The pending jobs that can still run: each dependency done, running, or itself pending and able to run (a
    failed, cancelled or never-enqueued dependency blocks the job and everything behind it)."""
    live: set[str] = set()
    grew = True
    while grew:
        grew = False
        for i, deps in pending.items():
            if i not in live and all(status.get(d) == "done" or d in running or d in live for d in deps):
                live.add(i)
                grew = True
    return live


def rank(job_id: str) -> tuple[str, int]:
    """(base id, N) for an id ending in _rN; a plain id is _r1."""
    m = RANK_RE.fullmatch(job_id)
    return (m[1], int(m[2] or 1)) if m else (job_id, 1)


def new_specs(queued: set[str]) -> tuple[list[tuple[str, Path]], set[str]]:
    """The committed 122B specs to enqueue, lens-free first (a lens stage runs d1_precheck.py), and the superseded ids
    (a committed _rN of a higher N exists). A spec with uncommitted edits waits for its commit."""
    tracked = run(["git", "ls-files", "jobs"], 60)
    edited = run(["git", "status", "--porcelain", "--", "jobs"], 60)
    if tracked is None or edited is None or tracked.returncode or edited.returncode:
        return [], set()
    changed = {line[3:].strip() for line in edited.stdout.splitlines()}
    specs = [(m[1], REPO / p) for p in tracked.stdout.split() if (m := SPEC_RE.fullmatch(p)) and p not in changed]
    best: dict[str, int] = {}
    for i, _ in specs:
        base, n = rank(i)
        best[base] = max(best.get(base, 0), n)
    superseded = {i for i, _ in specs if rank(i)[1] < best[rank(i)[0]]}
    out: list[tuple[bool, str, Path]] = []
    for i, p in specs:
        if i in queued or i in superseded or i in REJECTED:
            continue
        spec = jq.load_spec(p)
        if errors := jq.validate(spec, p):
            say(f"not enqueued {p.relative_to(REPO)}: {'; '.join(errors)}")
            REJECTED.add(i)
            continue
        out.append(("d1_precheck.py" in spec["command"], i, p))
    out.sort(key=lambda x: x[0])  # stable: lens-free first, then the lens stages, each in path order
    return [(i, p) for _, i, p in out], superseded


def enqueue_new(pending: list[str]) -> int:
    """Enqueue the new committed 122B specs (jobq enqueue --allow-dirty: the jobs run the committed tree) and cancel
    pending jobs a committed _rN superseded. Returns how many were enqueued."""
    ids = box("python3 ~/jobq/jobq.py box-ids")
    if ids is None:
        return 0
    new, superseded = new_specs(set(json.loads(ids)))
    for i in sorted(superseded & set(pending)):
        say(f"cancel {i}: superseded by a committed _rN")
        jq.cmd_cancel(i)
    if not new:
        return 0
    try:
        jq.cmd_enqueue([p for _, p in new], allow_dirty=True)
    except (SystemExit, subprocess.CalledProcessError) as e:
        say(f"enqueue of {[i for i, _ in new]} failed: {e}")
        return 0
    say(f"enqueued {len(new)}: {', '.join(i for i, _ in new)}")
    return len(new)


def pull() -> bool:
    """jobq's pull for this box (new run dirs, ledger, queue state, drafts, logs)."""
    try:
        jq.cmd_pull()
        return True
    except (subprocess.CalledProcessError, OSError) as e:
        say(f"pull failed: {e}")
        return False


def fill_and_copy() -> list[str]:
    """The final's copies besides jobq's pull: files missing here from the box's results (never overwriting one), the
    fit's small files and the prefetch log. Returns the failures."""
    FIT_COPY.mkdir(parents=True, exist_ok=True)
    copies = {
        "results (--ignore-existing)": ["rsync", "-a", "--ignore-existing", f"{HOST}:jobq/results/", f"{REPO / 'results'}/"],
        "fit32b small files": ["rsync", "-a", "--include=*.log", "--include=*.json", "--include=*.csv", "--include=*.txt",
                               "--exclude=*", f"{HOST}:work/fit32b/", f"{FIT_COPY}/"],
        "prefetch log": ["rsync", "-a", f"{HOST}:work/prefetch_122b.log", str(REPO / "log" / "remote" / "prefetch_122b.log")],
    }  # fmt: skip
    failed = []
    for name, argv in copies.items():
        r = run(argv, 1800)
        if r is None or r.returncode:
            failed.append(f"copy of {name}: {(r.stderr.strip() if r else 'timed out')[-200:]}")
    return failed


def lines(text: str) -> int:
    return sum(1 for x in text.splitlines() if x.strip())


def verify(running: set[str]) -> list[str]:
    """Dan's checks before the delete; [] when everything is on the Mac."""
    problems: list[str] = []
    out = box("cd ~/jobq/results && find . -type f -printf '%P\\t%s\\n'", 300)
    if out is None:
        problems.append("the box's results list did not come")
    else:
        bad = []
        for row in out.splitlines():
            path, size = row.rsplit("\t", 1)
            f = REPO / "results" / path
            if not f.is_file() or f.stat().st_size != int(size):
                bad.append(path)
        if bad:
            problems.append(
                f"{len(bad)} of the box's {lines(out)} result files not here with their size, e.g. {bad[:3]}"
            )
    led = box("cat ~/jobq/ledger.jsonl 2>/dev/null; true")
    here = lines(LEDGER.read_text()) if LEDGER.exists() else 0
    if led is None or lines(led) != here:
        problems.append(f"ledger: box {lines(led) if led is not None else '?'} lines, {LEDGER.name} {here}")
    out = box("cd ~/jobq/runs && find . -mindepth 2 -maxdepth 2 -name log.txt -printf '%P\\t%s\\n'", 120)
    if out is None:
        problems.append("the box's run logs list did not come")
    else:
        bad = []
        for row in out.splitlines():
            path, size = row.rsplit("\t", 1)
            f = REPO / "log" / "jobq" / path
            job = path.split("/")[0]
            if not f.is_file() or (job not in running and f.stat().st_size != int(size)):
                bad.append(path)
        if bad:
            problems.append(f"{len(bad)} run logs not under log/jobq/, e.g. {bad[:3]}")
    ok, why = fit_saved()
    if not ok:
        problems.append(f"the 32B fit's files: {why}")
    return problems


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_saved() -> tuple[bool, str]:
    """The 32B fit's files on the Mac (h200_finish.py's save): its status copy, and if DONE the lens with its sha256."""
    s = fit_status()
    if s is None or not terminal(s.get("state")):
        return False, f"the fit's state is {s.get('state') if s else 'unreadable'}"
    copies = [p for p in sorted((REPO / "results" / "lens_fit").glob("qwen3_32b_jpp64*/status.json"))
              if json.loads(p.read_text()).get("started") == s.get("started")]  # fmt: skip
    if not copies:
        return False, "no results/lens_fit/qwen3_32b_jpp64*/status.json of this fit on the Mac"
    if s["state"] == "DONE" and (not FIT_LENS.is_file() or sha256(FIT_LENS) != s.get("sha256")):
        return False, f"{FIT_LENS.relative_to(REPO)} missing or not the box's sha256"
    return True, f"fit {s['state']}, its files on the Mac ({copies[-1].parent.relative_to(REPO)})"


def terminate() -> bool:
    for i in range(1, 4):
        r = run(["uv", "run", "python", "scripts/lens_fit/h200_finish.py", "--terminate-only"], 300)
        out = (r.stdout + r.stderr).strip()[-1500:] if r is not None else "timed out"
        say(f"h200_finish.py --terminate-only, attempt {i}/3: exit {r.returncode if r else None}\n{out}")
        if r is not None and r.returncode == 0:
            return True
        time.sleep(60)
    return False


def final(reason: str, actions: set[str]) -> bool:
    """Pending jobs cancelled, then up to 3 tries of pull + fill + checks; the DELETE only if every check passes.
    False: the box is kept (an ACTION line says why, once per distinct reason)."""
    say(f"final: {reason}")
    q = queue()
    for i in q["pending"] if q else []:
        say(f"cancel {i}: the queue is ending")
        jq.cmd_cancel(i)
    problems = ["(not checked)"]
    for attempt in range(1, 4):
        pulled = pull()
        failed = fill_and_copy()
        q = queue()
        problems = ([] if pulled else ["jobq pull failed"]) + failed + verify(set(q["running"]) if q else set())
        if not problems:
            break
        say(f"final check {attempt}/3 failed: {'; '.join(problems)}")
        time.sleep(60)
    if problems:
        key = "; ".join(sorted(p.split(":")[0] for p in problems))
        if key not in actions:
            actions.add(key)
            say(f"ACTION: {HOST} NOT deleted ({reason}): {'; '.join(problems)}. The watchdog retries every "
                f"{RETRY_S // 60} min until {GIVE_UP:%H:%M}Z; by hand: JOBQ_HOST={HOST} uv run python scripts/jobq.py "
                f"pull, then uv run python scripts/remote/h200q_watchdog.py --check, then h200_finish.py --terminate-only")  # fmt: skip
        return False
    say("verified: every result file, the ledger, every run log and the 32B fit's files are on the Mac")
    if terminate():
        say("box deleted")
        return True
    say(
        "ACTION: the DELETE failed 3 times (a status deleting / deleted above means it went): check the Sesterce console"
    )
    return False


def summary(q: dict[str, Any] | None) -> str:
    if q is None:
        return "queue: the box did not answer"
    st = list(q["status"].values())
    running = "; ".join(f"{i} | {p}" for i, p in q["running"].items()) or "-"
    return (f"queue: running {running} | pending {len(q['pending'])} ({len(q['live'])} can run) | done "
            f"{st.count('done')}, failed {st.count('failed')}")  # fmt: skip


def check() -> int:
    global WRITE_LOG
    WRITE_LOG = False
    ok, why = start_condition()
    say(f"start condition {'MET' if ok else 'not met'}: {why}")
    q = queue()
    say(summary(q))
    ids = box("python3 ~/jobq/jobq.py box-ids")
    if ids is not None:
        new, superseded = new_specs(set(json.loads(ids)))
        say(f"would enqueue {[i for i, _ in new]}; superseded {sorted(superseded)}")
    say(
        f"workers on the box: GPU 0 {worker_running(0)}, GPU 1 {worker_running(1)}; last batch marked {LAST_BATCH.exists()}"
    )
    problems = verify(set(q["running"]) if q else set())
    say(f"delete checks now (no pull done here): {'; '.join(problems) or 'all pass'}")
    say(f"final from {FINAL_AT:%Y-%m-%d %H:%M}Z ({(FINAL_AT - now()).total_seconds() / 3600:.1f} h from now)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="every condition once; starts and deletes nothing")
    ap.add_argument("--last-batch", action="store_true", help="mark the last batch of 122B specs as committed")
    a = ap.parse_args()
    if a.check:
        return check()
    if a.last_batch:
        LAST_BATCH.parent.mkdir(parents=True, exist_ok=True)
        LAST_BATCH.write_text(now().isoformat() + "\n")
        say(f"last batch marked ({LAST_BATCH.relative_to(REPO)}): an empty queue now ends the box")
        return 0
    say(f"h200q watchdog on {HOST}: final from {FINAL_AT:%H:%M}Z (limit {LIMIT:%H:%M}Z); log {LOG.relative_to(REPO)}")
    try:
        jq._install_box_script()  # the Mac's jobq.py on the box, for box-status
    except subprocess.CalledProcessError as e:
        say(f"could not install jobq.py on the box ({e}); using the copy there")
    started = {g for g in (0, 1) if worker_running(g)}
    if started:
        say(f"workers already on the box: GPU {sorted(started)}")
    seen_failed: set[str] = set()
    actions: set[str] = set()
    last_why, last_pull, last_scan, last_enqueue, reason = "", 0.0, 0.0, time.time(), None
    finished_since: float | None = None
    while True:
        try:
            if reason is None and now() >= FINAL_AT:
                reason = f"{FINAL_AT:%H:%M} UTC: the hard limit {LIMIT:%H:%M} UTC is 10 min away"
            if reason is None and time.time() - last_scan >= PULL_S:  # new specs, also while waiting for the fit
                q0 = queue()
                if q0 is not None and enqueue_new(q0["pending"]):
                    last_enqueue = time.time()
                last_scan = time.time()
            if reason is not None:
                if final(reason, actions):
                    return 0
                if now() >= GIVE_UP:
                    say(f"ACTION: giving up 2 h after the limit; {HOST} is left up: verify and delete it by hand")
                    return 2
                time.sleep(RETRY_S)
                continue
            if 0 not in started:
                ok, why = start_condition()
                if why != last_why:
                    say(f"waiting to start: {why}")
                    last_why = why
                if not (ok and start_worker(0)):
                    time.sleep(WAIT_S)
                    continue
                started.add(0)
            q = queue()
            if time.time() - last_pull >= PULL_S:
                pull()
                last_pull = time.time()
                say(summary(q))
            if q is None:
                time.sleep(POLL_S)
                continue
            for j in sorted(i for i, s in q["status"].items() if s == "failed" and i not in seen_failed):
                say(f"job failed: {j}" + ("" if j in (GATE, PORT) else " (the queue goes on)"))
                seen_failed.add(j)
            if 1 not in started and q["status"].get(GATE) == "done" and start_worker(1):
                started.add(1)
            if stop := [j for j in (GATE, PORT) if q["status"].get(j) == "failed"]:
                reason = f"{' and '.join(stop)} failed"
                continue
            if q["running"] or q["live"]:
                finished_since = None
                time.sleep(POLL_S)
                continue
            finished_since = finished_since or time.time()
            idle = time.time() - max(finished_since, last_enqueue) >= IDLE_S
            if not (LAST_BATCH.exists() or idle):
                time.sleep(POLL_S)  # finished, but more batches may come
                continue
            if enqueue_new(q["pending"]):  # a batch committed just before --last-batch
                last_enqueue, finished_since = time.time(), None
                continue
            reason = "the queue is finished, " + ("the last batch marked" if LAST_BATCH.exists() else "idle 1 h")
        except Exception:
            say(f"watchdog error (it goes on):\n{traceback.format_exc()}")
            time.sleep(POLL_S)


if __name__ == "__main__":
    sys.exit(main())
