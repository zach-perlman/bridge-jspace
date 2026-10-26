"""x6_routes (Dan, 25 Oct ~01:50; after Gur-Arieh et al. 2025, arXiv 2510.06182): which information from the bridge word
does the lookup follow, the item's identity, its locker sentence's position, or the locker value?

Scenes (animals, generated here, seed fixed): 3 single-token items A, B, C, their 3 locker sentences ("The locker of
the frog is 5.", single digits) first, then 3 pick sentences (Iris picked A; two others picked B and C); every item's
first mention is its locker sentence. Original O: lockers A:a, B:b, C:c; lookup "Which locker belongs to Iris's pick?"
-> a; recall "How many legs does Iris's pick have?". A source S, and h_S - h_O added at the bridge word (Iris's pick)
at the layer fixed in advance, read on O:
  C0 sanity: S = O but Iris picked B (same order, same digits)              switch = b
  C1 position only: same bridge A; A's and C's locker sentences swapped, A -> d (new digit)
     identity / nothing -> a, position -> c, value -> d
  C2 identity vs position: Iris picked B; B's and C's locker sentences swapped, B -> e (new digit)
     identity -> b, position -> c, value -> e, nothing -> a
S's digits d, e are disjoint from O's a, b, c. All locker sentences have the same token length, so the bridge sits at
the same token index in O and S (asserted per scene; failures dropped and counted). The recall is the control: in C2 it
should follow B, in C1 stay on A.
Arms: whole; without the J++ part (k = 25, signed); without a random part of its share; without the pointer directions
(Alf, fit on the old fresh scenes, not refit, as in F15) and without a random part of their share.
Read: X0's chat read (the top token after the digit's space); each lookup answer classified as identity / position /
value / original / other (C1: identity = original). Eligible (X0): both readers say and read O's and S's answers
right; the first N per condition. Gate: O's read accuracy >= 0.80 per reader and condition (--gate: a lowered,
descriptive gate after the data, Dan 25 Oct ~13:20).
--bothoff (x6_routes_bothoff, Dan 25 Oct ~13:20): two more arms, without the union of the J++ part's span and the
pointer directions (each item's 25 signed-OMP atoms together with Alf; least-squares projection) and without a random
part of the union's share; per condition and reader, each part's extra loss and the union's minus the pointer
directions' (paired bootstrap).
--bothoff-ctrl (x6_routes_bothoff_ctrl, Dan 25 Oct ~14:30): one more arm, without the union of the pointer directions
and a random part of the J++ part's share (orthonormalized); per condition and reader, the switches lost without the
pointer directions, without them and J++, without them and the random part, and the second minus the third.
--keeponly (x6_routes_keeponly, Dan 25 Oct ~15:50): four more arms that add ONLY a part of the change at the bridge
word: the pointer-direction part, a random part of its share, the J++ part, a random part of J++'s share.
--identity (D1, Dan 26 Oct ~11:55): per scene the rank-1 identity direction mu_alt - mu_org (the two entities' mean
layout-free bridge-word states on the probe's fresh scenes) and that direction orthogonalized against the scene's 25 J++
atoms ("idout"); arms without id, without idout, without the pointer directions + idout, without J++ + the pointer
directions + idout, each against a random part of its own share; only id and its random part; and, descriptive, without
the identity subspace (the mass-mean of all entities, rank = entities - 1). Every part's share in norms.jsonl.
Rule (Dan, fixed in advance): a route counts as used if its share is >= 0.20 with lower CI >= 0.10 (cluster bootstrap
over the bridge item, 10,000 resamples, seed 0). C0 must reproduce the one-pick lookup switch rate within 0.10, or the
run stops.

uv run python scripts/x6_routes.py plan                                   # tokenizer only
uv run python scripts/x6_routes.py run --name x6_routes_27b               # GPU (C0 check, then C1 / C2), verdict
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x6_routes"
RESULTS = pins.RESULTS_DIR / EXP
SEED, N_GEN, N_ITEMS, N_SMOKE = 2510, 700, 300, 20
CONDITIONS = ("C0", "C1", "C2")
ROUTES = ("identity", "position", "value", "original", "other")
USED_SHARE, USED_LO = 0.20, 0.10
C0_TOL = 0.10
ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "no_both", "no_both_rand", "no_alf_jrand",
        "keep_alf", "keep_alf_rand", "keep_jpp", "keep_jpp_rand",
        # --identity (D1, Dan 26 Oct ~11:55): the rank-1 identity direction, it outside J++, with the pointer, with both
        "no_id", "no_id_rand", "no_idout", "no_idout_rand", "no_alfidout", "no_alfidout_rand", "no_jppalfidout",
        "no_jppalfidout_rand", "keep_id", "keep_id_rand", "no_idsub")  # fmt: skip
# --bothoff-ctrl: switches lost (Jdep) without the pointer directions, without them and J++, without them and a random
# part of J++'s share; the question is the second minus the third (Dan's Q36.1)
CTRL = (("alf", "no_alf"), ("alf + J++", "no_both"), ("alf + random (J++ share)", "no_alf_jrand"))
PARTS = (("jpp", "no_jpp", "no_jpp_rand"), ("alf", "no_alf", "no_alf_rand"), ("both", "no_both", "no_both_rand"),
         ("id", "no_id", "no_id_rand"), ("idout", "no_idout", "no_idout_rand"),
         ("alf+idout", "no_alfidout", "no_alfidout_rand"), ("jpp+alf+idout", "no_jppalfidout", "no_jppalfidout_rand"))  # fmt: skip
# the one-pick lookup switch rate in scenes with both locker sentences before the pick (x0_massmean_lf's items, the
# whole change), the reference C0 must reproduce (Dan: within 0.10)
C0_REF = {
    "qwen3.5-9b": ("qwen35_9b_x0_massmean_lf", "whole"),
    "qwen3.6-27b": ("x0_massmean_lf_27b", "whole"),
    "qwen3.5-122b-a10b": ("qwen35_122b_x0_massmean_grid", "whole"),
}  # fmt: skip (Muse: none; its C0 gate is --c0-min)
STATES = {"qwen3.5-9b": "qwen35_9b_x0_probe_v4", "qwen3.6-27b": "x0_probe_v4_27b",
          "qwen3.5-122b-a10b": "qwen35_122b_x0_probe_v4", "muse-glimmer-30b": "muse30b_x0_probe_v4"}  # fmt: skip
NOTE = "Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32)."
LOOKUP_Q, RECALL_Q = "Which locker belongs to {p}'s pick?", "How many legs does {p}'s pick have?"


def one_token(tok, word: str) -> bool:
    from scripts import suite_v1 as S

    return len(S.ids(tok, " " + word)) == 1


def context(lockers: list[tuple[str, int]], picks: list[tuple[str, str]]) -> str:
    return " ".join([f"The locker of the {x} is {d}." for x, d in lockers] + [f"{p} picked the {x}." for p, x in picks])


def scenes(tok, n: int, seed: int = SEED) -> tuple[list[dict], collections.Counter]:
    """n scenes per condition: O, S and the answers each route predicts; drops counted by reason."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    legs = T.DOMAINS["animals"].values
    animals = sorted(a for a in legs if one_token(tok, a) and 0 <= legs[a] <= 9)
    people = sorted(p for p in S.PEOPLE if one_token(tok, p))
    rng = random.Random(seed)
    out, dropped = [], collections.Counter()
    i = 0
    while len(out) < n * len(CONDITIONS):
        i += 1
        assert i < 100 * n, f"the generator cannot fill {n} scenes per condition: {dropped}"
        A, B, C = rng.sample(animals, 3)
        if legs[A] == legs[B]:
            dropped["A and B have the same number of legs"] += 1
            continue
        a, b, c, d, e = rng.sample(range(1, 10), 5)
        asked, p1, p2 = rng.sample(people, 3)
        order = rng.sample([A, B, C], 3)  # the locker sentences' slots
        val = {A: a, B: b, C: c}
        picks = rng.sample([(asked, A), (p1, B), (p2, C)], 3)
        o = context([(x, val[x]) for x in order], picks)
        for cond in CONDITIONS:
            if cond == "C0":
                s_lock, s_pick, bridge = (
                    [(x, val[x]) for x in order],
                    [(q, B if q == asked else x) for q, x in picks],
                    B,
                )
                expect = {"switch": b, "original": a}
            elif cond == "C1":
                sw = {A: C, C: A}
                s_lock = [(sw.get(x, x), d if sw.get(x, x) == A else val[sw.get(x, x)]) for x in order]
                s_pick, bridge = picks, A
                expect = {"identity": a, "position": c, "value": d, "original": a}
            else:
                sw = {B: C, C: B}
                s_lock = [(sw.get(x, x), e if sw.get(x, x) == B else val[sw.get(x, x)]) for x in order]
                s_pick, bridge = [(q, B if q == asked else x) for q, x in picks], B
                expect = {"identity": b, "position": c, "value": e, "original": a}
            s = context(s_lock, s_pick)
            case, why = encode(tok, o, s, asked, A, bridge, legs, expect, cond, f"{cond}-{i:04d}")
            if case is None:
                dropped[f"{cond}: {why}"] += 1
            elif sum(c_["condition"] == cond for c_ in out) < n:
                out.append(case)
    return out, dropped


