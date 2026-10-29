"""Phase 2: each view's headline numbers recounted from the per-item files over the whole item set (not the run's
verdict), beside the figures/story/data.csv value of its source key: match (within the 2-decimal rounding), mismatch,
or no source.

  extra loss   (switches without the random part - switches without the part) / switches with the whole change, per
               reader (= Jdep - Rdep); gap = recall's - lookup's
  route share  the share of the lookup's items whose class under an arm is the route (C0: switch / original / other);
               recall follows S: the share of the recall's items that switch
  x8           the target share of the writes minus that of the random directions, at the headline's s
  order        the lookups the whole change switches (k of n), the locker sentence before / after the pick sentence
"""

from __future__ import annotations

import csv
import re
from functools import lru_cache

from bridge_jspace.review import items as I

TOL = 0.005 + 1e-9  # data.csv holds 2 decimals
ROUTES = ("identity", "position", "value", "original", "other")


@lru_cache(maxsize=1)
def data_csv() -> tuple[dict[str, str], dict[str, str]]:
    """key -> its text value and its source file, from the rows figures/story/data.csv copies from x0_numbers.json."""
    value, source = {}, {}
    with (I.REPO / "figures" / "story" / "data.csv").open() as f:
        for r in csv.DictReader(f):
            if r["figure"] == "numbers":
                value[r["quantity"]], source[r["quantity"]] = r["value"], r["source"]
    return value, source


@lru_cache(maxsize=1)
def csv_rows() -> dict[tuple[str, str], list[dict]]:
    """(model column, quantity) -> its figures/story/data.csv rows (any figure): the README's src comments name a
    quantity and the model is the column."""
    out: dict[tuple[str, str], list[dict]] = {}
    with (I.REPO / "figures" / "story" / "data.csv").open() as f:
        for r in csv.DictReader(f):
            out.setdefault((r["model"], r["quantity"]), []).append(r)
    return out


def tolerance(text: str) -> float:
    """Half a unit of the stored number's last decimal (2 decimals: 0.005; a full-precision float: ~0)."""
    m = re.match(r"\s*[−-]?\d+(?:\.(\d+))?", text)
    return 0.5 * 10 ** -len(m.group(1) or "") + 1e-9 if m else 0.0


def compare_csv(value: float, model: str, quantity: str | None) -> dict:
    """Against the data.csv row(s) of (model, quantity); all its rows (one quantity can sit in several figures) must
    agree within each row's precision."""
    rows = csv_rows().get((model, quantity or ""), [])
    nums = [(r, first_number(r["value"])) for r in rows]
    nums = [(r, x) for r, x in nums if x is not None]
    if not nums:
        return {"key": f"data.csv: {quantity}" if quantity else "", "data": "", "status": "no source"}
    ok = all(abs(value - x) <= tolerance(r["value"]) for r, x in nums)
    shown = sorted({r["value"] for r, _ in nums})
    return {"key": f"data.csv: {quantity}", "data": " / ".join(shown), "status": "match" if ok else "mismatch",
            "source": sorted({r["source"] for r, _ in nums})[0]}  # fmt: skip


def compare_any(value: float, key: str | None, model: str, quantity: str | None) -> dict:
    """x0_numbers.json's key (through data.csv's numbers rows) where it exists, else data.csv by (model, quantity)."""
    got = compare(value, key)
    return got if got["status"] != "no source" or not quantity else compare_csv(value, model, quantity)


def first_number(text: str) -> float | None:
    m = re.match(r"\s*([−-]?\d+(?:\.\d+)?)", text)
    return float(m.group(1).replace("−", "-")) if m else None


def compare(value: float, key: str | None) -> dict:
    """Against data.csv; key may list alternatives "a|b" (the first that exists, e.g. the 9B's natural run at gate
    0.75 has natg75_* keys)."""
    vals, _ = data_csv()
    if key and "|" in key:
        key = next((k for k in key.split("|") if k in vals), key.split("|")[0])
    if not key or key not in vals:
        return {"key": key or "", "data": "", "status": "no source"}
    ref = first_number(vals[key])
    if ref is None:
        return {"key": key, "data": vals[key], "status": "no source"}
    return {"key": key, "data": vals[key], "status": "match" if abs(value - ref) <= TOL else "mismatch"}


def switched(rows: list[dict | None]) -> int:
    return sum(int(r["switched"]) for r in rows if r is not None)


