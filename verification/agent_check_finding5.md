# Agent check, finding 5: an order label for the 1st and 2nd sentence, the bridge's identity after

Date: 23 Oct 2026, about 11:00-12:00 UTC. Recomputed at repo commit 4cf5d35 (HEAD then; the saved runs under `results/` are unchanged by it). Packet: [finding5_2026-10-23/](finding5_2026-10-23/) (claim.md, recompute.py, checklist.md). This is an agent check, not a human verification: the finding stays UNVERIFIED until a human adds it to VERIFIED.md.

What was recomputed: every cell of this finding in `results/cross_model/20261023T091847Z/grid.csv` (the grid README cites): 8 models x draws 1-3 and lists of 8 and 12 sentences, each with a 1st-2nd row and a 3rd-on row. From the raw `outcomes.jsonl` of each patch run and the item files its manifest pins (sha256-checked), with an independent script (numpy and the standard library, no repo code, the saved verdicts not read): the decisive layer by the donor-digit rule (or the 27B's fixed 50), k per item, position minus identity for k = 1-2, identity minus position for k >= 3, the entity-cluster bootstrap interval (4,000 draws, seed 0, the same draw order as the repo's, so bounds match to the digit), the verdict by `scripts/finding5_confirm.py` (6538445), and the random-push control (decisive only for Muse draw 1).

Result: 37 of 37 model/setting cells match (74 grid rows: n, value, interval, verdict and layer); 3 cells have no run (Olmo-Hybrid draw 3, Gemma 8 and 12 sentences: no spec). The same 37 match the newer grid `20261023T104743Z`, whose rows for this finding are identical. Verdicts: 36 holds, 1 fails partly (Qwen3-32B draw 1: B's lower bound -5.5 against a -5 bar).

Found while checking (no number changes):

- 7 of the 37 cells ran on specs committed before the rule (27B draws 1-2, 9B, 32B, Gemma draw 1, OLMo-3 draws 1-2) and were judged by it afterwards; the split itself was chosen on the first draws.
- On Gemma a same-size random push at the decisive layer changes 98-99% of answers (other models 0-17%); those answers go off the list and give position minus identity within 2 points, so they do not make the split, but the push is far outside what Gemma tolerates.
- A donor from another topic also moves 23-48% of answers to the same place (27B draw 3, 32B draw 1): part of the 3rd-on "position" share is an order label any list carries.
- Older packet for the 27B and 32B: [finding5_label_identity.md](finding5_label_identity.md) (kept).
