"""pointer_fair (D3b, batch 3, "fair C2"): at the depth where "lookups go around the lens" was measured, does a pointer
code steer the lookup where the lens push of the same size does not?

Background (UNVERIFIED): read_write (EXPERIMENTS rows 32, 37) found that at layers 32-40, on the tokens after the cue,
the J-lens reads a recalled bridge used for a lookup (memory → prompt) 95% of the time, but its push (bridge alt −
bridge org) switches <= 3% of answers at any size: "read without write". d3b_slot_direction_main_27b found that at
layer 48 a direction fitted to "which statement the question asks" (target minus current statement) does switch 37% of
memory → prompt answers where the lens push does not, but at another depth. This run puts both pushes in read_write's
cell, at the same sizes, aimed at the SAME answer: bridge alt's own statement digit.

Data and fits:
  pointer_v1 (animals, elements): memory → prompt (the lookup the claim is about), named → prompt (the entity named in
      the question), memory → memory (the null: nothing is looked up). The pointer direction is fitted on pointer_v1's
      fit set (memory → prompt; answered right; queried entity in a seeded half of each pool, as d3b_slot_direction_
      main_27b), per-token class means of the 5 asked statements at layers 32, 36, 40, at two token groups:
        after the cue   the question's last token ('?') and everything after it (instruction, template, 'Answer:'):
                        read_write's cell; the same tokens in every family, so one fit serves all three
        question words  the question's own tokens, cue included (memory → prompt only; one fit per topic, since the
                        cue phrases differ in length between topics)
  prompt → prompt (the animal suite, wording A: "Jack's pet is a cow. ... The cow's locker is 5. ... Which locker
      belongs to Jack's pet?"): its own pointer direction, per-token class means of the 3 locker statements on half the
      eligible scenes (seeded), pushed on the other half, at the tokens after the subject ('?' and after)
Pushes (added at the group's tokens; layers 32, 36, 40 one at a time and all three at once; 0.5, 1, 2, 4 times the
per-token size of the alt-prompt patch there: pointer_v1's alt prompt, the suite's C prompt):
  pointer   mean(bridge alt's statement) − mean(the asked statement), per token
  lens      the J++ direction v(bridge alt) − v(bridge org), the same at every token (read_write's push)
  random    a random direction per token, the pointer push's size;  shuffled: a direction fitted on shuffled labels
  patch     the alt prompt's hidden states pasted at those tokens (reference, not rescaled)
Both the pointer and the lens push predict the same answer: the digit of bridge alt's statement in the org prompt.
Every answer is also recorded as the index of the statement whose digit it is (for the overshoot analysis).
Intervals: an entity-cluster bootstrap (the queried entities resampled within each topic, 2000, seed 0); Wilson as well.

Decision rule (fixed before the 27B run). Deciding cell: memory → prompt, the tokens after the cue, layers 32, 36 and 40
at once, 1x the alt-prompt patch's size, topics pooled. "A pointer code steers the lookup where the lens push of the
same size does not, at the lens's depth" iff (a) the pointer push's rate of answers = bridge alt's statement digit has
an entity-bootstrap 95% lower bound >= 0.30, and (b) it exceeds both the lens push and the random push by >= 20 points
with each paired entity-bootstrap lower bound > 0. Valid only if the shuffled-label direction (memory → prompt) stays
at an upper bound <= 0.10 for that digit and the pointer push changes memory → memory answers with an upper bound
<= 0.10 (n >= 35 each). Second deciding cell, same rule: memory → prompt, the question words, layers 32-40 at once, 1x
(it says whether the pointer also acts at the question words). Reported, not decisive: each layer, each size, per
topic, named → prompt, prompt → prompt. Secondary, pre-registered (an exploratory post-hoc pattern on
d3b_slot_direction_main_27b): among the pointer push's answers in the deciding cell that are neither answer org nor the
target, the share on statements BEYOND the target (on the far side from the asked statement) against a uniform choice
among the off-target statements, and against the shuffled-label direction: "overshoot" iff the observed share exceeds
the uniform expectation with an entity-bootstrap lower bound > 0.

Stages:  run --name N --why W [...]   analyze --name N   figures --name N   examples --name N [--k 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from bridge_jspace.tokens import raw_encoding
from scripts import pointer_fit as PF
from scripts import pointer_probe as PP
from scripts import pointer_swap as PS
from scripts import suite_split as SP
from scripts import suite_v1 as S

EXP = "pointer_fair"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {
    "domains": ["animals", "elements"], "layers": [32, 36, 40], "scales": [0.5, 1.0, 2.0, 4.0],
    "n": {"RL": 150, "DL": 100, "RR": 100, "BL": 400}, "competence": "d3b_competence_400", "suite": True,
    "primary_scale": 1.0, "fit_limit": None,
}  # fmt: skip
CONDS = ("pointer", "lens", "random", "shuffled")
SPLIT_SEED, SHUFFLE_SEED, SAMPLE_SEED, NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 1, 0, 0, 0, 2000, 0
RATE_MIN, MARGIN, CONTROL_MAX = 0.30, 0.20, 0.10
FAMILY_WORDS = {"RL": "memory → prompt", "DL": "named → prompt", "RR": "memory → memory", "BL": "prompt → prompt"}
BATCH = PS.BATCH
LOCKER = re.compile(r"The (\w+)'s locker is (\d)\.")


# ---- pure helpers (tests/test_pointer_fair.py) ---------------------------------------------------------------------


def after_group(question: list[int], final: list[int]) -> list[int]:
    """The question's last token ('?') and every token after it: read_write's cell, the same in every family."""
    return question[-1:] + final


def locker_order(context: str) -> list[tuple[str, str]]:
    """(animal, digit) of the animal suite's locker statements, in the order the context states them."""
    return LOCKER.findall(context)