def encode(tok, o: str, s: str, asked: str, a_item: str, bridge: str, legs: dict, expect: dict, cond: str, scene: str):
    """Both readers' O and S prompts; the bridge one token at the same index in O and S (asserted)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    readers, pos = {}, None
    s_answer = expect["switch"] if "switch" in expect else expect["value"]
    for w, q, ans in ((X.LOOKUP, LOOKUP_Q, (expect["original"], s_answer)),
                      (X.RECALL, RECALL_Q, (legs[a_item], legs[bridge]))):  # fmt: skip
        ids, at = {}, {}
        for v, ctx, x in (("org", o, a_item), ("alt", s, bridge)):
            item = {"format": "prose", "kind": "digit", "context": ctx, "question": q.format(p=asked)}
            text = T.render(tok, item)
            enc = raw_encoding(tok, text, offsets=True)
            sent = f"{asked} picked the {x}."
            w0 = text.index(ctx) + ctx.index(sent) + sent.index(x)
            ids[v], at[v] = list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(x))
        if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
            return None, "the bridge is not one token at the same index in O and S"
        if pos is not None and at["org"][0] != pos:
            return None, "the readers' bridge positions differ"
        pos = at["org"][0]
        org_ans, alt_ans = (str(v) for v in ans)
        readers[w] = {"question": q.format(p=asked), "answer": org_ans, "cf_answer": alt_ans, "ids": ids,
                      "tok_A": S.answer_token(tok, org_ans, "digit"), "tok_b": S.answer_token(tok, alt_ans, "digit")}  # fmt: skip
    for v in ("org", "alt"):
        if readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1]:
            return None, "the readers' prompts differ before the bridge"
    routes = {k: S.answer_token(tok, str(v), "digit") for k, v in expect.items() if k != "switch"}
    return {"scene": scene, "condition": cond, "rendering": "chat", "domain": "animals", "bridge": a_item,
            "cf_bridge": bridge, "context": o, "cf_context": s, "pos": pos, "space": S.ids(tok, " "),
            "expect": {k: int(v) for k, v in expect.items()}, "route_tokens": routes, "readers": readers}, ""  # fmt: skip


def classify(top: int, case: dict) -> str:
    """The lookup answer's route (C1: identity = original, reported as identity)."""
    hit = [r for r in ("identity", "position", "value", "original") if case["route_tokens"].get(r) == top]
    return hit[0] if hit else "other"


