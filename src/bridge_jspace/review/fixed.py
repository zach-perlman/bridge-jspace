"""The fixed sample Dan reads tomorrow (Dan 29 Oct 11:45, jobs/c3/batch53.yaml verify_prep_1145 item 3): seed 29,
N = 10 per tier-1 view, pooled over the view's models: 6 random, stratified by model x reader, and 4 targeted, 2
nearest the decision (|p_alt - p_org| smallest) and 2 "surprising" (the lookup switches without the lens part but not
without the random part, or the reverse; each view's equivalent is its "targeted" entry in the views file).

Drawn once (`uv run python scripts/review.py sample`) and written into docs/review/review_views.yaml (fixed_sample): the
dashboard and the export read the items from there, so no re-roll can change them.

Strata of the 6 random items: the view's models in a seeded order, one item per (model, reader), the reader
alternating, round after round (5 models: every model once, one twice; 1 model: 3 lookups and 3 recalls). Within a
stratum: random.Random(f"{seed}|{view}|{model}|{reader}|{k}").choice over the items sorted by id.
"""

from __future__ import annotations

import math
import random
import re
import subprocess
import time
from typing import Any

from bridge_jspace.review import items as I

SEED, N, N_RANDOM, N_NEAREST, N_SURPRISING = 29, 10, 6, 2, 2
BEGIN, END = "# ---- fixed_sample: BEGIN (generated", "# ---- fixed_sample: END"


def tier1() -> list[dict]:
    return [v for v in I.spec()["views"] if v.get("tier") == 1]


def keep(v: dict, it: dict) -> bool:
    """The view's sample_filter: the claim's condition (routes C2), the swap's dose and kind (x8 s = 2 writes)."""
    f = v.get("sample_filter") or {}
    if "condition" in f and it["condition"] != f["condition"]:
        return False
    if "reader" in f and it["reader"] != f["reader"]:
        return False
    x8 = it["x8"]
    return not (x8 and (("s" in f and float(x8["s"]) != float(f["s"])) or ("kind" in f and x8["kind"] != f["kind"])))


def pool(v: dict) -> list[dict]:
    return sorted(
        (it for m in I.spec()["models"] for it in I.items(v["id"], m) if keep(v, it)), key=lambda it: it["id"]
    )


def strata(models: list[str], seed: int, view_id: str, n: int = N_RANDOM) -> list[tuple[str, str]]:
    ms = sorted(models)
    random.Random(f"{seed}|{view_id}|strata").shuffle(ms)
    out = [(m, I.READERS[(i + r) % 2]) for r in range(math.ceil(n / len(ms)) + 1) for i, m in enumerate(ms)]
    return out[:n]


def draw_random(v: dict, got: list[dict], seed: int) -> list[tuple[dict, str]]:
    by: dict[tuple[str, str], list[dict]] = {}
    for it in got:
        by.setdefault((it["model"], it["reader"]), []).append(it)
    chosen: list[tuple[dict, str]] = []
    taken: set[str] = set()
    count: dict[tuple[str, str], int] = {}
    for m, w in strata(sorted({it["model"] for it in got}), seed, v["id"]):
        cand = [it for it in by.get((m, w), []) if it["id"] not in taken]
        if not cand:
            continue
        k = count.get((m, w), 0)
        count[(m, w)] = k + 1
        pick = random.Random(f"{seed}|{v['id']}|{m}|{w}|{k}").choice(cand)
        taken.add(pick["id"])
        chosen.append((pick, f"random: {I.spec()['models'][m]['label']} x {I.READER_NAME[w]}"))
    return chosen


def switched(r: dict | None) -> bool | None:
    return None if r is None else bool(r["switched"])


