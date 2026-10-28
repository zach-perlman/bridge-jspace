"""x48_route2 (batch 48, test 48.5; jobs/c3/batch48.yaml, design and rule fixed in advance; Q48.5 in
predictions/2026-10-28_dan.md): the recall's second route: can an address redirect a recall?

Scenes: each model's 45m run (x0_necessity --alt fresh), its items at the layer fixed in advance, kept where the new
item's locker sentence comes before the asked pick (x45p.select, the same items as 45p) and the asked (original)
item's locker sentence does too (x0_strata 'org locker vs asked pick' == before): locker-first for both items. The
scenes have four locker sentences (slots 0-3); j = the asked item's (the bridge's) locker slot in O.

O = the original prompt, S = the changed one. Every edit at L = X.PREDICTED, at the bridge token (c['pos']) of O's
prompt, one read per arm (X0's chat read, both readers):
  none    O unedited
  whole   h_S - h_O (45m's whole arm, rerun; a check against its stored outcome)
  a1      (i) the change minus its J++ part (signed OMP, k = 25, over the J++ lens atoms at L as X0 takes them)
  w<k>    (ii) a1 plus the pointer write s (mu_k - mu_j), s = 2, mu = x0_massmean.pointer_means of the model's probe
          states (x8_write's means, not refit), for each other slot k in 0-3 (three writes per scene, no seed)
  p<k>    (iii) the write alone
  r<k>    (iv) a1 plus a random vector of the write's norm (one draw per scene and k, seed 4401 as x8_write)
Reads: the recall's top token classified by the attribute it matches (the scene generator's facts, tasks_v2.DOMAINS):
the item at slot k's, the original item's, the changed (new) item's, other (first match in that order; every match
recorded). A write is informative when slot k's item is neither the original nor the changed item and its attribute
differs from both of theirs (else the answer cannot tell the written slot's item from a recall that did not move or
from the no-J++ residual); the rule counts informative writes only, all writes reported beside. The lookup beside:
its top token classified as slot k's locker number, the original's, the changed item's, another slot's, other.

Rule (stage verdict; recall, point estimates): a model holds if under (ii) the share of informative writes whose
recall names slot k's item is >= 0.3 and under (iv) <= 0.05 (EPS 1e-9); the batch holds on >= 2 of 3 models.
Cluster-bootstrap CIs over bridge items (10,000, seed 0) beside; (i) and (iii) beside as the baselines.

SEALED: the run writes no verdict. The verdict stage refuses until predictions/2026-10-28_dan.md holds Dan's Q48.5.

uv run python scripts/x48_route2.py plan                                              # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x48_route2.py run --name qwen35_9b_x48_route2    # GPU (sealed)
uv run python scripts/x48_route2.py verdict --runs qwen35_9b_x48_route2 x48_route2_27b muse30_x48_route2
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
from scripts import x8_write as W
from scripts import x45b_binding as B
from scripts import x45p as P

EXP = "x48_route2"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch48.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q48.5"
RUN_45M = P.RUN_45M
RUNS = {"qwen3.5-9b": "qwen35_9b_x48_route2", "qwen3.6-27b": "x48_route2_27b", "muse-glimmer-30b": "muse30_x48_route2"}
RENDERING = "chat"
S_WRITE = 2.0  # x8_write's s = 2: the write is 2 (mu_k - mu_j)
RAND_SEED = W.RAND_SEED  # 4401, one random vector per write, as x8_write
SLOTS = (0, 1, 2, 3)  # 45m's scenes have four locker sentences
BASE_ARMS = ("none", "whole", "a1")
KINDS = {"w": "write", "p": "alone", "r": "random"}  # arm prefix -> kind; w<k>, p<k>, r<k>
RECALL_CLASSES = ("slot_k", "original", "changed", "other")
LOOKUP_CLASSES = ("slot_k", "original", "changed", "other_slot", "other")
NAMES_MIN, RANDOM_MAX, MODELS_MIN = 0.3, 0.05, 2
EPS = 1e-9
RULE = ("the recall's second route is the address if under (ii) the recall names slot k's item in >= 0.3 of the "
        "informative writes with the random vector (iv) <= 0.05 (point estimates), on >= 2 of 3 models")  # fmt: skip
READER_NAME = P.READER_NAME
WORDS = {w: i for i, w in enumerate(("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"))}


# ---- scenes (tokenizer only) --------------------------------------------------------------------------------------


def number_of(s: str) -> int:
    """A locker number as the scene writes it: a digit ('2') or a word ('five')."""
    s = s.strip()
    return int(s) if s.isdigit() else WORDS[s]


def lockers(context: str) -> list[tuple[str, int]]:
    """The locker sentences in context order: (item, locker number) per slot."""
    out = []
    for sent, item in P.locker_items(context):
        m = B.LOCKER_RE.match(sent)
        assert m, sent
        out.append((item, number_of(m.group(2))))
    return out


def attributes(domain: str) -> dict[str, int]:
    """The domain's facts: item -> its number (legs, atomic number, position)."""
    from scripts import tasks_v2 as T

    return T.DOMAINS[domain].values


