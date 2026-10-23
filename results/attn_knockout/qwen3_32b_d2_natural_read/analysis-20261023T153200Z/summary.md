# attn_knockout / qwen3_32b_d2_natural_read

Measure: correct (items: {"NAT": {"items": 443, "unedited_right": 442}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "NAT": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.07,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.758,
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
| NAT | lookup | after | all | value | 442 | 0% [0,1] | 0% | -13.45 [-13.97,-12.94] | - | +99 [+98,+100] | needed |
| NAT | lookup | final | all | value | 442 | 7% [5,10] | 0% | -11.71 [-12.27,-11.15] | - | +93 [+90,+95] | needed |
| NAT | lookup | question | all | value | 442 | 76% [72,80] | 0% | -1.01 [-1.23,-0.80] | - | +24 [+20,+27] | needed |
| NAT | lookup_off | after | all | value | 442 | 99% [97,99] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| NAT | lookup_off | final | all | value | 442 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| NAT | lookup_off | question | all | value | 442 | 99% [98,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
