"""exp13_greedy_answers: does the model answer the probe-swap questions correctly, judged by its greedy continuation?

Part B (and our exp11/exp12 `eligible`) count an item correct only if the answer is the model's first word. Some
"wrong" items look right ("drum" -> drumsticks for "sticks", "gastric" -> gastric acid for "acid"). Here every item
gets a greedy continuation (raw prompt, no chat template, `max_new_tokens`, cut at the first sentence end) and three
criteria, all reported:
  A first word        the first word of the continuation is the answer (close to part B's first-token check)
  B first content     the same after skipping a / an / the
  C in continuation   the answer appears as a word, as the end of a compound word ("drumsticks"; answers of 4+
                      letters only), or as its number word / numeral ("26" = "twenty-six")   <- primary
An item whose continuation also contains the swap answer is ambiguous; compound matches and every item where C and
part B's `eligible` disagree are listed in review.md for a human to read. Variants: prompts as published (part B's)
and with the trailing space stripped.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.items import load_labelled_items
from bridge_jspace.utils import progress

ARTICLES = {"a", "an", "the"}
_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]  # fmt: skip
_TENS = ["_", "_", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


class GreedyAnswers(Experiment):
    def run(self) -> dict[str, Any]:
        p = self.params
        sanity = self.sanity_gate()
        items = load_labelled_items(Path(p["labels_file"]), p["labels_sha256"])[: p.get("limit")]
        rows = []
        for variant in p["variants"]:
            for it in progress(items, f"items ({variant})"):
                prompt = it["prompt"].rstrip() if variant == "stripped" else it["prompt"]
                text, n_new = self._greedy(prompt, p["max_new_tokens"])
                verdict = judge(text, it["answer"], it["swap_answer"])
                retried = False
                if not verdict["C"] and n_new >= p["max_new_tokens"] and not ends_sentence(text):
                    text, n_new = self._greedy(prompt, p["max_new_tokens_retry"])  # ran out of room: longer
                    verdict, retried = judge(text, it["answer"], it["swap_answer"]), True
                rows.append(
                    {
                        "name": it["name"],
                        "variant": variant,
                        "category": it["category"],
                        "answer": it["answer"],
                        "swap_answer": it["swap_answer"],
                        "status_b": it["status"],
                        "label_b": it["label"],
                        "continuation": text,
                        "n_new_tokens": n_new,
                        "retried": retried,
                        **verdict,
                    }
                )
        self.save_jsonl("items.jsonl", rows)
        summary = {"model": self.cfg.model.name, "sanity": sanity, "max_new_tokens": p["max_new_tokens"]}
        summary |= {v: summarize([r for r in rows if r["variant"] == v]) for v in p["variants"]}
        self.path("review.md").write_text(review_md(rows, p["variants"]))
        return summary

    @torch.no_grad()
    def _greedy(self, prompt: str, max_new: int) -> tuple[str, int]:
        ids = self.model.lm.encode(prompt)
        hf: Any = self.model.hf  # PreTrainedModel.generate is mistyped for pyright
        out = hf.generate(
            input_ids=ids,
            attention_mask=torch.ones_like(ids),
            max_new_tokens=max_new,
            do_sample=False,
            pad_token_id=self.model.tokenizer.eos_token_id,
        )
        new = out[0, ids.shape[1] :]
        return self.model.tokenizer.decode(new, skip_special_tokens=True), int(new.shape[0])


# ---- judging (pure; unit-tested) ---------------------------------------------------------------


def ends_sentence(text: str) -> bool:
    return bool(re.search(r"[.!?\n]", text))


def first_clause(text: str) -> str:
    """The continuation up to its first sentence end or line break (later text is a new statement). Leading
    whitespace and line breaks are skipped first, so a continuation that starts on a new line is not empty."""
    return re.split(r"(?<!\d)[.!?](?!\d)|\n", text.lstrip(), maxsplit=1)[0]


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def number_words(n: int) -> list[str]:
    if n < 20:
        return [_ONES[n]]
    tens, ones = divmod(n, 10)
    return [_TENS[tens]] + ([_ONES[ones]] if ones else []) if n < 100 else [str(n)]


def answer_forms(answer: str) -> list[list[str]]:
    """Word sequences that count as the answer: the answer itself and, for numbers, the numeral / number word."""
    forms = [words(answer)]
    a = answer.strip().lower()
    if a.isdigit():
        forms.append(number_words(int(a)))
    elif a in _ONES:
        forms.append([str(_ONES.index(a))])
    elif a in _TENS[2:]:
        forms.append([str(10 * _TENS.index(a))])
    return forms


def find(ws: list[str], answer: str) -> str | None:
    """'word' if a form of `answer` occurs as a contiguous word sequence, 'compound' if a single word ends with it
    (answers of 4+ letters, after a 3+ letter prefix: drumsticks, not hund-red), else None."""
    for form in answer_forms(answer):
        n = len(form)
        if any(ws[i : i + n] == form for i in range(len(ws) - n + 1)):
            return "word"
    a = answer.strip().lower()
    if len(a) >= 4 and a.isalpha() and any(w.endswith(a) and len(w) - len(a) >= 3 for w in ws):
        return "compound"
    return None


def judge(continuation: str, answer: str, swap_answer: str) -> dict[str, Any]:
    ws = words(first_clause(continuation))
    content = [w for w in ws if w not in ARTICLES]
    forms = answer_forms(answer)
    match = find(ws, answer)
    swap = find(ws, swap_answer)
    return {
        "A": bool(ws) and any(ws[: len(f)] == f for f in forms),
        "B": bool(content) and any(content[: len(f)] == f for f in forms),
        "C": match is not None,
        "match": match,
        "swap_also": swap is not None,
        "ambiguous": match is not None and swap is not None,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [r for r in rows if r["status_b"] == "eligible"]
    c = {r["name"] for r in rows if r["C"] and not r["ambiguous"]}
    e = {r["name"] for r in eligible}
    return {
        "n": len(rows),
        "correct": {k: sum(r[k] for r in rows) for k in ("A", "B", "C")},
        "ambiguous": sorted(r["name"] for r in rows if r["ambiguous"]),
        "compound_matches": sorted(r["name"] for r in rows if r["match"] == "compound"),
        "retried": sum(r["retried"] for r in rows),
        "vs_part_b_eligible": {
            "both": len(c & e),
            "only_C": sorted(c - e),  # correct by continuation, not eligible in part B
            "only_part_b": sorted(e - c),  # eligible in part B, not correct by continuation
        },
        "status_b_of_only_C": {r["name"]: r["status_b"] for r in rows if r["name"] in c - e},
    }


def review_md(rows: list[dict[str, Any]], variants: list[str]) -> str:
    """Items for a human to read: C disagrees with part B's eligible, compound matches, ambiguous ones."""
    out = ["# exp13 review", "", "Read each continuation and decide whether the model answered the question.", ""]
    for v in variants:
        vr = [r for r in rows if r["variant"] == v]
        flagged = [
            r for r in vr
            if (r["C"] and not r["ambiguous"]) != (r["status_b"] == "eligible") or r["match"] == "compound" or r["ambiguous"]
        ]  # fmt: skip
        out += [f"## {v} ({len(flagged)} to review)", "", "| item | part B | answer | continuation | C | match | swap answer also |",
                "|---|---|---|---|---|---|---|"]  # fmt: skip
        for r in flagged:
            cont = r["continuation"].replace("|", "\\|").replace("\n", "⏎")
            out.append(
                f"| `{r['name']}` | {r['status_b']} | {r['answer']} | `{cont}` | {'yes' if r['C'] else 'no'} | "
                f"{r['match'] or '-'} | {r['swap_answer'] if r['swap_also'] else '-'} |"
            )
        out.append("")
    return "\n".join(out)
