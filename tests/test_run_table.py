"""scripts/run_table.py on a synthetic grid folder (sources.txt + grid.csv) and two queue ledgers: the grid's finding
order and the requested model order, one cell per grid setting (breakdown rows dropped, a split setting merged), the
lens listed beside on a second line, links only to folders that exist, the job behind each run, and the night's counts
with a job copied into two ledgers counted once."""

import csv
import io
import json

import pytest

from scripts import cross_model_grid as G
from scripts import run_table as RT

F = {k: G.FINDING[k].name for k in ("f1", "f2", "f4", "f5")}
M = {k: G.MODEL[k].label for k in ("27b", "olmo_hybrid", "122b", "gemma")}
BESIDE = "plain J-lens, published (plain J-lens, listed beside)"
D1 = "results/d1_verdict/runA_20261022-185412/verdict.json"
F5 = "results/finding5_confirm/runD_20261023-010203/verdict.json"
ROWS = [  # model, finding, setting, role, run, files, grid.csv lens, verdict
    ("27b", "f1", "tasks, Zach's rule", "main", "full2", "origin/zach/x:results/ablate_v2/c1_v2/full2.json", "J++",
     "holds"),
    ("27b", "f2", "draw 1", "main", "runA", D1, "J++", "holds"),
    ("27b", "f2", "draw 1 · animals", "main", "runA", D1, "J++", "fails"),  # a breakdown row: not a cell
    ("27b", "f2", "draw 1", "plain J-lens", "runB", "results/statement_positions/runB/outcomes.jsonl", BESIDE,
     "not interpretable (the positive control fails)"),
    ("olmo_hybrid", "f2", "draw 1", "main", "-", "-", "", "not testable (no lens)"),
    ("122b", "f5", "draw 1, 1st-2nd", "main", "runD", F5, "none", "fails (partly: A True, B False)"),
    ("122b", "f5", "draw 1, 3rd on", "main", "runD", F5, "none", "fails (partly: A True, B False)"),
    ("gemma", "f4", "long context", "main", "runE", "results/attn_knockout/runE/rows.jsonl", "none",
     "missing (job runE_r2 failed at the run stage (exit 1))"),
]  # fmt: skip


def job(id_, start, end, wall, commit, gpu, new, status="done", gpus=1, **kw):
    return json.dumps({"id": id_, "status": status, "started_at": start, "ended_at": end, "wall_s": wall, "gpus": gpus,
                       "commit": commit, "gpu_name": gpu, "new_results": new, "exit_code": 0 if status == "done" else 1,
                       **kw})  # fmt: skip


@pytest.fixture
def repo(tmp_path):
    grid = tmp_path / "results/cross_model/20990101T000000Z"
    grid.mkdir(parents=True)
    lines, buf = [], io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(G.COLUMNS)
    for m, f, s, role, run, files, lens, verdict in ROWS:
        lines.append(f"{M[m]} | {F[f]} | {s} | {role} | {run} | {files}")
        w.writerow([M[m], F[f], s, lens, "", "", "", "", verdict, "", "", ""])
    (grid / "sources.txt").write_text("\n".join(lines) + "\n")
    (grid / "grid.csv").write_text(buf.getvalue())
    for path in (D1, F5, "results/attn_knockout/runE/rows.jsonl"):
        (tmp_path / path).parent.mkdir(parents=True)
        (tmp_path / path).write_text("{}\n")
    old = job("old", "2026-10-21T10:00:00+00:00", "2026-10-21T11:00:00+00:00", 3600, "1111111", "A100", ["x/old"])
    jq = tmp_path / "results/jobq"
    jq.mkdir()
    (jq / "ledger_boxa.jsonl").write_text("\n".join([
        old,
        job("runA", "2026-10-22T20:00:00+00:00", "2026-10-22T21:00:00+00:00", 3600, "abcdef0123", "A100",
            ["statement_positions/runA", "d1_verdict/runA_20261022-185412"]),
        job("runE_r2", "2026-10-23T01:00:00+00:00", "2026-10-23T01:30:00+00:00", 1800, "2222222", "A100",
            ["attn_knockout/runE"], status="failed"),
        job("died", "2026-10-23T00:00:00+00:00", "2026-10-23T05:00:00+00:00", None, "4444444", "A100", [],
            status="failed", exit_code=None, error="worker died during the run"),  # no wall time: not counted
    ]) + "\n")  # fmt: skip
    (jq / "ledger_boxb.jsonl").write_text("\n".join([
        old,  # the seeded copy: counted once, under boxa
        job("runD_b16", "2026-10-23T02:00:00+00:00", "2026-10-23T02:30:00+00:00", 1800, "3333333", "H200",
            ["finding5_confirm/runD_20261023-010203", "pointer_swap/runD"], gpus=2),
    ]) + "\n")  # fmt: skip
    return tmp_path


