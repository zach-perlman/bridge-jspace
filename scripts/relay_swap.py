"""relay_swap (Dan's relay test by digit substitution, 23 Oct 2026): with the answer's sentence hidden from the last
tokens as in the late read, does the answer still follow a change of that sentence's digit?

Finding 1: the answer's sentence hidden from the last tokens (the chat-template tokens after the user's text) leaves few
answers right on most models; Gemma 4 31B-it (first scene set) and Qwen3.6-27B with ~2000 filler tokens (long context)
keep more, read as a relay: the answer reaches the last tokens through other tokens that still see the sentence. Test:
replace the digit of the answer's sentence by a digit that is not in the list and block the last tokens exactly as the
late read does. If the answer is the new digit, the digit reached the last tokens by another route.

Items: the late-read run's own (--from RUN: its manifest's data set, families, n, competence run and gate, so
attn_knockout.build_pointer_cases picks the same scenes), memory -> prompt only. An item counts iff its original
prompt's unedited read is right (finding 1's rule). The run asserts its original prompts' token ids equal the RUN's
cases.jsonl.

Substitution (the agent's proposal): pointer_v4's own 'redigit' prompt of the item: the answer's digit replaced by the
scene's 'value' digit, drawn by the data generator (one fixed seed per set and topic, so one digit per item) among the
digits not in the list (under the generator's 'soft' policy, the usual one, also not a listed entity's remembered
digit); the question is unchanged. Checked per item on the tokenizer: the same token length, exactly one token differs
and it is the answer sentence's digit token, the new digit occurs nowhere in the original prompt and the old digit
nowhere in the substituted one. The competence run already required this prompt answered right unedited (every prompt
of an item right), so the positive control holds by selection on these items; the run's own read checks it again.

Rows per item (prompt: original / substituted; LATE = finding 1's layers: every attention layer on a hybrid (attn),
every layer otherwise (all); DeltaNet mode value):
  1, 2   unedited                                                           (2: the positive control)
  3, 4   the answer's sentence hidden from the last tokens at LATE          (Dan's test)
  5, 6   the off-path sentence of the same token length hidden there instead (the off-path control)
  7, 8   the answer's sentence hidden from every token after it, every layer (the floor; proposal)
  9, 10  hybrids only: hidden from the last tokens in every layer, DeltaNet included (proposal: on a hybrid the late
         read leaves the DeltaNet layers' direct read of the sentence open)
Per row: the top token; whether it is the new digit, the old digit, another listed digit; both digits' log-probs.

Decision rule (Dan, 23 Oct; the agent's proposals marked):
  R          over the counted items, mean of 1[substituted prompt's answer = the new digit] - 1[original prompt's
             answer = the new digit], both with the answer's sentence hidden from the last tokens at LATE (rows 4, 3);
             entity-cluster bootstrap 95% interval (the asked entity resampled within its topic, 4,000 draws, seed 0)
  relay      iff R's lower bound > 5 points; otherwise no relay
  positive   (proposal) the substituted prompt unedited answers the new digit on >= 90% of the items, Wilson lower
             bound >= 85%
  off-path   (proposal) the off-path sentence hidden instead: the substituted prompt answers the new digit on >= 90%,
             Wilson lower bound >= 85%
  floor      (proposal) R with the answer's sentence hidden from every token after it (rows 8, 7): lower bound <= 5
             points (no route is left there, so a difference would be a leak of the block, not a relay)
  verdict    'not interpretable (<the failed control>)' if a control fails, else 'relay' or 'no relay'
  reported   R per topic; R with the item bootstrap; R in every layer (hybrids); the answers' shares (new digit, old
             digit, another listed digit, other) in every row kind; agreement of row 3 and row 1 with the late-read run's
             own rows for the same items (the block reproduces).

Stages (write-once, results/relay_swap/<name>/):
  manifest --name N --from RUN --why W [--limit K] [--smoke]   checks every item's substitution on the tokenizer
  run --name N                                                  check.json, rows.jsonl, cases.jsonl, timing.json
  figures --name N                                              analysis-<UTC stamp>/: verdict.json, verdict.md, figure
--smoke: another model than RUN's is allowed (a CPU smoke on Qwen3.5-0.8B); set BJ_RELAY_RESULTS to write outside
results/.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import check_switches, switches
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts import attn_knockout as A
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl

EXP = "relay_swap"
RESULTS = Path(os.environ.get("BJ_RELAY_RESULTS", str(pins.RESULTS_DIR / EXP)))
FAMILY = "RL"  # memory -> prompt: finding 1's family
ARMS = ("orig", "sub")
RELAY_LO = 0.05  # Dan: a relay iff R's lower bound > 5 points
POS_MIN, POS_LO = 0.90, 0.85  # proposal: the positive and off-path controls (finding 1's off-path bar)
FLOOR_LO = 0.05  # proposal: the floor's R lower bound <= 5 points
OUTCOMES = ("new", "old", "listed", "other")


def rule_text() -> str:
    """The decision rule as the docstring states it (recorded in the manifest)."""
    return "Decision rule" + (__doc__ or "").split("Decision rule")[1].split("\nStages")[0].rstrip()


# ---- items -----------------------------------------------------------------------------------------------------------


def late_label(kinds: list[str]) -> str:
    """Finding 1's layers: every attention layer on a hybrid, every layer on a model without DeltaNet."""
    return "attn" if A.LINEAR in kinds else "all"


