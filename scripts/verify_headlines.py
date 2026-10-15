"""Recompute part A's headline numbers straight from the raw run files, for a human to check before VERIFIED.md.

Deliberately independent of the experiment code: only json / csv / numpy, one short function per number, each with
the file and formula in its docstring. Prints the recomputed value next to the value claimed in README.md.

    uv run python scripts/verify_headlines.py
"""

import json
import re
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[1] / "results"
EXP10 = R / "exp10_lens_sanity/20261013-205936"  # Qwen3.6-27B, space stripped
# Qwen3.6-27B, trailing space stripped, part B's v4 labels (77 eligible): the README's primary runs.
EXP11 = R / "exp11_bridge_vs_answer_by_layer/20261015-100110"  # v4 J-lens labels
EXP11_JPP = R / "exp11_bridge_vs_answer_by_layer/20261015-100426"  # same ranks, v4 J++ labels
EXP11_V3 = R / "exp11_bridge_vs_answer_by_layer/20261014-092835"  # prompts as published, earlier labels (67 eligible)
EXP12 = R / "exp12_position_map/20261015-100735"  # v4 J-lens labels
EXP14 = R / "exp14_cue_answer_swaps/20261015-111137"  # bridge vs answer lens-vector swaps
EXP14_PINNED = R / "exp14_cue_answer_swaps/20261015-114825"  # the same with the other pair held (pinned.yaml)
EXP15 = R / "exp15_oracle_lens/20261015-123226"  # oracle lens readings (clean, after the J++ bridge swap, mean)
BAND = (32, 48)  # layers averaged over


def jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


# ---- exp11: last prompt token -----------------------------------------------------------------


def exp11_band_share(reader, role, label=None, run=EXP11):
    """exp11 ranks.jsonl: for each eligible item (items.jsonl status == "eligible", optionally one part B label),
    the share of layers 32-48 where `<role>_pool` == 1 (top-1 in its pool); then the mean over items. Status and
    label are the ones the run was made with (its labels file is in manifest.json). Items whose word has no pool
    rank (`<role>_pool` is null: a multi-token answer) are left out."""
    meta = {m["name"]: m for m in jsonl(run / "items.jsonl")}
    names = [n for n, m in meta.items() if m["status"] == "eligible" and (label is None or m["label"] == label)]
    rows = {r["name"]: r for r in jsonl(run / "ranks.jsonl") if r["reader"] == reader}
    vals = []
    for n in names:
        r = rows[n]
        if r[f"{role}_pool"] is None:
            continue
        band = [i for i, layer in enumerate(r["layers"]) if BAND[0] <= layer <= BAND[1]]
        vals.append(np.mean([r[f"{role}_pool"][i] == 1 for i in band]))
    return float(np.mean(vals)), len(vals)


# ---- exp12: every prompt position -----------------------------------------------------------------


def exp12_load(reader):
    """grids_<reader>.npz holds, per item and field, a [layers, positions] array of ranks (key "<item>|<field>");
    items.jsonl gives each position's offset from the last content token; layers.json the layer of each row."""
    meta = {m["name"]: m for m in jsonl(EXP12 / "items.jsonl")}
    layers = json.loads((EXP12 / "layers.json").read_text())[reader]
    band = [i for i, layer in enumerate(layers) if BAND[0] <= layer <= BAND[1]]
    z = np.load(EXP12 / f"grids_{reader}.npz")
    eligible = [n for n, m in meta.items() if m["status"] == "eligible"]
    return meta, layers, band, z, eligible


def exp12_share_at_offset(reader, role, offset):
    """Mean over eligible items of: share of layers 32-48 with `<role>_pool` == 1 at that offset (items without
    that word's grid, i.e. a multi-token answer, are left out)."""
    meta, _, band, z, eligible = exp12_load(reader)
    vals = []
    for n in eligible:
        if offset in meta[n]["offsets"] and f"{n}|{role}_pool" in z:
            col = meta[n]["offsets"].index(offset)
            vals.append(np.mean(z[f"{n}|{role}_pool"][band, col] == 1))
    return float(np.mean(vals)), len(vals)


