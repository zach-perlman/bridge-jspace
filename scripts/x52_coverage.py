"""x52_coverage (batch 52 part C, jobs/c3/batch52.yaml with amendments 1-2): the model-coverage matrix, the full grid
(amendment 2): rows = every test with a card or claim on the depth page (the 10 key rows first, in Dan's order), columns
= 27B / Lightning / 9B / Muse, each cell done / partial / running / queued / missing / not tested with the reason and
the result folder or verdict it rests on; Bolt one line, out of scope. Built by hand from the committed verdicts
(results/*), the run manifests' targets, docs/x0_numbers.json and figures/story/data.csv sources, the job ledgers and
the coordinator's queue messages; this script holds the table, checks that every cited path exists in the checkout, and
writes results/x52_coverage/matrix-<UTC>/matrix.{md,json}. CPU only.

uv run python scripts/x52_coverage.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

OUT = pins.RESULTS_DIR / "x52_coverage"
MODELS = ("qwen3.6-27b", "nemotron-3.5-lightning", "qwen3.5-9b", "muse-glimmer-30b")
SHORT = {"qwen3.6-27b": "27B", "nemotron-3.5-lightning": "Lightning", "qwen3.5-9b": "9B", "muse-glimmer-30b": "Muse"}
STATUS = ("done", "partial", "running", "queued", "missing", "not tested", "not designed")
BOLT = ("Nemotron 3.5 Bolt: out of scope: only a J-lens exists, no J++ lens (amendment 2; every depth test uses J++ "
        "atoms). Checked 28 Oct ~23:15 UTC: no J++ file under cache/nemotron-3.5-bolt/lenses/jpp/ on mats, speedup or "
        "another; the H200 box it was fit on is unreachable")  # fmt: skip
LT_GATE = ("Lightning's gate: the main test's gate on all 516 scenes (lookup 0.957, recall 0.816), chosen after the "
           "60-scene pre-check was seen (lookup 0.883, recall 0.783: failed) — hollow mark (Dan 01:10); layer L14 by "
           "amendment 1 (results/x51_lightning/nem35l_x52_layer_r2)")  # fmt: skip
CLEAN = (
    "not tested: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change)"
)
CLEAN_SRC = "results/x0_necessity/nem35l_x45s_smoke_clean/gate.json"
LT = "missing: Lightning chain, spec in Dan's order (reads the committed L14)"
LT2 = "missing: Lightning, after the 10 key rows"


def c(status: str, note: str = "", *sources: str) -> dict:
    assert status in STATUS, status
    return {"status": status, "note": note, "sources": list(sources)}


def done(*sources: str, note: str = "") -> dict:
    return c("done", note, *sources)


# (row, rule / design source, {model: cell}); key rows 1-10 first (Dan's order), then the rest of the depth page.
ROWS: list[tuple[str, str, dict]] = [
    ("1. Conflict test (main test, at L)", "X0 (jobs/c3/x0_necessity_27b_chat.yaml)", {
        "qwen3.6-27b": done("results/x0_necessity/x0_necessity_27b_chat/verdict-20261024T135446Z",
                            note="not confirmed (lookup 0.14 > 0.10; recall 0.74)"),
        "nemotron-3.5-lightning": c("queued", "x52_lightning_conflict, speedup first: 3 arms at all 13 swept layers, "
                                    "decided at L14; " + LT_GATE, "jobs/c3/x52_lightning_conflict.yaml",
                                    "results/x51_lightning/nem35l_x52_layer_r2/layer.json"),
        "qwen3.5-9b": done("results/x0_necessity/qwen35_9b_x0_necessity/verdict-20261024T135419Z", note="confirmed"),
        "muse-glimmer-30b": done("results/x0_necessity/muse30b_x0_necessity/verdict-20261026T001148Z", note="confirmed")}),
    ("2. Answer control (51.12 E1)", "jobs/c3/batch51.yaml 51.12 r2", {
        "qwen3.6-27b": done("results/x51_answer/x51_12-20261028T201842Z", note="recall: the entity"),
        "nemotron-3.5-lightning": c("missing", LT),
        "qwen3.5-9b": done("results/x51_answer/x51_12-20261028T201842Z", note="recall: the entity"),
        "muse-glimmer-30b": done("results/x51_answer/x51_12-20261028T201842Z", note="answer word not read")}),
    ("3. Routes test (identity / position / value; no address; address alone)", "x6_routes (E5/E6)", {
        "qwen3.6-27b": done("results/x6_routes/x6_routes_27b/verdict-20261025T105901Z",
                            "results/x6_routes/x6_routes_keeponly_27b", note="0.66 / 0.34 / 0.00; alone fails"),
        "nemotron-3.5-lightning": c("missing", LT),
        "qwen3.5-9b": done("results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z",
                           "results/x6_routes/qwen35_9b_x6_routes_keeponly"),
        "muse-glimmer-30b": done("results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z")}),
    ("4. Address swap by dose (x8_write, s = 1 / 2 / 4)", "x8_write (Q44.1-3)", {
        "qwen3.6-27b": done("results/x8_write/x8_write_27b/verdict-20261026T125548Z", note="0.01 / 0.24 / 0.50"),
        "nemotron-3.5-lightning": c("missing", LT + "; needs the routes test's items"),
        "qwen3.5-9b": done("results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z", note="0.05 / 0.52 / 0.52"),
        "muse-glimmer-30b": done("results/x8_write/muse30b_x8_write/verdict-20261026T141141Z", note="0.02 / 0.46 / 0.73")}),
    ("5a. Order split (descriptive)", "x0_composition split-by-order", {
        "qwen3.6-27b": done("results/x0_composition/split-by-order-20261026T173323Z"),
        "nemotron-3.5-lightning": c("missing", "CPU from the conflict test's outcomes once it lands"),
        "qwen3.5-9b": done("results/x0_composition/split-by-order-20261026T173323Z"),
        "muse-glimmer-30b": done("results/x0_composition/split-by-order-20261026T173323Z")}),
    ("5b. Copy test (45q)", "jobs/c3/batch45.yaml 45b/45q", {
        "qwen3.6-27b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds"),
        "nemotron-3.5-lightning": c("not tested", CLEAN, CLEAN_SRC),
        "qwen3.5-9b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds"),
        "muse-glimmer-30b": done("results/x45b_binding/x45q-20261027T005345Z", note="holds")}),
    ("6. Anatomy by layer (47.8)", "jobs/c3/batch47.yaml 47.8", {
        "qwen3.6-27b": c("queued", "on record a reduced grid (9 of 15 layers); full grid x47_8_27b on mats (run "
                         "x47_anatomy_27b)", "results/x47_anatomy/x47_8-20261028T154518Z"),
        "nemotron-3.5-lightning": c("missing", LT),
        "qwen3.5-9b": done("results/x47_anatomy/x47_8-20261028T154518Z"),
        "muse-glimmer-30b": done("results/x47_anatomy/x47_8-20261028T154518Z")}),
    ("7. Ladder (49.2, rungs 1-6)", "jobs/c3/batch49.yaml 49.2", {
        "qwen3.6-27b": c("queued", "on record rungs 1-2 only; rungs 1-6 (rung 6 at Zach's L32-40) x52_ladder_27b on "
                         "another (the speedup copy was stopped after 2 min)", "results/x49_ladder/x49_2-20261028T161612Z",
                         "jobs/c3/x52_ladder_27b.yaml"),
        "nemotron-3.5-lightning": c("not tested", CLEAN, CLEAN_SRC),
        "qwen3.5-9b": done("results/x49_ladder/x49_2-20261028T161612Z"),
        "muse-glimmer-30b": c("queued", "on record, rung 6 at L23-29; rung 6 in Zach's L36-42: x52_ladder_muse on mats "
                              "(behind part B)", "results/x49_ladder/x49_2-20261028T161612Z", "jobs/c3/x52_ladder_muse.yaml")}),
    ("8. Lens readout with the item-change control (47.0)", "47.0 (descriptive)", {
        "qwen3.6-27b": done("results/x47_verbal/summary-20261028T033646Z"),
        "nemotron-3.5-lightning": c("missing", LT + "; needs x8_write's items"),
        "qwen3.5-9b": done("results/x47_verbal/summary-20261028T033646Z"),
        "muse-glimmer-30b": done("results/x47_verbal/summary-20261028T033646Z")}),
    ("9. Last-token read / write (51.10)", "jobs/c3/batch51.yaml addendum_2", {
        "qwen3.6-27b": done("results/x51_jread/x51_10-20261028T190608Z"),
        "nemotron-3.5-lightning": c("missing", LT),
        "qwen3.5-9b": done("results/x51_jread/x51_10-20261028T190608Z"),
        "muse-glimmer-30b": done("results/x51_jread/x51_10-20261028T190608Z")}),
    ("10. Attention under the swap (49.7)", "jobs/c3/batch49.yaml 49.7", {
        "qwen3.6-27b": done("results/x49_attn/x49_7-20261028T154511Z"),
        "nemotron-3.5-lightning": c("missing", LT + "; full attention at 6 of 52 blocks only"),
        "qwen3.5-9b": done("results/x49_attn/x49_7-20261028T154511Z"),
        "muse-glimmer-30b": done("results/x49_attn/x49_7-20261028T154511Z")}),
    # ---- the rest of the depth page (cards, claims, Part VI, appendix figures) ------------------------------------
    ("Split in other texts: varied scenes (x0b)", "x0b_generalize", {
        "qwen3.6-27b": done("results/x0b_generalize/x0b_v2_27b"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x0b_generalize/qwen35_9b_x0b_v2"),
        "muse-glimmer-30b": done("results/x0b_generalize/muse30b_x0b_v2")}),
    ("Split in other texts: natural passages (x5)", "x5_natural", {
        "qwen3.6-27b": done("results/x5_natural/x5_natural_27b"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x5_natural/qwen35_9b_x5_natural_g75", note="gate lowered after the data"),
        "muse-glimmer-30b": done("results/x5_natural/muse30b_x5_natural")}),
    ("Dose curves, a part alone (51.1)", "jobs/c3/batch51.yaml 51.1", {
        "qwen3.6-27b": done("results/x51_dose/x51_1-20261028T170335Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_dose/x51_1-20261028T170335Z"),
        "muse-glimmer-30b": done("results/x51_dose/x51_1-20261028T170335Z")}),
    ("Zeroing at one layer (47.5)", "jobs/c3/batch47.yaml 47.5", {
        "qwen3.6-27b": done("results/x47_zero/x47_5-20261028T113106Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_zero/x47_5-20261028T113106Z"),
        "muse-glimmer-30b": done("results/x47_zero/x47_5-20261028T113106Z")}),
    ("Earlier mention (45p)", "jobs/c3/batch45.yaml 45p", {
        "qwen3.6-27b": done("results/x45p/x45p-20261027T012017Z"),
        "nemotron-3.5-lightning": c("not tested", CLEAN, CLEAN_SRC),
        "qwen3.5-9b": done("results/x45p/x45p-20261027T012017Z"), "muse-glimmer-30b": done("results/x45p/x45p-20261027T012017Z")}),
    ("E3: identity route outside the lens (47.1 atom slices)", "jobs/c3/batch47.yaml 47.1", {
        "qwen3.6-27b": done("results/x47_atoms/x47_1-20261028T113101Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_atoms/x47_1-20261028T113101Z"),
        "muse-glimmer-30b": done("results/x47_atoms/x47_1-20261028T113101Z")}),
    ("E6: the address probe (x0_probe v4)", "x0_probe", {
        "qwen3.6-27b": done("results/x0_probe/x0_probe_v4_27b"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x0_probe/qwen35_9b_x0_probe_v4"),
        "muse-glimmer-30b": done("results/x0_probe/muse30b_x0_probe_v4")}),
    ("E6: the swap after neutral sentences (47.16 distance)", "jobs/c3/batch47.yaml 47.16", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write (mats)"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_distance/x47_16-20261028T131501Z"),
        "muse-glimmer-30b": done("results/x47_distance/x47_16-20261028T131501Z")}),
    ("E7: six lockers, one code per slot (47.2)", "jobs/c3/batch47.yaml 47.2", {
        "qwen3.6-27b": c("queued", "x47_2_27b on another (behind part B and the 27B ladder)"),
        "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_six/x47_2-20261028T113102Z"),
        "muse-glimmer-30b": done("results/x47_six/x47_2-20261028T113102Z")}),
    ("E8: the report prompt (47.10)", "jobs/c3/batch47.yaml 47.10", {
        "qwen3.6-27b": done("results/x47_report/x47_10-20261028T113109Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_report/x47_10-20261028T113109Z"),
        "muse-glimmer-30b": done("results/x47_report/x47_10-20261028T113109Z")}),
    ("E11: token by layer map (47.D1)", "jobs/c3/batch47.yaml D1", {
        "qwen3.6-27b": c("queued", "x47_d1_27b on mats (run x47_depthmap_27b)"),
        "nemotron-3.5-lightning": c("not tested", CLEAN, CLEAN_SRC),
        "qwen3.5-9b": done("results/x47_depthmap/depth-20261028T120525Z"),
        "muse-glimmer-30b": done("results/x47_depthmap/depth-20261028T120525Z")}),
    ("E11: lookups carried before L (47.4 cumulative)", "jobs/c3/batch47.yaml 47.4", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write (mats)"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_cumulative/x47_4-20261028T113105Z"),
        "muse-glimmer-30b": done("results/x47_cumulative/x47_4-20261028T113105Z")}),
    ("E12: address persistence across depth (D4, CPU)", "jobs/c3/batch47.yaml D4", {
        "qwen3.6-27b": c("missing", "CPU from x47_anatomy_27b's cache once it lands"),
        "nemotron-3.5-lightning": c("missing", "CPU after Lightning's anatomy"),
        "qwen3.5-9b": done("results/x47_depth_cpu/persistence-20261028T115530Z"),
        "muse-glimmer-30b": done("results/x47_depth_cpu/persistence-20261028T115530Z")}),
    ("Part V: Zach's passages Z1 / Z2 (x50)", "jobs/c3/batch50 (x50_zach)", {
        "qwen3.6-27b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z"),
        "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z"),
        "muse-glimmer-30b": done("results/x50_zach/z1-20261028T161649Z", "results/x50_zach/z2-20261028T162710Z")}),
    ("Part V: Zach's passages Z3 (routes on his passages)", "x50_zach z3", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x50_zach/z3-20261028T163053Z"), "muse-glimmer-30b": done("results/x50_zach/z3-20261028T163053Z")}),
    ("Described bridge (47.3, and 51.12's cue r2)", "jobs/c3/batch47.yaml 47.3", {
        "qwen3.6-27b": done("results/x47_cue/x47_3-20261028T113104Z", "results/x51_answer/x51_12-20261028T201842Z"),
        "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_cue/x47_3-20261028T113104Z", "results/x51_answer/x51_12-20261028T201842Z"),
        "muse-glimmer-30b": c("partial", "47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design)",
                              "results/x47_cue/x47_3-20261028T113104Z")}),
    ("One question, two instructions (49.6)", "jobs/c3/batch49.yaml 49.6", {
        "qwen3.6-27b": done("results/x49_report/x49_6-20261028T154511Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": c("not tested", "ran; the gate failed (README: the others miss the gate)",
                        "results/x49_report/x49_6-20261028T154511Z"),
        "muse-glimmer-30b": c("missing", "9B / Muse gap: not run on Muse")}),
    ("Address refit per text format (x45d)", "x45d", {
        "qwen3.6-27b": done("results/x0b_generalize/x45d_27b"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x0b_generalize/qwen35_9b_x45d"), "muse-glimmer-30b": done("results/x0b_generalize/muse30b_x45d")}),
    ("The lookup's errors are not address errors (47.13)", "jobs/c3/batch47.yaml 47.13", {
        "qwen3.6-27b": done("results/x47_errors/x47_13-20261028T113107Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_errors/x47_13-20261028T113107Z"),
        "muse-glimmer-30b": done("results/x47_errors/x47_13-20261028T113107Z")}),
    ("Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment)", "jobs/c3/batch48.yaml 48.2", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x48_enrich/x48_2-20261028T113111Z"), "muse-glimmer-30b": done("results/x48_enrich/x48_2-20261028T113111Z")}),
    ("Failed: a person mark at the locker sentence (48.3 bind)", "jobs/c3/batch48.yaml", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x48_bind/x48_bind-20261028T113120Z"), "muse-glimmer-30b": done("results/x48_bind/x48_bind-20261028T113120Z")}),
    ("Failed: copying heads pass the rest (48 heads)", "jobs/c3/batch48.yaml", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x48_heads/x48_heads-20261028T113126Z"), "muse-glimmer-30b": done("results/x48_heads/x48_heads-20261028T113126Z")}),
    ("Failed: the address as the recall's second route (48 route2)", "jobs/c3/batch48.yaml", {
        "qwen3.6-27b": done("results/x48_route2/x48_route2-20261028T113127Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x48_route2/x48_route2-20261028T113127Z"),
        "muse-glimmer-30b": done("results/x48_route2/x48_route2-20261028T113127Z")}),
    ("Failed: blocking the pick sentence (47.6 edges)", "jobs/c3/batch47.yaml 47.6", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_edges/x47_6-20261028T113107Z"), "muse-glimmer-30b": done("results/x47_edges/x47_6-20261028T113107Z")}),
    ("Failed: the second hop's key token (47.15 source)", "jobs/c3/batch47.yaml 47.15", {
        "qwen3.6-27b": done("results/x47_source/x47_15-20261028T142722Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_source/x47_15-20261028T142722Z"),
        "muse-glimmer-30b": done("results/x47_source/x47_15-20261028T142722Z")}),
    ("Failed: the address is the same for any kind of item (47.11 agnostic)", "jobs/c3/batch47.yaml 47.11", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_agnostic/x47_11-20261028T143952Z"),
        "muse-glimmer-30b": done("results/x47_agnostic/x47_11-20261028T143952Z")}),
    ("Chained addresses (47.14)", "jobs/c3/batch47.yaml 47.14", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_chain/x47_14-20261028T115841Z"), "muse-glimmer-30b": done("results/x47_chain/x47_14-20261028T115841Z")}),
    ("What is left of the route; the value (47.7)", "jobs/c3/batch47.yaml 47.7", {
        "qwen3.6-27b": done("results/x47_value/x47_7a-20261028T131819Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x47_value/x47_7a-20261028T131819Z"), "muse-glimmer-30b": done("results/x47_value/x47_7a-20261028T131819Z")}),
    ("Gain map (49.1)", "jobs/c3/batch49.yaml 49.1", {
        "qwen3.6-27b": done("results/x49_gain/x49_1-20261028T154510Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x49_gain/x49_1-20261028T154510Z"), "muse-glimmer-30b": done("results/x49_gain/x49_1-20261028T154510Z")}),
    ("Pooled person probe (49.3)", "jobs/c3/batch49.yaml 49.3", {
        "qwen3.6-27b": c("missing", "27B gap: spec to write"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x49_probe/x49_3-20261028T154604Z"), "muse-glimmer-30b": done("results/x49_probe/x49_3-20261028T154604Z")}),
    ("DAS by position (49.x das_pos)", "jobs/c3/batch49.yaml", {
        "qwen3.6-27b": c("not designed", "9B only by design"), "nemotron-3.5-lightning": c("not designed", "9B only by design"),
        "qwen3.5-9b": done("results/x49_das_pos/verdict-20261028T154510Z"), "muse-glimmer-30b": c("not designed", "9B only by design")}),
    ("Learned subspaces (48 DAS; 51.3 DAS at scale)", "jobs/c3/batch51.yaml 51.3", {
        "qwen3.6-27b": c("partial", "51.3 done; 48's DAS not run on the 27B (51.3 supersedes it)", "results/x51_das/verdict-20261028T194630Z"),
        "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_das/verdict-20261028T194630Z", "results/x48_das/verdict-20261028T134153Z"),
        "muse-glimmer-30b": done("results/x51_das/verdict-20261028T194630Z", "results/x48_das/verdict-20261028T134153Z")}),
    ("Joint head ablation under the swap (51.2)", "jobs/c3/batch51.yaml 51.2", {
        "qwen3.6-27b": done("results/x51_heads/x51_2-20261028T190358Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_heads/x51_2-20261028T190358Z"), "muse-glimmer-30b": done("results/x51_heads/x51_2-20261028T190358Z")}),
    ("The address at the last token (51.4)", "jobs/c3/batch51.yaml 51.4", {
        "qwen3.6-27b": done("results/x51_travel/x51_4-20261028T173333Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_travel/x51_4-20261028T173333Z"), "muse-glimmer-30b": done("results/x51_travel/x51_4-20261028T173333Z")}),
    ("Anatomy on Zach's passages (51.5)", "jobs/c3/batch51.yaml 51.5", {
        "qwen3.6-27b": done("results/x51_depth/x51_5-20261028T181100Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_depth/x51_5-20261028T181100Z"),
        "muse-glimmer-30b": c("missing", "9B / Muse gap (51.5 designed for the 9B and 27B)")}),
    ("Z1 on the full carrier (51.7)", "jobs/c3/batch51.yaml 51.7", {
        "qwen3.6-27b": done("results/x51_carrier/x51_7-20261028T171646Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_carrier/x51_7-20261028T171646Z"),
        "muse-glimmer-30b": c("missing", "9B / Muse gap (51.7 designed for the 9B and 27B)")}),
    ("What is the address: dimension, methods, geometry (51.11)", "jobs/c3/batch51.yaml 51.11", {
        "qwen3.6-27b": c("partial", "part 2 only by design (parts 1, 3 not designed for the 27B)", "results/x51_addr/verdict-20261028T215138Z"),
        "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_addr/verdict-20261028T215138Z"), "muse-glimmer-30b": done("results/x51_addr/verdict-20261028T215138Z")}),
    ("Answer-direction control on Zach's Z2 (51.12 Z2)", "jobs/c3/batch51.yaml 51.12", {
        "qwen3.6-27b": done("results/x51_answer/x51_12-20261028T201842Z"), "nemotron-3.5-lightning": c("missing", LT2),
        "qwen3.5-9b": done("results/x51_answer/x51_12-20261028T201842Z"),
        "muse-glimmer-30b": c("missing", "9B / Muse gap (Z2 designed for the 9B and 27B)")}),
]  # fmt: skip


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
             f"Built at {head} (amendment 2: every test with a card or claim on the depth page; the 10 key rows first, "
             "in Dan's order). Status: done / partial / running / queued / missing / not tested (reason) / not designed. "
             "Every result UNVERIFIED until hand-checked. Each cell's source is in matrix.json.", "", f"{BOLT}.", "",
             f"{LT_GATE}.", "", "| test | " + " | ".join(SHORT[m] for m in MODELS) + " |", "|---|" + "---|" * len(MODELS)]  # fmt: skip
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


def main() -> Path:
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
