"""x53_z1p_clean (batch 53, Dan 12:50, jobs/c3/batch53.yaml docs_1250 item 0; CPU, verification, no new forwards): Z1-P on
the 9B without the passages where the original bridge's true value stands in the lookup's passage as another entity's
value, Z1's rule verbatim on the rest, beside the full set.

Dan, verbatim: "CPU check first (verification): Z1-P on the 9B without the 60 passages where the bridge's true value
stands in the lookup's passage as another entity's value: rule verbatim on the remaining 140; report beside the
full-set number in the Z1 card, both ways."

Source: the stored run results/x50_zach/qwen35_9b_x52_z1p (L12; its full-set verdict results/x50_zach/
x52_z1p-20261029T081112Z). The excluded passages: the verify check "Z1-P: the true value is absent from the lookup's
passage" (review/verify_checks.json, scripts/verify_checks.zach_facts), recomputed here the same way
(bridge_jspace.review.items: word_in(the recall's (M) original answer = the bridge's true value, the lookup's (K)
original passage), a whole word, case-insensitive) over the run's 200 chosen passages; its count and the five ids the
check lists are asserted. A passage is one item key (set, scene) with both readers: K (the lookup) and M (the recall)
read their own passages but are one paired item, so excluding a passage drops both its K and its M rows (the gap is
the M minus K difference on the same draws). Z1's rule (x50_zach.RULE["z1p"] = Z1's, verbatim) and its computation
(x50_zach.layer_result: X0's excess per reader, the gap on paired cluster-bootstrap draws over the original bridge
entity, 10,000, seed 0) on the remaining passages; the full set recomputed the same way and checked against the stored
verdict. Descriptive verification; UNVERIFIED.

uv run python scripts/x53_z1p_clean.py            # CPU; writes results/x50_zach/x53_z1p_clean-<UTC>/
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x50_zach as Z

RUN = "qwen35_9b_x52_z1p"
STORED_VERDICT = "x52_z1p-20261029T081112Z"
VERIFY = pins.REPO_ROOT / "review" / "verify_checks.json"
CHECK = "Z1-P: the true value is absent from the lookup's passage"
DAN = ('"CPU check first (verification): Z1-P on the 9B without the 60 passages where the bridge\'s true value stands in '
       'the lookup\'s passage as another entity\'s value: rule verbatim on the remaining 140; report beside the full-set '
       'number in the Z1 card, both ways." (Dan 12:50, batch53.yaml docs_1250 item 0)')  # fmt: skip


def true_in_lookup_passage(case: dict) -> bool:
    """The verify check's test: the recall's (M) original answer, the bridge's true value, as a whole word in the
    lookup's (K) original passage (bridge_jspace.review.items.word_in)."""
    from bridge_jspace.review.items import word_in

    return word_in(case["readers"]["M"]["answer"], case["readers"]["K"]["context"])


def excluded_keys(run_dir: Path) -> tuple[list[tuple[str, str]], int]:
    """The run's chosen passages (gate.json order) whose lookup passage holds the bridge's true value, in that order, and
    the number chosen."""
    gate = json.loads((run_dir / "gate.json").read_text())
    chosen = [tuple(k) for k in gate["order"]]
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(run_dir / "cases.jsonl")}
    return [k for k in chosen if true_in_lookup_passage(cases[k])], len(chosen)


def verify_listed() -> tuple[int, list[str]]:
    """The verify check's count and the passage ids it lists (review/verify_checks.json, the 9B's Z1-P view)."""
    v = json.loads(VERIFY.read_text())["views"]["z1p"]["models"]["qwen3.5-9b"]
    chk = next(c for c in v["run_checks"] if c["check"] == CHECK)
    n = int(chk["detail"].split(" of ")[0])
    listed = chk["detail"].split(": ", 1)[1].strip("[]").replace("'", "").split(", ") if ": " in chk["detail"] else []
    return n, listed


def fmt(v) -> str:
    return (
        "-" if v is None or not isinstance(v[0], float) or math.isnan(v[0]) else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"
    )


