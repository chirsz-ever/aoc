#!/usr/bin/env python3

import sys

def main() -> None:
    global w, h
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    ranges = []
    state = 0
    ids = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                state = 1
            else:
                if state == 0:
                    l, h = map(int, l.split('-'))
                    ranges.append((l, h))
                else:
                    ids.append(int(l))

    # print(ranges)
    # print(ids)

    cnt = 0
    for i in ids:
        for l, h in ranges:
            if l <= i <= h:
                cnt += 1
                break
    print(f'{cnt=}')

if __name__ == '__main__':
    main()
