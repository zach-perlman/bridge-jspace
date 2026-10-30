"""nn_swap (Zach, 2026-10-28, prereg amendment 58 note 9): does a never-named bridge act as a workspace entity?

Items (jsuite v3, rendering 0, the model's v3 competence and note 4's eligibility): never-named RM (the question
describes the bridge, "the novelist who wrote Arrow of God"; the passage never names it), with references: MM (the same
kind of description, the bridge also named once in passing) and PM (named; edited at its mention, as jswap).
Site: RM / MM, the last token of the description in the question (--site last) or every description token (--site
span); PM, the last token of each mention of the bridge X. --site qmark: the question's "?" token; --site final: the
prompt's last token (both for every word; exp11 / exp14 read latent bridges at the last token from mid-late layers).
Donor D: another bridge of X's relation with a different answer, an eligible RM prompt of its own, and a name token
different from X's (many names share a first token; the clamp needs distinct name directions); seeded per item;
third: a random other answer of the relation (the chance of landing on any one answer).
Donor vectors, at every band layer:
  insert   D's residual at its last token in jswap_pointer's neutral sentence ("A reader asked a question about D ...")
  latent   D's residual at the last token of D's description in one of D's own eligible RM prompts (a computed bridge)
Conditions (k: the top-k J++ span by the lens's logits at each side, never one of the clean answer position's top-10, as
jswap):
  {src}_k{k}        h_X - Jk(h_X) + Jk(h_D)
  {src}_k{k}_rot    h_X + (Jk(h_D) - Jk(h_X)) R^T   (the same-size change in a fixed random direction)
  {src}_k{k}_rand   the transplant over a fixed random k-dim subspace: h_X - P h_X + P h_D
  {src}_k{k}_u      the transplant over the logit lens's top-k
  clamp             the paper's clamp (Gurnee et al. 2026; bridge_jspace.clamp.SwapClamp), at every position from 1: the
                    coordinates on X's and D's unit J-lens name vectors exchanged (clean coordinates, swapped), the rest
                    of the residual unchanged
  clamp_null        the clamp's edit, norm-matched, along a fixed random unit direction
  remove_k{k}       (note 9 addendum, necessity) h_X - Jk(h_X) at the site, no donor; remove_k{k}_rot: h_X - Jk(h_X) R^T
  note 10, the paper's decomposition of the patch D = h_D - h_X over S = the union of X's and D's top-10 J++ atoms:
  full_{src}        h_D (the whole patch)
  lens_{src}        h_X + P_S D            (the lens part only)
  rem_{src}         h_X + D - P_S D        (the remainder only)
  remfix_{src}      h_D - P_S h_D + P_S h_X_clean   (the remainder, the site's lens part held at its clean value)
  lensrand_{src}    h_X + P_R D, R a fixed random 20-dim subspace (control)
  note 11, bridge or answer: A = the span of the J++ atoms of every form of every answer in the v3 set (all relations);
  C = the span of as many fixed random atoms (control)
  {src}_k{k}_noans     the transplant with no answer in it: atoms never chosen from A, and the change projected off A:
                       h_X + (I - P_A)(Jk'(h_D) - Jk'(h_X))
  {src}_k{k}_noansctl  the same with C in place of A
  {src}_ans            the answer alone: h_X + P_{A_XD}(h_D - h_X), A_XD the span of X's and D's own answer atoms
  {src}_ansctl         the same over as many fixed random atoms
  remove_k{k}_noans    h_X - (I - P_A) Jk'(h_X)
  note 11 addendum, narrower scrubs (per item; atoms never chosen from the scrubbed rows; the change projected off them):
  {src}_k{k}_noansrel / _noansrelctl   the item's relation's answers (its answer_vocab), or as many of C's atoms
  {src}_k{k}_noansown / _noansownctl   X's and D's own answers only, or as many of C's atoms
  note 11, composition failures (--items fail: RM items whose hop 1 and hop 2 alone are right, the whole wrong):
  repair_k{k}          X's own lens part written in, from the neutral sentence about X: h_X - Jk(h_X) + Jk(h_Xn)
  repair_k{k}_rand / _rot / _noans    as the transplant's controls, with X's neutral state as the donor
  repair_full          h_Xn (the whole neutral state)
  note 13: clamp_noans, the clamp with X's and D's name vectors first made orthogonal to every answer direction (A);
  items with an in-context second hop (final P, jsuite_v3mp): D is another entity of the passage; classes kept (X's
  passage value), donor (D's passage value), third (D's remembered attribute), xmem (X's remembered attribute)
  note 15 (v4, cf only; Dan's 51.12 arms): Δ = h_D - h_X at the site, S as note 10, A an answer set (own: X's and D's own
  answers; rel: every answer of the item's relation), C as many of SEED_CTL's atoms, R note 10's random 20-dim subspace
  remrand_cf        h_X + Δ - P_R Δ                  (arms 1 and 2's random twin)
  remkeep{own,rel}_cf   h_X + Δ - (I - P_A) P_S Δ    (arm 2: without the lens part, its answer component kept)
  noa{own,rel}_cf   h_X + Δ - P_A Δ                  (arm 3: without the answer directions only); noa{own,rel}ctl_cf with C
  note 15 addendum 2: remkeepoth_cf / noaoth_cf / noaothctl_cf, the arms with two other answers of the relation (not X's,
  D's or the third's; random.Random('oth:' + id)) in place of X's and D's own
  note 15 addendum: lensshr_cf h_X + Rs, remshr_cf h_X + Δ - Rs, Rs = Δ's random part holding P_S Δ's share of ||Δ||²
  (Dan's random_subspace_part over rotation(d, 888 + layer))
  the "none" rows carry the readout check: the lens rank (over the letter tokens) of X's answer at h_X and D's at h_D,
  at the site and the band's first layer
  note 16 (v4, cf only; Dan's lens part): J = the signed OMP fit, 25 atoms, of Δ over the unit J++ vectors of the letter
  tokens and the ten digits (scripts/exp04_brew_parts.signed_omp); Jr = Δ's random part of the same share (Dan's
  random_subspace_part over rotation(d, 888 + layer))
  note 17 (--value-swap, v4): the donor prompt keeps the question about X and gives X another passage value (same
  vowel start, not in the passage, not X's real attribute); classes: donor = the new value; MP third = X's remembered
  attribute, MM third = X's old passage value
  note 18 (--position-swap, v4): the donor prompt keeps the question; X's fact sentence trades places with another
  entity Z's (X keeps its value); donor class = Z's value (the position route), kept = X's value; cf_ok = the donor prompt
  answered with X's value
  note 19 (--resample, v4): the donor is another passage's own question (same word and relation, a person absent from
  X's passage); classes: kept = X's answer, donor = the new person's remembered attribute, third = any other value of
  X's passage, xmem = X's remembered attribute (MP) / passage value (MM)
  note 21 addendum: lensnp_cf / remnp_cf / lensshrnp_cf / remshrnp_cf, the top-10 part and its same-share twin without the
  skip rule (no clean top-10 output token excluded)
  note 21 (--report, v4): the job's prompt is the item's hop-1 question over the same passage ('Which person wrote X?'),
  the donor the same with D's description clause; sites at the clause; classes the passage's names (kept X, donor D,
  third another entity)
  jpp_cf h_X + J; jpprand_cf h_X + Jr; nojpp_cf h_X + Δ - J; nojpprand_cf h_X + Δ - Jr ("jshare" on jpp rows: ||J||²/||Δ||²)
  note 38 (amendment 65; insert donor, k 10; e = insert_k10's edit Jk(h_D) - Jk(h_X); e'_V = the edit with atoms never
  chosen from V's rows, projected off them, as noansrel; Arel the relation's answers as noansrel):
  insert_k10_noansrel_nm        h_X + e'_Arel ||e|| / ||e'_Arel||   (per site row and layer: the scrubbed edit at e's norm)
  insert_k10_noansrel_x2 / _x4  h_X + 2 e'_Arel / 4 e'_Arel          (dose)
  insert_k10_noansoff           h_X + e'_Off, Off another relation's vocabulary count-matched to Arel's rows (n38_vocab:
                                film-director surnames for people / cities / companies / landmarks, demonyms for films;
                                subsampled, or padded with C's atoms)
  insert_k10_noansform          h_X + e'_Form, Form the people answers' countries (jsuite_v5kc.DEMONYM; people rows only)
  insert_relans                 h_X + P_Arel e                      (sufficiency)
  clamp_noans_nm                clamp_noans's delta rescaled per position to the clamp's delta norm (at the same h)
  rows of these carry share_rel = ||P_Arel e||²/||e||², share_c = ||P_C e||²/||e||² (C: as many of C's atoms as Arel's
  rows, noansrelctl's), share_off / share_form = ||P_V e||²/||e||², scrub_kept_{rel,off,form} = ||e'_V||²/||e||² (form:
  people only), each on the clean states (the same for every note 38 row of an item), mean over the band's layers, then
  the item's site rows; clamp_noans_nm rows carry clamp_ratio = ||delta_noans||²/||delta_clamp||² on the clean states
  (each summed over positions 1..; mean over layers). The vocabularies are written to <run>/n38_vocab.json.
Answers: the cand2 read among the relation's answers, classed kept (X's) / donor (D's) / third / other; transfer = donor
- third, 95% bootstrap over bridges (jswap.score), per word. For repair_*, kept is the fix rate.

python scripts/nn_swap.py --name N --why W --band 12-16 --competence C [--words RM MM PM] [--site last|span]
       [--ks 10] [--conds ...] [--sweep 4-8 8-12 ...] [--sample-per-word 0] [--batch 8] [--limit 0] [--seed 0]
       [--items eligible|fail]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.ablate import LensDictionary, rotation, top_span_removal  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts.ablate_v2 import bridge_positions  # noqa: E402
from scripts.jswap_pointer import NEUTRAL  # noqa: E402

RES = pins.RESULTS_DIR / "nn_swap"
SEED_RAND = 5800  # + layer: the random k-dim subspaces
SEED_NULL = 5900  # + layer: clamp_null's direction
SEED_CTL = 6100  # note 11: the fixed random atoms standing in for the answer atoms (noansctl, ansctl)


N15 = ("remrand", "remkeepown", "remkeeprel", "noaown", "noaownctl", "noarel", "noarelctl", "lensshr", "remshr",
       "remkeepoth", "noaoth", "noaothctl", "lensshrnp", "remshrnp")  # note 15 (+ addenda; oth: two other answers; np: no skip rule)
N16 = ("jpp", "jpprand", "nojpp", "nojpprand")  # note 16's arm kinds
N38 = ("insert_k10_noansrel_nm", "insert_k10_noansrel_x2", "insert_k10_noansrel_x4", "insert_k10_noansoff", "insert_k10_noansform",
       "insert_relans")  # note 38's transplant arms (clamp_noans_nm is with the clamp)


def n38_vocab(items: dict) -> dict:
    """Note 38: the other-relation vocabularies, from the set's own answer_vocab (deterministic). off: the films relation's
    answers (director surnames) for people, cities, companies and landmarks; the people relation's answers (demonyms) for
    films. form (people only): the people answers' countries (scripts/jsuite_v5kc.DEMONYM, checked to cover them)."""
    from scripts.jsuite_v5kc import DEMONYM

    vocab: dict = {}
    for it in items.values():
        if it.get("module") == "facts" and it["relation"] not in vocab:
            vocab[it["relation"]] = sorted(it["answer_vocab"])
    assert set(DEMONYM) == set(vocab["people"]), "note 38: DEMONYM must cover the people answers"
    return {"off": {r: vocab["people"] if r == "films" else vocab["films"] for r in vocab}, "form": {"people": sorted(set(DEMONYM.values()))}}


