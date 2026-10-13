"""The 90 two-hop items, the entity prompts, and the checks the entity prompts must pass."""

import hashlib
import json
import re
from collections import Counter, defaultdict

from . import pins

MIN_DISTINCT_ANSWERS = 3
MAX_CUE_REPEATS = 3


def load_items() -> list[dict]:
    raw = pins.PROBE_SWAP_FILE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pins.PROBE_SWAP_SHA256, "probe_swap.json differs from its pin"
    return json.loads(raw)["items"]


def load_entity_prompts(topup: bool = False) -> dict[str, list[dict]]:
    """Prompts per entity, each row tagged with its round: 1 from entity_prompts.json, 2 from the top-up file
    (appended to its entities when `topup`)."""
    prompts = {e: [{**r, "round": 1} for r in rows]
               for e, rows in json.loads(pins.ENTITY_PROMPTS_FILE.read_text())["entities"].items()}
    if topup:
        for e, rows in json.loads(pins.ENTITY_PROMPTS_TOPUP_FILE.read_text())["entities"].items():
            prompts[e] += [{**r, "round": 2} for r in rows]
    return prompts


def sha256_of(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entities_of(items: list[dict]) -> list[str]:
    return sorted({i["intermediate"] for i in items} | {i["swap_to"] for i in items}, key=str.lower)


def forbidden_answers(items: list[dict]) -> dict[str, set[str]]:
    """Per entity, the answers the test items expect from it (lowercase): its answer when it is the bridge and its
    swap answer when it is the swap target."""
    out = defaultdict(set)
    for item in items:
        out[item["intermediate"]].add(item["answer"].lower())
        out[item["swap_to"]].add(item["swap_answer"].lower())
    return dict(out)


def first_word(text: str) -> str | None:
    """The first word of a continuation (letters/digits, keeping inner hyphens and apostrophes), or None."""
    match = re.search(r"[^\W_]+(?:['’-][^\W_]+)*", text)
    return match.group(0) if match else None


FUNCTION_WORDS = frozenset(
    "fact a an the of in on at to for from by with and or is are was were be been its it that which who whose where "
    "when as this these those".split())


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.lower())


def _content_ngrams(text: str, n: int) -> set[tuple[str, ...]]:
    words = [w for w in _words(text) if w not in FUNCTION_WORDS]
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def swap_partners(items: list[dict]) -> dict[str, set[str]]:
    """Per entity, the entities it is swapped with in either direction."""
    out = defaultdict(set)
    for item in items:
        out[item["intermediate"]].add(item["swap_to"])
        out[item["swap_to"]].add(item["intermediate"])
    return dict(out)


def _name_pattern(entity: str) -> re.Pattern:
    return re.compile(rf"\b{re.escape(entity)}(e?s)?\b", re.IGNORECASE)


def check_entity_prompts(prompts: dict[str, list[dict]], items: list[dict]) -> list[str]:
    """Every rule in the prompt file's meta block that can be checked mechanically; returns the violations.
    Overlap is measured on content words (FUNCTION_WORDS removed): no 4-gram shared with any test prompt, and no
    3-gram shared with the test prompts that cue the same entity (so its test cue is not reused). Distinct cues: no
    content bigram appears in more than MAX_CUE_REPEATS of an entity's prompts."""
    problems = []
    entities = entities_of(items)
    if sorted(prompts, key=str.lower) != entities:
        problems.append(f"entity set differs: missing {set(entities) - set(prompts)}, extra {set(prompts) - set(entities)}")
    forbidden, partners = forbidden_answers(items), swap_partners(items)
    any_entity = [_name_pattern(e) for e in entities]
    test_4grams = set().union(*(_content_ngrams(i["prompt"], 4) for i in items))
    own_3grams = defaultdict(set)
    for i in items:
        own_3grams[i["intermediate"]] |= _content_ngrams(i["prompt"], 3)
    for entity, rows in prompts.items():
        name = _name_pattern(entity)
        partner_names = [_name_pattern(p) for p in partners.get(entity, ())]
        first_answers = {row["answers"][0].lower() for row in rows}
        if len(first_answers) < MIN_DISTINCT_ANSWERS:
            problems.append(f"{entity}: only {len(first_answers)} distinct answers")
        bigram_counts = Counter(g for row in rows for g in _content_ngrams(row["prompt"], 2))
        repeated = {" ".join(g): n for g, n in bigram_counts.items() if n > MAX_CUE_REPEATS}
        if repeated:
            problems.append(f"{entity}: cue repeated in more than {MAX_CUE_REPEATS} prompts {repeated}")
        for row in rows:
            prompt, answers = row["prompt"], row["answers"]
            tag = f"{entity}: {prompt!r}"
            if not prompt.startswith("Fact: ") or prompt.endswith(" "):
                problems.append(f"{tag}: must start with 'Fact: ' and not end in a space")
            if name.search(prompt):
                problems.append(f"{tag}: names the entity")
            if any(p.search(prompt) for p in partner_names):
                problems.append(f"{tag}: mentions a swap partner")
            if any(p.fullmatch(a) for a in answers for p in any_entity):
                problems.append(f"{tag}: an answer is one of the entities")
            shared = _content_ngrams(prompt, 4) & test_4grams
            if shared:
                problems.append(f"{tag}: shares content 4-grams with test prompts {sorted(shared)}")
            shared = _content_ngrams(prompt, 3) & own_3grams[entity]
            if shared:
                problems.append(f"{tag}: reuses this entity's test cue {sorted(shared)}")
            bad = {a.lower() for a in answers} & forbidden.get(entity, set())
            if bad:
                problems.append(f"{tag}: answer is a test answer for this entity {bad}")
            bad_words = set(_words(prompt)) & forbidden.get(entity, set())
            if bad_words:
                problems.append(f"{tag}: prompt contains a test answer for this entity {bad_words}")
    return problems
