"""v3_mp (Zach, 2026-10-28, prereg amendment 58 note 13): the latent first hop into an in-context second hop.

Rendering 0's MP items: the question describes the bridge ("Which nationality is the actor cast as the novelist who
wrote Things Fall Apart in the new film?"), and the passage gives every scene entity a made-up value ("The upcoming
biopic casts a Swedish actor as Achebe. ... a Mexican actor as Nobel."), so the answer is in context, arbitrary, and
not the bridge's remembered attribute. The generator stores hop 2 as the memory question; here hop 2 is the passage
lookup with the bridge named (the question's own template, d = the bridge), answer = the bridge's passage value. Each
item also records every scene entity's passage value ("passage_values", parsed by jswap.pfact_value and checked against
the answer). Writes data/tasks_v2/jsuite_v3mp_test_chat. CPU only.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
import jsuite_v3_tables as T3  # noqa: E402

from scripts import jswap as JS  # noqa: E402

D = ROOT / "data" / "tasks_v2"


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def main() -> None:
    tables = T3.tables()
    out = []
    for line in (D / "jsuite_v3_test_chat" / "items.jsonl").open():
        it = json.loads(line)
        if it.get("module") != "facts" or it["word"] != "MP":
            continue
        t, w = tables[it["relation"]], it["wording"]
        assert it["question"] == t["q2P"][w].format(d=it["start_desc"], D=cap(it["start_desc"])), it["id"]
        vals = {e: JS.pfact_value(t["pfact"][w], it["context"], e, it["answer_vocab"], the=True) for e in it["entities"]}
        assert vals[it["bridge"]] == it["answer"], (it["id"], vals)
        assert all(vals.values()), (it["id"], vals)
        s2 = {"question": t["q2P"][w].format(d=it["bridge"], D=cap(it["bridge"])), "answer": it["answer"], "kind": "open", "source": "P",
              "cand_vocab": it["answer_vocab"]}  # fmt: skip
        out.append({**it, "steps": [it["steps"][0], s2], "passage_values": vals})
    d = D / "jsuite_v3mp_test_chat"
    d.mkdir(exist_ok=True)
    (d / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    x = out[0]
    print(f"{len(out)} MP items | {x['question']} | hop 1: {x['steps'][0]['question']} | hop 2: {x['steps'][1]['question']} -> {x['answer']} | {x['passage_values']}")


if __name__ == "__main__":
    main()
