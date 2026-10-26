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
Batch 45 (Dan 26 Oct ~18:30; designs and rules in jobs/c3/batch45.yaml, fixed in advance):
--prepend (45a, C2 only): one sentence before O's and S's first sentence: V0 none (the control, a rerun); V1 a new
  person's pick of the item whose locker is first in O; V2 the same person's pick of another locker item (seeded); V3 of
  an item with no locker in the scene; V4 a neutral filler (x8_write.FILLERS of --filler-tokens tokens). A base scene is
  kept only if every variant encodes (the bridge one token at one index shared by O and S) and is eligible in every
  variant that passed its gate, so the variants are paired. Arms: whole, keep_alf, keep_alf_rand, no_alf, no_alf_rand.
  beta.jsonl: the code's shift per variant vs V0 (as x8_write order: beta = <U U^T (h_v - h_V0), mu_j+1 - mu_j> /
  ||mu_j+1 - mu_j||^2 at O's bridge word, j its locker slot). Verdict: 45a's rule (first_locker_rule).
--identity-controls (45e a, with --identity): two controls at idout's share of each scene's change: wrong pairs (class-mean
  differences of entity pairs sharing no entity with the scene's pair, orthonormalised one at a time in a seeded order)
  and the layer's top PCA directions (x0_parts.pca_dictionary, equal_share); each removed alone and in the union with
  the scene's J++ atoms and the pointer directions, each against a random part of its own share. Verdict: 45e's rule
  per model (identity_control_flags); idctrl-summary: over the models (identity_specific).
--rendering nochat (45i): X0's prompt without the chat template (thinking off), read by X0's digit rule (amendment 3).
--sealed: no verdict after the run (batch 45: no result is opened before Dan's predictions are committed).
examples (CPU): 10 random items (seed 0), each reader's prompt as the model reads it with the patch position marked
  ⟦...⟧, the source prompt, and every arm's answer.

uv run python scripts/x6_routes.py plan                                   # tokenizer only
uv run python scripts/x6_routes.py run --name x6_routes_27b               # GPU (C0 check, then C1 / C2), verdict
uv run python scripts/x6_routes.py plan --prepend V0,V1,V2,V3,V4          # 45a's prompts, tokenizer only
uv run python scripts/x6_routes.py run --name x6_routes_x45a_27b --conditions C2 --prepend V0,V1,V2,V3,V4 --sealed
uv run python scripts/x6_routes.py examples --name x6_routes_x45a_27b     # CPU
uv run python scripts/x6_routes.py idctrl-summary --names qwen35_9b_x6_routes_x45e,x6_routes_x45e_27b,muse30b_x6_routes_x45e
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
        "no_jppalfidout_rand", "keep_id", "keep_id_rand", "no_idsub",
        # --identity-controls (45e a): the wrong-pair and PCA controls at idout's share, alone and with J++ + the pointer
        "no_wrong", "no_wrong_rand", "no_pca", "no_pca_rand", "no_jppalfwrong", "no_jppalfwrong_rand", "no_jppalfpca",
        "no_jppalfpca_rand")  # fmt: skip
# --bothoff-ctrl: switches lost (Jdep) without the pointer directions, without them and J++, without them and a random
# part of J++'s share; the question is the second minus the third (Dan's Q36.1)
CTRL = (("alf", "no_alf"), ("alf + J++", "no_both"), ("alf + random (J++ share)", "no_alf_jrand"))
PARTS = (("jpp", "no_jpp", "no_jpp_rand"), ("alf", "no_alf", "no_alf_rand"), ("both", "no_both", "no_both_rand"),
         ("id", "no_id", "no_id_rand"), ("idout", "no_idout", "no_idout_rand"),
         ("alf+idout", "no_alfidout", "no_alfidout_rand"), ("jpp+alf+idout", "no_jppalfidout", "no_jppalfidout_rand"),
         ("wrong", "no_wrong", "no_wrong_rand"), ("pca", "no_pca", "no_pca_rand"),
         ("jpp+alf+wrong", "no_jppalfwrong", "no_jppalfwrong_rand"), ("jpp+alf+pca", "no_jppalfpca", "no_jppalfpca_rand"))  # fmt: skip
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
# batch 45 (jobs/c3/batch45.yaml, fixed in advance)
RENDERINGS = ("chat", "nochat")  # 45i: nochat = X0's prompt without the chat template, read by X0's digit rule
PREPEND = ("V0", "V1", "V2", "V3", "V4")  # 45a's variants
PREPEND_ARMS = ("whole", "keep_alf", "keep_alf_rand", "no_alf", "no_alf_rand")
PREPEND_SEED, WRONG_SEED, EXAMPLES_SEED, N_EXAMPLES = 4501, 4505, 0, 10
FIRST_CUT, FIRST_NEAR = 0.5, 0.10  # 45a: "at most half of V0" / "within 0.10 of V0"
IDC_LEFT, IDC_CUT, IDC_MODELS = 0.5, 0.15, 2  # 45e: at most half; at least 0.15 more; on at least 2 of 3 models
EPS = 1e-9  # thresholds on shares of counts: a share exactly at the bar counts as at the bar
PICK = re.compile(r"(\w+) picked the (\w+)\.")
MARK = "⟦{}⟧"  # the patch position in an example's prompt


def one_token(tok, word: str) -> bool:
    from scripts import suite_v1 as S

    return len(S.ids(tok, " " + word)) == 1


def context(lockers: list[tuple[str, int]], picks: list[tuple[str, str]]) -> str:
    return " ".join([f"The locker of the {x} is {d}." for x, d in lockers] + [f"{p} picked the {x}." for p, x in picks])


def pools(tok) -> tuple[dict[str, int], list[str], list[str]]:
    """The generator's pools: the animals' legs, the one-token animals with 0-9 legs and the one-token people."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    legs = T.DOMAINS["animals"].values
    animals = sorted(a for a in legs if one_token(tok, a) and 0 <= legs[a] <= 9)
    people = sorted(p for p in S.PEOPLE if one_token(tok, p))
    return legs, animals, people


def scenes(tok, n: int, seed: int = SEED, rendering: str = "chat") -> tuple[list[dict], collections.Counter]:
    """n scenes per condition: O, S and the answers each route predicts; drops counted by reason."""
    legs, animals, people = pools(tok)
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
            case, why = encode(tok, o, s, asked, A, bridge, legs, expect, cond, f"{cond}-{i:04d}", rendering)
            if case is None:
                dropped[f"{cond}: {why}"] += 1
            elif sum(c_["condition"] == cond for c_ in out) < n:
                out.append(case)
    return out, dropped


def encode(
    tok,
    o: str,
    s: str,
    asked: str,
    a_item: str,
    bridge: str,
    legs: dict,
    expect: dict,
    cond: str,
    scene: str,
    rendering: str = "chat",
):
    """Both readers' O and S prompts; the bridge one token at the same index in O and S (asserted). rendering: chat
    (tasks_v2's prompt) or nochat (X0's prompt without the chat template, 45i)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    readers, pos = {}, None
    s_answer = expect["switch"] if "switch" in expect else expect["value"]
    for w, q, ans in ((X.LOOKUP, LOOKUP_Q, (expect["original"], s_answer)),
                      (X.RECALL, RECALL_Q, (legs[a_item], legs[bridge]))):  # fmt: skip
        ids, at = {}, {}
        for v, ctx, x in (("org", o, a_item), ("alt", s, bridge)):
            item = {"format": "prose", "kind": "digit", "context": ctx, "question": q.format(p=asked)}
            text = X.render(tok, item, rendering, ctx)  # chat: tasks_v2.render(tok, item), as before
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
    return {"scene": scene, "condition": cond, "rendering": rendering, "domain": "animals", "bridge": a_item,
            "cf_bridge": bridge, "context": o, "cf_context": s, "pos": pos, "space": S.ids(tok, " "),
            "expect": {k: int(v) for k, v in expect.items()}, "route_tokens": routes, "readers": readers}, ""  # fmt: skip


def classify(top: int, case: dict) -> str:
    """The lookup answer's route (C1: identity = original, reported as identity)."""
    hit = [r for r in ("identity", "position", "value", "original") if case["route_tokens"].get(r) == top]
    return hit[0] if hit else "other"


def asked_of(case: dict) -> str:
    """The asked person of a routes case (from the lookup's question, "Which locker belongs to <p>'s pick?")."""
    return case["readers"][X.LOOKUP]["question"].split("'s pick")[0].rsplit(" ", 1)[-1]


def window_fillers(tok, lo: int, hi: int) -> list[str]:
    """x8_write's neutral fillers (batch 44 B) whose own token count, as inserted mid-prompt, is within [lo, hi]."""
    from scripts import x8_write as W

    n_tok = W.filler_lengths(tok)
    fillers = [f for f in W.FILLERS if lo <= n_tok[f] <= hi]
    assert fillers, f"no filler of {lo}-{hi} tokens for this tokenizer: {sorted(n_tok.values())}"
    return fillers


def prepend_sentences(
    case: dict, animals: list[str], people: list[str], fillers: list[str], rng: random.Random
) -> dict[str, str]:
    """45a's sentence per variant for one base C2 scene (V0: none). V1-V3: one new person (not in the scene; no name a
    suffix of a scene person's, so the asked pick sentence is found once) picks the item whose locker is first in O
    (V1), another locker item (V2), an item with no locker in the scene (V3); V4: a neutral filler. The draws come
    from rng alone, so the base scenes are the routes test's."""
    from scripts import x8_write as W

    named = {p for p, _ in PICK.findall(case["context"])}
    items = [x for x, _ in W.slots_of(case["context"])]
    new = rng.choice([p for p in people if p not in named and not any(p.endswith(q) or q.endswith(p) for q in named)])
    other = rng.choice(items[1:])
    free = rng.choice([a for a in animals if a not in items])
    return {"V0": "", "V1": f"{new} picked the {items[0]}.", "V2": f"{new} picked the {other}.",
            "V3": f"{new} picked the {free}.", "V4": rng.choice(fillers)}  # fmt: skip


def prepend_cases(
    tok, base: list[dict], variants: tuple[str, ...], fillers: list[str], seed: int = PREPEND_SEED
) -> tuple[list[dict], collections.Counter]:
    """45a: per base C2 case, one case per variant: the variant's sentence before O's and S's first sentence, everything
    else as the base. A base scene whose bridge is not one token at one index shared by O and S in some variant is
    dropped in every variant (counted by variant and reason), so the variants stay paired. Each case records its
    variant, base scene, the sentence and the pointer's move (x8_write.pointer_move: the O bridge's locker slot -> the S
    bridge's)."""
    from scripts import x8_write as W

    legs, animals, people = pools(tok)
    out, dropped = [], collections.Counter()
    for c in base:
        assert c["condition"] == "C2", f"--prepend is a C2 design: {c['scene']}"
        sent = prepend_sentences(c, animals, people, fillers, random.Random(f"{seed}|{c['scene']}"))
        mine = []
        for v in variants:
            pre = sent[v] + " " if sent[v] else ""
            case, why = encode(tok, pre + c["context"], pre + c["cf_context"], asked_of(c), c["bridge"], c["cf_bridge"],
                               legs, c["expect"], "C2", f"{c['scene']}-{v}", c["rendering"])  # fmt: skip
            if case is None:
                dropped[f"C2 {v}: {why}"] += 1
                break
            case.update(
                {"variant": v, "base_scene": c["scene"], "prepended": sent[v], "move": list(W.pointer_move(case))}
            )
            mine.append(case)
        else:
            out += mine
    return out, dropped


def stage_plan(
    prepend: tuple[str, ...] = (), rendering: str = "chat", filler_tokens: tuple[int, int] = (10, 12)
) -> None:
    from scripts import statement_positions as SP

    tok = SP.load_tokenizer()
    cases, dropped = scenes(tok, N_GEN, rendering=rendering)
    if prepend:
        fillers = window_fillers(tok, *filler_tokens)
        cases, more = prepend_cases(tok, [c for c in cases if c["condition"] == "C2"], prepend, fillers)
        moves = collections.Counter(tuple(c["move"]) for c in cases if c["variant"] == prepend[0])
        print(json.dumps({"cases": collections.Counter(c["variant"] for c in cases), "dropped": dropped + more,
                          "fillers": fillers, "moves": {f"{j}->{k}": v for (j, k), v in sorted(moves.items())}},
                         indent=1))  # fmt: skip
        base = cases[0]["base_scene"]
        for c in (c for c in cases if c["base_scene"] == base):
            print(c["variant"], "O:", c["context"], "\n   S:", c["cf_context"], "\n   move", c["move"])
        return
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


def wrong_pair_basis(means: dict, pair: tuple[str, str], x, target: float, rng: random.Random):
    """45e's wrong-pair control for one scene (x: its change [d]): the class-mean differences mu_b - mu_a of entity
    pairs that share no entity with the scene's pair, in rng's order, orthonormalised one at a time (a difference already
    in the span is skipped), added until the span holds `target` of ||x||^2; the number of directions is the one whose
    share is closest to the target (ties: fewer), as random_k and x0_parts.equal_share match shares. Pairs that share an
    entity are left out because they can hold the scene's own identity direction exactly: (mu_c - mu_a) - (mu_c - mu_b)
    = mu_b - mu_a. Returns (orthonormal basis [d, k] in x's dtype, its share of ||x||^2)."""
    import torch

    others = sorted(e for e in means if e not in pair)
    cand = [(a, b) for i, a in enumerate(others) for b in others[i + 1 :]]
    rng.shuffle(cand)
    xd = x.double()
    total = max(float(xd @ xd), 1e-30)
    cols, cum = [], [0.0]
    for a, b in cand:
        if cum[-1] >= target:
            break
        v = (means[b] - means[a]).double()
        size = float(v.norm())
        if cols:
            q = torch.stack(cols, 1)
            for _ in range(2):  # Gram-Schmidt twice keeps the columns orthonormal in floating point
                v = v - q @ (q.T @ v)
        if float(v.norm()) <= 1e-6 * size:
            continue
        cols.append(v / v.norm())
        cum.append(cum[-1] + float(cols[-1] @ xd) ** 2 / total)
    k = min(range(len(cum)), key=lambda i: abs(cum[i] - target))
    basis = torch.stack(cols[:k], 1).to(x.dtype) if k else x.new_zeros(x.shape[0], 0)
    return basis, cum[k]


def code_shift(dh, alf, step) -> dict:
    """x8_write order's code shift: d = U U^T dh (U: the pointer directions, orthonormal columns), beta = <d, step> /
    ||step||^2 (step: mu_j' - mu_j, the class means behind U)."""
    d = (dh @ alf) @ alf.T
    return {"beta": float(d @ step / (step @ step)), "norm_d": float(d.norm()), "norm_step": float(step.norm())}


def prepend_betas(chosen: list[dict], h_org: list, alf, mu: dict) -> list[dict]:
    """45a: per --prepend case other than V0, the code's shift of O's bridge-word state against the same base scene's V0
    state, in units of mu_j+1 - mu_j (j: the O bridge's locker slot; as x8_write order's B1). [] without V0."""
    at = {(c["base_scene"], c["variant"]): i for i, c in enumerate(chosen)}
    out = []
    for i, c in enumerate(chosen):
        j, ref = c["move"][0], at.get((c["base_scene"], "V0"))
        if c["variant"] != "V0" and ref is not None and j + 1 in mu:
            out.append({"scene": c["scene"], "base_scene": c["base_scene"], "entity": c["bridge"], "variant": c["variant"],
                        "j": j, "move": c["move"], **code_shift(h_org[i] - h_org[ref], alf, mu[j + 1] - mu[j])})  # fmt: skip
    return out


def control_parts(
    x,
    idout,
    means: dict,
    chosen: list[dict],
    jdic,
    atoms,
    alf,
    pca,
    seed: int = WRONG_SEED,
    domain_of: dict[str, str] | None = None,
):
    """45e (a): per scene (row of x), the two controls at the share of x that identity outside J++ holds (idout: that
    part, [n, d]): the wrong-pair part (wrong_pair_basis, seeded per scene) and the PCA part (x0_parts.equal_share over
    pca's unit rows), each also in the union with the scene's J++ atoms (atoms[i]: rows of jdic) and the pointer
    directions alf (span_part, least-squares projection). With domain_of (entity -> domain), the wrong pairs come from
    the bridge's own domain only (Dan 26 Oct ~21:20: never mixed; a short pool shows in the achieved share). Returns
    ({part: [n, d]}, {"k_wrong", "k_pca", "n_wrong_pool": per scene})."""
    import torch

    from scripts import x0_parts as XP

    at_share = idout.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    pools = [{e: v for e, v in means.items() if domain_of is None or domain_of.get(e) == domain_of[c["bridge"]]}
             for c in chosen]  # fmt: skip
    wrong = [wrong_pair_basis(pools[i], (c["bridge"], c["cf_bridge"]), x[i], float(at_share[i]),
                              random.Random(f"{seed}|{c['scene']}"))[0] for i, c in enumerate(chosen)]  # fmt: skip
    pca_part, k_pca = XP.equal_share(pca, x, at_share)
    top = (x @ pca.T).abs().argsort(dim=-1, descending=True)  # equal_share's atoms: the first k_pca of these
    jcols = [torch.cat([jdic[atoms[i]].T, alf], 1) for i in range(len(chosen))]
    parts = {"wrong": torch.stack([q @ (q.T @ x[i]) for i, q in enumerate(wrong)]), "pca": pca_part,
             "jpp+alf+wrong": span_part(x, [torch.cat([jcols[i], q], 1) for i, q in enumerate(wrong)]),
             "jpp+alf+pca": span_part(x, [torch.cat([jcols[i], pca[top[i, : int(k_pca[i])]].T], 1)
                                          for i in range(len(chosen))])}  # fmt: skip
    n_pool = [len(set(p) - {c["bridge"], c["cf_bridge"]}) for p, c in zip(pools, chosen, strict=True)]
    return parts, {
        "k_wrong": [int(q.shape[1]) for q in wrong],
        "k_pca": [int(k) for k in k_pca],
        "n_wrong_pool": n_pool,
    }


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
    prepend: tuple[str, ...] = (),
    filler_tokens: tuple[int, int] = (10, 12),
    identity_controls: bool = False,
    rendering: str = "chat",
    sealed: bool = False,
) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_massmean as MM
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert rendering in RENDERINGS, rendering
    assert set(prepend) <= set(PREPEND), f"--prepend {prepend}: of {PREPEND}"
    assert len(set(prepend)) == len(prepend), f"--prepend {prepend}: a variant twice"
    assert not prepend or (conds == ("C2",) and pointer and not (bothoff or identity or alf_from or smoke)), (
        "--prepend (45a): --conditions C2 only, the fresh-scene pointer directions, no other arm set"
    )
    assert identity or not identity_controls, "--identity-controls needs --identity"
    if rendering != "chat":  # 45i: X0's digit read (amendment 3), the read X0's no-template runs use
        X.READ = "digit"
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
         "seeds": {"scenes": SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED},
         "rendering": rendering, "read": "chat (the top token after a space)" if rendering == "chat" else f"X0 {X.READ}",
         "prepend": list(prepend), "identity_controls": identity_controls, "sealed": sealed}  # fmt: skip
    if prepend:
        m.update({"prepend_seed": PREPEND_SEED, "filler_tokens": list(filler_tokens), "batch45": "45a",
                  "arms": list(PREPEND_ARMS)})  # fmt: skip
    if identity_controls:
        m.update({"wrong_seed": WRONG_SEED, "batch45": "45e",
                  "wrong_pairs": "class-mean differences of entity pairs from the bridge's own domain (Dan 26 Oct ~21:20) "
                                 "sharing no entity with the scene's pair"})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    cases, dropped = scenes(tok, N_GEN, rendering=rendering)
    cases = [c for c in cases if c["condition"] in conds]
    if prepend:  # 45a: every base C2 scene in every variant; the variants' fillers recorded before any forward pass
        m["fillers"] = window_fillers(tok, *filler_tokens)
        cases, more = prepend_cases(tok, cases, prepend, m["fillers"])
        dropped.update(more)
        (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp = X.competence(model, cases, digits, ws)
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    gate, ok_by = {}, {}
    groups = ({v: [c for c in cases if c["variant"] == v] for v in prepend} if prepend else
              {cond: [c for c in cases if c["condition"] == cond] for cond in conds})  # fmt: skip
    for g, mine in groups.items():
        acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in mine])) for w in X.READERS}
        ok = [c for c in mine if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                     for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
        gate[g] = {"cases": len(mine), "org_read_accuracy": acc, "pass": all(a >= gate_min for a in acc.values()),
                   "eligible": len(ok)}  # fmt: skip
        ok_by[g] = ok
    if prepend:  # paired: the first n base scenes eligible in every variant that passed its gate
        passed = [v for v in prepend if gate[v]["pass"]]
        both = set.intersection(*({c["base_scene"] for c in ok_by[v]} for v in passed)) if passed else set()
        keep = set(list(dict.fromkeys(c["base_scene"] for c in cases if c["base_scene"] in both))[:n])
        gate["joint"] = {"variants": passed, "eligible_in_all": len(both), "chosen": len(keep)}
        chosen = [c for c in cases if c["variant"] in passed and c["base_scene"] in keep]
    else:
        chosen = [c for cond in conds if gate[cond]["pass"] for c in ok_by[cond][:n]]
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    (out / "gate.json").write_text(json.dumps({"dropped": dropped, "gate": gate}, indent=2) + "\n")
    if not chosen:
        raise SystemExit("no condition passed the gate fixed in advance (or none had eligible items); see gate.json")
    if identity:  # D1: mu_alt - mu_org needs both entities' class means (the probe's entities); other scenes dropped
        ent_means = MM.entity_means(STATES[target])
        keep = [c for c in chosen if c["bridge"] in ent_means and c["cf_bridge"] in ent_means]
        m["identity_dropped"] = {cond: sum(c["condition"] == cond for c in chosen if c not in keep) for cond in conds}
        chosen = keep
    sub = MM.subspaces(STATES[target])[0] if pointer else {}
    if alf_from:  # P_cf (x7_pcf, batch 43) in place of the mass-mean pointer directions
        sub["Alf"] = np.load(pins.RESULTS_DIR / alf_from / "pcf.npz")["P"]
    alf = torch.tensor(sub["Alf"], dtype=torch.float32, device="cuda") if pointer else None
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    rows, norms, betas = [], [], []
    kcount: dict[str, list[int]] = {}  # 45e: the controls' directions per scene
    with torch.no_grad():
        deltas, h_org = [], []
        for c in progress(chosen, "Δ at the bridge word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                 for v in ("org", "alt")}  # fmt: skip
            deltas.append((h["alt"] - h["org"]).float())
            if prepend:
                h_org.append(h["org"].float())
        x = torch.stack(deltas)
        if prepend:  # 45a: the code's shift vs V0 at O's bridge word
            assert alf is not None
            mu = {k: torch.tensor(v, dtype=torch.float32, device="cuda")
                  for k, v in MM.pointer_means(STATES[target]).items()}  # fmt: skip
            betas = prepend_betas(chosen, h_org, alf, mu)
        jpp = X.fit(jdic, x, X.K_MAIN, "signed")
        ptr = (x @ alf) @ alf.T if alf is not None else torch.zeros_like(x)  # alf is None iff not pointer
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
        if keeponly or prepend:
            arms.update({"keep_alf": ptr, "keep_alf_rand": SP.random_subspace_part(x, sh["alf"], basis),
                         "keep_jpp": jpp, "keep_jpp_rand": SP.random_subspace_part(x, sh["jpp"], basis)})  # fmt: skip
        if prepend:  # 45a's arms only
            arms = {a: arms[a] for a in PREPEND_ARMS}
        if identity:  # D1: the rank-1 identity direction mu_alt - mu_org, and it outside the scene's J++ atoms
            assert alf is not None
            means = {e: torch.tensor(v, dtype=torch.float32, device="cuda") for e, v in ent_means.items()}
            u, u_out, atoms = identity_dirs(means, [(c["bridge"], c["cf_bridge"]) for c in chosen], jdic, x, X.K_MAIN)
            idsub = torch.tensor(sub["Id"], dtype=torch.float32, device="cuda")
            m["id_rank"] = int(idsub.shape[1])
            parts = {"id": rank1_part(x, u), "idout": rank1_part(x, u_out),
                     "alf+idout": span_part(x, [torch.cat([alf, u_out[i : i + 1].T], 1) for i in range(len(chosen))]),
                     "jpp+alf+idout": span_part(x, [torch.cat([jdic[atoms[i]].T, alf, u_out[i : i + 1].T], 1)
                                                    for i in range(len(chosen))]),
                     "idsub": (x @ idsub) @ idsub.T}  # fmt: skip
            removed = [("id", "id"), ("idout", "idout"), ("alf+idout", "alfidout"), ("jpp+alf+idout", "jppalfidout")]
            if identity_controls:  # 45e (a): the wrong-pair and PCA controls at idout's share, per scene
                from scripts import x0_parts as XP

                pca, m["pca"] = XP.pca_dictionary(model, layer)
                assert isinstance(pca, torch.Tensor)
                more, kcount = control_parts(x, parts["idout"], means, chosen, jdic, atoms, alf, pca,
                                             domain_of=MM.entity_domains(STATES[target]))  # fmt: skip
                parts.update(more)
                removed += [
                    ("wrong", "wrong"),
                    ("pca", "pca"),
                    ("jpp+alf+wrong", "jppalfwrong"),
                    ("jpp+alf+pca", "jppalfpca"),
                ]
            for k, v in parts.items():
                sh[k] = v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            for k, name in removed:
                arms[f"no_{name}"] = x - parts[k]
                arms[f"no_{name}_rand"] = x - SP.random_subspace_part(x, sh[k], basis)
            arms.update({"keep_id": parts["id"], "keep_id_rand": SP.random_subspace_part(x, sh["id"], basis),
                         "no_idsub": x - parts["idsub"]})  # fmt: skip
        for i, c in enumerate(progress(chosen, f"reads at layer {layer} (case)")):
            pv = {"variant": c["variant"], "base_scene": c["base_scene"], "move": c["move"]} if prepend else {}
            norms.append({"scene": c["scene"], "condition": c["condition"], **pv, "norm": round(float(x[i].norm()), 4),
                          **{f"share_{k}": round(float(v[i]), 5) for k, v in sh.items()},
                          **{k: v[i] for k, v in kcount.items()}})  # fmt: skip
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in arms]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, c["rendering"], c["space"], ws)
                for a, lg in zip(("none", *arms), logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({"scene": c["scene"], "condition": c["condition"], **pv, "entity": c["bridge"],
                                 "reader": w, "arm": a, "top": top, "route": classify(top, c) if w == X.LOOKUP else None,
                                 **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    if prepend:
        X.write_jsonl(out / "beta.jsonl", betas)
        m["items_per_variant"] = {v: sum(c["variant"] == v for c in chosen) for v in prepend}
    m["items"] = {cond: sum(c["condition"] == cond for c in chosen) for cond in conds}
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    if "C0" in conds:
        c0 = [r["switched"] for r in rows if r["condition"] == "C0" and r["reader"] == X.LOOKUP and r["arm"] == "whole"]
        rate = float(np.mean(c0)) if c0 else float("nan")
        assert c0_min is not None or ref is not None, "no C0 reference for this target: pass --c0-min"
        ok = rate >= c0_min if c0_min is not None else ref is not None and abs(rate - ref) <= C0_TOL
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


def first_locker_rule(rows: list[dict], beta: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """45a (jobs/c3/batch45.yaml, fixed in advance) on a --prepend run's lookup rows. Moves to or from the first locker:
    the O bridge's locker slot -> the S bridge's involves slot 0; the base scenes every tested variant has (paired).
    pos[v]: the position share with only the pointer part (keep_alf). V1-V3 each "cut" it if pos[v] <= 0.5 pos[V0] and
    the paired cluster-bootstrap CI of pos[V0] - pos[v] excludes 0 (lower bound > 0); "near" if |pos[v] - pos[V0]| <=
    0.10. Verdict: "First locker stated before any item" if V1, V2 and V3 cut and V4 does not; else "Order of lockers,
    picks ignored" if V1, V2 and V3 are near; else "mixed" (both_rules_hold flags a run where both conditions hold: the
    first is reported, in the rule's order); "not tested" if a variant missed its gate. Beside it (descriptive): every
    arm's position share per variant on the first-locker moves and on all moves, the position lost without the pointer
    beyond its random part (no_alf_rand - no_alf, paired), and the code's shift beta vs V0, overall and per slot j."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP and r.get("variant")]
    got = {(r["base_scene"], r["variant"], r["arm"]): int(r["route"] == "position") for r in lk}
    ent = {r["base_scene"]: r["entity"] for r in lk}
    first = {r["base_scene"]: 0 in r["move"] for r in lk}
    tested = [v for v in PREPEND if any(r["variant"] == v for r in lk)]
    out: dict = {"tested": tested, "missing": [v for v in PREPEND if v not in tested], "moves": {}}
    common = set.intersection(*({b for b, v, a in got if v == t and a == "whole"} for t in tested)) if tested else set()
    for label, only_first in (("first_locker", True), ("all", False)):
        bases = sorted(b for b in common if first[b] or not only_first)
        if not bases:
            out["moves"][label] = {"n": 0}
            continue
        sw = {f"{v}|{a}": [got[(b, v, a)] for b in bases] for v in tested for a in PREPEND_ARMS}
        rr = X.resampled_rates(sw, [ent[b] for b in bases], n_boot)
        share = {k: [float(np.mean(s)), *X.interval(rr[k])] for k, s in sw.items()}

        def diff(a: str, b: str, share=share, rr=rr) -> list[float]:
            return [share[a][0] - share[b][0], *X.interval(rr[a] - rr[b])]

        out["moves"][label] = {
            "n": len(bases),
            "entities": len({ent[b] for b in bases}),
            "share": share,
            "pos_lost_beyond_rand": {v: diff(f"{v}|no_alf_rand", f"{v}|no_alf") for v in tested},
            "keep_alf_cut_vs_V0": {v: diff("V0|keep_alf", f"{v}|keep_alf") for v in tested if v != "V0"}
            if "V0" in tested
            else {},
        }
    out["beta"] = {}
    for v in sorted({b["variant"] for b in beta}):
        for j in (None, 0, 1, 2):
            mine = [b for b in beta if b["variant"] == v and (j is None or b["j"] == j)]
            if mine:
                rr = X.resampled_rates({"beta": [b["beta"] for b in mine]}, [b["entity"] for b in mine], n_boot)
                out["beta"][f"{v}|{'all' if j is None else j}"] = {
                    "n": len(mine),
                    "beta": [float(np.mean([b["beta"] for b in mine])), *X.interval(rr["beta"])],
                    "norm_ratio_median": float(np.median([b["norm_d"] / b["norm_step"] for b in mine])),
                }
    fl = out["moves"]["first_locker"]
    if out["missing"] or not fl["n"]:
        out["verdict"] = "not tested (" + (f"gate missed: {', '.join(out['missing'])}" if out["missing"] else
                                           "no move to or from the first locker") + ")"  # fmt: skip
        return out
    pos = {v: fl["share"][f"{v}|keep_alf"][0] for v in PREPEND}
    cut = {v: pos[v] <= FIRST_CUT * pos["V0"] + EPS and fl["keep_alf_cut_vs_V0"][v][1] > 0 for v in PREPEND[1:]}
    near = {v: abs(pos[v] - pos["V0"]) <= FIRST_NEAR + EPS for v in PREPEND[1:]}
    first_locker = cut["V1"] and cut["V2"] and cut["V3"] and not cut["V4"]
    order = near["V1"] and near["V2"] and near["V3"]
    out.update({"pos_keep_alf": pos, "cut": cut, "near": near, "first_locker": first_locker,
                "order_of_lockers": order, "both_rules_hold": first_locker and order})  # fmt: skip
    out["verdict"] = ("First locker stated before any item" if first_locker else
                      "Order of lockers, picks ignored" if order else "mixed")  # fmt: skip
    return out


def identity_control_flags(rows: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """45e (jobs/c3/batch45.yaml, fixed in advance), one model, the lookup. (i) C0: the share of the whole change's
    switches still switching without J++ + the pointer + identity outside J++ (no_jppalfidout) is at most half of that
    without J++ + the pointer + the wrong-pair control (no_jppalfwrong). (ii) C2: identity outside J++ removed alone cuts
    the identity answers at least 0.15 more than the wrong-pair control removed alone: identity share(no_wrong) -
    identity share(no_idout) >= 0.15. Point estimates decide; paired cluster-bootstrap CIs beside them; the PCA control
    and the union-arm version of (ii) are descriptive."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP]
    out: dict = {"c0": None, "c2": None}

    def paired(cond: str, arms: tuple[str, ...], key) -> tuple[list[str], dict, dict] | None:
        by = {a: {r["scene"]: r for r in lk if r["condition"] == cond and r["arm"] == a} for a in arms}
        scenes_ = sorted(set.intersection(*(set(v) for v in by.values())))
        if not scenes_:
            return None
        sw = {a: [key(by[a][s]) for s in scenes_] for a in arms}
        return scenes_, sw, X.resampled_rates(sw, [by["whole"][s]["entity"] for s in scenes_], n_boot)

    got = paired("C0", ("whole", "no_jppalfidout", "no_jppalfwrong", "no_jppalfpca"), lambda r: int(r["switched"]))
    if got:
        scenes_, sw, rr = got
        s = {a: float(np.mean(v)) for a, v in sw.items()}
        left = {a: float(1 - X.dependence(s["whole"], s[a])) for a in sw if a != "whole"}
        left_r = {a: 1 - X.dependence(rr["whole"], rr[a]) for a in left}
        out["c0"] = {"n": len(scenes_), "S_whole": s["whole"],
                     "left": {a: [left[a], *X.interval(left_r[a])] for a in left},
                     "idout_minus_half_wrong": [left["no_jppalfidout"] - IDC_LEFT * left["no_jppalfwrong"],
                                                *X.interval(left_r["no_jppalfidout"] - IDC_LEFT * left_r["no_jppalfwrong"])]}  # fmt: skip
    arms2 = ("whole", "no_idout", "no_wrong", "no_pca", "no_idout_rand", "no_wrong_rand", "no_pca_rand",
             "no_jppalfidout", "no_jppalfwrong", "no_jppalfpca")  # fmt: skip
    got = paired("C2", arms2, lambda r: int(r["route"] == "identity"))
    if got:
        scenes_, sw, rr = got
        share = {a: [float(np.mean(v)), *X.interval(rr[a])] for a, v in sw.items()}

        def more_cut(a: str, b: str) -> list[float]:  # how much more a cuts the identity share than b does
            return [share[b][0] - share[a][0], *X.interval(rr[b] - rr[a])]

        out["c2"] = {"n": len(scenes_), "identity_share": share,
                     "idout_vs_wrong": more_cut("no_idout", "no_wrong"), "idout_vs_pca": more_cut("no_idout", "no_pca"),
                     "union_idout_vs_wrong": more_cut("no_jppalfidout", "no_jppalfwrong")}  # fmt: skip
    out["holds_i"] = bool(out["c0"] and out["c0"]["left"]["no_jppalfidout"][0]
                          <= IDC_LEFT * out["c0"]["left"]["no_jppalfwrong"][0] + EPS)  # fmt: skip
    out["holds_ii"] = bool(out["c2"] and out["c2"]["idout_vs_wrong"][0] >= IDC_CUT - EPS)
    out["both"] = out["holds_i"] and out["holds_ii"]
    out["tested"] = out["c0"] is not None and out["c2"] is not None
    return out


def wrong_share_report(norms: list[dict], short: float = 0.9) -> dict:
    """45e: how close the wrong-pair control came to identity outside J++'s share, per condition: the median of
    share_wrong / share_idout, the scenes whose control holds less than `short` of the target (a same-domain pool too
    small to reach it: reported, not mixed with other domains; Dan 26 Oct ~21:20) and the smallest pool."""
    out = {}
    for cond in sorted({r["condition"] for r in norms if "share_wrong" in r}):
        mine = [r for r in norms if r["condition"] == cond and "share_wrong" in r]
        ratio = [r["share_wrong"] / r["share_idout"] for r in mine if r["share_idout"] > 0]
        out[cond] = {"n": len(mine), "median_ratio": float(np.median(ratio)) if ratio else float("nan"),
                     "short": sum(v < short for v in ratio),
                     "min_pool": min((r["n_wrong_pool"] for r in mine if "n_wrong_pool" in r), default=None)}  # fmt: skip
    return out


def identity_specific(flags: dict[str, dict]) -> dict:
    """45e's rule over the models (model -> identity_control_flags): identity outside J++ is specific if (i) and (ii)
    both hold on at least 2 of the 3 models."""
    held = [k for k, f in flags.items() if f["both"]]
    return {"models": list(flags), "held_on": held, "untested": [k for k, f in flags.items() if not f["tested"]],
            "specific": len(held) >= IDC_MODELS,
            "verdict": "identity outside J++ is specific" if len(held) >= IDC_MODELS else "not shown specific"}  # fmt: skip


def never_value(rows: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """45i (jobs/c3/batch45.yaml, fixed in advance) on a no-template run: "never the value" holds if the lookup's value
    share under the whole change in C2 is 0; the identity and position shares beside it, and the value share under
    every arm (descriptive)."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP and r["condition"] == "C2"]
    per = {}
    for arm in dict.fromkeys(r["arm"] for r in lk):
        mine = [r for r in lk if r["arm"] == arm]
        sw = {rt: [int(r["route"] == rt) for r in mine] for rt in ("identity", "position", "value")}
        rr = X.resampled_rates(sw, [r["entity"] for r in mine], n_boot)
        per[arm] = {"n": len(mine), "value_count": sum(sw["value"]),
                    **{rt: [float(np.mean(v)), *X.interval(rr[rt])] for rt, v in sw.items()}}  # fmt: skip
    whole = per.get("whole")
    return {"arms": per, "holds": bool(whole and whole["n"] and whole["value_count"] == 0),
            "value_zero_in_every_arm": bool(per) and all(p["value_count"] == 0 for p in per.values())}  # fmt: skip


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
    variants = m.get("prepend") or [None]  # 45a: one block per prepended sentence
    for cond in [c for c in CONDITIONS if c in m["conditions"]]:
        for var in variants:
            mine = [r for r in rows if r["condition"] == cond and r.get("variant") == var]
            label, tag = (cond, {}) if var is None else (f"{cond} {var}", {"variant": var})
            for arm in arms:
                lk = [r for r in mine if r["arm"] == arm and r["reader"] == X.LOOKUP]
                rc = {r["scene"]: r for r in mine if r["arm"] == arm and r["reader"] == X.RECALL}
                if not lk:
                    continue
                scenes_ = [r["scene"] for r in lk]
                sw = {rt: [int(r["route"] == rt) for r in lk] for rt in ROUTES}
                sw["recall_follows_s"] = [rc[s]["switched"] for s in scenes_]
                rr = X.resampled_rates(sw, [r["entity"] for r in lk], n_boot)
                share = {k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in sw.items()}
                used = [rt for rt in ROUTES[:4] if share[rt][0] >= USED_SHARE and share[rt][1] >= USED_LO]
                norm = float(
                    np.median([x["norm"] for x in norms if x["condition"] == cond and x.get("variant") == var])
                )
                blob.append({"condition": cond, **tag, "arm": arm, "n": len(lk), "share": share, "used": used,
                             "median_norm": norm})  # fmt: skip
                lines.append(f"| {label} | {arm} | {len(lk)} | " + " | ".join(ci(share[rt]) for rt in ROUTES)
                             + f" | {ci(share['recall_follows_s'])} |")  # fmt: skip
    lines += ["", f"Rule (fixed in advance): a route is used iff its share >= {USED_SHARE} with lower CI >= {USED_LO}. "
              "C1: identity = original (both a). Median norm of the change per condition: "
              + ", ".join(f"{b['condition']}{' ' + b['variant'] if 'variant' in b else ''} {b['median_norm']:.2f}"
                          for b in blob if b["arm"] == "whole") + "."]  # fmt: skip
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
    b45: dict = {}
    if m.get("prepend"):
        beta = X.read_jsonl(src / "beta.jsonl") if (src / "beta.jsonl").exists() else []
        b45["x45a"] = r = first_locker_rule(rows, beta, n_boot)
        lines += ["", "## 45a: first mention or first locker? (jobs/c3/batch45.yaml, fixed in advance)", "",
                  "Lookup, moves to or from the first locker (the O bridge's slot -> the S bridge's involves slot 0), "
                  "position share per arm; cut vs V0: V0's only-pointer position share minus the variant's (paired); "
                  "lost beyond random: position share without a random part of the pointer's share minus without the "
                  "pointer (paired).", "",
                  "| variant | moves | n | whole | only the pointer | only random | without the pointer | without random | lost beyond random | cut vs V0 |",
                  "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for label, cell in r["moves"].items():
            if not cell["n"]:
                continue
            for v in r["tested"]:
                sh_ = [ci(cell["share"][f"{v}|{a}"]) for a in PREPEND_ARMS]
                cut_ = cell["keep_alf_cut_vs_V0"].get(v)
                lines.append(f"| {v} | {label} | {cell['n']} | " + " | ".join(sh_)
                             + f" | {ci(cell['pos_lost_beyond_rand'][v])} | {ci(cut_) if cut_ else ''} |")  # fmt: skip
        if r["beta"]:
            lines += ["", "The code's shift beta vs V0 at O's bridge word (U U^T (h_v - h_V0) on mu_j+1 - mu_j, in its "
                      "units), per starting slot j:", "", "| variant | j | n | beta | ||d|| / ||mu_j+1 - mu_j|| (median) |",
                      "|---|---|---|---|---|"]  # fmt: skip
            lines += [f"| {k.split('|')[0]} | {k.split('|')[1]} | {b['n']} | {ci(b['beta'])} | {b['norm_ratio_median']:.2f} |"
                      for k, b in r["beta"].items()]  # fmt: skip
        lines += ["", "Rule: \"First locker stated before any item\" if V1, V2 and V3 each cut only-pointer position on "
                  "first-locker moves to at most half of V0 (paired CI excluding 0) while V4 does not; \"Order of "
                  "lockers, picks ignored\" if V1, V2 and V3 stay within 0.10 of V0; otherwise mixed. This run: "
                  + (f"cut {r['cut']}, within 0.10 {r['near']}" + (" (both rules hold; the first is reported)"
                                                                   if r["both_rules_hold"] else "") + " -> "
                     if "cut" in r else "")
                  + f"**{r['verdict']}**."]  # fmt: skip
    if m.get("identity_controls"):
        b45["x45e"] = f = identity_control_flags(rows, n_boot)
        lines += ["", "## 45e (a): identity controls (jobs/c3/batch45.yaml, fixed in advance)", ""]
        f["wrong_share"] = ws = wrong_share_report(norms)
        lines.append("The wrong-pair control's share against identity outside J++'s (wrong pairs from the bridge's own "
                     "domain): " + "; ".join(f"{c} median ratio {v['median_ratio']:.2f}, {v['short']} of {v['n']} scenes "
                                             f"under 0.9, smallest pool {v['min_pool']} entities"
                                             for c, v in ws.items()) + ".")  # fmt: skip
        if f["c0"]:
            lines.append("C0, lookup, share of the whole change's switches still switching (n = "
                         f"{f['c0']['n']}): " + "; ".join(f"{a} {ci(v)}" for a, v in f["c0"]["left"].items())
                         + f"; idout's minus half the wrong pair's {ci(f['c0']['idout_minus_half_wrong'])}.")  # fmt: skip
        if f["c2"]:
            lines.append(f"C2, lookup, identity share (n = {f['c2']['n']}): "
                         + "; ".join(f"{a} {ci(v)}" for a, v in f["c2"]["identity_share"].items())
                         + f". Cut by idout minus cut by the wrong pair: {ci(f['c2']['idout_vs_wrong'])} (PCA: "
                         f"{ci(f['c2']['idout_vs_pca'])}; with J++ + the pointer: {ci(f['c2']['union_idout_vs_wrong'])}).")  # fmt: skip
        lines += ["", f"(i) C0: idout + J++ + pointer leaves at most half of what the wrong pair + J++ + pointer leaves: "
                  f"{'yes' if f['holds_i'] else 'no'}; (ii) C2: idout cuts identity answers at least 0.15 more than the "
                  f"wrong pair: {'yes' if f['holds_ii'] else 'no'} -> both on this model: "
                  f"**{'yes' if f['both'] else 'no'}** (the rule counts models: idctrl-summary)."]  # fmt: skip
    if m.get("rendering", "chat") != "chat":
        b45["x45i"] = nv = never_value(rows, n_boot)
        w = nv["arms"].get("whole")
        lines += ["", f"## 45i: without the chat template ({m['rendering']}, read {m.get('read')})", "",
                  ("C2, lookup, whole change: " + f"value {ci(w['value'])} ({w['value_count']} of {w['n']}), identity "
                   f"{ci(w['identity'])}, position {ci(w['position'])}. " if w else "No C2 whole-change rows. ")
                  + f"\"Never the value\" (the value share stays at 0): **{'holds' if nv['holds'] else 'does not hold'}**"
                  f"; value share 0 in every arm: {'yes' if nv['value_zero_in_every_arm'] else 'no'}."]  # fmt: skip
    (out / "verdict.json").write_text(
        json.dumps({"run": name, "manifest": m, "rows": blob, "extra": extra, "ctrl": ctrl, **b45}, indent=1) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def marked(decode, ids: list[int], pos: int) -> str:
    """The prompt as decoded text with the token at pos (where the change is added) in ⟦...⟧."""
    return decode(ids[:pos]) + MARK.format(decode(ids[pos : pos + 1])) + decode(ids[pos + 1 :])


def stage_examples(name: str, k: int = N_EXAMPLES, seed: int = EXAMPLES_SEED, decode=None) -> Path:
    """CPU, over a run's files (batch 45: run by hand once Dan's predictions are committed): k random items of the run
    (seed), per reader the original prompt O exactly as the model reads it (ids decoded with special tokens, the
    template included) with the patch position in ⟦...⟧ (where h_S - h_O is added), the source prompt S with the same
    position marked, and every arm's answer (the top token at the read, the lookup's route). decode: ids -> text
    (default: the pinned tokenizer.json of the run's model)."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    if decode is None:
        from bridge_jspace.review import checks as RC

        tk = RC.tokenizer(m["model"]["target"])
        decode = lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    items = list(dict.fromkeys(r["scene"] for r in rows))
    rendering = m.get("rendering", "chat")
    read = ("the top token after a space token appended to O" if rendering == "chat" else
            "the first digit token among 8 greedy tokens after O (X0's digit read)")  # fmt: skip
    examples = []
    for s in random.Random(seed).sample(items, min(k, len(items))):
        c = cases[s]
        readers = {}
        for w, rd in c["readers"].items():
            mine = [r for r in rows if r["scene"] == s and r["reader"] == w]
            readers[w] = {"question": rd["question"], "answer_O": rd["answer"], "answer_S": rd["cf_answer"],
                          "prompt_O": marked(decode, rd["ids"]["org"], c["pos"]),
                          "prompt_S": marked(decode, rd["ids"]["alt"], c["pos"]),
                          "arms": [{"arm": r["arm"], "answer": decode([r["top"]]), "route": r.get("route"),
                                    "switched": r["switched"]} for r in mine]}  # fmt: skip
        examples.append({"scene": s, "condition": c["condition"], "variant": c.get("variant"),
                         "prepended": c.get("prepended"), "move": c.get("move"), "bridge_O": c["bridge"],
                         "bridge_S": c["cf_bridge"], "pos": c["pos"], "expect": c["expect"], "readers": readers})  # fmt: skip
    out = src / f"examples-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": name, "model": m["model"]["target"], "layer": m["layer"], "rendering": rendering, "read": read,
            "seed": seed, "k": len(examples), "of": len(items), "examples": examples}  # fmt: skip
    (out / "examples.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# Examples: {name}", "", f"{len(examples)} random items of {len(items)} (seed {seed}); model "
             f"{m['model']['target']}, layer {m['layer']}, rendering {rendering}. The change h_S - h_O (or the arm's part "
             f"of it) is added at ⟦...⟧ in O; the read is {read}. UNVERIFIED.", ""]  # fmt: skip
    for i, e in enumerate(examples, 1):
        lines += [f"## {i}. {e['scene']} ({e['condition']}" + (f", {e['variant']}: {e['prepended']!r}" if e["variant"]
                  else "") + ")", "", f"O bridge {e['bridge_O']!r}, S bridge {e['bridge_S']!r}, token {e['pos']}; "
                  f"expected digits {e['expect']}" + (f"; pointer move {e['move'][0]} -> {e['move'][1]}" if e["move"]
                                                      else "") + "."]  # fmt: skip
        for w, rd in e["readers"].items():
            lines += ["", f"### {'lookup' if w == X.LOOKUP else 'recall'} ({w}): O answers {rd['answer_O']}, S answers "
                      f"{rd['answer_S']}", "", "O, as read:", "", "```", rd["prompt_O"], "```", "", "S (the source):", "",
                      "```", rd["prompt_S"], "```", "", "| arm | answer | route | switched |", "|---|---|---|---|"]  # fmt: skip
            lines += [f"| {a['arm']} | {a['answer']!r} | {a['route'] or ''} | {a['switched']} |" for a in rd["arms"]]
        lines.append("")
    (out / "examples.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def stage_idctrl_summary(names: list[str], n_boot: int = X.N_BOOT) -> Path:
    """45e's rule over the models (CPU): each --identity-controls run's (i) and (ii) (identity_control_flags), a model
    whose C0 check failed counted as not tested, and the count of models where both hold (at least 2 of 3)."""
    flags, models = {}, {}
    for name in names:
        src = RESULTS / name
        m = json.loads((src / "manifest.json").read_text())
        assert m.get("identity_controls"), f"{name} is not an --identity-controls run"
        f = identity_control_flags(X.read_jsonl(src / "outcomes.jsonl"), n_boot)
        c0 = json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else None
        if not (c0 and c0["ok"]):
            f.update({"both": False, "tested": False, "c0_check": c0})
        flags[name], models[name] = f, m["model"]["target"]
    res = identity_specific(flags)
    out = RESULTS / f"x45e-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "x45e.json").write_text(json.dumps({"runs": models, "flags": flags, **res}, indent=1) + "\n")
    lines = ["# 45e (a): is identity outside J++ specific? (jobs/c3/batch45.yaml, fixed in advance)", "",
             "| run | model | (i) C0: idout + J++ + pointer leaves <= half of wrong pair + J++ + pointer | (ii) C2: cut minus "
             "wrong pair's >= 0.15 | both |", "|---|---|---|---|---|"]  # fmt: skip
    for name, f in flags.items():
        left = f["c0"]["left"] if f["c0"] else None
        i_ = f"{left['no_jppalfidout'][0]:.2f} vs {left['no_jppalfwrong'][0]:.2f}" if left else "–"
        ii_ = f"{f['c2']['idout_vs_wrong'][0]:.2f}" if f["c2"] else "–"
        lines.append(f"| {name} | {models[name]} | {i_} {'yes' if f['holds_i'] else 'no'} | {ii_} "
                     f"{'yes' if f['holds_ii'] else 'no'} | {'yes' if f['both'] else 'no'}"
                     + ("" if f["tested"] else " (not tested)") + " |")  # fmt: skip
    lines += ["", f"Both hold on {len(res['held_on'])} of {len(flags)} models (rule: at least {IDC_MODELS} of 3) -> "
              f"**{res['verdict']}**. UNVERIFIED."]  # fmt: skip
    (out / "x45e.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "examples", "idctrl-summary"])
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
    ap.add_argument("--prepend", default="", help="run / plan: 45a's variants on C2, comma-separated (V0,V1,V2,V3,V4)")
    ap.add_argument("--filler-tokens", nargs=2, type=int, default=[10, 12], metavar=("LO", "HI"),
                    help="--prepend: V4's fillers' length window (x8_write.filler_lengths)")  # fmt: skip
    ap.add_argument(
        "--identity-controls", action="store_true", help="run: 45e's wrong-pair and PCA controls (with --identity)"
    )
    ap.add_argument("--rendering", choices=RENDERINGS, default="chat",
                    help="run / plan: nochat = X0's prompt without the chat template, read by X0's digit rule (45i)")  # fmt: skip
    ap.add_argument("--sealed", action="store_true", help="run: no verdict after the run (batch 45: results closed)")
    ap.add_argument("--names", default="", help="idctrl-summary: the --identity-controls runs, comma-separated")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    prepend = tuple(v for v in a.prepend.split(",") if v)
    if a.stage == "plan":
        stage_plan(prepend, a.rendering, tuple(a.filler_tokens))
        return
    if a.stage == "examples":
        stage_examples(a.name)
        return
    if a.stage == "idctrl-summary":
        stage_idctrl_summary([n for n in a.names.split(",") if n], a.n_boot)
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
            a.identity or a.identity_controls,
            a.alf_from,
            prepend=prepend,
            filler_tokens=tuple(a.filler_tokens),
            identity_controls=a.identity_controls,
            rendering=a.rendering,
            sealed=a.sealed,
        )
    if a.stage == "verdict" or not (a.smoke or a.sealed):
        stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
