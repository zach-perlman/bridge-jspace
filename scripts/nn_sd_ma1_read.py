"""nn_sd_ma1_read (2026-10-30, prereg amendment 73 note 56, "copy or compute"; CPU): reads a scripts/nn_sd_necessity.py ko
run with the conversations instr_vis, hyp_vis, prem_vis, prem_hid and press_vis (sd_prompts.CONVS) and the mid-band edits
paper10, paper10_rot, paper10_pcasize, unembed10, paper10_keepA, ansJ, bridgeJ_ctrl, bridgeJ_peer (plus the unedited
forward), with --gen (their 12-token outcome, unedited).

Items: the run's items (note 40's known test items, round 0 right; first-token collisions are not read by the runner),
gated with names as written (amendment 66's second addendum: the gate run's gated_canonical), minus the items whose peers'
bridge e2' names the peers' answer e3' (names as written, word or 4-letter stem: sd_gate.name_check's rule applied to
(e2', e3')). Target = e3' (class peer); orig = e3; other.
  loss of e3'  = peer(none) - peer(edit); change = peer(edit) - peer(none); points, paired by item
  spec         = the test edit's minus a control's, on the same items; 95% bootstrap over bridges (2,000 draws, Random(0);
                 nn_sd_read.boot). "Every control" = paper10_rot, paper10_pcasize, unembed10.
Readings (as registered):
  C0 validity, unedited 12-token outcome: instr_vis says e3' >= 90%, hyp_vis >= 60%, and the first-token read agrees with
     the outcome >= 90%; otherwise that cell is "not readable" (agreement is printed for every conversation)
  C1 hyp_vis: paper10's spec loss of e3' >= 20 points against every control, lower end > 0: "acceptance needs the J-space"
  C2 instr_vis: paper10's loss of e3' <= max(10, C1's loss / 3): "compliance is spared" (losses as note 40's G2: paper10's
     raw loss here against paper10's raw hyp_vis loss; the spec form is printed beside)
  C3 the cell is prem_vis if its unedited e3' share (first-token read) is in [15, 85]%, else prem_hid if that one is, else
     not read; "following the peers' premise needs the J-space" if paper10's spec change in e3' has its upper end < 0
     against every control; beside, the same items' press_vis spec change (answer pressure)
  C4 (secondary) hyp_vis: keepA's net loss (minus paper10_rot's) as a share of paper10's; <= 1/3 "acceptance needs the
     answer's directions" (note 41's energy caveat); bridgeJ_peer - bridgeJ_ctrl loss (items with both spans non-empty),
     lower end > 0: "the stated premise's own directions are used"
  D1 (descriptive) the J++ readout of the agent's own bridge (hit@100 orig bridge - control bridge, --late layers,
     unedited) in instr_vis against solo (solo from note 40's run of the same model, --solo-run; same items, same prompts):
     <= 1/3 of solo "the readout tracks the agent's own computation", >= 2/3 "it tracks the words in context"
  D2 (descriptive) hyp_vis: where the e3' lost under paper10 goes (orig, ctrl or other)
  Sensitivity: C1 and C3 on the items whose orig and peer first tokens are both in that prompt's protected set (the
     runner's per-row prot); a change of sign against the full set is reported as "confounded by protection"
  Caveat (stated in the amendment): e3' is in context in instr_vis and usually the clean top token, so C2 is partly built
  in by the protection. Log-prob changes (lp_peer, nats) are printed beside, descriptive.

python scripts/nn_sd_ma1_read.py RUN --gate {P}sd_gate_v1 --late LO..HI [--solo-run {P}sd_ko_test_v1]
Writes results/sd_necessity/nn_sd_read/RUN_note56.json; prints one "reading:" line per registered reading.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT)]
from scripts import sd_prompts as SP  # noqa: E402
from scripts.nn_sd_read import RES, boot, load, mean  # noqa: E402
from scripts.sd_gate import name_check  # noqa: E402

CONTROLS = ("paper10_rot", "paper10_pcasize", "unembed10")
C3_YES = "following the peers' premise needs the J-space"
C4_YES = "acceptance needs the answer's directions"
OUT_OF = {"orig": "original", "peer": "peer"}


def peer_names_answer(peer: dict) -> tuple[bool, str]:
    """Does the peers' bridge e2' name their answer e3' (names as written: sd_gate.name_check's word / 4-letter-stem rule,
    canonical names, with e2' as the only host)?"""
    return name_check({"e1": "", "e2": peer["e2"], "e3": peer["e3"], "e2_aliases": [peer["e2"]], "e3_aliases": [peer["e3"]]}, canonical=True)


