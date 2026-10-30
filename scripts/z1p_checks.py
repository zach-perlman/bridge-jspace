"""z1p_checks: five CPU checks on the 9B's Z1-P run (Zach's made-up-fact passages, qwen35_9b_x52_z1p; POST HOC; Dan 30 Oct; report only).

C1  The class rule behind the blocked-beyond-random count is the answer's FIRST TOKEN (x50_zach.route: top == tok_b / tok_A; X.read_row's switched and
    role). The review card's narrative compared the decoded top token with the FULL answer word, so a first token ("Port" of "Portugal") read
    "another answer" while the arms table and the count said A. Counted: arm rows where the two disagree, before and after the display fix
    (bridge_jspace.review.page.answer_of now follows the count's rule and names the word the token starts).
C2  Items where the original and changed answers share a first token (tok_A == tok_b), per reader.
C3  The four "only the scene's words differ" rows (Mont Saint-Michel, Christ the Redeemer; two readers each): the extra differing token indices, decoded,
    whether they are inside the landmark name (the bridge / changed bridge), and the 9B numbers without those two scenes.
F4  Passages where the lookup's changed answer b equals the TRUE value of the original bridge (the recall's answer): count, and the lookup's and the
    recall's blocked-beyond-random and the gap without them, with intervals, beside the full set. Pre-set: if the lookup number moves by more than 0.05
    or its interval stops including 0, report it as a change to the claim; otherwise a caveat line.
F4b For every recall (PM) item: the recall's A and b (full word and first token) absent from the recall's own passage? Any where they appear.
F5  (CPU part) Items whose stored first token tok_A or tok_b has <= 2 characters (the GPU 4-token decode is not run here).

uv run python scripts/z1p_checks.py        # writes results/z1p_checks/<UTC>/
"""

from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace.review import checks as C  # noqa: E402
from bridge_jspace.review import items as I  # noqa: E402
from bridge_jspace.review import page as P  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x50_zach as Z  # noqa: E402

MODEL, RUN, VIEW = "qwen3.5-9b", "qwen35_9b_x52_z1p", "z1p"
RULE_F4 = ("if the lookup's blocked-beyond-random moves by more than 0.05 or its interval stops including 0, report it as a change to the claim; "
           "otherwise a caveat line")  # fmt: skip
FOUR = (
    "jsuite_v2_test_chat/j2:landmarks:P-L1-Mont Saint-Michel-0",
    "jsuite_v2nb_test_chat/j2:landmarks:P-L0-Christ the Redeemer-0",
)


def old_narrative(d: str, rd: dict) -> str:
    """The display before the fix: the decoded top token against the full answer word."""
    return "changed" if d == str(rd["cf_answer"]) else "original" if d == str(rd["answer"]) else "another"


def count_class(role: str) -> str:
    return {"b": "changed", "A": "original"}.get(role, "another")


def numbers(rows: list[dict], drop: set, n_boot: int) -> dict:
    r = Z.layer_result("z1p", [x for x in rows if (x["set"], x["scene"]) not in drop], n_boot)
    return {
        "n": r["n"],
        "lookup_excess": r["lookup"]["excess"],
        "recall_excess": r["recall"]["excess"],
        "gap": r["gap"],
        "verdict": r["verdict"],
    }


