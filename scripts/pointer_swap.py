"""pointer_swap (Dan's D3, 2026-10-20): what do the question tokens carry in transit when a recalled bridge feeds an
in-prompt lookup: the bridge's identity, a pointer to the binding statement's position, or the answer itself?

Items: scripts/pointer_v1.py (data/pointer_v1/<set>/). Each base item has a token-aligned source "dissoc" whose residual,
patched into the base, predicts four distinct answers (none = the base answer; identity = the base's digit for the
source's entity; position = the base's digit at the source's queried slot; value = the source's answer, absent from the
base context; for RR value = identity by construction).

Edits (activation patching: the base's block output at the positions replaced by the source's), on the read prompt:
  groups   question (the question's tokens, cue included), final (every token after the question: instruction,
           template, 'Answer:'), last (the read's last two tokens, ':' and the appended space, where lookback work puts
           the pointer at mid-late depth before the value), both (question + final)
  layers   one at a time (the manifest's list, every 2nd or 4th layer), and windows (all layers of the window at once;
           default early 16-28, mid 32-40, transit 44-52 on the 27B, the same depth fractions elsewhere)
  sources  dissoc (the 4-way prediction); controls: same (q_s = q_b at the same slot with the same digit, the rest of the
           context reshuffled and redigited: every hypothesis predicts the base answer, so a change is damage), rand (a
           seeded random direction with the dissoc patch's per-position norm, added), other (a random item of another
           domain, same family and level: its residual at the positions the same distance from the prompt's end, added
           as a difference rescaled per position to the dissoc patch's norm); rand and other at every `control_stride`-th
           layer of the list
  checks   per item: the unedited base read; base patched into base at the middle layer (must be a no-op); the dissoc
           source patched at every position at layer 0 (must reproduce the source's own read: the hook's positive
           control)
Scoring (suite_split's answer read): one forward with the digit answer's space token appended; the top token's role:
none / identity / position / value (in that priority) / context (another digit of the base context) / recall (a
recalled digit of q_b, q_s or p; lookups only) / other_digit / other; p of each predicted digit.

Decision rule (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window
x source dissoc), pooled over domains, Wilson 95% intervals over items:
  - interpretable iff the dissoc patch changes the answer (1 - share none: lower bound >= 0.20) and the same control
    changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"
  - verdict X in {identity, position, value} (RR: identity, position) iff X's lower bound exceeds the upper bounds of
    the other two and the chance bar: the rand control's upper bound for X at that layer (windows: the max over the
    window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)
  - otherwise "mixed". Primary: RL, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:
    position; H-word (or a lexical key): identity; H-value: value. DL is the reference (classic binding retrieval),
    RR the contrast (a pointer is useless there).

Stages:  manifest --name N --why W --set S [--levels ...] [--families ...] [--domains ...] [--n K] [--layers ...]
                  [--control-stride 2] [--competence RUN | --no-eligibility]
         run --name N          summarise --name N (re-aggregates into a new analysis-<stamp>/)
         examples --name N [--k 3] [--seed 0] (results/pointer_swap/N/examples.json)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "pointer_swap"
RESULTS = pins.RESULTS_DIR / EXP
GROUPS = ("question", "final", "last", "both")
SOURCES = ("dissoc", "same", "rand", "other")
ROLES = ("none", "identity", "position", "value", "context", "recall", "other_digit", "other")
WINDOW_FRACTIONS = {"early": (16 / 64, 28 / 64), "mid": (32 / 64, 40 / 64), "transit": (44 / 64, 52 / 64)}
SAMPLE_SEED, NULL_SEED, OTHER_SEED, EXAMPLE_SEED = 0, 0, 0, 0
BATCH = 64
CHANGED_MIN, DAMAGE_MAX = 0.20, 0.10


def default_layers(step: int = 2) -> list[int]:
    return list(range(0, pins.N_LAYERS - 3, step))


def default_windows() -> dict[str, list[int]]:
    n = pins.N_LAYERS
    return {w: list(range(round(lo * n), round(hi * n) + 1)) for w, (lo, hi) in WINDOW_FRACTIONS.items()}


class SetRows:
    """Edit for one layer: the rows at `positions` replaced by `rows` [P, d] (activation patching)."""

    def __init__(self, rows: torch.Tensor, positions: list[int]):
        self.rows, self.positions = rows, positions

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = self.rows.to(h.dtype)
        return out


class AddRows:
    def __init__(self, delta: torch.Tensor, positions: list[int]):
        self.delta, self.positions = delta, positions

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = h[self.positions] + self.delta.to(h.dtype)
        return out


def null_rows(delta: torch.Tensor, generator: torch.Generator) -> torch.Tensor:
    r = torch.randn(delta.shape, device=delta.device, generator=generator)
    return torch.nn.functional.normalize(r, dim=-1) * delta.norm(dim=-1, keepdim=True)


# ---- items ----------------------------------------------------------------------------------------------------------


def prompt_text(tok, ctx: str, question: str) -> str:
    return S.render(tok, ctx, question)


def prepare(item: dict, tok) -> dict[str, Any]:
    """Token ids (read form: the space token appended) of the base and the three sources, and the position groups."""
    from bridge_jspace.tokens import raw_encoding

    space = S.ids(tok, " ")
    texts = {"base": (item["context"], item["question"])}
    texts |= {s: (v["context"], v["question"]) for s, v in item["sources"].items()}
    rendered = {k: prompt_text(tok, c, q) for k, (c, q) in texts.items()}
    enc = raw_encoding(tok, rendered["base"], offsets=True)
    ids = {k: S.ids(tok, t) for k, t in rendered.items()}
    assert ids["base"] == list(enc["input_ids"]), f"{item['id']}: raw encoding differs"
    assert len({len(v) for v in ids.values()}) == 1, f"{item['id']}: sources not token-aligned"
    q0 = rendered["base"].rindex("\n" + item["question"]) + 1
    q1 = q0 + len(item["question"])
    offs = enc["offset_mapping"]
    question = [i for i, (s, e) in enumerate(offs) if e > q0 and s < q1]
    final = [i for i, (s, _) in enumerate(offs) if s >= q1]
    for k in ids:
        assert [ids[k][i] for i in final] == [ids["base"][i] for i in final], f"{item['id']}: template differs ({k})"
    n = len(ids["base"])
    return {
        "text": rendered["base"],
        "source_text": rendered["dissoc"],
        "offsets": offs,
        "read_ids": {k: v + space for k, v in ids.items()},
        "groups": {
            "question": question,
            "final": final,
            "last": [n - 1, n],
            "both": question + final,
            "all": list(range(n + len(space))),
        },
    }


def role_map(item: dict, preds: dict[str, str], lookup: bool) -> dict[str, str]:
    """digit -> role, by the docstring's priority."""
    out: dict[str, str] = {}
    for h in PV.HYPOTHESES:
        out.setdefault(preds[h], h)
    for d in item["digits"]:
        out.setdefault(str(d), "context")
    if lookup:
        sl = item["slots"]
        for e in (item["query"], item["entities"][sl["identity"]], item["entities"][sl["position"]]):
            out.setdefault(str(item["recalled"][e]), "recall")
    return out


def slot_class(item: dict) -> str:
    """first / middle / last statement for the base query (Mixing Mechanisms: positional binding dominates only at the
    ends; lexical and reflexive routes take over in the middle)."""
    a = item["slots"]["query"]
    return "first" if a == 0 else "last" if a == item["n_entities"] - 1 else "middle"


def other_predictions(item: dict, other: dict) -> dict[str, str]:
    """For the 'other' control: none; position = the base digit at the other item's queried slot (if not the base's);
    value = the other's answer if absent from the base context. No identity (another domain)."""
    k = other["slots"]["query"]
    p = {"none": item["answer"], "identity": "-", "position": "-", "value": "-"}
    if k != item["slots"]["query"] and k < len(item["digits"]) and item["family"] != "RR":
        p["position"] = str(item["digits"][k])
    if item["family"] != "RR" and int(other["answer"]) not in item["digits"]:
        p["value"] = other["answer"]
    return p


def load_items(m: dict) -> dict[str, list[dict]]:
    return {label: PV.load_file(pins.REPO_ROOT / pin["file"]) for label, pin in m["items"].items()}


