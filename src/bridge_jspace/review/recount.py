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


def recount(view_id: str) -> list[dict]:
    v = I.view(view_id)
    h = v.get("headline", {})
    out = []
    for m, meta in I.spec()["models"].items():
        got = I.items(view_id, m)
        if not got:
            continue
        mk = meta["key"]
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
            cond = h["condition"]
            for label in h["arms"]:
                arm = v["filters"]["arms"][label]
                lk = [
                    it for it in got if it["condition"] == cond and it["reader"] == "PP" and it["rows"]["PP"].get(label)
                ]
                rc = [
                    it for it in got if it["condition"] == cond and it["reader"] == "PM" and it["rows"]["PM"].get(label)
                ]
                if not lk:
                    continue
                first = lk[0]["rows"]["PP"][label]
                run = f"{lk[0]['run'].rsplit('/', 1)[0]}/{first['_run']}" if "_run" in first else lk[0]["run"]
                for route in ROUTES:
                    share = sum(I.route_class(it["rows"]["PP"][label], cond) == route for it in lk) / len(lk)
                    out.append({"model": m, "quantity": f"{cond} {label}: {route}", "n": len(lk), "value": share,
                                **compare(share, route_keys(cond, arm, route, mk, run))})  # fmt: skip
                if rc:
                    share = switched([it["rows"]["PM"][label] for it in rc]) / len(rc)
                    out.append({"model": m, "quantity": f"{cond} {label}: recall follows S", "n": len(rc), "value": share,
                                **compare(share, route_keys(cond, arm, "recall_follows_s", mk, run))})  # fmt: skip
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
