"""x47_chain (batch 47, test 47.14, amendment 5; Dan 28 Oct ~03:10; jobs/c3/batch47.yaml, design and rule fixed in
advance; Q47.14 in predictions/2026-10-28_dan.md): do addresses chain? The second hop's key token.

As computed (fixed before any run; Dan may override before the run; the specs jobs/c3/x47_14_*.yaml repeat it):

Scenes (plan, CPU; x6_routes' pools, sentences, chat rendering). Three layers of sentences in this order, so every
address can form: three hall sentences ("Locker 5 is in hall B.", single-letter halls, one per locker number), then
the three locker sentences ("The locker of the frog is 5."), then the three pick sentences (the asked person picks the
bridge; two others pick the other two items); the orders of the hall sentences (hall slots 0-2), of the locker
sentences (locker slots 0-2) and of the picks are drawn independently. Digits distinct (1-9); hall letters distinct,
single tokens on the target's tokenizer (capitals without A, I and O: an article, a pronoun, zero's look-alike), and
the letter S introduces is not in O. O is the scene; S differs only in the
hall layer, routes-style (x6_routes' C1 at the hall level): the hall sentence naming the bridge's locker number moves
from hall slot i to hall slot j (swapped with the sentence there) and its letter becomes the new letter. Questions:
P->P "Which locker belongs to <person>'s pick?" (a digit, X0's read: the top token after a space token appended to
"Answer:") and P->P->P "Which hall is the locker of <person>'s pick in?" (a letter, read as X0's word answers: the
token " B" right after "Answer:"; the instruction "Answer with a single letter and nothing else."). O's answers: the
bridge's digit and its hall letter; S's: the same digit (the locker question cannot switch) and the new letter.

The key token: the digit token of the bridge's locker sentence (one token, the same index in O and S; both readers'
prompts identical through it; else the scene is dropped and counted). Every read is at that token at the layer fixed
in advance (X.PREDICTED), on O. The hall question's answer is classified identity = the hall of the same number (O's
letter; identity = original, as in C1), position = the letter at hall slot j in O, value = the new letter, other.

Run (GPU, SEALED: per-item outputs only). Competence as X0 (8 greedy tokens and the read, unedited O and S, both
readers; the hall question's greedy answer is the first standalone capital letter of its first line); gate: O's read
accuracy >= 0.80 per reader over the candidates (the test names the three-step question's gate; the locker question's
is the common per-reader gate); a model that misses it is "not tested". Eligible: both readers say and read O's and
S's answers right; the first 300 in generation order. Split by bridge entity (seed 4715: the entities shuffled, each
added to the half with fewer scenes), so U_num's fit never sees a test scene's entity: the fit half and the test half.
U_num (fit half, before any arm): O's and S's states at the key token, labelled by the hall slot of the bridge
number's hall sentence in that prompt (i in O, j in S); x0_massmean's layout-free method with the layout group = the
locker slot the key token sits in (what the token can see without binding; the three hall sentences always precede
it); mu_k = hall slot k's mean; U_num = x0_massmean.mass_mean (orthonormal, rank 2). Arms (test half, on O, at the key
token, both readers): none; whole (Delta = h_S - h_O); without U_num (Delta - U U^T Delta) and without a random part
of the same share (X0's random subspace, seed 888 + L); only U_num (U U^T Delta) and only a random part of its share;
without J++ (the layer's J++ lens over the letter tokens and the ten digit tokens, signed OMP k = 25) and without a
random part of its share. The slot probe (verdict, CPU, from states.npz): x0_probe (b) on O's key-token states of
every chosen scene, target = the hall slot, 5 folds by bridge entity, beside chance (1/3), the training folds'
majority and the layout baseline (the training folds' most frequent hall slot given the locker slot).

Verdict (CPU; refuses until Q47.14's "Dan:" line is committed). Shares with cluster-bootstrap CIs over bridge items
(10,000 resamples, seed 0); point estimates decide, EPS 1e-9 at the bars. Per model, "addresses chain" if the slot
probe >= 0.80 and its layout baseline <= 0.6; the hall question's position share without U_num is >= 0.30 below the
share without the random part; only U_num gives position >= 0.15; and the locker question's kept share (top token =
O's digit) under every arm is within 0.05 of its unedited share. The batch answer needs both models. Reported beside:
the hall question's value share (expected 0) under every arm; whether J++ at the key token matters (the position
share without J++ falls >= 0.30 below the share without its random part: the same bar, expected not).

uv run python scripts/x47_chain.py plan                                                    # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_chain.py run --name qwen35_9b_x47_14       # GPU (sealed)
uv run python scripts/x47_chain.py verdict --runs qwen35_9b_x47_14 muse30_x47_14           # CPU, after Dan's Q47.14
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import string
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_massmean as MM
from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x6_routes as R
from scripts import x47_six as Q

EXP = "x47_chain"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml (47.14)"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.14"
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_14", "muse-glimmer-30b": "muse30_x47_14"}
SEED, SPLIT_SEED = 4714, 4715
N_GEN, N_ITEMS = 500, 300
HALL = "PPP"  # the three-step reader's key (X.LOOKUP = "PP" is the locker question)
READERS = (X.LOOKUP, HALL)
READER_NAME = {X.LOOKUP: "locker", HALL: "hall"}
HALL_Q = "Which hall is the locker of {p}'s pick in?"
HALL_INSTRUCTION = "Answer with a single letter and nothing else."
ROUTES = ("identity", "position", "value", "other")
ARMS = ("none", "whole", "no_U", "no_U_rand", "keep_U", "keep_U_rand", "no_jpp", "no_jpp_rand")
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change h_S - h_O at the key token (the bridge's locker digit)",
    "no_U": "the whole change without its part in U_num (the hall-slot means refit at the key token)",
    "no_U_rand": "the whole change without a random part of U_num's share",
    "keep_U": "only the U_num part of the change",
    "keep_U_rand": "only a random part of U_num's share",
    "no_jpp": "the whole change without its J++ part (k = 25, signed; letter and digit atoms)",
    "no_jpp_rand": "the whole change without a random part of J++'s share",
}
PROBE_MIN, LAYOUT_MAX, CUT_MIN, KEEP_MIN, LOCKER_TOL = 0.80, 0.6, 0.30, 0.15, 0.05
EPS = 1e-9  # a value at a bar counts as at the bar
N_SLOTS = 3
EXCLUDED_LETTERS = frozenset("AIO")
LETTER_RE = re.compile(r"(?<![A-Za-z])([A-Z])(?![A-Za-z])")
HALL_SENT = re.compile(r"Locker (\d) is in hall ([A-Z])\.")
LOCKER_SENT = re.compile(r"The locker of the (\w+) is (\d)\.")


# ---- scenes (text) -------------------------------------------------------------------------------------------------


def hall_sentence(digit: int, letter: str) -> str:
    return f"Locker {digit} is in hall {letter}."


def context(halls: list[tuple[int, str]], lockers: list[tuple[str, int]], picks: list[tuple[str, str]]) -> str:
    """The hall layer, then x6_routes' locker and pick layers."""
    return " ".join([hall_sentence(d, h) for d, h in halls] + [R.context(lockers, picks)])


