"""absent_entity (Dan's B4, 2026-10-23): finding 5's patch with a donor that asks about an entity the original's list
does not contain (Qwen3.6-27B, layer 50).

Finding 5: two prompts list the same entities in a different order; the donor prompt's last two tokens are patched into
the original at one layer, and the answer (each listed answer a different digit) shows what the patch pointed to: the
same place (an order label) when the donor asks its 1st or 2nd statement, the bridge's identity from the 3rd on. Here
the donor's list has a new entity x at its asked place k_d, in place of the entity it asked before, and the donor asks
about x. x is in no statement of the original, so the identity route has nothing to point to: an order label predicts
the original's statement at k_d, a fallback its 1st statement.

Donor (absent_donor; tokenizer-free, deterministic per scene): pointer_v4's dissoc donor of the same scene (its order,
digits and wording) with x in place of its asked entity at k_d. x is drawn from the topic's entity pool (split.json)
among the entities not in the original's list whose cue has the token length of the original's asked entity's cue (so
the memory -> prompt prompts stay token-aligned), with random.Random(f"absent:{scene}"), so both families of a scene
get the same x. The donor's answer is its digit at k_d (finding 5's 'value', absent from the original's digits).

Outcomes of a patched read (classify): order (the original's digit at k_d), fallback (the original's 1st statement's
digit), unchanged (the original's answer), donor (the donor's own digit), other_digit, other (no digit). Where two of
them are the same digit the outcome names both: k_d = 1 gives 'order=fallback', an original asking its 1st statement
gives 'fallback=unchanged'.

Decision rule (the agent's proposal for Dan's B4, fixed before any run; jobs/d3/d3_absent_entity_27b.yaml repeats it):
memory -> prompt, the donor's last two tokens patched at layer 50 (pointer_swap --donor absent: source dissoc, group
last).
  items     the run's scenes whose original and absent-entity donor are both read right unedited (the original:
            pointer_v4 seed3's competence run and the run's unedited read; the donor: the run's donor_unedited check)
  decisive  k_d = 2..5 and an original not asking its 1st statement: order, fallback, unchanged and donor are then four
            distinct digits. k_d = 1 (order = fallback) and originals asking their 1st statement (fallback =
            unchanged) are reported, not tested.
  D         over the decisive items, mean(1[order] - 1[fallback]) with the entity-cluster bootstrap 95% interval
            (finding5_confirm.diff: the original's asked entity resampled within its topic, 4,000 draws, seed 0)
  control   the random push of the same size (pointer_swap's rand: a seeded random direction with the patch's
            per-position norm, added at the same tokens and layer) on the same items: D_rand, the same way
  verdict   order iff D's lower bound > 0 and > D_rand's upper bound; fallback iff D's upper bound < 0 and < D_rand's
            lower bound; otherwise neither; not testable without decisive items or without random-push rows
  reported  every outcome's share per k_d (1-5) and per topic, D per k_d (2-5) and per topic, named -> prompt with the
            same rule, the same-entity control's change rate, the donor's and the original's unedited reads

uv run python scripts/absent_entity.py --run R [--layer 50] [--family RL]   (CPU; a new results/absent_entity/ folder)
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import finding5_confirm as F
from scripts import pointer_v4 as PV4

OUT = pins.RESULTS_DIR / "absent_entity"
LAYER, FAMILY = 50, "RL"
# prediction key -> outcome name (the prediction keys are pointer_swap's, plus 'first': the original's 1st statement)
OUTCOME = {"position": "order", "first": "fallback", "none": "unchanged", "value": "donor"}
OUTCOMES = ("order", "fallback", "unchanged", "donor", "other_digit", "other")


def rule_text() -> str:
    """The decision rule as the docstring states it (recorded in the run's manifest)."""
    return (__doc__ or "").split("Decision rule")[1].split("\nuv run")[0].strip()


def candidates(item: dict, split: dict[str, Any]) -> list[str]:
    """The topic's entities not in the original's list whose cue has the asked entity's cue token length."""
    dom = item["domain"]
    cue_len = split["domains"][dom]["cue_tokens"]
    return sorted(e for e in split["domains"][dom]["pool"]
                  if e not in item["entities"] and cue_len[e] == cue_len[item["query"]])  # fmt: skip


def with_absent(items: dict[str, list[dict]], split: dict[str, Any] | None = None) -> tuple[dict, dict[str, int]]:
    """The items of scenes that have an absent entity (candidates), before sampling, and the dropped scenes per topic
    (an asked entity whose cue length only the listed entities share)."""
    split = split or PV4.load_split()
    assert split, "no data/pointer_v4/split.json"
    bad = {(it["domain"], it["scene"]) for its in items.values() for it in its if not candidates(it, split)}
    kept = {k: [it for it in its if (it["domain"], it["scene"]) not in bad] for k, its in items.items()}
    return kept, dict(collections.Counter(d for d, _ in bad))


def absent_donor(item: dict, split: dict[str, Any]) -> dict:
    """The item with its dissoc donor rebuilt around an entity absent from the original's list (the docstring's
    Donor). The original prompt, the other sources and the slots are kept; the donor records 'absent' and the entity it
    replaced."""
    assert item["family"] in ("RL", "DL"), f"{item['id']}: lookups only"
    dom, d, k = item["domain"], item["sources"]["dissoc"], item["slots"]["position"]
    assert d["entities"][k] == d["query"], f"{item['id']}: the donor's asked entity is not at its slot"
    free = candidates(item, split)
    assert free, f"{item['id']}: no absent entity with the asked entity's cue length"
    x = random.Random(f"absent:{item['scene']}").choice(free)
    order, digits = list(d["entities"]), list(d["digits"])
    order[k] = x
    t, u = item["templates"]["statement"], item["templates"]["question"]
    st = PV4.statements(dom, t, order, digits)
    target = PV4.name_of if item["family"] == "DL" else PV4.cue_of
    answer = str(digits[k])
    preds = {"none": item["answer"], "identity": "-", "position": str(item["digits"][k]),
             "first": str(item["digits"][0]), "value": answer}  # fmt: skip
    out = copy.deepcopy(item)
    out["sources"]["dissoc"] = {"context": " ".join(st), "statements": st,
                                "question": PV4.SPEC[dom]["lookups"][u].format(x=target(dom, x)), "answer": answer,
                                "entities": order, "digits": digits, "query": x, "query_slot": k, "predictions": preds,
                                "absent": True, "replaced": d["query"]}  # fmt: skip
    out["slots"] = {**item["slots"], "identity": None}  # nothing in the original is about x
    return out


def absent_cases(cases: list[dict], split: dict[str, Any] | None = None) -> list[dict]:
    split = split or PV4.load_split()
    assert split, "no data/pointer_v4/split.json"
    return [absent_donor(c, split) for c in cases]


def donor_record(item: dict) -> dict:
    """What the run's donors.jsonl keeps per item: the donor prompt and its predictions, for a human to check."""
    d = item["sources"]["dissoc"]
    return {"id": item["id"], "k_d": item["slots"]["position"] + 1, "asked_slot": item["slots"]["query"] + 1,
            "absent_entity": d["query"], "replaced": d["replaced"], "context": d["context"], "question": d["question"],
            "answer": d["answer"], "predictions": d["predictions"]}  # fmt: skip


def classify(top: str, preds: dict[str, str]) -> str:
    """The outcome of a read's top token (docstring's Outcomes); coinciding outcomes joined by '='."""
    t = top.strip()
    if not (len(t) == 1 and t.isdigit()):
        return "other"
    hits = [OUTCOME[h] for h in ("position", "first", "none", "value") if preds.get(h) == t]
    return "=".join(hits) if hits else "other_digit"


def decisive(item: dict) -> bool:
    """k_d >= 2 and the original not asking its 1st statement: the four predicted digits are distinct."""
    return item["slots"]["position"] > 0 and item["slots"]["query"] > 0


def eligible(rows: list[dict], checks: list[dict]) -> tuple[set[str], dict[str, int]]:
    """Item ids whose original (the unedited read) and donor (donor_unedited) are read right, with the counts."""
    base_ok = {r["name"] for r in rows if r["source"] == "unedited" and r["role"] == "none"}
    base_all = {r["name"] for r in rows if r["source"] == "unedited"}
    donor = {c["name"]: c["correct"] for c in checks if c["check"] == "donor_unedited"}
    ok = {n for n in base_ok if donor.get(n)}
    return ok, {"items": len(base_all), "original_right": len(base_ok), "donor_right": sum(donor.values()),
                "both_right": len(ok)}  # fmt: skip


def tagged(rows: list[dict], items: dict[str, dict]) -> list[dict]:
    """Rows with 'role' set to the outcome (finding5_confirm.diff reads 'role'), k_d and the clustering entity."""
    out = []
    for r in rows:
        it = items[r["name"]]
        out.append({**r, "pointer_role": r["role"], "role": classify(r["top"], it["sources"]["dissoc"]["predictions"]),
                    "_k": it["slots"]["position"] + 1, "_entity": f"{it['domain']}:{it['query']}",
                    "_decisive": decisive(it)})  # fmt: skip
    return out


def shares(rows: list[dict]) -> dict[str, Any]:
    n = len(rows)
    c = collections.Counter(r["role"] for r in rows)
    return {"n": n, **{o: [round(x, 4) for x in wilson(k, n)] for o, k in sorted(c.items())}}


def judge(d: list[float], d_rand: list[float]) -> str:
    if math.isnan(d[0]):
        return "not testable (no decisive items)"
    if math.isnan(d_rand[0]):
        return "not testable (no random-push rows)"
    if d[1] > 0 and d[1] > d_rand[2]:
        return "order"
    if d[2] < 0 and d[2] < d_rand[1]:
        return "fallback"
    return "neither"


def verdict(rows: list[dict], checks: list[dict], items: dict[str, dict], layer: int) -> dict[str, Any]:
    """Per family at `layer`, the last two tokens: the docstring's rule and its reported cuts."""
    ok, counts = eligible(rows, checks)
    sel = [r for r in rows if r["group"] == "last" and str(r["layer"]) == str(layer) and r["name"] in ok]
    sel = tagged([r for r in sel if r["source"] in ("dissoc", "rand", "same")], items)
    families: dict[str, Any] = {}
    for fam in sorted({r["family"] for r in sel}):
        by = {s: [r for r in sel if r["family"] == fam and r["source"] == s] for s in ("dissoc", "rand", "same")}
        dec = {s: [r for r in v if r["_decisive"]] for s, v in by.items()}
        d = F.diff(dec["dissoc"], "order", "fallback")
        d_rand = F.diff(dec["rand"], "order", "fallback")
        block: dict[str, Any] = {
            "n": len(by["dissoc"]), "n_decisive": len(dec["dissoc"]), "n_rand_decisive": len(dec["rand"]),
            "D_order_minus_fallback": d, "D_rand": d_rand, "verdict": judge(d, d_rand),
            "shares_decisive": shares(dec["dissoc"]), "shares_rand_decisive": shares(dec["rand"]),
            "same_changed": [round(x, 4) for x in wilson(sum(r["pointer_role"] != "none" for r in by["same"]),
                                                          len(by["same"]))],
            "by_k": {k: {"all": shares([r for r in by["dissoc"] if r["_k"] == k]),
                         "decisive": shares([r for r in dec["dissoc"] if r["_k"] == k]),
                         **({"D": F.diff([r for r in dec["dissoc"] if r["_k"] == k], "order", "fallback")}
                            if k > 1 else {})}
                     for k in range(1, 6)},
            "original_asks_1st": shares([r for r in by["dissoc"] if r["_k"] > 1 and not r["_decisive"]]),
            "by_topic": {dom: {"D": F.diff([r for r in dec["dissoc"] if r["domain"] == dom], "order", "fallback"),
                               "shares": shares([r for r in dec["dissoc"] if r["domain"] == dom])}
                         for dom in sorted({r["domain"] for r in by["dissoc"]})},
        }  # fmt: skip
        families[fam] = block
    return {"layer": layer, "counts": counts, "families": families}


def _pts(x: list[float]) -> str:
    return f"{100 * x[0]:+.0f} [{100 * x[1]:+.0f}, {100 * x[2]:+.0f}] points" if not math.isnan(x[0]) else "-"


def report(out: dict, decisive_family: str) -> str:
    lines = [f"# absent_entity / {out['run']}, layer {out['layer']}", "",
             f"Unedited reads: {json.dumps(out['counts'])}", ""]  # fmt: skip
    for fam, b in out["families"].items():
        tag = " (decisive)" if fam == decisive_family else " (reported)"
        lines += [f"**{fam}{tag}: {b['verdict']}** (n {b['n']}, decisive {b['n_decisive']})",
                  f"- order - fallback (k_d 2-5, original not asking its 1st): {_pts(b['D_order_minus_fallback'])}",
                  f"- random push, the same items: {_pts(b['D_rand'])}",
                  f"- same-entity control changed: {100 * b['same_changed'][0]:.0f}%",
                  "- by k_d: " + "; ".join(f"{k}: " + ", ".join(f"{o} {100 * v[0]:.0f}%" for o, v in c["all"].items()
                                                                if o != "n") + f" (n {c['all']['n']})"
                                           for k, c in b["by_k"].items()), ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--layer", type=int, default=LAYER)
    ap.add_argument("--family", default=FAMILY)
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new verdict folder")
    a = ap.parse_args(argv)
    from scripts import pointer_swap as PS

    m, rows, checks = PS.load_run(a.run)
    assert m.get("donor") == "absent", f"{a.run} is not an absent-entity run"
    kept, _ = with_absent(PS.load_items(m))  # the run sampled from these scenes only
    items = {it["id"]: it for it in absent_cases([it for its in kept.values() for it in its])}
    out = {"run": a.run, **verdict(rows, checks, items, a.layer)}
    d = Path(a.out) / f"{a.run}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    text = report(out, a.family)
    (d / "verdict.md").write_text(text)
    print(text, end="")
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
