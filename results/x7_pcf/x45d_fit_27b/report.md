# 45d's fit: a label-free basis per format in the varied scenes (x45d_fit_27b)

Model qwen3.6-27b, layer 32; set x0b_v2, half 1 of the bridge items (seed 0); pairs: the bridge's locker statement trades places with another item's, both before the asked pick, numbers kept; PCA centered, rank 4. Descriptive; the test is x0b_generalize --pcf-from. UNVERIFIED.

| format | pairs | scenes | bridge items | variance explained 1-4 (cum.) | split-half mean cos² | mean cos² with U (random 0.0008) |
|---|---|---|---|---|---|---|
| prose | 878 | 367 | 29 | 0.492 | 0.878 | 0.462 |
| json | 326 | 121 | 14 | 0.521 | 0.599 | 0.190 |
| table | 1227 | 455 | 30 | 0.516 | 0.834 | 0.242 |

Mean cos² between the formats' bases: prose/json 0.197, prose/table 0.229, json/table 0.654.
