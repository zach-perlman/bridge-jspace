"""c1_v2: C1 on tasks_v2 (Zach, 2026-10-21, decided with Zach: v2 replaces v1 for the headline). Rule fixed before the
first tasks_v2 knock-out ran. Tests: the full v8 set (full_v8: all 12 words, 7 domains; Zach, 2026-10-21, "full v2
everywhere"): 27B full_ko_v1, Gemma gemma4itf_full_ko_v1. (tasks_ko_v1 on ctrl_v8 was stopped for it, its partial rows
never opened.) The rule uses the core stratum's P->P, M->P, P->M, M->M; every other word (computed starts, three-step,
the planets three-step stratum) is reported alongside.

Claim (C1-graded): memory steps need the J-space, prompt lookups much less. Rule, on the whole question (kind "clean")
under paper10 (the top-10 lens directions projected out at every position, the clean top-10 answer tokens kept) at the
middle band (27B layers 32-40; Gemma 30-38, the same relative depth): the memory-final words (P->M, M->M) lose on
average >= 30 points more accuracy than the prompt-final words (P->P, M->P), and every word's rotated control
(paper10_rot) stays within 10 points of its unedited accuracy at that band. Loss = unedited accuracy - knock-out
accuracy, per word; the two words of each group are averaged.
Reported alongside, outside the rule: every band (27B 12-20, 20-28, 32-40, whole depth; Gemma 11-19, 19-26, 30-38,
whole depth); the original strict C1 rule (every prompt-final word loses <= 10 points in every band and at whole depth,
controls >= 90%); text vs structured formats; each step alone (step1, step2); 95% intervals over bridge entities.

python scripts/c1_v2.py RUN [--middle L32-40] [--set ctrl_v8] [--drop-guessable]
--drop-guessable (Zach, 2026-10-21; a robustness split, not the rule's test): the same scoring without the items the
model answers right from the guess prompt; writes RUN_noguess.md and .json.   (writes results/ablate_v2/c1_v2/RUN.md and .json)
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

RES = pins.RESULTS_DIR / "ablate_v2"
PROMPT_FINAL, MEMORY_FINAL = ("PP", "MP"), ("PM", "MM")
ORDER = ("PP", "MP", "PM", "MM", "CP", "CM", "PPP", "PPM", "PMP", "MPP", "MPM", "MMP")
NAMES = {w: "->".join(w) for w in ORDER}
GAP, CONTROL_WITHIN, STRICT_LOSS, STRICT_CONTROL = 0.30, 0.10, 0.10, 0.90
TEXT = ("prose", "chat", "document")


def guessable_ids(comp_run: str) -> set[str]:
    """Items the model answers right from the guess prompt (the start replaced by an unknown one): answerable from
    priors without the bridge (tasks_v2 competence --guess)."""
    path = pins.RESULTS_DIR / "tasks_v2" / comp_run / "items.jsonl"
    return {r["id"] for r in map(json.loads, path.read_text().splitlines()) if r["part"] == "guess" and r["correct"]}


def ci(rows: list[dict], reps: int = 1000, seed: int = 0) -> tuple[float, float]:
    """95% bootstrap interval of accuracy, resampling bridge entities."""
    by = collections.defaultdict(list)
    for r in rows:
        by[r["bridge"]].append(r["correct"])
    groups = list(by.values())
    if not groups:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    stats = sorted(
        sum(sum(g) for g in d) / sum(len(g) for g in d)
        for d in ([groups[rng.randrange(len(groups))] for _ in groups] for _ in range(reps))
    )
    return stats[int(0.025 * reps)], stats[int(0.975 * reps) - 1]


def main(run: str, middle: str, set_name: str, drop_guessable: bool = False) -> None:
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    suffix = ""
    if drop_guessable:
        comp = json.loads((RES / run / "manifest.json").read_text())["tasks"][1]
        drop = guessable_ids(comp)
        rows = [r for r in rows if r["id"] not in drop]
        suffix = "_noguess"
    none = {(r["family"], r["id"], r["kind"]): r["correct"] for r in rows if r["condition"] == "none"}
    bands = list(dict.fromkeys(r["band"] for r in rows if r["condition"] != "none"))
    words = [w for w in ORDER if any(r["family"] == w for r in rows)]
    from scripts import tasks_v2 as T

    items = T.load(set_name)
    fmt = {it["id"]: it["format"] for it in items}  # id -> format
    strat = {it["id"]: T.stratum(it) for it in items}  # id -> core / secondary

    def acc(sel: list[dict]) -> float | None:
        return statistics.mean(r["correct"] for r in sel) if sel else None

    def pick(band: str, cond: str, kind: str = "clean", word: str | None = None, cls: str | None = None,
             st: str = "core") -> list[dict]:  # fmt: skip
        return [r for r in rows if r["band"] == band and r["condition"] == cond and r["kind"] == kind
                and (word is None or r["family"] == word) and strat.get(r["id"], "core") == st
                and (cls is None or (fmt.get(r["id"]) in TEXT) == (cls == "text"))]  # fmt: skip

    def unedited(word: str, kind: str = "clean", cls: str | None = None, st: str = "core") -> float:
        v = [c for (f, i, k), c in none.items() if f == word and k == kind and strat.get(i, "core") == st
             and (cls is None or (fmt.get(i) in TEXT) == (cls == "text"))]  # fmt: skip
        return statistics.mean(v) if v else float("nan")

    out: dict = {"run": run, "middle": middle, "bands": {}}
    lines = [f"# C1 on tasks_v2 / {run}{' WITHOUT guessable items (robustness split)' if suffix else ''} (rule fixed in scripts/c1_v2.py)", "",
             "Accuracy % on the whole question [95% CI over bridge entities]; unedited first.", ""]  # fmt: skip
    for cls in (None, "text", "structured"):
        title = "all formats" if cls is None else f"{cls} formats"
        lines += [f"## {title}", "", "| band | condition | " + " | ".join(f"{NAMES[w]}" for w in words) + " |",
                  "|---|---|" + "---|" * len(words),
                  "| - | unedited | " + " | ".join(f"{100 * unedited(w, cls=cls):.0f}" for w in words) + " |"]  # fmt: skip
        for band in bands:
            for cond in ("paper10", "paper10_rot"):
                cells = []
                for w in words:
                    sel = pick(band, cond, word=w, cls=cls)
                    a = acc(sel)
                    lo, hi = ci(sel)
                    cells.append("-" if a is None else f"{100 * a:.0f} [{100 * lo:.0f}-{100 * hi:.0f}] (n={len(sel)})")
                    if cls is None:
                        out["bands"].setdefault(band, {}).setdefault(cond, {})[w] = {
                            "acc": a,
                            "ci": [lo, hi],
                            "n": len(sel),
                        }
                lines.append(f"| {band} | {cond} | " + " | ".join(cells) + " |")
        lines.append("")
    sec = [w for w in words if any(r["family"] == w and strat.get(r["id"]) == "secondary" for r in rows)]
    if sec:  # the planets three-step stratum, reported apart (v8)
        lines += ["## secondary stratum (planets, three-step words), all formats", "",
                  "| band | condition | " + " | ".join(NAMES[w] for w in sec) + " |", "|---|---|" + "---|" * len(sec),
                  "| - | unedited | " + " | ".join(f"{100 * unedited(w, st='secondary'):.0f}" for w in sec) + " |"]  # fmt: skip
        for band in bands:
            for cond in ("paper10", "paper10_rot"):
                lines.append(f"| {band} | {cond} | " + " | ".join(
                    f"{100 * a:.0f} (n={len(sel)})" if (a := acc(sel := pick(band, cond, word=w, st="secondary"))) is not None
                    else "-" for w in sec) + " |")  # fmt: skip
        lines.append("")
    kinds = sorted({r["kind"] for r in rows} - {"clean"})
    for kind in kinds:
        lines += [f"## {kind} alone (all formats)", "", "| band | condition | " + " | ".join(NAMES[w] for w in words) + " |",
                  "|---|---|" + "---|" * len(words),
                  "| - | unedited | " + " | ".join(f"{100 * unedited(w, kind):.0f}" for w in words) + " |"]  # fmt: skip
        for band in bands:
            for cond in ("paper10", "paper10_rot"):
                lines.append(f"| {band} | {cond} | " + " | ".join(
                    f"{100 * a:.0f}" if (a := acc(pick(band, cond, kind, w))) is not None else "-" for w in words) + " |")  # fmt: skip
        lines.append("")
    # the rule
    mid = out["bands"].get(middle, {})
    loss = {
        w: unedited(w) - mid["paper10"][w]["acc"]
        for w in words
        if mid.get("paper10", {}).get(w, {}).get("acc") is not None
    }
    ctrl = {w: abs(unedited(w) - mid["paper10_rot"][w]["acc"]) for w in words
            if mid.get("paper10_rot", {}).get(w, {}).get("acc") is not None}  # fmt: skip
    have = all(w in loss and w in ctrl for w in PROMPT_FINAL + MEMORY_FINAL)
    gap = (
        (statistics.mean(loss[w] for w in MEMORY_FINAL) - statistics.mean(loss[w] for w in PROMPT_FINAL))
        if have
        else None
    )
    controls_ok = have and all(ctrl[w] <= CONTROL_WITHIN for w in words)
    holds = bool(have and gap >= GAP and controls_ok)

    def a_of(b: str, cond: str, w: str) -> float | None:
        return out["bands"].get(b, {}).get(cond, {}).get(w, {}).get("acc")

    vals = [a_of(b, c, w) for b in bands for c in ("paper10", "paper10_rot") for w in set(words) | set(PROMPT_FINAL)]
    strict = None if any(v is None for v in vals) else (
        all(unedited(w) - a_of(b, "paper10", w) <= STRICT_LOSS for b in bands for w in PROMPT_FINAL)
        and all(a_of(b, "paper10_rot", w) >= STRICT_CONTROL for b in bands for w in words))  # fmt: skip
    out["rule"] = {"loss": loss, "control_distance": ctrl, "gap": gap, "controls_ok": controls_ok, "C1_graded_holds": holds,
                   "strict_C1_holds": strict}  # fmt: skip
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out["commit"] = commit
    lines += [f"Rule at {middle}: losses " + ", ".join(f"{NAMES[w]} {100 * v:.0f}" for w, v in loss.items())
              + f"; memory-final minus prompt-final {'-' if gap is None else f'{100 * gap:.0f}'} points (>= 30 needed); "
              f"controls within 10 points: {'yes' if controls_ok else 'no'} -> C1-graded {'n/a (no whole-question rows at this band)' if not have else 'HOLDS' if holds else 'FAILS'}",
              f"Original strict C1 (reported): {'n/a' if strict is None else 'holds' if strict else 'fails'}. Output from commit {commit[:7]}."]  # fmt: skip
    (RES / "c1_v2").mkdir(exist_ok=True)
    (RES / "c1_v2" / f"{run}{suffix}.json").write_text(json.dumps(out, indent=2) + "\n")
    (RES / "c1_v2" / f"{run}{suffix}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--middle", default="L32-40", help="the rule's band label (Gemma: L30-38)")
    ap.add_argument("--set", dest="set_name", default="ctrl_v8", help="the tasks_v2 set the run drew from")
    ap.add_argument("--drop-guessable", action="store_true")
    a = ap.parse_args()
    main(a.run, a.middle, a.set_name, a.drop_guessable)
