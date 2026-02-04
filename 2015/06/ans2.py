#!/usr/bin/env python3

import sys
import re
from typing import Iterable

reInst = re.compile(r'(?P<op>.*) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)')

ON = 0
OFF = 1
TOGGLE = 2

op_map = {
    'turn on': ON,
    'turn off': OFF,
    'toggle': TOGGLE,
}

def main() -> None:
    inputFile = sys.argv[1]

    insts: list[tuple[int, int, int, int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            m = reInst.match(l)
            assert m, l
            op = op_map[m['op']]
            x1 = int(m['x1'])
            y1 = int(m['y1'])
            x2 = int(m['x2'])
            y2 = int(m['y2'])
            insts.append((op, x1, y1, x2, y2))

    lights = [[0 for _ in range(1000)] for _ in range(1000)]

    for op, x1, y1, x2, y2 in insts:
        if op == ON:
            for x in range_inclusive(x1, x2):
                for y in range_inclusive(y1, y2):
                    lights[x][y] += 1
        elif op == OFF:
            for x in range_inclusive(x1, x2):
                for y in range_inclusive(y1, y2):
                    lights[x][y] = 0 if lights[x][y] == 0 else lights[x][y] - 1
        elif op == TOGGLE:
            for x in range_inclusive(x1, x2):
                for y in range_inclusive(y1, y2):
                    lights[x][y] = lights[x][y] + 2
    print(sum(sum(r) for r in lights))

def range_inclusive(a: int, b: int) -> Iterable[int]:
    if a <= b:
        return range(a, b + 1)
    else:
        return range(b, a + 1)

if __name__ == "__main__":
    main()
