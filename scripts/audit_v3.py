"""audit_v3 (Zach, 2026-10-27, prereg amendment 58 note 4): measures every confound check on a jsuite v3 set after it is
built, and draws one overview figure. CPU only (tokenizers loaded offline).

python scripts/audit_v3.py NAME   ->  results/dataset_audit/NAME/{audit.json, audit.md, overview.png}
"""

from __future__ import annotations

import collections
import json
import re
import statistics
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[1] / "src"), str(Path(__file__).resolve().parents[1])]
from bridge_jspace import pins  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STARTS = ["P", "M", "W", "R", "T", "X", "Q", "J", "Y"]
FINALS = ["P", "K", "M", "A", "N", "H", "C", "D", "E", "F", "G"]
RELS = ["people", "cities", "companies", "landmarks", "films"]
MODELS = ["qwen3.6-27b", "qwen3.5-9b", "nemotron-3.5-lightning", "muse-glimmer-30b", "ministral-3-14b"]


def has(text: str, w: str) -> bool:
    return re.search(r"(?i)(?<![\w])" + re.escape(w) + r"(?![\w])", text) is not None


def main(name: str) -> None:
    rows = [json.loads(line) for line in (ROOT / "data/tasks_v2" / f"{name}_test_chat" / "items.jsonl").open()]
    r1 = ROOT / "data/tasks_v2" / f"{name}r1_test_chat" / "items.jsonl"  # the second rendering, split off after the build
    if r1.exists():
        rows += [json.loads(line) for line in r1.open()]
    facts = [r for r in rows if r.get("module") == "facts"]
    probes = [r for r in rows if r.get("module") == "probes"]
    bridges = json.loads((ROOT / "data/v3_bridges.json").read_text())
    out_dir = ROOT / "results/dataset_audit" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(label: str, bad: int, total: int, expect: str = "0 violations") -> None:
        checks.append({"check": label, "violations": bad, "of": total, "expect": expect, "pass": bad == 0})

    # composition
    words = collections.Counter((r["start"], r["final"], r["level"]) for r in facts if r["rep"] == 0)
    rel_answers = {rel: collections.Counter(b["answer"] for b in bridges if b["relation"] == rel) for rel in RELS}
    shares = {rel: sorted((v / sum(c.values()) for v in c.values()), reverse=True) for rel, c in rel_answers.items()}
    v2 = [json.loads(line) for line in (ROOT / "data/tasks_v2/jsuite_v2_test_chat/items.jsonl").open()]
    v2f = [r for r in v2 if r.get("module") == "facts" and r["word"] == "MM"]
    v2_shares = {}
    for rel in sorted({r["relation"] for r in v2f}):
        c = collections.Counter(r["answer"] for r in v2f if r["relation"] == rel)
        v2_shares[rel] = max(c.values()) / sum(c.values())

    # integrity
    m_like = [r for r in facts if r["final"] in "MN"]
    check("recalled finals (M, N): answer absent from the passage", sum(has(r["context"], r["answer"]) for r in m_like), len(m_like))
    a_items = [r for r in facts if r["final"] == "A"]
    check("answer-elsewhere finals (A): answer present once on another entity", sum(not has(r["context"], r["answer"]) for r in a_items), len(a_items))
    n_items = [r for r in facts if r["final"] == "N"]
    check("nothing-stated finals (N): no answer-vocabulary word anywhere",
          sum(any(has(r["context"], v) for v in r["answer_vocab"]) for r in n_items), len(n_items))
    r_items = [r for r in facts if r["start"] == "R"]
    check("never-named start (R): bridge never in the passage", sum(has(r["context"], r["bridge"]) for r in r_items), len(r_items))
    named = [r for r in facts if r["start"] != "R"]
    check("every other start names the bridge", sum(r["bridge_mentions"] < 1 for r in named), len(named))
    w_items = [r for r in facts if r["start"] == "W"]
    check("two-mention start (W): the distractor is named and not bound to anyone",
          sum((not has(r["context"], r["distractor_mention"])) or r["distractor_mention"] in r["entities"] for r in w_items), len(w_items))
    desc = [r for r in facts if r["start"] in ("M", "W", "R")]
    check("described starts: the question never names the bridge", sum(has(r["question"], r["bridge"]) for r in desc), len(desc))
    check("described starts: the question never contains the answer or an alias",
          sum(any(has(r["question"], a) for a in [r["real"], *r.get("answer_aliases", [])]) for r in desc), len(desc))
    stated = [r for r in facts if r["final"] in "KGH"]
    check("stated finals (K, G, H): the true answer is in the passage", sum(not has(r["context"], r["answer"]) for r in stated), len(stated))
    conf = [r for r in facts if r["final"] in "CDEF"]
    check("conflict finals: the counterfactual is in the passage", sum(not has(r["context"], r["conflict_value"]) for r in conf), len(conf))
    check("conflict finals: the counterfactual differs from the truth", sum(r["conflict_value"] == r["memory_answer"] for r in conf), len(conf))
    by_id = {r["id"]: r for r in facts}
    ys = [r for r in facts if r["start"] == "Y"]
    bad_pairs = 0
    for y in ys:
        p = by_id.get(y["pair_of"])
        if p is None:
            bad_pairs += 1
            continue
        back = re.sub(r"\b" + re.escape(y["bridge"]) + r"\b", p["bridge"], y["context"])
        if y["final"] == "K":  # a stated pair also states the other bridge's true value (as it reads in a sentence)
            disp = {"Netherlands": "the Netherlands", "United States": "the United States", "Czech Republic": "the Czech Republic",
                    "United Arab Emirates": "the United Arab Emirates"}
            back = re.sub(r"(?i)\b" + re.escape(disp.get(y["real"], y["real"])) + r"\b", disp.get(p["real"], p["real"]), back)
        if p["context"] != back:
            bad_pairs += 1
    check("counterfactual pairs (Y): passage identical to its P partner except the bridge", bad_pairs, len(ys))
    xs = [r for r in facts if r["start"] == "X"]
    bad_x = 0
    nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for r in xs:
        a_, b_ = re.search(r"number (\w+) minus (\w+)", r["question"]).groups()
        pos = nums.index(a_) - nums.index(b_)
        if f"number {nums[pos]} is {r['bridge']}" not in r["context"]:
            bad_x += 1
    check("computed start (X): the arithmetic picks the bridge", bad_x, len(xs))
    ids = [r["id"] for r in rows]
    check("duplicate item ids", len(ids) - len(set(ids)), len(ids))
    anchors = {a for r in facts if r.get("anchors") for a in r["anchors"]}
    realnames = {b["bridge"] for b in bridges} | {b["answer"] for b in bridges}
    check("hard-read anchors are made up (not a bridge or answer)", len(anchors & realnames), len(anchors))
    shared = [r for r in facts if r["final"] in "KCH" and any(e != r["bridge"] and [b for b in bridges if b["bridge"] == e and b["answer"] == r["real"]] for e in r["entities"])]
    checks.append({"check": "scenes where another entity shares the bridge's answer (reported, not excluded)", "violations": len(shared),
                   "of": len([r for r in facts if r["final"] in "KCH"]), "expect": "a few", "pass": True, "note": True})

    # first-token uniqueness per model
    from transformers import AutoTokenizer

    tok_report = {}
    for m in MODELS:
        t = pins.TARGETS[m]
        try:
            tok = AutoTokenizer.from_pretrained(t["repo"], revision=t["revision"], local_files_only=True)
        except Exception as e:  # noqa: BLE001
            tok_report[m] = f"tokenizer not loadable offline: {str(e)[:80]}"
            continue
        coll, low = 0, 0
        for rel in RELS:
            vocab = sorted(rel_answers[rel])
            for case in ("cap", "low"):
                first = collections.defaultdict(set)
                for v in vocab:
                    first[tok(v if case == "cap" else v.lower(), add_special_tokens=False)["input_ids"][0]].add(v)
                n = sum(len(x) > 1 for x in first.values())
                coll += n if case == "cap" else 0
                low += n if case == "low" else 0
        tok_report[m] = coll
        tok_report[m + " (lowercase forms, reported)"] = low
    for m in MODELS:
        if isinstance(tok_report.get(m), int):
            check(f"answers (as written) share no first token: {m}", tok_report[m], len(RELS))

    # lengths and key positions (Qwen tokenizer)
    t = pins.TARGETS["qwen3.6-27b"]
    tok = AutoTokenizer.from_pretrained(t["repo"], revision=t["revision"], local_files_only=True)
    lengths = collections.defaultdict(list)
    keypos = collections.defaultdict(list)
    for r in facts:
        if r["rep"] != 0 or r["start"] != "P" or r["final"] not in "KMH":
            continue
        lengths[(r["level"], r["final"])].append(len(tok(r["context"], add_special_tokens=False)["input_ids"]))
        i = r["context"].find(r["bridge"])
        keypos[r["level"]].append(i / max(1, len(r["context"])))
    conflict_mix = collections.Counter((r["final"], "near" if r["cf_near"] else "far") for r in conf if r["rep"] == 0)

    summary = {"name": name, "n_items": len(rows), "n_facts": len(facts), "n_probes": len(probes), "per_rep": len(facts) // 2,
               "bridges": {rel: sum(1 for b in bridges if b["relation"] == rel) for rel in RELS},
               "answers": {rel: len(c) for rel, c in rel_answers.items()}, "max_share": {rel: s[0] for rel, s in shares.items()},
               "v2_max_share": v2_shares, "checks": checks, "tokenizers": tok_report,
               "length_median": {f"L{k[0]}-{k[1]}": statistics.median(v) for k, v in sorted(lengths.items())},
               "keypos_median": {f"L{k}": round(statistics.median(v), 3) for k, v in sorted(keypos.items())},
               "conflict_mix": {f"{k[0]}-{k[1]}": v for k, v in sorted(conflict_mix.items())},
               "popularity": {rel: dict(collections.Counter(b["popularity"] for b in bridges if b["relation"] == rel)) for rel in RELS},
               "name_reveals": {rel: sum(b["name_reveals_answer"] for b in bridges if b["relation"] == rel) for rel in RELS}}
    (out_dir / "audit.json").write_text(json.dumps(summary, indent=1) + "\n")
    md = [f"# {name}: dataset audit", "", f"{len(facts)} fact items ({len(facts) // 2} per rendering), {len(probes)} probes.", "",
          "| check | violations | of | expected | pass |", "|---|---|---|---|---|"]
    md += [f"| {c['check']} | {c['violations']} | {c['of']} | {c['expect']} | {'yes' if c['pass'] else 'NO'} |" for c in checks]
    (out_dir / "audit.md").write_text("\n".join(md) + "\n")
    figure(out_dir / "overview.png", words, shares, v2_shares, lengths, keypos, summary["conflict_mix"], checks, summary)
    print("\n".join(md))


