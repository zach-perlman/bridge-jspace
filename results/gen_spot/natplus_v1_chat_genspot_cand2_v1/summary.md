# gen_spot / natplus_v1_chat_genspot_cand2_v1: 386 prompts at L32-40

Candidate read vs natplus_v1_chat_ko_cand2_v1: 1530 of 1544 agree.

| word / condition | n | cand acc | answer | lure | bridge | other cand | other |
|---|---|---|---|---|---|---|---|
| PP/none | 100 | 100 | 100 | 0 | 0 | 0 | 0 |
| PP/paper10 | 100 | 98 | 98 | 0 | 0 | 2 | 0 |
| PP/paper10_rot | 100 | 97 | 97 | 0 | 0 | 3 | 0 |
| PP/unembed10 | 100 | 99 | 99 | 0 | 0 | 1 | 0 |
| PM/none | 100 | 100 | 97 | 0 | 0 | 0 | 3 |
| PM/paper10 | 100 | 44 | 43 | 39 | 1 | 15 | 2 |
| PM/paper10_rot | 100 | 98 | 93 | 1 | 0 | 1 | 5 |
| PM/unembed10 | 100 | 98 | 92 | 1 | 0 | 1 | 6 |
| MP/none | 93 | 100 | 93 | 0 | 0 | 0 | 0 |
| MP/paper10 | 93 | 94 | 87 | 0 | 0 | 6 | 0 |
| MP/paper10_rot | 93 | 99 | 92 | 0 | 0 | 1 | 0 |
| MP/unembed10 | 93 | 100 | 93 | 0 | 0 | 0 | 0 |
| MM/none | 92 | 100 | 83 | 0 | 2 | 0 | 7 |
| MM/paper10 | 92 | 46 | 35 | 0 | 0 | 38 | 19 |
| MM/paper10_rot | 92 | 98 | 80 | 0 | 2 | 1 | 9 |
| MM/unembed10 | 92 | 99 | 83 | 0 | 2 | 0 | 7 |

## examples (first 3 items per word)

- PP np:chat:PP-L0-0005 (answer Europe, bridge Bhutan): none: 'Europe'; paper10: 'Europe'; paper10_rot: 'Europe'; unembed10: 'Europe'
- PP np:chat:PP-L0-0013 (answer North America, bridge Botswana): none: 'North America'; paper10: 'North America'; paper10_rot: 'North America'; unembed10: 'North America'
- PP np:chat:PP-L0-0015 (answer Europe, bridge Botswana): none: 'Europe'; paper10: 'Europe'; paper10_rot: 'Europe'; unembed10: 'Europe'
- PM np:chat:PM-L0-0005 (answer Asia, bridge Bhutan): none: 'Asia'; paper10: 'Asia'; paper10_rot: 'Asia'; unembed10: 'Asia'
- PM np:chat:PM-L0-0013 (answer Africa, bridge Botswana): none: 'Africa'; paper10: 'South America'; paper10_rot: 'Africa'; unembed10: 'Africa'
- PM np:chat:PM-L0-0015 (answer Africa, bridge Botswana): none: 'Africa'; paper10: 'Africa'; paper10_rot: 'Africa'; unembed10: 'Africa'
- MP np:chat:MP-L0-0006 (answer Africa, bridge Bhutan): none: 'Africa'; paper10: 'Africa'; paper10_rot: 'Africa'; unembed10: 'Africa'
- MP np:chat:MP-L0-0008 (answer Africa, bridge Bhutan): none: 'Africa'; paper10: 'Africa'; paper10_rot: 'Africa'; unembed10: 'Africa'
- MP np:chat:MP-L0-0010 (answer Africa, bridge Bolivia): none: 'Africa'; paper10: 'Africa'; paper10_rot: 'Africa'; unembed10: 'Africa'
- MM np:chat:MM-L0-0006 (answer Asia, bridge Bhutan): none: 'Asia'; paper10: 'Asia'; paper10_rot: 'Asia'; unembed10: 'Asia'
- MM np:chat:MM-L0-0008 (answer Asia, bridge Bhutan): none: 'Asia'; paper10: 'Africa'; paper10_rot: 'Asia'; unembed10: 'Asia'
- MM np:chat:MM-L0-0010 (answer South America, bridge Bolivia): none: 'South America'; paper10: 'South America'; paper10_rot: 'South America'; unembed10: 'South America'
