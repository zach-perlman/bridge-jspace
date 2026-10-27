# statement_positions / d1_rw_v1: analysis

EXP statement_positions/d1_rw_v1 @ 96c9ec2 (dirty tree) | model Qwen/Qwen3.6-27B | n=32 per family (prompt → prompt; prompt → memory; memory → prompt; memory → memory; prompt → prompt → memory; prompt → memory → prompt; countries: memory → memory; countries: prompt → memory) | seeds=[0]
Claim tested: Where the bridge is in transit, does the lens read bridge org there, and does a lens push (bridge alt − bridge org) change the answer?

- prompt → prompt: the whole context (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 90%; lens push 1x 0% [0%, 4%], 4x 0%, 16x 12%; random push (control) 4x 0%, 16x 9%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push unclear (rule: inconclusive)
- prompt → prompt → memory: the whole context (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 78%; lens push 1x 9% [3%, 24%], 4x 6%, 16x 22%; random push (control) 4x 0%, 16x 34%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push unclear (rule: inconclusive)
- memory → prompt: question and all after it (layers [36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 56%; lens push 1x 0% [0%, 6%], 4x 0%, 16x 2%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 81% (bridge alt 0%); the lens push does not change it (rule: not written)
- prompt → memory: sentence stating bridge org (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 100%; lens push 1x 100% [89%, 100%], 4x 62%, 16x 19%; random push (control) 4x 6%, 16x 22%; lens reads bridge org in its top 10 100% (bridge alt 0%); the lens push changes the answer (rule: written)
- prompt → memory: the bridge org word (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 100%; lens push 1x 100% [89%, 100%], 4x 56%, 16x 22%; random push (control) 4x 9%, 16x 19%; lens reads bridge org in its top 10 100% (bridge alt 0%); the lens push changes the answer (rule: written)
- prompt → memory: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 77%; lens push 1x 95% [87%, 98%], 4x 44%, 16x 14%; random push (control) 4x 11%, 16x 20%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)
- prompt → memory → prompt: the whole context (layers [32]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 69%; lens push 1x 19% [9%, 35%], 4x 19%, 16x 22%; random push (control) 4x 12%, 16x 22%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push unclear (rule: inconclusive)
- countries: prompt → memory: sentence stating bridge org (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 85%; lens push 1x 83% [75%, 89%], 4x 75%, 16x 23%; random push (control) 4x 2%, 16x 24%; lens reads bridge org in its top 10 100% (bridge alt 16%); the lens push changes the answer (rule: written)
- countries: prompt → memory: the bridge org word (layers [32, 36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 85%; lens push 1x 83% [75%, 89%], 4x 72%, 16x 21%; random push (control) 4x 5%, 16x 21%; lens reads bridge org in its top 10 100% (bridge alt 0%); the lens push changes the answer (rule: written)
- countries: prompt → memory: the whole context (layers [32, 36]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 97%; lens push 1x 100% [94%, 100%], 4x 80%, 16x 5%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 100% (bridge alt 100%); the lens push changes the answer (rule: written)
- countries: prompt → memory: question and all after it (layers [40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 88%; lens push 1x 100% [89%, 100%], 4x 94%, 16x 75%; random push (control) 4x 0%, 16x 0%; lens reads bridge org in its top 10 100% (bridge alt 34%); the lens push changes the answer (rule: written)
- countries: memory → memory: question and all after it (layers [36, 40]), % of original answers that become the alternative answer (answer org → answer alt): patch from the alt prompt 73%; lens push 1x 97% [89%, 99%], 4x 98%, 16x 45%; random push (control) 4x 2%, 16x 3%; lens reads bridge org in its top 10 100% (bridge alt 19%); the lens push changes the answer (rule: written)

Combined decision rule (with the split run):
- prompt → prompt: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: unclear (rule: inconclusive); combined verdict: neither (mixed)
- prompt → prompt → memory: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; lens push at the whole context: unclear (rule: inconclusive); combined verdict: neither (mixed)

Figures: results/statement_positions/d1_rw_v1/analysis-20261021-133148-figures/lens_write.png, results/statement_positions/d1_rw_v1/analysis-20261021-133148-figures/headline_d1.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"verdicts": true, "claims": true}

Status: UNVERIFIED
