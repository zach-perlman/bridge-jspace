"""gen_spot (Zach, 2026-10-23, prereg amendment 19): what the model actually says under the knock-out. The candidate
read asks only whether the right answer outranks its relation's other answers at the first token; this decodes the
whole short reply. For eligible items of a natural set (the same eligibility and first-n order as ablate_v2), greedy
continuations (max 12 tokens) unedited and under each condition at one band (edits on prompt positions only, as
ablate_v2; model.generate_batch, one batch row per condition). Each reply is classed: "answer" (starts with the
answer), "bridge" (starts with the bridge or one of its names: hop 1 resolved, hop 2 not given), "other_cand" (starts
with another answer of the relation), "other". The first step's candidate read is recorded too, and checked against
the knock-out run's rows (--check RUN, finished runs only) item by item. Amendment 20: TF32 on as ablate_v2, --read
(default cand2), replies classed by the earliest answer of the relation they name. Descriptive, no rule. Writes
results/gen_spot/NAME/.

python scripts/gen_spot.py --name N --why W --set natplus_v1_chat --competence C --band 32-40 [--n 25] [--check RUN]
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit, rotation  # noqa: E402
from scripts import ablate_v2 as AV  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

RESULTS = pins.RESULTS_DIR / "gen_spot"


def first_hit(text: str, words) -> int | None:
    """Where the earliest whole-word mention of any of words starts (any case, plural s allowed), or None."""
    hits = [m.start() for w in words if (m := re.search(r"\b" + re.escape(w.lower()) + r"s?\b", text.lower()))]
    return min(hits) if hits else None


def classify(text: str, it: dict, vocab: list[str]) -> str:
    """The earliest mentioned answer of the relation decides (the answer: "answer"; for PM the value the passage gives
    the bridge itself: "lure"; another: "other_cand"), so "Bhutan is in Asia" is an answer; a reply naming only the
    bridge (or one of its names) is "bridge"; else "other"."""
    lure = it.get("_lure")  # PM: the bridge's own made-up final-hop value in the shared passage (its PP answer)
    hits = {"answer": first_hit(text, [it["answer"]]), "lure": first_hit(text, [lure]) if lure else None,
            "other_cand": first_hit(text, [v for v in vocab if v not in (it["answer"], lure)])}
    hits = {k: v for k, v in hits.items() if v is not None}
    if hits:
        return min(hits, key=hits.get)
    return "bridge" if first_hit(text, set(it["steps"][0].get("alts", [])) | {it["bridge"]}) is not None else "other"


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    if args.check:  # only a finished knock-out run (amendment 20): a running one's rows.jsonl is partial
        assert (AV.RESULTS / args.check / "summary.json").exists(), f"--check {args.check}: not finished"
        check_read = json.loads((AV.RESULTS / args.check / "manifest.json").read_text())["read"]
    torch.backends.cuda.matmul.allow_tf32 = True  # as ablate_v2 (its default), so the first-step reads match its numerics
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    (band,) = AV.make_bands("bands", pins.N_LAYERS, [args.band])
    conds = ["none"] + args.conditions
    (out_dir / "manifest.json").write_text(json.dumps({
        "run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": commit, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
        "set": args.set, "competence": args.competence, "words": args.words, "level": args.level, "n_per_word": args.n,
        "band": AV.label(band), "conditions": conds, "max_new_tokens": args.max_new, "check": args.check,
        "read": args.read, "tf32": True,
        "seeds": {"rotation": f"{AV.SEED_ROT}+layer"}, "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    prompts = AV.tasks_prompts(tok, args.set, args.competence, args.words, args.n, ["clean"], args.level)
    items = {it["id"]: it for it in T.load(args.set)}
    pp_of = {it["scene"]: it["answer"] for it in items.values() if it["word"] == "PP"}
    for it in items.values():  # amendment 20: PM shares PP's passage, which gives the bridge a made-up value
        if it["word"] == "PM" and pp_of.get(it["scene"]) not in (None, it["answer"]):
            it["_lure"] = pp_of[it["scene"]]
    print(len(prompts), "prompts", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    rot = {la: rotation(wg.shape[1], AV.SEED_ROT + la) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))

    rows_out, t0 = [], time.time()
    for i, p in enumerate(prompts):
        ids = torch.tensor([p["ids"]], device="cuda")
        clean = AV.first_token_logits(model, ids, {})
        protected = row_of[clean.topk(10, dim=1).indices[0]]
        protected = protected[protected >= 0]
        edit_sets = []
        for cond in conds:
            if cond == "none":
                edit_sets.append({})
                continue
            e = {}
            for la in band:
                f = removal_edit("top", unembed if cond.startswith("unembed") else dic[la],
                                 [RowSettings(skip=[], protected=protected)],
                                 rotation=rot[la] if cond.endswith("_rot") else None, k=AV.top_k(cond))  # fmt: skip
                e[la] = lambda h, f=f: f(h[None])[0]
            edit_sets.append(e)
        texts, logits = model.generate_batch(ids, args.max_new, edit_sets, first_logits=True)
        it = items[p["id"]]
        vocab = it.get("answer_vocab") or sorted(AV.natural_vocab(args.set)[(it["domain"], "answer")])
        for cond, text, lg in zip(conds, texts, logits, strict=True):
            rows_out.append({"id": p["id"], "word": p["family"], "condition": cond, "answer": it["answer"],
                             "bridge": it["bridge"], "text": text, "class": classify(text, it, vocab),
                             **AV.reads(lg, p, args.read)})  # fmt: skip
        if i % 20 == 0:
            print(f"{i + 1}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows_out))

    summary: dict = {"seconds": round(time.time() - t0), "band": AV.label(band), "cells": {}}
    ok = {r["id"] for r in rows_out if r["condition"] == "none" and r["correct"]}
    for w in args.words:
        for cond in conds:
            rs = [r for r in rows_out if r["word"] == w and r["condition"] == cond and r["id"] in ok]
            if not rs:
                continue
            cls = collections.Counter(r["class"] for r in rs)
            fails = [r for r in rs if not r["correct"]]
            summary["cells"][f"{w}/{cond}"] = {
                "n": len(rs), "cand_acc": round(sum(r["correct"] for r in rs) / len(rs), 3),
                "class": {k: cls[k] for k in ("answer", "lure", "bridge", "other_cand", "other")},
                "class_of_cand_failures": dict(collections.Counter(r["class"] for r in fails)),
                "other_examples": [r["text"] for r in rs if r["class"] == "other"][:5]}  # fmt: skip
    if args.check:  # the first step's candidate read against the knock-out run's rows, same item and condition
        ko = {(r["id"], r["condition"]): r["correct"] for r in map(json.loads, (AV.RESULTS / args.check / "rows.jsonl").open())
              if r["kind"] == "clean" and r["band"] in ("-", AV.label(band))}  # fmt: skip
        pairs = [(r[f"correct_{check_read}"], ko[(r["id"], r["condition"])]) for r in rows_out if (r["id"], r["condition"]) in ko]
        summary["check"] = {"run": args.check, "read": check_read, "n": len(pairs), "agree": sum(a == b for a, b in pairs)}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    md = [f"# gen_spot / {args.name}: {len(prompts)} prompts at {AV.label(band)}", ""]
    if "check" in summary:
        md += [f"Candidate read vs {args.check}: {summary['check']['agree']} of {summary['check']['n']} agree.", ""]
    md += ["| word / condition | n | cand acc | answer | lure | bridge | other cand | other |", "|---|---|---|---|---|---|---|---|"]
    for k, c in summary["cells"].items():
        md.append(f"| {k} | {c['n']} | {100 * c['cand_acc']:.0f} | " + " | ".join(str(c["class"][x]) for x in ("answer", "lure", "bridge", "other_cand", "other")) + " |")
    md += ["", "## examples (first 3 items per word)", ""]
    for w in args.words:
        for pid in [r["id"] for r in rows_out if r["word"] == w and r["condition"] == "none"][:3]:
            rs = [r for r in rows_out if r["id"] == pid]
            md.append(f"- {w} {pid} (answer {rs[0]['answer']}, bridge {rs[0]['bridge']}): "
                      + "; ".join(f"{r['condition']}: {r['text']!r}" for r in rs))  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[: 4 + len(summary["cells"])]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--set", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--words", nargs="+", default=["PP", "PM", "MP", "MM"])
    ap.add_argument("--level", default="all")
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--band", required=True)
    ap.add_argument("--conditions", nargs="+", default=["paper10", "paper10_rot", "unembed10"])
    ap.add_argument("--max-new", type=int, default=12)
    ap.add_argument("--check", default=None, help="a finished ablate_v2 run on the same set and band: compare the first-step read")
    ap.add_argument("--read", choices=["top", "cand", "cand2"], default="cand2", help="the first-step read (ablate_v2.reads)")
    main(ap.parse_args())
