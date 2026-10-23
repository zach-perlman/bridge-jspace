"""cross_model_grid: one table of every finding on every model, each cell judged by its committed rule (Dan, 23 Oct).

Every cell reads the saved outputs of its run, or calls the repo's own verdict functions on the run's saved rows; no
rule is written here. Rules used (ids in RULES, printed in grid.md's mapping table):
  late read (finding 4)       scripts/d2_formats.py late_read: the answer's sentence hidden from the last tokens
  name vs digit (finding 3)   scripts/d2_parts.py cells / verdicts: valid-split, then H-digit-final-split
  tables and JSON             the same two, per format, as scripts/d2_formats.py main (computed in memory)
  order label / identity (5)  results/finding5_confirm/<run>_<stamp>/verdict.json, else finding5_confirm's functions
  order counting (6)          pointer_swap's v4x tests (saved analysis, else pointer_swap.analyze), at the spec's layers
  lens gate v1 / v2           results/lens_gate/<run>/summary.json "gate" / "gate_v2"
  stated bridge (2)           results/d1_verdict/<parts run>_<stamp>/verdict.json
  lens push (7)               results/early_push_where/<run>/summary.json (main rule) and analysis-v2.1-*/ (amended)
  lens write (8)              statement_positions readwrite summary: the write verdicts at the stated-bridge cell's set;
                              the fitted-code test's lens arm (pointer_fit): values only, open
  J-space removal (1)         Zach's own C1 verdict where his run has one (results/ablate_v2/c1_v2/<run>.json on his
                              branch); the animal-suite removal (ablate_pilot): the gap with an unpaired entity-bootstrap
                              interval, open (descriptive), not interpretable if the spec's gate G2 fails
Verdict words (Dan, 23 Oct): holds, fails, inconclusive (the rule itself says so; no control failed), not
interpretable (a control failed: which), not testable (no lens, gate or competence failed), missing (did not run,
failed, or no saved verdict: why), open (values shown, no committed rule).

Status of a cell without results: the queue ledgers (results/jobq/ledger*.jsonl), the queue states saved by
`jobq pull` (cache/jobq/queue_state*.json), the job logs it pulled (log/jobq/<id>/log.txt) and the specs in jobs/. A
job stopped by scripts/d1_precheck.py (exit 3; the reason it printed) or a statement_positions parts stage that finds
no transit cell from --lo on is "not testable"; a job behind it (pending, cancelled or never queued, through retries
of the same run) inherits that; a raw-format smoke stop (scripts/check_unedited.py, exit 3) is "missing: raw smoke
mismatch". Finding 2's cells show the same-share random part (jspace_matched; rand_sub where it ran) beside the lens
part, at the verdict's cell. DEVIATIONS: accepted deviations from a pre-registration, footnoted by spec.

uv run python scripts/cross_model_grid.py [--cells PAT[,PAT...]] [--no-values] [--out DIR]
  --cells      model:finding[:setting] glob patterns, e.g. "27b:f4:long*,olmo_hybrid:*" (models: 27b 9b olmo_hybrid
               32b olmo muse gemma 122b; findings: f1-f8, gate)
  --no-values  write only the status of each cell (has-run / failed / pending / running / blocked / not enqueued / no
               spec / no lens): no result file is opened
Writes results/cross_model/<UTC stamp>/: grid.csv (long format), grid.md, grid.json, sources.txt (cell -> files to
check by hand); with --no-values status.csv and status.md instead. Prints only the folder and counts.
"""

from __future__ import annotations

import argparse
import collections
import csv
import fnmatch
import functools
import io
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import d2_formats as DF
from scripts import d2_parts as DP

REPO = pins.REPO_ROOT
RESULTS = pins.RESULTS_DIR
OUT = RESULTS / "cross_model"
# Dan's verdict words (23 Oct): inconclusive only where a rule itself says so (the lens push's main rule); not
# interpretable only for a failed control; open: values shown under no committed rule (descriptive)
VERDICTS = ("holds", "fails", "inconclusive", "not interpretable", "not testable", "missing", "open")
SYMBOL = {"holds": "✓", "fails": "✗", "inconclusive": "≈", "not interpretable": "⚠", "not testable": "⊘",
          "missing": "·", "open": "○"}  # fmt: skip
ZACH_REF = "origin/zach/v8-breadth-1021"  # Zach's branch: his C1 verdicts (results/ablate_v2/c1_v2/<run>.json)
COLUMNS = ("model", "finding", "setting", "lens", "n", "value", "95% CI", "chance or control level", "verdict",
           "rule id", "spec commit", "result path")  # fmt: skip
STAMP_RE = r"\d{8}-\d{6}"
WHERE = {"question": "the question's tokens", "final": "the last tokens"}
# the draws' five listed answers only; the grid reads chance per run (chance_of: the formats' scenes list three, 33%).
# Kept for scripts/cross_model_figures.py, which still draws it on its prose / table / JSON panels too (flagged 23 Oct)
CHANCE = 0.20


# ---------------------------------------------------------------- models, findings, rules


@dataclass(frozen=True)
class Model:
    key: str
    label: str
    arch: str  # "hybrid" or "attention"
    lens_rows: tuple[str, str, str]  # results/lens_table rows: model label, main lens label, plain lens label ("" none)


MODELS = (
    Model("27b", "Qwen3.6-27B", "hybrid", ("Qwen3.6-27B", "published J++", "published plain J-lens (n1000)")),
    Model("9b", "Qwen3.5-9B", "hybrid", ("Qwen3.5-9B", "published J++", "")),
    Model("olmo_hybrid", "Olmo-Hybrid-7B", "hybrid", ("", "", "")),
    Model("32b", "Qwen3-32B", "attention", ("Qwen3-32B", "our J++ (64 prompts)", "published plain J-lens")),
    Model("olmo", "OLMo-3-7B-I", "attention", ("OLMo-3-7B-Instruct", "our J++ (64 prompts)", "mhough plain J-lens")),
    Model("muse", "Muse 30B", "attention", ("Muse Glimmer 30B", "Zach's J++ (every layer)", "")),
    Model("gemma", "Gemma 4 31B-it", "attention",
          ("Gemma 4 31B-it", "Zach's J++ (every layer)", "neuronpedia J++ (base model)")),
    Model("122b", "Qwen3.5-122B", "hybrid", ("Qwen3.5-122B-A10B (FP8)", "published J++", "")),
)  # fmt: skip
MODEL = {m.key: m for m in MODELS}


@dataclass(frozen=True)
class Finding:
    key: str
    number: str  # README's finding number ("" for the lens gate)
    name: str  # plain words, no internal codes
    lens: bool
    settings: tuple[str, ...]  # the rows of grid.md, in order
    codes: str  # internal names, for the mapping table only
    scripts: str


FINDINGS = (
    Finding("f1", "1", "Removing the J-space breaks recall, not the lookup", True,
            ("tasks, Zach's rule", "animal suite"), "C1 (Zach's J-space knock-out; the J-space removal)",
            "Zach's scripts/c1_v2.py (his branch); scripts/ablate_pilot.py"),
    Finding("f2", "2", "A lookup ignores the lens-readable part of a stated bridge", True,
            ("draw 1", "draw 2", "table", "JSON"), "D1 (topics, formats; parts)",
            "scripts/statement_positions.py parts, scripts/d1_verdict.py"),
    Finding("f3", "3", "The last tokens read the answer's digit, not the entity's name", False,
            ("draw 1", "draw 2", "draw 3", "prose", "table", "JSON"), "D2 parts (name vs digit)",
            "scripts/attn_knockout.py, scripts/d2_parts.py, scripts/d2_formats.py"),
    Finding("f4", "4", "A lookup ends in a late attention read of the answer's sentence", False,
            ("draw 1", "draw 2", "draw 3", "prose", "table", "JSON", "long context"), "D2 late read (C1b)",
            "scripts/attn_knockout.py, scripts/d2_formats.py"),
    Finding("f5", "5", "Order label for the 1st and 2nd sentence, the bridge's identity after", False,
            ("draw 1", "draw 2", "draw 3", "8 sentences", "12 sentences"), "D3 v4 / v5 (pointer_swap)",
            "scripts/pointer_swap.py, scripts/finding5_confirm.py"),
    Finding("f6", "6", "The order label counts order in the list, not place in the text", False,
            ("filler moved", "one statement more", "one statement fewer"), "D3 v4x (pointer_v4x)",
            "scripts/pointer_swap.py (v4x tests)"),
    Finding("gate", "", "The lens names a stated bridge where it is stated (lens gate)", True,
            ("v1 (at the word)", "v2 (after the word)"), "lens gate v1 / v2", "scripts/lens_gate.py"),
    Finding("f7", "7", "A lens push writes a stated bridge for recall; the lookup does not follow", True,
            ("main rule", "amended rule", "main rule, draw 2", "amended rule, draw 2"),
            "D4 v2 / v2.1 (early_push_where)", "scripts/early_push_where.py"),
    Finding("f8", "8", "Where the lens writes the bridge, the lookup still does not follow it", True,
            ("stated bridge, draw 1", "stated bridge, draw 2", "last tokens"), "D1 readwrite; D3b lens arm",
            "scripts/statement_positions.py readwrite, scripts/pointer_fit.py"),
)  # fmt: skip
FINDING = {f.key: f for f in FINDINGS}

RULES = {
    "late-read": "the answer's sentence hidden from the last tokens in every attention layer (every layer on "
    "attention-only models) leaves <= 20% right with the Wilson upper bound <= 30%; the off-path sentence hidden "
    "there keeps >= 90% (lower bound >= 85%); on a hybrid, hidden in every DeltaNet layer instead keeps >= 90%. "
    "Memory -> prompt, items right unedited (fixed 22 Oct; scripts/d2_formats.py late_read)",
    "name-digit": "the off-path sentence's parts hidden keep >= 90% at both places (valid-split); then the sentence "
    "without its name hidden from the last tokens leaves <= 35% right and without its digit >= 70% "
    "(H-digit-final-split). Memory -> prompt (amended 22 Oct 16:40; scripts/d2_parts.py verdicts)",
    "formats": "the late-read and name-vs-digit rules per format (prose, table, JSON), memory -> prompt "
    "(scripts/d2_formats.py, fixed 22 Oct evening)",
    "order-identity": "A: 1st-2nd asked, position - identity, entity-cluster lower bound > 0; B: 3rd on, identity - "
    "position >= 0 with lower bound >= -0.05; holds iff A and B. Layer: the last swept layer where the donor's digit "
    "has its Wilson upper bound < 10%, or fixed (Qwen3.6-27B: 50) (scripts/finding5_confirm.py)",
    "counting": "filler moved: the order slot's lower bound above the same place's upper bound, pooled and in >= 2 "
    "of 3 topics at one decisive layer; one more / one fewer: from the start above from the end and the same place, "
    "both layouts, same layer (scripts/pointer_swap.py v4x_tests). Decisive layers: the 27B's 48 and 50 and OLMo's "
    "17-19 fixed; elsewhere the swept layers where the donor's digit has its Wilson upper bound < 10% (the specs)",
    "lens-gate-v1": "the bridge in the lens's top 10 at its own sentence on >= 50% of items, the other bridge on <= "
    "20% (scripts/lens_gate.py gate, 22 Oct)",
    "lens-gate-v2": "the same bars read after the bridge's word (scripts/lens_gate.py gate_v2, 22 Oct 23:00)",
    "stated-bridge": "at the cell chosen without the lens: the lens-readable part alone switches <= 10% of lookups "
    "and the rest >= 50%, while the lens-readable part switches >= 30% of recalls (the control); where set, lookups "
    "keep their answer under the lens-part patch on >= 80% (scripts/d1_verdict.py)",
    "push-main": "rule v2: the valid cell with the most recall; holds (H-around) iff the lookup switches <= 10% and "
    "the scene-paired recall - lookup gap's lower bound >= 20 points; inconclusive where the rule says so (no control "
    "failed there); not interpretable when the off-path check fails or no cell writes recall (scripts/"
    "early_push_where.py decide)",
    "push-amended": "rule v2.1: v2 among cells from layer 20 on (Qwen3.5-9B: 10); written knowing the old data, "
    "reported beside the main rule",
    "lens-write": "statement_positions' write verdicts (written / not written / inconclusive) at the stated-bridge "
    "cell's set, primary window; holds iff recall is written and the lookup not written (recall not written: no "
    "positive control)",
    "fitted-code": "scripts/pointer_fit.py's rule judges the fitted position code; its lens push arm has no rule of "
    "its own: values only, verdict open (Dan, 23 Oct)",
    "zach-c1": "Zach's C1-graded rule (scripts/c1_v2.py on his branch, fixed 21 Oct): at the middle band, the "
    "memory-final words lose >= 30 points more accuracy than the prompt-final words under the top-10 lens "
    "knock-out, and every word's rotated control stays within 10 points of unedited; his verdict file is read as it "
    "is (results/ablate_v2/c1_v2/<run>.json on origin/zach/v8-breadth-1021)",
    "removal": "descriptive, no committed rule (Dan, 23 Oct): the gap = lookups (BL, RL) - recalls (BR, RR) right "
    "under J-space removal, clean question, with a 95% interval from an unpaired bootstrap over bridge entities "
    "(stats.cluster_bootstrap's resampling, entities drawn with replacement within each group, 4000 draws, seed 0). "
    "Where the run's spec has gate G2 (the control removals keep >= 90% on every family and step), a failed G2 makes "
    "the cell not interpretable. The 32B, Gemma and Muse runs (and the 27B's d2_abl_read_*_v2 copies) ran without "
    "the random-dictionary control (too large next to the model on an 80 GB GPU): G2 reads the rotated control "
    "alone. Zach's pilots (the 27B's abl_rot_v1, Gemma's refit, the 122B's abl_v1) have no G2",
}
# How finding 1's interval is computed, in plain words (grid.md's legend and its choices list)
GAP_METHOD = (
    "J-space removal (finding 1, animal suite) has no committed rule, so its cell is descriptive: the gap is the "
    "share of lookups right minus the share of recalls right with the J-space removed (the clean question; items "
    "pooled within each group). Its 95% interval: the bridge animals are drawn with replacement, separately for "
    "the lookup items and for the recall items (unpaired), 4000 times with seed 0; each draw gives the lookups' "
    "mean minus the recalls' mean, and the interval is the 2.5th to 97.5th percentile of those differences. "
    "stats.cluster_bootstrap does this resampling for one mean only, so the grid applies it to each group and takes "
    "the difference (scripts/cross_model_grid.py gap_ci). Chosen after seeing the data; accepted by Dan (23 Oct)."
)
# Choices made after seeing the data (grid.md lists them; the README keeps its own list)
CHOICES = (
    "Where the lens writes the bridge (finding 8, stated bridge): the cell holds iff the readwrite verdicts say "
    "recall written and lookup not written; recall not written means no positive control (not interpretable). The "
    "combination of the two committed per-family verdicts was written by the grid agent and accepted by Dan (23 Oct).",
    "Counting (finding 6) on Qwen3.5-9B, Qwen3-32B, Muse, Gemma and Qwen3.5-122B: the decisive layers are the swept "
    "layers where the donor's digit has its Wilson upper bound < 10% (the specs' rule, applied by the grid: "
    "pointer_swap's code tests every swept layer). Accepted by Dan (23 Oct).",
    "Late read (finding 4), draw 1: judged by the late-read rule fixed on 22 Oct for the second draws (the first "
    "draws ran under the older 'needed' rule). Accepted by Dan (23 Oct).",
    "The lens push's main rule says 'inconclusive' where the lookup moves 10-30%: shown as its own word, "
    "'inconclusive', not as a failed control (Dan, 23 Oct).",
    GAP_METHOD,
    "A late read that fails with its interval around chance (guessing among the scene's listed answers: 20% in the "
    "draws' five, 33% in the prose / table / JSON scenes' three; from each run's cases) is footnoted 'at chance' "
    "(Gemma's reading in the README; Dan, 23 Oct; chance per run since 23 Oct, it was 20% everywhere before).",
    "Seven verdict words: 'open' is its own word for a cell that shows values under no committed rule (finding 1's "
    "animal-suite removal, finding 8's last-token lens arm), never 'missing' for that reason (Dan, 23 Oct).",
)
# Accepted deviations from a pre-registration: (a pattern in the command of a spec that writes the cell's run, the
# cell's footnote). Attached by spec, not by result, so a cell carries its note while the run is pending or missing
DEVIATIONS = (
    (r"--map gemma4itf_d1_(topics2|formats)_map", "n = 167 (topics) / 169 (formats) instead of the pre-registered 180: "
     "73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct"),
)  # fmt: skip


