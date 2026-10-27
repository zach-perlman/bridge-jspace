# attn_knockout / qwen3_32b_d2_formats

Measure: correct (items: {"PP": {"items": 117, "unedited_right": 117}, "PM": {"items": 117, "unedited_right": 117}, "MP": {"items": 111, "unedited_right": 111}, "MM": {"items": 111, "unedited_right": 111}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "MP": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.018,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.802,
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
     "acc": 0.034,
     "verdict": "needed"
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
     "acc": 0.957,
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
  "MM": {
   "path": false,
   "final": {
    "all": {
     "acc": 0.973,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.982,
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
 "bands": {}
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MP | lookup | final | all | value | 111 | 2% [0,6] | 95% | -10.37 [-10.99,-9.76] | - | +98 [+95,+100] | needed |
| MP | lookup | question | all | value | 111 | 80% [72,87] | 19% | -0.58 [-0.89,-0.30] | - | +16 [+9,+24] | partial |
| MP | lookup_digit | final | all | value | 111 | 21% [14,29] | 75% | -7.81 [-8.72,-6.91] | - | +79 [+71,+86] | needed |
| MP | lookup_digit | question | all | value | 111 | 99% [95,100] | 1% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| MP | lookup_name | final | all | value | 111 | 93% [86,96] | 7% | -0.14 [-0.25,-0.05] | - | +7 [+3,+13] | partial |
| MP | lookup_name | question | all | value | 111 | 85% [77,90] | 15% | -0.50 [-0.79,-0.25] | - | +12 [+5,+19] | partial |
| MP | lookup_nodigit | final | all | value | 111 | 90% [83,94] | 9% | -0.20 [-0.34,-0.08] | - | +10 [+5,+15] | partial |
| MP | lookup_nodigit | question | all | value | 111 | 78% [70,85] | 22% | -0.58 [-0.88,-0.31] | - | +17 [+9,+25] | partial |
| MP | lookup_noname | final | all | value | 111 | 2% [0,6] | 93% | -10.12 [-10.77,-9.46] | - | +98 [+95,+100] | needed |
| MP | lookup_noname | question | all | value | 111 | 99% [95,100] | 1% | -0.01 [-0.02,+0.01] | - | - | not_needed |
| MP | lookup_off | final | all | value | 111 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| MP | lookup_off | question | all | value | 111 | 96% [91,99] | 4% | -0.06 [-0.13,-0.00] | - | - | not_needed |
| MP | lookup_off_digit | final | all | value | 111 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| MP | lookup_off_digit | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MP | lookup_off_name | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| MP | lookup_off_name | question | all | value | 111 | 96% [91,99] | 4% | -0.08 [-0.16,-0.01] | - | - | not_needed |
| MP | lookup_off_nodigit | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| MP | lookup_off_nodigit | question | all | value | 111 | 95% [90,98] | 5% | -0.07 [-0.14,-0.01] | - | - | partial |
| MP | lookup_off_noname | final | all | value | 111 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| MP | lookup_off_noname | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
| PP | lookup | final | all | value | 117 | 3% [1,8] | 86% | -9.05 [-9.68,-8.39] | - | +96 [+92,+99] | needed |
| PP | lookup | question | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_digit | final | all | value | 117 | 25% [18,33] | 62% | -6.42 [-7.24,-5.55] | - | +74 [+66,+82] | needed |
| PP | lookup_digit | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_name | final | all | value | 117 | 99% [95,100] | 1% | -0.05 [-0.14,-0.00] | - | - | not_needed |
| PP | lookup_name | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_nodigit | final | all | value | 117 | 97% [92,99] | 3% | -0.08 [-0.18,-0.01] | - | - | not_needed |
| PP | lookup_nodigit | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_noname | final | all | value | 117 | 3% [1,8] | 86% | -8.71 [-9.36,-8.04] | - | +96 [+92,+99] | needed |
| PP | lookup_noname | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off | final | all | value | 117 | 99% [95,100] | 1% | -0.04 [-0.12,+0.00] | - | - | not_needed |
| PP | lookup_off | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off_digit | final | all | value | 117 | 99% [95,100] | 1% | -0.02 [-0.06,+0.00] | - | - | not_needed |
| PP | lookup_off_digit | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off_name | final | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| PP | lookup_off_name | question | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| PP | lookup_off_nodigit | final | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off_nodigit | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PP | lookup_off_noname | final | all | value | 117 | 99% [95,100] | 1% | -0.04 [-0.12,+0.00] | - | - | not_needed |
| PP | lookup_off_noname | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| PM | lookup | final | all | value | 117 | 96% [90,98] | 4% | -0.20 [-0.44,-0.02] | - | - | not_needed |
| PM | lookup | question | all | value | 117 | 100% [97,100] | 0% | +0.02 [+0.01,+0.03] | - | - | not_needed |
| PM | lookup_digit | final | all | value | 117 | 100% [97,100] | 0% | +0.03 [+0.02,+0.04] | - | - | not_needed |
| PM | lookup_digit | question | all | value | 117 | 100% [97,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| PM | lookup_name | final | all | value | 117 | 90% [83,94] | 5% | -0.42 [-0.71,-0.19] | - | +10 [+5,+16] | partial |
| PM | lookup_name | question | all | value | 117 | 99% [95,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| PM | lookup_nodigit | final | all | value | 117 | 89% [82,93] | 6% | -0.43 [-0.72,-0.20] | - | +11 [+6,+17] | partial |
| PM | lookup_nodigit | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| PM | lookup_noname | final | all | value | 117 | 100% [97,100] | 0% | +0.03 [+0.02,+0.04] | - | - | not_needed |
| PM | lookup_noname | question | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.01,+0.02] | - | - | not_needed |
| PM | lookup_off | final | all | value | 117 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| PM | lookup_off | question | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| PM | lookup_off_digit | final | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| PM | lookup_off_digit | question | all | value | 117 | 100% [97,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| PM | lookup_off_name | final | all | value | 117 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| PM | lookup_off_name | question | all | value | 117 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| PM | lookup_off_nodigit | final | all | value | 117 | 100% [97,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| PM | lookup_off_nodigit | question | all | value | 117 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| PM | lookup_off_noname | final | all | value | 117 | 100% [97,100] | 0% | +0.01 [+0.00,+0.02] | - | - | not_needed |
| PM | lookup_off_noname | question | all | value | 117 | 98% [94,100] | 2% | -0.03 [-0.05,-0.01] | - | - | not_needed |
| MM | lookup | final | all | value | 111 | 97% [92,99] | 1% | -0.07 [-0.14,-0.01] | - | - | not_needed |
| MM | lookup | question | all | value | 111 | 98% [94,100] | 0% | -0.03 [-0.08,+0.00] | - | - | not_needed |
| MM | lookup_digit | final | all | value | 111 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_digit | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| MM | lookup_name | final | all | value | 111 | 96% [91,99] | 2% | -0.16 [-0.36,-0.03] | - | - | not_needed |
| MM | lookup_name | question | all | value | 111 | 98% [94,100] | 0% | -0.04 [-0.09,+0.00] | - | - | not_needed |
| MM | lookup_nodigit | final | all | value | 111 | 96% [91,99] | 2% | -0.15 [-0.34,-0.03] | - | - | not_needed |
| MM | lookup_nodigit | question | all | value | 111 | 98% [94,100] | 0% | -0.04 [-0.10,+0.00] | - | - | not_needed |
| MM | lookup_noname | final | all | value | 111 | 100% [97,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_noname | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_off | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off_digit | final | all | value | 111 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| MM | lookup_off_digit | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| MM | lookup_off_name | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off_name | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| MM | lookup_off_nodigit | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_off_nodigit | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| MM | lookup_off_noname | final | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| MM | lookup_off_noname | question | all | value | 111 | 100% [97,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
