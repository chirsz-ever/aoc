#!/usr/bin/env python3

import sys
from math import prod

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

def to_single_record(rgb_result: str) -> dict[str, int]:
    r = {}
    for t in rgb_result.split(','):
        n, color = t.split()
        r[color.strip()] = int(n.strip())
    return r


records: list[tuple[int, list[dict[str, int]]]] = []
with open(inputFile) as fin:
    for l in fin:
        game_id, bag_tries = l.split(':')
        game_id = int(game_id.split()[1])
        record = [to_single_record(single_try) for single_try in bag_tries.split(';') if len(single_try.split()) > 0]
        records.append((game_id, record))



s = 0
for index, rgb_results in records:
    min_possible = {'red': 0, 'green': 0, 'blue': 0}
    for single_rgb in rgb_results:
        for c in ['red', 'green', 'blue']:
            if (n := single_rgb.get(c)) and n > min_possible.get(c, 0):
                min_possible[c] = n
    # print(f'game {index}: {min_possible}')
    s += prod(min_possible.values())

print(f'{s=}')
