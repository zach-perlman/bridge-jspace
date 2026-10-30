# Claim 10: the lookup's switch rate under the whole change by both orders (post hoc)

Rule: {'models_where_the_changed_order_matters_more': 0, 'of': 5, 'outcome': 'keep claim 10; the 2x2 is a caveat table'}

## qwen3.5-9b (L12; 200 of 200 lookups in the 2x2)

| | changed before | changed after |
|---|---|---|
| original before | 75: 0.960 [0.915, 1.000] | 25: 0.560 [0.333, 0.762] |
| original after | 32: 0.469 [0.333, 0.593] | 68: 0.059 [0.013, 0.128] |

changed order's effect 0.405 [0.267, 0.544]; original order's effect 0.496 [0.374, 0.618]; examples []

## qwen3.6-27b (L32; 200 of 200 lookups in the 2x2)

| | changed before | changed after |
|---|---|---|
| original before | 69: 0.957 [0.911, 1.000] | 32: 0.344 [0.182, 0.517] |
| original after | 38: 0.210 [0.087, 0.349] | 61: 0.016 [0.000, 0.061] |

changed order's effect 0.404 [0.285, 0.515]; original order's effect 0.537 [0.435, 0.645]; examples [{'scene': 'P2-L0-0152', 'original': 'before', 'changed': 'after', 'switched': 0}]

## muse-glimmer-30b (L26; 200 of 200 lookups in the 2x2)

| | changed before | changed after |
|---|---|---|
| original before | 68: 0.809 [0.719, 0.897] | 24: 0.208 [0.062, 0.400] |
| original after | 39: 0.256 [0.097, 0.390] | 69: 0.000 [0.000, 0.000] |

changed order's effect 0.428 [0.301, 0.520]; original order's effect 0.380 [0.297, 0.491]; examples [{'scene': 'P2-L0-0208', 'original': 'after', 'changed': 'before', 'switched': 1}, {'scene': 'P2-L0-0041', 'original': 'after', 'changed': 'before', 'switched': 1}, {'scene': 'P2-L0-0040', 'original': 'after', 'changed': 'before', 'switched': 1}]

## nemotron-3.5-lightning (L14; 200 of 200 lookups in the 2x2)

| | changed before | changed after |
|---|---|---|
| original before | 59: 0.983 [0.941, 1.000] | 26: 0.577 [0.385, 0.769] |
| original after | 36: 0.361 [0.222, 0.500] | 79: 0.051 [0.012, 0.102] |

changed order's effect 0.358 [0.235, 0.489]; original order's effect 0.574 [0.453, 0.681]; examples []

## qwen3.5-122b-a10b (L33; 200 of 200 lookups in the 2x2)

| | changed before | changed after |
|---|---|---|
| original before | 53: 0.962 [0.902, 1.000] | 32: 0.781 [0.633, 0.938] |
| original after | 33: 0.364 [0.200, 0.565] | 82: 0.012 [0.000, 0.042] |

changed order's effect 0.266 [0.157, 0.375]; original order's effect 0.684 [0.557, 0.802]; examples []

