#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    sizes = []
    with open(inputFile) as fin:
        content = fin.read().strip()

    visited = {(0, 0)}
    i, j = 0, 0
    for c in content:
        if c == '^':
            i -= 1
        elif c == 'v':
            i += 1
        elif c == '>':
            j += 1
        elif c == '<':
            j -= 1
        visited.add((i, j))

    print(len(visited))

if __name__ == "__main__":
    main()
