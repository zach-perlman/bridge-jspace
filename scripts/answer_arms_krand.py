"""answer_arms_krand: the size control rule (b) of scripts/answer_arms_translated.py lacked (POST HOC; Dan 30 Oct; his design error: arm 2 was compared across two
answer-direction sets of different sizes without a control for the number of directions kept).

Same runs (the saved 51.12 E1 run), items, layer, seed, lens and reads as answer_arms_translated. Arm 2 = without the lens part, keeping some directions: Delta
- (P_J Delta - P_S P_J Delta), S the span of the kept directions. Here S is the span of K RANDOM token directions instead of the answer directions, built the
way the answer directions are built (x51_answer.answer_basis over JLens.vectors of single-token words: letter tokens whose text is a whole alphabetic word of at
least 2 letters), excluding the item's answer words (every language) and its old / new bridge words. K = the item's all-language count (about 102) and,
separately, its English count (about 15). 5 draws per item; the item's outcome is the average of the 5 switch indicators. Arms read here: whole, arm 2 with the
English answer directions, arm 2 with the all-language answer directions, and the two K-random twins (all in one process; gate: whole and both arm 2 counts within
+-1 of the saved run per reader).

Pre-set (written to the manifest first): the (b) shift counts as answer-specific only if [all-language arm 2 minus its K-random twin] minus [English arm 2
minus its K-random twin] (each: the share of the whole change's switches blocked, 95% cluster bootstrap over the bridge entity, paired) has an interval
excluding 0. Otherwise: "(b) shift is explained by the number of kept directions", and the label rests on (a) alone.

BJ_TARGET=muse-glimmer-30b BJ_SUITE_BATCH=64 BJ_DEVICE_MAP= uv run python scripts/answer_arms_krand.py --run muse30_x51_12_e1_r2 --from-tag run2
"""

from __future__ import annotations

import argparse
import json
import re
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
OUT_ROOT = REPO / "runs" / "answer_arms_krand"
SAVED_ROOT = REPO / "runs" / "answer_arms_translated"
N_DRAWS, SEED = 5, 29
BATCH_EDITS = 7  # arms per batch beside the unedited row: answer_arms_translated read 8 rows per (item, reader)
READERS = {"PM": "recall", "PP": "lookup"}
WORD = re.compile(r"^[^\W\d_]{2,}$")  # a whole alphabetic word of at least two letters
PRESET = ("The (b) shift counts as answer-specific only if [all-language arm 2 minus its K-random twin] minus [English arm 2 minus its K-random twin] "
          "(share of the whole change's switches blocked; 95% cluster bootstrap over the bridge entity, paired) has an interval excluding 0. Otherwise: "
          "'(b) shift is explained by the number of kept directions', and the label rests on (a) alone.")  # fmt: skip


def share_blocked(rr: dict, arm: str) -> np.ndarray:
    return X.dependence(rr["whole"], rr[arm])


