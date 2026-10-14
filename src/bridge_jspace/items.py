"""Probe-swap items with part B's labels, and the token ids part A reads for each of them.

Shared by exp11+ so every part A experiment scores the same words the same way as part B (`tokens.concept_token`
for entities, `tokens.surface_ids` for answers).
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any

from bridge_jspace.pins import probe_swap_items
from bridge_jspace.tokens import concept_token, surface_ids

# The four words read per item: the bridge and its same-category distractor; the answer and its distractor.
ROLES = ("bridge", "distractor", "answer", "swap_answer")
ROLE_FIELD = {"bridge": "intermediate", "distractor": "swap_to", "answer": "answer", "swap_answer": "swap_answer"}


def load_labelled_items(labels_file: Path, sha256: str) -> list[dict[str, Any]]:
    """Probe-swap items joined with part B's labels (status, label) by name; labels file checked against its pin."""
    blob = labels_file.read_bytes()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha256:
        raise ValueError(f"{labels_file} sha256 {got} != pinned {sha256}")
    labels = {r["name"]: r for r in csv.DictReader(blob.decode().splitlines())}
    items = probe_swap_items()
    if set(labels) != {it["name"] for it in items}:
        raise ValueError("labels.csv and probe_swap.json name different items")
    return [{**it, "status": labels[it["name"]]["status"], "label": labels[it["name"]]["label"]} for it in items]


def concept_or_none(tok, word: str) -> int | None:
    try:
        return concept_token(tok, word)
    except ValueError:
        return None


def token_pool(tok, words: list[str]) -> list[int]:
    """Unique concept tokens of `words` (words without a single-token surface are left out)."""
    return list(dict.fromkeys(t for w in dict.fromkeys(words) if (t := concept_or_none(tok, w)) is not None))


def entity_and_answer_pools(tok, items: list[dict[str, Any]]) -> tuple[list[int], list[int]]:
    entities = token_pool(tok, [w for it in items for w in (it["intermediate"], it["swap_to"])])
    answers = token_pool(tok, [w for it in items for w in (it["answer"], it["swap_answer"])])
    return entities, answers


def word_ids(tok, item: dict[str, Any]) -> dict[str, list[int]]:
    """Token ids per role for the vocabulary word rank (answers: every single-token surface; may be empty)."""
    return {
        "bridge": [concept_token(tok, item["intermediate"])],
        "distractor": [concept_token(tok, item["swap_to"])],
        "answer": surface_ids(tok, item["answer"]),
        "swap_answer": surface_ids(tok, item["swap_answer"]),
    }


def pool_ids(tok, item: dict[str, Any]) -> dict[str, int | None]:
    """The one id per role whose rank within its pool is read (None: no single-token surface)."""
    return {role: concept_or_none(tok, item[field]) for role, field in ROLE_FIELD.items()}


def role_ranks(
    logits,
    words: dict[str, list[int]],
    pool_targets: dict[str, int | None],
    entity_pool: list[int],
    answer_pool: list[int],
    mask,
) -> dict[str, Any]:
    """Ranks of the four words in `logits` [n, vocab]: `<role>_word` (vocabulary word rank) and `<role>_pool`
    (rank within the entity or answer pool), each a [n] long tensor, or None when the word has no usable token."""
    from bridge_jspace.readout import pool_ranks, word_ranks

    out: dict[str, Any] = {}
    cands = [words[r] for r in ROLES]
    wr = word_ranks(logits, [c or [0] for c in cands], mask)  # an empty set is scored on id 0, then dropped
    for j, role in enumerate(ROLES):
        out[f"{role}_word"] = wr[:, j] if cands[j] else None
    for (a, b), pool in ((("bridge", "distractor"), entity_pool), (("answer", "swap_answer"), answer_pool)):
        ta, tb = pool_targets[a], pool_targets[b]
        if ta is None or tb is None:
            out[f"{a}_pool"] = out[f"{b}_pool"] = None
        else:
            pr = pool_ranks(logits, [ta, tb], pool)
            out[f"{a}_pool"], out[f"{b}_pool"] = pr[:, 0], pr[:, 1]
    return out
