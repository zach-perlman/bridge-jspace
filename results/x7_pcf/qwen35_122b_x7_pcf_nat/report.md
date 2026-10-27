# P_cf_nat, the pointer from natural passages: qwen35_122b_x7_pcf_nat

Model qwen3.5-122b-a10b, layer 33; 59 of 154 passages allow a move ({'passages': 154, 'passages that allow a move': 59, 'the binding sentence is the first mention': 73, 'no other place before the binding sentence': 22, 'pairs': 167}); 167 pairs; PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 28.3%, 2: 11.0%, 3: 5.8%, 4: 3.8%, 5: 2.9%, 6: 2.6%, 7: 2.2%, 8: 1.9%.
- Split-half noise ceiling (two random halves by passage, seed 0): mean cos² 0.554 (81 / 86 rows).
- cos² of the principal angles with P_cf (qwen35_122b_x7_pcf): 0.573, 0.265, 0.073, 0.002; mean 0.228. With the mass-mean pointer directions: mean 0.334 (a random subspace: 0.0013).
- P_cf_nat's share inside each pair's 25-atom J++ span: mean 0.008 (descriptive).
