"""c2_route_collision: how often the recall cannot tell the position route from the entity in the routes test's C2 scenes (CPU,
saved scenes and rows only; no run, key or claim is touched; Dan 30 Oct).

C2 moves another item: in the changed prompt S the asked person's pick is another entity (cf_bridge), whose locker sentence sits at some
slot of S's locker list. The position-route entity is the entity that sits, in the original prompt O, at that same slot. If the recall's
answer for it (its legs) equals the recall's changed answer (the legs of cf_bridge), a recall that follows the position gives the changed
answer too, so its switch cannot be read as following the entity (example: C2-0538 on the 9B: deer and bear both have 4 legs).

1. Per model, over the routes view's C2 items (the run's item set, one per scene): collisions / n.
2. The one claim that reads the recall's change on C2 scenes as following an entity: the address swap (x8_write, s = 2) "of the recalls
   it changes, 0.84 (9B) / 0.85 (Lightning) name the swapped-in item's legs". Recomputed on the items where the swapped-in item's legs
   differ from the third item's (the two readings are then distinguishable) beside the published number.

uv run python scripts/c2_route_collision.py       # writes results/c2_route_collision/<UTC>/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from bridge_jspace.review import checks as C  # noqa: E402
from bridge_jspace.review import items as I  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x52_cpu_checks as CC  # noqa: E402


def routes_collisions() -> dict:
    legs = I.legs()
    out = {}
    for model in I.spec()["models"]:
        n, hits = 0, []
        for it in I.items("routes", model):
            if it["condition"] != "C2" or it["reader"] != "PP" or not it["case"]:
                continue
            c = it["case"]
            o = [x for x, _ in C.LOCKER.findall(c["context"])]
            s = [x for x, _ in C.LOCKER.findall(c["cf_context"])]
            if len(o) != 3 or len(s) != 3 or c["cf_bridge"] not in s:
                continue
            n += 1
            pos_entity = o[s.index(c["cf_bridge"])]
            if legs[pos_entity] == int(c["readers"]["PM"]["cf_answer"]):
                hits.append({"scene": it["scene"], "position_entity": pos_entity, "changed_entity": c["cf_bridge"], "legs": legs[pos_entity]})
        out[model] = {"n": n, "collisions": len(hits), "share": round(len(hits) / n, 4) if n else None, "items": hits}
    return out


def swap_claim() -> dict:
    from scripts import x6_routes as R
    from scripts import x8_write as W

    out = {}
    for target, run in CC.WRITE.items():
        tok = CC.tokenizer_of(target)
        legs_of, _, _ = R.pools(tok)
        cases = {c["scene"]: c for c in R.scenes(tok, R.N_GEN)[0] if c["condition"] == "C2"}

        def tok_id(d: int, tok=tok) -> int:
            return tok.encode(str(d), add_special_tokens=False)[0]

        rows = [r for r in X.read_jsonl(pins.RESULTS_DIR / "x8_write" / run / "outcomes.jsonl") if r["reader"] == "PM" and r["kind"] == "write" and r["s"] == 2]
        allc, clean = [], []
        n_all = n_clean = 0
        for r in rows:
            c = cases[r["scene"]]
            legs = [legs_of[item] for item, _ in W.slots_of(c["context"])]
            third = next(s for s in range(3) if s not in (r["j"], r["k"]))
            cls = CC.swap_class(r, tok_id, legs)
            ok = legs[r["k"]] != legs[third] and legs[r["k"]] != legs[r["j"]]  # the swapped-in item's legs name only it
            n_all += 1
            n_clean += ok
            if cls != "unchanged":
                allc.append(cls)
                if ok:
                    clean.append(cls)
        out[target] = {"run": run, "rows": n_all, "rows_non_colliding": n_clean,
                       "all": CC.shares(allc, CC.SWAP_CLASSES[1:]), "non_colliding": CC.shares(clean, CC.SWAP_CLASSES[1:])}
    return out


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "c2_route_collision" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "c2_route_collision", "written_utc": stamp, "script": "scripts/c2_route_collision.py",
                                                   "note": "CPU, saved scenes and rows only; no run, key, label or claim touched"}, indent=2))
    blob = {"routes_c2": routes_collisions(), "swap_claim": swap_claim()}
    (out / "tables.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False))
    print(json.dumps({m: {k: v for k, v in x.items() if k != "items"} for m, x in blob["routes_c2"].items()}, indent=1))
    print(json.dumps(blob["swap_claim"], indent=1))
    print(next((i for i in blob["routes_c2"]["qwen3.5-9b"]["items"] if i["scene"] == "C2-0538"), "C2-0538 not a collision on the 9B"))
    return out


if __name__ == "__main__":
    main()
