"""code_positions (D1 in code, 2026-10-21): does a lookup read a bridge STATED IN CODE through the lens-readable part
of the copy, or around it? statement_positions' test (D1: in the animal suite the lens-readable part of the stated
bridge carried 0/240 of the context paste's effect, concentration 0.10 [0.08, 0.13], while the stated-bridge -> memory
family was inside, 4.87; UNVERIFIED) moved to Python code, where the bridge is a variable's value.

Scene (countries, pointer_v4's probe-passing pool; 34 whose quoted name has one of two token lengths): a program
  ```python
  drawers = {"France": 3, "Japan": 7, "Peru": 5, "Kenya": 1, "Chile": 8}
  key = "Japan"
  spare = "Cuba"
Two families on the same program (same context, so a paste at the program is the same patch for both readers):
  KL  stated in code -> prompt:  "print(drawers[key])\\n```\\nWhat does this Python code print?"  -> 7
  KR  stated in code -> memory:  "```\\nWhat is the capital of the country stored in key?"     -> Tokyo  (the positive
      control: a recalled fact of the stated bridge, as D1's stated-bridge -> memory families)
C (the alt prompt) changes the key line to another dict key X of the same token length (key = "Peru": KL 5, KR Lima);
O changes the spare line (an off-path variable). Steps alone (competence): hop1 "What string is stored in key?",
hop2 the lookup with the country named (KL) or its capital asked directly (KR).

Position sets (statement_positions' names, code meanings): bind_bridge = the key line (key = "Japan"), bridge_word =
the country inside it, bind_other = the spare line, lookup_bridge / lookup_x = the dict entries of the bridge and of X
(C's change comes after them: exact no-ops, skipped), context = the whole program, question / q_words / final as
statement_positions.

Stages run statement_positions' map, parts and readwrite unchanged (its transit rule, J-space split, lens push and
decision rule), on these cases (its module constants set for the two families; this script's own competence, figures,
report and examples). Map layers 28-44 every 2 on the 27B; parts and readwrite at the map's transit cells on its coarse
grid below the answer onset (28, 32, 36, 40), primary 32-40.

Decision rule (fixed before the 27B run): statement_positions' (a J-space verdict of "around" needs the concentration's
upper bound < 1.0 and the rest's effect above the J-space part's; "inside" a lower bound > 1.2 and above the random
dictionary). H-D1-code holds iff at the key line (bind_bridge), primary layers, the stated-in-code -> prompt family is
in transit (the paste switches >= 50% of answers, above every control) and its J-space verdict is "around"; it is
interpretable only if the stated-in-code -> memory family is "inside" at the same set (the positive control).
Secondary, reported: the whole program (context), the key word, the lens push (statement_positions' write verdict).

Stages:  make (tokenizer; data/code_positions_v1/items.json)  verify  check
         manifest_competence --name N --why W [--limit K]  competence --name N   (GPU)
         plan [--n K]   map --name M --why W [--n K] [--layers ...]   parts --name P --map M --why W [--force SET:LAYER ...]
         readwrite --name R --map M --parts P --why W [--force ...]   figures --name R   examples --name M [--k 3]
Eligibility: BJ_D1CODE_COMPETENCE names the competence run (default d1code_competence_27b; "none": every scene, a smoke).
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import time
import types
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from bridge_jspace.tokens import raw_encoding
from scripts import pointer_v4 as P4
from scripts import statement_positions as SP
from scripts import suite_split as P
from scripts import suite_v1 as S

EXP = "code_positions"
DATA = pins.DATA_DIR / "code_positions_v1"
ITEMS = DATA / "items.json"
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES: tuple[str, ...] = ("KL", "KR")
LABEL = {"KL": "stated in code → prompt", "KR": "stated in code → memory"}
DESC = {"KL": "a variable holds the country, its number looked up in the program's dict",
        "KR": "a variable holds the country, its capital recalled"}  # fmt: skip
CAPITAL = {c: cap for c, (_, cap) in P4.COUNTRIES.items()}
# quoted-name token length on Qwen3.6-27B's tokenizer ('key = "France"' and '"Peru"' differ by one): pairs are drawn
# within a group; Venezuela and Lebanon (a third length) are left out. make/check assert it.
GROUPS = {
    0: ("France", "Italy", "Spain", "Germany", "Japan", "Egypt", "Russia", "China", "Canada", "Australia", "Sweden",
        "Turkey", "Iran", "Iraq", "Indonesia", "Pakistan"),
    1: ("Peru", "Norway", "Greece", "Ireland", "Austria", "Poland", "Portugal", "Thailand", "Kenya", "Cuba", "Finland",
        "Hungary", "Belgium", "Philippines", "Chile", "Denmark", "Korea", "Syria"),
}  # fmt: skip
COUNTRY_LIST = tuple(c for g in GROUPS.values() for c in g)
GROUP_OF = {c: g for g, cs in GROUPS.items() for c in cs}
N_KEYS, N_SCENES, SEED = 5, 200, 861
QUESTIONS = {
    "KL": "print(drawers[key])\n```\nWhat does this Python code print?",
    "KR": "```\nWhat is the capital of the country stored in key?",
}
HOP1 = "```\nWhat string is stored in key?"
MAP_LAYERS = tuple(range(28, 45, 2))  # the 27B's 28-44 every 2 (statement_positions' window and onset)
COMPETENCE = os.environ.get("BJ_D1CODE_COMPETENCE", "d1code_competence_27b")


# ---- items (tokenizer-free) ---------------------------------------------------------------------------------------


def program(keys: list[str], digits: list[int], key: str, spare: str) -> str:
    entries = ", ".join(f'"{k}": {d}' for k, d in zip(keys, digits, strict=True))
    return f'```python\ndrawers = {{{entries}}}\nkey = "{key}"\nspare = "{spare}"'


def scene(rng: random.Random, i: int, bridge: str) -> dict[str, Any]:
    x = rng.choice([c for c in GROUPS[GROUP_OF[bridge]] if c != bridge])
    others = rng.sample([c for c in COUNTRY_LIST if c not in (bridge, x)], N_KEYS - 2)
    keys = [bridge, x, *others]
    rng.shuffle(keys)
    digits = rng.sample(range(10), N_KEYS)
    g = rng.randrange(2)
    spare, spare_o = rng.sample([c for c in GROUPS[g] if c not in keys], 2)
    return {"scene": f"code-{i:04d}", "keys": keys, "digits": digits, "bridge": bridge, "x": x, "spare": spare,
            "spare_o": spare_o}  # fmt: skip


def items_for(sc: dict[str, Any]) -> dict[str, dict]:
    look = dict(zip(sc["keys"], sc["digits"], strict=True))
    ctx = program(sc["keys"], sc["digits"], sc["bridge"], sc["spare"])
    cf_ctx = program(sc["keys"], sc["digits"], sc["x"], sc["spare"])
    off_ctx = program(sc["keys"], sc["digits"], sc["bridge"], sc["spare_o"])
    b, x = sc["bridge"], sc["x"]
    out = {}
    for fam in FAMILIES:
        lookup = fam == "KL"
        answer, cf_answer = (str(look[b]), str(look[x])) if lookup else (CAPITAL[b], CAPITAL[x])
        hop2 = (f'print(drawers["{b}"])\n```\nWhat does this Python code print?' if lookup
                else f"```\nWhat is the capital of {b}?")  # fmt: skip
        out[fam] = {
            "id": f"{fam}-{sc['scene']}", "family": fam, "scene": sc["scene"], "context": ctx, "cf_context": cf_ctx,
            "off_context": off_ctx, "question": QUESTIONS[fam], "cf_question": QUESTIONS[fam], "cue": "key",
            "bridge": b, "cf_bridge": x, "spare": sc["spare"], "spare_o": sc["spare_o"], "keys": sc["keys"],
            "digits": sc["digits"], "answer": answer, "cf_answer": cf_answer,
            "answer_kind": "digit" if lookup else "word",
            "hop1": {"question": HOP1, "answer": b, "kind": "country"},
            "hop2": {"question": hop2, "answer": answer, "kind": "digit" if lookup else "capital"},
        }  # fmt: skip
    return out


def generate() -> list[dict]:
    """N_SCENES scenes, the bridge cycling through the countries in seeded rounds (each at most ceil(N / 34) times)."""
    rng = random.Random(SEED)
    out, seen, rounds = [], set(), []
    i = 0
    while i < N_SCENES:
        if not rounds:
            rounds = rng.sample(COUNTRY_LIST, len(COUNTRY_LIST))
        sc = scene(rng, i, rounds.pop())
        key = program(sc["keys"], sc["digits"], sc["bridge"], sc["spare"])
        if key in seen:
            continue
        seen.add(key)
        its = items_for(sc)
        out += [its[f] for f in FAMILIES]
        i += 1
    return out


def load_items() -> list[dict]:
    return json.loads(ITEMS.read_text())["items"]


# ---- judges (competence; statement_positions' greedy validation of word answers) -----------------------------------


_suite_said = S.said  # suite_v1's own judge (stage_competence replaces S.said with this module's)


def said(text: str, kind: str) -> str | None:
    """The first answer of the kind in the first non-empty line: a digit, a country or a capital."""
    if kind == "digit":
        return _suite_said(text, "digit")
    vocab = {"country": COUNTRY_LIST, "capital": tuple(CAPITAL.values()), "word": tuple(CAPITAL.values())}[kind]
    lower = {w.lower(): w for w in vocab}
    return next((lower[t] for t in re.findall(r"[a-z]+", S.first_line(text)) if t in lower), None)


def capital_judge(text: str) -> str | None:
    return said(text, "capital")


# ---- cases and position sets (tokenizer only) -------------------------------------------------------------------------


def eligible_scenes() -> set[str] | None:
    """Scenes whose every competence prompt is right in both families (None: no eligibility, BJ_D1CODE_COMPETENCE=none)."""
    if COMPETENCE == "none":
        return None
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    for line in (RESULTS / COMPETENCE / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        ok[r["id"].split("-", 1)[1]].append(r["correct"])
    fams: dict[str, set[str]] = collections.defaultdict(set)
    for line in (RESULTS / COMPETENCE / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        fams[r["id"].split("-", 1)[1]].add(r["family"])
    return {s for s, v in ok.items() if all(v) and fams[s] == set(FAMILIES)}


def position_sets(c: dict, rendered: str, offsets: list[tuple[int, int]]) -> tuple[dict, dict]:
    """statement_positions' sets on a program: the key line, its country, the spare line, the two dict entries, the
    whole program, the question, its words and the tail after the user's content."""
    ctx = c["context"]
    assert rendered.count(ctx) == 1, f"{c['id']}: the program is not once in the prompt"
    base = rendered.index(ctx)

    def span(sub: str, after: int = 0) -> tuple[int, int]:
        assert ctx.count(sub) == 1, f"{c['id']}: {sub!r} not once in the program"
        i = base + ctx.index(sub, after)
        return (i, i + len(sub))

    key_line = span(f'key = "{c["bridge"]}"')
    w0 = key_line[0] + len('key = "')
    marks = {"bind_bridge": [key_line], "bridge_word": [(w0, w0 + len(c["bridge"]))],
             "bind_other": [span(f'spare = "{c["spare"]}"')],
             "lookup_bridge": [span(f'"{c["bridge"]}": {c["digits"][c["keys"].index(c["bridge"])]}')],
             "lookup_x": [span(f'"{c["cf_bridge"]}": {c["digits"][c["keys"].index(c["cf_bridge"])]}')],
             "context": [(base, base + len(ctx))]}  # fmt: skip
    sets = {k: sorted({i for a, b in v for i in SP.tokens_in(offsets, a, b)}) for k, v in marks.items()}
    question = list(c["groups"]["question"])
    end = chat.content_end(rendered, base + len(ctx))
    final = [i for i, (s, e) in enumerate(offsets) if e > s and s >= end]
    sets["question"], sets["final"] = question, final
    sets["q_words"] = [i for i in question if i not in set(final)]
    for k in ("question", "final", "q_words"):
        marks[k] = [(offsets[sets[k][0]][0], offsets[sets[k][-1]][1])]
    check_sets(c, sets, len(offsets))
    return sets, marks


