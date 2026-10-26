"""Phase 2: each view's headline numbers recounted from the per-item files over the whole item set (not the run's
verdict), beside the figures/story/data.csv value of its source key: match (within the 2-decimal rounding), mismatch,
or no source.

  extra loss   (switches without the random part - switches without the part) / switches with the whole change, per
               reader (= Jdep - Rdep); gap = recall's - lookup's
  route share  the share of the lookup's items whose class under an arm is the route (C0: switch / original / other);
               recall follows S: the share of the recall's items that switch
  x8           the target share of the writes minus that of the random directions, at the headline's s
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


def first_number(text: str) -> float | None:
    m = re.match(r"\s*([−-]?\d+(?:\.\d+)?)", text)
    return float(m.group(1).replace("−", "-")) if m else None


def compare(value: float, key: str | None) -> dict:
    vals, _ = data_csv()
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
                out.append({"model": m, "quantity": f"{cond} {label}: {route}{tag}", "n": len(lk), "value": share,
                            **compare(share, route_keys(cond, arm, route, mk, src))})  # fmt: skip
            if rc:
                share = switched([it["rows"]["PM"][label] for it in rc]) / len(rc)
                out.append({"model": m, "quantity": f"{cond} {label}: recall follows S{tag}", "n": len(rc), "value": share,
                            **compare(share, route_keys(cond, arm, "recall_follows_s", mk, src))})  # fmt: skip
    return out


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
            else:
                out.append(one_part(got, e, m, mk, v))
        h = v.get("headline", {}) if isinstance(v.get("headline"), dict) else {}
        if h.get("stat") == "extra_loss":
            ex = {}
            for w in I.READERS:
                if w not in h.get("keys", {}):
                    continue
                ex[w], n = extra_loss(got, w, h)
                key = h["keys"][w].replace("<m>", mk)
                out.append(
                    {
                        "model": m,
                        "quantity": f"{I.READER_NAME[w]} extra loss",
                        "n": n,
                        "value": ex[w],
                        **compare(ex[w], key),
                    }
                )
            if "gap" in h.get("keys", {}) and len(ex) == 2:
                gap = ex["PM"] - ex["PP"]
                out.append({"model": m, "quantity": "gap (recall - lookup)", "n": out[-1]["n"], "value": gap,
                            **compare(gap, h["keys"]["gap"].replace("<m>", mk))})  # fmt: skip
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
