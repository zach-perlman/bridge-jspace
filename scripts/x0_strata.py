"""x0_strata (descriptive, added after data; Dan's generalization plan step 1, 24 Oct): an X0 run's lookup and recall
cells at one layer (word, J++ k = 25) split by scene features. Writes results/x0_necessity/<run>/strata-<UTC>/
{strata.md, strata.json}; never touches the run's files.

Strata: upstream change (the other changed pick comes before the asked one: yes / no); domain; the asked person's pick
sentence's place among the pick sentences (1st / 2nd / 3rd); whether the locker sentence of the org bridge, and of the
alt bridge, comes before or after the asked pick sentence; each reader's confidence (Dan's plan step 5, 25 Oct ~23:00:
its unpatched p_org, the 'none' arm, in terciles over the run's scenes at the layer). Per stratum: n, switched by the
whole edit, S_whole, Jdep, Rdep, excess (cluster bootstrap over entities, as X0) and the label; strata with fewer than
30 switched are flagged.

uv run python scripts/x0_strata.py --name x0_necessity_27b_chat --layer 32
uv run python scripts/x0_strata.py --name x0_necessity_27b_chat --layer 32 --features "recall's confidence"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from scripts import x0_necessity as X

NOTE = "Descriptive, added after data; not part of X0's rule."
PICK = re.compile(r"\b([A-Z][a-z]+) picked (?:the )?([\w-]+)\.")


def features(case: dict) -> dict[str, str]:
    """The scene features of one X0 case (chat rendering) for stratifying."""
    ctx = case["context"]
    q = case["readers"][X.LOOKUP]["question"]
    asked = re.search(r"([A-Z][a-z]+)'s pick", q).group(1)  # type: ignore[union-attr]
    sents = [s if s.endswith(".") else s + "." for s in ctx.split(". ")]
    picks = [i for i, s in enumerate(sents) if PICK.search(s)]
    mine = next(i for i in picks if sents[i].startswith(f"{asked} picked"))

    def locker(entity: str) -> str:
        i = next((i for i, s in enumerate(sents) if s.startswith("The locker of") and re.search(rf"\b{entity}\b", s)),
                 None)  # fmt: skip
        return "none" if i is None else ("before" if i < mine else "after")

    return {"upstream": "yes" if case["upstream"] else "no", "domain": case["domain"],
            "asked pick place": ["1st", "2nd", "3rd", "4th", "5th"][picks.index(mine)],
            "org locker vs asked pick": locker(case["bridge"]), "alt locker vs asked pick": locker(case["cf_bridge"])}  # fmt: skip


CONFIDENCE = {"lookup's confidence": X.LOOKUP, "recall's confidence": X.RECALL}
FEATURES = (
    "upstream",
    "domain",
    "asked pick place",
    "org locker vs asked pick",
    "alt locker vs asked pick",
    *CONFIDENCE,
)


def confidence(rows: list[dict]) -> tuple[dict[str, dict[str, str]], dict[str, list[float]]]:
    """Per scene, each reader's unpatched p_org (the 'none' arm) as its tercile over the scenes (1 low / 2 mid / 3
    high), and the tercile cut points."""
    p = {(r["scene"], r["reader"]): r["p_org"] for r in rows if r["arm"] == "none"}
    feat: dict[str, dict[str, str]] = {}
    cuts = {}
    for name, w in CONFIDENCE.items():
        vals = {s: v for (s, ww), v in p.items() if ww == w}
        lo, hi = (float(q) for q in np.quantile(list(vals.values()), [1 / 3, 2 / 3]))
        cuts[name] = [lo, hi]
        for s, v in vals.items():
            feat.setdefault(s, {})[name] = "1 low" if v < lo else "2 mid" if v < hi else "3 high"
    return feat, cuts


def readout_lines(readout: list[dict], feat: dict, features: list[str]) -> list[str]:
    """The digit check (c) per stratum: in the org and the alt run, the J++ readout's rank of the org and the alt
    answer digit among the 10 digits at the bridge's word (mean, and the share ranked first)."""
    lines = ["## Digit check (c): the J++ readout of the answer digits at the bridge's word", "",
             "| feature | value | reader | run | n | org digit: mean rank, share 1st | alt digit: mean rank, share 1st |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for key in features:
        for value in sorted({f[key] for f in feat.values()}):
            for w in X.READERS:
                for run in ("org", "alt"):
                    rs = [r for r in readout if r["reader"] == w and r["run"] == run and feat[r["scene"]][key] == value]
                    if not rs:
                        continue
                    o, b = [r["rank_org_answer"] for r in rs], [r["rank_alt_answer"] for r in rs]
                    lines.append(f"| {key} | {value} | {'lookup' if w == X.LOOKUP else 'recall'} | {run} | {len(rs)} | "
                                 f"{sum(o) / len(o):.2f}, {sum(x == 1 for x in o) / len(o):.2f} | "
                                 f"{sum(b) / len(b):.2f}, {sum(x == 1 for x in b) / len(b):.2f} |")  # fmt: skip
    return [*lines, ""]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--all-dicts", action="store_true", help="every dictionary, k and fit, not only J++ k = 25")
    ap.add_argument("--features", nargs="+", default=list(FEATURES), choices=list(FEATURES))
    a = ap.parse_args()
    src = X.RESULTS / a.name
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == a.layer]
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    conf, cuts = confidence(rows)
    feat = {
        s: {**features(cases[s]), **conf.get(s, dict.fromkeys(CONFIDENCE, "none"))} for s in {r["scene"] for r in rows}
    }
    lines = [f"# X0 strata: {a.name}, layer {a.layer}, the bridge's word, J++ k = 25", "",
             f"{NOTE} Bootstrap over the org bridge entity, {a.n_boot} resamples, seed {X.BOOT_SEED}. "
             "⚠ = fewer than 30 items switched by the whole edit (the cell is 'can't tell'). UNVERIFIED.", ""]  # fmt: skip
    blob: dict = {"run": a.name, "layer": a.layer, "note": NOTE, "confidence_cuts": cuts, "strata": []}
    for key in a.features:
        lines += [f"## {key}", ""]
        if key in CONFIDENCE:
            lines += [
                f"The reader's unpatched p_org in terciles; cut points {cuts[key][0]:.3f} and {cuts[key][1]:.3f}.",
                "",
            ]
        lines += ["| value | reader | dict | k | fit | n | switched | S_whole | Jdep | Rdep | excess | label |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for value in sorted({f[key] for f in feat.values()}):
            cells = X.cells_of([r for r in rows if feat[r["scene"]][key] == value], a.n_boot)
            keys = sorted(k for k in cells if a.all_dicts or k[3:] == X.MAIN)
            for k in sorted(keys, key=lambda k: (k[2] != X.LOOKUP, k[3] != "jpp", k[3], k[4], k[5])):
                c, w = cells[k], k[2]
                flag = " ⚠" if c["switched_whole"] < X.VALID_N else ""
                lines.append(f"| {value} | {'lookup' if w == X.LOOKUP else 'recall'} | {k[3]} | {k[4]} | {k[5]} | {c['n']} | "
                             f"{c['switched_whole']}{flag} | {X.fmt3(c['S_whole'])} | {X.fmt3(c['Jdep'])} | "
                             f"{X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
                blob["strata"].append({"feature": key, "value": value, "reader": w, "dict": k[3], "k": k[4],
                                       "omp": k[5], **c})  # fmt: skip
        lines.append("")
    readout = [r for r in X.read_jsonl(src / "readout.jsonl") if r["rendering"] == "chat" and r["layer"] == a.layer]
    if readout:
        lines += readout_lines(readout, feat, a.features)
    out = src / f"strata-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "strata.md").write_text("\n".join(lines) + "\n")
    (out / "strata.json").write_text(json.dumps(blob, indent=1) + "\n")
    print(out)


if __name__ == "__main__":
    main()
