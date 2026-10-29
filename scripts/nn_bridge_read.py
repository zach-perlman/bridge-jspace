"""nn_bridge_read (Zach, 2026-10-29, prereg amendment 59 note 26): what the J-space shows at the bridge, from nn_readout runs.
  (b) priming with no relation asked ({P}nn_readout_v4ctl_v1: --items v4ctl --priming): per scene whose MM is v4ok, the top-1
      share over note 25's description-end window of X's remembered attribute on the closed-book naming question H1 (and the
      recognition question RG) against MM; rho = (H1 attr - H1 third) / (MM attr - MM third). >= 0.7 association, <= 0.3 the
      asked relation brings it, mixed between, unclear if the interval holds 0.3 and 0.7.
  (c) priming on cue-conflict descriptions ({P}nn_readout_v4cc_v1: --items v4cc --priming): conflict items, MP and MM pooled,
      d = remembered - cue top-1 share at the description's end. "the person" if d >= 10 with its interval above 0 and
      remembered >= 2x cue; "the description's words" if cue - remembered >= 10 with its interval above 0; else mixed. Primary
      subset: named recall right (tag known); beside: gated (v4_split ok/fail) and all.
Cluster bootstrap over bridges (people), 2000 draws, seed 0. Writes results/nn_readout/nn_bridge_read/{P}v4_n26.json.

python scripts/nn_bridge_read.py PREFIX
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts.nn_priming_read import windows  # noqa: E402

RES = ROOT / "results" / "nn_readout"


def load(run: str, win: dict):
    hits, meta = collections.defaultdict(list), {}
    for line in (RES / run / "rows.jsonl").open():
        r = json.loads(line)
        lo, hi = win[r["site"]]
        if lo <= r["layer"] <= hi:
            hits[(r["site"], r["lens"], r["id"], r["what"])].append(r["rank"] == 1)
        meta[r["id"]] = r
    return {k: 100 * sum(v) / len(v) for k, v in hits.items()}, meta


def boot(units: list, fn, seed: int = 0):
    by = collections.defaultdict(list)
    for c, u in units:
        by[c].append(u)
    keys, rng, out = sorted(by), random.Random(seed), []
    for _ in range(2000):
        v = fn([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
        if v == v:
            out.append(v)
    out.sort()
    return [round(out[int(0.025 * len(out))], 3), round(out[int(0.975 * len(out)) - 1], 3)] if out else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def uid(i: str) -> str:
    return i.split(":")[-1].split("-", 1)[1]


def main(P: str) -> None:
    win = windows(P)
    out: dict = {"prefix": P, "windows": win, "b": {}, "c": {}}
    # (b) no relation asked
    run = RES / f"{P}nn_readout_v4ctl_v1"
    if (run / "rows.jsonl").exists():
        val, meta = load(run.name, win)
        by = collections.defaultdict(dict)
        for i, r in meta.items():
            by[uid(i)][r["family"]] = i
        units = [(meta[d["MM_ok"]]["bridge"], d) for d in by.values() if "MM_ok" in d and "H1_mmok" in d]
        for lens in ("jlens", "logit"):
            g = lambda d, fam, t: val.get(("desc_end", lens, d.get(fam), t))  # noqa: E731
            rec = {"n": len(units)}
            for fam in ("MM_ok", "MP_ok", "H1_mmok", "RG_mmok"):
                for t in ("attr", "other", "third", "bridge"):
                    rec[f"{fam}/{t}"] = round(mean([g(d, fam, t) for _, d in units]), 1)
            for q in ("H1_mmok", "RG_mmok"):
                def rho(us, q=q):
                    den = mean([g(d, "MM_ok", "attr") for d in us]) - mean([g(d, "MM_ok", "third") for d in us])
                    return (mean([g(d, q, "attr") for d in us]) - mean([g(d, q, "third") for d in us])) / den if den > 0 else float("nan")
                rec[f"rho_{q[:2]}"] = round(rho([d for _, d in units]), 3)
                rec[f"rho_{q[:2]}_ci"] = boot(units, rho)
            out["b"][lens] = rec
        r, lo_hi = out["b"]["jlens"]["rho_H1"], out["b"]["jlens"]["rho_H1_ci"] or [float("nan")] * 2
        out["b"]["reading"] = ("unclear" if lo_hi[0] <= 0.3 and lo_hi[1] >= 0.7 else "association (no relation asked)" if r >= 0.7
                               else "the asked relation brings it" if r <= 0.3 else "mixed")  # fmt: skip
    # (c) cue-conflict
    run = RES / f"{P}nn_readout_v4cc_v1"
    if (run / "rows.jsonl").exists():
        val, meta = load(run.name, win)
        for lens in ("jlens", "logit"):
            for subset, keep in (("known", lambda r: r.get("known")), ("gated", lambda r: r.get("gated") in ("ok", "fail")), ("all", lambda r: True)):
                rec = {}
                for typ in ("conflict", "aligned"):
                    units = []
                    for i, r in meta.items():
                        if r["family"].endswith(typ) and keep(r):
                            rem = "attr" if r["family"].startswith("MM") else "other"
                            units.append((r["bridge"], {"rem": val.get(("desc_end", lens, i, rem)), "cue": val.get(("desc_end", lens, i, "cue")),
                                                        "third": val.get(("desc_end", lens, i, "third")), "word": r["family"][:2]}))  # fmt: skip
                    st = {"n": len(units), "n_MP": sum(u["word"] == "MP" for _, u in units)}
                    for t in ("rem", "cue", "third"):
                        st[t] = round(mean([u[t] for _, u in units]), 1)
                    if typ == "conflict" and units:
                        dfn = lambda us: mean([u["rem"] for u in us]) - mean([u["cue"] for u in us])  # noqa: E731
                        st["d"], st["d_ci"] = round(dfn([u for _, u in units]), 1), boot(units, dfn)
                        for w in ("MP", "MM"):
                            st[f"d_{w}"] = round(dfn([u for _, u in units if u["word"] == w]), 1)
                    rec[typ] = st
                out["c"][f"{subset}/{lens}"] = rec
        c = out["c"].get("known/jlens", {}).get("conflict", {})
        if c.get("d_ci"):
            d, (lo, hi) = c["d"], c["d_ci"]
            out["c"]["reading"] = ("the person" if d >= 10 and lo > 0 and c["rem"] >= 2 * c["cue"] else
                                   "the description's words" if -d >= 10 and hi < 0 else "mixed")  # fmt: skip
    d = RES / "nn_bridge_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}v4_n26.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("windows",)}), "\n(b)", json.dumps(out["b"], indent=0)[:1500], "\n(c)", json.dumps(out["c"], indent=0)[:2500])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
