"""results_digest (Zach, 2026-10-26): one generated table of every model's v2 results, read straight from the result
files (no hand-copied numbers), for the write-up and its verification. Missing runs print as "-".

python scripts/results_digest.py  ->  docs/digest.md (and prints it)
"""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"

# model: (label, test KO run, band, set, swap run at the band, mid-depth swap run, probe run, variance run, xrel run, renderings)
MODELS = [
    ("Qwen3.6-27B", "jsuite_v2_test_chat_ko_cand2_v1", "L32-40", "jsuite_v2_test_chat", "jswap_v2_v1", None,
     "probe_ceiling_L32-40_v1", "jsuite_v2_test_chat_ko_cand2_L32-40_pca_v1", "jswap_xrel_v2_v1",
     ["jsuite_v2r2_test_chat_ko_cand2_s150_v1", "jsuite_v2r3_test_chat_ko_cand2_s150_v1"]),
    ("Qwen3.5-9B", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "L12-16", "jsuite_v2_test_chat", "qwen35_9b_jswap_v2_v1", None,
     "qwen35_9b_probe_ceiling_L12-16_v1", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_L12-16_pca_v1", "qwen35_9b_jswap_xrel_v2_v1",
     ["qwen35_9b_jsuite_v2r2_test_chat_ko_cand2_v1", "qwen35_9b_jsuite_v2r3_test_chat_ko_cand2_v1"]),
    ("DeepSeek-V4-Flash", "dsv4f_jsuite_v2_test_chat_ko_cand2_L18-23_v1", "L18-23", "jsuite_v2_test_chat", None, "dsv4f_jswap_v2_L22-27_v1",
     "dsv4f_probe_ceiling_L18-23_v1", "dsv4f_jsuite_v2_test_chat_ko_cand2_L18-23_pca_v1", None, []),
    ("Ministral-3-14B", "min14_jsuite_v2_test_chat_ko_cand2_v1", "L32-37", "jsuite_v2_test_chat", "min14_jswap_v2_v1", "min14_jswap_v2_L20-25_v1",
     "min14_probe_ceiling_L20-25_v1", "min14_jsuite_v2_test_chat_ko_cand2_L32-37_pca_v1", None, []),
    ("Nemotron-3.5-Lightning", "nem35l_jsuite_v2_test_chat_ko_cand2_v1", "L27-33", "jsuite_v2_test_chat", "nem35l_jswap_v2_v1", "nem35l_jswap_v2_L26-32_v1",
     "nem35l_probe_ceiling_L27-33_v1", "nem35l_jsuite_v2_test_chat_ko_cand2_L27-33_pca_v1", "nem35l_jswap_xrel_v2_v1",
     ["nem35l_jsuite_v2r2_test_chat_ko_cand2_s150_v1", "nem35l_jsuite_v2r3_test_chat_ko_cand2_s150_v1"]),
    ("Nemotron-3.5-Bolt", "nem35b_jsuite_v2_test_chat_ko_cand2_v1", "L42-53", "jsuite_v2_test_chat", "nem35b_jswap_v2_v1", "nem35b_jswap_v2_L44-55_v1",
     None, None, None, []),
    ("Muse-Glimmer-30B", "muse30_jsuite_v2_test_chat_ko_cand2_v1", "L36-42", "jsuite_v2_test_chat", None, None, None, None, None, []),
    ("Qwen3.5-122B", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1", "L39-45", "jsuite_v2_test_chat", None, None, None, None, None, []),
    ("OLMo-3-32B (base, Q&A)", "olmo32_jsuite_v2_test_qa_ko_cand2_L12-20_v1", "L12-20", "jsuite_v2_test_qa", "olmo32_jswap_v2_v1", None, None, None, None, []),
]


def load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def mk(run: str | None, cond: str = "paper10"):
    s = load(RES / "ablate_v2" / "jsuite2_score" / f"{run}.json") if run else None
    cell = (s or {}).get("facts", {}).get(f"{cond}/start=all")
    if not cell or "M-K" not in cell["contrasts"]:
        return None
    c = cell["contrasts"]["M-K"]
    return {"d": c["diff"], "ci": c["ci"], "K": cell["loss"].get("K"), "M": cell["loss"].get("M"), "P": cell["loss"].get("P"), "n": cell["n"].get("M")}


def fmt_mk(x, ci=True) -> str:
    if not x:
        return "-"
    return f"{x['d']:+.0f} [{x['ci'][0]}, {x['ci'][1]}]" if ci else f"{x['d']:+.0f}"


def soft(run: str | None, cond: str = "paper10") -> str:
    s = load(RES / "ablate_v2" / "soft_score" / f"{run}.json") if run else None
    c = (s or {}).get(cond)
    return f"{c['soft_M-K']:+.0f} [{c['soft_ci'][0]}, {c['soft_ci'][1]}]" if c else "-"


def swap(run: str | None, key: str = "PM") -> str:
    s = load(RES / "jswap" / run / "summary.json") if run else None
    if not s or f"{key}/swap" not in s:
        return "-"
    g = lambda c: s.get(f"{key}/{c}", {}).get("transfer")  # noqa: E731
    return f"swap {g('swap'):+.0f} / paste {g('paste'):+.0f} / comp {g('swap_comp'):+.0f} / u {g('swap_u'):+.0f} (n {s[key + '/swap']['n']})"


def xrel(run: str | None) -> str:
    s = load(RES / "jswap" / run / "summary.json") if run else None
    if not s:
        return "-"
    a, b = s["memory/swap_xrel"]["transfer"], s["memory/swap_srel"]["transfer"]
    return f"xrel {a:+.0f} / srel {b:+.0f} (ratio {a / b:.2f}; n {s['memory/swap_xrel']['n']})"


def probe(run: str | None) -> tuple[str, str]:
    d = RES / "probe_ceiling" / run if run else None
    ro, s = (load(d / "readout.json"), load(d / "summary.json")) if d else (None, None)
    if not ro or not s:
        return "-", "-"
    band = s.get("band") or json.loads((d / "manifest.json").read_text())["band"]
    lo, hi = map(int, band.split("-"))
    num = den = 0.0
    for v in ro.values():
        ls = [str(la) for la in range(lo, hi + 1) if str(la) in v["by_layer"]]
        p = sum(v["by_layer"][la]["probe"] for la in ls) / len(ls)
        j = sum(v["by_layer"][la]["jlens"] for la in ls) / len(ls)
        if v.get("probe_valid") and p - v["chance"] > 0.10:
            num += v["n_test"] * (j - v["chance"])
            den += v["n_test"] * (p - v["chance"])
    valid = s.get("probe_valid_relations", [])
    read = f"{num / den:.2f} on {', '.join(valid)}" if den else "no valid relation"
    sw, sp = s.get("memory_valid/swap", {}).get("transfer"), s.get("memory_valid/swap_probe", {}).get("transfer")
    return read, (f"J++ {sw:+.0f} vs probe {sp:+.0f} (n {s['memory_valid/swap']['n']})" if sw is not None else "-")


# pointer tests (amendment 51): model -> jswap_pointer run
POINTER = [("Qwen3.6-27B", "jswap_pointer_v2_s150_v1"), ("Qwen3.5-9B", "qwen35_9b_jswap_pointer_v2_s150_v1"),
           ("Nemotron-3.5-Lightning", "nem35l_jswap_pointer_v2_s150_v1")]  # fmt: skip
# removal size at the knock-out band (median share of the residual norm removed): model -> removal_size run
SIZE = [("Qwen3.6-27B", "removal_size_pca_L32-40_v1"), ("Qwen3.5-9B", "qwen35_9b_removal_size_pca_L12-16_v1"),
        ("DeepSeek-V4-Flash", "dsv4f_removal_size_pca_L18-23_v1"), ("Ministral-3-14B", "min14_removal_size_pca_L32-37_v1"),
        ("Nemotron-3.5-Lightning", "nem35l_removal_size_pca_L27-33_v1"), ("Nemotron-3.5-Bolt", "nem35b_removal_size_L42-53_v1")]  # fmt: skip
# dose in K (amendments 52, 53): model, KO band, swap band, removal_size runs at each, then per K:
# (K, test KO run, J++ / rotated / logit-lens conditions, jswap run)
DOSE = [
    ("Nemotron-3.5-Bolt", "L42-53", "L42-53", "nem35b_removal_size_L42-53_v1", "nem35b_removal_size_L42-53_v1", [
        (10, "nem35b_jsuite_v2_test_chat_ko_cand2_v1", "paper10", "paper10_rot", "unembed10", "nem35b_jswap_v2_v1"),
        (30, "nem35b_jsuite_v2_test_chat_ko_cand2_L42-53_k30k100_v1", "top30", "top30_rot", "unembed30", "nem35b_jswap_v2_k30_v1"),
        (100, "nem35b_jsuite_v2_test_chat_ko_cand2_L42-53_k30k100_v1", "top100", "top100_rot", "unembed100", "nem35b_jswap_v2_k100_v1")]),
    ("Ministral-3-14B", "L32-37", "L20-25", "min14_removal_size_L32-37_k_v1", "min14_removal_size_L20-25_k_v1", [
        (10, "min14_jsuite_v2_test_chat_ko_cand2_v1", "paper10", "paper10_rot", "unembed10", "min14_jswap_v2_L20-25_v1"),
        (30, "min14_jsuite_v2_test_chat_ko_cand2_L32-37_k30k100_v1", "top30", "top30_rot", "unembed30", "min14_jswap_v2_L20-25_k30_v1"),
        (100, "min14_jsuite_v2_test_chat_ko_cand2_L32-37_k30k100_v1", "top100", "top100_rot", "unembed100", "min14_jswap_v2_L20-25_k100_v1")]),
]  # fmt: skip
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")


def pooled(run: str | None) -> dict | None:
    """A jswap run scored on its memory finals pooled, as scripts/jswap_pool.py."""
    p = RES / "jswap" / run / "rows.jsonl" if run else None
    if not p or not p.exists():
        return None
    import sys

    sys.path[:0] = [str(ROOT), str(ROOT / "src")]
    from scripts import jswap as JS

    rows = [json.loads(x) for x in p.read_text().splitlines()]
    return JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY])


