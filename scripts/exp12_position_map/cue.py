"""exp12 add-on: is the bridge, or already the answer, readable on the cue phrase, where part B's swap acts?

Reads a finished exp12 run's grids (no model). The cue phrase's positions are part B's `cue` regime (exp02): the
tokens of the phrase in data/cue_spans.json ("Amazon River ends"), without the prompt's last two positions (-1 and 0,
part A's read sites). Per question and reader, for each layer band:
  cue    the best share of band layers with the word ranked first among its candidates, over the cue tokens; the
         same search for its same-category control (distractor / swap answer) is the noise ceiling, since several
         tokens are searched
  noncue the same best share over the other earlier tokens (part B's `earlier_noncue` positions)
  -1, 0  the share at one word before the end and at the last word (exp12's read sites), for comparison
and per layer, the share of questions with the word ranked first at some cue token. 95% bootstrap CI over questions.
Layers 0-4 are the lexical baseline: a cue word's own associations ("Munich" -> Germany, "Romeo" -> Shakespeare)
already rank the bridge first there, so a band's share counts as computed only by how far it exceeds 0-4's.
    uv run python -m scripts.exp12_position_map.cue <exp12 run dir>   # -> <run>/analysis-<timestamp>-cue/
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from bridge_jspace.pins import DATA_DIR
from bridge_jspace.stats import bootstrap_mean

ROLES = (("bridge", "distractor"), ("answer", "swap_answer"))
BANDS = {"32-48": (32, 48), "24-40": (24, 40), "0-4": (0, 4)}  # 0-4: lexical baseline, before much is computed
N_BOOT, SEED = 10000, 0


def cue_positions(tokens: list[str], cue: str) -> list[int]:
    """Token indices of `cue` inside the prompt the tokens spell, without position 0 and the last two positions
    (part B's `cue` regime: the cue phrase among the earlier words)."""
    text = "".join(tokens)
    start = text.index(cue)
    end, pos, out = start + len(cue), 0, []
    for i, t in enumerate(tokens):
        if pos < end and pos + len(t) > start:
            out.append(i)
        pos += len(t)
    last = len(tokens) - 1
    return [i for i in out if 1 <= i <= last - 2]


def band_share(grid: np.ndarray, rows: list[int], col: int) -> float:
    """Share of the band's layer rows with rank 1 at one position (grid: [layers, positions] pool ranks)."""
    return float(np.mean(grid[rows, col] == 1))


def analyze_cue(grids: dict, meta: list[dict], layers: list[int], cues: dict[str, str]) -> dict[str, Any]:
    eligible = [m for m in meta if m["status"] == "eligible" and m["name"] in cues and m["name"] in grids]
    out: dict[str, Any] = {"n": len(eligible), "bands": {}, "by_layer": {}}
    per_q: dict[str, Any] = {}
    for m in eligible:
        cue = cue_positions(m["tokens"], cues[m["name"]])
        noncue = [i for i in range(1, len(m["tokens"]) - 2) if i not in cue]
        per_q[m["name"]] = {"cue": cue, "noncue": noncue, "n_cue_tokens": len(cue)}
    for band, (lo, hi) in BANDS.items():
        rows = [i for i, layer in enumerate(layers) if lo <= layer <= hi]
        res: dict[str, Any] = {}
        for role, control in ROLES:
            for word in (role, control):
                vals: dict[str, list[float]] = {"cue": [], "noncue": [], "-1": [], "0": []}
                for m in eligible:
                    g = grids[m["name"]].get(f"{word}_pool")
                    cue = per_q[m["name"]]["cue"]
                    if g is None or not cue:
                        continue
                    last = len(m["tokens"]) - 1
                    vals["cue"].append(max(band_share(g, rows, c) for c in cue))
                    if per_q[m["name"]]["noncue"]:
                        vals["noncue"].append(max(band_share(g, rows, c) for c in per_q[m["name"]]["noncue"]))
                    vals["-1"].append(band_share(g, rows, last - 1))
                    vals["0"].append(band_share(g, rows, last))
                res[word] = {k: _ci(bootstrap_mean(v, N_BOOT, SEED)) | {"n": len(v)} for k, v in vals.items() if v}
        out["bands"][band] = res
    for role, control in ROLES:
        for word in (role, control):
            hits = []
            for m in eligible:
                g = grids[m["name"]].get(f"{word}_pool")
                cue = per_q[m["name"]]["cue"]
                if g is not None and cue:
                    hits.append((g[:, cue] == 1).any(axis=1))
            share = np.mean(hits, axis=0)
            reached = np.flatnonzero(share >= 0.5)
            out["by_layer"][word] = {
                "share": [round(float(s), 4) for s in share],
                "max": round(float(share.max()), 4),
                "first_layer_half": int(layers[reached[0]]) if reached.size else None,
            }
    out["cue_tokens_per_question"] = {
        "median": float(np.median([q["n_cue_tokens"] for q in per_q.values()])),
        "min": min(q["n_cue_tokens"] for q in per_q.values()),
        "max": max(q["n_cue_tokens"] for q in per_q.values()),
    }
    return out


def analyze(run_dir: str | Path) -> Path:
    from .experiment import load_grids

    run_dir = Path(run_dir)
    meta = [json.loads(x) for x in (run_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    layers = json.loads((run_dir / "layers.json").read_text())
    cues = json.loads((DATA_DIR / "cue_spans.json").read_text())["cues"]
    summary = {
        "source_run": str(run_dir),
        "cue_spans": "data/cue_spans.json",
        "readers": {r: analyze_cue(load_grids(run_dir / f"grids_{r}.npz"), meta, layers[r], cues) for r in layers},
        "ci": f"95% percentile bootstrap over questions, n_boot={N_BOOT}, seed={SEED}",
    }
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-cue"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return out


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[1]))
