#!/usr/bin/env python3

import sys
from functools import cache

def main() -> None:
    inputFile = sys.argv[1]

    pats: list[str] = []
    designs: list[str] = []
    with open(inputFile) as fin:
        for i, l in enumerate(fin):
            l = l.strip()
            if i == 0:
                pats = l.strip().split(', ')
            elif l:
                designs.append(l)

    s = 0
    for d in designs:
        pw = possible_ways(d, pats)
        # print(f'{d}: {pw}')
        s += pw
    print(s)

def possible_ways(d: str, pats: list[str]) -> int:
    @cache
    def ways(offset: int) -> int:
        if offset == len(d):
            return 1
        w = 0
        for p in pats:
            if d.startswith(p, offset):
                w += ways(offset + len(p))
        return w
    return ways(0)

if __name__ == '__main__':
    main()
