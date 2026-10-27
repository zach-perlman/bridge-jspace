# attn_knockout / d2_pointer_late_read

Measure: correct (items: {"RL": {"items": 175, "unedited_right": 175}, "DL": {"items": 175, "unedited_right": 175}, "RR": {"items": 175, "unedited_right": 175}})

Claims: {
 "positive_control": {
  "RL": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "DL": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  }
 },
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.114,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.114,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    },
    "band00-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    },
    "band32-47": {
     "acc": 0.869,
     "verdict": "partial"
    },
    "band32-47:attn": {
     "acc": 0.857,
     "verdict": "partial"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.194,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.194,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.88,
    "verdict": "partial"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RR": {
   "path": false,
   "final": {
    "all": {
     "acc": 0.989,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 0.994,
     "verdict": "not_needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.989,
    "verdict": "not_needed"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "DL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.131,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.126,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-31:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.114,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.114,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.011,
    "verdict": "needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  }
 },
 "C1a_RL_breaks_RR_survives": {
  "RL": "needed",
  "RR": "not_needed",
  "holds": true
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": null,
   "question": null
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
   "question": "not_needed",
   "final": "not_needed",
   "both": "not_needed",
   "after": "not_needed"
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
  "RL/lookup/final": {
   "windows_needed": [
    "band48-63",
    "band48-63:attn"
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
    "band32-47",
    "band32-47:attn",
    "band48-63",
    "band48-63:attn"
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
    "band48-63",
    "band48-63:attn"
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
    "band00-31",
    "band00-31:attn",
    "band48-63",
    "band48-63:attn"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
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
| RL | lookup | after | all | absent | 175 | 1% [0,3] | 98% | -5.57 [-5.79,-5.34] | 0.98 | +98 [+95,+99] | needed |
| RL | lookup | after | all | value | 175 | 0% [0,2] | 100% | -5.31 [-5.54,-5.08] | 0.95 | +97 [+94,+99] | needed |
| RL | lookup | both | all | absent | 175 | 6% [4,11] | 93% | -4.96 [-5.25,-4.68] | 0.99 | +93 [+89,+97] | needed |
| RL | lookup | both | all | value | 175 | 5% [2,9] | 94% | -4.97 [-5.24,-4.70] | 0.97 | +95 [+91,+98] | needed |
| RL | lookup | both | attn | value | 175 | 9% [5,14] | 90% | -5.18 [-5.51,-4.87] | - | +91 [+86,+95] | needed |
| RL | lookup | both | band00-31 | value | 175 | 89% [84,93] | 11% | -0.28 [-0.35,-0.21] | 0.97 | +10 [+6,+15] | partial |
| RL | lookup | both | band00-31:attn | value | 175 | 93% [88,96] | 7% | -0.28 [-0.40,-0.19] | - | +7 [+3,+11] | partial |
| RL | lookup | both | band00-31:gdn | value | 175 | 99% [96,100] | 1% | -0.03 [-0.04,-0.01] | 0.97 | - | not_needed |
| RL | lookup | both | band32-47 | value | 175 | 45% [37,52] | 55% | -1.17 [-1.29,-1.05] | 0.97 | +55 [+47,+63] | needed |
| RL | lookup | both | band32-47:attn | value | 175 | 44% [37,51] | 56% | -1.16 [-1.29,-1.04] | - | +56 [+49,+63] | needed |
| RL | lookup | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | band48-63 | value | 175 | 13% [8,18] | 86% | -5.82 [-6.20,-5.41] | 0.98 | +87 [+82,+92] | needed |
| RL | lookup | both | band48-63:attn | value | 175 | 13% [8,18] | 86% | -5.91 [-6.28,-5.50] | - | +87 [+82,+92] | needed |
| RL | lookup | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | both | gdn | value | 175 | 99% [96,100] | 1% | -0.03 [-0.05,-0.01] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 175 | 11% [8,17] | 86% | -4.31 [-4.60,-4.01] | 0.98 | +88 [+83,+93] | needed |
| RL | lookup | final | attn | value | 175 | 11% [8,17] | 87% | -4.31 [-4.60,-4.01] | - | +88 [+83,+93] | needed |
| RL | lookup | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | band00-31:gdn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band32-47 | value | 175 | 87% [81,91] | 13% | -0.36 [-0.45,-0.29] | 0.99 | +13 [+9,+18] | partial |
| RL | lookup | final | band32-47:attn | value | 175 | 86% [80,90] | 14% | -0.37 [-0.45,-0.29] | - | +14 [+9,+20] | partial |
| RL | lookup | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band48-63 | value | 175 | 19% [14,26] | 79% | -3.81 [-4.14,-3.46] | 0.99 | +81 [+74,+86] | needed |
| RL | lookup | final | band48-63:attn | value | 175 | 19% [14,26] | 78% | -3.85 [-4.18,-3.51] | - | +81 [+74,+86] | needed |
| RL | lookup | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | gdn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 175 | 88% [82,92] | 12% | -0.44 [-0.51,-0.36] | 0.97 | +11 [+7,+16] | partial |
| RL | lookup_off | after | all | absent | 175 | 98% [95,99] | 2% | -0.03 [-0.05,-0.01] | 0.98 | - | not_needed |
| RL | lookup_off | after | all | value | 175 | 97% [93,98] | 3% | -0.05 [-0.08,-0.03] | 0.95 | - | not_needed |
| RL | lookup_off | both | all | absent | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | both | all | value | 175 | 99% [97,100] | 1% | -0.00 [-0.02,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.02,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-31 | value | 175 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band00-31:attn | value | 175 | 99% [97,100] | 1% | -0.01 [-0.02,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-31:gdn | value | 175 | 99% [97,100] | 1% | -0.02 [-0.04,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | gdn | value | 175 | 99% [96,100] | 1% | -0.02 [-0.04,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 175 | 99% [97,100] | 1% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band00-31 | value | 175 | 99% [97,100] | 1% | -0.01 [-0.04,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | band00-31:attn | value | 175 | 99% [97,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-31:gdn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | gdn | value | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 175 | 99% [97,100] | 1% | -0.01 [-0.03,-0.00] | 0.97 | - | not_needed |
| RL | random | after | all | absent | 175 | 97% [93,99] | 3% | -0.04 [-0.07,-0.02] | 0.99 | - | not_needed |
| RL | random | after | all | value | 175 | 97% [93,99] | 3% | -0.05 [-0.08,-0.02] | 0.94 | - | not_needed |
| RL | random | both | all | absent | 175 | 100% [98,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| RL | random | both | all | value | 175 | 99% [97,100] | 1% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| RL | random | both | attn | value | 175 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | random | both | band00-31 | value | 175 | 99% [97,100] | 1% | -0.01 [-0.03,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | random | both | band00-31:gdn | value | 175 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | gdn | value | 175 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| RL | random | final | all | value | 175 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | attn | value | 175 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | random | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | random | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | question | all | value | 175 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RL | trailing | after | all | absent | 175 | 97% [93,98] | 3% | -0.13 [-0.17,-0.10] | 0.99 | - | not_needed |
| RL | trailing | after | all | value | 175 | 100% [98,100] | 0% | -0.03 [-0.04,-0.02] | 0.96 | - | not_needed |
| RL | trailing | both | all | absent | 175 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| RL | trailing | both | all | value | 175 | 99% [97,100] | 1% | -0.02 [-0.03,-0.01] | 0.98 | - | not_needed |
| RL | trailing | final | all | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RL | trailing | question | all | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RR | lookup | after | all | absent | 175 | 96% [92,98] | 4% | -0.14 [-0.18,-0.10] | 0.98 | - | not_needed |
| RR | lookup | after | all | value | 175 | 98% [94,99] | 2% | -0.11 [-0.15,-0.08] | 0.95 | - | not_needed |
| RR | lookup | both | all | absent | 175 | 96% [92,98] | 4% | -0.12 [-0.16,-0.09] | 0.99 | - | not_needed |
| RR | lookup | both | all | value | 175 | 96% [92,98] | 4% | -0.12 [-0.16,-0.09] | 0.97 | - | not_needed |
| RR | lookup | both | attn | value | 175 | 98% [95,99] | 2% | -0.09 [-0.13,-0.06] | - | - | not_needed |
| RR | lookup | both | band00-31 | value | 175 | 99% [97,100] | 1% | -0.04 [-0.06,-0.03] | 0.97 | - | not_needed |
| RR | lookup | both | band00-31:attn | value | 175 | 99% [97,100] | 1% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR | lookup | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | band32-47 | value | 175 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | 0.97 | - | not_needed |
| RR | lookup | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | - | - | not_needed |
| RR | lookup | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | band48-63 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | 0.98 | - | not_needed |
| RR | lookup | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RR | lookup | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | gdn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | 0.97 | - | not_needed |
| RR | lookup | final | all | value | 175 | 99% [96,100] | 1% | -0.04 [-0.05,-0.03] | 0.99 | - | not_needed |
| RR | lookup | final | attn | value | 175 | 99% [97,100] | 1% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR | lookup | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| RR | lookup | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | final | band32-47 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band48-63 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RR | lookup | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | question | all | value | 175 | 99% [96,100] | 1% | -0.05 [-0.07,-0.03] | 0.97 | - | not_needed |
| RR | lookup_off | after | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | after | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | not_needed |
| RR | lookup_off | both | all | absent | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup_off | both | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | both | band00-31 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band00-31:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | lookup_off | final | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band00-31 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | question | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | after | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | random | after | all | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | not_needed |
| RR | random | both | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | random | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | random | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | final | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band32-47 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | random | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | question | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | trailing | after | all | absent | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | trailing | after | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | - | not_needed |
| RR | trailing | both | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| RR | trailing | both | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR | trailing | final | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | trailing | question | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | after | all | absent | 175 | 14% [10,20] | 0% | -2.71 [-2.97,-2.48] | 0.98 | +86 [+81,+91] | needed |
| DL | lookup | after | all | value | 175 | 14% [9,20] | 0% | -2.70 [-2.94,-2.48] | 0.94 | +86 [+81,+91] | needed |
| DL | lookup | both | all | absent | 175 | 17% [12,23] | 0% | -2.69 [-2.94,-2.44] | 0.99 | +83 [+77,+88] | needed |
| DL | lookup | both | all | value | 175 | 15% [10,21] | 0% | -2.70 [-2.95,-2.45] | 0.97 | +85 [+80,+90] | needed |
| DL | lookup | both | attn | value | 175 | 15% [11,22] | 0% | -2.74 [-2.99,-2.51] | - | +85 [+79,+90] | needed |
| DL | lookup | both | band00-31 | value | 175 | 1% [0,3] | 5% | -4.88 [-5.06,-4.70] | 0.97 | +99 [+98,+100] | needed |
| DL | lookup | both | band00-31:attn | value | 175 | 3% [2,7] | 5% | -4.53 [-4.77,-4.30] | - | +97 [+94,+99] | needed |
| DL | lookup | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band32-47 | value | 175 | 98% [94,99] | 2% | -0.08 [-0.11,-0.05] | 0.97 | - | not_needed |
| DL | lookup | both | band32-47:attn | value | 175 | 97% [93,99] | 3% | -0.09 [-0.13,-0.06] | - | - | not_needed |
| DL | lookup | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band48-63 | value | 175 | 11% [8,17] | 89% | -7.94 [-8.38,-7.47] | 0.98 | +89 [+83,+93] | needed |
| DL | lookup | both | band48-63:attn | value | 175 | 11% [8,17] | 89% | -7.99 [-8.43,-7.52] | - | +89 [+83,+93] | needed |
| DL | lookup | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | final | all | value | 175 | 13% [9,19] | 83% | -4.48 [-4.83,-4.11] | 0.98 | +87 [+82,+91] | needed |
| DL | lookup | final | attn | value | 175 | 13% [8,18] | 83% | -4.51 [-4.87,-4.14] | - | +87 [+82,+92] | needed |
| DL | lookup | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band32-47 | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | 0.98 | - | not_needed |
| DL | lookup | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| DL | lookup | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band48-63 | value | 175 | 11% [8,17] | 89% | -6.03 [-6.39,-5.63] | 0.99 | +89 [+83,+93] | needed |
| DL | lookup | final | band48-63:attn | value | 175 | 11% [8,17] | 89% | -6.11 [-6.47,-5.71] | - | +89 [+83,+93] | needed |
| DL | lookup | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | all | value | 175 | 1% [0,4] | 5% | -4.86 [-5.02,-4.69] | 0.96 | +99 [+97,+100] | needed |
| DL | lookup_off | after | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | after | all | value | 175 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | not_needed |
| DL | lookup_off | both | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | lookup_off | both | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | final | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | lookup_off | question | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | after | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | after | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| DL | random | both | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | both | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | both | band00-31:attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | both | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | final | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | attn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-31 | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | final | band00-31:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-31:gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | final | band32-47 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band32-47:attn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band32-47:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band48-63 | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band48-63:attn | value | 175 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band48-63:gdn | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | gdn | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | question | all | value | 175 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | trailing | after | all | absent | 175 | 85% [79,90] | 15% | -0.38 [-0.48,-0.30] | 0.99 | - | partial |
| DL | trailing | after | all | value | 175 | 100% [98,100] | 0% | -0.03 [-0.05,-0.02] | 0.95 | - | not_needed |
| DL | trailing | both | all | absent | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DL | trailing | both | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | trailing | final | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | trailing | question | all | value | 175 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
