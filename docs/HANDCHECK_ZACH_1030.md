# Hand-check, Zach (breadth), 30 Oct 2026

Zach read 25 random Qwen3.6-27B items by hand, over four of the breadth claims, and marked for each whether the automatic grader's right/wrong calls match the answers shown and the item is a fair test (Dan's style of check: gold right, item tests what it claims, scored outcome matches the answers). Item text is synthetic and private; only ids are listed here.

**Result: 25 of 25 agree with the grader; 0 disagree, 0 unsure, 0 items flagged as unfair.**

| Claim | Items | Agree |
|---|---|---|
| Claim 1, twin set (note 20): the knock-out breaks recall (MM), not lookup (MP); rotated control beside | 10 | 10 / 10 |
| What recall loses (note 57): keep only / remove only the answer directions, random part of equal energy | 5 | 5 / 5 |
| Blind test (note 62): the city's J++ directions removed, and made orthogonal to the answers, on '{city} is in the country of' | 5 | 5 / 5 |
| Agents (notes 65 verify, 59 produce): checking a stated claim vs producing the answer alone | 5 | 5 / 5 |

## Sampling (seed 1030, from each run's gated items)

- **C1:** `rng = random.Random(1030); MM = rng.sample(sorted MM ids of the KO run, 5); then MP = rng.sample(sorted MP ids, 5)  (population: 338 MM / 473 MP gated items of results/ablate_v2/jsuite_v4_test_chat_ko_cand2_v1/rows.jsonl; from redteam_1030/handcheck_zach_items_for_dan.md, unchanged)`
- **M:** `rng = random.Random(1030); rng.sample(sorted({r['id'] for r in rows if r['family']=='MM'}), 5) over results/ablate_v2/jsuite_v4_test_chat_ko57_cand2_v1/rows.jsonl (338 MM). Same population and seed as C1's MM draw, so it returns the same 5 items.`
- **B:** `rng = random.Random(1030); rng.sample(sorted(gated onehop uids), 5); gated = gate.jsonl gated_canonical of results/sd_necessity/sd_gate_v1 (as scripts/nn_sd62_read.py), over the onehop rows of results/sd_necessity/sd62_ko_test_v1/rows.jsonl (415 read, 325 gated)`
- **G:** `rng = random.Random(1030); ver_true = rng.sample(sorted(gated ver_true uids of sd65_ko_test_v1), 2); ver_false = rng.sample(sorted(gated ver_false uids), 1) (same rng); rng = random.Random(1030); solo = rng.sample(sorted(gated solo uids of sd59_ko_test_v1), 2). gated as in B (325 of 415 each).`

## Items (id and the grader's per-condition calls)

