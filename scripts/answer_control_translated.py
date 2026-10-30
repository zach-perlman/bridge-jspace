"""answer_control_translated: the numbers behind the answer-control figure's post hoc rows (POST HOC; Dan 30 Oct; CPU, saved runs).

Per model run (9B, 27B, Muse; Lightning and the 122B were not run), the recall's three arms of 51.12's answer control, each as the switches blocked beyond its
size-matched random part, (S_random - S_arm) / S_whole, with 95% cluster-bootstrap intervals over the bridge entity (x0_necessity.resampled_rates, seed 0):
the English answer directions (the run as it stands) and the answer directions in any language (single-token translations;
scripts/answer_arms_translated.py), and arm 2 with K random token directions kept instead of the answer directions, K = the item's English count and its
all-language count (scripts/answer_arms_krand.py), 5 draws averaged, against the same size-matched random part as arm 2.

uv run python scripts/answer_control_translated.py     # writes results/answer_control_translated/<UTC>/tables.json
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
from scripts import x0_necessity as X  # noqa: E402

RUNS = {  # model: (the 51.12 E1 run, translated-arms folder, K-random folder)
    "qwen3.5-9b": ("qwen35_9b_x51_12_e1_r2", "qwen3.5-9b/run_qwen3.5-9b", "qwen3.5-9b/krand"),
    "qwen3.6-27b": ("x51_12_e1_27b_r2", "qwen3.6-27b/run_qwen3.6-27b", "qwen3.6-27b/krand_b8"),
    "muse-glimmer-30b": ("muse30_x51_12_e1_r2", "muse-glimmer-30b/run2", "muse-glimmer-30b/krand"),
}  # fmt: skip
READER = "PM"


def arrays(path: Path, arms: list[str], keys: list[str]) -> dict[str, list[float]]:
    got: dict = {}
    for r in X.read_jsonl(path):
        if r["reader"] == READER:
            got.setdefault((r["key"], r["arm"].split("#")[0]), []).append(r["sw"])
    return {a: [float(np.mean(got[(k, a)])) for k in keys] for a in arms}


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "answer_control_translated" / stamp
    out.mkdir(parents=True, exist_ok=False)
    res: dict = {"post_hoc": True, "reader": "recall (PM)", "models": {}}
    for model, (run, tdir, kdir) in RUNS.items():
        cases = X.read_jsonl(REPO / "results" / "x51_answer" / run / "cases.jsonl")
        keys = [c["key"] for c in cases]
        ents = [c["entity"] for c in cases]
        t = REPO / "runs" / "answer_arms_translated" / tdir
        en = arrays(
            t / "outcomes_english.jsonl",
            ["whole", "no_jpp", "no_jpp_rand", "no_jpp_A", "no_jpp_A_rand", "no_A", "no_A_rand"],
            keys,
        )
        al = arrays(t / "outcomes_all_languages.jsonl", ["no_jpp_A", "no_jpp_A_rand", "no_A", "no_A_rand"], keys)
        kr = arrays(REPO / "runs" / "answer_arms_krand" / kdir / "outcomes.jsonl", ["r_en", "r_all"], keys)
        arms = {"w": en["whole"], "a1": en["no_jpp"], "a1r": en["no_jpp_rand"], "a2e": en["no_jpp_A"], "a2er": en["no_jpp_A_rand"], "a3e": en["no_A"], "a3er": en["no_A_rand"],
                "a2a": al["no_jpp_A"], "a2ar": al["no_jpp_A_rand"], "a3a": al["no_A"], "a3ar": al["no_A_rand"], "k_en": kr["r_en"], "k_all": kr["r_all"]}  # fmt: skip
        rr = X.resampled_rates(arms, ents, X.N_BOOT, X.BOOT_SEED)

        def extra(arm: str, twin: str, rr=rr, arms=arms) -> list[float]:
            d = X.dependence(rr["w"], rr[arm]) - X.dependence(rr["w"], rr[twin])
            pt = float(
                X.dependence(np.mean(arms["w"]), np.mean(arms[arm]))
                - X.dependence(np.mean(arms["w"]), np.mean(arms[twin]))
            )
            return [round(pt, 4), *(round(v, 4) for v in X.interval(d))]

        res["models"][model] = {"run": run, "n": len(keys), "whole_switches": float(sum(arms["w"])), "extra": {
            "arm1_without_the_lens_part": extra("a1", "a1r"),
            "arm2_english": extra("a2e", "a2er"), "arm2_any_language": extra("a2a", "a2ar"),
            "arm2_K_random_english_count": extra("k_en", "a2er"), "arm2_K_random_any_language_count": extra("k_all", "a2ar"),
            "arm3_english": extra("a3e", "a3er"), "arm3_any_language": extra("a3a", "a3ar")},
            "sources": {"translated": str(t.relative_to(REPO)), "krand": f"runs/answer_arms_krand/{kdir}"}}  # fmt: skip
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    lines = ["# Answer control, recall: switches blocked beyond a size-matched random part (post hoc; answer in any language; 9B, 27B, Muse)", "",
             "| model | arm | value [95% interval] |", "|---|---|---|"]
    for m, v in res["models"].items():
        for k, x in v["extra"].items():
            lines.append(f"| {m} | {k.replace('_', ' ')} | {x[0]:+.3f} [{x[1]:.3f}, {x[2]:.3f}] |")
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    print(out)
    for m, v in res["models"].items():
        print(m, {k: x[0] for k, x in v["extra"].items()})
    return out


if __name__ == "__main__":
    main()
