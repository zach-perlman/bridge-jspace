"""Tables + figure from ss_out_*.json (post hoc, descriptive). Run with the figvenv python."""
import json
import statistics as st
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = "/home/zach/scratch/redteam_1030/shared_subspace/"
MODELS = [("27B", "ss_out_27b.json", "36", "40"), ("Lightning", "ss_out_L.json", "30", "33"), ("9B", "ss_out_9b.json", "14", "12")]
R = {m: json.load(open(D + f)) for m, f, *_ in MODELS}
MID = {m: a for m, _, a, _ in MODELS}
OTH = {m: b for m, _, _, b in MODELS}

CAT_ORDER = ["vocab_literal_both", "vocab_capital_word", "vocab_country_word", "vocab_capital_fragment", "vocab_country_fragment",
             "other_country", "other_capital", "other_city", "us_state", "demonym", "geo_term", "other_capitalised",
             "function_word", "other_word", "other_short_or_mixed"]
CAT_LABEL = {"vocab_literal_both": "literal rows in both vocabs (14)", "vocab_capital_word": "capital-vocab rows, whole word",
             "vocab_country_word": "country-vocab rows, whole word", "vocab_capital_fragment": "capital-vocab rows, fragment",
             "vocab_country_fragment": "country-vocab rows, fragment", "other_country": "other countries (not in the 49)",
             "other_capital": "other world capitals (not in the 54)", "other_city": "other (non-capital) cities",
             "us_state": "US states", "demonym": "demonyms / nationality adj.", "geo_term": "continents, regions, geo nouns",
             "other_capitalised": "other capitalised words (proper-noun proxy)", "function_word": "English function words",
             "other_word": "other lower-case words", "other_short_or_mixed": "other (short, symbols, non-Latin)"}


def t(s):
    return "`" + s.replace("`", "'").replace("|", "\\|").replace("\n", "\\n") + "`" if s.strip() else repr(s)


out = []
w = out.append


def cat_table(m, la):
    L = R[m]["layers"][la]
    c = L["cats"]
    sd = L["cats_sd_over_draws"]
    has_e = "R_energy_mean" in c
    hdr = ("| category | n | Shared | rand eq-rank (sd) | x | " + ("rand energy-matched | " if has_e else "") +
           "rand r-dim in span(Cap) | SharedNoLit | rand eq-rank (NoLit) | x |")
    w(hdr)
    w("|" + "---|" * (hdr.count("|") - 1))
    for k in CAT_ORDER:
        if k not in c["Shared"]:
            continue
        s, r_, nl, rn = c["Shared"][k]["mean"], c["R_eq_mean"][k]["mean"], c["SharedNoLit"][k]["mean"], c["R_eq_nolit_mean"][k]["mean"]
        row = (f"| {CAT_LABEL[k]} | {c['Shared'][k]['n']} | {s:.3f} | {r_:.3f} ({sd['R_eq'][k]:.3f}) | {s / r_:.1f} | " +
               (f"{c['R_energy_mean'][k]['mean']:.3f} | " if has_e else "") +
               f"{c['Rin_Cap_mean'][k]['mean']:.3f} | {nl:.3f} | {rn:.3f} | {nl / rn:.1f} |")
        w(row)
    ms = L["mean_share_all"]
    w(f"| **all letter tokens** | {R[m]['n_letters']} | {ms['Shared']:.3f} | {ms['R_eq']:.3f} | {ms['Shared'] / ms['R_eq']:.1f} | " +
      (f"{ms['R_energy']:.3f} | " if has_e else "") + f"{ms['Rin_Cap']:.3f} | {ms['SharedNoLit']:.3f} | {ms['R_eq_nolit']:.3f} | "
      f"{ms['SharedNoLit'] / ms['R_eq_nolit']:.1f} |")