def letters(tok) -> list[str]:
    """The hall letters: the capital letters that are one token both after a space (" B", the read) and bare ("B"),
    without A, I and O (an article, a pronoun and the digit zero's look-alike; the agent's choice, before any run)."""
    from scripts import suite_v1 as S

    return [c for c in string.ascii_uppercase if c not in EXCLUDED_LETTERS
            and len(S.ids(tok, " " + c)) == 1 and len(S.ids(tok, c)) == 1]  # fmt: skip


def scene_text(rng: random.Random, animals: list[str], people: list[str], halls: list[str]) -> dict:
    """One scene: O and its S (the bridge number's hall sentence moved to another hall slot with a new letter)."""
    a_item, b_item, c_item = rng.sample(animals, 3)
    digits = dict(zip((a_item, b_item, c_item), rng.sample(range(1, 10), 3), strict=True))
    h_a, h_b, h_c, new = rng.sample(halls, 4)
    letter = {digits[a_item]: h_a, digits[b_item]: h_b, digits[c_item]: h_c}
    asked, p1, p2 = rng.sample(people, 3)
    hall_order = rng.sample(list(letter), N_SLOTS)  # the digits in hall-slot order
    locker_order = rng.sample([a_item, b_item, c_item], N_SLOTS)
    picks = rng.sample([(asked, a_item), (p1, b_item), (p2, c_item)], 3)
    a = digits[a_item]
    i = hall_order.index(a)
    j = rng.choice([s for s in range(N_SLOTS) if s != i])
    o_halls = [(d, letter[d]) for d in hall_order]
    s_halls = list(o_halls)
    s_halls[i], s_halls[j] = o_halls[j], (a, new)
    lockers = [(x, digits[x]) for x in locker_order]
    return {"bridge": a_item, "asked": asked, "digit": a, "items": [a_item, b_item, c_item], "picks": picks,
            "hall_slot": i, "target_slot": j, "locker_slot": locker_order.index(a_item), "new": new,
            "halls_o": o_halls, "halls_s": s_halls, "o": context(o_halls, lockers, picks),
            "s": context(s_halls, lockers, picks),
            "expect": {"identity": h_a, "position": o_halls[j][1], "value": new, "original": h_a}}  # fmt: skip


def text_checks(t: dict) -> list[str]:
    """What must hold for a scene's texts ([] if all hold): three hall and three locker sentences with distinct digits
    and letters, the new letter not in O, every digit's hall sentence before every locker sentence, O and S differing
    in exactly the two swapped hall sentences, the routes' letters distinct, no item named in the questions."""
    bad = []
    o, s = t["o"], t["s"]
    ho, hs, lo = HALL_SENT.findall(o), HALL_SENT.findall(s), LOCKER_SENT.findall(o)
    if len(ho) != N_SLOTS or len(lo) != N_SLOTS or len({d for d, _ in ho}) != N_SLOTS or len({h for _, h in ho}) != 3:
        bad.append("not three hall sentences with distinct digits and letters")
    if {d for d, _ in ho} != {d for _, d in lo}:
        bad.append("the hall sentences' digits are not the lockers' digits")
    if re.search(rf"(?<![A-Za-z]){t['new']}(?![A-Za-z])", o):
        bad.append("the new letter is in O")
    if max(m.start() for m in HALL_SENT.finditer(o)) > min(m.start() for m in LOCKER_SENT.finditer(o)):
        bad.append("a hall sentence comes after a locker sentence")
    so, ss = Q.sentences(o), Q.sentences(s)
    diff = [k for k, (x, y) in enumerate(zip(so, ss, strict=True)) if x != y]
    if diff != sorted({t["hall_slot"], t["target_slot"]}):
        bad.append(f"O and S differ in sentences {diff}, not the two swapped hall slots")
    if len({t["expect"]["identity"], t["expect"]["position"], t["expect"]["value"]}) != 3:
        bad.append("the routes' letters are not distinct")
    if hs[t["target_slot"]] != (str(t["digit"]), t["new"]):
        bad.append("S does not put the bridge number's sentence at the target slot with the new letter")
    for q in (R.LOOKUP_Q, HALL_Q):
        if any(re.search(rf"\b{re.escape(x)}\b", q.format(p=t["asked"])) for x in t["items"]):
            bad.append("the question names an item")
    return bad


