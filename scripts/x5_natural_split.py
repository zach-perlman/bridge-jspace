"""x5_natural split (Dan, 25 Oct plan B2; descriptive, after the data, CPU only): a natural-passage run's J++ extra loss
per reader, split by whether the lookup answer's fact sentence (the sentence naming the bridge and its passage value)
comes before the bridge's mention (the binding sentence, the one the swap changes); also by both fact sentences (the
original's and the new bridge's) as in B1. Writes <run>/split-<stamp>/split.{json,md}. With --examples, also N random
passages (seed 0) to a Markdown file: the prompt, the swap, both answers, and each reader's answer per arm.

uv run python scripts/x5_natural_split.py --run x5_natural_27b --examples docs/natural_examples.md
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

RESULTS = pins.RESULTS_DIR / "x5_natural"
SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
ARMS = (("none", "original prompt, no patch"), ("whole", "whole change"), ("no_part", "without J++"),
        ("no_rand", "without a random part"))  # fmt: skip


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SPLIT.split(text) if s.strip()]


def has(sentence: str, word: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(word)}(?!\w)", sentence) is not None


def placement(case: dict) -> dict[str, str]:
    """Where the original's and the new bridge's fact sentences sit against the binding sentence."""
    org, alt = sentences(case["context"]), sentences(case["cf_context"])
    assert len(org) == len(alt), case["scene"]
    bind = next(i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b)
    rd = case["readers"][X.LOOKUP]

    def where(entity: str, value: str) -> str:
        i = next((i for i, s in enumerate(org) if i != bind and has(s, entity) and has(s, value)), None)
        return "not found" if i is None else ("before" if i < bind else "after")

    return {"original": where(case["bridge"], rd["answer"]), "new": where(case["cf_bridge"], rd["cf_answer"])}


def group_of(p: dict[str, str]) -> str:
    if p["original"] != "before":
        return (
            f"the original's fact sentence {p['original']} the bridge's mention"
            if p["original"] == "after"
            else "not found"
        )
    return "both fact sentences before" if p["new"] == "before" else "only the original's before"


PARTS = {"jpp": ("jpp", X.K_MAIN, "signed"), "alf": ("alf", 4, "signed")}  # alf: the pointer directions (T)


def cells(rows: list[dict], scenes: set[str], n_boot: int, part: str = "jpp") -> dict[str, dict]:
    mine = [r for r in rows if r["scene"] in scenes and r["dict"] in (PARTS[part][0], "-")]
    return {k[2]: c for k, c in X.cells_of(mine, n_boot).items() if k[3:] == PARTS[part]}


def examples(path: Path, run: str, cases: dict, rows: list[dict], n: int) -> None:
    by = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    scenes = sorted({r["scene"] for r in rows})
    pick = random.Random(0).sample(scenes, min(n, len(scenes)))
    out = [f"# Natural passages: {len(pick)} random examples ({run})", "",
           f"Drawn with seed 0 from the {len(scenes)} eligible scenes of results/x5_natural/{run} by "
           "scripts/x5_natural_split.py. The swapped prompt changes only the bridge in the binding sentence. Both "
           "readers read the same patched passage at the layer fixed in advance; the patch is added at the bridge's "
           "word. Answers are the read (the top first token among the relation's answer words). Unverified.", ""]  # fmt: skip
    for k, s in enumerate(pick, 1):
        c = cases[s]
        org, alt = sentences(c["context"]), sentences(c["cf_context"])
        bind = next(i for i, (a, b) in enumerate(zip(org, alt, strict=True)) if a != b)
        out += [f"## {k}. {s} ({c['relation']}, {c['genre']})", "", "Original passage:", "",
                *[f"> {line}" if line else ">" for line in c["context"].split("\n")], "",
                f"The swap: in \"{org[bind]}\" the bridge **{c['bridge']}** becomes **{c['cf_bridge']}** "
                f"(\"{alt[bind]}\").", "",
                "| reader | question | original answer | swapped answer | " + " | ".join(name for _, name in ARMS) + " |",
                "|---|---|---|---|" + "---|" * len(ARMS)]  # fmt: skip
        for w, name in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
            rd = c["readers"][w]
            tops = []
            for arm, _ in ARMS:
                r = by.get((s, w, arm))
                tops.append("–" if r is None else f"{r['top']}{' (switched)' if r['switched'] else ''}")
            out.append(f"| {name} | {rd['question']} | {rd['answer']} | {rd['cf_answer']} | " + " | ".join(tops) + " |")
        out.append("")
    path.write_text("\n".join(out) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--examples", type=Path, default=None)
    ap.add_argument("--n-examples", type=int, default=10)
    ap.add_argument("--part", choices=sorted(PARTS), default="jpp", help="the removed part (alf: the pointer, T)")
    a = ap.parse_args()
    src = RESULTS / a.run
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    done = {r["scene"] for r in rows if r["arm"] == "whole"}
    place = {s: placement(cases[s]) for s in done}
    groups = {s: group_of(place[s]) for s in done}
    two = {s: "before" if place[s]["original"] == "before" else place[s]["original"] for s in done}
    out = src / f"split-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    fmt = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# {a.run}: {'J++' if a.part == 'jpp' else 'the pointer directions'}: extra loss by where the answer's fact sentence sits (descriptive, after the data)", "",
             f"Cluster bootstrap over bridge entities ({a.n_boot} resamples). UNVERIFIED.", "",
             "| split | group | n | lookup switches (whole change) | lookup extra loss | recall switches | recall extra loss |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    table = []
    for split, lab in (("all", {s: "all" for s in done}), ("original's fact sentence vs the bridge's mention", two),
                       ("both fact sentences", groups)):  # fmt: skip
        for g in sorted(set(lab.values())):
            scenes = {s for s in done if lab[s] == g}
            c = cells(rows, scenes, a.n_boot, a.part)
            table.append({"split": split, "group": g, "n": len(scenes),
                          **{w: {k: c[w][k] for k in ("excess", "Jdep", "Rdep", "S_whole", "switched_whole")} for w in c}})  # fmt: skip
            lk, rc = c[X.LOOKUP], c[X.RECALL]
            lines.append(f"| {split} | {g} | {len(scenes)} | {lk['switched_whole']} | {fmt(lk['excess'])} | "
                         f"{rc['switched_whole']} | {fmt(rc['excess'])} |")  # fmt: skip
    lines += ["", "Extra loss is a share of the whole change's switches; where the lookup switches only a few times, its "
              "interval is wide and can leave [-1, 1]."]  # fmt: skip
    blob = {"run": a.run, "n_boot": a.n_boot, "rows": table, "placement": place}
    (out / "split.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "split.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if a.examples:
        examples(a.examples, a.run, cases, rows, a.n_examples)
        print("wrote", a.examples)


if __name__ == "__main__":
    main()