# ---------------------------------------------------------------- the cell registry


@dataclass
class Cell:
    model: str
    finding: str
    setting: str
    kind: str
    run: str = ""
    jobs: tuple[str, ...] = ()
    role: str = "main"  # main, or the lens it is listed beside: "plain J-lens", "base-model J++"
    opts: dict[str, Any] = field(default_factory=dict)
    why: str = ""  # for a cell with no run: why (no spec, no lens)


def _cells() -> list[Cell]:
    """The registry: one Cell per (model, finding, setting, lens role). Job ids are found from the specs by run name
    (Jobs.by_run), so retries (_r2, _q, ...) need no listing here."""
    out: list[Cell] = []

    def add(model: str, finding: str, setting: str, kind: str, run: str = "", role: str = "main", why: str = "",
            **opts: Any) -> None:  # fmt: skip
        out.append(Cell(model, finding, setting, kind, run, (run,) if run else (), role, opts, why))

    def none(model: str, finding: str, setting: str, why: str = "no spec") -> None:
        add(model, finding, setting, "none", why=why)

    p = {m: pins.TARGETS[t]["run_prefix"] for m, t in (("9b", "qwen3.5-9b"), ("32b", "qwen3-32b"),
         ("olmo", "olmo-3-7b-instruct"), ("muse", "muse-glimmer-30b"), ("gemma", "gemma-4-31b-it"),
         ("olmo_hybrid", "olmo-hybrid-7b-instruct-dpo"), ("122b", "qwen3.5-122b-a10b"))}  # fmt: skip
    # finding 1: Zach's C1 rule (his branch) where his runs have one; the animal-suite removal (ablate_pilot) beside.
    # g2: the run's spec has the gate G2 (the copies of the OLMo ladder's rule); Zach's pilots have none
    add("27b", "f1", "tasks, Zach's rule", "zach_c1", "full2_ko_v1")
    add("gemma", "f1", "tasks, Zach's rule", "zach_c1", "gemma4itf_full_ko_v1")
    add("27b", "f1", "animal suite", "removal", "abl_rot_v1")
    add("9b", "f1", "animal suite", "removal", "qwen35_9b_abl_rot_v1", g2=True)
    add("32b", "f1", "animal suite", "removal", "qwen3_32b_jpp_abl_rot_v1", g2=True)
    add("olmo", "f1", "animal suite", "removal", "olmo3_7b_instruct_jpp_abl_rot_raw_v1", g2=True)
    add("olmo", "f1", "animal suite", "removal", "olmo3_7b_instruct_abl_rot_raw_v1", role="plain J-lens", g2=True)
    add("muse", "f1", "animal suite", "removal", "muse30b_abl_rot_v1", g2=True)
    add("gemma", "f1", "animal suite", "removal", "gemma4itf_abl_rot_v1", g2=True)
    add("gemma", "f1", "animal suite", "removal", "gemma4itr_abl_rot_v1", role="refit J++")
    add("122b", "f1", "animal suite", "removal", "qwen35_122b_abl_rot_v1", g2=True)
    add("122b", "f1", "animal suite", "removal", "qwen35_122b_abl_v1", role="Zach's pilot")
    # finding 2: the stated-bridge split. draw 1 = the four-topic scenes (d1_topics_v1), draw 2 = d1_topics_v2
    add("27b", "f2", "draw 1", "d1", "d1_topics_parts_27b")
    add("27b", "f2", "draw 2", "d1", "d1_topics2_parts_27b")
    add("27b", "f2", "draw 2", "d1", "qwen36_27b_jlens_d1_topics2_parts", role="plain J-lens")
    add("9b", "f2", "draw 2", "d1", "qwen35_9b_d1_topics2_parts")
    add("32b", "f2", "draw 1", "d1", "qwen3_32b_jpp_d1_topics_parts")
    add("32b", "f2", "draw 1", "d1", "qwen3_32b_d1_topics_parts", role="plain J-lens")
    add("olmo", "f2", "draw 2", "d1", "olmo3_7b_instruct_jpp_d1_topics2_parts")
    add("olmo", "f2", "draw 2", "d1", "olmo3_7b_instruct_d1_topics2_parts", role="plain J-lens")
    add("muse", "f2", "draw 2", "d1", "muse30b_d1_topics2_parts")
    add("gemma", "f2", "draw 2", "d1", "gemma4itf_d1_topics2_parts")
    add("gemma", "f2", "draw 2", "d1", "gemma4itb_d1_topics2_parts", role="base-model J++")
    add("122b", "f2", "draw 2", "d1", "qwen35_122b_d1_topics2_parts")
    for m, run in (("27b", "d1_formats_parts_27b"), ("9b", "qwen35_9b_d1_formats_parts"),
                   ("32b", "qwen3_32b_jpp_d1_formats_parts"), ("olmo", "olmo3_7b_instruct_jpp_d1_formats_parts"),
                   ("muse", "muse30b_d1_formats_parts"), ("gemma", "gemma4itf_d1_formats_parts"),
                   ("122b", "qwen35_122b_d1_formats_parts")):  # fmt: skip
        add(m, "f2", "table", "d1_formats", run)
    # findings 3 and 4: three draws of prose scenes (main, seed2, seed3), tables / JSON, the long context
    d34 = {
        "27b": ("d2_parts_v2_27b", "d2_parts_seed2_27b", "d2_parts_seed3_27b", "d2_v4_late_read",
                "d2_late_read_seed2_27b", "d2_late_read_seed3_27b", "d2_formats_27b", "d2_late_read_long_27b_r3"),
        "olmo": ("olmo3_7b_instruct_d2_parts_v2", "olmo3_7b_instruct_d2_parts_seed2", "olmo3_7b_instruct_d2_parts_seed3",
                 "olmo3_7b_instruct_d2_v4_late_read_v3", "olmo3_7b_instruct_d2_late_read_seed2",
                 "olmo3_7b_instruct_d2_late_read_seed3", "olmo3_7b_instruct_d2_formats",
                 "olmo3_7b_instruct_d2_late_read_long"),
        "olmo_hybrid": ("olmo_hybrid_7b_d2_parts_v2", "olmo_hybrid_7b_d2_parts_seed2", "olmo_hybrid_7b_d2_parts_seed3",
                        "olmo_hybrid_7b_d2_v4_late_read_v3", "olmo_hybrid_7b_d2_late_read_seed2",
                        "olmo_hybrid_7b_d2_late_read_seed3", "olmo_hybrid_7b_d2_formats",
                        "olmo_hybrid_7b_d2_late_read_long"),
        "9b": ("qwen35_9b_d2_parts_v2", "qwen35_9b_d2_parts_seed2", "qwen35_9b_d2_parts_seed3",
               "qwen35_9b_d2_v4_late_read_r2", "qwen35_9b_d2_late_read_seed2", "qwen35_9b_d2_late_read_seed3",
               "qwen35_9b_d2_formats", "qwen35_9b_d2_late_read_long"),
        "32b": ("qwen3_32b_d2_parts_v2", "qwen3_32b_d2_parts_seed2", "qwen3_32b_d2_parts_seed3",
                "qwen3_32b_d2_v4_late_read_v2_r2", "qwen3_32b_d2_late_read_seed2", "qwen3_32b_d2_late_read_seed3",
                "qwen3_32b_d2_formats", "qwen3_32b_d2_late_read_long"),
        "muse": ("muse30b_d2_parts", "muse30b_d2_parts_seed2", "muse30b_d2_parts_seed3", "muse30b_d2_late_read",
                 "muse30b_d2_late_read_seed2", "muse30b_d2_late_read_seed3", "muse30b_d2_formats",
                 "muse30b_d2_late_read_long"),
        "gemma": ("gemma4it_d2_parts_v2", "gemma4it_d2_parts_seed2", "gemma4it_d2_parts_seed3",
                  "gemma4it_d2_v4_late_read_v3_r2", "gemma4it_d2_late_read_seed2", "gemma4it_d2_late_read_seed3",
                  "gemma4it_d2_formats", "gemma4it_d2_late_read_long"),
        "122b": ("qwen35_122b_d2_parts", "qwen35_122b_d2_parts_seed2", "qwen35_122b_d2_parts_seed3",
                 "qwen35_122b_d2_late_read", "qwen35_122b_d2_late_read_seed2", "qwen35_122b_d2_late_read_seed3",
                 "qwen35_122b_d2_formats", "qwen35_122b_d2_late_read_long"),
    }  # fmt: skip
    for m, (p1, p2, p3, l1, l2, l3, fmt, long) in d34.items():
        for i, (pr, lr) in enumerate(((p1, l1), (p2, l2), (p3, l3)), 1):
            add(m, "f3", f"draw {i}", "parts", pr)
            add(m, "f4", f"draw {i}", "late", lr, first_draw=i == 1)
        add(m, "f3", "prose", "formats_f3", fmt)
        add(m, "f4", "prose", "formats_f4", fmt)
        add(m, "f4", "long context", "late", long)
    # finding 5: draws 1-3 (main, seed2, seed3) and the 8 / 12-statement lists. layer: fixed (the 27B's 50), else
    # the spec's finding5_confirm --layers (Jobs.f5_layers), else the run's swept layers
    add("27b", "f5", "draw 1", "f5", "d3v4_swap_topics", layer=50)
    add("27b", "f5", "draw 2", "f5", "d3v4_seed2_swap_27b", layer=50)
    add("27b", "f5", "draw 3", "f5", "d3v4_seed3_swap_27b", layer=50)
    f5 = {"9b": "qwen35_9b_d3v4_swap_r2", "32b": "qwen3_32b_d3v4_swap_r2", "olmo": "olmo3_7b_instruct_d3v4_swap_fn",
          "muse": "muse30b_d3v4_swap", "gemma": "gemma4it_d3v4_swap_v2_r2", "olmo_hybrid": "olmo_hybrid_7b_d3v4_swap_fn",
          "122b": "qwen35_122b_d3v4_swap"}  # fmt: skip
    for m, first in f5.items():
        add(m, "f5", "draw 1", "f5", first, rand_gate=m == "muse")
        add(m, "f5", "draw 2", "f5", f"{p[m]}d3v4_seed2_swap")
        add(m, "f5", "draw 3", "f5", f"{p[m]}d3v4_seed3_swap")
    for m in ("27b", *f5):
        tail = "_27b" if m == "27b" else ""
        pre = "" if m == "27b" else p[m]
        add(m, "f5", "8 sentences", "f5", f"{pre}d3v5_len8_swap{tail}", level="e8-digit", sentences=8)
        add(m, "f5", "12 sentences", "f5", f"{pre}d3v5_len12_swap{tail}", level="e12-word", sentences=12)
    # finding 6: counting (one run, three settings); by_value: the spec picks the decisive layers by the donor-digit
    # rule; fixed primaries otherwise (the 27B 48 / 50, OLMo-3 and Olmo-Hybrid 17-19)
    add("27b", "f6", "filler moved", "f6", "d3v4x_swap_main")
    add("9b", "f6", "filler moved", "f6", "qwen35_9b_d3v4x_swap_r2", by_value=True)
    add("32b", "f6", "filler moved", "f6", "qwen3_32b_d3v4x_swap_r3", by_value=True)
    add("olmo", "f6", "filler moved", "f6", "olmo3_7b_instruct_d3v4x_swap")
    add("olmo_hybrid", "f6", "filler moved", "f6", "olmo_hybrid_7b_d3v4x_swap")
    add("muse", "f6", "filler moved", "f6", "muse30b_d3v4x_swap", by_value=True, rand_gate=True)
    add("gemma", "f6", "filler moved", "f6", "gemma4it_d3v4x_swap_r2", by_value=True)
    add("122b", "f6", "filler moved", "f6", "qwen35_122b_d3v4x_swap", by_value=True)
    # lens gates (v1 and v2 from one summary where the run has both)
    gates = {"27b": [("lens_gate_27b", "main", "v1"), ("lens_gate_v2_27b", "main", "v2"),
                     ("qwen36_27b_jlens_lens_gate_v2", "plain J-lens", "both")],
             "9b": [("qwen35_9b_lens_gate", "main", "v1"), ("qwen35_9b_lens_gate_v2", "main", "v2")],
             "32b": [("qwen3_32b_jpp_lens_gate", "main", "both"), ("qwen3_32b_lens_gate", "plain J-lens", "v1"),
                     ("qwen3_32b_lens_gate_v2", "plain J-lens", "v2")],
             "olmo": [("olmo3_7b_instruct_jpp_lens_gate", "main", "both"),
                      ("olmo3_7b_instruct_lens_gate_v2", "plain J-lens", "both")],
             "muse": [("muse30b_lens_gate_v2", "main", "both")],
             "gemma": [("gemma4itf_lens_gate_v2", "main", "both"), ("gemma4itb_lens_gate_v2_r2", "base-model J++", "both")],
             "122b": [("qwen35_122b_lens_gate_v2", "main", "both")]}  # fmt: skip
    for m, lst in gates.items():
        for run, role, which in lst:
            for v, setting in (("v1", "v1 (at the word)"), ("v2", "v2 (after the word)")):
                if which in (v, "both"):
                    add(m, "gate", setting, "gate", run, role=role, gate=v)
    # finding 7: the lens push on fresh scenes (one run, two settings) and a second fresh draw
    d4 = {"27b": ("d4_where_fresh_27b", "d4_where_fresh_seed2_27b"), "9b": ("qwen35_9b_d4_where", "qwen35_9b_d4_where_fresh_seed2"),
          "32b": ("qwen3_32b_jpp_d4_where", ""), "olmo": ("olmo3_7b_instruct_jpp_d4_where_raw", ""),  # chat copy not run
          "muse": ("muse30b_d4_where", ""), "gemma": ("gemma4itf_d4_where", ""),
          "122b": ("qwen35_122b_d4_where", "qwen35_122b_d4_where_fresh_seed2")}  # fmt: skip
    for m, (first, second) in d4.items():
        add(m, "f7", "main rule", "d4", first)
        if second:
            add(m, "f7", "main rule, draw 2", "d4", second, suffix=", draw 2")
    # finding 8: the lens write at the stated bridge (at its stated-bridge cell) and the fitted-code test's lens arm
    rw = {"27b": [("d1_topics_rw_27b", "d1_topics_parts_27b", "main", 1), ("d1_topics2_rw_27b", "d1_topics2_parts_27b", "main", 2),
                  ("qwen36_27b_jlens_d1_topics2_rw", "qwen36_27b_jlens_d1_topics2_parts", "plain J-lens", 2)],
          "9b": [("qwen35_9b_d1_topics2_rw", "qwen35_9b_d1_topics2_parts", "main", 2)],
          "32b": [("qwen3_32b_jpp_d1_topics_rw", "qwen3_32b_jpp_d1_topics_parts", "main", 1),
                  ("qwen3_32b_d1_topics_rw", "qwen3_32b_d1_topics_parts", "plain J-lens", 1)],
          "olmo": [("olmo3_7b_instruct_jpp_d1_topics2_rw", "olmo3_7b_instruct_jpp_d1_topics2_parts", "main", 2),
                   ("olmo3_7b_instruct_d1_topics2_rw", "olmo3_7b_instruct_d1_topics2_parts", "plain J-lens", 2)],
          "muse": [("muse30b_d1_topics2_rw", "muse30b_d1_topics2_parts", "main", 2)],
          "gemma": [("gemma4itf_d1_topics2_rw", "gemma4itf_d1_topics2_parts", "main", 2),
                    ("gemma4itb_d1_topics2_rw", "gemma4itb_d1_topics2_parts", "base-model J++", 2)],
          "122b": [("qwen35_122b_d1_topics2_rw", "qwen35_122b_d1_topics2_parts", "main", 2)]}  # fmt: skip
    for m, lst in rw.items():
        for run, parts, role, draw in lst:
            add(m, "f8", f"stated bridge, draw {draw}", "rw", run, role=role, parts=parts)
    for m, run in (("27b", "d3v4_fit_main"), ("9b", "qwen35_9b_d3b_fit_v2"), ("32b", "qwen3_32b_jpp_d3b_fit_v2"),
                   ("gemma", "gemma4itf_d3b_fit_v2"), ("olmo", "olmo3_7b_instruct_jpp_d3b_fit_v2"),
                   ("122b", "qwen35_122b_d3b_fit_v2")):  # fmt: skip
        add(m, "f8", "last tokens", "fitlens", run)
    add("olmo", "f8", "last tokens", "fitlens", "olmo3_7b_instruct_d3b_fit_v2", role="plain J-lens")
    # lens findings on a model without a lens
    for f in FINDINGS:
        if f.lens:
            for s in f.settings:
                none("olmo_hybrid", f.key, s, "no lens")
    # every other grid cell without a registered run: no spec
    have = {(c.model, c.finding, s) for c in out for s in settings_of(c)}
    for f in FINDINGS:
        for s in f.settings:
            for m in MODELS:
                if (m.key, f.key, s) not in have:
                    none(m.key, f.key, s)
    return out


