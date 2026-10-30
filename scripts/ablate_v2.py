"""ablate_v2: the J-space knock-out, version 2 (Zach, 2026-10-20). Removals and controls are in
src/bridge_jspace/ablate.py (decided with Zach on 2026-10-20); one model load runs every band x condition on every
prompt, sharing the unedited forward. TF32 is on for the OMP's matmuls (benchmark 2026-10-20: 5.1x, same atoms).
--positions restricts every condition to the facts (context) or to the question and after (question).

Plans (--plan):
  v1check   ablate_pilot v1's configuration (layers 32/36/40, the lens dictionary and v1's Gaussian random dictionary,
            v1's prompts) run with this code; compared item by item with results/ablate_pilot/v1
  depth     contiguous 3-layer bands sliding by 2 over layers 0 to n-2, and every one of those layers at once
  bands     the bands given with --bands, e.g. "32,36,40" "16-28"
Conditions (--conditions): omp25, omp25_rot, omp25_rdict, paper10, paper10_rot, paper10_rdict, keep_own, skip_subject,
  gauss (v1's Gaussian dictionary); 2026-10-21 (C1's second kill test, decided with Zach): paper10_keepown and
  paper10_keepown_rot, paper10 with the bridge's own-word directions (its surface tokens and every dictionary row with
  cosine >= OWN_COS to its concept token, as keep_own) also protected. 2026-10-21 (the specificity control, decided with
  Zach after the pipeline review): unembed10 and unembed10_rot, paper10's procedure over the unit unembedding rows of
  letter tokens (the final norm's gain folded in: the logit lens's directions, the same at every layer) instead of the
  J-lens vectors: is the damage specific to the J-space, or shared by any token-aligned directions? 2026-10-21
  (docs/prereg_sink_1021.md): any top-K condition with "_nosink" before its control suffix (paper10_nosink,
  paper10_nosink_rot, unembed10_nosink, top5_nosink_rot, paper10_keepown_nosink, ...) leaves attention-sink positions
  unedited: position 0 and every position whose residual norm exceeds 10x the prompt's median. Prompt kinds (--kinds): clean (the whole question), hop (the last step alone, as
  v1), step1/step2/step3 (each step alone). Reported per band x family/kind x condition: accuracy (top token = the
  answer's first token) and the mean change in the answer token's log-probability from the unedited run.

A new target (BJ_TARGET; 2026-10-21, Gemma 4 31B-it): --competence names its suite_v1 competence run (eligibility for
BL BR RL RR) and --countries-build draws its country cases with this model (exp09's eligibility); a lens fit at some
layers only takes --plan bands with those layers ("30,33,36").

python scripts/ablate_v2.py --name N --why W --plan depth [--n 100] [--families BL BR RL RR R B] [--kinds clean]
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.ablate import (
    OWN_COS,
    LensDictionary,
    MatrixDictionary,
    RotatedDictionary,
    RowSettings,
    first_token_logits,
    removal_edit,
    rotation,
)
from scripts import ablate_pilot as A
from scripts import control_split as C
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S

RESULTS = pins.RESULTS_DIR / "ablate_v2"
COMPETENCE = {  # the 27B's competence runs per suite family (eligibility: every check right)
    "BL": "competence_v2", "BR": "competence_v2", "RL": "competence_v2", "RR": "competence_v2",
    "BLR": "competence_tiebreak_v1", "BRL": "competence_tiebreak_v1",
    "TYPO": "competence_computed_v1", "TRANS": "competence_computed_v1",
    "TBL": "competence_tool_v1", "TBR": "competence_tool_v1",
}  # fmt: skip
CONDITIONS = ("omp25", "omp25_rot", "omp25_rdict", "paper10", "paper10_rot", "paper10_rdict", "keep_own",
              "skip_subject", "gauss", "unembed10", "unembed10_rot", "pca10", "paper10_pcasize",
              "ansJ", "ansJ_rot", "ansU", "ansU_rot",  # ans*: amendment 58 note 3
              "paper10_keepA", "paper10_keepA_rot",  # amendment 64 note 37: paper10's r minus its part in the answers' J++ span
              "paper10_keepR", "paper10_keepR_rot", "paper10_keepR2", "paper10_keepR2_rot", "paper10_keepR4",
              "paper10_keepR4_rot", "ansR", "ansR_rot",  # amendment 67 note 41 + addendum: random kept / removed spans
              "paper10_keepCap", "paper10_keepCty", "paper10_keepCapCty", "paper10_keepRcap", "ansCap", "ansCty",
              "ansCty_rot",  # fmt: skip  # amendment 68 note 44: capitals vs countries (jsuite_v5kn2c MC0)
              "ansRk", "ansRk_rot",  # fmt: skip  # amendment 72 note 50: random rows as many as ansJ's (cands2)
              "ansRe", "ansRe_rot")  # fmt: skip  # amendment 78 note 57: random rows energy-matched to ansJ's removal
# amendment 72 notes 49, 50, 52 (paper10_*: the protections, keeps and onlyA, each + _rot except note 52's) and note 51
# (topK_keepA / _rot): see n49_kind, is_n52, is_n51 and the docstring of main's "amendment 72" block
N49_KINDS = ("protF", "protC", "keepT10", "keepRT10", "keepOwn", "keepSib", "keepR4perp", "keepR8perp", "onlyA")
N52_KEEPS = ("CapPerp", "CtyPerp", "Shared")
N52B_KEEPS = ("RShared", "RCapPerp", "RCtyPerp", "SharedNoLit")  # amendment 80 note 52b: energy-matched random twins; Shared minus literal rows
PERP_TOL = 1e-3  # note 50 / 52: a re-orthonormalised column whose norm after projection is below this is dropped
SHARED_COS = 0.9  # note 52: keepShared = the principal vectors of span(Cap) and span(Cty) with cosine >= this
SEED_ROT, SEED_DICT, SEED_GAUSS = 888, 999, 777  # + layer (888 and 777 as ablate_pilot)
KEEPA_ROWS = {"every": "forms", "cands2": "cands2"}  # note 37's kept span: every form, or ansJ's rows (cands2) only
RAND_MULT = {"R": 1, "R2": 2, "R4": 4}  # note 41: random kept spans of 1x, 2x, 4x A's row count, nested (R in R2 in R4)


def keep_kind(cond: str) -> str | None:
    """The kept span of a paper10_keep* condition: A (note 37) or R, R2, R4 (note 41); None for any other condition."""
    m = re.fullmatch(r"paper10_keep(A|R|R2|R4|Cap|Cty|CapCty|Rcap)(_rot)?", cond)  # Cap ... Rcap: amendment 68 note 44
    if m:
        return m[1]
    # amendment 72: note 49's T10 / RT10 / Own / Sib, note 50's perps, note 52's residualised spans, note 51's topK_keepA
    m = re.fullmatch(r"paper10_keep(T10|RT10|Own|Sib|R4perp|R8perp|CapPerp|CtyPerp|Shared|RShared|RCapPerp|RCtyPerp|SharedNoLit)(_rot)?", cond) or re.fullmatch(
        r"top\d+_keep(A)(_rot)?", cond)
    if m:
        return m[1]
    # amendment 78 note 57: the rivals' spans and the energy-matched random keep at dose K
    m = re.fullmatch(r"paper10_keep(Rivals|RandRivals)(_rot)?", cond) or re.fullmatch(r"top\d+_keep(RE)(_rot)?", cond)
    return m[1] if m else None


def n57_kind(cond: str) -> str | None:
    """Amendment 78 note 57: onlyRperp, keepRivals, keepRandRivals (paper10_X / _rot), keepRE (topK_keepRE / _rot), ansRe (/ _rot)."""
    if cond in ("ansRe", "ansRe_rot"):
        return "ansRe"
    m = re.fullmatch(r"paper10_(onlyRperp|keepRivals|keepRandRivals)(_rot)?", cond) or re.fullmatch(r"top\d+_(keepRE)(_rot)?", cond)
    return m[1] if m else None


def n49_kind(cond: str) -> str | None:
    """Amendment 72 notes 49 / 50: protF, protC, keepT10, keepRT10, keepOwn, keepSib, keepR4perp, keepR8perp, onlyA (each
    paper10_X or paper10_X_rot), and "ansRk" for ansRk / ansRk_rot; None for any other condition."""
    if cond in ("ansRk", "ansRk_rot"):
        return "ansRk"
    m = re.fullmatch(r"paper10_(" + "|".join(N49_KINDS) + r")(_rot)?", cond)
    return m[1] if m else None


def is_n51(cond: str) -> bool:
    """Amendment 72 note 51: topK_keepA / topK_keepA_rot (topK's removal, paper10's protection, A's span kept)."""
    return re.fullmatch(r"top\d+_keepA(_rot)?", cond) is not None


def is_n52(cond: str) -> bool:
    """Amendment 72 note 52: paper10_keepCapPerp / keepCtyPerp / keepShared (note 44's spans residualised); amendment 80 note 52b:
    paper10_keepRShared / keepRCapPerp / keepRCtyPerp (random keeps energy-matched to each span in paper10's forward, the first k
    rows of note 44's Rcap pool) and paper10_keepSharedNoLit."""
    return keep_kind(cond) in N52_KEEPS + N52B_KEEPS


def is_n44(cond: str) -> bool:
    """Note 44's conditions: paper10_keepCap / Cty / CapCty / Rcap (+ _rot) and ansCap / ansCty (+ _rot)."""
    return keep_kind(cond) in ("Cap", "Cty", "CapCty", "Rcap") or re.fullmatch(r"ans(Cap|Cty)(_rot)?", cond) is not None


N44_SAY_SET = "jsuite_v5kn2_test_chat"  # note 44: the countries are kn2's say vocabulary (its MM answer_vocab)


def n44_values() -> tuple[list[str], list[str]]:
    """Note 44's capitals (note 35's table, scripts/jsuite_v5key.CAPITAL, and CAPITAL_ALIASES) and countries (kn2's say
    vocabulary), sorted."""
    from scripts import jsuite_v5key as K5
    from scripts import tasks_v2 as T

    caps = set(K5.CAPITAL.values()) | {x for v in K5.CAPITAL_ALIASES.values() for x in v}
    ctys = {v for it in T.load(N44_SAY_SET) if it["word"] == "MM" for v in it["answer_vocab"]}
    return sorted(caps), sorted(ctys)


def n44_subsample(item_id: str, rows: list[int], n: int) -> list[int]:
    """Note 44: keepCty's rows count-matched to keepCap's, random.Random("n44:" + item id).sample(rows, n), sorted (all of
    them if there are no more than n)."""
    import random

    return sorted(rows) if len(rows) <= n else sorted(random.Random("n44:" + item_id).sample(rows, n))


def is_rand(cond: str) -> bool:
    """Note 41's conditions on the random rows: paper10_keepR / R2 / R4 (+ _rot) and ansR (+ _rot)."""
    return keep_kind(cond) in RAND_MULT or cond in ("ansR", "ansR_rot")


def random_rows(item_id: str, n: int, n_dict: int, exclude: set[int]) -> list[int]:
    """Amendment 67 note 41 (+ addendum): 4n letter-token dictionary rows drawn with random.Random("n41:" + item id) from
    the rows not in exclude (A's rows and the protected rows), in draw order; R = the first n, R2 the first 2n, R4 all."""
    import random

    pool = [i for i in range(n_dict) if i not in exclude]
    return random.Random("n41:" + item_id).sample(pool, 4 * n)


def forms45(word: str) -> list[str]:
    """Note 45's forms of a word (scripts/paper_ko_decomp.forms): as written, lower case, capitalised; with and without a
    leading space."""
    cases = dict.fromkeys([word, word.lower(), word[:1].upper() + word[1:]])
    return [p + c for c in cases for p in ("", " ")]


def first_token_ids(tok, word: str) -> set[int]:
    """Amendment 72 note 49 (note 45's rule): the first token of every form of the word, whitespace-only tokens dropped."""
    out = set()
    for f in forms45(word):
        ids = tok(f, add_special_tokens=False).input_ids
        if ids and tok.decode([ids[0]]).strip():
            out.add(ids[0])
    return out


def perp_basis(Q: torch.Tensor, V: torch.Tensor) -> torch.Tensor:
    """Amendment 72 notes 50 / 52: an orthonormal basis [d, r] of span(V's rows) projected off span(Q) (Q [d, k]
    orthonormal) and re-orthonormalised: Gram-Schmidt by one QR of [Q | V^T]; a column whose norm after projection off Q
    and the earlier columns (|R_jj|) is below PERP_TOL is dropped (r = the rank logged)."""
    k = Q.shape[1]
    q, r = torch.linalg.qr(torch.cat([Q.double(), V.double().T], 1))
    keep = r.diagonal()[k:].abs() >= PERP_TOL
    return q[:, k:][:, keep].contiguous()


def shared_basis(Qa: torch.Tensor, Qb: torch.Tensor) -> tuple[torch.Tensor, list[float]]:
    """Amendment 72 note 52: span(a) ∩ span(b) estimated as the principal vectors (Qa u_i, Qb v_i) with cosine s_i >=
    SHARED_COS, each pair's normalised bisector (orthonormal across i); and every principal cosine >= SHARED_COS."""
    U, S_, Vh = torch.linalg.svd(Qa.T.double() @ Qb.double(), full_matrices=False)
    sel = S_ >= SHARED_COS
    B = Qa.double() @ U[:, sel] + Qb.double() @ Vh.T[:, sel]
    return (B / B.norm(dim=0, keepdim=True)).contiguous(), [round(float(x), 4) for x in S_[sel]]


class LazySpans:
    """Amendment 72: per-row kept spans built when removal_edit iterates over them (inside the forward), so the large
    note 50 / 52 bases (up to [d, 8|A|] per row and layer) are never all held at once."""

    def __init__(self, fn, n: int):
        self.fn, self.n = fn, n

    def __iter__(self):
        return (self.fn(i) for i in range(self.n))


def measured(inner, emask: torch.Tensor, acc: torch.Tensor):
    """Amendment 72 (shared logging, every condition): wraps an edit to log |edit| / |h|: per batch row b, acc[b] +=
    [sum over b's edited positions of |edit(h) - h|^2, the same sum of |h|^2] at each layer call; the row's edit_rel is
    acc[b, 0] / acc[b, 1] (summed over the band's layers). The edit's output is returned unchanged (the same tensor)."""

    def edit(h: torch.Tensor) -> torch.Tensor:
        out = inner(h)
        x = h.float()
        m = emask[:, : x.shape[1]].double()
        acc[:, 0] += ((x - out.reshape(x.shape)).double().pow(2).sum(-1) * m).sum(1)
        acc[:, 1] += (x.double().pow(2).sum(-1) * m).sum(1)
        return out

    if hasattr(inner, "sinks"):  # _nosink conditions: the same counter list
        edit.sinks = inner.sinks
    return edit


def suite_prompts(tok, fams: list[str], kinds: list[str], n: int, competence: dict[str, str], skip: int = 0,
                  wording: str = "A") -> list[dict]:  # fmt: skip
    """The first n eligible items per family after the first `skip` (a fresh sample of the same set), in a wording."""
    out = []
    for fam in fams:
        good = A.eligible_ids(competence[fam], (fam,)).get(fam, set())
        got, skipped = 0, 0
        for it in S.load(fam, wording):
            if got >= n or it["id"] not in good:
                continue
            try:
                prep = P.prepare(it, tok)
            except AssertionError:  # C or O not aligned in this tokenizer (as v1)
                continue
            if skipped < skip:
                skipped += 1
                continue
            got += 1
            for kind in kinds:
                if kind == "clean":
                    out.append({"family": fam, "id": it["id"], "kind": "clean", "ids": prep["read_ids"]["clean"],
                                "tok": prep["tok_A"], "bridge": it["bridge"]})  # fmt: skip
                    continue
                key = ("hop3" if "hop3" in it else "hop2") if kind == "hop" else "hop" + kind.removeprefix("step")
                if key not in it:
                    continue
                hop = it[key]
                text = S.render(tok, hop.get("context", it["context"]), hop["question"])
                ids = S.ids(tok, text) + (S.ids(tok, " ") if hop["kind"] == "digit" else [])
                out.append({"family": fam, "id": it["id"], "kind": kind, "ids": ids,
                            "tok": S.answer_token(tok, hop["answer"], hop["kind"]), "bridge": it["bridge"]})  # fmt: skip
    return out


def country_prompts(tok, fams: list[str], n: int, skip: int = 0) -> list[dict]:
    """ablate_pilot v1's country prompts (map_v1's cases, chat_prefill), whole question only."""
    picked = [json.loads(line)["id"] for line in (C.RESULTS / "map_v1" / "cases.jsonl").read_text().splitlines()]
    items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(items)}
    seen: collections.Counter = collections.Counter()
    out = []
    for uid in picked:
        index, item = by_uid[uid]
        if item["family"] not in fams or seen[item["family"]] >= n + skip:
            continue
        seen[item["family"]] += 1
        if seen[item["family"]] <= skip:
            continue
        prep = E.prepare(item, index, tok, "chat_prefill")
        out.append({"family": f"country-{item['family']}", "id": uid, "kind": "clean", "ids": prep["ids"]["clean"],
                    "tok": S.answer_token(tok, item["answer"], "word"), "bridge": item["bridge"]})  # fmt: skip
    return out


