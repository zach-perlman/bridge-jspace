"""lens_gate (22 Oct, night; rule fixed before any run): does a model's J-lens name a STATED bridge where it is stated?
A cheap read-only check (one clean forward per scene, no edits) before any lens test (D1, D4) on a new model.

Background (UNVERIFIED). D1's readwrite stage reads the bridge's best lens rank over a position set and the layers of
the window. Over the whole context the read is not specific: the other bridge X is mentioned there too, and on
Qwen3.6-27B X reaches the top 10 on 99-100% of items (d1_topics_rw_27b). At the bridge's own sentence it is: Qwen3.6-27B
bridge top-1 62%, top-10 85%, X top-10 5%; Qwen3-32B (whose D1 control failed) top-10 6-10%, X 1-2%.

Design. tasks_v2 PP items (level 0, the first n scenes in scene order; no competence filter: the read needs no right
answer), statement_positions' position sets: bind_bridge (the bridge's own sentence, "Clara picked the eagle."),
bridge_word ("eagle") and context. At each layer of the coarse grid in [lo, onset) (statement_positions' window: the
27B's 32-44; scaled by depth on other models), the lens readout at every position of the set; per item the bridge's
best word rank over the set's positions, and X's (the floor: a bridge that is mentioned elsewhere, not stated here).

Gate (fixed before the first run): PASS iff at bind_bridge, best over the window's layers, the bridge is in the lens's
top 10 on >= 50% of items and X on <= 20% (Wilson intervals reported). Reported, not decisive: top-1, each layer, the
bridge's word, the context (the old "92%"), digits vs words.

Gate v2 (22 Oct, 23:00, the outside review, before any v2 run). In the first runs the bridge's best rank over its
sentence sat on the bridge's own word in 166 / 180 (Qwen3.6-27B), 180 / 180 (Qwen3.5-9B) and 157 / 180 (Qwen3-32B)
cells: the lens decodes the input token where it stands, which shows the lens is not broken, not that it reads the
bridge as a variable. v2 reads only where the word is not: after_word (the bridge's sentence after its word: in prose
the closing period) and context_nomention (the context without any token of a mention of the bridge or of X). PASS iff
at after_word, best over the window's layers, the bridge is in the lens's top 10 on >= 50% of items and X on <= 20%
(the same bars). An item without an after_word token does not count. Reported: v1 (bind_bridge), context_nomention,
top-1, each layer.

uv run python scripts/lens_gate.py --name N --tasks-set S --n 60 --lo L --onset O [--why W]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.stats import wilson
from bridge_jspace.tokens import raw_encoding

EXP = "lens_gate"
RESULTS = pins.RESULTS_DIR / EXP
SETS = ("bind_bridge", "bridge_word", "after_word", "context_nomention", "context")
GATE_TOP10, FLOOR_TOP10 = 0.50, 0.20


def gate(best: dict[str, dict[str, int]], best_x: dict[str, dict[str, int]], key: str = "bind_bridge") -> dict:
    """best[set][item] = the bridge's best rank over the window; best_x the same for X; v1 key bind_bridge, v2
    after_word. Pure."""
    b = [r <= 10 for r in best.get(key, {}).values()]
    x = [r <= 10 for r in best_x.get(key, {}).values()]
    bt, xt = wilson(sum(b), len(b)), wilson(sum(x), len(x))
    ok = bool(b) and bt[0] >= GATE_TOP10 and xt[0] <= FLOOR_TOP10
    return {"pass": ok, "set": key, "bridge_top10": bt, "x_top10": xt, "n": len(b)}


def unmentioned(c: dict, offsets: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    """after_word (the bridge's sentence after its word) and context_nomention (context tokens that overlap no
    mention of the bridge or of X), from statement_positions' sets and the rendered prompt's offsets."""
    import re

    after = [i for i in c["sets"]["bind_bridge"] if i > max(c["sets"]["bridge_word"])]
    base = c["rendered"].index(c["context_text"])
    spans = [(base + m.start(), base + m.end()) for w in (c["bridge"], c["cf_bridge"])
             for m in re.finditer(rf"\b{re.escape(w)}\b", c["context_text"])]  # fmt: skip
    hit = {i for a, b in spans for i, (s, e) in enumerate(offsets) if e > s and s < b and e > a}
    return after, [i for i in c["sets"]["context"] if i not in hit]


def build(tok, set_name: str, n: int) -> list[dict]:
    from scripts import statement_positions as SP
    from scripts import tasks_v2 as T

    items = sorted((it for it in T.load(set_name) if it["word"] == "PP" and str(it["level"]) == "0"),
                   key=lambda it: it["scene"])[:n]  # fmt: skip
    out = []
    for it in items:
        try:  # C or O may not line up in another model's tokenizer (the sets were made with Qwen's): skipped
            c = {
                **it,
                **T.prepare(it, tok),
                "family": "PP",
                "rendered": T.render(tok, it),
                "context_text": it["context"],
            }
            enc = raw_encoding(tok, c["rendered"], offsets=True)
            assert enc["input_ids"] == c["ids"]["clean"], f"{c['id']}: the rendered prompt is not the clean one"
            c["sets"], _ = SP.position_sets(c, c["rendered"], enc["offset_mapping"])
            c["sets"]["after_word"], c["sets"]["context_nomention"] = unmentioned(c, enc["offset_mapping"])
        except AssertionError as e:
            print("skipped (unaligned):", str(e)[:120])
            continue
        out.append(c)
    return out


@torch.no_grad()
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", default="the lens gate before lens tests on this model")
    ap.add_argument("--tasks-set", default="d1_topics_v2")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--lo", type=int, required=True)
    ap.add_argument("--onset", type=int, required=True)
    a = ap.parse_args()
    from bridge_jspace.data import sha256_of
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import suite_split as P

    pins.check_run_name(a.name)
    out = RESULTS / a.name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "manifest.json").exists(), f"{out} exists; runs are written once"
    layers = [la for la in P.MAP_LAYERS if a.lo <= la < a.onset]
    data = pins.DATA_DIR / "tasks_v2" / a.tasks_set / "items.jsonl"
    manifest = {"exp": EXP, "run": a.name, "why": a.why, "model": pins.model_pin(),
                "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "tasks_set": a.tasks_set,
                "data_sha256": sha256_of(data), "n": a.n, "layers": layers, "window": [a.lo, a.onset],
                "gate": (__doc__ or "").split("Gate (fixed before the first run): ")[1].split("\n\nuv run")[0],
                "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    assert layers, f"no coarse layer in [{a.lo}, {a.onset})"
    model = load_model()
    lens = JLens(model, pins.FROZEN_LENS)
    cases = build(model.tokenizer, a.tasks_set, a.n)
    rows = []
    for c in progress(cases, "lens gate"):
        _, rec = model.run(torch.tensor([c["ids"]["clean"]], device="cuda"), record=tuple(layers))
        i_ids, x_ids = model.surface_ids(c["bridge"]), model.surface_ids(c["cf_bridge"])
        for s in SETS:
            pos = c["sets"][s]
            if not pos:  # no token after the bridge word in its sentence: the item does not count for v2
                continue
            for la in layers:
                logits = lens.readout(rec[la][pos], la)
                rows.append({"id": c["id"], "domain": c["domain"], "numbers": c["numbers"], "set": s, "layer": la,
                             "rank_bridge": min(model.word_rank(r, i_ids) for r in logits) if i_ids else None,
                             "rank_x": min(model.word_rank(r, x_ids) for r in logits) if x_ids else None})  # fmt: skip
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summary = summarise(rows, layers)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["gate_v2"]), json.dumps(summary["gate"]))
    print("wrote", out)
    return 0


def summarise(rows: list[dict], layers: list[int]) -> dict:
    best: dict[str, dict[str, int]] = collections.defaultdict(dict)
    best_x: dict[str, dict[str, int]] = collections.defaultdict(dict)
    per_layer: dict[str, dict] = {}
    for r in rows:
        s, i = r["set"], r["id"]
        if r["rank_bridge"] is not None:
            best[s][i] = min(best[s].get(i, 10**9), r["rank_bridge"])
        if r["rank_x"] is not None:
            best_x[s][i] = min(best_x[s].get(i, 10**9), r["rank_x"])
    for s in SETS:
        for la in layers:
            sel = [r for r in rows if r["set"] == s and r["layer"] == la and r["rank_bridge"] is not None]
            k1 = sum(r["rank_bridge"] <= 1 for r in sel)
            k10 = sum(r["rank_bridge"] <= 10 for r in sel)
            kx = sum(r["rank_x"] is not None and r["rank_x"] <= 10 for r in sel)
            per_layer[f"{s}/{la}"] = {"top1": wilson(k1, len(sel)), "top10": wilson(k10, len(sel)),
                                      "x_top10": wilson(kx, len(sel)), "n": len(sel)}  # fmt: skip
    window = {s: {"top1": wilson(sum(v <= 1 for v in best[s].values()), len(best[s])),
                  "top10": wilson(sum(v <= 10 for v in best[s].values()), len(best[s])),
                  "x_top10": wilson(sum(v <= 10 for v in best_x[s].values()), len(best_x[s]))} for s in SETS}  # fmt: skip
    return {
        "gate_v2": gate(best, best_x, "after_word"),
        "gate": gate(best, best_x),
        "window_best": window,
        "per_layer": per_layer,
    }


if __name__ == "__main__":
    raise SystemExit(main())