# ---------------------------------------------------------------- jobs: specs, ledger, queue


class Jobs:
    """Specs (jobs/*/<id>.yaml), the ledger records (latest per id) and the queue state saved by `jobq pull`."""

    def __init__(self, repo: Path = REPO):
        import yaml

        self.repo = repo
        self.specs: dict[str, Path] = {p.stem: p for p in repo.glob("jobs/*/*.yaml") if p.name != "titles.yaml"}
        self._spec_text: dict[str, dict] = {}
        self.ledger: dict[str, dict] = {}
        for p in sorted((repo / "results" / "jobq").glob("ledger*.jsonl")):  # every box's ledger, if kept apart
            for line in p.read_text().splitlines():
                if line.strip():
                    r = json.loads(line)
                    old = self.ledger.get(r["id"])
                    if old is None or (r.get("ended_at") or "") >= (old.get("ended_at") or ""):
                        self.ledger[r["id"]] = r
        self.queued: dict[str, str] = {}
        for state in sorted((repo / "cache" / "jobq").glob("queue_state*.json")):  # every box's (jobq pull)
            q = json.loads(state.read_text())
            self.queued |= {r["id"]: s for s in ("pending", "running") for r in q.get(s, [])}
        self.by_run: dict[str, list[str]] = collections.defaultdict(list)  # run name -> the specs that write it
        for job, p in sorted(self.specs.items()):
            for run in dict.fromkeys(re.findall(r"--name (\w+)", p.read_text())):
                self.by_run[run].append(job)
        self._yaml = yaml

    def jobs_of(self, cell: Cell) -> tuple[str, ...]:
        """The cell's job ids: every spec that writes its run (retries _r2, _q, ... included)."""
        return tuple(dict.fromkeys([*cell.jobs, *self.by_run.get(cell.run, [])]))

    def deviations(self, jobs: tuple[str, ...]) -> list[str]:
        """The DEVIATIONS notes whose pattern a command of these jobs' specs matches."""
        cmds = [self.spec(j).get("command") or "" for j in jobs]
        return [note for pat, note in DEVIATIONS if any(re.search(pat, c) for c in cmds)]

    def f5_layers(self, run: str, level: str | None) -> list[int] | None:
        """The --layers its spec gives scripts/finding5_confirm.py for `run` (and `level`), if a spec does."""
        for job in self.by_run.get(run, []):
            s = self.spec(job)
            for cmd in (s.get("figures_command") or "", s.get("command") or ""):
                for m in re.finditer(
                    rf"finding5_confirm\.py --run {re.escape(run)} --layers ([\d ]+)(--level (\S+))?", cmd
                ):
                    if level is None or m.group(3) == level:
                        return [int(x) for x in m.group(1).split()]
        return None

    def spec(self, job: str) -> dict:
        if job not in self._spec_text and job in self.specs:
            self._spec_text[job] = self._yaml.safe_load(self.specs[job].read_text()) or {}
        return self._spec_text.get(job, {})

    def latest(self, jobs: tuple[str, ...]) -> dict | None:
        recs = [self.ledger[j] for j in jobs if j in self.ledger]
        return max(recs, key=lambda r: r.get("ended_at") or "") if recs else None

    @functools.cache  # noqa: B019 (one Jobs per build)
    def added_commit(self, job: str) -> str:
        if job not in self.specs:
            return ""
        p = subprocess.run(["git", "-C", str(self.repo), "log", "--diff-filter=A", "--format=%h", "-1", "--",
                            str(self.specs[job].relative_to(self.repo))], capture_output=True, text=True, check=False)  # fmt: skip
        return p.stdout.strip()

    def commit(self, cell: Cell) -> str:
        """The commit the job ran at (ledger), else the commit that added its spec; '-' without a spec."""
        rec = self.latest(cell.jobs)
        if rec and rec.get("commit"):
            return rec["commit"][:7]
        for j in cell.jobs:
            if c := self.added_commit(j):
                return f"{c} (spec added)"
        return "-"

    def log(self, job: str) -> str:
        """The job's log as `jobq pull` brought it (log/jobq/<id>/log.txt), or ''."""
        p = self.repo / "log" / "jobq" / job / "log.txt"
        return p.read_text(errors="replace") if p.exists() else ""

    def stop_of(self, rec: dict) -> tuple[str, str] | None:
        """(verdict word, why) when a failed job's chain stopped because the test cannot be made: scripts/d1_precheck.py
        (exit 3: the gate failed, or too few eligible scenes; its printed reason) or statement_positions parts finding
        no transit cell from --lo on (the stated bridge can no longer be moved there): not testable;
        scripts/check_unedited.py (exit 3, a raw-format smoke mismatch): missing. None otherwise."""
        cmd = rec.get("command", "")
        if rec.get("status") != "failed":
            return None
        if "AssertionError: no transit cell in any family" in self.log(rec["id"]):
            lo = re.search(r"statement_positions\.py parts .*?--lo (\d+)", cmd)
            return (
                "not testable",
                f"no layer from {lo.group(1) if lo else '--lo'} on where the stated bridge can still be moved",
            )
        if rec.get("exit_code") != 3 or not ("d1_precheck" in cmd or "check_unedited" in cmd):
            return None
        gate = re.search(r"--gate (\w+)", cmd)
        s = RESULTS / "lens_gate" / gate.group(1) / "summary.json" if gate else None
        passed = json.loads(s.read_text())["gate"]["pass"] if s and s.exists() else None
        if passed is False:
            return "not testable", f"gate v1 failed ({gate.group(1) if gate else '?'})"
        if "check_unedited" in cmd and (passed or "d1_precheck" not in cmd):
            return "missing", "raw smoke mismatch: the smoke's unedited answers differ from the raw competence run"
        said = [x for x in self.log(rec["id"]).splitlines() if x.startswith("d1_precheck:") and "STOP" in x]
        how = said[-1].removeprefix("d1_precheck:").strip() if said else "too few eligible scenes, or the gate"
        return "not testable", f"stopped by the precheck in {rec['id']}: {how}"

    def attempts(self, job: str) -> tuple[str, ...]:
        """The job and every spec that writes one of its runs (its retries): a dependency is judged by its runs."""
        names = re.findall(r"--name (\w+)", self.spec(job).get("command") or "")
        return tuple(dict.fromkeys([job, *(j for n in names for j in self.by_run.get(n, []))]))

    def status(self, jobs: tuple[str, ...], values: bool = True, _seen: frozenset = frozenset()) -> tuple[str, str]:
        """(status, reason) of a run that has no results: failed / pending / running / blocked / not enqueued / no
        spec, or 'not testable' (stop_of, or behind such a job: pending, cancelled or never queued; only with
        values)."""
        if not jobs:
            return "no spec", "no spec"
        for j in jobs:  # a retry in the queue outranks an earlier attempt's failure
            if j in self.queued:
                deps = self.spec(j).get("depends_on") or []
                for d in deps:
                    if d in _seen:
                        continue
                    st, why = self.status((d,), values, _seen | {j})
                    if st == "not testable":
                        return st, blocks(why, j)
                    if st == "failed":
                        return "blocked", f"{j} waits on {d}, which failed"
                return self.queued[j], f"{j} is {self.queued[j]} in the queue"
        rec = self.latest(jobs)
        if rec is not None:
            if rec.get("status") == "failed":
                stop = self.stop_of(rec) if values else None
                if stop:
                    return stop
                err = (rec.get("error") or "").strip().splitlines()
                stage = ("figures" if rec.get("figures_exit") not in (None, 0) else
                         "examples" if rec.get("examples_exit") not in (None, 0) else "run")  # fmt: skip
                why = f"job {rec['id']} failed at the {stage} stage (exit {rec.get('exit_code')})"
                return "failed", why + (f": {err[-1][:120]}" if err and values else "")
            if rec.get("status") == "done":
                return "done, no results", f"job {rec['id']} done but its results are not here (pull?)"
        spec_jobs = [j for j in jobs if j in self.specs]
        if spec_jobs and values:  # never ran (cancelled or never queued): not testable if every attempt waits on a stop
            behind = [self.stopped_upstream(j, _seen) for j in spec_jobs]
            if all(behind):
                return "not testable", behind[-1] or ""
        if spec_jobs:
            return "not enqueued", f"spec {jobs[-1]} not run (not in the queue or the ledger)"
        return "no spec", "no spec"

    def stopped_upstream(self, job: str, _seen: frozenset = frozenset()) -> str | None:
        """Why a job that never ran cannot run: a dependency's runs are not testable (stop_of, possibly further up)."""
        for d in self.spec(job).get("depends_on") or []:
            if d not in _seen:
                st, why = self.status(self.attempts(d), True, _seen | {job})
                if st == "not testable":
                    return blocks(why, job)
        return None