- C1-1 `j3:chat:v4:MM-w0-00236`: {"cand2_right": {"none": true, "paper10": false, "paper10_rot": false}, "lost": {"paper10": true, "paper10_rot": true}}
- C1-2 `j3:chat:v4:MM-w1-00223`: {"cand2_right": {"none": true, "paper10": false, "paper10_rot": false}, "lost": {"paper10": true, "paper10_rot": true}}
- C1-3 `j3:chat:v4:MM-w1-00509`: {"cand2_right": {"none": true, "paper10": false, "paper10_rot": true}, "lost": {"paper10": true, "paper10_rot": false}}
- C1-4 `j3:chat:v4:MM-w0-00382`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- C1-5 `j3:chat:v4:MM-w1-00657`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- C1-6 `j3:chat:v4:MP-w1-00731`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- C1-7 `j3:chat:v4:MP-w0-00362`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- C1-8 `j3:chat:v4:MP-w0-00860`: {"cand2_right": {"none": true, "paper10": false, "paper10_rot": true}, "lost": {"paper10": true, "paper10_rot": false}}
- C1-9 `j3:chat:v4:MP-w1-00783`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- C1-10 `j3:chat:v4:MP-w1-00109`: {"cand2_right": {"none": true, "paper10": true, "paper10_rot": true}, "lost": {"paper10": false, "paper10_rot": false}}
- M-1 `j3:chat:v4:MM-w0-00236`: {"cand2_right": {"none": true, "paper10": false, "paper10_onlyA": false, "paper10_onlyRperp": true, "top30": false, "top30_keepA": true, "top100": false, "top100_keepA": true}}
- M-2 `j3:chat:v4:MM-w1-00223`: {"cand2_right": {"none": true, "paper10": false, "paper10_onlyA": false, "paper10_onlyRperp": false, "top30": false, "top30_keepA": false, "top100": false, "top100_keepA": false}}
- M-3 `j3:chat:v4:MM-w1-00509`: {"cand2_right": {"none": true, "paper10": false, "paper10_onlyA": false, "paper10_onlyRperp": true, "top30": false, "top30_keepA": false, "top100": false, "top100_keepA": false}}
- M-4 `j3:chat:v4:MM-w0-00382`: {"cand2_right": {"none": true, "paper10": true, "paper10_onlyA": false, "paper10_onlyRperp": true, "top30": false, "top30_keepA": true, "top100": false, "top100_keepA": true}}
- M-5 `j3:chat:v4:MM-w1-00657`: {"cand2_right": {"none": true, "paper10": true, "paper10_onlyA": false, "paper10_onlyRperp": true, "top30": false, "top30_keepA": true, "top100": false, "top100_keepA": true}}
- B-1 `thf:91113`: {"first_token_right": {"none": true, "bridgeJ": true, "bridgeJperp": true, "bridgeJ_rot": true, "bridgeJ_ctrl": true}}
- B-2 `thf:92479`: {"first_token_right": {"none": true, "bridgeJ": true, "bridgeJperp": true, "bridgeJ_rot": true, "bridgeJ_ctrl": true}}
- B-3 `thf:93399`: {"first_token_right": {"none": true, "bridgeJ": true, "bridgeJperp": true, "bridgeJ_rot": true, "bridgeJ_ctrl": true}}
- B-4 `thf:91343`: {"first_token_right": {"none": true, "bridgeJ": true, "bridgeJperp": true, "bridgeJ_rot": true, "bridgeJ_ctrl": true}}
- B-5 `thf:91410`: {"first_token_right": {"none": true, "bridgeJ": true, "bridgeJperp": true, "bridgeJ_rot": true, "bridgeJ_ctrl": true}}
- G-1 `thf:91113`: {"right": {"none": true, "paper10": true, "paper10_rot": true}}
- G-2 `thf:92479`: {"right": {"none": true, "paper10": false, "paper10_rot": true}}
- G-3 `thf:93399`: {"right": {"none": true, "paper10": true, "paper10_rot": true}}
- G-4 `thf:91113`: {"right": {"none": true, "paper10": false, "paper10_rot": true}}
- G-5 `thf:92479`: {"right": {"none": true, "paper10": false, "paper10_rot": true}}

## What a reader should know
- The sample is small: 25 items, one model (27B). Agreement checks the grader and item fairness, not the size of any effect.
- C1 shows the earlier packet's flags on three items (C1-2: the name may hint at the answer; C1-3: the closed-book hop-1 reply named the pipeline operator, not Gazprom; C1-4: under the knock-out the top token overall is not an answer option). Zach agreed with the grader on all three.
- M: the run stores 'keep only the answer directions' with the top-30 and top-100 knock-outs, not with paper10; those rows were shown. In this sample the keep rescues 3 of 5 recall items (M-1, M-4, M-5), as expected from the population's rescue (0.68 / 0.78 vs a random keep).
- B: none of the 5 sampled one-hop items broke under the city's J++ removal (population: about 29% break), so B checks the grader, not the effect.
- Built from stored rows on CPU (tokenizer only; no model loaded). Extraction scripts: Zach's scratch (handcheck/work/), not in the repo, because they embed the private items.