def conditions(kinds: list[str]) -> list[dict]:
    """The rows per item in run order (the docstring's Rows: Dan's test and controls first, the proposals last)."""
    late = late_label(kinds)
    out = [{"arm": a, "source": "none", "dest": "-", "layers": "-"} for a in ARMS]
    for src in ("lookup", "lookup_off"):
        out += [{"arm": a, "source": src, "dest": "final", "layers": late} for a in ARMS]
    out += [{"arm": a, "source": "lookup", "dest": "after", "layers": "all"} for a in ARMS]
    if late != "all":
        out += [{"arm": a, "source": "lookup", "dest": "final", "layers": "all"} for a in ARMS]
    return out


def standalone(text: str, digit: str) -> bool:
    """Whether `digit` occurs in `text` as a number of its own (not inside a longer number)."""
    return re.search(rf"(?<!\d){re.escape(digit)}(?!\d)", text) is not None


def substitute(case: dict, item: dict, tok) -> dict:
    """The case with its substituted prompt (the docstring's Substitution), checked on the tokenizer."""
    red, q = item["sources"]["redigit"], item["slots"]["query"]
    assert (red["question"], red["query"], red["query_slot"]) == (item["question"], item["query"], q), item["id"]
    new, old = str(red["digits"][q]), item["answer"]
    assert old == str(item["digits"][q]), f"{item['id']}: the answer is not the asked statement's digit"
    assert int(new) not in item["digits"], f"{item['id']}: the new digit {new} is in the list"
    others = [d for i, d in enumerate(red["digits"]) if i != q] == [d for i, d in enumerate(item["digits"]) if i != q]
    assert others, f"{item['id']}: another statement's digit differs too"
    text = S.render(tok, red["context"], red["question"])
    ids, _, prompt = A.encode(tok, text, item["answer_kind"] == "digit")
    diff = S.changed(case["ids"], ids)
    assert diff is not None, f"{item['id']}: the substituted prompt has another token length"
    assert len(diff) == 1, f"{item['id']}: {len(diff)} tokens changed"
    assert diff == case["sources"]["lookup_digit"], (
        f"{item['id']}: changed token {diff}, the answer's digit token {case['sources']['lookup_digit']}"
    )
    assert not standalone(case["prompt"], new), f"{item['id']}: the new digit {new} occurs in the original prompt"
    assert not standalone(prompt, old), f"{item['id']}: the old digit {old} occurs in the substituted prompt"
    tok_new = S.answer_token(tok, new, "digit")
    assert tok_new != case["tok_A"], f"{item['id']}: the new digit's token is the answer's"
    assert tok_new not in case["conf_toks"], f"{item['id']}: the new digit's token is a listed digit's"
    return {**case, "new": new, "tok_new": tok_new, "sub_ids": ids, "sub_prompt": prompt, "sub_pos": diff[0]}


