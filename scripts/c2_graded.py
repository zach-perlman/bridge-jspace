"""c2_graded: the graded C2 rule (Zach, 2026-10-21, decided with Zach), fixed after write_max v2 on the 27B suite
(wm2_suite_v1) failed the categorical rule, and before opening the tasks_v2 runs (wm2_ctrl_v1, wm2_ctrl_all_v1) or any
Gemma write_max run. wm2_suite_v1 is the data the rule was chosen on, so it is reported but is not evidence for it.

Claim (C2-graded): the bridge's own lens direction writes a memory-used bridge far more easily than a lookup-used one.
Rule: over the cells of lens_add and lens_swap (the bridge's own lens direction, v_X - v_I) at sites that exclude the
tokens C changes (position sets "question" and "final"; any single layer or the joint band; any strength), counting
only cells whose matched-norm random control keeps the clean answer on >= 95% of cases, take each family's best flip
rate to C's answer. C2-graded holds if M->M's best >= 3 x M->P's best and >= M->P's best + 30 points (M->P / M->M: RL /
RR on the suite, MP / MM on tasks_v2), and (interval guard, added with Zach one commit later, still before any
test run was opened) the lower end of M->M's 95% interval over bridge entities is >= the upper end of M->P's.
Reported alongside, outside the rule: P->P vs P->M; the transplant and difference-of-means writes at the same sites;
the own direction at the final position only; the transplant at natural size (strength 1) only.
Tests: wm2_full_v1 (27B, the full v8 set's counterfactual domains, every word, 40 per word; Zach, 2026-10-21, "full v2
everywhere") is the primary one (wm2_ctrl_all_v1 on ctrl_v8 was stopped for it before writing any outcome); wm2_ctrl_v1
(ctrl_v8, level 3) is reported. Other words than M->P / M->M are reported alongside. Positive control: countries recalled (R), countries given (B) and
M->M (RR) each reach >= 50% best gated flips with some lens write (lens_add, lens_swap or lens_transpl, any position
set). It was binding for Gemma; 2026-10-21 (Zach): reported for every model, binding for none.

C2-relative (Zach, 2026-10-21, decided with Zach after the overnight runs showed the copy at the question / final
positions moves only part of the answers, and that the best of ~100 cells is inflated; fixed before the reruns and any
Gemma steering): ceiling = a family's best copy flip rate at the question / final positions (single layer or every band
layer at once); written = the own lens direction's (lens_add, lens_swap) best gated cell chosen on a random half of the
bridge entities and scored on the other half (mean over 200 halvings); relative = written / ceiling (at most 1). Valid
only if M->P's and M->M's ceilings are both >= 0.5 (else "inconclusive: these sites carry the bridge only partly");
C2-relative holds if M->M's relative >= 0.5 and >= 3 x M->P's. --fresh-vs RUN scores only the cases RUN did not use: the
clean test on the 27B, whose rule was designed after seeing wm2_full2_v1 (written to RUN_fresh.md and .json).

--ceiling-from RUN2 (Zach, 2026-10-21): the ceiling from RUN2, a "write_max --writes copy" run on the same cases, for
runs made before 1330338, whose joint copy added each band layer's difference on top of the earlier ones (it overshot
instead of pasting C's state); RUN's own copy ceiling is reported beside it. Writes RUN[_fresh|_noguess]_paste.md/.json.

python scripts/c2_graded.py RUN [RUN ...] [--drop-guessable]   (writes results/write_max/c2_graded/RUN.md and .json)
--drop-guessable (Zach, 2026-10-21; a robustness split, not the rule's test): the same scoring without the cases the
model answers right from the guess prompt (tasks_v2 runs only); writes RUN_noguess.md and .json.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts.write_max import KEEP_GATE, RESULTS, entity_ci

PAIRS = {"suite": ("RL", "RR"), "tasks": ("MP", "MM")}
SECONDARY = {"suite": ("BL", "BR"), "tasks": ("PP", "PM")}
OWN = ("lens_add", "lens_swap")
SITES = ("question", "final")
RATIO, GAP, POSITIVE, CEILING = 3.0, 0.30, 0.50, 0.50
NAMES = {"BL": "P->P", "BR": "P->M", "RL": "M->P", "RR": "M->M", "PP": "P->P", "PM": "P->M", "MP": "M->P", "MM": "M->M",
         "R": "countries, recalled", "B": "countries, given"}  # fmt: skip


def guessable_ids(comp_run: str) -> set[str]:
    """Items the model answers right from the guess prompt (the start replaced by an unknown one): answerable from
    priors without the bridge (tasks_v2 competence --guess)."""
    path = pins.RESULTS_DIR / "tasks_v2" / comp_run / "items.jsonl"
    return {r["id"] for r in map(json.loads, path.read_text().splitlines()) if r["part"] == "guess" and r["correct"]}


def cells_of(rows: list[dict]) -> dict:
    cells: dict = collections.defaultdict(list)
    for r in rows:
        cells[(r["family"], r["write"], r["pos"], str(r["layer"]), r["strength"], r["control"])].append(r)
    return cells


def analyse(run: str, drop: set[str] | None = None, ceiling_run: str | None = None) -> dict:
    rows_all = [json.loads(line) for line in (RESULTS / run / "outcomes.jsonl").read_text().splitlines()]
    rows = [r for r in rows_all if not drop or r["name"] not in drop]
    n_dropped = len({r["name"] for r in rows_all} - {r["name"] for r in rows})
    cells = ceil_cells = cells_of(rows)
    if ceiling_run:  # the ceiling from a copy-only run on the same cases (--ceiling-from)
        crows = [json.loads(line) for line in (RESULTS / ceiling_run / "outcomes.jsonl").read_text().splitlines()]
        crows = [r for r in crows if not drop or r["name"] not in drop]
        for fam in {r["family"] for r in rows}:
            mine, theirs = ({r["name"] for r in rs if r["family"] == fam} for rs in (rows, crows))
            assert mine == theirs, f"{ceiling_run} has other {fam} cases than {run}"
        ceil_cells = cells_of(crows)

    def best(fam: str, writes: tuple, sites: tuple, strengths: tuple | None = None, cells: dict = cells) -> dict | None:
        cand = []
        for (f, w, pos, la, s, control), os_ in cells.items():
            if f != fam or w not in writes or pos not in sites or control or (strengths and s not in strengths):
                continue
            ctrl = cells.get((f, w, pos, la, s, True))
            if w != "copy" and (not ctrl or statistics.mean(o["role"] == "A" for o in ctrl) < KEEP_GATE):
                continue
            cand.append((statistics.mean(o["role"] == "b" for o in os_), w, pos, la, s, os_))
        if not cand:
            return None
        flips, w, pos, la, s, os_ = max(cand, key=lambda x: x[0])
        return {"flips": flips, "ci": entity_ci([(o["bridge"], o["role"] == "b") for o in os_]), "write": w, "pos": pos,
                "layer": la, "strength": s, "gated_cells": len(cand), "n": len(os_)}  # fmt: skip

    def cv_best(fam: str, writes: tuple, sites: tuple, halvings: int = 200, seed: int = 0) -> float | None:
        """The best gated cell chosen on a random half of the bridge entities, scored on the other half (mean)."""
        gated = {}
        for (f, w, pos, la, s, control), os_ in cells.items():
            if f != fam or w not in writes or pos not in sites or control:
                continue
            ctrl = cells.get((f, w, pos, la, s, True))
            if ctrl and statistics.mean(o["role"] == "A" for o in ctrl) >= KEEP_GATE:
                by: dict = collections.defaultdict(list)
                for o in os_:
                    by[o["bridge"]].append(o["role"] == "b")
                gated[(w, pos, la, s)] = by
        if not gated:
            return None
        ents = sorted({e for by in gated.values() for e in by})
        rng, scores = random.Random(seed), []

        def rate(by: dict, half: set) -> float:
            x = [v for e, vs in by.items() if e in half for v in vs]
            return sum(x) / len(x) if x else 0.0

        for _ in range(halvings):
            rng.shuffle(ents)
            a, b = set(ents[: len(ents) // 2]), set(ents[len(ents) // 2 :])
            pick = max(gated, key=lambda k: rate(gated[k], a))
            scores.append(rate(gated[pick], b))
        return statistics.mean(scores)

    fams = {r["family"] for r in rows}
    kind = "tasks" if "MP" in fams else "suite"
    mp, mm = PAIRS[kind]
    out: dict = {"run": run, "families": {}, "cases_dropped": n_dropped, "ceiling_from": ceiling_run}
    for fam in sorted(fams):
        out["families"][fam] = {
            "own_direction": best(fam, OWN, SITES),
            "transplant": best(fam, ("lens_transpl",), SITES),
            "dom": best(fam, ("dom_add", "dom_natural"), SITES),
            "own_final_only": best(fam, OWN, ("final",)),
            "transplant_1x": best(fam, ("lens_transpl",), SITES, (1.0,)),
            "any_lens_any_site": best(fam, ("lens_add", "lens_swap", "lens_transpl"), ("question", "final", "all")),
            "ceiling_copy": best(fam, ("copy",), SITES, cells=ceil_cells),
            "cv_own_direction": cv_best(fam, OWN, SITES),
            "cv_transplant": cv_best(fam, ("lens_transpl",), SITES),
            "cv_dom": cv_best(fam, ("dom_add", "dom_natural"), SITES),
        }
        if ceiling_run:
            out["families"][fam]["ceiling_copy_own_run"] = best(fam, ("copy",), SITES)
    if mp in fams and mm in fams:
        a, b = out["families"][mp]["own_direction"], out["families"][mm]["own_direction"]
        fa, fb = (a["flips"] if a else 0.0), (b["flips"] if b else 0.0)
        ci_ok = bool(a and b and b["ci"][0] >= a["ci"][1]) or bool(b and not a and b["ci"][0] > 0)
        out["rule"] = {"mp": mp, "mm": mm, "mp_best": fa, "mm_best": fb, "ratio_ok": fb >= RATIO * fa,
                       "gap_ok": fb >= fa + GAP, "ci_ok": ci_ok}  # fmt: skip
        out["rule"]["C2_graded_holds"] = out["rule"]["ratio_ok"] and out["rule"]["gap_ok"] and ci_ok
    else:  # a positive-control run (countries and M->M only): no rule
        out["rule"] = None
    if mp in fams and mm in fams:  # C2-relative
        ceil = {f: (out["families"][f]["ceiling_copy"] or {}).get("flips", 0.0) for f in (mp, mm)}
        rel = {
            f: min(1.0, (out["families"][f]["cv_own_direction"] or 0.0) / ceil[f]) if ceil[f] else None
            for f in (mp, mm)
        }
        valid = all(v >= CEILING for v in ceil.values())
        holds = valid and rel[mm] >= 0.5 and rel[mm] >= RATIO * rel[mp]
        out["rule_relative"] = {"ceiling": ceil, "relative": rel, "valid": valid,
                                "verdict": "HOLDS" if holds else "FAILS" if valid else "inconclusive: sites carry the bridge only partly"}  # fmt: skip
    else:
        out["rule_relative"] = None
    pc = {f: (out["families"][f]["any_lens_any_site"] or {}).get("flips", 0.0) for f in ("R", "B", mm) if f in fams}
    out["positive_control"] = {"best": pc, "passes": bool(pc) and all(v >= POSITIVE for v in pc.values())}
    return out


def show(res: dict, commit: str) -> str:
    def cell(b: dict | None) -> str:
        if not b:
            return "- (no gated cell)"
        return (f"{100 * b['flips']:.0f} [{100 * b['ci'][0]:.0f}-{100 * b['ci'][1]:.0f}] ({b['write']}, {b['pos']}, "
                f"{b['layer']}, {b['strength']:g})")  # fmt: skip

    lines = [f"# C2-graded / {res['run']} (rule fixed in scripts/c2_graded.py; this output from commit {commit[:7]})", "",
             "Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).", "",
             "| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | "
             "transplant, question/final | transplant at 1x | difference of means, question/final | "
             "any lens write, any positions |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for fam, d in res["families"].items():
        lines.append(f"| {NAMES.get(fam, fam)} | {cell(d['own_direction'])} | {cell(d['own_final_only'])} | "
                     f"{cell(d['transplant'])} | {cell(d['transplant_1x'])} | {cell(d['dom'])} | "
                     f"{cell(d['any_lens_any_site'])} |")  # fmt: skip
    r = res["rule"] or {}
    lines += [""] if r else ["", "Rule: n/a (no M->P / M->M pair in this run)"]
    lines += (
        []
        if not r
        else [
            f"Rule: {NAMES[r['mm']]} best {100 * r['mm_best']:.0f}% vs {NAMES[r['mp']]} best {100 * r['mp_best']:.0f}%: "
            f">= {RATIO:g}x {'yes' if r['ratio_ok'] else 'no'}, >= +{100 * GAP:.0f} points {'yes' if r['gap_ok'] else 'no'}, "
            f"intervals apart {'yes' if r['ci_ok'] else 'no'} "
            f"-> C2-graded {'HOLDS' if r['C2_graded_holds'] else 'FAILS'}"
        ]
    )
    lines += ["", "Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):", "",
              "| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |",
              "|---|---|---|---|---|---|"]  # fmt: skip
    for fam, d in res["families"].items():
        c = (d.get("ceiling_copy") or {}).get("flips")
        cv = d.get("cv_own_direction")
        f = lambda v: "-" if v is None else f"{100 * v:.0f}"  # noqa: E731
        lines.append(f"| {NAMES.get(fam, fam)} | {f(c)} | {f(cv)} | {f(min(1.0, cv / c) if c and cv is not None else None)} | "
                     f"{f(d.get('cv_transplant'))} | {f(d.get('cv_dom'))} |")  # fmt: skip
    if res.get("ceiling_from"):
        lines += ["", f"Copy ceiling from {res['ceiling_from']} (copy-only run on the same cases, the joint copy pasted); "
                      "this run's own (stacked joint copy): " + ", ".join(
                          f"{NAMES.get(f, f)} {100 * d['ceiling_copy_own_run']['flips']:.0f}"
                          for f, d in res["families"].items() if d.get("ceiling_copy_own_run"))]  # fmt: skip
    rr = res.get("rule_relative")
    if rr:
        lines += ["", f"C2-relative: ceilings {json.dumps({k: round(v, 2) for k, v in rr['ceiling'].items()})}, relative "
                      f"{json.dumps({k: None if v is None else round(v, 2) for k, v in rr['relative'].items()})} -> {rr['verdict']}"]  # fmt: skip
    lines += [f"Positive control (reported; binding for no model): {json.dumps({k: round(v, 2) for k, v in res['positive_control']['best'].items()})}"
              f" -> {'passes' if res['positive_control']['passes'] else 'FAILS'}"]  # fmt: skip
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--drop-guessable", action="store_true")
    ap.add_argument("--fresh-vs", default=None, help="score only the cases this earlier run did not use")
    ap.add_argument("--ceiling-from", default=None, help="take the copy ceiling from this copy-only run (same cases)")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out_dir = RESULTS / "c2_graded"
    out_dir.mkdir(exist_ok=True)
    a = ap.parse_args()
    for run in a.runs:
        drop, suffix = None, ""
        if a.fresh_vs:  # only cases the earlier run did not use
            drop = {json.loads(x)["name"] for x in (RESULTS / a.fresh_vs / "outcomes.jsonl").read_text().splitlines()}
            suffix = "_fresh"
        if a.drop_guessable:
            tasks = json.loads((RESULTS / run / "manifest.json").read_text()).get("tasks") or [None, None]
            if not tasks[1]:
                print(f"{run}: not a tasks_v2 run (no guess prompts); skipped")
                continue
            drop, suffix = guessable_ids(tasks[1]), "_noguess"
        res = analyse(run, drop, a.ceiling_from)
        suffix += "_paste" if a.ceiling_from else ""
        res["commit"] = commit
        (out_dir / f"{run}{suffix}.json").write_text(json.dumps(res, indent=2) + "\n")
        text = show(res, commit)
        if suffix.startswith("_fresh"):
            text = text.replace(
                "# C2-graded / ", f"# C2-graded, FRESH cases only ({res['cases_dropped']} seen ones dropped) / ", 1
            )
        elif drop is not None:
            text = text.replace(
                "# C2-graded / ",
                f"# C2-graded WITHOUT guessable cases ({res['cases_dropped']} dropped; robustness split) / ",
                1,
            )
        (out_dir / f"{run}{suffix}.md").write_text(text)
        print(text)
