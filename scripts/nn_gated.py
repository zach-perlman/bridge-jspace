"""nn_gated (Zach, 2026-10-28, prereg amendment 58 note 9 addendum): never-named results on the gated subset (CPU).

Gate (WorkspaceBench-style): an eligible RM item passes if, in the model's stored runs, its guess prompt is wrong (v3
competence), its clue-only questions are wrong (both wordings, where the description has a named clue), and its
final-clause-only question is wrong (cand2 and greedy, note 1's rule with v3's aliases). Re-scores any nn_swap run's RM
rows (jswap.score) on gated items vs all, and reports the gate's funnel.

python scripts/nn_gated.py PREFIX RUN [RUN ...]
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT), str(ROOT / "src")]
from score_greedy import right as right0  # noqa: E402

SET = "jsuite_v3_test_chat"


def gate(p: str) -> tuple[set, dict]:
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data/tasks_v2" / SET / "items.jsonl").open()}
    alias = collections.defaultdict(set)
    for it in items.values():
        alias[it["answer"]] |= set(it.get("answer_aliases") or [])
    right = lambda t, v: any(right0(t, x) for x in {v} | alias[v])  # noqa: E731
    guess = {}
    for line in (ROOT / "results/tasks_v2" / f"{p}{SET}_competence_cand2_v1" / "items.jsonl").open():
        r = json.loads(line)
        if r["part"] == "guess" and ":RM-" in r["id"]:
            guess[r["id"]] = bool(r["correct"])
    pitems = {}
    for sname in ("jsuite_v3probes_test_chat", "jsuite_v3probesB_test_chat"):
        for line in (ROOT / "data/tasks_v2" / sname / "items.jsonl").open():
            it = json.loads(line)
            pitems[it["id"]] = (it["bridge"], it["desc_index"])
    clue = {}
    for name in (f"{p}jsuite_v3probes_cv_v1", f"{p}jsuite_v3probesB_cv_v1"):
        for line in (ROOT / "results/competence_variants" / name / "rows.jsonl").open():
            r = json.loads(line)
            k = pitems[r["id"]]
            clue[k] = clue.get(k, False) or bool(r["correct_cand2"]) or right(r["text"], r["answer"])
    fc = {}
    for line in (ROOT / "results/competence_variants" / f"{p}jsuite_v3fc_cv_v1" / "rows.jsonl").open():
        r = json.loads(line)
        fc[r["id"].replace(":FC", "")] = bool(r["correct_cand2"]) or right(r["text"], r["answer"])
    funnel = collections.Counter()
    passed = set()
    for i, it in items.items():
        if it["word"] != "RM":
            continue
        funnel["rm"] += 1
        g_ok = not guess.get(i, False)
        c_ok = not clue.get((it["bridge"], it.get("desc_index")), False)
        f_ok = not fc.get(i, False)
        funnel["guess_wrong"] += g_ok
        funnel["clue_wrong_or_none"] += c_ok
        funnel["final_clause_wrong"] += f_ok
        if g_ok and c_ok and f_ok:
            passed.add(i)
    funnel["gated"] = len(passed)
    return passed, dict(funnel)


def main(p: str, runs: list[str]) -> None:
    from scripts import jswap as JS

    passed, funnel = gate(p)
    print("gate funnel (all 468 RM items):", funnel)
    out = {"funnel": funnel, "runs": {}}
    for run in runs:
        rows = [json.loads(line) for line in (ROOT / "results/nn_swap" / run / "rows.jsonl").open()]
        rm = [r for r in rows if r["family"] == "RM"]
        for label, rs in (("all", rm), ("gated", [r for r in rm if r["id"] in passed])):
            for band in sorted({r["band"] for r in rs}):
                s = JS.score([r for r in rs if r["band"] == band])
                out["runs"][f"{run}/{label}/{band}"] = s
                cells = {k.split("/")[1]: v for k, v in s.items() if v.get("n")}
                show = ("insert_k10", "insert_k100", "latent_k10", "latent_k100", "clamp", "insert_k10_rand", "full_insert", "lens_insert", "rem_insert",
                        "remfix_insert", "full_latent", "lens_latent", "rem_latent", "remfix_latent")  # fmt: skip
                txt = [f"{c} {v['transfer']:+.1f}" for c, v in cells.items() if c in show]
                txt += [f"{c} kept {v['kept']:.1f}" for c, v in cells.items() if c.startswith("remove")]  # necessity: the share kept
                print(f"{run:34s} {label:6s} {band:7s} n {cells.get('none', {}).get('n')}: " + "  ".join(txt))
    d = ROOT / "results/nn_gated"
    d.mkdir(exist_ok=True)
    (d / f"{p or 'qwen36_27b_'}gated.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