def arm_name(kind: str, k: int) -> str:
    return f"{kind}{k}"


def arms_of(ks: list[int]) -> list[str]:
    """The arms in read order: the base arms, then w<k>, p<k>, r<k> per slot k."""
    return [*BASE_ARMS, *(arm_name(kind, k) for k in ks for kind in KINDS)]


def parse_arm(arm: str) -> tuple[str, int | None]:
    """An arm's kind ('none' / 'whole' / 'a1' / 'write' / 'alone' / 'random') and its slot k (None for the base arms)."""
    if arm in BASE_ARMS:
        return arm, None
    return KINDS[arm[0]], int(arm[1:])


def writes_of(slots: list[tuple[str, int]], j: int, new_slot: int, attrs: dict[str, int]) -> list[dict]:
    """The writes of one scene: every other slot k, each with its item, its attribute and whether it is informative
    (slot k's item is neither the original nor the changed item, and its attribute differs from both of theirs)."""
    a_orig, a_new = attrs[slots[j][0]], attrs[slots[new_slot][0]]
    out = []
    for k in range(len(slots)):
        if k == j:
            continue
        item, _ = slots[k]
        a_k = attrs[item]
        out.append({"k": k, "item": item, "attribute": a_k, "locker": slots[k][1], "is_changed_slot": k == new_slot,
                    "informative": k != new_slot and a_k != a_orig and a_k != a_new})  # fmt: skip
    return out


def select(tok, run_45m: str, layer: int) -> tuple[list[dict], dict]:
    """The items: 45p's selection (the new item's locker before the asked pick, O and S the same but for the bridge
    word), kept where the original item's locker is before the asked pick too; each with its slots, j, the new item's
    slot, the domain's attributes and its writes. Counts beside 45p's."""
    base, counts = P.select(tok, run_45m, layer)
    out, org_order = [], collections.Counter()
    for it in base:
        org_order[it["features"]["org locker vs asked pick"]] += 1
        if it["features"]["org locker vs asked pick"] != "before":
            continue
        slots = lockers(it["context"])
        assert len(slots) == len(SLOTS), f"{it['scene']}: {len(slots)} locker sentences, not {len(SLOTS)}"
        names = [x for x, _ in slots]
        j, new_slot = names.index(it["entity"]), names.index(it["cf_bridge"])
        assert new_slot == it["new"]["index"], it["scene"]
        attrs = attributes(it["domain"])
        assert all(x in attrs for x in names), f"{it['scene']}: an item without a fact: {names}"
        rd = it["readers"][X.RECALL]
        assert rd["answer"] == str(attrs[it["entity"]]), f"{it['scene']}: O's recall answer is not the fact"
        assert rd["cf_answer"] == str(attrs[it["cf_bridge"]]), f"{it['scene']}: S's recall answer is not the fact"
        assert it["readers"][X.LOOKUP]["answer"] == str(slots[j][1]), (
            f"{it['scene']}: O's lookup answer is not slot j's"
        )
        writes = writes_of(slots, j, new_slot, attrs)
        out.append({**{k: v for k, v in it.items() if k not in ("new", "control", "marks")},
                    "marks": {"bridge": it["marks"]["bridge"]}, "slots": [list(s) for s in slots], "j": j,
                    "new_slot": new_slot, "attributes": {x: attrs[x] for x in names}, "writes": writes})  # fmt: skip
    n_w = sum(len(it["writes"]) for it in out)
    n_inf = sum(w["informative"] for it in out for w in it["writes"])
    counts = {**counts, "45p_items": counts["items"], "org locker vs asked pick": dict(org_order), "items": len(out),
              "entities": len({it["entity"] for it in out}), "writes": n_w, "informative_writes": n_inf,
              "j": dict(collections.Counter(it["j"] for it in out)),
              "uninformative_by_reason": dict(collections.Counter(
                  "the changed item's slot" if w["is_changed_slot"] else "the same attribute as the original's or "
                  "the changed item's" for it in out for w in it["writes"] if not w["informative"]))}  # fmt: skip
    return out, counts


