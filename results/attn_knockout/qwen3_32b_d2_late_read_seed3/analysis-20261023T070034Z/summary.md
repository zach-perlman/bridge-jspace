# attn_knockout / qwen3_32b_d2_late_read_seed3

Measure: correct (items: {"RL": {"items": 200, "unedited_right": 199}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.01,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.342,
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
| RL | lookup | final | all | value | 199 | 1% [0,4] | 94% | -9.32 [-9.79,-8.86] | - | +99 [+97,+100] | needed |
| RL | lookup | question | all | value | 199 | 34% [28,41] | 13% | -3.07 [-3.43,-2.70] | - | +65 [+58,+71] | needed |
| RL | lookup_off | final | all | value | 199 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 199 | 99% [96,100] | 1% | -0.04 [-0.10,-0.00] | - | - | not_needed |
