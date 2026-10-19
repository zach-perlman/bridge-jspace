# exp20_competence: unedited greedy accuracy per task and format

✓: Wilson 95% lower bound ≥ 0.85 (reading aid). As run: the format part B's runs use.

| task | format | clean | cf | off | all three | hop1 | hop2 | clean, given both hops | median p(answer), clean |
|---|---|---|---|---|---|---|---|---|---|
| probe_swap | **raw** (as run) | 77/90 86% [77,91] | - | - | - | - | - | - | 0.64 |
| probe_swap | chat | 77/90 86% [77,91] | - | - | - | - | - | - | 0.97 |
| probe_swap | chat_prefill | 76/90 84% [76,91] | - | - | - | - | - | - | 0.81 |
| brew_bank | chat | 100/100 100% [96,100] ✓ | - | - | - | 100/100 100% [96,100] ✓ | 100/100 100% [96,100] ✓ | 100/100 100% [96,100] ✓ | 0.97 |
| brew_bank | **chat_prefill** (as run) | 100/100 100% [96,100] ✓ | - | - | - | 100/100 100% [96,100] ✓ | 100/100 100% [96,100] ✓ | 100/100 100% [96,100] ✓ | 0.79 |
| brew_fresh | chat | 178/200 89% [84,93] | - | - | - | 200/200 100% [98,100] ✓ | 200/200 100% [98,100] ✓ | 178/200 89% [84,93] | 0.88 |
| brew_fresh | **chat_prefill** (as run) | 177/200 88% [83,92] | - | - | - | 200/200 100% [98,100] ✓ | 200/200 100% [98,100] ✓ | 177/200 88% [83,92] | 0.61 |
| brew_test | chat | 519/600 86% [84,89] | - | - | - | 600/600 100% [99,100] ✓ | 600/600 100% [99,100] ✓ | 519/600 86% [84,89] | 0.89 |
| brew_test | **chat_prefill** (as run) | 522/600 87% [84,89] | - | - | - | 600/600 100% [99,100] ✓ | 600/600 100% [99,100] ✓ | 522/600 87% [84,89] | 0.61 |
| R | **raw** (as run) | 274/360 76% [71,80] | 277/360 77% [72,81] | 271/360 75% [71,79] | 189/360 52% [47,58] | 359/360 100% [98,100] ✓ | 360/360 100% [99,100] ✓ | 273/359 76% [71,80] | 0.20 |
| R | chat | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 0.99 |
| R | chat_prefill | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 360/360 100% [99,100] ✓ | 0.81 |
| B | **raw** (as run) | 378/400 94% [92,96] ✓ | 377/400 94% [92,96] ✓ | 369/400 92% [89,94] ✓ | 345/400 86% [83,89] | 78/400 20% [16,24] | 400/400 100% [99,100] ✓ | 71/78 91% [83,96] | 0.30 |
| B | chat | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 0.99 |
| B | chat_prefill | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 0.88 |
| L | **raw** (as run) | 394/400 98% [97,99] ✓ | 394/400 98% [97,99] ✓ | 393/400 98% [96,99] ✓ | 385/400 96% [94,98] ✓ | 6/400 2% [1,3] | 275/400 69% [64,73] | 4/4 100% [51,100] | 0.48 |
| L | chat | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 0.97 |
| L | chat_prefill | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 400/400 100% [99,100] ✓ | 0.90 |
| RL | **raw** (as run) | 693/720 96% [95,97] ✓ | 705/720 98% [97,99] ✓ | 698/720 97% [95,98] ✓ | 676/720 94% [92,95] ✓ | 720/720 100% [99,100] ✓ | 492/720 68% [65,72] | 468/492 95% [93,97] ✓ | 0.49 |
| RL | chat | 718/720 100% [99,100] ✓ | 719/720 100% [99,100] ✓ | 718/720 100% [99,100] ✓ | 716/720 99% [99,100] ✓ | 720/720 100% [99,100] ✓ | 720/720 100% [99,100] ✓ | 718/720 100% [99,100] ✓ | 0.97 |
| RL | chat_prefill | 717/720 100% [99,100] ✓ | 719/720 100% [99,100] ✓ | 717/720 100% [99,100] ✓ | 716/720 99% [99,100] ✓ | 720/720 100% [99,100] ✓ | 720/720 100% [99,100] ✓ | 717/720 100% [99,100] ✓ | 0.86 |

## Wrong answers by role (clean)

- probe_swap / raw: {'wrong': 13}
- probe_swap / chat: {'wrong': 13}
- probe_swap / chat_prefill: {'wrong': 14}
- brew_fresh / chat: {'intermediate': 13, 'other': 9}
- brew_fresh / chat_prefill: {'intermediate': 12, 'start': 1, 'other': 10}
- brew_test / chat: {'intermediate': 40, 'other': 37, 'start': 4}
- brew_test / chat_prefill: {'intermediate': 43, 'other': 33, 'start': 2}
- R / raw: {'target': 19, 'none': 61, 'third': 6}
- B / raw: {'none': 12, 'target': 5, 'third': 5}
- L / raw: {'none': 6}
- RL / raw: {'other': 24, 'third': 2, 'none': 1}
- RL / chat: {'third': 2}
- RL / chat_prefill: {'third': 2, 'target': 1}

