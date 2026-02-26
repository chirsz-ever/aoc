#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    nums: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            a, b, c = map(int, l.split())
            nums.append([a, b, c])

    s = 0
    for i in range(0, len(nums), 3):
        for j in range(0, len(nums[i])):
            a = nums[i][j]
            b = nums[i+1][j]
            c = nums[i+2][j]
            if a + b > c and a + c > b and b + c > a:
                s += 1
    print(s)


if __name__ == "__main__":
    main()
