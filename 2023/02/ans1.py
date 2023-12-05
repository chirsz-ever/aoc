#!/usr/bin/env python3

import sys
import re

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

# print(f'{records=}')

max_nums = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

s = 0
for index, rgb_results in records:
    possible = True
    for single_rgb in rgb_results:
        for c in ['red', 'green', 'blue']:
            if single_rgb.get(c, 0) > max_nums[c]:
                possible = False
                break
        if not possible:
            break
    if possible:
        print(f'game {index} is possible')
        s += index

print(f'{s=}')
