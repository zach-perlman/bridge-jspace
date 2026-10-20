"""Dataset figures (Zach, 2026-10-20): what is in tasks_v2's calibration set (calib_v3, generator v3) and how it
compares with calib_v2 (the generator before the audit, rebuilt from git at 93e11f5) on the audit's checks, measured
with the same code; plus the per-entity spread of the existing knock-out results (suite_v1, countries).

python scripts/dataset_figures.py OUTDIR      (CPU only; needs the tokenizer for prompt lengths)
"""

from __future__ import annotations

import collections
import importlib.util
import json
import statistics
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.tokens import load_tokenizer
from scripts import suite_v1 as S
from scripts import tasks_v2 as T

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"
BLUE, ORANGE, AQUA, YELLOW, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#a3a29c"
BLUES = LinearSegmentedColormap.from_list("blues", ["#f4f8fd", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf",
                                                    "#184f95", "#0d366b"])  # fmt: skip
plt.rcParams.update({"font.size": 9, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK, "axes.edgecolor": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF})  # fmt: skip
WORDS = list(T.WORDS2 + T.WORDS3)
DIGIT_WORDS = [w for w in WORDS if w[1:] != "MM"]
M2O = ("animals", "vehicles", "instruments")  # domains where many things share a number


def style(ax, grid_axis="x"):
    ax.grid(axis=grid_axis, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def save(fig, name):
    fig.savefig(OUT / name, dpi=170, bbox_inches="tight", facecolor=SURF)
    plt.close(fig)
    print("wrote", OUT / name)


# ---- regenerate both sets with their scenes (each checked identical to the committed file) ----
def with_scenes(mod, set_name: str, make_args: tuple) -> list[dict]:
    last: dict = {}
    orig_scene = mod.scene

    def scene(*a, **k):
        last["sc"] = orig_scene(*a, **k)
        return last["sc"]

    mod.scene = scene
    maker = "make_scene" if hasattr(mod, "make_scene") else "make_item"
    orig = getattr(mod, maker)

    def wrapped(*a, **k):
        got = orig(*a, **k)
        for it in got if isinstance(got, list) else [got] if got else []:
            it["_sc"] = json.loads(json.dumps(last["sc"]))
        return got

    setattr(mod, maker, wrapped)
    tmp = f"_fig_{set_name}"
    mod.DATA.joinpath(tmp).mkdir(parents=True, exist_ok=True)
    try:
        mod.make(tmp, *make_args)
        items = [json.loads(line) for line in (mod.DATA / tmp / "items.jsonl").read_text().splitlines()]
    finally:
        for f in (mod.DATA / tmp).iterdir():
            f.unlink()
        (mod.DATA / tmp).rmdir()
        mod.scene = orig_scene
        setattr(mod, maker, orig)
    ref = T.load(set_name)
    assert [{k: v for k, v in it.items() if k != "_sc"} for it in items] == ref, f"{set_name} did not regenerate"
    return items


old_src = subprocess.run(
    ["git", "show", "93e11f5:scripts/tasks_v2.py"], capture_output=True, text=True, check=True
).stdout
old_path = Path("/tmp/tasks_v2_v2gen.py")
old_path.write_text(old_src)
spec = importlib.util.spec_from_file_location("tasks_v2_v2gen", old_path)
T2 = importlib.util.module_from_spec(spec)
sys.modules["tasks_v2_v2gen"] = T2
spec.loader.exec_module(T2)
v2 = with_scenes(T2, "calib_v2", (48, WORDS, list(T2.DOMAINS), list(T2.FORMATS), list(T2.LEVELS), 702))
v3 = with_scenes(T, "calib_v3", (48, WORDS, list(T.DOMAINS), list(T.FORMATS), list(T.LEVELS), 703))
tok = load_tokenizer()
for it in v3:
    it["_tokens"] = len(S.ids(tok, T.render(tok, it)))


# ---- audit metrics, one implementation for both generators ----
def start(it):
    return it["steps"][0]["answer"]


def person(it):
    return it["_sc"].get("person") or next(p for p, t in it["_sc"]["pick"].items() if t == start(it))


def partner_of(sc, x, gen):
    if gen == 3:
        return dict(sc["partner"]).get(x)
    return sc["partner"][x]


def coincidence(it, gen) -> bool:
    """A wrong route (other relation, skipped partner, skipped bin, the look-alike's pick) gives the right answer."""
    mod = T if gen == 3 else T2
    sc, dom, w = it["_sc"], mod.DOMAINS[it["domain"]], it["word"]
    lk, bins = sc["locker"], {int(k): v for k, v in sc["bin"].items()}
    x, ans = start(it), it["answer"]
    alts = []
    t = x if len(w) == 2 else (partner_of(sc, x, gen) if w[1] == "P" else None)
    if t is not None:
        alts.append(str(dom.values[t]) if w[-1] == "P" else str(lk[t]))
    if len(w) == 3 and w[1] == "P":
        alts.append(str(lk[x]) if w[2] == "P" else str(dom.values[x]))
    if len(w) == 3 and w[1:] == "MP":
        alts += [str(dom.values[x]), str(bins[lk[x]])]
    if w[0] == "P":
        near = (T.NEAR if gen == 3 else {p: T2.lookalike(p) for p in sc["pick"]}).get(person(it))
        for name, pick in sc["lookalike_picks"]:
            if name == near and pick != x:
                scn = {**sc, "bin": bins, "partner": sc["partner"]}
                d2 = mod.DOMAINS[it["domain2"]] if it.get("domain2") else None
                alts.append(mod.follow(w, dom, scn, pick, d2)[0])
    return ans in alts


def paraphrased(it, gen) -> bool:
    if gen == 2:
        return any(it["question"].startswith(b) for _, b in T2.PARAPHRASES)
    dom = T.DOMAINS[it["domain"]]
    alts = [T.Q_LOCKER[1], T.Q_BIN[1], dom.prop_q[1]] + (
        [T.DOMAINS[it["domain2"]].reverse_desc[1]] if it["domain2"] else []
    )
    return any(it["question"].startswith(a.split("{")[0]) for a in alts)


def partner_ambiguous(it, gen) -> bool:
    """Under a symmetric reading of the partner statements, the bridge has more than one partner."""
    sc, x = it["_sc"], start(it)
    if gen == 3:
        return sum(x in pair for pair in sc["pairs"]) > 1
    return sum(1 for a, b in sc["partner"].items() if x in (a, b)) > 1


def row_order_hit(it) -> bool:
    tabs = {}
    for block in it["context"].split("\n\n"):
        head, *rows = block.split("\n")
        tabs[head] = [r.strip("| ").split(" | ") for r in rows[2:]]
    picks, lockers = tabs["Table picks:"], tabs["Table lockers:"]
    i = next(k for k, r in enumerate(picks) if r[0] == person(it))
    return i < len(lockers) and lockers[i][0] == picks[i][1]


def lookalike_queried(it, gen) -> bool:
    near = T.NEAR.get(person(it)) if gen == 3 else T2.lookalike(person(it))
    return any(n == near and p != start(it) for n, p in it["_sc"]["lookalike_picks"])


def mean(xs):
    xs = list(xs)
    return statistics.mean(xs) if xs else float("nan")


audit = {}
for gen, items in ((2, v2), (3, v3)):
    hi = [it for it in items if it["level"] >= 2]
    m2o_mem = [it for it in items if it["word"][-1] == "M" and it["word"] in DIGIT_WORDS and it["domain"] in M2O]
    majority = mean(collections.Counter(it["answer"] for it in m2o_mem if it["word"] == w).most_common(1)[0][1]
                    / sum(1 for it in m2o_mem if it["word"] == w) for w in DIGIT_WORDS if w[-1] == "M")  # fmt: skip
    audit[gen] = {
        "Paraphrased (levels 2-3)\nprompt-final words": mean(paraphrased(it, gen) for it in hi if it["word"][-1] == "P"),
        "Paraphrased (levels 2-3)\nmemory-final words": mean(paraphrased(it, gen) for it in hi if it["word"][-1] == "M"),
        "A wrong route gives\nthe right answer": mean(coincidence(it, gen) for it in items),
        "Partner relation\nambiguous": mean(partner_ambiguous(it, gen) for it in items if len(it["word"]) == 3 and it["word"][1] == "P"),
        "Table: answer found\nby row position (P->P)": mean(row_order_hit(it) for it in items if it["format"] == "table" and it["word"] == "PP"),
        "Queried person has a\nlook-alike (levels 1-3)": mean(lookalike_queried(it, gen) for it in items if it["word"] == "PP" and it["level"] >= 1),
        "Most common answer, memory-\nfinal words, many-to-one domains": majority,
    }  # fmt: skip
    audit[gen]["distinct"] = mean(len({start(it) for it in items if it["word"] == w}) for w in WORDS)
(OUT / "audit_v2_v3.json").write_text(json.dumps(audit, indent=2) + "\n")

# ---- figure 1: what is in calib_v3 ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw={"width_ratios": [7, 6, 4.2], "wspace": 0.45})
rows = [f"{g}-start L{lv}" for g in "PMC" for lv in T.LEVELS]
for ax, key, cols, title in ((axes[0], "domain", list(T.DOMAINS), "Scenes by domain"),
                             (axes[1], "format", list(T.FORMATS), "Scenes by format")):  # fmt: skip
    grid = [[len({it["scene"] for it in v3 if it["word"][0] == r[0] and it["level"] == int(r[-1]) and it[key] == c})
             for c in cols] for r in rows]  # fmt: skip
    ax.imshow(grid, cmap=BLUES, vmin=0, vmax=14, aspect="auto")
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            ax.text(j, i, v, ha="center", va="center", fontsize=7.5, color="white" if v > 9 else INK)
    ax.set_xticks(range(len(cols)), cols, rotation=35, ha="right")
    ax.set_yticks(range(len(rows)), rows)
    ax.set_title(title + " (48 scenes per row)", loc="left", fontsize=10, fontweight="bold")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
ax = axes[2]
share = [mean(it["numbers"] == "words" for it in v3 if it["word"] == w) for w in WORDS]
ax.barh(range(len(WORDS)), [100 * (1 - s) for s in share], color=BLUE, height=0.7, label="digits ('is 7')")
ax.barh(range(len(WORDS)), [100 * s for s in share], left=[100 * (1 - s) for s in share], color=ORANGE, height=0.7,
        label="number words ('is seven')", edgecolor=SURF, linewidth=1.5)  # fmt: skip
ax.set_yticks(range(len(WORDS)), WORDS)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xlabel("% of items")
ax.set_title("How each word's context\nstates numbers", loc="left", fontsize=10, fontweight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), frameon=False, ncol=1, fontsize=8)
style(ax)
fig.suptitle(f"calib_v3: {len(v3):,} items = 14 words x 4 levels x 48 scenes; each scene is asked with every word that "
             "starts like it (P-, M- or C-start)", x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=1.04)  # fmt: skip
