"""x49_report (batch 49, test 49.6; jobs/c3/batch49.yaml "49.6", design and rule fixed in advance; Q49.6 in
predictions/2026-10-28_dan.md): the report of slot 1, reworded.

47.10's report reader ("Was the locker of <p>'s pick listed first, second or third?") failed the 9B's gate: slot 1 read
right in 0.03 of scenes (slot 2 0.92, slot 3 0.66), the digit variant 0.08. Is that the wording, or the model?

Scenes: 47.10's exactly (scripts/x47_report.py build_items: the routes generator's C0 scenes, seed 2510, 500
generated, the same drops), O only (unedited only). Two new wordings of the report, each its own prompt over the same
context, X0's chat read as 47.10's:
  position  "Was the locker of <p>'s pick listed in position 1, 2 or 3 of the list?"                          digit
  sentence  "Which of the three locker sentences - the first, the second or the third - gives the locker of
            <p>'s pick?"                                                                                       word
Dan's brief gives the first wording as "In position 1, 2 or 3 of the list?": here it replaces the tail of 47.10's
digit report ("listed 1, 2 or 3?"), so the two differ only in that phrase. The answer: the asked item's slot, as a
digit (1 / 2 / 3) or an ordinal word (' first' / ' second' / ' third', 47.10's read token). Question-last (the
routes order, 47.10's headline gate); --orders last,first adds 47.10's question-first order.

Reads per scene, order and wording: 8 greedy tokens and what they say (47.10's said: the first ordinal word or digit of
the first line), the decisive read (the top token is the answer token) and the candidate read (which of the three
answer tokens is highest: the slot the model prefers). Accuracy by the asked item's true slot: 'read' (decides: 47.10's
gate measure, the one whose slot 1 was 0.03, so 'stays' means the same thing), 'said' and 'candidate' beside; the
candidate's confusion (true slot x preferred slot); for the digit wording, the share that says the locker digit (the
lookup's answer) instead. 47.10's two wordings on the same scenes are read from its committed competence.jsonl
(question-last, O) beside, as the reference (no rerun). Note: on 47.10's own wording the 9B's slot 1 is 0.03 read but
0.33 said and 0.29 candidate (its greedy text often names the slot in another spelling); the verdict prints all three.

Rule (jobs/c3/batch49.yaml 49.6, verbatim): "If slot 1 stays <= 0.2 on the 9B under both wordings, keep as an
appendix curiosity; if it recovers, drop." As computed: slot 1's read accuracy, question-last order, point estimate
(EPS 1e-9); 'stays' if <= 0.2 under both new wordings, 'recovers' if > 0.2 under either (Q49.6's "above 0.2 under
either wording"); the action (appendix / drop) from the 9B; the 27B's label the same way, beside. No gate (the
accuracies are the outcome; the scenes' lookup read 1.00 / 1.00 on the 9B / 27B in 47.10). Cluster bootstrap over
bridge items (10,000, seed 0) beside every rate.

SEALED: the run writes per-scene reads only; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's
Q49.6 answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x49_report.py plan --out results/x49_report/plan-<UTC>   # CPU
uv run python scripts/x49_report.py run --name x49_6_27b                                            # GPU (sealed)
uv run python scripts/x49_report.py verdict --runs x49_6_27b qwen35_9b_x49_6                        # CPU, after Q49.6
uv run python scripts/x49_report.py view --name qwen35_9b_x49_6                                     # CPU: verify pack
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import subprocess
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
from scripts import x6_routes as R
from scripts import x47_report as Q

EXP = "x49_report"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch49.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION, TEST = "Q49.6", "49.6"
MODELS = ("qwen3.6-27b", "qwen3.5-9b")
RUNS = {"qwen3.6-27b": "x49_6_27b", "qwen3.5-9b": "qwen35_9b_x49_6"}
REFERENCE = {"qwen3.6-27b": "x47_report_27b", "qwen3.5-9b": "qwen35_9b_x47_report"}  # 47.10's runs (competence)
WORDINGS = ("position", "sentence")
QUESTIONS = {"position": "Was the locker of {p}'s pick listed in position 1, 2 or 3 of the list?",
             "sentence": "Which of the three locker sentences - the first, the second or the third - gives the "
                         "locker of {p}'s pick?"}  # fmt: skip
KIND = {"position": "digit", "sentence": "word"}
OLD = ("report", "report_digit")  # 47.10's wordings, read from its competence.jsonl
ORDERS = ("last",)
SLOTS = ("1", "2", "3")
RECOVER = 0.2
HEADLINE = ("qwen3.5-9b", "last")  # the rule's model and order
EPS = 1e-9
MEASURES = ("said", "read", "cand")
RULE_MEASURE = "read"  # 47.10's gate measure (its 9B slot 1: 0.03 read, 0.33 said)
FIELD = {"said": "said_right", "read": "read_right", "cand": "cand_right", "locker": "said_locker"}
# 'locker' (beside, the digit wording only): the share that says the asked item's locker digit, the lookup's answer


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def answer_of(slot: int, kind: str) -> str:
    """The report's answer for a 0-based slot: the digit or the ordinal word."""
    return str(slot + 1) if kind == "digit" else Q.ORDINALS[slot]