def extra_loss(items: list[dict], reader: str, h: dict) -> tuple[float, int]:
    mine = [it["rows"][reader] for it in items if it["reader"] == reader]
    whole = switched([r.get(h["whole"]) for r in mine])
    part, rand = switched([r.get(h["part"]) for r in mine]), switched([r.get(h["random"]) for r in mine])
    return ((rand - part) / whole if whole else float("nan")), len(mine)


def route_keys(cond: str, arm: str, route: str, mkey: str, run: str) -> str | None:
    """The data.csv key for this route share whose source file is in the run the arm's rows came from."""
    _, source = data_csv()
    tail = f"_{cond}_{arm}_{route}_{mkey}"
    hits = [k for k, s in source.items() if k.endswith(tail) and s.startswith(run + "/")]
    return min(hits, key=len) if hits else None  # several prefixes may read one verdict (Muse): the same number


def lost(items: list[dict], reader: str, part: str) -> float:
    """Jdep: the share of the whole change's switches lost without the part."""
    mine = [it["rows"][reader] for it in items if it["reader"] == reader]
    whole = switched([r.get("whole") for r in mine])
    return 1 - switched([r.get(part) for r in mine]) / whole if whole else float("nan")


def ld_extra(items: list[dict], reader: str, h: dict) -> float:
    """On the logit difference (batch 39): the shift of an arm = ld(arm) - ld(unedited); extra loss = (mean shift
    without the random part - mean shift without the part) / mean shift of the whole change."""
    mine = [it["rows"][reader] for it in items if it["reader"] == reader]
    shift = {
        a: sum(r[a]["ld"] - r["unedited"]["ld"] for r in mine) / len(mine) for a in ("whole", h["part"], h["random"])
    }
    return (shift[h["random"]] - shift[h["part"]]) / shift["whole"]


def compare_ref(value: float, ref: str, model_name: str, file: str) -> dict:
    """Against an analysis output (full precision): the JSON field at ref, <M> = the file's name for the model."""
    blob = I.read_json(file)
    for k in ref.replace("<M>", model_name).split("."):
        blob = blob[int(k)] if isinstance(blob, list) else blob.get(k, {})
    ok = isinstance(blob, float | int) and abs(value - blob) <= 1e-9
    return {"key": f"{file.split('/')[-2]}: {ref.replace('<M>', model_name)}", "data": f"{blob:.4f}" if ok or isinstance(blob, float) else "",
            "status": "match" if ok else "mismatch"}  # fmt: skip


def one_part(got: list[dict], e: dict, m: str, mk: str, v: dict | None = None) -> dict:
    """A headline entry on one condition and reader: extra_loss / lost, or the difference of two (…_minus); ld_extra
    / ld_gap on the logit difference, compared with the view's ref_file."""
    pool = [it for it in got if e.get("condition") in (None, it["condition"])]
    if e["stat"] in ("ld_extra", "ld_gap"):
        h = {"part": e["part"], "random": e["random"]}
        val = (
            ld_extra(pool, e.get("reader", "PP"), h)
            if e["stat"] == "ld_extra"
            else ld_extra(pool, "PM", h) - ld_extra(pool, "PP", h)
        )
        name = (
            f"{I.READER_NAME[e['reader']]} extra loss on ld"
            if e["stat"] == "ld_extra"
            else "gap on ld (recall - lookup)"
        )
        ref = compare_ref(val, e["ref"], (v or {}).get("ref_models", {}).get(m, m), (v or {})["ref_file"])
        return {"model": m, "quantity": name, "n": sum(it["reader"] == "PP" for it in pool), "value": val, **ref}
    if e["stat"] == "gap":  # the recall's extra loss minus the lookup's, on switches
        h = {"whole": "whole", "part": e["part"], "random": e["random"]}
        val = extra_loss(pool, "PM", h)[0] - extra_loss(pool, "PP", h)[0]
        n = sum(it["reader"] == "PP" for it in pool)
        return {"model": m, "quantity": f"gap (recall - lookup): {e['part']}", "n": n, "value": val,
                **compare(val, e["key"].replace("<m>", mk))}  # fmt: skip
    w = e["reader"]
    n = sum(it["reader"] == w for it in pool)
    h = {"whole": "whole", "part": e["part"], "random": e.get("random")}
    if e["stat"].startswith("extra_loss"):
        val = extra_loss(pool, w, h)[0]
        if e["stat"] == "extra_loss_minus":
            val -= extra_loss(pool, w, {"whole": "whole", "part": e["minus_part"], "random": e["minus_random"]})[0]
    else:
        val = lost(pool, w, e["part"]) - (lost(pool, w, e["minus_part"]) if e["stat"] == "lost_minus" else 0)
    what = {"extra_loss": "extra loss", "extra_loss_minus": "extra loss minus", "lost": "switches lost",
            "lost_minus": "switches lost minus"}[e["stat"]]  # fmt: skip
    name = f"{e.get('condition', '')} {I.READER_NAME[w]} {what}: {e['part']}" + (
        f" − {e['minus_part']}" if "minus_part" in e else ""
    )
    return {"model": m, "quantity": name.strip(), "n": n, "value": val, **compare(val, e["key"].replace("<m>", mk))}


