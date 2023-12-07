#!/usr/bin/env python3

import sys
from typing import Generator

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

schematic: list[str] = []
with open(inputFile) as fin:
    for l in fin:
        if len(l.strip()) != 0:
            schematic.append(l.strip())

def parse_schematic() -> list[tuple[str, int, int]]:
    nums: list[tuple[str, int, int]] = []
    for r, row in enumerate(schematic):
        n = ''
        start_col = 0
        for i, c in enumerate(row):
            if c.isdigit():
                if n == '':
                    start_col = i
                n += c
            elif len(n) != 0:
                nums.append((n, r, start_col))
                n = ''
        if len(n) != 0:
            nums.append((n, r, start_col))
            n = ''
    return nums

def coords(row: int, start_col: int, l: int) -> Generator[tuple[int, int], None, None]:
    if 0 <= row - 1 < len(schematic):
        for c in range(start_col - 1, start_col + l + 1):
            if 0 <= c < len(schematic[0]):
                yield row - 1, c
    if 0 <= start_col - 1 < len(schematic[0]):
        yield row, start_col - 1
    if 0 <= start_col + l < len(schematic[0]):
        yield row, start_col + l
    if 0 <= row + 1 < len(schematic):
        for c in range(start_col - 1, start_col + l + 1):
            if 0 <= c < len(schematic[0]):
                yield row + 1, c

if __name__ == '__main__':
    nums = parse_schematic()
    # print(f'{nums}')
    s = 0
    for n, row, start_col in nums:
        has_neighbor = False
        for r, c in coords(row, start_col, len(n)):
            k = schematic[r][c]
            if k != '.' and not k.isdigit():
                print(f'{n} has neighbor at {(r, c)}')
                has_neighbor = True
                break
        if has_neighbor:
            s += int(n)
        else:
            print(f'{n} not has neighbor')


    print(f'{s=}')
