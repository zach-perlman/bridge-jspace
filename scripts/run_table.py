"""run_table: the runs behind every cell of the cross-model grid, as tables for the README (a draft, never README.md).

Reads (no result file is opened; existence of the linked folders is checked):
  results/cross_model/<stamp>/sources.txt  each grid row: model | finding | setting | lens role | run | files read
  results/cross_model/<stamp>/grid.csv     the verdict of each of those rows (joined on model, finding, setting, role)
  results/jobq/ledger_*.jsonl              the job that wrote each run: box, finish time, GPU-hours, spec commit
Writes drafts/run_table_<UTC stamp>.md: one table per finding (findings 1-8 and the lens gate, in the grid's order and
words). Rows: the grid's settings. Columns: Qwen3.6-27B, Qwen3.5-9B, Olmo-Hybrid-7B, Qwen3.5-122B, Qwen3-32B,
OLMo-3-7B-I, Muse 30B, Gemma 4 31B-it. A cell: the run(s) behind the grid cell with the grid's verdict symbol, each run
a link (from the repo root) to the folder the grid read; a run with another lens or beside the main one on a second
line. Under each table the jobs behind its runs; on top, the night of 22-23 Oct from the ledgers (jobs done / failed
and GPU-hours per box, jobs started since --since, by default readme_draft's window).

Breakdown rows (a " · " setting: per topic, per family) are the same run as their grid row and are not listed again; a
grid setting split in parts (finding 5: "draw 1, 1st-2nd" / "draw 1, 3rd on") is one cell. A job copied into several
ledgers (the 4x A100's was seeded with the single A100's) is counted once, under the first ledger read. A run's job:
the ledger records whose new_results name the run (else whose id is the run), the last one done, else the last one.
GPU-hours: wall time x GPUs; a job whose record has no wall time (a worker that died) is named, not counted.

uv run python scripts/run_table.py [--grid DIR] [--since ISO] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace.ledgers import ledger_files
from scripts import cross_model_grid as G
from scripts import readme_draft as RD

REPO = G.REPO
COLUMNS = ("27b", "9b", "olmo_hybrid", "122b", "32b", "olmo", "muse", "gemma")  # Dan's order (23 Oct)
# grid.md's short reasons for a cell without a value (cross_model_grid.md_cell), first match wins
REASONS = (("no spec", "no spec"), ("no lens", "no lens"), (" failed at the ", "failed"), ("pending in the queue",
           "pending"), ("running in the queue", "running"), (" waits on ", "blocked"), ("not run", "not run"),
           ("Zach's branch", "not on Zach's branch"), ("competence", "competence"))  # fmt: skip


@dataclass(frozen=True)
class Source:
    model: str  # model key (cross_model_grid.MODELS)
    finding: str  # finding key
    setting: str  # the grid setting (grid.md's row)
    role: str  # "main", or the lens / run it is listed beside
    run: str  # "" for a cell without a run
    path: str  # the file the grid read for this run ("" none)
    word: str  # verdict word
    verdict: str  # grid.csv's verdict text


@dataclass(frozen=True)
class Job:
    id: str
    box: str  # the ledger's name: ledger_<box>.jsonl
    status: str
    started: dt.datetime | None
    ended: dt.datetime | None
    gpu_hours: float
    commit: str
    gpu_name: str
    runs: frozenset[str]  # the run names its new_results write
    failure: str = ""  # where a job that is not done stopped: "figures, exit 1", "run, exit 3", the ledger's error
    timed: bool = True  # False: no wall time in the ledger (a worker that died); its GPU-hours are not counted


# ---------------------------------------------------------------- inputs


def role_of(lens: str) -> str:
    """grid.csv's lens column -> the lens role: '<lens> (<role>, listed beside)' or the main lens."""
    return lens.rsplit(" (", 1)[1].removesuffix(RD.BESIDE) if lens.endswith(RD.BESIDE) else "main"


def run_path(run: str, paths: str) -> str:
    """The file a run's cell was read from: the first one that names the run, else the first."""
    ps = [p.strip() for p in paths.split(";") if p.strip() not in ("", "-")]
    return next((p for p in ps if run and run in RD.run_names(p)), ps[0] if ps else "")


def read_sources(grid_dir: Path) -> list[Source]:
    """sources.txt's grid rows (breakdown rows dropped), each with its grid.csv verdict."""
    verdicts: dict[tuple[str, str, str, str], collections.deque[str]] = collections.defaultdict(collections.deque)
    with open(grid_dir / "grid.csv", newline="") as f:
        for r in csv.DictReader(f):
            verdicts[(r["model"], r["finding"], r["setting"], role_of(r["lens"]))].append(r["verdict"])
    out = []
    for line in (grid_dir / "sources.txt").read_text().splitlines():
        if not line.strip():
            continue
        model, finding, setting, role, run, paths = line.split(" | ", 5)
        key = (model, finding, setting, role)
        if not verdicts.get(key):
            raise ValueError(f"no grid.csv row for this sources.txt row: {line}")
        verdict = verdicts[key].popleft()
        m, f = RD.MODEL_BY_LABEL.get(model), RD.FINDING_BY_NAME.get(finding)
        if m is None or f is None:
            raise ValueError(f"model or finding not in cross_model_grid: {line}")
        gs = RD.grid_setting(f, setting)
        if gs is None:  # a breakdown row: the same run as its grid row
            continue
        word = next((w for w in G.VERDICTS if verdict.startswith(w)), None)
        if word is None:
            raise ValueError(f"unknown verdict word: {verdict}")
        run = "" if run == "-" else run
        out.append(Source(m.key, f.key, gs[0], role, run, run_path(run, paths), word, verdict))
    return out


