#!/usr/bin/env python3

import sys
import re

reRepeat = re.compile(r'(.+)\1+')

def is_invalid(d):
    return reRepeat.fullmatch(str(d))

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
                print(d)
                s += d
    print(f'{s=}')

if __name__ == '__main__':
    main()
