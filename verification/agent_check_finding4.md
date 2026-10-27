# Agent check, finding 4: a lookup ends in a late attention read of the answer's sentence

Date: 23 Oct 2026, about 11:00-12:00 UTC. Recomputed at repo commit 4cf5d35 (HEAD then; the saved runs under `results/` are unchanged by it). Packet: [finding4_2026-10-23/](finding4_2026-10-23/) (claim.md, recompute.py, checklist.md). This is an agent check, not a human verification: the finding stays UNVERIFIED until a human adds it to VERIFIED.md.

What was recomputed: every cell of this finding in `results/cross_model/20261023T091847Z/grid.csv` (the grid README cites): 8 models x draws 1-3, prose / table / JSON, and the long context. From the raw `rows.jsonl` and `cases.jsonl` of each run, with an independent script (standard library only, no repo code): n, % right with the answer's sentence blocked from the last tokens in every attention layer (every layer on attention-only models), its Wilson 95% interval, the off-path sentence blocked instead, the DeltaNet layers blocked instead (hybrids), and the verdict by the late-read rule fixed on 22 Oct (`jobs/d2/d2_late_read_seed2_27b.yaml`, 6538445; per format `jobs/d2/d2_formats_27b.yaml`, 444500e).

Result: 51 of 51 cells match (n, value, interval, verdict, and the control numbers printed in grid.csv); 5 cells have no run (draw 3 on 27B, Olmo-Hybrid, 122B: no spec; long context on Olmo-Hybrid: running, on Gemma: failed). The same 51 match the newer grid `20261023T104743Z`, whose rows for this finding are identical. Verdicts: 38 holds, 6 fails (Gemma draws 1-2, prose, JSON; the 27B long context; Olmo-Hybrid tables), 5 not interpretable (small n), 2 not testable.

Found while checking (no number changes):

- grid.csv writes "chance 20%" for every cell, but the prose, table and JSON scenes have 3 facts (chance 33%). Gemma's JSON cell (21% [13, 34]), footnoted "at chance", is below chance there.
- Hook checks pass on all 57 runs of findings 3-4 (`check.json`: `passed`, no-op 0.0); the `correct` field equals (top == answer token) on all 1,089,871 rows; 96% of the wrong answers under the block are another digit of the list.
- The first draws ran under an older rule and are judged by the 22 Oct rule (choice after the data, accepted by Dan; README footnotes).
- Older packet for the 27B and 32B: [finding4_late_read.md](finding4_late_read.md) (kept).
