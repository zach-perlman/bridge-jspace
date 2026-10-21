"""Merge tasks_v2 sets into one (Zach, 2026-10-21: the full v8 set). make() cannot put the controlled tier (with
counterfactuals) and the knock-out tier in one call, and the knock-out tier has no hard cues, so M-start words exist
there at levels 0-1 only; the full set is made in parts and merged here. Item and scene ids restart at 0 in each part,
so they are prefixed with the part's tag ("cf:PP-L0-0000"); every other field is unchanged. Write-once.

python scripts/merge_tasks_sets.py --out NAME TAG=SET [TAG=SET ...]
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import tasks_v2 as T


def main(out: str, parts: list[str]) -> None:
    dst = T.DATA / out
    assert not dst.exists(), f"{dst} exists; sets are written once"
    items, sources = [], {}
    for part in parts:
        tag, name = part.split("=", 1)
        path = T.DATA / name / "items.jsonl"
        sources[tag] = {"set": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "manifest": json.loads((T.DATA / name / "manifest.json").read_text())}  # fmt: skip
        for it in T.load(name):
            items.append({**it, "id": f"{tag}:{it['id']}", "scene": f"{tag}:{it['scene']}", "part": tag})
    assert len({it["id"] for it in items}) == len(items), "duplicate ids after prefixing"
    dst.mkdir(parents=True)
    (dst / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    count = collections.Counter
    (dst / "manifest.json").write_text(json.dumps({
        "set": out, "merged_from": sources, "n_items": len(items),
        "per_word": count(it["word"] for it in items), "per_domain": count(it["domain"] for it in items),
        "per_level": count(str(it["level"]) for it in items), "per_format": count(it["format"] for it in items),
        "with_counterfactuals": sum("cf_context" in it for it in items),
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    print(f"wrote {dst / 'items.jsonl'}: {len(items)} items from {len(parts)} parts")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("parts", nargs="+")
    a = ap.parse_args()
    main(a.out, a.parts)