def stage_plan() -> None:
    from scripts import statement_positions as SP

    cases, dropped = scenes(SP.load_tokenizer(), N_GEN)
    print(json.dumps({"cases": collections.Counter(c["condition"] for c in cases), "dropped": dropped}, indent=1))
    for cond in CONDITIONS:
        c = next(c for c in cases if c["condition"] == cond)
        print(cond, "O:", c["context"], "\n   S:", c["cf_context"], "\n   expect", c["expect"])


def c0_reference(target: str) -> float | None:
    """The one-pick, locker-first lookup switch rate C0 must reproduce; None for a target without one (Muse: its C0 gate
    is --c0-min, Dan's G2)."""
    if target not in C0_REF:
        return None
    run, arm = C0_REF[target]
    rows = X.read_jsonl(pins.RESULTS_DIR / "x0_massmean" / run / "outcomes.jsonl")
    return float(np.mean([r["switched"] for r in rows if r["reader"] == X.LOOKUP and r["arm"] == arm]))


def union_part(jdic, alf, x, k: int):
    """Each row of x projected onto the span of its k signed-OMP J++ atoms together with the pointer directions."""
    import torch

    from scripts.x0_parts import omp_atoms

    atoms = omp_atoms(jdic, x, k)
    out = torch.empty_like(x)
    for i in range(x.shape[0]):
        span = torch.cat([jdic[atoms[i]].T.double(), alf.double()], dim=1)  # [d, k + r]
        u, s, _ = torch.linalg.svd(span, full_matrices=False)
        u = u[:, s > s[0] * 1e-6]  # an atom inside the pointer span adds no direction
        out[i] = (u @ (u.T @ x[i].double())).float()
    return out


