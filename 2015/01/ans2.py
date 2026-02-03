#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]
    with open(inputFile) as fin:
        content = fin.read().strip()

    l = 0
    for i, c in enumerate(content):
        if c == '(':
            l += 1
        elif c == ')':
            l -= 1
        if l == -1:
            print(i + 1)
            break


if __name__ == "__main__":
    main()