def original_manifest(run: str) -> dict:
    return json.loads((A.RESULTS / run / "manifest.json").read_text())


def build(tok, om: dict, limit: int | None) -> tuple[list[dict], dict]:
    """The late-read run's cases (the same call, every family it ran, so the same paired scenes), memory -> prompt
    only, each with its substituted prompt; the first `limit` (a smoke)."""
    set_name = om.get("set") or "main"
    cases, report = A.build_pointer_cases(tok, om["dataset"], om["families"], om.get("domains"), om["n_per_family"],
                                          om["eligibility"], om.get("competence"), set_name, om.get("gate_lo"))  # fmt: skip
    items = {it["id"]: it for p in A.pointer_files(om["dataset"], om["families"], om.get("domains"), set_name)
             for it in json.loads(p.read_text())["items"]}  # fmt: skip
    out = [substitute(c, items[c["id"]], tok) for c in cases if c["family"] == FAMILY]
    return (out[:limit] if limit else out), report


def check_original_ids(cases: list[dict], run: str, every: bool = True) -> None:
    """The original prompts are the late-read run's, token for token, and (every) all of its items are here."""
    orig = {}
    for line in (A.RESULTS / run / "cases.jsonl").read_text().splitlines():
        c = json.loads(line)
        if c["family"] == FAMILY:
            orig[c["id"]] = c["ids"]
    mine = {c["id"] for c in cases}
    assert mine <= set(orig), f"items not in {run}'s memory -> prompt items: {sorted(mine - set(orig))[:3]}"
    assert not every or mine == set(orig), f"{run}'s memory -> prompt items missing: {sorted(set(orig) - mine)[:3]}"
    bad = [c["id"] for c in cases if c["ids"] != orig[c["id"]]]
    assert not bad, f"{len(bad)} prompts differ from {run}'s, e.g. {bad[:3]}"


# ---- stages ----------------------------------------------------------------------------------------------------------


def stage_manifest(a: argparse.Namespace) -> None:
    from bridge_jspace.tokens import load_tokenizer

    pins.check_run_name(a.name)
    path = RESULTS / a.name / "manifest.json"
    assert not path.exists(), f"{path} exists; manifests are written once"
    om = original_manifest(a.src)
    assert om["dataset"] == "pointer_v4", f"{a.src}: not a pointer_v4 run"
    assert FAMILY in om["families"], f"{a.src}: no memory -> prompt items"
    kinds = A.model_kinds()
    if not a.smoke:
        assert pins.model_pin() == om["model"], f"the target {pins.model_pin()} is not {a.src}'s {om['model']}"
        assert kinds == om["layer_kinds"], "the layer kinds differ from the late-read run's"
    cases, report = build(load_tokenizer(), om, a.limit)
    assert cases, "no item"
    if not a.smoke:
        check_original_ids(cases, a.src, every=not a.limit)
    set_name = om.get("set") or "main"
    inputs = [*A.pointer_files(om["dataset"], om["families"], om.get("domains"), set_name),
              pins.RESULTS_DIR / om["dataset"] / om["competence"] / "items.jsonl",
              A.RESULTS / a.src / "manifest.json", A.RESULTS / a.src / "cases.jsonl", A.RESULTS / a.src / "rows.jsonl"]  # fmt: skip
    m = {"exp": EXP, "run": a.name, "why": a.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "from": a.src, "original": om, "limit": a.limit, "smoke": a.smoke,
         "family": FAMILY, "items": len(cases), "cases_report": report,
         "new_digits": dict(sorted(collections.Counter(c["new"] for c in cases).items())),
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
         "layer_kinds": kinds, "layer_sets": A.layer_sets(kinds, ["all", "kind"]), "late": late_label(kinds),
         "conditions": conditions(kinds), "mode": "value", "batch": A.BATCH,
         "seeds": {"new_digit": "pointer_v4's generator (redigit's value; the data set's seed per topic)",
                   "spans": A.SPAN_SEED, "bootstrap": A.BOOT_SEED, "cluster_draws": A.N_BOOT_CLUSTER,
                   "item_draws": A.N_BOOT},
         "rule": rule_text()}  # fmt: skip
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path, f"({len(cases)} items, every substitution checked)")