def span_part(x, cols):
    """Each row of x projected onto the span of its own columns cols[i] ([d, m_i]), orthonormalized."""
    import torch

    out = torch.empty_like(x)
    for i in range(x.shape[0]):
        u, s, _ = torch.linalg.svd(cols[i].double(), full_matrices=False)
        u = u[:, s > s[0] * 1e-6]
        out[i] = (u @ (u.T @ x[i].double())).float()
    return out


def identity_dirs(means, pairs, jdic, x, k: int):
    """D1 (Dan 26 Oct ~11:55): per scene the unit identity direction mu_alt - mu_org (`pairs`: (org, alt) entities;
    `means`: entity -> mean layout-free state), and that direction orthogonalized against the scene's k signed-OMP J++
    atoms ("identity outside J++"); also the atoms."""
    import torch

    from scripts.x0_parts import omp_atoms

    atoms = omp_atoms(jdic, x, k)
    u = torch.stack([means[alt] - means[org] for org, alt in pairs])
    u = u / u.norm(dim=1, keepdim=True)
    out = []
    for i in range(len(pairs)):
        q, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        v = u[i].double() - q @ (q.T @ u[i].double())
        out.append((v / v.norm()).float())
    return u, torch.stack(out), atoms


def rank1_part(x, u):
    """Each row of x projected onto its own unit direction u[i]."""
    return (x * u).sum(dim=1, keepdim=True) * u


def random_k(x, share, basis):
    """Per row of x, the number of leading columns of `basis` whose projection keeps share[row] of the row's squared
    norm (the rule of statement_positions.random_subspace_part)."""
    import torch

    coef = x.float() @ basis
    cum = torch.cumsum(coef**2, dim=-1) / (x.float().norm(dim=-1, keepdim=True) ** 2).clamp_min(1e-30)
    cum = torch.cat([torch.zeros_like(cum[:, :1]), cum], dim=-1)
    return (cum - share.float()[:, None]).abs().argmin(dim=-1)


def union_rand_part(alf, x, share, basis):
    """Each row of x projected onto the span of the pointer directions together with a random part of the given share
    (the leading random_k columns of `basis`), orthonormalized."""
    import torch

    k = random_k(x, share, basis)
    out = torch.empty_like(x)
    for i in range(x.shape[0]):
        span = torch.cat([basis[:, : int(k[i])].double(), alf.double()], dim=1)
        u, s, _ = torch.linalg.svd(span, full_matrices=False)
        u = u[:, s > s[0] * 1e-6]
        out[i] = (u @ (u.T @ x[i].double())).float()
    return out


