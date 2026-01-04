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
        if possible(d, pats):
            # print(f'{d} is ok')
            s += 1
        else:
            # print(f'{d} is impossible')
            pass
    print(s)

def possible(d: str, pats: list[str]) -> bool:
    @cache
    def step(offset: int) -> bool:
        if offset == len(d):
            return True
        for p in pats:
            if d.startswith(p, offset):
                if step(offset + len(p)):
                    return True
        return False
    return step(0)

if __name__ == '__main__':
    main()
