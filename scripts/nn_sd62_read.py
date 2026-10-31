"""nn_sd62_read (2026-10-30, prereg amendment 85 note 62; CPU): a positive control for note 54's bridge null. Reads a
scripts/nn_sd_necessity.py ko run with the conversations ctx2hop (I, the in-context two-hop), solo (P, note 54's prompt) and
onehop (O), the mid-band edits paper10, paper10_rot, bridgeJ, bridgeJ_rot, bridgeJ_ctrl (count-matched, --ctrl-match count),
bridgeJperp and ansJ, each acting only from the question's first token (--pos-from question).

Items: the run's items (the silent-dissent split's person-birthcity-cntry items, round 0 right; first-token collisions are not
read by the runner), gated as note 54: gated with names as written (the gate run's gated_canonical) and no direct shortcut
(primary); the gated set with shortcut items is printed beside.
  K share       = the share of items whose first token (top-1 over the vocabulary) is a first token of K's aliases (cls orig)
  loss(e)       = K share(none) - K share(e), points, paired by item
  e - c         = loss(e) - loss(c) on the items read unedited and under both edits whose span counts are > 0 (nb for the
                  bridge edits, nc for bridgeJ_ctrl); 95% bootstrap over items (2,000 draws, Random(0)); the bootstrap over
                  bridge cities is printed beside it
Readings (as registered):
  validity      unedited (I) K share >= 70% on the gated items, else (I) is "not readable" for the model (R1 and R2 are then
                not read); (P) as note 54 (round 0 right and gated by construction; its unedited K share and paper10 -
                paper10_rot loss are printed)
  R1            on (I): bridgeJperp - bridgeJ_ctrl >= 15 AND bridgeJperp - bridgeJ_rot >= 15, both lower ends > 0 = "the
                knock-out sees a needed bridge"; otherwise "the method cannot be shown to detect a bridge" (and note 54 is
                reworded to "found no bridge need; we could not show the test can detect one")
  R2 (given R1) S(k) = bridgeJperp's specific loss in kind k, min over the two controls (bridgeJ_ctrl, bridgeJ_rot).
                S(P) <= S(I) / 3 with the lower end of S(I) - S(P) > 0 = "the bridge is needed when it is a key in context,
                not in latent recall"; S(P) >= 2/3 S(I) = "(P) needs the bridge too" (note 54's null was a masking artefact);
                otherwise "between". Items in both (I) and (P) cells; S(I) - S(P) bootstrapped over items (the min inside).
  beside        bridgeJ (unorthogonalised) and ansJ on (I), (P), (O): raw loss, and bridgeJ against bridgeJ_rot and
                bridgeJ_ctrl; (O)'s bridgeJ loss; paper10 - paper10_rot per kind; in (I), the share whose top token is a
                distractor country (where a lost K goes); bridgeJperp's kept rank and the bridge forms' energy share inside
                the orthogonalising span (4 countries in (I), the two answers in (P) / (O)); nc == nb (count match) share;
                the unedited 12-token outcome (with --gen).

python scripts/nn_sd62_read.py RUN --gate {P}sd_gate_v1 [--res results/sd_necessity]
Writes results/sd_necessity/nn_sd_read/RUN_note62.json; prints one "reading" line per registered reading.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "sd_necessity"
KINDS = (("I", "ctx2hop"), ("P", "solo"), ("O", "onehop"))
NEED = {"bridgeJ": ("nb",), "bridgeJ_rot": ("nb",), "bridgeJperp": ("nb",), "bridgeJ_ctrl": ("nc",)}


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def boot(by: dict, fn, n: int = 2000) -> list | None:
    """95% interval of fn(list of items) over the keys of `by` resampled with replacement (nn_sd_read.boot's)."""
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


def load(res: Path, run: str):
    man = json.loads((res / run / "manifest.json").read_text())
    R: dict = collections.defaultdict(dict)  # (conv, cond) -> uid -> row
    for line in (res / run / "rows.jsonl").open():
        r = json.loads(line)
        R[(r["conv"], r["cond"])][r["uid"]] = r
    g: dict = collections.defaultdict(dict)
    if (res / run / "gen.jsonl").exists():
        for line in (res / run / "gen.jsonl").open():
            x = json.loads(line)
            g[x["conv"]][x["uid"]] = x["outcome"]
    return man, R, g


def K(r: dict) -> float:
    return float(r["cls"] == "orig")


class Reader:
    def __init__(self, R: dict, uids: set, bridge_of: dict):
        self.R, self.uids, self.bridge_of = R, uids, bridge_of

    def items(self, conv: str, conds: tuple) -> list[str]:
        base = self.R.get((conv, "none"), {})
        cells = [self.R.get((conv, c), {}) for c in conds]
        need = {f for c in conds for f in NEED.get(c, ())}
        return sorted(u for u in self.uids if u in base and all(u in d for d in cells) and all(base[u].get(f, 1) for f in need))

    def loss(self, conv: str, cond: str, uu: list) -> float | None:
        base, T = self.R[(conv, "none")], self.R[(conv, cond)]
        return 100 * mean(K(base[u]) - K(T[u]) for u in uu) if uu else None

    def spec(self, conv: str, t: str, c: str, uu: list) -> float | None:  # loss(t) - loss(c) = K(c) - K(t)
        T, C = self.R[(conv, t)], self.R[(conv, c)]
        return 100 * mean(K(C[u]) - K(T[u]) for u in uu) if uu else None

    def cis(self, uu: list, fn) -> tuple:
        items = {u: [u] for u in uu}
        br = collections.defaultdict(list)
        for u in uu:
            br[self.bridge_of[u]].append(u)
        return boot(items, fn), boot(br, fn), len(br)


def fmt(v) -> str:
    return "n/a" if v is None else f"{v:.1f}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--gate", required=True, help="the gate run (scripts/sd_gate.py), {P}sd_gate_v1")
    ap.add_argument("--res", default=str(RES))
    a = ap.parse_args()
    res = Path(a.res)
    man, R, g = load(res, a.run)
    mid = man["edits"][0][0]
    args = man["args"]
    gdir = res / a.gate if (res / a.gate / "gate.jsonl").exists() else RES / a.gate  # (a run moved to scratch: the gate stays in results)
    gate = {json.loads(x)["uid"]: json.loads(x) for x in (gdir / "gate.jsonl").read_text().splitlines()}
    read_uids = {u for d in R.values() for u in d}
    missing = sorted(read_uids - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row (e.g. {missing[:3]}): wrong --gate run?"
    bridge_of = {u: r["bridge"] for d in R.values() for u, r in d.items()}
    gated = {u for u in read_uids if gate[u]["gated_canonical"]}
    nosc = {u for u in gated if not gate[u]["shortcut"]}
    out: dict = {"run": a.run, "gate_run": a.gate, "model": man["model"], "band": mid, "pos_from": args.get("pos_from"),
                 "ctrl_match": args.get("ctrl_match"), "n_read": len(read_uids), "n_gated": len(gated), "n_no_shortcut": len(nosc),
                 "strata": {}}  # fmt: skip
    print(f"# note 62, {a.run}: {man['model'].get('target')}; band {mid}; pos_from {args.get('pos_from')}; ctrl_match "
          f"{args.get('ctrl_match')}; gate {a.gate} (names as written); read {len(read_uids)}, gated {len(gated)}, gated and no "
          f"shortcut {len(nosc)} (primary)")  # fmt: skip
    if args.get("pos_from") != "question" or args.get("ctrl_match") != "count":
        print("# WARNING: the registered run is --pos-from question --ctrl-match count; this run is not")
    for st, S in (("gated, no shortcut", nosc), ("gated", gated)):
        prim = st == "gated, no shortcut"
        pre = "reading" if prim else "beside: reading"
        rd = Reader(R, S, bridge_of)
        js: dict = {"n": len(S)}
        print(f"\n## [{st}] n {len(S)}")
        # rates table
        print("K share % (first token; n):")
        for k, conv in KINDS:
            parts = []
            for cond in ["none"] + man["edits"][0][1]:
                d = R.get((conv, cond), {})
                uu = [u for u in S if u in d]
                if uu:
                    parts.append(f"{cond} {100 * mean(K(d[u]) for u in uu):.1f}")
            print(f"  {k} {conv:8s} " + "; ".join(parts) + f" (n {len([u for u in S if u in R.get((conv, 'none'), {})])})")
        # validity
        base_i = R.get(("ctx2hop", "none"), {})
        ui = [u for u in S if u in base_i]
        vi = 100 * mean(K(base_i[u]) for u in ui) if ui else None
        ci_i = boot({u: [u] for u in ui}, lambda uu: 100 * mean(K(base_i[u]) for u in uu)) if ui else None
        readable = vi is not None and vi >= 70
        lab = "readable" if readable else "not readable"
        print(f"{pre} validity (I): unedited first-token K share {fmt(vi)} {ci_i} (n {len(ui)}; >= 70 required): {lab}")
        base_p = R.get(("solo", "none"), {})
        up = rd.items("solo", ("paper10", "paper10_rot"))
        vp = 100 * mean(K(base_p[u]) for u in up) if up else None
        g1 = rd.spec("solo", "paper10", "paper10_rot", up)
        g1ci = rd.cis(up, lambda uu: rd.spec("solo", "paper10", "paper10_rot", uu))[0] if up else None
        print(f"{pre} validity (P) as note 54 (round 0 right, gated): unedited K share {fmt(vp)} (n {len(up)}); paper10 - "
              f"paper10_rot loss {fmt(g1)} {g1ci}")  # fmt: skip
        js["validity"] = {"I_K_none": vi, "I_ci": ci_i, "I_n": len(ui), "I_readable": readable, "P_K_none": vp, "P_n": len(up),
                          "P_paper10_spec": g1, "P_paper10_spec_ci": g1ci}  # fmt: skip
        # R1
        S_of: dict = {}
        r1 = {}
        for k, conv in KINDS:
            uu = rd.items(conv, ("bridgeJperp", "bridgeJ_ctrl", "bridgeJ_rot"))
            if not uu:
                continue
            ec, er = rd.spec(conv, "bridgeJperp", "bridgeJ_ctrl", uu), rd.spec(conv, "bridgeJperp", "bridgeJ_rot", uu)
            cc, cb, nbr = rd.cis(uu, lambda x, c=conv: rd.spec(c, "bridgeJperp", "bridgeJ_ctrl", x))
            rc, rb, _ = rd.cis(uu, lambda x, c=conv: rd.spec(c, "bridgeJperp", "bridgeJ_rot", x))
            r1[k] = {"n": len(uu), "n_bridges": nbr, "perp_minus_ctrl": ec, "ci": cc, "ci_bridges": cb, "perp_minus_rot": er,
                     "ci_rot": rc, "ci_rot_bridges": rb, "loss_perp": rd.loss(conv, "bridgeJperp", uu),
                     "loss_ctrl": rd.loss(conv, "bridgeJ_ctrl", uu), "loss_rot": rd.loss(conv, "bridgeJ_rot", uu)}  # fmt: skip
            S_of[k] = (uu, conv)
        js["R1_cells"] = r1
        if "I" in r1:
            x = r1["I"]
            met = (x["perp_minus_ctrl"] >= 15 and x["perp_minus_rot"] >= 15 and x["ci"] and x["ci_rot"] and x["ci"][0] > 0 and x["ci_rot"][0] > 0)
            lab = ("the knock-out sees a needed bridge" if met else "the method cannot be shown to detect a bridge (note 54 is reworded: "
                   "found no bridge need; we could not show the test can detect one)")  # fmt: skip
            if not readable:
                lab = f"not readable ((I) validity failed; the rule alone: {'met' if met else 'not met'})"
                met = False
            print(f"{pre} R1 (I, bridgeJperp vs bridgeJ_ctrl and bridgeJ_rot, >= 15 each, lower ends > 0): {lab}; perp - ctrl "
                  f"{fmt(x['perp_minus_ctrl'])} {x['ci']} (bridges {x['ci_bridges']}); perp - rot {fmt(x['perp_minus_rot'])} {x['ci_rot']} "
                  f"(bridges {x['ci_rot_bridges']}); n {x['n']} ({x['n_bridges']} bridges); loss perp {fmt(x['loss_perp'])}, ctrl "
                  f"{fmt(x['loss_ctrl'])}, rot {fmt(x['loss_rot'])}")  # fmt: skip
        else:
            met = False
            print(f"{pre} R1: not read (no (I) rows with all three edits)")
        js["R1"] = met
        for k in ("P", "O"):
            if k in r1:
                x = r1[k]
                print(f"beside: ({k}) bridgeJperp - ctrl {fmt(x['perp_minus_ctrl'])} {x['ci']}; - rot {fmt(x['perp_minus_rot'])} {x['ci_rot']}; "
                      f"n {x['n']}; loss perp {fmt(x['loss_perp'])}, ctrl {fmt(x['loss_ctrl'])}, rot {fmt(x['loss_rot'])}")  # fmt: skip
        # R2
        if "I" in S_of and "P" in S_of:
            uu = sorted(set(S_of["I"][0]) & set(S_of["P"][0]))

            def s_of(conv, x):
                v = [rd.spec(conv, "bridgeJperp", c, x) for c in ("bridgeJ_ctrl", "bridgeJ_rot")]
                return None if any(y is None for y in v) else min(v)

            si, sp = s_of("ctx2hop", uu), s_of("solo", uu)
            dci, dcb, nbr = rd.cis(uu, lambda x: (lambda a_, b_: None if a_ is None or b_ is None else a_ - b_)(s_of("ctx2hop", x), s_of("solo", x)))
            if not met:
                lab2 = "not read (R1 not met)"
            elif si is None or sp is None or si <= 0:
                lab2 = "not read (S(I) <= 0)"
            elif sp <= si / 3 and dci and dci[0] > 0:
                lab2 = "the bridge is needed when it is a key in context, not in latent recall"
            elif sp >= 2 * si / 3:
                lab2 = "(P) needs the bridge too (note 54's null was a masking artefact)"
            else:
                lab2 = "between (neither rule met)"
            print(f"{pre} R2 (S(P) <= S(I)/3 with S(I) - S(P) lower end > 0): {lab2}; S(I) {fmt(si)}, S(P) {fmt(sp)}, S(I) - S(P) "
                  f"{fmt(None if si is None or sp is None else si - sp)} {dci} (bridges {dcb}); n {len(uu)} ({nbr} bridges)")  # fmt: skip
            js["R2"] = {"label": lab2, "S_I": si, "S_P": sp, "ci": dci, "ci_bridges": dcb, "n": len(uu)}
        else:
            print(f"{pre} R2: not read (no paired (I) and (P) cells)")
        # beside: bridgeJ and ansJ on I, P, O; paper10 - rot; O's bridgeJ loss
        bes: dict = {}
        for k, conv in KINDS:
            line = []
            for t, c in (("bridgeJ", None), ("bridgeJ", "bridgeJ_rot"), ("bridgeJ", "bridgeJ_ctrl"), ("ansJ", None), ("paper10", "paper10_rot")):
                conds = (t,) if c is None else (t, c)
                uu = rd.items(conv, conds)
                if not uu:
                    continue
                if c is None:
                    v = rd.loss(conv, t, uu)
                    ci = rd.cis(uu, lambda x, cv=conv, tt=t: rd.loss(cv, tt, x))[0]
                    name = f"{t} loss"
                else:
                    v = rd.spec(conv, t, c, uu)
                    ci = rd.cis(uu, lambda x, cv=conv, tt=t, cc=c: rd.spec(cv, tt, cc, x))[0]
                    name = f"{t} - {c}"
                bes[f"{k}:{name}"] = {"value": v, "ci": ci, "n": len(uu)}
                line.append(f"{name} {fmt(v)} {ci} (n {len(uu)})")
            if line:
                print(f"beside: ({k}, {conv}) " + "; ".join(line))
        js["beside"] = bes
        # descriptive: where (I)'s lost K goes; spans; count match; 12-token outcome
        di = []
        for cond in ["none"] + man["edits"][0][1]:
            d = R.get(("ctx2hop", cond), {})
            uu = [u for u in S if u in d]
            if uu and "ctx_dist" in d[uu[0]]:
                di.append(f"{cond} {100 * mean(float(d[u]['ctx_dist']) for u in uu):.1f}")
        if di:
            print("beside: (I) top token = a distractor country, %: " + "; ".join(di))
        sp_ = []
        for k, conv in KINDS:
            d = R.get((conv, "bridgeJperp"), {})
            uu = [u for u in S if u in d]
            if uu:
                sh = [d[u].get("ans_share") for u in uu if d[u].get("ans_share") is not None]
                sp_.append(f"{k} rank {mean(d[u]['span_rank'] for u in uu):.2f}, energy share in the orthogonalising span "
                           f"{fmt(None if not sh else 100 * mean(sh))}%")  # fmt: skip
        if sp_:
            print("beside: bridgeJperp spans: " + "; ".join(sp_))
        base = R.get(("solo", "none"), {})
        uu = [u for u in S if u in base]
        if uu:
            print(f"beside: count match: nc == nb on {sum(base[u]['nc'] == base[u]['nb'] for u in uu)} of {len(uu)} items; mean nb "
                  f"{mean(base[u]['nb'] for u in uu):.2f}, nc {mean(base[u]['nc'] for u in uu):.2f}")  # fmt: skip
        if g:
            parts = []
            for k, conv in KINDS:
                uu = [u for u in S if u in g.get(conv, {})]
                if uu:
                    c = collections.Counter(g[conv][u] for u in uu)
                    parts.append(f"{k} original {100 * c['original'] / len(uu):.1f}% (n {len(uu)})")
            print("beside: unedited 12-token outcome: " + "; ".join(parts))
        out["strata"][st] = js
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note62.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
