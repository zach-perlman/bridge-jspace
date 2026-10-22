"""Progress of tonight's J++ fits, from the Mac (standard library only):

  python3 scripts/lens_fit/jpp_progress.py            # once
  python3 scripts/lens_fit/jpp_progress.py --watch 300 # every 5 min

Qwen3-32B on the 2x H200 box (shards' last "prompt i/32" lines, the launcher's status.json, the Mac finisher in tmux
h200finish) and OLMo-3-7B-Instruct on the A100 queue (the jobq state and the stage its log is in).
"""

import argparse
import calendar
import json
import re
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROMPT = re.compile(r"prompt (\d+)/(\d+)\s.*?(\d+)s\s*$")


def ssh(host: str, cmd: str) -> str:
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=15", host, cmd], capture_output=True, text=True, timeout=60)
        return r.stdout
    except subprocess.TimeoutExpired:
        return ""


def eta(lines: list[str]) -> str:
    """i/N and the time left at the mean seconds per prompt of the lines seen."""
    hits = [PROMPT.search(x) for x in lines]
    hits = [h for h in hits if h]
    if not hits:
        return "no prompt finished yet"
    i, n = int(hits[-1][1]), int(hits[-1][2])
    per = sum(int(h[3]) for h in hits) / len(hits)
    left = (n - i) * per / 60
    return f"prompt {i}/{n}, {per:.0f} s/prompt, ~{left:.0f} min left"


def qwen32b() -> None:
    out = ssh("sesterce-h200x2", "for f in ~/work/fit32b/shard*_r*.log; do echo \"== $f\"; grep -h 'prompt [0-9]*/' "
              "$f; done; echo '== status'; cat ~/work/fit32b/status.json")  # fmt: skip
    print("Qwen3-32B J++ (2x H200)")
    if not out:
        print("  box unreachable (terminated after the fit, or the network)")
    blocks = out.split("== ")[1:]
    for b in blocks:
        head, *rest = b.splitlines()
        if head == "status":
            try:
                s = json.loads("\n".join(rest))
                started = calendar.timegm(time.strptime(s["started"], "%Y-%m-%dT%H:%M:%SZ"))
                print(
                    f"  launcher: {s.get('state')} at {s.get('at')}, {(time.time() - started) / 60:.0f} min since start"
                )
            except json.JSONDecodeError:
                pass
        else:
            print(f"  {Path(head).name}: {eta(rest)}")
    alive = subprocess.run(["tmux", "has-session", "-t", "h200finish"], capture_output=True).returncode == 0
    logs = sorted((REPO / "log").glob("h200_finish_*.log"))
    tail = [x for x in logs[-1].read_text().splitlines() if x[:2].isdigit()][-1:] if logs else []
    print(f"  finisher (Mac tmux h200finish): {'running' if alive else 'ended'}; {tail[0] if tail else 'waiting'}")


def olmo() -> None:
    out = ssh("sesterce-a100x4", "cd ~/jobq; for s in pending running done failed; do ls $s | grep -q "
              "olmo3_7b_instruct_jpp_fit && echo STATE $s; done; grep -v '^\\[jobq' "
              "runs/olmo3_7b_instruct_jpp_fit/log.txt | tail -400")  # fmt: skip
    print("OLMo-3-7B-Instruct J++ (A100 queue)")
    lines = out.splitlines()
    state = next((x.split()[1] for x in lines if x.startswith("STATE")), "unknown")
    # the recipe's own log messages, in pipeline order; the last one seen is the stage reached
    marks = [("router saved", "shards"), ("prompt ", "shards"), ("merged", "merge done"), ("lens saved", "readout weights done"),
             ("ranks saved", "evaluation done"), ("fp16", "export")]  # fmt: skip
    stage = "router (CPU-heavy)"
    for x in lines:
        stage = next((s for m, s in marks if m in x), stage)
    print(f"  job: {state}; last stage seen: {stage}; {eta([x for x in lines if 'prompt' in x])}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--watch", type=int, default=0, help="repeat every N seconds")
    a = ap.parse_args()
    while True:
        print(time.strftime("%H:%M:%S"))
        qwen32b()
        olmo()
        if not a.watch:
            break
        print()
        time.sleep(a.watch)


if __name__ == "__main__":
    main()
