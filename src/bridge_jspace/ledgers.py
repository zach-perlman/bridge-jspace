"""The local copies of every queue box's ledger and queue state (Dan, 23 Oct: each box has its own ledger). `jobq pull`
writes results/jobq/ledger_<host>.jsonl and cache/jobq/queue_state_<host>.json per box; an older unsuffixed
ledger.jsonl / queue_state.json (the A100's, before 23 Oct) is still read if present."""

import json
from pathlib import Path
from typing import Any


def ledger_files(results_dir: Path) -> list[Path]:
    d = results_dir / "jobq"
    legacy = d / "ledger.jsonl"
    return sorted(d.glob("ledger_*.jsonl")) + ([legacy] if legacy.exists() else [])


def ledger_records(results_dir: Path) -> list[dict[str, Any]]:
    """Every box's ledger records, box by box, each in its file's (append) order."""
    out: list[dict[str, Any]] = []
    for p in ledger_files(results_dir):
        out += [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
    return out


def queue_state_files(cache_dir: Path) -> list[Path]:
    d = cache_dir / "jobq"
    legacy = d / "queue_state.json"
    return sorted(d.glob("queue_state_*.json")) + ([legacy] if legacy.exists() else [])
