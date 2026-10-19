"""exp20_competence: can Qwen3.6-27B do part B's tasks, unedited, in the format each run feeds it and in its chat format?

Every part B run gates on items the model gets right (exp02: the clean answer; exp04/07: brew's answer; exp09: B, C and
O all answered). The gate keeps each run's items correct one by one but says nothing about the base rate: a task the
model does on half its items is a task it partly guesses, and the gated half can be the easy or shortcut half. Before
new runs (Phase 2/3) this measures, with no edits and greedy decoding, the accuracy per task and format, and hop by hop
where the item names its hops.

Tasks (the pinned item files, every item):
  probe_swap      B1's 90 two-hop facts (data/probe_swap.json)                   judged as exp13 (C, not ambiguous)
  brew_bank       brew's gated bank (data/brew_intermediates.json, 100)           the first palette colour, as exp03
  brew_fresh      ungated, exp03_make_items seed 1 (data/brew_fresh.json, 200)
  brew_test       ungated (data/brew_test.json, 600)
  R, B            bind_recall: the city recalled / the person bound -> capital    the first capital of the set, as exp09
  L               bind_lookup_v2: the person bound -> the in-context colour table the first palette colour
  RL              recall_lookup: the city recalled -> the colour table
Formats:
  raw            as the part B runs feed them: raw text, no chat template (probe_swap with the trailing space stripped,
                 as exp02's main runs; exp09's prompts as they are). Brew has no raw format (its runs use chat_prefill).
  chat           the chat template, thinking off, the assistant turn left empty. The statement to complete becomes a
                 question ("The capital of the country where Lyon is located is" -> "What is the capital of the country
                 where Lyon is located?"), after the same context, then " Answer with a single word and nothing else."
                 Brew's prompt is already a question with its own instruction and is used as it is. probe_swap's
                 endings are too varied for a question ("is called a", "border with", "the rider's"): its sentence,
                 without "Fact: ", follows "Fill in the blank. Answer with only the missing word or words and nothing
                 else." and a blank line, and ends " ___".
  chat_prefill   as chat, with the assistant turn prefilled "Answer:" (brew's format: exp03's render)
Prompts per item:
  clean          the item's prompt
  cf, off        exp09 only: its C (the bridge set to X) and O (X's and Z's holders swapped, off the path) prompts, the
                 same texts exp09's eligibility runs (R: the first city of X that keeps the tokens aligned, or the
                 first city of X when none does)
  hop1           the first hop alone. exp09: "<context> <city> is located in" (R, RL) / "<context> <person> lives in"
                 (B, L) -> the bridge (chat: "In which country is <city> located?" / "In which country does <person>
                 live?"); brew: "You stir the potion once." -> the intermediate
  hop2           the second hop given the bridge. exp09: "<context> The capital of <bridge> is" (R, B) / "<context>
                 <bridge>'s colour is" (L, RL); brew: once, starting from the intermediate -> the answer
  probe_swap names its bridge but not its hops' wording, so it has no hop prompts.
"""

import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from bridge_jspace.tokens import raw_encoding
from bridge_jspace.utils import git_state
from scripts.exp03_brew_swaps import PREFILL, answer_colour, write_jsonl
from scripts.exp03_make_items import PALETTE
from scripts.exp09_bind_recall import RECALLED, USE_SOURCE, variants, x_cities
from scripts.exp09_make_items import CAPITALS, LANDMARKS
from scripts.exp13_greedy_answers.experiment import judge