def sections(text: str) -> dict[str, str]:
    return {s.split("\n", 1)[0]: s for s in text.split("\n## ")[1:]}


def row(section: str, setting: str) -> list[str]:
    line = next(x for x in section.splitlines() if x.startswith(f"| {setting} |"))
    return [c.strip() for c in line.split("|")[2:-1]]  # cells hold no "|"


def test_tables_follow_the_grid_and_the_requested_model_order(repo):
    text = RT.build(repo / "results/cross_model/20990101T000000Z", repo)
    titles = list(sections(text))
    want = [f"Finding {f.number}: {f.name}" if f.number else f.name for f in G.FINDINGS]
    assert titles == want and titles.index(G.FINDING["gate"].name) == 6  # the gate between findings 6 and 7
    head = (
        "| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | "
    )
    assert text.count(head + "Gemma 4 31B-it |") == len(G.FINDINGS)


def test_cells_name_the_runs_with_their_verdicts(repo):
    sec = sections(RT.build(repo / "results/cross_model/20990101T000000Z", repo))
    f2 = sec[f"Finding 2: {F['f2']}"]
    cells = row(f2, "draw 1")
    assert cells[0] == "✓ [`runA`](results/d1_verdict/runA_20261022-185412/)<br>plain J-lens: ⚠ `runB`"  # no folder
    assert cells[2] == "⊘ no lens" and cells[1] == ""
    assert "· animals" not in f2 and "✗" not in f2  # the breakdown row's verdict is not a cell
    assert (
        row(sec[f"Finding 5: {F['f5']}"], "draw 1")[3] == "✗ [`runD`](results/finding5_confirm/runD_20261023-010203/)"
    )
    assert row(sec[f"Finding 1: {F['f1']}"], "tasks, Zach's rule")[0] == "✓ `full2` (on origin/zach/x)"
    assert row(sec[f"Finding 4: {F['f4']}"], "long context")[7] == "· [`runE`](results/attn_knockout/runE/) (failed)"


def test_jobs_come_from_the_ledgers(repo):
    text = RT.build(repo / "results/cross_model/20990101T000000Z", repo)
    sec = sections(text)
    assert "| `runA` | `runA` | boxa | 22 Oct 21:00 | 1.00 | abcdef0 |" in sec[f"Finding 2: {F['f2']}"]
    assert "| `runD` | `runD_b16` | boxb | 23 Oct 02:30 | 1.00 | 3333333 |" in sec[f"Finding 5: {F['f5']}"]
    assert "| `runE` | `runE_r2` (failed at run, exit 1) | boxa | 23 Oct 01:30 | 0.50 | 2222222 |" in text
    assert "on Zach's branch): `full2`." in sec[f"Finding 1: {F['f1']}"]
    assert "| `runB` |" not in text and "`runB`." not in text  # never ran here: named in its cell only
    night = next(x for x in text.splitlines() if x.startswith("Night of 22-23 Oct"))
    assert "from 22 Oct 19:30 UTC to the last record (23 Oct 05:00 UTC)" in night
    assert "boxa (A100): 3 jobs, 1 done, 2 failed, 1.5 GPU-hours; boxb (H200): 1 job, 1 done, 0 failed, 1.0" in night
    assert "In all 4 jobs, 2 done, 2 failed, 2.5 GPU-hours" in night  # "old" (21 Oct, in both ledgers) not counted
    assert "not counted: died (worker died during the run))." in night


def test_a_sources_row_without_its_grid_csv_row_stops(repo):
    grid = repo / "results/cross_model/20990101T000000Z"
    with open(grid / "sources.txt", "a") as f:
        f.write(f"{M['27b']} | {F['f2']} | draw 2 | main | runX | -\n")
    with pytest.raises(ValueError, match=r"no grid\.csv row"):
        RT.read_sources(grid)


def test_main_writes_a_draft(repo, capsys):
    assert RT.main(["--repo", str(repo), "--grid", str(repo / "results/cross_model/20990101T000000Z")]) == 0
    (out,) = (repo / "drafts").glob("run_table_*.md")
    assert (
        out.read_text().startswith("<!-- DRAFT written by scripts/run_table.py") and "wrote" in capsys.readouterr().out
    )