def beyond(a: int, j: int, k: int) -> bool:
    """Is statement k beyond the target j, on the far side from the asked statement a?"""
    return k > j if j > a else k < j


def overshoot_expectation(a: int, j: int, n: int) -> float:
    """Share of the off-target statements (not a, not j) that lie beyond j: the uniform null for one off-target answer."""
    off = [k for k in range(n) if k not in (a, j)]
    return sum(beyond(a, j, k) for k in off) / len(off) if off else math.nan


def answer_slot(digit: str | None, digits: list[str]) -> int | None:
    return digits.index(digit) if digit is not None and digit in digits else None


# ---- items ----------------------------------------------------------------------------------------------------------


def v1_items(cfg: dict) -> list[dict]:
    good = PF.eligible_main(cfg["competence"]) if cfg["competence"] else None
    rng = random.Random(SAMPLE_SEED)
    out = []
    for fam in ("RL", "DL", "RR"):
        for d in cfg["domains"]:
            its = [
                it
                for it in PF.PV.load_file(PF.PV.DATA / "main" / f"{d}_{fam}_e5f0.json")
                if good is None or it["id"] in good
            ]
            out += [its[i] for i in sorted(rng.sample(range(len(its)), min(cfg["n"][fam], len(its))))]
    return out


def suite_items(cfg: dict, tok) -> tuple[list[dict], list[dict]]:
    """The animal suite's prompt → prompt items (eligible), prepared, split into (fit half, push half) by scene."""
    its = S.load("BL", "A")
    if cfg["competence"]:
        ok: dict[str, list[bool]] = collections.defaultdict(list)
        for line in SP.competence_file("BL", "A").read_text().splitlines():
            r = json.loads(line)
            if r["family"] == "BL":
                ok[r["id"]].append(r["correct"])
        its = [it for it in its if ok.get(it["id"]) and all(ok[it["id"]])]
    its = its[: cfg["n"]["BL"]]
    out = []
    for it in its:
        c = {**it, **SP.prepare(it, tok)}
        rendered = S.render(tok, it["context"], it["question"])
        offs = raw_encoding(tok, rendered, offsets=True)["offset_mapping"]
        q0 = rendered.rindex("\n" + it["question"]) + 1
        q1 = q0 + len(it["question"])
        question = [i for i, (s, e) in enumerate(offs) if e > q0 and s < q1]
        final = [i for i, (s, _) in enumerate(offs) if s >= q1]
        order = locker_order(it["context"])
        animals = [a for a, _ in order]
        c |= {"after": after_group(question, final), "text": rendered, "offsets": [list(o) for o in offs],
              "locker_digits": [dg for _, dg in order], "asked": animals.index(it["bridge"]),
              "target": animals.index(it["cf_bridge"]), "query": it["bridge"], "alt_query": it["cf_bridge"],
              "domain": "animals"}  # fmt: skip
        out.append(c)
    names = sorted({c["scene"] for c in out})
    random.Random(SPLIT_SEED).shuffle(names)
    fit_scenes = set(names[: len(names) // 2])
    return [c for c in out if c["scene"] in fit_scenes], [c for c in out if c["scene"] not in fit_scenes]


def input_files(cfg: dict) -> list[Path]:
    files = [PF.PV.DATA / "fit" / f"{d}_RL_e5f0.json" for d in cfg["domains"]]
    files += [PF.PV.DATA / "main" / f"{d}_{f}_e5f0.json" for d in cfg["domains"] for f in ("RL", "DL", "RR")]
    if cfg["competence"]:
        files.append(PF.PV.RESULTS / cfg["competence"] / "items.jsonl")
    if cfg["suite"]:
        files.append(S.DATA / "BL.json")
        if cfg["competence"]:
            files.append(SP.competence_file("BL", "A"))
    return files


# ---- the run ----------------------------------------------------------------------------------------------------------


def fit_means(x: torch.Tensor, y: torch.Tensor, y_shuf: torch.Tensor, n_classes: int) -> dict[str, Any]:
    mu, m = PF.class_means(x, y, n_classes)
    mu_s, _ = PF.class_means(x, y_shuf, n_classes)
    return {"mu": mu, "m": m, "mu_shuf": mu_s}


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows

    pins.check_run_name(name)
    assert cfg["primary_scale"] in cfg["scales"], "the primary size must be one of the sizes"
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in input_files(cfg)},
                "entity_split": {d: {"fit": a, "held_out": b} for d, (a, b) in PF.pools(cfg["domains"]).items()},
                "seeds": {"split": SPLIT_SEED, "shuffle": SHUFFLE_SEED, "sample": SAMPLE_SEED, "null": NULL_SEED,
                          "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    layers = tuple(cfg["layers"])
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    split = PF.pools(cfg["domains"])
    # 1. pointer_v1 fit (after the cue: pooled; question words: per topic)
    feats: dict[tuple[str, str], dict[int, list[torch.Tensor]]] = collections.defaultdict(
        lambda: {la: [] for la in layers}
    )
    labels: dict[tuple[str, str], list[int]] = collections.defaultdict(list)
    preps = [
        (it, PS.prepare(it, tok)) for it in PF.fit_items({"domains": cfg["domains"], "fit_limit": cfg["fit_limit"]})
    ]
    by_len: dict[int, list[tuple[dict, dict]]] = collections.defaultdict(list)
    for it, p in preps:
        by_len[len(p["read_ids"]["base"])].append((it, p))
    for chunk in progress([g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)], "fit collect"):
        logits, rec = forward_rows(model, torch.tensor([p["read_ids"]["base"] for _, p in chunk], device="cuda"),
                                   [{}] * len(chunk), layers)  # fmt: skip
        for ri, (it, p) in enumerate(chunk):
            right = digit_tok.get(int(logits[ri].argmax())) == it["answer"]
            if (cfg.get("require_correct", True) and not right) or it["query"] not in split[it["domain"]][0]:
                continue
            g = p["groups"]
            for key, pos in (
                (("after", "all"), after_group(g["question"], g["final"])),
                (("question", it["domain"]), g["question"]),
            ):
                for la in layers:
                    feats[key][la].append(rec[la][ri, pos].half().cpu())
                labels[key].append(it["slots"]["query"])
    fits: dict[tuple[str, str], dict[int, dict[str, Any]]] = {}
    fit_info = []
    gen_s = torch.Generator().manual_seed(SHUFFLE_SEED)
    for key in feats:
        y = torch.tensor(labels[key], device="cuda")
        y_s = y[torch.randperm(len(y), generator=gen_s).to(y.device)]
        fits[key] = {la: fit_means(torch.stack(feats[key][la]).cuda().float(), y, y_s, PF.N_SLOTS) for la in layers}
        fit_info.append(
            {
                "group": key[0],
                "topic": key[1],
                "n": len(y),
                "per_statement": [int((y == c).sum()) for c in range(PF.N_SLOTS)],
            }
        )
    # 2. the animal suite's prompt → prompt fit (3 locker statements)
    bl_fit, bl_push = suite_items(cfg, tok) if cfg["suite"] else ([], [])
    if bl_fit:
        fx: dict[int, list[torch.Tensor]] = {la: [] for la in layers}
        fy = []
        for c in progress(bl_fit, "suite fit collect"):
            _, rec = forward_rows(model, torch.tensor([c["read_ids"]["clean"]], device="cuda"), [{}], layers)
            for la in layers:
                fx[la].append(rec[la][0, c["after"]].half().cpu())
            fy.append(c["asked"])
        y = torch.tensor(fy, device="cuda")
        y_s = y[torch.randperm(len(y), generator=gen_s).to(y.device)]
        fits[("after", "suite")] = {la: fit_means(torch.stack(fx[la]).cuda().float(), y, y_s, 3) for la in layers}
        fit_info.append(
            {"group": "after", "topic": "suite", "n": len(fy), "per_statement": [int((y == c).sum()) for c in range(3)]}
        )
    (out_dir / "fit.json").write_text(json.dumps({"fits": fit_info}, indent=2) + "\n")
    # 3. pushes
    out_f = open(out_dir / "outcomes.jsonl", "w")  # noqa: SIM115 - appended item by item, closed below
    cases: list[dict] = []
    n_rows = 0
    settings: list[tuple[Any, tuple[int, ...]]] = [(la, (la,)) for la in layers] + [("32-40", layers)]
    todo = [("v1", c) for c in v1_items(cfg)] + [("suite", c) for c in bl_push]
    for ci, (src, c) in enumerate(progress(todo, "push")):
        if src == "v1":
            p = PS.prepare(c, tok)
            g = p["groups"]
            groups = {"after": after_group(g["question"], g["final"])}
            if c["family"] == "RL":
                groups["question"] = g["question"]
            ids = [p["read_ids"]["base"], p["read_ids"]["dissoc"]]
            a, j = c["slots"]["query"], c["slots"]["identity"]
            digits = [str(d) for d in c["digits"]]
            target_digit, org = c["sources"]["dissoc"]["predictions"]["identity"], c["answer"]
            q_b, q_s = c["query"], c["sources"]["dissoc"]["query"]
            fit_key = {"after": ("after", "all"), "question": ("question", c["domain"])}
            text, offsets = p["text"], p["offsets"]
        else:
            groups = {"after": c["after"]}
            ids = [c["read_ids"]["clean"], c["read_ids"]["cf"]]
            a, j = c["asked"], c["target"]
            digits = c["locker_digits"]
            target_digit, org = c["cf_answer"], c["answer"]
            q_b, q_s = c["bridge"], c["cf_bridge"]
            fit_key = {"after": ("after", "suite")}
            text, offsets = c["text"], c["offsets"]
        _, rec = forward_rows(model, torch.tensor(ids, device="cuda"), [{}, {}], layers)
        pair = torch.tensor([model.concept_token(q_b), model.concept_token(q_s)], device="cuda")
        lens_dir = {la: (lambda v: v[1] - v[0])(lens.vectors(la, pair)) for la in layers}
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_003 * ci)
        jobs: list[tuple[dict, dict]] = [({"cond": "unedited", "group": None, "layer": None, "scale": None}, {})]
        for gname, pos in groups.items():
            ft = fits[fit_key[gname]]
            vec: dict[tuple[int, float, str], torch.Tensor] = {}
            for la in layers:
                size = (rec[la][1, pos] - rec[la][0, pos]).norm(dim=-1)
                for sc in cfg["scales"]:
                    pv = PF.matched(ft[la]["mu"][j] - ft[la]["mu"][a], sc * size)
                    vec[(la, sc, "pointer")] = pv
                    vec[(la, sc, "lens")] = PF.matched(lens_dir[la], sc * size)
                    vec[(la, sc, "random")] = PS.null_rows(pv, gen)
                    vec[(la, sc, "shuffled")] = PF.matched(ft[la]["mu_shuf"][j] - ft[la]["mu_shuf"][a], sc * size)
            for key, lay in settings:
                jobs.append(({"cond": "patch", "group": gname, "layer": key, "scale": None},
                             {la: PS.SetRows(rec[la][1, pos], pos) for la in lay}))  # fmt: skip
                for sc in cfg["scales"]:
                    for cn in CONDS:
                        jobs.append(({"cond": cn, "group": gname, "layer": key, "scale": sc},
                                     {la: PS.AddRows(vec[(la, sc, cn)], pos) for la in lay}))  # fmt: skip
        read = torch.tensor([ids[0]], device="cuda")
        base_top = -1
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            logits, _ = forward_rows(model, read, [e for _, e in chunk])
            for ri, (tags, _) in enumerate(chunk):
                top = int(logits[ri].argmax())
                if tags["cond"] == "unedited":
                    base_top = top
                dg = digit_tok.get(top)
                role = ("target" if dg == target_digit else "org" if dg == org else "context" if dg in digits else
                        "other_digit" if dg is not None else "other")  # fmt: skip
                out_f.write(json.dumps({"family": c["family"], "domain": c["domain"], "name": c["id"], "query": q_b,
                                        "asked": a, "target_slot": j, "n_statements": len(digits), **tags,
                                        "top": tok.decode([top]).strip(), "role": role, "changed": top != base_top,
                                        "answer_slot": answer_slot(dg, digits)}) + "\n")  # fmt: skip
                n_rows += 1
        cases.append({"id": c["id"], "family": c["family"], "domain": c["domain"], "query": q_b, "alt_query": q_s,
                      "asked": a, "target_slot": j, "digits": digits, "answer": org, "target_digit": target_digit,
                      "text": text, "context": c["context"],
                      "groups_chars": {gname: [offsets[pos[0]][0], offsets[pos[-1]][1]] for gname, pos in groups.items()}})  # fmt: skip
    out_f.close()
    PF.write_rows(out_dir / "cases.jsonl", cases)
    sm = summarise(load_rows(name), cfg)
    sm |= {"seconds": round(time.time() - t0), "edited_reads": n_rows}
    (out_dir / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(sm))
    print((out_dir / "summary.md").read_text())


