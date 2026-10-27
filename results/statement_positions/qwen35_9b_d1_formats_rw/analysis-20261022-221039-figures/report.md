# statement_positions / qwen35_9b_d1_formats_rw: analysis

EXP statement_positions/qwen35_9b_d1_formats_rw @ dbc4527 (dirty tree) | model Qwen/Qwen3.5-9B | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 59%; lens push 1x 1% [0%, 2%], 4x 3%, 16x 6%; random push (control) 4x 3%, 16x 7%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push does not change it (rule: not written)
- PM: sentence stating bridge org (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 72%; lens push 1x 64% [59%, 68%], 4x 42%, 16x 25%; random push (control) 4x 22%, 16x 24%; lens reads bridge org in its top 10 100% (bridge alt 21%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 73%; lens push 1x 63% [58%, 68%], 4x 38%, 16x 25%; random push (control) 4x 21%, 16x 24%; lens reads bridge org in its top 10 100% (bridge alt 18%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [16, 18]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 65%; lens push 1x 62% [57%, 67%], 4x 39%, 16x 19%; random push (control) 4x 16%, 16x 19%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported

Figures: results/statement_positions/qwen35_9b_d1_formats_rw/analysis-20261022-221039-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
