"""x51_carrier (batch 51, test 51.7; jobs/c3/batch51.yaml, design and rules fixed in advance; Q51.7 in
predictions/2026-10-28_dan.md): Z1 on the full carrier. The change at the bridge name's last token at every layer <= L.

Items: Z1's (scripts/x50_zach.py, part z1): its chosen passages in its order (gate.json), rebuilt with x50_zach.z1_cases
on the target's tokenizer and checked equal to Z1's stored cases (both readers' O and S ids, the patch token, the
answers' first tokens, S's entity, the stratum); a mismatch fails the job. Same gate (Z1's, read from its gate.json),
same lens file (the pinned J++), same layer L (9B L12, 27B L32), same strata (fact-first / fact-after: the original
bridge's fact sentence before / after the pointer sentence in the K passage), same readers (K = lookup, M = recall).

Arms on O (per reader: the K and M passages differ before the patch token, so each reader has its own states), read
with Z1's read (his chat framing, no prefill; switch = the top token is the other entity's answer's first token):
  none        O unedited (a check against Z1's stored none row)
  whole_bL    the patch token's state set to h_S,l at every block output l = 0..L          ("whole before-L")
  no_jpp_bL   set to h_S,l minus the J++ part of Delta_l = h_S,l - h_O,l (signed OMP, k = 25, layer l's own
              letter-token J++ atoms: x0_necessity.fit, as Z1 at L and x49_ladder per layer) ("without J++ before-L")
  rand_bL     set to h_S,l minus a random part of Delta_l of the J++ part's share of ||Delta_l||^2
              (statement_positions.random_subspace_part, X0's random basis, seed 888 + l)  ("random before-L")
  whole_emb   descriptive: whole_bL with S's token id at the patch token (47.4's (b): the input of block 0 counted as a
              layer); the three arms above edit block outputs only, as the ladder does, so they stay matched
  window      descriptive, rule (iii): the K reader, the first 50 fact-after passages in Z1's order: the patch token and
              every token of the bridge's fact sentence set to S's states at block outputs 0..L (S's own clean
              forward). "The bridge's fact sentence" is read as both bridges' (the K passage states the true fact of
              O's bridge and of S's): a sentence before the pointer has the same states in O and S, so patching it is
              a no-op, and either sentence after the pointer is where a link made away from the bridge token would
              sit. Recorded in every run (cheap); the verdict reports it only if rule (iii)'s condition holds.
States are set (exp04_brew_parts.SetRows), not added: added differences overshoot at layer after layer (47.4). At L the
three before-L states equal Z1's one-layer arms (h_O,L + its vector); they differ by what later tokens read below L. Z1's
one-layer arms (whole, no_jpp, no_jpp_rand at L, added) are read from its stored rows, not rerun.
Plain-text loss per arm (x49_gain's "dumbest way 1"): -log p(O's own next token) at the patch token, from O's prompt cut
after the patch token, under none, Z1's three one-layer arms (recomputed here: the loss was not stored), the three
before-L arms and whole_emb, per reader.

Rules (fixed in advance; batch51.yaml 51.7):
  (i)   "the slice explanation": the whole before-L raises the lookup's switch on fact-after items by >= 0.3 over the
        one-layer whole, and on fact-first brings the lookup within 0.10 of the recall.
  (ii)  on the full carrier, per model and per stratum, fact-first decisive: recall extra loss - lookup extra loss >= 0.3
        and lookup <= 0.10 -> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on
        the full carrier"; else in between.
  (iii) if fact-after lookups stay under 0.5 even under the whole before-L: "the link is made away from the bridge
        token"; only then the window-patching read (50 items, descriptive) is reported.

SEALED: the run writes per-item files only; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's Q51.7
answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x51_carrier.py plan                            # CPU, tokenizer + Z1's files
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_carrier.py run --name qwen35_9b_x51_7      # GPU (sealed)
uv run python scripts/x51_carrier.py verdict                                               # CPU, after Dan's Q51.7
uv run python scripts/x51_carrier.py view                                                  # CPU, after Dan's Q51.7
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
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x50_zach as Z

EXP = "x51_carrier"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = Z.PREDICTIONS
QUESTION = "Q51.7"
TARGETS = ("qwen3.5-9b", "qwen3.6-27b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x51_7", "qwen3.6-27b": "x51_7_27b"}
# batch 52 C coverage (amendment 3, extra f): Lightning on its own Z1 run (x50_zach.COVERAGE_RUNS); verdict --coverage
# reads it alone, 51.7's RUNS and own verdict unchanged
COVERAGE_RUNS = {"nemotron-3.5-lightning": "nem35l_x52_carrier"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
SCORED = "results/x51_carrier/x51_7-20261028T171646Z"  # 51.7's rules first scored


def z1_run(target: str) -> str:
    """Z1's run on the target: batch 50's, or batch 52's coverage run (Lightning)."""
    return {**Z.RUNS["z1"], **Z.COVERAGE_RUNS.get("z1", {})}[target]


