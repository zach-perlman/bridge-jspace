# attn_knockout / d2_ko_sweep_v1

Measure: correct (items: {"BL": {"items": 30, "unedited_right": 30}, "BR": {"items": 30, "unedited_right": 30}, "RL": {"items": 30, "unedited_right": 30}, "RR": {"items": 30, "unedited_right": 30}})

Claims: {
 "positive_control": {
  "BL": {
   "sources": {
    "lookup": "needed",
    "binding": "needed"
   },
   "passed": true
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
   "final": null,
   "question": null
  },
  "BRL": {
   "final": null,
   "question": null
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
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  },
  "BR": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
  },
  "BLR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BRL": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  }
 },
 "bands": {
  "BL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/lookup/final": {
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
   "suf_max_needed": 48,
   "pre_min_needed": 56
  },
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
   "suf_max_needed": 48,
   "pre_min_needed": 56
  },
  "BL/binding/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf24"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 24,
   "pre_min_needed": 32
  },
  "BL/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/binding/both": {
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
   "suf_max_needed": 24,
   "pre_min_needed": 32
  },
  "BR/binding/question": {
   "windows_needed": [],
   "suf_needed": [
    "suf08",
    "suf16"
   ],
   "pre_needed": [
    "pre32",
    "pre40",
    "pre48",
    "pre56"
   ],
   "suf_max_needed": 16,
   "pre_min_needed": 32
  },
  "BR/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BR/binding/both": {
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
   "suf_max_needed": 32,
   "pre_min_needed": 32
  },
  "RL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/final": {
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
   "suf_max_needed": 48,
   "pre_min_needed": 56
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
   "suf_max_needed": 48,
   "pre_min_needed": 56
  },
  "RR/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BL | binding | after | all | absent | 30 | 43% [27,61] | 57% | -1.23 [-1.40,-1.05] | 0.98 | +57 [+40,+73] | needed |
