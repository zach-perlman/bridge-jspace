"""Readability measures of a README, on the text a reader sees (readability brief, 8 Nov): HTML comments, code blocks
and image links stripped; "outside" = outside <details> folds.

  words            words outside folds / in total
  slash lists      per-model lists ("0.50 / 0.74 / 0.75 ○ / …": two or more numbers joined by " / ")
  long sentences   sentences over 30 and over 40 words, outside folds (tables and headings are not sentences)
  colons           colons outside folds
  captions         the italic line right under an image: mean and longest, in words
  ledger labels    notation the reader was not given (H0–H3, C1–C3, C2′, E1–E4, batch ids, "claim N"), outside link text

uv run python scripts/readme_lint.py [README.md docs/depth/README.md …]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TARGETS = {"words_outside": 2000, "words_total": 5000, "slash_outside": 0, "long30": 5, "long40": 0,
           "colons_outside": 25, "caption_mean": 50, "caption_max": 80, "labels": 0}  # fmt: skip
NUM = r"[−-]?\d+(?:\.\d+)?%?"
SLASH = re.compile(rf"{NUM}(?:\s*\[[^\]]*\])?(?:\s*○)?(?:\s*/\s*{NUM}(?:\s*\[[^\]]*\])?(?:\s*○)?){{1,}}")
LABEL = re.compile(r"(?<![\w-])(?:H[0-3]|C[1-3]′?|E[1-4]|[bt]\d{2}-\w+|claim \d+|claims \d+(?:, \d+)*)(?![\w-])")
WORD = re.compile(r"\w[\w'’.-]*")


def visible(text: str) -> str:
    for pat in (r"<!--.*?-->", r"```.*?```"):
        text = re.sub(pat, " ", text, flags=re.S)
    return text


def split_folds(text: str) -> tuple[str, str]:
    """(outside folds, inside folds)."""
    inside = " ".join(re.findall(r"<details>.*?</details>", text, flags=re.S))
    return re.sub(r"<details>.*?</details>", " ", text, flags=re.S), inside


def prose(text: str) -> str:
    """Text without images, link targets, headings, table rows and summary tags."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"</?(details|summary)>", " ", text)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith(("#", "|"))]
    return "\n".join(lines)


def words(text: str) -> int:
    """Every visible word, table cells included (headings and image links are not counted)."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"</?(details|summary)>", " ", text)
    return len(WORD.findall(text))


def sentences(text: str) -> list[str]:
    out = []
    for block in re.split(r"\n\s*\n|\n\s*[-*] ", prose(text)):
        block = " ".join(block.split())
        out += [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(\"“*])", block) if s.strip()]
    return out


def captions(text: str) -> list[int]:
    lines = text.splitlines()
    out = []
    for i, ln in enumerate(lines):
        if not re.match(r"\s*!\[[^\]]*\]\(", ln):
            continue
        for nxt in lines[i + 1 : i + 3]:
            s = nxt.strip()
            if s.startswith("*") and s.endswith("*") and len(s) > 2:
                out.append(len(WORD.findall(s)))
                break
    return out


def measure(path: Path) -> dict[str, float]:
    text = visible(path.read_text(encoding="utf-8"))
    out_, in_ = split_folds(text)
    sl = sentences(out_)
    caps = captions(text)
    link_free = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", prose(out_))
    return {
        "words_outside": words(out_), "words_total": words(out_) + words(in_),
        "slash_outside": len(SLASH.findall(prose(out_))), "slash_total": len(SLASH.findall(prose(text))),
        "long30": sum(len(WORD.findall(s)) > 30 for s in sl), "long40": sum(len(WORD.findall(s)) > 40 for s in sl),
        "colons_outside": prose(out_).count(":"),
        "caption_mean": round(sum(caps) / len(caps), 1) if caps else 0, "caption_max": max(caps, default=0),
        "labels": len(LABEL.findall(link_free)),
    }  # fmt: skip


def main(paths: list[str]) -> int:
    over = 0
    for p in paths or ["README.md"]:
        m = measure(REPO / p)
        print(p)
        for k, v in m.items():
            t = TARGETS.get(k)
            flag = "" if t is None else ("  ok" if v <= t else f"  over (target ≤ {t})")
            over += bool(t is not None and v > t)
            print(f"  {k:15} {v}{flag}")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
