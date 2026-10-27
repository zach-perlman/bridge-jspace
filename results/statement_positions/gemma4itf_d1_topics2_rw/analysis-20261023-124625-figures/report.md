# statement_positions / gemma4itf_d1_topics2_rw: analysis

EXP statement_positions/gemma4itf_d1_topics2_rw @ 347b40c (dirty tree) | model google/gemma-4-31B-it | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 84%; lens push 1x 23% [17%, 30%], 4x 23%, 16x 23%; random push (control) 4x 22%, 16x 22%; lens reads bridge org in its top 10 91% (bridge alt 93%); the lens push unclear (rule: inconclusive)
- PP: question and all after it (layers [36, 39, 42, 45, 48, 51, 54]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 87%; lens push 1x 0% [0%, 1%], 4x 0%, 16x 1%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 97% (bridge alt 46%); the lens push does not change it (rule: not written)
- PM: the whole context (layers [30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 68%; lens push 1x 15% [10%, 21%], 4x 14%, 16x 15%; random push (control) 4x 17%, 16x 17%; lens reads bridge org in its top 10 91% (bridge alt 93%); the lens push unclear (rule: inconclusive)
- PM: question and all after it (layers [45, 48, 51, 54]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 53%; lens push 1x 0% [0%, 1%], 4x 0%, 16x 0%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 100% (bridge alt 59%); the lens push does not change it (rule: not written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge unclear (rule: inconclusive); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: unclear (rule: inconclusive); combined verdict: neither (mixed)

Figures: results/statement_positions/gemma4itf_d1_topics2_rw/analysis-20261023-124625-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
