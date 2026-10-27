"""Dan's position check for the probes (x0_probe_27b, qwen35_9b_x0_probe):
1. the probe item's token index == the X0 patch index (cases.jsonl 'pos' of the X0 run and of the single-change run);
2. that index's character span lies inside the asked person's pick sentence, not the bridge's locker sentence, and
   the token is the bridge word (re-rendered prompt, the ids equal to the run's);
3. 5 random locker-before items (seed 0) with the probed token marked.
Run with BJ_TARGET unset for the 27B and BJ_TARGET=qwen3.5-9b for the 9B."""

import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.tokens import raw_encoding
from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x0_probe as P

probe_run, x0_run, single_run = sys.argv[1:4]
tok = SP.load_tokenizer()
items = X.read_jsonl(P.RESULTS / probe_run / "items.jsonl")
x0_cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / x0_run / "cases.jsonl") if c["rendering"] == "chat"}
single_cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / single_run / "cases.jsonl") if c["rendering"] == "chat"}
print(pins.TARGET, probe_run, len(items), "items")

bad1 = [it["scene"] for it in items if x0_cases[it["scene"]]["pos"] != it["pos"]]
bad1s = [it["scene"] for it in items if it["scene"] in single_cases and single_cases[it["scene"]]["pos"] != it["pos"]]
print(
    "1. probe index == X0 patch index:",
    len(items) - len(bad1),
    "of",
    len(items),
    "| == single-change patch index:",
    sum(it["scene"] in single_cases for it in items) - len(bad1s),
    "of",
    sum(it["scene"] in single_cases for it in items),
)

bad2, marked = [], {}
for it in items:
    c = x0_cases[it["scene"]]
    ids = c["readers"][X.LOOKUP]["ids"]["org"]
    item = {
        "context": c["context"],
        "question": c["readers"][X.LOOKUP]["question"],
        "word": "PP",
        "format": "prose",
        "kind": "digit",
        "id": c["readers"][X.LOOKUP]["id"],
    }
    text = X.render(tok, item, "chat", c["context"])
    enc = raw_encoding(tok, text, offsets=True)
    assert list(enc["input_ids"]) == ids, f"{it['scene']}: re-rendered ids differ from the run's"
    s, e = enc["offset_mapping"][it["pos"]]
    c0 = text.index(c["context"])
    asked = re.search(r"([A-Z][a-z]+)'s pick", item["question"]).group(1)
    pick = re.search(rf"\b{asked} picked (?:the )?{c['bridge']}\.", c["context"])
    locker = re.search(rf"The locker of (?:the )?{c['bridge']} is \w+\.", c["context"])
    in_pick = c0 + pick.start() <= s and e <= c0 + pick.end()
    in_locker = locker is not None and c0 + locker.start() <= s and e <= c0 + locker.end()
    word = text[s:e].strip()
    if not in_pick or in_locker or word != c["bridge"]:
        bad2.append((it["scene"], word, in_pick, in_locker))
    marked[it["scene"]] = c["context"][: s - c0] + "[[" + text[s:e] + "]]" + c["context"][e - c0 :]
print(
    "2. inside the asked pick sentence, not the locker sentence, token == bridge:",
    len(items) - len(bad2),
    "of",
    len(items),
    "| failures:",
    bad2[:5],
)
before = sorted(it["scene"] for it in items if it["order"] == "before")
print(
    "   locker-before items where the bridge occurs twice in the context:",
    sum(x0_cases[s]["context"].count(x0_cases[s]["bridge"]) >= 2 for s in before),
    "of",
    len(before),
)
print("3. five random locker-before items (seed 0):")
for s in random.Random(0).sample(before, 5):
    print(f"   {s} | asked: {x0_cases[s]['readers'][X.LOOKUP]['question']} | {marked[s]}")
print(json.dumps({"fail_1": len(bad1), "fail_1_single": len(bad1s), "fail_2": len(bad2)}))
