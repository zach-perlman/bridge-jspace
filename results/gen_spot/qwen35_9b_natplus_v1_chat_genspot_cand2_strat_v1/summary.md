# gen_spot / qwen35_9b_natplus_v1_chat_genspot_cand2_strat_v1: 368 prompts at L12-16

Candidate read vs qwen35_9b_natplus_v1_chat_ko_cand2_v1: 1455 of 1472 agree.

| word / condition | n | cand acc | answer | lure | bridge | other cand | other |
|---|---|---|---|---|---|---|---|
| PP/none | 100 | 100 | 100 | 0 | 0 | 0 | 0 |
| PP/paper10 | 100 | 87 | 86 | 0 | 0 | 11 | 3 |
| PP/paper10_rot | 100 | 95 | 95 | 0 | 0 | 5 | 0 |
| PP/unembed10 | 100 | 95 | 95 | 0 | 0 | 5 | 0 |
| PM/none | 99 | 100 | 94 | 0 | 2 | 0 | 3 |
| PM/paper10 | 99 | 50 | 46 | 17 | 5 | 28 | 3 |
| PM/paper10_rot | 99 | 94 | 89 | 4 | 1 | 1 | 4 |
| PM/unembed10 | 99 | 99 | 91 | 1 | 4 | 0 | 3 |
| MP/none | 84 | 100 | 84 | 0 | 0 | 0 | 0 |
| MP/paper10 | 84 | 90 | 76 | 0 | 0 | 8 | 0 |
| MP/paper10_rot | 84 | 93 | 78 | 0 | 0 | 6 | 0 |
| MP/unembed10 | 84 | 95 | 80 | 0 | 0 | 4 | 0 |
| MM/none | 84 | 100 | 79 | 0 | 2 | 0 | 3 |
| MM/paper10 | 84 | 45 | 37 | 0 | 0 | 38 | 9 |
| MM/paper10_rot | 84 | 98 | 76 | 0 | 6 | 0 | 2 |
| MM/unembed10 | 84 | 100 | 79 | 0 | 2 | 0 | 3 |

## examples (first 3 items per word)

- PP np:chat:PP-L0-0005 (answer Europe, bridge Bhutan): none: 'Europe\n'; paper10: 'Europe\n'; paper10_rot: 'Europe\n'; unembed10: 'Europe\n'
- PP np:chat:PP-L0-0009 (answer Africa, bridge Bolivia): none: 'Africa\n'; paper10: 'Africa\n'; paper10_rot: 'Africa\n'; unembed10: 'Africa\n'
- PP np:chat:PP-L0-0013 (answer North America, bridge Botswana): none: 'North America\n'; paper10: 'Europe\n'; paper10_rot: 'North America\n'; unembed10: 'North America\n'
- PM np:chat:PM-L0-0005 (answer Asia, bridge Bhutan): none: 'Asia\n'; paper10: 'Asia\n'; paper10_rot: 'Asia\n'; unembed10: 'Asia\n'
- PM np:chat:PM-L0-0009 (answer South America, bridge Bolivia): none: 'South America\n'; paper10: 'Europe\n'; paper10_rot: 'South America\n'; unembed10: 'South America\n'
- PM np:chat:PM-L0-0013 (answer Africa, bridge Botswana): none: 'Africa\n'; paper10: 'Europe\n'; paper10_rot: 'Africa\n'; unembed10: 'Africa\n'
- MP np:chat:MP-L0-0004 (answer North America, bridge Argentina): none: 'North America\n'; paper10: 'Europe\n'; paper10_rot: 'North America\n'; unembed10: 'North America\n'
- MP np:chat:MP-L0-0006 (answer Africa, bridge Bhutan): none: 'Africa\n'; paper10: 'Europe\n'; paper10_rot: 'Europe\n'; unembed10: 'Europe\n'
- MP np:chat:MP-L0-0008 (answer Africa, bridge Bhutan): none: 'Africa\n'; paper10: 'Africa\n'; paper10_rot: 'Africa\n'; unembed10: 'Africa\n'
- MM np:chat:MM-L0-0004 (answer South America, bridge Argentina): none: 'South America\n'; paper10: 'Europe\n'; paper10_rot: 'South America\n'; unembed10: 'South America\n'
- MM np:chat:MM-L0-0006 (answer Asia, bridge Bhutan): none: 'Asia\n'; paper10: 'Europe\n'; paper10_rot: 'Asia\n'; unembed10: 'Asia\n'
- MM np:chat:MM-L0-0008 (answer Asia, bridge Bhutan): none: 'Asia\n'; paper10: 'Europe\n'; paper10_rot: 'Asia\n'; unembed10: 'Asia\n'