def recall_class(digit: str, it: dict, k: int) -> tuple[str, list[str]]:
    """The recall's answer by whose attribute it gives: slot k's item, the original item, the changed item, other
    (the first match in that order), and every role it matches."""
    a = it["attributes"]
    slots = it["slots"]
    roles = (("slot_k", a[slots[k][0]]), ("original", a[it["entity"]]), ("changed", a[it["cf_bridge"]]))
    hit = [r for r, v in roles if digit == str(v)]
    return (hit[0] if hit else "other"), hit


def lookup_class(digit: str, it: dict, k: int) -> str:
    """The lookup's answer: slot k's locker number, the original item's, the changed item's, another slot's, other."""
    slots = it["slots"]
    numbers = {"slot_k": slots[k][1], "original": slots[it["j"]][1], "changed": slots[it["new_slot"]][1]}
    for role, n in numbers.items():
        if digit == str(n):
            return role
    return "other_slot" if any(digit == str(n) for _, n in slots) else "other"


def item_marked(it: dict, reader: str) -> str:
    """The reader's O prompt as the model reads it (the digit's space token appended), the bridge token (the write
    position) marked."""
    spans = [(a, b, "bridge") for a, b in it["marks"]["bridge"]]
    return P.marked(it["readers"][reader]["text"]["org"] + it["read_suffix"], spans)


def step_norms(mu: dict[int, Any]) -> dict[str, float]:
    """||mu_k - mu_j|| per ordered slot pair (numpy or torch rows)."""
    return {f"{j}-{k}": round(float(np.linalg.norm(np.asarray(mu[k] - mu[j], dtype=np.float64))), 4)
            for j in SLOTS for k in SLOTS if j != k}  # fmt: skip


def stage_plan() -> dict:
    """Tokenizer only: the target's items, drops, writes, the write norms (s = 2) and one example (seed 0)."""
    from scripts import x0_massmean as MM
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = select(tok, RUN_45M[pins.TARGET], layer)
    counts["target"] = pins.TARGET
    norms = step_norms(MM.pointer_means(R.STATES[pins.TARGET]))
    counts["write_norms_s2"] = {p: round(S_WRITE * v, 4) for p, v in norms.items()}
    if items:
        it = items[P.example_indices(len(items), 1)[0]]
        counts["example"] = {"scene": it["scene"], "bridge": it["entity"], "changed": it["cf_bridge"], "j": it["j"],
                             "slots": it["slots"], "writes": it["writes"],
                             "bridge_token": {it["pos"]: tok.decode([it["readers"][X.LOOKUP]["ids"]["org"][it["pos"]]])},
                             "recall_O_marked": item_marked(it, X.RECALL)}  # fmt: skip
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def edit_sets(add_rows, layer: int, pos: int, whole, base, steps: dict[int, Any], rands: dict[int, Any]) -> dict:
    """Each arm's edit set ({layer: add_rows(rows [1, d], [pos])}), in arms_of order: whole and base at the bridge
    token; per slot k the write (base + step), the write alone (step), the random control (base + rand)."""

    def at(row) -> dict:
        return {layer: add_rows(row[None], [pos])}

    out = {"none": {}, "whole": at(whole), "a1": at(base)}
    for k in steps:
        out[arm_name("w", k)] = at(base + steps[k])
        out[arm_name("p", k)] = at(steps[k])
        out[arm_name("r", k)] = at(base + rands[k])
    assert list(out) == arms_of(list(steps))
    return out


