#!/usr/bin/env python3

import sys

def my_hash(s: str) -> int:
    h = 0
    for c in s:
        n = ord(c)
        h += n
        h *= 17
        h %= 256
    return h

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        inputs: list[str] = fin.read().strip().split(',')

    result = 0
    for s in inputs:
        r1 = my_hash(s)
        # print(r1)
        result += r1
    print(f'{result=}')


if __name__ == '__main__':
    main()
