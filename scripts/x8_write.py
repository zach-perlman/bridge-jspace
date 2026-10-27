"""x8_write (batch 44, Dan 26 Oct ~13:00): writing the pointer.

A (stage run): the routes test's original prompts O from its C2 items (x6_routes' generator, eligibility and gate), at
the layer fixed in advance; at the bridge word, h + s (mu_k - mu_j), mu = the layout-free class means behind the
pointer directions (x0_massmean.pointer_means, not refit), j = the bridge item's locker slot, both k != j in {0, 1, 2};
s in --s (1 primary; 2, 4 descriptive). Controls: h + a random direction of the same norm, one per write (seeded), for
s in --rand-s. --halfway: only the halfway writes (descriptive; j = 0: h + s (mu_2 - mu_0) / 2, j = 2: the reverse) at
s in --s. Read: X0's chat read, both readers; the lookup's answer classified as target (locker k's digit), original
(locker j's), third, other (halfway: by slot); the recall as changed or not. Also ||mu_k - mu_j|| against the median
||U U^T Delta|| of the real C2 changes (U: the pointer directions).
B (stage order): forward passes only. B1 = O with a neutral filler sentence before the first locker sentence, B2 = the
filler between the last locker sentence and the first pick sentence (fillers: a fixed list, no entity or digit, 10-12
tokens; Muse 8-16, --filler-tokens, its tokenizer has none of 10-12). Gate per variant: the lookup reads right in >= 0.80 of scenes. Per scene d = U U^T (h_variant - h_B0) at the
bridge word; beta = <d, mu_j' - mu_j> / ||mu_j' - mu_j||^2, j' = j + 1 (B1), j - 1 (B2, j in {1, 2}).
Verdicts (stage verdict / order-verdict): cluster bootstrap over bridge items (10,000 resamples, seed 0). UNVERIFIED.

uv run python scripts/x8_write.py run --name x8_write_27b                 # GPU, then the verdict
uv run python scripts/x8_write.py run --name x8_halfway_27b --halfway
uv run python scripts/x8_write.py order --name x8_order_27b
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x6_routes as R

EXP = "x8_write"
RESULTS = pins.RESULTS_DIR / EXP
SLOTS = (0, 1, 2)
CLASSES = ("target", "original", "third", "other")
RAND_SEED = 4401
N_ITEMS = R.N_ITEMS
FILLERS = (
    "The weather stayed mild and quiet for most of the afternoon.",
    "Everyone agreed that the meeting had gone on far too long.",
    "A light rain began to fall just after the doors were closed.",
    "Nobody could remember when the hallway lights had last been changed.",
    "The old radio in the corner played softly through the whole day.",
    "Somebody had left a pile of folded towels near the front desk.",
    "It was later than usual when the cleaning crew finally arrived.",
    "The windows on the north side had been open since early morning.",
)
LOCKER = re.compile(r"The locker of the (\w+) is (\d)\.")


def slots_of(context: str) -> list[tuple[str, int]]:
    """The locker sentences in order: (item, digit) per slot."""
    return [(m.group(1), int(m.group(2))) for m in LOCKER.finditer(context)]


def classify(top: int, tokens: dict[int, int], j: int, k: int | None) -> str:
    """The lookup's answer: target (slot k's digit), original (slot j's), third, other; tokens: slot -> digit token.
    Without k (halfway writes): the slot it landed on ('slot0' / 'slot1' / 'slot2') or other."""
    hit = [s for s, t in tokens.items() if t == top]
    if not hit:
        return "other"
    if k is None:
        return f"slot{hit[0]}"
    return "target" if hit[0] == k else "original" if hit[0] == j else "third"


def eligible(model, gate_min: float, n: int):
    """The routes test's C2 items, gate and eligibility exactly as x6_routes.stage_run."""
    import torch

    cases, _ = R.scenes(model.tokenizer, R.N_GEN)
    cases = [c for c in cases if c["condition"] == "C2"]
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(model.tokenizer), device="cuda")
    X.DIGIT_IDS.update(X.digit_ids(model.tokenizer))
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    gate = {"cases": len(cases), "org_read_accuracy": acc, "pass": all(a >= gate_min for a in acc.values()),
            "eligible": len(ok), "gate_min": gate_min}  # fmt: skip
    return (ok[:n] if gate["pass"] else []), gate, ws, digits


def real_doses(dose_from: str) -> dict[str, float]:
    """Batch 45c: each slot pair's s* ('j-k', j < k) from an x8 run's recall stage: the s at which a write reaches the
    median norm of a real pointer change; a dose d then writes s = d s*."""
    found = sorted((RESULTS / dose_from).glob("recall-*/recall.json"))
    assert found, f"{dose_from}: no recall stage (s*) to scale the doses by"
    return {k: float(v) for k, v in json.loads(found[-1].read_text())["s_real"].items()}


