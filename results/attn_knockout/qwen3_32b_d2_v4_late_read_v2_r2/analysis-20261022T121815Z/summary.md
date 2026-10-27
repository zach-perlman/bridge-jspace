# attn_knockout / qwen3_32b_d2_v4_late_read_v2_r2

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}, "DL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.033,
     "verdict": "needed"
    },
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31": {
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
    "band16-19": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band20-23": {
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
    },
    "band32-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-35": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band36-39": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band40-43": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band44-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.03,
     "verdict": "needed"
    },
    "band48-51": {
     "acc": 0.967,
     "verdict": "not_needed"
    },
    "band52-55": {
     "acc": 0.373,
     "verdict": "needed"
    },
    "band56-59": {
     "acc": 0.993,
     "verdict": "not_needed"
    },
    "band60-63": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.32,
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
     "acc": 0.03,
     "verdict": "needed"
    },
    "band00-03": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31": {
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
    "band16-19": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band20-23": {
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
    },
    "band32-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-35": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band36-39": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band40-43": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band44-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.03,
     "verdict": "needed"
    },
    "band48-51": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band52-55": {
     "acc": 0.397,
     "verdict": "needed"
    },
    "band56-59": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band60-63": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.04,
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
  "RL/lookup/question": {
   "windows_needed": [
    "band32-47",
    "band40-43"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/final": {
   "windows_needed": [
    "band48-63",
    "band52-55"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/both": {
   "windows_needed": [
    "band32-47",
    "band48-63",
    "band40-43",
    "band52-55"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/question": {
   "windows_needed": [
    "band32-47"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/final": {
   "windows_needed": [
    "band48-63",
    "band52-55"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/both": {
   "windows_needed": [
    "band32-47",
    "band48-63",
    "band52-55"
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
| RL | lookup | after | all | value | 300 | 10% [7,14] | 52% | -4.67 [-5.03,-4.32] | - | +89 [+85,+92] | needed |
| RL | lookup | both | all | value | 300 | 6% [4,9] | 49% | -5.17 [-5.49,-4.85] | - | +94 [+91,+96] | needed |
| RL | lookup | both | band00-03 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup | both | band00-31 | value | 300 | 98% [96,99] | 2% | -0.05 [-0.09,-0.01] | - | - | not_needed |
| RL | lookup | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band16-19 | value | 300 | 99% [98,100] | 0% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band28-31 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup | both | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | band32-47 | value | 300 | 34% [29,39] | 24% | -3.08 [-3.39,-2.80] | - | +65 [+59,+71] | needed |
| RL | lookup | both | band36-39 | value | 300 | 92% [89,95] | 4% | -0.31 [-0.45,-0.19] | - | +8 [+5,+11] | partial |
| RL | lookup | both | band40-43 | value | 300 | 75% [69,79] | 11% | -1.08 [-1.32,-0.86] | - | +25 [+21,+30] | needed |
| RL | lookup | both | band44-47 | value | 300 | 91% [87,93] | 9% | -0.32 [-0.46,-0.21] | - | +9 [+6,+13] | partial |
| RL | lookup | both | band48-51 | value | 300 | 96% [94,98] | 3% | -0.11 [-0.19,-0.05] | - | - | not_needed |
| RL | lookup | both | band48-63 | value | 300 | 3% [2,6] | 93% | -9.23 [-9.62,-8.84] | - | +97 [+95,+99] | needed |
| RL | lookup | both | band52-55 | value | 300 | 38% [33,44] | 61% | -2.45 [-2.70,-2.18] | - | +62 [+57,+67] | needed |
| RL | lookup | both | band56-59 | value | 300 | 99% [98,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | both | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | all | value | 300 | 3% [2,6] | 93% | -9.25 [-9.64,-8.84] | - | +97 [+94,+99] | needed |
| RL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band32-35 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | band36-39 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | band48-51 | value | 300 | 97% [94,98] | 3% | -0.11 [-0.17,-0.05] | - | - | not_needed |
| RL | lookup | final | band48-63 | value | 300 | 3% [2,6] | 93% | -9.22 [-9.61,-8.83] | - | +97 [+95,+99] | needed |
| RL | lookup | final | band52-55 | value | 300 | 37% [32,43] | 61% | -2.52 [-2.79,-2.26] | - | +63 [+57,+68] | needed |
| RL | lookup | final | band56-59 | value | 300 | 99% [98,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | final | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | all | value | 300 | 32% [27,37] | 18% | -3.26 [-3.57,-2.95] | - | +67 [+61,+72] | needed |
| RL | lookup | question | band00-03 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup | question | band00-31 | value | 300 | 98% [96,99] | 2% | -0.05 [-0.09,-0.01] | - | - | not_needed |
| RL | lookup | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band16-19 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.03,-0.00] | - | - | not_needed |
| RL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band28-31 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup | question | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band32-47 | value | 300 | 34% [29,40] | 23% | -3.02 [-3.33,-2.73] | - | +65 [+59,+70] | needed |
| RL | lookup | question | band36-39 | value | 300 | 92% [88,94] | 5% | -0.31 [-0.45,-0.19] | - | +8 [+5,+12] | partial |
| RL | lookup | question | band40-43 | value | 300 | 75% [70,80] | 11% | -1.07 [-1.32,-0.85] | - | +25 [+20,+30] | needed |
| RL | lookup | question | band44-47 | value | 300 | 92% [88,94] | 8% | -0.26 [-0.39,-0.16] | - | +8 [+5,+12] | partial |
| RL | lookup | question | band48-51 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 99% [97,99] | 1% | -0.07 [-0.16,-0.01] | - | - | not_needed |
| RL | lookup_off | both | all | value | 300 | 99% [98,100] | 1% | -0.01 [-0.04,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band00-31 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band32-47 | value | 300 | 99% [97,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band36-39 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band40-43 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band40-43 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 99% [97,99] | 1% | -0.03 [-0.07,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-31 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band32-35 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band32-47 | value | 300 | 99% [97,100] | 1% | -0.02 [-0.04,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band36-39 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band40-43 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band48-51 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | all | value | 300 | 100% [98,100] | 0% | -0.02 [-0.06,+0.01] | - | - | not_needed |
| RL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | both | band32-35 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band32-47 | value | 300 | 99% [98,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | random | both | band36-39 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band40-43 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band48-51 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | both | band48-63 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | both | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | all | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band48-51 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band48-63 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | all | value | 300 | 99% [98,100] | 1% | -0.01 [-0.04,+0.00] | - | - | not_needed |
| RL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band32-35 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band32-47 | value | 300 | 99% [98,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | random | question | band36-39 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band40-43 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band48-51 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band60-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | trailing | after | all | value | 235 | 97% [93,98] | 3% | -0.09 [-0.16,-0.04] | - | - | not_needed |
| RL | trailing | both | all | value | 235 | 100% [98,100] | 0% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| RL | trailing | final | all | value | 235 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | trailing | question | all | value | 235 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| DL | lookup | after | all | value | 300 | 31% [26,36] | 1% | -3.08 [-3.38,-2.78] | - | +69 [+64,+74] | needed |
| DL | lookup | both | all | value | 300 | 14% [11,19] | 2% | -4.20 [-4.48,-3.92] | - | +86 [+82,+90] | needed |
| DL | lookup | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band00-31 | value | 300 | 91% [87,93] | 0% | -0.34 [-0.46,-0.23] | - | +9 [+6,+13] | partial |
| DL | lookup | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | both | band32-35 | value | 300 | 99% [98,100] | 0% | -0.03 [-0.08,-0.00] | - | - | not_needed |
| DL | lookup | both | band32-47 | value | 300 | 11% [8,15] | 5% | -5.19 [-5.47,-4.89] | - | +89 [+85,+92] | needed |
| DL | lookup | both | band36-39 | value | 300 | 97% [94,98] | 0% | -0.19 [-0.32,-0.08] | - | - | not_needed |
| DL | lookup | both | band40-43 | value | 300 | 99% [97,100] | 1% | -0.05 [-0.12,-0.00] | - | - | not_needed |
| DL | lookup | both | band44-47 | value | 300 | 94% [90,96] | 6% | -0.36 [-0.56,-0.19] | - | - | not_needed |
| DL | lookup | both | band48-51 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band48-63 | value | 300 | 3% [2,6] | 95% | -12.97 [-13.33,-12.58] | - | +97 [+95,+99] | needed |
| DL | lookup | both | band52-55 | value | 300 | 42% [36,47] | 58% | -3.21 [-3.59,-2.81] | - | +58 [+53,+64] | needed |
| DL | lookup | both | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | all | value | 300 | 3% [2,6] | 95% | -12.71 [-13.06,-12.34] | - | +97 [+95,+99] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band48-51 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band48-63 | value | 300 | 3% [2,6] | 95% | -12.90 [-13.25,-12.52] | - | +97 [+95,+99] | needed |
| DL | lookup | final | band52-55 | value | 300 | 40% [34,45] | 60% | -3.53 [-3.92,-3.12] | - | +60 [+55,+66] | needed |
| DL | lookup | final | band56-59 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | all | value | 300 | 4% [2,7] | 1% | -7.22 [-7.48,-6.95] | - | +96 [+94,+98] | needed |
| DL | lookup | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band00-31 | value | 300 | 91% [87,94] | 0% | -0.33 [-0.45,-0.23] | - | +9 [+6,+12] | partial |
| DL | lookup | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band32-35 | value | 300 | 99% [98,100] | 0% | -0.03 [-0.08,-0.00] | - | - | not_needed |
| DL | lookup | question | band32-47 | value | 300 | 11% [8,15] | 5% | -5.32 [-5.61,-5.01] | - | +89 [+85,+92] | needed |
| DL | lookup | question | band36-39 | value | 300 | 97% [94,98] | 0% | -0.19 [-0.32,-0.08] | - | - | not_needed |
| DL | lookup | question | band40-43 | value | 300 | 99% [97,100] | 1% | -0.05 [-0.12,-0.00] | - | - | not_needed |
| DL | lookup | question | band44-47 | value | 300 | 95% [92,97] | 5% | -0.31 [-0.50,-0.15] | - | - | not_needed |
| DL | lookup | question | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band52-55 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band44-47 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band32-35 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band36-39 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band40-43 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band44-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band48-51 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band52-55 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band56-59 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band60-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | trailing | after | all | value | 235 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | trailing | both | all | value | 235 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | trailing | final | all | value | 235 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | trailing | question | all | value | 235 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
