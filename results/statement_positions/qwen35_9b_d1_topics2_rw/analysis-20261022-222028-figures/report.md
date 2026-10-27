# statement_positions / qwen35_9b_d1_topics2_rw: analysis

EXP statement_positions/qwen35_9b_d1_topics2_rw @ a786b36 (dirty tree) | model Qwen/Qwen3.5-9B | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 55%; lens push 1x 0% [0%, 1%], 4x 5%, 16x 16%; random push (control) 4x 4%, 16x 15%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push does not change it (rule: not written)
- PM: sentence stating bridge org (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 61%; lens push 1x 50% [45%, 55%], 4x 30%, 16x 18%; random push (control) 4x 14%, 16x 17%; lens reads bridge org in its top 10 100% (bridge alt 10%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 60%; lens push 1x 49% [44%, 55%], 4x 26%, 16x 16%; random push (control) 4x 14%, 16x 15%; lens reads bridge org in its top 10 100% (bridge alt 9%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 63%; lens push 1x 59% [53%, 64%], 4x 42%, 16x 21%; random push (control) 4x 12%, 16x 18%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported

Figures: results/statement_positions/qwen35_9b_d1_topics2_rw/analysis-20261022-222028-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
