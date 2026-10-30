# Is the address verbalizable by the J++ lens? (post hoc, CPU)

Verdict by the pre-set rule: **not verbalizable by the J++ lens at this layer; consistent with the claim** (models meeting both conditions: 0 of 5)

## muse-glimmer-30b (L26, d = 6656)

Base rate: {'dictionary_tokens': 190773, 'ordinal_tokens': 125, 'cardinal_tokens': 265, 'generic_tokens': 220, 'position_tokens': 589, 'base_rate_any_position_class': 0.003087}

(a) position-atom energy share (mean over the six writes) 0.0 vs random 95th percentile 0.00169 (random mean 0.00015, shuffle mean 0.0); sign-correct ordinal on 0 of 6 pairs (rate 0.0) vs shuffle 0.0, random mean 0.007 / 95th percentile 0.0; rule: {'share_above_random_p95': False, 'sign_correct_on_most_pairs_above_shuffle': False, 'both': False}

Overlap: the 25-atom J++ part captures 0.0622 of the pointer basis directions' energy ([0.0478, 0.0597, 0.0632, 0.0781]), the six writes [0.0591, 0.0615, 0.066], random vectors 0.0523

| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |
|---|---|---|---|
| 0->1 | 0.0 | False | ' ramai' + 0.0040 -; 'にとって' - 0.0038 -; 'idenav' + 0.0037 -; ' V' - 0.0029 -; 'izzera' + 0.0029 -; '_REFERENCE' - 0.0031 -; ' acestuia' + 0.0028 -; ' blod' - 0.0027 -; '楼' + 0.0024 -; 'LR' - 0.0025 - |
| 0->2 | 0.0 | False | ' ebenfalls' + 0.0043 -; 'にとって' - 0.0035 -; ' ramai' + 0.0037 -; ' Tit' - 0.0028 -; 'idenav' + 0.0025 -; 'жар' - 0.0031 -; 'ซื้อ' + 0.0024 -; '-associated' - 0.0026 -; 'izzera' + 0.0023 -; 'embali' - 0.0027 - |
| 1->0 | 0.0 | False | ' ramai' - 0.0040 -; 'にとって' + 0.0038 -; 'idenav' - 0.0037 -; ' V' + 0.0029 -; 'izzera' - 0.0029 -; '_REFERENCE' + 0.0031 -; ' acestuia' - 0.0028 -; ' blod' + 0.0027 -; '楼' - 0.0024 -; 'LR' + 0.0025 - |
| 1->2 | 0.0 | False | ' Plen' + 0.0032 -; ' Beet' - 0.0037 -; 'abama' + 0.0028 -; "ley's" - 0.0029 -; 'Reasons' + 0.0026 -; 'degrees' - 0.0032 -; ' Fitch' - 0.0021 -; ' også' + 0.0023 -; ' titre' - 0.0027 -; ' Hits' + 0.0023 - |
| 2->0 | 0.0 | False | ' ebenfalls' - 0.0043 -; 'にとって' + 0.0035 -; ' ramai' - 0.0037 -; ' Tit' + 0.0028 -; 'idenav' - 0.0025 -; 'жар' + 0.0031 -; 'ซื้อ' - 0.0024 -; '-associated' + 0.0026 -; 'izzera' - 0.0023 -; 'embali' + 0.0027 - |
| 2->1 | 0.0 | False | ' Plen' - 0.0032 -; ' Beet' + 0.0037 -; 'abama' - 0.0028 -; "ley's" + 0.0029 -; 'Reasons' - 0.0026 -; 'degrees' + 0.0032 -; ' Fitch' + 0.0021 -; ' også' - 0.0023 -; ' titre' + 0.0027 -; ' Hits' - 0.0023 - |

(b) 30 random C2 scenes (seed 29): mean position share 0.00098, ambiguous (cardinal equal to a locker digit) 0.0, sign-correct ordinal in 5 of 30 scenes, the pointer component captured 0.0622. Three random scenes (seed 29), raw:

- C2-0629 j=2 k=0 share 0.0033 sign-correct True: ' ricev' - 0.0039; ' Cron' + 0.0035; ' Char' + 0.0025; ' keduanya' - 0.0027; ' erstes' + 0.0033; 'racuse' - 0.0027; 'にとって' + 0.0028; ' Outro' - 0.0027; 'būt' + 0.0022; ' 왜' - 0.0031
- C2-0625 j=1 k=0 share 0.00259 sign-correct False: 'Пользова' - 0.0031; '’Unione' + 0.0032; 'incinnati' - 0.0030; ' vler' + 0.0031; ' ricev' - 0.0040; ' розта' + 0.0029; '�蟹' - 0.0031; 'ISOString' + 0.0030; 'izzera' - 0.0037; ' Hbf' + 0.0029
- C2-0035 j=1 k=2 share 0.0 sign-correct False: ' trapped' - 0.0029; '(IDC' + 0.0040; ' Alpha' + 0.0031; 'Пользова' - 0.0042; ' Jeho' + 0.0031; ' turnaround' - 0.0028; 'IPMENT' + 0.0033; 'roga' - 0.0028; 'anel' + 0.0032; ' пошел' - 0.0028

