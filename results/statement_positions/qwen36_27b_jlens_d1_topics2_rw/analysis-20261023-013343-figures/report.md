# statement_positions / qwen36_27b_jlens_d1_topics2_rw: analysis

EXP statement_positions/qwen36_27b_jlens_d1_topics2_rw @ 2dadb64 (dirty tree) | model Qwen/Qwen3.6-27B | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 64%; lens push 1x 0% [0%, 1%], 4x 5%, 16x 15%; random push (control) 4x 7%, 16x 15%; lens reads bridge org in its top 10 96% (bridge alt 97%); the lens push does not change it (rule: not written)
- PM: sentence stating bridge org (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 78%; lens push 1x 35% [28%, 42%], 4x 28%, 16x 16%; random push (control) 4x 9%, 16x 14%; lens reads bridge org in its top 10 63% (bridge alt 3%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 74%; lens push 1x 36% [29%, 43%], 4x 27%, 16x 14%; random push (control) 4x 7%, 16x 13%; lens reads bridge org in its top 10 63% (bridge alt 2%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 66%; lens push 1x 41% [36%, 46%], 4x 41%, 16x 18%; random push (control) 4x 8%, 16x 17%; lens reads bridge org in its top 10 94% (bridge alt 95%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported

Figures: results/statement_positions/qwen36_27b_jlens_d1_topics2_rw/analysis-20261023-013343-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
