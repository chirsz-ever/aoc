#!/usr/bin/env python3

import sys

def is_invalid(d):
    s = str(d)
    l = len(s)
    return l % 2 == 0 and s[:l//2] == s[l//2:]

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        content = fin.read()

    s = 0
    for r in content.split(','):
        f, l = map(int, r.strip().split('-'))
        for d in range(f, l + 1):
            if is_invalid(d):
                # print(d)
                s += d
    print(f'{s=}')

if __name__ == '__main__':
    main()
