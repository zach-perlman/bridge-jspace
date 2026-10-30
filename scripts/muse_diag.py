"""muse_diag (Zach, 2026-10-22; docs/breadth/prereg_replication_1022.md amendment 6C): why can Muse's recalls be steered through
the lens but not knocked out? On full_v8's memory-final words (P->M, M->M), items the model gets right, at the model's
C1 band, the paper10 knock-out is replayed one prompt at a time with its removals logged:
- (a) the bridge's rank in the lens readout (letter tokens; best of its surface forms) at each band layer, clean, at the
  final position and at the best position of the question span (question_start .. final);
- (b) whether the knock-out removes the bridge (any surface form among the 10 removed directions) at one or more band
  layers, at the final position / at some question-span position;
- (c) the bridge's rank 2 and 4 layers after the band, clean vs under the knock-out;
- the answer, clean and under the knock-out (a check against the C1 run).
The question-span measure stands in for the pre-registered "question's last token" (the span includes it). Descriptive.
BJ_TARGET=... python scripts/muse_diag.py --name N --why W --band LO-HI [--n 60]
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch

from bridge_jspace import pins
from bridge_jspace.ablate import LensDictionary, top_span_removal
from bridge_jspace.lens import JLens
from bridge_jspace.model import load_model
from scripts.ablate_v2 import question_start, tasks_prompts

OUT = pins.RESULTS_DIR / "muse_diag"


@torch.no_grad()  # 2026-10-23: without it each LensDictionary kept a vocab x d autograd graph (2.8 GiB on the 122B)
def main(a) -> None:
    out_dir = OUT / a.name
    assert not out_dir.exists(), f"{out_dir} exists; results are written once"
    lo, hi = (int(x) for x in a.band.split("-"))
    band, after = list(range(lo, hi + 1)), [hi + 2, hi + 4]
    model = load_model()
    tok = model.tokenizer
    comp = a.competence or f"{pins.TARGETS[pins.TARGET]['run_prefix'] if pins.TARGET != 'qwen3.6-27b' else ''}full_v8_competence_v1"
    prompts = [p for p in tasks_prompts(tok, a.set, comp, ["PM", "MM"], a.n, ["clean"], "all") if p["bridge"]]
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band + after if la < pins.TARGETS[pins.TARGET]["n_layers"] - 1}
    after = [la for la in after if la in dic]
    rows, t0 = [], time.time()
    for p in prompts:
        ids = torch.tensor([p["ids"]], device="cuda")
        T = ids.shape[1]
        q0 = question_start(tok, p["ids"])
        span = torch.arange(q0, T, device="cuda")
        brows = torch.tensor(sorted({int(row_of[i]) for i in model.surface_ids(p["bridge"]) if int(row_of[i]) >= 0}), device="cuda")
        if not brows.numel():
            continue

        def rank(la: int, h: torch.Tensor, pos: torch.Tensor) -> int:
            lg = dic[la].logits(h[pos].float())  # [m, n]
            best = lg[:, brows].max(dim=1).values  # [m]
            return int((lg > best[:, None]).sum(dim=1).min())

        clean_logits, rec = model.run(ids, {}, record=tuple(band + after))
        prot = row_of[clean_logits.topk(10).indices]
        prot = prot[prot >= 0]
        removed = {"final": False, "span": False}

        def edit_for(la: int):
            def edit(h: torch.Tensor) -> torch.Tensor:
                proj, top = top_span_removal(dic[la], h, 10, protected=[(torch.arange(T, device="cuda"), prot)], return_chosen=True)
                hit = torch.isin(top, brows).any(dim=1)  # [T]
                removed["final"] |= bool(hit[T - 1])
                removed["span"] |= bool(hit[q0:].any())
                return h - proj

            return edit

        ko_logits, rec_ko = model.run(ids, {la: edit_for(la) for la in band}, record=tuple(after))
        fin = torch.tensor([T - 1], device="cuda")
        rows.append({
            "word": p["family"], "id": p["id"], "bridge": p["bridge"],
            "clean_rank_final": {la: rank(la, rec[la], fin) for la in band},
            "clean_rank_span": {la: rank(la, rec[la], span) for la in band},
            "removed_final": removed["final"], "removed_span": removed["span"],
            "after_clean_final": {la: rank(la, rec[la], fin) for la in after}, "after_ko_final": {la: rank(la, rec_ko[la], fin) for la in after},
            "after_clean_span": {la: rank(la, rec[la], span) for la in after}, "after_ko_span": {la: rank(la, rec_ko[la], span) for la in after},
            "correct_clean": int(clean_logits.argmax()) == p["tok"], "correct_ko": int(ko_logits.argmax()) == p["tok"],
        })  # fmt: skip
    ok = [r for r in rows if r["correct_clean"]]
    pct = lambda xs: round(100 * statistics.mean(xs), 1) if xs else None  # noqa: E731
    med = lambda xs: statistics.median(xs) if xs else None  # noqa: E731
    summ = {"target": pins.TARGET, "band": a.band, "n_items": len(ok), "by_word": {}}
    for w in ("PM", "MM", "all"):
        R = [r for r in ok if w == "all" or r["word"] == w]
        summ["by_word"][w] = {
            "n": len(R),
            "bridge_in_clean_top10_final_any_band_layer": pct([min(r["clean_rank_final"].values()) < 10 for r in R]),
            "bridge_in_clean_top10_span_any_band_layer": pct([min(r["clean_rank_span"].values()) < 10 for r in R]),
            "median_best_clean_rank_final": med([min(r["clean_rank_final"].values()) for r in R]),
            "median_best_clean_rank_span": med([min(r["clean_rank_span"].values()) for r in R]),
            "removed_final": pct([r["removed_final"] for r in R]), "removed_span": pct([r["removed_span"] for r in R]),
            "accuracy_ko": pct([r["correct_ko"] for r in R]),
            "accuracy_ko_if_removed_span": pct([r["correct_ko"] for r in R if r["removed_span"]]),
            "accuracy_ko_if_not_removed_span": pct([r["correct_ko"] for r in R if not r["removed_span"]]),
            "median_rank_after": {f"L{la}": {"clean_final": med([r["after_clean_final"][la] for r in R]), "ko_final": med([r["after_ko_final"][la] for r in R]),
                                             "clean_span": med([r["after_clean_span"][la] for r in R]), "ko_span": med([r["after_ko_span"][la] for r in R])}
                                  for la in after},
        }  # fmt: skip
    summ.update({"seconds": round(time.time() - t0), "command": " ".join(sys.argv), "why": a.why, "doc": __doc__.split("\n\n")[0]})
    out_dir.mkdir(parents=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print("DIAG", json.dumps({w: {k: v for k, v in d.items() if k != "median_rank_after"} for w, d in summ["by_word"].items()}))
    print("DIAG after", json.dumps(summ["by_word"]["all"]["median_rank_after"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--set", default="full_v8")  # 2026-10-23: the 122B's competence ran on full_v8_two (full_v8's two-step ids)
    ap.add_argument("--competence", default=None, help="competence run (default: PREFIX + full_v8_competence_v1)")
    main(ap.parse_args())
