# attn_knockout / d2_v4_late_read

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}, "DL": {"items": 300, "unedited_right": 300}, "RR": {"items": 300, "unedited_right": 300}})

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
     "acc": 0.087,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.087,
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
     "acc": 0.843,
     "verdict": "partial"
    },
    "band32-47:attn": {
     "acc": 0.837,
     "verdict": "partial"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.167,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.153,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.9,
    "verdict": "partial"
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
     "acc": 0.12,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.113,
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
     "acc": 0.057,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.083,
    "verdict": "needed"
   },
   "late_attention_read": true,
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
     "acc": 0.993,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 0.99,
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
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band32-47:attn": {
     "acc": 0.997,
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
    "acc": 0.953,
    "verdict": "not_needed"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  }
 },
 "C1a_RL_breaks_RR_survives": {
  "RL": "needed",
  "RR": "partial",
  "holds": false
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
   "both": "partial",
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
  "RL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
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
  "DL/lookup/question": {
   "windows_needed": [
    "band00-31",
    "band00-31:attn"
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
| RL | lookup | after | all | absent | 300 | 1% [0,3] | 98% | -4.97 [-5.17,-4.76] | 0.98 | +99 [+98,+100] | needed |
| RL | lookup | after | all | value | 300 | 1% [0,2] | 98% | -4.90 [-5.09,-4.71] | 0.94 | +99 [+98,+100] | needed |
| RL | lookup | both | all | absent | 300 | 4% [2,7] | 93% | -4.73 [-4.95,-4.53] | 0.99 | +96 [+94,+98] | needed |
| RL | lookup | both | all | value | 300 | 4% [2,7] | 94% | -4.78 [-5.00,-4.57] | 0.97 | +96 [+94,+98] | needed |
| RL | lookup | both | attn | value | 300 | 6% [4,9] | 92% | -5.01 [-5.26,-4.78] | - | +94 [+92,+97] | needed |
| RL | lookup | both | band00-31 | value | 300 | 96% [93,97] | 4% | -0.17 [-0.23,-0.12] | 0.97 | - | not_needed |
| RL | lookup | both | band00-31:attn | value | 300 | 95% [92,97] | 5% | -0.21 [-0.32,-0.12] | - | - | not_needed |
| RL | lookup | both | band00-31:gdn | value | 300 | 100% [98,100] | 0% | -0.01 [-0.03,-0.01] | 0.97 | - | not_needed |
| RL | lookup | both | band32-47 | value | 300 | 42% [36,47] | 58% | -1.25 [-1.37,-1.14] | 0.97 | +58 [+53,+64] | needed |
| RL | lookup | both | band32-47:attn | value | 300 | 42% [37,48] | 58% | -1.24 [-1.36,-1.13] | - | +58 [+53,+64] | needed |
| RL | lookup | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | both | band48-63 | value | 300 | 8% [5,12] | 91% | -6.71 [-7.01,-6.42] | 0.98 | +92 [+89,+95] | needed |
| RL | lookup | both | band48-63:attn | value | 300 | 7% [5,11] | 92% | -6.72 [-7.00,-6.43] | - | +93 [+90,+96] | needed |
| RL | lookup | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | both | gdn | value | 300 | 100% [98,100] | 0% | -0.01 [-0.03,-0.01] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 300 | 9% [6,12] | 88% | -4.21 [-4.44,-4.00] | 0.98 | +91 [+88,+95] | needed |
| RL | lookup | final | attn | value | 300 | 9% [6,12] | 88% | -4.17 [-4.39,-3.96] | - | +91 [+88,+95] | needed |
| RL | lookup | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band32-47 | value | 300 | 84% [80,88] | 16% | -0.40 [-0.46,-0.35] | 0.99 | +16 [+12,+20] | partial |
| RL | lookup | final | band32-47:attn | value | 300 | 84% [79,87] | 16% | -0.41 [-0.47,-0.35] | - | +16 [+12,+20] | partial |
| RL | lookup | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band48-63 | value | 300 | 17% [13,21] | 83% | -4.21 [-4.48,-3.94] | 0.99 | +83 [+79,+87] | needed |
| RL | lookup | final | band48-63:attn | value | 300 | 15% [12,20] | 84% | -4.22 [-4.49,-3.95] | - | +85 [+81,+89] | needed |
| RL | lookup | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 90% [86,93] | 10% | -0.36 [-0.42,-0.30] | 0.97 | +10 [+7,+14] | partial |
| RL | lookup | question | attn | value | 300 | 89% [85,92] | 11% | -0.43 [-0.54,-0.32] | - | +11 [+8,+15] | partial |
| RL | lookup | question | band00-31 | value | 300 | 97% [94,98] | 3% | -0.14 [-0.19,-0.10] | 0.96 | - | not_needed |
| RL | lookup | question | band00-31:attn | value | 300 | 95% [92,97] | 5% | -0.18 [-0.27,-0.11] | - | - | not_needed |
| RL | lookup | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.01 [-0.02,-0.01] | 0.96 | - | not_needed |
| RL | lookup | question | band32-47 | value | 300 | 99% [97,99] | 1% | -0.06 [-0.09,-0.04] | 0.96 | - | not_needed |
| RL | lookup | question | band32-47:attn | value | 300 | 98% [96,99] | 2% | -0.06 [-0.09,-0.04] | - | - | not_needed |
| RL | lookup | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | gdn | value | 300 | 100% [99,100] | 0% | -0.01 [-0.02,-0.01] | 0.97 | - | not_needed |
| RL | lookup_off | after | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | - | not_needed |
| RL | lookup_off | both | all | absent | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | after | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | random | after | all | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,+0.00] | 0.94 | - | not_needed |
| RL | random | both | all | absent | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | both | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | random | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | random | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | trailing | after | all | absent | 300 | 97% [95,99] | 3% | -0.11 [-0.14,-0.08] | 0.99 | - | not_needed |
| RL | trailing | after | all | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.00] | 0.96 | - | not_needed |
| RL | trailing | both | all | absent | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | trailing | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | trailing | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | trailing | question | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | after | all | absent | 300 | 23% [19,28] | 4% | -2.48 [-2.66,-2.32] | 0.98 | +77 [+72,+81] | needed |
| DL | lookup | after | all | value | 300 | 24% [19,29] | 5% | -2.42 [-2.58,-2.26] | 0.94 | +76 [+72,+81] | needed |
| DL | lookup | both | all | absent | 300 | 21% [17,26] | 6% | -2.63 [-2.82,-2.45] | 0.99 | +79 [+74,+84] | needed |
| DL | lookup | both | all | value | 300 | 20% [16,25] | 6% | -2.64 [-2.82,-2.46] | 0.97 | +80 [+75,+84] | needed |
| DL | lookup | both | attn | value | 300 | 17% [13,22] | 12% | -2.95 [-3.16,-2.75] | - | +83 [+79,+87] | needed |
| DL | lookup | both | band00-31 | value | 300 | 17% [13,22] | 1% | -3.35 [-3.56,-3.12] | 0.97 | +83 [+79,+87] | needed |
| DL | lookup | both | band00-31:attn | value | 300 | 42% [36,47] | 0% | -2.38 [-2.63,-2.14] | - | +58 [+52,+64] | needed |
| DL | lookup | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band32-47 | value | 300 | 93% [90,95] | 7% | -0.24 [-0.35,-0.13] | 0.97 | +7 [+4,+10] | partial |
| DL | lookup | both | band32-47:attn | value | 300 | 94% [90,96] | 6% | -0.25 [-0.36,-0.14] | - | - | not_needed |
| DL | lookup | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band48-63 | value | 300 | 4% [3,7] | 96% | -8.21 [-8.49,-7.94] | 0.98 | +96 [+93,+98] | needed |
| DL | lookup | both | band48-63:attn | value | 300 | 4% [3,7] | 96% | -8.26 [-8.54,-8.00] | - | +96 [+93,+98] | needed |
| DL | lookup | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | final | all | value | 300 | 12% [9,16] | 81% | -4.91 [-5.22,-4.61] | 0.98 | +88 [+84,+92] | needed |
| DL | lookup | final | attn | value | 300 | 11% [8,15] | 81% | -4.84 [-5.15,-4.54] | - | +89 [+85,+92] | needed |
| DL | lookup | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band48-63 | value | 300 | 6% [4,9] | 94% | -6.52 [-6.77,-6.29] | 0.99 | +94 [+92,+97] | needed |
| DL | lookup | final | band48-63:attn | value | 300 | 5% [3,8] | 95% | -6.59 [-6.84,-6.36] | - | +95 [+93,+97] | needed |
| DL | lookup | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | all | value | 300 | 8% [6,12] | 1% | -3.80 [-3.98,-3.61] | 0.96 | +92 [+88,+95] | needed |
| DL | lookup | question | attn | value | 300 | 18% [14,23] | 1% | -3.53 [-3.75,-3.30] | - | +82 [+77,+86] | needed |
| DL | lookup | question | band00-31 | value | 300 | 17% [13,22] | 1% | -3.35 [-3.56,-3.12] | 0.96 | +83 [+79,+87] | needed |
| DL | lookup | question | band00-31:attn | value | 300 | 42% [36,47] | 0% | -2.38 [-2.62,-2.14] | - | +58 [+52,+64] | needed |
| DL | lookup | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band32-47 | value | 300 | 99% [97,99] | 1% | -0.05 [-0.09,-0.01] | 0.96 | - | not_needed |
| DL | lookup | question | band32-47:attn | value | 300 | 99% [97,99] | 1% | -0.05 [-0.10,-0.02] | - | - | not_needed |
| DL | lookup | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | after | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| DL | lookup_off | both | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | random | after | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| DL | random | both | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | both | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | both | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | final | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | trailing | after | all | absent | 300 | 97% [94,98] | 3% | -0.12 [-0.15,-0.10] | 0.99 | - | not_needed |
| DL | trailing | after | all | value | 300 | 100% [99,100] | 0% | -0.02 [-0.02,-0.01] | 0.95 | - | not_needed |
| DL | trailing | both | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DL | trailing | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | trailing | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | trailing | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | after | all | absent | 300 | 94% [90,96] | 6% | -0.16 [-0.22,-0.12] | 0.98 | - | not_needed |
| RR | lookup | after | all | value | 300 | 94% [91,96] | 6% | -0.15 [-0.20,-0.10] | 0.95 | - | not_needed |
| RR | lookup | both | all | absent | 300 | 94% [90,96] | 6% | -0.16 [-0.21,-0.11] | 0.99 | - | not_needed |
| RR | lookup | both | all | value | 300 | 93% [90,96] | 7% | -0.16 [-0.21,-0.11] | 0.98 | +6 [+4,+9] | partial |
| RR | lookup | both | attn | value | 300 | 94% [91,96] | 6% | -0.13 [-0.17,-0.09] | - | - | not_needed |
| RR | lookup | both | band00-31 | value | 300 | 95% [92,97] | 5% | -0.09 [-0.12,-0.06] | 0.97 | - | not_needed |
| RR | lookup | both | band00-31:attn | value | 300 | 98% [96,99] | 2% | -0.06 [-0.09,-0.04] | - | - | not_needed |
| RR | lookup | both | band00-31:gdn | value | 300 | 99% [97,100] | 1% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR | lookup | both | band32-47 | value | 300 | 97% [94,98] | 3% | -0.05 [-0.07,-0.04] | 0.97 | - | not_needed |
| RR | lookup | both | band32-47:attn | value | 300 | 96% [94,98] | 4% | -0.05 [-0.07,-0.04] | - | - | not_needed |
| RR | lookup | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | band48-63 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| RR | lookup | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | gdn | value | 300 | 99% [97,100] | 1% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR | lookup | final | all | value | 300 | 99% [98,100] | 1% | -0.04 [-0.05,-0.02] | 0.99 | - | not_needed |
| RR | lookup | final | attn | value | 300 | 99% [97,100] | 1% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR | lookup | final | band00-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band32-47 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | 0.99 | - | not_needed |
| RR | lookup | final | band32-47:attn | value | 300 | 100% [98,100] | 0% | -0.02 [-0.02,-0.01] | - | - | not_needed |
| RR | lookup | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | question | all | value | 300 | 95% [92,97] | 5% | -0.11 [-0.15,-0.08] | 0.97 | - | not_needed |
| RR | lookup | question | attn | value | 300 | 96% [94,98] | 4% | -0.09 [-0.12,-0.06] | - | - | not_needed |
| RR | lookup | question | band00-31 | value | 300 | 96% [94,98] | 4% | -0.08 [-0.11,-0.05] | 0.97 | - | not_needed |
| RR | lookup | question | band00-31:attn | value | 300 | 98% [96,99] | 2% | -0.05 [-0.08,-0.03] | - | - | not_needed |
| RR | lookup | question | band00-31:gdn | value | 300 | 99% [98,100] | 1% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR | lookup | question | band32-47 | value | 300 | 99% [97,100] | 1% | -0.03 [-0.03,-0.02] | 0.97 | - | not_needed |
| RR | lookup | question | band32-47:attn | value | 300 | 99% [98,100] | 1% | -0.03 [-0.03,-0.02] | - | - | not_needed |
| RR | lookup | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | gdn | value | 300 | 99% [98,100] | 1% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR | lookup_off | after | all | absent | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | not_needed |
| RR | lookup_off | both | all | absent | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | all | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band00-31 | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band00-31:gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band32-47 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | band32-47:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | gdn | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | after | all | absent | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RR | random | after | all | value | 300 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.95 | - | not_needed |
| RR | random | both | all | absent | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| RR | random | both | all | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | random | both | band00-31 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | both | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | random | both | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | both | band32-47 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band32-47:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band32-47:gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band48-63 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band48-63:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | random | final | band00-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | random | final | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band32-47 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band32-47:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band48-63:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | question | all | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | random | question | band00-31 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | band00-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | random | question | band00-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | band32-47 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | band32-47:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | band32-47:gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | band48-63 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band48-63:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | band48-63:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | trailing | after | all | absent | 300 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | trailing | after | all | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 0.96 | - | not_needed |
| RR | trailing | both | all | absent | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | trailing | both | all | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR | trailing | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | trailing | question | all | value | 300 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
