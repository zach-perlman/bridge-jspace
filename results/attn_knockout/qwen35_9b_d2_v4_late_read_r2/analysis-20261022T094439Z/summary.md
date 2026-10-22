# attn_knockout / qwen35_9b_d2_v4_late_read_r2

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}, "DL": {"items": 300, "unedited_right": 300}, "RR": {"items": 200, "unedited_right": 200}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.023,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.027,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 0.993,
     "verdict": "not_needed"
    },
    "band00-15:attn": {
     "acc": 0.993,
     "verdict": "not_needed"
    },
    "band00-15:gdn": {
     "acc": 0.997,
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
     "acc": 0.997,
     "verdict": "not_needed"
    },
    "band16-23": {
     "acc": 0.557,
     "verdict": "needed"
    },
    "band16-23:attn": {
     "acc": 0.587,
     "verdict": "needed"
    },
    "band16-23:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band16-19": {
     "acc": 0.977,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.947,
     "verdict": "not_needed"
    },
    "band24-31": {
     "acc": 0.967,
     "verdict": "not_needed"
    },
    "band24-31:attn": {
     "acc": 0.963,
     "verdict": "not_needed"
    },
    "band24-31:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band24-27": {
     "acc": 0.993,
     "verdict": "not_needed"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.613,
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
     "acc": 0.063,
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
    "band16-23": {
     "acc": 0.783,
     "verdict": "needed"
    },
    "band16-23:attn": {
     "acc": 0.803,
     "verdict": "partial"
    },
    "band16-23:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band16-19": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.997,
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
    "acc": 0.03,
    "verdict": "needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "RR": {
   "path": false,
   "final": {
    "all": {
     "acc": 0.94,
     "verdict": "partial"
    },
    "attn": {
     "acc": 0.96,
     "verdict": "not_needed"
    },
    "gdn": {
     "acc": 0.995,
     "verdict": "not_needed"
    },
    "band00-15": {
     "acc": 0.995,
     "verdict": "not_needed"
    },
    "band00-15:attn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band00-15:gdn": {
     "acc": 0.995,
     "verdict": "not_needed"
    },
    "band00-03": {
     "acc": 0.995,
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
     "acc": 0.965,
     "verdict": "not_needed"
    },
    "band16-23:attn": {
     "acc": 0.985,
     "verdict": "not_needed"
    },
    "band16-23:gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    },
    "band16-19": {
     "acc": 0.995,
     "verdict": "not_needed"
    },
    "band20-23": {
     "acc": 0.995,
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
    "acc": 0.96,
    "verdict": "not_needed"
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
   "question": "not_needed",
   "final": "partial",
   "both": "not_needed",
   "after": "partial"
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
  "RL/lookup/final": {
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
  "RL/lookup/both": {
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
  "DL/lookup/question": {
   "windows_needed": [
    "band00-15",
    "band00-15:attn"
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
    "band16-23"
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
    "band16-23"
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
| RL | lookup | after | all | value | 300 | 3% [1,5] | 85% | -3.89 [-4.07,-3.71] | 0.95 | +96 [+94,+98] | needed |
| RL | lookup | both | all | value | 300 | 4% [3,7] | 84% | -3.81 [-3.99,-3.63] | 0.97 | +95 [+92,+97] | needed |
| RL | lookup | both | attn | value | 300 | 4% [2,7] | 88% | -4.16 [-4.35,-3.99] | - | +96 [+94,+98] | needed |
| RL | lookup | both | band00-03 | value | 300 | 99% [98,100] | 1% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
| RL | lookup | both | band00-15 | value | 300 | 53% [48,59] | 35% | -1.28 [-1.40,-1.17] | 0.97 | +46 [+40,+52] | needed |
| RL | lookup | both | band00-15:attn | value | 300 | 59% [54,65] | 35% | -1.07 [-1.18,-0.95] | - | +41 [+35,+46] | needed |
| RL | lookup | both | band00-15:gdn | value | 300 | 94% [91,96] | 4% | -0.18 [-0.23,-0.14] | 0.97 | - | not_needed |
| RL | lookup | both | band04-07 | value | 300 | 99% [97,99] | 1% | -0.07 [-0.09,-0.05] | 0.98 | - | not_needed |
| RL | lookup | both | band08-11 | value | 300 | 78% [73,82] | 17% | -0.64 [-0.74,-0.55] | 0.96 | +22 [+17,+26] | needed |
| RL | lookup | both | band12-15 | value | 300 | 93% [90,95] | 7% | -0.25 [-0.29,-0.21] | 0.97 | +7 [+4,+10] | partial |
| RL | lookup | both | band16-19 | value | 300 | 97% [95,99] | 2% | -0.16 [-0.18,-0.14] | 0.97 | - | not_needed |
| RL | lookup | both | band16-23 | value | 300 | 55% [49,60] | 45% | -0.95 [-1.03,-0.87] | 0.97 | +45 [+40,+51] | needed |
| RL | lookup | both | band16-23:attn | value | 300 | 58% [53,64] | 42% | -0.90 [-0.97,-0.83] | - | +42 [+36,+47] | needed |
| RL | lookup | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | band20-23 | value | 300 | 95% [92,97] | 5% | -0.14 [-0.16,-0.12] | 0.98 | - | not_needed |
| RL | lookup | both | band24-27 | value | 300 | 99% [98,100] | 1% | -0.04 [-0.05,-0.03] | 0.98 | - | not_needed |
| RL | lookup | both | band24-31 | value | 300 | 97% [94,98] | 3% | -0.07 [-0.09,-0.06] | 0.98 | - | not_needed |
| RL | lookup | both | band24-31:attn | value | 300 | 96% [94,98] | 4% | -0.07 [-0.09,-0.06] | - | - | not_needed |
| RL | lookup | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | 0.98 | - | not_needed |
| RL | lookup | both | gdn | value | 300 | 94% [90,96] | 5% | -0.19 [-0.24,-0.14] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 300 | 2% [1,5] | 97% | -4.67 [-4.84,-4.51] | 0.98 | +98 [+96,+99] | needed |
| RL | lookup | final | attn | value | 300 | 3% [1,5] | 96% | -4.40 [-4.57,-4.24] | - | +97 [+95,+99] | needed |
| RL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band00-15 | value | 300 | 99% [98,100] | 1% | -0.06 [-0.08,-0.04] | 0.98 | - | not_needed |
| RL | lookup | final | band00-15:attn | value | 300 | 99% [98,100] | 1% | -0.05 [-0.07,-0.04] | - | - | not_needed |
| RL | lookup | final | band00-15:gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band12-15 | value | 300 | 100% [98,100] | 0% | -0.04 [-0.05,-0.03] | 0.98 | - | not_needed |
| RL | lookup | final | band16-19 | value | 300 | 98% [95,99] | 2% | -0.15 [-0.17,-0.13] | 0.98 | - | not_needed |
| RL | lookup | final | band16-23 | value | 300 | 56% [50,61] | 44% | -0.95 [-1.04,-0.87] | 0.98 | +44 [+39,+50] | needed |
| RL | lookup | final | band16-23:attn | value | 300 | 59% [53,64] | 41% | -0.89 [-0.96,-0.82] | - | +41 [+36,+47] | needed |
| RL | lookup | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | band20-23 | value | 300 | 95% [92,97] | 5% | -0.14 [-0.16,-0.12] | 0.99 | - | not_needed |
| RL | lookup | final | band24-27 | value | 300 | 99% [98,100] | 1% | -0.04 [-0.05,-0.03] | 0.99 | - | not_needed |
| RL | lookup | final | band24-31 | value | 300 | 97% [94,98] | 3% | -0.07 [-0.09,-0.06] | 0.99 | - | not_needed |
| RL | lookup | final | band24-31:attn | value | 300 | 96% [94,98] | 4% | -0.07 [-0.09,-0.06] | - | - | not_needed |
| RL | lookup | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | 0.99 | - | not_needed |
| RL | lookup | final | gdn | value | 300 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 61% [56,67] | 29% | -1.12 [-1.24,-1.00] | 0.97 | +38 [+33,+44] | needed |
| RL | lookup | question | attn | value | 300 | 68% [63,73] | 27% | -0.86 [-0.97,-0.76] | - | +32 [+26,+37] | needed |
| RL | lookup | question | band00-03 | value | 300 | 99% [98,100] | 1% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL | lookup | question | band00-15 | value | 300 | 61% [55,66] | 28% | -1.11 [-1.24,-1.00] | 0.96 | +39 [+33,+44] | needed |
| RL | lookup | question | band00-15:attn | value | 300 | 68% [63,73] | 27% | -0.86 [-0.97,-0.76] | - | +32 [+26,+37] | needed |
| RL | lookup | question | band00-15:gdn | value | 300 | 95% [92,97] | 3% | -0.18 [-0.23,-0.13] | 0.96 | - | not_needed |
| RL | lookup | question | band04-07 | value | 300 | 99% [97,99] | 1% | -0.06 [-0.09,-0.05] | 0.97 | - | not_needed |
| RL | lookup | question | band08-11 | value | 300 | 78% [73,82] | 16% | -0.63 [-0.73,-0.53] | 0.95 | +22 [+17,+27] | needed |
| RL | lookup | question | band12-15 | value | 300 | 97% [94,98] | 3% | -0.13 [-0.16,-0.11] | 0.96 | - | not_needed |
| RL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | gdn | value | 300 | 94% [91,96] | 4% | -0.18 [-0.23,-0.14] | 0.97 | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 99% [97,100] | 1% | -0.01 [-0.03,+0.01] | 0.94 | - | not_needed |
| RL | lookup_off | both | all | value | 300 | 99% [98,100] | 0% | +0.02 [+0.01,+0.03] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.02 [+0.01,+0.03] | - | - | not_needed |
| RL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | band00-15 | value | 300 | 99% [98,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band00-15:gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.02,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band04-07 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band08-11 | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | 0.98 | - | not_needed |
| RL | lookup_off | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | band00-15:gdn | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RL | lookup_off | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [98,100] | 0% | -0.01 [-0.01,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band00-15 | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | band00-15:gdn | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.95 | - | not_needed |
| RL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.02,+0.00] | 0.97 | - | not_needed |
| RL | random | after | all | value | 300 | 99% [98,100] | 0% | -0.03 [-0.05,-0.01] | 0.95 | - | not_needed |
| RL | random | both | all | value | 300 | 100% [98,100] | 0% | +0.02 [+0.01,+0.03] | 0.98 | - | not_needed |
| RL | random | both | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | band00-15 | value | 300 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RL | random | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | random | both | band00-15:gdn | value | 300 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band08-11 | value | 300 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | gdn | value | 300 | 99% [98,100] | 1% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RL | random | final | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| RL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | random | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | gdn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | random | question | all | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | question | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | random | question | band00-03 | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band00-15 | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | question | band00-15:attn | value | 300 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | - | - | not_needed |
| RL | random | question | band00-15:gdn | value | 300 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.96 | - | not_needed |
| RL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | gdn | value | 300 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.97 | - | not_needed |
| RL | trailing | after | all | value | 300 | 98% [96,99] | 1% | -0.07 [-0.10,-0.04] | 0.96 | - | not_needed |
| RL | trailing | both | all | value | 300 | 99% [97,100] | 1% | -0.03 [-0.06,-0.01] | 0.98 | - | not_needed |
| RL | trailing | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | trailing | question | all | value | 300 | 99% [98,100] | 0% | -0.03 [-0.06,-0.01] | 0.98 | - | not_needed |
| DL | lookup | after | all | value | 300 | 20% [16,25] | 2% | -2.13 [-2.26,-2.00] | 0.94 | +80 [+76,+85] | needed |
| DL | lookup | both | all | value | 300 | 20% [16,25] | 4% | -2.02 [-2.15,-1.90] | 0.97 | +80 [+76,+85] | needed |
| DL | lookup | both | attn | value | 300 | 20% [16,25] | 7% | -2.00 [-2.13,-1.89] | - | +80 [+76,+85] | needed |
| DL | lookup | both | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band00-15 | value | 300 | 3% [2,6] | 2% | -4.73 [-4.90,-4.56] | 0.97 | +97 [+95,+99] | needed |
| DL | lookup | both | band00-15:attn | value | 300 | 7% [5,10] | 4% | -4.46 [-4.67,-4.25] | - | +93 [+90,+96] | needed |
| DL | lookup | both | band00-15:gdn | value | 300 | 99% [98,100] | 0% | -0.03 [-0.06,-0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band04-07 | value | 300 | 87% [83,90] | 1% | -0.58 [-0.75,-0.43] | 0.98 | +13 [+9,+17] | partial |
| DL | lookup | both | band08-11 | value | 300 | 86% [82,90] | 5% | -0.50 [-0.65,-0.37] | 0.96 | +14 [+10,+18] | partial |
| DL | lookup | both | band12-15 | value | 300 | 90% [86,93] | 10% | -0.28 [-0.39,-0.20] | 0.97 | +10 [+6,+13] | partial |
| DL | lookup | both | band16-19 | value | 300 | 100% [99,100] | 0% | -0.02 [-0.03,-0.02] | 0.97 | - | not_needed |
| DL | lookup | both | band16-23 | value | 300 | 77% [72,82] | 23% | -0.49 [-0.56,-0.42] | 0.97 | +23 [+18,+27] | needed |
| DL | lookup | both | band16-23:attn | value | 300 | 80% [75,84] | 20% | -0.47 [-0.54,-0.41] | - | +20 [+15,+24] | partial |
| DL | lookup | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | both | band20-23 | value | 300 | 100% [98,100] | 0% | -0.03 [-0.04,-0.02] | 0.98 | - | not_needed |
| DL | lookup | both | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band24-31 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | 0.98 | - | not_needed |
| DL | lookup | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| DL | lookup | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | both | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | both | gdn | value | 300 | 99% [98,100] | 0% | -0.02 [-0.05,-0.00] | 0.97 | - | not_needed |
| DL | lookup | final | all | value | 300 | 5% [3,8] | 93% | -4.34 [-4.56,-4.13] | 0.98 | +95 [+93,+98] | needed |
| DL | lookup | final | attn | value | 300 | 6% [4,10] | 91% | -4.17 [-4.37,-3.95] | - | +94 [+91,+96] | needed |
| DL | lookup | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.02 [-0.03,-0.02] | 0.98 | - | not_needed |
| DL | lookup | final | band16-23 | value | 300 | 78% [73,83] | 22% | -0.49 [-0.56,-0.42] | 0.98 | +22 [+17,+26] | needed |
| DL | lookup | final | band16-23:attn | value | 300 | 80% [75,84] | 20% | -0.46 [-0.52,-0.40] | - | +20 [+15,+24] | partial |
| DL | lookup | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | final | band20-23 | value | 300 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | 0.99 | - | not_needed |
| DL | lookup | final | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band24-31 | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | 0.99 | - | not_needed |
| DL | lookup | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| DL | lookup | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup | final | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | all | value | 300 | 3% [2,6] | 2% | -4.78 [-4.96,-4.60] | 0.97 | +97 [+95,+99] | needed |
| DL | lookup | question | attn | value | 300 | 8% [6,12] | 3% | -4.48 [-4.69,-4.27] | - | +92 [+88,+95] | needed |
| DL | lookup | question | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band00-15 | value | 300 | 3% [2,6] | 2% | -4.77 [-4.95,-4.59] | 0.96 | +97 [+94,+99] | needed |
| DL | lookup | question | band00-15:attn | value | 300 | 8% [5,12] | 3% | -4.48 [-4.68,-4.27] | - | +92 [+89,+95] | needed |
| DL | lookup | question | band00-15:gdn | value | 300 | 99% [98,100] | 0% | -0.03 [-0.07,-0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band04-07 | value | 300 | 87% [83,90] | 2% | -0.58 [-0.75,-0.43] | 0.97 | +13 [+9,+17] | partial |
| DL | lookup | question | band08-11 | value | 300 | 87% [83,90] | 5% | -0.49 [-0.64,-0.37] | 0.95 | +13 [+9,+17] | partial |
| DL | lookup | question | band12-15 | value | 300 | 95% [92,97] | 5% | -0.17 [-0.24,-0.11] | 0.96 | - | not_needed |
| DL | lookup | question | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup | question | band16-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | question | band24-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | lookup | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup | question | gdn | value | 300 | 99% [98,100] | 0% | -0.02 [-0.06,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.94 | - | not_needed |
| DL | lookup_off | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | both | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-03 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band16-19 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | band00-15:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| DL | lookup_off | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | lookup_off | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | lookup_off | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | after | all | value | 300 | 100% [99,100] | 0% | -0.01 [-0.01,-0.00] | 0.94 | - | not_needed |
| DL | random | both | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | both | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | both | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | both | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | both | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | both | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | both | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | both | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | both | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | both | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band00-15 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | final | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band04-07 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band08-11 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | final | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | final | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band20-23 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-27 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | final | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | band28-31 | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band00-03 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band00-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | question | band00-15:attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | random | question | band00-15:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band04-07 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | random | question | band08-11 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | random | question | band12-15 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DL | random | question | band16-19 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| DL | random | question | band16-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band16-23:attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | random | question | band16-23:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | random | question | band20-23 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band24-27 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DL | random | question | band24-31 | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band24-31:attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | random | question | band24-31:gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | band28-31 | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| DL | random | question | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| DL | trailing | after | all | value | 300 | 100% [99,100] | 0% | -0.01 [-0.02,-0.01] | 0.96 | - | not_needed |
| DL | trailing | both | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| DL | trailing | final | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DL | trailing | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | after | all | value | 200 | 93% [89,96] | 6% | -0.20 [-0.26,-0.16] | 0.95 | +6 [+4,+10] | partial |
| RR | lookup | both | all | value | 200 | 94% [90,97] | 6% | -0.19 [-0.23,-0.15] | 0.98 | - | not_needed |
| RR | lookup | both | attn | value | 200 | 94% [90,97] | 6% | -0.18 [-0.22,-0.14] | - | +6 [+3,+9] | partial |
| RR | lookup | both | band00-03 | value | 200 | 99% [96,100] | 1% | -0.01 [-0.01,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | band00-15 | value | 200 | 96% [93,98] | 4% | -0.15 [-0.18,-0.12] | 0.97 | - | not_needed |
| RR | lookup | both | band00-15:attn | value | 200 | 97% [94,99] | 3% | -0.13 [-0.17,-0.11] | - | - | not_needed |
| RR | lookup | both | band00-15:gdn | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | band04-07 | value | 200 | 99% [96,100] | 0% | -0.03 [-0.05,-0.01] | 0.98 | - | not_needed |
| RR | lookup | both | band08-11 | value | 200 | 99% [96,100] | 1% | -0.07 [-0.09,-0.06] | 0.96 | - | not_needed |
| RR | lookup | both | band12-15 | value | 200 | 100% [97,100] | 0% | -0.05 [-0.07,-0.03] | 0.97 | - | not_needed |
| RR | lookup | both | band16-19 | value | 200 | 99% [96,100] | 1% | -0.05 [-0.06,-0.03] | 0.97 | - | not_needed |
| RR | lookup | both | band16-23 | value | 200 | 96% [92,98] | 4% | -0.10 [-0.13,-0.07] | 0.98 | - | not_needed |
| RR | lookup | both | band16-23:attn | value | 200 | 98% [95,99] | 2% | -0.09 [-0.12,-0.06] | - | - | not_needed |
| RR | lookup | both | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| RR | lookup | both | band20-23 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.04,-0.01] | 0.98 | - | not_needed |
| RR | lookup | both | band24-27 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | both | band24-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | band24-31:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | band24-31:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | gdn | value | 200 | 99% [96,100] | 1% | -0.02 [-0.03,-0.01] | 0.98 | - | not_needed |
| RR | lookup | final | all | value | 200 | 94% [90,97] | 6% | -0.12 [-0.15,-0.09] | 0.99 | +6 [+3,+9] | partial |
| RR | lookup | final | attn | value | 200 | 96% [92,98] | 4% | -0.10 [-0.13,-0.08] | - | - | not_needed |
| RR | lookup | final | band00-03 | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band00-15 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band00-15:attn | value | 200 | 100% [98,100] | 0% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RR | lookup | final | band00-15:gdn | value | 200 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | lookup | final | band04-07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band08-11 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.98 | - | not_needed |
| RR | lookup | final | band12-15 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band16-19 | value | 200 | 100% [97,100] | 0% | -0.04 [-0.05,-0.03] | 0.99 | - | not_needed |
| RR | lookup | final | band16-23 | value | 200 | 96% [93,98] | 4% | -0.09 [-0.12,-0.06] | 0.99 | - | not_needed |
| RR | lookup | final | band16-23:attn | value | 200 | 98% [96,99] | 2% | -0.08 [-0.11,-0.05] | - | - | not_needed |
| RR | lookup | final | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band20-23 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.04,-0.01] | 0.99 | - | not_needed |
| RR | lookup | final | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band24-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band24-31:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | band24-31:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | gdn | value | 200 | 100% [97,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup | question | all | value | 200 | 96% [92,98] | 4% | -0.14 [-0.17,-0.11] | 0.97 | - | not_needed |
| RR | lookup | question | attn | value | 200 | 97% [94,99] | 3% | -0.11 [-0.14,-0.08] | - | - | not_needed |
| RR | lookup | question | band00-03 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RR | lookup | question | band00-15 | value | 200 | 96% [93,98] | 3% | -0.13 [-0.16,-0.11] | 0.96 | - | not_needed |
| RR | lookup | question | band00-15:attn | value | 200 | 97% [94,99] | 3% | -0.11 [-0.14,-0.08] | - | - | not_needed |
| RR | lookup | question | band00-15:gdn | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | 0.96 | - | not_needed |
| RR | lookup | question | band04-07 | value | 200 | 99% [96,100] | 0% | -0.03 [-0.05,-0.01] | 0.97 | - | not_needed |
| RR | lookup | question | band08-11 | value | 200 | 100% [97,100] | 0% | -0.06 [-0.07,-0.05] | 0.95 | - | not_needed |
| RR | lookup | question | band12-15 | value | 200 | 100% [97,100] | 0% | -0.03 [-0.05,-0.02] | 0.96 | - | not_needed |
| RR | lookup | question | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | question | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | band16-23:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | band20-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | band24-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | band24-31:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | band24-31:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | gdn | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | 0.97 | - | not_needed |
| RR | lookup_off | after | all | value | 200 | 100% [97,100] | 0% | +0.01 [-0.00,+0.03] | 0.95 | - | not_needed |
| RR | lookup_off | both | all | value | 200 | 100% [97,100] | 0% | +0.01 [+0.00,+0.03] | 0.98 | - | not_needed |
| RR | lookup_off | both | attn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | both | band00-03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band00-15 | value | 200 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RR | lookup_off | both | band00-15:attn | value | 200 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | both | band00-15:gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
| RR | lookup_off | both | band04-07 | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band08-11 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.96 | - | not_needed |
| RR | lookup_off | both | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | both | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band16-23:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band16-23:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band20-23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | band24-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | band24-31:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RR | lookup_off | final | all | value | 200 | 100% [98,100] | 0% | +0.02 [+0.01,+0.02] | 0.99 | - | not_needed |
| RR | lookup_off | final | attn | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | final | band00-03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup_off | final | band00-15 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RR | lookup_off | final | band00-15:attn | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | final | band00-15:gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RR | lookup_off | final | band04-07 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR | lookup_off | final | band08-11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | lookup_off | final | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band20-23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band24-27 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band24-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | band24-31:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | lookup_off | final | gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RR | lookup_off | question | all | value | 200 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | question | attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | question | band00-03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | question | band00-15 | value | 200 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.96 | - | not_needed |
| RR | lookup_off | question | band00-15:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | lookup_off | question | band00-15:gdn | value | 200 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.96 | - | not_needed |
| RR | lookup_off | question | band04-07 | value | 200 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RR | lookup_off | question | band08-11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.95 | - | not_needed |
| RR | lookup_off | question | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | band16-19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | band20-23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | band24-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | question | band24-31:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | band28-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | gdn | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | after | all | value | 200 | 99% [96,100] | 1% | +0.00 [-0.01,+0.02] | 0.95 | - | not_needed |
| RR | random | both | all | value | 200 | 100% [98,100] | 0% | +0.02 [+0.01,+0.02] | 0.98 | - | not_needed |
| RR | random | both | attn | value | 200 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RR | random | both | band00-03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band00-15 | value | 200 | 100% [98,100] | 0% | +0.02 [+0.01,+0.02] | 0.98 | - | not_needed |
| RR | random | both | band00-15:attn | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | random | both | band00-15:gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RR | random | both | band04-07 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | both | band08-11 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | both | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | both | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | band20-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | band24-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | band24-31:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| RR | random | final | all | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| RR | random | final | attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | random | final | band00-03 | value | 200 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band00-15 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| RR | random | final | band00-15:attn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | random | final | band00-15:gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR | random | final | band04-07 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RR | random | final | band08-11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | final | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | band20-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | band24-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | random | final | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | band24-31:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | random | final | band28-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | random | final | gdn | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| RR | random | question | all | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | attn | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | random | question | band00-03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | band00-15 | value | 200 | 100% [97,100] | 0% | +0.01 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | band00-15:attn | value | 200 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RR | random | question | band00-15:gdn | value | 200 | 100% [97,100] | 0% | +0.01 [-0.00,+0.01] | 0.97 | - | not_needed |
| RR | random | question | band04-07 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | random | question | band08-11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.96 | - | not_needed |
| RR | random | question | band12-15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | band16-19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | band16-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band16-23:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | band16-23:gdn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band20-23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band24-27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | question | band24-31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band24-31:attn | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | band24-31:gdn | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | band28-31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | gdn | value | 200 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| RR | trailing | after | all | value | 200 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.96 | - | not_needed |
| RR | trailing | both | all | value | 200 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | 0.98 | - | not_needed |
| RR | trailing | final | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RR | trailing | question | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
