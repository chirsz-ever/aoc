#!/usr/bin/env python3

import sys

def match_rule(u: list[int], r: tuple[int, int]) -> bool:
    a, b = r
    return a not in u or b not in u or u.index(a) < u.index(b)

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    rules: list[tuple[int, int]] = []
    updates: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                continue
            if '|' in l:
                rules.append(tuple(map(int, l.split('|'))))
            else:
                updates.append([int(x) for x in l.split(',')])
    # print(rules)
    # print(updates)

    cnt = 0
    for u in updates:
        if all(match_rule(u, r) for r in rules):
            cnt += u[len(u)//2]
    print(cnt)

if __name__ == '__main__':
    main()