def stage_run(
    name: str,
    smoke: bool,
    layer: int | None = None,
    c0_min: float | None = None,
    pointer: bool = True,
    conds: tuple[str, ...] = CONDITIONS,
    bothoff: bool = False,
    gate_min: float = X.GATE,
    ctrl: bool = False,
    keeponly: bool = False,
    identity: bool = False,
    alf_from: str | None = None,
) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = layer if layer is not None else X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    assert pointer or not bothoff, "--bothoff needs the pointer directions"
    assert bothoff or not ctrl, "--bothoff-ctrl needs --bothoff"
    assert pointer or not keeponly, "--keeponly needs the pointer directions"
    assert pointer or not identity, "--identity needs the pointer directions"
    conds = ("C0",) if smoke else conds
    n = N_SMOKE if smoke else N_ITEMS
    ref = c0_reference(target)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "seed": SEED,
         "smoke": smoke, "conditions": list(conds), "n_per_condition": n, "gate": gate_min, "gate_fixed_in_advance": X.GATE, "bothoff": bothoff, "bothoff_ctrl": ctrl, "keeponly": keeponly, "identity": identity,
         "alf_from": (alf_from or STATES[target]) if pointer else None, "c0_min": c0_min, "fixed_layer": X.PREDICTED[target],
         "c0_reference": {"run": C0_REF.get(target, (None,))[0], "lookup_switch": ref, "tolerance": C0_TOL},
         "rule": f"a route is used iff its share >= {USED_SHARE} with lower CI >= {USED_LO}",
         "seeds": {"scenes": SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    cases, dropped = scenes(tok, N_GEN)
    cases = [c for c in cases if c["condition"] in conds]
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate, chosen = {}, []
    for cond in conds:
        mine = [c for c in cases if c["condition"] == cond]
        acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in mine])) for w in X.READERS}
        ok = [c for c in mine if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                     for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
        gate[cond] = {"cases": len(mine), "org_read_accuracy": acc, "pass": all(a >= gate_min for a in acc.values()),
                      "eligible": len(ok)}  # fmt: skip
        if gate[cond]["pass"]:
            chosen += ok[:n]
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    (out / "gate.json").write_text(json.dumps({"dropped": dropped, "gate": gate}, indent=2) + "\n")
    if not chosen:
        raise SystemExit("no condition passed the gate fixed in advance (or none had eligible items); see gate.json")
    sub = MM.subspaces(STATES[target])[0] if pointer else {}
    if alf_from:  # P_cf (x7_pcf, batch 43) in place of the mass-mean pointer directions
        sub["Alf"] = np.load(pins.RESULTS_DIR / alf_from / "pcf.npz")["P"]
    alf = torch.tensor(sub["Alf"], dtype=torch.float32, device="cuda") if pointer else None
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    rows, norms = [], []
    with torch.no_grad():
        deltas = []
        for c in progress(chosen, "Δ at the bridge word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                 for v in ("org", "alt")}  # fmt: skip
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        jpp = X.fit(jdic, x, X.K_MAIN, "signed")
        ptr = (x @ alf) @ alf.T if pointer else torch.zeros_like(x)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        both = union_part(jdic, alf, x, X.K_MAIN) if bothoff else torch.zeros_like(x)
        sh = {k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
              for k, v in (("jpp", jpp), ("alf", ptr), ("both", both))}  # fmt: skip
        arms = {"whole": x, "no_jpp": x - jpp, "no_jpp_rand": x - SP.random_subspace_part(x, sh["jpp"], basis)}
        if pointer:
            arms.update({"no_alf": x - ptr, "no_alf_rand": x - SP.random_subspace_part(x, sh["alf"], basis)})
        if bothoff:
            arms.update({"no_both": x - both, "no_both_rand": x - SP.random_subspace_part(x, sh["both"], basis)})
        if ctrl:
            arms["no_alf_jrand"] = x - union_rand_part(alf, x, sh["jpp"], basis)
        if keeponly:
            arms.update({"keep_alf": ptr, "keep_alf_rand": SP.random_subspace_part(x, sh["alf"], basis),
                         "keep_jpp": jpp, "keep_jpp_rand": SP.random_subspace_part(x, sh["jpp"], basis)})  # fmt: skip
        if identity:  # D1: the rank-1 identity direction mu_alt - mu_org, and it outside the scene's J++ atoms
            assert alf is not None
            means = {e: torch.tensor(v, dtype=torch.float32, device="cuda")
                     for e, v in MM.entity_means(STATES[target]).items()}  # fmt: skip
            u, u_out, atoms = identity_dirs(means, [(c["bridge"], c["cf_bridge"]) for c in chosen], jdic, x, X.K_MAIN)
            idsub = torch.tensor(sub["Id"], dtype=torch.float32, device="cuda")
            m["id_rank"] = int(idsub.shape[1])
            parts = {"id": rank1_part(x, u), "idout": rank1_part(x, u_out),
                     "alf+idout": span_part(x, [torch.cat([alf, u_out[i : i + 1].T], 1) for i in range(len(chosen))]),
                     "jpp+alf+idout": span_part(x, [torch.cat([jdic[atoms[i]].T, alf, u_out[i : i + 1].T], 1)
                                                    for i in range(len(chosen))]),
                     "idsub": (x @ idsub) @ idsub.T}  # fmt: skip
            for k, v in parts.items():
                sh[k] = v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            for k, name in (
                ("id", "id"),
                ("idout", "idout"),
                ("alf+idout", "alfidout"),
                ("jpp+alf+idout", "jppalfidout"),
            ):
                arms[f"no_{name}"] = x - parts[k]
                arms[f"no_{name}_rand"] = x - SP.random_subspace_part(x, sh[k], basis)
            arms.update({"keep_id": parts["id"], "keep_id_rand": SP.random_subspace_part(x, sh["id"], basis),
                         "no_idsub": x - parts["idsub"]})  # fmt: skip
        for i, c in enumerate(progress(chosen, f"reads at layer {layer} (case)")):
            norms.append({"scene": c["scene"], "condition": c["condition"], "norm": round(float(x[i].norm()), 4),
                          **{f"share_{k}": round(float(v[i]), 5) for k, v in sh.items()}})  # fmt: skip
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in arms]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for a, lg in zip(("none", *arms), logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "condition": c["condition"], "entity": c["bridge"], "reader": w,
                                 "arm": a, "top": top, "route": classify(top, c) if w == X.LOOKUP else None,
                                 **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    m["items"] = {cond: sum(c["condition"] == cond for c in chosen) for cond in conds}
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    if "C0" in conds:
        c0 = [r["switched"] for r in rows if r["condition"] == "C0" and r["reader"] == X.LOOKUP and r["arm"] == "whole"]
        rate = float(np.mean(c0)) if c0 else float("nan")
        assert c0_min is not None or ref is not None, "no C0 reference for this target: pass --c0-min"
        ok = rate >= c0_min if c0_min is not None else abs(rate - ref) <= C0_TOL
        (out / "c0_check.json").write_text(json.dumps({"c0_lookup_switch": rate, "reference": ref, "c0_min": c0_min,
                                                       "ok": ok}) + "\n")  # fmt: skip
        if not ok:
            raise SystemExit("C0 sanity failed (" + (f"below {c0_min}" if c0_min is not None else f"not within {C0_TOL} of the "
                             "reference") + "); stop")  # fmt: skip
    print("wrote", out, flush=True)
    return out


def extra_losses(
    rows: list[dict], conds: list[str], n_boot: int = X.N_BOOT, norms: list[dict] | None = None
) -> list[dict]:
    """Per condition and reader: X0's cell (Jdep, Rdep, extra loss) for J++, the pointer directions and their union,
    each against its own random part; then the union's extra loss minus the pointer directions' on the same resamples."""
    out = []
    for cond in [c for c in CONDITIONS if c in conds]:
        for w in X.READERS:
            by = {a: {r["scene"]: r for r in rows if r["condition"] == cond and r["reader"] == w and r["arm"] == a}
                  for a in ARMS}  # fmt: skip
            scenes_ = sorted(by["whole"])
            ents = [by["whole"][s]["entity"] for s in scenes_]
            sw = {a: [int(by[a][s]["switched"]) for s in scenes_] for a in ARMS if by[a]}
            rr = X.resampled_rates(sw, ents, n_boot)
            ex, point = {}, {}
            for part, no, rand in PARTS:
                if no not in sw or rand not in sw:  # a run without these arms
                    continue
                c = X.cell({"whole": sw["whole"], "no_part": sw[no], "no_rand": sw[rand]}, ents, n_boot)
                ex[part] = X.dependence(rr["whole"], rr[no]) - X.dependence(rr["whole"], rr[rand])
                point[part] = c["excess"][0]
                share = [n[f"share_{part}"] for n in (norms or []) if n["condition"] == cond and f"share_{part}" in n]
                out.append({"condition": cond, "reader": w, "part": part, **c,
                            "share": float(np.median(share)) if share else float("nan")})  # fmt: skip
            if "both" in ex and "alf" in ex:
                out.append({"condition": cond, "reader": w, "part": "both - alf", "n": len(scenes_),
                            "excess": [point["both"] - point["alf"], *X.interval(ex["both"] - ex["alf"])]})  # fmt: skip
    return out


def ctrl_losses(rows: list[dict], conds: list[str], n_boot: int = X.N_BOOT) -> list[dict]:
    """Per condition and reader: the switches lost (Jdep) without each CTRL arm, and the J++ union's minus the random
    union's (paired resamples)."""
    out = []
    for cond in [c for c in CONDITIONS if c in conds]:
        for w in X.READERS:
            by = {a: {r["scene"]: r for r in rows if r["condition"] == cond and r["reader"] == w and r["arm"] == a}
                  for a in ("whole", *(arm for _, arm in CTRL))}  # fmt: skip
            scenes_ = sorted(by["whole"])
            ents = [by["whole"][s]["entity"] for s in scenes_]
            sw = {a: [int(v[s]["switched"]) for s in scenes_] for a, v in by.items()}
            rr = X.resampled_rates(sw, ents, n_boot)
            mean = {a: float(np.mean(v)) for a, v in sw.items()}
            lost = {}
            for label, arm in CTRL:
                lost[arm] = X.dependence(rr["whole"], rr[arm])
                point = float(X.dependence(mean["whole"], mean[arm]))
                out.append({"condition": cond, "reader": w, "arm": label, "n": len(scenes_), "S_whole": mean["whole"],
                            "lost": [point, *X.interval(lost[arm])]})  # fmt: skip
            point = out[-2]["lost"][0] - out[-1]["lost"][0]
            out.append({"condition": cond, "reader": w, "arm": "alf + J++ - alf + random", "n": len(scenes_),
                        "lost": [point, *X.interval(lost["no_both"] - lost["no_alf_jrand"])]})  # fmt: skip
    return out


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    norms = X.read_jsonl(src / "norms.jsonl")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# Which route the lookup follows: {name}", "", f"{NOTE} Model {m['model']['target']}, layer {m['layer']}. "
             f"Cluster bootstrap over the bridge item ({n_boot} resamples). UNVERIFIED.", "",
             "| condition | arm | n | " + " | ".join(ROUTES) + " | recall follows S |", "|---|---|---|" + "---|" * (len(ROUTES) + 1)]  # fmt: skip
    blob = []
    arms = tuple(a for a in ARMS if any(r["arm"] == a for r in rows))
    for cond in [c for c in CONDITIONS if c in m["conditions"]]:
        for arm in arms:
            lk = [r for r in rows if r["condition"] == cond and r["arm"] == arm and r["reader"] == X.LOOKUP]
            rc = {r["scene"]: r for r in rows if r["condition"] == cond and r["arm"] == arm and r["reader"] == X.RECALL}
            if not lk:
                continue
            scenes_ = [r["scene"] for r in lk]
            sw = {rt: [int(r["route"] == rt) for r in lk] for rt in ROUTES}
            sw["recall_follows_s"] = [rc[s]["switched"] for s in scenes_]
            rr = X.resampled_rates(sw, [r["entity"] for r in lk], n_boot)
            share = {k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in sw.items()}
            used = [rt for rt in ROUTES[:4] if share[rt][0] >= USED_SHARE and share[rt][1] >= USED_LO]
            norm = float(np.median([x["norm"] for x in norms if x["condition"] == cond]))
            blob.append(
                {"condition": cond, "arm": arm, "n": len(lk), "share": share, "used": used, "median_norm": norm}
            )
            lines.append(f"| {cond} | {arm} | {len(lk)} | " + " | ".join(ci(share[rt]) for rt in ROUTES)
                         + f" | {ci(share['recall_follows_s'])} |")  # fmt: skip
    lines += ["", f"Rule (fixed in advance): a route is used iff its share >= {USED_SHARE} with lower CI >= {USED_LO}. "
              "C1: identity = original (both a). Median norm of the change per condition: "
              + ", ".join(f"{b['condition']} {b['median_norm']:.2f}" for b in blob if b["arm"] == "whole") + "."]  # fmt: skip
    extra = extra_losses(rows, m["conditions"], n_boot, norms) if "no_both" in arms or "no_id" in arms else []
    if extra:
        lines += ["", "Extra loss of the switch (Jdep - Rdep, each part against a random part of its own share); "
                  "'both - alf': the union's extra loss minus the pointer directions' (paired resamples).", "",
                  "| condition | reader | part | n | S_whole | Jdep | Rdep | extra loss | median share |",
                  "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for e in extra:
            if e["part"] == "both - alf":
                lines.append(
                    f"| {e['condition']} | {e['reader']} | both - alf | {e['n']} | | | | {ci(e['excess'])} | |"
                )
            else:
                lines.append(f"| {e['condition']} | {e['reader']} | {e['part']} | {e['n']} | {e['S_whole'][0]:.2f} | "
                             f"{ci(e['Jdep'])} | {ci(e['Rdep'])} | {ci(e['excess'])} | {e['share']:.3f} |")  # fmt: skip
    ctrl = ctrl_losses(rows, m["conditions"], n_boot) if "no_alf_jrand" in arms else []
    if ctrl:
        lines += ["", "Switches lost (share of the whole change's switches; no random control subtracted) without the "
                  "pointer directions, without them and J++, and without them and a random part of J++'s share; the "
                  "last row: J++'s union minus the random union (paired resamples).", "",
                  "| condition | reader | removed | n | switches lost |", "|---|---|---|---|---|"]  # fmt: skip
        lines += [f"| {c['condition']} | {c['reader']} | {c['arm']} | {c['n']} | {ci(c['lost'])} |" for c in ctrl]
    (out / "verdict.json").write_text(
        json.dumps({"run": name, "manifest": m, "rows": blob, "extra": extra, "ctrl": ctrl}, indent=1) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name")
    ap.add_argument("--smoke", action="store_true", help="run: C0 on 20 scenes only (the sanity check)")
    ap.add_argument("--layer", type=int, default=None, help="run: a layer other than the one fixed in advance")
    ap.add_argument("--c0-min", type=float, default=None, help="run: a descriptive C0 gate (stop only below this rate)")
    ap.add_argument("--no-pointer", action="store_true", help="run: no pointer-direction arms")
    ap.add_argument("--conditions", default=",".join(CONDITIONS), help="run: the conditions, comma-separated")
    ap.add_argument(
        "--bothoff", action="store_true", help="run: also without the union of J++ and the pointer directions"
    )
    ap.add_argument("--gate", type=float, default=X.GATE, help="run: a lowered, descriptive read-accuracy gate")
    ap.add_argument(
        "--bothoff-ctrl", action="store_true", help="run: also without the pointer and a random J++-size part"
    )
    ap.add_argument("--keeponly", action="store_true", help="run: also arms that add only one part of the change")
    ap.add_argument("--identity", action="store_true", help="run: also the identity-direction arms (D1)")
    ap.add_argument("--alf-from", default=None, help="run: the pointer basis from results/<path>/pcf.npz (P_cf)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
        return
    if a.stage == "run":
        conds = tuple(c for c in a.conditions.split(",") if c)
        assert set(conds) <= set(CONDITIONS), f"conditions {conds}"
        stage_run(
            a.name,
            a.smoke,
            a.layer,
            a.c0_min,
            not a.no_pointer,
            conds,
            a.bothoff,
            a.gate,
            a.bothoff_ctrl,
            a.keeponly,
            a.identity,
            a.alf_from,
        )
    if not a.smoke:
        stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
