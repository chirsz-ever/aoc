#!/usr/bin/env python3

import sys
from dataclasses import dataclass
import re

@dataclass
class Machine:
    A: tuple[int, int]
    B: tuple[int, int]
    Prize: tuple[int, int]

reMachine = re.compile(r'''Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)''')

def main() -> None:
    inputFile = sys.argv[1]

    machines: list[Machine] = []
    with open(inputFile) as fin:
        for m in reMachine.findall(fin.read()):
            machines.append(Machine((int(m[0]), int(m[1])), (int(m[2]), int(m[3])), (int(m[4]) + 10000000000000, int(m[5]) + 10000000000000)))

    tokens = 0
    for m in machines:
        h = m.A[0] * m.B[1] - m.A[1] * m.B[0]
        k = m.A[0] * m.Prize[1] - m.A[1] * m.Prize[0]
        assert h != 0
        b = k // h
        print(f'{h=}, {k=}, {b=}')
        if b * h != k or b < 0:
            print(f'  cannot solve b')
            continue
        l = m.Prize[0] * m.A[1] - b * m.A[1] * m.B[0]
        n = m.A[0] * m.A[1]
        assert n != 0
        a = l // n
        print(f'  {l=}, {n=}, {a=}')
        if a * n != l or a < 0:
            print(f'  cannot solve a')
            continue
        tokens += 3 * a + b
    print(tokens)


if __name__ == '__main__':
    main()