def candidates(tok) -> dict[str, list[int]]:
    """Per answer kind, the three answer tokens in slot order (digit: '1' '2' '3' as X0 reads digits; word: 47.10's
    read tokens ' first' ' second' ' third')."""
    from scripts import suite_v1 as S

    words = Q.answer_ids(tok)
    return {"digit": [S.answer_token(tok, d, "digit") for d in SLOTS], "word": [words[w][0] for w in Q.ORDINALS]}


def build_reader(tok, context: str, asked: str, slot: int, wording: str, order: str) -> dict:
    """One wording's O prompt (47.10's prompt function), its ids and its answer."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import suite_v1 as S

    kind = KIND[wording]
    question = QUESTIONS[wording].format(p=asked)
    text = Q.prompt(tok, context, question, kind, order)
    assert text.count(context) == 1, "the context is not once in the prompt"
    ids = list(raw_encoding(tok, text, offsets=False)["input_ids"])
    ans = answer_of(slot, kind)
    return {"question": question, "kind": kind, "text": text, "ids": ids, "answer": ans,
            "tok_A": S.answer_token(tok, ans, kind), "suffix": Q.suffix(tok, kind)}  # fmt: skip


def build_items(tok, n_gen: int = Q.N_GEN, orders: tuple[str, ...] = ORDERS) -> tuple[list[dict], dict]:
    """47.10's items (the same scenes and drops), each with the two new wordings' O prompts per order."""
    base, counts = Q.build_items(tok, n_gen, orders)
    out = []
    for it in base:
        out.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "asked": it["asked"],
                    "context": it["context"], "slot": it["slot"]["org"],
                    "locker": it["orders"][orders[0]]["readers"]["lookup"]["answer"],
                    "orders": {o: {w: build_reader(tok, it["context"], it["asked"], it["slot"]["org"], w, o)
                                   for w in WORDINGS} for o in orders}})  # fmt: skip
    counts = {**counts, "orders": list(orders), "wordings": {w: {"question": QUESTIONS[w], "kind": KIND[w]}
                                                             for w in WORDINGS},
              "true_slot": dict(sorted(collections.Counter(str(it["slot"] + 1) for it in out).items()))}  # fmt: skip
    return out, counts


def marked(decode, rd: dict) -> str:
    """The prompt as the model reads it (ids decoded, the template included), the read suffix appended."""
    return decode(rd["ids"] + rd["suffix"])


def stage_plan(n_gen: int = Q.N_GEN, k: int = 5, out: Path | None = None, orders: tuple[str, ...] = ORDERS) -> dict:
    """Tokenizer only: the items, the answer tokens (one token each), and k example items' prompts (seed 0) under
    both wordings. With `out`, written there as <target>_plan.json and <target>_prompts.md."""
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    items, counts = build_items(tok, n_gen, orders)
    cands = candidates(tok)
    counts["target"] = pins.TARGET
    counts["answer_tokens"] = {kind: {tok.decode([t]): t for t in ts} for kind, ts in cands.items()}
    counts["read_suffix"] = {kind: Q.suffix(tok, kind) for kind in ("digit", "word")}
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    lines = [f"# 49.6 plan: {pins.TARGET}, {min(k, len(items))} example items of {len(items)} (seed "
             f"{X.EXAMPLES_SEED}): the two reworded reports as the model reads them (ids decoded, the template "
             "included, the read suffix appended: a space token for the digit wording, nothing for the word one). "
             "UNVERIFIED.", ""]  # fmt: skip
    for i in Q.example_indices(len(items), k):
        it = items[i]
        lines.append(f"### {it['scene']}: {it['asked']} picked {it['entity']}, its locker in slot {it['slot'] + 1}")
        for o in orders:
            for w in WORDINGS:
                rd = it["orders"][o][w]
                lines += ["", f"[{o}] {w}: answer {rd['answer']!r} (token {rd['tok_A']})", "", "```", marked(decode, rd),
                          "```"]  # fmt: skip
        lines.append("")
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("\n".join(lines))
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        tag = pins.RUN_PREFIX.rstrip("_") or "qwen36_27b"
        (out / f"{tag}_plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
        (out / f"{tag}_prompts.md").write_text("\n".join(lines) + "\n")
        print("wrote", out / f"{tag}_plan.json", out / f"{tag}_prompts.md")
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, orders: tuple[str, ...] = ORDERS, n_gen: int = Q.N_GEN) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.6 reads chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MODELS, f"49.6 runs on {MODELS}, not {target}"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "test": TEST,
         "spec": f"jobs/c3/batch49.yaml ({TEST})", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(SPEC.relative_to(pins.REPO_ROOT)): X.sha256_of(SPEC)},
         "scenes": f"47.10's: x6_routes.scenes C0 (seed {R.SEED}), {n_gen} generated, x47_report.build_items' drops; O only",
         "orders": {o: Q.ORDER_TEXT[o] for o in orders}, "wordings": {w: {"question": QUESTIONS[w], "kind": KIND[w]}
                                                                      for w in WORDINGS},
         "read": "X0's chat read (47.10's): a digit wording with the space token appended, the word wording right "
                 "after 'Answer:'; said = 47.10's said on 8 greedy tokens; read = the top token is the answer token; "
                 "cand = the highest of the three answer tokens",
         "reference": {"runs": REFERENCE, "what": "47.10's report / report_digit, question-last, O (competence.jsonl)"},
         "rule": "slot 1's read accuracy (question-last) <= 0.2 under both wordings on the 9B: keep as an appendix "
                 "curiosity; above 0.2 under either: drop",
         "seeds": {"scenes": R.SEED, "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no rates in the run; closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = build_items(tok, n_gen, orders)
    counts["target"] = target
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    cand = {k: torch.tensor(v, device=model.device) for k, v in candidates(tok).items()}
    rows = []
    with torch.no_grad():
        for it in progress(items, f"{TEST} reads (item)"):
            for o in orders:
                for w in WORDINGS:
                    rd = it["orders"][o][w]
                    text = model.generate_batch(torch.tensor([rd["ids"]], device=model.device), X.GEN_TOKENS, [{}])[0]
                    lg = X.read_logits(model, rd["ids"], [{}], "chat", Q.suffix(tok, rd["kind"]), ws)[0][0]
                    top = int(lg.argmax())
                    pref = int(lg[cand[rd["kind"]]].argmax())
                    s = Q.said(text, rd["kind"])
                    rows.append({"scene": it["scene"], "entity": it["entity"], "order": o, "wording": w,
                                 "slot": it["slot"] + 1, "greedy": text, "said": s, "said_right": int(s == rd["answer"]),
                                 "said_locker": int(rd["kind"] == "digit" and s == it["locker"]),
                                 "top": top, "top_text": tok.decode([top]), "read_right": int(top == rd["tok_A"]),
                                 "cand_slot": pref + 1, "cand_right": int(pref == it["slot"])})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    print("wrote", out, "(sealed: reads only)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q49.6 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def by_slot(rows: list[dict], measures: tuple[str, ...], n_boot: int) -> dict[str, Any]:
    """Per true slot and measure, the share right with a cluster-bootstrap CI over bridge items; all slots beside."""
    out: dict[str, Any] = {}
    for slot in (*SLOTS, "all"):
        mine = [r for r in rows if slot == "all" or str(r["slot"]) == slot]
        if not mine:
            out[slot] = {"n": 0, **{k: [math.nan] * 3 for k in measures}}
            continue
        flags = {k: [int(r[FIELD[k]]) for r in mine] for k in measures}
        rr = X.resampled_rates(flags, [r["entity"] for r in mine], n_boot)
        out[slot] = {"n": len(mine), **{k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in flags.items()}}
    return out


def confusion(rows: list[dict]) -> dict[str, dict[str, int]]:
    """True slot -> the slot the candidate read prefers -> count."""
    out: dict[str, dict[str, int]] = {s: dict.fromkeys(SLOTS, 0) for s in SLOTS}
    for r in rows:
        out[str(r["slot"])][str(r["cand_slot"])] += 1
    return out


def reference(target: str, n_boot: int) -> dict[str, Any] | None:
    """47.10's two wordings on the same scenes (question-last, O), by true slot, from its competence.jsonl."""
    path = Q.RESULTS / REFERENCE[target] / "competence.jsonl"
    if not path.exists():
        return None
    rows = X.read_jsonl(path)
    ents = {it["scene"]: it["entity"] for it in X.read_jsonl(path.parent / "cases.jsonl")}
    out = {}
    for w in OLD:
        mine = [{"slot": r["slot"] + 1, "entity": ents[r["scene"]], "said_right": int(r["right"]),
                 "read_right": int(r["read_right"]), "cand_right": int(r["cand_right"])}
                for r in rows if r["order"] == "last" and r["reader"] == w and r["variant"] == "org"]  # fmt: skip
        out[w] = by_slot(mine, MEASURES, n_boot)
    return out


