"""x53_subset27b (batch 53, test 53.5; Dan 29 Oct 09:30, jobs/c3/batch53.yaml): the 27B on its position-route scenes.

CPU only, existing outcomes; no forward pass. The subset: the routes test's scenes (C1 and C2; C0 has no position
answer) where the lookup's answer under the whole change is the position route's digit (x6_routes.classify's label
"position"). On that subset, from the keep-only run (one forward pass per scene with every arm below): the position
share without the address (no_alf) against without a random part of its share (no_alf_rand), and with the address alone
(keep_alf) against a random part of its share alone (keep_alf_rand). The swap at s = 2 from x8_write (the routes test's
C2 items, the address written toward another locker's slot): the share of writes the lookup follows (class "target"),
on the subset's C2 scenes, with the random write at s = 4 beside (x8_write has no random write at s = 2). The same
subset logic on the 9B beside, and, descriptive, the 27B's subset scenes read on the 9B.

Rule (verbatim, below in RULE): "same mechanism, used less" iff back >= 0.25 and left <= 0.10, where back = the address
alone's position share / the whole change's (1 on the subset by construction) and left = the position share without the
address, both raw shares on the pooled C1 + C2 subset; the differences from the random parts are reported beside.
Cluster bootstrap over the bridge items (x0_necessity.resampled_rates: 10,000 resamples, seed 0). UNVERIFIED.

uv run python scripts/x53_subset27b.py                 # CPU, writes results/x53_subset27b/x53_subset27b-<UTC>/
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x53_subset27b"
OUT_ROOT = pins.RESULTS_DIR / EXP
ROUTES_DIR, WRITE_DIR = pins.RESULTS_DIR / "x6_routes", pins.RESULTS_DIR / "x8_write"
# keeponly: the subset and every arm (one pass per scene); check: the routes run's own whole change on the same scenes
RUNS = {
    "qwen3.6-27b": {"keeponly": "x6_routes_keeponly_27b", "check": "x6_routes_27b", "swap": "x8_write_27b"},
    "qwen3.5-9b": {"keeponly": "qwen35_9b_x6_routes_keeponly", "check": "qwen35_9b_x6_routes",
                   "swap": "qwen35_9b_x8_write"},
}  # fmt: skip
NAMES = {"qwen3.6-27b": "Qwen3.6-27B", "qwen3.5-9b": "Qwen3.5-9B"}
SUBJECT, BESIDE = "qwen3.6-27b", "qwen3.5-9b"
CONDS = ("C1", "C2")  # the conditions with a position route
ARMS = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand")
SWAP_S, SWAP_RAND_S = 2, 4
BACK, LEFT = 0.25, 0.10
EPS = 1e-9  # as x6_routes: a share exactly at the bar counts as at the bar
LABEL = {True: "same mechanism, used less", False: "the 27B differs"}
RULE = (
    "Keep the scenes where the 27B's lookup goes by position under the whole change; recompute on them: position "
    'without the address vs random, the address alone, the swap at s = 2. Rule: "same mechanism, used less" if the '
    "address alone brings >= 0.25 of position answers back and its removal leaves <= 0.10 (the 9B's pattern); \"the "
    '27B differs" otherwise. Same subset on the 9B beside.'
)
ARM_TEXT = {"whole": "the whole change", "no_alf": "without the address", "no_alf_rand": "without a random part",
            "keep_alf": "the address alone", "keep_alf_rand": "a random part alone",
            "swap": f"the swap at s = {SWAP_S}", "swap_rand": f"a random write at s = {SWAP_RAND_S}"}  # fmt: skip


def lookup_rows(rows: list[dict], conds: tuple[str, ...] = CONDS) -> dict[tuple[str, str], dict[str, dict]]:
    """(condition, scene) -> arm -> the lookup's outcome row."""
    out: dict[tuple[str, str], dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        if r["reader"] == X.LOOKUP and r["condition"] in conds:
            key = (r["condition"], r["scene"])
            assert r["arm"] not in out[key], f"two rows for {key} {r['arm']}"
            out[key][r["arm"]] = r
    return dict(out)


def position_subset(by: dict[tuple[str, str], dict[str, dict]]) -> list[tuple[str, str]]:
    """The scenes whose lookup answers the position route's digit under the whole change, sorted."""
    return sorted(k for k, arms in by.items() if arms["whole"]["route"] == "position")


def position_vectors(by: dict, keys: list[tuple[str, str]], arms: tuple[str, ...] = ARMS) -> dict[str, list[int]]:
    """Per arm, 1 where the lookup answers the position route's digit, in keys' order."""
    return {a: [int(by[k][a]["route"] == "position") for k in keys] for a in arms}


def pattern(back: float, left: float) -> bool:
    """The 9B's pattern: the address alone brings >= BACK of position answers back and its removal leaves <= LEFT."""
    return back >= BACK - EPS and left <= LEFT + EPS


def ci3(v: float, rr: np.ndarray) -> list[float]:
    return [float(v), *X.interval(rr)]


def subset_cell(by: dict, keys: list[tuple[str, str]], n_boot: int) -> dict | None:
    """Every arm's position share on keys with cluster-bootstrap CIs; the paired differences from the random parts;
    back and left as the rule reads them."""
    if not keys:
        return None
    sw = position_vectors(by, keys)
    ents = [by[k]["whole"]["entity"] for k in keys]
    rr = X.resampled_rates(sw, ents, n_boot)
    share = {a: ci3(np.mean(sw[a]), rr[a]) for a in ARMS}
    whole = share["whole"][0]
    back = share["keep_alf"][0] / whole if whole > 0 else float("nan")
    with np.errstate(divide="ignore", invalid="ignore"):
        back_r = rr["keep_alf"] / rr["whole"]
    return {
        "n": len(keys), "entities": len(set(ents)), "share": share,
        "removal_beyond_random": ci3(share["no_alf_rand"][0] - share["no_alf"][0], rr["no_alf_rand"] - rr["no_alf"]),
        "alone_beyond_random": ci3(share["keep_alf"][0] - share["keep_alf_rand"][0], rr["keep_alf"] - rr["keep_alf_rand"]),
        "back": ci3(back, back_r), "left": share["no_alf"],
    }  # fmt: skip


def swap_cell(rows: list[dict], scenes: set[str], n_boot: int) -> dict | None:
    """x8_write's lookup rows on these C2 scenes: the target share of the writes at SWAP_S (and their original / third
    shares) and of the random writes at SWAP_RAND_S; the bridge item's slot j per scene."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP and r["scene"] in scenes]
    out: dict = {"scenes": len(scenes), "j": dict(collections.Counter(r["j"] for r in lk if r["kind"] == "none"))}
    for name, kind, s in (("swap", "write", SWAP_S), ("swap_rand", "random", SWAP_RAND_S)):
        mine = [r for r in lk if r["kind"] == kind and r["s"] == s]
        if not mine:
            out[name] = None
            continue
        sw = {c: [int(r["class"] == c) for r in mine] for c in ("target", "original", "third", "other")}
        rr = X.resampled_rates(sw, [r["entity"] for r in mine], n_boot)
        out[name] = {"n_writes": len(mine), **{c: ci3(np.mean(v), rr[c]) for c, v in sw.items()}}
    return out


def model_block(target: str, n_boot: int) -> dict:
    run = RUNS[target]
    by = lookup_rows(X.read_jsonl(ROUTES_DIR / run["keeponly"] / "outcomes.jsonl"))
    check = lookup_rows(X.read_jsonl(ROUTES_DIR / run["check"] / "outcomes.jsonl"))
    swaps = X.read_jsonl(WRITE_DIR / run["swap"] / "outcomes.jsonl")
    assert by, f"{target}: no routes outcomes in {run['keeponly']}"
    assert swaps, f"{target}: no swap outcomes in {run['swap']}"
    keys = position_subset(by)
    blk: dict = {"target": target, "runs": run, "scenes": {c: sum(k[0] == c for k in by) for c in CONDS},
                 "subset": {"pooled": subset_cell(by, keys, n_boot)}}  # fmt: skip
    for c in CONDS:
        blk["subset"][c] = subset_cell(by, [k for k in keys if k[0] == c], n_boot)
    pooled = blk["subset"]["pooled"]
    blk["pattern"] = pattern(pooled["back"][0], pooled["left"][0]) if pooled else None
    # the routes run (same scenes, its own forward pass): does it put the same scenes on the position route?
    common = [k for k in keys if k in check]
    blk["check"] = {"run": run["check"], "subset_in_check": len(common),
                    "also_position_in_check": sum(check[k]["whole"]["route"] == "position" for k in common),
                    "check_position_scenes": sum(a["whole"]["route"] == "position" for a in check.values()),
                    "no_alf_position_share_in_check": float(np.mean([check[k]["no_alf"]["route"] == "position"
                                                                     for k in common])) if common else None}  # fmt: skip
    c2 = {s for c, s in by if c == "C2"}
    sub2 = {s for c, s in keys if c == "C2"}
    ids = {r["scene"]: r["entity"] for r in swaps if r["reader"] == X.LOOKUP}
    mism = [s for s in c2 if s not in ids or ids[s] != by[("C2", s)]["whole"]["entity"]]
    assert not mism, f"{target}: x8_write's scenes differ from the routes test's C2 scenes: {mism[:5]}"
    blk["swap"] = {"subset": swap_cell(swaps, sub2, n_boot), "rest": swap_cell(swaps, c2 - sub2, n_boot),
                   "all": swap_cell(swaps, c2, n_boot)}  # fmt: skip
    blk["_by"], blk["_keys"] = by, keys
    return blk


def on_other(subj: dict, other: dict, n_boot: int) -> dict | None:
    """Descriptive: the subject's subset scenes (same scene id and bridge item) read on the other model's runs."""
    keys = [k for k in subj["_keys"] if k in other["_by"]
            and other["_by"][k]["whole"]["entity"] == subj["_by"][k]["whole"]["entity"]]  # fmt: skip
    return subset_cell(other["_by"], keys, n_boot)


def fmt(v) -> str:
    return "-" if v is None or v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def verdict_md(blocks: dict, cross: dict | None, n_boot: int, stamp: str) -> list[str]:
    s, b = blocks[SUBJECT], blocks[BESIDE]
    label = LABEL[s["pattern"]]
    lines = [
        "# 53.5: the 27B on its position-route scenes", "",
        f"Batch 53, test 53.5 (jobs/c3/batch53.yaml, Dan 29 Oct 09:30; written {stamp}). CPU only, existing outcomes. "
        "No prediction. UNVERIFIED.", "",
        "Rule (fixed in advance, verbatim):", "", f"> {RULE}", "",
        "As computed:",
        "- Subset: the routes test's C1 and C2 scenes (C0 has no position answer) where the lookup's answer under the "
        "whole change is the position route's digit (x6_routes' label \"position\"), from the keep-only run, which "
        "has every arm below on the same forward pass per scene. Rule read on C1 + C2 pooled; each condition beside.",
        f"- back = position share with the address alone (keep_alf) / with the whole change (1 on the subset by "
        f"construction); left = position share without the address (no_alf). The rule is applied verbatim to these "
        f"raw shares (back >= {BACK}, left <= {LEFT}); the differences from the random parts are beside, not in the "
        "rule.",
        f"- The swap at s = {SWAP_S}: x8_write's writes h + s (mu_k - mu_j) at the bridge word of the original prompt, "
        "both k != j, on the routes test's C2 items (same generator, seed and eligibility; scene ids and bridge items "
        f"match all 300); the share the lookup follows (target). x8_write has no random write at s = {SWAP_S}; the "
        f"random write at s = {SWAP_RAND_S} (twice the norm) is beside. The swap has no clause in the rule.",
        f"- Cluster bootstrap over the bridge items ({n_boot} resamples, seed {X.BOOT_SEED}), paired across arms.",
        "", "## Result", "",
        f"**27B: {label}.** back = {fmt(s['subset']['pooled']['back'])}, left = {fmt(s['subset']['pooled']['left'])}.",
        f"9B beside (same subset logic on its own position-route scenes): the pattern "
        f"{'holds' if b['pattern'] else 'does not hold'}; back = {fmt(b['subset']['pooled']['back'])}, left = "
        f"{fmt(b['subset']['pooled']['left'])}.", "",
        "Position share on the subset (lookup), per arm:", "",
        "| model | scenes | n (C1 + C2) | whole | without the address | without a random part | random minus without "
        "the address | the address alone | a random part alone | alone minus random |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]  # fmt: skip
    for t in (SUBJECT, BESIDE):
        for part in ("pooled", *CONDS):
            c = blocks[t]["subset"][part]
            if c is None:
                lines.append(f"| {NAMES[t]} | {part} | 0 | - | - | - | - | - | - | - |")
                continue
            n = f"{c['n']} ({c['entities']} items)"
            sh = c["share"]
            lines.append(f"| {NAMES[t]} | {'C1 + C2' if part == 'pooled' else part} | {n} | {fmt(sh['whole'])} | "
                         f"{fmt(sh['no_alf'])} | {fmt(sh['no_alf_rand'])} | {fmt(c['removal_beyond_random'])} | "
                         f"{fmt(sh['keep_alf'])} | {fmt(sh['keep_alf_rand'])} | {fmt(c['alone_beyond_random'])} |")  # fmt: skip
    lines += ["", "Per condition, the rule's two inputs: " + "; ".join(
        f"{NAMES[t]} {c} back {fmt(blocks[t]['subset'][c]['back'])}, left {fmt(blocks[t]['subset'][c]['left'])} "
        f"(pattern {'holds' if pattern(blocks[t]['subset'][c]['back'][0], blocks[t]['subset'][c]['left'][0]) else 'does not hold'})"
        for t in (SUBJECT, BESIDE) for c in CONDS if blocks[t]["subset"][c]) + ".", ""]  # fmt: skip
    sb = s["subset"]["pooled"]["back"]
    lines += [f"Read beside the label (descriptive, not in the rule): the 27B's back CI [{sb[1]:.2f}, {sb[2]:.2f}] "
              f"{'contains' if sb[1] <= BACK <= sb[2] else 'excludes'} the bar {BACK}. Without a random part of the "
              "address's share, C1 keeps " + ", ".join(
                  f"{fmt(blocks[t]['subset']['C1']['share']['no_alf_rand'])} ({NAMES[t]})"
                  for t in (SUBJECT, BESIDE) if blocks[t]["subset"]["C1"]) +
              " of its position answers, so in C1 the removal clause does not separate the address from a random "
              "part of its share; in C2 the removal beyond random is " + ", ".join(
                  f"{fmt(blocks[t]['subset']['C2']['removal_beyond_random'])} ({NAMES[t]})"
                  for t in (SUBJECT, BESIDE) if blocks[t]["subset"]["C2"]) + ".", ""]  # fmt: skip
    lines += [f"The swap at s = {SWAP_S} (C2 scenes; lookup's share per write; 2 writes per scene):", "",
              "| model | scenes | writes | follows the swap (target) | stays (original) | third | random write at "
              f"s = {SWAP_RAND_S}: target |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in (SUBJECT, BESIDE):
        for part, text in (("subset", "position-route subset"), ("rest", "the other C2 scenes"), ("all", "all C2")):
            w = blocks[t]["swap"][part]
            if w is None or w["swap"] is None:
                continue
            sw, rd = w["swap"], w["swap_rand"]
            lines.append(f"| {NAMES[t]} | {text} (n {w['scenes']}; bridge slot j: "
                         f"{', '.join(f'{j}: {n}' for j, n in sorted(w['j'].items()))}) | {sw['n_writes']} | "
                         f"{fmt(sw['target'])} | {fmt(sw['original'])} | {fmt(sw['third'])} | "
                         f"{fmt(rd['target']) if rd else '-'} |")  # fmt: skip
    lines += ["", "Checks:"]
    for t in (SUBJECT, BESIDE):
        ck = blocks[t]["check"]
        lines.append(f"- {NAMES[t]}: the routes run {ck['run']} (its own forward pass on the same scenes) puts "
                     f"{ck['also_position_in_check']} of the {ck['subset_in_check']} subset scenes on the position "
                     f"route ({ck['check_position_scenes']} position scenes there in all); its position share without "
                     f"the address on the subset: {ck['no_alf_position_share_in_check']:.2f}.")  # fmt: skip
    if cross:
        lines.append(f"- Descriptive: the 27B's subset scenes read on the 9B (same scene id and bridge item; n "
                     f"{cross['n']}): whole {fmt(cross['share']['whole'])}, without the address "
                     f"{fmt(cross['share']['no_alf'])}, the address alone {fmt(cross['share']['keep_alf'])}.")  # fmt: skip
    lines += ["", "Figure: x53_subset27b.png. Status: UNVERIFIED (exploration day; nothing into the README)."]
    return lines


def figure(blocks: dict, path: Path) -> None:
    from scripts import story_style as S

    plt = S.setup()
    order = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand", "swap", "swap_rand")
    color = {"whole": S.COL["lookup"], "no_alf": S.MARK_COL["address"], "no_alf_rand": S.COL["control"],
             "keep_alf": S.MARK_COL["address"], "keep_alf_rand": S.COL["control"], "swap": S.MARK_COL["address"],
             "swap_rand": S.COL["control"]}  # fmt: skip
    hatch = {"swap": "//", "swap_rand": "//"}
    text = {**ARM_TEXT, "swap": f"{ARM_TEXT['swap']} (C2)", "swap_rand": f"{ARM_TEXT['swap_rand']} (C2)"}
    ys = -(np.arange(len(order)) + np.array([0, 0, 0, 0, 0, 0.6, 0.6]))
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 4.4), sharey=True)
    for ax, t in zip(axes, (SUBJECT, BESIDE), strict=True):
        blk = blocks[t]
        c = blk["subset"]["pooled"]
        sw = blk["swap"]["subset"]
        vals = [c["share"][a] for a in order[:5]]
        vals += [sw["swap"]["target"] if sw and sw["swap"] else [np.nan] * 3,
                 sw["swap_rand"]["target"] if sw and sw["swap_rand"] else [np.nan] * 3]  # fmt: skip
        for y, a, v in zip(ys, order, vals, strict=True):
            ax.barh(y, v[0], height=0.7, color=color[a], hatch=hatch.get(a, ""), edgecolor="white", lw=0.5)
            ax.errorbar(v[0], y, xerr=[[max(v[0] - v[1], 0)], [max(v[2] - v[0], 0)]], color="#333333", capsize=2.5,
                        lw=1)  # fmt: skip
            ax.text(min(v[2], 1.0) + 0.03, y, f"{v[0]:.2f}", ha="left", va="center", fontsize=S.FONT - 1)
        for y, bar in ((ys[1], LEFT), (ys[3], BACK)):
            ax.vlines(bar, y - 0.45, y + 0.45, color="#333333", lw=1.4, ls="--")
        ax.axhline((ys[4] + ys[5]) / 2, color="#d4d4d4", lw=0.8)
        ax.set_yticks(ys, [text[a] for a in order])
        ax.set_xlim(0, 1.18)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        label = LABEL[blk["pattern"]] if t == SUBJECT else f"9B's pattern {'holds' if blk['pattern'] else 'fails'}"
        ax.set_title(f"{NAMES[t]}: {label}\nn = {c['n']} scenes; swap {sw['scenes'] if sw else 0} C2 scenes",
                     fontsize=S.FONT, loc="left")  # fmt: skip
        ax.set_xlabel("share of lookups")
    S.title(
        fig,
        "53.5: the address on each model's position-route scenes",
        "Lookup by position under the whole change; dashed: the rule's bars (0.10, 0.25)",
    )
    S.fit(fig, fig.text(0.01, 0.005, "Swap rows: share following the written slot (no random write at "
                        f"s = {SWAP_S}). Whiskers: 95% cluster-bootstrap CIs over bridge items. UNVERIFIED.",
                        fontsize=8, color=S.COL["muted"]))  # fmt: skip
    fig.tight_layout(rect=(0, 0.03, 1, 0.9))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv: list[str] | None = None) -> Path:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    args = ap.parse_args(argv)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = OUT_ROOT / f"{EXP}-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    blocks = {t: model_block(t, args.n_boot) for t in (SUBJECT, BESIDE)}
    cross = on_other(blocks[SUBJECT], blocks[BESIDE], args.n_boot)
    (out / "verdict.md").write_text("\n".join(verdict_md(blocks, cross, args.n_boot, stamp)) + "\n")
    blob = {"exp": EXP, "test": "53.5", "written_utc": stamp, "rule": RULE, "bars": {"back": BACK, "left": LEFT},
            "label": LABEL[blocks[SUBJECT]["pattern"]], "bootstrap": {"n": args.n_boot, "seed": X.BOOT_SEED,
            "cluster": "bridge item"}, "status": "UNVERIFIED", "prediction": None,
            "models": {t: {k: v for k, v in b.items() if not k.startswith("_")} for t, b in blocks.items()},
            "subject_subset_on_9b": cross,
            "subset_scenes": {t: [list(k) for k in b["_keys"]] for t, b in blocks.items()}}  # fmt: skip
    (out / f"{EXP}.json").write_text(json.dumps(blob, indent=1) + "\n")
    figure(blocks, out / f"{EXP}.png")
    print("wrote", out, flush=True)
    return out


if __name__ == "__main__":
    main()
