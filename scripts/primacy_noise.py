"""primacy_noise (D2 control, Dan, 2026-10-22): is the first-sentence bias of blocked lookups the model's general way of
guessing, or specific to blocking the read?

Background (UNVERIFIED; README slide 3): with the answer's statement hidden from the last tokens in every attention
layer, Qwen3.6-27B's wrong answers that are another digit of the list come from statements 1-5 as 128 / 56 / 35 / 25 /
19, against 59 / 51 / 51 / 51 / 51 under a uniform choice among each scene's 4 other statements (d2_v4_late_read).

Design. The same items (pointer_v4 main, memory -> prompt, the first 100 eligible scenes per topic, attn_knockout's
case builder and gate). Instead of blocking, damage the last tokens' read without any positional structure: at every
layer of the read band (the last quarter of the depth: 48-63 on the 27B) add, at the last tokens (the template after
the question and the read position), a random direction with norm sigma x that position's unedited residual norm,
sigma in SIGMAS; one generator per item. Read: the top token: right, another digit of the list (its statement's place
by where the digit sits in the prompt), or off the list.

Decision rule (fixed 2026-10-22 before the run):
  sigma*   the sigma whose accuracy is nearest the blocking's on the same items (recomputed from the blocking run's rows;
           ties: the smaller sigma), chosen on accuracy alone
  R1       over the items whose answer at sigma* is another digit of the list: observed / expected answers at the 1st
           statement (expected: uniform over each item's 4 other statements), scene bootstrap 95% interval
  verdict  'generic' (the bias is how the model guesses anyway) iff R1's lower bound >= 1.5; 'specific to blocking'
           iff R1's upper bound < 1.5; else inconclusive; fewer than 50 such answers: not testable at sigma*
  reported, not decisive: every sigma; the 5th statement's ratio (blocking: 19 / 51); the blocking run's own R1 with
           the same bootstrap; off-list shares
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import attn_knockout as AK
from scripts import early_push as EP
from scripts.exp04_brew_parts import AddRows

EXP = "primacy_noise"
RESULTS = pins.RESULTS_DIR / EXP
SIGMAS = (0.05, 0.1, 0.2, 0.4, 0.8)
SEED, N_BOOT, MIN_WRONG, GENERIC = 0, 4000, 50, 1.5


def classify(top: int, case: dict) -> tuple[str, int | None]:
    """right / list (with the 1-based place of the digit's statement) / off."""
    toks = [case["tok_A"], *case["conf_toks"]]
    order = sorted(toks, key=lambda t: case["ids"].index(t))
    if top == case["tok_A"]:
        return "right", order.index(top) + 1
    if top in order:
        return "list", order.index(top) + 1
    return "off", None


def ratios(items: list[tuple[int, int, int]], n_slots: int = 5) -> dict[int, float]:
    """items: (scene index, asked place, chosen place) of list-wrong answers -> observed / expected per place."""
    obs = collections.Counter(c for _, _, c in items)
    exp: dict[int, float] = collections.defaultdict(float)  # expected counts are fractional
    for _, asked, _ in items:
        for j in range(1, n_slots + 1):
            if j != asked:
                exp[j] += 1 / (n_slots - 1)
    return {j: obs[j] / exp[j] if exp[j] else float("nan") for j in range(1, n_slots + 1)}


def boot_ratio(items: list[tuple[int, int, int]], place: int = 1) -> list[float]:
    point = ratios(items)[place]
    if not items:
        return [point, float("nan"), float("nan")]
    rng = np.random.default_rng(SEED)
    scenes = sorted({s for s, _, _ in items})
    by: dict[int, list] = collections.defaultdict(list)
    for it in items:
        by[it[0]].append(it)
    vals = []
    for _ in range(N_BOOT):
        pick = rng.choice(scenes, size=len(scenes), replace=True)
        vals.append(ratios([it for s in pick for it in by[s]])[place])
    lo, hi = np.nanpercentile(vals, [2.5, 97.5])
    return [point, float(lo), float(hi)]


def decide(acc: dict[float, float], wrong: dict[float, list], blocked_acc: float) -> dict:
    star = min(acc, key=lambda s: (abs(acc[s] - blocked_acc), s))
    items = wrong[star]
    r1 = boot_ratio(items, 1)
    if len(items) < MIN_WRONG:
        verdict = "not testable at sigma*"
    elif r1[1] >= GENERIC:
        verdict = "generic: the model guesses the 1st statement anyway"
    elif r1[2] < GENERIC:
        verdict = "specific to blocking"
    else:
        verdict = "inconclusive"
    return {"sigma_star": star, "n_list_wrong": len(items), "R1": r1, "R5": boot_ratio(items, 5), "verdict": verdict}


@torch.no_grad()
def stage_run(name: str, why: str, n: int, competence: str, blocking_run: str) -> None:
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress

    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "manifest.json").exists(), f"{out} exists; runs are written once"
    (out / "manifest.json").write_text(json.dumps({"exp": EXP, "run": name, "why": why, "model": pins.model_pin(), "switches": switches(),
        "n_per_topic": n, "competence": competence, "blocking_run": blocking_run, "sigmas": SIGMAS, "seed": SEED,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "design": __doc__}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    # the blocking run's families, so that the gate and the scene pairing pick the same scenes; memory -> prompt only
    cases, _ = AK.build_pointer_cases(tok, "pointer_v4", ["RL", "DL", "RR"], None, n, "map", competence)
    cases = [c for c in cases if c["family"] == "RL"]
    n_layers = len(model.layers)
    band = list(range(n_layers * 3 // 4, n_layers))
    rows = []
    for k, c in enumerate(progress(cases, desc="items")):
        ids = torch.tensor([c["ids"]], device="cuda")
        pos = c["dests"]["final"]
        logits, rec = EP.forward_rows(model, ids, [{}], tuple(band))
        gen = torch.Generator(device="cuda").manual_seed(SEED + 1_000_003 * k)
        edits = []
        for s in SIGMAS:
            e = {}
            for la in band:
                h = rec[la][0][pos]
                r = torch.randn(h.shape, device="cuda", generator=gen)
                e[la] = AddRows(torch.nn.functional.normalize(r, dim=-1) * (s * h.norm(dim=-1, keepdim=True)), pos)
            edits.append(e)
        lg, _ = EP.forward_rows(model, ids, edits)
        for tag, row in [("none", logits[0]), *zip(SIGMAS, lg, strict=True)]:
            kind, place = classify(int(row.argmax()), c)
            rows.append({"id": c["id"], "scene": c["scene"], "domain": c["domain"], "sigma": tag, "class": kind,
                         "place": place, "asked": classify(c["tok_A"], c)[1]})  # fmt: skip
    with open(out / "rows.jsonl", "w") as fh:
        fh.writelines(json.dumps(r) + "\n" for r in rows)
    stage_analyze(name)


def blocked_accuracy(run: str) -> tuple[float, list[tuple[int, int, int]], set[str]]:
    d = pins.RESULTS_DIR / "attn_knockout" / run
    cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
    rows = [json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()]
    ok = {r["id"] for r in rows if r["family"] == "RL" and r["source"] == "none" and r["correct"]}
    sel = [r for r in rows if r["family"] == "RL" and r["id"] in ok and r["source"] == "lookup" and r["dest"] == "final"
           and r["layers"] == "attn" and r.get("mode", "value") == "value"]  # fmt: skip
    scene_ix = {s: i for i, s in enumerate(sorted({cases[r["id"]]["scene"] for r in sel}))}
    wrong = []
    for r in sel:
        kind, place = classify(r["top"], cases[r["id"]])
        if kind == "list":
            wrong.append(
                (scene_ix[cases[r["id"]]["scene"]], classify(cases[r["id"]]["tok_A"], cases[r["id"]])[1], place)
            )
    return sum(r["top"] == cases[r["id"]]["tok_A"] for r in sel) / len(sel), wrong, ok


def stage_analyze(name: str) -> None:
    out = RESULTS / name
    m = json.loads((out / "manifest.json").read_text())
    rows = [json.loads(x) for x in (out / "rows.jsonl").read_text().splitlines()]
    blocked_acc, blocked_wrong, _ = blocked_accuracy(m["blocking_run"])
    right_unedited = {r["id"] for r in rows if r["sigma"] == "none" and r["class"] == "right"}
    scene_ix = {s: i for i, s in enumerate(sorted({r["scene"] for r in rows}))}
    acc, wrong, shares = {}, {}, {}
    for s in m["sigmas"]:
        sel = [r for r in rows if r["sigma"] == s and r["id"] in right_unedited]
        acc[s] = sum(r["class"] == "right" for r in sel) / len(sel)
        wrong[s] = [(scene_ix[r["scene"]], r["asked"], r["place"]) for r in sel if r["class"] == "list"]
        shares[s] = {k: v / len(sel) for k, v in collections.Counter(r["class"] for r in sel).items()}
    dec = decide(acc, wrong, blocked_acc)
    summary = {"run": name, "decision": dec, "blocking": {"run": m["blocking_run"], "accuracy": blocked_acc,
               "R1": boot_ratio(blocked_wrong, 1), "R5": boot_ratio(blocked_wrong, 5), "n_list_wrong": len(blocked_wrong)},
               "by_sigma": {str(s): {"accuracy": acc[s], "shares": shares[s], "ratios": ratios(wrong[s]),
                                     "n_list_wrong": len(wrong[s])} for s in m["sigmas"]},
               "n_items": len(right_unedited)}  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    lines = [f"# {EXP} / {name}", "", f"**Verdict:** {dec['verdict']} (sigma* {dec['sigma_star']}, "
             f"{dec['n_list_wrong']} list-wrong answers)", "",
             f"- noise R1 (1st statement, observed / expected): {dec['R1'][0]:.2f} [{dec['R1'][1]:.2f}, {dec['R1'][2]:.2f}]; "
             f"R5 {dec['R5'][0]:.2f} [{dec['R5'][1]:.2f}, {dec['R5'][2]:.2f}]",
             f"- blocking ({m['blocking_run']}, accuracy {100 * blocked_acc:.0f}%): R1 {summary['blocking']['R1'][0]:.2f} "
             f"[{summary['blocking']['R1'][1]:.2f}, {summary['blocking']['R1'][2]:.2f}]", "",
             "| sigma | right | list | off | R1 | R5 | n list-wrong |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for s in m["sigmas"]:
        b = summary["by_sigma"][str(s)]
        lines.append(f"| {s} | {100 * b['accuracy']:.0f}% | {100 * b['shares'].get('list', 0):.0f}% | "
                     f"{100 * b['shares'].get('off', 0):.0f}% | {b['ratios'][1]:.2f} | {b['ratios'][5]:.2f} | "
                     f"{b['n_list_wrong']} |")  # fmt: skip
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--competence", default="d3v4_competence_27b")
    ap.add_argument("--blocking-run", default="d2_v4_late_read")
    a = ap.parse_args()
    if a.stage == "run":
        assert a.why, "run needs --why"
        stage_run(a.name, a.why, a.n, a.competence, a.blocking_run)
    else:
        stage_analyze(a.name)
