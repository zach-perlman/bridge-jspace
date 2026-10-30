"""cpuwins figure (post hoc, exploratory): where recalls go when they fail, natural vs under paper10."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
a3 = json.load(open("a3_results.json")); b = json.load(open("a3b_results.json"))
CATS = [("x_pv", "X's own passage value\n(the value the text binds to the same person)", "#2a78d6"),
        ("other_pv", "another person's\npassage value", "#eb6834"),
        ("ans", "another answer,\nnot in the passage", "#1baf7a"),
        ("non_answer", "non-answer token", "#b8b7b0")]
rows = []
for m in ["9B", "27B", "Lightning"]:
    nat = b[f"{m}|natural|MM_fail"]
    rows.append((m, f"natural recall failures\n(unedited, n={nat['n']})", {"x_pv": nat.get("x_pv", 0), "other_pv": nat.get("other_pv", 0),
                 "ans": nat.get("answer", 0), "non_answer": nat.get("non_answer", 0)}, None))
    k = a3[f"{m}|MM|paper10"]; r = b[f"{m}|paper10"]
    rows.append((m, f"recalls lost under the\nknock-out (paper10, n={k['n_lost']})", {"x_pv": k["x_pv"], "other_pv": k["other_pv"],
                 "ans": k["rival"] + k["answer"], "non_answer": k["non_answer"]}, r))
fig, axes = plt.subplots(3, 1, figsize=(9.5, 6.4), sharex=True, gridspec_kw={"hspace": 0.55})
names = {"9B": "Qwen3.5-9B", "27B": "Qwen3.6-27B", "Lightning": "Nemotron-3.5-Lightning"}
for ax, m in zip(axes, ["9B", "27B", "Lightning"]):
    rr = [x for x in rows if x[0] == m]
    for yi, (_, lab, d, r) in enumerate(rr[::-1]):
        left = 0
        for key, _, col in CATS:
            w = d[key]
            if w <= 0: continue
            ax.barh(yi, w, left=left, color=col, edgecolor="white", linewidth=2, height=0.62)
            if w >= 7:
                ax.text(left + w / 2, yi, f"{w:.0f}%", ha="center", va="center", fontsize=9, color="white" if key != "non_answer" else "#0b0b0b")
            left += w
        if r:
            ax.text(101.5, yi, f"X vs any one other\nperson: {r['per_entity_ratio_X_vs_other']:.1f}x [{r['ratio_ci'][0]:.1f}, {r['ratio_ci'][1]:.1f}]",
                    va="center", fontsize=8, color="#52514e")
    ax.set_yticks(range(len(rr))); ax.set_yticklabels([x[1] for x in rr[::-1]], fontsize=8.5, color="#0b0b0b")
    ax.set_title(names[m], loc="left", fontsize=10.5, color="#0b0b0b", pad=4)
    ax.set_xlim(0, 100)
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#b8b7b0"); ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", colors="#52514e")
axes[-1].set_xlabel("share of failed recalls (%)", color="#52514e")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in CATS]
fig.legend(handles, [l for _, l, _ in CATS], loc="upper center", ncol=4, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 1.0))
fig.suptitle("Recalls broken by the knock-out often become the value the passage gives the SAME person (4.5-6.4x any other\n"
             "person's value), the models' commonest natural recall error, though less often than natural failures do\n"
             "(v4 recall items, draw 4001; post hoc, exploratory)", y=1.11, fontsize=10.5, color="#0b0b0b")
fig.text(0.01, -0.06, "Knock-out rows: MM items right unedited and wrong under paper10 at each model's band; output = cand2 pick among the relation's answers "
         "(so no non-answer tokens by construction).\nNatural rows: v4-gated MM failures (hop 1 and hop 2 alone right); output = unedited top token. "
         "Ratio = P(X's value) / mean P(one given other person's value), bootstrap over bridges.\nChance if uniform over answers: X's value 3.5%, any other person's value 18%.",
         fontsize=7.2, color="#52514e")
plt.savefig("cpuwins_fig_failure_destination.png", dpi=180, bbox_inches="tight", facecolor="white")
print("ok")
