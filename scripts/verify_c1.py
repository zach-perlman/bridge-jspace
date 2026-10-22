"""verify_c1: a packet for a human to check a C1 headline by hand (Zach, 2026-10-22; for VERIFIED.md, which only a
human writes). (1) An independent recount, from the raw rows (rows.jsonl) only, of accuracy per word under no edit, the
knock-out and its rotated control at the middle band, the losses and the rule's gap (mean of the P->M and M->M losses
minus mean of the P->P and M->P losses; the C words are reported, as in c1_v2.py), side by side with what
scripts/c1_v2.py wrote. (2) 20 items drawn with a fixed seed (stratified by
word), each with its full prompt as the model saw it, the gold answer, the bridge, and right/wrong under no edit, the
knock-out and the control, to check that the items are sensible and the labels right. CPU only.

python scripts/verify_c1.py RUN MIDDLE SET COMPETENCE [--target T]   e.g. full2_ko_v1 L32-40 full_v8 full_v8_competence_v1
(writes results/verify/RUN.md)
"""

import collections
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins

WORDS = ("PP", "MP", "CP", "PM", "MM", "CM")
NAME = {"PP": "P->P", "MP": "M->P", "CP": "C->P", "PM": "P->M", "MM": "M->M", "CM": "C->M"}


def main(run: str, band: str, set_name: str, comp: str) -> None:
    rows = [json.loads(x) for x in (pins.RESULTS_DIR / "ablate_v2" / run / "rows.jsonl").read_text().splitlines()]
    clean = [r for r in rows if r["kind"] == "clean"]
    by = collections.defaultdict(dict)
    for r in clean:
        by[(r["family"], r["id"])][(r["band"], r["condition"])] = r["correct"]
    acc = {}
    for w in WORDS:
        items = [v for (f, _), v in by.items() if f == w]
        if not items:
            continue
        acc[w] = {c: 100 * statistics.mean(v[k] for v in items if k in v) for c, k in
                  (("none", ("-", "none")), ("ko", (band, "paper10")), ("rot", (band, "paper10_rot")))}  # fmt: skip
        acc[w]["n"] = len(items)
    loss = {w: a["none"] - a["ko"] for w, a in acc.items()}
    gap = statistics.mean(loss[w] for w in ("PM", "MM")) - statistics.mean(loss[w] for w in ("PP", "MP"))
    gap6 = statistics.mean(loss[w] for w in ("PM", "MM", "CM")) - statistics.mean(loss[w] for w in ("PP", "MP", "CP"))
    theirs = json.loads((pins.RESULTS_DIR / "ablate_v2" / "c1_v2" / f"{run}.json").read_text())["rule"]
    lines = [f"# Verification packet: C1 / {run} at {band} (target {pins.TARGET}; unverified until a human checks it)", "",
             "## 1. Independent recount from rows.jsonl", "",
             "| word | n | no edit | knock-out | rotated control | loss (recount) | loss (c1_v2.py) |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in WORDS:
        if w in acc:
            a = acc[w]
            lines.append(f"| {NAME[w]} | {a['n']} | {a['none']:.1f} | {a['ko']:.1f} | {a['rot']:.1f} | {loss[w]:.1f} | {100 * theirs['loss'][w]:.1f} |")
    lines += ["", f"Rule gap (mean P->M, M->M loss minus mean P->P, M->P loss): recount {gap:.1f}, c1_v2.py {100 * theirs['gap']:.1f} "
              f"(with the C words too: {gap6:.1f}); "
              f"rule >= 30 with rotated controls within 10 of no edit -> c1_v2.py says {'HOLDS' if theirs['C1_graded_holds'] else 'FAILS'}.", ""]  # fmt: skip
    from scripts import tasks_v2 as T
    from bridge_jspace.tokens import load_tokenizer

    tok = load_tokenizer()
    items = {it["id"]: it for it in T.eligible(set_name, comp, list(WORDS), 10**9, "all")}
    rng = random.Random(0)
    pick = []
    for w in WORDS:
        ids = sorted(i for (f, i) in by if f == w and i in items)
        pick += [(w, i) for i in rng.sample(ids, min(4 if w in ("PM", "MM") else 3, len(ids)))]
    lines += ["## 2. Twenty items (seed 0; 3-4 per word): check the item makes sense and the label is right", ""]
    for n, (w, i) in enumerate(pick[:20], 1):
        it, v = items[i], by[(w, i)]
        text = T.render(tok, {**it, "_question": it["question"], "_kind": it["kind"]})
        mark = lambda k: "right" if v.get(k) else ("wrong" if k in v else "-")  # noqa: E731
        lines += [f"### {n}. {NAME[w]} `{i}` ({it['domain']}, {it['format']}); gold answer **{it['answer']}**; bridge {it['steps'][0]['answer']!r}",
                  f"no edit: {mark(('-', 'none'))} · knock-out at {band}: {mark((band, 'paper10'))} · rotated control: {mark((band, 'paper10_rot'))}",
                  "Steps: " + " -> ".join(f"{s['question']} [{s['answer']}]" for s in it["steps"]), "", "```", text, "```", ""]  # fmt: skip
    out = pins.RESULTS_DIR / "verify"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{run}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:14 + len(WORDS)]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
