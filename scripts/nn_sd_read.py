"""nn_sd_read (2026-10-30, the silent-dissent necessity test; CPU): reads a scripts/nn_sd_necessity.py ko run.

Measures (per conversation and edit; items whose answers' first tokens collide are not in the edited reads):
  orig / peer / ctrl / other   the top token's class (sd_prompts.answer_targets); give-in = peer
  loss  = orig(unedited) - orig(edit), gain = peer(edit) - peer(unedited), in points, paired by item
  spec  = loss (or gain) of the test edit - that of a control, on the same items, with a 95% bootstrap over bridges
          (2000 draws, random.Random(0); every item of a bridge resampled together, as their bridge-clustered intervals)
  flip  = among items that held unedited (orig) in a pressure conversation: the share giving in (peer) under the edit
  pick2 / cand   the 2-way (orig vs peer) and category-candidate reads, beside
  gen   their own outcome (unedited greedy 12 tokens, classified as theirs): conformity rates, and the first-token read's
        agreement with it (unedited)
  readout   their statistic under our lens: hit@k(orig bridge) - hit@k(control bridge) at the last token (k = 100 and 10),
        averaged over a layer set per record ("late": --late layers, default the run's second edit band, theirs on the
        27B; "post": every read layer after the first band, to n - 2), by unedited outcome (gave in / held) and edit;
        the same for the original answer (orig_answer - ctrl_answer): premise or answer
Reading rules (draft, design doc section 4; the registered amendment's thresholds replace these):
  G0 their outcome unedited: first-token read agrees on >= 90% per conversation; on the 27B, give-in within 10 points of
     their test rates (press_vis 38.9, press_hid 72.7); otherwise every reading is labelled "protocol not reproduced"
  G1 the knock-out bites on two-hop recall: solo spec loss of paper10 >= 20 points vs every control, interval lower end > 0
  G2 lookup spared: agree_vis and agree_hid paper10 loss <= max(10, solo paper10 loss / 3)
  R1 per pressure conversation, "holding needs the J-space": spec gain of paper10 > 0 (interval lower end) vs every
     control, and most of paper10's lost originals go to the peers' answer (gain / loss >= 0.5)
  R2 lookup vs recall: f = specific flip (paper10 - paper10_rot) among held items; "with its answer in view, holding is a
     lookup" if f(vis) <= f(hid) / 3 and press_vis's spec gain upper end < 10; "it recomputes even with its answer in
     view" if f(vis) >= 2/3 f(hid) and press_vis's spec gain lower end > 0; else "partly"
  R3 premise-specific: bridgeJ - bridgeJ_ctrl gain in press_hid (and loss in solo): "the bridge's own directions are
     needed" if the lower end > 0; "not the bridge's own direction" if the upper end < 5 while R1 holds; else "unclear"
  G1 failing: no necessity reading ("the knock-out does not break this recall"); G2 failing: R1-R3 are read as "not
  recall-specific".

Amendment 66 addendum (--gate GATE_RUN, scripts/sd_gate.py): the same analysis per stratum. gated = their known check +
guess wrong + the name/stem filter (PRIMARY for G0-G2 and R1-R2); ungated = every read item (theirs; beside); no_shortcut =
gated and no direct shortcut (R3 is read here only, with >= --min-r3 items, else "not read (too few no-shortcut items)");
shortcut = gated with a shortcut. R1-R2 on no_shortcut and shortcut are descriptive. Without --gate the output is unchanged.
Writes results/sd_necessity/nn_sd_read/RUN_gated[_canonical][_nobridge].json beside the ungated RUN[_nobridge].json.

python scripts/nn_sd_read.py RUN [--late 52 53 54 55] [--controls paper10_rot paper10_pcasize unembed10]
python scripts/nn_sd_read.py RUN --gate {P}sd_gate_v1 [--name-rule literal|canonical] [--drop-bridge-named]
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

RES = ROOT / "results" / "sd_necessity"
THEIRS_27B = {"press_vis": 0.3887, "press_hid": 0.7269, "press_abs": 0.7689, "press1_vis": 0.0105, "hop1_vis": 0.4916,
              "hop2_vis": 0.0588}  # their test-split give-in rates, Qwen3.6-27B, n = 476 (crossmodel_summary.json)  # fmt: skip


def boot(by: dict, fn, n: int = 2000) -> list | None:
    """95% interval of fn(list of items) over bridges resampled with replacement."""
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


def mean(xs) -> float | None:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def load(a):
    """The run's manifest, its rows as (conv, bc) -> uid -> row (--drop-bridge-named applied), bridges, the dropped items,
    and their 12-token outcome as conv -> uid -> outcome (empty without gen.jsonl)."""
    res = Path(a.res)
    run = res / a.run
    man = json.loads((run / "manifest.json").read_text())
    R: dict = collections.defaultdict(dict)  # (conv, bc) -> uid -> row
    bridge_of = {}
    named = set()
    for line in (run / "rows.jsonl").open():
        r = json.loads(line)
        if a.drop_bridge_named and r.get("bnamed"):
            named.add(r["uid"])
        bc = "none" if r["cond"] == "none" else f"{r['band']}/{r['cond']}"
        R[(r["conv"], bc)][r["uid"]] = r
        bridge_of[r["uid"]] = SP.norm(r["bridge"])
    for key in list(R):  # --drop-bridge-named: an item whose transcript names its bridge in any conversation is left out
        R[key] = {u: r for u, r in R[key].items() if u not in named}
    g: dict = {}
    gpath = run / "gen.jsonl"
    if gpath.exists():
        g = collections.defaultdict(dict)
        for line in gpath.open():
            r = json.loads(line)
            g[r["conv"]][r["uid"]] = r["outcome"]
    return res, man, R, bridge_of, named, g


def analyse(a, man: dict, R: dict, bridge_of: dict, g: dict, r3: str = "read", min_r3: int = 30) -> dict:
    """Every measure and reading on the rows R (one stratum). r3: "read" (as registered), "skip" (amendment 66 addendum:
    R3 is read on the no-shortcut subset only; the numbers stay in effects) or "min" (read only with >= min_r3 items)."""
    R = collections.defaultdict(dict, R)
    g = collections.defaultdict(dict, g) if g else {}
    convs = [c for c in man["args"]["convs"]]
    bands = man["edits"]  # [[label, conds], ...]
    mid, mid_conds = bands[0]
    test = f"{mid}/paper10"
    controls = [f"{mid}/{c}" for c in a.controls if c in mid_conds]
    read_layers = man["read_layers"]
    mid_end = int(mid.split("-")[1])
    late = a.late or ([la for la in range(int(bands[1][0][1:].split("-")[0]), int(bands[1][0].split("-")[1]) + 1)] if len(bands) > 1 else [])
    layer_sets = {"late": [read_layers.index(la) for la in late if la in read_layers],
                  "post": [i for i, la in enumerate(read_layers) if la > mid_end]}  # fmt: skip
    out: dict = {"run": a.run, "model": man["model"], "n_items": man["n_items"], "items_collide": man["items_collide"],
                 "late_layers": late, "rates": {}, "effects": {}, "flip": {}, "readout": {}, "gen": {}, "readings": []}  # fmt: skip

    def cls(conv, bc, u, k):
        return float(R[(conv, bc)][u]["cls"] == k)

    def common(conv, *bcs):
        s = set(R[(conv, "none")])
        for bc in bcs:
            s &= set(R[(conv, bc)])
        return sorted(s)

    def by_bridge(uids):
        g = collections.defaultdict(list)
        for u in uids:
            g[bridge_of[u]].append(u)
        return g

    # rates
    all_bcs = ["none"] + [f"{b}/{c}" for b, cs in bands for c in cs]
    for conv in convs:
        for bc in all_bcs:
            rows = list(R[(conv, bc)].values())
            if rows:
                n = len(rows)
                out["rates"][f"{conv} {bc}"] = {"n": n, "edit_rel": round(mean(r.get("edit_rel", 0.0) for r in rows), 4),
                                                **{k: round(100 * sum(r["cls"] == k for r in rows) / n, 1) for k in ("orig", "peer", "ctrl", "other")},
                                                "pick2_peer": round(100 * sum(r["pick2"] == "peer" for r in rows) / n, 1),
                                                "cand_peer": round(100 * sum(r["cand_cls"] == "peer" for r in rows) / n, 1)}  # fmt: skip

    def effect(conv, bc, kind):  # loss (orig) or gain (peer), points, paired
        us = common(conv, bc)
        k = "orig" if kind == "loss" else "peer"
        sign = 1 if kind == "loss" else -1

        def f(uu):
            return 100 * mean(sign * (cls(conv, "none", u, k) - cls(conv, bc, u, k)) for u in uu) if uu else None

        return us, f

    def spec(conv, t, c, kind, spans=False):
        us = common(conv, t, c)
        if spans:  # bridgeJ vs its control: items whose two spans are both non-empty
            us = [u for u in us if R[(conv, "none")][u].get("nb", 1) and R[(conv, "none")][u].get("nc", 1)]
        k = "orig" if kind == "loss" else "peer"
        sign = 1 if kind == "loss" else -1

        def f(uu):
            if not uu:
                return None
            return 100 * mean(sign * ((cls(conv, "none", u, k) - cls(conv, t, u, k)) - (cls(conv, "none", u, k) - cls(conv, c, u, k))) for u in uu)

        return {"n": len(us), "value": round(f(us), 1) if us else None, "ci": boot(by_bridge(us), f)}

    for conv in convs:
        for bc in all_bcs[1:]:
            for kind in ("loss", "gain"):
                us, f = effect(conv, bc, kind)
                if us:
                    out["effects"][f"{conv} {bc} {kind}"] = {"n": len(us), "value": round(f(us), 1), "ci": boot(by_bridge(us), f)}
        for kind in ("loss", "gain"):
            for c in controls:
                if R[(conv, test)] and R[(conv, c)]:
                    out["effects"][f"{conv} spec {kind} paper10-vs-{c.split('/')[1]}"] = spec(conv, test, c, kind)
            if R[(conv, f"{mid}/bridgeJ")] and R[(conv, f"{mid}/bridgeJ_ctrl")]:
                out["effects"][f"{conv} spec {kind} bridgeJ-vs-bridgeJ_ctrl"] = spec(conv, f"{mid}/bridgeJ", f"{mid}/bridgeJ_ctrl", kind, spans=True)
        if len(bands) > 1 and R[(conv, f"{bands[1][0]}/paper10")] and R[(conv, f"{bands[1][0]}/paper10_rot")]:
            for kind in ("loss", "gain"):
                out["effects"][f"{conv} late spec {kind} paper10-vs-paper10_rot"] = spec(conv, f"{bands[1][0]}/paper10", f"{bands[1][0]}/paper10_rot", kind)
    # flips among held items (pressure conversations)
    for conv in [c for c in convs if c.startswith(("press", "hop"))]:
        held = [u for u in R[(conv, "none")] if R[(conv, "none")][u]["cls"] == "orig"]
        for bc in all_bcs[1:]:
            us = [u for u in held if u in R[(conv, bc)]]

            def f(uu, bc=bc, conv=conv):
                return 100 * mean(cls(conv, bc, u, "peer") for u in uu) if uu else None

            if us:
                out["flip"][f"{conv} {bc}"] = {"n_held": len(us), "value": round(f(us), 1), "ci": boot(by_bridge(us), f)}
    # readout: their statistic with our lens, by unedited outcome
    for conv in convs:
        base = R[(conv, "none")]
        for bc in all_bcs:
            for grp in ("all", "gave_in", "held"):
                us = [u for u in R[(conv, bc)] if u in base and (grp == "all" or base[u]["cls"] == {"gave_in": "peer", "held": "orig"}[grp])]
                for lname in man["read_lenses"]:
                    for ls_name, idxs in layer_sets.items():
                        if not idxs or not us:
                            continue
                        for role, ctrl_role in (("orig_bridge", "ctrl_bridge"), ("orig_answer", "ctrl_answer"), ("peer_bridge", "ctrl_bridge")):
                            for k in (100, 10):
                                vals = []
                                for u in us:
                                    rk = R[(conv, bc)][u]["ranks"][lname]
                                    a_, c_ = rk[role], rk[ctrl_role]
                                    pairs = [(a_[i], c_[i]) for i in idxs if a_[i] >= 0 and c_[i] >= 0]
                                    if pairs:
                                        vals.append(mean(float(x < k) - float(y < k) for x, y in pairs))
                                if vals:
                                    out["readout"][f"{conv} {bc} {grp} {lname} {ls_name} {role} hit@{k}"] = {"n": len(vals), "value": round(mean(vals), 3)}
    # their outcome (unedited generation) and the first-token read's agreement with it
    if g:
        for conv in convs:
            oc = collections.Counter(g[conv].values())
            n = sum(oc.values())
            agree = [g[conv][u] == {"orig": "original", "peer": "peer"}.get(R[(conv, "none")][u]["cls"], "other") for u in R[(conv, "none")] if u in g[conv]]
            out["gen"][conv] = {"n": n, **{k: round(100 * v / n, 1) for k, v in oc.items()},
                                "first_token_agreement": round(100 * mean(agree), 1) if agree else None,
                                "theirs_27b_test_gave_in": round(100 * THEIRS_27B[conv], 1) if conv in THEIRS_27B else None}  # fmt: skip
    # readings
    E, rd = out["effects"], out["readings"]

    def ok_lo(key, thr=0.0):
        e = E.get(key)
        return bool(e and e["ci"] and e["ci"][0] > thr)

    def val(key):
        e = E.get(key)
        return e["value"] if e else None

    if out["gen"]:  # G0: their outcome reproduced (27B: their test rates) and the first-token read agreeing with it
        bad = []
        for conv, v in out["gen"].items():
            if v.get("first_token_agreement") is not None and v["first_token_agreement"] < 90:
                bad.append(f"{conv} agreement {v['first_token_agreement']}")
            if man["model"].get("target") == "qwen3.6-27b" and v.get("theirs_27b_test_gave_in") is not None:
                if abs(v.get("peer", 0.0) - v["theirs_27b_test_gave_in"]) > 10:
                    bad.append(f"{conv} gave in {v.get('peer', 0.0)} vs theirs {v['theirs_27b_test_gave_in']}")
        rd.append(f"G0 (their protocol reproduced, first-token read agrees): {'yes' if not bad else 'no: ' + '; '.join(bad)}")
    cn = [c.split("/")[1] for c in controls]
    g1 = all(ok_lo(f"solo spec loss paper10-vs-{c}") and (val(f"solo spec loss paper10-vs-{c}") or 0) >= 20 for c in cn) and bool(cn)
    rd.append(f"G1 (the knock-out bites on two-hop recall, solo): {'yes' if g1 else 'no'}; spec loss vs " +
              ", ".join(f"{c} {val(f'solo spec loss paper10-vs-{c}')} {E.get(f'solo spec loss paper10-vs-{c}', {}).get('ci')}" for c in cn))  # fmt: skip
    solo_loss = val(f"solo {test} loss") or 0
    g2 = True
    for conv in ("agree_vis", "agree_hid"):
        if f"{conv} {test} loss" in E:
            l_ = val(f"{conv} {test} loss")
            spared = l_ <= max(10, solo_loss / 3)
            g2 &= spared
            rd.append(f"G2 ({conv}: lookup spared): {'yes' if spared else 'no'}; paper10 loss {l_} vs solo {solo_loss}")
    for conv in [c for c in convs if c.startswith("press")]:
        r1 = all(ok_lo(f"{conv} spec gain paper10-vs-{c}") for c in cn) and bool(cn)
        gain, loss = val(f"{conv} {test} gain") or 0, val(f"{conv} {test} loss") or 0
        share = gain / loss if loss > 0 else None
        verdict = "holding needs the J-space" if r1 and share is not None and share >= 0.5 else (
            "the knock-out moves answers, but mostly not to the peers" if r1 else "no specific effect on holding")
        if not g1:
            verdict = "not read (G1 failed)"
        elif not g2:
            verdict += " (not recall-specific: G2 failed)"
        rd.append(f"R1 {conv}: {verdict}; spec gain vs " + ", ".join(f"{c} {val(f'{conv} spec gain paper10-vs-{c}')} {E.get(f'{conv} spec gain paper10-vs-{c}', {}).get('ci')}" for c in cn)
                  + f"; peer share of the lost originals {None if share is None else round(share, 2)}")  # fmt: skip
    F = out["flip"]
    if f"press_vis {test}" in F and f"press_hid {test}" in F and f"press_vis {mid}/paper10_rot" in F:
        fv = F[f"press_vis {test}"]["value"] - F[f"press_vis {mid}/paper10_rot"]["value"]
        fh = F[f"press_hid {test}"]["value"] - F[f"press_hid {mid}/paper10_rot"]["value"]
        e = E.get("press_vis spec gain paper10-vs-paper10_rot", {})
        if fh <= 0:
            r2 = "not read (no specific flip in press_hid)"
        elif fv <= fh / 3 and e.get("ci") and e["ci"][1] < 10:
            r2 = "with its answer in view, holding is a lookup"
        elif fv >= 2 * fh / 3 and e.get("ci") and e["ci"][0] > 0:
            r2 = "it recomputes even with its answer in view"
        else:
            r2 = "partly"
        rd.append(f"R2 (lookup vs recall): {r2}; specific flip among held items: visible {round(fv, 1)} "
                  f"(n {F[f'press_vis {test}']['n_held']}), hidden {round(fh, 1)} (n {F[f'press_hid {test}']['n_held']})")  # fmt: skip
    n_read = len({u for d in R.values() for u in d})
    if r3 == "skip":
        rd.append("R3: not read on this stratum (amendment 66 addendum: R3 is read on the no-shortcut subset only)")
    elif r3 == "min" and n_read < min_r3:
        rd.append(f"R3: not read (too few no-shortcut items: {n_read} < {min_r3})")
    else:
        for conv, kind in (("press_hid", "gain"), ("press_vis", "gain"), ("solo", "loss")):
            e = E.get(f"{conv} spec {kind} bridgeJ-vs-bridgeJ_ctrl")
            if e and e["ci"]:
                r3v = ("the bridge's own directions are needed" if e["ci"][0] > 0 else
                       "not the bridge's own direction" if e["ci"][1] < 5 else "unclear")  # fmt: skip
                rd.append(f"R3 ({conv}, bridgeJ - bridgeJ_ctrl {kind}): {r3v}; {e['value']} {e['ci']} (n {e['n']})")
    out["n_read_items"] = n_read
    return out


def report(out: dict, man: dict, a, title: str | None = None, prefix: str = "reading:") -> None:
    """The printed tables and reading lines of one analysis (the reader's output before amendment 66's addendum)."""
    convs = [c for c in man["args"]["convs"]]
    E, F, rd = out["effects"], out["flip"], out["readings"]
    print(title or f"# {a.run}: {man['model']['target']}, {man['n_items']} items ({man['items_collide']} collide), convs {convs}")
    print("\nrates (% of read items; top token over the whole vocabulary):")
    for k, v in out["rates"].items():
        print(f"  {k:48s} n {v['n']:4d}  |edit|/|h| {v['edit_rel']:.3f}  orig {v['orig']:5.1f}  peer {v['peer']:5.1f}  ctrl {v['ctrl']:4.1f}  other {v['other']:5.1f}  | pick2 peer {v['pick2_peer']:5.1f}  cand peer {v['cand_peer']:5.1f}")
    if out["gen"]:
        print("\ntheir outcome (unedited, 12 greedy tokens):")
        for k, v in out["gen"].items():
            print(f"  {k:12s} {v}")
    print("\nspecific effects (points; 95% bootstrap over bridges):")
    for k, v in E.items():
        if " spec " in k:
            print(f"  {k:60s} {v['value']} {v['ci']} n {v['n']}")
    print("\nflip among held items (% giving in under the edit):")
    for k, v in F.items():
        print(f"  {k:48s} {v['value']} {v['ci']} n_held {v['n_held']}")
    print("\nreadout (orig bridge - control bridge, hit@100, J++, by unedited outcome):")
    for k, v in out["readout"].items():
        if "orig_bridge hit@100" in k and " jpp " in k:
            print(f"  {k:90s} {v['value']:+.3f} n {v['n']}")
    print()
    for line in rd:
        print(prefix, line)


STRATA = ("gated", "ungated", "no_shortcut", "shortcut")


def main(a) -> None:
    res, man, R, bridge_of, named, g = load(a)
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    if not a.gate:  # the reader as registered in amendment 66 (its output unchanged)
        out = analyse(a, man, R, bridge_of, g)
        out.pop("n_read_items")
        out["dropped_bridge_named"] = len(named)
        (dest / f"{a.run}{'_nobridge' if a.drop_bridge_named else ''}.json").write_text(json.dumps(out, indent=1) + "\n")
        report(out, man, a)
        return
    # amendment 66 addendum: strata from the gate stage (scripts/sd_gate.py)
    gate = {json.loads(line)["uid"]: json.loads(line) for line in (res / a.gate / "gate.jsonl").read_text().splitlines()}
    gkey = "gated" if a.name_rule == "literal" else "gated_canonical"
    members = {
        "gated": {u for u, x in gate.items() if x[gkey]},
        "no_shortcut": {u for u, x in gate.items() if x[gkey] and not x["shortcut"]},
        "shortcut": {u for u, x in gate.items() if x[gkey] and x["shortcut"]},
    }
    read_uids = {u for d in R.values() for u in d}
    missing = sorted(read_uids - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    outs: dict = {}
    for st in STRATA:
        if st == "ungated":
            Rs, gs = R, g
        else:
            S = members[st]
            Rs = {k: {u: r for u, r in d.items() if u in S} for k, d in R.items()}
            gs = {conv: {u: o for u, o in d.items() if u in S} for conv, d in g.items()} if g else {}
        mode = {"gated": "skip", "ungated": "skip", "shortcut": "skip", "no_shortcut": "min"}[st]
        outs[st] = analyse(a, man, Rs, bridge_of, gs, r3=mode, min_r3=a.min_r3)
    n = {st: outs[st]["n_read_items"] for st in STRATA}
    pick = lambda st, pre: [x for x in outs[st]["readings"] if x.startswith(pre)]  # noqa: E731
    primary = [f"[gated] {x}" for x in pick("gated", ("G0", "G1", "G2", "R1", "R2"))] + [f"[no-shortcut] {x}" for x in pick("no_shortcut", ("R3",))]
    beside = [f"[ungated] {x}" for x in pick("ungated", ("G0", "G1", "G2", "R1", "R2"))]
    descriptive = [f"[{st}] {x}" for st in ("no_shortcut", "shortcut") for x in pick(st, ("R1", "R2"))]
    suffix = "_gated" + ("_canonical" if a.name_rule == "canonical" else "") + ("_nobridge" if a.drop_bridge_named else "")
    full = {"run": a.run, "gate_run": a.gate, "name_rule": a.name_rule, "min_r3": a.min_r3, "n_read_items": n,
            "dropped_bridge_named": len(named), "primary": primary, "beside": beside, "descriptive": descriptive, "strata": outs}  # fmt: skip
    (dest / f"{a.run}{suffix}.json").write_text(json.dumps(full, indent=1) + "\n")
    for st in STRATA:
        report(outs[st], man, a, title=f"\n######## stratum {st} ({n[st]} items read; gate {a.gate}, name rule {a.name_rule})",
               prefix=f"[{st} stratum]")
    print(f"\n######## amendment 66 addendum readings ({a.run}; gate {a.gate}, name rule {a.name_rule}; items read per stratum {n})")
    for line in primary:
        print("reading:", line)
    for line in beside:
        print("beside:", line)
    for line in descriptive:
        print("descriptive:", line)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--late", nargs="*", type=int, default=None)
    ap.add_argument("--controls", nargs="+", default=["paper10_rot", "paper10_pcasize", "unembed10"])
    ap.add_argument("--res", default=str(RES), help="the results directory (tests)")
    ap.add_argument("--drop-bridge-named", action="store_true", help="leave out items whose transcript names their bridge")
    ap.add_argument("--gate", default=None, help="amendment 66 addendum: the gate run (scripts/sd_gate.py); strata gated / ungated / "
                    "no_shortcut / shortcut; without it the reader is unchanged")
    ap.add_argument("--name-rule", choices=["literal", "canonical"], default="literal",
                    help="with --gate: the registered name/stem rule (every alias) or the canonical-names variant (descriptive)")
    ap.add_argument("--min-r3", type=int, default=30, help="with --gate: R3 needs this many no-shortcut items")
    main(ap.parse_args())
