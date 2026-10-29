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
            for w in X.READERS:
                rd = c["readers"][w]
                rec = (layer,) if layer is not None and w == X.LOOKUP else ()
                ids = torch.tensor([rd["ids"]["org"] + c["space"]], device=model.device)
                logits, got = model.run(ids, record=rec)
                top = int(logits.argmax())
                rows.append({"scene": c["scene"], "reader": w, "top": top, "read_right": top == rd["tok_A"]})
                if rec:
                    states.append(got[rec[0]][c["pos"]].float().cpu().numpy())
    return rows, (np.stack(states) if states else None)


def gate_of(rows: list[dict]) -> dict:
    """X0's gate (x0_necessity.gate_and_eligible's pass): per reader the share of O prompts read right (rounded to 4
    places as X0's org_rate), passing iff both are >= GATE_BAR."""
    acc = {w: round(float(np.mean([r["read_right"] for r in rows if r["reader"] == w])), 4) for w in X.READERS
           if any(r["reader"] == w for r in rows)}  # fmt: skip
    ok = len(acc) == len(X.READERS) and all(a >= GATE_BAR for a in acc.values())
    return {"cases": len({r["scene"] for r in rows}), "org_read_accuracy": acc, "bar": GATE_BAR, "pass": ok,
            "status": "passed" if ok else not_tested(acc), "rule": GATE_TEXT}  # fmt: skip


