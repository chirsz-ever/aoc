#!/usr/bin/env python3

import sys


def main() -> None:
    row = int(sys.argv[1])
    column = int(sys.argv[2])

    n = row + column - 1
    order = n * (n - 1) // 2 + column
    # print(order)

    code = 20151125
    for _ in range(1, order):
        code = step(code)
    print(code)

def step(n: int) -> int:
    return n * 252533 % 33554393

if __name__ == "__main__":
    main()
