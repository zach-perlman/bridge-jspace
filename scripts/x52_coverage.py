"""x52_coverage (batch 52 part C, jobs/c3/batch52.yaml with amendments 1-3): the model-coverage matrix, the full grid
(amendment 2): rows = every test with a card or claim on the depth page (the 10 key rows first, in Dan's order), columns
= 27B / Lightning / 9B / Muse, each cell done / partial / running / queued / missing / not tested / not designed with the
reason and the result folder or verdict it rests on; Bolt one line, out of scope.

Two kinds of cell. Fixed cells (`done` / `c`) cite committed verdicts, typed by hand. Coverage cells (`track`) resolve
from the checkout when the script runs: done when a verdict folder that names the run exists, partial when the run landed
but no verdict reads it yet, else the job ledgers' status (results/jobq/ledger_*.jsonl: failed with its exit code, or
done on the box and not pulled), else queued. Row 4's doses are read from each x8_write verdict.md (the 'write | s | all'
target share), not typed. Every cited path is checked to exist; writes results/x52_coverage/matrix-<UTC>/matrix.{md,json}
(a new folder each run). CPU only.

uv run python scripts/x52_coverage.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

RES = pins.RESULTS_DIR
OUT = RES / "x52_coverage"
JOBS = pins.REPO_ROOT / "jobs" / "c3"
MODELS = ("qwen3.6-27b", "nemotron-3.5-lightning", "qwen3.5-9b", "muse-glimmer-30b")
SHORT = {"qwen3.6-27b": "27B", "nemotron-3.5-lightning": "Lightning", "qwen3.5-9b": "9B", "muse-glimmer-30b": "Muse"}
STATUS = ("done", "partial", "running", "queued", "missing", "not tested", "not designed")
BOLT = ("Nemotron 3.5 Bolt: out of scope: only a J-lens exists, no J++ lens (amendment 2; every depth test uses J++ "
        "atoms). Checked 28 Oct ~23:15 UTC: no J++ file under cache/nemotron-3.5-bolt/lenses/jpp/ on mats, speedup or "
        "another; the H200 box it was fit on is unreachable")  # fmt: skip
LT_GATE = ("Lightning's gate: the main test's gate on all 516 scenes (lookup 0.957, recall 0.816), chosen after the "
           "60-scene pre-check was seen (lookup 0.883, recall 0.783: failed) — hollow mark (Dan 01:10); layer L14 by "
           "amendment 1 (results/x51_lightning/nem35l_x52_layer_r2); every Lightning cell carries it")  # fmt: skip
# reasons (the cell's status word is printed before them)
CLEAN = "the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change)"
CLEAN_SRC = "results/x0_necessity/nem35l_x45s_smoke_clean/gate.json"
# specs written overnight but deliberately not enqueued (held for Dan): without this the cell would read "queued"
HELD: dict[str, str] = {}  # x47_16_muse_r2 was held until Dan's 09:05 decision 24 (run it now; enqueued on mats)
NO_KO = "the edge knock-out (knockout.py) is not ported to NemotronH's Mamba-2 blocks"
NO_DAS = ("DAS trains through the model's backward, unverified through NemotronH's Mamba-2 kernels; its recall half "
          "needs the clean design (gate fails)")  # fmt: skip
NOT_DESIGNED_LT = "the test was designed for the 9B and 27B; amendment 2's grid adds no new design"
NOT_DESIGNED_MUSE = "designed for the 9B and 27B (conservative, Dan 01:10)"


def c(status: str, note: str = "", *sources: str) -> dict:
    assert status in STATUS, status
    return {"status": status, "note": note, "sources": list(sources)}


def done(*sources: str, note: str = "") -> dict:
    return c("done", note, *sources)


# ---- coverage cells resolved at build time --------------------------------------------------------------------------


def ledger() -> dict[str, dict]:
    """Job id -> its last ledger entry over every box (results/jobq/ledger_*.jsonl, pulled by the coordinator)."""
    last: dict[str, dict] = {}
    for f in sorted((RES / "jobq").glob("ledger_*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                e = json.loads(line)
                if e.get("id") and (
                    e["id"] not in last or str(e.get("ended_at")) >= str(last[e["id"]].get("ended_at"))
                ):
                    last[e["id"]] = e | {"ledger": f.name}
    return last


LEDGER: dict[str, dict] = {}


def rel(p: Path) -> str:
    return str(p.relative_to(pins.REPO_ROOT))


def names(folder: Path, mention: str) -> bool:
    """Whether a verdict folder's own json / md files name the run (a verdict over the run)."""
    return any(mention in f.read_text(errors="ignore") for f in folder.iterdir() if f.suffix in (".json", ".md"))


# what a run writes before its GPU results (a job killed or failed after its gate leaves only these)
SETUP_FILES = {"manifest.json", "plan.json", "cases.jsonl", "competence.jsonl", "gate.json", "coverage.txt",
               "status.json", "cues.json", "items.jsonl"}  # fmt: skip


def landed(run_dir: Path) -> bool:
    """A run folder that holds results, not only its setup files (SETUP_FILES): any other file (outcomes, states,
    reads, ablations) or a result subfolder (verdict-*, probe-*, x45d-*)."""
    return any(p.is_dir() or p.name not in SETUP_FILES for p in run_dir.iterdir())


def gate_failed(g: dict) -> bool:
    """A gate.json that did not pass: its own 'pass' is false, or (per placement / condition, nested, as 47.15's and
    47.7's) no nested gate passed while at least one was read."""
    if "pass" in g:
        return g["pass"] is False
    passes, todo = [], [v for v in g.values() if isinstance(v, dict)]
    while todo:
        d = todo.pop()
        if "pass" in d:
            passes.append(bool(d["pass"]))
        else:
            todo += [v for v in d.values() if isinstance(v, dict)]
    return bool(passes) and not any(passes)


