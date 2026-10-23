# statement_positions / gemma4itf_d1_formats_rw: analysis

EXP statement_positions/gemma4itf_d1_formats_rw @ 347b40c (dirty tree) | model google/gemma-4-31B-it | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 74%; lens push 1x 5% [3%, 10%], 4x 7%, 16x 7%; random push (control) 4x 8%, 16x 9%; lens reads bridge org in its top 10 88% (bridge alt 88%); the lens push does not change it (rule: not written)
- PP: question and all after it (layers [42, 45, 48, 51, 54]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 88%; lens push 1x 0% [0%, 0%], 4x 0%, 16x 0%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 95% (bridge alt 7%); the lens push does not change it (rule: not written)
- PM: the whole context (layers [30]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 56%; lens push 1x 7% [4%, 11%], 4x 4%, 16x 4%; random push (control) 4x 4%, 16x 6%; lens reads bridge org in its top 10 88% (bridge alt 88%); the lens push unclear (rule: inconclusive)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried by the lens-readable part (rule: inside); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: neither (mixed)

Figures: results/statement_positions/gemma4itf_d1_formats_rw/analysis-20261023-153948-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
