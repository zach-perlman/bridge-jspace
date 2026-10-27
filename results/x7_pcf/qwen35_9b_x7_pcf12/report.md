# P_cf, a pointer without slot labels: qwen35_9b_x7_pcf12

Model qwen3.5-9b, layer 12; 1000 pairs (the bridge's locker sentence trades places with another item's, digits kept); PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 40.4%, 2: 17.0%, 3: 9.3%, 4: 5.0%, 5: 1.6%, 6: 1.3%, 7: 1.2%, 8: 0.9%.
- Split-half noise ceiling (two random halves by pair, seed 0): mean cos² 0.987 (500 / 500 rows).
- Principal angles with the mass-mean pointer directions (rank 4): cos² 0.000, 0.000; mean 0.000 (a random subspace: 0.0005).
- P_cf's share inside each pair's 25-atom J++ span: mean 0.018, median 0.018 (descriptive).
