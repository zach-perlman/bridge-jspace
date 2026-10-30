"""sink_decision: the attention-sink diagnostic's verdict, by the rule in docs/breadth/prereg_sink_1021.md (Zach, 2026-10-21,
written before Gemma's test-set C1 was opened). Reads Gemma's held-out ctrl_v8 run with `paper10_nosink` and
`paper10_nosink_rot` at layers 30-38, 40-48, 48-56:
- ARTIFACT if at one or more windows P->P and M->P each keep >= 80%, every word's rotated control keeps >= 90%, and the
  memory-final words' mean loss exceeds the lookup-final words' by >= 30 points;
- NOT ARTIFACT if P->P and M->P are both below 50% at all three windows;
- MIXED otherwise.
Writes results/ablate_v2/sink_decision/<RUN>.json and .md, and the protocol for every later C1 run to MARKER ("nosink"
for ARTIFACT, else "paper10"). Also tabulates the descriptive companions if present (plain-text loss, dose, the 27B).

python scripts/sink_decision.py GEMMA_DIAG_RUN [--textloss RUN] [--dose RUN] [--qwen RUN] [--marker PATH]
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

RES = pins.RESULTS_DIR / "ablate_v2"
WORDS = ("PP", "MP", "PM", "MM")
WINDOWS = ("L30-38", "L40-48", "L48-56")


def acc_table(run: str, conds: tuple[str, ...]) -> dict:
    rows = [json.loads(x) for x in (RES / run / "rows.jsonl").read_text().splitlines()]
    base = {(r["family"], r["id"]): r["correct"] for r in rows if r["condition"] == "none" and r["kind"] == "clean"}
    out: dict = {}
    for r in rows:
        if r["condition"] in conds and r["kind"] == "clean":
            out.setdefault(r["band"], {}).setdefault(r["condition"], {}).setdefault(r["family"], []).append(
                (int(base[(r["family"], r["id"])]), int(r["correct"]))
            )
    return {b: {c: {w: {"acc": statistics.mean(x for _, x in v), "unedited": statistics.mean(u for u, _ in v), "n": len(v)}
                    for w, v in cw.items()} for c, cw in bc.items()} for b, bc in out.items()}  # fmt: skip


def verdict(t: dict) -> tuple[str, dict]:
    per = {}
    for b in WINDOWS:
        k, kr = t.get(b, {}).get("paper10_nosink", {}), t.get(b, {}).get("paper10_nosink_rot", {})
        if not all(w in k and w in kr for w in WORDS):
            per[b] = None
            continue
        loss = {w: k[w]["unedited"] - k[w]["acc"] for w in WORDS}
        gap = (loss["PM"] + loss["MM"]) / 2 - (loss["PP"] + loss["MP"]) / 2
        per[b] = {"lookup_acc": {w: k[w]["acc"] for w in ("PP", "MP")}, "control_min": min(kr[w]["acc"] for w in WORDS),
                  "gap": gap, "pass": k["PP"]["acc"] >= 0.80 and k["MP"]["acc"] >= 0.80
                  and min(kr[w]["acc"] for w in WORDS) >= 0.90 and gap >= 0.30}  # fmt: skip
    done = [v for v in per.values() if v is not None]
    if any(v["pass"] for v in done):
        return "ARTIFACT", per
    if len(done) == len(WINDOWS) and all(v["lookup_acc"]["PP"] < 0.5 and v["lookup_acc"]["MP"] < 0.5 for v in done):
        return "NOT ARTIFACT", per
    return "MIXED", per


def main(a) -> None:
    t = acc_table(a.diag, ("paper10_nosink", "paper10_nosink_rot"))
    v, per = verdict(t)
    out = {"diag_run": a.diag, "verdict": v, "per_window": per, "protocol": "nosink" if v == "ARTIFACT" else "paper10",
           "rule": __doc__.split("\n\n")[0]}  # fmt: skip
    lines = [f"# Attention-sink diagnostic: {v} (rule fixed in docs/breadth/prereg_sink_1021.md)", "",
             "Gemma 4 31B-it, held-out ctrl_v8, knock-out with sink positions left unedited (accuracy %):", "",
             "| window | condition | " + " | ".join(WORDS) + " |", "|---|---|" + "---|" * len(WORDS)]  # fmt: skip
    for b in WINDOWS:
        for c in ("paper10_nosink", "paper10_nosink_rot"):
            cw = t.get(b, {}).get(c, {})
            lines.append(
                f"| {b} | {c} | " + " | ".join(f"{100 * cw[w]['acc']:.0f}" if w in cw else "-" for w in WORDS) + " |"
            )
    lines += ["", "Per window: " + json.dumps({b: None if p is None else {"P->P": round(100 * p["lookup_acc"]["PP"]),
              "M->P": round(100 * p["lookup_acc"]["MP"]), "gap": round(100 * p["gap"]), "control min": round(100 * p["control_min"]),
              "pass": p["pass"]} for b, p in per.items()})]  # fmt: skip
    summ = json.loads((RES / a.diag / "summary.json").read_text()).get("sink_positions", {})
    if summ:
        lines += ["", "Sink positions left unedited (share of positions): " + ", ".join(
            f"{k} {100 * v['skipped'] / max(v['positions'], 1):.1f}%" for k, v in summ.items())]  # fmt: skip
    for label, run in (("27B, ctrl_v8 (descriptive)", a.qwen), ("Gemma dose, layers 30-38 (descriptive)", a.dose)):
        if run and (RES / run / "rows.jsonl").exists():
            conds = tuple(json.loads((RES / run / "manifest.json").read_text())["conditions"])
            tt = acc_table(run, conds)
            lines += [
                "",
                f"## {label}: {run}",
                "",
                "| band | condition | " + " | ".join(WORDS) + " |",
                "|---|---|" + "---|" * len(WORDS),
            ]
            for b, bc in tt.items():
                for c, cw in bc.items():
                    lines.append(
                        f"| {b} | {c} | "
                        + " | ".join(f"{100 * cw[w]['acc']:.0f}" if w in cw else "-" for w in WORDS)
                        + " |"
                    )
            out[label] = tt
    if a.textloss and (pins.RESULTS_DIR / "removal_textloss" / a.textloss / "summary.json").exists():
        nll = json.loads((pins.RESULTS_DIR / "removal_textloss" / a.textloss / "summary.json").read_text())["mean_nll"]
        out["textloss"] = nll
        lines += ["", f"## Gemma plain-text loss, layers 30-38 ({a.textloss}; nats per token, descriptive)", "",
                  ", ".join(f"{k} {v:.2f}" for k, v in nll.items())]  # fmt: skip
    (RES / "sink_decision").mkdir(exist_ok=True)
    (RES / "sink_decision" / f"{a.diag}.json").write_text(json.dumps(out, indent=2) + "\n")
    (RES / "sink_decision" / f"{a.diag}.md").write_text("\n".join(lines) + "\n")
    if a.marker:
        Path(a.marker).write_text(out["protocol"] + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("diag")
    ap.add_argument("--textloss")
    ap.add_argument("--dose")
    ap.add_argument("--qwen")
    ap.add_argument("--marker")
    main(ap.parse_args())
