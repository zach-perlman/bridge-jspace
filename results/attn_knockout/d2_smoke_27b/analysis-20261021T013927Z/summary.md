# attn_knockout / d2_smoke_27b

Measure: correct (items: {"BL": {"items": 4, "unedited_right": 4}, "BR": {"items": 4, "unedited_right": 4}, "RL": {"items": 4, "unedited_right": 4}, "RR": {"items": 4, "unedited_right": 4}, "BLR": {"items": 4, "unedited_right": 4}, "BRL": {"items": 4, "unedited_right": 4}, "country-R": {"items": 4, "unedited_right": 4}, "country-B": {"items": 4, "unedited_right": 4}})

Claims: {
 "positive_control": {
  "BL": {
   "sources": {
    "lookup": "needed",
    "binding": "partial"
   },
   "passed": false
  },
  "BR": {
   "sources": {
    "binding": "needed"
   },
   "passed": true
  },
  "RL": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
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
  "RL": "needed",
  "RR": "partial",
  "holds": false
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": "needed",
   "question": "partial"
  },
  "RL": {
   "final": "needed",
   "question": "partial"
  },
  "BLR": {
   "final": "needed",
   "question": "partial"
  },
  "BRL": {
   "final": "needed",
   "question": "partial"
  }
 },
 "C1b_holds": true,
 "relay_holds": false,
 "recall_needs_no_locker": {
  "BR": {
   "question": "partial",
   "final": "partial",
   "both": "partial",
   "after": "partial"
  },
  "RR": {
   "question": "partial",
   "final": "partial",
   "both": "partial",
   "after": "partial"
  }
 },
 "binding_BL_vs_BR": {
  "BL": {
   "question": "partial",
   "final": "partial",
   "both": "partial",
   "after": "needed"
  },
  "BR": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  },
  "BLR": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  },
  "BRL": {
   "question": "partial",
   "final": "partial",
   "both": "partial",
   "after": "needed"
  }
 },
 "bands": {
  "BL/lookup/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32",
    "suf40",
    "suf48"
   ],
   "pre_needed": [
    "pre56"
   ],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 48,
   "pre_min_needed": 56
  },
  "BL/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16"
   ],
   "pre_needed": [
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 16,
   "pre_min_needed": 48
  },
  "BR/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 24,
   "pre_min_needed": 32
  },
  "RL/lookup/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32",
    "suf40",
    "suf48"
   ],
   "pre_needed": [
    "pre56"
   ],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 48,
   "pre_min_needed": 56
  },
  "RR/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BLR/lookup/both": {
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
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 48
  },
  "BLR/binding/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": 32
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
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 48,
   "pre_min_needed": 48
  },
  "BRL/binding/both": {
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
  "country-B/binding/both": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16",
    "suf24",
    "suf32"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": 32,
   "pre_min_needed": 32
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BL | binding | after | all | absent | 4 | 50% [15,85] | 50% | -1.29 [-1.72,-1.00] | 0.98 | +50 [+0,+100] | partial |
| BL | binding | after | all | value | 4 | 25% [5,70] | 75% | -1.32 [-1.62,-1.03] | 0.95 | +75 [+25,+100] | needed |
| BL | binding | both | all | absent | 4 | 50% [15,85] | 50% | -1.23 [-1.45,-1.04] | 0.99 | +50 [+0,+100] | partial |
| BL | binding | both | all | value | 4 | 75% [30,95] | 25% | -1.19 [-1.43,-0.98] | 0.98 | +25 [+0,+75] | partial |
| BL | binding | both | attn | value | 4 | 50% [15,85] | 50% | -1.19 [-1.42,-0.96] | - | +50 [+0,+100] | partial |
| BL | binding | both | gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.05,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre32 | value | 4 | 75% [30,95] | 25% | -0.85 [-1.17,-0.53] | 0.98 | +25 [+0,+75] | partial |
| BL | binding | both | pre40 | value | 4 | 75% [30,95] | 25% | -0.92 [-1.16,-0.72] | 0.98 | +25 [+0,+75] | partial |
| BL | binding | both | pre48 | value | 4 | 0% [0,49] | 100% | -1.26 [-1.49,-1.05] | 0.98 | +100 [+100,+100] | needed |
| BL | binding | both | pre56 | value | 4 | 25% [5,70] | 75% | -1.22 [-1.43,-1.01] | 0.98 | +75 [+25,+100] | needed |
| BL | binding | both | suf08 | value | 4 | 25% [5,70] | 75% | -1.17 [-1.30,-1.05] | 0.99 | +75 [+25,+100] | needed |
| BL | binding | both | suf16 | value | 4 | 25% [5,70] | 75% | -0.96 [-1.54,-0.30] | 0.99 | +75 [+25,+100] | needed |
| BL | binding | both | suf24 | value | 4 | 50% [15,85] | 50% | -2.98 [-6.71,-0.29] | 0.99 | +50 [+0,+100] | partial |
| BL | binding | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.22 [-0.48,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.13 [-0.26,-0.01] | - | +0 [+0,+0] | partial |
| BL | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | question | all | value | 4 | 75% [30,95] | 25% | -1.02 [-1.23,-0.87] | 0.98 | +25 [+0,+75] | partial |
| BL | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| BL | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BL | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| BL | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup | after | all | absent | 4 | 0% [0,49] | 25% | -4.77 [-5.99,-3.55] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | after | all | value | 4 | 0% [0,49] | 0% | -4.94 [-6.04,-3.67] | 0.93 | +100 [+100,+100] | needed |
| BL | lookup | both | all | absent | 4 | 0% [0,49] | 75% | -4.20 [-5.27,-3.13] | 0.99 | +100 [+100,+100] | needed |
| BL | lookup | both | all | value | 4 | 0% [0,49] | 75% | -4.34 [-5.41,-3.13] | 0.96 | +100 [+100,+100] | needed |
| BL | lookup | both | attn | value | 4 | 0% [0,49] | 100% | -4.17 [-5.20,-3.12] | - | +100 [+100,+100] | needed |
| BL | lookup | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.49 [-0.92,-0.13] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre56 | value | 4 | 25% [5,70] | 50% | -1.20 [-1.61,-0.78] | 0.96 | +75 [+25,+100] | needed |
| BL | lookup | both | suf08 | value | 4 | 0% [0,49] | 75% | -4.36 [-5.44,-3.28] | 0.96 | +100 [+100,+100] | needed |
| BL | lookup | both | suf16 | value | 4 | 0% [0,49] | 75% | -4.32 [-5.31,-3.33] | 0.96 | +100 [+100,+100] | needed |
| BL | lookup | both | suf24 | value | 4 | 0% [0,49] | 75% | -4.19 [-5.28,-3.10] | 0.96 | +100 [+100,+100] | needed |
| BL | lookup | both | suf32 | value | 4 | 0% [0,49] | 100% | -4.21 [-5.10,-3.28] | 0.97 | +100 [+100,+100] | needed |
| BL | lookup | both | suf40 | value | 4 | 0% [0,49] | 100% | -6.98 [-8.27,-5.69] | 0.97 | +100 [+100,+100] | needed |
| BL | lookup | both | suf48 | value | 4 | 0% [0,49] | 100% | -9.10 [-10.18,-7.44] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| BL | lookup | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| BL | lookup | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.18 [-0.27,-0.08] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.18 [-0.24,-0.07] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BL | lookup | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | all | value | 4 | 0% [0,49] | 75% | -3.63 [-4.33,-2.93] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.93 | - | partial |
| BL | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | lookup_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | random | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | random | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.93 | - | partial |
| BL | random | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | random | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BL | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| BL | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BL | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.03 [-0.05,-0.00] | 0.99 | - | partial |
| BL | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| BL | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BR | binding | after | all | absent | 4 | 25% [5,70] | 50% | -1.60 [-2.17,-0.96] | 0.98 | +75 [+25,+100] | needed |
| BR | binding | after | all | value | 4 | 25% [5,70] | 25% | -1.47 [-2.16,-0.86] | 0.95 | +75 [+25,+100] | needed |
| BR | binding | both | all | absent | 4 | 0% [0,49] | 50% | -2.84 [-3.79,-1.71] | 0.99 | +100 [+100,+100] | needed |
| BR | binding | both | all | value | 4 | 0% [0,49] | 50% | -2.81 [-3.84,-1.67] | 0.98 | +100 [+100,+100] | needed |
| BR | binding | both | attn | value | 4 | 25% [5,70] | 25% | -2.57 [-3.74,-1.36] | - | +75 [+25,+100] | needed |
| BR | binding | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.07,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | pre24 | value | 4 | 75% [30,95] | 25% | -0.47 [-0.86,-0.13] | 0.98 | +25 [+0,+75] | partial |
| BR | binding | both | pre32 | value | 4 | 25% [5,70] | 25% | -1.79 [-2.99,-0.88] | 0.98 | +75 [+25,+100] | needed |
| BR | binding | both | pre40 | value | 4 | 25% [5,70] | 25% | -1.90 [-2.98,-0.95] | 0.98 | +75 [+25,+100] | needed |
| BR | binding | both | pre48 | value | 4 | 25% [5,70] | 25% | -2.43 [-3.64,-1.20] | 0.98 | +75 [+25,+100] | needed |
| BR | binding | both | pre56 | value | 4 | 0% [0,49] | 50% | -2.80 [-3.82,-1.70] | 0.98 | +100 [+100,+100] | needed |
| BR | binding | both | suf08 | value | 4 | 0% [0,49] | 50% | -2.29 [-3.32,-1.25] | 0.98 | +100 [+100,+100] | needed |
| BR | binding | both | suf16 | value | 4 | 25% [5,70] | 75% | -2.19 [-2.86,-1.26] | 0.99 | +75 [+25,+100] | needed |
| BR | binding | both | suf24 | value | 4 | 25% [5,70] | 75% | -3.17 [-5.67,-0.68] | 0.99 | +75 [+25,+100] | needed |
| BR | binding | both | suf32 | value | 4 | 75% [30,95] | 25% | -1.07 [-3.02,-0.02] | 0.98 | +25 [+0,+75] | partial |
| BR | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.20 [-0.41,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.22 [-0.49,-0.01] | - | +0 [+0,+0] | partial |
| BR | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.08 [-0.23,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.10,-0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| BR | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.15 [-0.43,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | question | all | value | 4 | 25% [5,70] | 50% | -2.26 [-3.40,-1.20] | 0.98 | +75 [+25,+100] | needed |
| BR | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | after | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BR | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BR | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BR | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | lookup | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | lookup | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | +0 [+0,+0] | partial |
| BR | lookup | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | lookup | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BR | lookup | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | lookup | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BR | lookup_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| BR | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BR | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BR | random | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| BR | random | both | all | absent | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | random | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BR | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BR | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | - | partial |
| BR | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | random | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | random | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BR | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | partial |
| BR | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BR | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | binding | after | all | absent | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | binding | after | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | binding | both | all | absent | 4 | 75% [30,95] | 25% | -0.30 [-0.65,-0.00] | 0.99 | +25 [+0,+75] | partial |
| RL | binding | both | all | value | 4 | 75% [30,95] | 25% | -0.31 [-0.69,+0.00] | 0.98 | +25 [+0,+75] | partial |
| RL | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | binding | question | all | value | 4 | 100% [51,100] | 0% | -0.08 [-0.17,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | binding_off | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| RL | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | binding_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | binding_off | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup | after | all | absent | 4 | 0% [0,49] | 0% | -4.06 [-4.96,-2.83] | 0.99 | +100 [+100,+100] | needed |
| RL | lookup | after | all | value | 4 | 0% [0,49] | 0% | -3.92 [-4.82,-2.72] | 0.94 | +100 [+100,+100] | needed |
| RL | lookup | both | all | absent | 4 | 0% [0,49] | 0% | -4.14 [-5.08,-2.72] | 0.99 | +100 [+100,+100] | needed |
| RL | lookup | both | all | value | 4 | 0% [0,49] | 25% | -4.18 [-5.11,-2.80] | 0.97 | +100 [+100,+100] | needed |
| RL | lookup | both | attn | value | 4 | 0% [0,49] | 25% | -4.04 [-5.06,-2.67] | - | +100 [+100,+100] | needed |
| RL | lookup | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.50 [-0.96,-0.04] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | pre56 | value | 4 | 0% [0,49] | 25% | -1.60 [-1.97,-1.30] | 0.96 | +100 [+100,+100] | needed |
| RL | lookup | both | suf08 | value | 4 | 0% [0,49] | 25% | -4.17 [-5.09,-2.72] | 0.96 | +100 [+100,+100] | needed |
| RL | lookup | both | suf16 | value | 4 | 0% [0,49] | 25% | -4.36 [-5.52,-2.81] | 0.96 | +100 [+100,+100] | needed |
| RL | lookup | both | suf24 | value | 4 | 0% [0,49] | 25% | -4.29 [-5.12,-2.90] | 0.96 | +100 [+100,+100] | needed |
| RL | lookup | both | suf32 | value | 4 | 0% [0,49] | 25% | -4.77 [-5.95,-3.12] | 0.97 | +100 [+100,+100] | needed |
| RL | lookup | both | suf40 | value | 4 | 0% [0,49] | 50% | -6.73 [-7.52,-6.26] | 0.97 | +100 [+100,+100] | needed |
| RL | lookup | both | suf48 | value | 4 | 0% [0,49] | 100% | -7.49 [-9.15,-6.39] | 0.98 | +100 [+100,+100] | needed |
| RL | lookup | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.06 [-0.12,-0.01] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.06 [-0.11,-0.01] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | all | value | 4 | 0% [0,49] | 25% | -3.38 [-4.09,-2.44] | 0.98 | +100 [+100,+100] | needed |
| RL | lookup | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | partial |
| RL | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RL | lookup_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RL | lookup_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | random | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| RL | random | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | random | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | random | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | random | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.00] | 0.99 | - | partial |
| RL | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RR | binding | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | binding | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | binding | both | all | absent | 4 | 75% [30,95] | 25% | -0.24 [-0.70,-0.00] | 0.99 | +25 [+0,+75] | partial |
| RR | binding | both | all | value | 4 | 75% [30,95] | 25% | -0.34 [-1.01,-0.00] | 0.98 | +25 [+0,+75] | partial |
| RR | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | binding | question | all | value | 4 | 100% [51,100] | 0% | -0.18 [-0.54,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| RR | binding_off | after | all | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | partial |
| RR | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | binding_off | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| RR | binding_off | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | binding_off | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| RR | lookup | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| RR | lookup | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre08 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | both | win00-07 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | lookup | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | lookup | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| RR | lookup | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup_off | after | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | partial |
| RR | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre08 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RR | lookup_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | random | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | random | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | partial |
| RR | random | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| RR | random | both | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | random | both | pre08 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | random | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | random | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RR | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RR | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RR | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | random | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | random | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | partial |
| RR | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RR | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | trailing | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | trailing | question | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BLR | binding | after | all | absent | 4 | 25% [5,70] | 25% | -1.34 [-2.28,-0.63] | 0.98 | +75 [+25,+100] | needed |
| BLR | binding | after | all | value | 4 | 25% [5,70] | 50% | -1.58 [-2.23,-0.99] | 0.95 | +75 [+25,+100] | needed |
| BLR | binding | both | all | absent | 4 | 0% [0,49] | 0% | -1.49 [-1.85,-1.11] | 0.99 | +75 [+25,+100] | needed |
| BLR | binding | both | all | value | 4 | 0% [0,49] | 0% | -1.44 [-1.86,-1.03] | 0.98 | +100 [+100,+100] | needed |
| BLR | binding | both | attn | value | 4 | 0% [0,49] | 0% | -1.44 [-1.74,-1.13] | - | +100 [+100,+100] | needed |
| BLR | binding | both | gdn | value | 4 | 100% [51,100] | 0% | -0.16 [-0.47,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.07,-0.01] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.07,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | pre24 | value | 4 | 75% [30,95] | 0% | -0.66 [-1.30,-0.24] | 0.98 | +25 [+0,+75] | partial |
| BLR | binding | both | pre32 | value | 4 | 0% [0,49] | 0% | -1.41 [-1.75,-1.07] | 0.98 | +75 [+25,+100] | needed |
| BLR | binding | both | pre40 | value | 4 | 0% [0,49] | 0% | -1.40 [-1.80,-1.04] | 0.98 | +100 [+100,+100] | needed |
| BLR | binding | both | pre48 | value | 4 | 0% [0,49] | 0% | -1.48 [-1.85,-1.11] | 0.98 | +75 [+25,+100] | needed |
| BLR | binding | both | pre56 | value | 4 | 0% [0,49] | 0% | -1.50 [-1.89,-1.11] | 0.98 | +100 [+100,+100] | needed |
| BLR | binding | both | suf08 | value | 4 | 50% [15,85] | 25% | -1.04 [-1.56,-0.51] | 0.98 | +50 [+0,+100] | partial |
| BLR | binding | both | suf16 | value | 4 | 75% [30,95] | 0% | -0.49 [-1.14,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.28 [-0.56,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.15 [-0.44,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.12,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.12,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.07,-0.01] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.14,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,-0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.16 [-0.48,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.07 [-0.22,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.12 [-0.38,+0.01] | 0.98 | -25 [-75,+0] | partial |
| BLR | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.09 [-0.31,+0.05] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.16,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.13,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.16,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| BLR | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.08 [-0.25,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | binding | question | all | value | 4 | 0% [0,49] | 0% | -1.45 [-1.78,-1.11] | 0.97 | +75 [+25,+100] | needed |
| BLR | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | +0.04 [-0.00,+0.11] | 0.98 | - | partial |
| BLR | binding_off | after | all | value | 4 | 100% [51,100] | 0% | +0.05 [-0.00,+0.12] | 0.96 | - | partial |
| BLR | binding_off | both | all | absent | 4 | 75% [30,95] | 0% | -0.21 [-0.62,-0.00] | 0.99 | - | breaks (control) |
| BLR | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.16 [-0.46,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | -0.15 [-0.45,+0.00] | - | - | partial |
| BLR | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.01,+0.06] | 0.99 | - | partial |
| BLR | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | 0.98 | - | partial |
| BLR | binding_off | both | pre32 | value | 4 | 75% [30,95] | 0% | -0.20 [-0.59,+0.00] | 0.99 | - | breaks (control) |
| BLR | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.13 [-0.38,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | pre48 | value | 4 | 75% [30,95] | 0% | -0.17 [-0.51,+0.00] | 0.99 | - | breaks (control) |
| BLR | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.16 [-0.46,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.16 [-0.46,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | suf16 | value | 4 | 75% [30,95] | 0% | -0.19 [-0.56,-0.00] | 0.99 | - | breaks (control) |
| BLR | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.15 [-0.44,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.08] | 0.99 | - | partial |
| BLR | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | partial |
| BLR | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | 0.99 | - | partial |
| BLR | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.01] | 0.99 | - | partial |
| BLR | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | - | - | partial |
| BLR | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.01] | 0.98 | - | partial |
| BLR | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | - | - | partial |
| BLR | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | - | partial |
| BLR | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.00] | - | - | partial |
| BLR | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win24-31 | value | 4 | 75% [30,95] | 0% | -0.21 [-0.61,-0.00] | 0.99 | - | breaks (control) |
| BLR | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.15 [-0.44,-0.00] | - | - | partial |
| BLR | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.11,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.01,+0.08] | 0.99 | - | partial |
| BLR | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | - | - | partial |
| BLR | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.09] | 0.99 | - | partial |
| BLR | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | partial |
| BLR | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BLR | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | partial |
| BLR | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BLR | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | binding_off | final | all | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | binding_off | question | all | value | 4 | 75% [30,95] | 0% | -0.27 [-0.80,-0.00] | 0.99 | - | breaks (control) |
| BLR | lookup | after | all | absent | 4 | 25% [5,70] | 25% | -3.29 [-5.10,-1.52] | 0.99 | +75 [+25,+100] | needed |
| BLR | lookup | after | all | value | 4 | 25% [5,70] | 25% | -3.37 [-5.08,-1.58] | 0.94 | +75 [+25,+100] | needed |
| BLR | lookup | both | all | absent | 4 | 25% [5,70] | 25% | -3.02 [-5.11,-1.13] | 0.99 | +75 [+25,+100] | needed |
| BLR | lookup | both | all | value | 4 | 25% [5,70] | 25% | -3.15 [-5.23,-1.18] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | attn | value | 4 | 25% [5,70] | 50% | -2.89 [-4.77,-1.07] | - | +75 [+25,+100] | needed |
| BLR | lookup | both | gdn | value | 4 | 75% [30,95] | 0% | -0.47 [-1.41,+0.00] | 0.97 | +25 [+0,+75] | partial |
| BLR | lookup | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.09,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.15,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | pre32 | value | 4 | 75% [30,95] | 0% | -0.75 [-2.26,-0.00] | 0.97 | +25 [+0,+75] | partial |
| BLR | lookup | both | pre40 | value | 4 | 75% [30,95] | 25% | -1.45 [-4.15,-0.06] | 0.97 | +25 [+0,+75] | partial |
| BLR | lookup | both | pre48 | value | 4 | 25% [5,70] | 25% | -2.68 [-4.23,-1.12] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | pre56 | value | 4 | 25% [5,70] | 25% | -3.13 [-5.18,-1.17] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | suf08 | value | 4 | 25% [5,70] | 25% | -3.10 [-5.12,-1.17] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | suf16 | value | 4 | 25% [5,70] | 50% | -3.12 [-5.08,-1.14] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | suf24 | value | 4 | 25% [5,70] | 50% | -3.10 [-4.88,-1.18] | 0.97 | +75 [+25,+100] | needed |
| BLR | lookup | both | suf32 | value | 4 | 25% [5,70] | 50% | -2.98 [-4.75,-1.11] | 0.98 | +75 [+25,+100] | needed |
| BLR | lookup | both | suf40 | value | 4 | 50% [15,85] | 25% | -1.00 [-1.95,-0.05] | 0.98 | +50 [+0,+100] | partial |
| BLR | lookup | both | suf48 | value | 4 | 75% [30,95] | 25% | -0.33 [-0.66,-0.01] | 0.98 | +25 [+0,+75] | partial |
| BLR | lookup | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.09,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.07,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.11,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.01] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win24-31 | value | 4 | 75% [30,95] | 0% | -0.50 [-1.51,-0.00] | 0.96 | +25 [+0,+75] | partial |
| BLR | lookup | both | win24-31:attn | value | 4 | 75% [30,95] | 0% | -0.29 [-0.86,-0.00] | - | +25 [+0,+75] | partial |
| BLR | lookup | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.08 [-0.23,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BLR | lookup | both | win32-39 | value | 4 | 75% [30,95] | 25% | -1.42 [-4.13,-0.04] | 0.97 | +25 [+0,+75] | partial |
| BLR | lookup | both | win32-39:attn | value | 4 | 75% [30,95] | 25% | -1.38 [-4.04,-0.04] | - | +25 [+0,+75] | partial |
| BLR | lookup | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.12 [-0.35,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win40-47 | value | 4 | 75% [30,95] | 0% | -0.53 [-1.05,-0.03] | 0.97 | +25 [+0,+75] | partial |
| BLR | lookup | both | win40-47:attn | value | 4 | 75% [30,95] | 0% | -0.43 [-0.98,-0.03] | - | +25 [+0,+75] | partial |
| BLR | lookup | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BLR | lookup | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.27 [-0.52,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.16 [-0.32,-0.01] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.10,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BLR | lookup | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | +0 [+0,+0] | partial |
| BLR | lookup | final | all | value | 4 | 25% [5,70] | 50% | -2.85 [-4.77,-0.93] | 0.99 | +75 [+25,+100] | needed |
| BLR | lookup | question | all | value | 4 | 50% [15,85] | 25% | -1.12 [-2.04,-0.19] | 0.97 | +50 [+0,+100] | partial |
| BLR | lookup_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.04 [-0.15,+0.02] | 0.99 | - | partial |
| BLR | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.03] | 0.95 | - | partial |
| BLR | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.15 [-0.50,+0.04] | 0.99 | - | partial |
| BLR | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | -0.08 [-0.27,+0.04] | 0.97 | - | partial |
| BLR | lookup_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| BLR | lookup_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.11 [-0.32,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.13,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.16,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.02] | 0.97 | - | partial |
| BLR | lookup_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.31,+0.03] | 0.97 | - | partial |
| BLR | lookup_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.10 [-0.34,+0.04] | 0.97 | - | partial |
| BLR | lookup_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.30,+0.04] | 0.97 | - | partial |
| BLR | lookup_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.30,+0.04] | 0.97 | - | partial |
| BLR | lookup_off | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.29,+0.04] | 0.97 | - | partial |
| BLR | lookup_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.18,+0.03] | 0.98 | - | partial |
| BLR | lookup_off | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.08 [-0.25,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | partial |
| BLR | lookup_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | - | - | partial |
| BLR | lookup_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.01] | 0.97 | - | partial |
| BLR | lookup_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.01] | - | - | partial |
| BLR | lookup_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.12,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,+0.00] | - | - | partial |
| BLR | lookup_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.05] | 0.97 | - | partial |
| BLR | lookup_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.96 | - | partial |
| BLR | lookup_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.06] | - | - | partial |
| BLR | lookup_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,-0.00] | 0.96 | - | partial |
| BLR | lookup_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.12 [-0.35,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | - | - | partial |
| BLR | lookup_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.07 [-0.19,+0.00] | 0.97 | - | partial |
| BLR | lookup_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | partial |
| BLR | lookup_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | lookup_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BLR | lookup_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | partial |
| BLR | lookup_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BLR | lookup_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.02] | 0.98 | - | partial |
| BLR | lookup_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BLR | lookup_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | lookup_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BLR | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BLR | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | -0.12 [-0.38,+0.03] | 0.97 | - | partial |
| BLR | random | after | all | absent | 4 | 100% [51,100] | 0% | +0.04 [-0.00,+0.12] | 0.99 | - | partial |
| BLR | random | after | all | value | 4 | 100% [51,100] | 0% | +0.04 [-0.01,+0.12] | 0.95 | - | partial |
| BLR | random | both | all | absent | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.05] | 1.00 | - | partial |
| BLR | random | both | all | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.99 | - | partial |
| BLR | random | both | attn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | - | - | partial |
| BLR | random | both | gdn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.99 | - | partial |
| BLR | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | random | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.99 | - | partial |
| BLR | random | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | random | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.04] | 0.99 | - | partial |
| BLR | random | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.05] | 0.99 | - | partial |
| BLR | random | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.99 | - | partial |
| BLR | random | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.99 | - | partial |
| BLR | random | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.01,+0.07] | 0.99 | - | partial |
| BLR | random | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.13,+0.00] | 0.99 | - | partial |
| BLR | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.99 | - | partial |
| BLR | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.99 | - | partial |
| BLR | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.04] | 0.99 | - | partial |
| BLR | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | 0.99 | - | partial |
| BLR | random | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.05,+0.01] | 0.99 | - | partial |
| BLR | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.98 | - | partial |
| BLR | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BLR | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | partial |
| BLR | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.06 [-0.19,+0.01] | 0.99 | - | partial |
| BLR | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.11,+0.00] | - | - | partial |
| BLR | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | partial |
| BLR | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.01,+0.06] | - | - | partial |
| BLR | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | partial |
| BLR | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.05] | 0.99 | - | partial |
| BLR | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | - | - | partial |
| BLR | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.05] | 0.99 | - | partial |
| BLR | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BLR | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| BLR | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BLR | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BLR | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | partial |
| BLR | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BLR | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BLR | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BLR | random | final | all | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.99 | - | partial |
| BLR | random | question | all | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.03] | 0.99 | - | partial |
| BLR | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.15 [-0.25,-0.08] | 0.99 | - | partial |
| BLR | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.12 [-0.30,-0.01] | 0.96 | - | partial |
| BLR | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.07 [-0.23,+0.01] | 0.99 | - | partial |
| BLR | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.10 [-0.29,+0.01] | 0.98 | - | partial |
| BLR | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.01] | 0.99 | - | partial |
| BLR | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.06 [-0.18,+0.01] | 0.98 | - | partial |
| BRL | binding | after | all | absent | 4 | 0% [0,49] | 100% | -2.10 [-2.22,-1.91] | 0.98 | +100 [+100,+100] | needed |
| BRL | binding | after | all | value | 4 | 0% [0,49] | 100% | -2.91 [-4.16,-2.21] | 0.95 | +100 [+100,+100] | needed |
| BRL | binding | both | all | absent | 4 | 50% [15,85] | 50% | -0.93 [-1.07,-0.79] | 0.99 | +50 [+0,+100] | partial |
| BRL | binding | both | all | value | 4 | 50% [15,85] | 50% | -0.91 [-1.03,-0.79] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | attn | value | 4 | 50% [15,85] | 50% | -0.93 [-1.07,-0.80] | - | +50 [+0,+100] | partial |
| BRL | binding | both | gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.20 [-0.44,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | pre24 | value | 4 | 75% [30,95] | 25% | -0.57 [-0.81,-0.30] | 0.98 | +25 [+0,+75] | partial |
| BRL | binding | both | pre32 | value | 4 | 50% [15,85] | 50% | -0.81 [-0.94,-0.67] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | pre40 | value | 4 | 50% [15,85] | 50% | -0.82 [-0.90,-0.75] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | pre48 | value | 4 | 50% [15,85] | 50% | -0.91 [-1.03,-0.78] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | pre56 | value | 4 | 50% [15,85] | 50% | -0.92 [-1.03,-0.80] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | suf08 | value | 4 | 50% [15,85] | 50% | -0.85 [-0.95,-0.74] | 0.98 | +50 [+0,+100] | partial |
| BRL | binding | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.35 [-0.66,-0.17] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf24 | value | 4 | 75% [30,95] | 25% | -1.03 [-1.94,-0.37] | 0.98 | +25 [+0,+75] | partial |
| BRL | binding | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.23 [-0.48,-0.06] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,+0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,-0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.19,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.07 [-0.17,-0.01] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.28 [-0.64,-0.05] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.14 [-0.29,-0.04] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BRL | binding | question | all | value | 4 | 50% [15,85] | 50% | -0.86 [-0.99,-0.76] | 0.97 | +50 [+0,+100] | partial |
| BRL | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.02 [-0.07,+0.03] | 0.98 | - | partial |
| BRL | binding_off | after | all | value | 4 | 100% [51,100] | 0% | -0.08 [-0.18,-0.00] | 0.96 | - | partial |
| BRL | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | - | partial |
| BRL | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| BRL | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | - | partial |
| BRL | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | partial |
| BRL | binding_off | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | partial |
| BRL | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BRL | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| BRL | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.02] | - | - | partial |
| BRL | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | partial |
| BRL | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | - | - | partial |
| BRL | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| BRL | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BRL | binding_off | final | all | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | partial |
| BRL | binding_off | question | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| BRL | lookup | after | all | absent | 4 | 0% [0,49] | 100% | -7.18 [-8.50,-6.37] | 0.98 | +75 [+25,+100] | needed |
| BRL | lookup | after | all | value | 4 | 0% [0,49] | 100% | -7.01 [-7.86,-6.39] | 0.93 | +100 [+100,+100] | needed |
| BRL | lookup | both | all | absent | 4 | 0% [0,49] | 100% | -7.36 [-7.95,-6.63] | 0.99 | +100 [+100,+100] | needed |
| BRL | lookup | both | all | value | 4 | 0% [0,49] | 100% | -7.57 [-8.05,-7.08] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | attn | value | 4 | 0% [0,49] | 100% | -7.57 [-8.03,-7.02] | - | +100 [+100,+100] | needed |
| BRL | lookup | both | gdn | value | 4 | 100% [51,100] | 0% | -0.14 [-0.25,-0.04] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.05,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.22 [-0.39,-0.07] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | pre48 | value | 4 | 0% [0,49] | 75% | -2.76 [-3.68,-2.06] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | pre56 | value | 4 | 0% [0,49] | 100% | -5.48 [-6.52,-4.81] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf08 | value | 4 | 0% [0,49] | 100% | -7.56 [-8.07,-7.03] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf16 | value | 4 | 0% [0,49] | 100% | -7.47 [-7.94,-6.92] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf24 | value | 4 | 0% [0,49] | 100% | -7.27 [-7.74,-6.56] | 0.96 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf32 | value | 4 | 0% [0,49] | 100% | -7.25 [-7.83,-6.45] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf40 | value | 4 | 0% [0,49] | 100% | -7.05 [-7.47,-6.61] | 0.97 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf48 | value | 4 | 0% [0,49] | 100% | -6.29 [-7.43,-5.50] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.16,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.04 [-0.10,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.07 [-0.18,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.07 [-0.18,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.02] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.01] | 0.95 | +0 [+0,+0] | partial |
| BRL | lookup | both | win32-39 | value | 4 | 75% [30,95] | 25% | -0.42 [-1.03,-0.05] | 0.96 | +25 [+0,+75] | partial |
| BRL | lookup | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.24 [-0.54,-0.05] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | both | win40-47 | value | 4 | 25% [5,70] | 75% | -1.26 [-1.57,-0.86] | 0.96 | +75 [+25,+100] | needed |
| BRL | lookup | both | win40-47:attn | value | 4 | 25% [5,70] | 75% | -1.21 [-1.49,-0.75] | - | +75 [+25,+100] | needed |
| BRL | lookup | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.08,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup | both | win48-55 | value | 4 | 25% [5,70] | 75% | -1.09 [-1.43,-0.56] | 0.97 | +75 [+25,+100] | needed |
| BRL | lookup | both | win48-55:attn | value | 4 | 25% [5,70] | 75% | -1.40 [-1.81,-0.84] | - | +75 [+25,+100] | needed |
| BRL | lookup | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BRL | lookup | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.16,-0.02] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.09 [-0.17,-0.02] | - | +0 [+0,+0] | partial |
| BRL | lookup | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BRL | lookup | final | all | value | 4 | 0% [0,49] | 75% | -6.79 [-7.45,-6.17] | 0.98 | +100 [+100,+100] | needed |
| BRL | lookup | question | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BRL | lookup_off | after | all | absent | 4 | 75% [30,95] | 0% | -0.32 [-0.99,+0.04] | 0.98 | - | breaks (control) |
| BRL | lookup_off | after | all | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.93 | - | partial |
| BRL | lookup_off | both | all | absent | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.99 | - | partial |
| BRL | lookup_off | both | all | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | - | - | partial |
| BRL | lookup_off | both | gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.08,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.07 [-0.17,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.97 | - | partial |
| BRL | lookup_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | partial |
| BRL | lookup_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | lookup_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.97 | - | partial |
| BRL | lookup_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | lookup_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| BRL | lookup_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.07,+0.00] | 0.97 | - | partial |
| BRL | lookup_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.95 | - | partial |
| BRL | lookup_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | - | partial |
| BRL | lookup_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | partial |
| BRL | lookup_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.96 | - | partial |
| BRL | lookup_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | - | - | partial |
| BRL | lookup_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.96 | - | partial |
| BRL | lookup_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.03] | 0.97 | - | partial |
| BRL | lookup_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.04] | - | - | partial |
| BRL | lookup_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | 0.97 | - | partial |
| BRL | lookup_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.04] | 0.98 | - | partial |
| BRL | lookup_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.04] | - | - | partial |
| BRL | lookup_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BRL | lookup_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | partial |
| BRL | lookup_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| BRL | lookup_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | lookup_off | final | all | value | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.03] | 0.98 | - | partial |
| BRL | lookup_off | question | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.96 | - | partial |
| BRL | random | after | all | absent | 4 | 100% [51,100] | 0% | +0.01 [-0.03,+0.07] | 0.99 | - | partial |
| BRL | random | after | all | value | 4 | 100% [51,100] | 0% | -0.03 [-0.18,+0.07] | 0.94 | - | partial |
| BRL | random | both | all | absent | 4 | 100% [51,100] | 0% | +0.02 [-0.03,+0.07] | 1.00 | - | partial |
| BRL | random | both | all | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.06] | 0.98 | - | partial |
| BRL | random | both | attn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.01,+0.07] | - | - | partial |
| BRL | random | both | gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BRL | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | random | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BRL | random | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.98 | - | partial |
| BRL | random | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.10,-0.00] | 0.98 | - | partial |
| BRL | random | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.07,+0.00] | 0.98 | - | partial |
| BRL | random | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | 0.98 | - | partial |
| BRL | random | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.98 | - | partial |
| BRL | random | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.06] | 0.98 | - | partial |
| BRL | random | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.98 | - | partial |
| BRL | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.07] | 0.98 | - | partial |
| BRL | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.08] | 0.98 | - | partial |
| BRL | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.08] | 0.98 | - | partial |
| BRL | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.03 [-0.00,+0.07] | 0.98 | - | partial |
| BRL | random | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | partial |
| BRL | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.00] | 0.98 | - | partial |
| BRL | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| BRL | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | 0.98 | - | partial |
| BRL | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.00] | 0.98 | - | partial |
| BRL | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| BRL | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | partial |
| BRL | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.11 [-0.31,+0.00] | 0.97 | - | partial |
| BRL | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.05 [-0.13,+0.00] | - | - | partial |
| BRL | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BRL | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | - | partial |
| BRL | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | - | - | partial |
| BRL | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | partial |
| BRL | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | partial |
| BRL | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | - | - | partial |
| BRL | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | partial |
| BRL | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | 0.98 | - | partial |
| BRL | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.07] | - | - | partial |
| BRL | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | partial |
| BRL | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | partial |
| BRL | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| BRL | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | partial |
| BRL | random | final | all | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.06] | 0.99 | - | partial |
| BRL | random | question | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,+0.00] | 0.97 | - | partial |
| BRL | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.99 | - | partial |
| BRL | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.04,+0.02] | 0.96 | - | partial |
| BRL | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.01] | 0.99 | - | partial |
| BRL | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | - | partial |
| BRL | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,-0.00] | 0.99 | - | partial |
| BRL | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | partial |
| country-R | binding | after | all | absent | 4 | 100% [51,100] | 0% | -0.00 [-0.06,+0.05] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | after | all | value | 4 | 100% [51,100] | 0% | -0.03 [-0.11,+0.03] | 0.93 | -25 [-75,+0] | partial |
| country-R | binding | both | all | absent | 4 | 100% [51,100] | 0% | -0.04 [-0.08,+0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | both | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.06,+0.06] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | both | gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.03,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.03 [+0.00,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.04] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.08,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.04,+0.04] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.06,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.03,+0.07] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.02] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.11,+0.02] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.08,+0.03] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.03,+0.03] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.07,+0.01] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.03,+0.03] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.03 [+0.02,+0.06] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.01,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.04 [+0.02,+0.07] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.03 [+0.02,+0.05] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,-0.00] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.03,+0.03] | 0.97 | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.02,+0.03] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.04] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.03] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.01] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | - | +0 [+0,+0] | partial |
| country-R | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | final | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.05,+0.01] | 0.98 | +0 [+0,+0] | partial |
| country-R | binding | question | all | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.06] | 0.95 | +0 [+0,+0] | partial |
| country-R | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.03 [-0.14,+0.05] | 0.97 | - | partial |
| country-R | binding_off | after | all | value | 4 | 75% [30,95] | 0% | -0.11 [-0.30,+0.01] | 0.93 | - | breaks (control) |
| country-R | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | +0.00 [-0.02,+0.02] | 0.98 | - | partial |
| country-R | binding_off | both | all | value | 4 | 100% [51,100] | 0% | +0.07 [+0.02,+0.12] | 0.96 | - | partial |
| country-R | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | +0.04 [+0.02,+0.05] | - | - | partial |
| country-R | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | +0.05 [+0.01,+0.09] | 0.96 | - | partial |
| country-R | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.03,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.04 [+0.02,+0.06] | 0.95 | - | partial |
| country-R | binding_off | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.07 [+0.02,+0.11] | 0.95 | - | partial |
| country-R | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.06 [+0.02,+0.10] | 0.95 | - | partial |
| country-R | binding_off | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.08 [+0.04,+0.12] | 0.95 | - | partial |
| country-R | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.07 [+0.02,+0.13] | 0.95 | - | partial |
| country-R | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.07 [+0.03,+0.11] | 0.96 | - | partial |
| country-R | binding_off | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.06 [+0.03,+0.09] | 0.96 | - | partial |
| country-R | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.05 [+0.03,+0.09] | 0.96 | - | partial |
| country-R | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.04 [+0.02,+0.06] | 0.96 | - | partial |
| country-R | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.03 [+0.01,+0.04] | 0.96 | - | partial |
| country-R | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.01,+0.05] | 0.96 | - | partial |
| country-R | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | partial |
| country-R | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.03,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-R | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | +0.03 [+0.02,+0.03] | 0.94 | - | partial |
| country-R | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | - | - | partial |
| country-R | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.94 | - | partial |
| country-R | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.04 [+0.02,+0.06] | 0.96 | - | partial |
| country-R | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | - | - | partial |
| country-R | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.03 [+0.01,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.95 | - | partial |
| country-R | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | - | - | partial |
| country-R | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.03] | 0.95 | - | partial |
| country-R | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | 0.96 | - | partial |
| country-R | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-R | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.04] | 0.96 | - | partial |
| country-R | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.01,+0.02] | 0.95 | - | partial |
| country-R | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | - | - | partial |
| country-R | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.00,+0.03] | 0.95 | - | partial |
| country-R | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.95 | - | partial |
| country-R | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.01] | - | - | partial |
| country-R | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.03] | 0.95 | - | partial |
| country-R | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | partial |
| country-R | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.02,+0.02] | - | - | partial |
| country-R | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | partial |
| country-R | binding_off | final | all | value | 4 | 100% [51,100] | 0% | +0.03 [+0.00,+0.06] | 0.98 | - | partial |
| country-R | binding_off | question | all | value | 4 | 100% [51,100] | 0% | +0.07 [+0.03,+0.12] | 0.94 | - | partial |
| country-R | random | after | all | absent | 4 | 100% [51,100] | 0% | -0.10 [-0.14,-0.07] | 0.98 | - | partial |
| country-R | random | after | all | value | 4 | 75% [30,95] | 0% | -0.20 [-0.34,-0.11] | 0.93 | - | breaks (control) |
| country-R | random | both | all | absent | 4 | 100% [51,100] | 0% | -0.09 [-0.14,-0.05] | 0.98 | - | partial |
| country-R | random | both | all | value | 4 | 75% [30,95] | 0% | -0.18 [-0.34,-0.06] | 0.94 | - | breaks (control) |
| country-R | random | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.03,+0.01] | - | - | partial |
| country-R | random | both | gdn | value | 4 | 75% [30,95] | 0% | -0.17 [-0.34,-0.05] | 0.94 | - | breaks (control) |
| country-R | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,-0.01] | 0.95 | - | partial |
| country-R | random | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.11 [-0.21,-0.04] | 0.94 | - | partial |
| country-R | random | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.14 [-0.29,-0.03] | 0.94 | - | partial |
| country-R | random | both | pre32 | value | 4 | 75% [30,95] | 0% | -0.18 [-0.34,-0.07] | 0.94 | - | breaks (control) |
| country-R | random | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.14 [-0.29,-0.04] | 0.94 | - | partial |
| country-R | random | both | pre48 | value | 4 | 75% [30,95] | 0% | -0.15 [-0.33,-0.04] | 0.94 | - | breaks (control) |
| country-R | random | both | pre56 | value | 4 | 75% [30,95] | 0% | -0.15 [-0.33,-0.04] | 0.94 | - | breaks (control) |
| country-R | random | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.08 [-0.17,-0.03] | 0.94 | - | partial |
| country-R | random | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | - | partial |
| country-R | random | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.05,+0.00] | 0.95 | - | partial |
| country-R | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.02,+0.02] | 0.95 | - | partial |
| country-R | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| country-R | random | both | suf48 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.03] | 0.96 | - | partial |
| country-R | random | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.05] | 0.97 | - | partial |
| country-R | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,-0.01] | 0.95 | - | partial |
| country-R | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.01,+0.03] | - | - | partial |
| country-R | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.07,+0.00] | 0.95 | - | partial |
| country-R | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.01] | 0.93 | - | partial |
| country-R | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-R | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.02] | 0.93 | - | partial |
| country-R | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.04] | 0.94 | - | partial |
| country-R | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| country-R | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.03 [+0.01,+0.04] | 0.94 | - | partial |
| country-R | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.93 | - | partial |
| country-R | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | - | partial |
| country-R | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.93 | - | partial |
| country-R | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | - | partial |
| country-R | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | - | - | partial |
| country-R | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.94 | - | partial |
| country-R | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.94 | - | partial |
| country-R | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-R | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.94 | - | partial |
| country-R | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.01] | 0.95 | - | partial |
| country-R | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.02] | - | - | partial |
| country-R | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.02] | 0.95 | - | partial |
| country-R | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.97 | - | partial |
| country-R | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| country-R | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | partial |
| country-R | random | final | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.01] | 0.98 | - | partial |
| country-R | random | question | all | value | 4 | 100% [51,100] | 0% | -0.07 [-0.15,-0.02] | 0.92 | - | partial |
| country-R | trailing | after | all | absent | 4 | 100% [51,100] | 0% | -0.10 [-0.17,-0.04] | 0.99 | - | partial |
| country-R | trailing | after | all | value | 4 | 100% [51,100] | 0% | -0.15 [-0.27,-0.04] | 0.95 | - | partial |
| country-R | trailing | both | all | absent | 4 | 100% [51,100] | 0% | -0.05 [-0.09,-0.00] | 0.99 | - | partial |
| country-R | trailing | both | all | value | 4 | 100% [51,100] | 0% | -0.05 [-0.11,-0.01] | 0.97 | - | partial |
| country-R | trailing | final | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.00] | 0.99 | - | partial |
| country-R | trailing | question | all | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.01] | 0.97 | - | partial |
| country-B | binding | after | all | absent | 4 | 0% [0,49] | 0% | -8.49 [-10.44,-6.55] | 0.97 | +100 [+100,+100] | needed |
| country-B | binding | after | all | value | 4 | 0% [0,49] | 0% | -8.20 [-10.01,-6.39] | 0.93 | +100 [+100,+100] | needed |
| country-B | binding | both | all | absent | 4 | 0% [0,49] | 0% | -8.24 [-10.20,-6.28] | 0.98 | +100 [+100,+100] | needed |
| country-B | binding | both | all | value | 4 | 0% [0,49] | 0% | -8.04 [-10.00,-6.09] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | attn | value | 4 | 0% [0,49] | 0% | -5.76 [-7.82,-4.31] | - | +100 [+100,+100] | needed |
| country-B | binding | both | gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.04 [-0.07,-0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | pre24 | value | 4 | 50% [15,85] | 0% | -2.98 [-5.39,-0.81] | 0.95 | +50 [+0,+100] | partial |
| country-B | binding | both | pre32 | value | 4 | 0% [0,49] | 0% | -3.99 [-6.21,-2.21] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | pre40 | value | 4 | 0% [0,49] | 0% | -3.96 [-6.16,-2.18] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | pre48 | value | 4 | 0% [0,49] | 0% | -4.23 [-5.91,-2.95] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | pre56 | value | 4 | 0% [0,49] | 0% | -6.38 [-8.02,-4.85] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf08 | value | 4 | 0% [0,49] | 0% | -8.00 [-9.94,-6.05] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf16 | value | 4 | 0% [0,49] | 0% | -7.17 [-8.94,-5.41] | 0.95 | +100 [+100,+100] | needed |
| country-B | binding | both | suf24 | value | 4 | 0% [0,49] | 25% | -7.15 [-8.97,-5.34] | 0.96 | +100 [+100,+100] | needed |
| country-B | binding | both | suf32 | value | 4 | 0% [0,49] | 75% | -8.69 [-10.45,-6.20] | 0.96 | +100 [+100,+100] | needed |
| country-B | binding | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.04,+0.01] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | suf56 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.13 [-0.32,-0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.05 [-0.08,-0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.94 | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.06 [-0.11,-0.01] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.06,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.01,+0.00] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | 0.95 | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | +0 [+0,+0] | partial |
| country-B | binding | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| country-B | binding | final | all | value | 4 | 25% [5,70] | 75% | -3.21 [-4.68,-1.13] | 0.98 | +75 [+25,+100] | needed |
| country-B | binding | question | all | value | 4 | 0% [0,49] | 0% | -4.41 [-6.65,-2.72] | 0.94 | +100 [+100,+100] | needed |
| country-B | binding_off | after | all | absent | 4 | 100% [51,100] | 0% | -0.06 [-0.09,-0.01] | 0.97 | - | partial |
| country-B | binding_off | after | all | value | 4 | 100% [51,100] | 0% | -0.09 [-0.13,-0.04] | 0.93 | - | partial |
| country-B | binding_off | both | all | absent | 4 | 100% [51,100] | 0% | -0.06 [-0.09,-0.02] | 0.98 | - | partial |
| country-B | binding_off | both | all | value | 4 | 100% [51,100] | 0% | -0.08 [-0.13,-0.03] | 0.94 | - | partial |
| country-B | binding_off | both | attn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.00] | - | - | partial |
| country-B | binding_off | both | gdn | value | 4 | 100% [51,100] | 0% | -0.10 [-0.17,-0.03] | 0.94 | - | partial |
| country-B | binding_off | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | pre16 | value | 4 | 100% [51,100] | 0% | -0.07 [-0.10,-0.03] | 0.93 | - | partial |
| country-B | binding_off | both | pre24 | value | 4 | 100% [51,100] | 0% | -0.08 [-0.12,-0.03] | 0.93 | - | partial |
| country-B | binding_off | both | pre32 | value | 4 | 100% [51,100] | 0% | -0.10 [-0.15,-0.04] | 0.93 | - | partial |
| country-B | binding_off | both | pre40 | value | 4 | 100% [51,100] | 0% | -0.10 [-0.14,-0.03] | 0.93 | - | partial |
| country-B | binding_off | both | pre48 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.12,-0.03] | 0.93 | - | partial |
| country-B | binding_off | both | pre56 | value | 4 | 100% [51,100] | 0% | -0.09 [-0.13,-0.03] | 0.93 | - | partial |
| country-B | binding_off | both | suf08 | value | 4 | 100% [51,100] | 0% | -0.03 [-0.06,-0.00] | 0.93 | - | partial |
| country-B | binding_off | both | suf16 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | - | partial |
| country-B | binding_off | both | suf24 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.00] | 0.94 | - | partial |
| country-B | binding_off | both | suf32 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.01] | 0.95 | - | partial |
| country-B | binding_off | both | suf40 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-B | binding_off | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.96 | - | partial |
| country-B | binding_off | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | - | partial |
| country-B | binding_off | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.04,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.01] | 0.94 | - | partial |
| country-B | binding_off | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.01] | 0.92 | - | partial |
| country-B | binding_off | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.01] | - | - | partial |
| country-B | binding_off | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | -0.02 [-0.03,-0.01] | 0.92 | - | partial |
| country-B | binding_off | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.93 | - | partial |
| country-B | binding_off | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.01,+0.02] | 0.93 | - | partial |
| country-B | binding_off | both | win24-31 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,-0.01] | 0.92 | - | partial |
| country-B | binding_off | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| country-B | binding_off | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,-0.00] | 0.92 | - | partial |
| country-B | binding_off | both | win32-39 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | - | partial |
| country-B | binding_off | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | - | partial |
| country-B | binding_off | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.93 | - | partial |
| country-B | binding_off | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | - | partial |
| country-B | binding_off | both | win48-55 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| country-B | binding_off | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | binding_off | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | partial |
| country-B | binding_off | both | win56-63 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.00] | 0.97 | - | partial |
| country-B | binding_off | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| country-B | binding_off | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| country-B | binding_off | final | all | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | partial |
| country-B | binding_off | question | all | value | 4 | 100% [51,100] | 0% | -0.06 [-0.09,-0.03] | 0.91 | - | partial |
| country-B | random | after | all | absent | 4 | 100% [51,100] | 0% | +0.01 [-0.02,+0.05] | 0.97 | - | partial |
| country-B | random | after | all | value | 4 | 100% [51,100] | 0% | -0.01 [-0.03,+0.02] | 0.93 | - | partial |
| country-B | random | both | all | absent | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.02] | 0.98 | - | partial |
| country-B | random | both | all | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| country-B | random | both | gdn | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.03] | 0.96 | - | partial |
| country-B | random | both | pre08 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.96 | - | partial |
| country-B | random | both | pre16 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.96 | - | partial |
| country-B | random | both | pre24 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | pre32 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | 0.96 | - | partial |
| country-B | random | both | pre40 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.02] | 0.96 | - | partial |
| country-B | random | both | pre48 | value | 4 | 100% [51,100] | 0% | +0.02 [-0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | pre56 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | suf08 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | suf16 | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.04] | 0.96 | - | partial |
| country-B | random | both | suf24 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.96 | - | partial |
| country-B | random | both | suf32 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.01,+0.02] | 0.97 | - | partial |
| country-B | random | both | suf40 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.96 | - | partial |
| country-B | random | both | suf48 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | - | partial |
| country-B | random | both | suf56 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | partial |
| country-B | random | both | win00-07 | value | 4 | 100% [51,100] | 0% | -0.00 [-0.02,+0.01] | 0.96 | - | partial |
| country-B | random | both | win00-07:attn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.02] | - | - | partial |
| country-B | random | both | win00-07:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | - | partial |
| country-B | random | both | win08-15 | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.00] | 0.95 | - | partial |
| country-B | random | both | win08-15:attn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.01] | - | - | partial |
| country-B | random | both | win08-15:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.02] | 0.95 | - | partial |
| country-B | random | both | win16-23 | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.03] | 0.96 | - | partial |
| country-B | random | both | win16-23:attn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.01] | - | - | partial |
| country-B | random | both | win16-23:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [-0.00,+0.02] | 0.96 | - | partial |
| country-B | random | both | win24-31 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.95 | - | partial |
| country-B | random | both | win24-31:attn | value | 4 | 100% [51,100] | 0% | -0.01 [-0.02,+0.01] | - | - | partial |
| country-B | random | both | win24-31:gdn | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.95 | - | partial |
| country-B | random | both | win32-39 | value | 4 | 100% [51,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | partial |
| country-B | random | both | win32-39:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| country-B | random | both | win32-39:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.01,+0.02] | 0.97 | - | partial |
| country-B | random | both | win40-47 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | random | both | win40-47:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | random | both | win40-47:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | random | both | win48-55 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| country-B | random | both | win48-55:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| country-B | random | both | win48-55:gdn | value | 4 | 100% [51,100] | 0% | +0.00 [+0.00,+0.01] | 0.96 | - | partial |
| country-B | random | both | win56-63 | value | 4 | 100% [51,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| country-B | random | both | win56-63:attn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.01,-0.00] | - | - | partial |
| country-B | random | both | win56-63:gdn | value | 4 | 100% [51,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| country-B | random | final | all | value | 4 | 100% [51,100] | 0% | +0.02 [+0.01,+0.02] | 0.98 | - | partial |
| country-B | random | question | all | value | 4 | 100% [51,100] | 0% | +0.01 [-0.01,+0.04] | 0.95 | - | partial |
| country-B | trailing | after | all | absent | 3 | 33% [6,79] | 67% | -2.42 [-5.14,-0.56] | 0.98 | - | breaks (control) |
| country-B | trailing | after | all | value | 3 | 100% [44,100] | 0% | -0.13 [-0.16,-0.11] | 0.95 | - | partial |
| country-B | trailing | both | all | absent | 3 | 100% [44,100] | 0% | -0.01 [-0.02,+0.01] | 0.99 | - | partial |
| country-B | trailing | both | all | value | 3 | 100% [44,100] | 0% | +0.00 [-0.01,+0.02] | 0.97 | - | partial |
| country-B | trailing | final | all | value | 3 | 100% [44,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | - | partial |
| country-B | trailing | question | all | value | 3 | 100% [44,100] | 0% | -0.01 [-0.02,-0.00] | 0.96 | - | partial |