def built_country_prompts(model, tok, fams: list[str], n: int) -> list[dict]:
    """A new target's country prompts (no map run): exp09's eligibility generated now with this model
    (control_split.build_cases, as ablate_pilot --countries-build and read_write --from-competence), whole question."""
    return [
        {"family": f"country-{c['family']}", "id": c["id"], "kind": "clean", "ids": c["ids"]["clean"], "tok": c["tok_A"],
         "bridge": c["bridge"]}
        for c in C.build_cases(model, tok, n)[0]
        if c["family"] in fams
    ]  # fmt: skip


def tasks_prompts(tok, set_name: str, comp_run: str, words: list[str] | None, n: int, kinds: list[str],
                  level: str = "pick", strata: tuple[str, ...] = ("core",), per_word: bool = False,
                  scene_words: list[str] | None = None) -> list[dict]:  # fmt: skip
    """tasks_v2 items of the compared words (--tasks-words) from scenes the model gets right on them throughout, at
    one level for the comparison (tasks_v2.eligible), first n per word; the whole question ('clean') and each step
    alone ('stepN'), each with its own instruction, read as the suite reads them (a digit after 'Answer: ')."""
    from scripts import tasks_v2 as T

    assert words, "--tasks-words: name the compared words (they set the level and the eligibility)"
    out = []
    for it in T.eligible(set_name, comp_run, words, n, level, strata=tuple(strata), per_word=per_word, scene_words=scene_words):
        parts = [("clean", it["question"], it["answer"], it["kind"])]
        parts += [(f"step{i}", st["question"], st["answer"], st["kind"]) for i, st in enumerate(it["steps"], 1)]
        for kind, q, a, k in parts:
            if kind not in kinds:
                continue
            ids = S.ids(tok, T.render(tok, {**it, "_question": q, "_kind": k})) + (
                S.ids(tok, " ") if k == "digit" else []
            )
            out.append({"family": it["word"], "id": it["id"], "kind": kind, "ids": ids, "tok": S.answer_token(tok, a, k),
                        "bridge": it["steps"][0]["answer"], "domain": it["domain"], "format": it["format"], "desc": it.get("start_desc")})  # fmt: skip
            if "framing" in it:  # natural_v1 (2026-10-23): the read's candidates, its relation's answers (bridges for hop 1)
                own = it["steps"][int(kind[4:]) - 1].get("cand_vocab") if kind.startswith("step") else it.get("answer_vocab")
                vocab = own or natural_vocab(set_name)[(it["domain"], "bridge" if kind == "step1" else "answer")]  # natural3: own
                out[-1]["cands"] = sorted({S.answer_token(tok, v, k) for v in vocab} | {out[-1]["tok"]})
                # cand2 (2026-10-23, amendment 20): candidates in either case, and hop 1's other names for the bridge
                both = lambda v, k=k: {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k)}  # noqa: E731
                ok2 = both(a) | ({t for x in it["steps"][0].get("alts", []) for t in both(x)} if kind == "step1" else set())
                out[-1]["ok2"] = sorted(ok2)
                out[-1]["cands2"] = sorted({t for v in vocab for t in both(v)} | ok2)
                # forms (amendment 64 note 37, paper10_keepA's span): cands2 plus the same answers' first tokens with a
                # leading space, either case (note 35's "any form"); used by --keepA-forms every only
                sp = lambda v: {S.ids(tok, " " + v)[0], S.ids(tok, " " + v.lower())[0]}  # noqa: E731
                src = set(vocab) | {a} | (set(it["steps"][0].get("alts", [])) if kind == "step1" else set())
                out[-1]["forms"] = sorted(set(out[-1]["cands2"]) | {t for v in src for t in sp(v)})
    return out


_NATURAL_VOCAB: dict = {}


def natural_vocab(set_name: str) -> dict:
    """natural_v1 sets: per relation (domain), every answer and every bridge (with a person's first name) in the set."""
    if set_name not in _NATURAL_VOCAB:
        from scripts import natural_v1 as N
        from scripts import tasks_v2 as T

        v: dict = {}
        for it in T.load(set_name):
            v.setdefault((it["domain"], "answer"), set()).add(it["answer"])
            v.setdefault((it["domain"], "bridge"), set()).update(it["steps"][0].get("alts", [it["bridge"]]))
        for (dom, kind), vals in list(v.items()):
            if kind == "bridge":
                vals |= {N.FIRST_NAMES.get(x, x) for x in vals}
        _NATURAL_VOCAB[set_name] = v
    return _NATURAL_VOCAB[set_name]


def answertype_prompts(tok, n: int) -> list[dict]:
    """tool_answer_type's JSON scenes (seed 602): one context, asked for the pet's vet (a name: AT-name) and its
    locker (a digit: AT-digit), the whole question only; not filtered by competence (read accuracy on the items right
    unedited, from the rows' 'none' condition)."""
    from scripts import tool_answer_type as TA

    out = []
    for sc in TA.scenes(tok, n):
        for q, fam in (("name_clean", "AT-name"), ("digit_clean", "AT-digit")):
            text, ans, kind = sc["questions"][q]
            ids = S.ids(tok, S.render(tok, sc["context"], text)) + (S.ids(tok, " ") if kind == "digit" else [])
            out.append({"family": fam, "id": sc["scene"], "kind": "clean", "ids": ids,
                        "tok": S.answer_token(tok, ans, kind), "bridge": sc["bridge"]})  # fmt: skip
    return out


def reads(logits, p: dict, read: str) -> dict:
    """correct: the answer's first token is the top token ("top", every run before 2026-10-23) or, for prompts with
    candidates (natural_v1), the top among its relation's candidate answers ("cand": format tokens cannot fail it).
    Both are recorded when the prompt has candidates. "cand2" (2026-10-23, amendment 20): the candidates in either case,
    right if the top is any form of the answer (and, for hop 1, of the bridge's other names); all three are recorded."""
    top_id = int(logits.argmax())
    top = top_id == p["tok"]
    if "cands" not in p:
        return {"correct": top, "top_id": top_id}
    c = torch.tensor(p["cands"], device=logits.device)
    cand = int(c[logits[c].argmax()]) == p["tok"]
    c2 = torch.tensor(p["cands2"], device=logits.device)
    pick2 = int(c2[logits[c2].argmax()])
    cand2 = pick2 in p["ok2"]
    # top_id / pick2 (2026-10-24, the dataset audit): the top token and the candidate reads pick, so a knock-outs wrong
    # answers can be sorted into passage lures, priors and other candidates afterwards
    return {"correct": {"top": top, "cand": cand, "cand2": cand2}[read], "correct_top": top, "correct_cand": cand,
            "correct_cand2": cand2, "top_id": top_id, "pick2": pick2}  # fmt: skip


def bridge_positions(tok, ids: list[int], word: str) -> list[int]:
    """Token positions overlapping a mention of the word (case-insensitive, any suffix: cow, cows, Cow)."""
    pieces = [tok.decode([i]) for i in ids]
    starts, pos = [], 0
    for p in pieces:
        starts.append(pos)
        pos += len(p)
    text = "".join(pieces)
    spans = [(m.start(), m.end()) for m in re.finditer(r"(?i)\b" + re.escape(word), text)]
    return [
        i
        for i, (s, p) in enumerate(zip(starts, pieces, strict=True))
        if any(s < e and s + len(p) > b for b, e in spans)
    ]


def question_start(tok, ids: list[int]) -> int:
    """The first token of the prompt's question: the sentence ending in the user turn's last '?' (it starts after the
    last '. ' or line break before it). Positions from here on (question, instruction, template, 'Answer:') are the
    'question' set of --positions; earlier ones (template prefix, the facts) are 'context'."""
    pieces = [tok.decode([i]) for i in ids]
    starts, pos = [], 0
    for piece in pieces:
        starts.append(pos)
        pos += len(piece)
    text = "".join(pieces)
    end = text.rfind("<|im_end|>")  # Qwen's end of the user turn; another template's prompt: its last '?' (2026-10-21)
    q_end = text.rindex("?", 0, end if end >= 0 else len(text))
    q_start = max(text.rfind(". ", 0, q_end) + 2, text.rfind("\n", 0, q_end) + 1)
    return next(i for i, s in enumerate(starts) if s + len(pieces[i]) > q_start)


