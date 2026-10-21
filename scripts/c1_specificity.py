"""c1_specificity: is C1's damage specific to the J-space? (Zach, 2026-10-21, decided with Zach after the pipeline
review: the rotated control rules out "any 10 directions", not "any token-aligned directions".) Compares, on the same
items and bands, paper10 (the top-10 J-lens directions at each position, the clean top-10 answer tokens kept) with
unembed10 (the same procedure over the unembedding rows: the logit lens's directions), each with its rotated control:
every word's loss (unedited minus knock-out accuracy, whole question) and the C1 gap (memory-final P->M, M->M minus
prompt-final P->P, M->P), and at each band how many of the items paper10 breaks unembed10 breaks too. Descriptive: no
rule. If unembed10 does about what paper10 does, C1 should say "token-aligned directions", not "the J-space".

python scripts/c1_specificity.py PAPER_RUN UNEMBED_RUN [--set full_v8]
  (PAPER_RUN has paper10 / paper10_rot, UNEMBED_RUN unembed10 / unembed10_rot; they may be one run;
   writes results/ablate_v2/c1_specificity/UNEMBED_RUN.md and .json)
"""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.c1_v2 import MEMORY_FINAL, NAMES, ORDER, PROMPT_FINAL, RES, ci

SUFFIX = ""  # 2026-10-21: "_nosink" (--suffix) compares the conditions that leave attention sinks unedited


def load(run: str) -> list[dict]:
    return [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]


def main(paper_run: str, unembed_run: str, set_name: str, suffix: str = "") -> None:
    conds = {f"paper10{suffix}": f"paper10{suffix}_rot", f"unembed10{suffix}": f"unembed10{suffix}_rot"}
    P, U = f"paper10{suffix}", f"unembed10{suffix}"
    from scripts import tasks_v2 as T

    core = {it["id"] for it in T.load(set_name) if T.stratum(it) == "core"}
    rows = {P: [r for r in load(paper_run) if r["kind"] == "clean" and r["id"] in core],
            U: [r for r in load(unembed_run) if r["kind"] == "clean" and r["id"] in core]}  # fmt: skip
    none = {k: {(r["family"], r["id"]): r["correct"] for r in rs if r["condition"] == "none"} for k, rs in rows.items()}
    shared = set(none[P]) & set(none[U])
    assert shared, "no shared items"
    differ = sum(none[P][k] != none[U][k] for k in shared)
    bands = [b for b in dict.fromkeys(r["band"] for r in rows[U] if r["condition"] == U)
             if any(r["band"] == b and r["condition"] == P for r in rows[P])]  # fmt: skip
    words = [w for w in ORDER if any(k[0] == w for k in shared)]
    unedited = {m: {w: statistics.mean(none[m][k] for k in shared if k[0] == w) for w in words} for m in conds}
    out: dict = {"paper_run": paper_run, "unembed_run": unembed_run, "shared_items": len(shared),
                 "unedited_differ": differ, "bands": {}}  # fmt: skip
    lines = [f"# C1 specificity: J-lens (paper10, {paper_run}) vs unembedding (unembed10, {unembed_run})", "",
             f"{len(shared)} items in both runs ({differ} whose unedited answer differs between them). Accuracy % on the "
             "whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).", "",
             "| band | condition | " + " | ".join(NAMES[w] for w in words) + " | gap |",
             "|---|---|" + "---|" * (len(words) + 1),
             *(f"| - | unedited ({m} run) | " + " | ".join(f"{100 * unedited[m][w]:.0f}" for w in words) + " | |"
               for m in conds)]  # fmt: skip
    overlap = []
    for band in bands:
        out["bands"][band] = {}
        for main_cond, rot in conds.items():
            for cond in (main_cond, rot):
                sel = {w: [r for r in rows[main_cond] if r["band"] == band and r["condition"] == cond
                           and (r["family"], r["id"]) in shared and r["family"] == w] for w in words}  # fmt: skip
                acc = {w: statistics.mean(r["correct"] for r in v) if v else None for w, v in sel.items()}
                loss = {w: unedited[main_cond][w] - a for w, a in acc.items() if a is not None}
                have = all(w in loss for w in PROMPT_FINAL + MEMORY_FINAL)
                gap = (statistics.mean(loss[w] for w in MEMORY_FINAL) - statistics.mean(loss[w] for w in PROMPT_FINAL)
                       if have else None)  # fmt: skip
                out["bands"][band][cond] = {
                    "acc": acc,
                    "loss": loss,
                    "gap": gap,
                    "n": {w: len(v) for w, v in sel.items()},
                }
                cells = []
                for w in words:
                    lo, hi = ci(sel[w])
                    cells.append(
                        "-"
                        if acc[w] is None
                        else f"{100 * acc[w]:.0f} [{100 * lo:.0f}-{100 * hi:.0f}] (n={len(sel[w])})"
                    )
                lines.append(
                    f"| {band} | {cond} | " + " | ".join(cells) + f" | {'-' if gap is None else f'{100 * gap:.0f}'} |"
                )
        broke = {m: {(r["family"], r["id"]) for r in rows[m] if r["band"] == band and r["condition"] == m
                     and (r["family"], r["id"]) in shared and none[m][(r["family"], r["id"])] and not r["correct"]}
                 for m in conds}  # fmt: skip
        mem = {k for k in broke[P] if k[0] in MEMORY_FINAL}
        both = len(mem & broke[U])
        out["bands"][band]["overlap_memory_final"] = {"paper10_broken": len(mem), "also_unembed10": both}
        overlap.append(f"{band}: of the {len(mem)} memory-final items paper10 breaks, unembed10 breaks {both}"
                       f" ({'-' if not mem else f'{100 * both / len(mem):.0f}%'}).")  # fmt: skip
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out["commit"] = commit
    lines += ["", *overlap, "", f"Descriptive (no rule). Output from commit {commit[:7]}."]
    (RES / "c1_specificity").mkdir(exist_ok=True)
    (RES / "c1_specificity" / f"{unembed_run}{suffix}.json").write_text(json.dumps(out, indent=2) + "\n")
    (RES / "c1_specificity" / f"{unembed_run}{suffix}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper_run")
    ap.add_argument("unembed_run")
    ap.add_argument("--set", dest="set_name", default="full_v8", help="the tasks_v2 set the runs drew from")
    ap.add_argument("--suffix", default="", help='condition suffix, e.g. "_nosink"')
    a = ap.parse_args()
    main(a.paper_run, a.unembed_run, a.set_name, a.suffix)
