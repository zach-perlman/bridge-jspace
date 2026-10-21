# attn_knockout / d2_code_late_read

Measure: correct (items: {"DK": {"items": 120, "unedited_right": 120}, "IX": {"items": 120, "unedited_right": 120}, "CH2": {"items": 120, "unedited_right": 120}, "CH3": {"items": 120, "unedited_right": 120}, "RK": {"items": 60, "unedited_right": 60}})

Claims: {
 "positive_control": {
  "DK": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "IX": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "CH2": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "CH3": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "RK": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  }
 },
 "late_attention_read": {
  "DK": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.467,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.475,
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
     "acc": 0.5,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.5,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.058,
    "verdict": "needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "IX": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.358,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.342,
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
     "acc": 0.35,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.358,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 1.0,
    "verdict": "not_needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "CH2": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.417,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.425,
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
     "acc": 0.358,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.35,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 1.0,
    "verdict": "not_needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "CH3": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.325,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.325,
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
     "acc": 0.342,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.342,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 1.0,
    "verdict": "not_needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RK": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.267,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.25,
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
     "acc": 0.783,
     "verdict": "needed"
    },
    "band32-47:attn": {
     "acc": 0.767,
     "verdict": "needed"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.367,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.35,
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
  "DK/lookup/final": {
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
  "DK/lookup/both": {
   "windows_needed": [
    "band00-31",
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
  "IX/lookup/final": {
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
  "IX/lookup/both": {
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
  "CH2/lookup/final": {
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
  "CH2/lookup/both": {
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
  "CH3/lookup/final": {
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
  "CH3/lookup/both": {
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
  "RK/lookup/final": {
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
  "RK/lookup/both": {
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
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DK | lookup | after | all | absent | 120 | 4% [2,9] | 19% | -3.54 [-3.73,-3.34] | 0.99 | +96 [+92,+99] | needed |
| DK | lookup | after | all | value | 120 | 3% [1,8] | 23% | -3.43 [-3.61,-3.24] | 0.96 | +97 [+93,+99] | needed |
| DK | lookup | both | all | absent | 120 | 2% [1,7] | 11% | -3.42 [-3.61,-3.23] | 1.00 | +98 [+94,+100] | needed |
| DK | lookup | both | all | value | 120 | 0% [-0,3] | 8% | -3.49 [-3.68,-3.29] | 0.99 | +100 [+100,+100] | needed |
| DK | lookup | both | attn | value | 120 | 2% [1,7] | 18% | -3.31 [-3.48,-3.12] | - | +98 [+94,+100] | needed |
| DK | lookup | both | band00-31 | value | 120 | 52% [44,61] | 3% | -1.30 [-1.44,-1.17] | 0.99 | +48 [+38,+57] | needed |
| DK | lookup | both | band00-31:attn | value | 120 | 80% [72,86] | 2% | -0.74 [-0.85,-0.63] | - | +20 [+13,+28] | partial |
| DK | lookup | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DK | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup | both | band48-63 | value | 120 | 42% [33,51] | 57% | -3.42 [-4.01,-2.86] | 0.99 | +58 [+50,+68] | needed |
| DK | lookup | both | band48-63:attn | value | 120 | 42% [33,51] | 57% | -3.43 [-4.02,-2.86] | - | +58 [+50,+68] | needed |
| DK | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup | final | all | value | 120 | 47% [38,56] | 47% | -2.50 [-2.95,-2.04] | 1.00 | +53 [+45,+62] | needed |
| DK | lookup | final | attn | value | 120 | 48% [39,56] | 47% | -2.52 [-2.97,-2.07] | - | +52 [+44,+62] | needed |
| DK | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DK | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup | final | band48-63 | value | 120 | 50% [41,59] | 48% | -1.92 [-2.33,-1.53] | 1.00 | +50 [+42,+59] | needed |
| DK | lookup | final | band48-63:attn | value | 120 | 50% [41,59] | 48% | -1.96 [-2.37,-1.57] | - | +50 [+42,+59] | needed |
| DK | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup | question | all | value | 120 | 6% [3,12] | 3% | -2.35 [-2.49,-2.21] | 0.99 | +94 [+89,+98] | needed |
| DK | lookup_off | after | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DK | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DK | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | random | after | all | absent | 120 | 98% [94,100] | 2% | -0.03 [-0.07,-0.00] | 0.99 | - | not_needed |
| DK | random | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.01] | 0.97 | - | not_needed |
| DK | random | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | random | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | random | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DK | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | random | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | random | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | random | final | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DK | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DK | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DK | random | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | random | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | trailing | after | all | absent | 120 | 79% [71,85] | 21% | -0.51 [-0.68,-0.35] | 0.99 | - | breaks (control) |
| DK | trailing | after | all | value | 120 | 100% [97,100] | 0% | -0.04 [-0.05,-0.03] | 0.97 | - | not_needed |
| DK | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | trailing | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| IX | lookup | after | all | absent | 120 | 5% [2,10] | 68% | -3.84 [-4.08,-3.60] | 0.99 | +95 [+91,+98] | needed |
| IX | lookup | after | all | value | 120 | 5% [2,10] | 68% | -3.74 [-3.98,-3.51] | 0.97 | +95 [+91,+98] | needed |
| IX | lookup | both | all | absent | 120 | 34% [26,43] | 64% | -3.60 [-4.15,-3.06] | 1.00 | +66 [+57,+74] | needed |
| IX | lookup | both | all | value | 120 | 35% [27,44] | 62% | -3.59 [-4.14,-3.05] | 1.00 | +65 [+57,+73] | needed |
| IX | lookup | both | attn | value | 120 | 34% [26,43] | 63% | -3.59 [-4.15,-3.05] | - | +66 [+57,+74] | needed |
| IX | lookup | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | both | band48-63 | value | 120 | 34% [26,43] | 65% | -3.76 [-4.34,-3.22] | 1.00 | +66 [+57,+74] | needed |
| IX | lookup | both | band48-63:attn | value | 120 | 34% [26,43] | 65% | -3.79 [-4.38,-3.24] | - | +66 [+57,+74] | needed |
| IX | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | final | all | value | 120 | 36% [28,45] | 61% | -3.40 [-3.93,-2.89] | 1.00 | +64 [+56,+72] | needed |
| IX | lookup | final | attn | value | 120 | 34% [26,43] | 63% | -3.43 [-3.96,-2.91] | - | +66 [+57,+74] | needed |
| IX | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | final | band48-63 | value | 120 | 35% [27,44] | 64% | -3.42 [-3.96,-2.94] | 1.00 | +65 [+57,+73] | needed |
| IX | lookup | final | band48-63:attn | value | 120 | 36% [28,45] | 63% | -3.46 [-4.00,-2.97] | - | +64 [+56,+72] | needed |
| IX | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | after | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | 0.99 | - | not_needed |
| IX | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | 0.97 | - | not_needed |
| IX | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup_off | both | band00-31 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | lookup_off | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| IX | random | after | all | absent | 120 | 99% [95,100] | 1% | -0.02 [-0.05,-0.01] | 0.99 | - | not_needed |
| IX | random | after | all | value | 120 | 100% [97,100] | 0% | -0.02 [-0.03,-0.02] | 0.97 | - | not_needed |
| IX | random | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | final | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| IX | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| IX | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | random | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | trailing | after | all | absent | 120 | 88% [81,93] | 12% | -0.27 [-0.36,-0.19] | 0.99 | - | partial |
| IX | trailing | after | all | value | 120 | 100% [97,100] | 0% | -0.06 [-0.07,-0.05] | 0.97 | - | not_needed |
| IX | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| IX | trailing | both | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| IX | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| CH2 | lookup | after | all | absent | 120 | 2% [0,6] | 85% | -5.32 [-5.69,-4.94] | 0.99 | +98 [+96,+100] | needed |
| CH2 | lookup | after | all | value | 120 | 2% [0,6] | 87% | -5.32 [-5.67,-4.96] | 0.97 | +98 [+96,+100] | needed |
| CH2 | lookup | both | all | absent | 120 | 38% [29,46] | 61% | -3.67 [-4.26,-3.09] | 1.00 | +62 [+54,+71] | needed |
| CH2 | lookup | both | all | value | 120 | 38% [29,46] | 60% | -3.66 [-4.26,-3.07] | 1.00 | +62 [+54,+71] | needed |
| CH2 | lookup | both | attn | value | 120 | 40% [32,49] | 57% | -3.63 [-4.23,-3.04] | - | +60 [+52,+68] | needed |
| CH2 | lookup | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH2 | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | both | band48-63 | value | 120 | 35% [27,44] | 63% | -3.66 [-4.23,-3.09] | 1.00 | +65 [+57,+73] | needed |
| CH2 | lookup | both | band48-63:attn | value | 120 | 35% [27,44] | 63% | -3.68 [-4.26,-3.11] | - | +65 [+57,+73] | needed |
| CH2 | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | all | value | 120 | 42% [33,51] | 56% | -3.28 [-3.83,-2.73] | 1.00 | +58 [+50,+67] | needed |
| CH2 | lookup | final | attn | value | 120 | 42% [34,51] | 56% | -3.29 [-3.85,-2.74] | - | +57 [+49,+67] | needed |
| CH2 | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH2 | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | band48-63 | value | 120 | 36% [28,45] | 62% | -3.09 [-3.59,-2.58] | 1.00 | +64 [+56,+72] | needed |
| CH2 | lookup | final | band48-63:attn | value | 120 | 35% [27,44] | 63% | -3.11 [-3.62,-2.61] | - | +65 [+57,+73] | needed |
| CH2 | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | after | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| CH2 | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| CH2 | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | after | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| CH2 | random | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | 0.98 | - | not_needed |
| CH2 | random | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | random | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | random | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH2 | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH2 | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | random | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | trailing | after | all | absent | 120 | 71% [62,78] | 29% | -0.74 [-0.97,-0.54] | 0.99 | - | breaks (control) |
| CH2 | trailing | after | all | value | 120 | 98% [94,100] | 2% | -0.09 [-0.13,-0.06] | 0.97 | - | not_needed |
| CH2 | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | trailing | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| CH3 | lookup | after | all | absent | 120 | 2% [1,7] | 95% | -6.27 [-6.60,-5.94] | 0.99 | +97 [+93,+99] | needed |
| CH3 | lookup | after | all | value | 120 | 2% [0,6] | 96% | -6.14 [-6.46,-5.81] | 0.97 | +98 [+96,+100] | needed |
| CH3 | lookup | both | all | absent | 120 | 32% [25,41] | 67% | -3.97 [-4.57,-3.40] | 1.00 | +68 [+59,+76] | needed |
| CH3 | lookup | both | all | value | 120 | 32% [25,41] | 67% | -3.99 [-4.59,-3.42] | 1.00 | +68 [+59,+76] | needed |
| CH3 | lookup | both | attn | value | 120 | 32% [25,41] | 67% | -3.93 [-4.52,-3.36] | - | +68 [+59,+76] | needed |
| CH3 | lookup | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | lookup | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | both | band48-63 | value | 120 | 33% [26,42] | 66% | -4.01 [-4.59,-3.44] | 1.00 | +67 [+58,+75] | needed |
| CH3 | lookup | both | band48-63:attn | value | 120 | 33% [26,42] | 66% | -4.03 [-4.61,-3.45] | - | +67 [+58,+75] | needed |
| CH3 | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | all | value | 120 | 32% [25,41] | 67% | -3.78 [-4.33,-3.23] | 1.00 | +68 [+59,+76] | needed |
| CH3 | lookup | final | attn | value | 120 | 32% [25,41] | 67% | -3.77 [-4.33,-3.21] | - | +67 [+58,+75] | needed |
| CH3 | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | band48-63 | value | 120 | 34% [26,43] | 65% | -3.73 [-4.26,-3.18] | 1.00 | +66 [+57,+74] | needed |
| CH3 | lookup | final | band48-63:attn | value | 120 | 34% [26,43] | 65% | -3.75 [-4.29,-3.21] | - | +66 [+57,+74] | needed |
| CH3 | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | after | all | absent | 120 | 99% [95,100] | 1% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | - | not_needed |
| CH3 | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| CH3 | lookup_off | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| CH3 | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| CH3 | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | attn | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| CH3 | lookup_off | final | band00-31 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | band00-31:attn | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| CH3 | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| CH3 | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | after | all | absent | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | not_needed |
| CH3 | random | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,+0.01] | 0.98 | - | not_needed |
| CH3 | random | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH3 | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH3 | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| CH3 | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| CH3 | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | random | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | trailing | after | all | absent | 120 | 69% [60,77] | 31% | -0.95 [-1.20,-0.72] | 0.99 | - | breaks (control) |
| CH3 | trailing | after | all | value | 120 | 93% [87,97] | 7% | -0.18 [-0.27,-0.11] | 0.98 | - | partial |
| CH3 | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| CH3 | trailing | both | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| CH3 | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| CH3 | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup | after | all | absent | 60 | 3% [1,11] | 95% | -5.12 [-5.61,-4.59] | 0.99 | +97 [+92,+100] | needed |
| RK | lookup | after | all | value | 60 | 3% [1,11] | 93% | -4.84 [-5.28,-4.35] | 0.96 | +95 [+88,+100] | needed |
| RK | lookup | both | all | absent | 60 | 3% [1,11] | 95% | -4.90 [-5.36,-4.42] | 1.00 | +97 [+92,+100] | needed |
| RK | lookup | both | all | value | 60 | 3% [1,11] | 95% | -4.83 [-5.29,-4.37] | 0.99 | +97 [+92,+100] | needed |
| RK | lookup | both | attn | value | 60 | 3% [1,11] | 97% | -5.13 [-5.65,-4.62] | - | +97 [+92,+100] | needed |
| RK | lookup | both | band00-31 | value | 60 | 93% [84,97] | 7% | -0.13 [-0.20,-0.07] | 0.99 | +7 [+2,+13] | partial |
| RK | lookup | both | band00-31:attn | value | 60 | 88% [78,94] | 12% | -0.26 [-0.43,-0.11] | - | +12 [+5,+20] | partial |
| RK | lookup | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RK | lookup | both | band32-47 | value | 60 | 72% [59,81] | 28% | -0.65 [-0.81,-0.49] | 0.99 | +28 [+17,+40] | needed |
| RK | lookup | both | band32-47:attn | value | 60 | 72% [59,81] | 28% | -0.62 [-0.77,-0.46] | - | +28 [+17,+40] | needed |
| RK | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | lookup | both | band48-63 | value | 60 | 25% [16,37] | 75% | -5.26 [-6.14,-4.41] | 0.99 | +75 [+63,+87] | needed |
| RK | lookup | both | band48-63:attn | value | 60 | 25% [16,37] | 75% | -5.28 [-6.16,-4.42] | - | +75 [+63,+87] | needed |
| RK | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RK | lookup | final | all | value | 60 | 27% [17,39] | 73% | -3.65 [-4.27,-3.05] | 1.00 | +73 [+63,+85] | needed |
| RK | lookup | final | attn | value | 60 | 25% [16,37] | 75% | -3.60 [-4.22,-2.99] | - | +75 [+65,+85] | needed |
| RK | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup | final | band32-47 | value | 60 | 78% [66,87] | 22% | -0.47 [-0.61,-0.34] | 0.99 | +22 [+12,+32] | needed |
| RK | lookup | final | band32-47:attn | value | 60 | 77% [65,86] | 23% | -0.46 [-0.60,-0.33] | - | +23 [+13,+33] | needed |
| RK | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RK | lookup | final | band48-63 | value | 60 | 37% [26,49] | 63% | -3.15 [-3.80,-2.49] | 1.00 | +63 [+52,+75] | needed |
| RK | lookup | final | band48-63:attn | value | 60 | 35% [24,48] | 65% | -3.20 [-3.86,-2.53] | - | +65 [+53,+77] | needed |
| RK | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup | question | all | value | 60 | 90% [80,95] | 10% | -0.26 [-0.36,-0.16] | 0.99 | +10 [+3,+18] | partial |
| RK | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.03 [-0.06,-0.01] | 0.99 | - | not_needed |
| RK | lookup_off | after | all | value | 60 | 98% [91,100] | 2% | -0.04 [-0.07,-0.01] | 0.96 | - | not_needed |
| RK | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RK | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RK | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RK | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RK | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | not_needed |
| RK | random | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RK | random | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RK | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | random | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RK | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RK | random | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | trailing | after | all | absent | 60 | 82% [70,89] | 18% | -0.54 [-0.82,-0.30] | 0.99 | - | partial |
| RK | trailing | after | all | value | 60 | 98% [91,100] | 2% | -0.04 [-0.08,-0.02] | 0.97 | - | not_needed |
| RK | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RK | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
