#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    sizes = []
    with open(inputFile) as fin:
        content = fin.read().strip()

    visited = {(0, 0)}
    i = [0, 0]
    j = [0, 0]
    for kc, c in enumerate(content):
        k = kc % 2
        if c == "^":
            i[k] -= 1
        elif c == "v":
            i[k] += 1
        elif c == ">":
            j[k] += 1
        elif c == "<":
            j[k] -= 1
        visited.add((i[k], j[k]))

    print(len(visited))


if __name__ == "__main__":
    main()