# ---------------- reconstruction ----------------
w("## A. Reconstruction check (does my Shared match the runner's?)\n")
w("Ranks of Shared / SharedNoLit per layer, rebuilt on CPU from the frozen J++ (sha256-checked) and the lm_head + final-norm "
  "gain read from the pinned checkpoint, against the band averages the runs logged (keeplog `rank`). Capital/country rows were "
  "recomputed and asserted equal to the run's `n44_spans.json`; every item's `cty_rows` in `n44_rows.jsonl` is the same full "
  "list (185 / 186 country rows < 186 / 187 capital rows, so note 44's count-matched subsample keeps all of them).\n")
w("| model (run) | band | per-layer rank Shared | per-layer rank SharedNoLit | band mean (mine) | logged | principal cosines within 0.88-0.92 per layer |")
w("|---|---|---|---|---|---|---|")
for m, f, *_ in MODELS:
    rc = R[m]["rank_check"]
    lo, hi = R[m]["band"]
    mode = "tf32" if R[m]["basis_numerics"].startswith("tf32") else "fp32"
    ls = [str(x) for x in range(lo, hi + 1)]
    w(f"| {m} (`{R[m]['run_dir'].split('/')[-1]}`) | L{lo}-{hi} | " + ", ".join(str(rc[x][mode]['shared']) for x in ls) + " | " +
      ", ".join(str(rc[x][mode]['nolit']) for x in ls) + f" | {rc['mean_' + mode]['shared']:.2f} / {rc['mean_' + mode]['nolit']:.2f} | "
      f"{R[m]['logged_rank'].get('Shared', float('nan')):.2f} / {R[m]['logged_rank'].get('SharedNoLit', float('nan')):.2f} | " +
      ", ".join(str(rc[x][mode]['n_cos_0.88_0.92']) for x in ls) + " |")
w("")
w("fp32 and TF32-emulated atoms gave identical ranks at every layer. Several principal cosines sit within +/-0.02 of the 0.9 cut "
  "at every layer, so Shared's exact dimension is threshold-sensitive (a different cut would add or drop a few dimensions).\n")
w("The 14 literal rows (identical token rows in both vocabularies): " + "; ".join(
    f"{m}: " + " ".join(t(x) for x in R[m]["literal_rows"]) for m in R) + "\n")

# ---------------- categories ----------------
w("## B. J++ dictionary readout: energy share by token category\n")
w("Each letter-token J++ unit vector a_t at the layer is projected onto the subspace; share = |P a_t|^2 (0 to 1). Cells are the "
  "category mean. Controls: *rand eq-rank* = span of the first r rows of the item's note 44 Rcap pool (ablate_v2's random-keep "
  "draw, `random.Random('n41:'+id)` from letter rows minus capital rows and protected rows), mean over the pools of 10 MC0 items "
  "(sd across those 10 draws in brackets); *rand energy-matched* = the first k_RShared rows of the same pools (note 52b's RShared, "
  "k from the run's keeplog, about 75 (27B) / 37 (Lightning) rows, so a larger span); *rand r-dim in span(Cap)* = a random "
  "r-dimensional subspace of the capital span itself. x = Shared / rand eq-rank. Category lists are hand-written word lists "
  "(whole-token, case-insensitive match after stripping the leading space); 'other capitalised' is only a proxy for proper nouns.\n")
for m in ("27B", "Lightning", "9B"):
    for la in (MID[m], OTH[m]):
        L = R[m]["layers"][la]
        w(f"### {m}, layer {la} (Shared rank {L['rank_shared']}, SharedNoLit rank {L['rank_nolit']})\n")
        cat_table(m, la)
        w("")
        if m == "9B":
            break

w("### Composition of the 200 highest-share tokens (mid layer)\n")
w("| model | subspace | " + " | ".join(["literal", "vocab word", "vocab fragment", "other geo (countries/capitals/cities/states/demonyms/geo terms)",
                                         "function word", "other"]) + " |")
