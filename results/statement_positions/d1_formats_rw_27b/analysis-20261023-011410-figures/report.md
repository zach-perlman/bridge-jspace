# statement_positions / d1_formats_rw_27b: analysis

EXP statement_positions/d1_formats_rw_27b @ dbc4527 (dirty tree) | model Qwen/Qwen3.6-27B | n=180 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 76%; lens push 1x 0% [0%, 1%], 4x 4%, 16x 10%; random push (control) 4x 4%, 16x 12%; lens reads bridge org in its top 10 99% (bridge alt 100%); the lens push does not change it (rule: not written)
- PM: sentence stating bridge org (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 76%; lens push 1x 45% [40%, 50%], 4x 36%, 16x 14%; random push (control) 4x 5%, 16x 14%; lens reads bridge org in its top 10 98% (bridge alt 16%); the lens push changes the answer (rule: written)
- PM: the bridge org word (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 75%; lens push 1x 44% [39%, 49%], 4x 38%, 16x 12%; random push (control) 4x 4%, 16x 9%; lens reads bridge org in its top 10 98% (bridge alt 14%); the lens push changes the answer (rule: written)
- PM: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 68%; lens push 1x 34% [30%, 38%], 4x 44%, 16x 11%; random push (control) 4x 4%, 16x 8%; lens reads bridge org in its top 10 99% (bridge alt 100%); the lens push unclear (rule: inconclusive)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported

Figures: results/statement_positions/d1_formats_rw_27b/analysis-20261023-011410-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