EXP = "exp20_competence"
RESULTS = pins.RESULTS_DIR / EXP
FORMATS = ("raw", "chat", "chat_prefill")
KINDS = ("clean", "cf", "off", "hop1", "hop2", "hop3")
INSTRUCTION = "Answer with a single word and nothing else."
BLANK_INSTRUCTION = "Fill in the blank. Answer with only the missing word or words and nothing else."
MAX_NEW_TOKENS = 16
BATCH = 64  # prompts of one token length per generate_batch call
RELIABLE_LOWER = 0.85  # reading aid only: a cell is called reliable if its Wilson 95% lower bound is at least this
COUNTRIES = tuple(c.lower() for c in CAPITALS)
CAPITAL_WORDS = tuple(c.lower() for c in CAPITALS.values())
CITY_WORDS = tuple(c.lower() for c in LANDMARKS.values())
# task -> (pinned file, sha256, loader, family filter or None)
TASKS: dict[str, tuple[Path, str, Any, str | None]] = {
    "probe_swap": (pins.PROBE_SWAP_FILE, pins.PROBE_SWAP_SHA256, pins.probe_swap_items, None),
    "brew_bank": (pins.BREW_FILE, pins.BREW_SHA256, pins.brew_items, None),
    "brew_fresh": (pins.BREW_FRESH_FILE, pins.BREW_FRESH_SHA256, pins.brew_fresh_items, None),
    "brew_test": (pins.BREW_TEST_FILE, pins.BREW_TEST_SHA256, pins.brew_test_items, None),
    "R": (pins.BIND_RECALL_FILE, pins.BIND_RECALL_SHA256, pins.bind_recall_items, "R"),
    "B": (pins.BIND_RECALL_FILE, pins.BIND_RECALL_SHA256, pins.bind_recall_items, "B"),
    "L": (pins.BIND_LOOKUP_V2_FILE, pins.BIND_LOOKUP_V2_SHA256, pins.bind_lookup_v2_items, "L"),
    "RL": (pins.RECALL_LOOKUP_FILE, pins.RECALL_LOOKUP_SHA256, pins.recall_lookup_items, "RL"),
    **{f: (pins.USE_SOURCE_FILE, pins.USE_SOURCE_SHA256, pins.use_source_items, f) for f in USE_SOURCE},
}
AS_RUN = (
    {"probe_swap": "raw", "R": "raw", "B": "raw", "L": "raw", "RL": "raw"}
    | dict.fromkeys(USE_SOURCE, "chat_prefill")
    | {t: "chat_prefill" for t in ("brew_bank", "brew_fresh", "brew_test")}
)


def lower_the(s: str) -> str:
    return "the" + s[3:] if s.startswith("The ") else s


def as_question(statement: str) -> str:
    """A statement to complete as a question: 'The capital of X is' -> 'What is the capital of X?'."""
    s = statement.strip().removeprefix("Fact: ")
    if m := re.fullmatch(r"(.*) is located in", s):
        return f"In which country is {m[1]} located?"
    if m := re.fullmatch(r"(.*) lives in", s):
        return f"In which country does {m[1]} live?"
    if m := re.fullmatch(r"(.*) has the colour", s):
        return f"What colour does {lower_the(m[1])} have?"
    m = re.fullmatch(r"(.*) (is|was)(?: the)?", s)
    assert m, f"no question form for {statement!r}"
    return f"What {m[2]} {lower_the(m[1])}?"


def split_context(text: str) -> tuple[str, str]:
    """(context, the statement to complete): the statement is the text after the last sentence end."""
    cut = text.rfind(". ")
    return ("", text) if cut < 0 else (text[: cut + 1], text[cut + 2 :])


def chat_text(tokenizer, content: str, prefill: bool) -> str:
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": content}], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    return text + PREFILL if prefill else text


def render(tokenizer, task: str, fmt: str, text: str) -> list[int] | None:
    """Token ids of a prompt in a format (None: the task has no such format)."""
    brew = task.startswith("brew")
    if fmt == "raw":
        if brew:
            return None
        return raw_encoding(tokenizer, text.rstrip() if task == "probe_swap" else text)["input_ids"]
    if brew:
        content = text
    elif task == "probe_swap":  # endings vary too much for a question ("is called a", "border with", "the rider's")
        content = f"{BLANK_INSTRUCTION}\n\n{text.strip().removeprefix('Fact: ')} ___"
    else:
        ctx, statement = split_context(text)
        content = f"{ctx} {as_question(statement)}".strip() + " " + INSTRUCTION
    return tokenizer(chat_text(tokenizer, content, fmt == "chat_prefill"), add_special_tokens=False).input_ids


def first_ids(tokenizer, word: str, fmt: str) -> list[int]:
    """The answer's first token as written, capitalised and lowercase, with the space the format puts before it (none
    at the start of a chat reply; one after raw text or 'Answer:')."""
    space = "" if fmt == "chat" else " "
    return sorted(
        {tokenizer(space + w, add_special_tokens=False).input_ids[0] for w in {word, word.capitalize(), word.lower()}}
    )


