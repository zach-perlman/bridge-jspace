"""x53_lastconflict (batch 53, test 53.3; jobs/c3/batch53.yaml, the rule fixed in Dan's brief of 29 Oct 09:30 before any
run; no prediction): the conflict test at the last token.

Items: 51.10's (x51_jread.select: the main test's items of the target's X0 run at L, x47_cumulative.select, with P1 / P2
/ P3 per reader), restricted to 49.1's locker-first items as 51.10's write arms; the source run's gate (X0's: 0.80 per
reader on O unedited, >= 150 eligible) asserted. Both readers (lookup PP, recall PM), X0's chat read (the prompt with a
digit's space token appended); P3 = the last token, the appended space (whose next token is the answer).

Layers, per reader: 51.10's read-peak layer (results/x51_jread/<51.10 run>/peak.json) and the answer layer minus 2 (the
answer layer = 51.10's read: per reader the lower median over the locker-first items of the layer from which O's answer
is the logit lens's top token at P3; results/x51_jread/read-<run>-*/read.json, the newest).

The change: Δ = h_S - h_O at P3 at the layer (each reader's own S and O prompts; the readers' prompts differ at P3). The
lens part P_J Δ = its 25 J++ atoms (X0's signed OMP over the letter-token J++ dictionary at the layer, x49_gain.
lens_parts); the random part R Δ = X0's random subspace part at the lens part's share (seed 888 + layer). Arms, each
added at P3 at the layer on O (AddRows), each read: none; whole (Δ); no_jpp ("without the lens part": Δ - P_J Δ);
no_rand ("without a random part of the same share": Δ - R Δ); jpp ("the lens part alone": P_J Δ); rest ("the rest
alone": Δ - P_J Δ, the same vector as no_jpp in this additive patch, read separately and reported under the brief's
name). Switch = the top token over the vocabulary is S's answer's first token.

Rule per reader and layer (Dan's brief, batch 53.3): "computes outside the lens at the last token" if the loss without
the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss
is >= 0.30 beyond random; else "in between". As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) /
S_whole (S_arm = the share of the items switched under the arm); the rest alone's share = S_rest / S_whole; point
estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs over the original bridge entities (10,000, seed 0, paired:
the same draws for every arm) beside; S_whole = 0: "not tested (the whole change switches no item)". X0's validity bar
(S_whole >= 0.30 and >= 30 switches) reported beside, not in the rule.

No prediction, not sealed: the run writes the reads; `verdict` (CPU) writes results/x53_lastconflict/x53_lastconflict-
<UTC>/ (verdict.md, verdict.json, a figure, examples.md: 10 random items, seed 0). UNVERIFIED.

BJ_TARGET=qwen3.5-9b uv run python scripts/x53_lastconflict.py plan                       # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_lastconflict.py run --name qwen35_9b_x53_3 # GPU
uv run python scripts/x53_lastconflict.py verdict --runs qwen35_9b_x53_3                  # CPU
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x49_gain as G
from scripts import x51_jread as JR

EXP = "x53_lastconflict"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
TEST = "53.3"
NO_PREDICTION = "no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)"
SOURCE_RUNS = {**JR.RUNS, **JR.COVERAGE_RUNS}  # 51.10's runs: the read peak and the answer layer
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_3", "qwen3.6-27b": "x53_3_27b", "muse-glimmer-30b": "muse30_x53_3",
        "nemotron-3.5-lightning": "nem35l_x53_3"}  # fmt: skip
# batch 53.3b's check (Dan 10:05): 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3
MODES = ("53.3", "ans13")
RUNS_ANS13 = {"qwen3.5-9b": "qwen35_9b_x53_3l", "qwen3.6-27b": "x53_3l_27b", "muse-glimmer-30b": "muse30_x53_3l",
              "nemotron-3.5-lightning": "nem35l_x53_3l"}  # fmt: skip
READERS, READER_NAME = X.READERS, JR.READER_NAME
RENDERING = G.RENDERING
K = X.K_MAIN  # 25
ARMS = ("none", "whole", "no_jpp", "no_rand", "jpp", "rest")
ARM_TEXT = {"none": "O unedited", "whole": "the whole change Δ = h_S - h_O at P3",
            "no_jpp": "without the lens part: Δ - P_J Δ", "no_rand": "without a random part of the same share: Δ - R Δ",
            "jpp": "the lens part alone: P_J Δ", "rest": "the rest alone: Δ - P_J Δ (the same vector as no_jpp)"}  # fmt: skip
OUTSIDE_MAX, REST_MIN, THROUGH_MIN = 0.10, 0.7, 0.30
EPS = 1e-9
LABELS = {"outside": "computes outside the lens at the last token", "through": "through the lens",
          "between": "in between", "untested": "not tested (the whole change switches no item)"}  # fmt: skip
RULE = (f"per reader and layer: \"{LABELS['outside']}\" if the loss without the lens part is <= 0.10 beyond random and "
        f"the rest alone switches >= 0.7 of the whole; \"{LABELS['through']}\" if the loss is >= 0.30 beyond random; "
        f"else \"{LABELS['between']}\"")  # fmt: skip
# 53.3b (Dan 10:05, jobs/c3/batch53.yaml test_53_3b): the same test on word answers, Zach's named-bridge passages
TEST_WORDS = "53.3b"
WORD_SOURCE = {"qwen3.5-9b": "qwen35_9b_x52_z1p", "qwen3.6-27b": "x52_z1p_27b",
               "nemotron-3.5-lightning": "nem35l_x52_z1p",
               "muse-glimmer-30b": "muse30_x53_z1p"}  # Z1-P's runs (x50_zach --part z1p): the chosen passages  # fmt: skip
WORD_RUNS = {"qwen3.5-9b": "qwen35_9b_x53_3b", "qwen3.6-27b": "x53_3b_27b", "muse-glimmer-30b": "muse30_x53_3b",
             "nemotron-3.5-lightning": "nem35l_x53_3b"}  # fmt: skip
WORD_SLOTS = {"K": X.LOOKUP, "M": X.RECALL}  # Z1-P's reader slots: K = the PP passage (the lookup), M = PM (the recall)
WORD_SET, WORD_SET_V21 = (
    "jsuite_v2_test_chat",
    "jsuite_v2_1_test_chat",
)  # the brief's set: v2.1 keeps v2's PP / PM items
ARMS_WORDS = ("none", "whole", "no_jpp", "no_rand", "jpp")  # 53.3's arms without the redundant "rest alone"
WORD_OFFSETS = (1, 2, 3)  # the reader's own answer layer minus 1, 2, 3 (and 51.10's read peak)
ACROSS_OFFSETS, ACROSS_MIN, N_MODELS_WORDS = (1, 2), 3, 4
RULE_WORDS = ("\"copy bypasses the lens\" if at answer - 1 and - 2 the recall is \"through the lens\" and the lookup "
              "\"outside\" on >= 3 of 4 models; \"digits only\" if on words the lookup goes through the lens like the "
              "recall; else in between")  # fmt: skip
AS_COMPUTED_WORDS = ("53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, "
                     "the same vector); a cell under 53.3's validity bar is \"invalid\" and counts for neither clause; per "
                     "model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; \"digits "
                     "only\" read as the lookup and the recall both \"through the lens\" at both layers, on >= 3 of 4 "
                     "models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's "
                     "settle rule: the layer from which O's answer token stays top through the last layer, the lower "
                     "median over the passages); a layer without a J++ map is dropped and named")  # fmt: skip
AS_COMPUTED = ("the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / "
               "S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); "
               "point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities "
               f"({X.N_BOOT}, seed {X.BOOT_SEED}, paired) beside; S_whole = 0: not tested")  # fmt: skip


# ---- layers and items (CPU) ---------------------------------------------------------------------------------------


def layers_of(target: str, mode: str = "53.3") -> dict[str, Any]:
    """Per reader: 51.10's read-peak layer and its answer layer minus 2 (deduplicated, in order), with their sources.
    mode "ans13" (batch 53.3b's check on the locker scenes): the lookup alone, at its answer layer minus 1 and minus 3."""
    assert mode in MODES, f"mode {mode!r}, not one of {MODES}"
    run = SOURCE_RUNS[target]
    peak_file = JR.RESULTS / run / "peak.json"
    peaks = json.loads(peak_file.read_text())["peaks"]
    found = sorted(JR.RESULTS.glob(f"read-{run}-*/read.json"))
    assert found, f"no 51.10 read of {run} (results/x51_jread/read-{run}-*/read.json)"
    answer = json.loads(found[-1].read_text())["answer"]
    out: dict[str, Any] = {"source_run": run, "peak_file": str(peak_file.relative_to(pins.REPO_ROOT)),
                           "read_file": str(found[-1].relative_to(pins.REPO_ROOT)), "mode": mode, "readers": {}}  # fmt: skip
    for w in READERS if mode == "53.3" else (X.LOOKUP,):
        name = READER_NAME[w]
        peak, ans = peaks[name], answer[name]["layer"]
        assert peak is not None, f"{run}: {name} has no read peak"
        assert ans is not None, f"{run}: {name} has no answer layer"
        offsets = (int(ans) - 2,) if mode == "53.3" else (int(ans) - 1, int(ans) - 3)
        layers = list(dict.fromkeys((int(peak), *offsets) if mode == "53.3" else offsets))
        out["readers"][name] = {"peak": int(peak), "answer": int(ans), "layers": layers}
    return out


def select(tok, target: str) -> tuple[list[dict], dict]:
    """51.10's items (x51_jread.select) restricted to 49.1's locker-first ones (51.10's write arms)."""
    items, counts = JR.select(tok, target)
    lf = [it for it in items if it["lf"]]
    return lf, {**counts, "items_used": len(lf), "entities_used": len({it["entity"] for it in lf})}


def n_reads(lay: dict[str, Any]) -> int:
    """Reads per item: per reader O unedited plus every arm at each of its layers."""
    return sum(1 + len(r["layers"]) * (len(ARMS) - 1) for r in lay["readers"].values())


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    lay = layers_of(target)
    items, counts = select(tok, target)
    blob = {"target": target, "run": RUNS[target], "layers": lay, "counts": counts,
            "gate": G.source_gate(G.SOURCES[target]), "reads": len(items) * n_reads(lay),
            "forwards_states": len(items) * 2 * 2}  # fmt: skip
    print(json.dumps(blob, indent=1))
    return blob


# ---- the parts and the run (GPU) ----------------------------------------------------------------------------------


def arm_vectors(delta, pj, rj) -> dict[str, Any]:
    """The vectors the arms add at P3 (rows of Δ [n, d]); none adds nothing."""
    return {"whole": delta, "no_jpp": delta - pj, "no_rand": delta - rj, "jpp": pj, "rest": delta - pj}


def stage_run(name: str, why: str, mode: str = "53.3") -> Path:
    """53.3's run; mode "ans13": 53.3b's check, the lookup alone at its answer layer minus 1 and minus 3."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "53.3 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"53.3 runs on {sorted(RUNS)}, not {target}"
    lay = layers_of(target, mode)
    per_reader = {w: lay["readers"][READER_NAME[w]]["layers"] for w in READERS if READER_NAME[w] in lay["readers"]}
    all_layers = sorted({la for v in per_reader.values() for la in v})
    source = G.SOURCES[target]
    src = X.RESULTS / source
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl")),
              pins.REPO_ROOT / lay["peak_file"], pins.REPO_ROOT / lay["read_file"]]  # fmt: skip
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": TEST,
         "spec": "jobs/c3/batch53.yaml (53.3)" if mode == "53.3" else "jobs/c3/batch53.yaml (test_53_3b: the check)",
         "question": NO_PREDICTION, "mode": mode,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs}, "source": source,
         "L": X.PREDICTED[target], "layers": lay, "k": K, "arms": ARM_TEXT, "rule": RULE, "as_computed": AS_COMPUTED,
         "items_rule": "51.10's items (x51_jread.select), 49.1's locker-first ones (51.10's write arms)",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT, "sealed": "none (no prediction)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    gate = G.source_gate(source)
    assert G.gate_passes(gate), f"{source}: the gate fixed in advance does not pass ({gate})"
    model = load_model()
    lens = JLens(model, "jpp")
    missing = [la for la in all_layers if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at {missing}"
    tok = model.tokenizer
    items, counts = select(tok, target)
    assert items, "no locker-first items"
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    dev = model.device
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    letters = model.letter_token_ids()
    d = int(model.hf.lm_head.weight.shape[1])
    n = len(items)
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        # 1. the states at P3 at each reader's layers (one forward per item, reader and O / S), copied to the CPU
        h = {(w, v): {la: torch.zeros(n, d) for la in per_reader[w]} for w in per_reader for v in JR.VARIANTS}
        for i, it in enumerate(progress(items, "53.3: states at P3 (item: readers x O / S)")):
            for w, rd in it["readers"].items():
                if w not in per_reader:
                    continue
                for v in JR.VARIANTS:
                    ids = torch.tensor([rd["ids"][v] + it["space"]], device=dev)
                    _, rec = model.run(ids, record=tuple(per_reader[w]))
                    p3 = it["jpos"][w]["P3"][v]
                    assert p3 == ids.shape[1] - 1, f"{it['scene']}: P3 is not the last token"
                    for la in per_reader[w]:
                        h[(w, v)][la][i] = rec[la][p3].float().cpu()  # a copy (memory lesson 2)
                    del rec
        # 2. the parts per layer (the J++ dictionary built and freed per layer)
        vecs: dict[tuple[str, int], dict[str, Any]] = {}
        norms = []
        for la in all_layers:
            jdic = lens.vectors(la, letters)
            basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            for w in per_reader:
                if la not in per_reader[w]:
                    continue
                delta = (h[(w, "alt")][la] - h[(w, "org")][la]).to(dev)
                pj, rj = G.lens_parts(jdic, delta, K, basis)
                vecs[(w, la)] = {k: v.float().cpu().clone() for k, v in arm_vectors(delta, pj, rj).items()}
                sj, sr = G.share(pj, delta), G.share(rj, delta)
                norms += [{"scene": it["scene"], "reader": w, "layer": la, "norm_delta": round(float(delta[i].norm()), 4),
                           "share_J": round(float(sj[i]), 6), "share_rand": round(float(sr[i]), 6)}
                          for i, it in enumerate(items)]  # fmt: skip
            del jdic, basis
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        # 3. the reads: per item and reader, O unedited and every arm at each of the reader's layers (one batch list)
        rows = []
        for i, it in enumerate(progress(items, "53.3: reads (item: readers x arms x layers)")):
            for w, rd in it["readers"].items():
                if w not in per_reader:
                    continue
                p3 = it["jpos"][w]["P3"]["org"]
                names = [(la, a) for la in per_reader[w] for a in ARMS[1:]]
                edits = [{}] + [{la: AddRows(vecs[(w, la)][a][i : i + 1].to(dev), [p3])} for la, a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], None)
                for (la, a), lg in zip([(None, "none"), *names], logits, strict=True):
                    rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                                 "layer": la, "arm": a, **X.read_row(lg, rd, digits),
                                 "top_text": model.decoded[int(lg.argmax())]})  # fmt: skip
        X.write_jsonl(out / "outcomes.jsonl", rows)
    print(f"wrote {out}: {len(rows)} reads of {n} items", flush=True)
    return out


# ---- 53.3b: word answers (Zach's named-bridge passages; Z1-P's items) ---------------------------------------------


def words_items(target: str) -> tuple[list[dict], dict]:
    """Z1-P's chosen passages on the target (x50_zach's run: its gate.json "order", the cases in that order) of the
    brief's set: Zach's named-bridge passages of jsuite_v2_test_chat, whose PP and PM items jsuite_v2_1_test_chat keeps
    unchanged (same ids, asserted); Z1-P's passages of his second seed (jsuite_v2nb) are left out. Reader slot K = the
    PP passage (the lookup copies the made-up word the passage states), M = the PM passage (the recall, the same answer
    vocabulary); S = the pointer sentence names another entity."""
    from scripts import x50_zach as Z

    src = Z.RESULTS / WORD_SOURCE[target]
    gate = json.loads((src / "gate.json").read_text())
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    items = [cases[(s, sc)] for s, sc in gate["order"] if s == WORD_SET]
    assert items, f"{src.name}: no chosen passages of {WORD_SET}"
    v21 = {json.loads(line)["id"] for line in (pins.DATA_DIR / "tasks_v2" / WORD_SET_V21 / "items.jsonl").open()}
    for c in items:
        assert set(c["readers"]) == set(WORD_SLOTS), f"{c['scene']}: reader slots {sorted(c['readers'])}"
        for rd in c["readers"].values():
            assert rd["id"] in v21, f"{rd['id']} is not in {WORD_SET_V21}"
            assert len(rd["ids"]["org"]) == len(rd["ids"]["alt"]), f"{c['scene']}: O and S differ in length"
    return items, gate


def word_layers(answer: int | None, peak: int, have: list[int]) -> tuple[list[int], list[int]]:
    """A reader's layers: its answer layer minus 1, 2 and 3 and 51.10's read peak (deduplicated, in order); those
    without a lens map (or below 0) dropped and returned beside."""
    want = [*([answer - o for o in WORD_OFFSETS] if answer is not None else []), peak]
    want = list(dict.fromkeys(want))
    return [la for la in want if la >= 0 and la in have], [la for la in want if la < 0 or la not in have]


def stage_plan_words() -> dict:
    target = pins.TARGET
    items, gate = words_items(target)
    lay = layers_of(target)
    blob = {"target": target, "run": WORD_RUNS[target], "source": WORD_SOURCE[target], "items": len(items),
            "sets": dict(collections.Counter(c["set"] for c in items)), "gate": {k: gate[k] for k in
            ("org_read_accuracy", "pass", "eligible", "chosen") if k in gate},
            "peaks": {k: v["peak"] for k, v in lay["readers"].items()},
            "prompt_tokens": {s: [min(len(c["readers"][s]["ids"]["org"]) for c in items),
                                  max(len(c["readers"][s]["ids"]["org"]) for c in items)] for s in WORD_SLOTS}}  # fmt: skip
    print(json.dumps(blob, indent=1))
    return blob


def stage_run_words(name: str, why: str) -> Path:
    import statistics

    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x50_zach as Z
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in WORD_SOURCE, f"53.3b reads Z1-P's passages, which exist on {sorted(WORD_SOURCE)}, not {target}"
    items, gate = words_items(target)
    peaks = layers_of(target)
    below = None if gate.get("pass") else (
        f"below gate (exploratory): Z1-P's gate on {target} fails ({gate.get('org_read_accuracy')} < 0.80); its eligible "
        "passages only; hollow, rules verbatim, no prediction")  # fmt: skip
    src = Z.RESULTS / WORD_SOURCE[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, src / "gate.json", src / "cases.jsonl", pins.REPO_ROOT / peaks["peak_file"]]
    m: dict[str, Any] = {
        "exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
        "test": TEST_WORDS, "spec": "jobs/c3/batch53.yaml (test_53_3b)", "question": NO_PREDICTION, "mode": "words",
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs}, "source": WORD_SOURCE[target],
        "below_gate": below, "k": K, "arms": {a: ARM_TEXT[a] for a in ARMS_WORDS}, "arm_names": list(ARMS_WORDS),
        "rule": RULE, "rule_words": RULE_WORDS, "as_computed": AS_COMPUTED_WORDS,
        "items_rule": "Z1-P's chosen passages (x50_zach's run, gate.json order): Zach's jsuite v2 named-bridge passages "
                      "(jsuite_v2_1 keeps v2's PP / PM items unchanged); K = PP (the lookup), M = PM (the recall)",
        "read": "his open read (x50_zach's): the top token after the prompt (no appended token); switch = S's answer's "
                "first token",
        "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                  "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT, "sealed": "none (no prediction)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    model = load_model()
    lens = JLens(model, "jpp")
    have = sorted(int(la) for la in lens.source_layers)
    dev = model.device
    ws = X.whitespace_mask(model)
    letters = model.letter_token_ids()
    n_layers = pins.N_LAYERS
    n = len(items)
    X.write_jsonl(out / "cases.jsonl", items)
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        # 1. O at every layer at the last token: the logit lens (the answer layer, as 51.10) and the states (fp16, CPU)
        h_o = {
            s: torch.zeros(n, n_layers, int(model.hf.lm_head.weight.shape[1]), dtype=torch.float16) for s in WORD_SLOTS
        }
        settle: dict[str, list[int | None]] = {s: [] for s in WORD_SLOTS}
        for i, c in enumerate(progress(items, "53.3b: O at every layer (passage: 2 readers)")):
            for s, rd in c["readers"].items():
                ids = rd["ids"]["org"]
                _, rec = model.run(torch.tensor([ids], device=dev), record=tuple(range(n_layers)))
                last = torch.stack([rec[la][len(ids) - 1] for la in range(n_layers)])
                h_o[s][i] = last.to(torch.float16).cpu()
                settle[s].append(JR.settle_layer(model.unembed(last).argmax(1).tolist(), rd["tok_A"]))
                del rec, last
        assert all(torch.isfinite(v).all() for v in h_o.values()), "fp16 overflow in the cached O states"
        readers: dict[str, Any] = {}
        per: dict[str, list[int]] = {}
        for s, w in WORD_SLOTS.items():
            ok = [x for x in settle[s] if x is not None]
            ans = statistics.median_low(ok) if ok else None
            layers, dropped = word_layers(ans, peaks["readers"][READER_NAME[w]]["peak"], have)
            per[s] = layers
            readers[READER_NAME[w]] = {"answer": ans, "peak": peaks["readers"][READER_NAME[w]]["peak"], "layers": layers,
                                       "dropped": dropped, "n": len(settle[s]), "never": len(settle[s]) - len(ok),
                                       "per_item": settle[s]}  # fmt: skip
        m["layers"] = {"mode": "words", "source_run": peaks["source_run"], "peak_file": peaks["peak_file"],
                       "answer_from": "the plain logit lens at the last token of O, every layer: per passage the layer "
                                      "from which O's answer token is the top token through the last layer, the lower "
                                      "median over the passages (51.10's answer_layers, x51_jread.settle_layer)",
                       "readers": readers}  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        # 2. S at the reader's layers
        h_s = {s: {la: torch.zeros(n, h_o[s].shape[-1]) for la in per[s]} for s in WORD_SLOTS}
        for i, c in enumerate(progress(items, "53.3b: S at the readers' layers (passage)")):
            for s, rd in c["readers"].items():
                ids = rd["ids"]["alt"]
                _, rec = model.run(torch.tensor([ids], device=dev), record=tuple(per[s]))
                for la in per[s]:
                    h_s[s][la][i] = rec[la][len(ids) - 1].float().cpu()
                del rec
        # 3. the parts per layer
        vecs: dict[tuple[str, int], dict[str, Any]] = {}
        norms = []
        for la in sorted({la for v in per.values() for la in v}):
            jdic = lens.vectors(la, letters)
            basis = SP.random_basis(
                h_o[next(iter(WORD_SLOTS))].shape[-1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)
            ).to(dev)
            for s in WORD_SLOTS:
                if la not in per[s]:
                    continue
                delta = (h_s[s][la] - h_o[s][:, la].float()).to(dev)
                pj, rj = G.lens_parts(jdic, delta, K, basis)
                vecs[(s, la)] = {k: v.float().cpu().clone() for k, v in arm_vectors(delta, pj, rj).items()}
                sj, sr = G.share(pj, delta), G.share(rj, delta)
                norms += [{"scene": f"{c['set']}:{c['scene']}", "reader": WORD_SLOTS[s], "layer": la,
                           "norm_delta": round(float(delta[i].norm()), 4), "share_J": round(float(sj[i]), 6),
                           "share_rand": round(float(sr[i]), 6)} for i, c in enumerate(items)]  # fmt: skip
            del jdic, basis
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        # 4. the reads at the last token: O unedited and every arm at each of the reader's layers
        rows = []
        for i, c in enumerate(progress(items, "53.3b: reads (passage: 2 readers x arms x layers)")):
            for s, rd in c["readers"].items():
                last = len(rd["ids"]["org"]) - 1
                names = [(la, a) for la in per[s] for a in ARMS_WORDS[1:]]
                edits = [{}] + [{la: AddRows(vecs[(s, la)][a][i : i + 1].to(dev), [last])} for la, a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", [], ws)
                for (la, a), lg in zip([(None, "none"), *names], logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": f"{c['set']}:{c['scene']}", "entity": c["bridge"], "domain": c["relation"],
                                 "reader": WORD_SLOTS[s], "layer": la, "arm": a, "top": top, "switched": int(top == rd["tok_b"]),
                                 "right": int(top == rd["tok_A"]), "top_text": model.decoded[top]})  # fmt: skip
        X.write_jsonl(out / "outcomes.jsonl", rows)
    print(f"wrote {out}: {len(rows)} reads of {n} passages", flush=True)
    return out


def across_readers(models: list[dict]) -> dict[str, Any]:
    """53.3b's rule across readers: per model, at the answer layer minus 1 and minus 2, "copy bypasses" when the recall is
    "through the lens" and the lookup "outside" at both (valid cells only), "digits only" when the lookup is "through
    the lens" like the recall at both; the label over the models (>= 3 of 4), pending while too few models ran."""

    def at(mdl: dict, reader: str, offset: int) -> dict | None:
        info = mdl["layers"]["readers"].get(reader) or {}
        ans = info.get("answer")
        if ans is None:
            return None
        return next((c for c in mdl["cells"] if c["reader"] == reader and c["layer"] == ans - offset), None)

    per = {}
    for mdl in models:
        cells = {(w, o): at(mdl, w, o) for w in ("lookup", "recall") for o in ACROSS_OFFSETS}
        good = {k: v for k, v in cells.items() if v is not None and v["x0_valid"]}
        complete = len(good) == len(cells)
        copy = complete and all(good[("recall", o)]["label"] == "through" and good[("lookup", o)]["label"] == "outside"
                                for o in ACROSS_OFFSETS)  # fmt: skip
        digits = complete and all(good[("recall", o)]["label"] == "through" and good[("lookup", o)]["label"] == "through"
                                  for o in ACROSS_OFFSETS)  # fmt: skip
        per[mdl["target"]] = {"copy_bypasses": copy, "digits_only": digits, "complete": complete,
                              "below_gate": bool(mdl.get("below_gate")),
                              "labels": {f"{w} answer-{o}": (None if v is None else v["label"] if v["x0_valid"] else "invalid")
                                         for (w, o), v in cells.items()}}  # fmt: skip
    # a model below its source's gate is reported (hollow) and never counted toward a clause (the 09:50 standing rules)
    n_copy = sum(v["copy_bypasses"] and not v["below_gate"] for v in per.values())
    n_digits = sum(v["digits_only"] and not v["below_gate"] for v in per.values())
    missing = N_MODELS_WORDS - len(per)
    if n_copy >= ACROSS_MIN:
        lab = "copy bypasses the lens"
    elif n_digits >= ACROSS_MIN:
        lab = "digits only"
    elif missing and (n_copy + missing >= ACROSS_MIN or n_digits + missing >= ACROSS_MIN):
        lab = f"pending ({len(per)} of {N_MODELS_WORDS} models)"
    else:
        lab = "in between"
    return {"label": lab, "per_model": per, "copy_models": n_copy, "digits_models": n_digits, "models": len(per)}


