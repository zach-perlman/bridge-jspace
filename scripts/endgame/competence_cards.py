"""Competence cards from stored competence runs (CPU only, read-only on the repo; no new runs).

Per model and word: whole accuracy, each hop alone, guess-prompt accuracy, chance 1/k (mean over items, k = len(answer_vocab)),
majority baselines, real-composition share (acc - guess) / (1 - guess), eligible n (tasks_v2.eligible's rule with the
knock-out runs' settings, replicated without its assert so weak models do not abort). All reads are the runs' own
'correct' field (cand2 read; hop 1 also needs the greedy generation to name the bridge, natural_v1.competence hop1='gen').
"""

from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

REPO = Path("/workspace/bridge-jspace")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import tasks_v2 as T  # noqa: E402

assert "torch" not in sys.modules
OUT = Path("/workspace/scratch/endgame")
COMP = REPO / "results" / "tasks_v2"
FACTS = ["PP", "PK", "PM", "PA", "PN", "MP", "MK", "MM", "MA", "MN", "TP", "TK", "TM", "TA", "TN"]
THREE = ["PPP", "MPP", "PMP", "PPM", "MPM", "MMP", "PMM", "MMM"]
NUMS = ["nPR", "nPL", "nPM", "nKR", "nKL", "nKM", "nAR", "nAL", "nAM", "nMR", "nML", "nMM"]
RWORDS = ["RM", "RA", "RN"]
# model key -> (label, set, {module: competence run}, R run (set, run) or None)
MODELS = {
    "q27": ("Qwen3.6 27B", "jsuite_v2_test_chat", {"facts": "jsuite_v2_test_chat_competence_cand2_v1", "threehop": "jsuite_v2_test_chat_competence_cand2_v1", "numbers": "jsuite_v2_test_chat_competence_cand2_v1"},
            ("jsuite_v2_1_test_chat", "jsuite_v2_1_test_chat_R_competence_cand2_v1")),
    "q9": ("Qwen3.5 9B", "jsuite_v2_test_chat", {m: "qwen35_9b_jsuite_v2_test_chat_competence_cand2_v1" for m in ("facts", "threehop", "numbers")},
           ("jsuite_v2_1_test_chat", "qwen35_9b_jsuite_v2_1_test_chat_R_competence_cand2_v1")),
    "nl": ("Nemotron 3.5 Lightning", "jsuite_v2_test_chat", {"facts": "nem35l_jsuite_v2_test_chat_competence_cand2_v1",
           "threehop": "nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1", "numbers": "nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1"},
           ("jsuite_v2_1_test_chat", "nem35l_jsuite_v2_1_test_chat_R_competence_cand2_v1")),
    "min14": ("Ministral 3 14B", "jsuite_v2_test_chat", {"facts": "min14_jsuite_v2_test_chat_competence_cand2_v1"},
              ("jsuite_v2_1_test_chat", "min14_jsuite_v2_1_test_chat_R_competence_cand2_v1")),
    "nem35b": ("Nemotron 3.5 Bolt", "jsuite_v2_test_chat", {"facts": "nem35b_jsuite_v2_test_chat_competence_cand2_v1"}, None),
    "dsv4f": ("DeepSeek V4 Flash", "jsuite_v2_test_chat", {"facts": "dsv4f_jsuite_v2_test_chat_competence_cand2_v1"}, None),
    "muse30": ("Muse Glimmer 30B", "jsuite_v2_test_chat", {m: "muse30_jsuite_v2_test_chat_competence_cand2_v1" for m in ("facts", "threehop", "numbers")},
               ("jsuite_v2_1_test_chat", "muse30_jsuite_v2_1_test_chat_R_competence_cand2_v1")),
    "olmo32": ("OLMo 3 32B (QA rendering)", "jsuite_v2_test_qa", {m: "olmo32_jsuite_v2_test_qa_competence_cand2_v1" for m in ("facts", "threehop", "numbers")}, None),
    "q122": ("Qwen3.5 122B-A10B", "jsuite_v2_test_chat", {m: "qwen35_122b_jsuite_v2_test_chat_competence_cand2_v1" for m in ("facts", "threehop", "numbers")},
             ("jsuite_v2_1_test_chat", "qwen35_122b_jsuite_v2_1_test_chat_R_competence_cand2_v1")),
}
STRONG = ("q27", "q9", "nl")
WORDS_OF = {"facts": FACTS, "threehop": THREE, "numbers": NUMS}
PER_WORD = {"facts": False, "threehop": True, "numbers": True}  # the knock-out manifests' tasks_per_word

