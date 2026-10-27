# The probe's upper bound against the lens, at the bridge's word

Descriptive, after the data (Dan's plan step 5). Fresh scenes, the locker sentence before the pick (x0_probe v4, subset all); probe accuracy with its 95% interval over bridge entities, against the best baseline the probe script reports. Lens columns: the share of the single-change edit's J++ part (k = 25 / 100) and of the rest that lies in the address probe's subspace (x0_probe_patched energy). UNVERIFIED.

| model | target | n | classes | probe | best baseline | probe - baseline | J++ part in the probe's subspace (k = 25 / 100) | the rest in it (k = 25 / 100) |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B (L12) | address (locker sentence) | 758 | 5 | 0.97 [0.96, 0.98] | layout 0.53 [0.50, 0.56] | 0.44 [0.41, 0.47] | 0.5% / 3.2% | 90.6% / 69.5% |
| Qwen3.5-9B (L12) | bridge identity | 758 | 46 | 1.00 [1.00, 1.00] | majority 0.07 [0.00, 0.21] | 0.93 [0.79, 1.00] | not run (no identity-target probe_patched) | - |
| Qwen3.6-27B (L32) | address (locker sentence) | 758 | 5 | 0.99 [0.98, 1.00] | layout 0.53 [0.50, 0.56] | 0.46 [0.43, 0.49] | 0.5% / 2.8% | 90.5% / 73.4% |
| Qwen3.6-27B (L32) | bridge identity | 758 | 46 | 1.00 [1.00, 1.00] | majority 0.07 [0.00, 0.21] | 0.93 [0.79, 1.00] | not run (no identity-target probe_patched) | - |
| Qwen3.5-122B-A10B (L33) | address (locker sentence) | 758 | 5 | 0.92 [0.90, 0.94] | layout 0.53 [0.50, 0.56] | 0.39 [0.35, 0.42] | 0.5% / 2.5% | 93.3% / 76.7% |
| Qwen3.5-122B-A10B (L33) | bridge identity | 758 | 46 | 1.00 [1.00, 1.00] | majority 0.07 [0.00, 0.21] | 0.93 [0.79, 1.00] | not run (no identity-target probe_patched) | - |
| Muse Glimmer 30B (L26) | address (locker sentence) | 657 | 5 | 0.97 [0.95, 0.98] | layout 0.53 [0.49, 0.56] | 0.44 [0.41, 0.47] | 0.3% / 2.3% | 92.9% / 73.9% |
| Muse Glimmer 30B (L26) | bridge identity | 657 | 44 | 1.00 [0.99, 1.00] | majority 0.08 [0.00, 0.23] | 0.92 [0.76, 1.00] | not run (no identity-target probe_patched) | - |