fig.text(0.01, -0.12, "Memory-start scenes at levels 2-3 come from 4 domains only: shapes, vehicles and instruments have no "
         "hard (indirect) cues.", fontsize=8.5, color=INK2)  # fmt: skip
save(fig, "d1_composition.png")

# ---- figure 2: answers ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [9, 5], "wspace": 0.3})
ax = axes[0]
grid = []
for w in DIGIT_WORDS:
    c = collections.Counter(it["answer"] for it in v3 if it["word"] == w)
    grid.append([100 * c[str(d)] / sum(c.values()) for d in range(1, 10)])
ax.imshow(grid, cmap=BLUES, vmin=0, vmax=30, aspect="auto")
for i, row in enumerate(grid):
    for j, v in enumerate(row):
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7.5, color="white" if v > 20 else INK)
ax.set_xticks(range(9), [str(d) for d in range(1, 10)])
ax.set_yticks(range(len(DIGIT_WORDS)), DIGIT_WORDS)
ax.set_xlabel("answer")
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("Digit answers: % of each word's items (uniform = 11%)", loc="left", fontsize=10, fontweight="bold")
ax = axes[1]
y = range(len(WORDS))
for gen, items, col, lab in ((2, v2, GREY, "calib_v2"), (3, v3, BLUE, "calib_v3")):
    vals = []
    for w in WORDS:
        sel = [it for it in items if it["word"] == w and it["domain"] in M2O]
        vals.append(100 * collections.Counter(it["answer"] for it in sel).most_common(1)[0][1] / len(sel) if sel else 0)
    ax.barh([i + (0.2 if gen == 3 else -0.2) for i in y], vals, height=0.38, color=col, label=lab)
