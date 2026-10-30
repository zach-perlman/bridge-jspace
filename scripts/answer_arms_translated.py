"""answer_arms_translated: 51.12's answer-control ARMS with translated answer directions (POST HOC; Dan 30 Oct; Muse only).

Same run as the saved one (muse30_x51_12_e1_r2): same items (its cases.jsonl), layer, seed, lens, reads. Only the answer
directions A change: English set = the run's own (the English number words, 4 spellings, letter tokens), all-languages set =
the English set plus every whole-token translation of the items' answer values (scripts/answer_translation_check.py's
tokens_of: eleven languages, 4 spellings, whole tokens only, no lone I / V / X). Every other arm is read unchanged; each
part's size-matched random twin is rebuilt from the part's own share, so the twins of arms 2-4 follow the larger A.

Order inside one process (the model is loaded once): (1) pre-flight = the English set through this driver's code, its per-reader
per-arm switch counts compared with the saved outcomes.jsonl; any difference stops the run before the all-languages arms.
(2) the all-languages arms. Read-only on every existing run; writes runs/answer_arms_translated/<model>/.

Pre-set rule (written to the manifest before the numbers, not changed after): the claim changes only if, on the recall (the
decisive reader of E1), (a) "answer directions only" (arm 3, all languages) blocks more than its size-matched random part
(arm 4): the 95 % interval of the extra (S_rand - S_arm) / S_whole excludes 0 from above, or (b) "without the lens part,
answer directions kept" (arm 2) blocks a different share of the switches from the English-only arm: the 95 % intervals of the
two shares do not overlap. Otherwise: no change. The lookup is reported beside, not decisive.

BJ_TARGET=muse-glimmer-30b BJ_SUITE_BATCH=64 BJ_DEVICE_MAP= uv run python scripts/answer_arms_translated.py --run muse30_x51_12_e1_r2
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from scripts import answer_translation_check as T  # noqa: E402
from scripts import x51_answer as A  # noqa: E402

X = A.X
OUT_ROOT = REPO / "runs" / "answer_arms_translated"
SEED = 29
READERS = {"PM": "recall", "PP": "lookup"}  # the 51.12 e1 readers (key of the item's readers); the recall is decisive
DECISION = ("Claim changes only if, on the recall: (a) arm 3 (answer directions only, all languages) beats its size-matched random "
            "part (arm 4): the 95% interval of the extra (S_rand - S_arm) / S_whole is above 0; or (b) arm 2 (without the lens part, "
            "answer directions kept) blocks a different share of the switches than in the English-only arm: the two 95% intervals do "
            "not overlap. Otherwise no change. The lookup is reported beside, not decisive.")  # fmt: skip


def counts(rows: list[dict]) -> dict:
    out: dict = {}
    for r in rows:
        out.setdefault(r["reader"], {}).setdefault(r["arm"], 0)
        out[r["reader"]][r["arm"]] += int(r["sw"])
    return out


def read_arms(model, lens, items, toks_a, deltas, sources, jdic, basis, layer, digits, ws, label, progress):
    """All arms of every item for one A set (toks_a: per item the answer-direction token ids); returns (outcome rows, norm rows)."""
    import torch

    bases = [
        A.answer_basis(lens.vectors(layer, torch.tensor(ids, dtype=torch.long, device=model.device))) for ids in toks_a
    ]
    arms, norms = {}, []
    for s in sources:
        x = torch.stack(deltas[s]).to(model.device)
        pj = X.fit(jdic, x, X.K_MAIN, "signed").to(model.device)
        arms[s], sh = A.all_arms(x, pj, bases, basis)
        for i, it in enumerate(items):
            norms.append({"key": it["key"], "entity": it["entity"], "source": s, "norm": round(float(x[i].norm()), 4),
                          **{f"share_{k}": round(float(v[i]), 6) for k, v in sh.items()},
                          "A_tokens": len(toks_a[i]), "A_rank": int(bases[i].shape[1]), "A_ids": toks_a[i]})  # fmt: skip
    rows = []
    for i, it in enumerate(progress(items, f"{label}: {len(A.ARMS) + 1} arms x readers (item)")):
        rows += A.read_item(model, "e1", it, layer, arms, i, digits, ws)
    return rows, norms


def numbers(rows: list[dict], n_boot: int) -> dict:
    """Per reader: reader_numbers (rates, extra, label) plus per arm the switches blocked (count) and the share of the
    whole change's switches blocked, 1 - S_arm / S_whole, with the cluster-bootstrap 95 % interval."""
    out = {}
    for rid, name in READERS.items():
        mine = [r for r in rows if r["reader"] == rid]
        rn = A.reader_numbers(rows, rid, n_boot=n_boot)
        keys = list(dict.fromkeys(r["key"] for r in mine if r["arm"] == "whole"))
        ent = {r["key"]: r["entity"] for r in mine}
        by = {(r["key"], r["arm"]): int(r["sw"]) for r in mine}
        arms = list(dict.fromkeys(r["arm"] for r in mine))
        sw = {a: [by[(k, a)] for k in keys] for a in arms}
        rr = X.resampled_rates(sw, [ent[k] for k in keys], n_boot, X.BOOT_SEED)
        blocked = {}
        for a in arms:
            if a in ("none", "whole"):
                continue
            dep = X.dependence(rr["whole"], rr[a])
            blocked[a] = {"switches_blocked": sum(sw["whole"]) - sum(sw[a]), "of_whole": sum(sw["whole"]),
                          "share_blocked": [float(X.dependence(np.mean(sw["whole"]), np.mean(sw[a]))), *X.interval(dep)]}  # fmt: skip
        out[name] = {**rn, "blocked": blocked}
    return out


