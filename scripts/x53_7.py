"""x53_7 (batch 53, test 53.7; jobs/c3/batch53.yaml): the pointer in code and tool output. No prediction; UNVERIFIED.

Dan, 29 Oct 11:10 (next_1110, item 2), verbatim: "53.7 (the pointer in code and tool output): start now on any free GPU,
27B then 9B." His 09:50 priority list (standing_rules_0950, item 6): "53.7: the pointer in code and tool output (routes,
address probe, monitor)." 53.7 has no rule of its own; the coordinator's reading (next_1110_reading_537): each of the
three tests runs with its own rule verbatim on our locker scenes rendered as code and as tool output; no new rule.

The two renderings (fixed before any run). Only the rendering changes: the scene's statements and their order, the
question and the digit instruction are the source's; the alt (S) is the test's own.
  code  the scene as Python in the user turn, in tasks_v2's code framing (a ```python block, then the question and the
        instruction): `picks = {}` and `lockers = {}`, then one assignment per statement in the scene's order,
        `picks["Eva"] = "oxygen"` for "Eva picked oxygen." and `lockers["oxygen"] = 5` for "The locker of oxygen is
        5." (items by name, as tasks_v2's structured formats write them, no article; a number word stays a word).
  tool  the scene returned by a tool in the model's own chat template: the template's tools block declares get_notes();
        the user asks "Look up my notes."; the assistant calls get_notes; the tool turn holds the scene's text verbatim;
        then the question and the instruction in a new user turn; thinking off, "Answer:" prefilled.
The bridge word is located in the rendered prompt; each test's own checks keep a scene only if it is one token at one
index in O and S with both readers' prompts identical through it (drops counted). In code an item name follows a
quote, without its leading space: on both Qwen tokenizers 22 of the routes test's 32 animals, 1 of the 6 elements and
all 8 Greek letters stay one token, so code keeps fewer scenes (elements almost none). Every read is the chat read (the
prompt with a digit's space appended, the top token).

The tests, each with its own rule, arms and layer (the model's L: 27B L32, 9B L12; the monitor every second layer):
  routes   x6_routes.py run --format code|tool --keeponly --sealed (C0, C1, C2; whole; without J++ / the address, each
           against a random part of its share; J++ / the address alone, each against a random part). Its own gate per
           condition (O's read accuracy >= 0.80 per reader) and its C0 check (within 0.10 of the model's one-pick
           reference, or the run stops). Rule: "a route counts as used if its share is >= 0.20 with lower CI >= 0.10".
           routes-verdict (CPU).
  probe    the address probe (x0_probe v4: d1_topics_v4, the bridge word at L, x0_probe's probes, folds, baselines and
           bootstrap). probe-run (GPU) writes x0_probe's run layout per format; probe-verdict (CPU) scores it with
           x0_probe.score and states Dan's pre-stated reading verbatim (descriptive, as v4: no label).
  monitor  53.2 on the main test's items rendered in the format (x53_monitor datasets "code" and "tool"; S, positions,
           labels and layers as its "main"). monitor-run (GPU) computes the gate, then x53_monitor.stage_run for the
           formats that pass; x53_monitor.py probe (CPU) and monitor-verdict (CPU) apply 53.2's rule verbatim.
Gates: the routes test's are its own. The address probe and the monitor have none (descriptive / "no gate: a probe
reads states"), so each format must pass the main test's gate, X0's (the unedited O read right on >= 0.80 of the scenes
for both readers), over the test's own scenes in that format (probe: every aligned d1_topics_v4 scene; monitor: every
aligned scene of the main test's set, d1_topics_v3), before any state is kept: a failed format is "not tested (gate x <
0.80)", with no states and no probe. The gate is never lowered (BJ_GATE must be unset).

uv run python scripts/x53_7.py plan                                    # tokenizer only (BJ_TARGET): counts and drops
uv run python scripts/x6_routes.py run --name x53_7_routes_code_27b --format code --keeponly --sealed          # GPU
uv run python scripts/x53_7.py routes-verdict --names x53_7_routes_code_27b                                     # CPU
uv run python scripts/x53_7.py probe-run --name x53_7_probe_27b          # GPU: x0_probe/x53_7_probe_27b_{code,tool}
uv run python scripts/x53_7.py probe-verdict --names x53_7_probe_27b_code,x53_7_probe_27b_tool                  # CPU
uv run python scripts/x53_7.py monitor-run --name x53_7_monitor_27b      # GPU: gate, then the states (x53_monitor)
uv run python scripts/x53_monitor.py probe --name x53_7_monitor_27b --sets code,tool                            # CPU
uv run python scripts/x53_7.py monitor-verdict --names x53_7_monitor_27b                                        # CPU
Verdicts: results/<exp>/x53_7_<test>-<UTC>/ (never a script's default prefix).
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

TEST = "53.7 (the pointer in code and tool output)"
SPEC = "jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537)"
NO_PREDICTION = "Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED"
FORMATS = ("code", "tool")
FORMAT_TEXT = {
    "code": "the scene as Python in the user turn (tasks_v2's code framing): picks = {} and lockers = {}, then one "
    'assignment per statement in the scene\'s order (picks["Eva"] = "oxygen"; lockers["oxygen"] = 5), then the '
    "question and the digit instruction",
    "tool": "the scene's text verbatim as the response of a declared tool (get_notes) in the model's chat template, "
    "after the user's 'Look up my notes.' and the assistant's call; the question and the instruction in a new user turn",
}
TOOL_NAME, TOOL_REQUEST = "get_notes", "Look up my notes."
TOOL = {"type": "function", "function": {"name": TOOL_NAME, "description": "Return the user's notes.",
                                         "parameters": {"type": "object", "properties": {}, "required": []}}}  # fmt: skip
GATE_BAR = 0.80  # the main gate (X0's), fixed; never lowered
GATE_TEXT = ("X0's main gate in the format, over the test's own scenes: the unedited O prompt's chat read right on >= "
             "0.80 of the scenes for both readers; a failed format is not tested (no states, no probe)")  # fmt: skip
READ_TEXT = "the chat read: one forward of the prompt with a digit's space token appended, the top token"
# Dan 12:10 (jobs/c3/batch53.yaml decisions_1210), before any 53.7 routes or probe result was opened: the lookup-only gate
LOOKUP_GATE_DESIGN = "adapted design: lookup-only gate; the recall is not part of this test"
LOOKUP_GATE_TEXT = ("Dan 12:10 (decisions_1210): the share of the test's own scenes in the format where the lookup says "
                    "and reads O and S right (X0's competence: the greedy answer and the chat read) >= 0.80, before any "
                    "state is kept; a failed format is 'not tested (gate x < 0.80)'; an item is eligible when the lookup "
                    "is right on all four; the recall's rates are reported descriptively")  # fmt: skip
HOLLOW = "gate changed after the data (hollow)"  # Dan 12:25 (decisions_1225): the 9B code probe under the new gate
CAVEATS_1210B = ("tool output as prose (JSON is covered by x0b_v2), and the bridge ~250 tokens later in the tool format, "
                 "not separated from the format (47.16's distance robustness beside). The probe only shows the address "
                 "is readable; the routes test decides whether the lookup uses it.")  # fmt: skip
PROBE_SET = "d1_topics_v4"  # x0_probe v4's set
PICK = re.compile(r"^(\S+) picked (?:the )?(.+)\.$")
LOCKER = re.compile(r"^The locker of (?:the )?(.+) is (\S+)\.$")
PROBE_READING = (
    "Pre-stated reading (Dan, x0_probe): (a) high in locker-before and at chance in locker-after -> the answer value is "
    "stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address (a "
    "lookback-style pointer). In locker-after scenes the locker sentence follows the word, so (a) and (b) cannot be "
    "read there from the locker sentence itself: that stratum is the control by construction."
)
ROUTE_ARMS = ("whole", "no_alf", "no_alf_rand", "keep_alf", "keep_alf_rand", "no_jpp", "no_jpp_rand", "keep_jpp",
              "keep_jpp_rand")  # fmt: skip
ARM_TEXT = {"whole": "the whole change", "no_alf": "without the address", "no_alf_rand": "without a random part "
            "(the address's share)", "keep_alf": "the address alone", "keep_alf_rand": "a random part alone (the "
            "address's share)", "no_jpp": "without J++", "no_jpp_rand": "without a random part (J++'s share)",
            "keep_jpp": "J++ alone", "keep_jpp_rand": "a random part alone (J++'s share)"}  # fmt: skip
MODEL_NAME = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B"}


class Unrenderable(ValueError):
    """A sentence of the scene is neither a pick nor a locker statement."""


def utc() -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


def check_gate_bar() -> None:
    assert X.GATE == GATE_BAR, f"X.GATE is {X.GATE} (BJ_GATE set?): 53.7's gates are never lowered"


def not_tested(acc: dict[str, float]) -> str:
    """The rule's wording for a failed gate: the lowest reader's accuracy."""
    if not acc:
        return "not tested (no aligned scene)"
    return f"not tested (gate {min(acc.values()):.3f} < {GATE_BAR:.2f})"


# ---- renderings (tokenizer only) ----------------------------------------------------------------------------------


def sentences(context: str) -> list[str]:
    sents = re.split(r"(?<=\.) ", context)
    assert " ".join(sents) == context, "the context does not split into sentences"
    return sents


def statements(context: str) -> list[tuple[str, str, str]]:
    """Per sentence, in order: ("pick", person, item) or ("locker", item, number as written); items without "the"."""
    out = []
    for s in sentences(context):
        if m := PICK.match(s):
            out.append(("pick", m.group(1), m.group(2)))
        elif m := LOCKER.match(s):
            out.append(("locker", m.group(1), m.group(2)))
        else:
            raise Unrenderable(f"neither a pick nor a locker statement: {s!r}")
    return out


def code_line(kind: str, a: str, b: str) -> str:
    if kind == "pick":
        return f'picks["{a}"] = "{b}"'
    return f'lockers["{a}"] = {b if b.isdigit() else json.dumps(b)}'


def code_text(context: str) -> str:
    """The scene as Python: the two dicts, then one assignment per statement in the scene's order."""
    lines = ["picks = {}", "lockers = {}", *(code_line(*s) for s in statements(context))]
    return "```python\n" + "\n".join(lines) + "\n```"