def stage_run(
    name: str,
    s_list: tuple[float, ...],
    rand_s: tuple[float, ...],
    halfway: bool,
    gate_min: float,
    pairs: tuple[tuple[int, int], ...] | None = None,
    dose_from: str | None = None,
) -> Path:
    """--pairs: write only these (j, k) moves (batch 45c: the second and third slots); --dose-from: s and rand_s are
    doses, multiples of each pair's s* from that x8 run (the row keeps the dose and the s written)."""
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import suite_v1 as S
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "layer": layer, "stage": "halfway" if halfway else "write",
         "s": list(s_list), "rand_s": [] if halfway else list(rand_s), "gate": gate_min, "gate_fixed_in_advance": X.GATE,
         "mu_from": R.STATES[target], "seeds": {"scenes": R.SEED, "random_directions": RAND_SEED},
         "pairs": [list(p) for p in pairs] if pairs else None, "dose_from": dose_from,
         "s_star": real_doses(dose_from) if dose_from else None,
         "note": "batch 44 (Dan 26 Oct ~13:00); results closed until its answers"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    chosen, gate, ws, _ = eligible(model, gate_min, N_ITEMS)
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    if not chosen:
        raise SystemExit(f"the gate missed or no eligible items: {gate}")
    mu = {k: torch.tensor(v, dtype=torch.float32, device="cuda") for k, v in MM.pointer_means(R.STATES[target]).items()}
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device="cuda")
    gen = torch.Generator().manual_seed(RAND_SEED)
    rows, deltas = [], []
    with torch.no_grad():
        for c in progress(chosen, f"writes at layer {layer} (scene)"):
            sl = slots_of(c["context"])
            j = [x for x, _ in sl].index(c["bridge"])
            tokens = {s: S.answer_token(tok, str(d), "digit") for s, (_, d) in enumerate(sl)}
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].float()
                 for v in ("org", "alt")}  # fmt: skip
            deltas.append(float(((h["alt"] - h["org"]).to("cuda") @ alf).norm()))
            arms = []  # (kind, k, s, vector)
            if halfway:
                if j in (0, 2):
                    far = 2 - j
                    arms += [("halfway", None, s, s * (mu[far] - mu[j]) / 2) for s in s_list]
            else:
                for k in (x for x in SLOTS if x != j and (pairs is None or (j, x) in pairs)):
                    step = mu[k] - mu[j]
                    star = m["s_star"][f"{min(j, k)}-{max(j, k)}"] if dose_from else 1.0
                    arms += [("write", k, s, s * star * step) for s in s_list]
                    for s in rand_s:
                        r = torch.randn(step.shape[0], generator=gen).to("cuda")
                        arms.append(("random", k, s, r / r.norm() * (s * star * step).norm()))
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(vec[None], [c["pos"]])} for *_, vec in arms]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for (kind, k, s, vec), lg in zip([("none", None, 0, None), *arms], logits, strict=True):
                    top = int(lg.argmax())
                    row = {"scene": c["scene"], "entity": c["bridge"], "reader": w, "kind": kind, "j": j, "k": k, "s": s,
                           "top": top, "norm": None if vec is None else round(float(vec.norm()), 4)}  # fmt: skip
                    if dose_from and k is not None:  # s is the dose; the s written is dose x s*
                        row["s_written"] = round(s * m["s_star"][f"{min(j, k)}-{max(j, k)}"], 4)
                    if w == X.LOOKUP:
                        row["class"] = classify(top, tokens, j, None if kind == "halfway" else k)
                    else:
                        row["changed"] = int(top != rd["tok_A"])
                    rows.append(row)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    m["items"] = len(chosen)
    m["norms"] = {"step": {f"{a}-{b}": round(float((mu[b] - mu[a]).norm()), 4) for a in SLOTS for b in SLOTS if a != b},
                  "median_U_UT_delta_C2": round(float(np.median(deltas)), 4)}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out, flush=True)
    return out