w("|---|---|---|---|---|---|---|---|")
for m in R:
    for sub in ("Shared", "SharedNoLit", "R_eq_draw0", "Rin_Cap_draw0"):
        cc = R[m]["layers"][MID[m]]["top200_comp"][sub]
        g = lambda ks: sum(cc.get(k, 0) for k in ks)  # noqa: E731
        w(f"| {m} | {sub} | {g(['vocab_literal_both'])} | {g(['vocab_capital_word', 'vocab_country_word'])} | "
          f"{g(['vocab_capital_fragment', 'vocab_country_fragment'])} | "
          f"{g(['other_country', 'other_capital', 'other_city', 'us_state', 'demonym', 'geo_term', 'capital_word_other_form', 'country_word_other_form'])} | "
          f"{g(['function_word'])} | {g(['other_capitalised', 'other_word', 'other_short_or_mixed'])} |")
w("")

w("### Selectivity: category mean / the same subspace's all-token mean (removes each span's overall anisotropy)\n")
w("J++ dictionaries share a common component (section E, axis 1), so any span of J++ rows holds some energy of every token; "
  "this ratio asks which categories a subspace prefers. Values > 1 mean enriched relative to the average token.\n")
SEL = ["vocab_country_word", "vocab_capital_word", "other_country", "other_capital", "other_city", "us_state", "demonym", "geo_term",
       "other_capitalised", "function_word"]
w("| model, layer | subspace | " + " | ".join(CAT_LABEL[k] for k in SEL) + " |")
w("|---|---|" + "---|" * len(SEL))
for m in R:
    for la in (MID[m], OTH[m]):
        L = R[m]["layers"][la]
        for sub, key in (("Shared", "Shared"), ("rand eq-rank", "R_eq_mean"), ("SharedNoLit", "SharedNoLit"), ("rand NoLit-rank", "R_eq_nolit_mean")):
            c = L["cats"][key]
            allm = L["mean_share_all"][key.replace("_mean", "")]
            w(f"| {m} L{la} | {sub} | " + " | ".join(f"{c[k]['mean'] / allm:.1f}" for k in SEL) + " |")
w("")
w("### Highest-share tokens within each non-vocabulary category, SharedNoLit (mid layer)\n")
w("| category | 27B | Lightning | 9B |")
w("|---|---|---|---|")
for k in ["other_country", "other_capital", "other_city", "us_state", "demonym", "geo_term", "other_capitalised", "function_word"]:
    w(f"| {CAT_LABEL[k]} | " + " | ".join(", ".join(f"{t(a)} {b:.2f}" for a, b in R[m]["layers"][MID[m]]["cat_top"]["SharedNoLit"][k][:7]) for m in R) + " |")
w("")

# ---------------- top tokens ----------------
w("## C. Top tokens by energy share (mid layer)\n")
for m in R:
    L = R[m]["layers"][MID[m]]
    w(f"### {m}, layer {MID[m]}\n")
    w("**Shared, top 40 (all rows):** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top_Shared"][:40]) + "\n")
    w("**Shared, top 40 outside the capital/country vocab rows:** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top_nonvocab_Shared"][:40]) + "\n")
    w("**SharedNoLit, top 40 (all rows):** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top_SharedNoLit"][:40]) + "\n")
    w("**SharedNoLit, top 40 outside the vocab rows:** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top_nonvocab_SharedNoLit"][:40]) + "\n")
    w("**Random equal-rank span (draw 0), top 20:** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top_R_eq_draw0"][:20]) + "\n")

# ---------------- logit lens ----------------
w("## D. Logit-lens view (unit unembedding rows, final-norm gain folded in; no Jacobian)\n")
w("Two readings. (i) The same J++-built Shared / SharedNoLit, read by projecting each unit unembedding row onto it. (ii) A "
  "logit-lens analogue: Shared rebuilt from the unit unembedding rows of the same capital/country token rows (same 0.9 rule).\n")