def eligible_ids(comp_run: str | None) -> set[str] | None:
    if not comp_run:
        return None
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    for line in (PV.RESULTS / comp_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        ok[r["id"]].append(r["correct"])
    return {i for i, v in ok.items() if all(v)}


def sample_cases(m: dict, items: dict[str, list[dict]]) -> tuple[list[dict], dict]:
    """Per (domain, level): up to n scenes eligible in every family of the run, seed SAMPLE_SEED; every family on them."""
    good = eligible_ids(m["competence"])
    by_cell: dict[tuple[str, str], dict[str, dict[str, dict]]] = collections.defaultdict(dict)
    for its in items.values():
        for it in its:
            if it["family"] in m["families"] and it["domain"] in m["domains"] and it["level"] in m["levels"]:
                by_cell[(it["domain"], it["level"])].setdefault(it["family"], {})[it["scene"]] = it
    rng = random.Random(SAMPLE_SEED)
    cases, counts = [], {}
    for (dom, lv), fams in sorted(by_cell.items()):
        scenes = set.intersection(*(set(fams[f]) for f in m["families"]))
        if good is not None:
            scenes = {s for s in scenes if all(fams[f][s]["id"] in good for f in m["families"])}
        picked = rng.sample(sorted(scenes), min(m["n"], len(scenes)))
        counts[f"{dom}/{lv}"] = {"eligible_scenes": len(scenes), "sampled": len(picked)}
        cases += [fams[f][s] for s in picked for f in m["families"]]
    return cases, counts


# ---- stages ---------------------------------------------------------------------------------------------------------


def stage_manifest(args) -> None:
    pins.check_run_name(args.name)
    path = RESULTS / args.name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    levels = args.levels or list(PV.SETS[args.set]["levels"])
    files = {
        f"{d}_{f}_{lv}": PV.DATA / args.set / f"{d}_{f}_{lv}.json"
        for lv in levels
        for d in args.domains
        for f in args.families
    }
    assert args.competence or args.no_eligibility, "--competence RUN (or --no-eligibility for a smoke)"
    comp = PV.RESULTS / args.competence / "items.jsonl" if args.competence else None
    layers = args.layers or default_layers(args.layer_step)
    m = {
        "exp": EXP, "run": args.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": args.why,
        "model": pins.model_pin(), "set": args.set, "levels": levels, "families": args.families, "domains": args.domains,
        "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
        "competence": args.competence,
        "competence_sha256": sha256_of(comp) if comp else None,
        "n": args.n, "layers": layers, "control_stride": args.control_stride, "windows": default_windows(),
        "groups": list(GROUPS), "sources": list(SOURCES),
        "sample": f"per (domain, level), up to n scenes eligible (every competence prompt right) in all of the run's "
        f"families, seed {SAMPLE_SEED}; every family on the same scenes",
        "seeds": {"sample": SAMPLE_SEED, "null": NULL_SEED, "other": OTHER_SEED},
        "decision": (__doc__ or "").split("Decision rule")[1].split("Stages:")[0].strip(),
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def check_inputs(m: dict) -> None:
    for f, pin in m["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    if m["competence"]:
        comp = PV.RESULTS / m["competence"] / "items.jsonl"
        assert sha256_of(comp) == m["competence_sha256"], "the competence run changed since the manifest"


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    check_inputs(m)
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    items = load_items(m)
    cases, counts = sample_cases(m, items)
    print(json.dumps(counts), flush=True)
    pool: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)  # (family, level) -> items, for 'other'
    for its in items.values():
        for it in its:
            pool[(it["family"], it["level"])].append(it)
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    layers, windows, stride = m["layers"], m["windows"], m["control_stride"]
    mid = layers[len(layers) // 2]
    record = tuple(sorted(set(layers) | {la for w in windows.values() for la in w} | {0}))
    outcomes: list[dict] = []
    checks: list[dict] = []
    for ci, c in enumerate(progress(cases, "cases")):
        prep = prepare(c, tok)
        rng = random.Random(OTHER_SEED * 1_000_003 + ci)
        other = rng.choice([o for o in pool[(c["family"], c["level"])] if o["domain"] != c["domain"]] or [c])
        o_ids = S.ids(tok, prompt_text(tok, other["context"], other["question"])) + S.ids(tok, " ")
        runs = {k: model.run(torch.tensor([v], device="cuda"), record=record) for k, v in prep["read_ids"].items()}
        runs["other"] = model.run(torch.tensor([o_ids], device="cuda"), record=record)
        h = {k: v[1] for k, v in runs.items()}
        lookup = c["family"] != "RR"
        preds = c["sources"]["dissoc"]["predictions"]
        roles = role_map(c, preds, lookup)
        o_preds = other_predictions(c, other)
        o_roles = role_map(c, o_preds, lookup)
        g = prep["groups"]
        n_base, n_o = len(prep["read_ids"]["base"]), len(o_ids)
        jobs: list[tuple[dict, dict]] = [
            ({"layer": -1, "group": "-", "source": "unedited"}, {}),
            ({"layer": mid, "group": "both", "source": "self"}, {mid: SetRows(h["base"][mid][g["both"]], g["both"])}),
            ({"layer": 0, "group": "all", "source": "dissoc"}, {0: SetRows(h["dissoc"][0], g["all"])}),
        ]
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 7919 * ci)
        for li, la in enumerate(layers):
            for grp in GROUPS:
                pos = g[grp]
                for src in ("dissoc", "same"):
                    jobs.append(({"layer": la, "group": grp, "source": src}, {la: SetRows(h[src][la][pos], pos)}))
                if li % stride:
                    continue
                delta = h["dissoc"][la][pos] - h["base"][la][pos]
                jobs.append(({"layer": la, "group": grp, "source": "rand"}, {la: AddRows(null_rows(delta, gen), pos)}))
                pos_o = [n_o - (n_base - i) for i in pos]
                if min(pos_o) >= 0:
                    d_o = h["other"][la][pos_o] - h["base"][la][pos]
                    d_o = torch.nn.functional.normalize(d_o, dim=-1) * delta.norm(dim=-1, keepdim=True)
                    jobs.append(({"layer": la, "group": grp, "source": "other"}, {la: AddRows(d_o, pos)}))
        for wname, wl in windows.items():
            for grp in GROUPS:
                pos = g[grp]
                for src in ("dissoc", "same"):
                    edits = {la: SetRows(h[src][la][pos], pos) for la in wl}
                    jobs.append(({"layer": wname, "group": grp, "source": src}, edits))
        read_ids = torch.tensor([prep["read_ids"]["base"]], device="cuda")
        logits_unedited = None
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            _, logits = model.generate_batch(read_ids, 1, [e for _, e in chunk], first_logits=True)
            logp = logits.log_softmax(-1)
            for row, (tags, _) in enumerate(chunk):
                top = int(logits[row].argmax())
                digit = digit_tok.get(top)
                rm, pr = (o_roles, o_preds) if tags["source"] == "other" else (roles, preds)
                role = rm.get(digit, "other_digit") if digit is not None else "other"
                p = {h_: round(float(logp[row, S.ids(tok, v)[0]].exp()), 4) for h_, v in pr.items() if v != "-"}
                outcomes.append({"family": c["family"], "domain": c["domain"], "level": c["level"], "name": c["id"],
                                 "n_entities": c["n_entities"], "slot": slot_class(c), **tags, "top": tok.decode([top]),
                                 "role": role, "p": p})  # fmt: skip
                if tags["source"] == "unedited":
                    logits_unedited = logits[row].clone()
                elif tags["source"] == "self":
                    assert logits_unedited is not None
                    checks.append({"name": c["id"], "check": "self_noop", "same_top": top == int(logits_unedited.argmax()),
                                   "max_abs_dlogit": round(float((logits[row] - logits_unedited).abs().max()), 4)})  # fmt: skip
                elif tags["group"] == "all":
                    src_logits = runs["dissoc"][0]
                    checks.append({"name": c["id"], "check": "layer0_all_reproduces_source",
                                   "same_top": top == int(src_logits.argmax()),
                                   "max_abs_dlogit": round(float((logits[row] - src_logits).abs().max()), 4)})  # fmt: skip
    write_jsonl(out_dir / "cases.jsonl", [{"id": c["id"], "family": c["family"], "domain": c["domain"],
                                           "level": c["level"]} for c in cases])  # fmt: skip
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "checks.jsonl", checks)
    summary = summarise(outcomes, checks, m)
    summary |= {"counts": counts, "seconds": round(time.time() - t0), "edited_reads": len(outcomes)}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(name, summary))
    print((out_dir / "summary.md").read_text())


# ---- summaries ------------------------------------------------------------------------------------------------------


def cell_rates(rows: list[dict]) -> dict[str, Any]:
    n = len(rows)
    roles = collections.Counter(r["role"] for r in rows)
    return {"n": n, **{k: [round(x, 4) for x in wilson(roles[k], n)] for k in ROLES if roles[k] or k in PV.HYPOTHESES}}


def verdict(fam: str, d: dict, same: dict | None, chance: dict[str, float], n_ent: int) -> str:
    """The docstring's decision rule for one cell."""
    if not d or not d["n"]:
        return "no data"
    changed = wilson(d["n"] - round(d["none"][0] * d["n"]), d["n"])
    if same is not None and same["n"]:
        same_changed = wilson(same["n"] - round(same["none"][0] * same["n"]), same["n"])
        if same_changed[2] > DAMAGE_MAX:
            return "damage"
    if changed[1] < CHANGED_MIN:
        return "none"
    cands = ("identity", "position") if fam == "RR" else ("identity", "position", "value")
    ctx = d.get("context", [0.0, 0.0, 0.0])
    per_digit = ctx[2] / (n_ent - 3) if n_ent > 3 else 0.0
    for x in cands:
        others = [d[y][2] for y in cands if y != x]
        bar = max(chance.get(x, 0.0), per_digit)
        if d[x][1] > max(others) and d[x][1] > bar:
            return x
    return "mixed"