ax.set_yticks(list(y), WORDS)
ax.invert_yaxis()
ax.set_xlabel("% of items with the most common answer")
ax.set_title("Most common answer within animals,\nvehicles, instruments (many-to-one)", loc="left", fontsize=10,
             fontweight="bold")  # fmt: skip
ax.legend(frameon=False, loc="lower right")
style(ax)
fig.suptitle("Answers: prompt-final words are flat by construction; memory-final words follow the facts (4 legs is common)",
             x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=1.02)  # fmt: skip
save(fig, "d2_answers.png")

# ---- figure 3: entities ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), gridspec_kw={"width_ratios": [4, 9], "wspace": 0.25})
ax = axes[0]
for gen, items, col, lab in ((2, v2, GREY, "calib_v2"), (3, v3, BLUE, "calib_v3")):
    vals = [len({start(it) for it in items if it["word"] == w}) for w in WORDS]
    ax.barh([i + (0.2 if gen == 3 else -0.2) for i in range(len(WORDS))], vals, height=0.38, color=col, label=lab)
ax.set_yticks(range(len(WORDS)), WORDS)
ax.invert_yaxis()
ax.set_xlabel("distinct start things (bridges)")
ax.set_title("Bridge entities per word", loc="left", fontsize=10, fontweight="bold")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
style(ax)
ax = axes[1]
anim = collections.Counter(start(it) for it in v3 if it["domain"] == "animals" and it["word"] in ("PP", "MP", "CP"))
order = sorted(anim, key=lambda a: (T.DOMAINS["animals"].values[a], -anim[a]))
legs_col = {2: BLUE, 4: ORANGE, 6: AQUA, 8: YELLOW}
ax.bar(range(len(order)), [anim[a] for a in order], color=[legs_col[T.DOMAINS["animals"].values[a]] for a in order],
       width=0.75, edgecolor=SURF, linewidth=1)  # fmt: skip