def load_rows(name: str) -> list[dict]:
    return [json.loads(x) for x in (RESULTS / name / "outcomes.jsonl").read_text().splitlines()]


# ---- analysis ---------------------------------------------------------------------------------------------------------


def sel(rows: list[dict], **where) -> dict[str, dict]:
    return {o["name"]: o for o in rows if all(o.get(k) == v for k, v in where.items())}


def stat(c: dict[str, dict], key: str = "role", value: Any = "target") -> dict[str, Any]:
    """Rate of rows with row[key] == value: Wilson, entity-cluster bootstrap, n items, k entities."""
    rows = list(c.values())
    hits = [float(o[key] == value) for o in rows]
    return {"n": len(rows), "k_entities": len({(o["domain"], o["query"]) for o in rows}),
            "wilson": [round(v, 4) for v in wilson(int(sum(hits)), len(rows))] if rows else [math.nan] * 3,
            "entity_boot": [round(v, 4) for v in PP.entity_boot(hits, [o["domain"] for o in rows], [o["query"] for o in rows])]}  # fmt: skip


def paired_diff(c1: dict[str, dict], c2: dict[str, dict]) -> list[float]:
    names = sorted(set(c1) & set(c2))
    d = [float(c1[n]["role"] == "target") - float(c2[n]["role"] == "target") for n in names]
    return [round(v, 4) for v in PP.entity_boot(d, [c1[n]["domain"] for n in names], [c1[n]["query"] for n in names])]