def blocks(why: str, job: str) -> str:
    """'<stop>; blocks a' -> '<stop>; blocks a, then b' (the chain behind a stop, nearest first)."""
    return f"{why}, then {job}" if "; blocks " in why else f"{why}; blocks {job}"


# ---------------------------------------------------------------- reading results


def jl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def latest_dir(parent: Path, run: str, tag: str = "") -> Path | None:
    """parent/<run><tag>_<stamp>/ (the newest), matched exactly so that run names that extend `run` never match."""
    pat = re.compile(re.escape(run + tag) + "_" + STAMP_RE)
    hits = sorted(d for d in parent.glob(f"{run}{tag}_*") if d.is_dir() and pat.fullmatch(d.name))
    return hits[-1] if hits else None


def required(cell: Cell) -> Path:
    """The file whose presence means the run is here (no result is read)."""
    k, r = cell.kind, cell.run
    if k in ("late", "parts", "formats_f3", "formats_f4"):
        return RESULTS / "attn_knockout" / r / "rows.jsonl"
    if k in ("f5", "f6"):
        return RESULTS / "pointer_swap" / r / "outcomes.jsonl"
    if k == "gate":
        return RESULTS / "lens_gate" / r / "summary.json"
    if k in ("d1", "d1_formats"):
        return RESULTS / "statement_positions" / r / "outcomes.jsonl"
    if k == "d4":
        return RESULTS / "early_push_where" / r / "summary.json"
    if k == "rw":
        return RESULTS / "statement_positions" / r / "summary.json"
    if k == "fitlens":
        return RESULTS / "pointer_fit" / r / "summary.json"
    if k == "removal":
        return RESULTS / "ablate_pilot" / r / "summary.json"
    if k == "zach_c1":  # on Zach's branch, not in this tree (present() reads it with git show)
        return RESULTS / "ablate_v2" / "c1_v2" / f"{r}.json"
    raise ValueError(k)


@functools.cache
def zach_file(path: str) -> str | None:
    """A file on Zach's branch (git show), or None."""
    p = subprocess.run(["git", "-C", str(REPO), "show", f"{ZACH_REF}:{path}"], capture_output=True, text=True,
                       check=False)  # fmt: skip
    return p.stdout if p.returncode == 0 else None


def present(cell: Cell) -> bool:
    """Is the run's result here (no result is read)."""
    if cell.kind == "zach_c1":
        return zach_file(rel(required(cell))) is not None
    return required(cell).exists()


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


PREFIXES = sorted(
    ((t["run_prefix"], name) for name, t in pins.TARGETS.items() if t["run_prefix"]), key=lambda x: -len(x[0])
)  # longest prefix first
LENS_KNOWN = {  # sha256 prefix -> (type, source); the pins in src/bridge_jspace/pins.py
    "bbef480b": ("J++", "published (neuronpedia)"), "1718c8c5": ("plain J-lens", "published (neuronpedia, n1000)"),
    "8cda12f7": ("J++", "published (neuronpedia)"), "0af5ccf2": ("plain J-lens", "published (neuronpedia)"),
    "b847dbba": ("plain J-lens", "published (mhough)"), "d16d81d8": ("J++", "Zach (every layer)"),
    "ef50bc54": ("J++", "published (neuronpedia, base model)"), "323733a9": ("J++", "Zach (refit, layers 24-45)"),
    "90fc5e52": ("J++", "Zach"), "b771e502": ("J++", "published (neuronpedia)"), "0b092e93": ("J++", "ours (old fit)"),
}  # fmt: skip
LENS_FREE = ("late", "parts", "formats_f3", "formats_f4", "f5", "f6")


def lens_of(cell: Cell) -> str:
    """'type, source, sha256 prefix' from the run's manifest, else from the pins by the run's prefix."""
    if cell.kind in LENS_FREE:
        return "none (lens-free)"
    if cell.kind == "none":
        return "none (no lens)" if cell.why == "no lens" else ""
    exp = {"gate": "lens_gate", "d1": "statement_positions", "d1_formats": "statement_positions",
           "d4": "early_push_where", "rw": "statement_positions", "fitlens": "pointer_fit",
           "removal": "ablate_pilot", "zach_c1": ""}[cell.kind]  # fmt: skip
    name, sha = "", ""
    mp = RESULTS / exp / cell.run / "manifest.json"
    if exp and mp.exists():
        lens = json.loads(mp.read_text()).get("lens")
        if isinstance(lens, list) and len(lens) == 2:
            name, sha = lens
        elif isinstance(lens, dict):
            sha = lens.get("sha256", "")
            name = next((k for k in lens if k != "sha256"), "")
    if not sha:
        target = next((t for p, t in PREFIXES if cell.run.startswith(p)), "qwen3.6-27b")
        t = pins.TARGETS[target]
        name = t.get("frozen_lens", "jpp")
        sha = t.get("frozen_lens_sha256", pins.FROZEN_LENS_SHA256 if target == "qwen3.6-27b" else "")
        if "_jpp_" in cell.run:
            name, sha = "jpp", ""
    kind, source = LENS_KNOWN.get(sha[:8], ("J++" if name == "jpp" else "plain J-lens" if name == "jlens" else name,
                                            "ours" if "_jpp_" in cell.run else "unknown"))  # fmt: skip
    return f"{kind}, {source}, {sha[:8] or 'sha256 not here'}"


# ---------------------------------------------------------------- rows


@dataclass
class Row:
    model: str
    finding: str
    setting: str
    lens: str = ""
    n: int | None = None
    value: float | None = None  # a share or a difference, 0-1 scale
    ci: tuple[float, float] | None = None
    control: str = ""
    verdict: str = "missing"
    rule: str = ""
    commit: str = ""
    path: str = ""
    # grid.md
    role: str = "main"
    run: str = ""
    md_setting: str | None = None  # the grid.md row this csv row fills (None: csv only)
    md_text: str | None = None  # the cell text (key number + n), on the first csv row of an md cell
    unit: str = "%"  # "%" for shares, "pts" for differences
    sources: list[str] = field(default_factory=list)
    status: str = "has-run"
    notes: list[str] = field(default_factory=list)  # grid.md footnotes besides the not-interpretable reason
    # finding 2: the random parts beside the lens part at the verdict's cell (random_parts)
    random_parts: dict[str, dict[str, list]] = field(default_factory=dict)

    @property
    def word(self) -> str:
        w = next(v for v in VERDICTS if self.verdict.startswith(v))
        return w


def r100(x: float) -> int:
    """Percent, rounded as the repo's reports round (f"{:.0f}"), without a "-0"."""
    return int(f"{100 * x:.0f}") + 0


def pct(x: float | None) -> str:
    return "-" if x is None else f"{r100(x)}%"


def pts(x: float | None) -> str:
    return "-" if x is None else f"{r100(x):+d}"


def ci_txt(lo: float, hi: float, unit: str = "%") -> str:
    return f"[{r100(lo):+d}, {r100(hi):+d}]" if unit == "pts" else f"[{r100(lo)}, {r100(hi)}]"


def key(value: float | None, ci: tuple[float, float] | None, n: int | None, unit: str = "%") -> str:
    """'4% [2,9] n=300' (grid.md's cell text)."""
    v = (pts if unit == "pts" else pct)(value)
    c = "" if ci is None else " " + ci_txt(*ci, unit=unit).replace(", ", ",")
    return f"{v}{c}" + ("" if n is None else f" n={n}")


# ---------------------------------------------------------------- evaluators: each returns rows for one cell


def chance_of(cases: dict[str, dict], fam: str, fmt: str | None = None) -> tuple[float, list[int]] | None:
    """Guessing among a scene's listed answers (the asked one and its conf_answers) over the family's items (one
    format's with `fmt`): (the mean of 1 / k, the k's). The draws list 5 (20%), the formats 3 (33%). None: no list
    (open vocabulary, e.g. natural_read's empty conf_answers)."""
    ks = [1 + len(c["conf_answers"]) for c in cases.values()
          if c.get("family") == fam and c.get("conf_answers") and (fmt is None or c.get("format") == fmt)]  # fmt: skip
    return (sum(1 / k for k in ks) / len(ks), sorted(set(ks))) if ks else None


def chance_txt(chance: tuple[float, list[int]] | None) -> str:
    if chance is None:
        return "chance: the cases list no answers"
    return f"chance {pct(chance[0])} ({' or '.join(map(str, chance[1]))} listed answers)"


def ev_late(cell: Cell) -> list[Row]:
    d = RESULTS / "attn_knockout" / cell.run
    rows = jl(d / "rows.jsonl")
    ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
    fam = cell.opts.get("family", "RL")
    res = DF.late_read(rows, ok, fam)
    cases = {c["id"]: c for c in jl(d / "cases.jsonl")} if (d / "cases.jsonl").exists() else {}
    return [late_row(cell, cell.setting, res, rel(d / "rows.jsonl"), chance_of(cases, fam))]


NO_ITEMS = "not testable (competence: no memory -> prompt item the model answers right unedited here)"