## qwen3.5-9b (L12, d = 4096)

Base rate: {'dictionary_tokens': 242132, 'ordinal_tokens': 103, 'cardinal_tokens': 229, 'generic_tokens': 201, 'position_tokens': 513, 'base_rate_any_position_class': 0.002119}

(a) position-atom energy share (mean over the six writes) 0.0 vs random 95th percentile 0.00331 (random mean 0.00036, shuffle mean 0.0); sign-correct ordinal on 0 of 6 pairs (rate 0.0) vs shuffle 0.0, random mean 0.007 / 95th percentile 0.0; rule: {'share_above_random_p95': False, 'sign_correct_on_most_pairs_above_shuffle': False, 'both': False}

Overlap: the 25-atom J++ part captures 0.101 of the pointer basis directions' energy ([0.0671, 0.0786, 0.0936, 0.1646]), the six writes [0.078, 0.0783, 0.0823], random vectors 0.0844

| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |
|---|---|---|---|
| 0->1 | 0.0 | False | ' methane' - 0.0041 -; '了些' + 0.0034 -; '지와' - 0.0047 -; '这两个' + 0.0033 -; ' mij' + 0.0029 -; 'ztat' - 0.0029 -; ' visar' + 0.0032 -; ' noastre' - 0.0033 -; ' описа' + 0.0037 -; 'رو' + 0.0032 - |
| 0->2 | 0.0 | False | '.species' - 0.0044 -; ' وعدد' + 0.0036 -; ' residue' - 0.0032 -; ' impart' + 0.0031 -; '지와' - 0.0034 -; 'Cancelable' + 0.0045 -; '这两' + 0.0029 -; ' Perlu' - 0.0037 -; '疲劳' + 0.0037 -; ' miejsc' + 0.0032 - |
| 1->0 | 0.0 | False | ' methane' + 0.0041 -; '了些' - 0.0034 -; '지와' + 0.0047 -; '这两个' - 0.0033 -; ' mij' - 0.0029 -; 'ztat' + 0.0029 -; ' visar' - 0.0032 -; ' noastre' + 0.0033 -; ' описа' - 0.0037 -; 'رو' - 0.0032 - |
| 1->2 | 0.0 | False | 'deer' - 0.0044 -; '疲劳' + 0.0048 -; '长腿' - 0.0034 -; '召唤' + 0.0035 -; 'kit' - 0.0034 -; ' infine' + 0.0029 -; ' piac' - 0.0032 -; 'ental' + 0.0029 -; '其次' - 0.0027 -; 'ORD' + 0.0031 - |
| 2->0 | 0.0 | False | '.species' + 0.0044 -; ' وعدد' - 0.0036 -; ' residue' + 0.0032 -; ' impart' - 0.0031 -; '지와' + 0.0034 -; 'Cancelable' - 0.0045 -; '这两' - 0.0029 -; ' Perlu' + 0.0037 -; '疲劳' - 0.0037 -; ' miejsc' - 0.0032 - |
| 2->1 | 0.0 | False | 'deer' + 0.0044 -; '疲劳' - 0.0048 -; '长腿' + 0.0034 -; '召唤' - 0.0035 -; 'kit' + 0.0034 -; ' infine' - 0.0029 -; ' piac' + 0.0032 -; 'ental' - 0.0029 -; '其次' + 0.0027 -; 'ORD' - 0.0031 - |

## qwen3.6-27b (L32, d = 5120)

Base rate: {'dictionary_tokens': 242132, 'ordinal_tokens': 103, 'cardinal_tokens': 229, 'generic_tokens': 201, 'position_tokens': 513, 'base_rate_any_position_class': 0.002119}

(a) position-atom energy share (mean over the six writes) 0.0 vs random 95th percentile 0.0 (random mean 9e-05, shuffle mean 0.0); sign-correct ordinal on 0 of 6 pairs (rate 0.0) vs shuffle 0.0, random mean 0.01 / 95th percentile 0.0; rule: {'share_above_random_p95': False, 'sign_correct_on_most_pairs_above_shuffle': False, 'both': False}

Overlap: the 25-atom J++ part captures 0.0681 of the pointer basis directions' energy ([0.0533, 0.0711, 0.0665, 0.0815]), the six writes [0.0603, 0.0676, 0.0799], random vectors 0.067

| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |
|---|---|---|---|
| 0->1 | 0.0 | False | ' lesqu' - 0.0035 -; '出て' + 0.0048 -; ' прове' - 0.0034 -; 'ง่ายดาย' + 0.0048 -; 'ementara' + 0.0039 -; '以前の' - 0.0033 -; '大大小小的' + 0.0039 -; '升初' - 0.0035 -; '/var' - 0.0029 -; 'ให้เลือก' + 0.0031 - |
| 0->2 | 0.0 | False | ' kebak' - 0.0036 -; '大大小小的' + 0.0042 -; '本身的' - 0.0034 -; 'ให้เลือก' + 0.0038 -; '被称为' + 0.0029 -; 'mut' - 0.0026 -; 'ującego' - 0.0029 -; 'รายละเอียด' + 0.0029 -; '<boolean' + 0.0027 -; ' прове' - 0.0030 - |
| 1->0 | 0.0 | False | ' lesqu' + 0.0035 -; '出て' - 0.0048 -; ' прове' + 0.0034 -; 'ง่ายดาย' - 0.0048 -; 'ementara' - 0.0039 -; '以前の' + 0.0033 -; '大大小小的' - 0.0039 -; '升初' + 0.0035 -; '/var' + 0.0029 -; 'ให้เลือก' - 0.0031 - |
| 1->2 | 0.0 | False | '这三个' + 0.0050 -; ' Bucks' - 0.0033 -; '本身的' - 0.0031 -; ' funkc' + 0.0030 -; '과의' - 0.0029 -; ' usług' + 0.0028 -; '质量技术监督' + 0.0027 -; ' مضيف' - 0.0024 -; '在许多' + 0.0020 -; '经济和' - 0.0022 - |
| 2->0 | 0.0 | False | ' kebak' + 0.0036 -; '大大小小的' - 0.0042 -; '本身的' + 0.0034 -; 'ให้เลือก' - 0.0038 -; '被称为' - 0.0029 -; 'mut' + 0.0026 -; 'ującego' + 0.0029 -; 'รายละเอียด' - 0.0029 -; '<boolean' - 0.0027 -; ' прове' + 0.0030 - |
| 2->1 | 0.0 | False | '这三个' - 0.0050 -; ' Bucks' + 0.0033 -; '本身的' + 0.0031 -; ' funkc' - 0.0030 -; '과의' + 0.0029 -; ' usług' - 0.0028 -; '质量技术监督' - 0.0027 -; ' مضيف' + 0.0024 -; '在许多' - 0.0020 -; '经济和' + 0.0022 - |

## nemotron-3.5-lightning (L14, d = 2688)

Base rate: {'dictionary_tokens': 124782, 'ordinal_tokens': 98, 'cardinal_tokens': 190, 'generic_tokens': 159, 'position_tokens': 433, 'base_rate_any_position_class': 0.00347}

(a) position-atom energy share (mean over the six writes) 0.00058 vs random 95th percentile 0.00244 (random mean 0.0003, shuffle mean 0.00058); sign-correct ordinal on 0 of 6 pairs (rate 0.0) vs shuffle 0.0, random mean 0.007 / 95th percentile 0.0; rule: {'share_above_random_p95': False, 'sign_correct_on_most_pairs_above_shuffle': False, 'both': False}

Overlap: the 25-atom J++ part captures 0.1308 of the pointer basis directions' energy ([0.0587, 0.0969, 0.1474, 0.2202]), the six writes [0.0728, 0.0844, 0.1117], random vectors 0.087

| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |
|---|---|---|---|
| 0->1 | 0.0 | False | '.accept' + 0.0037 -; '�n' - 0.0041 -; ' المز' + 0.0034 -; 'Trim' - 0.0044 -; ' الإقليمية' + 0.0049 -; ' embod' - 0.0047 -; 'Lear' - 0.0036 -; 'jima' + 0.0034 -; 'alin' - 0.0038 -; ' الكهربائية' - 0.0031 - |
| 0->2 | 0.00173 | False | ' mais' - 0.0039 -; ' Mayotte' + 0.0049 -; ' Nixon' - 0.0038 -; ' jos' + 0.0035 -; ' dort' + 0.0035 -; 'Stack' - 0.0039 -; ' incred' - 0.0031 -; ' Noord' + 0.0028 -; ' sui' + 0.0025 -; ' الذاتية' - 0.0031 - |
| 1->0 | 0.0 | False | '.accept' - 0.0037 -; '�n' + 0.0041 -; ' المز' - 0.0034 -; 'Trim' + 0.0044 -; ' الإقليمية' - 0.0049 -; ' embod' + 0.0047 -; 'Lear' + 0.0036 -; 'jima' - 0.0034 -; 'alin' + 0.0038 -; ' الكهربائية' + 0.0031 - |
| 1->2 | 0.0 | False | ' Thé' + 0.0060 -; ' cyt' - 0.0068 -; 'κ' + 0.0062 -; 'Bride' - 0.0082 -; ' Kapelle' + 0.0050 -; ' FBI' - 0.0062 -; ' unter' - 0.0055 -; 'Struct' + 0.0045 -; 'لق' - 0.0053 -; ' cena' + 0.0041 - |
| 2->0 | 0.00173 | False | ' mais' + 0.0039 -; ' Mayotte' - 0.0049 -; ' Nixon' + 0.0038 -; ' jos' - 0.0035 -; ' dort' - 0.0035 -; 'Stack' + 0.0039 -; ' incred' + 0.0031 -; ' Noord' - 0.0028 -; ' sui' - 0.0025 -; ' الذاتية' + 0.0031 - |
| 2->1 | 0.0 | False | ' Thé' - 0.0060 -; ' cyt' + 0.0068 -; 'κ' - 0.0062 -; 'Bride' + 0.0082 -; ' Kapelle' - 0.0050 -; ' FBI' + 0.0062 -; ' unter' + 0.0055 -; 'Struct' - 0.0045 -; 'لق' + 0.0053 -; ' cena' - 0.0041 - |

## qwen3.5-122b-a10b (L33, d = 3072)

Base rate: {'dictionary_tokens': 242132, 'ordinal_tokens': 103, 'cardinal_tokens': 229, 'generic_tokens': 201, 'position_tokens': 513, 'base_rate_any_position_class': 0.002119}

(a) position-atom energy share (mean over the six writes) 0.0 vs random 95th percentile 0.0 (random mean 0.0, shuffle mean 0.0); sign-correct ordinal on 0 of 6 pairs (rate 0.0) vs shuffle 0.0, random mean 0.0 / 95th percentile 0.0; rule: {'share_above_random_p95': False, 'sign_correct_on_most_pairs_above_shuffle': False, 'both': False}

Overlap: the 25-atom J++ part captures 0.1003 of the pointer basis directions' energy ([0.0668, 0.0688, 0.1006, 0.1649]), the six writes [0.0677, 0.0694, 0.083], random vectors 0.1003

| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |
|---|---|---|---|
| 0->1 | 0.0 | False | '四个意识' - 0.0033 -; 'Responder' + 0.0046 -; '山楂' - 0.0031 -; 'upos' + 0.0036 -; ' nef' - 0.0027 -; ' afterward' + 0.0037 -; '身上的' - 0.0027 -; '-feira' + 0.0026 -; '第一项' - 0.0027 -; '所述第二' + 0.0034 - |
| 0->2 | 0.0 | False | ' squirrel' - 0.0034 -; '.out' + 0.0037 -; 'นึก' - 0.0040 -; '-feira' + 0.0045 -; '企业地址' - 0.0035 -; '네요' + 0.0032 -; '_AF' - 0.0030 -; '为他' + 0.0028 -; ' tâ' - 0.0031 -; '一元' - 0.0024 - |
| 1->0 | 0.0 | False | '四个意识' + 0.0033 -; 'Responder' - 0.0046 -; '山楂' + 0.0031 -; 'upos' - 0.0036 -; ' nef' + 0.0027 -; ' afterward' - 0.0037 -; '身上的' + 0.0027 -; '-feira' - 0.0026 -; '第一项' + 0.0027 -; '所述第二' - 0.0034 - |
| 1->2 | 0.0 | False | '\\Mail' - 0.0059 -; 'ήμερα' + 0.0049 -; ' squirrel' - 0.0049 -; '(Util' - 0.0044 -; 'iating' + 0.0034 -; 'igrated' - 0.0032 -; '_estimators' + 0.0035 -; 'باعة' - 0.0031 -; ' apprentice' - 0.0034 -; ' rovn' + 0.0036 - |
| 2->0 | 0.0 | False | ' squirrel' + 0.0034 -; '.out' - 0.0037 -; 'นึก' + 0.0040 -; '-feira' - 0.0045 -; '企业地址' + 0.0035 -; '네요' - 0.0032 -; '_AF' + 0.0030 -; '为他' - 0.0028 -; ' tâ' + 0.0031 -; '一元' + 0.0024 - |
| 2->1 | 0.0 | False | '\\Mail' + 0.0059 -; 'ήμερα' - 0.0049 -; ' squirrel' + 0.0049 -; '(Util' + 0.0044 -; 'iating' - 0.0034 -; 'igrated' + 0.0032 -; '_estimators' - 0.0035 -; 'باعة' + 0.0031 -; ' apprentice' + 0.0034 -; ' rovn' - 0.0036 - |