def stage_probe_run(base: str, formats: tuple[str, ...] = FORMATS, set_name: str = PROBE_SET) -> list[Path]:
    """The address probe's forwards per format into results/x0_probe/<base>_<format>/ (x0_probe's run layout:
    manifest.json, states.npz, items.jsonl; plus gate.json, reads.jsonl): every aligned scene of the set, the gate
    first; states and items only if the format passes."""
    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import x0_probe as P

    check_gate_bar()
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
            "gate": GATE_TEXT, "read": READ_TEXT, "model": pins.model_pin(), "switches": switches(), "code": git_state(),
            "position": f"the asked person's bridge word, org run, {fmt}",
            "inputs": {str(items_file.relative_to(pins.REPO_ROOT)): sha256_of(items_file)},
            "folds": {"outer": P.K_OUTER, "inner": P.K_INNER, "penalties": list(P.RELS)},
            "seeds": {"bootstrap": X.BOOT_SEED}, "targets": dict(P.TARGETS)}  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
        cases, counts = build_cases(model.tokenizer, set_name, fmt)
        print(json.dumps(counts), flush=True)
        rows, h = read_org(model, cases, layer, f"{set_name} {fmt}")
        gate = {**gate_of(rows), "counts": counts}
        (out / "gate.json").write_text(json.dumps(gate, indent=1) + "\n")
        X.write_jsonl(out / "reads.jsonl", rows)
        print(f"{name}: gate {gate['org_read_accuracy']} -> {gate['status']}", flush=True)
        if gate["pass"]:
            assert h is not None
            h = h.astype(np.float16) if np.abs(h).max() < 6e4 else h  # x0_probe's storage
            np.savez_compressed(out / "states.npz", h=h, scene=np.array([c["scene"] for c in cases]))
            X.write_jsonl(out / "items.jsonl", [{**P.item_of(c, False), "context": c["context"]} for c in cases])
        m.update({"gate_pass": gate["pass"], "cases": len(cases), "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
        outs.append(out)
    return outs


def stage_monitor_run(name: str, formats: tuple[str, ...] = FORMATS) -> Path:
    """The gate per format over every aligned scene of the main test's set, then x53_monitor.stage_run (same model) on
    the main test's items in each format that passes; the gate goes into the run's manifest (x53_7)."""
    from bridge_jspace.model import load_model
    from scripts import x53_monitor as M

    check_gate_bar()
    target = pins.TARGET
    pins.check_run_name(name)
    assert not (M.RESULTS / name).exists(), f"{name} exists"
    gate_set = main_set(target)
    model = load_model()
    gates, reads = {}, {}
    for fmt in formats:
        cases, counts = build_cases(model.tokenizer, gate_set, fmt)
        reads[fmt], _ = read_org(model, cases, None, f"{gate_set} {fmt}")
        gates[fmt] = {**gate_of(reads[fmt]), "set": gate_set, "counts": counts}
        print(f"{fmt}: gate {gates[fmt]['org_read_accuracy']} -> {gates[fmt]['status']}", flush=True)
    passing = tuple(f for f in formats if gates[f]["pass"])
    extra = {"x53_7": {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "formats": list(formats),
                       "format_text": {f: FORMAT_TEXT[f] for f in formats}, "gates": gates, "states_for": list(passing),
                       "items": "the main test's items (x53_monitor main) rendered in the format; x53_7.main_items"}}  # fmt: skip
    out = M.stage_run(name, sets_run=passing, model=model, extra=extra)
    for fmt, rows in reads.items():
        X.write_jsonl(out / f"x53_7_gate_reads_{fmt}.jsonl", rows)
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
                     "cells": cells})  # fmt: skip
    out = R.RESULTS / f"x53_7_routes-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    rule = f"a route counts as used if its share is >= {R.USED_SHARE} with lower CI >= {R.USED_LO}"
    blob = {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": rule,
            "c0_rule": f"C0 must reproduce the one-pick lookup switch rate within {R.C0_TOL}, or the run stops",
            "gate": f"per condition, O's read accuracy >= {GATE_BAR} per reader (x6_routes' gate)", "n_boot": n_boot,
            "seed": X.BOOT_SEED, "format_text": FORMAT_TEXT, "runs": runs, "written_utc": utc()}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {TEST}: the routes test in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             f'Rule (the routes test\'s, verbatim): "{rule[0].upper() + rule[1:]}." The C0 sanity swap must reproduce the '
             f"one-pick lookup switch rate within {R.C0_TOL}, or the run stops. Gate per condition: O's read accuracy "
             f">= {GATE_BAR} per reader; a failed condition is not tested. Cluster bootstrap over the bridge item "
             f"({n_boot:,} resamples, seed {X.BOOT_SEED}). C1: identity = original (both a).", "",
             *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
             "| model | format | condition | status | gate (lookup / recall) |", "|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        for cond, st in r["status"].items():
            acc = r["gate"]["gate"][cond]["org_read_accuracy"]
            lines.append(f"| {MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | {cond} | {st} | "
                         f"{acc.get(X.LOOKUP, float('nan')):.3f} / {acc.get(X.RECALL, float('nan')):.3f} |")  # fmt: skip
        if r["c0_check"]:
            c = r["c0_check"]
            lines.append(f"| | | C0 check | {'ok' if c['ok'] else 'failed: the run stops'} | lookup switch "
                         f"{c['c0_lookup_switch']:.3f} vs reference {c['reference']} |")  # fmt: skip
    lines += ["", "## Route shares of the lookup per arm (the rule's 'used' routes at the right)", "",
              "| model | format | condition | arm | n | identity | position | value | original | other | recall "
              "follows S | used |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
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
    fig, axes = plt.subplots(len(runs), 2, figsize=(12, 2.9 * len(runs) + 1.0), squeeze=False, sharex=True)
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
            ax.set_yticks(range(len(arms)), [ARM_TEXT[a] for a in arms], fontsize=7.5)
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


def stage_probe_verdict(names: list[str], n_boot: int = X.N_BOOT) -> Path:
    """The address probe per run (model x format): the gate, then x0_probe.score per stratum and target (every scene of
    the run), Dan's reading verbatim, the prose v4 run beside; results/x0_probe/x53_7_probe-<UTC>/."""
    from scripts import x0_probe as P

    out = P.RESULTS / f"x53_7_probe-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    runs = []
    for name in names:
        src = P.RESULTS / name
        m = json.loads((src / "manifest.json").read_text())
        gate = json.loads((src / "gate.json").read_text())
        rec: dict[str, Any] = {"run": name, "model": m["model"]["target"], "format": m["format"], "layer": m["layer"],
                               "set": m["set"], "gate": gate, "status": gate["status"] if not gate["pass"] else "tested"}  # fmt: skip
        if gate["pass"]:
            z = np.load(src / "states.npz")
            h, scenes = z["h"].astype(np.float64), [str(s) for s in z["scene"]]
            items = X.read_jsonl(src / "items.jsonl")
            assert [it["scene"] for it in items] == scenes, f"{name}: items.jsonl and states.npz disagree"
            for it in items:
                it["layout"] = P.layout(it["context"], it["pick_index"])
            rows = []
            for stratum in P.STRATA:
                idx = [i for i, it in enumerate(items) if stratum == "both" or it["order"] == stratum]
                for target in P.TARGETS:
                    rows.append({"subset": "all", "stratum": stratum, "target": target,
                                 **P.score(h[idx], [items[i] for i in idx], target, n_boot)})  # fmt: skip
            rec["rows"] = rows
            (out / name).mkdir()
            (out / name / "probe.json").write_text(json.dumps({"run": name, "manifest": m, "note": P.NOTE, "rows": rows},
                                                              indent=1) + "\n")  # fmt: skip
            P.figures(out / name)
        rec["prose_v4"], rec["prose_v4_rows"] = prose_v4_rows(rec["model"])
        runs.append(rec)
    blob = {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "reading": PROBE_READING,
            "rule": "none of its own (descriptive, x0_probe); the reading stated beside, verbatim", "gate": GATE_TEXT,
            "n_boot": n_boot, "seed": X.BOOT_SEED, "format_text": FORMAT_TEXT, "runs": runs, "written_utc": utc()}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {TEST}: the address probe in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             "Rule: none of its own (x0_probe v4 is descriptive, added after the data). " + PROBE_READING, "",
             f"Gate (53.7): {GATE_TEXT}.", "", *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
             "| model | format | layer | aligned scenes | gate (lookup / recall) | status |", "|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        acc = r["gate"]["org_read_accuracy"]
        lines.append(f"| {MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | L{r['layer']} | {r['gate']['cases']} | "
                     f"{acc.get(X.LOOKUP, float('nan')):.3f} / {acc.get(X.RECALL, float('nan')):.3f} | {r['status']} |")  # fmt: skip
    lines += ["", "## Probe accuracy (every scene of the run; folds by bridge entity for (a), (b), by item for (c))", "",
              "| model | format | locker vs pick | target | n | entities | classes | probe | majority | chance | structure "
              "| layout | probe - best baseline | prose v4 probe (beside) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in runs:
        prose = {(p["stratum"], p["target"]): p["probe"] for p in r["prose_v4_rows"] if p["subset"] == "all"}
        for p in r.get("rows", []):
            lines.append(f"| {MODEL_NAME.get(r['model'], r['model'])} | {r['format']} | {p['stratum']} | {p['target']} | "
                         f"{p['n']} | {p['entities']} | {p['classes']} | {fmt_ci(p['probe'])} | {fmt_ci(p['majority'])} | "
                         f"{p['chance']:.2f} | {fmt_ci(p['structure']) if 'structure' in p else '-'} | "
                         f"{fmt_ci(p['layout']) if 'layout' in p else '-'} | {fmt_ci(p['probe_minus_best'])} "
                         f"({p['best_baseline']}) | {fmt_ci(prose[(p['stratum'], p['target'])]) if (p['stratum'], p['target']) in prose else '-'} |")  # fmt: skip
    lines += report_lines("x0_probe (53.7 address probe)", runs, "probe (b), which locker sentence, locker before the "
                          "pick, against the best baseline (layout / pick index / majority); the locker-after stratum "
                          "is the control", "verdict.json: runs[].rows (stratum 'before', target 'locker sentence'); "
                          "rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}")  # fmt: skip
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
            g = x["gates"][fmt]
            rec = {"run": name, "model": target, "format": fmt, "gate": {k: g[k] for k in ("cases", "org_read_accuracy", "pass", "status", "set")}}  # fmt: skip
            if g["pass"]:
                pr = M.load_probes(name, fmt)
                assert pr is not None, f"{name} {fmt}: no probes in {M.CACHE / name}: run x53_monitor.py probe first"
                results.setdefault(target, {})[fmt] = M.summarize(pr, n_boot)
                rec["status"] = "tested"
            else:
                rec["status"] = g["status"]
            status.append(rec)
    out = M.RESULTS / f"x53_7_monitor-{utc()}"
    out.mkdir(parents=True, exist_ok=False)
    figs = []
    for fmt in FORMATS:
        if any(fmt in r for r in results.values()):
            M.figure(results, fmt, out / f"x53_7_monitor_{fmt}.png")
            figs.append(f"x53_7_monitor_{fmt}.png")
    blob = {"test": TEST, "spec": SPEC, "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": M.RULE,
            "gate": GATE_TEXT, "format_text": FORMAT_TEXT, "runs": status, "figures": figs, "n_boot": n_boot,
            "results": results, "written_utc": utc()}  # fmt: skip
    (out / "x53_7_monitor.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = [f"# {TEST}: the monitor test (53.2) in code and tool output", "", f"{NO_PREDICTION}. Spec: {SPEC}.", "",
             f"Rule (53.2's, verbatim): {M.RULE}", "", f"Gate (53.7): {GATE_TEXT}.", "",
             *(f"- {f}: {t}." for f, t in FORMAT_TEXT.items()), "",
             "| model | format | gate set | gate (lookup / recall) | status |", "|---|---|---|---|---|"]  # fmt: skip
    for s in status:
        acc = s["gate"]["org_read_accuracy"]
        lines.append(f"| {M.NAMES.get(s['model'], s['model'])} | {s['format']} | {s['gate']['set']} "
                     f"({s['gate']['cases']} scenes) | {acc.get(X.LOOKUP, float('nan')):.3f} / "
                     f"{acc.get(X.RECALL, float('nan')):.3f} | {s['status']} |")  # fmt: skip
    lines += ["", "## Labels (53.2's rule per position, target and k)", "",
              "| model | format | position | target | k = 25 | k = 100 | full max | J++25 max (gap max) | J++100 max (gap max) |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in M.MODELS:
        for fmt, r in results.get(t, {}).items():
            for p in M.PROBE_POS:
                for tg in M.TARGETS:
                    ru = r["rules"][f"{p}|{tg}"]
                    lines.append(f"| {M.NAMES[t]} | {fmt} (n {r['n_rows']} rows, {r['n_entities']} entities) | {p} | "
                                 f"{M.TARGET_TEXT[tg]} | {ru['k25']['label']} | {ru['k100']['label']} | "
                                 f"{ru['k25']['full_max']:.2f} | {ru['k25']['jpp_max']:.2f} ({ru['k25']['gap_max']:+.2f}) | "
                                 f"{ru['k100']['jpp_max']:.2f} ({ru['k100']['gap_max']:+.2f}) |")  # fmt: skip
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
    p = sub.add_parser("monitor-run", help="GPU: the monitor's gate per format, then its states (x53_monitor)")
    p.add_argument("--name", required=True)
    p.add_argument("--formats", default=",".join(FORMATS))
    for cmd in ("routes-verdict", "probe-verdict", "monitor-verdict"):
        p = sub.add_parser(cmd, help="CPU: the verdict into results/<exp>/x53_7_<test>-<UTC>/")
        p.add_argument("--names", required=True, help="the runs, comma-separated")
        p.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.cmd == "plan":
        stage_plan()
    elif a.cmd == "probe-run":
        stage_probe_run(a.name, tuple(a.formats.split(",")))
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