def share(run: str | None, key: str) -> float | None:
    """Median over the band's layers of the per-layer median share of the residual norm removed."""
    s = load(RES / "removal_size" / run / "summary.json") if run else None
    v = sorted(x[key] for x in (s or {}).get("median_share", {}).values() if key in x)
    return 100 * v[len(v) // 2] if v else None


def pct(x: float | None) -> str:
    return "-" if x is None else f"{x:.0f}%"


def pointer(lab: str, run: str) -> str:
    s = load(RES / "jswap" / run / "summary.json")
    if not s:
        return f"| {lab} | - | - | - | - | - | - | - | - | - |"
    t = lambda k, c: s.get(f"{k}/{c}", {}).get("transfer")  # noqa: E731
    sw = t("memory", "swap")
    rels = sorted({k.split("/")[0][len("memory_"):] for k in s if k.startswith("memory_")})
    read = [r for r in rels if (t(f"memory_{r}", "swap") or 0) >= 10]
    held = [r for r in read if t(f"memory_{r}", "swap_neutral") >= 2 / 3 * t(f"memory_{r}", "swap")]
    tl = s.get("timeline_memory", {})
    first = lambda c, k: next((la for la in sorted({int(x.split("/L")[1]) for x in tl}) if tl.get(f"{c}/L{la}", {}).get(k, 0) >= 50), None)  # noqa: E731
    peak = max((v["donor"] for x, v in tl.items() if x.startswith("swap_neutral/")), default=None)
    fx, fd = first("none", "kept"), first("swap_neutral", "donor")
    lookup = f"X from L{fx}; D (neutral donor) " + (f"from L{fd}" if fd is not None else f"peaks {peak:.0f}%")
    m = s["memory/swap"]
    return (f"| {lab} | {m['n']} | {sw:+.0f} [{m['ci'][0]:.0f}, {m['ci'][1]:.0f}] | {t('memory', 'swap_neutral'):+.0f} ({t('memory', 'swap_neutral') / sw:.2f}) | "
            f"{t('memory', 'swap_neutral_rot'):+.0f} / {t('memory', 'swap_neutral_u'):+.0f} | {t('memory', 'paste_neutral'):+.0f} | "
            f"{len(held)} of {len(read)} | {t('memory', 'swap_own'):+.0f} ({t('memory', 'swap_own') / sw:.2f}) | "
            f"{t('memory', 'swap_noown'):+.0f} ({t('memory', 'swap_noown') / sw:.2f}) | {lookup} |")  # fmt: skip


def dose_rows(lab: str, ko_band: str, sw_band: str, size_ko: str, size_sw: str, ks: list) -> list[str]:
    out = []
    for k, ko, cj, cr, cu, sw in ks:
        j, r, u = mk(ko, cj), mk(ko, cr), mk(ko, cu)
        p = pooled(sw) or {}
        g = lambda c: p.get(f"memory/{c}", {})  # noqa: E731
        sws = (f"{g('swap')['transfer']:+.0f} [{g('swap')['ci'][0]:.0f}, {g('swap')['ci'][1]:.0f}] / paste {g('paste')['transfer']:+.0f} / "
               f"comp {g('swap_comp')['transfer']:+.0f} / rot {g('swap_rot')['transfer']:+.0f} (n {g('swap')['n']})") if g("swap") else "-"  # fmt: skip
        out.append(f"| {lab} | {k} | {ko_band}: {pct(share(size_ko, f'jlens_top{k}'))} | {fmt_mk(j)} | {fmt_mk(r, False)} | {fmt_mk(u, False)} | "
                   f"{sw_band}: {pct(share(size_sw, f'jlens_top{k}'))} | {sws} |")  # fmt: skip
    return out


def main() -> None:
    out = [f"# Results digest (generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} by scripts/results_digest.py)", "",
           "Every number is read from results/ (jsuite2_score, soft_score, jswap and probe_ceiling summaries). M - K: points lost on",
           "memory finals minus stated-fact finals under the top-10 J++ removal at the band, start all, 95% bootstrap over bridges.",
           "Swaps: transfer (donor - third) on PM. '-' = not run (or not yet).", ""]  # fmt: skip
    out += ["## Knock-out (test set)", "",
            "| Model | Band | J++ M - K | n (M) | K lost | rotated | logit lens | by probability | size-matched variance (pcasize) | renderings |",
            "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for lab, ko, band, _set, *_rest in MODELS:
        renders = _rest[-1]
        j, r, u, pc = mk(ko), mk(ko, "paper10_rot"), mk(ko, "unembed10"), mk(_rest[3], "paper10_pcasize")
        rend = ", ".join(fmt_mk(mk(x), ci=False) for x in renders) if renders else "-"
        out.append(f"| {lab} | {band} | {fmt_mk(j)} | {j['n'] if j else '-'} | {j['K'] if j else '-'} | {fmt_mk(r, False)} | {fmt_mk(u, False)} | {soft(ko)} | {fmt_mk(pc)} | {rend} |")
    out += ["", "## What the mention carries (swaps) and what the lens reads", "",
            "| Model | Swap at the band | Swap at mid depth | Cross-relation | Probe readout (J++ / probe above chance) | Probe swap (valid relations) |",
            "|---|---|---|---|---|---|"]  # fmt: skip
    for lab, _ko, _band, _set, sw, mid, pr, _pc, xr, _r in MODELS:
        rd, ps = probe(pr)
        out.append(f"| {lab} | {swap(sw)} | {swap(mid)} | {xrel(xr)} | {rd} | {ps} |")
    out += ["", "## Pointer tests (amendment 51; memory finals pooled, 150 random per word)", "",
            "Neutral donor: the J-part from one neutral sentence about D. Own / no-own: the J-part's own-word rows alone / without them.",
            "Relations: neutral >= 2/3 of the same-passage swap, of the relations with swap >= 10. Lookup: first layer at the answer",
            "position where the lens reads X's answer (unedited) / D's answer (neutral-donor swap) on >= 50% of items.", "",
            "| Model | n | J-part swap | neutral donor (ratio) | neutral rot / u | paste_neutral | relations | own name (share) | no-own (share) | lookup |",
            "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    out += [pointer(lab, run) for lab, run in POINTER]
    out += ["", "## Removal size at the knock-out band (median share of the residual norm removed, top 10)", "",
            "| Model | J++ | logit lens | top principal directions |", "|---|---|---|---|"]  # fmt: skip
    out += [f"| {lab} | {pct(share(r, 'jlens_top10'))} | {pct(share(r, 'unembed_top10'))} | {pct(share(r, 'pca_top10'))} |" for lab, r in SIZE]
    out += ["", "## Dose in K (top-K J++ directions; amendments 52, 53)", "",
            "Knock-out on the test set at the knock-out band; swap pooled over memory finals at the swap band. Size: share of the",
            "residual norm the top-K J++ removal takes there.", "",
            "| Model | K | size (KO band) | M - K | rotated | logit lens | size (swap band) | J-part swap / paste / comp / rot |",
            "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for d in DOSE:
        out += dose_rows(*d)
    text ="\n".join(out) + "\n"
    (ROOT / "docs" / "digest.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
