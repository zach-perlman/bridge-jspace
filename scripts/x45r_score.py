"""45r's rule (jobs/c3/batch45.yaml, 45r; Q46.1 in predictions/2026-10-27_dan.md), scored by hand on the CPU.

Our side: the stored, fixed-in-advance Muse main test at L26 (gap 0.85 [0.68, 0.98], muse30b_x0_necessity; the spec's
as-computed (1)). Zach's side: his v2 knock-out on Muse over the band L23-29 (the rule's run). M - K per condition is
read from scripts/jsuite2_score.py's output, exactly as he scores it (start=all, items Muse gets right unedited, start R
left out, 1,000 draws). The J-specific excess = M - K (paper10) - M - K (unembed10), with a paired cluster bootstrap over
relation:bridge (both conditions on the same draws, 10,000, seed 0), the selection copied from jsuite2_score.main.
"Not needed" = M - K < 15 or excess <= 10; "carried, not needed" if our gap >= 0.3 and not needed, "carried and needed"
if our gap >= 0.3, M - K >= 15 and excess > 10. Point estimates decide; intervals beside them.

uv run python scripts/x45r_score.py     # results/x45r/score-<stamp>/{x45r.json, x45r.md}
"""

from __future__ import annotations

import collections
import json
import random
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RES = REPO / "results" / "ablate_v2"
DATA = REPO / "data" / "tasks_v2"
SET = "jsuite_v2_test_chat"
RULE_RUN = "muse30_jsuite_v2_test_chat_ko_cand2_L23-29_x45r_v1"
L26_RUN = "muse30_jsuite_v2_test_chat_ko_cand2_L26_x45r_v1"
BAND_RUN = "muse30_jsuite_v2_test_chat_ko_cand2_L36-42_pca_x45r_v1"
RECORD_RUN = "muse30_jsuite_v2_test_chat_ko_cand2_v1"  # Zach's record run at L36-42
OUR_GAP = (0.85, 0.68, 0.98)  # muse30b_x0_necessity at L26, the spec's as-computed (1)
NOT_NEEDED_MK, NOT_NEEDED_EXCESS, CARRIED = 15.0, 10.0, 0.3
N_BOOT, SEED = 10_000, 0


def scored(run: str) -> dict[str, dict]:
    """jsuite2_score's start=all cells of a run: condition -> {lossM, lossK, mk, ci}."""
    s = json.loads((RES / "jsuite2_score" / f"{run}.json").read_text())
    out = {}
    for key, cell in s["facts"].items():
        cond, _, sel = key.partition("/")
        if sel == "start=all":
            mk = cell["contrasts"]["M-K"]
            out[cond] = {"lossM": cell["loss"]["M"], "lossK": cell["loss"]["K"], "mk": mk["diff"], "ci": mk["ci"]}
    return out


def per_cluster(run: str, cond: str) -> dict[str, dict[str, list[int]]]:
    """cluster (relation:bridge) -> final (M / K) -> [correct], with jsuite2_score.main's selection."""
    items = {json.loads(x)["id"]: json.loads(x) for x in (DATA / SET / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(x) for x in (RES / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    out: dict = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        it = items[r["id"]]
        if r["condition"] != cond or (r["family"], r["id"]) not in ok or it["module"] != "facts" or it["start"] == "R":
            continue
        if it["final"] in ("M", "K"):
            out[f"{it['relation']}:{it['bridge']}"][it["final"]].append(int(r["correct"]))
    return out


def mk_of(cl: dict, pick: collections.Counter | None = None) -> float:
    def loss(f):
        tot = sum(sum(v[f]) * (pick[c] if pick else 1) for c, v in cl.items())
        n = sum(len(v[f]) * (pick[c] if pick else 1) for c, v in cl.items())
        return 100 * (1 - tot / n)

    return loss("M") - loss("K")


def excess_ci(run: str) -> tuple[float, float, float]:
    a, b = per_cluster(run, "paper10"), per_cluster(run, "unembed10")
    clusters = sorted(set(a) | set(b))
    rng = random.Random(SEED)
    point = mk_of(a) - mk_of(b)
    boots = []
    for _ in range(N_BOOT):
        pick = collections.Counter(rng.choice(clusters) for _ in clusters)
        boots.append(mk_of({c: a[c] for c in a if pick[c]}, pick) - mk_of({c: b[c] for c in b if pick[c]}, pick))
    boots.sort()
    return point, boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT) - 1]


def main() -> Path:
    rule = scored(RULE_RUN)
    mk, (ex, ex_lo, ex_hi) = rule["paper10"]["mk"], excess_ci(RULE_RUN)
    not_needed = mk < NOT_NEEDED_MK or ex <= NOT_NEEDED_EXCESS
    carried = OUR_GAP[0] >= CARRIED
    label = ("carried, not needed" if carried and not_needed else "carried and needed" if carried else "not carried")
    out = {"rule_run": RULE_RUN, "our_gap_L26": OUR_GAP, "his_L23_29": rule,
           "excess_L23_29": [round(ex, 1), round(ex_lo, 1), round(ex_hi, 1)], "not_needed": not_needed,
           "label": label, "q46_1": "(a)" if label == "carried, not needed" else "(b)",
           "descriptive": {"L26": scored(L26_RUN), "L36_42_size_matched": scored(BAND_RUN),
                           "L36_42_record": scored(RECORD_RUN)},
           "note": "opened 27 Oct ~17:55 at Dan's request, before Zach confirmed the use of his knock-out"}  # fmt: skip
    dest = REPO / "results" / "x45r" / f"score-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    dest.mkdir(parents=True)
    (dest / "x45r.json").write_text(json.dumps(out, indent=1) + "\n")
    row = lambda c, v: f"| {c} | {v['lossM']} | {v['lossK']} | {v['mk']:+.1f} [{v['ci'][0]}, {v['ci'][1]}] |"  # noqa: E731
    lines = ["# 45r: on Muse at mid depth, is the lens part needed where our test finds it carried? UNVERIFIED", "",
             f"Rule (fixed in advance; Q46.1): our gap at L26 {OUR_GAP[0]} [{OUR_GAP[1]}, {OUR_GAP[2]}] (carried if >= 0.3); "
             f"his knock-out over L23-29: not needed if M - K < 15 or J-specific excess (paper10 minus unembed10 M - K) "
             f"<= 10. Point estimates decide. Opened before Zach confirmed the use of his method (Dan's request).", "",
             f"**{label}** -> Q46.1 {out['q46_1']}: M - K {mk:+.1f} {rule['paper10']['ci']}, excess {ex:+.1f} "
             f"[{ex_lo:+.1f}, {ex_hi:+.1f}] (10,000 paired draws over relation:bridge, seed 0).", "",
             "| condition (L23-29) | M lost | K lost | M - K |", "|---|---|---|---|",
             *[row(c, v) for c, v in rule.items()], "",
             "Descriptive: L26 alone, and L36-42 (Zach's record run, plus the size-matched control run here):", "",
             "| run / condition | M lost | K lost | M - K |", "|---|---|---|---|",
             *[row(f"L26 {c}", v) for c, v in out["descriptive"]["L26"].items()],
             *[row(f"L36-42 record {c}", v) for c, v in out["descriptive"]["L36_42_record"].items()],
             *[row(f"L36-42 {c}", v) for c, v in out["descriptive"]["L36_42_size_matched"].items()]]  # fmt: skip
    (dest / "x45r.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return dest


if __name__ == "__main__":
    main()