def late_row(cell: Cell, setting: str, res: dict, path: str, chance: tuple[float, list[int]] | None) -> Row:
    lk, off = res["lookup"], res["off"]
    if not lk[3]:  # nothing to judge (and nothing to format: the rates are nan)
        return Row(cell.model, cell.finding, setting, n=0, verdict=NO_ITEMS, rule="late-read", path=path,
                   md_setting=setting, md_text="", sources=[path])  # fmt: skip
    where = "every attention layer" if res["layers"] == "attn" else "every layer"
    control = (f"{chance_txt(chance)}; blocked in {where}; the off-path sentence hidden instead keeps {pct(off[0])} "
               f"{ci_txt(off[1], off[2])}")  # fmt: skip
    if "deltanet" in res:
        control += f"; hidden in every DeltaNet layer instead: {pct(res['deltanet'][0])}"
    if res["holds"]:
        verdict = "holds"
    elif not (off[0] >= DF.OFF_MIN and off[1] >= DF.OFF_LO):
        verdict = "not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)"
    elif lk[0] <= DF.LATE_MAX and lk[2] <= DF.LATE_HI:
        verdict = "fails (the DeltaNet layers matter: blocking them instead keeps < 90%)"
    else:
        verdict = "fails (more than 20% right, or the upper bound above 30%)"
    notes = []
    if chance and verdict.startswith("fails") and lk[1] <= chance[0] <= lk[2]:
        notes.append(f"at chance ({pct(lk[0])} {ci_txt(lk[1], lk[2])}, chance {pct(chance[0])})")
    if cell.opts.get("first_draw") and setting == "draw 1":
        notes.append("draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran "
                     "under the older rule); accepted by Dan, 23 Oct")  # fmt: skip
    return Row(cell.model, cell.finding, setting, n=lk[3], value=lk[0], ci=(lk[1], lk[2]), control=control,
               verdict=verdict, rule="late-read", path=path, md_setting=setting,
               md_text=key(lk[0], (lk[1], lk[2]), lk[3]), sources=[path], notes=notes)  # fmt: skip


def parts_row(cell: Cell, setting: str, cl: dict, fam: str, path: str, chance: tuple[float, list[int]] | None) -> Row:
    need = [(fam, s, d) for s in DP.PARTS + DP.SPLIT for d in ("question", "final")]
    if not any(k[0] == fam for k in cl):  # no item of the family answered right: nothing was patched
        return Row(cell.model, cell.finding, setting, n=0, verdict=NO_ITEMS, rule="name-digit", path=path,
                   md_setting=setting, md_text="", sources=[path])  # fmt: skip
    if not all(k in cl for k in need):
        return Row(cell.model, cell.finding, setting, verdict="missing (the run has no leak-robust parts: first "
                   "version)", rule="name-digit", path=path, md_setting=setting, md_text="", sources=[path])  # fmt: skip
    v = DP.verdicts(cl, fam)
    noname, nodigit = cl[(fam, "lookup_noname", "final")], cl[(fam, "lookup_nodigit", "final")]
    # valid-split's control: each off-path part hidden at both places (keyed by both: the question's tokens count too)
    offs = {(s, d): cl[(fam, s, d)]["right"][0] for s in DP.SPLIT[2:] for d in ("question", "final")}
    (low_s, low_d), low = min(offs.items(), key=lambda kv: kv[1])
    q = ("not testable here (the whole sentence hidden from the question's tokens leaves > 70% right)"
         if not v["question_testable"] else "holds" if v["H-name-q-split"] else "fails")  # fmt: skip
    control = (f"the digit left visible (the sentence without its digit hidden): {pct(nodigit['right'][0])} "
               f"{ci_txt(*nodigit['right'][1:])}; off-path parts hidden (needs >= 90% at both places): lowest "
               f"{pct(low)}, the off-path sentence without its {'digit' if 'nodigit' in low_s else 'name'} hidden from "
               f"{WHERE[low_d]}; the question's tokens read the name: {q}; {chance_txt(chance)}")  # fmt: skip
    if not v["valid-split"]:
        verdict = "not interpretable (the off-path control: an off-path sentence's part hidden keeps < 90%)"
    else:
        verdict = "holds" if v["H-digit-final-split"] else "fails"
    r = noname["right"]
    return Row(cell.model, cell.finding, setting, n=noname["n"], value=r[0], ci=(r[1], r[2]), control=control,
               verdict=verdict, rule="name-digit", path=path, md_setting=setting, md_text=key(r[0], (r[1], r[2]), noname["n"]),
               sources=[path])  # fmt: skip


def ev_parts(cell: Cell) -> list[Row]:
    d = RESULTS / "attn_knockout" / cell.run
    cases = {c["id"]: c for c in jl(d / "cases.jsonl")}
    cl = DP.cells(jl(d / "rows.jsonl"), cases)
    return [parts_row(cell, cell.setting, cl, "RL", rel(d / "rows.jsonl"), chance_of(cases, "RL"))]


@functools.cache
def formats_eval(run: str) -> dict:
    """scripts/d2_formats.py main's per-format results, in memory (nothing written)."""
    d = RESULTS / "attn_knockout" / run
    cases = {c["id"]: c for c in jl(d / "cases.jsonl")}
    for c in cases.values():
        c.setdefault("format", c["wording"].split("/")[0])
    rows = jl(d / "rows.jsonl")
    ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
    out = {}
    for fmt in sorted({c["format"] for c in cases.values()}):
        sub = [r for r in rows if cases[r["id"]]["format"] == fmt]
        out[fmt] = {"late_MP": DF.late_read(sub, ok, "MP"), "cells": DP.cells(sub, cases),
                    "chance": chance_of(cases, "MP", fmt)}  # fmt: skip
    return out


FORMAT_SETTING = {"prose": "prose", "table": "table", "json": "JSON"}


def ev_formats(cell: Cell) -> list[Row]:
    d = RESULTS / "attn_knockout" / cell.run
    path = rel(d / "rows.jsonl")
    res = formats_eval(cell.run)
    saved = latest_dir(RESULTS / "d2_formats", cell.run)
    out = []
    for fmt, setting in FORMAT_SETTING.items():
        if fmt not in res:
            out.append(Row(cell.model, cell.finding, setting, verdict=f"missing (no {setting} items in the run)",
                           rule="formats", path=path, md_setting=setting, md_text=""))  # fmt: skip
            continue
        if cell.finding == "f4":
            row = late_row(cell, setting, res[fmt]["late_MP"], path, res[fmt]["chance"])
        else:
            row = parts_row(cell, setting, res[fmt]["cells"], "MP", path, res[fmt]["chance"])
        row.rule = "formats"
        if saved:  # the saved verdict must agree with the recomputation
            sv = json.loads((saved / "verdict.json").read_text())["formats"].get(fmt, {})
            same = (sv.get("late_MP", {}).get("holds") == res[fmt]["late_MP"]["holds"] if cell.finding == "f4"
                    else (sv.get("parts_MP") or {}).get("H-digit-final-split") == (row.word == "holds"))  # fmt: skip
            row.sources.append(rel(saved / "verdict.json"))
            if not same and row.word in ("holds", "fails"):
                row.verdict = f"missing (inconsistent: {rel(saved / 'verdict.json')} disagrees with the recomputation)"
        out.append(row)
    return out


def f5_block(cell: Cell) -> tuple[dict, int, str, str]:
    """(RL family block, layer, source path, how) from the saved verdict, else finding5_confirm's functions."""
    from scripts import finding5_confirm as FC

    level, sentences = cell.opts.get("level"), cell.opts.get("sentences", FC.SENTENCES)
    saved = latest_dir(RESULTS / "finding5_confirm", cell.run, f"_{level}" if level else "")
    if saved:
        v = json.loads((saved / "verdict.json").read_text())
        if v.get("sentences", FC.SENTENCES) == sentences and (cell.opts.get("layer") in (None, v["layer"])):
            return v["families"]["RL"], v["layer"], rel(saved / "verdict.json"), "saved verdict"
    from scripts import pointer_swap as PS

    d = RESULTS / "pointer_swap" / cell.run
    m = json.loads((d / "manifest.json").read_text())
    items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
    rows = FC.select(jl(d / "outcomes.jsonl"), items, level, sentences)
    layer = cell.opts.get("layer") or FC.pick_layer(rows, cell.opts.get("layers") or m["layers"], "RL")[0]
    fams = FC.confirm(rows, layer, sentences)
    return fams["RL"], layer, rel(d / "outcomes.jsonl"), "computed here with finding5_confirm's functions"


def rand_broken(run: str, layer: int | str) -> float | None:
    """Share of memory -> prompt answers a same-size random patch at the last two tokens changes (the Muse specs'
    random-patch control: > 30% means not interpretable)."""
    rows = [o for o in jl(RESULTS / "pointer_swap" / run / "outcomes.jsonl")
            if o["source"] == "rand" and o["family"] == "RL" and o["group"] == "last" and str(o["layer"]) == str(layer)]  # fmt: skip
    return sum(o["role"] != "none" for o in rows) / len(rows) if rows else None


def ev_f5(cell: Cell) -> list[Row]:
    path = rel(RESULTS / "pointer_swap" / cell.run / "outcomes.jsonl")
    try:
        b, layer, path, how = f5_block(cell)
    except AssertionError as e:
        why = str(e)
        word = "not testable" if "before the donor's digit arrives" in why else "missing"
        return [Row(cell.model, cell.finding, f"{cell.setting}, {part}", verdict=f"{word} ({why[:140]})",
                    rule="order-identity", path=path, md_setting=cell.setting if part == "1st-2nd" else None,
                    md_text="", sources=[path]) for part in ("1st-2nd", "3rd on")]  # fmt: skip
    verdict = {"confirms": "holds", "fails": "fails"}.get(b["verdict"], f"fails (partly: A {b['A']}, B {b['B']})")
    if cell.opts.get("rand_gate"):
        broken = rand_broken(cell.run, layer)
        if broken is not None and broken > 0.30:
            verdict = f"not interpretable (the random-patch control breaks {pct(broken)} of answers, above 30%)"
    a, r = b["first2"]["position_minus_identity"], b["rest"]["identity_minus_position"]
    ctl = f"layer {layer} ({how})"
    out = []
    for part, x, n, txt in (("1st-2nd", a, b["first2"]["n"], f"position - identity {pts(a[0])}, A: {b['A']}"),
                            ("3rd on", r, b["rest"]["n"], f"identity - position {pts(r[0])}, B: {b['B']}")):  # fmt: skip
        out.append(Row(cell.model, cell.finding, f"{cell.setting}, {part}", n=n, value=x[0], ci=(x[1], x[2]),
                       control=f"{txt}; {ctl}", verdict=verdict, rule="order-identity", path=path, unit="pts",
                       md_setting=cell.setting if part == "1st-2nd" else None, sources=[path]))  # fmt: skip
    out[0].md_text = f"{pts(a[0])}/{pts(r[0])} n={b['n']}"
    return out


V4X = (("filler moved", "e5-off", "H-order-v4", ("token",)), ("one statement more", "e5more", "H-start-v4",
       ("end", "token")), ("one statement fewer", "e5fewer", "H-start-v4", ("end", "token")))  # fmt: skip
RIVAL = {"token": "the same place in the text", "end": "counted from the end"}


def ev_f6(cell: Cell) -> list[Row]:
    from scripts import pointer_swap as PS

    d = RESULTS / "pointer_swap" / cell.run
    m = json.loads((d / "manifest.json").read_text())
    saved = sorted(p for p in d.glob("analysis-*/summary.json") if json.loads(p.read_text()).get("v4x"))
    if saved:
        v4x, src = json.loads(saved[-1].read_text())["v4x"], rel(saved[-1])
    else:
        v4x = PS.v4x_tests(m, PS.analyze(m, jl(d / "outcomes.jsonl"), jl(d / "checks.jsonl"))["rates"])
        src = rel(d / "outcomes.jsonl") + " (pointer_swap.analyze, computed here)"
    layers = list(PS.primary_layers(m))
    rows = [o for o in jl(d / "outcomes.jsonl") if o["family"] == "RL" and o["group"] == "last" and o["source"] == "dissoc"]  # fmt: skip
    by = collections.defaultdict(list)
    for o in rows:
        by[(o["level"], str(o["layer"]))].append(o)

    def ub(lv: str, la: str) -> float:  # the donor's digit (value) share's Wilson upper bound, the specs' layer rule
        sel = by[(lv, la)]
        return wilson(sum(o["role"] == "value" for o in sel), len(sel))[2] if sel else 1.0

    out = []
    for setting, lv, hyp, rivals in V4X:
        levels = ("e5-off",) if hyp == "H-order-v4" else ("e5more", "e5fewer")
        early = [la for la in layers if all(ub(x, la) < 0.10 for x in levels)]
        decisive = early if cell.opts.get("by_value") else layers
        show = (early or decisive)[-1:] if decisive else []
        path = src
        if not decisive:
            out.append(Row(cell.model, "f6", setting, verdict="not testable (no swept layer before the donor's digit "
                           "arrives)", rule="counting", path=path, md_setting=setting, md_text="", sources=[path]))  # fmt: skip
            continue
        holds = any(v4x[hyp].get(f"layer {la}") for la in decisive)
        c = v4x["cells"].get(f"{lv}|{show[0]}|all")
        if c is None:
            out.append(Row(cell.model, "f6", setting, verdict=f"missing (no {lv} cell at layer {show[0]})",
                           rule="counting", path=path, md_setting=setting, md_text="", sources=[path]))  # fmt: skip
            continue
        verdict = "holds" if holds else "fails"
        if cell.opts.get("rand_gate"):
            broken = rand_broken(cell.run, show[0])
            if broken is not None and broken > 0.30:
                verdict = f"not interpretable (the random-patch control breaks {pct(broken)} of answers, above 30%)"
        w = c["winner"]
        ctl = "; ".join(f"{RIVAL[r]} {pct(c[r][0])} {ci_txt(c[r][1], c[r][2])}" for r in rivals)
        ctl += f"; shown at layer {show[0]}; decisive layers {', '.join(decisive)}"
        notes = (["decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code "
                  "tests every swept layer); accepted by Dan, 23 Oct"] if cell.opts.get("by_value") else [])  # fmt: skip
        out.append(Row(cell.model, "f6", setting, n=c["n"], value=w[0], ci=(w[1], w[2]), control=ctl, verdict=verdict,
                       rule="counting", path=path, md_setting=setting,
                       md_text=f"{pct(w[0])} vs {pct(c[rivals[-1]][0])} n={c['n']}", sources=[path], notes=notes))  # fmt: skip
    return out


