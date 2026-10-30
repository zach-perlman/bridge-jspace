"""x51_10_other_answers: at the last token (51.10, view f), how often does each write move the reader's answer away from A to "other", and how many of those
answers are a locker digit of the scene (task confusion)? (POST HOC; Dan 30 Oct; CPU, saved arms, report only.)

Per model and reader (the recall PM decisive, the lookup PP beside), over the view's items whose unedited answer is A (the reader is right without a change):
for each arm at the last token (P3) at the reader's read peak - the lens swap, its random control, its rotated control, the J++ part and its random part at
gain 1 and 2, the whole-state patch - the share of items whose answer role is "other" (not A, not the swapped-in answer b), with 95% cluster-bootstrap
intervals over the bridge entity (x0_necessity.resampled_rates, seed 0), and how many of the "other" answers are a digit that is some locker's number in the
scene's context ("The locker of X is N."). Flag (Dan: tell before changing anything else): the lens swap moves away from A more than both its controls with
intervals not overlapping.

uv run python scripts/x51_10_other_answers.py        # writes results/x51_10_other_answers/<UTC>/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace.review import checks as C  # noqa: E402
from bridge_jspace.review import items as I  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402

VIEW = "last_token"
ARMS = [
    "lens swap",
    "its random control",
    "its rotated control",
    "J++ part, gain 1",
    "random part, gain 1",
    "J++ part, gain 2",
    "random part, gain 2",
    "whole-state patch",
]
MODELS = ["qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning"]


def ci(values: list[int], ents: list[str]) -> list[float]:
    boot = X.resampled_rates({"x": values}, ents, X.N_BOOT, X.BOOT_SEED)["x"]
    return [round(sum(values) / len(values), 4) if values else float("nan"), *(round(b, 4) for b in X.interval(boot))]


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "x51_10_other_answers" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "x51_10_other_answers", "post_hoc": True, "cpu": True, "view": VIEW, "arms": ARMS, "written_utc": stamp,
                                                   "flag": "the lens swap moves away from A more than both its controls with intervals not overlapping"}, indent=2) + "\n")  # fmt: skip
    res: dict = {}
    for model in MODELS:
        items = [i for i in I.items(VIEW, model) if i["case"]]
        res[model] = {}
        for w in ("PM", "PP"):
            mine = [
                i
                for i in items
                if i["reader"] == w and i["rows"][w].get("unedited") and i["rows"][w]["unedited"]["role"] == "A"
            ]
            ents = [i["case"]["entity"] for i in mine]
            cell = {"n_unedited_A": len(mine), "arms": {}}
            for arm in ARMS:
                rows = [i["rows"][w].get(arm) for i in mine]
                oth = [int(bool(r) and r["role"] == "other") for r in rows]
                bb = [int(bool(r) and r["role"] == "b") for r in rows]
                lock = []
                for i, r in zip(mine, rows, strict=True):
                    if r and r["role"] == "other":
                        digits = {
                            int(d) for d in __import__("re").findall(r"The locker of \w+ is (\d)", i["case"]["context"])
                        }
                        d = C.piece(model, r["top"]).strip()
                        lock.append(
                            {
                                "scene": i["scene"],
                                "answer": d,
                                "is_locker_digit": d.isdigit() and int(d) in digits,
                                "is_digit": d.isdigit(),
                            }
                        )
                cell["arms"][arm] = {"other": ci(oth, ents), "other_count": sum(oth), "switched_to_b": ci(bb, ents), "other_is_locker_digit": sum(x["is_locker_digit"] for x in lock),
                                     "other_is_a_digit": sum(x["is_digit"] for x in lock), "other_answers": [x["answer"] for x in lock][:12]}  # fmt: skip
            sw = cell["arms"]["lens swap"]["other"]
            flag = all(
                sw[0] > cell["arms"][c]["other"][0] and sw[1] > cell["arms"][c]["other"][2]
                for c in ("its random control", "its rotated control")
            )
            cell["flag_swap_above_both_controls_non_overlapping"] = bool(flag)
            res[model][w] = cell
    (out / "tables.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    L = ["# 51.10 (view f): the answer moved from A to other, by arm (post hoc, CPU)\n"]
    f = lambda v: f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"  # noqa: E731
    for model, d in res.items():
        for w, cell in d.items():
            L.append(
                f"## {model} {w} (items with unedited = A: {cell['n_unedited_A']}); flag: {cell['flag_swap_above_both_controls_non_overlapping']}\n"
            )
            L.append("| arm | other | count | locker digit | any digit | to b |\n|---|---|---|---|---|---|")
            for arm, a in cell["arms"].items():
                L.append(
                    f"| {arm} | {f(a['other'])} | {a['other_count']} | {a['other_is_locker_digit']} | {a['other_is_a_digit']} | {f(a['switched_to_b'])} |"
                )
            L.append("")
    (out / "tables.md").write_text("\n".join(L) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
