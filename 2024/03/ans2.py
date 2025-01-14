#!/usr/bin/env python3

import sys
import re

reMul = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        content = fin.read()

    s = 0
    enable = True
    for m in reMul.finditer(content):
        # print(m)
        if m[0] == "do()":
            enable = True
        elif m[0] == "don't()":
            enable = False
        else:
            if enable:
                s += int(m[1]) * int(m[2])
    print(s)

if __name__ == '__main__':
    main()
