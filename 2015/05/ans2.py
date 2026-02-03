#!/usr/bin/env python3

import sys
import re


def main() -> None:
    inputFile = sys.argv[1]

    strs = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            strs.append(l)

    cnt = 0
    for s in strs:
        if is_nice(s):
            # print(f'{s} is nice')
            cnt += 1
        else:
            # print(f'{s} is not nice')
            pass
    print(cnt)

re1 = re.compile(r'(..).*\1')
re2 = re.compile(r'(.).\1')

def is_nice(s: str) -> bool:
    return bool(re1.search(s) and re2.search(s))

if __name__ == "__main__":
    main()
