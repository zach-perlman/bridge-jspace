# Agent check, finding 3: the last tokens read the answer's digit, not the entity's name

Date: 23 Oct 2026, about 11:00-12:00 UTC. Recomputed at repo commit 4cf5d35 (HEAD then; the saved runs under `results/` are unchanged by it). Packet: [finding3_2026-10-23/](finding3_2026-10-23/) (claim.md, recompute.py, checklist.md). This is an agent check, not a human verification: the finding stays UNVERIFIED until a human adds it to VERIFIED.md.

What was recomputed: every cell of this finding in `results/cross_model/20261023T091847Z/grid.csv` (the grid README cites): 8 models x draws 1-3 of the sentence lists and the prose, table and JSON scenes. From the raw `rows.jsonl` and `cases.jsonl` of each run, with an independent script (standard library only, no repo code): n, % right with the sentence without its name hidden from the last tokens, its Wilson 95% interval, the sentence without its digit hidden, the off-path controls at both destinations, and the verdict by the rule fixed before the runs (`scripts/d2_parts.py`, 5cb6a87; per format `jobs/d2/d2_formats_27b.yaml`, 444500e).

Result: 45 of 45 cells match (n, value, interval, verdict, and the control numbers printed in grid.csv); 3 cells have no run (no spec). The same 45 match the newer grid `20261023T104743Z`, whose rows for this finding are identical. Verdicts: 39 holds, 1 fails (Muse prose, 5 items), 3 not interpretable, 2 not testable.

Found while checking (no number changes):

- grid.csv's control text for the not-interpretable format cells ("off-path parts hidden: lowest 100%") shows only the last tokens; the failing control is at the question's tokens (86-89%). The verdicts are right (`scripts/cross_model_grid.py` `parts_row` keys the off-path rates by source only).
- The prose, table and JSON scenes have 3 facts, not 5, so guessing there is 33%; the 35% bar is at chance in those cells (Gemma prose: 34%, holds).
- On Muse about 10% of the sentence-list prompts carry the answer's digit twice (the system prompt's dates); Muse's rates with the digit hidden are still 1-3%.
- Older packet for the 27B and 32B: [finding3_name_vs_digit.md](finding3_name_vs_digit.md) (kept).
