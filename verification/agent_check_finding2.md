# Agent check, finding 2 on Qwen3.6-27B: a lookup ignores the lens-readable part of a stated bridge

Date: 23 Oct 2026, about 11:00-12:00 UTC. Recomputed at repo commit 4cf5d35 (HEAD then; the saved runs under `results/` are unchanged by it). Packet: [finding2_2026-10-23/](finding2_2026-10-23/) (claim.md, recompute.py, checklist.md). Qwen3.6-27B only, at Dan's request. This is an agent check, not a human verification: the finding stays UNVERIFIED until a human adds it to VERIFIED.md.

What was recomputed: the 11 Qwen3.6-27B cells of this finding in `results/cross_model/20261023T091847Z/grid.csv` (the grid README cites): draw 1, draw 2 and its three topics, tables, JSON (J++), and draw 2 with its three topics for the plain J-lens listed beside. From the raw `outcomes.jsonl` of each parts run (`source == "cf"`, not null, the context at layer 32; PP = lookups, PM = recalls, role b = switched) and the item files for topic and format, with an independent script (standard library only, no repo code): the lens-readable part (jspace), the rest (not_jspace), the whole change (full) and the same-share random part (jspace_matched) on lookups and recalls, Wilson intervals, and the verdict by `scripts/d1_verdict.py`'s replication rule (specs 3e90959, a786b36, dbc4527).

Result: 11 of 11 cells match (n, value, interval, verdict, the recall control and the rest printed in grid.csv). Against the newer grid `20261023T104743Z`, which adds the same-share random part to the control text, 11 of 11 also match, including those values. Verdicts: 8 holds (J++: draws 1-2, three topics, tables, JSON), 3 not interpretable (plain J-lens: its recall control fails pooled and on two topics).

Key numbers (J++): the lens part switches 0-3% of lookups and 36-42% of recalls; the rest 81-96% of lookups; the whole change 83-98% of lookups and 78-93% of recalls; the same-share random part 0% of lookups and 0-2% of recalls.

Note: `scripts/d1_verdict.py` has uncommitted edits in the working tree today; the rule was read from HEAD.
