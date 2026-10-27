# attn_knockout / qwen36_27b_d2_natural_read

Measure: correct (items: {"NAT": {"items": 469, "unedited_right": 469}})

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
     "acc": 0.264,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.301,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.996,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.708,
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
| NAT | lookup | after | all | absent | 469 | 0% [0,1] | 0% | -8.35 [-8.70,-7.99] | 0.99 | +100 [+99,+100] | needed |
| NAT | lookup | after | all | value | 469 | 0% [0,2] | 0% | -8.11 [-8.45,-7.73] | 0.95 | +99 [+98,+100] | needed |
| NAT | lookup | both | all | absent | 469 | 2% [1,4] | 0% | -8.12 [-8.47,-7.75] | 0.99 | +98 [+97,+99] | needed |
| NAT | lookup | final | all | value | 469 | 26% [23,31] | 0% | -4.73 [-5.09,-4.35] | 0.98 | +73 [+69,+77] | needed |
| NAT | lookup | final | attn | value | 469 | 30% [26,34] | 0% | -3.75 [-4.06,-3.44] | - | +70 [+65,+74] | needed |
| NAT | lookup | final | gdn | value | 469 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| NAT | lookup | question | all | value | 469 | 71% [67,75] | 0% | -0.82 [-0.95,-0.71] | 0.97 | +29 [+25,+33] | needed |
| NAT | lookup_off | after | all | absent | 469 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| NAT | lookup_off | after | all | value | 469 | 99% [98,100] | 0% | -0.01 [-0.01,+0.00] | 0.95 | - | not_needed |
| NAT | lookup_off | both | all | absent | 469 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| NAT | lookup_off | final | all | value | 469 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| NAT | lookup_off | final | attn | value | 469 | 100% [99,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| NAT | lookup_off | final | gdn | value | 469 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| NAT | lookup_off | question | all | value | 469 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
