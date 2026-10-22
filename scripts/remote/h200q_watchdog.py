"""h200q: Qwen3.5-122B-A10B's job queue on the 2x H200 box after the Qwen3-32B J++ fit, then the box deleted (Dan, 23 Oct
~00:35). Runs on the Mac (the Sesterce key stays here), in tmux session h200q under caffeinate -i:

    caffeinate -i uv run python scripts/remote/h200q_watchdog.py   # log: log/remote/h200q_watchdog.log
    uv run python scripts/remote/h200q_watchdog.py --check         # every condition once; starts and deletes nothing

The queue is jobq's (scripts/jobq.py) on the box sesterce-h200x2 (~/jobq; jobs enqueued from the Mac with
JOBQ_HOST=sesterce-h200x2). This script only starts its workers, pulls, and ends the box:
1. Start: wait (every 2 min) until the fit's ~/work/fit32b/status.json is terminal, the Mac's tmux session h200finish has
   ended (it saves the fit's lens to the Mac), the 122B prefetch printed PREFETCH_DONE with its lens sha256 ok, and
   nvidia-smi shows both GPUs free. Then jobq's worker for GPU 0 (tmux jobq-gpu0 on the box); the worker for GPU 1 once
   the lens gate (first in the queue) is done: the gate before any other 122B job. One job per GPU (FP8 122B ~127 GB).
   Workers run with HF_HOME=~/work/hf (the prefetched weights and lens), UV_CACHE_DIR=~/work/uv-cache, and jobq's
   free-memory check off: an idle H200 shows 143771 - 616 MiB = 139.8 GiB free, under the specs' mem_gb 140, so the
   check would hold every job forever; nothing else runs on these GPUs once the fit is over.
2. Every minute the queue's state; every 5 min a pull: the box's run dirs into results/ (a dir that exists here and
   was not created by this watchdog goes to log/remote/h200q_conflicts/ instead: nothing here is overwritten), the
   ledger to results/jobq/ledger_h200.jsonl (results/jobq/ledger.jsonl stays the A100 queue's), drafts, job logs.
3. Stop when the queue is finished (nothing running; every pending job waits on a failed one), the lens gate or the
   port smoke job failed (other failures are logged and the queue goes on), or at 06:50 UTC (the hard limit is 07:00
   UTC). Then a last pull; every file of the box's run dirs must be here with its size, and the 32B fit's files too
   (its status copy in results/lens_fit/, and if DONE the lens with the box's sha256). Only then
   scripts/lens_fit/h200_finish.py --terminate-only (the checked DELETE). If a check fails it does NOT delete and
   retries every 5 min (an idle box costs less than lost results), giving up 2 h after the limit. Ctrl-C stops the
   watchdog only: no pull, no delete.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
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
jq.HOST = HOST  # jobq's Mac-side helpers read it at call time
REPO = jq.REPO
GATE, PORT = "qwen35_122b_lens_gate_v2", "qwen35_122b_port_smoke"
LIMIT = dt.datetime(2026, 10, 23, 7, 0, tzinfo=dt.UTC)
FINAL_AT = LIMIT - dt.timedelta(minutes=10)
GIVE_UP = LIMIT + dt.timedelta(hours=2)
WAIT_S, POLL_S, PULL_S = 120, 60, 300
LOG = REPO / "log" / "remote" / "h200q_watchdog.log"
PULLED = REPO / "cache" / "jobq" / "h200q_pulled.json"  # the run dirs this watchdog created in results/
CONFLICTS = REPO / "log" / "remote" / "h200q_conflicts"
FIT_LENS = REPO / "cache" / "qwen3-32b" / "lenses" / "jpp" / "Qwen3-32B_jpp_lens.pt"
WORKER = ("export HF_HOME=$HOME/work/hf UV_CACHE_DIR=$HOME/work/uv-cache; python3 -c {code} 2>&1 | "
          "tee -a ~/jobq/worker-gpu{gpu}.log; exec bash")  # fmt: skip
WORKER_CODE = (
    "import os, sys; sys.path.insert(0, os.path.expanduser('~/jobq')); import jobq; jobq.worker({gpu}, check_mem=False)"
)
WRITE_LOG = True


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


def start_worker(gpu: int) -> bool:
    inner = WORKER.format(code=shlex.quote(WORKER_CODE.format(gpu=gpu)), gpu=gpu)
    cmd = shlex.join(["tmux", "new-session", "-d", "-s", f"jobq-gpu{gpu}", "bash", "-c", inner])
    ok = box(f"tmux has-session -t jobq-gpu{gpu} 2>/dev/null || {cmd}") is not None
    say(f"worker GPU {gpu}: {'started' if ok else 'FAILED to start'} (ssh {HOST} -t tmux attach -t jobq-gpu{gpu})")
    return ok


def queue() -> dict[str, Any] | None:
    """Running and pending jobs, each job's last ledger status, and the pending jobs that can still run (every
    dependency done, running, or itself pending and able to run)."""
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
    live: set[str] = set()
    grew = True
    while grew:
        grew = False
        for i, deps in pending.items():
            if i not in live and all(status.get(d) == "done" or d in running or d in live for d in deps):
                live.add(i)
                grew = True
    return {"running": running, "pending": sorted(pending), "live": sorted(live), "status": status}


def pulled_dirs() -> set[str]:
    return set(json.loads(PULLED.read_text())) if PULLED.exists() else set()


def pull(announced: set[str]) -> bool:
    """The box's run dirs (results/<exp>/<run>) here, never over a file that exists; ledger, drafts, logs."""
    out = box("cd ~/jobq/results && find . -mindepth 2 -maxdepth 2 -type d", 120)
    if out is None:
        say("pull: the box did not answer")
        return False
    pulled, ok = pulled_dirs(), True
    for d in sorted(x.removeprefix("./") for x in out.split()):
        here = REPO / "results" / d
        if d not in pulled and here.exists():
            dst = CONFLICTS / d
            if d not in announced:
                say(
                    f"pull: results/{d} exists here and is not this queue's; the box's copy goes to {dst.relative_to(REPO)}"
                )
                announced.add(d)
        else:
            dst = here
            if d not in pulled:  # recorded first, so a copy cut short is completed by the next pull
                pulled.add(d)
                PULLED.parent.mkdir(parents=True, exist_ok=True)
                PULLED.write_text(json.dumps(sorted(pulled), indent=1) + "\n")
        dst.mkdir(parents=True, exist_ok=True)
        r = run(["rsync", "-a", "--ignore-existing", f"{HOST}:jobq/results/{d}/", f"{dst}/"], 1200)
        if r is None or r.returncode:
            ok = False
            say(f"pull: rsync of {d} failed: {(r.stderr if r else 'timed out')[-300:]}")
    (REPO / "results" / "jobq" / "drafts").mkdir(parents=True, exist_ok=True)
    (REPO / "log" / "jobq").mkdir(parents=True, exist_ok=True)
    run(["rsync", "-a", f"{HOST}:jobq/ledger.jsonl", str(REPO / "results" / "jobq" / "ledger_h200.jsonl")], 300)
    run(["rsync", "-a", f"{HOST}:jobq/drafts/", f"{REPO / 'results' / 'jobq' / 'drafts'}/"], 300)
    run(["rsync", "-a", "--exclude=code/", "--include=*/", "--include=log.txt", "--exclude=*", f"{HOST}:jobq/runs/",
         f"{REPO / 'log' / 'jobq'}/"], 300)  # fmt: skip
    return ok


