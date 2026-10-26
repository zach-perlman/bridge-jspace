# P_cf_nat, the pointer from natural passages: x7_pcf_27b_nat

Model qwen3.6-27b, layer 32; 59 of 154 passages allow a move ({'passages': 154, 'passages that allow a move': 59, 'the binding sentence is the first mention': 73, 'no other place before the binding sentence': 22, 'pairs': 167}); 167 pairs; PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 23.7%, 2: 8.6%, 3: 4.8%, 4: 4.1%, 5: 3.3%, 6: 2.5%, 7: 2.1%, 8: 2.0%.
- Split-half noise ceiling (two random halves by passage, seed 0): mean cos² 0.499 (81 / 86 rows).
- cos² of the principal angles with P_cf (x7_pcf_27b): 0.495, 0.185, 0.043, 0.029; mean 0.188. With the mass-mean pointer directions: mean 0.296 (a random subspace: 0.0008).
- P_cf_nat's share inside each pair's 25-atom J++ span: mean 0.007 (descriptive).