# ---- scenes (tokenizer) --------------------------------------------------------------------------------------------


def render(tok, ctx: str, question: str, kind: str) -> str:
    """The prompt as the run renders it: tasks_v2's chat prompt (the digit instruction) for the locker question; the
    same chat turn with the letter instruction for the hall question."""
    from bridge_jspace import chat

    if kind == "digit":
        return X.render(tok, {"format": "prose", "kind": "digit", "context": ctx, "question": question}, "chat", ctx)
    return chat.chat_text(tok, f"{ctx}\n{question} {HALL_INSTRUCTION}")


def said_letter(text: str) -> str | None:
    """The hall question's greedy answer: the first standalone capital letter of the first non-empty line."""
    line = next((ln for ln in text.split("\n") if ln.strip()), "")
    m = LETTER_RE.search(line)
    return m.group(1) if m else None


def encode(tok, t: dict, scene: str) -> tuple[dict | None, str]:
    """Both readers' O and S prompts with the key token (the bridge's locker digit) one token at one index shared by
    O and S and by the readers; the answer tokens per reader; the routes' letter tokens."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    bad = text_checks(t)
    assert not bad, f"{scene}: {bad}"
    sent = f"The locker of the {t['bridge']} is {t['digit']}."
    readers, pos = {}, None
    specs = ((X.LOOKUP, R.LOOKUP_Q, "digit", (str(t["digit"]), str(t["digit"]))),
             (HALL, HALL_Q, "letter", (t["expect"]["original"], t["expect"]["value"])))  # fmt: skip
    for w, q, kind, (org_ans, alt_ans) in specs:
        ids, at = {}, {}
        for v, ctx in (("org", t["o"]), ("alt", t["s"])):
            text = render(tok, ctx, q.format(p=t["asked"]), kind)
            if text.count(ctx) != 1 or ctx.count(sent) != 1:
                return None, "the context or the bridge's locker sentence is not once in the prompt"
            enc = raw_encoding(tok, text, offsets=True)
            w0 = text.index(ctx) + ctx.index(sent) + sent.rindex(str(t["digit"]))
            ids[v], at[v] = list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + 1)
        if len(ids["org"]) != len(ids["alt"]) or len(at["org"]) != 1 or at["org"] != at["alt"]:
            return None, "the key token is not one token at the same index in O and S"
        if pos is not None and at["org"][0] != pos:
            return None, "the readers' key positions differ"
        pos = at["org"][0]
        if ids["org"][pos] != ids["alt"][pos]:
            return None, "the key token differs between O and S"
        readers[w] = {"question": q.format(p=t["asked"]), "kind": kind, "answer": org_ans, "cf_answer": alt_ans,
                      "ids": ids, "tok_A": S.answer_token(tok, org_ans, kind), "tok_b": S.answer_token(tok, alt_ans, kind),
                      "space": S.ids(tok, " ") if kind == "digit" else []}  # fmt: skip
    assert pos is not None
    for v in ("org", "alt"):
        if readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[HALL]["ids"][v][: pos + 1]:
            return None, "the readers' prompts differ before the key token"
    routes = {k: S.answer_token(tok, v, "letter") for k, v in t["expect"].items()}
    if len({routes[k] for k in ("identity", "position", "value")}) != 3:
        return None, "two routes' letters share a token"
    return {"scene": scene, "condition": "H", "rendering": "chat", "domain": "animals", "bridge": t["bridge"],
            "cf_bridge": t["bridge"], "context": t["o"], "cf_context": t["s"], "pos": pos, "digit": t["digit"],
            "asked": t["asked"], "items": t["items"], "hall_slot": t["hall_slot"], "target_slot": t["target_slot"],
            "locker_slot": t["locker_slot"], "new": t["new"], "halls_o": t["halls_o"], "halls_s": t["halls_s"],
            "expect": t["expect"], "route_tokens": routes, "readers": readers}, ""  # fmt: skip


def build_cases(tok, n: int = N_GEN) -> tuple[list[dict], collections.Counter]:
    """n encodable scenes (seed SEED); drops counted by reason."""
    _, animals, people = R.pools(tok)
    halls = letters(tok)
    assert len(halls) >= 4, f"{len(halls)} one-token capital letters"
    rng = random.Random(SEED)
    out, dropped = [], collections.Counter()
    tries = 0
    while len(out) < n:
        tries += 1
        assert tries <= 50 * n, f"cannot fill {n} scenes ({dropped})"
        case, why = encode(tok, scene_text(rng, animals, people, halls), f"H-{tries:04d}")
        if case is None:
            dropped[why] += 1
            continue
        out.append(case)
    return out, dropped


def prompt_as_read(decode, rd: dict, pos: int, variant: str = "org") -> str:
    """A reader's prompt exactly as the model reads it (the read's space token appended for the digit question), the
    key token in ⟦...⟧."""
    return Q.marked(decode, rd["ids"][variant], pos, rd["space"])


def stage_plan(n: int = N_GEN, k_prompts: int = 5) -> dict:
    """Tokenizer only: the cases, drops, token checks, hall letters, slot and layout counts, and k rendered prompts
    (both readers' O as read, the key token marked; S beside)."""
    from scripts import x45m

    tok = x45m.tokenizer()
    cases, dropped = build_cases(tok, n)
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    for c in cases:
        ids = c["readers"][X.LOOKUP]["ids"]
        assert tok.decode([ids["org"][c["pos"]]]).strip() == str(c["digit"]), f"{c['scene']}: the key token"
    lengths = collections.Counter(len(c["readers"][X.LOOKUP]["ids"]["org"]) for c in cases)
    blob = {
        "target": pins.TARGET, "layer": X.PREDICTED.get(pins.TARGET), "prefix": pins.RUN_PREFIX, "cases": len(cases),
        "dropped": dict(dropped), "hall_letters": letters(tok), "entities": len({c["bridge"] for c in cases}),
        "key_token_index": sorted({c["pos"] for c in cases}), "prompt_tokens": [min(lengths), max(lengths)],
        "moves": dict(collections.Counter(f"{c['hall_slot']}->{c['target_slot']}" for c in cases)),
        "locker_slots": dict(collections.Counter(c["locker_slot"] for c in cases)),
        "hall_by_locker_slot": {f"locker {ls}": dict(collections.Counter(c["hall_slot"] for c in cases if c["locker_slot"] == ls))
                                for ls in range(N_SLOTS)},
        "prompts": [{"scene": c["scene"], "O": c["context"], "S": c["cf_context"], "expect": c["expect"],
                     **{f"{READER_NAME[w]}_O_as_read": prompt_as_read(decode, c["readers"][w], c["pos"])
                        for w in READERS},
                     "hall_S_as_read": prompt_as_read(decode, c["readers"][HALL], c["pos"], "alt")}
                    for c in cases[:k_prompts]],
    }  # fmt: skip
    print(json.dumps(blob, indent=1, ensure_ascii=False))
    write_plan(
        blob, [(p["scene"], f"{k}: {v}") for p in blob["prompts"] for k, v in p.items() if k.endswith("as_read")]
    )
    return blob


def write_plan(blob: dict, prompts: list[tuple[str, str]]) -> Path:
    """The plan's counts (plan.json) and its rendered prompts (prompts.md) in a new results/<exp>/plan-<time>/ folder
    (the competence report and the 5 rendered prompts the verify pack needs before an enqueue)."""
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "plan.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [
        f"# {EXP} plan on {blob['target']} (tokenizer only): {len(prompts)} rendered prompts, ⟦…⟧ the patched token",
        "",
    ]
    for scene, text in prompts:
        lines += [f"## {scene}", "", "```", text, "```", ""]
    (out / "prompts.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- the run (GPU) -------------------------------------------------------------------------------------------------


def competence(model, cases: list[dict], ws) -> list[dict]:
    """X0's competence with each reader's own answer kind: 8 greedy tokens and the read on the unedited O and S."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (case)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device=model.device)
                texts = model.generate_batch(ids, X.GEN_TOKENS, [{}, {}])
                for i, (v, gold, tok_gold) in enumerate(
                    (("org", rd["answer"], rd["tok_A"]), ("alt", rd["cf_answer"], rd["tok_b"]))
                ):
                    logits, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", rd["space"], ws)
                    said = S.said(texts[i], "digit") if rd["kind"] == "digit" else said_letter(texts[i])
                    rows.append({"scene": c["scene"], "reader": w, "variant": v, "greedy": texts[i], "said": said,
                                 "right": said == gold, "read_right": int(logits[0].argmax()) == tok_gold})  # fmt: skip
    return rows


def gate_of(cases: list[dict], comp: list[dict], gate_min: float | None = None) -> tuple[dict, list[dict]]:
    """O's read accuracy per reader over every case (the gate: >= gate_min for both) and the eligible cases in
    generation order (both readers say and read O's and S's answers right)."""
    gate_min = X.GATE if gate_min is None else gate_min
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in READERS}
    said = {w: float(np.mean([right[(c["scene"], w, "org")]["right"] for c in cases])) for w in READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in READERS for v in ("org", "alt"))]  # fmt: skip
    return {"cases": len(cases), "org_read_accuracy": acc, "org_said_accuracy": said, "gate": gate_min,
            "pass": bool(cases) and all(a >= gate_min - EPS for a in acc.values()), "eligible": len(ok)}, ok  # fmt: skip


def split_by_entity(chosen: list[dict], seed: int = SPLIT_SEED) -> tuple[list[dict], list[dict]]:
    """The fit and test halves: the bridge entities shuffled (seed), each added to the half with fewer scenes."""
    ents = sorted({c["bridge"] for c in chosen})
    random.Random(seed).shuffle(ents)
    halves: list[set[str]] = [set(), set()]
    count = [0, 0]
    per = collections.Counter(c["bridge"] for c in chosen)
    for e in ents:
        k = 0 if count[0] <= count[1] else 1
        halves[k].add(e)
        count[k] += per[e]
    return [c for c in chosen if c["bridge"] in halves[0]], [c for c in chosen if c["bridge"] in halves[1]]


def fit_u(h: np.ndarray, slots: list[int], groups: list[str]) -> dict:
    """The hall-slot means mu_0..mu_2 ([3, d]) of the layout-free states (each minus its layout group's mean; groups of
    one dropped) and U_num = x0_massmean.mass_mean (orthonormal, rank 2)."""
    res, keep = Q.layout_free(h, groups)
    lab = [int(slots[r]) for r in keep]
    assert set(lab) == set(range(N_SLOTS)), f"hall slots {sorted(set(lab))}, not 0..{N_SLOTS - 1}"
    mu = np.stack([res[[k for k, s in enumerate(lab) if s == slot]].mean(0) for slot in range(N_SLOTS)])
    return {"mu": mu, "U": MM.mass_mean(res, lab), "states": len(keep), "dropped_singletons": len(h) - len(keep),
            "per_slot": {str(k): lab.count(k) for k in range(N_SLOTS)},
            "groups": dict(collections.Counter(groups[r] for r in keep))}  # fmt: skip


def jpp_dictionary(model, layer: int):
    """The layer's J++ lens over the letter tokens and the ten digit tokens (digit atoms allowed, 47.14)."""
    import torch

    from bridge_jspace.lens import JLens

    letters_ = model.letter_token_ids()
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=letters_.device)
    ids = torch.unique(torch.cat([letters_, digits]))
    return JLens(model, "jpp").vectors(layer, ids)


