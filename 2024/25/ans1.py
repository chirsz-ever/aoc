#!/usr/bin/env python3

import sys
from itertools import product

def main() -> None:
    inputFile = sys.argv[1]

    keys: list[list[int]] = []
    locks: list[list[int]] = []
    with open(inputFile) as fin:
        lines = [l.strip() for l in fin]
        i = 0
        while i < len(lines):
            if not lines[i]:
                i += 1
                continue
            sch = lines[i:i+7]
            if is_key(sch):
                keys.append(to_nums(sch))
            elif is_lock(sch):
                locks.append(to_nums(sch))
            else:
                raise RuntimeError(f'{sch} is not key or lock')
            i += 7
    # print(f'{keys=}')
    # print(f'{locks=}')
    s = 0
    for k, l in product(keys, locks):
        if all(k[i] + l[i] <= 7 for i in range(5)):
            s += 1
    print(s)

def is_lock(sch: list[str]) -> bool:
    return all(c == '#' for c in sch[0])

def is_key(sch: list[str]) -> bool:
    return all(c == '#' for c in sch[-1])

def to_nums(sch: list[str]) -> list[int]:
    return [sum(int(sch[i][j]=='#') for i in range(len(sch))) for j in range(len(sch[0]))]

if __name__ == '__main__':
    main()
