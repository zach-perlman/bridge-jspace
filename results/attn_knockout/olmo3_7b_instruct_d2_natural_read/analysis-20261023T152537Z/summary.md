# attn_knockout / olmo3_7b_instruct_d2_natural_read

Measure: correct (items: {"NAT": {"items": 428, "unedited_right": 426}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "NAT": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.047,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.636,
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
 "bands": {}
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NAT | lookup | after | all | value | 426 | 1% [1,3] | 0% | -11.01 [-11.47,-10.55] | - | +97 [+96,+99] | needed |
| NAT | lookup | final | all | value | 426 | 5% [3,7] | 0% | -10.51 [-11.06,-10.01] | - | +95 [+93,+97] | needed |
| NAT | lookup | question | all | value | 426 | 64% [59,68] | 0% | -1.79 [-2.10,-1.51] | - | +35 [+31,+40] | needed |
| NAT | lookup_off | after | all | value | 426 | 99% [97,99] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
| NAT | lookup_off | final | all | value | 426 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| NAT | lookup_off | question | all | value | 426 | 99% [97,99] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