def key_states(model, c: dict, layer: int) -> dict:
    """O's and S's states [d] at the key token at the layer (the locker question's prompts; the hall question's are
    the same through the key token)."""
    import torch

    ids = c["readers"][X.LOOKUP]["ids"]
    return {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][c["pos"]].float()
            for v in ("org", "alt")}  # fmt: skip


def read_record(c: dict, w: str, arm: str, lg, rd: dict, tok) -> dict:
    import torch

    top = int(lg.argmax())
    p = torch.softmax(lg.float(), -1)
    rec = {"scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": arm, "top": top,
           "top_text": tok.decode([top]), "kept": int(top == rd["tok_A"]), "switched": int(top == rd["tok_b"]),
           "role": "b" if top == rd["tok_b"] else "A" if top == rd["tok_A"] else "other",
           "p_org": round(float(p[rd["tok_A"]]), 4), "p_alt": round(float(p[rd["tok_b"]]), 4),
           "ld": round(float(lg[rd["tok_b"]] - lg[rd["tok_A"]]), 3)}  # fmt: skip
    if w == HALL:
        rec["route"] = R.classify(top, c)
    return rec


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    manifest = out / "manifest.json"  # rewritten as the run goes: gate, items, fit (never a result)
    m: dict = {"exp": EXP, "run": name, "why": why, "test": "47.14", "spec": SPEC,
               "question": f"{QUESTION} ({PREDICTIONS})",
               "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
               "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer,
               "read": {"locker": "X0's chat read (the top token after a digit's space token appended to 'Answer:')",
                        "hall": "the top token right after 'Answer:' (X0's word read; the answer token ' B')"},
               "hall_instruction": HALL_INSTRUCTION, "gate": X.GATE, "n": {"candidates": N_GEN, "items": N_ITEMS},
               "seeds": {"scenes": SEED, "split": SPLIT_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)",
                         "bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED},
               "arms": ARM_TEXT, "k": X.K_MAIN, "omp": "signed", "jpp_atoms": "the layer's J++ lens over the letter tokens and the ten digit tokens",
               "key_token": "the digit token of the bridge's locker sentence (one token, the same index in O and S)",
               "U_num": "x0_massmean's layout-free hall-slot class means at the key token, fit on the fit half (O and S "
                        "states, labelled by the hall slot of the bridge number's sentence; layout group = the locker "
                        "slot); rank 2",
               "split": "by bridge entity (seed 4715), the test half's entities unseen by the fit",
               "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    ws = X.whitespace_mask(model)
    cases, dropped = build_cases(tok)
    comp = competence(model, cases, ws)
    gate, ok = gate_of(cases, comp)
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", cases)
    (out / "gate.json").write_text(json.dumps({"dropped": dict(dropped), **gate}, indent=2) + "\n")
    m["gate_result"] = {k: v for k, v in gate.items()}
    if not gate["pass"]:
        m["tested"] = False
        manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        print("not tested: the gate missed; see gate.json", flush=True)
        return out
    chosen = ok[:N_ITEMS]
    fit_c, test_c = split_by_entity(chosen)
    (out / "split.json").write_text(json.dumps({"seed": SPLIT_SEED, "fit": [c["scene"] for c in fit_c],
                                                "test": [c["scene"] for c in test_c]}, indent=1) + "\n")  # fmt: skip
    m.update({"tested": True, "items": {"chosen": len(chosen), "fit": len(fit_c), "test": len(test_c),
                                        "entities": {"fit": len({c["bridge"] for c in fit_c}),
                                                     "test": len({c["bridge"] for c in test_c})}}})  # fmt: skip
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    rows: list[dict] = []
    with torch.no_grad():
        states = {c["scene"]: key_states(model, c, layer) for c in progress(chosen, f"states at L{layer} (case)")}
        h_all = np.stack([states[c["scene"]]["org"].cpu().numpy() for c in chosen])
        fit_scenes = {c["scene"] for c in fit_c}
        half = ["fit" if c["scene"] in fit_scenes else "test" for c in chosen]
        np.savez_compressed(out / "states.npz", h=h_all.astype(np.float32), scene=np.array([c["scene"] for c in chosen]),
                            entity=np.array([c["bridge"] for c in chosen]),
                            hall_slot=np.array([c["hall_slot"] for c in chosen]),
                            locker_slot=np.array([c["locker_slot"] for c in chosen]), half=np.array(half))  # fmt: skip
        hs, labels, groups = [], [], []
        for c in fit_c:
            for v, slot in (("org", c["hall_slot"]), ("alt", c["target_slot"])):
                hs.append(states[c["scene"]][v].cpu().numpy())
                labels.append(slot)
                groups.append(str(c["locker_slot"]))
        fit = fit_u(np.stack(hs), labels, groups)
        np.savez(out / "fit.npz", mu=fit["mu"].astype(np.float32), U=fit["U"].astype(np.float32),
                 slot=np.array(labels), group=np.array(groups),
                 scene=np.array([c["scene"] for c in fit_c for _ in (0, 1)]), prompt=np.array(["O", "S"] * len(fit_c)))  # fmt: skip
        m["fit"] = {k: fit[k] for k in ("states", "dropped_singletons", "per_slot", "groups")}
        m["fit"]["U_rank"] = int(fit["U"].shape[1])
        manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        u = torch.tensor(fit["U"], dtype=torch.float32, device=dev)
        jdic = jpp_dictionary(model, layer)
        m["jpp_atom_count"] = int(jdic.shape[0])
        x = torch.stack([states[c["scene"]]["alt"] - states[c["scene"]]["org"] for c in test_c]).to(dev)
        u_part = (x @ u) @ u.T
        jpp = X.fit(jdic, x.to(jdic.device), X.K_MAIN, "signed").float().to(dev)
        share = {
            k: v.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30) for k, v in (("U", u_part), ("jpp", jpp))
        }
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        u_rand, j_rand = SP.random_subspace_part(x, share["U"], basis), SP.random_subspace_part(x, share["jpp"], basis)
        arms = {"whole": x, "no_U": x - u_part, "no_U_rand": x - u_rand, "keep_U": u_part, "keep_U_rand": u_rand,
                "no_jpp": x - jpp, "no_jpp_rand": x - j_rand}  # fmt: skip
        assert ("none", *arms) == ARMS
        norms = []
        for k, c in enumerate(progress(test_c, f"arms at L{layer} (case)")):
            edits = [{}] + [{layer: AddRows(arms[a][k : k + 1], [c["pos"]])} for a in arms]
            for w, rd in c["readers"].items():
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["space"], ws)
                rows += [read_record(c, w, a, lg, rd, tok) for a, lg in zip(ARMS, logits, strict=True)]
            norms.append({"scene": c["scene"], "norm": round(float(x[k].norm()), 4),
                          "share_U": round(float(share["U"][k]), 5), "share_jpp": round(float(share["jpp"][k]), 5)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    manifest.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- the verdict (CPU) ---------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q47.14 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def probe_cells(src: Path, n_boot: int) -> dict:
    """x0_probe (b) at the key token on O's states of every chosen scene: target = the hall slot, 5 folds by bridge
    entity; chance, the majority and the layout baseline (the most frequent hall slot given the locker slot)."""
    z = np.load(src / "states.npz")
    items = [{"entity": str(e), "locker_index": int(hs), "pick_index": int(ls), "layout": f"locker{int(ls)}"}
             for e, hs, ls in zip(z["entity"], z["hall_slot"], z["locker_slot"], strict=True)]  # fmt: skip
    return P.score(z["h"].astype(np.float64), items, "locker sentence", n_boot)


def hall_cells(rows: list[dict], n_boot: int) -> dict:
    """The hall question (test half): each route's share per arm, with paired cluster-bootstrap CIs; U_num's cut of
    position beyond random (pos without random - pos without U_num), only-U_num's position (its random part beside),
    J++'s cut beyond random, and the value share per arm."""
    at = {(r["scene"], r["arm"]): r for r in rows if r["reader"] == HALL}
    scenes = sorted({s for s, a in at if a == "whole"})
    ent = [at[(s, "whole")]["entity"] for s in scenes]
    sw = {f"{rt}|{a}": [int(at[(s, a)]["route"] == rt) for s in scenes] for a in ARMS for rt in ROUTES}
    sw.update({f"switched|{a}": [at[(s, a)]["switched"] for s in scenes] for a in ARMS})
    pt, rr = Q.shares(sw, ent, n_boot)
    return {"n": len(scenes), "entities": len(set(ent)),
            "routes": {a: {rt: pt[f"{rt}|{a}"] for rt in ROUTES} for a in ARMS},
            "switched": {a: pt[f"switched|{a}"] for a in ARMS},
            "U_cut_beyond_random": Q.paired(rr, pt, "position|no_U_rand", "position|no_U"),
            "keep_U_position": pt["position|keep_U"], "keep_U_rand_position": pt["position|keep_U_rand"],
            "keep_minus_rand": Q.paired(rr, pt, "position|keep_U", "position|keep_U_rand"),
            "jpp_cut_beyond_random": Q.paired(rr, pt, "position|no_jpp_rand", "position|no_jpp"),
            "value_count": {a: int(sum(sw[f"value|{a}"])) for a in ARMS}}  # fmt: skip


def locker_cells(rows: list[dict], n_boot: int) -> dict:
    """The locker question (test half): the kept share (top token = O's digit) per arm and its drift from unedited."""
    at = {(r["scene"], r["arm"]): r for r in rows if r["reader"] == X.LOOKUP}
    scenes = sorted({s for s, a in at if a == "whole"})
    ent = [at[(s, "whole")]["entity"] for s in scenes]
    sw = {a: [at[(s, a)]["kept"] for s in scenes] for a in ARMS}
    pt, rr = Q.shares(sw, ent, n_boot)
    drift = {a: Q.paired(rr, pt, a, "none") for a in ARMS if a != "none"}
    return {"n": len(scenes), "kept": pt, "drift": drift,
            "max_abs_drift": max(abs(v[0]) for v in drift.values()) if drift else 0.0}  # fmt: skip


def rule(probe: dict, hall: dict, locker: dict) -> dict:
    """47.14's clauses on one model (point estimates; EPS at the bars). See the module docstring."""
    clauses = {
        "probe": bool(probe["probe"][0] >= PROBE_MIN - EPS),
        "layout": bool(probe["layout"][0] <= LAYOUT_MAX + EPS),
        "U_cut": bool(hall["U_cut_beyond_random"][0] >= CUT_MIN - EPS),
        "keep_U": bool(hall["keep_U_position"][0] >= KEEP_MIN - EPS),
        "locker_within": bool(locker["max_abs_drift"] <= LOCKER_TOL + EPS),
    }
    value = hall["value_count"]["whole"]
    return {"clauses": clauses, "holds": all(clauses.values()),
            "value_ever": {"whole": value, "any_arm": int(sum(hall["value_count"].values()))},
            "jpp_matters": bool(hall["jpp_cut_beyond_random"][0] >= CUT_MIN - EPS),
            "why": "; ".join(f"{k}: {'yes' if v else 'no'}" for k, v in clauses.items())}  # fmt: skip


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.14 run {run!r} here, and it is not one of the specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False, "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else None
    base = {"run": run, "target": m["model"]["target"], "layer": m["layer"], "gate": gate}
    if m.get("tested") is False:
        return {**base, "status": "not tested", "holds": False, "why": "the gate missed (see gate.json)"}
    if not (src / "outcomes.jsonl").exists():
        return {**base, "status": "pending", "holds": False, "why": "no outcomes here (the run did not finish)"}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    probe, hall, locker = probe_cells(src, n_boot), hall_cells(rows, n_boot), locker_cells(rows, n_boot)
    r = rule(probe, hall, locker)
    norms = X.read_jsonl(src / "norms.jsonl")
    share = {k: float(np.median([x[f"share_{k}"] for x in norms])) for k in ("U", "jpp")}
    return {**base, "status": "tested", **r, "probe": probe, "hall": hall, "locker": locker, "fit": m.get("fit"),
            "items": m.get("items"), "median_share": share}  # fmt: skip


def ci(v: list) -> str:
    return Q.ci(v)


def report_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    tested = [m for m in models if m["status"] == "tested"]
    n_hold = sum(m["holds"] for m in models)
    pending = [m for m in models if m["status"] == "pending"]
    batch = ("addresses chain" if n_hold == len(RUNS) else "pending" if pending and n_hold + len(pending) >= len(RUNS)
             else "does not hold on both models")  # fmt: skip
    lines = ["# 47.14: do addresses chain? The second hop's key token", "",
             f"Batch 47, test 47.14 ({SPEC}; {QUESTION}, Dan: {answer}). Hall sentences, then locker sentences, then "
             "picks; every edit at the digit token of the bridge's locker sentence at the layer fixed in advance, read "
             f"on O; the test half; cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"**Verdict: {batch}** ({n_hold} of {len(RUNS)} models hold; the rule needs both).", "",
             "| model | run | status | n (test) | slot probe at the key token | layout baseline | hall: U_num's cut "
             "beyond random | only U_num: position | locker: max |drift| | holds | value (whole / any arm) | J++ matters |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | | | | | no | | |")
            continue
        p, h, lk = m["probe"], m["hall"], m["locker"]
        lines.append(f"| {m['target']} | {m['run']} | tested | {h['n']} | {ci(p['probe'])} | {ci(p['layout'])} | "
                     f"{ci(h['U_cut_beyond_random'])} | {ci(h['keep_U_position'])} | {lk['max_abs_drift']:.3f} | "
                     f"**{'yes' if m['holds'] else 'no'}** ({m['why']}) | {m['value_ever']['whole']} / "
                     f"{m['value_ever']['any_arm']} | {'yes' if m['jpp_matters'] else 'no'} "
                     f"({ci(h['jpp_cut_beyond_random'])}) |")  # fmt: skip
    lines += ["", f"Rule (fixed in advance): probe >= {PROBE_MIN} with the layout baseline <= {LAYOUT_MAX}; without "
              f"U_num the hall question's position share falls >= {CUT_MIN} below the share without its random part; "
              f"only U_num gives position >= {KEEP_MIN}; the locker question's kept share within {LOCKER_TOL} of "
              "unedited under every arm; on both models.", "",
              "## The hall question: route shares per arm (test half)", "",
              "| model | arm | identity (= original) | position | value | other | switched (= value) |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for a in ARMS:
            rt = m["hall"]["routes"][a]
            lines.append(f"| {m['target']} | {a} | " + " | ".join(ci(rt[x]) for x in ROUTES)
                         + f" | {ci(m['hall']['switched'][a])} |")  # fmt: skip
    lines += ["", "## The locker question: kept share per arm (test half) and its drift from unedited", "",
              "| model | arm | kept | drift |", "|---|---|---|---|"]  # fmt: skip
    for m in tested:
        for a in ARMS:
            d = m["locker"]["drift"].get(a)
            lines.append(f"| {m['target']} | {a} | {ci(m['locker']['kept'][a])} | {ci(d) if d else '–'} |")
    lines += ["", "## The slot probe at the key token (every chosen scene, 5 folds by bridge entity)", "",
              "| model | n | entities | probe | majority | chance | layout (given the locker slot) | probe − best baseline |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in tested:
        p = m["probe"]
        lines.append(f"| {m['target']} | {p['n']} | {p['entities']} | {ci(p['probe'])} | {ci(p['majority'])} | "
                     f"{p['chance']:.2f} | {ci(p['layout'])} | {ci(p['probe_minus_best'])} ({p['best_baseline']}) |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "",
              "## Gate, items, fit (descriptive)", ""]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"- {m['target']} ({m['run']}): pending ({m['why']}).")
            continue
        g = m["gate"] or {}
        gtxt = (f"O read accuracy {g.get('org_read_accuracy')} (said {g.get('org_said_accuracy')}; pass {g.get('pass')}; "
                f"eligible {g.get('eligible')} of {g.get('cases')}; dropped {g.get('dropped') or 'none'})")  # fmt: skip
        if m["status"] != "tested":
            lines.append(f"- {m['target']} ({m['run']}): not tested. Gate: {gtxt}.")
            continue
        f, it = m["fit"] or {}, m["items"] or {}
        lines.append(f"- {m['target']} ({m['run']}, L{m['layer']}): gate: {gtxt}. Items: chosen {it.get('chosen')}, fit "
                     f"{it.get('fit')}, test {it.get('test')} (entities {it.get('entities')}). U_num: rank {f.get('U_rank')} "
                     f"from {f.get('states')} layout-free states ({f.get('dropped_singletons')} singletons dropped; per "
                     f"hall slot {f.get('per_slot')}; layout groups {f.get('groups')}). Median share of the change: U_num "
                     f"{m['median_share']['U']:.3f}, J++ {m['median_share']['jpp']:.3f}.")  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
               for t in RUNS if t not in targets]  # fmt: skip
    out = RESULTS / f"x47_14-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = report_lines(models, answer, n_boot)
    (out / "x47_14.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1, default=str)
                                     + "\n")  # fmt: skip
    (out / "x47_14.md").write_text("\n".join(lines) + "\n")
    ex = examples_lines([m["run"] for m in models if m["status"] == "tested"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


# ---- the verify-pack view (CPU) ------------------------------------------------------------------------------------


def examples_lines(runs: list[str], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED, decode=None) -> list[str]:
    """Per run, k random test items (seed 0): each reader's O prompt exactly as read with the key token marked, S, the
    expected letters per route, and every arm's answer."""
    lines = ["# 47.14 examples (verify pack): O as the model reads it, ⟦…⟧ the key token (the bridge's locker digit) "
             "where every arm's vector is added at L; each arm's top token, the hall question's route. UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        src = RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        dec = decode
        if dec is None:
            from bridge_jspace.review import checks as RC

            tk = RC.tokenizer(m["model"]["target"])
            dec = lambda ids, tk=tk: tk.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
        test = json.loads((src / "split.json").read_text())["test"]
        rows = X.read_jsonl(src / "outcomes.jsonl")
        pick = sorted(random.Random(seed).sample(sorted(test), min(k, len(test))))
        lines += [f"## {run} ({m['model']['target']}, L{m['layer']}): {len(pick)} random test items of {len(test)} "
                  f"(seed {seed})", ""]  # fmt: skip
        for s in pick:
            c = cases[s]
            lines += [f"### {s}: the hall sentence of locker {c['digit']} (the {c['bridge']}'s) moves from hall slot "
                      f"{c['hall_slot']} to {c['target_slot']}; the key token sits in locker slot {c['locker_slot']}", "",
                      f"Halls in O {c['halls_o']}, in S {c['halls_s']}; expected: identity {c['expect']['identity']}, "
                      f"position {c['expect']['position']}, value {c['expect']['value']}.", ""]  # fmt: skip
            for w, rd in c["readers"].items():
                mine = [r for r in rows if r["scene"] == s and r["reader"] == w]
                lines += [f"**{READER_NAME[w]}** ({rd['question']}): O's answer {rd['answer']}, S's {rd['cf_answer']}",
                          "", "O, as read:", "", "```", prompt_as_read(dec, rd, c["pos"]), "```", "",
                          "S (the source):", "", "```", prompt_as_read(dec, rd, c["pos"], "alt"), "```", "",
                          "| arm | answer | route | kept O's answer |", "|---|---|---|---|"]  # fmt: skip
                lines += [f"| {r['arm']} | {r['top_text']!r} | {r.get('route') or ''} | {r['kept']} |" for r in mine]
                lines.append("")
    return lines


def stage_examples(runs: list[str]) -> Path:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    out = RESULTS / f"examples-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    (out / "examples.md").write_text("\n".join(examples_lines(runs)) + "\n")
    print("wrote", out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "examples"])
    ap.add_argument("--name", help="run: the run name (results/x47_chain/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / examples: the 47.14 runs")
    ap.add_argument("--why", default="batch 47, test 47.14 (jobs/c3/batch47.yaml; Q47.14)")
    ap.add_argument("--n-gen", type=int, default=N_GEN, help="plan: the candidates to generate")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.n_gen)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    else:
        stage_examples(a.runs)


if __name__ == "__main__":
    main()