def exp12_missed_rescued(reader):
    """Items whose bridge is top-1 in < half of layers 32-48 at the true last token (last column): how many, and
    the share of them with the bridge (and, as control, the distractor) top-1 in >= half the band layers at some
    earlier token."""
    _, _, band, z, eligible = exp12_load(reader)
    missed = rescued = control = 0
    for n in eligible:
        b = (z[f"{n}|bridge_pool"][band] == 1).mean(0)  # share per position
        d = (z[f"{n}|distractor_pool"][band] == 1).mean(0)
        if b[-1] < 0.5:
            missed += 1
            rescued += b[:-1].max() >= 0.5
            control += d[:-1].max() >= 0.5
    return missed, rescued / missed, control / missed


def exp12_first_layer_half(reader, role, offset):
    """First layer at which at least half of the eligible items have `<role>_pool` == 1 at that offset (items
    without that word's grid left out)."""
    meta, layers, _, z, eligible = exp12_load(reader)
    top = [
        z[f"{n}|{role}_pool"][:, meta[n]["offsets"].index(offset)] == 1
        for n in eligible
        if offset in meta[n]["offsets"] and f"{n}|{role}_pool" in z
    ]
    share = np.mean(top, axis=0)
    return layers[int(np.argmax(share >= 0.5))]


def exp12_cue_share(reader, word, band=BAND, best=False):
    """The cue phrase (data/cue_spans.json) located in the prompt the item's tokens spell (items.jsonl), minus
    position 0 and the last two positions; per eligible item with that word's grid, the share of `band` layers with
    `<word>_pool` == 1 at an average one of those tokens (or, with best=True, at the best one); mean over items."""
    meta, layers, _, z, eligible = exp12_load(reader)
    cues = json.loads((R.parent / "data" / "cue_spans.json").read_text())["cues"]
    rows = [i for i, layer in enumerate(layers) if band[0] <= layer <= band[1]]
    vals = []
    for n in eligible:
        key = f"{n}|{word}_pool"
        if n not in cues or key not in z:
            continue
        toks = meta[n]["tokens"]
        start = "".join(toks).index(cues[n])
        end, pos, idx = start + len(cues[n]), 0, []
        for i, t in enumerate(toks):
            if pos < end and pos + len(t) > start and 1 <= i <= len(toks) - 3:
                idx.append(i)
            pos += len(t)
        shares = [np.mean(z[key][rows, i] == 1) for i in idx]
        vals.append(max(shares) if best else np.mean(shares))
    return float(np.mean(vals)), len(vals)


def exp14_flip(lens, positions, band, kind, null=False, overlap=None, run=EXP14):
    """outcomes.jsonl: share of questions with flip == True for one lens / positions / band / kind (real or null).
    With overlap="low" / "high": only the questions whose mean over band layers of leakage.jsonl's diff_cosine (for
    that lens and cell) is below / at least its median over questions; returns (rate, flips, n)."""
    rows = [o for o in jsonl(run / "outcomes.jsonl")
            if (o["lens"], o["positions"], o["band"], o["kind"], o["null"]) == (lens, positions, band, kind, null)]  # fmt: skip
    if overlap:
        cos = {}
        for r in jsonl(run / "leakage.jsonl"):
            if (r["lens"], r["positions"], r["band"]) == (lens, positions, band):
                cos.setdefault(r["name"], []).append(r["diff_cosine"])
        mean = {n: float(np.mean(v)) for n, v in cos.items()}
        cut = float(np.median(list(mean.values())))
        keep = {n for n, c in mean.items() if (c < cut) == (overlap == "low")}
        rows = [o for o in rows if o["name"] in keep]
    flips = sum(o["flip"] for o in rows)
    return flips / len(rows), flips, len(rows)


# ---- exp15: oracle lens ------------------------------------------------------------------------------


def _says(word, text):
    """The oracle's text contains `word` as whole words (lower-cased letter runs; a plural s / es allowed)."""
    padded = " " + " ".join(re.findall(r"[^\W\d_]+", text.lower())) + " "
    return any(f" {form} " in padded for form in (word.lower(), word.lower() + "s", word.lower() + "es"))