def margin(it: dict, labels: list[str]) -> tuple[float, float] | None:
    """The smallest |p_alt - p_org| under the view's decisive arms, over the arms whose top token is one of the two
    answers (role A or b: where the top token is a third token both probabilities can be ~0, and |p_alt - p_org| = 0
    there says nothing about the decision); ties by |ld|. None where no probability is stored; x0-like items count only
    where the whole change switched them (the switches the extra loss counts)."""
    rows = it["rows"][it["reader"]]
    whole = next((r for label, r in rows.items() if label in ("whole", "whole-state patch")), None)
    if it["kind"] in ("x0", "x51_answer", "zach") and not (whole and whole["switched"]):
        return None
    rd = ((it["case"] or {}).get("readers") or {}).get(it["reader"]) or {}
    if rd.get("tok_A") is not None and rd.get("tok_A") == rd.get("tok_b"):  # one token for both answers: no decision
        return None
    got = [(abs(r["p_alt"] - r["p_org"]), abs(r.get("ld") or 0.0)) for label in labels
           if (r := rows.get(label)) and "p_alt" in r and r.get("role", "A") in ("A", "b")]  # fmt: skip
    return min(got) if got else None


def surprise(v: dict, it: dict) -> str | None:
    """Which "surprising" direction an item is in, or None (the view's targeted.surprising)."""
    s = (v.get("targeted") or {}).get("surprising") or {}
    w = it["reader"]
    if s.get("reader") and w != s["reader"]:
        return None
    rows = it["rows"][w]
    if s.get(
        "order_vs_switch"
    ):  # sentence order: a locker-first lookup that does not switch, or a locker-after one that does
        sw, o = switched(rows.get("whole")), it["order"].get("original")
        return ("locker first, not switched" if o == "before" and sw is False else
                "locker after, switched" if o == "after" and sw else None)  # fmt: skip
    if s.get("lookup_vs_recall"):  # x8: the lookup goes to the target but the recall does not change, or the reverse
        key = next(iter(k for k in rows if k != "unwritten"), None)
        pp, pm = it["rows"]["PP"].get(key), it["rows"]["PM"].get(key)
        if w != "PP" or pp is None or pm is None:
            return None
        to_target, changed = pp["class"] == "target", bool(pm["changed"])
        return ("lookup to the target, recall unchanged" if to_target and not changed else
                "recall changed, lookup not to the target" if changed and not to_target else None)  # fmt: skip
    rp, rr = rows.get(s.get("part")), rows.get(s.get("random"))
    if rp is None or rr is None:
        return None
    p, q = s["part"], s["random"]
    if (
        "route" in s
    ):  # routes: the position route kept without the address but lost without its random part, or the reverse
        a, b = I.route_class(rp, it["condition"]) == s["route"], I.route_class(rr, it["condition"]) == s["route"]
        name = s["route"]
        return (
            f"{name} under '{p}', not under '{q}'"
            if a and not b
            else (f"{name} under '{q}', not under '{p}'" if b and not a else None)
        )
    whole = next((r for label, r in rows.items() if label in ("whole", "whole-state patch")), None)
    if s.get("mode") != "differ" and not (whole and whole["switched"]):
        return None
    a, b = bool(rp["switched"]), bool(rr["switched"])
    return (f"switches under '{p}', not under '{q}'" if a and not b else
            f"switches under '{q}', not under '{p}'" if b and not a else None)  # fmt: skip


def draw_targeted(v: dict, got: list[dict], seed: int, taken: set[str]) -> list[tuple[dict, str]]:
    t = v.get("targeted") or {}
    out: list[tuple[dict, str]] = []
    n_sur = N_SURPRISING
    if t.get("nearest"):
        near = sorted(
            (m, it["id"], it) for it in got if it["id"] not in taken and (m := margin(it, t["nearest"])) is not None
        )
        for m, _, it in near[:N_NEAREST]:
            out.append((it, f"targeted: nearest the decision (|p_alt - p_org| = {m[0]:.4f}, |ld| {m[1]:.3f})"))
            taken.add(it["id"])
    else:  # no probabilities stored (x8): the 4 targeted items are all "surprising", 2 per direction
        n_sur += N_NEAREST
    groups: dict[str, list[dict]] = {}
    for it in got:
        if it["id"] not in taken and (d := surprise(v, it)):
            groups.setdefault(d, []).append(it)
    rng = random.Random(f"{seed}|{v['id']}|surprising")
    names = sorted(groups)
    # one direction after the other, as evenly as the candidates allow
    while n_sur and any(groups[d] for d in names):
        for d in names:
            if n_sur and groups[d]:
                it = groups[d].pop(rng.randrange(len(groups[d])))
                out.append((it, f"targeted: surprising ({d}; {len(groups[d]) + 1} candidates)"))
                taken.add(it["id"])
                n_sur -= 1
    return out