def stage(n_boot: int = X.N_BOOT, run: str = RUN, out_root: Path | None = None) -> Path:
    run_dir = Z.RESULTS / run
    m = json.loads((run_dir / "manifest.json").read_text())
    assert m["model"]["target"] == "qwen3.5-9b", f"{run} is {m['model']['target']}'s"
    excl, n_chosen = excluded_keys(run_dir)
    n_verify, listed = verify_listed() if run == RUN else (len(excl), [])
    assert len(excl) == n_verify, f"{len(excl)} passages hold the true value here, the verify check says {n_verify}"
    ids = [f"{s}/{sc}" for s, sc in excl]
    assert ids[: len(listed)] == listed, f"the verify check lists {listed}, recomputed {ids[: len(listed)]}"
    rows = X.read_jsonl(run_dir / "outcomes.jsonl")
    drop = set(excl)
    out: dict = {"run": run, "dan": DAN, "rule": Z.RULE["z1p"], "as_computed": Z.AS_COMPUTED, "n_boot": n_boot,
                 "seed": X.BOOT_SEED, "excluded": ids, "chosen": n_chosen,
                 "how": "the run's chosen passages (gate.json order) whose lookup (K) original passage holds the recall's "
                        "(M) original answer, the bridge's true value, as a whole word, case-insensitive "
                        "(bridge_jspace.review.items.word_in; the verify check of review/verify_checks.json, recomputed "
                        "and its count and listed ids asserted); a passage is one paired item (K and M rows), so both "
                        "readers' rows of an excluded passage are dropped", "layers": {}}  # fmt: skip
    stored = json.loads((Z.RESULTS / STORED_VERDICT / "z1p.json").read_text()) if run == RUN else None
    for la in m["layers"]:
        rs = [r for r in rows if r["layer"] == la]
        full = Z.layer_result("z1p", rs, n_boot)
        clean = Z.layer_result("z1p", [r for r in rs if (r["set"], r["scene"]) not in drop], n_boot)
        rec: dict = {"full": full, "clean": clean}
        if stored is not None:
            s = stored["models"][0]["layer_results"][str(la)]
            rec["full_matches_stored"] = bool(s["verdict"] == full["verdict"] and s["n"] == full["n"] and all(
                math.isclose(a, b, abs_tol=1e-9) for a, b in zip(s["gap"], full["gap"], strict=True)))  # fmt: skip
        out["layers"][str(la)] = rec
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dest = (out_root or Z.RESULTS) / f"x53_z1p_clean-{stamp}"
    dest.mkdir(parents=True, exist_ok=False)
    (dest / "verdict.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    (dest / "excluded.json").write_text(json.dumps({"how": out["how"], "excluded": ids}, indent=1) + "\n")
    lines = ["# Z1-P on the 9B, without the passages whose lookup passage holds the bridge's true value (UNVERIFIED)", "",
             f"Dan, verbatim: {DAN}", "", f"Rule (Z1's, verbatim): {Z.RULE['z1p']}", "", f"As computed: {Z.AS_COMPUTED}",
             "", f"Excluded ({len(ids)} of {n_chosen} chosen passages): {out['how']}. Ids in excluded.json.", "",
             "| set | layer | passages (entities) | K (lookup) extra loss | M (recall) extra loss | gap M - K | verdict |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for la, rec in out["layers"].items():
        for name, lr in (("full", rec["full"]), (f"without the {len(ids)}", rec["clean"])):
            lines.append(f"| {name} | {la} | {lr['n']} ({lr['entities']}) | {fmt(lr['lookup']['excess'])} | "
                         f"{fmt(lr['recall']['excess'])} | {fmt(lr['gap'])} | **{lr['verdict']}** |")  # fmt: skip
        if "full_matches_stored" in rec:
            lines += ["", f"L{la}: the full set recomputed here matches the stored verdict {STORED_VERDICT} "
                          f"(verdict, n, gap): {rec['full_matches_stored']}."]  # fmt: skip
        for name, lr in (("full", rec["full"]), ("clean", rec["clean"])):
            o = lr["order"]
            lines.append(f"L{la} {name}: order fact-first {fmt(o['strata']['fact-first']['whole_switch'])} (n "
                         f"{o['strata']['fact-first']['n']}), fact-after {fmt(o['strata']['fact-after']['whole_switch'])} "
                         f"(n {o['strata']['fact-after']['n']}); replicates {o['replicates']}; X0's validity bar K "
                         f"{lr['lookup']['valid']}, M {lr['recall']['valid']}.")  # fmt: skip
    lines += ["", "Status: UNVERIFIED until a human adds it to VERIFIED.md."]
    (dest / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    print("wrote", dest, flush=True)
    return dest


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    stage(ap.parse_args().n_boot)


if __name__ == "__main__":
    main()
