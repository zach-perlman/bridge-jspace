"""Delete the 4x A100 box when its queue is drained AND everything is on the Mac (Dan, 23 Oct ~00:55: "before deleting an
instance, make sure we pulled all the information, all experiments, else it must not be deleted"). Runs on the Mac:

  caffeinate -i uv run python scripts/remote/a100_watchdog.py --release-flag <path> [--dry-run]

Every 5 min: (1) wait for the release flag (the coordinator creates it once every planned job is enqueued, so a queue
that is empty between batches is never taken for done); (2) no pending and no running job for two checks in a row;
(3) jobq pull, then rsync --ignore-existing of the box's results/ (pull copies only run dirs new to the Mac; this fills
any missing file and never overwrites a local one), the run logs, and the lens fits' small files; (4) verify: every file
under the box's ~/jobq/results exists locally (size equal, or the local copy is newer: changed here on purpose), the local
ledger has at least the box ledger's lines, every run's log.txt is local; (5) only if all pass: delete through the API
(scripts/remote/sesterce_delete.py, matched by ip, 4x A100, active). A failed verification retries the pull 3 times,
then leaves the box up and prints ACTION. Nothing secret is printed.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOST, IP = "sesterce-a100x4", "38.80.123.239"


def log(msg: str) -> None:
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}", flush=True)


def ssh(cmd: str, timeout: int = 300) -> str:
    try:
        return subprocess.run(["ssh", HOST, cmd], capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return ""


def run(args: list[str], timeout: int = 3600) -> int:
    try:
        return subprocess.run(args, cwd=REPO, timeout=timeout).returncode
    except subprocess.TimeoutExpired:
        return -1


def queue_counts() -> tuple[int, int] | None:
    out = ssh("ls ~/jobq/pending | wc -l; ls ~/jobq/running | wc -l").split()
    return (int(out[0]), int(out[1])) if len(out) == 2 and all(x.isdigit() for x in out) else None


def pull_everything() -> None:
    run(["uv", "run", "python", "scripts/jobq.py", "pull"])
    run(["rsync", "-a", "--ignore-existing", f"{HOST}:jobq/results/", f"{REPO}/results/"])
    run(["rsync", "-a", "--include=*/", "--include=log.txt", "--exclude=*", f"{HOST}:jobq/runs/", f"{REPO}/log/jobq/"])
    (REPO / "log" / "remote" / "a100_lens_fit").mkdir(parents=True, exist_ok=True)
    run(["rsync", "-a", "--include=*/", "--include=*.log", "--include=*.csv", "--include=*.json", "--exclude=*",
         f"{HOST}:/ephemeral/lens_fit/", f"{REPO}/log/remote/a100_lens_fit/"])  # fmt: skip


def verify() -> list[str]:
    """Problems found (empty = everything on the Mac)."""
    problems: list[str] = []
    listing = ssh("cd ~/jobq/results && find . -type f -printf '%P\\t%s\\t%T@\\n'", timeout=600)
    if not listing.strip():
        return ["could not list the box's results"]
    n = 0
    for line in listing.splitlines():
        rel, size, mtime = line.split("\t")
        n += 1
        local = REPO / "results" / rel
        if not local.exists():
            problems.append(f"missing locally: results/{rel}")
        elif local.stat().st_size != int(size) and local.stat().st_mtime <= float(mtime):
            problems.append(f"size differs (local older): results/{rel}")
        if len(problems) > 20:
            break
    box_lines = ssh("wc -l < ~/jobq/ledger.jsonl").strip()
    local_ledger = REPO / "results" / "jobq" / f"ledger_{HOST}.jsonl"
    local_lines = len(local_ledger.read_text().splitlines()) if local_ledger.exists() else 0
    if not box_lines.isdigit() or local_lines < int(box_lines):
        problems.append(f"ledger: local {local_lines} lines, box {box_lines}")
    runs = ssh("cd ~/jobq/runs && ls -d */ 2>/dev/null").split()
    for r in runs:
        rid = r.rstrip("/")
        if (
            ssh(f"test -f ~/jobq/runs/{rid}/log.txt && echo y").strip() == "y"
            and not (REPO / "log" / "jobq" / rid / "log.txt").exists()
        ):
            problems.append(f"log missing locally: log/jobq/{rid}/log.txt")
    log(f"verify: {n} box result files checked, {len(runs)} run logs, ledger {local_lines}/{box_lines}: "
        f"{'OK' if not problems else str(len(problems)) + ' problems'}")  # fmt: skip
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release-flag", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true", help="verify but never delete")
    ap.add_argument("--every", type=int, default=300)
    a = ap.parse_args()
    empty_checks, failures = 0, 0
    while True:
        if not a.release_flag.exists():
            log("waiting: no release flag yet (planned jobs still to be enqueued)")
            time.sleep(a.every)
            continue
        counts = queue_counts()
        if counts is None:
            log("box unreachable; retrying")
            time.sleep(a.every)
            continue
        pending, running = counts
        if pending or running:
            empty_checks = 0
            log(f"queue: {pending} pending, {running} running")
            time.sleep(a.every)
            continue
        empty_checks += 1
        if empty_checks < 2:
            log("queue empty once; checking again before the pull")
            time.sleep(a.every)
            continue
        pull_everything()
        problems = verify()
        if problems:
            failures += 1
            for p in problems[:20]:
                log(f"  {p}")
            if failures >= 3:
                log("ACTION: verification failed 3 times; the box stays up (not deleted)")
                return 2
            time.sleep(60)
            continue
        log("everything is on the Mac")
        if a.dry_run:
            log("dry run: not deleting")
            return 0
        rc = run(
            ["uv", "run", "python", "scripts/remote/sesterce_delete.py", "--ip", IP, "--gpu", "A100", "--count", "4"]
        )
        log(f"delete exit {rc}")
        return rc


if __name__ == "__main__":
    sys.exit(main())
