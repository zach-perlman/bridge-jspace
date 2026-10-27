# statement_positions / qwen35_122b_d1_topics2_rw: analysis

EXP statement_positions/qwen35_122b_d1_topics2_rw @ 4a87d79 (dirty tree) | model Qwen/Qwen3.5-122B-A10B-FP8 | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: sentence stating bridge org (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 84%; lens push 1x 56% [52%, 60%], 4x 54%, 16x 39%; random push (control) 4x 9%, 16x 27%; lens reads bridge org in its top 10 100% (bridge alt 14%); the lens push changes the answer (rule: written)
- PP: the bridge org word (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 79%; lens push 1x 51% [47%, 56%], 4x 52%, 16x 36%; random push (control) 4x 9%, 16x 21%; lens reads bridge org in its top 10 100% (bridge alt 12%); the lens push changes the answer (rule: written)
- PP: the whole context (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 99%; lens push 1x 32% [28%, 36%], 4x 39%, 16x 21%; random push (control) 4x 17%, 16x 27%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)
- PM: sentence stating bridge org (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 95%; lens push 1x 78% [75%, 82%], 4x 81%, 16x 51%; random push (control) 4x 5%, 16x 23%; lens reads bridge org in its top 10 100% (bridge alt 14%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 94%; lens push 1x 77% [73%, 80%], 4x 77%, 16x 44%; random push (control) 4x 4%, 16x 15%; lens reads bridge org in its top 10 100% (bridge alt 12%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [24, 27, 30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 97%; lens push 1x 81% [78%, 84%], 4x 80%, 16x 61%; random push (control) 4x 7%, 16x 21%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at sentence stating bridge org: bridge unclear (rule: inconclusive); positive control (countries: prompt → memory) there: carried by the lens-readable part; at the bridge org word: bridge unclear (rule: inconclusive); positive control (countries: prompt → memory) there: carried by the lens-readable part; at the whole context: bridge carried by the lens-readable part (rule: inside); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at sentence stating bridge org: changes the answer (rule: written); lens push at the bridge org word: changes the answer (rule: written); lens push at the whole context: changes the answer (rule: written); combined verdict: H-loc supported

Figures: results/statement_positions/qwen35_122b_d1_topics2_rw/analysis-20261023-024117-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
