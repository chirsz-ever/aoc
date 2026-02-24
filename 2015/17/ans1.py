#!/usr/bin/env python3

import sys
from functools import cache


def main() -> None:
    inputFile = sys.argv[1]
    total = int(sys.argv[2]) if len(sys.argv) >= 3 else 150

    with open(inputFile) as fin:
        liters = [int(n) for n in fin.read().split()]
    # print(liters)

    @cache
    def step(target: int, i: int) -> int:
        if target == 0:
            return 1
        if i >= len(liters):
            return 0
        if target >= liters[i]:
            return step(target - liters[i], i + 1) + step(target, i + 1)
        else:
            return step(target, i + 1)

    n = step(total, 0)
    print(n)

if __name__ == "__main__":
    main()
