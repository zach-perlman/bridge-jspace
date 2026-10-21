# attn_knockout / d2_ko_tie_country_v1

Measure: correct (items: {"BLR": {"items": 25, "unedited_right": 25}, "BRL": {"items": 25, "unedited_right": 25}, "country-R": {"items": 25, "unedited_right": 25}, "country-B": {"items": 25, "unedited_right": 25}})

Claims: {
 "positive_control": {
  "BLR": {
   "sources": {
    "lookup": "needed",
    "binding": "needed"
   },
   "passed": true
  },
  "BRL": {
   "sources": {
    "lookup": "needed",
    "binding": "needed"
   },
   "passed": true
  },
  "country-B": {
   "sources": {
    "binding": "needed"
   },
   "passed": true
  }
 },
 "C1a_RL_breaks_RR_survives": {
  "RL": null,
  "RR": null,
  "holds": false
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": null,
   "question": null
  },
  "RL": {
   "final": null,
   "question": null
  },
  "BLR": {
   "final": "needed",
   "question": "needed"
  },
  "BRL": {
   "final": "needed",
   "question": "partial"
  }
 },
 "C1b_holds": false,
 "relay_holds": false,
 "recall_needs_no_locker": {
  "BR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "RR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  }
 },
 "binding_BL_vs_BR": {
  "BL": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BLR": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  },
  "BRL": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  }
 },
 "bands": {
  "BLR/lookup/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32"
   ],
   "pre_needed": [
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 48
  },
  "BLR/lookup/final": {
   "windows_needed": [
    "win32-39",
    "win32-39:attn"
   ],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32"
   ],
   "pre_needed": [
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 40
  },
  "BLR/lookup/both": {
   "windows_needed": [
    "win32-39",
    "win32-39:attn"
   ],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32",
    "suf40"
   ],
   "pre_needed": [
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 40,
   "pre_min_needed": 40
  },
  "BLR/binding/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 8,
   "pre_min_needed": 32
  },
  "BLR/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BLR/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08"
   ],
   "pre_needed": [
    "pre24",
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 8,
   "pre_min_needed": 24
  },
  "BRL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BRL/lookup/final": {
   "windows_needed": [
    "win40-47",
    "win40-47:attn",
    "win48-55",
    "win48-55:attn"
   ],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32",
    "suf40",
    "suf48"
   ],
   "pre_needed": [
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 48,
   "pre_min_needed": 48
  },
  "BRL/lookup/both": {
   "windows_needed": [
    "win40-47",
    "win40-47:attn",
    "win48-55",
    "win48-55:attn"
   ],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32",
    "suf40",
    "suf48"
   ],
   "pre_needed": [
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 48,
   "pre_min_needed": 48
  },
  "BRL/binding/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 8,
   "pre_min_needed": 32
  },
  "BRL/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BRL/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 8,
   "pre_min_needed": 32
  },
  "country-R/binding/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "country-R/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "country-R/binding/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "country-B/binding/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24"
   ],
   "pre_needed": [
    "pre24",
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 24,
   "pre_min_needed": 24
  },
  "country-B/binding/final": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32"
   ],
   "pre_needed": [
    "pre56"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 56
  },
  "country-B/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32"
   ],
   "pre_needed": [
    "pre24",
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 24
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BLR | binding | after | all | absent | 25 | 40% [23,59] | 24% | -1.65 [-2.06,-1.28] | 0.98 | +60 [+40,+80] | needed |
| BLR | binding | after | all | value | 25 | 44% [27,63] | 40% | -1.65 [-2.07,-1.27] | 0.95 | +56 [+36,+76] | needed |
| BLR | binding | both | all | absent | 25 | 28% [14,48] | 8% | -1.57 [-1.97,-1.23] | 0.99 | +68 [+52,+88] | needed |
| BLR | binding | both | all | value | 25 | 28% [14,48] | 8% | -1.58 [-1.97,-1.24] | 0.98 | +72 [+56,+88] | needed |
| BLR | binding | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | pre24 | value | 25 | 72% [52,86] | 12% | -0.70 [-0.95,-0.48] | 0.98 | +28 [+12,+48] | needed |
| BLR | binding | both | pre32 | value | 25 | 32% [17,52] | 8% | -1.55 [-1.95,-1.20] | 0.98 | +64 [+44,+84] | needed |
| BLR | binding | both | pre40 | value | 25 | 28% [14,48] | 8% | -1.53 [-1.93,-1.19] | 0.98 | +72 [+56,+88] | needed |
| BLR | binding | both | pre48 | value | 25 | 28% [14,48] | 8% | -1.60 [-2.00,-1.25] | 0.98 | +72 [+56,+88] | needed |
| BLR | binding | both | pre56 | value | 25 | 28% [14,48] | 8% | -1.57 [-1.97,-1.23] | 0.98 | +72 [+56,+88] | needed |
| BLR | binding | both | suf08 | value | 25 | 40% [23,59] | 12% | -1.30 [-1.66,-1.00] | 0.98 | +60 [+40,+80] | needed |
| BLR | binding | both | suf16 | value | 25 | 72% [52,86] | 20% | -0.74 [-1.03,-0.49] | 0.98 | +24 [+8,+40] | partial |
| BLR | binding | both | suf24 | value | 25 | 88% [70,96] | 12% | -0.36 [-0.53,-0.21] | 0.98 | +12 [+0,+24] | partial |
| BLR | binding | both | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.06,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.09,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.11 [-0.18,-0.05] | 0.98 | -4 [-12,+0] | partial |
| BLR | binding | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.09 [-0.15,-0.04] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | final | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | pre56 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win32-39 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | binding | question | all | value | 25 | 28% [14,48] | 8% | -1.57 [-1.96,-1.24] | 0.98 | +68 [+52,+88] | needed |
| BLR | binding | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.06,-0.02] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | question | pre24 | value | 25 | 76% [57,89] | 12% | -0.70 [-0.94,-0.48] | 0.98 | +24 [+8,+40] | partial |
| BLR | binding | question | pre32 | value | 25 | 32% [17,52] | 8% | -1.53 [-1.91,-1.20] | 0.98 | +64 [+44,+84] | needed |
| BLR | binding | question | pre40 | value | 25 | 32% [17,52] | 8% | -1.54 [-1.92,-1.21] | 0.98 | +64 [+44,+84] | needed |
| BLR | binding | question | pre48 | value | 25 | 28% [14,48] | 8% | -1.58 [-1.96,-1.25] | 0.98 | +68 [+52,+88] | needed |
| BLR | binding | question | pre56 | value | 25 | 28% [14,48] | 8% | -1.57 [-1.95,-1.25] | 0.98 | +68 [+52,+88] | needed |
| BLR | binding | question | suf08 | value | 25 | 44% [27,63] | 12% | -1.31 [-1.66,-1.01] | 0.98 | +52 [+32,+72] | needed |
| BLR | binding | question | suf16 | value | 25 | 76% [57,89] | 20% | -0.74 [-1.02,-0.50] | 0.98 | +20 [+4,+36] | partial |
| BLR | binding | question | suf24 | value | 25 | 88% [70,96] | 12% | -0.39 [-0.58,-0.22] | 0.98 | +8 [-8,+24] | partial |
| BLR | binding | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win08-15 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | question | win16-23 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.09,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.12 [-0.19,-0.06] | 0.98 | -4 [-12,+0] | partial |
| BLR | binding | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.10 [-0.17,-0.04] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding_off | after | all | absent | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.98 | - | partial |
| BLR | binding_off | after | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.95 | - | partial |
| BLR | binding_off | both | all | absent | 25 | 96% [80,99] | 0% | -0.06 [-0.14,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | all | value | 25 | 100% [87,100] | 0% | -0.04 [-0.10,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | pre32 | value | 25 | 96% [80,99] | 0% | -0.06 [-0.14,-0.01] | 0.98 | - | partial |
| BLR | binding_off | both | pre40 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.10,-0.01] | 0.98 | - | partial |
| BLR | binding_off | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.11,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | pre56 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.10,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf08 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.10,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf16 | value | 25 | 96% [80,99] | 0% | -0.05 [-0.12,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf24 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.09,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | binding_off | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BLR | binding_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| BLR | binding_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win24-31 | value | 25 | 96% [80,99] | 0% | -0.05 [-0.13,-0.01] | 0.99 | - | partial |
| BLR | binding_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.03 [-0.09,-0.01] | - | - | partial |
| BLR | binding_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | binding_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | all | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf24 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | binding_off | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf48 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | question | all | value | 25 | 96% [80,99] | 0% | -0.07 [-0.16,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | pre32 | value | 25 | 96% [80,99] | 0% | -0.06 [-0.14,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | pre40 | value | 25 | 96% [80,99] | 0% | -0.06 [-0.15,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | pre48 | value | 25 | 96% [80,99] | 0% | -0.07 [-0.17,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | pre56 | value | 25 | 96% [80,99] | 0% | -0.07 [-0.16,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | suf08 | value | 25 | 96% [80,99] | 0% | -0.06 [-0.15,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | suf16 | value | 25 | 96% [80,99] | 0% | -0.07 [-0.17,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | suf24 | value | 25 | 96% [80,99] | 0% | -0.05 [-0.13,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | suf48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BLR | binding_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | binding_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| BLR | binding_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win24-31 | value | 25 | 96% [80,99] | 0% | -0.05 [-0.12,-0.01] | 0.98 | - | partial |
| BLR | binding_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.04 [-0.09,-0.01] | - | - | partial |
| BLR | binding_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | binding_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | binding_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup | after | all | absent | 25 | 8% [2,25] | 68% | -3.35 [-3.90,-2.77] | 0.98 | +92 [+80,+100] | needed |
| BLR | lookup | after | all | value | 25 | 8% [2,25] | 68% | -3.32 [-3.92,-2.71] | 0.94 | +92 [+80,+100] | needed |
| BLR | lookup | both | all | absent | 25 | 12% [4,30] | 64% | -3.23 [-3.82,-2.60] | 0.99 | +88 [+76,+100] | needed |
| BLR | lookup | both | all | value | 25 | 12% [4,30] | 64% | -3.28 [-3.88,-2.64] | 0.97 | +88 [+76,+100] | needed |
| BLR | lookup | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre32 | value | 25 | 92% [75,98] | 4% | -0.21 [-0.49,-0.02] | 0.97 | +8 [+0,+20] | partial |
| BLR | lookup | both | pre40 | value | 25 | 64% [45,80] | 32% | -0.99 [-1.54,-0.53] | 0.97 | +36 [+20,+56] | needed |
| BLR | lookup | both | pre48 | value | 25 | 16% [6,35] | 60% | -2.45 [-2.95,-1.94] | 0.97 | +84 [+68,+96] | needed |
| BLR | lookup | both | pre56 | value | 25 | 12% [4,30] | 64% | -3.27 [-3.86,-2.63] | 0.97 | +88 [+76,+100] | needed |
| BLR | lookup | both | suf08 | value | 25 | 12% [4,30] | 64% | -3.25 [-3.84,-2.61] | 0.97 | +88 [+76,+100] | needed |
| BLR | lookup | both | suf16 | value | 25 | 12% [4,30] | 68% | -3.28 [-3.89,-2.63] | 0.97 | +88 [+76,+100] | needed |
| BLR | lookup | both | suf24 | value | 25 | 12% [4,30] | 68% | -3.28 [-3.85,-2.67] | 0.97 | +88 [+76,+100] | needed |
| BLR | lookup | both | suf32 | value | 25 | 12% [4,30] | 68% | -3.40 [-3.96,-2.78] | 0.98 | +88 [+76,+100] | needed |
| BLR | lookup | both | suf40 | value | 25 | 68% [48,83] | 20% | -0.60 [-0.93,-0.33] | 0.98 | +32 [+16,+52] | needed |
| BLR | lookup | both | suf48 | value | 25 | 84% [65,94] | 12% | -0.21 [-0.33,-0.10] | 0.98 | +16 [+4,+32] | partial |
| BLR | lookup | both | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win24-31 | value | 25 | 92% [75,98] | 4% | -0.16 [-0.38,-0.02] | 0.96 | +8 [+0,+20] | partial |
| BLR | lookup | both | win24-31:attn | value | 25 | 92% [75,98] | 4% | -0.12 [-0.25,-0.03] | - | +8 [+0,+20] | partial |
| BLR | lookup | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | both | win32-39 | value | 25 | 64% [45,80] | 32% | -1.05 [-1.64,-0.53] | 0.97 | +36 [+16,+56] | needed |
| BLR | lookup | both | win32-39:attn | value | 25 | 68% [48,83] | 28% | -0.97 [-1.55,-0.48] | - | +32 [+16,+52] | needed |
| BLR | lookup | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.03 [-0.07,-0.01] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win40-47 | value | 25 | 96% [80,99] | 0% | -0.15 [-0.28,-0.05] | 0.97 | +4 [+0,+12] | partial |
| BLR | lookup | both | win40-47:attn | value | 25 | 96% [80,99] | 0% | -0.13 [-0.25,-0.05] | - | +4 [+0,+12] | partial |
| BLR | lookup | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win48-55 | value | 25 | 88% [70,96] | 8% | -0.18 [-0.29,-0.08] | 0.98 | +12 [+0,+24] | partial |
| BLR | lookup | both | win48-55:attn | value | 25 | 92% [75,98] | 8% | -0.15 [-0.24,-0.07] | - | +8 [+0,+20] | partial |
| BLR | lookup | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | all | value | 25 | 20% [9,39] | 68% | -3.12 [-3.83,-2.42] | 0.99 | +80 [+64,+96] | needed |
| BLR | lookup | final | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | final | pre40 | value | 25 | 68% [48,83] | 28% | -0.93 [-1.51,-0.46] | 0.98 | +32 [+16,+52] | needed |
| BLR | lookup | final | pre48 | value | 25 | 60% [41,77] | 36% | -1.15 [-1.83,-0.57] | 0.99 | +40 [+24,+60] | needed |
| BLR | lookup | final | pre56 | value | 25 | 20% [9,39] | 68% | -3.13 [-3.84,-2.41] | 0.99 | +80 [+64,+96] | needed |
| BLR | lookup | final | suf08 | value | 25 | 16% [6,35] | 68% | -3.13 [-3.85,-2.43] | 0.99 | +84 [+68,+96] | needed |
| BLR | lookup | final | suf16 | value | 25 | 20% [9,39] | 68% | -3.10 [-3.81,-2.42] | 0.99 | +80 [+64,+96] | needed |
| BLR | lookup | final | suf24 | value | 25 | 16% [6,35] | 68% | -3.09 [-3.80,-2.41] | 0.99 | +84 [+68,+96] | needed |
| BLR | lookup | final | suf32 | value | 25 | 20% [9,39] | 68% | -2.99 [-3.70,-2.31] | 0.99 | +80 [+64,+96] | needed |
| BLR | lookup | final | suf40 | value | 25 | 84% [65,94] | 12% | -0.24 [-0.44,-0.09] | 0.99 | +16 [+4,+32] | partial |
| BLR | lookup | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.13 [-0.20,-0.06] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | +0 [+0,+0] | partial |
| BLR | lookup | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | final | win32-39 | value | 25 | 68% [48,83] | 28% | -0.86 [-1.37,-0.42] | 0.99 | +32 [+16,+52] | needed |
| BLR | lookup | final | win32-39:attn | value | 25 | 68% [48,83] | 28% | -0.82 [-1.29,-0.41] | - | +32 [+16,+52] | needed |
| BLR | lookup | final | win32-39:gdn | value | 25 | 96% [80,99] | 0% | -0.05 [-0.15,-0.01] | 0.99 | +4 [+0,+12] | partial |
| BLR | lookup | final | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.12 [-0.19,-0.05] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.10 [-0.16,-0.04] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | +0 [+0,+0] | partial |
| BLR | lookup | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | +0 [+0,+0] | partial |
| BLR | lookup | question | all | value | 25 | 60% [41,77] | 28% | -0.93 [-1.23,-0.65] | 0.97 | +40 [+20,+60] | needed |
| BLR | lookup | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | question | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | question | pre32 | value | 25 | 92% [75,98] | 4% | -0.17 [-0.40,-0.02] | 0.96 | +8 [+0,+20] | partial |
| BLR | lookup | question | pre40 | value | 25 | 92% [75,98] | 4% | -0.20 [-0.40,-0.08] | 0.96 | +8 [+0,+20] | partial |
| BLR | lookup | question | pre48 | value | 25 | 56% [37,73] | 32% | -0.93 [-1.21,-0.65] | 0.96 | +44 [+24,+64] | needed |
| BLR | lookup | question | pre56 | value | 25 | 60% [41,77] | 28% | -0.92 [-1.21,-0.65] | 0.96 | +40 [+20,+60] | needed |
| BLR | lookup | question | suf08 | value | 25 | 52% [33,70] | 36% | -0.92 [-1.21,-0.65] | 0.96 | +48 [+28,+68] | needed |
| BLR | lookup | question | suf16 | value | 25 | 56% [37,73] | 28% | -0.89 [-1.17,-0.63] | 0.97 | +44 [+24,+64] | needed |
| BLR | lookup | question | suf24 | value | 25 | 60% [41,77] | 24% | -0.90 [-1.19,-0.62] | 0.97 | +40 [+20,+60] | needed |
| BLR | lookup | question | suf32 | value | 25 | 68% [48,83] | 20% | -0.68 [-0.96,-0.40] | 0.97 | +32 [+12,+48] | needed |
| BLR | lookup | question | suf40 | value | 25 | 96% [80,99] | 0% | -0.13 [-0.27,-0.04] | 0.97 | +4 [+0,+12] | partial |
| BLR | lookup | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BLR | lookup | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win24-31 | value | 25 | 92% [75,98] | 4% | -0.15 [-0.36,-0.02] | 0.95 | +8 [+0,+20] | partial |
| BLR | lookup | question | win24-31:attn | value | 25 | 92% [75,98] | 4% | -0.12 [-0.25,-0.02] | - | +8 [+0,+20] | partial |
| BLR | lookup | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BLR | lookup | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.06 [-0.10,-0.03] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win32-39:attn | value | 25 | 96% [80,99] | 0% | -0.06 [-0.14,-0.02] | - | +4 [+0,+12] | partial |
| BLR | lookup | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | question | win40-47 | value | 25 | 96% [80,99] | 0% | -0.12 [-0.25,-0.03] | 0.97 | +4 [+0,+12] | partial |
| BLR | lookup | question | win40-47:attn | value | 25 | 96% [80,99] | 0% | -0.11 [-0.24,-0.03] | - | +4 [+0,+12] | partial |
| BLR | lookup | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | question | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup_off | after | all | absent | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | after | all | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.95 | - | partial |
| BLR | lookup_off | both | all | absent | 25 | 100% [87,100] | 0% | -0.02 [-0.08,+0.02] | 0.99 | - | partial |
| BLR | lookup_off | both | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.05,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | pre32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | pre40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.06,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | pre56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | suf08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | suf16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | suf24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | suf48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| BLR | lookup_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| BLR | lookup_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| BLR | lookup_off | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| BLR | lookup_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BLR | lookup_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | lookup_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | partial |
| BLR | lookup_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | partial |
| BLR | lookup_off | question | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.07,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.01] | 0.96 | - | partial |
| BLR | lookup_off | question | pre40 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.05,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | question | pre48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.06,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | question | pre56 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.05,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | question | suf08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | question | suf16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.05,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | question | suf24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | question | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | suf48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | question | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.96 | - | partial |
| BLR | lookup_off | question | win24-31 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| BLR | lookup_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| BLR | lookup_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| BLR | lookup_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.96 | - | partial |
| BLR | lookup_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | random | after | all | absent | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.99 | - | partial |
| BLR | random | after | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.95 | - | partial |
| BLR | random | both | all | absent | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 1.00 | - | partial |
| BLR | random | both | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | partial |
| BLR | random | final | all | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | partial |
| BLR | random | question | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BLR | trailing | after | all | absent | 25 | 84% [65,94] | 16% | -0.38 [-0.63,-0.17] | 0.99 | - | partial |
| BLR | trailing | after | all | value | 25 | 96% [80,99] | 4% | -0.11 [-0.20,-0.05] | 0.95 | - | partial |
| BLR | trailing | both | all | absent | 25 | 100% [87,100] | 0% | -0.02 [-0.05,-0.00] | 0.99 | - | partial |
| BLR | trailing | both | all | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,-0.00] | 0.98 | - | partial |
| BLR | trailing | final | all | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BLR | trailing | question | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.00] | 0.98 | - | partial |
| BRL | binding | after | all | absent | 25 | 16% [6,35] | 84% | -1.79 [-2.11,-1.48] | 0.98 | +84 [+68,+96] | needed |
| BRL | binding | after | all | value | 25 | 24% [11,43] | 76% | -1.85 [-2.24,-1.49] | 0.95 | +76 [+60,+92] | needed |
| BRL | binding | both | all | absent | 25 | 56% [37,73] | 44% | -0.94 [-1.10,-0.80] | 0.99 | +40 [+20,+60] | needed |
| BRL | binding | both | all | value | 25 | 60% [41,77] | 40% | -0.92 [-1.07,-0.78] | 0.98 | +40 [+20,+60] | needed |
| BRL | binding | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.11 [-0.17,-0.05] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | pre24 | value | 25 | 84% [65,94] | 16% | -0.53 [-0.69,-0.39] | 0.98 | +16 [+4,+32] | partial |
| BRL | binding | both | pre32 | value | 25 | 68% [48,83] | 32% | -0.78 [-0.93,-0.64] | 0.98 | +32 [+16,+52] | needed |
| BRL | binding | both | pre40 | value | 25 | 60% [41,77] | 40% | -0.84 [-0.97,-0.71] | 0.98 | +40 [+20,+60] | needed |
| BRL | binding | both | pre48 | value | 25 | 60% [41,77] | 40% | -0.92 [-1.08,-0.79] | 0.98 | +40 [+20,+60] | needed |
| BRL | binding | both | pre56 | value | 25 | 60% [41,77] | 40% | -0.91 [-1.06,-0.78] | 0.98 | +36 [+16,+56] | needed |
| BRL | binding | both | suf08 | value | 25 | 56% [37,73] | 44% | -0.92 [-1.07,-0.78] | 0.98 | +40 [+20,+60] | needed |
| BRL | binding | both | suf16 | value | 25 | 80% [61,91] | 20% | -0.68 [-0.89,-0.50] | 0.98 | +20 [+4,+36] | partial |
| BRL | binding | both | suf24 | value | 25 | 76% [57,89] | 24% | -0.77 [-0.97,-0.59] | 0.98 | +24 [+8,+40] | partial |
| BRL | binding | both | suf32 | value | 25 | 100% [87,100] | 0% | -0.13 [-0.21,-0.07] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.16 [-0.26,-0.09] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win24-31:attn | value | 25 | 92% [75,98] | 4% | -0.20 [-0.33,-0.10] | - | +8 [+0,+20] | partial |
| BRL | binding | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win32-39 | value | 25 | 96% [80,99] | 0% | -0.14 [-0.28,-0.04] | 0.98 | +4 [+0,+12] | partial |
| BRL | binding | both | win32-39:attn | value | 25 | 96% [80,99] | 0% | -0.12 [-0.25,-0.03] | - | +4 [+0,+12] | partial |
| BRL | binding | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | final | all | value | 25 | 100% [87,100] | 0% | -0.04 [-0.08,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.08 [-0.13,-0.03] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.09,-0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | pre56 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.08,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf08 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.09,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf16 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.09,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf24 | value | 25 | 96% [80,99] | 4% | -0.08 [-0.13,-0.04] | 0.99 | +4 [+0,+12] | partial |
| BRL | binding | final | suf32 | value | 25 | 100% [87,100] | 0% | -0.07 [-0.12,-0.03] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win32-39 | value | 25 | 96% [80,99] | 0% | -0.10 [-0.24,-0.02] | 0.99 | +4 [+0,+12] | partial |
| BRL | binding | final | win32-39:attn | value | 25 | 96% [80,99] | 0% | -0.09 [-0.22,-0.02] | - | +4 [+0,+12] | partial |
| BRL | binding | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | binding | question | all | value | 25 | 64% [45,80] | 36% | -0.81 [-0.94,-0.70] | 0.98 | +36 [+20,+56] | needed |
| BRL | binding | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.08 [-0.13,-0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | pre24 | value | 25 | 88% [70,96] | 12% | -0.52 [-0.67,-0.39] | 0.98 | +12 [+0,+24] | partial |
| BRL | binding | question | pre32 | value | 25 | 64% [45,80] | 36% | -0.80 [-0.95,-0.67] | 0.98 | +36 [+20,+56] | needed |
| BRL | binding | question | pre40 | value | 25 | 68% [48,83] | 32% | -0.77 [-0.90,-0.65] | 0.98 | +32 [+16,+52] | needed |
| BRL | binding | question | pre48 | value | 25 | 68% [48,83] | 32% | -0.81 [-0.94,-0.69] | 0.98 | +32 [+16,+52] | needed |
| BRL | binding | question | pre56 | value | 25 | 64% [45,80] | 36% | -0.81 [-0.95,-0.69] | 0.98 | +36 [+20,+56] | needed |
| BRL | binding | question | suf08 | value | 25 | 64% [45,80] | 36% | -0.81 [-0.94,-0.69] | 0.98 | +36 [+20,+56] | needed |
| BRL | binding | question | suf16 | value | 25 | 80% [61,91] | 20% | -0.58 [-0.78,-0.41] | 0.98 | +20 [+4,+36] | partial |
| BRL | binding | question | suf24 | value | 25 | 80% [61,91] | 16% | -0.67 [-0.87,-0.47] | 0.98 | +20 [+8,+36] | partial |
| BRL | binding | question | suf32 | value | 25 | 96% [80,99] | 0% | -0.03 [-0.07,-0.01] | 0.98 | +4 [+0,+12] | partial |
| BRL | binding | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.03] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.17 [-0.26,-0.09] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win24-31:attn | value | 25 | 92% [75,98] | 4% | -0.20 [-0.33,-0.09] | - | +8 [+0,+20] | partial |
| BRL | binding | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,-0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding_off | after | all | absent | 25 | 100% [87,100] | 0% | +0.03 [-0.01,+0.06] | 0.98 | - | partial |
| BRL | binding_off | after | all | value | 25 | 100% [87,100] | 0% | +0.02 [-0.02,+0.06] | 0.95 | - | partial |
| BRL | binding_off | both | all | absent | 25 | 96% [80,99] | 0% | -0.04 [-0.11,+0.02] | 0.99 | - | partial |
| BRL | binding_off | both | all | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BRL | binding_off | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.03] | 0.98 | - | partial |
| BRL | binding_off | both | pre40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.03] | 0.98 | - | partial |
| BRL | binding_off | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.07,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | pre56 | value | 25 | 96% [80,99] | 0% | -0.02 [-0.07,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | suf08 | value | 25 | 96% [80,99] | 0% | -0.02 [-0.07,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | suf16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.03] | 0.98 | - | partial |
| BRL | binding_off | both | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | - | partial |
| BRL | binding_off | both | suf32 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.01] | 0.98 | - | partial |
| BRL | binding_off | both | suf40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | binding_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | - | - | partial |
| BRL | binding_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | binding_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | - | - | partial |
| BRL | binding_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | binding_off | both | win24-31 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | - | - | partial |
| BRL | binding_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BRL | binding_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| BRL | binding_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.01] | - | - | partial |
| BRL | binding_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | final | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | final | pre24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.03,+0.04] | 0.99 | - | partial |
| BRL | binding_off | final | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.03,+0.04] | 0.99 | - | partial |
| BRL | binding_off | final | pre48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | suf08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.99 | - | partial |
| BRL | binding_off | final | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BRL | binding_off | final | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | suf40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | binding_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| BRL | binding_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | - | - | partial |
| BRL | binding_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | partial |
| BRL | binding_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | binding_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BRL | binding_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | binding_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.00] | - | - | partial |
| BRL | binding_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | question | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | binding_off | question | pre24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | binding_off | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | pre40 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.01,+0.05] | 0.98 | - | partial |
| BRL | binding_off | question | pre48 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | pre56 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | suf08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | suf16 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.05] | 0.98 | - | partial |
| BRL | binding_off | question | suf24 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.05] | 0.98 | - | partial |
| BRL | binding_off | question | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BRL | binding_off | question | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | binding_off | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | binding_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| BRL | binding_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | binding_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| BRL | binding_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win24-31 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.04] | 0.98 | - | partial |
| BRL | binding_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | - | - | partial |
| BRL | binding_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | binding_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | partial |
| BRL | binding_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| BRL | binding_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BRL | binding_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BRL | binding_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | lookup | after | all | absent | 25 | 0% [0,13] | 96% | -5.93 [-6.53,-5.35] | 0.98 | +96 [+88,+100] | needed |
| BRL | lookup | after | all | value | 25 | 0% [0,13] | 96% | -5.81 [-6.38,-5.23] | 0.93 | +100 [+100,+100] | needed |
| BRL | lookup | both | all | absent | 25 | 0% [0,13] | 96% | -6.18 [-6.74,-5.58] | 0.99 | +100 [+100,+100] | needed |
| BRL | lookup | both | all | value | 25 | 0% [0,13] | 96% | -6.36 [-6.95,-5.72] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | pre08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre40 | value | 25 | 96% [80,99] | 0% | -0.07 [-0.15,-0.01] | 0.97 | +4 [+0,+12] | partial |
| BRL | lookup | both | pre48 | value | 25 | 48% [30,67] | 40% | -1.34 [-1.76,-0.94] | 0.97 | +52 [+32,+72] | needed |
| BRL | lookup | both | pre56 | value | 25 | 0% [0,13] | 92% | -3.57 [-4.10,-3.05] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf08 | value | 25 | 0% [0,13] | 96% | -6.33 [-6.94,-5.65] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf16 | value | 25 | 0% [0,13] | 96% | -6.23 [-6.84,-5.60] | 0.97 | +96 [+88,+100] | needed |
| BRL | lookup | both | suf24 | value | 25 | 0% [0,13] | 96% | -6.13 [-6.77,-5.50] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf32 | value | 25 | 0% [0,13] | 96% | -6.15 [-6.78,-5.54] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf40 | value | 25 | 0% [0,13] | 96% | -6.35 [-6.80,-5.95] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf48 | value | 25 | 0% [0,13] | 100% | -6.52 [-6.88,-6.12] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf56 | value | 25 | 96% [80,99] | 4% | -0.09 [-0.15,-0.03] | 0.98 | +4 [+0,+12] | partial |
| BRL | lookup | both | win00-07 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.03] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.03] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.04,+0.02] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | both | win32-39 | value | 25 | 96% [80,99] | 4% | -0.11 [-0.25,-0.02] | 0.96 | +4 [+0,+12] | partial |
| BRL | lookup | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.07 [-0.14,-0.01] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | both | win40-47 | value | 25 | 64% [45,80] | 32% | -0.74 [-0.99,-0.51] | 0.96 | +36 [+20,+56] | needed |
| BRL | lookup | both | win40-47:attn | value | 25 | 68% [48,83] | 28% | -0.71 [-0.97,-0.47] | - | +32 [+16,+52] | needed |
| BRL | lookup | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | both | win48-55 | value | 25 | 64% [45,80] | 36% | -0.73 [-0.99,-0.51] | 0.97 | +36 [+20,+56] | needed |
| BRL | lookup | both | win48-55:attn | value | 25 | 60% [41,77] | 36% | -0.87 [-1.16,-0.62] | - | +40 [+24,+60] | needed |
| BRL | lookup | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win56-63 | value | 25 | 96% [80,99] | 4% | -0.09 [-0.16,-0.03] | 0.98 | +4 [+0,+12] | partial |
| BRL | lookup | both | win56-63:attn | value | 25 | 96% [80,99] | 4% | -0.09 [-0.15,-0.03] | - | +4 [+0,+12] | partial |
| BRL | lookup | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | all | value | 25 | 0% [0,13] | 92% | -5.71 [-6.19,-5.23] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | lookup | final | pre16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | +0 [+0,+0] | partial |
| BRL | lookup | final | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.08 [-0.14,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | pre48 | value | 25 | 40% [23,59] | 48% | -1.40 [-1.82,-1.02] | 0.98 | +60 [+40,+80] | needed |
| BRL | lookup | final | pre56 | value | 25 | 0% [0,13] | 88% | -3.34 [-3.84,-2.86] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf08 | value | 25 | 0% [0,13] | 92% | -5.73 [-6.21,-5.23] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf16 | value | 25 | 0% [0,13] | 96% | -5.73 [-6.21,-5.22] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf24 | value | 25 | 0% [0,13] | 96% | -5.58 [-6.08,-5.09] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf32 | value | 25 | 0% [0,13] | 96% | -5.60 [-6.13,-5.06] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf40 | value | 25 | 0% [0,13] | 96% | -5.61 [-6.07,-5.19] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf48 | value | 25 | 0% [0,13] | 100% | -5.81 [-6.15,-5.45] | 0.99 | +100 [+100,+100] | needed |
| BRL | lookup | final | suf56 | value | 25 | 96% [80,99] | 4% | -0.08 [-0.15,-0.03] | 0.99 | +4 [+0,+12] | partial |
| BRL | lookup | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | lookup | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BRL | lookup | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | +0 [+0,+0] | partial |
| BRL | lookup | final | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.04] | - | +0 [+0,+0] | partial |
| BRL | lookup | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | - | +0 [+0,+0] | partial |
| BRL | lookup | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | final | win32-39 | value | 25 | 92% [75,98] | 4% | -0.12 [-0.26,-0.02] | 0.97 | +8 [+0,+20] | partial |
| BRL | lookup | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.06 [-0.14,-0.01] | - | +0 [+0,+0] | partial |
| BRL | lookup | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.03 [-0.06,-0.01] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | final | win40-47 | value | 25 | 64% [45,80] | 32% | -0.71 [-0.97,-0.48] | 0.97 | +36 [+20,+56] | needed |
| BRL | lookup | final | win40-47:attn | value | 25 | 68% [48,83] | 28% | -0.67 [-0.93,-0.44] | - | +32 [+16,+52] | needed |
| BRL | lookup | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | final | win48-55 | value | 25 | 60% [41,77] | 40% | -0.76 [-1.01,-0.54] | 0.98 | +40 [+20,+60] | needed |
| BRL | lookup | final | win48-55:attn | value | 25 | 56% [37,73] | 40% | -0.91 [-1.18,-0.66] | - | +44 [+28,+64] | needed |
| BRL | lookup | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | win56-63 | value | 25 | 96% [80,99] | 4% | -0.09 [-0.16,-0.03] | 0.99 | +4 [+0,+12] | partial |
| BRL | lookup | final | win56-63:attn | value | 25 | 96% [80,99] | 4% | -0.08 [-0.15,-0.03] | - | +4 [+0,+12] | partial |
| BRL | lookup | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BRL | lookup | question | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.02] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.02] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | question | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | question | win08-15 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup_off | after | all | absent | 25 | 96% [80,99] | 0% | -0.02 [-0.15,+0.06] | 0.98 | - | partial |
| BRL | lookup_off | after | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.05,+0.06] | 0.94 | - | partial |
| BRL | lookup_off | both | all | absent | 25 | 100% [87,100] | 0% | -0.01 [-0.06,+0.03] | 0.99 | - | partial |
| BRL | lookup_off | both | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | pre08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | both | pre16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | both | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | pre32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf16 | value | 25 | 96% [80,99] | 0% | -0.02 [-0.09,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | suf24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | 0.98 | - | partial |
| BRL | lookup_off | both | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BRL | lookup_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | lookup_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | lookup_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.96 | - | partial |
| BRL | lookup_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | lookup_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.96 | - | partial |
| BRL | lookup_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | - | - | partial |
| BRL | lookup_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BRL | lookup_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | partial |
| BRL | lookup_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | final | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | lookup_off | final | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | partial |
| BRL | lookup_off | final | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | pre48 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | pre56 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | suf08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | suf24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.05,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | suf32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | partial |
| BRL | lookup_off | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | final | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | lookup_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | - | - | partial |
| BRL | lookup_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | lookup_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | - | - | partial |
| BRL | lookup_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | - | partial |
| BRL | lookup_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| BRL | lookup_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BRL | lookup_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | - | - | partial |
| BRL | lookup_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| BRL | lookup_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BRL | lookup_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | lookup_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| BRL | lookup_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | question | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | question | pre08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | question | pre16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | question | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.96 | - | partial |
| BRL | lookup_off | question | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | question | pre48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | question | pre56 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.04] | 0.96 | - | partial |
| BRL | lookup_off | question | suf08 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | 0.96 | - | partial |
| BRL | lookup_off | question | suf16 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.03] | 0.96 | - | partial |
| BRL | lookup_off | question | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.96 | - | partial |
| BRL | lookup_off | question | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BRL | lookup_off | question | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| BRL | lookup_off | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | lookup_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.96 | - | partial |
| BRL | lookup_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | - | - | partial |
| BRL | lookup_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.96 | - | partial |
| BRL | lookup_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.02] | 0.96 | - | partial |
| BRL | lookup_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | - | - | partial |
| BRL | lookup_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | - | partial |
| BRL | lookup_off | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.95 | - | partial |
| BRL | lookup_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| BRL | lookup_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | partial |
| BRL | lookup_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.96 | - | partial |
| BRL | lookup_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | lookup_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.96 | - | partial |
| BRL | lookup_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BRL | lookup_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | lookup_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BRL | lookup_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | lookup_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BRL | lookup_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | random | after | all | absent | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.04] | 0.99 | - | partial |
| BRL | random | after | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.03,+0.05] | 0.94 | - | partial |
| BRL | random | both | all | absent | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 1.00 | - | partial |
| BRL | random | both | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | random | final | all | value | 25 | 100% [87,100] | 0% | +0.03 [+0.00,+0.06] | 0.99 | - | partial |
| BRL | random | question | all | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.00] | 0.97 | - | partial |
| BRL | trailing | after | all | absent | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.99 | - | partial |
| BRL | trailing | after | all | value | 25 | 100% [87,100] | 0% | +0.02 [-0.01,+0.05] | 0.96 | - | partial |
| BRL | trailing | both | all | absent | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | trailing | both | all | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | trailing | final | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.99 | - | partial |
| BRL | trailing | question | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | partial |
| country-R | binding | after | all | absent | 25 | 100% [87,100] | 0% | -0.04 [-0.10,+0.01] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | after | all | value | 25 | 100% [87,100] | 0% | -0.09 [-0.14,-0.04] | 0.93 | -8 [-20,+0] | partial |
| country-R | binding | both | all | absent | 25 | 100% [87,100] | 0% | -0.06 [-0.10,-0.02] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | both | all | value | 25 | 100% [87,100] | 0% | -0.04 [-0.09,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.03] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre32 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.06,+0.02] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.07,+0.02] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | pre56 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.08,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | suf08 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.07,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | suf16 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | suf24 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.08,-0.02] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | suf32 | value | 25 | 96% [80,99] | 4% | -0.06 [-0.11,-0.03] | 0.96 | +4 [+0,+12] | partial |
| country-R | binding | both | suf40 | value | 25 | 96% [80,99] | 4% | -0.04 [-0.08,-0.01] | 0.96 | +4 [+0,+12] | partial |
| country-R | binding | both | suf48 | value | 25 | 96% [80,99] | 4% | -0.03 [-0.07,-0.00] | 0.96 | +4 [+0,+12] | partial |
| country-R | binding | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.03] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.02] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.02] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | final | all | value | 25 | 100% [87,100] | 0% | -0.05 [-0.09,-0.02] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | pre56 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.08,-0.03] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf08 | value | 25 | 100% [87,100] | 0% | -0.06 [-0.09,-0.03] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf16 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.08,-0.03] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf24 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.06,-0.02] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf32 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| country-R | binding | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win16-23 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win32-39 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| country-R | binding | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| country-R | binding | question | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | pre16 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.04] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | pre24 | value | 25 | 100% [87,100] | 0% | +0.03 [+0.01,+0.05] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.02,+0.05] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | pre40 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.01,+0.05] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | pre48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.04,+0.04] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | pre56 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.05,+0.03] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | suf08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.04] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | suf16 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.05,+0.00] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | suf24 | value | 25 | 100% [87,100] | 0% | -0.05 [-0.07,-0.02] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.06,-0.02] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | question | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.04] | 0.92 | +0 [+0,+0] | partial |
| country-R | binding | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.03] | 0.92 | +0 [+0,+0] | partial |
| country-R | binding | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.04] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.03] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.00] | 0.92 | +0 [+0,+0] | partial |
| country-R | binding | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.92 | +0 [+0,+0] | partial |
| country-R | binding | question | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.93 | +0 [+0,+0] | partial |
| country-R | binding | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | +0 [+0,+0] | partial |
| country-R | binding | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| country-R | binding | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding_off | after | all | absent | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.00] | 0.97 | - | partial |
| country-R | binding_off | after | all | value | 25 | 92% [75,98] | 0% | -0.08 [-0.13,-0.03] | 0.93 | - | partial |
| country-R | binding_off | both | all | absent | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| country-R | binding_off | both | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.96 | - | partial |
| country-R | binding_off | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,+0.00] | 0.95 | - | partial |
| country-R | binding_off | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.02] | 0.95 | - | partial |
| country-R | binding_off | both | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.03] | 0.95 | - | partial |
| country-R | binding_off | both | pre40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.03,+0.03] | 0.95 | - | partial |
| country-R | binding_off | both | pre48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.03,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | pre56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.03,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | suf08 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.00,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | suf16 | value | 25 | 100% [87,100] | 0% | +0.03 [+0.01,+0.04] | 0.96 | - | partial |
| country-R | binding_off | both | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | suf32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.96 | - | partial |
| country-R | binding_off | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.02,+0.02] | 0.96 | - | partial |
| country-R | binding_off | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.97 | - | partial |
| country-R | binding_off | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| country-R | binding_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.96 | - | partial |
| country-R | binding_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.96 | - | partial |
| country-R | binding_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.94 | - | partial |
| country-R | binding_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.94 | - | partial |
| country-R | binding_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.03] | - | - | partial |
| country-R | binding_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.95 | - | partial |
| country-R | binding_off | both | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.94 | - | partial |
| country-R | binding_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-R | binding_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | - | partial |
| country-R | binding_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | - | partial |
| country-R | binding_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.96 | - | partial |
| country-R | binding_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.95 | - | partial |
| country-R | binding_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| country-R | binding_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.96 | - | partial |
| country-R | binding_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.96 | - | partial |
| country-R | binding_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| country-R | binding_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-R | binding_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| country-R | binding_off | final | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | pre08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| country-R | binding_off | final | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-R | binding_off | final | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.01] | 0.98 | - | partial |
| country-R | binding_off | final | pre48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | pre56 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | suf08 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.99 | - | partial |
| country-R | binding_off | final | suf32 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.03] | 0.99 | - | partial |
| country-R | binding_off | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.99 | - | partial |
| country-R | binding_off | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | - | partial |
| country-R | binding_off | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | partial |
| country-R | binding_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-R | binding_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-R | binding_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | 0.98 | - | partial |
| country-R | binding_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | - | - | partial |
| country-R | binding_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.98 | - | partial |
| country-R | binding_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | partial |
| country-R | binding_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | partial |
| country-R | binding_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | partial |
| country-R | binding_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-R | binding_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-R | binding_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-R | binding_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.00] | 0.99 | - | partial |
| country-R | binding_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-R | binding_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| country-R | binding_off | question | all | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.05] | 0.94 | - | partial |
| country-R | binding_off | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.02] | 0.93 | - | partial |
| country-R | binding_off | question | pre24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.04] | 0.93 | - | partial |
| country-R | binding_off | question | pre32 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.01,+0.06] | 0.93 | - | partial |
| country-R | binding_off | question | pre40 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.05] | 0.93 | - | partial |
| country-R | binding_off | question | pre48 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.05] | 0.93 | - | partial |
| country-R | binding_off | question | pre56 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.02,+0.04] | 0.93 | - | partial |
| country-R | binding_off | question | suf08 | value | 25 | 100% [87,100] | 0% | +0.03 [+0.01,+0.06] | 0.94 | - | partial |
| country-R | binding_off | question | suf16 | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.04] | 0.94 | - | partial |
| country-R | binding_off | question | suf24 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.01,+0.02] | 0.94 | - | partial |
| country-R | binding_off | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.96 | - | partial |
| country-R | binding_off | question | suf56 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| country-R | binding_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-R | binding_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.92 | - | partial |
| country-R | binding_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-R | binding_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | 0.92 | - | partial |
| country-R | binding_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.93 | - | partial |
| country-R | binding_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.93 | - | partial |
| country-R | binding_off | question | win24-31 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.03] | 0.92 | - | partial |
| country-R | binding_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| country-R | binding_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | +0.02 [+0.01,+0.02] | 0.92 | - | partial |
| country-R | binding_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | - | partial |
| country-R | binding_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| country-R | binding_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | - | partial |
| country-R | binding_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.02,+0.01] | 0.93 | - | partial |
| country-R | binding_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| country-R | binding_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.93 | - | partial |
| country-R | binding_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.95 | - | partial |
| country-R | binding_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-R | binding_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.95 | - | partial |
| country-R | binding_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| country-R | binding_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| country-R | binding_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | partial |
| country-R | random | after | all | absent | 25 | 100% [87,100] | 0% | -0.04 [-0.09,+0.02] | 0.98 | - | partial |
| country-R | random | after | all | value | 25 | 96% [80,99] | 0% | -0.09 [-0.15,-0.03] | 0.93 | - | partial |
| country-R | random | both | all | absent | 25 | 100% [87,100] | 0% | -0.02 [-0.06,+0.03] | 0.98 | - | partial |
| country-R | random | both | all | value | 25 | 100% [87,100] | 0% | -0.03 [-0.09,+0.03] | 0.96 | - | partial |
| country-R | random | final | all | value | 25 | 100% [87,100] | 0% | +0.02 [-0.00,+0.06] | 0.99 | - | partial |
| country-R | random | question | all | value | 25 | 100% [87,100] | 0% | -0.02 [-0.08,+0.03] | 0.94 | - | partial |
| country-R | trailing | after | all | absent | 19 | 95% [75,99] | 0% | -0.09 [-0.14,-0.05] | 0.98 | - | partial |
| country-R | trailing | after | all | value | 19 | 100% [83,100] | 0% | -0.09 [-0.14,-0.05] | 0.95 | - | partial |
| country-R | trailing | both | all | absent | 19 | 100% [83,100] | 0% | -0.02 [-0.04,+0.00] | 0.99 | - | partial |
| country-R | trailing | both | all | value | 19 | 100% [83,100] | 0% | -0.02 [-0.04,+0.00] | 0.98 | - | partial |
| country-R | trailing | final | all | value | 19 | 100% [83,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | - | partial |
| country-R | trailing | question | all | value | 19 | 100% [83,100] | 0% | -0.01 [-0.03,+0.00] | 0.97 | - | partial |
| country-B | binding | after | all | absent | 25 | 0% [0,13] | 0% | -7.94 [-8.68,-7.17] | 0.97 | +100 [+100,+100] | needed |
| country-B | binding | after | all | value | 25 | 0% [0,13] | 0% | -7.54 [-8.25,-6.78] | 0.93 | +100 [+100,+100] | needed |
| country-B | binding | both | all | absent | 25 | 0% [0,13] | 0% | -7.84 [-8.55,-7.12] | 0.98 | +100 [+100,+100] | needed |
| country-B | binding | both | all | value | 25 | 0% [0,13] | 0% | -7.60 [-8.32,-6.84] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.03] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | pre24 | value | 25 | 32% [17,52] | 0% | -2.88 [-3.64,-2.16] | 0.95 | +68 [+52,+84] | needed |
| country-B | binding | both | pre32 | value | 25 | 12% [4,30] | 0% | -3.71 [-4.39,-3.05] | 0.94 | +88 [+72,+100] | needed |
| country-B | binding | both | pre40 | value | 25 | 12% [4,30] | 0% | -3.71 [-4.39,-3.03] | 0.95 | +88 [+72,+100] | needed |
| country-B | binding | both | pre48 | value | 25 | 8% [2,25] | 0% | -4.12 [-4.70,-3.53] | 0.95 | +92 [+80,+100] | needed |
| country-B | binding | both | pre56 | value | 25 | 0% [0,13] | 0% | -6.07 [-6.63,-5.50] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf08 | value | 25 | 0% [0,13] | 4% | -7.28 [-8.04,-6.52] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf16 | value | 25 | 0% [0,13] | 4% | -6.22 [-6.99,-5.42] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf24 | value | 25 | 0% [0,13] | 12% | -5.46 [-6.34,-4.60] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf32 | value | 25 | 4% [1,20] | 84% | -6.65 [-7.89,-5.43] | 0.95 | +96 [+88,+100] | needed |
| country-B | binding | both | suf40 | value | 25 | 96% [80,99] | 4% | -0.06 [-0.15,-0.01] | 0.95 | +4 [+0,+12] | partial |
| country-B | binding | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.06,-0.01] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.16 [-0.27,-0.07] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.16 [-0.28,-0.06] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.04,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | final | all | value | 25 | 52% [33,70] | 48% | -2.23 [-3.19,-1.34] | 0.98 | +48 [+28,+68] | needed |
| country-B | binding | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.04,-0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.02] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | pre56 | value | 25 | 56% [37,73] | 44% | -1.48 [-2.12,-0.88] | 0.98 | +44 [+24,+64] | needed |
| country-B | binding | final | suf08 | value | 25 | 52% [33,70] | 48% | -2.19 [-3.15,-1.33] | 0.98 | +48 [+28,+68] | needed |
| country-B | binding | final | suf16 | value | 25 | 52% [33,70] | 48% | -2.20 [-3.17,-1.32] | 0.98 | +48 [+28,+68] | needed |
| country-B | binding | final | suf24 | value | 25 | 52% [33,70] | 48% | -2.15 [-3.11,-1.27] | 0.98 | +48 [+28,+68] | needed |
| country-B | binding | final | suf32 | value | 25 | 52% [33,70] | 48% | -2.14 [-3.07,-1.27] | 0.98 | +48 [+28,+68] | needed |
| country-B | binding | final | suf40 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | +0 [+0,+0] | partial |
| country-B | binding | final | win00-07 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win32-39 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-B | binding | final | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| country-B | binding | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| country-B | binding | question | all | value | 25 | 12% [4,30] | 0% | -4.05 [-4.76,-3.36] | 0.93 | +88 [+72,+100] | needed |
| country-B | binding | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | pre24 | value | 25 | 28% [14,48] | 0% | -2.89 [-3.65,-2.17] | 0.93 | +72 [+52,+88] | needed |
| country-B | binding | question | pre32 | value | 25 | 12% [4,30] | 0% | -3.71 [-4.38,-3.06] | 0.92 | +88 [+72,+100] | needed |
| country-B | binding | question | pre40 | value | 25 | 20% [9,39] | 0% | -3.58 [-4.29,-2.86] | 0.93 | +80 [+64,+96] | needed |
| country-B | binding | question | pre48 | value | 25 | 12% [4,30] | 0% | -3.82 [-4.48,-3.18] | 0.93 | +88 [+72,+100] | needed |
| country-B | binding | question | pre56 | value | 25 | 12% [4,30] | 0% | -3.99 [-4.69,-3.32] | 0.93 | +88 [+72,+100] | needed |
| country-B | binding | question | suf08 | value | 25 | 12% [4,30] | 0% | -3.26 [-3.92,-2.64] | 0.93 | +88 [+76,+100] | needed |
| country-B | binding | question | suf16 | value | 25 | 44% [27,63] | 0% | -1.67 [-2.20,-1.16] | 0.93 | +56 [+36,+76] | needed |
| country-B | binding | question | suf24 | value | 25 | 60% [41,77] | 0% | -1.31 [-1.79,-0.84] | 0.93 | +40 [+20,+60] | needed |
| country-B | binding | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.06,-0.03] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.13 [-0.22,-0.06] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.16 [-0.28,-0.06] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.01] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.92 | +0 [+0,+0] | partial |
| country-B | binding | question | win48-55 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | +0 [+0,+0] | partial |
| country-B | binding | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | question | win56-63 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding_off | after | all | absent | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.97 | - | partial |
| country-B | binding_off | after | all | value | 25 | 100% [87,100] | 0% | -0.05 [-0.07,-0.02] | 0.93 | - | partial |
| country-B | binding_off | both | all | absent | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.02] | 0.98 | - | partial |
| country-B | binding_off | both | all | value | 25 | 100% [87,100] | 0% | -0.03 [-0.06,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | pre08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | partial |
| country-B | binding_off | both | pre16 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.02] | 0.94 | - | partial |
| country-B | binding_off | both | pre24 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.04,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | pre32 | value | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | pre40 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.02] | 0.94 | - | partial |
| country-B | binding_off | both | pre48 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.06,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | pre56 | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.02] | 0.94 | - | partial |
| country-B | binding_off | both | suf08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.00] | 0.94 | - | partial |
| country-B | binding_off | both | suf16 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | suf24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | partial |
| country-B | binding_off | both | suf32 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | - | partial |
| country-B | binding_off | both | suf48 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.96 | - | partial |
| country-B | binding_off | both | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| country-B | binding_off | both | win00-07 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | partial |
| country-B | binding_off | both | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | both | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | partial |
| country-B | binding_off | both | win08-15 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | both | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.01] | 0.93 | - | partial |
| country-B | binding_off | both | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.94 | - | partial |
| country-B | binding_off | both | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | both | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.94 | - | partial |
| country-B | binding_off | both | win24-31 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | both | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | both | win32-39 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | win40-47 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.94 | - | partial |
| country-B | binding_off | both | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | - | partial |
| country-B | binding_off | both | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | win48-55:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| country-B | binding_off | both | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| country-B | binding_off | final | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | pre08 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | partial |
| country-B | binding_off | final | pre24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,+0.00] | 0.98 | - | partial |
| country-B | binding_off | final | pre32 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-B | binding_off | final | pre40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | pre48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | pre56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | suf08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | suf16 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | partial |
| country-B | binding_off | final | suf24 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | suf32 | value | 25 | 100% [87,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | partial |
| country-B | binding_off | final | suf40 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| country-B | binding_off | final | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| country-B | binding_off | final | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| country-B | binding_off | final | win00-07 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win00-07:attn | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| country-B | binding_off | final | win00-07:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win08-15 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | partial |
| country-B | binding_off | final | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | final | win08-15:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.01] | 0.97 | - | partial |
| country-B | binding_off | final | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | final | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-B | binding_off | final | win24-31:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | final | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-B | binding_off | final | win32-39 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| country-B | binding_off | final | win32-39:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | final | win32-39:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | partial |
| country-B | binding_off | final | win40-47 | value | 25 | 100% [87,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | final | win40-47:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win48-55 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| country-B | binding_off | final | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | final | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| country-B | binding_off | final | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| country-B | binding_off | final | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | final | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| country-B | binding_off | question | all | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.92 | - | partial |
| country-B | binding_off | question | pre08 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.93 | - | partial |
| country-B | binding_off | question | pre16 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,-0.00] | 0.92 | - | partial |
| country-B | binding_off | question | pre24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | 0.92 | - | partial |
| country-B | binding_off | question | pre32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.92 | - | partial |
| country-B | binding_off | question | pre40 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.03,-0.00] | 0.92 | - | partial |
| country-B | binding_off | question | pre48 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.92 | - | partial |
| country-B | binding_off | question | pre56 | value | 25 | 100% [87,100] | 0% | -0.02 [-0.04,-0.01] | 0.92 | - | partial |
| country-B | binding_off | question | suf08 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.92 | - | partial |
| country-B | binding_off | question | suf16 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.93 | - | partial |
| country-B | binding_off | question | suf24 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | question | suf32 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | partial |
| country-B | binding_off | question | suf40 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | partial |
| country-B | binding_off | question | suf48 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| country-B | binding_off | question | suf56 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | binding_off | question | win00-07 | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | question | win00-07:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | question | win00-07:gdn | value | 25 | 100% [87,100] | 0% | -0.01 [-0.01,-0.00] | 0.93 | - | partial |
| country-B | binding_off | question | win08-15 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.91 | - | partial |
| country-B | binding_off | question | win08-15:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | question | win08-15:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.91 | - | partial |
| country-B | binding_off | question | win16-23 | value | 25 | 100% [87,100] | 0% | +0.01 [+0.01,+0.02] | 0.92 | - | partial |
| country-B | binding_off | question | win16-23:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | question | win16-23:gdn | value | 25 | 100% [87,100] | 0% | +0.01 [+0.00,+0.01] | 0.92 | - | partial |
| country-B | binding_off | question | win24-31 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,+0.00] | 0.91 | - | partial |
| country-B | binding_off | question | win24-31:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| country-B | binding_off | question | win24-31:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.91 | - | partial |
| country-B | binding_off | question | win32-39 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | - | partial |
| country-B | binding_off | question | win32-39:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | question | win32-39:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | - | partial |
| country-B | binding_off | question | win40-47 | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | 0.92 | - | partial |
| country-B | binding_off | question | win40-47:attn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | question | win40-47:gdn | value | 25 | 100% [87,100] | 0% | -0.00 [-0.01,-0.00] | 0.92 | - | partial |
| country-B | binding_off | question | win48-55 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | partial |
| country-B | binding_off | question | win48-55:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | binding_off | question | win48-55:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | partial |
| country-B | binding_off | question | win56-63 | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | binding_off | question | win56-63:attn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | question | win56-63:gdn | value | 25 | 100% [87,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | random | after | all | absent | 25 | 100% [87,100] | 0% | -0.03 [-0.05,-0.01] | 0.98 | - | partial |
| country-B | random | after | all | value | 25 | 100% [87,100] | 0% | -0.04 [-0.07,-0.02] | 0.93 | - | partial |
| country-B | random | both | all | absent | 25 | 100% [87,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | - | partial |
| country-B | random | both | all | value | 25 | 100% [87,100] | 0% | -0.01 [-0.02,+0.01] | 0.96 | - | partial |
| country-B | random | final | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | random | question | all | value | 25 | 100% [87,100] | 0% | +0.00 [-0.01,+0.01] | 0.94 | - | partial |
| country-B | trailing | after | all | absent | 17 | 53% [31,74] | 41% | -1.27 [-1.93,-0.77] | 0.98 | - | breaks (control) |
| country-B | trailing | after | all | value | 17 | 100% [82,100] | 0% | -0.09 [-0.11,-0.06] | 0.95 | - | partial |
| country-B | trailing | both | all | absent | 17 | 100% [82,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | partial |
| country-B | trailing | both | all | value | 17 | 100% [82,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | partial |
| country-B | trailing | final | all | value | 17 | 100% [82,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| country-B | trailing | question | all | value | 17 | 100% [82,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