w("| model | layer | rank of logit-lens Shared (ii) | its rank after removing the 14 literal rows | mean share, all tokens: Shared (i) / rand eq-rank / r/d |")
w("|---|---|---|---|---|")
for m in R:
    for la in (MID[m], OTH[m]):
        L = R[m]["layers"][la]
        ll = L["logit_lens"]["mean_share_all"]
        w(f"| {m} | {la} | {L['rank_SharedU_logitlens']} | {L['rank_SharedU_nolit']} | {ll['Shared']:.4f} / {ll['R_eq_mean']:.4f} / "
          f"{L['rank_shared'] / R[m]['d']:.4f} |")
w("")
w("Principal cosines between the unembedding-row spans of the capital and country vocabularies (mid layer is irrelevant here: no "
  "Jacobian), top 20: " + "; ".join(f"{m}: " + ", ".join(str(x) for x in R[m]["layers"][MID[m]]["logitlens_principal_cos_top20"][13:20])
                                   for m in R) + " (entries 14-20; the first 14 are the literal rows at 1.0).\n")
w("| category (mean share of unit unembedding rows, mid layer) | " + " | ".join(f"{m} Shared (i) | {m} rand" for m in R) + " |")
w("|---|" + "---|---|" * len(R))
for k in CAT_ORDER:
    cells = []
    for m in R:
        c = R[m]["layers"][MID[m]]["logit_lens"]["cats"]
        cells += [f"{c['Shared'][k]['mean']:.3f}", f"{c['R_eq_mean'][k]['mean']:.3f}"]
    w(f"| {CAT_LABEL[k]} | " + " | ".join(cells) + " |")
w("")
for m in R:
    L = R[m]["layers"][MID[m]]["logit_lens"]
    w(f"**{m} L{MID[m]}, logit lens on J++ Shared, top 30:** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top"]["Shared"][:30]) + "\n")
    w(f"**{m} L{MID[m]}, logit lens on J++ SharedNoLit, top 30:** " + ", ".join(f"{t(x[0])} {x[2]:.2f}" for x in L["top"]["SharedNoLit"][:30]) + "\n")

# ---------------- axes ----------------
w("## E. Principal axes of Shared (mid layer)\n")
w("Axes = right singular vectors of the matrix of every letter atom's coordinates in Shared (the directions in Shared along which "
  "the dictionary varies most); 'frac' = that axis's share of the dictionary's energy in Shared. Signs are arbitrary.\n")
for m in R:
    L = R[m]["layers"][MID[m]]
    w(f"### {m}, layer {MID[m]}\n")
    w("| axis | frac | top + tokens | top - tokens |")
    w("|---|---|---|---|")
    for i, a in enumerate(L["axes"][:6]):
        w(f"| {i + 1} | {a['sv_frac']:.3f} | " + ", ".join(t(x[0]) for x in a["plus"][:12]) + " | " + ", ".join(t(x[0]) for x in a["minus"][:12]) + " |")
    w("")

# ---------------- gold ----------------
w("## F. Each item's own answer (capital) and country inside Shared\n")
w("Per MC0 item: the mean, over the gold capital's forms (first token of `X`, `x`, ` X`, ` x`, aliases included) of the share of "
  "its J++ unit vector inside Shared; the same for the item's country (the bridge's country) and for the item's 5 distractor "
  "capitals (the other capitals of its scene). Controls: the item's own equal-rank random span (first r rows of its Rcap pool; "
  "the pool excludes every capital row and the item's protected rows) and a random r-dim subspace of span(Cap). Shared is the "
  "same subspace for every item, so 'gold vs distractor capitals' is the test of item specificity.\n")
