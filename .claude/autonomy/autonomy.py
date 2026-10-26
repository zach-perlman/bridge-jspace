"""Autonomy window for Claude Code (Dan, 26 Oct): for N hours (e.g. overnight) the agent works without permission
prompts, and when the time is up the old limits come back by themselves. A Claude Code tool, not part of the
experiments: it lives in .claude/autonomy/ and touches nothing outside .claude/.

`grant` backs up .claude/settings.local.json, adds tool-wide allow rules (Bash, Edit, Write, ...) and the deny rules
that keep a human in the loop (git push, git reset --hard, git clean, rm -rf), and records exactly what it added in
.claude/autonomy/state.json. At the deadline a detached watcher (it survives the Claude session) removes exactly those
rules: rules added to the file meanwhile, by hand or by "always allow", stay, and rules that were there before stay too.
Claude Code reloads the file live, so a running session switches over without a restart.

Failure modes covered: the Mac asleep at the deadline (the watcher wakes every 30 s, so it revokes on wake);
the watcher killed (a reboot): the window adds a SessionStart hook, so the next Claude session revokes an expired window,
as do `status` and `grant`. On macOS, `caffeinate` keeps the Mac awake until the deadline (idle and system sleep on AC
power; a closed lid still sleeps). Stdlib only, so the hook runs with the system python3. Log: .claude/autonomy/log.txt.

    python3 .claude/autonomy/autonomy.py grant --hours 10   # or --until 11:00 (its next occurrence); again while
                                                             # open: moves the deadline (make autonomy HOURS= / UNTIL=)
    python3 .claude/autonomy/autonomy.py status             # open?, deadline, time left (make autonomy-status)
    python3 .claude/autonomy/autonomy.py revoke             # close it now (make autonomy-off)
    uv run pytest .claude/autonomy                           # its tests (not in `make test`)
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SETTINGS = HERE.parent / "settings.local.json"
STATE = HERE / "state.json"
LOG = HERE / "log.txt"
ALLOW = ["Bash", "Edit", "Write", "Read", "NotebookEdit", "WebFetch", "WebSearch", "Agent", "Skill", "Monitor",
         "TaskStop", "ToolSearch"]  # fmt: skip
# AGENTS.md: push only after a human OK; never destroy results or history
DENY = ["Bash(git push*)", "Bash(git -C * push*)", "Bash(git reset --hard*)", "Bash(git clean*)", "Bash(rm -rf *)"]
HOOK_CMD = f"python3 {HERE / 'autonomy.py'} check"
POLL_S = 30


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text()) if path.exists() else {}


def save(path: Path, d: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(d, indent=2) + "\n")
    tmp.replace(path)


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} [{os.getpid()}] {msg}\n")


def _our_hook(entry: dict[str, Any]) -> bool:
    return any(h.get("command") == HOOK_CMD for h in entry.get("hooks", []))


def add_rules(settings: dict[str, Any]) -> dict[str, Any]:
    """Add the window's rules and hook to `settings` in place; return what was added (only what was missing, and the
    containers it had to create, so that revoking leaves the file as it was)."""
    new = [k for k, d in (("permissions", settings), ("hooks", settings)) if k not in d]
    perms = settings.setdefault("permissions", {})
    hooks = settings.setdefault("hooks", {})
    new += [k for k, d in (("allow", perms), ("deny", perms), ("SessionStart", hooks)) if k not in d]
    allow, deny = perms.setdefault("allow", []), perms.setdefault("deny", [])
    starts = hooks.setdefault("SessionStart", [])
    added = {"allow": [r for r in ALLOW if r not in allow], "deny": [r for r in DENY if r not in deny],
             "hook": not any(_our_hook(e) for e in starts), "new_keys": new}  # fmt: skip
    allow[:0] = added["allow"]
    deny.extend(added["deny"])
    if added["hook"]:
        starts.append({"hooks": [{"type": "command", "command": HOOK_CMD}]})
    return added


def remove_rules(settings: dict[str, Any], added: dict[str, Any]) -> dict[str, Any]:
    """Undo `add_rules` in place: drop exactly `added`, then the containers it created if they are empty again."""
    new = set(added.get("new_keys", []))
    perms, hooks = settings.get("permissions", {}), settings.get("hooks", {})
    for key in ("allow", "deny"):
        if key in perms:
            perms[key] = [r for r in perms[key] if r not in added.get(key, [])]
    if added.get("hook") and "SessionStart" in hooks:
        hooks["SessionStart"] = [e for e in hooks["SessionStart"] if not _our_hook(e)]
    for parent, key in ((perms, "allow"), (perms, "deny"), (hooks, "SessionStart"), (settings, "permissions"),
                        (settings, "hooks")):  # fmt: skip
        if key in new and key in parent and not parent[key]:
            del parent[key]
    return settings


def _alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except (ProcessLookupError, PermissionError):
        return False
    return True


def _stop(pid: int | None) -> None:
    if pid and pid != os.getpid() and _alive(pid):
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, signal.SIGTERM)


def _detach(argv: list[str]) -> int:
    with LOG.open("a") as out:
        return subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=out, start_new_session=True).pid


def parse_until(hours: float | None, until: str | None, now: dt.datetime) -> dt.datetime:
    """`hours` from now, or `until` as HH:MM (its next occurrence) or 'YYYY-MM-DD HH:MM'."""
    if (hours is None) == (until is None):
        raise SystemExit("give exactly one of --hours / --until")
    if hours is not None:
        if hours <= 0:
            raise SystemExit("--hours must be > 0")
        return now + dt.timedelta(hours=hours)
    assert until is not None
    if " " in until:
        end = dt.datetime.strptime(until, "%Y-%m-%d %H:%M")
    else:
        t = dt.datetime.strptime(until, "%H:%M").time()
        end = dt.datetime.combine(now.date(), t)
        if end <= now:
            end += dt.timedelta(days=1)
    if end <= now:
        raise SystemExit(f"--until {until} is in the past")
    return end


def grant(end: dt.datetime, spawn: bool = True) -> dict[str, Any]:
    """Open a window until `end`, or move the deadline of the open one. `spawn`: start the watcher and caffeinate."""
    check()  # an expired window left by a dead watcher goes first
    state = load(STATE)
    if state:  # active: move the deadline; the rules are in place and the watcher re-reads the state
        state["until"] = end.timestamp()
        log(f"deadline moved to {end:%Y-%m-%d %H:%M}")
    else:
        settings = load(SETTINGS)
        state = {
            "until": end.timestamp(),
            "started": time.time(),
            "created_file": not SETTINGS.exists(),
            "added": add_rules(settings),
        }
        if SETTINGS.exists():
            shutil.copy2(SETTINGS, SETTINGS.with_name(SETTINGS.name + ".autonomy-bak"))
        save(SETTINGS, settings)
        log(f"granted until {end:%Y-%m-%d %H:%M}: {state['added']}")
    if spawn:
        if not _alive(state.get("watcher_pid")):
            state["watcher_pid"] = _detach([sys.executable, str(Path(__file__).resolve()), "watch"])
        _stop(state.get("caffeinate_pid"))
        state.pop("caffeinate_pid", None)
        if shutil.which("caffeinate"):
            secs = max(1, int(end.timestamp() - time.time()))
            state["caffeinate_pid"] = _detach(["caffeinate", "-i", "-m", "-s", "-t", str(secs)])
    save(STATE, state)
    return state


def revoke(reason: str = "by hand") -> bool:
    """Undo the window; False if none was open (a second revoke is a no-op)."""
    state = load(STATE)
    if not state:
        return False
    settings = remove_rules(load(SETTINGS), state["added"])
    if state.get("created_file") and not settings:
        SETTINGS.unlink(missing_ok=True)
    else:
        save(SETTINGS, settings)
    STATE.unlink(missing_ok=True)
    _stop(state.get("caffeinate_pid"))
    _stop(state.get("watcher_pid"))
    log(f"revoked ({reason}): {state['added']}")
    return True


def check(now: float | None = None) -> bool:
    """Revoke the window if its deadline passed; True if it did."""
    state = load(STATE)
    if state and (time.time() if now is None else now) >= state["until"]:
        return revoke(reason="deadline")
    return False


def watch() -> None:
    log("watcher started")
    while state := load(STATE):
        left = state["until"] - time.time()
        if left <= 0:
            revoke(reason="deadline")
            return
        time.sleep(min(POLL_S, left))
    log("watcher: no window, exiting")


def status() -> str:
    if check():
        return "autonomy: off (the deadline had passed: revoked now)"
    state = load(STATE)
    if not state:
        return "autonomy: off"
    end = dt.datetime.fromtimestamp(state["until"])
    left = dt.timedelta(seconds=int(state["until"] - time.time()))
    watcher = "alive" if _alive(state.get("watcher_pid")) else "DEAD (the next session start or status revokes)"
    caff = "alive" if _alive(state.get("caffeinate_pid")) else "not running"
    return "\n".join([
        f"autonomy: ON until {end:%Y-%m-%d %H:%M} ({left} left)",
        f"  watcher {state.get('watcher_pid')}: {watcher}",
        f"  caffeinate {state.get('caffeinate_pid')}: {caff}",
        f"  added: allow {state['added']['allow']}, deny {state['added']['deny']}",
    ])  # fmt: skip


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grant")
    g.add_argument("--hours", type=float)
    g.add_argument("--until", help="HH:MM (its next occurrence) or 'YYYY-MM-DD HH:MM'")
    for name in ("revoke", "status", "check", "watch"):
        sub.add_parser(name)
    a = ap.parse_args()
    if a.cmd == "grant":
        state = grant(parse_until(a.hours, a.until, dt.datetime.now()))
        print(f"autonomy: ON until {dt.datetime.fromtimestamp(state['until']):%Y-%m-%d %H:%M}; added {state['added']}")
        print("off early: make autonomy-off   status: make autonomy-status")
    elif a.cmd == "revoke":
        print("autonomy: revoked" if revoke() else "autonomy: was off")
    elif a.cmd == "status":
        print(status())
    elif a.cmd == "check":
        check()
    else:
        watch()


if __name__ == "__main__":
    main()