def track(specs: str | tuple[str, ...] | None, run: str | None, verdict: str | None, note: str = "",
          mention: str | None = None, done_as: str = "done", gate_fail: bool = False) -> dict:  # fmt: skip
    """A coverage cell. `run`: '<exp>/<run folder glob>' under results/; `verdict`: '<exp>/<folder glob>' ('{run}' is the
    run folder's name), a folder that names `mention` (default the run's name); `specs`: the job spec id(s) behind it.
    `done_as`: 'partial' where the cell is half a row by design (the reason in `note`). `gate_fail`: the run's gate.json
    'pass' false with no outcomes reads 'not tested'."""
    specs = (specs,) if isinstance(specs, str) else tuple(specs or ())
    spec_paths = [rel(JOBS / f"{s}.yaml") for s in specs if (JOBS / f"{s}.yaml").exists()]
    runs = sorted(RES.glob(run)) if run else []
    run_dir = runs[-1] if runs else None
    if gate_fail and run_dir is not None and not (run_dir / "outcomes.jsonl").exists():
        g = json.loads((run_dir / "gate.json").read_text()) if (run_dir / "gate.json").exists() else {}
        if gate_failed(g):
            why = (f"({g.get('org_read_accuracy')}, eligible {g.get('eligible')})" if "pass" in g
                   else "(no placement / condition passed; see gate.json)")  # fmt: skip
            return c("not tested", f"its gate failed {why}; no lowered rerun (the spec's rule)"
                     + (f"; {note}" if note else ""), rel(run_dir / "gate.json"))  # fmt: skip
    if verdict:
        pat = verdict.replace("{run}", run_dir.name if run_dir is not None else "<none>")
        key = mention or (run_dir.name if run_dir is not None else None)
        found = [p for p in sorted(RES.glob(pat)) if p.is_dir() and key and ("{run}" in verdict or names(p, key))]
        if found:
            return c(
                done_as, note, rel(found[-1]), *([rel(run_dir)] if run_dir is not None and landed(run_dir) else [])
            )
    elif run_dir is not None and landed(run_dir):
        return c(done_as, note, rel(run_dir))
    if run_dir is not None and landed(run_dir):
        return c("partial", "the run landed; its coverage verdict is not written yet" + (f"; {note}" if note else ""),
                 rel(run_dir), *spec_paths)  # fmt: skip
    if run_dir is not None:  # a folder without outcomes: a job in progress, or one killed / failed
        bad = next((f"{s} {LEDGER[s].get('status')} (exit {LEDGER[s].get('exit_code')}, {LEDGER[s]['ledger']})"
                    for s in reversed(specs) if LEDGER.get(s, {}).get("status") not in (None, "done")), None)  # fmt: skip
        if bad:
            return c("missing", f"the run folder holds no outcomes; {bad}" + (f"; {note}" if note else ""),
                     rel(run_dir), *spec_paths)  # fmt: skip
        return c("running", "the run folder holds no outcomes yet" + (f"; {note}" if note else ""), rel(run_dir),
                 *spec_paths)  # fmt: skip
    for s in reversed(specs):
        e = LEDGER.get(s)
        if e and e.get("status") not in (None, "done"):
            return c("missing", f"{s} {e.get('status')} (exit {e.get('exit_code')}, {e['ledger']}); retried once, then "
                     "skipped with the reason logged (Dan 01:10)" + (f"; {note}" if note else ""), *spec_paths)  # fmt: skip
        if e and e.get("status") == "done":
            return c("running", f"{s} done on {e.get('host')} ({e['ledger']}); results not pulled here yet"
                     + (f"; {note}" if note else ""), *spec_paths)  # fmt: skip
    held = [s for s in specs if s in HELD]
    if held:
        return c("missing", f"{', '.join(held)} written, not enqueued: {HELD[held[-1]]}" + (f"; {note}" if note else ""),
                 *spec_paths)  # fmt: skip
    if spec_paths:
        return c("queued", f"{', '.join(specs)} (queued or running; no ledger entry here yet)" + (f"; {note}" if note else ""),
                 *spec_paths)  # fmt: skip
    return c("missing", note or "no spec")


def dose_note(verdict_md: str) -> str:
    """Row 4: the target share at s = 1 / 2 / 4 over all pairs, read from an x8_write verdict.md ('| write | s | all |')."""
    text = (pins.REPO_ROOT / verdict_md).read_text()
    vals = {s: re.search(rf"^\| write \| {s} \| all \| \d+ \| ([0-9.]+) ", text, re.M) for s in (1, 2, 4)}
    assert all(vals.values()), f"{verdict_md}: no 'write | s | all' row for every s"
    return " / ".join(vals[s].group(1) for s in (1, 2, 4))


def write_cell(fixed: str | None = None, **tracked) -> dict:
    """Row 4's cell: a fixed verdict (the three design models) or a tracked Lightning run, the doses read from it."""
    cell = done(fixed) if fixed else track(**tracked)
    if cell["status"] == "done":
        md = next(s for s in cell["sources"] if "verdict-" in s) + "/verdict.md"
        cell["note"] = f"target share at s = 1 / 2 / 4: {dose_note(md)}" + (f"; {cell['note']}" if cell["note"] else "")
    return cell


def parts(**cells: dict) -> dict:
    """A cell made of named parts (e.g. Z1 and Z2): done when every part is done, partial when some are (the rest named
    with their own status), else the first part's cell with the others' status in its note."""
    st = {k: v["status"] for k, v in cells.items()}
    srcs = [s for v in cells.values() for s in v["sources"]]
    if all(s == "done" for s in st.values()):
        return c("done", "; ".join(f"{k} done" for k in cells), *srcs)
    if any(s in ("done", "partial") for s in st.values()):
        return c("partial", "; ".join(f"{k} {v['status']}" + (f" ({v['note']})" if v["note"] else "")
                                      for k, v in cells.items()), *srcs)  # fmt: skip
    first = next(iter(cells.values()))
    return c(first["status"], "; ".join(f"{k} {v['status']}" + (f" ({v['note']})" if v["note"] else "")
                                        for k, v in cells.items()), *srcs)  # fmt: skip