| BL | binding | after | all | value | 30 | 33% [19,51] | 67% | -1.30 [-1.45,-1.14] | 0.95 | +67 [+50,+83] | needed |
| BL | binding | both | all | absent | 30 | 47% [30,64] | 50% | -1.39 [-1.58,-1.21] | 0.99 | +53 [+37,+70] | needed |
| BL | binding | both | all | value | 30 | 47% [30,64] | 50% | -1.38 [-1.56,-1.21] | 0.98 | +53 [+33,+70] | needed |
| BL | binding | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.02 [-0.03,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | pre24 | value | 30 | 97% [83,99] | 3% | -0.18 [-0.27,-0.10] | 0.98 | +3 [+0,+10] | partial |
| BL | binding | both | pre32 | value | 30 | 70% [52,83] | 30% | -1.01 [-1.15,-0.85] | 0.98 | +30 [+17,+47] | needed |
| BL | binding | both | pre40 | value | 30 | 67% [49,81] | 33% | -1.04 [-1.18,-0.89] | 0.98 | +33 [+17,+50] | needed |
| BL | binding | both | pre48 | value | 30 | 43% [27,61] | 53% | -1.36 [-1.54,-1.20] | 0.98 | +57 [+37,+73] | needed |
| BL | binding | both | pre56 | value | 30 | 47% [30,64] | 50% | -1.37 [-1.55,-1.20] | 0.98 | +53 [+37,+70] | needed |
| BL | binding | both | suf08 | value | 30 | 43% [27,61] | 57% | -1.36 [-1.55,-1.16] | 0.99 | +57 [+40,+73] | needed |
| BL | binding | both | suf16 | value | 30 | 50% [33,67] | 50% | -0.95 [-1.20,-0.69] | 0.99 | +50 [+33,+67] | needed |
| BL | binding | both | suf24 | value | 30 | 43% [27,61] | 57% | -1.40 [-2.09,-0.81] | 0.99 | +57 [+40,+73] | needed |
| BL | binding | both | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.02 [-0.03,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win24-31 | value | 30 | 97% [83,99] | 3% | -0.16 [-0.32,-0.06] | 0.99 | +3 [+0,+10] | partial |
| BL | binding | both | win28-35 | value | 30 | 97% [83,99] | 3% | -0.05 [-0.12,-0.01] | 0.99 | +3 [+0,+10] | partial |
| BL | binding | both | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | both | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | both | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | final | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | final | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | question | all | value | 30 | 63% [46,78] | 37% | -1.13 [-1.25,-1.00] | 0.98 | +37 [+20,+53] | needed |
| BL | binding | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.02 [-0.02,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | pre24 | value | 30 | 97% [83,99] | 3% | -0.19 [-0.28,-0.10] | 0.98 | +3 [+0,+10] | partial |
| BL | binding | question | pre32 | value | 30 | 67% [49,81] | 33% | -0.99 [-1.12,-0.84] | 0.98 | +33 [+17,+50] | needed |
| BL | binding | question | pre40 | value | 30 | 70% [52,83] | 30% | -1.00 [-1.14,-0.86] | 0.98 | +30 [+17,+47] | needed |
| BL | binding | question | pre48 | value | 30 | 63% [46,78] | 37% | -1.14 [-1.26,-1.02] | 0.98 | +37 [+20,+53] | needed |
| BL | binding | question | pre56 | value | 30 | 63% [46,78] | 37% | -1.14 [-1.26,-1.01] | 0.98 | +37 [+20,+53] | needed |
| BL | binding | question | suf08 | value | 30 | 70% [52,83] | 30% | -1.08 [-1.22,-0.94] | 0.98 | +30 [+17,+47] | needed |
| BL | binding | question | suf16 | value | 30 | 77% [59,88] | 23% | -0.75 [-0.95,-0.55] | 0.98 | +23 [+10,+40] | partial |
| BL | binding | question | suf24 | value | 30 | 63% [46,78] | 37% | -1.24 [-1.97,-0.64] | 0.98 | +37 [+20,+53] | needed |
| BL | binding | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.02 [-0.03,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | question | win24-31 | value | 30 | 97% [83,99] | 3% | -0.16 [-0.32,-0.06] | 0.98 | +3 [+0,+10] | partial |
| BL | binding | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.04 [-0.09,-0.01] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | question | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding | question | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | binding | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | binding_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | partial |
| BL | binding_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | both | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | both | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | binding_off | question | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | binding_off | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | binding_off | question | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | binding_off | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup | after | all | absent | 30 | 0% [-0,11] | 50% | -3.97 [-4.58,-3.42] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | after | all | value | 30 | 0% [-0,11] | 43% | -3.97 [-4.62,-3.38] | 0.93 | +100 [+100,+100] | needed |
| BL | lookup | both | all | absent | 30 | 0% [-0,11] | 90% | -4.41 [-4.90,-3.92] | 0.99 | +100 [+100,+100] | needed |
| BL | lookup | both | all | value | 30 | 3% [1,17] | 90% | -4.55 [-5.09,-4.01] | 0.97 | +97 [+90,+100] | needed |
| BL | lookup | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | pre48 | value | 30 | 90% [74,97] | 10% | -0.41 [-0.60,-0.26] | 0.96 | +10 [+0,+20] | partial |
| BL | lookup | both | pre56 | value | 30 | 53% [36,70] | 43% | -1.24 [-1.58,-0.93] | 0.96 | +47 [+27,+63] | needed |
| BL | lookup | both | suf08 | value | 30 | 3% [1,17] | 90% | -4.55 [-5.09,-4.01] | 0.96 | +97 [+90,+100] | needed |
| BL | lookup | both | suf16 | value | 30 | 0% [-0,11] | 87% | -4.61 [-5.17,-4.06] | 0.96 | +100 [+100,+100] | needed |
| BL | lookup | both | suf24 | value | 30 | 0% [-0,11] | 90% | -4.55 [-5.09,-3.99] | 0.97 | +100 [+100,+100] | needed |
| BL | lookup | both | suf32 | value | 30 | 0% [-0,11] | 100% | -4.58 [-5.17,-3.98] | 0.97 | +100 [+100,+100] | needed |
| BL | lookup | both | suf40 | value | 30 | 7% [2,21] | 77% | -6.28 [-7.26,-5.38] | 0.97 | +93 [+83,+100] | needed |
| BL | lookup | both | suf48 | value | 30 | 3% [1,17] | 97% | -8.35 [-9.07,-7.53] | 0.98 | +97 [+90,+100] | needed |
| BL | lookup | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | both | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | both | win44-51 | value | 30 | 97% [83,99] | 3% | -0.03 [-0.09,-0.00] | 0.97 | +3 [+0,+10] | partial |
| BL | lookup | both | win48-55 | value | 30 | 80% [63,90] | 20% | -0.50 [-0.79,-0.24] | 0.97 | +20 [+7,+33] | partial |
| BL | lookup | both | win52-59 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | all | value | 30 | 3% [1,17] | 83% | -3.96 [-4.48,-3.47] | 0.98 | +97 [+90,+100] | needed |
| BL | lookup | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | pre48 | value | 30 | 93% [79,98] | 7% | -0.21 [-0.30,-0.12] | 0.98 | +7 [+0,+17] | partial |
| BL | lookup | final | pre56 | value | 30 | 53% [36,70] | 47% | -1.20 [-1.56,-0.88] | 0.98 | +47 [+30,+63] | needed |
| BL | lookup | final | suf08 | value | 30 | 3% [1,17] | 83% | -3.96 [-4.49,-3.47] | 0.98 | +97 [+90,+100] | needed |
| BL | lookup | final | suf16 | value | 30 | 0% [-0,11] | 87% | -3.99 [-4.51,-3.49] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | final | suf24 | value | 30 | 0% [-0,11] | 87% | -4.09 [-4.65,-3.54] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | final | suf32 | value | 30 | 0% [-0,11] | 93% | -4.03 [-4.57,-3.50] | 0.98 | +100 [+100,+100] | needed |
| BL | lookup | final | suf40 | value | 30 | 7% [2,21] | 73% | -4.70 [-5.48,-3.98] | 0.99 | +93 [+83,+100] | needed |
| BL | lookup | final | suf48 | value | 30 | 7% [2,21] | 93% | -5.52 [-6.23,-4.73] | 0.99 | +93 [+83,+100] | needed |
| BL | lookup | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.03 [-0.08,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | final | win48-55 | value | 30 | 90% [74,97] | 10% | -0.33 [-0.57,-0.14] | 0.98 | +10 [+0,+23] | partial |
| BL | lookup | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BL | lookup | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | pre16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | pre24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| BL | lookup | question | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| BL | lookup | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | +0 [+0,+0] | partial |
| BL | lookup | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| BL | lookup | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| BL | lookup | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup | question | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BL | lookup_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.93 | - | partial |
| BL | lookup_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | both | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | both | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | both | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | both | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | both | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | both | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | lookup_off | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BL | lookup_off | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | partial |
| BL | lookup_off | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | final | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | final | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | final | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | final | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | final | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BL | lookup_off | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| BL | lookup_off | question | pre24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | question | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | question | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | question | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | question | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | question | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | partial |
| BL | lookup_off | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | - | partial |
| BL | lookup_off | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | partial |
| BL | lookup_off | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BL | lookup_off | question | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | lookup_off | question | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | lookup_off | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BL | random | after | all | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | partial |
| BL | random | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | random | final | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BL | random | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | trailing | after | all | absent | 30 | 97% [83,99] | 3% | -0.16 [-0.22,-0.09] | 0.99 | - | partial |
| BL | trailing | after | all | value | 30 | 100% [89,100] | 0% | -0.02 [-0.03,-0.01] | 0.95 | - | partial |
| BL | trailing | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BL | trailing | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BL | trailing | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BL | trailing | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BR | binding | after | all | absent | 30 | 40% [25,58] | 27% | -1.44 [-1.77,-1.13] | 0.98 | +60 [+43,+77] | needed |
| BR | binding | after | all | value | 30 | 47% [30,64] | 30% | -1.31 [-1.63,-1.04] | 0.95 | +53 [+37,+70] | needed |
| BR | binding | both | all | absent | 30 | 13% [5,30] | 23% | -2.48 [-3.00,-2.00] | 0.99 | +87 [+73,+97] | needed |
| BR | binding | both | all | value | 30 | 20% [10,37] | 23% | -2.48 [-3.00,-2.00] | 0.98 | +80 [+67,+93] | needed |
| BR | binding | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | pre24 | value | 30 | 80% [63,90] | 7% | -0.61 [-0.91,-0.40] | 0.98 | +20 [+7,+33] | partial |
| BR | binding | both | pre32 | value | 30 | 33% [19,51] | 17% | -1.59 [-2.00,-1.21] | 0.98 | +67 [+50,+83] | needed |
| BR | binding | both | pre40 | value | 30 | 27% [14,44] | 13% | -1.77 [-2.21,-1.37] | 0.98 | +73 [+57,+87] | needed |
| BR | binding | both | pre48 | value | 30 | 23% [12,41] | 17% | -2.11 [-2.61,-1.66] | 0.98 | +77 [+60,+90] | needed |
| BR | binding | both | pre56 | value | 30 | 17% [7,34] | 23% | -2.46 [-2.98,-2.00] | 0.98 | +83 [+70,+97] | needed |
| BR | binding | both | suf08 | value | 30 | 20% [10,37] | 40% | -2.19 [-2.70,-1.74] | 0.98 | +80 [+67,+93] | needed |
| BR | binding | both | suf16 | value | 30 | 40% [25,58] | 30% | -1.80 [-2.34,-1.27] | 0.99 | +60 [+43,+77] | needed |
| BR | binding | both | suf24 | value | 30 | 43% [27,61] | 50% | -2.20 [-3.10,-1.35] | 0.99 | +57 [+40,+73] | needed |
| BR | binding | both | suf32 | value | 30 | 70% [52,83] | 27% | -0.79 [-1.28,-0.33] | 0.98 | +30 [+13,+47] | needed |
| BR | binding | both | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.04 [-0.07,-0.02] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win24-31 | value | 30 | 97% [83,99] | 3% | -0.13 [-0.26,-0.05] | 0.98 | +3 [+0,+10] | partial |
| BR | binding | both | win28-35 | value | 30 | 97% [83,99] | 3% | -0.29 [-0.75,-0.04] | 0.98 | +3 [+0,+10] | partial |
| BR | binding | both | win32-39 | value | 30 | 100% [89,100] | 0% | -0.07 [-0.13,-0.03] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | both | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | all | value | 30 | 90% [74,97] | 7% | -0.30 [-0.52,-0.11] | 0.99 | +10 [+0,+23] | partial |
| BR | binding | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.03 [-0.05,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.04 [-0.08,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | pre56 | value | 30 | 87% [70,95] | 10% | -0.29 [-0.51,-0.11] | 0.99 | +13 [+3,+27] | partial |
| BR | binding | final | suf08 | value | 30 | 87% [70,95] | 10% | -0.30 [-0.52,-0.11] | 0.99 | +13 [+3,+27] | partial |
| BR | binding | final | suf16 | value | 30 | 83% [66,93] | 13% | -0.31 [-0.54,-0.12] | 0.99 | +17 [+3,+30] | partial |
| BR | binding | final | suf24 | value | 30 | 87% [70,95] | 10% | -0.28 [-0.50,-0.10] | 0.99 | +13 [+3,+27] | partial |
| BR | binding | final | suf32 | value | 30 | 87% [70,95] | 10% | -0.26 [-0.46,-0.09] | 0.99 | +13 [+3,+27] | partial |
| BR | binding | final | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.03 [-0.06,-0.01] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | question | all | value | 30 | 27% [14,44] | 23% | -1.76 [-2.17,-1.38] | 0.98 | +73 [+57,+87] | needed |
| BR | binding | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | pre24 | value | 30 | 83% [66,93] | 10% | -0.59 [-0.83,-0.39] | 0.98 | +17 [+3,+30] | partial |
| BR | binding | question | pre32 | value | 30 | 30% [17,48] | 20% | -1.56 [-1.93,-1.23] | 0.98 | +70 [+53,+87] | needed |
| BR | binding | question | pre40 | value | 30 | 33% [19,51] | 23% | -1.58 [-1.95,-1.23] | 0.98 | +67 [+50,+83] | needed |
| BR | binding | question | pre48 | value | 30 | 27% [14,44] | 20% | -1.74 [-2.15,-1.36] | 0.98 | +73 [+57,+87] | needed |
| BR | binding | question | pre56 | value | 30 | 23% [12,41] | 23% | -1.76 [-2.18,-1.38] | 0.98 | +77 [+60,+90] | needed |
| BR | binding | question | suf08 | value | 30 | 40% [25,58] | 23% | -1.43 [-1.83,-1.08] | 0.98 | +60 [+43,+77] | needed |
| BR | binding | question | suf16 | value | 30 | 50% [33,67] | 20% | -0.98 [-1.29,-0.70] | 0.98 | +50 [+33,+67] | needed |
| BR | binding | question | suf24 | value | 30 | 73% [56,86] | 23% | -0.75 [-1.26,-0.39] | 0.98 | +27 [+10,+43] | partial |
| BR | binding | question | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.04 [-0.06,-0.02] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | question | win24-31 | value | 30 | 97% [83,99] | 3% | -0.14 [-0.29,-0.05] | 0.98 | +3 [+0,+10] | partial |
| BR | binding | question | win28-35 | value | 30 | 97% [83,99] | 3% | -0.10 [-0.23,-0.01] | 0.98 | +3 [+0,+10] | partial |
| BR | binding | question | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | binding | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | binding_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | after | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| BR | binding_off | both | all | absent | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre16 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | pre48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | both | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | binding_off | final | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win40-47 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | binding_off | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre16 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win16-23 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win44-51 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | binding_off | question | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | binding_off | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | lookup | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| BR | lookup | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | +0 [+0,+0] | partial |
| BR | lookup | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | lookup | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| BR | lookup | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| BR | lookup | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| BR | lookup_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | lookup_off | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| BR | lookup_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | lookup_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BR | lookup_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | lookup_off | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| BR | random | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | random | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| BR | random | both | all | absent | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | random | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| BR | random | final | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| BR | random | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| BR | trailing | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| BR | trailing | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| BR | trailing | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | trailing | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| BR | trailing | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| BR | trailing | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | binding | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | binding | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | binding | both | all | absent | 30 | 97% [83,99] | 3% | -0.21 [-0.32,-0.12] | 0.99 | +3 [+0,+10] | partial |
| RL | binding | both | all | value | 30 | 97% [83,99] | 3% | -0.20 [-0.31,-0.10] | 0.98 | +3 [+0,+10] | partial |
| RL | binding | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | binding | question | all | value | 30 | 100% [89,100] | 0% | -0.04 [-0.07,-0.02] | 0.98 | +0 [+0,+0] | partial |
| RL | binding_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | binding_off | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | binding_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | binding_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | binding_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | binding_off | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup | after | all | absent | 30 | 7% [2,21] | 37% | -3.33 [-3.87,-2.87] | 0.98 | +93 [+83,+100] | needed |
| RL | lookup | after | all | value | 30 | 7% [2,21] | 30% | -3.19 [-3.71,-2.74] | 0.94 | +93 [+83,+100] | needed |
| RL | lookup | both | all | absent | 30 | 13% [5,30] | 53% | -3.55 [-4.10,-2.94] | 0.99 | +87 [+73,+97] | needed |
| RL | lookup | both | all | value | 30 | 13% [5,30] | 53% | -3.49 [-4.05,-2.91] | 0.97 | +87 [+73,+97] | needed |
| RL | lookup | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | pre48 | value | 30 | 93% [79,98] | 7% | -0.40 [-0.57,-0.24] | 0.97 | +7 [+0,+17] | partial |
| RL | lookup | both | pre56 | value | 30 | 57% [39,73] | 23% | -1.15 [-1.47,-0.87] | 0.97 | +43 [+27,+60] | needed |
| RL | lookup | both | suf08 | value | 30 | 13% [5,30] | 53% | -3.53 [-4.09,-2.92] | 0.97 | +87 [+73,+97] | needed |
| RL | lookup | both | suf16 | value | 30 | 10% [3,26] | 67% | -3.73 [-4.32,-3.11] | 0.97 | +90 [+80,+100] | needed |
| RL | lookup | both | suf24 | value | 30 | 7% [2,21] | 63% | -3.69 [-4.25,-3.11] | 0.97 | +93 [+83,+100] | needed |
| RL | lookup | both | suf32 | value | 30 | 3% [1,17] | 70% | -4.18 [-4.96,-3.43] | 0.97 | +97 [+90,+100] | needed |
| RL | lookup | both | suf40 | value | 30 | 0% [-0,11] | 77% | -6.04 [-6.89,-5.24] | 0.98 | +100 [+100,+100] | needed |
| RL | lookup | both | suf48 | value | 30 | 0% [-0,11] | 100% | -7.74 [-8.40,-7.11] | 0.98 | +100 [+100,+100] | needed |
| RL | lookup | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | both | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | both | win48-55 | value | 30 | 90% [74,97] | 10% | -0.27 [-0.43,-0.15] | 0.97 | +10 [+0,+20] | partial |
| RL | lookup | both | win52-59 | value | 30 | 100% [89,100] | 0% | -0.03 [-0.05,-0.01] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | all | value | 30 | 7% [2,21] | 63% | -3.33 [-3.87,-2.81] | 0.98 | +93 [+83,+100] | needed |
| RL | lookup | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.13 [-0.21,-0.06] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | pre56 | value | 30 | 60% [42,75] | 20% | -1.06 [-1.43,-0.75] | 0.98 | +40 [+23,+57] | needed |
| RL | lookup | final | suf08 | value | 30 | 7% [2,21] | 63% | -3.32 [-3.85,-2.81] | 0.98 | +93 [+83,+100] | needed |
| RL | lookup | final | suf16 | value | 30 | 7% [2,21] | 67% | -3.30 [-3.84,-2.79] | 0.98 | +93 [+83,+100] | needed |
| RL | lookup | final | suf24 | value | 30 | 7% [2,21] | 67% | -3.29 [-3.85,-2.75] | 0.98 | +93 [+83,+100] | needed |
| RL | lookup | final | suf32 | value | 30 | 10% [3,26] | 67% | -3.19 [-3.82,-2.64] | 0.98 | +90 [+80,+100] | needed |
| RL | lookup | final | suf40 | value | 30 | 7% [2,21] | 80% | -3.76 [-4.49,-3.05] | 0.99 | +93 [+83,+100] | needed |
| RL | lookup | final | suf48 | value | 30 | 17% [7,34] | 83% | -3.40 [-4.07,-2.66] | 0.99 | +83 [+70,+97] | needed |
| RL | lookup | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | final | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win48-55 | value | 30 | 100% [89,100] | 0% | -0.05 [-0.08,-0.03] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RL | lookup | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| RL | lookup | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | +0 [+0,+0] | partial |
| RL | lookup | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RL | lookup | question | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | +0 [+0,+0] | partial |
| RL | lookup | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RL | lookup | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup | question | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RL | lookup_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | after | all | value | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | partial |
| RL | lookup_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | lookup_off | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | lookup_off | both | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | both | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | both | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | both | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | final | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| RL | lookup_off | final | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | final | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | final | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win48-55 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RL | lookup_off | final | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | partial |
| RL | lookup_off | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | question | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RL | lookup_off | question | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | lookup_off | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | question | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | partial |
| RL | lookup_off | question | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | lookup_off | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | partial |
| RL | lookup_off | question | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RL | lookup_off | question | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| RL | lookup_off | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.93 | - | partial |
| RL | lookup_off | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | partial |
| RL | lookup_off | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RL | lookup_off | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RL | lookup_off | question | win52-59 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | lookup_off | question | win56-63 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RL | random | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | partial |
| RL | random | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | random | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | random | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | random | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | trailing | after | all | absent | 30 | 93% [79,98] | 7% | -0.20 [-0.30,-0.11] | 0.99 | - | partial |
| RL | trailing | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | partial |
| RL | trailing | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | trailing | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RL | trailing | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RL | trailing | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | binding | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | binding | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | binding | both | all | absent | 30 | 93% [79,98] | 7% | -0.12 [-0.23,-0.04] | 0.99 | +7 [+0,+17] | partial |
| RR | binding | both | all | value | 30 | 93% [79,98] | 7% | -0.11 [-0.22,-0.03] | 0.98 | +7 [+0,+17] | partial |
| RR | binding | final | all | value | 30 | 100% [89,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | binding | question | all | value | 30 | 97% [83,99] | 3% | -0.06 [-0.12,-0.02] | 0.98 | +3 [+0,+10] | partial |
| RR | binding_off | after | all | absent | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | binding_off | after | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RR | binding_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | binding_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | binding_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | binding_off | question | all | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | +0 [+0,+0] | partial |
| RR | lookup | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | both | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | both | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | both | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | +0 [+0,+0] | partial |
| RR | lookup | final | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | +0 [+0,+0] | partial |
| RR | lookup | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | +0 [+0,+0] | partial |
| RR | lookup | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | pre32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | pre40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | pre48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | pre56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | question | win00-07 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | question | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | lookup | question | win28-35 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | +0 [+0,+0] | partial |
| RR | lookup | question | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | +0 [+0,+0] | partial |
| RR | lookup | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | +0 [+0,+0] | partial |
| RR | lookup | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup | question | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | +0 [+0,+0] | partial |
| RR | lookup_off | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | partial |
| RR | lookup_off | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | partial |
| RR | lookup_off | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | both | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | both | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win24-31 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | both | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | both | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | both | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | both | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | both | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | lookup_off | final | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf08 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | suf56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| RR | lookup_off | final | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win04-11 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win08-15 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win12-19 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | win20-27 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | final | win32-39 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win36-43 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | partial |
| RR | lookup_off | final | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | partial |
| RR | lookup_off | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | pre08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | pre16 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | pre24 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | pre32 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | pre40 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | question | pre48 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | pre56 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf08 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf16 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf24 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf32 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf40 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | suf48 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | suf56 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | win00-07 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | win04-11 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | win08-15 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | win12-19 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | question | win16-23 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | question | win20-27 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | question | win24-31 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RR | lookup_off | question | win28-35 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | partial |
| RR | lookup_off | question | win32-39 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | partial |
| RR | lookup_off | question | win36-43 | value | 30 | 100% [89,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | win40-47 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | win44-51 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | win48-55 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | lookup_off | question | win52-59 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | lookup_off | question | win56-63 | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | partial |
| RR | random | after | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | random | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | partial |
| RR | random | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | partial |
| RR | random | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | random | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | random | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | partial |
| RR | trailing | after | all | absent | 30 | 100% [89,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | partial |
| RR | trailing | after | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | partial |
| RR | trailing | both | all | absent | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | trailing | both | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | partial |
| RR | trailing | final | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | partial |
| RR | trailing | question | all | value | 30 | 100% [89,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | partial |
