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
              "paper10_keepA", "paper10_keepA_rot")  # fmt: skip  # amendment 64 note 37: paper10's r minus its part in the answers' J++ span
SEED_ROT, SEED_DICT, SEED_GAUSS = 888, 999, 777  # + layer (888 and 777 as ablate_pilot)
KEEPA_ROWS = {"every": "forms", "cands2": "cands2"}  # note 37's kept span: every form, or ansJ's rows (cands2) only


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
    if any("_keepA" in c for c in args.conditions):  # amendment 64 note 37
        manifest["keepA_forms"] = args.keepA_forms
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
            for band in bands:
                tb = time.time()
                for cond in conditions_for(band, args.conditions):
                    edits = {}
                    for la in band:
                        if cond.startswith("ans"):  # amendment 58 note 3: the candidate answers' directions only
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
                        if "_keepA" in cond:  # amendment 64 note 37: the span A of the J++ unit vectors at this layer of the
                            keep = []  # relation's answers (--keepA-forms; QR as answer_span_edit), kept out of paper10's r
                            for p in chunk:
                                rr = row_of[torch.tensor(p[KEEPA_ROWS[args.keepA_forms]], device="cuda")]
                                rr = rr[rr >= 0].unique()
                                ck = (la, tuple(rr.tolist()))
                                if ck not in span_cache:
                                    span_cache[ck] = torch.linalg.qr(dic[la].atoms(rr).double().T)[0]
                                keep.append(span_cache[ck])
                        edits[la] = removal_edit(
                            method,
                            d,
                            rs,
                            rotation=rot[la] if cond.endswith("_rot") else None,
                            k=top_k(cond),
                            skip_sinks="_nosink" in cond,
                            size_match=pca[la].D[:PCA_K] if cond.endswith("_pcasize") else None,
                            keep_span=keep,
                        )
                    logits = first_token_logits(model, ids, edits, last)
                    if "_nosink" in cond:  # attention-sink positions left unedited: counted per band x condition
                        tally = sink_tally.setdefault(f"{label(band)}/{cond}", [0, 0])
                        for e in edits.values():
                            tally[0] += e.sinks[0]
                            tally[1] += e.sinks[1]
                            e.sinks[0] = e.sinks[1] = 0
                    logp = logits.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
                    for row, p in enumerate(chunk):
                        rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": label(band),
                                         "condition": cond, **reads(logits[row], p, args.read),
                                         "logp": float(logp[row]), "bridge_protected": shields[row], "bridge": p["bridge"]})  # fmt: skip
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
    ap.add_argument("--keepA-forms", dest="keepA_forms", choices=sorted(KEEPA_ROWS), default="every",
                    help="note 37's kept span: every form of the relation's answers (either case, with or without a leading "
                         "space) or cands2 only (ansJ's rows)")  # fmt: skip
    a = ap.parse_args()
    bad = [c for c in a.conditions if c not in CONDITIONS and top_k(c) is None]
    assert not bad, f"unknown conditions {bad}"
    keepa = [c for c in a.conditions if "keepA" in c]
    assert set(keepa) <= {"paper10_keepA", "paper10_keepA_rot"} and (not keepa or a.tasks), f"note 37: {keepa} needs --tasks"
    main(a)
