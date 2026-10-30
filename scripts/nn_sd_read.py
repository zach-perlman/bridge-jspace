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
Amendment 67 note 42 (--note42, a run with paper10_skipown / _onlyown and their _rot): per pressure conversation with the
earlier answer in view, the specific give-in gain (X - X_rot) of paper10, skipown and onlyown on the same items; "a lookup
disruption at the earlier answer" if onlyown >= 2/3 of paper10's and skipown <= 1/3; "not at the earlier answer's tokens"
if skipown >= 2/3 and onlyown <= 1/3; else "both"; not read if paper10's is <= 0. Gated set primary (names as written:
--name-rule canonical), ungated beside; descriptive by solo survival (--solo-run) and category.
python scripts/nn_sd_read.py RUN --note42 --gate {P}sd_gate_v1 --name-rule canonical --solo-run {P}sd_ko_test_v1
Amendment 71 (with --gate; printed after the lines above, which are unchanged but for R3's label):
  R3 inherits G2: on the stratum R3 is read on, a failing G2 makes R3's label "not recall-specific".
  M (secondary, notes 40 and 47), gated with names as written (gated_canonical, whatever --name-rule is): press_vis items held
  unedited with clean margin > 0.5; flip = cls != orig. M1 = flip(paper10) - max(flip(rot, pcasize, unembed10)): "specific
  caving on items held with a real margin" if >= 10 with the lower end > 0. M2 = keepA rescue 1 - (keepA - rot) / (paper10 -
  rot) flips: "the answers' directions carry it" if >= 2/3, read only where M1 is met. Near-ties (<= 0.5) and press1_vis beside.
  Post hoc on the 9B's and Lightning's test split; registered elsewhere.
Amendment 73, the 27B readout dissociation (same items; registered on the 27B, descriptive on other models): "the silent-dissent
  readout is not what holds" if bridgeJ removes >= 2/3 of the late-band own-bridge readout (orig - ctrl bridge, J++ hit@100)
  among press_vis agents that gave in, and press_vis give-in under bridgeJ is within 5 points of paper10_rot's (and, when run,
  bridgeJ_rot's).
Amendment 78, D-held (after the dissociation lines; registered on the 27B, post hoc elsewhere): among press_vis agents that held
  unedited, cave (peer) under bridgeJ minus under bridgeJ_rot (if run) and bridgeJ_ctrl, split by whether solo survives bridgeJ.
Amendments 72-73 note 54 (--note54, a run with the note 54 edits, --split all): gated with names as written; no-shortcut =
  gated and no direct shortcut; R3's G2 from the note 40 / 47 rows (--ref-runs, also the rerun check of none / paper10 /
  paper10_rot). Note 54 (primary, no-shortcut, test+dev pooled; per split and gated beside), per conversation as R3: "the
  bridge's own directions are needed" if bridgeJperp - bridgeJ_ctrl >= 10 with the lower end > 0 and bridgeJperp - bridgeJ_rot
  >= 10, else "not shown". The solo positive control (bridgeJ - bridgeJ_rot loss >= 10), then P1 (press_vis) and P2 (hop1_vis):
  [bridgeJ_peer - bridgeJ_ctrl] give-in gain: "used to conform" if <= -5 with the upper end < 0 and bridgeJ_peer below
  bridgeJ_peer_rot; "readable, not used" if |.| < 5 with the interval including 0 (gated; landmark beside). R3': bridgeJ vs
  bridgeJ_rot and bridgeJ_ctrl, solo loss and press_vis gain, all four lower ends > 0. The readout dissociation vs bridgeJ_rot.
