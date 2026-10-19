"""B0 (exp20): before any edit, can the model do part B's tasks, and in which format?

Every part B result edits a model that is supposed to be doing a task. exp20 runs each task unedited and greedy on
every item, in three formats: raw text (no chat template; B1 and exp09 ran this way), the chat template with thinking
off (the statement turned into a question; B1: a fill-in-the-blank instruction), and the chat template with the
assistant turn prefilled "Answer:" (brew ran this way). exp09's items also get their counterfactual (cf) and off-path
(off) prompts, as exp09's gate, and every exp09 and brew item gets each step alone (hop1, hop2).

This script re-judges every continuation itself and recomputes the table, then checks exp20 against the eligibility
of the runs it underlies (exp02, exp09, exp04), and prints examples to read.

Reads only results/exp20_competence/v1/{manifest.json,items.jsonl}, the item files in data/ it names, and
results/exp02_swaps/main_v4b200_jpp/items.jsonl, results/exp09_bind_recall/{map_v1,map_lookup_v2,map_rl_v1}/
items.jsonl, results/exp04_brew_patch/patch_map_fresh/items.jsonl. No code from this repo. Standard library only.
Run from the repo root:  python3 verification/b0_exp20.py
"""

import json
import math
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path

RUN = Path("results/exp20_competence/v1")
FORMATS = ("raw", "chat", "chat_prefill")
EXP09 = ("R", "B", "L", "RL")
BREW = ("brew_bank", "brew_fresh", "brew_test")
PALETTE = ("black", "blue", "brown", "gold", "gray", "green", "orange", "pink", "purple", "red", "teal", "white")


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def ci(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} {100 * p:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


def first_word_of(text, words):
    """The first word of `words` in the continuation's first non-empty line (lowercase), or None."""
    line = next((ln for ln in text.lower().split("\n") if ln.strip()), "")
    return next((w for w in re.findall(r"[a-z]+", line) if w in words), None)


NUMBER = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def in_first_clause(text, answer):
    """The answer (or its numeral / number word) as a run of words in the first clause (to the first . ! ? or line
    break after leading whitespace). A simpler judge than exp13's (no compound words such as 'honeybee')."""
    clause = re.split(r"(?<!\d)[.!?](?!\d)|\n", text.lstrip(), maxsplit=1)[0]
    ws = re.findall(r"[a-z0-9]+", clause.lower())
    forms = [re.findall(r"[a-z0-9]+", answer.lower())]
    a = answer.strip().lower()
    if a.isdigit() and int(a) < len(NUMBER):
        forms.append([NUMBER[int(a)]])
    elif a in NUMBER:
        forms.append([str(NUMBER.index(a))])
    return any(ws[i : i + len(f)] == f for f in forms for i in range(len(ws) - len(f) + 1))


manifest = json.loads((RUN / "manifest.json").read_text())
rows = jsonl(RUN / "items.jsonl")
data = {}
for task, pin in manifest["tasks"].items():
    items = json.loads(Path(pin["file"]).read_text())["items"]
    data[task] = items
capitals = {c.lower() for c in json.loads(Path("data/bind_recall.json").read_text())["capitals"].values()}
countries = {c.lower() for c in json.loads(Path("data/bind_recall.json").read_text())["capitals"]}


def expected_and_words(task, kind, item):
    """What the continuation should name, and the word set it is judged against, from the item file alone."""
    if task == "probe_swap":
        return item["answer"], None
    if task in BREW:
        return (item["intermediates"][0] if kind == "hop1" else item["answer"]), set(PALETTE)
    if kind == "hop1":
        return item["bridge"], countries
    answer = item["target_answer"] if kind == "cf" else item["answer"]
    return answer, capitals if task in ("R", "B") else set(PALETTE)


print("== 0. The run")
print(f"   {len(rows)} prompts; formats {FORMATS}; manifest written {manifest['written_utc']}")
print(f"   generation: {manifest['generation']}")
for task, pin in manifest["tasks"].items():
    n_items = len({r["index"] for r in rows if r["task"] == task})
    print(f"   {task:11s} {n_items:4d} items from {pin['file']} (family {pin['family']})")

print("\n== 1. Re-judging every continuation (this script's judge vs the run's 'correct')")
mine = {}
disagree = defaultdict(list)
for r in rows:
    item = data[r["task"]][r["index"]]
    exp, words = expected_and_words(r["task"], r["kind"], item)
    assert exp.lower() == r["expected"].lower(), (r["task"], r["index"], r["kind"], exp, r["expected"])
    if words is None:
        ok = in_first_clause(r["continuation"], exp) and not in_first_clause(r["continuation"], item["swap_answer"])
    else:
        ok = first_word_of(r["continuation"], words) == exp.lower()
    mine[id(r)] = ok
    if ok != r["correct"]:
        disagree[r["task"]].append(r)
print(f"   expected answers re-derived from the item files: all {len(rows)} match")
print(f"   judgements that differ: {sum(len(v) for v in disagree.values())} of {len(rows)}")
for task, rs in disagree.items():
    for r in rs[:5]:
        print(f"      {task} {r['name']} {r['kind']}/{r['format']}: run says {r['correct']}, expected {r['expected']!r}, "
              f"said {r['continuation'][:50]!r}")  # fmt: skip
print("   (probe_swap: this judge has no compound-word rule, exp13's does, e.g. 'drumsticks' for 'sticks')")

print("\n== 2. The table (this script's judgements; Wilson 95% CIs over items)")
cell = defaultdict(lambda: [0, 0])
per_item = defaultdict(dict)
pvals = defaultdict(list)
for r in rows:
    key = (r["task"], r["format"], r["kind"])
    cell[key][0] += mine[id(r)]
    cell[key][1] += 1
    per_item[(r["task"], r["format"], r["index"])][r["kind"]] = mine[id(r)]
    if r["kind"] == "clean" and r["p_answer"] is not None:
        pvals[(r["task"], r["format"])].append(r["p_answer"])
for task in manifest["tasks"]:
    print(f"\n   {task}")
    for fmt in FORMATS:
        if not cell[(task, fmt, "clean")][1]:
            continue
        line = f"      {fmt:13s} clean {ci(*cell[(task, fmt, 'clean')]):22s}"
        items = [v for (t, f, _), v in per_item.items() if t == task and f == fmt]
        if task in EXP09:
            k3 = sum(all(v[k] for k in ("clean", "cf", "off")) for v in items)
            line += f" all three (exp09's gate) {ci(k3, len(items)):22s}"
        if any("hop1" in v for v in items):
            both = [v for v in items if v["hop1"] and v["hop2"]]
            line += (f" hop1 {ci(*cell[(task, fmt, 'hop1')])}  hop2 {ci(*cell[(task, fmt, 'hop2')])}"
                     f"  clean given both hops {ci(sum(v['clean'] for v in both), len(both))}")  # fmt: skip
        line += f"  median p(answer) {statistics.median(pvals[(task, fmt)]):.2f}"
        print(line)
print("\n   README claims (exp20): exp09 in chat 99.7-100% clean (R 360/360, B 400/400, L 400/400, RL 718/720), all")
print("   three >= 716/720, hops 100%; raw: R 274/360 = 76% [71, 80], all three 189/360 = 52% [47, 58], B 94%, L 98%,")
print("   RL 96%; B1 77/90 = 86% [77, 91] raw and chat; brew (chat + Answer:) bank 100/100, fresh 177/200, test")
print("   522/600, each step alone 100%; median p(answer) raw .20-.64, chat .97-.99. p(answer) is the run's own value")
print("   (it needs the model); every other number above is recomputed here.")

print("\n== 3. What the raw-text misses are (exp09 R, clean prompt)")
fails = [r for r in rows if r["task"] == "R" and r["format"] == "raw" and r["kind"] == "clean" and not mine[id(r)]]
kinds = defaultdict(int)
for r in fails:
    t = r["continuation"]
    if "<think>" in t:  # the model starts its own reply, as to a user turn (sometimes after "A." or ":")
        kinds["opens a thinking turn"] += 1
    elif re.match(r"\s*A[.:]", t):
        kinds["writes a multiple-choice list"] += 1
    else:
        kinds["other"] += 1
print(f"   {len(fails)} misses: {dict(kinds)}")

print("\n== 4. Against the runs exp20 underlies (the raw format, as they ran)")
ex02 = jsonl("results/exp02_swaps/main_v4b200_jpp/items.jsonl")
elig02 = {r["name"] for r in ex02 if r["status"] == "eligible"}
right02 = {r["name"] for r in rows if r["task"] == "probe_swap" and r["format"] == "raw" and mine[id(r)]}
print(
    f"   exp02 main_v4b200_jpp eligible {len(elig02)}; exp20 raw correct {len(right02)}; both {len(elig02 & right02)}"
)
for fam, run in (("R", "map_v1"), ("B", "map_v1"), ("L", "map_lookup_v2"), ("RL", "map_rl_v1")):
    st = [r for r in jsonl(f"results/exp09_bind_recall/{run}/items.jsonl") if r["family"] == fam]
    aligned = [r for r in st if r["status"] != "unaligned"]
    agree = 0
    for r in aligned:
        idx = int(r["name"].split("-")[1])
        v = per_item[(fam, "raw", idx)]
        agree += all(v[k] for k in ("clean", "cf", "off")) == (r["status"] in ("eligible", "eligible_not_sampled"))
    elig = sum(r["status"] in ("eligible", "eligible_not_sampled") for r in aligned)
    chat3 = sum(all(per_item[(fam, "chat_prefill", int(r["name"].split("-")[1]))][k] for k in ("clean", "cf", "off")) for r in aligned)  # fmt: skip
    print(f"   exp09 {run} {fam}: {len(aligned)} aligned, {elig} pass its gate; exp20 raw agrees on {agree}; in chat + "
          f"Answer: {chat3} would pass")  # fmt: skip
pm = jsonl("results/exp04_brew_patch/patch_map_fresh/items.jsonl")
cw = {r["name"] for r in pm if r["status"] == "clean_wrong"}
w20 = {r["name"] for r in rows if r["task"] == "brew_fresh" and r["format"] == "chat_prefill" and r["kind"] == "clean" and not mine[id(r)]}  # fmt: skip
print(f"   exp04 patch_map_fresh clean_wrong {len(cw)}; exp20 (chat + Answer:) wrong {len(w20)}; both {len(cw & w20)}")

print("\n== 5. Examples to read (random, seed 0): the prompt's end and the continuation")
rng = random.Random(0)
for task, fmt in (("R", "raw"), ("R", "chat"), ("B", "raw"), ("RL", "raw"), ("probe_swap", "raw"), ("probe_swap", "chat"), ("brew_test", "chat_prefill")):  # fmt: skip
    pool = [r for r in rows if r["task"] == task and r["format"] == fmt and r["kind"] == "clean"]
    print(f"\n   {task} / {fmt}")
    for r in rng.sample(pool, 4):
        print(f"      [{'right' if mine[id(r)] else 'WRONG'}] ...{r['text'][-70:]!r} -> {r['continuation'][:60]!r} (expected {r['expected']})")  # fmt: skip