def exp09_texts(item: dict, index: int, tokenizer) -> dict[str, tuple[str, str]]:
    """kind -> (prompt text, expected answer) for an exp09 item; cf and off as exp09's prepare picks them."""
    family = item["family"]
    city2 = None
    if family in RECALLED:
        n = len(raw_encoding(tokenizer, item["prompt"])["input_ids"])
        fits = [
            c
            for c in x_cities(item, index)
            if len(raw_encoding(tokenizer, variants(item, index, c)["cf"])["input_ids"]) == n
        ]
        city2 = fits[0] if fits else None
    v = variants(item, index, city2)
    ctx = split_context(item["prompt"])[0]
    where = f"{item['cue']} is located in" if family in RECALLED else f"{item['cue']} lives in"
    texts = {
        "clean": (item["prompt"], item["answer"]),
        "cf": (v["cf"], item["target_answer"]),
        "off": (v["off"], item["answer"]),
        "hop1": (f"{ctx} {where}", item["bridge"]),
    }
    if family in ("LM", "RM"):  # the bridge's landmark (looked up), then the landmark's city (recalled)
        landmark = item["mid"][item["bridge"]]
        texts["hop2"] = (f"{ctx} {item['bridge']}'s landmark is", landmark)
        texts["hop3"] = (f"{ctx} The city where {landmark} stands is", item["answer"])
    elif family in ("BT", "RT"):  # the bridge's capital (recalled), then the capital's colour (looked up)
        capital = item["mid"][item["bridge"]]
        texts["hop2"] = (f"{ctx} The capital of {item['bridge']} is", capital)
        texts["hop3"] = (f"{ctx} {capital}'s colour is", item["answer"])
    else:
        second = f"The capital of {item['bridge']} is" if family in ("R", "B") else f"{item['bridge']}'s colour is"
        texts["hop2"] = (f"{ctx} {second}", item["answer"])
    return texts


def brew_texts(item: dict) -> dict[str, tuple[str, str]]:
    prompt, start, inter = item["prompt"], item["start"], item["intermediates"][0]
    twice, starts = "You stir the potion twice.", f"The potion starts out {start}."
    assert prompt.count(twice) == 1, item["name"]
    assert prompt.count(starts) == 1, item["name"]
    once = prompt.replace(twice, "You stir the potion once.")
    return {
        "clean": (prompt, item["answer"]),
        "hop1": (once, inter),
        "hop2": (once.replace(starts, f"The potion starts out {inter}."), item["answer"]),
    }


def other_answers(task: str, kind: str, item: dict) -> dict[str, str]:
    """Named wrong answers an exp09 or brew continuation can give (its role when wrong)."""
    if task in USE_SOURCE:
        if kind == "hop1":
            return {"bridge": item["bridge"], "target": item["target"], "third": item["third"]}
        table = item["mid"] if kind == "hop2" else item["values"]
        return {r: table[item[r]] for r in ("bridge", "target", "third")}
    if task in ("R", "B", "L", "RL"):
        value = (lambda c: CAPITALS[c]) if task in ("R", "B") else (lambda c: item["colours"][c])
        if kind == "hop1":
            return {"bridge": item["bridge"], "target": item["target"], "third": item["third"]}
        return {"bridge": value(item["bridge"]), "target": value(item["target"]), "third": value(item["third"])}
    if task.startswith("brew"):
        return {"answer": item["answer"], "intermediate": item["intermediates"][0], "start": item["start"]}
    return {}


def score(task: str, kind: str, item: dict, expected: str, text: str) -> dict:
    if task == "probe_swap":
        v = judge(text, item["answer"], item["swap_answer"])
        return {"said": v["match"], "correct": bool(v["C"] and not v["ambiguous"]), "ambiguous": v["ambiguous"]}
    if task in ("LM", "RM") and kind == "hop2":  # a landmark: its name (without 'the') in the first non-empty line
        line = next((ln for ln in text.lower().split("\n") if ln.strip()), "")
        hit = expected.lower().removeprefix("the ") in line
        named = (r for r, w in other_answers(task, kind, item).items() if w.lower().removeprefix("the ") in line)
        return {"said": line.strip()[:40], "correct": hit, "role": "bridge" if hit else next(named, "other")}
    if task.startswith("brew"):
        words = PALETTE
    elif kind == "hop1":
        words = COUNTRIES
    elif task in ("LM", "RM"):
        words = CITY_WORDS
    elif task in ("BT", "RT"):
        words = CAPITAL_WORDS if kind == "hop2" else PALETTE
    else:
        words = CAPITAL_WORDS if task in ("R", "B") else PALETTE
    said = answer_colour(text, list(words))
    role = next(
        (r for r, w in other_answers(task, kind, item).items() if w.lower() == said), "other" if said else "none"
    )
    return {"said": said, "correct": said == expected.lower(), "role": role}


