# Answer control, recall: switches blocked beyond a size-matched random part (post hoc; answer in any language; 9B, 27B, Muse)

| model | arm | value [95% interval] |
|---|---|---|
| qwen3.5-9b | arm1 without the lens part | +0.497 [0.411, 0.571] |
| qwen3.5-9b | arm2 english | +0.472 [0.388, 0.548] |
| qwen3.5-9b | arm2 any language | +0.274 [0.199, 0.355] |
| qwen3.5-9b | arm2 K random english count | +0.469 [0.384, 0.547] |
| qwen3.5-9b | arm2 K random any language count | +0.295 [0.215, 0.386] |
| qwen3.5-9b | arm3 english | +0.000 [0.000, 0.000] |
| qwen3.5-9b | arm3 any language | +0.005 [0.000, 0.018] |
| qwen3.6-27b | arm1 without the lens part | +0.733 [0.651, 0.801] |
| qwen3.6-27b | arm2 english | +0.687 [0.589, 0.767] |
| qwen3.6-27b | arm2 any language | +0.467 [0.356, 0.557] |
| qwen3.6-27b | arm2 K random english count | +0.703 [0.608, 0.777] |
| qwen3.6-27b | arm2 K random any language count | +0.497 [0.389, 0.581] |
| qwen3.6-27b | arm3 english | +0.027 [0.006, 0.054] |
| qwen3.6-27b | arm3 any language | +0.040 [0.006, 0.082] |
| muse-glimmer-30b | arm1 without the lens part | +0.771 [0.628, 0.886] |
| muse-glimmer-30b | arm2 english | +0.712 [0.556, 0.840] |
| muse-glimmer-30b | arm2 any language | +0.500 [0.374, 0.612] |
| muse-glimmer-30b | arm2 K random english count | +0.707 [0.557, 0.834] |
| muse-glimmer-30b | arm2 K random any language count | +0.503 [0.365, 0.615] |
| muse-glimmer-30b | arm3 english | -0.017 [-0.055, 0.014] |
| muse-glimmer-30b | arm3 any language | +0.085 [0.018, 0.154] |