def random_subspace_part(delta: torch.Tensor, share: torch.Tensor, basis: torch.Tensor) -> torch.Tensor:
    """Note 16, copied from Dan's scripts/statement_positions.random_subspace_part (23 Oct): each row of delta [P, d]
    projected onto the first k columns of a random orthonormal basis, k per row so that it keeps share[row] of the row's
    squared norm (to within one basis direction)."""
    delta = delta.float()
    coef = delta @ basis
    cum = torch.cumsum(coef**2, dim=-1) / (delta.norm(dim=-1, keepdim=True) ** 2).clamp_min(1e-30)
    cum = torch.cat([torch.zeros_like(cum[:, :1]), cum], dim=-1)
    k = (cum - share.float()[:, None]).abs().argmin(dim=-1)
    keep = torch.arange(basis.shape[1], device=delta.device)[None, :] < k[:, None]
    return (coef * keep) @ basis.T


def fact_span(ctx: str, name: str) -> tuple[int, int]:
    """Note 18: [start, end) of the sentence (or bullet line) that mentions name in a v4 passage (prose; checked on all
    10488 entity sentences: each holds its own value and no other entity)."""
    i = ctx.find(name)
    s = max(ctx.rfind(". ", 0, i) + 2, ctx.rfind("\n", 0, i) + 1, 0)
    ends = [j for j in (ctx.find(". ", i), ctx.find(".\n", i)) if j >= 0] + [len(ctx) - 1 if ctx.endswith(".") else len(ctx)]
    return s, min(ends) + 1


def conds_for(ks: list[int]) -> list[str]:
    """Note 9: at k 10 every control; at the other k, the transplant and its random-subspace control."""
    out = []
    for k in ks:
        for src in ("insert", "latent"):
            out += [f"{src}_k{k}", f"{src}_k{k}_rand"] + ([f"{src}_k{k}_rot", f"{src}_k{k}_u"] if k == 10 else [])
    return [*out, "clamp", "clamp_null"]


def name_token(model, tok, name: str) -> int:
    try:
        return model.concept_token(name)
    except ValueError:
        return S.ids(tok, " " + name)[0]


def answer_tokens(tok, items: dict) -> list[int]:
    """Note 11: every first token of every answer in the v3 set (all relations, aliases too), with and without a leading
    space, as written and lowercased."""
    vals = {(w, it["kind"]) for it in items.values() if it.get("module") == "facts"
            for v in {*it.get("answer_vocab", []), *(it.get("answer_aliases") or [])} for w in (v, v.lower())}  # fmt: skip
    out = set()
    for w, kind in vals:
        out |= JS.forms(tok, w, kind) | {S.ids(tok, " " + w)[0], S.ids(tok, w)[0]}
    return sorted(out)


def build_prompt(tok, it: dict, set_name: str) -> dict:
    """Note 11: one item's whole question as ablate_v2.tasks_prompts builds it (kind 'clean', the natural branch), for
    items outside the eligible set; checked equal to tasks_prompts on eligible items in the smoke."""
    from scripts.ablate_v2 import natural_vocab

    q, ans, k = it["question"], it["answer"], it["kind"]
    ids = S.ids(tok, T.render(tok, {**it, "_question": q, "_kind": k})) + (S.ids(tok, " ") if k == "digit" else [])
    p = {"family": it["word"], "id": it["id"], "kind": "clean", "ids": ids, "tok": S.answer_token(tok, ans, k),
         "bridge": it["steps"][0]["answer"], "domain": it["domain"], "format": it["format"]}  # fmt: skip
    vocab = it.get("answer_vocab") or natural_vocab(set_name)[(it["domain"], "answer")]
    both = lambda v: {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k)}  # noqa: E731
    ok2 = both(ans)
    p["cands"] = sorted({S.answer_token(tok, v, k) for v in vocab} | {p["tok"]})
    p["ok2"] = sorted(ok2)
    p["cands2"] = sorted({t for v in vocab for t in both(v)} | ok2)
    return p