def load_items(task: str, limit: int | None) -> list[tuple[int, dict]]:
    _, _, load, family = TASKS[task]
    items = [(i, it) for i, it in enumerate(load()) if family is None or it["family"] == family]
    return items[:limit] if limit else items


def stage_manifest(name: str, why: str, tasks: list[str], limit: int | None) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "competence",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Unedited and greedy, how often does the model answer each part B task correctly, in the format "
        "the runs feed it (raw text; brew: chat with 'Answer:') and in the chat format, whole and hop by hop?",
        "why": why,
        "model": pins.model_pin(),
        "tasks": {
            t: {"file": str(TASKS[t][0].relative_to(pins.REPO_ROOT)), "sha256": TASKS[t][1], "family": TASKS[t][3]}
            for t in tasks
        },
        "limit": f"the first {limit} items per task (file order)" if limit else "every item",
        "formats": {
            "raw": "raw text, no chat template, as the part B runs (probe_swap stripped of its trailing space, as "
            "exp02's main runs); none for brew",
            "chat": "chat template, enable_thinking=False, generation prompt, nothing prefilled. The statement becomes a "
            f"question after the same context, then ' {INSTRUCTION}' (brew: its own prompt, unchanged; probe_swap: "
            f"'{BLANK_INSTRUCTION}', a blank line, the sentence without 'Fact: ' and ' ___')",
            "chat_prefill": f"as chat, with the assistant turn prefilled {PREFILL!r} (brew's format, exp03's render)",
        },
        "as_run": AS_RUN,
        "kinds": {
            "clean": "the item's prompt",
            "cf": "exp09 only: its C prompt (the bridge set to X; answer X's capital or colour), as its eligibility",
            "off": "exp09 only: its O prompt (X's and Z's holders swap; the answer stays)",
            "hop1": "exp09: '<context> <city> is located in' (R, RL) or '<context> <person> lives in' (B, L) -> the "
            "bridge (chat: 'In which country is <city> located?' / 'In which country does <person> live?'); brew: "
            "'You stir the potion once.' -> the intermediate. (smoke_v1's wording, '<context> The country where <city> "
            "is located is', drew raw continuations such as 'the same as the country where Bob lives' and was replaced)",
            "hop2": "exp09: '<context> The capital of <bridge> is' (R, B) or '<context> <bridge>'s colour is' (L, RL) "
            "-> the answer; brew: once, starting from the intermediate -> the answer. probe_swap: no hop prompts",
        },
        "judge": {
            "probe_swap": "exp13's judge on the continuation: C (the answer as a word sequence in the first clause) and "
            "not ambiguous (the swap answer not there too)",
            "others": "exp03's answer_colour: the first word of the set in the first non-empty line (capitals: R, B; "
            "countries: exp09's hop1; colours: brew, L, RL), equal to the expected answer",
        },
        "generation": f"greedy, {MAX_NEW_TOKENS} new tokens, prompts of one token length batched {BATCH} at a time "
        "(Model.generate_batch, no edits)",
        "reported": "per task, format and kind: n, correct, Wilson 95% interval; the first step's probability of the "
        "answer's first token (as written, capitalised or lowercase; after a space except at the start of a chat reply); wrong answers by role (the bridge's, X's or Z's, other). "
        "exp09: all three of clean, cf and off (its eligibility) and the share of clean-correct items among those "
        "with both hops right",
        "reading_aid": f"a cell is called reliable if its Wilson lower bound is at least {RELIABLE_LOWER} (a reading aid "
        "proposed by the agent, not a decision rule fixed by a human)",
        "baselines": "chance among the three in-context options (exp09: 1/3); brew: 1/12 palette colours, or the "
        "answer of a one-stir shortcut (the intermediate) and the start, reported as roles",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    for t, pin in manifest["tasks"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], t
    limit = int(manifest["limit"].split()[2]) if manifest["limit"].startswith("the first") else None
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []  # one per (task, item, kind, format)
    for task in manifest["tasks"]:
        for index, item in load_items(task, limit):
            if task == "probe_swap":
                texts = {"clean": (item["prompt"], item["answer"])}
            elif task.startswith("brew"):
                texts = brew_texts(item)
            else:
                texts = exp09_texts(item, index, tok)
            for kind, (text, expected) in texts.items():
                for fmt in FORMATS:
                    ids = render(tok, task, fmt, text)
                    if ids is not None:
                        prompts.append(
                            {
                                "task": task,
                                "index": index,
                                "name": item["name"],
                                "kind": kind,
                                "format": fmt,
                                "text": text,
                                "expected": expected,
                                "ids": ids,
                                "item": item,
                            }
                        )
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = {}
    for p in prompts:
        by_len.setdefault(len(p["ids"]), []).append(p)
    done = 0
    for length in sorted(by_len):
        group = by_len[length]
        for start in range(0, len(group), BATCH):
            chunk = group[start : start + BATCH]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            texts, logits = model.generate_batch(ids, MAX_NEW_TOKENS, [{}] * len(chunk), first_logits=True)
            probs = logits.softmax(-1)
            for row, (p, text) in enumerate(zip(chunk, texts, strict=True)):
                surf = first_ids(tok, p["expected"], p["format"])
                p["continuation"] = text
                p["p_answer"] = float(probs[row, surf].sum()) if surf else None
                p.update(score(p["task"], p["kind"], p["item"], p["expected"], text))
            done += len(chunk)
        print(f"len {length}: {done}/{len(prompts)} done, {time.time() - t0:.0f}s", flush=True)
    rows = [{k: v for k, v in p.items() if k not in ("ids", "item")} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary = summarize(rows, manifest)
    summary.update(seconds=round(time.time() - t0), git=git_state(), command=" ".join(sys.argv))
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(summary, rows))
    print("wrote", out_dir / "summary.json")


