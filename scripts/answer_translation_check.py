"""answer_translation_check: 51.12's "the answer word is not read" with translations counted (Dan 30 Oct; GPU spot check, one model).

51.12 (E1) reads the J++ lens at the edited (bridge) token on O and S (readout rows, source PP) and ranks each reader's own answer
word, the best of its English number-word tokens; an item is "not read" when its best rank over O and S is > 50, and the model's
label is "the answer word is not read" when >= 90 % of its items are. This script rebuilds those states for ONE model and takes the
answer's rank as the best over its translations too: the whole-token number words (1-10) of scripts/atoms_multilingual.py's eleven
languages, in four spellings, no lone I / V / X (same rules as commit 9a34b0b5). Same layer, same position, same lens, same top-50
threshold, same rank function as scripts/x51_answer.py; the reader is the recall (PM), whose answer words the label is about.

Read-only on every existing run; writes only a new folder runs/answer_translation_check/<model>/. Pre-set decision rule (not
changed after the numbers): flips <= 5 % of the items: "translation does not change the verdict"; > 5 %: report only.

BJ_TARGET=muse-glimmer-30b uv run python scripts/answer_translation_check.py --run muse30_x51_12_e1_r2 --preflight
BJ_TARGET=muse-glimmer-30b uv run python scripts/answer_translation_check.py --run muse30_x51_12_e1_r2
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from scripts import atoms_multilingual as M  # noqa: E402
from scripts import x51_answer as A  # noqa: E402

RECALL = "PM"
SOURCE = "PP"  # E1's Δ and readout are from the lookup's prompts (51.12's manifest: "e1 / cue: from the lookup's prompts")
PREFLIGHT_ITEMS = {"muse-glimmer-30b": ("P2-L0-0095", "P2-L0-0208")}  # the items with saved states on the laptop
EXPECT = {("muse-glimmer-30b", "P2-L0-0095"): {"org": 61, "alt": 131}}  # Dan: ' three' = 61, ' seven' = 131
SEED = 29
OUT_ROOT = REPO / "runs" / "answer_translation_check"


def tokens_of(tok, value: int) -> dict:
    """The whole-token ids of the number word of `value` in each language (four spellings), and the union."""
    per = {}
    for lang, forms in M.CARDINAL.items():
        ids = M.whole_token_ids(tok, forms[value - 1])
        per[lang] = ids
    return {"per_language": per, "all": sorted({i for ids in per.values() for i in ids})}


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="the 51.12 run whose items and stored ranks are re-read")
    ap.add_argument("--preflight", action="store_true", help="only the items with saved states: check the English ranks, stop")
    a = ap.parse_args()
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import x6_routes as R

    target = pins.TARGET
    layer = A.layer_of("e1", target)
    src = A.RESULTS / a.run
    out = OUT_ROOT / target
    out_dir = out / ("preflight" if a.preflight else "full")
    if not a.preflight:
        assert (out / "preflight" / "summary.json").exists() and json.loads((out / "preflight" / "summary.json").read_text())["match"], \
            "the pre-flight has not matched: run --preflight first"  # fmt: skip
    out_dir.mkdir(parents=True, exist_ok=False)
    cases = {c["key"]: c for c in A.X.read_jsonl(src / "cases.jsonl")}
    stored = {(r["key"], r["variant"]): r for r in A.X.read_jsonl(src / "readout.jsonl") if r["source"] == SOURCE}
    keys = list(PREFLIGHT_ITEMS[target]) if a.preflight else list(json.loads((src / "gate.json").read_text())["order"])
    manifest = {"exp": "answer_translation_check", "model": target, "run": a.run, "layer": layer, "keys": len(keys), "preflight": a.preflight,
                "reader": RECALL, "source": SOURCE, "not_read_rank": A.NOT_READ_RANK, "not_read_share": A.NOT_READ_SHARE,
                "rules": "single-token translations only (4 spellings), no lone I/V/X; same layer, position, lens, rank function and top-50 threshold as 51.12",
                "decision_rule": "flips <= 5% of items: translation does not change the verdict; > 5%: report only",
                "lens": "jpp (JLens.readout)", "git": __import__("subprocess").run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip(),
                "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))  # before the numbers
    t0 = time.time()
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    lens = JLens(model, "jpp")
    assert layer in lens.source_layers
    print(f"model loaded in {time.time() - t0:.0f}s", flush=True)
    rows = []
    with torch.no_grad():
        for key in progress(keys, "answer translation check (item)"):
            c = cases[key]
            rd = c["readers"][SOURCE]
            h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][rd["pos"]].float().clone() for v in ("org", "alt")}
            pm = c["readers"][RECALL]
            row = {"key": key, "entity": c["entity"], "answers": {"org": pm["answer"], "alt": pm["cf_answer"]}}
            for v, f in (("org", "answer"), ("alt", "cf_answer")):
                lg = lens.readout(h[v][None], layer)[0].float()
                english_ids = c["tokens"]["own_word"][v][RECALL]
                english = min(A.rank_of(lg, t) for t in english_ids)
                tr = tokens_of(tok, int(pm[f]))
                ranked = [(A.rank_of(lg, t), t) for t in tr["all"]]
                best, tid = min(ranked) if ranked else (None, None)
                per_lang = {lang: min((A.rank_of(lg, t) for t in ids), default=None) for lang, ids in tr["per_language"].items()}
                row[v] = {"english_rank": english, "stored_rank": stored[(key, v)]["answer_word_rank"][RECALL], "best_rank": best,
                          "best_token": tok.decode([tid]) if tid is not None else None, "rank_by_language": per_lang,
                          "languages_without_single_token": sorted(lang for lang, ids in tr["per_language"].items() if not ids)}  # fmt: skip
            old = min(row["org"]["english_rank"], row["alt"]["english_rank"])
            new = min(r for r in (row["org"]["best_rank"], row["alt"]["best_rank"], old) if r is not None)
            row |= {"english_best": old, "best_over_translations": new, "label_old": "not read" if old > A.NOT_READ_RANK else "read",
                    "label_new": "not read" if new > A.NOT_READ_RANK else "read"}  # fmt: skip
            row["flip"] = row["label_old"] != row["label_new"]
            row["stored_matches"] = all(row[v]["english_rank"] == row[v]["stored_rank"] for v in ("org", "alt"))
            rows.append(row)
    A.X.write_jsonl(out_dir / "items.jsonl", rows)
    n, flips = len(rows), sum(r["flip"] for r in rows)
    ents = [r["entity"] for r in rows]
    boot = A.X.resampled_rates({"flip": [int(r["flip"]) for r in rows]}, ents, A.X.N_BOOT, A.X.BOOT_SEED)["flip"]
    summary = {"model": target, "run": a.run, "n": n, "layer": layer, "seconds": round(time.time() - t0),
               "labels_old": dict(collections.Counter(r["label_old"] for r in rows)), "labels_new": dict(collections.Counter(r["label_new"] for r in rows)),
               "flips": flips, "flip_rate": round(flips / n, 4) if n else None, "flip_rate_wilson95": wilson(flips, n),
               "flip_rate_cluster_bootstrap95": [round(float(np.mean([r["flip"] for r in rows])), 4), *(round(b, 4) for b in A.X.interval(boot))],
               "stored_rank_matches": sum(r["stored_matches"] for r in rows),
               "items_with_a_language_lacking_a_single_token": sum(any(r[v]["languages_without_single_token"] for v in ("org", "alt")) for r in rows),
               "languages_lacking_by_value": {str(v): sorted(l for l, ids in tokens_of(tok, v)["per_language"].items() if not ids) for v in range(1, 11)},
               "decision": None}  # fmt: skip
    if a.preflight:
        want = {k: EXPECT[(target, k)] for (t, k) in EXPECT if t == target}
        ok = all(r["stored_matches"] for r in rows) and all(rows_by(rows)[k][v]["english_rank"] == x for k, d in want.items() for v, x in d.items())
        summary["match"] = bool(ok)
        summary["expected"] = want
    else:
        summary["decision"] = ("translation does not change the verdict" if summary["flip_rate"] <= 0.05 else "report only (flips > 5%)")
        rnd = random.Random(SEED).sample(rows, min(5, n))
        (out_dir / "five_random_items.json").write_text(json.dumps(rnd, indent=1, ensure_ascii=False))
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False), flush=True)


def rows_by(rows: list[dict]) -> dict[str, dict]:
    return {r["key"]: r for r in rows}


if __name__ == "__main__":
    main()