def prompt(tok, context: str, question: str, kind: str, fmt: str) -> tuple[str, str]:
    """The prompt in a format and the scene as it appears in it (code: the code block; tool: the context)."""
    from bridge_jspace import chat
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    assert chat.FORMAT == "chat", "53.7's renderings are chat prompts: run with BJ_FORMAT unset"
    if fmt == "code":
        scene = code_text(context)
        return T.render(tok, {"format": "code", "kind": kind, "context": scene, "question": question}), scene
    assert fmt == "tool", f"format {fmt!r}: one of {FORMATS}"
    statements(context)  # the same scenes as code: only picks and lockers
    instr = T.DIGIT_INSTRUCTION if kind == "digit" else S.INSTRUCTION
    call = {"type": "function", "function": {"name": TOOL_NAME, "arguments": {}}}
    msgs = [{"role": "user", "content": TOOL_REQUEST}, {"role": "assistant", "content": "", "tool_calls": [call]},
            {"role": "tool", "content": context}, {"role": "user", "content": f"{question} {instr}"}]  # fmt: skip
    text = tok.apply_chat_template(
        msgs, tools=[TOOL], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    return text + chat.PREFILL, context


def text_and_bridge(tok, context: str, question: str, kind: str, fmt: str, asked: str, item: str) -> tuple[str, int]:
    """The prompt and the character offset of `item` in the asked person's pick statement (asserted to be that
    statement's item, the statement once in the scene)."""
    text, scene = prompt(tok, context, question, kind, fmt)
    assert text.count(scene) == 1, "the scene is not once in the prompt"
    base = text.index(scene)
    mine = [(s, st) for s, st in zip(sentences(context), statements(context), strict=True)
            if st[0] == "pick" and st[1] == asked]  # fmt: skip
    assert len(mine) == 1, f"{asked}'s pick is not once in the scene: {mine}"
    assert mine[0][1][2] == item, f"{asked} picked {mine[0][1][2]!r}, not {item!r}"
    if fmt == "tool":
        from scripts import statement_positions as SP

        sent = mine[0][0]
        return text, base + SP.find_sentence(context, sent) + sent.rindex(item)
    line = "\n" + code_line("pick", asked, item) + "\n"
    assert scene.count(line) == 1, f"{line!r} is not once in the code"
    return text, base + scene.index(line) + line.rindex(item)


def at_bridge(
    tok, context: str, question: str, kind: str, fmt: str, asked: str, item: str
) -> tuple[list[int], list[int]]:
    """The prompt's ids and the token positions overlapping the asked pick's item."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    text, w0 = text_and_bridge(tok, context, question, kind, fmt, asked, item)
    enc = raw_encoding(tok, text, offsets=True)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(item))


# ---- cases of a tasks_v2 set in a format (tokenizer only) ---------------------------------------------------------


def scene_case(tok, pair: dict[str, dict], fmt: str) -> tuple[dict | None, str | None]:
    """X0's scene_case (x0_necessity) in a 53.7 format, with X0's checks: the bridge one token at one position in O and
    S (the generator's cf), both readers' prompts identical through it, distinct answer tokens. The case keeps the
    prose context (the probe's and the monitor's labels read it; the format keeps its statements and their order)."""
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    readers: dict[str, dict] = {}
    pos = None
    for w in X.READERS:
        it = pair[w]
        asked = SP.tasks_statements(it)["holder"]
        try:
            ids_org, p_org = at_bridge(tok, it["context"], it["question"], it["kind"], fmt, asked, it["bridge"])
            ids_alt, p_alt = at_bridge(tok, it["cf_context"], it["question"], it["kind"], fmt, asked, it["cf_bridge"])
        except Unrenderable:
            return None, "a sentence is neither a pick nor a locker statement"
        if len(p_org) != 1 or p_alt != p_org:
            return None, "the bridge is not one token at one position in org and alt"
        diff = S.changed(ids_org, ids_alt)
        if not diff or p_org[0] not in diff:
            return None, "org and alt do not align at the bridge"
        if pos is not None and p_org[0] != pos:
            return None, "the readers' bridge positions differ"
        pos = p_org[0]
        tok_a, tok_b = (S.answer_token(tok, a, "digit") for a in (it["answer"], it["cf_answer"]))
        if tok_a == tok_b:
            return None, "the org and alt answers share their first token"
        readers[w] = {"id": it["id"], "question": it["question"], "answer": it["answer"], "cf_answer": it["cf_answer"],
                      "ids": {"org": ids_org, "alt": ids_alt}, "tok_A": tok_a, "tok_b": tok_b,
                      "upstream": min(diff) < pos}  # fmt: skip
    assert pos is not None
    for v in ("org", "alt"):
        if readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1]:
            return None, "the readers' prompts differ before the bridge"
    it = pair[X.LOOKUP]
    return {"scene": it["scene"], "rendering": "chat", "format": fmt, "domain": it["domain"], "bridge": it["bridge"],
            "cf_bridge": it["cf_bridge"], "context": it["context"], "cf_context": it["cf_context"], "pos": pos,
            "upstream": readers[X.LOOKUP]["upstream"], "space": S.ids(tok, " "), "readers": readers}, None  # fmt: skip


def pairs_of(set_name: str) -> dict[str, dict[str, dict]]:
    from scripts import tasks_v2 as T

    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in X.READERS:
            by_scene[it["scene"]][it["word"]] = it
    return by_scene


def build_cases(tok, set_name: str, fmt: str) -> tuple[list[dict], dict]:
    """Every scene of a tasks_v2 set with both readers in one format, in scene order (X0's build_cases, one format);
    drops counted by reason."""
    by_scene = pairs_of(set_name)
    cases, dropped = [], collections.Counter()
    for scene in sorted(by_scene):
        pair = by_scene[scene]
        if set(pair) != set(X.READERS):
            dropped["a reader is missing"] += 1
            continue
        if any(pair[X.LOOKUP][k] != pair[X.RECALL][k] for k in ("context", "cf_context", "bridge", "cf_bridge")):
            dropped["the readers' scenes differ"] += 1
            continue
        c, why = scene_case(tok, pair, fmt)
        if c is None:
            dropped[f"{pair[X.LOOKUP]['domain']}: {why}"] += 1
        else:
            cases.append(c)
    return cases, {"set": set_name, "format": fmt, "scenes": len(by_scene), "cases": len(cases),
                   "entities": len({c["bridge"] for c in cases}),
                   "domains": dict(collections.Counter(c["domain"] for c in cases)), "dropped": dict(sorted(dropped.items()))}  # fmt: skip


def main_set(target: str) -> str:
    """The tasks_v2 set of the main test's X0 run (the monitor's main dataset's source)."""
    from scripts import x49_gain as G

    return json.loads((X.RESULTS / G.SOURCES[target] / "manifest.json").read_text())["set"]


def main_items(tok, target: str, fmt: str) -> tuple[list[dict], dict]:
    """x53_monitor's main dataset (the main test's items, in its order, with its labels) rendered in a format: the same
    scenes, O and S and answers; positions B (the bridge word) and T (the last token) in the format's prompts. Items
    whose bridge fails the format's checks are dropped and counted."""
    from scripts import x53_monitor as M

    items, counts = M.main_items(tok, target)
    pairs = pairs_of(main_set(target))
    out, dropped = [], collections.Counter()
    for it in items:
        pair = pairs[it["scene"]]
        assert (pair[X.LOOKUP]["context"], pair[X.LOOKUP]["cf_context"]) == (it["context"], it["cf_context"]), it[
            "scene"
        ]
        c, why = scene_case(tok, pair, fmt)
        if c is None:
            dropped[f"{it['domain']}: {why}"] += 1
            continue
        readers = {}
        for w in X.READERS:
            rd, old = c["readers"][w], it["readers"][w]
            assert (rd["answer"], rd["cf_answer"]) == (old["answer"], old["cf_answer"]), f"{it['scene']}: answers"
            readers[w] = {"ids": rd["ids"], "suffix": c["space"], "question": rd["question"],
                          "pos": {v: {"B": c["pos"], "T": len(rd["ids"][v]) + len(c["space"]) - 1} for v in M.VARIANTS},
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")}}  # fmt: skip
        out.append({**{k: v for k, v in it.items() if k != "readers"}, "set": fmt, "format": fmt, "readers": readers})
    return out, {"format": fmt, "items": len(out), "entities": len({it["entity"] for it in out}),
                 "domains": dict(collections.Counter(it["domain"] for it in out)), "dropped": dict(sorted(dropped.items())),
                 "main": {k: v for k, v in counts.items() if k in ("source", "items", "entities", "families")}}  # fmt: skip


# ---- GPU: the gate's reads, the probe's states, the monitor's run -------------------------------------------------


def read_org(
    model, cases: list[dict], layer: int | None = None, what: str = ""
) -> tuple[list[dict], np.ndarray | None]:
    """Per case and reader, the chat read of the unedited O prompt (one forward of the prompt with the digit's space
    appended, as x53_monitor reads; the top token over the vocabulary); with a layer, also the lookup forward's block
    output at the bridge word there (x0_probe's state: causal, so the appended space does not reach it)."""
    import torch

    from bridge_jspace.utils import progress

    rows, states = [], []
    with torch.no_grad():
        for c in progress(cases, f"53.7 O reads{' and states' if layer is not None else ''} {what} (case)"):
            for w in (w for w in X.READERS if w in c["readers"]):  # code_pointer_v1's CH2: the lookup only
                rd = c["readers"][w]
                rec = (layer,) if layer is not None and w == X.LOOKUP else ()
                ids = torch.tensor([rd["ids"]["org"] + c["space"]], device=model.device)
                logits, got = model.run(ids, record=rec)
                top = int(logits.argmax())
                rows.append({"scene": c["scene"], "reader": w, "top": top, "read_right": top == rd["tok_A"]})
                if rec:
                    states.append(got[rec[0]][c["pos"]].float().cpu().numpy())
    return rows, (np.stack(states) if states else None)


def gate_of(rows: list[dict], readers: tuple[str, ...] = X.READERS) -> dict:
    """X0's gate (x0_necessity.gate_and_eligible's pass): per reader the share of O prompts read right (rounded to 4
    places as X0's org_rate), passing iff every reader's is >= GATE_BAR (readers: code_pointer_v1's CH2 has the lookup
    only)."""
    acc = {w: round(float(np.mean([r["read_right"] for r in rows if r["reader"] == w])), 4) for w in readers
           if any(r["reader"] == w for r in rows)}  # fmt: skip
    ok = len(acc) == len(readers) and all(a >= GATE_BAR for a in acc.values())
    return {"cases": len({r["scene"] for r in rows}), "org_read_accuracy": acc, "bar": GATE_BAR, "pass": ok,
            "status": "passed" if ok else not_tested(acc), "rule": GATE_TEXT}  # fmt: skip


def lookup_gate(comp: list[dict], cases: list[dict]) -> tuple[dict, list[dict]]:
    """53.7's adapted gate (Dan 12:10, decisions_1210): the share of scenes where the lookup says and reads O and S right
    (X0's competence rows: the greedy answer and the chat read), passing iff >= GATE_BAR; the eligible cases (the lookup
    right on all four, scene order). Beside (descriptive): every reader's said / read rates on O and S, and the share
    where it is right on all four."""
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    readers = [w for w in X.READERS if any(r["reader"] == w for r in comp)]

    def ok(c: dict, w: str) -> bool:
        return all(
            right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"] for v in ("org", "alt")
        )

    rates = {w: {"says_and_reads_O_and_S": round(float(np.mean([ok(c, w) for c in cases])), 4) if cases else 0.0,
                 **{f"{k}_{v}": round(float(np.mean([right[(c["scene"], w, v)][k] for c in cases])), 4) if cases else 0.0
                    for k in ("right", "read_right") for v in ("org", "alt")}} for w in readers}  # fmt: skip
    share = rates[X.LOOKUP]["says_and_reads_O_and_S"] if cases else 0.0
    passed = bool(cases) and share >= GATE_BAR
    eligible = [c for c in cases if ok(c, X.LOOKUP)]
    return {"cases": len(cases), "lookup_right_share": share, "bar": GATE_BAR, "pass": passed,
            "status": "passed" if passed else (not_tested({X.LOOKUP: share}) if cases else "not tested (no aligned scene)"),
            "eligible": len(eligible), "design": LOOKUP_GATE_DESIGN, "rule": LOOKUP_GATE_TEXT,
            "descriptive": {"rates": rates, "note": "the recall's rates are descriptive (not part of this test)"}}, eligible  # fmt: skip


def competence(model, cases: list[dict]) -> list[dict]:
    """X0's competence (x0_necessity.competence: per case, reader and O / S, the greedy answer and the chat read)."""
    import torch

    X.DIGIT_IDS.update(X.digit_ids(model.tokenizer))
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
    return X.competence(model, cases, digits, X.whitespace_mask(model))


def lookup_states(model, cases: list[dict], layer: int) -> np.ndarray:
    """x0_probe's state: the lookup's O prompt, the block output at the bridge word at the layer."""
    import torch

    from bridge_jspace.utils import progress

    out = []
    with torch.no_grad():
        for c in progress(cases, f"53.7 states at L{layer} (case)"):
            ids = torch.tensor([c["readers"][X.LOOKUP]["ids"]["org"]], device=model.device)
            out.append(model.run(ids, record=(layer,))[1][layer][c["pos"]].float().cpu().numpy())
    return np.stack(out)


def stage_probe_run(base: str, formats: tuple[str, ...] = FORMATS, set_name: str = PROBE_SET,
                    hollow: tuple[str, ...] = ()) -> list[Path]:  # fmt: skip
    """The address probe per format into results/x0_probe/<base>_<format>/ (x0_probe's run layout: manifest.json,
    states.npz, items.jsonl; plus gate.json, competence.jsonl): every aligned scene of the set; the lookup-only gate
    first (X0's competence, both readers, the recall descriptive), then the states only if the format passes. hollow:
    formats whose gate was changed after their data was seen (Dan 12:25: the 9B code probe), labelled so."""
    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import x0_probe as P

    check_gate_bar()
    assert set(hollow) <= set(formats), f"--hollow {hollow}: not among {formats}"
    target = pins.TARGET
    layer = X.PREDICTED[target]
    names = {f: f"{base}_{f}" for f in formats}
    for n in names.values():
        pins.check_run_name(n)
        assert not (P.RESULTS / n).exists(), f"{n} exists"
    items_file = pins.DATA_DIR / "tasks_v2" / set_name / "items.jsonl"
    model = load_model()
    outs = []
    for fmt, name in names.items():
        out = P.RESULTS / name
        out.mkdir(parents=True, exist_ok=False)
        m: dict[str, Any] = {
            "exp": P.EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": P.NOTE, "test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "source": None, "source_code": None,
            "set": set_name, "layer": layer, "x0_items": 0, "format": fmt, "format_text": FORMAT_TEXT[fmt],
            "gate": LOOKUP_GATE_TEXT, "gate_design": LOOKUP_GATE_DESIGN, "hollow": HOLLOW if fmt in hollow else None,
            "read": READ_TEXT, "model": pins.model_pin(), "switches": switches(), "code": git_state(),
            "position": f"the asked person's bridge word, org run, {fmt}",
            "inputs": {str(items_file.relative_to(pins.REPO_ROOT)): sha256_of(items_file)},
            "folds": {"outer": P.K_OUTER, "inner": P.K_INNER, "penalties": list(P.RELS)},
            "seeds": {"bootstrap": X.BOOT_SEED}, "targets": dict(P.TARGETS)}  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
        cases, counts = build_cases(model.tokenizer, set_name, fmt)
        print(json.dumps(counts), flush=True)
        comp = competence(model, cases)
        gate, _ = lookup_gate(comp, cases)
        gate = {**gate, "counts": counts, "hollow": m["hollow"]}
        (out / "gate.json").write_text(json.dumps(gate, indent=1) + "\n")
        X.write_jsonl(out / "competence.jsonl", comp)
        print(f"{name}: lookup gate {gate['lookup_right_share']} -> {gate['status']}", flush=True)
        if gate["pass"]:
            h = lookup_states(model, cases, layer)
            h = h.astype(np.float16) if np.abs(h).max() < 6e4 else h  # x0_probe's storage
            np.savez_compressed(out / "states.npz", h=h, scene=np.array([c["scene"] for c in cases]))
            X.write_jsonl(out / "items.jsonl", [{**P.item_of(c, False), "context": c["context"]} for c in cases])
        m.update({"gate_pass": gate["pass"], "cases": len(cases), "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
        outs.append(out)
    return outs


ELIGIBLE: dict[
    str, list[dict]
] = {}  # monitor-run: per format the lookup-eligible cases of the gate set (x53_monitor builds its items from them)


def eligible_items(tok, target: str, fmt: str) -> tuple[list[dict], dict]:
    """x53_monitor's datasets code_l / tool_l (the adapted design): the first X.N_ITEMS lookup-eligible scenes of the main
    test's set in the format (scene order, as X0 selects its items, by the lookup alone); O / S, labels and positions as
    53.2's main. Only within monitor-run, which sets ELIGIBLE from its gate."""
    from scripts import x53_monitor as M

    assert fmt in ELIGIBLE, f"{fmt}: no eligible cases (x53_7 monitor-run sets them from its gate)"
    out = []
    for c in ELIGIBLE[fmt][: X.N_ITEMS]:
        readers = {}
        for w in X.READERS:
            rd = c["readers"][w]
            readers[w] = {"ids": rd["ids"], "suffix": c["space"], "question": rd["question"],
                          "pos": {v: {"B": c["pos"], "T": len(rd["ids"][v]) + len(c["space"]) - 1} for v in M.VARIANTS},
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")}}  # fmt: skip
        lab = M.labels(c["context"], c["cf_context"], "prose", c["bridge"], c["cf_bridge"],
                       (readers[X.LOOKUP]["answer"], readers[X.LOOKUP]["cf_answer"]),
                       (readers[X.RECALL]["answer"], readers[X.RECALL]["cf_answer"]))  # fmt: skip
        out.append({"set": f"{fmt}_l", "scene": c["scene"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                    "domain": c["domain"], "format": fmt, "context": c["context"], "cf_context": c["cf_context"],
                    "labels": lab, "readers": readers})  # fmt: skip
    return out, {"format": fmt, "items": len(out), "entities": len({it["entity"] for it in out}),
                 "domains": dict(collections.Counter(it["domain"] for it in out)), "eligible": len(ELIGIBLE[fmt]),
                 "selection": f"the first {X.N_ITEMS} lookup-eligible scenes of {main_set(target)} in scene order"}  # fmt: skip


def stage_monitor_run(name: str, formats: tuple[str, ...] = FORMATS) -> Path:
    """The adapted design (Dan 12:10): per format the lookup-only gate over every aligned scene of the main test's set
    (X0's competence, both readers, the recall descriptive), then x53_monitor.stage_run (same model) on datasets
    <format>_l: the first X.N_ITEMS lookup-eligible scenes, for each format that passes; the gate in the manifest."""
    from bridge_jspace.model import load_model
    from scripts import x53_monitor as M

    check_gate_bar()
    target = pins.TARGET
    pins.check_run_name(name)
    assert not (M.RESULTS / name).exists(), f"{name} exists"
    gate_set = main_set(target)
    model = load_model()
    gates, comps = {}, {}
    for fmt in formats:
        cases, counts = build_cases(model.tokenizer, gate_set, fmt)
        comps[fmt] = competence(model, cases)
        gate, ELIGIBLE[fmt] = lookup_gate(comps[fmt], cases)
        gates[fmt] = {**gate, "set": gate_set, "counts": counts}
        print(
            f"{fmt}: lookup gate {gate['lookup_right_share']} ({gate['eligible']} eligible) -> {gate['status']}",
            flush=True,
        )
    passing = tuple(f for f in formats if gates[f]["pass"])
    extra = {"x53_7": {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "design": LOOKUP_GATE_DESIGN,
                       "formats": list(formats), "datasets": {f: f"{f}_l" for f in formats},
                       "format_text": {f: FORMAT_TEXT[f] for f in formats}, "gates": gates, "states_for": list(passing),
                       "items": f"the first {X.N_ITEMS} lookup-eligible scenes of {gate_set} per format (x53_7.eligible_items)"}}  # fmt: skip
    out = M.stage_run(name, sets_run=tuple(f"{f}_l" for f in passing), model=model, extra=extra)
    for fmt, rows in comps.items():
        X.write_jsonl(out / f"x53_7_competence_{fmt}.jsonl", rows)
    return out


def monitor_atom_ids(run_dir: Path) -> dict:
    """CPU: per recorded dataset and layer of a 53.7 monitor run, every J++ atom (token id) some training fold's fixed
    J++ subspace uses (x53_monitor.needed_atom_ids over its row_table, as its atom-ids stage); {} if no dataset passed
    its gate (no states were recorded)."""
    from scripts import x53_monitor as M

    m = json.loads((run_dir / "manifest.json").read_text())
    assert "x53_7" in m, f"{run_dir.name}: not a 53.7 monitor run"
    assert m.get("finished_utc"), f"{run_dir.name}: the forward run has not finished (no finished_utc)"
    out = {}
    for s in m["sets_done"]:
        rows = M.row_table(X.read_jsonl(run_dir / f"cases_{s}.jsonl"))
        atoms = np.load(run_dir / f"states_{s}_atoms.npy", mmap_mode="r")
        out[s] = {str(la): M.needed_atom_ids(np.asarray(atoms[li]), rows) for li, la in enumerate(m["layers"])}
    return out


def stage_monitor_atoms(source: str) -> Path:
    """GPU (53.2's fixed J++ arm, critic_1125, beside 53.7's monitor verdicts): the atom ids (monitor_atom_ids,
    computed here from the forward run in this checkout) and their unit J++ lens vectors (lens.vectors, as
    x0_necessity.dictionary and x53_monitor's atoms stage) into results/x53_monitor/<source>_atoms/:
    fixed_atom_ids.json and fixed_atoms_<set>.npz (ids_L<l> int64, vec_L<l> fp16; the layout x53_monitor's fixed pass
    reads)."""
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import x53_monitor as M

    run_dir = M.RESULTS / source
    assert (run_dir / "manifest.json").exists(), f"{run_dir}: the monitor run is not in this checkout (depends_on)"
    sm = json.loads((run_dir / "manifest.json").read_text())
    assert sm["model"]["target"] == pins.TARGET, f"{source} is a {sm['model']['target']} run, not {pins.TARGET}'s"
    name = M.atoms_run(source)
    pins.check_run_name(name)
    need = monitor_atom_ids(run_dir)
    out = M.RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": M.EXP, "run": name, "stage": "atoms", "source": source, "test": sm["x53_7"]["test"],
         "prediction": NO_PREDICTION, "spec": "jobs/c3/batch53.yaml (53.2 critic_1125 arms beside 53.7's monitor)",
         "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
         "switches": switches(), "code": git_state(), "lens": X.lens_record(), "sets": list(need),
         "what": "unit J++ lens vectors of the fixed J++ subspaces' atoms (lens.vectors, as x0_necessity.dictionary); "
                 "the ids computed here from the forward run (x53_7.monitor_atom_ids = x53_monitor.needed_atom_ids)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    (out / "fixed_atom_ids.json").write_text(json.dumps({"run": source, "sets": need}) + "\n")
    if not need:
        print(f"{source}: no dataset passed its gate; no atoms needed", flush=True)
    else:
        model = load_model()
        lens = JLens(model, "jpp")
        letters = set(model.letter_token_ids().tolist())
        with torch.no_grad():
            for s, per_layer in need.items():
                blob = {}
                for la, ids in per_layer.items():
                    assert set(ids) <= letters, f"{s} L{la}: an atom that is not a letter token"
                    vec = lens.vectors(int(la), torch.tensor(ids, device=model.device))
                    blob[f"ids_L{la}"] = np.array(ids, dtype=np.int64)
                    blob[f"vec_L{la}"] = vec.cpu().numpy().astype(np.float16)
                np.savez(out / f"fixed_atoms_{s}.npz", **blob)
                print(
                    f"{s}: {len(per_layer)} layers, {sum(len(v) for v in per_layer.values())} atom vectors", flush=True
                )
                lens._J_gpu.clear()
                torch.cuda.empty_cache()
    m["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- CPU: verdicts ----------------------------------------------------------------------------------------------------


def fmt_ci(v: list[float]) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def route_cell(rows: list[dict], cond: str, arm: str, n_boot: int = X.N_BOOT) -> dict | None:
    """x6_routes.stage_verdict's cell, verbatim: the lookup's route shares under one arm in one condition (cluster
    bootstrap over the bridge item), the recall's switch share beside, and the routes the rule counts as used."""
    from scripts import x6_routes as R

    mine = [r for r in rows if r["condition"] == cond and r.get("variant") is None and r["arm"] == arm]
    lk = [r for r in mine if r["reader"] == X.LOOKUP]
    rc = {r["scene"]: r for r in mine if r["reader"] == X.RECALL}
    if not lk:
        return None
    sw = {rt: [int(r["route"] == rt) for r in lk] for rt in R.ROUTES}
    sw["recall_follows_s"] = [rc[r["scene"]]["switched"] for r in lk]
    rr = X.resampled_rates(sw, [r["entity"] for r in lk], n_boot)
    share = {k: [float(np.mean(v)), *X.interval(rr[k])] for k, v in sw.items()}
    used = [rt for rt in R.ROUTES[:4] if share[rt][0] >= R.USED_SHARE and share[rt][1] >= R.USED_LO]
    return {"n": len(lk), "entities": len({r["entity"] for r in lk}), "share": share, "used": used}


def routes_status(src: Path) -> dict[str, str]:
    """Per condition of a routes run: "tested", or not tested by its gate (O's read accuracy per reader) or by the C0
    check (the rule: C0 within 0.10 of the reference "or the run stops"). Raises when the run failed otherwise."""
    m = json.loads((src / "manifest.json").read_text())
    assert m["gate"] == m["gate_fixed_in_advance"] == GATE_BAR, f"{src.name}: gate {m['gate']}, not {GATE_BAR}"
    assert (src / "gate.json").exists(), f"{src.name}: no gate.json (the run failed before its gate)"
    gate = json.loads((src / "gate.json").read_text())["gate"]
    if m.get("lookup_gate"):  # 53.7's adapted design (decisions_1210): the lookup's says-and-reads share
        out = {c: "tested" if gate[c]["pass"] else not_tested({X.LOOKUP: gate[c]["lookup_right_share"]})
               for c in m["conditions"]}  # fmt: skip
    else:
        out = {c: "tested" if gate[c]["pass"] else not_tested(gate[c]["org_read_accuracy"]) for c in m["conditions"]}
    c0 = json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else None
    if c0 is not None and not c0["ok"]:
        rate = "no C0 rows" if c0["c0_lookup_switch"] != c0["c0_lookup_switch"] else f"{c0['c0_lookup_switch']:.3f}"
        why = (f"not tested (the C0 check stopped the run: C0's lookup switch {rate}, reference "
               f"{c0['reference']:.3f} +- 0.10)" if c0.get("c0_min") is None else
               f"not tested (the C0 check stopped the run: C0's lookup switch {rate} < {c0['c0_min']})")  # fmt: skip
        return {c: s if s != "tested" else why for c, s in out.items()}
    if any(s == "tested" for s in out.values()):
        assert (src / "outcomes.jsonl").exists(), f"{src.name}: a condition passed its gate but there are no outcomes"
        assert c0 is not None or "C0" not in m["conditions"], f"{src.name}: outcomes but no C0 check"
    return out


def stage_routes_verdict(names: list[str], n_boot: int = X.N_BOOT) -> Path:
    """The routes test's rule per run (model x format), condition and arm, into results/x6_routes/x53_7_routes-<UTC>/."""
    from scripts import x6_routes as R

    runs = []
    for name in names:
        src = R.RESULTS / name
        m = json.loads((src / "manifest.json").read_text())
        status = routes_status(src)
        rows = X.read_jsonl(src / "outcomes.jsonl") if any(s == "tested" for s in status.values()) else []
        c0 = json.loads((src / "c0_check.json").read_text()) if (src / "c0_check.json").exists() else None
        gate = json.loads((src / "gate.json").read_text())
        cells = {}
        for cond, st in status.items():
            if st != "tested":
                continue
            for arm in ROUTE_ARMS:
                cell = route_cell(rows, cond, arm, n_boot)
                if cell is not None:
                    cells[f"{cond}|{arm}"] = cell
        runs.append({"run": name, "model": m["model"]["target"], "format": m.get("format", "prose"),
                     "layer": m["layer"], "items": m.get("items"), "status": status, "gate": gate, "c0_check": c0,
                     "cells": cells, "design": m.get("gate_design", "the routes test's two-reader gate"),
                     "u_from": m.get("alf_from")})  # fmt: skip
    out = R.RESULTS / f"x53_7_routes-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    rule = f"a route counts as used if its share is >= {R.USED_SHARE} with lower CI >= {R.USED_LO}"
    lookup = all(r["design"] == R.LOOKUP_GATE_DESIGN for r in runs)
    gate_text = (f"{R.LOOKUP_GATE_DESIGN} (Dan 12:10, decisions_1210): per condition {R.LOOKUP_GATE_RULE}" if lookup
                 else f"per condition, O's read accuracy >= {GATE_BAR} per reader (x6_routes' gate)")  # fmt: skip
    blob = {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": rule,
            "design": R.LOOKUP_GATE_DESIGN if lookup else "two-reader gate",
            "c0_rule": f"C0 must reproduce the one-pick lookup switch rate within {R.C0_TOL}, or the run stops",
            "gate": gate_text, "n_boot": n_boot, "seed": X.BOOT_SEED, "format_text": FORMAT_TEXT, "runs": runs,
            "written_utc": utc()}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {TEST}: the routes test in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             *([f"**{R.LOOKUP_GATE_DESIGN}.**", ""] if lookup else []),
             f'Rule (the routes test\'s, verbatim): "{rule[0].upper() + rule[1:]}." The C0 sanity swap must reproduce the '
             f"one-pick lookup switch rate within {R.C0_TOL}, or the run stops (lookup-based, unchanged). Gate: "
             f"{gate_text}; a failed condition is not tested. Cluster bootstrap over the bridge item "
             f"({n_boot:,} resamples, seed {X.BOOT_SEED}). C1: identity = original (both a)."
             + (" The recall's columns are descriptive (not part of this test)." if lookup else ""), "",
             *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
             "The address U (the 'address' arms) is carried over from prose, not refit on the code / tool scenes: "
             "x0_massmean.subspaces' Alf (the layout-free mass-mean of the bridge word's states by locker slot) on the "
             "model's prose probe states at L (x0_probe v4, d1_topics_v4; scripts/x6_routes.py stage_run, "
             "MM.subspaces(STATES[target])), per run: "
             + "; ".join(f"{MODEL_NAME.get(r['model'], r['model'])} {r['format']} {r['u_from']}" for r in runs) + ".", "",
             "| model | format | condition | status | gate | beside (descriptive) |", "|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        for cond, st in r["status"].items():
            g = r["gate"]["gate"][cond]
            if "lookup_right_share" in g:  # the adapted design: the lookup's share decides; the recall beside
                d = g["descriptive"]
                gate_txt = (
                    f"lookup says and reads O and S right: {g['lookup_right_share']:.3f} ({g['eligible']} eligible)"
                )
                side = (f"recall the same: {d['recall_right_share']:.3f}; O read lookup / recall "
                        f"{d['org_read_accuracy'][X.LOOKUP]:.3f} / {d['org_read_accuracy'][X.RECALL]:.3f}")  # fmt: skip
            else:
                acc = g["org_read_accuracy"]
                gate_txt, side = f"O read lookup / recall {acc[X.LOOKUP]:.3f} / {acc[X.RECALL]:.3f}", ""
            lines.append(
                f"| {MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | {cond} | {st} | {gate_txt} | {side} |"
            )
        if r["c0_check"]:
            c = r["c0_check"]
            lines.append(f"| | | C0 check | {'ok' if c['ok'] else 'failed: the run stops'} | lookup switch "
                         f"{c['c0_lookup_switch']:.3f} vs reference {c['reference']} |")  # fmt: skip
    lines += ["", "## Route shares of the lookup per arm (the rule's 'used' routes at the right)", "",
              "| model | format | condition | arm | n | identity | position | value | original | other | recall "
              "follows S (descriptive) | used |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        for key, c in r["cells"].items():
            cond, arm = key.split("|")
            s = c["share"]
            lines.append(f"| {MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | {cond} | {ARM_TEXT[arm]} | "
                         f"{c['n']} | " + " | ".join(fmt_ci(s[rt]) for rt in R.ROUTES)
                         + f" | {fmt_ci(s['recall_follows_s'])} | {', '.join(c['used']) or 'none'} |")  # fmt: skip
    lines += report_lines("x6_routes (53.7 routes)", runs, "the lookup's position share without the address against "
                          "without a random part of its share, and with the address alone against a random part "
                          "alone, per format; the value share under the whole change", "verdict.json: runs[].cells"
                          "['C2|whole'].share (recompute from results/x6_routes/<run>/outcomes.jsonl, lookup rows of "
                          "C2 under 'whole': the share of route == 'position')")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    routes_figure(blob, out / "x53_7_routes.png")
    print(f"wrote {out}", flush=True)
    return out


def routes_figure(blob: dict, path: Path) -> None:
    """Per run (rows) and condition C1 / C2 (columns): the lookup's route shares per arm as stacked bars; a condition
    not tested keeps its panel with the reason."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts import story_style as SS
    from scripts import x6_routes as R

    runs = blob["runs"]
    conds = ("C1", "C2")
    fig, axes = plt.subplots(len(runs), 2, figsize=(13, 2.9 * len(runs) + 1.0), squeeze=False, sharex=True)
    for i, r in enumerate(runs):
        for j, cond in enumerate(conds):
            ax = axes[i][j]
            st = r["status"].get(cond, "not run")
            ax.set_title(f"{MODEL_NAME.get(r['model'], r['model'])}, {r['format']}, {cond}", fontsize=9)
            if st != "tested":
                ax.text(0.5, 0.5, st, ha="center", va="center", fontsize=9, color="#777777", transform=ax.transAxes)
                ax.set_yticks([])
                continue
            arms = [a for a in ROUTE_ARMS if f"{cond}|{a}" in r["cells"]]
            for y, arm in enumerate(arms):
                left = 0.0
                for rt in R.ROUTES:
                    v = r["cells"][f"{cond}|{arm}"]["share"][rt][0]
                    ax.barh(y, v, left=left, color=SS.COL[rt], edgecolor="white", lw=0.5)
                    left += v
            # the arm names once per row (left panel): long labels on both panels squeeze the left one off the figure
            ax.set_yticks(range(len(arms)), [ARM_TEXT[a] for a in arms] if j == 0 else [""] * len(arms), fontsize=7.5)
            ax.invert_yaxis()
            ax.set_xlim(0, 1)
    for ax in axes[-1]:
        ax.set_xlabel("share of the lookup's answers", fontsize=9)
    from matplotlib.patches import Rectangle

    handles = [Rectangle((0, 0), 1, 1, color=SS.COL[rt]) for rt in R.ROUTES]
    fig.legend(handles, list(R.ROUTES), loc="upper center", ncol=5, frameon=False, fontsize=9)
    fig.suptitle(f"{TEST}: which route the lookup takes, per format (rule: {blob['rule']}; UNVERIFIED)", fontsize=10,
                 y=1.0 - 0.3 / (2.9 * len(runs) + 1.0))  # fmt: skip
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.7 / (2.9 * len(runs) + 1.0)))
    fig.subplots_adjust(left=0.2)  # room for the longest arm name
    fig.savefig(path, dpi=130, facecolor="white")
    plt.close(fig)


def prose_v4_rows(target: str) -> tuple[str | None, list[dict]]:
    """Beside (descriptive): the prose v4 probe of the same model (results/x0_probe/<run>/probe-*/probe.json, the
    newest), if it is here."""
    from scripts import x0_probe as P
    from scripts import x6_routes as R

    run = R.STATES.get(target)
    found = sorted((P.RESULTS / run).glob("probe-*/probe.json")) if run else []
    if not found:
        return None, []
    return str(found[-1].relative_to(pins.REPO_ROOT)), json.loads(found[-1].read_text())["rows"]


def stage_probe_verdict(names: list[str], n_boot: int = X.N_BOOT, prefix: str = "x53_7_probe") -> Path:
    """The address probe per run (model x format): the gate, then x0_probe.score per stratum and target (every scene of
    the run; the strata it has), Dan's reading verbatim, the prose v4 run beside; results/x0_probe/<prefix>-<UTC>/.
    prefix x53_7_cp_probe: code_pointer_v1's CH2 runs, numbers only (no reading, no prose run beside)."""
    from scripts import x0_probe as P

    cp = prefix != "x53_7_probe"  # code_pointer_v1 CH2: descriptive, numbers only (Dan, critic_1125)
    out = P.RESULTS / f"{prefix}-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    runs = []
    for name in names:
        src = P.RESULTS / name
        m = json.loads((src / "manifest.json").read_text())
        gate = json.loads((src / "gate.json").read_text())
        hollow = m.get("hollow")  # Dan 12:25: a gate changed after the data
        rec: dict[str, Any] = {"run": name, "model": m["model"]["target"], "format": m["format"], "layer": m["layer"],
                               "set": m["set"], "gate": gate, "design": m.get("gate_design", "two-reader gate"),
                               "hollow": hollow,
                               "status": gate["status"] if not gate["pass"] else "tested" + (f", {hollow}" if hollow else "")}  # fmt: skip
        if gate["pass"]:
            z = np.load(src / "states.npz")
            h, scenes = z["h"].astype(np.float64), [str(s) for s in z["scene"]]
            items = X.read_jsonl(src / "items.jsonl")
            assert [it["scene"] for it in items] == scenes, f"{name}: items.jsonl and states.npz disagree"
            for it in items:
                if "layout" not in it:  # prose scenes; CH2's items carry their own (every entry precedes the chain)
                    it["layout"] = P.layout(it["context"], it["pick_index"])
            orders = {it["order"] for it in items}
            strata = [s for s in P.STRATA if s in orders or (s == "both" and len(orders) > 1)]
            rows = []
            for stratum in strata:
                idx = [i for i, it in enumerate(items) if stratum == "both" or it["order"] == stratum]
                for target in P.TARGETS:
                    rows.append({"subset": "all", "stratum": stratum, "target": target,
                                 **P.score(h[idx], [items[i] for i in idx], target, n_boot)})  # fmt: skip
            rec["rows"] = rows
            (out / name).mkdir()
            (out / name / "probe.json").write_text(json.dumps({"run": name, "manifest": m, "note": P.NOTE, "rows": rows},
                                                              indent=1) + "\n")  # fmt: skip
            if strata == list(P.STRATA):
                P.figures(out / name)
            else:
                probe_bars(rows, out / name / "probe.png", f"{name}: {', '.join(strata)} only")
        rec["prose_v4"], rec["prose_v4_rows"] = prose_v4_rows(rec["model"]) if not cp else (None, [])
        runs.append(rec)
    lookup = not cp and all(r["design"] == LOOKUP_GATE_DESIGN for r in runs)
    gate_text = CP_GATE_TEXT if cp else f"{LOOKUP_GATE_DESIGN}: {LOOKUP_GATE_TEXT}" if lookup else GATE_TEXT
    blob = {"test": TEST if not cp else CP_TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED",
            "reading": PROBE_READING if not cp else None, "design": LOOKUP_GATE_DESIGN if lookup else None,
            "caveats": CAVEATS_1210B if not cp else None,
            "rule": "none of its own (descriptive, x0_probe); the reading stated beside, verbatim" if not cp else CP_RULE,
            "gate": gate_text, "n_boot": n_boot, "seed": X.BOOT_SEED,
            "format_text": FORMAT_TEXT if not cp else {"cp_ch2": CP_TEXT}, "runs": runs, "written_utc": utc()}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    if cp:
        lines = [f"# {CP_TEST}: the address probe (descriptive, numbers only)", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
                 f"Rule: {CP_RULE}", "", f"Gate: {CP_GATE_TEXT}.", "", f"- {CP_TEXT}.", "",
                 "| model | format | layer | aligned scenes | gate | beside (descriptive) | status |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    else:
        lines = [f"# {TEST}: the address probe in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
                 *([f"**{LOOKUP_GATE_DESIGN}.**", ""] if lookup else []),
                 "Rule: none of its own (x0_probe v4 is descriptive, added after the data). " + PROBE_READING, "",
                 f"Gate (53.7): {gate_text}.", "", f"Caveats (Dan 12:10b): {CAVEATS_1210B}", "",
                 *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
                 f"○ = {HOLLOW} (Dan 12:25, decisions_1225).", "",
                 "| model | format | layer | aligned scenes | gate | beside (descriptive) | status |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        g = r["gate"]
        if "lookup_right_share" in g:
            gate_txt = f"lookup says and reads O and S right: {g['lookup_right_share']:.3f}"
            side = "; ".join(f"{w} {v['says_and_reads_O_and_S']:.3f}, O read {v['read_right_org']:.3f}"
                             for w, v in g["descriptive"]["rates"].items())  # fmt: skip
        else:
            acc = g["org_read_accuracy"]
            gate_txt, side = "O read " + (" / ".join(f"{acc[w]:.3f}" for w in X.READERS if w in acc) or "-"), ""
        mark = "○ " if r["hollow"] else ""
        lines.append(f"| {mark}{MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | L{r['layer']} | {g['cases']} | "
                     f"{gate_txt} | {side} | {r['status']} |")  # fmt: skip
    lines += ["", "## Probe accuracy (every scene of the run; folds by bridge entity for (a), (b), by item for (c))", "",
              "| model | format | locker vs pick | target | n | entities | classes | probe | majority | chance | structure "
              "| layout | probe - best baseline | prose v4 probe (beside) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        prose = {(p["stratum"], p["target"]): p["probe"] for p in r["prose_v4_rows"] if p["subset"] == "all"}
        for p in r.get("rows", []):
            lines.append(f"| {'○ ' if r['hollow'] else ''}{MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | {p['stratum']} | {p['target']} | "
                         f"{p['n']} | {p['entities']} | {p['classes']} | {fmt_ci(p['probe'])} | {fmt_ci(p['majority'])} | "
                         f"{p['chance']:.2f} | {fmt_ci(p['structure']) if 'structure' in p else '-'} | "
                         f"{fmt_ci(p['layout']) if 'layout' in p else '-'} | {fmt_ci(p['probe_minus_best'])} "
                         f"({p['best_baseline']}) | {fmt_ci(prose[(p['stratum'], p['target'])]) if (p['stratum'], p['target']) in prose else '-'} |")  # fmt: skip
    if cp:
        lines += report_lines("x0_probe (code_pointer_v1 CH2, descriptive)", runs, "numbers only (no rule, no label): "
                              "probe (b), the key's dict slot, against the best baseline; there is no locker-after "
                              "stratum (the dict always comes first), so no control by construction", "verdict.json: "
                              "runs[].rows; rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}")  # fmt: skip
    else:
        lines += report_lines("x0_probe (53.7 address probe)", runs, "probe (b), which locker sentence, locker before "
                              "the pick, against the best baseline (layout / pick index / majority); the locker-after "
                              "stratum is the control", "verdict.json: runs[].rows (stratum 'before', target 'locker "
                              "sentence'); rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out}", flush=True)
    return out


def stage_monitor_verdict(names: list[str], n_boot: int = X.N_BOOT, states_root: Path | None = None) -> Path:
    """53.2's rule (x53_monitor.summarize, rule_label) per run (model) and format that passed its gate, from the CPU
    probes in cache/x53_monitor/<run>/<format>.npz; one figure per format (x53_monitor.figure);
    results/x53_monitor/x53_7_monitor-<UTC>/."""
    from scripts import x53_monitor as M

    root = states_root or M.RESULTS
    results: dict[str, dict] = {}
    status: list[dict] = []
    for name in names:
        m = json.loads((root / name / "manifest.json").read_text())
        target, x = m["model"]["target"], m["x53_7"]
        for fmt in x["formats"]:
            g, ds = x["gates"][fmt], x.get("datasets", {}).get(fmt, fmt)  # the adapted design's datasets: <format>_l
            rec = {"run": name, "model": target, "format": fmt, "dataset": ds,
                   "design": x.get("design", "two-reader gate (superseded, decisions_1210)"), "gate": g}  # fmt: skip
            if g["pass"]:
                pr = M.load_probes(name, ds)
                assert pr is not None, f"{name} {ds}: no probes in {M.CACHE / name}: run x53_monitor.py probe first"
                results.setdefault(target, {})[ds] = M.summarize(pr, n_boot)
                rec["status"] = "tested"
            else:
                rec["status"] = g["status"]
            status.append(rec)
    lookup = all(s["design"] == LOOKUP_GATE_DESIGN for s in status)
    gate_text = f"{LOOKUP_GATE_DESIGN}: {LOOKUP_GATE_TEXT}" if lookup else GATE_TEXT
    out = M.RESULTS / f"x53_7_monitor-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    figs = []
    for ds in dict.fromkeys(ds for r in results.values() for ds in r):
        M.figure(results, ds, out / f"x53_7_monitor_{ds}.png")
        figs.append(f"x53_7_monitor_{ds}.png")
    blob = {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": M.RULE,
            "design": LOOKUP_GATE_DESIGN if lookup else "two-reader gate", "gate": gate_text,
            "format_text": FORMAT_TEXT, "runs": status, "figures": figs, "n_boot": n_boot, "results": results,
            "written_utc": utc()}  # fmt: skip
    (out / "x53_7_monitor.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {TEST}: the monitor test (53.2) in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             *([f"**{LOOKUP_GATE_DESIGN}.** Target (d), the recall's answer, is a positive control (critic_1125); the "
                "gate's recall rates are descriptive.", ""] if lookup else []),
             f"Rule (53.2's, verbatim): {M.RULE}", "", f"Gate (53.7): {gate_text}.", "",
             *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
             "| model | format | gate set | gate | beside (descriptive) | status |", "|---|---|---|---|---|---|"]  # fmt: skip
    for s in status:
        g = s["gate"]
        if "lookup_right_share" in g:
            rates = g["descriptive"]["rates"]
            gate_txt = f"lookup says and reads O and S right: {g['lookup_right_share']:.3f} ({g['eligible']} eligible)"
            side = "; ".join(
                f"{w} {r['says_and_reads_O_and_S']:.3f}, O read {r['read_right_org']:.3f}" for w, r in rates.items()
            )
        else:
            acc = g["org_read_accuracy"]
            gate_txt, side = " / ".join(f"{acc[w]:.3f}" for w in X.READERS if w in acc), ""
        lines.append(f"| {M.NAMES.get(s['model'], s['model'])} | {s['format']} | {g['set']} ({g['cases']} scenes) | "
                     f"{gate_txt} | {side} | {s['status']} |")  # fmt: skip
    lines += ["", "## Labels (53.2's rule per position, target and k; the arms beside where their passes ran)", "",
              "The decisive label is the per-state J++ part against a random subspace of the same k. Beside it (53.2, "
              "critic_1125): the same rule with the fixed J++ subspace (fixed) and with the energy-matched random "
              "subspace (erand); '-' where that pass has not run.", "",
              "| model | format | position | target | k = 25 | k = 100 | full max | J++25 max (gap max) | J++100 max (gap max) "
              "| beside: fixed k25 / k100 | beside: erand k25 / k100 |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in M.MODELS:
        for fmt, r in results.get(t, {}).items():
            for p in M.PROBE_POS:
                for tg in M.TARGETS:
                    ru = r["rules"][f"{p}|{tg}"]
                    side = [" / ".join(ru[f"{tag}k{k}"]["label"] if f"{tag}k{k}" in ru else "-" for k in M.KS)
                            for tag in ("fixed_", "erand_")]  # fmt: skip
                    lines.append(f"| {M.NAMES[t]} | {fmt} (n {r['n_rows']} rows, {r['n_entities']} entities) | {p} | "
                                 f"{M.TARGET_TEXT[tg]} | {ru['k25']['label']} | {ru['k100']['label']} | "
                                 f"{ru['k25']['full_max']:.2f} | {ru['k25']['jpp_max']:.2f} ({ru['k25']['gap_max']:+.2f}) | "
                                 f"{ru['k100']['jpp_max']:.2f} ({ru['k100']['gap_max']:+.2f}) | {side[0]} | {side[1]} |")  # fmt: skip
    lines += report_lines("x53_monitor (53.7 monitor)", status, "per target and position the J++ probe against the "
                          "random subspace of the same k, and the full residual's best layer (53.2's rule)",
                          "x53_7_monitor.json: results[<model>][<format>]['acc'] and ['rules']; the probes in "
                          "cache/x53_monitor/<run>/<format>.npz (x53_monitor.py probe, deterministic)")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out}", flush=True)
    return out


def report_lines(exp: str, runs: list[dict], headline: str, verify: str) -> list[str]:
    """AGENTS.md's report block for a 53.7 verdict."""
    from bridge_jspace.utils import git_state

    sha = str(git_state()["sha"] or "?")[:8]
    cells = "; ".join(f"{MODEL_NAME.get(r['model'], r['model'])} {r['format']}: "
                      f"{r['status'] if isinstance(r['status'], str) else ', '.join(f'{c} {s}' for c, s in r['status'].items())}"
                      for r in runs)  # fmt: skip
    return ["", "## Report", "",
            f"EXP {exp} @ {sha} | models {', '.join(sorted({str(MODEL_NAME.get(r['model'], r['model'])) for r in runs}))} | "
            "n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's "
            "own generator / set", "",
            f"Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output "
            f"(53.7: no prediction). Headline: {headline}.", "", f"Status per run: {cells}.", "",
            "Three dumbest ways this could be wrong:",
            "1) The format changes which scenes survive the alignment check (code keeps names that are one token after a "
            "quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and "
            "domains per format are in each run's gate.json / manifest; not controlled.",
            "2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits "
            "~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.",
            "3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route "
            "would pass it. Not checked beyond each test's own controls.", "",
            f"For the human to verify: {verify}.", "", "Status: UNVERIFIED (batch 53, exploration; nothing into the README)."]  # fmt: skip


# ---- code_pointer_v1's CH2 chains (Dan 11:25, critic_1125: "only if time remains: descriptive, the address probe and
# the monitor"): no rule, no label, numbers only --------------------------------------------------------------------

CP_TEST = "53.7 add-on: code_pointer_v1's CH2 chains (Dan 11:25, critic_1125; descriptive)"
CP_SET, CP_FAMILY, CP_LEVEL, CP_DOMAINS = "main", "CH2", "e5f0", ("animals", "months")
CP_MONITOR_PER_DOMAIN = 100  # the monitor's items: the first 100 aligned scenes per domain (200, as 53.2's main)
CP_FORMAT = "cp_ch2"
CP_TEXT = ("cp_ch2: code_pointer_v1's CH2 programs (data/code_pointer_v1/main/{animals,months}_CH2_e5f0.json, 400 "
           "scenes each): a dict line `lockers = {...}` of 5 keys, then a 2-variable target chain (x = \"mouse\"; h = x) "
           "and a distractor chain, then print(lockers[h]); suite_v1's chat prompt ('What does this Python code print?'). "
           "The bridge word = the target chain's head key; S = the item's dissoc source (another key heads the chain, its "
           "own dict). One reader (the lookup): the monitor's (d) is the key's recalled number (legs / month), read at "
           "the bridge word and at the lookup's last token (CH2 has no recall prompt; the recall slot repeats the "
           "lookup's prompt); the dict always precedes the chain, so the probe has no locker-after stratum")  # fmt: skip
CP_RULE = ("none: descriptive, numbers only (Dan 11:25, critic_1125: 'code_pointer_v1 (CH2 chains) only if time "
           "remains: descriptive, the address probe and the monitor'); no label is computed or stated")  # fmt: skip
CP_GATE_TEXT = ("X0's main gate on CH2's one reader: the unedited base prompt's chat read right on >= 0.80 of the "
                "scenes (both domains pooled; per domain beside), before any state is kept; a failure is 'not tested "
                "(gate x < 0.80)'. code_pointer_v1's own competence gate (Wilson lower bound >= 0.85 per domain x family; "
                "the 27B: CH2 100% on both domains, results/code_pointer_v1/code_competence_27b) is not re-applied")  # fmt: skip


def cp_items() -> list[dict]:
    from scripts import code_pointer_v1 as CP

    return [it for d in CP_DOMAINS for it in CP.load_file(CP.DATA / CP_SET / f"{d}_{CP_FAMILY}_{CP_LEVEL}.json")]


def cp_bridge(tok, context: str, question: str, code: dict) -> tuple[list[int], list[int]]:
    """A CH2 program's chat prompt (suite_v1.render, as code_pointer_v1's competence) and the token positions of the
    target chain's head key (`x = "mouse"`: the key's characters)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S

    text = S.render(tok, context, question)
    head = code["heads"]["target"]
    line = "\n" + f'{code["vars"]["target"][0]} = "{head}"' + "\n"
    assert text.count(context) == 1, "the program is not once in the prompt"
    assert context.count(line) == 1, f"{line!r} is not once in the program"
    w0 = text.index(context) + context.index(line) + line.rindex(head)
    enc = raw_encoding(tok, text, offsets=True)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(head))


def cp_case(tok, it: dict) -> tuple[dict | None, str | None]:
    """One CH2 scene: O = the base program, S = its dissoc source; the head key one token in each; distinct answers."""
    from scripts import code_pointer_v1 as CP
    from scripts import suite_v1 as S

    src = it["sources"]["dissoc"]
    bridge, cf = it["code"]["heads"]["target"], src["code"]["heads"]["target"]
    assert bridge == it["query"], it["id"]
    assert it["entities"][it["slots"]["query"]] == bridge, it["id"]
    assert cf == src["query"], it["id"]
    assert src["entities"][src["query_slot"]] == cf, it["id"]
    ids_o, p_o = cp_bridge(tok, it["context"], it["question"], it["code"])
    ids_s, p_s = cp_bridge(tok, src["context"], src["question"], src["code"])
    if len(p_o) != 1 or len(p_s) != 1:
        return None, "the head key is not one token in O and S"
    tok_a, tok_b = (S.answer_token(tok, a, "digit") for a in (it["answer"], src["answer"]))
    if tok_a == tok_b:
        return None, "the O and S answers share their first token"
    lines = it["code"]["lines"]
    rd = {"id": it["id"], "question": it["question"], "answer": it["answer"], "cf_answer": src["answer"],
          "ids": {"org": ids_o, "alt": ids_s}, "tok_A": tok_a, "tok_b": tok_b}  # fmt: skip
    return {"scene": it["id"], "rendering": "chat", "format": CP_FORMAT, "domain": it["domain"], "bridge": bridge,
            "cf_bridge": cf, "context": it["context"], "cf_context": src["context"], "pos": p_o[0], "cf_pos": p_s[0],
            "space": S.ids(tok, " "), "readers": {X.LOOKUP: rd},
            "cp": {"slot": it["slots"]["query"], "cf_slot": src["query_slot"], "n_slots": it["n_entities"],
                   "recall": str(it["recalled"][bridge]), "cf_recall": str(CP.rec(it["domain"], cf)),
                   "head_line": lines.index(f'{it["code"]["vars"]["target"][0]} = "{bridge}"'),
                   "n_lines": len(lines)}}, None  # fmt: skip


def cp_cases(tok) -> tuple[list[dict], dict]:
    cases, dropped = [], collections.Counter()
    for it in cp_items():
        c, why = cp_case(tok, it)
        if c is None:
            dropped[f"{it['domain']}: {why}"] += 1
        else:
            cases.append(c)
    return cases, {"set": f"code_pointer_v1/{CP_SET} {CP_FAMILY}", "cases": len(cases),
                   "entities": len({c["bridge"] for c in cases}),
                   "domains": dict(collections.Counter(c["domain"] for c in cases)), "dropped": dict(sorted(dropped.items()))}  # fmt: skip


def cp_probe_item(c: dict) -> dict:
    """x0_probe's item for a CH2 scene: (a) the printed digit, (b) the key's dict slot, (c) the key; the dict precedes
    the chain ("before"); pick_index = the head line's place among the chain lines; layout = every entry before."""
    n = c["cp"]["n_slots"]
    return {"scene": c["scene"], "entity": c["bridge"], "domain": c["domain"], "x0": False, "order": "before",
            "answer": c["readers"][X.LOOKUP]["answer"], "locker_form": "digit", "pick_index": c["cp"]["head_line"],
            "locker_index": c["cp"]["slot"], "sentences": n + c["cp"]["n_lines"], "pos": c["pos"], "layout": f"{n}/{n}",
            "context": c["context"]}  # fmt: skip


def cp_monitor_items(tok, target: str) -> tuple[list[dict], dict]:
    """x53_monitor's dataset cp_ch2: the first CP_MONITOR_PER_DOMAIN aligned CH2 scenes per domain; O / S rows with
    their own labels; the recall slot repeats the lookup (CH2 has one reader), so T recall = T lookup."""
    from scripts import x53_monitor as M

    cases, counts = cp_cases(tok)
    out = []
    for d in CP_DOMAINS:
        for c in [c for c in cases if c["domain"] == d][:CP_MONITOR_PER_DOMAIN]:
            rd = c["readers"][X.LOOKUP]
            pos = {"org": c["pos"], "alt": c["cf_pos"]}
            reader = {"ids": rd["ids"], "suffix": c["space"], "question": rd["question"],
                      "pos": {v: {"B": pos[v], "T": len(rd["ids"][v]) + len(c["space"]) - 1} for v in M.VARIANTS},
                      **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")}}  # fmt: skip
            lab = {"org": {"bridge": c["bridge"], "slot": c["cp"]["slot"], "n_slots": c["cp"]["n_slots"],
                           "lookup": rd["answer"], "recall": c["cp"]["recall"]},
                   "alt": {"bridge": c["cf_bridge"], "slot": c["cp"]["cf_slot"], "n_slots": c["cp"]["n_slots"],
                           "lookup": rd["cf_answer"], "recall": c["cp"]["cf_recall"]}}  # fmt: skip
            out.append({"set": CP_FORMAT, "scene": c["scene"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                        "domain": d, "format": CP_FORMAT, "context": c["context"], "cf_context": c["cf_context"],
                        "labels": lab, "readers": {X.LOOKUP: reader, X.RECALL: dict(reader)},
                        "one_reader": True})  # fmt: skip
    return out, {**counts, "monitor_items": len(out), "per_domain": CP_MONITOR_PER_DOMAIN,
                 "monitor_entities": len({it["entity"] for it in out}), "target": target}  # fmt: skip


def stage_cp_run(probe_name: str, monitor_name: str) -> tuple[Path, Path]:
    """GPU: CH2's gate (the base read) with the lookup's state at the head key at L on every aligned scene (the address
    probe: results/x0_probe/<probe_name>/), then, if the gate passes, x53_monitor.stage_run on cp_ch2 (same model)."""
    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import code_pointer_v1 as CP
    from scripts import x0_probe as P
    from scripts import x53_monitor as M

    check_gate_bar()
    target = pins.TARGET
    layer = X.PREDICTED[target]
    for n, root in ((probe_name, P.RESULTS), (monitor_name, M.RESULTS)):
        pins.check_run_name(n)
        assert not (root / n).exists(), f"{n} exists"
    files = [CP.DATA / CP_SET / f"{d}_{CP_FAMILY}_{CP_LEVEL}.json" for d in CP_DOMAINS]
    out = P.RESULTS / probe_name
    out.mkdir(parents=True, exist_ok=False)
    m: dict[str, Any] = {
        "exp": P.EXP, "run": probe_name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": P.NOTE, "test": CP_TEST, "spec": SPEC, "prediction": NO_PREDICTION, "rule": CP_RULE, "source": None,
        "source_code": None, "set": f"code_pointer_v1/{CP_SET}/{CP_FAMILY}", "layer": layer, "x0_items": 0,
        "format": CP_FORMAT, "format_text": CP_TEXT, "gate": CP_GATE_TEXT, "read": READ_TEXT, "model": pins.model_pin(),
        "switches": switches(), "code": git_state(), "position": "the target chain's head key, base program",
        "inputs": {str(f.relative_to(pins.REPO_ROOT)): sha256_of(f) for f in files},
        "folds": {"outer": P.K_OUTER, "inner": P.K_INNER, "penalties": list(P.RELS)},
        "seeds": {"bootstrap": X.BOOT_SEED}, "targets": dict(P.TARGETS), "monitor_run": monitor_name}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    cases, counts = cp_cases(model.tokenizer)
    print(json.dumps(counts), flush=True)
    rows, h = read_org(model, cases, layer, "code_pointer_v1 CH2")
    by_domain = {d: gate_of([r for r, c in zip(rows, cases, strict=True) if c["domain"] == d], (X.LOOKUP,))
                 ["org_read_accuracy"] for d in CP_DOMAINS}  # fmt: skip
    gate = {**gate_of(rows, (X.LOOKUP,)), "rule": CP_GATE_TEXT, "per_domain": by_domain, "counts": counts}
    (out / "gate.json").write_text(json.dumps(gate, indent=1) + "\n")
    X.write_jsonl(out / "reads.jsonl", rows)
    print(f"{probe_name}: gate {gate['org_read_accuracy']} (per domain {by_domain}) -> {gate['status']}", flush=True)
    if gate["pass"]:
        assert h is not None
        h = h.astype(np.float16) if np.abs(h).max() < 6e4 else h
        np.savez_compressed(out / "states.npz", h=h, scene=np.array([c["scene"] for c in cases]))
        X.write_jsonl(out / "items.jsonl", [cp_probe_item(c) for c in cases])
    m.update({"gate_pass": gate["pass"], "cases": len(cases), "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    gate_m = {k: gate[k] for k in ("cases", "org_read_accuracy", "pass", "status", "per_domain")}
    extra = {"x53_7": {"test": CP_TEST, "spec": SPEC, "prediction": NO_PREDICTION, "rule": CP_RULE, "descriptive": True,
                       "formats": [CP_FORMAT], "format_text": {CP_FORMAT: CP_TEXT},
                       "gates": {CP_FORMAT: {**gate_m, "set": f"code_pointer_v1/{CP_SET} {CP_FAMILY} (every aligned scene)"}},
                       "states_for": [CP_FORMAT] if gate["pass"] else [], "probe_run": probe_name,
                       "items": f"the first {CP_MONITOR_PER_DOMAIN} aligned scenes per domain (x53_7.cp_monitor_items)"}}  # fmt: skip
    mon = M.stage_run(monitor_name, sets_run=(CP_FORMAT,) if gate["pass"] else (), model=model, extra=extra)
    return out, mon


def probe_bars(rows: list[dict], path: Path, title: str) -> None:
    """The probe and its baselines per target (and stratum present): bars with 95% CIs."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len({r["target"] for r in rows}), figsize=(11, 3.8), sharey=True, squeeze=False)
    for ax, target in zip(axes[0], dict.fromkeys(r["target"] for r in rows), strict=True):
        mine = [r for r in rows if r["target"] == target]
        for j, r in enumerate(mine):
            for k, (key, col) in enumerate((("probe", "#4a6fa5"), ("majority", "#bdbdbd"), ("structure", "#c27c0e"),
                                            ("layout", "#7a4ea3"))):  # fmt: skip
                if key in r:
                    v = r[key]
                    ax.bar(j + 0.2 * k - 0.3, v[0], 0.18, color=col, yerr=[[v[0] - v[1]], [v[2] - v[0]]], capsize=2,
                           label=key if j == 0 else None)  # fmt: skip
            ax.plot([j - 0.4, j + 0.4], [r["chance"]] * 2, color="black", lw=1, ls="--")
        ax.set_xticks(range(len(mine)), [f"{r['stratum']} (n {r['n']})" for r in mine])
        ax.set_title(target, fontsize=10)
        ax.set_ylim(0, 1.05)
    axes[0][0].set_ylabel("cross-validated accuracy")
    axes[0][0].legend(fontsize=8, frameon=False)
    fig.suptitle(f"{title} (dashed: chance; descriptive; UNVERIFIED)", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=130, facecolor="white")
    plt.close(fig)


def monitor_numbers_figure(results: dict, s: str, path: Path) -> None:
    """53.2's panels without any label: accuracy by layer per target (columns) and model x position (rows); full,
    J++_k, random_k, PCA_k (k = 25 solid, 100 dashed), chance dotted."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts import x53_monitor as M

    col = {"full": "#111111", "jpp": "#6a4bd6", "rand": "#9a9a9a", "pca": "#009e73", "chance": "#cccccc",
           "fix": "#c27c0e", "erand": "#d1495b"}  # fmt: skip
    rows = [(t, p) for t in M.MODELS if s in results.get(t, {}) for p in M.PROBE_POS]
    fig, axes = plt.subplots(len(rows), len(M.TARGETS), figsize=(13, 2.3 * len(rows) + 1.2), sharey=True, squeeze=False)
    for i, (t, p) in enumerate(rows):
        res = results[t][s]
        for j, tg in enumerate(M.TARGETS):
            ax, feats = axes[i][j], res["acc"][f"{p}|{tg}"]
            ax.plot(res["layers"], feats["chance"]["acc"], ":", color=col["chance"])
            ax.plot(res["layers"], feats["full"]["acc"], "-", color=col["full"], lw=1.8)
            for k, ls in zip(M.KS, ("-", "--"), strict=True):
                for fam in ("rand", "pca", "erand", "fix", "jpp"):  # fix / erand: 53.2's arms beside, if they ran
                    if f"{fam}{k}" in feats:
                        ax.plot(res["layers"], feats[f"{fam}{k}"]["acc"], ls, color=col[fam], lw=1.4)
            ax.set_title(M.TARGET_SHORT[tg], fontsize=8.5)
            ax.set_ylim(-0.02, 1.02)
            if j == 0:
                ax.set_ylabel(f"{M.NAMES[t]}\n{'bridge word' if p == 'B' else 'last token'}", fontsize=9)
    fig.suptitle(f"{CP_TEST}: probe accuracy by layer (numbers only, no label; full black, J++ purple, random grey, PCA "
                 "green, beside where run: fixed J++ amber, energy-matched random red; k = 25 solid, 100 dashed; "
                 "UNVERIFIED)", fontsize=9)  # fmt: skip
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=110, facecolor="white")
    plt.close(fig)


def stage_cp_monitor_report(names: list[str], n_boot: int = X.N_BOOT) -> Path:
    """CH2's monitor numbers (x53_monitor.summarize: per-layer accuracies and CIs), no label;
    results/x53_monitor/x53_7_cp_monitor-<UTC>/."""
    from scripts import x53_monitor as M

    results: dict[str, dict] = {}
    status = []
    for name in names:
        m = json.loads((M.RESULTS / name / "manifest.json").read_text())
        target, g = m["model"]["target"], m["x53_7"]["gates"][CP_FORMAT]
        rec = {
            "run": name,
            "model": target,
            "format": CP_FORMAT,
            "gate": g,
            "status": "tested" if g["pass"] else g["status"],
        }
        if g["pass"]:
            pr = M.load_probes(name, CP_FORMAT)
            assert pr is not None, f"{name}: no probes in {M.CACHE / name}: run x53_monitor.py probe first"
            summ = M.summarize(pr, n_boot)
            summ.pop("rules")  # numbers only (Dan: descriptive); the rule is not applied to CH2
            results.setdefault(target, {})[CP_FORMAT] = summ
        status.append(rec)
    out = M.RESULTS / f"x53_7_cp_monitor-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    figs = []
    if results:
        monitor_numbers_figure(results, CP_FORMAT, out / "x53_7_cp_monitor.png")
        figs.append("x53_7_cp_monitor.png")
    blob = {"test": CP_TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": CP_RULE,
            "gate": CP_GATE_TEXT, "format_text": {CP_FORMAT: CP_TEXT}, "runs": status, "figures": figs,
            "n_boot": n_boot, "results": results, "written_utc": utc()}  # fmt: skip
    (out / "x53_7_cp_monitor.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {CP_TEST}: the monitor (53.2's probes; numbers only)", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             f"Rule: {CP_RULE}.", "", f"Gate: {CP_GATE_TEXT}.", "", f"- {CP_TEXT}.", "",
             "| model | gate (lookup; per domain) | status |", "|---|---|---|"]  # fmt: skip
    for s in status:
        lines.append(f"| {M.NAMES.get(s['model'], s['model'])} | {s['gate']['org_read_accuracy']} "
                     f"{s['gate'].get('per_domain', '')} | {s['status']} |")  # fmt: skip
    lines += ["", "## Best layer per cell (accuracy [95% CI]; no label)", "",
              "| model | position | target | full (layer) | J++25 | random25 | J++100 | random100 | PCA25 | chance | "
              "fixed J++25 / 100 (beside) | energy-matched random25 / 100 (beside) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t, per in results.items():
        r = per[CP_FORMAT]
        for p in M.PROBE_POS:
            for tg in M.TARGETS:
                f = r["acc"][f"{p}|{tg}"]
                li = int(np.argmax(f["full"]["acc"]))
                best = lambda key, f=f: M.fmt_acc(f[key], int(np.argmax(f[key]["acc"]))) if key in f else "-"  # noqa: E731
                side = [" / ".join(best(f"{fam}{k}") for k in M.KS) for fam in ("fix", "erand")]
                lines.append(f"| {M.NAMES[t]} | {p} | {M.TARGET_SHORT[tg]} | {M.fmt_acc(f['full'], li)} (L{r['layers'][li]}) | "
                             + " | ".join(best(k) for k in ("jpp25", "rand25", "jpp100", "rand100", "pca25", "chance"))
                             + f" | {side[0]} | {side[1]} |")  # fmt: skip
    lines += ["", "Each column's best layer (full: the layer named). (d) at the last token is read on the lookup's prompt "
              "(CH2 has no recall prompt).", ""]  # fmt: skip
    lines += report_lines("x53_monitor (code_pointer_v1 CH2, descriptive)", status, "numbers only: per target and "
                          "position the J++ probe beside the random subspace and the full residual, no label",
                          "x53_7_cp_monitor.json: results[<model>]['cp_ch2']['acc']; the probes in "
                          "cache/x53_monitor/<run>/cp_ch2.npz (x53_monitor.py probe)")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out}", flush=True)
    return out


# ---- plan (tokenizer only) ----------------------------------------------------------------------------------------


def stage_plan() -> dict:
    """Per format: the routes test's scenes and drops, the address probe's aligned scenes, the monitor's main items and
    its gate set's aligned scenes, for BJ_TARGET's tokenizer."""
    from scripts import x6_routes as R
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    blob: dict[str, Any] = {"target": target, "layer": X.PREDICTED[target]}
    for fmt in FORMATS:
        cases, dropped = R.scenes(tok, R.N_GEN, fmt=fmt)
        probe, probe_counts = build_cases(tok, PROBE_SET, fmt)
        gate_cases, gate_counts = build_cases(tok, main_set(target), fmt)
        items, item_counts = main_items(tok, target, fmt)
        blob[fmt] = {"routes": {"cases": dict(collections.Counter(c["condition"] for c in cases)),
                                "dropped": dict(dropped), "animals": len({c["bridge"] for c in cases})},
                     "probe": probe_counts, "monitor_gate": gate_counts, "monitor_items": item_counts,
                     "tokens": {"routes_C2": len(next(c for c in cases if c["condition"] == "C2")["readers"][X.LOOKUP]["ids"]["org"]),
                                "probe": len(probe[0]["readers"][X.LOOKUP]["ids"]["org"]) if probe else None}}  # fmt: skip
        del gate_cases, items
    print(json.dumps(blob, indent=1))
    return blob


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan", help="tokenizer only: counts and drops per format for BJ_TARGET")
    p = sub.add_parser("probe-run", help="GPU: the address probe's gate and states per format")
    p.add_argument("--name", required=True, help="the run's base name; one run per format, <name>_<format>")
    p.add_argument("--formats", default=",".join(FORMATS))
    p.add_argument("--hollow", default="", help=f"formats labelled '{HOLLOW}' (Dan 12:25), comma-separated")
    p = sub.add_parser("monitor-run", help="GPU: the monitor's gate per format, then its states (x53_monitor)")
    p.add_argument("--name", required=True)
    p.add_argument("--formats", default=",".join(FORMATS))
    for cmd in ("routes-verdict", "probe-verdict", "monitor-verdict", "cp-probe-report", "cp-monitor-report"):
        p = sub.add_parser(cmd, help="CPU: the verdict (cp-*: numbers only) into results/<exp>/x53_7_<test>-<UTC>/")
        p.add_argument("--names", required=True, help="the runs, comma-separated")
        p.add_argument("--n-boot", type=int, default=X.N_BOOT)
    sub.add_parser("cp-plan", help="tokenizer only: code_pointer_v1 CH2's aligned scenes and monitor items")
    p = sub.add_parser("cp-run", help="GPU: CH2's gate and probe states, then its monitor states (descriptive)")
    p.add_argument("--probe-name", required=True)
    p.add_argument("--monitor-name", required=True)
    p = sub.add_parser("monitor-atoms", help="GPU: the fixed J++ arm's atom vectors for a 53.7 monitor run")
    p.add_argument("--source", required=True, help="the 53.7 monitor run (writes results/x53_monitor/<source>_atoms/)")
    a = ap.parse_args()
    if a.cmd == "plan":
        stage_plan()
    elif a.cmd == "monitor-atoms":
        stage_monitor_atoms(a.source)
    elif a.cmd == "cp-plan":
        from scripts import x45m

        tok = x45m.tokenizer()
        cases, _ = cp_cases(tok)
        _, item_counts = cp_monitor_items(tok, pins.TARGET)
        print(json.dumps({**item_counts, "prompt_tokens": len(cases[0]["readers"][X.LOOKUP]["ids"]["org"])}, indent=1))
    elif a.cmd == "cp-run":
        stage_cp_run(a.probe_name, a.monitor_name)
    elif a.cmd == "cp-probe-report":
        stage_probe_verdict(a.names.split(","), a.n_boot, prefix="x53_7_cp_probe")
    elif a.cmd == "cp-monitor-report":
        stage_cp_monitor_report(a.names.split(","), a.n_boot)
    elif a.cmd == "probe-run":
        stage_probe_run(a.name, tuple(a.formats.split(",")), hollow=tuple(f for f in a.hollow.split(",") if f))
    elif a.cmd == "monitor-run":
        stage_monitor_run(a.name, tuple(a.formats.split(",")))
    elif a.cmd == "routes-verdict":
        stage_routes_verdict(a.names.split(","), a.n_boot)
    elif a.cmd == "probe-verdict":
        stage_probe_verdict(a.names.split(","), a.n_boot)
    else:
        stage_monitor_verdict(a.names.split(","), a.n_boot)


if __name__ == "__main__":
    main()
