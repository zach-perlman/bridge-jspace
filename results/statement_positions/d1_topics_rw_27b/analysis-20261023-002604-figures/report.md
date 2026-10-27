# statement_positions / d1_topics_rw_27b: analysis

EXP statement_positions/d1_topics_rw_27b @ 3e90959 (dirty tree) | model Qwen/Qwen3.6-27B | n=120 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 68%; lens push 1x 0% [0%, 1%], 4x 6%, 16x 21%; random push (control) 4x 6%, 16x 18%; lens reads bridge org in its top 10 99% (bridge alt 100%); the lens push does not change it (rule: not written)
- PM: sentence stating bridge org (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 69%; lens push 1x 50% [41%, 59%], 4x 38%, 16x 16%; random push (control) 4x 11%, 16x 11%; lens reads bridge org in its top 10 85% (bridge alt 5%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 69%; lens push 1x 49% [40%, 58%], 4x 36%, 16x 15%; random push (control) 4x 9%, 16x 10%; lens reads bridge org in its top 10 85% (bridge alt 5%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 67%; lens push 1x 57% [51%, 63%], 4x 44%, 16x 16%; random push (control) 4x 10%, 16x 14%; lens reads bridge org in its top 10 99% (bridge alt 99%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported

Figures: results/statement_positions/d1_topics_rw_27b/analysis-20261023-002604-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