def overshoot(c: dict[str, dict]) -> dict[str, Any]:
    """Off-target answers (a statement's digit, not answer org, not the target): share beyond the target vs uniform."""
    rows = [
        o for o in c.values() if o["answer_slot"] is not None and o["answer_slot"] not in (o["asked"], o["target_slot"])
    ]
    obs = [float(beyond(o["asked"], o["target_slot"], o["answer_slot"])) for o in rows]
    exp = [overshoot_expectation(o["asked"], o["target_slot"], o["n_statements"]) for o in rows]
    diff = PP.entity_boot(
        [x - e for x, e in zip(obs, exp, strict=True)], [o["domain"] for o in rows], [o["query"] for o in rows]
    )
    return {"n_off_target": len(rows), "beyond": int(sum(obs)), "expected_uniform": round(float(sum(exp)), 2),
            "beyond_minus_uniform": [round(v, 4) for v in diff]}  # fmt: skip


def summarise(rows: list[dict], cfg: dict) -> dict:
    sc = cfg["primary_scale"]
    out: dict[str, Any] = {"cells": {}}
    grouped: dict[tuple, dict[str, dict]] = collections.defaultdict(dict)
    for o in rows:
        if o["cond"] != "unedited":
            grouped[(o["family"], o["group"], o["layer"], o["scale"], o["cond"])][o["name"]] = o
    for (fam, group, layer, scale, cond), rows_c in grouped.items():
        cell = {"target": stat(rows_c), "changed": stat(rows_c, "changed", True)}
        for dom in sorted({o["domain"] for o in rows_c.values()}):
            cell[f"target:{dom}"] = stat({n: o for n, o in rows_c.items() if o["domain"] == dom})
        out["cells"][f"{fam}|{group}|{layer}|{scale}|{cond}"] = cell
    decisions = {}
    for group in ("after", "question"):

        def c(cond: str, fam: str = "RL", group: str = group) -> dict[str, dict]:
            return sel(rows, family=fam, group=group, layer="32-40", scale=sc, cond=cond)

        if not c("pointer"):
            continue
        ptr = stat(c("pointer"))
        d_lens, d_rand = paired_diff(c("pointer"), c("lens")), paired_diff(c("pointer"), c("random"))
        shuf = stat(c("shuffled"))
        rr = stat(sel(rows, family="RR", group="after", layer="32-40", scale=sc, cond="pointer"), "changed", True)
        ok = (
            ptr["entity_boot"][1] >= RATE_MIN
            and d_lens[0] >= MARGIN
            and d_rand[0] >= MARGIN
            and d_lens[1] > 0
            and d_rand[1] > 0
        )
        valid = (
            shuf["entity_boot"][2] <= CONTROL_MAX
            and shuf["n"] >= 35
            and rr["entity_boot"][2] <= CONTROL_MAX
            and rr["n"] >= 35
        )
        decisions[group] = {"pointer": ptr, "lens": stat(c("lens")), "random": stat(c("random")), "shuffled": shuf,
                            "memory_memory_changed": rr, "pointer_minus_lens": d_lens, "pointer_minus_random": d_rand,
                            "patch": stat(sel(rows, family="RL", group=group, layer="32-40", scale=None, cond="patch")),
                            "overshoot": overshoot(c("pointer")), "overshoot_shuffled": overshoot(c("shuffled")),
                            "verdict": ("the pointer steers where the lens push does not" if ok else "not shown")
                            + ("" if valid else " (controls failed or n too small: not interpretable)")}  # fmt: skip
    out["decisions"] = decisions
    return out


