#!/usr/bin/env python3

import sys
import re

reMul = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        content = fin.read()

    s = 0
    for m in reMul.findall(content):
        # print(m)
        s += int(m[0]) * int(m[1])
    print(s)

if __name__ == '__main__':
    main()