def random_like(step, gen) -> Any:
    """A random direction of the step's norm (x8_write's draw: torch.randn on the generator, then scaled)."""
    import torch

    r = torch.randn(step.shape[0], generator=gen).to(step.device)
    return r / r.norm() * step.norm()


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "48.5 renders 45m's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUN_45M, f"48.5 runs on {sorted(RUN_45M)}, not {target}"
    run_45m, layer = RUN_45M[target], X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / run_45m
    mu_np = MM.pointer_means(R.STATES[target])
    assert set(SLOTS) <= set(mu_np), f"pointer means for slots {sorted(mu_np)}, need {SLOTS}"
    norms = step_norms(mu_np)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "48.5",
         "spec": "jobs/c3/batch48.yaml (48.5)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")},
         "run_45m": run_45m, "layer": layer, "k": X.K_MAIN, "omp": "signed", "s": S_WRITE,
         "mu_from": R.STATES[target], "step_norms": norms,
         "write_norms": {p: round(S_WRITE * v, 4) for p, v in norms.items()},
         "arms": {"none": "O unedited", "whole": "h_S - h_O at the bridge token (45m's whole arm, rerun)",
                  "a1": "(i) the change minus its J++ part (k = 25, signed)",
                  "w<k>": "(ii) a1 plus s (mu_k - mu_j), s = 2", "p<k>": "(iii) the write alone",
                  "r<k>": "(iv) a1 plus a random vector of the write's norm"},
         "write_position": "the bridge token of O's prompt (c['pos']), every arm, at L",
         "slots": "each other slot k of the four (three writes per scene; j = the asked item's locker slot in O)",
         "items_rule": "45p's items (the new item's locker before the asked pick; O and S the same but for the bridge "
                       "word) whose original item's locker is before the asked pick too",
         "informative": "slot k's item is neither the original nor the changed item and its attribute differs from "
                        "both of theirs; the rule counts informative writes, all writes reported beside",
         "read": "X0's chat read: the prompt with a digit's space token appended; the recall's top token classified "
                 "by the attribute it matches (slot k's item / original / changed / other, first match); the lookup's "
                 "by locker number", "rule": RULE, "decisive_reader": X.RECALL,
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "random_directions": RAND_SEED,
                   "fresh_draws": X.FRESH_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, run_45m, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    mu = {k: torch.tensor(v, dtype=torch.float32, device=jdic.device) for k, v in mu_np.items()}
    gen = torch.Generator().manual_seed(RAND_SEED)
    examples = set(P.example_indices(len(items)))
    rows, norm_rows, greedy = [], [], []
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"48.5 at L{layer} (item)")):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][it["pos"]]
                 for v in ("org", "alt")}  # fmt: skip
            whole = (h["alt"] - h["org"]).float().to(jdic.device)
            part = X.fit(jdic, whole[None], X.K_MAIN, "signed")[0].float()
            base = whole - part
            j, ks = it["j"], [w["k"] for w in it["writes"]]
            steps = {k: S_WRITE * (mu[k] - mu[j]) for k in ks}
            rands = {k: random_like(steps[k], gen) for k in ks}  # one draw per write, in scene then slot order
            edits = edit_sets(AddRows, layer, it["pos"], whole, base, steps, rands)
            norm_rows.append({"scene": it["scene"], "whole_norm": round(float(whole.norm()), 4),
                              "whole_jpp_share": round(float(part.norm() ** 2 / whole.norm().clamp_min(1e-30) ** 2), 5),
                              "base_norm": round(float(base.norm()), 4),
                              "write_norm": {k: round(float(steps[k].norm()), 4) for k in ks},
                              "random_norm": {k: round(float(rands[k].norm()), 4) for k in ks}})  # fmt: skip
            for w, rd in it["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(edits.values()), RENDERING, it["space"], ws)
                for arm, lg in zip(edits, logits, strict=True):
                    top = int(lg.argmax())
                    kind, k = parse_arm(arm)
                    text = tok.decode([top])
                    row = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                           "arm": arm, "kind": kind, "j": j, "k": k, **X.read_row(lg, rd, digits),
                           "right": int(top == rd["tok_A"]), "top_text": text}  # fmt: skip
                    if k is not None:
                        wr = next(x for x in it["writes"] if x["k"] == k)
                        row["informative"] = wr["informative"]
                        if w == X.RECALL:
                            row["class"], row["matches"] = recall_class(text.strip(), it, k)
                        else:
                            row["class"] = lookup_class(text.strip(), it, k)
                    rows.append(row)
                if i in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, list(edits.values()))
                    greedy += [{"scene": it["scene"], "reader": w, "arm": arm, "greedy": t}
                               for arm, t in zip(edits, texts, strict=True)]  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norm_rows)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q48.5 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return m.group(1).strip() if m else ""


