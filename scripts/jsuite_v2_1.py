"""jsuite_v2_1 (Zach, 2026-10-24, prereg amendment 35): v2 plus the one condition only v1 had, so v1 can be retired.

v1's recalled start never named the bridge in its memory finals (MM, MA); v2 names it once in every final (a neutral
sentence where it has no final-hop fact), to remove the audit's mention confound. v1's no-mention recall is what put the
recalled bridge's dependence in the question span (amendment 30). v2.1 keeps every v2 item unchanged (same ids, so runs on
v2 stay valid) and adds start R: each v2 recalled-start memory item (MM, MA, MN) with its one neutral bridge sentence
deleted, the rest of the scene identical. Words RM, RA, RN (memory finals only: P and K state facts by the bridge's
name); scene = the M scene + "/R", so R items are eligible as their own scene. RM - MM etc. is the effect of the bridge
being named once in passing.

python scripts/jsuite_v2_1.py   (reads jsuite_v2_{dev,test}_chat, writes jsuite_v2_1_{dev,test}_chat)
"""

from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import jsuite_v2_tables as TB  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def drop_sentence(ctx: str, sent: str) -> str:
    """Remove one sentence from a passage: a "- " bullet line (notes genre) or a sentence inside prose."""
    if ("\n- " + sent) in ctx:
        return ctx.replace("\n- " + sent, "", 1)
    if (sent + " ") in ctx:
        return ctx.replace(sent + " ", "", 1)
    if (" " + sent) in ctx:
        return ctx.replace(" " + sent, "", 1)
    return ctx.replace(sent, "", 1)


def main() -> None:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    for sp in ("dev", "test"):
        items = [json.loads(line) for line in (DATA / f"jsuite_v2_{sp}_chat" / "items.jsonl").read_text().splitlines()]
        new = []
        for it in items:
            if it.get("module") != "facts" or it["start"] != "M" or it["final"] not in "MAN":
                continue
            t = TB.REL2[it["relation"]]
            sent = t["nfact"][it["wording"]].format(x=it["bridge"], X=cap(it["bridge"]))
            assert it["context"].count(sent) == 1, (it["id"], sent)
            ctx = drop_sentence(it["context"], sent)
            n_bridge = len(re.findall(r"(?i)\b" + re.escape(it["bridge"]) + r"\b", ctx))
            assert n_bridge == 0, (it["id"], n_bridge)
            vocab = it["answer_vocab"]
            assert it["final"] == "A" or not re.search(r"(?i)\b" + re.escape(it["real"]) + r"\b", ctx), it["id"]
            assert it["final"] != "N" or not any(re.search(r"(?i)\b" + re.escape(w) + r"\b", ctx) for w in vocab), it["id"]
            r = {**it, "id": it["id"].replace(":facts:M", ":facts:R"), "word": "R" + it["final"], "start": "R", "context": ctx,
                 "bridge_in_passage": False, "bridge_mentions": 0, "scene": it["scene"] + "/R", "derived_from": it["id"]}  # fmt: skip
            r["steps"] = [{**r["steps"][0], "source": "R"}, r["steps"][1]]
            new.append(r)
        out = DATA / f"jsuite_v2_1_{sp}_chat"
        assert not out.exists(), f"{out} exists; sets are written once"
        out.mkdir(parents=True)
        allit = items + new
        ids = [it["id"] for it in allit]
        assert len(ids) == len(set(ids))
        (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in allit))
        man = {"set": out.name, "from": f"jsuite_v2_{sp}_chat", "split": sp, "n": len(allit), "added_R": len(new),
               "words": dict(collections.Counter(it["word"] for it in allit)), "git_commit": commit, "script": "scripts/jsuite_v2_1.py"}  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
        print(out.name, len(allit), "items;", len(new), "R items", dict(collections.Counter(it["word"] for it in new)))


if __name__ == "__main__":
    main()
