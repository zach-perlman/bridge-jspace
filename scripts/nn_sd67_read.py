"""nn_sd67_read (2026-10-30, prereg amendment 88 note 67 "as decided" and its addendum; CPU): reads a scripts/nn_sd67_datactl.py
ko run: conversations onehop (O), solo (P), ctx2hop (I); per band: none, cityRaw, cityRaw_RE, cityClean, cityClean_RE,
cityClean_RJ, bridgeJperp; every edit from the question's first token.

Roles (amendment 88 addendum): the 27B is primary (its labels decide note 67); the 9B and Lightning are confirmatory, read by
the same rules. Each line names the model and its role.
Items: the run's items (test split, person-birthcity-cntry, round 0 right; first-token collisions are not read), gated as note
62 (amendment 85 addendum 3): R1 and the fit check on the gated items (the gate run's gated_canonical, names as written); R2-P
on the gated items with no shortcut (note 62's R2 population; --r2-pop gated swaps it), the other population beside.
  K share   the share of items whose top-1 first token is a first token of K's aliases (cls orig)
  e - c     loss(e) - loss(c) = K(c) - K(e), points, paired by item, on items read under both; 95% bootstrap over items (2,000
            draws, Random(0), nn_sd62_read.boot); the bootstrap over bridge cities beside (quote it if they disagree)
Readings (as registered):
  fit check   per band, on (O): cityRaw - cityRaw_RE >= 15, lower end > 0; otherwise that band is "not readable"
  R1          on (O): cityClean - cityClean_RE >= 15, lower end > 0, at either band whose fit check is met = "an answer- and
              country-orthogonal removal sees the subject; the J++ null is a lens-coverage fact" (the band is named). Fails
              at every band with the fit check met = "this removal family is blind to the subject; claim 4 is untestable
              with it". No band with the fit check met = "not readable".
  R2-P        only if R1 holds, at R1's band(s): on (P), cityClean - cityClean_RE >= 15, lower end > 0 = "latent two-hop
              recall needs the bridge city's non-answer identity"; a CI half-width > 15 is printed as "underpowered"
  agreement   with the run's gen.jsonl: the unedited first-token read (cls orig) vs the 12-token outcome (original) per
              conversation; < 90% is flagged on every reading of that conversation (no edited generations are made)
  beside      every arm's raw loss per conversation; (I)'s contrast; cityClean - cityClean_RJ (random J++ rows); bridgeJperp
              (note 62's); ranks; the matched sizes k, their energy shares and how often the pool reached the target
python scripts/nn_sd67_read.py RUN --gate {P}sd_gate_v1 [--res results/sd_necessity] [--r2-pop nosc|gated]
Writes results/sd_necessity/nn_sd_read/RUN_note67.json; prints one "reading" line per registered reading.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nn_sd62_read import K, boot, fmt, mean  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "sd_necessity"
KINDS = (("O", "onehop"), ("P", "solo"), ("I", "ctx2hop"))
PRIMARY = "qwen3.6-27b"  # amendment 88 addendum


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--gate", default=None, help="sd stage: the gate run, {P}sd_gate_v1")
    ap.add_argument("--v4", action="store_true", help="a v4-stage run (nn_sd67_datactl.py v4; with --sd-json)")
    ap.add_argument("--sd-json", default=None, help="v4: the sd stage's reader json (R1 gates the v4 readings)")
    ap.add_argument("--res", default=str(RES))
    ap.add_argument("--r2-pop", default="nosc", choices=["nosc", "gated"])
    a = ap.parse_args()
    assert a.v4 or a.gate, "--gate is required for an sd-stage run"
    res = Path(a.res)
    if a.v4:
        return read_v4(a)
    man = json.loads((res / a.run / "manifest.json").read_text())
    R: dict = collections.defaultdict(dict)  # (conv, band, cond) -> uid -> row
    for line in (res / a.run / "rows.jsonl").open():
        r = json.loads(line)
        R[(r["conv"], r["band"], r["cond"])][r["uid"]] = r
    gen: dict = collections.defaultdict(dict)
    if (res / a.run / "gen.jsonl").exists():
        for line in (res / a.run / "gen.jsonl").open():
            x = json.loads(line)
            gen[x["conv"]][x["uid"]] = x["outcome"]
    gdir = res / a.gate if (res / a.gate / "gate.jsonl").exists() else RES / a.gate
    gate = {json.loads(x)["uid"]: json.loads(x) for x in (gdir / "gate.jsonl").read_text().splitlines()}
    read_uids = {u for d in R.values() for u in d}
    missing = sorted(read_uids - set(gate))
    assert not missing, f"{len(missing)} read items have no gate row: wrong --gate run?"
    bridge_of = {u: r["bridge"] for d in R.values() for u, r in d.items()}
    gated = {u for u in read_uids if gate[u]["gated_canonical"]}
    nosc = {u for u in gated if not gate[u]["shortcut"]}
    bands = [b for b, _ in man["edits"]]
    conds_of = {b: cs for b, cs in man["edits"]}
    target = man["model"].get("target")
    role = "PRIMARY" if target == PRIMARY else "confirmatory"
    tag = f"[{target}, {role}]"
    fl = man.get("fit_log") or {}
    out: dict = {"run": a.run, "gate_run": a.gate, "model": man["model"], "role": role, "bands": bands, "fit": man.get("fit"),
                 "fit_sha256": man.get("fit_sha256"), "fit_n_names": man.get("fit_n_names"), "fit_n_classes": man.get("fit_n_classes"),
                 "n_read": len(read_uids), "n_gated": len(gated), "n_no_shortcut": len(nosc), "r2_pop": a.r2_pop, "readings": {}}  # fmt: skip
    print(f"# note 67, {a.run}: {target} ({role}); bands {bands}; fit {man.get('fit_n_names')} cities / {man.get('fit_n_classes')} countries "
          f"(sha256 {str(man.get('fit_sha256'))[:12]}); read {len(read_uids)}, gated {len(gated)}, gated and no shortcut {len(nosc)}")  # fmt: skip
    print(fit_line(fl))

    def uids(conv, band, conds, S):
        base = R.get((conv, "-", "none"), {})
        ds = [R.get((conv, band, c), {}) for c in conds]
        return sorted(u for u in S if u in base and all(u in d for d in ds))

    def spec(conv, band, t, c, uu):  # loss(t) - loss(c)
        T, C = R[(conv, band, t)], R[(conv, band, c)]
        return 100 * mean(K(C[u]) - K(T[u]) for u in uu) if uu else None

    def loss(conv, band, t, uu):
        B_, T = R[(conv, "-", "none")], R[(conv, band, t)]
        return 100 * mean(K(B_[u]) - K(T[u]) for u in uu) if uu else None

    def contrast(conv, band, t, c, S):
        uu = uids(conv, band, (t, c), S)
        if not uu:
            return {"value": None, "ci": None, "ci_bridges": None, "n": 0, "n_bridges": 0}
        br = collections.defaultdict(list)
        for u in uu:
            br[bridge_of[u]].append(u)
        fn = lambda x: spec(conv, band, t, c, x)  # noqa: E731
        return {"value": spec(conv, band, t, c, uu), "ci": boot({u: [u] for u in uu}, fn), "ci_bridges": boot(br, fn), "n": len(uu),
                "n_bridges": len(br), "loss_t": loss(conv, band, t, uu), "loss_c": loss(conv, band, c, uu)}  # fmt: skip

    def show(x):
        return (f"{fmt(x['value'])} {x['ci']} (bridges {x['ci_bridges']}); n {x['n']} ({x['n_bridges']} bridges); loss "
                f"{fmt(x.get('loss_t'))} vs {fmt(x.get('loss_c'))}")  # fmt: skip

    def met(x):
        return x["value"] is not None and x["value"] >= 15 and bool(x["ci"]) and x["ci"][0] > 0

    # agreement (first token vs the unedited 12-token outcome), per conversation, on the gated items
    agree: dict = {}
    for k, conv in KINDS:
        base = R.get((conv, "-", "none"), {})
        uu = [u for u in gated if u in base and u in gen.get(conv, {})]
        if uu:
            agree[conv] = 100 * mean(float((base[u]["cls"] == "orig") == (gen[conv][u] == "original")) for u in uu)
    warn = {conv: (f" [WARNING: first-token agreement {v:.1f}% < 90% in {conv}; no edited generations exist]" if v < 90 else "")
            for conv, v in agree.items()}  # fmt: skip
    print("agreement (gated, unedited first token vs 12-token outcome): "
          + ("; ".join(f"{k} {fmt(agree.get(c))}%" for k, c in KINDS if c in agree) if agree else "no gen.jsonl"))
    out["agreement"] = agree
    # K shares
    for st, S in (("gated", gated), ("gated, no shortcut", nosc)):
        for k, conv in KINDS:
            base = R.get((conv, "-", "none"), {})
            uu = [u for u in S if u in base]
            if not uu:
                continue
            parts = [f"none {100 * mean(K(base[u]) for u in uu):.1f}"]
            for band in bands:
                for c in conds_of[band]:
                    d = R.get((conv, band, c), {})
                    v = [u for u in uu if u in d]
                    if v:
                        parts.append(f"{band}/{c} {100 * mean(K(d[u]) for u in v):.1f}")
            print(f"K share % [{st}] ({k} {conv}, n {len(uu)}): " + "; ".join(parts))
    # fit check and R1 (gated)
    fitc, r1, r1_bands, fit_any = {}, {}, [], False
    for band in bands:
        fc = contrast("onehop", band, "cityRaw", "cityRaw_RE", gated)
        fitc[band] = {**fc, "met": met(fc)}
        fit_any |= met(fc)
        print(f"reading {tag} fit check ({band}, O, cityRaw - cityRaw_RE >= 15, lower end > 0): "
              f"{'met' if met(fc) else 'NOT met: not readable at this band'}; {show(fc)}{warn.get('onehop', '')}")  # fmt: skip
        x = contrast("onehop", band, "cityClean", "cityClean_RE", gated)
        ok = met(x) and met(fc)
        r1[band] = {**x, "met": met(x), "fit_ok": met(fc)}
        if ok:
            r1_bands.append(band)
        lab = ("met" if met(x) else "not met") + ("" if met(fc) else " (fit check not met: not readable)")
        print(f"reading {tag} R1 ({band}, O, cityClean - cityClean_RE >= 15, lower end > 0): {lab}; {show(x)}{warn.get('onehop', '')}")
    if r1_bands:
        lab = f"an answer- and country-orthogonal removal sees the subject; the J++ null is a lens-coverage fact (band {', '.join(r1_bands)})"
    elif fit_any:
        lab = "this removal family is blind to the subject; claim 4 is untestable with it"
    else:
        lab = "not readable (the fit check is not met at any band)"
    print(f"reading {tag} R1 (either band): {lab}{warn.get('onehop', '')}")
    out["readings"].update({"fit_check": fitc, "R1_bands": r1, "R1": {"label": lab, "bands": r1_bands}})
    # R2-P
    pops = (("gated, no shortcut", nosc), ("gated", gated)) if a.r2_pop == "nosc" else (("gated", gated), ("gated, no shortcut", nosc))
    r2 = {}
    for i, (st, S) in enumerate(pops):
        for band in bands:
            x = contrast("solo", band, "cityClean", "cityClean_RE", S)
            hw = None if not x["ci"] else (x["ci"][1] - x["ci"][0]) / 2
            if band not in r1_bands:
                lab2 = "not read (R1 not met at this band)"
            elif met(x):
                lab2 = "latent two-hop recall needs the bridge city's non-answer identity"
            else:
                lab2 = "not met" + (" (underpowered: CI half-width > 15)" if hw is not None and hw > 15 else "")
            pre = f"reading {tag}" if i == 0 and band in r1_bands else "beside:"
            print(f"{pre} R2-P ({band}, P, [{st}], cityClean - cityClean_RE >= 15, lower end > 0): {lab2}; {show(x)}{warn.get('solo', '')}")
            r2[f"{st}/{band}"] = {**x, "label": lab2}
    out["readings"]["R2_P"] = r2
    # beside: I's contrast, the RJ control, bridgeJperp, every arm's loss, ranks and matched sizes
    bes: dict = {}
    for band in bands:
        for k, conv in KINDS:
            parts = []
            for t, c in (("cityClean", "cityClean_RE"), ("cityClean", "cityClean_RJ"), ("cityRaw", "cityRaw_RE")):
                if t in conds_of[band] and c in conds_of[band]:
                    x = contrast(conv, band, t, c, gated)
                    bes[f"{k}/{band}/{t}-{c}"] = x
                    parts.append(f"{t} - {c} {fmt(x['value'])} {x['ci']} (bridges {x['ci_bridges']})")
            if parts:
                print(f"beside: ({k}, {band}, gated) " + "; ".join(parts))
            parts = []
            for c in conds_of[band]:
                uu = uids(conv, band, (c,), gated)
                if not uu:
                    continue
                d = R[(conv, band, c)]
                extra = ""
                if "span_rank" in d[uu[0]]:
                    extra += f", rank {mean(d[u]['span_rank'] for u in uu):.1f}"
                if "k" in d[uu[0]]:
                    extra += (f", k {mean(mean(d[u]['k']) for u in uu):.0f}, energy {100 * mean(mean(d[u]['E_match']) for u in uu):.2f}% "
                              f"vs target {100 * mean(mean(d[u]['E_target']) for u in uu):.2f}%, reached {sum(d[u]['reached'] for u in uu)}/{len(uu)}")  # fmt: skip
                parts.append(f"{c} loss {fmt(loss(conv, band, c, uu))}{extra}")
            if parts:
                print(f"beside: ({k}, {band}, gated, n {len(uids(conv, band, (), gated))}) " + "; ".join(parts))
    out["beside"] = bes
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note67.json").write_text(json.dumps(out, indent=1) + "\n")


def fit_line(fl: dict) -> str:
    return ("# fit ranks per layer (raw / class / clean; clean's share of the centred energy; raw / clean mean share inside the "
            "classes' J++ forms): " + "; ".join(f"L{la} {v['rank_raw']}/{v['rank_class']}/{v['rank_clean']} ({v['energy_in_clean']}; "
                                                f"{v['raw_share_in_class_forms']}/{v['clean_share_in_class_forms']})"
                                                for la, v in sorted(fl.items(), key=lambda kv: int(kv[0]))))  # fmt: skip


def read_v4(a) -> None:
    """The v4 stage (amendment 88 note 67): note 37's v4 items (MP, MM; cand2 read; the run holds only gated items).
      fit check   per band, on MP: entRaw - entRaw_RE >= 15, lower end > 0 (MM printed beside)
      MP control  per band, on MP: entClean - entClean_RE >= 15, lower end > 0; otherwise the v4 stage is "not readable" at
                  that band (the bridge is the lookup key in MP, so its identity must be needed there)
      R2-v4       per band with both met, on MM: entClean - entClean_RE >= 15, lower end > 0 = "latent recall needs the bridge's
                  identity beyond its answer"; read only if the sd stage's R1 holds (--sd-json), else printed as not read"""
    res = Path(a.res)
    man = json.loads((res / a.run / "manifest.json").read_text())
    R: dict = collections.defaultdict(dict)  # (word, band, cond) -> id -> row
    for line in (res / a.run / "rows.jsonl").open():
        r = json.loads(line)
        R[(r["family"], r["band"], r["cond"])][r["id"]] = r
    bridge_of = {u: r["bridge"] for d in R.values() for u, r in d.items()}
    bands = [b for b, _ in man["edits"]]
    conds_of = {b: cs for b, cs in man["edits"]}
    target = man["model"].get("target")
    role = "PRIMARY" if target == PRIMARY else "confirmatory"
    tag = f"[{target}, {role}, v4]"
    r1 = None
    if a.sd_json:
        sd = json.loads(Path(a.sd_json).read_text())
        r1 = sd["readings"]["R1"]["bands"]
    gate_lab = "" if r1 else (" [not read: the sd stage's R1 is not met]" if r1 is not None else " [the sd stage's R1 was not given (--sd-json)]")
    print(f"# note 67 v4 stage, {a.run}: {target} ({role}); bands {bands}; fit {man.get('fit_n_names')} bridges / {man.get('fit_n_classes')} MM "
          f"answers (sha256 {str(man.get('fit_sha256'))[:12]}); prompts {man.get('by_word')}; sd R1 bands {r1}")  # fmt: skip
    print(fit_line(man.get("fit_log") or {}))

    def C(r):
        return float(bool(r["correct"]))

    def spec(w, band, t, c, uu):
        T, Cc = R[(w, band, t)], R[(w, band, c)]
        return 100 * mean(C(Cc[u]) - C(T[u]) for u in uu) if uu else None

    def contrast(w, band, t, c):
        base = R.get((w, "-", "none"), {})
        uu = sorted(u for u in base if u in R.get((w, band, t), {}) and u in R.get((w, band, c), {}))
        if not uu:
            return {"value": None, "ci": None, "ci_bridges": None, "n": 0, "n_bridges": 0}
        br = collections.defaultdict(list)
        for u in uu:
            br[bridge_of[u]].append(u)
        fn = lambda x: spec(w, band, t, c, x)  # noqa: E731
        lt = 100 * mean(C(base[u]) - C(R[(w, band, t)][u]) for u in uu)
        lc = 100 * mean(C(base[u]) - C(R[(w, band, c)][u]) for u in uu)
        return {"value": spec(w, band, t, c, uu), "ci": boot({u: [u] for u in uu}, fn), "ci_bridges": boot(br, fn), "n": len(uu),
                "n_bridges": len(br), "loss_t": lt, "loss_c": lc}  # fmt: skip

    def show(x):
        return (f"{fmt(x['value'])} {x['ci']} (bridges {x['ci_bridges']}); n {x['n']} ({x['n_bridges']} bridges); loss "
                f"{fmt(x.get('loss_t'))} vs {fmt(x.get('loss_c'))}")  # fmt: skip

    def met(x):
        return x["value"] is not None and x["value"] >= 15 and bool(x["ci"]) and x["ci"][0] > 0

    for w in ("MP", "MM"):
        base = R.get((w, "-", "none"), {})
        if not base:
            continue
        parts = [f"none {100 * mean(C(r) for r in base.values()):.1f}"]
        for band in bands:
            for c in conds_of[band]:
                d = R.get((w, band, c), {})
                if d:
                    parts.append(f"{band}/{c} {100 * mean(C(r) for r in d.values()):.1f}")
        print(f"cand2 accuracy % ({w}, n {len(base)}): " + "; ".join(parts))
    out: dict = {"run": a.run, "model": man["model"], "role": role, "bands": bands, "sd_R1_bands": r1, "readings": {}}
    held = []
    for band in bands:
        fc = contrast("MP", band, "entRaw", "entRaw_RE")
        fcm = contrast("MM", band, "entRaw", "entRaw_RE")
        pc = contrast("MP", band, "entClean", "entClean_RE")
        r2 = contrast("MM", band, "entClean", "entClean_RE")
        ok = met(fc) and met(pc)
        print(f"reading {tag} fit check ({band}, MP, entRaw - entRaw_RE >= 15, lower end > 0): {'met' if met(fc) else 'NOT met'}; {show(fc)}")
        print(f"beside: fit check on MM ({band}): {show(fcm)}")
        print(f"reading {tag} MP positive control ({band}, entClean - entClean_RE >= 15, lower end > 0): "
              f"{'met' if met(pc) else 'NOT met: the v4 stage is not readable at this band'}; {show(pc)}")  # fmt: skip
        if not ok:
            lab = "not readable (fit check or MP control not met)"
        elif met(r2):
            lab = "latent recall needs the bridge's identity beyond its answer"
            held.append(band)
        else:
            lab = "not met"
        print(f"reading {tag} R2-v4 ({band}, MM, entClean - entClean_RE >= 15, lower end > 0): {lab}{gate_lab}; {show(r2)}")
        rj = contrast("MM", band, "entClean", "entClean_RJ") if "entClean_RJ" in conds_of[band] else None
        if rj:
            print(f"beside: ({band}) MM entClean - entClean_RJ (random J++ rows) {show(rj)}; MP {show(contrast('MP', band, 'entClean', 'entClean_RJ'))}")
        for w in ("MP", "MM"):
            parts = []
            for c in conds_of[band]:
                d = R.get((w, band, c), {})
                if not d:
                    continue
                v = list(d.values())
                extra = f", rank {mean(r['span_rank'] for r in v):.1f}" if "span_rank" in v[0] else ""
                if "k" in v[0]:
                    extra += (f", k {mean(mean(r['k']) for r in v):.0f}, energy {100 * mean(mean(r['E_match']) for r in v):.2f}% vs target "
                              f"{100 * mean(mean(r['E_target']) for r in v):.2f}%, reached {sum(r['reached'] for r in v)}/{len(v)}")  # fmt: skip
                parts.append(f"{c}{extra}")
            print(f"beside: ({w}, {band}) " + "; ".join(parts))
        out["readings"][band] = {"fit_check": {**fc, "met": met(fc)}, "fit_check_MM": fcm, "MP_control": {**pc, "met": met(pc)},
                                 "R2_v4": {**r2, "label": lab}}  # fmt: skip
    lab = (f"latent recall needs the bridge's identity beyond its answer (band {', '.join(held)})" if held else "not shown at either band") + gate_lab
    print(f"reading {tag} R2-v4 (either band): {lab}")
    out["R2_v4"] = {"label": lab, "bands": held}
    dest = res / "nn_sd_read"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{a.run}_note67v4.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