def ev_gate(cell: Cell) -> list[Row]:
    p = RESULTS / "lens_gate" / cell.run / "summary.json"
    s = json.loads(p.read_text())
    g = s.get("gate" if cell.opts["gate"] == "v1" else "gate_v2")
    if g is None:
        return [Row(cell.model, "gate", cell.setting, verdict="missing (this run has no gate v2)", path=rel(p),
                    md_setting=cell.setting, md_text="", sources=[rel(p)])]  # fmt: skip
    b, x = g["bridge_top10"], g["x_top10"]
    return [Row(cell.model, "gate", cell.setting, n=g["n"], value=b[0], ci=(b[1], b[2]),
                control=f"the other bridge in the top 10: {pct(x[0])} {ci_txt(x[1], x[2])} (needs <= 20%; the bridge >= 50%)",
                verdict="holds" if g["pass"] else "fails", rule=f"lens-gate-{cell.opts['gate']}", path=rel(p),
                md_setting=cell.setting, md_text=key(b[0], (b[1], b[2]), g["n"]), sources=[rel(p)])]  # fmt: skip


def d1_word(v: str) -> str:
    if v == "replicates":
        return "holds"
    if v == "does not replicate":
        return "fails"
    if v.startswith("not interpretable"):
        return "not interpretable (" + v.split(":", 1)[-1].strip() + ")"
    return f"missing (unknown verdict {v!r})"


# the random parts statement_positions parts patches beside the lens part (d1_verdict reports neither as a rule):
# jspace_matched in every parts run; rand_sub only where a spec asks for it (the 122B late specs)
RANDOM_PARTS = (("jspace_matched", "same-share random part"), ("rand_sub", "random subspace, same share"))


@functools.cache
def parts_rows(path: Path) -> tuple[dict, ...]:
    """A parts run's patched rows of the random parts (outcomes.jsonl: source cf, not the random-direction null)."""
    if not path.exists():  # a verdict without its parts rows here (synthetic tests): nothing beside the lens part
        return ()
    keep = {p for p, _ in RANDOM_PARTS}
    return tuple(r for r in jl(path) if r["source"] == "cf" and not r["null"] and r["part"] in keep)


@functools.cache
def item_formats(manifest: Path) -> dict[str, str]:
    """Item id -> format, from the parts run's tasks set (d1_verdict.load_meta, which the verdict's by_format uses)."""
    from scripts import d1_verdict as DV

    tasks = (json.loads(manifest.read_text()).get("tasks") or {}).get("set")
    return {k: m["format"] for k, m in DV.load_meta(tasks).items()}


def random_parts(run: str, at: dict, fmt: str | None = None) -> dict[str, dict[str, list]]:
    """At the verdict's cell (`at`: its set and layer), each random part with rows: part -> {"lookups" (PP),
    "recalls" (PM)} -> [switched, Wilson lo, hi, n]; switched = role b, as d1_verdict.rate. `fmt`: that format's items
    only (table / json), as the verdict's by_format."""
    d = RESULTS / "statement_positions" / run
    rows = [r for r in parts_rows(d / "outcomes.jsonl") if r["set"] == at["set"] and r["layer"] == at["layer"]]
    if fmt is not None:
        formats = item_formats(d / "manifest.json")
        rows = [r for r in rows if formats.get(r["name"]) == fmt]
    out: dict[str, dict[str, list]] = {}
    for part, _ in RANDOM_PARTS:
        for fam, who in (("PP", "lookups"), ("PM", "recalls")):
            sel = [r for r in rows if r["part"] == part and r["family"] == fam]
            if sel:
                out.setdefault(part, {})[who] = [*wilson(sum(r["role"] == "b" for r in sel), len(sel)), len(sel)]
    return out


def random_parts_text(rp: dict[str, dict[str, list]]) -> str:
    """'same-share random part (jspace_matched): lookups 1% [0, 3] n=180, recalls 2% [1, 5] n=180' (+ rand_sub)."""
    out = []
    for part, name in RANDOM_PARTS:
        if part in rp:
            out.append(f"{name} ({part}): " + ", ".join(f"{who} {pct(x[0])} {ci_txt(x[1], x[2])} n={x[3]}"
                                                         for who, x in rp[part].items()))  # fmt: skip
        elif part == "jspace_matched":
            out.append(f"{name} ({part}): no rows at this cell")
    return "; ".join(out)


def ev_d1(cell: Cell) -> list[Row]:
    saved = latest_dir(RESULTS / "d1_verdict", cell.run)
    if saved is None:
        p = rel(required(cell))
        return [Row(cell.model, "f2", cell.setting, verdict="missing (the parts ran but no saved verdict: "
                    "scripts/d1_verdict.py not run on it)", rule="stated-bridge", path=p, md_setting=cell.setting,
                    md_text="", sources=[p])]  # fmt: skip
    p = rel(saved / "verdict.json")
    v = json.loads((saved / "verdict.json").read_text())
    lk, rc = v["lookup"], v["recall"]

    def row(setting: str, lj: list, ln: list, rj: list, verdict: str, md: str | None, fmt: str | None = None) -> Row:
        ctl = (f"recall, lens-readable part (the control, needs >= 30%): {pct(rj[0])} {ci_txt(rj[1], rj[2])}; "
               f"lookup, the rest (needs >= 50%): {pct(ln[0])}; cell {v['cell']['set']} at layer {v['cell']['layer']}")  # fmt: skip
        if "kept_under_lens_part" in v and md:
            ctl += f"; lookups keep their answer under the lens-part patch: {pct(v['kept_under_lens_part'][0])}"
        rp = random_parts(cell.run, v["cell"], fmt) if md else {}  # beside the lens part, at the verdict's cell
        if md:
            ctl += "; " + random_parts_text(rp)
        return Row(cell.model, "f2", setting, n=lj[3], value=lj[0], ci=(lj[1], lj[2]), control=ctl,
                   verdict=d1_word(verdict), rule="stated-bridge", path=p, md_setting=md,
                   md_text=key(lj[0], (lj[1], lj[2]), lj[3]) if md else None, random_parts=rp,
                   sources=[p, rel(RESULTS / "statement_positions" / cell.run / "outcomes.jsonl")] if md else [p])  # fmt: skip

    if cell.kind == "d1_formats":  # one row per format, its own verdict (format_verdicts); pooled in the control
        out = []
        for fmt, setting in (("table", "table"), ("json", "JSON")):
            c, fv = v.get("by_format", {}).get(fmt), (v.get("format_verdicts") or {}).get(fmt)
            if c is None or fv is None:
                out.append(Row(cell.model, "f2", setting, verdict=f"missing (no {setting} rows in {p})",
                               rule="stated-bridge", path=p, md_setting=setting, md_text="", sources=[p]))  # fmt: skip
                continue
            r = row(setting, c["PP_jspace"], c["PP_not_jspace"], c["PM_jspace"], fv, setting, fmt)
            r.control += f"; pooled over formats: {v['verdict']}"
            out.append(r)
        return out
    out = [row(cell.setting, lk["jspace"], lk["not_jspace"], rc["jspace"], v["verdict"], cell.setting)]
    for t, tv in (v.get("topic_verdicts") or {}).items():
        c = v["by_topic"][t]
        out.append(row(f"{cell.setting} · {t}", c["PP_jspace"], c["PP_not_jspace"], c["PM_jspace"], tv, None))
    return out


def d4_word(v: str) -> str:
    if v.startswith("H-around"):
        return "holds"
    if v.startswith("H-where"):
        return "fails"
    if v.startswith("not valid"):
        return f"not interpretable (the off-path check failed at the decisive cell; reading there: {v[11:-1]})"
    if v.startswith(("no cell", "no valid cell")):
        return "not interpretable (no cell where the lens push writes recall: the positive control fails)"
    if v == "inconclusive":
        return "inconclusive (the rule's reading: the lookup moves between 10% and 30%, or the gap is unclear)"
    return f"missing (unknown verdict {v!r})"


def ev_d4(cell: Cell) -> list[Row]:
    d = RESULTS / "early_push_where" / cell.run
    out = []
    amended = sorted(d.glob("analysis-v2.1-*/summary.json"))
    sfx = cell.opts.get("suffix", "")
    for setting, p in (
        (f"main rule{sfx}", d / "summary.json"),
        (f"amended rule{sfx}", amended[-1] if amended else None),
    ):
        if p is None:
            out.append(Row(cell.model, "f7", setting, verdict="missing (no amended-rule analysis: early_push_where "
                           "analyze --rule v2.1 not run)", rule="push-amended", path=rel(d), md_setting=setting,
                           md_text="", sources=[rel(d)]))  # fmt: skip
            continue
        dec = json.loads(p.read_text())["decision"]
        rule = "push-main" if setting.startswith("main rule") else "push-amended"
        if dec.get("rule") not in ("v2", "v2.1"):
            out.append(Row(cell.model, "f7", setting, verdict=f"missing (the run's rule is {dec.get('rule')}, not v2)",
                           rule=rule, path=rel(p), md_setting=setting, md_text="", sources=[rel(p)]))  # fmt: skip
            continue
        rates, prim = dec.get("rates") or {}, dec.get("primary") or {}
        bl, br = rates.get("BL"), rates.get("BR")
        n = dec.get("n_scenes_paired")
        where = f"{'word' if prim.get('subset') == 'w' else 'sentence'}, layer {prim.get('layer')}, {prim.get('scale', 0):g}x"
        ctl = "" if not br else (f"recall switched {pct(br[0])} {ci_txt(br[1], br[2])}; random push on lookups "
                                 f"{pct(rates['BL_random'][0])}; off-path changed {pct(rates['RL_changed'][0])} / "
                                 f"{pct(rates['RR_changed'][0])}; cell: {where}")  # fmt: skip
        out.append(Row(cell.model, "f7", setting, n=n, value=bl[0] if bl else None, ci=(bl[1], bl[2]) if bl else None,
                       control=ctl, verdict=d4_word(dec["verdict"]), rule=rule, path=rel(p), md_setting=setting,
                       md_text=(f"{pct(bl[0])} vs recall {pct(br[0])} n={n}" if bl and br else ""), sources=[rel(p)]))  # fmt: skip
    return out


def ev_rw(cell: Cell) -> list[Row]:
    p = RESULTS / "statement_positions" / cell.run / "summary.json"
    saved = latest_dir(RESULTS / "d1_verdict", cell.opts["parts"])
    if saved is None:
        return [Row(cell.model, "f8", cell.setting, verdict="missing (no stated-bridge verdict to give the cell)",
                    rule="lens-write", path=rel(p), md_setting=cell.setting, md_text="", sources=[rel(p)])]  # fmt: skip
    s = json.loads(p.read_text())
    st = json.loads((saved / "verdict.json").read_text())["cell"]["set"]
    pp, pm = s["cells"].get(f"PP/{st}/primary"), s["cells"].get(f"PM/{st}/primary")
    if not pp or not pm:
        return [Row(cell.model, "f8", cell.setting, verdict=f"missing (no write cell at {st})", rule="lens-write",
                    path=rel(p), md_setting=cell.setting, md_text="", sources=[rel(p)])]  # fmt: skip
    if pm["verdict"] != "written":
        verdict = f"not interpretable (the lens push does not write recall here: {pm['verdict']}; no positive control)"
    elif pp["verdict"] == "written":
        verdict = "fails"
    elif pp["verdict"] == "not written":
        verdict = "holds"
    else:
        verdict = f"not interpretable (the lookup write is {pp['verdict']} by the rule)"
    x1, r1 = pp["by_scale"].get("x1", {}), pm["by_scale"].get("x1", {})
    v = x1.get("lens_flips")
    ctl = (f"recall written: {pct(r1.get('lens_flips'))} at 1x (random {pct(r1.get('random_flips'))}); lookup at 4x "
           f"{pct(pp['by_scale'].get('x4', {}).get('lens_flips'))} (random {pct(pp['by_scale'].get('x4', {}).get('random_flips'))}); "
           f"set {st}, layers {pp['layers']}; write verdicts: lookup {pp['verdict']}, recall {pm['verdict']}")  # fmt: skip
    return [Row(cell.model, "f8", cell.setting, n=pp["n"], value=v, control=ctl, verdict=verdict, rule="lens-write",
                path=rel(p), md_setting=cell.setting, md_text=f"{pct(v)} vs recall {pct(r1.get('lens_flips'))} n={pp['n']}",
                sources=[rel(p), rel(saved / "verdict.json")])]  # fmt: skip