def check_sets(c: dict, sets: dict[str, list[int]], n_tokens: int) -> None:
    name = c["id"]
    parts = ("bind_bridge", "bind_other", "lookup_bridge", "lookup_x")
    for a in parts:
        for b in parts:
            assert a == b or not set(sets[a]) & set(sets[b]), f"{name}: {a} and {b} overlap"
    for k in SP.SETS:
        assert sets[k], f"{name}: {k} is empty"
    assert set(sets["bridge_word"]) <= set(sets["bind_bridge"]), f"{name}: the country is outside its line"
    assert all(set(sets[k]) <= set(sets["context"]) for k in parts), f"{name}: a line outside the program"
    assert max(sets["context"]) < min(sets["question"]), f"{name}: a program token sits in the question"
    assert sorted(sets["q_words"] + sets["final"]) == sets["question"], f"{name}: question != q_words + final"
    assert sets["final"] == list(range(sets["final"][0], n_tokens)), f"{name}: final is not the prompt's tail"
    cf, off = set(c["changed"]["cf"]), set(c["changed"]["off"])
    assert cf <= set(sets["bridge_word"]), f"{name}: C changes more than the key's country"
    assert off <= set(sets["bind_other"]), f"{name}: O changes more than the spare line"


def build_cases(tok, n: int, families: list[str]) -> tuple[list[dict], dict]:
    """statement_positions' build_cases for code: the first n eligible scenes (both families right in every
    competence prompt), both families on each; cases whose C or O does not line up are skipped and counted."""
    good = eligible_scenes()
    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in load_items():
        if it["family"] in families:
            by_scene[it["scene"]][it["family"]] = it
    cases, skipped, picked = [], 0, []
    for sc in sorted(by_scene):
        if len(picked) >= n:
            break
        if good is not None and sc not in good:
            continue
        built = []
        try:
            for fam in families:
                it = by_scene[sc][fam]
                prep = P.prepare(it, tok)
                rendered = S.render(tok, it["context"], it["question"])
                c = {**it, **prep, "rendered": rendered, "context_text": it["context"]}
                enc = raw_encoding(tok, rendered, offsets=True)
                assert enc["input_ids"] == c["ids"]["clean"], f"{c['id']}: the rendered prompt is not the run's"
                c["offsets"] = enc["offset_mapping"]
                c["sets"], c["marks"] = position_sets(c, rendered, c["offsets"])
                built.append(c)
        except AssertionError:
            skipped += 1
            continue
        picked.append(sc)
        cases += built
    order = {f: i for i, f in enumerate(families)}
    cases.sort(key=lambda c: order[c["family"]])
    return cases, {"code": {"n": len(picked), "eligible": None if good is None else len(good),
                            "unaligned_skipped": skipped, "competence": COMPETENCE}}  # fmt: skip