def write_table(rows: list[dict], items: list[dict], reader: str) -> list[dict]:
    """One row per write (scene, k) for the reader: the entity, informative, and each kind's class under that k
    (write / alone / random from their own arms; 'base' = a1's answer classified against this k, the (i) baseline)."""
    by = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    out = []
    for it in items:
        for w in it["writes"]:
            k = w["k"]
            a1 = by[(it["scene"], reader, "a1")]
            text = a1["top_text"].strip()
            base = recall_class(text, it, k)[0] if reader == X.RECALL else lookup_class(text, it, k)
            cls = {kind: by[(it["scene"], reader, arm_name(pre, k))]["class"] for pre, kind in KINDS.items()}
            out.append({"scene": it["scene"], "entity": it["entity"], "k": k, "j": it["j"],
                        "informative": w["informative"], "base": base, **cls})  # fmt: skip
    return out


def numbers(table: list[dict], classes: tuple[str, ...], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """Per kind (base / write / alone / random) the share of each class over the writes, with cluster-bootstrap CIs
    over bridge items (the same draws for every kind and class: paired), and write minus random for 'slot_k'."""
    kinds = ("base", *KINDS.values())
    n = len(table)
    if not n:
        return {"n": 0, "entities": 0}
    ents = [r["entity"] for r in table]
    hits = {f"{kd}|{c}": [int(r[kd] == c) for r in table] for kd in kinds for c in classes}
    boot = X.resampled_rates(hits, ents, n_boot, seed)
    share = {kd: {c: [float(np.mean(hits[f"{kd}|{c}"])), *X.interval(boot[f"{kd}|{c}"])] for c in classes}
             for kd in kinds}  # fmt: skip
    d = boot["write|slot_k"] - boot["random|slot_k"]
    diff = [share["write"]["slot_k"][0] - share["random"]["slot_k"][0], *X.interval(d)]
    return {"n": n, "entities": len(set(ents)), "share": share, "write_minus_random_slot_k": diff}


def rule(recall: dict) -> dict:
    """48.5 on one model's informative writes (point estimates): holds iff the recall names slot k's item in >= 0.3
    under the write and <= 0.05 under the random vector (EPS); no informative writes: not tested."""
    if not recall.get("n"):
        return {"status": "not tested", "holds": False, "why": "no informative writes"}
    w, r = recall["share"]["write"]["slot_k"][0], recall["share"]["random"]["slot_k"][0]
    ok_w, ok_r = w >= NAMES_MIN - EPS, r <= RANDOM_MAX + EPS
    why = (f"write names slot k's item {w:.3f} {'>=' if ok_w else '<'} {NAMES_MIN}; random {r:.3f} "
           f"{'<=' if ok_r else '>'} {RANDOM_MAX} ({recall['n']} informative writes)")  # fmt: skip
    return {"status": "tested", "holds": ok_w and ok_r, "write_ok": ok_w, "random_ok": ok_r, "why": why}


def batch_verdict(models: list[dict]) -> dict:
    """The rule over the models: holds once MODELS_MIN hold; does not hold once too few can still hold; else pending."""
    n_hold = sum(bool(m["holds"]) for m in models)
    n_pending = sum(m["status"] == "pending" for m in models)
    label = "holds" if n_hold >= MODELS_MIN else "does not hold" if n_hold + n_pending < MODELS_MIN else "pending"
    return {"label": label, QUESTION: {"holds": "yes", "does not hold": "no"}.get(label, "pending"),
            "models_holding": n_hold, "models": len(models),
            "per_model": {m["target"]: ("yes" if m["holds"] else "no" if m["status"] == "tested" else m["status"])
                          for m in models}}  # fmt: skip


def per_pair(table: list[dict], n_boot: int) -> dict[str, dict]:
    """Descriptive: the 'slot_k' numbers per (j, k) pair over the informative writes."""
    out = {}
    for j, k in sorted({(r["j"], r["k"]) for r in table}):
        mine = [r for r in table if (r["j"], r["k"]) == (j, k) and r["informative"]]
        if mine:
            out[f"{j}-{k}"] = numbers(mine, ("slot_k",), n_boot)
    return out


def agreement(items: list[dict], rows: list[dict]) -> dict:
    """Descriptive checks against the 45m run: the rerun whole and a1 arms against its stored whole and no_part."""
    by = {(r["scene"], r["reader"], r["arm"]): int(r["switched"]) for r in rows}
    out = {}
    for w in X.READERS:
        for arm in ("whole", "a1"):
            pairs = [(by[(it["scene"], w, arm)], it["stored"][arm][w]) for it in items if w in it["stored"][arm]]
            out[f"{READER_NAME[w]} {arm} vs 45m's stored {'whole' if arm == 'whole' else 'no_part'}"] = {
                "n": len(pairs), "agree": sum(a == b for a, b in pairs), "rerun": sum(a for a, _ in pairs),
                "stored": sum(b for _, b in pairs)}  # fmt: skip
    return out


def base_rates(rows: list[dict]) -> dict:
    """The base arms per reader: switch rate and right rate (none / whole / a1)."""
    out: dict = {}
    for w in X.READERS:
        for arm in BASE_ARMS:
            mine = [r for r in rows if r["reader"] == w and r["arm"] == arm]
            out[f"{READER_NAME[w]} {arm}"] = {"n": len(mine), "switched": float(np.mean([r["switched"] for r in mine])),
                                              "right": float(np.mean([r["right"] for r in mine]))}  # fmt: skip
    return out


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), or its numbers per reader (informative writes and all writes) and the
    rule on the recall's informative writes."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 48.5 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False,
                "why": "the run has no manifest or outcomes here"}  # fmt: skip
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "cases.jsonl")
    readers: dict = {}
    for w, classes in ((X.RECALL, RECALL_CLASSES), (X.LOOKUP, LOOKUP_CLASSES)):
        table = write_table(rows, items, w)
        inf = [r for r in table if r["informative"]]
        readers[READER_NAME[w]] = {"informative": numbers(inf, classes, n_boot), "all": numbers(table, classes, n_boot),
                                   "per_pair": per_pair(table, n_boot)}  # fmt: skip
    r = rule(readers["recall"]["informative"])
    norms = X.read_jsonl(src / "norms.jsonl")
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "run_45m": m["run_45m"], **r,
            "readers": readers, "base": base_rates(rows), "checks": agreement(items, rows),
            "write_norms": m.get("write_norms"), "whole_jpp_share_median": P.median([x["whole_jpp_share"] for x in norms]),
            "whole_norm_median": P.median([x["whole_norm"] for x in norms]),
            "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items of the run (seed 0): each reader's O prompt with the write position marked, the slots, each
    arm's top token, its class and greedy text."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {run}: {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in P.example_indices(len(items), k, seed):
        it = items[i]
        slots = ", ".join(f"slot {s} {x} (locker {n}, attribute {it['attributes'][x]})"
                          for s, (x, n) in enumerate(it["slots"]))  # fmt: skip
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} (slot {it['j']}) → {it['cf_bridge']} "
                  f"(slot {it['new_slot']}); {slots}; informative writes: "
                  + ", ".join(f"k = {w['k']}" for w in it["writes"] if w["informative"]) + "", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}; the "
                      "write position is the ⟦bridge:…⟧ token", "", "```", item_marked(it, w), "```", "",
                      "| arm | top token | class | switched | right | greedy |", "|---|---|---|---|---|---|"]  # fmt: skip
            for arm in arms_of([x["k"] for x in it["writes"]]):
                r = reads[(it["scene"], w, arm)]
                lines.append(f"| {arm} | {r['top_text']!r} | {r.get('class', '-')} | {r['switched']} | {r['right']} | "
                             f"{greedy.get((it['scene'], w, arm))!r} |")  # fmt: skip
            lines.append("")
    return lines


