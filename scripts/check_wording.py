"""check_wording: reader-facing text does not say "loss" (a TA read it as training loss; Dan 30 Oct) and does not say "kept"
next to a switch or an answer (Dan 30 Oct: "still switched" / "switch blocked", "answers unchanged", "retained").

The band measure is an "accuracy drop (points)", the one-layer measure "switches blocked beyond a random part", both
together "the effect". Only a training or fitting loss (the J++ lens fit) may say "loss": a line that mentions the fit or
training is let through. Source comments (`<!-- src: ... -->`), template markers, code spans and link targets are not
reader-facing and are skipped; data keys keep their names.

uv run python scripts/check_wording.py     # the READMEs, the ledger and the glossary; exit 1 on a hit
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FILES = (REPO / "README.md", REPO / "docs" / "depth" / "README.md", REPO / "docs" / "breadth" / "README.md",
         REPO / "docs" / "depth" / "EXPERIMENTS.md", REPO / "docs" / "shared" / "glossary_joint.md",
         REPO / "docs" / "readme" / "README.template.md", REPO / "docs" / "depth" / "README.template.md",
         REPO / "docs" / "breadth" / "README.template.md", REPO / "docs" / "depth" / "x0_details.md",
         REPO / "docs" / "depth" / "x0_details.template.md", REPO / "docs" / "depth" / "digest.md")  # fmt: skip
LOSS = re.compile(r"\b(loss|lose|loses|lost|losing)\b", re.I)
# "kept" within three words of switch / switched / answer(s), either side: ambiguous (a switch that survives an arm, an answer that
# stayed, a part that was retained); other meanings ("the run kept the ids") are not matched
KEPT = re.compile(r"\b(?:switch\w*|answers?)\b(?:\W+\w+){0,3}?\W+kept\b|\bkept\b(?:\W+\w+){0,3}?\W+\b(?:switch\w*|answers?)\b", re.I)
FIT = re.compile(r"\b(fit|fitting|training)\b", re.I)
SKIP = re.compile(r"<!--.*?-->|\{\{.*?\}\}|`[^`\n]*`|\]\([^)]*\)", re.S)


def _clean(text: str) -> list[str]:
    return SKIP.sub(lambda m: " " * len(m.group(0)) if "\n" not in m.group(0) else "\n" * m.group(0).count("\n"), text).split("\n")


def kept_words(text: str) -> list[str]:
    """'line N: …context…' for every "kept" next to a switch or an answer in reader-facing text."""
    found = []
    for n, line in enumerate(_clean(text), 1):
        for m in KEPT.finditer(line):
            found.append(f"line {n}: …{line[max(0, m.start() - 20) : m.end() + 20].strip()}…")
    return found


def loss_words(text: str) -> list[str]:
    """'line N: …context…' for every reader-facing use of the word loss (or lose, lost, losing) outside a fit."""
    found = []
    for n, line in enumerate(SKIP.sub(lambda m: " " * len(m.group(0)) if "\n" not in m.group(0) else "\n" * m.group(0).count("\n"), text).split("\n"), 1):
        if FIT.search(line):
            continue
        for m in LOSS.finditer(line):
            found.append(f"line {n}: …{line[max(0, m.start() - 40) : m.end() + 40].strip()}…")
    return found


def main() -> int:
    bad = 0
    for path in FILES:
        if path.exists():
            body = path.read_text(encoding="utf-8")
            hits = loss_words(body) + kept_words(body)
            bad += len(hits)
            for h in hits:
                print(f"{path.relative_to(REPO)}: {h}")
    print(f"check_wording: {bad} use(s) of loss / kept")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