READERS, LOOKUP, RECALL = Z.READERS, Z.LOOKUP, Z.RECALL
STRATA = ("fact-first", "fact-after")
GROUPS = (*STRATA, "all")
ONE = ("whole_1L", "no_jpp_1L", "rand_1L")  # Z1's one-layer arms, stored
Z1_ARM = dict(zip(Z.ARMS, ONE, strict=True))  # Z1's arm names -> ours
BEFORE = ("whole_bL", "no_jpp_bL", "rand_bL")
EMB, WINDOW = "whole_emb", "window"
READ_ARMS = ("none", *BEFORE, EMB)
LOSS_ARMS = ("none", *ONE, *BEFORE, EMB)
KIND = {"one": ONE, "before": BEFORE}
N_WINDOW = 50
SLICE_RISE, NEAR, AWAY = 0.30, 0.10, 0.50
EPS = Z.EPS
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0
ARM_TEXT = {
    "none": "O unedited",
    "whole_1L": "Z1's whole arm: h_S,L - h_O,L added at the patch token at L (stored rows)",
    "no_jpp_1L": "Z1's without-J++ arm at L (stored rows)",
    "rand_1L": "Z1's without-a-random-part arm at L (stored rows)",
    "whole_bL": "whole before-L: the patch token set to h_S,l at block outputs 0..L",
    "no_jpp_bL": "without J++ before-L: set to h_S,l - P_J,l Delta_l (layer l's own 25 signed-OMP J++ atoms)",
    "rand_bL": "random before-L: set to h_S,l - a random part of Delta_l of P_J,l Delta_l's share (seed 888 + l)",
    "whole_emb": "descriptive: whole before-L with S's token at the patch token (47.4's (b))",
    "window": "descriptive (rule iii): the patch token and both bridges' fact sentences (O's and S's, K passage) set "
              "to S's states at block outputs 0..L; K reader, the first 50 fact-after passages",
}  # fmt: skip
RULE = (
    '(i) "The slice explanation": the whole before-L raises the lookup\'s switch on fact-after items by >= 0.3 over the '
    "one-layer whole, and on fact-first brings the lookup within 0.10 of the recall. (ii) On the full carrier, per model "
    "and reported per stratum with fact-first decisive: recall extra loss - lookup extra loss >= 0.3 and lookup <= 0.10 "
    '-> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on the full carrier"; else '
    'in between. (iii) If fact-after lookups stay under 0.5 even under whole before-L: "the link is made away from the '
    'bridge token" -- only then the window-patching read (the bridge token at layers <= L plus the bridge\'s fact '
    "sentence), 50 items, descriptive."
)  # fmt: skip
AS_COMPUTED = (
    "Items: Z1's chosen passages in Z1's order (its gate.json), rebuilt with x50_zach.z1_cases on the target's tokenizer "
    "and equal to Z1's stored cases; Z1's gate decides tested / not tested (numbers descriptive only on a failed gate). "
    "Switch = the top token is the first token of the other entity's answer (Z1's read). Before-L = block outputs 0..L "
    "(the input embedding is not edited in the three arms: the lens has no map there, and the arms must stay matched; "
    "whole_emb, 47.4's (b), beside). Delta_l = h_S,l - h_O,l at the name's last token from clean S and O forwards, per "
    "reader; J++ part = x0_necessity.fit(layer l's letter-token J++ atoms, Delta_l, 25, signed); random part = "
    "statement_positions.random_subspace_part(Delta_l, its share, X0's random basis seed 888 + l). Shares per stratum "
    "(fact-first, fact-after; 'all' beside) with 95% cluster-bootstrap intervals over the original bridge entity "
    "(10,000 resamples, seed 0; every arm and both readers on the same draws). (i): rise = S_K(whole_bL) - "
    "S_K(whole_1L) on fact-after, clause at >= 0.30; fact-first |S_K(whole_bL) - S_M(whole_bL)| <= 0.10 (the recall "
    "under the same arm); 'the slice explanation' iff both; Q51.7 (i) reads the rise clause. (ii): extra loss = X0's "
    "excess (S_rand_bL - S_no_jpp_bL) / S_whole_bL per reader, gap = M's - K's on paired draws; labels as written, "
    "fact-first decisive, fact-after and all reported; Z1's one-layer cells beside. An undefined extra loss (no switch "
    "under whole_bL) holds no clause (\"can't tell\"). (iii): S_K(whole_bL) on fact-after < 0.50 -> 'the link is made "
    "away from the bridge token' and the window read is reported (S_K(window) beside S_K(whole_bL) on the same 50 "
    "passages; window = the patch token and both bridges' fact sentences, O's and S's, in the K passage, set to S's "
    "states at blocks 0..L); else it stays in the files, unreported. Point estimates decide (EPS 1e-9 at the bars). Loss: mean "
    "plain-text loss per arm and reader with intervals, and its ratio to the one-layer whole's (descriptive). Checks: "
    "our none read against Z1's stored none read (top token, item by item); the whole before-L switch split by "
    "whether only the name's last token differs between O and S (descriptive)."
)  # fmt: skip


def layer_of(target: str) -> int:
    return Z.LAYERS[target][0]


def z1_dir(target: str) -> Path:
    return Z.RESULTS / z1_run(target)


# ---- items (tokenizer and Z1's stored files) ------------------------------------------------------------------------


def mismatch(built: dict | None, stored: dict | None) -> str:
    """Why a rebuilt Z1 case differs from Z1's stored one ('' if it does not)."""
    if built is None or stored is None:
        return "not rebuilt" if built is None else "not stored"
    for f in ("cf_bridge", "stratum", "answer", "cf_answer"):
        if built[f] != stored[f]:
            return f
    for r in READERS:
        b, s = built["readers"][r], stored["readers"][r]
        for f in ("pos", "tok_A", "tok_b", "tok_lure"):
            if b[f] != s[f]:
                return f"{r} {f}"
        if any(list(b["ids"][v]) != list(s["ids"][v]) for v in ("org", "alt")):
            return f"{r} ids"
    return ""


def with_window(tok, c: dict, p: dict) -> dict:
    """The case with its K reader's window (the patch token, the original bridge's fact sentence and S's bridge's fact
    sentence in the K passage) and, per reader, how many tokens differ between O and S."""
    from bridge_jspace.tokens import raw_encoding

    rd = c["readers"][LOOKUP]
    org, alt, pos = rd["ids"]["org"], rd["ids"]["alt"], rd["pos"]
    text = Z.render(tok, p[LOOKUP], rd["context"], rd["question"])
    assert list(raw_encoding(tok, text)["input_ids"]) == list(org), f"{c['scene']}: O's prompt does not re-render"
    fact = {role: Z.sent_tokens(tok, text, rd["context"], Z.kfact(c["relation"], c["wording"], c[role]))
            for role in ("bridge", "cf_bridge")}  # fmt: skip
    for role, ps in fact.items():
        assert ps, f"{c['scene']}: the {role}'s fact sentence has no token"
        assert pos not in ps, f"{c['scene']}: the {role}'s fact sentence holds the patch token"
        assert all(org[q] == alt[q] for q in ps), f"{c['scene']}: the {role}'s fact sentence differs in S"
    changed = {r: sum(a != b for a, b in zip(v["ids"]["org"], v["ids"]["alt"], strict=True))
               for r, v in c["readers"].items()}  # fmt: skip
    return {**c, "fact_pos": fact, "window": sorted({pos, *fact["bridge"], *fact["cf_bridge"]}), "n_changed": changed}


