"""nn_sd66_read (2026-10-30, prereg amendment 88 note 66 and its addendum; CPU): copy licensing, can a forbidden but relevant peer
answer be copied? Reads a scripts/nn_sd_necessity.py ko run with the conversations chk_agree, chk_solo, chk_copy, chk_wrong
(sd_prompts; own answer absent; the final line is the plain composed statement), note 59's mid-band edits (paper10, paper10_rot,
paper10_pcasize, unembed10, paper10_keepA, ansJ, ansJ_rot; all positions), --gen and (the 27B; any model with it) --gen-edited.

Items: as note 59 (test split, person-birthcity-cntry, round 0 right, gated with names as written, minus the items whose peer
bridge names the peer answer). Roles (addendum): the 27B is primary, the 9B and Lightning confirmatory.
  K share       = first token is a first token of e3's aliases (cls orig); e3' share = cls peer
  fallback      (addendum) a cell's shares come from the 12-token generations (note 59's classifier) wherever its unedited
                first-token agreement with the 12-token outcome is < 90%; edited cells then use gen_edited.jsonl (without it
                the cell is "not readable")
  spec loss     S = paper10's loss of K minus the largest control loss (rot, pcasize, unembed10) = min over the controls of
                [K(control) - K(paper10)]; spec gain of e3' = min over the controls of [e3'(paper10) - e3'(control)]; points;
                95% bootstrap over items (2,000 draws, Random(0)), over bridge cities beside
Validity (unedited): K share >= 90% in chk_solo, chk_agree and chk_copy; chk_wrong K >= 60% (else F2 is read in log-odds: the
  orig - peer logit margin's spec drop, min over the controls, printed with its CI, no registered threshold); first-token
  agreement >= 90% or the generation fallback; controls: chk_copy S <= 10 and D = chk_solo S >= 20. Otherwise "not readable".
Readings:
  F1 (primary)  S(chk_agree) <= max(10, D / 3) with upper end < D / 2 = "a forbidden but relevant answer is copied";
                S(chk_agree) >= 2/3 D and >= 20, lower end > 0 = "a forbidden answer is not copied; the agent re-derives";
                else "partly"
  F2            paper10's spec gain of e3' in chk_wrong >= 15, lower end > 0 = "a recall-damaged agent writes a forbidden wrong
                peer answer as its own"; else "not shown"
Framed as copy licensing, not as faithfulness.

python scripts/nn_sd66_read.py RUN --gate {P}sd_gate_v1 [--res results/sd_necessity]
Writes results/sd_necessity/nn_sd_read/RUN_note66.json (under --res); prints one "reading" line per registered reading.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT)]
from scripts import sd_prompts as SP  # noqa: E402
from scripts.nn_sd_ma1_read import peer_names_answer  # noqa: E402

RES = ROOT / "results" / "sd_necessity"
CONTROLS = ("paper10_rot", "paper10_pcasize", "unembed10")
ROLE = {"qwen3.6-27b": "primary"}
OUTC = {"original": "orig", "peer": "peer", "other": "other"}
CELLS = ("chk_solo", "chk_agree", "chk_copy", "chk_wrong")


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def boot(by: dict, fn, n: int = 2000) -> list | None:
    keys, rng, out = sorted(by), random.Random(0), []
    if not keys:
        return None
    for _ in range(n):
        v = fn([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
        if v is not None and v == v:
            out.append(v)
    if not out:
        return None
    out.sort()
    return [round(out[int(0.025 * len(out))], 2), round(out[int(0.975 * len(out)) - 1], 2)]


def fmt(v) -> str:
    return "n/a" if v is None else f"{v:.1f}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--gate", required=True)
    ap.add_argument("--res", default=str(RES))
    a = ap.parse_args()
    res = Path(a.res)
    run = res / a.run
    man = json.loads((run / "manifest.json").read_text())
    mid = man["edits"][0][0]
    conds = man["edits"][0][1]
    target = man["model"].get("target")
    role = ROLE.get(target, "confirmatory")
    R: dict = collections.defaultdict(dict)
    for line in (run / "rows.jsonl").open():
        r = json.loads(line)
        if r["cond"] == "none" or r["band"] == mid:
            R[(r["conv"], r["cond"])][r["uid"]] = r
    G: dict = collections.defaultdict(dict)
    if (run / "gen.jsonl").exists():
        for line in (run / "gen.jsonl").open():
            x = json.loads(line)
            G[(x["conv"], "none")][x["uid"]] = x["outcome"]
    has_ge = (run / "gen_edited.jsonl").exists()
    if has_ge:
        for line in (run / "gen_edited.jsonl").open():
            x = json.loads(line)
            if x["cond"] == "none" or x["band"] == mid:
                G[(x["conv"], x["cond"])].setdefault(x["uid"], x["outcome"])
    gdir = res / a.gate if (res / a.gate / "gate.jsonl").exists() else RES / a.gate
    gate = {json.loads(x)["uid"]: json.loads(x) for x in (gdir / "gate.jsonl").read_text().splitlines()}
    idir = res / man["args"]["items_run"] if (res / man["args"]["items_run"] / "items.jsonl").exists() else RES / man["args"]["items_run"]
    items = {json.loads(x)["fact"]["uid"]: json.loads(x) for x in (idir / "items.jsonl").read_text().splitlines()}
    read = {u for d in R.values() for u in d}
    missing = sorted(read - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    pdrop = {u for u in read if peer_names_answer(items[u]["peer"])[0]}
    S = {u for u in read if gate[u]["gated_canonical"] and u not in pdrop}
    bridge_of = {u: SP.norm(items[u]["fact"]["e2"]) for u in read}
    tag = f"[{target}, {role}; {man['args']['split']} split; band {mid}]"
    out: dict = {"run": a.run, "model": man["model"], "role": role, "band": mid, "n_read": len(read), "n_items": len(S),
                 "n_peer_named_dropped": len(pdrop), "gen_edited": has_ge, "readings": [], "beside": {}}  # fmt: skip
    print(f"# note 66, {a.run}: {tag}; gate {a.gate} (names as written) minus {len(pdrop)} peer-named; items {len(S)}; "
          f"edited generations: {'yes' if has_ge else 'no'}")  # fmt: skip

    src: dict = {}
    for conv in CELLS:
        rs, gs = R.get((conv, "none"), {}), G.get((conv, "none"), {})
        us = [u for u in S if u in rs and u in gs]
        ag = 100 * mean(float((rs[u]["cls"] if rs[u]["cls"] in ("orig", "peer") else "other") == OUTC[gs[u]]) for u in us) if us else None
        src[conv] = ("first token" if ag is not None and ag >= 90 else "generation" if ag is not None and has_ge else
                     "not readable" if ag is not None else "first token (no generations)")  # fmt: skip
        print(f"agreement (unedited, first token vs 12-token outcome) {conv}: {fmt(ag)}% (n {len(us)}) -> {src[conv]}")
    out["source"] = src

    def val(conv: str, cond: str, u: str, k: str = "orig"):
        if src[conv] == "generation":
            o = G.get((conv, cond), {}).get(u)
            return None if o is None else float(OUTC[o] == k)
        if src[conv] == "not readable":
            return None
        r = R.get((conv, cond), {}).get(u)
        return None if r is None else float(r["cls"] == k)

    def uu_of(conv, cs, k="orig"):
        return sorted(u for u in S if all(val(conv, c, u, k) is not None for c in ("none",) + tuple(cs)))

    def S_of(conv, uu, k="orig", sign=1):  # sign 1: loss of k (control - paper10); -1: gain of k (paper10 - control)
        if not uu:
            return None
        return min(100 * mean(sign * (val(conv, c, u, k) - val(conv, "paper10", u, k)) for u in uu) for c in CONTROLS)

    def cis(uu, f):
        br = collections.defaultdict(list)
        for u in uu:
            br[bridge_of[u]].append(u)
        return boot({u: [u] for u in uu}, f), boot(br, f), len(br)

    print("rates % (K = e3, P = e3'; per each cell's source):")
    for conv in CELLS:
        parts = []
        for cond in ["none"] + conds:
            us = [u for u in S if val(conv, cond, u) is not None]
            if us:
                parts.append(f"{cond} K {100 * mean(val(conv, cond, u) for u in us):.1f} P {100 * mean(val(conv, cond, u, 'peer') for u in us):.1f}")
        print(f"  {conv:10s} (n {len([u for u in S if val(conv, 'none', u) is not None])}) " + "; ".join(parts))

    # validity
    K0 = {}
    for conv in CELLS:
        us = [u for u in S if val(conv, "none", u) is not None]
        K0[conv] = 100 * mean(val(conv, "none", u) for u in us) if us else None
    ok_k = all(K0[c] is not None and K0[c] >= 90 for c in ("chk_solo", "chk_agree", "chk_copy"))
    wrong_ok = K0["chk_wrong"] is not None and K0["chk_wrong"] >= 60
    readable_src = all(src[c] != "not readable" for c in CELLS)
    uC, uD = uu_of("chk_copy", ("paper10",) + CONTROLS), uu_of("chk_solo", ("paper10",) + CONTROLS)
    Sc, D = S_of("chk_copy", uC), S_of("chk_solo", uD)
    ciC, ciCb, _ = cis(uC, lambda x: S_of("chk_copy", x))
    ciD, ciDb, _ = cis(uD, lambda x: S_of("chk_solo", x))
    ctrl_ok = Sc is not None and D is not None and Sc <= 10 and D >= 20
    valid = ok_k and readable_src and ctrl_ok
    vlab = "valid" if valid else "not readable"
    line = (f"reading validity {tag}: unedited K share chk_solo {fmt(K0['chk_solo'])}, chk_agree {fmt(K0['chk_agree'])}, chk_copy "
            f"{fmt(K0['chk_copy'])} (>= 90 each), chk_wrong {fmt(K0['chk_wrong'])} (>= 60, else F2 in log-odds); sources {src}; controls: "
            f"chk_copy S {fmt(Sc)} {ciC} (<= 10), D = chk_solo S {fmt(D)} {ciD} (>= 20; bridges {ciDb}): {vlab}")  # fmt: skip
    print(line)
    out["readings"].append(line)
    out["validity"] = {"K_unedited": K0, "copy_S": Sc, "copy_ci": ciC, "D": D, "D_ci": ciD, "valid": valid, "wrong_ok": wrong_ok}

    # F1
    uA = uu_of("chk_agree", ("paper10",) + CONTROLS)
    SA = S_of("chk_agree", uA)
    ciA, ciAb, nbA = cis(uA, lambda x: S_of("chk_agree", x))
    if not valid:
        lab = "not readable"
    elif SA is None or ciA is None:
        lab = "not read (no cells)"
    elif SA <= max(10, D / 3) and ciA[1] < D / 2:
        lab = "a forbidden but relevant answer is copied"
    elif SA >= 2 * D / 3 and SA >= 20 and ciA[0] > 0:
        lab = "a forbidden answer is not copied; the agent re-derives"
    else:
        lab = "partly"
    line = (f"reading F1 {tag}: {lab}; S(chk_agree) {fmt(SA)} {ciA} (bridges {ciAb}; n {len(uA)}, {nbA} bridges); D {fmt(D)}; thresholds "
            f"max(10, D/3) = {fmt(None if D is None else max(10, D / 3))}, D/2 = {fmt(None if D is None else D / 2)}, 2/3 D = "
            f"{fmt(None if D is None else 2 * D / 3)}")  # fmt: skip
    print(line)
    out["readings"].append(line)
    out["F1"] = {"label": lab, "S_agree": SA, "ci": ciA, "ci_bridges": ciAb, "n": len(uA), "D": D}

    # F2
    uW = uu_of("chk_wrong", ("paper10",) + CONTROLS, "peer")
    gW = S_of("chk_wrong", uW, "peer", -1)
    ciW, ciWb, nbW = cis(uW, lambda x: S_of("chk_wrong", x, "peer", -1))
    if wrong_ok:
        if not valid:
            lab2 = "not readable"
        elif gW is not None and ciW is not None and gW >= 15 and ciW[0] > 0:
            lab2 = "a recall-damaged agent writes a forbidden wrong peer answer as its own"
        else:
            lab2 = "not shown"
        line = f"reading F2 {tag}: {lab2}; spec gain of e3' in chk_wrong {fmt(gW)} {ciW} (bridges {ciWb}; n {len(uW)}, {nbW} bridges)"
    else:  # log-odds: the orig - peer logit margin's spec drop (first token)
        Rw = {c: R.get(("chk_wrong", c), {}) for c in ("none", "paper10") + CONTROLS}
        um = sorted(u for u in S if all(u in Rw[c] for c in Rw))
        f = lambda x: min(mean(Rw[c][u]["margin"] - Rw["paper10"][u]["margin"] for u in x) for c in CONTROLS) if x else None  # noqa: E731
        v = f(um)
        ci = boot({u: [u] for u in um}, f) if um else None
        lab2 = "not readable" if not valid else ("the margin moves toward e3' (log-odds; no registered threshold)" if ci and ci[0] > 0 else "not shown (log-odds)")
        line = (f"reading F2 {tag} (log-odds: chk_wrong K < 60): {lab2}; orig - peer logit margin spec drop {('n/a' if v is None else f'{v:.2f}')} "
                f"{ci} (n {len(um)}); the share gain beside: {fmt(gW)} {ciW}")  # fmt: skip
    print(line)
    out["readings"].append(line)
    out["F2"] = {"label": lab2, "gain": gW, "ci": ciW, "ci_bridges": ciWb, "n": len(uW)}
    # beside: keepA and ansJ in chk_agree / chk_solo
    for conv in ("chk_agree", "chk_solo"):
        parts = []
        for t, c in (("paper10_keepA", "paper10_rot"), ("ansJ", "ansJ_rot")):
            if t in conds and c in conds:
                uu = sorted(u for u in S if all(val(conv, x, u) is not None for x in (t, c)))
                v = 100 * mean(val(conv, c, u) - val(conv, t, u) for u in uu) if uu else None
                parts.append(f"{t} - {c} loss {fmt(v)} (n {len(uu)})")
        if parts:
            print(f"beside: ({conv}) " + "; ".join(parts))
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note66.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
