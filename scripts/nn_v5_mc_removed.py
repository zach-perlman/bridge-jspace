"""nn_v5_mc_removed (Zach, 2026-10-30, prereg amendment 63 note 35 and its addendum): two per-prompt records that
ablate_v2's rows do not keep, for note 35's answer exclusion and margin matching.

  removal (default): ablate_v2's paper10 at the band, re-run on the knock-out's own prompts (tasks_prompts, the per-word
    eligibility, v4_split's gate, exact-length batches, TF32, the frozen lens, protected = the unedited top-10 tokens'
    rows; BJ_GRAM_PROJ as exported) with removal_edit's top path written out so the chosen rows can be read. Per prompt:
    how many (position, band layer) removals took the answer's first-token J++ row (every position is edited, as
    --positions all), whether any did (note 35's exclusion), the same for any form of the answer's first token (either
    case, with or without a leading space), and the edited cand2 read (checked against the knock-out run's paper10 rows
    with --ko-run).
  margins (--margin-only, and in removal runs too): the unedited cand2 margin, the right candidate's logit minus the best
    other candidate's (the read's own candidates, cands2 / ok2, as ablate_v2.reads).

python scripts/nn_v5_mc_removed.py --name N --why W --bands 12-16 --tasks jsuite_v5kn2c_test_chat --tasks-competence C
    --tasks-words MC MC0 --kinds clean step2 --tasks-v4-h1 CV --batch 32 [--ko-run RUN]
python scripts/nn_v5_mc_removed.py --name N --why W --bands 12-16 --tasks jsuite_v5kn2_test_chat --tasks-competence C
    --tasks-words MP --kinds clean --tasks-v4-h1 CV --batch 32 --margin-only
Writes results/ablate_v2/N/{manifest.json, rows.jsonl, summary.json}.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.ablate import K_PAPER, LensDictionary, first_token_logits, top_span_removal  # noqa: E402
from scripts import ablate_v2 as AV  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

CHUNK = 4096  # removal_edit's rows per call (k <= 100)


def answer_of(items: dict, p: dict) -> str:
    it = items[p["id"]]
    return it["answer"] if p["kind"] == "clean" else it["steps"][int(p["kind"][4:]) - 1]["answer"]


@torch.no_grad()
def main(a) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(a.name)
    out = AV.RESULTS / a.name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    torch.backends.cuda.matmul.allow_tf32 = True  # as ablate_v2 without --no-tf32
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    (band,) = AV.make_bands("bands", pins.N_LAYERS, a.bands)
    prompts = AV.tasks_prompts(tok, a.tasks, a.tasks_competence, a.tasks_words, a.n, a.kinds, "all", ("core",), True, None)
    if a.tasks_v4_h1:  # the knock-out's gate (ablate_v2 --tasks-v4-h1)
        from scripts.nn_swap import v4_split

        ok = {i for i, s in v4_split(a.tasks_competence, a.tasks_v4_h1, a.tasks).items() if s == "ok"}
        prompts = [p for p in prompts if p["id"] in ok]
    items = {it["id"]: it for it in T.load(a.tasks)}
    import os

    (out / "manifest.json").write_text(json.dumps({
        "run": a.name, "why": a.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "git_commit": commit,
        "git_state": pins.git_state(), "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
        "band": AV.label(band), "condition": None if a.margin_only else "paper10", "k": K_PAPER, "positions": "all",
        "tasks": [a.tasks, a.tasks_competence, a.tasks_words, "all"], "tasks_per_word": True, "tasks_v4_h1": a.tasks_v4_h1,
        "kinds": a.kinds, "n": a.n, "batch": a.batch, "tf32": True, "bj_gram_proj": bool(os.environ.get("BJ_GRAM_PROJ")),
        "margin_only": a.margin_only, "ko_run": a.ko_run, "n_prompts": len(prompts), "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    print(len(prompts), "prompts; band", AV.label(band), flush=True)

    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {}
    if not a.margin_only:
        lens = JLens(model, pins.FROZEN_LENS)
        dic = {la: LensDictionary(wg, lens.J(la)) for la in band}

    def rows_of(toks: set[int]) -> torch.Tensor:
        r = row_of[torch.tensor(sorted(toks), device="cuda")]
        return r[r >= 0].unique()

    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    rows, t0 = [], time.time()
    for group in by_len.values():
        for start in range(0, len(group), a.batch):
            chunk = group[start : start + a.batch]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            clean = first_token_logits(model, ids, {}, None)
            recs = []
            for row, p in enumerate(chunk):
                right = [t for t in p["cands2"] if t in set(p["ok2"])]
                wrong = [t for t in p["cands2"] if t not in set(p["ok2"])]
                lg = clean[row]
                margin = float(lg[right].max() - lg[wrong].max()) if right and wrong else None
                r0 = AV.reads(clean[row], p, "cand2")
                recs.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "margin2": None if margin is None else round(margin, 4),
                             "correct_cand2_none": r0["correct_cand2"], "correct_top_none": r0["correct_top"]})  # fmt: skip
            if not a.margin_only:
                protected = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]  # as ablate_v2
                ex, fm = [], []
                for p in chunk:
                    ans, k = answer_of(items, p), items[p["id"]]["kind"]
                    ex.append(rows_of({p["tok"]}))
                    fm.append(rows_of({S.answer_token(tok, ans, k), S.answer_token(tok, ans.lower(), k), S.ids(tok, " " + ans)[0],
                                       S.ids(tok, " " + ans.lower())[0]}))  # fmt: skip
                hits = [[0, 0] for _ in chunk]  # (position, layer) removals taking the answer token's row / any form's row

                def make_edit(D):
                    def edit(h: torch.Tensor) -> torch.Tensor:  # removal_edit's "top" path (no skipped positions), recording
                        B, Tn, d = h.shape
                        x = h.reshape(B * Tn, d).float()
                        r = torch.zeros_like(x)
                        idx = torch.arange(B * Tn, device=h.device)
                        for s in range(0, idx.numel(), CHUNK):
                            sel = idx[s : s + CHUNK]
                            owner = sel // Tn
                            groups = []
                            for b in owner.unique().tolist():
                                if protected[b].numel():
                                    groups.append(((owner == b).nonzero().squeeze(1), protected[b]))
                            proj, top = top_span_removal(D, x[sel], K_PAPER, protected=groups, return_chosen=True)
                            r[sel] = proj
                            for b in owner.unique().tolist():
                                tb = top[owner == b]
                                hits[b][0] += int(torch.isin(tb, ex[b]).any(dim=1).sum()) if ex[b].numel() else 0
                                hits[b][1] += int(torch.isin(tb, fm[b]).any(dim=1).sum()) if fm[b].numel() else 0
                        return (x - r).reshape(B, Tn, d)

                    return edit

                logits = first_token_logits(model, ids, {la: make_edit(dic[la]) for la in band}, None)
                for row, (p, rec) in enumerate(zip(chunk, recs, strict=True)):
                    rec.update({"answer_row_hits": hits[row][0], "answer_row_removed": hits[row][0] > 0, "any_form_hits": hits[row][1],
                                "any_form_removed": hits[row][1] > 0, "answer_has_row": bool(ex[row].numel()),
                                "correct_cand2_paper10": AV.reads(logits[row], p, "cand2")["correct_cand2"]})  # fmt: skip
            rows += recs
            print(f"{len(rows)} rows, {time.time() - t0:.0f}s", flush=True)
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summ: dict = {"seconds": round(time.time() - t0), "n": len(rows), "cells": {}}
    for fk in sorted({(r["family"], r["kind"]) for r in rows}):
        rs = [r for r in rows if (r["family"], r["kind"]) == fk]
        ms = [r["margin2"] for r in rs if r["margin2"] is not None]
        cell = {"n": len(rs), "margin2_median": round(statistics.median(ms), 3) if ms else None,
                "acc_none": round(statistics.mean(r["correct_cand2_none"] for r in rs), 4)}  # fmt: skip
        if not a.margin_only:
            cell.update({"answer_row_removed": round(statistics.mean(r["answer_row_removed"] for r in rs), 4),
                         "any_form_removed": round(statistics.mean(r["any_form_removed"] for r in rs), 4),
                         "acc_paper10": round(statistics.mean(r["correct_cand2_paper10"] for r in rs), 4)})  # fmt: skip
        summ["cells"]["/".join(fk)] = cell
    if a.ko_run:  # the same prompts' reads in the knock-out run: unedited, and paper10 (the re-run must reproduce them)
        ko = {}
        for line in (AV.RESULTS / a.ko_run / "rows.jsonl").open():
            r = json.loads(line)
            if r["condition"] in ("none", "paper10"):
                ko[(r["family"], r["id"], r.get("kind", "clean"), r["condition"])] = bool(r["correct_cand2"])
        agree = collections.Counter()
        for r in rows:
            for cond, key in (("none", "correct_cand2_none"), ("paper10", "correct_cand2_paper10")):
                k = (r["family"], r["id"], r["kind"], cond)
                if key in r and k in ko:
                    agree[(cond, ko[k] == r[key])] += 1
        summ["ko_agreement"] = {f"{c}/{'same' if s else 'differ'}": v for (c, s), v in sorted(agree.items())}
    (out / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--bands", nargs=1, required=True, help='the knock-out band, e.g. "12-16"')
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--tasks-competence", required=True)
    ap.add_argument("--tasks-words", nargs="+", required=True)
    ap.add_argument("--tasks-v4-h1", default=None)
    ap.add_argument("--kinds", nargs="+", default=["clean"], choices=["clean", "step1", "step2", "step3"])
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--margin-only", action="store_true", help="unedited margins only (no removal re-run)")
    ap.add_argument("--ko-run", default=None, help="the knock-out run of the same prompts, for the agreement check")
    main(ap.parse_args())
