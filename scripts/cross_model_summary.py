"""cross_model_summary: one table (and figure) of the replication runs, per model, read from the result files as they land
(Zach, 2026-10-22). C1: the middle band chosen on ctrl_v8, the C1-graded rule's losses, gap and verdict, the guessable
split, the specificity control (unembedding directions), keep-own-word, the extra rotated-control seeds, the plain-text
gate. C2: C2-graded and C2-relative (pre-registered), C2' (docs/prereg_replication_1022.md), at the current band and at
the aligned band. Missing runs show as "-". Everything unverified until in VERIFIED.md.

python scripts/cross_model_summary.py   (writes results/cross_model/summary.md, .json and figures/archive/cross_model/c1_by_model.png)
"""

from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

R = pins.RESULTS_DIR
MODELS = [  # label, run prefix, lens, steering run (current band), plain-text run, its band
    ("Qwen3.6-27B", "", "published J++", "wm2_full2_v2", "textloss_top_l32_40_v1"),
    ("Qwen3-32B", "qwen3_32b_", "our J++ (32 prompts)", "qwen3_32b_wm2_full2_v1", "qwen3_32b_textloss_top_v1"),
    ("Muse Glimmer 30B", "muse30_", "our J++ (32 prompts)", "muse30_wm2_full2_v1", "muse30_textloss_top_v1"),
    ("Qwen3.5-9B", "qwen35_9b_", "published J++", "qwen35_9b_wm2_full2_v1", "qwen35_9b_textloss_top_v1"),
    ("Gemma 4 31B-it", "gemma4itf_", "our J++ (64 prompts)", "gemma4itf_wm2_full2_v1", "gemma4itf_sink_textloss_v1"),
]
WORDS = ("PP", "MP", "CP", "PM", "MM", "CM")
NAME = {"PP": "P→P", "MP": "M→P", "CP": "C→P", "PM": "P→M", "MM": "M→M", "CM": "C→M"}