def z1_items(tok, target: str) -> tuple[list[dict], list[str]]:
    """Z1's chosen passages in its order, rebuilt on tok, each checked against Z1's stored case; (items, mismatches)."""
    src = z1_dir(target)
    order = [tuple(k) for k in json.loads((src / "gate.json").read_text())["order"]]
    stored = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    built, pairs = {}, {}
    for s in [s for s in Z.SETS if any(k[0] == s for k in order)]:
        ps, _ = Z.load_pairs(s, "z1")
        pairs.update({(s, p[LOOKUP]["scene"]): p for p in ps})
        cases, _ = Z.z1_cases(tok, ps)
        built.update({(s, c["scene"]): c for c in cases})
    items, bad = [], []
    for key in order:
        why = mismatch(built.get(key), stored.get(key))
        if why:
            bad.append(f"{key[0]}/{key[1]}: {why}")
            continue
        items.append(with_window(tok, built[key], pairs[key]))
    return items, bad


def window_keys(items: list[dict], n: int | None = None) -> list[tuple[str, str]]:
    """The first n (default N_WINDOW) fact-after passages in Z1's order (rule iii's window read)."""
    return [(c["set"], c["scene"]) for c in items if c["stratum"] == "fact-after"][: N_WINDOW if n is None else n]


def swapped(rd: dict) -> list[int]:
    """O's prompt with S's token at the patch token (whole_emb)."""
    ids = list(rd["ids"]["org"])
    ids[rd["pos"]] = rd["ids"]["alt"][rd["pos"]]
    return ids


# ---- plan (CPU) -----------------------------------------------------------------------------------------------------


def plan_counts(items: list[dict], bad: list[str], target: str) -> dict:
    L = layer_of(target)
    lens = [len(c["readers"][w]["ids"]["org"]) for c in items for w in READERS]
    return {"target": target, "z1_run": z1_run(target), "layer": L, "patched_layers": [0, L], "n_patched": L + 1,
            "items": len(items), "mismatches": bad, "strata": dict(collections.Counter(c["stratum"] for c in items)),
            "entities": {s: len({c["bridge"] for c in items if c["stratum"] == s}) for s in STRATA}
            | {"all": len({c["bridge"] for c in items})},
            "sets": dict(collections.Counter(c["set"] for c in items)),
            "only_last_token_changed": {s: {r: sum(c["n_changed"][r] == 1 for c in items if c["stratum"] == s)
                                            for r in READERS} for s in STRATA},
            "window_items": len(window_keys(items)),
            "window_tokens": {"min": min((len(c["window"]) for c in items), default=0),
                              "max": max((len(c["window"]) for c in items), default=0)},
            "prompt_tokens": {"min": min(lens, default=0), "median": statistics.median(lens) if lens else 0,
                              "max": max(lens, default=0)},
            "read_arms": list(READ_ARMS), "loss_arms": list(LOSS_ARMS), "stored_arms": list(ONE),
            "reads": len(items) * len(READERS) * len(READ_ARMS) + len(window_keys(items)),
            "loss_rows": len(items) * len(READERS) * len(LOSS_ARMS),
            "forwards_for_states": len(items) * len(READERS) * 2}  # fmt: skip


def prompt_lines(decode, c: dict) -> list[str]:
    lines = [f"### {c['set']}/{c['scene']}: {c['bridge']} -> {c['cf_bridge']} ({c['answer']} -> {c['cf_answer']}), "
             f"{c['stratum']}", ""]  # fmt: skip
    for w, rd in c["readers"].items():
        lines += [f"**{w}** ({rd['id']}), tokens changed O -> S: {c['n_changed'][w]}. O, as read (patch token in ⟦…⟧):",
                  "", "```", Z.mark(decode, rd["ids"]["org"], rd["pos"]), "```", "", "S:", "", "```",
                  Z.mark(decode, rd["ids"]["alt"], rd["pos"]), "```", ""]  # fmt: skip
        if w == LOOKUP:
            lines += [
                f"Window (rule iii): positions {c['window']}: {decode([rd['ids']['org'][q] for q in c['window']])!r}",
                "",
            ]
    return lines


