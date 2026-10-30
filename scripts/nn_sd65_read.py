"""nn_sd65_read (2026-10-30, prereg amendment 88 note 65 and its addendum; CPU): generate vs verify a single claim, same facts, one
knock-out. Reads a scripts/nn_sd_necessity.py ko run with the conversations solo (G), ver_true (V+), ver_false (V-), choose_tf /
choose_ft (C2, beside), the mid-band edits paper10, paper10_rot, paper10_pcasize, unembed10, ansJ, ansRe (all positions), --gen
and (the 27B; any model with it) --gen-edited.

Items: the test split's person-birthcity-cntry items, round 0 right, gated as note 59 (gated with names as written, minus the
items whose peer bridge names the peer answer: nn_sd_ma1_read.peer_names_answer); first-token collisions are not read by the
runner. Roles (addendum): the 27B is primary, the 9B and Lightning confirmatory; every model's labels are printed.
  d             = logit(" Yes") - logit(" No") at "Agent 1:" (the runner's yn_d), first token, for V+ and V-
  BA            = balanced absolute accuracy per item, ([d(V+) > 0] + [d(V-) < 0]) / 2 (threshold 0)
  G             = the K share of solo (first token, cls orig); C2 = the order-averaged pick2 truth share (e3 over e3')
  fallback      (addendum) G's and C2's shares come from the 12-token generations (note 59's classifier: original / peer /
                other) wherever the unedited first-token agreement with the 12-token outcome is < 90% in that cell; the edited
                cells then use gen_edited.jsonl (without it that cell is "not readable")
  spec loss     paper10's loss minus the largest control loss (rot, pcasize, unembed10) = min over the controls of
                [metric(control) - metric(paper10)], points; 95% bootstrap over items (2,000 draws, Random(0)), over bridge
                cities beside
Readings:
  validity  " Yes" or " No" among the top-2 tokens in >= 90% of the band's V rows (every edit and unedited; unedited beside; the
            stricter "both are the top 2" share printed beside: the builder's reading of "Yes / No in the top-2 tokens", since
            the 9B smoke put " Yes" or " No" first in 16 / 16 unedited rows with the other below rank 2), and the unedited BA >=
            85%; otherwise "the model cannot verify in this format" and nothing below is read
  V1        L_V = BA's spec loss, L_G = G's spec loss in-run. L_V <= max(10, L_G / 3) with upper end < L_G / 2 = "verification
            survives the knock-out"; L_V >= L_G / 2 with lower end > 0 = "verification needs the J-space"; else "partly"
  beside    V- accuracy alone (spec loss); paired ranking P(d(V+) > d(V-)); the yes-bias shift (mean d, paper10 - rot);
            C2; ansJ vs ansRe on BA (ansRe's energy match logged); the 12-token Yes / No classification
Caveat (registered): paper10 protects the clean top-10 outputs, here Yes / No-type tokens.

python scripts/nn_sd65_read.py RUN --gate {P}sd_gate_v1 [--res results/sd_necessity]
Writes results/sd_necessity/nn_sd_read/RUN_note65.json (under --res); prints one "reading" line per registered reading.
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


def yn_text(ans: str) -> str:
    w = SP.norm(ans).split(" ")[0] if SP.norm(ans) else ""
    return "yes" if w == "yes" else "no" if w == "no" else "other"


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
    R: dict = collections.defaultdict(dict)  # (conv, cond) -> uid -> row (the mid band and the unedited read)
    for line in (run / "rows.jsonl").open():
        r = json.loads(line)
        if r["cond"] == "none" or r["band"] == mid:
            R[(r["conv"], r["cond"])][r["uid"]] = r
    G: dict = collections.defaultdict(dict)  # (conv, cond) -> uid -> 12-token answer
    if (run / "gen.jsonl").exists():
        for line in (run / "gen.jsonl").open():
            x = json.loads(line)
            G[(x["conv"], "none")][x["uid"]] = x["answer"]
    has_ge = (run / "gen_edited.jsonl").exists()
    if has_ge:
        for line in (run / "gen_edited.jsonl").open():
            x = json.loads(line)
            if x["cond"] == "none" or x["band"] == mid:
                G[(x["conv"], x["cond"])].setdefault(x["uid"], x["answer"])
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
    print(f"# note 65, {a.run}: {tag}; gate {a.gate} (names as written) minus {len(pdrop)} peer-named; items {len(S)}; "
          f"edited generations: {'yes' if has_ge else 'no'}")  # fmt: skip

    # per-item metrics per cond
    def d(conv, cond, u):
        r = R.get((conv, cond), {}).get(u)
        return None if r is None else r["yn_d"]

    def ba(cond, u):
        p, m = d("ver_true", cond, u), d("ver_false", cond, u)
        return None if p is None or m is None else ((p > 0) + (m < 0)) / 2

    def vneg(cond, u):
        m = d("ver_false", cond, u)
        return None if m is None else float(m < 0)

    def paired(cond, u):
        p, m = d("ver_true", cond, u), d("ver_false", cond, u)
        return None if p is None or m is None else float(p > m)

    def meand(cond, u):
        p, m = d("ver_true", cond, u), d("ver_false", cond, u)
        return None if p is None or m is None else (p + m) / 2

    # G and C2: first token, or the generations where the unedited agreement is < 90%
    def agree(conv: str) -> float | None:
        rs, gs = R.get((conv, "none"), {}), G.get((conv, "none"), {})
        us = [u for u in S if u in rs and u in gs]
        if not us:
            return None
        if conv == "solo":
            ft = lambda r: r["cls"] if r["cls"] in ("orig", "peer") else "other"  # noqa: E731
        else:
            ft = lambda r: r["pick2"]  # noqa: E731
        return 100 * mean(float(ft(rs[u]) == OUTC[SP.classify(gs[u], items[u]["fact"], items[u]["peer"])]) for u in us)

    src: dict = {}
    for conv in ("solo", "choose_tf", "choose_ft"):
        ag = agree(conv)
        src[conv] = "first token" if ag is not None and ag >= 90 else ("generation" if ag is not None and has_ge else
                                                                       ("not readable" if ag is not None else "first token (no generations)"))  # fmt: skip
        print(f"agreement (unedited, first token vs 12-token outcome) {conv}: {fmt(ag)}% -> {src[conv]}")
    out["source"] = src

    def gval(cond, u):
        if src["solo"] == "generation":
            ans = G.get(("solo", cond), {}).get(u)
            return None if ans is None else float(SP.classify(ans, items[u]["fact"], items[u]["peer"]) == "original")
        r = R.get(("solo", cond), {}).get(u)
        return None if r is None else float(r["cls"] == "orig")

    def c2val(cond, u):
        v = []
        for conv in ("choose_tf", "choose_ft"):
            if src[conv] == "generation":
                ans = G.get((conv, cond), {}).get(u)
                if ans is None:
                    return None
                v.append(float(SP.classify(ans, items[u]["fact"], items[u]["peer"]) == "original"))
            else:
                r = R.get((conv, cond), {}).get(u)
                if r is None:
                    return None
                v.append(float(r["pick2"] == "orig"))
        return mean(v)

    def spec(fn, t: str, cs, uu):  # min over controls of mean(fn(c) - fn(t)), points
        if not uu:
            return None
        return min(100 * mean(fn(c, u) - fn(t, u) for u in uu) for c in cs)

    def items_for(fn, cs):
        return sorted(u for u in S if all(fn(c, u) is not None for c in ("none",) + tuple(cs)))

    def cis(uu, f):
        br = collections.defaultdict(list)
        for u in uu:
            br[bridge_of[u]].append(u)
        return boot({u: [u] for u in uu}, f), boot(br, f), len(br)

    # rates table
    print("rates % (items with the cell; BA / V+ / V- / paired from first-token d; G and C2 per their source):")
    for cond in ["none"] + conds:
        us = [u for u in S if ba(cond, u) is not None]
        gs = [u for u in S if gval(cond, u) is not None]
        cs_ = [u for u in S if c2val(cond, u) is not None]
        vrows = [r for conv in ("ver_true", "ver_false") for u, r in R.get((conv, cond), {}).items() if u in S]
        extra = ""
        if cond == "ansRe" and vrows:
            extra = f"  ansRe k {mean(r['re_k'] for r in vrows):.0f}, reached {sum(r['re_reached'] for r in vrows)}/{len(vrows)}"
        print(f"  {cond:16s} BA {fmt(None if not us else 100 * mean(ba(cond, u) for u in us))} (n {len(us)})  V+ "
              f"{fmt(None if not us else 100 * mean(float(d('ver_true', cond, u) > 0) for u in us))}  V- {fmt(None if not us else 100 * mean(vneg(cond, u) for u in us))}  "
              f"paired {fmt(None if not us else 100 * mean(paired(cond, u) for u in us))}  mean d {(mean(meand(cond, u) for u in us) if us else float('nan')):.2f}  "
              f"Y/N in top-2 {fmt(None if not vrows else 100 * mean(float(r['yn_any2']) for r in vrows))} top-1 {dict(collections.Counter(r['yn_top1'] for r in vrows))}  G {fmt(None if not gs else 100 * mean(gval(cond, u) for u in gs))} "
              f"(n {len(gs)})  C2 {fmt(None if not cs_ else 100 * mean(c2val(cond, u) for u in cs_))}{extra}")  # fmt: skip

    # validity
    vrows_all = [r for conv in ("ver_true", "ver_false") for cond in ["none"] + conds for u, r in R.get((conv, cond), {}).items() if u in S]
    vrows_0 = [r for conv in ("ver_true", "ver_false") for u, r in R.get((conv, "none"), {}).items() if u in S]
    top2 = 100 * mean(float(r["yn_any2"]) for r in vrows_all) if vrows_all else None
    top2_0 = 100 * mean(float(r["yn_any2"]) for r in vrows_0) if vrows_0 else None
    both = 100 * mean(float(r["yn_top2"]) for r in vrows_all) if vrows_all else None
    u0 = [u for u in S if ba("none", u) is not None]
    ba0 = 100 * mean(ba("none", u) for u in u0) if u0 else None
    valid = top2 is not None and top2 >= 90 and ba0 is not None and ba0 >= 85
    vlab = "valid" if valid else "the model cannot verify in this format"
    line = (f"reading validity {tag}: Yes or No among the top-2 tokens in {fmt(top2)}% of V rows (every edit; unedited {fmt(top2_0)}%; "
            f">= 90 required; both the top 2: {fmt(both)}%), unedited balanced accuracy {fmt(ba0)}% (n {len(u0)}; >= 85 required): {vlab}")  # fmt: skip
    print(line)
    out["readings"].append(line)
    out["validity"] = {"yn_any2": top2, "yn_any2_unedited": top2_0, "yn_both_top2": both, "ba_unedited": ba0, "n": len(u0), "valid": valid}

    # V1
    uV = items_for(ba, ("paper10",) + CONTROLS)
    uG = items_for(gval, ("paper10",) + CONTROLS)
    LV = spec(ba, "paper10", CONTROLS, uV)
    LG = spec(gval, "paper10", CONTROLS, uG)
    ciV, ciVb, nbV = cis(uV, lambda x: spec(ba, "paper10", CONTROLS, x))
    ciG, ciGb, _ = cis(uG, lambda x: spec(gval, "paper10", CONTROLS, x))
    if not valid:
        lab = f"not read (validity failed: {vlab})"
    elif LV is None or LG is None or ciV is None:
        lab = "not read (no cells)"
    elif LV <= max(10, LG / 3) and ciV[1] < LG / 2:
        lab = "verification survives the knock-out"
    elif LV >= LG / 2 and ciV[0] > 0:
        lab = "verification needs the J-space"
    else:
        lab = "partly"
    line = (f"reading V1 {tag}: {lab}; L_V (BA spec loss) {fmt(LV)} {ciV} (bridges {ciVb}; n {len(uV)}, {nbV} bridges); L_G (G spec "
            f"loss, {src['solo']}) {fmt(LG)} {ciG} (bridges {ciGb}; n {len(uG)}); thresholds max(10, L_G/3) = "
            f"{fmt(None if LG is None else max(10, LG / 3))}, L_G/2 = {fmt(None if LG is None else LG / 2)}")  # fmt: skip
    print(line)
    out["readings"].append(line)
    out["V1"] = {"label": lab, "L_V": LV, "ci": ciV, "ci_bridges": ciVb, "n": len(uV), "L_G": LG, "ci_G": ciG, "n_G": len(uG)}

    # beside
    bes = out["beside"]

    def bline(name, fn, t="paper10", cs=CONTROLS):
        uu = items_for(fn, (t,) + tuple(cs))
        v = spec(fn, t, cs, uu)
        ci, cib, _ = cis(uu, lambda x: spec(fn, t, cs, x))
        bes[name] = {"value": v, "ci": ci, "ci_bridges": cib, "n": len(uu)}
        return f"{name} {fmt(v)} {ci} (bridges {cib}; n {len(uu)})"

    print("beside: " + bline("V- accuracy spec loss", vneg) + "; " + bline("paired ranking spec loss", paired))
    uu = items_for(meand, ("paper10", "paper10_rot"))
    ys = None if not uu else mean(meand("paper10", u) - meand("paper10_rot", u) for u in uu)
    yci = boot({u: [u] for u in uu}, lambda x: mean(meand("paper10", u) - meand("paper10_rot", u) for u in x)) if uu else None
    bes["yes_bias_shift"] = {"value": ys, "ci": yci, "n": len(uu)}
    print(f"beside: yes-bias shift (mean d over V+ and V-, paper10 - rot, logits) {('n/a' if ys is None else f'{ys:.2f}')} {yci} (n {len(uu)})")
    print(f"beside: C2 ({src['choose_tf']} / {src['choose_ft']}) " + bline("C2 spec loss", c2val) + f"; unedited truth share "
          f"{fmt(None if not items_for(c2val, ()) else 100 * mean(c2val('none', u) for u in items_for(c2val, ())))}")  # fmt: skip
    if "ansRe" in conds and "ansJ" in conds:
        print("beside: " + bline("BA ansJ - ansRe loss", ba, "ansJ", ("ansRe",)) + "; " + bline("G ansJ - ansRe loss", gval, "ansJ", ("ansRe",)))
    if any(k[1] == "none" for k in G if k[0].startswith("ver")):
        parts = []
        for cond in ["none"] + (conds if has_ge else []):
            p_, m_ = G.get(("ver_true", cond), {}), G.get(("ver_false", cond), {})
            us = [u for u in S if u in p_ and u in m_]
            if us:
                bag = 100 * mean(((yn_text(p_[u]) == "yes") + (yn_text(m_[u]) == "no")) / 2 for u in us)
                oth = 100 * mean(((yn_text(p_[u]) == "other") + (yn_text(m_[u]) == "other")) / 2 for u in us)
                parts.append(f"{cond} BA {bag:.1f} (neither {oth:.1f})")
        ag = [float((yn_text(G[('ver_true', 'none')][u]) == "yes") == (d("ver_true", "none", u) > 0)) for u in S
              if u in G.get(("ver_true", "none"), {}) and d("ver_true", "none", u) is not None]  # fmt: skip
        print(f"beside: 12-token Yes / No classification: " + "; ".join(parts) + f"; V+ unedited agreement with sign(d) {fmt(None if not ag else 100 * mean(ag))}%")
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note65.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
