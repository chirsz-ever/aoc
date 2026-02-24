#!/usr/bin/env python3

import sys


def main() -> None:
    # inputFile = sys.argv[1]
    input_num = int(sys.argv[1])

    houses = [0] * (input_num // 11)
    for elf in range(1, len(houses)):
        for h in range(elf, min(len(houses), elf * 50 + 1), elf):
            houses[h] += elf * 11
    for h in range(1, len(houses)):
        if houses[h] >= input_num:
            print(h, houses[h])
            break

if __name__ == "__main__":
    main()