def direction_sizes(ns: list[dict]) -> dict:
    return {"mean_tokens": round(float(np.mean([r["A_tokens"] for r in ns])), 2), "mean_rank": round(float(np.mean([r["A_rank"] for r in ns])), 2),
            "min_rank": min(r["A_rank"] for r in ns), "max_rank": max(r["A_rank"] for r in ns)}  # fmt: skip


def mean_share(ns: list[dict]) -> float:
    return round(float(np.mean([r["share_A"] for r in ns])), 4)


def decide(en: dict, al: dict) -> dict:
    rc_en, rc_al = en["recall"], al["recall"]
    e3 = rc_al["extra"]["3"]
    a_holds = e3[1] > 0  # the interval's lower end
    s_en, s_al = rc_en["blocked"]["no_jpp_A"]["share_blocked"], rc_al["blocked"]["no_jpp_A"]["share_blocked"]
    b_holds = s_en[2] < s_al[1] or s_al[2] < s_en[1]
    return {"a_arm3_beats_random_all_languages": bool(a_holds), "arm3_extra_all_languages": e3,
            "b_arm2_share_differs": bool(b_holds), "arm2_share_english": s_en, "arm2_share_all_languages": s_al,
            "claim_changes": bool(a_holds or b_holds)}  # fmt: skip


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    target = pins.TARGET
    layer = A.layer_of("e1", target)
    src = A.RESULTS / a.run
    out = OUT_ROOT / target
    out.mkdir(parents=True, exist_ok=False)
    cases = X.read_jsonl(src / "cases.jsonl")
    items = [{k: v for k, v in c.items() if k != "tokens"} for c in cases]
    saved = X.read_jsonl(src / "outcomes.jsonl")
    manifest = {
        "exp": "answer_arms_translated",
        "post_hoc": True,
        "model": target,
        "run": a.run,
        "layer": layer,
        "items": len(items),
        "what": "51.12 E1 arms with the answer directions A taken in every language (Muse only)",
        "english_set": "the run's own A (cases.jsonl tokens.A)",
        "all_languages_set": "the English set + tokens_of() translations of the items' answer values (answer_translation_check: eleven languages, 4 spellings, whole tokens, no lone I/V/X)",
        "size_matched_random": "each part's random twin rebuilt from the part's own share (x6_routes.removal_arms), seed 888 + layer",
        "preflight": "English set through this driver; per reader per arm switch counts must equal the saved outcomes.jsonl, else stop",
        "decision_rule": DECISION,
        "decisive_reader": "recall (PM)",
        "seed_for_random_items": SEED,
        "git": subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True
        ).stdout.strip()
        or "pod: no git (tar)",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")  # before the numbers
    t0 = time.time()
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    lens = JLens(model, "jpp")
    assert layer in lens.source_layers
    english = [c["tokens"]["A"] for c in cases]
    values = [sorted({int(x) for rd in it["readers"].values() for x in rd["words_A"]}) for it in items]
    translated = [
        sorted(set(en) | {t for v in vs for t in T.tokens_of(tok, v)["all"]})
        for en, vs in zip(english, values, strict=True)
    ]
    assert all(set(en) <= set(al) for en, al in zip(english, translated, strict=True))
    print(f"loaded in {time.time() - t0:.0f}s; mean directions English {np.mean([len(x) for x in english]):.1f}, all languages {np.mean([len(x) for x in translated]):.1f}", flush=True)  # fmt: skip
    ws = X.whitespace_mask(model)
    digit_list = X.digit_ids(tok)
    digits = torch.tensor(digit_list, device=dev)
    sources = sorted({rd["src"] for it in items for rd in it["readers"].values()})
    with torch.no_grad():
        deltas: dict[str, list] = {s: [] for s in sources}
        for it in progress(items, f"delta at L{layer} (item)"):
            for s in sources:
                rd = it["readers"][s]
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][rd["pos"]].float().clone() for v in ("org", "alt")}  # fmt: skip
                deltas[s].append(h["alt"] - h["org"])
        letters = model.letter_token_ids()
        jdic = lens.vectors(layer, letters).to(dev)
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        rows_en, norms_en = read_arms(
            model,
            lens,
            items,
            english,
            deltas,
            sources,
            jdic,
            basis,
            layer,
            digits,
            ws,
            "pre-flight (English set)",
            progress,
        )
        X.write_jsonl(out / "outcomes_english.jsonl", rows_en)
        X.write_jsonl(out / "norms_english.jsonl", norms_en)
        c_new, c_old = counts(rows_en), counts(saved)
        pre = {"match": c_new == c_old, "counts_driver": c_new, "counts_saved": c_old,
               "rows_agreeing": sum(1 for r in rows_en if {(s["key"], s["reader"], s["arm"]): int(s["sw"]) for s in saved}.get((r["key"], r["reader"], r["arm"])) == int(r["sw"])),
               "rows": len(rows_en)}  # fmt: skip
        (out / "preflight.json").write_text(json.dumps(pre, indent=1) + "\n")
        print("pre-flight:", json.dumps({k: pre[k] for k in ("match", "rows_agreeing", "rows")}), flush=True)
        if not pre["match"]:
            print("PRE-FLIGHT DID NOT MATCH the saved outcomes: stop (counts in preflight.json)", flush=True)
            sys.exit(2)
        rows_al, norms_al = read_arms(
            model, lens, items, translated, deltas, sources, jdic, basis, layer, digits, ws, "all languages", progress
        )
        X.write_jsonl(out / "outcomes_all_languages.jsonl", rows_al)
        X.write_jsonl(out / "norms_all_languages.jsonl", norms_al)
    en, al = numbers(rows_en, X.N_BOOT), numbers(rows_al, X.N_BOOT)
    size = direction_sizes
    summary = {
        "post_hoc": True,
        "model": target,
        "run": a.run,
        "layer": layer,
        "n": len(items),
        "seconds": round(time.time() - t0),
        "directions": {
            "english": size([r for r in norms_en if r["source"] == "PP"]),
            "all_languages": size([r for r in norms_al if r["source"] == "PP"]),
            "mean_share_A_english": mean_share(norms_en),
            "mean_share_A_all_languages": mean_share(norms_al),
        },
        "preflight_match": True,
        "english": en,
        "all_languages": al,
        "decision": decide(en, al),
        "decision_rule": DECISION,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    keys = [it["key"] for it in items]
    rnd = random.Random(SEED).sample(keys, 3)
    by_en = {(r["key"], r["reader"], r["arm"]): r for r in rows_en}
    by_al = {(r["key"], r["reader"], r["arm"]): r for r in rows_al}
    ex = []
    for k in rnd:
        ex.append({"key": k, "A_english": english[keys.index(k)], "A_all_languages": translated[keys.index(k)],
                   "A_all_languages_decoded": [tok.decode([t]) for t in translated[keys.index(k)]],
                   "arms": {rid: {arm: {"english_sw": by_en[(k, rid, arm)]["sw"], "all_languages_sw": by_al[(k, rid, arm)]["sw"]} for arm in ("none", *A.ARMS)} for rid in READERS}})  # fmt: skip
    (out / "three_random_items.json").write_text(json.dumps(ex, indent=1, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {"directions": summary["directions"], "decision": summary["decision"]}, indent=1, ensure_ascii=False
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