def row_of(c: dict, x: dict, top: int, logp: Any) -> dict:
    return {"family": c["family"], "id": c["id"], "scene": c["scene"], "domain": c["domain"], "bridge": c["bridge"],
            **x, "mode": "-" if x["source"] == "none" else "value", "top": top, "new": top == c["tok_new"],
            "old": top == c["tok_A"], "listed": top in c["conf_toks"],
            "logp_new": round(float(logp[c["tok_new"]]), 4), "logp_old": round(float(logp[c["tok_A"]]), 4)}  # fmt: skip


def stage_run(name: str) -> None:
    import torch

    from bridge_jspace.knockout import knock_out, layer_kinds
    from bridge_jspace.utils import progress

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    check_switches(m)
    assert not (out_dir / "rows.jsonl").exists(), f"{out_dir} has results; runs are written once"
    for rel, sha in m["inputs"].items():
        assert sha256_of(pins.REPO_ROOT / rel) == sha, f"{rel} changed since the manifest"
    model = A.load_target()
    assert layer_kinds(model) == m["layer_kinds"], "the loaded model's layer kinds differ from the manifest's"
    t0 = time.time()
    cases, _ = build(model.tokenizer, m["original"], m["limit"])
    assert len(cases) == m["items"], "another number of items than the manifest's"
    if not m["smoke"]:
        check_original_ids(cases, m["from"], every=not m["limit"])
    check = A.run_check(model, cases[0], m["layer_kinds"])
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    assert check["passed"], "the pre-run check failed (check.json); not running"
    sets, conds, rows = m["layer_sets"], m["conditions"], []
    with torch.no_grad():
        for c in progress(cases, desc="items"):
            for start in range(0, len(conds), A.BATCH):
                chunk = conds[start : start + A.BATCH]
                ids = torch.tensor([c["ids"] if x["arm"] == "orig" else c["sub_ids"] for x in chunk], device=A.DEVICE)
                pos = [A.positions(c, x) if x["source"] != "none" else ([], []) for x in chunk]
                layers = [sets[x["layers"]] if x["source"] != "none" else [] for x in chunk]
                with knock_out(model, layers, [p[0] for p in pos], [p[1] for p in pos], mode="value"):
                    lg = A.forward_last(model, ids)
                logp, top = lg.log_softmax(-1), lg.argmax(-1).tolist()
                rows += [row_of(c, x, top[r], logp[r]) for r, x in enumerate(chunk)]
    seconds = time.time() - t0
    write_jsonl(out_dir / "rows.jsonl", rows)
    keep = ("id", "family", "scene", "domain", "bridge", "cue", "answer", "new", "tok_A", "tok_new", "conf_toks",
            "sub_pos", "prompt", "sub_prompt", "ids", "sub_ids", "sources", "source_text", "dests", "wording")  # fmt: skip
    write_jsonl(out_dir / "cases.jsonl", [{k: c[k] for k in keep if k in c} for c in cases])
    timing = {"items": len(cases), "rows": len(rows), "seconds": round(seconds, 1),
              "mean_prompt_tokens": sum(len(c["ids"]) for c in cases) / len(cases)}  # fmt: skip
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)


# ---- verdict ---------------------------------------------------------------------------------------------------------

NAN3 = [math.nan] * 3


def outcome(r: dict) -> str:
    """A row's answer: the new digit, the old digit, another listed digit, or other (exclusive by construction)."""
    return next((o for o in OUTCOMES[:3] if r[o]), "other")


