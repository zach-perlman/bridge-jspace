# P_cf_nat, the pointer from natural passages: qwen35_9b_x7_pcf_nat

Model qwen3.5-9b, layer 12; 59 of 154 passages allow a move ({'passages': 154, 'passages that allow a move': 59, 'the binding sentence is the first mention': 73, 'no other place before the binding sentence': 22, 'pairs': 167}); 167 pairs; PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 23.9%, 2: 10.0%, 3: 5.7%, 4: 4.0%, 5: 3.2%, 6: 2.5%, 7: 2.2%, 8: 1.9%.
- Split-half noise ceiling (two random halves by passage, seed 0): mean cos² 0.534 (81 / 86 rows).
- cos² of the principal angles with P_cf (qwen35_9b_x7_pcf): 0.489, 0.206, 0.049, 0.037; mean 0.195. With the mass-mean pointer directions: mean 0.317 (a random subspace: 0.0010).
- P_cf_nat's share inside each pair's 25-atom J++ span: mean 0.008 (descriptive).
