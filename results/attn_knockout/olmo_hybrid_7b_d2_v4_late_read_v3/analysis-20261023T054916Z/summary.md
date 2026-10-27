# attn_knockout / olmo_hybrid_7b_d2_v4_late_read_v3

Measure: correct (items: {"DL": {"items": 300, "unedited_right": 300}, "RL": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.07,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.08,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band00-15:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15:gdn": {
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
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band16-19": {
     "acc": 0.71,
     "verdict": "needed"
    },
    "band16-23": {
     "acc": 0.18,
     "verdict": "needed"
    },
    "band16-23:attn": {
     "acc": 0.15,
     "verdict": "needed"
    },
    "band16-23:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 0.99,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band24-31:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band24-31:gdn": {
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
     "acc": 0.047,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.077,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15:gdn": {
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
    "band16-19": {
     "acc": 0.97,
     "verdict": "not_needed"
    },
    "band16-23": {
     "acc": 0.287,
     "verdict": "needed"
    },
    "band16-23:attn": {
     "acc": 0.283,
     "verdict": "needed"
    },
    "band16-23:gdn": {
     "acc": 1.0,
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
    "band24-31:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band24-31:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band28-31": {
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
  "DL/lookup/question": {
   "windows_needed": [
    "band00-15",
    "band00-15:attn",
    "band08-11"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/final": {
   "windows_needed": [
    "band16-23",
    "band16-23:attn"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/both": {
   "windows_needed": [
    "band00-15",
    "band00-15:attn",
    "band16-23",
    "band16-23:attn",
    "band08-11"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/question": {
   "windows_needed": [
    "band00-15",
    "band00-15:attn",
    "band00-15:gdn",
    "band08-11"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn",
    "gdn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/final": {
   "windows_needed": [
    "band16-23",
    "band16-23:attn",
    "band16-19"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/both": {
   "windows_needed": [
    "band00-15",
    "band00-15:attn",
    "band00-15:gdn",
    "band16-23",
    "band16-23:attn",
    "band08-11",
    "band16-19"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn",
    "gdn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | after | all | value | 100 | 5% [2,11] | 40% | -3.25 [-3.51,-2.99] | 0.98 | +78 [+69,+86] | needed |
| RL | lookup | both | all | value | 100 | 6% [3,12] | 43% | -3.31 [-3.60,-3.02] | 0.98 | +91 [+85,+96] | needed |
| RL | lookup | both | attn | value | 100 | 5% [2,11] | 67% | -4.57 [-5.10,-4.06] | - | +94 [+89,+98] | needed |
| RL | lookup | both | band00-03 | value | 100 | 99% [95,100] | 0% | -0.03 [-0.09,+0.01] | 0.99 | - | not_needed |
| RL | lookup | both | band00-15 | value | 100 | 20% [13,29] | 27% | -3.15 [-3.53,-2.78] | 0.98 | +75 [+67,+83] | needed |
| RL | lookup | both | band00-15:attn | value | 100 | 37% [28,47] | 47% | -3.18 [-3.78,-2.59] | - | +62 [+53,+71] | needed |
| RL | lookup | both | band00-15:gdn | value | 100 | 67% [57,75] | 12% | -1.11 [-1.43,-0.79] | 0.98 | +30 [+21,+39] | needed |
| RL | lookup | both | band04-07 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.04,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | band08-11 | value | 100 | 17% [11,26] | 25% | -3.39 [-3.79,-2.98] | 0.97 | +82 [+74,+89] | needed |
| RL | lookup | both | band12-15 | value | 100 | 83% [74,89] | 15% | -0.75 [-1.12,-0.39] | 0.96 | +16 [+9,+23] | partial |
| RL | lookup | both | band16-19 | value | 100 | 73% [64,81] | 16% | -0.84 [-1.12,-0.58] | 0.97 | +27 [+19,+36] | needed |
| RL | lookup | both | band16-23 | value | 100 | 17% [11,26] | 63% | -3.17 [-3.60,-2.76] | 0.97 | +83 [+75,+90] | needed |
| RL | lookup | both | band16-23:attn | value | 100 | 15% [9,23] | 67% | -3.20 [-3.63,-2.78] | - | +85 [+78,+92] | needed |
| RL | lookup | both | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.02,+0.01] | 0.97 | - | not_needed |
| RL | lookup | both | band20-23 | value | 100 | 99% [95,100] | 1% | -0.05 [-0.12,-0.01] | 0.98 | - | not_needed |
| RL | lookup | both | band24-27 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | band24-31 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup | both | band24-31:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | both | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | gdn | value | 100 | 69% [59,77] | 10% | -1.03 [-1.34,-0.73] | 0.98 | +28 [+20,+37] | needed |
| RL | lookup | final | all | value | 100 | 7% [3,14] | 71% | -5.18 [-5.68,-4.70] | 0.99 | +92 [+86,+97] | needed |
| RL | lookup | final | attn | value | 100 | 8% [4,15] | 73% | -4.98 [-5.46,-4.51] | - | +91 [+85,+96] | needed |
| RL | lookup | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup | final | band00-15 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band00-15:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-15:gdn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band12-15 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band16-19 | value | 100 | 71% [61,79] | 18% | -0.87 [-1.16,-0.61] | 0.99 | +29 [+20,+38] | needed |
| RL | lookup | final | band16-23 | value | 100 | 18% [12,27] | 62% | -3.21 [-3.63,-2.79] | 0.98 | +82 [+75,+89] | needed |
| RL | lookup | final | band16-23:attn | value | 100 | 15% [9,23] | 67% | -3.23 [-3.66,-2.81] | - | +85 [+78,+92] | needed |
| RL | lookup | final | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL | lookup | final | band20-23 | value | 100 | 99% [95,100] | 1% | -0.05 [-0.12,-0.01] | 0.99 | - | not_needed |
| RL | lookup | final | band24-27 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band24-31 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup | final | band24-31:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band28-31 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | gdn | value | 100 | 99% [95,100] | 1% | -0.01 [-0.05,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 100 | 21% [14,30] | 31% | -3.15 [-3.53,-2.78] | 0.98 | +75 [+66,+83] | needed |
| RL | lookup | question | attn | value | 100 | 35% [26,45] | 49% | -3.24 [-3.84,-2.65] | - | +64 [+55,+73] | needed |
| RL | lookup | question | band00-03 | value | 100 | 99% [95,100] | 0% | -0.03 [-0.09,+0.01] | 0.99 | - | not_needed |
| RL | lookup | question | band00-15 | value | 100 | 20% [13,29] | 31% | -3.17 [-3.55,-2.79] | 0.97 | +76 [+67,+84] | needed |
| RL | lookup | question | band00-15:attn | value | 100 | 35% [26,45] | 49% | -3.24 [-3.84,-2.64] | - | +64 [+55,+73] | needed |
| RL | lookup | question | band00-15:gdn | value | 100 | 72% [63,80] | 12% | -1.06 [-1.38,-0.75] | 0.97 | +25 [+17,+33] | needed |
| RL | lookup | question | band04-07 | value | 100 | 99% [95,100] | 0% | -0.02 [-0.05,-0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band08-11 | value | 100 | 19% [13,28] | 24% | -3.39 [-3.79,-2.97] | 0.96 | +80 [+72,+88] | needed |
| RL | lookup | question | band12-15 | value | 100 | 84% [76,90] | 14% | -0.71 [-1.08,-0.37] | 0.96 | +15 [+8,+22] | partial |
| RL | lookup | question | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band16-23:attn | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band24-27 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band24-31:attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-31:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | gdn | value | 100 | 73% [64,81] | 13% | -1.03 [-1.35,-0.73] | 0.98 | +24 [+16,+32] | needed |
| RL | lookup_off | after | all | value | 100 | 83% [74,89] | 10% | -0.55 [-0.87,-0.29] | 0.98 | - | partial |
| RL | lookup_off | both | all | value | 100 | 97% [92,99] | 3% | -0.14 [-0.32,-0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | attn | value | 100 | 99% [95,100] | 1% | -0.02 [-0.06,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 100 | 99% [95,100] | 1% | -0.03 [-0.08,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | both | band00-15 | value | 100 | 95% [89,98] | 5% | -0.17 [-0.36,-0.03] | 0.98 | - | partial |
| RL | lookup_off | both | band00-15:attn | value | 100 | 99% [95,100] | 1% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band00-15:gdn | value | 100 | 97% [92,99] | 3% | -0.11 [-0.28,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 100 | 99% [95,100] | 1% | -0.02 [-0.06,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band16-23 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band16-23:attn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band24-31:attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band24-31:gdn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | both | gdn | value | 100 | 97% [92,99] | 3% | -0.11 [-0.28,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | all | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 100 | 99% [95,100] | 1% | -0.00 [-0.02,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | band00-15 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band00-15:attn | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band00-15:gdn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band16-23 | value | 100 | 100% [96,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band16-23:attn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | final | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-31:attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band24-31:gdn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | gdn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 96% [90,98] | 4% | -0.17 [-0.35,-0.02] | 0.98 | - | not_needed |
| RL | lookup_off | question | attn | value | 100 | 99% [95,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 100 | 99% [95,100] | 1% | -0.02 [-0.07,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | band00-15 | value | 100 | 96% [90,98] | 4% | -0.17 [-0.35,-0.02] | 0.98 | - | not_needed |
| RL | lookup_off | question | band00-15:attn | value | 100 | 99% [95,100] | 1% | -0.01 [-0.04,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-15:gdn | value | 100 | 97% [92,99] | 3% | -0.11 [-0.28,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.02,+0.01] | 0.96 | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.04,+0.01] | 0.96 | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band16-23 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band16-23:attn | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-23:gdn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-31:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | gdn | value | 100 | 97% [92,99] | 3% | -0.10 [-0.28,+0.00] | 0.98 | - | not_needed |
| RL | random | after | all | value | 100 | 94% [88,97] | 2% | -0.21 [-0.45,-0.05] | 0.97 | - | partial |
| RL | random | both | all | value | 100 | 99% [95,100] | 1% | -0.05 [-0.16,+0.02] | 0.98 | - | not_needed |
| RL | random | both | attn | value | 100 | 99% [95,100] | 1% | +0.00 [-0.02,+0.02] | - | - | not_needed |
| RL | random | both | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | 1.00 | - | not_needed |
| RL | random | both | band00-15 | value | 100 | 99% [95,100] | 1% | -0.04 [-0.14,+0.02] | 0.98 | - | not_needed |
| RL | random | both | band00-15:attn | value | 100 | 99% [95,100] | 1% | +0.00 [-0.02,+0.02] | - | - | not_needed |
| RL | random | both | band00-15:gdn | value | 100 | 100% [96,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| RL | random | both | band04-07 | value | 100 | 100% [96,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | both | band08-11 | value | 100 | 100% [96,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | not_needed |
| RL | random | both | band12-15 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | both | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band16-23:attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band24-31:gdn | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | gdn | value | 100 | 100% [96,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | not_needed |
| RL | random | final | all | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL | random | final | attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | random | final | band00-15 | value | 100 | 99% [95,100] | 1% | -0.01 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band00-15:attn | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | final | band00-15:gdn | value | 100 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band04-07 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RL | random | final | band08-11 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band12-15 | value | 100 | 99% [95,100] | 1% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-23:attn | value | 100 | 100% [96,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | final | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band24-31:gdn | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | random | question | all | value | 100 | 99% [95,100] | 1% | -0.04 [-0.15,+0.02] | 0.98 | - | not_needed |
| RL | random | question | attn | value | 100 | 99% [95,100] | 1% | +0.00 [-0.02,+0.02] | - | - | not_needed |
| RL | random | question | band00-03 | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | 1.00 | - | not_needed |
| RL | random | question | band00-15 | value | 100 | 99% [95,100] | 1% | -0.04 [-0.14,+0.02] | 0.98 | - | not_needed |
| RL | random | question | band00-15:attn | value | 100 | 99% [95,100] | 1% | +0.00 [-0.02,+0.02] | - | - | not_needed |
| RL | random | question | band00-15:gdn | value | 100 | 100% [96,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| RL | random | question | band04-07 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | question | band08-11 | value | 100 | 100% [96,100] | 0% | +0.01 [-0.01,+0.02] | 0.97 | - | not_needed |
| RL | random | question | band12-15 | value | 100 | 100% [96,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RL | random | question | band16-19 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band16-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band16-23:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-23:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band20-23 | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band24-27 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band24-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | band24-31:attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | question | band24-31:gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | band28-31 | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | gdn | value | 100 | 100% [96,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| RL | trailing | after | all | value | 79 | 97% [91,99] | 1% | -0.10 [-0.24,-0.02] | 0.97 | - | not_needed |
| RL | trailing | both | all | value | 79 | 99% [93,100] | 1% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | trailing | final | all | value | 79 | 100% [95,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| RL | trailing | question | all | value | 79 | 99% [93,100] | 1% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| DL | lookup | after | all | value | 300 | 19% [15,24] | 7% | -2.60 [-2.77,-2.44] | 0.98 | +80 [+75,+84] | needed |
| DL | lookup | both | all | value | 300 | 14% [11,18] | 5% | -2.94 [-3.11,-2.77] | 0.98 | +86 [+82,+90] | needed |
| DL | lookup | both | attn | value | 300 | 10% [7,14] | 23% | -4.08 [-4.39,-3.78] | - | +90 [+87,+93] | needed |
| DL | lookup | both | band00-03 | value | 300 | 99% [97,100] | 0% | -0.05 [-0.11,-0.00] | 0.99 | - | not_needed |
| DL | lookup | both | band00-15 | value | 300 | 4% [2,6] | 4% | -5.48 [-5.71,-5.25] | 0.98 | +96 [+94,+98] | needed |
| DL | lookup | both | band00-15:attn | value | 300 | 12% [9,16] | 17% | -5.45 [-5.81,-5.10] | - | +88 [+84,+92] | needed |
| DL | lookup | both | band00-15:gdn | value | 300 | 92% [88,95] | 1% | -0.42 [-0.60,-0.26] | 0.98 | +8 [+5,+11] | partial |
| DL | lookup | both | band04-07 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.03,-0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band08-11 | value | 300 | 46% [40,51] | 9% | -3.17 [-3.56,-2.78] | 0.97 | +54 [+49,+60] | needed |
| DL | lookup | both | band12-15 | value | 300 | 82% [77,86] | 18% | -1.32 [-1.70,-0.98] | 0.96 | +18 [+14,+23] | partial |
| DL | lookup | both | band16-19 | value | 300 | 96% [93,97] | 4% | -0.18 [-0.31,-0.08] | 0.97 | - | not_needed |
| DL | lookup | both | band16-23 | value | 300 | 23% [19,28] | 76% | -4.27 [-4.65,-3.89] | 0.97 | +77 [+72,+82] | needed |
| DL | lookup | both | band16-23:attn | value | 300 | 24% [19,29] | 75% | -4.19 [-4.56,-3.81] | - | +76 [+71,+81] | needed |
| DL | lookup | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band20-23 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.06,-0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | gdn | value | 300 | 93% [89,95] | 1% | -0.38 [-0.55,-0.23] | 0.98 | +7 [+5,+10] | partial |
| DL | lookup | final | all | value | 300 | 5% [3,8] | 89% | -8.27 [-8.66,-7.87] | 0.99 | +95 [+93,+98] | needed |
| DL | lookup | final | attn | value | 300 | 8% [5,11] | 87% | -7.56 [-7.97,-7.14] | - | +92 [+89,+95] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DL | lookup | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 97% [94,98] | 3% | -0.15 [-0.27,-0.06] | 0.98 | - | not_needed |
| DL | lookup | final | band16-23 | value | 300 | 29% [24,34] | 70% | -3.72 [-4.09,-3.36] | 0.98 | +71 [+66,+77] | needed |
| DL | lookup | final | band16-23:attn | value | 300 | 28% [24,34] | 70% | -3.69 [-4.05,-3.33] | - | +72 [+67,+77] | needed |
| DL | lookup | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band20-23 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.06,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | question | all | value | 300 | 4% [2,7] | 5% | -5.52 [-5.75,-5.28] | 0.97 | +96 [+94,+98] | needed |
| DL | lookup | question | attn | value | 300 | 12% [9,16] | 16% | -5.53 [-5.89,-5.18] | - | +88 [+85,+92] | needed |
| DL | lookup | question | band00-03 | value | 300 | 99% [97,100] | 0% | -0.05 [-0.11,-0.00] | 0.99 | - | not_needed |
| DL | lookup | question | band00-15 | value | 300 | 4% [2,7] | 5% | -5.53 [-5.77,-5.31] | 0.97 | +96 [+94,+98] | needed |
| DL | lookup | question | band00-15:attn | value | 300 | 12% [9,16] | 16% | -5.52 [-5.89,-5.18] | - | +88 [+85,+92] | needed |
| DL | lookup | question | band00-15:gdn | value | 300 | 92% [89,95] | 1% | -0.41 [-0.58,-0.25] | 0.97 | +8 [+5,+11] | partial |
| DL | lookup | question | band04-07 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band08-11 | value | 300 | 44% [39,50] | 10% | -3.21 [-3.60,-2.82] | 0.96 | +56 [+50,+61] | needed |
| DL | lookup | question | band12-15 | value | 300 | 83% [78,87] | 17% | -1.20 [-1.57,-0.87] | 0.95 | +17 [+13,+22] | partial |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | gdn | value | 300 | 93% [89,95] | 1% | -0.39 [-0.56,-0.24] | 0.97 | +7 [+5,+10] | partial |
| DL | lookup_off | after | all | value | 300 | 99% [98,100] | 1% | -0.07 [-0.17,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DL | lookup_off | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | after | all | value | 300 | 99% [98,100] | 1% | -0.01 [-0.03,-0.00] | 0.97 | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DL | random | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | trailing | after | all | value | 239 | 99% [96,100] | 1% | -0.03 [-0.09,-0.00] | 0.97 | - | not_needed |
| DL | trailing | both | all | value | 239 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | trailing | final | all | value | 239 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DL | trailing | question | all | value | 239 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
