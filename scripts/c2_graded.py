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
Tests: wm2_ctrl_all_v1 (27B, tasks_v2 ctrl_v8, all levels) is the primary one; wm2_ctrl_v1 (its level-3 subset) is
reported. A Gemma run counts only if its positive control passes: countries recalled (R), countries given (B) and M->M
(RR) each reach >= 50% best gated flips with some lens write (lens_add, lens_swap or lens_transpl, any position set).

python scripts/c2_graded.py RUN [RUN ...]   (writes results/write_max/c2_graded/RUN.md and .json)
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.write_max import KEEP_GATE, RESULTS, entity_ci

PAIRS = {"suite": ("RL", "RR"), "tasks": ("MP", "MM")}
SECONDARY = {"suite": ("BL", "BR"), "tasks": ("PP", "PM")}
OWN = ("lens_add", "lens_swap")
SITES = ("question", "final")
RATIO, GAP, POSITIVE = 3.0, 0.30, 0.50
NAMES = {"BL": "P->P", "BR": "P->M", "RL": "M->P", "RR": "M->M", "PP": "P->P", "PM": "P->M", "MP": "M->P", "MM": "M->M",
         "R": "countries, recalled", "B": "countries, given"}  # fmt: skip


def analyse(run: str) -> dict:
    rows = [json.loads(line) for line in (RESULTS / run / "outcomes.jsonl").read_text().splitlines()]
    cells: dict = collections.defaultdict(list)
    for r in rows:
        cells[(r["family"], r["write"], r["pos"], str(r["layer"]), r["strength"], r["control"])].append(r)

    def best(fam: str, writes: tuple, sites: tuple, strengths: tuple | None = None) -> dict | None:
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

    fams = {r["family"] for r in rows}
    kind = "tasks" if "MP" in fams else "suite"
    mp, mm = PAIRS[kind]
    out: dict = {"run": run, "families": {}}
    for fam in sorted(fams):
        out["families"][fam] = {
            "own_direction": best(fam, OWN, SITES),
            "transplant": best(fam, ("lens_transpl",), SITES),
            "dom": best(fam, ("dom_add", "dom_natural"), SITES),
            "own_final_only": best(fam, OWN, ("final",)),
            "transplant_1x": best(fam, ("lens_transpl",), SITES, (1.0,)),
            "any_lens_any_site": best(fam, ("lens_add", "lens_swap", "lens_transpl"), ("question", "final", "all")),
        }
    a, b = out["families"][mp]["own_direction"], out["families"][mm]["own_direction"]
    fa, fb = (a["flips"] if a else 0.0), (b["flips"] if b else 0.0)
    ci_ok = bool(a and b and b["ci"][0] >= a["ci"][1]) or bool(b and not a and b["ci"][0] > 0)
    out["rule"] = {"mp": mp, "mm": mm, "mp_best": fa, "mm_best": fb, "ratio_ok": fb >= RATIO * fa,
                   "gap_ok": fb >= fa + GAP, "ci_ok": ci_ok}  # fmt: skip
    out["rule"]["C2_graded_holds"] = out["rule"]["ratio_ok"] and out["rule"]["gap_ok"] and ci_ok
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
    r = res["rule"]
    lines += ["", f"Rule: {NAMES[r['mm']]} best {100 * r['mm_best']:.0f}% vs {NAMES[r['mp']]} best {100 * r['mp_best']:.0f}%: "
              f">= {RATIO:g}x {'yes' if r['ratio_ok'] else 'no'}, >= +{100 * GAP:.0f} points {'yes' if r['gap_ok'] else 'no'}, "
              f"intervals apart {'yes' if r['ci_ok'] else 'no'} "
              f"-> C2-graded {'HOLDS' if r['C2_graded_holds'] else 'FAILS'}",
              f"Positive control (binding for Gemma only): {json.dumps({k: round(v, 2) for k, v in res['positive_control']['best'].items()})}"
              f" -> {'passes' if res['positive_control']['passes'] else 'FAILS'}"]  # fmt: skip
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out_dir = RESULTS / "c2_graded"
    out_dir.mkdir(exist_ok=True)
    for run in ap.parse_args().runs:
        res = analyse(run)
        res["commit"] = commit
        (out_dir / f"{run}.json").write_text(json.dumps(res, indent=2) + "\n")
        text = show(res, commit)
        (out_dir / f"{run}.md").write_text(text)
        print(text)
