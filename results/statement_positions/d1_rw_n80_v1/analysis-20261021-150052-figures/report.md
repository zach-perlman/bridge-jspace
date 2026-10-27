# statement_positions / d1_rw_n80_v1: analysis

EXP statement_positions/d1_rw_n80_v1 @ 0b960f6 (dirty tree) | model Qwen/Qwen3.6-27B | n=80 per family (prompt → prompt; prompt → memory; memory → prompt; memory → memory; prompt → prompt → memory; prompt → memory → prompt; countries: memory → memory; countries: prompt → memory) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- prompt → prompt: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 87%; lens push 1x 0% [-0%, 2%], 4x 0%, 16x 10%; random push (control) 4x 0%, 16x 12%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push does not change it (rule: not written)
- prompt → prompt → memory: the whole context (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 78%; lens push 1x 6% [3%, 14%], 4x 12%, 16x 31%; random push (control) 4x 1%, 16x 38%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push unclear (rule: inconclusive)
- memory → prompt: question and all after it (layers [36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 62%; lens push 1x 0% [-0%, 2%], 4x 1%, 16x 1%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 82% (bridge alt 1%); the lens push does not change it (rule: not written)
- prompt → memory: sentence stating bridge org (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 74%; lens push 1x 88% [81%, 92%], 4x 31%, 16x 7%; random push (control) 4x 6%, 16x 9%; lens reads bridge org in its top 10 100% (bridge alt 4%); the lens push changes the answer (rule: written)
- prompt → memory: the bridge org word (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 74%; lens push 1x 87% [81%, 91%], 4x 31%, 16x 11%; random push (control) 4x 5%, 16x 10%; lens reads bridge org in its top 10 100% (bridge alt 0%); the lens push changes the answer (rule: written)
- prompt → memory: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 77%; lens push 1x 96% [91%, 98%], 4x 46%, 16x 12%; random push (control) 4x 10%, 16x 20%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)
- prompt → memory → prompt: the whole context (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 65%; lens push 1x 26% [18%, 37%], 4x 26%, 16x 21%; random push (control) 4x 15%, 16x 28%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push unclear (rule: inconclusive)
- countries: prompt → memory: sentence stating bridge org (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 100%; lens push 1x 100% [98%, 100%], 4x 92%, 16x 30%; random push (control) 4x 6%, 16x 36%; lens reads bridge org in its top 10 100% (bridge alt 20%); the lens push changes the answer (rule: written)
- countries: prompt → memory: the bridge org word (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 100%; lens push 1x 100% [98%, 100%], 4x 90%, 16x 22%; random push (control) 4x 4%, 16x 32%; lens reads bridge org in its top 10 100% (bridge alt 0%); the lens push changes the answer (rule: written)
- countries: prompt → memory: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 93%; lens push 1x 100% [98%, 100%], 4x 78%, 16x 4%; random push (control) 4x 0%, 16x 1%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)
- countries: prompt → memory: question and all after it (layers [40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 82%; lens push 1x 100% [95%, 100%], 4x 95%, 16x 65%; random push (control) 4x 0%, 16x 2%; lens reads bridge org in its top 10 98% (bridge alt 34%); the lens push changes the answer (rule: written)
- countries: memory → memory: question and all after it (layers [36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 77%; lens push 1x 92% [87%, 95%], 4x 97%, 16x 45%; random push (control) 4x 1%, 16x 3%; lens reads bridge org in its top 10 100% (bridge alt 26%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: does not change it (rule: not written); combined verdict: H-around supported
- prompt → prompt → memory: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: unclear (rule: inconclusive); combined verdict: neither (mixed)

Figures: results/statement_positions/d1_rw_n80_v1/analysis-20261021-150052-figures/lens_write.png, results/statement_positions/d1_rw_n80_v1/analysis-20261021-150052-figures/headline_d1.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