def word_example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = X.read_jsonl(src / "outcomes.jsonl")
    pick = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    lines = [f"## {run}: {len(pick)} random passages of {len(items)} (seed {seed})", ""]
    for i in pick:
        c = items[i]
        key = f"{c['set']}:{c['scene']}"
        lines += [f"### {key} ({c['relation']}): bridge {c['bridge']} → {c['cf_bridge']}", ""]
        for s, rd in c["readers"].items():
            w = WORD_SLOTS[s]
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): {rd['question']} O's answer {rd['answer']}, S's answer "
                      f"{rd['cf_answer']}", "", "```", rd["context"], "```", "", "| layer | arm | top token | switched |",
                      "|---|---|---|---|"]  # fmt: skip
            for r in reads:
                if r["scene"] == key and r["reader"] == w:
                    lines.append(f"| {'-' if r['layer'] is None else r['layer']} | {r['arm']} | {r['top_text']!r} | "
                                 f"{r['switched']} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict_words(runs: list[str], locker_runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    """53.3b's verdict: per model, reader and layer 53.3's labels (53.3's validity bar applied: a cell under it is
    "invalid"), the rule across readers, and the check on the locker scenes (53.3's lookup at answer - 1 / - 3)."""
    models = [run_numbers(r, n_boot) for r in runs]
    checks = [run_numbers(r, n_boot) for r in locker_runs]
    across = across_readers(models)
    out = RESULTS / f"x53_lastconflict_words-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 53.3b: the last-token conflict test on word answers", "",
             f"Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; {NO_PREDICTION}). Zach's named-bridge passages "
             "(Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer "
             "vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read "
             "peak. UNVERIFIED.", "", f"Rule per reader and layer (53.3's): {RULE}; 53.3's validity bar (S_whole >= "
             f"{X.VALID_S}, >= {X.VALID_N} switches) applied.", "", f"Rule across readers: {RULE_WORDS}.", "",
             f"As computed: {AS_COMPUTED_WORDS}.", "", f"**Across readers: {across['label']}** (copy bypasses on "
             f"{across['copy_models']} of {across['models']} models run, digits only on {across['digits_models']}).", "",
             "| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the "
             "lens part alone | loss beyond random | rest / whole | label | valid |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in models:
        for c in mdl["cells"]:
            info = mdl["layers"]["readers"][c["reader"]]
            r = c["rates"]
            lab = c["text"] if c["x0_valid"] else f"invalid ({c['text']})"
            lines.append(f"| {mdl['target']}{' ○' if mdl.get('below_gate') else ''} | {c['reader']} | {c['layer']} "
                         f"({why_of(c['layer'], info)}) | {c['n']} ({c['entities']}) | {fmt(r['whole'])} | "
                         f"{fmt(r['no_jpp'])} | {fmt(r['no_rand'])} | {fmt(r['jpp'])} | {fmt(c['excess'])} | "
                         f"{fmt(c['rest_share'])} | **{lab}** | {'yes' if c['x0_valid'] else 'no'} |")  # fmt: skip
    lines += ["", "Per model (answer - 1 and - 2): " + "; ".join(
        f"{t}: copy bypasses {'yes' if v['copy_bypasses'] else 'no'}, digits only {'yes' if v['digits_only'] else 'no'} "
        f"{json.dumps(v['labels'])}" for t, v in across["per_model"].items()) + ".", ""]  # fmt: skip
    for mdl in models:
        if mdl.get("below_gate"):
            lines.append(f"○ {mdl['target']}: {mdl['below_gate']}")
        ans = {k: (v["answer"], v["never"], v["dropped"]) for k, v in mdl["layers"]["readers"].items()}
        lines.append(f"- {mdl['target']} ({mdl['run']}): answer layer (never settled, layers without a lens map) {ans}")
    lines += ["", "## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3", "",
              "| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond "
              "random | rest / whole | label | valid |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in checks:
        for c in mdl["cells"]:
            info = mdl["layers"]["readers"][c["reader"]]
            r = c["rates"]
            lines.append(f"| {mdl['target']} | {c['reader']} | {c['layer']} ({why_of(c['layer'], info)}) | {c['n']} | "
                         f"{fmt(r['whole'])} | {fmt(r['no_jpp'])} | {fmt(r['no_rand'])} | {fmt(c['excess'])} | "
                         f"{fmt(c['rest_share'])} | **{c['text']}** | {'yes' if c['x0_valid'] else 'no'} |")  # fmt: skip
    lines += ["", "Figure: x53_lastconflict_words.png"]
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "locker_runs": locker_runs, "question": NO_PREDICTION,
                                                  "rule": RULE, "rule_words": RULE_WORDS, "across": across,
                                                  "models": models, "checks": checks}, indent=1, default=str) + "\n")  # fmt: skip
    figure(models + checks, out / "x53_lastconflict_words.png")
    ex = ["# 53.3b examples (verify pack): the passages as read and every arm's top token. UNVERIFIED.", ""]
    for mdl in models:
        ex += word_example_lines(mdl["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def why_of(layer: int, info: dict) -> str:
    """Why a layer was read: 51.10's read peak, or the reader's answer layer minus some offset."""
    if layer == info.get("peak"):
        return "read peak"
    return f"answer L{info['answer']} - {info['answer'] - layer}" if info.get("answer") is not None else "-"


def label(excess: float, rest: float) -> str:
    """The brief's rule on one reader and layer (point estimates, EPS at the bars)."""
    if excess <= OUTSIDE_MAX + EPS and rest >= REST_MIN - EPS:
        return "outside"
    if excess >= THROUGH_MIN - EPS:
        return "through"
    return "between"


def cell_numbers(rows: list[dict], reader: str, layer: int, n_boot: int = X.N_BOOT,
                 arms: tuple[str, ...] = ARMS) -> dict[str, Any]:  # fmt: skip
    """One reader at one layer: each arm's switch rate (none: O unedited), the excess and the rest's share with paired
    cluster-bootstrap CIs over the bridge entities, the label. Without a "rest" arm (53.3b's arms) the rest alone is
    read from no_jpp, the same vector."""
    by: dict[tuple[str, str], int] = {}
    ent: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader and (r["layer"] == layer or r["arm"] == "none"):
            by[(r["scene"], r["arm"])] = int(r["switched"])
            ent.setdefault(r["scene"], r["entity"])
    scenes = list(ent)
    missing = [(s, a) for s in scenes for a in arms if (s, a) not in by]
    assert not missing, f"{reader} L{layer}: {len(missing)} reads missing, e.g. {missing[:3]}"
    sw = {a: [by[(s, a)] for s in scenes] for a in arms}
    rest_arm = "rest" if "rest" in arms else "no_jpp"
    ents = [ent[s] for s in scenes]
    boot = X.resampled_rates(sw, ents, n_boot)
    rate = {a: float(np.mean(sw[a])) for a in arms}
    with np.errstate(divide="ignore", invalid="ignore"):
        ex_b = (boot["no_rand"] - boot["no_jpp"]) / boot["whole"]
        rest_b = boot[rest_arm] / boot["whole"]
    s_whole = rate["whole"]
    if s_whole <= 0:
        excess = rest = math.nan
        lab = "untested"
    else:
        excess = (rate["no_rand"] - rate["no_jpp"]) / s_whole
        rest = rate[rest_arm] / s_whole
        lab = label(excess, rest)
    return {"reader": READER_NAME[reader], "layer": layer, "n": len(scenes), "entities": len(set(ents)),
            "rates": {a: [rate[a], *X.interval(boot[a])] for a in arms},
            "switches_whole": int(sum(sw["whole"])), "excess": [excess, *X.interval(ex_b)],
            "rest_share": [rest, *X.interval(rest_b)], "label": lab, "text": LABELS[lab],
            "x0_valid": bool(s_whole >= X.VALID_S - EPS and sum(sw["whole"]) >= X.VALID_N),
            "rest_equals_no_jpp": sw[rest_arm] == sw["no_jpp"]}  # fmt: skip


def run_numbers(run: str, n_boot: int = X.N_BOOT, results: Path | None = None) -> dict[str, Any]:
    src = (results or RESULTS) / run
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    arms = tuple(m.get("arm_names") or ARMS)
    cells = [cell_numbers(rows, w, la, n_boot, arms) for w in READERS if READER_NAME[w] in m["layers"]["readers"]
             for la in m["layers"]["readers"][READER_NAME[w]]["layers"]]  # fmt: skip
    return {"run": run, "target": m["model"]["target"], "layers": m["layers"], "cells": cells, "arms": arms,
            "mode": m.get("mode", "53.3"), "below_gate": m.get("below_gate")}  # fmt: skip


def fmt(v: list) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(models: list[dict], path: Path) -> None:
    """Per model a panel: per reader and layer each edit arm's switch rate with its 95% CI."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(models), figsize=(5.5 * len(models), 3.8), squeeze=False)
    for ax, mdl in zip(axes[0], models, strict=True):
        cells = mdl["cells"]
        arms = tuple(mdl.get("arms") or ARMS)[1:]
        width = 0.8 / len(arms)
        for j, a in enumerate(arms):
            xs = [i + (j - (len(arms) - 1) / 2) * width for i in range(len(cells))]
            ys = [c["rates"][a][0] for c in cells]
            err = [[max(0.0, c["rates"][a][0] - c["rates"][a][1]) for c in cells],
                   [max(0.0, c["rates"][a][2] - c["rates"][a][0]) for c in cells]]  # fmt: skip
            ax.bar(xs, ys, width, yerr=err, capsize=2, label=ARM_TEXT[a].split(":")[0])
        ax.set_xticks(range(len(cells)))
        ax.set_xticklabels([f"{c['reader']} L{c['layer']}\n{c['text'][:24]}" for c in cells], fontsize=7)
        ax.set_ylim(0, 1)
        ax.set_ylabel("switched to S's answer")
        ax.set_title(f"{mdl['target']} ({mdl['run']}{', below gate' if mdl.get('below_gate') else ''})", fontsize=9)
    axes[0][0].legend(fontsize=6)
    fig.suptitle(f"{'53.3b: word answers' if any(m.get('mode') == 'words' for m in models) else '53.3'}: the conflict "
                 "test at the last token (UNVERIFIED)", fontsize=10)  # fmt: skip
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items (seed 0): per reader its answers and every arm's top token per layer (the prompts as read are
    51.10's, marked in its plan)."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = X.read_jsonl(src / "outcomes.jsonl")
    pick = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    lines = [f"## {run}: {len(pick)} random items of {len(items)} (seed {seed})", ""]
    for i in pick:
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} → {it['cf_bridge']}", "",
                  f"O's context: {it.get('context', '-')}", "", f"S's context: {it.get('cf_context', '-')}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['question']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}",
                      "", "| layer | arm | top token | switched |", "|---|---|---|---|"]  # fmt: skip
            for r in reads:
                if r["scene"] == it["scene"] and r["reader"] == w:
                    lines.append(f"| {'-' if r['layer'] is None else r['layer']} | {r['arm']} | {r['top_text']!r} | "
                                 f"{r['switched']} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    models = [run_numbers(r, n_boot) for r in runs]
    out = RESULTS / f"x53_lastconflict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 53.3: the conflict test at the last token", "",
             f"Batch 53, test 53.3 (jobs/c3/batch53.yaml; {NO_PREDICTION}). The change at the last token (P3) at 51.10's "
             "read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.", "",
             f"Rule (Dan's brief): {RULE}.", "", f"As computed: {AS_COMPUTED}.", "",
             "| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | "
             "the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in models:
        for c in mdl["cells"]:
            info = mdl["layers"]["readers"][c["reader"]]
            why = why_of(c["layer"], info)
            r = c["rates"]
            lines.append(f"| {mdl['target']} | {c['reader']} | {c['layer']} ({why}) | {c['n']} ({c['entities']}) | "
                         f"{fmt(r['whole'])} | {fmt(r['no_jpp'])} | {fmt(r['no_rand'])} | {fmt(r['jpp'])} | "
                         f"{fmt(r.get('rest'))} | {fmt(c['excess'])} | {fmt(c['rest_share'])} | **{c['text']}** | "
                         f"{'yes' if c['x0_valid'] else 'no'} |")  # fmt: skip
    floors = "; ".join(f"{m['target']} {c['reader']} {fmt(c['rates']['none'])}" for m in models for c in m["cells"])
    sources = "; ".join(f"{m['target']}: {m['layers']['peak_file']}, {m['layers']['read_file']}" for m in models)
    lines += ["", f"O unedited switched (floor): {floors}.", "", f"Layer sources: {sources}.", "",
              "Figure: x53_lastconflict.png"]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "question": NO_PREDICTION, "rule": RULE,
                                                  "as_computed": AS_COMPUTED, "models": models}, indent=1) + "\n")  # fmt: skip
    figure(models, out / "x53_lastconflict.png")
    ex = ["# 53.3 examples (verify pack): every arm's top token per layer for 10 random items per run. UNVERIFIED.", ""]
    for mdl in models:
        ex += example_lines(mdl["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "plan-words", "run-words", "verdict-words"])
    ap.add_argument("--name", help="run / run-words: the run name (results/x53_lastconflict/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict(-words): the runs (default: every one here)")
    ap.add_argument("--locker-runs", nargs="*", default=None,
                    help="verdict-words: 53.3b's check runs (run --mode ans13; default: every one here)")  # fmt: skip
    ap.add_argument("--mode", choices=MODES, default="53.3",
                    help="run: 53.3 (read peak, answer - 2) or ans13 (53.3b's check: the lookup at answer - 1, - 3)")  # fmt: skip
    ap.add_argument("--why", default="batch 53, test 53.3 (jobs/c3/batch53.yaml)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    here = lambda d: [r for r in d.values() if (RESULTS / r / "outcomes.jsonl").exists()]  # noqa: E731
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.mode)
    elif a.stage == "verdict":
        stage_verdict(a.runs or here(RUNS), a.n_boot)
    elif a.stage == "plan-words":
        stage_plan_words()
    elif a.stage == "run-words":
        assert a.name, "run-words needs --name"
        stage_run_words(a.name, a.why)
    else:
        locker = here(RUNS_ANS13) if a.locker_runs is None else a.locker_runs
        stage_verdict_words(a.runs or here(WORD_RUNS), locker, a.n_boot)


if __name__ == "__main__":
    main()