LT = "nemotron-3.5-lightning"


def rows() -> list[tuple[str, str, dict]]:
    """(row, rule / design source, {model: cell}); key rows 1-10 first (Dan's order), then the rest of the depth page."""
    return [
        ("1. Conflict test (main test, at L)", "X0 (jobs/c3/x0_necessity_27b_chat.yaml)", {
            "qwen3.6-27b": done("results/x0_necessity/x0_necessity_27b_chat/verdict-20261024T135446Z",
                                note="not confirmed (lookup 0.14 > 0.10; recall 0.74)"),
            LT: track("x52_lightning_conflict", "x0_necessity/nem35l_x52_conflict", "x0_necessity/{run}/verdict-*",
                   "decided at L14; 3 arms at all 13 swept layers"),
            "qwen3.5-9b": done("results/x0_necessity/qwen35_9b_x0_necessity/verdict-20261024T135419Z", note="confirmed"),
            "muse-glimmer-30b": done("results/x0_necessity/muse30b_x0_necessity/verdict-20261026T001148Z", note="confirmed")}),
        ("2. Answer control (51.12 E1)", "jobs/c3/batch51.yaml 51.12 r2", {
            "qwen3.6-27b": done("results/x51_answer/x51_12-20261028T201842Z", note="recall: the entity"),
            # pinned: later x52_answer-* verdicts (other sets) also name this run but list its E1 cell as pending
            LT: track("x52_lightning_answer", "x51_answer/nem35l_x52_answer", "x51_answer/x52_answer-20261029T002056Z"),
            "qwen3.5-9b": done("results/x51_answer/x51_12-20261028T201842Z", note="recall: the entity"),
            "muse-glimmer-30b": done("results/x51_answer/x51_12-20261028T201842Z", note="answer word not read")}),
        ("3. Routes test (identity / position / value; no address; address alone)", "x6_routes (E5/E6)", {
            "qwen3.6-27b": done("results/x6_routes/x6_routes_27b/verdict-20261025T105901Z",
                                "results/x6_routes/x6_routes_keeponly_27b", note="0.66 / 0.34 / 0.00; alone fails"),
            LT: track("x52_lightning_routes", "x6_routes/nem35l_x52_routes", "x6_routes/{run}/verdict-*"),
            "qwen3.5-9b": done("results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z",
                               "results/x6_routes/qwen35_9b_x6_routes_keeponly"),
            "muse-glimmer-30b": done("results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z")}),
        ("4. Address swap by dose (x8_write, s = 1 / 2 / 4)", "x8_write (Q44.1-3)", {
            "qwen3.6-27b": write_cell("results/x8_write/x8_write_27b/verdict-20261026T125548Z"),
            LT: write_cell(specs="x52_lightning_write", run="x8_write/nem35l_x52_write", verdict="x8_write/{run}/verdict-*"),
            "qwen3.5-9b": write_cell("results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z"),
            "muse-glimmer-30b": write_cell("results/x8_write/muse30b_x8_write/verdict-20261026T141141Z")}),
        ("5a. Order split (descriptive)", "x0_composition split-by-order", {
            "qwen3.6-27b": done("results/x0_composition/split-by-order-20261026T173323Z"),
            LT: track(None, "x0_necessity/nem35l_x52_conflict", "x0_composition/split-by-order-*",
                   "CPU from the conflict test's outcomes", mention="nem35l_x52_conflict"),
            "qwen3.5-9b": done("results/x0_composition/split-by-order-20261026T173323Z"),
            "muse-glimmer-30b": done("results/x0_composition/split-by-order-20261026T173323Z")}),
        ("5b. Copy test (45q)", "jobs/c3/batch45.yaml 45b/45q", {
            "qwen3.6-27b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds"),
            LT: c("not tested", CLEAN, CLEAN_SRC),
            "qwen3.5-9b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds"),
            "muse-glimmer-30b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds")}),
        ("6. Anatomy by layer (47.8)", "jobs/c3/batch47.yaml 47.8", {
            "qwen3.6-27b": track("x47_8_27b", "x47_anatomy/x47_anatomy_27b", "x47_anatomy/x52_anatomy-*", "full grid"),
            LT: track("x52_lightning_anatomy", "x47_anatomy/nem35l_x52_anatomy", "x47_anatomy/x52_anatomy-*",
                   "every 4th layer L2-L50"),
            "qwen3.5-9b": done("results/x47_anatomy/x47_8-20261028T154518Z"),
            "muse-glimmer-30b": done("results/x47_anatomy/x47_8-20261028T154518Z")}),
        ("7. Ladder (49.2, rungs 1-6)", "jobs/c3/batch49.yaml 49.2", {
            "qwen3.6-27b": track(("x52_ladder_27b", "x52_ladder_27b_a", "x52_ladder_27b_s"), "x49_ladder/x52_ladder_27b*",
                                 "x49_ladder/x52_ladder-*", "rungs 1-6, rung 6 at Zach's L32-40",
                                 mention="x52_ladder_27b"),
            LT: c("not tested", CLEAN, CLEAN_SRC),
            "qwen3.5-9b": done("results/x49_ladder/x49_2-20261028T161612Z"),
            "muse-glimmer-30b": track(("x52_ladder_muse", "x52_ladder_muse_r2", "x52_ladder_muse_r3"),
                                      "x49_ladder/muse30_x52_ladder", "x49_ladder/x52_ladder-*",
                                      "rung 6 in Zach's L36-42 (49.2 ran it at L23-29)")}),
        ("8. Lens readout with the item-change control (47.0)", "47.0 (descriptive)", {
            "qwen3.6-27b": done("results/x47_verbal/summary-20261028T033646Z"),
            LT: track("x52_lightning_verbal", "x47_verbal/nem35l_x52_verbal", "x47_verbal/summary-*"),
            "qwen3.5-9b": done("results/x47_verbal/summary-20261028T033646Z"),
            "muse-glimmer-30b": done("results/x47_verbal/summary-20261028T033646Z")}),
        ("9. Last-token read / write (51.10)", "jobs/c3/batch51.yaml addendum_2", {
            "qwen3.6-27b": done("results/x51_jread/x51_10-20261028T190608Z"),
            LT: track("x52_lightning_jread", "x51_jread/nem35l_x52_jread", "x51_jread/x52_jread-*"),
            "qwen3.5-9b": done("results/x51_jread/x51_10-20261028T190608Z"),
            "muse-glimmer-30b": done("results/x51_jread/x51_10-20261028T190608Z")}),
        ("10. Attention under the swap (49.7)", "jobs/c3/batch49.yaml 49.7", {
            "qwen3.6-27b": done("results/x49_attn/x49_7-20261028T154511Z"),
            LT: track("x52_lightning_attn", "x49_attn/nem35l_x52_attn", "x49_attn/x52_attn-*",
                   "attention blocks 19 / 26 / 33 / 42 after L14 (6 of 52 blocks)"),
            "qwen3.5-9b": done("results/x49_attn/x49_7-20261028T154511Z"),
            "muse-glimmer-30b": done("results/x49_attn/x49_7-20261028T154511Z")}),
        # ---- the rest of the depth page (cards, claims, Part VI, appendix figures) --------------------------------
        ("Split in other texts: varied scenes (x0b)", "x0b_generalize", {
            "qwen3.6-27b": done("results/x0b_generalize/x0b_v2_27b"),
            LT: track("x52_lightning_varied", "x0b_generalize/nem35l_x52_x0b", "x0b_generalize/{run}/verdict-*"),
            "qwen3.5-9b": done("results/x0b_generalize/qwen35_9b_x0b_v2"),
            "muse-glimmer-30b": done("results/x0b_generalize/muse30b_x0b_v2")}),
        ("Split in other texts: natural passages (x5)", "x5_natural", {
            "qwen3.6-27b": done("results/x5_natural/x5_natural_27b"),
            LT: track("x52_lightning_natural", "x5_natural/nem35l_x52_natural", "x5_natural/{run}/verdict-*", gate_fail=True),
            "qwen3.5-9b": done("results/x5_natural/qwen35_9b_x5_natural_g75", note="gate lowered after the data"),
            "muse-glimmer-30b": done("results/x5_natural/muse30b_x5_natural")}),
        ("Dose curves, a part alone (51.1)", "jobs/c3/batch51.yaml 51.1", {
            "qwen3.6-27b": done("results/x51_dose/x51_1-20261028T170335Z"),
            LT: track("x52_lightning_dose", "x51_dose/nem35l_x52_dose", "x51_dose/x52_dose-*"),
            "qwen3.5-9b": done("results/x51_dose/x51_1-20261028T170335Z"),
            "muse-glimmer-30b": done("results/x51_dose/x51_1-20261028T170335Z")}),
        ("Zeroing at one layer (47.5)", "jobs/c3/batch47.yaml 47.5", {
            "qwen3.6-27b": done("results/x47_zero/x47_5-20261028T113106Z"),
            LT: track("x52_lightning_zero", "x47_zero/nem35l_x52_zero", "x47_zero/x52_zero-*",
                      "L14 and L14..17; the 60 dev scenes kept out"),
            "qwen3.5-9b": done("results/x47_zero/x47_5-20261028T113106Z"),
            "muse-glimmer-30b": done("results/x47_zero/x47_5-20261028T113106Z")}),
        ("Earlier mention (45p)", "jobs/c3/batch45.yaml 45p", {
            "qwen3.6-27b": done("results/x45p/x45p-20261027T012017Z"), LT: c("not tested", CLEAN, CLEAN_SRC),
            "qwen3.5-9b": done("results/x45p/x45p-20261027T012017Z"), "muse-glimmer-30b": done("results/x45p/x45p-20261027T012017Z")}),
        ("E3: identity route outside the lens (47.1 atom slices)", "jobs/c3/batch47.yaml 47.1", {
            "qwen3.6-27b": done("results/x47_atoms/x47_1-20261028T113101Z"),
            LT: track("x52_lightning_atoms47", "x0_necessity/nem35l_x52_x47_1_main", "x47_atoms/x52_atoms47-*"),
            "qwen3.5-9b": done("results/x47_atoms/x47_1-20261028T113101Z"),
            "muse-glimmer-30b": done("results/x47_atoms/x47_1-20261028T113101Z")}),
        ("E6: the address probe (x0_probe v4)", "x0_probe", {
            "qwen3.6-27b": done("results/x0_probe/x0_probe_v4_27b"),
            LT: track("x52_lightning_probe", "x0_probe/nem35l_x52_probe", "x0_probe/{run}/probe-*"),
            "qwen3.5-9b": done("results/x0_probe/qwen35_9b_x0_probe_v4"),
            "muse-glimmer-30b": done("results/x0_probe/muse30b_x0_probe_v4")}),
        ("E6: the swap after neutral sentences (47.16 distance)", "jobs/c3/batch47.yaml 47.16", {
            "qwen3.6-27b": track("x52_27b_gaps_a", "x47_distance/x47_16_27b", "x47_distance/x52_distance-*"),
            LT: track("x52_lightning_fill1", "x47_distance/nem35l_x52_distance", "x47_distance/x52_distance-*"),
            "qwen3.5-9b": done("results/x47_distance/x47_16-20261028T131501Z"),
            "muse-glimmer-30b": track("x47_16_muse_r2", "x47_distance/muse30_x47_16_r2",
                                      "x47_distance/x52_distance-*", "x47_16_muse was cancelled by Dan mid-run (batch 49 "
                                      "amendment 1; no outcomes); r2 re-opens it under amendment 2 (flagged)")}),
        ("E7: six lockers, one code per slot (47.2)", "jobs/c3/batch47.yaml 47.2", {
            "qwen3.6-27b": track(("x47_2_27b", "x47_2_27b_r2", "x47_2_27b_r3", "x47_2_27b_r4"), "x47_six/x47_2_27b*",
                                 "x47_six/x52_six-*"),
            LT: track("x52_lightning_six", "x47_six/nem35l_x52_six", "x47_six/x52_six-*"),
            "qwen3.5-9b": done("results/x47_six/x47_2-20261028T113102Z"),
            "muse-glimmer-30b": done("results/x47_six/x47_2-20261028T113102Z")}),
        ("E8: the report prompt (47.10)", "jobs/c3/batch47.yaml 47.10", {
            "qwen3.6-27b": done("results/x47_report/x47_10-20261028T113109Z"),
            LT: track("x52_lightning_fill2", "x47_report/nem35l_x52_report", "x47_report/x52_report-*"),
            "qwen3.5-9b": done("results/x47_report/x47_10-20261028T113109Z"),
            "muse-glimmer-30b": done("results/x47_report/x47_10-20261028T113109Z")}),
        ("E11: token by layer map (47.D1)", "jobs/c3/batch47.yaml D1", {
            "qwen3.6-27b": track("x47_d1_27b", "x47_depthmap/x47_depthmap_27b", "x47_depthmap/x52_depthmap-*"),
            LT: track("x52_lightning_depthmap", "x47_depthmap/nem35l_x52_depthmap", "x47_depthmap/x52_depthmap-*",
                   "the main design only; the clean design (the decisive cell) not tested: gate fails", done_as="partial"),
            "qwen3.5-9b": done("results/x47_depthmap/depth-20261028T120525Z"),
            "muse-glimmer-30b": done("results/x47_depthmap/depth-20261028T120525Z")}),
        ("E11: lookups carried before L (47.4 cumulative)", "jobs/c3/batch47.yaml 47.4", {
            "qwen3.6-27b": track("x52_27b_gaps_a", "x47_cumulative/x47_cumulative_27b", "x47_cumulative/x52_cumulative-*"),
            LT: track("x52_lightning_fill4", "x47_cumulative/nem35l_x52_cumulative", "x47_cumulative/x52_cumulative-*",
                   "the main design only; the clean design not tested: gate fails", done_as="partial"),
            "qwen3.5-9b": done("results/x47_cumulative/x47_4-20261028T113105Z"),
            "muse-glimmer-30b": done("results/x47_cumulative/x47_4-20261028T113105Z")}),
        ("E12: address persistence across depth (D4, CPU)", "jobs/c3/batch47.yaml D4", {
            "qwen3.6-27b": track(None, "x47_anatomy/x47_anatomy_27b", "x47_depth_cpu/persistence-*",
                                 "CPU from x47_anatomy_27b's cache", mention="x47_anatomy_27b"),
            LT: track(None, "x47_anatomy/nem35l_x52_anatomy", "x47_depth_cpu/persistence-*",
                   "CPU from Lightning's anatomy cache (on its box)", mention="nem35l_x52_anatomy"),
            "qwen3.5-9b": done("results/x47_depth_cpu/persistence-20261028T115530Z"),
            "muse-glimmer-30b": done("results/x47_depth_cpu/persistence-20261028T115530Z")}),
        ("Part V: Zach's passages Z1 / Z2 (x50)", "jobs/c3/batch50 (x50_zach)", {
            "qwen3.6-27b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z"),
            LT: parts(Z1=track("x52_lightning_zach", "x50_zach/nem35l_x52_z1", "x50_zach/x52_z1-*", "L14 and L27"),
                      Z2=track("x52_lightning_z2", "x50_zach/nem35l_x52_z2", "x50_zach/x52_z2-*", "L14 and L27")),
            "qwen3.5-9b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z"),
            "muse-glimmer-30b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z")}),
        ("Part V: Zach's passages Z3 (routes on his passages)", "x50_zach z3", {
            "qwen3.6-27b": track("x52_27b_z3", "x50_zach/x50_z3_27b", "x50_zach/x52_z3-*",
                                 "at L32 (X0's layer = the start of his band L32-40)"),
            LT: track("x52_lightning_zach", "x50_zach/nem35l_x52_z3", "x50_zach/x52_z3-*", "at L14 and L27"),
            "qwen3.5-9b": done("results/x50_zach/z3-20261028T163053Z"), "muse-glimmer-30b": done("results/x50_zach/z3-20261028T163053Z")}),
        ("Described bridge (47.3, and 51.12's cue r2)", "jobs/c3/batch47.yaml 47.3", {
            "qwen3.6-27b": done("results/x47_cue/x47_3-20261028T113104Z", "results/x51_answer/x51_12-20261028T201842Z"),
            LT: parts(**{"47.3": track("x52_lightning_fill2", "x47_cue/nem35l_x52_cue", "x47_cue/x52_cue-*"),
                         "51.12 cue r2": track("x52_lightning_cue_answer", "x51_answer/nem35l_x52_cue_answer",
                                               "x51_answer/x52_answer-*")}),
            "qwen3.5-9b": done("results/x47_cue/x47_3-20261028T113104Z", "results/x51_answer/x51_12-20261028T201842Z"),
            "muse-glimmer-30b": c("partial", "47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design)",
                                  "results/x47_cue/x47_3-20261028T113104Z")}),
        ("Report of slot 1, reworded (49.6)", "jobs/c3/batch49.yaml 49.6", {
            "qwen3.6-27b": done("results/x49_report/x49_6-20261028T154511Z"),
            LT: track("x52_lightning_report49", "x49_report/nem35l_x52_report49", "x49_report/x52_report49-*",
                      "the 9B / 27B design; read per model, the action is the 9B's"),
            "qwen3.5-9b": done("results/x49_report/x49_6-20261028T154511Z", note="the deciding model"),
            "muse-glimmer-30b": c("not designed", NOT_DESIGNED_MUSE)}),
        ("Address refit per text format (x45d)", "x45d", {
            "qwen3.6-27b": done("results/x0b_generalize/x45d_27b"),
            LT: track("x52_lightning_fill5", "x0b_generalize/nem35l_x52_x45d", "x0b_generalize/{run}/x45d-*"),
            "qwen3.5-9b": done("results/x0b_generalize/qwen35_9b_x45d"), "muse-glimmer-30b": done("results/x0b_generalize/muse30b_x45d")}),
        ("The lookup's errors are not address errors (47.13)", "jobs/c3/batch47.yaml 47.13", {
            "qwen3.6-27b": done("results/x47_errors/x47_13-20261028T113107Z"),
            LT: track("x52_lightning_fill5", "x47_errors/nem35l_x52_errors-gpu-*", "x47_errors/x47_13-*",
                   "count (CPU) then the verdict", mention="nem35l_x52_errors"),
            "qwen3.5-9b": done("results/x47_errors/x47_13-20261028T113107Z"),
            "muse-glimmer-30b": done("results/x47_errors/x47_13-20261028T113107Z")}),
        ("Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment)", "jobs/c3/batch48.yaml 48.2", {
            "qwen3.6-27b": track("x52_27b_gaps_c", "x48_enrich/x48_2a_27b", "x48_enrich/x52_enrich-*", "A and B"),
            LT: track("x52_lightning_fill4", "x48_enrich/nem35l_x52_enrich_a", "x48_enrich/x52_enrich-*",
                   "A only; B not tested: it ablates each block's MLP and NemotronH has none (MoE blocks are separate)",
                   done_as="partial"),
            "qwen3.5-9b": done("results/x48_enrich/x48_2-20261028T113111Z"), "muse-glimmer-30b": done("results/x48_enrich/x48_2-20261028T113111Z")}),
        ("Failed: a person mark at the locker sentence (48.3 bind)", "jobs/c3/batch48.yaml", {
            "qwen3.6-27b": track("x52_27b_gaps_b", "x48_bind/x48_bind_27b", "x48_bind/x52_bind-*"),
            LT: c("not tested", CLEAN + " (48.3 reads the 45m scenes too)", CLEAN_SRC),
            "qwen3.5-9b": done("results/x48_bind/x48_bind-20261028T113120Z"), "muse-glimmer-30b": done("results/x48_bind/x48_bind-20261028T113120Z")}),
        ("Failed: copying heads pass the rest (48 heads)", "jobs/c3/batch48.yaml", {
            "qwen3.6-27b": track("x52_27b_gaps_c", "x48_heads/x48_heads_27b", "x48_heads/x52_heads48-*"),
            LT: track("x52_lightning_fill4", "x48_heads/nem35l_x52_heads48", "x48_heads/x52_heads48-*",
                   "attention blocks after L14 (NemotronH port)"),
            "qwen3.5-9b": done("results/x48_heads/x48_heads-20261028T113126Z"), "muse-glimmer-30b": done("results/x48_heads/x48_heads-20261028T113126Z")}),
        ("Failed: the address as the recall's second route (48 route2)", "jobs/c3/batch48.yaml", {
            "qwen3.6-27b": done("results/x48_route2/x48_route2-20261028T113127Z"),
            LT: c("not tested", CLEAN + " (route2 reads the 45m scenes)", CLEAN_SRC),
            "qwen3.5-9b": done("results/x48_route2/x48_route2-20261028T113127Z"),
            "muse-glimmer-30b": done("results/x48_route2/x48_route2-20261028T113127Z")}),
        ("Failed: blocking the pick sentence (47.6 edges)", "jobs/c3/batch47.yaml 47.6", {
            "qwen3.6-27b": track("x52_27b_gaps_b", "x47_edges/x47_6_b_27b", "x47_edges/x52_edges-*"),
            LT: c("not tested", NO_KO, "src/bridge_jspace/knockout.py"),
            "qwen3.5-9b": done("results/x47_edges/x47_6-20261028T113107Z"), "muse-glimmer-30b": done("results/x47_edges/x47_6-20261028T113107Z")}),
        ("One question, two sources (47.15)", "jobs/c3/batch47.yaml 47.15", {
            "qwen3.6-27b": done("results/x47_source/x47_15-20261028T142722Z"),
            LT: track("x52_lightning_fill3", "x47_source/nem35l_x52_source", "x47_source/x52_source-*", gate_fail=True),
            # the r2 rerun (the original 47.15 verdict lists the 9B as pending) missed its gate
            "qwen3.5-9b": track("x47_15_9b_r2", "x47_source/qwen35_9b_x47_15_r2", None, gate_fail=True),
            "muse-glimmer-30b": done("results/x47_source/x47_15-20261028T142722Z")}),
        ("Failed: the address is the same for any kind of item (47.11 agnostic)", "jobs/c3/batch47.yaml 47.11", {
            "qwen3.6-27b": track("x52_27b_gaps_b", "x47_agnostic/x47_agnostic_27b", "x47_agnostic/x52_agnostic-*"),
            LT: track("x52_lightning_fill3", "x47_agnostic/nem35l_x52_agnostic", "x47_agnostic/x52_agnostic-*"),
            "qwen3.5-9b": done("results/x47_agnostic/x47_11-20261028T143952Z"),
            "muse-glimmer-30b": done("results/x47_agnostic/x47_11-20261028T143952Z")}),
        ("Chained addresses (47.14)", "jobs/c3/batch47.yaml 47.14", {
            "qwen3.6-27b": track("x52_27b_gaps_a", "x47_chain/x47_14_27b", "x47_chain/x52_chain-*"),
            LT: track("x52_lightning_fill1", "x47_chain/nem35l_x52_chain", "x47_chain/x52_chain-*"),
            "qwen3.5-9b": done("results/x47_chain/x47_14-20261028T115841Z"), "muse-glimmer-30b": done("results/x47_chain/x47_14-20261028T115841Z")}),
        ("What is left of the route; the value (47.7)", "jobs/c3/batch47.yaml 47.7", {
            "qwen3.6-27b": done("results/x47_value/x47_7a-20261028T131819Z"),
            LT: parts(**{"(a)": track("x52_lightning_fill3", "x47_value/nem35l_x52_value_a", "x47_value/x52_valuea-*",
                                      gate_fail=True),
                         "(c)": track("x52_lightning_value_c", "x47_value/nem35l_x52_value_c", "x47_value/x52_valuec-*")}),
            # (a) on the 9B and Muse: the r2 reruns (flag 26; the original verdict lists both as pending) missed their gates
            "qwen3.5-9b": track(("x47_7a_9b_r2", "x47_7a_9b_r2_q"), "x47_value/qwen35_9b_x47_7a_r2", None, gate_fail=True),
            "muse-glimmer-30b": track("x47_7a_muse_r2", "x47_value/muse30_x47_7a_r2", None, gate_fail=True)}),
        ("Gain map (49.1)", "jobs/c3/batch49.yaml 49.1", {
            "qwen3.6-27b": done("results/x49_gain/x49_1-20261028T154510Z"),
            LT: track("x52_lightning_fill1", "x49_gain/nem35l_x52_gain", "x49_gain/x52_gain-*"),
            "qwen3.5-9b": done("results/x49_gain/x49_1-20261028T154510Z"), "muse-glimmer-30b": done("results/x49_gain/x49_1-20261028T154510Z")}),
        ("Pooled person probe (49.3)", "jobs/c3/batch49.yaml 49.3", {
            "qwen3.6-27b": track("x52_27b_gaps_c", "x49_probe/x49_3_27b", "x49_probe/x52_probe49-*"),
            LT: c("not tested", CLEAN + " (49.3 reads the 45m scenes)", CLEAN_SRC),
            "qwen3.5-9b": done("results/x49_probe/x49_3-20261028T154604Z"), "muse-glimmer-30b": done("results/x49_probe/x49_3-20261028T154604Z")}),
        ("DAS by position (49.x das_pos)", "jobs/c3/batch49.yaml", {
            "qwen3.6-27b": c("not designed", "9B only by design"), LT: c("not designed", "9B only by design"),
            "qwen3.5-9b": done("results/x49_das_pos/verdict-20261028T154510Z"), "muse-glimmer-30b": c("not designed", "9B only by design")}),
        ("Learned subspaces (48 DAS; 51.3 DAS at scale)", "jobs/c3/batch51.yaml 51.3", {
            "qwen3.6-27b": parts(**{"51.3": done("results/x51_das/verdict-20261028T194630Z"),
                                    "48.1": track("x48_1_27b_r2", "x48_das/x48_das_27b", "x48_das/x52_das-*")}),
            LT: c("not tested", NO_DAS),
            "qwen3.5-9b": done("results/x51_das/verdict-20261028T194630Z", "results/x48_das/verdict-20261028T134153Z"),
            "muse-glimmer-30b": done("results/x51_das/verdict-20261028T194630Z", "results/x48_das/verdict-20261028T134153Z")}),
        ("Joint head ablation under the swap (51.2)", "jobs/c3/batch51.yaml 51.2", {
            "qwen3.6-27b": done("results/x51_heads/x51_2-20261028T190358Z"),
            LT: track("x52_lightning_heads", "x51_heads/nem35l_x52_heads", "x51_heads/x52_heads-*"),
            "qwen3.5-9b": done("results/x51_heads/x51_2-20261028T190358Z"), "muse-glimmer-30b": done("results/x51_heads/x51_2-20261028T190358Z")}),
        ("The address at the last token (51.4)", "jobs/c3/batch51.yaml 51.4", {
            "qwen3.6-27b": done("results/x51_travel/x51_4-20261028T173333Z"),
            LT: track("x52_lightning_travel", "x51_travel/nem35l_x52_travel", "x51_travel/x52_travel-*"),
            "qwen3.5-9b": done("results/x51_travel/x51_4-20261028T173333Z"), "muse-glimmer-30b": done("results/x51_travel/x51_4-20261028T173333Z")}),
        ("Anatomy on Zach's passages (51.5)", "jobs/c3/batch51.yaml 51.5", {
            "qwen3.6-27b": done("results/x51_depth/x51_5-20261028T181100Z"), LT: c("not designed", NOT_DESIGNED_LT),
            "qwen3.5-9b": done("results/x51_depth/x51_5-20261028T181100Z"),
            "muse-glimmer-30b": c("not designed", NOT_DESIGNED_MUSE)}),
        ("Z1 on the full carrier (51.7)", "jobs/c3/batch51.yaml 51.7", {
            "qwen3.6-27b": done("results/x51_carrier/x51_7-20261028T171646Z"),
            LT: track("x52_lightning_carrier", "x51_carrier/nem35l_x52_carrier", "x51_carrier/x52_carrier-*"),
            "qwen3.5-9b": done("results/x51_carrier/x51_7-20261028T171646Z"),
            "muse-glimmer-30b": c("not designed", NOT_DESIGNED_MUSE)}),
        ("What is the address: dimension, methods, geometry (51.11)", "jobs/c3/batch51.yaml 51.11", {
            "qwen3.6-27b": c("partial", "part 2 only by design (parts 1, 3 not designed for the 27B)", "results/x51_addr/verdict-20261028T215138Z"),
            LT: c("not tested", NO_DAS),
            "qwen3.5-9b": done("results/x51_addr/verdict-20261028T215138Z"), "muse-glimmer-30b": done("results/x51_addr/verdict-20261028T215138Z")}),
        ("Answer-direction control on Zach's Z2 (51.12 Z2)", "jobs/c3/batch51.yaml 51.12", {
            "qwen3.6-27b": done("results/x51_answer/x51_12-20261028T201842Z"), LT: c("not designed", NOT_DESIGNED_LT),
            "qwen3.5-9b": done("results/x51_answer/x51_12-20261028T201842Z"),
            "muse-glimmer-30b": c("not designed", NOT_DESIGNED_MUSE)}),
    ]  # fmt: skip