def outside_positions(mode: str, n: int, q0: int, bridge_pos: list[int], desc_pos: list[int] | None = None) -> list[int]:
    """Positions a removal leaves unedited under --positions: all (none), context (the question on), question (before
    it), final (every position but the last, the answer position; 2026-10-24) or bridge (every position but the
    bridge's mentions; a prompt that never names its bridge, e.g. a recalled start, is left unedited; 2026-10-24) or desc
    (amendment 61 note 33: every position but the question's description of the bridge, start_desc; none found: unedited)."""
    keep = set(bridge_pos)
    if mode == "desc":
        d = set(desc_pos or [])
        return [i for i in range(n) if i not in d]
    return {"all": [], "context": list(range(q0, n)), "question": list(range(q0)), "final": list(range(n - 1)),
            "bridge": [i for i in range(n) if i not in keep]}[mode]  # fmt: skip


def make_bands(plan: str, n_layers: int, spec: list[str], workspace: int | None = None) -> list[tuple[int, ...]]:
    if plan == "v1check":
        return [(32, 36, 40)]
    if (
        plan == "coarse"
    ):  # 9 contiguous layers sliding by 4, and every layer (Zach, 2026-10-20: coarse first, then zoom)
        top = n_layers - 2
        return [tuple(range(s, s + 9)) for s in range(0, top - 7, 4)] + [tuple(range(0, top + 1))]
    if plan == "depth":
        top = n_layers - 2  # the last edited layer; the final block is the lens's target
        bands = [tuple(range(s, s + 3)) for s in range(0, top - 1, 2)]  # 3 contiguous layers, sliding by 2
        bands += [tuple(range(s, s + 9)) for s in range(0, top - 7, 4)]  # 9 contiguous layers, sliding by 4
        bands.append(tuple(range(0, top + 1)))  # every layer
        if workspace is not None:  # every layer from the first where the lens mostly stops reading the input token
            bands.append(tuple(range(workspace, top + 1)))
        return bands
    bands = []
    for b in spec:
        if "-" in b:
            lo, hi = map(int, b.split("-"))
            bands.append(tuple(range(lo, hi + 1)))
        else:
            bands.append(tuple(int(x) for x in b.split(",")))
    return bands


WIDE = 9  # bands wider than this run paper10 and its controls only (Zach, 2026-10-20: OMP at whole depth breaks
#           everything, its random controls too, so it says nothing there)


def top_k(cond: str) -> int | None:
    """K of a top-K condition: paper10 or unembed10 (K = 10) or topK, with any control suffix; None for OMP and others."""
    if cond.startswith("paper10"):
        return 10
    # topK: the J-lens dictionary; unembedK (2026-10-22, the size-matched specificity control): the unembedding rows
    m = re.fullmatch(r"(?:top|unembed|pca)(\d+)(_nosink)?(_rot|_rdict|_pcasize)?", cond)  # _pcasize: amendment 54
    if m:
        return int(m[1])
    m = re.fullmatch(r"top(\d+)_keepA(_rot)?", cond)  # amendment 72 note 51: topK with A's span kept (paper10's protection)
    if m:
        return int(m[1])
    m = re.fullmatch(r"top(\d+)_keepRE(_rot)?", cond)  # amendment 78 note 57: topK with an energy-matched random span kept
    return int(m[1]) if m else None


PCA_ROWS, PCA_K = 64, 256


@torch.no_grad()
def pca_dictionaries(model, layers) -> dict:
    """pca10 (2026-10-25, the TA's variance control): at each layer, the top PCA_K principal directions of the block's
    output over the first PCA_ROWS pinned WikiText rows of >= 64 words (128 tokens, as the harness encodes raw text;
    centred), each with both signs, as a MatrixDictionary. Its top-10 removal takes, at each position, the span of the
    10 principal directions with the largest projection there (paper10's per-position selection, over the residual's
    own highest-variance directions instead of the lens's)."""
    from bridge_jspace import tokens

    rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64][:PCA_ROWS]
    acts = {la: [] for la in layers}
    for r in rows:
        ids = torch.tensor([tokens.raw_encoding(model.tokenizer, r)["input_ids"][:128]], device="cuda")
        _, rec = model.run(ids, record=tuple(layers))
        for la in layers:
            acts[la].append(rec[la][1:])  # the first position (BOS / sink) left out
    out = {}
    for la in layers:
        X = torch.cat(acts[la]).double()
        X = X - X.mean(0, keepdim=True)
        _, _, V = torch.linalg.svd(X, full_matrices=False)
        P = V[:PCA_K].float()
        out[la] = MatrixDictionary(torch.cat([P, -P]))
    print(f"pca10: top {PCA_K} principal directions per layer from {len(rows)} WikiText rows", flush=True)
    return out


def conditions_for(band: tuple[int, ...], conditions: list[str]) -> list[str]:
    return [c for c in conditions if len(band) <= WIDE or top_k(c) is not None]


def answer_span_edit(D, rows: list[torch.Tensor], outside: list[list[int]], rotation: torch.Tensor | None = None):
    """Amendment 58 note 3 (Zach, 2026-10-27): at every edited position of batch row b, remove the projection onto the
    span of D's unit vectors for rows[b] (the item's candidate answers' first tokens, both cases: its cands2), the
    same span at every position; with rotation, the removal vector is turned by it (the same-size control).
    Positions in outside[b] are unchanged."""
    bases = []
    for r in rows:
        A = D.atoms(r).double()  # [k, d]
        Q, _ = torch.linalg.qr(A.T)  # [d, k], orthonormal columns spanning the candidates' directions
        bases.append(Q)

    def edit(h: torch.Tensor) -> torch.Tensor:
        out = h.float().clone()
        for b, Q in enumerate(bases):
            x = out[b].double()
            r = (x @ Q) @ Q.T
            if outside[b]:
                r[torch.tensor(outside[b], device=h.device)] = 0
            if rotation is not None:
                r = r @ rotation.double().T
            out[b] = (x - r).float()
        return out

    return edit


