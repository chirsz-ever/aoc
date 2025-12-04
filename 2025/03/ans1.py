#!/usr/bin/env python3

import sys

def find_max2(l: str) -> int:
    ms = [int(c) for c in l]
    m1 = ms[0]
    m1i = 0
    for i in range(0, len(ms) - 1):
        if ms[i] > m1:
            m1 = ms[i]
            m1i = i
    m2 = ms[m1i + 1]
    m2i = m1i + 1
    for i in range(m1i + 1, len(ms)):
        if ms[i] > m2:
            m2 = ms[i]
            m2i = i
    return m1 * 10 + m2

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    s = 0
    with open(inputFile) as fin:
        for l in fin:
            n = find_max2(l.strip())
            s += n
    print(f'{s=}')

if __name__ == '__main__':
    main()