ROWS: list[tuple[str, str, dict]] = []


def check_sources() -> list[str]:
    return [s for _, _, cells in ROWS for cell in cells.values() for s in cell["sources"]
            if not (pins.REPO_ROOT / s).exists()]  # fmt: skip


def counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {m: {} for m in MODELS}
    for _, _, cells in ROWS:
        for m in MODELS:
            st = cells[m]["status"]
            out[m][st] = out[m].get(st, 0) + 1
    return out


def md_lines(stamp: str, head: str) -> list[str]:
    lines = [f"# Batch 52 C: model coverage matrix, full grid ({stamp})", "",
             f"Built at {head} from this checkout (amendments 2-3: every test with a card or claim on the depth page; the "
             "10 key rows first, in Dan's order). Status: done / partial / running / queued / missing / not tested "
             "(reason) / not designed. Coverage cells read what has landed here (verdict folders, run folders, the job "
             "ledgers); 'queued' means queued or running with no ledger entry pulled yet. Coverage verdicts carry no "
             "prediction (rules first scored on the 9B / 27B / Muse). Every result UNVERIFIED until hand-checked. Each "
             "cell's sources are in matrix.json.", "", f"{BOLT}.", "", f"{LT_GATE}.", "",
             "| test | " + " | ".join(SHORT[m] for m in MODELS) + " |", "|---|" + "---|" * len(MODELS)]  # fmt: skip
    for row, _, cells in ROWS:
        txt = []
        for m in MODELS:
            cell = cells[m]
            note = f": {cell['note']}" if cell["note"] and cell["status"] != "done" else (
                f" ({cell['note']})" if cell["note"] else "")  # fmt: skip
            txt.append(f"**{cell['status']}**{note}".replace("|", "/"))
        lines.append(f"| {row} | " + " | ".join(txt) + " |")
    lines += ["", "Counts per model: " + "; ".join(f"{SHORT[m]} {counts()[m]}" for m in MODELS), "",
              "## Rules / designs per row", ""] + [f"- {row}: {rule}" for row, rule, _ in ROWS]  # fmt: skip
    return lines