def shares(rows: list[dict], key: str, values: tuple[str, ...], n_boot: int) -> dict:
    """Per value, its share with a cluster-bootstrap interval over bridge items; the resamples for paired differences."""
    sw = {v: [int(r[key] == v) for r in rows] for v in values}
    rr = X.resampled_rates(sw, [r["entity"] for r in rows], n_boot)
    return {v: [float(np.mean(sw[v])), *X.interval(rr[v])] for v in values} | {"_r": rr, "n": len(rows)}


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lk = [r for r in rows if r["reader"] == X.LOOKUP]
    rc = [r for r in rows if r["reader"] == X.RECALL]
    blob: dict = {"run": name, "manifest": m, "cells": []}
    lines = [f"# Writing the pointer: {name}", "", f"Model {m['model']['target']}, layer {m['layer']}; {m.get('items')} "
             f"scenes; ||mu_k - mu_j||: {m.get('norms', {}).get('step')}; median ||U U^T Delta|| of the real C2 changes: "
             f"{m.get('norms', {}).get('median_U_UT_delta_C2')}. Cluster bootstrap over bridge items ({n_boot}). UNVERIFIED.", ""]  # fmt: skip
    if m["stage"] == "halfway":
        lines += [
            "| s | j | n | slot 0 | slot 1 | slot 2 | other | recall changed |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for s in m["s"]:
            for j in (0, 2):
                mine = [r for r in lk if r["kind"] == "halfway" and r["s"] == s and r["j"] == j]
                if not mine:
                    continue
                sh = shares(mine, "class", ("slot0", "slot1", "slot2", "other"), n_boot)
                ch = [r["changed"] for r in rc if r["kind"] == "halfway" and r["s"] == s and r["j"] == j]
                blob["cells"].append({"s": s, "j": j, **{k: v for k, v in sh.items() if k != "_r"}})
                lines.append(f"| {s} | {j} | {sh['n']} | {ci(sh['slot0'])} | {ci(sh['slot1'])} | {ci(sh['slot2'])} | "
                             f"{ci(sh['other'])} | {np.mean(ch):.2f} |")  # fmt: skip
    else:
        lines += ["| arm | s | (j, k) | n | target | original | third | other | recall changed |",
                  "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        pairs = [None] + [(j, k) for j in SLOTS for k in SLOTS if j != k]
        res: dict = {}
        for kind in ("write", "random"):
            for s in sorted({r["s"] for r in lk if r["kind"] == kind}):
                for pr in pairs:
                    mine = [
                        r for r in lk if r["kind"] == kind and r["s"] == s and (pr is None or (r["j"], r["k"]) == pr)
                    ]
                    if not mine:
                        continue
                    sh = shares(mine, "class", CLASSES, n_boot)
                    res[(kind, s, pr)] = sh
                    ch = [r["changed"] for r in rc if r["kind"] == kind and r["s"] == s
                          and (pr is None or (r["j"], r["k"]) == pr)]  # fmt: skip
                    blob["cells"].append({"kind": kind, "s": s, "pair": pr, "recall_changed": float(np.mean(ch)),
                                          **{k: v for k, v in sh.items() if k != "_r"}})  # fmt: skip
                    lines.append(f"| {kind} | {s} | {'all' if pr is None else pr} | {sh['n']} | {ci(sh['target'])} | "
                                 f"{ci(sh['original'])} | {ci(sh['third'])} | {ci(sh['other'])} | {np.mean(ch):.2f} |")  # fmt: skip
        q: dict = {}
        if ("write", 1, None) in res and ("random", 1, None) in res:
            w, r = res[("write", 1, None)], res[("random", 1, None)]
            diff = [w["target"][0] - r["target"][0], *X.interval(w["_r"]["target"] - r["_r"]["target"])]
            moved = [x for x in lk if x["kind"] == "write" and x["s"] == 1 and x["class"] in ("target", "third")]
            spec = float(np.mean([x["class"] == "target" for x in moved])) if moved else float("nan")
            per_pair = {f"{pr}": res[("write", 1, pr)]["target"][0] - res[("random", 1, pr)]["target"][0]
                        for pr in pairs[1:] if ("write", 1, pr) in res and ("random", 1, pr) in res}  # fmt: skip
            q = {"q44_1_target_minus_random": diff, "q44_1_pass": diff[0] >= 0.15 and diff[1] > 0,
                 "q44_2_moved": len(moved), "q44_2_specificity": spec, "q44_2_counts": len(moved) >= 30,
                 "q44_2_pass": len(moved) >= 30 and spec >= 0.80, "q44_3_per_pair": per_pair,
                 "q44_3_pass": len(per_pair) == 6 and all(v >= 0.10 for v in per_pair.values())}  # fmt: skip
            lines += ["", f"Q44.1: target minus random at s = 1: {ci(diff)} -> {'yes' if q['q44_1_pass'] else 'no'}.",
                      f"Q44.2: {len(moved)} writes move the lookup to another locker; target / (target + third) = {spec:.2f} "
                      f"-> {'counts, ' if q['q44_2_counts'] else 'does not count (< 30), '}{'yes' if q['q44_2_pass'] else 'no'}.",
                      "Q44.3: target minus random per (j, k): " + ", ".join(f"{k} {v:.2f}" for k, v in per_pair.items())
                      + f" -> {'yes' if q['q44_3_pass'] else 'no'}."]  # fmt: skip
        blob["questions"] = q
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, default=str) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def with_filler(context: str, filler: str, where: str) -> str:
    """B1 ('before'): the filler before the first locker sentence; B2 ('between'): after the last locker sentence."""
    sl = list(LOCKER.finditer(context))
    if where == "before":
        return context[: sl[0].start()] + filler + " " + context[sl[0].start() :]
    end = sl[-1].end()
    return context[:end] + " " + filler + context[end:]


def filler_lengths(tok) -> dict[str, int]:
    """Each filler's own tokens as inserted mid-prompt (after a space): no BOS. raw_encoding would add Muse's BOS, a token
    the inserted sentence does not have (that made every filler one token too long on Muse, 26 Oct)."""
    return {f: len(tok(" " + f, add_special_tokens=False)["input_ids"]) for f in FILLERS}


def stage_order(name: str, gate_min: float, filler_tokens: tuple[int, int] = (10, 12)) -> Path:
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.tokens import raw_encoding
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import tasks_v2 as T
    from scripts import x0_massmean as MM

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    model = load_model()
    tok = model.tokenizer
    lo, hi = filler_tokens
    n_tok = filler_lengths(tok)
    fillers = [f for f in FILLERS if lo <= n_tok[f] <= hi]
    assert fillers, f"no filler of {lo}-{hi} tokens for this tokenizer: {sorted(n_tok.values())}"
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "stage": "order",
         "model": pins.model_pin(), "code": git_state(), "layer": layer, "fillers": fillers, "gate": gate_min,
         "filler_tokens": [lo, hi],
         "mu_from": R.STATES[target], "note": "batch 44 B (Dan 26 Oct ~13:00); results closed until its answers"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    chosen, gate, ws, _ = eligible(model, gate_min, N_ITEMS)
    if not chosen:
        raise SystemExit(f"the gate missed or no eligible items: {gate}")
    mu = {k: torch.tensor(v, dtype=torch.float32, device="cuda") for k, v in MM.pointer_means(R.STATES[target]).items()}
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device="cuda")
    rows = []
    with torch.no_grad():
        for i, c in enumerate(progress(chosen, f"B variants at layer {layer} (scene)")):
            sl = slots_of(c["context"])
            j = [x for x, _ in sl].index(c["bridge"])
            rd = c["readers"][X.LOOKUP]
            asked = re.search(r"(\w+)'s pick", rd["question"]).group(1)  # type: ignore[union-attr]
            filler = fillers[i % len(fillers)]
            h, right = {}, {}
            for v, ctx in (("B0", c["context"]), ("B1", with_filler(c["context"], filler, "before")),
                           ("B2", with_filler(c["context"], filler, "between"))):  # fmt: skip
                text = T.render(tok, {"format": "prose", "kind": "digit", "context": ctx, "question": rd["question"]})
                enc = raw_encoding(tok, text, offsets=True)
                sent = f"{asked} picked the {c['bridge']}."
                w0 = text.index(ctx) + ctx.index(sent) + sent.index(c["bridge"])
                pos = SP.tokens_in(enc["offset_mapping"], w0, w0 + len(c["bridge"]))
                assert len(pos) == 1, (c["scene"], v)
                ids = list(enc["input_ids"])
                h[v] = (
                    model.run(torch.tensor([ids], device="cuda"), record=(layer,))[1][layer][pos[0]].float().to("cuda")
                )
                logits, _ = X.read_logits(model, ids, [{}], "chat", c["space"], ws)
                right[v] = int(int(logits[0].argmax()) == rd["tok_A"])
            row = {"scene": c["scene"], "entity": c["bridge"], "j": j, "filler": filler, "filler_tokens": n_tok[filler],
                   "right": right}  # fmt: skip
            for v, jp in (("B1", j + 1), ("B2", j - 1)):
                if jp < 0:
                    continue
                d = ((h[v] - h["B0"]) @ alf) @ alf.T
                step = mu[jp] - mu[j]
                row[v] = {
                    "beta": float(d @ step / (step @ step)),
                    "norm_d": float(d.norm()),
                    "norm_step": float(step.norm()),
                }
            rows.append(row)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    m["items"] = len(rows)
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out, flush=True)
    return out