def stage_plan(plan_dir: str | None = None) -> Path:
    """On BJ_TARGET's tokenizer: Z1's items rebuilt and checked, the counts, 5 rendered prompts (the first five items),
    as plan-<target>.{json,md} in plan_dir (default results/x51_carrier/plan-<UTC>/). No Z1 outcome is read."""
    from bridge_jspace.utils import git_state
    from scripts import x45m

    t = pins.TARGET
    assert t in RUNS, f"51.7 runs on {list(RUNS)}, not {t}"
    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    tok = x45m.tokenizer()
    items, bad = z1_items(tok, t)
    counts = plan_counts(items, bad, t) | {"code": git_state()}
    decode = lambda ids: tok.decode([int(i) for i in ids], skip_special_tokens=False)  # noqa: E731
    lines = [f"# x51_carrier (51.7) plan on {t}'s tokenizer (UNVERIFIED)", "", "```json",
             json.dumps({k: v for k, v in counts.items() if k != "code"}, indent=1, ensure_ascii=False), "```", ""]  # fmt: skip
    for c in items[:N_PROMPTS]:
        lines += prompt_lines(decode, c)
    (out / f"plan-{t}.json").write_text(json.dumps(counts, indent=1, ensure_ascii=False) + "\n")
    (out / f"plan-{t}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in counts.items() if k != "code"}, ensure_ascii=False))
    print(out)
    return out


# ---- the edits (CPU-testable) ---------------------------------------------------------------------------------------


def layer_values(jdic, h_s, h_o, basis) -> tuple[dict, dict, Any]:
    """One layer, every item of one reader: h_s, h_o [n, d] the patch token's clean states in S and O. Returns the
    before-L arms' set values {arm: [n, d]}, Z1's one-layer vectors {arm: [n, d]} (added on O at L: x6_routes'
    removal_arms, as Z1) and the J++ part's share of ||Delta||^2 [n]."""
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    h_s, h_o = h_s.float(), h_o.float()
    x = h_s - h_o
    fit = X.fit(jdic, x, X.K_MAIN, "signed").to(x.device)
    more, sh = R.removal_arms(x, {"jpp": fit}, basis)
    rand = SP.random_subspace_part(x, sh["jpp"], basis)
    sets = {"whole_bL": h_s, "no_jpp_bL": h_s - fit, "rand_bL": h_s - rand}
    one = {"whole_1L": x, "no_jpp_1L": more["no_jpp"], "rand_1L": more["no_jpp_rand"]}
    return sets, one, sh["jpp"]


def edit_sets(sets_i: dict[str, dict[int, Any]], one_i: dict[str, Any], pos: int, layer: int) -> dict[str, dict]:
    """One item and reader: each arm's edit set ({block: edit}) in LOSS_ARMS order. sets_i[arm][l]: [d] the value set
    at the patch token at block output l (l = 0..L); one_i[arm]: [d] Z1's one-layer vector added at L. whole_emb's edits
    are whole_bL's (its prompt differs: swapped)."""
    from scripts.exp04_brew_parts import AddRows, SetRows

    out: dict[str, dict] = {"none": {}}
    for a in ONE:
        out[a] = {layer: AddRows(one_i[a][None], [pos])}
    for a in BEFORE:
        assert sorted(sets_i[a]) == list(range(layer + 1)), f"{a}: blocks {sorted(sets_i[a])}"
        out[a] = {la: SetRows(v[None], [pos]) for la, v in sets_i[a].items()}
    out[EMB] = out["whole_bL"]
    assert tuple(out) == LOSS_ARMS
    return out


def read_row(c: dict, w: str, rd: dict, arm: str, lg, layer: int) -> dict:
    """Z1's read row (x0_necessity.read_row over Z1's candidate tokens, x50_zach.route)."""
    import torch

    cands = torch.tensor(sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}),
                         device=lg.device)  # fmt: skip
    row = X.read_row(lg, rd, cands)
    return {"scene": c["scene"], "set": c["set"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
            "relation": c["relation"], "stratum": c["stratum"], "layer": layer, "reader": w, "arm": arm,
            "route": Z.route(row["top"], rd), **row}  # fmt: skip


# ---- GPU ------------------------------------------------------------------------------------------------------------


def run_items(model, lens, items: list[dict], layer: int, ws) -> tuple[list, list, list, list]:
    """(read rows, loss rows, window rows, norms). Clean S and O forwards per item and reader (the patch token's
    states at blocks 0..L kept on the CPU), the arms' values layer by layer (one lens dictionary and random basis at a
    time), then the reads, the losses and the window."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import SetRows

    dev = model.device
    layers = tuple(range(layer + 1))
    letters = model.letter_token_ids()
    h: dict[str, dict[str, dict[int, list]]] = {
        v: {w: {la: [] for la in layers} for w in READERS} for v in ("org", "alt")
    }
    with torch.no_grad():
        for c in progress(items, f"51.7: clean S and O states at the patch token, blocks 0..{layer} (passage)"):
            for w, rd in c["readers"].items():
                for v in ("org", "alt"):
                    rec = model.run(torch.tensor([rd["ids"][v]], device=dev), record=layers)[1]
                    for la in layers:
                        h[v][w][la].append(rec[la][rd["pos"]].cpu())  # a copy, not a view of [seq, d]
                    del rec
        d = int(h["alt"][LOOKUP][0][0].shape[0])
        sets: dict[str, dict[str, dict[int, Any]]] = {w: {a: {} for a in BEFORE} for w in READERS}
        one: dict[str, dict[str, Any]] = {}
        norms = []
        for la in progress(layers, "51.7: the J++ and random parts per layer (layer)"):
            jdic = lens.vectors(la, letters)
            basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            for w in READERS:
                hs, ho = torch.stack(h["alt"][w][la]).to(dev), torch.stack(h["org"][w][la]).to(dev)
                st, on, share = layer_values(jdic, hs, ho, basis)
                for a in BEFORE:
                    sets[w][a][la] = st[a].cpu()
                if la == layer:
                    one[w] = {a: v.cpu() for a, v in on.items()}
                dn, sn = (hs - ho).float().norm(dim=-1), hs.float().norm(dim=-1)
                norms += [{"scene": c["scene"], "set": c["set"], "reader": w, "layer": la,
                           "norm_delta": round(float(dn[i]), 4), "norm_hS": round(float(sn[i]), 4),
                           "share_jpp": round(float(share[i]), 5)} for i, c in enumerate(items)]  # fmt: skip
                del hs, ho, st, on
            del jdic, basis
            # JLens keeps every layer's fp32 J_l on the GPU once used (d x d each; 33 of them on the 27B): free them
            getattr(lens, "_J_gpu", {}).clear()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        del h
        win = set(window_keys(items))
        rows, losses, wrows = [], [], []
        for i, c in enumerate(progress(items, "51.7: reads and losses (passage)")):
            for w, rd in c["readers"].items():
                pos, org = rd["pos"], rd["ids"]["org"]
                es = edit_sets({a: {la: sets[w][a][la][i].to(dev) for la in layers} for a in BEFORE},
                               {a: one[w][a][i].to(dev) for a in ONE}, pos, layer)  # fmt: skip
                arms = ("none", *BEFORE)
                lg, _ = X.read_logits(model, org, [es[a] for a in arms], "chat", [], ws)
                lg_e, _ = X.read_logits(model, swapped(rd), [es[EMB]], "chat", [], ws)
                rows += [read_row(c, w, rd, a, x, layer) for a, x in zip((*arms, EMB), [*lg, *lg_e], strict=True)]
                # plain-text loss: O's own next token at the patch token, the prompt cut after it
                nxt = org[pos + 1]
                cut = [a for a in LOSS_ARMS if a != EMB]
                lo, _ = X.read_logits(model, org[: pos + 1], [es[a] for a in cut], "chat", [], ws)
                le, _ = X.read_logits(model, swapped(rd)[: pos + 1], [es[EMB]], "chat", [], ws)
                lp = torch.log_softmax(torch.cat([lo, le]).float(), dim=-1)
                losses += [{"scene": c["scene"], "set": c["set"], "entity": c["bridge"], "stratum": c["stratum"],
                            "reader": w, "arm": a, "next": nxt, "loss": round(float(-row[nxt]), 5),
                            "top_is_next": int(int(row.argmax()) == nxt)}
                           for a, row in zip((*cut, EMB), lp, strict=True)]  # fmt: skip
                if w == LOOKUP and (c["set"], c["scene"]) in win:
                    rec = model.run(torch.tensor([rd["ids"]["alt"]], device=dev), record=layers)[1]
                    assert torch.allclose(rec[layer][pos].cpu(), sets[w]["whole_bL"][layer][i], atol=1e-3, rtol=1e-3), (
                        f"{c['scene']}: S's state at the patch token is not the stored one"
                    )
                    pw = c["window"]
                    ew = {la: SetRows(rec[la][pw].clone(), pw) for la in layers}
                    del rec
                    lw, _ = X.read_logits(model, org, [ew], "chat", [], ws)
                    wrows.append({**read_row(c, w, rd, WINDOW, lw[0], layer), "window": pw})
    return rows, losses, wrows, norms


def manifest(name: str, target: str) -> dict:
    from bridge_jspace.data import sha256_of
    from bridge_jspace.utils import git_state

    src = z1_dir(target)
    L = layer_of(target)
    inputs = {str(p.relative_to(pins.REPO_ROOT) if p.is_relative_to(pins.REPO_ROOT) else p): sha256_of(p)
              for p in (SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl")),
                        *(pins.DATA_DIR / "tasks_v2" / s / "items.jsonl" for s in Z.SETS)) if p.exists()}  # fmt: skip
    return {"exp": EXP, "run": name, "test": "51.7", "spec": "jobs/c3/batch51.yaml (51.7)",
            "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "inputs": inputs, "source": z1_run(target), "layer": L, "layers": list(range(L + 1)), "k": X.K_MAIN,
            "omp": "signed", "arms": ARM_TEXT, "read_arms": list(READ_ARMS), "loss_arms": list(LOSS_ARMS),
            "stored_arms": {"from": z1_run(target), "map": Z1_ARM},
            "items_rule": "Z1's chosen passages in Z1's order (gate.json), rebuilt with x50_zach.z1_cases on the "
                          "target's tokenizer and equal to Z1's stored cases (ids, patch token, answer tokens, S's "
                          "entity, stratum); a mismatch fails the job",
            "gate": "Z1's (read from its gate.json by the verdict)",
            "edit": "SetRows at the patch token at block outputs 0..L (states set, not added); whole_emb also swaps "
                    "the patch token's id; the one-layer arms (losses only) are Z1's AddRows at L",
            "read": "Z1's: the top token after the prompt (his chat framing, no prefill) against the other entity's "
                    "answer's first token",
            "loss": "-log p(O's token after the patch token) at the patch token, O's prompt cut after it, per reader",
            "window": {"n": N_WINDOW, "items": "the first 50 fact-after passages in Z1's order", "reader": LOOKUP,
                       "tokens": "the patch token and both bridges' fact sentences (O's and S's; K passage)",
                       "reported": "recorded in every run; the verdict reports it only if rule (iii)'s condition holds"},
            "rule": RULE, "as_computed": AS_COMPUTED,
            "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                      "view": VIEW_SEED, "cf_order": Z.CF_SEED}, "n_boot": X.N_BOOT,
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip


def stage_run(name: str) -> Path:
    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts import x6_routes as R

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "51.7 renders Z1's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS or target in COVERAGE_RUNS, f"51.7 runs on {[*RUNS, *COVERAGE_RUNS]}, not {target}"
    L = layer_of(target)
    assert (z1_dir(target) / "gate.json").exists(), f"Z1's run {z1_dir(target)} is not here"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, target)
    if target in COVERAGE_RUNS:  # batch 52: no Q-line; verdict --coverage when it lands
        m |= {"question": NO_PREDICTION, "batch": 52, "rules_first_scored": SCORED}
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    R.warm_cusolver()
    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    missing = [la for la in range(L + 1) if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at blocks {missing}"
    items, bad = z1_items(model.tokenizer, target)
    counts = plan_counts(items, bad, target)
    (out / "plan.json").write_text(json.dumps(counts, indent=1, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert not bad, f"{len(bad)} of Z1's items do not rebuild as stored, e.g. {bad[:3]}"
    assert items, "no items"
    ws = X.whitespace_mask(model)
    rows, losses, wrows, norms = run_items(model, lens, items, L, ws)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "losses.jsonl", losses)
    X.write_jsonl(out / "window.jsonl", wrows)
    X.write_jsonl(out / "norms.jsonl", norms)
    m["items"] = len(items)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(rows)} reads, {len(losses)} losses, {len(wrows)} window reads (sealed: no verdict)",
          flush=True)  # fmt: skip
    return out


# ---- verdict (CPU, sealed) ------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.7 (x50_zach.dan_answer: the 'Dan:' / 'Dan (27B):' lines and bullet continuations
    of its block in the predictions file at `rev`), '' if none."""
    return Z.dan_answer(QUESTION, rev)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def ok(v: float | None) -> bool:
    return Z.ok(v)


def slice_rule(rise: float, k_minus_m: float) -> dict[str, bool]:
    """(i): the fact-after rise >= 0.3 and the fact-first |K - M| <= 0.10 under the whole before-L."""
    a = ok(rise) and rise >= SLICE_RISE - EPS
    b = ok(k_minus_m) and abs(k_minus_m) <= NEAR + EPS
    return {"rise_ge_0_3": bool(a), "fact_first_within_0_1": bool(b), "slice_explanation": bool(a and b)}


def carrier_rule(lookup: float, gap: float) -> str:
    """(ii), as x50_zach.main_rule's bars."""
    if not ok(lookup):
        return "can't tell (no lookup switch under the whole before-L)"
    if ok(gap) and gap >= Z.GAP_MIN - EPS and lookup <= Z.LOOKUP_MAX + EPS:
        return "the split holds on the full carrier"
    if lookup >= Z.THROUGH_MIN - EPS:
        return "the lookup follows the lens on the full carrier"
    return "in between"


def away_rule(after_whole: float) -> bool:
    """(iii): fact-after lookups under 0.5 under the whole before-L."""
    return bool(ok(after_whole) and after_whole < AWAY - EPS)


def point_ci(values: list[float], draws) -> list[float]:
    return [float(np.mean(values)), *X.interval(draws)] if values else [math.nan] * 3


def group_result(sw: dict[tuple[str, str], dict], keys: list[tuple], ent: dict, n_boot: int) -> dict:
    """One stratum: every arm's switch share per reader, the one-layer and before-L cells (X0's), the gaps on paired
    draws, (ii)'s label, (i)'s two differences."""
    ents = [ent[k] for k in keys]
    arms = ("none", *ONE, *BEFORE, EMB)
    vals = {f"{w}|{a}": [sw[(w, a)][k] for k in keys] for w in READERS for a in arms}
    rr = X.resampled_rates(vals, ents, n_boot)
    shares = {w: {a: point_ci(vals[f"{w}|{a}"], rr[f"{w}|{a}"]) for a in arms} for w in READERS}
    out: dict[str, Any] = {"n": len(keys), "entities": len(set(ents)), "shares": shares}
    for kind, (wh, nj, rd) in KIND.items():
        cells, draws = {}, {}
        for w in READERS:
            cells[w] = X.cell({"whole": vals[f"{w}|{wh}"], "no_part": vals[f"{w}|{nj}"], "no_rand": vals[f"{w}|{rd}"]},
                              ents, n_boot)  # fmt: skip
            draws[w] = X.dependence(rr[f"{w}|{wh}"], rr[f"{w}|{nj}"]) - X.dependence(rr[f"{w}|{wh}"], rr[f"{w}|{rd}"])
        gap = [cells[RECALL]["excess"][0] - cells[LOOKUP]["excess"][0], *X.interval(draws[RECALL] - draws[LOOKUP])]
        out[kind] = {"lookup": cells[LOOKUP], "recall": cells[RECALL], "gap": gap,
                     "label": carrier_rule(cells[LOOKUP]["excess"][0], gap[0])}  # fmt: skip
    k, m = f"{LOOKUP}|whole_bL", f"{RECALL}|whole_bL"
    out["rise"] = [shares[LOOKUP]["whole_bL"][0] - shares[LOOKUP]["whole_1L"][0],
                   *X.interval(rr[k] - rr[f"{LOOKUP}|whole_1L"])]  # fmt: skip
    out["k_minus_m"] = [shares[LOOKUP]["whole_bL"][0] - shares[RECALL]["whole_bL"][0], *X.interval(rr[k] - rr[m])]
    return out


def loss_result(losses: list[dict], keys: list[tuple], ent: dict, n_boot: int) -> dict:
    """Per reader: the mean plain-text loss per arm (cluster CIs) and its ratio to the one-layer whole's."""
    by = {(r["set"], r["scene"], r["reader"], r["arm"]): r for r in losses}
    ents = [ent[k] for k in keys]
    out = {}
    for w in READERS:
        vals = {a: [by[(*k, w, a)]["loss"] for k in keys] for a in LOSS_ARMS}
        rr = X.resampled_rates(vals, ents, n_boot)
        base = float(np.mean(vals["whole_1L"]))
        with np.errstate(divide="ignore", invalid="ignore"):
            out[w] = {a: {"mean": point_ci(v, rr[a]),
                          "ratio_to_whole_1L": [float(np.mean(v)) / base if base > 0 else math.nan,
                                                *X.interval(rr[a] / rr["whole_1L"])],
                          "top_is_next": float(np.mean([by[(*k, w, a)]["top_is_next"] for k in keys]))}
                      for a, v in vals.items()}  # fmt: skip
    return out


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"target": target, "run": run, "status": "pending", "why": "no run here"}
    m = json.loads((src / "manifest.json").read_text())
    if not (src / "outcomes.jsonl").exists():
        return {"target": target, "run": run, "status": "pending", "why": "no outcome rows"}
    zsrc = Z.RESULTS / m["source"]
    zgate = json.loads((zsrc / "gate.json").read_text())
    cases = X.read_jsonl(src / "cases.jsonl")
    keys = [(c["set"], c["scene"]) for c in cases]
    ent = {k: c["bridge"] for k, c in zip(keys, cases, strict=True)}
    strat = {k: c["stratum"] for k, c in zip(keys, cases, strict=True)}
    sw: dict[tuple[str, str], dict] = collections.defaultdict(dict)
    top: dict[tuple[str, str], dict] = collections.defaultdict(dict)
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        sw[(r["reader"], r["arm"])][(r["set"], r["scene"])] = int(r["switched"])
        top[(r["reader"], r["arm"])][(r["set"], r["scene"])] = r["top"]
    for r in X.read_jsonl(zsrc / "outcomes.jsonl"):
        if r["layer"] != m["layer"]:
            continue
        k = (r["set"], r["scene"])
        if r["arm"] in Z1_ARM:
            sw[(r["reader"], Z1_ARM[r["arm"]])][k] = int(r["switched"])
        elif r["arm"] == "none":
            top[(r["reader"], "none_z1")][k] = r["top"]
    groups = {g: group_result(sw, [k for k in keys if g == "all" or strat[k] == g], ent, n_boot) for g in GROUPS}
    ff, fa = groups["fact-first"], groups["fact-after"]
    rule_i = {
        "rise": fa["rise"],
        "k_minus_m_fact_first": ff["k_minus_m"],
        **slice_rule(fa["rise"][0], ff["k_minus_m"][0]),
    }
    after_whole = fa["shares"][LOOKUP]["whole_bL"]
    rule_iii: dict[str, Any] = {"fact_after_lookup_whole_bL": after_whole, "away": away_rule(after_whole[0])}
    wrows = X.read_jsonl(src / "window.jsonl") if (src / "window.jsonl").exists() else []
    wk = [(r["set"], r["scene"]) for r in wrows]
    if wrows:
        vals = {"window": [int(r["switched"]) for r in wrows], "whole_bL": [sw[(LOOKUP, "whole_bL")][k] for k in wk]}
        rr = X.resampled_rates(vals, [ent[k] for k in wk], n_boot)
        window = {
            "n": len(wk),
            "entities": len({ent[k] for k in wk}),
            **{a: point_ci(v, rr[a]) for a, v in vals.items()},
        }
    else:
        window = {"n": 0}
    rule_iii["window"] = window if rule_iii["away"] else {"n": window["n"], "reported": False}
    single = {}
    for s in STRATA:
        for only in (True, False):
            ks = [k for k, c in zip(keys, cases, strict=True)
                  if c["stratum"] == s and (c["n_changed"][LOOKUP] == 1) == only]  # fmt: skip
            v = [sw[(LOOKUP, "whole_bL")][k] for k in ks]
            single[f"{s}, {'only the last token' if only else 'more tokens'} changed"] = {
                "n": len(ks),
                "lookup_whole_bL": float(np.mean(v)) if v else math.nan,
            }
    agree = [top[(w, "none")][k] == top[(w, "none_z1")].get(k) for w in READERS for k in keys]
    checks = {"none_matches_z1_none": [int(sum(agree)), len(agree)],
              "none_reads_O": {w: float(np.mean([top[(w, "none")][k] == c["readers"][w]["tok_A"]
                                                 for k, c in zip(keys, cases, strict=True)])) for w in READERS},
              "only_last_token": single}  # fmt: skip
    status = "tested" if zgate["pass"] else "not tested (Z1's gate; numbers descriptive only)"
    losses = X.read_jsonl(src / "losses.jsonl")
    return {"target": target, "run": run, "source": m["source"], "layer": m["layer"], "status": status,
            "gate": {k: v for k, v in zgate.items() if k not in ("order", "counts")}, "groups": groups,
            "rule_i": rule_i, "rule_ii": {g: groups[g]["before"]["label"] for g in GROUPS},
            "rule_ii_decisive": groups["fact-first"]["before"]["label"], "rule_iii": rule_iii,
            "loss": loss_result(losses, keys, ent, n_boot), "checks": checks}  # fmt: skip


