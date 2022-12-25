#!/usr/bin/env python3

import sys
from collections import deque

inputFile = "input"
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

def read_input(fname) -> list[str]:
    ns: list[str] = []
    with open(fname) as fin:
        for row, l in enumerate(fin):
            l = l.rstrip()
            if len(l) == 0:
                continue
            ns.append(l)
    return ns

s2d = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

def s2t(s: str) -> int:
    t = 0
    for x in s:
        d = s2d[x]
        t = t * 5 + d
    return t

# https://stackoverflow.com/a/28666223
def numberToBase(n, b) -> list[int]:
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits

d2s = {v: k for k, v in s2d.items()}

def t2s(n: int) -> str:
    n5 = numberToBase(n, 5)
    c = 0
    ss = []
    for d in n5:
        d += c
        assert d <= 5
        if d > 2:
            d -= 5
            c = 1
        else:
            c = 0
        ss.append(d)
    if c != 0:
        ss.append(c)
    return ''.join([d2s[d] for d in ss[::-1]])

def main() -> None:
    ns = read_input(inputFile)
    ts = [s2t(s) for s in ns]
    # for t in ts:
    #     print(t)
    sum_t = sum(ts)
    print(sum_t)
    print(t2s(sum_t))


if __name__ == '__main__':
    main()