def ev_fitlens(cell: Cell) -> list[Row]:
    p = RESULTS / "pointer_fit" / cell.run / "summary.json"
    s = json.loads(p.read_text())
    pr = s["primary"]
    lens, slot, rnd = pr["lens"], pr["slot"], pr["random"]
    ctl = (f"the fitted code (slot direction) {pct(slot[0])}; random push {pct(rnd[0])}; layer {pr['layer']}, "
           f"{pr['scale']:g}x; the run's verdict: {s['verdict']}")  # fmt: skip
    return [Row(cell.model, "f8", cell.setting, n=lens[3], value=lens[0], ci=(lens[1], lens[2]), control=ctl,
                verdict="open (no rule for the lens arm)", rule="fitted-code", path=rel(p), md_setting=cell.setting,
                md_text=key(lens[0], (lens[1], lens[2]), lens[3]), sources=[rel(p)])]  # fmt: skip


def ev_zach_c1(cell: Cell) -> list[Row]:
    """Zach's own C1 verdict (scripts/c1_v2.py on his branch), read as it is."""
    path = rel(required(cell))
    src = f"{ZACH_REF}:{path}"
    v = json.loads(zach_file(path) or "{}")
    rule, mid = v.get("rule") or {}, v.get("middle")
    band = ((v.get("bands") or {}).get(mid) or {}).get("paper10") or {}
    n = sum(band[w].get("n", 0) for w in ("PP", "MP", "PM", "MM") if w in band) or None
    gap = rule.get("gap")
    if gap is None:
        verdict = "missing (no whole-question rows at the middle band in Zach's verdict)"
    elif not rule.get("controls_ok"):
        verdict = "not interpretable (Zach's rotated control: a word moves more than 10 points from unedited)"
    else:
        verdict = "holds" if rule.get("C1_graded_holds") else "fails"
    ctl = (f"Zach's rule: memory-final words lose >= 30 points more than prompt-final ones under the top-10 lens "
           f"knock-out at the middle band ({mid}); rotated controls within 10 points: {rule.get('controls_ok')}; "
           f"the strict C1 rule (reported by Zach): {rule.get('strict_C1_holds')}")  # fmt: skip
    return [Row(cell.model, "f1", cell.setting, n=n, value=gap, control=ctl, verdict=verdict, rule="zach-c1", path=src,
                unit="pts", md_setting=cell.setting, md_text=f"{pts(gap)} pts" + ("" if n is None else f" n={n}"),
                sources=[src])]  # fmt: skip


REMOVAL = (("lookup, bridge stated", "BL"), ("lookup, bridge recalled", "RL"), ("recall, bridge stated", "BR"),
           ("recall, bridge recalled", "RR"))  # fmt: skip


G2_MIN = 0.90  # the specs' gate G2: the control removals keep >= 90% on every family / step


def g2(fams: dict) -> tuple[bool | None, list[str], bool]:
    """(G2 passes, the family/steps where a control removal keeps < 90%, the random-dictionary control ran). None:
    no control removal in the summary. The rotated control alone where the random one was dropped (--no-random)."""
    has_random = any("random" in f["accuracy"] for f in fams.values())
    if not any("rotated" in f["accuracy"] or "random" in f["accuracy"] for f in fams.values()):
        return None, [], has_random
    low = [f"{k} ({c} {pct(f['accuracy'][c])})" for k, f in fams.items() for c in ("rotated", "random")
           if c in f["accuracy"] and f["accuracy"][c] < G2_MIN]  # fmt: skip
    return not low, low, has_random


GAP_BOOT, GAP_SEED = 4000, 0


@functools.cache
def suite_entities() -> dict[tuple[str, str], str]:
    """(family, item id) -> the bridge entity of the animal suite's items (wording A, as ablate_pilot's prompts)."""
    from scripts import suite_v1 as S

    return {(fam, it["id"]): it["bridge"] for fam in ("BL", "BR", "RL", "RR") for it in S.load(fam, "A")}


def gap_ci(look: list[tuple[float, str]], rec: list[tuple[float, str]]) -> tuple[float, float, float]:
    """(mean(look) - mean(rec), 2.5th, 97.5th percentile): an unpaired bootstrap over entities, stats.
    cluster_bootstrap's resampling (whole entities with replacement, each group keeping its number of entities)
    applied to each group, on the difference of the two groups' item means. look / rec: (value, entity) per item."""
    rng = np.random.default_rng(GAP_SEED)

    def means(vals: list[tuple[float, str]]) -> np.ndarray:
        by: dict[str, list[float]] = {}
        for v, e in vals:
            s = by.setdefault(e, [0.0, 0.0])
            s[0] += v
            s[1] += 1
        keys = sorted(by)
        sums, cnt = np.array([by[k][0] for k in keys]), np.array([by[k][1] for k in keys])
        pick = rng.integers(0, len(keys), size=(GAP_BOOT, len(keys)))
        return sums[pick].sum(1) / cnt[pick].sum(1)

    lo, hi = np.quantile(means(look) - means(rec), [0.025, 0.975])
    point = sum(v for v, _ in look) / len(look) - sum(v for v, _ in rec) / len(rec)
    return point, float(lo), float(hi)


def ev_removal(cell: Cell) -> list[Row]:
    d = RESULTS / "ablate_pilot" / cell.run
    p = d / "summary.json"
    fams = json.loads(p.read_text())["families"]
    ok, low, has_random = g2(fams)
    acc_of = {fam: fams[f"{fam}/clean"]["accuracy"]["jspace"] for _, fam in REMOVAL if f"{fam}/clean" in fams}
    ents = suite_entities()
    items = [(r["family"], float(r["correct"]), ents.get((r["family"], r["id"]))) for r in jl(d / "rows.jsonl")
             if r["kind"] == "clean" and r["condition"] == "jspace" and r["family"] in ("BL", "RL", "BR", "RR")]  # fmt: skip
    look = [(v, e) for f, v, e in items if f in ("BL", "RL") and e]
    rec = [(v, e) for f, v, e in items if f in ("BR", "RR") and e]
    gap = gap_ci(look, rec) if look and rec and len(look) + len(rec) == len(items) else None
    g2_txt = ("G2 not readable (no control removal)" if ok is None else "G2 passes" if ok else
              f"G2 fails: {', '.join(low[:4])}")  # fmt: skip
    norandom = "" if has_random else "; no random-dictionary control (G2 reads the rotated control alone)"
    if cell.opts.get("g2") and ok is False:
        verdict = f"not interpretable (G2: a control removal keeps < 90% on {', '.join(low[:4])})"
    else:
        verdict = "open (descriptive, no committed rule)"
    ctl = (f"recall right {'/'.join(pct(acc_of[f]) for f in ('BR', 'RR') if f in acc_of)}, lookups "
           f"{'/'.join(pct(acc_of[f]) for f in ('BL', 'RL') if f in acc_of)} with the J-space removed; "
           f"{g2_txt if cell.opts.get('g2') else g2_txt + ' (no G2 in this run: reported)'}{norandom}")  # fmt: skip
    if gap is None:
        ctl += "; no interval: an item's bridge entity was not found"
    out = [Row(cell.model, "f1", cell.setting, n=len(items) or None, value=gap[0] if gap else None,
               ci=(gap[1], gap[2]) if gap else None, control=ctl, rule="removal", path=rel(p), verdict=verdict,
               unit="pts", md_setting=cell.setting, sources=[rel(p), rel(d / "rows.jsonl")])]  # fmt: skip
    out[0].md_text = (f"gap {key(gap[0] if gap else None, (gap[1], gap[2]) if gap else None, len(items), 'pts')}"
                      + ("" if has_random else ", no random-dictionary control"))  # fmt: skip
    for name, fam in REMOVAL:
        f = fams.get(f"{fam}/clean")
        if not f:
            continue
        acc, n = f["accuracy"], f["n"]
        lo, hi = wilson(round(acc["jspace"] * n), n)[1:]
        c = "; ".join(f"{w} removed instead: {pct(acc[k])}" for k, w in (("rotated", "the J-space fit rotated"),
                      ("random", "a random dictionary")) if k in acc)  # fmt: skip
        out.append(Row(cell.model, "f1", f"{cell.setting} · {name}", n=n, value=acc["jspace"], ci=(lo, hi),
                       control=f"{c}; unedited: {pct(acc.get('none'))}{norandom}", rule="removal", path=rel(p),
                       verdict=verdict, sources=[rel(p)]))  # fmt: skip
    return out


EVAL = {"late": ev_late, "parts": ev_parts, "formats_f3": ev_formats, "formats_f4": ev_formats, "f5": ev_f5,
        "f6": ev_f6, "gate": ev_gate, "d1": ev_d1, "d1_formats": ev_d1, "d4": ev_d4, "rw": ev_rw,
        "fitlens": ev_fitlens, "removal": ev_removal, "zach_c1": ev_zach_c1}  # fmt: skip
EXPAND = {  # the grid cells one run fills (several settings)
    "formats_f3": ("prose", "table", "JSON"), "formats_f4": ("prose", "table", "JSON"), "d1_formats": ("table", "JSON"),
    "f6": ("filler moved", "one statement more", "one statement fewer"),
}  # fmt: skip


# ---------------------------------------------------------------- the build


def selected(cell: Cell, patterns: list[str] | None) -> bool:
    if not patterns:
        return True
    name = f"{cell.model}:{cell.finding}:{cell.setting}"
    return any(fnmatch.fnmatch(name, p if p.count(":") >= 2 else p + ":*") for p in patterns)


def settings_of(cell: Cell) -> tuple[str, ...]:
    if cell.kind == "d4":
        sfx = cell.opts.get("suffix", "")
        return (f"main rule{sfx}", f"amended rule{sfx}")
    return EXPAND.get(cell.kind, (cell.setting,))


def empty_rows(cell: Cell, verdict: str, status: str, jobs: Jobs | None) -> list[Row]:
    out = []
    for s in settings_of(cell):
        out.append(Row(cell.model, cell.finding, s, lens=lens_of(cell) if cell.kind != "none" or cell.why else "",
                       verdict=verdict, commit=jobs.commit(cell) if jobs and cell.jobs else "-",
                       path=rel(required(cell)) if cell.kind != "none" else "", role=cell.role, run=cell.run,
                       md_setting=s, md_text="", status=status))  # fmt: skip
    return out


def build(patterns: list[str] | None = None, values: bool = True, runs: set[str] | None = None) -> list[Row]:
    """Every selected cell's rows. `runs`: only cells whose run is in it (tests: README-opened runs)."""
    jobs = Jobs()
    rows: list[Row] = []
    for cell in _cells():
        if not selected(cell, patterns) or (runs is not None and cell.run not in runs):
            continue
        if cell.kind == "none":
            word = "not testable" if cell.why == "no lens" else "missing"
            rows += empty_rows(cell, f"{word} ({cell.why})", cell.why, jobs)
            continue
        cell.jobs = jobs.jobs_of(cell)
        if cell.kind == "f5" and "layer" not in cell.opts:
            cell.opts["layers"] = jobs.f5_layers(cell.run, cell.opts.get("level"))
        if cell.kind == "zach_c1" and not present(cell):
            got = empty_rows(cell, "missing (no verdict file on Zach's branch)", "not on Zach's branch", jobs)
        elif not present(cell):
            st, why = jobs.status(cell.jobs, values)
            word = "not testable" if st == "not testable" else "missing"
            got = empty_rows(cell, f"{word} ({why})", st, jobs)
        elif not values:
            got = empty_rows(cell, "", "has-run", jobs)
        else:
            try:
                got = EVAL[cell.kind](cell)
            except Exception as e:  # one unreadable run is a missing cell, listed, never a crash of the whole grid
                why = f"{type(e).__name__}: {e}"[:160]
                got = [Row(cell.model, cell.finding, s, verdict=f"missing (files inconsistent: {why})",
                           path=rel(required(cell)), md_setting=s, md_text="") for s in settings_of(cell)]  # fmt: skip
            for r in got:
                r.lens, r.commit, r.role, r.run = lens_of(cell), jobs.commit(cell), cell.role, cell.run
                assert r.word in VERDICTS, r.verdict
        notes = jobs.deviations(cell.jobs)  # by spec: the note stands whether or not the run is here
        for r in got:
            r.notes += notes
        rows += got
    return rows


# ---------------------------------------------------------------- outputs


def csv_text(rows: list[Row]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS)
    for r in rows:
        unit = r.unit
        val = "" if r.value is None else f"{100 * r.value:.1f}"
        ci = "" if r.ci is None else f"[{100 * r.ci[0]:.1f}, {100 * r.ci[1]:.1f}]"
        lens = r.lens + ("" if r.role == "main" else f" ({r.role}, listed beside)")
        w.writerow([MODEL[r.model].label, FINDING[r.finding].name, r.setting, lens, "" if r.n is None else r.n,
                    val + ("" if not val else " pts" if unit == "pts" else " %"), ci, r.control, r.verdict, r.rule,
                    r.commit, r.path])  # fmt: skip
    return buf.getvalue()


