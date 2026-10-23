"""finding5_confirm: the pre-registered confirmation of finding 5 on fresh scenes (Dan, 2026-10-22, before the runs).

Finding 5 (README slide 4): with the donor prompt's last two tokens copied into the original prompt, the answer goes to
the original's statement at the same place when the donor asks its 1st or 2nd statement (an order label), and to the
original's statement about the donor's entity from the 3rd on (the bridge's identity). That split was chosen after the
pooled pre-registered test; this run tests it as a rule fixed in advance.

Items: memory -> prompt, the donor's last two tokens copied at one layer (pointer_swap, source dissoc, group last),
split by the place k of the donor's asked statement. Per item: position = the answer is the original's statement at k;
identity = the original's statement about the donor's entity. Shares are over all patched items of the split.
  A  1st and 2nd (k = 1, 2 pooled): position - identity has its 95% lower bound > 0
  B  3rd to the last (k = 3 .. N pooled; N = 5, finding 5's lists: 3rd-5th): identity - position >= 0 (point) and its
     95% lower bound >= -0.05
  verdict  confirms iff A and B; partly if one of them; fails if neither
  layer    --layer L, or with --layers the last of them where the donor's own digit ('value') has its Wilson upper bound
           < 0.10 (the fixed rule the other models' layers follow); decided before the split is read
Intervals: entity-cluster bootstrap (the original's queried entity resampled within its topic, 4,000 draws, seed 0).
Reported, not decisive: every k, per topic, named -> prompt.
Longer lists (generalised 2026-10-22 night, before any 8- or 12-statement run; the 5-statement verdicts are reproduced
byte for byte, tests/test_finding5_confirm.py): --sentences N names the list length; every selected item must have N
statements (asserted), so B pools exactly the 3rd to the Nth. --level LV keeps one level of a run with several
(pointer_v5: e8-digit and e8-word on the same scenes); the layer rule then reads that level's rows only ('value' is the
donor's own answer, a digit or a word).

uv run python scripts/finding5_confirm.py --run R (--layer L | --layers L1 L2 ...) [--level LV] [--sentences N]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import cluster_bootstrap, wilson

PS_RESULTS = pins.RESULTS_DIR / "pointer_swap"
OUT = pins.RESULTS_DIR / "finding5_confirm"
A_LO, B_POINT, B_LO, VALUE_UB = 0.0, 0.0, -0.05, 0.10
N_BOOT, SEED = 4000, 0
SENTENCES = 5  # finding 5's list length, the default


def diff(rows: list[dict], a: str, b: str) -> list[float]:
    """mean(1[role a] - 1[role b]) with its entity-cluster bootstrap interval (within topic); NaNs for no rows (a group
    the competence filter emptied, e.g. the few 1st / 2nd-sentence scenes of a 12-sentence set: judged not testable)."""
    if not rows:
        return [float("nan")] * 3
    vals = [float(r["role"] == a) - float(r["role"] == b) for r in rows]
    return list(cluster_bootstrap(vals, [r["_entity"] for r in rows], [r["domain"] for r in rows], n_boot=N_BOOT,
                                  seed=SEED))  # fmt: skip


def judge(first2: list[float], rest: list[float]) -> dict:
    if math.isnan(first2[0]) or math.isnan(rest[0]):  # a test with no items cannot pass or fail
        empty = [name for name, v in (("A (1st-2nd)", first2), ("B (3rd on)", rest)) if math.isnan(v[0])]
        return {"A": None, "B": None, "verdict": f"not testable (no items: {', '.join(empty)})"}
    a = first2[1] > A_LO
    b = rest[0] >= B_POINT and rest[1] >= B_LO
    return {"A": a, "B": b, "verdict": "confirms" if a and b else "partly" if a or b else "fails"}


def ordinal(k: int) -> str:
    return f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def select(rows: list[dict], items: dict[str, dict], level: str | None, sentences: int) -> list[dict]:
    """The dissoc rows at the last two tokens (of `level` if given), each with the 1-based place k of the donor's
    asked statement and the original's asked entity; asserts every selected item has `sentences` statements."""
    out = []
    for r in rows:
        if r["source"] != "dissoc" or r["group"] != "last" or (level is not None and r["level"] != level):
            continue
        it = items[r["name"]]
        n = len(it["entities"])
        assert n == sentences, f"{r['name']}: {n} statements, but --sentences {sentences}"
        r["_k"] = it["slots"]["position"] + 1
        r["_entity"] = f"{it['domain']}:{it['query']}"
        out.append(r)
    assert out, f"no dissoc rows at the last two tokens{f' of level {level}' if level else ''}"
    return out


