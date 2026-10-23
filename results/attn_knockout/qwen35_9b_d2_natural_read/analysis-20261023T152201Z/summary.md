# attn_knockout / qwen35_9b_d2_natural_read

Measure: correct (items: {"NAT": {"items": 503, "unedited_right": 502}})

Claims: {
 "positive_control": {
  "NAT": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  }
 },
 "late_attention_read": {
  "NAT": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.076,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.994,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.813,
    "verdict": "partial"
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
  "NAT/lookup/final": {
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
| NAT | lookup | after | all | absent | 502 | 1% [0,2] | 0% | -8.76 [-9.09,-8.42] | 0.99 | +98 [+97,+99] | needed |
| NAT | lookup | after | all | value | 502 | 1% [0,2] | 0% | -8.67 [-9.01,-8.34] | 0.95 | +98 [+97,+99] | needed |
| NAT | lookup | both | all | absent | 502 | 2% [1,3] | 0% | -8.78 [-9.09,-8.45] | 0.99 | +97 [+96,+99] | needed |
| NAT | lookup | final | all | value | 502 | 5% [3,7] | 0% | -7.41 [-7.72,-7.06] | 0.98 | +95 [+93,+97] | needed |
| NAT | lookup | final | attn | value | 502 | 8% [6,10] | 0% | -6.04 [-6.32,-5.74] | - | +92 [+90,+95] | needed |
| NAT | lookup | final | gdn | value | 502 | 99% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.98 | - | not_needed |
| NAT | lookup | question | all | value | 502 | 81% [78,84] | 0% | -0.66 [-0.77,-0.56] | 0.97 | +18 [+15,+22] | partial |
| NAT | lookup_off | after | all | absent | 502 | 99% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| NAT | lookup_off | after | all | value | 502 | 99% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | not_needed |
| NAT | lookup_off | both | all | absent | 502 | 99% [98,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| NAT | lookup_off | final | all | value | 502 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| NAT | lookup_off | final | attn | value | 502 | 100% [99,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| NAT | lookup_off | final | gdn | value | 502 | 99% [98,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| NAT | lookup_off | question | all | value | 502 | 99% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.97 | - | not_needed |
