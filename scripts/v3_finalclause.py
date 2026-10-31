"""v3_finalclause (Zach, 2026-10-28, prereg amendment 58 note 9 addendum): WorkspaceBench's "final clause only" gate for
the never-named items. Each RM question with its description cut to its role noun ("Which nationality was the novelist
who wrote Arrow of God?" -> "Which nationality was the novelist?"), same passage, same answer and vocabulary. Writes
data/tasks_v2/jsuite_v3fc_test_chat (word FC, ids RM-id + ":FC"). CPU only.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"


def main() -> None:
    out = []
    for line in (ROOT / "jsuite_v3_test_chat" / "items.jsonl").open():
        it = json.loads(line)
        if it.get("module") != "facts" or it["word"] != "RM":
            continue
        desc = it["start_desc"]
        noun = re.split(r" (?:who|that) ", desc, maxsplit=1)[0]  # "the novelist"
        m = re.search(re.escape(desc), it["question"], flags=re.IGNORECASE)
        assert m, (it["id"], desc, it["question"])
        rep = noun[0].upper() + noun[1:] if it["question"][m.start()].isupper() else noun
        q = it["question"][: m.start()] + rep + it["question"][m.end() :]
        out.append({**it, "id": it["id"] + ":FC", "word": "FC", "scene": it["scene"] + ":FC", "question": q})
    d = ROOT / "jsuite_v3fc_test_chat"
    d.mkdir(exist_ok=True)
    (d / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    print(len(out), "items;", " | ".join(x["question"] for x in out[:2]), "|", next(x["question"] for x in out if x["relation"] == "landmarks"))


if __name__ == "__main__":
    main()