def missing_here() -> list[str]:
    """Files of the box's run dirs not here with the same size ([] when everything came back)."""
    out = box("cd ~/jobq/results && find . -mindepth 3 -type f -printf '%P\\t%s\\n'", 300)
    if out is None:
        return ["(the box did not answer)"]
    pulled, missing = pulled_dirs(), []
    for line in out.splitlines():
        path, size = line.rsplit("\t", 1)
        base = REPO / "results" if "/".join(path.split("/")[:2]) in pulled else CONFLICTS
        f = base / path
        if not f.is_file() or f.stat().st_size != int(size):
            missing.append(path)
    return missing


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


def final(reason: str, announced: set[str]) -> bool:
    """A last pull and the checks, then the DELETE; False (box kept) if anything is not on the Mac."""
    say(f"final: {reason}")
    missing = ["(not pulled)"]
    for _ in range(3):
        pull(announced)
        if not (missing := missing_here()):
            break
        time.sleep(30)
    if missing:
        say(f"NOT DELETING: {len(missing)} files of the box's results are not here, e.g. {missing[:5]}")
        return False
    say(f"results: every file of the box's {len(pulled_dirs())} run dirs is here")
    ok, why = fit_saved()
    if not ok:
        say(f"NOT DELETING: the 32B fit's files are not on the Mac ({why})")
        return False
    say(why)
    if terminate():
        say("box deleted")
        return True
    say("!! the DELETE failed 3 times (a status deleting / deleted above means it went): check the Sesterce console")
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
    say(summary(queue()))
    say(f"fit files on the Mac: {fit_saved()}")
    say(f"final from {FINAL_AT:%Y-%m-%d %H:%M}Z ({(FINAL_AT - now()).total_seconds() / 3600:.1f} h from now)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="every condition once; starts and deletes nothing")
    if ap.parse_args().check:
        return check()
    say(f"h200q watchdog on {HOST}: final from {FINAL_AT:%H:%M}Z (limit {LIMIT:%H:%M}Z); log {LOG.relative_to(REPO)}")
    try:
        jq._install_box_script()  # the Mac's jobq.py on the box, for box-status
    except subprocess.CalledProcessError as e:
        say(f"could not install jobq.py on the box ({e}); using the copy there")
    started: set[int] = set()
    announced: set[str] = set()
    seen_failed: set[str] = set()
    last_why, last_pull, reason = "", 0.0, None
    while True:
        try:
            if reason is None and now() >= FINAL_AT:
                reason = "06:50 UTC: the hard limit 07:00 UTC is 10 min away"
            if reason is not None:
                if final(reason, announced):
                    return 0
                if now() >= GIVE_UP:
                    say("giving up 2 h after the limit: the box is still running; delete it by hand")
                    return 2
                time.sleep(PULL_S)
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
                pull(announced)
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
            elif not q["running"] and not q["live"]:
                reason = "the queue is finished"
            else:
                time.sleep(POLL_S)
        except Exception:
            say(f"watchdog error (it goes on):\n{traceback.format_exc()}")
            time.sleep(POLL_S)


if __name__ == "__main__":
    sys.exit(main())