def md_cell(rows: list[Row]) -> tuple[str, list[tuple[str, str]]]:
    """grid.md text for one (finding, md setting, model): the main cell, then the cells listed beside it; with the
    footnotes the not-interpretable ones need."""
    parts, notes = [], []
    for r in sorted(rows, key=lambda r: r.role != "main"):
        sym = SYMBOL[r.word]
        if r.word in ("missing", "not testable"):
            reason = r.verdict[len(r.word) :].strip(" ()")
            short = ("no spec" if reason.startswith("no spec") else "no lens" if reason == "no lens" else
                     "failed" if " failed at the " in reason else "pending" if "pending in the queue" in reason else
                     "running" if "running in the queue" in reason else "blocked" if " waits on " in reason else
                     "not run" if "not run" in reason else "gate failed" if "gate v1 failed" in reason else
                     "too few scenes" if "stopped by the precheck" in reason and "gate v1 passed" in reason else
                     "precheck stop" if "stopped by the precheck" in reason else
                     reason.split(" where ")[0] if reason.startswith("no layer from ") else
                     "raw smoke mismatch" if "raw smoke mismatch" in reason else
                     "not on Zach's branch" if "Zach's branch" in reason else
                     "no early layer" if "before the donor's digit" in reason else
                     "no item right" if reason.startswith("competence") else "see csv")  # fmt: skip
            text = f"{sym} {r.word}: {short}" if r.md_text == "" or r.md_text is None else f"{sym} {r.md_text}"
        else:
            text = f"{sym} {r.md_text}"
        where = f"{MODEL[r.model].label}, {FINDING[r.finding].name}, {r.md_setting}" + (
            "" if r.role == "main" else f" ({r.role})"
        )
        for note in ([r.verdict] if r.word == "not interpretable" else []) + r.notes:
            notes.append((where, note))
            text += " [{n}]"
        parts.append(text if r.role == "main" else f"{r.role}: {text}")
    return "<br>".join(parts), notes


def lens_block(rows: list[Row]) -> list[str]:
    table = sorted((RESULTS / "lens_table").glob("*/table.json"))
    lt = json.loads(table[-1].read_text())["rows"] if table else []

    def score(model: str, lens: str) -> str:
        r = next((x for x in lt if x["model"] == model and x["lens"] == lens), None)
        if not r:
            return "-"
        if r.get("macro") is None:
            return r.get("status", "-")
        d = r.get("d_logit")
        # a lens graded in its own run (our J++ fits) is compared with the logit lens on the items both runs kept
        shared = f", on the {r['shared_items']} items both runs kept" if r.get("shared_items") else ""
        return f"{r['macro']:.2f}" + ("" if d is None else f" ({d:+.2f} vs the logit lens{shared})")

    def recipe(model: str, lens: str) -> str:
        r = next((x for x in lt if x["model"] == model and x["lens"] == lens), None)
        return r["recipe"] if r else "-"

    def gate(m: str, role: str, v: str) -> str:
        g = [r for r in rows if r.model == m and r.finding == "gate" and r.role == role and r.setting.startswith(v)]
        return (SYMBOL[g[0].word] + " " + (g[0].md_text or g[0].word)) if g else "-"

    lines = ["## Lens", "",
             f"Lens quality: pass@10 (macro) on the J++ recipe's held-out readout evals, minus the logit lens on the "
             f"same items and layers ({rel(table[-1]) if table else 'results/lens_table: none'}). Gates: the bridge "
             "in the lens's top 10 at its own sentence (v1) or after its word (v2), share of items.", "",
             "| Model | Lens | Source, sha256 | Recipe (prompts) | pass@10 | Gate v1 | Gate v2 | Listed beside |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in MODELS:
        if m.key == "olmo_hybrid":
            lines.append(f"| {m.label} | none | - | - | - | ⊘ no lens | ⊘ no lens | - |")
            continue
        mains = [r for r in rows if r.model == m.key and r.finding == "gate" and r.role == "main"]
        lens = mains[0].lens if mains else "-"
        kind, _, rest = lens.partition(", ")
        beside = []
        for role in sorted({r.role for r in rows if r.model == m.key and r.finding == "gate" and r.role != "main"}):
            other = next(r for r in rows if r.model == m.key and r.finding == "gate" and r.role == role)
            sc = score(m.lens_rows[0], m.lens_rows[2]) if m.lens_rows[2] else "-"
            beside.append(f"{role} ({other.lens}): v1 {gate(m.key, role, 'v1')}, v2 {gate(m.key, role, 'v2')}, "
                          f"pass@10 {sc}")  # fmt: skip
        lines.append(f"| {m.label} | {kind} | {rest} | {recipe(m.lens_rows[0], m.lens_rows[1])} | "
                     f"{score(m.lens_rows[0], m.lens_rows[1])} | {gate(m.key, 'main', 'v1')} | {gate(m.key, 'main', 'v2')} | "
                     f"{'<br>'.join(beside) or '-'} |")  # fmt: skip
    return [*lines, ""]


KEY_CELLS = (
    ("27b", "f4", "long context"), ("32b", "f6", "filler moved"), ("olmo_hybrid", "f3", "draw 2"),
    ("olmo_hybrid", "f4", "draw 2"), ("olmo_hybrid", "f5", "draw 1"), ("olmo_hybrid", "f5", "draw 2"),
    ("olmo_hybrid", "f6", "filler moved"),
    ("olmo", "f7", "main rule"), ("32b", "gate", "v1 (at the word)"), ("32b", "gate", "v2 (after the word)"),
    ("olmo", "gate", "v1 (at the word)"), ("olmo", "gate", "v2 (after the word)"), ("gemma", "gate", "v1 (at the word)"),
    ("gemma", "gate", "v2 (after the word)"), ("muse", "gate", "v1 (at the word)"), ("muse", "gate", "v2 (after the word)"),
    ("32b", "f2", "draw 1"), ("olmo", "f2", "draw 2"), ("gemma", "f2", "draw 2"), ("muse", "f2", "draw 2"),
)  # fmt: skip


def grid_md(rows: list[Row], meta: dict) -> str:
    cells: dict[tuple, list[Row]] = collections.defaultdict(list)
    for r in rows:
        if r.md_setting is not None:
            cells[(r.finding, r.md_setting, r.model)].append(r)
    notes: list[tuple[str, str]] = []
    done: dict[tuple, str] = {}

    def text(k: tuple) -> str:  # once per cell, so that a footnote is numbered once
        if k not in cells:
            return ""
        if k not in done:
            t, ns = md_cell(cells[k])
            for n in ns:
                notes.append(n)
                t = t.replace("[{n}]", f"[{len(notes)}]", 1)
            done[k] = t
        return done[k]

    head = ["# Every finding on every model", "",
            f"Built by scripts/cross_model_grid.py at {meta['git']} ({meta['written_utc']}) from the saved results; "
            "each cell is judged by the rule committed with its run (rule ids in the mapping table below). Nothing here "
            "is human-verified. Long format with every number: grid.csv; the files behind each cell: sources.txt.", "",
            "Cell: verdict, key number [95% CI], n. ✓ holds · ✗ fails · ≈ inconclusive (the rule itself says so; no "
            "control failed) · ⚠ not interpretable (a control failed; footnote) · ⊘ not testable (no lens, the gate or "
            "competence failed) · · missing (did not run, failed, or no saved verdict) · ○ open (values shown, no "
            "committed rule: descriptive). A second line lists a run with another lens (plain J-lens, base-model J++) or "
            "another run beside the main one. Numbered footnotes: failed controls and the cell-level notes.", "",
            "Finding 1: \"no random-dictionary control\" marks the removal runs that dropped it (Qwen3-32B, Gemma 4, "
            "Muse: too large next to the model on an 80 GB GPU); their gate G2 reads the rotated control alone.", "",
            GAP_METHOD, ""]  # fmt: skip
    key_lines = ["## Key cells", ""]
    for m, f, s in KEY_CELLS:
        key_lines.append(f"- {MODEL[m].label}, {FINDING[f].name} ({s}): {text((f, s, m)) or 'no cell'}")
    key_lines.append("")
    models = [m for m in MODELS]
    tab = ["## The grid", "",
           "| # | Finding | Setting | " + " | ".join(m.label for m in models) + " |",
           "|---|---|---|" + "---|" * len(models)]  # fmt: skip
    for f in FINDINGS:
        if f.key == "gate":
            continue
        for s in f.settings:
            if not any((f.key, s, m.key) in cells for m in models):
                continue
            tab.append(f"| {f.number} | {f.name} | {s} | " + " | ".join(text((f.key, s, m.key)) for m in models) + " |")
    what = ["", "What the key numbers are, by finding:", "",
            "- 1: tasks, Zach's rule: points, memory-final minus prompt-final loss under the lens knock-out (his "
            "verdict); animal suite: points, lookups minus recalls right with the J-space removed [unpaired bootstrap "
            "over bridge entities], descriptive.",
            "- 2: % of lookups the lens-readable part of a stated bridge's change switches.",
            "- 3: % right with the sentence without its name hidden from the last tokens (the digit hidden too).",
            "- 4: % right with the answer's sentence hidden from the last tokens (chance: 20% in the draws, five "
            "listed answers; 33% in prose / table / JSON, three).",
            "- 5: points, position - identity for the 1st-2nd asked sentence / identity - position from the 3rd on.",
            "- 6: % of patched answers at the same order in the list vs at the same place in the text (or from the end).",
            "- 7: % of lookups vs recalls the lens push switches at the rule's cell.",
            "- 8: % of lookups vs recalls the lens push writes (1x) at the stated bridge's cell; last tokens: % of "
            "lookups the lens push moves in the fitted-code test.", ""]  # fmt: skip
    foot = ["## Footnotes", ""] + [f"{i}. {w}: {v}" for i, (w, v) in enumerate(notes, 1)] + [""]
    choices = ["## Choices made after seeing the data", ""] + [f"- {c}" for c in CHOICES] + [""]
    mapping = ["## Mapping: names, internal codes, scripts, rules", "",
               "| # | Finding | Internal codes | Scripts | Rule ids |", "|---|---|---|---|---|"]  # fmt: skip
    for f in FINDINGS:
        ids = sorted({r.rule for r in rows if r.finding == f.key and r.rule})
        mapping.append(f"| {f.number} | {f.name} | {f.codes} | {f.scripts} | {', '.join(ids) or '-'} |")
    mapping += ["", "| Rule id | Rule |", "|---|---|"] + [f"| {k} | {v} |" for k, v in RULES.items()] + [""]
    body = [*head, *key_lines, *lens_block(rows), *tab, *what, *foot, *choices, *mapping]
    return "\n".join(body)


def status_outputs(rows: list[Row]) -> tuple[str, str]:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(("model", "finding", "setting", "lens role", "run", "status", "spec commit", "result path"))
    for r in rows:
        w.writerow(
            (MODEL[r.model].label, FINDING[r.finding].name, r.setting, r.role, r.run, r.status, r.commit, r.path)
        )
    counts = collections.Counter(r.status for r in rows)
    md = ["# Cell status (no values)", "", "| status | cells |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in sorted(counts.items())] + [""]
    return buf.getvalue(), "\n".join(md)


def git_head() -> str:
    p = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                       check=False)  # fmt: skip
    dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True, check=False).stdout.strip()  # fmt: skip
    return p.stdout.strip() + (" (uncommitted changes)" if dirty else "")


def write(rows: list[Row], out_root: Path, values: bool) -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d = out_root / stamp
    d.mkdir(parents=True, exist_ok=False)
    meta = {"written_utc": stamp, "git": git_head(), "script": "scripts/cross_model_grid.py", "values": values}
    if not values:
        c, md = status_outputs(rows)
        (d / "status.csv").write_text(c)
        (d / "status.md").write_text(md)
        return d
    (d / "grid.csv").write_text(csv_text(rows))
    (d / "grid.md").write_text(grid_md(rows, meta))
    (d / "grid.json").write_text(json.dumps({"meta": meta, "rules": RULES, "rows": [r.__dict__ for r in rows]},
                                            indent=1, default=str) + "\n")  # fmt: skip
    src = [f"{MODEL[r.model].label} | {FINDING[r.finding].name} | {r.setting} | {r.role} | {r.run or '-'} | "
           f"{'; '.join(r.sources) or r.path or '-'}" for r in rows]  # fmt: skip
    (d / "sources.txt").write_text("\n".join(src) + "\n")
    return d


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cells", default=None, help="model:finding[:setting] glob patterns, comma-separated")
    ap.add_argument("--no-values", action="store_true", help="status only; no result file is opened")
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new grid folder")
    a = ap.parse_args(argv)
    patterns = [p.strip() for p in a.cells.split(",")] if a.cells else None
    rows = build(patterns, values=not a.no_values)
    d = write(rows, Path(a.out), values=not a.no_values)
    if a.no_values:
        print("cells by status:", dict(collections.Counter(r.status for r in rows)))
    else:
        print(f"{len(rows)} rows")
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