## Examples of wrong clean answers (first 4 per task and format)

- probe_swap / raw / atomic-80-state: expected 'liquid', said ' solid.\nQuestion: The state of matter at room temperature of the element with'
- probe_swap / raw / bird-country-eagle: expected 'America', said ' the United States.\nQuestion: The country whose national emblem is the bird with'
- probe_swap / raw / chem-bones-Z: expected '20', said ' 26. What is the name of this metal?\n\n<think>\n\n</think>'
- probe_swap / raw / etym-frigg-position: expected '5', said ' 2.\nQuestion: What is the day of the week named after the'
- probe_swap / chat / atomic-80-state: expected 'liquid', said 'solid'
- probe_swap / chat / bird-country-eagle: expected 'America', said 'the United States'
- probe_swap / chat / etym-frigg-position: expected '5', said '2'
- probe_swap / chat / etym-saturn-position: expected '6', said 'four'
- probe_swap / chat_prefill / atomic-80-state: expected 'liquid', said ' solid'
- probe_swap / chat_prefill / bird-country-eagle: expected 'America', said ' the United States'
- probe_swap / chat_prefill / etym-frigg-position: expected '5', said ' 2'
- probe_swap / chat_prefill / etym-saturn-position: expected '6', said ' 8'
- brew_fresh / chat / brewfresh-0009: expected 'brown', said 'gold'
- brew_fresh / chat / brewfresh-0010: expected 'orange', said 'gray'
- brew_fresh / chat / brewfresh-0043: expected 'white', said 'gold'
- brew_fresh / chat / brewfresh-0046: expected 'gray', said 'white'
- brew_fresh / chat_prefill / brewfresh-0009: expected 'brown', said ' gold'
- brew_fresh / chat_prefill / brewfresh-0016: expected 'red', said ' gray'
- brew_fresh / chat_prefill / brewfresh-0022: expected 'gold', said ' black'
- brew_fresh / chat_prefill / brewfresh-0043: expected 'white', said ' gold'
- brew_test / chat / brewtest-0015: expected 'green', said 'pink'
- brew_test / chat / brewtest-0018: expected 'brown', said 'purple'
- brew_test / chat / brewtest-0037: expected 'black', said 'purple'
- brew_test / chat / brewtest-0043: expected 'gray', said 'purple'
- brew_test / chat_prefill / brewtest-0018: expected 'brown', said ' purple'
- brew_test / chat_prefill / brewtest-0023: expected 'red', said ' gray'
- brew_test / chat_prefill / brewtest-0035: expected 'blue', said ' black'
- brew_test / chat_prefill / brewtest-0044: expected 'purple', said ' blue'
- R / raw / R-0000: expected 'Paris', said '\nA. Moscow\nB. Paris\nC. Beijing\nD. London'
- R / raw / R-0000: expected 'Paris', said '\nA. Moscow\nB. Paris\nC. Berlin\nD. London'
- R / raw / R-0018: expected 'Paris', said "\n\n<think>\nHere's a thinking process:\n\n1.  **Analyze"
- R / raw / R-0054: expected 'Madrid', said "\n\n<think>\nHere's a thinking process:\n\n1.  **Analyze"
- B / raw / B-0000: expected 'Athens', said "\nA.\n\n<think>\nHere's a thinking process:\n\n1. "
- B / raw / B-0000: expected 'Ottawa', said "\nA.\n\n<think>\nHere's a thinking process:\n\n1. "
- B / raw / B-0000: expected 'Athens', said ':\n\n<think>\n\n</think>\n\nSam lives in Greece. The capital of Greece is'
- B / raw / B-0000: expected 'Beijing', said '\nA. Madrid\nB. Rome\nC. Beijing\nD. Paris'
- L / raw / L-0052: expected 'brown', said ' of the country where Mark lives. The country where Henry lives has the colour of'
- L / raw / L-0116: expected 'white', said ' of the country where Emma lives. The country where Tom lives has the colour of'
- L / raw / L-0117: expected 'white', said ' of the country where Victor lives. The country where Alice lives has the colour of'
- L / raw / L-0132: expected 'gold', said ' of the flag of the country where Emma lives. The country where Emma lives has'
- RL / raw / RL-0039: expected 'white', said ' red. The country where Paris is located has the people who are called French.'
- RL / raw / RL-0045: expected 'white', said ' red. The country where Paris is located has the colour green. The country where'
- RL / raw / RL-0051: expected 'black', said ' pink. The country where Paris is located has the colour black. The country where'
- RL / raw / RL-0056: expected 'green', said ' red. The country where Paris is located has the color green. The country where'
- RL / chat / RL-0243: expected 'teal', said 'black'
- RL / chat / RL-0342: expected 'blue', said 'brown'
- RL / chat_prefill / RL-0243: expected 'teal', said ' black'
- RL / chat_prefill / RL-0339: expected 'teal', said ' orange'
- RL / chat_prefill / RL-0342: expected 'blue', said ' brown'
