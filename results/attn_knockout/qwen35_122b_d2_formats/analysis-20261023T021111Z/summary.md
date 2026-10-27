# attn_knockout / qwen35_122b_d2_formats

Measure: correct (items: {"PP": {"items": 162, "unedited_right": 162}, "PM": {"items": 162, "unedited_right": 161}, "MP": {"items": 158, "unedited_right": 157}, "MM": {"items": 158, "unedited_right": 158}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "MP": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.057,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.045,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.962,
    "verdict": "not_needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "PP": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.037,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.049,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 1.0,
    "verdict": "not_needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "PM": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.907,
     "verdict": "partial"
    }
   },
   "question_all": {
    "acc": 0.994,
    "verdict": "not_needed"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "MM": {
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
    }
   },
   "question_all": {
    "acc": 1.0,
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
  "PP/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "PP/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "PP/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MP/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MP/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MP/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MM/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MM/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "MM/lookup/both": {
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
| MP | lookup | both | attn | value | 157 | 1% [0,5] | 91% | -4.31 [-4.55,-4.08] | - | +98 [+96,+100] | needed |
| MP | lookup | both | gdn | value | 157 | 99% [96,100] | 1% | -0.00 [-0.02,+0.01] | 0.99 | - | not_needed |
| MP | lookup | final | all | value | 157 | 6% [3,11] | 84% | -3.67 [-3.91,-3.43] | 0.99 | +94 [+90,+97] | needed |
| MP | lookup | final | attn | value | 157 | 4% [2,9] | 86% | -3.55 [-3.79,-3.32] | - | +96 [+92,+99] | needed |
| MP | lookup | final | gdn | value | 157 | 99% [96,100] | 1% | -0.01 [-0.04,+0.01] | 0.99 | - | not_needed |
| MP | lookup | question | all | value | 157 | 96% [92,98] | 4% | -0.11 [-0.15,-0.07] | 0.98 | - | not_needed |
| MP | lookup | question | attn | value | 157 | 96% [92,98] | 4% | -0.08 [-0.12,-0.05] | - | - | not_needed |
| MP | lookup | question | gdn | value | 157 | 99% [96,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| MP | lookup_digit | final | all | value | 157 | 33% [26,41] | 53% | -2.51 [-2.84,-2.19] | 1.00 | +67 [+59,+74] | needed |
| MP | lookup_digit | question | all | value | 157 | 100% [98,100] | 0% | -0.02 [-0.03,-0.01] | 1.00 | - | not_needed |
| MP | lookup_name | final | all | value | 157 | 96% [91,98] | 4% | -0.08 [-0.12,-0.05] | 1.00 | - | not_needed |
| MP | lookup_name | question | all | value | 157 | 97% [94,99] | 3% | -0.07 [-0.10,-0.04] | 1.00 | - | not_needed |
| MP | lookup_nodigit | final | all | value | 157 | 92% [87,96] | 8% | -0.18 [-0.25,-0.11] | 0.99 | +7 [+3,+11] | partial |
| MP | lookup_nodigit | question | all | value | 157 | 97% [94,99] | 3% | -0.08 [-0.11,-0.05] | 0.98 | - | not_needed |
| MP | lookup_noname | final | all | value | 157 | 9% [5,14] | 79% | -3.53 [-3.79,-3.28] | 0.99 | +91 [+87,+96] | needed |
| MP | lookup_noname | question | all | value | 157 | 99% [96,100] | 1% | -0.02 [-0.04,-0.01] | 0.98 | - | not_needed |
| MP | lookup_off | both | attn | value | 157 | 99% [96,100] | 1% | +0.02 [+0.00,+0.03] | - | - | not_needed |
| MP | lookup_off | both | gdn | value | 157 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| MP | lookup_off | final | all | value | 157 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| MP | lookup_off | final | attn | value | 157 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| MP | lookup_off | final | gdn | value | 157 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| MP | lookup_off | question | all | value | 157 | 99% [96,100] | 1% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| MP | lookup_off | question | attn | value | 157 | 99% [96,100] | 1% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| MP | lookup_off | question | gdn | value | 157 | 99% [96,100] | 1% | +0.01 [-0.00,+0.02] | 0.98 | - | not_needed |
| MP | lookup_off_digit | final | all | value | 157 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 1.00 | - | not_needed |
| MP | lookup_off_digit | question | all | value | 157 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| MP | lookup_off_name | final | all | value | 157 | 99% [95,100] | 1% | -0.01 [-0.04,+0.00] | 1.00 | - | not_needed |
| MP | lookup_off_name | question | all | value | 157 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| MP | lookup_off_nodigit | final | all | value | 157 | 99% [96,100] | 1% | +0.01 [-0.01,+0.02] | 0.99 | - | not_needed |
| MP | lookup_off_nodigit | question | all | value | 157 | 99% [95,100] | 1% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| MP | lookup_off_noname | final | all | value | 157 | 100% [98,100] | 0% | +0.02 [+0.01,+0.03] | 0.99 | - | not_needed |
| MP | lookup_off_noname | question | all | value | 157 | 99% [96,100] | 1% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| PP | lookup | both | attn | value | 162 | 3% [1,7] | 91% | -4.13 [-4.37,-3.90] | - | +97 [+94,+99] | needed |
| PP | lookup | both | gdn | value | 162 | 99% [97,100] | 1% | -0.02 [-0.04,-0.00] | 0.99 | - | not_needed |
| PP | lookup | final | all | value | 162 | 4% [2,8] | 87% | -3.84 [-4.04,-3.62] | 0.99 | +96 [+93,+99] | needed |
| PP | lookup | final | attn | value | 162 | 5% [3,9] | 85% | -3.66 [-3.88,-3.45] | - | +95 [+91,+98] | needed |
| PP | lookup | final | gdn | value | 162 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| PP | lookup | question | all | value | 162 | 100% [98,100] | 0% | -0.02 [-0.03,-0.01] | 0.98 | - | not_needed |
| PP | lookup | question | attn | value | 162 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| PP | lookup | question | gdn | value | 162 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| PP | lookup_digit | final | all | value | 162 | 30% [23,37] | 56% | -2.57 [-2.88,-2.27] | 1.00 | +70 [+63,+78] | needed |
| PP | lookup_digit | question | all | value | 162 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| PP | lookup_name | final | all | value | 162 | 99% [97,100] | 1% | -0.05 [-0.07,-0.03] | 1.00 | - | not_needed |
| PP | lookup_name | question | all | value | 162 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 1.00 | - | not_needed |
| PP | lookup_nodigit | final | all | value | 162 | 94% [90,97] | 6% | -0.15 [-0.20,-0.11] | 0.99 | +6 [+2,+9] | partial |
| PP | lookup_nodigit | question | all | value | 162 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| PP | lookup_noname | final | all | value | 162 | 2% [1,6] | 85% | -3.72 [-3.92,-3.52] | 0.99 | +98 [+95,+99] | needed |
| PP | lookup_noname | question | all | value | 162 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| PP | lookup_off | both | attn | value | 162 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| PP | lookup_off | both | gdn | value | 162 | 99% [97,100] | 1% | -0.01 [-0.03,-0.00] | 0.99 | - | not_needed |
| PP | lookup_off | final | all | value | 162 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| PP | lookup_off | final | attn | value | 162 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| PP | lookup_off | final | gdn | value | 162 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| PP | lookup_off | question | all | value | 162 | 99% [97,100] | 1% | -0.00 [-0.02,+0.00] | 0.98 | - | not_needed |
| PP | lookup_off | question | attn | value | 162 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| PP | lookup_off | question | gdn | value | 162 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| PP | lookup_off_digit | final | all | value | 162 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_digit | question | all | value | 162 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_name | final | all | value | 162 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_name | question | all | value | 162 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| PP | lookup_off_nodigit | final | all | value | 162 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| PP | lookup_off_nodigit | question | all | value | 162 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| PP | lookup_off_noname | final | all | value | 162 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| PP | lookup_off_noname | question | all | value | 162 | 100% [98,100] | 0% | -0.00 [-0.02,+0.01] | 0.98 | - | not_needed |
| PM | lookup | final | all | value | 161 | 91% [85,94] | 7% | -0.22 [-0.34,-0.11] | 0.99 | +9 [+5,+13] | partial |
| PM | lookup | question | all | value | 161 | 99% [97,100] | 0% | +0.00 [-0.01,+0.02] | 0.98 | - | not_needed |
| PM | lookup_digit | final | all | value | 161 | 100% [98,100] | 0% | +0.03 [+0.01,+0.04] | 1.00 | - | not_needed |
| PM | lookup_digit | question | all | value | 161 | 99% [96,100] | 0% | +0.01 [-0.00,+0.01] | 1.00 | - | not_needed |
| PM | lookup_name | final | all | value | 161 | 86% [79,90] | 11% | -0.32 [-0.47,-0.20] | 1.00 | +13 [+8,+19] | partial |
| PM | lookup_name | question | all | value | 161 | 99% [97,100] | 0% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| PM | lookup_nodigit | final | all | value | 161 | 86% [80,91] | 9% | -0.31 [-0.45,-0.19] | 0.99 | +12 [+7,+17] | partial |
| PM | lookup_nodigit | question | all | value | 161 | 98% [95,99] | 0% | -0.01 [-0.03,+0.00] | 0.98 | - | not_needed |
| PM | lookup_noname | final | all | value | 161 | 100% [98,100] | 0% | +0.02 [+0.00,+0.05] | 0.99 | - | not_needed |
| PM | lookup_noname | question | all | value | 161 | 99% [97,100] | 0% | +0.02 [+0.01,+0.03] | 0.99 | - | not_needed |
| PM | lookup_off | final | all | value | 161 | 99% [97,100] | 0% | +0.01 [-0.00,+0.02] | 0.99 | - | not_needed |
| PM | lookup_off | question | all | value | 161 | 99% [97,100] | 1% | +0.01 [-0.01,+0.02] | 0.98 | - | not_needed |
| PM | lookup_off_digit | final | all | value | 161 | 99% [97,100] | 0% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| PM | lookup_off_digit | question | all | value | 161 | 99% [97,100] | 0% | +0.01 [-0.01,+0.02] | 1.00 | - | not_needed |
| PM | lookup_off_name | final | all | value | 161 | 99% [96,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PM | lookup_off_name | question | all | value | 161 | 99% [96,100] | 0% | +0.01 [-0.00,+0.02] | 1.00 | - | not_needed |
| PM | lookup_off_nodigit | final | all | value | 161 | 99% [96,100] | 1% | -0.00 [-0.03,+0.01] | 0.99 | - | not_needed |
| PM | lookup_off_nodigit | question | all | value | 161 | 98% [94,99] | 1% | -0.03 [-0.07,-0.00] | 0.98 | - | not_needed |
| PM | lookup_off_noname | final | all | value | 161 | 99% [96,100] | 1% | -0.00 [-0.02,+0.02] | 0.99 | - | not_needed |
| PM | lookup_off_noname | question | all | value | 161 | 98% [95,99] | 1% | -0.01 [-0.04,+0.01] | 0.99 | - | not_needed |
| MM | lookup | both | attn | value | 158 | 100% [98,100] | 0% | -0.01 [-0.02,+0.00] | - | - | not_needed |
| MM | lookup | both | gdn | value | 158 | 100% [98,100] | 0% | -0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| MM | lookup | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup | final | attn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup | final | gdn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup | question | all | value | 158 | 100% [98,100] | 0% | -0.02 [-0.03,-0.01] | 0.99 | - | not_needed |
| MM | lookup | question | attn | value | 158 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| MM | lookup | question | gdn | value | 158 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| MM | lookup_digit | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_digit | question | all | value | 158 | 99% [97,100] | 1% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| MM | lookup_name | final | all | value | 158 | 99% [97,100] | 1% | -0.02 [-0.02,-0.01] | 1.00 | - | not_needed |
| MM | lookup_name | question | all | value | 158 | 99% [97,100] | 1% | -0.02 [-0.03,-0.01] | 1.00 | - | not_needed |
| MM | lookup_nodigit | final | all | value | 158 | 100% [98,100] | 0% | -0.01 [-0.01,+0.00] | 0.99 | - | not_needed |
| MM | lookup_nodigit | question | all | value | 158 | 100% [98,100] | 0% | -0.02 [-0.03,-0.01] | 0.99 | - | not_needed |
| MM | lookup_noname | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| MM | lookup_noname | question | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off | both | attn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | both | gdn | value | 158 | 99% [97,100] | 1% | +0.00 [-0.01,+0.02] | 0.99 | - | not_needed |
| MM | lookup_off | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off | final | attn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | final | gdn | value | 158 | 99% [97,100] | 1% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off | question | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off | question | attn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | question | gdn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off_digit | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| MM | lookup_off_digit | question | all | value | 158 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| MM | lookup_off_name | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| MM | lookup_off_name | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_off_nodigit | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off_nodigit | question | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off_noname | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| MM | lookup_off_noname | question | all | value | 158 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.99 | - | not_needed |
