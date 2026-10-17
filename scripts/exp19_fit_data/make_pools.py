"""exp19_fit_data: build the lens-fitting prompt pools, one JSON list of 1000 texts per condition.

Run with the jpp_lens venv (it has `datasets` and `transformers`), from anywhere:
    python scripts/exp19_fit_data/make_pools.py OUT_DIR

Pools (each the first 1000 qualifying records of its stream, in stream order, as J++'s WikiText loader takes them):
  wiki_a  WikiText-103 train records of >= 600 characters: exactly the J++ recipe's pool (jlens.examples)
  wiki_b  the next 1000 such WikiText records (disjoint from wiki_a): the noise floor between two WikiText fits
  math    open-web-math/open-web-math train records of >= 600 characters
  chat    HuggingFaceH4/ultrachat_200k train_sft conversations rendered with Qwen3.6-27B's chat template (thinking
          off, as our brew prompts), >= 600 characters
  mix     wiki_a, math and chat interleaved (record k of each, in that order), so its first 25 are 9 + 8 + 8
Texts are cut at 2000 characters: the fit reads only the first 128 tokens (J++ recipe), well inside that.
"""

import json
import sys
from pathlib import Path

from datasets import load_dataset
from transformers import AutoTokenizer

N = 1000
MIN_CHARS = 600
CUT = 2000
QWEN = ("Qwen/Qwen3.6-27B", "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9")


def first(stream, text_of, n, skip=0):
    out, seen = [], 0
    for record in stream:
        text = text_of(record)
        if text is None or len(text.strip()) < MIN_CHARS:
            continue
        seen += 1
        if seen <= skip:
            continue
        out.append(text[:CUT])
        if len(out) == n:
            return out
    raise RuntimeError(f"stream ended after {len(out)} records")


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    wiki = lambda: load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train", streaming=True)  # noqa: E731
    pools = {
        "wiki_a": first(wiki(), lambda r: r["text"], N),
        "wiki_b": first(wiki(), lambda r: r["text"], N, skip=N),
        "math": first(
            load_dataset("open-web-math/open-web-math", split="train", streaming=True), lambda r: r["text"], N
        ),
    }
    tok = AutoTokenizer.from_pretrained(QWEN[0], revision=QWEN[1])

    def render(record):
        try:
            return tok.apply_chat_template(record["messages"], tokenize=False, enable_thinking=False)
        except Exception:  # a malformed conversation is skipped, not fatal
            return None

    pools["chat"] = first(load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft", streaming=True), render, N)
    pools["mix"] = [pools[name][k] for k in range(N) for name in ("wiki_a", "math", "chat")][:N]
    for name, texts in pools.items():
        assert len(texts) == N, name
        (out_dir / f"{name}.json").write_text(json.dumps(texts, ensure_ascii=False))
        print(name, len(texts), "texts; first:", repr(texts[0][:80]))
    assert not set(pools["wiki_a"]) & set(pools["wiki_b"]), "wiki_a and wiki_b overlap"


if __name__ == "__main__":
    main(Path(sys.argv[1]))