def when(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    t = dt.datetime.fromisoformat(s)
    return t if t.tzinfo else t.replace(tzinfo=dt.UTC)


def run_name(folder: str) -> str:
    """results/<exp>/<run>[_<level>]_<stamp> -> <run>."""
    seg = folder.rstrip("/").split("/")[-1]
    m = RD.STAMPED.fullmatch(seg)
    return m.group(1) if m else seg


def failure(r: dict) -> str:
    """The stage a ledger record stopped at (a job can fail at its figures stage after its run stage wrote results)."""
    if r.get("status") == "done":
        return ""
    for stage, key in (("run", "exit_code"), ("examples", "examples_exit"), ("figures", "figures_exit")):
        if r.get(key) not in (None, 0):
            return f"{stage}, exit {r[key]}"
    return r.get("error") or ""


def read_jobs(results_dir: Path) -> list[Job]:
    seen: set[tuple[str, str]] = set()
    out = []
    for p in ledger_files(results_dir):
        box = p.stem.removeprefix("ledger_")
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            key = (r.get("id"), r.get("started_at"))
            if key in seen:
                continue
            seen.add(key)
            wall = r.get("wall_s")
            out.append(Job(r["id"], box, r.get("status", "?"), when(r.get("started_at")), when(r.get("ended_at")),
                           (wall or 0.0) * r.get("gpus", 1) / 3600, (r.get("commit") or "")[:7],
                           r.get("gpu_name") or "?", frozenset(run_name(d) for d in r.get("new_results") or []),
                           failure(r), wall is not None))  # fmt: skip
    return out


def job_of(run: str, jobs: list[Job]) -> Job | None:
    mine = [j for j in jobs if run in j.runs] or [j for j in jobs if j.id == run]
    if not mine:
        return None
    done = [j for j in mine if j.status == "done"]
    floor = dt.datetime.min.replace(tzinfo=dt.UTC)
    return max(done or mine, key=lambda j: j.ended or j.started or floor)


# ---------------------------------------------------------------- the page


def on_branch(path: str) -> str:
    """The git ref a path is on ('<ref>:results/...'), else ''."""
    ref, sep, _ = path.partition(":")
    return ref if sep and not path.startswith("results/") else ""


def folder_of(path: str, repo: Path) -> str:
    """The repo-relative folder a run's file is in, if it is here ('' otherwise)."""
    if not path or on_branch(path):
        return ""
    key = RD.run_key(path)
    p = repo / key
    return f"{key}/" if p.is_dir() else key if p.exists() else ""


def link(s: Source, repo: Path) -> str:
    ref = on_branch(s.path)
    if ref:
        return f"`{s.run}` (on {ref})"
    folder = folder_of(s.path, repo)
    return f"[`{s.run}`]({folder})" if folder else f"`{s.run}`"


def reason(verdict: str) -> str:
    inner = verdict.partition("(")[2].removesuffix(")")
    return next((short for key, short in REASONS if key in inner), inner)


def cell(srcs: list[Source], repo: Path) -> str:
    groups: dict[tuple[str, str], list[Source]] = {}
    for s in sorted(srcs, key=lambda s: s.role != "main"):
        groups.setdefault((s.role, s.run), []).append(s)
    parts = []
    for (role, run), ss in groups.items():
        words = list(dict.fromkeys(s.word for s in ss))
        sym = " ".join(G.SYMBOL[w] for w in words)
        why = reason(ss[0].verdict) if words[0] in ("missing", "not testable") else ""
        body = (link(ss[0], repo) + (f" ({why})" if why else "")) if run else (why or words[0])
        parts.append(f"{sym} {body}" if role == "main" else f"{role}: {sym} {body}")
    return "<br>".join(parts)


def jobs_block(srcs: list[Source], jobs: list[Job], repo: Path) -> list[str]:
    runs = list(dict.fromkeys(s.run for s in srcs if s.run))
    rows, elsewhere = [], []
    for run in runs:
        j = job_of(run, jobs)
        s = next(s for s in srcs if s.run == run)
        if j is not None:
            state = "" if j.status == "done" else f" ({j.status}" + (f" at {j.failure}" if j.failure else "") + ")"
            end = f"{j.ended:%d %b %H:%M}" if j.ended else "-"
            rows.append(f"| `{run}` | `{j.id}`{state} | {j.box} | {end} | {j.gpu_hours:.2f} | {j.commit or '-'} |")
        elif on_branch(s.path) or folder_of(s.path, repo):
            elsewhere.append(f"`{run}`")
    out = []
    if rows:
        out += ["Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):", "",
                "| Run | Job | Box | Finished | GPU-hours | Spec commit |", "|---|---|---|---|---|---|", *rows, ""]  # fmt: skip
    if elsewhere:
        out += [f"Not in the queue ledgers (run by hand, before the queue, or on Zach's branch): {', '.join(elsewhere)}.",
                ""]  # fmt: skip
    return out


def night(jobs: list[Job], since: dt.datetime) -> str:
    sel = [j for j in jobs if j.started and j.started >= since]
    if not sel:
        return f"No job in the queue ledgers started since {since:%d %b %H:%M} UTC."
    parts = []
    for box in dict.fromkeys(j.box for j in sel):
        js = [j for j in sel if j.box == box]
        st = collections.Counter(j.status for j in js)
        counts = ", ".join(f"{st[k]} {k}" for k in ("done", "failed", *sorted(set(st) - {"done", "failed"})))
        gpu = " / ".join(collections.Counter(j.gpu_name for j in js))
        parts.append(f"{box} ({gpu}): {len(js)} job{'' if len(js) == 1 else 's'}, {counts}, "
                     f"{sum(j.gpu_hours for j in js):.1f} GPU-hours")  # fmt: skip
    st = collections.Counter(j.status for j in sel)
    last = max(t for j in sel for t in (j.ended, j.started) if t is not None)
    untimed = [f"{j.id} ({j.failure or j.status})" for j in sel if not j.timed]
    return (f"Night of 22-23 Oct, from the queue ledgers: the jobs started from {since:%d %b %H:%M} UTC to the last "
            f"record ({last:%d %b %H:%M} UTC). " + "; ".join(parts) + f". In all {len(sel)} jobs, {st['done']} done, "
            f"{st['failed']} failed, {sum(j.gpu_hours for j in sel):.1f} GPU-hours (wall time x GPUs, failed jobs "
            "included" + (f"; without a wall time in the ledger, not counted: {', '.join(untimed)}" if untimed else "")
            + ").")  # fmt: skip


def build(grid_dir: Path, repo: Path = REPO, since: dt.datetime | None = None) -> str:
    srcs = read_sources(grid_dir)
    jobs = read_jobs(repo / "results")
    gd, root = grid_dir.resolve(), repo.resolve()
    rel = gd.relative_to(root) if gd.is_relative_to(root) else gd
    legend = " · ".join(f"{G.SYMBOL[w]} {w}" for w in G.VERDICTS)
    out = [f"<!-- DRAFT written by scripts/run_table.py from {rel}/sources.txt, grid.csv and results/jobq/ledger_*.jsonl;"
           " links resolve from the repo root -->", "", "# Runs behind the cross-model grid", "",
           f"Each table is one finding of the grid ([grid.md]({rel}/grid.md)), in its order and words. A row is a "
           "setting, a column a model; a cell names the run behind the grid cell, linked to the folder the grid read, "
           f"with the grid's verdict ({legend}). A second line in a cell is a run with another lens, or another run "
           "listed beside the main one. A run that never ran is named without a link, with the reason. Under each "
           "table, the job that wrote each run, from the queue ledgers; a job that failed at its figures step had "
           "finished its run step (exit 0). Nothing here is human-verified.", "",
           night(jobs, since or RD.when(RD.SINCE)), ""]  # fmt: skip
    by_cell: dict[tuple[str, str, str], list[Source]] = collections.defaultdict(list)
    for s in srcs:
        by_cell[(s.finding, s.setting, s.model)].append(s)
    for f in G.FINDINGS:
        title = f"Finding {f.number}: {f.name}" if f.number else f.name
        out += [f"## {title}", "", "| Setting | " + " | ".join(G.MODEL[m].label for m in COLUMNS) + " |",
                "|---|" + "---|" * len(COLUMNS)]  # fmt: skip
        for setting in f.settings:
            out.append(f"| {setting} | " + " | ".join(cell(by_cell[(f.key, setting, m)], repo) for m in COLUMNS) + " |")
        out += ["", *jobs_block([s for s in srcs if s.finding == f.key], jobs, repo)]
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp>/ folder (default: the latest)")
    ap.add_argument("--since", default=RD.SINCE, help="the night: jobs started at or after this time (ISO)")
    ap.add_argument("--out", default=None, help="folder for run_table_<stamp>.md (default: drafts/)")
    ap.add_argument("--repo", default=str(REPO), help=argparse.SUPPRESS)  # tests: a synthetic repo
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    grid_dir = Path(a.grid) if a.grid else RD.latest_grid(repo)
    if grid_dir is None or not (grid_dir / "sources.txt").exists():
        print("no results/cross_model/<stamp>/ with sources.txt and grid.csv: nothing written")
        return 1
    text = build(grid_dir, repo, RD.when(a.since))
    now = dt.datetime.now(dt.UTC)
    out_dir = Path(a.out) if a.out else repo / "drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"run_table_{now:%Y%m%dT%H%M%SZ}.md"
    path.write_text(text)
    print("wrote", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