def prot_of(r: dict) -> bool | None:
    """The runner's per-row prot (both answers' first tokens protected), as a bool; None if the run has no prot."""
    p = r.get("prot")
    if p is None:
        return None
    if isinstance(p, dict):
        return all(bool(v) for v in p.values())
    if isinstance(p, (list, tuple)):
        return all(bool(v) for v in p)
    return bool(p)


def peer_span_size(r: dict) -> int:
    """bridgeJ_peer's span size as the runner logs it (np: the token count of forms(e2') minus the forms of e2, e3, e3')."""
    for k in ("np", "npeer", "n_peer_forms", "pforms_n"):
        if k in r:
            return int(r[k])
    return 1


def main(a) -> None:
    res, man, R0, bridge_of, _named, g0 = load(a)
    mid = man["edits"][0][0]
    convs = list(man["args"]["convs"])
    E = lambda c: f"{mid}/{c}"  # noqa: E731
    # items: gated (names as written) and the peer-name filter
    gate = {json.loads(x)["uid"]: json.loads(x) for x in (res / a.gate / "gate.jsonl").read_text().splitlines()}
    items = {json.loads(x)["fact"]["uid"]: json.loads(x) for x in (res / man["args"]["items_run"] / "items.jsonl").read_text().splitlines()
             if json.loads(x)["split"] == man["args"]["split"] or man["args"]["split"] == "all"}  # fmt: skip
    read = {u for d in R0.values() for u in d}
    missing = sorted(read - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    gkey = "gated_canonical" if a.name_rule == "canonical" else "gated"
    pdrop = {u for u in read if peer_names_answer(items[u]["peer"])[0]}
    S = {u for u in read if gate[u][gkey] and u not in pdrop}
    cat_n = collections.Counter(items[u]["fact"]["category"] for u in S)
    R = collections.defaultdict(dict, {k: {u: r for u, r in d.items() if u in S} for k, d in R0.items()})
    g = {c: {u: o for u, o in d.items() if u in S} for c, d in g0.items()} if g0 else {}
    out: dict = {"run": a.run, "model": man["model"], "gate_run": a.gate, "name_rule": a.name_rule, "mid": mid,
                 "n_read": len(read), "n_gated": sum(gate[u][gkey] for u in read), "n_peer_named_dropped": len(pdrop),
                 "n_gated_peer_named_dropped": sum(gate[u][gkey] for u in pdrop), "n_primary": len(S),
                 "categories": dict(cat_n), "rates": {}, "gen": {}, "effects": {}, "readings": []}  # fmt: skip

    def by_bridge(uids):
        d = collections.defaultdict(list)
        for u in uids:
            d[bridge_of[u]].append(u)
        return d

    def is_(conv, bc, u, k):
        return float(R[(conv, bc)][u]["cls"] == k)

    def common(conv, *bcs, within=None):
        s = set(R[(conv, "none")])
        for bc in bcs:
            s &= set(R[(conv, bc)])
        if within is not None:
            s &= set(within)
        return sorted(s)

    def eff(conv, bc, u, kind, cls="peer"):  # loss (none - edit) or change (edit - none) of a class, one item, points
        d = is_(conv, "none", u, cls) - is_(conv, bc, u, cls)
        return 100 * (d if kind == "loss" else -d)

    def raw(conv, bc, kind, within=None, cls="peer"):
        us = common(conv, bc, within=within)
        f = lambda uu: mean(eff(conv, bc, u, kind, cls) for u in uu) if uu else None  # noqa: E731
        return {"n": len(us), "value": round(f(us), 1) if us else None, "ci": boot(by_bridge(us), f) if us else None}

    def spec(conv, t, c, kind, within=None, need=None):
        us = common(conv, t, c, within=within)
        if need:
            us = [u for u in us if need(R[(conv, "none")][u])]
        f = lambda uu: mean(eff(conv, t, u, kind) - eff(conv, c, u, kind) for u in uu) if uu else None  # noqa: E731
        return {"n": len(us), "value": round(f(us), 1) if us else None, "ci": boot(by_bridge(us), f) if us else None}

    def lp_spec(conv, t, c, within=None):  # descriptive: change in log p(e3' first token), nats, edit minus control
        us = common(conv, t, c, within=within)
        f = lambda uu: mean((R[(conv, t)][u]["lp_peer"] - R[(conv, c)][u]["lp_peer"]) for u in uu) if uu else None  # noqa: E731
        return {"n": len(us), "value": round(f(us), 3) if us else None, "ci": boot(by_bridge(us), f) if us else None}

    def fmt(e):
        return f"{e['value']} {e['ci']} (n {e['n']})" if e and e.get("value") is not None else "n/a"

    # rates (primary items)
    bcs = ["none"] + [f"{b}/{c}" for b, cs in man["edits"] for c in cs]
    for conv in convs:
        for bc in bcs:
            rows = list(R[(conv, bc)].values())
            if rows:
                n = len(rows)
                out["rates"][f"{conv} {bc}"] = {"n": n, **{k: round(100 * sum(r["cls"] == k for r in rows) / n, 1) for k in ("orig", "peer", "ctrl", "other")},
                                                "prot": round(100 * mean(bool(prot_of(r)) for r in rows), 1) if prot_of(rows[0]) is not None else None,
                                                "edit_rel": round(mean(r.get("edit_rel", 0.0) for r in rows), 4)}  # fmt: skip
    # C0: their outcome (unedited 12 tokens) on the primary read items, and the first-token read's agreement with it
    for conv in convs:
        us = [u for u in R[(conv, "none")] if u in g.get(conv, {})]
        if not us:
            continue
        oc = collections.Counter(g[conv][u] for u in us)
        agree = mean(g[conv][u] == OUT_OF.get(R[(conv, "none")][u]["cls"], "other") for u in us)
        out["gen"][conv] = {"n": len(us), **{k: round(100 * v / len(us), 1) for k, v in oc.items()}, "first_token_agreement": round(100 * agree, 1)}
    rd = out["readings"]
    thr = {"instr_vis": 90.0, "hyp_vis": 60.0}
    readable = {}
    for conv, t in thr.items():
        v = out["gen"].get(conv)
        if not v:
            readable[conv] = False
            rd.append(f"C0 {conv}: not readable (no generation rows)")
            continue
        says, ag = v.get("peer", 0.0), v["first_token_agreement"]
        readable[conv] = says >= t and ag >= 90
        rd.append(f"C0 {conv}: {'readable' if readable[conv] else 'not readable'}; says e3' {says}% (>= {t:.0f} needed), "
                  f"first-token agreement {ag}% (>= 90 needed); n {v['n']}")  # fmt: skip
    for conv in [c for c in convs if c not in thr and c in out["gen"]]:
        v = out["gen"][conv]
        rd.append(f"C0 beside {conv}: says e3' {v.get('peer', 0.0)}%, orig {v.get('original', 0.0)}%, first-token agreement {v['first_token_agreement']}%; n {v['n']}")
    # C1: hyp_vis acceptance
    c1 = {c: spec("hyp_vis", E("paper10"), E(c), "loss") for c in CONTROLS}
    out["effects"].update({f"hyp_vis spec loss paper10-vs-{c}": v for c, v in c1.items()})
    hyp_raw = raw("hyp_vis", E("paper10"), "loss")
    out["effects"]["hyp_vis paper10 loss"] = hyp_raw
    for c in CONTROLS:
        out["effects"][f"hyp_vis {c} loss"] = raw("hyp_vis", E(c), "loss")
    c1_ok = all(v["value"] is not None and v["value"] >= 20 and v["ci"] and v["ci"][0] > 0 for v in c1.values())
    c1_lab = ("not readable (C0)" if not readable["hyp_vis"] else "acceptance needs the J-space" if c1_ok else "not shown")
    rd.append(f"C1 hyp_vis: {c1_lab}; paper10 spec loss of e3' vs " + ", ".join(f"{c} {fmt(v)}" for c, v in c1.items())
              + f"; paper10 raw loss {fmt(hyp_raw)}")  # fmt: skip
    # C2: instr_vis compliance spared
    ins_raw = raw("instr_vis", E("paper10"), "loss")
    out["effects"]["instr_vis paper10 loss"] = ins_raw
    c2s = {c: spec("instr_vis", E("paper10"), E(c), "loss") for c in CONTROLS}
    out["effects"].update({f"instr_vis spec loss paper10-vs-{c}": v for c, v in c2s.items()})
    if ins_raw["value"] is None or hyp_raw["value"] is None:
        c2_lab = "not read (no rows)"
    else:
        bound = max(10.0, hyp_raw["value"] / 3)
        c2_lab = ("not readable (C0)" if not readable["instr_vis"] else
                  "compliance is spared" if ins_raw["value"] <= bound else "compliance is not spared")  # fmt: skip
        c2_lab += f"; paper10 loss of e3' {fmt(ins_raw)} vs bound max(10, {hyp_raw['value']} / 3) = {round(bound, 1)}"
    spec_min = min((v["value"] for v in c1.values() if v["value"] is not None), default=None)
    rd.append(f"C2 instr_vis: {c2_lab}; beside, spec loss vs " + ", ".join(f"{c} {fmt(v)}" for c, v in c2s.items())
              + f" (against C1's smallest spec loss / 3 = {None if spec_min is None else round(spec_min / 3, 1)}); caveat: e3' is in context "
              "and usually the clean top token, so C2 is partly built in by the protection")  # fmt: skip
    # C3: premise pressure
    cell = None
    for conv in ("prem_vis", "prem_hid"):
        r = out["rates"].get(f"{conv} none")
        if r and 15 <= r["peer"] <= 85:
            cell = conv
            break
    shares = {c: out["rates"].get(f"{c} none", {}).get("peer") for c in ("prem_vis", "prem_hid")}
    c3 = {}
    if cell is None:
        rd.append(f"C3: not read (unedited e3' share prem_vis {shares['prem_vis']}%, prem_hid {shares['prem_hid']}%, neither in [15, 85])")
    else:
        c3 = {c: spec(cell, E("paper10"), E(c), "change") for c in CONTROLS}
        out["effects"].update({f"{cell} spec change paper10-vs-{c}": v for c, v in c3.items()})
        ok = all(v["ci"] and v["ci"][1] < 0 for v in c3.values())
        same = common(cell, E("paper10"), *[E(c) for c in CONTROLS])
        pv = {c: spec("press_vis", E("paper10"), E(c), "change", within=same) for c in CONTROLS}
        out["effects"].update({f"press_vis (C3 items) spec change paper10-vs-{c}": v for c, v in pv.items()})
        ag = out["gen"].get(cell, {}).get("first_token_agreement")
        rd.append(f"C3 {cell} (unedited e3' share {shares[cell]}%; first-token agreement {ag}%): "
                  f"{C3_YES if ok else 'not shown'}; paper10 spec change in e3' vs "
                  + ", ".join(f"{c} {fmt(v)}" for c, v in c3.items())
                  + "; beside, answer pressure (press_vis, same items) spec change vs " + ", ".join(f"{c} {fmt(v)}" for c, v in pv.items()))  # fmt: skip
    # C4: keepA share and bridgeJ_peer - bridgeJ_ctrl (hyp_vis)
    us = common("hyp_vis", E("paper10"), E("paper10_keepA"), E("paper10_rot"))

    def share(uu):
        if not uu:
            return None
        den = mean(eff("hyp_vis", E("paper10"), u, "loss") - eff("hyp_vis", E("paper10_rot"), u, "loss") for u in uu)
        num = mean(eff("hyp_vis", E("paper10_keepA"), u, "loss") - eff("hyp_vis", E("paper10_rot"), u, "loss") for u in uu)
        return num / den if den > 0 else None

    sh = share(us)
    ci = boot(by_bridge(us), share) if us else None
    out["effects"]["hyp_vis keepA net loss share"] = {"n": len(us), "value": None if sh is None else round(sh, 3), "ci": ci}
    out["effects"]["hyp_vis spec loss keepA-vs-paper10_rot"] = spec("hyp_vis", E("paper10_keepA"), E("paper10_rot"), "loss")
    if sh is None:
        rd.append(f"C4 keepA (hyp_vis): not read (paper10's net loss <= 0); n {len(us)}")
    else:
        rd.append(f"C4 keepA (hyp_vis): {C4_YES if sh <= 1 / 3 else 'not shown'}; keepA net loss share "
                  f"{round(sh, 3)} {ci} (n {len(us)}; net = minus paper10_rot); keepA spec loss vs paper10_rot "
                  f"{fmt(out['effects']['hyp_vis spec loss keepA-vs-paper10_rot'])}; note 41's energy caveat applies")  # fmt: skip
    need = lambda r0: r0.get("nc", 1) and peer_span_size(r0)  # noqa: E731
    bp = spec("hyp_vis", E("bridgeJ_peer"), E("bridgeJ_ctrl"), "loss", need=need)
    out["effects"]["hyp_vis spec loss bridgeJ_peer-vs-bridgeJ_ctrl"] = bp
    lab = "the stated premise's own directions are used" if bp["ci"] and bp["ci"][0] > 0 else "not shown"
    beside = []
    for conv, kind in (("prem_vis", "change"), ("prem_hid", "change"), ("instr_vis", "loss"), ("press_vis", "change")):
        e = spec(conv, E("bridgeJ_peer"), E("bridgeJ_ctrl"), kind, need=need)
        out["effects"][f"{conv} spec {kind} bridgeJ_peer-vs-bridgeJ_ctrl"] = e
        beside.append(f"{conv} {kind} {fmt(e)}")
    rd.append(f"C4 bridgeJ_peer (hyp_vis): {lab}; bridgeJ_peer - bridgeJ_ctrl loss of e3' {fmt(bp)}; beside " + "; ".join(beside))
    # D1: own-bridge readout, instr_vis vs solo (unedited; J++; late layers)
    late = a.late or []
    solo_vals: dict = {}
    if a.solo_run and (res / a.solo_run / "rows.jsonl").exists():
        sman = json.loads((res / a.solo_run / "manifest.json").read_text())
        if not late and len(sman["edits"]) > 1:
            lo, hi = map(int, sman["edits"][1][0][1:].split("-"))
            late = list(range(lo, hi + 1))
        sidx = [sman["read_layers"].index(la) for la in late if la in sman["read_layers"]]
        for line in (res / a.solo_run / "rows.jsonl").open():
            r = json.loads(line)
            if r["conv"] == "solo" and r["cond"] == "none" and r["uid"] in S:
                solo_vals[r["uid"]] = hitdiff(r, sidx)
    idx = [man["read_layers"].index(la) for la in late if la in man["read_layers"]]
    out["late_layers"] = late
    ro = {}
    for conv in convs:
        for role in ("orig_bridge", "peer_bridge", "orig_answer"):
            vals = {u: hitdiff(r, idx, role) for u, r in R[(conv, "none")].items()}
            vals = {u: v for u, v in vals.items() if v is not None}
            if vals:
                ro[f"{conv} none {role}"] = {"n": len(vals), "value": round(mean(vals.values()), 3)}
            if role == "orig_bridge":
                for bc in ("paper10", "bridgeJ_peer", "bridgeJ_ctrl"):
                    v2 = {u: hitdiff(r, idx, role) for u, r in R[(conv, E(bc))].items()}
                    v2 = [v for v in v2.values() if v is not None]
                    if v2:
                        ro[f"{conv} {bc} {role}"] = {"n": len(v2), "value": round(mean(v2), 3)}
    out["readout"] = ro
    ins = {u: hitdiff(r, idx) for u, r in R[("instr_vis", "none")].items()}
    both = sorted(u for u in ins if ins[u] is not None and solo_vals.get(u) is not None)
    if not idx or not both:
        why = ("no late layers in the read layers" if not idx else "no instr_vis readout" if not any(v is not None for v in ins.values())
               else "no solo rows for these items (--solo-run)")  # fmt: skip
        rd.append(f"D1 (descriptive): not read ({why})")
    else:
        def ratio(uu):
            s = mean(solo_vals[u] for u in uu)
            return mean(ins[u] for u in uu) / s if uu and s > 0 else None

        rv, rci = ratio(both), boot(by_bridge(both), ratio)
        si, ii = mean(solo_vals[u] for u in both), mean(ins[u] for u in both)
        if rv is None:
            d1 = "not read (solo readout <= 0)"
        else:
            d1 = ("the readout tracks the agent's own computation" if rv <= 1 / 3 else "it tracks the words in context" if rv >= 2 / 3 else "between")
        out["effects"]["D1 ratio instr_vis / solo"] = {"n": len(both), "value": None if rv is None else round(rv, 3), "ci": rci,
                                                       "solo": round(si, 3), "instr_vis": round(ii, 3)}  # fmt: skip
        rd.append(f"D1 (descriptive): {d1}; own-bridge readout (J++ hit@100 orig - control bridge, layers {late[0]}-{late[-1]}, unedited) "
                  f"instr_vis {round(ii, 3)} vs solo {round(si, 3)} (note 40 run {a.solo_run}); ratio {None if rv is None else round(rv, 3)} {rci}; n {len(both)}")  # fmt: skip
    # D2: where lost e3' goes in hyp_vis
    for bc in ("paper10",) + CONTROLS:
        us2 = [u for u in common("hyp_vis", E(bc)) if R[("hyp_vis", "none")][u]["cls"] == "peer" and R[("hyp_vis", E(bc))][u]["cls"] != "peer"]
        base = sum(R[("hyp_vis", "none")][u]["cls"] == "peer" for u in common("hyp_vis", E(bc)))
        to = collections.Counter(R[("hyp_vis", E(bc))][u]["cls"] for u in us2)
        out["effects"][f"D2 hyp_vis {bc}"] = {"held_e3p": base, "lost": len(us2), **dict(to)}
        if bc == "paper10":
            n2 = len(us2)
            rd.append(f"D2 (descriptive) hyp_vis paper10: of {base} items saying e3' unedited, {n2} lose it: to orig {to['orig']}"
                      f" ({round(100 * to['orig'] / n2, 1) if n2 else None}%), other {to['other']}, ctrl {to['ctrl']}")  # fmt: skip
        else:
            rd.append(f"D2 beside hyp_vis {bc}: lose {len(us2)} of {base}: orig {to['orig']}, other {to['other']}, ctrl {to['ctrl']}")
    # sensitivity: both answers protected
    for conv, kind, ref, name in (("hyp_vis", "loss", c1, "C1"), (cell, "change", c3, "C3")):
        if conv is None:
            rd.append(f"Sensitivity {name}: not read (no C3 cell)")
            continue
        rows0 = R[(conv, "none")]
        if not rows0 or prot_of(next(iter(rows0.values()))) is None:
            rd.append(f"Sensitivity {name} ({conv}): not read (the run has no per-row prot)")
            continue
        P = [u for u, r in rows0.items() if prot_of(r)]
        sv = {c: spec(conv, E("paper10"), E(c), kind, within=P) for c in CONTROLS}
        out["effects"].update({f"protected {conv} spec {kind} paper10-vs-{c}": v for c, v in sv.items()})
        flip = [c for c in CONTROLS if sv[c]["value"] is not None and ref[c]["value"] is not None and sv[c]["value"] * ref[c]["value"] < 0]
        rd.append(f"Sensitivity {name} ({conv}, both answers protected, {len(P)} of {len(rows0)} items): "
                  f"{'confounded by protection (' + ', '.join(flip) + ')' if flip else 'same sign'}; paper10 spec {kind} vs "
                  + ", ".join(f"{c} {fmt(v)}" for c, v in sv.items()))  # fmt: skip
    # log-prob beside (descriptive)
    lp = {}
    for conv in [c for c in ("hyp_vis", "instr_vis", cell, "press_vis") if c]:
        for c in CONTROLS:
            lp[f"{conv} lp_peer paper10-vs-{c}"] = lp_spec(conv, E("paper10"), E(c))
    out["logprob"] = lp
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note56.json").write_text(json.dumps(out, indent=1) + "\n")
    # print
    print(f"# note 56 (amendment 73), {a.run}: {man['model'].get('target')}; mid band {mid}; gate {a.gate} ({gkey}); {out['n_read']} read items, "
          f"{out['n_gated']} gated, {out['n_peer_named_dropped']} dropped by the peer-name filter ({out['n_gated_peer_named_dropped']} of them gated); "
          f"primary {len(S)} items {dict(cat_n)}")  # fmt: skip
    print("\nrates (% of primary read items; top token over the whole vocabulary; prot = % both answers protected):")
    for k, v in out["rates"].items():
        print(f"  {k:36s} n {v['n']:4d}  orig {v['orig']:5.1f}  peer {v['peer']:5.1f}  ctrl {v['ctrl']:4.1f}  other {v['other']:5.1f}  prot {v['prot']}  |edit|/|h| {v['edit_rel']:.3f}")
    print("\ntheir outcome (unedited 12 greedy tokens, primary read items):")
    for k, v in out["gen"].items():
        print(f"  {k:10s} {v}")
    print("\nreadout (unedited and some edits; J++ hit@100 role - control role, late layers):")
    for k, v in ro.items():
        print(f"  {k:40s} {v['value']:+.3f} n {v['n']}")
    print("\nlog p(e3' first token), paper10 minus control (nats, descriptive):")
    for k, v in lp.items():
        print(f"  {k:48s} {fmt(v)}")
    print()
    for line in rd:
        print("reading:", line)


def hitdiff(r: dict, idx: list[int], role: str = "orig_bridge", k: int = 100) -> float | None:
    """Their statistic under J++ for one row: mean over the layers idx of hit@k(role) - hit@k(control role)."""
    if not idx:
        return None
    ctrl = {"orig_bridge": "ctrl_bridge", "peer_bridge": "ctrl_bridge", "orig_answer": "ctrl_answer", "peer_answer": "ctrl_answer"}[role]
    rk = r["ranks"]["jpp"]
    a_, c_ = rk[role], rk[ctrl]
    pairs = [(a_[i], c_[i]) for i in idx if a_[i] >= 0 and c_[i] >= 0]
    return mean(float(x < k) - float(y < k) for x, y in pairs) if pairs else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--gate", required=True, help="the gate run (scripts/sd_gate.py), {P}sd_gate_v1")
    ap.add_argument("--name-rule", choices=["literal", "canonical"], default="canonical",
                    help="canonical = names as written (amendment 66's second addendum; the primary here)")
    ap.add_argument("--late", nargs="*", type=int, default=None, help="D1's late layers (default: the solo run's second band)")
    ap.add_argument("--solo-run", default=None, help="D1: note 40's run of the same model (its unedited solo rows)")
    ap.add_argument("--res", default=str(RES))
    ap.add_argument("--drop-bridge-named", action="store_true", help="(nn_sd_read.load's option; off: as note 40's primary)")
    main(ap.parse_args())
