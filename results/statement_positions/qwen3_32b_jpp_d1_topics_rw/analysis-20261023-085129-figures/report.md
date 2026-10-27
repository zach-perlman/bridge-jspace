# statement_positions / qwen3_32b_jpp_d1_topics_rw: analysis

EXP statement_positions/qwen3_32b_jpp_d1_topics_rw @ 193c060 (dirty tree) | model Qwen/Qwen3-32B | n=120 per family (PP; PM) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- PP: sentence stating bridge org (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 71%; lens push 1x 2% [1%, 5%], 4x 28%, 16x 32%; random push (control) 4x 20%, 16x 35%; lens reads bridge org in its top 10 80% (bridge alt 4%); the lens push unclear (rule: inconclusive)
- PP: the bridge org word (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 89%; lens push 1x 2% [1%, 7%], 4x 23%, 16x 22%; random push (control) 4x 18%, 16x 20%; lens reads bridge org in its top 10 72% (bridge alt 3%); the lens push unclear (rule: inconclusive)
- PP: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 100%; lens push 1x 1% [0%, 2%], 4x 29%, 16x 21%; random push (control) 4x 28%, 16x 21%; lens reads bridge org in its top 10 99% (bridge alt 98%); the lens push unclear (rule: inconclusive)
- PM: sentence stating bridge org (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 83%; lens push 1x 20% [16%, 25%], 4x 41%, 16x 29%; random push (control) 4x 15%, 16x 30%; lens reads bridge org in its top 10 80% (bridge alt 5%); the lens push unclear (rule: inconclusive)
- PM: the bridge org word (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 81%; lens push 1x 20% [16%, 25%], 4x 31%, 16x 15%; random push (control) 4x 10%, 16x 15%; lens reads bridge org in its top 10 80% (bridge alt 5%); the lens push unclear (rule: inconclusive)
- PM: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 98%; lens push 1x 28% [23%, 33%], 4x 47%, 16x 31%; random push (control) 4x 14%, 16x 20%; lens reads bridge org in its top 10 99% (bridge alt 98%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: no statement set in transit at the primary layers: H-loc's location premise fails there
- prompt → prompt → memory: no statement set in transit at the primary layers: H-loc's location premise fails there
- PP: at sentence stating bridge org: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: unclear; at the bridge org word: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: unclear; at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: unclear; lens push at sentence stating bridge org: unclear (rule: inconclusive); lens push at the bridge org word: unclear (rule: inconclusive); lens push at the whole context: unclear (rule: inconclusive); combined verdict: neither (mixed)

Figures: results/statement_positions/qwen3_32b_jpp_d1_topics_rw/analysis-20261023-085129-figures/lens_write.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