def route_shares(v: dict, got: list[dict], e: dict, m: str, mk: str) -> list[dict]:
    """Per run of the view (join: false gives one per layer) and arm: the lookup's route shares, the recall's switches."""
    out = []
    cond = e["condition"]
    for run in sorted({it["run"] for it in got}):
        mine = [it for it in got if it["run"] == run and it["condition"] == cond]
        tag = f" ({run.split('/')[-1]})" if v.get("join", True) is False else ""
        for label in e["arms"]:
            arm = v["filters"]["arms"][label]
            lk = [it for it in mine if it["reader"] == "PP" and it["rows"]["PP"].get(label)]
            rc = [it for it in mine if it["reader"] == "PM" and it["rows"]["PM"].get(label)]
            if not lk:
                continue
            first = lk[0]["rows"]["PP"][label]
            src = f"{run.rsplit('/', 1)[0]}/{first['_run']}" if "_run" in first else run
            for route in ROUTES:
                share = sum(I.route_class(it["rows"]["PP"][label], cond) == route for it in lk) / len(lk)
                q = e["csv"].replace("<arm>", arm).replace("<route>", route) if e.get("csv") and cond == "C2" else None
                out.append({"model": m, "quantity": f"{cond} {label}: {route}{tag}", "n": len(lk), "value": share,
                            **compare_any(share, route_keys(cond, arm, route, mk, src), m, q)})  # fmt: skip
            if rc:
                share = switched([it["rows"]["PM"][label] for it in rc]) / len(rc)
                out.append({"model": m, "quantity": f"{cond} {label}: recall follows S{tag}", "n": len(rc), "value": share,
                            **compare(share, route_keys(cond, arm, "recall_follows_s", mk, src))})  # fmt: skip
    return out


TIER1_STATS = ("share_kept", "answer_rank_below", "x8_target_mean_pairs", "x8_recall_changed", "switch_share")
E1_ARMS = {1: ("arm 1: without the lens part", "arm 1's random part"),
           2: ("arm 2: without the lens part, its answer directions kept", "arm 2's random part")}  # fmt: skip


def tier1_stat(got: list[dict], e: dict, m: str) -> dict:
    """The tier-1 views' own headline numbers (Dan 29 Oct 11:45), each against data.csv by (model, quantity):
    share_kept           51.12 E1: arm 2's extra loss / arm 1's (the recall's loss kept with the answer directions)
    answer_rank_below    51.12 E1: the share of items whose answer word ranks below the lens's top N at the bridge
                         word on both O and S (readout.jsonl variants org and alt; x51_answer's "not_read" =
                         1 - top50_either)
    x8_target_mean_pairs the swap: the lookup's target share per locker pair (j, k), then the mean over the pairs
    x8_recall_changed    the swap: the share of recalls that change
    switch_share         51.10: the share of a reader's items an arm switches"""
    w = e.get("reader", "PP")
    mine = [it for it in got if it["reader"] == w]
    if e["stat"] == "share_kept":
        ex = {a: extra_loss(got, w, {"whole": "whole", "part": p, "random": r})[0] for a, (p, r) in E1_ARMS.items()}
        val, what = ex[2] / ex[1] if ex[1] else float("nan"), "share of arm 1's extra loss kept by arm 2"
    elif e["stat"] == "answer_rank_below":
        rk = [it["more"].get("answer_rank") or {} for it in mine]
        pairs = [(o, s) for r in rk if (o := (r.get("org") or {}).get(w)) is not None
                 and (s := (r.get("alt") or {}).get(w)) is not None]  # fmt: skip
        val = sum(o > e["top"] and s > e["top"] for o, s in pairs) / len(pairs)
        what = f"answer word below the lens's top {e['top']} on both O and S"
        mine = pairs
    elif e["stat"].startswith("x8_"):
        mine = [it for it in mine if it["x8"]["kind"] == "write" and float(it["x8"]["s"]) == float(e["s"])]
        if e["stat"] == "x8_target_mean_pairs":
            pairs: dict = {}
            for it in mine:
                pairs.setdefault((it["x8"]["j"], it["x8"]["k"]), []).append(it["cls"] == "target")
            val = sum(sum(x) / len(x) for x in pairs.values()) / len(pairs) if pairs else float("nan")
            what = f"lookup target share, mean over {len(pairs)} locker pairs, s = {e['s']:g}"
        else:
            val, what = sum(it["cls"] == "changed" for it in mine) / len(mine), f"recalls that change, s = {e['s']:g}"
    else:  # switch_share
        rows = [it["rows"][w].get(e["arm"]) for it in mine]
        val, what = switched(rows) / len(mine), f"switched by {e['arm']}"
    return {"model": m, "quantity": f"{I.READER_NAME[w]}: {what}", "n": len(mine), "value": val,
            **compare_csv(val, m, e["csv"])}  # fmt: skip


