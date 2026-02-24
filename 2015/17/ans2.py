#!/usr/bin/env python3

import sys
from functools import cache


def main() -> None:
    inputFile = sys.argv[1]
    total = int(sys.argv[2]) if len(sys.argv) >= 3 else 150

    with open(inputFile) as fin:
        liters = [int(n) for n in fin.read().split()]
    # print(liters)

    min_used = len(liters)

    def step1(target: int, i: int, used: int) -> int:
        nonlocal min_used
        if target == 0:
            min_used = min(min_used, used)
            return 1
        if i >= len(liters):
            return 0
        if target >= liters[i]:
            return step1(target - liters[i], i + 1, used + 1) + step1(target, i + 1, used)
        else:
            return step1(target, i + 1, used)

    def step2(target: int, i: int, used: int) -> int:
        if target == 0:
            return int(used == min_used)
        if i >= len(liters):
            return 0
        if target >= liters[i]:
            return step2(target - liters[i], i + 1, used + 1) + step2(target, i + 1, used)
        else:
            return step2(target, i + 1, used)

    step1(total, 0, 0)
    min_ways = step2(total, 0, 0)

    print(f'{min_used=}')
    print(min_ways)

if __name__ == "__main__":
    main()
