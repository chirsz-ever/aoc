#!/usr/bin/env python3

import sys

def find_max12(l: str) -> int:
    ms = [int(c) for c in l]
    N = 12
    # start
    s = 0
    r = 0
    for i in range(0, N):
        mi = ms[s]
        mi_index = s
        for k in range(s, len(ms) - N + i + 1):
            if ms[k] > mi:
                mi = ms[k]
                mi_index = k
        s = mi_index + 1
        r = r * 10 + mi
    # print(f'{r=}')
    return r

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    s = 0
    with open(inputFile) as fin:
        for l in fin:
            n = find_max12(l.strip())
            s += n
    print(f'{s=}')

if __name__ == '__main__':
    main()
