"""x0_strata (descriptive, added after data; Dan's generalization plan step 1, 24 Oct): an X0 run's lookup and recall
cells at one layer (word, J++ k = 25) split by scene features. Writes results/x0_necessity/<run>/strata-<UTC>/
{strata.md, strata.json}; never touches the run's files.

Strata: upstream change (the other changed pick comes before the asked one: yes / no); domain; the asked person's pick
sentence's place among the pick sentences (1st / 2nd / 3rd); whether the locker sentence of the org bridge, and of the
alt bridge, comes before or after the asked pick sentence. Per stratum: n, switched by the whole edit, S_whole, Jdep,
Rdep, excess (cluster bootstrap over entities, as X0) and the label; strata with fewer than 30 switched are flagged.

uv run python scripts/x0_strata.py --name x0_necessity_27b_chat --layer 32
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    src = X.RESULTS / a.name
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == a.layer]
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    feat = {s: features(cases[s]) for s in {r["scene"] for r in rows}}
    lines = [f"# X0 strata: {a.name}, layer {a.layer}, the bridge's word, J++ k = 25", "",
             f"{NOTE} Bootstrap over the org bridge entity, {a.n_boot} resamples, seed {X.BOOT_SEED}. "
             "⚠ = fewer than 30 items switched by the whole edit (the cell is 'can't tell'). UNVERIFIED.", ""]  # fmt: skip
    blob: dict = {"run": a.name, "layer": a.layer, "note": NOTE, "strata": []}
    for key in ("upstream", "domain", "asked pick place", "org locker vs asked pick", "alt locker vs asked pick"):
        lines += [f"## {key}", "", "| value | reader | n | switched | S_whole | Jdep | Rdep | excess | label |",
                  "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for value in sorted({f[key] for f in feat.values()}):
            cells = X.cells_of([r for r in rows if feat[r["scene"]][key] == value], a.n_boot)
            for w in X.READERS:
                c = cells.get(("chat", a.layer, w, *X.MAIN))
                if c is None:
                    continue
                flag = " ⚠" if c["switched_whole"] < X.VALID_N else ""
                lines.append(f"| {value} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | {c['switched_whole']}{flag} "
                             f"| {X.fmt3(c['S_whole'])} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | "
                             f"{X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
                blob["strata"].append({"feature": key, "value": value, "reader": w, **c})
        lines.append("")
    out = src / f"strata-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "strata.md").write_text("\n".join(lines) + "\n")
    (out / "strata.json").write_text(json.dumps(blob, indent=1) + "\n")
    print(out)


if __name__ == "__main__":
    main()
