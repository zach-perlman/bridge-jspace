# attn_knockout / olmo_hybrid_7b_d2_late_read_seed2_after

Measure: correct (items: {"RL": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.07,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.25,
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
   "windows_needed": [],
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
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn",
    "gdn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/after": {
   "windows_needed": [],
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
| RL | lookup | after | all | value | 100 | 9% [5,16] | 42% | -3.51 [-3.91,-3.13] | 0.98 | +76 [+67,+84] | needed |
| RL | lookup | after | attn | value | 100 | 6% [3,12] | 61% | -4.11 [-4.56,-3.68] | - | +94 [+89,+98] | needed |
| RL | lookup | after | gdn | value | 100 | 65% [55,74] | 8% | -1.51 [-1.92,-1.12] | 0.98 | +17 [+6,+28] | partial |
| RL | lookup | both | attn | value | 100 | 5% [2,11] | 58% | -4.00 [-4.42,-3.59] | - | +95 [+90,+99] | needed |
| RL | lookup | both | gdn | value | 100 | 72% [63,80] | 9% | -1.14 [-1.52,-0.78] | 0.98 | +27 [+19,+36] | needed |
| RL | lookup | final | all | value | 100 | 5% [2,11] | 72% | -5.10 [-5.58,-4.64] | 0.99 | +95 [+90,+99] | needed |
| RL | lookup | final | attn | value | 100 | 7% [3,14] | 75% | -4.92 [-5.38,-4.47] | - | +93 [+88,+97] | needed |
| RL | lookup | final | gdn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 100 | 25% [18,34] | 34% | -3.34 [-3.77,-2.93] | 0.98 | +74 [+65,+82] | needed |
| RL | lookup | question | attn | value | 100 | 36% [27,46] | 40% | -3.00 [-3.54,-2.45] | - | +64 [+54,+73] | needed |
| RL | lookup | question | gdn | value | 100 | 73% [64,81] | 8% | -1.12 [-1.50,-0.77] | 0.98 | +26 [+18,+35] | needed |
| RL | lookup_off | after | all | value | 100 | 85% [77,91] | 12% | -0.56 [-0.87,-0.30] | 0.98 | - | partial |
| RL | lookup_off | after | attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | after | gdn | value | 100 | 82% [73,88] | 15% | -0.76 [-1.13,-0.44] | 0.98 | - | partial |
| RL | lookup_off | both | attn | value | 100 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 100 | 99% [95,100] | 1% | -0.03 [-0.08,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | all | value | 100 | 100% [96,100] | 0% | -0.02 [-0.04,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 100 | 100% [96,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 99% [95,100] | 1% | -0.02 [-0.05,+0.01] | 0.98 | - | not_needed |
| RL | lookup_off | question | attn | value | 100 | 100% [96,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 100 | 99% [95,100] | 1% | -0.02 [-0.05,-0.00] | 0.98 | - | not_needed |