def summarise(outcomes: list[dict], checks: list[dict], m: dict) -> dict[str, Any]:
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    for o in outcomes:
        if o["source"] in ("unedited", "self") or o["group"] == "all":
            continue
        for dom in (o["domain"], "all"):
            cells[(o["family"], dom, o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
        if o["source"] == "dissoc":
            cells[(o["family"], f"slot_{o['slot']}", o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
    rates = {"|".join(k): cell_rates(v) for k, v in cells.items()}
    windows = m["windows"]
    verdicts: dict[str, dict[str, str]] = {}
    for key, d in rates.items():
        fam, dom, lv, grp, layer, src = key.split("|")
        if dom != "all" or src != "dissoc":
            continue
        same = rates.get("|".join((fam, dom, lv, grp, layer, "same")))
        layers = windows.get(layer, [int(layer)] if layer.lstrip("-").isdigit() else [])
        chance: dict[str, float] = {}
        for la in layers:
            r = rates.get("|".join((fam, dom, lv, grp, str(la), "rand")))
            for x in PV.HYPOTHESES:
                if r and x in r:
                    chance[x] = max(chance.get(x, 0.0), r[x][2])
        n_ent = int(lv[1])
        verdicts.setdefault(f"{fam}|{lv}|{grp}", {})[layer] = verdict(fam, d, same, chance, n_ent)
    chk: dict[str, Any] = {}
    for kind in ("self_noop", "layer0_all_reproduces_source"):
        rows = [c for c in checks if c["check"] == kind]
        if rows:
            chk[kind] = {"n": len(rows), "same_top": sum(c["same_top"] for c in rows),
                         "max_abs_dlogit_max": max(c["max_abs_dlogit"] for c in rows)}  # fmt: skip
    unedited = [o for o in outcomes if o["source"] == "unedited"]
    chk["unedited_base_answer_read"] = {"n": len(unedited), "base_answer": sum(o["role"] == "none" for o in unedited)}
    primary = {k: v.get("transit") for k, v in verdicts.items() if k.startswith("RL|") and k.endswith("|final")}
    return {"rates": rates, "verdicts": verdicts, "checks": chk, "primary_RL_final_transit": primary}


def summary_md(name: str, s: dict) -> str:
    lines = [f"# {EXP} / {name}", "", f"Checks: {json.dumps(s['checks'])}", "",
             f"Primary (RL, final, transit window): {json.dumps(s['primary_RL_final_transit'])}", "",
             "## Verdicts (dissoc, pooled over domains), per layer / window", ""]  # fmt: skip
    for k, v in s["verdicts"].items():
        lines.append(f"- {k}: " + ", ".join(f"{la}: {x}" for la, x in v.items()))
    lines += ["", "## Shares (pooled over domains): role rate [95% CI]", "",
              "| family | level | group | layer | source | n | none | identity | position | value | context | other |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, d in s["rates"].items():
        fam, dom, lv, grp, layer, src = key.split("|")
        if dom != "all":
            continue

        def f(r, d=d):
            x = d.get(r)
            return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f},{100 * x[2]:.0f}]" if x else "-"

        oth = sum(d[r][0] for r in ("recall", "other_digit", "other") if r in d)
        lines.append(f"| {fam} | {lv} | {grp} | {layer} | {src} | {d['n']} | {f('none')} | {f('identity')} | "
                     f"{f('position')} | {f('value')} | {f('context')} | {100 * oth:.0f}% |")  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_summarise(name: str) -> None:
    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    checks = [json.loads(x) for x in (run_dir / "checks.jsonl").read_text().splitlines()]
    out = run_dir / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    s = summarise(rows, checks, m)
    (out / "summary.json").write_text(json.dumps(s, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(name, s))
    print("wrote", out)


# ---- analysis (CPU: re-applies the pre-registered rule to a finished run, with domain and slot cuts) -----------------

# The 'same' control's Wilson upper bound at zero changes is 3.84 / (n + 3.84): <= DAMAGE_MAX only from n = 35, so a
# cell with fewer items can never be interpretable under the rule (d3_pilot_27b's "damage" everywhere).
MIN_N_RULE = 35
CUT_KINDS = ("all", "domain", "slot")
SUPERSEDED = {  # shown in figure notes and reports: plain words, no run ids
    "d3_pilot_27b": "pilot with 34 prompts per family: below 35 the rule's control bound cannot pass, so every cell "
    "reads 'damage'; includes topics that failed the competence check",
    "d3_main_27b": "includes months and planets, whose memory → prompt / memory → memory prompts fail the "
    "pre-registered competence check (months memory → prompt 46%, planets memory → memory 55%, planets memory → "
    "prompt lower bound 0.84)",
    "d3_pilot_levels_27b": "includes topics that failed the competence check and only 15 prompts per topic",
    "d3_smoke_27b": "smoke run: 1 prompt per topic, competence check skipped; a code-path and timing check, not a result",
}


def roles_of(rows: list[dict]) -> dict[str, Any]:
    """n, role counts, Wilson (rate, lo, hi) per role and for 'changed' (any role but none)."""
    n = len(rows)
    k = collections.Counter(r["role"] for r in rows)
    out: dict[str, Any] = {"n": n, "k": dict(k)}
    for role in ROLES:
        out[role] = [round(x, 4) for x in wilson(k[role], n)]
    out["changed"] = [round(x, 4) for x in wilson(n - k["none"], n)]
    return out


def newcombe(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float, float]:
    """Difference of two independent proportions with Newcombe's hybrid Wilson interval (method 10)."""
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d, d - ((p1 - l1) ** 2 + (u2 - p2) ** 2) ** 0.5, d + ((u1 - p1) ** 2 + (p2 - l2) ** 2) ** 0.5)


def analyze(m: dict, rows: list[dict], checks: list[dict]) -> dict[str, Any]:
    """Every cell (family x cut x level x group x layer/window x source) with its rates; the rule's verdict for every
    dissoc cell, flagged where n < MIN_N_RULE makes it unreachable; strongest layers; level contrasts."""
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    for o in rows:
        if o["source"] not in SOURCES or o["group"] == "all":
            continue
        for cut in ("all", f"domain:{o['domain']}", f"slot:{o['slot']}"):
            cells[(o["family"], cut, o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
    rates = {"|".join(k): roles_of(v) for k, v in cells.items()}
    windows = m["windows"]
    verdicts: dict[str, Any] = {}
    for key, d in rates.items():
        fam, cut, lv, grp, layer, src = key.split("|")
        if src != "dissoc":
            continue
        same = rates.get("|".join((fam, cut, lv, grp, layer, "same")))
        chance: dict[str, float] = {}
        for la in windows.get(layer, [int(layer)] if layer.lstrip("-").isdigit() else []):
            r = rates.get("|".join((fam, cut, lv, grp, str(la), "rand")))
            for x in PV.HYPOTHESES:
                if r:
                    chance[x] = max(chance.get(x, 0.0), r[x][2])
        n_same = same["n"] if same else 0
        verdicts["|".join((fam, cut, lv, grp, layer))] = {
            "verdict": verdict(fam, d, same, chance, int(lv[1])),
            "n": d["n"],
            "n_same": n_same,
            "rule_reachable": min(d["n"], n_same) >= MIN_N_RULE,
            "chance_bar": chance,
        }
    single = [la for la in m["layers"]]
    strongest: dict[str, Any] = {}
    for fam in m["families"]:
        for lv in m["levels"]:
            for grp in GROUPS:
                cand = [
                    (rates[k]["changed"][0], la) for la in single if (k := f"{fam}|all|{lv}|{grp}|{la}|dissoc") in rates
                ]
                if not cand:
                    continue
                best = max(cand, key=lambda t: (t[0], -t[1]))[1]
                d = rates[f"{fam}|all|{lv}|{grp}|{best}|dissoc"]
                strongest[f"{fam}|{lv}|{grp}"] = {"layer": best, **{r: d[r] for r in ("changed", *PV.HYPOTHESES)}}
    levels: dict[str, Any] = {}
    if "e5f0" in m["levels"] and len(m["levels"]) > 1:
        for lv in m["levels"]:
            if lv == "e5f0":
                continue
            for grp in ("final", "last"):
                a, b = rates.get(f"RL|all|{lv}|{grp}|transit|dissoc"), rates.get(f"RL|all|e5f0|{grp}|transit|dissoc")
                if not a or not b:
                    continue
                ok = all(
                    verdicts[f"RL|all|{x}|{grp}|transit"]["verdict"] not in ("none", "damage") for x in (lv, "e5f0")
                )
                diffs = {}
                for role in PV.HYPOTHESES:
                    dd = newcombe(a["k"].get(role, 0), a["n"], b["k"].get(role, 0), b["n"])
                    label = (
                        "same"
                        if dd[1] >= -0.15 and dd[2] <= 0.15
                        else "differs"
                        if (dd[1] > 0 or dd[2] < 0) and abs(dd[0]) > 0.15
                        else "unclear"
                    )
                    diffs[role] = {"diff": [round(x, 4) for x in dd], "label": label}
                levels[f"{lv}_vs_e5f0|{grp}"] = {"interpretable": ok, "diffs": diffs}
    chk: dict[str, Any] = {}
    for kind in ("self_noop", "layer0_all_reproduces_source"):
        cr = [c for c in checks if c["check"] == kind]
        if cr:
            chk[kind] = {"n": len(cr), "same_top": sum(c["same_top"] for c in cr),
                         "max_abs_dlogit_max": max(c["max_abs_dlogit"] for c in cr)}  # fmt: skip
    unedited = [o for o in rows if o["source"] == "unedited"]
    chk["unedited_base_answer_read"] = {"n": len(unedited), "base_answer": sum(o["role"] == "none" for o in unedited)}
    unreachable = sorted(k for k, v in verdicts.items() if not v["rule_reachable"])
    return {
        "run": m["run"],
        "superseded": SUPERSEDED.get(m["run"]),
        "levels": m["levels"],
        "domains": sorted({o["domain"] for o in rows}),
        "n_per_family": {
            f"{f}|{lv}": rates[f"{f}|all|{lv}|final|transit|dissoc"]["n"]
            for f in m["families"]
            for lv in m["levels"]
            if f"{f}|all|{lv}|final|transit|dissoc" in rates
        },
        "checks": chk,
        "primary": {
            lv: {
                "verdict": verdicts.get(f"RL|all|{lv}|final|transit", {}),
                "rates": rates.get(f"RL|all|{lv}|final|transit|dissoc"),
            }
            for lv in m["levels"]
        },
        "strongest_layer": strongest,
        "level_contrasts": levels,
        "verdicts": verdicts,
        "rule_unreachable_cells": {"count": len(unreachable), "cuts": sorted({k.split("|")[1] for k in unreachable})},
        "rates": rates,
    }


def load_run(name: str) -> tuple[dict, list[dict], list[dict]]:
    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    checks = [json.loads(x) for x in (run_dir / "checks.jsonl").read_text().splitlines()]
    return m, rows, checks


def stage_analyze(name: str) -> Path:
    m, rows, checks = load_run(name)
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-rule"
    out.mkdir()
    a = analyze(m, rows, checks)
    (out / "summary.json").write_text(json.dumps(a, indent=1) + "\n")
    print("wrote", out)
    return out


def near_ties(rows: list[dict], gap: float = 0.1) -> dict[str, Any]:
    """Among dissoc reads whose top token is a predicted digit, the share where the runner-up prediction's p is within
    `gap` of the winner's (bf16 batch noise could flip those)."""
    win = [o for o in rows if o["source"] == "dissoc" and o["role"] in PV.HYPOTHESES and o["group"] != "all"]
    close = 0
    for o in win:
        ps = sorted({o["p"].get(h, 0.0) for h in PV.HYPOTHESES if h in o["p"]}, reverse=True)
        close += len(ps) > 1 and ps[0] - ps[1] < gap
    return {"n": len(win), "within_gap": close, "gap": gap}


# ---- figures (CPU) --------------------------------------------------------------------------------------------------

# Outcome hues: the reference categorical palette's first three slots (validated: adjacent CVD dE >= 9.2, normal-vision
# >= 27.6 on the light surface; aqua is below 3:1 contrast, so lines carry direct labels). 'none' and every control are
# grey: they are baselines, not identities.
OUTCOME_COLOR = {"identity": "#2a78d6", "position": "#eb6834", "value": "#1baf7a"}
NONE_COLOR = "#52514e"
CONTROL_STYLE = {
    "same": ("#898781", (0, (4, 2))),
    "rand": ("#898781", (0, (1, 1.6))),
    "other": ("#b5b3aa", (0, (6, 2, 1, 2))),
}
# Display terms for an outside reader (figure_terms.md, 2026-10-21): org prompt = the base, alt prompt = the source,
# bridge alt = the entity the alt prompt asks about.
OUTCOME_TERM = {
    "identity": "answer of bridge alt's statement",
    "position": "answer at the same statement slot",
    "value": "the alt prompt's own answer",
    "none": "answer org kept",
}
OUTCOME_SHORT = {"identity": "bridge alt's statement", "position": "same slot", "value": "alt prompt's answer"}
GROUP_SHORT = {
    "question": "question words",
    "final": "after the question",
    "last": "last 2 tokens",
    "both": "question + after",
}
OUTCOME_HELP = {
    "identity": "org prompt's digit for bridge alt",
    "position": "org prompt's digit in bridge alt's slot",
    "value": "not in the org prompt",
    "none": "",
}
CONTROL_LABEL = {
    "same": "control: same entity, statements reshuffled (% changed)",
    "rand": "control: random push, same size (% changed)",
    "other": "control: another topic's prompt, same size (% changed)",
}
GROUP_TITLE = {
    "question": "question words",
    "final": "everything after the question",
    "last": "last two tokens before the answer",
    "both": "question words + everything after",
}
FAMILY_TITLE = {  # display names (the user's rule: never the letter codes): where the bridge comes from -> the answer
    "RL": "memory → prompt (recalled cue, prompt lookup)",
    "DL": "named → prompt (entity named, prompt lookup)",
    "RR": "memory → memory (recalled cue, recalled fact)",
}
_CODE_RE = re.compile(r"(?<![\w|/`=-])(BLR|BRL|RL|RR|DL|BL|BR)(?![\w|/`-])")


def plain(text: str) -> str:
    """Family codes replaced by their display names, outside `code spans` (data keys keep their codes there)."""
    from bridge_jspace.plotting import family_label

    words = (("base's residual", "org prompt's hidden states"), ("dissoc source's", "alt prompt's"),
             ("the dissoc source", "the alt prompt"), ("dissoc", "alt prompt"),
             ("the 'same' control", "the same-entity control (statements reshuffled)"),
             ("'same' control", "same-entity control"), ("'same' changes", "same-entity control changes"),
             ("the same control", "the same-entity control (statements reshuffled)"),
             ("same control", "same-entity control"), ("the rand control", "the random-push control"),
             ("rand control", "random-push control"), ("random-direction control", "random-push control"),
             ("random direction changed", "random push of the same size changed"),
             ("other item changed", "another domain's prompt changed"), ("| same n |", "| control n |"))  # fmt: skip
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = _CODE_RE.sub(lambda mm: family_label(mm.group(1)), parts[i])
        for old, new in words:
            parts[i] = parts[i].replace(old, new)
    return "`".join(parts)


VERDICT_TERM = {
    "identity": "bridge alt's statement (H-word)",
    "position": "same statement slot (H-pointer)",
    "value": "alt prompt's own answer (H-value)",
    "none": "no effect",
    "mixed": "mixed",
    "damage": "damage",
    "no data": "no data",
}


def rule_plain(text: str) -> str:
    """The pre-registered rule with its outcome names in the outside reader's terms (the variable X renamed W)."""
    text = re.sub(r"\bX\b", "W", text)
    for old, new in (("identity", OUTCOME_TERM["identity"]), ("position", OUTCOME_TERM["position"]),
                     ("value", OUTCOME_TERM["value"]), ("share none", f"share '{OUTCOME_TERM['none']}'")):  # fmt: skip
        text = re.sub(rf"\b{old}\b", new, text)
    return text


def example_line(m: dict, name: str) -> str:
    """One shortened prompt pair in outside-reader terms, from the run's examples.json (a memory → prompt item whose
    patch gave the same-slot answer, else the first example)."""
    ex = RESULTS / name / "examples.json"
    if not ex.exists():
        return ""
    e = json.loads(ex.read_text())["examples"]
    pick = next((x for x in e if x["family"] == "RL" and x["group"] == "position"), None) or (e[0] if e else None)
    if not pick:
        return ""
    it = next((i for its in load_items(m).values() for i in its if i["id"] == pick["item_id"]), None)
    if not it:
        return ""
    d, sl = it["sources"]["dissoc"], it["slots"]
    k = sl["position"]
    nth = {0: "1st", 1: "2nd", 2: "3rd"}.get(k, f"{k + 1}th")
    exp = d["predictions"]
    stmt = PV.DOMAINS[it["domain"]]["statement"]
    shown = sorted({sl["query"], sl["identity"], k})
    org = " ... ".join(stmt.format(e=it["entities"][j], d=it["digits"][j]) for j in shown)
    return (
        f'org prompt "... {org} ... {it["question"]}" -> answer org {exp["none"]}; the alt prompt asks about the '
        f"{d['query']} (bridge alt), its {nth} statement. Possible answers after the patch: {exp['identity']} (answer "
        f"of bridge alt's statement), {exp['position']} (answer at the same statement slot), {exp['value']} (the alt "
        f"prompt's own answer), {exp['none']} (answer org kept)."
    )


def _series(
    a: dict, prefix: str, layers: list[int], src: str, role: str
) -> tuple[list[int], list[float], list[float], list[float]]:
    xs, r, lo, hi = [], [], [], []
    for la in layers:
        d = a["rates"].get(f"{prefix}|{la}|{src}")
        if d:
            xs.append(la)
            r.append(d[role][0])
            lo.append(max(0.0, d[role][1]))
            hi.append(d[role][2])
    return xs, r, lo, hi


def _band(ax, lo: int, hi: int, text: str | None) -> None:
    from bridge_jspace.plotting import GRID, MUTED

    ax.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    if text:
        ax.annotate(text, ((lo + hi) / 2, 1), xycoords=("data", "axes fraction"), xytext=(0, -3),
                    textcoords="offset points", ha="center", va="top", fontsize=7, color=MUTED)  # fmt: skip


def _panel(
    ax, a: dict, m: dict, fam: str, cut: str, lv: str, grp: str, controls=("same", "rand", "other"), band=True
) -> int:
    """Outcome shares by layer for one cell, with Wilson bands, the 'none' share, and each control's change rate."""
    from bridge_jspace.plotting import percent_axis, style_axes

    style_axes(ax)
    layers = sorted(m["layers"])
    prefix = f"{fam}|{cut}|{lv}|{grp}"
    tr = m["windows"]["transit"]
    if band:
        _band(ax, tr[0], tr[-1], None)  # labelled once, in the legend
    n = 0
    roles = ("identity", "position") if fam == "RR" else ("identity", "position", "value")
    for role in roles:
        xs, r, lo, hi = _series(a, prefix, layers, "dissoc", role)
        if not xs:
            continue
        near = [r[j] > 0 or (j > 0 and r[j - 1] > 0) or (j + 1 < len(r) and r[j + 1] > 0) for j in range(len(r))]
        ax.fill_between(xs, lo, hi, where=near, color=OUTCOME_COLOR[role], alpha=0.14, lw=0)
        ax.plot(xs, r, color=OUTCOME_COLOR[role], lw=2, solid_capstyle="round")
    xs, r, _, _ = _series(a, prefix, layers, "dissoc", "none")
    ax.plot(xs, r, color=NONE_COLOR, lw=1.1)
    for src in controls:
        xs, r, _, _ = _series(a, prefix, layers, src, "changed")
        if xs:
            col, ls = CONTROL_STYLE[src]
            ax.plot(xs, r, color=col, lw=1.2, ls=ls, marker="o" if src != "same" else None, ms=2.5)
    d = a["rates"].get(f"{prefix}|{layers[0]}|dissoc")
    n = d["n"] if d else 0
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlim(layers[0] - 1, layers[-1] + 1)
    percent_axis(ax)
    return n


def _handles(fams: list[str], controls=("same", "rand", "other")) -> list:
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import GRID

    h: list[Any] = [Line2D([], [], color=OUTCOME_COLOR[r], lw=2,
                label=f"% that become {OUTCOME_TERM[r].removeprefix('the ')} ({OUTCOME_HELP[r]})")
         for r in ("identity", "position", "value")]  # fmt: skip
    h.append(Line2D([], [], color=NONE_COLOR, lw=1.1, label="% of original answers kept (answer org kept)"))
    tr = default_windows()["transit"]
    h.append(
        Patch(
            color=GRID, alpha=0.7, lw=0, label=f"layers {tr[0]}-{tr[-1]}: the lens reads the bridge but cannot steer it"
        )
    )
    for src in controls:
        col, ls = CONTROL_STYLE[src]
        h.append(
            Line2D(
                [],
                [],
                color=col,
                lw=1.2,
                ls=ls,
                marker="o" if src != "same" else None,
                ms=2.5,
                label=CONTROL_LABEL[src],
            )
        )
    return h


def _finish(fig, path: Path, title: str, rows: list[tuple[str, str]], handles: list, ncols: int = 2) -> list[str]:
    """plotting.finish's frame with its labelled caption rows (What we did / Example / How to read / Control / Data),
    legend below; saved as PNG at 200 dpi and as SVG (plotting.finish saves one PNG at 150 dpi)."""
    import textwrap

    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, SURFACE

    h, w = fig.get_figheight(), fig.get_figwidth()
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=INK)
    label_w, y = 1.05, 0.38
    for label, text in rows:
        lines = textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]
        fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=INK, fontweight="bold")
        fig.text(
            label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=MUTED, linespacing=1.4
        )
        y += 0.155 * len(lines) + 0.05
    head = y + 0.1
    n_rows = -(-len(handles) // ncols)
    foot = 0.2 + 0.25 * n_rows
    fig.legend(handles=handles, loc="lower center", ncols=ncols, frameon=False, fontsize=8, labelcolor=INK,
               handlelength=3.2, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    out = []
    for ext in ("png", "svg"):
        p = path.with_suffix(f".{ext}")
        fig.savefig(p, dpi=200, facecolor=SURFACE)
        out.append(p.name)
    plt.close(fig)
    return out


def _caption(
    a: dict,
    m: dict,
    lv: str,
    patched: str,
    how: str,
    windows: bool = False,
    all_levels: bool = False,
    control: str | None = None,
) -> list[tuple[str, str]]:
    """The caption rows (figure_terms.md's CAPTION FORMAT): What we did, Example, How to read, Control, Data."""
    levels = {"e3f0": "3 statements", "e5f0": "5 statements", "e5f4": "5 statements with filler sentences between them"}
    level = "3 or 5 statements" if all_levels else levels[lv]
    when = "at every layer of a window at once" if windows else "one layer at a time"
    n = {f: a["n_per_family"].get(f"{f}|{lv}") for f in m["families"]}
    if all_levels:
        n = {f: "/".join(str(a["n_per_family"].get(f"{f}|{x}")) for x in m["levels"]) for f in m["families"]}
    ns = ", ".join(f"{FAMILY_TITLE[f].split(' (')[0]} {v}" for f, v in n.items())
    rows = [
        ("What we did", f"The org prompt lists {level} (an entity and its locker digit each). We copied the alt "
         f"prompt's hidden states ({patched}) into the org prompt, {when}, and read the answer."),
        ("Example", a.get("example_line", "")),
        ("How to read", how),
        ("Control", control or "Grey: the same patch from a prompt asking about the same entity with the statements "
         "reshuffled, a random push of the same size, and a prompt from another topic. The first two should change "
         "nothing."),
        ("Data", f"Qwen3.6-27B; topics: {', '.join(a['domains'])}; {ns} prompts per family; "
         + ("bars" if windows else "shading") + " = 95% Wilson interval over prompts."),
    ]  # fmt: skip
    if a["superseded"]:
        rows.insert(0, ("Not a headline", a["superseded"]))
    return [(k, plain(v)) for k, v in rows if v]


def fig_by_layer(a: dict, m: dict, lv: str, path: Path, headline: bool = False) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, grps = m["families"], ("question", "final", "last")
    fig, axes = plt.subplots(
        len(grps), len(fams), figsize=(4.2 * len(fams), 2.6 * len(grps) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    for i, grp in enumerate(grps):
        for j, fam in enumerate(fams):
            ax = axes[i][j]
            _panel(ax, a, m, fam, "all", lv, grp)
            if i == 0:
                ax.set_title(FAMILY_TITLE[fam], fontsize=10, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel(f"patched: {GROUP_SHORT[grp]}\n% of original answers", fontsize=9, color=INK)
            if i == len(grps) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    title = ("Patch from the alt prompt: does the answer follow bridge alt's statement, its slot, or the alt "
             "prompt's own answer?") if headline else (
             f"Patch from the alt prompt: which answer does the org prompt give, by layer and patched tokens? ({lv})")  # fmt: skip
    rows = _caption(
        a,
        m,
        lv,
        "rows: question words / everything after the question / the last 2 tokens",
        "Each coloured line: % of original answers that become that answer after the patch; dark line: % of original answers kept. Grey band: layers 44-52, where the lens reads this bridge but cannot steer it.",
    )
    return _finish(fig, path, title, rows, _handles(fams), ncols=2)


def fig_slots(a: dict, m: dict, lv: str, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, slots = m["families"], ("first", "middle", "last")
    fig, axes = plt.subplots(
        len(fams), 3, figsize=(12.6, 2.6 * len(fams) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    for i, fam in enumerate(fams):
        for j, slot in enumerate(slots):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, f"slot:{slot}", lv, grp, controls=("same",))
            ok = n >= MIN_N_RULE
            ax.set_title(f"{plain(fam)} · {slot} (n={n}{'' if ok else ', too few'})",
                         fontsize=9, color=INK, loc="left")  # fmt: skip
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    rows = _caption(a, m, lv, GROUP_TITLE[grp], "Columns: bridge org's statement is the first, a middle or the last "
                    f"one in the org prompt. Lines as in the main figure. Panels with fewer than {MIN_N_RULE} prompts "
                    "cannot pass the pre-registered rule.", control="Grey dashed: the same patch from a prompt about "
                    "the same entity with the statements reshuffled; it should change nothing.")  # fmt: skip
    return _finish(fig, path, "Does it matter where bridge org's statement sits (first, middle, last)?",
                   rows, _handles(fams, ("same",)), ncols=2)  # fmt: skip


def fig_domains(a: dict, m: dict, lv: str, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, doms = m["families"], a["domains"]
    fig, axes = plt.subplots(
        len(fams), len(doms), figsize=(4.2 * len(doms), 2.6 * len(fams) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    for i, fam in enumerate(fams):
        for j, dom in enumerate(doms):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, f"domain:{dom}", lv, grp)
            ax.set_title(f"{plain(fam)} · {dom} (n={n})", fontsize=9, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    rows = _caption(
        a, m, lv, GROUP_TITLE[grp], "One column per topic; lines as in the main figure. Grey band: layers 44-52."
    )
    return _finish(fig, path, "Is the pattern the same for each topic?", rows, _handles(fams), ncols=2)


def fig_levels(a: dict, m: dict, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, lvs = m["families"], m["levels"]
    fig, axes = plt.subplots(
        len(fams), len(lvs), figsize=(4.2 * len(lvs), 2.6 * len(fams) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    names = {"e3f0": "3 statements", "e5f0": "5 statements", "e5f4": "5 statements + filler"}
    for i, fam in enumerate(fams):
        for j, lv in enumerate(lvs):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, "all", lv, grp)
            ax.set_title(f"{plain(fam)} · {names[lv]} (n={n})", fontsize=9, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    rows = _caption(a, m, lvs[0], GROUP_TITLE[grp], "One column per prompt layout (3 statements; 5; 5 with filler "
                    "sentences between them); lines as in the main figure.", all_levels=True)  # fmt: skip
    return _finish(fig, path, "Does the split change with 3 statements, or with filler between the statements?", rows,
                   _handles(fams), ncols=2)  # fmt: skip


def fig_windows(a: dict, m: dict, lv: str, path: Path) -> list[str]:
    """The window patches (every layer of the window at once): each outcome's share with its Wilson interval, next to
    the 'same' control's change rate."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, percent_axis, style_axes

    fams, grps, wins = m["families"], GROUPS, list(m["windows"])
    roles = ("none", "identity", "position", "value")
    col = {"none": NONE_COLOR, **OUTCOME_COLOR}
    fig, axes = plt.subplots(
        len(grps), len(fams), figsize=(4.2 * len(fams), 2.3 * len(grps) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    for i, grp in enumerate(grps):
        for j, fam in enumerate(fams):
            ax = axes[i][j]
            style_axes(ax)
            for wi, w in enumerate(wins):
                d = a["rates"].get(f"{fam}|all|{lv}|{grp}|{w}|dissoc")
                s = a["rates"].get(f"{fam}|all|{lv}|{grp}|{w}|same")
                if not d:
                    continue
                for ri, role in enumerate(roles):
                    if fam == "RR" and role == "value":
                        continue
                    x = wi + (ri - 1.5) * 0.17
                    r, lo, hi = d[role]
                    ax.errorbar([x], [r], yerr=[[r - max(lo, 0)], [hi - r]], fmt="o", ms=5, color=col[role], ecolor=col[role], elinewidth=1.4, capsize=0)  # fmt: skip
                if s:
                    r, lo, hi = s["changed"]
                    ax.errorbar([wi + 0.42], [r], yerr=[[r - max(lo, 0)], [hi - r]], fmt="s", ms=4, mfc="none",
                                color=CONTROL_STYLE["same"][0], elinewidth=1, capsize=0)  # fmt: skip
            ax.set_xticks(
                range(len(wins)), [f"{w}\n{m['windows'][w][0]}-{m['windows'][w][-1]}" for w in wins], fontsize=8
            )
            ax.set_ylim(-0.02, 1.05)
            percent_axis(ax)
            if i == 0:
                ax.set_title(FAMILY_TITLE[fam], fontsize=10, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel(f"patched: {GROUP_SHORT[grp]}\n% of original answers", fontsize=9, color=INK)
    handles = [Line2D([], [], color=col[r], marker="o", ls="none", ms=5,
                      label="% of original answers kept" if r == "none" else f"% that become {OUTCOME_TERM[r].removeprefix('the ')}")
               for r in roles]  # fmt: skip
    handles.append(Line2D([], [], color=CONTROL_STYLE["same"][0], marker="s", mfc="none", ls="none", ms=4,
                          label=CONTROL_LABEL["same"]))  # fmt: skip
    rows = _caption(a, m, lv, "rows: question words / everything after / the last 2 tokens / question + after",
                    "Each dot: % of original answers that become that answer when a whole window of layers is patched; "
                    "the pre-registered main test is memory → prompt, everything after the question, layers 44-52.",
                    windows=True, control="Grey squares: the same patch from a prompt about the same entity with the "
                    "statements reshuffled (% changed); it should change nothing.")  # fmt: skip
    return _finish(fig, path, "Patching a whole window of layers from the alt prompt: which answer wins?", rows,
                   handles, ncols=3)  # fmt: skip


PRIMARY_RUNS = ("d3_main_ae_27b", "d3_levels_animals_27b")
LEDGER = pins.RESULTS_DIR / "jobq" / "ledger.jsonl"


def _commit(name: str) -> str:
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            r = json.loads(line)
            if r.get("id") == name and r.get("commit"):
                return r["commit"][:7]
    return "unknown"


def _pct(x: list[float] | None) -> str:
    return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}]" if x else "-"


def _shares(d: dict | None, roles=("none", "identity", "position", "value")) -> str:
    return ", ".join(f"{OUTCOME_TERM[r]} {_pct(d[r])}" for r in roles) if d else "-"


COMPETENCE_RUN = "d3_competence_27b"


def dan_section(a: dict) -> list[str]:
    """Dan's written D3 predictions (jobs/predictions/2026-10-21_dan.md) next to this run's numbers. The numbers are
    computed; the last column is the agent's reading of them."""
    r, s = a["rates"], a["strongest_layer"]

    def sh(d: dict) -> str:
        return " / ".join(f"{100 * d[x][0]:.0f}" for x in ("identity", "position", "value", "none"))

    comp = PV.RESULTS / COMPETENCE_RUN / "summary.json"
    q31 = "-"
    if comp.exists():
        c = json.loads(comp.read_text())["labels"]
        q31 = "; ".join(f"{d} {_pct([c[f'main/{d}_RL_e5f0']['cells']['clean'][k] for k in ('rate', 'lo', 'hi')])}"
                        for d in PV.DOMAINS if f"main/{d}_RL_e5f0" in c)  # fmt: skip
    rq, rl = s["RL|e5f0|question"], s["RL|e5f0|last"]
    rl50 = r["RL|all|e5f0|last|50|dissoc"]
    slots = "; ".join(
        f"{sl} n={r[f'RL|slot:{sl}|e5f0|final|transit|dissoc']['n']} {OUTCOME_TERM['position']} "
        f"{_pct(r[f'RL|slot:{sl}|e5f0|final|transit|dissoc']['position'])}"
        for sl in ("first", "middle", "last")
    )
    rr, dq = s["RR|e5f0|question"], s["DL|e5f0|question"]
    rr_last = r["RR|all|e5f0|last|transit|dissoc"]
    dl_q = max((r[f"DL|all|e5f0|question|{la}|dissoc"]["position"][0], la) for la in range(16, 46, 2))
    dl_f50 = r["DL|all|e5f0|final|50|dissoc"]
    prim = r["RL|all|e5f0|final|transit|dissoc"]
    q_tr = r["RL|all|e5f0|question|transit|dissoc"]
    T = OUTCOME_TERM
    rows = [
        ("Q3.1 memory → prompt with 5 statements >= 80%?", "yes, >= 95%",
         f"org prompt answered (main, first 100 per topic): {q31}",
         "partly: >= 80% for 3 of 4 topics; >= 95% only for animals; months fail"),
        ("Q3.2 memory → prompt, patch the question words: shares at the strongest layer", "60 / 10 / 10 / 20",
         f"layer {rq['layer']}: {sh(rq)}", f"direction right ({T['identity']}), more extreme; from layer 40 on the "
         f"question words carry nothing (layers 44-52: {T['none']} {100 * q_tr['none'][0]:.0f}%)"),
        ("Q3.3 memory → prompt, patch only the last tokens", "80 / 10 / 5 / 5",
         f"strongest layer {rl['layer']}: {sh(rl)}; at layer 50: {sh(rl50)}",
         f"wrong: the last tokens give the {T['position']} (layer 50), then {T['value']} (52+); "
         f"{T['identity']} never above ~25%"),
        ("Q3.4 does it depend on where bridge org's statement sits?", "no",
         f"memory → prompt, everything after the question, layers 44-52: {slots}",
         "undetermined: first/last panels have n < 35 (the rule cannot pass); first is lowest, not highest as Mixing "
         "Mechanisms predicts"),
        ("Q3.5 memory → memory (a pointer is useless)", "85 / 5 / 5 / 5",
         f"question words, layer {rr['layer']}: {sh(rr)}; last two tokens, layers 44-52: {T['identity']} "
         f"{_pct(rr_last['identity'])}, {T['position']} {_pct(rr_last['position'])}",
         f"right: {T['identity']} (here the same digit as {T['value']}); {T['position']} ~0 everywhere"),
        ("Q3.5 named → prompt (direct question)", "80 / 5 / 5 / 10",
         f"question words, layer {dq['layer']}: {sh(dq)}; question words, layer {dl_q[1]}: {T['position']} "
         f"{100 * dl_q[0]:.0f}%; everything after the question, layer 50: {sh(dl_f50)}",
         f"partly wrong: from layer 28 the question words give the {T['position']} for ~40% of prompts, and the "
         f"tokens after the question give it before {T['value']}"),
        ("Q3.6 what the lens reads but cannot steer", "the word dominates; the statement's slot has little effect",
         f"memory → prompt, everything after the question, layers 44-52: {sh(prim)}",
         "contradicted at 44-52: the bridge is no longer on the question words; the tokens after the question carry "
         f"a pointer to the statement's slot ({T['position']}, more than {T['identity']}), then the answer itself; "
         "pooled verdict 'same statement slot', but 'mixed' for each topic alone"),
    ]  # fmt: skip
    out = ["", "## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D3) vs results", "",
           f"Shares are {T['identity']} / {T['position']} / {T['value']} / {T['none']}, in % of prompts.", "",
           "| question | Dan | result (this run unless said) | reading |", "|---|---|---|---|"]  # fmt: skip
    out += [f"| {q} | {d} | {res} | {rd} |" for q, d, res, rd in rows]
    return out


def prior_checks(m: dict, a: dict) -> list[str]:
    """Each job-spec hypothesis's numeric prediction against the run (main-type and levels-type runs)."""
    r = a["rates"]
    lvs = m["levels"]
    lv = "e5f0" if "e5f0" in lvs else lvs[0]
    T = OUTCOME_TERM

    def c(fam: str, grp: str, w: str = "transit", level: str = lv) -> dict:
        return r.get(f"{fam}|all|{level}|{grp}|{w}|dissoc") or {x: [float("nan")] * 3 for x in (*ROLES, "changed")}

    def onset(grp: str) -> int | None:
        return next((la for la in sorted(m["layers"]) if c("RL", grp, str(la))["value"][0] >= 0.2), None)

    def yn(ok: bool) -> str:
        return "met" if ok else "not met"

    if a["level_contrasts"]:
        out = []
        for k, cc in a["level_contrasts"].items():
            d = cc["diffs"]
            out.append(f"- {k} (interpretable: {cc['interpretable']}): " + ", ".join(
                f"{T[x]} {100 * d[x]['diff'][0]:+.0f} [{100 * d[x]['diff'][1]:+.0f}, {100 * d[x]['diff'][2]:+.0f}] "
                f"{d[x]['label']}" for x in PV.HYPOTHESES))  # fmt: skip
        win = max(("identity", "position", "value"), key=lambda x: c("RL", "final")[x][0])
        out.append(f"- H-robust / H-contiguity: this run's leading outcome at 5 statements (memory → prompt, everything "
                   f"after the question, layers 44-52) is '{T[win]}'; e5f4 vs e5f0 for it: see the rows above "
                   f"('same' = within 0.15 supports H-robust, 'differs' with a drop H-contiguity, 'unclear' neither).")  # fmt: skip
        out.append(f"- H-fewer-entities: the e3f0_vs_e5f0 '{T['position']}' entries above ('differs' with a positive "
                   "difference supports it).")  # fmt: skip
        return out
    f_, l_ = c("RL", "final"), c("RL", "last")
    rr_f, rr_l, dl_f = c("RR", "final"), c("RR", "last"), c("DL", "final")
    return [
        f"- H-pointer: memory → prompt, {T['position']}: after the question {_pct(f_['position'])}, last two tokens "
        f"{_pct(l_['position'])} (>= 50%: {yn(f_['position'][0] >= 0.5 or l_['position'][0] >= 0.5)}); memory → "
        f"memory {_pct(rr_f['position'])} / {_pct(rr_l['position'])} (<= 10%: "
        f"{yn(max(rr_f['position'][0], rr_l['position'][0]) <= 0.1)}); named → prompt after the question "
        f"{_pct(dl_f['position'])} (>= 50%: {yn(dl_f['position'][0] >= 0.5)})",
        f"- H-word: memory → prompt, {T['identity']}: {_pct(f_['identity'])} / {_pct(l_['identity'])} (>= 50%: "
        f"{yn(max(f_['identity'][0], l_['identity'][0]) >= 0.5)})",
        f"- H-value: memory → prompt, {T['value']}: {_pct(f_['value'])} / {_pct(l_['value'])} (>= 50%: "
        f"{yn(max(f_['value'][0], l_['value'][0]) >= 0.5)}); first single layer where it reaches 20%: after the "
        f"question {onset('final')}, last two tokens {onset('last')}",
        f"- H-none: memory → prompt, answer changed after the question {_pct(f_['changed'])} (< 20%: "
        f"{yn(f_['changed'][0] < 0.2)})",
    ]


def report_md(name: str, m: dict, a: dict, out: Path) -> str:
    """AGENTS.md's report block, the rule's verdicts (with cuts and reachability), checks, Dan's predictions, priors."""
    r, v = a["rates"], a["verdicts"]
    lvs = m["levels"]
    main_lv = "e5f0" if "e5f0" in lvs else lvs[0]
    n_fam = {k: x for k, x in a["n_per_family"].items()}
    prim = r.get(f"RL|all|{main_lv}|final|transit|dissoc")
    same = r.get(f"RL|all|{main_lv}|final|transit|same")
    tr = m["windows"]["transit"]
    rand_l = [r.get(f"RL|all|{main_lv}|final|{la}|rand") for la in tr]
    rand_changed = max((x["changed"] for x in rand_l if x), default=None, key=lambda t: t[0])
    other_l = [r.get(f"RL|all|{main_lv}|final|{la}|other") for la in tr]
    other_changed = max((x["changed"] for x in other_l if x), default=None, key=lambda t: t[0])
    where = out.relative_to(pins.REPO_ROOT) if out.is_relative_to(pins.REPO_ROOT) else out
    figs = [f"{where}/{f}" for fs in a["figures"].values() for f in fs if f.endswith(".png")]
    titles = pins.REPO_ROOT / "jobs" / "titles.yaml"
    title = name
    if titles.exists():
        import yaml

        title = (yaml.safe_load(titles.read_text()) or {}).get(name, name)
    lines = [f"# {title}", "", f"Run `{name}` (results/pointer_swap/), analysis of the saved outputs only.", ""]
    if a["superseded"]:
        lines += [f"**NOT A HEADLINE RUN (superseded or smoke)**: {a['superseded']}. Shown for completeness.", ""]
    seeds = json.dumps(list(m.get("seeds", {"sample": 0}).values()))
    lines += [
        "```",
        f"EXP {name} @ {_commit(name)} | model Qwen3.6-27B | n={json.dumps(n_fam)} | seeds={seeds} (sample, null, other)",
        "Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers "
        f"{tr[0]}-{tr[-1]}: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the "
        "answer (H-value)",
        f"Headline: RL, tokens after the question, transit window ({main_lv}): position = {_pct(prim['position']) if prim else '-'}   "
        f"Baseline: none = {_pct(prim['none']) if prim else '-'}, identity = {_pct(prim['identity']) if prim else '-'}, "
        f"value = {_pct(prim['value']) if prim else '-'}   Control: 'same' changed = {_pct(same['changed']) if same else '-'}; "
        f"random direction changed (max over transit layers) = {_pct(rand_changed)}; other item changed = {_pct(other_changed)}",
        f"Figures: {', '.join(figs)}",
        "Three dumbest ways this could be wrong: see below",
        f"For the human to verify: results/pointer_swap/{name}/outcomes.jsonl, rows `family == 'RL'`, "
        f"`group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == '{main_lv}'`: count `role` "
        f"(n={prim['n'] if prim else '-'}); position should be "
        f"{prim['k'].get('position', 0) if prim else '-'}, identity {prim['k'].get('identity', 0) if prim else '-'}, value "
        f"{prim['k'].get('value', 0) if prim else '-'}, none {prim['k'].get('none', 0) if prim else '-'}",
        "Status: UNVERIFIED",
        "```",
        "",
    ]
    ch = a["checks"]
    nt = a["near_ties"]
    dom_v = {dm: v.get(f"RL|domain:{dm}|{main_lv}|final|transit", {}).get("verdict") for dm in a["domains"]}
    dumb = [
        "Position here could be the absolute token offset rather than the statement's order: statements have equal "
        "length, so the two coincide (the filler level keeps the same layout in base and source and does not separate "
        "them). Not checked; needs an offset-shift variant.",
        f"Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. "
        f"Checked: the random-direction control at the same per-token norm changes RL's answer {_pct(rand_changed)} "
        f"(max over transit layers); digits of the base context that no hypothesis predicts win "
        f"{_pct(prim['context']) if prim else '-'}; among dissoc reads won by a predicted digit, "
        f"{nt['within_gap']}/{nt['n']} have the runner-up prediction within p {nt['gap']}; hook checks "
        f"self no-op {ch['self_noop']['same_top']}/{ch['self_noop']['n']}, layer-0 reproduction "
        f"{ch['layer0_all_reproduces_source']['same_top']}/{ch['layer0_all_reproduces_source']['n']}.",
        f"The pooled verdict could rest on pooling: per domain the same cell's verdict is {json.dumps(dom_v)}; the "
        f"spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.",
    ]
    lines += ["## Three dumbest ways this could be wrong", ""] + [f"{i + 1}. {t}" for i, t in enumerate(dumb)] + [""]
    lines += [
        "## Pre-registered decision rule and its verdict",
        "",
        "Rule (scripts/pointer_swap.py docstring, written before any run):",
        "",
        "> " + rule_plain(m["decision"].replace("\n", " ")),
        "",
        "Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): "
        + "; ".join(
            f"{lv}: **{VERDICT_TERM.get(a['primary'][lv]['verdict'].get('verdict', 'no data'))}** "
            f"({_shares(a['primary'][lv]['rates'])})"
            for lv in lvs
        ),
        "",
        f"A cell needs n >= {MIN_N_RULE} items for the 'same' control's Wilson upper bound to reach <= {DAMAGE_MAX} even "
        f"with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives "
        f"'damage'. Cells where the rule cannot pass: {a['rule_unreachable_cells']['count']}, in cuts "
        f"{a['rule_unreachable_cells']['cuts']}.",
        "",
        "| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |",
        "|---|---|---|---|---|---|",
    ]
    for fam in m["families"]:
        for grp in GROUPS:
            for lv in lvs:
                cells = []
                for w in m["windows"]:
                    vv = v.get(f"{fam}|all|{lv}|{grp}|{w}", {})
                    d = r.get(f"{fam}|all|{lv}|{grp}|{w}|dissoc")
                    top = max(("identity", "position", "value"), key=lambda x: d[x][0]) if d else None
                    cells.append(
                        f"{VERDICT_TERM.get(vv.get('verdict', '-'), '-')} (answer org kept {100 * d['none'][0]:.0f}%, "
                        f"{OUTCOME_TERM[top]} {100 * d[top][0]:.0f}%)"
                        if d and top
                        else "-"
                    )
                lines.append(f"| {fam} | {GROUP_TITLE[grp]} | {lv} | " + " | ".join(cells) + " |")
    lines += ["", "Cuts of the primary cell (RL, tokens after the question, transit window):", "",
              "| cut | level | n | same n | verdict | rule reachable | shares |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for lv in lvs:
        for cut in ["all", *(f"domain:{d}" for d in a["domains"]), "slot:first", "slot:middle", "slot:last"]:
            vv = v.get(f"RL|{cut}|{lv}|final|transit")
            if not vv:
                continue
            d = r.get(f"RL|{cut}|{lv}|final|transit|dissoc")
            sm = r.get(f"RL|{cut}|{lv}|final|transit|same")
            dmg = f" ({sm['n'] - sm['k'].get('none', 0)} 'same' changes)" if vv["verdict"] == "damage" and sm else ""
            lines.append(f"| {cut} | {lv} | {vv['n']} | {vv['n_same']} | {VERDICT_TERM[vv['verdict']]}{dmg} | "
                         f"{'yes' if vv['rule_reachable'] else 'NO (n < 35)'} | {_shares(d)} |")  # fmt: skip
    lines += ["", "## Checks", "", f"`{json.dumps(a['checks'])}`; near ties: `{json.dumps(a['near_ties'])}`", ""]
    lines += ["## Strongest single layer per family and patch site (largest share changed; earliest on ties)", "",
              f"| family | level | patched tokens | layer | changed | {OUTCOME_TERM["none"]} | {OUTCOME_TERM["identity"]} | {OUTCOME_TERM["position"]} | {OUTCOME_TERM["value"]} |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for k, s in a["strongest_layer"].items():
        fam, lv, grp = k.split("|")
        lines.append(f"| {fam} | {lv} | {GROUP_TITLE[grp]} | {s['layer']} | {_pct(s['changed'])} | {_pct(s['none'])} | "
                     f"{_pct(s['identity'])} | {_pct(s['position'])} | {_pct(s['value'])} |")  # fmt: skip
    if a["level_contrasts"]:
        lines += ["", "## Level contrasts (spec rule: Newcombe 95% interval of the share difference vs e5f0; 'same' "
                  "if within +-0.15, 'differs' if it excludes 0 and |diff| > 0.15)", "",
                  f"| contrast | interpretable | {OUTCOME_TERM["none"]} | {OUTCOME_TERM["identity"]} | {OUTCOME_TERM["position"]} | {OUTCOME_TERM["value"]} |", "|---|---|---|---|---|---|"]  # fmt: skip
        for k, c in a["level_contrasts"].items():
            cells = [f"{100 * c['diffs'][x]['diff'][0]:+.0f} [{100 * c['diffs'][x]['diff'][1]:+.0f}, "
                     f"{100 * c['diffs'][x]['diff'][2]:+.0f}] {c['diffs'][x]['label']}" for x in PV.HYPOTHESES]  # fmt: skip
            lines.append(f"| {k} | {c['interpretable']} | " + " | ".join(cells) + " |")
    if name == "d3_main_ae_27b":
        lines += dan_section(a)
    lines += ["", "## Agent priors in the job spec (jobs/d3/" + name + ".yaml `hypotheses`) vs results", ""]
    spec = pins.REPO_ROOT / "jobs" / "d3" / f"{name}.yaml"
    if spec.exists():
        import yaml

        for h, txt in yaml.safe_load(spec.read_text())["hypotheses"].items():
            lines.append(f"- {h}: {rule_plain(txt)}")
    lines += ["", "Against the saved numbers:", "", *prior_checks(m, a), ""]
    ex = RESULTS / name / "examples.json"
    if ex.exists():
        e = json.loads(ex.read_text())
        pick = (
            next((x for x in e["examples"] if x["group"] == "position" and x["family"] == "RL"), None)
            or (e["examples"] or [None])[0]
        )
        if pick:
            exp, pp = pick["answers"]["expected"], pick["numbers"]["p"]
            outcome = OUTCOME_TERM.get(pick["group"], pick["group"])
            lines += ["## Worked example (from examples.json)", "", f"Item `{pick['item_id']}` ({pick['family']}; the "
                      f"patched answer was the {outcome}). {pick['condition']}.", "", "Org prompt (as fed):", "", "```",
                      pick["prompt"], "```", "", "Alt prompt:", "", "```", pick["source_prompt"], "```", "",
                      f"Answers: answer org {pick['answers']['clean']}; after the patch {pick['answers']['edited']}. "
                      "Predicted: " + "; ".join(f"{OUTCOME_TERM[h]} {exp[h]} (p {pp.get(h, 0):.3f})" for h in PV.HYPOTHESES)
                      + ".", ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_figures(name: str) -> Path:
    """Re-applies the rule (analyze), draws the run's figures, writes summary.json and report.md into a new
    results/pointer_swap/<run>/analysis-<stamp>-figures/."""
    import matplotlib

    matplotlib.use("Agg")
    m, rows, checks = load_run(name)
    import shutil

    for old in (RESULTS / name).glob("analysis-*-figures"):  # one figures folder per run (the user's rule)
        shutil.rmtree(old)
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    out.mkdir()
    a = analyze(m, rows, checks)
    a["near_ties"] = near_ties(rows)
    a["example_line"] = example_line(m, name)
    figs: dict[str, list[str]] = {}
    main_lv = "e5f0" if "e5f0" in m["levels"] else m["levels"][0]
    for lv in m["levels"]:
        figs[f"by_layer_{lv}"] = fig_by_layer(
            a, m, lv, out / f"by_layer_{lv}", headline=(name in PRIMARY_RUNS and lv == main_lv)
        )
    figs["slots_final"] = fig_slots(a, m, main_lv, "final", out / f"slots_final_{main_lv}")
    figs["slots_last"] = fig_slots(a, m, main_lv, "last", out / f"slots_last_{main_lv}")
    figs["windows"] = fig_windows(a, m, main_lv, out / f"windows_{main_lv}")
    if len(a["domains"]) > 1:
        figs["domains_final"] = fig_domains(a, m, main_lv, "final", out / f"domains_final_{main_lv}")
    if len(m["levels"]) > 1:
        figs["levels_final"] = fig_levels(a, m, "final", out / "levels_final")
        figs["levels_last"] = fig_levels(a, m, "last", out / "levels_last")
    a["figures"] = figs
    (out / "summary.json").write_text(json.dumps(a, indent=1) + "\n")
    (out / "report.md").write_text(plain(report_md(name, m, a, out)))
    print("wrote", out)
    return out


# ---- examples -------------------------------------------------------------------------------------------------------


GROUP_DEFS = {
    "position": "the patched base answered the base's digit at the source's queried slot (H-pointer's prediction)",
    "identity": "the patched base answered the base's digit for the source's entity (H-word / lexical key)",
    "value": "the patched base answered the source's own answer, absent from the base context (H-value)",
    "none": "the patch left the base answer",
    "context": "another digit of the base context, predicted by no hypothesis",
    "other": "any other answer (a recalled digit, another digit, a word)",
    "same_changed": "control: the 'same' source (every hypothesis predicts the base answer) changed the answer",
}


def char_spans(offsets: list[tuple[int, int]], positions: list[int]) -> list[tuple[int, int]]:
    """Merge the tokens' char spans into contiguous runs."""
    spans: list[list[int]] = []
    for i in sorted(positions):
        if i >= len(offsets):
            continue
        s, e = offsets[i]
        if spans and s <= spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], e)
        else:
            spans.append([s, e])
    return [(s, e) for s, e in spans]


def statement_char_spans(text: str, item: dict, order: list[str], digits: list[int]) -> list[tuple[int, int]]:
    facts = [PV.DOMAINS[item["domain"]]["statement"].format(e=e, d=d) for e, d in zip(order, digits, strict=True)]
    ctx = (
        item["context"]
        if order == item["entities"] and digits == item["digits"]
        else item["sources"]["dissoc"]["context"]
    )
    return PV.statement_spans(text, ctx, facts)


def stage_examples(name: str, k: int, seed: int, group: str | None) -> None:
    from bridge_jspace.tokens import load_tokenizer

    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    try:
        tok = load_tokenizer()
    except Exception:
        tok = PV.tokenizer()
    items = {it["id"]: it for its in load_items(m).values() for it in its}
    primary = [la for la in m["windows"]["transit"] if la in m["layers"]]
    focus = group or "final"
    picked = [
        o for o in rows if o["source"] == "dissoc" and o["group"] == focus and o["layer"] in (*primary, "transit")
    ]
    if not picked:  # a smoke run without the transit layers: every dissoc row of the group
        picked = [o for o in rows if o["source"] == "dissoc" and o["group"] == focus and o["layer"] != 0]
    by_group: dict[str, list[dict]] = collections.defaultdict(list)
    for o in picked:
        g = o["role"] if o["role"] in ("position", "identity", "value", "none", "context") else "other"
        by_group[g].append(o)
    by_group["same_changed"] = [
        o for o in rows if o["source"] == "same" and o["group"] == focus and o["role"] != "none"
    ]
    rng = random.Random(seed)
    unedited = {o["name"]: o for o in rows if o["source"] == "unedited"}
    examples = []
    for g, cand in by_group.items():
        for o in rng.sample(cand, min(k, len(cand))):
            it = items[o["name"]]
            prep = prepare(it, tok)
            text = prep["text"] + " "  # the read's prompt, exactly as fed: the space token appended
            sl, d = it["slots"], it["sources"]["dissoc"]
            st = statement_char_spans(prep["text"], it, it["entities"], it["digits"])
            q0 = prep["text"].rindex("\n" + it["question"]) + 1
            cue_at = prep["text"].index(it["cue"], q0)
            spans = [
                {"start": s, "end": e, "role": f"patched ({o['group']})"}
                for s, e in char_spans(prep["offsets"], prep["groups"][o["group"]])
            ]
            spans += [{"start": st[sl["query"]][0], "end": st[sl["query"]][1], "role": "bridge statement (base query, slot a)"},
                      {"start": st[sl["identity"]][0], "end": st[sl["identity"]][1], "role": "identity statement (source's entity in the base)"},
                      {"start": st[sl["position"]][0], "end": st[sl["position"]][1], "role": "position statement (base entity at the source's queried slot)"},
                      {"start": cue_at, "end": cue_at + len(it["cue"]), "role": "cue"}]  # fmt: skip
            s_st = statement_char_spans(prep["source_text"], it, d["entities"], d["digits"])
            examples.append({
                "group": g, "family": it["family"], "item_id": it["id"], "domain": it["domain"], "prompt": text,
                "spans": spans,
                "source_prompt": prep["source_text"] + " ",
                "source_spans": [{"start": s_st[sl["position"]][0], "end": s_st[sl["position"]][1],
                                  "role": "source's queried statement (slot k)"}],
                "condition": f"base's residual at the {o['group']} tokens replaced by the dissoc source's at layer "
                             f"{o['layer']} (one forward, answer read after 'Answer:' and a space)",
                "answers": {"clean": it["answer"], "edited": o["top"].strip(), "expected": d["predictions"],
                            "unedited_read": unedited[o["name"]]["top"].strip() if o["name"] in unedited else None},
                "numbers": {"p": o["p"], "layer": o["layer"], "role": o["role"]},
                "why": GROUP_DEFS[g] + f" ({o['top'].strip()!r})",
            })  # fmt: skip
    groups = [{"key": g, "title": g.replace("_", " "), "definition": GROUP_DEFS[g], "n_total": len(v)}
              for g, v in by_group.items()]  # fmt: skip
    out = {"exp": EXP, "run": name, "seed": seed, "k": k,
           "selection": f"source dissoc, group {focus}, layers {primary or 'all but 0'} and the transit window",
           "groups": groups, "examples": examples}  # fmt: skip
    (run_dir / "examples.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote", run_dir / "examples.json", len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "examples", "analyze", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--set", default="dev", choices=list(PV.SETS))
    ap.add_argument("--levels", nargs="+", default=None)
    ap.add_argument("--families", nargs="+", default=list(PV.FAMILIES), choices=list(PV.FAMILIES))
    ap.add_argument("--domains", nargs="+", default=list(PV.DOMAINS), choices=list(PV.DOMAINS))
    ap.add_argument("--n", type=int, default=25, help="scenes per (domain, level)")
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    ap.add_argument("--layer-step", type=int, default=2)
    ap.add_argument("--control-stride", type=int, default=2)
    ap.add_argument("--competence", default=None, help="pointer_v1 competence run deciding eligibility")
    ap.add_argument("--no-eligibility", action="store_true", help="smoke runs: sample regardless of competence")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--seed", type=int, default=EXAMPLE_SEED)
    ap.add_argument("--group", default=None, choices=list(GROUPS))
    args = ap.parse_args()
    if args.stage == "manifest":
        assert args.why, "manifest needs --why"
        stage_manifest(args)
    elif args.stage == "run":
        stage_run(args.name)
    elif args.stage == "summarise":
        stage_summarise(args.name)
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k, args.seed, args.group)