def figure(path, words, shares, v2_shares, lengths, keypos, conflict_mix, checks, s) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans"})
    blue, grey, red = "#2a78d6", "#8a8a8a", "#d03b3b"
    fig = plt.figure(figsize=(16, 10.5))
    fig.suptitle(f"jsuite v3 at a glance: {s['per_rep']:,} items per rendering (x2 renderings), {sum(s['bridges'].values())} bridges, "
                 f"5 relations, {s['n_probes']} skip-the-bridge probes", x=0.02, ha="left", fontsize=14, fontweight="bold")

    # (a) the design matrix
    ax = fig.add_axes((0.10, 0.53, 0.25, 0.37))
    import numpy as np

    grid = np.zeros((len(STARTS), len(FINALS)))
    lab = [["" for _ in FINALS] for _ in STARTS]
    for (st, f, lv), n in words.items():
        i, j = STARTS.index(st), FINALS.index(f)
        grid[i, j] += n
        lab[i][j] = (lab[i][j] + "," if lab[i][j] else "") + str(lv)
    ax.imshow(np.where(grid > 0, np.log10(grid + 1), np.nan), cmap="Blues", vmin=0, vmax=4, aspect="auto")
    for i in range(len(STARTS)):
        for j in range(len(FINALS)):
            if lab[i][j]:
                ax.text(j, i, "L" + lab[i][j], ha="center", va="center", fontsize=7, color="#0b0b0b")
    snames = ["P read", "M described", "W two mentions", "R never named", "T tracked", "X computed", "Q table", "J JSON", "Y cf. pair"]
    fnames = ["P made-up", "K stated", "M recalled", "A ans. elsewhere", "N nothing", "H hard read", "C conflict", "D conf. attrib.",
              "E conf. 'notes' q", "F attrib.+'notes'", "G attrib. true"]
    ax.set_yticks(range(len(STARTS)), snames)
    ax.set_xticks(range(len(FINALS)), fnames, rotation=55, ha="right")
    ax.set_title("(a) Design: which levels exist for each start x final", loc="left", fontweight="bold")

    # (b) answer balance
    ax = fig.add_axes((0.40, 0.58, 0.25, 0.32))
    for k, (rel, sh) in enumerate(shares.items()):
        ax.plot(range(1, len(sh) + 1), [100 * x for x in sh], marker="o", ms=3, lw=1.2, label=f"{rel} ({len(sh)} answers)")
    ax.axhline(5, color=red, ls="--", lw=1)
    ax.text(30, 5.6, "5% bar", color=red)
    ax.set_xlabel("answers, most common first")
    ax.set_ylabel("% of the relation's bridges")
    ax.set_ylim(0, 45)
    for v in v2_shares.values():
        ax.plot([0.3], [100 * v], marker="_", ms=12, color=grey)
    ax.text(0.6, 100 * max(v2_shares.values()), "v2's commonest answers\n(grey ticks, up to 42%)", color=grey, fontsize=8, va="center")
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    ax.set_title("(b) Answer balance: every v3 answer is under 5%", loc="left", fontweight="bold")

    # (c) passage length by level
    ax = fig.add_axes((0.71, 0.58, 0.27, 0.32))
    keys = [(lv, f) for lv in (1, 2, 3) for f in "KMH" if (lv, f) in lengths]
    ax.boxplot([lengths[k] for k in keys], tick_labels=[f"L{lv}\n{f}" for lv, f in keys], showfliers=False,
               medianprops={"color": blue})
    ax.set_ylabel("passage tokens (read start)")
    ax.set_title("(c) Passage length by level and final", loc="left", fontweight="bold")

    # (d) where the bridge first appears
    ax = fig.add_axes((0.07, 0.08, 0.20, 0.30))
    ax.boxplot([keypos[lv] for lv in sorted(keypos)], tick_labels=[f"L{lv}" for lv in sorted(keypos)], showfliers=False,
               medianprops={"color": blue})
    ax.axhline(1 / 3, color=grey, ls=":", lw=1)
    ax.set_ylabel("first mention of the bridge\n(fraction of the passage)")
    ax.set_title("(d) Level 3 puts the bridge early", loc="left", fontweight="bold")

    # (e) conflict design
    ax = fig.add_axes((0.32, 0.08, 0.20, 0.30))
    fs = ["C", "D", "E", "F"]
    near = [conflict_mix.get(f"{f}-near", 0) for f in fs]
    far = [conflict_mix.get(f"{f}-far", 0) for f in fs]
    ax.bar(fs, near, color=blue, label="near (same region)")
    ax.bar(fs, far, bottom=near, color=grey, label="far / films")
    ax.set_xticks(range(4), ["C plain", "D attributed", "E 'notes' q", "F both"])
    ax.set_ylabel("items (one rendering)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("(e) Conflict finals: near and far counterfactuals", loc="left", fontweight="bold")

    # (f) integrity checks
    ax = fig.add_axes((0.56, 0.04, 0.43, 0.40))
    ax.axis("off")
    ax.set_title("(f) Integrity checks, measured on the built set", loc="left", fontweight="bold")
    y = 0.98
    for c in checks:
        mark = "note" if c.get("note") else ("PASS" if c["pass"] else "FAIL")
        col = blue if c["pass"] else (grey if mark == "note" else red)
        ax.text(0.0, y, mark, color=col, fontweight="bold", fontsize=8, transform=ax.transAxes, va="top")
        ax.text(0.07, y, f"{c['check']}: {c['violations']:,} of {c['of']:,}", fontsize=8, transform=ax.transAxes, va="top")
        y -= 0.95 / max(1, len(checks))
    fig.savefig(path, dpi=150)


if __name__ == "__main__":
    main(sys.argv[1])
