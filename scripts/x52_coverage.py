"""x52_coverage (batch 52 part C, jobs/c3/batch52.yaml): the model-coverage matrix, rows = the key experiments in Dan's
order, columns = the five models, each cell done / partial / running / missing / not applicable / cancelled with the
result folder or verdict it rests on. Built by hand from the committed verdicts (results/*), docs/x0_numbers.json,
figures/story/data.csv sources and the read-only box checks of 29 Oct; this script holds the table, checks that every
cited path exists in the checkout, and writes results/x52_coverage/matrix-<UTC>/matrix.{md,json}. CPU only.

uv run python scripts/x52_coverage.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

OUT = pins.RESULTS_DIR / "x52_coverage"
MODELS = ("qwen3.6-27b", "nemotron-3.5-lightning", "qwen3.5-9b", "muse-glimmer-30b", "nemotron-3.5-bolt")
SHORT = {"qwen3.6-27b": "27B (tier 1)", "nemotron-3.5-lightning": "Lightning (tier 2)", "qwen3.5-9b": "9B (tier 3)",
         "muse-glimmer-30b": "Muse (tier 3)", "nemotron-3.5-bolt": "Bolt (tier 4)"}  # fmt: skip
STATUS = ("done", "partial", "running", "queued", "missing", "not applicable", "cancelled")

LIGHTNING_WAIT = ("missing: spec after the layer (x52_lightning_layer, running on speedup) is committed; the cell "
                  "reads it through x51_lightning.committed_layer()")  # fmt: skip
BOLT = ("cancelled: no J++ lens file on any box (mats, speedup, another: cache/nemotron-3.5-bolt/lenses/jpp/ absent, "
        "28 Oct ~23:15 UTC; the H200 box it was fit on is unreachable; no hub copy under zachperlman20). Dan's rule: "
        "no lens file -> the column is cancelled")  # fmt: skip
BOLT_TIER = "not applicable: tier 4 runs only the first five rows (and the column is cancelled: no lens file)"


def c(status: str, verdict: str, *sources: str) -> dict:
    assert status in STATUS, status
    return {"status": status, "verdict": verdict, "sources": list(sources)}


ROWS: list[dict] = [
    {"row": "1. Conflict test (main test; whole / without the J++ part / without a random part, at L)",
     "rule": "X0 (jobs/c3/x0_necessity_27b_chat.yaml): confirmed iff lookup extra loss <= 0.10 and recall Jdep >= 0.30; "
             "killed iff lookup >= 0.20 or recall < 0.20",
     "cells": {
         "qwen3.6-27b": c("done", "not confirmed at L32 (lookup 0.14 [0.08, 0.20] > 0.10; recall 0.74 [0.66, 0.80]); n 200",
                          "results/x0_necessity/x0_necessity_27b_chat/verdict-20261024T135446Z/verdict.md"),
         "nemotron-3.5-lightning": c("missing", "45s smoke only (plumbing on 8 scenes; gate on all 516 scenes: lookup "
                                     "0.957, recall 0.816, pass). " + LIGHTNING_WAIT,
                                     "results/x45s/nem35l_x45s_smoke/report.md",
                                     "results/x0_necessity/nem35l_x45s_smoke_main/gate.json"),
         "qwen3.5-9b": c("done", "confirmed at L12 (lookup -0.03 [-0.08, 0.03]; recall 0.50 [0.41, 0.57]); n 200",
                         "results/x0_necessity/qwen35_9b_x0_necessity/verdict-20261024T135419Z"),
         "muse-glimmer-30b": c("done", "confirmed at L26 (lookup -0.10 [-0.15, -0.04]; recall 0.75 [0.61, 0.87]); n 200",
                               "results/x0_necessity/muse30b_x0_necessity/verdict-20261026T001148Z"),
         "nemotron-3.5-bolt": c("cancelled", BOLT)}},
    {"row": "2. Answer control (the conflict test's specificity: the lens part without / with only the answer words' "
            "directions; the answer word's lens rank at the bridge word)",
     "rule": "51.12 E1 (jobs/c3/batch51.yaml, r2 amendment): the lens effect is the entity if the recall keeps >= 0.7 of "
             "its loss with the answer directions kept and loses <= 0.10 beyond random without them only; 'not read' "
             "if the answer word ranks > 50 on >= 90 % of items",
     "cells": {
         "qwen3.6-27b": c("done", "recall: the lens effect is the entity (keeps 0.93, answer-only 0.03); n 200",
                          "results/x51_answer/x51_12-20261028T201842Z/verdict.md"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT),
         "qwen3.5-9b": c("done", "recall: the lens effect is the entity (keeps 0.95, answer-only 0.00); n 200",
                         "results/x51_answer/x51_12-20261028T201842Z/verdict.md"),
         "muse-glimmer-30b": c("done", "recall: the answer word is not read at the bridge word (rank > 50 on 100 %); "
                               "arms beside: the entity; n 200", "results/x51_answer/x51_12-20261028T201842Z/verdict.md"),
         "nemotron-3.5-bolt": c("cancelled", BOLT)}},
    {"row": "3. Routes test (identity / position / value; without the address vs a random part; the address alone)",
     "rule": "x6_routes (E5/E6): the lookup follows identity, position or value; removing the address stops position "
             "answers; keep-only creates them",
     "cells": {
         "qwen3.6-27b": c("done", "identity 0.66 / position 0.34 / value 0.00; no address 0.06 vs random 0.25; address "
                          "alone 0.09 (fails); n 300", "results/x6_routes/x6_routes_27b/verdict-20261025T105901Z",
                          "results/x6_routes/x6_routes_keeponly_27b"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT),
         "qwen3.5-9b": c("done", "identity 0.48 / position 0.51 / value 0.00; no address 0.08 vs random 0.54; alone 0.26",
                         "results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z",
                         "results/x6_routes/qwen35_9b_x6_routes_keeponly"),
         "muse-glimmer-30b": c("done", "identity 0.44 / position 0.54 / value 0.00; no address 0.27 vs random 0.55; alone 0.29",
                               "results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z"),
         "nemotron-3.5-bolt": c("cancelled", BOLT)}},
    {"row": "4. Address swap by dose (mu_k - mu_j at the bridge word, s = 1 / 2 / 4, vs a random vector of its norm)",
     "rule": "x8_write (Q44.1-44.3): target minus random at s = 1; s = 2 = a real change's size",
     "cells": {
         "qwen3.6-27b": c("done", "lookup to the written locker s=1/2/4: 0.01 / 0.24 / 0.50 (random <= 0.01); Q44.1-3 no",
                          "results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT),
         "qwen3.5-9b": c("done", "0.05 / 0.52 / 0.52 (random <= 0.01); Q44.1-3 no",
                         "results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md"),
         "muse-glimmer-30b": c("done", "0.02 / 0.46 / 0.73 (random 0.00); Q44.1-3 no",
                               "results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md"),
         "nemotron-3.5-bolt": c("cancelled", BOLT)}},
    {"row": "5. Order split and copy test (the conflict test split by sentence order; the changed prompt's "
            "locker-sentence states copied in at L)",
     "rule": "split: descriptive (after the data); copy test 45q (jobs/c3/batch45.yaml): the link is made in the locker "
             "sentences if (c) or (d) switches >= half of the lookups S switches while (a) <= 0.25",
     "cells": {
         "qwen3.6-27b": c("done", "lookups switch 76 % locker-first vs 9 % after; copy (c) 0.74 [0.68, 0.80]: holds",
                          "results/x0_composition/split-by-order-20261026T173323Z/split.md",
                          "results/x45b_binding/x45q-20261027T005345Z/x45q.md"),
         "nemotron-3.5-lightning": c("missing", "split: CPU from the conflict test's outcomes once it lands; copy test: "
                                     "not testable under the existing rule unless the clean design's gate passes (45s "
                                     "smoke: recall 0.751 < 0.80 on the clean one-pick scenes)",
                                     "results/x0_necessity/nem35l_x45s_smoke_clean/gate.json"),
         "qwen3.5-9b": c("done", "86 % vs 19 %; copy (c) 0.70 [0.65, 0.74]: holds",
                         "results/x0_composition/split-by-order-20261026T173323Z/split.md",
                         "results/x45b_binding/x45q-20261027T005345Z/x45q.md"),
         "muse-glimmer-30b": c("done", "65 % vs 9 %; copy (c) 0.76 [0.70, 0.81]: holds",
                               "results/x0_composition/split-by-order-20261026T173323Z/split.md",
                               "results/x45b_binding/x45q-20261027T005345Z/x45q.md"),
         "nemotron-3.5-bolt": c("cancelled", BOLT)}},
    {"row": "6. Anatomy by layer (the change's parts per layer against random parts; slot probe)",
     "rule": "47.8 (jobs/c3/batch47.yaml): l_J, l_P, l_probe; (a) handoff, (b) address before use, (c) identity leaves "
             "the lens, (d) never the value",
     "cells": {
         "qwen3.6-27b": c("running", "partial on record: reduced grid (9 of 15 layers: L8-56 every 8th + L30/32/34), "
                          "150 scenes; (a) yes gap 14, (b) yes, (c) no, (d) yes. Full grid (every 4th L4-L60) running: "
                          "x47_8_27b on mats, run x47_anatomy_27b (enqueued by the coordinator 29 Oct)",
                          "results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md", "results/x47_anatomy/x49_4_anatomy_27b"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT),
         "qwen3.5-9b": c("done", "every 2nd L2-L30, 200 scenes: (a) yes gap 0, (b) yes, (c) no, (d) yes",
                         "results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md"),
         "muse-glimmer-30b": c("done", "every 4th L2-L50, 200 scenes: (a) yes gap 20, (b) yes, (c) no, (d) yes",
                               "results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md"),
         "nemotron-3.5-bolt": c("not applicable", BOLT_TIER)}},
    {"row": "7. Ladder (the J++ part removed from the changed prompt rung by rung, rungs 1-6)",
     "rule": "49.2 (jobs/c3/batch49.yaml): (a) second copy = the earlier mention; (b) needed only when everything goes; "
             "(c) the lookup never needs it",
     "cells": {
         "qwen3.6-27b": c("queued", "partial on record: rungs 1-2 only (no rule). Rungs 1-6 with rung 6 over Zach's 27B "
                          "band L32-40: x52_ladder_27b on another (after x47_2_27b)",
                          "results/x49_ladder/x49_2-20261028T161612Z/x49_2.md", "jobs/c3/x52_ladder_27b.yaml"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT + "; needs the clean design (its gate failed on the 45s "
                                     "smoke: recall 0.751)", "results/x0_necessity/nem35l_x45s_smoke_clean/gate.json"),
         "qwen3.5-9b": c("done", "(a) yes, (b) no, (c) yes; n 417", "results/x49_ladder/x49_2-20261028T161612Z/x49_2.md"),
         "muse-glimmer-30b": c("queued", "on record (a) no, (b) no, (c) yes, n 409, rung 6 at L23-29 (outside Zach's "
                               "band). Rung 6 inside his band L36-42: x52_ladder_muse on mats (tier 3)",
                               "results/x49_ladder/x49_2-20261028T161612Z/x49_2.md", "jobs/c3/x52_ladder_muse.yaml"),
         "nemotron-3.5-bolt": c("not applicable", BOLT_TIER)}},
    {"row": "8. Lens readout with the item-change control (the address swap read through the J++ lens vs 200 random "
            "draws; an identity change as the positive control)",
     "rule": "47.0: descriptive (verbalizable or not)",
     "cells": {
         "qwen3.6-27b": c("done", "not verbalizable (rebuilt 0.94x random; identity control 5.16x)",
                          "results/x47_verbal/summary-20261028T033646Z/verbal.md"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT + "; needs the routes test's items (x8_write)"),
         "qwen3.5-9b": c("done", "not verbalizable (1.16x; identity 4.42x)",
                         "results/x47_verbal/summary-20261028T033646Z/verbal.md"),
         "muse-glimmer-30b": c("done", "not verbalizable (1.22x; identity 8.62x)",
                               "results/x47_verbal/summary-20261028T033646Z/verbal.md"),
         "nemotron-3.5-bolt": c("not applicable", BOLT_TIER)}},
    {"row": "9. Last-token read / write (lens readout and probes per layer at the last token and the pick token; the "
            "lens swap vs the whole-state patch)",
     "rule": "51.10 (jobs/c3/batch51.yaml addendum_2): (a) in J-space, (b) readable not used, (c) routes around, (d) "
             "not represented",
     "cells": {
         "qwen3.6-27b": c("done", "last token: recall (b) readable, not used; lookup none of the four",
                          "results/x51_jread/x51_10-20261028T190608Z/verdict.md"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT),
         "qwen3.5-9b": c("done", "last token: recall (b); lookup (c) routes around J-space",
                         "results/x51_jread/x51_10-20261028T190608Z/verdict.md"),
         "muse-glimmer-30b": c("done", "last token: recall (b); lookup none of the four",
                               "results/x51_jread/x51_10-20261028T190608Z/verdict.md"),
         "nemotron-3.5-bolt": c("not applicable", BOLT_TIER)}},
    {"row": "10. Attention under the swap (the question's / last token's attention to the lockers under the address "
            "swap, s = 2, vs a random vector)",
     "rule": "49.7 (jobs/c3/batch49.yaml): follows / elsewhere / distributed; necessity of the best head",
     "cells": {
         "qwen3.6-27b": c("done", "neither; distributed: no", "results/x49_attn/x49_7-20261028T154511Z/verdict.md"),
         "nemotron-3.5-lightning": c("missing", LIGHTNING_WAIT + "; full attention only at 6 of 52 blocks "
                                     "(5, 12, 19, 26, 33, 42)"),
         "qwen3.5-9b": c("done", "neither; distributed: no", "results/x49_attn/x49_7-20261028T154511Z/verdict.md"),
         "muse-glimmer-30b": c("done", "neither; distributed: no", "results/x49_attn/x49_7-20261028T154511Z/verdict.md"),
         "nemotron-3.5-bolt": c("not applicable", BOLT_TIER)}},
]  # fmt: skip

OUTSIDE = [  # cards with a missing 27B cell, outside Dan's key list; the coordinator enqueued them (29 Oct ~00:35 Paris)
    {"row": "Six lockers: one code per locker (E7, 47.2)", "qwen3.6-27b": "running: x47_2_27b on another",
     "qwen3.5-9b": "done", "muse-glimmer-30b": "done", "sources": ["results/x47_six/x47_2-20261028T113102Z"]},
    {"row": "Token by layer map (E11, 47.D1)", "qwen3.6-27b": "running: x47_d1_27b on mats (run x47_depthmap_27b)",
     "qwen3.5-9b": "done", "muse-glimmer-30b": "done", "sources": ["results/x47_depthmap/depth-20261028T120525Z"]},
]  # fmt: skip

PREREQ = {
    "nemotron-3.5-lightning": "lens present on speedup, sha 3306b6e4 = pin, J++ (LN rule, 32 prompts), maps L0-50, "
                              "d_model 2688, held-out pass@10 0.587 vs logit 0.443; Zach's band L27-33; weights "
                              "a9904d24 14/14 shards on speedup; gate (45s smoke, all 516 scenes) lookup 0.957 / recall "
                              "0.816; layer: x52_lightning_layer running on speedup (every 4th layer L2-L50, 60 dev "
                              "scenes, earliest where both switch >= 0.3)",
    "nemotron-3.5-bolt": BOLT + "; fit on mats by arithmetic only: bf16 snapshot 149.8 GB = 139.5 GiB of 159 GiB, "
                         "~10 GiB headroom per GPU, unmeasured",
}  # fmt: skip


def check_sources() -> list[str]:
    missing = []
    for r in ROWS:
        for cell in r["cells"].values():
            missing += [s for s in cell["sources"] if not (pins.REPO_ROOT / s).exists()]
    for r in OUTSIDE:
        missing += [s for s in r["sources"] if not (pins.REPO_ROOT / s).exists()]
    return missing


def counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for m in MODELS:
        out[m] = {}
        for r in ROWS:
            st = r["cells"][m]["status"]
            out[m][st] = out[m].get(st, 0) + 1
    return out


def md_lines(stamp: str, head: str) -> list[str]:
    lines = [f"# Batch 52 C: model coverage matrix ({stamp})", "",
             f"Built at {head} from the committed verdicts (each cell names its source) and read-only box checks; "
             "rows in Dan's order (rows 6-10 for tiers 1-3 only). Status: done / partial / running / queued / missing / "
             "not applicable / cancelled. Every result UNVERIFIED until hand-checked.", "",
             "| row | " + " | ".join(SHORT[m] for m in MODELS) + " |", "|---|" + "---|" * len(MODELS)]  # fmt: skip
    for r in ROWS:
        cells = [f"**{r['cells'][m]['status']}**: {r['cells'][m]['verdict']}" for m in MODELS]
        lines.append(f"| {r['row']} | " + " | ".join(x.replace("|", "/") for x in cells) + " |")
    lines += ["", "Counts per model: " + "; ".join(f"{SHORT[m]} {counts()[m]}" for m in MODELS), "",
              "## Rules and sources per row", ""]  # fmt: skip
    for r in ROWS:
        srcs = sorted({s for m in MODELS for s in r["cells"][m]["sources"]})
        lines += [f"- **{r['row']}** Rule: {r['rule']}. Sources: " + ", ".join(f"`{s}`" for s in srcs)]
    lines += ["", "## Prerequisites for the new families", ""]
    lines += [f"- **{SHORT[m]}**: {t}" for m, t in PREREQ.items()]
    lines += ["", "## Outside the key list (27B cells the coordinator enqueued)", ""]
    lines += [f"- {r['row']}: 27B {r['qwen3.6-27b']}; 9B {r['qwen3.5-9b']}; Muse {r['muse-glimmer-30b']} "
              f"(`{r['sources'][0]}`)" for r in OUTSIDE]  # fmt: skip
    return lines


def main() -> Path:
    import subprocess

    missing = check_sources()
    assert not missing, f"cited paths missing in this checkout: {missing}"
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=pins.REPO_ROOT, capture_output=True,
                          text=True).stdout.strip()  # fmt: skip
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = OUT / f"matrix-{stamp}"
    out.mkdir(parents=True)
    blob = {"batch": 52, "built_at": head, "utc": stamp, "models": list(MODELS), "rows": ROWS, "outside": OUTSIDE,
            "prerequisites": PREREQ, "counts": counts()}  # fmt: skip
    (out / "matrix.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "matrix.md").write_text("\n".join(md_lines(stamp, head)) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