def label(band: tuple[int, ...]) -> str:
    contiguous = band == tuple(range(band[0], band[-1] + 1))
    return f"L{band[0]}-{band[-1]}" if contiguous and len(band) > 1 else "L" + ",".join(map(str, band))


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    torch.backends.cuda.matmul.allow_tf32 = not args.no_tf32
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    bands = make_bands(args.plan, pins.N_LAYERS, args.bands, args.workspace)
    manifest = {"run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "git_commit": commit, "git_state": pins.git_state(), "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "plan": args.plan, "bands": [label(b) for b in bands], "conditions": args.conditions,
                "families": args.families, "kinds": args.kinds, "skip": args.skip, "wording": args.wording, "n_per_family": args.n, "batch": args.batch,
                "tf32": not args.no_tf32, "workspace_start": args.workspace, "positions": args.positions, "pad": args.pad, "competence": args.competence, "countries_build": args.countries_build, "tasks": [args.tasks, args.tasks_competence, args.tasks_words, args.tasks_level, args.tasks_strata], "tasks_per_word": args.tasks_per_word, "tasks_scene_words": args.tasks_scene_words, "read": args.read, "sample_per_word": args.sample_per_word, "sample_seed": args.sample_seed, "dict_digits": args.dict_digits, "wide": WIDE, "seed_offset": args.seed_offset, "seeds": {"rotation": f"{SEED_ROT + args.seed_offset}+layer", "rotated_dictionary": f"{SEED_DICT + args.seed_offset}+layer",
                "gauss": f"{SEED_GAUSS}+layer"}, "own_cos": OWN_COS, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    if any(keep_kind(c) or is_rand(c) for c in args.conditions):  # amendment 64 note 37; amendment 67 note 41
        manifest["keepA_forms"] = args.keepA_forms
    if any(is_rand(c) for c in args.conditions):
        manifest["n41_random_rows"] = ('random.Random("n41:" + id).sample(letter-token rows minus A\'s rows minus the protected '
                                       "rows, 4 |A|), in draw order: R = the first |A|, R2 the first 2 |A|, R4 all (rand_rows.jsonl)")
    if any(is_n44(c) for c in args.conditions):
        manifest["n44_spans"] = ("Cap: every form of every capital in jsuite_v5key.CAPITAL / CAPITAL_ALIASES; Cty: every form of every "
                                 f"country in {N44_SAY_SET}'s MM answer_vocab, count-matched to Cap by random.Random(\"n44:\" + id).sample; "
                                 "CapCty: their union; Rcap: random.Random(\"n41:\" + id).sample(letter rows minus Cap's minus the "
                                 "protected, 4 |Cap|), its shortest prefix whose share of paper10's removal energy is >= Cap's (n44_spans.json, "
                                 "n44_rows.jsonl, paper10 rows' retained44)")  # fmt: skip
    if any(n49_kind(c) or is_n51(c) or is_n52(c) for c in args.conditions):  # amendment 72 notes 49-52
        manifest["amendment72"] = {
            "protF": "protected = paper10's (clean top-10 letter rows) + the letter rows of the first token of every form (note 45: "
                     "stripped decode as written, lower, capitalised; with and without a leading space) of each clean top-10 token",
            "protC": f"protF + every letter row with cosine >= {OWN_COS} to a clean top-10 letter token's atom at that layer",
            "keepT10": "keep_span = QR of the unit J++ vectors of protF's rows (the top-10's own rows + added forms)",
            "keepRT10": 'random.Random("n49:" + id).sample(letter rows minus protF\'s rows, |T10 rows|)',
            "keepOwn": "every form of the item's own answer (note 37's forms: as read and lower case; leading space, either case)",
            "keepSib": 'one sibling answer of the relation (answer_vocab), letter rows disjoint from Own\'s, row count matched (closest if '
                       'none), random.Random("n49sib:" + id).choice(sorted candidates)',
            "R4perp_R8perp": 'note 41\'s rows (random.Random("n41:" + id); R8 = the 8|A| draw, its first 4|A| = R4, asserted), each '
                             f"projected off span(A) per layer and re-orthonormalised (one QR of [Q_A | V]; |R_jj| < {PERP_TOL} dropped)",
            "onlyA": "r' = P_A r under paper10's protection (+ _rot: turned by the same rotation)",
            "ansRk": 'answer_span_edit over random.Random("n50:" + id).sample(letter rows minus A\'s rows, |cands2 rows|)',
            "topK_keepA": "topK's removal (paper10's protection: the clean top-10 letter rows) minus its part in span(A)",
            "CapPerp_CtyPerp": "note 44's Cap span projected off the item's Cty span per layer (and the reverse), as R4perp",
            "Shared": f"bisectors of the principal vectors of span(Cap) and span(Cty) with cosine >= {SHARED_COS}",
            "keeplog": "keeplog.jsonl: per item, in paper10's (and topK's) forward, summed over the band's layers and edited positions: "
                       "E_X = sum |P_X r|^2 / sum |r|^2 for each keep; alpha_X = 1 - sum |P_A (r - P_X r)|^2 / sum |P_A r|^2; for "
                       "protF / protC (their removal r_X recomputed on paper10's residuals) E_X = 1 - sum <r, r_X> / sum |r|^2 and the "
                       "share of paper10's answer part they still remove, sum |P_A r_X|^2 / sum |P_A r|^2; ranks; |edit| / |h|. The new "
                       "conditions' rows carry keeplog: |edit| / |h| in their own forward and the kept rank / protected row count",
            "topk_chunk": args.topk_chunk,
            **({"note52b": "keepRShared / RCapPerp / RCtyPerp: the first k rows of note 44's Rcap pool (random.Random(\"n41:\" + id), "
                           "4 |Cap| rows, nested QR), k per item = the smallest prefix whose share of paper10's removal energy reaches the "
                           "span's (paper10's forward; keeplog k52b, E_R*); keepSharedNoLit: Shared projected off the item's rows in both "
                           "Cap and its Cty, re-orthonormalised (perp_basis)"} if any(keep_kind(c) in N52B_KEEPS for c in args.conditions) else {}),
        }  # fmt: skip
    if any(n57_kind(c) for c in args.conditions):  # amendment 78 note 57
        manifest["amendment78"] = {
            "onlyRperp": 'r\' = P_X r; X = the first k columns of QR([Q_A | V]) beyond A (V: random.Random("n41:" + id).sample(note 41\'s pool, '
                         "16 |A|), its first 4 |A| = note 41's R4, asserted); k per item = the smallest whose share of paper10's removal "
                         "energy (paper10's forward, summed over layers and positions) reaches E_A (all 16 |A| if none: reached false)",
            "topK_keepRE": "topK's removal minus its part in span(first k of the same 16 |A| rows), k per item energy-matched to E_A in "
                           "topK's forward (nested QR of the rows)",
            "ansRe": 'answer_span_edit over the first k of random.Random("n50:" + id).sample(letter rows minus A\'s, 16 |cands2 rows|) (its '
                     "first |cands2 rows| = ansRk's), k = the smallest whose removed energy reaches ansJ's in ansJ's forward",
            "keepRivals": "keep span = every form (note 37's) of every relation answer (not gold) with a form among the clean top-10 tokens, "
                          "gold's form rows removed",
            "keepRandRivals": 'as many random relation answers (not gold, not rivals, no form in the top-10, no gold row), each matched to a '
                              'rival\'s form-row count (closest), random.Random("n57rr:" + id) order',
            "logs": "n57_rows.jsonl (rows, rivals, tokens), n57_log.jsonl (per item and matching forward: k, reached, E_target, E_match); "
                    "rows: edit_rel, keeplog.rank",
        }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    suite_fams = [f for f in args.families if f in COMPETENCE]
    if args.plan == "v1check":  # exactly v1's prompts
        prompts = [
            dict(p)
            for p in A.prompts(tok, args.n)
            if p["family"] in args.families + [f"country-{f}" for f in args.families]
        ]
        bridge_of = {it["id"]: it["bridge"] for f in suite_fams for it in S.load(f)}
        for p in prompts:
            p["bridge"] = bridge_of.get(p["id"], "")
    elif args.tasks:
        prompts = tasks_prompts(
            tok,
            args.tasks,
            args.tasks_competence,
            args.tasks_words,
            args.n,
            args.kinds,
            args.tasks_level,
            args.tasks_strata,
            args.tasks_per_word,
            args.tasks_scene_words,
        )
        if args.tasks_v4_h1:  # amendment 58 note 20: v4's gate (scripts/nn_swap.v4_split): H1 closed-book right, guess wrong
            from scripts.nn_swap import v4_split

            v4ok = {i for i, s in v4_split(args.tasks_competence, args.tasks_v4_h1, args.tasks).items() if s == "ok"}
            prompts = [p for p in prompts if p["id"] in v4ok]
            print(f"note 20: v4's gate keeps {len(prompts)} prompts", flush=True)
        if args.sample_per_word:  # 2026-10-26 (amendment 49): a seeded random subset of each word's items, not the first n
            import random

            ids_by: dict = collections.defaultdict(set)
            for p in prompts:
                ids_by[p["family"]].add(p["id"])
            keep = {i for f, ids in ids_by.items()
                    for i in (ids if len(ids) <= args.sample_per_word else random.Random(f"{args.sample_seed}:{f}").sample(sorted(ids), args.sample_per_word))}  # fmt: skip
            prompts = [p for p in prompts if p["id"] in keep]
            print(f"sampled {args.sample_per_word} per word (seed {args.sample_seed}): {len(keep)} items", flush=True)
    else:
        competence = COMPETENCE if args.wording == "A" else {f: "competence_b_v1" for f in ("BL", "BR", "RL", "RR")}
        if args.competence:  # a new target: its own suite_v1 competence run decides eligibility
            competence = {f: args.competence for f in ("BL", "BR", "RL", "RR")}
        prompts = suite_prompts(tok, suite_fams, args.kinds, args.n, competence, args.skip, args.wording)
        cfams = [f for f in args.families if f in ("R", "B")]
        if args.countries_build:
            assert not args.skip, "--countries-build draws its own sample: no --skip"
            prompts += built_country_prompts(model, tok, cfams, args.n)
        else:
            prompts += country_prompts(tok, cfams, args.n, args.skip)
    if args.answertype:
        prompts += answertype_prompts(tok, args.answertype)
    for p in prompts:
        p["skip"] = bridge_positions(tok, p["ids"], p["bridge"]) if p["bridge"] else []
        q0 = question_start(tok, p["ids"])
        dpos = bridge_positions(tok, p["ids"], p["desc"]) if args.positions == "desc" and p.get("desc") else []
        p["outside"] = outside_positions(args.positions, len(p["ids"]), q0, p["skip"], dpos)
    print(len(prompts), "prompts;", len(bands), "bands;", len(args.conditions), "conditions", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    if args.dict_digits:  # 2026-10-23 (amendment 21 note): digit tokens join the dictionary, for numbers as intermediates
        digits = [i for i, s_ in enumerate(model.decoded) if i not in model.special_ids and s_.strip().isdigit()]
        letters = torch.tensor(sorted(set(letters.tolist()) | set(digits)), device="cuda")
        print(f"dictionary: {letters.numel()} tokens ({len(digits)} digit tokens added)", flush=True)
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    layers = sorted({la for b in bands for la in b})
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    rot = {la: rotation(wg.shape[1], SEED_ROT + args.seed_offset + la) for la in layers}
    rdict = {la: RotatedDictionary(dic[la], rotation(wg.shape[1], SEED_DICT + args.seed_offset + la)) for la in layers}
    unembed = None  # the logit lens's directions: the same dictionary with J = identity, one for every layer
    if any(c.startswith("unembed") or c.startswith("ansU") for c in args.conditions):
        unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    pca = {}  # 2026-10-25 (TA note, variance control): the residual's top principal directions at each layer, +/- each
    if any("pca" in c for c in args.conditions):  # paper10_pcasize (amendment 48 note 1): paper10's size, along these
        pca = pca_dictionaries(model, layers)
    gauss = {}
    if "gauss" in args.conditions:
        for la in layers:  # v1's control, drawn exactly as ablate_pilot did
            g = torch.Generator(device="cuda").manual_seed(SEED_GAUSS + la)
            gauss[la] = MatrixDictionary(torch.nn.functional.normalize(torch.randn((letters.numel(), wg.shape[1]),
                                                                                    device="cuda", generator=g), dim=-1))  # fmt: skip
    own_cache: dict[tuple[str, int], torch.Tensor] = {}
    cap_rows = cty_rows = None  # note 44: the letter-token rows of every form of every capital / country
    if any(is_n44(c) or is_n52(c) for c in args.conditions):  # amendment 72 note 52: note 44's spans, residualised
        caps, ctys = n44_values()

        def every_form(vals: list[str]) -> torch.Tensor:  # either case, with or without a leading space (note 37's forms)
            ids = {S.ids(tok, f)[0] for v in vals for f in (v, v.lower(), " " + v, " " + v.lower())}
            rr = row_of[torch.tensor(sorted(ids), device="cuda")]
            return rr[rr >= 0].unique()

        cap_rows, cty_rows = every_form(caps), every_form(ctys)
        shared = sorted(set(cap_rows.tolist()) & set(cty_rows.tolist()))
        print(f"note 44: {len(caps)} capitals -> {cap_rows.numel()} rows; {len(ctys)} countries -> {cty_rows.numel()} rows; "
              f"{len(shared)} rows shared", flush=True)
        (out_dir / "n44_spans.json").write_text(json.dumps({"capitals": caps, "countries": ctys, "cap_rows": cap_rows.tolist(),
                                                            "cty_rows": cty_rows.tolist(), "shared_rows": shared,
                                                            "shared_tokens": [model.decoded[int(letters[i])] for i in shared]}) + "\n")  # fmt: skip

    def own_rows(word: str, la: int) -> torch.Tensor:
        if (word, la) not in own_cache:
            rows = {int(row_of[i]) for i in model.surface_ids(word) if int(row_of[i]) >= 0}
            try:
                concept = int(row_of[model.concept_token(word)])
            except ValueError:
                concept = -1
            if concept >= 0:
                cos = dic[la].scores(dic[la].atoms(torch.tensor([concept], device="cuda")))[0]
                rows |= set((cos >= OWN_COS).nonzero().squeeze(1).tolist())
            own_cache[(word, la)] = torch.tensor(sorted(rows), dtype=torch.long, device="cuda")
        return own_cache[(word, la)]

    # amendment 72 (notes 49-52): which machinery this run needs
    n4950 = any(n49_kind(c) for c in args.conditions)
    has_keepA = any(keep_kind(c) == "A" for c in args.conditions)  # amendment 72 (shared): paper10 logs E_A whenever A is kept
    n51ks = {top_k(c) for c in args.conditions if is_n51(c)}  # doses whose plain topK forward logs E_A
    n52on = any(is_n52(c) for c in args.conditions)
    n57on = any(n57_kind(c) for c in args.conditions)  # amendment 78 note 57
    re_ks = {top_k(c) for c in args.conditions if n57_kind(c) == "keepRE"}  # doses whose plain topK forward sets keepRE's size
    items72 = {}
    if any(n49_kind(c) in ("keepOwn", "keepSib") or n57_kind(c) in ("keepRivals", "keepRandRivals") for c in args.conditions):
        from scripts import tasks_v2 as T

        items72 = {it["id"]: it for it in T.load(args.tasks)}
    form_cache: dict[int, list[int]] = {}  # token id -> letter rows of the first tokens of its forms (note 45)
    nbr_cache: dict[tuple[int, int], torch.Tensor] = {}  # (letter row, layer) -> rows with cosine >= OWN_COS to its atom

    def form_rows(t: int) -> list[int]:
        if t not in form_cache:
            w = model.decoded[t].strip()
            form_cache[t] = sorted({int(row_of[i]) for i in first_token_ids(tok, w) if int(row_of[i]) >= 0}) if w else []
        return form_cache[t]

    def nbr_rows(row: int, la: int) -> torch.Tensor:
        if (row, la) not in nbr_cache:
            cos = dic[la].scores(dic[la].atoms(torch.tensor([row], device="cuda")))[0]
            nbr_cache[(row, la)] = (cos >= OWN_COS).nonzero().squeeze(1)
        return nbr_cache[(row, la)]

    def letter_rows(ids_: set[int]) -> list[int]:
        return sorted({int(row_of[i]) for i in ids_ if int(row_of[i]) >= 0})

    def answer_forms(v: str, k: str) -> set[int]:  # note 37's forms of one answer: as read and lower case; leading space, either case
        return {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k), S.ids(tok, " " + v)[0], S.ids(tok, " " + v.lower())[0]}

    def own_sib(p: dict) -> dict:
        """Note 49: the item's own answer's form rows, and one sibling's (letter rows disjoint from own's, count matched)."""
        it = items72.get(p["id"])
        if it is None or p["kind"] != "clean":
            return {"own": [], "sib": [], "sib_word": None, "sib_matched": False}
        a, k = it["answer"], it["kind"]
        own = letter_rows(answer_forms(a, k))
        vocab = it.get("answer_vocab") or natural_vocab(args.tasks)[(it["domain"], "answer")]
        cands = {}
        for v in sorted(set(vocab)):
            if v.lower() == a.lower():
                continue
            rr = letter_rows(answer_forms(v, k))
            if rr and not set(rr) & set(own) and S.answer_token(tok, v, k) != S.answer_token(tok, a, k):
                cands[v] = rr
        if not cands:
            return {"own": own, "sib": [], "sib_word": None, "sib_matched": False}
        best = min(abs(len(rr) - len(own)) for rr in cands.values())
        pool = sorted(v for v, rr in cands.items() if abs(len(rr) - len(own)) == best)
        import random

        v = random.Random("n49sib:" + p["id"]).choice(pool)
        return {"own": own, "sib": cands[v], "sib_word": v, "sib_matched": best == 0}

    def rivals_of(p: dict, top10_ids: list[int]) -> dict:
        """Note 57: the relation's answers (not gold) with a form among the clean top-10 tokens (rivals; their form rows minus
        gold's), and as many random answers of the relation that are not gold, not rivals, have no form in the top-10 and no row
        of gold's, each with its rival's form-row count (closest if none; Random("n57rr:" + id) order)."""
        it = items72.get(p["id"])
        if it is None or p["kind"] != "clean":
            return {"riv": [], "rand": [], "riv_rows": [], "rand_rows": [], "riv_tok": [], "rand_tok": [], "matched": False}
        a, k = it["answer"], it["kind"]
        vocab = sorted(set(it.get("answer_vocab") or natural_vocab(args.tasks)[(it["domain"], "answer")]))
        S10 = set(top10_ids)
        gold = set(letter_rows(answer_forms(a, k)))
        rows_v = {v: sorted(set(letter_rows(answer_forms(v, k))) - gold) for v in vocab}
        riv = [v for v in vocab if v.lower() != a.lower() and answer_forms(v, k) & S10]
        pool = [v for v in vocab if v.lower() != a.lower() and v not in riv and not answer_forms(v, k) & S10
                and not set(letter_rows(answer_forms(v, k))) & gold and rows_v[v]]  # fmt: skip
        import random

        random.Random("n57rr:" + p["id"]).shuffle(pool)
        rand: list[str] = []
        for v in riv:
            left = [u for u in pool if u not in rand]
            if not left:
                break
            want = len(rows_v[v])
            rand.append(min(left, key=lambda u: abs(len(rows_v[u]) - want)))  # the first in seeded order among the closest
        rr = sorted({x for v in riv for x in rows_v[v]})
        ra = sorted({x for v in rand for x in rows_v[v]})
        return {"riv": riv, "rand": rand, "riv_rows": rr, "rand_rows": ra, "matched": len(rr) == len(ra) and len(rand) == len(riv),
                "riv_tok": sorted({t for v in riv for t in answer_forms(v, k)}), "rand_tok": sorted({t for v in rand for t in answer_forms(v, k)})}

    t0 = time.time()
    rows_out, band_seconds = [], collections.Counter()
    sink_tally: dict[str, list[int]] = {}
    rows_path = out_dir / "rows.jsonl"
    assert not rows_path.exists(), f"{rows_path} exists"
    written = 0
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    if args.pad:  # 2026-10-21 (Zach): length-sorted, right-padded batches instead of exact-length ones
        by_len = {0: sorted(prompts, key=lambda p: len(p["ids"]))}
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    for group in by_len.values():
        for start in range(0, len(group), args.batch):
            chunk = group[start : start + args.batch]
            width = max(len(p["ids"]) for p in chunk)
            ids = torch.tensor([p["ids"] + [pad_id] * (width - len(p["ids"])) for p in chunk], device="cuda")
            last = torch.tensor([len(p["ids"]) - 1 for p in chunk], device="cuda") if args.pad else None
            answer = torch.tensor([p["tok"] for p in chunk], device="cuda")
            clean = first_token_logits(model, ids, {}, last)
            base_logp = clean.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
            for row, p in enumerate(chunk):
                rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": "-", "condition": "none",
                                 **reads(clean[row], p, args.read), "logp": float(base_logp[row])})  # fmt: skip
            protected = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            # does the protected set (clean top-10 at the answer position) shield the bridge itself? (logged per row)
            shields = [bool(p["bridge"]) and bool(set(model.surface_ids(p["bridge"])) & set(t.tolist()))
                       for p, t in zip(chunk, clean.topk(10, dim=1).indices, strict=True)]  # fmt: skip
            span_cache: dict = {}  # note 37: (layer, rows) -> kept span, this batch only
            a_rows, rand_rows = [], []  # note 41: per row, A's dictionary rows and its 4|A| random rows (draw order)
            if any(is_rand(c) for c in args.conditions) or n4950 or n57on:  # amendments 72 / 78 use A and note 41's rows too
                for i, p in enumerate(chunk):
                    rr = row_of[torch.tensor(p[KEEPA_ROWS[args.keepA_forms]], device="cuda")]
                    a_rows.append(rr[rr >= 0].unique())
                    pick = random_rows(p["id"], a_rows[-1].numel(), letters.numel(), set(a_rows[-1].tolist()) | set(protected[i].tolist()))
                    rand_rows.append(torch.tensor(pick, device="cuda"))
                with (out_dir / "rand_rows.jsonl").open("a") as fh:  # the draws, for audit
                    fh.writelines(json.dumps({"id": p["id"], "family": p["family"], "n_A": int(a_rows[i].numel()),
                                              "rows4": rand_rows[i].tolist()}) + "\n" for i, p in enumerate(chunk))  # fmt: skip

            n44: dict = {}  # note 44: per row, its Cty rows (count-matched), CapCty rows, Rcap pool (draw order) and Rcap's size
            if cap_rows is not None:
                nc = cap_rows.numel()
                for i, p in enumerate(chunk):
                    cty = torch.tensor(n44_subsample(p["id"], cty_rows.tolist(), nc), device="cuda")
                    n44.setdefault("cty", []).append(cty)
                    n44.setdefault("capcty", []).append(torch.cat([cap_rows, cty]).unique())
                    pool = random_rows(p["id"], nc, letters.numel(), set(cap_rows.tolist()) | set(protected[i].tolist()))
                    n44.setdefault("pool", []).append(torch.tensor(pool, device="cuda"))
                n44["k"] = [4 * nc] * len(chunk)  # set from paper10's forward (energy-matched); paper10 runs first
                with (out_dir / "n44_rows.jsonl").open("a") as fh:  # the draws, for audit
                    fh.writelines(json.dumps({"id": p["id"], "family": p["family"], "kind": p["kind"], "cty_rows": n44["cty"][i].tolist(),
                                              "rcap_pool": n44["pool"][i].tolist()}) + "\n" for i, p in enumerate(chunk))  # fmt: skip

            def kept_span(i: int, la: int, kind: str) -> torch.Tensor:
                """Row i's kept span at layer la (orthonormal [d, k]): A as note 37, or the first 1x / 2x / 4x |A| columns of
                one QR of the 4|A| random rows' J++ unit vectors (their spans are nested); note 44: Cap, Cty, CapCty, or Rcap
                (the first k rows of the item's 4|Cap| random pool, k energy-matched in paper10's forward). Only Cap is cached
                across conditions: the per-item note 44 spans are rebuilt per use (GPU memory: up to 32 rows x 9 layers)."""
                if kind == "A":
                    rr = row_of[torch.tensor(chunk[i][KEEPA_ROWS[args.keepA_forms]], device="cuda")]
                    rr = rr[rr >= 0].unique()
                elif kind in ("Cty", "CapCty", "Rcap"):
                    rr = n44["pool"][i][: n44["k"][i]] if kind == "Rcap" else n44[{"Cty": "cty", "CapCty": "capcty"}[kind]][i]
                    return torch.linalg.qr(dic[la].atoms(rr).double().T)[0]
                elif kind == "Cap":
                    rr = cap_rows
                else:
                    rr = rand_rows[i]
                ck = (la, tuple(rr.tolist()))
                if ck not in span_cache:
                    span_cache[ck] = torch.linalg.qr(dic[la].atoms(rr).double().T)[0]
                return span_cache[ck] if kind in ("A", "R4", "Cap") else span_cache[ck][:, : RAND_MULT[kind] * a_rows[i].numel()]

            # amendment 72 notes 49 / 50: per row, protF's rows (= keepT10's), keepRT10's, own / sibling forms, R8, ansRk's rows
            g72: dict = {}
            emask = torch.zeros(len(chunk), width, dtype=torch.bool, device="cuda")  # edited positions (|edit| / |h| log)
            for i, p in enumerate(chunk):
                emask[i, : len(p["ids"])] = True
                if p["outside"]:
                    emask[i, torch.tensor(p["outside"], device="cuda")] = False
            if n4950:
                import random

                top10 = clean.topk(10, dim=1).indices
                for i, p in enumerate(chunk):
                    added = sorted({r_ for t in top10[i].tolist() for r_ in form_rows(t)} - set(protected[i].tolist()))
                    pf = torch.cat([protected[i], torch.tensor(added, dtype=torch.long, device="cuda")]).unique()
                    g72.setdefault("protF", []).append(pf)
                    g72.setdefault("n_added", []).append(len(added))
                    excl = set(pf.tolist())
                    pool = [j for j in range(letters.numel()) if j not in excl]
                    g72.setdefault("RT10", []).append(torch.tensor(sorted(random.Random("n49:" + p["id"]).sample(pool, pf.numel())), device="cuda"))
                    os_ = own_sib(p)
                    g72.setdefault("Own", []).append(torch.tensor(os_["own"], dtype=torch.long, device="cuda"))
                    g72.setdefault("Sib", []).append(torch.tensor(os_["sib"], dtype=torch.long, device="cuda"))
                    g72.setdefault("sib", []).append({k: os_[k] for k in ("sib_word", "sib_matched")})
                    n = a_rows[i].numel()
                    excl = set(a_rows[i].tolist()) | set(protected[i].tolist())
                    r8 = random.Random("n41:" + p["id"]).sample([j for j in range(letters.numel()) if j not in excl], 8 * n)
                    assert r8[: 4 * n] == rand_rows[i].tolist(), "note 50: R8's first 4|A| rows are not note 41's R4"
                    g72.setdefault("R8", []).append(torch.tensor(r8, device="cuda"))
                    c2 = row_of[torch.tensor(p["cands2"], device="cuda")]
                    nc = int(c2[c2 >= 0].unique().numel())
                    excl = set(a_rows[i].tolist())
                    g72.setdefault("Rk", []).append(torch.tensor(random.Random("n50:" + p["id"]).sample(
                        [j for j in range(letters.numel()) if j not in excl], nc), device="cuda"))  # fmt: skip
                with (out_dir / "n49_rows.jsonl").open("a") as fh:  # the per-item rows, for audit
                    fh.writelines(json.dumps({"id": p["id"], "family": p["family"], "kind": p["kind"],
                                              "top10": top10[i].tolist(), "protected": protected[i].tolist(),
                                              "protF": g72["protF"][i].tolist(), "RT10": g72["RT10"][i].tolist(),
                                              "own": g72["Own"][i].tolist(), "sib": g72["Sib"][i].tolist(), **g72["sib"][i],
                                              "R8_beyond_R4": g72["R8"][i][4 * a_rows[i].numel():].tolist(),
                                              "Rk": g72["Rk"][i].tolist()}) + "\n" for i, p in enumerate(chunk))  # fmt: skip
            g57: dict = {}  # amendment 78 note 57: per row, R16 / Re draws, rivals, and the energy-matched sizes (set in the forwards)
            if n57on:
                import random

                top10_57 = clean.topk(10, dim=1).indices.tolist()
                for i, p in enumerate(chunk):
                    n = a_rows[i].numel()
                    excl = set(a_rows[i].tolist()) | set(protected[i].tolist())
                    r16 = random.Random("n41:" + p["id"]).sample([j for j in range(letters.numel()) if j not in excl], 16 * n)
                    assert r16[: 4 * n] == rand_rows[i].tolist(), "note 57: the 16|A| draw's first 4|A| rows are not note 41's R4"
                    g57.setdefault("R16", []).append(torch.tensor(r16, device="cuda"))
                    c2 = row_of[torch.tensor(p["cands2"], device="cuda")]
                    c2 = c2[c2 >= 0].unique()
                    g57.setdefault("J", []).append(c2)
                    exa = set(a_rows[i].tolist())
                    g57.setdefault("Re", []).append(torch.tensor(random.Random("n50:" + p["id"]).sample(
                        [j for j in range(letters.numel()) if j not in exa], 16 * c2.numel()), device="cuda"))  # fmt: skip
                    rv = rivals_of(p, top10_57[i])
                    g57.setdefault("riv", []).append(rv)
                    g57.setdefault("Rivals", []).append(torch.tensor(rv["riv_rows"], dtype=torch.long, device="cuda"))
                    g57.setdefault("RandRivals", []).append(torch.tensor(rv["rand_rows"], dtype=torch.long, device="cuda"))
                g57["k_onlyR"] = [int(x.numel()) for x in g57["R16"]]  # defaults (all rows) until the matching forward sets them
                g57["k_RE"] = {K_: [int(x.numel()) for x in g57["R16"]] for K_ in re_ks}
                g57["k_Re"] = [int(x.numel()) for x in g57["Re"]]
                with (out_dir / "n57_rows.jsonl").open("a") as fh:
                    fh.writelines(json.dumps({"id": p["id"], "family": p["family"], "kind": p["kind"], "top10": top10_57[i], "n_A": int(a_rows[i].numel()),
                                              "R16_beyond_R4": g57["R16"][i][4 * a_rows[i].numel():].tolist(), "Re": g57["Re"][i].tolist(),
                                              **g57["riv"][i]}) + "\n" for i, p in enumerate(chunk))  # fmt: skip
            acc57: dict = {}  # cond -> per row {"target", "tot", "cols", ...}, filled in the matching forwards

            def obs57(r: torch.Tensor, B: int, T: int, la: int, cond: str, h: torch.Tensor) -> None:
                """Note 57's matching in paper10's forward (onlyRperp's size; the rivals' E) and in topK's (keepRE's size). Reads r only."""
                A_ = acc57.setdefault(cond, [collections.defaultdict(float) for _ in range(B)])
                for b in range(B):
                    rb = r[b * T : (b + 1) * T].double()
                    QA = kept_span(b, la, "A")
                    l = A_[b]
                    l["target"] += float((rb @ QA).pow(2).sum())
                    l["tot"] += float(rb.pow(2).sum())
                    V = dic[la].atoms(g57["R16"][b]).double()
                    if cond == "paper10":
                        q, R_ = torch.linalg.qr(torch.cat([QA, V.T], 1))
                        Q = q[:, QA.shape[1] :]
                        l["min_R"] = min(l.get("min_R", 1e9), float(R_.diagonal()[QA.shape[1] :].abs().min()))
                        for kk in ("Rivals", "RandRivals"):
                            if f"paper10_keep{kk}" in args.conditions and g57[kk][b].numel():
                                l["E_" + kk] += float((rb @ torch.linalg.qr(dic[la].atoms(g57[kk][b]).double().T)[0]).pow(2).sum())
                    else:
                        Q = torch.linalg.qr(V.T)[0]
                    c = (rb @ Q).pow(2).sum(0)
                    l["cols"] = c if isinstance(l["cols"], float) else l["cols"] + c

            def obs57_ans(h: torch.Tensor, la: int) -> None:
                """Note 57: ansJ's removed energy and each random row's in ansJ's forward (edited positions), for ansRe's size."""
                A_ = acc57.setdefault("ansJ", [collections.defaultdict(float) for _ in range(h.shape[0])])
                for b in range(h.shape[0]):
                    xb = h[b].double()[emask[b, : h.shape[1]]]
                    l = A_[b]
                    l["target"] += float((xb @ torch.linalg.qr(dic[la].atoms(g57["J"][b]).double().T)[0]).pow(2).sum())
                    l["tot"] += float(xb.pow(2).sum())
                    c = (xb @ torch.linalg.qr(dic[la].atoms(g57["Re"][b]).double().T)[0]).pow(2).sum(0)
                    l["cols"] = c if isinstance(l["cols"], float) else l["cols"] + c

            def finalize57(cond: str) -> None:
                """Set the energy-matched sizes from cond's forward and log them (n57_log.jsonl)."""
                lines_ = []
                for b, l in enumerate(acc57.pop(cond)):
                    cum = l["cols"].cumsum(0)
                    hit = (cum >= l["target"]).nonzero()
                    k = int(hit[0]) + 1 if hit.numel() else cum.numel()
                    if cond == "paper10":
                        g57["k_onlyR"][b] = k
                    elif cond == "ansJ":
                        g57["k_Re"][b] = k
                    else:
                        g57["k_RE"][top_k(cond)][b] = k
                    tot = l["tot"]
                    lines_.append({"id": chunk[b]["id"], "family": chunk[b]["family"], "kind": chunk[b]["kind"], "forward": cond, "k": k,
                                   "n_pool": int(cum.numel()), "reached": bool(hit.numel()), "E_target": l["target"] / tot if tot > 0 else None,
                                   "E_match": float(cum[k - 1]) / tot if tot > 0 else None, "min_R": l.get("min_R"),
                                   **{k_: v / tot for k_, v in l.items() if k_.startswith("E_") and tot > 0}})  # fmt: skip
                with (out_dir / "n57_log.jsonl").open("a") as fh:
                    fh.writelines(json.dumps(x) + "\n" for x in lines_)

            def edit57(cond: str, la: int):
                """Note 57's edit for cond at layer la."""
                rot_ = rot[la] if cond.endswith("_rot") else None
                kind = n57_kind(cond)
                if kind == "ansRe":
                    rows_ = [g57["Re"][i][: g57["k_Re"][i]] for i in range(len(chunk))]
                    for i in range(len(chunk)):
                        rank72[cond][i].append(int(rows_[i].numel()))
                    return answer_span_edit(dic[la], rows_, [p["outside"] for p in chunk], rotation=rot_)
                rs = [RowSettings(skip=p["outside"], protected=protected[i]) for i, p in enumerate(chunk)]
                if kind == "onlyRperp":  # r' = P_X r, X the energy-matched random span orthogonal to A
                    cap: dict = {}
                    inner = removal_edit("top", dic[la], rs, k=10, observe=lambda r, B, T: cap.__setitem__("r", r))

                    def only(h: torch.Tensor, inner=inner, cap=cap, la=la, rot_=rot_, cond=cond) -> torch.Tensor:
                        B, T, d = h.shape
                        inner(h)
                        r = cap.pop("r")
                        out = torch.zeros_like(r)
                        for b in range(B):
                            QA = kept_span(b, la, "A")
                            V = dic[la].atoms(g57["R16"][b][: g57["k_onlyR"][b]]).double()
                            Q = torch.linalg.qr(torch.cat([QA, V.T], 1))[0][:, QA.shape[1] :]
                            rank72[cond][b].append(int(Q.shape[1]))
                            rb = r[b * T : (b + 1) * T].double()
                            out[b * T : (b + 1) * T] = ((rb @ Q) @ Q.T).float()
                        if rot_ is not None:
                            out = out @ rot_.T
                        return (h.reshape(B * T, d).float() - out).reshape(B, T, d)

                    return only
                K_ = top_k(cond)

                def fn(i: int, la=la, kind=kind, cond=cond, K_=K_) -> torch.Tensor:
                    rr = g57["R16"][i][: g57["k_RE"][K_][i]] if kind == "keepRE" else g57[kind.removeprefix("keep")][i]
                    Q = (torch.linalg.qr(dic[la].atoms(rr).double().T)[0] if rr.numel()
                         else torch.zeros(wg.shape[1], 0, dtype=torch.float64, device="cuda"))  # fmt: skip
                    rank72[cond][i].append(int(Q.shape[1]))
                    return Q

                return removal_edit("top", dic[la], rs, rotation=rot_, k=K_, keep_span=LazySpans(fn, len(chunk)),
                                    **({"chunk": args.topk_chunk} if args.topk_chunk and K_ > 10 else {}))  # fmt: skip

            protc_cache: dict = {}

            def protc_rows(i: int, la: int) -> torch.Tensor:
                """Note 49's protC at layer la: protF's rows + every row with cosine >= OWN_COS to a clean top-10 letter token's atom."""
                if (i, la) not in protc_cache:
                    protc_cache[(i, la)] = torch.cat([g72["protF"][i]] + [nbr_rows(int(r_), la) for r_ in protected[i]]).unique()
                return protc_cache[(i, la)]

            rank72: dict = collections.defaultdict(lambda: collections.defaultdict(list))  # cond -> row -> kept rank per layer

            def span72(i: int, la: int, kind: str) -> torch.Tensor:
                """Amendment 72's kept spans (orthonormal [d, r]) of row i at layer la."""
                if kind in ("T10", "RT10", "Own", "Sib"):
                    rr = g72["protF" if kind == "T10" else kind][i]
                    if rr.numel() == 0:
                        return torch.zeros(wg.shape[1], 0, dtype=torch.float64, device="cuda")
                    return torch.linalg.qr(dic[la].atoms(rr).double().T)[0]
                if kind in ("R4perp", "R8perp"):
                    return perp_basis(kept_span(i, la, "A"), dic[la].atoms(rand_rows[i] if kind == "R4perp" else g72["R8"][i]))
                if kind == "CapPerp":
                    return perp_basis(kept_span(i, la, "Cty"), dic[la].atoms(cap_rows))
                if kind == "CtyPerp":
                    return perp_basis(kept_span(i, la, "Cap"), dic[la].atoms(n44["cty"][i]))
                if kind == "Shared":
                    return shared_basis(kept_span(i, la, "Cap"), kept_span(i, la, "Cty"))[0]
                if kind == "SharedNoLit":  # note 52b: Shared projected off the rows literally in both sets (this item's Cty)
                    lit = sorted(set(cap_rows.tolist()) & set(n44["cty"][i].tolist()))
                    ql = (torch.linalg.qr(dic[la].atoms(torch.tensor(lit, device="cuda")).double().T)[0] if lit
                          else torch.zeros(wg.shape[1], 0, dtype=torch.float64, device="cuda"))  # fmt: skip
                    return perp_basis(ql, shared_basis(kept_span(i, la, "Cap"), kept_span(i, la, "Cty"))[0].T)
                if kind in ("RShared", "RCapPerp", "RCtyPerp"):  # note 52b: the first k rows of the Rcap pool, k matched in paper10's forward
                    return torch.linalg.qr(dic[la].atoms(n44["pool"][i][: k52b[kind[1:]][i]]).double().T)[0]
                raise ValueError(kind)

            def edit72(cond: str, la: int):
                """Amendment 72's edit for cond at layer la (notes 49, 50, 52)."""
                rot_ = rot[la] if cond.endswith("_rot") else None
                kind = n49_kind(cond)
                outside = [p["outside"] for p in chunk]
                if kind == "ansRk":  # note 50: answer_span_edit over as many random rows as ansJ's
                    for i in range(len(chunk)):
                        rank72[cond][i].append(int(g72["Rk"][i].numel()))
                    return answer_span_edit(dic[la], list(g72["Rk"]), outside, rotation=rot_)
                rs = [RowSettings(skip=p["outside"], protected=protected[i]) for i, p in enumerate(chunk)]
                if kind in ("protF", "protC"):
                    rs = [RowSettings(skip=p["outside"], protected=g72["protF"][i] if kind == "protF" else protc_rows(i, la))
                          for i, p in enumerate(chunk)]  # fmt: skip
                    for i in range(len(chunk)):
                        rank72[cond][i].append(int(rs[i].protected.numel()))
                    return removal_edit("top", dic[la], rs, rotation=rot_, k=10)
                if kind == "onlyA":  # note 50: r' = P_A r (the removal's answer part only), turned for _rot
                    cap: dict = {}
                    inner = removal_edit("top", dic[la], rs, k=10, observe=lambda r, B, T: cap.__setitem__("r", r))

                    def only(h: torch.Tensor, inner=inner, cap=cap, la=la, rot_=rot_) -> torch.Tensor:
                        B, T, d = h.shape
                        inner(h)
                        r = cap.pop("r")
                        out = torch.zeros_like(r)
                        for b in range(B):
                            Q = kept_span(b, la, "A")
                            rb = r[b * T : (b + 1) * T].double()
                            out[b * T : (b + 1) * T] = ((rb @ Q) @ Q.T).float()
                        if rot_ is not None:
                            out = out @ rot_.T
                        return (h.reshape(B * T, d).float() - out).reshape(B, T, d)

                    for i in range(len(chunk)):
                        rank72[cond][i].append(int(kept_span(i, la, "A").shape[1]))
                    return only
                kk = keep_kind(cond)  # a kept span: T10, RT10, Own, Sib, R4perp, R8perp, CapPerp, CtyPerp, Shared

                def fn(i: int, la=la, kk=kk, cond=cond) -> torch.Tensor:
                    Q = span72(i, la, kk)
                    rank72[cond][i].append(int(Q.shape[1]))
                    return Q

                return removal_edit("top", dic[la], rs, rotation=rot_, k=10, keep_span=LazySpans(fn, len(chunk)))

            log72: dict = {}  # paper10's (notes 49, 50, 52) and topK's (note 51) per-row sums, filled by observe72
            k52b = {kk: [int(x.numel()) for x in n44.get("pool", [])] for kk in N52_KEEPS}  # note 52b: matched sizes (set after paper10)

            def observe72(r: torch.Tensor, B: int, T: int, la: int, cond: str, h: torch.Tensor) -> None:
                """Amendment 72's log in paper10's forward (notes 49 / 50 / 52) or a plain topK's (note 51): energies of r in each
                kept span, alpha, the protections' removals on the same residuals, ranks, |edit| / |h|. Reads r only."""
                L = log72.setdefault(cond, [collections.Counter() for _ in range(B)])
                d = h.shape[-1]
                x = h.reshape(B * T, d).float()
                xn = x.norm(dim=-1)
                rp: dict = {}
                if cond == "paper10" and n4950:
                    for kp in ("F", "C"):
                        if any(n49_kind(c) == "prot" + kp for c in args.conditions):
                            cap: dict = {}
                            rs = [RowSettings(skip=p["outside"], protected=g72["protF"][i] if kp == "F" else protc_rows(i, la))
                                  for i, p in enumerate(chunk)]  # fmt: skip
                            removal_edit("top", dic[la], rs, k=10, observe=lambda rr, B_, T_, cap=cap: cap.__setitem__("r", rr.clone()))(h)
                            rp[kp] = cap["r"]
                for b in range(B):
                    rb = r[b * T : (b + 1) * T].double()
                    m = emask[b, :T]
                    l = L[b]
                    l["energy"] += float(rb.pow(2).sum())
                    l["dr2"] += float(r[b * T : (b + 1) * T].double().pow(2).sum(-1)[m].sum())
                    l["h2"] += float(xn[b * T : (b + 1) * T].double().pow(2)[m].sum())
                    l["layers"] += 1
                    if cond == "paper10" and n52on:
                        for kk in N52_KEEPS + ("SharedNoLit",):
                            if f"paper10_keep{kk}" in args.conditions or f"paper10_keepR{kk}" in args.conditions:
                                if kk == "Shared":
                                    Q, cs = shared_basis(kept_span(b, la, "Cap"), kept_span(b, la, "Cty"))
                                    l["n_cos_ge"] += len(cs)
                                    if "paper10_keepSharedNoLit" in args.conditions:  # note 52b: literal shared rows per item
                                        l["n_lit"] = len(set(cap_rows.tolist()) & set(n44["cty"][b].tolist()))
                                else:
                                    Q = span72(b, la, kk)
                                l["E_" + kk] += float((rb @ Q).pow(2).sum())
                                l["rank_" + kk] += Q.shape[1]
                        continue
                    QA = kept_span(b, la, "A")
                    aA = rb @ QA
                    l["ansE"] += float(aA.pow(2).sum())
                    l["E_A"] += float(aA.pow(2).sum())
                    l["rank_A"] += QA.shape[1]
                    if cond != "paper10":  # note 51: topK's E_A only
                        continue
                    spans = {"A": QA, "R": kept_span(b, la, "R"), "R2": kept_span(b, la, "R2"), "R4": kept_span(b, la, "R4")}
                    for kk in ("T10", "RT10", "Own", "Sib", "R4perp", "R8perp"):
                        if f"paper10_keep{kk}" in args.conditions:
                            spans[kk] = span72(b, la, kk)
                    for kk, Q in spans.items():
                        pX = rb @ Q
                        l["alpha_num_" + kk] += float(((rb - pX @ Q.T) @ QA).pow(2).sum())
                        if kk != "A":  # A's energy and rank are logged above
                            l["E_" + kk] += float(pX.pow(2).sum())
                            l["rank_" + kk] += Q.shape[1]
                    for kp, rX in rp.items():
                        rXb = rX[b * T : (b + 1) * T].double()
                        l["dot_" + kp] += float((rb * rXb).sum())
                        l["ansX_" + kp] += float((rXb @ QA).pow(2).sum())
                        l["dr2_" + kp] += float(rX[b * T : (b + 1) * T].double().pow(2).sum(-1)[m].sum())
                        l["n_prot_" + kp] += int(g72["protF"][b].numel() if kp == "F" else protc_rows(b, la).numel())

            def keeplog_line(cond: str, b: int) -> dict:
                l, p = log72[cond][b], chunk[b]
                nl, e, a = max(l["layers"], 1), l["energy"], l["ansE"]
                out = {"id": p["id"], "family": p["family"], "kind": p["kind"], "condition": cond, "energy": e,
                       "edit_rel": l["dr2"] / l["h2"] if l["h2"] > 0 else None, "E": {}, "rank": {}}  # fmt: skip
                for k_, v in l.items():
                    if k_.startswith("E_"):
                        out["E"][k_[2:]] = v / e if e > 0 else None
                    elif k_.startswith("rank_"):
                        out["rank"][k_[5:]] = v / nl
                if cond == "paper10" and n4950:
                    out["ansE"] = a
                    out["alpha"] = {k_[10:]: (1 - v / a if a > 0 else None) for k_, v in l.items() if k_.startswith("alpha_num_")}
                    out["prot"] = {kp: {"E": (1 - l["dot_" + kp] / e if e > 0 else None), "ans_removed": (l["ansX_" + kp] / a if a > 0 else None),
                                        "edit_rel": l["dr2_" + kp] / l["h2"] if l["h2"] > 0 else None, "n_rows": l["n_prot_" + kp] / nl}
                                   for kp in ("F", "C") if ("dot_" + kp) in l}  # fmt: skip
                    out["n_rows"] = {"A": int(a_rows[b].numel()), "protected": int(protected[b].numel()), "protF": int(g72["protF"][b].numel()),
                                     "protF_added": g72["n_added"][b], "RT10": int(g72["RT10"][b].numel()), "Own": int(g72["Own"][b].numel()),
                                     "Sib": int(g72["Sib"][b].numel()), "R8": int(g72["R8"][b].numel()), "Rk": int(g72["Rk"][b].numel())}  # fmt: skip
                    out["sib"] = g72["sib"][b]
                if cond == "paper10" and n52on:
                    out["n_cos_ge_shared"] = l["n_cos_ge"] / nl
                    if any(k_.startswith("k_R") for k_ in l):  # note 52b: the matched random keeps' sizes
                        out["k52b"] = {k_: v for k_, v in l.items() if k_.startswith(("k_R", "reached_R", "n_pool"))}
                    if "n_lit" in l:
                        out["n_lit_shared_rows"] = l["n_lit"]
                return out

            for band in bands:
                tb = time.time()
                for cond in conditions_for(band, args.conditions):
                    edits = {}
                    energy = torch.zeros(len(chunk), 5, dtype=torch.float64, device="cuda") if rand_rows else None  # note 41: |r|^2, in A, R, R2, R4
                    if energy is None and has_keepA:  # amendment 72 (shared): |r|^2 and its part in A when A is kept but no note 41 rows
                        energy = torch.zeros(len(chunk), 2, dtype=torch.float64, device="cuda")
                    if n44 and cond == "paper10":  # note 44: |r|^2, in Cap, Cty, CapCty; the pool's per-column energy; span overlap
                        e44 = torch.zeros(len(chunk), 4, dtype=torch.float64, device="cuda")
                        e44pool = torch.zeros(len(chunk), 4 * cap_rows.numel(), dtype=torch.float64, device="cuda")
                        ov44 = torch.zeros(len(chunk), dtype=torch.float64, device="cuda")
                    acc72 = torch.zeros(len(chunk), 2, dtype=torch.float64, device="cuda")  # amendment 72: |edit|^2, |h|^2 sums
                    for la in band:
                        if n57_kind(cond):  # amendment 78 note 57 (ansRe before ansR's prefix test)
                            edits[la] = edit57(cond, la)
                            continue
                        if n49_kind(cond) or is_n52(cond):  # amendment 72 notes 49, 50, 52 (ansRk before ansR's prefix test)
                            edits[la] = edit72(cond, la)
                            continue
                        if cond.startswith("ans"):  # amendment 58 note 3: the candidate answers' directions only
                            if cond.startswith("ansR"):  # amendment 67 note 41: R's span instead (the first |A| random rows)
                                cand_rows = [rr[: a_rows[i].numel()] for i, rr in enumerate(rand_rows)]
                            elif cond.startswith("ansCap"):  # amendment 68 note 44: every form of every capital
                                cand_rows = [cap_rows] * len(chunk)
                            elif cond.startswith("ansCty"):  # note 44: the item's count-matched country rows
                                cand_rows = list(n44["cty"])
                            else:
                                cand_rows = []
                                for p in chunk:
                                    rr = row_of[torch.tensor(p["cands2"], device="cuda")]
                                    cand_rows.append(rr[rr >= 0].unique())
                            edits[la] = answer_span_edit(unembed if cond.startswith("ansU") else dic[la], cand_rows,
                                                         [p["outside"] for p in chunk],
                                                         rotation=rot[la] if cond.endswith("_rot") else None)
                            continue
                        if cond.startswith("pca"):  # the variance control: no protected atoms (they index token rows)
                            rs = [RowSettings(skip=p["outside"]) for p in chunk]
                        elif top_k(cond) is not None and "keepown" in cond:  # C1's kill test under paper10 (2026-10-21)
                            rs = [RowSettings(skip=p["outside"], protected=torch.cat([protected[i], own_rows(p["bridge"], la)])
                                              if p["bridge"] else protected[i]) for i, p in enumerate(chunk)]  # fmt: skip
                        elif top_k(cond) is not None:
                            rs = [RowSettings(skip=p["outside"], protected=protected[i]) for i, p in enumerate(chunk)]
                        elif cond == "keep_own":
                            rs = [RowSettings(skip=p["outside"], banned=own_rows(p["bridge"], la) if p["bridge"] else None)
                                  for p in chunk]  # fmt: skip
                        elif cond == "skip_subject":
                            rs = [RowSettings(skip=sorted(set(p["skip"]) | set(p["outside"]))) for p in chunk]
                        else:
                            rs = [RowSettings(skip=p["outside"]) for p in chunk]
                        method = "top" if top_k(cond) is not None else "omp"
                        d = (unembed if cond.startswith("unembed") else pca[la] if cond.startswith("pca") else rdict[la] if cond.endswith("_rdict")
                             else gauss[la] if cond == "gauss" else dic[la])  # fmt: skip
                        keep = None
                        if keep_kind(cond):  # amendment 64 note 37: the span A of the J++ unit vectors at this layer of the
                            # relation's answers (--keepA-forms; QR as answer_span_edit), kept out of paper10's r; note 41: R, R2, R4
                            keep = [kept_span(i, la, keep_kind(cond)) for i in range(len(chunk))]
                        observe = None
                        if cond == "paper10" and (rand_rows or n44 or has_keepA):  # note 41 addendum / note 44 / amendment 72: paper10's removal energy per span
                            def observe(r, B, T, la=la):
                                for b in range(B):
                                    rb = r[b * T : (b + 1) * T].double()
                                    if rand_rows:
                                        n = a_rows[b].numel()
                                        e4 = (rb @ kept_span(b, la, "R4")).pow(2).sum(0)  # per column of the nested basis
                                        energy[b] += torch.stack([rb.pow(2).sum(), (rb @ kept_span(b, la, "A")).pow(2).sum(),
                                                                  e4[:n].sum(), e4[: 2 * n].sum(), e4.sum()])  # fmt: skip
                                    elif has_keepA:  # amendment 72 (shared): A only
                                        energy[b] += torch.stack([rb.pow(2).sum(), (rb @ kept_span(b, la, "A")).pow(2).sum()])
                                    if n44:
                                        qc, qt = kept_span(b, la, "Cap"), kept_span(b, la, "Cty")
                                        e44[b] += torch.stack([rb.pow(2).sum(), (rb @ qc).pow(2).sum(), (rb @ qt).pow(2).sum(),
                                                               (rb @ kept_span(b, la, "CapCty")).pow(2).sum()])  # fmt: skip
                                        qp = torch.linalg.qr(dic[la].atoms(n44["pool"][b]).double().T)[0]  # nested: prefixes span prefixes
                                        e44pool[b] += (rb @ qp).pow(2).sum(0)
                                        ov44[b] += (qc.T @ qt).pow(2).sum() / min(qc.shape[1], qt.shape[1]) / len(band)
                        holder: dict = {}
                        if (cond == "paper10" and (n4950 or n52on)) or (cond in (f"top{k_}" for k_ in n51ks)):  # amendment 72 log
                            def observe(r, B, T, la=la, cond=cond, base=observe, holder=holder):
                                if base is not None:
                                    base(r, B, T)
                                observe72(r, B, T, la, cond, holder["h"])
                        need57 = n57on and (cond == "paper10" or cond in (f"top{k_}" for k_ in re_ks))
                        if need57:  # amendment 78 note 57: the energy matching (onlyRperp's, keepRE's sizes)
                            def observe(r, B, T, la=la, cond=cond, base=observe, holder=holder):
                                if base is not None:
                                    base(r, B, T)
                                obs57(r, B, T, la, cond, holder["h"])
                        edits[la] = removal_edit(
                            method,
                            d,
                            rs,
                            rotation=rot[la] if cond.endswith("_rot") else None,
                            k=top_k(cond),
                            skip_sinks="_nosink" in cond,
                            size_match=pca[la].D[:PCA_K] if cond.endswith("_pcasize") else None,
                            keep_span=keep,
                            observe=observe,
                            **({"chunk": args.topk_chunk} if args.topk_chunk and top_k(cond) is not None and top_k(cond) > 10 else {}),
                        )
                        if holder is not None and observe is not None and (cond == "paper10" and (n4950 or n52on) or cond in (f"top{k_}" for k_ in n51ks) or need57):
                            def with_h(h, inner=edits[la], holder=holder):  # the residual, for observe72 (output unchanged)
                                holder["h"] = h
                                return inner(h)

                            edits[la] = with_h
                    if n57on and cond == "ansJ" and any(n57_kind(c) == "ansRe" for c in args.conditions):  # note 57: ansRe's size

                        def ans_obs(inner, la_):
                            def f(h: torch.Tensor) -> torch.Tensor:
                                obs57_ans(h, la_)
                                return inner(h)

                            return f

                        edits = {la_: ans_obs(e_, la_) for la_, e_ in edits.items()}
                    edits = {la_: measured(e_, emask, acc72) for la_, e_ in edits.items()}  # amendment 72: |edit| / |h|, every row
                    logits = first_token_logits(model, ids, edits, last)
                    if "_nosink" in cond:  # attention-sink positions left unedited: counted per band x condition
                        tally = sink_tally.setdefault(f"{label(band)}/{cond}", [0, 0])
                        for e in edits.values():
                            tally[0] += e.sinks[0]
                            tally[1] += e.sinks[1]
                            e.sinks[0] = e.sinks[1] = 0
                    logp = logits.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
                    retained = []  # note 41 addendum: per row, the share of paper10's removal energy (summed over the edited
                    if cond == "paper10" and rand_rows:  # positions and the band's layers) lying in A, R, R2, R4
                        e = energy.tolist()
                        retained = [{"energy": x[0], **{k: (x[j] / x[0] if x[0] > 0 else None) for j, k in enumerate(("A", "R", "R2", "R4"), 1)}}
                                    for x in e]  # fmt: skip
                    elif cond == "paper10" and has_keepA:  # amendment 72 (shared): A's retained share when no note 41 rows are drawn
                        retained = [{"energy": x[0], "A": (x[1] / x[0] if x[0] > 0 else None)} for x in energy.tolist()]
                    retained44 = []  # note 44: the same shares for Cap, Cty, CapCty; Rcap = the smallest prefix of the item's pool whose
                    if n44 and cond == "paper10":  # share is not below Cap's (all of it if none reaches), used by paper10_keepRcap
                        cum = e44pool.cumsum(1)
                        for b in range(len(chunk)):
                            hit = (cum[b] >= e44[b, 1]).nonzero()
                            n44["k"][b] = int(hit[0]) + 1 if hit.numel() else cum.shape[1]
                            tot = float(e44[b, 0])
                            retained44.append({"energy": tot, **{k: (float(e44[b, j]) / tot if tot > 0 else None) for j, k in enumerate(("Cap", "Cty", "CapCty"), 1)},
                                               "Rcap": float(cum[b, n44["k"][b] - 1]) / tot if tot > 0 else None, "k_Rcap": n44["k"][b],
                                               "Rcap_reached": bool(hit.numel()), "n_cap": int(cap_rows.numel()), "n_cty": int(n44["cty"][b].numel()),
                                               "shared_rows": len(set(cap_rows.tolist()) & set(n44["cty"][b].tolist())),
                                               "span_overlap": float(ov44[b])})  # fmt: skip
                    if cond in acc57:  # note 57: the energy-matched sizes from this forward
                        finalize57(cond)
                    k72 = []  # amendment 72: the new conditions' own |edit| / |h| and kept rank (or protected rows), mean over layers
                    if n49_kind(cond) or is_n51(cond) or is_n52(cond) or n57_kind(cond):
                        for row in range(len(chunk)):
                            rk_ = rank72[cond][row] if not is_n51(cond) else [kept_span(row, la_, "A").shape[1] for la_ in band]
                            k72.append({"rank": sum(rk_) / len(rk_) if rk_ else None})
                    if cond == "paper10" and n52on and any(f"paper10_keepR{kk}" in args.conditions for kk in N52_KEEPS):
                        for b in range(len(chunk)):  # note 52b: k = the smallest Rcap-pool prefix whose energy reaches the span's
                            l = log72["paper10"][b]
                            cum = e44pool[b].cumsum(0)
                            l["n_pool"] = int(cum.numel())
                            for kk in N52_KEEPS:
                                if f"paper10_keepR{kk}" in args.conditions:
                                    hit = (cum >= l["E_" + kk]).nonzero()
                                    k52b[kk][b] = int(hit[0]) + 1 if hit.numel() else int(cum.numel())
                                    l["k_R" + kk], l["reached_R" + kk] = k52b[kk][b], bool(hit.numel())
                                    l["E_R" + kk] = float(cum[k52b[kk][b] - 1])
                    if cond in log72:  # paper10's / topK's per-item log (keeplog.jsonl)
                        with (out_dir / "keeplog.jsonl").open("a") as fh:
                            fh.writelines(json.dumps({"band": label(band), **keeplog_line(cond, b)}) + "\n" for b in range(len(chunk)))
                        del log72[cond]
                    for row, p in enumerate(chunk):
                        rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": label(band),
                                         "condition": cond, **reads(logits[row], p, args.read),
                                         "logp": float(logp[row]), "bridge_protected": shields[row], "bridge": p["bridge"],
                                         **({"retained": retained[row]} if retained else {}),
                                         **({"retained44": retained44[row]} if retained44 else {}),
                                         **({"keeplog": k72[row]} if k72 else {}),
                                         "edit_rel": float(acc72[row, 0] / acc72[row, 1]) if acc72[row, 1] > 0 else None})  # fmt: skip
                band_seconds[label(band)] += time.time() - tb
            with rows_path.open("a") as fh:  # this batch's rows, so partial results are readable during the run
                fh.writelines(json.dumps(r) + "\n" for r in rows_out[written:])
            written = len(rows_out)
            print(f"{len(rows_out)} rows, {time.time() - t0:.0f}s", flush=True)

    base = {(r["family"], r["id"], r["kind"]): r for r in rows_out if r["condition"] == "none"}
    cells: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (bl, fk, cond), rs in _group(rows_out).items():
        cells[bl][fk][cond] = {"n": len(rs), "accuracy": statistics.mean(r["correct"] for r in rs),
                               "dlogp": statistics.mean(r["logp"] - base[(r["family"], r["id"], r["kind"])]["logp"] for r in rs)}  # fmt: skip
    none_acc = {
        fk: statistics.mean(r["correct"] for r in rs) for (bl, fk, cond), rs in _group(rows_out, none=True).items()
    }
    summary = {"seconds": round(time.time() - t0), "band_seconds": {k: round(v) for k, v in band_seconds.items()},
               "unedited_accuracy": none_acc, "cells": cells,
               "sink_positions": {k: {"skipped": v[0], "positions": v[1]} for k, v in sink_tally.items()}}  # fmt: skip
    if args.plan == "v1check":
        summary["v1_agreement"] = v1_agreement(rows_out)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# ablate_v2 / {args.name}: {len(prompts)} prompts, {time.time() - t0:.0f}s", "",
             "Unedited accuracy: " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in none_acc.items()), ""]  # fmt: skip
    fks = list(none_acc)
    for cond in args.conditions:
        lines += [
            f"## {cond}: accuracy (%) by band",
            "",
            "| band | " + " | ".join(fks) + " |",
            "|---" * (len(fks) + 1) + "|",
        ]
        for band in bands:
            c = cells[label(band)]
            lines.append(
                f"| {label(band)} | "
                + " | ".join(f"{100 * c[fk][cond]['accuracy']:.0f}" if cond in c[fk] else "-" for fk in fks)
                + " |"
            )
        lines.append("")
    if args.plan == "v1check":
        lines += ["## agreement with ablate_pilot v1 (same items)", "", json.dumps(summary["v1_agreement"], indent=1)]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text()[:3000])


