"""nn_v5_read (Zach, 2026-10-29, prereg amendment 60 notes 29-31 and addendum): the three v4-family sets' readings.

python scripts/nn_v5_read.py key PREFIX     note 29: jsuite_v5kn (named, primary) and jsuite_v5kd (described)
python scripts/nn_v5_read.py kc PREFIX      note 30: jsuite_v5kc
python scripts/nn_v5_read.py alias PREFIX   note 31: jsuite_v5al
Writes results/ablate_v2/nn_v5_read/{PREFIX}{set}.json and prints the readings. Windows: note 25's (scripts.nn_priming_read).
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

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"


def items_of(s):
    return {json.loads(l)["id"]: json.loads(l) for l in (DATA / s / "items.jsonl").open()}


def ko_rows(run):
    acc = collections.defaultdict(dict)  # (family, kind, condition) -> id -> correct
    for line in (RES / "ablate_v2" / run / "rows.jsonl").open():
        r = json.loads(line)
        acc[(r["family"], r.get("kind", "clean"), r["condition"])][r["id"]] = bool(r["correct_cand2"])
    return acc


def boot_ci(by: dict, fn, n=2000, seed=0):
    keys, rng, out = sorted(by), random.Random(seed), []
    for _ in range(n):
        v = fn([x for k in (rng.choice(keys) for _ in keys) for x in by[k]])
        if v == v:
            out.append(v)
    out.sort()
    return [round(out[int(0.025 * len(out))], 3), round(out[int(0.975 * len(out)) - 1], 3)] if out else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return 100 * sum(xs) / len(xs) if xs else float("nan")


def readout(run, win):
    hits, fam = collections.defaultdict(list), {}
    p = RES / "nn_readout" / run / "rows.jsonl"
    if not p.exists():
        return None, None
    for line in p.open():
        r = json.loads(line)
        lo, hi = win[r["site"]]
        if lo <= r["layer"] <= hi:
            hits[(r["site"], r["lens"], r["id"], r["what"])].append(r["rank"] == 1)
        fam[r["id"]] = r["family"]
    return {k: sum(v) / len(v) for k, v in hits.items()}, fam


def per_layer(run, ids, site, what, lens="jlens"):
    acc = collections.defaultdict(list)
    for line in (RES / "nn_readout" / run / "rows.jsonl").open():
        r = json.loads(line)
        if r["id"] in ids and r["site"] == site and r["lens"] == lens and r["what"] == what:
            acc[r["layer"]].append(r["rank"] == 1)
    return {la: round(100 * sum(v) / len(v), 1) for la, v in sorted(acc.items())}


def key(P):
    win, out = windows(P), {}
    for tag, step in (("v5kn", "step2"), ("v5kd", "step3")):
        s = f"jsuite_{tag}_test_chat"
        items = items_of(s)
        run = f"{P}{s}_ko_cand2_v1"
        if not (RES / "ablate_v2" / run / "rows.jsonl").exists():
            continue
        acc = ko_rows(run)
        rec = {"n": {f: len(acc.get((f, "clean", "none"), {})) for f in ("MP", "MM")}}
        for flag in ("all", "no_flag_colour"):
            for cond in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize"):
                if ("MP", "clean", cond) not in acc:
                    continue
                ids = [i for i in acc[("MP", "clean", "none")] if i in acc.get(("MP", step, "none"), {}) and (flag == "all" or not items[i].get("flag_colour_match"))]
                by = collections.defaultdict(list)
                for i in ids:  # per item: whole loss minus the direct key lookup's loss (1 / 0 / -1 each)
                    lw = acc[("MP", "clean", "none")][i] - acc[("MP", "clean", cond)][i]
                    ls = acc[("MP", step, "none")][i] - acc[("MP", step, cond)][i]
                    by[items[i]["bridge"]].append((lw, ls))
                xs = [x for v in by.values() for x in v]
                mm = acc.get(("MM", "clean", "none"), {})
                mm_loss = mean([mm[i] - acc[("MM", "clean", cond)][i] for i in mm]) if mm else float("nan")
                rec[f"{flag}/{cond}"] = {"n_items": len(xs), "loss_MP": round(mean([a for a, _ in xs]), 1), "loss_lookup": round(mean([b for _, b in xs]), 1),
                                         "contrast": round(mean([a - b for a, b in xs]), 1), "ci": boot_ci(by, lambda us: mean([a - b for a, b in us])),
                                         "loss_MM": round(mm_loss, 1)}  # fmt: skip
        c, r = rec.get("all/paper10"), rec.get("all/paper10_rot")
        if c and r and c["ci"]:
            if c["contrast"] >= 15 and c["ci"][0] > 0 and r["contrast"] < 5 and c["loss_MP"] >= 0.5 * c["loss_MM"]:
                rec["reading1"] = "a remembered word used, not said, needs the J-space"
            elif c["contrast"] < 10 and c["ci"][1] < 15:
                rec["reading1"] = "goes around"
            else:
                rec["reading1"] = "mixed"
        # reading 3: priming at the bridge site and the key before the value at the final token
        val, fam = readout(f"{P}nn_readout_{tag}_v1", win)
        if val:
            sc = collections.defaultdict(dict)
            for i, f in fam.items():
                sc[i.split(":")[-1].split("-", 1)[1]][f] = i
            pairs = [(items[d["MP_ok"]]["bridge"], d) for d in sc.values() if "MP_ok" in d and "MM_ok" in d]
            g = lambda i, w, site="desc_end": val.get((site, "jlens", i, w))  # noqa: E731

            def rho(us):
                den = mean([g(d["MM_ok"], "attr") for d in us]) - mean([g(d["MM_ok"], "third") for d in us])
                return (mean([g(d["MP_ok"], "key") for d in us]) - mean([g(d["MP_ok"], "keythird") for d in us])) / den if den > 0 else float("nan")

            by = collections.defaultdict(list)
            for b, d in pairs:
                by[b].append(d)
            ds = [d for _, d in pairs]
            rec["priming"] = {"n_pairs": len(ds), "MP_key": round(mean([g(d["MP_ok"], "key") for d in ds]), 1), "MP_keythird": round(mean([g(d["MP_ok"], "keythird") for d in ds]), 1),
                              "MM_attr": round(mean([g(d["MM_ok"], "attr") for d in ds]), 1), "MM_third": round(mean([g(d["MM_ok"], "third") for d in ds]), 1),
                              "rho": round(rho(ds), 3), "rho_ci": boot_ci(by, rho)}  # fmt: skip
            mp_ok = {d["MP_ok"] for d in ds}
            k_l, t_l, v_l = (per_layer(f"{P}nn_readout_{tag}_v1", mp_ok, "final", w) for w in ("key", "keythird", "attr"))
            lo, hi = win["final"]
            first_v = min([la for la, x in v_l.items() if x > 50] or [99])
            early = [la for la in k_l if lo <= la <= hi and la < first_v and k_l[la] - t_l.get(la, 0) >= 10]
            rec["final_by_layer"] = {"key": k_l, "keythird": t_l, "colour": v_l, "first_colour_layer_over_50": first_v,
                                     "key_before_value": bool(early), "layers": early}  # fmt: skip
        out[tag] = rec
    return out


def kc(P):
    win, s = windows(P), "jsuite_v5kc_test_chat"
    items = items_of(s)
    norm = lambda x: (x or "").strip().lower()  # noqa: E731
    comp = collections.defaultdict(dict)
    for line in (RES / "tasks_v2" / f"{P}{s}_competence_cand2_v1" / "items.jsonl").open():
        r = json.loads(line)
        comp[r["id"]][r["part"]] = r
    cv = {}
    for line in (RES / "competence_variants" / f"{P}jsuite_v5kcctl_cv_v1" / "rows.jsonl").open():
        r = json.loads(line)
        cv[r["id"]] = r

    def known(i):
        suf = i.split(":")[-1].split("-", 1)[1]
        h2 = cv.get(f"j3:chat:v5kc:H2-{suf}", {}).get("correct_cand2")
        h1 = cv.get(f"j3:chat:v5kc:H1-{suf}", {}).get("correct_cand2")
        return bool(h2) and (items[i]["named"] or bool(h1))

    def label(i):
        it, top = items[i], norm(comp[i]["whole"].get("read_top"))
        match = lambda v: bool(top) and bool(v) and (norm(v).startswith(top) or top.startswith(norm(v)))  # noqa: E731
        return "memory" if match(it["real"]) else "passage" if match(it.get("false_value")) else "other"

    out = {"behaviour": {}, "knockout": {}, "bridge": {}, "framing": {}}
    elig = {i for i in items if i in comp and known(i)}
    for w in ("CN", "CA", "DN", "DA", "TN", "TD"):
        ids = [i for i in elig if items[i]["word"] == w]
        c = collections.Counter(label(i) for i in ids)
        out["behaviour"][w] = {"n": len(ids), **{k: round(100 * c[k] / max(1, len(ids)), 1) for k in ("memory", "passage", "other")}}
    run = f"{P}{s}_ko_cand2_v1"
    if (RES / "ablate_v2" / run / "rows.jsonl").exists():
        # answer source under each condition from the knock-out rows' top token, against each item's true and false values
        src = collections.defaultdict(dict)
        tokmap = None
        for line in (RES / "ablate_v2" / run / "rows.jsonl").open():
            r = json.loads(line)
            if r["id"] in elig and r.get("kind", "clean") == "clean" and items[r["id"]]["word"] in ("CN", "DN"):
                src[r["condition"]][r["id"]] = r
        # rows carry the top token id; the source label needs the tokenizer's first tokens of the two values
        from transformers import AutoTokenizer  # noqa: E402
        from bridge_jspace import pins  # noqa: E402

        pin = pins.TARGETS[pins.TARGET]
        tok = AutoTokenizer.from_pretrained(pin["repo"], revision=pin.get("revision"), local_files_only=True)
        first = lambda v: {tok(" " + v, add_special_tokens=False)["input_ids"][0], tok(v, add_special_tokens=False)["input_ids"][0]}  # noqa: E731
        lab = lambda i, r: "passage" if r["pick2"] in first(items[i]["false_value"]) else "memory" if r["pick2"] in first(items[i]["real"]) else "other"  # noqa: E731
        share = {c: collections.Counter(lab(i, r) for i, r in rows.items()) for c, rows in src.items()}
        out["knockout"]["share"] = {c: {k: round(100 * v[k] / max(1, sum(v.values())), 1) for k in ("memory", "passage", "other")} for c, v in share.items()}
        if "none" in src:
            ids = sorted(src["none"])
            for c in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize"):
                if c not in src:
                    continue
                by = collections.defaultdict(list)
                for i in ids:
                    by[items[i]["bridge"]].append((lab(i, src[c][i]) == "passage") - (lab(i, src["none"][i]) == "passage"))
                out["knockout"][f"shift_{c}"] = {"shift": round(mean([x for v in by.values() for x in v]), 1), "ci": boot_ci(by, lambda us: mean(us))}
            for ctl in ("paper10_rot", "unembed10"):
                if ctl in src and "paper10" in src:
                    by = collections.defaultdict(list)
                    for i in ids:
                        by[items[i]["bridge"]].append((lab(i, src["paper10"][i]) == "passage") - (lab(i, src[ctl][i]) == "passage"))
                    d = mean([x for v in by.values() for x in v])
                    ci = boot_ci(by, lambda us: mean(us))
                    out["knockout"][f"paper10_minus_{ctl}"] = {"d": round(d, 1), "ci": ci, "met": bool(ci) and d >= 10 and ci[0] > 0}
    val, fam = readout(f"{P}nn_readout_v5kc_v1", win)
    if val:
        for w in ("CN", "DN", "CA", "DA"):
            for lens in ("jlens", "logit"):
                grp = {"memory": [], "passage": []}
                for i in elig:
                    if items[i]["word"] == w and label(i) in grp:
                        grp[label(i)].append((items[i]["bridge"], i))
                g = lambda i, t: val.get(("desc_end", lens, i, t))  # noqa: E731
                rec = {o: {"n": len(v), **{t: round(mean([g(i, t) for _, i in v]), 1) for t in ("attr", "other", "third", "ctxreal")}} for o, v in grp.items()}
                # AUC: memory-wins vs passage-wins from the bridge score (true minus false share)
                sm = [g(i, "attr") - g(i, "other") for _, i in grp["memory"] if g(i, "attr") is not None]
                sp = [g(i, "attr") - g(i, "other") for _, i in grp["passage"] if g(i, "attr") is not None]
                auc = (sum((a > b) + 0.5 * (a == b) for a in sm for b in sp) / (len(sm) * len(sp))) if sm and sp else None
                rec["auc"] = round(auc, 3) if auc is not None else None
                if lens == "jlens" and rec["memory"]["n"] and rec["passage"]["n"]:
                    m, p = rec["memory"], rec["passage"]
                    rec["reading"] = ("memory channel" if abs(p["attr"] - m["attr"]) <= 10 and p["other"] <= p["third"] + 3 else
                                      "current belief" if p["other"] >= p["third"] + 10 else
                                      "memory strength" if m["attr"] - p["attr"] >= 10 else "mixed")  # fmt: skip
                out["bridge"][f"{w}/{lens}"] = rec
        for a, b in (("CN", "CA"), ("DN", "DA")):  # framing, paired by scene (eligible)
            suf = lambda i: i.split(":")[-1].split("-", 1)[1]  # noqa: E731
            pa = {suf(i): i for i in elig if items[i]["word"] == a}
            pb = {suf(i): i for i in elig if items[i]["word"] == b}
            both = sorted(set(pa) & set(pb))
            g = lambda i: val.get(("desc_end", "jlens", i, "attr"))  # noqa: E731
            out["framing"][f"{a}->{b}"] = {"n": len(both), "bridge_true_share_change": round(mean([g(pb[x]) for x in both]) - mean([g(pa[x]) for x in both]), 1),
                                           "passage_share_change": round(mean([label(pb[x]) == "passage" for x in both]) - mean([label(pa[x]) == "passage" for x in both]), 1)}  # fmt: skip
    return out


def alias(P):
    win, s = windows(P), "jsuite_v5al_test_chat"
    out = {}
    run = f"{P}{s}_ko_cand2_v1"
    if (RES / "ablate_v2" / run / "rows.jsonl").exists():
        sys.path.insert(0, str(ROOT / "scripts"))
        from scripts.nn_ko_read import main as ko

        out["knockout"] = ko(run)
        g = out["knockout"]["conditions"].get("paper10", {})
        out["reading1"] = bool(g) and g["gap"] >= 10 and g["gap_ci"][0] > 0
    items = items_of(s)
    val, fam = readout(f"{P}nn_readout_v5al_v1", win)
    if val:
        sc = collections.defaultdict(dict)
        for i, f in fam.items():
            sc[i.split(":")[-1].split("-", 1)[1]][f] = i
        units = []
        for d in sc.values():
            for f, rem in (("MM_ok", "attr"), ("MP_ok", "other")):
                if f in d:
                    i = d[f]
                    g = lambda t, i=i: val.get(("desc_end", "jlens", i, t))  # noqa: E731
                    units.append((items[i]["bridge"], (g(rem), g("third"), g("ctxreal"), f)))
        by = collections.defaultdict(list)
        for b, u in units:
            by[b].append(u)
        xs = [u for _, u in units]
        d1 = mean([(a or 0) - (t or 0) for a, t, _, _ in xs])
        d2 = mean([(a or 0) - (c or 0) for a, _, c, _ in xs if c is not None])
        ci1 = boot_ci(by, lambda us: mean([(a or 0) - (t or 0) for a, t, _, _ in us]))
        ci2 = boot_ci(by, lambda us: mean([(a or 0) - (c or 0) for a, _, c, _ in us if c is not None]))
        out["priming"] = {"n": len(xs), "remembered": round(mean([a for a, _, _, _ in xs]), 1), "third": round(mean([t for _, t, _, _ in xs]), 1),
                          "ctxreal": round(mean([c for _, _, c, _ in xs]), 1), "rem_minus_third": round(d1, 1), "ci": ci1,
                          "rem_minus_ctxreal": round(d2, 1), "ci_ctxreal": ci2}  # fmt: skip
        out["reading2"] = ("identity carries the attribute into the J-space" if d1 >= 10 and ci1 and ci1[0] > 0 and d2 >= 5 and ci2 and ci2[0] > 0 else
                           "scene-level association, not this identity" if d1 >= 10 and ci1 and ci1[0] > 0 else "not shown")  # fmt: skip
    return out


if __name__ == "__main__":
    which, P = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
    res = {"key": key, "kc": kc, "alias": alias}[which](P)
    d = RES / "ablate_v2" / "nn_v5_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}{which}.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1)[:6000])
