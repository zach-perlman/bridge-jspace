# statement_positions / d1_parts_n80_repro: analysis

EXP statement_positions/d1_parts_n80_repro @ 80880cd (dirty tree) | model Qwen/Qwen3.6-27B | n=80 per family (prompt → prompt; prompt → memory; memory → prompt; memory → memory; prompt → prompt → memory; prompt → memory → prompt; countries: memory → memory; countries: prompt → memory) | seeds=[0]
Claim tested: Where the bridge is in transit, is the patch's effect carried by its lens-readable part?

- prompt → prompt: the whole context (layers [32, 36, 40]): concentration of the lens-readable part 0.10 [0.08, 0.13]; random-dictionary fit (null) 0.07 [0.05, 0.09]; matched piece (control) 0.03 [0.02, 0.05]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 0%, whole patch 87%; bridge carried around it (rule: around)
- prompt → prompt → memory: the whole context (layers [32]): concentration of the lens-readable part 0.10 [0.02, 0.17]; random-dictionary fit (null) 0.13 [0.09, 0.18]; matched piece (control) 0.04 [0.01, 0.08]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 0%, whole patch 78%; bridge carried around it (rule: around)
- prompt → memory: sentence stating bridge org (layers [32, 36]): concentration of the lens-readable part 3.11 [2.92, 3.32]; random-dictionary fit (null) 0.25 [0.21, 0.31]; matched piece (control) 0.55 [0.47, 0.64]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 69%, whole patch 74%; bridge carried by the lens-readable part (rule: inside)
- prompt → memory: the bridge org word (layers [32, 36]): concentration of the lens-readable part 2.82 [2.68, 2.97]; random-dictionary fit (null) 0.26 [0.21, 0.31]; matched piece (control) 0.51 [0.44, 0.58]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 68%, whole patch 74%; bridge carried by the lens-readable part (rule: inside)
- prompt → memory: the whole context (layers [32, 36]): concentration of the lens-readable part 4.87 [4.60, 5.18]; random-dictionary fit (null) 0.25 [0.20, 0.31]; matched piece (control) 0.87 [0.74, 1.00]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 66%, whole patch 78%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: sentence stating bridge org (layers [32, 36]): concentration of the lens-readable part 2.49 [2.41, 2.57]; random-dictionary fit (null) 0.10 [0.08, 0.12]; matched piece (control) 0.56 [0.50, 0.63]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 94%, whole patch 99%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: the bridge org word (layers [32, 36]): concentration of the lens-readable part 2.29 [2.24, 2.35]; random-dictionary fit (null) 0.10 [0.08, 0.12]; matched piece (control) 0.52 [0.46, 0.58]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 94%, whole patch 99%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: the whole context (layers [32, 36]): concentration of the lens-readable part 2.74 [2.61, 2.87]; random-dictionary fit (null) 0.13 [0.11, 0.15]; matched piece (control) 0.59 [0.51, 0.68]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 91%, whole patch 93%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: question and all after it (layers [40]): concentration of the lens-readable part 2.55 [2.38, 2.72]; random-dictionary fit (null) 0.25 [0.22, 0.29]; matched piece (control) 0.40 [0.36, 0.44]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 18%, whole patch 82%; bridge carried by the lens-readable part (rule: inside)
- Same patch, two questions (the whole context, layers [32, 36]): concentration of prompt → memory minus prompt → prompt = 4.73 [4.47, 5.04] (scene bootstrap); largest share difference between the two patches 0.0
- Same patch, two questions (the whole context, layers [32]): concentration of prompt → memory → prompt minus prompt → prompt → memory = 2.16 [1.89, 2.42] (scene bootstrap); largest share difference between the two patches 0.1324

Split half of the decision rule:
- prompt → prompt: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; split half of the rule: H-around
- prompt → prompt → memory: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; split half of the rule: H-around

Figures: results/statement_positions/d1_parts_n80_repro/analysis-20261021-233944-figures/jspace_concentration.png, results/statement_positions/d1_parts_n80_repro/analysis-20261021-233944-figures/paired_readers.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"claims": true, "verdicts": true, "concentrations": true}

Status: UNVERIFIED