def v4_split(comp: str, cv_h1: str, set_name: str = "jsuite_v4_test_chat") -> dict[str, str]:
    """Note 14: MP / MM item id -> 'ok' (closed-book hop 1 right, hop 2 alone right, whole right, the no-description guess
    wrong) or 'fail' (the same but the whole wrong), from the model's v4 competence run (cand2; hop 1 also by its
    generated name) and its competence_variants run on H1 (the closed-book hop 1: cand2 or the greedy reply, with the
    bridge's other names)."""
    from scripts.score_greedy import right

    # the controls' own set: v4 family jsuite_v4* -> jsuite_v4ctl* (scripts/jsuite_v4.py); amendment 60: jsuite_v5<tag>_test_chat ->
    # jsuite_v5<tag>ctl_test_chat
    ctl_set = set_name.replace("jsuite_v4", "jsuite_v4ctl") if set_name.startswith("jsuite_v4") else set_name.replace("_test_chat", "ctl_test_chat")
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / ctl_set / "items.jsonl").read_text().splitlines()}
    h1 = {}
    for line in (pins.RESULTS_DIR / "competence_variants" / cv_h1 / "rows.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("variant", "none") == "none" and ":H1-" in r["id"]:
            it = items[r["id"]]
            h1[r["id"].replace(":H1-", ":XX-")] = bool(r["correct_cand2"]) or any(right(r["text"], v) for v in {it["answer"], *it["answer_aliases"]})
    parts: dict = collections.defaultdict(dict)
    for line in (pins.RESULTS_DIR / "tasks_v2" / comp / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        parts[r["id"]][r["part"]] = bool(r["correct"])
    out = {}
    words = (":MP-", ":MM-", ":MC-", ":MC0-") if set_name.startswith("jsuite_v5") else (":MP-", ":MM-")  # amendment 63 note 35: MC, MC0
    for i, d in parts.items():
        key = i.replace(":MP-", ":XX-").replace(":MM-", ":XX-").replace(":MC-", ":XX-").replace(":MC0-", ":XX-")
        if any(w in i for w in words) and h1.get(key) and d.get("step2") and d.get("guess") is False:
            out[i] = "ok" if d.get("whole") else "fail"
    return out


def composition_split(comp: str) -> dict[str, str]:
    """Note 11: RM item id -> 'ok' (hop 1, hop 2 and the whole right) or 'fail' (both hops right, the whole wrong), from
    the model's v3 competence run (cand2, hop 1 by its generated name, as eligibility)."""
    parts: dict = collections.defaultdict(dict)
    for line in (pins.RESULTS_DIR / "tasks_v2" / comp / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        parts[r["id"]][r["part"]] = bool(r["correct"])
    return {i: ("ok" if d.get("whole") else "fail") for i, d in parts.items() if ":RM-" in i and d.get("step1") and d.get("step2")}


@torch.no_grad()
def run_band(a, model, tok, lens, items, jobs, band: list[int], conds: list[str], tag: str, rows: list, t0: float, ans_tok: list[int]) -> None:
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    d = wg.shape[1]
    rot = {la: rotation(d, JS.SEED_ROT + la) for la in band}
    rand = {la: rotation(d, SEED_RAND + la) for la in band}  # first k columns: an orthonormal random k-subspace
    null = {la: rotation(d, SEED_NULL + la)[:, 0] for la in band}
    # note 11: the answer atoms A (every answer form in the set) and as many fixed random atoms C (control)
    a_rows = torch.unique(row_of[torch.tensor(ans_tok, device="cuda")])
    a_rows = a_rows[a_rows >= 0]
    g = torch.Generator().manual_seed(SEED_CTL)
    others = torch.tensor(sorted(set(range(letters.numel())) - set(a_rows.tolist())))
    c_rows = others[torch.randperm(len(others), generator=g)[: len(a_rows)]].to("cuda")

    def basis(D, rws: torch.Tensor) -> torch.Tensor:  # an orthonormal basis [d, r] of the atoms' span (rank-revealing)
        U, sv, _ = torch.linalg.svd(D.atoms(rws).T.double(), full_matrices=False)
        return U[:, sv > sv[0] * 1e-6].float()

    rel_cache: dict = {}

    def rel_rows(j: dict) -> list[int]:  # note 11 addendum: the relation's answer atoms, cached per (relation, kind)
        key = (j["rel"], j["kind_"])
        if key not in rel_cache:
            vocab = items[j["id"]]["answer_vocab"]
            toks = {t for v in vocab for w in (v, v.lower()) for t in (*JS.forms(tok, w, j["kind_"]), S.ids(tok, " " + w)[0], S.ids(tok, w)[0])}
            rel_cache[key] = sorted({int(row_of[t]) for t in toks if int(row_of[t]) >= 0})
        return rel_cache[key]

    n38_cache: dict = {}
    v38 = n38_vocab(items) if any(c in N38 for c in conds) else {}

    def n38_rows(j: dict) -> dict:  # note 38: off (count-matched to Arel's rows) and form (people) rows, as rel_rows; cached
        key = (j["rel"], j["kind_"])
        if key not in n38_cache:
            rel = rel_rows(j)

            def rows_of(words: list[str]) -> list[int]:  # every form of each word's first token, minus the relation's own rows
                toks = {t for v in words for w in (v, v.lower()) for t in (*JS.forms(tok, w, j["kind_"]), S.ids(tok, " " + w)[0], S.ids(tok, w)[0])}
                return sorted({int(row_of[t]) for t in toks if int(row_of[t]) >= 0} - set(rel))

            pool = rows_of(v38["off"][j["rel"]])
            pad = [r for r in c_rows.tolist() if r not in set(rel) | set(pool)][: max(0, len(rel) - len(pool))]
            off = sorted(random.Random(f"n38off:{j['rel']}").sample(pool, len(rel))) if len(pool) >= len(rel) else pool + pad
            form = rows_of(v38["form"][j["rel"]]) if j["rel"] in v38["form"] else []
            dec = lambda rs: [tok.decode([int(letters[r])]) for r in rs]  # noqa: E731
            n38_cache[key] = {"off": off, "form": form, "rel_rows": len(rel), "rel_tokens": dec(rel), "off_words": v38["off"][j["rel"]],
                              "off_pool": len(pool), "off_padded_from_c": len(off) - min(len(pool), len(rel)), "off_tokens": dec(off),
                              "form_words": v38["form"].get(j["rel"], []), "form_tokens": dec(form)}  # fmt: skip
            (RES / a.name / "n38_vocab.json").write_text(json.dumps({"|".join(k): v for k, v in n38_cache.items()}, indent=1) + "\n")
        return n38_cache[key]

    jdic = {}
    if any(c.split("_")[0] in N16 for c in conds):  # note 16: Dan's dictionary, the letter tokens and the ten digits
        digits = torch.tensor([S.ids(tok, str(i))[0] for i in range(10)], device="cuda")
        jids = torch.unique(torch.cat([letters, digits]))
        jdic = {la: lens.vectors(la, jids) for la in band}
        from scripts.exp04_brew_parts import signed_omp
    qa, qc = {}, {}
    if any(c.endswith(("_noans", "_noansctl")) for c in conds) or "clamp_noans_nm" in conds:  # note 38: clamp_noans_nm too
        for la in band:
            qa[la], qc[la] = basis(dic[la], a_rows), basis(dic[la], c_rows)
        print(f"[{tag}] note 11: {len(a_rows)} answer atoms (rank {qa[band[0]].shape[1]}), control rank {qc[band[0]].shape[1]}", flush=True)

    def forward(ids, hook_fn, record=False):
        rec = {}

        def hook_for(la):
            def hook(_m, _a, out):
                h = out[0] if isinstance(out, tuple) else out
                if record:
                    rec[la] = h.float().clone()
                if hook_fn is None:
                    return None
                new = hook_fn(la, h)
                return (new, *out[1:]) if isinstance(out, tuple) else new

            return hook

        with _forward_hooks([(model.layers[la], hook_for(la)) for la in band]):
            logits = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1).logits[:, -1].float()
        return logits, rec

    # donor vectors at every band layer: neutral sentences (insert) and D's own description end (latent)
    need = {}
    for j in jobs:
        need[("insert", j["d"], j["kind_"], j["format_"])] = j["neutral"]
        need[("latent", j["lat_id"])] = (j["lat_ids"], j["lat_pos"])
        if "self_neutral" in j:  # note 11: X's own neutral state (repair_*)
            need[("insert", j["x"], j["kind_"], j["format_"])] = j["self_neutral"]
        for key, val in j.get("cf", []):  # note 14: the counterfactual prompt's states at the aligned positions
            need[key] = val
    vec, cf_ok = {}, {}
    by_len = collections.defaultdict(list)
    for key, (ids, _pos) in need.items():
        by_len[len(ids)].append(key)
    job_of = {j["jid"]: j for j in jobs if "jid" in j}
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            lg_d, rec = forward(torch.tensor([need[k][0] for k in chunk], device="cuda"), None, record=True)
            for b, key in enumerate(chunk):
                vec[key] = torch.stack([rec[la][b, need[key][1]] for la in band])
                if key[0] == "cf" and key[2] == 0:  # note 14: does the model answer the counterfactual prompt with D's answer?
                    j = job_of[key[1]]
                    c2 = torch.tensor(j["cands2"], device=lg_d.device)
                    cf_ok[key[1]] = int(c2[lg_d[b, c2].argmax()]) in j["fx" if a.position_swap else "fd"]  # note 18: X's value, moved
    print(f"[{tag}] {len(vec)} donor residuals, {time.time() - t0:.0f}s", flush=True)

    def classify(lg, j):
        c2 = torch.tensor(j["cands2"], device=lg.device)
        pick = int(c2[lg[c2].argmax()])
        cls = "kept" if pick in j["ok2"] or pick in j["fx"] else "donor" if pick in j["fd"] else "third" if pick in j["ft"] else "xmem" if pick in j.get("fm", ()) else "other"
        return cls, pick

    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            clean, rec = forward(ids, None, record=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            meta = lambda j: {"x": j["x"], "donor": j["d"], "third": j["at"], "ax": j["ax"], "ad": j["ad"], "at": j["at"], "rel": j["rel"], "band": tag,  # noqa: E731
                              **({"cf_ok": cf_ok.get(j["jid"])} if "jid" in j else {})}  # fmt: skip
            none_at = len(rows)  # note 15: the readout check is added to these rows below
            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, **meta(j)})
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["sites"]], device="cuda")
            xi = torch.tensor([p for j in chunk for p in j["sites"]], device="cuda")
            ins = torch.stack([vec[("insert", chunk[b]["d"], chunk[b]["kind_"], chunk[b]["format_"])] for b in bi.tolist()])  # [m, L, d]
            lat = torch.stack([vec[("latent", chunk[b]["lat_id"])] for b in bi.tolist()])
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            cfv = torch.stack([vec[k] for j in chunk for k, _ in j["cf"]]) if any(c.endswith("_cf") for c in conds) else None  # note 14
            # note 11: atom choice also never from A (noans) or C (noansctl); X's and D's own answer atoms (ans), and as
            # many of C's atoms (ansctl); X's own neutral state (repair_*)
            groups_a = [((bi == b).nonzero().squeeze(1), torch.cat([prot[b], a_rows])) for b in range(len(chunk))]
            groups_c = [((bi == b).nonzero().squeeze(1), torch.cat([prot[b], c_rows])) for b in range(len(chunk))]
            own = [sorted({int(row_of[t]) for t in (*j["fx"], *j["fd"]) if int(row_of[t]) >= 0}) for j in chunk]
            width = max(1, max(len(o) for o in own))
            own_idx = torch.tensor([o + [0] * (width - len(o)) for o in own], device="cuda")[bi]
            own_mask = torch.tensor([[1] * len(o) + [0] * (width - len(o)) for o in own], device="cuda")[bi]
            ctl_idx = c_rows[:width][None].expand(len(chunk), -1)[bi]
            # note 11 addendum: the item's relation's answer atoms (every form of every answer in its answer_vocab) and X's
            # and D's own, each with as many of C's atoms; the atom choice never from the scrubbed rows
            narrow: dict = {}
            if any(c.split("_")[-1].startswith(("noansrel", "noansown")) or c.startswith(("remkeeprel", "noarel")) for c in conds):
                rel = [rel_rows(j) for j in chunk]
                rwidth = max(1, max(len(r) for r in rel))
                rel_idx = torch.tensor([r + [0] * (rwidth - len(r)) for r in rel], device="cuda")[bi]
                rel_mask = torch.tensor([[1] * len(r) + [0] * (rwidth - len(r)) for r in rel], device="cuda")[bi]
                relc_idx = c_rows[:rwidth][None].expand(len(chunk), -1)[bi]

                def excl(per_item: list[list[int]], ctl: bool) -> list:
                    return [((bi == b).nonzero().squeeze(1), torch.cat([prot[b], c_rows[: len(r)] if ctl else torch.tensor(r, dtype=torch.long, device="cuda")]))
                            for b, r in enumerate(per_item)]  # fmt: skip

                narrow = {"noansrel": (rel_idx, rel_mask, excl(rel, False)), "noansrelctl": (relc_idx, rel_mask, excl(rel, True)),
                          "noansown": (own_idx, own_mask, excl(own, False)), "noansownctl": (ctl_idx, own_mask, excl(own, True))}  # fmt: skip
            selfv = torch.stack([vec[("insert", chunk[b]["x"], chunk[b]["kind_"], chunk[b]["format_"])] for b in bi.tolist()]) if any(
                c.startswith("repair") for c in conds) else None  # fmt: skip
            # note 15: the answer sets (per site row) and the readout check on this chunk's "none" rows
            ans_sets = {"own": (own_idx, own_mask), "ownctl": (ctl_idx, own_mask)}
            if any(c.split("_")[0] in ("remkeepoth", "noaoth", "noaothctl") for c in conds):  # note 15 addendum 2: two other answers
                oth = []
                for j in chunk:
                    pool = sorted(set(items[j["id"]]["answer_vocab"]) - {j["ax"], j["ad"], j["at"]} - set(items[j["id"]].get("passage_values", {}).values()))
                    picks = random.Random(f"oth:{j['id']}").sample(pool, 2)
                    oth.append(sorted({int(row_of[t]) for v in picks for t in JS.forms(tok, v, j["kind_"]) if int(row_of[t]) >= 0}))
                ow = max(1, max(len(o) for o in oth))
                oth_idx = torch.tensor([o + [0] * (ow - len(o)) for o in oth], device="cuda")[bi]
                oth_mask = torch.tensor([[1] * len(o) + [0] * (ow - len(o)) for o in oth], device="cuda")[bi]
                ans_sets.update({"oth": (oth_idx, oth_mask), "othctl": (c_rows[:ow][None].expand(len(chunk), -1)[bi], oth_mask)})
            if "noansrel" in narrow:
                ans_sets.update({"rel": narrow["noansrel"][:2], "relctl": narrow["noansrelctl"][:2]})
            if any(c.split("_")[0] in N15 for c in conds):
                la0 = band[0]
                for which, hs, key in (("rank_ax", rec[la0][bi, xi], "fx"), ("rank_ad", cfv[:, 0], "fd")):
                    lg0 = dic[la0].logits(hs.float())  # [m, n] over the letter tokens
                    for b, j in enumerate(chunk):
                        r = [int(row_of[t]) for t in j[key] if int(row_of[t]) >= 0]
                        m0 = int((bi == b).nonzero()[0, 0])
                        rows[none_at + b][which] = int((lg0[m0] > lg0[m0, r].max()).sum()) + 1 if r else None
            jshare: dict = {}

            def note11(cond: str, la: int, li: int, hx: torch.Tensor) -> torch.Tensor:
                src, rest = cond.split("_")[0], cond.split("_")[1:]
                hd = None if src == "remove" else (ins if src == "insert" else lat if src == "latent" else selfv)[:, li]
                if rest[0] in ("ans", "ansctl"):  # the answer alone (or as many random atoms)
                    return hx + JS.span_proj(dic[la], hd - hx, own_idx if rest[0] == "ans" else ctl_idx, own_mask)
                if rest[0] == "full":  # repair_full
                    return hd
                kk, suf = int(rest[0][1:]), (rest[1] if len(rest) > 1 else "")
                if suf in ("noans", "noansctl"):
                    G, Q = (groups_a, qa[la]) if suf == "noans" else (groups_c, qc[la])
                    rx = top_span_removal(dic[la], hx, kk, protected=G)
                    e = -rx if src == "remove" else top_span_removal(dic[la], hd, kk, protected=G) - rx
                    return hx + e - (e @ Q) @ Q.T
                if suf in narrow:  # note 11 addendum: narrower scrubs, per item
                    idx, msk, G = narrow[suf]
                    rx = top_span_removal(dic[la], hx, kk, protected=G)
                    e = -rx if src == "remove" else top_span_removal(dic[la], hd, kk, protected=G) - rx
                    return hx + e - JS.span_proj(dic[la], e, idx, msk)
                if suf == "rand":  # repair_k_rand
                    Q = rand[la][:, :kk]
                    return hx - (hx @ Q) @ Q.T + (hd @ Q) @ Q.T
                rx, rd = top_span_removal(dic[la], hx, kk, protected=groups), top_span_removal(dic[la], hd, kk, protected=groups)
                return hx + (rd - rx) @ rot[la].T if suf == "rot" else hx - rx + rd  # repair_k / repair_k_rot
            # note 38: per item, the relation's answer rows (as noansrel), the other relation's (off), the people answers'
            # countries (form), and C's first len(Arel) atoms (noansrelctl's); each as (idx, mask) per site row and the
            # atom-choice exclusion. The logged shares are taken on the clean states at every band layer (the same for every
            # note 38 row of an item; equal to the in-run edit's at the band's first layer)
            n38: dict = {}
            n38_info: dict = {}

            def n38_edit(w: str, la: int, li: int, hx: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
                """insert_k10's edit e at hx, and the edit scrubbed of w's rows e' (atoms never chosen from them; projected
                off them; noansrel's for w = rel)."""
                hd = ins[:, li]
                e = top_span_removal(dic[la], hd, 10, protected=groups) - top_span_removal(dic[la], hx, 10, protected=groups)
                idx, msk, G = n38[w]
                e2 = top_span_removal(dic[la], hd, 10, protected=G) - top_span_removal(dic[la], hx, 10, protected=G)
                return e, e2 - JS.span_proj(dic[la], e2, idx, msk)

            if any(c in N38 for c in conds):
                sets = {"rel": [rel_rows(j) for j in chunk], "off": [n38_rows(j)["off"] for j in chunk], "form": [n38_rows(j)["form"] for j in chunk]}
                sets["c"] = [c_rows[: len(r)].tolist() for r in sets["rel"]]
                for w, per_item in sets.items():
                    wd = max(1, max(len(r) for r in per_item))
                    n38[w] = (torch.tensor([r + [0] * (wd - len(r)) for r in per_item], device="cuda")[bi],
                              torch.tensor([[1] * len(r) + [0] * (wd - len(r)) for r in per_item], device="cuda")[bi],
                              [((bi == b).nonzero().squeeze(1), torch.cat([prot[b], torch.tensor(r, dtype=torch.long, device="cuda")])) for b, r in enumerate(per_item)])  # fmt: skip
                sq = lambda v: (v.double() ** 2).sum(-1)  # noqa: E731
                acc = collections.defaultdict(list)  # stat -> one [m] tensor per band layer
                for li, la in enumerate(band):
                    hx = rec[la][bi, xi]
                    for w in ("rel", "off", "form"):
                        e, e2 = n38_edit(w, la, li, hx)
                        ee = sq(e).clamp_min(1e-30)
                        acc[f"scrub_kept_{w}"].append(sq(e2) / ee)
                        acc[f"share_{w}"].append(sq(JS.span_proj(dic[la], e, *n38[w][:2])) / ee)
                    acc["share_c"].append(sq(JS.span_proj(dic[la], e, *n38["c"][:2])) / ee)
                for stat, per_layer in acc.items():
                    v = torch.stack(per_layer).mean(0)
                    for b, j in enumerate(chunk):
                        if not stat.endswith("_form") or j["rel"] == "people":
                            n38_info.setdefault(b, {})[stat] = round(float(v[bi == b].mean()), 4)

            def note38(cond: str, la: int, li: int, hx: torch.Tensor) -> torch.Tensor:
                if cond == "insert_relans":  # sufficiency: only the relation-vocabulary component of the transplant
                    e = top_span_removal(dic[la], ins[:, li], 10, protected=groups) - top_span_removal(dic[la], hx, 10, protected=groups)
                    return hx + JS.span_proj(dic[la], e, *n38["rel"][:2])
                e, e2 = n38_edit({"noansoff": "off", "noansform": "form"}.get(cond.split("_")[2], "rel"), la, li, hx)
                if cond.endswith("_nm"):  # per site row: the scrubbed edit at the unscrubbed edit's norm
                    e2 = e2 * (e.norm(dim=-1, keepdim=True) / e2.norm(dim=-1, keepdim=True).clamp_min(1e-12))
                elif cond.endswith(("_x2", "_x4")):
                    e2 = e2 * int(cond[-1])
                return hx + e2

            def n38_stats(cond: str, b: int) -> dict:  # note 38: the logged shares on this condition's rows
                return n38_info.get(b, {}) if cond in N38 else n38_info.get(("clamp", b), {}) if cond == "clamp_noans_nm" else {}

            # the clamp: X's and D's unit J-lens name vectors per item and layer; clean coordinates swapped
            clamp_atoms, clamp_pinv, clamp_tgt = {}, {}, {}
            if any(c.startswith("clamp") for c in conds):
                rows_xd = torch.tensor([[int(row_of[j["tx"]]), int(row_of[j["td"]])] for j in chunk], device="cuda")
                ok_rows = (rows_xd >= 0).all(dim=1)
                for la in band:
                    A = dic[la].atoms(rows_xd.clamp_min(0))  # [B, 2, d]
                    P = torch.linalg.pinv(A.double()).float()  # [B, d, 2]
                    c = rec[la] @ P  # [B, T, 2] clean coordinates
                    clamp_atoms[la], clamp_pinv[la], clamp_tgt[la] = A, P, c[..., [1, 0]]
                    if "clamp_noans" in conds or "clamp_noans_nm" in conds:  # note 13: the name vectors made orthogonal to every answer direction first
                        An = A - (A @ qa[la]) @ qa[la].T
                        An = An / An.norm(dim=-1, keepdim=True).clamp_min(1e-6)
                        Pn = torch.linalg.pinv(An.double()).float()
                        clamp_atoms[("noans", la)], clamp_pinv[("noans", la)], clamp_tgt[("noans", la)] = An, Pn, (rec[la] @ Pn)[..., [1, 0]]
                    if "clamp_noans_nm" in conds:  # note 38: ||delta_noans||² / ||delta_clamp||² on the clean states, summed over positions 1..
                        dn_, dc_ = ((clamp_tgt[k_] - rec[la] @ clamp_pinv[k_]) @ clamp_atoms[k_] for k_ in (("noans", la), la))
                        cr = (dn_[:, 1:].double() ** 2).sum((1, 2)) / (dc_[:, 1:].double() ** 2).sum((1, 2)).clamp_min(1e-30)
                        for b in range(len(chunk)):
                            n38_info.setdefault(("clamp", b), {}).setdefault("clamp_ratio", []).append(float(cr[b]))
                for b in range(len(chunk)):
                    if ("clamp", b) in n38_info:
                        n38_info[("clamp", b)]["clamp_ratio"] = round(sum(n38_info[("clamp", b)]["clamp_ratio"]) / len(band), 4)
            for cond in conds:

                def hook_fn(la, h, cond=cond):
                    li = band.index(la)
                    h = h.clone()
                    if cond.startswith("clamp"):
                        k = ("noans", la) if cond in ("clamp_noans", "clamp_noans_nm") else la
                        delta = (clamp_tgt[k] - h.float() @ clamp_pinv[k]) @ clamp_atoms[k]  # [B, T, d]
                        if cond == "clamp_null":
                            delta = delta.norm(dim=-1, keepdim=True) * null[la]
                        if cond == "clamp_noans_nm":  # note 38: rescaled per position to the clamp's delta norm at the same h
                            full = (clamp_tgt[la] - h.float() @ clamp_pinv[la]) @ clamp_atoms[la]
                            delta = delta * (full.norm(dim=-1, keepdim=True) / delta.norm(dim=-1, keepdim=True).clamp_min(1e-12))
                        delta[:, 0] = 0  # position 0 (the attention sink) is never edited, as SwapClamp
                        delta[~ok_rows] = 0
                        return (h.float() + delta).to(h.dtype)
                    if cond in N38:  # note 38
                        h[bi, xi] = note38(cond, la, li, h[bi, xi].float()).to(h.dtype)
                        return h
                    if cond.startswith("repair") or cond.split("_")[-1] in ("noans", "noansctl", "ans", "ansctl", "noansrel", "noansrelctl",
                                                                            "noansown", "noansownctl"):  # note 11 (and its addendum)  # fmt: skip
                        h[bi, xi] = note11(cond, la, li, h[bi, xi].float()).to(h.dtype)
                        return h
                    kind0 = cond.split("_")[0]
                    if kind0 in N15 or kind0 in N16:  # notes 15-16 (cf only)
                        hx = h[bi, xi].float()
                        dl = cfv[:, li] - hx
                        if kind0 in N16:  # Dan's lens part: the 25-atom signed OMP fit of the change, or its random twin
                            jp = signed_omp(jdic[la], dl, 25)
                            share = jp.norm(dim=-1) ** 2 / (dl.norm(dim=-1) ** 2).clamp_min(1e-30)
                            if kind0 == "jpp" and li == 0:
                                jshare.update({b: float(share[bi == b].mean()) for b in range(len(chunk))})
                            if kind0.endswith("rand"):
                                jp = random_subspace_part(dl, share, rot[la])
                            new = hx + jp if kind0 in ("jpp", "jpprand") else hx + dl - jp
                        elif kind0 == "remrand":  # arms 1 and 2's random twin
                            Q = rand[la][:, :20]
                            new = hx + dl - (dl @ Q) @ Q.T
                        elif kind0 in ("lensshr", "remshr", "lensshrnp", "remshrnp"):  # note 15 addendum: S's same-share random twin
                            pg = None if kind0.endswith("np") else groups  # note 21 addendum: np, the top-10 without the skip rule
                            _, cx = top_span_removal(dic[la], hx, 10, protected=pg, return_chosen=True)
                            _, cd = top_span_removal(dic[la], cfv[:, li], 10, protected=pg, return_chosen=True)
                            Q = torch.linalg.qr(dic[la].atoms(torch.cat([cx, cd], dim=1)).transpose(1, 2).double())[0].float()
                            ps = (Q @ (Q.transpose(1, 2) @ dl.unsqueeze(2))).squeeze(2)
                            rp = random_subspace_part(dl, ps.norm(dim=-1) ** 2 / (dl.norm(dim=-1) ** 2).clamp_min(1e-30), rot[la])
                            new = hx + rp if kind0.startswith("lensshr") else hx + dl - rp
                        else:
                            idx, msk = ans_sets[kind0.removeprefix("remkeep").removeprefix("noa")]
                            if kind0.startswith("noa"):  # arm 3: without the answer directions only (or C's)
                                new = hx + dl - JS.span_proj(dic[la], dl, idx, msk)
                            else:  # arm 2: without the lens part, its answer component kept (S as note 10)
                                _, cx = top_span_removal(dic[la], hx, 10, protected=groups, return_chosen=True)
                                _, cd = top_span_removal(dic[la], cfv[:, li], 10, protected=groups, return_chosen=True)
                                Q = torch.linalg.qr(dic[la].atoms(torch.cat([cx, cd], dim=1)).transpose(1, 2).double())[0].float()
                                ps = (Q @ (Q.transpose(1, 2) @ dl.unsqueeze(2))).squeeze(2)
                                new = hx + dl - (ps - JS.span_proj(dic[la], ps, idx, msk))
                        h[bi, xi] = new.to(h.dtype)
                        return h
                    if cond.split("_")[0] in ("full", "lens", "rem", "remfix", "lensrand", "lensnp", "remnp"):  # note 10 (np: note 21 addendum)
                        kind, src = cond.split("_")
                        hx = h[bi, xi].float()
                        hd = (ins if src == "insert" else lat if src == "latent" else cfv)[:, li]  # note 14: cf, the counterfactual prompt
                        if kind == "full":
                            new = hd
                        else:
                            if kind == "lensrand":  # control: a fixed random 20-dim subspace
                                Q = rand[la][:, :20][None].expand(hx.shape[0], -1, -1)
                            else:  # the union of X's and D's top-10 J++ atoms at the site (one subspace for every cell)
                                pg = None if kind.endswith("np") else groups  # np: without the skip rule (note 21 addendum)
                                _, cx = top_span_removal(dic[la], hx, 10, protected=pg, return_chosen=True)
                                _, cd = top_span_removal(dic[la], hd, 10, protected=pg, return_chosen=True)
                                Q = torch.linalg.qr(dic[la].atoms(torch.cat([cx, cd], dim=1)).transpose(1, 2).double())[0].float()
                            proj = lambda v, Q=Q: (Q @ (Q.transpose(1, 2) @ v.unsqueeze(2))).squeeze(2)  # noqa: E731
                            if kind in ("lens", "lensrand", "lensnp"):
                                new = hx + proj(hd - hx)
                            elif kind in ("rem", "remnp"):
                                new = hx + (hd - hx) - proj(hd - hx)
                            else:  # remfix: the remainder, with the site's lens part held at its clean value
                                hc = rec[la][bi, xi]
                                new = hd - proj(hd) + proj(hc)
                        h[bi, xi] = new.to(h.dtype)
                        return h
                    src, kk = cond.split("_")[0], int(cond.split("_")[1][1:])
                    hx = h[bi, xi].float()
                    if src == "remove":  # note 9 addendum: the slice erased at the site, no donor (necessity)
                        rx = top_span_removal(dic[la], hx, kk, protected=groups)
                        new = hx - rx @ rot[la].T if cond.endswith("_rot") else hx - rx
                        h[bi, xi] = new.to(h.dtype)
                        return h
                    hd = (ins if src == "insert" else lat)[:, li]
                    if cond.endswith("_rand"):
                        Q = rand[la][:, :kk]
                        new = hx - (hx @ Q) @ Q.T + (hd @ Q) @ Q.T
                    else:
                        D = unembed if cond.endswith("_u") else dic[la]
                        rx, rd = top_span_removal(D, hx, kk, protected=groups), top_span_removal(D, hd, kk, protected=groups)
                        new = hx + (rd - rx) @ rot[la].T if cond.endswith("_rot") else hx - rx + rd
                    h[bi, xi] = new.to(h.dtype)
                    return h

                lg, _ = forward(ids, hook_fn)
                for b, j in enumerate(chunk):
                    if cond.startswith("clamp") and not bool(ok_rows[b]):
                        continue
                    if cond == "insert_k10_noansform" and j["rel"] != "people":  # note 38: people only
                        continue
                    cls, pick = classify(lg[b], j)
                    rows.append({"id": j["id"], "family": j["family"], "condition": cond, "cls": cls, "pick": pick, **meta(j),
                                 **({"jshare": round(jshare[b], 4)} if cond.startswith("jpp_") and b in jshare else {}), **n38_stats(cond, b)})  # fmt: skip
        print(f"[{tag}] {len(rows)} rows, {time.time() - t0:.0f}s", flush=True)


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    bands = [list(range(int(w.split("-")[0]), int(w.split("-")[1]) + 1)) for w in (a.sweep or [a.band])]
    conds = a.conds or (["insert_k10", "insert_k10_rand"] if a.sweep else conds_for(a.ks))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "model": pins.model_pin(), "lens": pins.FROZEN_LENS,
                                                       "bands": [f"{b[0]}-{b[-1]}" for b in bands], "set": a.set, "competence": a.competence, "words": a.words,
                                                       "site": a.site, "conditions": conds, "ks": a.ks, "sample_per_word": a.sample_per_word, "limit": a.limit,
                                                       "neutral": NEUTRAL, "seeds": {"items": "random.Random(item id)" if not a.seed else f"random.Random('{a.seed}:' + item id)",
                                                                 "rand": f"{SEED_RAND}+layer", "null": f"{SEED_NULL}+layer", "rot": f"{JS.SEED_ROT}+layer", "ctl": SEED_CTL},
                                                       "seed": a.seed, "items": a.items, "sample_refs": a.sample_refs, "scene_words": a.scene_words, "cv_h1": a.cv_h1, "value_swap": a.value_swap, "position_swap": a.position_swap, "resample": a.resample, "report": a.report,
                                                       "git_commit": commit, "git_state": pins.git_state(), "bj_gram_proj": __import__("os").environ.get("BJ_GRAM_PROJ")}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    # note 14: v4 needs no eligible pool (its targets come from v4_split, its donors from the scene)
    prompts = [] if a.items.startswith("v4") else [p for p in JS.v3_prompts(tok, a.set, a.competence, list(a.words), a.scene_words) if p["family"] in a.words]
    targets = prompts
    if a.items in ("v4ok", "v4fail"):  # note 14: v4's gate (scene donors; no eligible-prompt pool needed)
        split = v4_split(a.competence, a.cv_h1, a.set)
        want = a.items[2:]
        targets = [build_prompt(tok, items[i], a.set) for i, s in sorted(split.items()) if s == want and items[i]["word"] in a.words]
        print(f"note 14: {len(targets)} v4 items ({want}); gate counts {dict(collections.Counter(split.values()))}", flush=True)
    if a.items == "fail":  # note 11: RM items whose hops alone are right and the whole wrong; donors stay the eligible ones
        split = composition_split(a.competence)
        targets = [build_prompt(tok, items[i], a.set) for i, s in sorted(split.items()) if s == "fail" and items[i]["word"] in a.words]
        print(f"note 11: {len(targets)} composition failures (both hops right, the whole wrong); {sum(s == 'ok' for s in split.values())} successes", flush=True)
    rm_by = collections.defaultdict(list)  # (relation, bridge) -> eligible RM prompts (latent donors)
    for p in prompts:
        if p["family"] == "RM":
            it = items[p["id"]]
            pos = bridge_positions(tok, p["ids"], it["start_desc"])
            if pos:
                rm_by[(it["relation"], it["bridge"])].append((p, pos[-1]))
    jobs = []
    for p in targets:
        it = items[p["id"]]
        x, rel, kind = it["bridge"], it["relation"], it["kind"]
        t = JS.table(it)
        ans = lambda b, t=t: t["facts"][b][0]  # noqa: E731
        ax = ans(x)
        if p["family"] in ("PM", "PK") and a.site in ("last", "span"):
            sites = JS.spans(bridge_positions(tok, p["ids"], x))
        elif a.site == "final":
            sites = [len(p["ids"]) - 1]
        elif a.site == "qmark":  # the question's own "?": the last token whose text contains "?" after the description
            pieces = [tok.decode([i]) for i in p["ids"]]
            desc_end = (bridge_positions(tok, p["ids"], it["start_desc"]) or [0])[-1]
            sites = [i for i, piece in enumerate(pieces) if "?" in piece and i >= desc_end][:1]
        else:
            pos = bridge_positions(tok, p["ids"], it["start_desc"])
            sites = pos if a.site == "span" else pos[-1:]
        if not sites:
            continue
        rng = random.Random(p["id"] if not a.seed else f"{a.seed}:{p['id']}")  # note 11: --seed draws other donors
        ok_name = lambda e: not (e.lower().startswith(x.lower()) or x.lower().startswith(e.lower()))  # noqa: E731
        tx = name_token(model, tok, x)  # the clamp needs distinct name directions: no donor whose name token is X's
        if it.get("set_version") == "v4":  # note 14: D another entity of the scene; the counterfactual prompt asks about D
            pv, mem = it["passage_values"], (lambda e, t=t: t["facts"][e][0])
            xv = pv[x]
            lookup = it["final"] == "P"
            cands = sorted(e for e in it["entities"] if e != x and mem(e) not in (xv, pv[e]) and (lookup or mem(e) != mem(x))
                           and ok_name(e) and name_token(model, tok, e) != tx)  # fmt: skip
            if not cands:
                continue
            dn = rng.choice(cands)
            desc_x, desc_d = it["start_desc"], rng.choice(it["entity_descs"][dn])
            assert it["question"].count(desc_x) == 1, it["id"]
            if a.value_swap:  # note 17: the same question about X; the donor passage gives X another value
                vowel = xv[0].lower() in "aeiou"
                pool = sorted(v for v in it["answer_vocab"] if v not in pv.values() and v != mem(x) and (v[0].lower() in "aeiou") == vowel
                              and not any(v in w or w in v for w in pv.values()))  # fmt: skip
                if it["context"].count(xv) != 1 or not pool:
                    continue
                vnew = rng.choice(pool)
                ctx2 = it["context"].replace(xv, vnew, 1)
                if ctx2.count(vnew) != 1:
                    continue
                dn, desc_d = x, desc_x
                cf_ids = S.ids(tok, T.render(tok, {**it, "context": ctx2, "_question": it["question"], "_kind": kind}))
            elif a.report:  # note 21: the same passage, the hop-1 question ("Which person wrote X?"): the bridge is said, not used
                q1, k1 = it["steps"][0]["question"], it["steps"][0]["kind"]
                desc_x, desc_d = (re.split(r" (?:who|that) ", d_, maxsplit=1)[-1] for d_ in (desc_x, desc_d))
                if q1.count(desc_x) != 1:
                    continue
                p = {**p, "ids": S.ids(tok, T.render(tok, {**it, "_question": q1, "_kind": k1}))}
                cf_ids = S.ids(tok, T.render(tok, {**it, "_question": q1.replace(desc_x, desc_d), "_kind": k1}))
            elif a.resample:  # note 19: the donor is another passage's own question, about a person absent from X's passage
                pool = sorted(i for i, o in items.items() if o.get("set_version") == "v4" and o["word"] == it["word"] and o["relation"] == rel
                              and o["scene"] != it["scene"] and o["bridge"] not in it["entities"] and o["bridge"] in t["facts"]
                              and mem(o["bridge"]) not in set(pv.values()) | {mem(x)} and ok_name(o["bridge"]))  # fmt: skip
                if not pool:
                    continue
                od = items[rng.choice(pool)]
                dn, desc_d = od["bridge"], od["start_desc"]
                cf_ids = S.ids(tok, T.render(tok, {**od, "_question": od["question"], "_kind": od["kind"]}))
            elif a.position_swap:  # note 18: the same question about X; X's fact sentence trades places with Z's
                ctx = it["context"]
                zs = sorted(e for e in it["entities"] if e != x and pv[e] not in (xv, mem(x)) and ctx.count(e) == 1)
                if ctx.count(x) != 1 or not zs:
                    continue
                zn = rng.choice(zs)
                (s1, e1), (s2, e2) = sorted((fact_span(ctx, x), fact_span(ctx, zn)))
                if e1 > s2:
                    continue
                ctx2 = ctx[:s1] + ctx[s2:e2] + ctx[e1:s2] + ctx[s1:e1] + ctx[e2:]
                assert sorted(ctx2) == sorted(ctx) and ctx2 != ctx, it["id"]
                dn, desc_d, zval = x, desc_x, pv[zn]
                cf_ids = S.ids(tok, T.render(tok, {**it, "context": ctx2, "_question": it["question"], "_kind": kind}))
            else:
                cf_ids = S.ids(tok, T.render(tok, {**it, "_question": it["question"].replace(desc_x, desc_d), "_kind": kind}))
            cf_desc = bridge_positions(tok, cf_ids, desc_d)
            x_desc = bridge_positions(tok, p["ids"], desc_x)
            if not cf_desc or not x_desc:
                continue
            if a.site == "span":  # the two descriptions right-aligned over the shorter one
                n_al = min(len(cf_desc), len(x_desc))
                sites, cf_pos = x_desc[-n_al:], cf_desc[-n_al:]
            elif a.site == "final":
                sites, cf_pos = [len(p["ids"]) - 1], [len(cf_ids) - 1]
            else:
                sites, cf_pos = x_desc[-1:], cf_desc[-1:]
            text = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(dn), "question": "Has anyone else heard about this?", "kind": kind, "format": it["format"]})
            nids = S.ids(tok, text)
            npos = JS.spans(bridge_positions(tok, nids, dn))
            if not npos:
                continue
            # MP: kept X's passage value, donor D's passage value, third D's remembered attribute, xmem X's remembered one;
            # MM (recall twin): kept X's attribute, donor D's attribute, third D's passage value, xmem X's passage value
            ax, ad, at, am = (xv, pv.get(dn), mem(dn), mem(x)) if lookup else (mem(x), mem(dn), pv.get(dn), xv)  # note 19: dn may be absent from the passage (overridden below)
            if a.value_swap:  # note 17: donor = X's new passage value; MP third = X's remembered attribute, MM third = X's old value
                ax, ad, at, am = (xv, vnew, mem(x), xv) if lookup else (mem(x), vnew, xv, mem(x))
            if a.position_swap:  # note 18: donor = Z's value (the value at X's new slot in the original passage: the position route)
                ax, ad, at, am = (xv, zval, mem(x), xv) if lookup else (mem(x), zval, xv, mem(x))
            if a.resample:  # note 19: donor = the new person's remembered attribute; third = another value of X's passage (set below)
                ax, ad, at, am = (xv, mem(dn), xv, mem(x)) if lookup else (mem(x), mem(dn), xv, xv)
            jid = f"{p['id']}|{dn}"
            jobs.append({**p, "x": x, "d": dn, "rel": rel, "sites": sites, "kind_": kind, "format_": it["format"], "neutral": (nids, npos[0]),
                         "lat_id": f"none:{p['id']}", "lat_ids": nids, "lat_pos": npos[0], "tx": tx, "td": name_token(model, tok, dn),
                         "cf": [(("cf", jid, si), (cf_ids, cp)) for si, cp in enumerate(cf_pos)], "jid": jid,
                         "fx": JS.forms(tok, ax, kind), "fd": JS.forms(tok, ad, kind), "ft": JS.forms(tok, at, kind), "fm": JS.forms(tok, am, kind),
                         "ax": ax, "ad": ad, "at": at})  # fmt: skip
            if a.resample:  # note 19: third = any other value of X's passage
                jobs[-1]["ft"] = set().union(*(JS.forms(tok, v, kind) for v in pv.values() if v != xv))
                jobs[-1]["at"] = "another passage value"
            if a.report:  # note 21: kept X's name, donor D's name, third another entity of the passage; candidates the passage's names
                nm = lambda e: {S.ids(tok, " " + e)[0], S.ids(tok, e)[0]}  # noqa: E731
                jobs[-1].update({"fx": nm(x), "fd": nm(dn), "ft": set().union(*(nm(e) for e in it["entities"] if e not in (x, dn))),
                                 "fm": set(), "ax": x, "ad": dn, "at": "another entity of the passage",
                                 "ok2": sorted(nm(x)), "cands2": sorted(set().union(*(nm(e) for e in it["entities"])))})  # fmt: skip
            continue
        if it.get("final") == "P":  # note 13: an in-context second hop (jsuite_v3mp); D is another entity of the passage
            pv, mem = it["passage_values"], (lambda e, t=t: t["facts"][e][0] if e in t["facts"] else None)
            ax = it["answer"]  # X's passage value
            cands = sorted(e for e in it["entities"] if e != x and pv.get(e) and pv[e] != ax and mem(e) and mem(e) not in (ax, pv[e])
                           and ok_name(e) and name_token(model, tok, e) != tx)  # fmt: skip
            if not cands:
                continue
            dn = rng.choice(cands)
            text = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(dn), "question": "Has anyone else heard about this?", "kind": kind, "format": it["format"]})
            nids = S.ids(tok, text)
            npos = JS.spans(bridge_positions(tok, nids, dn))
            if not npos:
                continue
            # kept: X's passage value; donor: D's passage value (the lookup followed D); third: D's remembered attribute (D's
            # memory bundle); xmem: X's remembered attribute
            jobs.append({**p, "x": x, "d": dn, "rel": rel, "sites": sites, "kind_": kind, "format_": it["format"], "neutral": (nids, npos[0]),
                         "lat_id": f"none:{p['id']}", "lat_ids": nids, "lat_pos": npos[0], "tx": tx, "td": name_token(model, tok, dn),
                         "fx": JS.forms(tok, ax, kind), "fd": JS.forms(tok, pv[dn], kind), "ft": JS.forms(tok, mem(dn), kind),
                         "fm": JS.forms(tok, mem(x), kind) if mem(x) else set(), "ax": ax, "ad": pv[dn], "at": mem(dn)})  # fmt: skip
            continue
        donors = sorted(b for (r, b) in rm_by if r == rel and b != x and ans(b) != ax and ok_name(b) and name_token(model, tok, b) != tx)
        if not donors:
            continue
        dn = rng.choice(donors)
        lat_p, lat_pos = rng.choice(rm_by[(rel, dn)])
        thirds = sorted(set(it["answer_vocab"]) - {ax, ans(dn)})
        at = rng.choice(thirds)
        text = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(dn), "question": "Has anyone else heard about this?", "kind": kind, "format": it["format"]})
        nids = S.ids(tok, text)
        npos = JS.spans(bridge_positions(tok, nids, dn))
        if not npos:
            continue
        jobs.append({**p, "x": x, "d": dn, "rel": rel, "sites": sites, "kind_": kind, "format_": it["format"], "neutral": (nids, npos[0]),
                     "lat_id": lat_p["id"], "lat_ids": lat_p["ids"], "lat_pos": lat_pos, "tx": tx, "td": name_token(model, tok, dn),
                     "fx": JS.forms(tok, ax, kind), "fd": JS.forms(tok, ans(dn), kind), "ft": JS.forms(tok, at, kind), "ax": ax, "ad": ans(dn), "at": at})  # fmt: skip
        if any(c.startswith("repair") for c in conds):  # note 11: X's own neutral sentence
            stext = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(x), "question": "Has anyone else heard about this?", "kind": kind, "format": it["format"]})
            sids = S.ids(tok, stext)
            spos = JS.spans(bridge_positions(tok, sids, x))
            if not spos:
                jobs.pop()
                continue
            jobs[-1]["self_neutral"] = (sids, spos[0])
    per = collections.defaultdict(list)
    for j in jobs:
        per[j["family"]].append(j)
    if a.sample_per_word:
        jobs = [j for f in a.words for k, j in enumerate(per[f])
                if len(per[f]) <= a.sample_per_word or k in set(random.Random(f"0:{f}").sample(range(len(per[f])), a.sample_per_word))]  # fmt: skip
    if a.sample_refs:  # note 10: the reference words (all but RM) capped at N, seeded
        jobs = [j for f in a.words for k, j in enumerate(per[f])
                if f == "RM" or len(per[f]) <= a.sample_refs or k in set(random.Random(f"0:{f}").sample(range(len(per[f])), a.sample_refs))]  # fmt: skip
    if a.limit:
        jobs = [j for f in a.words for j in per[f][: a.limit]]
    print(f"{len(prompts)} eligible prompts; {len(jobs)} jobs; by word {dict(collections.Counter(j['family'] for j in jobs))}; "
          f"by relation {dict(collections.Counter(j['rel'] for j in jobs))}; bands {[f'{b[0]}-{b[-1]}' for b in bands]}; conditions {conds}", flush=True)  # fmt: skip
    lens = JLens(model, pins.FROZEN_LENS)
    rows, t0 = [], time.time()
    ans_tok = answer_tokens(tok, items)
    for band in bands:
        run_band(a, model, tok, lens, items, jobs, band, conds, f"L{band[0]}-{band[-1]}", rows, t0, ans_tok)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summ = {}
    for tag in sorted({r["band"] for r in rows}):
        summ.update({f"{tag}/{k}": v for k, v in JS.score([r for r in rows if r["band"] == tag]).items()})
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for k, cell in summ.items():
        if cell.get("n"):
            print(f"{k:34s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}  other {cell['other']:5.1f}"
                  f"  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", default=None)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    ap.add_argument("--words", nargs="+", default=["RM", "MM", "PM"])
    ap.add_argument("--site", choices=["last", "span", "qmark", "final"], default="last")
    ap.add_argument("--ks", nargs="+", type=int, default=[10])
    ap.add_argument("--conds", nargs="+", default=None)
    ap.add_argument("--sweep", nargs="+", default=None, help="layer windows, e.g. 4-8 8-12 (one run per window)")
    ap.add_argument("--sample-per-word", type=int, default=0)
    ap.add_argument("--sample-refs", type=int, default=0, help="note 10: cap every word but RM at N (seeded)")
    ap.add_argument("--scene-words", nargs="+", default=None, help="note 10: eligibility words (default note 4's V3 scene words)")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0, help="note 11: 0 = notes 9-10's donors; s > 0 draws donors with random.Random('s:' + id)")
    ap.add_argument("--items", choices=["eligible", "fail", "v4ok", "v4fail"], default="eligible",
                    help="note 11: fail = composition failures (RM); note 14: v4ok / v4fail = v4's gate")  # fmt: skip
    ap.add_argument("--cv-h1", default=None, help="note 14: the competence_variants run on v4's H1 (closed-book hop 1)")
    ap.add_argument("--value-swap", action="store_true", help="note 17: the donor prompt keeps the question about X and gives X another passage value")
    ap.add_argument("--position-swap", action="store_true", help="note 18: the donor prompt keeps the question; X's fact sentence trades places with Z's")
    ap.add_argument("--report", action="store_true", help="note 21: the hop-1 question over the same passage (the bridge is said)")
    ap.add_argument("--resample", action="store_true", help="note 19: the donor is another passage's own question, about a person absent from X's passage")
    a = ap.parse_args()
    assert a.band or a.sweep, "--band or --sweep"
    main(a)