def draw(v: dict, seed: int = SEED) -> list[dict[str, Any]]:
    got = pool(v)
    rand = draw_random(v, got, seed)
    taken = {it["id"] for it, _ in rand}
    chosen = rand + draw_targeted(v, got, seed, taken)
    return [{"item": it["id"], "model": it["model"], "reader": it["reader"], "scene": it["scene"], "run": it["run"],
             "layer": it["layer"], "stratum": why, **({"condition": it["condition"]} if it["condition"] else {}),
             **({"x8": {k: it["x8"][k] for k in ("kind", "j", "k", "s")}} if it["x8"] else {})} for it, why in chosen]  # fmt: skip


def yaml_block(seed: int = SEED) -> str:
    """The fixed_sample block for the end of the views file (one line per item, so a diff shows every change)."""
    import json

    sha = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=I.REPO, capture_output=True, text=True
    ).stdout.strip()
    lines = [f"{BEGIN} by `uv run python scripts/review.py sample` at {sha}, "
             f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; do not edit by hand, never re-roll)",
             "fixed_sample:", f"  seed: {seed}", f"  n_per_view: {N}",
             "  rule: >-",
             "    Dan 29 Oct 11:45 (verify_prep_1145 item 3): per tier-1 view, pooled over its models, 6 random stratified by",
             "    model x reader (the models in a seeded order, one item per (model, reader), the reader alternating, round",
             "    after round) + 4 targeted: 2 nearest the decision (|p_alt - p_org| smallest under the view's decisive arms,",
             "    items the whole change switched) and 2 surprising (the view's targeted.surprising, one per direction where",
             "    both exist). N = 10 per view in all (not per model): the agent's reading of 'N = 10 per view' with 6 + 4;",
             "    flagged. Item ids as the dashboard's: model|run|scene|reader[|condition][|kind|j-k|s].",
             "  views:"]  # fmt: skip
    for v in tier1():
        lines.append(f"    {v['id']}:")
        for e in draw(v, seed):
            lines.append("      - " + json.dumps(e, ensure_ascii=False))
    return "\n".join([*lines, END]) + "\n"


def write(seed: int = SEED) -> None:
    """Replace (or append) the fixed_sample block of the views file; the rest of the file is kept as is."""
    text = I.VIEWS_FILE.read_text()
    block = yaml_block(seed)
    if BEGIN in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip("\n") + "\n\n" + block
    I.VIEWS_FILE.write_text(text)
    I.spec.cache_clear()


def fixed(view_id: str, seed: int) -> list[dict] | None:
    """The view's fixed sample for this seed, if one was drawn."""
    fs = I.spec().get("fixed_sample") or {}
    if fs.get("seed") != seed:
        return None
    return (fs.get("views") or {}).get(view_id)


def samples(v: dict, seed: int, models: list[str]) -> dict[str, list[dict]] | None:
    """The fixed sample in the dashboard's format, per model: [{stratum, population, items}] (None: no fixed sample
    for this view and seed). An item no longer in the item set is a finding: it raises."""
    got = fixed(v["id"], seed)
    if got is None:
        return None
    out: dict[str, list[dict]] = {}
    for m in models:
        by_id = {it["id"]: it for it in I.items(v["id"], m)}
        mine = [e for e in got if e["model"] == m]
        if not mine:
            continue
        missing = [e["item"] for e in mine if e["item"] not in by_id]
        if missing:
            raise KeyError(f"fixed sample items not in the item set any more: {missing}")
        pop = sum(keep(v, it) for it in by_id.values())
        out[m] = [{"stratum": e["stratum"], "population": pop, "items": [by_id[e["item"]]]} for e in mine]
    return out
