# attn_knockout / olmo3_7b_dpo_d2_v4_late_read_v2

Measure: correct (items: {"DL": {"items": 300, "unedited_right": 300}, "RL": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.01,
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
     "acc": 0.37,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.96,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.93,
     "verdict": "partial"
    },
    "band24-31": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.21,
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
     "acc": 0.043,
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
     "acc": 0.517,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.957,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.047,
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
    "band08-11"
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
| RL | lookup | after | all | value | 100 | 7% [3,14] | 43% | -4.65 [-5.11,-4.21] | - | +91 [+85,+96] | needed |
| RL | lookup | both | all | value | 100 | 5% [2,11] | 39% | -4.92 [-5.36,-4.51] | - | +94 [+89,+98] | needed |
| RL | lookup | both | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.05,-0.01] | - | - | not_needed |
| RL | lookup | both | band00-15 | value | 100 | 14% [9,22] | 32% | -3.82 [-4.24,-3.39] | - | +85 [+78,+92] | needed |
| RL | lookup | both | band04-07 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.05,-0.01] | - | - | not_needed |
| RL | lookup | both | band08-11 | value | 100 | 59% [49,68] | 18% | -1.71 [-2.19,-1.29] | - | +39 [+30,+49] | needed |
| RL | lookup | both | band12-15 | value | 100 | 81% [72,87] | 17% | -0.92 [-1.35,-0.56] | - | +19 [+12,+27] | partial |
| RL | lookup | both | band16-19 | value | 100 | 96% [90,98] | 4% | -0.14 [-0.28,-0.05] | - | - | not_needed |
| RL | lookup | both | band16-23 | value | 100 | 38% [29,48] | 60% | -2.17 [-2.60,-1.78] | - | +62 [+53,+72] | needed |
| RL | lookup | both | band20-23 | value | 100 | 93% [86,97] | 7% | -0.18 [-0.30,-0.09] | - | +7 [+3,+12] | partial |
| RL | lookup | both | band24-27 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup | both | band24-31 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | both | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | all | value | 100 | 1% [0,5] | 94% | -7.60 [-8.28,-6.97] | - | +99 [+97,+100] | needed |
| RL | lookup | final | band00-03 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-15 | value | 100 | 96% [90,98] | 4% | -0.10 [-0.19,-0.03] | - | - | not_needed |
| RL | lookup | final | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | band12-15 | value | 100 | 96% [90,98] | 4% | -0.08 [-0.15,-0.03] | - | - | not_needed |
| RL | lookup | final | band16-19 | value | 100 | 96% [90,98] | 4% | -0.13 [-0.27,-0.05] | - | - | not_needed |
| RL | lookup | final | band16-23 | value | 100 | 37% [28,47] | 61% | -2.25 [-2.69,-1.86] | - | +63 [+53,+72] | needed |
| RL | lookup | final | band20-23 | value | 100 | 93% [86,97] | 7% | -0.18 [-0.31,-0.09] | - | +7 [+3,+12] | partial |
| RL | lookup | final | band24-27 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup | final | band24-31 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | final | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | all | value | 100 | 21% [14,30] | 27% | -3.48 [-3.92,-3.04] | - | +77 [+69,+85] | needed |
| RL | lookup | question | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.05,-0.01] | - | - | not_needed |
| RL | lookup | question | band00-15 | value | 100 | 21% [14,30] | 27% | -3.47 [-3.92,-3.03] | - | +77 [+69,+85] | needed |
| RL | lookup | question | band04-07 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.05,-0.01] | - | - | not_needed |
| RL | lookup | question | band08-11 | value | 100 | 60% [50,69] | 17% | -1.69 [-2.16,-1.27] | - | +38 [+29,+48] | needed |
| RL | lookup | question | band12-15 | value | 100 | 92% [85,96] | 6% | -0.23 [-0.38,-0.11] | - | +8 [+3,+14] | partial |
| RL | lookup | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | all | value | 100 | 98% [93,99] | 2% | -0.02 [-0.09,+0.02] | - | - | not_needed |
| RL | lookup_off | both | all | value | 100 | 99% [95,100] | 0% | -0.01 [-0.07,+0.02] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-15 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.08,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 100 | 98% [93,99] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | all | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-15 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 98% [93,99] | 1% | -0.03 [-0.09,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-15 | value | 100 | 98% [93,99] | 1% | -0.03 [-0.09,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 100 | 98% [93,99] | 1% | -0.01 [-0.04,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | after | all | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | all | value | 100 | 98% [93,99] | 1% | -0.02 [-0.07,+0.01] | - | - | not_needed |
| RL | random | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band00-15 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.08,+0.02] | - | - | not_needed |
| RL | random | both | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | both | band16-19 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | random | both | band16-23 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | random | both | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | all | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,+0.01] | - | - | not_needed |
| RL | random | final | band00-03 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | final | band00-15 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | random | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band16-19 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | random | final | band16-23 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | random | final | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | all | value | 100 | 99% [95,100] | 0% | -0.02 [-0.08,+0.02] | - | - | not_needed |
| RL | random | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | question | band00-15 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.08,+0.02] | - | - | not_needed |
| RL | random | question | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | question | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | question | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | question | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | trailing | after | all | value | 80 | 100% [95,100] | 0% | -0.01 [-0.03,+0.02] | - | - | not_needed |
| RL | trailing | both | all | value | 80 | 100% [95,100] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | trailing | final | all | value | 80 | 100% [95,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | trailing | question | all | value | 80 | 100% [95,100] | 0% | -0.00 [-0.02,+0.00] | - | - | not_needed |
| DL | lookup | after | all | value | 300 | 17% [13,22] | 7% | -3.43 [-3.70,-3.16] | - | +83 [+78,+87] | needed |
| DL | lookup | both | all | value | 300 | 10% [7,14] | 7% | -4.28 [-4.55,-4.00] | - | +90 [+86,+93] | needed |
| DL | lookup | both | band00-03 | value | 300 | 95% [92,97] | 0% | -0.23 [-0.40,-0.10] | - | - | not_needed |
| DL | lookup | both | band00-15 | value | 300 | 3% [2,6] | 4% | -7.70 [-8.08,-7.30] | - | +97 [+95,+99] | needed |
| DL | lookup | both | band04-07 | value | 300 | 99% [97,100] | 0% | -0.05 [-0.11,-0.00] | - | - | not_needed |
| DL | lookup | both | band08-11 | value | 300 | 80% [75,84] | 9% | -1.26 [-1.62,-0.93] | - | +20 [+15,+25] | partial |
| DL | lookup | both | band12-15 | value | 300 | 81% [76,85] | 18% | -1.17 [-1.52,-0.84] | - | +19 [+15,+24] | partial |
| DL | lookup | both | band16-19 | value | 300 | 96% [93,97] | 2% | -0.16 [-0.28,-0.08] | - | - | not_needed |
| DL | lookup | both | band16-23 | value | 300 | 51% [46,57] | 45% | -2.31 [-2.64,-1.96] | - | +49 [+43,+54] | needed |
| DL | lookup | both | band20-23 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | both | band24-31 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | all | value | 300 | 4% [3,7] | 87% | -11.24 [-11.77,-10.68] | - | +96 [+93,+98] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 96% [93,97] | 2% | -0.17 [-0.29,-0.07] | - | - | not_needed |
| DL | lookup | final | band16-23 | value | 300 | 52% [46,57] | 44% | -2.24 [-2.57,-1.90] | - | +48 [+43,+54] | needed |
| DL | lookup | final | band20-23 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | final | band24-31 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | all | value | 300 | 5% [3,8] | 3% | -7.76 [-8.16,-7.33] | - | +95 [+93,+98] | needed |
| DL | lookup | question | band00-03 | value | 300 | 95% [92,97] | 0% | -0.23 [-0.40,-0.10] | - | - | not_needed |
| DL | lookup | question | band00-15 | value | 300 | 4% [3,7] | 3% | -7.76 [-8.17,-7.33] | - | +96 [+93,+98] | needed |
| DL | lookup | question | band04-07 | value | 300 | 99% [97,100] | 0% | -0.05 [-0.11,-0.00] | - | - | not_needed |
| DL | lookup | question | band08-11 | value | 300 | 81% [76,85] | 9% | -1.26 [-1.62,-0.92] | - | +19 [+15,+24] | partial |
| DL | lookup | question | band12-15 | value | 300 | 92% [89,95] | 6% | -0.38 [-0.58,-0.22] | - | +8 [+5,+11] | partial |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,+0.00] | - | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
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
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | after | all | value | 240 | 96% [93,98] | 4% | -0.14 [-0.27,-0.05] | - | - | not_needed |
| DL | trailing | both | all | value | 240 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | final | all | value | 240 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | question | all | value | 240 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