def fmt(v: list) -> str:
    return "-" if v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−"))  # fmt: skip


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    assert set(targets) <= set(RUN_45M), f"48.5 runs on {sorted(RUN_45M)}, not {sorted(set(targets) - set(RUN_45M))}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
               for t in RUN_45M if t not in targets]  # fmt: skip
    v = batch_verdict(models)
    out = RESULTS / f"{EXP}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 48.5: the recall's second route: can an address redirect a recall?", "",
             f"Batch 48, test 48.5 (jobs/c3/batch48.yaml; {QUESTION}, Dan: {answer}). 45m's locker-first scenes (both "
             "items' lockers before the asked pick; only the bridge token differs); every arm at the bridge token at the "
             "layer fixed in advance, on O. The recall's answer classified by the attribute it matches; the rule counts "
             f"the informative writes. Cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.",
             "", f"Rule (fixed in advance): {RULE}.", "",
             f"**Verdict: {v['label']}** ({QUESTION} {v[QUESTION]}; per model {v['per_model']}): {v['models_holding']} "
             f"of {v['models']} models hold (at least {MODELS_MIN} needed).", "",
             "| model | run | status | informative writes (items) | (ii) write: slot k | (iv) random: slot k | "
             "(i) no-J++ alone: slot k | (iii) write alone: slot k | write − random | holds |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {m['run']} | pending ({m['why']}) | | | | | | | |")
            continue
        rc = m["readers"]["recall"]["informative"]
        if not rc["n"]:
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} | 0 | | | | | | no |")
            continue
        s = rc["share"]
        lines.append(f"| {m['target']} | {m['run']} | {m['status']} | {rc['n']} ({rc['entities']}) | "
                     f"{fmt(s['write']['slot_k'])} | {fmt(s['random']['slot_k'])} | {fmt(s['base']['slot_k'])} | "
                     f"{fmt(s['alone']['slot_k'])} | {fmt(rc['write_minus_random_slot_k'])} | "
                     f"{'yes' if m['holds'] else 'no'} |")  # fmt: skip
    lines += ["", "Per reader and kind, every class (informative writes; the lookup beside the recall). Collateral: "
              "under (ii) the recall's 'original' share is the clean answer kept, 'changed' the no-J++ residual.", "",
              "| model | reader | kind | n | " + " | ".join(RECALL_CLASSES) + " | other_slot (lookup) |",
              "|---|---|---|---|" + "---|" * (len(RECALL_CLASSES) + 1)]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for w in ("recall", "lookup"):
            r = m["readers"][w]["informative"]
            if not r["n"]:
                continue
            for kd in ("base", *KINDS.values()):
                s = r["share"][kd]
                lines.append(f"| {m['target']} | {w} | {kd} | {r['n']} | " + " | ".join(fmt(s[c]) for c in RECALL_CLASSES)
                             + f" | {fmt(s['other_slot']) if 'other_slot' in s else '-'} |")  # fmt: skip
    lines += ["", "All writes (uninformative ones included; descriptive): the recall's slot k share per kind.", "",
              "| model | n | base | write | alone | random |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        a = m["readers"]["recall"]["all"]
        lines.append(f"| {m['target']} | {a['n']} | " + " | ".join(fmt(a["share"][kd]["slot_k"])
                                                                   for kd in ("base", *KINDS.values())) + " |")  # fmt: skip
    lines += ["", "Per slot pair j → k (informative writes; descriptive): the recall's slot k share under the write / "
              "the random vector.", "", "| model | pair | n | write | random |", "|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for pr, c in m["readers"]["recall"]["per_pair"].items():
            lines.append(f"| {m['target']} | {pr} | {c['n']} | {fmt(c['share']['write']['slot_k'])} | "
                         f"{fmt(c['share']['random']['slot_k'])} |")  # fmt: skip
    lines += ["", "Items, norms and checks (descriptive):", ""]
    for m in models:
        if m["status"] == "pending":
            continue
        p = m["plan"]
        lines.append(f"- {m['target']} ({m['run']}, from {m['run_45m']}, L{m['layer']}): {p['items']} items of 45p's "
                     f"{p['45p_items']} (original locker {p['org locker vs asked pick']}); {p['writes']} writes, "
                     f"{p['informative_writes']} informative (uninformative: {p['uninformative_by_reason']}); write norms "
                     f"s = 2: {m['write_norms']}; median change norm {m['whole_norm_median']}, median J++ share "
                     f"{m['whole_jpp_share_median']}; base arms: {m['base']}; checks: " + "; ".join(
                         f"{k}: {c['agree']} of {c['n']} agree (rerun {c['rerun']}, stored {c['stored']})"
                         for k, c in m["checks"].items()))  # fmt: skip
    (out / f"{EXP}.json").write_text(json.dumps({"runs": runs, "dan": answer, "verdict": v, "models": models},
                                                indent=1, default=str) + "\n")  # fmt: skip
    (out / f"{EXP}.md").write_text("\n".join(lines) + "\n")
    ex = ["# 48.5 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, where "
          "every arm is written. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x48_route2/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the runs (9B, 27B, Muse)")
    ap.add_argument("--why", default="batch 48, test 48.5 (jobs/c3/batch48.yaml; Q48.5)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        stage_verdict(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
