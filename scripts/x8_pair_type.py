"""x8_pair_type: does the address swap's "third" landing depend on how far apart the slots are? (POST HOC; Dan 30 Oct; CPU, saved x8_write rows.)

x8_write writes h + s (mu_k - mu_j) at the bridge word of the C2 scenes (j = the bridge item's locker slot, both k != j; s = 1, 2, 4 for the write, s = 1
and 4 for a random vector of the same size). Pair type: adjacent (|k - j| = 1) or far (|k - j| = 2). Class of the answer: target (slot k's), original
(slot j's), third (the other slot's), other. Lookup: the stored class (x8_write.classify). Recall, non-colliding scenes only (legs[k] != legs[j]): an
unchanged recall is "original"; a changed one is target (legs of slot k), third (legs of the third slot), else other (x8_write.recall_item's order;
when the third slot's legs equal the original's the third cannot be seen: such a recall is "original"); a second subset keeps only the scenes where the three
slots' legs all differ.

Per model, kind and dose: n, the class shares per pair type, 95% cluster-bootstrap intervals over the bridge entity (x0_necessity.resampled_rates,
seed 0; ratio of the resampled sums), and the gap third share (far) - third share (adjacent) with its interval.

Pre-set prediction (written to the manifest first): an ordinal address predicts third share (far) > third share (adjacent), largest at s = 1 and falling at
s = 4, and absent from the random arms. "Supported" only if far - adjacent excludes 0 (interval above 0) on at least 3 of 5 models at s = 1 or 2 and the
random arms show no such gap (no model's random far - adjacent interval is above 0, at s = 1 or 4). Otherwise: "third is generic disruption". The rule is
applied to the lookup; the recall is reported beside with the same rule.

uv run python scripts/x8_target_legs_check.py        # (the sibling script)
uv run python scripts/x8_pair_type.py                # writes results/x8_pair_type/<UTC>/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace.review import checks as RC  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x8_write as W  # noqa: E402

RUNS = {"qwen3.5-9b": "qwen35_9b_x8_write", "qwen3.6-27b": "x8_write_27b", "muse-glimmer-30b": "muse30b_x8_write",
        "nemotron-3.5-lightning": "nem35l_x52_write", "qwen3.5-122b-a10b": "qwen35_122b_x8_write_g75"}  # fmt: skip
CLASSES = ("target", "original", "third", "other")
PREDICTION = ("An ordinal address predicts third share (far) > third share (adjacent), largest at s = 1 and falling at s = 4, and absent from the random arms. "
              "'Supported' only if far - adjacent excludes 0 (interval above 0) on at least 3 of 5 models at s = 1 or 2 and the random arms show no such gap "
              "(no model's random far - adjacent interval above 0, at s = 1 or 4). Otherwise: 'third is generic disruption'. Applied to the lookup; the recall is reported beside.")  # fmt: skip


def interval(num: list[int], den: list[int], ents: list[str]) -> list[float]:
    boot = X.resampled_rates({"n": num, "d": den}, ents, X.N_BOOT, X.BOOT_SEED)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = boot["n"] / boot["d"]
    pt = sum(num) / sum(den) if sum(den) else float("nan")
    return [round(pt, 4), *(round(b, 4) for b in X.interval(r))]


def cells(rows: list[dict]) -> dict:
    """rows: dicts with pair ('adjacent'/'far'), cls, entity. Class shares per pair type, and the third-share gap."""
    ents = [r["entity"] for r in rows]
    out: dict = {"n": {t: sum(r["pair"] == t for r in rows) for t in ("adjacent", "far")}, "shares": {}}
    for t in ("adjacent", "far"):
        den = [int(r["pair"] == t) for r in rows]
        out["shares"][t] = {c: {"count": sum(int(r["pair"] == t and r["cls"] == c) for r in rows),
                                "share": interval([int(r["pair"] == t and r["cls"] == c) for r in rows], den, ents)} for c in CLASSES}  # fmt: skip
    den = {t: [int(r["pair"] == t) for r in rows] for t in ("adjacent", "far")}
    num = {t: [int(r["pair"] == t and r["cls"] == "third") for r in rows] for t in ("adjacent", "far")}
    boot = X.resampled_rates(
        {"nf": num["far"], "df": den["far"], "na": num["adjacent"], "da": den["adjacent"]}, ents, X.N_BOOT, X.BOOT_SEED
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        gap = boot["nf"] / boot["df"] - boot["na"] / boot["da"]
    pt = out["shares"]["far"]["third"]["share"][0] - out["shares"]["adjacent"]["third"]["share"][0]
    out["third_gap_far_minus_adjacent"] = [round(pt, 4), *(round(b, 4) for b in X.interval(gap))]
    return out


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "x8_pair_type" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "x8_pair_type", "post_hoc": True, "cpu": True, "runs": RUNS, "prediction": PREDICTION,
                                                   "script": "scripts/x8_pair_type.py", "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    legs = T.DOMAINS["animals"].values
    res: dict = {}
    for model, run in RUNS.items():
        cases = {
            c["scene"]: c
            for c in X.read_jsonl(REPO / "results/x6_routes" / W.ROUTES_OF[model] / "cases.jsonl")
            if c["condition"] == "C2"
        }
        look, rec_nc, rec_distinct = {}, {}, {}
        for r in X.read_jsonl(REPO / "results/x8_write" / run / "outcomes.jsonl"):
            if r["kind"] not in ("write", "random"):
                continue
            slots = W.slots_of(cases[r["scene"]]["context"])
            lg = [legs[s[0]] for s in slots]
            pair = "adjacent" if abs(r["k"] - r["j"]) == 1 else "far"
            key = (r["kind"], r["s"])
            if r["reader"] == X.LOOKUP:
                look.setdefault(key, []).append(
                    {
                        "pair": pair,
                        "cls": r["class"],
                        "entity": r["entity"],
                        "scene": r["scene"],
                        "j": r["j"],
                        "k": r["k"],
                    }
                )
            elif lg[r["k"]] != lg[r["j"]]:
                third = ({0, 1, 2} - {r["j"], r["k"]}).pop()
                if not r["changed"]:
                    cls = "original"
                else:
                    d = RC.piece(model, r["top"]).strip()
                    cls = "target" if d == str(lg[r["k"]]) else "third" if d == str(lg[third]) else "other"
                row = {"pair": pair, "cls": cls, "entity": r["entity"], "scene": r["scene"]}
                rec_nc.setdefault(key, []).append(row)
                if len({lg[0], lg[1], lg[2]}) == 3:
                    rec_distinct.setdefault(key, []).append(row)
        res[model] = {"run": run, "lookup": {f"{k}|{s:g}": cells(v) for (k, s), v in sorted(look.items())},
                      "recall_non_colliding": {f"{k}|{s:g}": cells(v) for (k, s), v in sorted(rec_nc.items())},
                      "recall_three_legs_distinct": {f"{k}|{s:g}": cells(v) for (k, s), v in sorted(rec_distinct.items())}}  # fmt: skip

    def verdict(which: str) -> dict:
        wr, rd = [], []
        for model, m in res.items():
            gaps = {k: m[which][k]["third_gap_far_minus_adjacent"] for k in m[which]}
            if any(gaps[f"write|{s}"][1] > 0 for s in (1, 2)):
                wr.append(model)
            if any(gaps[f"random|{s}"][1] > 0 for s in (1, 4)):
                rd.append(model)
        supported = len(wr) >= 3 and not rd
        return {"models_with_write_gap_above_0_at_s1_or_s2": wr, "models_with_random_gap_above_0": rd,
                "verdict": "supported" if supported else "third is generic disruption"}  # fmt: skip

    res["_verdict"] = {w: verdict(w) for w in ("lookup", "recall_non_colliding", "recall_three_legs_distinct")}
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    L = [
        "# The address swap by pair type: adjacent (|k-j| = 1) vs far (|k-j| = 2), post hoc\n",
        "Prediction (pre-set): " + PREDICTION + "\n",
        f"Verdicts: {json.dumps(res['_verdict'])}\n",
    ]
    f = lambda v: f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"  # noqa: E731
    for model, m in res.items():
        if model == "_verdict":
            continue
        for which in ("lookup", "recall_non_colliding", "recall_three_legs_distinct"):
            L.append(f"## {model}: {which}\n")
            L.append(
                "| kind, s | n adjacent / far | third share adjacent | third share far | far - adjacent | target adj / far | original adj / far | other adj / far |\n|---|---|---|---|---|---|---|---|"
            )
            for key, c in m[which].items():
                sh = c["shares"]

                def pair(cl, sh=sh):
                    return f"{sh['adjacent'][cl]['share'][0]:.3f} / {sh['far'][cl]['share'][0]:.3f}"

                L.append(
                    f"| {key} | {c['n']['adjacent']} / {c['n']['far']} | {f(sh['adjacent']['third']['share'])} | {f(sh['far']['third']['share'])} | {f(c['third_gap_far_minus_adjacent'])} | {pair('target')} | {pair('original')} | {pair('other')} |"
                )
            L.append("")
    (out / "tables.md").write_text("\n".join(L) + "\n")
    ex = [
        r
        for r in X.read_jsonl(REPO / "results/x8_write/nem35l_x52_write/outcomes.jsonl")
        if r["scene"] == "C2-0111" and r["kind"] == "write" and r["reader"] == X.LOOKUP
    ]
    (out / "example_C2_0111_lightning.json").write_text(json.dumps(ex, indent=1) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
