"""mm_absent (Zach, 2026-10-23, prereg amendment 10): full_v8's M->M items with the bridge never mentioned in the context.
In tasks_v2 every scene states the start thing's pick and locker, so an M->M item's "recalled" bridge also sits in the
prompt (112/112 in full_v8). Here each M->M context loses every sentence, table row, JSON record or code entry that
names its bridge; nothing else changes (question, steps, ids). The C and O variants are dropped (their contexts name
other bridges); C1 does not use them. Items where a mention survives are left out.

python scripts/mm_absent.py SRC DST      e.g. full_v8 full_v8_mmabs (data/tasks_v2/DST/items.jsonl, write-once)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"


def mentions(text: str, word: str) -> bool:
    return re.search(r"(?i)(?<![A-Za-z])" + re.escape(word) + r"(?![A-Za-z])", text) is not None


def strip_bridge(context: str, bridge: str) -> str:
    out_lines = []
    for line in context.split("\n"):
        if not mentions(line, bridge):
            out_lines.append(line)
            continue
        s = line.strip()
        if s.startswith("|"):  # a table row naming the bridge
            continue
        if s.startswith("[") and s.endswith("]"):  # a JSON list of records
            recs = re.findall(r"\{[^{}]*\}", s)
            keep = [r for r in recs if not mentions(r, bridge)]
            out_lines.append("[" + ", ".join(keep) + "]")
            continue
        if "{" in s and "}" in s and "=" in s:  # a Python dict line
            head, body = s.split("{", 1)
            body, tail = body.rsplit("}", 1)
            entries = re.findall(r"'[^']*'\s*:\s*'[^']*'", body)
            keep = [e for e in entries if not mentions(e, bridge)]
            out_lines.append(head + "{" + ", ".join(keep) + "}" + tail)
            continue
        sents = re.split(r"(?<=[.!?])\s+", line)  # prose, chat, document
        out_lines.append(" ".join(x for x in sents if not mentions(x, bridge)))
    return "\n".join(out_lines)


def main(src: str, dst: str) -> None:
    out = DATA / dst
    assert not out.exists(), f"{out} exists; sets are written once"
    items = [json.loads(line) for line in (DATA / src / "items.jsonl").read_text().splitlines()]
    kept, left_out = [], 0
    for it in items:
        if it["word"] != "MM":
            continue
        bridge = it.get("bridge") or it["steps"][0]["answer"]
        ctx = strip_bridge(it["context"], bridge)
        if mentions(ctx, bridge) or any(mentions(ctx, b) for b in (it.get("bridges") or [])):
            left_out += 1
            continue
        new = {k: v for k, v in it.items() if not k.startswith(("cf_", "off_"))}
        new["context"] = ctx
        new["context_original_has_bridge"] = mentions(it["context"], bridge)
        new["mm_absent_from"] = src
        kept.append(new)
    out.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in kept))
    (out / "manifest.json").write_text(json.dumps({"set": dst, "from": src, "n": len(kept), "left_out": left_out,
                                                   "script": "scripts/mm_absent.py"}, indent=2) + "\n")  # fmt: skip
    print(f"{dst}: {len(kept)} M->M items with the bridge removed from the context ({left_out} left out)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
