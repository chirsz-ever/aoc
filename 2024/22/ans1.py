#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        secret_numbers = list(int(l.strip()) for l in fin if l.strip())

    n2000 = []
    for n in secret_numbers:
        for _ in range(2000):
            n = step(n)
        n2000.append(n)
    print(sum(n2000))

def step(n: int) -> int:
    n = ((n << 6) ^ n) & 0xFFFFFF
    n = ((n >> 5) ^ n) & 0xFFFFFF
    n = ((n << 11) ^ n) & 0xFFFFFF
    return n

if __name__ == '__main__':
    main()