def label_of(cells: dict[str, dict]) -> dict[str, Any]:
    """'stays' if slot 1's RULE_MEASURE accuracy <= RECOVER under both wordings, 'recovers' if above under either."""
    s1 = {w: cells[w]["1"][RULE_MEASURE][0] for w in WORDINGS}
    up = [w for w, v in s1.items() if v == v and v > RECOVER + EPS]
    label = "recovers" if up else "stays"
    return {"label": label, "slot1": s1, "measure": RULE_MEASURE, "recovers_under": up,
            "why": "; ".join(f"{w}: slot 1 {RULE_MEASURE} {v:.2f} {'>' if w in up else '<='} {RECOVER}"
                             for w, v in s1.items())}  # fmt: skip


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 49.6 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "why": "no outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    target = m["model"]["target"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    orders = {}
    for o in m["orders"]:
        cells = {w: by_slot([r for r in rows if r["order"] == o and r["wording"] == w],
                            (*MEASURES, "locker") if KIND[w] == "digit" else MEASURES, n_boot) for w in WORDINGS}  # fmt: skip
        conf = {w: confusion([r for r in rows if r["order"] == o and r["wording"] == w]) for w in WORDINGS}
        orders[o] = {"cells": cells, "confusion": conf, "rule": label_of(cells)}
    return {"run": run, "target": target, "status": "tested", "orders": orders, "reference": reference(target, n_boot),
            "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def decide(models: list[dict]) -> dict[str, Any]:
    """The action from the 9B's question-last label: stays -> appendix curiosity; recovers -> drop."""
    nine = next((m for m in models if m["target"] == HEADLINE[0] and m["status"] == "tested"), None)
    if nine is None or HEADLINE[1] not in nine["orders"]:
        return {"label": "pending", "action": "pending"}
    lab = nine["orders"][HEADLINE[1]]["rule"]["label"]
    return {"label": lab, "action": "keep as an appendix curiosity" if lab == "stays" else "drop",
            QUESTION: {"recovers": "yes", "stays": "no"}[lab]}  # fmt: skip


def fmt(v: list | None) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [mm["target"] for mm in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "why": "no run given"} for t in MODELS
               if t not in targets]  # fmt: skip
    v = decide(models)
    out = RESULTS / f"x49_6-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 49.6: the report of slot 1, reworded", "",
             f"Batch 49, test {TEST} (jobs/c3/batch49.yaml; {QUESTION}, Dan: {answer}). 47.10's C0 scenes, O only; two "
             "new wordings: " + "; ".join(f"{w} ({KIND[w]}) {QUESTIONS[w].format(p='<p>')!r}" for w in WORDINGS)
             + f". Accuracy by the asked item's true slot: {RULE_MEASURE} (decides: 47.10's gate measure), the others "
             f"beside. Cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             "Rule (fixed in advance): if slot 1 stays <= 0.2 on the 9B under both wordings, keep as an appendix "
             f"curiosity; if it recovers, drop. As computed: slot 1's {RULE_MEASURE} accuracy, question-last, point "
             "estimate.", "",
             f"**Verdict (9B, question-last): slot 1 {v['label']}; {v['action']}** ({QUESTION}: "
             f"{v.get(QUESTION, 'pending')}).", "",
             "| model | order | recovers under | label | why |", "|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            lines.append(f"| {mm['target']} | | | pending ({mm['why']}) | |")
            continue
        for o, r in mm["orders"].items():
            lines.append(f"| {mm['target']} | {o} | {r['rule']['recovers_under'] or 'none'} | {r['rule']['label']} | "
                         f"{r['rule']['why']} |")  # fmt: skip
    lines += ["", "Accuracy by true slot (said / read / candidate; 'locker' = the share that says the asked item's "
              "locker digit, the digit wording only); 47.10's wordings on the same scenes (question-last) as the "
              "reference.", "", "| model | order | wording | measure | slot 1 | slot 2 | slot 3 | all |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            continue
        blocks = [(o, w, c) for o, r in mm["orders"].items() for w, c in r["cells"].items()]
        blocks += [("last", f"47.10 {w}", c) for w, c in (mm["reference"] or {}).items()]
        for o, w, c in blocks:
            for k in (k for k in FIELD if k in c["all"]):
                lines.append(f"| {mm['target']} | {o} | {w} | {k} | " + " | ".join(
                    f"{fmt(c[s][k])} (n {c[s]['n']})" for s in (*SLOTS, "all")) + " |")  # fmt: skip
    lines += ["", "The candidate read's confusion (rows: true slot; columns: the slot the model prefers).", "",
              "| model | order | wording | true slot | 1 | 2 | 3 |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if mm["status"] != "tested":
            continue
        for o, r in mm["orders"].items():
            for w, conf in r["confusion"].items():
                for s in SLOTS:
                    lines.append(f"| {mm['target']} | {o} | {w} | {s} | "
                                 + " | ".join(str(conf[s][p]) for p in SLOTS) + " |")  # fmt: skip
    (out / "x49_6.json").write_text(json.dumps({"runs": runs, "dan": answer, "verdict": v, "models": models},
                                               indent=1, default=str) + "\n")  # fmt: skip
    (out / "x49_6.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(name: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> Path:
    """The verify-pack view: k random items (seed 0), each wording's prompt as the model reads it, the answer, the
    greedy text, the top token and the slot the candidate read prefers."""
    assert dan_answer(), f"sealed: {PREDICTIONS} has no committed answer to {QUESTION}"
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["order"], r["wording"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    out = src / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# 49.6 view: {name}", "", f"Model {m['model']['target']}. {min(k, len(items))} random items of "
             f"{len(items)} (seed {seed}); prompts exactly as the model reads them, the read suffix appended. "
             "UNVERIFIED.", ""]  # fmt: skip
    for i in Q.example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"## {it['scene']}: {it['asked']} picked {it['entity']}, its locker in slot {it['slot'] + 1}", ""]
        for o, rds in it["orders"].items():
            for w, rd in rds.items():
                r = reads[(it["scene"], o, w)]
                lines += [f"**[{o}] {w}**: answer {rd['answer']!r}; said {r['said']!r} (greedy {r['greedy']!r}); top "
                          f"token {r['top_text']!r}; candidate prefers slot {r['cand_slot']}", "", "```",
                          marked(decode, rd), "```", ""]  # fmt: skip
    (out / "examples.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run / view: the run name (results/x49_report/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 49.6 runs (27B, 9B)")
    ap.add_argument("--why", default=f"batch 49, test {TEST} (jobs/c3/batch49.yaml; {QUESTION})")
    ap.add_argument("--orders", default=",".join(ORDERS), help="plan / run: question orders (last[,first])")
    ap.add_argument("--n-gen", type=int, default=Q.N_GEN)
    ap.add_argument("--out", type=Path, default=None, help="plan: write the counts and the prompts into this folder")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    orders = tuple(o for o in a.orders.split(",") if o)
    assert set(orders) <= set(Q.ORDERS), f"--orders {orders}: of {Q.ORDERS}"
    assert len(set(orders)) == len(orders), f"--orders {orders}: an order twice"
    if a.stage == "plan":
        stage_plan(a.n_gen, out=a.out, orders=orders)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, orders, a.n_gen)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    else:
        assert a.name, "view needs --name"
        stage_view(a.name)


if __name__ == "__main__":
    main()
