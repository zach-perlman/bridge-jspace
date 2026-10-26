# P_cf, a pointer without slot labels: qwen35_122b_x7_pcf

Model qwen3.5-122b-a10b, layer 33; 1000 pairs (the bridge's locker sentence trades places with another item's, digits kept); PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 44.4%, 2: 15.6%, 3: 9.3%, 4: 3.3%, 5: 2.1%, 6: 1.6%, 7: 1.4%, 8: 1.2%.
- Split-half noise ceiling (two random halves by pair, seed 0): mean cos² 0.970 (500 / 500 rows).
- Principal angles with the mass-mean pointer directions (rank 4): cos² 0.856, 0.680, 0.031, 0.020; mean 0.397 (a random subspace: 0.0013).
- P_cf's share inside each pair's 25-atom J++ span: mean 0.016, median 0.016 (descriptive).
