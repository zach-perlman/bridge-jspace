# exp20_competence: unedited greedy accuracy per task and format

✓: Wilson 95% lower bound ≥ 0.85 (reading aid). As run: the format part B's runs use.

| task | format | clean | cf | off | all three | hop1 | hop2 | hop3 | clean, given every hop | median p(answer), clean |
|---|---|---|---|---|---|---|---|---|---|---|
| probe_swap | **raw** (as run) | 68/90 76% [66,83] | - | - | - | - | - | - | - | 0.43 |
| probe_swap | chat | 68/90 76% [66,83] | - | - | - | - | - | - | - | 0.68 |
| probe_swap | chat_prefill | 70/90 78% [68,85] | - | - | - | - | - | - | - | 0.66 |
| brew_test | chat | 163/600 27% [24,31] | - | - | - | 598/600 100% [99,100] ✓ | 598/600 100% [99,100] ✓ | - | 163/596 27% [24,31] | 0.20 |
| brew_test | **chat_prefill** (as run) | 225/600 38% [34,41] | - | - | - | 590/600 98% [97,99] ✓ | 593/600 99% [98,99] ✓ | - | 218/583 37% [34,41] | 0.19 |

## Wrong answers by role (clean)

- probe_swap / raw: {'wrong': 22}
- probe_swap / chat: {'wrong': 22}
- probe_swap / chat_prefill: {'wrong': 20}
- brew_test / chat: {'intermediate': 290, 'other': 141, 'start': 6}
- brew_test / chat_prefill: {'other': 200, 'start': 9, 'intermediate': 166}

## Examples of wrong clean answers (first 4 per task and format)

- probe_swap / raw / atomic-80-state: expected 'liquid', said ' solid.\nQuestion: What is the state of matter at room temperature of the'
- probe_swap / raw / basketball-players: expected '5', said ' 11.\nQuestion: What is the sport?\nAnswer:\n\n'
- probe_swap / raw / beverage-source-wine: expected 'grape', said ' same fruit that is used to make the alcoholic drink known as brandy.\n'
- probe_swap / raw / bird-time-owl: expected 'night', said ' the same as the time of day when the animal that is a mammal and'
- probe_swap / chat / atomic-80-state: expected 'liquid', said 'solid\n'
- probe_swap / chat / basketball-players: expected '5', said '11\n'
- probe_swap / chat / bird-country-eagle: expected 'America', said 'India\n'
- probe_swap / chat / chem-photosynthesis-Z: expected '8', said '2\n'
- probe_swap / chat_prefill / atomic-80-state: expected 'liquid', said ' solid\n'
- probe_swap / chat_prefill / basketball-players: expected '5', said ' 11\n'
- probe_swap / chat_prefill / bird-country-eagle: expected 'America', said ' India\n'
- probe_swap / chat_prefill / element-color-gold2: expected 'yellow', said ' gold\n'
- brew_test / chat / brewtest-0000: expected 'teal', said 'black\n'
- brew_test / chat / brewtest-0001: expected 'black', said 'pink\n'
- brew_test / chat / brewtest-0002: expected 'white', said 'green\n'
- brew_test / chat / brewtest-0003: expected 'teal', said 'orange\n'
- brew_test / chat_prefill / brewtest-0000: expected 'teal', said ' gray\n'
- brew_test / chat_prefill / brewtest-0002: expected 'white', said ' red\n'
- brew_test / chat_prefill / brewtest-0006: expected 'red', said ' gray\n'
- brew_test / chat_prefill / brewtest-0007: expected 'gold', said ' gray\n'
