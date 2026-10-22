# attn_knockout / olmo3_7b_instruct_d2_v4_late_read_v3

Measure: correct (items: {"DL": {"items": 300, "unedited_right": 300}, "RL": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.0,
     "verdict": "needed"
    },
    "band00-15": {
     "acc": 0.96,
     "verdict": "not_needed"
    },
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band04-07": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band08-11": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band12-15": {
     "acc": 0.96,
     "verdict": "not_needed"
    },
    "band16-23": {
     "acc": 0.28,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.94,
     "verdict": "partial"
    },
    "band20-23": {
     "acc": 0.9,
     "verdict": "partial"
    },
    "band24-27": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.14,
    "verdict": "needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "DL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.037,
     "verdict": "needed"
    },
    "band00-15": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band04-07": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band08-11": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band12-15": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band16-23": {
     "acc": 0.467,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.977,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.05,
    "verdict": "needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  }
 },
 "C1a_RL_breaks_RR_survives": {
  "RL": "needed",
  "RR": null,
  "holds": false
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": null,
   "question": null
  },
  "RL": {
   "final": "needed",
   "question": "needed"
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
  "DL/lookup/question": {
   "windows_needed": [
    "band00-15"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/final": {
   "windows_needed": [
    "band16-23"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/both": {
   "windows_needed": [
    "band00-15",
    "band16-23"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/question": {
   "windows_needed": [
    "band00-15",
    "band08-11"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/final": {
   "windows_needed": [
    "band16-23"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/both": {
   "windows_needed": [
    "band00-15",
    "band16-23",
    "band08-11",
    "band12-15"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | after | all | value | 100 | 4% [2,10] | 39% | -5.18 [-5.65,-4.72] | - | +94 [+89,+98] | needed |
| RL | lookup | both | all | value | 100 | 3% [1,8] | 33% | -5.48 [-5.91,-5.04] | - | +96 [+92,+99] | needed |
| RL | lookup | both | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.06,-0.01] | - | - | not_needed |
| RL | lookup | both | band00-15 | value | 100 | 9% [5,16] | 33% | -4.06 [-4.50,-3.66] | - | +90 [+84,+95] | needed |
| RL | lookup | both | band04-07 | value | 100 | 99% [95,100] | 1% | -0.04 [-0.06,-0.02] | - | - | not_needed |
| RL | lookup | both | band08-11 | value | 100 | 53% [43,62] | 20% | -1.98 [-2.44,-1.56] | - | +47 [+37,+57] | needed |
| RL | lookup | both | band12-15 | value | 100 | 74% [65,82] | 23% | -1.12 [-1.56,-0.73] | - | +26 [+18,+35] | needed |
| RL | lookup | both | band16-19 | value | 100 | 94% [88,97] | 6% | -0.18 [-0.32,-0.09] | - | +6 [+2,+11] | partial |
| RL | lookup | both | band16-23 | value | 100 | 29% [21,39] | 68% | -2.36 [-2.75,-1.95] | - | +71 [+62,+79] | needed |
| RL | lookup | both | band20-23 | value | 100 | 91% [84,95] | 9% | -0.26 [-0.41,-0.14] | - | +9 [+4,+15] | partial |
| RL | lookup | both | band24-27 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | both | band24-31 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | both | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | all | value | 100 | 0% [0,4] | 96% | -8.02 [-8.69,-7.37] | - | +100 [+100,+100] | needed |
| RL | lookup | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-15 | value | 100 | 96% [90,98] | 4% | -0.12 [-0.19,-0.05] | - | - | not_needed |
| RL | lookup | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | band12-15 | value | 100 | 96% [90,98] | 4% | -0.11 [-0.18,-0.04] | - | - | not_needed |
| RL | lookup | final | band16-19 | value | 100 | 94% [88,97] | 6% | -0.18 [-0.32,-0.08] | - | +6 [+2,+11] | partial |
| RL | lookup | final | band16-23 | value | 100 | 28% [20,37] | 69% | -2.43 [-2.82,-2.02] | - | +72 [+63,+80] | needed |
| RL | lookup | final | band20-23 | value | 100 | 90% [83,94] | 10% | -0.26 [-0.41,-0.14] | - | +10 [+5,+16] | partial |
| RL | lookup | final | band24-27 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | final | band24-31 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | final | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | all | value | 100 | 14% [9,22] | 29% | -3.73 [-4.19,-3.31] | - | +85 [+77,+92] | needed |
| RL | lookup | question | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.06,-0.01] | - | - | not_needed |
| RL | lookup | question | band00-15 | value | 100 | 14% [9,22] | 29% | -3.72 [-4.19,-3.30] | - | +85 [+77,+92] | needed |
| RL | lookup | question | band04-07 | value | 100 | 99% [95,100] | 1% | -0.04 [-0.06,-0.02] | - | - | not_needed |
| RL | lookup | question | band08-11 | value | 100 | 56% [46,65] | 19% | -1.96 [-2.43,-1.54] | - | +44 [+35,+54] | needed |
| RL | lookup | question | band12-15 | value | 100 | 87% [79,92] | 11% | -0.29 [-0.45,-0.16] | - | +13 [+7,+20] | partial |
| RL | lookup | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | all | value | 100 | 98% [93,99] | 2% | -0.04 [-0.12,+0.01] | - | - | not_needed |
| RL | lookup_off | both | all | value | 100 | 99% [95,100] | 0% | -0.02 [-0.07,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-15 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.07,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | all | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 99% [95,100] | 0% | -0.02 [-0.06,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-15 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.06,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | after | all | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | all | value | 100 | 99% [95,100] | 0% | -0.02 [-0.09,+0.01] | - | - | not_needed |
| RL | random | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band00-15 | value | 100 | 99% [95,100] | 0% | -0.03 [-0.10,+0.01] | - | - | not_needed |
| RL | random | both | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band12-15 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,+0.01] | - | - | not_needed |
| RL | random | both | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | all | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band00-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | all | value | 100 | 99% [95,100] | 0% | -0.03 [-0.09,+0.01] | - | - | not_needed |
| RL | random | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | question | band00-15 | value | 100 | 99% [95,100] | 0% | -0.03 [-0.10,+0.01] | - | - | not_needed |
| RL | random | question | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | question | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | question | band12-15 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | random | question | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-27 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | trailing | after | all | value | 81 | 100% [95,100] | 0% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | trailing | both | all | value | 81 | 100% [95,100] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | trailing | final | all | value | 81 | 100% [95,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | trailing | question | all | value | 81 | 100% [95,100] | 0% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| DL | lookup | after | all | value | 300 | 16% [12,20] | 8% | -3.62 [-3.90,-3.35] | - | +84 [+80,+88] | needed |
| DL | lookup | both | all | value | 300 | 10% [7,14] | 9% | -4.46 [-4.74,-4.16] | - | +90 [+87,+93] | needed |
| DL | lookup | both | band00-03 | value | 300 | 96% [93,98] | 0% | -0.20 [-0.34,-0.08] | - | - | not_needed |
| DL | lookup | both | band00-15 | value | 300 | 5% [3,8] | 7% | -7.36 [-7.74,-6.93] | - | +95 [+93,+98] | needed |
| DL | lookup | both | band04-07 | value | 300 | 99% [97,100] | 0% | -0.04 [-0.09,-0.00] | - | - | not_needed |
| DL | lookup | both | band08-11 | value | 300 | 82% [78,86] | 9% | -1.13 [-1.50,-0.83] | - | +18 [+14,+22] | partial |
| DL | lookup | both | band12-15 | value | 300 | 81% [76,85] | 19% | -1.23 [-1.59,-0.90] | - | +19 [+15,+24] | partial |
| DL | lookup | both | band16-19 | value | 300 | 97% [95,99] | 3% | -0.11 [-0.22,-0.04] | - | - | not_needed |
| DL | lookup | both | band16-23 | value | 300 | 46% [41,52] | 50% | -2.60 [-2.95,-2.25] | - | +54 [+48,+59] | needed |
| DL | lookup | both | band20-23 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | all | value | 300 | 4% [2,6] | 90% | -11.91 [-12.44,-11.33] | - | +96 [+94,+98] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 98% [95,99] | 2% | -0.12 [-0.22,-0.04] | - | - | not_needed |
| DL | lookup | final | band16-23 | value | 300 | 47% [41,52] | 50% | -2.53 [-2.87,-2.18] | - | +53 [+48,+59] | needed |
| DL | lookup | final | band20-23 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | all | value | 300 | 5% [3,8] | 4% | -7.35 [-7.77,-6.89] | - | +95 [+92,+97] | needed |
| DL | lookup | question | band00-03 | value | 300 | 96% [93,98] | 0% | -0.20 [-0.34,-0.08] | - | - | not_needed |
| DL | lookup | question | band00-15 | value | 300 | 5% [3,8] | 3% | -7.35 [-7.77,-6.89] | - | +95 [+92,+97] | needed |
| DL | lookup | question | band04-07 | value | 300 | 99% [97,100] | 0% | -0.03 [-0.09,-0.00] | - | - | not_needed |
| DL | lookup | question | band08-11 | value | 300 | 82% [78,86] | 9% | -1.14 [-1.49,-0.83] | - | +18 [+14,+22] | partial |
| DL | lookup | question | band12-15 | value | 300 | 92% [88,94] | 8% | -0.45 [-0.68,-0.26] | - | +8 [+5,+12] | partial |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | after | all | value | 241 | 98% [95,99] | 2% | -0.10 [-0.19,-0.02] | - | - | not_needed |
| DL | trailing | both | all | value | 241 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | final | all | value | 241 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | question | all | value | 241 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
