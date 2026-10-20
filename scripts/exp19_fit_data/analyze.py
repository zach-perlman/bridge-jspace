"""exp19_fit_data: the manifest's comparisons on an evaluate output. Standard library only.

    python3 scripts/exp19_fit_data/analyze.py OUT_DIR [EVAL_RANKS_CSV ...]   (writes OUT_DIR/analysis_<utc>/)
With no CSV given it reads OUT_DIR/eval_ranks.csv. Several CSVs (separate evaluate calls) are pooled; each lens must
come from one file only.

pass@k as J++'s pass_at_k_over_layers (item-weighted): per (item, intermediate) the best rank over layers, a hit if
<= k, averaged over an item's intermediates, then over the family's items; macro = the mean of the five families.
Each 25-prompt condition is compared with wiki_a, and the 64-prompt lenses (fit_v3) with each other, with their
25-prompt lenses and with the published J++, lens kind by lens kind (J++ with J++, pooled with pooled): the paired
bootstrap over items (10,000 resamples, seed 0) of the difference in pass@k; for macro each family is resampled on its
own and the five means averaged. H1 splits multihop by intermediate: digits or a number word, against the rest.
"""

import csv
import json
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

FAMILIES = ("multihop", "multilingual", "typo", "association", "poetry")
KS = (1, 10)
N_BOOT = 10_000
NUMBER_WORDS = set(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million "
    "billion dozen".split()
)


def is_number(word: str) -> bool:
    w = word.strip().lower()
    return bool(re.fullmatch(r"[\d.,]+", w)) or w in NUMBER_WORDS


def load(paths):
    """best[(family, lens, item, intermediate)] = min rank over layers, and the file each lens came from."""
    best, source = {}, {}
    for path in paths:
        with path.open() as f:
            for r in csv.DictReader(f):
                assert source.setdefault(r["lens"], str(path)) == str(path), f"{r['lens']} is in two files"
                key = (r["eval"], r["lens"], r["item"], r["intermediate"])
                rank = int(r["rank"])
                if key not in best or rank < best[key]:
                    best[key] = rank
    return best, source


def item_scores(best, k, keep=lambda intermediate: True):
    """scores[(family, lens)][item] = fraction of the item's intermediates hit at k."""
    hits = defaultdict(lambda: defaultdict(list))
    for (family, lens, item, intermediate), rank in best.items():
        if keep(intermediate):
            hits[(family, lens)][item].append(rank <= k)
    return {g: {i: sum(h) / len(h) for i, h in items.items()} for g, items in hits.items()}


def mean(xs):
    return sum(xs) / len(xs)


def paired(scores, family_list, a, b, rng):
    """b - a over the families' items: point estimate and 95% bootstrap CI (macro = mean over families)."""
    diffs = []
    for family in family_list:
        sa, sb = scores[(family, a)], scores[(family, b)]
        assert sa.keys() == sb.keys(), (family, a, b)
        diffs.append([sb[i] - sa[i] for i in sorted(sa)])
    point = mean([mean(d) for d in diffs])
    boot = sorted(
        mean([mean([d[rng.randrange(len(d))] for _ in d]) for d in diffs]) for _ in range(N_BOOT)
    )
    return point, boot[int(0.025 * N_BOOT)], boot[int(0.975 * N_BOOT) - 1]


