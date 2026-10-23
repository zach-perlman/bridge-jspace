# gen_spot / qwen35_9b_natplus_v1_chat_genspot_cand2_v1: 100 prompts at L12-16

Candidate read vs qwen35_9b_natplus_v1_chat_ko_cand2_v1: 394 of 400 agree.

| word / condition | n | cand acc | answer | lure | bridge | other cand | other |
|---|---|---|---|---|---|---|---|
| PP/none | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| PP/paper10 | 25 | 88 | 22 | 0 | 0 | 3 | 0 |
| PP/paper10_rot | 25 | 92 | 23 | 0 | 0 | 2 | 0 |
| PP/unembed10 | 25 | 96 | 24 | 0 | 0 | 1 | 0 |
| PM/none | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| PM/paper10 | 25 | 60 | 15 | 3 | 1 | 6 | 0 |
| PM/paper10_rot | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| PM/unembed10 | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| MP/none | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| MP/paper10 | 25 | 80 | 20 | 0 | 0 | 5 | 0 |
| MP/paper10_rot | 25 | 96 | 24 | 0 | 0 | 1 | 0 |
| MP/unembed10 | 25 | 96 | 24 | 0 | 0 | 1 | 0 |
| MM/none | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| MM/paper10 | 25 | 32 | 8 | 0 | 0 | 17 | 0 |
| MM/paper10_rot | 25 | 100 | 25 | 0 | 0 | 0 | 0 |
| MM/unembed10 | 25 | 100 | 25 | 0 | 0 | 0 | 0 |

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