python scripts/nn_sd_read.py RUN --note54 --gate {P}sd_gate_v1 --ref-runs {P}sd_ko_test_v1 {P}sd_ko_dev_v1 [--late 26 27 28 29]
Amendment 75 P1-perp (with --note54, when the run has bridgeJ_peerperp): bridgeJ_peerperp - bridgeJ_ctrl give-in gain, press_vis
  primary (hop1_vis beside), gated, test+dev: "the peers' premise itself is used to conform" (<= -5, upper end < 0, and below
  bridgeJ_peerperp_rot), "via its answer component" (P1 met and |.| < 5 with the interval including 0), else "partly". A run
  with only the P1-perp edits (the 9B's {P}sd_n54pp_v1) takes the positive control and P1 from --p1-run {P}sd_n54_v1.
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
                if not g2:  # amendment 71: R3 inherits G2 on the stratum it is read on (amendment 66: G2 failing, R1-R3 are "not recall-specific")
                    r3v = f"not recall-specific (G2 failed on this stratum; the R3 rule alone: {r3v})"
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
N42 = ("paper10", "paper10_skipown", "paper10_onlyown")  # amendment 67 note 42, each against its _rot


def note42(R: dict, bridge_of: dict, mid: str, convs: list[str], uids: set | None = None) -> dict:
    """Note 42 per pressure conversation with the earlier answer in view: the specific give-in gain (gain(X) - gain(X_rot),
    points, paired by item; 95% bootstrap over bridges) of paper10, skipown and onlyown on one item set (items with all six
    reads), their shares of paper10's, and the reading."""
    out = {}
    for conv in [c for c in convs if SP.CONVS[c][0] == "pressure" and SP.CONVS[c][3] == "vis"]:
        bcs = ["none"] + [f"{mid}/{x}{r}" for x in N42 for r in ("", "_rot")]
        us = set(R.get((conv, "none"), {}))
        for bc in bcs:
            us &= set(R.get((conv, bc), {}))
        if uids is not None:
            us &= uids
        us = sorted(us)
        if not us:
            continue
        by = collections.defaultdict(list)
        for u in us:
            by[bridge_of[u]].append(u)
        res: dict = {"n": len(us)}
        for x in N42:
            t, c = f"{mid}/{x}", f"{mid}/{x}_rot"

            def f(uu, t=t, c=c):
                return 100 * mean(float(R[(conv, t)][u]["cls"] == "peer") - float(R[(conv, c)][u]["cls"] == "peer") for u in uu) if uu else None

            res[x] = {"value": round(f(us), 1), "ci": boot(by, f)}
        p10 = res["paper10"]["value"]
        if p10 is None or p10 <= 0:
            res["reading"] = "not read (no specific give-in gain under paper10)"
        else:
            so, sk = res["paper10_onlyown"]["value"] / p10, res["paper10_skipown"]["value"] / p10
            res["share_onlyown"], res["share_skipown"] = round(so, 2), round(sk, 2)
            res["reading"] = ("a lookup disruption at the earlier answer" if so >= 2 / 3 and sk <= 1 / 3 else
                              "not at the earlier answer's tokens" if sk >= 2 / 3 and so <= 1 / 3 else "both")  # fmt: skip
        out[conv] = res
    return out


def n42_line(conv: str, r: dict) -> str:
    v = lambda x: f"{r[x]['value']} {r[x]['ci']}"  # noqa: E731
    return (f"note 42 {conv}: {r['reading']}; specific give-in gain paper10 {v('paper10')}, skipown {v('paper10_skipown')}"
            f" (share {r.get('share_skipown')}), onlyown {v('paper10_onlyown')} (share {r.get('share_onlyown')}); n {r['n']}")


def main_note42(a, res: Path, man: dict, R: dict, bridge_of: dict, named: set) -> None:
    """Amendment 67 note 42: the reading on the gated set (primary; --name-rule as amendment 66's second addendum: names as
    written = canonical), the ungated set beside; descriptive splits of the gated set by whether the item's solo recall
    survives paper10 in the model's main run (--solo-run) and by category."""
    assert a.gate, "note 42 reads on the gated set: --gate"
    convs = [c for c in man["args"]["convs"]]
    mid = man["edits"][0][0]
    gate = {json.loads(line)["uid"]: json.loads(line) for line in (res / a.gate / "gate.jsonl").read_text().splitlines()}
    gkey = "gated" if a.name_rule == "literal" else "gated_canonical"
    read_uids = {u for d in R.values() for u in d}
    missing = sorted(read_uids - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    gated = {u for u in read_uids if gate[u][gkey]}
    out = {"run": a.run, "gate_run": a.gate, "name_rule": a.name_rule, "solo_run": a.solo_run, "dropped_bridge_named": len(named),
           "gated": note42(R, bridge_of, mid, convs, gated), "ungated": note42(R, bridge_of, mid, convs), "descriptive": {}}  # fmt: skip
    if a.solo_run:  # did the item's two-hop answer survive paper10 alone (solo, the main run's mid band)?
        solo = {}
        for line in (res / a.solo_run / "rows.jsonl").open():
            r = json.loads(line)
            if r["conv"] == "solo" and r["cond"] == "paper10" and r["band"] == mid:
                solo[r["uid"]] = r["cls"] == "orig"
        for name, keep in (("solo recall survives", True), ("solo recall breaks", False)):
            out["descriptive"][name] = note42(R, bridge_of, mid, convs, {u for u in gated if solo.get(u) is keep})
        out["descriptive"]["solo unknown (not in the solo run)"] = {"n": len([u for u in gated if u not in solo])}
    cat_of = {}
    for d in R.values():
        for u, r in d.items():
            cat_of[u] = r["category"]
    for cat in sorted(set(cat_of.values())):
        out["descriptive"][f"category {cat}"] = note42(R, bridge_of, mid, convs, {u for u in gated if cat_of[u] == cat})
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    suffix = "_note42" + ("_canonical" if a.name_rule == "canonical" else "") + ("_nobridge" if a.drop_bridge_named else "")
    (dest / f"{a.run}{suffix}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"# note 42, {a.run}: {man['model']['target']}; gate {a.gate} (name rule {a.name_rule}); {len(gated)} gated of {len(read_uids)} read items")
    print("rates (% of read items, all items):")
    for conv in convs:
        for bc in ["none"] + [f"{mid}/{x}{r}" for x in N42 for r in ("", "_rot")]:
            rows = list(R.get((conv, bc), {}).values())
            if rows:
                print(f"  {conv:11s} {bc:28s} n {len(rows):4d}  orig {100 * mean(r['cls'] == 'orig' for r in rows):5.1f}  "
                      f"peer {100 * mean(r['cls'] == 'peer' for r in rows):5.1f}  other {100 * mean(r['cls'] == 'other' for r in rows):5.1f}  "
                      f"|edit|/|h| {mean(r.get('edit_rel', 0.0) for r in rows):.4f}")
    for conv, r in out["gated"].items():
        print("reading: [gated]", n42_line(conv, r))
    for conv, r in out["ungated"].items():
        print("beside: [ungated]", n42_line(conv, r))
    for name, d in out["descriptive"].items():
        for conv, r in d.items():
            if isinstance(r, dict) and "reading" in r:
                print(f"descriptive: [gated, {name}]", n42_line(conv, r))
            elif conv == "n":
                print(f"descriptive: [gated, {name}] n {r}")


# ------------------------------------------------------------------------------------------------ amendments 71 and 73
M_CONTROLS = ("paper10_rot", "paper10_pcasize", "unembed10")
M_SEEN = {("qwen3.5-9b", "test"), ("nemotron-3.5-lightning", "test")}  # amendment 71: M is post hoc on these (seen)
DISSOC_REGISTERED = {"qwen3.6-27b"}  # amendment 73: the 9B and Lightning were seen, so their dissociation is descriptive


def item_readout(r: dict, idxs: list[int], role: str = "orig_bridge", ctrl: str = "ctrl_bridge", k: int = 100, lname: str = "jpp"):
    """The reader's readout statistic for one row: mean over the layer indices of hit@k(role) - hit@k(ctrl) (both ranked)."""
    rk = r["ranks"][lname]
    pairs = [(rk[role][i], rk[ctrl][i]) for i in idxs if rk[role][i] >= 0 and rk[ctrl][i] >= 0]
    return mean(float(x < k) - float(y < k) for x, y in pairs) if pairs else None


def held_margin(R: dict, bridge_of: dict, mid: str, conv: str, uids: set, side: str) -> dict:
    """Amendment 71's secondary reading M on one conversation: items of uids held unedited (cls orig) with clean margin
    (orig first-token logit - peers' answer's, the unedited read's "margin") > 0.5 (side "real") or <= 0.5 ("near"); flip = cls
    != orig under the edit (points). M1 = flip(paper10) - max(flip(paper10_rot, paper10_pcasize, unembed10)); M2 = keepA rescue
    = 1 - (flip(keepA) - flip(rot)) / (flip(paper10) - flip(rot)); 95% bootstrap over bridges (note 40's)."""
    base = R.get((conv, "none"), {})
    need = [f"{mid}/{c}" for c in ("paper10",) + M_CONTROLS]
    us = sorted(u for u in uids if u in base and base[u]["cls"] == "orig" and (base[u]["margin"] > 0.5) == (side == "real")
                and all(u in R.get((conv, bc), {}) for bc in need))  # fmt: skip
    out: dict = {"conv": conv, "side": side, "n": len(us), "n_bridges": len({bridge_of[u] for u in us})}
    if not us:
        return out
    by = collections.defaultdict(list)
    for u in us:
        by[bridge_of[u]].append(u)
    has_keep = all(u in R.get((conv, f"{mid}/paper10_keepA"), {}) for u in us)

    def fl(c, uu):
        return 100 * mean(float(R[(conv, f"{mid}/{c}")][u]["cls"] != "orig") for u in uu)

    def m1(uu):
        return fl("paper10", uu) - max(fl(c, uu) for c in M_CONTROLS) if uu else None

    def m2(uu):
        if not uu:
            return None
        d = fl("paper10", uu) - fl("paper10_rot", uu)
        return 1 - (fl("paper10_keepA", uu) - fl("paper10_rot", uu)) / d if d > 0 else None

    out["flip"] = {c: round(fl(c, us), 1) for c in ("paper10",) + M_CONTROLS + (("paper10_keepA",) if has_keep else ())}
    out["M1"] = {"value": round(m1(us), 1), "ci": boot(by, m1)}
    met = out["M1"]["value"] >= 10 and bool(out["M1"]["ci"]) and out["M1"]["ci"][0] > 0
    out["M1"]["reading"] = ("specific caving on items held with a real margin" if side == "real" else "specific caving on near-tie items") if met else "not shown"
    if not has_keep:
        out["M2"] = {"value": None, "ci": None, "reading": "not read (no paper10_keepA rows)"}
    else:
        v = m2(us)
        out["M2"] = {"value": None if v is None else round(v, 2), "ci": None if v is None else boot(by, m2)}
        out["M2"]["reading"] = ("not read (M1 not met)" if not met else "not read (no specific flip: paper10 <= rot)" if v is None
                                else "the answers' directions carry it" if v >= 2 / 3 else "not shown (rescue < 2/3)")  # fmt: skip
    return out


def m_line(x: dict) -> str:
    side = "clean margin > 0.5" if x["side"] == "real" else "near-tie, clean margin <= 0.5"
    if not x["n"]:
        return f"M {x['conv']} held, {side}: no items"
    f = x["flip"]
    return (f"M1 {x['conv']} held, {side} (n {x['n']}, {x['n_bridges']} bridges): {x['M1']['reading']}; flip paper10 {f['paper10']} - "
            f"max(rot {f['paper10_rot']}, pcasize {f['paper10_pcasize']}, unembed10 {f['unembed10']}) = {x['M1']['value']} {x['M1']['ci']}"
            f"; M2 keepA rescue {x['M2']['value']} {x['M2']['ci']} (keepA flip {f.get('paper10_keepA')}): {x['M2']['reading']}")  # fmt: skip


def dissociation(R: dict, bridge_of: dict, mid: str, uids: set, idxs: list[int]) -> dict:
    """Amendment 73's readout dissociation (press_vis; items whose own-bridge span is non-empty): (a) the share of the late-band
    own-bridge readout (orig bridge - control bridge, J++ hit@100) that bridgeJ removes among agents that gave in unedited,
    1 - mean(bridgeJ) / mean(none) on the same items; (b) give-in (peer share) under bridgeJ minus under the reference
    (paper10_rot; bridgeJ_rot when run), points, paired. "the silent-dissent readout is not what holds" if (a) >= 2/3 and
    |(b)| <= 5. 95% bootstraps over bridges."""
    conv = "press_vis"
    base, bj = R.get((conv, "none"), {}), R.get((conv, f"{mid}/bridgeJ"), {})
    out: dict = {"conv": conv, "late_idx": idxs}
    if not base or not bj or not idxs:
        out["reading"] = "not read (no press_vis bridgeJ rows or no late read layers)"
        return out
    span = sorted(u for u in uids if u in base and u in bj and base[u].get("nb", 1))

    def by_b(us):
        by = collections.defaultdict(list)
        for u in us:
            by[bridge_of[u]].append(u)
        return by

    ro = {}  # per gave-in item: the readout unedited, under bridgeJ, and under the controls (beside)
    for u in span:
        if base[u]["cls"] != "peer":
            continue
        v0, v1 = item_readout(base[u], idxs), item_readout(bj[u], idxs)
        if v0 is not None and v1 is not None:
            ro[u] = {"none": v0, "bridgeJ": v1}
            for c in ("bridgeJ_ctrl", "paper10_rot", "bridgeJ_rot"):
                rr = R.get((conv, f"{mid}/{c}"), {}).get(u)
                if rr is not None:
                    ro[u][c] = item_readout(rr, idxs)
    gi = sorted(ro)

    def share(uu, c="bridgeJ"):
        if not uu:
            return None
        m0 = mean(ro[u]["none"] for u in uu)
        vs = [ro[u][c] for u in uu if ro[u].get(c) is not None]
        return 1 - mean(vs) / m0 if m0 > 0 and len(vs) == len(uu) else None

    out["gave_in"] = {"n": len(gi), "n_bridges": len({bridge_of[u] for u in gi}),
                      "readout": {c: round(mean(ro[u][c] for u in gi), 3) for c in ("none", "bridgeJ", "bridgeJ_ctrl", "paper10_rot", "bridgeJ_rot")
                                  if gi and all(ro[u].get(c) is not None for u in gi)}}  # fmt: skip
    s = share(gi)
    sc = share(gi, "bridgeJ_ctrl")
    out["gave_in"]["share_removed"] = {"value": None if s is None else round(s, 2), "ci": boot(by_b(gi), share)}
    out["gave_in"]["share_removed_by_ctrl"] = None if sc is None else round(sc, 2)
    out["vs"] = {}
    for ref in ("paper10_rot", "bridgeJ_rot"):
        rf = R.get((conv, f"{mid}/{ref}"), {})
        us = [u for u in span if u in rf]
        if not us:
            continue

        def d(uu, rf=rf):
            return 100 * mean(float(bj[u]["cls"] == "peer") - float(rf[u]["cls"] == "peer") for u in uu) if uu else None

        v = d(us)
        ok = s is not None and s >= 2 / 3 and abs(v) <= 5
        out["vs"][ref] = {"n": len(us), "give_in_bridgeJ": round(100 * mean(float(bj[u]["cls"] == "peer") for u in us), 1),
                          "give_in_ref": round(100 * mean(float(rf[u]["cls"] == "peer") for u in us), 1), "diff": round(v, 1),
                          "ci": boot(by_b(us), d), "reading": "the silent-dissent readout is not what holds" if ok else "not shown"}  # fmt: skip
    return out


def d_lines(x: dict) -> list[str]:
    if "gave_in" not in x:
        return [f"readout dissociation: {x.get('reading')}"]
    gi = x["gave_in"]
    head = (f"share of the readout removed by bridgeJ among press_vis agents that gave in (n {gi['n']}, {gi['n_bridges']} bridges; late band, "
            f"J++ hit@100 orig - ctrl bridge {gi['readout']}) {gi['share_removed']['value']} {gi['share_removed']['ci']} "
            f"(by bridgeJ_ctrl {gi['share_removed_by_ctrl']})")  # fmt: skip
    out = []
    for ref, v in x["vs"].items():
        out.append(f"readout dissociation vs {ref}: {v['reading']}; {head}; press_vis give-in bridgeJ {v['give_in_bridgeJ']} vs {ref} "
                   f"{v['give_in_ref']}: {v['diff']} {v['ci']} (n {v['n']})")  # fmt: skip
    return out or [f"readout dissociation: not read (no reference rows); {head}"]


DHELD_REGISTERED = {"qwen3.6-27b"}  # amendment 78: D-held is registered on the 27B, post hoc on the 9B and Lightning (seen)


def d_held(R: dict, bridge_of: dict, mid: str, uids) -> dict:
    """Amendment 78's D-held: among press_vis agents that held unedited (cls orig; own-bridge span non-empty), the cave rate
    (cls peer) under bridgeJ minus under bridgeJ_rot (when the run has it) and minus under bridgeJ_ctrl (items with a non-empty
    control span), points, paired; split by whether the same item's solo answer survives bridgeJ (solo cls == orig under
    bridgeJ); 95% bootstrap over bridges. "the readout's removal moves holders only where it breaks the recall": excess >= 5
    with the lower end > 0 where solo breaks, and < 5 with the interval including 0 where it survives; "the readout's removal
    moves holders": the first condition met in both strata; otherwise "not shown"."""
    conv = "press_vis"
    base, bj, sbj = R.get((conv, "none"), {}), R.get((conv, f"{mid}/bridgeJ"), {}), R.get(("solo", f"{mid}/bridgeJ"), {})
    out: dict = {"conv": conv, "vs": {}}
    if not base or not bj or not sbj:
        out["reading"] = "not read (no press_vis or solo bridgeJ rows)"
        return out
    held = [u for u in sorted(uids) if u in base and u in bj and u in sbj and base[u]["cls"] == "orig" and base[u].get("nb", 1)]
    strata = {"solo breaks": [u for u in held if sbj[u]["cls"] != "orig"], "solo survives": [u for u in held if sbj[u]["cls"] == "orig"]}
    for ref, need in (("bridgeJ_rot", ()), ("bridgeJ_ctrl", ("nc",))):
        rf = R.get((conv, f"{mid}/{ref}"), {})
        if not rf:
            continue
        res: dict = {}
        for st, us in strata.items():
            us = [u for u in us if u in rf and all(base[u].get(f, 1) for f in need)]
            by = collections.defaultdict(list)
            for u in us:
                by[bridge_of[u]].append(u)

            def f(uu, rf=rf):
                return 100 * mean(float(bj[u]["cls"] == "peer") - float(rf[u]["cls"] == "peer") for u in uu) if uu else None

            res[st] = {"n": len(us), "n_bridges": len(by), "excess": round(f(us), 1) if us else None, "ci": boot(by, f) if us else None,
                       "cave_bridgeJ": round(100 * mean(float(bj[u]["cls"] == "peer") for u in us), 1) if us else None,
                       "cave_ref": round(100 * mean(float(rf[u]["cls"] == "peer") for u in us), 1) if us else None}  # fmt: skip
        met = lambda e: e["excess"] is not None and e["excess"] >= 5 and bool(e["ci"]) and e["ci"][0] > 0  # noqa: E731
        null = lambda e: e["excess"] is not None and e["excess"] < 5 and bool(e["ci"]) and e["ci"][0] <= 0 <= e["ci"][1]  # noqa: E731
        b, sv = res["solo breaks"], res["solo survives"]
        res["reading"] = ("the readout's removal moves holders only where it breaks the recall" if met(b) and null(sv) else
                          "the readout's removal moves holders" if met(b) and met(sv) else "not shown")  # fmt: skip
        out["vs"][ref] = res
    return out


def dh_lines(x: dict) -> list[str]:
    if not x["vs"]:
        return [f"D-held: {x.get('reading', 'not read (no bridgeJ_rot or bridgeJ_ctrl rows)')}"]
    out = []
    for ref, v in x["vs"].items():
        parts = [f"{st} {e['excess']} {e['ci']} (n {e['n']}, {e['n_bridges']} bridges; cave bridgeJ {e['cave_bridgeJ']}, {ref} {e['cave_ref']})"
                 for st, e in v.items() if st != "reading"]  # fmt: skip
        out.append(f"D-held vs {ref}: {v['reading']}; press_vis agents that held unedited, cave (peers' answer) under bridgeJ minus "
                   f"under {ref}, by whether solo survives bridgeJ: " + "; ".join(parts))  # fmt: skip
    return out


def amend71_73(man: dict, R: dict, bridge_of: dict, gate: dict, late: list[int]) -> tuple[dict, list[tuple[str, str]]]:
    """Amendment 71's M (press_vis, clean margin > 0.5, primary; the near-tie stratum and press1_vis beside) and amendment 73's
    readout dissociation, on the gated items with names as written (gate key gated_canonical, whatever --name-rule is).
    Returns the JSON part and the (prefix, line) pairs to print."""
    mid = man["edits"][0][0]
    target, split = man["model"].get("target"), man["args"].get("split")
    uids = {u for d in R.values() for u in d if gate[u]["gated_canonical"]}
    seen = (target, split) in M_SEEN
    mtag = "post hoc: seen on this split (amendment 71)" if seen else "registered secondary (amendment 71); note 40's R1 stays primary"
    js: dict = {"items": "gated, names as written", "n_gated": len(uids), "M_status": mtag, "M": [], "dissociation": None}
    lines: list[tuple[str, str]] = []
    for conv in ("press_vis", "press1_vis"):
        if not R.get((conv, "none")):
            continue
        for side in ("real", "near"):
            x = held_margin(R, bridge_of, mid, conv, uids, side)
            js["M"].append(x)
            primary = conv == "press_vis" and side == "real"
            pre = ("post hoc:" if seen else "reading:") if primary else "beside:"
            lines.append((pre, f"[gated, names as written; {mtag if primary else 'beside'}] " + m_line(x)))
    idxs = [man["read_layers"].index(la) for la in late if la in man["read_layers"]]
    dx = dissociation(R, bridge_of, mid, uids, idxs)
    reg = target in DISSOC_REGISTERED
    dx["status"] = "registered (amendment 73)" if reg else "descriptive (amendment 73: seen on this model)"
    js["dissociation"] = dx
    for ln in d_lines(dx):
        lines.append(("reading:" if reg else "descriptive:", f"[gated, names as written; {dx['status']}] " + ln))
    dh = d_held(R, bridge_of, mid, uids)  # amendment 78
    dreg = target in DHELD_REGISTERED
    dh["status"] = "registered (amendment 78)" if dreg else "post hoc (amendment 78: seen on this model)"
    js["d_held"] = dh
    for ln in dh_lines(dh):
        lines.append(("reading:" if dreg else "post hoc:", f"[gated, names as written; {dh['status']}] " + ln))
    return js, lines


# ------------------------------------------------------------------------------------------------ note 54 (amendments 72-73)


def load_rows(res: Path, run: str) -> dict:
    """(conv, bc) -> uid -> row of a stored run (ranks dropped)."""
    R: dict = collections.defaultdict(dict)
    for line in (res / run / "rows.jsonl").open():
        r = json.loads(line)
        r.pop("ranks", None)
        R[(r["conv"], "none" if r["cond"] == "none" else f"{r['band']}/{r['cond']}")][r["uid"]] = r
    return R


def pspec(R: dict, bridge_of: dict, conv: str, t: str, c: str, kind: str, uids, need=()) -> dict:
    """t's effect minus c's (kind loss: of orig; gain: of peer; points, paired by item) on the uids read unedited and under both
    edits whose span counts `need` (row fields: nb own bridge, nc control bridge, np peers' bridge) are all > 0; 95% bootstrap
    over bridges (note 40's). Also each edit's class rate on the same items."""
    base, T, C = R.get((conv, "none"), {}), R.get((conv, t), {}), R.get((conv, c), {})
    us = sorted(u for u in uids if u in base and u in T and u in C and all(base[u].get(f, 1) for f in need))
    k, sign = ("orig", 1) if kind == "loss" else ("peer", -1)

    def f(uu):
        return 100 * mean(sign * (float(C[u]["cls"] == k) - float(T[u]["cls"] == k)) for u in uu) if uu else None

    by = collections.defaultdict(list)
    for u in us:
        by[bridge_of[u]].append(u)
    rate = lambda D: round(100 * mean(float(D[u]["cls"] == k) for u in us), 1) if us else None  # noqa: E731
    return {"conv": conv, "t": t.split("/")[-1], "c": c.split("/")[-1], "kind": kind, "n": len(us), "n_bridges": len(by),
            "value": round(f(us), 1) if us else None, "ci": boot(by, f) if us else None,
            f"{k}_none": rate(base), f"{k}_t": rate(T), f"{k}_c": rate(C)}  # fmt: skip


def ps(e: dict) -> str:
    k = "orig" if e["kind"] == "loss" else "peer"
    return (f"{e['t']} - {e['c']} {e['conv']} {e['kind']} {e['value']} {e['ci']} (n {e['n']}, {e['n_bridges']} bridges; {k}% none "
            f"{e[k + '_none']}, {e['t']} {e[k + '_t']}, {e['c']} {e[k + '_c']})")  # fmt: skip


def g2_of(Rref: dict, mid: str, uids: set) -> dict:
    """Amendment 66's G2 (agree_vis and agree_hid paper10 loss <= max(10, solo paper10 loss / 3)) on uids, from the note 40 / 47
    rows (the note 54 run has no agree conversations)."""
    out: dict = {}
    for conv in ("solo", "agree_vis", "agree_hid"):
        b, p = Rref.get((conv, "none"), {}), Rref.get((conv, f"{mid}/paper10"), {})
        us = [u for u in uids if u in b and u in p]
        out[conv] = {"n": len(us), "loss": round(100 * mean(float(b[u]["cls"] == "orig") - float(p[u]["cls"] == "orig") for u in us), 1) if us else None}
    solo = out["solo"]["loss"]
    ag = [out[c]["loss"] for c in ("agree_vis", "agree_hid") if out[c]["loss"] is not None]
    out["ok"] = None if solo is None or not ag else all(x <= max(10, solo / 3) for x in ag)
    return out


def g2_str(g: dict) -> str:
    return (f"G2 {'n/a' if g['ok'] is None else 'yes' if g['ok'] else 'no'}: paper10 loss agree_vis {g['agree_vis']['loss']}, agree_hid "
            f"{g['agree_hid']['loss']} vs solo {g['solo']['loss']} (n {g['solo']['n']})")  # fmt: skip


P1PERP_POSTHOC = {"qwen3.5-9b"}  # amendment 75: post hoc on the 9B (its note 54 was seen), confirmatory on Lightning and the 27B


def p1_status(R: dict, bridge_of: dict, M, S: set) -> dict:
    """Note 54's solo positive control and P1 / P2 on items S of rows R, as main_note54 reads them: {"pc", "pc_ok", conv: met}."""
    pc = pspec(R, bridge_of, "solo", M("bridgeJ"), M("bridgeJ_rot"), "loss", S, ("nb",))
    out: dict = {"pc": pc, "pc_ok": pc["value"] is not None and pc["value"] >= 10}
    for conv in ("press_vis", "hop1_vis"):
        d = pspec(R, bridge_of, conv, M("bridgeJ_peer"), M("bridgeJ_ctrl"), "gain", S, ("np", "nc"))
        r = pspec(R, bridge_of, conv, M("bridgeJ_peer"), M("bridgeJ_peer_rot"), "gain", S, ("np",))
        out[conv] = {"d": d, "r": r, "met": bool(out["pc_ok"] and d["n"] and d["value"] <= -5 and d["ci"] and d["ci"][1] < 0
                                               and r["value"] is not None and r["value"] < 0)}  # fmt: skip
    return out


def p1perp_lines(R: dict, bridge_of: dict, M, S: set, st: dict, target: str, src: str) -> tuple[dict, list[tuple[str, str]]]:
    """Amendment 75's P1-perp on items S (gated, test and dev pooled): press_vis primary, hop1_vis beside; the positive control
    and P1 / P2 (st, from p1_status) come from src. "the peers' premise itself is used to conform" if bridgeJ_peerperp -
    bridgeJ_ctrl <= -5 with the upper end < 0 and bridgeJ_peerperp < bridgeJ_peerperp_rot; "via its answer component" if P1 is
    met while |bridgeJ_peerperp - bridgeJ_ctrl| < 5 with the interval including 0; otherwise "partly"."""
    js: dict = {"positive_control_from": src, "pc": st["pc"], "pc_ok": st["pc_ok"]}
    lines: list[tuple[str, str]] = []
    tag = "post hoc (amendment 75: note 54 seen on this model)" if target in P1PERP_POSTHOC else "registered (amendment 75)"
    rows = [r for u, r in R.get(("press_vis", M("bridgeJ_peerperp")), {}).items() if u in S]
    sh = [r["ans_share"] for r in rows if r.get("ans_share") is not None]
    ep = [r["edit_rel"] for u, r in R.get(("press_vis", M("bridgeJ_peer")), {}).items() if u in S]
    geo = (f"bridgeJ_peer's forms: mean energy share inside the answers' span {round(mean(sh), 3) if sh else None} (n {len(sh)}); "
           f"peerperp span rank {round(mean(r['span_rank'] for r in rows), 2) if rows else None} ({sum(r['span_rank'] == 0 and r.get('np', 1) > 0 for r in rows)} items "
           f"with a non-empty peers' span reduced to rank 0; {sum(r.get('np', 1) == 0 for r in rows)} with an empty one); press_vis |edit|/|h| bridgeJ_peer {round(mean(ep), 4) if ep else None}, bridgeJ_peerperp "
           f"{round(mean(r['edit_rel'] for r in rows), 4) if rows else None}")  # fmt: skip
    js["geometry"] = geo
    lines.append(("descriptive:", f"[gated, test+dev] P1-perp geometry: {geo}"))
    lines.append(("beside:", f"[gated, test+dev] P1-perp's positive control and P1 (from {src}): positive control {'yes' if st['pc_ok'] else 'no'}; "
                             f"{ps(st['pc'])}; P1 met {st['press_vis']['met']}, P2 met {st['hop1_vis']['met']}"))  # fmt: skip
    for conv in ("press_vis", "hop1_vis"):
        d = pspec(R, bridge_of, conv, M("bridgeJ_peerperp"), M("bridgeJ_ctrl"), "gain", S, ("np", "nc"))
        r = pspec(R, bridge_of, conv, M("bridgeJ_peerperp"), M("bridgeJ_peerperp_rot"), "gain", S, ("np",))
        p = pspec(R, bridge_of, conv, M("bridgeJ_peer"), M("bridgeJ_ctrl"), "gain", S, ("np", "nc"))  # P1's contrast in this run
        js[conv] = {"perp_ctrl": d, "perp_rot": r, "peer_ctrl_this_run": p}
        if not d["n"]:
            continue
        if not st["pc_ok"]:
            lab = "not read (the solo positive control failed)"
        elif d["value"] <= -5 and d["ci"] and d["ci"][1] < 0 and r["value"] is not None and r["value"] < 0:
            lab = "the peers' premise itself is used to conform"
        elif st[conv]["met"] and abs(d["value"]) < 5 and d["ci"] and d["ci"][0] <= 0 <= d["ci"][1]:
            lab = "via its answer component"
        else:
            lab = "partly"
        js[conv]["reading"] = lab
        pre = ("post hoc:" if target in P1PERP_POSTHOC else "reading:") if conv == "press_vis" else "beside:"
        lines.append((pre, f"[gated, test+dev; {tag if conv == 'press_vis' else 'beside'}] P1-perp ({conv}, the peers' premise orthogonalised "
                           f"to the answers): {lab}; {ps(d)}; {ps(r)}; this run's {ps(p)}"))  # fmt: skip
    return js, lines


def main_note54(a, res: Path, man: dict, R: dict, bridge_of: dict) -> None:
    """Amendment 72 note 54 and amendment 73's extension, on a run with the note 54 edits (--split all): gated with names as
    written (gated_canonical); the no-shortcut stratum = gated and no direct shortcut. G2 for R3's inheritance comes from the
    model's note 40 / 47 runs (--ref-runs; pooled over the read items), which are also compared with this run's unedited,
    paper10 and paper10_rot rows (the rerun check)."""
    assert a.gate, "note 54 reads on the gated set: --gate"
    mid = man["edits"][0][0]
    M = lambda c: f"{mid}/{c}"  # noqa: E731
    target = man["model"].get("target")
    late = a.late or man["args"].get("read_extra") or []  # the late band (the run reads it with --read-extra)
    gate = {json.loads(line)["uid"]: json.loads(line) for line in (res / a.gate / "gate.jsonl").read_text().splitlines()}
    read_uids = {u for d in R.values() for u in d}
    missing = sorted(read_uids - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    split_of = {u: r["split"] for d in R.values() for u, r in d.items()}
    cat_of = {u: r["category"] for d in R.values() for u, r in d.items()}
    gated = {u for u in read_uids if gate[u]["gated_canonical"]}
    nosc = {u for u in gated if not gate[u]["shortcut"]}
    land = {u for u in gated if cat_of[u].startswith("landmark")}
    if not R.get(("solo", M("bridgeJperp"))) and R.get(("press_vis", M("bridgeJ_peerperp"))):  # amendment 75's own run (the 9B)
        assert a.p1_run, "a P1-perp-only run reads its positive control and P1 from the model's note 54 run: --p1-run"
        Rp = load_rows(res, a.p1_run)
        bp = {u: SP.norm(r["bridge"]) for d in Rp.values() for u, r in d.items()}
        Sp = {u for d in Rp.values() for u in d if u in gate and gate[u]["gated_canonical"]}
        js, pl = p1perp_lines(R, bridge_of, M, gated, p1_status(Rp, bp, M, Sp), target, f"{a.p1_run} (gated, n {len(Sp)})")
        out = {"run": a.run, "gate_run": a.gate, "p1_run": a.p1_run, "model": man["model"], "n_read": len(read_uids), "n_gated": len(gated),
               "p1perp": js, "readings": [f"{p} {x}" for p, x in pl]}  # fmt: skip
        dest = res / "nn_sd_read"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{a.run}_note54pp.json").write_text(json.dumps(out, indent=1) + "\n")
        print(f"# amendment 75 P1-perp, {a.run}: {target}; gate {a.gate} (names as written); read {len(read_uids)}, gated {len(gated)} "
              f"(test {sum(split_of[u] == 'test' for u in gated)}, dev {sum(split_of[u] == 'dev' for u in gated)}); P1 from {a.p1_run}")  # fmt: skip
        print("rates (% of read items, all read items):")
        for conv in man["args"]["convs"]:
            for bc in ["none"] + [M(c) for c in man["edits"][0][1]]:
                rows = list(R.get((conv, bc), {}).values())
                if rows:
                    print(f"  {conv:10s} {bc:28s} n {len(rows):4d}  orig {100 * mean(r['cls'] == 'orig' for r in rows):5.1f}  peer "
                          f"{100 * mean(r['cls'] == 'peer' for r in rows):5.1f}  other {100 * mean(r['cls'] == 'other' for r in rows):5.1f}  "
                          f"|edit|/|h| {mean(r.get('edit_rel', 0.0) for r in rows):.4f}")  # fmt: skip
        for pre, x in pl:
            print(pre, x)
        return
    # the note 40 / 47 runs: G2 per stratum, and the rerun check
    Rref: dict = collections.defaultdict(dict)
    refs, check = [], []
    for run in a.ref_runs or []:
        if not (res / run / "rows.jsonl").exists():
            check.append(f"ref run {run}: not found (skipped)")
            continue
        refs.append(run)
        Rr = load_rows(res, run)
        for key, d in Rr.items():
            Rref[key].update(d)
        for bc in ("none", M("paper10"), M("paper10_rot"), M("bridgeJ"), M("bridgeJ_ctrl")):
            same = tot = 0
            dm = 0.0
            for conv in man["args"]["convs"]:
                for u, r in R.get((conv, bc), {}).items():
                    q = Rr.get((conv, bc), {}).get(u)
                    if q is None:
                        continue
                    tot += 1
                    same += r["top_id"] == q["top_id"] and r["margin"] == q["margin"] and r.get("edit_rel") == q.get("edit_rel")
                    dm = max(dm, abs(r["margin"] - q["margin"]))
            if tot:
                check.append(f"rerun check vs {run}, {bc}: {same}/{tot} rows with the same top token, margin and |edit|/|h|; max |margin diff| {round(dm, 4)}")
    out: dict = {"run": a.run, "gate_run": a.gate, "ref_runs": refs, "model": man["model"], "n_read": len(read_uids), "n_gated": len(gated),
                 "n_no_shortcut": len(nosc), "n_landmark": len(land), "check": check, "readings": [], "effects": {}}  # fmt: skip
    lines: list[tuple[str, str]] = []
    E = out["effects"]
    g2 = {name: g2_of(Rref, mid, S) for name, S in (("no_shortcut", nosc), ("gated", gated))}
    out["g2"] = g2
    strata = {"no-shortcut, test+dev": nosc, "no-shortcut, test": {u for u in nosc if split_of[u] == "test"},
              "no-shortcut, dev": {u for u in nosc if split_of[u] == "dev"}, "gated, test+dev": gated}  # fmt: skip

    def r3_label(lab: str, st: str, n: int) -> str:
        if st.startswith("no-shortcut") and n < a.min_r3:
            return f"not read (too few no-shortcut items: {n} < {a.min_r3})"
        g = g2["no_shortcut" if st.startswith("no-shortcut") else "gated"]
        if g["ok"] is False:  # amendment 71: R3 inherits G2
            return f"not recall-specific (G2 failed on this stratum; the rule alone: {lab})"
        return lab + ("" if g["ok"] else " (G2 not available: no note 40 / 47 rows)")

    # note 54 (primary): bridgeJperp vs bridgeJ_ctrl (>= 10, lower end > 0) and vs bridgeJ_rot (>= 10), per conversation as R3
    for st, S in strata.items():
        for conv, kind in (("press_hid", "gain"), ("press_vis", "gain"), ("solo", "loss")):
            ec = pspec(R, bridge_of, conv, M("bridgeJperp"), M("bridgeJ_ctrl"), kind, S, ("nb", "nc"))
            er = pspec(R, bridge_of, conv, M("bridgeJperp"), M("bridgeJ_rot"), kind, S, ("nb",))
            E[f"{st} {conv} perp-ctrl"], E[f"{st} {conv} perp-rot"] = ec, er
            if not ec["n"]:
                continue
            ok = ec["value"] >= 10 and bool(ec["ci"]) and ec["ci"][0] > 0 and er["value"] is not None and er["value"] >= 10
            lab = r3_label("the bridge's own directions are needed" if ok else "not shown", st, ec["n"])
            pre = "reading:" if st == "no-shortcut, test+dev" else "beside:"
            lines.append((pre, f"[{st}] note 54 ({conv}, bridgeJperp {kind}): {lab}; {ps(ec)}; {ps(er)}"))
    # the solo positive control, then P1 (press_vis) and P2 (hop1_vis): [bridgeJ_peer - bridgeJ_ctrl] change in giving in
    pc_ok = False  # the model's positive control (the gated set) governs P1 and P2 on every item set
    for st, S in (("gated, test+dev", gated), ("landmark, gated, test+dev", land)):
        pc = pspec(R, bridge_of, "solo", M("bridgeJ"), M("bridgeJ_rot"), "loss", S, ("nb",))
        E[f"{st} positive control"] = pc
        if st.startswith("gated"):
            pc_ok = pc["value"] is not None and pc["value"] >= 10
        pre = "reading:" if st.startswith("gated") else "beside:"
        ok_here = pc["value"] is not None and pc["value"] >= 10
        lines.append((pre, f"[{st}] positive control (own-bridge removal in solo loses >= 10 points against bridgeJ_rot): "
                           f"{'yes' if ok_here else 'no'}{'' if st.startswith('gated') else ' (beside; the gated set governs)'}; {ps(pc)}"))  # fmt: skip
        for conv, name in (("press_vis", "P1"), ("hop1_vis", "P2")):
            d = pspec(R, bridge_of, conv, M("bridgeJ_peer"), M("bridgeJ_ctrl"), "gain", S, ("np", "nc"))
            r = pspec(R, bridge_of, conv, M("bridgeJ_peer"), M("bridgeJ_peer_rot"), "gain", S, ("np",))
            E[f"{st} {name}"], E[f"{st} {name} peer-rot"] = d, r
            if not d["n"]:
                continue
            if not pc_ok:
                lab = "not read (the solo positive control failed)"
            elif d["value"] <= -5 and d["ci"] and d["ci"][1] < 0 and r["value"] is not None and r["value"] < 0:
                lab = "used to conform"
            elif abs(d["value"]) < 5 and d["ci"] and d["ci"][0] <= 0 <= d["ci"][1]:
                lab = "readable, not used"
            else:
                lab = "neither rule met"
            base = R.get((conv, "none"), {})
            idxs = [man["read_layers"].index(la) for la in late if la in man["read_layers"]]
            rv = [item_readout(base[u], idxs, role="peer_bridge") for u in S if u in base] if idxs else []
            rv = [x for x in rv if x is not None]
            rd = f"; peers' bridge readout unedited (late band, J++ hit@100 - ctrl bridge) {round(mean(rv), 3)} (n {len(rv)})" if rv else ""
            lines.append((pre, f"[{st}] {name} ({conv}, peers' implied premise): {lab}; {ps(d)}; {ps(r)}{rd}"))
    # R3': bridgeJ against both bridgeJ_rot and bridgeJ_ctrl, solo loss and press_vis gain, no-shortcut test+dev pooled
    for st, S in strata.items():
        if st.startswith("gated"):
            continue
        es = []
        for conv, kind in (("solo", "loss"), ("press_vis", "gain")):
            es.append(pspec(R, bridge_of, conv, M("bridgeJ"), M("bridgeJ_rot"), kind, S, ("nb",)))
            es.append(pspec(R, bridge_of, conv, M("bridgeJ"), M("bridgeJ_ctrl"), kind, S, ("nb", "nc")))
        E[f"{st} R3'"] = es
        n = min(e["n"] for e in es)
        if not n:
            continue
        ok = all(e["ci"] and e["ci"][0] > 0 for e in es)
        lab = r3_label("the bridge's own directions are needed" if ok else "not shown", st, n)
        pre = "reading:" if st == "no-shortcut, test+dev" else "beside:"
        lines.append((pre, f"[{st}] R3' (bridgeJ vs bridgeJ_rot and bridgeJ_ctrl): {lab}; " + "; ".join(ps(e) for e in es)))
    # the readout dissociation, re-read against bridgeJ_rot (registered on the 27B; on its no-shortcut + landmark items here)
    idxs = [man["read_layers"].index(la) for la in late if la in man["read_layers"]]
    dx = dissociation(R, bridge_of, mid, gated, idxs)
    reg = target in DISSOC_REGISTERED
    dx["status"] = "registered (amendment 73), on this run's items" if reg else "descriptive (amendment 73: seen on this model)"
    out["dissociation"] = dx
    for ln in d_lines(dx):
        lines.append(("reading:" if reg else "descriptive:", f"[gated, test+dev; {dx['status']}] " + ln))
    dh = d_held(R, bridge_of, mid, gated)  # amendment 78
    dreg = target in DHELD_REGISTERED
    dh["status"] = ("registered (amendment 78), on this run's items" if dreg else "post hoc (amendment 78: seen on this model)")
    out["d_held"] = dh
    for ln in dh_lines(dh):
        lines.append(("reading:" if dreg else "post hoc:", f"[gated, test+dev; {dh['status']}] " + ln))
    if R.get(("press_vis", M("bridgeJ_peerperp"))):  # amendment 75, in the same run (Lightning, the 27B)
        out["p1perp"], pl = p1perp_lines(R, bridge_of, M, gated, p1_status(R, bridge_of, M, gated), target, "this run")
        lines += pl
    out["readings"] = [f"{p} {x}" for p, x in lines]
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note54.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"# note 54 (amendments 72-73), {a.run}: {target}; gate {a.gate} (names as written); read {len(read_uids)}, gated {len(gated)} "
          f"(test {sum(split_of[u] == 'test' for u in gated)}, dev {sum(split_of[u] == 'dev' for u in gated)}), no-shortcut {len(nosc)}, "
          f"landmark {len(land)}; ref runs {refs}")  # fmt: skip
    print("rates (% of read items, all read items):")
    for conv in man["args"]["convs"]:
        for bc in ["none"] + [M(c) for c in man["edits"][0][1]]:
            rows = list(R.get((conv, bc), {}).values())
            if rows:
                print(f"  {conv:10s} {bc:24s} n {len(rows):4d}  orig {100 * mean(r['cls'] == 'orig' for r in rows):5.1f}  peer "
                      f"{100 * mean(r['cls'] == 'peer' for r in rows):5.1f}  other {100 * mean(r['cls'] == 'other' for r in rows):5.1f}  "
                      f"|edit|/|h| {mean(r.get('edit_rel', 0.0) for r in rows):.4f}"
                      + (f"  span rank {mean(r['span_rank'] for r in rows):.2f}" if "span_rank" in rows[0] else ""))  # fmt: skip
    print("G2 (from the ref runs): " + "; ".join(f"[{k}] {g2_str(v)}" for k, v in g2.items()))
    for c in check:
        print("check:", c)
    for pre, x in lines:
        print(pre, x)


def main(a) -> None:
    res, man, R, bridge_of, named, g = load(a)
    if a.note42:  # amendment 67 note 42 (a run of the note 42 edits)
        main_note42(a, res, man, R, bridge_of, named)
        return
    if a.note54:  # amendments 72-73 note 54 (a run of the note 54 edits)
        main_note54(a, res, man, R, bridge_of)
        return
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
    full["amendment71_73"], extra = amend71_73(man, R, bridge_of, gate, outs["gated"]["late_layers"])
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
    print(f"\n######## amendment 71 (M) and amendment 73 (readout dissociation) ({a.run}: {man['model'].get('target')}, split "
          f"{man['args'].get('split')}; gated with names as written, {full['amendment71_73']['n_gated']} items, whatever --name-rule is)")
    for pre, line in extra:
        print(pre, line)


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
    ap.add_argument("--note42", action="store_true", help="amendment 67 note 42's reading (a run with the skipown / onlyown edits; needs --gate)")
    ap.add_argument("--solo-run", default=None, help="note 42: the model's main knock-out run, for the split by whether solo recall survives")
    ap.add_argument("--note54", action="store_true", help="amendments 72-73 note 54's readings (a run with the note 54 edits; needs --gate)")
    ap.add_argument("--ref-runs", nargs="*", default=None, help="note 54: the model's note 40 / 47 runs (G2, and the rerun check)")
    ap.add_argument("--p1-run", default=None, help="amendment 75: a P1-perp-only run reads its positive control and P1 from this note 54 run")
    main(ap.parse_args())