def exp15_named(role, lens_word="bridge", condition="clean"):
    """reads.jsonl (clean readings): per lens class of `lens_word` (both J-lens and J++ rank 1 / one / neither, from
    the reads' jlens_rank / jpp_rank copied from exp12's grids; for the answer, exp12's grids_<lens>.npz answer_pool),
    the share of readings whose text names `role` (bridge = intermediate, distractor = swap_to, answer, swap_answer),
    each question's share first, then the mean over questions; for the answer, questions with numeric answers are
    left out. Returns {class: share}."""
    field = {"bridge": "intermediate", "distractor": "swap_to", "answer": "answer", "swap_answer": "swap_answer"}[role]
    items = {it["name"]: it for it in json.loads((R.parent / "data/probe_swap.json").read_text())["items"]}
    if lens_word == "answer":
        meta = {m["name"]: m for m in jsonl(EXP12 / "items.jsonl")}
        grids = {lens: np.load(EXP12 / f"grids_{lens}.npz") for lens in ("jlens", "jpp")}
        rows = {r["name"]: r for r in jsonl(EXP15 / "items.jsonl")}
    per_q = {}
    for r in jsonl(EXP15 / "reads.jsonl"):
        if r["condition"] != condition:
            continue
        if lens_word == "bridge":
            ranks = (r["jlens_rank"], r["jpp_rank"])
        else:
            key = f"{r['name']}|answer_pool"
            numeric = any(c.isdigit() for c in items[r["name"]]["answer"] + items[r["name"]]["swap_answer"])
            if key not in grids["jlens"] or numeric:  # numeric answers are left out (list numbering)
                continue
            row = rows[r["name"]]
            col = meta[r["name"]]["offsets"].index(row["read_at"][r["position"]] - (row["seq_len"] - 1))
            ranks = tuple(int(grids[lens][key][r["layer"], col]) for lens in ("jlens", "jpp"))
        cls = {2: "both", 1: "one", 0: "neither"}[sum(x == 1 for x in ranks)]
        per_q.setdefault(cls, {}).setdefault(r["name"], []).append(_says(items[r["name"]][field], r["text"]))
    return {cls: float(np.mean([np.mean(v) for v in qs.values()])) for cls, qs in per_q.items()}


def exp15_after_swap(position, flipped, layer=44):
    """reads.jsonl, after the swap (condition swapped), at `position` and `layer`: share of questions whose text names
    the swap target (swap_to), over the questions whose exp14 J++ cue 24-40 bridge swap flips the answer (`flipped`
    True; exp14 run 20261015-111137 outcomes.jsonl) or keeps it."""
    flips = {o["name"]: o["flip"] for o in jsonl(EXP14 / "outcomes.jsonl")
             if (o["lens"], o["positions"], o["band"], o["kind"], o["null"]) == ("jpp", "cue", "24-40", "bridge", False)}  # fmt: skip
    items = {it["name"]: it for it in json.loads((R.parent / "data/probe_swap.json").read_text())["items"]}
    hits = [_says(items[r["name"]]["swap_to"], r["text"]) for r in jsonl(EXP15 / "reads.jsonl")
            if r["condition"] == "swapped" and r["position"] == position and r["layer"] == layer
            and flips.get(r["name"]) is flipped]  # fmt: skip
    return float(np.mean(hits))


# ---- exp10: lens-eval multihop, pass@10 -------------------------------------------------------------


NUMBER_WORDS = set(
    [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
        "hundred",
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "eleventh",
        "twelfth",
    ]
)


def exp10_pass10(reader, kind=None, band=None):
    """multihop_ranks.jsonl: per item, 1 if any of its intermediates (forms of one bridge, '5' / 'five') has
    min_rank < 10 (0-based rank, best over layers at the last token); mean over items whose intermediates are all
    single tokens (multihop_items.jsonl)."""
    meta = {m["name"]: m for m in jsonl(EXP10 / "multihop_items.jsonl")}
    forms = {}
    for it in json.loads((R.parent / "data" / "lens_eval_multihop.json").read_text())["items"]:
        forms[it["name"]] = [w.strip() for w in it["intermediates"]]

    def kind_of(name):  # number if any form is a numeral / number word; letter if every form is one letter
        f = forms[name]
        if any(w.isdigit() or w.lower() in NUMBER_WORDS for w in f):
            return "number"
        return "letter" if all(len(w) == 1 and w.isalpha() for w in f) else "word"

    per_item = {}
    for r in jsonl(EXP10 / "multihop_ranks.jsonl"):
        if r["reader"] == reader and meta[r["name"]]["all_single_token"] and kind in (None, kind_of(r["name"])):
            if band:  # best layer only within the band: any rank < 10 at one of those layers
                hit = any(
                    rk < 10 for layer, rk in zip(r["layers"], r["ranks"], strict=True) if band[0] <= layer <= band[1]
                )
            else:
                hit = r["min_rank"] < 10
            per_item.setdefault(r["name"], []).append(hit)
    return float(np.mean([any(v) for v in per_item.values()])), len(per_item)


