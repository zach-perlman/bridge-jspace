"""v3_relafter (Zach, 2026-10-28, prereg amendment 58 note 12): rendering A, the relation after the bridge everywhere.

Rendering 0's RM, MM and PM items (final M) with the question re-rendered by its relation's relation-after template
(jsuite_v3_tables q2M[2]: "{D} was of which nationality?", "{D} is in which country?", "{D} comes from which country?",
"{D} was directed by whom?"), so the question names what to recall only after the bridge or its description. The
passage, ids, bridge, description, hops and vocabulary are unchanged; hop 2 alone and the guess question get the same
template (hop 1 is unchanged). Items already in that form are kept as they are. Every converted question is checked to
re-render exactly from its rendering-0 template first. Writes data/tasks_v2/jsuite_v3ra_test_chat. CPU only.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
import jsuite_v3_tables as T3  # noqa: E402

D = ROOT / "data" / "tasks_v2"
AFTER = 2  # q2M[2] starts with "{D}" for every relation (checked below)


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def fill(tpl: str, d: str) -> str:
    return tpl.format(d=d, D=cap(d))


def unfill(tpl: str, text: str) -> str:
    """The description a template was filled with."""
    rx = re.escape(tpl).replace(re.escape("{d}"), "(?P<d>.+)").replace(re.escape("{D}"), "(?P<d>.+)")
    m = re.fullmatch(rx, text)
    assert m, (tpl, text)
    d = m.group("d")
    return d[0].lower() + d[1:] if tpl.startswith("{D}") else d


def main() -> None:
    tables = T3.tables()
    for rel, t in tables.items():
        assert t["q2M"][AFTER].startswith("{D}"), rel
    out, moved = [], 0
    for line in (D / "jsuite_v3_test_chat" / "items.jsonl").open():
        it = json.loads(line)
        if it.get("module") != "facts" or it["word"] not in ("RM", "MM", "PM"):
            continue
        q2 = tables[it["relation"]]["q2M"]
        w, desc = it["wording"], it["start_desc"]
        assert it["question"] == fill(q2[w], desc), (it["id"], it["question"])
        gd = unfill(q2[w], it["guess_question"])
        s2 = it["steps"][1]
        assert s2["question"] == fill(q2[w], it["bridge"]), (it["id"], s2["question"])
        new = {**it, "question": fill(q2[AFTER], desc), "guess_question": fill(q2[AFTER], gd),
               "steps": [it["steps"][0], {**s2, "question": fill(q2[AFTER], it["bridge"])}], "rendering": "A"}  # fmt: skip
        moved += new["question"] != it["question"]
        out.append(new)
    d = D / "jsuite_v3ra_test_chat"
    d.mkdir(exist_ok=True)
    (d / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    print(f"{len(out)} items ({moved} re-rendered, {len(out) - moved} already relation-after)")
    for w in ("RM", "MM", "PM"):
        x = next(x for x in out if x["word"] == w)
        print(f"  {w}: {x['question']} | hop 2: {x['steps'][1]['question']} | guess: {x['guess_question']}")


if __name__ == "__main__":
    main()
