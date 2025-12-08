#!/usr/bin/env python3

import sys
import re

reSpaces = re.compile(' +')

def prod(ns):
    p = 1
    for n in ns:
        p *= n
    return p

def main() -> None:
    global w, h
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    numbers: list[list[int]] = []
    ops: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            ns = reSpaces.split(l)
            if ns[0].isdecimal():
                numbers.append([int(n) for n in ns])
            else:
                ops = ns
                break

    # print(numbers)
    # print(ops)

    s = 0
    for j in range(0, len(numbers[0])):
        if ops[j] == '+':
            f = sum
        else:
            assert ops[j] == '*'
            f = prod
        r = f(numbers[i][j] for i in range(0, len(numbers)))
        s += r
    print(f'{s=}')

if __name__ == '__main__':
    main()