def stats(rows: list[dict], items: list[dict], reader: str, n_boot: int) -> dict:
    mine = [r for r in rows if r["reader"] == reader]
    ent = {it["key"]: it["entity"] for it in items}
    keys = [it["key"] for it in items]
    by: dict = {}
    for r in mine:
        by.setdefault((r["key"], r["arm"].split("#")[0]), []).append(r["sw"])
    arms = ("whole", "a_en", "a_all", "r_en", "r_all")
    sw = {a: [float(np.mean(by[(k, a)])) for k in keys] for a in arms}
    rr = X.resampled_rates(sw, [ent[k] for k in keys], n_boot, X.BOOT_SEED)
    d = {a: share_blocked(rr, a) for a in arms[1:]}
    pt = {a: float(X.dependence(np.mean(sw["whole"]), np.mean(sw[a]))) for a in arms[1:]}
    diff_all, diff_en = d["a_all"] - d["r_all"], d["a_en"] - d["r_en"]
    delta = diff_all - diff_en

    def ci(point: float, draws: np.ndarray) -> list[float]:
        return [round(point, 4), *(round(v, 4) for v in X.interval(draws))]

    out = {"n": len(keys), "whole_switches": float(sum(sw["whole"])),
           "share_blocked": {a: ci(pt[a], d[a]) for a in arms[1:]},
           "arm2_minus_K_random_all_languages": ci(pt["a_all"] - pt["r_all"], diff_all),
           "arm2_minus_K_random_english": ci(pt["a_en"] - pt["r_en"], diff_en)}  # fmt: skip
    out["b_beyond_K_random"] = ci((pt["a_all"] - pt["r_all"]) - (pt["a_en"] - pt["r_en"]), delta)
    lo, hi = out["b_beyond_K_random"][1:]
    out["answer_specific"] = bool(lo > 0 or hi < 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument(
        "--from-tag", required=True, help="the answer_arms_translated tag whose saved arm 2 counts gate this run"
    )
    ap.add_argument("--tag", default="krand")
    a = ap.parse_args()
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    target = pins.TARGET
    layer = A.layer_of("e1", target)
    src = A.RESULTS / a.run
    out = OUT_ROOT / target / a.tag
    out.mkdir(parents=True, exist_ok=False)
    saved_dir = SAVED_ROOT / target / a.from_tag
    cases = X.read_jsonl(src / "cases.jsonl")
    items = [{k: v for k, v in c.items() if k != "tokens"} for c in cases]
    manifest = {
        "exp": "answer_arms_krand",
        "post_hoc": True,
        "why": "rule (b) of answer_arms_translated lacked a size control (Dan's design error)",
        "model": target,
        "run": a.run,
        "layer": layer,
        "items": len(items),
        "saved_arm2_from": str(saved_dir.relative_to(REPO)),
        "draws_per_item": N_DRAWS,
        "K": "the item's all-language count and, separately, its English count",
        "random_directions": "letter tokens that are whole alphabetic words of >= 2 letters, excluding the item's answer tokens (all languages) and its old / new bridge tokens; built with x51_answer.answer_basis over JLens.vectors",
        "preset": PRESET,
        "gate": "whole and both arm 2 switch counts within +-1 of the saved run, per reader",
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
    excluded = [
        set(tr) | set(c["tokens"]["bridge"]["org"]) | set(c["tokens"]["bridge"]["alt"])
        for tr, c in zip(translated, cases, strict=True)
    ]
    letters = model.letter_token_ids().tolist()
    pool = np.array([t for t in letters if WORD.match(model.decoded[t].strip())])
    print(f"loaded in {time.time() - t0:.0f}s; pool {len(pool)} of {len(letters)} letter tokens; K all {np.mean([len(x) for x in translated]):.1f}, K en {np.mean([len(x) for x in english]):.1f}", flush=True)  # fmt: skip
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
        jdic = lens.vectors(layer, model.letter_token_ids()).to(dev)

        def basis_of(ids: list[int]):
            return A.answer_basis(lens.vectors(layer, torch.tensor(ids, dtype=torch.long, device=dev)))

        b_en = [basis_of(ids) for ids in english]
        b_all = [basis_of(ids) for ids in translated]
        draws, shown = {}, {}
        for kind, kfun in (("en", lambda i: len(english[i])), ("all", lambda i: len(translated[i]))):
            for d in range(N_DRAWS):
                bases, ids_list = [], []
                for i in range(len(items)):
                    rng = np.random.default_rng((SEED, i, d, 0 if kind == "en" else 1))
                    ok = pool[~np.isin(pool, list(excluded[i]))]
                    ids = [int(t) for t in rng.choice(ok, size=kfun(i), replace=False)]
                    ids_list.append(ids)
                    bases.append(basis_of(ids))
                draws[(kind, d)] = bases
                shown[(kind, d)] = ids_list
        arms: dict[str, dict[str, object]] = {}
        for s in sources:
            x = torch.stack(deltas[s]).to(dev)
            pj = X.fit(jdic, x, X.K_MAIN, "signed").to(dev)
            arm = {"whole": x, "a_en": x - A.answer_parts(x, pj, b_en)[0], "a_all": x - A.answer_parts(x, pj, b_all)[0]}
            for (kind, d), bases in draws.items():
                arm[f"r_{kind}#{d}"] = x - A.answer_parts(x, pj, bases)[0]
            arms[s] = arm
        names = list(arms[sources[0]])
        rows = []
        for i, it in enumerate(progress(items, f"{len(names)} arms x readers (item)")):
            for w, rd in it["readers"].items():
                # read in batches of BATCH_EDITS + 1 rows ([{}] first, as answer_arms_translated's 8-row batches): batched-kernel rounding depends on the batch size
                for s0 in range(0, len(names), BATCH_EDITS):
                    chunk = names[s0 : s0 + BATCH_EDITS]
                    edits = [{}] + [{layer: AddRows(arms[rd["src"]][n][i : i + 1], [rd["pos"]])} for n in chunk]
                    logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
                    for n, lg in zip(chunk, logits[1:], strict=True):
                        rows.append(
                            {"key": it["key"], "reader": w, "arm": n, "sw": int(X.read_row(lg, rd, digits)["switched"])}
                        )
    X.write_jsonl(out / "outcomes.jsonl", rows)

    def counts(rs: list[dict]) -> dict:
        c: dict = {}
        for r in rs:
            c.setdefault(r["reader"], {}).setdefault(r["arm"], 0)
            c[r["reader"]][r["arm"]] += r["sw"]
        return c

    mine = counts(rows)
    saved_en, saved_all = (
        counts(X.read_jsonl(saved_dir / "outcomes_english.jsonl")),
        counts(X.read_jsonl(saved_dir / "outcomes_all_languages.jsonl")),
    )
    gate = {w: {"whole": [mine[w]["whole"], saved_en[w]["whole"]], "a_en": [mine[w]["a_en"], saved_en[w]["no_jpp_A"]], "a_all": [mine[w]["a_all"], saved_all[w]["no_jpp_A"]]} for w in READERS}  # fmt: skip
    gate_ok = all(abs(v[0] - v[1]) <= 1 for w in gate.values() for v in w.values())
    (out / "gate.json").write_text(json.dumps({"ok": gate_ok, "now_vs_saved": gate}, indent=1) + "\n")
    print("gate:", json.dumps({"ok": gate_ok, **gate}), flush=True)
    summary = {"post_hoc": True, "model": target, "run": a.run, "layer": layer, "n": len(items), "seconds": round(time.time() - t0), "gate": {"ok": gate_ok, "now_vs_saved": gate},
               "K_mean": {"all_languages": round(float(np.mean([len(x) for x in translated])), 1), "english": round(float(np.mean([len(x) for x in english])), 1)},
               "pool_tokens": len(pool), "preset": PRESET, "readers": {name: stats(rows, items, rid, X.N_BOOT) for rid, name in READERS.items()}}  # fmt: skip
    rc = summary["readers"]["recall"]
    summary["verdict"] = (
        "(b) shift is answer-specific (beyond K random directions)"
        if rc["answer_specific"]
        else "(b) shift is explained by the number of kept directions"
    )
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    import random as _r

    ex = []
    for k in _r.Random(SEED).sample([it["key"] for it in items], 3):
        i = [it["key"] for it in items].index(k)
        ex.append({"key": k, "K_all": len(translated[i]), "K_en": len(english[i]),
                   "random_all_draw0": [model.decoded[t] for t in shown[("all", 0)][i]][:20], "random_en_draw0": [model.decoded[t] for t in shown[("en", 0)][i]],
                   "sw": {w: {n: next(r["sw"] for r in rows if r["key"] == k and r["reader"] == w and r["arm"] == n) for n in names} for w in READERS}})  # fmt: skip
    (out / "three_random_items.json").write_text(json.dumps(ex, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"verdict": summary["verdict"], "recall": rc}, indent=1, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