def stage_order_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob: dict = {"run": name, "variants": {}}
    lines = [f"# Order, sentence index or distance: {name}", "", f"Model {m['model']['target']}, layer {m['layer']}; "
             f"{len(rows)} scenes. Cluster bootstrap over bridge items ({n_boot}). UNVERIFIED.", "",
             "| variant | lookup right (gate 0.80) | n | mean beta | ||d|| / ||mu_j' - mu_j|| (median) | shifted |",
             "|---|---|---|---|---|---|"]  # fmt: skip
    shifted = {}
    for v in ("B1", "B2"):
        acc = float(np.mean([r["right"][v] for r in rows]))
        mine = [r for r in rows if v in r]
        if acc < 0.80 or not mine:
            shifted[v] = None
            lines.append(f"| {v} | {acc:.2f} | {len(mine)} | not tested | | |")
            continue
        rr = X.resampled_rates({"beta": [r[v]["beta"] for r in mine]}, [r["entity"] for r in mine], n_boot)
        beta = [float(np.mean([r[v]["beta"] for r in mine])), *X.interval(rr["beta"])]
        ratio = float(np.median([r[v]["norm_d"] / r[v]["norm_step"] for r in mine]))
        shifted[v] = beta[0] >= 0.5 and beta[1] > 0
        blob["variants"][v] = {"lookup_right": acc, "n": len(mine), "beta": beta, "norm_ratio_median": ratio,
                               "shifted": shifted[v]}  # fmt: skip
        lines.append(f"| {v} | {acc:.2f} | {len(mine)} | {beta[0]:.2f} [{beta[1]:.2f}, {beta[2]:.2f}] | {ratio:.2f} | "
                     f"{'yes' if shifted[v] else 'no'} |")  # fmt: skip
    if None in shifted.values():
        reading = "(d) can't tell (a variant not tested)"
    else:
        reading = {(False, False): "(a) order", (True, False): "(b) sentence index / absolute position",
                   (False, True): "(c) distance", (True, True): "(d) both shift"}[(shifted["B1"], shifted["B2"])]  # fmt: skip
    blob["reading"] = reading
    lines += ["", f"Reading: {reading}."]
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def geometry(n_boot: int = 0) -> Path:
    """The pointer geometry (CPU, descriptive): per model the 5 class means, centered; PC1's share of their variance;
    Spearman between PC1 and slot order; the midpoint deviation ||mu_1 - (mu_0 + mu_2) / 2|| / ||mu_2 - mu_0||."""
    from scripts import x0_massmean as MM

    out = RESULTS / f"geometry-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    blob, lines = {}, ["# Pointer geometry: the 5 class means behind the pointer directions (descriptive)", "",
                       "| model | states | PC1 share | Spearman(PC1, slot) | midpoint deviation | ‖μ0 − μ1‖ | ‖μ0 − μ2‖ | ‖μ1 − μ2‖ |",
                       "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for target, run in R.STATES.items():
        mu = MM.pointer_means(run)
        ks = sorted(mu)
        x = np.stack([mu[k] for k in ks])
        xc = x - x.mean(0)
        u, s, _ = np.linalg.svd(xc, full_matrices=False)
        share = float(s[0] ** 2 / (s**2).sum())
        rho = float(np.corrcoef(np.argsort(np.argsort(u[:, 0])), ks)[0, 1])  # Spearman: Pearson on the ranks (no ties)
        mid = float(np.linalg.norm(mu[1] - (mu[0] + mu[2]) / 2) / np.linalg.norm(mu[2] - mu[0]))
        dist = {f"{a}-{b}": float(np.linalg.norm(mu[a] - mu[b])) for a, b in ((0, 1), (0, 2), (1, 2))}
        blob[target] = {"states": run, "pc1_share": share, "spearman_pc1_slot": rho, "midpoint_deviation": mid,
                        "distances": dist, "variance_shares": (s**2 / (s**2).sum()).tolist()}  # fmt: skip
        lines.append(f"| {target} | {run} | {share:.2f} | {rho:.2f} | {mid:.2f} | "
                     + " | ".join(f"{d:.2f}" for d in dist.values()) + " |")  # fmt: skip
    (out / "geometry.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "geometry.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


ROUTES_OF = {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b",
             "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_g75", "muse-glimmer-30b": "muse30b_x6_routes"}  # fmt: skip
RECALL_CLASSES = ("target", "third", "original", "other")


def recall_item(digit: str, slots: list[tuple[str, int]], legs: dict[str, int], j: int, k: int) -> str:
    """Whose legs a changed recall gives: the item at the target slot k, the third slot, the original slot j, or none
    (the first that matches, in that order)."""
    third = ({0, 1, 2} - {j, k}).pop()
    return next(
        (n for n, s in (("target", k), ("third", third), ("original", j)) if digit == str(legs[slots[s][0]])), "other"
    )


def stage_recall(name: str) -> Path:
    """After the data, descriptive (Dan 26 Oct ~14:50; CPU): the recall's changed answers by item: the legs of the item at
    the target slot, the third slot, the original slot, or other; the writes where the target item's legs equal the
    original's (there a followed pointer cannot show as a change); and per pair the dose s* = median ||U U^T Delta|| /
    ||mu_k - mu_j|| at which a write first reaches the norm of a real pointer change. x8 stores no prompts: the scenes
    are the C2 cases of the model's routes run (same generator, seed and gate), checked per scene by entity and slot."""
    from bridge_jspace.review import checks as RC
    from scripts import tasks_v2 as T

    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    target = m["model"]["target"]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {
        c["scene"]: c for c in X.read_jsonl(R.RESULTS / ROUTES_OF[target] / "cases.jsonl") if c["condition"] == "C2"
    }
    legs = T.DOMAINS["animals"].values
    bad = sum(1 for r in rows if r["kind"] == "none" and r["reader"] == X.LOOKUP and (
        r["scene"] not in cases or cases[r["scene"]]["bridge"] != r["entity"]
        or [x for x, _ in slots_of(cases[r["scene"]]["context"])].index(r["entity"]) != r["j"]))  # fmt: skip
    assert bad == 0, f"{bad} scenes do not match the routes run's C2 cases"
    tally: dict = collections.defaultdict(collections.Counter)
    same, pairs = 0, set()
    for r in rows:
        if r["reader"] != X.RECALL or r["kind"] not in ("write", "random"):
            continue
        slots = slots_of(cases[r["scene"]]["context"])
        if (r["scene"], r["k"]) not in pairs:
            pairs.add((r["scene"], r["k"]))
            same += legs[slots[r["k"]][0]] == legs[slots[r["j"]][0]]
        if r["changed"]:
            d = RC.piece(target, r["top"]).strip()
            tally[(r["kind"], r["s"])][recall_item(d, slots, legs, r["j"], r["k"])] += 1
    norms = m["norms"]
    s_real = {pair: norms["median_U_UT_delta_C2"] / step for pair, step in norms["step"].items()}
    out = src / f"recall-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# The recall under the writes, by item: {name}", "",
             "After the data, descriptive (Dan 26 Oct ~14:50). Changed recalls (top token not O's answer) by whose legs they "
             "give: the item at the target slot, the third slot, the original slot (first match in that order), other. "
             f"Scenes: the C2 cases of {ROUTES_OF[target]} (entity and slot checked on every scene). UNVERIFIED.", "",
             "| arm | s | changed recalls | target item | third item | original item | other |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for (kind, s), c in sorted(tally.items()):
        lines.append(f"| {kind} | {s:g} | {sum(c.values())} | " + " | ".join(str(c[x]) for x in RECALL_CLASSES) + " |")
    lines += ["", f"Writes whose target item has as many legs as the original: {same} of {len(pairs)} (a followed pointer "
              "cannot show as a changed recall there).", "",
              f"Dose at the norm of a real pointer change (median ||U U^T Delta|| = {norms['median_U_UT_delta_C2']}): s* = "
              + ", ".join(f"{p} {v:.2f}" for p, v in s_real.items())
              + f". The primary dose s = 1 was below it on {'every' if min(s_real.values()) > 1 else 'not every'} pair: a "
              "design error in batch 44, not a finding."]  # fmt: skip
    blob = {"run": name, "after_the_data": True, "cases_from": ROUTES_OF[target],
            "changed_by_item": {f"{k}|{s:g}": dict(c) for (k, s), c in sorted(tally.items())},
            "same_legs": [same, len(pairs)], "s_real": s_real, "median_real": norms["median_U_UT_delta_C2"]}  # fmt: skip
    (out / "recall.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "recall.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


KEEPONLY = {"qwen3.5-9b": "qwen35_9b_x6_routes_keeponly", "qwen3.6-27b": "x6_routes_keeponly_27b",
            "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_keeponly_g75", "muse-glimmer-30b": "muse30b_x6_routes"}  # fmt: skip
X8_RUN = {"qwen3.5-9b": "qwen35_9b_x8_write", "qwen3.6-27b": "x8_write_27b", "qwen3.5-122b-a10b": "qwen35_122b_x8_write_g75",
          "muse-glimmer-30b": "muse30b_x8_write"}  # fmt: skip
PAIRS = ((0, 1), (0, 2), (1, 2))
# batch 43's routes runs with the label-free pointer (P_cf, --alf-from; their no_alf / keep_alf arms remove / keep it)
PCF_ROUTES = {"qwen3.5-9b": "qwen35_9b_x6_routes_pcf", "qwen3.6-27b": "x6_routes_pcf_27b",
              "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_pcf_g75", "muse-glimmer-30b": "muse30b_x6_routes_pcf"}  # fmt: skip


def half_means(states_run: str, entities: set[str]) -> tuple[dict[int, np.ndarray], np.ndarray, list[dict]]:
    """x0_massmean.layout_free and pointer_means on the probe states of these bridge entities only (the layout groups'
    means taken within the half): the class means by locker-sentence index, the layout-free states and their items."""
    from scripts import x0_massmean as MM

    src = MM.P.RESULTS / states_run
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before" and it["entity"] in entities]
    h = np.load(src / "states.npz")["h"].astype(np.float64)[keep]
    kept = [items[i] for i in keep]
    group = [MM.P.layout(it["context"], it["pick_index"]) for it in kept]
    size = collections.Counter(group)
    multi = [j for j, g in enumerate(group) if size[g] > 1]
    res = h[multi].copy()
    for g in {group[j] for j in multi}:
        rows = [r for r, j in enumerate(multi) if group[j] == g]
        res[rows] -= res[rows].mean(0)
    its = [kept[j] for j in multi]
    idx = [int(it["locker_index"]) for it in its]
    return {k: res[[i for i, x in enumerate(idx) if x == k]].mean(0) for k in sorted(set(idx))}, res, its


def pointer_move(case: dict) -> tuple[int, int]:
    """Where the routes case's change moves the pointer: from the O bridge's locker slot (in O) to the S bridge's locker
    slot (in S), comparable with x8's write j -> k (Dan 26 Oct ~16:00)."""
    o, s = [x for x, _ in slots_of(case["context"])], [x for x, _ in slots_of(case["cf_context"])]
    return o.index(case["bridge"]), s.index(case["cf_bridge"])


MOVES_12 = ((1, 2), (2, 1))  # batch 45c: moves between the second and third locker


def cells_45c(rows: list[dict], cases: dict[str, dict], n_boot: int = X.N_BOOT) -> dict:
    """Batch 45c on one routes run (the restricted basis as the pointer part): over the C2 lookups whose pointer moves
    between the second and third locker, the position share per arm, the removal's cut (whole minus without the basis)
    with its cluster-bootstrap interval, and the rule's two clauses (fixed in advance, jobs/c3/batch45.yaml): removal
    halves position (without <= whole / 2, the cut's CI excluding 0) and keep-only gives at least 0.15 position."""
    arms = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand")
    lk = [r for r in rows if r["condition"] == "C2" and r["reader"] == X.LOOKUP and r["arm"] in arms]
    mine = sorted({r["scene"] for r in lk if pointer_move(cases[r["scene"]]) in MOVES_12})
    pos = {(r["scene"], r["arm"]): int(r["route"] == "position") for r in lk}
    ent = {r["scene"]: r["entity"] for r in lk}
    if not mine:
        return {"n": 0}
    sw = {a: [pos[(s, a)] for s in mine] for a in arms}
    r_ = X.resampled_rates(sw, [ent[s] for s in mine], n_boot)
    share = {a: float(np.mean(v)) for a, v in sw.items()}
    cut = [share["whole"] - share["no_alf"], *X.interval(r_["whole"] - r_["no_alf"])]
    halves = share["no_alf"] <= share["whole"] / 2 and cut[1] > 0
    keep = share["keep_alf"] >= 0.15
    # beside the rule (Dan 26 Oct ~21:20, not in it): the same clause for the random part of the basis' share
    rand_cut = [share["whole"] - share["no_alf_rand"], *X.interval(r_["whole"] - r_["no_alf_rand"])]
    rand_halves = share["no_alf_rand"] <= share["whole"] / 2 and rand_cut[1] > 0
    return {"n": len(mine), "position": share, "cut": cut, "halves": bool(halves), "keep_015": bool(keep),
            "found": bool(halves and keep), "rand_cut": rand_cut, "rand_halves": bool(rand_halves)}  # fmt: skip


def stage_score45c(routes: list[str], writes: list[str], n_boot: int = X.N_BOOT) -> Path:
    """Batch 45c over its models: the rule per routes run (cells_45c), the count of models where it holds, and,
    descriptive, the writes mu_k - mu_j between the second and third slot at doses 1-4 x a real change (target share).
    Unsealed only after Dan's predictions are committed."""
    out = RESULTS / f"score45c-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    f = lambda v: f"{v:.2f}"  # noqa: E731
    lines = ["# Batch 45c: second vs third (scored against the rule fixed in advance)", "",
             "| routes run | n | position: whole / without / random part / only it / only a random part | cut [CI] | halves | random part's cut [CI] | random part halves | keep >= 0.15 | found |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob, found = {}, 0
    for run in routes:
        src = R.RESULTS / run
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
        c = cells_45c(X.read_jsonl(src / "outcomes.jsonl"), cases, n_boot)
        blob[run] = c
        if not c["n"]:
            lines.append(f"| {run} | 0 | – | – | – | – | – | – | – |")
            continue
        found += c["found"]
        p, rc = c["position"], c["rand_cut"]
        lines.append(f"| {run} | {c['n']} | {f(p['whole'])} / {f(p['no_alf'])} / {f(p['no_alf_rand'])} / {f(p['keep_alf'])} / "
                     f"{f(p['keep_alf_rand'])} | {f(c['cut'][0])} [{f(c['cut'][1])}, {f(c['cut'][2])}] | {c['halves']} | "
                     f"{f(rc[0])} [{f(rc[1])}, {f(rc[2])}] | {c['rand_halves']} | {c['keep_015']} | {c['found']} |")  # fmt: skip
    lines += ["", f"Found on {found} of {len(routes)} models (Q45.6: all three / one or two / none). The random part's "
              "cut and halves are beside the rule, not in it (Dan 26 Oct ~21:20).", "",
              "## The writes between the second and third slot (descriptive)", "",
              "| write run | move | kind | dose | n | target share |", "|---|---|---|---|---|---|"]  # fmt: skip
    for run in writes:
        rows = [
            r for r in X.read_jsonl(RESULTS / run / "outcomes.jsonl") if r["reader"] == X.LOOKUP and r["kind"] != "none"
        ]
        for (j, k), kind, s in sorted({((r["j"], r["k"]), r["kind"], r["s"]) for r in rows}):
            got = [r["class"] == "target" for r in rows if (r["j"], r["k"], r["kind"], r["s"]) == (j, k, kind, s)]
            blob.setdefault(run, {})[f"{j}-{k}|{kind}|{s:g}"] = {"n": len(got), "target": float(np.mean(got))}
            lines.append(f"| {run} | {j} → {k} | {kind} | {s:g} | {len(got)} | {np.mean(got):.2f} |")
    (out / "score.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "score.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def stage_pairs() -> Path:
    """After the data, descriptive (Dan 26 Oct ~15:30, regrouped ~16:00; CPU): the slot pairs. (a) The address vectors'
    stability per pair: the class means refit on two halves of the probe states split by bridge entity (seed 0), cos(mu_k
    - mu_j) between the halves, and ||mu_k - mu_j|| against the pooled within-class SD of the layout-free states along
    that direction. (b) Per pointer move j -> k (the O bridge's slot -> the S bridge's slot, routes C2): the lookup's
    position share under the whole change, without the pointer directions, without a random part of their size (the
    routes run), and with only the pointer part or only a random part of its size (the keep-only run); beside it the
    mean-difference write j -> k at s = 4 (x8: target share)."""
    import random

    from scripts import x0_massmean as MM

    out = RESULTS / f"pairs-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    blob: dict = {"after_the_data": True}
    f = lambda v: "–" if v is None else f"{v:.2f}"  # noqa: E731
    stab = ["## (a) The address vectors per slot pair", "",
            "| model | pair | cos (half A, half B) | separation | ‖μk − μj‖ | within SD |", "|---|---|---|---|---|---|"]  # fmt: skip
    move = ["## (b) Per pointer move j -> k: the lookup's position share (routes C2) and the mean-difference write", "",
            "| model | move | n | whole | without the pointer | without its random part | only the pointer part | only a random part | x8 write s = 4: target | without P_cf | only P_cf |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for target, states in R.STATES.items():
        _, _, res, items, _ = MM.layout_free(states)
        mu = MM.pointer_means(states)
        idx = np.array([int(it["locker_index"]) for it in items])
        ents = sorted({it["entity"] for it in items})
        random.Random(0).shuffle(ents)
        halves = [
            half_means(states, set(ents[: len(ents) // 2]))[0],
            half_means(states, set(ents[len(ents) // 2 :]))[0],
        ]
        blob[target] = {"pairs": {}, "moves": {}}
        for j, k in PAIRS:
            d = mu[k] - mu[j]
            u = d / np.linalg.norm(d)
            sd = float(np.sqrt((np.var(res[idx == j] @ u) + np.var(res[idx == k] @ u)) / 2))
            da, db = halves[0][k] - halves[0][j], halves[1][k] - halves[1][j]
            cos = float(da @ db / np.linalg.norm(da) / np.linalg.norm(db))
            blob[target]["pairs"][f"{j}-{k}"] = {"cos_halves": cos, "separation": float(np.linalg.norm(d)) / sd,
                                                 "norm": float(np.linalg.norm(d)), "within_sd": sd}  # fmt: skip
            stab.append(
                f"| {target} | {j} ↔ {k} | {cos:.2f} | {np.linalg.norm(d) / sd:.2f} | {np.linalg.norm(d):.2f} | {sd:.2f} |"
            )
        x8 = sorted((RESULTS / X8_RUN[target]).glob("verdict-*/verdict.json"))
        cells = json.loads(x8[-1].read_text())["cells"] if x8 else []
        rows = []
        for run, arms in (
            (ROUTES_OF[target], ("whole", "no_alf", "no_alf_rand")),
            (KEEPONLY[target], ("keep_alf", "keep_alf_rand")),
        ):
            cases = {c["scene"]: c for c in X.read_jsonl(R.RESULTS / run / "cases.jsonl") if c["condition"] == "C2"}
            rows += [(pointer_move(cases[r["scene"]]), r) for r in X.read_jsonl(R.RESULTS / run / "outcomes.jsonl")
                     if r["condition"] == "C2" and r["reader"] == X.LOOKUP and r["arm"] in arms]  # fmt: skip
        pcf_rows = []
        pcf = R.RESULTS / PCF_ROUTES[target]
        if (pcf / "outcomes.jsonl").exists():
            cases = {c["scene"]: c for c in X.read_jsonl(pcf / "cases.jsonl") if c["condition"] == "C2"}
            pcf_rows = [(pointer_move(cases[r["scene"]]), r) for r in X.read_jsonl(pcf / "outcomes.jsonl")
                        if r["condition"] == "C2" and r["reader"] == X.LOOKUP and r["arm"] in ("no_alf", "keep_alf")]  # fmt: skip
        for j, k in ((a, b) for a in SLOTS for b in SLOTS if a != b):
            share, n = {}, 0
            for arm in ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand"):
                mine = [r for mv, r in rows if mv == (j, k) and r["arm"] == arm]
                share[arm] = float(np.mean([r["route"] == "position" for r in mine])) if mine else None
                n = max(n, len(mine))
            for arm in ("no_alf", "keep_alf"):
                mine = [r for mv, r in pcf_rows if mv == (j, k) and r["arm"] == arm]
                share[f"pcf_{arm}"] = float(np.mean([r["route"] == "position" for r in mine])) if mine else None
            wr = next((c for c in cells if c["kind"] == "write" and c["s"] == 4 and c["pair"] == [j, k]), None)
            blob[target]["moves"][f"{j}-{k}"] = {
                "n": n,
                "position": share,
                "x8_s4_target": wr["target"][0] if wr else None,
            }
            main = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand")
            move.append(f"| {target} | {j} → {k} | {n} | " + " | ".join(f(share[a]) for a in main)
                        + f" | {f(wr['target'][0] if wr else None)} | {f(share['pcf_no_alf'])} | {f(share['pcf_keep_alf'])} |")  # fmt: skip
    lines = ["# The slot pairs (after the data, descriptive)", "",
             "(a) cos between the two halves' mu_k - mu_j (probe states split by bridge entity, seed 0); separation = ||mu_k - "
             "mu_j|| / the pooled within-class SD of the layout-free states along that direction. (b) The routes test's C2 "
             "items grouped by the pointer's move, from the O bridge's locker slot to the S bridge's (Dan's correction, "
             "~16:00: the first version grouped by the two slots S swapped, which is not the pointer's move). UNVERIFIED.",
             "", *stab, "", *move, "",
             "Reading (Dan ~16:00): the pointer directions carry first slot vs the rest; the model also separates slots 1 and 2 "
             "(the whole change gives position answers there) but mostly outside the 4 pointer directions. Neither branch of "
             "the reading fixed before fits (that the mean-difference vector is our artefact, or that the model does not "
             "separate 1 and 2): a third outcome."]  # fmt: skip
    (out / "pairs.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "pairs.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "stage", choices=["run", "verdict", "order", "order-verdict", "geometry", "recall", "pairs", "score45c"]
    )
    ap.add_argument("--name")
    ap.add_argument("--s", nargs="+", type=float, default=[1, 2, 4])
    ap.add_argument("--rand-s", nargs="+", type=float, default=[1, 4])
    ap.add_argument("--halfway", action="store_true", help="run: only the halfway writes (descriptive)")
    ap.add_argument("--gate", type=float, default=X.GATE, help="the 122B: 0.75, after the data, as its routes runs")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--filler-tokens", nargs=2, type=int, default=[10, 12], metavar=("LO", "HI"),
                    help="order: the fillers' length window (Muse: 8 16, Dan ~16:40; no filler of 10-12 tokens)")  # fmt: skip
    ap.add_argument("--pairs", nargs="+", default=None, metavar="J-K", help="run: only these slot moves (45c: 1-2 2-1)")
    ap.add_argument("--dose-from", default=None, help="run: --s / --rand-s are doses x each pair's s* from this x8 run")
    ap.add_argument("--routes", nargs="+", default=[], help="score45c: the batch-45c routes runs")
    ap.add_argument("--writes", nargs="+", default=[], help="score45c: the batch-45c write runs")
    a = ap.parse_args()
    if a.stage == "run":
        pairs = tuple(tuple(int(v) for v in p.split("-")) for p in a.pairs) if a.pairs else None
        stage_run(a.name, tuple(a.s), tuple(a.rand_s), a.halfway, a.gate, pairs, a.dose_from)  # type: ignore[arg-type]
        if pairs is None and a.dose_from is None:  # batch 45c's writes stay sealed until Dan's predictions
            stage_verdict(a.name, a.n_boot)
    elif a.stage == "verdict":
        stage_verdict(a.name, a.n_boot)
    elif a.stage == "order":
        stage_order(a.name, a.gate, tuple(a.filler_tokens))
        stage_order_verdict(a.name, a.n_boot)
    elif a.stage == "order-verdict":
        stage_order_verdict(a.name, a.n_boot)
    elif a.stage == "recall":
        stage_recall(a.name)
    elif a.stage == "score45c":
        stage_score45c(a.routes, a.writes, a.n_boot)
    elif a.stage == "pairs":
        stage_pairs()
    else:
        geometry()


if __name__ == "__main__":
    main()
