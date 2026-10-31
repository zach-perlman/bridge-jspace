"""v3_probes_b (Zach, 2026-10-28, prereg amendment 58 note 9): the skip-the-bridge probes in a second wording.

From data/tasks_v2/jsuite_v3probes_test_chat (wording A: "Which nationality is most associated with {cue}?"), writes
data/tasks_v2/jsuite_v3probesB_test_chat with wording B: "{Cue} is most associated with which nationality?" (country,
film director as A). Same ids with ":B", same answers and vocabularies. CPU only.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
REL = {"people": "nationality", "films": "film director"}


def main() -> None:
    src = [json.loads(line) for line in (ROOT / "jsuite_v3probes_test_chat" / "items.jsonl").open()]
    out = []
    for it in src:
        cue = it["skip_cue"]
        q = f"{cue[0].upper() + cue[1:]} is most associated with which {REL.get(it['relation'], 'country')}?"
        out.append({**it, "id": it["id"] + ":B", "scene": it["scene"] + ":B", "question": q})
    d = ROOT / "jsuite_v3probesB_test_chat"
    d.mkdir(exist_ok=True)
    (d / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    print(len(out), "probes;", out[0]["question"], "|", out[-1]["question"])


if __name__ == "__main__":
    main()