def entries(obj, target: str) -> list[dict]:
    """Every dict in a verdict's JSON that names `target` and carries a status (a model row)."""
    if isinstance(obj, dict):
        own = [obj] if obj.get("target") == target and isinstance(obj.get("status"), str) else []
        return own + [e for v in obj.values() for e in entries(v, target)]
    if isinstance(obj, list):
        return [e for v in obj for e in entries(v, target)]
    return []


def audit(cell: dict, target: str) -> dict:
    """A done / partial cell checked against what it cites: a verdict whose model row for this column is pending or not
    tested (the model's run never produced outcomes), or a run folder without results, is not done."""
    if cell["status"] not in ("done", "partial"):
        return cell
    for s in cell["sources"]:
        p = pins.REPO_ROOT / s
        if not p.is_dir():
            continue
        if (p / "manifest.json").exists() and not landed(p):
            return c("missing", f"the cited run folder holds no results ({s}); was: {cell['note'] or cell['status']}",
                     *cell["sources"])  # fmt: skip
        rows_ = [e for f in p.glob("*.json") for e in entries(json.loads(f.read_text()), target)]
        if rows_ and not any(e["status"] in ("tested", "done") for e in rows_):
            st = sorted({e["status"] for e in rows_})
            why = "; ".join(sorted({str(e.get("why")) for e in rows_ if e.get("why")}))
            new = "not tested" if st == ["not tested"] else "missing"
            return c(new, f"the cited verdict lists {SHORT[target]} as {' / '.join(st)} ({why + '; ' if why else ''}{s})"
                     + (f"; was: {cell['note']}" if cell["note"] else ""), *cell["sources"])  # fmt: skip
    return cell


def build() -> list[tuple[str, str, dict]]:
    global LEDGER, ROWS
    LEDGER = ledger()
    ROWS = [(row, rule, {m: audit(cell, m) for m, cell in cells.items()}) for row, rule, cells in rows()]
    for row, _, cells in ROWS:
        assert set(cells) == set(MODELS), f"{row}: cells for {sorted(cells)}"
    return ROWS


def main() -> Path:
    build()
    missing = check_sources()
    assert not missing, f"cited paths missing in this checkout: {missing}"
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=pins.REPO_ROOT, capture_output=True,
                          text=True).stdout.strip()  # fmt: skip
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = OUT / f"matrix-{stamp}"
    out.mkdir(parents=True)
    blob = {"batch": 52, "built_at": head, "utc": stamp, "models": list(MODELS), "bolt": BOLT, "lightning_gate": LT_GATE,
            "rows": [{"row": r, "rule": rule, "cells": cells} for r, rule, cells in ROWS], "counts": counts()}  # fmt: skip
    (out / "matrix.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "matrix.md").write_text("\n".join(md_lines(stamp, head)) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