def summary_md(sm: dict) -> str:
    def r(x):
        b = x["entity_boot"]
        return f"{100 * b[0]:.0f}% [{100 * b[1]:.0f}, {100 * b[2]:.0f}] (n={x['n']}, k={x['k_entities']})"

    lines = [f"# {EXP}", ""]
    for group, d in sm["decisions"].items():
        where = "after the cue" if group == "after" else "question words"
        lines += [f"## memory → prompt, {where}, layers 32-40 at once, 1x: **{d['verdict']}**", "",
                  f"pointer {r(d['pointer'])}; lens {r(d['lens'])}; random {r(d['random'])}; shuffled {r(d['shuffled'])}; "
                  f"patch {r(d['patch'])}", f"memory → memory answers changed by the pointer: {r(d['memory_memory_changed'])}",
                  f"pointer - lens {d['pointer_minus_lens']}; pointer - random {d['pointer_minus_random']}",
                  f"overshoot: {json.dumps(d['overshoot'])}; shuffled: {json.dumps(d['overshoot_shuffled'])}", ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_analyze(name: str) -> Path:
    m = json.loads((RESULTS / name / "manifest.json").read_text())
    sm = summarise(load_rows(name), m["config"])
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(sm))
    print(out)
    return out


# ---- figures and examples ---------------------------------------------------------------------------------------------

