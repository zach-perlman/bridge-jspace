"""CPU audit of jsuite_v2 (Zach, 2026-10-24): the v2 fixes hold in the generated data."""
import collections, json, re, sys
sys.path.insert(0, "."); sys.path.insert(0, "src")
D = "data/tasks_v2"
sets = {sp: [json.loads(l) for l in open(f"{D}/jsuite_v2_{sp}_chat/items.jsonl")] for sp in ("dev", "test")}
fails = collections.Counter()
for sp, its in sets.items():
    facts = [it for it in its if it["module"] == "facts"]
    by_scene = collections.defaultdict(dict)
    for it in facts:
        by_scene[it["scene"]][it["final"]] = it
    unequal = sum(1 for sc in by_scene.values() if len({it["bridge_mentions"] for it in sc.values()}) > 1)
    incomplete = sum(1 for sc in by_scene.values() if set(sc) != set("PKMAN"))
    for it in facts:
        voc = it["answer_vocab"]
        hit = [w for w in voc if re.search(r"(?i)\b" + re.escape(w) + r"\b", it["context"])]
        if it["final"] == "N" and hit: fails["N passage has answer words"] += 1
        if it["final"] == "M" and re.search(r"(?i)\b" + re.escape(it["real"]) + r"\b", it["context"]): fails["M passage has the answer"] += 1
        if re.search(r"(?i)\b" + re.escape(it["answer"]) + r"\b", it["question"]): fails["answer in question"] += 1
        if it["bridge_mentions"] == 0: fails["bridge never named"] += 1
    ment = collections.Counter((it["start"], it["final"], it["bridge_mentions"]) for it in facts)
    print(f"## {sp}: facts {len(facts)}, scenes {len(by_scene)}, unequal bridge mentions across finals {unequal}, incomplete scenes {incomplete}")
    print("   bridge mentions by start/final:", {f"{s}{f}": collections.Counter(m for (s2, f2, m), n in ment.items() for _ in range(n) if (s2, f2) == (s, f)).most_common(2) for s in "PMT" for f in "PKMAN"})
    print("   eponymous items:", sum(it["eponymous"] for it in facts), "| answers per relation:", {r: len({it["real"] for it in facts if it["relation"] == r}) for r in sorted({it["relation"] for it in facts})})
    print("   words:", dict(collections.Counter(it["word"] for it in its)))
    print("   filler sentences distinct (facts):", len({s for it in facts for s in re.split(r"(?<=[.!?])\s+", it["context"])}))
fb = {sp: {(it["relation"], it["bridge"]) for it in its if it["module"] == "facts"} for sp, its in sets.items()}
print("facts bridges dev & test overlap:", len(fb["dev"] & fb["test"]))
th = {sp: {b for it in its if it["module"] == "threehop" for b in it.get("bridges", [])} for sp, its in sets.items()}
print("threehop: South Africa present:", any("South Africa" in json.dumps(it) for its in sets.values() for it in its if it["module"] == "threehop"), "| dev/test chain-entity overlap:", len(th["dev"] & th["test"]))
ids = [it["id"] for its in sets.values() for it in its]
print("ids unique:", len(ids) == len(set(ids)), "| fails:", dict(fails) or "none")