def index(rows: list[dict]) -> tuple[set[str], dict[tuple, dict[str, dict]]]:
    """Counted items (the original prompt's unedited read right) and their rows by (arm, source, dest, layers) -> id."""
    ok = {r["id"] for r in rows if r["arm"] == "orig" and r["source"] == "none" and r["old"]}
    idx: dict[tuple, dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        if r["id"] in ok:
            idx[(r["arm"], r["source"], r["dest"], r["layers"])][r["id"]] = r
    return ok, idx


def share(by: dict[str, dict], answer: str = "new") -> list[float]:
    """Wilson (rate, lo, hi) of the rows whose answer is `answer` (OUTCOMES)."""
    return [round(x, 4) for x in wilson(sum(outcome(r) == answer for r in by.values()), len(by))]


def relay(idx: dict, k: tuple[str, ...], cases: dict[str, dict]) -> dict:
    """R for one block (k = source, dest, layers): substituted minus original prompt, answering the new digit, on the
    counted items with both rows; entity-cluster interval (pooled and per topic) and the item bootstrap."""
    sub, org = idx.get(("sub", *k), {}), idx.get(("orig", *k), {})
    ids = sorted(set(sub) & set(org))
    if not ids:
        return {"n": 0, "k": 0, "R": NAN3, "R_items": NAN3, "sub_new": NAN3, "orig_new": NAN3, "topics": {}}
    s, o = [float(sub[i]["new"]) for i in ids], [float(org[i]["new"]) for i in ids]
    vals = [x - y for x, y in zip(s, o, strict=True)]
    ents, doms = [cases[i]["bridge"] for i in ids], [cases[i]["domain"] for i in ids]
    topics = {}
    for d in sorted(set(doms)):
        j = [n for n, dd in enumerate(doms) if dd == d]
        r_d = A.entity_boot([vals[n] for n in j], [ents[n] for n in j], [d] * len(j))
        topics[d] = {"n": len(j), "k": len({ents[n] for n in j}), "R": [round(x, 4) for x in r_d]}
    return {"n": len(ids), "k": len(set(zip(doms, ents, strict=True))),
            "R": [round(x, 4) for x in A.entity_boot(vals, ents, doms)],
            "R_items": [round(x, 4) for x in paired_bootstrap_diff(s, o, A.N_BOOT, A.BOOT_SEED)],
            "sub_new": share({i: sub[i] for i in ids}), "orig_new": share({i: org[i] for i in ids}), "topics": topics}  # fmt: skip


def judge(v: dict) -> str:
    """The docstring's verdict: the controls first, then Dan's rule on R's lower bound."""
    if not v["n_counted"]:
        return "not testable (no item answered right unedited)"
    pos, off, floor = v["positive"], v["off_path"]["sub_new"], v["floor"]["R"]
    if not (pos[0] >= POS_MIN and pos[1] >= POS_LO):
        return "not interpretable (the positive control: unedited, the substituted prompt answers the new digit < 90% or its lower bound < 85%)"  # fmt: skip
    if not (off[0] >= POS_MIN and off[1] >= POS_LO):
        return "not interpretable (the off-path control: the off-path sentence hidden, the new digit < 90% or its lower bound < 85%)"  # fmt: skip
    if not floor[1] <= FLOOR_LO:
        return "not interpretable (the floor: hidden from every token after it, R's lower bound > 5 points)"
    return "relay" if v["test"]["R"][1] > RELAY_LO else "no relay"


def agreement(ok: set[str], idx: dict, run_rows: Path, late: str) -> dict:
    """Rows 3 and 1 against the late-read run's own rows for the same items: the share with the same top token."""
    if not run_rows.exists():
        return {}
    theirs: dict[tuple, int] = {}
    for line in run_rows.read_text().splitlines():
        r = json.loads(line)
        if r["family"] == FAMILY and r["id"] in ok and r.get("mode", "value") in ("value", "-"):
            theirs[(r["source"], r["dest"], r["layers"], r["id"])] = r["top"]
    out = {}
    for name, k in (("blocked", ("lookup", "final", late)), ("unedited", ("none", "-", "-"))):
        mine = idx.get(("orig", *k), {})
        both = [i for i in mine if (*k, i) in theirs]
        same = sum(mine[i]["top"] == theirs[(*k, i)] for i in both)
        out[name] = {"n": len(both), "same_top": round(same / len(both), 4) if both else None}
    return out


def verdict(m: dict, rows: list[dict], cases: dict[str, dict], run_rows: Path | None = None) -> dict:
    late = m["late"]
    ok, idx = index(rows)
    v: dict[str, Any] = {
        "n_items": len({r["id"] for r in rows}), "n_counted": len(ok), "late": late,
        "test": relay(idx, ("lookup", "final", late), cases),
        "positive": share(idx.get(("sub", "none", "-", "-"), {})),
        "off_path": relay(idx, ("lookup_off", "final", late), cases),
        "floor": relay(idx, ("lookup", "after", "all"), cases),
        "every_layer": relay(idx, ("lookup", "final", "all"), cases) if late != "all" else None,
        "answers": {"|".join(k): {o: share(by, o) for o in OUTCOMES} for k, by in sorted(idx.items())},
        "agreement_with_late_read_run": agreement(ok, idx, run_rows, late) if run_rows else {},
    }  # fmt: skip
    v["verdict"] = judge(v)
    return v


def _pts(x: list[float]) -> str:
    return "-" if math.isnan(x[0]) else f"{100 * x[0]:+.1f} [{100 * x[1]:+.1f}, {100 * x[2]:+.1f}] points"


def _pct(x: list[float]) -> str:
    return "-" if math.isnan(x[0]) else f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}]"


