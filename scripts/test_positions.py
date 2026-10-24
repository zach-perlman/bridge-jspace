"""CPU check of ablate_v2's --positions sets on real module 1 prompts (Zach, 2026-10-24)."""
import collections, os, sys
sys.path.insert(0, "/workspace/bridge-jspace/src"); sys.path.insert(0, "/workspace/bridge-jspace")
from bridge_jspace import tokens
from scripts import ablate_v2 as A
tok = tokens.load_tokenizer()
ps = A.tasks_prompts(tok, "jsuite_v1_facts_test_chat", "qwen35_9b_jsuite_v1_facts_test_chat_competence_cand2_v1",
                     ["PP", "PM", "MP", "MM", "TP", "TM"], 6, ["clean"], "all")
edited = collections.defaultdict(list)
for p in ps:
    n, q0 = len(p["ids"]), A.question_start(tok, p["ids"])
    bp = A.bridge_positions(tok, p["ids"], p["bridge"])
    for m in ("all", "context", "question", "final", "bridge"):
        out = set(A.outside_positions(m, n, q0, bp))
        ed = [i for i in range(n) if i not in out]
        edited[(p["family"][0], m)].append(len(ed))
        if m == "final": assert ed == [n - 1]
        if m == "bridge": assert ed == bp
        if m in ("context", "question"): assert (min(ed) >= q0) == (m == "question")
p = next(p for p in ps if p["family"].startswith("P"))
bp = A.bridge_positions(tok, p["ids"], p["bridge"])
print("example P-start bridge", repr(p["bridge"]), "mentions ->", [tok.decode([p["ids"][i]]) for i in bp])
print("last token:", repr(tok.decode([p["ids"][-1]])), "| question starts:", repr(tok.decode(p["ids"][A.question_start(tok, p["ids"]):][:8])))
for k in sorted(edited):
    v = edited[k]; print(f"start {k[0]} {k[1]:8s} edited positions per prompt: mean {sum(v)/len(v):6.1f}  min {min(v)}  max {max(v)}")
print("POSITIONS OK")
