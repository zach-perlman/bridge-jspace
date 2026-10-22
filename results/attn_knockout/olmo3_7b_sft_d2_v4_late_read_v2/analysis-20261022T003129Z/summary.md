# attn_knockout / olmo3_7b_sft_d2_v4_late_read_v2

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
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 0.94,
     "verdict": "partial"
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
     "acc": 0.95,
     "verdict": "partial"
    },
    "band16-23": {
     "acc": 0.16,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.94,
     "verdict": "partial"
    },
    "band20-23": {
     "acc": 0.87,
     "verdict": "partial"
    },
    "band24-31": {
     "acc": 0.98,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.38,
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
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 0.997,
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
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band16-23": {
     "acc": 0.307,
     "verdict": "needed"
    },
    "band16-19": {
     "acc": 0.967,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 1.0,
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
    "acc": 0.087,
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
| RL | lookup | after | all | value | 100 | 6% [3,12] | 80% | -3.70 [-4.02,-3.41] | - | +93 [+87,+98] | needed |
| RL | lookup | both | all | value | 100 | 3% [1,8] | 78% | -3.61 [-3.88,-3.34] | - | +96 [+92,+99] | needed |
| RL | lookup | both | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | both | band00-15 | value | 100 | 20% [13,29] | 58% | -2.17 [-2.35,-1.98] | - | +79 [+71,+87] | needed |
| RL | lookup | both | band04-07 | value | 100 | 100% [96,100] | 0% | -0.05 [-0.06,-0.03] | - | - | not_needed |
| RL | lookup | both | band08-11 | value | 100 | 64% [54,73] | 29% | -1.10 [-1.31,-0.92] | - | +35 [+26,+44] | needed |
| RL | lookup | both | band12-15 | value | 100 | 76% [67,83] | 24% | -0.73 [-0.95,-0.53] | - | +24 [+16,+33] | needed |
| RL | lookup | both | band16-19 | value | 100 | 93% [86,97] | 7% | -0.20 [-0.26,-0.15] | - | +7 [+2,+12] | partial |
| RL | lookup | both | band16-23 | value | 100 | 16% [10,24] | 84% | -1.78 [-1.96,-1.61] | - | +84 [+77,+91] | needed |
| RL | lookup | both | band20-23 | value | 100 | 87% [79,92] | 13% | -0.31 [-0.39,-0.24] | - | +13 [+7,+20] | partial |
| RL | lookup | both | band24-27 | value | 100 | 99% [95,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | both | band24-31 | value | 100 | 98% [93,99] | 2% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | both | band28-31 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | all | value | 100 | 1% [0,5] | 99% | -5.45 [-5.85,-5.06] | - | +99 [+97,+100] | needed |
| RL | lookup | final | band00-03 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-15 | value | 100 | 94% [88,97] | 6% | -0.14 [-0.20,-0.09] | - | +6 [+2,+11] | partial |
| RL | lookup | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band12-15 | value | 100 | 95% [89,98] | 5% | -0.13 [-0.20,-0.09] | - | +5 [+1,+10] | partial |
| RL | lookup | final | band16-19 | value | 100 | 94% [88,97] | 6% | -0.20 [-0.26,-0.15] | - | +6 [+2,+11] | partial |
| RL | lookup | final | band16-23 | value | 100 | 16% [10,24] | 84% | -1.80 [-1.98,-1.63] | - | +84 [+76,+91] | needed |
| RL | lookup | final | band20-23 | value | 100 | 87% [79,92] | 13% | -0.31 [-0.40,-0.24] | - | +13 [+7,+20] | partial |
| RL | lookup | final | band24-27 | value | 100 | 99% [95,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | final | band24-31 | value | 100 | 98% [93,99] | 2% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | final | band28-31 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | question | all | value | 100 | 38% [29,48] | 44% | -1.99 [-2.19,-1.78] | - | +60 [+49,+70] | needed |
| RL | lookup | question | band00-03 | value | 100 | 99% [95,100] | 1% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | question | band00-15 | value | 100 | 38% [29,48] | 45% | -1.99 [-2.18,-1.78] | - | +60 [+49,+70] | needed |
| RL | lookup | question | band04-07 | value | 100 | 100% [96,100] | 0% | -0.05 [-0.06,-0.03] | - | - | not_needed |
| RL | lookup | question | band08-11 | value | 100 | 66% [56,75] | 28% | -1.09 [-1.30,-0.91] | - | +33 [+24,+42] | needed |
| RL | lookup | question | band12-15 | value | 100 | 88% [80,93] | 12% | -0.26 [-0.36,-0.18] | - | +12 [+6,+19] | partial |
| RL | lookup | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-27 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | all | value | 100 | 99% [95,100] | 1% | -0.02 [-0.07,+0.02] | - | - | not_needed |
| RL | lookup_off | both | all | value | 100 | 99% [95,100] | 0% | +0.00 [-0.02,+0.02] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-15 | value | 100 | 99% [95,100] | 0% | -0.01 [-0.04,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band16-23 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | all | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-15 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band16-23 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 98% [93,99] | 1% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-15 | value | 100 | 98% [93,99] | 1% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | after | all | value | 100 | 99% [95,100] | 1% | +0.01 [-0.01,+0.03] | - | - | not_needed |
| RL | random | both | all | value | 100 | 99% [95,100] | 1% | +0.01 [-0.02,+0.03] | - | - | not_needed |
| RL | random | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band00-15 | value | 100 | 99% [95,100] | 1% | +0.01 [-0.03,+0.03] | - | - | not_needed |
| RL | random | both | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band08-11 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band12-15 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band16-19 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | both | band16-23 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| RL | random | both | band20-23 | value | 100 | 100% [96,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL | random | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | all | value | 100 | 99% [95,100] | 1% | +0.01 [-0.01,+0.02] | - | - | not_needed |
| RL | random | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band00-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | random | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band12-15 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band16-19 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band16-23 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| RL | random | final | band20-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | all | value | 100 | 99% [95,100] | 1% | +0.00 [-0.03,+0.03] | - | - | not_needed |
| RL | random | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | question | band00-15 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.03,+0.02] | - | - | not_needed |
| RL | random | question | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | question | band08-11 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | question | band12-15 | value | 100 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | trailing | after | all | value | 82 | 100% [96,100] | 0% | -0.02 [-0.04,+0.00] | - | - | not_needed |
| RL | trailing | both | all | value | 82 | 99% [93,100] | 1% | -0.00 [-0.02,+0.01] | - | - | not_needed |
| RL | trailing | final | all | value | 82 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | trailing | question | all | value | 82 | 99% [93,100] | 1% | -0.00 [-0.02,+0.01] | - | - | not_needed |
| DL | lookup | after | all | value | 300 | 18% [14,23] | 10% | -2.53 [-2.69,-2.39] | - | +82 [+78,+86] | needed |
| DL | lookup | both | all | value | 300 | 11% [8,15] | 12% | -2.89 [-3.05,-2.74] | - | +89 [+85,+92] | needed |
| DL | lookup | both | band00-03 | value | 300 | 97% [94,98] | 0% | -0.11 [-0.19,-0.05] | - | - | not_needed |
| DL | lookup | both | band00-15 | value | 300 | 6% [4,9] | 8% | -4.29 [-4.50,-4.08] | - | +94 [+92,+97] | needed |
| DL | lookup | both | band04-07 | value | 300 | 99% [97,100] | 0% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| DL | lookup | both | band08-11 | value | 300 | 86% [82,90] | 8% | -0.47 [-0.61,-0.34] | - | +14 [+10,+18] | partial |
| DL | lookup | both | band12-15 | value | 300 | 81% [77,85] | 18% | -0.54 [-0.70,-0.40] | - | +19 [+15,+23] | partial |
| DL | lookup | both | band16-19 | value | 300 | 96% [94,98] | 4% | -0.10 [-0.14,-0.06] | - | - | not_needed |
| DL | lookup | both | band16-23 | value | 300 | 29% [24,34] | 70% | -1.84 [-2.00,-1.68] | - | +71 [+66,+76] | needed |
| DL | lookup | both | band20-23 | value | 300 | 99% [97,100] | 1% | -0.05 [-0.08,-0.03] | - | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | all | value | 300 | 4% [3,7] | 95% | -7.28 [-7.57,-6.99] | - | +96 [+93,+98] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-15 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 97% [94,98] | 3% | -0.09 [-0.13,-0.06] | - | - | not_needed |
| DL | lookup | final | band16-23 | value | 300 | 31% [26,36] | 69% | -1.79 [-1.95,-1.64] | - | +69 [+64,+75] | needed |
| DL | lookup | final | band20-23 | value | 300 | 99% [97,100] | 1% | -0.05 [-0.08,-0.03] | - | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | all | value | 300 | 9% [6,12] | 5% | -4.20 [-4.42,-3.97] | - | +91 [+88,+94] | needed |
| DL | lookup | question | band00-03 | value | 300 | 97% [94,98] | 0% | -0.11 [-0.19,-0.05] | - | - | not_needed |
| DL | lookup | question | band00-15 | value | 300 | 8% [6,12] | 5% | -4.20 [-4.43,-3.98] | - | +92 [+88,+95] | needed |
| DL | lookup | question | band04-07 | value | 300 | 99% [97,100] | 0% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| DL | lookup | question | band08-11 | value | 300 | 87% [83,90] | 8% | -0.47 [-0.61,-0.34] | - | +13 [+9,+17] | partial |
| DL | lookup | question | band12-15 | value | 300 | 94% [91,96] | 6% | -0.22 [-0.32,-0.13] | - | - | not_needed |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | after | all | value | 242 | 98% [95,99] | 2% | -0.04 [-0.07,-0.02] | - | - | not_needed |
| DL | trailing | both | all | value | 242 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | final | all | value | 242 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | question | all | value | 242 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
