#!/usr/bin/env python3

import sys
from typing import Generator, Optional
from math import prod

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

def search_num(r: int, c: int) -> Optional[tuple[str, int ,int]]:
    if not schematic[r][c].isdigit():
        return
    for n, rn, cn in nums:
        if r != rn:
            continue
        if cn <= c < cn + len(n):
            return (n, rn, cn)


if __name__ == '__main__':
    nums = parse_schematic()
    # print(f'{nums}')
    s = 0
    for r, row in enumerate(schematic):
        for c, grid in enumerate(row):
            if grid != '*':
                continue
            gear_nums: set[tuple[str, int ,int]] = set()
            for r1, c1 in coords(r, c, 1):
                if n := search_num(r1, c1):
                    gear_nums.add(n)
            if len(gear_nums) >= 2:
                print(f'gear at {(r, c)}: {gear_nums}')
                s += prod(int(t[0]) for t in gear_nums)


    print(f'{s=}')