def load(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def rot_min(run: str, band: str) -> float | None:
    p = R / "ablate_v2" / run / "rows.jsonl"
    if not p.exists():
        return None
    acc = collections.defaultdict(list)
    for line in p.read_text().splitlines():
        r = json.loads(line)
        if r["kind"] == "clean" and r["condition"].endswith("_rot") and r["band"] == band:
            acc[r["family"]].append(r["correct"])
    return min(statistics.mean(v) for v in acc.values()) if acc else None


def model_row(label: str, p: str, lens: str, steer: str, textloss: str) -> dict:
    out: dict = {"model": label, "lens": lens}
    c1 = load(R / "ablate_v2" / "c1_v2" / f"{p}full2_ko_v1.json")
    if c1:
        rule = c1["rule"]
        out["c1"] = {"band": c1["middle"], "loss": rule["loss"], "gap": rule["gap"], "controls_ok": rule["controls_ok"],
                     "holds": rule["C1_graded_holds"], "strict": rule["strict_C1_holds"]}  # fmt: skip
        ng = load(R / "ablate_v2" / "c1_v2" / f"{p}full2_ko_v1_noguess.json")
        out["c1"]["gap_noguess"] = ng["rule"]["gap"] if ng else None
        band = c1["middle"]
        spec = load(R / "ablate_v2" / "c1_specificity" / f"{p}full2_ko_unembed_v1.json")
        if spec and band in spec["bands"]:
            out["c1"]["unembed_gap"] = spec["bands"][band].get("unembed10", {}).get("gap")
        keep = load(R / "ablate_v2" / "c1_v2" / f"{p}full2_ko_keepown_v1.json")
        if keep and "keepown" in keep:
            out["c1"]["keepown_restored"], out["c1"]["keepown_kills"] = keep["keepown"]["restored"], keep["keepown"]["kills_C1"]
        seeds = [rot_min(f"{p}full2_ko_rotseed{s}_v1", band) for s in (1, 2)]
        out["c1"]["rot_seed_min"] = [s for s in seeds if s is not None]
    tl = load(R / "removal_textloss" / textloss / "summary.json")
    if tl:
        m = tl["mean_nll"]
        out["plain_text"] = {"none": m["none"], "top10": m["top10"] - m["none"], "top10_rot": m["top10_rot"] - m["none"],
                             "untestable": (m["top10"] - m["none"] >= 2.0) and abs(m["top10_rot"] - m["none"]) <= 0.3}  # fmt: skip
    for key, run in (("c2", steer), ("c2_aligned", steer.replace("wm2_full2_v2", "wm2_full2_aligned_v1").replace("wm2_full2_v1", "wm2_full2_aligned_v1"))):
        g = load(R / "write_max" / "c2_graded" / f"{run}_paste.json") or load(R / "write_max" / "c2_graded" / f"{run}.json")  # the paste ceiling when re-measured (27B)
        n = load(R / "write_max" / "c2_narrow" / f"{run}.json")
        if g or n:
            out[key] = {"run": run}
            if g:
                out[key] |= {"graded": g["rule"]["C2_graded_holds"], "mm_best": g["rule"]["mm_best"], "mp_best": g["rule"]["mp_best"],
                             "relative": g["rule_relative"]["verdict"]}  # fmt: skip
            if n:
                out[key] |= {"narrow": n["verdict"], "narrow_writes": {x: [v["write_XP"], v["write_XM"]] for x, v in n["per_source"].items()}}
    return out


def pct(x, signed=False):
    return "-" if x is None else (f"{100 * x:+.0f}" if signed else f"{100 * x:.0f}")


def main() -> None:
    rows = [model_row(*m) for m in MODELS]
    (R / "cross_model").mkdir(parents=True, exist_ok=True)
    (R / "cross_model" / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    lines = ["# Cross-model replication summary (unverified; one data seed; written by scripts/cross_model_summary.py)", "",
             "## C1: memory steps need the J-space, prompt lookups don't (knock-out at each model's held-out-chosen band)", "",
             "| model | lens | band | loss P→P / M→P / C→P | loss P→M / M→M / C→M | gap (≥30) | controls | C1-graded | no-guess gap | unembedding gap | keep-own restored (kill ≥75%) | extra control seeds (min acc) | plain-text +nats top-10 / random |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in rows:
        c, t = r.get("c1"), r.get("plain_text")
        tl = "-" if not t else f"{t['top10']:+.2f} / {t['top10_rot']:+.2f}" + (" UNTESTABLE" if t["untestable"] else "")
        if not c:
            lines.append(f"| {r['model']} | {r['lens']} | - | - | - | - | - | - | - | - | - | - | {tl} |")
            continue
        lo = " / ".join(pct(c["loss"][w]) for w in ("PP", "MP", "CP"))
        hi = " / ".join(pct(c["loss"][w]) for w in ("PM", "MM", "CM"))
        seeds = ", ".join(pct(s) for s in c.get("rot_seed_min", [])) or "-"
        keep = "-" if "keepown_restored" not in c else f"{pct(c['keepown_restored'])}%" + (" KILLS" if c["keepown_kills"] else "")
        verdict = "n/a (untestable)" if t and t["untestable"] else ("HOLDS" if c["holds"] else "FAILS")
        lines.append(f"| {r['model']} | {r['lens']} | {c['band']} | {lo} | {hi} | {pct(c['gap'])} | {'ok' if c['controls_ok'] else 'NO'} | "
                     f"**{verdict}** | {pct(c.get('gap_noguess'))} | {pct(c.get('unembed_gap'))} | {keep} | {seeds} | {tl} |")  # fmt: skip
    lines += ["", "## C2: the lens writes bridges (two-step steering at the question / final positions)", "",
              "| model | band | C2-graded (M→M best vs M→P best) | C2-relative | C2' (narrow): P→P vs P→M; C→P vs C→M (cross-validated writes) |",
              "|---|---|---|---|---|"]  # fmt: skip
    for r in rows:
        for key, lab in (("c2", "current"), ("c2_aligned", "aligned")):
            c2 = r.get(key)
            if not c2:
                continue
            g = "-" if "graded" not in c2 else f"{'HOLDS' if c2['graded'] else 'FAILS'} ({pct(c2['mm_best'])} vs {pct(c2['mp_best'])})"
            nw = c2.get("narrow_writes", {})
            nar = "-" if "narrow" not in c2 else f"**{c2['narrow']}**: P {pct(nw['P'][0])}→{pct(nw['P'][1])}; C {pct(nw['C'][0])}→{pct(nw['C'][1])}"
            lines.append(f"| {r['model']} | {lab} | {g} | {c2.get('relative', '-')} | {nar} |")
    lines += ["", "The 27B's C2' is the data the rule was read off (not evidence); the other models are the test."]
    (R / "cross_model" / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    figure(rows)


def figure(rows: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    have = [r for r in rows if r.get("c1")]
    if not have:
        return
    fig, ax = plt.subplots(figsize=(1.9 + 2.1 * len(have), 4.6))
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#e4e3df")
    ax.set_axisbelow(True)
    cols = {"PP": "#2a78d6", "MP": "#5d9be3", "CP": "#9cc2ee", "PM": "#eb6834", "MM": "#f08f62", "CM": "#f5b99a"}
    for i, r in enumerate(have):
        for j, w in enumerate(WORDS):
            v = 100 * r["c1"]["loss"][w]
            ax.bar(i * 7.5 + j + (0.5 if j >= 3 else 0), v, 0.85, color=cols[w], label=NAME[w] if i == 0 else None)
        verdict = "holds" if r["c1"]["holds"] else "fails"
        ax.text(i * 7.5 + 2.75, -9, f"{r['model']}\n{r['c1']['band']} · gap {100 * r['c1']['gap']:.0f} · C1 {verdict}", ha="center", va="top", fontsize=8.5)
    ax.set_xticks([])
    ax.set_ylim(0, 100)
    ax.set_ylabel("accuracy lost under the knock-out (points)")
    ax.legend(ncol=6, frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("C1 by model: lookup-final (blue) vs memory-final (orange) chains at each model's held-out-chosen band", loc="left", fontsize=10)
    fig.text(0.01, 0.01, "Top-10 J-lens directions removed at every position (answer protected); one data seed; unverified.", fontsize=7.5, color="#52514e")
    fig.subplots_adjust(bottom=0.27, top=0.88, left=0.08, right=0.99)
    out = pins.FIGURES_DIR / "cross_model"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "c1_by_model.png", dpi=180)


if __name__ == "__main__":
    main()