def _group(rows: list[dict], none: bool = False) -> dict:
    g: dict = collections.defaultdict(list)
    for r in rows:
        if (r["condition"] == "none") == none:
            g[(r["band"], f"{r['family']}/{r['kind']}", r["condition"])].append(r)
    return g


def v1_agreement(rows: list[dict]) -> dict:
    """Item-by-item agreement with ablate_pilot v1 (omp25 vs v1's 'jspace', gauss vs 'random', none vs 'none')."""
    v1 = {}
    for line in (A.RESULTS / "v1" / "rows.jsonl").read_text().splitlines():
        r = json.loads(line)
        v1[(r["family"], r["id"], r["kind"], r["condition"])] = r
    names = {"none": "none", "omp25": "jspace", "gauss": "random"}
    out = {}
    for ours, theirs in names.items():
        pairs = [(r, v1.get((r["family"], r["id"], r["kind"], theirs))) for r in rows if r["condition"] == ours]
        pairs = [(a, b) for a, b in pairs if b is not None]
        if pairs:
            out[ours] = {"n": len(pairs), "same_correct": statistics.mean(a["correct"] == b["correct"] for a, b in pairs),
                         "median_abs_dlogp": statistics.median(abs(a["logp"] - b["logp"]) for a, b in pairs),
                         "accuracy_ours": statistics.mean(a["correct"] for a, _ in pairs),
                         "accuracy_v1": statistics.mean(b["correct"] for _, b in pairs)}  # fmt: skip
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--plan", choices=["v1check", "coarse", "depth", "bands"], required=True)
    ap.add_argument("--bands", nargs="*", default=[], help='with --plan bands: "32,36,40" or "16-28"')
    ap.add_argument("--conditions", nargs="+", default=["omp25", "omp25_rot", "omp25_rdict", "paper10", "paper10_rot",
                                                        "paper10_rdict"],
                    help=f"{', '.join(CONDITIONS)}, or topK[_rot|_rdict] (the top K lens directions, answer kept)")  # fmt: skip
    ap.add_argument("--families", nargs="+", default=["BL", "BR", "RL", "RR", "R", "B"])
    ap.add_argument("--kinds", nargs="+", default=["clean"], choices=["clean", "hop", "step1", "step2", "step3"])
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--sample-per-word", type=int, default=0, help="tasks: a seeded random N items per word (0: all eligible, then --n)")
    ap.add_argument("--sample-seed", type=int, default=0)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument(
        "--pad", action="store_true", help="length-sorted right-padded batches (validated against exact-length)"
    )
    ap.add_argument("--no-tf32", action="store_true", help="full fp32 matmuls (the v1 numerics check)")
    ap.add_argument("--dict-digits", action="store_true", help="add digit tokens to the letter-token dictionary (amendment 21 note)")
    ap.add_argument("--tasks", default=None, help="a tasks_v2 set to draw prompts from instead of the suite")
    ap.add_argument("--read", choices=["top", "cand", "cand2"], default="top",
                    help='"cand" (natural_v1 only): correct = top among the relation\'s candidate answers')
    ap.add_argument("--tasks-competence", default=None, help="its competence run (eligibility: every part right)")
    ap.add_argument("--tasks-words", nargs="*", default=None, help="tasks_v2 words to include (default: all)")
    ap.add_argument("--skip", type=int, default=0, help="skip the first K eligible items per family (a fresh sample)")
    ap.add_argument("--wording", default="A", choices=["A", "B"], help="the suite's wording (B: data/suite_v1_b)")
    ap.add_argument(
        "--competence", default=None, help="a new target's suite_v1 competence run (BL BR RL RR eligibility)"
    )
    ap.add_argument("--countries-build", action="store_true", help="a new target: build its country cases now")
    ap.add_argument("--answertype", type=int, default=0, help="add N tool_answer_type scenes (AT-name, AT-digit)")
    ap.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="added to the rotation and rotated-dictionary seeds (another draw of the random controls)",
    )
    ap.add_argument("--tasks-level", default="pick", help='tasks_v2 level: "pick" (calibrated), "all" or a number')
    ap.add_argument(
        "--tasks-strata", nargs="+", default=["core"], help="tasks_v2 strata (core, secondary: planets 3-step)"
    )
    ap.add_argument("--tasks-per-word", action="store_true", help="tasks_v2: judge each item on its own (three-step)")
    ap.add_argument("--tasks-v4-h1", default=None, help="note 20: v4's H1 competence_variants run; keep v4_split's ok items only")
    ap.add_argument("--tasks-scene-words", nargs="*", default=None,
                    help="amendment 58 note 4 (v3): a scene passes when its items of these words are right; the compared words are kept on it")
    ap.add_argument("--workspace", type=int, default=None, help="depth plan: first layer of the workspace range")
    ap.add_argument("--positions", default="all", choices=["all", "context", "question", "final", "bridge", "desc"],
                    help="where to remove: every position, only before the question (the facts), only from the "
                         "question on (question, instruction, 'Answer:'; see question_start), only the last position, "
                         "or only the bridge's mentions (bridge_positions)")  # fmt: skip
    ap.add_argument("--topk-chunk", type=int, default=0,
                    help="amendment 72 note 51: rows per chunk for top-K removals with K > 10 (memory at K = 100); 0: removal_edit's default")
    ap.add_argument("--keepA-forms", dest="keepA_forms", choices=sorted(KEEPA_ROWS), default="every",
                    help="note 37's kept span: every form of the relation's answers (either case, with or without a leading "
                         "space) or cands2 only (ansJ's rows)")  # fmt: skip
    a = ap.parse_args()
    bad = [c for c in a.conditions if c not in CONDITIONS and top_k(c) is None]
    assert not bad, f"unknown conditions {bad}"
    keepa = [c for c in a.conditions if "keep" in c and "keepown" not in c and c != "keep_own"]
    assert all(keep_kind(c) for c in keepa) and (not keepa or a.tasks), f"notes 37 / 41: {keepa} unknown or without --tasks"
    n44c = [c for c in a.conditions if is_n44(c)]
    assert not n44c or (a.tasks and "paper10" in a.conditions and ("paper10_keepRcap" not in a.conditions
                        or a.conditions.index("paper10") < a.conditions.index("paper10_keepRcap"))), \
        f"note 44: {n44c} need --tasks and paper10 in the run, before paper10_keepRcap (it sets Rcap's size)"
    rand = [c for c in a.conditions if is_rand(c)]
    assert not rand or (a.tasks and a.keepA_forms == "every" and "paper10" in a.conditions), \
        f"note 41: {rand} need --tasks, --keepA-forms every and paper10 in the run (the retained-energy log)"
    n57c = [c for c in a.conditions if n57_kind(c)]  # amendment 78 note 57: each matching forward runs before its condition
    pos = {c: i for i, c in enumerate(a.conditions)}
    assert all((n57_kind(c) == "ansRe" and pos.get("ansJ", 1e9) < pos[c]) or (n57_kind(c) == "keepRE" and pos.get(f"top{top_k(c)}", 1e9) < pos[c])
               or (n57_kind(c) not in ("ansRe", "keepRE") and pos.get("paper10", 1e9) < pos[c]) for c in n57c) and not (n57c and any(is_n52(c) for c in a.conditions)), \
        f"note 57: {n57c} need paper10 / topK / ansJ earlier in --conditions (they set the matched sizes), and no note 52 conditions"  # fmt: skip
    assert all(pos.get("paper10", 1e9) < pos[c] for c in a.conditions if keep_kind(c) in ("RShared", "RCapPerp", "RCtyPerp")), \
        "note 52b: paper10 must run before the matched random keeps (it sets their sizes)"
    n72 = [c for c in a.conditions if n49_kind(c) or is_n51(c) or is_n52(c) or n57_kind(c)]  # amendments 72 / 78 / 80
    assert not n72 or (a.tasks and a.keepA_forms == "every" and "paper10" in a.conditions and "paper10_rot" in a.conditions
                       and not any("_nosink" in c for c in n72)
                       and not (any(n49_kind(c) for c in n72) and any(is_n52(c) for c in n72))), \
        f"amendment 72: {n72} need --tasks, --keepA-forms every and paper10 / paper10_rot in the run (notes 49/50 and 52 in separate runs)"  # fmt: skip
    main(a)