def recount(view_id: str) -> list[dict]:
    v = I.view(view_id)
    out = []
    for m, meta in I.spec()["models"].items():
        got = I.items(view_id, m)
        if not got:
            continue
        mk = meta["key"]
        entries = v.get("headline")
        for e in entries if isinstance(entries, list) else []:
            if e["stat"] == "route_share":
                out += route_shares(v, got, e, m, mk)
            elif e["stat"] in TIER1_STATS:
                out.append(tier1_stat(got, e, m))
            elif "key" not in e and "csv" in e:  # an extra loss read against data.csv only
                val, n = extra_loss(got, e["reader"], {"whole": e.get("whole", "whole"), **e})
                out.append({"model": m, "quantity": f"{I.READER_NAME[e['reader']]} extra loss: {e['part']}", "n": n,
                            "value": val, **compare_csv(val, m, e["csv"])})  # fmt: skip
            else:
                out.append(one_part(got, e, m, mk, v))
        h = v.get("headline", {}) if isinstance(v.get("headline"), dict) else {}
        if h.get("stat") == "extra_loss":
            ex = {}
            keys, qs = h.get("keys", {}), h.get("csv", {})
            for w in I.READERS:
                if w not in keys and w not in qs:
                    continue
                ex[w], n = extra_loss(got, w, h)
                key = keys.get(w, "").replace("<m>", mk) or None
                out.append({"model": m, "quantity": f"{I.READER_NAME[w]} extra loss", "n": n, "value": ex[w],
                            **compare_any(ex[w], key, m, qs.get(w))})  # fmt: skip
            if ("gap" in keys or "gap" in qs) and len(ex) == 2:
                gap = ex["PM"] - ex["PP"]
                key = keys.get("gap", "").replace("<m>", mk) or None
                out.append({"model": m, "quantity": "gap (recall - lookup)", "n": out[-1]["n"], "value": gap,
                            **compare_any(gap, key, m, qs.get("gap"))})  # fmt: skip
        elif h.get("stat") == "order_switched":  # the lookups the whole change switches, by sentence order
            for o in ("before", "after"):
                lk = [it for it in got if it["reader"] == "PP" and it["order"].get("original") == o]
                k = switched([it["rows"]["PP"].get("whole") for it in lk])
                for what, val in (("k", k), ("n", len(lk))):
                    key = h["keys"][what].replace("<o>", o).replace("<m>", mk)
                    out.append({"model": m, "quantity": f"lookups switched, locker {o} the pick: {what}", "n": len(lk),
                                "value": float(val), **compare(val, key)})  # fmt: skip
                if h.get("csv") and lk:  # the share, as the README's Lightning numbers and fig03 / s03 store it
                    out.append({"model": m, "quantity": f"lookups switched, locker {o} the pick: share", "n": len(lk),
                                "value": k / len(lk), **compare_csv(k / len(lk), m, h["csv"].replace("<o>", o))})  # fmt: skip
        elif h.get("stat") == "route_share":
            out += route_shares(v, got, h, m, mk)
        elif h.get("stat") == "x8_target_minus_random":
            s = h["s"]
            lk = [it for it in got if it["reader"] == "PP" and it["x8"]["s"] == s]
            tgt = {
                kind: [it["cls"] == "target" for it in lk if it["x8"]["kind"] == kind] for kind in ("write", "random")
            }
            if tgt["write"] and tgt["random"]:
                val = sum(tgt["write"]) / len(tgt["write"]) - sum(tgt["random"]) / len(tgt["random"])
                out.append({"model": m, "quantity": f"target share, write - random, s = {s}", "n": len(tgt["write"]),
                            "value": val, **compare(val, None)})  # fmt: skip
    return out