def cell(rows: list[dict]) -> dict:
    hits = sum(r["correct"] for r in rows)
    rate, lo, hi = wilson(hits, len(rows))
    ps = [r["p_answer"] for r in rows if r["p_answer"] is not None]
    roles: dict[str, int] = {}
    for r in rows:
        if not r["correct"]:
            roles[r.get("role", "wrong")] = roles.get(r.get("role", "wrong"), 0) + 1
    return {
        "n": len(rows),
        "correct": hits,
        "rate": rate,
        "ci": [lo, hi],
        "reliable": bool(lo >= RELIABLE_LOWER) if rows else None,
        "median_p_answer": statistics.median(ps) if ps else None,
        "n_p_answer": len(ps),
        "wrong_roles": roles,
    }


def summarize(rows: list[dict], manifest: dict) -> dict:
    out: dict[str, Any] = {"n_prompts": len(rows), "as_run": manifest["as_run"], "cells": {}, "joint": {}}
    for task in manifest["tasks"]:
        out["cells"][task], out["joint"][task] = {}, {}
        for fmt in FORMATS:
            mine = [r for r in rows if r["task"] == task and r["format"] == fmt]
            if not mine:
                continue
            out["cells"][task][fmt] = {
                k: cell([r for r in mine if r["kind"] == k]) for k in KINDS if any(r["kind"] == k for r in mine)
            }
            per_item: dict[int, dict[str, bool]] = {}
            for r in mine:
                per_item.setdefault(r["index"], {})[r["kind"]] = r["correct"]
            joint = {}
            if task in ("R", "B", "L", "RL", *USE_SOURCE):
                n_all3 = sum(all(v[k] for k in ("clean", "cf", "off")) for v in per_item.values())
                joint["all_three"] = dict(zip(("rate", "lo", "hi"), wilson(n_all3, len(per_item)), strict=True)) | {
                    "n": len(per_item),
                    "correct": n_all3,
                }
            if any("hop1" in v for v in per_item.values()):
                hops = [k for k in ("hop1", "hop2", "hop3") if any(k in v for v in per_item.values())]
                both = [v for v in per_item.values() if all(v[k] for k in hops)]
                n_clean = sum(v["clean"] for v in both)
                key = "both_hops" if len(hops) == 2 else "all_hops"  # 2-step tasks keep v1's key names
                joint[key] = {"n": len(per_item), "correct": len(both)}
                joint[f"clean_given_{key}"] = dict(
                    zip(("rate", "lo", "hi"), wilson(n_clean, len(both)), strict=True)
                ) | {"n": len(both), "correct": n_clean}
            out["joint"][task][fmt] = joint
    return out


