#!/usr/bin/env python3

import sys
from functools import cmp_to_key

def match_rule(u: list[int], r: tuple[int, int]) -> bool:
    a, b = r
    return a not in u or b not in u or u.index(a) < u.index(b)

def my_cmp(a: int, b: int, rules: set[tuple[int, int]]) -> int:
    if (a, b) in rules:
        return -1
    if (b, a) in rules:
        return 1
    return 0

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
    rules_set = set(rules)
    for u in updates:
        if not all(match_rule(u, r) for r in rules):
            u1 = sorted(u, key=cmp_to_key(lambda a, b: my_cmp(a, b, rules_set)))
            cnt += u1[len(u1) // 2]
    print(cnt)

if __name__ == '__main__':
    main()
