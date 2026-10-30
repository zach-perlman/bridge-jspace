"""c1_v2: C1 on tasks_v2 (Zach, 2026-10-21, decided with Zach: v2 replaces v1 for the headline). Rule fixed before the
first tasks_v2 knock-out ran. Tests: the full v8 set (full_v8: all 12 words, 7 domains; Zach, 2026-10-21, "full v2
everywhere"): 27B full_ko_v1, Gemma gemma4itf_full_ko_v1. (tasks_ko_v1 on ctrl_v8 was stopped for it, its partial rows
never opened.) The rule uses the core stratum's P->P, M->P, P->M, M->M; every other word (computed starts, three-step,
the planets three-step stratum) is reported alongside.
Second kill test (the sprint plan's; fixed 2026-10-21 before its data, decided with Zach): if paper10_keepown (paper10
with the bridge's own-word directions also protected) restores >= 75% of the memory-final words' loss at the middle
band, with paper10_keepown_rot within 10 points of unedited, the recall damage is the subject's word: C1 is killed.

Claim (C1-graded): memory steps need the J-space, prompt lookups much less. Rule, on the whole question (kind "clean")
under paper10 (the top-10 lens directions projected out at every position, the clean top-10 answer tokens kept) at the
middle band (every model: the band scripts/choose_band.py picks on its ctrl_v8 depth sweep, fixed before its
full_v8 knock-outs; ctrl_v8 shares no prompt with full_v8. The 27B's 32-40 came from the old suite and is re-chosen
the same way, its middle-band runs redone if it moves; Zach, 2026-10-21): the memory-final words (P->M, M->M) lose on
average >= 30 points more accuracy than the prompt-final words (P->P, M->P), and every word's rotated control
(paper10_rot) stays within 10 points of its unedited accuracy at that band. Loss = unedited accuracy - knock-out
accuracy, per word; the two words of each group are averaged.
Reported alongside, outside the rule: every band (27B 12-20, 20-28, 32-40, whole depth; Gemma 11-19, 19-26, 30-38,
whole depth); the original strict C1 rule (every prompt-final word loses <= 10 points in every band and at whole depth,
controls >= 90%); text vs structured formats; each step alone (step1, step2); 95% intervals over bridge entities.

python scripts/c1_v2.py RUN [--middle L32-40] [--set ctrl_v8] [--drop-guessable]
--drop-guessable (Zach, 2026-10-21; a robustness split, not the rule's test): the same scoring without the items the
model answers right from the guess prompt; writes RUN_noguess.md and .json.
Margin-matched gap (Zach, 2026-10-21, after the pipeline review; reported, outside the rule, added after the rule was
fixed and after the 27B's full2_ko_v1 was seen): memory-final items are less confident unedited, and less confident
items break more easily. At the middle band, each condition's loss by quartile of the unedited answer margin (the
logit margin of the answer's first token, from the set's competence run), and the memory-final minus prompt-final gap
with the items pooled per group: raw, reweighted to either group's quartile distribution, and matched (memory-final
items against prompt-final items in the same BIN-logit margin bin, bins weighted by their memory-final items; 95%
bootstrap over items). 1:1 nearest-margin pairs were tried first and dropped before any real data: margins are rounded
and the groups sit apart, so the nearest free partner is systematically more confident (a 10-point gap from nothing in
a toy test).   (writes results/ablate_v2/c1_v2/RUN.md and .json)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
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
TABLE_CONDS = ("paper10", "paper10_rot", "unembed10", "unembed10_rot")
BIN = 0.25


def margin_matched(items: list[tuple[str, float, int]], reps: int = 1000, seed: int = 0) -> dict:
    """items: (word, unedited margin, loss) with loss = unedited correct - knock-out correct, for the rule's four words.
    Losses by margin quartile (cuts over all four words) and the memory-final minus prompt-final gap: raw, reweighted to
    each group's quartile distribution, and matched within BIN-logit margin bins (weighted by memory-final items)."""
    ms = sorted(m for _, m, _ in items)
    cuts = [ms[len(ms) // 4], ms[len(ms) // 2], ms[3 * len(ms) // 4]]

    def q(m: float) -> int:
        return sum(m > c for c in cuts)

    group = {w: g for g, ws in (("memory", MEMORY_FINAL), ("prompt", PROMPT_FINAL)) for w in ws}
    cell: dict = collections.defaultdict(list)
    for w, m, loss in items:
        cell[(w, q(m))].append(loss)
        cell[(group[w], q(m))].append(loss)
    mean = lambda v: statistics.mean(v) if v else None  # noqa: E731
    out: dict = {"cuts": cuts}
    out["by_quartile"] = {k: [[mean(cell[(k, b)]), len(cell[(k, b)])] for b in range(4)]
                          for k in (*PROMPT_FINAL, *MEMORY_FINAL, "prompt", "memory")}  # fmt: skip
    out["median_margin"] = {
        w: statistics.median([m for w2, m, _ in items if w2 == w]) for w in (*PROMPT_FINAL, *MEMORY_FINAL)
    }
    pooled = {g: [loss for w, _, loss in items if group[w] == g] for g in ("memory", "prompt")}
    out["raw_gap"] = mean(pooled["memory"]) - mean(pooled["prompt"]) if all(pooled.values()) else None
    for ref in ("prompt", "memory"):
        w_ = {b: len(cell[(ref, b)]) for b in range(4) if cell[("memory", b)] and cell[("prompt", b)]}
        tot = sum(w_.values())
        out[f"gap_at_{ref}_margins"] = (sum(n * (mean(cell[("memory", b)]) - mean(cell[("prompt", b)]))
                                            for b, n in w_.items()) / tot) if tot else None  # fmt: skip

    def matched(mem: list[tuple[float, int]], prm: list[tuple[float, int]]) -> tuple[float | None, int]:
        bins: dict = collections.defaultdict(lambda: ([], []))
        for k, its in enumerate((mem, prm)):
            for m, loss in its:
                bins[math.floor(m / BIN)][k].append(loss)
        num = den = 0.0
        for a, b in bins.values():
            if a and b:
                num += len(a) * (statistics.mean(a) - statistics.mean(b))
                den += len(a)
        return (num / den if den else None), int(den)

    mem = [(m, loss) for w, m, loss in items if group[w] == "memory"]
    prm = [(m, loss) for w, m, loss in items if group[w] == "prompt"]
    out["matched_gap"], out["matched_n"] = matched(mem, prm)
    out["memory_n"] = len(mem)
    rng = random.Random(seed)
    boot = sorted(g for g, _ in (matched(rng.choices(mem, k=len(mem)), rng.choices(prm, k=len(prm)))
                                 for _ in range(reps)) if g is not None)  # fmt: skip
    if boot:
        out["matched_gap_ci"] = [boot[int(0.025 * len(boot))], boot[int(0.975 * len(boot)) - 1]]
    return out


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


def main(run: str, middle: str, set_name: str, drop_guessable: bool = False, cond_suffix: str = "") -> None:
    # cond_suffix (2026-10-21, docs/breadth/prereg_sink_1021.md): "_nosink" scores the conditions that leave attention sinks
    # unedited; outputs are written to RUN_nosink[_noguess].md / .json
    s_ = cond_suffix
    P10, P10R, PK, PKR = f"paper10{s_}", f"paper10{s_}_rot", f"paper10_keepown{s_}", f"paper10_keepown{s_}_rot"
    U10 = f"unembed10{s_}"
    table_conds = (P10, P10R, U10, f"unembed10{s_}_rot")
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
    conds = [c for c in table_conds if any(r["condition"] == c for r in rows)]
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
    lines = [f"# C1 on tasks_v2 / {run}{' WITHOUT guessable items (robustness split)' if suffix else ''} (rule fixed in scripts/c1_v2.py){' — conditions ' + cond_suffix if cond_suffix else ''}", "",
             "Accuracy % on the whole question [95% CI over bridge entities]; unedited first.", ""]  # fmt: skip
    for cls in (None, "text", "structured"):
        title = "all formats" if cls is None else f"{cls} formats"
        lines += [f"## {title}", "", "| band | condition | " + " | ".join(f"{NAMES[w]}" for w in words) + " |",
                  "|---|---|" + "---|" * len(words),
                  "| - | unedited | " + " | ".join(f"{100 * unedited(w, cls=cls):.0f}" for w in words) + " |"]  # fmt: skip
        for band in bands:
            for cond in conds:
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
            for cond in conds:
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
            for cond in conds:
                lines.append(f"| {band} | {cond} | " + " | ".join(
                    f"{100 * a:.0f}" if (a := acc(pick(band, cond, kind, w))) is not None else "-" for w in words) + " |")  # fmt: skip
        lines.append("")
    # the rule
    mid = out["bands"].get(middle, {})
    loss = {w: unedited(w) - mid[P10][w]["acc"] for w in words if mid.get(P10, {}).get(w, {}).get("acc") is not None}
    ctrl = {w: abs(unedited(w) - mid[P10R][w]["acc"]) for w in words
            if mid.get(P10R, {}).get(w, {}).get("acc") is not None}  # fmt: skip
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

    vals = [a_of(b, c, w) for b in bands for c in (P10, P10R) for w in set(words) | set(PROMPT_FINAL)]
    strict = None if any(v is None for v in vals) else (
        all(unedited(w) - a_of(b, P10, w) <= STRICT_LOSS for b in bands for w in PROMPT_FINAL)
        and all(a_of(b, P10R, w) >= STRICT_CONTROL for b in bands for w in words))  # fmt: skip
    out["rule"] = {"loss": loss, "control_distance": ctrl, "gap": gap, "controls_ok": controls_ok, "C1_graded_holds": holds,
                   "strict_C1_holds": strict}  # fmt: skip
    if any(r["condition"] == PK for r in rows):  # C1's second kill test (fixed 2026-10-21, before its data)
        kk: dict = {}
        for w in [w for w in MEMORY_FINAL if w in words]:
            base, ko, keep = (
                unedited(w),
                acc(pick(middle, P10, word=w)),
                acc(pick(middle, PK, word=w)),
            )
            krot = acc(pick(middle, PKR, word=w))
            kk[w] = {"unedited": base, "paper10": ko, "keepown": keep, "keepown_rot": krot,
                     "restored": None if ko is None or keep is None or base - ko <= 0 else (keep - ko) / (base - ko)}  # fmt: skip
        res_ = [v["restored"] for v in kk.values() if v["restored"] is not None]
        restored = statistics.mean(res_) if res_ else None
        ctrl_ok = all(
            v["keepown_rot"] is not None and abs(v["unedited"] - v["keepown_rot"]) <= CONTROL_WITHIN
            for v in kk.values()
        )
        out["keepown"] = {"per_word": kk, "restored": restored, "control_ok": ctrl_ok,
                          "kills_C1": bool(restored is not None and restored >= 0.75 and ctrl_ok)}  # fmt: skip
        lines += ["", f"Keep-own-word kill test at {middle} (memory-final words): " + ", ".join(
            f"{NAMES[w]} unedited {100 * v['unedited']:.0f} / paper10 {100 * (v['paper10'] or 0):.0f} / keep-own "
            f"{100 * (v['keepown'] or 0):.0f} (its control {100 * (v['keepown_rot'] or 0):.0f})" for w, v in kk.items())
            + f"; restored {'-' if restored is None else f'{100 * restored:.0f}%'} of the damage (>= 75% kills C1); control "
            f"within 10: {'yes' if ctrl_ok else 'no'} -> {'C1 KILLED (the damage is the subject word)' if out['keepown']['kills_C1'] else 'C1 survives'}"]  # fmt: skip
    comp = (json.loads((RES / run / "manifest.json").read_text()).get("tasks") or [None, None])[1]
    if comp and all(w in words for w in PROMPT_FINAL + MEMORY_FINAL):  # the margin-matched gap (reported)
        margin = {r["id"]: r["margin"] for r in map(json.loads, (pins.RESULTS_DIR / "tasks_v2" / comp / "items.jsonl")
                  .read_text().splitlines()) if r["part"] == "whole" and r.get("margin") is not None}  # fmt: skip
        out["margin_matched"] = {}
        for cond in [c for c in (P10, U10) if c in conds]:
            its = [(r["family"], margin[r["id"]], int(none[(r["family"], r["id"], "clean")]) - int(r["correct"]))
                   for w in PROMPT_FINAL + MEMORY_FINAL for r in pick(middle, cond, word=w) if r["id"] in margin]  # fmt: skip
            if not its:
                continue
            mm = out["margin_matched"][cond] = margin_matched(its)
            f = lambda v: "-" if v is None else f"{100 * v:.0f}"  # noqa: E731
            lines += ["", f"## Margin-matched gap under {cond} at {middle} (reported, outside the rule; added after the rule)", "",
                      "Median unedited answer margin (logits): " + ", ".join(f"{NAMES[w]} {v:.2f}" for w, v in mm["median_margin"].items())
                      + f". Loss (points) by quartile of that margin (cuts {', '.join(f'{c:.2f}' for c in mm['cuts'])}), n per cell:", "",
                      "| word | Q1 (least confident) | Q2 | Q3 | Q4 |", "|---|---|---|---|---|"]  # fmt: skip
            for k, v in mm["by_quartile"].items():
                lines.append(
                    f"| {NAMES.get(k, k + '-final, pooled')} | " + " | ".join(f"{f(a)} (n={n})" for a, n in v) + " |"
                )
            ci_ = mm.get("matched_gap_ci")
            lines += ["", f"Memory-final minus prompt-final, items pooled per group: raw {f(mm['raw_gap'])}; reweighted to the "
                      f"prompt-final margins {f(mm['gap_at_prompt_margins'])}, to the memory-final margins "
                      f"{f(mm['gap_at_memory_margins'])}; matched within {BIN}-logit margin bins {f(mm['matched_gap'])}"
                      + (f" [{f(ci_[0])}-{f(ci_[1])}]" if ci_ else "")
                      + f" ({mm['matched_n']} of {mm['memory_n']} memory-final items have a same-bin partner) points."]  # fmt: skip
    if U10 not in conds and all(w in words for w in PROMPT_FINAL + MEMORY_FINAL):
        lines += ["", "Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 "
                  "--conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py."]  # fmt: skip
    lines.append("")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out["commit"] = commit
    lines += [f"Rule at {middle}: losses " + ", ".join(f"{NAMES[w]} {100 * v:.0f}" for w, v in loss.items())
              + f"; memory-final minus prompt-final {'-' if gap is None else f'{100 * gap:.0f}'} points (>= 30 needed); "
              f"controls within 10 points: {'yes' if controls_ok else 'no'} -> C1-graded {'n/a (no whole-question rows at this band)' if not have else 'HOLDS' if holds else 'FAILS'}",
              f"Original strict C1 (reported): {'n/a' if strict is None else 'holds' if strict else 'fails'}. Output from commit {commit[:7]}."]  # fmt: skip
    (RES / "c1_v2").mkdir(exist_ok=True)
    (RES / "c1_v2" / f"{run}{cond_suffix}{suffix}.json").write_text(json.dumps(out, indent=2) + "\n")
    (RES / "c1_v2" / f"{run}{cond_suffix}{suffix}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--middle", default="L32-40", help="the rule's band label (Gemma: L30-38)")
    ap.add_argument("--set", dest="set_name", default="ctrl_v8", help="the tasks_v2 set the run drew from")
    ap.add_argument("--drop-guessable", action="store_true")
    ap.add_argument("--suffix", default="", help='condition suffix, e.g. "_nosink" (attention sinks left unedited)')
    a = ap.parse_args()
    main(a.run, a.middle, a.set_name, a.drop_guessable, a.suffix)