_items: dict = {}


def items_of(set_name: str) -> dict:
    if set_name not in _items:
        _items[set_name] = {it["id"]: it for it in T.load(set_name)}
    return _items[set_name]


_rows: dict = {}


def rows_of(run: str) -> dict:
    """id -> part -> correct."""
    if run not in _rows:
        d: dict = collections.defaultdict(dict)
        for line in (COMP / run / "items.jsonl").read_text().splitlines():
            r = json.loads(line)
            d[r["id"]][r["part"]] = r["correct"]
        _rows[run] = d
    return _rows[run]


def eligible_ids(set_name: str, comp_run: str, words: list[str], per_word: bool) -> set:
    """tasks_v2.eligible(set, comp, words, n=1000, level='all', strata=('core',), per_word) without its final assert."""
    ok: dict = collections.defaultdict(list)
    for line in (COMP / comp_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["part"] != "guess":
            ok[r["id"]].append(r["correct"])
    its = [it for it in T.load(set_name) if it["word"] in words and T.stratum(it) in ("core",)
           and (len(it["word"]) == 2 or it["domain"] in T.THREE_STEP_DOMAINS or "framing" in it)]
    bridge_free = {it["scene"] for it in its if it.get("chance_same_answer", 0) >= 0.5}
    scene_ok: dict = collections.defaultdict(lambda: True)
    for it in its:
        scene_ok[it["scene"]] &= bool(ok.get(it["id"])) and all(ok[it["id"]]) and it["scene"] not in bridge_free
    out, got = set(), collections.Counter()
    for it in its:
        passes = (bool(ok.get(it["id"])) and all(ok[it["id"]]) and it.get("chance_same_answer", 0) < 0.5) if per_word else scene_ok[it["scene"]]
        if got[it["word"]] >= 1000 or not passes:
            continue
        got[it["word"]] += 1
        out.add(it["id"])
    return out


def group_key(it: dict) -> str:
    return it.get("relation") or it.get("domain")


def card(sel: list[dict], rows: dict, elig: set | None) -> dict:
    """sel: items. Fields as described in the module doc."""
    have = [it for it in sel if "whole" in rows.get(it["id"], {})]
    if not have:
        return {"n": 0}
    acc = lambda part: (statistics.mean(rows[it["id"]][part] for it in have if part in rows[it["id"]])  # noqa: E731
                        if any(part in rows[it["id"]] for it in have) else None)
    whole, guess = acc("whole"), acc("guess")
    c = {"n": len(have), "whole": whole, "guess": guess,
         "hops": {p: acc(p) for p in ("step1", "step2", "step3") if acc(p) is not None},
         "chance": statistics.mean(1 / len(it["answer_vocab"]) for it in have if it.get("answer_vocab")),
         "k": sorted({len(it["answer_vocab"]) for it in have if it.get("answer_vocab")})}
    # majority: (a) pooled over the word's items; (b) per relation (or domain), the most common answer's count summed
    cnt = collections.Counter(it["answer"] for it in have)
    c["majority_pooled"] = cnt.most_common(1)[0][1] / len(have)
    c["majority_answer"] = cnt.most_common(1)[0][0]
    byg = collections.defaultdict(collections.Counter)
    for it in have:
        byg[group_key(it)][it["answer"]] += 1
    c["majority_per_relation"] = sum(v.most_common(1)[0][1] for v in byg.values()) / len(have)
    c["real_comp"] = (whole - guess) / (1 - guess) if guess is not None and guess < 1 else None
    c["real_comp_ge_0.7"] = c["real_comp"] is not None and c["real_comp"] >= 0.7
    if elig is not None:
        c["eligible_n"] = sum(1 for it in have if it["id"] in elig)
    # shortcut diagnostic: items whose hop 1 alone is wrong, share right on the whole chain
    w1 = [it for it in have if rows[it["id"]].get("step1") is False]
    c["hop1_wrong_n"] = len(w1)
    c["hop1_wrong_whole_right"] = statistics.mean(rows[it["id"]]["whole"] for it in w1) if w1 else None
    return c


def to_chat(i: str) -> str:
    return i.replace(":qa:", ":chat:")


res: dict = {"models": {}, "R": {}, "common": {}, "notes": []}
elig_all: dict = {}
for m, (label, set_name, runs, rrun) in MODELS.items():
    its = items_of(set_name)
    out = {"label": label, "set": set_name, "runs": runs, "words": {}, "per_relation": {}}
    for mod, words in WORDS_OF.items():
        if mod not in runs:
            for w in words:
                out["words"][w] = {"n": 0, "missing": f"no {mod} competence run for this model"}
            continue
        run = runs[mod]
        rows = rows_of(run)
        elig = eligible_ids(set_name, run, words, PER_WORD[mod])
        elig_all[(m, mod)] = {to_chat(i) for i in elig}
        for w in words:
            out["words"][w] = card([it for it in its.values() if it["word"] == w], rows, elig)
        if mod == "facts":
            for w in ("PM", "MM", "TM"):
                rels = sorted({it["relation"] for it in its.values() if it["word"] == w})
                out["per_relation"][w] = {r: card([it for it in its.values() if it["word"] == w and it["relation"] == r], rows, elig)
                                          for r in rels}  # fmt: skip
    res["models"][m] = out
    if rrun:
        rs, rr = rrun
        rits = items_of(rs)
        rows = rows_of(rr)
        elig = eligible_ids(rs, rr, RWORDS, False)
        res["R"][m] = {"run": rr, "words": {w: card([it for it in rits.values() if it["word"] == w], rows, elig) for w in RWORDS},
                       "per_relation_RM": {r: card([it for it in rits.values() if it["word"] == "RM" and it["relation"] == r], rows, elig)
                                           for r in sorted({it["relation"] for it in rits.values() if it["word"] == "RM"})}}  # fmt: skip

# Lightning: the facts competence run vs the clean-checkout rerun (agreement, item by item)
a, b = rows_of("nem35l_jsuite_v2_test_chat_competence_cand2_v1"), rows_of("nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1")
pairs = [(a[i][p], b[i][p]) for i in a for p in a[i] if i in b and p in b[i]]
res["notes"].append(f"Lightning facts competence vs its clean-checkout rerun: {sum(x == y for x, y in pairs)} of {len(pairs)} prompt reads agree")

# common subset: items eligible (by the knock-out's rule) in all three strong models
for mod, words in WORDS_OF.items():
    common = set.intersection(*(elig_all[(m, mod)] for m in STRONG))
    res["common"][mod] = {"n_items": len(common), "per_model": {}}
    for m, (label, set_name, runs, rrun) in MODELS.items():
        if mod not in runs:
            continue
        its = items_of(set_name)
        rows = rows_of(runs[mod])
        res["common"][mod]["per_model"][m] = {w: card([it for it in its.values() if it["word"] == w and to_chat(it["id"]) in common], rows, None)
                                              for w in words}  # fmt: skip

(OUT / "competence_cards.json").write_text(json.dumps(res, indent=1, default=str))
print("wrote", OUT / "competence_cards.json")
print(res["notes"])
for mod in res["common"]:
    print(mod, "common n", res["common"][mod]["n_items"])

# verification: the replicated eligibility equals tasks_v2.eligible (where it does not assert) and the knock-out rows' items
chk = []
for m, run_ko, mod, comp in (("q27", "jsuite_v2_test_chat_ko_cand2_v1", "facts", "jsuite_v2_test_chat_competence_cand2_v1"),
                             ("q9", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "facts", "qwen35_9b_jsuite_v2_test_chat_competence_cand2_v1"),
                             ("nl", "nem35l_jsuite_v2_test_chat_ko_cand2_v1", "facts", "nem35l_jsuite_v2_test_chat_competence_cand2_v1"),
                             ("q27", "jsuite_v2_test_chat_threehop_ko_cand2_v1", "threehop", "jsuite_v2_test_chat_competence_cand2_v1"),
                             ("nl", "nem35l_jsuite_v2_test_chat_numbers_ko_cand2_dd_v1", "numbers", "nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1")):
    mine = eligible_ids("jsuite_v2_test_chat", comp, WORDS_OF[mod], PER_WORD[mod])
    theirs = {it["id"] for it in T.eligible("jsuite_v2_test_chat", comp, WORDS_OF[mod], 1000, "all", strata=("core",), per_word=PER_WORD[mod])}
    ko = {json.loads(x)["id"] for x in (REPO / "results/ablate_v2" / run_ko / "rows.jsonl").read_text().splitlines()}
    chk.append(f"{m} {mod}: replicated {len(mine)}, tasks_v2.eligible {len(theirs)}, equal {mine == theirs}; knock-out rows' items {len(ko)}, equal {ko == mine}")
res["notes"] += chk
print("\n".join(chk))
(OUT / "competence_cards.json").write_text(json.dumps(res, indent=1, default=str))
