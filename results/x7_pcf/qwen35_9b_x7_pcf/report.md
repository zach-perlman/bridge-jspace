# P_cf, a pointer without slot labels: qwen35_9b_x7_pcf

Model qwen3.5-9b, layer 12; 1000 pairs (the bridge's locker sentence trades places with another item's, digits kept); PCA centered over the bridge word's S - O. UNVERIFIED.

- Variance explained by components 1-8: 1: 44.6%, 2: 17.5%, 3: 9.3%, 4: 3.7%, 5: 1.8%, 6: 1.4%, 7: 1.1%, 8: 1.1%.
- Split-half noise ceiling (two random halves by pair, seed 0): mean cos² 0.981 (500 / 500 rows).
- Principal angles with the mass-mean pointer directions (rank 4): cos² 0.811, 0.571, 0.079, 0.018; mean 0.370 (a random subspace: 0.0010).
- P_cf's share inside each pair's 25-atom J++ span: mean 0.018, median 0.018 (descriptive).
