"""nn_readout (Zach, 2026-10-28, prereg amendment 58 note 9): is a never-named bridge visible in the workspace where it
would be computed? Descriptive, with note 9's fixed reading.

Prompts (jsuite v3 rendering 0, the model's v3 competence and note 4's eligibility): never-named RM (the question
describes the bridge; the passage never names it), MM (the same description, the bridge also named in passing), and
RM's hop 1 alone ("Which novelist wrote Arrow of God?", same passage). Sites: the last token of the description in the
question, and the last token of the prompt. At every 2nd layer, the J++ lens and the logit lens over two candidate sets,
each candidate scored by the best of its first tokens (with and without a leading space): the relation's bridges (is the
bridge X the top one?) and the relation's answers (is X's attribute the top one?). Chance: 1/k. Many bridges share a
first token with another bridge of their relation (Qwen: people 25/63, landmarks 22/40), so a tie counts against the
true candidate (rank = the number of candidates scoring at least as high): the bridge read is conservative.
Reading (note 9): "bridge visible" if X is the top bridge at >= 3x chance at some layer, before the layer where the
attribute's top-1 rate first peaks.
--items v4 (note 14): v4's gate (scripts/nn_swap.v4_split), families MP_ok / MP_fail / MM_ok / MM_fail, the answer read
being the item's own (MP: X's passage value).
--items composition (note 11): instead, RM items whose hop 1 and hop 2 alone are right, as RM_ok (the whole right too)
and RM_fail (the whole wrong), the same reads; per-item ranks are written to rows.jsonl (scripts/nn_fail_read.py).
--priming (note 25, with --items v4): three more answer reads per prompt: "other" (MP: X's remembered attribute; MM: X's
passage value), "third" (an answer of the relation that appears nowhere in the scene) and "ctx" (another entity's passage
value). Read by scripts/nn_priming_read.py.
Note 26 (amendment 59): --items v4ctl adds the closed-book naming question H1 and the recognition question RG (no relation
asked) for scenes whose MM is v4ok, read for X's remembered attribute; --items v4cc reads every MP / MM item of the cue-conflict
set (families by word and description type; rows tagged known = named recall right, gated = v4_split), with one more priming
target, the description's cue; --topk K writes the top-K tokens of each lens (full vocabulary and letter tokens) to topk.jsonl.
Read by scripts/nn_bridge_read.py.
Amendment 60 (notes 29-31): --items v4all --words W ... reads every item of those words, ungated (the knowledge-conflict
set; its scorer gates); key-set items (set_kind "key", note 29) are read on MP for the unsaid key (X's country) among the
countries (key_vocab) as well as the colour, and on MM for an absent country.

python scripts/nn_readout.py --name N --competence C [--set jsuite_v3_test_chat] [--every 2] [--batch 16]
       [--items eligible|composition|v4] [--cv-h1 CV] [--priming]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics
import subprocess
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts.ablate_v2 import bridge_positions  # noqa: E402

RES = pins.RESULTS_DIR / "nn_readout"


def priming_targets(it: dict, avals: list[str], said: str) -> dict | None:
    """note 25: candidate indices of the other word's answer, an answer absent from the scene, another entity's value.
    Note 29 (key sets): MP -> ("k", index) targets over key_vocab: the unsaid key and an absent country; MM -> an absent country
    and another scene country over its own answer_vocab (the countries)."""
    if it.get("set_kind") == "key":
        keys = set(it["scene_keys"])
        absent = [v for v in it["key_vocab"] if v not in keys | {it["key"]}]
        rng = random.Random("third:" + it["id"])
        if it["word"] == "MP":
            return {"key": ("k", it["key_vocab"].index(it["key"])), "keythird": ("k", it["key_vocab"].index(rng.choice(absent)))}
        others = [v for v in sorted(keys) if v != it["key"] and v in avals]
        return {"third": avals.index(rng.choice([v for v in absent if v in avals])),
                "ctx": avals.index(random.Random("ctx:" + it["id"]).choice(others))} if others else None
    pv, x, cue = it["passage_values"], it["bridge"], it.get("cue")
    other = it["real"] if it["word"] == "MP" else pv[x]
    thirds = [v for v in avals if v not in set(pv.values()) | {it["real"], said} | ({cue} if cue else set())]
    ctxs = [pv[e] for e in sorted(pv) if e != x and pv[e] not in (said, other)]
    if other not in avals or other == said or not thirds or not ctxs:
        return None
    out = {"other": avals.index(other), "third": avals.index(random.Random("third:" + it["id"]).choice(thirds)),
           "ctx": avals.index(random.Random("ctx:" + it["id"]).choice(ctxs))}  # fmt: skip
    if cue and cue in avals and cue not in (said, other):  # note 26 (c): the description's cue (cue-conflict items)
        out["cue"] = avals.index(cue)
    er = it.get("entity_reals")  # amendment 60 addendum: another scene entity's real attribute (within-scene control)
    if er:
        reals = [er[e] for e in sorted(er) if e != x and er[e] in avals and er[e] not in (said, other, it["real"])]
        if reals:
            out["ctxreal"] = avals.index(random.Random("ctxreal:" + it["id"]).choice(reals))
    return out


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    layers = sorted(la for la in (int(x) for x in lens.source_layers) if la % a.every == 0)
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "target": pins.TARGET, "model": pins.model_pin(), "lens": pins.FROZEN_LENS, "set": a.set,
                                                       "competence": a.competence, "layers": layers, "items": a.items, "priming": a.priming, "topk": a.topk, "git_commit": commit, "git_state": pins.git_state()}, indent=2) + "\n")  # fmt: skip
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    if a.items == "v4":  # note 14: v4's gate, successes vs failures, the lookup (MP) and its recall twin (MM)
        from scripts.nn_swap import build_prompt, v4_split

        split = v4_split(a.competence, a.cv_h1, a.set)
        prompts = [{**build_prompt(tok, items[i], a.set), "family": f"{items[i]['word']}_{s}"} for i, s in sorted(split.items())]
    elif a.items == "v4ctl":  # note 26 (b): v4's MP / MM as --items v4, plus H1 and RG for scenes whose MM is v4ok
        from scripts.nn_swap import build_prompt, v4_split

        split = v4_split(a.competence, a.cv_h1, a.set)
        prompts = [{**build_prompt(tok, items[i], a.set), "family": f"{items[i]['word']}_{s}"} for i, s in sorted(split.items())]
        ctl_set = a.set.replace("jsuite_v4", "jsuite_v4ctl")
        ctl = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / ctl_set / "items.jsonl").read_text().splitlines()}
        for i, s in sorted(split.items()):
            if ":MM-" in i and s == "ok":
                for w in ("H1", "RG"):
                    c = ctl[i.replace(":MM-", f":{w}-")]
                    # read for X's remembered attribute over the relation's answers (the MM twin's vocabulary)
                    items[c["id"]] = {**c, "word": w, "answer_vocab": items[i]["answer_vocab"], "relation": items[i]["relation"], "bridge": items[i]["bridge"]}
                    prompts.append({"id": c["id"], "ids": S.ids(tok, T.render(tok, {**c, "_question": c["question"], "_kind": c["kind"]})), "family": f"{w}_mmok"})
    elif a.items == "v4cc":  # note 26 (c): every MP / MM item of the cue-conflict set, tagged
        from scripts.nn_swap import build_prompt, v4_split

        split = v4_split(a.competence, a.cv_h1, a.set)
        parts: dict = collections.defaultdict(dict)
        for line in (pins.RESULTS_DIR / "tasks_v2" / a.competence / "items.jsonl").read_text().splitlines():
            r = json.loads(line)
            parts[r["id"]][r["part"]] = bool(r["correct"])
        prompts = [{**build_prompt(tok, it, a.set), "family": f"{it['word']}_{it['cc_type']}",
                    "tags": {"known": bool(parts.get(i.replace(":MP-", ":MM-"), {}).get("step2")), "gated": split.get(i, "")}}
                   for i, it in sorted(items.items()) if it["word"] in ("MP", "MM")]  # fmt: skip
    elif a.items == "v4all":  # amendment 60: every item of --words, ungated (the knowledge-conflict set's scorer gates)
        from scripts.nn_swap import build_prompt

        prompts = [{**build_prompt(tok, it, a.set), "family": it["word"]} for i, it in sorted(items.items()) if it["word"] in (a.words or [])]
    elif a.items == "composition":  # note 11: successes vs failures among RM items whose hops alone are right
        from scripts.nn_swap import build_prompt, composition_split

        split = composition_split(a.competence)
        prompts = [{**build_prompt(tok, items[i], a.set), "family": f"RM_{s}"} for i, s in sorted(split.items())]
    else:
        prompts = [p for p in JS.v3_prompts(tok, a.set, a.competence, ["RM", "MM"]) if p["family"] in ("RM", "MM")]
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")

    def cand_rows(vals: list[str]) -> list[list[int]]:
        return [[int(row_of[t]) for t in {S.ids(tok, " " + v)[0], S.ids(tok, v)[0]} if int(row_of[t]) >= 0] for v in vals]

    bridges_of = collections.defaultdict(set)
    for it in items.values():
        if it.get("module") == "facts" and (it["word"] in ("PK", "PM", "RM", "MM", "MP") or it.get("set_kind") in ("key", "kc")):
            bridges_of[it["relation"]].add(it["bridge"])
    jobs, nskip = [], 0
    for p in prompts:
        it = items[p["id"]]
        variants = [(p["family"], p["ids"])]
        if p["family"] == "RM":  # hop 1 alone, same passage
            q1 = it["steps"][0]["question"]
            variants.append(("RM_hop1", S.ids(tok, T.render(tok, {**it, "_question": q1, "_kind": it["steps"][0]["kind"]}))))
        bvals, avals = sorted(bridges_of[it["relation"]]), list(it["answer_vocab"])
        brows, arows = cand_rows(bvals), cand_rows(avals)
        krows = cand_rows(list(it["key_vocab"])) if it.get("key_vocab") else None
        # note 14: MP's answer is X's passage value; note 26: H1 / RG are read for X's remembered attribute
        true_a = it["real"] if it["word"] in ("H1", "RG") else it["answer"] if it.get("set_version") == "v4" else it["real"]
        if not all(brows) or not all(arows) or it["bridge"] not in bvals or true_a not in avals:
            continue
        for fam, ids in variants:
            # the description's last token; hop 1 repeats its clause ("Which novelist wrote Arrow of God?")
            desc = re.split(r" (?:who|that) ", it["start_desc"], maxsplit=1)[-1] if fam == "RM_hop1" or fam[:2] in ("H1", "RG") else it["start_desc"]
            pos = bridge_positions(tok, ids, desc)
            if not pos:
                continue
            ex = priming_targets(it, avals, true_a) if a.priming else {}
            if ex is None:
                nskip += 1
                continue
            jobs.append({"id": p["id"], "family": fam, "ids": ids, "sites": {"desc_end": pos[-1], "final": len(ids) - 1}, "brows": brows, "arows": arows,
                         "bx": bvals.index(it["bridge"]), "ax": avals.index(true_a), "rel": it["relation"], "bridge": it["bridge"], "extra": ex, "tags": p.get("tags", {}), "krows": krows})  # fmt: skip
    if a.limit:  # a smoke: the first N prompts per family
        per = collections.defaultdict(list)
        for j in jobs:
            per[j["family"]].append(j)
        jobs = [j for v in per.values() for j in v[: a.limit]]
    if a.priming:
        assert a.items in ("v4", "v4ctl", "v4cc", "v4all"), "--priming reads v4 items"
        print(f"note 25: {nskip} prompts without the extra targets skipped", flush=True)
    print(f"{len(jobs)} prompts; by family {dict(collections.Counter(j['family'] for j in jobs))}; layers {layers}", flush=True)
    stats = collections.defaultdict(list)
    item_rows, topk_rows, dec_cache = [], [], {}
    wfull = model.hf.lm_head.weight.float() * model.norm_gain() if a.topk else None

    def dec(t: int) -> str:
        if t not in dec_cache:
            dec_cache[t] = tok.decode([t])
        return dec_cache[t]
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            rec = {}

            def hook_for(la):
                def hook(_m, _a, out):
                    h = out[0] if isinstance(out, tuple) else out
                    rec[la] = h.float()

                return hook

            with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
                model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
            for la in layers:
                for site in ("desc_end", "final"):
                    x = torch.stack([rec[la][b, j["sites"][site]] for b, j in enumerate(chunk)])
                    for ln, M in (("jlens", lens.J(la)), ("logit", None)):
                        lg = (x if M is None else x @ M.T) @ wg.T
                        if a.topk:  # note 26 (a): the lens's top tokens, full vocabulary and letter tokens
                            tv = ((x if M is None else x @ M.T) @ wfull.T).topk(a.topk, dim=-1).indices.tolist()
                            tl = letters[lg.topk(a.topk, dim=-1).indices].tolist()
                            for b, j in enumerate(chunk):
                                topk_rows.append({"id": j["id"], "family": j["family"], "site": site, "lens": ln, "layer": la,
                                                  "top": [dec(t) for t in tv[b]], "top_letters": [dec(t) for t in tl[b]]})  # fmt: skip
                        for b, j in enumerate(chunk):
                            for what, rws, true in (("bridge", j["brows"], j["bx"]), ("attr", j["arows"], j["ax"]),
                                                    *((w, j["krows"], t[1]) if isinstance(t, tuple) else (w, j["arows"], t) for w, t in j["extra"].items())):
                                cand = torch.stack([lg[b, r].max() for r in rws])
                                # conservative: a tie (bridges sharing a first token) counts against the true candidate
                                rank = int((cand >= cand[true]).sum())
                                stats[(j["family"], site, ln, what, la)].append((rank == 1, rank, 1 / len(rws)))
                                if a.items in ("composition", "v4", "v4ctl", "v4cc", "v4all"):  # amendment 60: v4all too (fixed 2026-10-29 after the 9B v5kc2 readout wrote no rows)
                                    item_rows.append({"id": j["id"], "family": j["family"], "rel": j["rel"], "bridge": j["bridge"], "site": site,
                                                      "lens": ln, "what": what, "layer": la, "rank": rank, "k": len(rws), **j["tags"]})  # fmt: skip
    summ = {}
    for (fam, site, ln, what, la), xs in sorted(stats.items()):
        summ[f"{fam}/{site}/{ln}/{what}/L{la}"] = {"n": len(xs), "top1": round(100 * sum(t for t, _, _ in xs) / len(xs), 1),
                                                    "chance": round(100 * sum(c for _, _, c in xs) / len(xs), 1),
                                                    "median_rank": statistics.median(r for _, r, _ in xs)}  # fmt: skip
    # note 9's reading, per family and lens at the description's end
    reading = {}
    for fam in sorted({j["family"] for j in jobs}):
        for ln in ("jlens", "logit"):
            br = [(la, summ[f"{fam}/desc_end/{ln}/bridge/L{la}"]) for la in layers if f"{fam}/desc_end/{ln}/bridge/L{la}" in summ]
            at = [(la, summ[f"{fam}/desc_end/{ln}/attr/L{la}"]) for la in layers if f"{fam}/desc_end/{ln}/attr/L{la}" in summ]
            if not br or not at:
                continue
            peak = max(at, key=lambda z: z[1]["top1"])[0]
            vis = [la for la, c in br if c["top1"] >= 3 * c["chance"] and la <= peak]
            reading[f"{fam}/{ln}"] = {"bridge_visible_before_attr_peak": bool(vis), "layers": vis, "attr_peak_layer": peak,
                                      "bridge_best": max(c["top1"] for _, c in br), "attr_best": max(c["top1"] for _, c in at)}  # fmt: skip
    summ["reading"] = reading
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    if item_rows:
        (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in item_rows))
    if topk_rows:
        (out_dir / "topk.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in topk_rows))
    for fam in sorted({j["family"] for j in jobs}):
        for site in ("desc_end", "final"):
            line = f"{fam:8s} {site:8s}"
            for la in layers:
                cb, ca = summ.get(f"{fam}/{site}/jlens/bridge/L{la}"), summ.get(f"{fam}/{site}/jlens/attr/L{la}")
                if cb and ca:
                    line += f" L{la} {cb['top1']:.0f}/{ca['top1']:.0f}"
            print(line + "   (J++ top-1 %: bridge / attribute)", flush=True)
    print(json.dumps(reading, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0, help="first N prompts per family (a smoke)")
    ap.add_argument("--items", choices=["eligible", "composition", "v4", "v4ctl", "v4cc", "v4all"], default="eligible", help="note 11: RM_ok vs RM_fail; note 14: v4")
    ap.add_argument("--cv-h1", default=None, help="note 14: the competence_variants run on v4's H1")
    ap.add_argument("--words", nargs="*", default=None, help="amendment 60: --items v4all's words")
    ap.add_argument("--topk", type=int, default=0, help="note 26: write each lens's top-K tokens per site and layer")
    ap.add_argument("--priming", action="store_true", help="note 25: the other word's answer, an absent answer, another entity's value")
    main(ap.parse_args())
