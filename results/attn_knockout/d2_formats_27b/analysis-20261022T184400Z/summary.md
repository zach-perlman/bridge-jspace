# attn_knockout / d2_formats_27b

Measure: correct (items: {"PP": {"items": 155, "unedited_right": 155}, "PM": {"items": 155, "unedited_right": 155}, "MP": {"items": 159, "unedited_right": 159}, "MM": {"items": 159, "unedited_right": 158}})

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
     "acc": 0.05,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.931,
    "verdict": "partial"
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
     "acc": 0.116,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.116,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
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
  "PM": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.948,
     "verdict": "not_needed"
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
     "acc": 0.994,
     "verdict": "not_needed"
    },
    "attn": {
     "acc": 0.987,
     "verdict": "not_needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.975,
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
| MP | lookup | both | attn | value | 159 | 4% [2,8] | 79% | -4.25 [-4.50,-4.01] | - | +96 [+93,+99] | needed |
| MP | lookup | both | gdn | value | 159 | 99% [97,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| MP | lookup | final | all | value | 159 | 6% [3,10] | 77% | -3.38 [-3.61,-3.16] | 0.99 | +94 [+90,+97] | needed |
| MP | lookup | final | attn | value | 159 | 5% [3,10] | 77% | -3.34 [-3.58,-3.12] | - | +94 [+91,+97] | needed |
| MP | lookup | final | gdn | value | 159 | 99% [97,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| MP | lookup | question | all | value | 159 | 93% [88,96] | 7% | -0.13 [-0.18,-0.09] | 0.98 | +6 [+3,+9] | partial |
| MP | lookup | question | attn | value | 159 | 96% [91,98] | 4% | -0.11 [-0.16,-0.07] | - | - | not_needed |
| MP | lookup | question | gdn | value | 159 | 99% [97,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| MP | lookup_digit | final | all | value | 159 | 38% [31,45] | 40% | -2.07 [-2.35,-1.79] | 1.00 | +62 [+55,+70] | needed |
| MP | lookup_digit | question | all | value | 159 | 99% [96,100] | 1% | -0.02 [-0.03,-0.01] | 1.00 | - | not_needed |
| MP | lookup_name | final | all | value | 159 | 93% [88,96] | 6% | -0.08 [-0.12,-0.05] | 1.00 | +7 [+3,+11] | partial |
| MP | lookup_name | question | all | value | 159 | 94% [90,97] | 6% | -0.10 [-0.15,-0.07] | 1.00 | +3 [+0,+6] | partial |
| MP | lookup_nodigit | final | all | value | 159 | 92% [87,96] | 8% | -0.12 [-0.17,-0.08] | 0.99 | +8 [+4,+12] | partial |
| MP | lookup_nodigit | question | all | value | 159 | 95% [90,97] | 5% | -0.11 [-0.16,-0.07] | 0.98 | - | not_needed |
| MP | lookup_noname | final | all | value | 159 | 6% [3,10] | 70% | -3.32 [-3.56,-3.10] | 0.99 | +94 [+91,+97] | needed |
| MP | lookup_noname | question | all | value | 159 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| MP | lookup_off | both | attn | value | 159 | 100% [98,100] | 0% | +0.02 [+0.01,+0.04] | - | - | not_needed |
| MP | lookup_off | both | gdn | value | 159 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| MP | lookup_off | final | all | value | 159 | 99% [97,100] | 0% | +0.02 [+0.01,+0.04] | 0.99 | - | not_needed |
| MP | lookup_off | final | attn | value | 159 | 99% [97,100] | 0% | +0.02 [+0.01,+0.04] | - | - | not_needed |
| MP | lookup_off | final | gdn | value | 159 | 99% [96,100] | 1% | -0.01 [-0.03,+0.01] | 0.99 | - | not_needed |
| MP | lookup_off | question | all | value | 159 | 99% [96,100] | 1% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| MP | lookup_off | question | attn | value | 159 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| MP | lookup_off | question | gdn | value | 159 | 99% [97,100] | 1% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| MP | lookup_off_digit | final | all | value | 159 | 100% [98,100] | 0% | +0.02 [+0.01,+0.02] | 1.00 | - | not_needed |
| MP | lookup_off_digit | question | all | value | 159 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| MP | lookup_off_name | final | all | value | 159 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| MP | lookup_off_name | question | all | value | 159 | 97% [94,99] | 3% | -0.01 [-0.03,-0.00] | 1.00 | - | not_needed |
| MP | lookup_off_nodigit | final | all | value | 159 | 100% [98,100] | 0% | +0.01 [-0.01,+0.02] | 0.99 | - | not_needed |
| MP | lookup_off_nodigit | question | all | value | 159 | 99% [96,100] | 1% | -0.01 [-0.02,+0.01] | 0.98 | - | not_needed |
| MP | lookup_off_noname | final | all | value | 159 | 100% [98,100] | 0% | +0.02 [+0.01,+0.04] | 0.99 | - | not_needed |
| MP | lookup_off_noname | question | all | value | 159 | 99% [96,100] | 1% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| PP | lookup | both | attn | value | 155 | 7% [4,12] | 69% | -3.80 [-4.10,-3.50] | - | +93 [+88,+97] | needed |
| PP | lookup | both | gdn | value | 155 | 99% [96,100] | 1% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| PP | lookup | final | all | value | 155 | 12% [7,18] | 63% | -3.14 [-3.42,-2.86] | 0.99 | +88 [+83,+93] | needed |
| PP | lookup | final | attn | value | 155 | 12% [7,18] | 64% | -3.13 [-3.40,-2.86] | - | +88 [+83,+93] | needed |
| PP | lookup | final | gdn | value | 155 | 99% [96,100] | 1% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| PP | lookup | question | all | value | 155 | 99% [96,100] | 1% | -0.01 [-0.03,+0.00] | 0.98 | - | not_needed |
| PP | lookup | question | attn | value | 155 | 100% [98,100] | 0% | -0.00 [-0.02,+0.01] | - | - | not_needed |
| PP | lookup | question | gdn | value | 155 | 99% [96,100] | 1% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| PP | lookup_digit | final | all | value | 155 | 41% [33,49] | 32% | -1.94 [-2.21,-1.66] | 1.00 | +59 [+52,+67] | needed |
| PP | lookup_digit | question | all | value | 155 | 99% [96,100] | 1% | -0.01 [-0.03,-0.00] | 1.00 | - | not_needed |
| PP | lookup_name | final | all | value | 155 | 100% [98,100] | 0% | -0.01 [-0.02,-0.00] | 1.00 | - | not_needed |
| PP | lookup_name | question | all | value | 155 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| PP | lookup_nodigit | final | all | value | 155 | 99% [96,100] | 0% | -0.05 [-0.08,-0.03] | 0.99 | - | not_needed |
| PP | lookup_nodigit | question | all | value | 155 | 100% [98,100] | 0% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| PP | lookup_noname | final | all | value | 155 | 10% [6,15] | 67% | -3.24 [-3.50,-2.97] | 0.99 | +90 [+85,+95] | needed |
| PP | lookup_noname | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| PP | lookup_off | both | attn | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| PP | lookup_off | both | gdn | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| PP | lookup_off | final | all | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| PP | lookup_off | final | attn | value | 155 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| PP | lookup_off | final | gdn | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| PP | lookup_off | question | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| PP | lookup_off | question | attn | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off | question | gdn | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| PP | lookup_off_digit | final | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_digit | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.01,+0.00] | 1.00 | - | not_needed |
| PP | lookup_off_name | final | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_name | question | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PP | lookup_off_nodigit | final | all | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.99 | - | not_needed |
| PP | lookup_off_nodigit | question | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| PP | lookup_off_noname | final | all | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| PP | lookup_off_noname | question | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| PM | lookup | final | all | value | 155 | 95% [90,97] | 4% | -0.16 [-0.26,-0.07] | 0.99 | - | not_needed |
| PM | lookup | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| PM | lookup_digit | final | all | value | 155 | 99% [96,100] | 1% | +0.01 [+0.00,+0.02] | 1.00 | - | not_needed |
| PM | lookup_digit | question | all | value | 155 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| PM | lookup_name | final | all | value | 155 | 93% [88,96] | 5% | -0.19 [-0.29,-0.10] | 1.00 | +7 [+3,+12] | partial |
| PM | lookup_name | question | all | value | 155 | 99% [96,100] | 1% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| PM | lookup_nodigit | final | all | value | 155 | 94% [89,96] | 5% | -0.18 [-0.28,-0.09] | 0.99 | +6 [+3,+10] | partial |
| PM | lookup_nodigit | question | all | value | 155 | 99% [96,100] | 1% | -0.01 [-0.02,+0.00] | 0.98 | - | not_needed |
| PM | lookup_noname | final | all | value | 155 | 99% [95,100] | 1% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| PM | lookup_noname | question | all | value | 155 | 99% [96,100] | 1% | +0.01 [-0.00,+0.01] | 0.98 | - | not_needed |
| PM | lookup_off | final | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| PM | lookup_off | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| PM | lookup_off_digit | final | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| PM | lookup_off_digit | question | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| PM | lookup_off_name | final | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| PM | lookup_off_name | question | all | value | 155 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| PM | lookup_off_nodigit | final | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| PM | lookup_off_nodigit | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| PM | lookup_off_noname | final | all | value | 155 | 99% [96,100] | 1% | +0.00 [-0.01,+0.01] | 0.99 | - | not_needed |
| PM | lookup_off_noname | question | all | value | 155 | 99% [96,100] | 1% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| MM | lookup | both | attn | value | 158 | 96% [92,98] | 3% | -0.06 [-0.10,-0.03] | - | - | not_needed |
| MM | lookup | both | gdn | value | 158 | 99% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| MM | lookup | final | all | value | 158 | 99% [97,100] | 0% | -0.01 [-0.02,+0.00] | 0.99 | - | not_needed |
| MM | lookup | final | attn | value | 158 | 99% [96,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| MM | lookup | final | gdn | value | 158 | 99% [97,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup | question | all | value | 158 | 97% [94,99] | 1% | -0.05 [-0.08,-0.03] | 0.98 | - | not_needed |
| MM | lookup | question | attn | value | 158 | 98% [95,99] | 1% | -0.04 [-0.07,-0.03] | - | - | not_needed |
| MM | lookup | question | gdn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| MM | lookup_digit | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_digit | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_name | final | all | value | 158 | 98% [95,99] | 1% | -0.03 [-0.05,-0.01] | 1.00 | - | not_needed |
| MM | lookup_name | question | all | value | 158 | 97% [94,99] | 1% | -0.06 [-0.09,-0.04] | 1.00 | - | not_needed |
| MM | lookup_nodigit | final | all | value | 158 | 99% [97,100] | 0% | -0.02 [-0.03,-0.00] | 0.99 | - | not_needed |
| MM | lookup_nodigit | question | all | value | 158 | 97% [93,99] | 1% | -0.06 [-0.08,-0.03] | 0.98 | - | not_needed |
| MM | lookup_noname | final | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| MM | lookup_noname | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| MM | lookup_off | both | attn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| MM | lookup_off | both | gdn | value | 158 | 99% [97,100] | 0% | +0.00 [-0.01,+0.01] | 0.98 | - | not_needed |
| MM | lookup_off | final | all | value | 158 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| MM | lookup_off | final | attn | value | 158 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| MM | lookup_off | final | gdn | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| MM | lookup_off | question | attn | value | 158 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | question | gdn | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
| MM | lookup_off_digit | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_off_digit | question | all | value | 158 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| MM | lookup_off_name | final | all | value | 158 | 99% [97,100] | 1% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
| MM | lookup_off_name | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [-0.00,+0.01] | 1.00 | - | not_needed |
| MM | lookup_off_nodigit | final | all | value | 158 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| MM | lookup_off_nodigit | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.02] | 0.98 | - | not_needed |
| MM | lookup_off_noname | final | all | value | 158 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| MM | lookup_off_noname | question | all | value | 158 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.98 | - | not_needed |
