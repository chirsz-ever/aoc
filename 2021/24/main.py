#!/usr/bin/env python3

import sys
import re


def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default


inputFile = getArg(1, "input")

reStep = re.compile(
'''inp w
mul x 0
add x z
mod x 26
div z (?P<d>-?\d+)
add x (?P<a>-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (?P<b>-?\d+)
mul y x
add z y
'''
)

insts = ""
with open(inputFile) as fin:
    insts = fin.read()
    cnt = 0
    for m in reStep.finditer(insts):
        cnt += 1
        d = int(m['d'])
        a = int(m['a'])
        b = int(m['b'])
        print(f"{cnt:2}: {d = :3} {a = :3}, {b = :3}")