ax.set_xticks(range(len(order)), order, rotation=60, ha="right")
ax.set_ylabel("scenes starting from it")
for legs, col in legs_col.items():
    ax.bar([0], [0], color=col, label=f"{legs} legs")
ax.legend(frameon=False, ncol=2, loc="upper left")
eight = sum(anim[a] for a in order if T.DOMAINS["animals"].values[a] == 8)
ax.set_title("Scenes per start animal (animals domain; P-, M-, C-start; all levels)", loc="left", fontsize=10,
             fontweight="bold")  # fmt: skip
ax.text(0.99, 0.97, f"the start's number is drawn uniformly over the domain's numbers,\nso the 3 eight-legged animals start "
        f"{eight} of {sum(anim.values())} animal scenes", transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
        color=INK2)  # fmt: skip
style(ax, "y")
fig.suptitle("Entities: 52-62 bridges per word in calib_v3 (16 animals in the suite behind today's results)", x=0.01,
             ha="left", fontsize=11.5, fontweight="bold", y=1.0)  # fmt: skip
save(fig, "d3_entities.png")

# ---- figure 4: the difficulty ladder ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4.4), gridspec_kw={"wspace": 0.32})
ax = axes[0]
for last, col, lab in (("P", BLUE, "prompt-final words"), ("M", ORANGE, "memory-final words")):
    meds, lo, hi = [], [], []
    for lv in T.LEVELS:
        v = sorted(it["_tokens"] for it in v3 if it["word"][-1] == last and it["level"] == lv)
        meds.append(statistics.median(v))
        lo.append(v[len(v) // 4])
        hi.append(v[3 * len(v) // 4])
    xs = [lv + (-0.06 if last == "P" else 0.06) for lv in T.LEVELS]
    ax.plot(xs, meds, color=col, lw=2, marker="o", markersize=5, label=lab)
    ax.vlines(xs, lo, hi, color=col, lw=1.2)
ax.set_xticks(list(T.LEVELS), [f"L{lv}" for lv in T.LEVELS])
ax.set_ylabel("prompt tokens (median, IQR)")
ax.set_title("Prompt length by level", loc="left", fontsize=10, fontweight="bold")
ax.legend(frameon=False, loc="upper left")
style(ax, "y")
ax = axes[1]
doms = list(T.DOMAINS)
grid = [[mean(it["n_things"] for it in v3 if it["domain"] == d and it["level"] == lv) for lv in T.LEVELS] for d in doms]
ax.imshow(grid, cmap=BLUES, vmin=0, vmax=14, aspect="auto")
for i, row in enumerate(grid):
    for j, v in enumerate(row):
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8, color="white" if v > 9 else INK)
ax.set_xticks(range(4), [f"L{lv}\n(asks {T.LEVELS[lv]['entities']})" for lv in T.LEVELS])
ax.set_yticks(range(len(doms)), doms)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("Things per scene (capped by domain size)", loc="left", fontsize=10, fontweight="bold")
ax = axes[2]
ax.axis("off")
cells = [[f"L{lv}", str(k["entities"]), "yes" if k["distractors"] else "-", str(k["filler"]), "yes" if k["paraphrase"] else "-",
          "yes" if k["hard_cues"] else "-"] for lv, k in T.LEVELS.items()]  # fmt: skip
tb = ax.table(cellText=cells, colLabels=["level", "entities", "look-\nalikes", "filler", "para-\nphrase", "hard\ncues"],
              loc="center", cellLoc="center")  # fmt: skip
tb.auto_set_font_size(False)
tb.set_fontsize(8.5)
tb.scale(1.1, 2.2)
for (r, _), cell in tb.get_celld().items():
    cell.set_edgecolor(GRID)
    cell.set_facecolor(SURF if r else "#f0efec")
ax.set_title("The ladder (all knobs up together)", loc="left", fontsize=10, fontweight="bold")
fig.suptitle("Difficulty: one ladder; each word is calibrated to the hardest level where the 27B scores 85-95%", x=0.01,
             ha="left", fontsize=11.5, fontweight="bold", y=1.04)  # fmt: skip
save(fig, "d4_difficulty.png")

# ---- figure 5: before / after on the audit's checks ----
keys = [k for k in audit[3] if k != "distinct"]
fig, axes = plt.subplots(1, len(keys), figsize=(16, 3.6), sharey=False, gridspec_kw={"wspace": 0.55})
for ax, k in zip(axes, keys, strict=True):
    vals = [100 * audit[2][k], 100 * audit[3][k]]
    ax.bar([0, 1], vals, color=[GREY, BLUE], width=0.62)
    for x, v in zip([0, 1], vals, strict=True):
        ax.text(x, v + 2, f"{v:.0f}%", ha="center", fontsize=9, color=INK)
    ax.set_xticks([0, 1], ["v2", "v3"])
    ax.set_ylim(0, 112)
    ax.set_yticks([])
    ax.set_title(k, fontsize=8.5, loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
fig.suptitle("Audit checks, calib_v2 (grey) vs calib_v3 (blue), same measurement code on both sets", x=0.01, ha="left",
             fontsize=11.5, fontweight="bold", y=1.12)  # fmt: skip
fig.text(0.01, -0.1, "Row position: share of table P->P items where the queried person's row in the picks table is the same "
         "row as their pick's locker (chance ~1/entities). Look-alike: the queried person has a look-alike name with a different pick.",
         fontsize=8, color=INK2)  # fmt: skip
save(fig, "d5_audit_before_after.png")

# ---- figure 6: entity spread in the existing knock-out results ----
from scripts import exp09_bind_recall as E  # noqa: E402

bridge = {}
for fam in ("BR", "RR"):
    bridge.update({(fam, it["id"]): it["bridge"] for it in S.load(fam)})
for i, it in enumerate(E.ITEM_SETS["bind_recall"][2]()):
    bridge[(f"country-{it['family']}", E.uid(it, i))] = it["bridge"]
rows = [json.loads(line) for line in (pins.RESULTS_DIR / "ablate_v2" / "paper10_stability_tf32" / "rows.jsonl").open()]
fams = [
    ("BR", "P->M (suite BR)"),
    ("RR", "M->M (suite RR)"),
    ("country-B", "countries, given"),
    ("country-R", "countries, recalled"),
]
fig, axes = plt.subplots(1, 4, figsize=(16, 5.4), gridspec_kw={"wspace": 0.55})
for ax, (fam, title) in zip(axes, fams, strict=True):
    by = collections.defaultdict(list)
    for r in rows:
        if r["condition"] == "paper10" and r["family"] == fam and r["kind"] == "clean":
            by[bridge[(fam, r["id"])]].append(r["correct"])
    ents = sorted(by, key=lambda e: mean(by[e]))
    ax.scatter([100 * mean(by[e]) for e in ents], range(len(ents)), s=[18 * len(by[e]) for e in ents], color=BLUE,
               edgecolor=SURF, linewidth=1.5, zorder=3)  # fmt: skip
    item_mean = 100 * mean(x for v in by.values() for x in v)
    ax.axvline(item_mean, color=INK2, lw=1, ls="--")
    ax.text(
        item_mean,
        len(ents) - 0.2,
        f"all items {item_mean:.0f}%",
        fontsize=8,
        color=INK2,
        ha="right" if item_mean > 70 else "center",
        va="bottom",
    )
    ax.set_yticks(range(len(ents)), [f"{e} (n={len(by[e])})" for e in ents])
    ax.set_xlim(-5, 105)
    ax.set_xlabel("accuracy, J-space removed (%)")
    ax.set_title(f"{title}: {len(ents)} bridges", loc="left", fontsize=10, fontweight="bold", pad=18)
    style(ax)
fig.suptitle("The data behind today's results: survival under paper10 (layers 32/36/40) depends on the bridge entity; "
             "dot size = items", x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=1.02)  # fmt: skip
save(fig, "d6_entity_spread_existing.png")
print(json.dumps(audit, indent=1))