def report(m: dict, v: dict) -> str:
    where = "every attention layer" if v["late"] == "attn" else "every layer"
    t = v["test"]
    lines = [f"# relay_swap / {m['run']} ({m['model']['repo'].split('/')[-1]}, items of {m['from']})", "",
             f"**Verdict: {v['verdict']}**", "",
             f"Items: {v['n_items']} memory -> prompt; counted (original prompt right unedited): {v['n_counted']}.", "",
             f"- R, the answer's sentence hidden from the last tokens in {where}: {_pts(t['R'])} (entity cluster; "
             f"items: {_pts(t['R_items'])}); new digit {_pct(t['sub_new'])} substituted vs {_pct(t['orig_new'])} "
             "original",
             f"- positive control (substituted, nothing hidden, answers the new digit): {_pct(v['positive'])}",
             f"- off-path control (the off-path sentence hidden instead, substituted): {_pct(v['off_path']['sub_new'])}; "
             f"its R {_pts(v['off_path']['R'])}",
             f"- floor (hidden from every token after it, every layer): R {_pts(v['floor']['R'])}"]  # fmt: skip
    if v["every_layer"]:
        lines.append(
            f"- hidden from the last tokens in every layer, DeltaNet included: R {_pts(v['every_layer']['R'])}"
        )
    topics = "; ".join(f"{d} {_pts(x['R'])} (n {x['n']}, k {x['k']})" for d, x in t["topics"].items())
    lines += ["", f"R per topic: {topics}", "",
              "Answers per row kind (counted items): new digit / old digit / another listed digit / other"]  # fmt: skip
    lines += [f"- {k}: " + " / ".join(f"{100 * o[x][0]:.0f}%" for x in OUTCOMES) for k, o in v["answers"].items()]
    if v["agreement_with_late_read_run"]:
        lines += ["", f"Agreement with the late-read run's rows: {json.dumps(v['agreement_with_late_read_run'])}"]
    return "\n".join(lines) + "\n"


SETTINGS = (  # (block, label) in figure order; LATE is finding 1's layers; the last one only where LATE is not 'all'
    (("none", "-", "-"), "nothing\nhidden"),
    (("lookup", "final", "LATE"), "answer's sentence\nhidden from\nthe last tokens"),
    (("lookup_off", "final", "LATE"), "off-path sentence\nhidden from\nthe last tokens"),
    (("lookup", "after", "all"), "answer's sentence\nhidden from\nevery later token"),
    (("lookup", "final", "all"), "answer's sentence\nhidden from the last\ntokens, every layer\n(DeltaNet too)"),
)


