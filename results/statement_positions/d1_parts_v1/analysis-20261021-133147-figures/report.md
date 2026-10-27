# statement_positions / d1_parts_v1: analysis

EXP statement_positions/d1_parts_v1 @ 96c9ec2 (dirty tree) | model Qwen/Qwen3.6-27B | n=32 per family (prompt → prompt; prompt → memory; memory → prompt; memory → memory; prompt → prompt → memory; prompt → memory → prompt; countries: memory → memory; countries: prompt → memory) | seeds=[0]
Claim tested: Where the bridge is in transit, is the patch's effect carried by its lens-readable part?

- prompt → prompt: the whole context (layers [32, 36, 40]): concentration of the lens-readable part 0.14 [0.10, 0.19]; random-dictionary fit (null) 0.07 [0.04, 0.10]; matched piece (control) 0.05 [0.02, 0.07]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 0%, whole patch 90%; bridge carried around it (rule: around)
- prompt → prompt → memory: the whole context (layers [32]): concentration of the lens-readable part 0.08 [-0.06, 0.21]; random-dictionary fit (null) 0.18 [0.12, 0.25]; matched piece (control) 0.06 [-0.01, 0.15]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 0%, whole patch 75%; bridge carried around it (rule: around)
- prompt → memory: sentence stating bridge org (layers [32]): concentration of the lens-readable part 3.36 [3.07, 3.71]; random-dictionary fit (null) 0.24 [0.17, 0.31]; matched piece (control) 0.65 [0.47, 0.85]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 97%, whole patch 100%; bridge carried by the lens-readable part (rule: inside)
- prompt → memory: the bridge org word (layers [32]): concentration of the lens-readable part 3.01 [2.79, 3.26]; random-dictionary fit (null) 0.26 [0.19, 0.34]; matched piece (control) 0.56 [0.42, 0.71]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 97%, whole patch 100%; bridge carried by the lens-readable part (rule: inside)
- prompt → memory: the whole context (layers [32, 36]): concentration of the lens-readable part 5.02 [4.63, 5.46]; random-dictionary fit (null) 0.25 [0.19, 0.32]; matched piece (control) 0.91 [0.72, 1.12]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 61%, whole patch 75%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: sentence stating bridge org (layers [32, 36, 40]): concentration of the lens-readable part 2.47 [2.36, 2.58]; random-dictionary fit (null) 0.13 [0.11, 0.16]; matched piece (control) 0.54 [0.46, 0.64]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 68%, whole patch 85%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: the bridge org word (layers [32, 36, 40]): concentration of the lens-readable part 2.29 [2.21, 2.38]; random-dictionary fit (null) 0.13 [0.11, 0.16]; matched piece (control) 0.53 [0.44, 0.62]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 68%, whole patch 85%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: the whole context (layers [32, 36]): concentration of the lens-readable part 2.66 [2.51, 2.83]; random-dictionary fit (null) 0.16 [0.13, 0.19]; matched piece (control) 0.60 [0.48, 0.72]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 97%, whole patch 97%; bridge carried by the lens-readable part (rule: inside)
- countries: prompt → memory: question and all after it (layers [40]): concentration of the lens-readable part 2.80 [2.56, 3.04]; random-dictionary fit (null) 0.30 [0.25, 0.35]; matched piece (control) 0.45 [0.38, 0.52]; % of original answers that become the alternative answer (answer org → answer alt): lens-readable part alone 25%, whole patch 88%; bridge carried by the lens-readable part (rule: inside)
- Same patch, two questions (the whole context, layers [32, 36]): concentration of prompt → memory minus prompt → prompt = 4.84 [4.46, 5.27] (scene bootstrap); largest share difference between the two patches 0.0
- Same patch, two questions (the whole context, layers [32]): concentration of prompt → memory → prompt minus prompt → prompt → memory = 2.01 [1.62, 2.44] (scene bootstrap); largest share difference between the two patches 0.1324

Split half of the decision rule:
- prompt → prompt: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; split half of the rule: H-around
- prompt → prompt → memory: at the whole context: bridge carried around it (rule: around); positive control (countries: prompt → memory) there: carried by the lens-readable part; split half of the rule: H-around

Figures: results/statement_positions/d1_parts_v1/analysis-20261021-133147-figures/jspace_concentration.png, results/statement_positions/d1_parts_v1/analysis-20261021-133147-figures/paired_readers.png

Gates:
- no gate of its own (reads without greedy validation); the map run's gates apply

Recomputed from the saved outputs == the run's summary.json: {"claims": true, "verdicts": true, "concentrations": true}

Status: UNVERIFIED