def pick_layer(rows: list[dict], layers: list[int], family: str) -> tuple[int, dict]:
    """The last of `layers` where the donor's own answer ('value', `family`) has its Wilson upper bound < VALUE_UB."""
    value_by_layer = {}
    for la in layers:
        sel = [r for r in rows if r["family"] == family and str(r["layer"]) == str(la)]
        value_by_layer[la] = list(wilson(sum(r["role"] == "value" for r in sel), len(sel)))
    ok = [la for la in layers if value_by_layer[la][2] < VALUE_UB]
    assert ok, f"no layer of {layers} before the donor's digit arrives"
    return max(ok), value_by_layer


def confirm(rows: list[dict], layer: int, sentences: int = SENTENCES) -> dict[str, dict]:
    """Per family at `layer`: A (1st and 2nd), B (3rd to the `sentences`th), every k, per topic, the verdict."""
    families = {}
    for fam in sorted({r["family"] for r in rows}):
        sel = [r for r in rows if r["family"] == fam and str(r["layer"]) == str(layer)]
        first2 = [r for r in sel if r["_k"] <= 2]
        rest = [r for r in sel if r["_k"] >= 3]
        block = {"n": len(sel), "first2": {"n": len(first2), "position_minus_identity": diff(first2, "position", "identity")},
                 "rest": {"n": len(rest), "identity_minus_position": diff(rest, "identity", "position")},
                 "by_k": {k: dict(collections.Counter(r["role"] for r in sel if r["_k"] == k))
                          for k in range(1, sentences + 1)},
                 "by_topic": {}}  # fmt: skip
        for dom in sorted({r["domain"] for r in sel}):
            f2 = [r for r in first2 if r["domain"] == dom]
            rs = [r for r in rest if r["domain"] == dom]
            block["by_topic"][dom] = {"first2": [*diff(f2, "position", "identity"), len(f2)],
                                      "rest": [*diff(rs, "identity", "position"), len(rs)]}  # fmt: skip
        block.update(judge(block["first2"]["position_minus_identity"], block["rest"]["identity_minus_position"]))
        families[fam] = block
    return families


def report(out: dict, decisive: str, sentences: int) -> str:
    title = f"# finding5_confirm / {out['run']}, layer {out['layer']}"
    if "sentences" in out:
        title += f" ({out['level'] or 'every level'}, {sentences} statements)"
    lines = [title, ""]
    for fam, b in out["families"].items():
        f2, rs = b["first2"]["position_minus_identity"], b["rest"]["identity_minus_position"]
        tag = " (decisive)" if fam == decisive else " (reported)"
        lines += [f"**{fam}{tag}: {b['verdict']}** (A {b['A']}, B {b['B']}; n {b['n']})",
                  f"- 1st and 2nd: position - identity {100 * f2[0]:+.0f} [{100 * f2[1]:+.0f}, {100 * f2[2]:+.0f}] points (n {b['first2']['n']})",
                  f"- 3rd-{ordinal(sentences)}: identity - position {100 * rs[0]:+.0f} [{100 * rs[1]:+.0f}, {100 * rs[2]:+.0f}] points (n {b['rest']['n']})",
                  f"- by k: {json.dumps(b['by_k'])}", ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--layer", type=int)
    g.add_argument("--layers", type=int, nargs="+")
    ap.add_argument("--family", default="RL")
    ap.add_argument("--level", default=None, help="one level of the run (default: every row, as for one-level runs)")
    ap.add_argument("--sentences", type=int, default=SENTENCES, help="statements per list; B pools the 3rd to the last")
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new verdict folder")
    a = ap.parse_args(argv)
    assert a.sentences >= 3, "--sentences: B needs a 3rd statement"
    from scripts import pointer_swap as PS

    m = json.loads((PS_RESULTS / a.run / "manifest.json").read_text())
    items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
    rows = [json.loads(x) for x in (PS_RESULTS / a.run / "outcomes.jsonl").read_text().splitlines()]
    rows = select(rows, items, a.level, a.sentences)
    if a.layer is not None:
        layer, value_by_layer = a.layer, {}
    else:
        layer, value_by_layer = pick_layer(rows, a.layers, a.family)
    out: dict = {"run": a.run}
    if a.level is not None or a.sentences != SENTENCES:  # recorded when set (finding 5's own runs predate them)
        out |= {"level": a.level, "sentences": a.sentences}
    out |= {"layer": layer, "value_by_layer": value_by_layer, "families": confirm(rows, layer, a.sentences)}
    tag = f"_{a.level}" if a.level else ""
    d = Path(a.out) / f"{a.run}{tag}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    text = report(out, a.family, a.sentences)
    (d / "verdict.md").write_text(text)
    print(text, end="")
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
