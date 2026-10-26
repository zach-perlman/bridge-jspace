"""x0b_generalize (X0b, jobs/c3/X0b.md; exploratory): does X0's lookup / recall contrast hold on a diverse set?

The X0 test (scripts/x0_necessity.py: Δ at the asked person's bridge word, arms whole / no_part / no_rand, J++ k = 25
signed OMP with the random-subspace part of its share, both readers on the identical patch, top-token read, chat) on a
tasks_v2 set with all 7 domains, levels 0-2 and the prose / json / table formats. The alt is built here for every
domain (Dan, 24 Oct evening): the asked person's pick becomes another person's pick in the scene (the first, by name,
whose locker and memory number both differ and whose name is one token at the bridge's position); nothing else
changes. Gate per cell (domain x format x level): unedited org accuracy under the decisive read >= 0.80 for both
readers; a failing cell is "can't test" and left out. Eligible: org and alt right for both readers (said and read), at
most CAP per cell, in scene order.

The rule (X0b.md v2, Dan 24 Oct ~19:30), pooled at the predicted layer, J++ k = 25: the lookup's excess and the
contrast C = recall excess - lookup excess (paired, bootstrap by entity): holds iff lookup excess <= 0.10 (upper CI <=
0.20) and C >= 0.20 (lower CI >= 0.10); fails iff lookup excess >= 0.20 or C's upper CI < 0.10; can't tell if a
reader's cell is invalid; else mixed. Descriptive: the k-curve (50, 100) at the predicted layer, the strata (format,
level, domain, locker order, number style), and probe (b) on the org states at the bridge's word (the bridge's locker
row ordinal among the locker statements, per format and order, cross-validated by entity).

45d (batch 45, jobs/c3/batch45.yaml; fixed in advance), `run --pcf-from x7_pcf/<fit>`: only the held-out half (per
format the bridge items of split.json's "test"), the predicted layer, and two more parts each against a random part of
its share: the format's label-free basis refit on the other half (dict "pcf", x7_pcf varied: pcf_<format>.npz) and the
simple-scene pointer basis U (dict "alf", not refit). The rule (pcf_rule) is on the lookup's extra loss with the refit
basis per format; `pcf-verdict` writes it, `examples` 10 random items (seed 0) with each arm's answer.

uv run python scripts/x0b_generalize.py plan --set x0b_v2                     # tokenizer only: cases and drops
uv run python scripts/x0b_generalize.py run --name x0b_27b --set x0b_v2        # GPU, then verdict and figures
uv run python scripts/x0b_generalize.py verdict --name x0b_27b                 # CPU
uv run python scripts/x0b_generalize.py run --name x45d_27b --no-curve --pcf-from x7_pcf/x45d_fit_27b  # GPU, 45d
uv run python scripts/x0b_generalize.py pcf-verdict --name x45d_27b            # CPU: 45d's rule and figure
uv run python scripts/x0b_generalize.py examples --name x45d_27b               # CPU (tokenizer): examples.json / .md
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from scripts import x0_necessity as X

EXP = "x0b_generalize"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "X0b.md"
LAYERS = {
    "qwen3.6-27b": (28, 30, 32, 34),
    "qwen3.5-9b": (10, 12, 14),
    "qwen3.5-122b-a10b": (33,),
    "muse-glimmer-30b": (26,),
}  # 122B: b6, L33 only; Muse: L26 only (fmt: skip)
CAP = 40  # eligible scenes per cell
CHUNK = 500  # cases per run_rendering call (the batched OMP's memory)
CELL = ("domain", "format", "level")
STRATA = ("format", "level", "domain", "order", "numbers")
K_CURVE = (50, 100)
HOLD_LOOKUP, HOLD_LOOKUP_HI, HOLD_C, HOLD_C_LO = 0.10, 0.20, 0.20, 0.10
FAIL_LOOKUP, FAIL_C_HI = 0.20, 0.10
# 45d (batch 45, fixed in advance): "pointer elsewhere" if the refit basis's lookup extra loss is >= 0.2 with lower CI
# > 0.1 in at least 2 of the 3 formats; "no linear pointer found" if all three point estimates are < 0.1
FORMATS = ("prose", "json", "table")
ELSEWHERE, ELSEWHERE_LO, ELSEWHERE_FORMATS, NONE_BELOW = 0.20, 0.10, 2, 0.10
PCF_RULE = ('"Pointer elsewhere" if the refit basis gives a lookup extra loss of at least 0.2, with lower CI above 0.1, '
            'in 2 of 3 formats; "No linear pointer found" if all three formats are below 0.1 (point estimate); '
            "otherwise neither.")  # fmt: skip
PARTS_45D = {"pcf": "the refit basis (rank 4, the other half)", "alf": "U (simple scenes, not refit)"}


def statements(item: dict, person: str, thing: str) -> tuple[str, str]:
    """The asked pick's statement and the start of the thing's locker statement, as tasks_v2 renders them."""
    from scripts import tasks_v2 as T

    fmt = item["format"]
    if fmt == "prose":
        ref = T.ref(T.DOMAINS[item["domain"]], thing)
        return f"{person} picked {ref}.", f"The locker of {ref} is "
    if fmt == "json":
        return json.dumps({"name": person, "pick": thing}), json.dumps({"item": thing})[:-1] + ', "locker": '
    assert fmt == "table", fmt
    return f"| {person} | {thing} |", f"\n| {thing} | "


def bridge_start(item: dict, context: str, thing: str) -> int:
    """The character offset of the bridge word in the asked person's pick statement (asserted to be once)."""
    person = item["facts"]["person"]
    pick, _ = statements(item, person, thing)
    assert context.count(pick) == 1, f"{item['id']}: {pick!r} is not once in the context"
    return context.index(pick) + pick.rindex(thing)


