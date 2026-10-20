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
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "examples"])
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
    else:
        stage_examples(args.name, args.k, args.seed, args.group)
