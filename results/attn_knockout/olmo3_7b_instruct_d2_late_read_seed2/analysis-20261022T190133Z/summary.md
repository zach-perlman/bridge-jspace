# attn_knockout / olmo3_7b_instruct_d2_late_read_seed2

Measure: correct (items: {"RL": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.0,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.24,
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
 "bands": {}
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | final | all | value | 100 | 0% [0,4] | 90% | -8.64 [-9.29,-7.98] | - | +98 [+95,+100] | needed |
| RL | lookup | question | all | value | 100 | 24% [17,33] | 19% | -3.09 [-3.47,-2.70] | - | +75 [+66,+83] | needed |
| RL | lookup_off | final | all | value | 100 | 98% [93,99] | 1% | -0.02 [-0.04,-0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 100 | 99% [95,100] | 0% | -0.01 [-0.03,+0.00] | - | - | not_needed |