def split(scene: str) -> tuple[str, str]:
    s, _, sc = scene.partition("/")
    return s, sc


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "z1p_checks" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "z1p_checks", "post_hoc": True, "cpu": True, "model": MODEL, "run": RUN, "rule_F4": RULE_F4,
                                                   "gpu_part_F5": "not run: the 9B is not loaded on the pod", "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    items = [i for i in I.items(VIEW, MODEL) if i["case"]]
    by_scene: dict[str, dict] = collections.defaultdict(dict)
    for it in items:
        by_scene[it["scene"]][it["reader"]] = it
    res: dict = {"scenes": len(by_scene)}
    # ---- C1: the class rule and the display
    mism_before, mism_after, n_rows, examples = collections.Counter(), collections.Counter(), 0, []
    for it in items:
        rd = it["case"]["readers"][it["reader"]]
        for label, r in it["rows"][it["reader"]].items():
            if not r or "top" not in r:
                continue
            n_rows += 1
            d = C.top_text(MODEL, r["top"]).strip()
            want = count_class(r["role"])
            if old_narrative(d, rd) != want:
                mism_before[(it["reader"], label)] += 1
                if len(examples) < 12:
                    examples.append({"item": it["id"], "arm": label, "top_text": d, "count_rule": want, "old_narrative": old_narrative(d, rd), "answer": rd["answer"], "cf_answer": rd["cf_answer"]})  # fmt: skip
            _, what = P.answer_of(it, it["reader"], r)
            if what.split(" ")[0] != want:
                mism_after[(it["reader"], label)] += 1
    res["C1"] = {"rule": "first token: x50_zach.route / X.read_row (top == tok_b -> changed, == tok_A -> original), the count's switched and role",
                 "arm_rows_with_a_top_token": n_rows, "disagree_before": sum(mism_before.values()), "disagree_after_fix": sum(mism_after.values()),
                 "before_by_reader_arm": {f"{k[0]}|{k[1]}": v for k, v in mism_before.items()}, "examples": examples}  # fmt: skip
    # ---- C2: shared first token
    shared = []
    for scene, d in by_scene.items():
        for w, it in d.items():
            rd = it["case"]["readers"][w]
            if rd["tok_A"] == rd["tok_b"]:
                shared.append(
                    {
                        "scene": scene,
                        "reader": w,
                        "answer": rd["answer"],
                        "cf_answer": rd["cf_answer"],
                        "token": C.piece(MODEL, rd["tok_A"]),
                    }
                )
    res["C2"] = {"items_with_tok_A_equal_tok_b": len(shared), "list": shared}
    # ---- the numbers
    rows = X.read_jsonl(REPO / "results" / "x50_zach" / RUN / "outcomes.jsonl")
    n_boot = X.N_BOOT
    full = numbers(rows, set(), n_boot)
    res["full"] = full
    den = {}
    for r in rows:
        if r["layer"] == 12 and r["arm"] in ("none", "whole", "no_jpp", "no_jpp_rand"):
            den.setdefault(r["reader"], {}).setdefault(r["arm"], [0, 0])
            den[r["reader"]][r["arm"]][0] += int(r["switched"])
            den[r["reader"]][r["arm"]][1] += 1
    res["denominators"] = {"lookup (K)": den["K"], "recall (M)": den["M"], "format": "arm: [switched, rows]"}
    # ---- C3: the four rows
    four = {}
    for scene in FOUR:
        for w in ("PP", "PM"):
            it = by_scene[scene][w]
            c, rd = it["case"], it["case"]["readers"][w]
            diff = C.diff_positions(it)
            ca, cb = C.changed_words(c["context"], c["cf_context"])
            org, alt = rd["ids"]["org"], rd["ids"]["alt"]

            def inside(t: int, words: set[str]) -> bool:
                s = C._strip(C.piece(MODEL, t))
                return bool(s) and any(s in x for x in words)

            bad = [i for i in diff if not (inside(org[i], ca) and inside(alt[i], cb))]
            names = (c["bridge"], c["cf_bridge"])
            four[f"{scene}|{w}"] = {"check": C.check_diff(it)[1], "differing_positions": diff, "bridge": c["bridge"], "cf_bridge": c["cf_bridge"],
                                    "extra_positions": bad, "extra_tokens": [{"i": i, "org": C.piece(MODEL, org[i]), "alt": C.piece(MODEL, alt[i]),
                                                                              "context_org": C.piece(MODEL, 0) and "".join(C.piece(MODEL, t) for t in org[max(0, i - 4) : i + 3]),
                                                                              "inside_landmark_name": bool(any(C._strip(C.piece(MODEL, org[i])) in n or C._strip(C.piece(MODEL, alt[i])) in m for n in [names[0]] for m in [names[1]])),
                                                                              "org_in_changed_words": inside(org[i], ca), "alt_in_changed_words": inside(alt[i], cb)} for i in bad]}  # fmt: skip
    res["C3"] = {"rows": four, "without_the_two_scenes": numbers(rows, {split(s) for s in FOUR}, n_boot)}
    # ---- F4: b (lookup) equals the true value of the original bridge (the recall's answer)
    f4 = []
    for scene, d in by_scene.items():
        k, m = d["PP"]["case"]["readers"]["PP"], d["PM"]["case"]["readers"]["PM"]
        full_eq = str(k["cf_answer"]).casefold() == str(m["answer"]).casefold()
        tok_eq = k["tok_b"] == m["tok_A"]
        if full_eq or tok_eq:
            f4.append(
                {
                    "scene": scene,
                    "bridge": d["PP"]["case"]["bridge"],
                    "k_b": k["cf_answer"],
                    "m_true": m["answer"],
                    "full_word_equal": full_eq,
                    "first_token_equal": tok_eq,
                }
            )
    drop4 = {split(x["scene"]) for x in f4 if x["full_word_equal"]}
    wo = numbers(rows, drop4, n_boot)
    dl = wo["lookup_excess"][0] - full["lookup_excess"][0]
    res["F4"] = {"rule": RULE_F4, "items_full_word_equal": sum(x["full_word_equal"] for x in f4), "items_first_token_equal": sum(x["first_token_equal"] for x in f4),
                 "list": f4, "full": full, "without": wo, "lookup_moves_by": round(dl, 4),
                 "reading": ("change to the claim" if abs(dl) > 0.05 or not (wo["lookup_excess"][1] <= 0 <= wo["lookup_excess"][2]) else "caveat line")}  # fmt: skip
    # ---- F4b: the recall's A and b absent from the recall's own passage
    f4b, n_checked = [], 0
    for scene, d in by_scene.items():
        m = d["PM"]["case"]["readers"]["PM"]
        n_checked += 1
        for which, word, tokid in (("A", m["answer"], m["tok_A"]), ("b", m["cf_answer"], m["tok_b"])):
            for name, text in (("passage", m["context"]), ("changed passage", m["cf_context"])):
                if I.word_in(word, text):
                    f4b.append({"scene": scene, "which": which, "word": word, "where": name, "kind": "full word"})
            for name, ids in (("passage", m["ids"]["org"]), ("changed passage", m["ids"]["alt"])):
                if tokid in ids:
                    f4b.append(
                        {
                            "scene": scene,
                            "which": which,
                            "word": word,
                            "token": C.piece(MODEL, tokid),
                            "where": name,
                            "kind": "first token",
                        }
                    )
    drop4b = {split(x["scene"]) for x in f4b if x["kind"] == "full word"}
    res["F4b"] = {"recall_items": n_checked, "appearances": len(f4b), "items_with_a_full_word_in_the_recalls_passage": len(drop4b),
                  "without_those_items": numbers(rows, drop4b, n_boot), "list": f4b}  # fmt: skip
    # ---- F5 (CPU part): short first tokens
    short = []
    for scene, d in by_scene.items():
        for w, it in d.items():
            rd = it["case"]["readers"][w]
            for which, tid, word in (("A", rd["tok_A"], rd["answer"]), ("b", rd["tok_b"], rd["cf_answer"])):
                t = C.piece(MODEL, tid).strip()
                if len(t) <= 2:
                    short.append({"scene": scene, "reader": w, "which": which, "token": t, "word": word})
    res["F5"] = {"gpu_part": "not run (the 9B is not loaded on the pod)", "items_with_a_first_token_of_at_most_2_characters": len({(x["scene"], x["reader"]) for x in short}),
                 "tokens": len(short), "scenes": len({x["scene"] for x in short}), "list": short}  # fmt: skip
    (out / "tables.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