# ---- part B: exp02 swaps (v4, layers 24-40, n=77) and exp03 brew ------------------------------------------------

EXP02 = R / "exp02_swaps"
EXP03 = R / "exp03_brew_swaps"


def exp02_flips(run, condition, null=False, band="24-40"):
    """exp02_swaps/<run>/outcomes.jsonl: {item: flip} for one condition, band and null flag (flip = the greedy
    continuation has the swap answer and not the clean answer; one row per eligible item)."""
    rows = jsonl(EXP02 / run / "outcomes.jsonl")
    return {
        o["name"]: o["flip"] for o in rows if o["condition"] == condition and o["band"] == band and o["null"] == null
    }


def exp02_rate(run, condition, null=False, band="24-40"):
    """Share of eligible items whose swap flips: mean of exp02_flips."""
    f = exp02_flips(run, condition, null, band)
    return float(np.mean(list(f.values()))), len(f)


def exp02_max_null(run):
    """The highest flip rate of any matched-norm random-direction control in the run (null == true rows)."""
    conditions = {o["condition"] for o in jsonl(EXP02 / run / "outcomes.jsonl")}
    return max(exp02_rate(run, c, null=True)[0] for c in conditions)


def exp02_paired_diff(run, a, b):
    """Mean over items of flip(a) - flip(b), same items (the point estimate of the paired bootstrap)."""
    fa, fb = exp02_flips(run, a), exp02_flips(run, b)
    return float(np.mean([fa[n] - fb[n] for n in fa]))


def exp02_bridge_types():
    """PLACES and PEOPLE as listed in scripts/exp02_figures.py (read as literals, not imported)."""
    import ast

    tree = ast.parse((R.parent / "scripts/exp02_figures.py").read_text())
    sets = {
        t.id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        for t in node.targets
        if isinstance(t, ast.Name) and t.id in ("PLACES", "PEOPLE")
    }
    return sets["PLACES"], sets["PEOPLE"]


def exp02_rate_by_type(run, kind):
    """J-part flip rate over items whose bridge (items.jsonl `intermediate`) is a place, a person, or anything else."""
    places, people = exp02_bridge_types()
    bridge = {m["name"]: m["intermediate"] for m in jsonl(EXP02 / run / "items.jsonl")}
    pick = {"place": lambda e: e in places, "person": lambda e: e in people}.get(
        kind, lambda e: e not in places and e not in people
    )
    f = {n: v for n, v in exp02_flips(run, "jpart").items() if pick(bridge[n])}
    return float(np.mean(list(f.values()))), len(f)


def exp02_jpp_superset():
    """main_v4 J-part (24-40): items the J-lens flips and J++ does not, and the reverse."""
    jl, jp = exp02_flips("main_v4_jlens", "jpart"), exp02_flips("main_v4_jpp", "jpart")
    return sum(jl[n] and not jp[n] for n in jl), sum(jp[n] and not jl[n] for n in jl)


def exp03_rate(run, lens, kind, regime, null=False, amp=1, scale=None, field="flip"):
    """exp03_brew_swaps/<run>/outcomes.jsonl: share of rows (one per eligible item) with `field` true, for one lens,
    kind, regime, null flag, amplification and steering scale."""
    rows = [
        o
        for o in jsonl(EXP03 / run / "outcomes.jsonl")
        if (o["lens"], o["kind"], o["regime"], o["null"], o.get("amp", 1), o.get("scale"))
        == (lens, kind, regime, null, amp, scale)
    ]
    return float(np.mean([o[field] for o in rows])), len(rows)


