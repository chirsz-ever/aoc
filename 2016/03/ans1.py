#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    s = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            a, b, c = map(int, l.split())
            if a + b > c and a + c > b and b + c > a:
                s += 1
    print(s)


if __name__ == "__main__":
    main()