def order_of(item: dict) -> str:
    """'before' if the bridge's locker statement starts before the asked pick statement, else 'after'."""
    f = item["facts"]
    pick, locker = statements(item, f["person"], f["x"])
    ctx = item["context"]
    assert ctx.count(locker) == 1, f"{item['id']}: {locker!r} is not once in the context"
    return "before" if ctx.index(locker) < ctx.index(pick) else "after"


def ordinals(item: dict) -> dict:
    """Probe (b)'s target and baselines' keys: the bridge's locker statement's ordinal among the locker statements, the
    asked pick's ordinal among the pick statements (look-alikes included), and how many locker statements precede the
    asked pick, of how many (what the word can see of the layout)."""
    f, ctx = item["facts"], item["context"]
    lock = {t: ctx.index(statements(item, f["person"], t)[1]) for t in f["locker"]}
    picks = [*f["pick"].items(), *(tuple(p) for p in f["lookalike_picks"])]
    at = {p: ctx.index(statements(item, p, t)[0]) for p, t in picks}
    asked = at[f["person"]]
    return {"locker_index": sorted(lock.values()).index(lock[f["x"]]), "pick_index": sorted(at.values()).index(asked),
            "layout": f"{sum(o < asked for o in lock.values())}/{len(lock)}"}  # fmt: skip


def rule(lookup: dict, recall: dict, c: list[float]) -> str:
    """X0b's pooled rule: holds / fails / mixed / can't tell (module docstring)."""
    if not (lookup["valid"] and recall["valid"]):
        return "can't tell"
    ex, _, ex_hi = lookup["excess"]
    if ex <= HOLD_LOOKUP and ex_hi <= HOLD_LOOKUP_HI and c[0] >= HOLD_C and c[1] >= HOLD_C_LO:
        return "holds"
    if ex >= FAIL_LOOKUP or c[2] < FAIL_C_HI:
        return "fails"
    return "mixed"


def contrast(rows: list[dict], layer: int, spec: tuple, n_boot: int) -> list[float]:
    """C = recall excess - lookup excess at one layer and dictionary spec, on the same items and the same resamples."""
    got = {(r["scene"], r["reader"], r["arm"] if r["arm"] == "whole" else (r["dict"], r["k"], r["omp"], r["arm"])):
           r["switched"] for r in rows if r["layer"] == layer}  # fmt: skip
    ent = {r["scene"]: r["entity"] for r in rows}
    scenes = sorted(
        {s for s, w, a in got if a == "whole" and (s, X.RECALL, "whole") in got and (s, X.LOOKUP, "whole") in got}
    )
    sw = {f"{w}/{a}": [got[(s, w, "whole" if a == "whole" else (*spec, a))] for s in scenes]
          for w in X.READERS for a in ("whole", "no_part", "no_rand")}  # fmt: skip
    r = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
    m = {k: float(sum(v) / len(v)) for k, v in sw.items()}

    def excess(src: dict, w: str):
        return X.dependence(src[f"{w}/whole"], src[f"{w}/no_part"]) - X.dependence(
            src[f"{w}/whole"], src[f"{w}/no_rand"]
        )

    return [float(excess(m, X.RECALL) - excess(m, X.LOOKUP)), *X.interval(excess(r, X.RECALL) - excess(r, X.LOOKUP))]


def alt_candidates(pp: dict, pm: dict) -> list[str]:
    """Other people's picks (by name; look-alikes excluded) whose locker and memory number differ from the bridge's."""
    from scripts import tasks_v2 as T

    f = pp["facts"]
    values = T.DOMAINS[pp["domain"]].values
    x = f["x"]
    assert pp["answer"] == str(f["locker"][x]), f"{pp['id']}: lookup answer vs facts"
    assert pm["answer"] == str(values[x]), f"{pm['id']}: recall answer vs facts"
    return [t for p, t in sorted(f["pick"].items())
            if p != f["person"] and t != x and f["locker"][t] != f["locker"][x] and values[t] != values[x]]  # fmt: skip


def alt_context(item: dict, thing: str) -> str:
    ctx = item["context"]
    i = bridge_start(item, ctx, item["facts"]["x"])
    return ctx[:i] + thing + ctx[i + len(item["facts"]["x"]) :]


def encode(tok, item: dict, context: str, thing: str) -> tuple[list[int], list[int]]:
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    text = X.render(tok, item, "chat", context)
    assert text.count(context) == 1, f"{item['id']}: the context is not once in the prompt"
    enc = raw_encoding(tok, text, offsets=True)
    w0 = text.index(context) + bridge_start(item, context, thing)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(thing))