# ---- statement_positions, configured for the two code families ---------------------------------------------------


def configure() -> None:
    """Point statement_positions' module constants at this script's families, cases and results folder."""
    SP.EXP, SP.RESULTS = EXP, RESULTS
    SP.FAMILIES = FAMILIES
    SP.SUITE = ()
    SP.COUNTRIES = ("KR",)  # word answers: its greedy validation uses C.judge
    SP.C = types.SimpleNamespace(judge=capital_judge)
    SP.CUE_ONLY = ()
    SP.BOUND = FAMILIES
    SP.LOOKUP_USED_BOUND = ("KL",)
    SP.POSITIVE = ("KR",)
    SP.PAIRS = (("KL", "KR"),)
    SP.build_cases = build_cases
    common = SP.manifest_common

    def manifest_common(name: str, why: str, kind: str, families: list[str], n: int) -> dict:
        saved, SP.COUNTRIES = SP.COUNTRIES, ()  # its countries branch pins exp09's files, which these runs do not read
        try:
            m = common(name, why, kind, families, n)
        finally:
            SP.COUNTRIES = saved
        m["inputs"] = {str(ITEMS.relative_to(pins.REPO_ROOT)): sha256_of(ITEMS)}
        if COMPETENCE != "none":
            comp = RESULTS / COMPETENCE / "items.jsonl"
            m["inputs"][str(comp.relative_to(pins.REPO_ROOT))] = sha256_of(comp)
        m["cases"] = (f"code_positions: the first n scenes (scene order) answered right in every competence prompt of "
                      f"both families by {COMPETENCE}; both families on each scene")  # fmt: skip
        m["families_meaning"] = {f: f"{LABEL[f]}: {DESC[f]}" for f in FAMILIES}
        m["sets"] = (__doc__ or "").split("\n\n")[3]
        m["d1code_decision"] = (__doc__ or "").split("\n\n")[5]
        return m

    SP.manifest_common = manifest_common


