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
  gauss (v1's Gaussian dictionary). Prompt kinds (--kinds): clean (the whole question), hop (the last step alone, as
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
              "skip_subject", "gauss")  # fmt: skip
SEED_ROT, SEED_DICT, SEED_GAUSS = 888, 999, 777  # + layer (888 and 777 as ablate_pilot)


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
                  level: str = "pick", strata: tuple[str, ...] = ("core",)) -> list[dict]:  # fmt: skip
    """tasks_v2 items of the compared words (--tasks-words) from scenes the model gets right on them throughout, at
    one level for the comparison (tasks_v2.eligible), first n per word; the whole question ('clean') and each step
    alone ('stepN'), each with its own instruction, read as the suite reads them (a digit after 'Answer: ')."""
    from scripts import tasks_v2 as T

    assert words, "--tasks-words: name the compared words (they set the level and the eligibility)"
    out = []
    for it in T.eligible(set_name, comp_run, words, n, level, strata=tuple(strata)):
        parts = [("clean", it["question"], it["answer"], it["kind"])]
        parts += [(f"step{i}", st["question"], st["answer"], st["kind"]) for i, st in enumerate(it["steps"], 1)]
        for kind, q, a, k in parts:
            if kind not in kinds:
                continue
            ids = S.ids(tok, T.render(tok, {**it, "_question": q, "_kind": k})) + (
                S.ids(tok, " ") if k == "digit" else []
            )
            out.append({"family": it["word"], "id": it["id"], "kind": kind, "ids": ids, "tok": S.answer_token(tok, a, k),
                        "bridge": it["steps"][0]["answer"], "domain": it["domain"], "format": it["format"]})  # fmt: skip
    return out


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
    """K of a top-K condition: paper10 (K = 10) or topK, with any control suffix; None for OMP and others."""
    if cond.startswith("paper10"):
        return 10
    m = re.fullmatch(r"top(\d+)(_rot|_rdict)?", cond)
    return int(m[1]) if m else None


def conditions_for(band: tuple[int, ...], conditions: list[str]) -> list[str]:
    return [c for c in conditions if len(band) <= WIDE or top_k(c) is not None]


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
                "git_commit": commit, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "plan": args.plan, "bands": [label(b) for b in bands], "conditions": args.conditions,
                "families": args.families, "kinds": args.kinds, "skip": args.skip, "wording": args.wording, "n_per_family": args.n, "batch": args.batch,
                "tf32": not args.no_tf32, "workspace_start": args.workspace, "positions": args.positions, "pad": args.pad, "competence": args.competence, "countries_build": args.countries_build, "tasks": [args.tasks, args.tasks_competence, args.tasks_words, args.tasks_level, args.tasks_strata], "wide": WIDE, "seed_offset": args.seed_offset, "seeds": {"rotation": f"{SEED_ROT + args.seed_offset}+layer", "rotated_dictionary": f"{SEED_DICT + args.seed_offset}+layer",
                "gauss": f"{SEED_GAUSS}+layer"}, "own_cos": OWN_COS, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
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
        )
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
        p["outside"] = {"all": [], "context": list(range(q0, len(p["ids"]))), "question": list(range(q0))}[
            args.positions
        ]
    print(len(prompts), "prompts;", len(bands), "bands;", len(args.conditions), "conditions", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    layers = sorted({la for b in bands for la in b})
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    rot = {la: rotation(wg.shape[1], SEED_ROT + args.seed_offset + la) for la in layers}
    rdict = {la: RotatedDictionary(dic[la], rotation(wg.shape[1], SEED_DICT + args.seed_offset + la)) for la in layers}
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
                                 "correct": int(clean[row].argmax()) == p["tok"], "logp": float(base_logp[row])})  # fmt: skip
            protected = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            # does the protected set (clean top-10 at the answer position) shield the bridge itself? (logged per row)
            shields = [bool(p["bridge"]) and bool(set(model.surface_ids(p["bridge"])) & set(t.tolist()))
                       for p, t in zip(chunk, clean.topk(10, dim=1).indices, strict=True)]  # fmt: skip
            for band in bands:
                tb = time.time()
                for cond in conditions_for(band, args.conditions):
                    edits = {}
                    for la in band:
                        if top_k(cond) is not None:
                            rs = [RowSettings(skip=p["outside"], protected=protected[i]) for i, p in enumerate(chunk)]
                        elif cond == "keep_own":
                            rs = [RowSettings(skip=p["outside"], banned=own_rows(p["bridge"], la) if p["bridge"] else None)
                                  for p in chunk]  # fmt: skip
                        elif cond == "skip_subject":
                            rs = [RowSettings(skip=sorted(set(p["skip"]) | set(p["outside"]))) for p in chunk]
                        else:
                            rs = [RowSettings(skip=p["outside"]) for p in chunk]
                        method = "top" if top_k(cond) is not None else "omp"
                        d = rdict[la] if cond.endswith("_rdict") else gauss[la] if cond == "gauss" else dic[la]
                        edits[la] = removal_edit(
                            method, d, rs, rotation=rot[la] if cond.endswith("_rot") else None, k=top_k(cond)
                        )
                    logits = first_token_logits(model, ids, edits, last)
                    logp = logits.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
                    for row, p in enumerate(chunk):
                        rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": label(band),
                                         "condition": cond, "correct": int(logits[row].argmax()) == p["tok"],
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
               "unedited_accuracy": none_acc, "cells": cells}  # fmt: skip
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
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument(
        "--pad", action="store_true", help="length-sorted right-padded batches (validated against exact-length)"
    )
    ap.add_argument("--no-tf32", action="store_true", help="full fp32 matmuls (the v1 numerics check)")
    ap.add_argument("--tasks", default=None, help="a tasks_v2 set to draw prompts from instead of the suite")
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
    ap.add_argument("--workspace", type=int, default=None, help="depth plan: first layer of the workspace range")
    ap.add_argument("--positions", default="all", choices=["all", "context", "question"],
                    help="where to remove: every position, only before the question (the facts), or only from the "
                         "question on (question, instruction, 'Answer:'); see question_start")  # fmt: skip
    a = ap.parse_args()
    bad = [c for c in a.conditions if c not in CONDITIONS and top_k(c) is None]
    assert not bad, f"unknown conditions {bad}"
    main(a)