def fmt(v: list | None) -> str:
    return Z.fmt(v)


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# Batch 51, 51.7: Z1 on the full carrier (UNVERIFIED)", "",
             f"{QUESTION} (Dan: {answer}). Items: Z1's chosen passages (Zach's jsuite v2, P start, named bridge). "
             f"Cluster bootstrap over the original bridge entity ({n_boot}, seed {X.BOOT_SEED}).", "",
             f"Rule (fixed in advance): {RULE}", "", f"As computed: {AS_COMPUTED}", "",
             "| model | run | status | (i) fact-after rise | (i) fact-first K - M | (i) slice explanation | (ii) fact-first "
             "(decisive) | (ii) fact-after | (iii) away from the bridge token |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        if "groups" not in mm:
            lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} ({mm.get('why', '')}) |" + " |" * 6)
            continue
        ri = mm["rule_i"]
        lines.append(f"| {mm['target']} | {mm['run']} | {mm['status']} | {fmt(ri['rise'])} ({ri['rise_ge_0_3']}) | "
                     f"{fmt(ri['k_minus_m_fact_first'])} ({ri['fact_first_within_0_1']}) | {ri['slice_explanation']} | "
                     f"{mm['rule_ii']['fact-first']} | {mm['rule_ii']['fact-after']} | {mm['rule_iii']['away']} |")  # fmt: skip
    for mm in models:
        if "groups" not in mm:
            continue
        g = mm["gate"]
        lines += ["", f"## {mm['target']} ({mm['run']}, L{mm['layer']}; items from {mm['source']})", "",
                  f"Z1's gate: O's read accuracy {g.get('org_read_accuracy')}, pass {g.get('pass')}; chosen "
                  f"{g.get('chosen')} (strata {g.get('chosen_strata')}).", "",
                  "Switch shares (the other entity's answer), one-layer (Z1's stored rows) and before-L (this run):", "",
                  "| stratum | n (entities) | reader | none | whole 1L | without J++ 1L | random 1L | whole bL | "
                  "without J++ bL | random bL | whole bL + emb |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for gname, gr in mm["groups"].items():
            for w in READERS:
                s = gr["shares"][w]
                lines.append(f"| {gname} | {gr['n']} ({gr['entities']}) | {w} | "
                             + " | ".join(fmt(s[a]) for a in ("none", *ONE, *BEFORE, EMB)) + " |")  # fmt: skip
        lines += ["", "Extra loss without J++ (X0's excess) and the gap (rule ii; before-L decides, one-layer beside):", "",
                  "| stratum | carrier | K extra loss | M extra loss | gap | label | K S_whole | M S_whole | K valid | "
                  "M valid |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for gname, gr in mm["groups"].items():
            for kind in ("before", "one"):
                c = gr[kind]
                lines.append(f"| {gname} | {kind} | {fmt(c['lookup']['excess'])} | {fmt(c['recall']['excess'])} | "
                             f"{fmt(c['gap'])} | {c['label']} | {fmt(c['lookup']['S_whole'])} | "
                             f"{fmt(c['recall']['S_whole'])} | {c['lookup']['valid']} | {c['recall']['valid']} |")  # fmt: skip
        r3 = mm["rule_iii"]
        lines += ["", f"Rule (iii): fact-after lookups under the whole before-L {fmt(r3['fact_after_lookup_whole_bL'])}; "
                  f"under 0.5: {r3['away']}."]  # fmt: skip
        if r3["away"]:
            wd = r3["window"]
            lines.append(f"\"The link is made away from the bridge token\". Window read (descriptive; K reader, the first "
                         f"{wd['n']} fact-after passages, {wd.get('entities')} entities): window {fmt(wd.get('window'))} vs "
                         f"whole before-L on the same passages {fmt(wd.get('whole_bL'))}.")  # fmt: skip
        else:
            lines.append(f"The window read ({r3['window']['n']} passages) is recorded in window.jsonl and not reported "
                         "(rule iii's condition does not hold).")  # fmt: skip
        lines += ["", "Plain-text loss at the patch token (O's own next token), mean [CI] and ratio to the one-layer "
                  "whole's, all passages (descriptive):", "", "| reader | " + " | ".join(LOSS_ARMS) + " |",
                  "|---|" + "---|" * len(LOSS_ARMS)]  # fmt: skip
        for w in READERS:
            lw = mm["loss"][w]
            lines.append(f"| {w} | " + " | ".join(f"{fmt(lw[a]['mean'])} (x{lw[a]['ratio_to_whole_1L'][0]:.2f})"
                                                  for a in LOSS_ARMS) + " |")  # fmt: skip
        ck = mm["checks"]
        lines += ["", f"Checks: our none read's top token equals Z1's stored none read on {ck['none_matches_z1_none'][0]} "
                  f"of {ck['none_matches_z1_none'][1]} (passage, reader); none reads O's answer {ck['none_reads_O']}; the "
                  f"lookup's whole before-L by whether only the name's last token differs: "
                  f"{json.dumps(ck['only_last_token'])}."]  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def figure(mm: dict, path: Path) -> None:
    """Stratum x reader; per panel one-layer vs before-L, three arms (whole, without J++, random), 95% intervals."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"whole": "#2a6fbb", "without J++": "#e07b39", "random part": "#8c8c8c"}
    fig, axes = plt.subplots(len(STRATA), len(READERS), figsize=(7.2, 5.4), sharey=True)
    wd = 0.26
    for i, s in enumerate(STRATA):
        gr = mm["groups"][s]
        for j, w in enumerate(READERS):
            ax = axes[i][j]
            for x0, arms in enumerate((ONE, BEFORE)):
                for t, (a, lab) in enumerate(zip(arms, colors, strict=True)):
                    v = gr["shares"][w][a]
                    err = [[max(v[0] - v[1], 0)], [max(v[2] - v[0], 0)]]
                    ax.bar(x0 + (t - 1) * wd, v[0], wd * 0.92, yerr=err, color=colors[lab], capsize=2,
                           label=lab if (i, j, x0) == (0, 0, 0) else None, error_kw={"lw": 0.8})  # fmt: skip
            ax.set_xticks([0, 1], ["one layer (Z1)", f"every layer <= L{mm['layer']}"], fontsize=8)
            ax.set_ylim(0, 1)
            ax.grid(axis="y", lw=0.4, alpha=0.4)
            ax.set_title(f"{s}, {'lookup (K)' if w == LOOKUP else 'recall (M)'}; n {gr['n']}", fontsize=9)
            if j == 0:
                ax.set_ylabel("switch share")
    fig.legend(loc="upper center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.995))
    fig.suptitle(f"51.7 {mm['target']}: the change at the bridge name's last token (UNVERIFIED)", fontsize=9, y=0.94)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def view_lines(
    run: str, decode=None, n_prompts: int = N_PROMPTS, n_rows: int = N_ROWS, seed: int = VIEW_SEED
) -> list[str]:
    """The verify pack: n_prompts random passages' prompts as read (seed), then per arm n_rows random rows (seed)."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    cases = X.read_jsonl(src / "cases.jsonl")
    by_key = {(c["set"], c["scene"]): c for c in cases}
    rows = X.read_jsonl(src / "outcomes.jsonl") + (
        X.read_jsonl(src / "window.jsonl") if (src / "window.jsonl").exists() else []
    )
    loss = {(r["set"], r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "losses.jsonl")}
    lines = [f"## {run} ({m['model']['target']}, blocks 0..{m['layer']}): {min(n_prompts, len(cases))} random passages "
             f"of {len(cases)} (random.Random({seed}))", ""]  # fmt: skip
    for i in sorted(random.Random(seed).sample(range(len(cases)), min(n_prompts, len(cases)))):
        lines += prompt_lines(decode, cases[i])
    for arm in (*READ_ARMS, WINDOW):
        mine = [r for r in rows if r["arm"] == arm]
        pick = sorted(random.Random(seed).sample(range(len(mine)), min(n_rows, len(mine))))
        lines += [f"### arm {arm}: {len(pick)} random rows of {len(mine)} (random.Random({seed}))", "",
                  "| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |",
                  "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for j in pick:
            r = mine[j]
            c = by_key[(r["set"], r["scene"])]
            lr = loss.get((r["set"], r["scene"], r["reader"], arm))
            lines.append(f"| {r['set']}/{r['scene']} | {r['stratum']} | {r['reader']} | {c['answer']} | {c['cf_answer']} | "
                         f"{decode([r['top']])!r} | {r['switched']} | {r['route']} | {lr['loss'] if lr else '-'} |")  # fmt: skip
        lines.append("")
    return lines


def resolve(runs: list[str] | None) -> dict[str, str]:
    if not runs:
        return dict(RUNS)
    inv = {r: t for t, r in {**RUNS, **COVERAGE_RUNS}.items()}
    return {inv.get(r, json.loads((RESULTS / r / "manifest.json").read_text())["model"]["target"]): r for r in runs}


def stage_verdict(runs: list[str] | None = None, n_boot: int = X.N_BOOT, decode=None, coverage: bool = False) -> Path:
    """51.7's verdict (sealed until Q51.7), or with coverage (batch 52) the same rules on COVERAGE_RUNS alone, no seal
    guard, "no prediction" in place of Dan's answer (x52_carrier-<UTC>/)."""
    answer = f"{NO_PREDICTION}; rules first scored in {SCORED}" if coverage else unsealed()
    models = [
        model_result(t, r, n_boot)
        for t, r in resolve(runs or (list(COVERAGE_RUNS.values()) if coverage else None)).items()
    ]
    out = RESULTS / f"{'x52_carrier' if coverage else 'x51_7'}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    if coverage:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 coverage, ") for ln in lines]
    for mm in models:
        if "groups" in mm:
            png = out / f"x51_7_{mm['target']}.png"
            figure(mm, png)
            lines += ["", f"Figure: {png.name}"]
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"dan": answer, "models": models}, indent=1, default=str) + "\n")
    view = ["# 51.7 view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the patch token. UNVERIFIED.", ""]
    for mm in models:
        if "groups" in mm:
            view += view_lines(mm["run"], decode)
    (out / "view.md").write_text("\n".join(view) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_view(runs: list[str] | None = None, decode=None) -> Path:
    unsealed()
    out = RESULTS / f"x51_7-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.7 view (verify pack). UNVERIFIED.", ""]
    for run in resolve(runs).values():
        if (RESULTS / run / "outcomes.jsonl").exists():
            lines += view_lines(run, decode)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x51_carrier/<name>/)")
    ap.add_argument("--runs", nargs="+", help="verdict / view: the runs (default: the 9B's and the 27B's)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--plan-dir", help="plan: the folder to write into (one per model, the same folder)")
    ap.add_argument("--coverage", action="store_true", help=f"verdict: batch 52 coverage runs ('{NO_PREDICTION}')")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.plan_dir)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot, coverage=a.coverage)
    else:
        stage_view(a.runs)


if __name__ == "__main__":
    main()
