# attn_knockout / d2_alias_late_read

Measure: correct (items: {"RL-same": {"items": 120, "unedited_right": 120}, "DL-same": {"items": 120, "unedited_right": 120}, "RR-same": {"items": 120, "unedited_right": 120}, "RL-xlang": {"items": 60, "unedited_right": 60}, "DL-xlang": {"items": 60, "unedited_right": 60}, "RR-xlang": {"items": 60, "unedited_right": 60}, "DL-syn": {"items": 60, "unedited_right": 60}, "RR-syn": {"items": 60, "unedited_right": 60}})

Claims: {
 "positive_control": {
  "RL-same": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "RL-xlang": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "DL-same": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "DL-syn": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  },
  "DL-xlang": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  }
 },
 "late_attention_read": {
  "RL-same": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.075,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.075,
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
     "acc": 0.792,
     "verdict": "needed"
    },
    "band32-47:attn": {
     "acc": 0.8,
     "verdict": "partial"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.108,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.117,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.867,
    "verdict": "partial"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RL-xlang": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.017,
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
     "acc": 0.75,
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
     "acc": 0.45,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.483,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.85,
    "verdict": "partial"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RR-same": {
   "path": false,
   "final": {
    "all": {
     "acc": 0.983,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 0.983,
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
    "acc": 0.992,
    "verdict": "not_needed"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RR-syn": {
   "path": false,
   "final": {
    "all": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 1.0,
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
    "acc": 1.0,
    "verdict": "not_needed"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "RR-xlang": {
   "path": false,
   "final": {
    "all": {
     "acc": 0.983,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 0.983,
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
    "acc": 0.983,
    "verdict": "not_needed"
   },
   "late_attention_read": false,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "DL-same": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.1,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.1,
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
     "acc": 0.075,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.075,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.008,
    "verdict": "needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "DL-syn": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.0,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.0,
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
     "acc": 0.95,
     "verdict": "partial"
    },
    "band32-47:attn": {
     "acc": 0.967,
     "verdict": "partial"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.0,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.0,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.267,
    "verdict": "needed"
   },
   "late_attention_read": true,
   "bands": {
    "early": "band00-31",
    "middle": "band32-47",
    "late": "band48-63"
   }
  },
  "DL-xlang": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.05,
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
     "acc": 0.883,
     "verdict": "partial"
    },
    "band32-47:attn": {
     "acc": 0.883,
     "verdict": "partial"
    },
    "band32-47:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band48-63": {
     "acc": 0.067,
     "verdict": "needed"
    },
    "band48-63:attn": {
     "acc": 0.067,
     "verdict": "needed"
    },
    "band48-63:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.0,
    "verdict": "needed"
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
  "RL-same/lookup/final": {
   "windows_needed": [
    "band32-47",
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
  "RL-same/lookup/both": {
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
  "DL-same/lookup/final": {
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
  "DL-same/lookup/both": {
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
  "RR-same/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR-same/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL-xlang/lookup/final": {
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
  "RL-xlang/lookup/both": {
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
  "DL-xlang/lookup/final": {
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
  "DL-xlang/lookup/both": {
   "windows_needed": [
    "band00-31",
    "band00-31:attn",
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
  "RR-xlang/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR-xlang/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL-syn/lookup/final": {
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
  "DL-syn/lookup/both": {
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
  "RR-syn/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR-syn/lookup/both": {
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
| RL-same | lookup | after | all | absent | 120 | 0% [-0,3] | 99% | -5.40 [-5.66,-5.14] | 0.98 | +94 [+90,+98] | needed |
| RL-same | lookup | after | all | value | 120 | 0% [-0,3] | 98% | -5.09 [-5.36,-4.83] | 0.95 | +96 [+92,+99] | needed |
| RL-same | lookup | both | all | absent | 120 | 2% [0,6] | 94% | -4.89 [-5.19,-4.60] | 0.99 | +98 [+96,+100] | needed |
| RL-same | lookup | both | all | value | 120 | 2% [1,7] | 93% | -4.89 [-5.19,-4.61] | 0.97 | +97 [+93,+99] | needed |
| RL-same | lookup | both | attn | value | 120 | 2% [0,6] | 96% | -5.23 [-5.55,-4.91] | - | +98 [+94,+100] | needed |
| RL-same | lookup | both | band00-31 | value | 120 | 89% [82,94] | 11% | -0.25 [-0.32,-0.19] | 0.97 | +10 [+5,+16] | partial |
| RL-same | lookup | both | band00-31:attn | value | 120 | 92% [85,95] | 8% | -0.24 [-0.38,-0.14] | - | +8 [+4,+13] | partial |
| RL-same | lookup | both | band00-31:gdn | value | 120 | 99% [95,100] | 1% | -0.02 [-0.04,-0.01] | 0.97 | - | not_needed |
| RL-same | lookup | both | band32-47 | value | 120 | 43% [35,52] | 57% | -1.18 [-1.34,-1.02] | 0.97 | +56 [+47,+64] | needed |
| RL-same | lookup | both | band32-47:attn | value | 120 | 43% [35,52] | 57% | -1.16 [-1.32,-1.00] | - | +56 [+47,+64] | needed |
| RL-same | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| RL-same | lookup | both | band48-63 | value | 120 | 8% [4,14] | 92% | -6.24 [-6.65,-5.80] | 0.98 | +92 [+88,+97] | needed |
| RL-same | lookup | both | band48-63:attn | value | 120 | 8% [4,14] | 92% | -6.31 [-6.71,-5.87] | - | +92 [+88,+97] | needed |
| RL-same | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL-same | lookup | both | gdn | value | 120 | 99% [95,100] | 1% | -0.03 [-0.05,-0.01] | 0.97 | - | not_needed |
| RL-same | lookup | final | all | value | 120 | 8% [4,14] | 90% | -4.55 [-4.84,-4.24] | 0.98 | +92 [+87,+96] | needed |
| RL-same | lookup | final | attn | value | 120 | 8% [4,14] | 89% | -4.57 [-4.86,-4.26] | - | +92 [+87,+96] | needed |
| RL-same | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL-same | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL-same | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL-same | lookup | final | band32-47 | value | 120 | 79% [71,85] | 21% | -0.45 [-0.55,-0.35] | 0.99 | +20 [+12,+28] | needed |
| RL-same | lookup | final | band32-47:attn | value | 120 | 80% [72,86] | 20% | -0.46 [-0.56,-0.36] | - | +19 [+12,+27] | partial |
| RL-same | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | lookup | final | band48-63 | value | 120 | 11% [6,18] | 88% | -4.25 [-4.60,-3.86] | 0.99 | +89 [+83,+94] | needed |
| RL-same | lookup | final | band48-63:attn | value | 120 | 12% [7,19] | 88% | -4.30 [-4.64,-3.91] | - | +88 [+82,+93] | needed |
| RL-same | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL-same | lookup | question | all | value | 120 | 87% [79,92] | 13% | -0.39 [-0.47,-0.32] | 0.97 | +12 [+7,+18] | partial |
| RL-same | lookup_off | after | all | absent | 120 | 94% [88,97] | 6% | -0.06 [-0.11,-0.02] | 0.98 | - | partial |
| RL-same | lookup_off | after | all | value | 120 | 96% [91,98] | 4% | -0.06 [-0.10,-0.02] | 0.95 | - | not_needed |
| RL-same | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | +0.01 [+0.00,+0.03] | 0.99 | - | not_needed |
| RL-same | lookup_off | both | all | value | 120 | 99% [95,100] | 1% | +0.01 [-0.00,+0.03] | 0.97 | - | not_needed |
| RL-same | lookup_off | both | attn | value | 120 | 99% [95,100] | 1% | +0.02 [+0.00,+0.03] | - | - | not_needed |
| RL-same | lookup_off | both | band00-31 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL-same | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL-same | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,+0.00] | 0.97 | - | not_needed |
| RL-same | lookup_off | both | band32-47 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL-same | lookup_off | both | band32-47:attn | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL-same | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-same | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.01 [+0.01,+0.02] | 0.98 | - | not_needed |
| RL-same | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.02 [+0.01,+0.03] | - | - | not_needed |
| RL-same | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-same | lookup_off | both | gdn | value | 120 | 99% [95,100] | 1% | -0.01 [-0.03,+0.00] | 0.97 | - | not_needed |
| RL-same | lookup_off | final | all | value | 120 | 99% [95,100] | 1% | +0.02 [+0.01,+0.04] | 0.99 | - | not_needed |
| RL-same | lookup_off | final | attn | value | 120 | 99% [95,100] | 1% | +0.02 [+0.00,+0.04] | - | - | not_needed |
| RL-same | lookup_off | final | band00-31 | value | 120 | 99% [95,100] | 1% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| RL-same | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL-same | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL-same | lookup_off | final | band32-47 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL-same | lookup_off | final | band32-47:attn | value | 120 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL-same | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.02 [+0.01,+0.03] | 0.99 | - | not_needed |
| RL-same | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL-same | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL-same | lookup_off | question | all | value | 120 | 99% [95,100] | 1% | -0.01 [-0.03,-0.00] | 0.97 | - | not_needed |
| RL-same | random | after | all | absent | 120 | 98% [93,99] | 2% | -0.03 [-0.05,-0.00] | 0.99 | - | not_needed |
| RL-same | random | after | all | value | 120 | 99% [95,100] | 1% | -0.03 [-0.05,-0.00] | 0.94 | - | not_needed |
| RL-same | random | both | all | absent | 120 | 100% [97,100] | 0% | +0.00 [-0.02,+0.02] | 0.99 | - | not_needed |
| RL-same | random | both | all | value | 120 | 99% [95,100] | 1% | +0.00 [-0.01,+0.02] | 0.98 | - | not_needed |
| RL-same | random | both | attn | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.03] | - | - | not_needed |
| RL-same | random | both | band00-31 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| RL-same | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL-same | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL-same | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL-same | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL-same | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-same | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RL-same | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL-same | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-same | random | both | gdn | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RL-same | random | final | all | value | 120 | 100% [97,100] | 0% | +0.01 [-0.01,+0.03] | 0.99 | - | not_needed |
| RL-same | random | final | attn | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL-same | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| RL-same | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL-same | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL-same | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL-same | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL-same | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| RL-same | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL-same | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-same | random | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RL-same | random | question | all | value | 120 | 99% [95,100] | 1% | -0.01 [-0.02,+0.01] | 0.97 | - | not_needed |
| RL-same | trailing | after | all | absent | 120 | 97% [92,99] | 3% | -0.11 [-0.16,-0.07] | 0.99 | - | not_needed |
| RL-same | trailing | after | all | value | 120 | 98% [93,99] | 2% | -0.03 [-0.05,-0.01] | 0.96 | - | not_needed |
| RL-same | trailing | both | all | absent | 120 | 99% [95,100] | 1% | -0.00 [-0.02,+0.01] | 1.00 | - | not_needed |
| RL-same | trailing | both | all | value | 120 | 98% [94,100] | 2% | -0.01 [-0.03,+0.00] | 0.98 | - | not_needed |
| RL-same | trailing | final | all | value | 120 | 99% [95,100] | 1% | +0.00 [-0.01,+0.02] | 0.99 | - | not_needed |
| RL-same | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,+0.01] | 0.98 | - | not_needed |
| RL-xlang | lookup | after | all | absent | 60 | 3% [1,11] | 82% | -3.60 [-3.98,-3.25] | 0.98 | +95 [+90,+100] | needed |
| RL-xlang | lookup | after | all | value | 60 | 2% [0,9] | 78% | -3.45 [-3.80,-3.14] | 0.94 | +98 [+95,+100] | needed |
| RL-xlang | lookup | both | all | absent | 60 | 2% [0,9] | 83% | -3.53 [-3.94,-3.18] | 0.99 | +98 [+95,+100] | needed |
| RL-xlang | lookup | both | all | value | 60 | 2% [0,9] | 82% | -3.48 [-3.87,-3.14] | 0.98 | +98 [+95,+100] | needed |
| RL-xlang | lookup | both | attn | value | 60 | 0% [-0,6] | 87% | -4.04 [-4.45,-3.67] | - | +100 [+100,+100] | needed |
| RL-xlang | lookup | both | band00-31 | value | 60 | 93% [84,97] | 7% | -0.37 [-0.48,-0.26] | 0.98 | +7 [+2,+13] | partial |
| RL-xlang | lookup | both | band00-31:attn | value | 60 | 88% [78,94] | 12% | -0.45 [-0.66,-0.27] | - | +12 [+5,+20] | partial |
| RL-xlang | lookup | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup | both | band32-47 | value | 60 | 32% [21,44] | 68% | -1.33 [-1.52,-1.14] | 0.97 | +68 [+57,+80] | needed |
| RL-xlang | lookup | both | band32-47:attn | value | 60 | 32% [21,44] | 68% | -1.32 [-1.49,-1.14] | - | +68 [+57,+80] | needed |
| RL-xlang | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-xlang | lookup | both | band48-63 | value | 60 | 0% [-0,6] | 100% | -6.67 [-7.08,-6.26] | 0.98 | +100 [+100,+100] | needed |
| RL-xlang | lookup | both | band48-63:attn | value | 60 | 0% [-0,6] | 100% | -6.72 [-7.13,-6.30] | - | +100 [+100,+100] | needed |
| RL-xlang | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup | final | all | value | 60 | 5% [2,14] | 90% | -2.94 [-3.19,-2.70] | 0.98 | +95 [+88,+100] | needed |
| RL-xlang | lookup | final | attn | value | 60 | 2% [0,9] | 90% | -2.94 [-3.16,-2.72] | - | +98 [+95,+100] | needed |
| RL-xlang | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup | final | band32-47 | value | 60 | 75% [63,84] | 25% | -0.74 [-0.85,-0.63] | 0.98 | +25 [+15,+37] | needed |
| RL-xlang | lookup | final | band32-47:attn | value | 60 | 77% [65,86] | 23% | -0.77 [-0.88,-0.66] | - | +23 [+13,+35] | needed |
| RL-xlang | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup | final | band48-63 | value | 60 | 45% [33,58] | 55% | -1.94 [-2.41,-1.50] | 0.98 | +55 [+42,+67] | needed |
| RL-xlang | lookup | final | band48-63:attn | value | 60 | 48% [36,61] | 52% | -2.00 [-2.47,-1.56] | - | +52 [+38,+63] | needed |
| RL-xlang | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup | question | all | value | 60 | 85% [74,92] | 13% | -0.76 [-0.94,-0.61] | 0.97 | +15 [+7,+25] | partial |
| RL-xlang | lookup_off | after | all | absent | 60 | 98% [91,100] | 2% | -0.04 [-0.12,-0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.02 [-0.04,-0.00] | 0.94 | - | not_needed |
| RL-xlang | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-xlang | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-xlang | lookup_off | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-xlang | lookup_off | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL-xlang | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL-xlang | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RL-xlang | random | after | all | absent | 60 | 93% [84,97] | 7% | -0.19 [-0.40,-0.03] | 0.99 | - | partial |
| RL-xlang | random | after | all | value | 60 | 92% [82,96] | 8% | -0.25 [-0.49,-0.07] | 0.94 | - | partial |
| RL-xlang | random | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| RL-xlang | random | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | random | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL-xlang | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL-xlang | trailing | after | all | absent | 60 | 98% [91,100] | 2% | -0.10 [-0.20,-0.04] | 0.99 | - | not_needed |
| RL-xlang | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.04 [-0.06,-0.02] | 0.95 | - | not_needed |
| RL-xlang | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL-xlang | trailing | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL-xlang | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup | after | all | absent | 120 | 98% [94,100] | 2% | -0.14 [-0.20,-0.09] | 0.98 | - | not_needed |
| RR-same | lookup | after | all | value | 120 | 96% [91,98] | 4% | -0.13 [-0.18,-0.09] | 0.95 | - | not_needed |
| RR-same | lookup | both | all | absent | 120 | 98% [93,99] | 2% | -0.10 [-0.14,-0.06] | 0.99 | - | not_needed |
| RR-same | lookup | both | all | value | 120 | 97% [92,99] | 3% | -0.11 [-0.16,-0.07] | 0.97 | - | not_needed |
| RR-same | lookup | both | attn | value | 120 | 98% [94,100] | 2% | -0.06 [-0.09,-0.04] | - | - | not_needed |
| RR-same | lookup | both | band00-31 | value | 120 | 99% [95,100] | 1% | -0.03 [-0.05,-0.02] | 0.97 | - | not_needed |
| RR-same | lookup | both | band00-31:attn | value | 120 | 99% [95,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RR-same | lookup | both | band00-31:gdn | value | 120 | 99% [95,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RR-same | lookup | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR-same | lookup | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RR-same | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR-same | lookup | both | band48-63 | value | 120 | 100% [97,100] | 0% | -0.02 [-0.02,-0.01] | 0.98 | - | not_needed |
| RR-same | lookup | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RR-same | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup | both | gdn | value | 120 | 99% [95,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RR-same | lookup | final | all | value | 120 | 98% [94,100] | 2% | -0.04 [-0.06,-0.02] | 0.99 | - | not_needed |
| RR-same | lookup | final | attn | value | 120 | 98% [94,100] | 2% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR-same | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| RR-same | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR-same | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR-same | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-same | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR-same | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup | final | band48-63 | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | 0.99 | - | not_needed |
| RR-same | lookup | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RR-same | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR-same | lookup | question | all | value | 120 | 99% [95,100] | 1% | -0.03 [-0.06,-0.02] | 0.97 | - | not_needed |
| RR-same | lookup_off | after | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | 0.95 | - | not_needed |
| RR-same | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR-same | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | both | band00-31 | value | 120 | 99% [95,100] | 1% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RR-same | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RR-same | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR-same | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR-same | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR-same | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR-same | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR-same | random | after | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RR-same | random | after | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.94 | - | not_needed |
| RR-same | random | both | all | absent | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| RR-same | random | both | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-same | random | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR-same | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-same | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR-same | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR-same | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | random | both | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-same | random | final | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-same | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | random | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RR-same | trailing | after | all | absent | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-same | trailing | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,+0.00] | 0.96 | - | not_needed |
| RR-same | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR-same | trailing | both | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-same | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-same | trailing | question | all | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-syn | lookup | after | all | absent | 60 | 97% [89,99] | 3% | -0.16 [-0.24,-0.10] | 0.98 | +3 [+0,+8] | partial |
| RR-syn | lookup | after | all | value | 60 | 95% [86,98] | 5% | -0.16 [-0.25,-0.08] | 0.94 | +5 [+0,+12] | partial |
| RR-syn | lookup | both | all | absent | 60 | 100% [94,100] | 0% | -0.06 [-0.09,-0.04] | 0.99 | - | not_needed |
| RR-syn | lookup | both | all | value | 60 | 100% [94,100] | 0% | -0.05 [-0.07,-0.02] | 0.98 | - | not_needed |
| RR-syn | lookup | both | attn | value | 60 | 100% [94,100] | 0% | -0.04 [-0.05,-0.02] | - | - | not_needed |
| RR-syn | lookup | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RR-syn | lookup | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RR-syn | lookup | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RR-syn | lookup | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RR-syn | lookup | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR-syn | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR-syn | lookup | both | band48-63 | value | 60 | 100% [94,100] | 0% | -0.03 [-0.04,-0.02] | 0.98 | - | not_needed |
| RR-syn | lookup | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR-syn | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-syn | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.01,+0.02] | 0.97 | - | not_needed |
| RR-syn | lookup | final | all | value | 60 | 100% [94,100] | 0% | -0.05 [-0.06,-0.03] | 0.99 | - | not_needed |
| RR-syn | lookup | final | attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.05,-0.02] | - | - | not_needed |
| RR-syn | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR-syn | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RR-syn | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | final | band48-63 | value | 60 | 100% [94,100] | 0% | -0.02 [-0.04,-0.01] | 0.99 | - | not_needed |
| RR-syn | lookup | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RR-syn | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup | question | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | 0.97 | - | not_needed |
| RR-syn | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| RR-syn | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | 0.94 | - | not_needed |
| RR-syn | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | +0.01 [-0.01,+0.02] | 0.99 | - | not_needed |
| RR-syn | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.01,+0.02] | 0.98 | - | not_needed |
| RR-syn | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| RR-syn | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RR-syn | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RR-syn | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.01,+0.02] | 0.97 | - | not_needed |
| RR-syn | lookup_off | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR-syn | lookup_off | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR-syn | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-syn | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-syn | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.00] | - | - | not_needed |
| RR-syn | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR-syn | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.02] | 0.98 | - | not_needed |
| RR-syn | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RR-syn | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-syn | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR-syn | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.00] | - | - | not_needed |
| RR-syn | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RR-syn | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | after | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | 0.94 | - | not_needed |
| RR-syn | random | both | all | absent | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.99 | - | not_needed |
| RR-syn | random | both | all | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.98 | - | not_needed |
| RR-syn | random | both | attn | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.02] | - | - | not_needed |
| RR-syn | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.98 | - | not_needed |
| RR-syn | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RR-syn | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.98 | - | not_needed |
| RR-syn | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-syn | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR-syn | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR-syn | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR-syn | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR-syn | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-syn | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.98 | - | not_needed |
| RR-syn | random | final | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RR-syn | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RR-syn | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR-syn | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-syn | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-syn | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-syn | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | random | question | all | value | 60 | 100% [94,100] | 0% | +0.02 [+0.01,+0.03] | 0.97 | - | not_needed |
| RR-syn | trailing | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | not_needed |
| RR-syn | trailing | after | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.95 | - | not_needed |
| RR-syn | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| RR-syn | trailing | both | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RR-syn | trailing | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR-syn | trailing | question | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RR-xlang | lookup | after | all | absent | 60 | 98% [91,100] | 2% | -0.06 [-0.11,-0.02] | 0.98 | - | not_needed |
| RR-xlang | lookup | after | all | value | 60 | 100% [94,100] | 0% | -0.04 [-0.07,-0.02] | 0.94 | - | not_needed |
| RR-xlang | lookup | both | all | absent | 60 | 97% [89,99] | 3% | -0.05 [-0.10,-0.02] | 0.99 | +3 [+0,+8] | partial |
| RR-xlang | lookup | both | all | value | 60 | 98% [91,100] | 2% | -0.05 [-0.10,-0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | attn | value | 60 | 98% [91,100] | 2% | -0.05 [-0.09,-0.02] | - | - | not_needed |
| RR-xlang | lookup | both | band00-31 | value | 60 | 98% [91,100] | 2% | -0.03 [-0.07,-0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.06,-0.01] | - | - | not_needed |
| RR-xlang | lookup | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | band32-47 | value | 60 | 98% [91,100] | 2% | -0.03 [-0.07,-0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.06,-0.01] | - | - | not_needed |
| RR-xlang | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | band48-63 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR-xlang | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| RR-xlang | lookup | final | all | value | 60 | 98% [91,100] | 2% | -0.03 [-0.07,-0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | attn | value | 60 | 98% [91,100] | 2% | -0.02 [-0.05,-0.00] | - | - | not_needed |
| RR-xlang | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR-xlang | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | band48-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR-xlang | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup | question | all | value | 60 | 98% [91,100] | 2% | -0.04 [-0.08,-0.01] | 0.97 | - | not_needed |
| RR-xlang | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,+0.00] | 0.94 | - | not_needed |
| RR-xlang | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.97 | - | not_needed |
| RR-xlang | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RR-xlang | random | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.94 | - | not_needed |
| RR-xlang | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR-xlang | random | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-xlang | random | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR-xlang | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | random | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR-xlang | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR-xlang | trailing | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-xlang | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.96 | - | not_needed |
| RR-xlang | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| RR-xlang | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR-xlang | trailing | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR-xlang | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup | after | all | absent | 120 | 18% [12,26] | 0% | -2.70 [-3.02,-2.39] | 0.98 | +82 [+75,+88] | needed |
| DL-same | lookup | after | all | value | 120 | 16% [10,23] | 0% | -2.69 [-3.02,-2.40] | 0.94 | +84 [+78,+90] | needed |
| DL-same | lookup | both | all | absent | 120 | 18% [12,25] | 0% | -2.69 [-3.01,-2.39] | 0.99 | +82 [+76,+89] | needed |
| DL-same | lookup | both | all | value | 120 | 15% [10,22] | 0% | -2.74 [-3.07,-2.45] | 0.97 | +85 [+78,+91] | needed |
| DL-same | lookup | both | attn | value | 120 | 15% [10,22] | 0% | -2.80 [-3.12,-2.51] | - | +85 [+78,+91] | needed |
| DL-same | lookup | both | band00-31 | value | 120 | 1% [0,5] | 0% | -5.09 [-5.34,-4.82] | 0.97 | +99 [+98,+100] | needed |
| DL-same | lookup | both | band00-31:attn | value | 120 | 2% [1,7] | 0% | -4.93 [-5.23,-4.63] | - | +98 [+94,+100] | needed |
| DL-same | lookup | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-same | lookup | both | band32-47 | value | 120 | 98% [93,99] | 2% | -0.12 [-0.22,-0.05] | 0.97 | - | not_needed |
| DL-same | lookup | both | band32-47:attn | value | 120 | 98% [93,99] | 2% | -0.13 [-0.23,-0.06] | - | - | not_needed |
| DL-same | lookup | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL-same | lookup | both | band48-63 | value | 120 | 8% [4,14] | 92% | -8.37 [-8.80,-7.88] | 0.98 | +92 [+88,+97] | needed |
| DL-same | lookup | both | band48-63:attn | value | 120 | 8% [4,14] | 92% | -8.40 [-8.84,-7.92] | - | +92 [+88,+97] | needed |
| DL-same | lookup | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-same | lookup | final | all | value | 120 | 10% [6,17] | 85% | -4.72 [-5.07,-4.31] | 0.98 | +90 [+84,+95] | needed |
| DL-same | lookup | final | attn | value | 120 | 10% [6,17] | 83% | -4.77 [-5.15,-4.36] | - | +90 [+84,+95] | needed |
| DL-same | lookup | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL-same | lookup | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup | final | band32-47 | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| DL-same | lookup | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup | final | band48-63 | value | 120 | 8% [4,14] | 92% | -6.41 [-6.79,-6.00] | 0.99 | +92 [+88,+97] | needed |
| DL-same | lookup | final | band48-63:attn | value | 120 | 8% [4,14] | 92% | -6.48 [-6.85,-6.07] | - | +92 [+88,+97] | needed |
| DL-same | lookup | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup | final | gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup | question | all | value | 120 | 1% [0,5] | 0% | -5.10 [-5.33,-4.86] | 0.96 | +99 [+98,+100] | needed |
| DL-same | lookup_off | after | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | after | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| DL-same | lookup_off | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL-same | lookup_off | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | both | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-same | lookup_off | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup_off | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup_off | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup_off | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL-same | lookup_off | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | lookup_off | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | lookup_off | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL-same | random | after | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | random | after | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| DL-same | random | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL-same | random | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | both | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | both | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | random | both | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | both | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | random | both | band32-47 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | both | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | both | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | both | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | both | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | both | band48-63:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | both | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-same | random | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | final | attn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | final | band00-31 | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | random | final | band00-31:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | final | band00-31:gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | random | final | band32-47 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | final | band32-47:attn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-same | random | final | band32-47:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | final | band48-63 | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | final | band48-63:attn | value | 120 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL-same | random | final | band48-63:gdn | value | 120 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | final | gdn | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-same | random | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL-same | trailing | after | all | absent | 120 | 83% [76,89] | 17% | -0.43 [-0.56,-0.31] | 0.99 | - | partial |
| DL-same | trailing | after | all | value | 120 | 100% [97,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | not_needed |
| DL-same | trailing | both | all | absent | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DL-same | trailing | both | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL-same | trailing | final | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL-same | trailing | question | all | value | 120 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-syn | lookup | after | all | absent | 60 | 10% [5,20] | 27% | -3.79 [-4.40,-3.21] | 0.98 | +88 [+78,+95] | needed |
| DL-syn | lookup | after | all | value | 60 | 7% [3,16] | 45% | -4.08 [-4.69,-3.50] | 0.94 | +90 [+80,+98] | needed |
| DL-syn | lookup | both | all | absent | 60 | 7% [3,16] | 42% | -4.00 [-4.57,-3.44] | 0.99 | +93 [+87,+98] | needed |
| DL-syn | lookup | both | all | value | 60 | 5% [2,14] | 45% | -4.00 [-4.56,-3.46] | 0.97 | +95 [+88,+100] | needed |
| DL-syn | lookup | both | attn | value | 60 | 3% [1,11] | 70% | -4.56 [-5.00,-4.13] | - | +97 [+92,+100] | needed |
| DL-syn | lookup | both | band00-31 | value | 60 | 90% [80,95] | 2% | -0.46 [-0.75,-0.23] | 0.97 | +10 [+3,+18] | partial |
| DL-syn | lookup | both | band00-31:attn | value | 60 | 92% [82,96] | 0% | -0.29 [-0.55,-0.11] | - | +8 [+2,+17] | partial |
| DL-syn | lookup | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| DL-syn | lookup | both | band32-47 | value | 60 | 63% [51,74] | 37% | -0.85 [-1.07,-0.66] | 0.97 | +37 [+25,+50] | needed |
| DL-syn | lookup | both | band32-47:attn | value | 60 | 67% [54,77] | 33% | -0.84 [-1.04,-0.66] | - | +33 [+22,+47] | needed |
| DL-syn | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| DL-syn | lookup | both | band48-63 | value | 60 | 0% [-0,6] | 100% | -7.40 [-7.73,-7.07] | 0.98 | +100 [+100,+100] | needed |
| DL-syn | lookup | both | band48-63:attn | value | 60 | 0% [-0,6] | 100% | -7.49 [-7.78,-7.18] | - | +100 [+100,+100] | needed |
| DL-syn | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| DL-syn | lookup | final | all | value | 60 | 0% [-0,6] | 92% | -5.20 [-5.45,-4.96] | 0.98 | +100 [+100,+100] | needed |
| DL-syn | lookup | final | attn | value | 60 | 0% [-0,6] | 90% | -5.27 [-5.49,-5.06] | - | +100 [+100,+100] | needed |
| DL-syn | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL-syn | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL-syn | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup | final | band32-47 | value | 60 | 95% [86,98] | 5% | -0.20 [-0.27,-0.13] | 0.98 | +5 [+0,+12] | partial |
| DL-syn | lookup | final | band32-47:attn | value | 60 | 97% [89,99] | 3% | -0.19 [-0.26,-0.13] | - | +3 [+0,+8] | partial |
| DL-syn | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup | final | band48-63 | value | 60 | 0% [-0,6] | 100% | -5.48 [-5.79,-5.18] | 0.99 | +100 [+100,+100] | needed |
| DL-syn | lookup | final | band48-63:attn | value | 60 | 0% [-0,6] | 100% | -5.65 [-5.92,-5.37] | - | +100 [+100,+100] | needed |
| DL-syn | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup | question | all | value | 60 | 27% [17,39] | 18% | -2.39 [-2.83,-1.99] | 0.96 | +73 [+63,+83] | needed |
| DL-syn | lookup_off | after | all | absent | 60 | 98% [91,100] | 2% | -0.03 [-0.08,+0.01] | 0.98 | - | not_needed |
| DL-syn | lookup_off | after | all | value | 60 | 97% [89,99] | 3% | -0.05 [-0.11,-0.00] | 0.94 | - | partial |
| DL-syn | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | 0.99 | - | not_needed |
| DL-syn | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.03] | 0.98 | - | not_needed |
| DL-syn | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.03] | - | - | not_needed |
| DL-syn | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.03] | 0.97 | - | not_needed |
| DL-syn | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| DL-syn | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| DL-syn | lookup_off | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| DL-syn | lookup_off | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| DL-syn | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL-syn | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| DL-syn | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| DL-syn | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| DL-syn | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.01,+0.02] | 0.99 | - | not_needed |
| DL-syn | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.01,+0.02] | - | - | not_needed |
| DL-syn | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-syn | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| DL-syn | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL-syn | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| DL-syn | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| DL-syn | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.01,+0.03] | 0.97 | - | not_needed |
| DL-syn | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.03 [-0.06,-0.02] | 0.98 | - | not_needed |
| DL-syn | random | after | all | value | 60 | 100% [94,100] | 0% | -0.05 [-0.09,-0.02] | 0.94 | - | not_needed |
| DL-syn | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| DL-syn | random | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | not_needed |
| DL-syn | random | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| DL-syn | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| DL-syn | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| DL-syn | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| DL-syn | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| DL-syn | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL-syn | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| DL-syn | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| DL-syn | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-syn | random | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| DL-syn | random | final | all | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.03] | 0.99 | - | not_needed |
| DL-syn | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| DL-syn | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-syn | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| DL-syn | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL-syn | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| DL-syn | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| DL-syn | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 0.97 | - | not_needed |
| DL-syn | trailing | after | all | absent | 60 | 98% [91,100] | 2% | -0.25 [-0.31,-0.20] | 0.99 | - | not_needed |
| DL-syn | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.04 [-0.07,-0.01] | 0.95 | - | not_needed |
| DL-syn | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 1.00 | - | not_needed |
| DL-syn | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.02] | 0.98 | - | not_needed |
| DL-syn | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-syn | trailing | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.01,+0.02] | 0.97 | - | not_needed |
| DL-xlang | lookup | after | all | absent | 60 | 17% [9,28] | 0% | -2.53 [-2.86,-2.23] | 0.98 | +82 [+72,+90] | needed |
| DL-xlang | lookup | after | all | value | 60 | 17% [9,28] | 0% | -2.50 [-2.81,-2.21] | 0.94 | +83 [+73,+92] | needed |
| DL-xlang | lookup | both | all | absent | 60 | 18% [11,30] | 0% | -2.47 [-2.84,-2.14] | 0.99 | +82 [+72,+90] | needed |
| DL-xlang | lookup | both | all | value | 60 | 18% [11,30] | 0% | -2.47 [-2.85,-2.13] | 0.98 | +82 [+72,+90] | needed |
| DL-xlang | lookup | both | attn | value | 60 | 18% [11,30] | 0% | -2.54 [-2.91,-2.21] | - | +82 [+72,+90] | needed |
| DL-xlang | lookup | both | band00-31 | value | 60 | 0% [-0,6] | 0% | -4.50 [-4.80,-4.20] | 0.98 | +100 [+100,+100] | needed |
| DL-xlang | lookup | both | band00-31:attn | value | 60 | 12% [6,22] | 0% | -3.87 [-4.23,-3.47] | - | +88 [+80,+95] | needed |
| DL-xlang | lookup | both | band00-31:gdn | value | 60 | 98% [91,100] | 0% | -0.04 [-0.09,-0.01] | 0.98 | - | not_needed |
| DL-xlang | lookup | both | band32-47 | value | 60 | 67% [54,77] | 30% | -0.90 [-1.04,-0.76] | 0.97 | +32 [+20,+43] | needed |
| DL-xlang | lookup | both | band32-47:attn | value | 60 | 62% [49,73] | 30% | -0.94 [-1.08,-0.79] | - | +37 [+25,+48] | needed |
| DL-xlang | lookup | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL-xlang | lookup | both | band48-63 | value | 60 | 2% [0,9] | 98% | -6.39 [-6.85,-5.91] | 0.98 | +98 [+95,+100] | needed |
| DL-xlang | lookup | both | band48-63:attn | value | 60 | 2% [0,9] | 98% | -6.47 [-6.91,-6.00] | - | +98 [+95,+100] | needed |
| DL-xlang | lookup | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup | both | gdn | value | 60 | 98% [91,100] | 0% | -0.08 [-0.18,-0.02] | 0.97 | - | not_needed |
| DL-xlang | lookup | final | all | value | 60 | 5% [2,14] | 90% | -3.31 [-3.57,-3.04] | 0.98 | +95 [+88,+100] | needed |
| DL-xlang | lookup | final | attn | value | 60 | 5% [2,14] | 90% | -3.28 [-3.54,-3.02] | - | +95 [+88,+100] | needed |
| DL-xlang | lookup | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | lookup | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | lookup | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | lookup | final | band32-47 | value | 60 | 88% [78,94] | 12% | -0.43 [-0.54,-0.34] | 0.98 | +12 [+5,+20] | partial |
| DL-xlang | lookup | final | band32-47:attn | value | 60 | 88% [78,94] | 12% | -0.44 [-0.55,-0.35] | - | +12 [+5,+20] | partial |
| DL-xlang | lookup | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup | final | band48-63 | value | 60 | 7% [3,16] | 93% | -4.06 [-4.46,-3.65] | 0.98 | +93 [+87,+98] | needed |
| DL-xlang | lookup | final | band48-63:attn | value | 60 | 7% [3,16] | 93% | -4.17 [-4.56,-3.77] | - | +93 [+87,+98] | needed |
| DL-xlang | lookup | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | lookup | question | all | value | 60 | 0% [-0,6] | 0% | -4.51 [-4.76,-4.25] | 0.97 | +98 [+95,+100] | needed |
| DL-xlang | lookup_off | after | all | absent | 60 | 98% [91,100] | 2% | -0.03 [-0.08,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.03 [-0.06,+0.00] | 0.94 | - | not_needed |
| DL-xlang | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL-xlang | lookup_off | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL-xlang | lookup_off | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | both | band32-47 | value | 60 | 98% [91,100] | 2% | -0.01 [-0.04,-0.00] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | both | band32-47:attn | value | 60 | 98% [91,100] | 2% | -0.01 [-0.04,-0.00] | - | - | not_needed |
| DL-xlang | lookup_off | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL-xlang | lookup_off | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| DL-xlang | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| DL-xlang | lookup_off | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | lookup_off | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | lookup_off | final | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | lookup_off | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | final | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL-xlang | lookup_off | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | lookup_off | question | all | value | 60 | 98% [91,100] | 2% | -0.01 [-0.03,+0.00] | 0.97 | - | not_needed |
| DL-xlang | random | after | all | absent | 60 | 93% [84,97] | 7% | -0.20 [-0.39,-0.04] | 0.98 | - | partial |
| DL-xlang | random | after | all | value | 60 | 92% [82,96] | 8% | -0.24 [-0.43,-0.09] | 0.93 | - | partial |
| DL-xlang | random | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| DL-xlang | random | both | all | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL-xlang | random | both | band00-31 | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | random | both | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | random | both | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | random | both | band32-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| DL-xlang | random | both | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL-xlang | random | both | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | random | both | band48-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | random | both | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | random | both | band48-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL-xlang | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| DL-xlang | random | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | random | final | band00-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | random | final | band00-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| DL-xlang | random | final | band00-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | random | final | band32-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | random | final | band32-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | random | final | band32-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | random | final | band48-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | random | final | band48-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL-xlang | random | final | band48-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | random | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| DL-xlang | random | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| DL-xlang | trailing | after | all | absent | 60 | 98% [91,100] | 2% | -0.14 [-0.19,-0.09] | 0.99 | - | not_needed |
| DL-xlang | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.08 [-0.11,-0.06] | 0.95 | - | not_needed |
| DL-xlang | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | not_needed |
| DL-xlang | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| DL-xlang | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL-xlang | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