w("| model | layer | n items | gold capital in Shared | distractor capitals in Shared | gold capital in rand eq-rank | gold capital in rand r-dim of span(Cap) | gold country in Shared | gold country in rand eq-rank | gold capital in SharedNoLit | distractors in SharedNoLit | gold capital in rand (NoLit rank) | gold country in SharedNoLit |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for m in R:
    for la in (MID[m], OTH[m]):
        g = R[m]["layers"][la]["gold"]
        mn = lambda k: st.mean(x[k] for x in g if x[k] is not None)  # noqa: E731
        w(f"| {m} | {la} | {len(g)} | {mn('cap_in_Shared'):.3f} | {mn('distractor_caps_in_Shared'):.3f} | {mn('cap_in_Req'):.3f} | "
          f"{mn('cap_in_RinCap'):.3f} | {mn('cty_in_Shared'):.3f} | {mn('cty_in_Req'):.3f} | {mn('cap_in_NoLit'):.3f} | "
          f"{mn('distractor_caps_in_NoLit'):.3f} | {mn('cap_in_Req_nolit'):.3f} | {mn('cty_in_NoLit'):.3f} |")
w("")
for m in ("27B", "Lightning"):
    pc = R[m]["layers"][MID[m]]["per_capital"]
    srt = sorted(pc.items(), key=lambda kv: -kv[1]["Shared"])
    w(f"**{m} L{MID[m]}, per capital (mean over forms), Shared:** highest " +
      ", ".join(f"{k} {v['Shared']:.2f}" for k, v in srt[:8]) + "; lowest " + ", ".join(f"{k} {v['Shared']:.2f}" for k, v in srt[-8:]) + "\n")
    pt = R[m]["layers"][MID[m]]["per_country"]
    srt = sorted(pt.items(), key=lambda kv: -kv[1]["NoLit"])
    w(f"**{m} L{MID[m]}, per country, SharedNoLit:** highest " + ", ".join(f"{k} {v['NoLit']:.2f}" for k, v in srt[:10]) +
      "; lowest " + ", ".join(f"{k} {v['NoLit']:.2f}" for k, v in srt[-6:]) + "\n")

open(D + "tables.md", "w").write("\n".join(out) + "\n")

# ---------------- figure ----------------
FIG_CATS = ["vocab_country_word", "vocab_capital_word", "vocab_capital_fragment", "other_country", "other_capital", "other_city",
            "us_state", "demonym", "other_capitalised", "function_word", "other_word"]
short = {"vocab_country_word": "country vocab\n(whole word)", "vocab_capital_word": "capital vocab\n(whole word)",
         "vocab_capital_fragment": "capital vocab\n(fragment)", "other_country": "other\ncountries", "other_capital": "other\ncapitals",
         "other_city": "other\ncities", "us_state": "US\nstates", "demonym": "demonyms", "other_capitalised": "other\ncapitalised",
         "function_word": "function\nwords", "other_word": "other\nwords"}
fig, axs = plt.subplots(2, 1, figsize=(11, 7.2), sharex=True)
cols = {"Shared": "#1f4e79", "R_eq_mean": "#9dc3e6", "SharedNoLit": "#c55a11", "R_eq_nolit_mean": "#f4b183"}
lab = {"Shared": "Shared", "R_eq_mean": "random rows, equal rank", "SharedNoLit": "SharedNoLit", "R_eq_nolit_mean": "random rows, NoLit rank"}
for ax, m in zip(axs, ("27B", "Lightning")):
    L = R[m]["layers"][MID[m]]
    c = L["cats"]
    x = range(len(FIG_CATS))
    wd = 0.2
    for j, k in enumerate(["Shared", "R_eq_mean", "SharedNoLit", "R_eq_nolit_mean"]):
        ax.bar([i + (j - 1.5) * wd for i in x], [c[k][q]["mean"] for q in FIG_CATS], wd, color=cols[k], label=lab[k])
    ax.set_ylabel("mean energy share\nof J++ unit vector")
    ax.set_title(f"{m}, layer {MID[m]}: Shared rank {L['rank_shared']}, SharedNoLit rank {L['rank_nolit']}", fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
axs[0].legend(frameon=False, ncol=4, fontsize=8, loc="upper right")
axs[1].set_xticks(list(range(len(FIG_CATS))))
axs[1].set_xticklabels([short[q] for q in FIG_CATS], fontsize=8)
fig.suptitle("What the closed-book capital 'Shared' subspace reads out as (post hoc, CPU, descriptive; random = mean of 10 draws)", fontsize=10)
fig.tight_layout()
fig.savefig(D + "shared_categories.png", dpi=160)
print("ok")