def joint_cell(j: dict | None) -> dict | None:
    """A joint rate (rate, lo, hi, n, correct) in a cell's shape."""
    if not j or not j["n"]:
        return None
    return {**j, "ci": [j["lo"], j["hi"]], "reliable": j["lo"] >= RELIABLE_LOWER}


def fmt_cell(c: dict | None) -> str:
    if not c or not c.get("n"):
        return "-"
    flag = " ✓" if c.get("reliable") else ""
    return f"{c['correct']}/{c['n']} {100 * c['rate']:.0f}% [{100 * c['ci'][0]:.0f},{100 * c['ci'][1]:.0f}]{flag}"


def summary_md(summary: dict, rows: list[dict]) -> str:
    out = [
        f"# {EXP}: unedited greedy accuracy per task and format",
        "",
        f"✓: Wilson 95% lower bound ≥ {RELIABLE_LOWER:.2f} (reading aid). As run: the format part B's runs use.",
        "",
        "| task | format | clean | cf | off | all three | hop1 | hop2 | hop3 | clean, given every hop | median p(answer), clean |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for task, formats in summary["cells"].items():
        for fmt, kinds in formats.items():
            joint = summary["joint"][task].get(fmt, {})
            a3 = joint.get("all_three")
            cg = joint.get("clean_given_both_hops") or joint.get("clean_given_all_hops")
            p = kinds.get("clean", {}).get("median_p_answer")
            label = f"**{fmt}** (as run)" if summary["as_run"][task] == fmt else fmt
            out.append(
                f"| {task} | {label} | {fmt_cell(kinds.get('clean'))} | {fmt_cell(kinds.get('cf'))} | "
                f"{fmt_cell(kinds.get('off'))} | {fmt_cell(joint_cell(a3))} | {fmt_cell(kinds.get('hop1'))} | "
                f"{fmt_cell(kinds.get('hop2'))} | {fmt_cell(kinds.get('hop3'))} | {fmt_cell(joint_cell(cg))} | {'-' if p is None else f'{p:.2f}'} |"
            )
    out += ["", "## Wrong answers by role (clean)", ""]
    for task, formats in summary["cells"].items():
        for fmt, kinds in formats.items():
            roles = kinds.get("clean", {}).get("wrong_roles")
            if roles:
                out.append(f"- {task} / {fmt}: {roles}")
    out += ["", "## Examples of wrong clean answers (first 4 per task and format)", ""]
    for task in summary["cells"]:
        for fmt in FORMATS:
            wrong = [
                r
                for r in rows
                if r["task"] == task and r["format"] == fmt and r["kind"] == "clean" and not r["correct"]
            ]
            for r in wrong[:4]:
                out.append(f"- {task} / {fmt} / {r['name']}: expected {r['expected']!r}, said {r['continuation']!r}")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--name", required=True)
    m.add_argument("--why", required=True)
    m.add_argument("--tasks", nargs="+", default=list(TASKS), choices=list(TASKS))
    m.add_argument("--limit", type=int, default=None, help="the first N items per task (a smoke run)")
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    sub.add_parser("check", help="tokenizer only: every prompt renders in every format")
    args = ap.parse_args()
    if args.stage == "manifest":
        stage_manifest(args.name, args.why, args.tasks, args.limit)
    elif args.stage == "run":
        stage_run(args.name)
    else:
        stage_check()


def stage_check() -> None:
    from bridge_jspace.tokens import load_tokenizer

    tok = load_tokenizer()
    for task in TASKS:
        items = load_items(task, None)
        n = 0
        for index, item in items:
            if task == "probe_swap":
                texts = {"clean": (item["prompt"], item["answer"])}
            elif task.startswith("brew"):
                texts = brew_texts(item)
            else:
                texts = exp09_texts(item, index, tok)
            for _kind, (text, _) in texts.items():
                for fmt in FORMATS:
                    n += render(tok, task, fmt, text) is not None
        index, item = items[0]
        print(f"{task}: {len(items)} items, {n} prompts")
        first = {"probe_swap": {"clean": (item["prompt"], "")}}.get(task) or (
            brew_texts(item) if task.startswith("brew") else exp09_texts(item, index, tok)
        )
        for kind, (text, expected) in first.items():
            for fmt in FORMATS:
                ids = render(tok, task, fmt, text)
                if ids is not None and (fmt != "raw" or kind == "clean") and not task.startswith("brew"):
                    print(f"  [{kind}/{fmt}] -> {expected!r}\n    {tok.decode(ids)!r}")


if __name__ == "__main__":
    main()