def figure(m: dict, v: dict, rows: list[dict], cases: dict[str, dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as P

    _, idx = index(rows)
    blocks: list[tuple[tuple, str]] = []
    for k, lab in SETTINGS:  # where LATE is 'all' the last setting repeats the second: kept once, the first label
        k = tuple(v["late"] if x == "LATE" else x for x in k)
        if ("sub", *k) in idx and k not in dict(blocks):
            blocks.append((k, lab))
    fig, ax = plt.subplots(figsize=(9.0, 6.8))
    P.style_axes(ax)
    series = (("orig", "#5f5e59", "s", "original prompt"), ("sub", "#2a78d6", "o", "digit substituted"))
    for j, (arm, color, marker, _) in enumerate(series):
        for i, (k, _) in enumerate(blocks):
            p, lo, hi = share(idx.get((arm, *k), {}))
            if not math.isnan(p):
                ax.errorbar([i + (j - 0.5) * 0.22], [p], yerr=[[p - lo], [hi - p]], fmt=marker, color=color, ms=8,
                            lw=1.6, mec=P.SURFACE, mew=0.8, zorder=3)  # fmt: skip
    for i, (k, _) in enumerate(blocks):
        if k[0] != "none":
            r = relay(idx, k, cases)["R"]
            text = "R -" if math.isnan(r[0]) else f"R {100 * r[0]:+.0f} points\n[{100 * r[1]:+.0f}, {100 * r[2]:+.0f}]"
            ax.annotate(text, (i, 1.02), ha="center", va="bottom", fontsize=7.5, color=P.INK,
                        annotation_clip=False)  # fmt: skip
    ax.set_xticks(range(len(blocks)), [lab for _, lab in blocks], fontsize=8.5, color=P.INK)
    ax.set_ylim(-0.03, 1.03)
    P.percent_axis(ax)
    ax.set_ylabel("% of answers that are the new digit", color=P.INK, fontsize=9)
    where = "every attention layer" if v["late"] == "attn" else "every layer"
    model = m["model"]["repo"].split("/")[-1]
    handles = [Line2D([], [], color=c, marker=mk, ls="", ms=8, label=lab) for _, c, mk, lab in series]
    title = f"Does the answer follow the hidden sentence's new digit? {model}: {v['verdict'].split(' (')[0]}"
    P.finish(fig, path, title, "",
             handles=handles, explain=[
                 ("What we did", "The digit of the sentence that gives the answer is replaced by a digit not in the "
                  "list; that sentence is hidden from the last tokens (the chat-template tokens after the question) "
                  f"in {where}, exactly as in the late read."),
                 ("Example", "\"The eagle's locker is 9.\" becomes \"The eagle's locker is 6.\"; the question stays "
                  "\"Which locker belongs to the animal known for its talons?\"; the new digit is 6."),
                 ("How to read", "R = substituted minus original prompt, in points of answers that are the new digit, "
                  "with its 95% interval (asked entities resampled within topic); a relay iff the lower bound > 5 "
                  "points. Marker bars: Wilson 95%."),
                 ("Control", "nothing hidden (the model reads the new digit); the off-path sentence hidden instead; "
                  "the sentence hidden from every later token (no route left, so R should be about 0)."),
                 ("Data", f"{v['n_counted']} memory -> prompt questions answered right unedited, the items of the "
                  "late-read run."),
             ])  # fmt: skip


def stage_figures(name: str) -> None:
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    rows = [json.loads(line) for line in (out_dir / "rows.jsonl").read_text().splitlines()]
    cases = {c["id"]: c for c in map(json.loads, (out_dir / "cases.jsonl").read_text().splitlines())}
    v = verdict(m, rows, cases, A.RESULTS / m["from"] / "rows.jsonl")
    d = out_dir / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir()
    (d / "verdict.json").write_text(json.dumps(v, indent=1) + "\n")
    text = report(m, v)
    (d / "verdict.md").write_text(text)
    figure(m, v, rows, cases, d / "relay_swap.png")
    print(text, end="")
    print("wrote", d)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest", "run", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--from", dest="src", help="manifest: the late-read run (results/attn_knockout/<RUN>)")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items (a smoke)")
    ap.add_argument("--smoke", action="store_true", help="manifest: allow another model than the late-read run's")
    a = ap.parse_args(argv)
    if a.stage == "manifest":
        assert a.src, "manifest needs --from"
        assert a.why, "manifest needs --why"
        stage_manifest(a)
    elif a.stage == "run":
        stage_run(a.name)
    else:
        stage_figures(a.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