def scene_case(tok, pair: dict[str, dict]) -> tuple[dict | None, str | None]:
    """One scene with both readers and the first alt candidate that aligns (X0's checks), or the reason it is dropped."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    pp, pm = pair[X.LOOKUP], pair[X.RECALL]
    cands = alt_candidates(pp, pm)
    if not cands:
        return None, "no other pick with a different locker and memory number"
    why = "no alt aligns"
    values = T.DOMAINS[pp["domain"]].values
    x = pp["facts"]["x"]
    for t in cands:
        cf = {X.LOOKUP: str(pp["facts"]["locker"][t]), X.RECALL: str(values[t])}
        readers, pos = {}, None
        for w, it in pair.items():
            ids_org, p_org = encode(tok, it, it["context"], x)
            ids_alt, p_alt = encode(tok, it, alt_context(it, t), t)
            if len(p_org) != 1 or p_alt != p_org:
                why = "the bridge is not one token at one position in org and alt"
                break
            diff = S.changed(ids_org, ids_alt)
            if diff != [p_org[0]]:
                why = "org and alt differ elsewhere than the bridge"
                break
            tok_a, tok_b = (S.answer_token(tok, a, "digit") for a in (it["answer"], cf[w]))
            if tok_a == tok_b:
                why = "the org and alt answers share their first token"
                break
            pos = p_org[0]
            readers[w] = {"id": it["id"], "question": it["question"], "answer": it["answer"], "cf_answer": cf[w],
                          "ids": {"org": ids_org, "alt": ids_alt}, "tok_A": tok_a, "tok_b": tok_b, "upstream": False}  # fmt: skip
        if len(readers) < 2:
            continue
        if any(
            readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1] for v in ("org", "alt")
        ):
            why = "the readers' prompts differ before the bridge"
            continue
        return {"scene": pp["scene"], "rendering": "chat", "domain": pp["domain"], "format": pp["format"],
                "level": pp["level"], "numbers": pp["numbers"], "order": order_of(pp), "bridge": x, "cf_bridge": t,
                "context": pp["context"], "cf_context": alt_context(pp, t), "pos": pos, "upstream": False,
                "space": S.ids(tok, " "), "readers": readers, "facts": pp["facts"]}, None  # fmt: skip
    return None, why


def build_cases(tok, set_name: str) -> tuple[list[dict], dict]:
    from scripts import tasks_v2 as T

    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in X.READERS:
            by_scene[it["scene"]][it["word"]] = it
    cases, dropped = [], collections.Counter()
    for scene in sorted(by_scene):
        pair = by_scene[scene]
        if set(pair) != set(X.READERS) or pair[X.LOOKUP]["context"] != pair[X.RECALL]["context"]:
            dropped["the readers' scenes differ or a reader is missing"] += 1
            continue
        c, why = scene_case(tok, pair)
        if c is None:
            dropped[f"{pair[X.LOOKUP]['domain']}: {why}"] += 1
        else:
            cases.append(c)
    per_cell = collections.Counter("/".join(str(c[k]) for k in CELL) for c in cases)
    return cases, {"scenes": len(by_scene), "cases": len(cases), "dropped": dict(sorted(dropped.items())),
                   "cases_per_cell": dict(sorted(per_cell.items()))}  # fmt: skip


def gate_cells(cases: list[dict], comp: list[dict]) -> tuple[dict, list[dict]]:
    """Per cell: the gate (X0's, within the cell) and the eligible cases (at most CAP, scene order); pooled list."""
    right = {(r["scene"], r["rendering"], r["reader"], r["variant"]): r for r in comp}
    cells: dict[str, list[dict]] = collections.defaultdict(list)
    for c in cases:
        cells["/".join(str(c[k]) for k in CELL)].append(c)
    gate, eligible = {}, []
    for key, mine in sorted(cells.items()):
        acc = X.org_rate(right, mine, "chat", "read_right")
        ok = [c for c in mine if all(right[(c["scene"], "chat", w, v)]["right"] and right[(c["scene"], "chat", w, v)]["read_right"]
                                     for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
        passed = all(a >= X.GATE for a in acc.values())
        gate[key] = {"cases": len(mine), "org_accuracy": acc, "pass": passed, "eligible": len(ok),
                     "used": min(len(ok), CAP) if passed else 0}  # fmt: skip
        eligible += ok[:CAP] if passed else []
    return gate, eligible


def stage_run(
    name: str,
    why: str,
    set_name: str,
    formats: tuple[str, ...] = (),
    levels: tuple[int, ...] = (),
    curve: bool = True,
    pointer: bool = False,
    pcf_from: str | None = None,
) -> Path:
    """formats / levels: keep only those cells (the 122B's b6, Dan 25 Oct ~00:20); curve: the k = 50 / 100 curve;
    pointer: also the pointer directions as a part (T, Dan 26 Oct ~11:55: fit on the simple scenes at the layer fixed
    in advance, not refit), at that layer only; pcf_from (45d, results/<pcf_from>/ of x7_pcf varied): only the held-out
    half, and also the format's refit basis as a part (implies pointer: U is the comparison)."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "run with BJ_FORMAT unset"
    layers, predicted = LAYERS[pins.TARGET], X.PREDICTED[pins.TARGET]
    X.DICTS, X.CURVE_DICTS, X.K_CURVE = (
        ("jpp",),
        ("jpp",),
        K_CURVE if curve else (),
    )  # k = 25 everywhere; 50 / 100 at the predicted layer
    split, pcf = None, {}
    if pcf_from:  # 45d: the per-format bases refit on the other half, and that half's split
        pointer = True
        fm = json.loads((pins.RESULTS_DIR / pcf_from / "manifest.json").read_text())
        assert (fm["model"]["target"], fm["layer"]) == (pins.TARGET, predicted), f"{pcf_from}: another model or layer"
        split = json.loads((pins.RESULTS_DIR / pcf_from / "split.json").read_text())
        assert split["set"] == set_name, f"{pcf_from}: fit on set {split['set']}, not {set_name}"
        pcf = {f: np.load(pins.RESULTS_DIR / pcf_from / f"pcf_{f}.npz")["P"] for f in split["formats"]}
        assert len({p.shape[1] for p in pcf.values()}) == 1, "the formats' bases differ in rank"
    if pointer:
        from scripts import x0_massmean as MM
        from scripts.x6_routes import STATES

        alf = MM.subspaces(STATES[pins.TARGET])[0]["Alf"]
        X.ALF = torch.tensor(alf, dtype=torch.float32, device="cuda")
        X.K_OF["alf"] = alf.shape[1]
        X.DICTS = ("jpp", "alf")
        layers = (predicted,)
    if pcf:
        X.K_OF["pcf"] = next(iter(pcf.values())).shape[1]
        X.DICTS = ("jpp", "alf", "pcf")
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items = pins.DATA_DIR / "tasks_v2" / set_name / "items.jsonl"
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "set": set_name,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in (items, SPEC)},
         "layers": list(layers), "predicted": predicted, "dicts": list(X.DICTS), "k": X.K_MAIN, "cap_per_cell": CAP,
         "gate": f"per cell {CELL}: >= {X.GATE} unedited org accuracy (decisive read), both readers",
         "alt": "the asked pick becomes another person's pick (first by name with a different locker and memory "
                "number that aligns); built here for every domain",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED},
         "rule": {"hold": [HOLD_LOOKUP, HOLD_LOOKUP_HI, HOLD_C, HOLD_C_LO], "fail": [FAIL_LOOKUP, FAIL_C_HI]},
         "k_curve": list(K_CURVE) if curve else [], "formats": list(formats), "levels": list(levels),
         "pointer_from": STATES[pins.TARGET] if pointer else None,
         "pcf_from": pcf_from, "held_out": "per format, the bridge items of split.json's 'test' half" if pcf_from else None,
         "rule_45d": PCF_RULE if pcf_from else None,
         "design": "jobs/c3/batch45.yaml, 45d" if pcf_from else "jobs/c3/X0b.md (v2, exploratory)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, "jpp")
    cases, counts = build_cases(model.tokenizer, set_name)
    if formats or levels:
        cases = [c for c in cases if (not formats or c["format"] in formats) and (not levels or c["level"] in levels)]
        counts["kept_after_filter"] = {"formats": list(formats), "levels": list(levels), "cases": len(cases)}
    if split is not None:
        cases = held_out(cases, split)
        counts["held_out"] = {"pcf_from": pcf_from, "cases": dict(collections.Counter(c["format"] for c in cases))}
    print(json.dumps(counts, indent=1), flush=True)
    ws = X.whitespace_mask(model)
    X.DIGIT_IDS.update(X.digit_ids(model.tokenizer))
    comp = X.competence(model, cases, torch.tensor(X.digit_ids(model.tokenizer), device="cuda"), ws)
    gate, eligible = gate_cells(cases, comp)
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    (out / "gate.json").write_text(
        json.dumps({"counts": counts, "gate": gate, "eligible": len(eligible)}, indent=1) + "\n"
    )
    print(f"eligible {len(eligible)} in {sum(g['pass'] for g in gate.values())} of {len(gate)} cells", flush=True)
    states = []
    with torch.no_grad():  # probe (b): the org state at the bridge's word, predicted layer, every aligned case
        for c in progress(cases, f"h_org at layer {predicted} (case)"):
            ids = torch.tensor([c["readers"][X.LOOKUP]["ids"]["org"]], device="cuda")
            states.append(model.run(ids, record=(predicted,))[1][predicted][c["pos"]].float().cpu().numpy())
    np.savez_compressed(
        out / "states.npz", h=np.stack(states).astype(np.float16), scene=np.array([c["scene"] for c in cases])
    )
    groups = {f: [c for c in eligible if c["format"] == f] for f in pcf} if pcf else {None: eligible}
    for f, mine in groups.items():
        if f is not None:  # 45d: this format's refit basis
            X.PCF = torch.tensor(pcf[f], dtype=torch.float32, device="cuda")
        for s in range(0, len(mine), CHUNK):
            X.run_rendering(model, lens, mine[s : s + CHUNK], layers, predicted, out, ws)
    return out


def held_out(cases: list[dict], split: dict) -> list[dict]:
    """45d: the cases whose bridge item is in its format's held-out ("test") half of x7_pcf varied's split; asserts the
    split covers every case of its formats (the same tokenizer and set built both)."""
    out = []
    for c in cases:
        if c["format"] not in split["formats"]:
            continue
        halves = split["formats"][c["format"]]
        assert c["bridge"] in set(halves["fit"]) | set(halves["test"]), f"{c['scene']}: {c['bridge']} not in the split"
        if c["bridge"] in set(halves["test"]):
            out.append(c)
    return out


def probe_rows(src: Path, cases: dict[str, dict], n_boot: int) -> list[dict]:
    """Probe (b) per format and locker order on the run's states (x0_probe's ridge, folds and baselines)."""
    from scripts import x0_probe as P

    if not (src / "states.npz").exists():
        return []
    z = np.load(src / "states.npz")
    h, scenes = z["h"].astype(np.float64), [str(s) for s in z["scene"]]
    items = [{"entity": cases[s]["bridge"], "format": cases[s]["format"], "order": cases[s]["order"], **ordinals(cases[s])}
             for s in scenes]  # fmt: skip
    out = []
    for fmt in sorted({it["format"] for it in items}):
        for order in ("before", "after"):
            idx = [i for i, it in enumerate(items) if it["format"] == fmt and it["order"] == order]
            sub = [items[i] for i in idx]
            if (
                len(idx) < 2 * P.K_OUTER
                or len({it["entity"] for it in sub}) < P.K_OUTER
                or len({it["locker_index"] for it in sub}) < 2
            ):
                continue
            out.append({"format": fmt, "order": order, **P.score(h[idx], sub, "locker sentence", n_boot)})
    return out


def write_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    gate = json.loads((src / "gate.json").read_text())
    pred = m["predicted"]
    main = lambda cells, w: cells.get(("chat", pred, w, *X.MAIN))  # noqa: E731
    cells = X.cells_of(rows, n_boot)
    lk, rc = main(cells, X.LOOKUP), main(cells, X.RECALL)
    layers = sorted({k[1] for k in cells})
    cs = {la: contrast(rows, la, X.MAIN, n_boot) for la in layers}
    v = rule(lk, rc, cs[pred]) if lk and rc else "can't test (no rows)"
    probe = probe_rows(src, cases, n_boot)
    strata = []
    for key in STRATA:
        for value in sorted({str(c[key]) for c in cases.values()}):
            sub = X.cells_of([r for r in rows if str(cases[r["scene"]][key]) == value], n_boot) if rows else {}
            for w in X.READERS:
                c = main(sub, w)
                if c:
                    strata.append({"feature": key, "value": value, "reader": w, **c})
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": name, "model": m["model"], "lens": m["lens"], "predicted": pred, "verdict": v,
            "contrast": {str(la): c for la, c in cs.items()}, "probe_b": probe,
            "cells": [{"layer": k[1], "reader": k[2], "dict": k[3], "k": k[4], "omp": k[5], **c}
                      for k, c in sorted(cells.items())], "strata": strata}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    n_pass = sum(g["pass"] for g in gate["gate"].values())
    lines = [f"# X0b (exploratory): {name}", "",
             f"Model {m['model']['target']} ({m['model']['revision'][:8]}); set {m['set']}; predicted layer {pred}; J++ "
             f"k = {X.K_MAIN} signed, the random part of its share; the alt built here (single change). UNVERIFIED.", "",
             f"Gate per cell: {n_pass} of {len(gate['gate'])} cells pass; {gate['eligible']} eligible scenes used "
             f"(at most {m['cap_per_cell']} per cell).", "",
             f"## X0b's rule at layer {pred}, pooled: {v.upper()} (C = {X.fmt3(cs[pred])})", "",
             f"Holds iff lookup excess <= {HOLD_LOOKUP} (upper CI <= {HOLD_LOOKUP_HI}) and C >= {HOLD_C} (lower CI >= "
             f"{HOLD_C_LO}); fails iff lookup excess >= {FAIL_LOOKUP} or C's upper CI < {FAIL_C_HI}.", "",
             "| layer | reader | n | entities | S_whole | Jdep | Rdep | excess | label | C (recall - lookup) |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for (_, la, w, *d), c in sorted(cells.items()):
        if tuple(d) == X.MAIN:
            lines.append(f"| {la} | {w} | {c['n']} | {c['entities']} | {X.fmt3(c['S_whole'])} | {X.fmt3(c['Jdep'])} | "
                         f"{X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} | {c['label']} | {X.fmt3(cs[la])} |")  # fmt: skip
    lines += ["", f"## The k-curve at layer {pred} (descriptive)", "",
              "| k | reader | Jdep | Rdep | excess | label |", "|---|---|---|---|---|---|"]  # fmt: skip
    for (_, la, w, d, k, omp), c in sorted(cells.items(), key=lambda kv: (kv[0][4], kv[0][2])):
        if la == pred and d == "jpp" and omp == "signed":
            lines.append(
                f"| {k} | {w} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} | {c['label']} |"
            )
    lines += ["", f"## Probe (b) at layer {pred}: the bridge's locker row ordinal (descriptive)", "",
              "Org states at the bridge's word of every aligned scene; cross-validated by bridge entity. 'layout': the "
              "most frequent ordinal given how many locker statements precede the asked pick, of how many.", "",
              "| format | locker vs pick | n | entities | classes | probe | majority | chance | pick ordinal only | "
              "layout | probe - best baseline |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for p in probe:
        lines.append(f"| {p['format']} | {p['order']} | {p['n']} | {p['entities']} | {p['classes']} | {X.fmt3(p['probe'])} | "
                     f"{X.fmt3(p['majority'])} | {p['chance']:.2f} | {X.fmt3(p['structure'])} | {X.fmt3(p['layout'])} | "
                     f"{X.fmt3(p['probe_minus_best'])} ({p['best_baseline']}) |")  # fmt: skip
    lines += ["", f"## Strata at layer {pred} (descriptive)", "", "⚠ = fewer than 30 switched by the whole edit.", "",
              "| feature | value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |",
              "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for s in strata:
        flag = " ⚠" if s["switched_whole"] < X.VALID_N else ""
        lines.append(f"| {s['feature']} | {s['value']} | {s['reader']} | {s['n']} | {s['switched_whole']}{flag} | "
                     f"{X.fmt3(s['S_whole'])} | {X.fmt3(s['Jdep'])} | {X.fmt3(s['Rdep'])} | {X.fmt3(s['excess'])} | "
                     f"{s['label']} |")  # fmt: skip
    lines += ["", "## Gate per cell", "", "| cell | cases | org accuracy (lookup / recall) | pass | eligible | used |",
              "|---|---|---|---|---|---|"]  # fmt: skip
    for key, g in gate["gate"].items():
        acc = g["org_accuracy"]
        lines.append(f"| {key} | {g['cases']} | {acc.get(X.LOOKUP, 0):.2f} / {acc.get(X.RECALL, 0):.2f} | {g['pass']} | "
                     f"{g['eligible']} | {g['used']} |")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:20]))
    return out


def figures(verdict_dir: Path) -> Path:
    """Excess per stratum at the predicted layer, lookup and recall, with CIs; the pooled cell on top."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    blob = json.loads((verdict_dir / "verdict.json").read_text())
    pooled = [("pooled", "all", next((c for c in blob["cells"] if c["layer"] == blob["predicted"] and c["reader"] == w
                                      and (c["dict"], c["k"], c["omp"]) == X.MAIN), None), w) for w in X.READERS]  # fmt: skip
    rows = [(s["feature"], s["value"], s, s["reader"]) for s in blob["strata"]]
    labels = list(dict.fromkeys(f"{f}: {v}" for f, v, _, _ in [*pooled, *rows]))
    fig, ax = plt.subplots(figsize=(8, 0.32 * len(labels) + 1.6))
    color = {X.LOOKUP: F.LOOKUP, X.RECALL: F.RECALL}
    for f, v, c, w in [*pooled, *rows]:
        if c is None:
            continue
        y = labels.index(f"{f}: {v}") + (-0.15 if w == X.LOOKUP else 0.15)
        e = c["excess"]
        ax.errorbar(e[0], y, xerr=[[e[0] - e[1]], [e[2] - e[0]]], fmt="o" if c["switched_whole"] >= X.VALID_N else "x",
                    color=color[w], ms=5, capsize=2)  # fmt: skip
    ax.axvspan(-0.3, X.AROUND_EXCESS, color="#f1f1f1", lw=0, zorder=0)
    ax.axvline(X.THROUGH_EXCESS, color="#bbbbbb", lw=0.8, ls=":")
    ax.axvline(0, color="black", lw=0.6)
    ax.set_yticks(range(len(labels)), labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(-0.3, 1.0)
    ax.set_xlabel(f"extra loss (J++ part vs a random part of its share), layer {blob['predicted']}")
    ax.set_title(f"X0b {blob['run']}: lookup (blue) and recall, by stratum (exploratory; UNVERIFIED; x = < 30 switched)",
                 fontsize=9)  # fmt: skip
    fig.tight_layout()
    path = verdict_dir / "x0b_strata.png"
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    print(path)
    return path


def cross(name: str, n_boot: int = X.N_BOOT) -> Path:
    """Descriptive: both readers' cells at the predicted layer by format x locker order (Q27.12 asks about the lookup by
    format in locker-before scenes)."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["layer"] == m["predicted"]]
    lines = [f"# X0b: format x locker order, layer {m['predicted']} ({name})", "",
             "Descriptive. J++ k = 25 signed; bootstrap over bridge entities. UNVERIFIED. ⚠ = fewer than 30 switched.", "",
             "| format | locker vs pick | reader | n | switched | S_whole | Jdep | Rdep | excess | label |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for fmt in ("prose", "json", "table"):
        for order in ("before", "after"):
            sub = [r for r in rows if cases[r["scene"]]["format"] == fmt and cases[r["scene"]]["order"] == order]
            if not sub:
                continue
            cells = X.cells_of(sub, n_boot)
            for w in X.READERS:
                c = cells[("chat", m["predicted"], w, *X.MAIN)]
                blob.append({"format": fmt, "order": order, "reader": w, **c})
                flag = " ⚠" if c["switched_whole"] < X.VALID_N else ""
                lines.append(f"| {fmt} | {order} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | "
                             f"{c['switched_whole']}{flag} | {X.fmt3(c['S_whole'])} | {X.fmt3(c['Jdep'])} | "
                             f"{X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
    out = src / f"cross-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "cross.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "cross.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


# ---- 45d (batch 45): the refit basis on the held-out half --------------------------------------------------------

EPS = 1e-9  # float tolerance: an extra loss equal to a bar on paper counts as equal (e.g. 1 - 0.8 = 0.19999...)


def pcf_rule(lookup: dict[str, list[float] | None]) -> dict:
    """45d's rule (PCF_RULE) on the lookup's extra loss with the refit basis per format, [point, lower, upper] (None:
    no cell). "At least 0.2" and "below 0.1" read the point estimate, "lower CI above 0.1" is strict. Not in
    batch45.yaml, so fixed here: a format without a finite point estimate (no rows, or nothing switched with the whole
    change) is "not tested" and never passes; with one such format the outcome is "incomplete" unless two others
    already make "pointer elsewhere"."""
    cell = {f: v for f, v in lookup.items() if f in FORMATS and v is not None and math.isfinite(v[0])}
    tested = [f for f in FORMATS if f in cell]
    passed = [f for f in tested
              if cell[f][0] >= ELSEWHERE - EPS and math.isfinite(cell[f][1]) and cell[f][1] > ELSEWHERE_LO + EPS]  # fmt: skip
    below = [f for f in tested if cell[f][0] < NONE_BELOW - EPS]
    if len(passed) >= ELSEWHERE_FORMATS:
        outcome = "pointer elsewhere"
    elif len(tested) < len(FORMATS):
        outcome = "incomplete"
    elif len(below) == len(FORMATS):
        outcome = "no linear pointer found"
    else:
        outcome = "neither"
    return {"outcome": outcome, "passed": passed, "below": below, "not_tested": [f for f in FORMATS if f not in tested]}


def pcf_cells(rows: list[dict], fmt_of: dict[str, str], layer: int, n_boot: int = X.N_BOOT) -> dict[tuple, dict]:
    """Per (format, part, reader): X0's cell at the layer for the refit basis ("pcf") and U ("alf"), each against its
    own random part (cluster bootstrap over bridge items)."""
    out = {}
    for f in FORMATS:
        sub = [r for r in rows if r["layer"] == layer and fmt_of.get(r["scene"]) == f
               and (r["arm"] == "whole" or r["dict"] in PARTS_45D)]  # fmt: skip
        for key, c in (X.cells_of(sub, n_boot) if sub else {}).items():
            out[(f, key[3], key[2])] = c
    return out


def write_pcf_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    """45d's verdict: the rule on the lookup, both readers' cells for both parts per format, the parts' median shares;
    results/x0b_generalize/<name>/x45d-<time>/{verdict.json, verdict.md}. Prints only where it wrote."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("pcf_from"), f"{name}: not a 45d run (its manifest has no pcf_from)"
    rows = X.read_jsonl(src / "outcomes.jsonl")
    fmt_of = {c["scene"]: c["format"] for c in X.read_jsonl(src / "cases.jsonl")}
    pred = m["predicted"]
    cells = pcf_cells(rows, fmt_of, pred, n_boot)
    lookup = {f: cells[(f, "pcf", X.LOOKUP)]["excess"] if (f, "pcf", X.LOOKUP) in cells else None for f in FORMATS}
    v = pcf_rule(lookup)
    shares: dict[tuple, list[float]] = collections.defaultdict(list)
    for s in X.read_jsonl(src / "shares.jsonl"):
        if s["layer"] == pred and s["dict"] in PARTS_45D:
            shares[(fmt_of[s["scene"]], s["dict"])].append(s["share"])
    med = {k: statistics.median(v_) for k, v_ in shares.items()}
    out = src / f"x45d-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": name, "model": m["model"], "predicted": pred, "pcf_from": m["pcf_from"], "rule": PCF_RULE,
            "n_boot": n_boot, "verdict": v, "lookup_refit": lookup,
            "cells": [{"format": f, "part": d, "reader": w, "median_share": med.get((f, d)), **c}
                      for (f, d, w), c in sorted(cells.items())]}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# 45d, a pointer outside templates: {name}", "",
             f"Model {m['model']['target']}, layer {pred}; the held-out half of the varied scenes (per format, the bridge "
             f"items not used for the fit, {m['pcf_from']}). Extra loss = switches lost without the part minus without a "
             f"random part of its share; cluster bootstrap over bridge items ({n_boot} resamples, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", f"Rule (fixed in advance, on the lookup with the refit basis): {PCF_RULE}", "",
             f"**Outcome: {v['outcome']}** (formats at >= {ELSEWHERE} with lower CI > {ELSEWHERE_LO}: "
             f"{', '.join(v['passed']) or 'none'}; below {NONE_BELOW}: {', '.join(v['below']) or 'none'}; not tested: "
             f"{', '.join(v['not_tested']) or 'none'}).", "",
             "| format | part | reader | n | items | switched (whole) | valid | median share | Jdep | Rdep | extra loss |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for f in FORMATS:
        for d, label in PARTS_45D.items():
            for w in X.READERS:
                c = cells.get((f, d, w))
                if c is None:
                    lines.append(f"| {f} | {label} | {w} | – | – | – | – | – | – | – | not tested |")
                    continue
                sh = f"{med[(f, d)]:.3f}" if (f, d) in med else "–"
                lines.append(f"| {f} | {label} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | {c['entities']} | "
                             f"{c['switched_whole']} | {c['valid']} | {sh} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | "
                             f"{X.fmt3(c['excess'])} |")  # fmt: skip
    lines += ["", "valid (descriptive, not in the rule): S_whole >= 0.30 and >= 30 switched by the whole change. U is the "
              "comparison part (simple scenes, not refit); the rule reads only the refit basis on the lookup."]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def pcf_figure(verdict_dir: Path) -> Path:
    """The lookup's and the recall's extra loss per format, the refit basis and U side by side (one shared axis), with
    the rule's bars; into a new analysis-*-x45d/ folder of the run (the job page shows it)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    blob = json.loads((verdict_dir / "verdict.json").read_text())
    cells = {(c["format"], c["part"], c["reader"]): c for c in blob["cells"]}
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    style = {X.LOOKUP: ("lookup", F.LOOKUP, "o", -0.12), X.RECALL: ("recall", F.RECALL, "s", 0.12)}
    for ax, (d, label) in zip(axes, PARTS_45D.items(), strict=True):
        for w, (wl, color, mk, dx) in style.items():
            for i, f in enumerate(FORMATS):
                c = cells.get((f, d, w))
                if c is None or not math.isfinite(c["excess"][0]):
                    ax.text(i + dx, 0, "–", color=F.CAPTION_INK, ha="center", fontsize=9)
                    continue
                e = c["excess"]
                ax.errorbar(i + dx, e[0], yerr=[[e[0] - e[1]], [e[2] - e[0]]], fmt=mk, color=color, ms=7, capsize=3,
                            lw=1.5, label=wl if i == 0 else None, mfc=color if c["valid"] else "white")  # fmt: skip
        for y, txt in ((ELSEWHERE, f"{ELSEWHERE} (point)"), (ELSEWHERE_LO, f"{ELSEWHERE_LO} (lower CI / below)")):
            ax.axhline(y, color=F.CONTROL, lw=0.8, ls="--")
            ax.text(2.45, y, f" {txt}", color=F.CAPTION_INK, fontsize=7, va="bottom", ha="right")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_xticks(range(len(FORMATS)), [f"{f}\n(n {cells[(f, d, X.LOOKUP)]['n']})" if (f, d, X.LOOKUP) in cells else f
                                             for f in FORMATS])  # fmt: skip
        ax.set_xlim(-0.5, 2.5)
        ax.set_title(f"without {label}", fontsize=10)
        ax.grid(axis="y", color="#eeeeee", lw=0.6)
    axes[0].set_ylabel("extra loss (vs a random part of its share)")
    axes[0].legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle(f"45d {blob['run']} ({blob['model']['target']}, layer {blob['predicted']}): outcome "
                 f"{blob['verdict']['outcome']} (UNVERIFIED; open marker = invalid cell: S_whole < 0.30 or < 30 switched)",
                 fontsize=10)  # fmt: skip
    fig.tight_layout()
    folder = verdict_dir.parent / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-x45d"
    folder.mkdir()
    path = folder / "x45d_extra_loss.png"
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    print("wrote", path, flush=True)
    return path


EXAMPLE_ARMS_45D = (("-", "none", "unedited"), ("-", "whole", "the whole change"),
                    ("jpp", "no_part", "without J++"), ("jpp", "no_rand", "without a random part (J++'s share)"),
                    ("alf", "no_part", "without U"), ("alf", "no_rand", "without a random part (U's share)"),
                    ("pcf", "no_part", "without the refit basis"),
                    ("pcf", "no_rand", "without a random part (the refit basis's share)"))  # fmt: skip
MARK = ("⟦", "⟧")


def marked_prompt(tok, ids: list[int], pos: int, tail: list[int]) -> tuple[str, int, int]:
    """The prompt as the model reads it (ids, then `tail`: the chat read's appended space) and the character span of
    the token at pos, where the change is added."""
    before, word = tok.decode(ids[:pos]), tok.decode(ids[pos : pos + 1])
    text = before + word + tok.decode(ids[pos + 1 :] + tail)
    return text, len(before), len(before) + len(word)


def examples_blob(tok, name: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> tuple[dict, list[str]]:
    """k random items (seed) of a 45d run, both readers: the prompt as the model sees it with the patch position
    marked, and each arm's answer (the top token read; its class: changed answer, original answer, other). The
    job-page examples.json blob and a Markdown version."""
    from scripts import suite_v1 as S

    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    pred = m["predicted"]
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["layer"] == pred]
    got = {(r["scene"], r["reader"], r["dict"], r["arm"]): r for r in rows}
    scenes = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    pick = sorted(random.Random(seed).sample(scenes, min(k, len(scenes))))
    space = S.ids(tok, " ")
    role = {"b": "changed answer", "A": "original answer", "other": "other"}
    examples, md = [], [f"# 45d examples: {name}", "",
                        f"{len(pick)} random items (seed {seed}) of {len(scenes)}; the prompt as the model reads it (the "
                        f"chat read appends a space), {MARK[0]}the bridge word{MARK[1]} where the change is added at layer "
                        f"{pred}; each arm's answer = the top token at the read step. UNVERIFIED.", ""]  # fmt: skip
    for s in pick:
        c = cases[s]
        md += [f"## {s} ({c['format']}, level {c['level']}, {c['domain']}; bridge {c['bridge']} -> {c['cf_bridge']}, "
               f"locker {c['order']} the pick)", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            text, a, b = marked_prompt(tok, rd["ids"]["org"], c["pos"], space)
            answers = {}
            for d, arm, label in EXAMPLE_ARMS_45D:
                r = got.get((s, w, d, arm))
                if r is not None:
                    top = repr(tok.decode([r["top"]])) if "top" in r else "(not stored)"
                    answers[label] = f"{top}, {role[r['role']]}"
            reader = "lookup" if w == X.LOOKUP else "recall"
            examples.append({"group": reader, "family": reader, "item_id": s, "prompt": text,
                             "spans": [{"start": a, "end": b, "role": "patch position (the bridge word)"}],
                             "condition": f"{c['format']}, level {c['level']}; the bridge {c['bridge']} -> {c['cf_bridge']} at "
                                          f"layer {pred}",
                             "answers": {"clean": rd["answer"], "edited": answers.get("the whole change"),
                                         "expected": {"original": rd["answer"], "changed": rd["cf_answer"]}},
                             "numbers": answers, "why": f"random item (seed {seed})"})  # fmt: skip
            md += [f"**{reader}** (original {rd['answer']}, changed {rd['cf_answer']})", "", "```",
                   text[:a] + MARK[0] + text[a:b] + MARK[1] + text[b:], "```", "", "| arm | answer |", "|---|---|",
                   *(f"| {label} | {ans} |" for label, ans in answers.items()), ""]  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g, "definition": f"the {g} reader on the same patch", "n_total": len(pick)}
                       for g in ("lookup", "recall")], "examples": examples}  # fmt: skip
    return blob, md


def stage_examples(name: str) -> Path:
    from scripts import statement_positions as SP

    path = RESULTS / name / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    blob, md = examples_blob(SP.load_tokenizer(), name)
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (RESULTS / name / "examples.md").write_text("\n".join(md) + "\n")
    print("wrote", path, len(blob["examples"]), "examples")
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "figures", "cross", "pcf-verdict", "examples"])
    ap.add_argument("--name")
    ap.add_argument("--why", default="")
    ap.add_argument("--set", default="x0b_v2")
    ap.add_argument("--formats", nargs="*", default=[], help="run: keep only these formats")
    ap.add_argument("--levels", nargs="*", type=int, default=[], help="run: keep only these levels")
    ap.add_argument("--no-curve", action="store_true", help="run: no k = 50 / 100 curve")
    ap.add_argument("--pointer", action="store_true", help="run: also the pointer directions as a part (T)")
    ap.add_argument("--pcf-from", default=None,
                    help="run (45d): the held-out half and the per-format refit bases of x7_pcf varied (results/<path>)")  # fmt: skip
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        from scripts import statement_positions as SP

        cases, counts = build_cases(SP.load_tokenizer(), a.set)
        print(json.dumps(counts, indent=1))
        print("order:", collections.Counter((c["format"], c["order"]) for c in cases))
        print("entities:", len({c["bridge"] for c in cases}), "levels:", collections.Counter(c["level"] for c in cases))
        print("median cases per cell:", statistics.median(counts["cases_per_cell"].values()))
    elif a.stage == "run":
        stage_run(a.name, a.why, a.set, tuple(a.formats), tuple(a.levels), not a.no_curve, a.pointer, a.pcf_from)
        # 45d is sealed until Dan's predictions are committed (Dan 26 Oct 18:25): no verdict runs after the run;
        # pcf-verdict (and verdict) run by hand once Q45.4 is filled
        if not a.pcf_from:
            figures(write_verdict(a.name, a.n_boot))
    elif a.stage == "pcf-verdict":
        pcf_figure(write_pcf_verdict(a.name, a.n_boot))
    elif a.stage == "examples":
        stage_examples(a.name)
    elif a.stage == "cross":
        cross(a.name, a.n_boot)
    elif a.stage == "verdict":
        figures(write_verdict(a.name, a.n_boot))
    else:
        figures(sorted((RESULTS / a.name).glob("verdict-*"))[-1])


if __name__ == "__main__":
    main()