COND_STYLE = {"pointer": ("#2a78d6", "-", "pointer push (bridge alt's statement − the asked one)"),
              "lens": ("#eb6834", "-", "lens push (bridge alt − bridge org)"),
              "random": ("#898781", "--", "control: random push (same size)"),
              "shuffled": ("#898781", ":", "control: shuffled-label direction")}  # fmt: skip


def stage_figures(name: str) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as PL

    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    cfg = m["config"]
    for old in d.glob("analysis-*-figures"):
        for f_ in old.iterdir():
            f_.unlink()
        old.rmdir()
    out = d / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    rows = load_rows(name)
    cases = [json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines()]
    sm = summarise(rows, cfg)
    model_name = m["model"]["repo"].split("/")[-1]
    figs: list[str] = []
    rl = next((c for c in cases if c["family"] == "RL"), None)
    ex = ""
    if rl:
        q = rl["text"][rl["text"].rindex("Which") :].split("?")[0] + "?"
        ex = (f"\"... {rl['context'][:80]}... {q}\" -> answer org {rl['answer']} (bridge org {rl['query']}); both pushes "
              f"aim at {rl['target_digit']}, the digit of bridge alt's statement ({rl['alt_query']}).")  # fmt: skip
    keys = [*cfg["layers"], "32-40"]
    xs = np.arange(len(keys))
    panels = [(fam, grp) for fam, grp in (("RL", "after"), ("RL", "question"), ("DL", "after"), ("BL", "after"))
              if sel(rows, family=fam, group=grp)]  # fmt: skip
    fig, axes = plt.subplots(len(panels), len(cfg["scales"]), figsize=(3.9 * len(cfg["scales"]), 3.1 * len(panels) + 0.4),
                             squeeze=False, sharey=True)  # fmt: skip
    for i, (fam, grp) in enumerate(panels):
        for jx, sc in enumerate(cfg["scales"]):
            ax = axes[i][jx]
            PL.style_axes(ax)
            PL.percent_axis(ax)
            for k_, cn in enumerate(CONDS):
                colour, ls, _ = COND_STYLE[cn]
                v = np.array([stat(sel(rows, family=fam, group=grp, layer=key, scale=sc, cond=cn))["entity_boot"]
                              if sel(rows, family=fam, group=grp, layer=key, scale=sc, cond=cn) else [math.nan] * 3 for key in keys], float)  # fmt: skip
                ax.errorbar(xs + (k_ - 1.5) * 0.08, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None),
                            color=colour, ls=ls, lw=2 if cn in ("pointer", "lens") else 1.2, marker="o", ms=4,
                            mfc=colour if cn in ("pointer", "lens") else PL.SURFACE, elinewidth=1, capsize=0)  # fmt: skip
            ax.set_xticks(xs, [str(k) if k != "32-40" else "all 3" for k in keys])
            ax.set_ylim(-0.04, 1.04)
            if i == 0:
                ax.set_title(f"{sc:g}x the alt-prompt patch's size", fontsize=9.5, color=PL.INK, loc="left")
            if jx == 0:
                where = (
                    ("after the subject" if fam == "BL" else "after the cue") if grp == "after" else "question words"
                )
                ax.set_ylabel(
                    f"{FAMILY_WORDS[fam]}, {where}\n% answers = bridge alt's statement", fontsize=8.5, color=PL.INK
                )
            if i == len(panels) - 1:
                ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
    handles = [Line2D([], [], color=c_, ls=ls, lw=2, marker="o", label=lab) for c_, ls, lab in COND_STYLE.values()]
    dec = sm["decisions"].get("after", {})
    explain = [("What we did", "At layers 32-40, where the lens reads the recalled word, pushed the tokens after the cue "
                               "(and the question words) along a fitted pointer to bridge alt's statement, or along the lens "
                               "direction bridge alt − bridge org, at the same size; both aim at the same digit."),
               ("Example", ex),
               ("How to read", f"Each dot: share of answers that become bridge alt's statement digit. Deciding cell "
                               f"(memory → prompt, after the cue, all 3 layers, 1x): '{dec.get('verdict', '-')}'."),
               ("Control", "Gray: a random push and a shuffled-label direction of the same size; memory → memory items "
                           "(nothing looked up) are reported in the summary.")]  # fmt: skip
    PF.save_fig(fig, out, "fig1_pointer_vs_lens_32_40", "Where the lens reads the word, does a pointer code steer the lookup when the lens push cannot?",
                explain, f"{model_name}; held-out scenes; error bars: bootstrap over the asked entities within each topic.",
                handles, ncols=2, figs=figs)  # fmt: skip
    (out / "summary.json").write_text(
        json.dumps({"run": name, "decisions": sm["decisions"], "figures": figs}, indent=2) + "\n"
    )
    print(out)
    return out


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    m = json.loads((d / "manifest.json").read_text())
    sc = m["config"]["primary_scale"]
    rows = load_rows(name)
    cases = {c["id"]: c for c in (json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines())}
    prim = sel(rows, family="RL", group="after", layer="32-40", scale=sc, cond="pointer")
    lens_c = sel(rows, family="RL", group="after", layer="32-40", scale=sc, cond="lens")
    groups = {"pointer_only": "the pointer push gives bridge alt's digit, the lens push does not",
              "both": "both give it", "neither": "neither gives it", "lens_only": "only the lens push gives it"}  # fmt: skip
    members: dict[str, list[str]] = {g: [] for g in groups}
    for n, o in prim.items():
        p_hit, l_hit = o["role"] == "target", lens_c.get(n, {}).get("role") == "target"
        members["both" if p_hit and l_hit else "pointer_only" if p_hit else "lens_only" if l_hit else "neither"].append(
            n
        )
    rng = np.random.default_rng(seed)
    examples = []
    for g, names in members.items():
        for n in (
            [names[i] for i in sorted(rng.choice(len(names), size=min(k, len(names)), replace=False))] if names else []
        ):
            c = cases[n]
            spans = PF.statement_spans(c["text"], c["context"])
            base = [{"start": spans[c["asked"]][0], "end": spans[c["asked"]][1], "role": "asked statement"},
                    {"start": spans[c["target_slot"]][0], "end": spans[c["target_slot"]][1], "role": "bridge alt's statement"},
                    {"start": c["groups_chars"]["after"][0], "end": c["groups_chars"]["after"][1], "role": "pushed tokens"}]  # fmt: skip
            for cn in ("pointer", "lens", "random", "shuffled"):
                o = sel(rows, name=n, family="RL", group="after", layer="32-40", scale=sc, cond=cn).get(n)
                if o is None:
                    continue
                examples.append({"group": g, "family": "RL", "item_id": n, "prompt": c["text"] + " ", "spans": base,
                                 "condition": f"{COND_STYLE[cn][2]}, layers 32-40, {sc:g}x the alt-prompt patch's size",
                                 "answers": {"clean": c["answer"], "edited": o["top"],
                                             "expected": {"H-pointer": c["target_digit"] if cn == "pointer" else c["answer"],
                                                          "H-lens": c["target_digit"] if cn == "lens" else c["answer"]}},
                                 "numbers": {"role": o["role"], "answer_statement": o["answer_slot"]},
                                 "why": groups[g]})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--domains", nargs="+", default=DEFAULTS["domains"])
    ap.add_argument("--layers", nargs="+", type=int, default=DEFAULTS["layers"])
    ap.add_argument("--scales", nargs="+", type=float, default=DEFAULTS["scales"])
    ap.add_argument(
        "--n",
        nargs=4,
        type=int,
        metavar=("RL", "DL", "RR", "BL"),
        default=None,
        help="items per topic for memory → prompt, named → prompt, memory → memory; scenes for prompt → prompt",
    )
    ap.add_argument("--competence", default=DEFAULTS["competence"])
    ap.add_argument("--no-eligibility", action="store_true", help="a smoke on another model: no competence filter")
    ap.add_argument("--keep-wrong", action="store_true", help="a smoke on a weak model: fit on wrong answers too")
    ap.add_argument("--no-suite", action="store_true", help="skip the animal suite's prompt → prompt items")
    ap.add_argument("--fit-limit", type=int, default=None)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        n = dict(zip(("RL", "DL", "RR", "BL"), args.n, strict=True)) if args.n else DEFAULTS["n"]
        stage_run(args.name, args.why, {"domains": args.domains, "layers": args.layers, "scales": args.scales, "n": n,
                                        "competence": None if args.no_eligibility else args.competence,
                                        "suite": not args.no_suite, "primary_scale": DEFAULTS["primary_scale"],
                                        "fit_limit": args.fit_limit, "require_correct": not args.keep_wrong})  # fmt: skip
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