# ---- competence (suite_v1's, on these items) ---------------------------------------------------------------------


def stage_manifest_competence(name: str, why: str, limit: int | None) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "switches": switches(), "items": {"code": {"file": str(ITEMS.relative_to(pins.REPO_ROOT)),
                                                       "sha256": sha256_of(ITEMS)}},
         "limit": limit, "format": f"suite_v1's: {chat.format_note()}",
         "prompts": "clean, C (the key line changed), O (the spare line changed), hop1 (the key's value), hop2 (the "
         "lookup with the country named / its capital asked directly)",
         "judge": "suite_v1's greedy judge: digits; the countries / capitals of the items (code_positions.said)",
         "eligibility": "a scene enters the map iff every prompt of both families is right"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    """suite_v1's competence (this script's judge and results folder), then the same table per family (suite_v1
    pools a file's items; both families live in one file)."""
    from bridge_jspace.stats import wilson

    S.RESULTS = RESULTS
    S.said = said
    S.stage_competence(name)
    rows = SP.read_jsonl(RESULTS / name / "items.jsonl")
    per: dict[str, dict[str, dict[str, bool]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in rows:
        per[r["family"]][r["id"]][r["kind"]] = r["correct"]
    out: dict[str, Any] = {}
    lines = [
        "| family | n | " + " | ".join(("clean", "cf", "off", "hop1", "hop2")) + " | all right |",
        "|---" * 8 + "|",
    ]
    for fam in FAMILIES:
        items = per[fam]
        cells = {
            k: wilson(sum(v[k] for v in items.values()), len(items)) for k in ("clean", "cf", "off", "hop1", "hop2")
        }
        all_right = sum(all(v.values()) for v in items.values())
        out[fam] = {"n": len(items), "cells": cells, "all_right": all_right, "reliable": cells["clean"][1] >= 0.85}
        lines.append(f"| {LABEL[fam]} | {len(items)} | "
                     + " | ".join(f"{100 * c[0]:.0f}% [{100 * c[1]:.0f}, {100 * c[2]:.0f}]" for c in cells.values())
                     + f" | {all_right} |")  # fmt: skip
    good = eligible_scenes() if name == COMPETENCE else None
    out["scenes_right_in_both"] = len(good) if good is not None else None
    (RESULTS / name / "summary_by_family.json").write_text(json.dumps(out, indent=2) + "\n")
    (RESULTS / name / "summary_by_family.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


# ---- make / verify / check ----------------------------------------------------------------------------------------


def check_tokens(tok) -> None:
    for g, cs in GROUPS.items():
        lens = {len(S.ids(tok, f'\nkey = "{c}"\n')) for c in cs}
        assert len(lens) == 1, f"group {g}: key lines of {sorted(lens)} tokens"
    assert len({len(S.ids(tok, f'\nkey = "{cs[0]}"\n')) for cs in GROUPS.values()}) == len(GROUPS)
    for cap in CAPITAL.values():
        assert len(S.ids(tok, " " + cap)) == 1, f"{cap} is not one token"


def stage_make() -> None:
    tok = P4.PV.tokenizer()
    check_tokens(tok)
    assert not ITEMS.exists(), f"{ITEMS} exists; data files are written once"
    items = generate()
    ITEMS.parent.mkdir(parents=True, exist_ok=True)
    head = {"generator": f"scripts/code_positions.py make (seed {SEED}, {N_SCENES} scenes)",
            "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    ITEMS.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
    print("wrote", ITEMS, len(items))


def stage_verify() -> None:
    same = load_items() == generate()
    print("items", "same" if same else "DIFFERENT")
    assert same, "the generator no longer reproduces the items"


def stage_check() -> None:
    tok = P4.PV.tokenizer()
    check_tokens(tok)
    configure()
    global COMPETENCE
    COMPETENCE = "none"
    cases, counts = build_cases(tok, N_SCENES, list(FAMILIES))
    sizes = {s: sorted({len(c["sets"][s]) for c in cases}) for s in SP.SETS}
    bridges = collections.Counter(c["bridge"] for c in cases if c["family"] == "KL")
    report = {"counts": counts, "cases": len(cases), "set_sizes": sizes, "max_bridge_share": max(bridges.values()) / sum(bridges.values()),
              "bridges": len(bridges)}  # fmt: skip
    print(json.dumps(report))
    assert counts["code"]["unaligned_skipped"] == 0, "a scene's C or O is not token-aligned"
    assert len(cases) == 2 * N_SCENES
    (DATA / "check.json").write_text(json.dumps(report, indent=1) + "\n")


# ---- figures and report (CPU) -------------------------------------------------------------------------------------

SET_PLAIN = {"bind_bridge": 'the key line (key = "Japan")', "bridge_word": "the country in the key line",
             "bind_other": "the other variable's line", "context": "the whole program", "question": "the question",
             "q_words": "the question's words", "final": "after the question", "lookup_bridge": "the key's dict entry",
             "lookup_x": "the alt key's dict entry"}  # fmt: skip
EXAMPLE = (
    'org prompt "```python drawers = {..., "Japan": 7, "Peru": 5, ...} key = "Japan" spare = "Cuba" '
    'print(drawers[key]) ``` What does this Python code print?" -> answer org 7 (bridge org Japan); alt prompt: '
    'key = "Peru" -> answer alt 5 (bridge alt Peru); the memory question asks the capital (Tokyo / Lima).'
)


FLIPS_LABEL = "% of original answers that become\nthe alternative answer\n(answer org → answer alt)"  # TERM["flips"]


def h_d1_code(parts: dict, rw: dict | None, mp: dict) -> dict[str, Any]:
    """The pre-registered H-D1-code reading of the three runs' summaries."""
    key = "bind_bridge"
    kl, kr = parts["cells"].get(f"KL/{key}/primary"), parts["cells"].get(f"KR/{key}/primary")
    transit = sorted(mp["transit"].get("KL", {}).get(key, []))
    out: dict[str, Any] = {"key_line_transit_layers_KL": transit, "KL_verdict": kl["verdict"] if kl else None,
                           "KR_verdict": kr["verdict"] if kr else None}  # fmt: skip
    if kl:
        out["KL_concentration"] = kl["frac"]["jspace"]["concentration"]
    if kr:
        out["KR_concentration"] = kr["frac"]["jspace"]["concentration"]
    if rw:
        out["KL_lens_write"] = rw["cells"].get(f"KL/{key}/primary", {}).get("verdict")
    holds = bool(kl) and kl["verdict"] == "around"
    out["H-D1-code"] = ("holds" if holds and kr and kr["verdict"] == "inside" else
                        "around, but the positive control is not inside (not interpretable)" if holds else
                        "no key-line cell in transit at the primary layers" if not kl else "does not hold")  # fmt: skip
    return out


def stage_figures(name: str) -> None:
    """The figures and report.md of one run: a map run gets the map figure; a parts run also the concentration figure
    (its map's); a readwrite run all three and the H-D1-code reading (its manifest names its map and parts runs)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as PL

    configure()
    run_m = json.loads((RESULTS / name / "manifest.json").read_text())
    kind = run_m["kind"]
    map_name = name if kind == "map" else run_m["map"]["run"]
    parts_name = name if kind == "parts" else run_m.get("parts", {}).get("run")
    rw = json.loads((RESULTS / name / "summary.json").read_text()) if kind == "readwrite" else None
    mp = json.loads((RESULTS / map_name / "summary.json").read_text())
    mp_m = json.loads((RESULTS / map_name / "manifest.json").read_text())
    parts = json.loads((RESULTS / parts_name / "summary.json").read_text()) if parts_name else None
    folder = SP.new_figure_folder(name)
    made: list[str] = []
    model = run_m["model"]["repo"].split("/")[-1]
    n = mp.get("counts", {}).get("code", {}).get("n")
    layers = list(mp_m["layers"])
    colors = {"bind_bridge": "#2a78d6", "context": "#eb6834", "bridge_word": "#1baf7a", "q_words": "#eda100",
              "final": "#6250d6"}  # fmt: skip
    # 1. map: % of answers switched to the alt answer, by layer and position set, per family
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.8), sharey=True)
    for ax, fam in zip(axes, FAMILIES, strict=True):
        PL.style_axes(ax)
        PL.percent_axis(ax)
        for s, col in colors.items():
            rows = [SP.map_cell(mp, fam, s, la) for la in layers]
            pts = [(la, r["cf"]["flips"]) for la, r in zip(layers, rows, strict=True) if r]
            if pts:
                ax.plot([p[0] for p in pts], [p[1][0] for p in pts], color=col, lw=2, marker="o", ms=3)
                ax.fill_between([p[0] for p in pts], [p[1][1] for p in pts], [p[1][2] for p in pts], color=col,
                                alpha=0.12, lw=0)  # fmt: skip
            ctrl = [(la, r["rand"]["flips"][0]) for la, r in zip(layers, rows, strict=True) if r and "rand" in r]
            if ctrl and s == "bind_bridge":
                ax.plot([p[0] for p in ctrl], [p[1] for p in ctrl], color=PL.MUTED, lw=1.2, ls=(0, (1, 1.6)))
        ax.axhline(SP.TRANSIT_FLIPS, color=PL.MUTED, lw=0.8, ls=":")
        ax.set_title(f"{LABEL[fam]}\n({DESC[fam]})", fontsize=9, color=PL.INK, loc="left")
        ax.set_xlabel("layer pasted", fontsize=9, color=PL.INK)
    axes[0].set_ylabel(FLIPS_LABEL, fontsize=9)
    handles = [
        Line2D([], [], color=c, lw=2, marker="o", ms=3, label=f"paste: {SET_PLAIN[s]}") for s, c in colors.items()
    ]
    handles.append(
        Line2D(
            [],
            [],
            color=PL.MUTED,
            lw=1.2,
            ls=(0, (1, 1.6)),
            label="control: random push of the same size at the key line",
        )
    )
    SP.caption(fig, folder, "map_paste_by_layer", made, "Where does pasting the alt program switch the answer?",
               [("What we did", "Pasted the alt program's hidden states (key line changed) into the org program at one set "
                 "of positions and one layer, and read the answer."), ("Example", EXAMPLE),
                ("How to read", "Each line: % of answers switched to the alt answer; dotted line at 50%: the transit bar."),
                ("Control", "Grey dotted: a random push of the same size at the key line; it should switch nothing.")],
               f"{model}; {n} programs per family, the same programs for both; shading = 95% Wilson interval.",
               handles=handles, ncols=2)  # fmt: skip
    if parts is None:
        (folder / "summary.json").write_text(json.dumps({"transit": mp["transit"], "figures": made}, indent=2) + "\n")
        (folder / "report.md").write_text(f"# D1 in code: map {map_name}\n\nTransit cells (family -> set -> layers): "
                                          f"`{json.dumps(mp['transit'])}`\n\nSanity: `{json.dumps(mp['sanity'])}`\n")  # fmt: skip
        print("wrote", folder)
        return
    # 2. parts: concentration of the lens-readable part, per family and set (primary window)
    fig, ax = plt.subplots(figsize=(12.6, 4.6))
    PL.style_axes(ax)
    rows = [(k, v) for k, v in parts["cells"].items() if k.endswith("/primary")]
    for y, (k, v) in enumerate(rows):
        conc = v["frac"]["jspace"]["concentration"]
        fam, s, _ = k.split("/")
        col = "#2a78d6" if fam == "KL" else "#1baf7a"
        ax.errorbar([conc[0]], [y], xerr=[[conc[0] - conc[1]], [conc[2] - conc[0]]], fmt="o", color=col, ms=6,
                    elinewidth=1.4, capsize=0)  # fmt: skip
        ax.text(conc[2] + 0.05, y, f"{v['verdict']}", va="center", fontsize=8, color=PL.INK)
    ax.set_yticks(
        range(len(rows)), [f"{LABEL[k.split('/')[0]]}: {SET_PLAIN[k.split('/')[1]]}" for k, _ in rows], fontsize=8
    )
    ax.axvline(SP.OUTSIDE, color=PL.MUTED, lw=0.8, ls="--")
    ax.axvline(SP.INSIDE, color=PL.MUTED, lw=0.8, ls=":")
    ax.set_xlabel("concentration: the lens-readable part's share of the paste's effect / its share of the paste's size",
                  fontsize=9)  # fmt: skip
    SP.caption(fig, folder, "parts_concentration", made, "Does the lens-readable part of the pasted key carry its share?",
               [("What we did", "Split each paste into its lens-readable part (25 words of the J-lens) and the rest, "
                 "pasted each alone at the transit cells, layers 32-40."), ("Example", EXAMPLE),
                ("How to read", "Right of the dotted line (1.2): the part carries more than its size (inside); left of the "
                 "dashed line (1.0) with the rest stronger: around."),
                ("Control", "A random dictionary of the same size (reported in summary.json); the memory question is "
                 "the positive control.")],
               f"{model}; {n} programs per family; bars = 95% scene-bootstrap interval.")  # fmt: skip
    # 3. readwrite: the lens push vs a random push, by size, at the key line
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.0), sharey=True)
    for ax, fam in zip(axes, FAMILIES if rw else (), strict=False):
        assert rw is not None
        PL.style_axes(ax)
        PL.percent_axis(ax)
        cell = rw["cells"].get(f"{fam}/bind_bridge/primary")
        if cell:
            sc = [float(k[1:]) for k in cell["by_scale"]]
            ax.plot(sc, [v["lens_flips"] for v in cell["by_scale"].values()], color="#eb6834", lw=2, marker="o",
                    label="lens push (bridge alt − bridge org)")  # fmt: skip
            ax.plot(sc, [v["random_flips"] for v in cell["by_scale"].values()], color=PL.MUTED, lw=1.2, ls="--",
                    marker="o", label="random push, same size")  # fmt: skip
            ax.axhline(cell["write"]["copy"]["flips"], color="#2a78d6", lw=1.5, label="the paste itself")
            ax.set_xscale("log", base=2)
            ax.set_xticks(sc, [f"{x:g}x" for x in sc])
            ax.minorticks_off()
        ax.set_title(f"{LABEL[fam]}: {cell['verdict'] if cell else 'no transit cell'}", fontsize=9, loc="left")
        ax.set_xlabel("push size (x the paste's size per token)", fontsize=9)
    if rw is not None:
        axes[0].set_ylabel(FLIPS_LABEL, fontsize=9)
        axes[0].legend(frameon=False, fontsize=8)
        SP.caption(fig, folder, "lens_push", made, "Can the lens direction write the key where the paste does?",
                   [("What we did", "Added the lens direction from bridge org to bridge alt at the key line, at 0.5-16x "
                     "the paste's size per token, layers 32-40."), ("Example", EXAMPLE),
                    ("How to read", "Orange above grey at some size <= 4x with >= 30%: written."),
                    ("Control", "Grey dashed: a random direction of the same size.")],
                   f"{model}; {n} programs per family.")  # fmt: skip
    else:
        plt.close(fig)
    verdict = h_d1_code(parts, rw, mp)
    (folder / "summary.json").write_text(json.dumps({"H-D1-code": verdict, "figures": made}, indent=2) + "\n")
    claims = rw.get("claims") if rw else parts.get("claims")
    lines = [f"# D1 in code: {name} (map {map_name}, parts {parts_name})", "",
             f"H-D1-code (pre-registered): **{verdict['H-D1-code']}**"
             + ("" if rw else " (J-space half only: the lens push is the readwrite run's)"), "",
             "```", json.dumps(verdict, indent=1), "```", "",
             f"statement_positions' claims: `{json.dumps(claims)}`", "",
             "| family / set / window | J-space verdict | concentration [95%] |", "|---|---|---|"]  # fmt: skip
    for k, v in parts["cells"].items():
        c = v["frac"]["jspace"]["concentration"]
        fam, s, w = k.split("/")
        lines.append(f"| {LABEL[fam]} / {SET_PLAIN[s]} / {w} | {v['verdict']} | {c[0]:.2f} [{c[1]:.2f}, {c[2]:.2f}] |")
    (folder / "report.md").write_text("\n".join(lines) + "\n")
    print("wrote", folder)


def stage_examples(map_name: str, k: int, seed: int = SP.EXAMPLES_SEED) -> None:
    """k examples per group of a map run: the paste at the key line switched the answer to the alt answer, or kept
    it, at a primary layer; and the random push at the key line that switched it (control)."""
    out = RESULTS / map_name
    cases = {c["id"]: c for c in SP.read_jsonl(out / "cases.jsonl")}
    rows = SP.read_jsonl(out / "outcomes.jsonl")
    prim = [r for r in rows if r.get("set") == "bind_bridge" and r.get("layer", -1) >= SP.PRIMARY_LO]
    groups = {"switched": ("the paste at the key line gave the alt answer", lambda r: r["source"] == "cf" and r["role"] == "b"),
              "kept": ("the paste at the key line left the org answer", lambda r: r["source"] == "cf" and r["role"] == "A"),
              "control_switched": ("a random push of the paste's size at the key line changed the answer",
                                   lambda r: r["source"] == "rand" and r["role"] != "A")}  # fmt: skip
    rng = random.Random(seed)
    examples, meta = [], []
    for g, (definition, pred) in groups.items():
        cand = [r for r in prim if pred(r)]
        meta.append({"key": g, "title": g.replace("_", " "), "definition": definition, "n_total": len(cand)})
        for r in rng.sample(cand, min(k, len(cand))):
            c = cases[r["name"]]
            spans = [{"start": a, "end": b, "role": SET_PLAIN[s]} for s in ("bind_bridge", "bind_other")
                     for a, b in c["marks"][s]]  # fmt: skip
            examples.append({"group": g, "family": LABEL[c["family"]], "item_id": c["id"], "prompt": c["prompt"],
                             "spans": spans, "condition": f"{r['source']} at {SET_PLAIN['bind_bridge']}, layer {r['layer']}",
                             "answers": {"clean": c["answer"], "edited": r["top_text"].strip(), "expected": c["cf_answer"]},
                             "numbers": {"frac": r["frac"], "ld": r["ld"], "role": r["role"]},
                             "why": f"{definition}; alt prompt: key = \"{c['cf_bridge']}\""})  # fmt: skip
    path = out / "examples.json"
    path.write_text(json.dumps({"exp": EXP, "run": map_name, "seed": seed, "k": k, "groups": meta,
                                "examples": examples}, indent=1, ensure_ascii=False) + "\n")  # fmt: skip
    print("wrote", path, len(examples), "examples")


# ---- CLI ------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest_competence", "competence", "plan", "map",
                                      "parts", "readwrite", "figures", "examples"])  # fmt: skip
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--map")
    ap.add_argument("--parts")
    ap.add_argument("--n", type=int, default=SP.N_CASES)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    ap.add_argument("--force", nargs="+", default=None)
    ap.add_argument("--sets", nargs="+", default=None, choices=list(SP.SETS), help="parts / readwrite: these sets only")
    ap.add_argument("--k", type=int, default=SP.K_EXAMPLES)
    args = ap.parse_args()
    fams: list[str] = list(FAMILIES)
    if args.stage == "make":
        stage_make()
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check()
    elif args.stage == "manifest_competence":
        assert args.name, "manifest_competence needs --name"
        assert args.why, "manifest_competence needs --why"
        stage_manifest_competence(args.name, args.why, args.limit)
    elif args.stage == "competence":
        assert args.name, "competence needs --name"
        stage_competence(args.name)
    else:
        configure()
        if args.sets:
            SP.CELL_SETS = tuple(args.sets)
        layers = tuple(args.layers) if args.layers else MAP_LAYERS
        if args.stage == "plan":
            SP.stage_plan(args.n, fams, layers, 33.0)
        elif args.stage == "map":
            assert args.name, "map needs --name"
            assert args.why, "map needs --why"
            SP.stage_map(args.name, args.why, args.n, fams, layers)
        else:
            assert args.name, f"{args.stage} needs --name"
            if args.stage in ("parts", "readwrite"):
                assert args.map, f"{args.stage} needs --map"
                assert args.why, f"{args.stage} needs --why"
            if args.stage == "parts":
                SP.stage_parts(args.name, args.map, args.why, SP.parse_force(args.force))
            elif args.stage == "readwrite":
                SP.stage_readwrite(args.name, args.map, args.why, args.parts, SP.parse_force(args.force))
            elif args.stage == "figures":
                stage_figures(args.name)
            else:
                stage_examples(args.name, args.k)
