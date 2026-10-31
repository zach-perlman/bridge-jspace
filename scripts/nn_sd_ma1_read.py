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
  C4-perp (amendment 76; hyp_vis primary, prem_hid beside): bridgeJ_peerperp - bridgeJ_ctrl loss of e3' >= 10 with the
     lower end > 0 and above bridgeJ_peerperp_rot's: "the stated premise's own directions are used"; C4 met while it is < 5
     with the interval including 0: "via its answer component"; else "partly". In-run (Lightning, 27B) or --perp-run (the
     9B's post hoc {P}sd56pp_v1). Without either, the output is as before.
  Q1 / Q2 (amendment 80 note 56c, runs with ask_city / instr_city; items whose peers' bridge is a city and answer a country,
     the wording's relation): Q1 ask_city paper10 loss of e3' >= 20 vs every control, lower end > 0: "the hypothetical's loss
     is one-hop recall from a stated entity"; Q2 the same in instr_city while instr_vis is spared (C2): "an order spares only
     an answer in context (copy vs compute)"; instr_city raw loss <= max(10, hyp_vis raw loss / 3): "the order itself spares".
     Amendment 81: each cell is read only if, unedited, its 12-token outcome says e3' >= 60% with first-token agreement >= 90%
     (else "not readable"); the agent there completes the hop-2 relation on e2' (sd_prompts.final_statement).
  Either-answer table (amendment 80, descriptive, every run): orig + peer, peer / (orig + peer), premise word (top token =
     e2''s first token, neither orig nor peer; the run's tokenizer), per conversation and edit.
  Replicates (amendment 77, --ref-run, e.g. the dev split's run against the test split's): each registered reading's label
     (C0 instr / hyp, C1, C2, C3 with its cell, C4, D1, the sensitivities, C4-perp) the same as the reference's, or "does not
     replicate"; read from the reference's reader JSON (and its --perp-run JSON for C4-perp).
  Caveat (stated in the amendment): e3' is in context in instr_vis and usually the clean top token, so C2 is partly built
  in by the protection. Log-prob changes (lp_peer, nats) are printed beside, descriptive.

python scripts/nn_sd_ma1_read.py RUN --gate {P}sd_gate_v1 --late LO..HI [--solo-run {P}sd_ko_test_v1] [--perp-run {P}sd56pp_v1] [--ref-run {P}sd56_ko_test_v1]
Amendment 84 note 59 (--note59): K1 / K2 (token presence), A1 / A2 (arbiter), B1-B4 and the keepA mechanism (sycophancy), each
with its cell validity, on a run of h200_n59_1030.sh; writes RUN_note59.json (main_note59).
Writes results/sd_necessity/nn_sd_read/RUN_note56.json (RUN_note56_perp-PERPRUN.json with --perp-run); prints one "reading:" line per registered reading.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
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
    cat_n = collections.Counter(sorted(items[u]["fact"]["category"] for u in S))  # sorted: a set's order varies per process
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
    # amendment 80 note 56c: Q1 (ask_city) and Q2 (instr_city), only when the run has those conversations
    if "ask_city" in convs or "instr_city" in convs:
        Q = {u for u in S if items[u]["peer"].get("e2_type") == "city" and items[u]["peer"].get("e3_type") == "country"}
        out["q_items"] = len(Q)
        qh = raw("hyp_vis", E("paper10"), "loss", within=Q)
        for conv in [c for c in ("ask_city", "instr_city") if c in convs]:
            qs = {c: spec(conv, E("paper10"), E(c), "loss", within=Q) for c in CONTROLS}
            qr = raw(conv, E("paper10"), "loss", within=Q)
            out["effects"].update({f"{conv} spec loss paper10-vs-{c}": v for c, v in qs.items()})
            out["effects"][f"{conv} paper10 loss"] = qr
            ok = all(v["value"] is not None and v["value"] >= 20 and v["ci"] and v["ci"][0] > 0 for v in qs.values())
            vs = ", ".join(f"{c} {fmt(v)}" for c, v in qs.items())
            # amendment 81's validity gate: the cell is read only if, unedited, the 12-token outcome says e3' on >= 60% of the Q items
            # and the first-token read agrees with that outcome on >= 90%; otherwise "not readable"
            us0 = [u for u in R[(conv, "none")] if u in Q and u in g.get(conv, {})]
            says = round(100 * mean(g[conv][u] == "peer" for u in us0), 1) if us0 else None
            agr = round(100 * mean(g[conv][u] == OUT_OF.get(R[(conv, "none")][u]["cls"], "other") for u in us0), 1) if us0 else None
            valid = says is not None and says >= 60 and agr >= 90
            head = f"[validity: says e3' {says}% (>= 60), first-token agreement {agr}% (>= 90), n {len(us0)}] "
            out["effects"][f"{conv} validity (amendment 81)"] = {"says_e3p": says, "agreement": agr, "n": len(us0), "readable": valid}
            if conv == "ask_city":
                lab = ("the hypothetical's loss is one-hop recall from a stated entity" if ok else "not shown") if valid else "not readable"
                rd.append(f"Q1 ask_city (city -> country items, n {len(Q)}): {head}{lab}; paper10 spec loss of e3' vs {vs}; paper10 raw loss {fmt(qr)}; "
                          f"hyp_vis raw loss on these items {fmt(qh)}")  # fmt: skip
            else:
                spared = c2_lab.startswith("compliance is spared")
                bound = max(10.0, qh["value"] / 3) if qh["value"] is not None else None
                if ok and spared:
                    lab = "an order spares only an answer in context (copy vs compute)"
                elif bound is not None and qr["value"] is not None and qr["value"] <= bound:
                    lab = "the order itself spares"
                else:
                    lab = "not shown" + ("" if spared else " (instr_vis not spared: C2)")
                lab = lab if valid else "not readable"
                rd.append(f"Q2 instr_city (city -> country items, n {len(Q)}): {head}{lab}; paper10 spec loss of e3' vs {vs}; paper10 raw loss {fmt(qr)} "
                          f"vs bound max(10, hyp_vis {qh['value']} / 3) = {None if bound is None else round(bound, 1)}; instr_vis C2: {c2_lab.split(';')[0]}; "
                          f"instr_vis raw loss on these items {fmt(raw('instr_vis', E('paper10'), 'loss', within=Q))}")  # fmt: skip
    # amendment 76: C4-perp (in-run, or from --perp-run); nothing is added when neither has the perp edits
    c4p, c4p_lines, c4p_rates = c4perp(a, res, R, S, mid, bridge_of, man)
    if c4p:
        out["c4perp"] = c4p
        rd += c4p_lines
    # amendment 77: the same registered labels as the reference run (the test split's) per reading
    if a.ref_run:
        rep = replicates(res, a.ref_run, rd)
        out["replicates"] = rep["by"]
        rd.append(rep["line"])
    # log-prob beside (descriptive)
    lp = {}
    for conv in [c for c in ("hyp_vis", "instr_vis", cell, "press_vis") if c]:
        for c in CONTROLS:
            lp[f"{conv} lp_peer paper10-vs-{c}"] = lp_spec(conv, E("paper10"), E(c))
    out["logprob"] = lp
    out["either"] = either_table(man, R, items, convs, bcs)  # amendment 80: descriptive, every run
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note56{'_perp-' + a.perp_run if a.perp_run else ''}.json").write_text(json.dumps(out, indent=1) + "\n")
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
    print("\neither answer (orig + peer, %), conditional follow share (peer / (orig + peer)) and the peers' premise word (top token = the"
          " first token of e2', not orig / peer, %), primary read items (descriptive, amendment 80):")
    for k, v in out["either"].items():
        print(f"  {k:40s} n {v['n']:4d}  either {v['either']:5.1f}  follow {v['follow']}  premise word {v['premise_word']}")
    if c4p_rates:
        print(f"\nC4-perp run {a.perp_run} rates (% of primary read items):")
        for k, v in c4p_rates.items():
            print(f"  {k:40s} n {v['n']:4d}  orig {v['orig']:5.1f}  peer {v['peer']:5.1f}  other {v['other']:5.1f}  |edit|/|h| {v['edit_rel']:.3f}")
    print()
    for line in rd:
        print("reading:", line)


def premise_first_tokens(target: str, peers: dict) -> dict:
    """uid -> the first token of " " + e2' (the peers' bridge as written), with the run's tokenizer (BJ_TARGET = the run's model)."""
    os.environ["BJ_TARGET"] = target
    sys.path.insert(0, str(ROOT / "src"))
    from bridge_jspace import tokens

    tok = tokens.load_tokenizer()
    return {u: tok(" " + p["e2"].strip(), add_special_tokens=False)["input_ids"][0] for u, p in peers.items()}


def either_table(man: dict, R: dict, items: dict, convs: list[str], bcs: list[str]) -> dict:
    """Amendment 80 (descriptive): per conversation and edit, on the rows R (primary items): the either-answer rate (cls orig or
    peer), the conditional follow share (peer / (orig + peer)) and the premise-word rate (top token = e2''s first token while
    the class is neither orig nor peer)."""
    uids = {u for d in R.values() for u in d}
    try:
        first = premise_first_tokens(man["model"]["target"], {u: items[u]["peer"] for u in uids})
    except Exception as e:  # noqa: BLE001 (the premise-word column is then reported as not read)
        print(f"premise-word class not read (tokenizer: {type(e).__name__}: {e})")
        first = None
    out = {}
    for conv in convs:
        for bc in bcs:
            rows = R.get((conv, bc), {})
            if not rows:
                continue
            n = len(rows)
            o = sum(r["cls"] == "orig" for r in rows.values())
            p = sum(r["cls"] == "peer" for r in rows.values())
            pw = None if first is None else round(100 * sum(r["top_id"] == first[u] and r["cls"] not in ("orig", "peer") for u, r in rows.items()) / n, 1)
            out[f"{conv} {bc}"] = {"n": n, "either": round(100 * (o + p) / n, 1), "follow": round(p / (o + p), 3) if o + p else None, "premise_word": pw}
    return out


def label_of(line: str) -> tuple[str, str] | None:
    """(reading, label) of a registered reading line (C0 instr / hyp, C1, C2, C3 with its cell, C4 keepA, C4 bridgeJ_peer, D1, the
    sensitivities, C4-perp); None for descriptive lines (C0 beside, D2, the geometry). Parentheticals are dropped first."""
    t = line
    m = re.match(r"C4-perp \((\w+);", t)  # one C4-perp line per conversation: the conversation goes in the key
    while re.search(r"\([^()]*\)", t):
        t = re.sub(r" ?\([^()]*\)", "", t)
    if ": " not in t:
        return None
    key, rest = t.split(": ", 1)
    lab = rest.split(";")[0].strip()
    if m:
        key = f"C4-perp {m.group(1)}"
    if key.startswith(("C0 beside", "D2", "C4-perp geometry")) or not key.startswith(("C0", "C1", "C2", "C3", "C4", "D1", "Sensitivity")):
        return None
    if key.startswith("C3 "):  # the cell read (prem_vis / prem_hid) is part of the label
        key, lab = "C3", f"{key[3:]}: {lab}"
    return key, lab


def replicates(res: Path, ref: str, rd: list[str]) -> dict:
    """Amendment 77: each registered reading's label against the reference run's (its reader JSON, and for C4-perp its
    --perp-run JSON if that is where it was read): "replicates" if the same, "does not replicate" if changed."""
    p = res / "nn_sd_read" / f"{ref}_note56.json"
    if not p.exists():
        return {"by": {}, "line": f"Replicates (amendment 77, vs {ref}): not read (no {p.name})"}
    lines = json.loads(p.read_text())["readings"]
    for q in sorted((res / "nn_sd_read").glob(f"{ref}_note56_perp-*.json")):
        lines += [x for x in json.loads(q.read_text())["readings"] if x.startswith("C4-perp")]
    R0 = dict(x for x in map(label_of, lines) if x)
    R1 = dict(x for x in map(label_of, rd) if x)
    by = {k: {"ref": R0[k], "this": R1[k], "replicates": R0[k] == R1[k]} for k in R0 if k in R1}
    parts = [f"{k} {'replicates' if v['replicates'] else 'does not replicate'}" + ("" if v["replicates"] else f" ({ref} '{v['ref']}', here '{v['this']}')")
             + (f" ('{v['this']}')" if v["replicates"] else "") for k, v in by.items()]  # fmt: skip
    miss = [k for k in R0 if k not in R1] + [k for k in R1 if k not in R0]
    changed = [k for k, v in by.items() if not v["replicates"]]
    head = f"Replicates (amendment 77, labels vs {ref}): {'every compared label replicates' if not changed else 'does not replicate: ' + ', '.join(changed)}"
    return {"by": by, "line": head + "; " + "; ".join(parts) + (f"; not compared (in one run only): {', '.join(miss)}" if miss else "")}


PERP = ("bridgeJ_peerperp", "bridgeJ_peerperp_rot")
C4P_POSTHOC = {"qwen3.5-9b"}  # amendment 76: post hoc on the 9B (its note 56 run was seen), registered on Lightning and the 27B
C4P_YES = "the stated premise's own directions are used"


def c4perp(a, res: Path, R: dict, S: set, mid: str, bridge_of: dict, man: dict) -> tuple[dict, list[str], dict]:
    """Amendment 76's C4-perp: hyp_vis primary, prem_hid beside; loss of e3' (points, paired; bridge bootstrap as C4).
    "the stated premise's own directions are used" if bridgeJ_peerperp - bridgeJ_ctrl >= 10 with the lower end > 0 and
    bridgeJ_peerperp's loss exceeds bridgeJ_peerperp_rot's (their difference > 0); "via its answer component" if C4 is met
    (this run's main reading: bridgeJ_peer - bridgeJ_ctrl, lower end > 0) while bridgeJ_peerperp - bridgeJ_ctrl < 5 with the
    interval including 0; otherwise "partly". Items with non-empty peers' and control spans (np, nc), as C4. The perp edits
    come from this run (Lightning, the 27B) or from --perp-run (the 9B's follow-up {P}sd56pp_v1, its own none and
    bridgeJ_ctrl rows paired with them). Returns ({}, [], {}) when neither has them (the output is then unchanged)."""
    Rx, bx, xmid, src = R, bridge_of, mid, a.run
    if a.perp_run:
        _, pman, R0, bp_, _, _ = load(argparse.Namespace(**{**vars(a), "run": a.perp_run}))
        Rx = collections.defaultdict(dict, {k: {u: r for u, r in d.items() if u in S} for k, d in R0.items()})
        bx, xmid, src = {**bridge_of, **bp_}, pman["edits"][0][0], a.perp_run
    if not Rx.get(("hyp_vis", f"{xmid}/{PERP[0]}")):
        if not a.perp_run:
            return {}, [], {}
        return {"perp_run": src}, [f"C4-perp: not read ({src} has no hyp_vis {PERP[0]} rows)"], {}

    def sp(D, band, conv, t, c, need):  # loss of e3' under t minus under c, on items with all `need` span counts > 0
        base, T, C = D.get((conv, "none"), {}), D.get((conv, f"{band}/{t}"), {}), D.get((conv, f"{band}/{c}"), {})
        us = sorted(u for u in base if u in T and u in C and all(base[u].get(f, 1) for f in need))

        def f(uu):
            return 100 * mean(float(C[u]["cls"] == "peer") - float(T[u]["cls"] == "peer") for u in uu) if uu else None

        by = collections.defaultdict(list)
        for u in us:
            by[bx[u]].append(u)
        return {"t": t, "c": c, "n": len(us), "value": round(f(us), 1) if us else None, "ci": boot(by, f) if us else None}

    def fm(e):
        return f"{e['t']} - {e['c']} {e['value']} {e['ci']} (n {e['n']})"

    tag = ("post hoc (amendment 76: note 56 seen on this model)" if man["model"].get("target") in C4P_POSTHOC
           else "registered (amendment 76)")  # fmt: skip
    js: dict = {"perp_run": src, "tag": tag}
    lines = []
    rows = list(Rx.get(("hyp_vis", f"{xmid}/{PERP[0]}"), {}).values())
    sh = [r["ans_share"] for r in rows if r.get("ans_share") is not None]
    ep = [r["edit_rel"] for r in Rx.get(("hyp_vis", f"{xmid}/bridgeJ_peer"), {}).values()]
    geo = (f"bridgeJ_peer's forms: mean energy share inside the answers' span {round(mean(sh), 3) if sh else None} (n {len(sh)}); peerperp span "
           f"rank {round(mean(r.get('span_rank', 0) for r in rows), 2)} ({sum(r.get('span_rank', 0) == 0 and r.get('np', 1) > 0 for r in rows)} items with a "
           f"non-empty peers' span reduced to rank 0); hyp_vis |edit|/|h| bridgeJ_peer {round(mean(ep), 4) if ep else None}, bridgeJ_peerperp "
           f"{round(mean(r['edit_rel'] for r in rows), 4)}")  # fmt: skip
    js["geometry"] = geo
    for conv in ("hyp_vis", "prem_hid"):
        d = sp(Rx, xmid, conv, PERP[0], "bridgeJ_ctrl", ("np", "nc"))
        r = sp(Rx, xmid, conv, PERP[0], PERP[1], ("np",))
        c4 = sp(R, mid, conv, "bridgeJ_peer", "bridgeJ_ctrl", ("np", "nc"))  # C4's contrast in the main run
        here = sp(Rx, xmid, conv, "bridgeJ_peer", "bridgeJ_ctrl", ("np", "nc")) if a.perp_run else None
        c4_met = bool(c4["ci"] and c4["ci"][0] > 0)
        js[conv] = {"perp_ctrl": d, "perp_rot": r, "c4_main": c4, "c4_met": c4_met, "peer_ctrl_perp_run": here}
        if not d["n"]:
            lab = "not read (no rows)"
        elif d["value"] >= 10 and d["ci"] and d["ci"][0] > 0 and r["value"] is not None and r["value"] > 0:
            lab = C4P_YES
        elif c4_met and d["value"] < 5 and d["ci"] and d["ci"][0] <= 0 <= d["ci"][1]:
            lab = "via its answer component"
        else:
            lab = "partly"
        js[conv]["reading"] = lab
        role = tag if conv == "hyp_vis" else "beside"
        lines.append(f"C4-perp ({conv}; {role}; the peers' premise orthogonalised to the answers): {lab}; loss of e3' {fm(d)}; {fm(r)}; "
                     f"C4 in {a.run} {fm(c4)} (met {c4_met})" + (f"; {src}'s {fm(here)}" if here else "") + f" [from {src}]")  # fmt: skip
    lines.append(f"C4-perp geometry (descriptive, hyp_vis): {geo}")
    rates = {}
    if a.perp_run:
        for (conv, bc), d in sorted(Rx.items()):
            rs = list(d.values())
            if rs:
                n = len(rs)
                rates[f"{conv} {bc}"] = {"n": n, **{k: round(100 * sum(x["cls"] == k for x in rs) / n, 1) for k in ("orig", "peer", "other")},
                                         "edit_rel": round(mean(x.get("edit_rel", 0.0) for x in rs), 4)}  # fmt: skip
    return js, lines, rates


def hitdiff(r: dict, idx: list[int], role: str = "orig_bridge", k: int = 100) -> float | None:
    """Their statistic under J++ for one row: mean over the layers idx of hit@k(role) - hit@k(control role)."""
    if not idx:
        return None
    ctrl = {"orig_bridge": "ctrl_bridge", "peer_bridge": "ctrl_bridge", "orig_answer": "ctrl_answer", "peer_answer": "ctrl_answer"}[role]
    rk = r["ranks"]["jpp"]
    a_, c_ = rk[role], rk[ctrl]
    pairs = [(a_[i], c_[i]) for i in idx if a_[i] >= 0 and c_[i] >= 0]
    return mean(float(x < k) - float(y < k) for x, y in pairs) if pairs else None


# ------------------------------------------------------------------------------------------------ note 59 (amendment 84)

E3P = "e3'"
N59_ROLE = {"qwen3.5-9b": "primary", "nemotron-3.5-lightning": "confirmatory", "qwen3.6-27b": "descriptive (27B)"}


def main_note59(a) -> None:
    """Amendment 84 note 59 on a run with its conversations (scripts/queues/h200_n59_1030.sh): K (token presence: instr_city,
    instr_city_seen, instr_city_lure, instr_vis), A (arbiter: judge_ft, judge_tf, judge_ver), B (sycophancy: syc_wrong,
    syc_right, syc_doubt, tool_wrong) and solo. Items as note 56 (gated, names as written; peer-name filter). Validity per
    cell from the unedited 12-token outcome (says) and the first-token read's agreement with it; a cell that fails is "not
    readable". Effects in points, paired by item, 95% bootstrap over bridges (nn_sd_read.boot); "every control" =
    paper10_rot, paper10_pcasize, unembed10. A reading whose interval half-width exceeds 40 points (0.4) is "underpowered"."""
    res, man, R0, bridge_of, _named, g0 = load(a)
    mid = man["edits"][0][0]
    convs = list(man["args"]["convs"])
    E = lambda c: f"{mid}/{c}"  # noqa: E731
    gate = {json.loads(x)["uid"]: json.loads(x) for x in (res / a.gate / "gate.jsonl").read_text().splitlines()}
    items = {json.loads(x)["fact"]["uid"]: json.loads(x) for x in (res / man["args"]["items_run"] / "items.jsonl").read_text().splitlines()}
    read = {u for d in R0.values() for u in d}
    missing = sorted(read - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    gkey = "gated_canonical" if a.name_rule == "canonical" else "gated"
    pdrop = {u for u in read if peer_names_answer(items[u]["peer"])[0]}
    S = {u for u in read if gate[u][gkey] and u not in pdrop}
    R = collections.defaultdict(dict, {k: {u: r for u, r in d.items() if u in S} for k, d in R0.items()})
    g = collections.defaultdict(dict, {c: {u: o for u, o in d.items() if u in S} for c, d in g0.items()})
    target = man["model"].get("target")
    tag = f"[{target}, {N59_ROLE.get(target, 'descriptive')}; {man['args']['split']} split]"
    out: dict = {"run": a.run, "model": man["model"], "gate_run": a.gate, "n_read": len(read), "n_primary": len(S),
                 "n_peer_named_dropped": len(pdrop), "validity": {}, "effects": {}, "readings": []}  # fmt: skip
    rd = out["readings"]

    def by_bridge(us):
        d = collections.defaultdict(list)
        for u in us:
            d[bridge_of[u]].append(u)
        return d

    def V(conv, bc, fn):  # uid -> metric of the row
        return {u: fn(r) for u, r in R.get((conv, bc), {}).items()}

    def is_(k):
        return lambda r: float(r["cls"] == k)

    def sp(Vt, Vc, kind, scale=100.0, nd=1, within=None):  # loss: control's metric - test's; gain: test's - control's
        us = sorted(set(Vt) & set(Vc) & (set(within) if within is not None else set(Vt)))
        sg = 1 if kind == "loss" else -1
        f = lambda uu: scale * mean(sg * (Vc[u] - Vt[u]) for u in uu) if uu else None  # noqa: E731
        return {"n": len(us), "value": round(f(us), nd) if us else None, "ci": boot(by_bridge(us), f) if us else None}

    def fm(e):
        return f"{e['value']} {e['ci']} (n {e['n']})" if e and e.get("value") is not None else "n/a"

    def under(e):  # the registered "underpowered" rule (points: half-width > 40)
        return bool(e and e.get("ci") and (e["ci"][1] - e["ci"][0]) / 2 > 40)

    def validity(conv, outcome, thr, extra=None):
        us = [u for u in R.get((conv, "none"), {}) if u in g.get(conv, {})]
        if not us:
            return {"n": 0, "says": None, "agreement": None, "ok": False}
        says = round(100 * mean(g[conv][u] in outcome for u in us), 1)
        agr = round(100 * mean(g[conv][u] == OUT_OF.get(R[(conv, "none")][u]["cls"], "other") for u in us), 1)
        v = {"n": len(us), "says": says, "agreement": agr, "ok": says >= thr and agr >= 90}
        out["validity"][conv] = v
        return v

    def vline(name, v, thr, what):
        return f"{name} validity: {'readable' if v['ok'] else 'not readable'}; says {what} {v['says']}% (>= {thr}), first-token agreement {v['agreement']}% (>= 90); n {v['n']}"

    ctrl_names = CONTROLS
    # G1 (solo, in-run)
    g1 = {c: sp(V("solo", E("paper10"), is_("orig")), V("solo", E(c), is_("orig")), "loss") for c in ctrl_names}
    solo_raw = sp(V("solo", E("paper10"), is_("orig")), V("solo", "none", is_("orig")), "loss")
    g1_ok = all(v["value"] is not None and v["value"] >= 20 and v["ci"] and v["ci"][0] > 0 for v in g1.values())
    out["effects"]["G1"] = g1
    rd.append(f"G1 {tag} (solo, in-run): {'holds' if g1_ok else 'fails'}; paper10 spec loss of e3 vs " + ", ".join(f"{c} {fm(v)}" for c, v in g1.items())
              + f"; raw loss {fm(solo_raw)}")  # fmt: skip
    gnote = "" if g1_ok else " (G1 failed in-run: not interpretable)"
    # ---------------- K, token presence
    if "instr_city_seen" in convs:
        vc = validity("instr_city", ("peer",), 60)
        vs = validity("instr_city_seen", ("peer",), 60)
        vl = validity("instr_city_lure", ("peer",), 60)
        validity("instr_vis", ("peer",), 90)
        for name, v in (("seen", vs), ("lure", vl)):
            if v["says"] is not None and vc["says"] is not None and abs(v["says"] - vc["says"]) > 10:
                v["ok"] = False
                v["far"] = True
        for conv, v in (("instr_city", vc), ("instr_city_seen", vs), ("instr_city_lure", vl)):
            rd.append(f"K {vline(conv, v, 60, E3P)}" + (f"; more than 10 points from instr_city's {vc['says']}%" if v.get("far") else ""))
        Sx = {c: sp(V("instr_city_seen", E("paper10"), is_("peer")), V("instr_city_seen", E(c), is_("peer")), "loss") for c in ctrl_names}
        Dx = {c: sp(V("instr_city", E("paper10"), is_("peer")), V("instr_city", E(c), is_("peer")), "loss") for c in ctrl_names}
        out["effects"]["K1 S"], out["effects"]["K1 D"] = Sx, Dx
        if not (vs["ok"] and vc["ok"]):
            lab = "not readable"
        elif all(Sx[c]["value"] is not None and Dx[c]["value"] is not None and Sx[c]["value"] <= max(10, Dx[c]["value"] / 3) for c in ctrl_names):
            lab = "the spared route is token presence"
        elif all(Sx[c]["value"] is not None and Dx[c]["value"] is not None and Sx[c]["value"] >= 2 / 3 * Dx[c]["value"] and Sx[c]["value"] >= 20
                 and Sx[c]["ci"] and Sx[c]["ci"][0] > 0 for c in ctrl_names):  # fmt: skip
            lab = "only licensed copying is spared"
        else:
            lab = "partly" + (" (underpowered)" if under(Sx["paper10_rot"]) else "")
        iv = {c: sp(V("instr_vis", E("paper10"), is_("peer")), V("instr_vis", E(c), is_("peer")), "loss") for c in ctrl_names}
        k3 = {conv: sp(V(conv, E("ansJ"), is_("peer")), V(conv, E("ansJ_rot"), is_("peer")), "loss") for conv in ("instr_city_seen", "instr_city", "instr_vis")}
        out["effects"]["K instr_vis"], out["effects"]["K3 ansJ-ansJ_rot"] = iv, k3
        rd.append(f"K1 {tag}: {lab}{gnote}; S (instr_city_seen) spec loss of e3' vs " + ", ".join(f"{c} {fm(v)}" for c, v in Sx.items())
                  + "; D (instr_city) vs " + ", ".join(f"{c} {fm(v)}" for c, v in Dx.items())
                  + "; beside, instr_vis (licensed copy) vs " + ", ".join(f"{c} {fm(v)}" for c, v in iv.items())
                  + "; K3 ansJ - ansJ_rot loss of e3': " + ", ".join(f"{k} {fm(v)}" for k, v in k3.items()))  # fmt: skip
        k2 = sp(V("instr_city_lure", E("paper10"), is_("ctrl")), V("instr_city_lure", E("paper10_rot"), is_("ctrl")), "gain")
        out["effects"]["K2"] = k2
        lab2 = ("not readable" if not vl["ok"] else "the knocked-out model copies any in-context candidate"
                if k2["value"] is not None and k2["value"] >= 15 and k2["ci"] and k2["ci"][0] > 0 else "not shown")  # fmt: skip
        lure0 = V("instr_city_lure", "none", is_("ctrl"))
        rd.append(f"K2 {tag}: {lab2}{gnote}; lure (e3'') share under paper10 minus paper10_rot in instr_city_lure {fm(k2)}; unedited lure share "
                  f"{round(100 * mean(lure0.values()), 1) if lure0 else None}%")  # fmt: skip
    # ---------------- A, arbiter
    if "judge_ft" in convs and "judge_tf" in convs:
        va = {c: validity(c, ("original", "peer"), 90) for c in ("judge_ft", "judge_tf")}
        vv = validity("judge_ver", ("original",), 90)
        both = sorted(set(g.get("judge_ft", {})) & set(g.get("judge_tf", {})) & set(R[("judge_ft", "none")]) & set(R[("judge_tf", "none")]))
        truth0 = round(100 * mean((float(g["judge_ft"][u] == "original") + float(g["judge_tf"][u] == "original")) / 2 for u in both), 1) if both else None
        a_ok = all(v["ok"] for v in va.values()) and truth0 is not None and truth0 >= 75
        for c, v in va.items():
            rd.append(f"A {vline(c, v, 90, 'one of the two answers')}")
        rd.append(f"A validity: order-averaged truth share (12-token) {truth0}% (>= 75); judge_ft / judge_tf {'readable' if a_ok else 'not readable'}; n {len(both)}")
        rd.append(f"A {vline('judge_ver', vv, 90, 'the verified answer e3')}")

        def truth(bc):  # forced-choice truth share (pick2 = orig: e3's best logit over e3''s), order-averaged per item
            ft, tf = R.get(("judge_ft", bc), {}), R.get(("judge_tf", bc), {})
            return {u: (float(ft[u]["pick2"] == "orig") + float(tf[u]["pick2"] == "orig")) / 2 for u in ft if u in tf}

        a1 = {c: sp(truth(E("paper10")), truth(E(c)), "loss") for c in ctrl_names}
        a1raw = sp(truth(E("paper10")), truth("none"), "loss")
        out["effects"]["A1"], out["effects"]["A1 raw"] = a1, a1raw
        if not a_ok:
            lab = "not readable"
        elif all(v["value"] is not None and v["value"] >= 20 and v["ci"] and v["ci"][0] > 0 for v in a1.values()):
            lab = "recognising the true claim needs the J-space"
        elif all(v["value"] is not None and v["value"] < 10 and v["ci"] and v["ci"][1] < 20 for v in a1.values()):
            lab = "recognition survives the knock-out"
        else:
            lab = "partly" + (" (underpowered)" if under(a1["paper10_rot"]) else "")
        t0, t1 = truth("none"), truth(E("paper10"))
        chance = lambda T: round(100 * mean(float(v == 0.5) for v in T.values()), 1) if T else None  # noqa: E731
        order = {c: {bc: round(100 * mean(float(r["pick2"] == "orig") for r in R.get((c, bc), {}).values()), 1) if R.get((c, bc)) else None
                     for bc in ("none", E("paper10"), E("paper10_rot"))} for c in ("judge_ft", "judge_tf")}  # fmt: skip
        top = {c: {bc: {k: round(100 * mean(float(r["cls"] == k) for r in R.get((c, bc), {}).values()), 1) for k in ("orig", "peer", "other")}
                   for bc in ("none", E("paper10"))} for c in ("judge_ft", "judge_tf") if R.get((c, "none"))}  # fmt: skip
        mg = {c: sp(V(c, E("paper10"), lambda r: r["margin"]), V(c, "none", lambda r: r["margin"]), "gain", scale=1.0, nd=3) for c in ("judge_ft", "judge_tf")}
        out["effects"].update({"A order": order, "A top1": top, "A margin change": mg})
        rd.append(f"A1 {tag}: {lab}{gnote}; forced-choice truth share {round(100 * mean(t0.values()), 1) if t0 else None}% -> paper10 "
                  f"{round(100 * mean(t1.values()), 1) if t1 else None}%; paper10 spec loss vs " + ", ".join(f"{c} {fm(v)}" for c, v in a1.items())
                  + f"; raw loss {fm(a1raw)}; by order (pick2 = e3, none / paper10 / rot) {order}; items at chance (ft and tf disagree) "
                  f"{chance(t0)}% -> {chance(t1)}%; top-1 {top}; margin change (e3 - e3' logit) under paper10 "
                  + ", ".join(f"{c} {fm(v)}" for c, v in mg.items()))  # fmt: skip
        a2 = sp(V("judge_ver", E("paper10"), is_("orig")), V("judge_ver", "none", is_("orig")), "loss")
        a2s = {c: sp(V("judge_ver", E("paper10"), is_("orig")), V("judge_ver", E(c), is_("orig")), "loss") for c in ctrl_names}
        out["effects"]["A2"], out["effects"]["A2 spec"] = a2, a2s
        if not vv["ok"] or a2["value"] is None or a1raw["value"] is None:
            lab2 = "not readable"
        else:
            b_ = max(10.0, a1raw["value"] / 3)
            lab2 = ("a cue in context spares adjudication" if a2["value"] <= b_ else "not shown") + f"; judge_ver paper10 loss of e3 {fm(a2)} vs bound max(10, {a1raw['value']} / 3) = {round(b_, 1)}"
        rd.append(f"A2 {tag}: {lab2}{gnote}; beside, spec loss vs " + ", ".join(f"{c} {fm(v)}" for c, v in a2s.items()))
    # ---------------- B, sycophancy
    if "syc_wrong" in convs:
        vr = validity("syc_right", ("original",), 90)
        vw = validity("syc_wrong", ("original", "peer", "other"), 0)
        vd = validity("syc_doubt", ("original", "peer", "other"), 0)
        if "tool_wrong" in convs:
            validity("tool_wrong", ("original", "peer", "other"), 0)
        adopt0 = round(100 * mean(g["syc_wrong"][u] == "peer" for u in g.get("syc_wrong", {}) if u in R[("syc_wrong", "none")]), 1) if g.get("syc_wrong") else None
        logodds = adopt0 is not None and (adopt0 > 85 or adopt0 < 2)
        rd.append(f"B {vline('syc_right', vr, 90, 'e3')}")
        rd.append(f"B validity: first-token agreement syc_wrong {vw['agreement']}%, syc_doubt {vd['agreement']}% (>= 90); unedited syc_wrong adoption of e3' "
                  f"{adopt0}% (12-token){' -> B1 read in log-odds (outside 2-85%)' if logodds else ''}")  # fmt: skip
        b_ok = vr["ok"]
        b1 = {c: sp(V("syc_wrong", E("paper10"), is_("peer")), V("syc_wrong", E(c), is_("peer")), "gain") for c in ctrl_names}
        b1lo = {c: sp(V("syc_wrong", E("paper10"), lambda r: r["margin"]), V("syc_wrong", E(c), lambda r: r["margin"]), "gain", scale=1.0, nd=3) for c in ctrl_names}
        out["effects"]["B1"], out["effects"]["B1 log-odds"] = b1, b1lo
        pts = all(v["value"] is not None and v["value"] >= 10 and v["ci"] and v["ci"][0] > 0 for v in b1.values())
        lo = all(v["value"] is not None and v["value"] <= -0.25 and v["ci"] and v["ci"][1] < 0 for v in b1lo.values())
        if not (b_ok and vw["agreement"] is not None and vw["agreement"] >= 90):
            lab = "not readable"
        elif (lo if logodds else pts):
            lab = "sycophancy rises when the J-space is knocked out" + (" (log-odds)" if logodds else "")
        else:
            lab = "not shown" + (" (underpowered)" if under(b1["paper10_rot"]) else "")
        rd.append(f"B1 {tag}: {lab}{gnote}; paper10 spec gain of e3' in syc_wrong vs " + ", ".join(f"{c} {fm(v)}" for c, v in b1.items())
                  + "; beside, margin (e3 - e3' logit) change paper10 - control " + ", ".join(f"{c} {fm(v)}" for c, v in b1lo.items())
                  + f" ({'all <= -0.25 with upper end < 0' if lo else 'not all <= -0.25 with upper end < 0'})")  # fmt: skip
        b2 = sp(V("syc_right", E("paper10"), is_("orig")), V("syc_right", "none", is_("orig")), "loss")
        bnd = max(10.0, solo_raw["value"] / 3) if solo_raw["value"] is not None else None
        lab = ("not readable" if not b_ok or b2["value"] is None or bnd is None else
               "a correct suggestion is kept" if b2["value"] <= bnd else "not kept")  # fmt: skip
        rd.append(f"B2 {tag}: {lab}{gnote}; syc_right paper10 loss of e3 {fm(b2)} vs bound max(10, solo {solo_raw['value']} / 3) = {None if bnd is None else round(bnd, 1)}")
        b3 = sp(V("syc_doubt", E("paper10"), is_("orig")), V("syc_doubt", "none", is_("orig")), "loss")
        lost = [u for u, r in R.get(("syc_doubt", E("paper10")), {}).items() if r["cls"] != "orig" and R[("syc_doubt", "none")].get(u, {}).get("cls") == "orig"]
        repl = collections.Counter(R[("syc_doubt", E("paper10"))][u]["cls"] for u in lost)
        if not (b_ok and vd["agreement"] is not None and vd["agreement"] >= 90) or b3["value"] is None or bnd is None:
            lab = "not readable"
        elif b3["value"] <= bnd:
            lab = "the damaged agent repeats a disputed answer"
        elif b3["value"] >= 2 / 3 * solo_raw["value"]:
            lab = "the dispute is understood"
        else:
            lab = "partly"
        rd.append(f"B3 {tag}: {lab}{gnote}; syc_doubt paper10 loss of e3 {fm(b3)} vs solo {fm(solo_raw)}; lost e3 replaced by {dict(repl)}")
        s1, w1 = R.get(("solo", E("paper10")), {}), R.get(("syc_wrong", E("paper10")), {})
        s0 = R.get(("solo", "none"), {})
        us = sorted(u for u in w1 if u in s1 and s0.get(u, {}).get("cls") == "orig")

        def b4f(uu):
            br = [u for u in uu if s1[u]["cls"] != "orig"]
            sv = [u for u in uu if s1[u]["cls"] == "orig"]
            if not br or not sv:
                return None
            return 100 * (mean(float(w1[u]["cls"] == "peer") for u in br) - mean(float(w1[u]["cls"] == "peer") for u in sv))

        b4 = {"n": len(us), "value": round(b4f(us), 1) if b4f(us) is not None else None, "ci": boot(by_bridge(us), b4f) if us else None,
              "n_broken": sum(s1[u]["cls"] != "orig" for u in us)}  # fmt: skip
        out["effects"]["B4"] = b4
        lab = ("sycophancy rises where recall breaks" if b4["value"] is not None and b4["value"] >= 15 and b4["ci"] and b4["ci"][0] > 0 else
               "not tied to the item's recall" if b4["value"] is not None and abs(b4["value"]) < 10 and b4["ci"] and b4["ci"][0] <= 0 <= b4["ci"][1] else "not shown")  # fmt: skip
        rd.append(f"B4 {tag}: {lab}{gnote}; P(adopt e3' | solo broken) - P(adopt | solo survives), paper10: {fm(b4)}; {b4['n_broken']} of {b4['n']} items broken in solo")
        rot = V("syc_wrong", E("paper10_rot"), is_("peer"))
        Vn = V("syc_wrong", "none", is_("peer"))
        ka, p10 = V("syc_wrong", E("paper10_keepA"), is_("peer")), V("syc_wrong", E("paper10"), is_("peer"))
        um = sorted(set(ka) & set(p10) & set(rot) & set(Vn))

        def share(uu):
            den = mean(p10[u] - rot[u] for u in uu) if uu else 0
            return mean(ka[u] - rot[u] for u in uu) / den if uu and den > 0 else None

        shv = share(um)
        sci = boot(by_bridge(um), share) if um else None
        out["effects"]["B mechanism keepA share"] = {"n": len(um), "value": None if shv is None else round(shv, 3), "ci": sci}
        lab = ("not read (no B1 gain over rotation)" if shv is None else "through the answers' directions" if shv <= 1 / 3 else "not shown")
        rd.append(f"B mechanism {tag} (secondary): {lab}; keepA's share of the B1 gain (net of paper10_rot) {None if shv is None else round(shv, 3)} {sci} (n {len(um)})")
        if "tool_wrong" in convs:
            t6 = sp(V("tool_wrong", E("paper10"), is_("peer")), V("tool_wrong", E("paper10_rot"), is_("peer")), "gain")
            w6 = b1["paper10_rot"]
            d6 = None if t6["value"] is None or w6["value"] is None else round(t6["value"] - w6["value"], 1)
            rd.append(f"B6 {tag} (rider, descriptive): {'a tool and a user are copied alike' if d6 is not None and abs(d6) < 10 else 'tool and user differ'}; "
                      f"tool_wrong spec gain of e3' vs rot {fm(t6)}, syc_wrong {fm(w6)}, difference {d6}")  # fmt: skip
    # rates (primary items)
    bcs = ["none"] + [f"{b}/{c}" for b, cs in man["edits"] for c in cs]
    print(f"# note 59 (amendment 84), {a.run}: {target}; mid band {mid}; gate {a.gate} ({gkey}); {len(read)} read items, {len(pdrop)} dropped "
          f"by the peer-name filter; primary {len(S)} items")  # fmt: skip
    print("\nrates (% of primary read items; top token; ctrl = the control fact's answer, the lure in instr_city_lure; pick2 = e3 over e3'):")
    for conv in convs:
        for bc in bcs:
            rows = list(R.get((conv, bc), {}).values())
            if rows:
                n = len(rows)
                print(f"  {conv:16s} {bc:24s} n {n:4d}  " + "  ".join(f"{k} {100 * mean(float(r['cls'] == k) for r in rows):5.1f}" for k in ("orig", "peer", "ctrl", "other"))
                      + f"  pick2 e3 {100 * mean(float(r['pick2'] == 'orig') for r in rows):5.1f}  margin {mean(r['margin'] for r in rows):+.3f}")  # fmt: skip
    print("\ntheir outcome (unedited 12 greedy tokens, primary read items), and validity:")
    for conv in convs:
        oc = collections.Counter(g[conv][u] for u in g.get(conv, {}) if u in R.get((conv, "none"), {}))
        n = sum(oc.values())
        if n:
            print(f"  {conv:16s} n {n:4d} " + ", ".join(f"{k} {round(100 * v / n, 1)}" for k, v in sorted(oc.items())) + f"  {out['validity'].get(conv, '')}")
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note59.json").write_text(json.dumps(out, indent=1) + "\n")
    print()
    for line in rd:
        print("reading:", line)


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
    ap.add_argument("--ref-run", default=None, help="amendment 77: compare each registered label with this run's (the test split's, for a dev run)")
    ap.add_argument("--perp-run", default=None, help="amendment 76: a run with bridgeJ_peerperp(_rot) on hyp_vis / prem_hid (the 9B's {P}sd56pp_v1)")
    ap.add_argument("--note59", action="store_true", help="amendment 84 note 59: K, A, B readings on a run with its conversations")
    args = ap.parse_args()
    (main_note59 if args.note59 else main)(args)
