#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    dial = 50
    t = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if l[0] == 'L':
                dial = (dial - int(l[1:])) % 100
            else:
                dial = (dial + int(l[1:])) % 100
            if dial == 0:
                t += 1
    print(f'{t=}')

if __name__ == '__main__':
    main()