def main(res: Path, csvs: list[Path]) -> None:
    out = res / time.strftime("analysis_%Y%m%dT%H%M%SZ", time.gmtime()) / "summary.json"
    best, source = load(csvs or [res / "eval_ranks.csv"])
    lenses = sorted({lens for _, lens, _, _ in best})
    conds = [c for c in ("wiki_a", "math", "wiki_b", "chat", "mix") if f"jpp_{c}" in lenses]
    summary = {"lens_files": source, "conditions": conds, "pass_at_k": {}, "comparisons": {}, "H1_multihop_split": {}}

    for k in KS:
        scores = item_scores(best, k)
        table = {
            lens: {f: mean(list(scores[(f, lens)].values())) for f in FAMILIES if (f, lens) in scores} for lens in lenses
        }
        for lens in lenses:
            table[lens]["macro"] = mean([table[lens][f] for f in FAMILIES])
        summary["pass_at_k"][k] = table
        print(f"\npass@{k} (item-weighted; n items: " + ", ".join(
            f"{f} {len(scores[(f, lenses[0])])}" for f in FAMILIES) + ")")
        print(f"{'lens':34s}" + "".join(f"{f[:10]:>12s}" for f in (*FAMILIES, "macro")))
        for lens in lenses:
            print(f"{lens:34s}" + "".join(f"{table[lens][f]:12.3f}" for f in (*FAMILIES, "macro")))

        rng = random.Random(0)
        comps = [(f"{kind}_wiki_a", f"{kind}_{c}") for kind in ("jpp", "pooled") for c in conds if c != "wiki_a"]
        if "Qwen3.6-27B_jpp_lens" in lenses:
            comps.append(("Qwen3.6-27B_jpp_lens", "jpp_wiki_a"))  # what fitting on 25 prompts instead of 64 costs
        for kind in ("jpp", "pooled"):  # fit_v3: chat vs WikiText at 64 prompts, and 64 vs 25 within each pool
            comps += [(a, b) for a, b in ((f"{kind}_wiki64", f"{kind}_chat64"), (f"{kind}_chat", f"{kind}_chat64"),
                      (f"{kind}_wiki_a", f"{kind}_wiki64")) if a in lenses and b in lenses]
        comps += [("Qwen3.6-27B_jpp_lens", b) for b in ("jpp_wiki64", "jpp_chat64") if b in lenses]
        print(f"\npass@{k}: B - A, 95% paired bootstrap CI over items ('*' = CI excludes 0)")
        for a, b in comps:
            row = {}
            for f in (*FAMILIES, "macro"):
                point, lo, hi = paired(scores, FAMILIES if f == "macro" else (f,), a, b, rng)
                row[f] = {"diff": point, "ci95": [lo, hi], "excludes_0": lo > 0 or hi < 0}
            summary["comparisons"].setdefault(k, {})[f"{b} - {a}"] = row
            print(f"{b + ' - ' + a:44s}" + "".join(
                f"  {f[:5]} {row[f]['diff']:+.3f} [{row[f]['ci95'][0]:+.2f},{row[f]['ci95'][1]:+.2f}]"
                + ("*" if row[f]["excludes_0"] else " ") for f in (*FAMILIES, "macro")))

        split = {}
        for name, keep in (("number", is_number), ("other", lambda w: not is_number(w))):
            s = item_scores({key: r for key, r in best.items() if key[0] == "multihop"}, k, keep)
            split[name] = {"n_items": len(s[("multihop", lenses[0])]),
                           "pass": {lens: mean(list(s[("multihop", lens)].values())) for lens in lenses}}
            for c in conds:
                if c != "wiki_a":
                    for kind in ("jpp", "pooled"):
                        point, lo, hi = paired(s, ("multihop",), f"{kind}_wiki_a", f"{kind}_{c}", rng)
                        split[name][f"{kind}_{c} - {kind}_wiki_a"] = {"diff": point, "ci95": [lo, hi]}
        summary["H1_multihop_split"][k] = split
        print(f"\nH1 pass@{k}: multihop split by intermediate")
        for name, d in split.items():
            print(f"  {name} ({d['n_items']} items): " + ", ".join(
                f"{key} {v['diff']:+.3f} [{v['ci95'][0]:+.2f},{v['ci95'][1]:+.2f}]"
                for key, v in d.items() if " - " in key))

    numbers = sorted({w for f, _, _, w in best if f == "multihop" and is_number(w)})
    summary["H1_number_intermediates"] = numbers
    print("\nmultihop intermediates counted as numbers:", numbers)
    out.parent.mkdir()
    out.write_text(json.dumps(summary, indent=1) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main(Path(sys.argv[1]), [Path(a) for a in sys.argv[2:]])