def exp03_changed(run, lens, kind, regime, null, amp=1, scale=None):
    """Share of rows whose answer changed (not kept_clean): the random-direction null's 'answer changed' rate."""
    rate, n = exp03_rate(run, lens, kind, regime, null, amp, scale, field="kept_clean")
    return 1 - rate, n


EXP04 = R / "exp04_brew_patch/patch_map"


def exp04_role_rate(source, group, layer, role):
    """exp04 outcomes.jsonl: share of rows (one per eligible item) for one source (cf / off), position group and
    layer whose answer has that role (b = f(X), c = the counterfactual's answer, A = the original answer)."""
    rows = [
        o for o in jsonl(EXP04 / "outcomes.jsonl") if (o["source"], o["group"], o["layer"]) == (source, group, layer)
    ]
    return float(np.mean([o["role"] == role for o in rows])), len(rows)


def exp04_max_off_changed():
    """The highest share of answers the off-path control's patch changes, over every group and layer."""
    cells = {}
    for o in jsonl(EXP04 / "outcomes.jsonl"):
        if o["source"] == "off":
            cells.setdefault((o["group"], o["layer"]), []).append(o["role"] != "A")
    return max(float(np.mean(v)) for v in cells.values())


def main():
    checks = [
        ("exp10", "27B stripped, pass@10, J++", exp10_pass10("jpp")[0], 0.77),
        ("exp10", "27B stripped, pass@10, logit lens", exp10_pass10("logit")[0], 0.54),
        ("exp10", "27B stripped, pass@10, J-lens", exp10_pass10("jlens")[0], 0.58),
        ("exp10", "word bridges, J-lens", exp10_pass10("jlens", "word")[0], 0.67),
        ("exp10", "word bridges, logit lens", exp10_pass10("logit", "word")[0], 0.52),
        ("exp10", "word bridges, J++", exp10_pass10("jpp", "word")[0], 0.89),
        ("exp10", "number bridges, J-lens", exp10_pass10("jlens", "number")[0], 0.41),
        ("exp10", "number bridges, logit lens", exp10_pass10("logit", "number")[0], 0.65),
        ("exp10", "number bridges, layers 32-48, logit lens", exp10_pass10("logit", "number", (32, 48))[0], 0.06),
        ("exp10", "number bridges, layers 32-48, J-lens", exp10_pass10("jlens", "number", (32, 48))[0], 0.18),
        ("exp10", "number bridges, layers 32-48, J++", exp10_pass10("jpp", "number", (32, 48))[0], 0.41),
        ("exp10", "word bridges, layers 32-48, J-lens", exp10_pass10("jlens", "word", (32, 48))[0], 0.30),
        ("exp11", "bridge top-1 among entities, L32-48, J-lens", exp11_band_share("jlens", "bridge")[0], 0.57),
        ("exp11", "bridge top-1, J++", exp11_band_share("jpp", "bridge")[0], 0.56),
        ("exp11", "bridge top-1, logit lens", exp11_band_share("logit", "bridge")[0], 0.25),
        ("exp11", "distractor top-1, J-lens", exp11_band_share("jlens", "distractor")[0], 0.05),
        ("exp11", "answer top-1 among answers, J-lens", exp11_band_share("jlens", "answer")[0], 0.41),
        ("exp11", "J-lens, J-mediated (v4 J-lens labels)", exp11_band_share("jlens", "bridge", "J-mediated")[0], 0.73),
        ("exp11", "J-lens, 'neither' (v4 J-lens labels)", exp11_band_share("jlens", "bridge", "neither")[0], 0.50),
        (
            "exp11",
            "J++, J-mediated (v4 J++ labels)",
            exp11_band_share("jpp", "bridge", "J-mediated", EXP11_JPP)[0],
            0.70,
        ),
        ("exp11", "J++, 'neither' (v4 J++ labels)", exp11_band_share("jpp", "bridge", "neither", EXP11_JPP)[0], 0.41),
        (
            "exp11",
            "earlier labels: J-lens, J-mediated",
            exp11_band_share("jlens", "bridge", "J-mediated", EXP11_V3)[0],
            0.79,
        ),
        (
            "exp11",
            "earlier labels: J-lens, 'neither'",
            exp11_band_share("jlens", "bridge", "neither", EXP11_V3)[0],
            0.49,
        ),
        ("exp12", "bridge top-1 at offset -1, J-lens", exp12_share_at_offset("jlens", "bridge", -1)[0], 0.65),
        ("exp12", "bridge top-1 at offset 0, J-lens", exp12_share_at_offset("jlens", "bridge", 0)[0], 0.57),
        ("exp12", "answer top-1 at offset 0, J-lens", exp12_share_at_offset("jlens", "answer", 0)[0], 0.41),
        ("exp12", "missed at the last token, J-lens (count)", exp12_missed_rescued("jlens")[0], 30),
        ("exp12", "... of those, bridge on top earlier", exp12_missed_rescued("jlens")[1], 0.73),
        ("exp12", "... distractor on top earlier (control)", exp12_missed_rescued("jlens")[2], 0.33),
        ("exp12", "half of items: bridge at -1, first layer", exp12_first_layer_half("jlens", "bridge", -1), 23),
        ("exp12", "half of items: answer at 0, first layer", exp12_first_layer_half("jlens", "answer", 0), 44),
        ("exp12", "cue phrase, average token: bridge, J-lens", exp12_cue_share("jlens", "bridge")[0], 0.56),
        ("exp12", "cue phrase, average token: distractor", exp12_cue_share("jlens", "distractor")[0], 0.07),
        ("exp12", "cue phrase, average token: answer", exp12_cue_share("jlens", "answer")[0], 0.17),
        ("exp12", "cue phrase, average token: swap answer", exp12_cue_share("jlens", "swap_answer")[0], 0.02),
        ("exp12", "cue phrase, best token: bridge", exp12_cue_share("jlens", "bridge", best=True)[0], 0.80),
        ("exp12", "cue phrase, best token: distractor", exp12_cue_share("jlens", "distractor", best=True)[0], 0.19),
        ("exp14", "cue 24-40, bridge swap, J++", exp14_flip("jpp", "cue", "24-40", "bridge")[0], 0.30),
        ("exp14", "cue 24-40, bridge swap, J-lens", exp14_flip("jlens", "cue", "24-40", "bridge")[0], 0.22),
        ("exp14", "cue 24-40, answer swap, J++", exp14_flip("jpp", "cue", "24-40", "answer")[0], 0.17),
        ("exp14", "cue 24-40, answer swap, J-lens", exp14_flip("jlens", "cue", "24-40", "answer")[0], 0.11),
        ("exp14", "cue 24-40, answer swap, null, J++", exp14_flip("jpp", "cue", "24-40", "answer", True)[0], 0.0),
        ("exp14", "control: answer swap, last 40-56, J++", exp14_flip("jpp", "last", "40-56", "answer")[0], 0.40),
        ("exp14", "control: answer swap, last 40-56, J-lens", exp14_flip("jlens", "last", "40-56", "answer")[0], 0.39),
        (
            "exp14",
            "low overlap: answer swap on cue, J++ (flips)",
            exp14_flip("jpp", "cue", "24-40", "answer", overlap="low")[1],
            0,
        ),
        (
            "exp14",
            "low overlap: answer swap on cue, J-lens (flips)",
            exp14_flip("jlens", "cue", "24-40", "answer", overlap="low")[1],
            1,
        ),
        (
            "exp14",
            "low overlap: bridge swap on cue, J++",
            exp14_flip("jpp", "cue", "24-40", "bridge", overlap="low")[0],
            0.14,
        ),
        *(
            (
                "exp14",
                f"pinned: {what}, {name}",
                exp14_flip(lens, pos, band, kind, overlap=half, run=EXP14_PINNED)[0],
                v,
            )
            for what, pos, band, kind, half, claimed in (
                ("cue 24-40, bridge swapped, answer held", "cue", "24-40", "bridge_pinned", None, (0.18, 0.18)),
                ("cue 24-40, answer swapped, bridge held", "cue", "24-40", "answer_pinned", None, (0.06, 0.01)),
                ("cue, high overlap, bridge held-answer", "cue", "24-40", "bridge_pinned", "high", (0.28, 0.24)),
                ("cue, high overlap, answer held-bridge", "cue", "24-40", "answer_pinned", "high", (0.08, 0.03)),
                ("control: last 40-56, answer held-bridge", "last", "40-56", "answer_pinned", None, (0.26, 0.17)),
            )
            for (lens, name), v in zip((("jlens", "J-lens"), ("jpp", "J++")), claimed, strict=True)
        ),
        ("exp15", "both lenses: oracle names the bridge", exp15_named("bridge")["both"], 0.82),
        ("exp15", "neither lens: oracle names the bridge", exp15_named("bridge")["neither"], 0.37),
        ("exp15", "neither lens (answer): oracle names the answer", exp15_named("answer", "answer")["neither"], 0.33),
        (
            "exp15",
            "neither lens (answer): names the swap answer",
            exp15_named("swap_answer", "answer")["neither"],
            0.08,
        ),
        ("exp15", "after swap, flipped, L44 last word: target", exp15_after_swap("last", True), 0.61),
        ("exp15", "after swap, flipped, L44 -1: target", exp15_after_swap("prev", True), 0.74),
        ("exp15", "after swap, kept, L44 last word: target", exp15_after_swap("last", False), 0.09),
        ("exp15", "after swap, kept, L44 -1: target", exp15_after_swap("prev", False), 0.11),
        (
            "exp14",
            "pinned: cue 24-40, bridge held-answer, null, J++",
            exp14_flip("jpp", "cue", "24-40", "bridge_pinned", True, run=EXP14_PINNED)[0],
            0.0,
        ),
        ("exp02", "J-part flips, J++ (main_v4_jpp)", exp02_rate("main_v4_jpp", "jpart")[0], 0.52),
        ("exp02", "J-part flips, J-lens (main_v4_jlens)", exp02_rate("main_v4_jlens", "jpart")[0], 0.35),
        ("exp02", "remainder flips, J++", exp02_rate("main_v4_jpp", "remainder")[0], 0.08),
        ("exp02", "remainder flips, J-lens", exp02_rate("main_v4_jlens", "remainder")[0], 0.12),
        ("exp02", "remainder, J-space held, J++", exp02_rate("main_v4_jpp", "remainder_clamped")[0], 0.01),
        ("exp02", "remainder, J-space held, J-lens", exp02_rate("main_v4_jlens", "remainder_clamped")[0], 0.04),
        ("exp02", "raw lens vectors, J++", exp02_rate("main_v4_jpp", "raw_jlens")[0], 0.49),
        ("exp02", "raw lens vectors, J-lens", exp02_rate("main_v4_jlens", "raw_jlens")[0], 0.40),
        ("exp02", "full probe (lens-free)", exp02_rate("main_v4_jpp", "full_probe")[0], 0.27),
        (
            "exp02",
            "highest random-direction control, either lens",
            max(map(exp02_max_null, ("main_v4_jpp", "main_v4_jlens"))),
            0.03,
        ),
        ("exp02", "J-part minus remainder, J++ (pts)", exp02_paired_diff("main_v4_jpp", "jpart", "remainder"), 0.44),
        ("exp02", "J-part minus remainder, J-lens", exp02_paired_diff("main_v4_jlens", "jpart", "remainder"), 0.23),
        ("exp02", "matched-alignment flips, J++", exp02_rate("matched_v4_jpp", "jpart_matched")[0], 0.14),
        ("exp02", "matched-alignment flips, J-lens", exp02_rate("matched_v4_jlens", "jpart_matched")[0], 0.10),
        ("exp02", "J-part minus matched, J++", exp02_paired_diff("matched_v4_jpp", "jpart", "jpart_matched"), 0.38),
        (
            "exp02",
            "J-part minus matched, J-lens",
            exp02_paired_diff("matched_v4_jlens", "jpart", "jpart_matched"),
            0.25,
        ),
        ("exp02", "J-part at the cue phrase, J++", exp02_rate("main_v4_jpp_pos-cue", "jpart")[0], 0.31),
        ("exp02", "J-part at the cue phrase, J-lens", exp02_rate("main_v4_jlens_pos-cue", "jpart")[0], 0.19),
        ("exp02", "J-part at offset -1 only, J++", exp02_rate("main_v4_jpp_pos-prev", "jpart")[0], 0.09),
        ("exp02", "J-part, bridge a place, J++", exp02_rate_by_type("main_v4_jpp", "place")[0], 0.88),
        ("exp02", "J-part, bridge a person, J++", exp02_rate_by_type("main_v4_jpp", "person")[0], 0.86),
        ("exp02", "J-part, bridge anything else, J++", exp02_rate_by_type("main_v4_jpp", "other")[0], 0.25),
        ("exp02", "J-part, bridge a person, J-lens", exp02_rate_by_type("main_v4_jlens", "person")[0], 0.14),
        ("exp02", "items J-lens flips and J++ does not (count)", exp02_jpp_superset()[0], 0),
        ("exp02", "items J++ flips and J-lens does not (count)", exp02_jpp_superset()[1], 13),
        (
            "exp03",
            "start swap S->S' x3, 8-24, J++",
            exp03_rate("swap_amp", "jpp", "start", "start_line", amp=3)[0],
            0.61,
        ),
        ("exp03", "start swap x3, J-lens", exp03_rate("swap_amp", "jlens", "start", "start_line", amp=3)[0], 0.17),
        (
            "exp03",
            "start swap x3, random direction, J++",
            exp03_rate("swap_amp", "jpp", "start", "start_line", True, 3)[0],
            0.01,
        ),
        (
            "exp03",
            "intermediate swap x3 after start, J++",
            exp03_rate("swap_amp", "jpp", "swap", "after_start", amp=3)[0],
            0.0,
        ),
        (
            "exp03",
            "intermediate swap x3 every position, J++",
            exp03_rate("swap_amp", "jpp", "swap", "all", amp=3)[0],
            0.03,
        ),
        (
            "exp03",
            "fresh items: start-line steer 3%, J++",
            exp03_rate("fresh_steer", "jpp", "steer_start", "start_line", scale=0.03)[0],
            0.63,
        ),
        (
            "exp03",
            "fresh items: start-line steer 3%, J-lens",
            exp03_rate("fresh_steer", "jlens", "steer_start", "start_line", scale=0.03)[0],
            0.30,
        ),
        (
            "exp03",
            "fresh items: random direction 3%, flips, J++",
            exp03_rate("fresh_steer", "jpp", "steer_start", "start_line", True, scale=0.03)[0],
            0.0,
        ),
        (
            "exp03",
            "fresh items: random direction 3%, answer changed, J++",
            exp03_changed("fresh_steer", "jpp", "steer_start", "start_line", True, scale=0.03)[0],
            0.0,
        ),
        ("exp04", "after the start line, layer 36: f(X)", exp04_role_rate("cf", "after_start", 36, "b")[0], 0.11),
        ("exp04", "after the start line, layer 46: f(X)", exp04_role_rate("cf", "after_start", 46, "b")[0], 0.48),
        ("exp04", "after the start line, layer 50: f(X)", exp04_role_rate("cf", "after_start", 50, "b")[0], 0.48),
        ("exp04", "after the start line, layer 52: c", exp04_role_rate("cf", "after_start", 52, "c")[0], 0.71),
        ("exp04", "the start line, layer 46: original answer", exp04_role_rate("cf", "start_line", 46, "A")[0], 1.0),
        ("exp04", "rule lines, layer 24: c", exp04_role_rate("cf", "rules", 24, "c")[0], 0.95),
        ("exp04", "rule lines, layer 40: original answer", exp04_role_rate("cf", "rules", 40, "A")[0], 0.84),
        ("exp04", "off-path control, most answers changed", exp04_max_off_changed(), 0.02),
    ]
    width = max(len(c[1]) for c in checks)
    for exp, what, got, claimed in checks:
        ok = round(got, 2) == round(claimed, 2) if isinstance(claimed, float) else got == claimed
        shown = f"{got:.4f}" if isinstance(got, float) else str(got)
        print(f"{'OK  ' if ok else 'DIFF'} {exp}  {what:<{width}}  recomputed {shown:>8}  README {claimed}")
    n11 = exp11_band_share("jlens", "bridge")[1]
    n12 = exp12_share_at_offset("jlens", "bridge", -1)[1]
    print(
        f"\nitems: exp11 eligible n={n11}, exp12 eligible at offset -1 n={n12}, exp10 single-token n={exp10_pass10('jpp')[1]}"
    )


if __name__ == "__main__":
    main()
